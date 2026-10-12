"""第20章 ベイズ統計入門"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

import style as S

CH = "ch20"


def prior_likelihood_posterior():
    th = np.linspace(0.001, 0.999, 600)
    a, b = 2, 2
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.8), sharey=False)
    for ax, (n, k) in zip(axes, [(10, 7), (100, 70)]):
        prior = stats.beta.pdf(th, a, b)
        lik = stats.beta.pdf(th, k + 1, n - k + 1)  # 尤度を面積1に正規化したもの
        post = stats.beta.pdf(th, a + k, b + n - k)
        ax.plot(th, prior, color=S.MUTED, lw=1.8, ls=(0, (5, 3)), label=f"事前分布 $Be({a}, {b})$")
        ax.plot(th, lik, color=S.ORANGE, lw=1.8, label="尤度（面積を1にそろえた）")
        ax.fill_between(th, post, color=S.BLUE, alpha=0.15, lw=0)
        ax.plot(th, post, color=S.BLUE, lw=2.2, label=f"事後分布 $Be({a+k}, {b+n-k})$")
        ax.set_title(f"{n}回中{k}回表", fontsize=11)
        ax.set_xlabel(r"$\theta$（表の確率）")
        ax.legend(loc="upper left", fontsize=9)
        S.only_x_axis(ax)
    fig.tight_layout()
    S.save(fig, CH, "prior_likelihood_posterior")


def sequential_update():
    seq = [1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1]
    th = np.linspace(0.001, 0.999, 600)
    stops = [0, 1, 2, 5, 10, 20]
    cols = [S.MUTED, S.VIOLET, S.MAGENTA, S.AQUA, S.ORANGE, S.BLUE]
    fig, ax = plt.subplots(figsize=(8.2, 3.9))
    for n, col in zip(stops, cols):
        k = sum(seq[:n])
        ax.plot(th, stats.beta.pdf(th, 1 + k, 1 + n - k), color=col, lw=2,
                label=f"{n}回後（表 {k} 回）" if n else "最初（一様分布）")
    ax.set_xlabel(r"$\theta$")
    ax.set_ylim(0, 4.6)
    ax.legend(loc="upper left", fontsize=9.5, ncol=2)
    ax.set_title("データが増えるたびに事後分布が更新され、鋭くなっていく", fontsize=11)
    S.only_x_axis(ax)
    S.save(fig, CH, "sequential_update")


def normal_normal():
    mu0, tau0 = 5.0, 3.0
    xbar, se = 10.0, 8.0 / np.sqrt(10)
    prec = 1 / tau0**2 + 1 / se**2
    mpost = (mu0 / tau0**2 + xbar / se**2) / prec
    spost = np.sqrt(1 / prec)
    xs = np.linspace(-6, 22, 600)
    fig, ax = plt.subplots(figsize=(8.2, 3.8))
    ax.plot(xs, stats.norm.pdf(xs, mu0, tau0), color=S.MUTED, lw=1.8, ls=(0, (5, 3)),
            label=f"事前分布 $N({mu0:g}, {tau0:g}^2)$（過去の研究）")
    ax.plot(xs, stats.norm.pdf(xs, xbar, se), color=S.ORANGE, lw=1.8,
            label=f"尤度：$\\bar{{x}}$ = {xbar:g}、標準誤差 {se:.2f}")
    ax.fill_between(xs, stats.norm.pdf(xs, mpost, spost), color=S.BLUE, alpha=0.15, lw=0)
    ax.plot(xs, stats.norm.pdf(xs, mpost, spost), color=S.BLUE, lw=2.2,
            label=f"事後分布 $N({mpost:.2f}, {spost:.2f}^2)$")
    ax.set_xlabel(r"効果 $\mu$（血圧の低下量 mmHg）")
    ax.legend(loc="upper right", fontsize=9.5)
    ax.set_title("事後平均は事前平均とデータの平均の「精度で重みづけた平均」", fontsize=11)
    S.only_x_axis(ax)
    S.save(fig, CH, "normal_normal")


def prior_sensitivity():
    th = np.linspace(0.001, 0.999, 600)
    priors = [((1, 1), "一様 $Be(1, 1)$", S.BLUE), ((0.5, 0.5), "ジェフリーズ $Be(0.5, 0.5)$", S.ORANGE),
              ((10, 10), "強い信念 $Be(10, 10)$", S.AQUA)]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.4))
    ax = axes[0]
    for (a, b), lab, col in priors:
        ax.plot(th, stats.beta.pdf(th, a, b), color=col, lw=2, label=lab)
    ax.set_ylim(0, 4)
    ax.set_title("3つの事前分布", fontsize=11)
    handles, labels = ax.get_legend_handles_labels()
    for ax, (n, k) in zip(axes[1:], [(10, 7), (200, 140)]):
        for (a, b), lab, col in priors:
            ax.plot(th, stats.beta.pdf(th, a + k, b + n - k), color=col, lw=2)
        ax.axvline(0.7, color=S.INK2, lw=1, ls=(0, (3, 2)))
        ax.set_title(f"{n}回中{k}回表のあとの事後分布", fontsize=11)
    for ax in axes:
        S.only_x_axis(ax)
        ax.set_xlabel(r"$\theta$")
    fig.tight_layout()
    fig.legend(handles, labels, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.1), fontsize=10)
    S.save(fig, CH, "prior_sensitivity")


def main():
    prior_likelihood_posterior()
    sequential_update()
    normal_normal()
    prior_sensitivity()
