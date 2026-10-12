"""付録B の数表（正規分布表・t 分布表・カイ二乗分布表・F 分布表）を生成する。

docs/appendix/distributions.md の
<!-- tables:start --> と <!-- tables:end --> の間を書き換える。

使い方:
    python scripts/make_tables.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "docs" / "appendix" / "distributions.md"
START, END = "<!-- tables:start -->", "<!-- tables:end -->"


def normal_table() -> str:
    lines = [
        "### 標準正規分布表（上側確率） { #normal-table }",
        "",
        "表の値は $Q(z) = P(Z \\ge z) = 1 - \\Phi(z)$ です。行が $z$ の小数第1位まで、列が小数第2位を表します。",
        "例：$z = 1.96$ なら「1.9 の行」と「0.06 の列」の交点 0.0250 を読みます。",
        "",
        "| $z$ | " + " | ".join(f"0.0{d}" for d in range(10)) + " |",
        "|---|" + "---:|" * 10,
    ]
    for r in np.arange(0, 3.5, 0.1):
        vals = [stats.norm.sf(r + d / 100) for d in range(10)]
        lines.append(f"| {r:.1f} | " + " | ".join(f"{v:.4f}" for v in vals) + " |")
    lines.append("")
    return "\n".join(lines)


def t_table() -> str:
    alphas = [0.10, 0.05, 0.025, 0.01, 0.005]
    dfs = list(range(1, 31)) + [40, 60, 120]
    lines = [
        "### $t$ 分布表（上側パーセント点） { #t-table }",
        "",
        "表の値は $P(T \\ge t_\\alpha(k)) = \\alpha$ となる $t_\\alpha(k)$ です。両側検定・95%信頼区間には $\\alpha = 0.025$ の列を使います。",
        "",
        "| 自由度 $k$ | " + " | ".join(f"$\\alpha$ = {a}" for a in alphas) + " |",
        "|---:|" + "---:|" * len(alphas),
    ]
    for k in dfs:
        lines.append(f"| {k} | " + " | ".join(f"{stats.t.isf(a, k):.3f}" for a in alphas) + " |")
    lines.append("| ∞ | " + " | ".join(f"{stats.norm.isf(a):.3f}" for a in alphas) + " |")
    lines.append("")
    return "\n".join(lines)


def chi2_table() -> str:
    alphas = [0.995, 0.99, 0.975, 0.95, 0.05, 0.025, 0.01, 0.005]
    dfs = list(range(1, 31)) + [40, 50, 60, 80, 100]
    lines = [
        "### カイ二乗分布表（上側パーセント点） { #chi2-table }",
        "",
        "表の値は $P(\\chi^2 \\ge \\chi^2_\\alpha(k)) = \\alpha$ となる $\\chi^2_\\alpha(k)$ です。"
        "カイ二乗分布は左右対称でないので、下側の点（$\\alpha = 0.975$ など）も必要になります。",
        "",
        "| 自由度 $k$ | " + " | ".join(f"{a}" for a in alphas) + " |",
        "|---:|" + "---:|" * len(alphas),
    ]
    for k in dfs:
        vals = []
        for a in alphas:
            v = stats.chi2.isf(a, k)
            if v < 0.1:
                vals.append(np.format_float_positional(v, precision=3, unique=False, fractional=False))
            else:
                vals.append(f"{v:.3f}" if v < 10 else f"{v:.2f}")
        lines.append(f"| {k} | " + " | ".join(vals) + " |")
    lines.append("")
    return "\n".join(lines)


def f_table(alpha: float, anchor: str) -> str:
    ms = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20]
    ns = list(range(1, 11)) + [12, 15, 20, 25, 30, 40, 60, 120]
    lines = [
        f"### $F$ 分布表（上側 {alpha*100:g}% 点） {{ #{anchor} }}",
        "",
        f"表の値は $P(F \\ge F_{{{alpha}}}(m, n)) = {alpha}$ となる点です。列が分子の自由度 $m$、行が分母の自由度 $n$ です。"
        "下側の点は $F_{1-\\alpha}(m, n) = 1/F_\\alpha(n, m)$ で求めます。",
        "",
        "| $n$ ＼ $m$ | " + " | ".join(str(m) for m in ms) + " |",
        "|---:|" + "---:|" * len(ms),
    ]
    for n in ns:
        vals = []
        for m in ms:
            v = stats.f.isf(alpha, m, n)
            vals.append(f"{v:.1f}" if v >= 100 else f"{v:.2f}")
        lines.append(f"| {n} | " + " | ".join(vals) + " |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    body = "\n".join([
        START,
        "",
        "## B.3 数表 { #tables }",
        "",
        "以下の数表は Python（SciPy）で計算した値です（`scripts/make_tables.py` で再生成できます）。"
        "実際の分析では、ソフトウェアで直接 $p$ 値やパーセント点を計算するのがふつうです。",
        "",
        normal_table(),
        t_table(),
        chi2_table(),
        f_table(0.05, "f-table-05"),
        f_table(0.025, "f-table-025"),
        END,
    ])
    text = TARGET.read_text(encoding="utf-8")
    if START in text and END in text:
        pre = text.split(START)[0]
        post = text.split(END)[1]
        text = pre + body + post
    else:
        text = text.rstrip() + "\n\n" + body + "\n"
    TARGET.write_text(text, encoding="utf-8")
    print(f"updated {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
