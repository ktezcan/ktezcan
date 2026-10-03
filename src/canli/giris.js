/**
 * Canlı katman — teklif bölümünün arkasında fareyle dalgalanan gözenek yüzeyi.
 * Hikâyenin sonunda "dokunulabilir" gazbeton: imleç hareket ettikçe yüzey
 * fiziksel ağırlıkla dalgalanır, durunca sakin, doğal bir nefes alır.
 * Yalnız bölüm görünürken çalışır (IntersectionObserver + sekme görünürlüğü).
 * three.js bu dosyaya gömülüdür (CDN yok → çevrimdışı maket ve KVKK uyumlu).
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

const root = document.querySelector('[data-canli]');
if (root) {
  const caps = detectCapabilities();
  root.dataset.kademe = caps.tier;
  if (caps.mode !== 'off') {
    try {
      const sahne = new HeroScene(THREE, {
        root,
        canvas: root.querySelector('canvas'),
        tier: caps.tier,
        mode: caps.mode,
        reducedMotion: caps.reducedMotion,
        debugEl: null,
      });
      sahne.init();
      window.__egeCanli = sahne;
      // düğmelerin üzerine gelince yüzeye nazik bir dalga
      const bolum = root.closest('section') || document;
      for (const a of bolum.querySelectorAll('.eg-dugme')) {
        a.addEventListener('pointerenter', () => {
          const r = a.getBoundingClientRect();
          root.dispatchEvent(new CustomEvent('eg:pulse', { detail: { x: r.left + r.width / 2, y: r.bottom + 40, strength: 0.7 } }));
        });
      }
    } catch (err) {
      console.warn('[EgeCanli] canlı katman açılamadı, düz zemin kullanılıyor.', err);
    }
  }
}
