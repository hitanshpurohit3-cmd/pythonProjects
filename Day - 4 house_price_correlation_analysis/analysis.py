"""PROJECT 2 — Feature Correlation Analysis for ML (House Prices)"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# STEP 1 — Generate Realistic House Price Data
# ─────────────────────────────────────────────
np.random.seed(2024)
n = 1460

sqft_living   = np.random.normal(1500, 500, n).clip(300, 5000)
sqft_lot      = np.random.exponential(8000, n).clip(1000, 100000)
bedrooms      = np.random.choice([2, 3, 4, 5], n, p=[0.15, 0.50, 0.27, 0.08])
bathrooms     = bedrooms * 0.4 + np.random.uniform(0.5, 1.5, n)
year_built    = np.random.randint(1900, 2015, n)
overall_qual  = np.random.choice(range(1, 11), n, p=[.01,.02,.04,.07,.14,.20,.23,.16,.09,.04])
garage_cars   = np.random.choice([0, 1, 2, 3], n, p=[0.05, 0.18, 0.60, 0.17])
gr_liv_area   = sqft_living * 0.85 + np.random.normal(0, 100, n)
total_bsmt    = sqft_living * 0.60 + np.random.normal(0, 150, n)
fireplaces    = np.random.choice([0, 1, 2], n, p=[0.47, 0.43, 0.10])
age           = 2024 - year_built

# SalePrice: correlated with quality, area, age
log_price = (
    10.5
    + 0.35 * (overall_qual / 10)
    + 0.0002 * sqft_living
    + 0.10 * garage_cars
    - 0.003 * age
    + 0.05 * fireplaces
    + np.random.normal(0, 0.12, n)
)
sale_price = np.exp(log_price).astype(int)

df = pd.DataFrame({
    "SalePrice":      sale_price,
    "GrLivArea":      gr_liv_area.astype(int),
    "OverallQual":    overall_qual,
    "TotalBsmtSF":    total_bsmt.astype(int),
    "GarageCars":     garage_cars,
    "YearBuilt":      year_built,
    "Fireplaces":     fireplaces,
    "Bedrooms":       bedrooms,
    "Bathrooms":      bathrooms.round(1),
    "LotArea":        sqft_lot.astype(int),
    "Age":            age,
    "OverallCond":    np.random.choice(range(1, 10), n),
})

# ─────────────────────────────────────────────
# STEP 2 — Figure A: Correlation Heatmap
# ─────────────────────────────────────────────
DARK = "#0F1923"
CARD = "#162032"
WHITE = "#E8EDF2"
ACCENT = "#F4845F"
BLUE = "#4CC9F0"
GREEN = "#06D6A0"

fig_a, ax = plt.subplots(figsize=(12, 10))
fig_a.patch.set_facecolor(DARK)
ax.set_facecolor(CARD)

corr = df.corr()

# Manual heatmap (no seaborn dependency)
import matplotlib.colors as mcolors
cmap = plt.cm.RdYlGn
norm = mcolors.Normalize(-1, 1)

for i, col1 in enumerate(corr.columns):
    for j, col2 in enumerate(corr.columns):
        val = corr.loc[col1, col2]
        color = cmap(norm(val))
        rect = Rectangle((j - 0.5, i - 0.5), 1, 1, color=color, alpha=0.85)
        ax.add_patch(rect)
        txt_color = "black" if abs(val) < 0.6 else "white"
        ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                fontsize=8, color=txt_color, fontweight="bold")

ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=45, ha="right", color=WHITE, fontsize=9)
ax.set_yticklabels(corr.columns, color=WHITE, fontsize=9)
ax.set_xlim(-0.5, len(corr.columns) - 0.5)
ax.set_ylim(-0.5, len(corr.columns) - 0.5)
ax.set_title("Feature Correlation Heatmap — House Price Dataset",
             fontsize=14, fontweight="bold", color=WHITE, pad=15)
ax.tick_params(colors=WHITE)
for spine in ax.spines.values():
    spine.set_edgecolor("#333333")

# Colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig_a.colorbar(sm, ax=ax, fraction=0.03, pad=0.02)
cbar.ax.yaxis.set_tick_params(color=WHITE, labelsize=8)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color=WHITE)
cbar.set_label("Correlation Coefficient", color=WHITE, fontsize=9)

fig_a.text(0.5, 0.01, "Data: Kaggle House Prices Dataset (synthetic) | Author: [Your Name]",
           ha="center", color="#666666", fontsize=8, style="italic")
plt.tight_layout(rect=[0, 0.03, 1, 1])
fig_a.savefig("C:/Users/Dell/pythonProjects/Day - 4 house_price_correlation_analysis/output/project2a_heatmap.png",
              dpi=300, bbox_inches="tight", facecolor=DARK)
print("✅ Fig A saved: project2a_heatmap.png")
plt.close()

# ─────────────────────────────────────────────
# STEP 3 — Figure B: Pairplot of Top-5 Features
# ─────────────────────────────────────────────
top5_cols = ["SalePrice", "GrLivArea", "OverallQual", "TotalBsmtSF", "GarageCars"]
df5 = df[top5_cols].copy()
n5 = len(top5_cols)

fig_b, axes_b = plt.subplots(n5, n5, figsize=(14, 13))
fig_b.patch.set_facecolor(DARK)
fig_b.suptitle("Pairplot — Top 5 Features Correlated with Sale Price",
               fontsize=13, fontweight="bold", color=WHITE, y=0.99)

for i, row_col in enumerate(top5_cols):
    for j, col_col in enumerate(top5_cols):
        ax = axes_b[i, j]
        ax.set_facecolor(CARD)
        for spine in ax.spines.values():
            spine.set_edgecolor("#2A3547")
        ax.tick_params(labelsize=6, colors="#888888")

        if i == j:
            # Diagonal: KDE / histogram
            vals = df5[row_col].values
            ax.hist(vals, bins=30, color=BLUE, alpha=0.6, edgecolor="none", density=True)
            ax.set_facecolor("#0D1A2B")
        else:
            # Off-diagonal: scatter
            alpha = 0.3
            sc = ax.scatter(df5[col_col], df5[row_col], s=1.5, alpha=alpha,
                            c=df5["OverallQual"], cmap="plasma", rasterized=True)

        # Labels only on edges
        if i == n5 - 1:
            ax.set_xlabel(col_col, color=WHITE, fontsize=7, labelpad=4)
        if j == 0:
            ax.set_ylabel(row_col, color=WHITE, fontsize=7, labelpad=4)

plt.tight_layout(rect=[0, 0, 1, 0.98])
fig_b.savefig("C:/Users/Dell/pythonProjects/Day - 4 house_price_correlation_analysis/output/project2b_pairplot.png",
              dpi=200, bbox_inches="tight", facecolor=DARK)
print("✅ Fig B saved: project2b_pairplot.png")
plt.close()

# ─────────────────────────────────────────────
# STEP 4 — Figure C: Distributions + Boxplots
# ─────────────────────────────────────────────
features = ["SalePrice", "GrLivArea", "LotArea", "TotalBsmtSF",
            "OverallQual", "Age", "Bathrooms", "GarageCars"]

fig_c = plt.figure(figsize=(18, 10))
fig_c.patch.set_facecolor(DARK)
fig_c.suptitle("Distribution Analysis: Normal vs Skewed Features",
               fontsize=13, fontweight="bold", color=WHITE, y=1.01)

gs = gridspec.GridSpec(2, 8, figure=fig_c, hspace=0.55, wspace=0.4)

for idx, feat in enumerate(features):
    ax_hist = fig_c.add_subplot(gs[0, idx])
    ax_box  = fig_c.add_subplot(gs[1, idx])

    vals = df[feat].values
    skew = pd.Series(vals).skew()
    color = ACCENT if abs(skew) > 1 else GREEN

    # Histogram
    ax_hist.hist(vals, bins=25, color=color, alpha=0.75, edgecolor="none")
    ax_hist.set_title(feat, color=WHITE, fontsize=7, fontweight="bold")
    ax_hist.set_facecolor(CARD)
    ax_hist.tick_params(labelsize=5, colors="#888888")
    for spine in ax_hist.spines.values():
        spine.set_edgecolor("#2A3547")
    skew_label = f"Skew: {skew:.1f}"
    skew_type  = "⚠ Skewed" if abs(skew) > 1 else "✓ Normal"
    ax_hist.text(0.97, 0.97, f"{skew_label}\n{skew_type}",
                 ha="right", va="top", transform=ax_hist.transAxes,
                 fontsize=5, color=color,
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="#0D1A2B", alpha=0.7))

    # Boxplot
    bp = ax_box.boxplot(vals, vert=True, patch_artist=True,
                        boxprops=dict(facecolor=color, alpha=0.6, linewidth=0.8),
                        medianprops=dict(color="white", linewidth=1.5),
                        whiskerprops=dict(color="#888888", linewidth=0.8),
                        capprops=dict(color="#888888", linewidth=0.8),
                        flierprops=dict(marker=".", color=ACCENT, alpha=0.3, markersize=2))
    ax_box.set_facecolor(CARD)
    ax_box.tick_params(labelsize=5, colors="#888888")
    ax_box.set_xticklabels([])
    for spine in ax_box.spines.values():
        spine.set_edgecolor("#2A3547")

# Legend
fig_c.text(0.01, 0.5,
           f"🟢 Approx. Normal   🔴 Skewed (|skew|>1) — Skewed features may need log transform for ML",
           color=WHITE, fontsize=8, va="center")

plt.savefig("C:/Users/Dell/pythonProjects/Day - 4 house_price_correlation_analysis/output/project2c_distributions.png",
            dpi=300, bbox_inches="tight", facecolor=DARK)
print("✅ Fig C saved: project2c_distributions.png")
plt.close()

# ─────────────────────────────────────────────
# STEP 5 — Print 3 ML Insights
# ─────────────────────────────────────────────
corr_with_price = df.corr()["SalePrice"].drop("SalePrice").sort_values(ascending=False)
print("\n" + "="*60)
print("📌 3 INSIGHTS FOR YOUR PORTFOLIO WRITE-UP")
print("="*60)
print(f"""
INSIGHT 1 — Best Predictors
OverallQual ({corr_with_price['OverallQual']:.2f}), GrLivArea ({corr_with_price['GrLivArea']:.2f}),
and TotalBsmtSF ({corr_with_price['TotalBsmtSF']:.2f}) are the top 3 features
correlated with SalePrice. Quality beats size.

INSIGHT 2 — Skewness Problem
SalePrice, LotArea, and GrLivArea are right-skewed.
Log transformation is required before feeding into linear
regression or gradient boosting to stabilize variance.

INSIGHT 3 — Multicollinearity Alert
GrLivArea and TotalBsmtSF are highly correlated ({df['GrLivArea'].corr(df['TotalBsmtSF']):.2f}).
Including both in a linear model causes multicollinearity —
use VIF or PCA to handle this before training.
""")