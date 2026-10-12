"""第1章 データの種類と可視化"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, FancyArrowPatch

import style as S

CH = "ch01"

SCORES = np.array([
    18, 33, 35, 40, 43, 45, 46, 49, 50, 51,
    51, 53, 54, 55, 56, 57, 58, 59, 60, 60,
    60, 62, 63, 64, 65, 66, 67, 68, 69, 70,
    70, 72, 72, 75, 75, 77, 79, 81, 84, 88,
])


def population_sample():
    rng = np.random.default_rng(1)
    fig, ax = plt.subplots(figsize=(8.6, 3.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.6)
    ax.axis("off")

    # 母集団
    ax.add_patch(Ellipse((2.3, 2.2), 4.0, 3.4, fc="#eaf2fc", ec=S.BLUE, lw=1.5))
    n = 260
    r = np.sqrt(rng.uniform(0, 1, n))
    t = rng.uniform(0, 2 * np.pi, n)
    px, py = 2.3 + 1.8 * r * np.cos(t), 2.2 + 1.5 * r * np.sin(t)
    ax.scatter(px, py, s=9, color=S.BLUE, alpha=0.55, lw=0)
    idx = rng.choice(n, 14, replace=False)
    ax.scatter(px[idx], py[idx], s=26, color=S.ORANGE, lw=0, zorder=3)
    ax.text(2.3, 4.25, "母集団", ha="center", fontsize=13, weight="bold", color=S.INK)
    ax.text(2.3, 0.15, "知りたい対象の全体（大きすぎて全部は調べられない）",
            ha="center", fontsize=9, color=S.INK2)

    # 標本
    ax.add_patch(Ellipse((7.7, 2.2), 2.2, 2.0, fc="#fdeee7", ec=S.ORANGE, lw=1.5))
    sx = 7.7 + rng.uniform(-0.75, 0.75, 14)
    sy = 2.2 + rng.uniform(-0.6, 0.6, 14)
    ax.scatter(sx, sy, s=26, color=S.ORANGE, lw=0, zorder=3)
    ax.text(7.7, 3.55, "標本（データ）", ha="center", fontsize=13, weight="bold", color=S.INK)
    ax.text(7.7, 0.75, "実際に手元にある一部", ha="center", fontsize=9, color=S.INK2)

    a1 = FancyArrowPatch((4.45, 2.75), (6.5, 2.75), connectionstyle="arc3,rad=-0.25",
                         arrowstyle="-|>", mutation_scale=16, color=S.INK2, lw=1.4)
    a2 = FancyArrowPatch((6.5, 1.65), (4.45, 1.65), connectionstyle="arc3,rad=-0.25",
                         arrowstyle="-|>", mutation_scale=16, color=S.INK2, lw=1.4)
    ax.add_patch(a1)
    ax.add_patch(a2)
    ax.text(5.45, 3.35, "無作為に抽出", ha="center", fontsize=10.5, color=S.INK)
    ax.text(5.45, 0.95, "推測する（推測統計）", ha="center", fontsize=10.5, color=S.INK)
    ax.text(9.05, 2.2, "要約する\n（記述統計）", ha="left", va="center", fontsize=10.5, color=S.INK)
    S.save(fig, CH, "population_sample")


def histogram_scores():
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    bins = np.arange(0, 101, 10)
    counts, _, patches = ax.hist(SCORES, bins=bins, color=S.BLUE, edgecolor=S.SURFACE, linewidth=2)
    for c, left in zip(counts, bins[:-1]):
        if c > 0:
            ax.text(left + 5, c + 0.25, f"{int(c)}", ha="center", va="bottom", fontsize=10, color=S.INK2)
    ax.set_xticks(bins)
    ax.set_xlabel("点数")
    ax.set_ylabel("人数（度数）")
    ax.set_ylim(0, 13)
    ax.set_title("数学のテストの点数（40人）")
    ax.grid(axis="x", visible=False)
    S.save(fig, CH, "histogram_scores")


def bin_width():
    rng = np.random.default_rng(3)
    h = np.concatenate([rng.normal(157.5, 5.0, 150), rng.normal(171.5, 5.5, 150)])
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.3), sharey=False)
    settings = [(1, "階級幅 1 cm：細かすぎてギザギザ"), (3, "階級幅 3 cm：ちょうどよい"),
                (15, "階級幅 15 cm：粗すぎて山が消える")]
    for ax, (w, title) in zip(axes, settings):
        bins = np.arange(135, 196, w)
        ax.hist(h, bins=bins, color=S.BLUE, edgecolor=S.SURFACE, linewidth=0.8 if w == 1 else 1.5)
        ax.set_title(title, fontsize=10.5)
        ax.set_xlabel("身長 (cm)")
        ax.grid(axis="x", visible=False)
        ax.set_xlim(135, 195)
    axes[0].set_ylabel("度数")
    fig.tight_layout()
    S.save(fig, CH, "bin_width")


def shapes():
    rng = np.random.default_rng(5)
    data = [
        (rng.normal(50, 10, 3000), "左右対称（単峰）"),
        (rng.gamma(2.0, 8.0, 3000), "右に裾が長い（右に歪む）"),
        (100 - rng.gamma(2.0, 8.0, 3000), "左に裾が長い（左に歪む）"),
        (np.concatenate([rng.normal(35, 7, 1500), rng.normal(70, 7, 1500)]), "二峰性（山が2つ）"),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(11.5, 2.8))
    for ax, (x, title) in zip(axes, data):
        ax.hist(x, bins=30, color=S.BLUE, edgecolor=S.SURFACE, linewidth=0.8)
        ax.set_title(title, fontsize=10.5)
        S.only_x_axis(ax)
        ax.set_xticks([])
    fig.tight_layout()
    S.save(fig, CH, "shapes")


def bar_vs_hist():
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    fruits = ["りんご", "みかん", "ぶどう", "もも", "いちご"]
    votes = [9, 7, 11, 5, 8]
    ax = axes[0]
    ax.bar(fruits, votes, width=0.55, color=S.ORANGE)
    ax.set_title("棒グラフ：質的データ（好きな果物）")
    ax.set_ylabel("人数")
    ax.grid(axis="x", visible=False)
    ax.text(0.98, 0.95, "棒の順番を入れ替えてもよい\n棒の間にすき間", transform=ax.transAxes,
            ha="right", va="top", fontsize=9, color=S.INK2)

    ax = axes[1]
    ax.hist(SCORES, bins=np.arange(10, 101, 10), color=S.BLUE, edgecolor=S.SURFACE, linewidth=1.5)
    ax.set_title("ヒストグラム：量的データ（点数）")
    ax.set_xlabel("点数")
    ax.set_ylabel("人数")
    ax.grid(axis="x", visible=False)
    ax.text(0.02, 0.95, "横軸は数直線\n柱はすき間なく並ぶ", transform=ax.transAxes,
            ha="left", va="top", fontsize=9, color=S.INK2)
    fig.tight_layout()
    S.save(fig, CH, "bar_vs_hist")


def cumulative():
    bins = np.arange(10, 101, 10)
    counts, _ = np.histogram(SCORES, bins=bins)
    cum = np.concatenate([[0], np.cumsum(counts)]) / len(SCORES)
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    ax.plot(bins, cum, color=S.BLUE, marker="o", ms=6, mec=S.SURFACE, mew=2)
    ax.set_xticks(bins)
    ax.set_yticks(np.linspace(0, 1, 6))
    ax.set_yticklabels([f"{int(v*100)}%" for v in np.linspace(0, 1, 6)])
    ax.set_xlabel("点数")
    ax.set_ylabel("累積相対度数")
    ax.set_title("累積相対度数のグラフ")
    # 60点未満
    ax.plot([60, 60], [0, cum[5]], color=S.ORANGE, lw=1.4, ls=(0, (3, 2)))
    ax.plot([10, 60], [cum[5], cum[5]], color=S.ORANGE, lw=1.4, ls=(0, (3, 2)))
    ax.text(61.5, cum[5] - 0.06, f"60点未満は {cum[5]*100:.0f}%", fontsize=10, color=S.INK)
    ax.set_xlim(10, 100)
    ax.set_ylim(0, 1.04)
    S.save(fig, CH, "cumulative")


def misleading_axis():
    years = ["2022", "2023", "2024", "2025"]
    sales = [102, 104, 103, 107]
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.4))
    for ax, (lo, title) in zip(axes, [(100, "縦軸が100から始まる → 急成長に見える"),
                                       (0, "縦軸が0から始まる → ほぼ横ばい")]):
        ax.bar(years, sales, width=0.5, color=S.BLUE)
        ax.set_ylim(lo, 110 if lo else 120)
        ax.set_title(title, fontsize=10.5)
        ax.grid(axis="x", visible=False)
        ax.set_ylabel("売上（億円）")
    fig.tight_layout()
    S.save(fig, CH, "misleading_axis")


def main():
    population_sample()
    histogram_scores()
    bin_width()
    shapes()
    bar_vs_hist()
    cumulative()
    misleading_axis()
