/**
 * Ege Gazbeton — giriş sayfası hikâyesi (giriş noktası).
 *
 * Performans sözleşmesi:
 *  • requestAnimationFrame yalnız gerektiğinde çalışır: kaydırma ya da fare
 *    hareketi yumuşatılırken. Hareket durunca döngü kendiliğinden durur.
 *  • Hikâye bölümü görüş alanından çıkınca hiçbir sahne çizilmez, döngü
 *    hiç başlamaz; sayfanın geri kalanı (ürünler, blog, katalog) sıfır yükle çalışır.
 *  • WebGL kullanılmaz: sahneler önceden hesaplanmış karelerdir (2B tuval; DPR ≤ 1,25).
 *  • Kare belleği pencerelidir (sahne.js): etkin sahnede ±16 kare çözülü, geri kalanı bırakılır.
 *  • Tarayıcı depolaması (localStorage/sessionStorage/çerez) kullanılmaz; bağlam yalnız bellekte ve bağlantı parametresindedir.
 *  • Hareket azaltma tercihinde sahneler tek kare (son kare) olarak durur.
 *
 * Akış: tek yapışkan sahne, 7 parça uç uca (s0..s5 + finale). Kaydırma TEK yerde yumuşatılır; parça sınırında
 * önceki parçanın son karesi sonrakinin ilk karesidir, kare seti anında değişir (ek erime yok).
 * Bağlantı parametreleri: ?debug (HUD + __ege), ?kayit (tanıtım kaydı), ?az (hareket azaltma), ?dil=en, ?t=<film saniyesi>.
 */
import { SAHNELER, DIKEY_ESIK, YUMUSAKLIK, ES_ZAMANLI, ES_HAREKETLI, SANIYE_VH, ATLAMA_VH, DPR_ENFAZLA, ONYUKLE_P, ONYUKLE_GERI, PENCERE_FINALE, YUKLEME_DURAKLAT_VH } from './ayarlar.js';
import { Sahne, Kuyruk } from './sahne.js';
import { dilUygula } from './dil.js';
import { arayuzKur } from './arayuz.js';
import { finalKur } from './final.js';
import { modullerKur } from './moduller/index.js';

const root = document.documentElement;
root.classList.replace('no-js', 'js') || root.classList.add('js');

const params = new URLSearchParams(location.search);
const debug = params.has('debug');
// ?kayit: tanıtım kaydı için — kaydırma yumuşatılmaz, her kare tam konumda çizilir (tools/kayit.mjs)
const kayit = params.has('kayit');
const azHareket = window.matchMedia('(prefers-reduced-motion: reduce)').matches || params.has('az');
if (azHareket) root.classList.add('az-hareket');

const META = window.EGE_KARELER || {};

let raf = 0;
let last = 0;
let rafSayac = 0;
// ?debug / ?kayit: her karenin betik süresi (ms) burada toplanır; sınama aracı kare hızı darboğazının JS mi, tarayıcı mı olduğunu ayırır
const sureler = debug || kayit ? [] : null;
let hizVh = 0; // yumuşatılmış kaydırma hızı (vh/sn)
let ilk = true; // ilk karede (yenileme / bağlantıyla gelişte) yumuşatmadan doğrudan otur
const aboneler = new Set();
// kare indirme/çözme kuyruğu: kaydırma sürerken eşzamanlılık düşer (ortak.hareketli, kare başına güncellenir)
const kuyruk = new Kuyruk(() => (ortak.hareketli ? ES_HAREKETLI : ES_ZAMANLI));
const ortak = {
  kuyruk,
  azHareket,
  yumusaklik: YUMUSAKLIK,
  kick,
  /** Kaydırma yumuşatması sürüyor mu (sahneler bunu seyrek kare oturması için okur). */
  hareketli: false,
  /** Kaydırma çok hızlı mı (> YUKLEME_DURAKLAT_VH): pencere kareleri indirilmez, yalnız anahtar kareler. */
  cokHizli: false,
  /** Kanvas çözünürlük çarpanı (≤ DPR_ENFAZLA): final.js kanvas piksel boyutunu bununla bilir. */
  dpr: () => Math.min(DPR_ENFAZLA, window.devicePixelRatio || 1),
  noktaOlustur: () => document.createElement('button'),
  noktaGizlendi: () => {},
  final: null,
};
ortak.final = finalKur(ortak);

// Her parça için bir Sahne: DOM'da öğesi yoksa (örn. finale henüz işaretlenmemiş) kanvassız boş parça olur,
// böylece kaydırma boyları ve indeksler hep plana uyar.
const sahneler = SAHNELER.map((cfg) => {
  const el = document.querySelector(`[data-sahne="${cfg.id}"]`) || document.createElement('div');
  return new Sahne(el, cfg, META[cfg.id], ortak);
});
const finaleIdx = SAHNELER.findIndex((c) => c.tur === 'finale');
const konakIdx = finaleIdx >= 0 ? sahneler.findIndex((s) => s.id === SAHNELER[finaleIdx].konak) : -1;

const ui = arayuzKur({ sahneler, ortak, debug });
modullerKur({ sahneler, ortak, ui });

function variantFor() {
  return window.innerWidth / Math.max(1, window.innerHeight) < DIKEY_ESIK ? 'm' : 'd';
}

for (const s of sahneler) s.setVariant(variantFor());

// --- Tek akış: kaydırma → sahne eşlemesi ------------------------------------
const akis = document.querySelector('[data-akis]');
const bas = []; // her parçanın akıştaki başlangıcı (vh birimi); parçalar uç uca biner
let toplamVh = 0;
for (const c of SAHNELER) {
  bas.push(toplamVh);
  toplamVh += c.boy;
}

function akisBoyu() {
  if (akis && !azHareket) akis.style.height = `${Math.round(((toplamVh + 100) * window.innerHeight) / 100)}px`;
}
akisBoyu();

const sinir = (x, a, b) => (x < a ? a : x > b ? b : x);

/**
 * Akış içindeki kaydırma (vh) → her parça için [ilerleme 0..1, görünür, saydamlık] ve etkin parça.
 * Dikiş bölgesi yok: sınırda etkin parça anında değişir (son kare = sonraki ilk kare).
 * Finale parçası etkinken konak sahne (s5) da görünür kalır ve son karesini çizer.
 */
function dagit(yVh) {
  const out = SAHNELER.map((c, i) => [sinir((yVh - bas[i]) / c.boy, 0, 1), false, 0]);
  let aktif = 0;
  for (let i = SAHNELER.length - 1; i >= 0; i--) {
    if (yVh >= bas[i]) {
      aktif = i;
      break;
    }
  }
  out[aktif][1] = true;
  out[aktif][2] = 1;
  if (aktif === finaleIdx && konakIdx >= 0) {
    out[konakIdx][1] = true;
    out[konakIdx][2] = 1;
  }
  return { out, aktif };
}

let akisDurum = { aktif: 0, ilerleme: 0, gorunur: true, yVh: 0, saniye: 0 };
let yS = 0; // gösterilen kaydırma (vh): akış genelinde tek yumuşatma
let finaleAktif = false;

/**
 * Bellek rolleri: etkin parçanın kare penceresi çözülü tutulur; komşularda yalnız anahtar kareler ve dikişe yakın kareler;
 * uzaktakiler tümüyle bırakılır. Komşunun yüklemesi etkin parçanın ilerlemesine bağlı bekletilir (açılışta bant yalnız s0'a).
 */
function yukle(ham, akisYakin) {
  const c = SAHNELER[ham.aktif];
  const finale = c.tur === 'finale';
  const konak = finale ? konakIdx : ham.aktif;
  const p = ham.out[konak] ? ham.out[konak][0] : 0;
  sahneler.forEach((s, i) => {
    if (!s.canvas) return;
    const d = i - konak;
    if (!akisYakin) s.rolVer('uzak');
    else if (d === 0) s.rolVer('aktif', true, finale ? PENCERE_FINALE : undefined);
    else if (d === 1) s.rolVer('ileri', finale || p > ONYUKLE_P);
    else if (d === -1) s.rolVer('geri', p < ONYUKLE_GERI);
    else s.rolVer('uzak');
  });
}

/** Film saniyesi → akıştaki kaydırma uzunluğu (vh). Plan saniyeleri (docs/plan) kaydırmaya böyle eşlenir. */
ortak.saniyeVh = (t) => t * SANIYE_VH;
/** Gösterilen film saniyesi (0..146). */
ortak.saniye = () => yS / SANIYE_VH;
/** Toplam film süresi (sn). */
ortak.toplamSaniye = toplamVh / SANIYE_VH;
/** Film saniyesinin geldiği parçanın indeksi. */
ortak.parcaIndeksi = (t) => {
  const y = t * SANIYE_VH;
  for (let i = SAHNELER.length - 1; i >= 0; i--) if (y >= bas[i]) return i;
  return 0;
};

/** Plan saniyesine kaydır (pazarlama/modüller için). Hareket azaltmada saniyenin düştüğü parçaya iner. Başarılıysa true. */
ortak.saniyeyeGit = (t, davranis = 'auto') => {
  if (!akis || !Number.isFinite(t)) return false;
  const tt = sinir(t, 0, ortak.toplamSaniye);
  if (azHareket) {
    const s = sahneler[ortak.parcaIndeksi(tt)];
    s.el.scrollIntoView({ behavior: davranis, block: 'start' });
    return true;
  }
  const top = akis.getBoundingClientRect().top + window.scrollY;
  window.scrollTo({ top: top + (ortak.saniyeVh(tt) * window.innerHeight) / 100, behavior: davranis });
  return true;
};

/** Yolculuk çubuğundan sahneye git (sahne başlangıcının biraz sonrası). */
ortak.sahneyeGit = (id) => {
  const i = sahneler.findIndex((s) => s.id === id);
  if (i < 0 || !akis) return false;
  if (azHareket) {
    sahneler[i].el.scrollIntoView({ behavior: 'auto', block: 'start' });
    return true;
  }
  const top = akis.getBoundingClientRect().top + window.scrollY;
  window.scrollTo({ top: top + ((bas[i] + 2) * window.innerHeight) / 100, behavior: 'auto' });
  return true;
};

/** Akış durumu her karede bildirilir: fn({ aktif, ilerleme, gorunur, yVh, saniye }). Dönen işlev aboneliği bırakır. */
ortak.abone = (fn) => {
  aboneler.add(fn);
  return () => aboneler.delete(fn);
};

/** İsteğe bağlı kare döngüsü: yalnız hareket varken çalışır. */
function kick() {
  if (!raf) raf = requestAnimationFrame(frame);
}

function frame(now) {
  raf = 0;
  rafSayac++;
  const basla = sureler ? performance.now() : 0;
  const dt = last ? Math.min(0.05, (now - last) / 1000) : 1 / 60;
  last = now;
  const vh = window.innerHeight;
  // 1) okumalar önce: akışın konumu
  const r = akis ? akis.getBoundingClientRect() : { top: 0, bottom: 0, height: 0 };
  const yHam = sinir((-r.top / vh) * 100, 0, toplamVh);
  const akisGorunur = r.bottom > 0 && r.top < vh;
  const akisYakin = r.bottom > -vh * 1.5 && r.top < vh * 2.5;
  // tek yumuşatma: gösterilen konum ham konuma yaklaşır; çok uzaksa (menüden atlama, çubuk sürükleme) doğrudan atlar
  const ySOnce = yS;
  const fark = yHam - yS;
  if (ilk || kayit || azHareket || Math.abs(fark) > ATLAMA_VH) yS = yHam;
  else {
    yS += fark * (1 - Math.exp(-YUMUSAKLIK * dt));
    if (Math.abs(yHam - yS) < 0.04) yS = yHam;
  }
  ilk = false;
  const hareketli = yS !== yHam;
  ortak.hareketli = hareketli;
  // hız: çok hızlıyken pencere yüklemesi durur; yavaşlayınca yeniden planlanır
  hizVh = hareketli ? hizVh * 0.7 + (Math.abs(yS - ySOnce) / Math.max(dt, 1e-3)) * 0.3 : 0;
  const hizli = hizVh > YUKLEME_DURAKLAT_VH;
  if (hizli !== ortak.cokHizli) {
    ortak.cokHizli = hizli;
    if (!hizli) for (const s of sahneler) s.planKirli = true;
  }
  // hareket azaltma: akış durağan sütun, her sahne kendi yerinde tek kare
  const ham = azHareket ? { out: SAHNELER.map(() => [1, true, 1]), aktif: 0 } : dagit(yHam);
  const { out, aktif } = azHareket ? ham : dagit(yS);
  const vis = sahneler.map((s, i) => s.konumla(out[i][0], (azHareket || akisGorunur) && out[i][1], out[i][2], ham.out[i][0]));
  // finale: konak sahne kanvasında efekt çizilir; ilerleme yalnız finale etkinken geçerli
  const finaleP = !azHareket && aktif === finaleIdx && finaleIdx >= 0 ? out[finaleIdx][0] : -1;
  if (konakIdx >= 0) sahneler[konakIdx].finaleP = finaleP;
  if (ortak.final && finaleP >= 0) ortak.final.konumla(finaleP);
  if ((finaleP >= 0) !== finaleAktif) {
    finaleAktif = finaleP >= 0;
    document.dispatchEvent(new CustomEvent('ege:finale', { detail: { aktif: finaleAktif } }));
  }
  if (azHareket) {
    for (const s of sahneler) if (s.canvas) s.rolVer('sabit');
  } else yukle(ham, akisYakin);
  // 2) sonra yazımlar
  let more = hareketli;
  sahneler.forEach((s, i) => {
    if (!vis[i] && !s.wasVisible) return;
    if (s.step(dt)) more = true;
    s.render();
    s.wasVisible = vis[i];
  });
  akisDurum = {
    aktif,
    ilerleme: Math.min(1, Math.max(0, yS / toplamVh)),
    gorunur: r.top < vh * 0.4 && r.bottom > vh * 0.6,
    yVh: yS,
    saniye: yS / SANIYE_VH,
  };
  ui.guncelle(sahneler, akisDurum);
  for (const fn of aboneler) fn(akisDurum);
  if (more) raf = requestAnimationFrame(frame);
  else last = 0;
  if (sureler) sureler.push(performance.now() - basla);
}

window.addEventListener('scroll', kick, { passive: true });
let lastVariant = variantFor();
window.addEventListener(
  'resize',
  () => {
    const v = variantFor();
    akisBoyu();
    for (const s of sahneler) {
      if (v !== lastVariant) s.setVariant(v);
      else s.layout();
    }
    lastVariant = v;
    kick();
  },
  { passive: true }
);

// Fare ile hafif eğim (yalnız ince işaretçide, yalnız görünen sahnede)
if (window.matchMedia('(pointer: fine)').matches && !azHareket) {
  window.addEventListener(
    'pointermove',
    (e) => {
      const nx = (e.clientX / window.innerWidth) * 2 - 1;
      const ny = (e.clientY / window.innerHeight) * 2 - 1;
      let any = false;
      for (const s of sahneler) {
        if (s.visible) {
          s.setTilt(nx, ny);
          any = true;
        }
      }
      if (any) kick();
    },
    { passive: true }
  );
}

document.addEventListener('visibilitychange', () => {
  if (document.hidden && raf) {
    cancelAnimationFrame(raf);
    raf = 0;
    last = 0;
  } else if (!document.hidden) kick();
});

// Dil: yalnız ?dil=en bağlantı parametresi (tarayıcı depolaması kullanılmaz)
dilUygula(params.get('dil') === 'en' ? 'en' : 'tr');

// ?t=<film saniyesi>: bağlantıyla belirli saniyeden aç (sahnenin ilk karesi yüklenmeden ilk boyama poster ile olur)
const t0 = parseFloat(params.get('t'));
if (Number.isFinite(t0)) {
  ortak.saniyeyeGit(t0);
  window.addEventListener('load', () => ortak.saniyeyeGit(t0), { once: true });
}

kick();

// Canlı katman: teklif bölümü 1,5 ekran yaklaşınca yüklenir (veri tasarrufunda hiç yüklenmez)
const canli = document.querySelector('[data-canli]');
const tasarruf = navigator.connection && navigator.connection.saveData;
if (canli && !tasarruf) {
  const io = new IntersectionObserver(
    (entries) => {
      if (!entries.some((e) => e.isIntersecting)) return;
      io.disconnect();
      const sc = document.createElement('script');
      sc.src = 'assets/js/canli.js';
      sc.async = true;
      document.body.appendChild(sc);
    },
    { rootMargin: '150% 0px' }
  );
  io.observe(canli);
}

if (debug || kayit) {
  window.__ege = {
    sahneler,
    ortak,
    /** indirme kuyruğu boş ve çizim döngüsü durmuşsa true (kayıt aracı bekler) */
    hazir() {
      return kuyruk.jobs.length === 0 && kuyruk.active === 0 && raf === 0;
    },
    /** çözülmüş kare belleği: toplam adet ve yaklaşık MB (sınama aracı ölçer) */
    bellek() {
      let adet = 0;
      let mb = 0;
      const sahne = {};
      for (const s of sahneler) {
        const b = s.bellek();
        adet += b.adet;
        mb += b.mb;
        sahne[s.id] = { adet: b.adet, mb: +b.mb.toFixed(1) };
      }
      return { adet, mb: +mb.toFixed(1), sahne };
    },
    /** Kare başına betik süresi (ms): { say, ort, p95, enBuyuk }; sifirla=true ise sayaç sıfırlanır */
    sureler(sifirla = false) {
      const d = [...sureler].sort((a, b) => a - b);
      const say = d.length;
      const r = say ? { say, ort: +(d.reduce((a, b) => a + b, 0) / say).toFixed(2), p95: +d[Math.floor(say * 0.95)].toFixed(2), enBuyuk: +d[say - 1].toFixed(2) } : { say: 0, ort: 0, p95: 0, enBuyuk: 0 };
      if (sifirla) sureler.length = 0;
      return r;
    },
    get raf() {
      return rafSayac;
    },
    get calisiyor() {
      return raf !== 0;
    },
    get saniye() {
      return yS / SANIYE_VH;
    },
    toplamVh,
    bas,
  };
}
