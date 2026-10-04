/**
 * Pazarlama bağlamı: bağlantı şeması, ürün bağlamı ve dataLayer ölçümü (docs/plan/pazarlama.json).
 *
 *  • Bağlantı şeması: {yol}?kaynak=hikaye&dil={tr|en}[&urun=][&kitle=][&nokta=] (+ gelen utm_*). Statik href'ler TEMİZ kalır
 *    (arama motoru ve JS'siz görünüm parametre görmez); JS bağlam değişince [data-link] öğelerinin href'ini günceller.
 *  • Ürün bağlamı (urun) yalnız ÖLÇÜLMÜŞ ilgiden gelir ve YALNIZ BELLEKTE durur (çerez/localStorage/sessionStorage yok):
 *    skor = durakta görünür süre (sn, durak başına en çok 20) + 8 × açılan nokta kartı + 15 × ürün çipi/bağlantı tıklaması;
 *    en yüksek skor kazanır (eşitlikte en son bakılan), eşik 5. Hikâye atlandıysa bağlam yoktur.
 *  • Olaylar yalnız window.dataLayer bir dizi ise push edilir (ağ çağrısı/sendBeacon yok); kare başı iş yok: kuyruk boşta boşaltılır.
 *    Parametreler sayı ya da sabit sözlükten kod; serbest metin, URL sorgusu, kimlik yok.
 */
import { dil, URUN, EN } from './dil.js';

/** Ürün durakları (film sn, [başlangıç, bitiş)): s1 ürün turu. */
export const DURAKLAR = [
  ['duvar', 36, 41],
  ['lento', 41, 46],
  ['ublok', 46, 51],
  ['tutkal', 51, 56],
  ['panel', 56, 62],
  ['egepor', 62, 66],
];

/** Hikâyeden çıkan bağlantılardaki kaynak adı; hikâye ekranda değilken üst çubuk 'ust' olur. */
const KAYNAK = 'hikaye';
const ESIK_SKOR = 5;
const DURAK_TAVAN_SN = 20;
/** ege_ilerleme eşikleri (film sn): ilk ulaşılışta, ileri yönde, oturumda bir kez. */
const ILERLEME = [5, 10, 20, 28, 32, 45, 60, 70, 90, 104, 120, 130, 136, 140, 142, 146];
/** ege_sahne girişleri (film sn). */
const SAHNE_GIRIS = [[32, 's1'], [70, 's2'], [90, 's3'], [104, 's4'], [120, 's5'], [136, 'finale']];
/** CTA pencereleri (film sn): ege_cta_gor ilk görünüşte bir kez (plan cta_zaman_cizelgesi; denetim düzeltmeli). */
const CTA_PENCERE = [
  ['giris_teklif', 0, 2], ['s0_tir_urunler', 30, 32], ['s1_duvar_hesapla', 38, 41], ['s1_sistem_teklif', 64, 67], ['s3_muhur_foy', 100, 102],
  ['s4_olcek_bayi', 115.6, 117.6], ['s5_ihracat', 131.5, 134], ['son_teklif', 142, 146], ['son_kitle', 143, 146],
];
const OLAY_TAVAN = 80;

const yuvarla = (x) => Math.round(x);

export function baglamKur({ ortak }) {
  const dl = () => (Array.isArray(window.dataLayer) ? window.dataLayer : null);
  const skor = Object.fromEntries(DURAKLAR.map((d) => [d[0], 0]));
  const sira = []; // en son bakılanlar (eşitlikte kazanır)
  let urun = null;
  let susturuldu = false; // kullanıcı bağlam çipini sildiyse yeni ilgi gelene dek geri dönmez
  let degisti = () => {};
  let sonSn = 0;
  let sonMs = 0;
  let enYuksek = 0;
  let basladi = false;
  const goruldu = new Set();
  const kuyruk = [];
  let olaySayisi = 0;
  let bosta = 0;
  const hizOrnek = []; // [ms, film sn]: son 3 sn kaydırma hızı

  // --- Olaylar ---------------------------------------------------------------
  function hiz() {
    if (hizOrnek.length < 2) return 'normal';
    const a = hizOrnek[0];
    const b = hizOrnek[hizOrnek.length - 1];
    const dt = (b[0] - a[0]) / 1000;
    if (dt < 0.3) return 'normal';
    const v = Math.abs(b[1] - a[1]) / dt; // 1× = 1 film sn / gerçek sn (22 vh/sn)
    return v < 0.5 ? 'yavas' : v > 2 ? 'hizli' : 'normal';
  }

  function sahneAdi() {
    const t = ortak.saniye ? ortak.saniye() : 0;
    const i = ortak.parcaIndeksi ? ortak.parcaIndeksi(t) : 0;
    return ['s0', 's1', 's2', 's3', 's4', 's5', 'finale'][i] || 's0';
  }

  function bosalt() {
    bosta = 0;
    const d = dl();
    while (kuyruk.length) {
      const o = kuyruk.shift();
      if (d) d.push(o);
    }
  }

  /** Olay kuyruğa alınır, boşta dataLayer'a yazılır. Kullanıcı eylemleri (tık) sınırı aşmaz. */
  function iz(olay, veri = {}, acil = false) {
    if (!dl()) return;
    if (olay !== 'ege_tik' && olay !== 'ege_cikis' && ++olaySayisi > OLAY_TAVAN) return;
    const o = { event: olay, dil: dil(), t: yuvarla(ortak.saniye ? ortak.saniye() : 0), sahne: sahneAdi(), ...veri };
    if (urun && o.urun === undefined) o.urun = urun;
    kuyruk.push(o);
    if (acil) return bosalt();
    if (!bosta) bosta = typeof requestIdleCallback === 'function' ? requestIdleCallback(bosalt, { timeout: 800 }) : setTimeout(bosalt, 200);
  }

  // --- Bağlam ----------------------------------------------------------------
  function hesapla(neden) {
    let en = null;
    let enSkor = ESIK_SKOR - 0.001;
    for (const [kod] of DURAKLAR) {
      const s = skor[kod];
      if (s > enSkor || (s === enSkor && en && sira.lastIndexOf(kod) > sira.lastIndexOf(en))) {
        en = kod;
        enSkor = s;
      }
    }
    if (susturuldu) en = null;
    if (en !== urun) {
      urun = en;
      if (urun) iz('ege_baglam', { urun, kaynak: neden });
      degisti();
    }
  }

  function artir(kod, puan, neden) {
    if (!(kod in skor)) return;
    skor[kod] += puan;
    const i = sira.indexOf(kod);
    if (i >= 0) sira.splice(i, 1);
    sira.push(kod);
    if (puan >= 8) susturuldu = false; // yeni bir kullanıcı eylemi bağlamı geri getirir
    hesapla(neden);
  }

  function durakta(t) {
    for (const [kod, a, b] of DURAKLAR) if (t >= a && t < b) return kod;
    return null;
  }

  /** Her karede: görünür süre (durak başına tavanlı), eşik ve pencere olayları. */
  function zaman(t, ms, durum) {
    if (sonMs) {
      // iki örnek arası (boşta kalma dahil) önceki konumdaki durağa yazılır
      const kod = durakta(sonSn);
      if (kod && ms > sonMs) {
        const dt = Math.min((ms - sonMs) / 1000, 5);
        const eski = skor[kod];
        const tavan = DURAK_TAVAN_SN;
        // süre puanı yalnız ilk DURAK_TAVAN_SN saniye için sayılır (8/15 puanlık eylemler tavana dahil değil)
        if (eski < tavan) {
          skor[kod] = Math.min(tavan, eski + dt);
          if (!sira.includes(kod)) sira.push(kod);
          if (urun === null || kod !== urun) hesapla('sure');
        }
      }
    }
    sonSn = t;
    sonMs = ms;
    hizOrnek.push([ms, t]);
    while (hizOrnek.length > 2 && ms - hizOrnek[0][0] > 3000) hizOrnek.shift();
    if (t > enYuksek) {
      // ilerleme eşikleri: ilk ulaşılışta, ileri yönde
      for (const e of ILERLEME) {
        if (enYuksek < e && t >= e) iz('ege_ilerleme', { t: e, hiz: hiz() });
      }
      for (const [e, s] of SAHNE_GIRIS) {
        if (enYuksek < e && t >= e) iz('ege_sahne', { sahne: s, yon: 'ileri' });
      }
      enYuksek = t;
    }
    for (const [id, a, b] of CTA_PENCERE) {
      if (!goruldu.has(id) && t >= a && t < b) {
        goruldu.add(id);
        iz('ege_cta_gor', { cta: id });
        if (id === 'son_teklif') iz('ege_son_gor', { atladi: enYuksek < 138 ? 1 : 0 });
      }
    }
  }

  // --- Bağlantı şeması ---------------------------------------------------------
  const utm = () => {
    try {
      return [...new URLSearchParams(location.search)].filter(([k, v]) => /^utm_[a-z_]+$/.test(k) && /^[\w.\- %+]{1,80}$/.test(v));
    } catch {
      return [];
    }
  };

  /** Teklif/föy/ürün bağlantısı: yalnız küçük harf ASCII parametreler; kişisel veri yok. */
  function baglantiYap(yol, { nokta, kitle, urun: u, kaynak = KAYNAK } = {}) {
    const q = [`kaynak=${kaynak}`, `dil=${dil()}`];
    if (u) q.push(`urun=${u}`);
    if (kitle) q.push(`kitle=${kitle}`);
    if (nokta) q.push(`nokta=${nokta}`);
    for (const [k, v] of utm()) q.push(`${k}=${encodeURIComponent(v)}`);
    return `${yol}?${q.join('&')}`;
  }

  let imza = '';
  /** [data-link] öğelerinin href'ini bağlama göre yeniden yazar (sağ tık/bağlantıyı kopyala da doğru çalışsın). */
  function linkleriGuncelle(ustKaynak) {
    const yeni = `${dil()}|${urun || ''}|${ustKaynak}`;
    if (yeni === imza) return;
    imza = yeni;
    for (const a of document.querySelectorAll('[data-link]')) {
      const yol = a.dataset.link;
      if (!yol || yol.charAt(0) !== '/') continue;
      const kaynak = a.hasAttribute('data-ust-teklif') ? ustKaynak : KAYNAK;
      const u = a.dataset.urun || (a.hasAttribute('data-urun-baglam') ? urun : null) || undefined;
      a.setAttribute('href', baglantiYap(yol, { nokta: a.dataset.nokta, kitle: a.dataset.kitle, urun: u, kaynak }));
    }
  }

  // --- İlk eylem ve çıkış --------------------------------------------------------
  const t0 = performance.now();
  function ilkEylem(eylem) {
    if (basladi) return;
    basladi = true;
    iz('ege_hikaye_basla', { bekleme_ms: Math.round((performance.now() - t0) / 250) * 250, eylem });
  }
  window.addEventListener('scroll', () => ilkEylem('kaydir'), { passive: true, once: true });
  window.addEventListener('pointerdown', () => ilkEylem('dokun'), { passive: true, once: true });
  window.addEventListener('keydown', () => ilkEylem('klavye'), { once: true });
  const cikis = () => iz('ege_cikis', { t_maks: yuvarla(enYuksek), sure_sn: Math.round((performance.now() - t0) / 5000) * 5, cta_gordu: goruldu.has('son_teklif') ? 1 : 0 }, true);
  document.addEventListener('visibilitychange', () => document.hidden && cikis());
  window.addEventListener('pagehide', cikis);

  return {
    iz,
    zaman,
    baglantiYap,
    linkleriGuncelle,
    urun: () => urun,
    /** Ad (TR/EN) — bağlam çipi ve teklif düğmesi için. */
    ad(kod = urun) {
      const u = URUN[kod];
      return u ? u[dil()] : '';
    },
    /** Ürün kartı/noktası açıldı (+8). */
    kartAcildi: (kod) => artir(kod, 8, 'nokta'),
    /** Ürün çipi ya da ürün bağlantısı tıklandı (+15). */
    cipTik: (kod) => artir(kod, 15, 'tik'),
    /** Kullanıcı bağlam çipini sildi (×). */
    sil() {
      for (const k of Object.keys(skor)) skor[k] = 0;
      sira.length = 0;
      susturuldu = true;
      hesapla('sil');
    },
    onDegis(fn) {
      degisti = fn;
    },
    /** Oturumda en yüksek ulaşılan film saniyesi (hikâye atlandı mı?). */
    enYuksek: () => enYuksek,
    basla: ilkEylem,
    /** EN karşılığı (ör. 'Get a quote for …' kalıbı). */
    metin: (k) => EN[k],
  };
}
