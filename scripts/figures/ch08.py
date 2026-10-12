"""第8章 代表的な連続分布"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

import style as S

CH = "ch08"


def uniform_pdf_cdf():
    a, b = 2, 5
    xs = np.linspace(0, 7, 701)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.2))
    ax = axes[0]
    f = np.where((xs >= a) & (xs <= b), 1 / (b - a), 0)
    ax.fill_between(xs, f, color=S.BLUE, alpha=0.2, lw=0)
    ax.plot(xs, f, color=S.BLUE)
    ax.set_title(r"密度関数 $f(x) = \frac{1}{b-a}$（$a \leq x \leq b$）", fontsize=11)
    ax.set_xticks([0, a, b, 7])
    ax.set_xticklabels(["0", "$a$", "$b$", "7"])
    ax.set_yticks([0, 1 / 3])
    ax.set_yticklabels(["0", r"$\frac{1}{b-a}$"])
    ax.set_ylim(0, 0.45)
    ax = axes[1]
    ax.plot(xs, np.clip((xs - a) / (b - a), 0, 1), color=S.BLUE)
    ax.set_title(r"累積分布関数 $F(x) = \frac{x-a}{b-a}$", fontsize=11)
    ax.set_xticks([0, a, b, 7])
    ax.set_xticklabels(["0", "$a$", "$b$", "7"])
    fig.tight_layout()
    S.save(fig, CH, "uniform_pdf_cdf")


def normal_params():
    xs = np.linspace(-7, 9, 600)
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.4))
    ax = axes[0]
    for mu, col in zip([-2, 0, 3], [S.BLUE, S.ORANGE, S.AQUA]):
        ax.plot(xs, stats.norm.pdf(xs, mu, 1), color=col, label=f"$\\mu = {mu}$")
    ax.set_title(r"$\mu$ を変える（$\sigma = 1$）：左右に平行移動", fontsize=11)
    ax.legend()
    S.only_x_axis(ax)
    ax = axes[1]
    for sd, col in zip([0.6, 1, 2], [S.BLUE, S.ORANGE, S.AQUA]):
        ax.plot(xs, stats.norm.pdf(xs, 0, sd), color=col, label=f"$\\sigma = {sd}$")
    ax.set_title(r"$\sigma$ を変える（$\mu = 0$）：横に伸び縮み", fontsize=11)
    ax.legend()
    S.only_x_axis(ax)
    fig.tight_layout()
    S.save(fig, CH, "normal_params")


def normal_rule():
    xs = np.linspace(-4, 4, 800)
    y = stats.norm.pdf(xs)
    fig, ax = plt.subplots(figsize=(8.4, 3.9))
    for k, alpha in [(3, 0.12), (2, 0.22), (1, 0.38)]:
        m = np.abs(xs) <= k
        ax.fill_between(xs[m], y[m], color=S.BLUE, alpha=alpha, lw=0)
    ax.plot(xs, y, color=S.BLUE)
    for k, p, h in [(1, 0.6827, 0.47), (2, 0.9545, 0.53), (3, 0.9973, 0.59)]:
        ax.annotate("", xy=(-k, h), xytext=(k, h), arrowprops=dict(arrowstyle="<->", color=S.INK2, lw=1))
        ax.text(0, h + 0.008, f"{p*100:.1f}%", ha="center", va="bottom", fontsize=10.5, color=S.INK)
    ax.set_xticks(range(-3, 4))
    ax.set_xticklabels([r"$\mu-3\sigma$", r"$\mu-2\sigma$", r"$\mu-\sigma$", r"$\mu$", r"$\mu+\sigma$",
                        r"$\mu+2\sigma$", r"$\mu+3\sigma$"])
    S.only_x_axis(ax)
    ax.set_ylim(0, 0.66)
    S.save(fig, CH, "normal_rule")


def normal_table():
    xs = np.linspace(-4, 4, 800)
    y = stats.norm.pdf(xs)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.2))
    ax = axes[0]
    z = 1.2
    ax.fill_between(xs[xs <= z], y[xs <= z], color=S.BLUE, alpha=0.3, lw=0)
    ax.plot(xs, y, color=S.BLUE)
    ax.text(-0.6, 0.12, rf"$\Phi({z}) = {stats.norm.cdf(z):.4f}$", fontsize=11, ha="center")
    ax.set_xticks([0, z])
    ax.set_xticklabels(["0", f"$z = {z}$"])
    ax.set_title(r"累積分布関数 $\Phi(z) = P(Z \leq z)$", fontsize=11)
    S.only_x_axis(ax)
    ax = axes[1]
    za = 1.96
    m = xs >= za
    ax.fill_between(xs[m], y[m], color=S.ORANGE, alpha=0.45, lw=0)
    ax.fill_between(xs[xs <= -za], y[xs <= -za], color=S.ORANGE, alpha=0.45, lw=0)
    ax.plot(xs, y, color=S.BLUE)
    ax.annotate("2.5%", xy=(2.3, 0.012), xytext=(2.8, 0.12), fontsize=10.5, color=S.INK,
                arrowprops=dict(arrowstyle="-|>", color=S.MUTED, lw=1))
    ax.annotate("2.5%", xy=(-2.3, 0.012), xytext=(-3.4, 0.12), fontsize=10.5, color=S.INK,
                arrowprops=dict(arrowstyle="-|>", color=S.MUTED, lw=1))
    ax.text(0, 0.15, "95%", ha="center", fontsize=12, color=S.INK)
    ax.set_xticks([-za, 0, za])
    ax.set_xticklabels(["−1.96", "0", "1.96"])
    ax.set_title(r"上側 2.5% 点 $z_{0.025} = 1.96$", fontsize=11)
    S.only_x_axis(ax)
    fig.tight_layout()
    S.save(fig, CH, "normal_table")


def standardization():
    mu, sd = 170, 6
    fig, axes = plt.subplots(2, 1, figsize=(8.4, 4.4), sharex=False)
    xs = np.linspace(mu - 4 * sd, mu + 4 * sd, 600)
    zs = (xs - mu) / sd
    for ax, X, lab, ticks, labels in [
        (axes[0], xs, "身長 $X \\sim N(170, 6^2)$", np.arange(150, 191, 6 * 1) + 2,
         None),
        (axes[1], zs, "標準化 $Z = (X - 170)/6 \\sim N(0, 1)$", np.arange(-3, 4), None),
    ]:
        y = stats.norm.pdf(zs) if X is zs else stats.norm.pdf(xs, mu, sd)
        thr = 180 if X is xs else (180 - mu) / sd
        m = X >= thr
        ax.fill_between(X[m], y[m], color=S.ORANGE, alpha=0.45, lw=0)
        ax.plot(X, y, color=S.BLUE)
        ax.axvline(thr, color=S.INK2, lw=1.1, ls=(0, (3, 2)))
        ax.set_title(lab, fontsize=11, loc="left")
        S.only_x_axis(ax)
    axes[0].set_xticks([152, 158, 164, 170, 176, 180, 188])
    axes[1].set_xticks([-3, -2, -1, 0, 1, 5 / 3, 3])
    axes[1].set_xticklabels(["−3", "−2", "−1", "0", "1", "1.67", "3"])
    axes[0].text(181.5, stats.norm.pdf(180, mu, sd) * 1.6, "180 cm 以上\n= 面積 0.048", fontsize=10, color=S.INK)
    axes[1].text(1.9, stats.norm.pdf(5 / 3) * 1.6, "1.67 以上\n= 同じ面積 0.048", fontsize=10, color=S.INK)
    fig.tight_layout()
    S.save(fig, CH, "standardization")


def exponential_poisson():
    rng = np.random.default_rng(4)
    lam = 2.0
    times = np.array([0.5, 1.3, 1.6, 2.6, 3.4, 3.5, 4.1, 4.9, 5.6, 5.8, 6.3, 7.2, 7.5, 7.9, 8.6, 9.1, 9.7])
    fig, axes = plt.subplots(2, 1, figsize=(9.2, 4.6), gridspec_kw={"height_ratios": [1, 2.2]})
    ax = axes[0]
    ax.plot([0, 10], [0, 0], color=S.AXIS, lw=1.5)
    ax.scatter(times, np.zeros_like(times), s=60, marker="|", color=S.BLUE, linewidths=2.5, zorder=3)
    for k in range(1, 4):
        t0 = times[k - 1]
        ax.annotate("", xy=(times[k], 0.32), xytext=(t0, 0.32), arrowprops=dict(arrowstyle="<->", color=S.ORANGE, lw=1.2))
    ax.text(times[3] + 0.2, 0.32, "← 間隔（待ち時間）", fontsize=9.5, color=S.INK2, va="center")
    for s in range(10):
        ax.axvline(s, ymin=0.25, ymax=0.45, color=S.MUTED, lw=0.6)
    ax.set_ylim(-0.4, 0.7)
    ax.set_xlim(0, 10)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.grid(False)
    ax.set_xlabel("時刻（分）")
    ax.set_title("1分あたり平均 2 回起こる出来事（ポアソン過程）", fontsize=11, loc="left")

    ax = axes[1]
    many = rng.exponential(1 / lam, 20000)
    ax.hist(many, bins=np.arange(0, 3.01, 0.1), density=True, color=S.BLUE, edgecolor=S.SURFACE, lw=1,
            label="間隔のヒストグラム（20000個）")
    xs = np.linspace(0, 3, 300)
    ax.plot(xs, lam * np.exp(-lam * xs), color=S.ORANGE, lw=2.2, label=r"指数分布 $Ex(2)$ の密度 $2e^{-2x}$")
    ax.set_xlabel("出来事の間隔（分）")
    ax.legend()
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    S.save(fig, CH, "exponential_poisson")


def gamma_shapes():
    xs = np.linspace(0.001, 12, 600)
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.5))
    ax = axes[0]
    for a, col in zip([0.7, 1, 2, 4, 7], [S.VIOLET, S.BLUE, S.ORANGE, S.AQUA, S.MAGENTA]):
        ax.plot(xs, stats.gamma.pdf(xs, a, scale=1), color=col, label=f"$\\alpha = {a}$")
    ax.set_ylim(0, 1.0)
    ax.set_title(r"形状 $\alpha$ を変える（$\lambda = 1$）", fontsize=11)
    ax.legend()
    S.only_x_axis(ax)
    ax = axes[1]
    for lam, col in zip([0.5, 1, 2], [S.BLUE, S.ORANGE, S.AQUA]):
        ax.plot(xs, stats.gamma.pdf(xs, 3, scale=1 / lam), color=col, label=f"$\\lambda = {lam}$")
    ax.set_title(r"率 $\lambda$ を変える（$\alpha = 3$）：横に伸び縮み", fontsize=11)
    ax.legend()
    S.only_x_axis(ax)
    fig.tight_layout()
    S.save(fig, CH, "gamma_shapes")


def beta_shapes():
    xs = np.linspace(0.001, 0.999, 500)
    params = [(0.5, 0.5), (1, 1), (2, 2), (2, 5), (5, 2), (8, 8)]
    fig, axes = plt.subplots(1, 6, figsize=(12, 2.4), sharey=True)
    for ax, (a, b) in zip(axes, params):
        y = stats.beta.pdf(xs, a, b)
        ax.fill_between(xs, np.minimum(y, 4), color=S.BLUE, alpha=0.18, lw=0)
        ax.plot(xs, y, color=S.BLUE)
        ax.set_ylim(0, 3.6)
        ax.set_title(f"$Be({a:g},\\ {b:g})$", fontsize=10.5)
        ax.set_xticks([0, 0.5, 1])
        ax.set_xticklabels(["0", "0.5", "1"])
        ax.grid(False)
    fig.tight_layout()
    S.save(fig, CH, "beta_shapes")


def lognormal():
    rng = np.random.default_rng(6)
    x = rng.lognormal(mean=6.0, sigma=0.6, size=20000)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.2))
    ax = axes[0]
    ax.hist(x, bins=80, range=(0, 2000), density=True, color=S.BLUE, edgecolor=S.SURFACE, lw=0.6)
    ax.set_title("$X$（対数正規分布）：右に長い裾", fontsize=11)
    ax.set_yticks([])
    ax.grid(False)
    ax = axes[1]
    ax.hist(np.log(x), bins=60, density=True, color=S.ORANGE, edgecolor=S.SURFACE, lw=0.6)
    ax.set_title(r"$\log X$：正規分布になる", fontsize=11)
    ax.set_yticks([])
    ax.grid(False)
    fig.tight_layout()
    S.save(fig, CH, "lognormal")


def main():
    uniform_pdf_cdf()
    normal_params()
    normal_rule()
    normal_table()
    standardization()
    exponential_poisson()
    gamma_shapes()
    beta_shapes()
    lognormal()
