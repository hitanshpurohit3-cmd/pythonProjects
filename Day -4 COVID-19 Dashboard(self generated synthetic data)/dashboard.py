"""PROJECT 1 — COVID-19 India Multi-Panel Dashboard"""

from http.client import ImproperConnectionState
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyArrowPatch
import warnings
warnings.filterwarnings("ignore")

# STEP 1 — Generating Realistic Synthetic Data

np.random.seed(42)

# Daily national data: Jan 2020 – Dec 2021 (730 days)
dates = pd.date_range("2020-01-30", periods=730, freq="D")

def wave(peak_day, peak_val, width=80):
    """Create a Gaussian wave of cases."""
    x = np.arange(730)
    return peak_val * np.exp(-0.5 * ((x - peak_day) / width) ** 2)

daily_cases = (
    wave(130, 50_000) + wave(310, 90_000) + wave(450, 400_000)
    + np.random.normal(0, 3000, 730)
).clip(0)

daily_deaths = (daily_cases * np.random.uniform(0.010, 0.014, 730)).clip(0)
daily_recovered = (daily_cases * np.random.uniform(0.88, 0.95, 730)).clip(0)

df_national = pd.DataFrame({
    "date": dates,
    "cases": daily_cases.astype(int),
    "deaths": daily_deaths.astype(int),
    "recovered": daily_recovered.astype(int),
})
df_national["week"] = df_national["date"].dt.to_period("W")

# State-wise cumulative data
states = [
    "Maharashtra", "Kerala", "Karnataka", "Tamil Nadu",
    "Andhra Pradesh", "Uttar Pradesh", "Delhi", "West Bengal",
    "Rajasthan", "Odisha", "Gujarat", "Madhya Pradesh",
    "Chhattisgarh", "Bihar", "Telangana"
]
state_cases  = np.array([6_300_000, 6_200_000, 2_900_000, 2_600_000,
                          2_300_000, 1_700_000, 1_400_000, 1_200_000,
                          1_000_000,   900_000,   800_000,   700_000,
                            600_000,   500_000,   400_000])
state_deaths = (state_cases * np.random.uniform(0.010, 0.018, len(states))).astype(int)

df_states = pd.DataFrame({
    "state": states,
    "cases": state_cases,
    "deaths": state_deaths,
    "cfr": (state_deaths / state_cases * 100).round(2)
})

# Weekly aggregation
df_weekly = df_national.groupby("week")["cases"].sum().reset_index()
df_weekly["week_str"] = df_weekly["week"].astype(str)

# Rolling recovery rate (7-day)
df_national["recovery_rate"] = (
    df_national["recovered"].rolling(7).sum() /
    df_national["cases"].rolling(7).sum().replace(0, np.nan) * 100
).clip(0, 100)

# STEP 2 — Build the 6-Panel Figure

ACCENT  = "#E63946"
BLUE    = "#457B9D"
GREEN   = "#2A9D8F"
ORANGE  = "#E9C46A"
DARK    = "#1D3557"
LIGHT   = "#F1FAEE"

fig, axes = plt.subplots(2, 3, figsize=(20, 12))
fig.patch.set_facecolor(DARK)

# ── Sub-figure styling helper ──────────────────
def style_ax(ax, title):
    ax.set_facecolor("#162032")
    ax.set_title(title, color="white", fontsize=11, fontweight="bold", pad=8)
    ax.tick_params(colors="#AAAAAA", labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor("#333333")
    ax.title.set_color("white")
    return ax

# ── CHART 1: Daily Cases Over Time (line) ─────
ax1 = axes[0, 0]
ax1.plot(df_national["date"], df_national["cases"] / 1000,
         color=ACCENT, linewidth=1.2, alpha=0.9)
ax1.fill_between(df_national["date"], df_national["cases"] / 1000,
                 alpha=0.15, color=ACCENT)
# Annotate wave peaks
for day, label in [(130, "Wave 1"), (310, "Wave 2"), (450, "Delta Wave")]:
    ax1.annotate(label, xy=(dates[day], daily_cases[day] / 1000),
                 xytext=(0, 15), textcoords="offset points",
                 fontsize=7, color="white",
                 arrowprops=dict(arrowstyle="->", color="#AAAAAA", lw=0.8))
style_ax(ax1, "① Daily New Cases Over Time")
ax1.set_ylabel("Cases (thousands)", color="#AAAAAA", fontsize=8)
ax1.yaxis.label.set_color("#AAAAAA")

# ── CHART 2: Top-10 States — Horizontal Bar ───
import matplotlib as mpl


ax2 = axes[0, 1]
top10 = df_states.nlargest(10, "cases").sort_values("cases")
colors_bar = mpl.colormaps["YlOrRd"](np.linspace(0.3, 0.9, 10))
#colors_bar = plt.cm.YlOrRd(np.linspace(0.3, 0.9, 10))
bars = ax2.barh(top10["state"], top10["cases"] / 1_000_000, color=colors_bar)
for bar, val in zip(bars, top10["cases"] / 1_000_000):
    ax2.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
             f"{val:.1f}M", va="center", fontsize=7, color="white")
style_ax(ax2, "② State-wise Total Cases (Top 10)")
ax2.set_xlabel("Cases (millions)", color="#AAAAAA", fontsize=8)
ax2.xaxis.label.set_color("#AAAAAA")

# ── CHART 3: Deaths vs Recoveries — Stacked Area ─
ax3 = axes[0, 2]
# Smooth with rolling average
d_smooth = df_national["deaths"].rolling(7).mean().fillna(0)
r_smooth  = df_national["recovered"].rolling(7).mean().fillna(0)
ax3.stackplot(df_national["date"],
              d_smooth / 1000, r_smooth / 1000,
              labels=["Deaths", "Recovered"],
              colors=[ACCENT, GREEN], alpha=0.85)
ax3.legend(loc="upper left", fontsize=7, facecolor="#162032",
           labelcolor="white", framealpha=0.5)
style_ax(ax3, "③ Deaths vs Recoveries (7-day avg)")
ax3.set_ylabel("Count (thousands)", color="#AAAAAA", fontsize=8)
ax3.yaxis.label.set_color("#AAAAAA")

# ── CHART 4: Case Fatality Rate by State ──────
ax4 = axes[1, 0]
df_cfr = df_states.sort_values("cfr", ascending=False)
cfr_colors = [ACCENT if v > df_cfr["cfr"].mean() else BLUE for v in df_cfr["cfr"]]
ax4.bar(df_cfr["state"], df_cfr["cfr"], color=cfr_colors, edgecolor="none")
ax4.axhline(df_cfr["cfr"].mean(), color="white", linestyle="--",
            linewidth=1, label=f'Avg: {df_cfr["cfr"].mean():.2f}%')
ax4.legend(fontsize=7, facecolor="#162032", labelcolor="white", framealpha=0.5)
ax4.tick_params(axis='x', rotation=45)
style_ax(ax4, "④ Case Fatality Rate by State (%)")
ax4.set_ylabel("CFR (%)", color="#AAAAAA", fontsize=8)
ax4.yaxis.label.set_color("#AAAAAA")

# ── CHART 5: Weekly New Cases ──────────────────
ax5 = axes[1, 1]
n = len(df_weekly)
week_colors = mpl.colormaps["plasma"](np.linspace(0.2, 0.9, n))
#week_colors = plt.cm.plasma(np.linspace(0.2, 0.9, n))
ax5.bar(range(n), df_weekly["cases"] / 1000, color=week_colors, width=0.8)
# Show every 8th week label
tick_pos = list(range(0, n, 8))
ax5.set_xticks(tick_pos)
ax5.set_xticklabels([df_weekly["week_str"].iloc[i][:7] for i in tick_pos],
                    rotation=45, fontsize=6)
style_ax(ax5, "⑤ Weekly New Cases (thousands)")
ax5.set_ylabel("Cases (thousands)", color="#AAAAAA", fontsize=8)
ax5.yaxis.label.set_color("#AAAAAA")

# ── CHART 6: Recovery Rate Trend ──────────────
ax6 = axes[1, 2]
rr = df_national["recovery_rate"].rolling(14).mean()
ax6.plot(df_national["date"], rr, color=GREEN, linewidth=1.5)
ax6.fill_between(df_national["date"], rr, 70, where=(rr >= 70),
                 alpha=0.2, color=GREEN, label="Above 70%")
ax6.axhline(70, color=ORANGE, linestyle="--", linewidth=1, label="70% threshold")
ax6.set_ylim(0, 105)
ax6.legend(fontsize=7, facecolor="#162032", labelcolor="white", framealpha=0.5)
style_ax(ax6, "⑥ Recovery Rate Trend (14-day avg)")
ax6.set_ylabel("Recovery Rate (%)", color="#AAAAAA", fontsize=8)
ax6.yaxis.label.set_color("#AAAAAA")

# STEP 3 — Master Title + Source Annotation

fig.suptitle("COVID-19 India — Comprehensive Dashboard (Jan 2020 – Dec 2021)",
             fontsize=16, fontweight="bold", color="white", y=0.98)

fig.text(0.5, 0.01,
         "Data source: covid19india.org / data.gov.in  |  Visualization: Python / Matplotlib  |  Author: [Your Name]",
         ha="center", fontsize=8, color="#888888", style="italic")

plt.tight_layout()
plt.subplots_adjust(top=0.93, bottom=0.06)
plt.savefig("C:/Users/Dell/pythonProjects/Day -4/outputs/project1_covid_dashboard.png",
            dpi=300, bbox_inches="tight", facecolor=DARK)
print("✅ Project 1 saved: project1_covid_dashboard.png")
plt.close()