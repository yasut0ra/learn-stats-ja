"""第4章 確率の基本"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

import style as S

CH = "ch04"


def venn():
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.0))
    titles = [r"和事象 $A \cup B$", r"積事象 $A \cap B$", r"余事象 $A^c$", "排反（$A \\cap B = \\varnothing$）"]
    xx, yy = np.meshgrid(np.linspace(0, 4, 500), np.linspace(0, 3, 380))
    inA = (xx - 1.55) ** 2 + (yy - 1.5) ** 2 <= 0.95**2
    inB = (xx - 2.45) ** 2 + (yy - 1.5) ** 2 <= 0.95**2
    masks = [inA | inB, inA & inB, ~inA]
    for k, ax in enumerate(axes):
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 3)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.add_patch(Rectangle((0.05, 0.05), 3.9, 2.9, fc="none", ec=S.INK2, lw=1.2))
        ax.text(0.2, 2.65, r"$\Omega$", fontsize=13, color=S.INK2)
        if k < 3:
            img = np.zeros(xx.shape + (4,))
            rgb = np.array([0x2a, 0x78, 0xd6]) / 255
            inside = (xx > 0.05) & (xx < 3.95) & (yy > 0.05) & (yy < 2.95)
            img[masks[k] & inside] = [*rgb, 0.45]
            ax.imshow(img, extent=(0, 4, 0, 3), origin="lower", zorder=1)
            ax.add_patch(Circle((1.55, 1.5), 0.95, fc="none", ec=S.INK2, lw=1.4, zorder=2))
            ax.add_patch(Circle((2.45, 1.5), 0.95, fc="none", ec=S.INK2, lw=1.4, zorder=2))
            ax.text(1.05, 1.5, "$A$", fontsize=14, ha="center", va="center", zorder=3)
            ax.text(2.95, 1.5, "$B$", fontsize=14, ha="center", va="center", zorder=3)
        else:
            ax.add_patch(Circle((1.15, 1.5), 0.75, fc=S.BLUE, alpha=0.45, ec=S.INK2, lw=1.4))
            ax.add_patch(Circle((2.85, 1.5), 0.75, fc=S.ORANGE, alpha=0.45, ec=S.INK2, lw=1.4))
            ax.text(1.15, 1.5, "$A$", fontsize=14, ha="center", va="center")
            ax.text(2.85, 1.5, "$B$", fontsize=14, ha="center", va="center")
        ax.set_title(titles[k], fontsize=11)
    fig.tight_layout()
    S.save(fig, CH, "venn")


def relative_frequency():
    rng = np.random.default_rng(10)
    n = 5000
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for col in [S.BLUE, S.ORANGE, S.AQUA]:
        x = rng.random(n) < 0.5
        prop = np.cumsum(x) / np.arange(1, n + 1)
        i = S.log_idx(n)
        ax.plot(np.arange(1, n + 1)[i], prop[i], color=col, lw=1.6)
    ax.axhline(0.5, color=S.INK2, lw=1.2, ls=(0, (4, 3)))
    ax.set_xscale("log")
    ax.set_ylim(0, 1)
    ax.set_xlim(1, n)
    ax.set_xlabel("投げた回数（対数目盛り）")
    ax.set_ylabel("表が出た割合")
    ax.text(n * 0.9, 0.54, "1/2", ha="right", fontsize=11, color=S.INK2)
    ax.set_title("コインを投げ続けたときの「表の割合」（3人分）")
    S.save(fig, CH, "relative_frequency")


def birthday():
    ns = np.arange(1, 71)
    p = np.array([1 - np.prod((365 - np.arange(k)) / 365) for k in ns])
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    ax.plot(ns, p, color=S.BLUE)
    ax.fill_between(ns, p, color=S.BLUE, alpha=0.1, lw=0)
    for k in [23, 40, 50]:
        ax.plot([k, k], [0, p[k - 1]], color=S.MUTED, lw=1, ls=(0, (3, 2)))
        ax.scatter([k], [p[k - 1]], s=50, color=S.ORANGE, edgecolor=S.SURFACE, lw=2, zorder=3)
        ax.text(k + 1, p[k - 1] - 0.07, f"{k}人で {p[k-1]*100:.1f}%", fontsize=10, color=S.INK)
    ax.axhline(0.5, color=S.MUTED, lw=1)
    ax.set_xlim(0, 70)
    ax.set_ylim(0, 1.02)
    ax.set_yticks(np.linspace(0, 1, 6))
    ax.set_yticklabels([f"{int(v*100)}%" for v in np.linspace(0, 1, 6)])
    ax.set_xlabel("集まった人数 $n$")
    ax.set_ylabel("誕生日が同じ組がいる確率")
    S.save(fig, CH, "birthday")


def conditional_area():
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.9))
    for k, ax in enumerate(axes):
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.12, 1.08)
        ax.set_aspect("equal")
        ax.axis("off")
        if k == 0:
            ax.add_patch(Rectangle((0, 0), 1, 1, fc="#f2f1ec", ec=S.INK2, lw=1.2))
            ax.text(0.03, 0.93, r"$\Omega$（面積 1）", fontsize=11, color=S.INK2)
        ax.add_patch(Rectangle((0.35, 0.1), 0.55, 0.6, fc=S.ORANGE if k == 0 else "#fdeee7", alpha=0.25 if k == 0 else 1,
                               ec=S.ORANGE, lw=1.8))
        if k == 0:
            ax.add_patch(Rectangle((0.1, 0.3), 0.45, 0.55, fc=S.BLUE, alpha=0.18, ec=S.BLUE, lw=1.8))
            ax.text(0.15, 0.78, "$A$", fontsize=14, color=S.INK)
        ax.add_patch(Rectangle((0.35, 0.3), 0.2, 0.4, fc=S.VIOLET, alpha=0.45, ec="none"))
        ax.text(0.82, 0.15, "$B$", fontsize=14, color=S.INK)
        ax.text(0.45, 0.5, r"$A\cap B$", fontsize=10.5, ha="center", va="center", color=S.INK)
        if k == 1:
            ax.text(0.5, -0.08, r"$B$ が起きたと知ったら、$B$ を新しい「全体」とみなす", ha="center", fontsize=10,
                    color=S.INK2)
    axes[0].set_title(r"$P(A) = $ $A$ の面積 ÷ 全体の面積", fontsize=11)
    axes[1].set_title(r"$P(A \mid B) = $ $A\cap B$ の面積 ÷ $B$ の面積", fontsize=11)
    S.save(fig, CH, "conditional_area")


def independence_area():
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.0))
    for k, ax in enumerate(axes):
        ax.set_xlim(-0.08, 1.08)
        ax.set_ylim(-0.1, 1.1)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.add_patch(Rectangle((0, 0), 1, 1, fc="none", ec=S.INK2, lw=1.2))
    ax = axes[0]
    pa, pb = 0.4, 0.3
    ax.add_patch(Rectangle((0, 0), pa, 1, fc=S.BLUE, alpha=0.2, ec="none"))
    ax.add_patch(Rectangle((0, 0), 1, pb, fc=S.ORANGE, alpha=0.25, ec="none"))
    ax.add_patch(Rectangle((0, 0), pa, pb, fc=S.VIOLET, alpha=0.4, ec="none"))
    ax.text(pa / 2, 0.65, f"$A$\n$P(A)={pa}$", ha="center", fontsize=10.5)
    ax.text(0.72, pb / 2, f"$B$:  $P(B)={pb}$", ha="center", va="center", fontsize=10.5)
    ax.text(pa / 2, pb / 2, f"{pa}×{pb}\n= {pa*pb:.2f}", ha="center", va="center", fontsize=9.5)
    ax.set_title("独立：$B$ の中でも外でも $A$ の割合は 40%", fontsize=10.5)
    ax.text(pa / 2, -0.06, "40%", ha="center", fontsize=9.5, color=S.INK2)

    ax = axes[1]
    # B の中では A の割合が 80%、B の外では A の割合が 23%
    ax.add_patch(Rectangle((0, 0), 1, pb, fc=S.ORANGE, alpha=0.25, ec="none"))
    ax.add_patch(Rectangle((0, 0), 0.8, pb, fc=S.VIOLET, alpha=0.4, ec="none"))
    ax.add_patch(Rectangle((0, pb), 0.229, 1 - pb, fc=S.BLUE, alpha=0.2, ec="none"))
    ax.text(0.4, pb / 2, "$A\\cap B$：$B$ の 80%", ha="center", va="center", fontsize=10)
    ax.text(0.115, 0.65, "$A$", ha="center", fontsize=11)
    ax.text(0.9, pb / 2, "$B$", ha="center", va="center", fontsize=11)
    ax.set_title("独立でない：$B$ が起きると $A$ が起きやすい", fontsize=10.5)
    S.save(fig, CH, "independence_area")


def tree():
    fig, ax = plt.subplots(figsize=(10.6, 4.6))
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 6)
    ax.axis("off")

    def box(x, y, text, col, w=2.3, hgt=0.8):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - hgt / 2), w, hgt, boxstyle="round,pad=0.02,rounding_size=0.12",
                                    fc=col, ec="none", alpha=1))
        ax.text(x, y, text, ha="center", va="center", fontsize=10.5, color=S.INK)

    def edge(x0, y0, x1, y1, label):
        ax.plot([x0, x1], [y0, y1], color=S.AXIS, lw=1.6, zorder=0)
        ax.text((x0 + x1) / 2, (y0 + y1) / 2 + 0.18, label, ha="center", fontsize=9.5, color=S.INK2,
                bbox=dict(fc=S.SURFACE, ec="none", pad=1))

    box(1.2, 3, "10000人", "#ecebe6", w=1.9)
    box(4.3, 4.6, "病気 100人", "#fdeee7")
    box(4.3, 1.4, "健康 9900人", "#eaf2fc")
    edge(2.15, 3, 3.15, 4.6, "1%")
    edge(2.15, 3, 3.15, 1.4, "99%")
    box(8.2, 5.4, "陽性 90人", "#f8cdb9")
    box(8.2, 3.9, "陰性 10人", "#fdeee7")
    box(8.2, 2.1, "陽性 891人", "#bfd7f4")
    box(8.2, 0.6, "陰性 9009人", "#eaf2fc")
    edge(5.45, 4.6, 7.05, 5.4, "感度 90%")
    edge(5.45, 4.6, 7.05, 3.9, "10%")
    edge(5.45, 1.4, 7.05, 2.1, "9%（偽陽性）")
    edge(5.45, 1.4, 7.05, 0.6, "特異度 91%")
    ax.annotate("", xy=(9.5, 2.3), xytext=(9.5, 5.2),
                arrowprops=dict(arrowstyle="<->", color=S.ORANGE, lw=1.4, connectionstyle="arc3,rad=-0.4"))
    ax.text(10.0, 3.75, "陽性は合計 981人\nうち病気は 90人\n→ 約 9.2%", fontsize=10, color=S.INK, va="center")
    S.save(fig, CH, "tree")


def main():
    venn()
    relative_frequency()
    birthday()
    conditional_area()
    independence_area()
    tree()
