/**
 * Ege Gazbeton — giriş sayfası hikâyesi (giriş noktası).
 *
 * Performans sözleşmesi:
 *  • requestAnimationFrame yalnız gerektiğinde çalışır: kaydırma ya da fare
 *    hareketi yumuşatılırken. Hareket durunca döngü kendiliğinden durur.
 *  • Hikâye bölümü görüş alanından çıkınca hiçbir sahne çizilmez, döngü
 *    hiç başlamaz; sayfanın geri kalanı (ürünler, blog, katalog) sıfır yükle çalışır.
 *  • WebGL kullanılmaz: sahneler önceden hesaplanmış karelerdir (2B tuval).
 *  • Hareket azaltma tercihinde sahneler tek kare (son kare) olarak durur.
 */
import { SAHNELER, DIKEY_ESIK, YUMUSAKLIK, ES_ZAMANLI } from './ayarlar.js';
import { Sahne, Kuyruk } from './sahne.js';
import { dilUygula } from './dil.js';
import { arayuzKur } from './arayuz.js';

const root = document.documentElement;
root.classList.replace('no-js', 'js') || root.classList.add('js');

const params = new URLSearchParams(location.search);
const debug = params.has('debug');
const azHareket = window.matchMedia('(prefers-reduced-motion: reduce)').matches || params.has('az');
if (azHareket) root.classList.add('az-hareket');

const META = window.EGE_KARELER || {};
const kuyruk = new Kuyruk(ES_ZAMANLI);

let raf = 0;
let last = 0;
let rafSayac = 0;
const ortak = {
  kuyruk,
  azHareket,
  yumusaklik: YUMUSAKLIK,
  kick,
  noktaOlustur: () => document.createElement('button'),
  noktaGizlendi: () => {},
};

const sahneler = [];
for (const cfg of SAHNELER) {
  const el = document.querySelector(`[data-sahne="${cfg.id}"]`);
  if (el) sahneler.push(new Sahne(el, cfg, META[cfg.id], ortak));
}

const ui = arayuzKur({ sahneler, ortak, debug });

function variantFor() {
  return window.innerWidth / Math.max(1, window.innerHeight) < DIKEY_ESIK ? 'm' : 'd';
}

for (const s of sahneler) s.setVariant(variantFor());

// Yakınlık: sahne 1,5 ekran yaklaşınca kareleri indir; 3 ekran uzaklaşınca bırak
const yakin = new IntersectionObserver(
  (entries) => {
    for (const e of entries) {
      const s = sahneler.find((x) => x.el === e.target);
      if (!s) continue;
      s.near = e.isIntersecting;
      if (s.near) s.ensure();
    }
  },
  { rootMargin: '150% 0px 150% 0px' }
);
const uzak = new IntersectionObserver(
  (entries) => {
    for (const e of entries) {
      const s = sahneler.find((x) => x.el === e.target);
      if (s && !e.isIntersecting) s.release();
    }
  },
  { rootMargin: '300% 0px 300% 0px' }
);
for (const s of sahneler) {
  yakin.observe(s.el);
  uzak.observe(s.el);
}

/** İsteğe bağlı kare döngüsü: yalnız hareket varken çalışır. */
function kick() {
  if (!raf) raf = requestAnimationFrame(frame);
}

function frame(now) {
  raf = 0;
  rafSayac++;
  const dt = last ? Math.min(0.05, (now - last) / 1000) : 1 / 60;
  last = now;
  const vh = window.innerHeight;
  // 1) tüm okumalar (yerleşim) önce
  const vis = sahneler.map((s) => s.measure(vh));
  // 2) sonra yazımlar
  let more = false;
  sahneler.forEach((s, i) => {
    if (!vis[i] && !s.wasVisible) return;
    if (s.step(dt)) more = true;
    s.render();
    s.wasVisible = vis[i];
  });
  ui.guncelle(sahneler, vis);
  if (more) raf = requestAnimationFrame(frame);
  else last = 0;
}

window.addEventListener('scroll', kick, { passive: true });
let lastVariant = variantFor();
window.addEventListener(
  'resize',
  () => {
    const v = variantFor();
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

// Dil: ?dil=en ya da kayıtlı tercih
let lang = params.get('dil');
try {
  lang = lang || localStorage.getItem('ege-dil');
} catch {
  /* gizli pencere */
}
dilUygula(lang === 'en' ? 'en' : 'tr');

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

if (debug) {
  window.__ege = {
    sahneler,
    get raf() {
      return rafSayac;
    },
    get calisiyor() {
      return raf !== 0;
    },
  };
}
