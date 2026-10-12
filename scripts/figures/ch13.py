"""第13章 母集団と標本分布"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from scipy import stats

import style as S

CH = "ch13"


def sampling_concept():
    rng = np.random.default_rng(31)
    pop = rng.gamma(3, 10, 100000)  # 右に歪んだ母集団（平均30）
    n = 10
    fig = plt.figure(figsize=(12, 4.2))
    ax_pop = fig.add_axes([0.02, 0.18, 0.25, 0.62])
    ax_pop.hist(pop, bins=60, range=(0, 120), density=True, color=S.MUTED, edgecolor=S.SURFACE, lw=0.4)
    ax_pop.axvline(30, color=S.INK2, lw=1.2, ls=(0, (3, 2)))
    ax_pop.set_title("母集団の分布（μ = 30）", fontsize=11)
    ax_pop.set_yticks([])
    ax_pop.grid(False)

    ys = [0.66, 0.42, 0.18]
    for k, y in enumerate(ys):
        ax = fig.add_axes([0.36, y, 0.24, 0.14])
        s = rng.choice(pop, n)
        ax.scatter(s, np.zeros(n), s=22, color=S.BLUE, alpha=0.8, lw=0)
        ax.axvline(s.mean(), color=S.ORANGE, lw=2)
        ax.text(s.mean() + 2, 0.55, f"x̄ = {s.mean():.1f}", fontsize=9.5, color=S.INK)
        ax.set_xlim(0, 120)
        ax.set_ylim(-0.6, 1)
        ax.set_yticks([])
        ax.grid(False)
        ax.spines["left"].set_visible(False)
        ax.tick_params(labelsize=8)
        ax.set_title(f"標本 {k+1}（n = {n}）", fontsize=9.5, loc="left", pad=2)
    fig.text(0.48, 0.07, "（これを何万回もくり返す）", ha="center", fontsize=10.5, color=S.INK2)

    ax_s = fig.add_axes([0.72, 0.18, 0.26, 0.62])
    means = rng.choice(pop, (20000, n)).mean(1)
    ax_s.hist(means, bins=60, range=(0, 120), density=True, color=S.ORANGE, edgecolor=S.SURFACE, lw=0.4)
    ax_s.axvline(30, color=S.INK2, lw=1.2, ls=(0, (3, 2)))
    ax_s.set_title("標本平均 X̄ の分布（標本分布）", fontsize=11)
    ax_s.set_yticks([])
    ax_s.grid(False)
    for (x0, y0), (x1, y1) in [((0.275, 0.5), (0.355, 0.73)), ((0.275, 0.5), (0.355, 0.49)),
                               ((0.275, 0.5), (0.355, 0.25)), ((0.61, 0.73), (0.715, 0.5)),
                               ((0.61, 0.49), (0.715, 0.5)), ((0.61, 0.25), (0.715, 0.5))]:
        fig.patches.append(FancyArrowPatch((x0, y0), (x1, y1), transform=fig.transFigure, arrowstyle="-|>",
                                           mutation_scale=12, color=S.AXIS, lw=1.2))
    S.save(fig, CH, "sampling_concept")


def unbiased_sim():
    rng = np.random.default_rng(13)
    n = 5
    x = rng.normal(0, 1, (100000, n))
    ss = ((x - x.mean(1, keepdims=True)) ** 2).sum(1)
    s_n, s_n1 = ss / n, ss / (n - 1)
    fig, ax = plt.subplots(figsize=(8, 3.6))
    bins = np.linspace(0, 4, 81)
    ax.hist(s_n, bins=bins, density=True, histtype="step", lw=2, color=S.ORANGE, label="$n$ で割る")
    ax.hist(s_n1, bins=bins, density=True, histtype="step", lw=2, color=S.BLUE, label="$n-1$ で割る（不偏分散）")
    ax.axvline(1, color=S.INK2, lw=1.2, ls=(0, (4, 3)))
    ax.axvline(s_n.mean(), color=S.ORANGE, lw=1.4)
    ax.axvline(s_n1.mean(), color=S.BLUE, lw=1.4)
    ax.text(2.0, 0.62, f"真の分散 σ² = 1（点線）\n不偏分散の平均 = {s_n1.mean():.3f}（青の縦線）\n"
            f"n で割った方の平均 = {s_n.mean():.3f}（橙の縦線）", fontsize=10, color=S.INK, va="top",
            transform=ax.get_xaxis_transform())
    ax.set_xlabel("分散の推定値")
    ax.set_yticks([])
    ax.legend(loc="upper right")
    ax.set_title("$N(0, 1)$ から $n = 5$ の標本を10万回とったときの分散の推定値", fontsize=11)
    S.save(fig, CH, "unbiased_sim")


def chi2_shapes():
    xs = np.linspace(0.01, 25, 500)
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    for k, col in zip([1, 2, 3, 5, 10], [S.VIOLET, S.BLUE, S.ORANGE, S.AQUA, S.MAGENTA]):
        ax.plot(xs, stats.chi2.pdf(xs, k), color=col, label=f"自由度 {k}")
    ax.set_ylim(0, 0.55)
    ax.set_xlim(0, 25)
    ax.legend()
    ax.set_title("カイ二乗分布 $\\chi^2(k)$：平均 $k$、分散 $2k$", fontsize=11)
    S.only_x_axis(ax)
    S.save(fig, CH, "chi2_shapes")


def t_vs_normal():
    xs = np.linspace(-5, 5, 600)
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.6))
    ax = axes[0]
    ax.plot(xs, stats.norm.pdf(xs), color=S.INK2, lw=2, ls=(0, (4, 3)), label="標準正規分布")
    for k, col in zip([1, 3, 10], [S.ORANGE, S.BLUE, S.AQUA]):
        ax.plot(xs, stats.t.pdf(xs, k), color=col, label=f"$t$ 分布（自由度 {k}）")
    ax.legend(fontsize=9)
    ax.set_title("$t$ 分布は正規分布より裾が重い", fontsize=11)
    S.only_x_axis(ax)
    ax = axes[1]
    xs2 = np.linspace(1.5, 5, 300)
    ax.plot(xs2, stats.norm.pdf(xs2), color=S.INK2, lw=2, ls=(0, (4, 3)))
    for k, col in zip([1, 3, 10], [S.ORANGE, S.BLUE, S.AQUA]):
        ax.plot(xs2, stats.t.pdf(xs2, k), color=col)
    ax.set_title("裾の拡大図", fontsize=11)
    ax.set_xlim(1.5, 5)
    ax.set_ylim(0, 0.14)
    fig.tight_layout()
    S.save(fig, CH, "t_vs_normal")


def f_shapes():
    xs = np.linspace(0.01, 4, 500)
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    for (m, n), col in zip([(1, 10), (5, 10), (10, 30), (30, 30)], [S.VIOLET, S.BLUE, S.ORANGE, S.AQUA]):
        ax.plot(xs, stats.f.pdf(xs, m, n), color=col, label=f"$F({m}, {n})$")
    ax.set_ylim(0, 1.6)
    ax.legend()
    ax.set_title("$F$ 分布：分散の比の分布", fontsize=11)
    S.only_x_axis(ax)
    S.save(fig, CH, "f_shapes")


def t_sim():
    rng = np.random.default_rng(21)
    n = 4
    x = rng.normal(50, 10, (200000, n))
    xbar = x.mean(1)
    s = x.std(1, ddof=1)
    chi = (n - 1) * s**2 / 100
    t = (xbar - 50) / (s / np.sqrt(n))
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.6))
    ax = axes[0]
    ax.hist(chi, bins=np.linspace(0, 15, 61), density=True, color=S.BLUE, edgecolor=S.SURFACE, lw=0.5,
            label=r"$(n-1)S^2/\sigma^2$")
    xs = np.linspace(0.01, 15, 300)
    ax.plot(xs, stats.chi2.pdf(xs, n - 1), color=S.ORANGE, label=f"$\\chi^2({n-1})$")
    ax.legend()
    ax.set_title(f"標本分散の分布（$n = {n}$）", fontsize=11)
    ax.set_yticks([])
    ax.grid(False)
    ax = axes[1]
    ax.hist(t, bins=np.linspace(-6, 6, 97), density=True, color=S.BLUE, edgecolor=S.SURFACE, lw=0.5,
            label=r"$(\bar{X}-\mu)/(S/\sqrt{n})$")
    xs = np.linspace(-6, 6, 400)
    ax.plot(xs, stats.t.pdf(xs, n - 1), color=S.ORANGE, label=f"$t({n-1})$")
    ax.plot(xs, stats.norm.pdf(xs), color=S.INK2, lw=1.5, ls=(0, (4, 3)), label="$N(0, 1)$")
    ax.legend(fontsize=9)
    ax.set_title("σ を S で置き換えると正規分布より裾が重くなる", fontsize=11)
    ax.set_yticks([])
    ax.grid(False)
    fig.tight_layout()
    S.save(fig, CH, "t_sim")


def main():
    sampling_concept()
    unbiased_sim()
    chi2_shapes()
    t_vs_normal()
    f_shapes()
    t_sim()
