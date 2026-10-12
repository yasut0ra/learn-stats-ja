"""第12章 中心極限定理"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

import style as S

CH = "ch12"


def clt_grid():
    rng = np.random.default_rng(12)
    parents = [
        ("一様分布", lambda size: rng.random(size), 0.5, np.sqrt(1 / 12)),
        ("指数分布", lambda size: rng.exponential(1.0, size), 1.0, 1.0),
        ("ベルヌーイ分布 p=0.2", lambda size: (rng.random(size) < 0.2).astype(float), 0.2, 0.4),
    ]
    ns = [1, 2, 5, 30]
    fig, axes = plt.subplots(3, 4, figsize=(12, 6.6))
    zs = np.linspace(-4, 4, 300)
    for i, (name, draw, mu, sd) in enumerate(parents):
        for j, n in enumerate(ns):
            ax = axes[i, j]
            m = draw((30000, n)).mean(1)
            z = (m - mu) / (sd / np.sqrt(n))
            if "ベルヌーイ" in name:
                vals = np.unique(np.round(z, 8))
                width = np.min(np.diff(vals)) if len(vals) > 1 else 1
                bins = np.concatenate([vals - width / 2, [vals[-1] + width / 2]])
                bins = bins[(bins > -4.6) & (bins < 4.6)] if n > 2 else bins
            else:
                bins = np.linspace(-4, 4, 41)
            ax.hist(z, bins=bins, density=True, color=S.BLUE, edgecolor=S.SURFACE, lw=0.5)
            ax.plot(zs, stats.norm.pdf(zs), color=S.ORANGE, lw=1.6)
            ax.set_xlim(-4, 4)
            ax.set_ylim(0, 1.05)
            ax.set_yticks([])
            ax.set_xticks([-2, 0, 2])
            ax.grid(False)
            if i == 0:
                ax.set_title(f"$n = {n}$", fontsize=12)
            if j == 0:
                ax.set_ylabel(name, fontsize=10.5)
    fig.suptitle("標準化した標本平均の分布（青）と標準正規分布（橙）", fontsize=12, y=1.0)
    fig.tight_layout()
    S.save(fig, CH, "clt_grid")


def binom_normal_approx():
    n, p = 100, 0.5
    mu, sd = n * p, np.sqrt(n * p * (1 - p))
    x = np.arange(35, 66)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.6))
    ax = axes[0]
    ax.bar(x, stats.binom.pmf(x, n, p), width=0.8, color=S.BLUE, label="$B(100, 0.5)$")
    xs = np.linspace(35, 65, 400)
    ax.plot(xs, stats.norm.pdf(xs, mu, sd), color=S.ORANGE, lw=2, label="$N(50, 5^2)$")
    ax.legend(loc="upper left")
    ax.set_title("二項分布と正規分布はほぼ重なる", fontsize=11)
    ax.grid(axis="x", visible=False)
    ax = axes[1]
    x2 = np.arange(54, 67)
    ax.bar(x2, stats.binom.pmf(x2, n, p), width=1.0, color=[S.BLUE if v >= 60 else S.AXIS for v in x2],
           edgecolor=S.SURFACE, lw=1.5)
    xs = np.linspace(54, 66, 300)
    ax.plot(xs, stats.norm.pdf(xs, mu, sd), color=S.ORANGE, lw=2)
    m = xs >= 59.5
    ax.fill_between(xs[m], stats.norm.pdf(xs[m], mu, sd), color=S.ORANGE, alpha=0.25, lw=0)
    ax.axvline(59.5, color=S.INK2, lw=1.2, ls=(0, (3, 2)))
    ax.axvline(60, color=S.MUTED, lw=1, ls=(0, (1, 2)))
    ax.text(59.3, 0.045, "59.5 から\n積分する", ha="right", fontsize=10, color=S.INK)
    ax.set_title("連続修正：棒 $x = 60$ は区間 [59.5, 60.5] を占める", fontsize=11)
    ax.set_xticks(range(54, 67, 2))
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    S.save(fig, CH, "binom_normal_approx")


def galton_board():
    rng = np.random.default_rng(8)
    rows = 12
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 6.4), gridspec_kw={"height_ratios": [1.3, 1]}, sharex=True)
    ax = axes[0]
    for r in range(rows):
        xs = np.arange(-r, r + 1, 2) / 2
        ax.scatter(xs, np.full_like(xs, -r, dtype=float), s=14, color=S.INK2, zorder=3)
    # 1個の球の軌跡
    pos = 0.0
    path_x, path_y = [0.0], [0.6]
    for r in range(rows):
        path_x.append(pos)
        path_y.append(-r)
        pos += 0.5 if rng.random() < 0.5 else -0.5
    path_x.append(pos)
    path_y.append(-rows - 0.4)
    ax.plot(path_x, path_y, color=S.ORANGE, lw=2, zorder=2)
    ax.scatter([0], [0.8], s=80, color=S.ORANGE, zorder=4)
    ax.text(3.4, -1.5, "釘に当たるたびに\n左右に 1/2 ずつ\n（独立な ±1/2 の和）", fontsize=10, color=S.INK2)
    ax.set_ylim(-rows - 0.6, 1.4)
    ax.axis("off")
    ax2 = axes[1]
    steps = rng.choice([-0.5, 0.5], size=(20000, rows)).sum(1)
    vals, cnt = np.unique(steps, return_counts=True)
    ax2.bar(vals, cnt / cnt.sum(), width=0.42, color=S.BLUE)
    xs = np.linspace(-6.5, 6.5, 300)
    ax2.plot(xs, stats.norm.pdf(xs, 0, np.sqrt(rows) / 2), color=S.ORANGE, lw=2)
    ax2.set_yticks([])
    ax2.grid(False)
    ax2.set_xlabel("球が落ちた位置（20000個）")
    ax2.set_xlim(-6.8, 6.8)
    S.save(fig, CH, "galton_board")


def delta_method():
    lam = 1.0
    mu = 1 / lam
    n = 40
    se = (1 / lam) / np.sqrt(n)
    g = lambda x: 1 / x  # noqa: E731
    xs = np.linspace(0.55, 1.6, 300)
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.plot(xs, g(xs), color=S.INK2, lw=2, label=r"$g(x) = 1/x$")
    ax.plot(xs, g(mu) - (xs - mu) / mu**2, color=S.ORANGE, lw=1.6, ls=(0, (5, 3)),
            label=r"$\mu$ での接線（傾き $g'(\mu)$）")
    dens = stats.norm.pdf(xs, mu, se)
    ax.fill_between(xs, 0.3, 0.3 + dens * 0.12, color=S.BLUE, alpha=0.25, lw=0)
    ax.plot(xs, 0.3 + dens * 0.12, color=S.BLUE, lw=1.5)
    ys = np.linspace(0.4, 1.8, 300)
    dy = stats.norm.pdf(ys, g(mu), se * abs(-1 / mu**2))
    ax.fill_betweenx(ys, 0.55, 0.55 + dy * 0.05, color=S.AQUA, alpha=0.25, lw=0)
    ax.plot(0.55 + dy * 0.05, ys, color=S.AQUA, lw=1.5)
    ax.scatter([mu], [g(mu)], s=50, color=S.INK, zorder=4)
    ax.text(1.12, 0.42, r"$\bar{X}$ の分布 $\approx N(\mu, \sigma^2/n)$", fontsize=10.5, color=S.INK)
    ax.annotate(r"$g(\bar{X})$ の分布 $\approx N(g(\mu),\ g'(\mu)^2\sigma^2/n)$", xy=(0.66, 1.2), xytext=(0.98, 1.45),
                fontsize=10.5, color=S.INK, arrowprops=dict(arrowstyle="-|>", color=S.MUTED, lw=1))
    ax.set_xlim(0.55, 1.6)
    ax.set_ylim(0.3, 1.85)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$g(x)$")
    ax.legend(loc="upper right")
    S.save(fig, CH, "delta_method")


def main():
    clt_grid()
    binom_normal_approx()
    galton_board()
    delta_method()
