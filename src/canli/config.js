/**
 * Ege Gazbeton — Hero sahnesi yapılandırması
 * ------------------------------------------------------------
 * Sahnenin tüm ayarlanabilir değerleri bu dosyadadır.
 * Kodun geri kalanına dokunmadan görünümü ve fiziği ayarlayabilirsiniz.
 * Renkler CSS'ten okunur (assets/css/hero.css → :root --eg-*).
 */

/** Gömülü Three.js sürümü (derle.mjs ile canli.js'e paketlenir; dış CDN yok). */
export const THREE_VERSION = '0.186.1';

/**
 * Kalite kademeleri. Cihaz yeteneğine göre başlangıç kademesi seçilir;
 * çalışma sırasında kare süresi izlenir ve gerekirse kalite kademeli düşürülür.
 *  particles : gözenek + taneli doku parçacık bütçesi
 *  motes     : havada süzülen "gaz kabarcığı" parçacıkları
 *  dprMax    : en yüksek piksel oranı (retina keskinliği ↔ GPU yükü)
 *  cell      : dalga simülasyonu hücre boyu (dünya birimi; küçük = daha detaylı)
 *  attempts  : gözenek yerleştirme deneme sayısı (açılış süresini etkiler)
 *  octaves   : rölanti dalgası gürültü katmanı (1 = daha hafif)
 */
export const TIERS = {
  low: { particles: 9000, motes: 90, dprMax: 1, cell: 0.32, attempts: 9000, octaves: 1 },
  mid: { particles: 17000, motes: 160, dprMax: 1.5, cell: 0.26, attempts: 15000, octaves: 2 },
  high: { particles: 30000, motes: 240, dprMax: 2, cell: 0.21, attempts: 24000, octaves: 2 },
};

/** Fizik: imlecin "ağırlığı" ve yüzeyin akışkanlığı. */
export const PHYSICS = {
  waveSpeed: 4.4, // dalga yayılma hızı (birim/sn)
  damping: 0.62, // genel sönüm (1/sn) — büyüdükçe dalgalar daha çabuk söner
  viscosity: 0.035, // yüksek frekanslı kırışıklığı yumuşatır
  sponge: 7, // kenarlarda dalgayı yutan bant (hücre) — yansıma olmaz
  followStiffness: 34, // imleç takipçisinin yay sertliği (düşük = daha ağır)
  followDamping: 0.74, // sönüm oranı (1 = kritik; <1 hafif organik salınım)
  wakeGain: 1.35, // hareket izinin (iz dalgası) gücü
  wakeRadius: 0.8, // iz çekirdeği yarıçapı (dünya birimi)
  maxSpeed: 12, // dalgaya aktarılan en yüksek hız
  pulseGain: 2.6, // arayüz etkileşimi (buton, sekme) dalga gücü
  pulseRadius: 1.25,
  sleepEpsilon: 1.5e-4, // bu eşiğin altında simülasyon uyur (CPU = 0)
};

/** Görünüm ve kompozisyon. */
export const LOOK = {
  fov: 40,
  fovPortrait: 52,
  camera: [0, 6.2, 7.4],
  cameraPortrait: [0, 7.6, 8.6],
  target: [0, 0, -1.9],
  parallax: [0.65, 0.32], // fare ile kamera kayması (x, y)
  heightScale: 0.6, // etkileşim dalgalarının yükseklik çarpanı
  idleAmplitude: 0.24, // fare durunca süren doğal dalgalanma genliği
  pointSize: 2.15,
  fog: [11, 27], // sis başlangıç/bitiş mesafesi
  introDuration: 3.4, // açılış hikâyesi (gazlanma → kür → yerleşme) süresi, sn
  seed: 1907, // gözenek dizilimi tohum değeri (her açılışta aynı kompozisyon)
};
