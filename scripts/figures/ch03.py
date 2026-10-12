"""第3章 2つの変数の関係"""

import matplotlib.pyplot as plt
import numpy as np

import style as S

CH = "ch03"


def study_data():
    rng = np.random.default_rng(11)
    hours = np.round(rng.uniform(1, 12, 30), 1)
    score = np.clip(np.round(35 + 4.0 * hours + rng.normal(0, 9, 30)), 0, 100)
    return hours, score


def scatter_study():
    x, y = study_data()
    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    ax.scatter(x, y, s=55, color=S.BLUE, edgecolor=S.SURFACE, lw=1.5, zorder=3)
    ax.set_xlabel("1週間の勉強時間（時間）")
    ax.set_ylabel("テストの点数")
    ax.set_title("勉強時間と点数（30人）")
    ax.set_xlim(0, 13)
    ax.set_ylim(20, 100)
    S.save(fig, CH, "scatter_study")


def correlation_types():
    rng = np.random.default_rng(2)
    n = 80
    x = rng.normal(0, 1, n)
    cases = [(0.8, "正の相関\n（右上がり）"), (-0.8, "負の相関\n（右下がり）"), (0.0, "相関なし\n（無相関）")]
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.3))
    for ax, (r, title) in zip(axes, cases):
        e = rng.normal(0, 1, n)
        y = r * x + np.sqrt(1 - r**2) * e
        ax.scatter(x, y, s=22, color=S.BLUE, edgecolor=S.SURFACE, lw=0.8)
        ax.set_title(title, fontsize=10.5)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.set_aspect("equal")
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
    fig.tight_layout()
    S.save(fig, CH, "correlation_types")


def covariance_quadrants():
    x, y = study_data()
    mx, my = x.mean(), y.mean()
    prod = (x - mx) * (y - my)
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    ax.axvline(mx, color=S.INK2, lw=1.2)
    ax.axhline(my, color=S.INK2, lw=1.2)
    xl, yl = (0, 13), (20, 100)
    ax.fill_between([mx, xl[1]], my, yl[1], color=S.BLUE, alpha=0.07, lw=0)
    ax.fill_between([xl[0], mx], yl[0], my, color=S.BLUE, alpha=0.07, lw=0)
    ax.fill_between([xl[0], mx], my, yl[1], color=S.ORANGE, alpha=0.07, lw=0)
    ax.fill_between([mx, xl[1]], yl[0], my, color=S.ORANGE, alpha=0.07, lw=0)
    pos = prod >= 0
    ax.scatter(x[pos], y[pos], s=55, color=S.BLUE, edgecolor=S.SURFACE, lw=1.5, zorder=3, label="偏差の積がプラス")
    ax.scatter(x[~pos], y[~pos], s=55, marker="s", color=S.ORANGE, edgecolor=S.SURFACE, lw=1.5, zorder=3,
               label="偏差の積がマイナス")
    kw = dict(fontsize=10.5, color=S.INK, ha="center", va="center")
    ax.text(9.4, 96, "(+) × (+) = +", **kw)
    ax.text(2.2, 25, "(−) × (−) = +", **kw)
    ax.text(2.2, 96, "(−) × (+) = −", **kw)
    ax.text(11, 25, "(+) × (−) = −", **kw)
    ax.text(mx + 0.15, 21.5, r"$\bar{x}$", fontsize=12, color=S.INK2)
    ax.text(0.2, my + 1.5, r"$\bar{y}$", fontsize=12, color=S.INK2)
    ax.set_xlim(*xl)
    ax.set_ylim(*yl)
    ax.set_xlabel("勉強時間 $x$")
    ax.set_ylabel("点数 $y$")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.32), ncol=2)
    S.save(fig, CH, "covariance_quadrants")


def correlation_grid():
    rng = np.random.default_rng(4)
    n = 100
    rs = [-0.9, -0.5, 0.0, 0.3, 0.7, 0.95]
    fig, axes = plt.subplots(1, 6, figsize=(12, 2.4))
    for ax, r in zip(axes, rs):
        x = rng.normal(0, 1, n)
        y = r * x + np.sqrt(1 - r**2) * rng.normal(0, 1, n)
        rr = np.corrcoef(x, y)[0, 1]
        ax.scatter(x, y, s=10, color=S.BLUE, lw=0, alpha=0.85)
        ax.set_title(f"$r$ = {rr:.2f}", fontsize=11)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal")
        ax.set_xlim(-3.2, 3.2)
        ax.set_ylim(-3.2, 3.2)
    fig.tight_layout()
    S.save(fig, CH, "correlation_grid")


ANSCOMBE = {
    "I": ([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
          [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
    "II": ([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
           [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
    "III": ([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
            [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
    "IV": ([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8],
           [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]),
}


def anscombe():
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.0), sharey=True)
    xx = np.array([2, 20])
    for ax, (name, (x, y)) in zip(axes, ANSCOMBE.items()):
        x, y = np.array(x), np.array(y)
        r = np.corrcoef(x, y)[0, 1]
        b, a = np.polyfit(x, y, 1)
        ax.plot(xx, a + b * xx, color=S.ORANGE, lw=1.6)
        ax.scatter(x, y, s=34, color=S.BLUE, edgecolor=S.SURFACE, lw=1.2, zorder=3)
        ax.set_title(f"データ{name}　$r$ = {r:.3f}", fontsize=10.5)
        ax.set_xlim(2, 20)
        ax.set_ylim(2, 14)
    fig.tight_layout()
    S.save(fig, CH, "anscombe")


def pitfalls():
    rng = np.random.default_rng(8)
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6))
    x = np.linspace(-3, 3, 40)
    y = x**2 + rng.normal(0, 0.6, 40)
    ax = axes[0]
    ax.scatter(x, y, s=26, color=S.BLUE, edgecolor=S.SURFACE, lw=1)
    ax.set_title(f"はっきりした関係があるのに  $r$ = {np.corrcoef(x, y)[0, 1]:.2f}", fontsize=10.5)
    ax.set_xticks([])
    ax.set_yticks([])

    ax = axes[1]
    x = rng.normal(0, 1, 25)
    y = rng.normal(0, 1, 25)
    r0 = np.corrcoef(x, y)[0, 1]
    x2, y2 = np.append(x, 7), np.append(y, 7)
    r1 = np.corrcoef(x2, y2)[0, 1]
    ax.scatter(x, y, s=26, color=S.BLUE, edgecolor=S.SURFACE, lw=1)
    ax.scatter([7], [7], s=60, facecolor=S.SURFACE, edgecolor=S.RED, lw=2, zorder=3)
    ax.annotate("この1点だけで", xy=(7, 7), xytext=(3.2, 6.6), fontsize=10, color=S.INK2,
                arrowprops=dict(arrowstyle="-|>", color=S.MUTED, lw=1))
    ax.set_title(f"外れ値1つで  $r$ = {r0:.2f} → {r1:.2f}", fontsize=10.5)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()
    S.save(fig, CH, "pitfalls")


SIMPSON_GROUPS = [("30代", 2, 180, S.BLUE, "o"), ("50代", 5, 205, S.ORANGE, "s"), ("70代", 8, 230, S.AQUA, "^")]


def simpson_data():
    """年代ごとの (運動時間, コレステロール値) のデータ。第18章でも使う。"""
    rng = np.random.default_rng(21)
    out = []
    for _, cx, cy, _, _ in SIMPSON_GROUPS:
        x = cx + rng.normal(0, 0.9, 25)
        y = cy - 6 * (x - cx) + rng.normal(0, 5, 25)
        out.append((x, y))
    return out


def simpson():
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    data = simpson_data()
    for (name, _, _, col, mk), (x, y) in zip(SIMPSON_GROUPS, data):
        ax.scatter(x, y, s=34, color=col, marker=mk, edgecolor=S.SURFACE, lw=1, label=name, zorder=3)
        b, a = np.polyfit(x, y, 1)
        xx = np.array([x.min(), x.max()])
        ax.plot(xx, a + b * xx, color=col, lw=2)
    X = np.concatenate([d[0] for d in data])
    Y = np.concatenate([d[1] for d in data])
    b, a = np.polyfit(X, Y, 1)
    xx = np.array([X.min(), X.max()])
    ax.plot(xx, a + b * xx, color=S.INK2, lw=1.6, ls=(0, (5, 3)), label="全体の傾向")
    ax.set_xlabel("1週間の運動時間（時間）")
    ax.set_ylabel("コレステロール値")
    ax.legend(loc="upper left", ncol=2)
    ax.set_title("グループ内では右下がり、全体では右上がり")
    S.save(fig, CH, "simpson")


def crosstab_bar():
    fig, ax = plt.subplots(figsize=(7.6, 2.4))
    rows = [("朝食を食べる (80人)", 42 / 80), ("朝食を食べない (20人)", 8 / 20)]
    for i, (name, p) in enumerate(rows[::-1]):
        ax.barh(i, p, color=S.BLUE, height=0.5)
        ax.barh(i, 1 - p, left=p, color=S.ORANGE, height=0.5)
        ax.text(p / 2, i, f"上位 {p*100:.1f}%", ha="center", va="center", color="white", fontsize=10)
        ax.text(p + (1 - p) / 2, i, f"下位 {(1-p)*100:.1f}%", ha="center", va="center", color="white",
                fontsize=10)
    ax.set_yticks([0, 1])
    ax.set_yticklabels([r[0] for r in rows[::-1]])
    ax.set_xlim(0, 1)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.grid(axis="y", visible=False)
    ax.set_title("朝食の有無別にみた成績上位・下位の割合（帯グラフ）", fontsize=11)
    S.save(fig, CH, "crosstab_bar")


def main():
    scatter_study()
    correlation_types()
    covariance_quadrants()
    correlation_grid()
    anscombe()
    pitfalls()
    simpson()
    crosstab_bar()
