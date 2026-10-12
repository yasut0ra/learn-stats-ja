/*
 * やさしく学ぶ統計学 ― インタラクティブ・シミュレーション
 *
 * Markdown 中に <div class="sim" data-sim="名前"></div> を置くと、
 * 対応するシミュレーションがその場所に組み立てられる。外部ライブラリは使わない。
 */
(function () {
  "use strict";

  /* ============================================================
   * 数学ユーティリティ
   * ============================================================ */
  const M = {};

  M.randn = function () {
    let u = 0, v = 0;
    while (u === 0) u = Math.random();
    while (v === 0) v = Math.random();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  };

  const LANCZOS = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
    771.32342877765313, -176.61502916214059, 12.507343278686905,
    -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];

  M.lgamma = function (x) {
    if (x < 0.5) return Math.log(Math.PI / Math.abs(Math.sin(Math.PI * x))) - M.lgamma(1 - x);
    x -= 1;
    let a = LANCZOS[0];
    const t = x + 7.5;
    for (let i = 1; i < 9; i++) a += LANCZOS[i] / (x + i);
    return 0.5 * Math.log(2 * Math.PI) + (x + 0.5) * Math.log(t) - t + Math.log(a);
  };

  M.erfc = function (x) {
    const z = Math.abs(x);
    const t = 1 / (1 + 0.5 * z);
    const r = t * Math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 +
      t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 +
      t * (-0.82215223 + t * 0.17087277)))))))));
    return x >= 0 ? r : 2 - r;
  };

  M.normPdf = (x, mu = 0, s = 1) => Math.exp(-0.5 * ((x - mu) / s) ** 2) / (s * Math.sqrt(2 * Math.PI));
  M.normCdf = (x) => 0.5 * M.erfc(-x / Math.SQRT2);

  M.normInv = function (p) {
    const a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
      1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00];
    const b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
      6.680131188771972e+01, -1.328068155288572e+01];
    const c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
      -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00];
    const d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00, 3.754408661907416e+00];
    const lo = 0.02425, hi = 1 - lo;
    let q, r;
    if (p < lo) {
      q = Math.sqrt(-2 * Math.log(p));
      return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) /
        ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);
    }
    if (p <= hi) {
      q = p - 0.5; r = q * q;
      return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q /
        (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);
    }
    q = Math.sqrt(-2 * Math.log(1 - p));
    return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) /
      ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);
  };

  function betacf(a, b, x) {
    const FPMIN = 1e-300;
    const qab = a + b, qap = a + 1, qam = a - 1;
    let c = 1, d = 1 - qab * x / qap;
    if (Math.abs(d) < FPMIN) d = FPMIN;
    d = 1 / d;
    let h = d;
    for (let m = 1; m <= 300; m++) {
      const m2 = 2 * m;
      let aa = m * (b - m) * x / ((qam + m2) * (a + m2));
      d = 1 + aa * d; if (Math.abs(d) < FPMIN) d = FPMIN;
      c = 1 + aa / c; if (Math.abs(c) < FPMIN) c = FPMIN;
      d = 1 / d; h *= d * c;
      aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2));
      d = 1 + aa * d; if (Math.abs(d) < FPMIN) d = FPMIN;
      c = 1 + aa / c; if (Math.abs(c) < FPMIN) c = FPMIN;
      d = 1 / d;
      const del = d * c;
      h *= del;
      if (Math.abs(del - 1) < 3e-14) break;
    }
    return h;
  }

  /** 正則化不完全ベータ関数 I_x(a, b) */
  M.incbeta = function (x, a, b) {
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    const bt = Math.exp(M.lgamma(a + b) - M.lgamma(a) - M.lgamma(b) + a * Math.log(x) + b * Math.log(1 - x));
    if (x < (a + 1) / (a + b + 2)) return bt * betacf(a, b, x) / a;
    return 1 - bt * betacf(b, a, 1 - x) / b;
  };

  M.bisect = function (f, lo, hi, target) {
    for (let i = 0; i < 100; i++) {
      const mid = (lo + hi) / 2;
      if (f(mid) < target) lo = mid; else hi = mid;
    }
    return (lo + hi) / 2;
  };

  M.tCdf = function (t, v) {
    const ib = M.incbeta(v / (v + t * t), v / 2, 0.5);
    return t >= 0 ? 1 - 0.5 * ib : 0.5 * ib;
  };
  M.tInv = (p, v) => M.bisect((t) => M.tCdf(t, v), -100, 100, p);
  M.betaInv = (p, a, b) => M.bisect((x) => M.incbeta(x, a, b), 0, 1, p);

  M.binomPmf = function (k, n, p) {
    if (k < 0 || k > n) return 0;
    if (p <= 0) return k === 0 ? 1 : 0;
    if (p >= 1) return k === n ? 1 : 0;
    return Math.exp(M.lgamma(n + 1) - M.lgamma(k + 1) - M.lgamma(n - k + 1) + k * Math.log(p) + (n - k) * Math.log(1 - p));
  };
  M.poisPmf = (k, lam) => (k < 0 ? 0 : Math.exp(k * Math.log(lam) - lam - M.lgamma(k + 1)));
  M.geomPmf = (k, p) => (k < 0 ? 0 : p * Math.pow(1 - p, k));
  M.gammaPdf = (x, shape, rate) => (x <= 0 ? 0 :
    Math.exp(shape * Math.log(rate) + (shape - 1) * Math.log(x) - rate * x - M.lgamma(shape)));
  M.betaPdf = (x, a, b) => (x <= 0 || x >= 1 ? 0 :
    Math.exp((a - 1) * Math.log(x) + (b - 1) * Math.log(1 - x) + M.lgamma(a + b) - M.lgamma(a) - M.lgamma(b)));
  M.tPdf = (x, v) => Math.exp(M.lgamma((v + 1) / 2) - M.lgamma(v / 2) - 0.5 * Math.log(v * Math.PI) -
    (v + 1) / 2 * Math.log(1 + x * x / v));
  M.chi2Pdf = (x, k) => M.gammaPdf(x, k / 2, 0.5);
  M.fPdf = (x, m, n) => (x <= 0 ? 0 : Math.exp(0.5 * (m * Math.log(m * x) + n * Math.log(n) - (m + n) * Math.log(m * x + n)) -
    Math.log(x) - (M.lgamma(m / 2) + M.lgamma(n / 2) - M.lgamma((m + n) / 2))));

  M.mean = (a) => a.reduce((s, v) => s + v, 0) / a.length;
  M.sd = function (a, ddof = 0) {
    const m = M.mean(a);
    return Math.sqrt(a.reduce((s, v) => s + (v - m) ** 2, 0) / (a.length - ddof));
  };
  M.corr = function (x, y) {
    const mx = M.mean(x), my = M.mean(y);
    let sxy = 0, sxx = 0, syy = 0;
    for (let i = 0; i < x.length; i++) {
      sxy += (x[i] - mx) * (y[i] - my);
      sxx += (x[i] - mx) ** 2;
      syy += (y[i] - my) ** 2;
    }
    return sxy / Math.sqrt(sxx * syy);
  };
  M.linspace = function (a, b, n) {
    const out = [];
    for (let i = 0; i < n; i++) out.push(a + (b - a) * i / (n - 1));
    return out;
  };
  M.range = function (a, b) {
    const out = [];
    for (let i = a; i <= b; i++) out.push(i);
    return out;
  };

  /* ============================================================
   * 描画ユーティリティ
   * ============================================================ */
  const PLOTS = new Set();

  function h(tag, cls, parent, text) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }

  function palette(el) {
    const cs = getComputedStyle(el);
    const g = (n) => cs.getPropertyValue(n).trim();
    return {
      surface: g("--sim-surface"), ink: g("--sim-ink"), ink2: g("--sim-ink2"), muted: g("--sim-muted"),
      grid: g("--sim-grid"), axis: g("--sim-axis"),
      s1: g("--sim-s1"), s2: g("--sim-s2"), s3: g("--sim-s3"), s4: g("--sim-s4"), red: g("--sim-red"),
      font: g("--sim-font") || "system-ui, sans-serif",
    };
  }

  function niceStep(range, n) {
    const raw = range / n;
    const p = Math.pow(10, Math.floor(Math.log10(raw)));
    const f = raw / p;
    return (f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10) * p;
  }

  function ticks(a, b, n) {
    const s = niceStep(b - a, n || 5);
    const out = [];
    for (let v = Math.ceil(a / s - 1e-9) * s; v <= b + 1e-9 * Math.abs(s); v += s) out.push(+v.toFixed(10));
    return out;
  }

  function fmtTick(v, step) {
    const d = Math.max(0, -Math.floor(Math.log10(step) + 1e-9));
    return v.toFixed(Math.min(d, 4));
  }

  function rgba(hex, a) {
    const m = hex.replace("#", "");
    const n = parseInt(m.length === 3 ? m.split("").map((c) => c + c).join("") : m, 16);
    return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
  }

  class Plot {
    constructor(root, o) {
      this.o = Object.assign({ height: 300, pad: [14, 16, 44, 54] }, o || {});
      this.root = root;
      this.wrap = h("div", "sim-plot", o && o.parent ? o.parent : root);
      if (this.o.maxWidth) this.wrap.style.maxWidth = this.o.maxWidth + "px";
      this.canvas = h("canvas", "", this.wrap);
      this.canvas.setAttribute("role", "img");
      if (this.o.label) this.canvas.setAttribute("aria-label", this.o.label);
      this.ctx = this.canvas.getContext("2d");
      this.x0 = 0; this.x1 = 1; this.y0 = 0; this.y1 = 1; this.xlog = false;
      this.draw = function () {};
      this.hover = null;
      this.hx = null;
      const move = (e) => {
        if (!this.hover) return;
        const r = this.canvas.getBoundingClientRect();
        this.hx = e.clientX - r.left;
        this.hy = e.clientY - r.top;
        this.render();
      };
      this.canvas.addEventListener("pointermove", move);
      this.canvas.addEventListener("pointerdown", move);
      this.canvas.addEventListener("pointerleave", () => { this.hx = null; this.render(); });
      if (window.ResizeObserver) new ResizeObserver(() => this.render()).observe(this.wrap);
      PLOTS.add(this);
    }

    render() {
      const w = this.wrap.clientWidth;
      if (!w) return;
      const hgt = typeof this.o.height === "function" ? this.o.height(w) : this.o.height;
      const dpr = window.devicePixelRatio || 1;
      if (this.canvas.width !== Math.round(w * dpr) || this.canvas.height !== Math.round(hgt * dpr)) {
        this.canvas.width = Math.round(w * dpr);
        this.canvas.height = Math.round(hgt * dpr);
        this.canvas.style.width = w + "px";
        this.canvas.style.height = hgt + "px";
      }
      this.W = w; this.H = hgt;
      const ctx = this.ctx;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      this.c = palette(this.root);
      ctx.fillStyle = this.c.surface;
      ctx.fillRect(0, 0, w, hgt);
      const [t, r, b, l] = this.o.pad;
      this.L = l; this.R = w - r; this.T = t; this.B = hgt - b;
      this.draw(this);
      if (this.hover && this.hx != null && this.hx >= this.L && this.hx <= this.R) this.drawHover();
    }

    domain(x0, x1, y0, y1) { this.x0 = x0; this.x1 = x1; this.y0 = y0; this.y1 = y1; return this; }

    sx(x) {
      if (this.xlog) {
        const a = Math.log10(this.x0), b = Math.log10(this.x1);
        return this.L + (Math.log10(x) - a) / (b - a) * (this.R - this.L);
      }
      return this.L + (x - this.x0) / (this.x1 - this.x0) * (this.R - this.L);
    }
    sy(y) { return this.B - (y - this.y0) / (this.y1 - this.y0) * (this.B - this.T); }
    ix(px) {
      const f = (px - this.L) / (this.R - this.L);
      if (this.xlog) {
        const a = Math.log10(this.x0), b = Math.log10(this.x1);
        return Math.pow(10, a + f * (b - a));
      }
      return this.x0 + f * (this.x1 - this.x0);
    }
    iy(py) { return this.y0 + (this.B - py) / (this.B - this.T) * (this.y1 - this.y0); }

    font(size, weight) { return `${weight || 400} ${size || 12}px ${this.c.font}`; }

    axes(o) {
      o = o || {};
      const ctx = this.ctx, c = this.c;
      ctx.save();
      ctx.lineWidth = 1;
      ctx.font = this.font(11);
      // y 目盛り・グリッド
      if (!o.noY) {
        const yt = o.yticks || ticks(this.y0, this.y1, o.yn || 5);
        const ystep = yt.length > 1 ? yt[1] - yt[0] : 1;
        ctx.textAlign = "right";
        ctx.textBaseline = "middle";
        for (const v of yt) {
          const y = Math.round(this.sy(v)) + 0.5;
          if (o.grid !== false) {
            ctx.strokeStyle = c.grid;
            ctx.beginPath(); ctx.moveTo(this.L, y); ctx.lineTo(this.R, y); ctx.stroke();
          }
          ctx.fillStyle = c.ink2;
          ctx.fillText(o.yfmt ? o.yfmt(v) : fmtTick(v, ystep), this.L - 6, y);
        }
      }
      // x 目盛り
      let xt;
      if (this.xlog) {
        xt = [];
        for (let e = Math.ceil(Math.log10(this.x0)); e <= Math.log10(this.x1) + 1e-9; e++) xt.push(Math.pow(10, e));
      } else {
        xt = o.xticks || ticks(this.x0, this.x1, o.xn || 6);
      }
      const xstep = xt.length > 1 ? xt[1] - xt[0] : 1;
      ctx.textAlign = "center";
      ctx.textBaseline = "top";
      ctx.fillStyle = c.ink2;
      for (const v of xt) {
        const x = this.sx(v);
        if (x < this.L - 1 || x > this.R + 1) continue;
        if (o.xgrid) {
          ctx.strokeStyle = c.grid;
          ctx.beginPath(); ctx.moveTo(Math.round(x) + 0.5, this.T); ctx.lineTo(Math.round(x) + 0.5, this.B); ctx.stroke();
        }
        ctx.fillText(o.xfmt ? o.xfmt(v) : (this.xlog ? String(v) : fmtTick(v, xstep)), x, this.B + 6);
      }
      // 軸線
      ctx.strokeStyle = c.axis;
      ctx.beginPath();
      ctx.moveTo(this.L, Math.round(this.B) + 0.5);
      ctx.lineTo(this.R, Math.round(this.B) + 0.5);
      ctx.stroke();
      // ラベル
      ctx.fillStyle = c.ink2;
      ctx.font = this.font(12);
      if (o.xlabel) {
        ctx.textAlign = "center"; ctx.textBaseline = "bottom";
        ctx.fillText(o.xlabel, (this.L + this.R) / 2, this.H - 4);
      }
      if (o.ylabel) {
        ctx.save();
        ctx.translate(13, (this.T + this.B) / 2);
        ctx.rotate(-Math.PI / 2);
        ctx.textAlign = "center"; ctx.textBaseline = "middle";
        ctx.fillText(o.ylabel, 0, 0);
        ctx.restore();
      }
      ctx.restore();
    }

    clip(fn) {
      const ctx = this.ctx;
      ctx.save();
      ctx.beginPath();
      ctx.rect(this.L, this.T - 2, this.R - this.L, this.B - this.T + 2);
      ctx.clip();
      fn();
      ctx.restore();
    }

    line(xs, ys, color, width, dash) {
      const ctx = this.ctx;
      this.clip(() => {
        ctx.strokeStyle = color;
        ctx.lineWidth = width || 2;
        ctx.lineJoin = "round"; ctx.lineCap = "round";
        ctx.setLineDash(dash || []);
        ctx.beginPath();
        let started = false;
        for (let i = 0; i < xs.length; i++) {
          if (!isFinite(ys[i])) { started = false; continue; }
          const X = this.sx(xs[i]), Y = this.sy(ys[i]);
          if (!started) { ctx.moveTo(X, Y); started = true; } else ctx.lineTo(X, Y);
        }
        ctx.stroke();
      });
    }

    area(xs, ys, color, alpha, base) {
      const ctx = this.ctx;
      const b = this.sy(base == null ? Math.max(this.y0, 0) : base);
      if (xs.length < 2) return;
      this.clip(() => {
        ctx.fillStyle = rgba(color, alpha == null ? 0.15 : alpha);
        ctx.beginPath();
        ctx.moveTo(this.sx(xs[0]), b);
        for (let i = 0; i < xs.length; i++) ctx.lineTo(this.sx(xs[i]), this.sy(Math.min(ys[i], this.y1 * 2)));
        ctx.lineTo(this.sx(xs[xs.length - 1]), b);
        ctx.closePath();
        ctx.fill();
      });
    }

    /** ヒストグラム：edges は境界（長さ k+1）、heights は長さ k */
    hist(edges, heights, color, alpha) {
      const ctx = this.ctx;
      this.clip(() => {
        ctx.fillStyle = alpha == null ? color : rgba(color, alpha);
        for (let i = 0; i < heights.length; i++) {
          if (!(heights[i] > 0)) continue;
          const x0 = this.sx(edges[i]) + 1, x1 = this.sx(edges[i + 1]) - 1;
          const y = this.sy(heights[i]);
          ctx.fillRect(x0, y, Math.max(1, x1 - x0), this.B - y);
        }
      });
    }

    /** 離散分布の棒（幅 w はデータ単位） */
    bars(xs, ys, color, w, highlight) {
      const ctx = this.ctx;
      const pxw = Math.min(24, Math.max(2, Math.abs(this.sx(w) - this.sx(0)) * 0.7));
      this.clip(() => {
        for (let i = 0; i < xs.length; i++) {
          if (!(ys[i] > 0)) continue;
          const X = this.sx(xs[i]), Y = this.sy(ys[i]);
          ctx.fillStyle = highlight && highlight(xs[i]) ? highlight(xs[i]) : color;
          const r = Math.min(3, pxw / 2, (this.B - Y) / 2);
          ctx.beginPath();
          ctx.moveTo(X - pxw / 2, this.B);
          ctx.lineTo(X - pxw / 2, Y + r);
          ctx.quadraticCurveTo(X - pxw / 2, Y, X - pxw / 2 + r, Y);
          ctx.lineTo(X + pxw / 2 - r, Y);
          ctx.quadraticCurveTo(X + pxw / 2, Y, X + pxw / 2, Y + r);
          ctx.lineTo(X + pxw / 2, this.B);
          ctx.closePath();
          ctx.fill();
        }
      });
    }

    dots(xs, ys, color, r, ring) {
      const ctx = this.ctx;
      r = r || 4;
      this.clip(() => {
        for (let i = 0; i < xs.length; i++) {
          const X = this.sx(xs[i]), Y = this.sy(ys[i]);
          ctx.beginPath();
          ctx.arc(X, Y, r, 0, 2 * Math.PI);
          ctx.fillStyle = color;
          ctx.fill();
          if (ring !== false) {
            ctx.lineWidth = 1.5;
            ctx.strokeStyle = this.c.surface;
            ctx.stroke();
          }
        }
      });
    }

    vline(x, color, width, dash, label, labelSide) {
      const ctx = this.ctx;
      const X = this.sx(x);
      if (X < this.L - 1 || X > this.R + 1) return;
      ctx.save();
      ctx.strokeStyle = color;
      ctx.lineWidth = width || 1.5;
      ctx.setLineDash(dash || []);
      ctx.beginPath(); ctx.moveTo(X, this.T); ctx.lineTo(X, this.B); ctx.stroke();
      if (label) {
        ctx.setLineDash([]);
        ctx.font = this.font(11.5);
        ctx.fillStyle = this.c.ink;
        ctx.textBaseline = "top";
        ctx.textAlign = labelSide === "left" ? "right" : "left";
        ctx.fillText(label, X + (labelSide === "left" ? -5 : 5), this.T + 2);
      }
      ctx.restore();
    }

    hline(y, color, width, dash) {
      const ctx = this.ctx;
      const Y = this.sy(y);
      ctx.save();
      ctx.strokeStyle = color;
      ctx.lineWidth = width || 1.5;
      ctx.setLineDash(dash || []);
      ctx.beginPath(); ctx.moveTo(this.L, Y); ctx.lineTo(this.R, Y); ctx.stroke();
      ctx.restore();
    }

    text(str, x, y, o) {
      o = o || {};
      const ctx = this.ctx;
      ctx.save();
      ctx.font = this.font(o.size || 12, o.weight);
      ctx.fillStyle = o.color || this.c.ink;
      ctx.textAlign = o.align || "left";
      ctx.textBaseline = o.baseline || "middle";
      ctx.fillText(str, o.px ? x : this.sx(x), o.px ? y : this.sy(y));
      ctx.restore();
    }

    drawHover() {
      const res = this.hover(this.ix(this.hx), this.iy(this.hy));
      if (!res) return;
      const ctx = this.ctx, c = this.c;
      const X = res.x != null ? this.sx(res.x) : this.hx;
      ctx.save();
      ctx.strokeStyle = c.muted;
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(Math.round(X) + 0.5, this.T); ctx.lineTo(Math.round(X) + 0.5, this.B); ctx.stroke();
      if (res.points) {
        for (const p of res.points) {
          ctx.beginPath();
          ctx.arc(this.sx(p[0]), this.sy(p[1]), 4.5, 0, 2 * Math.PI);
          ctx.fillStyle = p[2] || c.s1;
          ctx.fill();
          ctx.lineWidth = 2;
          ctx.strokeStyle = c.surface;
          ctx.stroke();
        }
      }
      ctx.font = this.font(12);
      const lines = res.lines;
      const w = Math.max(...lines.map((s) => ctx.measureText(s).width)) + 16;
      const hh = lines.length * 17 + 10;
      let bx = X + 12;
      if (bx + w > this.W - 4) bx = X - 12 - w;
      const by = this.T + 4;
      ctx.fillStyle = c.surface;
      ctx.strokeStyle = c.axis;
      ctx.lineWidth = 1;
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(bx, by, w, hh, 6); else ctx.rect(bx, by, w, hh);
      ctx.fill();
      ctx.stroke();
      ctx.fillStyle = c.ink;
      ctx.textAlign = "left";
      ctx.textBaseline = "top";
      lines.forEach((s, i) => ctx.fillText(s, bx + 8, by + 6 + i * 17));
      ctx.restore();
    }
  }

  /* ---------- 操作パネル ---------- */
  function panel(root) { return h("div", "sim-controls", root); }

  function slider(parent, o, onInput) {
    const box = h("label", "sim-field", parent);
    const top = h("span", "sim-field-label", box);
    h("span", "", top, o.label);
    const val = h("output", "sim-value", top);
    const input = h("input", "", box);
    input.type = "range";
    input.min = o.min; input.max = o.max; input.step = o.step; input.value = o.value;
    const fmt = o.fmt || ((v) => String(v));
    const api = {
      get value() { return o.map ? o.map(+input.value) : +input.value; },
      set value(v) { input.value = v; val.textContent = fmt(api.value); },
      setMax(m) { input.max = m; if (+input.value > m) input.value = m; val.textContent = fmt(api.value); },
      input,
    };
    val.textContent = fmt(api.value);
    input.addEventListener("input", () => { val.textContent = fmt(api.value); onInput && onInput(); });
    return api;
  }

  function select(parent, o, onChange) {
    const box = h("label", "sim-field", parent);
    h("span", "sim-field-label", box, o.label);
    const sel = h("select", "", box);
    for (const [v, t] of o.options) {
      const op = h("option", "", sel, t);
      op.value = v;
    }
    sel.value = o.value;
    sel.addEventListener("change", () => onChange && onChange());
    return { get value() { return sel.value; }, set value(v) { sel.value = v; }, el: sel };
  }

  function button(parent, text, onClick, primary) {
    const b = h("button", primary ? "sim-btn sim-btn-primary" : "sim-btn", parent, text);
    b.type = "button";
    b.addEventListener("click", onClick);
    return b;
  }

  function checkbox(parent, text, value, onChange) {
    const box = h("label", "sim-check", parent);
    const i = h("input", "", box);
    i.type = "checkbox";
    i.checked = !!value;
    h("span", "", box, text);
    i.addEventListener("change", () => onChange && onChange());
    return { get value() { return i.checked; } };
  }

  function buttons(parent) { return h("div", "sim-buttons", parent); }
  function readout(root) { return h("div", "sim-readout", root); }
  function legend(root, items) {
    const box = h("div", "sim-legend", root);
    for (const [key, text, kind] of items) {
      const it = h("span", "sim-legend-item", box);
      const sw = h("span", "sim-swatch" + (kind ? " sim-swatch-" + kind : ""), it);
      sw.style.setProperty("--sw", `var(--sim-${key})`);
      h("span", "", it, text);
    }
    return box;
  }

  const f = (v, d) => (v == null || !isFinite(v) ? "—" : v.toFixed(d == null ? 3 : d));
  const pct = (v, d) => (v * 100).toFixed(d == null ? 1 : d) + "%";

  /* ============================================================
   * シミュレーション本体
   * ============================================================ */
  const SIMS = {};

  /* ---------- 第3章 相関係数 ---------- */
  SIMS.correlation = function (root) {
    const ui = panel(root);
    let Z;
    const regen = () => {
      Z = [[], []];
      for (let i = 0; i < 500; i++) { Z[0].push(M.randn()); Z[1].push(M.randn()); }
    };
    regen();
    const rho = slider(ui, { label: "相関の強さ（データを作る設定値）", min: -1, max: 1, step: 0.05, value: 0.7, fmt: (v) => v.toFixed(2) }, () => plot.render());
    const nS = slider(ui, { label: "点の数 n", min: 10, max: 500, step: 10, value: 100 }, () => plot.render());
    const bt = buttons(root);
    button(bt, "新しいデータを作る", () => { regen(); plot.render(); }, true);
    const plot = new Plot(root, { height: (w) => Math.min(w, 400) - 8, maxWidth: 420, pad: [12, 12, 36, 44], label: "散布図" });
    const out = readout(root);
    plot.draw = (p) => {
      const r = rho.value, n = nS.value;
      const xs = Z[0].slice(0, n);
      const ys = xs.map((x, i) => r * x + Math.sqrt(Math.max(0, 1 - r * r)) * Z[1][i]);
      p.domain(-3.6, 3.6, -3.6, 3.6);
      p.axes({ xlabel: "x", ylabel: "y", xgrid: true });
      p.dots(xs, ys, p.c.s1, n > 250 ? 2.5 : 3.5);
      out.innerHTML = `データから計算した相関係数 <b>r = ${f(M.corr(xs, ys))}</b>` +
        (n <= 30 ? "　（点が少ないと、設定値からのずれが大きくなります）" : "");
    };
  };

  /* ---------- 第4章 ベイズの定理（検査の陽性的中率） ---------- */
  SIMS["bayes-test"] = function (root) {
    const ui = panel(root);
    const prev = slider(ui, { label: "有病率（病気の人の割合）", min: 0.1, max: 30, step: 0.1, value: 1, fmt: (v) => v.toFixed(1) + "%" }, () => plot.render());
    const sens = slider(ui, { label: "感度 P(陽性 | 病気)", min: 50, max: 100, step: 1, value: 90, fmt: (v) => v + "%" }, () => plot.render());
    const spec = slider(ui, { label: "特異度 P(陰性 | 健康)", min: 50, max: 99.9, step: 0.1, value: 91, fmt: (v) => v.toFixed(1) + "%" }, () => plot.render());
    const plot = new Plot(root, { height: (w) => Math.round(Math.min(w, 640) * 0.42), maxWidth: 640, pad: [6, 6, 6, 6], label: "1000人の検査結果" });
    legend(root, [["s2", "病気・陽性"], ["s2", "病気・陰性", "light"], ["s1", "健康・陽性（偽陽性）"], ["grid", "健康・陰性", "plain"]]);
    const out = readout(root);
    plot.draw = (p) => {
      const pr = prev.value / 100, se = sens.value / 100, sp = spec.value / 100;
      const N = 1000, cols = 50, rows = 20;
      const D = Math.round(N * pr);
      const TP = Math.round(D * se), FN = D - TP;
      const FP = Math.round((N - D) * (1 - sp));
      const cw = (p.R - p.L) / cols, ch = (p.B - p.T) / rows;
      const ctx = p.ctx;
      const colorOf = (i) => {
        if (i < TP) return p.c.s2;
        if (i < TP + FN) return rgba(p.c.s2, 0.35);
        if (i < TP + FN + FP) return p.c.s1;
        return p.c.grid;
      };
      for (let i = 0; i < N; i++) {
        const col = Math.floor(i / rows), row = i % rows;
        ctx.fillStyle = colorOf(i);
        const x = p.L + col * cw, y = p.T + row * ch;
        ctx.beginPath();
        if (ctx.roundRect) ctx.roundRect(x + 1, y + 1, cw - 2, ch - 2, 2); else ctx.rect(x + 1, y + 1, cw - 2, ch - 2);
        ctx.fill();
      }
      const n = 10000;
      const d = n * pr, tp = d * se, fp = (n - d) * (1 - sp);
      const post = tp / (tp + fp);
      out.innerHTML =
        `<div>10000人が検査を受けると：病気の人 <b>${Math.round(d)}人</b> のうち陽性 <b>${Math.round(tp)}人</b>、` +
        `健康な人 <b>${Math.round(n - d)}人</b> のうち陽性（偽陽性）<b>${Math.round(fp)}人</b>。</div>` +
        `<div>陽性になった ${Math.round(tp + fp)}人 のうち、本当に病気なのは ${Math.round(tp)}人 → ` +
        `<b class="sim-big">P(病気 | 陽性) = ${pct(post)}</b></div>`;
    };
  };

  /* ---------- 第7・8・13章 分布エクスプローラ ---------- */
  const DISTS = {
    binom: {
      name: "二項分布 B(n, p)", discrete: true,
      params: [{ k: "n", label: "試行回数 n", min: 1, max: 60, step: 1, value: 10 },
        { k: "p", label: "成功確率 p", min: 0.01, max: 0.99, step: 0.01, value: 0.3 }],
      pmf: (x, P) => M.binomPmf(x, P.n, P.p), xr: (P) => [0, Math.max(10, P.n)],
      mean: (P) => P.n * P.p, vari: (P) => P.n * P.p * (1 - P.p),
    },
    pois: {
      name: "ポアソン分布 Po(λ)", discrete: true,
      params: [{ k: "lam", label: "平均 λ", min: 0.1, max: 20, step: 0.1, value: 3 }],
      pmf: (x, P) => M.poisPmf(x, P.lam), xr: () => [0, 35],
      mean: (P) => P.lam, vari: (P) => P.lam,
    },
    geom: {
      name: "幾何分布 Ge(p)（失敗の回数）", discrete: true,
      params: [{ k: "p", label: "成功確率 p", min: 0.05, max: 1, step: 0.01, value: 0.3 }],
      pmf: (x, P) => M.geomPmf(x, P.p), xr: () => [0, 30],
      mean: (P) => (1 - P.p) / P.p, vari: (P) => (1 - P.p) / (P.p * P.p),
    },
    norm: {
      name: "正規分布 N(μ, σ²)",
      params: [{ k: "mu", label: "平均 μ", min: -4, max: 4, step: 0.1, value: 0 },
        { k: "sd", label: "標準偏差 σ", min: 0.3, max: 3, step: 0.05, value: 1 }],
      pdf: (x, P) => M.normPdf(x, P.mu, P.sd), xr: () => [-8, 8], cap: 1.4,
      mean: (P) => P.mu, vari: (P) => P.sd * P.sd,
    },
    exp: {
      name: "指数分布 Ex(λ)",
      params: [{ k: "lam", label: "率 λ", min: 0.2, max: 3, step: 0.05, value: 1 }],
      pdf: (x, P) => (x < 0 ? 0 : P.lam * Math.exp(-P.lam * x)), xr: () => [0, 8], cap: 3.2,
      mean: (P) => 1 / P.lam, vari: (P) => 1 / (P.lam * P.lam),
    },
    gamma: {
      name: "ガンマ分布 Ga(α, λ)",
      params: [{ k: "a", label: "形状 α", min: 0.5, max: 12, step: 0.1, value: 2 },
        { k: "lam", label: "率 λ", min: 0.2, max: 3, step: 0.05, value: 1 }],
      pdf: (x, P) => M.gammaPdf(x, P.a, P.lam), xr: () => [0, 20], cap: 1.6,
      mean: (P) => P.a / P.lam, vari: (P) => P.a / (P.lam * P.lam),
    },
    beta: {
      name: "ベータ分布 Be(a, b)",
      params: [{ k: "a", label: "a", min: 0.5, max: 12, step: 0.1, value: 2 },
        { k: "b", label: "b", min: 0.5, max: 12, step: 0.1, value: 5 }],
      pdf: (x, P) => M.betaPdf(x, P.a, P.b), xr: () => [0, 1], cap: 5,
      mean: (P) => P.a / (P.a + P.b), vari: (P) => P.a * P.b / ((P.a + P.b) ** 2 * (P.a + P.b + 1)),
    },
    unif: {
      name: "一様分布 U(a, b)",
      params: [{ k: "a", label: "下端 a", min: -3, max: 3, step: 0.1, value: 0 },
        { k: "w", label: "幅 b − a", min: 0.5, max: 8, step: 0.1, value: 2 }],
      pdf: (x, P) => (x >= P.a && x <= P.a + P.w ? 1 / P.w : 0), xr: () => [-4, 12], cap: 2.2,
      mean: (P) => P.a + P.w / 2, vari: (P) => P.w * P.w / 12,
    },
    chi2: {
      name: "カイ二乗分布 χ²(k)",
      params: [{ k: "k", label: "自由度 k", min: 1, max: 30, step: 1, value: 3 }],
      pdf: (x, P) => M.chi2Pdf(x, P.k), xr: () => [0, 45], cap: 0.55,
      mean: (P) => P.k, vari: (P) => 2 * P.k,
    },
    t: {
      name: "t 分布 t(ν)（点線は標準正規分布）",
      params: [{ k: "v", label: "自由度 ν", min: 1, max: 50, step: 1, value: 3 }],
      pdf: (x, P) => M.tPdf(x, P.v), xr: () => [-5, 5], cap: 0.45, ref: (x) => M.normPdf(x),
      mean: (P) => (P.v > 1 ? 0 : NaN), vari: (P) => (P.v > 2 ? P.v / (P.v - 2) : NaN),
    },
    f: {
      name: "F 分布 F(m, n)",
      params: [{ k: "m", label: "自由度 m", min: 1, max: 50, step: 1, value: 5 },
        { k: "n", label: "自由度 n", min: 1, max: 50, step: 1, value: 10 }],
      pdf: (x, P) => M.fPdf(x, P.m, P.n), xr: () => [0, 5], cap: 2.5,
      mean: (P) => (P.n > 2 ? P.n / (P.n - 2) : NaN),
      vari: (P) => (P.n > 4 ? 2 * P.n * P.n * (P.m + P.n - 2) / (P.m * (P.n - 2) ** 2 * (P.n - 4)) : NaN),
    },
  };
  const FAMILIES = {
    discrete: ["binom", "pois", "geom"],
    continuous: ["norm", "exp", "gamma", "beta", "unif"],
    sampling: ["chi2", "t", "f"],
  };

  SIMS.distribution = function (root) {
    const keys = FAMILIES[root.dataset.family || "continuous"] || FAMILIES.continuous;
    const ui = panel(root);
    const sel = select(ui, { label: "分布", options: keys.map((k) => [k, DISTS[k].name]), value: root.dataset.initial || keys[0] }, build);
    const paramBox = h("div", "sim-controls sim-sub", root);
    const plot = new Plot(root, { height: 300, label: "確率分布のグラフ" });
    const out = readout(root);
    let sliders = {};
    function params() {
      const P = {};
      for (const k in sliders) P[k] = sliders[k].value;
      return P;
    }
    function build() {
      paramBox.innerHTML = "";
      sliders = {};
      const d = DISTS[sel.value];
      for (const q of d.params) {
        const dec = q.step < 0.1 ? 2 : q.step < 1 ? 1 : 0;
        sliders[q.k] = slider(paramBox, Object.assign({ fmt: (v) => v.toFixed(dec) }, q), () => plot.render());
      }
      plot.render();
    }
    plot.draw = (p) => {
      const d = DISTS[sel.value], P = params();
      const [a, b] = d.xr(P);
      const mean = d.mean(P), vari = d.vari(P);
      if (d.discrete) {
        const xs = M.range(a, b), ys = xs.map((x) => d.pmf(x, P));
        const ymax = Math.max(...ys) * 1.15 || 1;
        p.domain(a - 0.7, b + 0.7, 0, ymax);
        p.axes({ xlabel: "x", ylabel: "P(X = x)", xticks: ticks(a, b, 8).filter((v) => Number.isInteger(v)) });
        p.bars(xs, ys, p.c.s1, 1);
        if (isFinite(mean)) p.vline(mean, p.c.s2, 1.5, [4, 3], "平均 " + f(mean, 2));
        p.hover = (x) => {
          const k = Math.round(x);
          if (k < a || k > b) return null;
          return { x: k, lines: [`x = ${k}`, `P(X = ${k}) = ${f(d.pmf(k, P), 4)}`] };
        };
      } else {
        const xs = M.linspace(a, b, 600), ys = xs.map((x) => d.pdf(x, P));
        const inner = ys.filter((v, i) => i > 2 && i < ys.length - 3 && isFinite(v));
        let ymax = Math.min(Math.max(...inner) * 1.15, d.cap);
        if (d.ref) ymax = Math.max(ymax, 0.45);
        p.domain(a, b, 0, ymax);
        p.axes({ xlabel: "x", ylabel: "密度 f(x)" });
        p.area(xs, ys, p.c.s1, 0.14);
        if (d.ref) p.line(xs, xs.map(d.ref), p.c.muted, 1.5, [5, 4]);
        p.line(xs, ys, p.c.s1, 2);
        if (isFinite(mean)) p.vline(mean, p.c.s2, 1.5, [4, 3], "平均 " + f(mean, 2));
        p.hover = (x) => ({ x, lines: [`x = ${f(x, 2)}`, `f(x) = ${f(d.pdf(x, P), 4)}`], points: [[x, Math.min(d.pdf(x, P), ymax)]] });
      }
      out.innerHTML = `期待値 E[X] = <b>${f(mean, 3)}</b>　分散 V[X] = <b>${f(vari, 3)}</b>　標準偏差 = <b>${f(Math.sqrt(vari), 3)}</b>` +
        (isFinite(mean) ? "" : "　（この自由度では期待値が存在しません）");
    };
    build();
  };

  /* ---------- 第11章 大数の法則 ---------- */
  SIMS.lln = function (root) {
    const ui = panel(root);
    const pS = slider(ui, { label: "表が出る確率 p", min: 0.1, max: 0.9, step: 0.05, value: 0.5, fmt: (v) => v.toFixed(2) }, reset);
    const bt = buttons(root);
    const K = 3, MAX = 10000;
    let seqs, n;
    function reset() { seqs = Array.from({ length: K }, () => []); n = 0; plot.render(); }
    function add(m) {
      const p = pS.value;
      m = Math.min(m, MAX - n);
      for (const s of seqs) {
        let c = s.length ? s[s.length - 1] * s.length : 0;
        for (let i = 0; i < m; i++) {
          c += Math.random() < p ? 1 : 0;
          s.push(c / (s.length + 1));
        }
      }
      n += m;
      plot.render();
    }
    button(bt, "+10回", () => add(10), true);
    button(bt, "+100回", () => add(100));
    button(bt, "+1000回", () => add(1000));
    button(bt, "一気に10000回まで", () => add(MAX));
    button(bt, "リセット", reset);
    const plot = new Plot(root, { height: 320, label: "表の割合の推移" });
    legend(root, [["s1", "1人目"], ["s2", "2人目"], ["s3", "3人目"], ["s1", "p ± 2√(p(1−p)/n) の範囲", "band"]]);
    const out = readout(root);
    plot.draw = (pl) => {
      const p = pS.value;
      pl.xlog = true;
      pl.domain(1, MAX, 0, 1);
      const xs = [], lo = [], hi = [];
      for (let k = 1; k <= MAX; k = Math.ceil(k * 1.05)) {
        xs.push(k);
        const s = 2 * Math.sqrt(p * (1 - p) / k);
        lo.push(Math.max(0, p - s)); hi.push(Math.min(1, p + s));
      }
      // 帯（±2σ）
      const ctx = pl.ctx;
      pl.clip(() => {
        ctx.fillStyle = rgba(pl.c.s1, 0.1);
        ctx.beginPath();
        xs.forEach((x, i) => (i ? ctx.lineTo(pl.sx(x), pl.sy(hi[i])) : ctx.moveTo(pl.sx(x), pl.sy(hi[i]))));
        for (let i = xs.length - 1; i >= 0; i--) ctx.lineTo(pl.sx(xs[i]), pl.sy(lo[i]));
        ctx.closePath();
        ctx.fill();
      });
      pl.axes({ xlabel: "投げた回数 n（対数目盛り）", ylabel: "表の割合" });
      pl.hline(p, pl.c.muted, 1.2, [5, 4]);
      const cols = [pl.c.s1, pl.c.s2, pl.c.s3];
      seqs.forEach((s, j) => {
        if (!s.length) return;
        const idx = [];
        for (let k = 1; k <= s.length; k = k < 50 ? k + 1 : Math.ceil(k * 1.01)) idx.push(k);
        if (idx[idx.length - 1] !== s.length) idx.push(s.length);
        pl.line(idx, idx.map((k) => s[k - 1]), cols[j], 1.8);
      });
      pl.text(`真の確率 p = ${p.toFixed(2)}`, pl.R - 4, pl.sy(p) - 10, { px: true, align: "right", color: pl.c.ink2, size: 11 });
      out.innerHTML = n === 0 ? "ボタンを押してコインを投げてください。" :
        `${n}回投げた時点での表の割合：` + seqs.map((s, j) => `${j + 1}人目 <b>${f(s[s.length - 1], 3)}</b>`).join("　");
    };
    reset();
  };

  /* ---------- 第12章 中心極限定理 ---------- */
  const PARENTS = {
    unif: { name: "一様分布 U(0, 1)", draw: () => Math.random(), mu: 0.5, sd: Math.sqrt(1 / 12), xr: [0, 1],
      pdf: (x) => (x >= 0 && x <= 1 ? 1 : 0) },
    exp: { name: "指数分布 Ex(1)（右に歪んだ分布）", draw: () => -Math.log(1 - Math.random()), mu: 1, sd: 1, xr: [0, 5],
      pdf: (x) => (x >= 0 ? Math.exp(-x) : 0) },
    dice: { name: "サイコロの目", draw: () => 1 + Math.floor(6 * Math.random()), mu: 3.5, sd: Math.sqrt(35 / 12), xr: [0.5, 6.5],
      pmf: [1, 2, 3, 4, 5, 6].map((k) => [k, 1 / 6]) },
    bern: { name: "ベルヌーイ分布（p = 0.1）", draw: () => (Math.random() < 0.1 ? 1 : 0), mu: 0.1, sd: 0.3, xr: [-0.15, 1.15],
      pmf: [[0, 0.9], [1, 0.1]] },
    bimodal: { name: "山が2つある分布", draw: () => (Math.random() < 0.5 ? -2 : 2) + 0.6 * M.randn(), mu: 0, sd: Math.sqrt(4 + 0.36), xr: [-4.5, 4.5],
      pdf: (x) => 0.5 * M.normPdf(x, -2, 0.6) + 0.5 * M.normPdf(x, 2, 0.6) },
  };
  const NS = [1, 2, 3, 4, 5, 10, 20, 30, 50, 100];

  SIMS.clt = function (root) {
    const ui = panel(root);
    const sel = select(ui, { label: "元の分布（母集団）", options: Object.keys(PARENTS).map((k) => [k, PARENTS[k].name]), value: root.dataset.initial || "exp" }, reset);
    const nS = slider(ui, { label: "標本の大きさ n", min: 0, max: NS.length - 1, step: 1, value: 0, map: (i) => NS[i] }, reset);
    const bt = buttons(root);
    button(bt, "標本平均を1000回つくる", () => add(1000), true);
    button(bt, "+10000回", () => add(10000));
    button(bt, "リセット", reset);
    const top = new Plot(root, { height: 130, pad: [10, 16, 26, 54], label: "元の分布" });
    const plot = new Plot(root, { height: 280, label: "標本平均のヒストグラム" });
    legend(root, [["s1", "標本平均のヒストグラム"], ["s2", "正規分布 N(μ, σ²/n)", "line"]]);
    const out = readout(root);
    let means = [];
    function reset() { means = []; top.render(); plot.render(); }
    function add(m) {
      const P = PARENTS[sel.value], n = nS.value;
      for (let i = 0; i < m; i++) {
        let s = 0;
        for (let j = 0; j < n; j++) s += P.draw();
        means.push(s / n);
      }
      plot.render();
    }
    top.draw = (p) => {
      const P = PARENTS[sel.value];
      if (P.pmf) {
        p.domain(P.xr[0], P.xr[1], 0, Math.max(...P.pmf.map((q) => q[1])) * 1.2);
        p.axes({ yn: 2, xticks: P.pmf.map((q) => q[0]) });
        p.bars(P.pmf.map((q) => q[0]), P.pmf.map((q) => q[1]), p.c.muted, P.xr[1] > 3 ? 1 : 0.4);
      } else {
        const xs = M.linspace(P.xr[0], P.xr[1], 300), ys = xs.map(P.pdf);
        p.domain(P.xr[0], P.xr[1], 0, Math.max(...ys) * 1.25);
        p.axes({ yn: 2 });
        p.area(xs, ys, p.c.muted, 0.18);
        p.line(xs, ys, p.c.muted, 2);
      }
      p.text("元の分布", p.R - 4, p.T + 8, { px: true, align: "right", color: p.c.ink2, size: 11 });
    };
    plot.draw = (p) => {
      const P = PARENTS[sel.value], n = nS.value;
      const [a, b] = P.xr;
      const se = P.sd / Math.sqrt(n);
      const xs = M.linspace(a, b, 400), ys = xs.map((x) => M.normPdf(x, P.mu, se));
      const bins = 50, w = (b - a) / bins;
      const counts = new Array(bins).fill(0);
      for (const m of means) {
        const i = Math.floor((m - a) / w);
        if (i >= 0 && i < bins) counts[i]++;
      }
      const dens = counts.map((c) => (means.length ? c / (means.length * w) : 0));
      const ymax = Math.max(Math.max(...ys), Math.max(...dens)) * 1.12;
      p.domain(a, b, 0, ymax);
      p.axes({ xlabel: "標本平均 X̄", ylabel: "密度" });
      p.hist(M.linspace(a, b, bins + 1), dens, p.c.s1, 0.85);
      p.line(xs, ys, p.c.s2, 2);
      p.vline(P.mu, p.c.muted, 1, [4, 3], "μ = " + f(P.mu, 2));
      if (!means.length) {
        out.innerHTML = "ボタンを押すと、元の分布から大きさ n の標本をとって平均を計算する操作をくり返します。";
      } else {
        out.innerHTML = `${means.length}回の標本平均：平均 <b>${f(M.mean(means), 3)}</b>（理論値 μ = ${f(P.mu, 3)}）、` +
          `標準偏差 <b>${f(M.sd(means), 3)}</b>（理論値 σ/√n = ${f(se, 3)}）`;
      }
    };
    reset();
  };

  /* ---------- 第14章 最尤推定（ベルヌーイ） ---------- */
  SIMS.mle = function (root) {
    const ui = panel(root);
    const nS = slider(ui, { label: "投げた回数 n", min: 1, max: 200, step: 1, value: 10 }, () => { kS.setMax(nS.value); plot.render(); });
    const kS = slider(ui, { label: "表が出た回数 k", min: 0, max: 10, step: 1, value: 7 }, () => plot.render());
    const lg = checkbox(ui, "対数尤度で表示する", false, () => plot.render());
    const plot = new Plot(root, { height: 300, label: "尤度関数" });
    const out = readout(root);
    plot.draw = (p) => {
      const n = nS.value, k = Math.min(kS.value, n);
      const hat = k / n;
      const ll = (t) => (k ? k * Math.log(t) : 0) + (n - k ? (n - k) * Math.log(1 - t) : 0);
      const llhat = ll(Math.min(Math.max(hat, 1e-12), 1 - 1e-12));
      const xs = M.linspace(0.0005, 0.9995, 800);
      if (lg.value) {
        const ys = xs.map((t) => ll(t) - llhat);
        p.domain(0, 1, -10, 0.8);
        p.axes({ xlabel: "表の確率 p", ylabel: "対数尤度（最大値を0にそろえる）" });
        p.line(xs, ys, p.c.s1, 2);
        p.hover = (t) => (t <= 0 || t >= 1 ? null : { x: t, lines: [`p = ${f(t, 3)}`, `log L(p) − log L(p̂) = ${f(ll(t) - llhat, 3)}`], points: [[t, Math.max(ll(t) - llhat, -10)]] });
      } else {
        const ys = xs.map((t) => Math.exp(ll(t) - llhat));
        p.domain(0, 1, 0, 1.12);
        p.axes({ xlabel: "表の確率 p", ylabel: "尤度（最大値を1にそろえる）" });
        p.area(xs, ys, p.c.s1, 0.14);
        p.line(xs, ys, p.c.s1, 2);
        p.hover = (t) => (t <= 0 || t >= 1 ? null : { x: t, lines: [`p = ${f(t, 3)}`, `L(p) / L(p̂) = ${f(Math.exp(ll(t) - llhat), 4)}`], points: [[t, Math.exp(ll(t) - llhat)]] });
      }
      p.vline(hat, p.c.s2, 1.5, [4, 3], "p̂ = k/n = " + f(hat, 3), hat > 0.7 ? "left" : "right");
      out.innerHTML = `最尤推定値 <b>p̂ = ${k}/${n} = ${f(hat, 3)}</b>　山の幅の目安（標準誤差）√(p̂(1−p̂)/n) = <b>${f(Math.sqrt(hat * (1 - hat) / n), 3)}</b>`;
    };
    plot.render();
  };

  /* ---------- 第15章 信頼区間 ---------- */
  SIMS.ci = function (root) {
    const MU = 50, SIGMA = 10;
    const ui = panel(root);
    const nS = slider(ui, { label: "標本の大きさ n", min: 2, max: 100, step: 1, value: 10 }, reset);
    const lv = select(ui, { label: "信頼係数", options: [["0.90", "90%"], ["0.95", "95%"], ["0.99", "99%"]], value: "0.95" }, reset);
    const bt = buttons(root);
    button(bt, "標本を100回とって区間をつくる", run, true);
    button(bt, "リセット", reset);
    const plot = new Plot(root, { height: 420, pad: [14, 16, 44, 40], label: "100本の信頼区間" });
    legend(root, [["s1", "真の平均を含む区間", "line"], ["red", "真の平均を含まない区間", "line"]]);
    const out = readout(root);
    let cur = [], total = 0, cover = 0;
    function reset() { cur = []; total = 0; cover = 0; plot.render(); }
    function run() {
      const n = nS.value, conf = +lv.value;
      const tq = M.tInv(1 - (1 - conf) / 2, n - 1);
      cur = [];
      for (let i = 0; i < 100; i++) {
        const xs = [];
        for (let j = 0; j < n; j++) xs.push(MU + SIGMA * M.randn());
        const m = M.mean(xs), s = M.sd(xs, 1);
        const half = tq * s / Math.sqrt(n);
        const ok = m - half <= MU && MU <= m + half;
        cur.push([m, m - half, m + half, ok]);
        total++; if (ok) cover++;
      }
      plot.render();
    }
    plot.draw = (p) => {
      p.domain(MU - 25, MU + 25, 0, 101);
      p.axes({ xlabel: "値", noY: true });
      const ctx = p.ctx;
      p.clip(() => {
        cur.forEach(([m, lo, hi, ok], i) => {
          const y = p.sy(100 - i);
          ctx.strokeStyle = ok ? p.c.s1 : p.c.red;
          ctx.lineWidth = ok ? 1.6 : 2.6;
          ctx.beginPath(); ctx.moveTo(p.sx(lo), y); ctx.lineTo(p.sx(hi), y); ctx.stroke();
          ctx.fillStyle = ok ? p.c.s1 : p.c.red;
          ctx.beginPath(); ctx.arc(p.sx(m), y, 2, 0, 2 * Math.PI); ctx.fill();
        });
      });
      p.vline(MU, p.c.ink2, 1.5, null, "真の平均 μ = 50");
      if (!cur.length) {
        out.innerHTML = "母集団は平均 50、標準偏差 10 の正規分布（実験者は平均を知らないとします）。ボタンを押すと、標本から t 分布を使った信頼区間を100回つくります。";
      } else {
        const k = cur.filter((c) => c[3]).length;
        out.innerHTML = `今回の100本のうち真の平均を含む区間：<b>${k}本</b>　` +
          `累計：<b>${cover} / ${total}（${pct(cover / total)}）</b>　← 信頼係数 ${pct(+lv.value, 0)} に近づく`;
      }
    };
    reset();
  };

  /* ---------- 第16章 検出力 ---------- */
  SIMS.power = function (root) {
    const ui = panel(root);
    const dS = slider(ui, { label: "効果量 d = (μ₁ − μ₀)/σ", min: 0, max: 1.5, step: 0.05, value: 0.5, fmt: (v) => v.toFixed(2) }, () => plot.render());
    const nS = slider(ui, { label: "標本の大きさ n", min: 1, max: 100, step: 1, value: 20 }, () => plot.render());
    const aS = select(ui, { label: "有意水準 α", options: [["0.01", "1%"], ["0.05", "5%"], ["0.10", "10%"]], value: "0.05" }, () => plot.render());
    const sd = select(ui, { label: "対立仮説", options: [["one", "片側 (μ > μ₀)"], ["two", "両側 (μ ≠ μ₀)"]], value: "one" }, () => plot.render());
    const plot = new Plot(root, { height: 300, label: "検定統計量の分布" });
    legend(root, [["muted", "帰無仮説のもとでの分布", "line"], ["s1", "対立仮説のもとでの分布", "line"], ["s2", "有意水準 α（第1種の過誤）"], ["s1", "検出力 1 − β"]]);
    const out = readout(root);
    plot.draw = (p) => {
      const d = dS.value, n = nS.value, a = +aS.value, two = sd.value === "two";
      const shift = d * Math.sqrt(n);
      const zc = two ? M.normInv(1 - a / 2) : M.normInv(1 - a);
      const x1 = Math.min(Math.max(4.5, shift + 4), 16);
      const xs = M.linspace(-4.5, x1, 700);
      const h0 = xs.map((x) => M.normPdf(x)), h1 = xs.map((x) => M.normPdf(x, shift, 1));
      p.domain(-4.5, x1, 0, 0.46);
      p.axes({ xlabel: "検定統計量 Z", ylabel: "密度" });
      const rej = (x) => (two ? Math.abs(x) >= zc : x >= zc);
      const seg = (ys, cond) => { const X = [], Y = []; xs.forEach((x, i) => { if (cond(x)) { X.push(x); Y.push(ys[i]); } }); return [X, Y]; };
      let [X, Y] = seg(h1, (x) => x >= zc);
      p.area(X, Y, p.c.s1, 0.35);
      if (two) { [X, Y] = seg(h1, (x) => x <= -zc); p.area(X, Y, p.c.s1, 0.35); }
      [X, Y] = seg(h0, (x) => x >= zc);
      p.area(X, Y, p.c.s2, 0.55);
      if (two) { [X, Y] = seg(h0, (x) => x <= -zc); p.area(X, Y, p.c.s2, 0.55); }
      p.line(xs, h0, p.c.muted, 2);
      p.line(xs, h1, p.c.s1, 2);
      p.vline(zc, p.c.ink2, 1.2, [4, 3], "棄却域 →");
      if (two) p.vline(-zc, p.c.ink2, 1.2, [4, 3], "← 棄却域", "left");
      const power = 1 - M.normCdf(zc - shift) + (two ? M.normCdf(-zc - shift) : 0);
      p.hover = (x) => ({ x, lines: [`Z = ${f(x, 2)}`, `H₀ の密度 ${f(M.normPdf(x), 3)}`, `H₁ の密度 ${f(M.normPdf(x, shift, 1), 3)}`, rej(x) ? "→ 棄却域" : "→ 採択域"] });
      out.innerHTML = `検出力 1 − β = <b class="sim-big">${pct(power)}</b>　第2種の過誤の確率 β = <b>${pct(1 - power)}</b>　` +
        `臨界値 ${two ? "±" : ""}${f(zc, 3)}　対立仮説のもとでの Z の平均 d√n = ${f(shift, 2)}`;
    };
    plot.render();
  };

  /* ---------- 第18章 最小二乗法 ---------- */
  SIMS.regression = function (root) {
    const INIT = [[1, 2.2], [2, 2.8], [3, 4.6], [4, 3.9], [5, 5.8], [6, 5.4], [7, 7.4], [8, 7.0]];
    let pts = INIT.map((q) => q.slice());
    const ui = panel(root);
    const aS = slider(ui, { label: "切片 a", min: -3, max: 8, step: "any", value: 3, fmt: (v) => v.toFixed(2) }, () => plot.render());
    const bS = slider(ui, { label: "傾き b", min: -1, max: 2, step: "any", value: 0.2, fmt: (v) => v.toFixed(2) }, () => plot.render());
    const bt = buttons(root);
    const ols = () => {
      const xs = pts.map((q) => q[0]), ys = pts.map((q) => q[1]);
      const mx = M.mean(xs), my = M.mean(ys);
      let sxy = 0, sxx = 0;
      for (let i = 0; i < xs.length; i++) { sxy += (xs[i] - mx) * (ys[i] - my); sxx += (xs[i] - mx) ** 2; }
      const b = sxx > 0 ? sxy / sxx : 0;
      return [my - b * mx, b];
    };
    button(bt, "最小二乗法で当てはめる", () => { const [a, b] = ols(); aS.value = a; bS.value = b; plot.render(); }, true);
    button(bt, "点を元に戻す", () => { pts = INIT.map((q) => q.slice()); plot.render(); });
    button(bt, "点をすべて消す", () => { pts = []; plot.render(); });
    const plot = new Plot(root, { height: (w) => w - 8, maxWidth: 460, pad: [12, 12, 36, 44], label: "散布図と回帰直線" });
    const out = readout(root);
    plot.canvas.addEventListener("click", (e) => {
      const r = plot.canvas.getBoundingClientRect();
      const x = plot.ix(e.clientX - r.left), y = plot.iy(e.clientY - r.top);
      if (x < 0 || x > 10 || y < 0 || y > 10) return;
      pts.push([+x.toFixed(2), +y.toFixed(2)]);
      plot.render();
    });
    plot.draw = (p) => {
      const a = aS.value, b = bS.value;
      p.domain(0, 10, 0, 10);
      p.axes({ xlabel: "x", ylabel: "y", xgrid: true });
      const ctx = p.ctx;
      let sse = 0;
      p.clip(() => {
        for (const [x, y] of pts) {
          const yh = a + b * x, e = y - yh;
          sse += e * e;
          const side = Math.abs(e);
          const dir = x + side > 10 ? -1 : 1;
          const X0 = p.sx(x), X1 = p.sx(x + dir * side), Y0 = p.sy(yh), Y1 = p.sy(y);
          ctx.fillStyle = rgba(p.c.s2, 0.13);
          ctx.strokeStyle = rgba(p.c.s2, 0.7);
          ctx.lineWidth = 1;
          ctx.fillRect(Math.min(X0, X1), Math.min(Y0, Y1), Math.abs(X1 - X0), Math.abs(Y1 - Y0));
          ctx.strokeRect(Math.min(X0, X1), Math.min(Y0, Y1), Math.abs(X1 - X0), Math.abs(Y1 - Y0));
        }
      });
      p.line([0, 10], [a, a + 10 * b], p.c.s1, 2.2);
      p.dots(pts.map((q) => q[0]), pts.map((q) => q[1]), p.c.ink, 4.5);
      let best = "";
      if (pts.length >= 2) {
        const [a0, b0] = ols();
        const smin = pts.reduce((s, [x, y]) => s + (y - a0 - b0 * x) ** 2, 0);
        best = `　（最小値は ${f(smin, 2)}：a = ${f(a0, 2)}, b = ${f(b0, 2)} のとき）`;
      }
      out.innerHTML = `直線 y = ${f(a, 2)} + ${f(b, 2)}x　残差平方和（オレンジの正方形の面積の合計）= <b class="sim-big">${f(sse, 2)}</b>${best}` +
        `<div class="sim-note">グラフをクリックすると点を追加できます。</div>`;
    };
    plot.render();
  };

  /* ---------- 第20章 ベイズ更新（ベータ・二項） ---------- */
  SIMS["bayes-coin"] = function (root) {
    const ui = panel(root);
    const aS = slider(ui, { label: "事前分布の a", min: 0.5, max: 20, step: 0.5, value: 2, fmt: (v) => v.toFixed(1) }, () => plot.render());
    const bS = slider(ui, { label: "事前分布の b", min: 0.5, max: 20, step: 0.5, value: 2, fmt: (v) => v.toFixed(1) }, () => plot.render());
    const tS = slider(ui, { label: "コインの真の表の確率 θ（本当は未知）", min: 0.05, max: 0.95, step: 0.05, value: 0.7, fmt: (v) => v.toFixed(2) }, () => plot.render());
    const bt = buttons(root);
    let H = 0, T = 0;
    const toss = (m) => { for (let i = 0; i < m; i++) { if (Math.random() < tS.value) H++; else T++; } plot.render(); };
    button(bt, "1回投げる", () => toss(1), true);
    button(bt, "10回投げる", () => toss(10));
    button(bt, "100回投げる", () => toss(100));
    button(bt, "リセット", () => { H = 0; T = 0; plot.render(); });
    const plot = new Plot(root, { height: 300, label: "事前分布と事後分布" });
    legend(root, [["muted", "事前分布", "dash"], ["s1", "事後分布", "line"], ["s2", "真の θ", "dash"]]);
    const out = readout(root);
    plot.draw = (p) => {
      const a = aS.value, b = bS.value, A = a + H, B = b + T;
      const xs = M.linspace(0.001, 0.999, 600);
      const pri = xs.map((x) => M.betaPdf(x, a, b)), post = xs.map((x) => M.betaPdf(x, A, B));
      const ymax = Math.min(Math.max(...post.slice(3, -3), ...pri.slice(3, -3)) * 1.12, 60);
      p.domain(0, 1, 0, ymax);
      p.axes({ xlabel: "θ（表が出る確率）", ylabel: "密度" });
      p.line(xs, pri, p.c.muted, 1.8, [5, 4]);
      p.area(xs, post, p.c.s1, 0.16);
      p.line(xs, post, p.c.s1, 2.2);
      p.vline(tS.value, p.c.s2, 1.5, [4, 3]);
      p.hover = (x) => (x <= 0 || x >= 1 ? null : { x, lines: [`θ = ${f(x, 3)}`, `事前 ${f(M.betaPdf(x, a, b), 3)}`, `事後 ${f(M.betaPdf(x, A, B), 3)}`], points: [[x, Math.min(M.betaPdf(x, A, B), ymax)]] });
      const lo = M.betaInv(0.025, A, B), hi = M.betaInv(0.975, A, B);
      out.innerHTML = `表 <b>${H}</b> 回・裏 <b>${T}</b> 回 → 事後分布 Be(${f(A, 1)}, ${f(B, 1)})<br>` +
        `事後平均 <b>${f(A / (A + B), 3)}</b>　95%信用区間 <b>[${f(lo, 3)}, ${f(hi, 3)}]</b>` +
        (H + T ? `　（参考：最尤推定値 ${f(H / (H + T), 3)}）` : "");
    };
    plot.render();
  };

  /* ============================================================
   * 起動
   * ============================================================ */
  function init() {
    document.querySelectorAll(".sim[data-sim]").forEach((el) => {
      if (el.dataset.ready) return;
      const fn = SIMS[el.dataset.sim];
      if (!fn) return;
      el.dataset.ready = "1";
      try {
        fn(el);
      } catch (e) {
        console.error(e);
        el.textContent = "シミュレーションを読み込めませんでした。";
      }
    });
  }

  function start() {
    if (window.document$ && typeof window.document$.subscribe === "function") window.document$.subscribe(init);
    else init();
    new MutationObserver(() => PLOTS.forEach((p) => p.render()))
      .observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();

  window.StatsSim = { M, SIMS };
})();
