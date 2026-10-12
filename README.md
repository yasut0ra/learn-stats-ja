# やさしく学ぶ統計学 ― 記述統計から数理統計まで

[![Deploy](https://github.com/yasut0ra/learn-stats-ja/actions/workflows/deploy.yml/badge.svg)](https://github.com/yasut0ra/learn-stats-ja/actions/workflows/deploy.yml)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/deed.ja)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)

**初学者向けの統計学の無料教材です。図とシミュレーションで直感をつかみながら、数理統計学の基礎（推定・検定の理論）までしっかり学べます。**

📖 **サイトで読む → <https://yasut0ra.github.io/learn-stats-ja/>**

## 特徴

- **図が豊富**：120点以上の図で、数式の意味を「見て」理解できます。
- **動かして体感**：中心極限定理・信頼区間・検出力・最小二乗法・ベイズ更新などを、ブラウザで動くシミュレーションで体験できます。
- **数理統計までしっかり**：最尤法、フィッシャー情報量、クラメール・ラオの不等式、ネイマン・ピアソンの補題、尤度比検定まで、証明つきで扱います（証明は折りたたみ式なので、初学者は飛ばして読めます）。
- **練習問題つき**：全章に解答つきの練習問題があります。

## 目次

| 部 | 章 |
|---|---|
| 第1部 データを要約する | 1. データの種類と可視化 ／ 2. 代表値と散らばり ／ 3. 2つの変数の関係 |
| 第2部 確率と確率分布 | 4. 確率の基本 ／ 5. 確率変数と確率分布 ／ 6. 期待値と分散 ／ 7. 代表的な離散分布 ／ 8. 代表的な連続分布 ／ 9. 多次元の確率分布 ／ 10. 確率変数の変換 |
| 第3部 極限定理 | 11. 大数の法則 ／ 12. 中心極限定理 |
| 第4部 推測統計 | 13. 母集団と標本分布 ／ 14. 点推定 ／ 15. 区間推定 ／ 16. 仮説検定の考え方 ／ 17. いろいろな検定 |
| 第5部 統計モデリング | 18. 回帰分析 ／ 19. 分散分析 ／ 20. ベイズ統計入門 |
| 付録 | A. 数学の準備 ／ B. 確率分布一覧と数表 ／ C. 記号と用語 ／ D. 参考文献と次のステップ |

対象：統計学を初めて学ぶ大学生・社会人、統計検定（2級〜準1級）を目指す人、数理統計学の基礎を固めたい人。
前提知識：高校数学（数学II・B 程度の微分積分）。

## ローカルで動かす

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

ブラウザで <http://127.0.0.1:8000/learn-stats-ja/> を開くとプレビューできます。

### 図を作り直す

本文の図（`docs/assets/figures/**/*.svg`）は `scripts/figures/` の Python スクリプトから生成しています。
日本語フォント（BIZ UDGothic、ヒラギノ角ゴシック、Noto Sans CJK JP、IPAex ゴシックのいずれか）が必要です。

```bash
python scripts/make_figures.py            # すべての図
python scripts/make_figures.py ch08 ch12  # 指定した章の図だけ
python scripts/make_tables.py             # 付録Bの数表
```

## ディレクトリ構成

```text
docs/                    本文（Markdown）
├── part1 ... part5/     各部の章
├── appendix/            付録
├── assets/figures/      図（SVG、スクリプトで生成）
├── javascripts/         MathJax の設定、シミュレーション（demos.js）
└── stylesheets/         追加の CSS
scripts/
├── figures/             章ごとの図の生成スクリプトと共通スタイル
├── make_figures.py      図の一括生成
└── make_tables.py       数表の生成
mkdocs.yml               サイトの設定（MkDocs Material）
```

## 誤りの報告・貢献

誤字・計算ミス・わかりにくい説明などを見つけたら、[Issue](https://github.com/yasut0ra/learn-stats-ja/issues) で教えてください。Pull Request も歓迎します。

## ライセンス

- 本文・図：[クリエイティブ・コモンズ 表示 4.0 国際（CC BY 4.0）](https://creativecommons.org/licenses/by/4.0/deed.ja)
- ソースコード（`scripts/`、`docs/javascripts/`、`docs/stylesheets/`）：[MIT License](LICENSE)

詳しくは [LICENSE](LICENSE) と [LICENSE-CONTENT](LICENSE-CONTENT) を参照してください。
