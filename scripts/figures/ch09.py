"""第9章 多次元の確率分布"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from scipy import stats

import style as S

CH = "ch09"

JOINT = np.array([[1, 1, 0], [1, 2, 1], [0, 1, 1]]) / 8  # 行: X=0,1,2  列: Y=0,1,2


def joint_table():
    fig = plt.figure(figsize=(6.4, 5.4))
    gs = GridSpec(2, 2, width_ratios=[3, 1.1], height_ratios=[1.1, 3], hspace=0.08, wspace=0.08)
    ax = fig.add_subplot(gs[1, 0])
    top = fig.add_subplot(gs[0, 0], sharex=ax)
    right = fig.add_subplot(gs[1, 1], sharey=ax)
    for i in range(3):
        for j in range(3):
            p = JOINT[i, j]
            if p > 0:
                ax.scatter(i, j, s=p * 8 * 900, color=S.BLUE, alpha=0.85, edgecolor=S.SURFACE, lw=2)
            ax.text(i, j, f"{int(p*8)}/8", ha="center", va="center", fontsize=11,
                    color="white" if p > 0 else S.MUTED)
    ax.set_xlim(-0.6, 2.6)
    ax.set_ylim(-0.6, 2.6)
    ax.set_xticks([0, 1, 2])
    ax.set_yticks([0, 1, 2])
    ax.set_xlabel("$X$ = 1・2回目の表の数")
    ax.set_ylabel("$Y$ = 2・3回目の表の数")
    ax.grid(False)
    px, py = JOINT.sum(1), JOINT.sum(0)
    top.bar([0, 1, 2], px, width=0.45, color=S.ORANGE)
    for i, v in enumerate(px):
        top.text(i, v + 0.02, f"{int(v*8)}/8", ha="center", fontsize=10, color=S.INK2)
    top.set_ylim(0, 0.68)
    top.set_yticks([])
    top.spines["left"].set_visible(False)
    top.grid(False)
    plt.setp(top.get_xticklabels(), visible=False)
    top.set_title("$X$ の周辺分布（縦に足す）", fontsize=10, loc="left")
    right.barh([0, 1, 2], py, height=0.45, color=S.ORANGE)
    for j, v in enumerate(py):
        right.text(v + 0.02, j, f"{int(v*8)}/8", va="center", fontsize=10, color=S.INK2)
    right.set_xlim(0, 0.75)
    right.set_xticks([])
    right.spines["bottom"].set_visible(False)
    right.grid(False)
    plt.setp(right.get_yticklabels(), visible=False)
    right.set_title("$Y$ の周辺分布", fontsize=10, loc="left")
    S.save(fig, CH, "joint_table")


def bivariate_surface():
    rho = 0.6
    xs = np.linspace(-3, 3, 70)
    X, Y = np.meshgrid(xs, xs)
    rv = stats.multivariate_normal([0, 0], [[1, rho], [rho, 1]])
    Z = rv.pdf(np.dstack([X, Y]))
    fig = plt.figure(figsize=(10.4, 4.2))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="Blues", linewidth=0, antialiased=True, rstride=2, cstride=2, alpha=0.95,
                    rasterized=True)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zticks([])
    ax.view_init(elev=28, azim=-60)
    ax.set_title("同時密度関数 $f(x, y)$：体積が確率", fontsize=11)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.contourf(X, Y, Z, levels=10, cmap="Blues", rasterized=True)
    ax2.contour(X, Y, Z, levels=10, colors=S.SURFACE, linewidths=0.6)
    ax2.set_aspect("equal")
    ax2.set_xlabel("$x$")
    ax2.set_ylabel("$y$")
    ax2.set_title("真上から見た等高線", fontsize=11)
    ax2.grid(False)
    fig.tight_layout()
    S.save(fig, CH, "bivariate_surface")


def conditional_slices():
    rho = 0.7
    xs = np.linspace(-3, 3, 200)
    X, Y = np.meshgrid(xs, xs)
    rv = stats.multivariate_normal([0, 0], [[1, rho], [rho, 1]])
    Z = rv.pdf(np.dstack([X, Y]))
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    ax.contour(X, Y, Z, levels=8, colors=S.AXIS, linewidths=0.9)
    for x0, col in [(-1.5, S.BLUE), (0.0, S.ORANGE), (1.5, S.AQUA)]:
        m, s = rho * x0, np.sqrt(1 - rho**2)
        ys = np.linspace(-3, 3, 300)
        dens = stats.norm.pdf(ys, m, s)
        ax.axvline(x0, color=col, lw=1, ls=(0, (3, 2)))
        ax.fill_betweenx(ys, x0, x0 + dens * 0.9, color=col, alpha=0.25, lw=0)
        ax.plot(x0 + dens * 0.9, ys, color=col, lw=2)
        ax.scatter([x0], [m], s=40, color=col, edgecolor=S.SURFACE, lw=1.5, zorder=4)
    ax.plot(xs, rho * xs, color=S.INK2, lw=1.4, label=r"$E[Y \mid X = x] = \rho x$")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend(loc="upper left")
    ax.set_title(r"$X = x$ で切った切り口が条件付き分布（$\rho = 0.7$）", fontsize=11)
    ax.grid(False)
    S.save(fig, CH, "conditional_slices")


def rho_panels():
    rng = np.random.default_rng(9)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.7))
    xs = np.linspace(-3, 3, 150)
    X, Y = np.meshgrid(xs, xs)
    for ax, rho in zip(axes, [-0.7, 0.0, 0.7]):
        cov = [[1, rho], [rho, 1]]
        Z = stats.multivariate_normal([0, 0], cov).pdf(np.dstack([X, Y]))
        pts = rng.multivariate_normal([0, 0], cov, 300)
        ax.scatter(pts[:, 0], pts[:, 1], s=7, color=S.BLUE, alpha=0.45, lw=0)
        ax.contour(X, Y, Z, levels=5, colors=S.INK2, linewidths=1)
        ax.set_aspect("equal")
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_title(f"$\\rho = {rho}$", fontsize=11)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    S.save(fig, CH, "rho_panels")


def diversification():
    n = np.arange(1, 31)
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    for rho, col in [(0.0, S.BLUE), (0.3, S.ORANGE), (0.6, S.AQUA)]:
        v = rho + (1 - rho) / n
        ax.plot(n, np.sqrt(v), color=col, marker="o", ms=4, mec=S.SURFACE, mew=1, label=f"相関 $\\rho = {rho}$")
        ax.axhline(np.sqrt(rho), color=col, lw=0.8, ls=(0, (3, 2)))
    ax.set_xlabel("組み合わせる銘柄の数 $n$")
    ax.set_ylabel("平均の標準偏差 ÷ $\\sigma$")
    ax.set_ylim(0, 1.05)
    ax.set_xlim(0.5, 30.5)
    ax.legend()
    ax.set_title(r"分散投資の効果：$\sqrt{\rho + (1-\rho)/n}$ まで下がる", fontsize=11)
    S.save(fig, CH, "diversification")


def main():
    joint_table()
    bivariate_surface()
    conditional_slices()
    rho_panels()
    diversification()
