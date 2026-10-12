"""図の共通スタイル。

すべての図はこのモジュールの `setup()` を呼んでから描き、`save()` で
docs/assets/figures/<章>/<名前>.svg に書き出す。
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "docs" / "assets" / "figures"

# カテゴリ色（順番固定で使う。色覚多様性に配慮して検証済みの並び）
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
YELLOW = "#eda100"
MAGENTA = "#e87ba4"
GREEN = "#008300"
VIOLET = "#4a3aa7"
RED = "#e34948"
SERIES = [BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED]

# 文字・軸の色
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
SURFACE = "#fcfcfb"

# 塗りの透明度（面は薄く）
WASH = 0.18

JP_FONTS = [
    "BIZ UDGothic",
    "Hiragino Sans",
    "Noto Sans CJK JP",
    "Noto Sans JP",
    "IPAexGothic",
    "Yu Gothic",
    "YuGothic",
]


def _pick_font() -> str:
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in JP_FONTS:
        if name in available:
            return name
    raise RuntimeError("日本語フォントが見つかりません: " + ", ".join(JP_FONTS))


def setup() -> None:
    font = _pick_font()
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [font, "DejaVu Sans"],
            "mathtext.fontset": "cm",
            "axes.unicode_minus": False,
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.titlepad": 10,
            "axes.labelsize": 11,
            "axes.labelcolor": INK2,
            "axes.edgecolor": AXIS,
            "axes.linewidth": 1.0,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.axisbelow": True,
            "axes.facecolor": SURFACE,
            "axes.prop_cycle": plt.cycler(color=SERIES),
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "grid.linestyle": "-",
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "xtick.labelcolor": INK2,
            "ytick.labelcolor": INK2,
            "xtick.major.size": 0,
            "ytick.major.size": 0,
            "legend.frameon": False,
            "legend.fontsize": 10,
            "lines.linewidth": 2.0,
            "lines.solid_capstyle": "round",
            "lines.solid_joinstyle": "round",
            "figure.facecolor": SURFACE,
            "figure.dpi": 100,
            "savefig.facecolor": SURFACE,
            "savefig.bbox": "tight",
            "savefig.dpi": 160,
            "savefig.pad_inches": 0.15,
            "svg.fonttype": "path",
            "svg.hashsalt": "learn-stats-ja",
            "text.color": INK,
        }
    )


def save(fig, chapter: str, name: str) -> Path:
    out_dir = FIG_DIR / chapter
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.svg"
    fig.savefig(path, format="svg", metadata={"Date": None, "Creator": None})
    preview = os.environ.get("FIG_PREVIEW_DIR")
    if preview:  # 確認用の PNG も書き出す
        Path(preview).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(preview) / f"{chapter}_{name}.png", dpi=80)
    plt.close(fig)
    print(f"  saved {path.relative_to(ROOT)}")
    return path


def no_grid(ax) -> None:
    ax.grid(False)


def only_x_axis(ax) -> None:
    """密度曲線などで y 軸を消して x 軸だけ残す。"""
    ax.spines["left"].set_visible(False)
    ax.set_yticks([])
    ax.grid(False)


def annotate(ax, text, xy, xytext, color=INK2, **kw):
    ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        color=color,
        fontsize=kw.pop("fontsize", 10),
        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0, shrinkA=2, shrinkB=3),
        **kw,
    )


def log_idx(n: int, m: int = 700):
    """対数目盛りの折れ線用に 1..n から対数間隔で約 m 個の添字（0 始まり）を選ぶ。"""
    import numpy as np

    idx = np.unique(np.round(np.logspace(0, np.log10(n), m)).astype(int)) - 1
    return idx


def lin_idx(n: int, m: int = 1500):
    """線形目盛りの折れ線用に等間隔で約 m 個の添字を選ぶ。"""
    import numpy as np

    return np.unique(np.linspace(0, n - 1, m).astype(int))
