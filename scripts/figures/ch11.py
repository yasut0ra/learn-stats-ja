"""第11章 大数の法則"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

import style as S

CH = "ch11"


def dice_running_mean():
    rng = np.random.default_rng(2)
    n = 3000
    k = np.arange(1, n + 1)
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    sd = np.sqrt(35 / 12)
    kk = k[S.log_idx(n, 300)]
    ax.fill_between(kk, 3.5 - 2 * sd / np.sqrt(kk), 3.5 + 2 * sd / np.sqrt(kk), color=S.BLUE, alpha=0.08, lw=0,
                    label=r"$3.5 \pm 2\sigma/\sqrt{n}$")
    for col in [S.BLUE, S.ORANGE, S.AQUA, S.VIOLET]:
        x = rng.integers(1, 7, n)
        i = S.log_idx(n)
        ax.plot(k[i], (np.cumsum(x) / k)[i], color=col, lw=1.5)
    ax.axhline(3.5, color=S.INK2, lw=1.2, ls=(0, (4, 3)))
    ax.set_xscale("log")
    ax.set_xlim(1, n)
    ax.set_ylim(1, 6)
    ax.set_xlabel("サイコロを振った回数 $n$（対数目盛り）")
    ax.set_ylabel(r"出た目の平均 $\bar{X}_n$")
    ax.text(n * 0.9, 3.62, "期待値 3.5", ha="right", fontsize=10, color=S.INK2)
    ax.legend(loc="upper right")
    S.save(fig, CH, "dice_running_mean")


def concentration():
    rng = np.random.default_rng(5)
    eps = 0.3
    fig, axes = plt.subplots(1, 4, figsize=(12, 2.9), sharey=True)
    for ax, n in zip(axes, [1, 5, 25, 100]):
        means = rng.integers(1, 7, (40000, n)).mean(1)
        inside = np.mean(np.abs(means - 3.5) < eps)
        bins = np.arange(0.95, 6.1, 0.1) if n > 1 else np.arange(0.5, 6.6, 1)
        ax.hist(means, bins=bins, density=True, color=S.BLUE, edgecolor=S.SURFACE, lw=0.5)
        ax.axvspan(3.5 - eps, 3.5 + eps, color=S.ORANGE, alpha=0.15, lw=0)
        ax.set_title(f"$n = {n}$：±{eps} 以内に {inside*100:.0f}%", fontsize=10.5)
        ax.set_xlim(0.8, 6.2)
        ax.grid(axis="x", visible=False)
        ax.set_yticks([])
    fig.tight_layout()
    S.save(fig, CH, "concentration")


def gambler():
    rng = np.random.default_rng(14)
    n = 20000
    k = np.arange(1, n + 1)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.6))
    for col in [S.BLUE, S.ORANGE, S.AQUA]:
        x = rng.random(n) < 0.5
        h = np.cumsum(x)
        i, j = S.log_idx(n), S.lin_idx(n)
        axes[0].plot(k[i], (h / k)[i], color=col, lw=1.4)
        axes[1].plot(k[j], (2 * h - k)[j], color=col, lw=1.4)
    axes[0].axhline(0.5, color=S.INK2, lw=1.1, ls=(0, (4, 3)))
    axes[0].set_xscale("log")
    axes[0].set_ylim(0.2, 0.8)
    axes[0].set_title("表の「割合」は 1/2 に近づく", fontsize=11)
    axes[0].set_xlabel("投げた回数（対数目盛り）")
    axes[1].axhline(0, color=S.INK2, lw=1.1, ls=(0, (4, 3)))
    axes[1].plot(k, 2 * np.sqrt(k), color=S.MUTED, lw=1, ls=(0, (2, 2)))
    axes[1].plot(k, -2 * np.sqrt(k), color=S.MUTED, lw=1, ls=(0, (2, 2)))
    axes[1].text(n * 0.98, 2 * np.sqrt(n) + 15, r"$\pm 2\sqrt{n}$", ha="right", fontsize=10, color=S.INK2)
    axes[1].set_title("表と裏の「回数の差」は 0 に戻らず広がる", fontsize=11)
    axes[1].set_xlabel("投げた回数")
    fig.tight_layout()
    S.save(fig, CH, "gambler")


def cauchy():
    rng = np.random.default_rng(7)
    n = 10000
    k = np.arange(1, n + 1)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.4))
    xs = np.linspace(-6, 6, 400)
    axes[0].plot(xs, stats.norm.pdf(xs), color=S.MUTED, label="標準正規分布")
    axes[0].plot(xs, stats.cauchy.pdf(xs), color=S.ORANGE, label="コーシー分布")
    axes[0].legend()
    axes[0].set_title("形は似ているが、コーシー分布は裾がとても重い", fontsize=11)
    S.only_x_axis(axes[0])
    for col in [S.ORANGE, S.RED, S.MAGENTA]:
        x = rng.standard_cauchy(n)
        i = S.log_idx(n, 1500)
        axes[1].plot(k[i], (np.cumsum(x) / k)[i], color=col, lw=1.3)
    x = rng.standard_normal(n)
    i = S.log_idx(n)
    axes[1].plot(k[i], (np.cumsum(x) / k)[i], color=S.BLUE, lw=1.6, label="正規分布の標本平均")
    axes[1].axhline(0, color=S.INK2, lw=1, ls=(0, (4, 3)))
    axes[1].set_xscale("log")
    axes[1].set_ylim(-6, 6)
    axes[1].set_title("コーシー分布の標本平均はいつまでも落ち着かない", fontsize=11)
    axes[1].set_xlabel("$n$（対数目盛り）")
    axes[1].legend(loc="lower left", fontsize=9)
    fig.tight_layout()
    S.save(fig, CH, "cauchy")


def monte_carlo_pi():
    rng = np.random.default_rng(3)
    n = 2000
    x, y = rng.random(n), rng.random(n)
    inside = x**2 + y**2 <= 1
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.2), gridspec_kw={"width_ratios": [1, 1.4]})
    ax = axes[0]
    ax.scatter(x[inside], y[inside], s=5, color=S.BLUE, lw=0, rasterized=True)
    ax.scatter(x[~inside], y[~inside], s=5, color=S.ORANGE, lw=0, rasterized=True)
    t = np.linspace(0, np.pi / 2, 200)
    ax.plot(np.cos(t), np.sin(t), color=S.INK2, lw=1.4)
    ax.set_aspect("equal")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(f"円の内側の割合 × 4 = {4*inside.mean():.3f}", fontsize=11)
    ax.grid(False)
    ax = axes[1]
    big = 100000
    for col in [S.BLUE, S.ORANGE, S.AQUA]:
        u, v = rng.random(big), rng.random(big)
        est = 4 * np.cumsum(u**2 + v**2 <= 1) / np.arange(1, big + 1)
        i = S.log_idx(big)
        ax.plot(np.arange(1, big + 1)[i], est[i], color=col, lw=1.3)
    ax.axhline(np.pi, color=S.INK2, lw=1.1, ls=(0, (4, 3)))
    ax.text(big * 0.9, np.pi + 0.05, r"$\pi = 3.14159\ldots$", ha="right", fontsize=10, color=S.INK2)
    ax.set_xscale("log")
    ax.set_ylim(2.6, 3.7)
    ax.set_xlabel("点の数（対数目盛り）")
    ax.set_title("点を増やすと推定値は π に近づく", fontsize=11)
    fig.tight_layout()
    S.save(fig, CH, "monte_carlo_pi")


def main():
    dice_running_mean()
    concentration()
    gambler()
    cauchy()
    monte_carlo_pi()
