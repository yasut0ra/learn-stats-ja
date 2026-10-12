"""第15章 区間推定"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

import style as S

CH = "ch15"


def ci_mechanism():
    mu, se = 50.0, 2.0
    xs = np.linspace(mu - 4.2 * se, mu + 4.2 * se, 500)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.4, 5.4), sharex=True,
                                   gridspec_kw={"height_ratios": [1.2, 1.5], "hspace": 0.32})
    y = stats.norm.pdf(xs, mu, se)
    m = np.abs(xs - mu) <= 1.96 * se
    ax1.fill_between(xs[m], y[m], color=S.BLUE, alpha=0.2, lw=0)
    ax1.plot(xs, y, color=S.BLUE)
    ax1.axvline(mu, color=S.INK2, lw=1.2)
    for s_ in (-1, 1):
        ax1.axvline(mu + s_ * 1.96 * se, color=S.BLUE, lw=1, ls=(0, (3, 2)))
    ax1.text(mu, y.max() * 0.45, "95%", ha="center", fontsize=12, color=S.INK)
    ax1.text(mu + 1.96 * se + 0.2, y.max() * 0.8, r"$\mu + 1.96\,\sigma/\sqrt{n}$", fontsize=10, color=S.INK2)
    ax1.text(mu - 1.96 * se - 0.2, y.max() * 0.8, r"$\mu - 1.96\,\sigma/\sqrt{n}$", fontsize=10, color=S.INK2,
             ha="right")
    ax1.set_title(r"$\bar{X}$ の標本分布：95% の確率で $\mu \pm 1.96\,\sigma/\sqrt{n}$ に入る", fontsize=11)
    S.only_x_axis(ax1)

    xbars = [48.1, 52.6, 50.9, 54.6, 46.7, 49.2]
    for k, xb in enumerate(xbars):
        yk = len(xbars) - k
        ok = abs(xb - mu) <= 1.96 * se
        col = S.BLUE if ok else S.RED
        ax2.plot([xb - 1.96 * se, xb + 1.96 * se], [yk, yk], color=col, lw=2.6 if not ok else 2)
        ax2.scatter([xb], [yk], s=40, color=col, zorder=3)
        ax2.text(mu + 4.75 * se, yk, "μ を含む" if ok else "μ を含まない", va="center", fontsize=10,
                 color=S.INK if ok else S.RED)
    ax2.axvline(mu, color=S.INK2, lw=1.2)
    ax2.axvspan(mu - 1.96 * se, mu + 1.96 * se, color=S.BLUE, alpha=0.06, lw=0)
    ax2.set_ylim(0.3, len(xbars) + 0.7)
    ax2.set_yticks([])
    ax2.spines["left"].set_visible(False)
    ax2.grid(False)
    ax2.set_xlim(mu - 4.2 * se, mu + 7.4 * se)
    ax2.set_xticks([mu])
    ax2.set_xticklabels([r"真の値 $\mu$"])
    ax2.set_title(r"各標本の区間 $\bar{x} \pm 1.96\,\sigma/\sqrt{n}$：$\bar{x}$ が色の範囲内なら $\mu$ を含む", fontsize=11)
    S.save(fig, CH, "ci_mechanism")


def ci_hundred():
    rng = np.random.default_rng(15)
    mu, sigma, n = 50, 10, 10
    tq = stats.t.isf(0.025, n - 1)
    fig, ax = plt.subplots(figsize=(7.6, 7.2))
    miss = 0
    for k in range(100):
        x = rng.normal(mu, sigma, n)
        m, s = x.mean(), x.std(ddof=1)
        h = tq * s / np.sqrt(n)
        ok = m - h <= mu <= m + h
        miss += not ok
        ax.plot([m - h, m + h], [k, k], color=S.BLUE if ok else S.RED, lw=1.4 if ok else 2.4)
        ax.scatter([m], [k], s=6, color=S.BLUE if ok else S.RED, zorder=3)
    ax.axvline(mu, color=S.INK2, lw=1.4)
    ax.set_yticks([])
    ax.set_xlabel("値")
    ax.grid(axis="y", visible=False)
    ax.set_title(f"95% 信頼区間を100回つくると、μ を含まないもの（赤）は {miss} 本", fontsize=11)
    S.save(fig, CH, "ci_hundred")


def sample_size():
    E = np.linspace(0.01, 0.1, 300)
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    for z, lab, col in [(1.645, "信頼係数 90%", S.AQUA), (1.96, "信頼係数 95%", S.BLUE), (2.576, "信頼係数 99%", S.ORANGE)]:
        ax.plot(E * 100, (z / (2 * E)) ** 2, color=col, label=lab)
    for e in [0.03, 0.05]:
        n = (1.96 / (2 * e)) ** 2
        ax.scatter([e * 100], [n], s=40, color=S.BLUE, edgecolor=S.SURFACE, lw=1.5, zorder=3)
        ax.text(e * 100 + 0.2, n * 1.25, f"±{e*100:.0f}% → 約{int(np.ceil(n))}人", fontsize=10, color=S.INK)
    ax.set_yscale("log")
    ax.set_xlabel("許容する誤差 $E$（%ポイント）")
    ax.set_ylabel("必要な標本の大きさ $n$")
    ax.legend()
    ax.set_title("支持率調査に必要な人数（最悪の場合 $p = 1/2$）", fontsize=11)
    S.save(fig, CH, "sample_size")


def wald_coverage():
    n = 30
    z = 1.96
    ps = np.linspace(0.01, 0.99, 391)
    k = np.arange(n + 1)
    phat = k / n
    se = np.sqrt(phat * (1 - phat) / n)
    w_lo, w_hi = phat - z * se, phat + z * se
    center = (phat + z**2 / (2 * n)) / (1 + z**2 / n)
    half = z / (1 + z**2 / n) * np.sqrt(phat * (1 - phat) / n + z**2 / (4 * n**2))
    s_lo, s_hi = center - half, center + half
    cw, cs = [], []
    for p in ps:
        pk = stats.binom.pmf(k, n, p)
        cw.append(pk[(w_lo <= p) & (p <= w_hi)].sum())
        cs.append(pk[(s_lo <= p) & (p <= s_hi)].sum())
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    ax.plot(ps, cw, color=S.ORANGE, lw=1.4, label="ワルド区間 $\\hat{p} \\pm 1.96\\sqrt{\\hat{p}(1-\\hat{p})/n}$")
    ax.plot(ps, cs, color=S.BLUE, lw=1.4, label="ウィルソン区間（スコア区間）")
    ax.axhline(0.95, color=S.INK2, lw=1.2, ls=(0, (4, 3)))
    ax.set_ylim(0.5, 1.0)
    ax.set_xlabel("真の母比率 $p$")
    ax.set_ylabel("実際の被覆確率")
    ax.legend(loc="lower center")
    ax.set_title(f"$n = {n}$ のときの「95%」信頼区間が実際に真の値を含む確率", fontsize=11)
    S.save(fig, CH, "wald_coverage")


def main():
    ci_mechanism()
    ci_hundred()
    sample_size()
    wald_coverage()
