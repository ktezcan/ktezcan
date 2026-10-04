# MOTION — Ege Gazbeton giriş hikâyesi hareket sözleşmesi

Tüm sahne, efekt ve sayfa işleri bu dosyaya uyar. Fikir: tek bir sözleşme dosyası renk, zamanlama ve hareket kalitesini sabitler
(esinlenilen yaklaşım: charlie947/motion-graphics-skills, MIT; burada Ege Gazbeton'a uyarlandı, kuralları kendimize aittir).

## 1. Renk (anlamlarıyla)
- Lime `#b8d84a` (parlak `LIME_HI`): YALNIZ bizim ürün (blok, derz, lento, streç, fabrika şeridi, ürün vurgusu) ve onaylı marka vurgusu (Türkiye poligonu, yaylar, fabrika iğneleri).
- Bej kâğıt `#ebe3d5` + grafit çizgi `#292623`: Perde 1 çizim dili. Sıcak ışık `#ffd696`: pencere, kıvılcım, ev. Soğuk beyaz `#e9f2ff`: tel kafes, halka silme.
- Stüdyo beyaz/sıcak gri gradyan: ürün turu. Koyu fabrika zemini: doğuş. Gece laciverti: dünya ve finale.

## 2. Yazı
Barlow (gövde) ve Barlow Condensed (başlık); yalnız HTML/SVG. Render içinde yazı ve rakam YOK.

## 3. Zamanlama (giriş · tutuş · çıkış)
- Giriş 0,6–0,9 sn (yumuşak ease-in-out); tutuş = okuma süresi (≤ 3 kelime/sn, en az 1,2 sn); çıkış 0,4 sn.
- Dizilerde her öğe bir öncekinden 40–80 ms geç başlar (kademe): harfler, rakamlar, kartlar, parçacıklar.
- Her perdenin ilk 3 sn'si kanca taşır; boş açılış yok. Her perdenin son 3 sn'si bir sonraki perdeye eşleşen kareyle geçer.
- Her çekimin ORTA karesi kontrol edilir: metin taşması, örtüşme, yanlış bilgi, lime yanlış nesnede.

## 4. Hareket kalitesi
- Sayfa kaydırmaya bağlıdır: tüm 2B efektler ilerleme p'nin SAF fonksiyonudur (aynı p → aynı kare); rastgelelik sabit tohumla (seed). Geri sarma kusursuz.
- Yakınsama (kıvılcımların logoya, parçacıkların sayıya toplanması): uzun, kademeli ease — "yerçekimi gibi, çarpıp durma gibi değil". Başlangıç ve bitiş durumu piksel eşleşir.
- Parçacık oranı: ~%85 ana şekle, ~%15 atmosfere (sönük sürüklenenler). Şekil, hedef geometriden (logo/küre) örneklenir.
- Kalem/çizim: "ikili tutuş" hissi (el yapımı); çizgi başta ince, ortada basınçlı; sıralı tek kalem, aynı anda çoklu dikme yok.
- Fiziksel oturma (blok yerine iner) hafif sekmeye izin verir; başka yerde sekme (bounce), daktilo yazısı ve metinde gradyan YOK.
- Kamera: göz hizası C kadrajı perde 1 boyunca ana dildir; yörüngelerde ease-in-out, hızlı yörüngede kare yoğunluğu artar (hayalet önlemi).

## 5. Doku ve bitiş
Kâğıt dişi + vinyet (perde 1); bloom ≤ 0,4 ve yumuşak halo (bilinçli, ürün/kıvılcım/yay vurgusu); film greni yok. Kanvas üstünde backdrop-filter ve mix-blend yok.

## 6. Asla yapma (beş madde)
1. Kaynaksız rakam, ülke adı, "yanmaz". 2. Lime'ı ürün/marka vurgusu dışına boyama. 3. Render içine yazı koyma. 4. Kaydırmayı kilitleme / tarayıcı depolaması kullanma. 5. Yakın planda insan yüzü.

## 7. Referans çekim (doğru uygulama)
t=0–3 sn: bej kâğıtta tek sıcak ışık noktası nabız atar (makro 2,2×) → kıvılcım ışınlarla patlar, kamera geri çekilir → kıvılcım kalem ucuna dönüşür, ilk aks çizgisi kapı hizasından geçer. Metin yerinde kalır, düğmeler soluklaşır; ışık noktası sonda pencere ışığı olarak geri döner (görsel kafiye).
