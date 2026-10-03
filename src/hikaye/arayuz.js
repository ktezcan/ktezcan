/**
 * Arayüz: menü, dil seçimi, yolculuk çubuğu, tıklanır noktalar ve açılır kart,
 * kitle seçici, analitik kancaları, hata ayıklama paneli.
 */
import { NOKTALAR, dil, dilUygula, EN } from './dil.js';

export function arayuzKur({ sahneler, ortak, debug }) {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  // --- Mobil menü ----------------------------------------------------------
  const menuBtn = $('[data-menu-ac]');
  const menu = $('#ana-menu');
  if (menuBtn && menu) {
    menuBtn.addEventListener('click', () => {
      const open = menuBtn.getAttribute('aria-expanded') !== 'true';
      menuBtn.setAttribute('aria-expanded', String(open));
      document.documentElement.classList.toggle('menu-acik', open);
    });
    menu.addEventListener('click', (e) => {
      if (e.target.closest('a')) {
        menuBtn.setAttribute('aria-expanded', 'false');
        document.documentElement.classList.remove('menu-acik');
      }
    });
  }

  // --- Üst çubuk: açık zeminli bölümün üstündeyken koyu dolgu (logo okunur kalsın) ---
  const ust = $('.eg-ust');
  const acikZemin = $$('.eg-sonrasi, .eg-alt');
  if (ust && acikZemin.length && 'IntersectionObserver' in window) {
    const altinda = new Set();
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) (e.isIntersecting ? altinda.add(e.target) : altinda.delete(e.target));
        ust.classList.toggle('is-dolu', altinda.size > 0);
      },
      { rootMargin: '0px 0px -91% 0px' } // ekranın üst şeridi ≈ üst çubuk
    );
    for (const el of acikZemin) io.observe(el);
  }

  // --- Dil -----------------------------------------------------------------
  for (const b of $$('[data-dil-sec]')) {
    b.addEventListener('click', () => {
      const l = b.dataset.dilSec;
      dilUygula(l);
      try {
        localStorage.setItem('ege-dil', l);
      } catch {
        /* yok say */
      }
      kartKapat();
      for (const s of sahneler) for (const [id, btn] of s.noktalar) etiketYaz(btn, id);
    });
  }

  // --- Analitik (varsa GTM/GA dataLayer'a yazar; çerez/harici servis eklemez) --
  document.addEventListener('click', (e) => {
    const a = e.target.closest('[data-iz]');
    if (!a) return;
    const dl = window.dataLayer;
    if (Array.isArray(dl)) dl.push({ event: 'ege_tik', hedef: a.dataset.iz, dil: dil() });
  });

  // --- Tıklanır noktalar ve kart --------------------------------------------
  const kart = $('#nokta-kart');
  let acikId = null;
  let acikSahne = null;

  function metin(id) {
    const d = NOKTALAR[id];
    if (!d) return [id, '', ''];
    return d[dil()] || d.tr;
  }

  function etiketYaz(btn, id) {
    const [baslik] = metin(id);
    btn.querySelector('.eg-nokta__etiket').textContent = baslik;
    btn.setAttribute('aria-label', baslik);
  }

  ortak.noktaOlustur = (id, sahne) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'eg-nokta is-gizli';
    btn.dataset.nokta = id;
    btn.tabIndex = -1;
    btn.innerHTML = '<span class="eg-nokta__halka" aria-hidden="true"></span><span class="eg-nokta__etiket"></span>';
    etiketYaz(btn, id);
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (acikId === id) kartKapat();
      else kartAc(id, btn, sahne);
    });
    return btn;
  };

  ortak.noktaGizlendi = (id) => {
    if (acikId === id) kartKapat();
  };

  function kartAc(id, btn, sahne) {
    if (!kart) return;
    const [baslik, aciklama, kaynak] = metin(id);
    kart.querySelector('[data-kart-baslik]').textContent = baslik;
    kart.querySelector('[data-kart-metin]').textContent = aciklama;
    const k = kart.querySelector('[data-kart-kaynak]');
    k.hidden = !kaynak;
    k.textContent = kaynak ? `${dil() === 'en' ? EN.kaynak : 'Kaynak'}: ${kaynak}` : '';
    const r = btn.getBoundingClientRect();
    const sr = sahne.sabit.getBoundingClientRect();
    const x = Math.min(Math.max(16, r.left - sr.left + 26), sr.width - 316);
    const y = Math.min(Math.max(72, r.top - sr.top - 12), sr.height - 200);
    sahne.sabit.appendChild(kart);
    kart.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    kart.hidden = false;
    acikId = id;
    acikSahne = sahne;
    btn.setAttribute('aria-expanded', 'true');
    kart.querySelector('[data-kart-kapat]').focus({ preventScroll: true });
  }

  function kartKapat() {
    if (!kart || kart.hidden) return;
    kart.hidden = true;
    if (acikSahne) {
      const btn = acikSahne.noktalar.get(acikId);
      if (btn) {
        btn.setAttribute('aria-expanded', 'false');
      }
    }
    acikId = null;
    acikSahne = null;
  }

  if (kart) {
    kart.querySelector('[data-kart-kapat]').addEventListener('click', kartKapat);
    document.addEventListener('click', (e) => {
      if (!kart.hidden && !kart.contains(e.target)) kartKapat();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') kartKapat();
    });
  }

  // --- Yolculuk çubuğu (bölüm adı + ilerleme; dokununca liste) ---------------
  const yol = $('[data-yolculuk]');
  const yolDolgu = yol ? $('[data-yol-dolgu]', yol) : null;
  const yolAd = yol ? $('[data-yol-ad]', yol) : null;
  const yolBtn = yol ? $('[data-yol-ac]', yol) : null;
  const hikaye = $('[data-hikaye]');
  let sonAd = '';
  const YOL_TR = { s0: 'Blok', s1: 'Üretim', s2: 'Yapı', s3: 'Sistem', s4: 'Dünya', son: 'Teklif' };
  function yolAdYaz() {
    if (!yolAd) return;
    const tr = YOL_TR[sonAd] || '';
    yolAd.textContent = dil() === 'en' ? EN[`yol.${sonAd}`] || tr : tr;
  }
  document.addEventListener('ege:dil', yolAdYaz);
  if (yolBtn) {
    yolBtn.addEventListener('click', () => {
      const open = yolBtn.getAttribute('aria-expanded') !== 'true';
      yolBtn.setAttribute('aria-expanded', String(open));
      yol.classList.toggle('is-acik', open);
    });
    for (const a of $$('a', yol)) {
      a.addEventListener('click', () => {
        yolBtn.setAttribute('aria-expanded', 'false');
        yol.classList.remove('is-acik');
      });
    }
  }

  // --- İçerik blokları: görünür olunca yumuşak yükselme (bir kez) -------------
  const icerikIO = new IntersectionObserver(
    (entries) => {
      for (const e of entries) {
        if (e.isIntersecting) {
          e.target.classList.add('is-gorunur');
          icerikIO.unobserve(e.target);
        }
      }
    },
    { threshold: 0.18 }
  );
  for (const el of $$('.eg-icerik')) icerikIO.observe(el);

  // --- Hata ayıklama paneli ---------------------------------------------------
  const hud = debug ? document.createElement('pre') : null;
  let hudVis = [];
  if (hud) {
    hud.className = 'eg-hud';
    document.body.appendChild(hud);
    // yalnız ?debug: döngüden bağımsız okur → rAF durunca da doğru durumu gösterir
    setInterval(() => {
      const e = window.__ege;
      const lines = sahneler.map((s, i) => `${s.id} ${hudVis[i] ? '●' : '·'} p=${s.p.toFixed(3)} kare ${s.v ? s.frameFloat().toFixed(1) : '-'} / ${s.v ? s.v.n : 0}  yüklü ${s.loadedCount} [${s.variant}]`);
      hud.textContent = `rAF: ${e && e.calisiyor ? 'ÇALIŞIYOR' : 'DURDU (boşta)'}  kare sayacı ${e ? e.raf : 0}\n${lines.join('\n')}`;
    }, 300);
  }

  return {
    guncelle(list, vis) {
      // yolculuk çubuğu: hikâye görünürken
      if (yol && hikaye) {
        const r = hikaye.getBoundingClientRect();
        const vh = window.innerHeight;
        const on = r.top < vh * 0.4 && r.bottom > vh * 0.6;
        yol.classList.toggle('is-gorunur', on);
        if (on) {
          const p = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - vh)));
          yolDolgu.style.transform = `scaleX(${p.toFixed(4)})`;
          let ad = '';
          for (let i = 0; i < list.length; i++) if (vis[i]) ad = list[i].id;
          if (!ad) {
            // sahneler arası içerik kartındayken bir önceki sahne; teklif bölümündeyse 'son'
            const son = document.getElementById('teklif');
            if (son && son.getBoundingClientRect().top < vh * 0.6) ad = 'son';
            else {
              for (let i = list.length - 1; i >= 0; i--) {
                if (list[i].el.getBoundingClientRect().top < 0) {
                  ad = list[i].id;
                  break;
                }
              }
            }
          }
          if (ad !== sonAd) {
            sonAd = ad;
            yolAdYaz();
            for (const a of $$('[data-yol-hedef]', yol)) a.classList.toggle('is-aktif', a.dataset.yolHedef === ad);
          }
        }
      }
      hudVis = vis;
    },
  };
}
