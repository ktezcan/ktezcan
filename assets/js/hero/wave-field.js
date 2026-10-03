/**
 * WaveField — 2B dalga denklemi (yükseklik alanı) simülasyonu.
 * Three.js'ten bağımsızdır; yalnızca Float32Array üzerinde çalışır.
 *
 *   ∂²h/∂t² = c²·∇²h − γ·∂h/∂t + ν·∇²(∂h/∂t)
 *
 * c: yayılma hızı, γ: sönüm, ν: viskozite (ince kırışıklığı yumuşatır).
 * Yarı-örtük Euler + CFL güvenli alt adımlar → kare hızından bağımsız
 * (60 Hz, 120 Hz veya takılan bir karede aynı fiziksel davranış).
 * Kenarlarda "sünger" bant dalgaları yutar; yapay yansıma oluşmaz.
 * Enerji eşiğin altına düşünce alan "uyur" ve hiç CPU harcamaz.
 */
export class WaveField {
  /**
   * @param {object} o
   * @param {number} o.xMin  Alanın dünya koordinatındaki sol kenarı
   * @param {number} o.zMin  Alanın dünya koordinatındaki uzak kenarı
   * @param {number} o.width
   * @param {number} o.depth
   * @param {number} o.cell  Hücre boyu (dünya birimi)
   */
  constructor({ xMin, zMin, width, depth, cell, speed, damping, viscosity, sponge, sleepEpsilon }) {
    this.cols = Math.max(16, Math.round(width / cell));
    this.rows = Math.max(16, Math.round(depth / cell));
    this.xMin = xMin;
    this.zMin = zMin;
    this.width = width;
    this.depth = depth;
    this.dx = width / this.cols; // kare olmayan hücreler için ortalama alınır
    this.dz = depth / this.rows;

    this.speed = speed;
    this.viscosity = viscosity;
    this.sleepEpsilon = sleepEpsilon;

    const n = this.cols * this.rows;
    this.h = new Float32Array(n);
    this.v = new Float32Array(n);
    this.vNext = new Float32Array(n);
    this.damp = new Float32Array(n);

    // Sönüm haritası: iç bölgede sabit, kenara yaklaştıkça artan sünger.
    const { cols, rows } = this;
    for (let j = 0; j < rows; j++) {
      for (let i = 0; i < cols; i++) {
        const edge = Math.min(i, j, cols - 1 - i, rows - 1 - j);
        const s = edge < sponge ? 1 - edge / sponge : 0;
        this.damp[j * cols + i] = damping + s * s * 7.5;
      }
    }

    // CFL kararlılık sınırı: c·Δt/Δx ≤ 1/√2 (güvenlik payıyla)
    const minCell = Math.min(this.dx, this.dz);
    this.maxStep = Math.min(1 / 60, (0.5 * minCell) / speed);

    this.awake = false;
    this.dirty = true; // GPU'ya yüklenmesi gereken değişiklik var mı
    this._quiet = 0;
  }

  /** Dünya koordinatını hücre koordinatına çevirir. */
  toCell(x, z) {
    return [((x - this.xMin) / this.width) * this.cols - 0.5, ((z - this.zMin) / this.depth) * this.rows - 0.5];
  }

  /**
   * Yumuşak çekirdekli itki uygular (hız alanına eklenir).
   * @param {number} x       Dünya X
   * @param {number} z       Dünya Z
   * @param {number} amount  Hız katkısı (negatif = yüzeyi bastırır)
   * @param {number} radius  Dünya birimi
   */
  impulse(x, z, amount, radius) {
    if (!amount) return;
    const [ci, cj] = this.toCell(x, z);
    const ri = radius / this.dx;
    const rj = radius / this.dz;
    const i0 = Math.max(1, Math.floor(ci - ri));
    const i1 = Math.min(this.cols - 2, Math.ceil(ci + ri));
    const j0 = Math.max(1, Math.floor(cj - rj));
    const j1 = Math.min(this.rows - 2, Math.ceil(cj + rj));
    if (i0 > i1 || j0 > j1) return;

    const { v, cols } = this;
    for (let j = j0; j <= j1; j++) {
      const dj = (j - cj) / rj;
      for (let i = i0; i <= i1; i++) {
        const di = (i - ci) / ri;
        const q = 1 - (di * di + dj * dj);
        if (q > 0) v[j * cols + i] += amount * q * q; // (1−r²)² çekirdeği: keskin kenar yok
      }
    }
    this.awake = true;
    this._quiet = 0;
  }

  /**
   * Simülasyonu dt saniye ilerletir.
   * @returns {boolean} alan değiştiyse true (GPU'ya yükleme gerekir)
   */
  step(dt) {
    if (!this.awake) return false;

    const steps = Math.max(1, Math.ceil(dt / this.maxStep));
    const h = dt / steps;
    let peak = 0;
    for (let s = 0; s < steps; s++) peak = this._substep(h);

    if (peak < this.sleepEpsilon) {
      this._quiet += dt;
      if (this._quiet > 0.4) {
        this.h.fill(0);
        this.v.fill(0);
        this.awake = false;
      }
    } else {
      this._quiet = 0;
    }
    this.dirty = true;
    return true;
  }

  _substep(dt) {
    const { cols, rows, h, v, vNext, damp } = this;
    const kx = (this.speed * this.speed) / (this.dx * this.dx);
    const kz = (this.speed * this.speed) / (this.dz * this.dz);
    const nx = this.viscosity / (this.dx * this.dx);
    const nz = this.viscosity / (this.dz * this.dz);
    let peak = 0;

    // Hız güncellemesi (iç hücreler; kenarlar sabit h = 0)
    for (let j = 1; j < rows - 1; j++) {
      const row = j * cols;
      for (let i = 1; i < cols - 1; i++) {
        const k = row + i;
        const hc = h[k];
        const vc = v[k];
        const lapH = (h[k - 1] + h[k + 1] - 2 * hc) * kx + (h[k - cols] + h[k + cols] - 2 * hc) * kz;
        const lapV = (v[k - 1] + v[k + 1] - 2 * vc) * nx + (v[k - cols] + v[k + cols] - 2 * vc) * nz;
        vNext[k] = vc + (lapH + lapV - damp[k] * vc) * dt;
      }
    }

    // Konum güncellemesi + tepe değeri (uyku tespiti için)
    for (let j = 1; j < rows - 1; j++) {
      const row = j * cols;
      for (let i = 1; i < cols - 1; i++) {
        const k = row + i;
        const nv = vNext[k];
        v[k] = nv;
        const nh = h[k] + nv * dt;
        h[k] = nh;
        const a = nh < 0 ? -nh : nh;
        if (a > peak) peak = a;
      }
    }
    return peak;
  }

  /** Alanı sıfırlar (ör. yeniden başlatma). */
  reset() {
    this.h.fill(0);
    this.v.fill(0);
    this.awake = false;
    this.dirty = true;
  }
}
