/**
 * Sahne — kaydırmaya bağlı kare dizisi oynatıcı (2B tuval, WebGL gerekmez).
 *
 *  • Kareler yalnız sahne yaklaşınca, önce kaba (her 8. kare) sonra ara kareler
 *    olarak iner; eksik kare varsa en yakın iki kare arasında yumuşak geçiş çizilir.
 *  • Sahne uzaklaşınca ara kareler bellekten bırakılır (yalnız anahtar kareler kalır).
 *  • Çizim yalnız kare değişince yapılır; boşta hiçbir iş yapılmaz.
 *  • Video sahnesinde gerçek video, render edilmiş bloğun ön yüzüne homografiyle oturur.
 */
import { KARE_KOK, KOPRU_BASLA, EGIM_PX } from './ayarlar.js';
import { matrix3d } from './homografi.js';

const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
const smooth = (a, b, x) => {
  const t = clamp01((x - a) / (b - a));
  return t * t * (3 - 2 * t);
};
const easeInOut = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);

/** Ortak indirme kuyruğu: öncelikli, eş zamanlı sınırı olan. */
export class Kuyruk {
  constructor(limit) {
    this.limit = limit;
    this.active = 0;
    this.jobs = [];
  }

  add(job) {
    this.jobs.push(job);
    this.pump();
  }

  drop(owner) {
    this.jobs = this.jobs.filter((j) => j.owner !== owner);
  }

  pump() {
    while (this.active < this.limit && this.jobs.length) {
      let bi = 0;
      for (let i = 1; i < this.jobs.length; i++) if (this.jobs[i].pri > this.jobs[bi].pri) bi = i;
      const job = this.jobs.splice(bi, 1)[0];
      this.active++;
      job.run().finally(() => {
        this.active--;
        this.pump();
      });
    }
  }
}

export class Sahne {
  /**
   * @param {HTMLElement} el      [data-sahne] bölümü
   * @param {object} cfg          ayarlar.SAHNELER öğesi
   * @param {object} meta         window.EGE_KARELER[id] → { d: {...}, m: {...} }
   * @param {object} ortak        { kuyruk, kick(), nokta(id, btn, sahne), dikey(), azHareket }
   */
  constructor(el, cfg, meta, ortak) {
    this.el = el;
    this.cfg = cfg;
    this.id = cfg.id;
    this.meta = meta || {};
    this.ortak = ortak;
    this.sabit = el.querySelector('.eg-sahne__sabit');
    this.katman = el.querySelector('.eg-sahne__katman');
    this.canvas = el.querySelector('.eg-sahne__tuval');
    this.ctx = this.canvas.getContext('2d', { alpha: false });
    this.kopru = el.querySelector('.eg-sahne__kopru');
    this.noktaKatman = el.querySelector('.eg-noktalar');
    this.videoKap = el.querySelector('.eg-video');
    this.video = this.videoKap ? this.videoKap.querySelector('video') : null;
    this.giris = el.querySelector('.eg-giris'); // açılış metni: kaydırma başlayınca kaybolur
    this.girisOpacity = -1;

    this.variant = '';
    this.v = null; // seçili varyantın metası
    this.frames = [];
    this.loading = new Set();
    this.failed = new Set();
    this.loadedCount = 0;

    this.p = 0;
    this.target = 0;
    this.visible = false;
    this.near = false;
    this.drawnKey = '';
    this.noktalar = new Map();
    this.tilt = { x: 0, y: 0, tx: 0, ty: 0 };
    this.fit = { s: 1, dx: 0, dy: 0, cw: 1, ch: 1, dpr: 1 };
    this.vsize = { w: -1, h: -1 };
    this.lastTransform = '';
    this.videoOpacity = -1;
  }

  /** Varyant (d: masaüstü 16:9, m: telefon dikey) seçimi; yoksa masaüstüne düşer. */
  setVariant(want) {
    const pick = this.meta[want] && this.meta[want].mevcut && this.meta[want].mevcut.length ? want : 'd';
    if (pick === this.variant) return;
    this.variant = pick;
    this.v = this.meta[pick] || { n: 1, res: [1600, 900], mevcut: [], hotspots: {}, face: {} };
    this.ortak.kuyruk.drop(this);
    this.frames = new Array(this.v.n).fill(null);
    this.loading.clear();
    this.failed.clear();
    this.loadedCount = 0;
    this.drawnKey = '';
    this.vsize = { w: -1, h: -1 };
    this.layout();
    if (this.near) this.ensure();
  }

  frameUrl(i) {
    return `${KARE_KOK}/${this.id}/${this.variant}/${String(i).padStart(3, '0')}.webp`;
  }

  /** Görünürlüğe yakınsa kareleri kaba → ince sırayla kuyruğa ekler. */
  ensure() {
    if (!this.v) return;
    const exists = new Set(this.v.mevcut);
    const order = [];
    const seen = new Set();
    for (const step of [8, 4, 2, 1]) {
      for (let i = 0; i < this.v.n; i += step) {
        if (!seen.has(i)) {
          seen.add(i);
          order.push([i, step]);
        }
      }
    }
    // son kare ("sonuç") ilk kareden hemen sonra iner
    const li = order.findIndex(([i]) => i === this.v.n - 1);
    if (li > 1) order.splice(1, 0, order.splice(li, 1)[0]);
    for (const [i, step] of order) {
      if (!exists.has(i) || this.frames[i] || this.loading.has(i) || this.failed.has(i)) continue;
      this.loading.add(i);
      const pri = (this.visible ? 100 : 10) + (step === 8 ? 8 : step === 4 ? 4 : step === 2 ? 2 : 1);
      this.ortak.kuyruk.add({ owner: this, pri, run: () => this.load(i) });
    }
  }

  load(i) {
    const variant = this.variant;
    return new Promise((resolve) => {
      const img = new Image();
      img.decoding = 'async';
      img.onload = () => {
        const done = () => {
          if (variant === this.variant) {
            this.frames[i] = img;
            this.loadedCount++;
            this.loading.delete(i);
            this.drawnKey = '';
            this.ortak.kick();
          }
          resolve();
        };
        if (img.decode) img.decode().then(done, done);
        else done();
      };
      img.onerror = () => {
        this.loading.delete(i);
        this.failed.add(i);
        resolve();
      };
      img.src = this.frameUrl(i);
    });
  }

  /** Uzaklaşınca ara kareleri bırak (bellek); anahtar kareler kalır. */
  release() {
    this.ortak.kuyruk.drop(this);
    this.loading.clear();
    for (let i = 0; i < this.frames.length; i++) {
      if (this.frames[i] && i % 8 !== 0 && i !== this.frames.length - 1) {
        this.frames[i] = null;
        this.loadedCount--;
      }
    }
    this.drawnKey = '';
  }

  /** Tuval ve "cover" yerleşimi (yalnız boyut değişince). */
  layout() {
    const cw = Math.max(1, this.sabit.clientWidth);
    const ch = Math.max(1, this.sabit.clientHeight);
    const dpr = Math.min(1.25, window.devicePixelRatio || 1);
    const [iw, ih] = this.v ? this.v.res : [1600, 900];
    const s = Math.max(cw / iw, ch / ih);
    this.fit = { s, dx: (cw - iw * s) / 2, dy: (ch - ih * s) / 2, cw, ch, dpr, iw, ih };
    const bw = Math.round(cw * dpr);
    const bh = Math.round(ch * dpr);
    if (this.canvas.width !== bw || this.canvas.height !== bh) {
      this.canvas.width = bw;
      this.canvas.height = bh;
    }
    this.drawnKey = '';
    this.vsize = { w: -1, h: -1 };
  }

  /** Kaydırma konumundan hedef ilerleme (okuma yapılır, yazma yapılmaz). */
  measure(vh) {
    const r = this.el.getBoundingClientRect();
    const span = r.height - vh;
    this.target = span > 0 ? clamp01(-r.top / span) : 0;
    if (this.ortak.azHareket) this.target = this.cfg.video ? 0 : 1;
    this.visible = r.bottom > 0 && r.top < vh;
    return this.visible;
  }

  /** Yumuşak yaklaşma; hâlâ hareket varsa true. */
  step(dt) {
    let moving = false;
    const k = 1 - Math.exp(-this.ortak.yumusaklik * dt);
    const d = this.target - this.p;
    if (Math.abs(d) > 0.00025) {
      this.p += d * k;
      moving = true;
    } else {
      this.p = this.target;
    }
    const t = this.tilt;
    const kt = 1 - Math.exp(-5 * dt);
    if (Math.abs(t.tx - t.x) > 0.05 || Math.abs(t.ty - t.y) > 0.05) {
      t.x += (t.tx - t.x) * kt;
      t.y += (t.ty - t.y) * kt;
      moving = true;
    }
    return moving;
  }

  frameFloat() {
    const g = this.cfg.giris || 0;
    const fp = g ? clamp01((this.p - g) / (1 - g)) : this.p;
    return fp * Math.max(0, this.v.n - 1);
  }

  /** Yüklü en yakın iki kare ve aradaki oran. */
  neighbors(f) {
    const n = this.frames.length;
    let a = -1;
    let b = -1;
    for (let i = Math.floor(f); i >= 0; i--) if (this.frames[i]) {
      a = i;
      break;
    }
    for (let i = Math.ceil(f); i < n; i++) if (this.frames[i]) {
      b = i;
      break;
    }
    if (a < 0 && b < 0) return null;
    if (a < 0) return [b, b, 0];
    if (b < 0) return [a, a, 0];
    return [a, b, b === a ? 0 : (f - a) / (b - a)];
  }

  render() {
    if (!this.v) return;
    const f = this.frameFloat();
    const nb = this.neighbors(f);
    if (nb) {
      const [a, b, t] = nb;
      const key = `${a}|${b}|${t.toFixed(3)}`;
      if (key !== this.drawnKey) {
        this.drawnKey = key;
        const { s, dx, dy, dpr, iw, ih } = this.fit;
        const ctx = this.ctx;
        ctx.globalAlpha = 1;
        ctx.drawImage(this.frames[a], dx * dpr, dy * dpr, iw * s * dpr, ih * s * dpr);
        if (b !== a && t > 0.004) {
          ctx.globalAlpha = t;
          ctx.drawImage(this.frames[b], dx * dpr, dy * dpr, iw * s * dpr, ih * s * dpr);
          ctx.globalAlpha = 1;
        }
        this.el.classList.add('is-hazir');
      }
    }
    this.renderHotspots(f);
    if (this.videoKap) this.renderVideo(f);
    if (this.giris) {
      const go = this.ortak.azHareket ? 1 : Math.round((1 - smooth(0.0, 0.07, this.p)) * 1000) / 1000;
      if (go !== this.girisOpacity) {
        this.giris.style.opacity = String(go);
        this.giris.style.visibility = go < 0.01 ? 'hidden' : '';
        this.girisOpacity = go;
      }
    }
    if (this.kopru) {
      const o = smooth(KOPRU_BASLA, 1, this.p).toFixed(3);
      if (this.kopru.style.opacity !== o) this.kopru.style.opacity = o;
    }
    const tr = EGIM_PX && !this.ortak.azHareket ? `translate3d(${this.tilt.x.toFixed(2)}px,${this.tilt.y.toFixed(2)}px,0) scale(1.03)` : '';
    if (tr !== this.lastTransform) {
      this.katman.style.transform = tr;
      this.lastTransform = tr;
    }
  }

  /** Kare koordinatı (0..1) → sahne pikseli */
  toPx(u, v) {
    const { s, dx, dy, iw, ih } = this.fit;
    return [dx + u * iw * s, dy + v * ih * s];
  }

  renderHotspots(f) {
    const hs = this.v.hotspots || {};
    const fa = Math.floor(f);
    const fb = Math.min(this.v.n - 1, fa + 1);
    const t = f - fa;
    const A = hs[fa];
    const B = hs[fb];
    const seen = new Set();
    const ids = new Set([...(A ? Object.keys(A) : []), ...(B ? Object.keys(B) : [])]);
    for (const id of ids) {
      const pa = A && A[id];
      const pb = B && B[id];
      let u;
      let v;
      if (pa && pb) {
        u = pa[0] + (pb[0] - pa[0]) * t;
        v = pa[1] + (pb[1] - pa[1]) * t;
      } else if ((pa && t < 0.5) || (pb && t >= 0.5)) {
        [u, v] = pa || pb;
      } else continue;
      let btn = this.noktalar.get(id);
      if (!btn) {
        btn = this.ortak.noktaOlustur(id, this);
        this.noktaKatman.appendChild(btn);
        this.noktalar.set(id, btn);
      }
      const [x, y] = this.toPx(u, v);
      btn.style.transform = `translate3d(${x.toFixed(1)}px,${y.toFixed(1)}px,0)`;
      btn.classList.remove('is-gizli');
      btn.tabIndex = 0;
      seen.add(id);
    }
    for (const [id, btn] of this.noktalar) {
      if (!seen.has(id) && !btn.classList.contains('is-gizli')) {
        btn.classList.add('is-gizli');
        btn.tabIndex = -1;
        this.ortak.noktaGizlendi(id, this);
      }
    }
  }

  faceAt(i) {
    const face = this.v.face || {};
    let k = i;
    if (!face[k]) {
      // en yakın kayıtlı kare
      let best = null;
      for (const key of Object.keys(face)) if (best === null || Math.abs(+key - i) < Math.abs(best - i)) best = +key;
      if (best === null) return null;
      k = best;
    }
    return face[k].map(([u, v]) => this.toPx(u, v));
  }

  renderVideo(f) {
    const g = this.cfg.giris || 0;
    const q0 = this.faceAt(0);
    if (!q0) return;
    const r0 = { x: q0[0][0], y: q0[0][1], w: q0[1][0] - q0[0][0], h: q0[3][1] - q0[0][1] };
    let w;
    let h;
    let transform;
    let opacity = 1;
    if (this.p <= g || this.ortak.azHareket) {
      // 1. aşama: tam ekran video, bloğun ön yüzüyle aynı banda iner (bozulma yok: boyut değişir)
      const k = this.ortak.azHareket ? 0 : easeInOut(clamp01(this.p / g));
      const R = {
        x: r0.x * k,
        y: r0.y * k,
        w: this.fit.cw + (r0.w - this.fit.cw) * k,
        h: this.fit.ch + (r0.h - this.fit.ch) * k,
      };
      w = R.w;
      h = R.h;
      transform = `translate3d(${R.x.toFixed(2)}px,${R.y.toFixed(2)}px,0)`;
    } else {
      // 2. aşama: video, dönen bloğun ön yüzüne projektif olarak yapışır
      const fa = Math.floor(f);
      const fb = Math.min(this.v.n - 1, fa + 1);
      const t = f - fa;
      const qa = this.faceAt(fa);
      const qb = this.faceAt(fb) || qa;
      const q = qa.map((p, i) => [p[0] + (qb[i][0] - p[0]) * t, p[1] + (qb[i][1] - p[1]) * t]);
      w = r0.w;
      h = r0.h;
      transform = matrix3d(w, h, q);
      const fp = f / Math.max(1, this.v.n - 1);
      opacity = 1 - smooth(0.2, 0.46, fp);
    }
    if (Math.abs(w - this.vsize.w) > 0.5 || Math.abs(h - this.vsize.h) > 0.5) {
      this.videoKap.style.width = `${w.toFixed(1)}px`;
      this.videoKap.style.height = `${h.toFixed(1)}px`;
      this.vsize = { w, h };
    }
    this.videoKap.style.transform = transform;
    const o = Math.round(opacity * 1000) / 1000;
    if (o !== this.videoOpacity) {
      this.videoKap.style.opacity = String(o);
      this.videoOpacity = o;
    }
    // görünmüyorsa videoyu durdur (çözme maliyeti olmasın)
    if (this.video) {
      const shouldPlay = this.visible && o > 0.01 && !this.ortak.azHareket;
      if (shouldPlay && this.video.paused) this.video.play().catch(() => {});
      else if (!shouldPlay && !this.video.paused) this.video.pause();
    }
  }

  setTilt(nx, ny) {
    if (!EGIM_PX || this.ortak.azHareket) return;
    this.tilt.tx = -nx * EGIM_PX;
    this.tilt.ty = -ny * EGIM_PX * 0.6;
  }
}
