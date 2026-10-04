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
import { SAHNELER, DIKEY_ESIK, YUMUSAKLIK, ES_ZAMANLI, GECIS } from './ayarlar.js';
import { Sahne, Kuyruk } from './sahne.js';
import { dilUygula } from './dil.js';
import { arayuzKur } from './arayuz.js';
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
const kuyruk = new Kuyruk(ES_ZAMANLI);

let raf = 0;
let last = 0;
let rafSayac = 0;
let ilk = true; // ilk karede (yenileme / bağlantıyla gelişte) yumuşatmadan doğrudan otur
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
modullerKur({ sahneler, ortak, ui });

function variantFor() {
  return window.innerWidth / Math.max(1, window.innerHeight) < DIKEY_ESIK ? 'm' : 'd';
}

for (const s of sahneler) s.setVariant(variantFor());

// --- Tek akış: kaydırma → sahne ve geçiş eşlemesi ---------------------------
const akis = document.querySelector('[data-akis]');
const bas = []; // her sahnenin akıştaki başlangıcı (vh birimi)
let toplamVh = 0;
SAHNELER.forEach((c, i) => {
  bas.push(toplamVh);
  toplamVh += c.boy + (i < SAHNELER.length - 1 ? GECIS : 0);
});

function akisBoyu() {
  if (akis && !azHareket) akis.style.height = `${Math.round(((toplamVh + 100) * window.innerHeight) / 100)}px`;
}
akisBoyu();

/** Akış içindeki kaydırma (vh) → her sahne için [p, görünür, saydamlık] ve etkin sahne. */
function dagit(yVh) {
  const n = sahneler.length;
  const out = sahneler.map(() => [0, false, 0]);
  let aktif = 0;
  for (let i = 0; i < n; i++) {
    const st = bas[i];
    const en = st + SAHNELER[i].boy;
    if (yVh < st && i === 0) {
      out[0] = [0, true, 1];
      aktif = 0;
      break;
    }
    if (yVh >= st && yVh <= en) {
      out[i] = [(yVh - st) / SAHNELER[i].boy, true, 1];
      aktif = i;
      break;
    }
    if (i === n - 1 || (yVh > en && yVh < en + GECIS)) {
      if (i === n - 1) {
        out[i] = [1, true, 1];
        aktif = i;
        break;
      }
      const u = (yVh - en) / GECIS;
      const a = u * u * (3 - 2 * u);
      out[i] = [1, true, 1];
      out[i + 1] = [0, true, a];
      aktif = a < 0.5 ? i : i + 1;
      break;
    }
  }
  return { out, aktif };
}

let akisDurum = { aktif: 0, ilerleme: 0, gorunur: true };

/** Yakınlık: etkin sahne ve komşuları iner; uzaktakiler bellekten bırakılır. */
function yukle(aktif, akisYakin) {
  sahneler.forEach((s, i) => {
    const d = Math.abs(i - aktif);
    const yakin = akisYakin && d <= 1;
    if (yakin && !s.near) {
      s.near = true;
      s.ensure();
    } else if (!yakin && s.near) {
      s.near = false;
      if (d >= 2 || !akisYakin) s.release();
    }
  });
}

/** Yolculuk çubuğundan sahneye git (sahne başlangıcının biraz sonrası). */
ortak.sahneyeGit = (id) => {
  const i = sahneler.findIndex((s) => s.id === id);
  if (i < 0 || !akis) return false;
  const top = akis.getBoundingClientRect().top + window.scrollY;
  window.scrollTo({ top: top + ((bas[i] + 2) * window.innerHeight) / 100, behavior: 'auto' });
  return true;
};

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
  // 1) okumalar önce: akışın konumu
  const r = akis ? akis.getBoundingClientRect() : { top: 0, bottom: 0, height: 0 };
  const yVh = (-r.top / vh) * 100;
  const akisGorunur = r.bottom > 0 && r.top < vh;
  const akisYakin = r.bottom > -vh * 1.5 && r.top < vh * 2.5;
  // hareket azaltma: akış durağan sütun, her sahne kendi yerinde tek kare
  const { out, aktif } = azHareket ? { out: sahneler.map(() => [1, true, 1]), aktif: 0 } : dagit(yVh);
  const vis = sahneler.map((s, i) => s.konumla(out[i][0], (azHareket || akisGorunur) && out[i][1], out[i][2]));
  if (azHareket) for (const s of sahneler) {
    if (!s.near) {
      s.near = true;
      s.ensure();
    }
  }
  else yukle(aktif, akisYakin);
  if (ilk || kayit) {
    for (const s of sahneler) s.p = s.target;
    ilk = false;
  }
  // 2) sonra yazımlar
  let more = false;
  sahneler.forEach((s, i) => {
    if (!vis[i] && !s.wasVisible) return;
    if (s.step(dt)) more = true;
    s.render();
    s.wasVisible = vis[i];
  });
  akisDurum = { aktif, ilerleme: Math.min(1, Math.max(0, yVh / toplamVh)), gorunur: r.top < vh * 0.4 && r.bottom > vh * 0.6 };
  ui.guncelle(sahneler, akisDurum);
  if (more) raf = requestAnimationFrame(frame);
  else last = 0;
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

if (debug || kayit) {
  window.__ege = {
    sahneler,
    /** indirme kuyruğu boş ve çizim döngüsü durmuşsa true (kayıt aracı bekler) */
    hazir() {
      return kuyruk.jobs.length === 0 && kuyruk.active === 0 && raf === 0;
    },
    get raf() {
      return rafSayac;
    },
    get calisiyor() {
      return raf !== 0;
    },
  };
}
