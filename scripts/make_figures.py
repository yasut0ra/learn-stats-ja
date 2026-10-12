"""教材のすべての図を生成する。

使い方:
    python scripts/make_figures.py            # すべての章
    python scripts/make_figures.py ch01 ch12  # 指定した章だけ
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "figures"))

import style  # noqa: E402


def main(argv: list[str]) -> None:
    style.setup()
    modules = sorted(p.stem for p in (HERE / "figures").glob("ch*.py"))
    targets = argv or modules
    for name in targets:
        if name not in modules:
            raise SystemExit(f"不明な章: {name}（候補: {', '.join(modules)}）")
        print(f"[{name}]")
        importlib.import_module(name).main()


if __name__ == "__main__":
    main(sys.argv[1:])
