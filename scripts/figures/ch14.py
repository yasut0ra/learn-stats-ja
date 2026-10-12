"""第14章 点推定"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from scipy import stats

import style as S

CH = "ch14"


def bias_variance_target():
    rng = np.random.default_rng(3)
    cases = [("偏りなし・ばらつき小", 0, 0.12), ("偏りなし・ばらつき大", 0, 0.38),
             ("偏りあり・ばらつき小", 0.45, 0.12), ("偏りあり・ばらつき大", 0.45, 0.38)]
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.3))
    for ax, (title, b, s) in zip(axes, cases):
        for r, a in zip([1.0, 0.66, 0.33], [0.06, 0.1, 0.16]):
            ax.add_patch(Circle((0, 0), r, fc=S.BLUE, alpha=a, ec=S.AXIS, lw=1))
        ax.plot([-1.05, 1.05], [0, 0], color=S.AXIS, lw=0.8)
        ax.plot([0, 0], [-1.05, 1.05], color=S.AXIS, lw=0.8)
        ax.scatter([0], [0], s=40, marker="+", color=S.INK, zorder=4, lw=2)
        pts = rng.normal([b, b * 0.6], s, (14, 2))
        ax.scatter(pts[:, 0], pts[:, 1], s=36, color=S.ORANGE, edgecolor=S.SURFACE, lw=1.2, zorder=5)
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=10.5)
    fig.text(0.5, 0.0, "中心（＋）が真の値 θ、点が標本をとり直すたびの推定値", ha="center", fontsize=10, color=S.INK2)
    fig.tight_layout()
    S.save(fig, CH, "bias_variance_target")


def mse_variance():
    n = np.arange(2, 31)
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    for d, col, lab in [(n - 1, S.BLUE, "$n-1$ で割る（不偏）"), (n, S.ORANGE, "$n$ で割る（最尤推定量）"),
                        (n + 1, S.AQUA, "$n+1$ で割る")]:
        # 正規母集団: SS/σ² ~ χ²(n-1), E=n-1, V=2(n-1)
        bias = (n - 1) / d - 1
        var = 2 * (n - 1) / d**2
        ax.plot(n, bias**2 + var, color=col, marker="o", ms=4, mec=S.SURFACE, mew=1, label=lab)
    ax.set_yscale("log")
    ax.set_xlabel("標本の大きさ $n$")
    ax.set_ylabel(r"平均二乗誤差 ÷ $\sigma^4$")
    ax.legend()
    ax.set_title("正規母集団で分散を推定するときの MSE：不偏推定量が最良とは限らない", fontsize=11)
    S.save(fig, CH, "mse_variance")


def mean_vs_median():
    rng = np.random.default_rng(17)
    n = 25
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.5))
    for ax, (name, draw) in zip(axes, [("正規分布の母集団", lambda size: rng.normal(0, 1, size)),
                                       ("裾の重い母集団（ラプラス分布）", lambda size: rng.laplace(0, 1 / np.sqrt(2), size))]):
        x = draw((40000, n))
        m, med = x.mean(1), np.median(x, 1)
        bins = np.linspace(-1, 1, 81)
        ax.hist(m, bins=bins, density=True, histtype="step", lw=2, color=S.BLUE,
                label=f"標本平均（標準偏差 {m.std():.3f}）")
        ax.hist(med, bins=bins, density=True, histtype="step", lw=2, color=S.ORANGE,
                label=f"標本中央値（標準偏差 {med.std():.3f}）")
        ax.set_title(f"{name}，$n = {n}$", fontsize=11)
        ax.legend(fontsize=9, loc="upper left")
        ax.set_yticks([])
        ax.set_ylim(0, 3.6)
        ax.grid(False)
    fig.tight_layout()
    S.save(fig, CH, "mean_vs_median")


def likelihood_coin():
    p = np.linspace(0.001, 0.999, 600)
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.7))
    for (n, k), col in zip([(10, 7), (50, 35), (200, 140)], [S.BLUE, S.ORANGE, S.AQUA]):
        ll = k * np.log(p) + (n - k) * np.log(1 - p)
        ll -= ll.max()
        axes[0].plot(p, np.exp(ll), color=col, label=f"{n}回中{k}回が表")
        axes[1].plot(p, ll, color=col, label=f"$n = {n}$")
    axes[0].axvline(0.7, color=S.INK2, lw=1, ls=(0, (3, 2)))
    axes[1].axvline(0.7, color=S.INK2, lw=1, ls=(0, (3, 2)))
    axes[0].set_title("尤度 $L(p)$（最大値を1にそろえた）", fontsize=11)
    axes[0].set_xlabel("$p$")
    axes[0].legend(fontsize=9)
    axes[1].set_ylim(-8, 0.5)
    axes[1].set_title(r"対数尤度 $\ell(p) - \ell(\hat{p})$：$n$ が大きいほど鋭く曲がる", fontsize=11)
    axes[1].set_xlabel("$p$")
    axes[1].legend(fontsize=9)
    fig.tight_layout()
    S.save(fig, CH, "likelihood_coin")


def likelihood_uniform():
    x = np.array([0.8, 2.1, 3.4, 4.2, 5.6])
    th = np.linspace(0.01, 12, 600)
    L = np.where(th >= x.max(), th ** (-len(x)), 0)
    fig, ax = plt.subplots(figsize=(7.6, 3.4))
    ax.plot(th, L / L.max(), color=S.BLUE)
    ax.scatter(x, np.zeros_like(x), s=50, color=S.ORANGE, edgecolor=S.SURFACE, lw=1.5, zorder=4, clip_on=False,
               label="データ")
    ax.annotate(r"最尤推定値 $\hat{\theta} = \max x_i = 5.6$", xy=(5.6, 1), xytext=(6.6, 0.8), fontsize=10.5,
                arrowprops=dict(arrowstyle="-|>", color=S.MUTED, lw=1))
    ax.text(1.0, 0.45, r"$\theta < \max x_i$ では" "\n" r"データが起こりえないので $L = 0$", fontsize=10, color=S.INK2)
    ax.set_xlabel(r"$\theta$")
    ax.set_title(r"$U(0, \theta)$ の尤度 $L(\theta) = \theta^{-n}$（$\theta \geq \max x_i$）", fontsize=11)
    ax.set_ylim(0, 1.12)
    ax.legend(loc="upper right")
    S.save(fig, CH, "likelihood_uniform")


def uniform_estimators():
    rng = np.random.default_rng(5)
    n = 10
    x = rng.random((100000, n))
    mom = 2 * x.mean(1)
    mle_u = (n + 1) / n * x.max(1)
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    bins = np.linspace(0.3, 1.7, 141)
    ax.hist(mom, bins=bins, density=True, histtype="step", lw=2, color=S.BLUE,
            label=f"モーメント推定量 $2\\bar{{X}}$（標準偏差 {mom.std():.3f}）")
    ax.hist(mle_u, bins=bins, density=True, histtype="step", lw=2, color=S.ORANGE,
            label=f"$\\frac{{n+1}}{{n}}\\max X_i$（標準偏差 {mle_u.std():.3f}）")
    ax.axvline(1, color=S.INK2, lw=1.2, ls=(0, (4, 3)))
    ax.set_yticks([])
    ax.grid(False)
    ax.legend(loc="upper left", fontsize=9.5)
    ax.set_title(r"$U(0, 1)$、$n = 10$ のとき、上限 $\theta = 1$ の2つの不偏推定量", fontsize=11)
    S.save(fig, CH, "uniform_estimators")


def mle_asymptotic():
    rng = np.random.default_rng(9)
    lam = 2.0
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.2), sharey=False)
    for ax, n in zip(axes, [5, 20, 100]):
        est = 1 / rng.exponential(1 / lam, (60000, n)).mean(1)
        se = lam / np.sqrt(n)
        lo, hi = max(0, lam - 4.5 * se), lam + 5.5 * se
        ax.hist(est, bins=np.linspace(lo, hi, 70), density=True, color=S.BLUE, edgecolor=S.SURFACE, lw=0.4)
        xs = np.linspace(lo, hi, 300)
        ax.plot(xs, stats.norm.pdf(xs, lam, se), color=S.ORANGE, lw=1.8)
        ax.axvline(lam, color=S.INK2, lw=1, ls=(0, (3, 2)))
        ax.set_title(f"$n = {n}$", fontsize=11)
        ax.set_yticks([])
        ax.grid(False)
    fig.suptitle(r"指数分布 $Ex(2)$ の率の最尤推定量 $\hat{\lambda} = 1/\bar{X}$ の分布（青）と $N(\lambda, \lambda^2/n)$（橙）",
                 fontsize=11, y=1.02)
    fig.tight_layout()
    S.save(fig, CH, "mle_asymptotic")


def main():
    bias_variance_target()
    mse_variance()
    mean_vs_median()
    likelihood_coin()
    likelihood_uniform()
    uniform_estimators()
    mle_asymptotic()
