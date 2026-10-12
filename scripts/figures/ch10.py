"""第10章 確率変数の変換"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from scipy import stats

import style as S

CH = "ch10"


def transform_intuition():
    # X ~ N(0.6, 0.45^2),  Y = e^X （単調増加）
    mu, sd = 0.6, 0.45
    g = np.exp
    xs = np.linspace(-0.6, 2.0, 400)
    ys = g(xs)
    fx = stats.norm.pdf(xs, mu, sd)
    yy = np.linspace(g(-0.6), g(2.0), 400)
    fy = stats.lognorm.pdf(yy, s=sd, scale=np.exp(mu))

    fig = plt.figure(figsize=(7.6, 6.4))
    gs = GridSpec(2, 2, width_ratios=[1, 3.2], height_ratios=[3.2, 1], hspace=0.05, wspace=0.05)
    ax = fig.add_subplot(gs[0, 1])
    axl = fig.add_subplot(gs[0, 0], sharey=ax)
    axb = fig.add_subplot(gs[1, 1], sharex=ax)

    ax.plot(xs, ys, color=S.INK2, lw=2)
    for x0, dx, col in [(0.1, 0.12, S.BLUE), (1.3, 0.12, S.ORANGE)]:
        y0, y1 = g(x0), g(x0 + dx)
        ax.axvspan(x0, x0 + dx, color=col, alpha=0.15, lw=0)
        ax.axhspan(y0, y1, color=col, alpha=0.15, lw=0)
        m = (xs >= x0) & (xs <= x0 + dx)
        axb.fill_between(xs[m], fx[m], color=col, alpha=0.6, lw=0)
        m2 = (yy >= y0) & (yy <= y1)
        axl.fill_betweenx(yy[m2], fy[m2], color=col, alpha=0.6, lw=0)
    ax.text(1.5, 2.5, r"$y = g(x) = e^x$", fontsize=12, color=S.INK)
    ax.text(0.28, 7.1, "同じ色の帯は同じ確率\n傾きが急な所では\n$y$ の幅が広がり\n密度が低くなる",
            fontsize=9.5, color=S.INK2, va="top")
    ax.set_xlim(-0.6, 2.0)
    ax.set_ylim(0.4, 7.4)
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)

    axb.plot(xs, fx, color=S.BLUE)
    axb.set_yticks([])
    axb.spines["left"].set_visible(False)
    axb.grid(False)
    axb.set_xlabel("$x$　（$X$ の密度 $f_X$）")

    axl.plot(fy, yy, color=S.BLUE)
    axl.invert_xaxis()
    axl.set_xticks([])
    axl.spines["bottom"].set_visible(False)
    axl.grid(False)
    axl.set_ylabel("$y$　（$Y$ の密度 $f_Y$）")
    S.save(fig, CH, "transform_intuition")


def chi2_from_normal():
    rng = np.random.default_rng(1)
    z = rng.standard_normal(50000)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.3))
    ax = axes[0]
    ax.hist(z, bins=np.linspace(-4, 4, 61), density=True, color=S.BLUE, edgecolor=S.SURFACE, lw=0.6)
    xs = np.linspace(-4, 4, 300)
    ax.plot(xs, stats.norm.pdf(xs), color=S.ORANGE)
    ax.set_title("$X \\sim N(0, 1)$", fontsize=11)
    ax.grid(axis="x", visible=False)
    ax = axes[1]
    ax.hist(z**2, bins=np.linspace(0, 6, 61), density=True, color=S.BLUE, edgecolor=S.SURFACE, lw=0.6,
            label="$X^2$ のヒストグラム")
    ys = np.linspace(0.02, 6, 300)
    ax.plot(ys, stats.chi2.pdf(ys, 1), color=S.ORANGE, label=r"$\frac{1}{\sqrt{2\pi y}}e^{-y/2}$")
    ax.set_ylim(0, 1.6)
    ax.set_title("$Y = X^2$：0の近くに集中する", fontsize=11)
    ax.legend()
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    S.save(fig, CH, "chi2_from_normal")


def inverse_transform():
    rng = np.random.default_rng(3)
    lam = 1.0
    xs = np.linspace(0, 5, 300)
    F = 1 - np.exp(-lam * xs)
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.6))
    ax = axes[0]
    ax.plot(xs, F, color=S.BLUE)
    for u, col in [(0.25, S.ORANGE), (0.6, S.AQUA), (0.9, S.VIOLET)]:
        x = -np.log(1 - u) / lam
        ax.annotate("", xy=(x, u), xytext=(0, u), arrowprops=dict(arrowstyle="-|>", color=col, lw=1.4))
        ax.annotate("", xy=(x, 0), xytext=(x, u), arrowprops=dict(arrowstyle="-|>", color=col, lw=1.4))
        ax.text(-0.08, u, f"$u = {u}$", ha="right", va="center", fontsize=10, color=S.INK)
    ax.set_xlim(-0.05, 5)
    ax.set_ylim(0, 1.02)
    ax.set_yticks([])
    ax.set_title(r"$U \sim U(0,1)$ を $F^{-1}$ で横軸へ写す", fontsize=11)
    ax.set_xlabel(r"$x = F^{-1}(u) = -\log(1-u)$")
    ax = axes[1]
    u = rng.random(30000)
    x = -np.log(1 - u) / lam
    ax.hist(x, bins=np.linspace(0, 5, 51), density=True, color=S.BLUE, edgecolor=S.SURFACE, lw=0.6,
            label="変換した30000個の乱数")
    ax.plot(xs, lam * np.exp(-lam * xs), color=S.ORANGE, label=r"$Ex(1)$ の密度")
    ax.legend()
    ax.set_title("結果は指数分布に従う", fontsize=11)
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    S.save(fig, CH, "inverse_transform")


def convolution_uniform():
    xs = np.linspace(-0.2, 3.2, 600)
    f1 = ((xs >= 0) & (xs <= 1)).astype(float)
    f2 = np.clip(np.where(xs <= 1, xs, 2 - xs), 0, None)
    f3 = np.where(xs < 0, 0, np.where(xs < 1, xs**2 / 2, np.where(xs < 2, (-2 * xs**2 + 6 * xs - 3) / 2,
                                                                       np.where(xs <= 3, (3 - xs) ** 2 / 2, 0))))
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.1), sharey=True)
    for ax, f, title, n in [(axes[0], f1, "$U_1$：一様分布", 1), (axes[1], f2, "$U_1 + U_2$：三角形", 2),
                            (axes[2], f3, "$U_1 + U_2 + U_3$：もう釣り鐘型", 3)]:
        ax.fill_between(xs, f, color=S.BLUE, alpha=0.2, lw=0)
        ax.plot(xs, f, color=S.BLUE)
        if n == 3:
            ax.plot(xs, stats.norm.pdf(xs, 1.5, 0.5), color=S.ORANGE, lw=1.6, ls=(0, (4, 3)),
                    label="同じ平均・分散の正規分布")
            ax.legend(fontsize=9, loc="upper right")
        ax.set_title(title, fontsize=11)
        ax.set_ylim(0, 1.25)
        ax.grid(axis="x", visible=False)
    fig.tight_layout()
    S.save(fig, CH, "convolution_uniform")


def order_stats():
    xs = np.linspace(0, 1, 400)
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    for n, col in zip([1, 2, 5, 10], [S.BLUE, S.ORANGE, S.AQUA, S.VIOLET]):
        ax.plot(xs, n * xs ** (n - 1), color=col, label=f"$n = {n}$")
    ax.set_ylim(0, 10.5)
    ax.set_xlabel("$x$")
    ax.set_title("$U(0, 1)$ からの $n$ 個の標本の最大値の密度 $n x^{n-1}$", fontsize=11)
    ax.legend(loc="upper left")
    S.save(fig, CH, "order_stats")


def main():
    transform_intuition()
    chi2_from_normal()
    inverse_transform()
    convolution_uniform()
    order_stats()
