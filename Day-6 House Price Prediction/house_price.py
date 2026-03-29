"""
=============================================================
PROJECT 2: House Price Prediction — End-to-End Regression
=============================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.inspection import permutation_importance

import warnings, os
warnings.filterwarnings("ignore")
os.makedirs("outputs", exist_ok=True)

# ─── 1. LOAD & EXPLORE DATA ──────────────────────────────────────────────────
housing = fetch_california_housing(as_frame=True)
df = housing.frame.copy()
df.columns = [*housing.feature_names, "MedHouseValue"]

print("=" * 65)
print("       HOUSE PRICE PREDICTION — ANALYSIS REPORT")
print("=" * 65)
print(f"\n{'Dataset Shape:':<30} {df.shape}")
print(f"{'Features:':<30} {list(housing.feature_names)}")
print(f"{'Target:':<30} MedHouseValue (100k USD)")
print(f"\n{'─'*65}")
print("BASIC STATISTICS:")
print(df.describe().round(3).to_string())

# ─── 2. EDA — CORRELATION HEATMAP ────────────────────────────────────────────
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(11, 8))
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
cmap = sns.diverging_palette(230, 20, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
            annot=True, fmt=".2f", square=True, linewidths=0.5,
            cbar_kws={"shrink": 0.8}, ax=ax, annot_kws={"size": 9})
ax.set_title("Feature Correlation Matrix — California Housing",
             fontsize=14, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig("outputs/correlation_heatmap.png", dpi=150, bbox_inches="tight")
print("\n  ✅ Saved: outputs/correlation_heatmap.png")
plt.close()

top_corr = corr["MedHouseValue"].drop("MedHouseValue").abs().sort_values(ascending=False)
print(f"\n  Top correlations with MedHouseValue:")
for feat, val in top_corr.items():
    print(f"    {feat:<20} r = {val:+.3f}")

# ─── 3. FEATURE ENGINEERING ──────────────────────────────────────────────────
df_fe = df.copy()
df_fe["RoomsPerPerson"]    = df["AveRooms"]  / df["AveOccup"]
df_fe["BedsPerRoom"]       = df["AveBedrms"] / df["AveRooms"]
df_fe["PopulationDensity"] = df["Population"] / (df["AveRooms"] + 1)
df_fe["IncomePerRoom"]     = df["MedInc"]    / (df["AveRooms"] + 1)
df_fe["LogPopulation"]     = np.log1p(df["Population"])
df_fe["IncomeSquared"]     = df["MedInc"] ** 2

TARGET   = "MedHouseValue"
BASE_FEATURES = list(housing.feature_names)
ENG_FEATURES  = BASE_FEATURES + ["RoomsPerPerson", "BedsPerRoom",
                                  "PopulationDensity", "IncomePerRoom",
                                  "LogPopulation", "IncomeSquared"]

# ─── 4. TRAIN/TEST SPLIT ─────────────────────────────────────────────────────
X_base = df[BASE_FEATURES]
y      = df[TARGET]
X_eng  = df_fe[ENG_FEATURES]

X_base_train, X_base_test, y_train, y_test = train_test_split(
    X_base, y, test_size=0.20, random_state=42
)
X_eng_train, X_eng_test, _, _ = train_test_split(
    X_eng, y, test_size=0.20, random_state=42
)

print(f"\n  Train set: {X_base_train.shape[0]:,} | Test set: {X_base_test.shape[0]:,}")

# ─── 5. MODEL TRAINING & EVALUATION ──────────────────────────────────────────
def evaluate_model(name, y_true, y_pred):
    mae  = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2   = r2_score(y_true, y_pred)
    return {"Model": name, "MAE": mae, "RMSE": rmse, "R²": r2}

results = []

# --- Model 1: Baseline Linear Regression ------------------------------------
lr_base = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  LinearRegression())
])
lr_base.fit(X_base_train, y_train)
y_pred_base = lr_base.predict(X_base_test)
results.append(evaluate_model("Baseline Linear", y_test, y_pred_base))

# --- Model 2: Linear Regression + Engineered Features -----------------------
lr_eng = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  LinearRegression())
])
lr_eng.fit(X_eng_train, y_train)
y_pred_eng = lr_eng.predict(X_eng_test)
results.append(evaluate_model("Linear + Eng. Features", y_test, y_pred_eng))

# --- Model 3: Polynomial Features (degree 2) --------------------------------
poly_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("poly",   PolynomialFeatures(degree=2, include_bias=False)),
    ("model",  Ridge(alpha=1.0))   # Ridge to prevent overfitting with poly
])
poly_pipe.fit(X_base_train, y_train)
y_pred_poly = poly_pipe.predict(X_base_test)
results.append(evaluate_model("Polynomial (deg=2) + Ridge", y_test, y_pred_poly))

# --- Cross-validation --------------------------------------------------------
cv_scores = cross_val_score(lr_base, X_base, y, cv=5, scoring="r2")

results_df = pd.DataFrame(results)
print(f"\n{'─'*65}")
print("  MODEL COMPARISON TABLE:")
print(f"{'─'*65}")
print(results_df.to_string(index=False, float_format="%.4f"))
print(f"\n  5-Fold CV R² (Baseline): {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

r2_baseline = results_df.loc[0, "R²"]
r2_poly     = results_df.loc[2, "R²"]
print(f"\n  📈 R² Improvement: {r2_baseline:.4f} → {r2_poly:.4f}")
print(f"     Polynomial features boosted R² by {(r2_poly - r2_baseline)*100:.1f} pp")

# ─── 6. VISUALIZATIONS ───────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 12))
gs  = GridSpec(2, 3, figure=fig, hspace=0.42, wspace=0.35)

BLUE   = "#1a6bb5"
ORANGE = "#e07b29"
GREEN  = "#27ae60"
RED    = "#e74c3c"
GREY   = "#7f8c8d"

# --- Panel 1: Actual vs Predicted (Baseline) --------------------------------
ax1 = fig.add_subplot(gs[0, 0])
ax1.scatter(y_test, y_pred_base, alpha=0.3, s=12, color=BLUE, rasterized=True)
lims = [min(y_test.min(), y_pred_base.min()), max(y_test.max(), y_pred_base.max())]
ax1.plot(lims, lims, "r--", lw=2, label="Perfect prediction")
ax1.set_xlabel("Actual Price (100k$)", fontsize=10)
ax1.set_ylabel("Predicted Price (100k$)", fontsize=10)
ax1.set_title(f"Baseline Model\nActual vs Predicted  (R²={r2_baseline:.3f})",
              fontsize=11, fontweight="bold")
ax1.legend(fontsize=9)

# --- Panel 2: Actual vs Predicted (Polynomial) ------------------------------
ax2 = fig.add_subplot(gs[0, 1])
ax2.scatter(y_test, y_pred_poly, alpha=0.3, s=12, color=GREEN, rasterized=True)
ax2.plot(lims, lims, "r--", lw=2, label="Perfect prediction")
ax2.set_xlabel("Actual Price (100k$)", fontsize=10)
ax2.set_ylabel("Predicted Price (100k$)", fontsize=10)
ax2.set_title(f"Polynomial Model\nActual vs Predicted  (R²={r2_poly:.3f})",
              fontsize=11, fontweight="bold")
ax2.legend(fontsize=9)

# --- Panel 3: Residuals Plot (Baseline) -------------------------------------
ax3 = fig.add_subplot(gs[0, 2])
residuals = y_test - y_pred_base
ax3.scatter(y_pred_base, residuals, alpha=0.3, s=12, color=ORANGE, rasterized=True)
ax3.axhline(0, color="red", lw=2, linestyle="--")
ax3.axhline(residuals.std(), color=GREY, lw=1, linestyle=":", alpha=0.7)
ax3.axhline(-residuals.std(), color=GREY, lw=1, linestyle=":", alpha=0.7)
ax3.set_xlabel("Predicted Price", fontsize=10)
ax3.set_ylabel("Residual", fontsize=10)
ax3.set_title("Residuals Plot (Baseline)\n[Check: random scatter = good fit]",
              fontsize=11, fontweight="bold")

# --- Panel 4: Model Comparison Bar Chart ------------------------------------
ax4 = fig.add_subplot(gs[1, 0])
colors_bar = [BLUE, ORANGE, GREEN]
bars = ax4.bar(results_df["Model"], results_df["R²"],
               color=colors_bar, edgecolor="white", linewidth=1.5)
for bar, r2 in zip(bars, results_df["R²"]):
    ax4.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 0.005, f"{r2:.3f}",
             ha="center", va="bottom", fontweight="bold", fontsize=10)
ax4.set_ylim(0, 1.0)
ax4.set_ylabel("R² Score", fontsize=10)
ax4.set_title("Model R² Comparison", fontsize=11, fontweight="bold")
ax4.tick_params(axis="x", labelsize=8, rotation=15)
ax4.set_yticks(np.arange(0, 1.1, 0.1))

# --- Panel 5: MAE/RMSE Comparison -------------------------------------------
ax5 = fig.add_subplot(gs[1, 1])
x = np.arange(len(results_df))
w = 0.35
b1 = ax5.bar(x - w/2, results_df["MAE"],  width=w, color=BLUE,   label="MAE",  edgecolor="white")
b2 = ax5.bar(x + w/2, results_df["RMSE"], width=w, color=ORANGE, label="RMSE", edgecolor="white")
ax5.set_xticks(x)
ax5.set_xticklabels(results_df["Model"], fontsize=8, rotation=15)
ax5.set_ylabel("Error (100k USD)", fontsize=10)
ax5.set_title("MAE & RMSE Comparison\n(Lower is Better)", fontsize=11, fontweight="bold")
ax5.legend(fontsize=9)

# --- Panel 6: Residual Distribution -----------------------------------------
ax6 = fig.add_subplot(gs[1, 2])
ax6.hist(residuals, bins=60, color=BLUE, edgecolor="white", alpha=0.8, density=True)
mu, sigma = residuals.mean(), residuals.std()
x_norm = np.linspace(residuals.min(), residuals.max(), 300)
ax6.plot(x_norm, stats_norm := __import__("scipy").stats.norm.pdf(x_norm, mu, sigma),
         color=RED, lw=2.5, label=f"Normal (μ={mu:.2f}, σ={sigma:.2f})")
ax6.axvline(0, color=GREY, lw=1.5, linestyle="--")
ax6.set_xlabel("Residual Value", fontsize=10)
ax6.set_ylabel("Density", fontsize=10)
ax6.set_title("Residual Distribution\n[Should be ~Normal around 0]",
              fontsize=11, fontweight="bold")
ax6.legend(fontsize=8)

fig.suptitle("House Price Prediction — Model Evaluation Dashboard",
             fontsize=16, fontweight="bold", y=1.01)
plt.savefig("outputs/actual_vs_predicted.png", dpi=150, bbox_inches="tight")
print("  ✅ Saved: outputs/actual_vs_predicted.png")
plt.close()

print("\n  ✅ PROJECT 2 COMPLETE\n")