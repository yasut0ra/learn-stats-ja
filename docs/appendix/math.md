# 付録A 数学の準備

この付録では、本教材で使う数学をまとめます。すべてを最初に読む必要はありません。本文で出てきて「あれ？」と思ったときに戻ってきてください。
高校数学（数学II・B 程度）の微分積分を知っていれば、ほぼ十分です。

## A.1 和の記号 Σ { #sigma }

$\sum$（シグマ）は、たくさんの数の和を短く書くための記号です。

$$
\sum_{i=1}^{n} x_i = x_1 + x_2 + \cdots + x_n
$$

「$i$ を 1 から $n$ まで1ずつ増やしながら、$x_i$ を全部足す」と読みます。$i$ は **添字** と呼ばれ、文字は何を使ってもかまいません（$\sum_{k=1}^n x_k$ も同じ意味です）。

### 基本的な性質

$a, c$ を $i$ によらない定数とすると

1. $\displaystyle\sum_{i=1}^{n} c = nc$（同じ数 $c$ を $n$ 回足す）
2. $\displaystyle\sum_{i=1}^{n} a x_i = a\sum_{i=1}^{n} x_i$（定数は外に出せる）
3. $\displaystyle\sum_{i=1}^{n}(x_i + y_i) = \sum_{i=1}^{n} x_i + \sum_{i=1}^{n} y_i$（和は分けられる）

!!! warning "積の和は和の積ではない"
    $\sum x_i y_i \ne \left(\sum x_i\right)\left(\sum y_i\right)$、$\sum x_i^2 \ne \left(\sum x_i\right)^2$ です。

**例**：平均を $\bar{x} = \frac{1}{n}\sum x_i$ とすると、性質1〜3から

$$
\sum_{i=1}^{n}(x_i - \bar{x}) = \sum_{i=1}^{n} x_i - n\bar{x} = 0
$$

### よく使う和の公式

$$
\sum_{k=1}^{n} k = \frac{n(n+1)}{2}, \qquad \sum_{k=1}^{n} k^2 = \frac{n(n+1)(2n+1)}{6}
$$

**等比級数**：有限和は $r \ne 1$ のとき、無限和は $|r| < 1$ のとき

$$
\sum_{k=0}^{n-1} r^k = \frac{1 - r^n}{1 - r}, \qquad \sum_{k=0}^{\infty} r^k = \frac{1}{1 - r}
$$

### 二重和と積の記号

$\sum_{i}\sum_{j} a_{ij}$ は「$i$ と $j$ のすべての組み合わせについて足す」ことを表します（表のすべてのセルの合計）。
また、$\prod$（パイ）は積を表します：$\prod_{i=1}^n x_i = x_1 \times x_2 \times \cdots \times x_n$。尤度関数（第14章）で使います。

## A.2 順列・組合せ・二項定理 { #counting }

- **階乗**：$n! = n \times (n-1) \times \cdots \times 2 \times 1$。ただし $0! = 1$ と約束する。
- **順列**：$n$ 個から $r$ 個を選んで **並べる** 方法の数

    $$
    {}_n\mathrm{P}_r = n(n-1)\cdots(n-r+1) = \frac{n!}{(n-r)!}
    $$

- **組合せ**：$n$ 個から $r$ 個を **選ぶ**（順番は区別しない）方法の数

    $$
    \binom{n}{r} = {}_n\mathrm{C}_r = \frac{n!}{r!\,(n-r)!}
    $$

    順列 ${}_n\mathrm{P}_r$ の中で、選んだ $r$ 個の並べ方 $r!$ 通りを同一視したものです。

**性質**：$\binom{n}{r} = \binom{n}{n-r}$、$\binom{n}{r} = \binom{n-1}{r-1} + \binom{n-1}{r}$（パスカルの三角形）。

**二項定理**：

$$
(a + b)^n = \sum_{k=0}^{n}\binom{n}{k}a^k b^{n-k}
$$

$(a + b)$ を $n$ 個掛けるとき、$n$ 個の括弧のうちどの $k$ 個から $a$ を選ぶかが $\binom{n}{k}$ 通りあるからです。第7章の二項分布の名前の由来です。

## A.3 指数関数と対数関数

### ネイピア数 $e$

$$
e = \lim_{n\to\infty}\left(1 + \frac{1}{n}\right)^n = 2.71828\ldots
$$

より一般に $\displaystyle\lim_{n\to\infty}\left(1 + \frac{x}{n}\right)^n = e^x$ が成り立ちます。この極限は、ポアソン分布の導出（第7章）や中心極限定理の証明（第12章）で使います。
$e^x$ を $\exp(x)$ と書くこともあります（指数部分が長い式のとき見やすいため）。

### 指数法則と対数

$$
e^{a}e^{b} = e^{a+b}, \qquad (e^a)^b = e^{ab}, \qquad e^0 = 1
$$

本教材の $\log$ は、特に断らない限り **自然対数**（底が $e$、$\ln$ とも書く）です。$y = \log x \iff x = e^y$。

$$
\log(ab) = \log a + \log b, \qquad \log\frac{a}{b} = \log a - \log b, \qquad \log a^r = r\log a
$$

対数をとると **積が和に変わる** ので、尤度（多数の確率の積）は対数をとって扱います（第14章）。また $\log$ は増加関数なので、$L(\theta)$ と $\log L(\theta)$ は同じ $\theta$ で最大になります。

## A.4 微分 { #calculus }

### 微分の意味と基本公式

関数 $f(x)$ の **微分**（導関数）

$$
f'(x) = \frac{df}{dx} = \lim_{h \to 0}\frac{f(x + h) - f(x)}{h}
$$

は、グラフの各点での接線の傾き（瞬間的な変化率）を表します。

| $f(x)$ | $f'(x)$ |
|---|---|
| $x^n$ | $nx^{n-1}$ |
| $e^x$ | $e^x$ |
| $e^{ax}$ | $ae^{ax}$ |
| $\log x$ | $1/x$ |

### 微分の規則

- 和：$(f + g)' = f' + g'$、定数倍：$(cf)' = cf'$
- **積の微分**：$(fg)' = f'g + fg'$
- **合成関数の微分**（連鎖律）：$\{f(g(x))\}' = f'(g(x))\,g'(x)$

    例：$\frac{d}{dx}e^{-x^2/2} = e^{-x^2/2}\cdot(-x) = -xe^{-x^2/2}$（正規分布の密度の微分で使う）

### 最大・最小

なめらかな関数が最大・最小になる点では、$f'(x) = 0$ です（接線が水平）。
さらに $f''(x) < 0$ なら極大、$f''(x) > 0$ なら極小です。最尤推定（第14章）で「尤度方程式 $\ell'(\theta) = 0$ を解く」のはこの原理です。

### 偏微分

複数の変数をもつ関数 $f(x, y)$ を、$y$ を定数とみなして $x$ について微分したものを **偏微分** $\frac{\partial f}{\partial x}$ といいます。
多変数関数の最大・最小では、すべての変数についての偏微分が0になります。最小二乗法（第18章）や、正規分布の2つの母数の最尤推定（第14章）で使います。

## A.5 積分

### 定積分と面積

$f(x) \ge 0$ のとき、定積分 $\int_a^b f(x)\,dx$ は、$x = a$ から $x = b$ までの、グラフと $x$ 軸の間の **面積** を表します。
連続型確率変数では「密度関数の面積 ＝ 確率」なので、確率の計算は積分になります（第5章）。

**微分積分学の基本定理**：$F'(x) = f(x)$ となる $F$（原始関数）があれば

$$
\int_a^b f(x)\,dx = \big[F(x)\big]_a^b = F(b) - F(a)
$$

また $\frac{d}{dx}\int_a^x f(t)\,dt = f(x)$。累積分布関数を微分すると密度関数になる（$F' = f$）のはこのためです。

| $f(x)$ | 原始関数 $F(x)$ |
|---|---|
| $x^n$（$n \ne -1$） | $\frac{x^{n+1}}{n+1}$ |
| $1/x$ | $\log\lvert x \rvert$ |
| $e^{ax}$ | $\frac{1}{a}e^{ax}$ |

### 置換積分

$x = g(t)$ と置き換えると、$dx = g'(t)\,dt$ として

$$
\int f(x)\,dx = \int f(g(t))\,g'(t)\,dt
$$

確率変数の変数変換（第10章）の公式に現れる $\left|\frac{dx}{dy}\right|$ は、この置換積分の $g'(t)$ にあたります。

### 部分積分

積の微分の公式を積分すると

$$
\int_a^b f(x)g'(x)\,dx = \big[f(x)g(x)\big]_a^b - \int_a^b f'(x)g(x)\,dx
$$

**例**：$\displaystyle\int_0^\infty x e^{-x}\,dx = \Big[-xe^{-x}\Big]_0^\infty + \int_0^\infty e^{-x}\,dx = 0 + 1 = 1$（指数分布の期待値の計算）。

### 広義積分

積分範囲が無限大を含む場合は、極限として定義します：$\int_a^\infty f(x)\,dx = \lim_{b\to\infty}\int_a^b f(x)\,dx$。
$x \to \infty$ で $x^n e^{-x} \to 0$（指数関数は多項式より速く0に近づく）ことをよく使います。

### 重積分

2変数の関数 $f(x, y) \ge 0$ の重積分 $\iint_D f(x, y)\,dx\,dy$ は、領域 $D$ の上にあるグラフの下の **体積** を表します（第9章の同時密度関数）。
多くの場合、一方の変数について積分してから、もう一方について積分すれば計算できます。

## A.6 テイラー展開

なめらかな関数は、ある点のまわりで多項式で近似できます。$x = 0$ のまわりでは

$$
f(x) = f(0) + f'(0)x + \frac{f''(0)}{2!}x^2 + \frac{f'''(0)}{3!}x^3 + \cdots
$$

よく使う展開：

$$
e^x = \sum_{k=0}^{\infty}\frac{x^k}{k!} = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots
$$

$$
\log(1 + x) = x - \frac{x^2}{2} + \frac{x^3}{3} - \cdots \qquad (|x| < 1)
$$

$e^x$ の展開は、ポアソン分布の確率の合計が1になること（第7章）や、積率母関数がモーメントを生み出すこと（第6章）の鍵です。
また、$x$ が小さいときの1次近似 $f(x) \approx f(a) + f'(a)(x - a)$ は、デルタ法（第12章）や最尤推定量の漸近正規性（第14章）の証明で使います。

## A.7 ガウス積分 { #gauss }

正規分布の基礎となる積分です。

!!! theorem "ガウス積分"
    $$
    \int_{-\infty}^{\infty} e^{-x^2/2}\,dx = \sqrt{2\pi}
    $$

??? proof "証明"
    求める積分を $I$ とします。$I^2$ を2つの積分の積として書き、2変数の重積分に直します。

    $$
    I^2 = \int_{-\infty}^{\infty} e^{-x^2/2}\,dx\int_{-\infty}^{\infty} e^{-y^2/2}\,dy = \iint_{\mathbb{R}^2} e^{-(x^2 + y^2)/2}\,dx\,dy
    $$

    極座標 $x = r\cos\theta$、$y = r\sin\theta$ に変換すると、$x^2 + y^2 = r^2$、面積要素は $dx\,dy = r\,dr\,d\theta$（ヤコビアンが $r$）なので

    $$
    I^2 = \int_0^{2\pi}\int_0^{\infty} e^{-r^2/2}\,r\,dr\,d\theta = 2\pi\Big[-e^{-r^2/2}\Big]_0^\infty = 2\pi
    $$

    $I > 0$ なので $I = \sqrt{2\pi}$。

1変数のままでは原始関数が求まらないのに、2変数にして回転対称性を使うと解ける、という見事な証明です。
この結果から、$\frac{1}{\sqrt{2\pi}}e^{-x^2/2}$ の面積が1になり、標準正規分布の密度関数として使えることがわかります。

## A.8 ガンマ関数とベータ関数

### ガンマ関数

$$
\Gamma(\alpha) = \int_0^{\infty} x^{\alpha - 1}e^{-x}\,dx \qquad (\alpha > 0)
$$

1. $\Gamma(\alpha + 1) = \alpha\,\Gamma(\alpha)$（部分積分で示せる）
2. $\Gamma(1) = 1$ なので、正の整数 $n$ について $\Gamma(n) = (n - 1)!$。ガンマ関数は階乗を実数に拡張したもの。
3. $\Gamma(1/2) = \sqrt{\pi}$（$x = t^2/2$ と置換してガウス積分に帰着できる）

### ベータ関数

$$
B(a, b) = \int_0^1 x^{a-1}(1 - x)^{b-1}\,dx = \frac{\Gamma(a)\Gamma(b)}{\Gamma(a + b)}
$$

ガンマ分布・ベータ分布・カイ二乗分布・$t$ 分布・$F$ 分布の密度関数の「面積を1にする定数」に現れます。

**便利な公式**：密度関数の面積が1であることから、次の積分がすぐに求まります。

$$
\int_0^\infty x^{\alpha - 1}e^{-\lambda x}\,dx = \frac{\Gamma(\alpha)}{\lambda^\alpha}
$$

## A.9 行列の基礎

重回帰分析（第18章）や多変量正規分布（第9章）で使う行列の基本事項です。

- **行列の積**：$A$ が $m \times n$、$B$ が $n \times p$ のとき、$AB$ は $m \times p$ 行列で、$(AB)_{ij} = \sum_{k=1}^n A_{ik}B_{kj}$。一般に $AB \ne BA$。
- **転置**：$A^\top$ は行と列を入れ替えた行列。$(AB)^\top = B^\top A^\top$。
- **単位行列** $I$：対角成分が1、それ以外が0の正方行列。$AI = IA = A$。
- **逆行列**：正方行列 $A$ について $AA^{-1} = A^{-1}A = I$ となる $A^{-1}$。存在するのは **行列式** $\det A \ne 0$ のとき。

    2×2の場合：$A = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$ なら $\det A = ad - bc$、$A^{-1} = \dfrac{1}{ad - bc}\begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$

- **2次形式**：ベクトル $\boldsymbol{x}$ と対称行列 $A$ について $\boldsymbol{x}^\top A\boldsymbol{x} = \sum_i\sum_j A_{ij}x_i x_j$（スカラー）。
- **ベクトルの微分**：$\dfrac{\partial}{\partial\boldsymbol{b}}(\boldsymbol{b}^\top\boldsymbol{c}) = \boldsymbol{c}$、$\dfrac{\partial}{\partial\boldsymbol{b}}(\boldsymbol{b}^\top A\boldsymbol{b}) = 2A\boldsymbol{b}$（$A$ が対称のとき）。
- **確率ベクトルの1次変換**：$V[A\boldsymbol{X}] = A\,V[\boldsymbol{X}]\,A^\top$（$V[\cdot]$ は分散共分散行列）。
