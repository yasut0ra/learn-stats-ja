"""第17章 いろいろな検定"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

import style as S

CH = "ch17"


def t_one_sample():
    t_obs, df = 2.232, 9
    xs = np.linspace(-4.5, 4.5, 600)
    y = stats.t.pdf(xs, df)
    fig, ax = plt.subplots(figsize=(8.2, 3.5))
    ax.plot(xs, y, color=S.BLUE, label="$t(9)$")
    ax.plot(xs, stats.norm.pdf(xs), color=S.MUTED, lw=1.4, ls=(0, (4, 3)), label="$N(0, 1)$")
    crit = stats.t.isf(0.025, df)
    for m in [xs >= t_obs, xs <= -t_obs]:
        ax.fill_between(xs[m], y[m], color=S.ORANGE, alpha=0.5, lw=0)
    for c in (-crit, crit):
        ax.axvline(c, color=S.INK2, lw=1, ls=(0, (3, 2)))
    ax.axvline(t_obs, color=S.INK, lw=1.5)
    ax.text(t_obs + 0.1, 0.25, f"観測値\n$t$ = {t_obs}", fontsize=10.5)
    ax.text(crit + 0.1, 0.12, f"臨界値 {crit:.3f}", fontsize=9.5, color=S.INK2)
    ax.set_title("1標本 $t$ 検定：$p$ 値（橙）= 0.0525。わずかに 0.05 を超える", fontsize=11)
    ax.legend(loc="upper left")
    S.only_x_axis(ax)
    S.save(fig, CH, "t_one_sample")


def welch_vs_pooled():
    rng = np.random.default_rng(17)
    scenarios = [("n 同じ・分散同じ\n(10, 10), σ=(1, 1)", 10, 10, 1, 1),
                 ("n 同じ・分散違う\n(10, 10), σ=(1, 3)", 10, 10, 1, 3),
                 ("小さい群の分散が大\n(5, 25), σ=(3, 1)", 5, 25, 3, 1),
                 ("大きい群の分散が大\n(5, 25), σ=(1, 3)", 5, 25, 1, 3)]
    reps = 40000
    pooled, welch = [], []
    for _, n1, n2, s1, s2 in scenarios:
        x = rng.normal(0, s1, (reps, n1))
        y = rng.normal(0, s2, (reps, n2))
        pooled.append(np.mean(stats.ttest_ind(x, y, axis=1).pvalue < 0.05))
        welch.append(np.mean(stats.ttest_ind(x, y, axis=1, equal_var=False).pvalue < 0.05))
    fig, ax = plt.subplots(figsize=(9, 3.8))
    idx = np.arange(len(scenarios))
    w = 0.34
    ax.bar(idx - w / 2 - 0.01, pooled, width=w, color=S.ORANGE, label="スチューデントの $t$ 検定（等分散を仮定）")
    ax.bar(idx + w / 2 + 0.01, welch, width=w, color=S.BLUE, label="ウェルチの $t$ 検定")
    for i in idx:
        ax.text(i - w / 2, pooled[i] + 0.004, f"{pooled[i]*100:.1f}%", ha="center", fontsize=9.5, color=S.INK2)
        ax.text(i + w / 2, welch[i] + 0.004, f"{welch[i]*100:.1f}%", ha="center", fontsize=9.5, color=S.INK2)
    ax.axhline(0.05, color=S.INK2, lw=1.2, ls=(0, (4, 3)))
    ax.set_xticks(idx)
    ax.set_xticklabels([s[0] for s in scenarios], fontsize=9.5)
    ax.set_ylabel("実際の第1種の過誤の確率")
    ax.set_ylim(0, 0.36)
    ax.legend(loc="upper left", fontsize=9.5)
    ax.grid(axis="x", visible=False)
    ax.set_title("有意水準 5% のつもりでも、等分散を仮定した検定は大きく狂うことがある", fontsize=11)
    S.save(fig, CH, "welch_vs_pooled")


def paired_plot():
    before = np.array([148, 152, 139, 160, 145, 155, 142, 150])
    after = np.array([140, 147, 138, 151, 143, 146, 141, 144])
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.9), gridspec_kw={"width_ratios": [1.2, 1]})
    ax = axes[0]
    for b, a in zip(before, after):
        ax.plot([0, 1], [b, a], color=S.BLUE, lw=1.6, marker="o", ms=6, mec=S.SURFACE, mew=1.5)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["服用前", "服用後"])
    ax.set_xlim(-0.3, 1.3)
    ax.set_ylabel("収縮期血圧 (mmHg)")
    ax.set_title("個人差は大きいが、全員が下がっている", fontsize=11)
    ax.grid(axis="x", visible=False)
    ax = axes[1]
    d = before - after
    vals, cnt = np.unique(d, return_counts=True)
    for v, c in zip(vals, cnt):
        for k in range(c):
            ax.scatter(v, k + 1, s=110, color=S.ORANGE, edgecolor=S.SURFACE, lw=1.5)
    ax.axvline(0, color=S.INK2, lw=1.2)
    ax.axvline(d.mean(), color=S.ORANGE, lw=1.4, ls=(0, (3, 2)))
    ax.text(d.mean() + 0.2, 2.6, f"平均 {d.mean():.3f}", fontsize=10, color=S.INK)
    ax.set_ylim(0, 3)
    ax.set_yticks([])
    ax.set_xlim(-2, 11)
    ax.set_xlabel("差（前 − 後）")
    ax.set_title("差だけを見ると、0 から明らかに離れている", fontsize=11)
    ax.grid(False)
    fig.tight_layout()
    S.save(fig, CH, "paired_plot")


def chi2_gof():
    obs = np.array([15, 22, 18, 25, 16, 24])
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.6))
    ax = axes[0]
    x = np.arange(1, 7)
    ax.bar(x, obs, width=0.5, color=S.BLUE, label="観測度数 $O$")
    ax.axhline(20, color=S.ORANGE, lw=2, label="期待度数 $E = 20$")
    for xi, o in zip(x, obs):
        ax.text(xi, o + 0.5, str(o), ha="center", fontsize=10, color=S.INK2)
    ax.set_xticks(x)
    ax.set_xlabel("出た目")
    ax.set_ylim(0, 30)
    ax.legend(loc="upper left", fontsize=9.5)
    ax.grid(axis="x", visible=False)
    ax.set_title("サイコロを120回振った結果", fontsize=11)
    ax = axes[1]
    xs = np.linspace(0, 20, 400)
    y = stats.chi2.pdf(xs, 5)
    ax.plot(xs, y, color=S.BLUE)
    m = xs >= 4.5
    ax.fill_between(xs[m], y[m], color=S.ORANGE, alpha=0.45, lw=0)
    crit = stats.chi2.isf(0.05, 5)
    ax.axvline(crit, color=S.INK2, lw=1, ls=(0, (3, 2)))
    ax.text(crit + 0.2, 0.12, f"5% 点\n{crit:.2f}", fontsize=9.5, color=S.INK2)
    ax.axvline(4.5, color=S.INK, lw=1.4)
    ax.text(4.7, 0.15, "観測値 4.5\n$p$ = 0.48", fontsize=10.5)
    ax.set_title("$H_0$ のもとでの $\\chi^2$ 統計量の分布 $\\chi^2(5)$", fontsize=11)
    S.only_x_axis(ax)
    fig.tight_layout()
    S.save(fig, CH, "chi2_gof")


def contingency_bar():
    rows = [("20代 (70人)", 30, 40), ("40代 (70人)", 35, 35), ("60代 (60人)", 40, 20)]
    fig, ax = plt.subplots(figsize=(7.8, 2.8))
    for i, (name, a, b) in enumerate(rows[::-1]):
        p = a / (a + b)
        ax.barh(i, p, color=S.BLUE, height=0.55)
        ax.barh(i, 1 - p, left=p, color=S.ORANGE, height=0.55)
        ax.text(p / 2, i, f"支持 {p*100:.0f}%", ha="center", va="center", color="white", fontsize=10)
        ax.text(p + (1 - p) / 2, i, f"不支持 {(1-p)*100:.0f}%", ha="center", va="center", color="white", fontsize=10)
    ax.axvline(105 / 200, color=S.INK, lw=1.2, ls=(0, (3, 2)))
    ax.text(105 / 200, 2.45, "全体 52.5%", ha="center", fontsize=9.5, color=S.INK)
    ax.set_yticks(range(3))
    ax.set_yticklabels([r[0] for r in rows[::-1]])
    ax.set_xlim(0, 1)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.set_ylim(-0.5, 2.7)
    ax.grid(axis="y", visible=False)
    S.save(fig, CH, "contingency_bar")


def qqplots():
    rng = np.random.default_rng(23)
    n = 60
    data = [("正規分布からのデータ", rng.normal(50, 10, n)),
            ("右に歪んだデータ（指数分布）", rng.exponential(10, n)),
            ("裾の重いデータ（t 分布 自由度2）", rng.standard_t(2, n))]
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.5))
    for ax, (title, x) in zip(axes, data):
        x = np.sort(x)
        q = stats.norm.ppf((np.arange(1, n + 1) - 0.5) / n)
        ax.scatter(q, x, s=18, color=S.BLUE, edgecolor=S.SURFACE, lw=0.6, zorder=3)
        q1, q3 = np.percentile(x, [25, 75])
        z1, z3 = stats.norm.ppf([0.25, 0.75])
        slope = (q3 - q1) / (z3 - z1)
        ax.plot([-2.6, 2.6], [q1 + slope * (-2.6 - z1), q1 + slope * (2.6 - z1)], color=S.ORANGE, lw=1.6)
        ax.set_title(title, fontsize=10.5)
        ax.set_xlabel("標準正規分布の分位点")
    axes[0].set_ylabel("データの値（小さい順）")
    fig.tight_layout()
    S.save(fig, CH, "qqplots")


def ranks():
    a = np.array([12.1, 14.3, 15.0, 17.8, 19.2])
    b = np.array([16.4, 20.5, 21.1, 22.9, 25.0, 26.3])
    allv = np.concatenate([a, b])
    order = np.argsort(allv)
    rk = np.empty(len(allv), int)
    rk[order] = np.arange(1, len(allv) + 1)
    fig, ax = plt.subplots(figsize=(9, 2.4))
    ax.plot([10, 28], [0, 0], color=S.AXIS, lw=1)
    ax.scatter(a, np.zeros_like(a), s=110, color=S.BLUE, edgecolor=S.SURFACE, lw=1.5, zorder=3, label="グループA")
    ax.scatter(b, np.zeros_like(b), s=110, marker="s", color=S.ORANGE, edgecolor=S.SURFACE, lw=1.5, zorder=3,
               label="グループB")
    for v, r in zip(allv, rk):
        ax.text(v, 0.32, str(r), ha="center", fontsize=10.5, color=S.INK)
    ax.text(10.2, 0.32, "順位：", fontsize=10, color=S.INK2)
    ax.set_ylim(-0.5, 0.7)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.grid(False)
    ax.set_xlim(10, 28)
    ax.legend(loc="lower right", ncol=2, fontsize=9.5)
    ax.set_title(f"値を順位に置き換える：A の順位和 = {rk[:5].sum()}、B の順位和 = {rk[5:].sum()}", fontsize=11)
    S.save(fig, CH, "ranks")


def main():
    t_one_sample()
    welch_vs_pooled()
    paired_plot()
    chi2_gof()
    contingency_bar()
    qqplots()
    ranks()
