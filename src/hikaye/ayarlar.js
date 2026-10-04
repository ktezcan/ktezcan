/**
 * Giriş hikâyesi — ayarlar.
 * Sahne sırası, kare klasörleri ve zamanlama burada; metinler dil.js'te.
 */
export const KARE_KOK = 'kareler'; // index.html'e göre göreli yol

/**
 * Sahneler (sayfadaki sırayla). id = kareler/<id>/ klasörü ve [data-sahne] değeri.
 */
export const SAHNELER = [
  { id: 's0', boy: 560 }, // Hayalden yuvaya: kıvılcım → plan → eskiz → tel kafes → gazbeton → sokak → akşam
  { id: 's1', boy: 440 }, // Ürün turu: ev etrafında, duraklarda ürün + özellik
  { id: 's2', boy: 360 }, // Doğuş: blok hammaddeye çözülür, kabarma, kesim
  { id: 's3', boy: 280 }, // Gözenek: kapalı hava hücresi
  { id: 's4', boy: 260 }, // Yol: fabrikadan tır çıkar, kamera tepeye yükselir
  { id: 's5', boy: 280 }, // Dünya: 5 kıtaya yaylar
];

/**
 * Tek akış: sahne uzunlukları (boy, ekran yüksekliği yüzdesi cinsinden kaydırma) ve iki sahne
 * arasındaki çapraz geçiş (GECIS). Önceki sahnenin son karesi, sonrakinin ilk karesine erir;
 * kareler bu geçiş için eşleşecek biçimde hesaplandı (küp → blok, tepeden şantiye → İzmir).
 */
export const GECIS = 70;

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
