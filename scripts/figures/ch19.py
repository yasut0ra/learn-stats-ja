"""第19章 分散分析"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

import style as S

CH = "ch19"

GROUPS = {"A": [20, 22, 19, 24, 20], "B": [25, 27, 24, 28, 26], "C": [22, 24, 21, 23, 25]}
COLORS = [S.BLUE, S.ORANGE, S.AQUA]
MARKERS = ["o", "s", "^"]


def variation():
    allv = np.concatenate([np.array(v) for v in GROUPS.values()])
    gm = allv.mean()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.0), sharey=True)
    for k, ax in enumerate(axes):
        ax.axhline(gm, color=S.INK2, lw=1.3, ls=(0, (4, 3)))
        ax.text(2.55, gm + 0.15, "全体の平均", fontsize=9.5, color=S.INK2, va="bottom", ha="right")
        for i, ((name, v), col, mk) in enumerate(zip(GROUPS.items(), COLORS, MARKERS)):
            v = np.array(v)
            xs = i + np.linspace(-0.18, 0.18, len(v))
            m = v.mean()
            ax.plot([i - 0.3, i + 0.3], [m, m], color=col, lw=2.5)
            if k == 0:
                ax.annotate("", xy=(i + 0.34, m), xytext=(i + 0.34, gm),
                            arrowprops=dict(arrowstyle="<->", color=col, lw=1.6))
            else:
                for x, y in zip(xs, v):
                    ax.plot([x, x], [m, y], color=col, lw=1.2, alpha=0.8)
            ax.scatter(xs, v, s=46, color=col, marker=mk, edgecolor=S.SURFACE, lw=1.2, zorder=3)
        ax.set_xticks(range(3))
        ax.set_xticklabels([f"肥料{n}" for n in GROUPS])
        ax.grid(axis="x", visible=False)
        ax.set_xlim(-0.6, 2.6)
    axes[0].set_ylabel("収穫量 (kg)")
    axes[0].set_title("群間の変動：グループ平均と全体平均のずれ", fontsize=11)
    axes[1].set_title("群内の変動：各データとグループ平均のずれ", fontsize=11)
    fig.tight_layout()
    S.save(fig, CH, "variation")


def f_intuition():
    rng = np.random.default_rng(19)
    means = [21, 26, 23]
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.7), sharey=True)
    for ax, sd, title in [(axes[0], 1.0, "群内のばらつきが小さい → 差は明らか"),
                          (axes[1], 5.0, "群内のばらつきが大きい → 差は埋もれる")]:
        for i, (m, col, mk) in enumerate(zip(means, COLORS, MARKERS)):
            v = m + rng.normal(0, sd, 8)
            ax.scatter(i + rng.uniform(-0.15, 0.15, 8), v, s=36, color=col, marker=mk, edgecolor=S.SURFACE, lw=1)
            ax.plot([i - 0.3, i + 0.3], [m, m], color=col, lw=2.5)
        ax.set_xticks(range(3))
        ax.set_xticklabels(["A", "B", "C"])
        ax.set_title(title, fontsize=11)
        ax.grid(axis="x", visible=False)
    fig.suptitle("グループ平均の差は同じでも、群内のばらつきによって判断は変わる", fontsize=11, y=1.02)
    fig.tight_layout()
    S.save(fig, CH, "f_intuition")


def f_test():
    xs = np.linspace(0, 14, 500)
    y = stats.f.pdf(xs, 2, 12)
    fig, ax = plt.subplots(figsize=(7.8, 3.4))
    ax.plot(xs, y, color=S.BLUE)
    crit = stats.f.isf(0.05, 2, 12)
    m = xs >= crit
    ax.fill_between(xs[m], y[m], color=S.ORANGE, alpha=0.35, lw=0)
    ax.axvline(10.56, color=S.INK, lw=1.4)
    ax.text(10.7, 0.3, "観測値\n$F$ = 10.56\n$p$ = 0.002", fontsize=10.5)
    ax.text(crit + 0.15, 0.18, f"5% 点 {crit:.2f}", fontsize=9.5, color=S.INK2)
    ax.set_title("$H_0$ のもとでの $F$ 統計量の分布 $F(2, 12)$", fontsize=11)
    S.only_x_axis(ax)
    S.save(fig, CH, "f_test")


def interaction():
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
    cases = [("交互作用なし：線が平行", {"肥料A": (20, 24), "肥料B": (23, 27)}),
             ("交互作用あり：線が平行でない", {"肥料A": (20, 24), "肥料B": (22, 30)})]
    for ax, (title, d) in zip(axes, cases):
        for (name, (lo, hi)), col, mk in zip(d.items(), [S.BLUE, S.ORANGE], ["o", "s"]):
            ax.plot([0, 1], [lo, hi], color=col, lw=2, marker=mk, ms=8, mec=S.SURFACE, mew=1.5, label=name)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["水やり少", "水やり多"])
        ax.set_xlim(-0.3, 1.3)
        ax.set_title(title, fontsize=11)
        ax.legend(loc="upper left")
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("平均収穫量")
    fig.tight_layout()
    S.save(fig, CH, "interaction")


def main():
    variation()
    f_intuition()
    f_test()
    interaction()
