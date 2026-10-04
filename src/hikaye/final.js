/**
 * Finale (son bölüm, 136–146 sn) — 2B kanvas efektleri ve canlı gözenek katmanının yaşam döngüsü.
 *
 * Akış (p = finale ilerlemesi 0..1; 1 film sn = 0,1 p; plan docs/plan/akt-son.json, denetim düzeltmeli):
 *   0,00–0,20 (t 136–138)  s5'in SON karesi üzerinde küre erir; dünyanın ışıkları Ege'ye (İzmir/Söke) akar, tek kor ışıması büyür
 *   0,20–0,30 (t 138–139)  "Güven." (HTML) · kıvılcım 1 Hz nabız atar, kor parçacıkları yükselir
 *   0,30–0,40 (t 139–140)  46 ışınlık patlama; kıvılcım logonun dört köşe çizgisini çizer (lime)
 *   0,40–0,50 (t 140–141)  logo + slogan "Bugünden Yarına Güvenle" (HTML); canlı gözenek katmanı merkezden dışa açılır
 *   0,50–1,00 (t 141–146)  logo küçülür; teklif başlığı → ana CTA + ikincil (142) → kitle çipleri (143) → 3 kanıt kartı (144) → baştan izle (145)
 *
 * Sözleşme (motor): finalKur(ortak) → { konumla(p), ciz(ctx, w, h, p, dpr) }
 *   • konumla: finale etkinken her karede (DOM evresi, canlı katman yaşam döngüsü)
 *   • ciz: ana kanvasta s5'in son karesi çizildikten SONRA çağrılır; tuval piksel boyutunda, 2B bağlam (blend yalnız tuval içi 'lighter')
 * Büyük logo YALNIZ burada görünür (üst çubuktaki yer tutucu logo hariç). WebGL yalnız finale etkinken ve boşta, DPR ≤ 1,25 (src/canli).
 */

const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
const smooth = (a, b, x) => {
  const t = clamp01((x - a) / (b - a));
  return t * t * (3 - 2 * t);
};
const easeIn = (x) => x * x * (1.6 - 0.6 * x);

/** Küçük, tohumlu rastgele sayı üreteci (her açılışta aynı kompozisyon). */
function mulberry32(a) {
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * s5 son karesinde (F192) İzmir'in konumu ve kürenin merkez/yarıçapı (görüntü oranı 0..1; yarıçap görüntü genişliğine oranlı).
 * blender/s4_dunya.py kamerasından hesaplandı (d=9, 50 mm / telefon 5,9 m, 36 mm; kaydırma d −0,17, m +0,16). Kareler meta'sında son karede
 * 'ege' (ya da 'kaynak') çapası varsa o kullanılır.
 */
const EGE = { d: [0.6045, 0.432], m: [0.4234, 0.565] };
const KURE = { d: { c: [0.67, 0.487], r: 0.1554 }, m: { c: [0.5, 0.5854], r: 0.172 } };
/** Logo köşe çizgileri (logo SVG'sinin viewBox 300×190 birimleri): saat yönünde sol-üst, sağ-üst, sağ-alt, sol-alt. */
const KOSELER = [
  [[5, 54], [5, 5], [54, 5]],
  [[246, 5], [295, 5], [295, 54]],
  [[295, 136], [295, 185], [246, 185]],
  [[54, 185], [5, 185], [5, 136]],
];
const LOGO_W = 300;
const LOGO_H = 190;
const SICAK = '255, 214, 150'; // s0 pencere ışığının sıcak tonu
const LIME = '162, 191, 55';
const PARCACIK = 64;

export function finalKur(ortak) {
  const el = document.querySelector('[data-sahne="finale"]');
  const canliKok = el ? el.querySelector('[data-canli-kok]') : null;
  const marka = el ? el.querySelector('.eg-final__marka') : null;
  let faz = -1;
  let canliDurum = 'yok'; // yok | hazirlaniyor | hazir | acik
  let betikYuklendi = false;
  let kapatZamani = 0;
  let sonKlip = '';
  let parcaciklar = null;
  let kutu = null;
  let kutuAnahtar = '';

  // ------------------------------------------------------------------ canlı gözenek katmanı
  /** canli.js (≈0,5 MB): s4 sonundan itibaren boşta indirilir; veri tasarrufu ve hareket azaltmada hiç. */
  function betikYukle() {
    if (betikYuklendi || ortak.azHareket || !canliKok) return;
    const baglanti = navigator.connection;
    if (baglanti && baglanti.saveData) return;
    betikYuklendi = true;
    const sc = document.createElement('script');
    sc.src = 'assets/js/canli.js';
    sc.async = true;
    document.body.appendChild(sc);
  }
  if (typeof ortak.abone === 'function') {
    ortak.abone((d) => {
      if (!betikYuklendi && d.saniye >= 116) betikYukle();
    });
  }

  const canli = () => window.EgeCanli || null;

  function canliHazirla() {
    if (canliDurum !== 'yok') return;
    const c = canli();
    if (!c) return; // betik henüz inmedi: sonraki karede yeniden denenir
    canliDurum = 'hazirlaniyor';
    // WebGL bağlamı ve gölgelendirici derlemesi boşta (ilk render finale t ≥ 138)
    const is = () => {
      if (canliDurum !== 'hazirlaniyor') return;
      canliDurum = c.hazirla() ? 'hazir' : 'yok';
      if (canliDurum === 'yok') canliDurum = 'hata';
    };
    if (typeof requestIdleCallback === 'function') requestIdleCallback(is, { timeout: 500 });
    else setTimeout(is, 60);
  }

  function klipYaz(oran) {
    const k = oran <= 0 ? 'circle(0% at 50% 46%)' : oran >= 1 ? 'none' : `circle(${(oran * 78).toFixed(1)}% at 50% 46%)`;
    if (k !== sonKlip && canliKok) {
      canliKok.style.clipPath = k;
      sonKlip = k;
    }
  }

  function canliKapat(hemen) {
    clearTimeout(kapatZamani);
    const c = canli();
    if (c && (canliDurum === 'acik' || canliDurum === 'hazir')) c.uyut();
    if (canliKok) canliKok.classList.remove('is-acik');
    klipYaz(0);
    if (canliDurum === 'acik') canliDurum = 'hazir';
    const bitir = () => {
      const cc = canli();
      if (cc) cc.kapat();
      canliDurum = 'yok';
    };
    if (canliDurum === 'yok' || canliDurum === 'hata') return;
    // WebGL bağlamı finale dışında tutulmaz; hızlı ileri-geri kaydırmada boşuna yıkılmasın diye kısa bekleme
    if (hemen) bitir();
    else kapatZamani = setTimeout(bitir, 1500);
  }

  document.addEventListener('ege:finale', (e) => {
    if (!(e.detail && e.detail.aktif)) canliKapat(false);
  });

  // ------------------------------------------------------------------ DOM evresi + canlı katman
  function konumla(p) {
    if (!el) return;
    const f = p < 0.2 ? 0 : p < 0.3 ? 1 : p < 0.4 ? 2 : p < 0.5 ? 3 : 4;
    if (f !== faz) {
      faz = f;
      el.dataset.faz = String(f);
    }
    if (!canliKok || ortak.azHareket) return;
    clearTimeout(kapatZamani);
    if (!betikYuklendi) betikYukle();
    if (p >= 0.2) canliHazirla();
    if (p < 0.2) {
      if (canliDurum === 'hazir' || canliDurum === 'acik') canliKapat(false);
      return;
    }
    const c = canli();
    if (p >= 0.4 && c && (canliDurum === 'hazir' || canliDurum === 'acik')) {
      if (canliDurum === 'hazir') {
        c.ac();
        canliDurum = 'acik';
        canliKok.classList.add('is-acik');
      }
      klipYaz(smooth(0.4, 0.56, p));
    } else if (p < 0.4 && canliDurum === 'acik') {
      c.uyut();
      canliDurum = 'hazir';
      canliKok.classList.remove('is-acik');
      klipYaz(0);
    }
  }

  // ------------------------------------------------------------------ 2B efektler
  function s5() {
    return (ortak.sahneler || []).find((s) => s.id === 's5') || null;
  }

  /** Görüntü koordinatı (0..1) → tuval pikseli (cover uyumu: sahne.fit ile aynı). */
  function yerlesim(w, h) {
    const s = s5();
    const v = s && s.variant === 'm' ? 'm' : 'd';
    const fit = s && s.fit;
    const dpr = fit ? fit.dpr : w / Math.max(1, window.innerWidth);
    const iw = fit ? fit.iw : 1600;
    const ih = fit ? fit.ih : 900;
    const sc = fit ? fit.s : Math.max(w / dpr / iw, h / dpr / ih);
    const dx = fit ? fit.dx : (w / dpr - iw * sc) / 2;
    const dy = fit ? fit.dy : (h / dpr - ih * sc) / 2;
    const nokta = (u, vv) => [(dx + u * iw * sc) * dpr, (dy + vv * ih * sc) * dpr];
    // İzmir: meta'nın son karesinde 'ege'/'kaynak' çapası varsa o
    let ege = EGE[v];
    if (s && s.v && s.hsAnahtar && s.hsAnahtar.length) {
      const son = s.v.hotspots[s.hsAnahtar[s.hsAnahtar.length - 1]];
      const q = son && (son.ege || son.kaynak);
      if (q) ege = q;
    }
    const kure = KURE[v];
    return { nokta, ege: nokta(ege[0], ege[1]), merkez: nokta(kure.c[0], kure.c[1]), r: kure.r * iw * sc * dpr, dpr };
  }

  function parcaciklarKur() {
    const r = mulberry32(1907);
    const a = [];
    for (let i = 0; i < PARCACIK; i++) {
      a.push({
        aci: i * 2.399963 + r() * 0.4, // altın açı: eşit dağılım
        yar: Math.sqrt((i + 0.5) / PARCACIK) * (0.55 + r() * 0.6),
        gecikme: r() * 0.45,
        egri: (r() - 0.5) * 0.9,
        boy: 0.7 + r() * 1.1,
      });
    }
    return a;
  }

  /** Logonun BÜYÜK (ortalı) durumundaki SVG kutusu (CSS px): konum DOM dönüşümünden bağımsız hesaplanır. */
  function logoKutu() {
    if (!marka) return null;
    const anahtar = `${window.innerWidth}x${window.innerHeight}|${marka.offsetWidth}x${marka.offsetHeight}`;
    if (anahtar === kutuAnahtar && kutu) return kutu;
    const W = marka.offsetWidth;
    const Hm = marka.offsetHeight;
    kutu = { x: window.innerWidth / 2 - W / 2, y: window.innerHeight / 2 - Hm / 2, w: W, h: (W * LOGO_H) / LOGO_W };
    kutuAnahtar = anahtar;
    return kutu;
  }

  /** Işıma noktası: iç çekirdek + yumuşak hale (tuval içi 'lighter' birleştirme; CSS blend yok). */
  function isima(ctx, x, y, yaricap, alfa, renk = SICAK) {
    const g = ctx.createRadialGradient(x, y, 0, x, y, yaricap);
    g.addColorStop(0, `rgba(255, 250, 235, ${alfa})`);
    g.addColorStop(0.18, `rgba(${renk}, ${alfa * 0.85})`);
    g.addColorStop(1, `rgba(${renk}, 0)`);
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(x, y, yaricap, 0, Math.PI * 2);
    ctx.fill();
  }

  function ciz(ctx, w, h, p, dpr) {
    if (p < 0) return;
    const L = yerlesim(w, h);
    const k = L.dpr || dpr || 1;
    // 1) küre erir: yalnız Ege'nin ışığı kalır (s5 son karesi karartılır; yıldızlar kararır)
    const karar = 0.86 * smooth(0, 0.2, p);
    if (karar > 0.001) {
      ctx.fillStyle = `rgba(8, 13, 17, ${karar.toFixed(3)})`;
      ctx.fillRect(0, 0, w, h);
    }
    const kb = logoKutu();
    const [ox, oy] = L.ege;
    // t=138: kıvılcım Ege'den ekranın ortasına (logo çerçevesinin merkezine) süzülür; "Güven." orada belirir
    const gt = smooth(0.2, 0.29, p);
    const mx = kb ? (kb.x + kb.w / 2) * k : ox;
    const my = kb ? (kb.y + kb.h / 2) * k : oy;
    const ex = ox + (mx - ox) * gt;
    const ey = oy + (my - oy) * gt;
    ctx.globalCompositeOperation = 'lighter';
    // 2) dünyanın ışıkları Ege'ye akar (2 px kuyruk, ease-in)
    if (p < 0.24) {
      if (!parcaciklar) parcaciklar = parcaciklarKur();
      const ilk = clamp01(p / 0.2);
      const [ex0, ey0] = L.ege;
      ctx.lineCap = 'round';
      for (const q of parcaciklar) {
        const u = clamp01((ilk - q.gecikme) / (1 - q.gecikme));
        if (u <= 0) continue;
        const sx = L.merkez[0] + Math.cos(q.aci) * q.yar * L.r * 1.25;
        const sy = L.merkez[1] + Math.sin(q.aci) * q.yar * L.r * 1.25;
        const dxv = ex0 - sx;
        const dyv = ey0 - sy;
        const nx = -dyv;
        const ny = dxv;
        const nok = (t) => {
          const e = easeIn(t);
          const eg = Math.sin(Math.PI * t) * q.egri;
          return [sx + dxv * e + nx * eg * 0.35, sy + dyv * e + ny * eg * 0.35];
        };
        const [x1, y1] = nok(u);
        const [x0, y0] = nok(Math.max(0, u - 0.09));
        const alfa = Math.min(1, u * 5) * (1 - smooth(0.9, 1, u)) * 0.9;
        ctx.strokeStyle = `rgba(${SICAK}, ${alfa.toFixed(3)})`;
        ctx.lineWidth = q.boy * 1.4 * k;
        ctx.beginPath();
        ctx.moveTo(x0, y0);
        ctx.lineTo(x1, y1);
        ctx.stroke();
      }
    }
    // 3) Ege'de tek kıvılcım: kor büyür, sonra 1 Hz nabız (1 film sn = 0,1 p)
    const buyume = smooth(0.06, 0.2, p);
    const nabiz = p < 0.2 ? 0 : 0.5 + 0.5 * Math.sin((p - 0.2) * 10 * Math.PI * 2 - Math.PI / 2);
    const sonuk = 1 - smooth(0.36, 0.46, p);
    const yar = (7 + 24 * buyume + 12 * nabiz * (p < 0.4 ? 1 : 0)) * k;
    if (sonuk > 0.01) isima(ctx, ex, ey, yar, 0.95 * sonuk);
    // kor parçacıkları yavaşça yükselir (t 138–140)
    if (p >= 0.2 && p < 0.42) {
      const r = mulberry32(138);
      for (let i = 0; i < 12; i++) {
        const evre = (((p - 0.2) * 5 + i / 12) % 1 + 1) % 1;
        const sapma = (r() - 0.5) * 36 * k;
        const x = ex + sapma + Math.sin(evre * 6 + i) * 6 * k;
        const y = ey - evre * 70 * k;
        const a = Math.sin(Math.PI * evre) * 0.75 * (1 - smooth(0.36, 0.42, p));
        ctx.fillStyle = `rgba(${SICAK}, ${a.toFixed(3)})`;
        ctx.beginPath();
        ctx.arc(x, y, (1.1 + r() * 1.2) * k, 0, Math.PI * 2);
        ctx.fill();
      }
    }
    // 4) 46 ışınlık kısa patlama (s0 t=1 ile aynı), 5) kıvılcım logonun köşe çizgilerini çizer
    if (p >= 0.3 && p < 0.37) {
      const u = (p - 0.3) / 0.07;
      const uzun = (0.06 + 0.07 * smooth(0, 1, u)) * Math.min(w, h * 1.3);
      ctx.lineWidth = 1.4 * k;
      for (let i = 0; i < 46; i++) {
        const a = (i / 46) * Math.PI * 2 + 0.05 * Math.sin(i * 3.1);
        const bas = uzun * 0.1;
        const son = uzun * (0.35 + 0.65 * ((i * 37) % 11) / 11);
        ctx.strokeStyle = `rgba(${SICAK}, ${((1 - u) * 0.7).toFixed(3)})`;
        ctx.beginPath();
        ctx.moveTo(ex + Math.cos(a) * bas, ey + Math.sin(a) * bas);
        ctx.lineTo(ex + Math.cos(a) * son, ey + Math.sin(a) * son);
        ctx.stroke();
      }
    }
    if (p >= 0.3 && p < 0.5 && kb) {
      const olcek = (kb.w / LOGO_W) * k;
      const pt = (v) => [kb.x * k + v[0] * olcek, kb.y * k + v[1] * olcek];
      ctx.lineCap = 'butt';
      ctx.lineJoin = 'miter';
      ctx.lineWidth = 9 * olcek;
      const g = clamp01((p - 0.3) / 0.1); // dört ışık birlikte: ilk %30 köşeye uçuş (çizgisiz), kalanı L çizimi
      const solma = 1 - smooth(0.46, 0.5, p); // logo küçülmeden önce çizgiler söner (HTML logonun kendi köşeleri kalır)
      for (let b = 0; b < 4; b++) {
        const seg = KOSELER[b].map(pt);
        const u1 = Math.hypot(seg[1][0] - seg[0][0], seg[1][1] - seg[0][1]);
        const u2 = Math.hypot(seg[2][0] - seg[1][0], seg[2][1] - seg[1][1]);
        // polyline üzerinde uzunluğa göre nokta
        const konum = (t) => (t <= u1
          ? [seg[0][0] + ((seg[1][0] - seg[0][0]) * t) / u1, seg[0][1] + ((seg[1][1] - seg[0][1]) * t) / u1]
          : [seg[1][0] + ((seg[2][0] - seg[1][0]) * (t - u1)) / u2, seg[1][1] + ((seg[2][1] - seg[1][1]) * (t - u1)) / u2]);
        let bas;
        if (g < 0.3) {
          const e = smooth(0, 1, g / 0.3);
          bas = [mx + (seg[0][0] - mx) * e, my + (seg[0][1] - my) * e];
        } else {
          const tt = (u1 + u2) * smooth(0, 1, (g - 0.3) / 0.7);
          bas = konum(tt);
          ctx.strokeStyle = `rgba(${LIME}, ${(0.95 * solma).toFixed(3)})`;
          ctx.beginPath();
          ctx.moveTo(seg[0][0], seg[0][1]);
          if (tt > u1) ctx.lineTo(seg[1][0], seg[1][1]);
          ctx.lineTo(bas[0], bas[1]);
          ctx.stroke();
        }
        if (g < 1) isima(ctx, bas[0], bas[1], 15 * k, 0.9);
        else if (p < 0.46) isima(ctx, bas[0], bas[1], 13 * k * (1 - smooth(0.4, 0.46, p)), 0.8);
      }
    }
    ctx.globalCompositeOperation = 'source-over';
  }

  return { konumla, ciz };
}
