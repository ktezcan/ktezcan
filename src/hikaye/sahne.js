/**
 * Sahne — kaydırmaya bağlı kare dizisi oynatıcı (2B tuval, WebGL gerekmez).
 *
 *  • Bellek pencerelidir: etkin sahnede odak karenin ±PENCERE karesi ImageBitmap olarak çözülü tutulur,
 *    pencere dışı kareler close() ile bırakılır. Komşu sahnelerde yalnız anahtar kareler (her 8.) ve
 *    dikişe yakın kareler kalır; uzak sahnelerde hiçbir şey. (Eski sürüm sahneyi komple tutuyordu: ≈2,9 GB.)
 *  • Kare seti seyrek olabilir (render sürerken pakette her 8. kare vardır): eksik kareler en yakın iki
 *    yüklü kare arasında erime ile doldurulur; erime ortaya sıkıştırılır, kaydırma durunca en yakın kareye oturur.
 *  • Çizim yalnız kare değişince yapılır; boşta hiçbir iş yapılmaz.
 *  • Finale parçasının kendi karesi yoktur: konak sahne (s5) son karesini çizerken final.js 2B efektini üstüne çizer.
 */
import {
  KARE_KOK, KOPRU_BASLA, EGIM_PX, DPR_ENFAZLA, PENCERE, ANAHTAR_ADIM, KOMSU_KARE, MAKS_BOSLUK, HIZLI_ESIK,
} from './ayarlar.js';

const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
const smooth = (a, b, x) => {
  const t = clamp01((x - a) / (b - a));
  return t * t * (3 - 2 * t);
};

/** Çözülmüş kare belleğini geri ver (ImageBitmap.close; düz <img> yedeğinde işlem yok). */
const birak = (b) => {
  if (b && typeof b.close === 'function') b.close();
};

/** Sayısal anahtarlı kaydın (kare → değer) sıralı anahtar listesi. */
const siraliAnahtar = (o) => Object.keys(o || {}).map(Number).sort((x, y) => x - y);

/** f'yi çevreleyen anahtarlar: [alt (≤ f), üst (≥ f)] ; yoksa -1. */
function cevre(keys, f) {
  let lo = -1;
  let hi = -1;
  for (let i = 0; i < keys.length; i++) {
    if (keys[i] <= f) lo = keys[i];
    if (keys[i] >= f) {
      hi = keys[i];
      break;
    }
  }
  return [lo, hi];
}

/** Ortak indirme kuyruğu: öncelikli, eş zamanlı sınırı olan (limit sayı ya da her seferinde sorulan işlev). */
export class Kuyruk {
  constructor(limit) {
    this.limitFn = typeof limit === 'function' ? limit : () => limit;
    this.active = 0;
    this.jobs = [];
  }

  add(job) {
    this.jobs.push(job);
    this.pump();
  }

  /** Sahibin henüz başlamamış işlerini kuyruktan çıkarır; çıkarılanları döndürür (sahibi 'iniyor' kaydını silebilsin). */
  drop(owner) {
    const atilan = this.jobs.filter((j) => j.owner === owner);
    if (atilan.length) this.jobs = this.jobs.filter((j) => j.owner !== owner);
    return atilan;
  }

  pump() {
    while (this.active < this.limitFn() && this.jobs.length) {
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
   * @param {HTMLElement} el      [data-sahne] bölümü (finale ve eksik parçalarda kanvassız olabilir)
   * @param {object} cfg          ayarlar.SAHNELER öğesi
   * @param {object} meta         window.EGE_KARELER[id] → { d: {...}, m: {...} }
   * @param {object} ortak        { kuyruk, kick(), noktaOlustur(), azHareket, hareketli, final, ... }
   */
  constructor(el, cfg, meta, ortak) {
    this.el = el;
    this.cfg = cfg;
    this.id = cfg.id;
    this.meta = meta || {};
    this.ortak = ortak;
    // tek akış: sahne katmanı ortak yapışkan sahnenin içinde, tüm alanı kaplar
    this.sabit = el;
    this.perde = el.querySelector('.eg-sahne__perde');
    this.vuruslar = Array.from(el.querySelectorAll('[data-bas]')).map((v) => ({ el: v, bas: +v.dataset.bas, son: +v.dataset.son, acik: false }));
    this.alfa = -1;
    this.hedefAlfa = 0;
    this.katman = el.querySelector('.eg-sahne__katman');
    this.canvas = el.querySelector('.eg-sahne__tuval');
    this.ctx = this.canvas ? this.canvas.getContext('2d', { alpha: false }) : null;
    // opak kanvas çizilene dek siyah görünür ve altındaki poster'i örter: ilk kare çizilene kadar gizli
    this.hazir = false;
    if (this.canvas) this.canvas.style.visibility = 'hidden';
    this.kopru = el.querySelector('.eg-sahne__kopru');
    this.kopruAcik = cfg.kopru !== false;
    this.noktaKatman = el.querySelector('.eg-noktalar');
    this.kalem = el.querySelector('[data-kalem]'); // eskiz kalemi (meta.pen: kalem ucu konumu)
    this.kalemGorunur = true;
    this.giris = el.querySelector('.eg-giris'); // açılış metni: kaydırma başlayınca kaybolur
    this.girisOpacity = -1;

    this.variant = '';
    this.v = null; // seçili varyantın metası
    this.frames = []; // çözülmüş kareler (ImageBitmap | null)
    this.loading = new Set();
    this.failed = new Set();
    this.loadedCount = 0;
    this.nesil = 0; // varyant/çözme ölçeği değişince uçuşta kalan yüklemeler çöpe gider
    this.cozOlcek = 0; // kare çözme ölçeği (≤ 1): küçük ekranda bitmap'ler küçültülerek çözülür
    this.var = null; // var olan kare indeksleri (seyrek set) ya da null = hepsi
    this.hsAnahtar = [];
    this.kalemAnahtar = [];

    // bellek penceresi: rol 'aktif' | 'ileri' (etkinden sonraki) | 'geri' (önceki) | 'sabit' (hareket azaltma) | 'uzak'
    this.rol = 'uzak';
    this.izin = false;
    this.yaricap = PENCERE;
    this.odak = -1000;
    this.yogunluk = 1; // var olan kare / toplam kare (setVariant)
    this.odakYon = 0; // odağın son hareket yönü (+1 ileri, -1 geri): hareket yönündeki kareler önce iner
    this.tutFn = () => false;
    this.planKirli = true;

    this.p = 0; // gösterilen ilerleme (akış genelinde yumuşatılmış)
    this.hamP = 0; // ham kaydırma hedefi (yükleme penceresini bu belirler)
    this.target = 0;
    this.visible = false;
    this.near = false;
    this.wasVisible = false;
    this.drawnKey = '';
    this.noktalar = new Map();
    this.tilt = { x: 0, y: 0, tx: 0, ty: 0 };
    this.fit = { s: 1, dx: 0, dy: 0, cw: 1, ch: 1, dpr: 1, iw: 1600, ih: 900 };
    this.lastTransform = '';
    this.fGoster = -1; // gösterilen kare konumu (seyrek sette durunca en yakın kareye oturur)
    this.sonF = -1; // en son çizimdeki gerçek kare konumu
    this.yon = 1; // kaydırmanın son yönü (+1 ileri, -1 geri)
    this.hiz = 0; // kare/çizim cinsinden yumuşatılmış kaydırma hızı
    this.fHedef = 0;
    this.seyrek = false;
    this.finaleP = -1; // konak sahnede: finale ilerlemesi (0..1), finale dışında -1
    this.finaleHata = false;
  }

  /** Varyant (d: masaüstü 16:9, m: telefon dikey) seçimi; yoksa masaüstüne düşer. */
  setVariant(want) {
    if (!this.canvas) return; // kanvassız parça (finale)
    // yarım kalmış bir set (render sürerken paketlenmiş) sahneyi ortada dondurur:
    // yalnız baştan sona kapsayan set seçilir (ilk + son kare, en fazla MAKS_BOSLUK karelik boşluk)
    const tam = (k) => {
      const m = this.meta[k];
      const s = m && m.mevcut;
      if (!s || !s.length || s[0] !== 0 || s[s.length - 1] !== m.n - 1) return false;
      for (let i = 1; i < s.length; i++) if (s[i] - s[i - 1] > MAKS_BOSLUK) return false;
      return true;
    };
    const pick = tam(want) ? want : 'd';
    if (pick === this.variant) return;
    this.sifirla();
    this.variant = pick;
    this.v = this.meta[pick] || { n: 1, res: [1600, 900], mevcut: [], hotspots: {}, pen: {} };
    this.var = Array.isArray(this.v.mevcut) ? new Set(this.v.mevcut) : null;
    // var olan kare yoğunluğu (telefon seti her 2. kare → 0,5): pencere yarıçapı var olan kare cinsinden sayılır
    this.yogunluk = this.var ? Math.max(0.05, this.var.size / Math.max(1, this.v.n)) : 1;
    this.hsAnahtar = siraliAnahtar(this.v.hotspots);
    this.kalemAnahtar = siraliAnahtar(this.v.pen);
    this.frames = new Array(this.v.n).fill(null);
    this.cozOlcek = 0;
    this.fGoster = -1;
    this.layout();
    this.planKirli = true;
  }

  /** Tüm kareleri bırak, uçuştaki yüklemeleri geçersiz kıl. */
  sifirla() {
    this.ortak.kuyruk.drop(this);
    for (let i = 0; i < this.frames.length; i++) {
      const b = this.frames[i];
      this.frames[i] = null;
      birak(b);
    }
    this.nesil++;
    this.loading.clear();
    this.failed.clear();
    this.loadedCount = 0;
    this.drawnKey = '';
    this.odak = -1000;
    this.planKirli = true;
  }

  frameUrl(i) {
    return `${KARE_KOK}/${this.id}/${this.variant}/${String(i).padStart(3, '0')}.webp`;
  }

  /** i. kare pakette var mı? (seyrek set; 'mevcut' yoksa hepsi var sayılır) */
  varMi(i) {
    return !this.var || this.var.has(i);
  }

  /** Mevcut role göre tutulacak kareler (anahtar kareler her zaman; pencere rolüne göre). */
  tutYap() {
    const n = this.v.n;
    const anahtar = (i) => i % ANAHTAR_ADIM === 0 || i === n - 1;
    if (this.rol === 'uzak') return () => false;
    if (this.rol === 'sabit') return (i) => i === n - 1;
    const r = this.yaricap;
    let lo = this.odak - r;
    let hi = this.odak + r;
    if (this.rol === 'aktif') {
      // uçlarda pencere kısalmasın: taşan kısım karşı yana eklenir (ilk açılışta 0..2·PENCERE = ilk 32 kare)
      if (lo < 0) hi -= lo;
      if (hi > n - 1) lo -= hi - (n - 1);
    }
    return (i) => anahtar(i) || (i >= lo && i <= hi);
  }

  /**
   * Akış denetleyicisi her karede çağırır: sahnenin bellek rolü. Rol, izin ya da odak değişince
   * fazla kareler bırakılır ve eksikler öncelik sırasıyla kuyruğa alınır.
   * @param {string} rol     aktif | ileri | geri | sabit | uzak
   * @param {boolean} izin   false ise yeni kare indirilmez (komşunun ön yüklemesi bekletilir), eldekiler kalır
   * @param {number} [yaricap]  pencere yarıçapı (kare)
   */
  rolVer(rol, izin = true, yaricap) {
    if (!this.v) {
      this.rol = rol;
      return;
    }
    const n = this.v.n;
    // yarıçap var olan kare cinsinden verilir (±PENCERE kare çözülü); dizin birimine çevrilir
    const r = Math.round((yaricap != null ? yaricap : rol === 'aktif' ? PENCERE : KOMSU_KARE) / this.yogunluk);
    let odak = 0;
    if (rol === 'aktif') odak = Math.round(this.hamP * (n - 1));
    else if (rol === 'geri' || rol === 'sabit') odak = n - 1;
    const sabitOdak = rol !== 'aktif';
    const degisti =
      this.planKirli || rol !== this.rol || izin !== this.izin || r !== this.yaricap || (!sabitOdak && Math.abs(odak - this.odak) >= 2) || (sabitOdak && odak !== this.odak);
    if (!degisti) return;
    if (rol === 'aktif' && Math.abs(odak - this.odak) < 200 && odak !== this.odak) this.odakYon = odak > this.odak ? 1 : -1;
    this.rol = rol;
    this.izin = izin;
    this.yaricap = r;
    this.odak = odak;
    this.planKirli = false;
    this.near = rol !== 'uzak';
    this.planla();
  }

  /** Pencere dışını bırak, penceredeki eksikleri öncelik sırasıyla kuyruğa ekle. */
  planla() {
    const n = this.v.n;
    const tut = this.tutYap();
    this.tutFn = tut;
    for (let i = 0; i < this.frames.length; i++) {
      if (this.frames[i] && !tut(i)) {
        const b = this.frames[i];
        this.frames[i] = null;
        this.loadedCount--;
        birak(b);
        this.drawnKey = '';
      }
    }
    // kuyruktan atılan (henüz başlamamış) işlerin 'iniyor' kaydı silinir: yoksa o kareler bir daha hiç istenmez
    for (const j of this.ortak.kuyruk.drop(this)) this.loading.delete(j.idx);
    const yukler = this.rol === 'aktif' || this.rol === 'sabit' || ((this.rol === 'ileri' || this.rol === 'geri') && this.izin);
    if (!yukler) return;
    const o = this.odak;
    const r = this.yaricap;
    const aday = [];
    let en = -1; // odağa en yakın var olan kare: önce o iner
    let enD = Infinity;
    for (let i = 0; i < n; i++) {
      if (!this.varMi(i)) continue;
      const d = Math.abs(i - o);
      if (d < enD) {
        en = i;
        enD = d;
      }
      if (!tut(i) || this.frames[i] || this.loading.has(i) || this.failed.has(i)) continue;
      aday.push([i, d]);
    }
    // sıra: odak kare → penceredeki anahtar kareler (kaba kapsam, hızlı ilk boyama) → penceredeki diğerleri → uzaktaki anahtarlar
    const kademe = (i, d) => (i === en ? 0 : d <= r + 8 && (i % ANAHTAR_ADIM === 0 || i === n - 1) ? 1 : d <= r + 8 ? 2 : 3);
    // aynı kademede hareket yönündeki kare, arkada kalandan önce iner (hızlı kaydırmada pencere önde dolsun)
    const yon = this.odakYon;
    const agirlik = (i, d) => (yon && (i - o) * yon < 0 ? d * 1.6 : d);
    // çok hızlı kaydırmada pencere yetişmez: yalnız odak kare ve yakın anahtar kareler iner (bkz. ayarlar.YUKLEME_DURAKLAT_VH)
    if (this.ortak.cokHizli) {
      for (let k = aday.length - 1; k >= 0; k--) if (kademe(aday[k][0], aday[k][1]) > 1) aday.splice(k, 1);
    }
    aday.sort((x, y) => kademe(x[0], x[1]) - kademe(y[0], y[1]) || agirlik(x[0], x[1]) - agirlik(y[0], y[1]));
    const taban = this.visible ? 3000 : this.rol === 'aktif' ? 2000 : 1000;
    aday.forEach(([i], k) => {
      this.loading.add(i);
      this.ortak.kuyruk.add({ owner: this, idx: i, pri: taban - k, run: () => this.load(i) });
    });
  }

  /** Kareyi indir, çöz (gerekirse ekran ölçeğine küçülterek) ve belleğe al. */
  load(i) {
    const nesil = this.nesil;
    return new Promise((resolve) => {
      const img = new Image();
      img.decoding = 'async';
      const bitir = (b) => {
        this.kabul(i, b, nesil);
        resolve();
      };
      img.onload = () => {
        const yedek = () => (img.decode ? img.decode().then(() => bitir(img), () => bitir(img)) : bitir(img));
        if (typeof createImageBitmap !== 'function') {
          yedek();
          return;
        }
        const w = Math.round(this.fit.iw * this.cozOlcek);
        const kucult = this.cozOlcek > 0 && this.cozOlcek < 1 && w < img.naturalWidth - 8;
        const p = kucult
          ? createImageBitmap(img, { resizeWidth: w, resizeHeight: Math.round((w * img.naturalHeight) / img.naturalWidth), resizeQuality: 'high' })
          : createImageBitmap(img);
        p.then(bitir, yedek);
      };
      img.onerror = () => {
        this.loading.delete(i);
        this.failed.add(i);
        resolve();
      };
      img.src = this.frameUrl(i);
    });
  }

  /** Gelen kare hâlâ isteniyorsa belleğe girer; pencere dışında kaldıysa hemen bırakılır. */
  kabul(i, b, nesil) {
    this.loading.delete(i);
    if (nesil !== this.nesil || this.frames[i] || !this.tutFn(i)) {
      birak(b);
      return;
    }
    this.frames[i] = b;
    this.loadedCount++;
    this.drawnKey = '';
    this.ortak.kick();
  }

  /** Bellekteki çözülmüş kareler: adet ve yaklaşık MB (RGBA). */
  bellek() {
    let adet = 0;
    let bayt = 0;
    for (const b of this.frames) {
      if (!b) continue;
      adet++;
      bayt += (b.width || 0) * (b.height || 0) * 4;
    }
    return { adet, mb: bayt / 1048576 };
  }

  /** Tuval ve "cover" yerleşimi (yalnız boyut değişince). */
  layout() {
    if (!this.canvas) return;
    const cw = Math.max(1, this.canvas.clientWidth || this.sabit.clientWidth);
    const ch = Math.max(1, this.canvas.clientHeight || this.sabit.clientHeight);
    const dpr = Math.min(DPR_ENFAZLA, window.devicePixelRatio || 1);
    const [iw, ih] = this.v ? this.v.res : [1600, 900];
    const s = Math.max(cw / iw, ch / ih);
    this.fit = { s, dx: (cw - iw * s) / 2, dy: (ch - ih * s) / 2, cw, ch, dpr, iw, ih };
    const bw = Math.round(cw * dpr);
    const bh = Math.round(ch * dpr);
    if (this.canvas.width !== bw || this.canvas.height !== bh) {
      this.canvas.width = bw;
      this.canvas.height = bh;
    }
    // çözme ölçeği: ekranda gerekenden büyük çözmeyin (bellek). Yalnız büyüme yeniden yükleme ister.
    const k = s * dpr;
    const olcek = k <= 0.5 ? 0.5 : k <= 0.75 ? 0.75 : 1;
    if (olcek > this.cozOlcek) {
      const ilk = this.cozOlcek === 0;
      this.cozOlcek = olcek;
      if (!ilk) this.sifirla();
    }
    this.drawnKey = '';
  }

  /** Akış denetleyicisinden: ilerleme (yumuşatılmış), görünürlük, katman saydamlığı ve ham hedef ilerleme. */
  konumla(p, gorunur, alfa, hamP) {
    this.target = this.ortak.azHareket ? 1 : p;
    this.p = this.target;
    this.hamP = hamP != null ? hamP : this.target;
    this.visible = gorunur;
    this.hedefAlfa = gorunur ? alfa : 0;
    return gorunur;
  }

  /** Fare eğimi ve seyrek kare oturması; hâlâ hareket varsa true. */
  step(dt) {
    let moving = false;
    const t = this.tilt;
    const kt = 1 - Math.exp(-5 * dt);
    if (Math.abs(t.tx - t.x) > 0.05 || Math.abs(t.ty - t.y) > 0.05) {
      t.x += (t.tx - t.x) * kt;
      t.y += (t.ty - t.y) * kt;
      moving = true;
    }
    // kaydırma durunca gösterilen konum hedef kareye oturur (seyrek sette ara kare erimesi hayalet bırakmasın)
    if (this.v && this.visible && this.fGoster >= 0 && this.frameFloat() === this.sonF) {
      this.hiz = 0;
      const d = this.fHedef - this.fGoster;
      if (Math.abs(d) > 0.02) {
        this.fGoster += d * (1 - Math.exp(-14 * dt));
        moving = true;
      } else this.fGoster = this.fHedef;
    }
    return moving;
  }

  frameFloat() {
    return this.p * Math.max(0, this.v.n - 1);
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

  /** Katman saydamlığı, anlatım vuruşları, perde: yalnız değişince yazılır. */
  katmanYaz() {
    const a = Math.round(this.hedefAlfa * 1000) / 1000;
    if (a !== this.alfa) {
      this.el.style.opacity = String(a);
      this.el.style.visibility = a <= 0 ? 'hidden' : 'visible';
      this.alfa = a;
    }
    const p = this.p;
    for (const v of this.vuruslar) {
      const acik = this.visible && p >= v.bas && p < v.son;
      if (acik !== v.acik) {
        v.el.classList.toggle('is-aktif', acik);
        v.acik = acik;
      }
    }
  }

  render() {
    this.katmanYaz();
    if (!this.ctx || !this.v || !this.visible) return;
    const f = this.frameFloat();
    // konum değiştikçe gösterilen konum gerçek konumdur; durunca fGoster en yakın kareye oturur (bkz. step)
    if (f !== this.sonF || this.fGoster < 0) {
      if (this.sonF >= 0 && f !== this.sonF) {
        this.yon = f > this.sonF ? 1 : -1;
        this.hiz = this.hiz * 0.6 + Math.abs(f - this.sonF) * 0.4;
      }
      this.fGoster = f;
      this.sonF = f;
    }
    this.fHedef = f;
    const fg = this.fGoster;
    const nb = this.neighbors(fg);
    if (nb) {
      const [a, b, t0] = nb;
      // Seyrek karelerde (inmemiş/bırakılmış ara kareler) uzun çapraz geçiş çift görüntü (hayalet) bırakır:
      // aralık büyüdükçe erime ortaya sıkıştırılır; çok büyük aralıkta (≥ 3 anahtar) erime yok, en yakın kare.
      // Hızlı kaydırmada erime daha da kısalır ve hareket yönüne doğru öne alınır (yeni kare önden gelir, eski iz uzun kalmaz).
      // Ardışık karelerde (aralık ≤ 2) doğrusal kalır.
      const gap = b - a;
      this.seyrek = gap > 2;
      this.fHedef = this.seyrek ? (t0 < 0.5 ? a : b) : f;
      let t = t0;
      if (gap > 2) {
        const hizli = this.hiz > HIZLI_ESIK;
        const w = Math.min(0.5, (hizli ? 0.7 : 1.25) / gap);
        const c = 0.5 - this.yon * (hizli ? 0.1 : 0);
        t = gap > ANAHTAR_ADIM * 3 ? (t0 < c ? 0 : 1) : smooth(c - w, c + w, t0);
      }
      const fin = this.finaleP >= 0 && this.ortak.final && !this.finaleHata && !this.ortak.azHareket ? this.finaleP : -1;
      const key = `${a}|${b}|${t.toFixed(3)}|${fin < 0 ? '' : fin.toFixed(4)}`;
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
        // finale: s5'in son karesi üzerine 2B efekt (kanvas piksel boyutunda çizilir; son argüman çözünürlük çarpanı)
        if (fin >= 0) {
          try {
            ctx.save();
            this.ortak.final.ciz(ctx, this.canvas.width, this.canvas.height, fin, dpr);
            ctx.restore();
          } catch (e) {
            this.finaleHata = true; // bozuk efekt döngüyü düşürmesin: bir kez bildir, bırak
            console.error('final.ciz hatası:', e);
          }
        }
        if (!this.hazir) {
          this.hazir = true;
          this.canvas.style.visibility = '';
          this.el.classList.add('is-hazir');
        }
      }
    }
    this.renderHotspots(fg);
    this.renderKalem(fg);
    if (this.giris) {
      // açılış metni: data-bas/data-son (sahne ilerlemesi) verilmediyse 0..0,07'de söner
      const gb = +(this.giris.dataset.bas || 0);
      const gs = +(this.giris.dataset.son || 0.07);
      const go = this.ortak.azHareket ? 1 : Math.round((1 - smooth(gb, gs, this.p)) * 1000) / 1000;
      if (go !== this.girisOpacity) {
        this.giris.style.opacity = String(go);
        this.giris.style.visibility = go < 0.01 ? 'hidden' : '';
        this.girisOpacity = go;
      }
    }
    if (this.kopru) {
      const o = (this.kopruAcik ? smooth(KOPRU_BASLA, 1, this.p) : 0).toFixed(3);
      if (this.kopru.style.opacity !== o) this.kopru.style.opacity = o;
    }
    const tr = EGIM_PX && !this.ortak.azHareket ? `translate3d(${this.tilt.x.toFixed(2)}px,${this.tilt.y.toFixed(2)}px,0) scale(1.03)` : '';
    if (tr !== this.lastTransform && this.katman) {
      this.katman.style.transform = tr;
      this.lastTransform = tr;
    }
  }

  /** Kare koordinatı (0..1) → sahne pikseli */
  toPx(u, v) {
    const { s, dx, dy, iw, ih } = this.fit;
    return [dx + u * iw * s, dy + v * ih * s];
  }

  /** Tıklanır noktalar: çevreleyen iki kayıtlı kare arasında doğrusal konum (seyrek kayıtta da çalışır). */
  renderHotspots(f) {
    if (!this.noktaKatman) return;
    const hs = this.v.hotspots || {};
    const [lo, hi] = cevre(this.hsAnahtar, f);
    const A = lo >= 0 ? hs[lo] : null;
    const B = hi >= 0 ? hs[hi] : null;
    const dar = lo >= 0 && hi >= 0 && hi - lo <= 12; // çok açık kayıtlar arasında ara değer yok
    const t = lo >= 0 && hi > lo ? (f - lo) / (hi - lo) : 0;
    const seen = new Set();
    const ids = new Set([...(A ? Object.keys(A) : []), ...(B ? Object.keys(B) : [])]);
    for (const id of ids) {
      const pa = A && A[id];
      const pb = B && B[id];
      let u;
      let v;
      if (pa && pb && dar) {
        u = pa[0] + (pb[0] - pa[0]) * t;
        v = pa[1] + (pb[1] - pa[1]) * t;
      } else if ((pa && t < 0.5) || (pb && t >= 0.5)) {
        [u, v] = (t < 0.5 ? pa : pb) || pa || pb;
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

  /** Kalem sprite'ı ([data-kalem]): meta.pen kalem ucu konumu (kare → [x, y]); kayıt yoksa gizli. */
  renderKalem(f) {
    if (!this.kalem || !this.kalemAnahtar.length) return;
    const pen = this.v.pen;
    const [lo, hi] = cevre(this.kalemAnahtar, f);
    let q = null;
    if (lo >= 0 && hi >= 0 && hi - lo <= 12) {
      const t = hi > lo ? (f - lo) / (hi - lo) : 0;
      q = [pen[lo][0] + (pen[hi][0] - pen[lo][0]) * t, pen[lo][1] + (pen[hi][1] - pen[lo][1]) * t];
    }
    if (q) {
      const [x, y] = this.toPx(q[0], q[1]);
      this.kalem.style.transform = `translate3d(${x.toFixed(1)}px,${y.toFixed(1)}px,0)`;
    }
    if (!!q !== this.kalemGorunur) {
      this.kalem.classList.toggle('is-gizli', !q);
      this.kalemGorunur = !!q;
    }
  }

  setTilt(nx, ny) {
    if (!EGIM_PX || this.ortak.azHareket) return;
    this.tilt.tx = -nx * EGIM_PX;
    this.tilt.ty = -ny * EGIM_PX * 0.6;
  }
}
