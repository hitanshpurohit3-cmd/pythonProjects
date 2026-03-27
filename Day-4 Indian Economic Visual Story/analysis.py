"""PROJECT 3 — India Economic Indicators Visual Story"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# STEP 1 — Realistic India Economic Data 2000–2023
# ─────────────────────────────────────────────
years = list(range(2000, 2024))

# GDP Growth Rate (%) — matches actual World Bank data shape
gdp_growth = [
    5.4, 5.8, 3.8, 8.0, 7.9, 9.3, 9.3, 9.8, 3.9, 8.4,
    10.3, 6.6, 5.5, 6.4, 7.4, 8.0, 8.3, 6.1, 6.5, 4.2,
    -5.8, 9.7, 7.2, 7.6
]

# Inflation (CPI %) — matches RBI data
inflation = [
    3.8, 5.2, 4.0, 3.8, 3.8, 4.2, 6.1, 6.4, 8.3, 10.9,
    11.9, 8.9, 9.3, 10.9, 6.7, 5.9, 4.9, 2.5, 3.4, 4.8,
    6.2, 5.5, 6.7, 5.4
]

# Unemployment rate (%) — approximated from CMIE/ILO
unemployment = [
    7.3, 7.0, 7.6, 7.1, 6.8, 6.5, 6.2, 6.1, 6.8, 6.4,
    6.2, 6.1, 5.8, 5.6, 5.4, 5.1, 5.0, 5.4, 6.1, 7.6,
    9.1, 7.6, 7.3, 7.1
]

df = pd.DataFrame({
    "year": years,
    "gdp": gdp_growth,
    "inflation": inflation,
    "unemployment": unemployment
})

# ─────────────────────────────────────────────
# STEP 2 — Build the 3-Panel Visual Story
# ─────────────────────────────────────────────
DARK    = "#111827"
CARD    = "#1F2937"
WHITE   = "#F9FAFB"
MUTED   = "#9CA3AF"
ACCENT  = "#F59E0B"   # gold
RED     = "#EF4444"
GREEN   = "#10B981"
BLUE    = "#3B82F6"
TEAL    = "#14B8A6"

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 16))
fig.patch.set_facecolor(DARK)

def base_style(ax, title):
    ax.set_facecolor(CARD)
    ax.set_title(title, color=WHITE, fontsize=12, fontweight="bold", pad=10, loc="left")
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.set_xlim(1999, 2024)
    for spine in ax.spines.values():
        spine.set_edgecolor("#374151")
    ax.xaxis.set_tick_params(colors=MUTED)
    ax.yaxis.set_tick_params(colors=MUTED)

# ── CHART 1: GDP Growth — Line with Recession Highlights ──────
base_style(ax1, "① India GDP Growth Rate (%) — 2000 to 2023")

# Shade recession / slowdown zones
slowdown_zones = [
    (2008, 2009, "Global\nFinancial Crisis"),
    (2019, 2020, "Pre-COVID\nSlowdown"),
    (2020, 2021, "COVID-19\nContraction"),
]
for start, end, label in slowdown_zones:
    ax1.axvspan(start, end, alpha=0.15, color=RED, zorder=0)
    ax1.text((start + end) / 2, -7.5, label, ha="center",
             fontsize=7, color=RED, fontweight="bold")

# Highlight boom years
ax1.axvspan(2004, 2008, alpha=0.08, color=GREEN, zorder=0)
ax1.text(2006, 10.5, "India Growth Story\n(Avg 8.8%)", ha="center",
         fontsize=7.5, color=GREEN, fontweight="bold")

ax1.plot(df["year"], df["gdp"], color=ACCENT, linewidth=2.5, zorder=5)
ax1.fill_between(df["year"], df["gdp"], 0, where=(np.array(gdp_growth) >= 0),
                 alpha=0.2, color=GREEN)
ax1.fill_between(df["year"], df["gdp"], 0, where=(np.array(gdp_growth) < 0),
                 alpha=0.3, color=RED)
ax1.axhline(0, color=MUTED, linewidth=0.8, linestyle="--")

# Key annotations
ax1.annotate("COVID Crash\n−5.8%", xy=(2020, -5.8),
             xytext=(2017.5, -3.5),
             fontsize=8, color=RED, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

ax1.annotate("Post-COVID\nBounce +9.7%", xy=(2021, 9.7),
             xytext=(2021.5, 11),
             fontsize=8, color=GREEN, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.2))

ax1.set_ylabel("GDP Growth (%)", color=MUTED, fontsize=9)
ax1.set_yticks(range(-8, 14, 2))
ax1.set_xticks(range(2000, 2024, 2))
ax1.grid(axis="y", color="#374151", linewidth=0.5, alpha=0.5)

# ── CHART 2: Inflation Bar with RBI Target Zone ────────────────
base_style(ax2, "② Consumer Price Inflation (%) — with RBI Target Band")

bar_colors = [RED if v > 6 else (GREEN if v <= 4 else BLUE) for v in inflation]
ax2.bar(df["year"], df["inflation"], color=bar_colors, alpha=0.85, width=0.7)

# RBI target band (4% ±2 = 2–6%)
ax2.axhspan(2, 6, alpha=0.10, color=GREEN, label="RBI Target Band (2–6%)")
ax2.axhline(4, color=GREEN, linewidth=1.5, linestyle="--", label="RBI Target (4%)")
ax2.axhline(6, color=RED, linewidth=1, linestyle=":", alpha=0.8, label="Upper Tolerance (6%)")

# Annotations
ax2.annotate("High inflation era\n(supply shocks)", xy=(2009.5, 11.0),
             xytext=(2007, 12.5), fontsize=8, color=RED,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1))

ax2.annotate("Demonetization\n demand crash", xy=(2017, 2.5),
             xytext=(2014.5, 1.0), fontsize=8, color=GREEN,
             arrowprops=dict(arrowstyle="->", color=GREEN, lw=1))

ax2.legend(loc="upper right", fontsize=8, facecolor=CARD,
           labelcolor=WHITE, framealpha=0.7)
ax2.set_ylabel("Inflation (%)", color=MUTED, fontsize=9)
ax2.set_xticks(range(2000, 2024, 2))
ax2.grid(axis="y", color="#374151", linewidth=0.5, alpha=0.5)

# Legend: color meaning
red_p   = mpatches.Patch(color=RED,   label="Above 6% (High)")
blue_p  = mpatches.Patch(color=BLUE,  label="4–6% (On Target)")
green_p = mpatches.Patch(color=GREEN, label="Below 4% (Low)")
ax2.legend(handles=[red_p, blue_p, green_p], loc="upper left",
           fontsize=7, facecolor=CARD, labelcolor=WHITE, framealpha=0.7)

# ── CHART 3: GDP vs Unemployment Scatter + Story ──────────────
base_style(ax3, "③ GDP Growth vs Unemployment — Is Growth Creating Jobs?")
ax3.set_xlim(-8, 13)

sc = ax3.scatter(df["gdp"], df["unemployment"],
                 c=df["year"], cmap="cool", s=90, zorder=5,
                 edgecolors="#374151", linewidth=0.5)

# Trend line
z = np.polyfit(df["gdp"], df["unemployment"], 1)
p = np.poly1d(z)
x_line = np.linspace(-7, 12, 100)
ax3.plot(x_line, p(x_line), color=ACCENT, linewidth=1.5,
         linestyle="--", alpha=0.7, label=f"Trend (slope {z[0]:.2f})")

# Annotate key years
for _, row in df.iterrows():
    if row["year"] in [2008, 2020, 2021, 2004, 2017]:
        ax3.annotate(str(int(row["year"])),
                     xy=(row["gdp"], row["unemployment"]),
                     xytext=(5, 5), textcoords="offset points",
                     fontsize=7.5, color=WHITE)

# Quadrant labels
ax3.axvline(0, color=MUTED, linewidth=0.7, linestyle=":")
ax3.axhline(df["unemployment"].mean(), color=MUTED, linewidth=0.7, linestyle=":")
ax3.text(8, 8.5, "High Growth\nHigh Unemployment\n(Jobless Growth?)",
         fontsize=7.5, color=ACCENT, ha="center",
         bbox=dict(boxstyle="round", facecolor=DARK, alpha=0.6))
ax3.text(8, 5.5, "High Growth\nLow Unemployment\n(Ideal Zone)",
         fontsize=7.5, color=GREEN, ha="center",
         bbox=dict(boxstyle="round", facecolor=DARK, alpha=0.6))

cbar = fig.colorbar(sc, ax=ax3, fraction=0.02, pad=0.01)
cbar.set_label("Year", color=WHITE, fontsize=8)
cbar.ax.yaxis.set_tick_params(color=WHITE, labelsize=7)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color=WHITE)

ax3.set_xlabel("GDP Growth Rate (%)", color=MUTED, fontsize=9)
ax3.set_ylabel("Unemployment Rate (%)", color=MUTED, fontsize=9)
ax3.legend(loc="lower right", fontsize=8, facecolor=CARD,
           labelcolor=WHITE, framealpha=0.7)
ax3.grid(color="#374151", linewidth=0.5, alpha=0.4)

# ─────────────────────────────────────────────
# STEP 3 — Master Story Title + Source
# ─────────────────────────────────────────────
fig.suptitle(
    "India's Economic Journey: Growth, Inflation & Employment (2000–2023)",
    fontsize=15, fontweight="bold", color=WHITE, y=1.005
)

fig.text(0.5, -0.005,
         "Sources: World Bank, RBI Annual Reports, CMIE | Visualization: Python / Matplotlib | Author: [Your Name]",
         ha="center", color="#6B7280", fontsize=8, style="italic")

plt.tight_layout()
plt.subplots_adjust(hspace=0.45)
plt.savefig("C:/Users/Dell/pythonProjects/Day-4 Indian Economic Visual Story/outputs/project3_india_economy.png",
            dpi=300, bbox_inches="tight", facecolor=DARK)
print("✅ Project 3 saved: project3_india_economy.png")
plt.close()