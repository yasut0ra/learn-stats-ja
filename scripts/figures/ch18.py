"""第18章 回帰分析"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

import style as S
from ch03 import SIMPSON_GROUPS, simpson_data

CH = "ch18"

X = np.array([20, 22, 24, 25, 27, 28, 30, 31, 33, 35.0])
Y = np.array([115, 138, 140, 158, 160, 180, 178, 205, 200, 226.0])


def fit(x, y):
    b1, b0 = np.polyfit(x, y, 1)
    return b0, b1


def regression_model():
    rng = np.random.default_rng(18)
    b0, b1, sigma = 1.0, 0.8, 0.9
    fig, ax = plt.subplots(figsize=(8, 4.6))
    xs = np.linspace(0, 10, 100)
    ax.plot(xs, b0 + b1 * xs, color=S.INK2, lw=2, label=r"$E[Y \mid x] = \beta_0 + \beta_1 x$")
    for x0 in [2, 5, 8]:
        ys = np.linspace(b0 + b1 * x0 - 3 * sigma, b0 + b1 * x0 + 3 * sigma, 200)
        d = stats.norm.pdf(ys, b0 + b1 * x0, sigma)
        ax.fill_betweenx(ys, x0, x0 + d * 1.6, color=S.BLUE, alpha=0.2, lw=0)
        ax.plot(x0 + d * 1.6, ys, color=S.BLUE, lw=1.6)
        ax.plot([x0, x0], [ys[0], ys[-1]], color=S.BLUE, lw=0.8, ls=(0, (2, 2)))
    x = rng.uniform(0.5, 9.5, 40)
    y = b0 + b1 * x + rng.normal(0, sigma, 40)
    ax.scatter(x, y, s=22, color=S.ORANGE, edgecolor=S.SURFACE, lw=0.8, zorder=3, label="観測データ")
    ax.text(8.6, 9.6, r"各 $x$ で $Y$ は" "\n" r"$N(\beta_0 + \beta_1 x,\ \sigma^2)$", fontsize=10.5, color=S.INK)
    ax.set_xlim(0, 10.8)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend(loc="upper left")
    ax.set_title("単回帰モデル：直線のまわりに、同じ形の正規分布の誤差が乗る", fontsize=11)
    S.save(fig, CH, "regression_model")


def ols_residuals():
    b0, b1 = fit(X, Y)
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    xs = np.linspace(18, 37, 100)
    ax.plot(xs, b0 + b1 * xs, color=S.BLUE, lw=2, label=f"回帰直線 $y = {b0:.2f} + {b1:.2f}x$")
    yh = b0 + b1 * X
    for xi, yi, hi in zip(X, Y, yh):
        ax.plot([xi, xi], [hi, yi], color=S.ORANGE, lw=1.6)
    ax.scatter(X, Y, s=46, color=S.INK, edgecolor=S.SURFACE, lw=1.4, zorder=3, label="データ")
    ax.plot([], [], color=S.ORANGE, lw=1.6, label=r"残差 $e_i = y_i - \hat{y}_i$")
    ax.scatter([X.mean()], [Y.mean()], s=90, marker="X", color=S.VIOLET, zorder=4, label=r"$(\bar{x}, \bar{y})$")
    ax.set_xlabel("最高気温 $x$（℃）")
    ax.set_ylabel("アイスの売上 $y$（個）")
    ax.legend(loc="upper left", fontsize=9.5)
    S.save(fig, CH, "ols_residuals")


def ss_decomposition():
    b0, b1 = fit(X, Y)
    i = 7
    xi, yi = X[i], Y[i]
    hi = b0 + b1 * xi
    yb = Y.mean()
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    xs = np.linspace(18, 37, 100)
    ax.plot(xs, b0 + b1 * xs, color=S.BLUE, lw=2)
    ax.axhline(yb, color=S.MUTED, lw=1.4, ls=(0, (4, 3)))
    ax.text(18.3, yb + 2, r"$\bar{y}$", fontsize=12, color=S.INK2)
    ax.scatter(np.delete(X, i), np.delete(Y, i), s=22, color=S.AXIS, zorder=3)
    ax.scatter([xi], [yi], s=60, color=S.INK, zorder=4)
    off = 0.35
    ax.annotate("", xy=(xi - off, yi), xytext=(xi - off, yb), arrowprops=dict(arrowstyle="<->", color=S.INK2, lw=1.4))
    ax.text(xi - off - 0.3, (yi + yb) / 2, r"$y_i - \bar{y}$" "\n（全体のずれ）", ha="right", va="center", fontsize=10)
    ax.annotate("", xy=(xi + off, hi), xytext=(xi + off, yb), arrowprops=dict(arrowstyle="<->", color=S.BLUE, lw=1.4))
    ax.text(xi + off + 0.3, (hi + yb) / 2 - 4, r"$\hat{y}_i - \bar{y}$" "\n（回帰で説明できるずれ）", va="center", fontsize=10)
    ax.annotate("", xy=(xi + off, yi), xytext=(xi + off, hi), arrowprops=dict(arrowstyle="<->", color=S.ORANGE, lw=1.4))
    ax.annotate(r"$y_i - \hat{y}_i$（残差）", xy=(xi + off + 0.1, (yi + hi) / 2), xytext=(xi + 1.2, yi + 14),
                fontsize=10, arrowprops=dict(arrowstyle="-", color=S.MUTED, lw=0.8))
    ax.set_xlim(18, 38)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title(r"$y_i - \bar{y} = (\hat{y}_i - \bar{y}) + (y_i - \hat{y}_i)$", fontsize=12)
    S.save(fig, CH, "ss_decomposition")


def bands():
    b0, b1 = fit(X, Y)
    n = len(X)
    yh = b0 + b1 * X
    s = np.sqrt(((Y - yh) ** 2).sum() / (n - 2))
    Sxx = ((X - X.mean()) ** 2).sum()
    t = stats.t.isf(0.025, n - 2)
    xs = np.linspace(16, 39, 200)
    m = b0 + b1 * xs
    hm = t * s * np.sqrt(1 / n + (xs - X.mean()) ** 2 / Sxx)
    hp = t * s * np.sqrt(1 + 1 / n + (xs - X.mean()) ** 2 / Sxx)
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    ax.fill_between(xs, m - hp, m + hp, color=S.ORANGE, alpha=0.15, lw=0, label="予測区間（個々の日の売上）")
    ax.fill_between(xs, m - hm, m + hm, color=S.BLUE, alpha=0.3, lw=0, label="信頼区間（平均的な売上）")
    ax.plot(xs, m, color=S.BLUE, lw=2)
    ax.scatter(X, Y, s=40, color=S.INK, edgecolor=S.SURFACE, lw=1.2, zorder=3)
    ax.axvline(X.mean(), color=S.MUTED, lw=0.8, ls=(0, (2, 2)))
    ax.text(X.mean() + 0.2, 95, r"$\bar{x}$ で最も狭い", fontsize=9.5, color=S.INK2)
    ax.set_xlabel("最高気温 $x$（℃）")
    ax.set_ylabel("アイスの売上 $y$（個）")
    ax.legend(loc="upper left", fontsize=9.5)
    ax.set_xlim(16, 39)
    ax.set_title("95% 信頼区間と予測区間", fontsize=11)
    S.save(fig, CH, "bands")


def residual_plots():
    rng = np.random.default_rng(4)
    n = 80
    x = rng.uniform(0, 10, n)
    cases = [("問題なし：ランダムに散らばる", 2 + 0.5 * x + rng.normal(0, 0.8, n)),
             ("曲線的な関係：U字型のパターン", 1 + 0.08 * (x - 5) ** 2 * 4 + 0.5 * x + rng.normal(0, 0.8, n)),
             ("分散が一定でない：ラッパ型", 2 + 0.5 * x + rng.normal(0, 0.15 + 0.25 * x, n))]
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.2))
    for ax, (title, y) in zip(axes, cases):
        b1, b0 = np.polyfit(x, y, 1)
        fitted = b0 + b1 * x
        ax.scatter(fitted, y - fitted, s=16, color=S.BLUE, edgecolor=S.SURFACE, lw=0.5)
        ax.axhline(0, color=S.INK2, lw=1)
        ax.set_title(title, fontsize=10.5)
        ax.set_xlabel("予測値 $\\hat{y}$")
    axes[0].set_ylabel("残差 $e$")
    fig.tight_layout()
    S.save(fig, CH, "residual_plots")


def regression_to_mean():
    rng = np.random.default_rng(7)
    n = 400
    rho, mu, sd = 0.5, 170, 6
    f = rng.normal(mu, sd, n)
    s = mu + rho * (f - mu) + rng.normal(0, sd * np.sqrt(1 - rho**2), n)
    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    ax.scatter(f, s, s=10, color=S.BLUE, alpha=0.45, lw=0)
    xs = np.linspace(150, 190, 10)
    ax.plot(xs, xs, color=S.MUTED, lw=1.5, ls=(0, (4, 3)), label="$y = x$（父と同じ身長）")
    ax.plot(xs, mu + rho * (xs - mu), color=S.ORANGE, lw=2.2, label="回帰直線（傾き $\\rho$ = 0.5）")
    ax.set_xlim(150, 190)
    ax.set_ylim(150, 190)
    ax.set_aspect("equal")
    ax.set_xlabel("父の身長 (cm)")
    ax.set_ylabel("息子の身長 (cm)")
    ax.legend(loc="upper left", fontsize=9.5)
    ax.set_title("平均への回帰：背の高い父の息子は、父ほどは高くない", fontsize=11)
    S.save(fig, CH, "regression_to_mean")


def simpson_regression():
    data = simpson_data()
    Xa = np.concatenate([d[0] for d in data])
    Ya = np.concatenate([d[1] for d in data])
    age = np.concatenate([np.full(25, v) for v in (35, 55, 75)])
    A = np.column_stack([np.ones_like(Xa), Xa, age])
    beta = np.linalg.lstsq(A, Ya, rcond=None)[0]
    b1s, b0s = np.polyfit(Xa, Ya, 1)
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    for (name, _, _, col, mk), (x, y), a in zip(SIMPSON_GROUPS, data, (35, 55, 75)):
        ax.scatter(x, y, s=30, color=col, marker=mk, edgecolor=S.SURFACE, lw=1, label=name, zorder=3)
        xx = np.array([x.min(), x.max()])
        ax.plot(xx, beta[0] + beta[1] * xx + beta[2] * a, color=col, lw=2)
    xx = np.array([Xa.min(), Xa.max()])
    ax.plot(xx, b0s + b1s * xx, color=S.INK2, lw=1.6, ls=(0, (5, 3)), label=f"単回帰（傾き {b1s:+.2f}）")
    ax.set_xlabel("1週間の運動時間 $x_1$（時間）")
    ax.set_ylabel("コレステロール値 $y$")
    ax.legend(loc="upper left", ncol=2, fontsize=9.5)
    ax.set_title(f"年齢も入れた重回帰：運動時間の係数は {beta[1]:+.2f}（実線）", fontsize=11)
    S.save(fig, CH, "simpson_regression")


def main():
    regression_model()
    ols_residuals()
    ss_decomposition()
    bands()
    residual_plots()
    regression_to_mean()
    simpson_regression()
