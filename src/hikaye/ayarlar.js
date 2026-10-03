/**
 * Giriş hikâyesi — ayarlar.
 * Sahne sırası, kare klasörleri ve zamanlama burada; metinler dil.js'te.
 */
export const KARE_KOK = 'kareler'; // index.html'e göre göreli yol

/**
 * Sahneler (sayfadaki sırayla). id = kareler/<id>/ klasörü ve [data-sahne] değeri.
 *  giris  : sahnenin ilk bölümü (0..1) — yalnız video→blok sahnesinde: video önce
 *           bant hâline gelir, sonra kareler başlar.
 *  video  : ön yüz köşeleri meta.face'ten okunur, gerçek video bu yüze oturur.
 */
export const SAHNELER = [
  { id: 's0', giris: 0.16, video: true },
  { id: 's1' },
  { id: 's2' },
  { id: 's3' },
  { id: 's4' },
];

/** Dikey ekran eşiği (genişlik/yükseklik): altındaysa telefon kareleri (m) kullanılır. */
export const DIKEY_ESIK = 0.82;

/** Kaydırma yumuşatması (saniyede yaklaşma katsayısı). Büyüdükçe daha çabuk oturur. */
export const YUMUSAKLIK = 9;

/** Fare ile sahne eğimi (piksel, en fazla). 0 = kapalı. */
export const EGIM_PX = 14;

/** Aynı anda en fazla kaç kare indirilir. */
export const ES_ZAMANLI = 6;

/** Sahne bitişinde içerik zeminine erime (köprü) başlangıcı (0..1). */
export const KOPRU_BASLA = 0.88;
