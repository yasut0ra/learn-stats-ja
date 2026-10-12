# 付録C 記号と用語

## C.1 記号一覧

| 記号 | 読み方・意味 | 初出 |
|---|---|---|
| $\bar{x}$ | エックスバー。データの平均値 | 第2章 |
| $s^2,\ s$ | データの分散（$n$ で割る）、標準偏差 | 第2章 |
| $s_{xy},\ r$ | データの共分散、相関係数 | 第3章 |
| $\Omega$ | オメガ。標本空間 | 第4章 |
| $A \cup B,\ A \cap B,\ A^c$ | 和事象、積事象、余事象 | 第4章 |
| $P(A),\ P(A \mid B)$ | 事象 $A$ の確率、$B$ のもとでの $A$ の条件付き確率 | 第4章 |
| $X,\ x$ | 確率変数（大文字）、その実現値（小文字） | 第5章 |
| $p(x),\ f(x),\ F(x)$ | 確率関数、確率密度関数、累積分布関数 | 第5章 |
| $E[X],\ \mu$ | 期待値（平均） | 第6章 |
| $V[X],\ \sigma^2,\ \sigma$ | 分散、標準偏差 | 第6章 |
| $M_X(t)$ | 積率母関数 | 第6章 |
| $X \sim N(\mu, \sigma^2)$ | $X$ は正規分布 $N(\mu, \sigma^2)$ に従う | 第7・8章 |
| $\phi(z),\ \Phi(z)$ | 標準正規分布の密度関数、累積分布関数 | 第8章 |
| $\mathrm{Cov}(X, Y),\ \rho$ | 共分散、相関係数（確率変数） | 第9章 |
| i.i.d. | 独立同分布 | 第9章 |
| $\xrightarrow{P},\ \xrightarrow{d}$ | 確率収束、分布収束 | 第11・12章 |
| $\bar{X}$ | 標本平均（確率変数） | 第9・13章 |
| $S^2$ | 不偏分散（$n-1$ で割る） | 第13章 |
| $\chi^2(k),\ t(k),\ F(m, n)$ | カイ二乗分布、$t$ 分布、$F$ 分布 | 第13章 |
| $z_\alpha,\ t_\alpha(k),\ \chi^2_\alpha(k),\ F_\alpha(m, n)$ | 各分布の上側 $100\alpha$% 点 | 第13章 |
| $\theta,\ \hat{\theta}$ | シータ、シータハット。母数とその推定量 | 第14章 |
| $L(\theta),\ \ell(\theta)$ | 尤度関数、対数尤度 | 第14章 |
| $I(\theta)$ | フィッシャー情報量 | 第14章 |
| $H_0,\ H_1$ | 帰無仮説、対立仮説 | 第16章 |
| $\alpha,\ \beta$ | 有意水準（第1種の過誤の確率）、第2種の過誤の確率 | 第16章 |
| $\beta_0,\ \beta_1,\ b_0,\ b_1$ | 回帰係数とその推定値 | 第18章 |
| $R^2$ | 決定係数 | 第18章 |
| $\pi(\theta),\ \pi(\theta \mid x)$ | 事前分布、事後分布 | 第20章 |

## C.2 用語集（五十音順）

| 用語 | 英語 | 説明 | 章 |
|---|---|---|---|
| i.i.d.（独立同分布） | independent and identically distributed | 互いに独立で、同じ分布に従うこと | 9 |
| 一致推定量 | consistent estimator | 標本を増やすと真の値に確率収束する推定量 | 14 |
| 帰無仮説 | null hypothesis | 検定で否定することを目指して立てる仮説 | 16 |
| 共分散 | covariance | 2変数の偏差の積の平均。関係の向きを表す | 3, 9 |
| 共役事前分布 | conjugate prior | 事後分布が事前分布と同じ種類になる事前分布 | 20 |
| 検出力 | power | 対立仮説が正しいときに帰無仮説を棄却できる確率 | 16 |
| 交絡因子 | confounder | 2つの変数の両方に影響し、見かけの関係を生む変数 | 3 |
| 最尤推定量 | maximum likelihood estimator | 尤度を最大にする母数の値 | 14 |
| 残差 | residual | 実際の値と予測値の差 | 18 |
| 四分位範囲 | interquartile range | 第3四分位数 − 第1四分位数 | 2 |
| 自由度 | degrees of freedom | 自由に値をとれる量の個数 | 13 |
| 信頼区間 | confidence interval | くり返すと一定割合で母数を含む区間 | 15 |
| 信用区間 | credible interval | 事後分布にもとづく、母数を一定確率で含む区間 | 20 |
| 正規分布 | normal distribution | 釣り鐘型の連続分布。ガウス分布 | 8 |
| 積率母関数 | moment generating function | $E[e^{tX}]$。微分するとモーメントが得られる | 6 |
| 尖度 | kurtosis | 分布の裾の重さを表す指標 | 6 |
| 相関係数 | correlation coefficient | 直線的な関係の強さ。$-1$ から $1$ | 3, 9 |
| 大数の法則 | law of large numbers | 標本平均が母平均に収束すること | 11 |
| 中心極限定理 | central limit theorem | 標本平均の分布が正規分布に近づくこと | 12 |
| 中央値 | median | 小さい順に並べたときの真ん中の値 | 2 |
| 統計量 | statistic | 標本から計算される量 | 13 |
| 独立 | independent | 一方の情報が他方の確率に影響しないこと | 4, 9 |
| 標準誤差 | standard error | 推定量の標準偏差 | 13 |
| 標本分布 | sampling distribution | 統計量の確率分布 | 13 |
| 不偏推定量 | unbiased estimator | 期待値が母数に等しい推定量 | 14 |
| 不偏分散 | unbiased variance | $n - 1$ で割った分散 | 13 |
| 分散 | variance | 平均からの偏差の2乗の平均 | 2, 6 |
| 分散分析 | analysis of variance (ANOVA) | 3つ以上の群の平均を比べる方法 | 19 |
| 平均二乗誤差 | mean squared error | 推定量と真の値の差の2乗の期待値 | 14 |
| 母集団 | population | 知りたい対象の全体 | 1, 13 |
| 母数 | parameter | 母集団分布を特徴づける定数 | 13 |
| 無作為標本 | random sample | 母集団から偏りなく選んだ標本 | 13 |
| 有意水準 | significance level | 帰無仮説を棄却する基準の確率 | 16 |
| 有効推定量 | efficient estimator | 分散がクラメール・ラオの下限に達する不偏推定量 | 14 |
| 尤度 | likelihood | データを固定し、母数の関数とみた確率（密度） | 14 |
| $p$ 値 | $p$-value | 帰無仮説のもとで観測値以上に極端な値が出る確率 | 16 |
| 歪度 | skewness | 分布の左右の非対称さを表す指標 | 6 |
