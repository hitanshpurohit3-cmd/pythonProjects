"""
=============================================================
PROJECT 3: Customer Churn Classifier — Logistic Regression
=============================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from matplotlib.patches import FancyBboxPatch

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    confusion_matrix, classification_report, roc_curve, auc,
    accuracy_score, precision_score, recall_score, f1_score,
    ConfusionMatrixDisplay, RocCurveDisplay
)

import warnings, os
warnings.filterwarnings("ignore")
os.makedirs("outputs", exist_ok=True)

# ─── 1. LOAD DATA ────────────────────────────────────────────────────────────
CSV_PATH = "WA_Fn-UseC_-Telco-Customer-Churn.csv"

try:
    df = pd.read_csv(CSV_PATH)
    print(f"  ✅ Loaded Telco Churn dataset: {df.shape}")
except FileNotFoundError:
    print("  ⚠️  CSV not found. Generating synthetic Telco-like dataset for demo...")
    # Synthetic fallback (mirrors real dataset structure closely)
    np.random.seed(42)
    n = 7043
    tenure      = np.random.exponential(30, n).clip(0, 72).astype(int)
    monthly_chg = np.random.uniform(20, 110, n)
    total_chg   = monthly_chg * tenure + np.random.normal(0, 50, n)
    total_chg   = total_chg.clip(0)
    contracts   = np.random.choice(["Month-to-month","One year","Two year"], n,
                                   p=[0.55, 0.25, 0.20])
    internet    = np.random.choice(["DSL","Fiber optic","No"], n, p=[0.34, 0.44, 0.22])
    payment     = np.random.choice(["Electronic check","Mailed check",
                                    "Bank transfer (automatic)","Credit card (automatic)"], n)
    tech_support= np.random.choice(["Yes","No","No internet service"], n, p=[0.29, 0.50, 0.21])
    paperless   = np.random.choice(["Yes","No"], n, p=[0.59, 0.41])
    senior      = np.random.choice([0,1], n, p=[0.84, 0.16])
    partner     = np.random.choice(["Yes","No"], n, p=[0.48, 0.52])
    dependents  = np.random.choice(["Yes","No"], n, p=[0.30, 0.70])
    phone_svc   = np.random.choice(["Yes","No"], n, p=[0.90, 0.10])
    multiple_ln = np.random.choice(["Yes","No","No phone service"], n, p=[0.42, 0.48, 0.10])
    online_bck  = np.random.choice(["Yes","No","No internet service"], n, p=[0.28, 0.51, 0.21])
    device_prot = np.random.choice(["Yes","No","No internet service"], n, p=[0.29, 0.50, 0.21])
    streaming_t = np.random.choice(["Yes","No","No internet service"], n, p=[0.38, 0.41, 0.21])
    streaming_m = np.random.choice(["Yes","No","No internet service"], n, p=[0.38, 0.41, 0.21])

    churn_prob = (
        0.35 * (contracts == "Month-to-month").astype(float)
      - 0.25 * (contracts == "Two year").astype(float)
      + 0.20 * (internet  == "Fiber optic").astype(float)
      - 0.15 * (tech_support == "Yes").astype(float)
      + 0.10 * (payment   == "Electronic check").astype(float)
      - 0.008 * tenure
      + 0.002 * monthly_chg
      - 0.10 * (online_bck == "Yes").astype(float)
    )
    churn_prob = 1 / (1 + np.exp(-churn_prob * 2))
    churn_label = (np.random.uniform(0, 1, n) < churn_prob).astype(int)

    df = pd.DataFrame({
        "customerID": [f"CUST-{i:05d}" for i in range(n)],
        "gender": np.random.choice(["Male","Female"], n),
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_svc,
        "MultipleLines": multiple_ln,
        "InternetService": internet,
        "OnlineSecurity": np.random.choice(["Yes","No","No internet service"], n, p=[0.28,0.51,0.21]),
        "OnlineBackup": online_bck,
        "DeviceProtection": device_prot,
        "TechSupport": tech_support,
        "StreamingTV": streaming_t,
        "StreamingMovies": streaming_m,
        "Contract": contracts,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly_chg.round(2),
        "TotalCharges": total_chg.round(2),
        "Churn": ["Yes" if c else "No" for c in churn_label],
    })
    print(f"  ✅ Synthetic dataset created: {df.shape}")

print("=" * 65)
print("       CUSTOMER CHURN MODEL — ANALYSIS REPORT")
print("=" * 65)
print(f"\n  Shape: {df.shape}")
print(f"\n  Churn Distribution:")
print(df["Churn"].value_counts(normalize=True).map(lambda x: f"{x:.2%}").to_string())

# ─── 2. DATA CLEANING ────────────────────────────────────────────────────────
df = df.drop("customerID", axis=1, errors="ignore")

# TotalCharges sometimes arrives as string with spaces
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

print(f"\n  Missing values after cleaning: {df.isnull().sum().sum()}")

# ─── 3. ENCODE CATEGORICALS ──────────────────────────────────────────────────
df_enc = df.copy()
TARGET = "Churn"
df_enc[TARGET] = (df_enc[TARGET] == "Yes").astype(int)

binary_cols   = ["gender","Partner","Dependents","PhoneService","PaperlessBilling"]
multi_cols    = [c for c in df_enc.select_dtypes("object").columns
                 if c not in binary_cols + [TARGET]]

# Label-encode binary
le = LabelEncoder()
for col in binary_cols:
    if col in df_enc.columns:
        df_enc[col] = le.fit_transform(df_enc[col].astype(str))

# One-hot encode multi-class
df_enc = pd.get_dummies(df_enc, columns=multi_cols, drop_first=True)

FEATURES = [c for c in df_enc.columns if c != TARGET]
X = df_enc[FEATURES]
y = df_enc[TARGET]

print(f"\n  Feature matrix: {X.shape}  |  Target: {y.shape}")
print(f"  Churn rate: {y.mean():.2%}")

# ─── 4. TRAIN / TEST SPLIT ───────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
print(f"  Train: {X_train.shape[0]:,} | Test: {X_test.shape[0]:,}")

# ─── 5. MODEL TRAINING ───────────────────────────────────────────────────────
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("clf",    LogisticRegression(
        C=0.5,            # regularization (smaller C = stronger penalty)
        max_iter=1000,
        class_weight="balanced",   # handles class imbalance
        solver="lbfgs",
        random_state=42
    ))
])
pipeline.fit(X_train, y_train)
y_pred      = pipeline.predict(X_test)
y_pred_prob = pipeline.predict_proba(X_test)[:, 1]

# ─── 6. EVALUATION METRICS ───────────────────────────────────────────────────
acc  = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec  = recall_score(y_test, y_pred)
f1   = f1_score(y_test, y_pred)
fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
roc_auc = auc(fpr, tpr)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(pipeline, X, y, cv=cv, scoring="roc_auc")

print(f"\n{'─'*65}")
print("  MODEL PERFORMANCE METRICS")
print(f"{'─'*65}")
print(f"  Accuracy           : {acc:.4f}  ({acc*100:.1f}%)")
print(f"  Precision (churn)  : {prec:.4f}")
print(f"  Recall (churn)     : {rec:.4f}")
print(f"  F1-Score (churn)   : {f1:.4f}")
print(f"  ROC-AUC            : {roc_auc:.4f}")
print(f"  5-Fold CV AUC      : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
print(f"\n  Full Classification Report:")
print(classification_report(y_test, y_pred, target_names=["No Churn","Churn"]))

with open("outputs/classification_report.txt", "w",encoding="utf-8") as f:
    f.write(f"Customer Churn Model — Classification Report\n{'='*50}\n\n")
    f.write(f"Accuracy  : {acc:.4f}\nPrecision : {prec:.4f}\n")
    f.write(f"Recall    : {rec:.4f}\nF1-Score  : {f1:.4f}\nROC-AUC   : {roc_auc:.4f}\n\n")
    f.write(classification_report(y_test, y_pred, target_names=["No Churn","Churn"]))
    f.write(f"\n5-Fold CV AUC: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}\n")
print("  ✅ Saved: outputs/classification_report.txt")

# ─── 7. TOP CHURN DRIVERS ────────────────────────────────────────────────────
coefs = pipeline.named_steps["clf"].coef_[0]
feat_importance = pd.DataFrame({
    "Feature"    : FEATURES,
    "Coefficient": coefs,
    "AbsCoef"    : np.abs(coefs)
}).sort_values("AbsCoef", ascending=False)

top5_churn    = feat_importance[feat_importance["Coefficient"] > 0].head(5)
top5_protect  = feat_importance[feat_importance["Coefficient"] < 0].head(5)

print(f"\n{'─'*65}")
print("  TOP 5 CHURN DRIVERS (positive coefficient = higher churn risk)")
print(f"{'─'*65}")
for _, row in top5_churn.iterrows():
    print(f"  ▲  {row['Feature']:<40}  coef = {row['Coefficient']:+.4f}")

print(f"\n  TOP 5 CHURN PROTECTORS (negative = lower churn risk)")
print(f"{'─'*65}")
for _, row in top5_protect.iterrows():
    print(f"  ▼  {row['Feature']:<40}  coef = {row['Coefficient']:+.4f}")

# ─── 8. VISUALIZATIONS ───────────────────────────────────────────────────────
plt.style.use("seaborn-v0_8-whitegrid")
fig = plt.figure(figsize=(18, 12))
gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.38)

BLUE   = "#1a6bb5"
ORANGE = "#e07b29"
GREEN  = "#27ae60"
RED    = "#e74c3c"

# --- Panel 1: Confusion Matrix ----------------------------------------------
ax1 = fig.add_subplot(gs[0, 0])
cm   = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=["No Churn", "Churn"])
disp.plot(cmap="Blues", ax=ax1, colorbar=False)
ax1.set_title(f"Confusion Matrix\n(Accuracy: {acc:.2%})",
              fontsize=12, fontweight="bold")

# --- Panel 2: ROC Curve -----------------------------------------------------
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(fpr, tpr, color=BLUE, lw=2.5, label=f"Logistic Reg (AUC = {roc_auc:.3f})")
ax2.plot([0,1], [0,1], color=RED, lw=1.5, linestyle="--", label="Random Classifier")
ax2.fill_between(fpr, tpr, alpha=0.12, color=BLUE)
ax2.set_xlabel("False Positive Rate", fontsize=11)
ax2.set_ylabel("True Positive Rate", fontsize=11)
ax2.set_title("ROC Curve", fontsize=12, fontweight="bold")
ax2.legend(fontsize=10, loc="lower right")
ax2.set_xlim([-0.02, 1.02])
ax2.set_ylim([-0.02, 1.05])

# --- Panel 3: Precision-Recall Tradeoff vs Threshold ------------------------
ax3 = fig.add_subplot(gs[0, 2])
from sklearn.metrics import precision_recall_curve
precision_c, recall_c, thresh_pr = precision_recall_curve(y_test, y_pred_prob)
ax3.plot(thresh_pr, precision_c[:-1], color=ORANGE, lw=2.5, label="Precision")
ax3.plot(thresh_pr, recall_c[:-1],    color=BLUE,   lw=2.5, label="Recall")
ax3.axvline(0.5, color=RED, lw=1.5, linestyle="--", label="Default threshold (0.5)")
ax3.set_xlabel("Classification Threshold", fontsize=11)
ax3.set_ylabel("Score", fontsize=11)
ax3.set_title("Precision-Recall vs Threshold\n[Tune threshold for business needs]",
              fontsize=12, fontweight="bold")
ax3.legend(fontsize=9)
ax3.set_ylim([0, 1.05])

# --- Panel 4: Top Churn Drivers Bar Chart -----------------------------------
ax4 = fig.add_subplot(gs[1, :2])
top_n  = 15
top_df = pd.concat([
    feat_importance.nlargest(top_n // 2, "Coefficient"),
    feat_importance.nsmallest(top_n // 2, "Coefficient")]).sort_values("Coefficient")

colors_bar = [GREEN if c < 0 else RED for c in top_df["Coefficient"]]
bars = ax4.barh(top_df["Feature"], top_df["Coefficient"],
                color=colors_bar, edgecolor="white", linewidth=0.8, height=0.7)
ax4.axvline(0, color="black", lw=1.2)
ax4.set_xlabel("Logistic Regression Coefficient", fontsize=11)
ax4.set_title("Top Churn Drivers vs Protectors (Logistic Regression Coefficients)\n"
              "Red = Increases Churn Risk  |  Green = Decreases Churn Risk",
              fontsize=12, fontweight="bold")
ax4.tick_params(axis="y", labelsize=9)

# Annotate bars
for bar in bars:
    w = bar.get_width()
    ax4.text(w + (0.02 if w > 0 else -0.02), bar.get_y() + bar.get_height() / 2,
             f"{w:+.3f}", va="center",
             ha="left" if w > 0 else "right", fontsize=8)

# --- Panel 5: Metric Summary Scorecard --------------------------------------
ax5 = fig.add_subplot(gs[1, 2])
ax5.axis("off")
metrics = [
    ("Accuracy",       f"{acc:.2%}",      acc >= 0.80),
    ("Precision",      f"{prec:.2%}",     prec >= 0.70),
    ("Recall",         f"{rec:.2%}",      rec >= 0.70),
    ("F1-Score",       f"{f1:.2%}",       f1 >= 0.70),
    ("ROC-AUC",        f"{roc_auc:.3f}",  roc_auc >= 0.80),
    ("CV AUC (mean)",  f"{cv_scores.mean():.3f}", cv_scores.mean() >= 0.80),
]
ax5.set_title("Model Scorecard", fontsize=13, fontweight="bold", pad=15)
for i, (name, val, good) in enumerate(metrics):
    y_pos = 0.88 - i * 0.14
    color = GREEN if good else ORANGE
    ax5.text(0.05, y_pos, name, transform=ax5.transAxes,
             fontsize=12, va="center", color="#333333")
    ax5.text(0.70, y_pos, val, transform=ax5.transAxes,
             fontsize=12, va="center", fontweight="bold", color=color)
    ax5.text(0.92, y_pos, "✓" if good else "~", transform=ax5.transAxes,
             fontsize=14, va="center", color=color)
rect = FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                      boxstyle="round,pad=0.02",
                      linewidth=1.5, edgecolor="#cccccc", facecolor="#f9f9f9",
                      transform=ax5.transAxes, zorder=0)
ax5.add_patch(rect)

fig.suptitle("Customer Churn Classifier — Evaluation Dashboard",
             fontsize=16, fontweight="bold", y=1.01)
plt.savefig("outputs/roc_curve.png", dpi=150, bbox_inches="tight")
print("  ✅ Saved: outputs/roc_curve.png")
plt.close()

# ─── 9. DEDICATED TOP DRIVERS CHART ─────────────────────────────────────────
fig2, ax = plt.subplots(figsize=(12, 7))
top10 = feat_importance.head(10).sort_values("Coefficient")
colors_d = [GREEN if c < 0 else RED for c in top10["Coefficient"]]
ax.barh(top10["Feature"], top10["Coefficient"],
        color=colors_d, edgecolor="white", linewidth=0.8, height=0.65)
ax.axvline(0, color="black", lw=1.5)
for i, (val, label) in enumerate(zip(top10["Coefficient"], top10["Feature"])):
    ax.text(val + (0.01 if val > 0 else -0.01), i,
            f"{val:+.3f}", va="center",
            ha="left" if val > 0 else "right",
            fontsize=10, fontweight="bold")
ax.set_xlabel("Logistic Regression Coefficient (Standardized Features)", fontsize=12)
ax.set_title("Top 10 Features Driving Customer Churn\n"
             "■ Red = Higher churn probability  |  ■ Green = Lower churn probability",
             fontsize=14, fontweight="bold")
ax.tick_params(axis="y", labelsize=11)
plt.tight_layout()
plt.savefig("outputs/top_churn_drivers.png", dpi=150, bbox_inches="tight")
print("  ✅ Saved: outputs/top_churn_drivers.png")
plt.close()

print("\n  ✅ PROJECT 3 COMPLETE")
print("\n" + "=" * 65)
print("=" * 65)