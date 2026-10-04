/**
 * Canlı katman — hikâyenin finalinde (src/hikaye/final.js) fareyle dalgalanan gözenek yüzeyi.
 * Hikâyenin sonunda "dokunulabilir" gazbeton: imleç hareket ettikçe yüzey fiziksel ağırlıkla dalgalanır,
 * durunca sakin, doğal bir nefes alır.
 *
 * Yaşam döngüsü (kural: WebGL yalnız finale etkinken ve boşta; DPR ≤ 1,25 — config.js TIERS.dprMax):
 *   window.EgeCanli.hazirla() → bağlam + gölgelendirici + ilk görünmez render (finale t ≥ 138, requestIdleCallback ile)
 *   window.EgeCanli.ac()      → açılış animasyonu ve döngü başlar (finale t ≥ 140, perde açılırken)
 *   window.EgeCanli.uyut()    → döngü durur (rAF iptal, işaretçi dinleyicileri sökülür)
 *   window.EgeCanli.kapat()   → sahne yıkılır, WebGL bağlamı bırakılır (finale bitince / geri kaydırınca)
 * Betik yüklenince hiçbir şey başlamaz; çağıran final.js'tir. three.js bu dosyaya gömülüdür (CDN yok →
 * çevrimdışı maket ve KVKK uyumlu).
 */
import {
  AdditiveBlending, BufferAttribute, BufferGeometry, Color, DataTexture, DataUtils, HalfFloatType, LinearFilter,
  PerspectiveCamera, Points, RedFormat, Scene, ShaderMaterial, Vector2, Vector3, Vector4, WebGLRenderer,
} from 'three';

// Yalnız kullanılan sınıflar → paketleyici geri kalan three.js'i atar (daha küçük dosya)
const THREE = {
  AdditiveBlending, BufferAttribute, BufferGeometry, Color, DataTexture, DataUtils, HalfFloatType, LinearFilter,
  PerspectiveCamera, Points, RedFormat, Scene, ShaderMaterial, Vector2, Vector3, Vector4, WebGLRenderer,
};
import { HeroScene } from './scene.js';
import { detectCapabilities } from './capabilities.js';

const kok = document.querySelector('[data-canli-kok]');
let sahne = null;

/** Sahneyi kur ve görünmez ilk karesini çiz. true = hazır (ya da zaten hazırdı). */
function hazirla() {
  if (!kok) return false;
  if (sahne) return true;
  const caps = detectCapabilities();
  kok.dataset.kademe = caps.tier;
  if (caps.mode === 'off') return false;
  // taze tuval: kapatılmış bir bağlam aynı tuvalde yeniden açılamaz
  const eski = kok.querySelector('canvas');
  const tuval = eski.cloneNode(false);
  eski.replaceWith(tuval);
  try {
    const s = new HeroScene(THREE, {
      root: kok,
      canvas: tuval,
      tier: caps.tier,
      mode: caps.mode,
      reducedMotion: caps.reducedMotion,
      debugEl: null,
      aktif: false,
    });
    s.init();
    s.hazirla();
    sahne = s;
    window.__egeCanli = s;
    // düğmelerin üzerine gelince yüzeye nazik bir dalga
    const bolum = kok.closest('.eg-sahne--finale') || document;
    for (const a of bolum.querySelectorAll('.eg-dugme')) {
      if (a.dataset.nabiz) continue; // yeniden hazırlamada dinleyici çoğalmasın
      a.dataset.nabiz = '1';
      a.addEventListener('pointerenter', () => {
        const r = a.getBoundingClientRect();
        kok.dispatchEvent(new CustomEvent('eg:pulse', { detail: { x: r.left + r.width / 2, y: r.bottom + 40, strength: 0.7 } }));
      });
    }
    return true;
  } catch (err) {
    console.warn('[EgeCanli] canlı katman açılamadı, düz zemin kullanılıyor.', err);
    sahne = null;
    return false;
  }
}

function ac() {
  if (!sahne) return;
  sahne.introBaslat();
  sahne.setAktif(true);
}

function uyut() {
  if (sahne) sahne.setAktif(false);
}

function kapat() {
  if (!sahne) return;
  sahne.destroy();
  sahne = null;
  window.__egeCanli = null;
}

window.EgeCanli = { hazirla, ac, uyut, kapat, calisiyor: () => !!(sahne && sahne.running), hazir: () => !!sahne };
