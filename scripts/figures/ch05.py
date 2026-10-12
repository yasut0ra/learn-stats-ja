"""第5章 確率変数と確率分布"""

from itertools import product

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from scipy import stats

import style as S

CH = "ch05"


def rv_mapping():
    outcomes = ["".join(p) for p in product("表裏", repeat=3)]
    vals = [o.count("表") for o in outcomes]
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.3, 8.6)
    ax.axis("off")
    ax.text(1.5, 8.35, r"標本空間 $\Omega$（根元事象）", ha="center", fontsize=11, color=S.INK)
    ax.text(8.0, 8.35, r"$X$ の値（実数）", ha="center", fontsize=11, color=S.INK)
    ys = np.arange(len(outcomes))[::-1] * 1.0
    targets = {3: 6.6, 2: 4.6, 1: 2.6, 0: 0.6}
    cols = {3: S.BLUE, 2: S.ORANGE, 1: S.AQUA, 0: S.VIOLET}
    for o, v, y in zip(outcomes, vals, ys):
        ax.add_patch(FancyBboxPatch((0.6, y - 0.32), 1.8, 0.64, boxstyle="round,pad=0.02,rounding_size=0.15",
                                    fc="#f2f1ec", ec="none"))
        ax.text(1.5, y, o, ha="center", va="center", fontsize=11)
        ax.annotate("", xy=(7.5, targets[v]), xytext=(2.5, y),
                    arrowprops=dict(arrowstyle="-|>", color=cols[v], lw=1.3, alpha=0.8, shrinkA=2, shrinkB=6))
    for v, y in targets.items():
        ax.scatter([8.0], [y], s=420, color=cols[v], zorder=3)
        ax.text(8.0, y, str(v), ha="center", va="center", fontsize=13, color="white", weight="bold", zorder=4)
        ax.text(8.6, y, f"確率 {[1, 3, 3, 1][3 - v]}/8", va="center", fontsize=10.5, color=S.INK2)
    ax.text(5.0, -1.05, r"$X$ = 表の枚数：各結果に数を1つ対応させる「関数」", ha="center", fontsize=10.5, color=S.INK2)
    S.save(fig, CH, "rv_mapping")


def pmf_coin3():
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    x = np.arange(4)
    p = np.array([1, 3, 3, 1]) / 8
    ax.bar(x, p, width=0.45, color=S.BLUE)
    for xi, pi in zip(x, p):
        ax.text(xi, pi + 0.01, f"{int(pi*8)}/8", ha="center", va="bottom", fontsize=10.5, color=S.INK2)
    ax.set_xticks(x)
    ax.set_xlabel("$x$（表の枚数）")
    ax.set_ylabel("$P(X = x)$")
    ax.set_ylim(0, 0.46)
    ax.grid(axis="x", visible=False)
    S.save(fig, CH, "pmf_coin3")


def dice_sum():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.0), gridspec_kw={"width_ratios": [1, 1.3]})
    ax = axes[0]
    cmap = plt.get_cmap("Blues")
    for i in range(1, 7):
        for j in range(1, 7):
            s = i + j
            shade = 0.15 + 0.7 * (6 - abs(s - 7)) / 6
            ax.add_patch(plt.Rectangle((i - 0.5, j - 0.5), 0.94, 0.94, fc=cmap(shade), ec="none"))
            ax.text(i - 0.03, j - 0.03, str(s), ha="center", va="center", fontsize=10,
                    color="white" if shade > 0.55 else S.INK)
    ax.set_xlim(0.4, 6.6)
    ax.set_ylim(0.4, 6.6)
    ax.set_aspect("equal")
    ax.set_xticks(range(1, 7))
    ax.set_yticks(range(1, 7))
    ax.grid(False)
    ax.set_xlabel("1個目の目")
    ax.set_ylabel("2個目の目")
    ax.set_title("36通りの結果と目の和", fontsize=11)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    ax = axes[1]
    xs = np.arange(2, 13)
    ps = (6 - np.abs(xs - 7)) / 36
    ax.bar(xs, ps, width=0.55, color=S.BLUE)
    for xi, pi in zip(xs, ps):
        ax.text(xi, pi + 0.004, f"{int(round(pi*36))}", ha="center", va="bottom", fontsize=9.5, color=S.INK2)
    ax.set_xticks(xs)
    ax.set_xlabel("目の和 $x$")
    ax.set_ylabel("$P(X = x)$")
    ax.set_title("和の確率分布（棒の上の数 ÷ 36）", fontsize=11)
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    S.save(fig, CH, "dice_sum")


def cdf_step():
    x = np.arange(4)
    p = np.array([1, 3, 3, 1]) / 8
    F = np.cumsum(p)
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    edges = [-1.0, 0, 1, 2, 3, 4.0]
    levels = [0, *F]
    for k in range(len(levels)):
        ax.plot([edges[k], edges[k + 1]], [levels[k], levels[k]], color=S.BLUE, lw=2.2)
    for k in range(4):
        ax.scatter([x[k]], [F[k]], s=46, color=S.BLUE, zorder=3)
        ax.scatter([x[k]], [levels[k]], s=46, facecolor=S.SURFACE, edgecolor=S.BLUE, lw=1.8, zorder=3)
        ax.plot([x[k], x[k]], [levels[k], F[k]], color=S.BLUE, lw=1, ls=(0, (2, 2)))
    ax.annotate("跳びの大きさ\n= P(X = 1) = 3/8", xy=(1.05, 0.31), xytext=(1.5, 0.12), fontsize=10, color=S.INK2,
                arrowprops=dict(arrowstyle="-|>", color=S.MUTED, lw=1))
    ax.set_xlim(-1, 4)
    ax.set_ylim(-0.05, 1.1)
    ax.set_yticks([0, 1 / 8, 4 / 8, 7 / 8, 1])
    ax.set_yticklabels(["0", "1/8", "4/8", "7/8", "1"])
    ax.set_xlabel("$x$")
    ax.set_ylabel(r"$F(x) = P(X \leq x)$")
    S.save(fig, CH, "cdf_step")


def hist_to_density():
    rng = np.random.default_rng(12)
    data = rng.gamma(4, 1.0, 200000)
    xs = np.linspace(0, 14, 400)
    fig, axes = plt.subplots(1, 4, figsize=(12, 2.9), sharey=True)
    for ax, w in zip(axes[:3], [2.0, 1.0, 0.25]):
        bins = np.arange(0, 14 + w, w)
        ax.hist(data, bins=bins, density=True, color=S.BLUE, edgecolor=S.SURFACE, lw=0.8 if w < 0.5 else 1.5)
        ax.set_title(f"階級幅 {w}", fontsize=10.5)
    axes[3].fill_between(xs, stats.gamma.pdf(xs, 4), color=S.BLUE, alpha=0.18, lw=0)
    axes[3].plot(xs, stats.gamma.pdf(xs, 4), color=S.BLUE)
    axes[3].set_title("幅 → 0 の極限：確率密度関数", fontsize=10.5)
    for ax in axes:
        ax.set_xlim(0, 14)
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("相対度数 ÷ 階級幅")
    fig.tight_layout()
    S.save(fig, CH, "hist_to_density")


def pdf_cdf():
    a, b = 2.0, 5.0
    xs = np.linspace(0, 14, 500)
    f = stats.gamma.pdf(xs, 4)
    F = stats.gamma.cdf(xs, 4)
    pa, pb = stats.gamma.cdf(a, 4), stats.gamma.cdf(b, 4)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.6))
    ax = axes[0]
    ax.plot(xs, f, color=S.BLUE)
    m = (xs >= a) & (xs <= b)
    ax.fill_between(xs[m], f[m], color=S.BLUE, alpha=0.3, lw=0)
    ax.text(3.5, 0.06, f"面積\n= {pb-pa:.3f}", ha="center", fontsize=10.5, color=S.INK)
    ax.set_xticks([0, a, b, 10])
    ax.set_xticklabels(["0", "$a$", "$b$", "10"])
    ax.set_title(r"密度関数 $f(x)$：$P(a \leq X \leq b)$ は面積", fontsize=11)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 0.24)
    ax = axes[1]
    ax.plot(xs, F, color=S.BLUE)
    for v, Fv in [(a, pa), (b, pb)]:
        ax.plot([v, v], [0, Fv], color=S.MUTED, lw=1, ls=(0, (3, 2)))
        ax.plot([0, v], [Fv, Fv], color=S.MUTED, lw=1, ls=(0, (3, 2)))
        ax.scatter([v], [Fv], s=40, color=S.BLUE, edgecolor=S.SURFACE, lw=1.5, zorder=3)
    ax.annotate("", xy=(0.5, pb), xytext=(0.5, pa), arrowprops=dict(arrowstyle="<->", color=S.ORANGE, lw=1.6))
    ax.text(0.8, (pa + pb) / 2, f"$F(b) - F(a)$\n= {pb-pa:.3f}", va="center", fontsize=10.5, color=S.INK)
    ax.set_xticks([0, a, b, 10])
    ax.set_xticklabels(["0", "$a$", "$b$", "10"])
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 1.05)
    ax.set_title(r"累積分布関数 $F(x)$：同じ確率は高さの差", fontsize=11)
    fig.tight_layout()
    S.save(fig, CH, "pdf_cdf")


def quantile():
    xs = np.linspace(0, 14, 500)
    F = stats.gamma.cdf(xs, 4)
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.plot(xs, F, color=S.BLUE)
    for p, lab in [(0.25, "第1四分位点"), (0.5, "中央値"), (0.9, "90%点")]:
        q = stats.gamma.ppf(p, 4)
        ax.plot([0, q], [p, p], color=S.ORANGE, lw=1.2, ls=(0, (3, 2)))
        ax.plot([q, q], [0, p], color=S.ORANGE, lw=1.2, ls=(0, (3, 2)))
        ax.scatter([q], [p], s=40, color=S.ORANGE, edgecolor=S.SURFACE, lw=1.5, zorder=3)
        ax.text(q + 0.25, p - 0.07, f"{lab} {q:.2f}", fontsize=10, color=S.INK)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 1.04)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$F(x)$")
    ax.set_title("縦軸の値 $p$ から横軸の値を読む：$p$ 分位点", fontsize=11)
    S.save(fig, CH, "quantile")


def main():
    rv_mapping()
    pmf_coin3()
    dice_sum()
    cdf_step()
    hist_to_density()
    pdf_cdf()
    quantile()
