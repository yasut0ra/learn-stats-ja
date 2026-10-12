"""第7章 代表的な離散分布"""

from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from scipy import stats

import style as S

CH = "ch07"


def binom_paths():
    n, k = 4, 2
    seqs = []
    for pos in combinations(range(n), k):
        seqs.append(["○" if i in pos else "×" for i in range(n)])
    fig, ax = plt.subplots(figsize=(8.4, 3.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.4, 6.4)
    ax.axis("off")
    for r, s in enumerate(seqs):
        y = 5.6 - r
        for i, c in enumerate(s):
            col = S.BLUE if c == "○" else S.MUTED
            ax.add_patch(FancyBboxPatch((0.4 + i * 0.75, y - 0.32), 0.6, 0.64,
                                        boxstyle="round,pad=0.0,rounding_size=0.12", fc=col, ec="none",
                                        alpha=1 if c == "○" else 0.35))
            ax.text(0.7 + i * 0.75, y, c, ha="center", va="center", fontsize=12,
                    color="white" if c == "○" else S.INK)
        ax.text(3.7, y, r"確率 $p \cdot p \cdot (1-p)(1-p) = p^2(1-p)^2$" if r == 0 else r"$p^2(1-p)^2$",
                va="center", fontsize=10.5, color=S.INK2)
    ax.annotate("", xy=(7.4, 5.8), xytext=(7.4, 0.4), arrowprops=dict(arrowstyle="-", color=S.INK2, lw=1.2))
    ax.text(7.6, 3.1, r"並べ方は $\binom{4}{2} = 6$ 通り" "\n\n" r"$P(X=2) = 6\,p^2(1-p)^2$",
            va="center", fontsize=11.5, color=S.INK)
    ax.text(0.4, 6.25, "4回の試行で成功（○）がちょうど2回になる並べ方", fontsize=10.5, color=S.INK2)
    S.save(fig, CH, "binom_paths")


def binom_shapes():
    fig, axes = plt.subplots(2, 3, figsize=(11, 5.2), sharey="row")
    for i, n in enumerate([10, 40]):
        for j, p in enumerate([0.1, 0.5, 0.8]):
            ax = axes[i, j]
            x = np.arange(0, n + 1)
            ax.bar(x, stats.binom.pmf(x, n, p), width=0.6, color=S.BLUE)
            ax.set_title(f"$B({n},\\ {p})$　平均 {n*p:g}, 分散 {n*p*(1-p):.2f}", fontsize=10.5)
            ax.set_xlim(-0.8, n + 0.8)
            ax.grid(axis="x", visible=False)
    fig.tight_layout()
    S.save(fig, CH, "binom_shapes")


def poisson_limit():
    lam = 3
    x = np.arange(0, 13)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.3), sharey=True)
    for ax, n in zip(axes, [6, 15, 60]):
        ax.bar(x, stats.binom.pmf(x, n, lam / n), width=0.6, color=S.BLUE, label=f"二項分布 $B({n},\\ 3/{n})$")
        ax.plot(x, stats.poisson.pmf(x, lam), "o", ms=7, color=S.ORANGE, mec=S.SURFACE, mew=1.5,
                label=r"ポアソン分布 $Po(3)$")
        ax.set_title(f"$n = {n}$", fontsize=11)
        ax.grid(axis="x", visible=False)
        ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    S.save(fig, CH, "poisson_limit")


def horsekick():
    obs = np.array([109, 65, 22, 3, 1])
    lam = 0.61
    exp_ = 200 * stats.poisson.pmf(np.arange(5), lam)
    exp_[-1] += 200 * stats.poisson.sf(4, lam)
    x = np.arange(5)
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    w = 0.36
    ax.bar(x - w / 2 - 0.01, obs, width=w, color=S.BLUE, label="実際の度数")
    ax.bar(x + w / 2 + 0.01, exp_, width=w, color=S.ORANGE, label=r"ポアソン分布 $Po(0.61)$ からの予測")
    for xi, o, e in zip(x, obs, exp_):
        ax.text(xi - w / 2, o + 2, str(o), ha="center", fontsize=9.5, color=S.INK2)
        ax.text(xi + w / 2, e + 2, f"{e:.1f}", ha="center", fontsize=9.5, color=S.INK2)
    ax.set_xticks(x)
    ax.set_xticklabels(["0人", "1人", "2人", "3人", "4人以上"])
    ax.set_xlabel("1年間に馬に蹴られて死亡した兵士の数（1軍団あたり）")
    ax.set_ylabel("軍団×年の数")
    ax.grid(axis="x", visible=False)
    ax.legend()
    S.save(fig, CH, "horsekick")


def poisson_shapes():
    fig, axes = plt.subplots(1, 4, figsize=(12, 2.9), sharey=True)
    x = np.arange(0, 25)
    for ax, lam in zip(axes, [0.5, 2, 5, 12]):
        ax.bar(x, stats.poisson.pmf(x, lam), width=0.6, color=S.BLUE)
        ax.set_title(f"$\\lambda = {lam}$", fontsize=11)
        ax.grid(axis="x", visible=False)
    fig.tight_layout()
    S.save(fig, CH, "poisson_shapes")


def geometric_memoryless():
    p = 0.25
    x = np.arange(0, 20)
    pmf = stats.geom.pmf(x + 1, p)
    s = 4
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.4))
    ax = axes[0]
    ax.bar(x, pmf, width=0.6, color=[S.BLUE if v >= s else S.AXIS for v in x])
    ax.axvline(s - 0.5, color=S.ORANGE, lw=1.4, ls=(0, (3, 2)))
    ax.text(s - 0.2, pmf.max() * 0.95, f"すでに{s}回失敗した", fontsize=10, color=S.INK)
    ax.set_title("幾何分布 $Ge(0.25)$：失敗の回数 $X$", fontsize=11)
    ax.grid(axis="x", visible=False)
    ax.set_xlabel("$x$")

    ax = axes[1]
    cond = pmf[s:] / pmf[s:].sum()
    ax.bar(x[: len(cond)], cond, width=0.6, color=S.BLUE, label=f"条件付き分布（{s}回失敗したあとの、さらなる失敗回数）")
    ax.plot(x, pmf, "o", ms=6, color=S.ORANGE, mec=S.SURFACE, mew=1.5, label="もとの分布")
    ax.set_title("残りの部分を拡大すると、もとの分布とまったく同じ", fontsize=11)
    ax.grid(axis="x", visible=False)
    ax.legend(fontsize=9)
    ax.set_xlabel("$x$")
    for ax in axes:
        ax.set_xticks(range(0, 20, 2))
    fig.tight_layout()
    S.save(fig, CH, "geometric_memoryless")


def hypergeom_vs_binom():
    n = 10
    x = np.arange(0, n + 1)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.3), sharey=True)
    for ax, N in zip(axes, [20, 1000]):
        M = int(0.3 * N)
        w = 0.36
        ax.bar(x - w / 2, stats.hypergeom.pmf(x, N, M, n), width=w, color=S.BLUE, label="超幾何分布（戻さない）")
        ax.bar(x + w / 2, stats.binom.pmf(x, n, 0.3), width=w, color=S.ORANGE, label="二項分布（戻す）")
        ax.set_title(f"全体 $N$ = {N} 個（うち当たり 30%）から {n} 個取り出す", fontsize=10.5)
        ax.grid(axis="x", visible=False)
        ax.set_xticks(x)
        ax.legend(fontsize=9)
    fig.tight_layout()
    S.save(fig, CH, "hypergeom_vs_binom")


def main():
    binom_paths()
    binom_shapes()
    poisson_limit()
    horsekick()
    poisson_shapes()
    geometric_memoryless()
    hypergeom_vs_binom()
