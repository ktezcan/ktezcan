/**
 * Giriş hikâyesi — ayarlar.
 * Sahne sırası, kare klasörleri ve zamanlama burada; metinler dil.js'te.
 */
export const KARE_KOK = 'kareler'; // index.html'e göre göreli yol

/** Film saniyesi başına kaydırma (ekran yüksekliği yüzdesi). Plan saniyeleri bununla kaydırmaya eşlenir. */
export const SANIYE_VH = 22;

/**
 * Akıştaki parçalar (sayfadaki sırayla). id = kareler/<id>/ klasörü ve [data-sahne] değeri.
 * boy = parçanın kaydırma uzunluğu (vh) = (bitiş sn − başlangıç sn) × SANIYE_VH; sn = filmdeki başlangıç saniyesi.
 * Toplam 146 sn = 3212 vh. Parçalar uç uca biner: dikişte kare seti anında değişir (aşağıya bakın).
 */
export const SAHNELER = [
  { id: 's0', boy: 704, sn: 0 }, //   Hayalden yuvaya: kıvılcım → plan → eskiz → tel kafes → gazbeton → sokak → akşam (0–32 sn)
  { id: 's1', boy: 836, sn: 32 }, //  Ürün turu: ev etrafında, duraklarda ürün + özellik (32–70 sn)
  { id: 's2', boy: 440, sn: 70 }, //  Doğuş: blok hammaddeye çözülür, kabarma, kesim (70–90 sn)
  { id: 's3', boy: 308, sn: 90 }, //  Gözenek: kapalı hava hücresi (90–104 sn)
  { id: 's4', boy: 352, sn: 104 }, // Yol: fabrikadan tır çıkar, kamera tepeye yükselir (104–120 sn)
  { id: 's5', boy: 352, sn: 120, kopru: false }, // Dünya: 5 kıtaya yaylar (120–136 sn); köprü finale ait
  // Finale kendi karesi olmayan parçadır: ana kanvasta s5'in SON karesi durur, final.js (finalKur) 2B efektini üstüne çizer.
  { id: 'finale', boy: 220, sn: 136, tur: 'finale', konak: 's5' }, // Güven → logo → slogan → teklif (136–146 sn)
];

/**
 * Parçalar arası çapraz geçiş (vh). Artık YOK: dikişlerde önceki parçanın son karesi sonrakinin ilk karesiyle
 * aynıdır (paketlemede tools/dikis_kopyala.py kopyalar), bu yüzden sınırda kare seti anında ve kayıpsız değişir.
 * Başka modüllerin içe aktarması bozulmasın diye sabit duruyor; 0'dan başka değer desteklenmez.
 */
export const GECIS = 0;

/** Dikey ekran eşiği (genişlik/yükseklik): altındaysa telefon kareleri (m) kullanılır. */
export const DIKEY_ESIK = 0.82;

/** Kaydırma yumuşatması (saniyede yaklaşma katsayısı). Büyüdükçe daha çabuk oturur. Tek, akış genelinde. */
export const YUMUSAKLIK = 9;

/** Hedef ile gösterilen konum arası bu kadar vh'den fazlaysa (menüden atlama, kaydırma çubuğu) yumuşatmadan atlanır. */
export const ATLAMA_VH = 300;

/** Fare ile sahne eğimi (piksel, en fazla). 0 = kapalı. */
export const EGIM_PX = 14;

/**
 * Aynı anda en fazla kaç kare indirilir/çözülür. Kaydırma sürerken az tutulur: çözme işçileri tarayıcının
 * çizim/birleştirme işini aç bırakıp kare hızını düşürür (ölçüm: 6 eşzamanlı → ≈35 fps, 2 → ≈57 fps).
 * Boştayken (kaydırma durmuş) hızlı dolsun diye ES_ZAMANLI kullanılır.
 */
export const ES_ZAMANLI = 4;
export const ES_HAREKETLI = 2;

/** Kanvas çözünürlük çarpanı üst sınırı (tüm kanvaslar). */
export const DPR_ENFAZLA = 1.25;

/** Sahne bitişinde içerik zeminine erime (köprü) başlangıcı (0..1). */
export const KOPRU_BASLA = 0.88;

/**
 * Kare belleği (pencereli yükleme). Çözülmüş kare (ImageBitmap) ~5,8 MB: bütün sahneyi tutmak GB'lara çıkar.
 *  • Etkin sahnede odak karenin ±PENCERE karesi çözülü tutulur; pencere dışı bitmap.close() ile bırakılır.
 *  • Her sahnede anahtar kareler (her ANAHTAR_ADIM'inci + son kare) kalır: hızlı sarmada en az bunlar vardır.
 *  • Komşu sahnelerde yalnız anahtar kareler ve dikişe yakın KOMSU_KARE kare (sonrakinin ilk, öncekinin son kareleri).
 *  • Komşunun yüklemesi etkin sahnenin ilerlemesi ONYUKLE_P'yi geçince (sonraki) / ONYUKLE_GERI'nin altına inince (önceki) başlar:
 *    sayfa açılışında bant genişliği yalnız s0'a gider.
 */
export const PENCERE = 16;
export const ANAHTAR_ADIM = 8;
export const KOMSU_KARE = 12;
export const ONYUKLE_P = 0.6;
export const ONYUKLE_GERI = 0.4;
/** Finale sırasında s5 yalnız son karesini gösterir: odak çevresinde tutulacak kare yarıçapı. */
export const PENCERE_FINALE = 2;
/**
 * Kaydırma bu hızı (vh/sn) aşınca pencere kareleri indirilmez, yalnız odak kare ve anahtar kareler (hızlı sarmada
 * pencere zaten yetişmez; çözme işçileri çizimi aç bırakır). Hız düşünce pencere dolar.
 */
export const YUKLEME_DURAKLAT_VH = 110;
/** Hızlı kaydırmada (kare/çizim) bu eşiğin üstünde ara kare erimesi kısalır ve hareket yönüne kayar (hayalet azaltma). */
export const HIZLI_ESIK = 0.35;
/** Yüklü karelerin bu aralıktan (kare) geniş boşluklu seti baştan sona kapsamış sayılmaz (bkz. Sahne.setVariant). */
export const MAKS_BOSLUK = 16;
