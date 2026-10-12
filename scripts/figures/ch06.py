"""第6章 期待値と分散"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

import style as S

CH = "ch06"


def fulcrum(ax, x, top, label):
    """y=0 の板の下に支点（三角形）を描く。top は y 軸の上端。"""
    ax.axhline(0, color=S.INK2, lw=2.5, zorder=3)
    ax.plot([x], [-0.075 * top], marker="^", ms=17, color=S.ORANGE, mec="none", zorder=4, clip_on=False)
    ax.text(x + 0.03 * np.diff(ax.get_xlim())[0], -0.1 * top, label, ha="left", va="center", fontsize=10.5,
            color=S.INK)
    ax.set_ylim(-0.17 * top, top)
    ax.spines["bottom"].set_visible(False)


def expectation_balance():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.8))
    ax = axes[0]
    x = np.arange(0, 9)
    p = stats.binom.pmf(x, 8, 0.3)
    m = (x * p).sum()
    ax.bar(x, p, width=0.5, color=S.BLUE)
    ax.set_xticks(x)
    ax.set_xlim(-0.6, 8.6)
    ax.set_yticks([0, 0.1, 0.2, 0.3])
    fulcrum(ax, m, 0.34, f"期待値 {m:.1f}")
    ax.set_title("確率関数：確率を「おもり」とみたときの重心", fontsize=10.5)

    ax = axes[1]
    xs = np.linspace(0, 12, 400)
    f = stats.gamma.pdf(xs, 2.5, scale=1.4)
    m = 2.5 * 1.4
    ax.fill_between(xs, f, color=S.BLUE, alpha=0.25, lw=0)
    ax.plot(xs, f, color=S.BLUE)
    ax.set_xlim(0, 12)
    ax.set_yticks([0, 0.1, 0.2])
    fulcrum(ax, m, 0.25, f"期待値 {m:.1f}")
    ax.set_title("密度関数：板の形をした物体の重心", fontsize=10.5)
    fig.tight_layout()
    S.save(fig, CH, "expectation_balance")


def variance_compare():
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.2), sharey=True)
    x = np.arange(1, 10)
    pa = np.array([0, 0, 1, 4, 10, 4, 1, 0, 0]) / 20
    pb = np.array([2, 2, 2, 3, 2, 3, 2, 2, 2]) / 20
    for ax, p, title, col in [(axes[0], pa, "分散が小さい", S.BLUE), (axes[1], pb, "分散が大きい", S.ORANGE)]:
        m = (x * p).sum()
        v = ((x - m) ** 2 * p).sum()
        ax.bar(x, p, width=0.5, color=col)
        ax.axvline(m, color=S.INK2, lw=1.2, ls=(0, (3, 2)))
        ax.set_title(f"{title}：$E[X]$ = {m:g}, $V[X]$ = {v:.2f}", fontsize=10.5)
        ax.set_xticks(x)
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("$P(X = x)$")
    fig.tight_layout()
    S.save(fig, CH, "variance_compare")


def chebyshev_bound():
    k = np.linspace(1, 4, 300)
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    ax.plot(k, 1 / k**2, color=S.INK2, lw=2.2, label=r"チェビシェフの上限 $1/k^2$")
    ax.plot(k, 2 * stats.norm.sf(k), color=S.BLUE, label="正規分布")
    ax.plot(k, np.exp(-(1 + k)), color=S.ORANGE, label="指数分布")
    ax.plot(k, np.clip(1 - k / np.sqrt(3), 0, None), color=S.AQUA, label="一様分布")
    ax.set_xlabel("$k$（平均から標準偏差 $k$ 個ぶん）")
    ax.set_ylabel(r"$P(|X-\mu| \geq k\sigma)$")
    ax.set_xlim(1, 4)
    ax.set_ylim(0, 1.02)
    ax.legend(loc="upper right")
    ax.set_title("実際の確率は、どの分布でも上限 $1/k^2$ を下回る", fontsize=11)
    S.save(fig, CH, "chebyshev_bound")


def skew_kurt():
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.6))
    ax = axes[0]
    xs = np.linspace(-4, 4, 500)
    a = 4.0
    g = stats.gamma(a, loc=-np.sqrt(a), scale=1 / np.sqrt(a))  # 平均0, 分散1
    ax.plot(xs, g.pdf(xs), color=S.BLUE, label=f"右に歪む（歪度 {2/np.sqrt(a):.1f}）")
    ax.plot(xs, stats.norm.pdf(xs), color=S.MUTED, label="対称（歪度 0）")
    ax.plot(xs, g.pdf(-xs), color=S.ORANGE, label=f"左に歪む（歪度 {-2/np.sqrt(a):.1f}）")
    ax.set_title("歪度：左右の非対称さ", fontsize=11)
    ax.legend(loc="upper left", fontsize=9)
    S.only_x_axis(ax)
    ax.set_ylim(0, 0.62)

    ax = axes[1]
    lap = stats.laplace(scale=1 / np.sqrt(2))
    uni = stats.uniform(loc=-np.sqrt(3), scale=2 * np.sqrt(3))
    ax.plot(xs, lap.pdf(xs), color=S.BLUE, label="尖って裾が重い（尖度 6）")
    ax.plot(xs, stats.norm.pdf(xs), color=S.MUTED, label="正規分布（尖度 3）")
    ax.plot(xs, uni.pdf(xs), color=S.ORANGE, label="平らで裾がない（尖度 1.8）")
    ax.set_title("尖度：裾の重さ（いずれも平均0・分散1）", fontsize=11)
    ax.legend(loc="upper left", fontsize=9)
    S.only_x_axis(ax)
    ax.set_ylim(0, 0.85)
    fig.tight_layout()
    S.save(fig, CH, "skew_kurt")


def mgf_tangent():
    t = np.linspace(-0.6, 0.45, 300)
    M = np.mean([np.exp(k * t) for k in range(1, 7)], axis=0)
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.plot(t, M, color=S.BLUE, label=r"$M(t) = E[e^{tX}]$（サイコロ）")
    ax.plot(t, 1 + 3.5 * t, color=S.ORANGE, lw=1.6, ls=(0, (5, 3)), label=r"$t=0$ での接線：傾き $M'(0) = E[X] = 3.5$")
    ax.scatter([0], [1], s=50, color=S.INK, zorder=3)
    ax.text(0.02, 0.8, r"$M(0) = 1$", fontsize=10.5, color=S.INK)
    ax.set_xlabel("$t$")
    ax.set_ylim(0, 4.6)
    ax.legend(loc="upper left")
    S.save(fig, CH, "mgf_tangent")


def main():
    expectation_balance()
    variance_compare()
    chebyshev_bound()
    skew_kurt()
    mgf_tangent()
