"""第16章 仮説検定の考え方"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

import style as S

CH = "ch16"


def pvalue_coin():
    x = np.arange(30, 71)
    p = stats.binom.pmf(x, 100, 0.5)
    extreme = (x >= 60) | (x <= 40)
    fig, ax = plt.subplots(figsize=(8.4, 3.6))
    ax.bar(x, p, width=0.75, color=[S.ORANGE if e else S.BLUE for e in extreme])
    pv = 2 * stats.binom.sf(59, 100, 0.5)
    ax.annotate("観測値 60", xy=(60, p[x == 60][0]), xytext=(63, 0.06), fontsize=10.5,
                arrowprops=dict(arrowstyle="-|>", color=S.MUTED, lw=1))
    ax.text(66.5, 0.025, f"橙の部分の合計\n＝ p 値 {pv:.3f}", fontsize=10.5, color=S.INK, ha="center")
    ax.text(33.5, 0.025, "反対側も\n同じだけ極端", fontsize=10, color=S.INK2, ha="center")
    ax.set_xlabel("100回中の表の回数")
    ax.set_ylabel("確率（公正なコインの場合）")
    ax.set_title("帰無仮説「公正なコイン」のもとでの表の回数の分布 $B(100, 0.5)$", fontsize=11)
    ax.grid(axis="x", visible=False)
    S.save(fig, CH, "pvalue_coin")


def rejection_region():
    xs = np.linspace(-4, 4, 600)
    y = stats.norm.pdf(xs)
    z_obs = 2.25
    fig, ax = plt.subplots(figsize=(8.4, 3.6))
    ax.plot(xs, y, color=S.BLUE)
    for m in [xs >= 1.96, xs <= -1.96]:
        ax.fill_between(xs[m], y[m], color=S.ORANGE, alpha=0.35, lw=0)
    for m in [xs >= z_obs, xs <= -z_obs]:
        ax.fill_between(xs[m], y[m], color=S.RED, alpha=0.55, lw=0, hatch="////", edgecolor=S.SURFACE)
    ax.axvline(z_obs, color=S.INK, lw=1.6)
    ax.text(z_obs + 0.08, 0.3, f"観測された\n$z$ = {z_obs}", fontsize=10.5, color=S.INK)
    ax.text(2.9, 0.075, "棄却域\n（面積 2.5%）", fontsize=10, color=S.INK2, ha="center")
    ax.text(-2.9, 0.075, "棄却域\n（面積 2.5%）", fontsize=10, color=S.INK2, ha="center")
    ax.text(0, 0.15, "採択域\n（95%）", fontsize=10.5, color=S.INK, ha="center")
    ax.set_xticks([-1.96, 0, 1.96, z_obs])
    ax.set_xticklabels(["−1.96", "0", "1.96", ""])
    ax.set_title(r"有意水準 5% の両側検定：$|z| \geq 1.96$ なら棄却。$p$ 値は斜線部 = 0.024", fontsize=11)
    S.only_x_axis(ax)
    S.save(fig, CH, "rejection_region")


def errors():
    xs = np.linspace(-4, 7, 700)
    d = 2.5
    c = 1.645
    h0, h1 = stats.norm.pdf(xs), stats.norm.pdf(xs, d, 1)
    fig, ax = plt.subplots(figsize=(8.8, 3.8))
    ax.plot(xs, h0, color=S.MUTED, lw=2, label="$H_0$ が正しいときの検定統計量の分布")
    ax.plot(xs, h1, color=S.BLUE, lw=2, label="$H_1$ が正しいときの検定統計量の分布")
    m = xs >= c
    ax.fill_between(xs[m], h0[m], color=S.ORANGE, alpha=0.5, lw=0)
    m2 = xs < c
    ax.fill_between(xs[m2], h1[m2], color=S.VIOLET, alpha=0.3, lw=0)
    ax.fill_between(xs[m], h1[m], color=S.BLUE, alpha=0.15, lw=0)
    ax.axvline(c, color=S.INK, lw=1.4)
    ax.text(c + 0.05, 0.43, "← 採択 ｜ 棄却 →", fontsize=10.5, color=S.INK, ha="center")
    ax.annotate(r"$\alpha$：第1種の過誤", xy=(2.0, 0.03), xytext=(3.7, 0.12), fontsize=10.5, color=S.INK,
                arrowprops=dict(arrowstyle="-|>", color=S.MUTED, lw=1))
    ax.annotate(r"$\beta$：第2種の過誤", xy=(1.2, 0.07), xytext=(-2.6, 0.2), fontsize=10.5, color=S.INK,
                arrowprops=dict(arrowstyle="-|>", color=S.MUTED, lw=1))
    ax.text(3.6, 0.3, r"検出力 $1 - \beta$", fontsize=10.5, color=S.INK)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_ylim(0, 0.5)
    S.only_x_axis(ax)
    ax.set_xlabel("検定統計量")
    S.save(fig, CH, "errors")


def power_curve():
    mu0, sigma = 20.0, 0.4
    mus = np.linspace(19.5, 20.5, 400)
    fig, ax = plt.subplots(figsize=(8, 3.8))
    for n, col in [(10, S.AQUA), (25, S.BLUE), (50, S.ORANGE)]:
        d = (mus - mu0) / (sigma / np.sqrt(n))
        pw = stats.norm.sf(1.96 - d) + stats.norm.cdf(-1.96 - d)
        ax.plot(mus, pw, color=col, label=f"$n = {n}$")
    ax.axhline(0.05, color=S.INK2, lw=1, ls=(0, (3, 2)))
    ax.text(19.52, 0.08, r"$\mu = \mu_0$ では検出力 = $\alpha$ = 0.05", fontsize=9.5, color=S.INK2)
    ax.axvline(mu0, color=S.MUTED, lw=0.8)
    ax.set_xlabel(r"真の母平均 $\mu$（$H_0: \mu = 20.0$）")
    ax.set_ylabel("検出力（$H_0$ を棄却する確率）")
    ax.set_ylim(0, 1.03)
    ax.legend(loc="center right")
    ax.set_title("検出力関数：真の値が $\\mu_0$ から離れるほど、$n$ が大きいほど検出しやすい", fontsize=11)
    S.save(fig, CH, "power_curve")


def multiple_testing():
    m = np.arange(1, 61)
    fig, ax = plt.subplots(figsize=(7.4, 3.5))
    ax.plot(m, 1 - 0.95**m, color=S.BLUE, marker="o", ms=3.5, mec=S.SURFACE, mew=0.8)
    for k in [1, 14, 20, 60]:
        v = 1 - 0.95**k
        ax.text(k + 1, v - 0.07, f"{k}回で {v*100:.0f}%", fontsize=10, color=S.INK)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("独立な検定の回数 $m$（すべて帰無仮説が正しい）")
    ax.set_ylabel("少なくとも1回は\n誤って有意になる確率")
    ax.set_title("有意水準 5% の検定をくり返すと、偽の発見が避けられなくなる", fontsize=11)
    S.save(fig, CH, "multiple_testing")


def pvalue_distribution():
    rng = np.random.default_rng(16)
    n = 20
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.3), sharey=True)
    for ax, (mu, title) in zip(axes, [(0.0, "$H_0$ が正しいとき：一様分布"), (0.5, "$H_1$ が正しいとき（効果量 0.5）：0付近に集中")]):
        x = rng.normal(mu, 1, (20000, n))
        t = x.mean(1) / (x.std(1, ddof=1) / np.sqrt(n))
        p = 2 * stats.t.sf(np.abs(t), n - 1)
        ax.hist(p, bins=np.linspace(0, 1, 21), density=True, color=S.BLUE, edgecolor=S.SURFACE, lw=1)
        ax.axvline(0.05, color=S.ORANGE, lw=1.4, ls=(0, (3, 2)))
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("$p$ 値")
        ax.grid(axis="x", visible=False)
        ax.text(0.06, 0.92, f"p < 0.05 の割合 {np.mean(p < 0.05)*100:.1f}%", transform=ax.transAxes, fontsize=10,
                color=S.INK)
    fig.tight_layout()
    S.save(fig, CH, "pvalue_distribution")


def main():
    pvalue_coin()
    rejection_region()
    errors()
    power_curve()
    multiple_testing()
    pvalue_distribution()
