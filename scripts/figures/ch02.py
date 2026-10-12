"""第2章 代表値と散らばり"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Rectangle
from scipy import stats

import style as S
from ch01 import SCORES

CH = "ch02"


def balance_point():
    x = np.array([2, 3, 3, 4, 8])
    m = x.mean()
    fig, ax = plt.subplots(figsize=(7.6, 2.6))
    ax.plot([0.5, 9.5], [0, 0], color=S.INK2, lw=3, solid_capstyle="butt")
    vals, cnt = np.unique(x, return_counts=True)
    for v, c in zip(vals, cnt):
        for k in range(c):
            ax.add_patch(Rectangle((v - 0.3, 0.05 + 0.62 * k), 0.6, 0.55, fc=S.BLUE, ec=S.SURFACE, lw=2))
    ax.add_patch(Polygon([[m, -0.02], [m - 0.35, -0.6], [m + 0.35, -0.6]], fc=S.ORANGE, ec="none"))
    ax.text(m, -0.95, f"平均 = {m:g}（つり合いの点）", ha="center", fontsize=11, color=S.INK)
    for t in range(1, 10):
        if t == m:
            continue
        ax.text(t, -0.25, str(t), ha="center", va="top", fontsize=9, color=S.MUTED)
    ax.set_xlim(0.3, 9.7)
    ax.set_ylim(-1.2, 1.6)
    ax.axis("off")
    S.save(fig, CH, "balance_point")


def mean_median_mode():
    a, scale = 2.2, 180
    x = np.linspace(0, 2000, 800)
    pdf = stats.gamma.pdf(x, a, scale=scale)
    mode = (a - 1) * scale
    median = stats.gamma.median(a, scale=scale)
    mean = a * scale
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.fill_between(x, pdf, color=S.BLUE, alpha=S.WASH, lw=0)
    ax.plot(x, pdf, color=S.BLUE)
    top = pdf.max()
    for v, name, col, tx, ty in [(mode, "最頻値", S.GREEN, 40, 1.12), (median, "中央値", S.VIOLET, 620, 0.95),
                                  (mean, "平均値", S.ORANGE, 720, 0.70)]:
        h = stats.gamma.pdf(v, a, scale=scale)
        ax.plot([v, v], [0, h], color=col, lw=2)
        ax.text(tx, top * ty, f"{name} {v:.0f}万円", fontsize=10, color=S.INK, va="center",
                ha="right" if tx < v else "left")
        ax.plot([v, tx + (8 if tx < v else -8)], [h * 0.8, top * ty], color=S.MUTED, lw=0.8)
    ax.set_xlabel("年収（万円）")
    S.only_x_axis(ax)
    ax.set_xlim(0, 1800)
    ax.set_ylim(0, top * 1.25)
    ax.set_title("右に裾が長い分布では  最頻値 < 中央値 < 平均値")
    S.save(fig, CH, "mean_median_mode")


def boxplot_scores():
    q1, med, q3 = 51, 60, 70
    iqr = q3 - q1
    lo_fence, hi_fence = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    inside = SCORES[(SCORES >= lo_fence) & (SCORES <= hi_fence)]
    wl, wh = inside.min(), inside.max()
    outliers = SCORES[(SCORES < lo_fence) | (SCORES > hi_fence)]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5.0), sharex=True,
                                   gridspec_kw={"height_ratios": [2.2, 1.3], "hspace": 0.08})
    ax1.hist(SCORES, bins=np.arange(10, 101, 10), color=S.BLUE, edgecolor=S.SURFACE, lw=2)
    ax1.set_ylabel("人数")
    ax1.grid(axis="x", visible=False)
    for v in [q1, med, q3]:
        ax1.axvline(v, color=S.ORANGE, lw=1.2, ls=(0, (3, 2)))

    y = 0
    ax2.add_patch(Rectangle((q1, y - 0.3), q3 - q1, 0.6, fc="#fdeee7", ec=S.ORANGE, lw=2))
    ax2.plot([med, med], [y - 0.3, y + 0.3], color=S.ORANGE, lw=3)
    ax2.plot([wl, q1], [y, y], color=S.INK2, lw=1.6)
    ax2.plot([q3, wh], [y, y], color=S.INK2, lw=1.6)
    ax2.plot([wl, wl], [y - 0.15, y + 0.15], color=S.INK2, lw=1.6)
    ax2.plot([wh, wh], [y - 0.15, y + 0.15], color=S.INK2, lw=1.6)
    ax2.scatter(outliers, [y] * len(outliers), s=50, facecolor=S.SURFACE, edgecolor=S.RED, lw=2, zorder=3)
    labels = [(outliers[0], "外れ値\n18"), (wl, f"最小値\n(外れ値除く)\n{wl}"), (q1, f"第1四分位数\n$Q_1$={q1}"),
              (med, f"中央値\n{med}"), (q3, f"第3四分位数\n$Q_3$={q3}"), (wh, f"最大値\n{wh}")]
    for v, t in labels:
        ax2.text(v, -0.55, t, ha="center", va="top", fontsize=8.5, color=S.INK2)
    ax2.annotate("", xy=(q1, 0.48), xytext=(q3, 0.48),
                 arrowprops=dict(arrowstyle="<->", color=S.INK2, lw=1))
    ax2.text((q1 + q3) / 2, 0.58, f"四分位範囲 IQR = {iqr}", ha="center", fontsize=9.5, color=S.INK)
    ax2.set_ylim(-1.6, 0.9)
    ax2.set_yticks([])
    ax2.spines["left"].set_visible(False)
    ax2.grid(False)
    ax2.set_xlim(10, 100)
    ax2.set_xlabel("点数")
    S.save(fig, CH, "boxplot_scores")


def squared_deviations():
    x = np.array([3, 5, 6, 7, 9])
    m = x.mean()
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    for xi in x:
        d = xi - m
        if d == 0:
            continue
        left = min(xi, m)
        ax.add_patch(Rectangle((left, 0), abs(d), abs(d), fc=S.BLUE, alpha=0.13, ec=S.BLUE, lw=1.4))
        cx = left + abs(d) / 2
        cy = abs(d) / 2 if abs(d) > 1 else 0.5
        if abs(d) > 1:
            ax.text(cx + (0.4 if d < 0 else -0.4), abs(d) - 0.45, f"({d:+g})² = {d*d:g}", ha="center",
                    fontsize=10, color=S.INK)
        else:
            ax.text(cx, cy, f"{d*d:g}", ha="center", va="center", fontsize=10, color=S.INK)
    ax.plot([m, m], [-0.2, 3.6], color=S.ORANGE, lw=2)
    ax.text(m, 3.7, f"平均 {m:g}", ha="center", fontsize=10.5, color=S.INK)
    ax.plot([1.6, 10.4], [0, 0], color=S.AXIS, lw=1)
    ax.scatter(x, np.zeros_like(x), s=70, color=S.BLUE, edgecolor=S.SURFACE, lw=2, zorder=3)
    for xi in x:
        ax.text(xi, -0.3, f"{xi}", ha="center", va="top", fontsize=10, color=S.INK2)
    ax.set_xlim(1.6, 10.4)
    ax.set_ylim(-0.8, 4.1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("偏差の二乗 ＝ 正方形の面積　合計 9+1+0+1+9 = 20、÷5 で分散 4", fontsize=11)
    S.save(fig, CH, "squared_deviations")


def same_mean_diff_sd():
    x = np.linspace(20, 100, 500)
    fig, ax = plt.subplots(figsize=(8, 3.4))
    for sd, col, name in [(5, S.BLUE, "クラスA：標準偏差 5"), (15, S.ORANGE, "クラスB：標準偏差 15")]:
        y = stats.norm.pdf(x, 60, sd)
        ax.plot(x, y, color=col, label=name)
        ax.fill_between(x, y, color=col, alpha=0.10, lw=0)
    ax.axvline(60, color=S.MUTED, lw=1)
    ax.text(61, 0.078, "どちらも平均60点", fontsize=10, color=S.INK2)
    S.only_x_axis(ax)
    ax.set_xlabel("点数")
    ax.legend(loc="upper right")
    S.save(fig, CH, "same_mean_diff_sd")


def zscore_compare():
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.2))
    cases = [("国語：平均 60, 標準偏差 5", 60, 5, 70, S.BLUE),
             ("数学：平均 50, 標準偏差 15", 50, 15, 75, S.ORANGE)]
    for ax, (title, mu, sd, score, col) in zip(axes, cases):
        x = np.linspace(mu - 3.3 * sd, mu + 3.3 * sd, 400)
        y = stats.norm.pdf(x, mu, sd)
        ax.plot(x, y, color=col)
        ax.fill_between(x[x >= score], y[x >= score], color=col, alpha=0.25, lw=0)
        ax.axvline(score, color=S.INK2, lw=1.2)
        z = (score - mu) / sd
        ax.text(score, y.max() * 0.95, f" {score}点\n z = {z:+.2f}", fontsize=10, color=S.INK, va="top")
        ax.set_title(title, fontsize=10.5)
        S.only_x_axis(ax)
        ticks = [mu + k * sd for k in range(-3, 4)]
        ax.set_xticks(ticks)
        ax.set_xticklabels([f"{t:g}" for t in ticks], fontsize=8.5)
    fig.suptitle("素点は数学の方が高いが、z（偏差値）で見ると国語の方が上位", fontsize=11, y=1.03)
    fig.tight_layout()
    S.save(fig, CH, "zscore_compare")


def loss_functions():
    x = np.array([2, 3, 3, 4, 8])
    a = np.linspace(0, 10, 500)
    sq = ((x[:, None] - a) ** 2).sum(0)
    ab = np.abs(x[:, None] - a).sum(0)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.4))
    ax = axes[0]
    ax.plot(a, sq, color=S.BLUE)
    ax.axvline(x.mean(), color=S.ORANGE, lw=1.4, ls=(0, (3, 2)))
    ax.text(x.mean() + 0.2, sq.max() * 0.85, f"最小 ＝ 平均 {x.mean():g}", color=S.INK, fontsize=10)
    ax.set_title(r"二乗誤差の和  $\sum (x_i-a)^2$", fontsize=11)
    ax.set_xlabel("$a$")
    ax = axes[1]
    ax.plot(a, ab, color=S.BLUE)
    ax.axvline(np.median(x), color=S.VIOLET, lw=1.4, ls=(0, (3, 2)))
    ax.text(np.median(x) + 0.2, ab.max() * 0.85, f"最小 ＝ 中央値 {np.median(x):g}", color=S.INK, fontsize=10)
    ax.set_title(r"絶対誤差の和  $\sum |x_i-a|$", fontsize=11)
    ax.set_xlabel("$a$")
    for ax in axes:
        ax.scatter(x, np.zeros_like(x), color=S.INK2, s=18, zorder=3, clip_on=False)
    fig.tight_layout()
    S.save(fig, CH, "loss_functions")


def main():
    balance_point()
    mean_median_mode()
    boxplot_scores()
    squared_deviations()
    same_mean_diff_sd()
    zscore_compare()
    loss_functions()
