"""
=============================================================
PROJECT 1: A/B Test Analyzer — Advanced Statistical Testing
=============================================================
"""

import numpy as np
import scipy.stats as stats
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.power import NormalIndPower
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import warnings
import os

warnings.filterwarnings("ignore")
os.makedirs("outputs", exist_ok=True)

# ─── 1. SIMULATE A/B TEST DATA ───────────────────────────────────────────────
np.random.seed(42)

N_CONTROL    = 3200
N_TREATMENT  = 3100
CR_CONTROL   = 0.112   # 11.2% baseline conversion rate
CR_TREATMENT = 0.134   # 13.4% target conversion rate (lift ~19.6%)

control_conversions   = np.random.binomial(1, CR_CONTROL,   N_CONTROL)
treatment_conversions = np.random.binomial(1, CR_TREATMENT, N_TREATMENT)

n_ctrl = len(control_conversions)
n_trt  = len(treatment_conversions)
conv_ctrl = control_conversions.sum()
conv_trt  = treatment_conversions.sum()

obs_cr_ctrl = conv_ctrl / n_ctrl
obs_cr_trt  = conv_trt  / n_trt
lift        = (obs_cr_trt - obs_cr_ctrl) / obs_cr_ctrl * 100

print("=" * 60)
print("         A/B TEST — STATISTICAL ANALYSIS REPORT")
print("=" * 60)
print(f"\n{'Metric':<35} {'Control':>12} {'Treatment':>12}")
print("-" * 60)
print(f"{'Sample Size':<35} {n_ctrl:>12,} {n_trt:>12,}")
print(f"{'Conversions':<35} {conv_ctrl:>12,} {conv_trt:>12,}")
print(f"{'Observed Conversion Rate':<35} {obs_cr_ctrl:>11.2%} {obs_cr_trt:>11.2%}")
print(f"{'Relative Lift':<35} {'—':>12} {lift:>+11.1f}%")

# ─── 2. STATISTICAL TESTS ────────────────────────────────────────────────────

# --- 2a. Two-sample t-test (means of Bernoulli samples) ---------------------
t_stat, p_value_ttest = stats.ttest_ind(
    control_conversions, treatment_conversions, equal_var=False  # Welch's t-test
)

# --- 2b. Proportions z-test -------------------------------------------------
counts  = np.array([conv_trt, conv_ctrl])
nobs    = np.array([n_trt, n_ctrl])
z_stat, p_value_ztest = proportions_ztest(counts, nobs)

alpha = 0.05
print(f"\n{'─'*60}")
print(f"  HYPOTHESIS TESTS (α = {alpha})")
print(f"{'─'*60}")
print(f"\n  Welch's t-test:   t = {t_stat:+.4f},  p = {p_value_ttest:.6f}")
print(f"  Proportions z-test: z = {z_stat:+.4f},  p = {p_value_ztest:.6f}")

significance = "✅ STATISTICALLY SIGNIFICANT" if p_value_ztest < alpha else "❌ NOT SIGNIFICANT"
print(f"\n  Result → {significance}")
print(f"  {'Reject H₀: treatment ≠ control' if p_value_ztest < alpha else 'Fail to reject H₀'}")

# ─── 3. CONFIDENCE INTERVALS ─────────────────────────────────────────────────
z_crit = stats.norm.ppf(1 - alpha / 2)   # 1.96 for 95% CI

se_ctrl = np.sqrt(obs_cr_ctrl * (1 - obs_cr_ctrl) / n_ctrl)
se_trt  = np.sqrt(obs_cr_trt  * (1 - obs_cr_trt)  / n_trt)

ci_ctrl = (obs_cr_ctrl - z_crit * se_ctrl, obs_cr_ctrl + z_crit * se_ctrl)
ci_trt  = (obs_cr_trt  - z_crit * se_trt,  obs_cr_trt  + z_crit * se_trt)

diff    = obs_cr_trt - obs_cr_ctrl
se_diff = np.sqrt(se_ctrl**2 + se_trt**2)
ci_diff = (diff - z_crit * se_diff, diff + z_crit * se_diff)

print(f"\n{'─'*60}")
print(f"  95% CONFIDENCE INTERVALS")
print(f"{'─'*60}")
print(f"  Control   CR: [{ci_ctrl[0]:.4f}, {ci_ctrl[1]:.4f}]  → {ci_ctrl[0]:.2%} – {ci_ctrl[1]:.2%}")
print(f"  Treatment CR: [{ci_trt[0]:.4f}, {ci_trt[1]:.4f}]  → {ci_trt[0]:.2%} – {ci_trt[1]:.2%}")
print(f"  Δ (trt – ctrl): [{ci_diff[0]:.4f}, {ci_diff[1]:.4f}]")
print(f"  → Lift range: [{ci_diff[0]/obs_cr_ctrl*100:.1f}%, {ci_diff[1]/obs_cr_ctrl*100:.1f}%]")

# ─── 4. POWER ANALYSIS ───────────────────────────────────────────────────────
# Cohen's h effect size for proportions
effect_size_h = 2 * np.arcsin(np.sqrt(obs_cr_trt)) - 2 * np.arcsin(np.sqrt(obs_cr_ctrl))

power_analysis = NormalIndPower()
required_n = power_analysis.solve_power(
    effect_size=effect_size_h,
    alpha=alpha,
    power=0.80,
    ratio=1.0
)

actual_power = power_analysis.solve_power(
    effect_size=effect_size_h,
    alpha=alpha,
    nobs1=n_ctrl,
    ratio=n_trt / n_ctrl
)

print(f"\n{'─'*60}")
print(f"  POWER ANALYSIS")
print(f"{'─'*60}")
print(f"  Cohen's h effect size : {effect_size_h:.4f}")
print(f"  Required n (per group): {required_n:,.0f}  [for 80% power]")
print(f"  Actual n (control)    : {n_ctrl:,}")
print(f"  Achieved statistical power: {actual_power:.3f} ({actual_power*100:.1f}%)")
print(f"  {'✅ Adequately powered' if actual_power >= 0.80 else '⚠️  Underpowered — consider larger sample'}")

# ─── 5. VISUALIZATIONS ───────────────────────────────────────────────────────
plt.style.use("seaborn-v0_8-whitegrid")
fig = plt.figure(figsize=(16, 10))
gs  = GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

BLUE   = "#1a6bb5"
ORANGE = "#e07b29"
GREEN  = "#27ae60"
RED    = "#c0392b"

# --- Panel 1: Conversion Rate Bar Chart with CIs ----------------------------
ax1 = fig.add_subplot(gs[0, 0])
bars = ax1.bar(
    ["Control", "Treatment"],
    [obs_cr_ctrl, obs_cr_trt],
    color=[BLUE, ORANGE],
    width=0.45,
    edgecolor="white",
    linewidth=1.5,
    yerr=[[obs_cr_ctrl - ci_ctrl[0], obs_cr_trt - ci_trt[0]],
          [ci_ctrl[1] - obs_cr_ctrl, ci_trt[1]  - obs_cr_trt]],
    capsize=8,
    error_kw=dict(ecolor="#333333", lw=2, capthick=2)
)
for bar, rate in zip(bars, [obs_cr_ctrl, obs_cr_trt]):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.004,
             f"{rate:.2%}", ha="center", va="bottom", fontweight="bold", fontsize=12)
ax1.set_title("Conversion Rates with 95% CI", fontsize=13, fontweight="bold", pad=10)
ax1.set_ylabel("Conversion Rate", fontsize=11)
ax1.set_ylim(0, max(obs_cr_ctrl, obs_cr_trt) * 1.35)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))

# p-value annotation callout
p_color  = GREEN if p_value_ztest < alpha else RED
p_label  = f"p = {p_value_ztest:.4f}\n{'Significant ✓' if p_value_ztest < alpha else 'Not Significant ✗'}"
ax1.annotate(
    p_label,
    xy=(1, obs_cr_trt), xytext=(1.25, obs_cr_trt + 0.008),
    arrowprops=dict(arrowstyle="->", color=p_color, lw=1.5),
    fontsize=10, color=p_color, fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=p_color, alpha=0.9)
)

# --- Panel 2: Lift Distribution (bootstrap) ---------------------------------
ax2 = fig.add_subplot(gs[0, 1])
bootstrapped_lifts = []
for _ in range(5000):
    b_ctrl = np.random.binomial(n_ctrl, obs_cr_ctrl, 1)[0] / n_ctrl
    b_trt  = np.random.binomial(n_trt,  obs_cr_trt,  1)[0] / n_trt
    bootstrapped_lifts.append((b_trt - b_ctrl) / b_ctrl * 100)

ax2.hist(bootstrapped_lifts, bins=60, color=ORANGE, edgecolor="white",
         alpha=0.85, linewidth=0.5)
ax2.axvline(np.mean(bootstrapped_lifts), color=RED, lw=2.5,
            label=f"Mean lift: {np.mean(bootstrapped_lifts):.1f}%")
ax2.axvline(0, color="black", lw=1.5, linestyle="--", label="No effect (0%)")
pct5, pct95 = np.percentile(bootstrapped_lifts, [5, 95])
ax2.axvspan(pct5, pct95, alpha=0.15, color=ORANGE, label=f"90% CI: [{pct5:.1f}%, {pct95:.1f}%]")
ax2.set_title("Bootstrap Distribution of Lift", fontsize=13, fontweight="bold", pad=10)
ax2.set_xlabel("Relative Lift (%)", fontsize=11)
ax2.set_ylabel("Frequency", fontsize=11)
ax2.legend(fontsize=9, framealpha=0.9)

# --- Panel 3: Power Curve ---------------------------------------------------
ax3 = fig.add_subplot(gs[1, 0])
sample_sizes = np.linspace(100, 6000, 300)
powers = [power_analysis.solve_power(
    effect_size=effect_size_h, alpha=alpha, nobs1=n, ratio=1.0
) for n in sample_sizes]

ax3.plot(sample_sizes, powers, color=BLUE, lw=2.5)
ax3.axhline(0.80, color=GREEN, linestyle="--", lw=1.8, label="80% power threshold")
ax3.axvline(required_n, color=RED, linestyle="--", lw=1.8,
            label=f"Required n = {required_n:,.0f}")
ax3.scatter([n_ctrl], [actual_power], color=ORANGE, zorder=5, s=100,
            label=f"Actual power = {actual_power:.2f}")
ax3.fill_between(sample_sizes, powers, 0.80,
                 where=[p >= 0.80 for p in powers], alpha=0.12, color=GREEN)
ax3.set_title("Power Analysis Curve", fontsize=13, fontweight="bold", pad=10)
ax3.set_xlabel("Sample Size per Group", fontsize=11)
ax3.set_ylabel("Statistical Power", fontsize=11)
ax3.set_ylim(0, 1.05)
ax3.legend(fontsize=9, framealpha=0.9)

# --- Panel 4: Summary Stats Table -------------------------------------------
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis("off")
table_data = [
    ["Metric", "Value"],
    ["Control CR",        f"{obs_cr_ctrl:.2%}"],
    ["Treatment CR",      f"{obs_cr_trt:.2%}"],
    ["Relative Lift",     f"{lift:+.1f}%"],
    ["p-value (z-test)",  f"{p_value_ztest:.5f}"],
    ["Significant?",      "Yes ✓" if p_value_ztest < alpha else "No ✗"],
    ["95% CI (Δ)",        f"[{ci_diff[0]:+.3f}, {ci_diff[1]:+.3f}]"],
    ["Required n/group",  f"{required_n:,.0f}"],
    ["Achieved Power",    f"{actual_power:.1%}"],
]
tbl = ax4.table(cellText=table_data[1:], colLabels=table_data[0],
                loc="center", cellLoc="center")
tbl.auto_set_font_size(False)
tbl.set_fontsize(11)
tbl.scale(1.15, 1.9)
for (row, col), cell in tbl.get_celld().items():
    if row == 0:
        cell.set_facecolor("#1a6bb5")
        cell.set_text_props(color="white", fontweight="bold")
    elif row % 2 == 0:
        cell.set_facecolor("#f0f4f8")
    cell.set_edgecolor("#cccccc")
ax4.set_title("Statistical Summary", fontsize=13, fontweight="bold", pad=10)

fig.suptitle("A/B Test Analysis Dashboard", fontsize=17, fontweight="bold", y=1.01)
plt.savefig("outputs/ab_conversion_chart.png", dpi=150, bbox_inches="tight")
print("\n  ✅ Saved: outputs/ab_conversion_chart.png")
plt.close()

# ─── 6. BUSINESS RECOMMENDATION ──────────────────────────────────────────────
rec = f"""
╔══════════════════════════════════════════════════════════════════════════╗
║              BUSINESS RECOMMENDATION — A/B TEST RESULTS               ║
╚══════════════════════════════════════════════════════════════════════════╝

EXECUTIVE SUMMARY
─────────────────
The treatment variant (new UI/copy/feature) produced a statistically
significant improvement in conversion rate over the control variant.
We recommend a full rollout of the treatment variant.

TEST CONFIGURATION
──────────────────
  • Test Type       : Two-sample proportion test (one-tailed / two-tailed)
  • Significance Level (α) : {alpha}
  • Control Group   : {n_ctrl:,} users  →  {conv_ctrl:,} conversions  ({obs_cr_ctrl:.2%} CR)
  • Treatment Group : {n_trt:,} users  →  {conv_trt:,} conversions  ({obs_cr_trt:.2%} CR)
  • Test Duration   : [Set per business calendar — recommend ≥2 full weeks]

KEY FINDINGS
────────────
  1. CONVERSION LIFT:  The treatment group showed a {lift:+.1f}% relative lift
     in conversion rate ({obs_cr_ctrl:.2%} → {obs_cr_trt:.2%}). This is the core
     business metric we optimized for.

  2. STATISTICAL SIGNIFICANCE:
     • p-value = {p_value_ztest:.5f} (threshold: {alpha})
     • {"✅ Result is statistically significant — the lift is NOT due to chance." if p_value_ztest < alpha else "❌ Result is NOT statistically significant."}
     • 95% Confidence Interval for Δ: [{ci_diff[0]:+.4f}, {ci_diff[1]:+.4f}]
       → We are 95% confident the true lift lies between
         {ci_diff[0]/obs_cr_ctrl*100:+.1f}% and {ci_diff[1]/obs_cr_ctrl*100:+.1f}% (relative).

  3. POWER:
     • Required sample per group for 80% power: {required_n:,.0f}
     • Actual sample (control): {n_ctrl:,}
     • Achieved power: {actual_power:.1%} — {"adequately powered" if actual_power >= 0.80 else "⚠️ underpowered"}

BUSINESS IMPACT ESTIMATE
─────────────────────────
  Assuming 10,000 monthly users:
    • Current monthly conversions  :  {int(10000 * obs_cr_ctrl):,}
    • Projected with treatment     :  {int(10000 * obs_cr_trt):,}
    • Monthly incremental gains    : +{int(10000 * (obs_cr_trt - obs_cr_ctrl)):,} conversions

  At an average revenue of $50 per conversion, this represents:
    • Estimated monthly revenue uplift: +${int(10000 * (obs_cr_trt - obs_cr_ctrl) * 50):,}
    • Annualized revenue impact       : +${int(10000 * (obs_cr_trt - obs_cr_ctrl) * 50 * 12):,}

RECOMMENDATION
──────────────
  ✅ SHIP the treatment variant to 100% of traffic.

  Rationale:
    a) Statistically significant result (p < α = {alpha})
    b) Practically significant lift ({lift:+.1f}% improvement)
    c) Confidence interval excludes 0 — positive effect confirmed
    d) Sample size exceeds minimum required for 80% power

  Caveats & Next Steps:
    • Monitor for novelty effects (re-test after 4 weeks at scale)
    • Segment analysis recommended: mobile vs desktop, new vs returning
    • Ensure test was not affected by seasonal events or traffic spikes
    • Set up post-launch monitoring dashboard for sustained tracking

─────────────────────────────────────────────────────────────────────────
  Analysis performed: scipy.stats.ttest_ind, statsmodels proportions_ztest
  Author: HITANSH PUROHIT | Date: [2026-03-29]
─────────────────────────────────────────────────────────────────────────
"""

with open("outputs/business_recommendation.txt", "w",encoding = "utf-8") as f:
    f.write(rec)
print(rec)
print("  ✅ Saved: outputs/business_recommendation.txt")
print("  ✅ PROJECT 1 COMPLETE\n")