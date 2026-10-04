/**
 * Arayüz: menü, dil seçimi (yalnız bellekte), yolculuk çubuğu (7 bölüm), tıklanır noktalar ve kart, kıta etiketleri ve sayacı,
 * ürün çip çubuğu, hero/CTA zamanlaması, kitle yolları, pazarlama bağlamı ve dataLayer olayları, hata ayıklama paneli.
 *
 * Tarayıcı depolaması (localStorage/sessionStorage/çerez) KULLANILMAZ: dil ?dil=en parametresiyle, ürün bağlamı bellekte.
 * Zamana bağlı her şey film saniyesinden (durum.saniye, 1 sn = 22 vh) okunur; guncelle() yalnız değişince DOM'a yazar.
 */
import { NOKTALAR, NOKTA_SAHNE, KITA, KITA_KARE, KITA_SURE_SN, URUN, EN, dil, dilUygula } from './dil.js';
import { baglamKur, DURAKLAR } from './baglam.js';

const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
const smooth = (a, b, x) => {
  const t = clamp01((x - a) / (b - a));
  return t * t * (3 - 2 * t);
};

/** CTA/ana düğme pencereleri (film sn): bu aralıklarda ekranın tek lime dolgulu düğmesi ana CTA'dır (üst çubuk düğmesi çizgili olur). */
const ANA_CTA = [[0, 2.4], [64, 67], [142, 147]];
/** Finale CTA grubunun göründüğü saniye ("Hikâyeyi atla" ve yolculuk çubuğundaki "Teklif" buraya iner). */
const FINALE_CTA_SN = 142;
/** Ürün çip çubuğunun görünür olduğu aralık (film sn). */
const DURAK_PENCERE = [34, 66];
/** Dünya parçası: kıta sayacı görünür aralığı (film sn) ve süresi 16 sn olan parçanın p'ye çevrimi. */
const DUNYA_SN = 16;
const SAYAC_PENCERE = [124, 134];

export function arayuzKur({ sahneler, ortak, debug }) {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const kok = document.documentElement;
  // final.js dünya parçasının yerleşimini (cover uyumu, meta) buradan okur
  ortak.sahneler = sahneler;
  const baglam = baglamKur({ ortak });
  const iz = baglam.iz;
  const saniyeyeGit = (t) => (ortak.saniyeyeGit ? ortak.saniyeyeGit(t) : false);

  // --- Mobil menü ----------------------------------------------------------
  const menuBtn = $('[data-menu-ac]');
  const menu = $('#ana-menu');
  function menuKapat() {
    if (!menuBtn) return;
    menuBtn.setAttribute('aria-expanded', 'false');
    kok.classList.remove('menu-acik');
  }
  if (menuBtn && menu) {
    menuBtn.addEventListener('click', () => {
      const open = menuBtn.getAttribute('aria-expanded') !== 'true';
      menuBtn.setAttribute('aria-expanded', String(open));
      kok.classList.toggle('menu-acik', open);
    });
    menu.addEventListener('click', (e) => {
      if (e.target.closest('a')) menuKapat();
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

  // --- Dil (depolama yok: ?dil=en bağlantı parametresi; geçişte adres çubuğu parametresi yenilenir) -----------------
  function dilDegistir(l) {
    if (l === dil()) return;
    dilUygula(l);
    try {
      const u = new URL(location.href);
      if (l === 'en') u.searchParams.set('dil', 'en');
      else u.searchParams.delete('dil');
      history.replaceState(null, '', u.toString());
    } catch {
      /* file:// ya da kısıtlı bağlamda adres değişmez: sorun değil */
    }
    iz('ege_dil', { dil: l });
    kartKapat();
    for (const s of sahneler) for (const [id, btn] of s.noktalar) etiketYaz(btn, id);
  }
  for (const b of $$('[data-dil-sec]')) b.addEventListener('click', () => dilDegistir(b.dataset.dilSec));
  // tarayıcı dili Türkçe değilse hero'da "View in English" önerisi (otomatik geçiş yok) ve ihracat çipi öne
  const dilOneri = $('[data-dil-oneri]');
  if (dilOneri && !/^tr/i.test(navigator.language || 'tr')) {
    dilOneri.hidden = false;
    dilOneri.addEventListener('click', () => dilDegistir('en'));
    for (const a of $$('[data-kitle="bayi"]')) a.style.order = '-1';
  }

  // --- Ürün bağlamı: teklif düğmesi etiketi, bağlam çipi, ürün grupları vurgusu -------------------------
  const teklifEtiket = $('[data-teklif-etiket] > span:first-child');
  const baglamCip = $('[data-baglam-cip]');
  function baglamYaz() {
    const u = baglam.urun();
    const ad = baglam.ad();
    if (teklifEtiket) {
      if (u) teklifEtiket.textContent = dil() === 'en' ? `Get a quote for ${ad}` : `${ad} için teklif alın`;
      else teklifEtiket.innerHTML = dil() === 'en' ? EN['cta.sistem'] : teklifEtiket.dataset.tr || teklifEtiket.innerHTML;
    }
    if (baglamCip) {
      baglamCip.hidden = !u;
      const b = $('[data-baglam-ad]', baglamCip);
      if (b) b.textContent = ad;
    }
    for (const a of $$('.eg-urun')) {
      const bakti = !!u && a.dataset.urun === u;
      a.classList.toggle('is-baktiginiz', bakti);
      if (bakti) a.dataset.etiket = dil() === 'en' ? EN['sonra.baktiginiz'] : 'Hikâyede baktığınız';
      else delete a.dataset.etiket;
    }
    baglam.linkleriGuncelle(sonUst);
  }
  let sonUst = 'hikaye';
  baglam.onDegis(baglamYaz);
  document.addEventListener('ege:dil', baglamYaz);
  const cipSil = $('[data-baglam-sil]');
  if (cipSil) cipSil.addEventListener('click', () => baglam.sil());

  // --- Tıklamalar: ölçüm (data-iz), kitle, atla, durak çipleri, tekrar izle, paylaş, iç bağlantılar ---------------------
  document.addEventListener('click', (e) => {
    const a = e.target.closest('[data-iz]');
    if (a) {
      const veri = { hedef: a.dataset.iz };
      if (a.dataset.kitle) veri.kitle = a.dataset.kitle;
      if (a.dataset.urun) veri.urun = a.dataset.urun;
      iz('ege_tik', veri, true);
      if (a.dataset.kitle) iz('ege_kitle', { kitle: a.dataset.kitle, yer: /^son/.test(a.dataset.iz) ? 'son' : 'giris' });
      if (a.dataset.urun) baglam.cipTik(a.dataset.urun);
    }
    const d = e.target.closest('[data-durak]');
    if (d) {
      baglam.cipTik(d.dataset.durak);
      if (saniyeyeGit(+d.dataset.git)) e.preventDefault();
      return;
    }
    const atla = e.target.closest('[data-atla]');
    if (atla) {
      iz('ege_atla', { nokta: 'giris', t_atlanan: Math.round(baglam.enYuksek()) });
      if (saniyeyeGit(FINALE_CTA_SN)) e.preventDefault();
      return;
    }
    const tekrar = e.target.closest('[data-tekrar]');
    if (tekrar) {
      iz('ege_tekrar', {});
      const akis = $('[data-akis]');
      if (akis && !ortak.azHareket) {
        e.preventDefault();
        window.scrollTo({ top: akis.getBoundingClientRect().top + window.scrollY, behavior: 'auto' });
      }
      return;
    }
    const ic = e.target.closest('a[href^="#sahne-"]');
    if (ic && !ic.closest('.eg-yol') && ortak.sahneyeGit) {
      if (ortak.sahneyeGit(ic.getAttribute('href').slice(7))) e.preventDefault();
    }
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
    const et = btn.querySelector('.eg-nokta__etiket');
    if (!et) return;
    const ad = KITA[id] ? KITA[id][dil()] : metin(id)[0];
    et.textContent = ad;
    if (!btn.hasAttribute('aria-hidden')) btn.setAttribute('aria-label', ad);
  }

  /** Sahneye bağlı nokta öğesi: tür NOKTA_SAHNE'den; listede olmayan anahtarlar gizli kalır (ör. s0'da yalnız Sokak ve Eskiz). */
  ortak.noktaOlustur = (id, sahne) => {
    const tur = (NOKTA_SAHNE[sahne.id] || {})[id];
    if (!tur) {
      const gizli = document.createElement('span');
      gizli.className = 'eg-nokta is-gizli';
      gizli.hidden = true;
      return gizli;
    }
    const sabit = tur === 'kita' || tur === 'etiket';
    const el = document.createElement(sabit ? 'span' : 'button');
    el.className = `eg-nokta is-gizli${tur === 'kita' ? ' eg-nokta--kita' : tur.startsWith('etiket') ? ' eg-nokta--etiket' : ''}${sabit ? ' eg-nokta--sabit' : ''}`;
    el.dataset.nokta = id;
    if (sabit) {
      el.setAttribute('aria-hidden', 'true');
      el.inert = true; // etiket tıklanmaz, odak almaz
    } else {
      el.type = 'button';
      el.tabIndex = -1;
    }
    el.innerHTML = '<span class="eg-nokta__halka" aria-hidden="true"></span><span class="eg-nokta__etiket"></span>';
    etiketYaz(el, id);
    if (!sabit) {
      el.addEventListener('click', (e) => {
        e.stopPropagation();
        if (acikId === id) kartKapat();
        else kartAc(id, el, sahne);
      });
    }
    return el;
  };

  ortak.noktaGizlendi = (id) => {
    if (acikId === id) kartKapat();
  };

  function kartAc(id, btn, sahne) {
    if (!kart) return;
    const d = NOKTALAR[id] || {};
    const [baslik, aciklama, kaynak] = metin(id);
    kart.querySelector('[data-kart-baslik]').textContent = baslik;
    kart.querySelector('[data-kart-metin]').textContent = aciklama;
    const k = kart.querySelector('[data-kart-kaynak]');
    k.hidden = !kaynak;
    k.textContent = kaynak ? `${dil() === 'en' ? EN.kaynak : 'Kaynak'}: ${kaynak}` : '';
    // ürün kartlarında: ürün sayfası + teknik föy (bağlam parametreli; yalnız kullanıcı noktaya dokununca)
    const l = kart.querySelector('[data-kart-linkler]');
    l.hidden = !d.urun;
    l.textContent = '';
    if (d.urun) {
      const lenkler = [
        [URUN[d.urun].yol, EN['kart.urun'], 'Ürün sayfası', `s1_${d.urun}_kart`],
        ['/teknik-foyler/', EN['kart.foy'], 'Teknik föy', `s1_${d.urun}_foy`],
      ];
      for (const [yol, en, tr, nokta] of lenkler) {
        const a = document.createElement('a');
        a.href = baglam.baglantiYap(yol, { nokta, urun: d.urun });
        a.dataset.iz = nokta;
        a.dataset.urun = d.urun;
        a.textContent = `${dil() === 'en' ? en : tr} →`;
        l.appendChild(a);
      }
    }
    const r = btn.getBoundingClientRect();
    const sr = sahne.sabit.getBoundingClientRect();
    const x = Math.min(Math.max(16, r.left - sr.left + 26), sr.width - 336);
    const y = Math.min(Math.max(72, r.top - sr.top - 12), sr.height - 240);
    sahne.sabit.appendChild(kart);
    kart.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    kart.hidden = false;
    acikId = id;
    acikSahne = sahne;
    btn.setAttribute('aria-expanded', 'true');
    kart.querySelector('[data-kart-kapat]').focus({ preventScroll: true });
    iz('ege_nokta', { nokta: id, kaynak: 'dokun' });
    if (d.urun) baglam.kartAcildi(d.urun);
  }

  function kartKapat() {
    if (!kart || kart.hidden) return;
    kart.hidden = true;
    if (acikSahne) {
      const btn = acikSahne.noktalar.get(acikId);
      if (btn) btn.setAttribute('aria-expanded', 'false');
    }
    acikId = null;
    acikSahne = null;
  }

  if (kart) {
    kart.querySelector('[data-kart-kapat]').addEventListener('click', kartKapat);
    document.addEventListener('click', (e) => {
      if (!kart.hidden && !kart.contains(e.target)) kartKapat();
    });
    // kilit yok: kaydırma kartı kapatır (kart noktayı izlemez), sayfa aynı jestle kayar
    window.addEventListener('scroll', kartKapat, { passive: true });
  }
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    kartKapat();
    menuKapat();
    if (yol) {
      yolBtn.setAttribute('aria-expanded', 'false');
      yol.classList.remove('is-acik');
    }
  });

  // --- Yolculuk çubuğu: 7 bölüm (bölüm adı + ilerleme; dokununca liste) + Paylaş ---------------------------
  const yol = $('[data-yolculuk]');
  const yolDolgu = yol ? $('[data-yol-dolgu]', yol) : null;
  const yolAd = yol ? $('[data-yol-ad]', yol) : null;
  const yolBtn = yol ? $('[data-yol-ac]', yol) : null;
  let sonAd = '';
  const YOL_TR = { s0: 'Hayal', s1: 'Ürünler', s2: 'Üretim', s3: 'Yapı', s4: 'Yol', s5: 'Dünya', son: 'Teklif' };
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
    for (const a of $$('a[data-yol-hedef]', yol)) {
      a.addEventListener('click', (e) => {
        yolBtn.setAttribute('aria-expanded', 'false');
        yol.classList.remove('is-acik');
        const h = a.dataset.yolHedef;
        // sahneler tek yapışkan akışın içinde: bağlantı yerine akıştaki konuma kaydır; "Teklif" finale CTA'larının göründüğü ana iner
        const gitti = h === 'son' ? saniyeyeGit(FINALE_CTA_SN) : ortak.sahneyeGit && ortak.sahneyeGit(h);
        if (gitti) e.preventDefault();
        if (h === 'son') iz('ege_atla', { nokta: 'yol', t_atlanan: Math.round(baglam.enYuksek()) });
      });
    }
    const paylas = $('[data-paylas]', yol);
    if (paylas && navigator.share) {
      paylas.parentElement.hidden = false;
      paylas.addEventListener('click', () => {
        // temiz adres (kaynak/ürün parametresi eklenmez)
        navigator.share({ title: document.title, url: location.href.split(/[?#]/)[0] }).catch(() => {});
      });
    }
  }

  // --- Finale etkinken: dünya parçasının nokta/sayaç/perdesi kapanır (CSS .finale-aktif) -----------------------
  document.addEventListener('ege:finale', (e) => kok.classList.toggle('finale-aktif', !!(e.detail && e.detail.aktif)));

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

  // --- Zamana bağlı öğeler (guncelle içinde yalnız değişince yazılır) ------------------------------------
  const heroEylem = [$('[data-giris-eylem]'), $('.eg-giris__alt')].filter(Boolean);
  let heroOp = -1;
  const durakCubugu = $('[data-durak-cubugu]');
  const durakDugmeler = durakCubugu ? $$('[data-durak]', durakCubugu) : [];
  let durakKey = '';
  const kitaSayac = $('[data-kita-sayac]');
  const kitaHalkalar = kitaSayac ? $$('[data-halka]', kitaSayac) : [];
  const kitaSay = kitaSayac ? $('[data-kita-say]', kitaSayac) : null;
  let sayacKey = '';
  const dunya = sahneler.find((s) => s.id === 's5');
  const KITA_SIRA = Object.keys(KITA); // varış sırası: Avrupa, Afrika, Amerika, Asya, Okyanusya
  const varisP = (id) => KITA[id].varis / (KITA_KARE - 1);
  let gorYapildi = false;

  function zamanOgeleri(t, durum) {
    if (ortak.azHareket) return;
    // ana CTA durumu: ekranda tek lime düğme (üst çubuk düğmesi çizgili olur)
    const ana = ANA_CTA.some(([a, b]) => t >= a && t < b);
    if (ana !== kok.classList.contains('ana-cta-acik')) kok.classList.toggle('ana-cta-acik', ana);
    // hero: düğme/çip/atla t=1'de soluklaşır (H1 + cümle kalır; onları sahne giriş perdesi söndürür)
    const op = Math.round((1 - smooth(0.25, 1.0, t)) * 100) / 100;
    if (op !== heroOp) {
      heroOp = op;
      for (const el of heroEylem) {
        el.style.opacity = String(op);
        el.style.visibility = op < 0.02 ? 'hidden' : '';
      }
    }
    // s1 ürün çip çubuğu: t=34–66; geçerli durak vurgulu, biten duraklar işaretli
    if (durakCubugu) {
      const goster = durum.gorunur !== false && t >= DURAK_PENCERE[0] && t < DURAK_PENCERE[1];
      let aktif = '';
      for (const [kod, a, b] of DURAKLAR) if (t >= a && t < b) aktif = kod;
      const key = `${goster ? 1 : 0}|${aktif}|${Math.floor(t >= 66)}|${DURAKLAR.filter((d) => t >= d[2]).length}`;
      if (key !== durakKey) {
        durakKey = key;
        durakCubugu.classList.toggle('is-gorunur', goster);
        for (const b of durakDugmeler) {
          const d = DURAKLAR.find((x) => x[0] === b.dataset.durak);
          b.classList.toggle('is-aktif', b.dataset.durak === aktif);
          b.classList.toggle('is-bitti', t >= d[2]);
          if (b.dataset.durak === aktif) b.setAttribute('aria-current', 'step');
          else b.removeAttribute('aria-current');
        }
      }
    }
    // dünya: kıta etiketi (varışta 1,6 sn) ve 5 halkalı sayaç
    if (dunya && dunya.visible) {
      const p = dunya.p;
      const sure = KITA_SURE_SN / DUNYA_SN;
      let dolu = 0;
      for (const id of KITA_SIRA) {
        const a = varisP(id);
        if (p >= a) dolu++;
        const el = dunya.noktalar.get(id);
        if (el) el.classList.toggle('is-kita-acik', p >= a && p < a + sure);
      }
      const goster = t >= SAYAC_PENCERE[0] && t < SAYAC_PENCERE[1];
      const key = `${goster ? 1 : 0}|${dolu}`;
      if (kitaSayac && key !== sayacKey) {
        sayacKey = key;
        kitaSayac.classList.toggle('is-gorunur', goster);
        kitaHalkalar.forEach((h, i) => h.classList.toggle('is-dolu', i < dolu));
        if (kitaSay) kitaSay.textContent = String(dolu);
      }
    }
  }

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

  baglamYaz();

  return {
    kartAc,
    kartKapat,
    baglam,
    iz,
    guncelle(list, durum) {
      const t = durum.saniye;
      baglam.zaman(t, performance.now(), durum);
      if (!gorYapildi && list[0] && list[0].el.classList.contains('is-hazir')) {
        gorYapildi = true;
        iz('ege_hikaye_gor', { varyant: list[0].variant, hareket: ortak.azHareket ? 'az' : 'normal', ekran: window.innerWidth < 480 ? 0 : window.innerWidth < 761 ? 1 : window.innerWidth < 1281 ? 2 : 3 });
      }
      zamanOgeleri(t, durum);
      // üst çubuktaki Teklif Al: hikâye ekranda iken kaynak=hikaye, değilken kaynak=ust
      const ustK = durum.gorunur ? 'hikaye' : 'ust';
      if (ustK !== sonUst) {
        sonUst = ustK;
        baglam.linkleriGuncelle(sonUst);
      }
      if (yol) {
        // yolculuk çubuğu t=2'den itibaren (hero sakin kalsın) hikâye ekrandayken görünür
        const on = !ortak.azHareket && durum.gorunur && t >= 2;
        yol.classList.toggle('is-gorunur', !!on);
        if (on) {
          yolDolgu.style.transform = `scaleX(${durum.ilerleme.toFixed(4)})`;
          const s = list[durum.aktif];
          const ad = s ? (s.id === 'finale' ? 'son' : s.id) : '';
          if (ad !== sonAd) {
            sonAd = ad;
            yolAdYaz();
            for (const a of $$('[data-yol-hedef]', yol)) a.classList.toggle('is-aktif', a.dataset.yolHedef === ad);
          }
        }
      }
      hudVis = list.map((s) => s.visible);
    },
  };
}
