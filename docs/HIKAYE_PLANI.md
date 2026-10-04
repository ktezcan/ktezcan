# Ege Gazbeton giriş hikâyesi — saniye saniye plan

Bu belge `docs/plan/*.json` dosyalarından `tools/plan_md.py` ile üretilir (JSON kaynaktır; belgeyi elle değiştirmeyin).

**Okuma kılavuzu.** Hikâye 146 film saniyesidir (2:26). 1 saniye = 22 vh kaydırma (referans hız); toplam 3212 vh. Her saniye bir blok: görsel, efekt, ekran metni (TR/EN), rakam ve kaynağı, etkileşim, pazarlama rolü, üretim ve maliyet. Her perdenin son 3 saniyesi bir sonraki perdeye geçiştir; sonraki perde o görüntüyle birebir başlar.

## 1. Genel yapı

| Perde | Süre | Saniye | vh | Amaç |
|---|---|---|---|---|
| **s0 · Hayalden yuvaya (ana giriş)** | 32 sn | 0–32 (0:00–0:32) | 0–704 | Duygu: tek bir ışık noktası çizgiye, çizgi evin hacmine, hacim gazbeton duvara, duvar akşamın sıcak penceresine dönüşür. Mesaj: ev önce hayaldir; gerçek olunca onu yuva yapan şey malzemesidir. Sonda soru: bu evi iyi yapan ne? |
| **s1 · Ürün turu: bu evi iyi yapan ne?** | 38 sn | 32–70 (0:32–1:10) | 704–1540 | Merak, keşif, güven. Soru ile açılır; izleyici evin etrafında dolaşıp altı ürünü gerçek yerinde görür, her durakta NEREDE kullanıldığını ve NE KAZANDIRDIĞINI tek bir görsel mekanizmayla öğrenir (ısı oku, açıklık ölçüsü, beton dolumu, derz çizgisi, kütle … |
| **s2 · Doğuş: hammaddeden bloğa** | 20 sn | 70–90 (1:10–1:30) | 1540–1980 | Merak, şaşkınlık, kavrayış, güven. Sağlam blok önce beş sade hammaddeye çözülür; her birinin görevi tek sözcük ve dokunulur kartla öğrenilir. Karışım, kalıp, kabarma (hidrojen), tel kesim ve otoklav gerçek makine diliyle görünür olur. Çıkışta 'hacmin çoğu … |
| **s3 · Gözenek: ısıyı tutan hava** | 14 sn | 90–104 (1:30–1:44) | 1980–2288 | Merak, şaşkınlık, güven. Bildiğimiz gri bloğun içine girilir; kapalı hava hücreleri görünür; ısının gözenek ağında dolanıp yavaşladığı bilim gibi izlenir. Üç kaynaklı rakam (λ 0,08 · A1 · 300–600) mühür gibi dizilir. Çıkışta gözenekten geri çekilip blok, … |
| **s4 · Yol: fabrikadan sahaya** | 16 sn | 104–120 (1:44–2:00) | 2288–2640 | Gurur, ölçek, güven. Blok artık ürün: sabah ışığında lime streçli paletler, forklift, kayış, kantar; s0'da evin önünden geçen tırın doğduğu yer. Üç onaylı rakam (2 fabrika, kendi kireç tesisi 200 t/gün, 1.100.000 m³) görsel kanıtla gelir. Çıkışta tır yola … |
| **s5 · Dünya: Ege'den 5 kıtaya** | 16 sn | 120–136 (2:00–2:16) | 2640–2992 | Duygu: yerellikten güvene. İki fabrikanın ışığı dünyaya yayılır. Mesaj: Ege'de üretilen, 5 kıtada kullanılan ürün; 25+ ülke · 5 kıta (ihracat bölümü). Karanlık küre kıta kıta yanar; sonuç sakin, parlak, güven veren bir ışık ağı. Öğretici: fabrikaların yeri, … |
| **son · Finale: teklif, logo, slogan** | 10 sn | 136–146 (2:16–2:26) | 2992–3212 | Duygu: sakin şaşkınlıktan güvene, güvenden harekete. Dünyanın ışıkları Ege'de tek kıvılcıma toplanır; kıvılcım logonun köşe çizgilerini çizer ve s0'daki 'Peki bu evi iyi yapan ne?' sorusuna tek sözcükle yanıt verir: 'Güven.' Canlı gözenek yüzeyi ürünü … |

Tempo eğrisi: duygu %22 (0–32 sn) → kanıt %49 (32–104) → güç %22 (104–136) → eylem %7 (136–146).

## 2. Senin kararına bırakılanlar

- **s0** — [KAPANDI · plan kararı] Açılış H1: ‘Her yuva bir çizgiyle başlar.’ (eyebrow ‘EGE GAZBETON · Söke & İzmir’ + tek cümle); ‘Bugünden Yarına Güvenle’ açılışta görünmez, yalnız son t=140 ve <title>/OG'de (pazarlama önerisi benimsendi; hero H1 ile eski t=2 vuruşu tek öğe, t=0/t=1/t=2 satırları buna göre güncellendi).
- **s0** — Tır kabinine logo çıkartması: ‘logo yalnız son bölümde’ kuralı gereği logosuz (lime şerit + HTML ‘Ege Gazbeton’ etiketi) mi kalsın, yoksa bu perdede kabinde gerçek logo mu görünsün?
- **s0** — Anne-çocuk eve girer ve ilk pencere yanar kurgusu (kapı animasyonu + ‘ışığı sen yak’ etkileşimi, ≈2 gün ek iş) onaylanır mı, yoksa pencereler yalnız zamanla mı yansın?
- **s1** — Ürün çeşitleri (düz/geçmeli blok, çatı/döşeme/duvar paneli), duvar bloğu kalınlığı (5–35 cm) ve EGEPOR'da 'ısı köprüsü' ifadesi üreticiden teyit edildi mi? Edilmediyse çeşit spotları ve bu etiketler çıkarılsın mı?
- **s1** — ODTÜ çalışmasındaki −%17 yapı kütlesi yalnız panele mi, tüm gazbeton sisteme mi ait? Etiket metni buna göre yazılacak.
- **s1** — Ürün turu 96 yerine 152 kare (4 kare/sn) + 8 karelik makro derz + 4 karelik önce/sonra ek render ile üretilsin mi? SÜRE ÖLÇÜLDÜ (render/s1.log, 35 kare, d, 4 çekirdek): medyan ≈109 sn, ort ≈140 sn (aykırı hariç), max 1318 sn; eski '~40 sn' geçersiz. 160 render: d ≈6,2 sa (96 kare ≈3,7 sa, fark ≈+2,5 sa); m seti ≈+0,9 sa; toplam fark ≈+3,4 sa; d+m ≈8,5 sa. Düzeltme paketi + ön test tutarsa (hedef ort ≤90 sn): d ≈4,0 sa, d+m ≈5,5 sa (varsayım). Karar: (A) 152 kare, ön testten sonra; (B) pass_order ile 2. geçişte durup (76 kare, ≈yarı süre) oynatıcının ara kareyi erimeyle doldurması (telefondaki gibi), dalış f140–151 ve geçiş kareleri tam; (C) 96 kare (≈3,7 sa; 2,5 kare/sn, satırlar yeniden yazılır). Çalışan 96 kareli seri (yön −32°) yeni plana uymaz: durdurulup yeni klasörde yeniden başlatılması da onaylanmalı.
- **s2** — Otoklav sıcaklık/basınç/süresi, kabarma ve ön sertleşme süresi ile gazbetonun hava hacim oranı için Ege Gazbeton'un resmi rakamları var mı? Şimdilik ekranda yok; verilirse kaynaklı karta eklenir.
- **s2** — Söke hattının gerçek kalıp, tel kesme makinesi ve otoklav fotoğrafları (yalnız yerel referans) verilebilir mi? Yoksa genel, temsilî makine tasarımı mı kullanılsın?
- **s2** — Kabarma anında 'eğitim kesiti' (kalıbın ön cidarı şeffaf, hücreler görünür) temsilî olarak kabul mü, yoksa yalnız opak kalıp ve üstten görünüm mü?
- **s3** — Suda yüzme sahnesi planlanmadı (t=99-100 şimdi tezgâhta G1/G2/G4 blok + 300–600 kg/m³ + λ · A1 · 300–600 şeridi). Geri istenirse: ürün föyleri ve CE belgelerinde ‘suda yüzer’ ifadesi yok (yalnız 300–600 kg/m³); yazılı kaynak ya da ölçüm var mı? Onay gelse bile cümle ‘yüzer’ yerine kaynaklı yazılır (ör. ‘Yoğunluk 300–600 kg/m³’).
- **s3** — A1 sahnesinden alev ve ‘serin yüz’ görseli çıkarıldı (yangın direncini, EN 13501-2, ima ediyordu); sahne yalnız ‘A1 · yangına tepki sınıfı · EN 13501-1 · CE belgeleri’ kartı + sınıf merdiveni + nötr tezgâh. Yangın direnci belgeniz var mı? Gelirse alev ya da serin yüz ayrı karar olarak, belgeye bağlı ve süre/°C yazmadan yeniden planlanır. Sınıf merdiveni harfleri (A1…F) EN 13501-1'den gösterilebilir mi?
- **s3** — Gözenek boyutu (mm), ölçek çubuğu ve hücre sayısı için ürün föyü ya da laboratuvar kaynağı var mı? Şimdilik ekranda hiçbir ölçek rakamı yok; kaynak gelirse makro sahneye eklenir.
- **s4** — Söke tesisinin gerçek dış görünümü (cephe rengi, otoklav/silo sayısı, kireç tesisinin yeri) için yerel referans fotoğraf/plan verilebilir mi, yoksa bu plandaki temsilî genel fabrika mı kalsın?
- **s4** — 1.100.000 m³ kapasiteye 'yıllık' ibaresi eklensin mi (kaynakta süre yok)? İzmir fabrikası hangi ilçede (çıkıştaki harita noktası için)?
- **s4** — Tır çıkışındaki hayalet riskine karşı perde 6 yerine 8 kare/sn (96 → 128 kare, render ≈ +%33, d ≈ +0,7 sa) üretilsin mi?
- **s5** — Aliağa ve Alsancak limanları: ihracat gerçekten bu limanlardan mı? dil.js'te kaynaksız; web'de yalnız Söke OSB ve İzmir/Bornova fabrikası görünüyor. Onay yoksa cümleden ve etiketlerden çıkarılır, kart 'İki fabrika: Söke ve İzmir' kalır.
- **s5** — Kıta adları (Avrupa, Afrika, Amerika, Asya, Okyanusya) küre üstünde etiket olarak gösterilebilir mi? Ülke adı değil; onay yoksa yalnız 5 halkalı sayaç kalır.
- **s5** — 25+ ülke · 5 kıta için ihracat bölümünden güncel yazılı teyit ve tarih var mı? Dış haberlerde 19 ülke / 4 kıta yazıyor (eski olabilir); çelişki görünürlük riski taşır.
- **son** — Üst çubuktaki küçük logo hikâye boyunca gizli mi kalsın ('logo yalnız sonda' katı yorum; logo t=141'de kilitten üst çubuğa iner), yoksa gezinme güveni için baştan görünür mü kalsın?
- **son** — Güven işaretleri ve teklif vaadi: CE belgeleri dışında hangileri doğrulandı (ISO 9001, TSE, EPD, kuruluş yılı) ve teklife 'X saatte dönüş' gibi bir söz verilsin mi? Doğrulanmayan hiçbiri eklenmeyecek.
- **son** — /teklif/ formu ?urun=...&kaynak=hikaye&kitle=... parametrelerini okuyup ön doldurabilir mi (site tarafı iş)? Ürün kodları (duvar, lento, ublok, tutkal, panel, egepor) uygun mu; Katalog düğmesi doğrudan PDF mi, /katalog/ sayfası mı?
- **modüller** — Panel kipi (KARAR, onayınıza sunulur): panel yalnız kullanıcı başlatımlıdır ve KİLİTSİZdir; kaydırma/tuş olayı yutulmaz, kaydırma, Esc, Kapat, geri tuşu ve dış dokunma paneli kapatır; film kaydırma konumuna bağlı olduğundan panel açıkken zaten durur; telefonda tam ekran modal yerine alt sheet (en çok 70svh). pazarlama.cta_kurallari'na 'kullanıcı başlatımlı panel istisnası' yazıldı, otomatik pencereler kilitsiz kalır. Onaylar mısınız (özellikle telefonda sheet yüksekliği ve 'kaydırınca kapanır' davranışı)?
- **modüller** — duvar_hesap ile /duvar-tasarla/ (KARAR, onayınıza sunulur): birleştirilmez ve çakışmaz; mini hesap sitedeki aracın film içi 'ön metraj' ön kapısıdır. t=38–40'taki tek 'Duvarlarınızı hesaplayın →' öğesi hem /duvar-tasarla/'ya giden gerçek bağlantı hem paneli açan düğmedir (JS'siz/yeni sekme → site aracı); panelde sonucun altında 'Ayrıntılı tasarım →' ölçüleri taşır; SON'da gömülü form yok. Teyit gerekli: /duvar-tasarla/ ne hesaplıyor (formül alan ÷ 0,15 m² ile aynı mı; farklıysa panel kapatılıp yalnız bağlantı kalır), ölçü parametrelerini (?uzunluk=&yukseklik=&acik=&kalinlik=) okuyup ön doldurabilir mi ve /teklif/ formu ?urun=&alan=&kalinlik=&kaynak=hikaye parametrelerini okuyabilir mi (site işi)?
- **modüller** — Duvar bloğu 5–35 cm kalınlığı üreticiden teyitli mi; stok kalınlıkları (kaydırıcı adımı) ve G3 sınıfının yoğunluğu nedir? Teyit gelene dek kaydırıcı sürekli, G3 işaretsiz.
- **modüller** — Duvar hesabında fire/kırık payı için yönlendirme yapılsın mı (varsayılan 0, kullanıcı girer)? Tutkal tüketimi (kg/m²), palet başına blok adedi/m³ ve tır kapasitesi verilirse 'bu ev kaç palet / kaç tır?' maket sayacına eklenir.
- **modüller** — Isı modülünde tasarım değeri λ 0,08 (G2/350) ile kuru değerler (U blok 0,16; EGEPOR 0,051–0,062) aynı panelde ayrı etiketlerle gösterilebilir mi? U hesabına yüzey dirençleri (Rsi/Rse) eklensin mi ve TS 825 sınır değeriyle kıyas yapılsın mı (müşteri kararı; şimdilik yok)?
- **modüller** — ODTÜ −%17 yapı kütlesi yalnız panele mi tüm gazbeton sisteme mi ait? README'deki eski '−%14 taban kesme' DEVIR/dil.js'te yok: doğrulanmış mı, kullanılabilir mi?
- **modüller** — 'Suda yüzer' ve 'öbür yüz serin' (EN 13501-2 yangın direnci) için belge var mı? A1 modülünde sınıf merdiveni harfleri (A1…F) standarttan gösterilebilir mi? Üretici sayfasında 'A1 Hiç Yanmaz' yazıyor; bizde yasak kalmaya devam ediyor mu?
- **modüller** — Kıta adları (Avrupa, Afrika, Amerika, Asya, Okyanusya) ekranda gösterilebilir mi? 25+ ülke · 5 kıta için ihracat bölümünden güncel yazılı teyit ve tarih var mı (dış haberlerde 19 ülke / 4 kıta çelişkisi)?
- **modüller** — EGEPOR için 'ısı köprüsü' ifadesi ve ODTÜ/ürün föylerindeki 'kolon ve kiriş kaplaması' dışındaki kullanım iddiaları üreticiden teyitli mi? U bloktaki '50 kgf/cm²' hangi değerin etiketi?
- **modüller** — Maket sayacı bina_detay.py çıktısına bağlı: iç bölme duvarı (y=0 aksı) ve 4,5 m panel bölmesi eklenince sayılar değişir; derz maketi görünürlük için 12 mm çizili. Sayımı hep derleme zamanında üretmeyi ve 'maket modeli, gerçek proje değil' etiketini onaylar mısınız?
- **modüller** — Karışım ve zincir modüllerinde makine/tezgâh temsilî olacak (gerçek Söke hattı referansı yok); gerçek reçete, oran ve süre hiçbir yerde gösterilmeyecek: onaylı mı?
- **modüller** — Tır kabininde logo kararı (DEVIR teyit #1) ve tır/araç ayrıntısı yeterli kalite eşiğine gelmeden tır/forklift parça noktaları açılmasın: kalite kapısı için altın kare onayı kim verecek?
- **modüller** — Analitik: GTM'de 'ege_modul' olayı ve parametre şeması (modul, eylem, film_sn …) tanımlanabilir mi? Denenen modül rozeti için localStorage 'ege-modul' ve 'ege-yaris' kullanımı KVKK aydınlatmasında belirtilmeli mi (çerez değil, kişisel veri yok)?
- **modüller** — 14 modülün hepsi mi yoksa önceliğe göre ilk dalga (urun_secici, duvar_hesap, maket_blok_sayaci, once_sonra, kesit_gezgini, bilgi_yarismasi) mı hikâyeyle birlikte yayımlansın; kalanlar ikinci dalga olarak mı gelsin?
- **pazarlama** — 1. [KAPANDI · plan kararı] Açılış H1 = "Her yuva bir çizgiyle başlar." (eyebrow "EGE GAZBETON · Söke & İzmir" + tek cümle; akt-s0 t=0); slogan "Bugünden Yarına Güvenle" açılışta görünmez, yalnız t=140'ta (ödül) ve title/OG'de. Hero H1 ile eski t=2 vuruşu tek öğe; akt-s0 t=0/t=1/t=2 satırları buna göre güncellendi.
- **pazarlama** — 2. Hikâye boyunca üst çubukta logo SVG gizli, yerinde düz metin "Ege Gazbeton" bağlantısı mı kalsın (logo en sonda kuralı), yoksa mevcut yer tutucu logo baştan görünsün mü?
- **pazarlama** — 3. /katalog/ doğrudan PDF dosyası mı yoksa sayfa mı? Katalog "22.09.25" tarihli: güncel mi, İngilizce sürümü var mı (ihracat çipi için)?
- **pazarlama** — 4. /teklif/ formu ?urun=&kaynak=&dil=&kitle=&nokta= okuyup ön doldurabilir mi (site işi)? Ürün kodları (duvar, lento, ublok, tutkal, panel, egepor) uygun mu; form "bayi/ihracat" türünü ayırıyor mu?
- **pazarlama** — 5. /duvar-tasarla/ aracı tam olarak ne yapıyor (yalnız "Calculate your walls" metni var), sonucu teklif formuna aktarabilir mi? Aracın sonuç vaadi yoksa CTA metni "Duvarlarınızı hesaplayın" kalır.
- **pazarlama** — 6. /ihracat/ sayfasının içeriği/formu nedir; yurt içi bayilik başvurusu veya toplu alım akışı var mı ("Toplu alım ve bayilik →" CTA'sı buna bağlı)?
- **pazarlama** — 7. Hangi güven işaretleri ekranda kullanılabilir: CE belge numaraları (CE 2179-CPR-0043/0052) ve TS EN 771-4 (README'de var, DEVIR.md/dil.js'te yok), ISO 9001, TSE, EPD, kuruluş yılı, referans proje sayısı? ODTÜ −%17: yalnız panele mi tüm gazbeton sistemine mi ait, çalışma adı/yılı/bağlantısı var mı; taban kesme −%14 kullanılabilir mi?
- **pazarlama** — 8. Telefon/WhatsApp numarası, çalışma saatleri ve teklife "X saatte dönüş" vaadi verilebilir mi? (Yoksa mobil WhatsApp düğmesi ve vaat konmaz.) Teyit gelene dek WhatsApp düğmesi ve alt sabit çubuk finale konmaz (karar).
- **pazarlama** — 9. Sitede GA4/GTM ve onay (consent) aracı var mı (dataLayer adı "dataLayer" mı)? Mevcut aylık teklif sayısı taban çizgisi alınabilir mi? Hikâyesiz kontrol grubu için çerezsiz atama KVKK açısından uygun mu?
- **pazarlama** — 10. Tır kabinine logo çıkartması: SVG katmanıyla (3B'de yazı yok kuralına uyar) ya da EGE_LOGO ile basılırsa "logo en sonda" kuralıyla çelişir. Tır logosuz kalsın (lime streç + HTML etiket) mı?
- **pazarlama** — 11. Üretici ürün sayfaları "A1 Hiç Yanmaz" yazıyor (DEVIR.md); hikâyedeki ürün sayfası bağlantıları tutarlı olsun diye sayfa metni de "yangına tepki sınıfı" olarak düzeltilecek mi?
- **pazarlama** — 12. İngilizce için ayrı URL (/en/) ve hreflang planlanıyor mu? Şimdilik EN yalnız JS ile; arama motoru EN'i göremez. EN kopyada "lime" çift anlamı (kireç / renk) için "lime-green stretch film" kabul mü?
- **pazarlama** — 13. OG/paylaşım görseline (hikâye dışında) logo ve slogan metni PIL ile eklenebilir mi (3B içinde yazı kuralı yalnız renderlar için mi geçerli)?
- **pazarlama** — 14. Aliağa ve Alsancak limanları (dil.js'te var) kaynaklı mı; pazarlama metnine girsin mi? 1.100.000 m³ kapasite yıllık mı?
- **pazarlama** — 15. Kitle çipi etiketi TR "Ev / bina yapıyorum" (müteahhidi kapsar) kabul mü; müteahhit için ayrı çip/yol istenir mi?

## 3. Saniye saniye plan

### s0 · Hayalden yuvaya (ana giriş) — 0–32 sn

**Amaç.** Duygu: tek bir ışık noktası çizgiye, çizgi evin hacmine, hacim gazbeton duvara, duvar akşamın sıcak penceresine dönüşür. Mesaj: ev önce hayaldir; gerçek olunca onu yuva yapan şey malzemesidir. Sonda soru: bu evi iyi yapan ne?

#### t=0 (0:00) · 0 vh · p=0.0
- **Kare:** F000-F007 · 2B kâğıt K00-K07 (poster = F000) + canlı JS kıvılcım katmanı
- **Görsel:** Bej kâğıt, koyu vinyet, makro 2,2× yakın kadraj. Kapı konumunda tek sıcak ışık noktası nabız atıyor; eğik ışıkta kâğıt lifleri görünüyor.
- **Metin:** EGE GAZBETON · Söke & İzmir (eyebrow) / Her yuva bir çizgiyle başlar. (H1) / Gazbeton blok, lento, panel ve tutkal; Söke ve İzmir'deki iki fabrikada, tek kalite anlayışıyla. (tek cümle) — açılış paneli, CTA'larla  
  *EN:* EGE GAZBETON · Söke & İzmir (eyebrow) / Every home starts with a line. (H1) / AAC blocks, lintels, panels and adhesive from our two plants in Söke and İzmir, built to one standard of quality. (one sentence) — hero panel, with CTAs
- **Efekt:** Nabızlı ışık, 46 ışın uzar (mevcut küme), kâğıt lifi, 40 kor parçacığı süzülür. 2B +0,3 sn/kare; JS ≤0,4 ms.
- **Rakam · kaynak:** 2 fabrika (Söke ve İzmir) · Ege Gazbeton ortak rakamlar (yalnız cümlede ‘iki fabrika’; ayrı rakam kartı yok).
- **Etkileşim:** Parmak/fare kâğıtta soluk grafit iz bırakır (1 sn'de silinir). Kaydırmazsa 3 sn sonra kıvılcım kısa bir çizgi çeker, ‘Kaydırın’ oku nabız atar.
- **Pazarlama:** İlk izlenim: sıcak, el yapımı, çizgi. Marka adı (eyebrow) + ‘Her yuva bir çizgiyle başlar.’ ilk ekranda; tek lime ana düğme Teklif Al (Katalog/Teknik düğmeleri hero'da yok: pazarlama.json). Slogan açılışta görünmez; ‘Güven.’ sözcüğünü devralıp yalnız son t=140'ta (ödül) ve <title>/OG'de çıkar.
- **Üretim:** 2B kâğıt dokusu + ışık 0,3 sn/kare. JS canvas parçacık + iz. Efor 1 gün (ortak kivilcim.js).
- **Telefon:** Işık noktası üst-orta; hero metni üstte; parmak izi aynı.
- **Risk:** KARAR (pazarlama önerisi benimsendi, açık soru 1 kapandı): açılış H1 = ‘Her yuva bir çizgiyle başlar.’; slogan ‘Bugünden Yarına Güvenle’ açılışta YOK, yalnız son t=140 ve <title>/OG (metinleri pazarlama.seo_paylasim belirler); akt-son t=138-140 ‘Güven.’ → slogan sırası böylece ödül olur. Hero H1 ile eski t=2 vuruşu tek öğe: aynı cümle ikinci kez yazılmaz. Düğme/çip/atla t=1'de soluklaşır, H1 + cümle t=2'de çözülür: ekranda hiçbir an iki başlık yok (tek H1). H1 anahtar sözcük taşımaz; marka/ürün adı eyebrow + cümle + title'da (SEO etkisini site ekibi onaylamalı: pazarlama.seo_paylasim[4]).
#### t=1 (0:01) · 22 vh · p=0.03
- **Kare:** F008-F015 · 2B kâğıt K08-K15 (zoom 2,2×→1,5×) + canlı JS
- **Görsel:** Kıvılcım patlar: ışınlar kâğıdı boydan boya uzar, kamera geri çekilir. Hero düğmeleri/çipleri/‘atla’ soluklaşır, H1 + cümle yerinde kalır; bir ışın koyulaşıp ilk çizginin yönünü seçer.
- **Metin:** ↳ H1 + cümle sürer (t=0'dan); düğme/çip/atla soluklaşır.  
  *EN:* ↳ headline + sentence stay (from t=0); buttons/chips/skip fade out.
- **Efekt:** Işın demeti + 120 grafit/kor kıvılcımı yerçekimiyle saçılır, sıcak bloom. 2B +0,4 sn/kare; JS ≤0,5 ms.
- **Etkileşim:** Işın uçlarına gelen imleç ışını titretir. ‘Kaydırın’ ipucu kaymayla söner.
- **Pazarlama:** Görsel kafiye: bu ışık noktası ilk fikirdir; sonda pencere ışığı olarak geri döner.
- **Üretim:** Aynı 2B zemin; 2× süper örneklemeli plan karesinden kırpılır (zoom), 0,3 sn/kare.
#### t=2 (0:02) · 44 vh · p=0.06
- **Kare:** F016-F023 · P00-P07: üstten plan, 2B çizim motoru
- **Görsel:** Kıvılcım kalem ucuna dönüşür; ilk aks çizgisi kapı hizasından kâğıdı boydan boya geçer. Kamera 1,5×→1,0× çekilir, tam plan kadrajı oturur. Yeni metin yok: hero H1 + cümle çizgi geçerken soluklaşıp kalkar; ekranda yalnız aks balonu A belirir.
- **Metin:** A (aks balonu, SVG harf; yeni metin vuruşu yok)  
  *EN:* A (axis bubble, SVG letter; no new text beat)
- **Efekt:** Kalem ucu sprite + toz; çizgi başta ince, ortada koyu (basınç); kâğıt dişi; aks balonu A (SVG) pop. 2B +1,5 sn/kare.
- **Etkileşim:** Kalemin yoluna giren imleç grafit tozunu savurur.
- **Pazarlama:** Mimari titizlik: ev ölçülü bir çizgiyle başlar; marka tonu güven.
- **Üretim:** Bir kerelik üstten Freestyle+Position render 3200×1800 ≈100 sn; reveal 2B 1,5 sn/kare. Çizim motoru 4 gün (ortak).
- **Telefon:** Dikey kadraj: önce dikey akslar çizilir; plan alt-orta.
- **Risk:** ‘Her yuva bir çizgiyle başlar.’ burada TEKRARLANMAZ: t=0'daki hero H1'dir (açık soru 1 kapandı); H1 + cümle çizgi geçerken CSS clip-path/opacity ile kalemle senkron çözülür, t=3'te ‘Önce fikir…’ vuruşu gelir. Kalem sprite kodla çizilir (görsel indirme yok); canvas üstünde blend yok.
#### t=3 (0:03) · 66 vh · p=0.09
- **Kare:** F024-F031 · P08-P15
- **Görsel:** Akslar kesişir; kalem kolon karelerini tek tek damgalar, sonra duvar konturunu kalın basınçla bağlar. Bina ayak izi netleşir.
- **Metin:** Önce fikir, sonra plan: güneşe, sokağa ve bahçeye göre.  
  *EN:* First the idea, then the plan: shaped by the sun, the street and the garden.
- **Efekt:** Her damgada 6 kıvılcım; aks balonları B-D ve 1-3 SVG pop; kalın kontur daha koyu. 2B +1,5 sn/kare.
- **Etkileşim:** Aks balonuna dokun/hover: aks çizgisi kalınlaşır (yalnız vurgu, rakam yok).
- **Pazarlama:** Öğretici: ev kolon-aks ızgarasında kurulur; gazbeton bu karkasın içine örülecek.
- **Üretim:** Reveal 2B; balon konumları kit.project çapalarından (meta.json), SVG. 1 gün.
- **Risk:** Ölçü rakamı yazılmaz: örnek yapı ölçüsünün kaynağı yok (teyit gerekli).
#### t=4 (0:04) · 88 vh · p=0.13
- **Kare:** F032-F039 · P16-P23
- **Görsel:** Planın çevresine kesik çizgili güneş yayı ve kuzey oku çizilir. Kalem sokağa iner: kaldırım, bordür, asfalt, kesik şeritler soldan sağa.
- **Metin:** ↳ cümle sürer; ‘güneşe’ ve ‘sokağa’ sözcüklerinin altı çizim anında çizilir.  
  *EN:* ↳ sentence stays; ‘sun’ and ‘street’ are underlined as they are drawn.
- **Efekt:** Güneş sembolünün ışınları açılıştaki kıvılcım ışınlarıdır (kafiye); şeritler tak-tak damgalanır. 2B +1,5 sn/kare.
- **Etkileşim:** ‘Sokak’ noktası belirir; dokununca Sokak kartı.
- **Pazarlama:** Ev tek başına değil: güneşe, sokağa, bahçeye göre düşünülür.
- **Üretim:** Aynı reveal; güneş yayı ve kuzey oku SVG stroke-dashoffset. 1 gün (JS).
- **Telefon:** Kuzey oku sağ üstte.
- **Risk:** Altı çizili sözcükler lime olamaz (lime = bizim ürün): grafit/sıcak ton.
#### t=5 (0:05) · 110 vh · p=0.16
- **Kare:** F040-F047 · P24-P31
- **Görsel:** Bahçe: giriş yolu, alçak duvar, ağaç taçları sık dairesel taramayla, lavanta halkaları; komşu ev izleri silik. Plan tamamlanır, kalem kalkar.
- **Metin:** ↳ ‘bahçeye’ altı çizilir.  
  *EN:* ↳ ‘garden’ is underlined.
- **Efekt:** Taçlar el yapımı spiralle taranır; plan kâğıda ‘oturur’: hafif gölge ve kâğıt nefesi. 2B +1,5 sn/kare.
- **Etkileşim:** Giriş ve Bahçe noktaları: dokununca kart.
- **Pazarlama:** Yuva fikri: kapıdan sokağa uzanan yaşam alanı; bahçe sıcaklık katar.
- **Üretim:** Aynı reveal, son 8 kare; 1,5 sn/kare.
#### t=6 (0:06) · 132 vh · p=0.19
- **Kare:** F048-F055 · P32-P33 + E00-E05 (eğim başlar)
- **Görsel:** Plan oturur; kamera üstten eğilmeye başlar, zemin çizgileri perspektife kayar. Kalem dört köşe kolonuna gider. Hiçbir şey yerden yükselmez.
- **Efekt:** Kamera eğimi 0→0,3; vinyet yumuşar; çizgiler dünya uzayına bağlı (Position geçişi), kaymaz. Blender +28 sn/kare.
- **Etkileşim:** İmleç/jiroskop sahneyi ±14 px eğer (mevcut EGIM_PX).
- **Üretim:** egim-v2: bina tam boy, kâğıt malzeme; scale.z ve hide_render animasyonu SİLİNİR. Freestyle+Position+Normal ≈28 sn/kare.
- **Risk:** Üstten bakışta tam boy çatı plan çizgisine karışır: zaman haritasıyla gizlenir. Altın kare E04 onayı.
#### t=7 (0:07) · 154 vh · p=0.22
- **Kare:** F056-F063 · E06-E13
- **Görsel:** Kamera göz hizasına iner. Köşe kolonlarından dikmeler kalemle tek hamlede çizilir (sağ ön köşe önce); kat hizaları ve parapet yatay çekilir.
- **Efekt:** Kalem ucu görünür, grafit tozu aşağı dökülür; köşe aşımı mevcut ‘Uzat’ ayarıyla. 2B +0,5 sn/kare.
- **Etkileşim:** Kalem ucuna gelen imleç tozu savurur.
- **Pazarlama:** Plan → hacim: ‘çizgiden eve’ mantığı okunur.
- **Üretim:** E kareleri ≈28 sn/kare; kalem ucu konumu meta.pen (kare başı 1 nokta) JS sprite'a gider.
- **Telefon:** Ev ekranın alt yarısında; dikmeler daha uzun görünür.
- **Risk:** Dikmeler aynı anda büyürse ‘yükseliyor’ okunur: tek kalem, sıralı hamle (kullanıcı şikâyeti).
#### t=8 (0:08) · 176 vh · p=0.25
- **Kare:** F064-F071 · E14-E21
- **Görsel:** Kamera C'ye yaklaşır. Pencere kutuları, kapı ve lento hatları kalem darbeleriyle tek tek çizilir; yan cephe ve çatı hatılı tamamlanır.
- **Metin:** Çizgi hacme dönüşür.  
  *EN:* Lines become volume.
- **Efekt:** Her pencere 3 darbe, farklı basınç; doğrama çizgileri ince. 2B +0,5 sn/kare.
- **Pazarlama:** Eskizdeki pencere ve kapı yerleri sonra ürün turunda duvar/lento duraklarına bağlanır.
- **Üretim:** E kareleri ≈28 sn/kare; çizim motoru ‘pencere kutusu’ vuruş sırası.
#### t=9 (0:09) · 198 vh · p=0.28
- **Kare:** F072-F079 · E22-E29
- **Görsel:** Tarama: doğu yan yüz yoğun 45° taramayla kararır, ön cephe seyrek; zemine düşen gölge taranır. Kalem şeritleri soldan sağa sürükler.
- **Efekt:** AO/Normal geçişinden türeyen tarama; şerit başı 0,3 sn; kâğıt dişi. Blender +2 sn, numpy +1,5 sn/kare.
- **Etkileşim:** Eskiz noktası: dokununca ‘İlk çizgiler: kütle, pencereler, bahçe duvarı’ kartı.
- **Pazarlama:** Çizimle hacim hissi: tasarım emeği görünür.
- **Üretim:** Normal+AO geçişi aynı render'da; tarama 2B (çizim motoru ‘tarama’ kipi).
- **Risk:** Tarama aşırı yoğunsa ev karanlık kalır: aydınlık yüzde seyrek tutulur, altın kare E24.
#### t=10 (0:10) · 220 vh · p=0.31
- **Kare:** F080-F087 · E30-E37
- **Görsel:** Son dokunuşlar: camlara tek yansıma çizgisi, ağaçlar taranır; aks çizgileri silgiyle silikleşir. Kamera C'ye oturur, kalem kalkar, ucunda son kıvılcım.
- **Efekt:** Silgi: yardımcı çizgi alfası 1→0,2 ve kâğıt tozu; kalem ucu kıvılcımı evin merkezine yönelir. 2B +1 sn/kare.
- **Etkileşim:** Kalem kalkınca kıvılcıma dokun: bir sonraki sahneye hızlı kaydırma ipucu.
- **Pazarlama:** Eskiz tamam: yatırımcı/mimar için ‘fikrim hazır’ anı.
- **Üretim:** E30-E37 ≈28 sn/kare; kıvılcım konumu = dolum D00 parlak piksel ağırlık merkezi (mevcut hesap).
- **Risk:** Kamera C'ye oturuş E37'de dolum D00 kadrajıyla birebir olmalı.
#### t=11 (0:11) · 242 vh · p=0.34
- **Kare:** F088-F095 · W00-W07: eskiz E37 → dolum D00 (2B)
- **Görsel:** Kalemin kıvılcımı binanın merkezine uçar, karanlık daire olarak açılır; dairenin içinde kurşun çizgiler beyaz tel kafese döner.
- **Efekt:** Dairesel silme (mevcut) + yırtık kâğıt kenarı (gürültü maskesi) + sınırda ışık halkası; içeride grafit→beyaz tersleme. 2B +0,8 sn/kare.
- **Etkileşim:** Halka kaydırmayla büyür; kaydırma durunca halka nabız atar.
- **Pazarlama:** Fikirden karkasa: çizgi ‘yapı’ya döner.
- **Üretim:** Mevcut D adımı 6→8 kare; 0,8 sn/kare, 0,5 gün.
- **Risk:** Halka rengi soğuk beyaz (lime değil).
#### t=12 (0:12) · 264 vh · p=0.38
- **Kare:** F096-F103 · D00-D07: dolum-v2 (Blender)
- **Görsel:** Siyah boşlukta beyaz karkas ve ışıyan tel kafes duvarlar. Zemin kat blokları 0,9 m yüksekten süzülüp tek tek yerine oturur.
- **Metin:** Duvarlar gazbetonla, sıra sıra.  
  *EN:* AAC walls, course by course.
- **Efekt:** Son örülen sıranın derzi lime ince çizgi ışıldar, sonra söner (tutkal vurgusu); parlak zemin yansıması; bloom. Blender +4 sn/kare.
- **Etkileşim:** Kat çipi ‘ZEMİN → 1. KAT → 2. KAT’ dolum ilerledikçe dolar.
- **Pazarlama:** Ürün sahneye girer: gazbeton duvar karkasın içine örülür.
- **Üretim:** Mevcut dolum betiği + lime sıra ışıltısı; ≈55 sn/kare × 40 kare.
- **Telefon:** Tel kafes dar kadrajda büyük görünür; kat çipi üstte.
- **Risk:** Lime yalnız ürün (blok/derz/lento) üzerinde; karkas beyaz, donatı ve çelik yeşil olmaz.
#### t=13 (0:13) · 286 vh · p=0.41
- **Kare:** F104-F111 · D08-D15
- **Görsel:** Zemin kat tamamlanır, ilk kat blokları şaşırtmalı örgüyle iner. Kamera 40 cm sağa kayar: paralaks derinlik; ışıyan teller bloklara dönüşür.
- **Metin:** Karkasın içine 60 × 25 cm bloklar, 1–3 mm derzle örülür.  
  *EN:* Inside the frame, 60 × 25 cm blocks are laid with 1–3 mm joints.
- **Efekt:** İsteğe bağlı hacimsel ışık huzmesi + havada toz (kit.dust). Blender +35 sn/kare (gürültülü, opsiyonel); bloom.
- **Rakam · kaynak:** 60 × 25 cm blok yüzü · Ürün föyleri
- **Etkileşim:** Blok noktası: dokununca Gazbeton blok kartı (60 × 25 cm, şaşırtmalı).
- **Pazarlama:** Öğretici: nizami örgü; hızlı örülen, düz yüzeyli duvar.
- **Üretim:** Kamera C'de başlayıp biter (arası ±40 cm). Dolum ≈55 sn/kare.
- **Risk:** Kamera kayması son karede C'ye dönmezse sokak karesiyle silme uyuşmaz.
#### t=14 (0:14) · 308 vh · p=0.44
- **Kare:** F112-F119 · D16-D23 + makro M00-M07 (büyüteç)
- **Görsel:** İki blok arasında büyüteç dairesi açılır: içinde makro, blok iner, tutkal şeridi ezilip 1–3 mm derze döner. Altta duvar örülmeye sürer.
- **Efekt:** Daire maskeli makro (2B); derzde lime tutkal vurgusu; SVG ölçü çizgisi. Makro Blender +30 sn/kare × 8 kare.
- **Rakam · kaynak:** 1–3 mm ince derz · Ürün föyleri
- **Etkileşim:** Derz noktası ve büyüteç: dokununca İnce derz kartı (1–3 mm).
- **Pazarlama:** Teknik güven: ince derz = düz, homojen duvar.
- **Üretim:** stil_r5.sahne_derz taslağından makro: 8 kare × 30 sn; büyüteç 2B. Efor 1 gün.
- **Telefon:** Büyüteç alt yarıda, ölçü çizgisi dikey.
- **Risk:** Tutkal gerçek rengi gri; yalnız kenar ışıltısı lime. Rakam yalnız föy kaynaklı (1–3 mm).
#### t=15 (0:15) · 330 vh · p=0.47
- **Kare:** F120-F127 · D24-D31
- **Görsel:** Pencere ve kapı üstüne uzun lentolar düşer; lento anlık lime kenar ışıltısı alır. Katlar yükselirken kamera C'ye geri döner.
- **Efekt:** Lento kenarında 0,5 sn lime ışıltı (ürün vurgusu) + bloom. Blender +2 sn/kare.
- **Rakam · kaynak:** 4,50 m'ye kadar lento açıklığı · Ürün föyleri
- **Etkileşim:** Lento noktası: dokununca Lentolar kartı.
- **Pazarlama:** Aynı malzemeden süreklilik: lento duvarla bütünleşir.
- **Üretim:** Dolum ≈55 sn/kare; lento ışıltısı emisyon animasyonu 0,5 gün.
#### t=16 (0:16) · 352 vh · p=0.5
- **Kare:** F128-F135 · D32-D39
- **Görsel:** Çatıda paneller sırayla kapanır; doğrama ve camlar yerine gelir. Cam gökten ışık alır; bina bütünleşir, kamera tam C'de durur.
- **Efekt:** Son panelde duvar boyunca alttan üste tek seferlik lime tarama ışığı (ürün ‘tamam’). Blender +1 sn/kare.
- **Rakam · kaynak:** 6 m'ye varan panel açıklığı · Ürün föyleri
- **Etkileşim:** Panel noktası: Çatı panelleri kartı.
- **Pazarlama:** Karkas + duvar + çatı: eksiksiz sistem; ürün gruplarına işaret (s1'e hazırlık).
- **Üretim:** Dolum ≈55 sn/kare; panel/cam mevcut.
#### t=17 (0:17) · 374 vh · p=0.53
- **Kare:** F136-F143 · G00-G07 (D39 → sokak S00-S07 altta oynar)
- **Görsel:** Sol alttan yukarı sağa lime tarama çizgisi ilerler; arkasında siyah boşluk gündüz sokağa döner: ağaçlar, kaldırım, kırmızı park halindeki araba, bisikletli.
- **Metin:** Çizimden gerçeğe.  
  *EN:* From drawing to reality.
- **Efekt:** Çapraz silme + lime çizgi + hale (mevcut); çizgi boyunca 60 kıvılcım; silinen alan canlı sokak karelerini oynatır. 2B +0,6 sn/kare.
- **Etkileşim:** Kaydırma durunca tarama çizgisi nabız atar.
- **Pazarlama:** Dönüm noktası: hayal gerçek malzemeye (gazbeton cephe) dönüşür.
- **Üretim:** G kareleri 2B: D39 + S00-S15, 0,6 sn/kare. Kırmızı araba v2: A-sütunu eğimli, uzun kaput, bütün far/ızgara (araba() profil dizileri), 1 gün.
- **Telefon:** Silme çizgisi dikeyde alttan üste; sokak kadrajı dar.
- **Risk:** Lime tarama çizgisi marka şeridi gibi okunur (mevcut, onaylı kullanım). Kırmızı araba önü şikâyeti bu yenilemeyle kapanır.
#### t=18 (0:18) · 396 vh · p=0.56
- **Kare:** F144-F151 · G08-G15 (S08-S15 altta)
- **Görsel:** Silme sağa tamamlanır; ev gerçek gazbeton cephesiyle belirir. Mavi araba sağdan geçer (hareket bulanıklı); bisikletli pedal çevirerek ağaçların önünden süzülür.
- **Efekt:** Cycles hareket bulanıklığı (shutter 0,35) araba ve bisikletli için. Blender +18 sn/kare.
- **Etkileşim:** Bisikletli noktası: dokununca ince dalga halkası (zil), kart yok.
- **Pazarlama:** Yaşayan mahalle: eller gidonda, pedal dönüyor; gerçeklik dili.
- **Üretim:** sokak-v2 S08-S15; bisiklet pedal/tekerlek dönüşü yeni (krank boş nesnesi + IK hedefleri). Blender ≈96 sn/kare.
- **Risk:** Krank rig'i yeni iş; olmazsa serbest sürüş (mevcut) kalır.
#### t=19 (0:19) · 418 vh · p=0.59
- **Kare:** F152-F159 · S16-S23
- **Görsel:** Tırın lime şeritli kabini sağ kenardan girer; kamera 3° sağa yatıp tırı karşılar, lens 24→28 mm. Kabin camında gök yansıması, ızgara, aynalar.
- **Metin:** Sokakta hayat başlar.  
  *EN:* Life starts on the street.
- **Efekt:** DOF f/4, odak tır düzleminde; hareket bulanıklığı; kabin camı yansıması. Blender +8 (DOF) +18 (bulanıklık) sn/kare.
- **Pazarlama:** Marka sahneye girer: kabinde lime şerit; logo yok (kural), marka lime streçle okunur.
- **Üretim:** Tır v2 (kabin ayrıntı, ızgara, ayna, jant, tekerlek dönüşü) 2 gün; kamera animasyonu kare başı +0 sn.
- **Telefon:** Kabin ekranın tüm yüksekliğini kaplar; kamera daha az döner.
- **Risk:** Kamera yaw/lens S63'te C'ye dönmeli (S63 = plaka A00 kadrajı).
#### t=20 (0:20) · 440 vh · p=0.63
- **Kare:** F160-F167 · S24-S31
- **Görsel:** Kabin evin önünden geçer; çekici ayrıntıları: spoyler, güneşlik, projektörler, jant somunları. Tırı izleyen ‘Ege Gazbeton’ etiketi lime noktayla doğar.
- **Metin:** Yoldan geçen tırda Söke ve İzmir'den gelen gazbeton paletleri.  
  *EN:* On the passing truck: AAC pallets from Söke and İzmir.
- **Efekt:** Etiket HTML (3B içinde yazı yok), kare başı hotspot çapası; kabin gölgesi yola düşer. Blender +0; JS 0,2 ms.
- **Rakam · kaynak:** 2 fabrika (Söke ve İzmir) · Ege Gazbeton ortak rakamlar. Palet adedi/tır kapasitesi yazılmaz (teyit gerekli).
- **Etkileşim:** Tır etiketi: dokununca Ege Gazbeton kartı (Lime streçli paletler: Söke ve İzmir'den sahaya).
- **Pazarlama:** Reklam çekirdeği: tır = fabrikadan sahaya güven; etiket markayı söyler.
- **Üretim:** meta.json tir çapası (mevcut) + yeni: kare başı 2 nokta (kabin, palet merkezi). JS 0,5 gün.
- **Telefon:** Etiket tırın üstünde tek satır; kart alt sayfa.
- **Risk:** Etiket + başlık + cümle = 3 öğe: etiket 2 kelime, kart kapalı; okuma kuralı sınırda.
#### t=21 (0:21) · 462 vh · p=0.66
- **Kare:** F168-F175 · S32-S39
- **Görsel:** Dorse girer: lime streçli paletler yan görünüşte, gazbeton bloklar filmin içinden seçilir; amber kayışlar. Kamera tırı yarı hızla izler.
- **Efekt:** Streç: ince şeffaf lime film, kırışık bump, güneş çizgileri yansıması. Blender +10 sn/kare (şeffaflık sıçraması).
- **Etkileşim:** Palete gelen imleç: palet çevresinde lime halka (SVG), kart yok.
- **Pazarlama:** Lime streç = marka rengi, ürün ambalajı: tır bir reklam panosu gibi okunur.
- **Üretim:** strec_m v2 (transmission + normal) 1 gün; palet ahşap ayak ayrıntısı 0,5 gün.
- **Risk:** Kayış, çelik, tuğla yeşil olamaz: kayış amber (mevcut).
#### t=22 (0:22) · 484 vh · p=0.69
- **Kare:** F176-F183 · S40-S47
- **Görsel:** Tır ekranın ortasında: iki sıra lime palet tam karşıda, kamera tırla yan yana kayıyor; arkada ev ve ağaçlar alan derinliğiyle yumuşar.
- **Efekt:** Hero planı: DOF odak palette, ev/ağaç bokeh; güneş kırışık streçte parlar. Blender toplam ≈100 sn/kare.
- **Etkileşim:** Palet halkasına dokun: Ege Gazbeton kartı açılır; kaydırma durursa palet üstünde lime parıltı nabzı.
- **Pazarlama:** En net marka karesi: slogansız, logosuz, yalnız lime ve etiket; paylaşılabilir ekran görüntüsü.
- **Üretim:** Altın kare S44 (tır net) onayı; tüm S kareleri ≈96-100 sn/kare × 64.
- **Telefon:** Tır ortada, ev üst planda; etiket üstte.
- **Risk:** Okunurluk: 3B yazı yok; etiket ve palet halkası tırı tek başına anlatmalı. Altın kare onayı.
#### t=23 (0:23) · 506 vh · p=0.72
- **Kare:** F184-F191 · S48-S55
- **Görsel:** Dorsenin arkası geçer: ikiz lastikler dönüyor, yan koruma, stop lambaları, çamurluk. Tır yola gölge düşürerek solda kadrajdan çıkmaya başlar.
- **Efekt:** Tekerlek dönüşü yol/yarıçap; hareket bulanıklığı; gökte 5 martı süzülür (2B sprite +0,2 sn/kare).
- **Etkileşim:** Etiket altında ‘Ürünleri gör ↓’ mikro bağlantısı: ürün turuna atlar.
- **Pazarlama:** CTA: tırdan ürüne geçiş (ürün turu s1).
- **Üretim:** Martı sprite 3 kare döngü 2B, 0,5 gün; tekerlek dönüşü tır v2 içinde.
- **Telefon:** Bağlantı alt sayfa çipi olarak.
#### t=24 (0:24) · 528 vh · p=0.75
- **Kare:** F192-F199 · S56-S63
- **Görsel:** Tır sol kenardan çıkar, yol boş. Anne ve çocuk bahçe yolundan kapıya varır; kapı aralanır, içeriden sıcak ışık yola düşer, ikisi girer, kapı kapanır.
- **Efekt:** Kapı menteşe animasyonu + SPOT sıcak ışık sızıntısı 2 kare. Blender +5 sn/kare; yüz görünmez (≥12 m, yan/arka).
- **Etkileşim:** Kapı/Giriş noktası: dokununca Giriş kartı.
- **Pazarlama:** Duygusal köprü: eve dönüş; yuva fikri ilk kez insanla kurulur.
- **Üretim:** Kapı ayrı nesne (B.kur 'kapi' menteşe boş nesnesine) 1 gün; aile yolu kaldırımdan kapıya ≈9 m, 1,2 m/sn.
- **Risk:** S63'te hareketli nesne kalmamalı: erkek/yaşlı yaya çerçeve dışına alınır ya da A00 erimesinde hayalet bırakmaz.
#### t=25 (0:25) · 550 vh · p=0.78
- **Kare:** F200-F207 · H00-H07 (S63 → plaka A00-A04, 2B erime)
- **Görsel:** Zaman akar: kamera sabit, gölgeler uzar, bulutlar kayar, sokak sessizleşir. Sol üstte ince güneş yayı belirir; güneş noktası batıya ilerler.
- **Metin:** Gün biter, ışıklar yanar.  
  *EN:* The day ends, the lights come on.
- **Efekt:** Aşamalar arası 2-3 ara kare erimesi; martı + 25 yaprak savrulması (2B +0,4 sn/kare); gün yayı SVG.
- **Etkileşim:** Gün yayındaki güneş noktasını sürükle: zaman sarılır (kaydırmaya eşdeğer).
- **Pazarlama:** Güven: gün boyu ayakta duran yapı; plandaki güneş yayı geri döner.
- **Üretim:** plaka-v2: 14 aşama (A00-A13) ≈150 sn/kare ≈35 dk/varyant; bu saniye A00-A04.
- **Telefon:** Gün yayı üst orta.
- **Risk:** Aşamalar arası gölge hayaleti: ≥12 aşama gerekli; erimede gölge çiftlenirse aşama artırılır.
#### t=26 (0:26) · 572 vh · p=0.81
- **Kare:** F208-F215 · H08-H15 (A04-A08)
- **Görsel:** Altın saat: cephe kehribar, uzun gölgeler asfaltı şeritlere böler; güneş ağaç taçlarından huzmeler saçar. Asfalt alçak ışıkta parlar.
- **Efekt:** Işık huzmesi (Glare Sun Beams) +1 sn; ıslak asfalt etkisi roughness 0,88→0,3 +12 sn; Mist hava perspektifi +0,5 sn/kare.
- **Etkileşim:** Fare cepheye gelince huzme yönü ±5° kayar (2B).
- **Pazarlama:** Duygu: sıcaklık; gazbeton cephe altın ışıkta ‘ev’ gibi görünür.
- **Üretim:** A04-A08 ≈165 sn/kare; ıslak asfalt tüm aşamalar için ortak malzeme parametresi.
- **Risk:** Huzme yönü güneş yönüne (rot 200→250°) bağlı: önizlemeyle teyit; ıslak asfalt kuru gündüz karesine sıçramamalı (kademeli).
#### t=27 (0:27) · 594 vh · p=0.84
- **Kare:** F216-F223 · H16-H23 (A08-A12)
- **Görsel:** Mavi saat: gök mora döner, sokak lambaları yanar, asfaltta sıcak ışık adaları. Zemin kat penceresi ilk yanar; sonra ikinci kat.
- **Efekt:** Lamba SPOT'ları + cam parlaklığı; pencere ışığı 2700 K, hafif titreme. Blender A09-A12 ≈165 sn/kare.
- **Etkileşim:** Karanlık pencereye dokun: ışığı sen yak (A13 karesi poligon maskesiyle kırpılır).
- **Pazarlama:** ‘Yuva’ anı: aile girdi, ilk ışık yandı (nedensellik).
- **Üretim:** Pencere poligonları meta.pencereler (mevcut); JS canvas clip + drawImage ≈0,3 ms.
- **Telefon:** Pencereler küçük: dokunma hedefi 44 px'e genişletilir.
- **Risk:** Etkileşim için A13 karesi önceden yüklenmeli (indirme önceliği).
#### t=28 (0:28) · 616 vh · p=0.88
- **Kare:** F224-F231 · H24-H31 (A12 → A13, pencere maskeleri)
- **Görsel:** Pencereler tek tek yanar: mutfak, salon (TV mavi titreşir), çocuk odası yıldız lambası; ışıklar ıslak asfalta yansır. Ev ışıldar.
- **Metin:** Peki bu evi iyi yapan ne?  
  *EN:* So what makes this home so good?
- **Efekt:** Maske erimesi 10 adım (mevcut) + bloom; TV mavi titreşim 2B tint; ışık sızıntısı. 2B +0,5 sn/kare.
- **Etkileşim:** Yuva noktası: dokununca ‘Akşam olur; her pencerede başka bir hayat.’ kartı.
- **Pazarlama:** Duygusal zirve; soru ürün turunun kapısı.
- **Üretim:** Mevcut pencere maske erimesi; TV tint yeni (2B, 0,2 sn/kare).
- **Risk:** Her pencere farklı sıcaklıkta olmalı; hepsi aynı sarı olursa ‘maket’ okunur.
#### t=29 (0:29) · 638 vh · p=0.91
- **Kare:** F232-F239 · X00-X07 (A13 → çıkış K1, 2B maske)
- **Görsel:** Işıklı ev, kamera sabit. Gökyüzü ufuktan beyaza açılır; kaldırım, komşu evler ve lambalar sis gibi erir. Ev merkezde kalır.
- **Metin:** ↳ soru ekranda sürer.  
  *EN:* ↳ the question stays on screen.
- **Efekt:** Alttan yukarı beyaz sis (2B gradyan + bina maskesi), hava perspektifi artar, huzme söner. 2B +0,8 sn/kare; Blender K1 ≈120 sn.
- **Etkileşim:** ‘Kaydırın’ ipucu yeniden belirir: ürünleri keşfedin.
- **Pazarlama:** Köprü: ev güzel; peki içinde ne var?
- **Üretim:** ‘cikis’ kipi: Holdout ile sokak/ağaç solması + gök beyaz; bina maskesi (IndexOB) 2B; 2 anahtar kare.
- **Telefon:** Beyaz zemin üstten başlar; metin koyu renge döner.
- **Risk:** Sözleşme yorumu: ‘s0 son karesi akşam, pencereler yanık’ çıkışın BAŞLANGICI (t=29) sayıldı; son kare s1 F000.
#### t=30 (0:30) · 660 vh · p=0.94
- **Kare:** F240-F247 · X08-X15 (K1 → K2)
- **Görsel:** Sokak, ağaç, araçlar tümüyle beyaza erir; ev stüdyo zemininde tek başına, yumuşak temas gölgeli. Cephe röntgene döner: gazbeton dokusu saydamlaşır.
- **Efekt:** Malzeme karışımı 0,4→0,8 (s1_urun geçiş malzemesi: gerçek↔röntgen↔saydam); pencere ışıkları kısılır. Blender K2 ≈120 sn.
- **Pazarlama:** Ev gerçek malzemeden ‘içine bakılan’ hayalete dönüşür: şeffaflık = güven.
- **Üretim:** K2 = stüdyo + ev %50 röntgen; s1_urun.gecis_malzeme parametresi 0→1; 2B maske erimesi 0,8 sn/kare.
- **Risk:** Röntgen çizgileri soğuk gri-mavi (lime değil); lime yalnız s1 duraklarında ürün vurgusu.
#### t=31 (0:31) · 682 vh · p=0.97
- **Kare:** F248-F255 · X16-X23 (K2 → s1 F000)
- **Görsel:** Hayalet ev beyaz stüdyoda, s1'in ilk karesiyle aynı kadraj; pencerelerdeki sıcak ışık son kez nabız atar, sonra %15 kalır.
- **Efekt:** Röntgen malzemesi 1,0; sıcak ışık %15 kalıcı (lime değil). X23 ile s1 F000 piksel farkı <%1. 2B +0,3 sn/kare.
- **Etkileşim:** İpucu oku ‘Ürünleri keşfedin’ nabız atar.
- **Pazarlama:** Köprü: hayal → yuva → ‘neden iyi?’; ürün turu başlıyor.
- **Üretim:** X23 = s1 F000 ortak kare (tek render, iki perdede kullanılır); 2B eşleme testi 0,5 gün.
- **Risk:** X23 = s1 F000 birebir: aynı kamera, kaydırma, pozlama. Altın kare X23; sıcak pencere ışığı s1 ile mutabakat.

**Geçiş ve üretim notu (s0).** Satırlar t=0..31 (t_son=32 dışlayıcı). Kare haritası: tek tip 8 kare/sn, t satırı = F[8t]…F[8t+7], toplam 256 kare (eski 162); telefon her 2. kare. Kaynak kodları: K kâğıt, P plan, E eğim+eskiz, W daire silme, D dolum, M makro derz, G çapraz silme, S sokak (64 kare, G altında S00-S15 oynar), H gün, A plaka aşaması, X çıkış. ÇIKIŞ t=29-31 (F232-F255): sözleşmedeki 'son kare akşam, pencereler yanık' bu geçişin BAŞLANGICI (t=29); X23 = s1 F000 (stüdyoda hayalet ev, aynı C kadrajı) piksel eşleşir. s1 t=32 pencere ışığını röntgen mavisine söndürür; s0 sıcak ışığı %15 bırakır.

**Gereken yeni işler (s0):**
- Çizim motoru (tools/cizim_kalem.py): Position+Normal geçişinden dünya-uzayı zaman haritası, tek kalemle sıralı vuruş, basınç, tarama, silgi, meta.pen (kalem ucu konumu). 4 gün; +3 sn/kare.
- s0_hayal.py egim-v2: scale.z/hide_render yükselme animasyonu silinir, bina tam boy kâğıt malzeme; aks çizgileri, güneş yayı, ağaç tacı halkaları; üstten 3200×1800 plan karesi; E00-E37 (38 kare).
- tools/s0_birlestir.py yeniden: 256 karelik zaman çizelgesi (8 kare/sn), kâğıt zoom K, plan P, daire silme W (8 kare), çapraz silme G (S altında), gün H, çıkış X.
- Web/JS: kivilcim.js canlı katman (kalem sprite, grafit tozu, imleç izi, boşta nefes), martı/yaprak sprite, tır takip etiketi + palet halkası, ışığı-sen-yak pencere maskeleri, aks balonu + güneş yayı + gün yayı SVG. Bütçe ≤0,6 ms/kare, DPR ≤1,25.
- Dolum-v2: lime sıra ışıltısı, C'de biten ±40 cm kamera sürüklenmesi, makro derz 8 kare + büyüteç (stil_r5.sahne_derz taslağı).
- Sokak-v2 (64 kare, 8 sn): koreografi (mavi araba, bisikletli, aile kapıya, tır s=2,2-7,8), kamera yaw/lens animasyonu, DOF + hareket bulanıklığı; ≈96-100 sn/kare.
- Araç yenileme: tır v2 (kabin ızgara/ayna/jant, ikiz lastik, tekerlek dönüşü, şeffaf lime streç + kırışık bump), kırmızı araba ön profili (araba()), bisiklet krank/pedal dönüşü, kapı ayrı menteşeli nesne.
- Plaka-v2: 14 aşama (A00-A13), ıslak asfalt kademesi, Sun Beams huzmesi, Mist, sokak lambaları, pencere ışığı çeşitliliği (TV, mutfak, yıldız lamba), kapı ışığı. ≈150-165 sn/kare.
- ‘cikis’ kipi: Holdout ile sokak solması, gök beyaz, stüdyo zemini, s1_urun geçiş malzemesi; K1, K2 anahtarları + X kareleri; X23 = s1 F000 (s1 yazarıyla mutabakat).
- ayarlar.js s0 boy 560→704 vh; dil.js: yeni h0e ‘Çizgi hacme dönüşür.’, kısaltılmış h0b.metin; vuruş p aralıkları h0 0,09-0,22 (başlığı hero H1'e taşındı), h0e 0,25-0,33, h0b 0,38-0,52, h0c 0,53-0,77, h0d 0,78-1,01. Açılış kararı (açık soru 1 kapandı): index.html H1 + dil.js giris.baslik TR/EN = ‘Her yuva <em>bir çizgiyle</em> başlar.’ / ‘Every home starts <em>with a line.</em>’; giris.metin = t=0 cümlesi (‘Kaydırın, hikâyeyi izleyin’ cümleden çıkar, ipucu giris.kaydir okunda); h0.baslik kalkar, h0 vuruşu yalnız ‘01 · Hayal’ + ‘Önce fikir, sonra plan…’ olur (article aria-labelledby → giris-baslik); slogan yalnız son.slogan ve <title>/OG.
- Toplam Blender ≈3,5 sa/varyant (d); telefon EGE_MINSTEP=2 ile ≈1,8 sa. Kare yükü ≈11 MB (d) / ≈5 MB (m): ilk 24 kare ve A13 önce iner. Altın kareler: E04, E24, D20, S44, A09, X23.

### s1 · Ürün turu: bu evi iyi yapan ne? — 32–70 sn

**Amaç.** Merak, keşif, güven. Soru ile açılır; izleyici evin etrafında dolaşıp altı ürünü gerçek yerinde görür, her durakta NEREDE kullanıldığını ve NE KAZANDIRDIĞINI tek bir görsel mekanizmayla öğrenir (ısı oku, açıklık ölçüsü, beton dolumu, derz çizgisi, kütle çubuğu, kaplama). Rakamlar kaynağıyla gelir. Çıkışta altı ürün tek sistem olarak yanar ve 'peki bu blok nasıl doğuyor?' merakıyla tek bloğa dalınır.

#### t=32 (0:32) · 704 vh · p=0.0
- **Kare:** Blender s1_urun f000–003 (f000 = s0 çıkış karesiyle birebir)
- **Görsel:** Beyaz stüdyoda hayalet ev, s0 kamera C kadrajında: göz hizası, sağ-ön 3/4 (az +32°, el 1°, 24 mm, 24 m). Kamera yükselmeye başlar; ev sağda, metin alanı solda.
- **Metin:** Bu evi iyi yapan ne?  
  *EN:* What makes this house good?
- **Efekt:** Pencere ışıkları röntgen mavisine söner, zeminde temas gölgesi belirir; G≈0,6. Dolly-zoom başlar: 24→27 mm, uzaklık 24→27 m, ev aynı boyda kalır.
- **Etkileşim:** Kaydırma ipucu s0'dan taşınır; çipler henüz gizli.
- **Pazarlama:** Merak sorusu; marka sessiz (logo yok).
- **Üretim:** Blender 4 kare × ≈130 sn (d; G≈0,6 kısmi hayalet: ölç. f000–008 63–171 sn). kamera_pozu başlangıcı s0 C kamerasına bağlanır: hedef (-0,5; -4; 4,6)→(0;0;4,6) (0,5 gün).
- **Telefon:** Lens 30→35 mm; soru üstte tek satır, ev alt %60'ta.
- **Risk:** s0 C kamerası az +32° (C_YON x=+0,62); s1_urun.py bugün az -32° ile başlıyor: ayna kayması, +32°'ye alınmalı.
#### t=33 (0:33) · 726 vh · p=0.03
- **Kare:** Blender s1_urun f004–007 + CSS tarama çizgisi
- **Görsel:** Kamera yükselir (az +33°, el 5°→9°, 0,8×). Beyaz-mavi ince tarama çizgisi evi tepeden zemine süpürür; geçtiği yerde kolon-kiriş iskeleti, pencereler ve blok örgüsü belirginleşir.
- **Efekt:** Röntgen taraması: Blender'da z eşiğiyle G azalır, ekranda 2 px çizgi aynı hızda kayar (meta 'tarama' çapası). Çizgi beyaz-mavi, lime değil.
- **Etkileşim:** Masaüstünde tarama çizgisi imleci hafifçe izler (±20 px); dokunmatikte sabit.
- **Pazarlama:** Şeffaflık: evin içine bakıyoruz; güven duygusu.
- **Üretim:** Blender 4 kare × ≈130 sn (ölç. G kısmi, f004–008 63–171). Tarama bandı: ghost eşiği + meta çapası (0,5 gün).
- **Telefon:** Çizgi tam genişlik; ev ekranın alt yarısında.
#### t=34 (0:34) · 748 vh · p=0.05
- **Kare:** Blender s1_urun f008–011 + HTML çip çubuğu
- **Görsel:** Tarama biter, ev tam röntgen. Kamera el 11°, 0,9×. Blok, lento, U blok, derz, panel türleri soluk lime nabızla sırayla anılır; EGEPOR henüz yok.
- **Metin:** Başlık: İçindekiler.  
  *EN:* Title: What's inside.
- **Efekt:** Her tür 0,15 sn H=3 flaşı (sıra blok, lento, U, harç, panel). Çip çubuğu alttan 24 px yükselip açılır.
- **Etkileşim:** Çip çubuğu belirir: Duvar, Lento, U blok, Tutkal, Panel, EGEPOR; ilk çip nabız atar.
- **Pazarlama:** Ürün ailesi tek bakışta; sistem satışının açılışı.
- **Üretim:** Blender 4 kare × ≈130 sn (ölç. f008 171). Çip çubuğu HTML/CSS + durak vh tablosu (0,5 gün).
- **Telefon:** Çipler altta yatay kaydırılır; aktif çip ortalanır.
#### t=35 (0:35) · 770 vh · p=0.08
- **Kare:** Blender s1_urun f012–015
- **Görsel:** Kamera yörüngeye girer (az +37°, el 16°, 1,0×, 35 mm). İlk durak için duvar blok sıraları alttan üste ön ışıma alır; ev sağ-merkezde yerleşir.
- **Metin:** Cümle: Her durakta bir ürün.  
  *EN:* One product at every stop.
- **Efekt:** Dolly-zoom tamamlanır (35 mm, 34 m). H=2 ön ışıma dalgası alttan üste çıkar.
- **Etkileşim:** Klavyede ← → ile durak atlama; çipler ve oklar ipucu olarak 1 sn yanıp söner.
- **Pazarlama:** Etkileşim vaadi: turu izleyici kendi hızında yönetir.
- **Üretim:** Blender 4 kare × ≈120 sn (ölç. f008–012 105–171). kamera_pozu durak eşikleri saniyeye taşınır, u=(t-32)/38 (0,25 gün).
- **Risk:** FRAMES 96→152 (+%58 kare) + 8 makro + 4 ek: ölçüm tabanında d ≈ +2,5 sa, d+m ≈ +3,4 sa (açık soru 3, süre bütçesi yeniden onay). Cümle t=36'da başlıkla 0,3 sn örtüşür, sonra söner.
#### t=36 (0:36) · 792 vh · p=0.11
- **Kare:** Blender s1_urun f016–019
- **Görsel:** Kamera sağ cepheye süzülür (az +38°→+52°, 0,95×). Ev röntgene geçer; yalnız dolgu duvar blokları gerçek malzemede kalır, kenarları lime parlar.
- **Metin:** Başlık: Duvar blokları  
  *EN:* Title: Wall blocks
- **Efekt:** Blok türü G=0, H=6; karkas, pencere ve döşeme G≈0,9. Lime parıltı dalga olarak alttan üste çıkar.
- **Etkileşim:** Duvar çipi aktif olur (lime halka dolar); çipe tıklamak bu saniyeye atlatır, kareler 4× hızla sarılır.
- **Pazarlama:** Marka ürününün ilk tanışması: lime = bizim ürün.
- **Üretim:** Blender 4 kare × ≈120 sn (ölç. duvar durağı f006–016, ort 123). Durak ağırlık eğrileri s1_urun.DURAK'a taşınır (0,25 gün).
- **Telefon:** Başlık üstte tek satır; ev alt %60'ta, sağ cephe ortalı.
#### t=37 (0:37) · 814 vh · p=0.13
- **Kare:** Blender s1_urun f020–023 + beyaz perde spotu
- **Görsel:** Kamera yaklaşır (az +52°→+62°, 0,5×). Dış duvar blokları lime; iç bölme duvarı röntgenin içinde lime yanar: ürün hem dışta hem içte. Tek bloğa yumuşak spot düşer.
- **Metin:** Cümle: Dış ve iç duvarlar.  
  *EN:* Exterior and interior walls.
- **Efekt:** Spot = canvas üstünde radial-gradient beyaz perde (normal karışım, mix-blend yok). İç duvar H animasyonuyla alttan yanar.
- **Etkileşim:** u_duvar noktası belirir (ekran ~0,68/0,42); dokun: kart (60 × 25 cm, 1–3 mm ince derz).
- **Pazarlama:** Kullanım alanı yapı sahibinin diliyle: nerede, hangi duvar.
- **Üretim:** Blender 4 kare × ≈130 sn (ölç. f012–016 93–173). Yeni: iç bölme duvarı (bina_detay.uret, y=0 aksı, 3 bölme/kat; 0,5 gün).
- **Telefon:** Spot daha geniş, nokta hedefi 44 px.
- **Risk:** Modelde iç duvar yok; eklenmezse 'iç' ifadesi çıkarılır.
#### t=38 (0:38) · 836 vh · p=0.16
- **Kare:** Blender s1_urun f024–027 + SVG ölçü
- **Görsel:** Kamera 0,3×'e yaklaşır (az +62°→+70°). Duvardan iki blok çıkıp önde havada yan yana durur: önce düz, sonra geçmeli blok (geçme oluğu belli). Sırayla spot altına girerler.
- **Metin:** Etiket: Düz · Geçmeli  
  *EN:* Label: Plain · Tongue-and-groove
- **Efekt:** Çeşit spotu: beyaz perde bloktan bloğa kayar; blok yavaş 20° döner, lime kenar. Yüz ölçüsü için SVG 60 × 25 çizgisi çizilir (iki çapa).
- **Rakam · kaynak:** 60 × 25 cm yüz (Ürün föyleri).
- **Etkileşim:** Düz / Geçmeli etiketlerine dokun: kısa kart; seçilen blok spotta 1 sn kalır.
- **Pazarlama:** Seçenek zenginliği: projeye uygun çeşit var hissi.
- **Üretim:** Blender 4 kare × ≈140 sn (ölç. taban 123 × 1,1 çıkan 2 blok). Yeni: çıkan 2 blok animasyonu, kit.gecmeli_blok (0,5 gün); yakın plan gözenek bump testi.
- **Telefon:** Bloklar alt alta değil yan yana kalır, ölçü çizgisi tek ucundan etiketlenir.
- **Risk:** Düz/geçmeli çeşit bilgisi site metninde var, DEVIR teyitli listesinde yok: teyit gerekli. Kalınlık 5–35 cm DEVIR'de Egepor satırında geçiyor: duvar bloğu için teyit gerekli, ekrana yazılmadı.
#### t=39 (0:39) · 858 vh · p=0.18
- **Kare:** Blender s1_urun f028–031
- **Görsel:** Bloklar geri oturur; cephede dikey kesit açılır, 20 cm duvar yakın planda (az +70°, 0,1×, ~3,5 m). İçeriden turuncu ısı okları duvara girer, incelip söner; dışarı yalnız soluk iz çıkar.
- **Metin:** Cümle: Isıyı yavaşlatır, hafif, hızlı örülür.  
  *EN:* Slows heat, light, quick to lay.
- **Efekt:** 3B emissive ok kümesi (turuncu #e8894a, lime değil), duvar içinde boyut ve parlaklık azalır; dış yüzde ince soğuk mavi buğu. Kesit düzlemi boolean ile.
- **Etkileşim:** Metin sütunundaki .eg-ozellik--isi simgesi fareyle yeniden oynar; oklara dokun: 'ısı akışı' etiketi.
- **Pazarlama:** Yapı sahibine fayda: konfor ve enerji; rakam (λ) bilerek s3'e bırakıldı.
- **Üretim:** Blender 4 kare × ≈170 sn (ölç. taban 123 × 1,4 yeni boolean kesit + emissive ok). Ok kümesi stil_r4.sahne_isi'den s1_urun'a taşınır, kesit boolean (1 gün).
- **Telefon:** Kesit penceresi ekran ortasında, oklar dikeyde daha uzun.
- **Risk:** Yön: kışın içeriden dışarı. Ok turuncu; lime yalnız ürün. λ değeri burada verilmez, s3 ile çakışmaz.
#### t=40 (0:40) · 880 vh · p=0.21
- **Kare:** Blender s1_urun f032–035 + HTML rakam kartı
- **Görsel:** Kesit kapanır; kamera geri çekilip sağ cepheyi baştan sona gösterir (az +84°, 0,82×). Tüm dolgu duvarlar lime sınırlı tek yüzey; şaşırtmalı örgü okunur. Lento çubukları sonraki durak için ısınır.
- **Efekt:** Rakam kartı soldan kayar; lento türü H=1 ön ışıma, duvar H yumuşakça 3'e iner.
- **Rakam · kaynak:** 60 × 25 cm yüz · 1–3 mm ince derz (Ürün föyleri)
- **Etkileşim:** Kartta 'Ürün sayfası →' (/urunler/duvar-bloklari/) ve 'Teknik föy' bağlantısı; kart noktadan açılır.
- **Pazarlama:** Güven: kaynaklı rakam; mimara föy, yapı sahibine ürün sayfası (yumuşak CTA).
- **Üretim:** Blender 4 kare × ≈120 sn (ölç. f020–024 107–203). Kartta bağlantı alanı için dil.js NOKTALAR'a 'href' eklenir (0,25 gün).
- **Telefon:** Rakam kartı metnin altında tek satır.
#### t=41 (0:41) · 902 vh · p=0.24
- **Kare:** Blender s1_urun f036–039
- **Görsel:** Kamera arka-sağ cepheye geçer (az +98°→+112°, 0,8×). Duvar röntgene döner; pencere üstlerindeki lento çubukları lime yanar, kat kat alttan üste.
- **Metin:** Başlık: Lentolar  
  *EN:* Title: Lintels
- **Efekt:** Blok G 0→0,92, lento H=6; yanma kat gecikmeli (0,12 sn/kat) dalga. Eski vurgu bir saniyede söner.
- **Etkileşim:** Lento çipi aktif; Duvar çipinde tamam işareti kalır.
- **Pazarlama:** İkinci ürün: duvar ailesinin devamı hissi.
- **Üretim:** Blender 4 kare × ≈130 sn (ölç. lento durağı f018–028, ort 127). Kat gecikmeli H eğrisi (0,25 gün).
#### t=42 (0:42) · 924 vh · p=0.26
- **Kare:** Blender s1_urun f040–043 + SVG iki çapa
- **Görsel:** Kamera bir pencereye iner (az +112°→+120°, 0,35×). Lento pencerenin hemen üstünde, iki yanda duvara oturur; pencere boşluğu ince beyaz kontur, lento lime.
- **Metin:** Cümle: Açıklıkların üstünde köprü kurar.  
  *EN:* Bridges the openings.
- **Efekt:** Pencere kenarı beyaz kontur çizilir; lento nabız atar. İki yan oturma noktası SVG küçük halkalarla işaretlenir.
- **Etkileşim:** u_lento noktası lentoda; dokun: kart (açıklık üstü, 4,50 m'ye kadar).
- **Pazarlama:** Nerede kullanılır: açık ve anlaşılır; yapı sahibi için.
- **Üretim:** Blender 4 kare × ≈130 sn (ölç. f024–028 81–177). Meta: u_lento_a/u_lento_b çoklu çapa (kit.project, 0,5 gün).
- **Telefon:** Pencere ekranı doldurur; çapa halkaları 44 px.
#### t=43 (0:43) · 946 vh · p=0.29
- **Kare:** Blender s1_urun f044–047 + SVG ölçü ve yük okları
- **Görsel:** Kamera 0,2×'e iner (az +120°→+128°). Pencere boşluğunun iki ucundan ölçü çizgisi çizilir; üstten küçük beyaz yük okları iner, lentoda durur ve yük iki yana oturma noktalarına yayılır.
- **Efekt:** Ölçü çizgisi stroke-dash ile çizilir (beyaz); yük okları 3B, lento altında kesilir. İki yan nokta nabız atar.
- **Etkileşim:** Ölçü çizgisine fare gelince okların yük yayılımı bir tur daha oynar (CSS tetikli).
- **Pazarlama:** Öğretici an: lento neden var, tek bakışta anlaşılır.
- **Üretim:** Blender 4 kare × ≈150 sn (ölç. f026–030 81–177 + yük oku kümesi). Yeni: yük oku kümesi + lento oturma vurgusu (0,5 gün).
- **Telefon:** Ölçü yazısı çizginin üstüne, tek satır.
- **Risk:** Mevcut CSS oz-olcu çizgisi lime-hi: beyaz/açık griye çevrilmeli, lime yalnız ürüne. Yük aktarımı ifadesi mühendis gözüyle teyit gerekli.
#### t=44 (0:44) · 968 vh · p=0.32
- **Kare:** Blender s1_urun f048–051
- **Görsel:** Kamera lento ile bitişik duvar bloğuna yaklaşır (0,12×, ~4 m, az +128°→+134°). Lento duvardan 10 cm dışarı kayar; ikisinin gözenekli dokusu aynı. Sonra lento ve duvar birlikte lime yanar.
- **Metin:** Cümle: Duvarla aynı malzeme.  
  *EN:* Same material as the wall.
- **Efekt:** Makro doku (kit.aac_material bump) iki yüzeyde aynı; lime nabız senkron. Hafif odak yumuşaması (arka plan beyaz zaten).
- **Etkileşim:** Dokunduğun yüzey kısa süre parlar: lento mu duvar mı etiketi çıkar.
- **Pazarlama:** Tek malzeme bütünlüğü: sistem güveni.
- **Üretim:** Blender 4 kare × ≈250 sn (yakın plan; ölç. f030–036 113–384 sn, makro bump + odak yumuşaması). Lento kayma animasyonu (0,25 gün).
- **Risk:** Yakın planda blok kenar bevel ve harç boxları kontrol edilmeli.
#### t=45 (0:45) · 990 vh · p=0.34
- **Kare:** Blender s1_urun f052–055 + SVG kapasite çubuğu
- **Görsel:** Lento yerine oturur. Pencerenin yanında kapasite çubuğu 0'dan 4,50 m'ye uzar; pencere boşluğu bunun küçük bir parçası kalır. Kamera geri çekilir ve çatıya yükselir (az +140°, el 18°→30°).
- **Efekt:** Sayaç 0→4,50 m (600 ms, JS); çubuk beyaz, uç işareti lime değil. Kamera yükselirken lento H söner.
- **Rakam · kaynak:** 4,50 m'ye kadar açıklık (Ürün föyleri)
- **Etkileşim:** Lento çipine yeniden tıklamak durağı baştan oynatır; sayaç yeniden sayar.
- **Pazarlama:** Mimara somut kapasite; ürün sayfası bağlantısı kartta.
- **Üretim:** Blender 4 kare × ≈170 sn (ölç. f032–036 156–384, kamera çatıya yükselir). Sayaç ve çubuk HTML/SVG (0,25 gün).
- **Telefon:** Kapasite çubuğu yatay, ekran genişliğinin %70'i.
- **Risk:** Modeldeki pencere 1,5 m; çubuk 'kapasite' olarak etiketlenmeli, bu evin açıklığı gibi okunmamalı.
#### t=46 (0:46) · 1012 vh · p=0.37
- **Kare:** Blender s1_urun f056–059
- **Görsel:** Kamera arka cephede çatıya yükselir (az +150°→+165°, el 30°→52°, 0,5×→0,12×). Parapetin üst sırası lime yanar, ev geri kalanı röntgen.
- **Metin:** Başlık: U bloklar  
  *EN:* Title: U-blocks
- **Efekt:** U blok kabuğu H=6; donatı ve hatıl betonu H=0. Yükselişte yumuşak ease-in-out, hafif bloom.
- **Etkileşim:** U blok çipi aktif; kamera yükselişi sırasında çatı çizgisine dokunma ipucu.
- **Pazarlama:** Üçüncü ürün: daha az bilinen ürün öne çıkar, merak.
- **Üretim:** Blender 4 kare × ≈250 sn (ölç. U blok durağı f030–040 63–384, ort 175; çatı yakın plan en ağır durak). Kamera eğrisi DURAK_HEDEF'e bağlanır (var).
- **Telefon:** Çatı üstten kadraj, parapet ekran ortasında.
- **Risk:** s1_urun'da donatı ve hatıl'a da H uygulanıyor: donatı yeşil olamaz, H=0'a çekilmeli.
#### t=47 (0:47) · 1034 vh · p=0.39
- **Kare:** Blender s1_urun f060–063 + SVG kullanım pinleri
- **Görsel:** Parapetteki üç U blok havaya kalkar (açık kesit, kanal yukarı bakıyor; az +165°→+178°). Çevrede kullanım pinleri çizilir: çatı hizası, yüksek duvar ara hatılı, gizli baca ve iniş borusu.
- **Metin:** Cümle: Hatıl için hazır kalıp.  
  *EN:* Ready-made formwork for bond beams.
- **Efekt:** Kalk eğrisi s1_urun.kalk (var), 4 sn'ye göre yeniden zamanlanır. Pinler 0,3 sn arayla belirir (beyaz çizgi, lime nokta yok).
- **Etkileşim:** 3 kullanım pinine dokun: evde ilgili yer 1 sn spotlanır, kartta açıklama.
- **Pazarlama:** Kullanım alanı zenginliği: ürünün çok işe yaradığını gösterir.
- **Üretim:** Blender 4 kare × ≈220 sn (ölç. f032–036 156–384; havadaki 3 U blok). Pin çapaları meta'ya (u_ublok_cati, _ara, _baca; 0,5 gün).
- **Telefon:** Pinler iki ile sınırlı, üçüncü kartta.
- **Risk:** Ara hatıl ve baca pinleri yalnız pin; modelde karşılığı yok, çizgi cepheye şematik biner.
#### t=48 (0:48) · 1056 vh · p=0.42
- **Kare:** Blender s1_urun f064–067 + SVG donatı etiketi
- **Görsel:** Kamera havadaki U bloklara iner (az +178°, el 56°, ~3 m). U kesit okunur: taban ve iki yan cidar; kanalda dört koyu donatı çubuğu uzanır.
- **Efekt:** Donatı koyu metalik (lime değil); kabuk lime kenar. Spot altında, geri kalan hafif beyaz perde.
- **Etkileşim:** Donatıya dokun: 'Donatı' etiketi ve kart başlığı (çelik; yeşil değil).
- **Pazarlama:** Öğretici: içi dolu bir kalıp olarak U blok.
- **Üretim:** Blender 4 kare × ≈250 sn (ölç. f032 384; kamera ~3 m, metalik donatı). Çelik malzeme koyu kalır (var).
- **Telefon:** Kamera biraz daha uzak (3,5 m), kanal yatay okunur.
#### t=49 (0:49) · 1078 vh · p=0.45
- **Kare:** Blender s1_urun f068–071 + SVG kalıp simgesi
- **Görsel:** Gri beton kanala aşağıdan yukarı dolar (%30→%90). Köşede ince ahşap kalıp çerçevesi belirir ve üzeri çizilerek silinir: U blok kalıp görevini üstlenir.
- **Metin:** Cümle: Beton dökülür, ahşap kalıp gerekmez.  
  *EN:* Pour concrete: no timber formwork.
- **Efekt:** hatil_ob z-ölçek dolumu (var), 4 kare ile yumuşatılır. Kalıp simgesi SVG ince çerçeve + çapraz çizgi (gri, kırmızı değil).
- **Etkileşim:** Dolum sırasında kaydırmayı geri alınca beton boşalır: kare tabanlı oynatıcı ters oynar (otomatik).
- **Pazarlama:** Şantiye avantajı: kalıp işçiliği ve süre tasarrufu hissi (rakamsız).
- **Üretim:** Blender 4 kare × ≈200 sn (ölç. f036–044 63–292; dolum animasyonu). Dolum eğrisi s1_urun.dol 4 sn'e göre ayarlanır (0,25 gün).
- **Risk:** Süre tasarrufu iddiası rakamsız kalmalı; rakam teyit gerekli.
#### t=50 (0:50) · 1100 vh · p=0.47
- **Kare:** Blender s1_urun f072–075 + HTML rakam kartı
- **Görsel:** Dolum biter; U bloklar parapete geri oturur, hatıl betonu blokların içinde gizlenir. Kamera geri açılır (az +178°→+198°, el 56°→40°) ve evin sol-arka köşesine döner.
- **Efekt:** Lime kenar yumuşak söner, rakam kartı soldan girer. Parapet çizgisi bir kez parlayıp sönerek 'tamam' hissi verir.
- **Rakam · kaynak:** 60 × 25 cm, 20–25 cm kalınlık; λ 0,16 W/mK kuru (G4/06) (Ürün föyleri, U Bloklar sayfası)
- **Etkileşim:** u_ublok noktası parapette; kart: hatıl kalıbı, gizli baca, iniş borusu.
- **Pazarlama:** Teknik güven: G4/06 sınıfı ve λ açık yazılır; mimar için föy bağlantısı.
- **Üretim:** Blender 4 kare × ≈150 sn (ölç. f044–048 202–292). Kart metni dil.js'te var, bağlantı eklenir.
- **Telefon:** Rakam kartı iki satıra bölünür.
#### t=51 (0:51) · 1122 vh · p=0.5
- **Kare:** Blender s1_urun f076–079
- **Görsel:** Kamera sol-arka cepheye alçalır (az +205°, el 30°→20°, 0,6×). Bloklar neredeyse saydam; blokların arasındaki harç ağı lime çizgiler olarak belirir: önce yatay, sonra düşey derzler.
- **Metin:** Başlık: Gazbeton tutkalı  
  *EN:* Title: AAC adhesive
- **Efekt:** Harç emissive lime, blok G=0,92. Çizgiler yapım sırasına göre (zaman) alttan üste çizilir. Çizim 0,8 sn'de biter.
- **Etkileşim:** Tutkal çipi aktif; derz ağı ekranda gezinen imleçle hafif ışıldar (CSS, hotspot yakınında).
- **Pazarlama:** Dördüncü ürün: duvarın görünmeyen kahramanı; lime = tutkalımız.
- **Üretim:** Blender 4 kare × ≈190 sn (ölç. tutkal durağı f044–052, ort 187). Harç emissive eğrisi (var: ayarla('harc')), lime kenar yerine dolu çizgi (0,25 gün).
#### t=52 (0:52) · 1144 vh · p=0.53
- **Kare:** Blender s1_urun f080–083
- **Görsel:** Ön planda tutkal torbası belirir (lime şeritli beyaz ambalaj, yazısız) ve yavaş döner; arkada derz ağı nabız atar (az +205°→+218°, 0,4×).
- **Metin:** Cümle: İnce derz harcı.  
  *EN:* Thin-joint mortar.
- **Efekt:** Torba spotta, çevresi beyaz perde. Torba stil_r4.sahne_urunler modelinden; lime bant. 3B yazı yok.
- **Etkileşim:** Torbaya dokun: kart 'Gazbeton tutkalı' (1–3 mm, ürün sayfası bağlantısı).
- **Pazarlama:** Ambalaj lime: marka tanınırlığı; sahada ürünün kendisi.
- **Üretim:** Blender 4 kare × ≈170 sn (ölç. f048 202, f052 67; torba nesnesi). Torba bir Blender nesnesi olarak s1_urun'a eklenir (0,5 gün).
- **Telefon:** Torba ekran alt-ortada, küçük.
- **Risk:** Gerçek ambalaj rengi/şekli teyit gerekli; yazı ve logo 3B içinde yok, etiket HTML.
#### t=53 (0:53) · 1166 vh · p=0.55
- **Kare:** 2B halka geçiş: altta s1_urun f084–087, içinde makro derz (stil_r5.sahne_derz) m000–003
- **Görsel:** Bir derz kesişiminden lime halka açılır ve ekranı doldurur; makro sahne: iki blok arasında 3 mm ince tutkal hattı, yan yanında ölçü köşeleri.
- **Metin:** Etiket: 1–3 mm  
  *EN:* Label: 1–3 mm
- **Efekt:** Daire maskesi (clip-path, mix-blend yok) hotspot'tan büyür; makro kamera 0,6 m. Derz hattı lime, bloklar gerçek doku.
- **Rakam · kaynak:** 1–3 mm derz (Ürün föyleri)
- **Etkileşim:** Halka büyürken dokunma devam eder; kaydırma yönü tersine çevrilirse halka kapanır.
- **Pazarlama:** Vurucu detay: ince derz, tek bakışta.
- **Üretim:** Altta ana f084–087: 4 kare × ≈130 sn (ölç. f052–056 67–191). Makro sahnenin tamamı m000–007: 8 kare × ≈80 sn (d; ölçülmedi, varsayım 60–100 sn: saydamsız, 2 blok + derz; ön testle doğrulanacak; t=54 satırında ayrıca sayılmaz). Halka geçişi JS 2B. sahne_derz'i s1 lime diline taşı (1 gün).
- **Telefon:** Halka ekran genişliğini doldurur; makro kadraj dikey.
- **Risk:** Mevcut sahne_derz lime lazer çizgisi kullanıyor: lazer beyaza çevrilmeli (lime yalnız tutkal hattı). Makro ek sahne maliyeti +8 kare ≈ +11 dk (80 sn/kare varsayım, ölçülmedi).
#### t=54 (0:54) · 1188 vh · p=0.58
- **Kare:** Blender makro derz m004–007 (tam ekran; ana sahne f088–091 render gerekmez)
- **Görsel:** Makro sahnede yeni blok indirilip lime tutkal şeridine oturur; ince beyaz düzlük çizgisi sıra boyunca kayar ve hiç sapmaz.
- **Metin:** Cümle: Duvar düz ve homojen olur.  
  *EN:* The wall stays flat and uniform.
- **Efekt:** Blok yerleşme hafif bounce; düzlük çizgisi beyaz (lazer lime değil). Derz kenarında taşma yok.
- **Etkileşim:** Çizgiye dokun: 'düzlük' etiketi; imleç çizgiyle birlikte kayar (masaüstü).
- **Pazarlama:** Kalite hissi: 'dümdüz' duvar, sıva ve işçilik tasarrufu çağrışımı (rakamsız).
- **Üretim:** Makro m004–007: 4 kare × ≈80 sn (varsayım; t=53'teki 8 karelik makro toplamına dahil, çift sayılmaz); ana f088–091 render yok. Düzlük çizgisi 3B ince kutu (0,25 gün).
- **Risk:** Sıva tasarrufu iddiası yazılmaz; yalnız görsel çağrışım, rakam yok.
#### t=55 (0:55) · 1210 vh · p=0.61
- **Kare:** 2B halka kapanış + Blender s1_urun f092–095
- **Görsel:** Halka kapanır, kamera sol cepheden panel durağına döner (az +255°, el 10°→25°, 0,7×). Duvar boyunca bütün derz ağı lime devre gibi tek seferde yanıp söner.
- **Efekt:** Lime derz ağı tüm yüzeyde 0,4 sn'lik flaş; sonra G=1'e söner (duvar hayalete döner).
- **Rakam · kaynak:** 1–3 mm derz kalınlığı (Ürün föyleri)
- **Etkileşim:** u_tutkal noktası derz kesişiminde; kart: ince derz harcı.
- **Pazarlama:** Rakam kartı güven; 'Ürün sayfası →' bağlantısı.
- **Üretim:** Blender 4 kare × ≈150 sn (ölç. f056–060 110–191). Halka kapanış JS.
#### t=56 (0:56) · 1232 vh · p=0.63
- **Kare:** Blender s1_urun f096–099
- **Görsel:** Kamera sol-ön tarafta tepeye çıkar (az +262°→+275°, el 35°→55°, 0,95×). Çatıdaki 60 cm'lik panel şeritleri soldan sağa dalga halinde lime yanar; ev röntgen.
- **Metin:** Başlık: Paneller  
  *EN:* Title: Panels
- **Efekt:** Panel türü H=6, şerit başına 0,05 sn gecikme (dalga). Duvar ve karkas G=0,9.
- **Etkileşim:** Panel çipi aktif; çatı yüzeyi dokunulur hissi (imleç el simgesi). Soru 1 çipi köşede belirir (bilgi_yarismasi): 'Bloklar neyle birleşir?' + 3 şık, tek dokunuş, zorunlu değil; tutkal kartı açıksa soru bekler (kart cevabı verir).
- **Pazarlama:** Beşinci ürün: çatıya geçiş, evin 'üstü' kapanıyor.
- **Üretim:** Blender 4 kare × ≈110 sn (ölç. panel durağı f060–064 66–110). Şerit gecikmeli H eğrisi (0,25 gün).
- **Telefon:** Çatı üstten bakışta ekran ortasında.
#### t=57 (0:57) · 1254 vh · p=0.66
- **Kare:** Blender s1_urun f100–103 + SVG çeşit çipleri
- **Görsel:** Şeritler tek tek yukarı kalkıp iner (piyano tuşu gibi). Köşede çeşit çipleri: Çatı, Döşeme, Duvar; çatı panelleri evde, döşeme ve duvar küçük kesit ikonuyla spotlanır.
- **Metin:** Cümle: Çatı, döşeme ve duvarda.  
  *EN:* For roofs, floors and walls.
- **Efekt:** Şerit kalkışı ±3 cm, sıralı. Çip spotu beyaz perde kayar; ikonlar SVG (filtre yok).
- **Etkileşim:** Çeşit çiplerine dokun: ilgili ikon büyür, kart kısa kullanım açıklaması verir. Soru 1 çipi köşede sürer; cevap sonrası 'Doğru.' + kaynak (Ürün föyleri) ya da doğrusu + nedeni, ardından çip söner; soru açıkken yalnız o çip nabız atar.
- **Pazarlama:** Çeşit zenginliği: panel yalnız çatı değil, üç kullanım.
- **Üretim:** Blender 4 kare × ≈110 sn (ölç. f064 66; şerit hareketi). Piyano animasyonu (0,25 gün); 2 SVG kesit ikonu (0,25 gün).
- **Telefon:** Çipler yatay tek sıra.
- **Risk:** Döşeme ve duvar paneli ifadesi site metninde var, DEVIR teyitli listesinde yok: teyit gerekli.
#### t=58 (0:58) · 1276 vh · p=0.68
- **Kare:** Blender s1_urun f104–107 + SVG ölçü
- **Görsel:** Kamera panelin tam üstüne geçer (az +290°, el 65°, 0,5×). Kiriş kiriş ölçü çizgisi çizilir; yanında kapasite çubuğu 6 m'ye uzar. Paneller y=0 kirişinde iki açıklığa bölünmüş.
- **Efekt:** Ölçü çizgisi stroke-dash (beyaz), sayaç 0→6 m. Panel kenarlarında lime ince kenar parlar.
- **Rakam · kaynak:** 6 m'ye kadar açıklık, döşeme / çatı paneli (Ürün föyleri)
- **Etkileşim:** Sayaç dokunuşla yeniden sayar; ölçü çapaları panel kenarlarına bağlıdır.
- **Pazarlama:** Mimara somut kapasite: tek parça ile geniş açıklık.
- **Üretim:** Blender 4 kare × ≈140 sn (ölç. f064–068 66–198). Yeni: panelleri 4,5 m açıklığa böl (bina_detay.uret, 0,25 gün).
- **Telefon:** Çubuk yatay, kadraj dikey olduğundan ölçü çizgisi diyagonal olmaz.
- **Risk:** Modelde panel tek parça 8,8 m (>6 m): iki açıklığa bölünmeli, aksi halde ürünün 6 m sınırıyla çelişir.
#### t=59 (0:59) · 1298 vh · p=0.71
- **Kare:** Blender s1_urun f108–111 + SVG ağırlık oku ve zemin dalgası
- **Görsel:** Kamera geri çekilir (az +300°, el 45°, 1,0×). Evin yanında kalın ağırlık oku ince okla yer değiştirir; zeminde üç soluk sismik dalga halkası yayılır. Panel şeritleri hafifçe yüzer.
- **Metin:** Cümle: Hafif bina, düşük deprem yükü.  
  *EN:* Lighter building, lower seismic load.
- **Efekt:** Ok SVG (soğuk gri, lime değil); halkalar SVG ellips, 3 halka, filtre yok. Şerit yüzmesi ±3 cm sinüs.
- **Etkileşim:** Zemin halkalarına dokun: halka yeniden yayılır; kart 'ODTÜ çalışması' notu.
- **Pazarlama:** Güvenlik duygusu: deprem bölgesinde evin hafifliği; duygusal vurgu.
- **Üretim:** Blender 4 kare × ≈160 sn (ölç. f068 198). Halka ve ok 2B SVG, ekstra render yok (0,25 gün).
- **Telefon:** Halkalar ev altında yarım elips, ok sağ kenarda.
- **Risk:** Doğrudan 'deprem güvenli' denmez; yalnız yük azalması anlatılır.
#### t=60 (1:00) · 1320 vh · p=0.74
- **Kare:** Blender s1_urun f112–115 + SVG kütle çubuğu
- **Görsel:** Kütle çubuğu 100'den 83'e iner, alt yazısı 'ODTÜ, 8 katlı örnek bina'. Kamera sol-ön cepheye alçalır (az +312°, el 55°→30°) ve EGEPOR durağına yönelir.
- **Efekt:** Çubuk SVG, sayaç 100→83 (700 ms). Panel lime söner; kolon ve kirişler sonraki durak için gri hayalet olarak belirir.
- **Rakam · kaynak:** −%17 yapı kütlesi (ODTÜ çalışması, 8 katlı örnek bina hesabı)
- **Etkileşim:** Çubuğa gelince ODTÜ çalışma kartı (u_panel): kapsam ve 8 katlı örnek bina notu.
- **Pazarlama:** Üçüncü taraf kanıt: ODTÜ kaynağı güveni artırır.
- **Üretim:** Blender 4 kare × ≈110 sn (ölç. f072 104). Kütle çubuğu HTML/SVG (0,25 gün).
- **Telefon:** Çubuk metnin altında, kaynak iki satır.
- **Risk:** −%17 değeri 8 katlı örnek bina hesabı; bu ev 3 katlı, etikette belirtilmeli. Kapsamı (yalnız panel mi, tüm gazbeton sistem mi) teyit gerekli.
#### t=61 (1:01) · 1342 vh · p=0.76
- **Kare:** Blender s1_urun f116–119
- **Görsel:** Kamera ön-sol cepheye iner (az +318°, el 16°, 0,85×). EGEPOR henüz yok: çıplak beton kolon ve kirişler gri hayalet; üzerlerinde turuncu ısı sızıntısı parlaması termal kamera gibi çerçeveyi belli eder.
- **Metin:** Başlık: EGEPOR  
  *EN:* Title: EGEPOR
- **Efekt:** Kolon/kiriş malzemesine turuncu emission (yeni H_isi); duvarlar çok soluk. Başlık kenarında SVG ince lime çizgi (EGEPOR ürün vurgusu).
- **Etkileşim:** EGEPOR çipi aktif; altı çipin hepsi artık doludur.
- **Pazarlama:** Altıncı ürün: yalıtım hikâyesi, enerji ve konfor vurgusu.
- **Üretim:** Blender 4 kare × ≈110 sn (ölç. f072 104 × 1,1 termal emission). Termal emission malzeme katmanı (0,5 gün).
- **Risk:** Egepor levhalar bu saniyede gizli (ep_ob.hide_render): lime başlık vurgusu SVG ile verilir.
#### t=62 (1:02) · 1364 vh · p=0.79
- **Kare:** Blender s1_urun f120–123
- **Görsel:** Beyaz, lime kenarlı 5 cm levhalar dışarıdan kayarak kolonlara ve kirişlere oturur (kolon kolon, soldan sağa; az +330°, 0,55×). Oturduğu yerde turuncu parlama söner, soğuk ton kalır.
- **Metin:** Cümle: Kolon ve kirişe kaplama.  
  *EN:* Cladding for columns and beams.
- **Efekt:** ep_ob tek nesne: kolon başına ayrı gecikme için parçalanır. Temas anında lime kenar flaşı, hafif bounce.
- **Etkileşim:** Levhalara dokun: u_egepor kartı (kolon ve kiriş kaplaması).
- **Pazarlama:** Nerede kullanılır: kolon ve kiriş, müşteri onaylı kullanım.
- **Üretim:** Blender 4 kare × ≈90 sn (ölç. f076 63 × 1,4 parça başına animasyon). Yeni: egepor_parcalari parça başına animasyon (0,5 gün).
#### t=63 (1:03) · 1386 vh · p=0.82
- **Kare:** Blender s1_urun f124–127 (önce/sonra çift render) + SVG süpürme
- **Görsel:** Önce/sonra: dikey bölme çizgisi cepheyi süpürür. Solda çıplak betonun turuncu sızıntısı, sağda EGEPOR'lu kolon-kiriş serin. Kamera kolon-kiriş birleşimine yaklaşır (az +342°, 0,3×).
- **Metin:** Etiket: Isı sızıntısı  
  *EN:* Label: Heat leak
- **Efekt:** İki render (ısı açık/kapalı), 2B wipe (clip-path, mix-blend yok). Bölme çizgisi beyaz.
- **Etkileşim:** Bölme çizgisi sürüklenebilir (masaüstü) / dokunmatikte kaydırmayla ilerler; önce/sonra karşılaştırması.
- **Pazarlama:** Öğretici kanıt: görerek anlaşılan yalıtım farkı.
- **Üretim:** Blender 4 kare × 2 durum × ≈90 sn = 8 render (ölç. f080 65 sn × 1,4 termal emission). Süpürme JS (0,5 gün).
- **Telefon:** Bölme çizgisi yatay (üst/alt), sürükleme dikey.
- **Risk:** Ürün sayfasında 'ısı köprüsü' ifadesi yok; etikette 'ısı sızıntısı', ısı köprüsü yorumu teyit gerekli.
#### t=64 (1:04) · 1408 vh · p=0.84
- **Kare:** Blender s1_urun f128–131 + SVG kullanım çipleri
- **Görsel:** Kamera geri çekilir (az +356°, 0,7×). Kullanım çipleri sırayla yanar: dış cephe (cephe lime), otopark tavanı, bodrum tavanı (iki küçük SVG kesit ikonu).
- **Metin:** Cümle: Cephede, otopark ve bodrum tavanında da.  
  *EN:* Also on facades, car park and basement ceilings.
- **Efekt:** Çip spotu beyaz perde kayar; ikonlar SVG. Cephe levhaları 0,4 sn H=6.
- **Etkileşim:** Çiplere dokun: ikon büyür, kart kısa kullanım açıklaması verir.
- **Pazarlama:** Kullanım alanı genişliği: yalnız kolon değil, cephe ve tavan; teklif nedeni.
- **Üretim:** Blender 4 kare × ≈100 sn (ölç. f080–084 65–92). 2 yeni SVG kesit ikonu (0,25 gün).
- **Telefon:** Çipler iki satır, ikonlar küçük.
#### t=65 (1:05) · 1430 vh · p=0.87
- **Kare:** Blender s1_urun f132–135 + HTML rakam kartı
- **Görsel:** Rakamlar belirir. Altı ürünün lime kenarı sırayla (blok, lento, U, derz, panel, EGEPOR) kısa parlayıp söner. Kamera ön cepheye oturur (az +368°, el 14°, 0,9×).
- **Efekt:** Çip çubuğunda koro: altı çip sırayla yanar, evde ilgili tür 0,15 sn H=4. Rakam kartı soldan kayar.
- **Rakam · kaynak:** λ 0,051–0,062 W/mK (kuru) · 150–200 kg/m³ (Ürün föyleri, EGEPOR sayfası)
- **Etkileşim:** u_egepor noktası; kart: kolon-kiriş kaplaması, dış cephe, otopark ve bodrum tavanı, λ.
- **Pazarlama:** Teknik güven: λ ve yoğunluk açık, kaynaklı; 'Teknik föy' bağlantısı.
- **Üretim:** Blender 4 kare × ≈110 sn (ölç. f084 92). Koro için çip animasyonu (0,25 gün).
- **Telefon:** Rakam kartı iki satır.
#### t=66 (1:06) · 1452 vh · p=0.89
- **Kare:** Blender s1_urun f136–139
- **Görsel:** Tüm ürünler aynı anda lime: ev altı ürünün birleşimi olarak alttan üste dalgayla parlar. Kamera ön cephede sabitlenir (az +20°, el 15°, 0,9×); çip çubuğunda altı çip birden dolu.
- **Metin:** Cümle: Duvardan çatıya tek mineral malzeme.  
  *EN:* One mineral material from wall to roof.
- **Efekt:** Tüm türler H=6, G=0,4; dalga z eşiğiyle. Evin etrafına hafif beyaz bloom.
- **Etkileşim:** Çipler 'durağa dön' için tıklanabilir; kaydırmaya devam ipucu.
- **Pazarlama:** Sistem iddiası: altı ürün, tek adres, tek malzeme dili.
- **Üretim:** Blender 4 kare × ≈190 sn (ölç. f084–088 92–290; tüm türler eşzamanlı H). Koro eğrisi (0,25 gün).
- **Risk:** Mineral ifadesi mevcut site metninden; kapsam EGEPOR ve beton hatılı da içeriyor: ifade teyit gerekli.
#### t=67 (1:07) · 1474 vh · p=0.92
- **Kare:** Blender s1_urun f140–143
- **Görsel:** Kamera ön cephedeki odak bloğa dalar (zemin kat, x≈-3; 0,9×→0,2×). Evin geri kalanı hızla saydamlaşır; bloğun lime halesi büyür, ev ekrandan kayar.
- **Efekt:** Dalış: loc lerp (kit.smoother u 0,895→1), V 0→0,6, kaydir 1→0.5. Lime halesi H=6'dan 8'e.
- **Etkileşim:** u_blok noktası belirir ('Tek blok'); dokun: kart ve kaydırma ipucu.
- **Pazarlama:** Merak köprüsü: tek bloğa odak.
- **Üretim:** Blender 4 kare × ≈300 sn (dalış f140–143, V≈0,54–0,84 kısmi saydam (mevcut dal eğrisiyle); ölç. f088 V≈0,52 = 290 sn; yakın plan, DOF kapalı). Dalış eğrisi 4 sn'ye göre (0,25 gün).
- **Telefon:** Dalış ekran ortasına, blok dikey kadrajda ortalı.
- **Risk:** Render: V ara değerli (≈0,54–0,84) karelerde her ışın ve gölge ışını onlarca saydam yüzey geçer: ≥300 sn. V kilidi/hide_render ve transparent_max_bounces 12 olmadan seri bu kareleri içermez (yeni_isler: RENDER HIZLANDIRMA).
#### t=68 (1:08) · 1496 vh · p=0.95
- **Kare:** Blender s1_urun f144–147
- **Görsel:** Blok duvardan 45 cm öne kayar; arkasında kalan boşluk beyaza erir. Ev tamamen saydam; blok lime kenarlı, yanında yumuşak temas gölgesi (kamera ~2,4 m).
- **Metin:** Cümle: Peki bu blok nasıl doğuyor?  
  *EN:* So how is this block born?
- **Efekt:** odak_ob y -0,45 (var); V→1; lime kenar tepe noktada. Zeminde beyaz stüdyo gölgesi.
- **Etkileşim:** Blok halesine dokun: kartta 'Kaydırın' ipucu; kaydırma sürdürülür.
- **Pazarlama:** Anlatıyı sürükleyen soru; üretim hikâyesine bağlar.
- **Üretim:** Blender 4 kare: f144–146 ≈300–1300 sn (merkez 600; V=0,91–0,9965 kilitsiz; ölç. f092 V=0,9991 = 1318 sn), f147 V=1 ≈220 sn; düzeltme sonrası hedef ≤120 sn (varsayım). Zemin gölgesi yeni (0,25 gün).
- **Risk:** Render: f144–146 V=0,91–0,9965 (kilitsiz). Ölçüm: f092 (V=0,9991) 1318 sn ve karede koyu leke artefaktı (%0,09 opak kalıntı ışın, adaptif örnekleme yakınsamaz). V≥0,98 → hide_render + V=1'e kilit; yoksa f140–147 tek başına ≈0,6–1,5 sa.
#### t=69 (1:09) · 1518 vh · p=0.97
- **Kare:** Blender s1_urun f148–151 (f151 = s2 f000)
- **Görsel:** Beyaz fonda tek blok, ekran merkezinde, hafif 3/4 sağ-ön, ekran genişliğinin ~%40'ı. Lime kenar söner, blok doğal gazbeton rengine döner; kamera yavaşça durur.
- **Efekt:** H→0, kaydir 0, zemin gölgesi ve bloom s2'ye birebir. Son kare s2 ilk karesiyle çapraz erimeye hazır.
- **Etkileşim:** Kaydırma ipucu yeniden belirir (ok).
- **Pazarlama:** Temiz, odaklı kare: sonraki bölüm üretim güveni.
- **Üretim:** Blender 4 kare × ≈220 sn (V=1 sabit; ölç. f095 = 218 sn; V kilidi + hide_render sonrası ≈70–120 sn varsayım, ön testle doğrulanacak). s2 ilk karesi ile poz ve ölçek karşılaştırması (altın kare).
- **Telefon:** Blok kadrajın üst-orta bölümünde, ekranın %55'i.
- **Risk:** s2 planlayıcısı ile blok pozu, ölçeği, zemin gölgesi ve kamera eşleşmeli; ayrı planlandığı için teyit. Render: V=1 karelerinde bile ölç. f095 = 218 sn; ev nesneleri hide_render ile çıkarılınca tek blok + zemin yeterli.

**Geçiş ve üretim notu (s1).** Satırlar t=32..69 (38 satır; t=70 s2'nin ilk saniyesi). p = (t-32)/38 (satır başı). Kare: 4 kare/sn, 152 kare, f=(t-32)*4..+3, u=f/151; telefon her 2. kare. Sözlük: G=röntgen/hayalet karışımı, V=saydamlaşıp kaybolma, H=lime kenar ışıltısı (s1_urun.gecis_malzeme). Metin düzeni: her durakta başlık (durak boyu), cümle A (2. ve 3. sn), cümle B (4. ve 5. sn); metin yalnız belirdiği saniyeye yazıldı, sonraki saniyede '' kalır ve ekranda durur (en çok 1 başlık + 1 cümle, etiketler en çok 2 kelime). Durak sınırları: giriş 32-35, duvar 36-40, lento 41-45, U blok 46-50, tutkal 51-55, panel 56-60, EGEPOR 61-65, çıkış 66-69 (geçiş 67-69). Kamera yörüngesi az +32° (s0 C kamerası) -> +380°, tur sonunda ön cephede biter; duraklar: duvar sağ cephe, lento arka-sağ, U blok arka çatı, tutkal sol-arka, panel sol-ön çatı, EGEPOR ön cephe. s0->s1: s0 son karesi (stüdyoda hayalet ev, C kadrajı) f000 ile birebir; s0'ın çıkış satırları pencere ışıklarını söndürmüyorsa t=32 bunu tamamlar. s1->s2: f151 = beyaz fonda tek blok, ekran merkezinde, hafif 3/4 sağ-ön, blok ekran genişliğinin ~%40'ı; s2 ilk karesiyle poz ve ölçek eşleşmeli. RENDER SÜRESİ (ölçülü; eski '~40 sn' varsayımı terk edildi): render/s1.log (eski 96 kareli seri, d 1600×900, 28 spp, adaptif eşik 0,02, 4 çekirdek %391), 35 karede medyan ≈109 sn, ort ≈140 sn (f092 aykırı hariç; dahil ≈175), min 63, max 1318 (f092, u≈0,968, V=0,9991: dalış). Satırlardaki sn değerleri: ilgili durağın ölçüm ortalaması ('ölç. fNNN' = eski seri kare no, u eşleşmesiyle; f_eski≈f_yeni×0,63) × yeni ek çarpanı (boolean kesit, emissive, DOF, yakın plan) tahminidir; makro derz ölçülmedi (varsayım 80 sn). Toplam d = 148 ana (f088–091 yok) + 8 makro + 4 önce/sonra ek = 160 render: ölçüm ortalamasıyla ≈6,2 sa, satır toplamıyla ≈7,0 sa (dalışın 3 karesi 600 sn varsayımıyla); m seti (her 2. kare, 0,73 piksel) ≈+2,3–2,6 sa; d+m ≈8,5–9,6 sa. Düzeltme paketi (yeni_isler: RENDER HIZLANDIRMA) tutarsa hedef ort ≤90 sn: d ≈4,0 sa, d+m ≈5,5 sa (varsayım). Seri, ön süre testi bitmeden ve açık soru 3 yeniden onaylanmadan başlatılmaz.

**Gereken yeni işler (s1):**
- s1_urun.py: kamera_pozu başlangıcını s0 C kamerasına bağla (az +32°, el 1°, 24 mm, 24 m, hedef (-0,5; -4; 4,6)); tur yönü +az; dolly-zoom 24→35 mm; FRAMES 96→152; DURAK eşikleri saniyeden: u=(t-32)/38.
- RENDER HIZLANDIRMA (s1_urun.py; seri öncesi ön koşul): (1) transparent_max_bounces 32→12 (kit varsayılanı 8, s1_urun 32'ye çıkarmış; yüksek saydamlıkta her kamera ve gölge ışını onlarca yüzey geçiyor); röntgen karelerinde (f016, f032, f056 benzeri) koyu leke çıkarsa 16'ya. (2) V kilidi: dal>0,995 ise V=1,0 yaz (Mix sabit katlanır; f092'de V=0,9991 olduğundan ham gazbeton malzemesi her saydam vuruşta hesaplanıyor ve %0,09 opak ışın koyu leke bırakıyor — olası neden, ön testle doğrulanacak) ve V≥0,98 olan türlerin nesnelerini hide_render=True yap (alternatif: kamera + gölge ışın görünürlüğünü kapat; holdout alfa gerektirir, film_transparent kapalı: tercih edilmez); V ara değer penceresini (0<V<0,98) ≤6 kareyle sınırla (f140–145). (3) örnekleme: samples 28→20, adaptive_threshold 0,02→0,04–0,05, adaptive_min_samples 0→8 (OIDN albedo+normal zaten açık); her değişiklik f032/f092/f020 benzeri kareyle ölçülür, görsel fark kabul edilirse alınır. (4) yedek: dalış V karışımını Blender'da değil, iki geçişin (ev katı + yalnız blok) 2B çapraz erimesiyle yap (saydam ışın maliyeti sıfır).
- ÖN SÜRE TESTİ (seriden önce; ağır render yok): EGE_PREVIEW=25, samples ≤8, tek kare. Kareler: f140, f144, f146, f092 benzeri V≈0,999, f032 (U blok yakın), f088/f090. Her biri bounces 32 / 12 ve V 0,9991 / 1,0 ile 2×2 karşılaştırılır; arka plandaki tam render kuyruğu süreleri bozar, süreler yalnız göreli okunur (mümkünse kuyruk dururken). Kabul: dalış kareleri ≤120 sn, ort ≤90 sn (tam çözünürlük karşılığı); tutmazsa açık soru 3'te B/C seçeneği.
- SERİ ÇIKTISI: yeni 152 kareli seri YENİ klasöre (ör. render/s1urund152, s1urunm152) yazılır. Çalışan 96 kareli seri (s1urund, az −32°, FRAMES 96, 35 kare ≈1,7 sa render) yeni plana uymaz ve arşive (eski_s1d_96) alınır; aynı klasörde --skip-existing kullanılırsa 000–095.png eski kareleri yeni dizinin kareleri sanıp atlar. Önce d, sonra m (EGE_MINSTEP=2).
- s1_urun.py: giriş röntgeni (u=0'da G≈0,6) + z eşikli tarama bandı + meta 'tarama' çapası.
- s1_urun.py: donatı ve hatıl betonuna lime (H) uygulamayı kapat; lime yalnız ürün kabuğu, harç/torba/levha. Lazer çizgisi beyaz.
- bina_detay.uret: iç bölme duvarı (y=0 aksı); çatı panellerini y=0 kirişinde 4,5 m açıklığa böl.
- s1_urun.py: düz + geçmeli blok çıkış animasyonu (kit.gecmeli_blok); cephe kesit penceresi + turuncu ısı oku kümesi (stil_r4.sahne_isi'den taşı); lento yük okları ve kayma.
- s1_urun.py: U blok kullanım pin çapaları, beton dolum ve kalk eğrilerini 5 sn'ye göre yeniden zamanla; harç ağı lime çizim animasyonu; tutkal torbası (stil_r4.sahne_urunler); panel şerit dalgası ve piyano animasyonu.
- s1_urun.py: EGEPOR levhaları parça parça yerleşir; kolon/kiriş turuncu ısı emission'ı; önce/sonra çift render (f124–127); çıkış koro dalgası; dalış eğrisi 4 sn.
- Makro derz sahnesi: stil_r5.sahne_derz'den 8 karelik (m000–007) 3 mm derz makrosu; halka geçişi JS 2B; lazer beyaz, lime yalnız tutkal.
- meta.json çoklu çapa: u_lento_a/b, u_ublok_cati/ara/baca, u_panel_aciklik, u_tutkal_derz, tarama; kit.project ile her kare yazılır.
- Web: ayarlar.js SAHNELER boy güncelle (s0 704, s1 836, s2 440, s3 308, s4 352, s5 352; son 220 vh); index.html s1 data-bas/data-son p'ye göre (giriş 0–0,105, duvar 0,105–0,237, lento –0,368, U blok –0,5, tutkal –0,632, panel –0,763, EGEPOR –0,895, çıkış –1,01).
- Web: ürün çip çubuğu (6 çip, tıklayınca 4× hızlı sarma, ← → klavye, aktif çip lime), ek SVG katmanı (.eg-ek: ölçü çizgileri, pinler, kütle çubuğu), beyaz perde spotu (radial-gradient), sayaç, önce/sonra süpürme, halka geçişi (clip-path).
- Web: dil.js yeni nokta kartları (u_duvar_cesit, u_lento_a, u_ublok_cati, u_tutkal_derz, u_panel_aciklik), kartlara 'Ürün sayfası' ve 'Teknik föy' bağlantısı; CSS oz-olcu lime-hi → beyaz/açık gri.

### s2 · Doğuş: hammaddeden bloğa — 70–90 sn

**Amaç.** Merak, şaşkınlık, kavrayış, güven. Sağlam blok önce beş sade hammaddeye çözülür; her birinin görevi tek sözcük ve dokunulur kartla öğrenilir. Karışım, kalıp, kabarma (hidrojen), tel kesim ve otoklav gerçek makine diliyle görünür olur. Çıkışta 'hacmin çoğu hava' cümlesi, hafiflik ve yalıtımın nedenini anlatacak gözenek dalışına (s3) köprü kurar.

#### t=70 (1:10) · 1540 vh · p=0.0
- **Kare:** Blender s1_dogus f000-004 (f000 = s1 f151) + HTML metin
- **Görsel:** Beyaz fonda tek blok, merkezde, 3/4 sağ-ön, ekran genişliğinin ~%40'ı. Kamera çok yavaş yaklaşır; lens kayması 0'dan 0,5'e, blok sağa süzülür, sol anlatım alanı açılır.
- **Metin:** 05 · Üretim — Bir blok, beş hammadde.  
  *EN:* 05 · Production — One block, five raw materials.
- **Efekt:** Blok üst kenarında ince lime ışık çizgisi doğar (çözülme cephesi, ürün vurgusu). Anahtar ışık 8° kayar; yüzde gözenek benekleri parlar.
- **Rakam · kaynak:** 5 hammadde (müşteri onaylı i1 metni)
- **Etkileşim:** İmleç bloğa gelince hafif eğim (EGIM_PX 14); kaydırma oku nabız atar.
- **Pazarlama:** 'Bu blok nasıl doğuyor?' sorusuna cevap: şeffaf üretim vaadi.
- **Üretim:** s1_dogus beyaz stüdyoya taşınır; s1 f151 kamera ve ışığı kopyalanır. 5 kare x ~45 sn (d). Lens kayması animasyonu 0,25 gün.
- **Telefon:** Blok üst-orta, başlık üstte; kaydırma oku altta.
- **Risk:** s1 f151 ile poz, ölçek ve zemin gölgesi birebir olmalı (altın kare); s1_dogus bugün koyu stüdyoda.
#### t=71 (1:11) · 1562 vh · p=0.05
- **Kare:** Blender s1_dogus f005-009
- **Görsel:** Lime cephe bloğu üstten alta süpürür; geçtiği yer taneye dağılır, 4800 tane yay çizerek yükselir. Kamera 1,3x geri çekilip yükselir; beş kaide belirir.
- **Efekt:** dissolve_material: cephe H/2+0,06'dan aşağı (τ0,6-2,0); iç yüzde çekirdek ışıması, bloom. Kaideler zeminden çıkar (k_p).
- **Etkileşim:** Kaydırmayı durdurunca cephe karede kalır; geri kaydırınca blok yeniden birleşir (çift yönlü).
- **Pazarlama:** Görsel şok: sağlam blok ham haline döner; üretimin merak anı.
- **Üretim:** grain_setup/grain_state ve cephe var; zamanlar τ saniyeye çevrilir. 5 kare x ~50 sn (4800 tane).
- **Risk:** Lime yalnız blok yüzünde; taneler lime olmasın (hammadde = ürün değil).
#### t=72 (1:12) · 1584 vh · p=0.1
- **Kare:** Blender s1_dogus f010-014 + SVG nokta halkaları
- **Görsel:** Son taneler yay sonunda kaidelere oturur: kum, kireç, çimento, alçı yığını; ortada havada alüminyum bulutu. Kamera yüksek 3/4 geniş (x1,48, pitch 14°).
- **Metin:** Noktalara dokunun.  
  *EN:* Tap the dots.
- **Efekt:** Taneler yerçekimiyle yığına oturur (2 kare sekme); kaide temas gölgeleri; DOF f/5,6. Blok tamamen gitti.
- **Etkileşim:** Beş hammadde noktası nabız halkasıyla belirir (kum, kireç, çimento, alçı, alüminyum); dokununca görev kartı.
- **Pazarlama:** Keşif daveti: izleyici üretimin içine girer, kendi hızında öğrenir.
- **Üretim:** kit.project ile 5 çapa her kare meta.json'a (var). Yığınlar koni dizilimi ~900 tane/kaide (0,4 gün). 5 kare x ~50 sn.
- **Telefon:** Yay 0,68 daraltılır; noktalar 44 px dokunma alanı, etiket yalnız dokununca.
- **Risk:** Yığın boyları reçete oranı izlenimi vermesin: dört yığın eşit, alüminyum küçük; gerçek reçete teyit gerekli.
#### t=73 (1:13) · 1606 vh · p=0.15
- **Kare:** Blender s1_dogus f015-019 + HTML
- **Görsel:** Kamera sola kayıp kum yığınına rack focus yapar: sıcak bej silis kumu taneleri, yığında kayan parıltı. Diğer yığınlar %35 flulaşır.
- **Metin:** Kum — Ana hammadde.  
  *EN:* Sand — Main raw material.
- **Efekt:** Sıcak yan ışık; yığından 20 tane havalanıp süzülür; seçili nokta halkası vurgulanır; focus_distance kare başına animasyonlu.
- **Etkileşim:** Kum noktası: 'Silis kumu: gazbetonun ana hammaddesi.' (NOKTALAR.kum). Stepper 'Hammadde' yanar.
- **Pazarlama:** Tanıdık, sade malzemeyle başlayan güven.
- **Üretim:** cam_pose anahtarları τ3-8 kaide x'ine bağlanır; DOF odak eğrisi. 5 kare x ~50 sn.
- **Telefon:** Kamera dikey kayar; yığın alt-orta, kart alttan sayfa.
#### t=74 (1:14) · 1628 vh · p=0.2
- **Kare:** Blender s1_dogus f020-024 + HTML
- **Görsel:** Kamera kireç yığınına geçer: ince beyaz toz, zirvede toz tütmesi. Kum yığını arkada flulaşır.
- **Metin:** Kireç — Bağlayıcı.  
  *EN:* Lime — Binder.
- **Efekt:** Beyaz toz tütmesi (40 parçacık); yığın hafif titrer; yumuşak üst ışık. Kireç beyaz kalır, lime yeşili yok.
- **Rakam · kaynak:** 200 t/gün kireç tesisi (Söke) · Ege Gazbeton ortak rakamlar; yalnız kartta
- **Etkileşim:** Kireç noktası: 'Karışımın bağlayıcısı. Söke'de günde 200 ton kapasiteli kendi kireç tesisimiz var.'
- **Pazarlama:** Fark: kendi kireç tesisi, hammadde kontrolü; s4'te yeniden anılır.
- **Üretim:** Mevcut yığın + toz tütmesi parçacıkları (0,1 gün). 5 kare x ~50 sn.
- **Risk:** Kireç (malzeme) ile lime (marka yeşili) karışmasın: yığın beyaz.
#### t=75 (1:15) · 1650 vh · p=0.25
- **Kare:** Blender s1_dogus f025-029 + HTML
- **Görsel:** Kamera sağa kayar: mat gri çimento yığını yoğun ve ağır durur; yığın kenarından ince gri toz çizgisi akar.
- **Metin:** Çimento — Dayanımı destekler.  
  *EN:* Cement — Adds strength.
- **Efekt:** Işık alçalır, kontrast artar; mat tane (rough 0,8); toz çizgisi 60 parçacık; arka yığınlar flu.
- **Etkileşim:** Çimento noktası: 'Dayanımı destekleyen bağlayıcı.' Kart kapanınca kamera kaldığı yerden sürer.
- **Pazarlama:** Dayanım vurgusu: hafif ama sağlam algısı.
- **Üretim:** Toz çizgisi parçacıkları (0,1 gün). 5 kare x ~50 sn.
#### t=76 (1:16) · 1672 vh · p=0.3
- **Kare:** Blender s1_dogus f030-034 + SVG kumsaati
- **Görsel:** Kamera dördüncü yığına geçer: kırık beyaz-pembe ince alçı tozu. Yığın yanında küçük kumsaati simgesi çizilir; kum yavaş akar.
- **Metin:** Alçı — Prizi düzenler.  
  *EN:* Gypsum — Controls setting.
- **Efekt:** Kumsaati simgesi çizilir (stroke-dashoffset 0,5 sn); toz yumuşak, parlaklık düşük; kamera hafif yükselir.
- **Etkileşim:** Alçı noktası: 'Prizlenmeyi düzenler.' Karta tek cümle sözlük: priz = sertleşmeye başlama (teyit gerekli).
- **Pazarlama:** Jargonu açan dil: uzmana da yapı sahibine de hitap.
- **Üretim:** SVG kumsaati (0,1 gün); Blender kısmı mevcut yığın. 5 kare x ~50 sn.
- **Risk:** 'Priz' sözlüğü mühendis onayı gerektirir; alçının tam rolü kartta ek iddiaya dönüşmesin.
#### t=77 (1:17) · 1694 vh · p=0.35
- **Kare:** Blender s1_dogus f035-039 + HTML
- **Görsel:** Kamera yükselip ortada havada asılı alüminyum bulutuna rack focus yapar: gümüş pul taneler, metalik pırıltı; en küçük bulut.
- **Metin:** Alüminyum tozu — Kabartır.  
  *EN:* Aluminium powder — Makes it rise.
- **Efekt:** Pul tanelerde kayan spekülar parıltı (bloom eşiği); bulut içinde birkaç küçük parıltı: kabarmanın habercisi.
- **Etkileşim:** Alüminyum noktası: 'Kireçle tepkimeye girip hidrojen açığa çıkarır: karışım kabarır.' Beş nokta tamamlanınca stepper 'Hammadde' dolar.
- **Pazarlama:** Merak kancası: az ama kritik malzeme; pay oranı gösterilmez.
- **Üretim:** ALU_CLOUD metalik taneler (var); DOF odak eğrisi. 5 kare x ~50 sn.
- **Telefon:** Alüminyum bulutu ekran üst-ortasında, kamera dikey yükselir.
- **Risk:** Alüminyum emisyonu (0,9) beyaz stüdyoda gerekmez; yalnız spekülerle parlasın.
#### t=78 (1:18) · 1716 vh · p=0.4
- **Kare:** Blender s1_dogus f040-044 + SVG stepper
- **Görsel:** Beş bulut birlikte kalkıp tek dar sarmalda karışarak iner. Soldan raylar üstünde çelik kalıp arabası kayarak girer. Girdap merkezine ince su akımı iner.
- **Metin:** Karışım — Su katılır.  
  *EN:* Mixing — Water is added.
- **Efekt:** Beş renk sarmal (helix, τ8,0-9,0); su akımı: şeffaf Principled, IOR 1,33; kaideler zemine iner; kalıp tekerleği ışıltısı.
- **Etkileşim:** Stepper 'Karışım' yanar; adımlara tıklayınca ilgili ana sarılır (4x hızlı).
- **Pazarlama:** Beş ayrı malzeme tek karışım: kontrollü üretim algısı.
- **Üretim:** Raylar ve kalıp arabası animasyonu (0,5 gün); su şeridi (silindir + akış gölgelendiricisi, 0,25 gün). 5 kare x ~55 sn.
- **Telefon:** Raylar dikey kadrajda alt şeritte; kalıp ortada.
- **Risk:** Su 6. madde gibi okunmasın: 'beş hammadde' sayısı korunur, su yalnız görsel.
#### t=79 (1:19) · 1738 vh · p=0.45
- **Kare:** Blender s1_dogus f045-049 + HTML
- **Görsel:** Kamera yüksek ön açıdan kalıba iner: sarmal kalıba akar, krem-gri bulamaç dibe yayılıp kalıbın yarısına yakın dolar. Nervürler, yan kilitler, ray tekerlekleri seçilir.
- **Metin:** Kalıp dolar.  
  *EN:* The mould fills.
- **Efekt:** Bulamaç ıslak parlak (rough 0,25, coat); yüzeyde yavaş dalga bump; SVG kesikli dolum çizgisi çizilir.
- **Etkileşim:** Kalıp noktası (yeni kart): 'Karışım çelik kalıba dökülür; kabarma burada olur.'
- **Pazarlama:** Endüstriyel ölçek: çelik kalıp, ray, kilit; ciddi tesis hissi.
- **Üretim:** build_mold detay: 6 nervür, 8 kilit, conta, kaynak dikişi, ray; Bevel düğümü + Pointiness kenar aşınması (0,6 gün). 5 kare x ~50 sn.
- **Risk:** Kalıp gri çelik, yeşil yok. Kalıp ölçeği temsilî (gerçek kalıp çok daha uzun).
#### t=80 (1:20) · 1760 vh · p=0.5
- **Kare:** Blender s1_dogus f050-054 + SVG 'H₂' simgesi
- **Görsel:** Kamera kalıbın açık ön kesitine alçalır (eğitim kesiti, ön cidar şeffaf). Bulamaç içinde ilk hidrojen kabarcıkları belirir ve yukarı süzülür.
- **Metin:** Kabarma — Hidrojen kabarcıkları.  
  *EN:* Rising — Hydrogen bubbles.
- **Efekt:** 1500 kabarcık (alfa 0,6, kırılmasız, ucuz); kesit yüzünde Voronoi hücre maskesi yarıçapı 0'dan büyür; iki kabarcıkta 'H₂' simgesi.
- **Etkileşim:** Kabarma noktası (var): kartta mini şema Al + Ca(OH)₂ + H₂O → H₂↑ (basitleştirilmiş). Stepper 'Kabarma' yanar.
- **Pazarlama:** Görünmez kimyayı görünür kılmak: uzmanlık ve şeffaflık.
- **Üretim:** Kesit Voronoi gölgelendiricisi ve kabarcık dizisi (0,6 gün). 5 kare x ~60 sn.
- **Telefon:** Kesit tam genişlik alt yarıda; 'H₂' simgesi büyük.
- **Risk:** Denklem basitleştirilmiş, denkleştirilmemiş: mühendis teyidi gerekli. Şeffaf cidar temsilî (gerçek kalıp opak).
#### t=81 (1:21) · 1782 vh · p=0.55
- **Kare:** Blender s1_dogus f055-059 + SVG seviye oku
- **Görsel:** Seviye kalıbın yarısından tepesine tırmanır, üst yüzey kubbeleşir. Kesitte hücreler büyür, kabarcıklar yüzeyde kaybolur. Kamera alçalıp seviyeyi izler.
- **Metin:** Karışım şişer.  
  *EN:* The mix swells.
- **Efekt:** level = MOLD_H*(0,45+0,55*ease_out); kubbe gürültüsü; hücre yarıçapı x3; SVG yukarı ok ve kesikli başlangıç çizgisi.
- **Etkileşim:** Seviye okuna dokun: başlangıç çizgisine 0,6 sn geri sarar, sonra devam eder (tekrar izle). Soru 2 çipi köşede belirir (bilgi_yarismasi): 'Karışımı ne kabartır?' + 3 şık, tek dokunuş, zorunlu değil; alüminyum/kabarma kartı açıksa soru bekler. Çip CTA değildir (s2 CTA'sız kalır).
- **Pazarlama:** Hacim artışı: hafiflik fikrinin kaynağı.
- **Üretim:** KekDeri ölçek 0,2->1 (var); hücre gölgelendirici zaman değeri; SVG ok (0,15 gün). 5 kare x ~60 sn.
- **Risk:** Yükseklik oranı rakamla gösterilmez (gerçek kabarma oranı teyit gerekli).
#### t=82 (1:22) · 1804 vh · p=0.6
- **Kare:** Blender s1_dogus f060-064 + SVG saat halkası
- **Görsel:** Kabarma biter: kek kalıbı doldurur, kubbe hafif taşar; yüzey ıslak parlaklıktan mata döner. Köşede saat halkası döner (bekleme). Kesitte hücreler hava dolu.
- **Metin:** Hava hücreleri kalır.  
  *EN:* Air cells remain.
- **Efekt:** Malzeme ıslak->mat karışımı (0,6 sn); SVG saat ibresi 1 tur; kabarcık sayısı 0'a iner; kamera x0,92 geri çekilir.
- **Rakam · kaynak:** Ön sertleşme süresi: teyit gerekli (ekranda yok)
- **Etkileşim:** Saat halkasına dokun: 'Kalıptaki karışım kabarır ve ön sertleşme kazanır.' (kabarma kartı). Soru 2 çipi köşede sürer; cevap sonrası 'Doğru.' + kaynak (dil.js aluminyum) ya da doğrusu, ardından söner; pencere t=82'de kapanır, çıkış geçişi (t=87–89) modülsüz kalır.
- **Pazarlama:** Sabır ve kontrol: zamana yayılan süreç, tutarlı sonuç.
- **Üretim:** Saat halkası SVG (0,15 gün); ıslak/mat malzeme geçişi. 5 kare x ~55 sn.
- **Telefon:** Saat halkası sağ üst köşede küçük.
- **Risk:** Süre hiçbir yerde rakamla gösterilmez; Ege hattı süresi alınana dek.
#### t=83 (1:23) · 1826 vh · p=0.65
- **Kare:** Blender s1_dogus f065-069 + HTML
- **Görsel:** Kalıp yan cidarları aşağı açılır; kek çıplak, nemli koyu gri. Tel kesme portalı raylarda girer: çerçeve, makara, gergi yayı, gerili teller. Kamera sol-alçak, tel hizasında.
- **Metin:** Tel kesim.  
  *EN:* Wire cutting.
- **Efekt:** Cidarlar z -MOLD_H*1,02 iner; portal kayar; tel emission 6 + bloom; yay (helix) hafif titrer; turuncu uyarı bandı.
- **Etkileşim:** Kesim noktası (var): 'Teller keki hassas ölçüde keser; yüzeyler düz ve gönyede olur.' Hover'da teller sırayla parlar (CSS).
- **Pazarlama:** Mühendislik gösterisi: tel kesme makinesi = hassasiyet.
- **Üretim:** tel_kesme(): 2 sütun + traverse, 6 makara, helix gergi yayı, 0,6 mm tel silindiri, ray (0,75 gün). 5 kare x ~50 sn.
- **Telefon:** Portal dikey kadrajda ortada; teller dikey çizgi.
- **Risk:** Söke kesme makinesi farklı olabilir (portal/yatık kesim); referans fotoğraf (yalnız yerel, depoya konmaz) gerekli.
#### t=84 (1:24) · 1848 vh · p=0.7
- **Kare:** Blender s1_dogus f070-074 + HTML
- **Görsel:** Teller kekten aşağı geçer: kek beş dilime ayrılır, kesit yüzleri parlak ve düz; ince toz dökülür. Yatay tel kabarık üstü sıyırır; bloklar aralanır.
- **Metin:** Yüzeyler düz, gönyede.  
  *EN:* Faces flat and square.
- **Efekt:** wires z=MOLD_H+0,06'dan aşağı (τ13,4-14,6); kesit yüzünde 0,2 sn nemli parıltı; 300 toz parçacığı; KekDeri sıyrılıp gizlenir.
- **Rakam · kaynak:** 60 × 25 cm yüz (Ürün föyleri); yalnız blok kartında
- **Etkileşim:** Dilim üzerinde imleç: blok hafif kalkar (CSS parıltı). Kesim kartı açık kalabilir.
- **Pazarlama:** Düz yüzey, ince derz: s1'deki 1-3 mm derz vaadinin kaynağı (çıkarım; teyit gerekli).
- **Üretim:** k_cut eğrisi 1,2 sn'ye göre; yatay tel + kubbe sıyırma yeni (0,3 gün). 5 kare x ~50 sn.
- **Risk:** Kubbe sıyırma/geri dönüşüm Ege hattında aynen uygulanıyor mu: teyit gerekli (yalnız görsel).
#### t=85 (1:25) · 1870 vh · p=0.75
- **Kare:** Blender s1_dogus f075-079 + HTML
- **Görsel:** Bloklar arabayla raylarda sağa taşınır, kamera yatay izler. Önde otoklav: fırçalanmış alüminyum kılıflı yatay silindir, açık kapı, buhar sızıntısı. Arkada hayalet hol, lime şerit.
- **Metin:** Otoklav — Basınçlı buhar.  
  *EN:* Autoclave — Pressurised steam.
- **Efekt:** Travelling; kapak kilit segmentleri (24 örnek); buhar düzlemleri; arka hol %8 hayalet (lime şerit = fabrika şeridi).
- **Etkileşim:** Otoklav noktası (yeni kart): 'Yüksek basınçlı buhar: kek burada sertleşir, mineral yapıya kavuşur.' Stepper 'Otoklav' yanar.
- **Pazarlama:** Gerçek tesis hissi, s4 fabrikasına hazırlık.
- **Üretim:** otoklav(): silindir + elips kapak, fırçalı alüminyum kılıf bantları, 24 kilit, menteşe, boru, vana, yazısız manometre (1 gün). 5 kare x ~55 sn.
- **Telefon:** Otoklav kapısı alt-orta, araba soldan girer; hayalet hol yok.
- **Risk:** Otoklav detayı gerçek tesisten farklı olabilir (referans fotoğraf gerekli). Yeşil yalnız fabrika şeridi.
#### t=86 (1:26) · 1892 vh · p=0.8
- **Kare:** Blender s1_dogus f080-084 + SVG kadran
- **Görsel:** Kesit görünümü: otoklavın ön yarısı saydamlaşır; raylı vagonda bloklar, buhar dalgalanır. Bloklar nemli griden aydınlık beyaza ağarır. Manometre ibresi yükselir.
- **Metin:** Mineral yapı oluşur.  
  *EN:* A mineral structure forms.
- **Efekt:** Kesit penceresi (nesne koordinatı eşiği); buhar düzlemleri + sıcak amber iç ışık; blok gri->beyaz mix 0->1 (1 sn); SVG kadran ibresi.
- **Rakam · kaynak:** Tipik AAC otoklavı yaklaşık 180-200 °C, 10-12 bar (genel bilgi): TEYİT GEREKLİ, ekranda yok
- **Etkileşim:** Mineral matris noktası (var): 'Otoklavda buharla sertleşen kalsiyum silikat yapı.' Kadran yalnız gösterge, çentikli, rakamsız.
- **Pazarlama:** Dayanıklılığın kaynağı: otoklavda oluşan mineral yapı.
- **Üretim:** Kesit penceresi s1_urun.gecis_malzeme dilinden; blok sertleşme mix; SVG kadran (0,2 gün). 5 kare x ~60 sn.
- **Telefon:** Kadran sağ üstte küçük; kesit tam genişlik.
- **Risk:** Kimya iddiası mevcut kart metniyle sınırlı kalır; sıcaklık/basınç rakamı doğrulanmadan gösterilmez.
#### t=87 (1:27) · 1914 vh · p=0.85
- **Kare:** Blender s1_dogus f085-089 (çıkış geçişi 1/3) + HTML
- **Görsel:** Otoklav kapısı açılır, buhar fışkırır, vagon dışarı kayar. Kamera buhar perdesinden geçip en öndeki sertleşmiş bloğa dalar (1 m -> 15 cm); blok bembeyaz.
- **Metin:** Sertleşti.  
  *EN:* Hardened.
- **Efekt:** Buhar düzlemi kamera önünden geçer (geçiş maskesi); kapı menteşe eylemsizliği; blok kenarında ürün lime ışıltısı H=3; arka plan beyaza erir.
- **Etkileşim:** Blok noktası ('blok' kartı): '60 × 25 cm yüz; sıra sıra, şaşırtmalı örülür.' Kaydırma oku nabız atar.
- **Pazarlama:** Sonuç anı: ham maddeden kusursuz bloğa; güven tamamlanır.
- **Üretim:** Dalış eğrisi (kit.smoother) 1 sn'ye göre; DOF f/2,8; buhar perdesi (0,2 gün). 5 kare x ~50 sn.
- **Telefon:** Blok dikey kadrajın ortasında, ekranın %55'i.
- **Risk:** Lime kenar yalnız blokta; vagon ve ray yeşil olamaz.
#### t=88 (1:28) · 1936 vh · p=0.9
- **Kare:** Blender s1_dogus f090-094 (makro, 2/3) + SVG halka
- **Görsel:** Kamera kesilmiş yüze 15 cm'den 3 cm'ye yaklaşıp yüzey boyunca kayar: yüz düz, küçük gözenek çukurları belirir, büyür; iri bir kahraman gözenek merkeze oturur.
- **Metin:** Hacmin çoğu hava.  
  *EN:* Mostly air by volume.
- **Efekt:** Makro DOF f/1,8; Cycles hareket bulanıklığı; blok dışı beyaza erir, lime kenar söner; SVG lime halka daralır (clip-path).
- **Rakam · kaynak:** Hava hacim oranı (%): teyit gerekli (ekranda yok)
- **Etkileşim:** Gözenek noktası belirir ('hucre' kartı s3'te açılır); kaydırma oku nabız atar.
- **Pazarlama:** Hafifliğin nedeni tek cümlede; s3 yalıtım vaadine köprü.
- **Üretim:** aac_material bump 1,1 + kahraman gözenek (3 mm küre kesici); hareket bulanıklığı (0,25 gün). 5 kare x ~55 sn.
- **Telefon:** Halka üst-ortada; yüzey tam dolgu.
- **Risk:** Blok yüzü s3 numune dokusuyla birebir değil: kahraman gözenek hizası ve bulanıklık farkı saklamalı.
#### t=89 (1:29) · 1958 vh · p=0.95
- **Kare:** Blender s2_gozenek ön-ısınma f(-5..-1) = s2 f095-099
- **Görsel:** Kamera kahraman gözeneğe iner (3 cm -> 1,5 cm): gri-beyaz makro yüzey, gözenekler ekranı doldurur. Son kare, s3 f000'dan bir adım önce; poz birebir devam eder.
- **Metin:** İçine bakalım.  
  *EN:* Let's look inside.
- **Efekt:** Numune ışığı ve yüzeyi; f094->095 hizalı çapraz erime + hareket bulanıklığı; beyaz stüdyo hafif griye iner; vinyet 0,2.
- **Etkileşim:** Kaydırma oku nabız atar; s3'ün ilk kartı için 'hucre' noktası f100'den başlar.
- **Pazarlama:** Merak köprüsü: hafifliğin ve yalıtımın nedeni içeride.
- **Üretim:** s2_gozenek.py'ye u<0 ön-ısınma 5 kare; dalış eğrisi s3 ile tek fonksiyon (0,5 gün). 5 kare x ~75 sn.
- **Telefon:** Gözenek dikey kadrajda merkezde; kamera aynı.
- **Risk:** s3 planlayıcısıyla ilk kare, kamera eğrisi, ışık ve zemin rengi eşleşmeli; ayrı planlandığı için teyit.

**Geçiş ve üretim notu (s2).** Satırlar t=70..89 (20 satır; t=90 s3'ün ilk saniyesi). p=(t-70)/20 (satır başı); τ=t-70. Kare: 5 kare/sn, 100 kare, f=(t-70)*5..+4, u=f/99; telefon her 2. kare (EGE_MINSTEP=2). Zamanlama (τ sn): bekleme 0-0,6; çözülme cephesi 0,6-2,0; tane uçuşu 0,8-2,8; hammadde sırası kum 3, kireç 4, çimento 5, alçı 6, alüminyum 7; sarmal ve kalıp girişi 8-9; dolum 9-10; kabarma 10-13; tel kesim 13-15; otoklav 15-17; çıkış 17-20. Metin düzeni s1 ile aynı: metin yalnız belirdiği saniyeye yazıldı, sonraki saniyede '' kalır ve ekranda durur; yeni sözcük en çok 3/sn. Web vuruşları (p): başlık 0-0,10; ipucu 0,10-0,15; kum 0,15; kireç 0,20; çimento 0,25; alçı 0,30; alüminyum 0,35; karışım 0,40-0,50; kabarma 0,50-0,65; tel kesim 0,65-0,75; otoklav 0,75-0,85; çıkış 0,85-1,01. Stepper adımları: Hammadde 0,15; Karışım 0,40; Kabarma 0,50; Kesim 0,65; Otoklav 0,75. Işık ve renk: s1_urun ile aynı beyaz stüdyo (stil_r.studyo + kit zemin gölge tutucu); s1_dogus bugün koyu stüdyoda (s0_video_blok), beyaza taşınmalı. Lime YALNIZ ürün: blok çözülme cephesi, bitmiş blok kenarı, lime halka ve fabrika şeridi; hammadde, buhar, kalıp, tel, ray, otoklav beyaz-gri-amber (çelik yeşil olamaz). Kek rengi: nemli koyu gri (#bdb7ad) -> otoklav sonrası beyaz (#e9e6e0). s1->s2: s2 f000 = s1 f151 (poz, ölçek, gölge, ışık birebir); lens kayması 0'dan başlar, τ0-2'de 1'e gider (anlatım alanı sola açılır). s2->s3: f090-094 s1_dogus makro, f095-099 s2_gozenek ön-ısınma (u<0); aynı dalış eğrisi ve kahraman gözenek (s2_gozenek CHAIN[0], r 0,17 cm) ekran merkezinde; s3 f000 = s2 f100. Geri kaydırınca blok yeniden birleşir (kare tabanı çift yönlü). ayarlar.js: s2 boy 440; GECIS eşleşen kare geçişlerinde (s1->s2, s2->s3) 70 vh yerine 22 vh önerilir, yoksa kamera hareketliyken çift görüntü kalır.

**Gereken yeni işler (s2):**
- s1_dogus.py yeniden: FRAMES 96->100, zaman τ saniyeye bağlı, beyaz stüdyo (stil_r.studyo + kit zemin), s1 f151 kamera/ışık kopyası, lens kayması animasyonu, hotspot pencereleri (5 hammadde τ2,6-7,9; kalıp; kabarma; kesim; otoklav; matris; blok). ~0,75 gün.
- Hammadde yığınları: kaide başına ~900 tane koni dizilimi (33° yığılma açısı), tane yolu blok -> yay -> yığın; yalnız alüminyum bulut kalır. ~0,4 gün.
- fabrika_kit.py (yeni): boyalı çelik, fırçalı alüminyum kılıf (anizotropik), kauçuk conta, yağlı kalıp tabanı; Bevel düğümü ve Pointiness kenar aşınması, kaynak dikişi, cıvata örnekleri. Gerçeklik reçetesi: işlevsel ayrıntı (menteşe, kilit, yay, makara, ray), eylemsizlikli hareket, buhar ve toz. ~0,5 gün.
- kalip() + raylar + kalıp arabası animasyonu (nervür, yan kilit, tekerlek). ~0,6 gün.
- Kabarma kesiti: Voronoi hücre gölgelendiricisi (yarıçap zamanla büyür), 1500 kabarcık, kubbe ve ıslak->mat geçişi. ~0,6 gün.
- tel_kesme() portalı: sütun, traverse, makara, helix gergi yayı, 0,6 mm teller, yatay tel, kubbe sıyırma, kesit nem parıltısı, toz. ~0,75 gün.
- otoklav(): silindir + elips kapak, kılıf bantları, 24 kilit segmenti, menteşe kolu, boru/vana, yazısız manometre; kesit penceresi; buhar düzlemleri; vagon; kapı animasyonu; %8 hayalet hol (lime şerit). ~1 gün.
- Kek malzemesi: nemli koyu gri -> beyaz sertleşme geçişi; bitmiş blok için ürün lime kenarı (H). ~0,2 gün.
- s2_gozenek.py: u<0 ön-ısınma 5 kare, tek dalış eğrisi, kahraman gözenek (CHAIN[0]) hizası; s1_dogus f090-094 makro kahraman gözenek kesicisi. ~0,5 gün.
- Web: 5 adımlı stepper (tıklayınca 4x sarma), SVG katmanları (kesikli seviye çizgisi + ok, saat halkası, rakamsız kadran, kumsaati, lime halka clip-path), index.html SAHNE 2 vuruşları (data-bas/data-son yukarıdaki p'ler), ayarlar.js s2 boy 440 ve GECIS 22. ~1,25 gün.
- dil.js: yeni kartlar kalip, otoklav, kabarma mini şeması (Al + Ca(OH)₂ + H₂O → H₂↑), alçı 'priz' sözlüğü; TR/EN; kaynak satırları. ~0,25 gün.
- meta.json çoklu çapa: kum, kirec, cimento, alci, aluminyum, kalip, kabarma, kesim, otoklav, matris, blok (kit.project, her kare). Telefon: her 2. kare, dikey kamera varyantı. ~0,3 gün.
- Referans toplama: Söke hattı iç fotoğraf/video kareleri (yalnız yerel referans, depo herkese açık olduğundan konmaz); kalıp, kesme makinesi, otoklav oranları buradan alınır.

### s3 · Gözenek: ısıyı tutan hava — 90–104 sn

**Amaç.** Merak, şaşkınlık, güven. Bildiğimiz gri bloğun içine girilir; kapalı hava hücreleri görünür; ısının gözenek ağında dolanıp yavaşladığı bilim gibi izlenir. Üç kaynaklı rakam (λ 0,08 · A1 · 300–600) mühür gibi dizilir. Çıkışta gözenekten geri çekilip blok, palet ve Söke sahasına varılır: ürün hazır, yola çıkıyor.

#### t=90 (1:30) · 1980 vh · p=0.0
- **Kare:** Blender makro F00-F05 (F00 = s2 f100 adımı)
- **Görsel:** Kesilmiş blok yüzü makro: gri-beyaz gözenekler, kahraman gözenek ekran merkezinde. Kamera s2 dalışının ivmesiyle yavaşlayarak süzülür; odak yüzeyde.
- **Metin:** Isıyı tutan, içindeki hava.  
  *EN:* The insulation is the air inside.
- **Efekt:** Sığ netlik (f/11); sıyıran ışık gözenek kenarlarını oyar; havada 140 toz zerresi, bloom 0,3, vinyet 0,2. Başlık 12 px yükselip belirir.
- **Etkileşim:** Fare/parmak 14 px paralaks eğimi (mevcut EGIM_PX): gözenek derinliği hissedilir.
- **Pazarlama:** Kicker ‘06 · Yapı’; bilimsel merak: bildiğiniz gri bloğun içine bakıyoruz. Marka sessiz.
- **Üretim:** makro F00-F05: 6 kare × ~85 sn (d), efor 0,5 gün (kamera anahtarlarını saniyeye bağlama).
- **Telefon:** Gözenek alt-orta (shift_y 0,16), başlık üstte 2 satır.
- **Risk:** s2 f099 → s3 F00: kamera, ışık, odak, vinyet birebir (altın kare); s2 planıyla mutabakat.
#### t=91 (1:31) · 2002 vh · p=0.07
- **Kare:** Blender makro F06-F11 + SVG gözenek halkası
- **Görsel:** Kamera kahraman gözeneğe doğru kayar, hafif yukarı eğilir. Odak yüzeyden gözenek kenarına çekilir; gözeneğin derininde komşu hücrenin ışığı seçilir.
- **Metin:** Gözeneklerde hapsolmuş hava.  
  *EN:* Air trapped in every pore.
- **Efekt:** Odak çekme; gözenek ağzından içeri ışık huzmesi (kit.sis). Hava ışığı kirli zeytin yerine sıcak beyaz. Gözenek çevresinde ince lime SVG halka nefes alır.
- **Etkileşim:** Nabız atan halka + ‘dokunun’ ipucu. Dokununca kart: Kapalı hava hücresi (dil.js hucre: hücredeki hava hareket etmez).
- **Pazarlama:** Merak ve katılım daveti: site izlenmekle kalmaz, oynanır.
- **Üretim:** makro F06-F11 × ~85 sn. meta.json: kit.project ile gözenek merkezi/yarıçapı her kare; SVG halka JS ≤0,2 ms.
- **Telefon:** Halka ≥44 px dokunma hedefi; ipucu parmak simgesi.
- **Risk:** Hava ışığı rengi (s2_gozenek taslağında zeytin) sıcak beyaza çevrilir; lime yalnız halka, yani ürün vurgusu.
#### t=92 (1:32) · 2024 vh · p=0.14
- **Kare:** Blender makro F12-F17
- **Görsel:** Kamera gözeneğin ağzından içeri dalar; duvarlar sarar. Önde ince bir duvarda küçük pencere; ardındaki komşu, kapalı hücre sıcak beyaz ışıldar.
- **Metin:** etiket: Kapalı hava hücresi  
  *EN:* label: Closed air cell
- **Efekt:** Lens 42→15 mm; ağız açıklığı vinyet ve kaydırma geri alma ile gizlenir; huzme toz zerrelerini yakalar, bloom 0,3. Hücre içi zerreler neredeyse durağan.
- **Etkileşim:** Pencerede lime pin: dokununca ‘Hücredeki hava hareket etmez; ısı kolay geçemez.’ kartı (mevcut hucre).
- **Pazarlama:** Ürünün içine girmek: şeffaflık güven verir.
- **Üretim:** makro F12-F17 × ~90 sn (yakın alan + hacim, en pahalı); samples 24 + denoise. Efor 0,5 gün.
- **Telefon:** Lens 28 mm (dar); ağızdan stüdyo sızmaz.
- **Risk:** Dış stüdyo sızması: kit.kaydir ‘ic’ eğrisi (mevcut 0,24-0,34) yeni anahtarlara taşınmalı.
#### t=93 (1:33) · 2046 vh · p=0.21
- **Kare:** Blender makro F18-F23 (hayalet hücre ağı)
- **Görsel:** Kamera pencereye yaklaşırken ince duvar röntgene döner; ardında onlarca kapalı hücre hayalet balon olarak belirir. Kamera geri süzülmeye başlar.
- **Efekt:** Röntgen malzemesi (s1_urun.gecis_malzeme) hücre kürelerinde: beyaz-mavi Fresnel kenar, iç %12 saydam; matris yarı saydam. Hücre içi zerreler durağan.
- **Etkileşim:** Hayalet hücreler imleçle tek tek parlar (6 SVG halka); her biri aynı ‘Kapalı hava hücresi’ kartını açar.
- **Pazarlama:** Kapalı hücre ağı ürünün imzası; bir sonraki saniyede ısıyla ilişkilenir.
- **Üretim:** makro F18-F23 × ~70 sn. 2560 gözenekten en büyük 120 küre toplu_mesh ile; efor 1 gün (malzeme + meta).
- **Telefon:** 4 halka; hayalet kürelerde daha kalın kenar.
- **Risk:** Küreler arası duvar korunur (kodda ≥0,0075 birim): kapalı hücre okunmalı, kesişen küre görünmemeli.
#### t=94 (1:34) · 2068 vh · p=0.29
- **Kare:** Blender makro F24-F29 + SVG ısı çizgileri
- **Görsel:** Kamera ağızdan geri çıkıp kesit yüzüne dik, uzun objektifle durur: yüz dolusu gözenek. Solda sıcak, sağda soğuk kenar; soldan turuncu ısı çizgileri girer.
- **Metin:** Isı gözenekleri dolanır, yavaşlar. · etiket: sıcak · soğuk  
  *EN:* Heat winds around the pores and slows. · label: hot · cold
- **Efekt:** Hayalet küreler katı yüze erir. 28 akış çizgisi soldan sağa çizilir (stroke-dashoffset 0,7 sn); sol kenarda sıcak, sağda soğuk ışık.
- **Etkileşim:** Gözeneğe dokun: lime halka; o hattaki ısı darbesi gözeneğin kenarından dolanır (mini kart: hava hücresi).
- **Pazarlama:** Öğretici an: yalıtım görünür oluyor.
- **Üretim:** makro F24-F29 × ~55 sn. tools/isi_akis.py: yüz kesiti iletim çözümü (prototip 2 sn), JSON ≈40 KB; SVG/JS 1 gün.
- **Telefon:** Yüz tam genişlik, etiketler yüzün üstünde yatay.
- **Risk:** Çizgi-gözenek hizası: SVG, meta kesit dörtgeni + homografi.js ile oturur; kamera kayması ≤%1 (F26 sonrası sabit).
#### t=95 (1:35) · 2090 vh · p=0.36
- **Kare:** Blender makro F30-F35 + canvas ısı damlaları
- **Görsel:** Yüz sabit, %4 yaklaşma. Çizgiler gözenek boyunları arasında sıkışır, gözeneğin ardında seyrekleşir; ısı damlaları çizgi boyunca soldan sağa akar.
- **Efekt:** Damla hızı soldan sağa 1,0→0,25, alfa sönümü; renk turuncu→soluk amber→gri-mavi. 120 damla, 2B canvas ≤0,5 ms.
- **Etkileşim:** Gözenekler arası mineral duvara dokun: ‘Mineral matris’ kartı (otoklavda buharla sertleşen kalsiyum silikat yapı).
- **Pazarlama:** Merak çözülür: yalıtım = hava + dolanan yol.
- **Üretim:** makro F30-F35 × ~55 sn; ortak parçacık motoru (s0 kivilcim.js) 0,5 gün.
- **Telefon:** Damla sayısı 70.
- **Risk:** Hız ve sönüm anlatım amaçlı (fiziksel hız değil): sayı, süre, sıcaklık gösterilmez.
#### t=96 (1:36) · 2112 vh · p=0.43
- **Kare:** Blender makro F36-F41 + λ rakamı (F40-F41 halka başlangıcı)
- **Görsel:** Sağ kenarda çizgiler neredeyse söner, yüz soğuk tona geçer. Kamera hafif açılırken λ rakamı belirir; son karede lime halka yüzdeki bir gözeneğe kapanmaya başlar.
- **Metin:** λ 0,08 · W/mK · G2/350 duvar tasarım değeri  
  *EN:* λ 0.08 · W/mK · design value for G2/350 walls
- **Efekt:** Sağ yarıda çizgi alfası 0,1; rakam 12 px yükselip belirir, altında lime çizgi çizilir (0,5 sn). Halka 2B clip-path.
- **Rakam · kaynak:** λ 0,08 W/mK, G2/350 duvar tasarım değeri; kaynak: Ege Gazbeton ortak rakamlar
- **Etkileşim:** Rakama dokun: kaynak kartı + ‘Teknik föyler’ bağlantısı.
- **Pazarlama:** Güven: kaynaklı rakam, rakip kıyası yok.
- **Üretim:** makro F36-F41 × ~50 sn; rakam HTML (dil.js i2.k1, kaynak.ortak) 0,2 gün.
- **Telefon:** Rakam yatay etiket, metin alanında üstte.
- **Risk:** ‘Tasarım değeri’ ibaresi rakamdan ayrılmaz; ölçüm değeri gibi okunmamalı. Kaynak satırı zorunlu.
#### t=97 (1:37) · 2134 vh · p=0.5
- **Kare:** Blender tezgah F42-F47 (halka geçişi 2B F40-F43)
- **Görsel:** Halka bir gözeneğe kapanıp nokta olur; yeni halka açılınca nötr açık-gri stüdyo tezgâhı: 4 sıra gazbeton duvar parçası (60 × 25 cm bloklar, ince derz), yumuşak üst ışık. Kamera yavaş ileri dolly.
- **Metin:** A1 · yangına tepki sınıfı  
  *EN:* A1 · reaction-to-fire class
- **Efekt:** Ölçek atlaması (gözenek→duvar, 2B halka). Sıyıran yumuşak ışık blok dokusunu verir; A1 başlığı 12 px yükselip belirir. Alev, kor, renkli ışık, ısı efekti YOK. Nötr açık-gri stüdyo (#b8bec5).
- **Rakam · kaynak:** A1, yangına tepki sınıfı (EN 13501-1); kaynak: CE belgeleri
- **Etkileşim:** A1 rakamına dokun: CE belgeleri kartı (sınıf ne demek, belge nerede).
- **Pazarlama:** Bilgi tonu: sınıf adı + belge kapısı; korku ya da dramatik anlatım yok.
- **Üretim:** tezgah F42-F47 × ~30 sn (nötr stüdyo, hacim/alev yok); alev flipbook YOK; 2B halka tools/s3_birlestir.py 0,5 gün.
- **Telefon:** Duvar parçası ortada-alt; rakam üstte.
- **Risk:** Metin yalnız sınıfı söyler; yasak ifade kullanılmaz; sahnede yangını çağrıştıran görsel yok. Kamera yalnız ileri dolly (orbit yok): F47→F48 hizası korunur.
#### t=98 (1:38) · 2156 vh · p=0.57
- **Kare:** Blender tezgah F48-F53 + SVG sınıf merdiveni
- **Görsel:** Kamera duvar parçasına yavaşça yaklaşır; blok yüzleri sakin, gri-beyaz, sıyıran ışık gözenek dokusunu verir. Yanda HTML/SVG sınıf merdiveni basamak basamak çizilir; A1 basamağı vurgulanır.
- **Metin:** EN 13501-1 · CE belgeleri  
  *EN:* EN 13501-1 · CE certificates
- **Efekt:** Ağır dolly. Sınıf merdiveni (SVG, 7 basamak F→A1; stroke-dashoffset 0,6 sn) alttan çizilir, A1 vurgulu, ötekiler sönük (nötr koyu mürekkep; lime yok). Alev, kor, ısıl degrade, 'serin' etiketi YOK.
- **Etkileşim:** A1 basamağına/rozetine dokun: ‘Yangına tepki sınıfı’ mini kartı (a1_demo: sınıf, malzemenin yangına nasıl tepki verdiğini sınıflandırır; genel tanım) + CE belgeleri bağlantısı. Yalnız A1 dokunulur; ötekiler sönük. Soru 3 çipi köşede belirir (bilgi_yarismasi): 'A1 neyi anlatır?' + 3 şık, tek dokunuş, zorunlu değil; A1 mini kartı açıksa soru bekler (kart cevabı verir).
- **Pazarlama:** Kanıt kapısı: sınıf adı + belge; güvence ima eden görsel ya da söz yok.
- **Üretim:** tezgah F48-F53 × ~30 sn; meta ‘duvar’ + ‘a1_kart’ çapaları; sınıf merdiveni SVG 0,25 gün (gozenek.js içinde). Flipbook YOK.
- **Telefon:** Merdiven duvarın üstünde tek satır yatay (7 harf); duvar parçası ortada-alt.
- **Risk:** Alev, ısıl degrade, ‘serin yüz’, süre ve °C YOK: yangın direnci (EN 13501-2) belgesi yok, ima edilmez (açık soru 2). Merdiven harfleri (A1 A2 B C D E F) EN 13501-1'den, teyit gerekli: teyit gelmezse yalnız A1 rozeti + kart (yedek). Alev ya da yangın çağrıştıran öğe yalnız yangın direnci belgesi gelince ve ayrı karar olarak yeniden değerlendirilir.
#### t=99 (1:39) · 2178 vh · p=0.64
- **Kare:** Blender tezgah F54-F59 (yumuşak pan, G1/G2/G4 blok sırası)
- **Görsel:** Kamera duvar parçasından sağa yumuşak pan eder: aynı tezgâhta yan yana üç blok, G1, G2 ve G4. Üç blok aynı boyutta ve aynı dokuda (60 × 25 cm), eşit aralıkla; ortada G2.
- **Metin:** 300–600 kg/m³ · yoğunluk aralığı (G1–G4)  
  *EN:* 300–600 kg/m³ · density range (G1–G4)
- **Efekt:** Hafif hareket bulanıklığı; pozlama ve ışık sabit (tezgâh aynı kalır). Blokların üstünde HTML/SVG etiketleri G1/300 · G2/350 · G4/600 sırayla (0,25 sn aralık) belirir; rakam başlığı 12 px yükselir.
- **Rakam · kaynak:** 300–600 kg/m³ (G1–G4); kaynak: Ürün sınıfları G1/300 – G4/600
- **Etkileşim:** Blok etiketine dokun: sınıf adı kartı (yalnız sınıf adı + ‘Ürün sınıfları’ kaynağı; G3 yok). Rakam altında G1 → G4 kayan ok ipucu. Soru 3 çipi köşede sürer; cevap sonrası 'Doğru.' + kaynak (CE belgeleri) ya da doğrusu + nedeni, ardından söner; ağırlık 'Dene' çipi bu saniyede YOK, t=100'de açılır.
- **Pazarlama:** Kaynaklı rakam: sınıf adları ve yoğunluk aralığı; hafiflik, taşıma ya da suda davranış sözü yok.
- **Üretim:** tezgah F54-F59 × ~30 sn (üç blok, sığ tezgâh; cam, su, kaustik YOK); pan hareket bulanıklığı; üç blok dizilimi 0,5 gün (tank yeniden kurulumu 2 gün düştü).
- **Telefon:** Üç blok alt-orta, yan yana; dar kadrajda kamera biraz geri, etiketler üstte tek satır.
- **Risk:** Yüzme/su/tank YOK: ‘suda yüzer’ föy ve CE belgelerinde yok, yoğunluktan çıkarım (açık soru 1). Bloklar arasında doku farkı ‘fark var’ iddiası olarak okunmaz: üçü aynı doku, fark yalnız etiket. G3 gösterilmez (yoğunluğu teyit gerekli). G1/300 – G4/600 Ürün sınıfları, G2/350 ortak rakamlar kaynaklı. Tank/yüzme sürümü (F54-F65) yüzme onayı olmadan başlamaz; bu satırdaki tezgâh sürümü altın kare onayıyla render edilir.
#### t=100 (1:40) · 2200 vh · p=0.71
- **Kare:** Blender tezgah F60-F65 + şerit (halka başlangıcı F64-F65)
- **Görsel:** Kamera üç bloğun önünde hafifçe yükselir, ortadaki G2 bloğunun üst yüzüne eğilir. Blok etiketleri sönerken üç rakam şeride dizilir; lime halka G2'nin üst yüzündeki bir gözeneğe kapanmaya başlar.
- **Metin:** şerit: λ 0,08 · A1 · 300–600  
  *EN:* strip: λ 0.08 · A1 · 300–600
- **Efekt:** Yumuşak yükselme + hafif tilt; üç rakam soldan sağa 0,15 sn arayla dizilir (λ 0,08 · A1 · 300–600); halka daralır (2B clip-path). Cümle yok.
- **Rakam · kaynak:** Şerit: λ 0,08 · A1 · 300–600 (kaynaklar: ortak rakamlar, CE belgeleri, ürün sınıfları)
- **Etkileşim:** Şerit rakamlarına dokun: her biri kendi kaynak kartını açar (ortak rakamlar / CE belgeleri / Ürün sınıfları). ‘Teknik föyler’ bağlantısı. Film içinde G1–G4 kaydırıcısı yok; ağırlık denemesi ‘agirlik’ modülünde (panel); 'Dene' çipi bu saniyede rakam kartı köşesinde açılır (kullanıcı başlatımlı panel, kilitsiz).
- **Pazarlama:** Üç rakam mühür gibi yan yana; yumuşak CTA ‘Teknik föyler’ (bağlantı şeridin altında, hiçbir davranış iddiasına bağlı değil).
- **Üretim:** tezgah F60-F65 × ~30 sn; G1–G4 durağan kareleri, cam, su ÇIKTI; şerit HTML 0,2 gün dahil efor 0,5 gün.
- **Telefon:** Şerit 3 satır dikey yığın; blok sırası alt-orta.
- **Risk:** Cümle bilinçli yok: ‘Kuru blok suda yüzer’ kaldırıldı (kaynaksız). Yüzme onayı gelse bile cümle ‘yüzer’ yerine kaynaklı ifadeyle yazılır (ör. ‘Yoğunluk 300–600 kg/m³’). G3 ve ara yoğunluk rakamı yazılmaz; halka merkezi G2 üst yüzündeki gözenekle hizalı (t=101 makro-çıkış buradan açılır).
#### t=101 (1:41) · 2222 vh · p=0.79
- **Kare:** Blender makro-çıkış F66-F71 (halka açılışı 2B F64-F67)
- **Görsel:** Halkanın içinde gözenekli yüzey makro doldurur; kamera gözenekten geri çekilir: gözenekler küçülür, numune küp beyaz fonda belirir.
- **Efekt:** Ters dalış (lens 15→50 mm), odak çekme; şerit 0,4 sn'de solar; beyaz stüdyo, küpün altında yumuşak temas gölgesi.
- **Etkileşim:** Geri çekilirken gözenek halkaları küçülüp küp yüzüne oturur: son tıklanabilir an.
- **Pazarlama:** Köprü: küçücük detay, büyük ürünün parçası.
- **Üretim:** makro F66-F71 × ~60 sn; kamera eğrisi s2_gozenek dalışının tersi, efor 0,3 gün.
- **Telefon:** Küp alt-orta.
- **Risk:** Sözleşme: ‘gözenekten geri çekilme’. Tezgâh→gözenek 2B halka ile (s3 içi yeni); halka merkezi blok yüzündeki gözenekle hizalanmalı.
#### t=102 (1:42) · 2244 vh · p=0.86
- **Kare:** Blender cikis F72-F77 (2B ölçek zinciri F72-F74)
- **Görsel:** Küp, bloğun yüzündeki bir kesikte duruyor; kamera geri çekilirken tam boy blok açılır, paletin üst sırasında yer alır; lime streç alttan sarılır.
- **Efekt:** Ölçek zinciri: küp→blok yüzü, 50× üstel zoom, hizalı çapraz erime. Streç: z-eşikli spiral maske, kırışık bump, mat lime.
- **Etkileşim:** Paletteki lime streç pini: ‘Ege Gazbeton’ kartı (lime streçli paletler: Söke ve İzmir'den sahaya).
- **Pazarlama:** Lime streç, marka imzası, ilk kez büyük ve net.
- **Üretim:** cikis F72-F77: stüdyoda blok + palet ~35 sn/kare; streç sarma 4 kare; 2B zincir tools/s3_birlestir.py 1 gün.
- **Telefon:** Palet dikey kadrajda ortada; kamera aşağıdan yükselir.
- **Risk:** Küp-kesik ölçek hizası (altın kare F72); streç yalnız lime, palet tahtası ahşap.
#### t=103 (1:43) · 2266 vh · p=0.93
- **Kare:** Blender cikis F78-F83 (+F84 = s4 F000)
- **Görsel:** Beyaz stüdyo Söke stok sahasının sabah ışığına açılır: streç filmli palet yığını, arkada paletler ve fabrika silueti; kamera geri çekilmeye devam eder.
- **Efekt:** Palet merkezli radyal erime (0,45 sn): beyaz zemin→çakıl, boşluk→sabah göğü; alçak güneş uzun gölge, hafif sis; streç parlar.
- **Etkileşim:** ‘Söke fabrikası’ pini belirir (dil.js fabrika kartı); s4'te sürer.
- **Pazarlama:** Üretimden sahaya: ürün mühürlendi, yola çıkıyor; ‘Söke & İzmir’ s4'te.
- **Üretim:** cikis F78-F84: saha s4_yol.py stok sahası, ~40 sn/kare × 7; F84 ortak kare (tek render, iki perde).
- **Telefon:** Palet yığını alt-orta, fabrika silueti üstte.
- **Risk:** F84 = s4 F000 birebir (kamera, ışık, sis, streç); s4 planıyla mutabakat. Pin s4'ün ilk vuruşuyla çakışmamalı.

**Geçiş ve üretim notu (s3).** Satırlar t=90..103 (14 satır; t=104 s4'ün ilk saniyesi). p=(t-90)/14 (satır başı). Kare: 6 kare/sn, n=85 kare (F00..F84), satır t = F[6(t-90)]..+5; p*(n-1) ile F84 tam p=1'e düşer, kayma yok. Telefon her 2. kare (EGE_MINSTEP=2, 43 kare, F84 dahil). Kare haritası: makro F00-F41 (yüzey, dalış, hücre içi, hayalet ağ, kesit yüzü), tezgah F42-F65 (nötr tezgâh: A1 duvar parçası F42-F53, yan yana G1/G2/G4 blok F54-F65; alev, tank, su YOK), makro-çıkış F66-F71, cikis F72-F84 (blok, palet, saha). Kamera/sahne: s2→s3: s2 planı 'f095-099 ön-ısınma, s3 f000 = s2 f100' dedi; F00 bu yüzden s2 son karesinin bir adım ilerisi, kahraman gözenek (CHAIN[0]) ekran merkezinde, aynı dalış eğrisi, beyaz-gri stüdyo, vinyet 0,2. s3→s4 (çıkış 101-103): t=101 gözenekten geri çekilme, küp; t=102 küp→blok→palet, lime streç sarılır; t=103 beyaz stüdyo Söke stok sahasının sabah ışığına erir. F84 = s4 F000 (streç filmli palet yığını, kamera geri çekilmeye devam eder); s4 planıyla ortak kare (tek render). Ölçek atlamaları (gözenek→duvar, tezgâh→gözenek) lime halka merceğiyle (2B clip-path, 0,5 sn = 11 vh). Web vuruşları (p): başlık+cümle 0,00-0,28 (başlık 0,00; cümle 0,07); ısı cümlesi 0,29-0,49 (λ rakamı 0,43); A1 0,50-0,63; yoğunluk+şerit 0,64-0,78 (şerit 0,71; bu aralıkta cümle yok); çıkış 0,79-1,01 metinsiz. Aynı anda en çok 1 başlık/rakam + 1 cümle, yeni sözcük en çok 3/sn. Işık ritmi: aydınlık makro → nötr açık-gri tezgâh (t=97-100, tek ışık düzeni, pozlama sabit) → beyaz stüdyo → sabah. Lime YALNIZ ürün halkası/pini ve streç; ısı turuncu (yalnız t=94-95 gözenek ölçeği), hava ışığı sıcak beyaz. DENETİM KARARI (t=97-100): A1 sahnesinde alev, kor, ısıl degrade, 'serin yüz' ve etiketi YOK (yangın direnci EN 13501-2 belgesi yok; ima edilmez); yalnız 'A1 · yangına tepki sınıfı · EN 13501-1 · CE belgeleri' kartı + sınıf merdiveni SVG + nötr tezgâh/blok görseli. 'Kuru blok suda yüzer' sahnesi (cam tank, su, kaustik, salınım) YOK: föy/CE belgelerinde ifade yok; yerine tezgâhta yan yana G1/G2/G4 blok + '300–600 kg/m³ · yoğunluk aralığı' + λ · A1 · 300–600 şeridi. s3_tezgah.py'nin alev/flipbook ve tank/yüzme kısımları, yangın direnci belgesi ve yüzme onayı gelmeden BAŞLAMAZ (önce sınıf merdiveni SVG + kart yedeği). ayarlar.js: s3 boy 308 vh; s2→s3 ve s3→s4 eşleşen kare geçişlerinde GECIS 70 yerine 22 vh önerilir. Geri kaydırınca tüm dizi çift yönlü çalışır.

**Gereken yeni işler (s3):**
- blender/s2_gozenek.py v3: 85 kare (6 kare/sn); kamera anahtarları saniyeye bağlı (dalış F00-F17, hücre içi F12-F23, geri çıkış ve kesit yüzü F24-F41, çıkış F66-F71); beyaz-gri stüdyo; hava ışığı sıcak beyaz; meta çapaları (gözenek merkezleri, kesit dörtgeni). ~1 gün.
- Hayalet hücre ağı: en büyük 120 gözenek küre, s1_urun.gecis_malzeme röntgen malzemesi, F18-F27 hayalet→katı karışımı. ~0,5 gün.
- tools/isi_akis.py: yüz kesitinde iletim çözümü + akış fonksiyonu konturları. Prototip plan/_gz/isi_test3.py (400×400 ızgara, 2 sn, 28 çizgi, 82 KB; 2 haneye yuvarlanınca ≈40 KB), çizgiler gözenek boyunlarında sıkışıyor, gözeneğe giren parçalar kırpılacak. Çıktı isi_akis.js (file:// için JS). ~0,75 gün. stil_r4.sahne_isi 3B ok çubukları bırakılır (kaba).
- Web gozenek.js: SVG gözenek halkaları/pinleri, ısı çizgileri (homografi.js) + 120 damla canvas (hız 1,0→0,25), A1 sınıf merdiveni SVG (7 basamak, A1 vurgulu) + kart, G1/G2/G4 sınıf etiketleri, rakam şeridi, halka mercek geçişi (clip-path). Alev flipbook, ısıl degrade ve G1-G4 film içi kaydırıcısı kapsam dışı. Bütçe ≤0,8 ms/kare, DPR ≤1,25, WebGL yok. ~2 gün (önceki ~2,5 gün).
- blender/s3_tezgah.py (yeni): nötr açık-gri tezgâh, F42-F65: 4 sıra duvar parçası (F42-F53, ileri dolly) + yan yana G1/G2/G4 blok (F54-F65, pan ve yükselme), meta çapaları (duvar, a1_kart, blok_g1/g2/g4, G2 üst yüz gözeneği). Alev, cam tank, su, kaustik, sönümlü salınım KAPSAM DIŞI: alev kısmı yangın direnci (EN 13501-2) belgesi, tank/yüzme kısmı yüzme onayı + föy/CE kaynağı gelmeden BAŞLAMAZ; stil_r5 sahne_alev/sahne_yuzer taslakları dondurulur. ~1 gün (önceki ~2,5 gün).
- A1 sahnesi yedeği (alev flipbook'un yerine): sınıf merdiveni SVG (A1 A2 B C D E F; harfler EN 13501-1'den, teyit gerekli) + ‘A1 · yangına tepki sınıfı · EN 13501-1 · CE belgeleri’ kartı; teyit gelmezse yalnız A1 rozeti + kart. Alev flipbook (16 kare RGBA WebP) DÜŞTÜ; yangın direnci belgesi gelirse yalnız bloğa değmeyen, süresiz, etki göstermeyen şematik biçimde ayrı karar olarak yeniden açılır. SVG işi gozenek.js içinde ~0,25 gün.
- blender/s3_cikis.py (yeni): numune küp→blok kesiği, blok + palet, lime streç sarma (spiral maske), stüdyo→saha radyal erime; F84 = s4 F000 (s4_yol.py stok sahası kamera ucu). ~1,5 gün.
- tools/s3_birlestir.py (2B): halka mercek (F40-F43, F64-F67), ölçek zinciri (F72-F74), radyal erime (F80-F83), 85 kare dizi, WebP + meta (kesit, duvar, a1_kart, blok_g1/g2/g4, gözenek çapaları). ~1 gün.
- dil.js i2.*: kısa metinler (2 yeni cümle: t=91, t=94) + kartlar (isi_yolu, a1, yogunluk; yüzme kartı YOK), TR/EN, kaynak satırları. ayarlar.js s3 boy 308 vh, GECIS 22; index.html SAHNE 3 vuruşları yukarıdaki p aralıklarıyla. ~0,5 gün.
- Üretim özeti (tahmini, s2d günlüklerinden): d ≈75 dk (makro 48 kare ~65 sn, tezgah 24 kare ~30 sn, cikis 13 kare ~38 sn; flipbook, G1-G4 durağan kareleri, tank çıktı); m ≈38 dk. Önceki plan d ≈110 dk, m ≈55 dk. Kare yükü ≈9 MB (d) / ≈3,5 MB (m) (üst sınır; flipbook ve G1-G4 durağan kareleri çıkınca bir miktar düşer).

### s4 · Yol: fabrikadan sahaya — 104–120 sn

**Amaç.** Gurur, ölçek, güven. Blok artık ürün: sabah ışığında lime streçli paletler, forklift, kayış, kantar; s0'da evin önünden geçen tırın doğduğu yer. Üç onaylı rakam (2 fabrika, kendi kireç tesisi 200 t/gün, 1.100.000 m³) görsel kanıtla gelir. Çıkışta tır yola çıkar, kamera yükselir, saha haritada iki lime noktaya dönüşür; 'peki nereye gidiyor?' sorusu s5'e köprü kurar.

#### t=104 (1:44) · 2288 vh · p=0.0
- **Kare:** Blender s4_yol 'yol' F000-005 (F000 = s3 son karesi)
- **Görsel:** Lime streçli palet yığını (2-3 palet) yakın plan: bloklar film ardından seçilir, sarım kırışıkları ışıldar. Kamera 1,6 m'den geri çekilmeye devam eder.
- **Efekt:** Alçak sabah güneşi (13°, sıcak) filmden geçip içten parlar; çiy damlaları, ışıkta toz; DOF f/2,8. Stüdyo beyazı sıcak sabaha çoktan erimiş.
- **Etkileşim:** Kaydırma oku nabız atar; imleç eğimi (EGIM_PX 14) filmdeki parıltıyı kaydırır.
- **Pazarlama:** Lime streç = Ege Gazbeton imzası: blok artık ambalajlı ürün.
- **Üretim:** palet() v2 + streç gölgelendirici (yeni); 6 kare × ~70 sn (d); 0,5 gün.
- **Telefon:** Palet yığını köşegende; üst %40 anlatım alanı boş.
- **Risk:** F000 s3 t=103 son karesiyle poz, lens, ışık birebir olmalı (altın kare); s3 yazarıyla mutabakat.
#### t=105 (1:45) · 2310 vh · p=0.06
- **Kare:** Blender 'yol' F006-011
- **Görsel:** Geri çekilme sürer: yığın, iki sıra, sonra stok sahası. Lime streçli paletler ızgara gibi uzar; ufukta Söke holünün testere dişi çatısı ve bacası belirir.
- **Metin:** 07 · Yol — Fabrikadan sahaya.  
  *EN:* 07 · On the road — From the plant to the site.
- **Efekt:** Sabah buğusu (kit.sis 0,004) holü yumuşatır; paletler arasından güneş huzmeleri; rack focus palet → hol; lime kenarlarda bloom.
- **Etkileşim:** Başlık belirince kaydırma ipucu söner; imleç konumuna göre hafif parallax eğimi.
- **Pazarlama:** Perde başlığı: fabrikadan sahaya vaadi; lime rengin ilk tekrarı.
- **Üretim:** Stok sahası: 10×5 nizami palet ızgarası (toplu_mesh, ~1 200 palet); 6 kare × ~75 sn.
- **Risk:** Stok ızgarası temsilî; palet adedi ekranda yok.
#### t=106 (1:46) · 2332 vh · p=0.13
- **Kare:** Blender 'yol' F012-017
- **Görsel:** Kamera sağa süzülerek geri çekilir: önde lime paletler, ortada forklift koridora dönüp ilk paleti almaya gelir; uzakta hol ve otoklav buharı.
- **Metin:** Her palet lime streçle sarılır.  
  *EN:* Every pallet is wrapped in lime stretch film.
- **Efekt:** Forklift amber flaşörü 2 Hz yanıp söner; tekerlek altında toz; palet gölgeleri kameraya uzanır; orta planda hafif DOF f/5,6.
- **Etkileşim:** 'palet' noktası halka olarak doğar; tıkla: Lime streç kartı (streç film, kayışla bağlama).
- **Pazarlama:** Kurumsal lime rengi ürüne bağlanır; özenli ambalaj = güven.
- **Üretim:** forklift() yeni model + koridor yolu; 6 kare × ~80 sn; 1 gün (model + hareket).
- **Telefon:** Forklift alt-ortada, palet sıraları köşegende.
- **Risk:** Forklift grafit + amber (yeşil olamaz); kartın 'kayışla bağlanır' ifadesi üretici teyidi gerekli.
#### t=107 (1:47) · 2354 vh · p=0.19
- **Kare:** Blender 'yol' F018-023
- **Görsel:** Kamera alçak (1,4 m), forklift 3/4: çatallar paletin altına girer, mast geriye yatar, palet 30 cm kalkar. Uzak planda yelekli işçi el işareti yapar.
- **Efekt:** Çatal temasında toz kabarır; film gerilip parlar; 4 cm yavaş itme (dolly-in); DOF f/4 forklifte; hidrolik sarsıntı.
- **Etkileşim:** Forklift ve palet üstünde imleç: lime halka vurgusu; kaydırma durursa bacadan buhar sprite'ı döner.
- **Pazarlama:** Düzenli, güvenli saha: iş disiplini görünür.
- **Üretim:** forklift hidrolik animasyonu (mast eğimi, kaldırma) + insan 'isaret' pozu; 6 kare × ~80 sn; 0,5 gün.
- **Risk:** İşçi >=12 m, yüz yok (kural); yelek turuncu (lime değil).
#### t=108 (1:48) · 2376 vh · p=0.25
- **Kare:** Blender 'yol' F024-029
- **Görsel:** Kamera yana geçip tırı boydan gösterir: dorse yarı dolu, forklift ikinci paleti güverte hizasına çıkarır. Arkada hol bandı, silolar ve konveyör.
- **Metin:** 2 fabrika · Söke & İzmir  
  *EN:* 2 plants · Söke & İzmir
- **Efekt:** Yatay dolly parallax'ı: ön palet sırası bulanık kayar; hol lime şeridi güneşte parlar; çatal ve palette hareket bulanıklığı.
- **Rakam · kaynak:** 2 fabrika, Söke ve İzmir (Ege Gazbeton ortak rakamlar)
- **Etkileşim:** 'fabrika' noktası holün üstünde doğar; tıkla: Söke fabrikası kartı (hol, otoklav, silo, kireç tesisi).
- **Pazarlama:** Ölçek: iki fabrika, tek kalite anlayışı.
- **Üretim:** Yatay dolly eğrisi + hol çatı çapası (kit.project); 6 kare × ~85 sn.
- **Telefon:** Tır dikeyde köşegen; rakam kartı üstte.
- **Risk:** Cümle A bu saniye kalkar, yerini rakam kartı alır (1 başlık + 1 öğe); tek kaynaklı sayı: 2.
#### t=109 (1:49) · 2398 vh · p=0.31
- **Kare:** Blender 'yol' F030-035 (altın kare F030)
- **Görsel:** Son palet dorseye iner; işçi kayışı yükün üstünden atar. Yakın plan: amber kayış köşe koruyucuya oturur, çırçır gerilir; streç filmde gerilme çizgileri.
- **Efekt:** Kayış yayı ve titreşimi; çırçır metalinde parıltı; film kenarında lime parlama; toz zerreleri. SVG 'yük bağlama' çizgisi kayış boyunca çizilir.
- **Etkileşim:** Kayış üstünde imleç: çizgi yeniden çizilir (draw-on 0,6 sn); 'Kayış' çipi sonraki saniyede tıklanır olur.
- **Pazarlama:** Taşıma özeni: ürün sahaya sağlam ulaşır.
- **Üretim:** kayis() eğri + çırçır mesh + atış animasyonu (8 anahtar kare); 6 kare × ~90 sn; 0,75 gün.
- **Telefon:** Çırçır makrosu ortada; daha yakın kırpma.
- **Risk:** Kayış amber (lime değil); kayış sayısı ve dizilimi temsilî, ekranda sayı yok.
#### t=110 (1:50) · 2420 vh · p=0.38
- **Kare:** Blender 'yol' F036-041 + SVG taşıma grafiği
- **Görsel:** Yüklü tır boydan, neredeyse sabit kadrajda: iki sıra lime streçli palet, amber kayışlar, kabinde lime şerit. SVG çipleri 'Streç' ve 'Kayış' çizilir (kahraman kare).
- **Metin:** Yük bağlanır, tır yola çıkar.  
  *EN:* Load secured, the truck rolls out.
- **Efekt:** Leader çizgileri çizilir (stroke-dashoffset); motor çalışır: kabin titrer, egzoz buharı; güneş film üstünde kayar.
- **Etkileşim:** 'tir' etiketi ('Ege Gazbeton') tırı izlemeye başlar; tıkla: kart. Çipler tıklanınca ilgili parça lime halkayla vurgulanır.
- **Pazarlama:** Reklam karesi: lime şeritli beyaz tır, marka taşıyıcısı; s0'da evin önünden geçen aynı tır.
- **Üretim:** SVG .eg-ek (leader + çip) + meta çapaları palet_ust, kayis_a; 6 kare × ~85 sn; web 0,5 gün.
- **Telefon:** Çipler tırın altında iki satır.
- **Risk:** Plaka boş/okunmaz, 3B'de yazı yok; kabin logosu s0 sorusuna bağlı (şimdilik yok).
#### t=111 (1:51) · 2442 vh · p=0.44
- **Kare:** Blender 'yol' F042-047
- **Görsel:** Tır yavaşça kalkar: bariyer kolu yükselir, kantar plakasından geçer. Kamera tırla aynı hızda yan takibe başlar (kabin hizası, 32 mm); tekerlekler döner, dorse salınır.
- **Efekt:** Hareket bulanıklığı: arka plan kayar, tır net; tekerlek dönüşü ve süspansiyon salınımı; egzoz bulutu; gölge tırla kayar.
- **Etkileşim:** Tır etiketi hareketle kayar; kaydırma hızı ile tır hızı 1:1 hissedilir.
- **Pazarlama:** 'Yola çıkış' anı: s0'da sokaktan geçen tırın başladığı yer.
- **Üretim:** Tır anahtar kareli hareket (hız eğrisi, tekerlek dönüşü, süspansiyon) + bariyer + kantar; 6 kare × ~95 sn; 0,75 gün.
- **Telefon:** Kamera tırın 3/4 ön açısında; kabin üstte.
- **Risk:** Hareket bulanıklığı + 6 kare/sn çapraz geçişte hayalet yapabilir: sınama; gerekirse 8 kare/sn (açık soru 3). Bariyer sarı-siyah, kantar göstergesiz.
#### t=112 (1:52) · 2464 vh · p=0.5
- **Kare:** Blender 'yol' F048-053 (altın kare F048)
- **Görsel:** Yan takip sürer: tır hızlanır, kamera 9 m güneyde aynı hızda; fabrikanın yan cephesi, silolar ve konveyör akıp gider; lime stok ızgarası geride küçülür.
- **Efekt:** Üç parallax katmanı: bulanık çit direkleri, net tır, yavaş hol; reflektör bantları ve yan lambalar güneşte parlar; yolda toz izi.
- **Etkileşim:** 'fabrika' noktası holle birlikte kayar; tıklanırsa kart açılır, kaydırma sürer.
- **Pazarlama:** Tırın ayrıntı zenginliği (kabin, dorse, jant) marka kalitesini taşır.
- **Üretim:** Tır v3 yakın LOD (lastik sırtı, hava körüğü, çamurluk perdesi); 6 kare × ~100 sn (en ağır saniye).
- **Risk:** Şeffaf streç + transmission_bounces >=8 pahalı: bu saniye ~10 dk/varyant; gerekirse DOF kapalı.
#### t=113 (1:53) · 2486 vh · p=0.56
- **Kare:** Blender 'yol' F054-059
- **Görsel:** Tır çıkış kapısından geçip doğuya, sabah güneşine döner. Kamera takipten ayrılır; yavaşça yükselir (3 → 10 m) ve geri süzülür; tır sağda küçülür.
- **Efekt:** Karşı ışık: dorse kenarları ve streç film kontur ışığıyla parlar; hafif lens parlaması (Glare ghosts); yolda toz izi.
- **Etkileşim:** 'tir' etiketi küçülür, tırı izlemeyi sürdürür; kaydırma oku yeniden nabız atar.
- **Pazarlama:** Ürün sahaya gidiyor: tır, hikâyeyi s5'e taşıyan nesne.
- **Üretim:** Kamera: yan takipten vinç (crane up) eğrisine C1 sürekli geçiş; 6 kare × ~85 sn.
- **Risk:** Takipten yükselişe hız sürekliliği (kesik olmamalı); parlama zayıf kalmalı.
#### t=114 (1:54) · 2508 vh · p=0.63
- **Kare:** Blender 'yol' F060-065
- **Görsel:** Kamera 10 → 36 m yükselip kule ve baca tarafına dönerek 3/4 avluyu açar: hol, silolar, kireç kulesi ve lime bantlı baca; tır yolda küçülür.
- **Metin:** 200 t · günlük kireç tesisi kapasitesi  
  *EN:* 200 t · lime plant capacity per day
- **Efekt:** Kule tabanında lime halka dalgası; bacadan beyaz buhar (hacim); derinlik sisi; leader çizgisi baca bandına uzanır. Pitch 8° → 30°.
- **Rakam · kaynak:** 200 t/gün kireç tesisi, Söke (Ege Gazbeton ortak rakamlar)
- **Etkileşim:** 'kirec' noktası kule/baca üstünde doğar (s2 kartı yeniden kullanılır); sayaç 0 → 200 kaydırmaya bağlı.
- **Pazarlama:** Fark: karışımın bağlayıcısı kireç kendi tesisimizde üretilir.
- **Üretim:** Kireç kulesi + baca v2 (çelik karkas, sac cephe, boru köprüsü), buhar hacmi; 6 kare × ~90 sn; 1 gün.
- **Telefon:** Kule dikeyde üstte; sayaç altta.
- **Risk:** Kaynak teyitli (kirec kartı); baca bandı lime = fabrika şeridi, sac gövde beyaz-gri.
#### t=115 (1:55) · 2530 vh · p=0.69
- **Kare:** Blender 'yol' F066-071 (altın kare F066)
- **Görsel:** Kamera 36 → 124 m: tüm saha açılır; testere dişi çatı, otoklav sırası buharıyla, silolar, konveyör köprüsü, lime stok ızgarası. Pitch 30° → 65°, yarım orbit.
- **Metin:** 1.100.000 m³ · üretim kapasitesi  
  *EN:* 1,100,000 m³ · production capacity
- **Efekt:** Stok ızgarasında lime bloom; otoklav buhar şeritleri rüzgârda yatar; uzun sabah gölgeleri; hol lime şeridi kamera dönerken çizgiye dönüşür.
- **Rakam · kaynak:** 1.100.000 m³ üretim kapasitesi (Ege Gazbeton ortak rakamlar); süre ibaresi teyit gerekli
- **Etkileşim:** 'otoklav' noktası (s2 kartı); sayaç 0 → 1.100.000 kaydırmaya bağlı; hover'da silo/otoklav adı.
- **Pazarlama:** Güç: kapasite rakamı tüm fabrikanın üstünde okunur.
- **Üretim:** otoklav(), silo(), konveyör v2 (fabrika_kit, s2 ile ortak); stok ızgarası; 6 kare × ~110 sn (en geniş kadraj).
- **Telefon:** Saha dikeyde çapraz; sayaç üstte.
- **Risk:** Ekranda yalnız 'm³ üretim kapasitesi' yazar; yıllık mı, teyit gerekli.
#### t=116 (1:56) · 2552 vh · p=0.75
- **Kare:** Blender 'yol' F072-077
- **Görsel:** Kamera 124 → 420 m, pitch 65° → 90°: saha tam tepeden; testere dişi çatı desen olur, hol bandı lime dikdörtgen çizer, stok lime nokta ızgarası; tır yolda lime çizgi.
- **Efekt:** Perspektif düzleşir (24 → 30 mm); yol ve çit çizgileri grafikleşir; ufuk sisi açılır; ince vinyet 0,15.
- **Etkileşim:** 'fabrika' noktası holün merkezinde; 'tir' etiketi yolda küçük okla; sayaçlar tamamlanmış.
- **Pazarlama:** Grafik sadelik: lime = Ege Gazbeton, ölçek hissi.
- **Üretim:** Kamera: logaritmik irtifa, pitch smoother; arazi 6 km'ye genişler; 6 kare × ~70 sn.
- **Telefon:** Hol dikeyde çapraz; metin üstte.
- **Risk:** Arazi 1 600 m kutu: ~900 m üstünde kenar görünür, 6 km'ye genişletilmeli.
#### t=117 (1:57) · 2574 vh · p=0.81
- **Kare:** ÇIKIŞ 1 · Blender 'yukselis' Z F078-083 (420 → 900 m) + eğri lime halka
- **Görsel:** Tam tepeden saha küçük bir levha: lime saha halkası holün merkezinden çizilerek sahayı çevreler; tır sağ kenara lime nokta olarak kayıp çıkar.
- **Metin:** Tır yola çıktı. Peki nereye gidiyor?  
  *EN:* The truck is on its way. So where is it headed?
- **Efekt:** Halka (eğri, bevel_factor_end) 0,8 sn'de çizilir + bloom; radyal zoom bulanıklığı artar; arazi sisle yumuşar.
- **Etkileşim:** Tır etiketi çıkar (tır kadraj dışı); 'fabrika' noktası halka merkezinde kalır; kaydırma oku nabız atar.
- **Pazarlama:** Merak köprüsü: s5 vaadi (dünya); s0/s1/s2 sonlarındaki 'Peki...' ritmi.
- **Üretim:** Blender Z kareleri (6 × ~60 sn); eğri halka 0,25 gün.
- **Telefon:** Halka alt-ortada; soru üstte.
- **Risk:** Halka rengi ve kalınlığı s5'in İzmir halkasıyla aynı motif (kit.halo_ring); lime = saha/bizim, kural tamam.
#### t=118 (1:58) · 2596 vh · p=0.88
- **Kare:** ÇIKIŞ 2 · Z F084-089 + N nokta dalgası + B (bölge) çapraz (altın kare F084)
- **Görsel:** Yükselme hızlanır: saha 900 m → 20 km. Gerçek arazi sis içinde yarı-ton noktalara dönüşür; nokta dalgası halkadan dışa yayılır; kıyı ve körfez nokta/boşluk olarak belirir.
- **Efekt:** Piksel → nokta dönüşümü (parlaklık = nokta yarıçapı); sis → koyu slate zemin; radyal zoom bulanıklığı; Söke halkası ölçeklenir.
- **Etkileşim:** Yükselme kaydırma kadar hızlı; oku nabız atar. Hotspot yok (geçiş akışı bozulmasın).
- **Pazarlama:** Gerçek sahadan haritaya geçiş: yerel üretim, geniş erişim mesajı.
- **Üretim:** tools/s4_birlestir.py N (numpy, ~0,4 sn/kare) + B kareleri (~25 sn/kare); 0,75 gün.
- **Telefon:** Nokta ızgarası aynı; kadraj dikey.
- **Risk:** Çift görüntü kalmamalı: Z/N/B tek zaman çizelgesiyle birleştirilmiş kare olarak yazılır, JS erimesine bırakılmaz.
#### t=119 (1:59) · 2618 vh · p=0.94
- **Kare:** ÇIKIŞ 3 · B 'bolge' F090-095 (≈100 → 300 km); F095 = s5 f000
- **Görsel:** Tepeden Ege: gri kara noktaları, lime Türkiye kıyısı, gri adalar, körfez koyu boşluk; Söke (güney) ve İzmir (kuzey) iki lime halka nabız atar; kamera küreye doğru çekilmeye hazırlanır.
- **Efekt:** İki halka 0,3 sn arayla yanar, nabzı genişler; kıyı noktaları lime kısmen parlar; koyu slate arka plan; yıldız tozu başlar.
- **Etkileşim:** 'fabrika' (Söke) ve 'kaynak' (İzmir) noktaları tıklanır; kartlar s5 ile aynı.
- **Pazarlama:** Köprü: iki lime nokta = 2 fabrika; hemen ardından beş kıta (s5).
- **Üretim:** s4_dunya.py 'bolge' kipi: land-10m + countries-10m yoğun nokta yaması, 6 kare × ~30 sn; 1 gün (veri + kip, s5 ile ortak).
- **Telefon:** Dikey kadrajda kıyı çaprazlanır; iki halka orta hatta.
- **Risk:** SEAM: s5 f000 ile birebir (kadraj, nokta yoğunluğu, halka rengi); H_GIRIS ~0,1 R gerek. İzmir fabrikasının ilçesi bilinmiyor: nokta temsilî, teyit gerekli. Ülke sınırı çizilmez.

**Geçiş ve üretim notu (s4).** Satırlar t=104..119 (t=120 s5'in ilk saniyesi). p=(t-104)/16 (satır başı); τ=t-104. Kare: 6 kare/sn, 96 kare, f=(t-104)*6..+5, u=f/95; telefon her 2. kare (EGE_MINSTEP=2). Kaynak kodları: Y = s4_yol 'yol' (F000-077), Z = 'yukselis' tepe kareleri (F078-089), N = yarı-ton nokta dalgası (tools/s4_birlestir.py), B = s4_dunya 'bolge' kipi (F084-095). s3→s4: s3 çıkışı (t=101-103) gözenek→blok→paletteki bloklar→palet yığını; F000 = o son kare (poz, lens, ışık birebir; sabah ışığı s3 çıkışında oturur). Zamanlama (τ): 0-2 yığın→saha (geri çekilme), 3-5 forklift ve yükleme, 6 hazır tır (kahraman kare + taşıma grafiği), 7-9 çıkış ve yan takip, 9-13 vinç yükselişi (irtifa 3→10→36→124→420 m, pitch 8°→90°), 13-15 çıkış geçişi (420 m→900 m→bölge ~300 km). Kamera: τ0 1,6 m f/2,8 50 mm; τ2 14 m 35 mm; τ3-5 12→9 m z1,4 40 mm; τ6 20 m 28 mm; τ7-9 yan takip 9 m z1,6 32→40 mm; τ10-11 24 mm. Saha v2 (s4_yol): tır şeridi y=-22, stok y -46..-34 (tırın güneyi), hol y>=-9, otoklavlar hol batısında, çıkış kapısı + kantar doğuda x≈62, kamu yolu doğuya düz. Işık: sabah güneşi 13°, azimut 125° (GD), sıcak (1,0;0,82;0,62), AgX. Lime YALNIZ ürün/marka: streç, tır şeridi, hol ve baca bandı, saha ve Söke/İzmir halkaları; forklift grafit+amber, kayış amber, yelek turuncu, çelik beyaz-gri. Metin düzeni s1/s2 ile aynı: metin belirdiği saniyeye yazılır, sonrası '' ve ekranda kalır; en çok 1 başlık + 1 cümle/rakam, yeni sözcük en çok 3/sn. Web vuruşları (p): başlık 0,06-0,81; cümle A 0,13-0,25; rakam 2 0,25-0,38; cümle B 0,38-0,50; rakam 200 t 0,63-0,81; rakam 1.100.000 0,69-0,81; söz 0,81-1,01. ayarlar.js: s4 boy 260→352 vh; eşleşen kare geçişlerinde (s3→s4, s4→s5) GECIS 22 vh. s4→s5: F095 = s5 f000 (tepeden İzmir bölgesi: kıyı, körfez, iki lime halka); s4_dunya H_GIRIS 0,42→~0,1 R (genişlik ~300 km) + yerel yoğun nokta yaması gerekir, s5 yazarıyla mutabakat.

**Gereken yeni işler (s4):**
- s4_yol.py v2: saha yerleşimi v2 (tır şeridi, güneyde stok, batıda otoklav, kapı + kantar + bariyer), 96 kare, anahtar kareli hareket + hareket bulanıklığı, DOF, 13° sabah gökyüzü, kit.sis + kit.dust, arazi 6 km, çapalar palet/tir/fabrika/kirec/otoklav. ~1,5 gün.
- fabrika_kit.py cephe v2 (s2 ile ortak): sandviç panel (Wave bump), kirli alt şerit (AO/Pointiness), şerit pencere, testere çatı (polikarbon + sac), yükleme rampası + sundurma, bollard, oluk/iniş borusu, havalandırma türbini, beton saha (derz, lastik izi, yağ lekesi, boyalı çizgi), çit. ~1,5 gün.
- Ekipman v2: silo (şerit dikiş, merdiven kafesi, korkuluk, filtre kutusu), konveyör galeri (kafes kiriş + sac), otoklav dış görünümü (kılıf bantları, kilit segmentleri, boru/vana, tahliye bacası, vagon), kireç kulesi + baca (çelik karkas, boru köprüsü, lime bant). ~1,5 gün.
- Buhar/atmosfer: otoklav ve baca için 3 hacim (Principled Volume + gürültü), zemin sisi; 2B buhar sprite katmanı (boşta nefes, <=0,3 ms) için meta 'ankraj' alanı (hotspots'tan ayrı: nokta düğmesi üretmesin). ~0,75 gün.
- forklift() (gövde, iki kademeli mast + zincir, çatal, kafes, amber flaşör, tekerlek) + hidrolik animasyon; insan.py 'isaret' ve 'kayis' pozları, 3 kişi orta/uzak plan (yüzsüz, baret, turuncu yelek). ~1,5 gün.
- Taşıma grafiği: palet() v2 (ahşap palet, şaşırtmalı blok katları, köşe koruyucu), streç gölgelendirici v2 (şeffaf lime, sarım bandı, gerilme çizgisi, çiy), kayis() (yassı eğri + çırçır + atış), dorse bağlama aksamı (baş duvar, ankraj halkası, yan kolon cebi), boş plaka. ~1,5 gün.
- Tır v3 (s0 'tır v2' üzerine, yakın LOD): hava körüğü/yay, ikiz arka lastik + sırt bump, jant dönüşü, çamurluk perdesi, reflektör bantları, ayna kolu, ızgara lamelleri, rüzgârlık, yüzsüz kabin silüeti. ~1 gün.
- Çıkış: s4_yol 'yukselis' (Z) + eğri lime halka; tools/s4_birlestir.py yarı-ton nokta dalgası (numpy) ve Z/N/B birleştirme. ~0,75 gün.
- s4_dunya.py 'bolge' kipi (s5 ile ortak): world-atlas land-10m + countries-10m ile 36-40°K × 25-29°D yoğun nokta yaması (~0,04°), Söke/İzmir halkaları, H_GIRIS ~0,1 R; Türkiye lime yalnız gerçek poligon. ~1 gün.
- Web: taşıma grafiği SVG (.eg-ek leader + çip draw-on), kaydırmaya bağlı sayaçlar (2, 200, 1.100.000), tır takip etiketi, palet/fabrika/kirec/otoklav/kaynak noktaları, buhar sprite, vuruş parçalama (başlık, cümle A/B, 3 rakam, söz). ~1,5 gün.
- dil.js: h4.metin → cümle A/B, h4.soz, NOKTALAR.palet (TR/EN); ayarlar.js s4 boy 352, GECIS 22; index.html SAHNE 4 p pencereleri. ~0,5 gün.
- Toplam render: d ≈ 96 × ~80 sn ≈ 2,2 sa, m (EGE_MINSTEP=2) ≈ 1,1 sa; kare yükü ≈ 5 MB (d, tahmini). Altın kareler: F000, F030, F048, F066, F084, F095.

### s5 · Dünya: Ege'den 5 kıtaya — 120–136 sn

**Amaç.** Duygu: yerellikten güvene. İki fabrikanın ışığı dünyaya yayılır. Mesaj: Ege'de üretilen, 5 kıtada kullanılan ürün; 25+ ülke · 5 kıta (ihracat bölümü). Karanlık küre kıta kıta yanar; sonuç sakin, parlak, güven veren bir ışık ağı. Öğretici: fabrikaların yeri, Türkiye silüeti, lime yayın paleti temsil ettiği, beş kıtanın sayılması.

#### t=120 (2:00) · 2640 vh · p=0.0
- **Kare:** Blender bolge F000-F011 (F000 = s4 son karesi)
- **Görsel:** Nadir kamera 200 km yükseklikte: İzmir Körfezi ve Karaburun ince nokta dokusunda; deniz koyu ve boş, kara serin beyaz noktalar. Yükseliş yavaş başlar.
- **Efekt:** s4 ile aynı sabah ışığı: noktaların uzun yumuşak gölgeleri; İzmir'den tek halka dalgası dışa yayılır (nokta boyu); kıyıda ince ışıma.
- **Etkileşim:** İzmir iğnesi (lime) nabız atar; tıklayınca 'Söke & İzmir' kartı (mevcut nokta: kaynak).
- **Pazarlama:** Kök: hikâye Ege'de başlıyor. Sessiz, güven veren açılış; lime yalnız fabrika iğnesinde.
- **Üretim:** bolge kipi, L0 nokta ızgarası (1 km, ~60 bin nokta): 12 kare × ~75 sn ≈ 15 dk (d), 6 kare × ~35 sn ≈ 3,5 dk (m).
- **Telefon:** Dikeyde Aliağa-İzmir-Söke aynı kadrajda (260 km yükseklik); iğne etiketleri alt yarıda.
- **Risk:** F000 s4 son karesiyle birebir olmalı (ışık yönü, nokta dokusu, kadraj): altın kare onayı. Kıyı Natural Earth 10 m (kamu malı); körfez içinde 2-3 km sapabilir.
#### t=121 (2:01) · 2662 vh · p=0.06
- **Kare:** Blender bolge F012-F023
- **Görsel:** 450→1.500 km: Söke güneyde, Aliağa kuzeyde kadraja girer; kıyı ve Ege adaları genişler. İzmir ve Söke iğneleri lime halkayla yanar, ince ışık direği uzar.
- **Metin:** 08 · Dünya — Ege'den dünyaya.  
  *EN:* 08 · World — From the Aegean to the world.
- **Efekt:** Nokta aralığı 1 km→10 km'ye birleşir (L0→L1, 0,5 sn); kamera önünden ince bulut örtüsü geçip geçişi saklar; başlık 12 px yükselir.
- **Etkileşim:** İğneler üstüne gelince 'Söke', 'İzmir' etiketi belirir; tıklanır kart. Aliağa/Alsancak etiketleri teyit gelene dek kapalı.
- **Pazarlama:** Başlık duyguyu kurar: yerel kökten küresel yola. İki fabrika = iki lime iğne (üretimin sahibi biziz).
- **Üretim:** L0→L1 geçişi (12 kare) + bulut örtüsü düzlemi (kamera önü, Noise alfa): 12 kare × ~75 sn ≈ 15 dk (d), 6 kare × ~35 sn ≈ 3,5 dk (m).
- **Telefon:** Başlık üstte 2 satır; iki iğne ve etiket alt yarıda.
- **Risk:** Liman etiketleri kaynaksız (teyit gerekli). Web'de İzmir fabrikası Bornova görünüyor (3. taraf): iğneler şehir düzeyinde, fabrika konumu iddia etmez.
#### t=122 (2:02) · 2684 vh · p=0.13
- **Kare:** Blender bolge/kure F024-F035
- **Görsel:** 1.500 km→küre: Ege, Akdeniz ve Karadeniz kıyıları görünür (≈3.000 km'de tüm Anadolu); Türkiye'nin gerçek poligonu içindeki noktalar lime yanar, silüet İzmir'den dışa dolar.
- **Metin:** Söke ve İzmir'de yüklenen paletler beş kıtaya ulaşıyor.  
  *EN:* Pallets loaded in Söke and İzmir reach five continents.
- **Efekt:** Lime dalgası coğrafi uzaklıkla yayılır (isik 0,05→1,3); iki iğne söner; L1→L2 geçişi ufuk parıltısında saklanır; cümle yarım sn sonra (122,5) belirir.
- **Rakam · kaynak:** beş kıta (cümlede) — Ege Gazbeton ihracat bölümü
- **Etkileşim:** Fare/parmak 14 px paralaks eğimi (EGIM_PX): noktalar derinlik verir; İzmir 'kaynak' noktası nabız atar.
- **Pazarlama:** Lime Türkiye silüeti = üretimin kaynağı; marka rengi ilk kez büyük ölçekte, ülke adı yazılmadan.
- **Üretim:** L1 seviyesi (50 m poligon, ~26 bin nokta) + L2 küre: 12 kare × ~75 sn ≈ 15 dk (d), 6 kare × ~35 sn ≈ 3,5 dk (m). Dalga: numpy, jeodezik uzaklık.
- **Telefon:** Cümle üstte 3 satır; silüet alt yarıda, dar kadrajda tam sığar.
- **Risk:** Türkiye vurgusu yalnız Türkiye poligonu: Kıbrıs ve Ege adaları nötr kalır. L1 (50 m) ile L2 (110 m) kenar farkı geçiş erimesinde gizlenir.
#### t=123 (2:03) · 2706 vh · p=0.19
- **Kare:** Blender kure F036-F047 (damla: Avrupa F040, Afrika F046)
- **Görsel:** Küre doğar: ufuk iki yandan kıvrılır (d 2,0→3,4), Türkiye lime merkezde. F040'ta Avrupa damlası İzmir'den kuzeybatıya, F046'da Afrika damlası güneye süzülür.
- **Efekt:** Atmosfer fresnel parıltısıyla doğar; yıldızlar belirir; sol yarı gece: soluk sıcak şehir ışıkları; damlanın arkasında lime kuyruk, yay çizilerek uzar.
- **Etkileşim:** Yaylar kaydırmayla çizilir, ileri-geri sarılır: parmakla damlayı hızlandır, yavaşlat.
- **Pazarlama:** Ürünün yola çıkışı: ilk lime ışık İzmir'den ayrılır. Lime = bizim paletin yolu.
- **Üretim:** Küre + bulut kabuğu + gece ışıkları: 12 kare × ~75 sn ≈ 15 dk (d), 6 kare × ~35 sn ≈ 3,5 dk (m).
- **Telefon:** Küre alt yarıda, d ×0,66; damla ve yay kalınlığı ×1,3 (küçük ekranda okunsun).
- **Risk:** Gece ışıkları stilize, veri değil: ışıklı nokta oranı ≤%8, sıcak beyaz (lime değil); gerçek şehir verisi gibi sunulmaz.
#### t=124 (2:04) · 2728 vh · p=0.25
- **Kare:** Blender kure F048-F059 (Avrupa varış F050, Afrika varış F059) + SVG etiket
- **Görsel:** Avrupa damlası F050'de iner: lime halka büyür, kıta noktaları sıcak beyaza yanar. F053'te Amerika yayı batıya açılır; F059'da Afrika damlası güneyde iner. Kamera batıya döner.
- **Metin:** Avrupa (kıta etiketi, 1,6 sn)  
  *EN:* Europe
- **Efekt:** Varış dalgası: soğuk gri→sıcak beyaz, dalga ucu 1,6 parlaklık, 1 sn; bloom; yay izi kalıcı ince lime çizgi olarak kalır.
- **Rakam · kaynak:** Kıta sayacı 1/5 — 5 kıta: Ege Gazbeton ihracat bölümü
- **Etkileşim:** Etiket üstüne gelince varış halkası yeniden nabız atar (SVG); etiket tıklanmaz.
- **Pazarlama:** Kanıt başlıyor: yakın komşudan başlayıp uzağa yayılan güven.
- **Üretim:** Varış dalgası numpy ~0,2 sn/kare; 12 kare × ~75 sn ≈ 15 dk (d), 6 kare × ~35 sn ≈ 3,5 dk (m).
- **Telefon:** Yalnız aktif kıtanın etiketi görünür; aynı anda iki etiket yok.
- **Risk:** Kıta adı etiketi serbest mi? teyit gerekli. Yay hedefleri kıta iç bölgesinde, ülke işaretlemez. Başlık+cümle ile birlikte tek kısa etiket: okuma yükü sınırda.
#### t=125 (2:05) · 2750 vh · p=0.31
- **Kare:** Blender kure F060-F071 (Afrika dalgası biter F071)
- **Görsel:** Afrika kıtası yanar, Avrupa dalgası biter (F062). Uzun Amerika damlası Akdeniz'den Atlantik'e süzülür; kamera küreyi batıya çevirir (c -5°→-20°), yay ufka doğru kıvrılır.
- **Metin:** Afrika (kıta etiketi)  
  *EN:* Africa
- **Efekt:** Yay iki katmanlı: parlak çekirdek + yumuşak ışıma, kuyruk 0,18; ince bulut kabuğu küreden farklı hızda kayar (paralaks), Ege üstü açık.
- **Rakam · kaynak:** Kıta sayacı 2/5
- **Etkileşim:** Kaydırma hızı damla hızıdır: yavaş kaydıran damlayı yakından izler.
- **Pazarlama:** Yolculuk hissi: paletin yolu çizgi olarak okunur; her kıtaya aynı özen.
- **Üretim:** Yay: çift eğri (bevel start/end) + damla; bulut kabuğu Noise alfa; 12 kare × ~75 sn ≈ 15 dk (d), 6 kare × ~35 sn ≈ 3,5 dk (m).
- **Telefon:** Dönüş telefonda %25 yavaş (6 kare/sn'de çift görüntü); Afrika etiketi sol alt.
- **Risk:** Dönüş tepe ≤33°/sn: 12 kare/sn'de kare başı ≤2,8° (nokta aralığı 1,25°) → hafif çift görüntü; kabul edilir, aksi halde 16 kare/sn.
#### t=126 (2:06) · 2772 vh · p=0.38
- **Kare:** Blender kure F072-F083 (Amerika varış F073)
- **Görsel:** Amerika damlası F073'te karanlık yarım küreye iner: soluk şehir ışıkları arasında büyük lime halka açılır; kıta karanlıktan sıcak ışığa yanar. Kamera c≈-22° ile Atlantik'i kadrajlar.
- **Metin:** Amerika (kıta etiketi)  
  *EN:* The Americas
- **Efekt:** En yüksek kontrast: karanlıkta 75° yarıçaplı dalga, 1,25 sn; şehir ışıkları dalgayla parlar; halka + bloom; başlık ve cümle çekilir (0,4 sn).
- **Rakam · kaynak:** Kıta sayacı 3/5
- **Etkileşim:** İki Amerika yarısı da yanar; etiket üstüne gelince halka vurgulanır; metin alanı boşalınca küre sahnenin sahibi olur.
- **Pazarlama:** En uzak varış: ulaşılmaz sanılan yer de ağın içinde. Ölçek ve güven.
- **Üretim:** Dalga 75° (kıta en uzak noktası); 12 kare × ~75 sn ≈ 15 dk (d), 6 kare × ~35 sn ≈ 3,5 dk (m).
- **Telefon:** Küre kadrajda hafif yukarı kayar; etiket küre altında.
- **Risk:** Eski hedef (18°,-86°) denizde (en yakın kara noktası 2,2° ötede): (15°,-88°) kara üstüne alınır; ülke işareti yok.
#### t=127 (2:07) · 2794 vh · p=0.44
- **Kare:** Blender kure F084-F095 (Asya damlası F088) + SVG sayaç
- **Görsel:** Amerika dalgası F088'de tamamlanır: iki yarım küre karanlıktan sıcak ışığa. Küre doğuya dönmeye başlar (c -9°→20°); F088'de Asya damlası İzmir'den ufka doğru çıkar.
- **Efekt:** Dönüş ease-in-out ile hızlanır; noktalar hafif iz bırakır; Türkiye'nin lime silüeti merkezden kayarken ışıma bırakır; Amerika ışıkları kenara çekilir.
- **Etkileşim:** 5 halkalı kıta sayacı (SVG): üçü dolu, ikisi boş, merak uyandırır; tıklanmaz.
- **Pazarlama:** Merak ve ritim: kalan iki kıta nerede? sorusu bir sonraki dönüşü çeker.
- **Üretim:** Dönüş kareleri aynı sahne, yalnız kamera/küre açısı; 12 kare × ~75 sn ≈ 15 dk (d), 6 kare × ~35 sn ≈ 3,5 dk (m).
- **Telefon:** Sayaç üst metin bandının altında, 5 küçük nokta.
- **Risk:** Telefon her 2. karede 5,6°/kare: çapraz geçiş bulanıklığı; telefon dönüşü ×0,75 hızda.
#### t=128 (2:08) · 2816 vh · p=0.5
- **Kare:** Blender kure F096-F107 (Okyanusya damlası F102, Asya varış F103)
- **Görsel:** Küre doğuya döner (c 20°→52°). F103'te Asya damlası iner: en büyük kıta İzmir'den uzaklıkla yanar. F102'de Okyanusya damlası Asya'nın güneyinden Hint Okyanusu'na uzanır.
- **Metin:** Asya (kıta etiketi)  
  *EN:* Asia
- **Efekt:** Asya dalgası 65° yarıçaplı, 1 sn; küre tüm ışık noktalarıyla ağ gibi görünür; yeni damla başında küçük lime ışıma; bloom tepede.
- **Rakam · kaynak:** Kıta sayacı 4/5
- **Etkileşim:** Etiket üstüne gelince varış halkası nabız atar; kıtalar tıklanmaz (kaynaklı bilgi yok).
- **Pazarlama:** En büyük kıta: ölçek hissi; aynı özen, aynı lime ışık.
- **Üretim:** Dalga 65°; 12 kare × ~75 sn ≈ 15 dk (d), 6 kare × ~35 sn ≈ 3,5 dk (m).
- **Telefon:** Yay telefonda sol alttan sağ üste okunur.
- **Risk:** Asya hedefi (40°,92°) iç bölge: ülke merkezi gibi okunmasın; halka küçük, etiket yalnız kıta adı.
#### t=129 (2:09) · 2838 vh · p=0.56
- **Kare:** Blender kure F108-F119 (Asya dalgası biter F115)
- **Görsel:** Asya tamamen yanar. Okyanusya damlası Hint Okyanusu üstünde en uzun yaya (118°) süzülür; küre sakinleşir (c 52°→74°), Avrupa-Afrika-Asya ışıkları tek ağa dönüşür.
- **Efekt:** Uzun yay: kuyruk 0,25; damla yanında küçük lime ışıma; arka plan koyu, yıldızlar yavaş akar; bloom 0,4 sabit; atmosfer doğuya doğru hafif ısınır.
- **Etkileşim:** Küre üstünde ‘5 kıta’ noktası belirmeye hazırlanır: ipucu halkası nabız atar (varıştan sonra tıklanır).
- **Pazarlama:** Gerilim: son kıta yolda. Marka sessiz; yalnız lime damla.
- **Üretim:** 12 kare × ~75 sn ≈ 15 dk (d), 6 kare × ~35 sn ≈ 3,5 dk (m).
- **Telefon:** Damla yarıçapı ×1,3; yay ince kalmasın.
- **Risk:** Yay ufka çok yaklaşıp okunmaz olursa hedef iç noktaya (-25°,134°) çekilip c 78°'ye hızlandırılır.
#### t=130 (2:10) · 2860 vh · p=0.63
- **Kare:** Blender kure F120-F131 (Okyanusya varış F124) + JS sayaç
- **Görsel:** Okyanusya damlası F124'te kıtaya iner: son kıta yanar, büyük halka açılır. Küre beş kıtada ışıklı; kamera c≈78°'de durur. Sayaç 0'dan 25'e sayar.
- **Metin:** Okyanusya (kıta etiketi) · 25+ ülke  
  *EN:* Oceania · 25+ countries
- **Efekt:** Son varış dalgası 44°; halka + bloom tepe; sayaç 0,9 sn'de 25'e (ease-out, kaydırmaya bağlı), '+' son anda belirir; 5/5 halkası dolar.
- **Rakam · kaynak:** 25+ ülke; kıta sayacı 5/5 — Ege Gazbeton ihracat bölümü
- **Etkileşim:** Rakam kartı tıklanır: '5 kıtada 25'ten fazla ülkeye ihracat' + kaynak (kitalar kartı); açıkken 5 halka sırayla yeniden yanar.
- **Pazarlama:** Kapanış kanıtı: 25+ ülke. Rakam büyük, kaynak küçük ve açık: güven.
- **Üretim:** Sayaç HTML (kaydırmaya bağlı), ek render yok; 12 kare × ~75 sn ≈ 15 dk (d), 6 kare × ~35 sn ≈ 3,5 dk (m).
- **Telefon:** Rakam kartı üst bandın altında yatay; sayaç aynı.
- **Risk:** Ara sayaç değerleri bilgi taşımaz (kıta başına ülke gösterilmez). Dış haberlerde 19 ülke/4 kıta yazıyor: 25+/5 için ihracat bölümü teyidi gerekli.
#### t=131 (2:11) · 2882 vh · p=0.69
- **Kare:** Blender kure F132-F143 (Okyanusya dalgası biter F138)
- **Görsel:** Beş kıta ışıklı: tüm yaylar kalıcı ince lime çizgi. Kamera yavaşça geri çekilir (d 6,0→6,2); Türkiye lime merkezde parlar. İkinci rakam kartı gelir.
- **Metin:** 5 kıta  
  *EN:* 5 continents
- **Efekt:** Yaylarda damla akışı yeniden başlar (1,4 sn döngü): sevkiyat sürüyor; '25+' tamamlanır, '+' sıçrar; atmosfer parıltısı en parlak.
- **Rakam · kaynak:** 5 kıta — Ege Gazbeton ihracat bölümü
- **Etkileşim:** İki rakam kartı yan yana: üstüne gelince kaynak satırı büyür; tıklayınca kart açılır.
- **Pazarlama:** Ülke · kıta ikilisi: iddia değil, kaynaklı rakam. Güven.
- **Üretim:** Yay akışı: damla konumu kareye bağlı (periyot 1,4 sn); 12 kare × ~75 sn ≈ 15 dk (d), 6 kare × ~35 sn ≈ 3,5 dk (m).
- **Telefon:** İki rakam yan yana (CSS 3 sütun); küre alt yarıda.
- **Risk:** 5 damla aynı anda akıyor: faz kaydırmalı ve sakin kalsın; kare tabanlı olduğundan ≥50 fps etkilenmez.
#### t=132 (2:12) · 2904 vh · p=0.75
- **Kare:** Blender kure F144-F155
- **Görsel:** Işıklı küre yavaşça döner (c 78°→70°); yaylarda damlalar akar, Avrupa-Afrika-Asya ışıkları ağ gibi birleşir. Rakamlar yerinde; ‘kaydırmaya devam’ ipucu belirir.
- **Efekt:** Atmosfer nefes alır (parlaklık ±%6, 2 sn); kıta ışıkları hafif titrer; yıldızlar yavaş sürüklenir; vinyet 0,2'ye çıkar (çıkış hazırlığı).
- **Etkileşim:** Alt ortada ince ok nabzı (CSS, 1,2 sn): kaydırmaya devam.
- **Pazarlama:** Güven anı: sessiz ve güçlü. Logo henüz yok (yalnız son bölümde).
- **Üretim:** Her kare farklı (tekrar yok); 12 kare × ~75 sn ≈ 15 dk (d), 6 kare × ~35 sn ≈ 3,5 dk (m).
- **Risk:** Hareket azalırsa donmuş hissi: damla akışı ve atmosfer nefesi bunu önler.
#### t=133 (2:13) · 2926 vh · p=0.81
- **Kare:** Blender cikis F156-F167 (çıkış 1)
- **Görsel:** Çıkış 1: kamera geri çekilir (d 6,5→7,3), küre küçülür; gövde camlaşmaya başlar, arka yarıdaki ışıklı kıtalar yumuşakça belirir; c 70°→60°.
- **Efekt:** Gövde saydamlığı 0→0,35; arka yüz noktaları %40 ışıkla görünür; yay izleri %60'a soluyor; kürenin arkasında sıcak ışıma; rakamlar yerinde.
- **Etkileşim:** ‘5 kıta’ noktası hâlâ tıklanır; kart açıkken kaydırma kartı kapatır.
- **Pazarlama:** Köprü: ışık dünyaya yayıldı; sıradaki bölüm bunu 'güvenle' tamamlayacak.
- **Üretim:** Cam gövde: Principled alfa + arka yüz nokta ışığı (numpy yön testi); 12 kare × ~75 sn ≈ 15 dk (d), 6 kare × ~35 sn ≈ 3,5 dk (m).
- **Risk:** Cam görünüm kalabalık olursa arka yüz ışığı %25'e, gövde saydamlığı 0,25'e iner (altın karede A/B).
#### t=134 (2:14) · 2948 vh · p=0.88
- **Kare:** Blender cikis F168-F179 (çıkış 2)
- **Görsel:** Çıkış 2: küre d 7,3→8,3'e uzaklaşır (c 60°→50°); cam içinde Amerika ışığı arka yarıda görünür: beş kıta aynı anda ışıklı. Rakamlar çözülür, kadraj temizlenir.
- **Efekt:** Rakam ve halka opaklığı 1→0 (0,8 sn); kürenin kenarında ince mavi-beyaz parıltı; yıldızlar parlar; yay izleri yarı ışıkta.
- **Etkileşim:** Kaydırma ipucu oku belirir ve nabız atar.
- **Pazarlama:** Ekran sadeleşir: dünya + lime merkez; son bölümdeki logo için alan açılıyor.
- **Üretim:** 12 kare × ~75 sn ≈ 15 dk (d), 6 kare × ~35 sn ≈ 3,5 dk (m).
- **Risk:** Rakamlar 134,7'de tamamen gitmeli: son karede metin yok (son bölümle çakışmasın).
#### t=135 (2:15) · 2970 vh · p=0.94
- **Kare:** Blender cikis F180-F191 (+ F192 = son F000, ortak kare)
- **Görsel:** Çıkış 3: küre d 8,3→9,0'da yavaşlayıp durur; kadrajın sağ-ortasında (~%56 yükseklik), solda boşluk. Türkiye lime merkezde, beş kıta ışıklı, arka plan koyu.
- **Efekt:** Son 6 kare ease-out ile durulur; bloom ve atmosfer sabit; tek hareket yay damlaları ve yıldızlar. Logo ve slogan son bölümde bu görselin üstüne belirir.
- **Etkileşim:** Kaydırma ipucu oku; ileri kaydırınca son bölümün teklif düğmeleri açılır.
- **Pazarlama:** Köprü: ışık ağı → 'Bugünden Yarına Güvenle' (son bölüm). Logo YALNIZ son bölümde.
- **Üretim:** F180-F191 + F192 (bir kez render): 13 kare × ~75 sn ≈ 16 dk (d), 7 kare × ~35 sn ≈ 4 dk (m).
- **Telefon:** Küre alt-orta (shift_y 0,16); sonda üstte logo alanı boş.
- **Risk:** Küre konumu/boyu son planıyla mutabık olmalı (altın kare); değişirse yalnız d, c ve kaydırma sabitleri değişir.

**Geçiş ve üretim notu (s5).** Satırlar t=120..135 (16 satır; t=136 son bölümün ilk saniyesi). p=(t-120)/16 (satır başı). Kare: 12 kare/sn (6 kare/sn küre dönüşünde nokta çift görüntüsü bırakır: nokta aralığı 1,25°, dönüş kare başı ≤2,8°), n=193 (F000..F192), satır t = F[12(t-120)]..+11; F192 = son bölümün F000'ı (ortak kare, bir kez render). Telefon her 2. kare (EGE_MINSTEP=2, 97 kare, F192 dahil). Kipler: bolge F000-F035 (nadir bölge → Anadolu → küre doğuşu), kure F036-F155 (yaylar), cikis F156-F192 (uzaklaşma, cam gövde). s4→s5: F000 = s4'ün son karesi (tepeden İzmir bölgesi: kıyı, körfez; sabah ışığı yönü s4 ile aynı); fabrika sahası → bölge ölçek atlaması s4'ün çıkış saniyelerinde, s4 planıyla mutabakat gerekir. Yay/varış programı (kare): Avrupa 40→50 (dalga →62), Afrika 46→59 (→71), Amerika 53→73 (→88), Asya 88→103 (→115), Okyanusya 102→124 (→138). Kamera: küre boylamı c 27° (F036) → -22° (F073) → 78° (F126) → 40° (F192), dönüş ease-in-out tepe ≤33°/sn; uzaklık d: 1,03 (F000) → 2,0 (F036) → 6,0 (F132) → 9,0 (F192); yükseklik: 200 km → 450 km (F012) → 1.500 km (F024) → küre. Işık: sabah güneşi sağ-ön, sol yarı gece (metin alanı koyu kalır, Amerika karanlıkta yanar). Web vuruşları (p): başlık + cümle 0,06-0,375 (cümle 122,5'ten); kıta etiketleri varışlara bağlı (1,6 sn, tek etiket); 5 halkalı kıta sayacı 0,22-0,68; rakamlar 0,65-0,92 (25+ sayacı 0,65-0,71); son kare metinsiz. Hotspot: kaynak F000-F060, kitalar F125 sonrası. ayarlar.js: s5 boy 352 vh (16×22), s4→s5 ve s5→son eşleşen karelerde GECIS 22 vh, s5 'köprü' (açık zemine erime) kaldırılır; çıkış karesi koyu kalır.

**Gereken yeni işler (s5):**
- tools/kure_noktalari.mjs: bolge kipi. land-10m + countries-10m (Türkiye 10 m poligon), pencere 36,6-39,6 K / 25,2-28,8 D, ~1 km → tex/bolge_L0.json (~60 bin nokta); L1: 50 m, 0,09°, pencere 30-46 K / 15-45 D → tex/kara_L1.json; kıta kimlikleri aynı. ~0,75 gün.
- blender/s4_dunya.py v2: FRAMES=193; kipler bolge/kure/cikis; nokta seviyeleri L0/L1/L2 (instance 'olcek' özniteliğiyle çapraz geçiş); kamera anahtarları (yükseklik, d, c, pitch) saniyeye bağlı; meta çapaları. ~2 gün.
- Küre görünümü: bulut kabuğu (Noise alfa, Ege üstü açık, ayrı hız), çift atmosfer + arka ışıma diski, stilize gece ışıkları (≤%8, sıcak beyaz), cam gövde + arka yüz zayıflatma (numpy yön testi); zemin, zemin lime halkası ve KonturLime ışığı kaldırılır (kürede lime sızıntısı olmasın). ~1,5 gün.
- Yaylar: çift eğri (çekirdek + ışıma) + kuyruk (bevel start/end) + damla döngüsü (1,4 sn) + varış dalgası (jeodezik uzaklık, 1-1,25 sn); hedefler: Amerika (15°,-88°) kara üstü; kare programı yukarıdaki F tablosu. ~1 gün.
- Meta/hotspot: kaynak (Söke, İzmir iğneleri; Aliağa/Alsancak yalnız teyitle), varış çapaları v_avrupa..v_okyanusya (ufuk testiyle: arka yüzde null), kitalar (0°,0° okyanus açığı); kit.project'e ufuk testi. ~0,5 gün.
- Web dunya.js + CSS: iğne/etiket, kıta etiketi (tek, 1,6 sn), 5 halkalı sayaç, 25+ sayacı (p'ye bağlı), kitalar kartı halka tekrarı; dil.js: i4.metin kısalır (liman ifadesi kartta), kıta etiketleri TR/EN; ayarlar.js s5 boy 352, GECIS 22; index.html SAHNE 5 vuruş pencereleri (0,06-0,375; 0,65-0,92), köprü kaldırılır. ~2 gün.
- Altın kareler (onay sonra seri): F000 (s4 ile), F036, F073, F103, F124, F180, F192 (son bölümle). 7 kare × ~75 sn ≈ 9 dk (A/B için ×2 ≈ 18 dk). Cam gövde ve dönüş çift görüntüsü bu karelerde A/B.
- kareler.py 193 kare (d) / 97 kare (m) + meta; s5 için sahne bazlı WebP kalitesi (q≈70, method 6; diğer sahneler q90 kalır, .kalite işareti sahne bazında) denenir, nokta/yıldız dokusu q90'da sıkışmıyor; sinama.mjs: s5 ileri-geri sarma, sayaç p'ye bağlılığı, hotspot ufuk gizleme. ~0,5 gün.
- Üretim özeti (ölçüme dayalı; eski dünya sahnesi render/is_s4d_k*.log ve WebP kareleri): d ≈ 193 kare × ~75 sn ≈ 4 sa (ölçülen 72-79 sn/kare; yeni sahnedeki 60 bin nokta L0, bulut kabuğu, çift atmosfer ve cam gövde ile üst sınır); m ≈ 97 kare × ~35 sn ≈ 1 sa (ölçülen 29-35 sn/kare); kare yükü (WebP q90) ≈ 34 MB (d: 193 × ~178 KB) / ≈ 10 MB (m: 97 × ~104 KB), önceki 6 MB / 2,5 MB tahmini iyimserdi. Azaltma sırası: (1) kareler.py'de s5 için WebP q≈70, method 6 (eski dünya karelerinde ölçüm, 1600×900: q90→q70 boyut ≈ -%45, 183→101 ve 254→147 KB, yoğun karelerde PSNR ≈ 42→37 dB; hedef ≈ 19 MB (d) / ≈ 6 MB (m); nokta/yıldız keskinliği altın karelerde A/B); (2) L0 nokta sayısı ~60 bin → ~40 bin (1 km → ~1,2 km), OIDN denoise açık kalır; (3) gerekirse 12 → 10 kare/sn (161 kare, d ≈ 3,4 sa, q90'da ≈ 29 MB (d) / ≈ 8 MB (m); dönüş tepe hızı ≤28°/sn'ye indirilerek kare başı ≤2,8° korunur; F tablosu ×10/12 yeniden hesaplanır, karar seri render öncesi altın karede verilir). Toplam yeni iş ≈ 8-9 gün.

### son · Finale: teklif, logo, slogan — 136–146 sn

**Amaç.** Duygu: sakin şaşkınlıktan güvene, güvenden harekete. Dünyanın ışıkları Ege'de tek kıvılcıma toplanır; kıvılcım logonun köşe çizgilerini çizer ve s0'daki 'Peki bu evi iyi yapan ne?' sorusuna tek sözcükle yanıt verir: 'Güven.' Canlı gözenek yüzeyi ürünü dokunulur kılar. Mesaj: güvenin adı Ege Gazbeton, sıradaki adım teklif. Çıkışta gece şafağa döner ('Bugünden Yarına') ve açık 'Ürün grupları' bölümüne yumuşakça bağlanır; hikâyede bakılan ürün öne çıkar.

#### t=136 (2:16) · 2992 vh · p=0.0
- **Kare:** F192 (s5 ortak son kare = son F000) + 2B JS: son-katman-d/m.json nokta, yay, damla; 0,6 sn çapraz çözülme
- **Görsel:** Koyu gecede sağ-ortada ışıklı küre (boy %56): beş kıta yanık, Türkiye lime, yaylar yarı ışıkta. Kamera sabit; solda boş karanlık. Küre çözülmeye hazırlanır.
- **Efekt:** Pişmiş kare ile 2B nokta/yay katmanı üst üste biner, kare erir; damlalar yaylarda akmayı sürdürür; yıldızlar 6 px paralaksla süzülür; atmosfer kenarı sönmeye başlar.
- **Etkileşim:** İmleç yıldız katmanını ters yönde 6 px iter (derinlik); açık nokta kartı varsa kapanır; kaydırma oku nabız atar.
- **Pazarlama:** Sakin güç anı: s5'in ışık ağı sahnede, ekranda söz yok; dikkat tamamen küreye.
- **Üretim:** Yeni Blender render yok (F192 s5'te). Katman JSON ≈20 sn; JS ≤1,8 ms/kare (14k nokta). Efor 1,25 gün (son.js iskeleti dahil).
- **Telefon:** Küre alt-orta (s5 shift_y 0,16); nokta üst sınırı 8k; üstteki alan logo için boş.
- **Risk:** SEAM: 2B katman F192 ile piksel hizalı olmalı (altın kare farkı <%2). Küre sağda: bu perde kompozisyonu merkeze alır (s5'in 'logo solda' notundan sapma; mutabakat).
#### t=137 (2:17) · 3014 vh · p=0.1
- **Kare:** 2B JS (p'ye bağlı, geri sarılır): yaylar geri sarılır, noktalar Ege noktasına akar; Blender yok
- **Görsel:** Yaylar Okyanusya'dan Avrupa'ya sırayla geri sarılır; kıta noktaları yay boyunca ışık damlası olup Ege'ye akar. Cam gövde söner, Türkiye lime en son kalır.
- **Efekt:** Noktalar 2 px kuyrukla hızlanır (ease-in); Ege noktasında kor ışıması büyür; kanvas içi 'lighter' birleştirme (CSS blend değil); yıldızlar kararır.
- **Etkileşim:** İmleç yakınındaki akan noktaları 40 px saptırır, sonra yay geri çeker; hareketsizken etki yok.
- **Pazarlama:** Köken vurgusu: dünyaya yayılan bütün ışık Ege'ye (Söke, İzmir) döner; marka hikâyesinin merkezi, metinsiz.
- **Üretim:** Nokta konumu = köken→hedef lerp (Float32Array, kıta gecikmeli); ≈1,4 ms/kare (d). Efor 1 gün.
- **Telefon:** Akan nokta 4k, kuyruk 1 px; hedef nokta %42 yükseklikte.
- **Risk:** ≥50 fps: kare süresi 6 ms'yi aşarsa nokta sayısı yarıya iner (statik katman). Ülke sınırı/adı çizilmez; Türkiye lime yalnız gerçek poligon noktaları.
#### t=138 (2:18) · 3036 vh · p=0.2
- **Kare:** 2B JS kıvılcım (kivilcim.js, s0 ile ortak) + HTML 'Güven.'
- **Görsel:** Her şey tek sıcak ışık noktasında toplandı: kıvılcım ekranın ortasına süzülür ve nabız atar. Altında tek sözcük belirir: 'Güven.' Küre, yaylar, noktalar kayboldu.
- **Metin:** Güven.  
  *EN:* Trust.
- **Efekt:** 0,5 sn tam karanlık nefes; kıvılcım 1 Hz nabız, bloom, 12 kor parçacığı yavaşça yükselir; ışık rengi s0'daki pencere ışığıyla aynı sıcak ton.
- **Etkileşim:** Kıvılcım imlece 12 px süzülür; tıklama/dokunma kısa ışın demeti atar (s0 t=1 ile aynı).
- **Pazarlama:** Hikâyenin yanıtı: s0'daki 'Peki bu evi iyi yapan ne?' sorusuna tek sözcük; marka vaadinin özü.
- **Üretim:** kivilcim.js s0'dan ortak; 'Güven.' HTML (Barlow Condensed 700). ≤0,3 ms/kare. Efor 0,5 gün.
- **Telefon:** Kıvılcım %42 yükseklikte; 'Güven.' 56 px, altında.
- **Risk:** s0 H1 slogansa 'Güven.' ile yineleme olur (s0 açık soru 1). Yanıt sözcüğü onay ister; sözsüz alternatif: yalnız kıvılcım.
#### t=139 (2:19) · 3058 vh · p=0.3
- **Kare:** SVG + 2B JS: kıvılcım 4'e bölünür, logo köşe işaretleri çizilir (stroke-dashoffset, p'ye bağlı)
- **Görsel:** Kıvılcım patlar; dört ışık çerçevenin köşelerine uçar, her biri geri dönerek bir lime L çizer. 'Güven.' çerçevenin tam ortasında kalır.
- **Efekt:** 46 ışınlık kısa patlama (s0 t=1 ile aynı); çizgi ucunda kor izi; merkezden ince lime halka dalgası başlar (1 px, 0,9 sn).
- **Etkileşim:** Çizgi ucundan geçen imleç kor saçar; kıvılcıma tıklamak çizimi hızlandırır.
- **Pazarlama:** Marka imzası çizgiyle doğar: s0'ın kıvılcım→çizgi motifi logonun köşelerinde tamamlanır.
- **Üretim:** 4 SVG yolu, draw-on 0,9 sn; iz JS ≈0,4 ms. Efor 0,75 gün; gerçek logo gelince köşe yolları yeniden çıkarılır.
- **Telefon:** Çerçeve 240×152 px (genişliğin %62'si), ortada.
- **Risk:** Logo hâlâ YER TUTUCU (köşe işaretli). Gerçek logo köşesizse çizim yerine ölçek+belirme. Logo bu ana dek DOM'da hidden/aria-hidden olmalı (logo yalnız burada).
#### t=140 (2:20) · 3080 vh · p=0.4
- **Kare:** SVG logo + WebGL canlı katman (src/canli): halka dalgasıyla clip-path açılışı (eg:ready sonrası)
- **Görsel:** 'Güven.' kabarcıklara dağılır; yerine EGE ve GAZBETON açılır, çerçeve tamamlanır. Halka dalgası arkada gözenek yüzeyini açar; altında slogan belirir.
- **Metin:** Bugünden Yarına Güvenle  
  *EN:* Built on trust — today and tomorrow
- **Efekt:** Gazlanma: gözenekler easeOutBack ile şişer, amber ısıyla doğup mineral beyaza soğur; merkezden dışa 1,6 sn clip-path halkası; logo clip reveal 0,9 sn.
- **Etkileşim:** İmleç/dokunuş yüzeyde dalga bırakır (wake, pointerdown damlası); yakın gözenekler lime ışır; ipucu halkası imleci izler.
- **Pazarlama:** Logo YALNIZ burada: marka anı. Slogan 'Güven' sözcüğünü devralır ve 'Bugünden Yarına Güvenle' olur.
- **Üretim:** canli.js s4 başında iner, t=135'te ön ısıtılır; intro p'ye bağlı (λ2,4). Efor 2,5 gün (entegrasyon + logo).
- **Telefon:** Canlı katman mid kademe (17k nokta, DPR<=1,25); logo %62 genişlik; ışık merkezi %40.
- **Risk:** TIERS dprMax şimdi 1,5/2: kural gereği 1,25 olmalı. eg:ready gelmezse halkasız 1,4 sn opacity yedeği. --eg-warm lime→amber (ısı ürün değil).
#### t=141 (2:21) · 3102 vh · p=0.5
- **Kare:** JS/CSS FLIP: logo+slogan üst kilide oturur; H2 gelir; canlı katman etkileşimli
- **Görsel:** Logo ve slogan küçülüp üst-ortaya kilitlenir; altında 'Projeniz için teklif alın.' yükselir. Yüzey yerleşir: mineral beyaz gözenekler imleçle dalgalanır.
- **Metin:** Projeniz için teklif alın.  
  *EN:* Get a quote for your project.
- **Efekt:** FLIP ölçek 1→0,62 (0,8 sn); H2 translateY 22→0; gözenek idle dalga + imleç izi; radyal vinyet metni okunur tutar (backdrop-filter yok).
- **Etkileşim:** 'Yüzeye dokunun' ipucu (3 sn, ilk harekette söner): imleç gezdikçe gözenekler lime parıldar, dalgalar yayılır.
- **Pazarlama:** Değer önerisi + marka kilidi; üst çubuk logosu bu anda görünür (varsayılan; açık soru 1).
- **Üretim:** FLIP ≈40 satır JS, yalnız transform/opacity, ≈0,2 ms. Efor 1 gün (H2 ve ipucu dahil).
- **Telefon:** H2 32 px iki satır; kilit %11 yükseklikte; ipucu 'Dokunun'.
- **Risk:** Üst çubuk logosu hikâye boyunca gizli tutulacaksa t=141'e dek visibility:hidden (kural yorumu). Hareket azaltmada statik kilit.
#### t=142 (2:22) · 3124 vh · p=0.6
- **Kare:** HTML/CSS: cümle + ana CTA (Teklif Al) + 1 ikincil (Ürün Kataloğu · PDF) sırayla (80 ms arayla) + tek bağlam çipi; baglam.js
- **Görsel:** Cümle belirir; yalnız iki düğme yükselir: Teklif Al (lime, ana) ve çizgili Ürün Kataloğu · PDF (tek ikincil). Teklif Al altında hikâyede en çok bakılan ürünün tek bağlam çipi: 'EGEPOR ×'. Kitle çipleri ve kanıt kartları henüz yok (t=143 ve t=144): ana CTA ekranda tek başına okunur.
- **Metin:** Duvar ölçünüzü iletin; çözümü biz hazırlayalım.  
  *EN:* Send your wall dimensions; we prepare the solution.
- **Efekt:** Teklif Al ilk belirir, ikincil +80 ms, çip +160 ms; Teklif Al halkası 2 sn'de bir nabız (transform/opacity); düğme üstünde yüzeye dalga (eg:pulse, mevcut); ok kayar.
- **Etkileşim:** Teklif Al → /teklif/?urun=egepor&kaynak=hikaye; Ürün Kataloğu · PDF → /katalog/ (yer tutucu); çipteki × bağlamı siler. Çip tek: duvar hesabı çekmecede yapıldıysa aynı çipe ölçü eklenir ('EGEPOR · 84 m² ×'), ikinci çip yok. Teknik Özellikler düğmesi bu gruptan çıktı: mimar için aynı hedef t=143'teki 'Mimar / mühendisim' çipinde (/teknik-foyler/). Son sahnede quiz rozeti, gömülü mini hesap formu ve 'Araçlar' çekmecesi/düğmesi yok (rozet yalnız çekmecede).
- **Pazarlama:** Net CTA: tek lime ana düğme + tek ikincil (önceki 3 düğme 2'ye indi); ana CTA'ya ulaşma sürtünmesi azalır (t=142 = filmin %97'si, ek öğe yok); hikâyede izlenen ürün teklife taşınır (kişiselleştirme). Mobil alt çubuk ve WhatsApp numara teyidi gelene dek konmaz.
- **Üretim:** baglam.js: s1 durak bekleme süresi + nokta kartı tıklaması, sessionStorage (çerezsiz), tüm [data-teklif] href güncellemesi. Efor 1 gün.
- **Telefon:** Düğmeler dikey ve tam genişlik: Teklif Al, altında Ürün Kataloğu · PDF (çizgili), en altta çip; üst çubuktaki Teklif Al gizli olduğundan ana CTA budur. Alt sabit çubuk ve WhatsApp düğmesi konmaz (numara teyidi gelene dek).
- **Risk:** /teklif/ parametreyi okumazsa zararsız. Katalog PDF bağlantısı yer tutucu (/katalog/) ve dosya tarihli (22.09.25): güncelliği ve ürün kodları site tarafıyla teyit gerekli. Yanıt süresi sözü yok. 'Hikâyeyi atla' ve yolculuk çubuğu 'Teklif' bu duruma (p=0,62) iner: bu karede sahne içinde yalnız 3 etkileşimli öğe vardır.
#### t=143 (2:23) · 3146 vh · p=0.7
- **Kare:** HTML/CSS/JS: tek sıra kitle çipleri; ÇIKIŞ 1: şafak başlar, canlı kamera yükselir
- **Görsel:** 'Size en uygun yol:' etiketiyle tek sıra üç kitle çipi (yapı sahibi, mimar-mühendis, ihracat alıcısı/bayi) ana CTA grubunun altında belirir; kanıt kartları henüz yok (t=144). Alt kenarda ılık şafak parıltısı yükselir.
- **Metin:** Size en uygun yol:  
  *EN:* Find your way:
- **Efekt:** Amber şafak gradyanı alttan %0→35 (lime değil); canlı kamera setProgress 0→0,3; gözenekler alt yarıda ısınır (uDawn); kabarcıklar yukarı hızlanır.
- **Etkileşim:** Çip üstünde yüzeye dalga (eg:pulse); her çip ?urun&kaynak=hikaye&kitle= taşır; mimar çipi Teknik Özellikler yolunu (/teknik-foyler/) üstlenir. Bu saniyede başka yeni düğme, kart ya da bağlantı yok.
- **Pazarlama:** Kitle yönlendirmesi tek sırada: üç yol, tek karar; ana CTA'yı gölgelemeyen ince çizgili çipler. Kanıt kartları bir saniye sonra gelir (dönüşüm sürtünmesi iki saniyeye yayılır).
- **Üretim:** CSS/JS + uDawn (≈12 GLSL satırı). Efor 1,5 gün (şafak dahil).
- **Telefon:** Çipler tek sıra yatay kaydırma şeridi (scroll-snap); şerit dikey kaydırmayı engellemez.
- **Risk:** Çipler ana CTA ile yarışmamalı: ince çizgili, lime dolgu yalnız Teklif Al. Şafak başlangıcı CTA ve çip bölgesini örtmemeli (alt %35'te yalnız gradyan, metin yok). Ülke adı yok.
#### t=144 (2:24) · 3168 vh · p=0.8
- **Kare:** CSS/JS: 3 statik kanıt kartı sırayla (80 ms arayla); şafak güçlenir; gözenek kenarlı açık kâğıt perde alttan yükselir (ÇIKIŞ 2)
- **Görsel:** Kitle çiplerinin altına üç kanıt kartı sırayla gelir (2 fabrika, CE belgeleri, 25+ ülke · 5 kıta; kaynak her kartın altında). Gece ılık şafağa döner: gözenekler yükselip seyrelir, kamera yüzeyin üstüne süzülür. Altta gözenek kenarlı açık perde yükselir; kabarcıklar perdeye karışır.
- **Efekt:** Kartlar translateY 14→0 + opacity (80 ms arayla); şafak %35→70; perde translateY 100→88%; canlı uFade 0,7→0,45; 14 CSS kabarcığı perdeden içeri süzülür; CTA bloğu −3 vh paralaks.
- **Rakam · kaynak:** 2 fabrika · Söke & İzmir (Ege Gazbeton ortak rakamlar); 25+ ülke · 5 kıta (Ege Gazbeton ihracat bölümü); CE belgeleri
- **Etkileşim:** Kanıt kartları bilgi kartıdır: bağlantı ve odak yok (Tab sırasına girmez), kaynak satırı okunur; CTA ve çipler tıklanır kalır (perde pointer-events:none); aşağı ok nabız atar; yüzey hâlâ imleçle dalgalanır.
- **Pazarlama:** Güven kanıtı kitle seçiminden hemen sonra, ayrı bir saniyede: 2 fabrika, CE belgeleri, 25+ ülke · 5 kıta; 'Bugünden Yarına' görselleşir: akşamla başlayan hikâye şafakla biter; sıradaki adım ürünler.
- **Üretim:** tools/gozenek_kenar.py: tek SVG kenar (~3 KB, ≈80 satır), CSS tekrar; kabarcık CSS; kanıt kartları HTML/CSS (t=143 satırındaki 1,5 günlük işe dahil, toplam değişmez). Efor 0,5 gün.
- **Telefon:** Perde %10 yükseklik + safe-area-inset-bottom; kabarcık 8; kanıt 3 sütun, kaynaklar tek dipnot satırında (gizlenmez).
- **Risk:** Perde CTA'yı örtmemeli (≤%14 yükseklik); kenar ile .eg-sonrasi üst kenarı piksel hizalı olmalı. Yalnız doğrulanmış kanıt: ISO/TSE/EPD vb. teyit gerekli, eklenmedi; 'CE belgeleri' kapsamı (hangi ürünler) teyit gerekli. Ülke adı yok. Atlayan ziyaretçi p=0,62'de (t≈142) iner, kartlar p≥0,80'de belirir: kaydırdıkça görünür; kanıt kaybı ölçülürse iniş p=0,82'ye alınabilir (açık karar).
#### t=145 (2:25) · 3190 vh · p=0.9
- **Kare:** CSS/JS: ince 'Hikâyeyi baştan izle' bağlantısı gelir; perde %16'ya oturur; canlı katman uyur; sticky bırakma (+100 vh) ile 'Ürün grupları'na bağlanır (ÇIKIŞ 3)
- **Görsel:** Perde alt %16'yı kaplar; perdenin hemen üstünde ince 'Hikâyeyi baştan izle' bağlantısı belirir; üstte şafaktaki sönük gözenek yüzeyi, logo kilidi, CTA, kitle çipleri ve kanıt kartları okunur kalır. Kaydırma sürünce sahne yukarı kayar, açık 'Ürün grupları' gelir.
- **Metin:** Hikâyeyi baştan izle  
  *EN:* Watch the story again
- **Efekt:** Perde ease-out ile oturur; bağlantı opacity 0→0,7 (dikkat çekmez); canlı katman %40'a düşüp setActive(false) ile uyur (rAF iptal); şafak tam; aşağı ok nabız atar.
- **Etkileşim:** Hikâyeyi baştan izle → akış başına döner (iç bağlantı, parametresiz; ege_tekrar). Yalnız sticky bırakıldıktan sonra (film dışı, 'Ürün grupları' bölümünde) hikâyede bakılan ürünün kartı lime kenar + 'Hikâyede baktığınız' etiketiyle öne çıkar; kartlar tıklanır.
- **Pazarlama:** Yumuşak devam: teklif akışı kesilmeden ürün gruplarına, kişiselleştirilmiş vurguyla (finale ekranında değil, bırakmadan sonra); 'Hikâyeyi baştan izle' ana CTA ile yarışmayan ince bağlantı; Teklif Al üst çubukta sürer.
- **Üretim:** .eg-urun.is-izlenen CSS + 10 satır JS; WebGL uyutma 5 satır. Efor 0,5 gün.
- **Telefon:** Kartlar tek sütun; vurgulu kart kaydırmada merkeze yakın, sıra değişmez; 'tekrar izle' ≥44 px dokunma alanı, perde ve safe-area üstünde.
- **Risk:** Perde kenarı piksel hizası; 'tekrar izle' perdeyle örtüşmez (≥8 px üstünde). t_son=146 dışlayıcı: sticky bırakma 100 vh ayrı. Uyuyan canlı katmanın donuk karesi opacity ile gizlenir, GPU belleği bırakılır.

**Geçiş ve üretim notu (son).** Satırlar t=136..145 (t=146 = 'Ürün grupları'). p=(t-136)/10 (satır başı); τ=t-136; akış 2992-3212 vh. ayarlar.js SAHNELER'e { id:'son', boy:220, tur:'son' } eklenir (s5→son GECIS 22 vh, eşleşen kare). MİMARİ: son, kare dizisi olmayan 7. yapışkan sahnedir (SonSahne; Sahne ile aynı konumla/step/render API'si). İçerik bugünkü #teklif bölümünden taşınır; no-JS ve hareket azaltma için durağan sütun yedeği kalır. KATMANLAR (alttan üste): (1) 2B tuval: s5 F192 (= son F000) + son-katman-d/m.json (nokta, yay, damla, Ege noktası; s4_dunya.py 'katman' kipi, render yok) + kivilcim.js (s0 ile ortak) + yıldız; (2) WebGL canlı katman (src/canli, three.js) clip-path halkasıyla açılır; (3) SVG: halka dalgası, logo köşe işaretleri ve yazı; (4) HTML: Güven., slogan, H2, cümle, ana CTA + 1 ikincil, tek bağlam çipi, 3 kitle çipi (tek sıra), 3 kanıt kartı (statik), tekrar izle; (5) şafak gradyanı + gözenek kenarlı kâğıt perde. Yalnız transform/opacity/clip-path; backdrop-filter ve mix-blend yok ('lighter' yalnız 2B kanvas içinde). Çöküş/çizim animasyonları p'ye bağlıdır (ileri-geri sarılır, kaydırma yokken iş yok); istisna boşta döngüler (kıvılcım nabzı, yıldız, canlı katman rAF). ZAMANLAMA (τ): 0 çözülme, 1 çöküş, 2 kıvılcım + 'Güven.', 3 köşe çizimi, 4 logo + slogan + canlı açılış, 5 kilit + H2, 6 cümle + ana CTA + 1 ikincil + bağlam çipi, 7 kitle çipleri (tek sıra) + şafak başlar, 8 kanıt kartları + şafak güçlenir + perde yükselir, 9 tekrar izle + perde oturur. WEB VURUŞLARI (p): Güven. 0,18-0,40; slogan 0,40-1,01; H2 0,50-1,01; ipucu 0,50-0,70; cümle + ana CTA + ikincil + çip 0,60-1,01; kitle çipleri 0,70-1,01; kanıt kartları 0,80-1,01; tekrar izle 0,90-1,01; şafak 0,70-1,0; perde 0,80-1,0. SADELEŞTİRME (denetim, yüksek): t=142-145 ekranında ana CTA + 1 ikincil + 1 bağlam çipi önce gelir; sonra tek sıra 3 kitle çipi (t=143), 3 statik kanıt kartı (t=144), 1 ince tekrar izle bağlantısı (t=145). Sahne içi en çok 7 etkileşimli öğe, saniyede en çok 3 yeni etkileşimli öğe (t=142: 3, t=143: 3, t=144: 0, t=145: 1). Son sahnede YOK: quiz rozeti/sonuç kartı, gömülü duvar_hesap mini formu, 'Araçlar' çekmecesi ve düğmesi (moduller yalnız çekmecede; rozet yalnız çekmecede), ayrı 'Teknik Özellikler' düğmesi (mimar çipi aynı hedefe gider), mobil alt sabit çubuk ve WhatsApp düğmesi (son_bar_mobil/son_whatsapp_mobil numara teyidi gelene dek konmaz). 'Hikâyede baktığınız' vurgusu finale ekranında değil, yalnız sticky bırakıldıktan sonra 'Ürün grupları' bölümünde. CANLI KATMAN YAŞAM DÖNGÜSÜ: canli.js (565 KB, 146 KB gz) bugün IntersectionObserver ile sayfa başında iner çünkü sticky sahne hep görünür; s4 başına (t>=104) taşınır. init t>=128 (requestIdleCallback); ilk render t=135 opacity 0 (shader derleme sıçraması karanlıkta saklanır); setActive(true) p>=0,15; intro hedefi smoothstep(p; 0,25-0,55) ve damp λ2,4 (süre-bağımsız, atlamaya dayanıklı); setProgress kamerayı p 0,7→1 arasında yükseltir; p>=0,95 setActive(false). BAĞLAM: s1 vuruşlarına data-urun; en uzun bekleme ya da nokta kartı tıklaması baglam.js'e yazılır; [data-teklif] ve kitle bağlantılarına ?urun=...&kaynak=hikaye(&kitle=...) eklenir; hikâye atlanırsa urun yok. s5→son: s5 F192 küre sağ-ortada (boy %56), solda boş, metin yok, arka plan koyu; bu perde küreyi 2 sn'de Ege noktasına toplayıp kompozisyonu merkeze alır (s5 notundaki 'logo solda belirir'den sapma, ilk satırın riskinde). son→Ürün grupları: açık perde (paper #f6f7f7, gözenek kenarı) t=144-145'te alttan %16'ya yükselir; sticky bırakıldığında gerçek .eg-sonrasi üst kenarıyla piksel eşleşir. YEDEKLER: reduced-motion/no-js durağan sütun (WebGL static tek kare); WebGL yok veya saveData için kareler/son/gozenek.webp; 'Hikâyeyi atla' sahneyeGit('son') p=0,62 (CTA durumu).

**Gereken yeni işler (son):**
- s4_dunya.py 'katman' kipi: s5 F192 pozunun nokta (≤14k d / 8k m; kıta ve Türkiye bayrağı), yay çoklu çizgi, Ege noktası ekran koordinatları → kareler/son/son-katman-d/m.json; render yok (~20 sn). 0,25 gün.
- src/hikaye/son.js (SonSahne) + kivilcim.js (s0 ile ortak): 2B nokta/yay çöküşü, kıvılcım, yıldız, p'ye bağlı. ~3 gün.
- SVG logo: köşe draw-on + yazı clip reveal + FLIP kilit; gerçek logo SVG'sinden köşe/yazı yollarının ayrılması. ~1,5 gün.
- src/canli: HeroScene.setActive/setProgress/setIntro/setDawn; TIERS dprMax<=1,25; --eg-warm amber; odak ekran merkezine; ön ısıtma; context-lost yedeği; yükleme zamanı t>=104. ~2 gün.
- baglam.js + index.html: s1 vuruşlarına data-urun, [data-teklif] href, çip arayüzü, sessionStorage, .eg-urun.is-izlenen, dataLayer olayları (son_goruldu, logo, cta, kitle, urun). ~1,5 gün.
- HTML/CSS: eg-sahne--son (H2, cümle, ana CTA + 1 ikincil, tek bağlam çipi, 3 kitle çipi tek sırada, 3 statik kanıt kartı, tekrar izle), mobil düzen, şafak, kâğıt perde; tools/gozenek_kenar.py. ~2,5 gün.
- dil.js: son.cevap, son.slogan A/B/C, son.metin2, son.ctx, son.kanit.*, son.dokun, son.tekrar, son.izlenen (TR/EN); ayarlar.js son boy 220; arayuz.js 'sonda' mantığı sahne tabanlı. ~0,5 gün.
- sinama.mjs: logo yalnız son sahnede (DOM + aria), fps ölçümü, CTA tıklanabilirliği t=142-145, ?urun href, reduced-motion; son sahne kural taraması (sahne içi etkileşimli öğe ≤7, saniyede ≤3 yeni; quiz rozeti, gömülü duvar_hesap formu, 'Araçlar' düğmesi/çekmece, son_bar/WhatsApp DOM'da yok); statik gözenek yedeği (gozenek.webp). Altın kareler: t=136, 138, 140, 142, 145. ~1,5 gün.
- Toplam yeni iş ≈ 12-13 gün; yeni Blender render yok (yalnız JSON, ~20 sn).

## 4. Etkileşimli ve öğretici modüller

Hikâye boyunca eklenecek etkileşimli + öğretici modül kataloğu (14 modül). Render gerektirmez; HTML/SVG/CSS/2B canvas/JS, çevrimdışı, ≥50 fps. Her modülde sayıların kaynağı yazılıdır; doğrulanamayanlar 'teyit gerekli'. Ek alanlar: kip, mobil, bagimlilik (modül başına); film_haritasi, ortak_teknik, dogrulanmis_rakamlar, dogrulanamayanlar (üst düzey).

### Evde nerede? — ürün seçici ve araç rafı (`urun_secici`) — efor: buyuk
- **Nerede:** s1 Ürün turu (Perde 2) · film t=34–35 sn (İçindekiler; çip çubuğuyla birlikte 'Evde nerede?' çipi belirir) · ayrıca t=0–135 sn kalıcı 'Araçlar n/14' düğmesi (yolculuk çubuğunun yanında, .eg-yol); SON sahnede (t≥136) düğme ve çekmece yok, modül yüzeyi yok: yalnız seçilen ürün tek bağlam çipine ('EGEPOR ×') taşınır.
- **Ne yapar:** Maket evin 3 katlı kesit silüeti (bina_detay.py ile aynı 12 × 9 m aks, 3 kat) açılır; 7 sıcak nokta: dış duvar, pencere/kapı üstü, çatı kenarı (parapet hatılı), derz, döşeme/çatı, kolon-kiriş, otopark ve bodrum tavanı. Dokununca nokta lime halka alır (yalnız Ege ürünü vurgulanır), altta ürün adı + tek cümle + iki düğme çıkar: 'Turda gör' (ürünün film durağına 4× hızla sarma: duvar t=36, lento t=41, U blok t=46, tutkal t=51, panel t=56, EGEPOR t=61) ve 'Dene' (ilgili modül: dış duvar → duvar_hesap, çatı kenarı → kesit_gezgini, kolon-kiriş → once_sonra). 'Araçlar' çekmecesi: 14 modülün kart ızgarası, denenenler işaretli, ilerleme çubuğu; her modül kendi bağlamında açılır. Dokunulan ürün baglam.js'e yazılır (akt-son): SON'daki tek bağlam çipi ('EGEPOR ×') ve /teklif/?urun=… bağlantısı bu seçimle gelir; 'Hikâyede baktığınız' kartı yalnız sticky bırakıldıktan sonra 'Ürün grupları'nda öne çıkar (finale ekranında değil).
- **Öğretici değer:** Ürün adı → evdeki yeri eşlemesini YER üzerinden öğretir (zihinsel harita): duvar = blok, açıklık üstü = lento, çatı hatılı = U blok, derz = tutkal, döşeme/çatı = panel, kolon-kiriş = EGEPOR. Soruyu tersine çevirir ('nerede kullanıyorum?'); ürün adını bilmeyen yapı sahibi de, mimar da kendi sorusundan girer. Çekmece ayrıca öğrenme sırasını gösterir (nerede → ne kadar → içinde ne → neden → nasıl yapılır → nasıl gider → pekiştir).
- **Pazarlama değeri:** Niyet sinyali: hangi noktaya basıldığı = hangi ürünle ilgilendiği; baglam.js üzerinden Teklif CTA'sına ?urun= taşınır, satış ekibi ilk temasta ilgiyi bilir. Hero'daki kitle seçici (yapı sahibi / mimar / bayi) 'kim olduğunu' sorar, bu modül 'ne için' sorusunu ekler. 'Araçlar n/14' ilerleme çubuğu keşfi oyunlaştırır; modül kullanım oranı, oturum süresi ve araçtan CTA'ya geçiş ölçülebilir olur.
- **Veri ve kaynak:** Rakam üretmez; açılan kartlarda yalnız doğrulanmış değerler: 60 × 25 cm blok yüzü, 1–3 mm derz, 4,50 m'ye kadar lento, 6 m'ye varan panel açıklığı (Ürün föyleri); EGEPOR kullanım yerleri: dış cephe, otopark ve bodrum tavanı, kolon/kiriş kaplaması (Ürün föyleri, egegazbeton.com.tr/urunlerimiz/egepor/, müşteri onaylı); U blok kullanım yerleri (Ürün föyleri, /urunlerimiz/u-bloklar/). Ev silüeti = 'maket modeli' (blender/bina_detay.py: 4 × 3 aks, 3 kat, kat yüksekliği 3,0 m). Köşe bloğu hikâyede yok (DEVIR §3 teyit bekleyen #2) → seçicide de yok.
- **Teknik:** Tek inline SVG (≤90 düğüm), 7 hit-area ≥44 px, geçişler yalnız transform/opacity (CSS); rAF kullanmaz. Çekmece: role=dialog + aria-modal=false (modal değil), odak tuzağı YOK, Esc/geri/kaydırma = kapat. KABUK (src/hikaye/moduller/kabuk.js ≈6 KB min) hikaye.js içine girer; modül gövdeleri tembel: ilk 'Dene/Araçlar' dokunuşunda ya da s1 başında requestIdleCallback ile assets/js/moduller.js (≤60 KB min, klasik IIFE; canli.js deseni, file:// uyumlu <script src> enjeksiyonu). Panel kipi KİLİTSİZ ve kullanıcı başlatımlı (ortak_teknik.kilit_ve_kaydirma): wheel/touchmove/tuş yutulmaz, passive:false yok; kaydırma paneli kapatır, kare kaydırma konumundan türediği için panel açıkken zaten sabit kalır. Masaüstü: sol anlatım sütununda açılır (konu sağda görünür kalır); telefon: alt sheet (≤70svh, tam ekran/100svh YOK), kapat 44 px. localStorage 'ege-modul' (denenen modüller) try/catch içinde, yoksa oturum belleği. Ek bitmap yok; çekmece açıkken sahne render'ı zaten durur → ≥50 fps korunur. Efor ≈ 3–4 gün (kabuk + çekmece + SVG).
- **TR metin:** chip: Evde nerede? | baslik: Hangi ürün, evin neresinde? | ipucu: Bir noktaya dokunun. | noktalar: Dış duvar · Pencere üstü · Çatı hatılı · Derz · Döşeme ve çatı · Kolon ve kiriş · Otopark ve bodrum tavanı | dugmeler: Turda gör · Dene | cekmece: Araçlar {n}/14 · Denedikleriniz işaretli
- **EN metin:** chip: Where in the house? | title: Which product, where in the house? | hint: Tap a point. | points: Exterior wall · Above openings · Roof bond beam · Joint · Floor and roof · Columns and beams · Car park and basement ceilings | buttons: See it on the tour · Try it | drawer: Tools {n}/14 · Ticked = tried
- **Kural riski:** Lime yalnız seçilen Ege ürününde (halka/kenar); kolon, kiriş, donatı, çelik gri. Ürün–yer eşlemesi yalnız teyitli kullanım yerlerinden; köşe bloğu veya yeni ürün eklenmez. 'Araçlar' düğmesi yolculuk çubuğunu kalabalıklaştırmamalı (≤2 kelime). Logo yok (logo en sonda). Panel kullanıcıyı hikâyede hapsetmez (kilit YOK): kaydırma, Esc, belirgin Kapat, geri tuşu ve dış dokunma kapatır; yalnız kullanıcı açar (çip/'Araçlar'). Telefonda anlatım alanı 40svh olduğundan s1 çip çubuğu (akt-s1 t=34) ile çakışma testi gerekir.

### Duvar hesaplayıcı (`duvar_hesap`) — efor: orta
- **Nerede:** s1 Ürün turu (Perde 2) · film t=38–40 sn (Duvar blokları: 'Düz · Geçmeli' etiketi ve 60 × 25 cm yüz rakamı t=38; t=38–40 tek otomatik öğe = pazarlama s1_duvar_hesapla bağlantısı 'Duvarlarınızı hesaplayın →': statik href /duvar-tasarla/, JS'te düz sol tık bu paneli açar; ayrı 'Hesapla' çipi yok) · araç rafı (çekmece). SON'da modül yüzeyi YOK (akt-son sadeleştirmesi): t=142'de 'Duvar ölçünüzü iletin' cümlesi + ana CTA yeter; hesap yoluna kitle çipi 'Ev / bina yapıyorum' (t=143, /duvar-tasarla/) ulaştırır; ölçü varsa yalnız tek bağlam çipinde taşınır ('EGEPOR · 84 m² ×').
- **Ne yapar:** Girdiler: duvar toplam uzunluğu (m), yükseklik (m), açıklık (pencere + kapı) toplam alanı (m²), kalınlık kaydırıcısı (5–35 cm), isteğe bağlı fire payı (% — varsayılan 0, öneri yok). Anında çıktı: net duvar alanı (m²), blok adedi (alan ÷ 0,15 m², yukarı yuvarlanmış), duvar hacmi (m³), 300–600 kg/m³ aralığında kütle aralığı (t). Animasyon: SVG minyatür duvar girdilerin oranında çizilir ve 60 × 25 şaşırtmalı bloklarla örülür, açıklıklar boş kalır (çizim 0,8 sn). 'Maket evle kıyas' çubuğu: sonuç maket evin %X'i (maket_blok_sayaci verisi). 'Özeti kopyala', 'Bu ölçüyle teklif iste' (yalnız kullanıcı sonuç ürettikten SONRA görünür; panel açıkken ekranın tek lime dolgulu düğmesi) ve yumuşak 'Ayrıntılı tasarım →' (/duvar-tasarla/, ölçüleri taşır) düğmeleri; sonuç baglam.js'e yazılır ve SON'daki TEK bağlam çipine eklenir ('EGEPOR · 84 m² ×'; ayrı ikinci çip ve ayrı bağlantı yok; blok adedi çipte gösterilmez: 'ön hesap' yalnız hesap panelinde; örnek hesap: 84 ÷ 0,15 = 560).
- **Öğretici değer:** Metraj mantığı: net alan = brüt − açıklık; blok adedi = alan ÷ blok yüzü (0,15 m²); kalınlık hacmi ve kütleyi belirler; ince derzle örüldüğü için adet nominal yüzden hesaplanır. Mimar için hızlı ön metraj, yapı sahibi için 'duvarım kaç blok' somutluğu.
- **Pazarlama değeri:** En güçlü lead aracı: kullanıcı kendi ölçüsünü girer (yüksek niyet), sonuç teklif bağlamına taşınır (?alan=&kalinlik= — site tarafı iş). Hero'daki 'Yapı sahibiyim' (→ /duvar-tasarla/) ve menüdeki 'Araçlar' ile aynı dili konuşur; hikâyenin ortasında (t=38–40) ve çekmecede iki giriş kapısı (SON'da yok: son sahnede yol 'Ev / bina yapıyorum' çipinden /duvar-tasarla/). KARAR (açık soru 2): /duvar-tasarla/ ile çakışmaz, onun film içi 'ön metraj' ön kapısıdır: t=38–40'taki 'Duvarlarınızı hesaplayın →' hem /duvar-tasarla/'ya giden gerçek bağlantı hem panel açıcıdır (JS'siz/orta tık/yeni sekme → site aracı); panelde sonucun altında 'Ayrıntılı tasarım →' derin bağlantısı (ölçüler ?uzunluk=&yukseklik=&acik=&kalinlik= ile; okunması site işi, okunmazsa yok sayılır). dataLayer ile ölçü dağılımı ve terk noktası analiz edilir; dil.js'te hazır duran (kullanılmayan) 'cta.hesapla' = 'Duvarlarınızı hesaplayın' anahtarı bu girişin düğme metni olur.
- **Veri ve kaynak:** 60 × 25 cm = 0,15 m² → 6,67 blok/m² (Ürün föyleri; hesap). Kalınlık aralığı 5–35 cm (dil.js u_duvar / h1b.k1, Ürün föyleri; üretici teyidi akt-s1 açık sorusunda bekliyor; stok kalınlıkları teyit gerekli → kaydırıcı sürekli, 'standart kalınlık' etiketi yok). Kütle: 300–600 kg/m³ (Ürün sınıfları G1/300 – G4/600; ortak rakamlar) × hacim (hesap). Fire payı: sektör oranı teyit gerekli → varsayılan 0, kullanıcı girer. Tutkal tüketimi (kg/m²), palet başına blok adedi, tır kapasitesi: teyit gerekli, ekranda yok.
- **Teknik:** HTML form (5 alan, native <input type=number|range>, inputmode=decimal, virgül/nokta kabulü), sonuç satırları aria-live=polite (500 ms debounce). Minyatür duvar: tek inline SVG, ≤12 düğüm (blok deseni <pattern> ile; binlerce blokluk duvar bile DOM'u büyütmez); rAF yalnız 0,8 sn çizim süresince. Panel kullanıcı başlatımlı ve KİLİTSİZ: kaydırma yutulmaz, kaydırma/Esc/Kapat/geri tuşu paneli kapatır; kare kaydırma konumundan türediği için panel açıkken film zaten sabit kalır. Bellek ≈0; JS ≈4 KB. Kopyalama: navigator.clipboard (file://'da güvenli bağlam olmayabilir) → yedek: seçili <textarea> + execCommand. Sayı biçimi Intl.NumberFormat('tr-TR' / 'en-GB'), yedek elle biçim. Efor ≈ 1,5–2 gün.
- **TR metin:** giris: Duvarlarınızı hesaplayın → (cta.hesapla) | baslik: Duvarınız kaç blok? | alanlar: Duvar uzunluğu (m) · Yükseklik (m) · Pencere ve kapı alanı (m²) · Kalınlık (cm) · Fire payı (%, isteğe bağlı) | sonuc: Net alan {a} m² · {n} blok · {v} m³ | kutle: Kütle {k1}–{k2} t (300–600 kg/m³) | not: Ön hesaptır; 60 × 25 cm blok yüzüne göre (Ürün föyleri). Kesin metraj için ekibimizle görüşün. | dugmeler: Özeti kopyala · Bu ölçüyle teklif iste · Ayrıntılı tasarım →
- **EN metin:** entry: Calculate your walls → (cta.hesapla) | title: How many blocks is your wall? | fields: Wall length (m) · Height (m) · Window and door area (m²) · Thickness (cm) · Allowance (%, optional) | result: Net area {a} m² · {n} blocks · {v} m³ | mass: Mass {k1}–{k2} t (300–600 kg/m³) | note: Preliminary estimate based on a 60 × 25 cm block face (product sheets). Talk to our team for an exact take-off. | buttons: Copy summary · Request a quote with this size · Detailed wall design →
- **Kural riski:** 'Ön hesap' ibaresi ve kaynak ('Ürün föyleri') zorunlu; fire, tutkal, palet rakamı uydurulmaz. Sürekli kalınlık kaydırıcısı stokta olmayan kalınlığı ima edebilir (teyit). Sitede zaten /duvar-tasarla/ aracı var: ÇAKIŞMA KARARI: iki ayrı sonuç göstermez; mini hesap onun 'ön metraj' ön kapısıdır ve /duvar-tasarla/ formülü (alan ÷ 0,15 m² ile aynı mı?) teyit edilene dek 'ön hesap' etiketi + 'Ayrıntılı tasarım →' bağlantısı zorunlu; formül farklıysa panel kapatılır, yalnız bağlantı kalır (açık soru 2). Form yalnız ölçü alanıdır (ad/e-posta/telefon yok, gönderim yok); pazarlama.cta_kurallari 'kullanıcı başlatımlı panel istisnası' kapsamında; panel içi teklif düğmesi yalnız sonuç sonrası (sürtünme sırası: araç → teklif). Teklif URL parametreleri site tarafı iş (akt-son açık sorusu). KVKK: kişisel veri alınmaz, yalnız ölçü. Lime yalnız minyatür duvardaki blok kenarı ve CTA; açıklıklar gri. Kütle yazarken 'kuru birim hacim ağırlığı' notu.

### Bu evde kaç blok var? — maket sayacı (`maket_blok_sayaci`) — efor: kucuk
- **Nerede:** s0 Hayalden yuvaya (Perde 1) · film t=12–17 sn (dolum: tel kafes → gazbeton bloklar sıra sıra iner; 'Duvarlar gazbetonla, sıra sıra' t=12, 60 × 25 cm t=13, 1–3 mm derz t=14); 'Say' kartı t=17 sn (vuruş p≈0,53) ve araç rafı.
- **Ne yapar:** Bloklar inerken ekranın sağ-altında canlı sayaç 0'dan yükselir ('Maket evde: N blok'); sayı kaydırma konumuna bağlıdır, geri kaydırınca azalır. Dolumun kat çipleri (ZEMİN → 1. KAT → 2. KAT → PARAPET; akt-s0 t=12) aynı veriden dolar. Dolum bitince 'Say' kartı açılır: toplam, kat başına, 'tam / kesik' ayrımı, duvar hacmi (m³), 300–600 kg/m³ aralığında toplam kütle; 'Senin evin?' düğmesi duvar_hesap'ı maket evin net alanıyla önyükleyip açar. 'Kesik' kutusuna dokununca kısa açıklama: kesik blok, tam bloktan kesilir (kesim/fire kavramı).
- **Öğretici değer:** Blok adedi = alan ÷ 0,15 m² (60 × 25 cm yüz); bir evin duvarı binlerce bloktur; şaşırtmalı örgüde kat kat ilerleme; kesik blok kavramı; duvar hacmi → kütle bağı (hafiflik s3'te tamamlanır).
- **Pazarlama değeri:** Sayı etkisi: 'bu evin duvarı ≈1.700 blok' somut, paylaşılabilir bir cümle; hikâyeyi 'izlenen şey'den 'hesaplanabilir şey'e çevirir. Dolumun heyecanını ölçülebilir sayıyla taçlandırır ve duvar_hesap'a doğal köprü kurar (lead).
- **Veri ve kaynak:** KAYNAK = 'maket modeli' (gerçek proje değil). Bugünkü blender/bina_detay.py çıktısından hesaplandı: 2.107 blok parçası = 1.253 tam + 854 kesik parça; kat dağılımı 627 / 626 / 626 + 228 parapet (toplam 1.879 + 228). Duvar+parapet nominal alanı 253,65 m² (222,15 m² 3 kat + 31,5 m² parapet) ÷ 0,15 m² = 1.691 tam-blok eşdeğeri; nominal hacim 50,73 m³ (20 cm duvar); 300–600 kg/m³ ile 15,2–30,4 t (hesap). Sayılar elle yazılmaz: tools/maket_say.py (yeni) bina_detay.uret() ve s0_hayal.kip_dolum'daki zaman formülüyle (t = lerp(−0,04; 1,045; seg(u; 0,06; 0,94)); parça, z01 < t ise yerleşmiş) her dolum karesi için kümülatif sayıyı assets/js/maket-say.js (window.EGE_MAKET) dosyasına yazar. İç bölme duvarı (akt-s1: y=0 aksı) ve 4,5 m panel bölmesi bina_detay'a eklenince sayı değişir → üretim derleme zamanında zorunlu.
- **Teknik:** Veri: window.EGE_MAKET = {toplam, tam, kesik, kat:[…], parapet, alan_m2, hacim_m3, kare:[kümülatif tamsayılar…]} (dolum kare sayısı kadar tamsayı, <1 KB, .js globali: file:// fetch yapmaz). Gösterim: tek <output> + 4 SVG çubuk (transform:scaleX); metin yalnız yuvarlanmış sayı değişince yazılır (tabular-nums). Kendi rAF'ı yok: Sahne.render içinde frameFloat() → kare dizisi interpolasyonu. Canvas yok; ≤0,1 ms/kare; bellek ≈0. Telefonda sayaç anlatım alanı ile 3B konu arasında 44 px şerit (konunun üstüne taşmaz). Efor ≈ 1 gün (maket_say.py 0,5 + JS 0,5).
- **TR metin:** sayac: Maket evde: {n} blok | kart-baslik: Maket evin blok sayımı | satirlar: Toplam {n} parça · {tam} tam + {kesik} kesik · Kat başına: {k0} · {k1} · {k2} · parapet {p} · Duvar hacmi: {v} m³ · Alan eşdeğeri: {a} m² ÷ 0,15 m² = {e} blok | not: Kesik parçalar tam bloktan kesilir. Maket modeli; gerçek proje değil. | kaynak: maket modeli | dugme: Senin evin kaç blok?
- **EN metin:** counter: In the model house: {n} blocks | card-title: Block count of the model house | rows: Total {n} pieces · {tam} full + {kesik} cut · Per floor: {k0} · {k1} · {k2} · parapet {p} · Wall volume: {v} m³ · Area equivalent: {a} m² ÷ 0.15 m² = {e} blocks | note: Cut pieces are cut from full blocks. Model house, not a real project. | source: model house | button: How many blocks in your house?
- **Kural riski:** Kaynak etiketi 'maket modeli' ve 'gerçek proje değil' ibaresi zorunlu (her sayının kaynağı kartta). İki sayı (2.107 parça / 1.691 eşdeğer) tek cümlede açıklanmazsa karışır. Maket derzi görünürlük için 12 mm çizilmiş (bina_detay DERZ=0,012) — yazılı 1–3 mm ile çelişir; sayım nominal 60 cm adımla yapılır, sayaç/kart metninde derz kalınlığı geçmez. Panel (20 şerit × 8,8 m) sayımı yapılmaz: föydeki 6 m açıklıkla çelişir (akt-s1 bunu 4,5 m'ye böler). Sayaç eksik inmiş karede sıçramasın (kare interpolasyonu). 3B karede rakam yok: sayaç HTML.

### Önce / sonra kaydırıcısı — kolon kaplama (`once_sonra`) — efor: kucuk
- **Nerede:** s1 Ürün turu (Perde 2) · film t=63–64 sn (EGEPOR: 'Isı sızıntısı' etiketi ve bölme çizgisi, akt-s1 t=63) · araç rafı ve urun_secici'de 'Kolon ve kiriş' noktası.
- **Ne yapar:** Ekranın ortasında dikey bölme çizgisi: sol 'Önce' — kolon ve kiriş turuncu ısı parıltısıyla (ısı sızıntısı, nitel); sağ 'Sonra' — aynı kadraj, kolon-kiriş EGEPOR levhalarla kaplı ve soğuk tonda; levhalar lime kenarlı. Çizgi parmak/fare ile sürüklenir (klavyede ← →); ilk girişte 1,5 sn otomatik süpürme ipucu. 'Kesiti gör' bağlantısı kesit_gezgini EGEPOR sekmesini açar. Aynı bileşen (karsilastir.js) kesit_gezgini'ndeki 'Ahşap kalıp ↔ U blok' karşılaştırmasında yeniden kullanılır.
- **Öğretici değer:** Kolon/kiriş kaplamasının amacını yan yana görerek öğretir: ısı kaybı yüzeylerde yoğunlaşabilir, EGEPOR bunları kaplar (nitel). Karşılaştırmayla öğrenme: aynı kadrajda tek değişken.
- **Pazarlama değeri:** Tek bakışta 'fark'; ekran görüntüsü olarak paylaşılabilir kalite; EGEPOR'u (az bilinen/yeni ürün) öne çıkarır, Egepor ürün sayfasına yönlendirir (/urunler/egepor/).
- **Veri ve kaynak:** Rakam yok (nitel). Kart rakamları: λ kuru 0,051–0,062 W/mK; 150–200 kg/m³ (Ürün föyleri). Görsel kaynak: s1 çift render (f124 ≈ 'önce', f127 ≈ 'sonra'; akt-s1) — render'daki turuncu parıltı ısı sızıntısı SEMBOLÜDÜR, ölçüm değil → alt yazı 'şematik gösterim'.
- **Teknik:** Yeni kare indirilmez: s1 dizisindeki iki kare Sahne.frames'ten alınır (zaten bellekte). Tek 2B tuval içinde: sol bölüm frame A, sağ bölüm frame B → ctx.drawImage ile iki kırpılmış çizim (clip-path / mix-blend YOK); yalnız pointermove (rAF'la birleştirilmiş) ve bölme konumu değişince çizilir; ≤1 ms (1600 × 900, DPR ≤1,25). Tutamak: touch-action:pan-y (yatay sürükleme JS'e, dikey kaydırma sayfaya); role=slider, aria-valuenow, ← → ve Home/End. Çizgi + tutamak SVG (≤6 düğüm). JS ≈2 KB. Efor ≈ 1 gün (render'ın kendisi akt-s1 işi).
- **TR metin:** etiketler: Önce · Sonra | ust: Isı sızıntısı | ipucu: Çizgiyi sürükleyin. | alt: Kolon ve kiriş kaplaması (EGEPOR). Şematik gösterim. | baglanti: Kesiti gör
- **EN metin:** labels: Before · After | top: Heat leakage | hint: Drag the line. | sub: Column and beam cladding (EGEPOR). Schematic illustration. | link: See the section
- **Kural riski:** 'Isı sızıntısı' görseli rakamsız ve şematik; 'ısı köprüsü' sözcüğü teyit gerekli (akt-s1 açık sorusu). Turuncu = ısı (yeşil değil); lime yalnız EGEPOR levha kenarı. 3B karede yazı yok; Önce/Sonra HTML. Dikey kaydırmayı bozmamak (touch-action) telefonda sınanır. Çift render hizalaması (f124/f127 aynı kamera) bozulursa çizgide sıçrama görünür → altın kare onayı.

### Kesit gezgini — blok, U blok, EGEPOR (`kesit_gezgini`) — efor: buyuk
- **Nerede:** s1 Ürün turu (Perde 2) · otomatik çip yalnız t=46–50 sn (U bloklar: t=48 donatı etiketi, t=49 'beton dökülür'; varsayılan sekme U blok). Duvar bloğu sekmesine duvar_hesap'taki 'Kesite bak' bağlantısından (t=38–40), EGEPOR sekmesine once_sonra'daki 'Kesiti gör' bağlantısından (t=63–64) ve araç rafından ulaşılır (durak başına tek çip kuralı).
- **Ne yapar:** 3 sekmeli SVG kesit + 'Katmanları ayır' kaydırıcısı (0→1: parçalar yerlerinden ayrılır; her parçaya dokununca ad + tek cümle). (a) Duvar bloğu: yatay kesit (üstten plan) — iki sıra şaşırtmalı örgü, 1–3 mm derz (lens: derz abartılı çizim), 'Düz ↔ Geçmeli' geçiş düğmesi. (b) U blok: enine kesit — U kabuk (lime kenar), donatı (koyu gri çelik), hatıl betonu (gri); kaydırıcı betonu dolduruyor; 'Ahşap kalıp ↔ U blok' karşılaştırması (aynı sürüklemeli karşılaştırma bileşeni): kalıp yok; 6 kullanım pini (yüksek duvar ara hatılı, çatı hizası, yatay/düşey betonarme hatıl, gizli baca, yağmur iniş borusunu gizleme) maket silüetinde yeri vurgular. (c) EGEPOR: kolon plan kesiti — betonarme kolon (maket 35 × 35 cm) çevresinde EGEPOR levhaları; kalınlık kaydırıcısı 5–35 cm; ölçü çizgileri; nitel ısı okları kolondan geçerken azalır.
- **Öğretici değer:** Ürünün 'içini' gösterir: örgü ve derz mantığı, U bloğun kalıp işi görmesi (kanala donatı, sonra beton), EGEPOR'un kaplama olarak yeri. Kesit okuma becerisi; donatı–beton–kalıp ayrımı.
- **Pazarlama değeri:** Mimar/mühendis kitlesine derinlik (her sekmede 'Teknik föy' bağlantısı = föye ilk adım); 'ahşap kalıp yerine' iş gücü/süre avantajını rakamsız görselleştirir; EGEPOR'u bilmeyen kitleye tanıtır (çapraz satış).
- **Veri ve kaynak:** Blok 60 × 25 cm; derz 1–3 mm; kalınlık 5–35 cm (Ürün föyleri). U blok: 60 × 25 cm, 20–25 cm kalınlık, G4/06, λ kuru 0,16 W/mK, 600 kg/m³ (Ürün föyleri; egegazbeton.com.tr/urunlerimiz/u-bloklar/); kullanım yerleri ürün sayfasından (DEVIR §3). EGEPOR: 60 × 25–50 cm, 5–35 cm, λ kuru 0,051–0,062 W/mK, 150–200 kg/m³ (Ürün föyleri; /urunlerimiz/egepor/; kolon ve kiriş kaplaması müşteri onaylı). Kolon 35 × 35 cm = maket modeli (bina_detay COL). TEYİT GEREKLİ (ekranda yok): U bloktaki '50 kgf/cm²' (DEVIR'de neyin değeri olduğu yazılı değil), 'ısı köprüsü' ifadesi (akt-s1 açık sorusu) → 'kolon ve kiriş kaplaması' denir.
- **Teknik:** 3 inline SVG (her biri ≤110 düğüm); parçalar <g> + CSS transform: translate; tek kaydırıcı → tek CSS değişkeni (--ayir 0..1), layout yok. Beton dolumu clip-path yerine scaleY (akt-s1/hikaye.css oz-dol deseni). rAF yok; JS ≈7 KB; çizimler kodla (üretilmiş görsel yok), yazılar HTML/SVG TR/EN. Mevcut .eg-ozellik çizimleri (oz-ukabuk, oz-beton, oz-donati) başlangıç noktası olarak yeniden kullanılır. Bellek ≈0. Efor ≈ 3 gün (üç sekme + pinler).
- **TR metin:** sekmeler: Duvar bloğu · U blok · EGEPOR | kaydirici: Katmanları ayır | parcalar: U kabuğu · Donatı · Hatıl betonu · Derz · Levha · Kolon | tus: Ahşap kalıp ↔ U blok | pinler: Yüksek duvar ara hatılı · Çatı hizası · Yatay/düşey hatıl · Gizli baca · İniş borusunu gizleme | not: Şematik kesit; ölçüler ürün föylerine göredir.
- **EN metin:** tabs: Wall block · U-block · EGEPOR | slider: Separate the layers | parts: U shell · Reinforcement · Bond beam concrete · Joint · Board · Column | button: Timber formwork ↔ U-block | pins: Intermediate beam in tall walls · Roof level · Horizontal/vertical beam · Hidden chimney · Concealed downpipe | note: Schematic section; dimensions per the product sheets.
- **Kural riski:** Donatı/çelik yeşil olamaz (koyu gri); s1 yönergesi: donatı ve hatıl betonuna lime uygulanmaz → yalnız U kabuğu, EGEPOR levha ve derz tutkalı lime. Köşe bloğu çizilmez. 'Ahşap kalıp yok' ürün sayfasındaki 'kalıp yerine' ifadesidir; süre/maliyet kazancı rakamla söylenmez. 'Isı köprüsü' teyitsiz kullanılmaz. Derz abartılı çizim 'ölçek dışı' notuyla. Kolon kesiti maket ölçüsü: gerçek proje değil.

### 3 soruda gazbeton — mini bilgi yarışması (`bilgi_yarismasi`) — efor: kucuk
- **Nerede:** Soru 1 — s1 Ürün turu t=56–57 sn (tutkal durağı t=51–55 biter bitmez, panel durağı girişi: 'Paneller' başlığı t=56; konu tutkal/derz). Soru 2 — s2 Doğuş t=81–82 sn (kabarma anı: 'Karışım şişer.' t=81, 'Hava hücreleri kalır.' t=82; konu kabartan hammadde). Soru 3 — s3 Gözenek t=98–99 sn (A1 rakamı t=97'den hemen sonra, sınıf merdiveni t=98 ile birlikte; konu A1). Üç pencere de perdelerin çıkış geçişi DIŞINDADIR (s1 t=67–69, s2 t=87–89, s3 t=101–103: hiçbir modül çipi açılmaz). Sonuç kartı ve rozet: YALNIZ 'Araçlar' çekmecesinde (araç rafı); SON sahnede yok. Kaçırılan soru çekmecede 'bekliyor' kalır (SON'da sorulmaz).
- **Ne yapar:** Her soru köşede tek satır + 3 şık (tek dokunuş); doğruysa 'Doğru' + kaynak, yanlışsa doğrusu ve nedeni gösterilir (geri sayım/baskı yok). Soru 1: 'Bloklar neyle birleşir?' → gazbeton tutkalı (1–3 mm ince derz). Soru 2: 'Karışımı ne kabartır?' → alüminyum tozu. Soru 3: 'A1 neyi anlatır?' → yangına tepki sınıfını (EN 13501-1). Sonuç: rozet (SVG) 'Gazbeton bilgisi N/3' yalnız çekmecedeki yarışma kartında; 3/3'te kartta 'Teknik föylere göz at' bağlantısı, eksikte eksik soruları çekmeceden yanıtlama (SON'daki ince 'Hikâyeyi baştan izle' bağlantısı ayrıdır, kartta kopyası yok). Kişisel veri/giriş istemez.
- **Öğretici değer:** Anlatılandan hemen sonra geri çağırma (retrieval practice): bilgi kalıcılaşır; yanlış cevap kavram ayrımı öğretir (A1 = yangına tepki sınıfı; yoğunluk sınıfı ve ısı iletkenliği başka şeylerdir).
- **Pazarlama değeri:** Hikâye boyunca dikkati canlı tutar; 'kaç kişi 3/3 yaptı' kampanya metriği; son soru sonrası CTA tıklama farkı ölçülür; rozet paylaşımı (Web Share varsa). Teklif öncesi 'güven' basamağını bilgiyle kurar.
- **Veri ve kaynak:** Cevaplar yalnız doğrulanmış metinlerden: 'Bloklar 1–3 mm gazbeton tutkalıyla birleşir' (Ürün föyleri; dil.js derz); 'Alüminyum tozu: kireçle tepkimeye girip hidrojen açığa çıkarır: karışım kabarır' (dil.js aluminyum); 'A1: yangına tepki sınıfı, EN 13501-1' (CE belgeleri; dil.js i2.k2). Yanlış şıklar sayı içermez (uydurma rakam yok): kavram adları (ahşap kalıp, alçı, kum, çimento, yoğunluk sınıfı, ısı iletkenliği).
- **Teknik:** Saf HTML/CSS + durum makinesi (<fieldset role=radiogroup>); sonuç localStorage 'ege-yaris' (try/catch) + oturum belleği; rAF yok; JS ≈3 KB. Mobil: soru anlatım alanının alt şeridinde (≤2 satır). Cevaplanmayan soru 3 sn sonra çipe küçülür. Çevrimdışı. Efor ≈ 1 gün.
- **TR metin:** soru1: Bloklar neyle birleşir? · Gazbeton tutkalı · Ahşap kalıp · Alçı | soru2: Karışımı ne kabartır? · Alüminyum tozu · Kum · Çimento | soru3: A1 neyi anlatır? · Yangına tepki sınıfını · Yoğunluk sınıfını · Isı iletkenliğini | dogru: Doğru. | yanlis: Doğrusu: {cevap} | sonuc: Gazbeton bilgisi {n}/3 | cta: Teknik föylere göz atın
- **EN metin:** q1: What joins the blocks? · AAC adhesive · Timber formwork · Gypsum | q2: What makes the mix rise? · Aluminium powder · Sand · Cement | q3: What does A1 describe? · The reaction-to-fire class · The density class · Thermal conductivity | correct: Correct. | wrong: The answer: {cevap} | result: AAC knowledge {n}/3 | cta: Browse the technical specifications
- **Kural riski:** Şıklarda 'yanmaz' asla (şık olarak bile). Yanlış şıklar ürünün yanlış özelliğini iddia ediyormuş gibi okunmamalı. Rozet kurumsal (lime köşe işareti, ürün rengi değil). Sorular anlatılan metinden birebir ve kaynaklı. Cevaplanmamış soru ekranı kirletmemeli. Okuma hızı: soru ≤8 kelime, şık ≤3 kelime. Zamanlama: soru çipleri çıkış geçişi (perdenin son 3 sn'si) dışında başlar ve biter (s1 t=56–57, s2 t=81–82, s3 t=98–99); cevabı veren kart/nokta (tutkal kartı, alüminyum/kabarma noktası, A1 mini kartı) açıkken soru bekler, kart kapanınca çıkar; soru çipi CTA değildir (satış eylemi yok; s2 'CTA'sız' kuralını bozmaz), bilgi CTA'sı yalnız çekmecedeki sonuç kartındadır (SON'da yok); soru penceresinde başka yeni çip açılmaz (s3'te agirlik 'Dene' çipi t=100'e kayar).

### Hafiflik: blok ve duvar ağırlığı (+ ODTÜ −%17) (`agirlik`) — efor: kucuk
- **Nerede:** s3 Gözenek (Perde 4) · film t=99–100 sn ('300–600 kg/m³ yoğunluk aralığı (G1–G4)' rakamı + tezgâhta yan yana G1/G2/G4 blok ve λ · A1 · 300–600 şeridi; film içi kaydırıcı ve 'suda yüzer' sahnesi yok; 'Dene' çipi yalnız t=100'de açılır, t=98–99 Soru 3 çipi (bilgi_yarismasi) ile yarışmaz) · ikinci giriş: s1 t=59–60 sn (Paneller: '−%17 yapı kütlesi' rakamı t=60) · araç rafı.
- **Ne yapar:** Tek yoğunluk kaydırıcısı (300 → 600 kg/m³; G1/300, G2/350, G4/600 işaretli, G3 işaretsiz) ve ürün seçici (Duvar bloğu 5–35 cm · U blok G4/06 · EGEPOR 150–200). Çıktı: tek blok (60 × 25 × kalınlık) kg, 1 m² duvar kg, 10 m² duvar kg. SVG terazi: bir kefede blok, öbür kefede kullanıcının girdiği 'kendi duvarım' (yoğunluk + kalınlık; varsayılan BOŞ — kıyas rakamını biz vermeyiz) ve fark % hesabı. Blok yüzü şematiği: yoğunluk arttıkça hücre (daire) sayısı azalır (temsili). İkinci sekme 'Deprem yükü': 8 katlı örnek bina kütle çubuğu 100 → 83 (−%17) ve onaylı cümle 'Daha hafif bina, daha düşük deprem yükü.'; ODTÜ kaynak etiketi.
- **Öğretici değer:** Kütle = yoğunluk × hacim; kalınlık ve yoğunluk iki ayrı kaldıraçtır; sınıf adındaki sayı (G2/350) kuru yoğunluğu anlatır; hafif yapı kütlesi → deprem yükü ilişkisi (ODTÜ çalışması). 'Hafif' soyut sıfattan ölçülebilir kg'a iner.
- **Pazarlama değeri:** Taşıma, işçilik ve temel yükü konuşmalarına rakamsız söz vermeden kapı açar; kullanıcı kendi malzemesini girerek kıyası kendisi üretir (iddia bizden değil, hesap kullanıcıdan); ODTÜ üçüncü taraf güvencesi. Mimar/mühendis için 'kütle' dili, yapı sahibi için 'hafif = rahat' sezgisi.
- **Veri ve kaynak:** 300–600 kg/m³ (G1/300 – G4/600; Ürün sınıfları); 350 = G2/350 sınıf adından; U blok G4/06 600 kg/m³ (Ürün föyleri); EGEPOR 150–200 kg/m³ kuru (Ürün föyleri); blok 60 × 25 cm; kalınlık 5–35 cm (Ürün föyleri; teyit akt-s1); −%17 yapı kütlesi (ODTÜ çalışması, 8 katlı örnek bina hesabı). Hesap örnekleri: 60 × 25 × 20 cm blok = 0,03 m³ → 9–18 kg; 1 m² × 20 cm duvar → 60–120 kg; 1 m² × 35 cm → 105–210 kg; EGEPOR 1 m² × 5 cm → 7,5–10 kg. TEYİT GEREKLİ (kullanılmaz): G3 sınıfı yoğunluğu, nem etkisi, 'suda yüzer' ifadesi, −%17'nin kapsamı (yalnız panel mi tüm sistem mi — etiket birebir kalır), taban kesme −%14 (README'deki eski karta ait; DEVIR.md/dil.js'te yok).
- **Teknik:** SVG terazi (≈40 düğüm; CSS transform: rotate geçişi 300 ms), native range; rAF yok → ≤0,1 ms. Hücre şematiği: 30 daireli sabit SVG, opacity ile seyreltilir. Canvas yok. JS ≈3 KB. Film tarafı: akt-s3'te G1–G4 durağan kare/kaydırıcı yok (tezgâhta yan yana G1/G2/G4 blok, tek sürekli pan); modül yalnız panel/overlay (t=99–100 vuruşunda rakam kartı köşesinde 'Dene' olarak eklenir; çip t=100'de açılır, t=99'da Soru 3 çipi vardır). Efor ≈ 1 gün.
- **TR metin:** chip: Tartıya koy | baslik: Bir blok kaç kilo? | alanlar: Yoğunluk (kg/m³) · Kalınlık (cm) · Ürün: Duvar bloğu · U blok · EGEPOR | sonuc: Tek blok {b1}–{b2} kg · 1 m² duvar {m1}–{m2} kg | kendi: Kendi duvarınızı girin (yoğunluk, kalınlık) | odtu: Yapı kütlesi −%17 · ODTÜ çalışması, 8 katlı örnek bina hesabı · Daha hafif bina, daha düşük deprem yükü. | not: Kuru birim hacim ağırlığıdır.
- **EN metin:** chip: Put it on the scale | title: How heavy is one block? | fields: Density (kg/m³) · Thickness (cm) · Product: Wall block · U-block · EGEPOR | result: One block {b1}–{b2} kg · 1 m² of wall {m1}–{m2} kg | own: Enter your own wall (density, thickness) | metu: Building mass −17% · METU study, calculation for an 8-storey sample building · A lighter building means a lower seismic load. | note: Values are for dry density.
- **Kural riski:** 'Suda yüzer' ve diğer çıkarımlı iddialar yok (akt-s3 açık sorusu). Kıyas malzemesi rakamı uydurulmaz: yalnız kullanıcı girer. ODTÜ etiketi birebir 'ODTÜ çalışması, 8 katlı örnek bina hesabı'; −%17 'yapı kütlesi' dışına taşırılmaz (deprem yükü yüzdesi verilmez). Birim hacim ağırlığı kuru; şantiye/nem ağırlığı farklı olabilir notu. Lime yalnız Ege blok/levha; kıyas kefesi gri.

### Isı yolculuğu: λ'dan R ve U (`isi_yolculugu`) — efor: orta
- **Nerede:** s3 Gözenek (Perde 4) · film t=96–97 sn ('λ 0,08 · W/mK · G2/350 duvar tasarım değeri' rakamı t=96; kartın köşesinde 'Kalınlığı dene') · ikinci giriş: s1 t=64–65 sn (EGEPOR rakam kartı λ 0,051–0,062) · araç rafı.
- **Ne yapar:** Duvar kesiti (iç | duvar | dış) üzerinde ısı yolculuğu: malzeme seç (G2/350 duvar λ 0,08 tasarım · U blok G4/06 λ 0,16 kuru · EGEPOR λ 0,051–0,062 kuru, iki uç gölge bant), kalınlık kaydırıcısı (5–35 cm), iç/dış sıcaklık kaydırıcıları (örnek senaryo). Çıktı: R = d/λ (m²K/W), U ≈ λ/d (W/m²K, yüzey dirençleri hariç), ısı akısı q = ΔT·λ/d (W/m²), duvar içinde doğrusal sıcaklık profili. 50 turuncu ısı damlası iç yüzden dışa akar; hız ve sıklık q ile orantılıdır: duvarı kalınlaştırdıkça damlalar yavaşlar ve seyrekleşir. 'Aynı malzeme, ikinci duvar' yan yana (ör. 20 cm ↔ 25 cm) farkı gösterir. Film gözenek ölçeğinde (isi_akis.js), bu modül duvar ölçeğinde: 'gözenekten duvara' ölçek zinciri.
- **Öğretici değer:** λ, R, U kavramları ve ilişkisi (R = d/λ; U ≈ 1/R): kalınlık ↔ iletkenlik, neden iki kaldıraç; λ'nın hangi koşulda verildiğini (tasarım / kuru) okumayı öğretir. Isı geçişinin duvar içinde doğrusal düştüğünü görünür kılar.
- **Pazarlama değeri:** λ rakamı soyut kalır; kaydırıcıyla duvara dönüşür. Mimar/mühendis kitlesine 'hesabı gösteren üretici' güveni; teknik föy bağlantısı (cta.foyler); G2/350 değerinin ortak rakamlardan geldiği açıkça yazılır. Yapı sahibi için 'kalınlık seçimi' kararını destekler.
- **Veri ve kaynak:** λ 0,08 W/mK: G2/350 duvar tasarım değeri (Ege Gazbeton ortak rakamlar); λ 0,16 W/mK kuru: U blok G4/06 (Ürün föyleri); λ 0,051–0,062 W/mK kuru: EGEPOR (Ürün föyleri); kalınlık 5–35 cm (Ürün föyleri; teyit akt-s1); formüller R = d/λ, U ≈ λ/d, q = ΔT·λ/d (fizik, hesap). Örnek (hesap, G2/350 λ 0,08): 20 cm → R 2,50, U ≈ 0,40; 25 cm → R 3,13, U ≈ 0,32; 35 cm → R 4,38, U ≈ 0,23. Sıcaklıklar (varsayılan iç 20, dış 0 °C) kullanıcı senaryosudur, ürün verisi değildir. TEYİT GEREKLİ (ekranda yok): yüzey dirençleri (Rsi/Rse), TS 825 sınır değerleri, yönetmelik kıyası.
- **Teknik:** 2B tuval 360 × 200 CSS px (DPR ≤1,25) + SVG profil (≈30 düğüm). 50 damla; rAF yalnız panel görünürken ve sekme açıkken, dt ≤0,05 sabitlemeli; ≤0,5 ms/kare; IntersectionObserver + visibilitychange ile durur. Hareket azaltmada oklar statik, damla yok. Bitmap yok, bellek <1 MB. JS ≈6 KB. Efor ≈ 2 gün.
- **TR metin:** chip: Kalınlığı dene | baslik: Isı duvardan nasıl geçer? | alanlar: Malzeme · Kalınlık (cm) · İç sıcaklık · Dış sıcaklık (örnek senaryo) | sonuc: R = {r} m²K/W · U ≈ {u} W/m²K · q = {q} W/m² | etiket: λ {l} W/mK ({tur}) | not: U, yüzey dirençleri hariç yaklaşık değerdir. Tasarım ve kuru λ değerleri birbiriyle kıyaslanmaz.
- **EN metin:** chip: Try the thickness | title: How does heat cross a wall? | fields: Material · Thickness (cm) · Indoor temperature · Outdoor temperature (example scenario) | result: R = {r} m²K/W · U ≈ {u} W/m²K · q = {q} W/m² | label: λ {l} W/mK ({tur}) | note: U is approximate, excluding surface resistances. Design and dry λ values are not compared with each other.
- **Kural riski:** En büyük risk: tasarım değeri (0,08) ile kuru değerlerin (0,16; 0,051–0,062) aynı ekranda 'daha iyi/kötü' sıralamasına dönüşmesi → ürünler arası sıralama yok, her malzemenin yanında λ türü yazılı; kıyas 'aynı malzeme, farklı kalınlık' ile yapılır. U 'yaklaşık, yüzey dirençleri hariç' etiketli; yönetmelik uygunluğu iddia edilmez; ısı tasarrufu yüzdesi verilmez. Isı rengi turuncu → mavi (yeşil değil); lime yalnız Ege malzeme dilimi.

### Hücreye dokun — kapalı hava hücresi (`hucre_dokun`) — efor: orta
- **Nerede:** s3 Gözenek (Perde 4) · film t=91–95 sn (t=91 'Gözeneklerde hapsolmuş hava' + 'dokunun' ipucu; t=92 'Kapalı hava hücresi' etiketi; t=93 hayalet hücreler; t=94 ısı gözenekleri dolanır; t=95 mineral duvar; akt-s3) · araç rafı.
- **Ne yapar:** Film üzerinde 6 SVG halka (meta çapaları hucre_1…6; akt-s3) imleçle tek tek parlar; dokunulan hücre lime halka alır ve 'mikroskop kartı' açılır: 2B kesit — mineral duvar (gri) içinde hava hücresi, 40 hava noktası hücrede hapsolmuş titreşir. Soldan ısı darbesi (turuncu halka dalgası) gelir: hücrenin kenarına ulaşınca hava içinden değil mineral duvar boyunca dolanır ve yavaşlar. Anahtar 'Kapalı hücre ↔ açık boşluk': açık boşlukta noktalar akar (hava hareketi) ve ısı hızla geçer — fark yaşatılır. 'Hücre çokluğu' kaydırıcısı (az ↔ çok, şematik): darbenin karşıya varış gecikmesi artar. Her halka aynı 'Kapalı hava hücresi' kartını (dil.js hucre), mineral duvara dokunmak 'Mineral matris' kartını (dil.js matris) açar.
- **Öğretici değer:** Gazbetonun yalıtım nedeni: hapsolmuş, hareketsiz hava + mineral yolun uzaması (dil.js onaylı cümleler). Kapalı/açık boşluk ayrımı; 'ısı hava hareketiyle de taşınır' sezgisi.
- **Pazarlama değeri:** Ürünün 'neden?' sorusuna oyunla cevap: 3B filmden sonra elle öğrenme; kısa (≈20 sn) etkileşim; 'Isıyı tutan, içindeki hava' vaadini yaşatır; SON'daki canlı gözenek katmanıyla görsel dilde süreklilik (aynı lime halka dili).
- **Veri ve kaynak:** Yalnız dil.js kartları: hucre ('Hücredeki hava hareket etmez; ısı kolay geçemez.'), matris ('Otoklavda buharla sertleşen kalsiyum silikat yapı.'), i2.metin ('Kapalı hava hücreleri ısının geçişini yavaşlatır.'). Hiçbir sayı yok: gözenek boyutu (mm), hacimce hava oranı, hücre sayısı TEYİT GEREKLİ (akt-s2/s3 açık soruları) → şematik, 'ölçek yok, temsili' etiketi.
- **Teknik:** Halkalar: akt-s3'ün SVG katmanı (Sahne.renderHotspots ile aynı çapa hattı; ≤8 düğüm). Mikroskop kartı: 2B tuval 280 × 200 (DPR ≤1,25), 40 + 24 parçacık, yalnız kart açıkken rAF; ≤0,4 ms/kare; bitmap yok. Isı dalgası: halka yarıçapı + mineral yol üzerinde kenar boyunca ilerleyen nokta (ön hesaplı 40 noktalı yol). Hareket azaltmada tek durağan çizim + açıklama. JS ≈5 KB. Efor ≈ 1,5–2 gün.
- **TR metin:** ipucu: Bir hücreye dokunun. | kart-baslik: Kapalı hava hücresi | tuslar: Kapalı hücre · Açık boşluk | slider: Hücre çokluğu | alt: Hücredeki hava hareket etmez; ısı kolay geçemez. | not: Şematik gösterim; ölçek ve oran temsilidir.
- **EN metin:** hint: Tap a cell. | card-title: Closed air cell | buttons: Closed cell · Open void | slider: Number of cells | sub: The air in the cell does not move; heat cannot pass easily. | note: Schematic illustration; scale and proportions are representative.
- **Kural riski:** Gözenek ölçeği/oranı sayı olarak verilmez (teyit gerekli). 'Açık boşluk' karşı örneği bir rakip ürünü ima etmemeli: genel fizik etiketi. Lime halka = ürünün gözeneği (bizim); hammadde yeşili değil. 3B karede yazı yok: etiketler HTML/SVG. Simülasyon ürün performans garantisi gibi okunmamalı → 'şematik' notu; film içindeki isi_akis.js ile çelişen yön/hız olmamalı.

### İhracat kıtaları — 5 halka ve 25+ ülke sayacı (`ihracat_kitalar`) — efor: kucuk
- **Nerede:** s5 Dünya (Perde 6) · film t=122–131 sn (t=122 'beş kıta' cümlesi; t=124 Avrupa, t=125 Afrika, t=126 Amerika, t=128 Asya, t=130 Okyanusya + '25+ ülke'; t=131 '5 kıta'; akt-s5) · SON kanıt kartında (t=144) yeniden kullanılır.
- **Ne yapar:** Ekranda 5 halkalı sayaç (SVG): her kıtaya yay vardığında bir halka dolar (kaydırmaya bağlı; geri kaydırınca boşalır). Halkaya dokununca ilgili varışın halkası küre üzerinde yeniden nabız atar (kare çapası v_avrupa…v_okyanusya) — ülke/sayı/kıta bazında bilgi verilmez. '25+' sayacı p'ye bağlı 0 → 25 ve sonunda '+' belirir. Rakam kartına dokununca 'kitalar' kartı: '5 kıtada 25'ten fazla ülkeye ihracat' + kaynak. Etkileşim: kaydırma hızı = yay üstündeki ışık damlasının hızı (akt-s5 t=123/125). Kıta adları yalnız onay gelirse (açık soru); onay yoksa halkalar numaralı (1–5).
- **Öğretici değer:** Coğrafi ölçek: iki fabrika (Söke, İzmir) → 5 kıta; sayma ritmiyle '5' akılda kalır; Türkiye silüeti gerçek poligon; ülke adı vermeden güven.
- **Pazarlama değeri:** İhracat alıcısı/bayi kitlesine güven (hero kitle seçicisindeki 'İhracat alıcısı / bayiyim' → /ihracat/); sayaç tamamlandığı anda CTA ('İhracat için iletişim'); 'dünyaya ihracat yapan yerel üretici' prestiji.
- **Veri ve kaynak:** 25+ ülke · 5 kıta — Ege Gazbeton ihracat bölümü (tek kaynak, DEVIR §2). Ülke adı, ülke sınırı, müşteri sayısı, fiyat, liman adı (Aliağa/Alsancak kaynaksız, akt-s5 açık sorusu) YOK. TEYİT GEREKLİ: güncellik ve tarih (dış haberlerde 19 ülke / 4 kıta yazıyor; akt-s5 açık sorusu) → yayın öncesi ihracat bölümünden yazılı teyit.
- **Teknik:** SVG 5 halka + sayaç (≈25 düğüm); halka dolumu stroke-dashoffset (p'ye bağlı, Sahne.render içinde, ek rAF yok); sayaç metni yalnız tamsayı değişince yazılır. Küre/yay filmden (akt-s5: 12 kare/sn, 193 kare). Etiketler HTML. ≤0,1 ms/kare. Bellek ≈0; JS ≈2 KB. Efor ≈ 1 gün.
- **TR metin:** sayac: 5 kıta · 25+ ülke | halkalar: Avrupa · Afrika · Amerika · Asya · Okyanusya (onaya bağlı; yoksa 1–5) | kart: 5 kıtada 25'ten fazla ülkeye ihracat. Kaynak: Ege Gazbeton ihracat bölümü | ipucu: Halkaya dokunun.
- **EN metin:** counter: 5 continents · 25+ countries | rings: Europe · Africa · Americas · Asia · Oceania (subject to approval; otherwise 1–5) | card: Exports to more than 25 countries on five continents. Source: Ege Gazbeton export department | hint: Tap a ring.
- **Kural riski:** En sıkı kural alanı: yalnız '25+ ülke · 5 kıta'; ülke adı/sınırı/müşteri sayısı/fiyat yok; Türkiye vurgusu yalnız gerçek poligon (modül Türkiye'ye dokunmaz). Küreye lime sızdırılmaz (akt-s5); sayaç halkası UI olarak lime olabilir. 25+ doğrulaması ve 19/4 çelişkisi görünürlük riski: yayın öncesi yazılı teyit. Kıta adı etiketi onaya bağlı; haritada sınır çizgisi yok.

### Tır ve palet etiketi — palet röntgeni (`tir_palet`) — efor: orta
- **Nerede:** s0 Hayalden yuvaya (Perde 1) · film t=20–23 sn (sokakta geçen Ege tırı: takip eden 'Ege Gazbeton' etiketi t=20; palet halkası t=21–22; 'Ürünleri gör ↓' mikro bağlantısı t=23) · s4 Yol (Perde 5) · t=106–117 sn (palet t=106, fabrika t=108, kayış t=109, tır etiketi t=110–117) · s3 t=102 palet pininden de açılır.
- **Ne yapar:** (1) Tırı izleyen HTML etiketi 'Ege Gazbeton' (meta çapası 'tir' → translate3d; kaydırma hızıyla 1:1; kadraj dışına çıkınca küçük okla kenara yapışır). (2) Palete dokun: 'palet röntgeni' açılır — patlatılmış SVG: ahşap palet → şaşırtmalı blok katları → köşe koruyucu → lime streç film (sarım çizgileri çizilir) → kayış (amber); 'Patlat' kaydırıcısı; her parçaya dokununca ad + tek cümle ('Lime streç: paletleri sarar', 'Kayış: yükü bağlar'). (3) Tır ve forklift parça noktaları (kabin, ikiz arka aks, dorse bağlama, forklift çatalı) — yalnız film detayı güçlü olduğunda açılır; amaç 'ayrıntı' algısını artırmak (önceki oturum şikâyeti). Gerçek takip/ETA/konum verisi YOK.
- **Öğretici değer:** Ürünün sahaya nasıl hazırlanıp gittiği: palet yapısı, streç ve kayış; ambalajın korumadaki rolü (tek cümle). s0'da yoldan geçen tır ile s4'te doğduğu fabrika arasında bağ kurar.
- **Pazarlama değeri:** Marka görünürlüğü (lime streç = Ege imzası); lojistik güveni (bayi/inşaat firması kitlesi); s0 'tır'dan s4 'fabrika'ya hikâye kafiyesi: etiket her iki yerde aynı bileşen. 'Ürünleri gör ↓' mikro bağlantısı ürün turuna atlatır (urun_secici/ortak.saniyeyeGit).
- **Veri ve kaynak:** dil.js tir kartı: 'Lime streçli paletler: Söke ve İzmir'den sahaya.'; 2 fabrika (Söke & İzmir; Ege Gazbeton ortak rakamlar). TEYİT GEREKLİ (ekranda yok): palet başına blok adedi/m³, palet ölçüsü, tır kapasitesi, sefer sayısı ('bu ev kaç tır?' hesabı ancak föy/lojistik rakamı gelirse eklenir). Konum/ETA/hız/plaka: uydurulmaz.
- **Teknik:** Etiket: tek <button> DOM, transform; konum Sahne.renderHotspots hattında (ek maliyet ≈0). Palet röntgeni: inline SVG ≈60 düğüm, CSS transform (patlatma kaydırıcısı → --patla), streç sarımı stroke-dashoffset. Tuval yok; rAF yok. s0 ve s4 için aynı bileşen, farklı çapalar (meta 'tir', 'palet', 'ankraj'). Bellek ≈0; JS ≈4 KB. Telefonda röntgen alt sheet (60svh, kilitsiz). Efor ≈ 2 gün.
- **TR metin:** etiket: Ege Gazbeton | palet: Palet röntgeni | parcalar: Ahşap palet · Blok katları · Köşe koruyucu · Lime streç · Kayış | kaydirici: Patlat | mikro: Ürünleri gör ↓ | not: Şematik; ölçüler gösterilmez.
- **EN metin:** label: Ege Gazbeton | pallet: Pallet X-ray | parts: Wooden pallet · Block layers · Corner protector · Lime stretch film · Strap | slider: Explode | micro: See the products ↓ | note: Schematic; dimensions are not shown.
- **Kural riski:** Logo yalnız en sonda: tır kabininde logo yok, HTML 'Ege Gazbeton' etiketi (DEVIR teyit #1: gerçek logo dosyası gelirse karar). Lime = streç film (bizim ambalaj); kayış amber, dorse/çelik gri, palet ahşap kahve; yeşil kayış/çelik yok. Sahte takip/ETA/hız/plaka yok; palet/tır rakamı yok. Tır/araç ayrıntısı hâlâ zayıfsa parça noktaları açılmaz (görsel kalite kapısı). Sürücü/insan: yüzsüz, orta-uzak plan.

### Karışımı sen hazırla (`karisim_hazirla`) — efor: orta
- **Nerede:** s2 Doğuş (Perde 3) · film t=78–79 sn ('Karışım — Su katılır' t=78; 'Kalıp dolar' t=79; çip t=78'de belirir) · beş hammadde noktaları (t=73–77) tamamlanınca çip nabız atar · araç rafı.
- **Ne yapar:** Sol sütunda küçük bir tezgâh: 5 hammadde kapsülü (kum, kireç, çimento, alçı, alüminyum tozu) + su. Kapsülü mikser kabına sürükle (veya dokun) → kabın rengi/dokusu değişir, kapsülün görevi tek sözcükle çıkar (Ana hammadde · Bağlayıcı · Dayanımı destekler · Prizi düzenler · Kabartır). 'Karıştır ve dök' → karışım kalıba dolar ve kabarma animasyonu başlar: alüminyum VARSA hücreler (SVG daireler) çoğalır, kek şişer; YOKSA kek şişmez, hücre oluşmaz. Eksik her hammadde için görevini söyleyen tek satır ('Eksik: bağlayıcı'). Sıra serbest; miktar/oran YOK (şematik). Tam karışımda ödül: 'Hava hücreleri oluştu' + kek lime kenar (ürün doğdu) + zincirde (uretim_zinciri) 'Kabarma' ilerlemesi.
- **Öğretici değer:** Her hammaddenin görevi (dil.js onaylı cümleler); alüminyum = kabartıcı → hava hücresi → yalıtım zincirini kurar; 'çıkarırsam ne olur?' deneyerek öğrenme (sorgulayarak keşif, ezber değil).
- **Pazarlama değeri:** Üretici bilgisine marka sahipliği ('bunu bilen firma'); geniş kitle (öğrenci, çocuklu aile, mimarlık öğrencisi) ilgisi; hafif, rakamsız 'Karışım ustası' rozeti ve ekran kaydı/paylaşım anı; sevimli ve hatırlanır.
- **Veri ve kaynak:** Görev cümleleri dil.js'ten: kum 'Silis kumu: gazbetonun ana hammaddesi.'; kireç 'Karışımın bağlayıcısı.' (Söke'de günde 200 ton kapasiteli kendi kireç tesisi; Ege Gazbeton ortak rakamlar); çimento 'Dayanımı destekleyen bağlayıcı.'; alçı 'Prizlenmeyi düzenler.'; alüminyum 'Kireçle tepkimeye girip hidrojen açığa çıkarır: karışım kabarır, hava hücreleri oluşur.' Gerçek reçete/oran/süre: gösterilmez (ticari gizlilik + teyit gerekli). Kimyasal denklem yok (akt-s2'deki 'Al + Ca(OH)₂ + H₂O → H₂↑' şeması teyit gerekli; modül yalnız sözcükle anlatır). 'Priz' sözlüğü teyit gerekli.
- **Teknik:** HTML + pointer events (HTML5 DnD yok: mobilde çalışmaz); 6 kapsül <button> (klavyede Enter ile kaba eklenir). Kabarma: 36 SVG daire, CSS scale/transform (≤40 düğüm); toplam DOM ≈70; rAF yok (CSS animasyon). ≤0,3 ms. Bellek ≈0; JS ≈4 KB. Çevrimdışı: tamamen yerel. Hareket azaltmada animasyonsuz sonuç. Efor ≈ 2 gün.
- **TR metin:** chip: Hazırla | baslik: Karışımı sen hazırla | kapsuller: Kum · Kireç · Çimento · Alçı · Alüminyum tozu · Su | gorevler: Ana hammadde · Bağlayıcı · Dayanımı destekler · Prizi düzenler · Kabartır | dugme: Karıştır ve dök | tam: Kabardı: hava hücreleri oluştu. | eksik-alum: Alüminyum yok: kabarma yok. | eksik-kirec: Eksik: bağlayıcı. | not: Şematik; gerçek oranlar paylaşılmaz.
- **EN metin:** chip: Prepare | title: Prepare the mix yourself | capsules: Sand · Lime · Cement · Gypsum · Aluminium powder · Water | roles: Main raw material · Binder · Supports strength · Regulates setting · Makes it rise | button: Mix and pour | full: It rose: air cells formed. | missing-alu: No aluminium: no rising. | missing-lime: Missing: binder. | note: Schematic; real proportions are not shared.
- **Kural riski:** Hammadde renkleri: kireç beyaz (lime-yeşil DEĞİL), alüminyum gümüş-gri, çimento koyu gri, kum bej; lime yalnız bitmiş kek kenarı (ürün). Oran/miktar/süre yok; 'eksik olursa' ifadeleri yalnız onaylı görev cümlelerinden türetilir (ör. 'kireç yok → bağlayıcı eksik'; çökme/kırılma gibi fiziksel iddia yok). Kimyasal denklem ve sıcaklık yok. Temsili tezgâh gerçek Söke hattı değildir. İnsan figürü/yüz yok.

### Üretim zinciri çizelgesi — hammaddeden yola (`uretim_zinciri`) — efor: orta
- **Nerede:** s2 Doğuş (Perde 3) t=80 sn'den s4 Yol (Perde 5) t=117 sn'e kalıcı alt şerit (s3'te sönük): düğümler Hammadde t=73–77 · Karışım t=78 · Kalıp t=79 · Kabarma t=80–82 · Tel kesim t=83–84 · Otoklav t=85–86 · Blok t=87 · Palet t=102–106 · Yola t=110.
- **Ne yapar:** Ekranın altında 8 düğümlü yatay çizelge ('Hammadde → Karışım → Kalıp → Kabarma → Tel kesim → Otoklav → Palet → Yola'); 'Buradasınız' imleci kaydırmayla ilerler, geçilen düğümler dolar. Düğüme dokun: 4× hızla o ana sar + kart (NOKTALAR: kum, kirec, cimento, alci, aluminyum, kabarma, kesim, matris, blok; yeni: kalip, otoklav, palet). Her düğümde yalnız aktifken oynayan 1 mikro ikon animasyonu (kum yığını, toz bulutu, daire çoğalması, tel geçişi, buhar, streç sarılması, tır). akt-s2'nin 5 adımlı stepper'ını (Hammadde, Karışım, Kabarma, Kesim, Otoklav) 8 düğüme genişletir ve s3–s4'e taşır; 'üretimden sahaya' tek zincir olarak okunur.
- **Öğretici değer:** Sıra ve gerekçe: hammadde → karışım → kabarma → kesim → otoklav → paketleme → sevkiyat; neyin neden önce geldiği. 'Kabartan alüminyum', 'otoklavda buharla sertleşir' (süre/basınç yok) akılda kalır; zincirin tamamı tek ekranda görülür.
- **Pazarlama değeri:** Üretim kontrolü ve ölçek hissi: 'iki fabrika, tek standart'; kendi kireç tesisi (günde 200 t) ve 1.100.000 m³ kapasite bu zincirde fabrikaya bağlanır; bayi/mimar sunumlarında kurumsal anlatı olarak ekran görüntüsüne uygun.
- **Veri ve kaynak:** Sıra: dil.js kartları ve i1 adımları (Karışım, Kabarma, Kesim ve otoklav). Rakam yok; yalnız kart bağlantıları: 200 t/gün kireç tesisi (Söke), 1.100.000 m³ üretim kapasitesi, 2 fabrika (Ege Gazbeton ortak rakamlar). TEYİT GEREKLİ: süreler, sıcaklık, basınç (otoklav değerleri, ön sertleşme süresi; akt-s2 açık sorusu) → çizelge sıralıdır, zaman ölçekli değildir.
- **Teknik:** Tek inline SVG şerit (≈50 düğüm) + 8 ikon <symbol>; aktif düğüm CSS animasyonu (transform/opacity); düğüm tıklayınca ortak.saniyeyeGit(t) (t × 22 vh; main.js bas[] ile). Kaydırma ilerlemesi → imleç translateX (Sahne.render içinde; ek rAF yok). Mobilde şerit 44 px yükseklikte yatay kaydırılabilir. Bellek ≈0. JS ≈4 KB. Efor ≈ 2 gün.
- **TR metin:** dugumler: Hammadde · Karışım · Kalıp · Kabarma · Tel kesim · Otoklav · Palet · Yola | imlec: Buradasınız | ipucu: Bir adıma dokunun.
- **EN metin:** nodes: Raw materials · Mixing · Mould · Rising · Wire cutting · Autoclave · Pallet · On the road | marker: You are here | hint: Tap a step.
- **Kural riski:** Süre/sıcaklık/basınç yazılmaz. Kalıp, otoklav ve tel kesme makineleri temsili (akt-s2 açık sorusu: gerçek Söke hattı referansı yok). Lime yalnız blok, palet streci ve fabrika şeridi; kalıp, tel, ray, otoklav gri/beyaz/amber. Düğüm etiketleri ≤2 kelime (okuma hızı). Şerit anlatım metniyle çakışmamalı (alt 56 px).

### A1 sınıf merdiveni — yangına tepki sınıfı (`a1_demo`) — efor: kucuk
- **Nerede:** s3 Gözenek (Perde 4) · film t=97–98 sn (t=97 'A1 · yangına tepki sınıfı' rakamı; t=98 'EN 13501-1 · CE belgeleri' + sınıf merdiveni çizilir; nötr tezgâh F42–F53, akt-s3; t=98–99 Soru 3 çipi (bilgi_yarismasi) belirir: A1 mini kartı açıkken soru bekler, çünkü kart cevabı verir) · araç rafı.
- **Ne yapar:** Nötr tezgâh sahnesinde HTML/SVG 'sınıf merdiveni' (7 basamak: A1 A2 B C D E F; yalnız A1 vurgulu, ötekiler sönük ve dokunulmaz) kaydırmayla alttan çizilir; A1 rozetine/basamağına dokununca 'Yangına tepki sınıfı' mini kartı açılır: 'Yangına tepki sınıfı, malzemenin yangına nasıl tepki verdiğini sınıflandırır.' (genel tanım; teyit gerekli), altında 'A1 · yangına tepki sınıfı · EN 13501-1' ve kaynak 'CE belgeleri' + CE belgeleri/teknik föy bağlantısı. Sahnede ve modülde alev, kor, ısıl degrade, 'öbür yüz serin' görseli, süre ve sıcaklık YOK. Önceki 'Alevi yaklaştır — basılı tut' alev flipbook'u DÜŞTÜ: yangın direnci (EN 13501-2) belgesi yok; 'alev bloğa tutunmaz, yüzey değişmez' görseli pratikte 'yanmaz' gösterimi olurdu; basılı tut flipbook'u ile akt-s3'ün kaydırmayla oynayan kareleri de uyuşmuyordu. Modülün kendi karesi/oynatıcısı yok: yalnız film kareleri + SVG/HTML.
- **Öğretici değer:** 'Yangına tepki' kavramını öğretir; A1'in bir sınıf adı olduğunu (rakam/süre değil) ve sınıfın EN 13501-1 standardından geldiğini gösterir. Yangın direnci (EN 13501-2) ayrımı belge gelene dek anlatılmaz, yalnız 'teyit gerekli' notuyla beklemede.
- **Pazarlama değeri:** Güvenlik güveni en yüksek duygusal değerlerden; bilgi tonuyla (sınıf adı + belge kapısı, dramatik görsel yok) verilir. CE belgeleri bağlantısı (/teknik-foyler/) mimar ve bayi için kanıt kapısı. Aynı sahnedeki λ ve 300–600 mührüyle 'üç kaynaklı güven' bütünlüğü.
- **Veri ve kaynak:** A1, yangına tepki sınıfı (EN 13501-1) — CE belgeleri (dil.js i2.k2). Başka rakam YOK: süre, °C, direnç yok. TEYİT GEREKLİ: sınıf merdiveni harfleri (A1 A2 B C D E F) EN 13501-1 standardından alınır, ekranda yalnız A1 vurgulu (teyit gelmezse yalnız A1 rozeti + kart); yangın direnci (EN 13501-2) belgesi yok (akt-s3 açık sorusu) → 'öbür yüz serin', alev ve ısıl görsel kullanılmaz; 'yangına tepki' genel tanım cümlesi.
- **Teknik:** Yalnız SVG + HTML: merdiven ≈20 düğüm (7 basamak + etiket), kaydırmaya bağlı stroke-dashoffset çizimi (ayrı rAF yok; sahne kick() hattında), mini kart statik. Bitmap, canvas, flipbook, parçacık YOK (ek bellek ≈0, ≤0,1 ms). Native button (Enter/Space), aria-label 'A1, yangına tepki sınıfı'. Hareket azaltma: merdiven çizilmiş halde, statik. Efor ≈ 0,5–0,75 gün (önceki ≈1,5 gün; flipbook render'ı ve JS çıktı).
- **TR metin:** chip: Sınıfı gör | etiket: A1 · yangına tepki sınıfı | alt: EN 13501-1 · CE belgeleri | kart: Yangına tepki sınıfı, malzemenin yangına nasıl tepki verdiğini sınıflandırır. | not: Şematik gösterim.
- **EN metin:** chip: See the class | label: A1 · reaction-to-fire class | sub: EN 13501-1 · CE certificates | card: The reaction-to-fire class classifies how a material reacts to fire. | note: Schematic illustration.
- **Kural riski:** 'Yanmaz' sözcüğü hiçbir yerde kullanılmaz (şık, alt yazı, aria-label dahil); üretici sayfası 'A1 Hiç Yanmaz' yazsa da bizde yasak. Alev, kor, ısıl degrade, 'serin yüz', süre, °C ve 'alev bloğa tutunmaz / yüzey değişmez' izlenimi veren her görsel YOK; 'yangın güvenliği garantisi' izlenimi verilmez. Alev ya da yangın çağrıştıran öğe, yangın direnci belgesi gelene dek geri gelmez; gelirse ayrı karar olarak yalnız bloğa değmeyen, süresiz, etki göstermeyen şematik biçimde değerlendirilir. EN 13501-2 ayrımı belge gelene dek kullanılmaz. Merdivende lime yok (A1 sınıfı ürün değil; renk nötr). Metin kontrastı (WCAG).

**Doğrulanamayanlar (ekranda kullanılmaz / teyit gerekli):**

- G3 sınıfının yoğunluğu ve G1–G4'ün tam listesi (yalnız G1/300, G2/350, G4/600 bilinir)
- Duvar bloğu stok kalınlıkları ve 5–35 cm'nin üretici teyidi
- Fire/kırık payı, tutkal tüketimi (kg/m²), palet başına blok adedi ve m³, palet ölçüsü, tır kapasitesi
- Hacimce hava oranı, gözenek boyutu (mm), hücre sayısı
- Otoklav sıcaklık/basınç/süre, ön sertleşme süresi, kabarma süresi, kimyasal tepkime denklemi, 'priz' sözlüğü
- ODTÜ −%17'nin kapsamı (yalnız panel mi tüm sistem mi) ve README'deki eski −%14 taban kesme kartı
- A1 sınıf merdiveni harfleri ve 'yangına tepki' genel tanımı; yangın direnci (EN 13501-2) belgesi; 'öbür yüz serin' görseli
- Yüzey dirençleri (Rsi/Rse), TS 825 sınır değerleri, yönetmelik kıyası
- 'Isı köprüsü' ifadesi (EGEPOR); U bloktaki '50 kgf/cm²' değerinin etiketi
- 'Suda yüzer' ifadesi
- Kıta adlarının ekranda gösterilmesi; 25+ ülke · 5 kıta'nın güncel yazılı teyidi (dış haberlerde 19 ülke / 4 kıta); Aliağa/Alsancak liman ifadesi
- Gerçek logo dosyası (tır kabini kararı)

## 5. Pazarlama ve dönüşüm akışı

{'amac': 'Ege Gazbeton hikâyesinin pazarlama ve dönüşüm tasarımı: duygu → kanıt → güç → eylem hunisi, üç kitle yolu, saniye saniye CTA yerleşimi, bağlam taşıyan bağlantılar, güven işaretleri, çerezsiz dataLayer ölçümü, marka (lime) görünürlüğü, SEO/paylaşım, mobil ve ilk 10 sn testi.', 'cta_ritmi': "Otomatik CTA pencereleri film saniyesinde: t=0 (hero), 23, 38, 64–67 (ilk ANA), 99, 115, 131, 142 (finale). Aralar 23, 15, 26, 35, 16, 16, 11 sn; s2 (70–90) CTA'sız; her pencere bir kanıttan hemen sonra gelir.", 'ana_kararlar': ["İlk CTA t=0'da (üst çubuk Teklif Al + hero'da tek lime ana düğme + 3 kitle çipi + atla); duygu sahnesinde (t=2–22) otomatik CTA yok; ilk ANA CTA t=64–67 (altı ürün sonrası); finalde t=142.", "Hero'dan Katalog/Teknik düğmeleri çıkar (tek ana eylem); yerlerine t=64, 99, 142 bağlamı.", 'Bağlantılarda ?kaynak=hikaye&dil=&urun=&kitle=&nokta= ; urun yalnız ölçülmüş ilgiden (süre + kart + çip), bellekte; statik href temiz.', 'Slogan açılışta değil finalde (öneri; s0/son planlarından sapma, açık soru 1). Logo yalnız t=140–141.', 'Telefonda iki hata: üst çubukta Teklif gizli ve kaydırma ipucu gizli; ayrıca .eg-rakam small gizliyor (kaynak kuralı ihlali).', 'Doğrulanmayan hiçbir sayı/belge ekranda yok: CE belge no, TS EN 771-4, ISO/TSE, kuruluş yılı, limanlar, teslim süresi = teyit gerekli.', 'Finale t=142–145 sadeleştirildi: t=142 ana CTA + 1 ikincil + 1 bağlam çipi; t=143 tek sıra kitle çipleri; t=144 statik kanıt kartları; t=145 ince tekrar izle. Alt sabit çubuk/WhatsApp (numara teyidi) ve quiz rozeti, gömülü mini hesap, Araçlar çekmecesi finalde yok.'], 'kaynak_dosyalar': ['DEVIR.md', 'src/hikaye/dil.js', 'src/hikaye/arayuz.js', 'src/hikaye/main.js', 'src/hikaye/ayarlar.js', 'giris-hikaye/index.html', 'giris-hikaye/assets/css/hikaye.css', 'plan/akt-s0..son.json (ajan planları)'], 'zaman_notu': 'Film saniyesi t; vh = t × 22 (akış başından). Perde sınırları: s0 0–32, s1 32–70, s2 70–90, s3 90–104, s4 104–120, s5 120–136, son 136–146 (toplam 146 sn = 3212 vh).'}

### Huni
- **1 · DUYGU** (0–32 sn, %21.9): Her yuva bir çizgiyle başlar; o yuvayı yuva yapan malzemedir. — izleyici: Sıcak merak → hayranlık (çizilen ev) → sahiplenme (sokak, aile) → huzur (akşam, yanan pencereler) → "bunun cevabı ne?" merakı.
- **2 · KANIT** (32–104 sn, %49.3): Altı ürün, tek mineral malzeme; hammaddesinden gözeneğine kadar açık. — izleyici: Keşif (altı ürün) → şaşkınlık (blok hammaddeye çözülür) → kavrayış (hacmin çoğu hava) → güven (üç kaynaklı rakam mührü).
- **3 · GÜÇ** (104–136 sn, %21.9): Ege'de üretilir, beş kıtada kullanılır. — izleyici: Gurur ve ölçek (saha yukarıdan) → "ürün yola çıktı" (tır) → sakin güç (küre, 25+ ülke · 5 kıta).
- **4 · EYLEM** (136–146 sn, %6.8): Güvenin adı Ege Gazbeton; sıradaki adım teklif. — izleyici: Sakin şaşkınlık → güven (logo, slogan) → net adım (tek lime düğme).
- **EYLEM KATMANI (SÜREKLİ)** (0–146 sn, %100.0): — — izleyici: Kontrol bende: zorlanmıyorum ama yol açık.

### Kitle yolları
- **Yapı sahibi / müteahhit (ev, bina yapan)** — çip: “Ev / bina yapıyorum” → `/duvar-tasarla/?kaynak=hikaye&dil={dil}&kitle=sahip&nokta=giris_kitle`
  - arar: Evim sağlam, rahat ve sıcak mı olur?
  - arar: Şantiyede iş kolay ve hızlı mı?
  - arar: Kaç m² / ne kadar? (fiyat hikâyede yok; teklife yönlendirilir)
- **Mimar / mühendis (proje, statik, yalıtım)** — çip: “Mimar / mühendisim” → `/teknik-foyler/?kaynak=hikaye&dil={dil}&kitle=mimar&nokta=giris_kitle`
  - arar: Hangi sınıf, hangi λ, hangi boyut?
  - arar: Belgesi ve standardı ne?
  - arar: Detay/föy nerede?
- **Bayi · ihracat alıcısı · toplu alıcı** — çip: “İhracat alıcısı / bayiyim” → `/ihracat/?kaynak=hikaye&dil={dil}&kitle=bayi&nokta=giris_kitle`
  - arar: Üretici mi, ölçeği ve sürekliliği ne?
  - arar: Kapasite, sevkiyat, paletleme?
  - arar: Kime, nasıl yazarım?

### CTA zaman çizelgesi

| Saniye | Yer | Metin (TR) | Bağlantı |
|---|---|---|---|
| 0–146 | Üst çubuk sağ (masaüstü). Telefonda: logo hikâye boyunca gizliyse kompakt 44 px düğme … | Teklif Al | `/teklif/?kaynak=hikaye&dil={dil}[&urun={urun}]&nokta=ust  (hikâye ekranda değilken kaynak=ust)` |
| 0–2 | Hero paneli (masaüstü sol, telefon üst), başlık + cümlenin altında; t=0'da hazır, ilk … | Teklif Al → | `/teklif/?kaynak=hikaye&dil={dil}&nokta=giris` |
| 0–2 | Hero, düğmenin altında tek satır "Size en uygun yol:" çipleri (ince çizgili, küçük). | Ev / bina yapıyorum | `/duvar-tasarla/?kaynak=hikaye&dil={dil}&kitle=sahip&nokta=giris_kitle` |
| 0–2 | Hero, aynı çip satırı. | Mimar / mühendisim | `/teknik-foyler/?kaynak=hikaye&dil={dil}&kitle=mimar&nokta=giris_kitle` |
| 0–2 | Hero, aynı çip satırı. Tarayıcı dili Türkçe değilse bu çip birinci sıraya alınır ve "View … | İhracat alıcısı / bayiyim | `/ihracat/?kaynak=hikaye&dil={dil}&kitle=bayi&nokta=giris_kitle` |
| 0–2 | Hero alt sırası (sol). t≥2'den sonra yolculuk çubuğundaki "Teklif" öğesi aynı işi görür. | Hikâyeyi atla | `#teklif  (sahneyeGit('son'): akışta p=0,62 = t≈142, CTA grubunun görünür olduğu an)` |
| 23–25 | Tırı izleyen "Ege Gazbeton" etiketinin hemen altı (mikro bağlantı, 14 px, ok ile). | Ürünleri gör ↓ | `iç bağlantı: sahneyeGit('s1')  → akış t=33 (ürün turu girişi). Parametre yok.` |
| 34–66 | Anlatım sütununun üstünde altı çip: Duvar · Lento · U blok · Tutkal · Panel · EGEPOR. … | Duvar · Lento · U blok · Tutkal · Panel · EGEPOR | `iç bağlantı: her çip kendi durağın başına kaydırır (t=36, 41, 46, 51, 56, 61). Parametre yok.` |
| 38–40 | Anlatım sütununun alt kenarı, "Düz · Geçmeli" etiketi ve rakamdan sonra; düğmesiz metin + … | Duvarlarınızı hesaplayın → | `/duvar-tasarla/?kaynak=hikaye&dil={dil}&urun=duvar&nokta=s1_duvar_hesapla` |
| 39–41 | Tıklanır nokta kartı (u_duvar) içi; yalnız kullanıcı noktaya dokununca görünür (otomatik … | Ürün sayfası → · Teknik föy | `/urunler/duvar-bloklari/?kaynak=hikaye&dil={dil}&urun=duvar&nokta=s1_duvar_kart  |  /teknik-foyler/?kaynak=hikaye&dil={dil}&urun=duvar&nokta=s1_duvar_foy` |
| 44–46 | Tıklanır nokta kartı (u_lento) içi; yalnız kullanıcı noktaya dokununca görünür (otomatik … | Ürün sayfası → · Teknik föy | `/urunler/lentolar/?kaynak=hikaye&dil={dil}&urun=lento&nokta=s1_lento_kart  |  /teknik-foyler/?kaynak=hikaye&dil={dil}&urun=lento&nokta=s1_lento_foy` |
| 49–51 | Tıklanır nokta kartı (u_ublok) içi; yalnız kullanıcı noktaya dokununca görünür (otomatik … | Ürün sayfası → · Teknik föy | `/urunler/u-blok-kose/?kaynak=hikaye&dil={dil}&urun=ublok&nokta=s1_ublok_kart  |  /teknik-foyler/?kaynak=hikaye&dil={dil}&urun=ublok&nokta=s1_ublok_foy` |
| 54–56 | Tıklanır nokta kartı (u_tutkal) içi; yalnız kullanıcı noktaya dokununca görünür (otomatik … | Ürün sayfası → · Teknik föy | `/urunler/tutkal/?kaynak=hikaye&dil={dil}&urun=tutkal&nokta=s1_tutkal_kart  |  /teknik-foyler/?kaynak=hikaye&dil={dil}&urun=tutkal&nokta=s1_tutkal_foy` |
| 59–61 | Tıklanır nokta kartı (u_panel) içi; yalnız kullanıcı noktaya dokununca görünür (otomatik … | Ürün sayfası → · Teknik föy | `/urunler/paneller/?kaynak=hikaye&dil={dil}&urun=panel&nokta=s1_panel_kart  |  /teknik-foyler/?kaynak=hikaye&dil={dil}&urun=panel&nokta=s1_panel_foy` |
| 64–67 | Tıklanır nokta kartı (u_egepor) içi; yalnız kullanıcı noktaya dokununca görünür (otomatik … | Ürün sayfası → · Teknik föy | `/urunler/egepor/?kaynak=hikaye&dil={dil}&urun=egepor&nokta=s1_egepor_kart  |  /teknik-foyler/?kaynak=hikaye&dil={dil}&urun=egepor&nokta=s1_egepor_foy` |
| 64–67 | Anlatım sütununun alt kenarı; "Duvardan çatıya tek mineral malzeme." cümlesinin hemen … | {Ürün} için teklif alın  ·  Ürün Kataloğu (PDF) | `/teklif/?kaynak=hikaye&dil={dil}&urun={urun}&nokta=s1_sistem_teklif  |  /katalog/ (PDF doğrudan ise parametre eklenmez)` |
| 96–98 | λ rakam kartı ve A1 rakam kartı açıldığında kart içinde (yalnız kullanıcı dokununca). | Teknik föyler · CE belgeleri | `/teknik-foyler/?kaynak=hikaye&dil={dil}&urun=duvar&nokta=s3_lambda_kart  |  /teknik-foyler/?kaynak=hikaye&dil={dil}&belge=ce&nokta=s3_a1_kart` |
| 99–101 | Üç rakam mührünün (λ 0,08 · A1 · 300–600) altında tek satır. | Teknik Özellikler → | `/teknik-foyler/?kaynak=hikaye&dil={dil}&urun={urun|duvar}&nokta=s3_muhur` |
| 115–118 | Anlatım sütunu, "200 t" ve "1.100.000 m³" sayaçlarının hemen altında. | Toplu alım ve bayilik → | `/teklif/?kaynak=hikaye&dil={dil}&kitle=bayi&nokta=s4_olcek` |
| 131–134 | Küre sahnesinde alt orta, "25+ ülke · 5 kıta" rakam kartlarının altı; küre ve yaylar … | İhracat bölümüne ulaşın → | `/ihracat/?kaynak=hikaye&dil={dil}&kitle=bayi&nokta=s5_ihracat` |
| 142–146 | Finale: logo ve slogan kilitlendikten sonra (t=141), "Projeniz için teklif alın." başlığı … | Teklif Al → | `/teklif/?kaynak=hikaye&dil={dil}&urun={urun}&nokta=son_teklif` |
| 142–146 | Finale, ana düğmenin yanında; finalin TEK ikincil düğmesi (telefonda altında, tam … | Ürün Kataloğu · PDF | `/katalog/  (sunucuda doğrudan PDF ise parametresiz; sayfaysa ?kaynak=hikaye&dil={dil}&nokta=son_katalog)` |
| 143–146 | Finale, düğmelerin altı, t=143'te tek sırada: "Size en uygun yol:" çipleri (hero ile aynı … | Ev / bina yapıyorum | `/duvar-tasarla/?kaynak=hikaye&dil={dil}&kitle=sahip&nokta=son_kitle` |
| 143–146 | Finale, aynı çip satırı. | Mimar / mühendisim | `/teknik-foyler/?kaynak=hikaye&dil={dil}&kitle=mimar&nokta=son_kitle` |
| 143–146 | Finale, aynı çip satırı. | İhracat alıcısı / bayiyim | `/ihracat/?kaynak=hikaye&dil={dil}&kitle=bayi&nokta=son_kitle` |
| 145–146 | Finale, CTA grubunun altında, perde bandının hemen üstünde ince metin bağlantı (dikkat … | Hikâyeyi baştan izle | `iç bağlantı: window.scrollTo(akış başı); parametre yok` |
| 145–146 | Yalnız sticky bırakıldıktan sonra (finale ekranında değil): perde altı "Ürün grupları" … | Duvar blokları · Lentolar · U blok ve köşe bloğu · Paneller · Gazbeton tutkalı · EGEPOR | `/urunler/{slug}/?kaynak=hikaye&dil={dil}&nokta=sonra_{urun}  (6 kart)` |
| 2–146 | Yolculuk çubuğu (sağ üst, açılır liste): son öğe "Teklif". | Teklif | `iç bağlantı: sahneyeGit('son') → akış p=0,62 (t≈142)` |

**Bağlantı şeması.** ŞABLON
  {yol}?kaynak=hikaye&dil={tr|en}[&urun={kod}][&kitle={sahip|mimar|bayi}][&nokta={cta_id}]

PARAMETRELER (hepsi isteğe bağlı olan köşeli; küçük harf ASCII; kişisel veri YOK)
  kaynak  sabit "hikaye" (hikâye bloğundan çıkan her bağlantı: hero, perdeler, finale). Üst çubuk "Teklif Al" düğmesi hikâye ekranda iken kaynak=hikaye, hikâye dışındaki sayfa bölümlerinde kaynak=ust.
  dil     dilUygula() durumu: tr | en (dil.js dil()).
  urun    duvar | lento | ublok | tutkal | panel | egepor  (finale ajanındaki kodlarla aynı). Yalnız ÖLÇÜLMÜŞ ilgiden gelir; hikâye atlandıysa ya da ilgi yoksa HİÇ eklenmez.
  kitle   sahip | mimar | bayi  YALNIZ tıklanan öğe kitleyi adıyla söylüyorsa (hero/finale çipleri, "Toplu alım ve bayilik", "İhracat bölümüne ulaşın"). Genel "Teklif Al" kitle taşımaz.
  nokta   CTA kimliği (cta_zaman_cizelgesi.id; ≤24 karakter; [a-z0-9_]). Teklif formu bunu gizli alana yazar → "hangi saniyede/hangi cümleden geldi" bilinir. Film saniyesi (t) URL'ye yazılmaz: nokta zaten sahneyi belirler.
  utm_*   sayfaya utm_* ile gelinmişse AYNEN iletilir (kampanya ilişkisi kopmasın). gclid/fbclid iletilmez (site etiketi kendisi okur).

URUN → SAYFA EŞLEMESİ (index.html'deki ürün grubu bağlantılarıyla aynı)
  duvar  /urunler/duvar-bloklari/   lento /urunler/lentolar/   ublok /urunler/u-blok-kose/
  tutkal /urunler/tutkal/            panel /urunler/paneller/   egepor /urunler/egepor/
  Föy: /teknik-foyler/?urun={kod}

BAĞLAM ÇIKARIMI (src/hikaye/baglam.js; yalnız bellek, depolama/çerez YOK)
  skor(urun) = duraktaki görünür süre (sn, durak başına en çok 20) + 8 × açılan nokta kartı + 15 × ürün çipi veya ürün bağlantısı tıklaması.
  En yüksek skor kazanır; eşitlikte en son bakılan. Eşik: skor ≥ 5 (1 sn gezinme urun ayarlamaz). ege_baglam olayı t≥64'te ya da finalde bir kez atılır; urun değişirse yeniden hesaplanır.
  Hikâye atlandıysa urun yok; finale bağlam çipi gizli, düğmeler jenerik.

HREF DÜZENİ
  Statik HTML'de href'ler TEMİZ kalır (/teklif/, /katalog/ ...): arama motoru ve JS'siz görünüm parametre görmez, kanonik sorunu çıkmaz.
  JS (baglam.js) bağlam değiştiğinde ilgili href'leri ve data-iz'i günceller (tıklama anına bırakılmaz: sağ tık/uzun basış/bağlantıyı kopyala da doğru çalışsın).
  /katalog/ doğrudan PDF dosyasıysa parametre eklenmez (önbellek ve dosya adı bozulmasın); izleme data-iz + GA4 file_download ile yapılır. /katalog/ sayfaysa kaynak/dil/nokta eklenir.
  İç bağlantılar (sahneyeGit, #teklif, tekrar izle) parametresizdir.

OKUMA TARAFI (site işi; açık soru 4): /teklif/ formu parametreleri beyaz listeyle okur (bilinmeyen değer yok sayılır, HTML olarak basılmaz), şunları yapar: urun ön seçimi + "Hikâyede baktığınız: EGEPOR ×" çipi (× ile silinir), kitle'ye göre alan seti/başlık, gizli alanlar kaynak ve nokta (CRM/teklif e-postasında görünür).

ÖRNEKLER
  Finale ana düğme      /teklif/?kaynak=hikaye&dil=tr&urun=egepor&nokta=son_teklif
  Mimar çipi (EN)       /teknik-foyler/?kaynak=hikaye&dil=en&kitle=mimar&nokta=giris_kitle
  İhracat CTA           /ihracat/?kaynak=hikaye&dil=en&kitle=bayi&nokta=s5_ihracat
  Lento kartı           /urunler/lentolar/?kaynak=hikaye&dil=tr&urun=lento&nokta=s1_lento_kart
  Lento föyü            /teknik-foyler/?kaynak=hikaye&dil=tr&urun=lento&nokta=s1_lento_foy
  Üst çubuk (hikâye dışı) /teklif/?kaynak=ust&dil=tr&nokta=ust
  Hikâye atlandı        /teklif/?kaynak=hikaye&dil=tr&nokta=son_teklif   (urun yok)


### Güven işaretleri
-
  - **id**: g_fabrika
  - **isaret**: 2 fabrika · Söke & İzmir
  - **kaynak**: Ege Gazbeton ortak rakamlar (dil.js h4.k1; DEVIR.md)
  - **durum**: doğrulandı
  - **nerede_gorunur**: t=20 (tır kartı), 108, 144 kanıt kartı
-
  - **id**: g_kapasite
  - **isaret**: 1.100.000 m³ üretim kapasitesi
  - **kaynak**: Ege Gazbeton ortak rakamlar (index.html h4.k2)
  - **durum**: doğrulandı
  - **nerede_gorunur**: t=115
  - **not**: Süre ibaresi (yıllık?) kaynakta yok: ekranda yalnız "üretim kapasitesi".
-
  - **id**: g_kireç
  - **isaret**: Söke'de günde 200 ton kapasiteli kendi kireç tesisi
  - **kaynak**: Ege Gazbeton ortak rakamlar (dil.js NOKTALAR.kirec, h4.k3)
  - **durum**: doğrulandı
  - **nerede_gorunur**: t=74 (kart), 114
  - **not**: Sahiplik vurgusu: "kendi" sözcüğü kalır.
-
  - **id**: g_lambda
  - **isaret**: λ 0,08 W/mK · G2/350 duvar tasarım değeri
  - **kaynak**: Ege Gazbeton ortak rakamlar (index.html s3)
  - **durum**: doğrulandı
  - **nerede_gorunur**: t=96
-
  - **id**: g_a1
  - **isaret**: A1 · yangına tepki sınıfı · EN 13501-1
  - **kaynak**: CE belgeleri (index.html s3)
  - **durum**: doğrulandı
  - **nerede_gorunur**: t=97, 144 kanıt kartı
  - **not**: Hiçbir yerde "yanmaz". Üretici ürün sayfası "A1 Hiç Yanmaz" yazıyor (DEVIR.md): bağlantılı sayfalarla tutarlılık teyit gerekli.
-
  - **id**: g_yogunluk
  - **isaret**: 300–600 kg/m³ (G1–G4)
  - **kaynak**: Ürün sınıfları G1/300 – G4/600 (index.html s3)
  - **durum**: doğrulandı
  - **nerede_gorunur**: t=99
-
  - **id**: g_blok
  - **isaret**: 60 × 25 cm yüz · 1–3 mm ince derz · 5–35 cm kalınlık · lento 4,50 m'ye kadar · panel 6 m açıklık
  - **kaynak**: Ürün föyleri (index.html, dil.js)
  - **durum**: doğrulandı
  - **nerede_gorunur**: t=13–16, 36–60
-
  - **id**: g_ublok
  - **isaret**: U blok G4/06: 60 × 25 cm, 20–25 cm, λ 0,16 W/mK kuru; "hatılda ahşap kalıp yerine"
  - **kaynak**: Ürün föyleri · U Bloklar sayfası (DEVIR.md: egegazbeton.com.tr/urunlerimiz/u-bloklar/)
  - **durum**: doğrulandı
  - **nerede_gorunur**: t=49–50
  - **not**: 50 kgf/cm² ve 600 kg/m³ ekranda yok; gerekirse kartta kaynakla.
-
  - **id**: g_egepor
  - **isaret**: EGEPOR λ 0,051–0,062 W/mK kuru · 150–200 kg/m³; kolon ve kiriş kaplaması
  - **kaynak**: Ürün föyleri · EGEPOR sayfası (DEVIR.md: egegazbeton.com.tr/urunlerimiz/egepor/)
  - **durum**: doğrulandı
  - **nerede_gorunur**: t=64–65
-
  - **id**: g_odtu
  - **isaret**: ODTÜ çalışması: 8 katlı örnek bina hesabı, yapı kütlesi −%17
  - **kaynak**: ODTÜ çalışması (index.html h1e.k2; dil.js i3.kaynak)
  - **durum**: doğrulandı
  - **nerede_gorunur**: t=59–60
  - **not**: Etiket "ODTÜ çalışması, 8 katlı örnek bina hesabı" olarak kalır; onay/sertifika dili ve genelleme yok. Kapsam (yalnız panel mi, tüm sistem mi) ve çalışmanın bağlantısı teyit gerekli.
-
  - **id**: g_ihracat
  - **isaret**: 25+ ülke · 5 kıta
  - **kaynak**: Ege Gazbeton ihracat bölümü (DEVIR.md, dil.js)
  - **durum**: doğrulandı
  - **nerede_gorunur**: t=130–131, 144 kanıt kartı
  - **not**: Ülke adı, ülke sınırı, müşteri sayısı, fiyat yok.
-
  - **id**: g_surec
  - **isaret**: Şeffaf üretim: kum, kireç, çimento, alçı, alüminyum tozu; kabarma, tel kesim, otoklav
  - **kaynak**: Müşteri onaylı i1 metinleri ve NOKTALAR (dil.js)
  - **durum**: doğrulandı
  - **nerede_gorunur**: t=72–87
  - **not**: Güven işareti olarak "açık üretim": rakam yok (otoklav °C/bar ve hava hacim oranı teyit gerekli).
-
  - **id**: g_kunye
  - **isaret**: Kurumsal künye: © Ege Gazbeton — Akkuş Mimarlık İnşaat Turizm San. ve Tic. A.Ş.
  - **kaynak**: index.html alt bilgi (müşteri sayfası)
  - **durum**: doğrulandı
  - **nerede_gorunur**: alt bilgi; JSON-LD legalName
  - **not**: DEVIR.md'de değil; sayfada mevcut olduğu için kullanılabilir, yine de kuruluşa teyit.
-
  - **id**: g_ce_no
  - **isaret**: CE belge numaraları (CE 2179-CPR-0043 / 0052) ve TS EN 771-4
  - **kaynak**: Yalnız README.md/OKU-BENI.txt'te; DEVIR.md ve dil.js'te YOK
  - **durum**: teyit gerekli
  - **nerede_gorunur**: ekranda GÖSTERİLMEZ
  - **not**: Belge dosyası/PDF ile doğrulanana kadar yalnız "CE belgeleri" kaynak adı kullanılır.
-
  - **id**: g_taban_kesme
  - **isaret**: Taban kesme kuvveti −%14 (ODTÜ)
  - **kaynak**: OKU-BENI.txt; dil.js'te yalnız i3.k2 anahtarı, rakamsız
  - **durum**: teyit gerekli
  - **nerede_gorunur**: kullanılmaz
-
  - **id**: g_iso
  - **isaret**: ISO 9001 / TSE / EPD / yeşil bina katkısı
  - **kaynak**: kayıtta yok
  - **durum**: teyit gerekli
  - **nerede_gorunur**: kullanılmaz
-
  - **id**: g_yangin_direnci
  - **isaret**: Yangın direnci (EN 13501-2) belgesi
  - **kaynak**: kayıtta yok (s3 ajanı da işaretledi)
  - **durum**: teyit gerekli
  - **nerede_gorunur**: serin yüz/süre/°C ima edilmez
-
  - **id**: g_kurulus
  - **isaret**: Kuruluş yılı, tecrübe yılı, referans proje sayısı
  - **kaynak**: kayıtta yok; müşteri sayısı zaten yasak
  - **durum**: teyit gerekli
  - **nerede_gorunur**: kullanılmaz
-
  - **id**: g_teslimat
  - **isaret**: Teslim süresi, stok, garanti, "X saatte dönüş" vaadi
  - **kaynak**: kayıtta yok
  - **durum**: teyit gerekli
  - **nerede_gorunur**: kullanılmaz
  - **not**: Teklif sayfasında vaat verilecekse müşteri tarafından yazılı onay gerekir.
-
  - **id**: g_liman
  - **isaret**: Aliağa ve Alsancak limanlarına yakınlık
  - **kaynak**: dil.js'te var (i4.metin, NOKTALAR.kaynak) ama kaynaksız; s5 ajanı da işaretledi
  - **durum**: teyit gerekli
  - **nerede_gorunur**: pazarlama kopyasına ALINMAZ
-
  - **id**: g_palet
  - **isaret**: Palet/tır kapasitesi, sevkiyat süresi
  - **kaynak**: kayıtta yok
  - **durum**: teyit gerekli
  - **nerede_gorunur**: kullanılmaz
-
  - **id**: g_sunum_kurallari
  - **isaret**: SUNUM KURALLARI (hepsi için)
  - **kaynak**: DEĞİŞMEZ KURALLAR
  - **durum**: kural
  - **nerede_gorunur**: tüm film
  - **kurallar**:
    - Her sayının kaynağı kartta yazılı; telefonda da (hikaye.css ≤760 px'te .eg-rakam small{display:none} yapıyor: bu kural ile ÇELİŞİR → tek satır dipnot).
    - Üst düzey iddia sözcükleri yok: "en iyi", "lider", "garantili", "yanmaz", "depreme dayanıklı", "%… tasarruf".
    - Kanıt şeridi (t=144; statik bilgi kartları) üç kart: "2 fabrika · Söke & İzmir" | "CE belgeleri · A1 EN 13501-1" | "25+ ülke · 5 kıta" — her birinin altında kaynak adı.
    - Güven = iddia değil kaynaklı rakam + açık üretim (s2) + üçüncü taraf (ODTÜ) + belge (CE).
    - Yeni bir güven işareti ancak doğrulanınca bu tabloya "doğrulandı" olarak eklenir.

### Ölçüm
-
  - **tur**: kural
  - **ad**: Gizlilik ve çerez
  - **kurallar**:
    - Hikâye kodu YENİ çerez, localStorage, sessionStorage, parmak izi, harici istek eklemez. Mevcut tek depolama: tercih edilen dil (localStorage "ege-dil", işlevsel).
    - Olaylar yalnız window.dataLayer bir dizi ise push edilir (mevcut arayuz.js davranışı); yoksa hiçbir şey olmaz. Ağ çağrısı/sendBeacon YOK.
    - Olayları GA4/GTM'ye iletip iletmeyeceğine sitenin onay (consent) yapısı karar verir; hikâye bundan bağımsız. Onay aracı ve GTM kurulumu teyit gerekli (açık soru 9).
    - Parametreler sayı veya sabit sözlükten kod; serbest metin, URL sorgusu, IP, kimlik YOK.
    - Bağlam (urun) yalnız bellekte; sayfa yenilenince sıfırlanır.
-
  - **tur**: kural
  - **ad**: Film saniyesi ve hız sınıfı
  - **kurallar**:
    - t_film = akış içinde kaydırılan vh / 22 (referans hız 22 vh/sn; dagit() içindeki yVh). 1 ondalık yuvarlanır, olaylarda tam sayı.
    - hiz sınıfı (son 3 sn ortalama kaydırma): yavas < 0,5×, normal 0,5–2×, hizli > 2× (1× = 22 vh/sn). Hızlı kaydıranın "izledi" sayılmaması için ege_ilerleme olayında taşınır.
    - Eşik olayları oturumda bir kez ve yalnız ilk ulaşılışta (ileri yön); geri kaydırma yeniden saymaz.
    - Kare başı iş yok: olaylar frame() içinde kuyruğa alınır, requestIdleCallback ile boşaltılır; oturumda en çok ~80 olay.
-
  - **tur**: olay
  - **olay**: ege_hikaye_gor
  - **ne_zaman**: Poster (kareler/s0/poster.webp) çözüldü ve ilk boyama olduktan sonra, bir kez
  - **t_film**: 0
  - **sahne**: s0
  - **parametreler**:
    - dil
    - varyant d|m
    - hareket normal|az
    - tasarruf 0|1
    - ekran kova (<480, 480–760, 761–1280, >1280)
  - **amac**: ziyaretçi hacmi, LCP ile birlikte okunur; huninin tabanı
-
  - **tur**: olay
  - **olay**: ege_hikaye_basla
  - **ne_zaman**: İlk kaydırma (>0), ilk dokunuş/tık veya klavye ile ilk eylem
  - **t_film**: 0–2
  - **sahne**: s0
  - **parametreler**:
    - bekleme_ms (250 ms kovalı)
    - eylem kaydir|dokun|klavye|tik
  - **amac**: 10 sn testinin canlı karşılığı: ziyaretçi ne kadar sürede harekete geçti?
-
  - **tur**: olay
  - **olay**: ege_ilerleme
  - **ne_zaman**: Film saniyesi eşiklerinde (ilk ulaşılışta)
  - **t_film**: 5, 10, 20, 28, 32, 45, 60, 70, 90, 104, 120, 130, 136, 140, 142, 146
  - **sahne**: her sahne
  - **parametreler**:
    - t
    - sahne
    - gecen_sn (hikaye_basla'dan, kovalı)
    - hiz
    - dil
  - **amac**: huni raporu; kritik eşikler 10 (duygu tutma), 32 (kanıt başlar), 104 (güç başlar), 136 (eylem başlar), 142 (CTA görünür)
-
  - **tur**: olay
  - **olay**: ege_sahne
  - **ne_zaman**: Sahne görünür olduğunda (giriş) ve çıktığında (süre)
  - **t_film**: 32, 70, 90, 104, 120, 136 (girişler)
  - **sahne**: s0–son
  - **parametreler**:
    - sahne
    - sure_sn (görünür süre)
    - yon ileri|geri
  - **amac**: hangi perdede ne kadar duruldu; geri dönüşler (zorlandığı/ilgilendiği yer)
-
  - **tur**: olay
  - **olay**: ege_durak
  - **ne_zaman**: Ürün durağı bırakıldığında
  - **t_film**: 40, 45, 50, 55, 60, 65 (çıkışlar)
  - **sahne**: s1
  - **parametreler**:
    - urun duvar|lento|ublok|tutkal|panel|egepor
    - sure_sn
    - nokta_acti 0|1
    - cip_ile 0|1
  - **amac**: ürün ilgisi: hangi ürünün durağında kaç sn kalındı; ege_baglam'ın girdisi
-
  - **tur**: olay
  - **olay**: ege_nokta
  - **ne_zaman**: Tıklanır nokta kartı açıldığında (arayuz.js kartAc)
  - **t_film**: her
  - **sahne**: her
  - **parametreler**:
    - nokta (NOKTALAR kimliği: tir, fabrika, u_egepor, kirec, hucre, kitalar ...)
    - sahne
    - t
    - kaynak dokun|klavye
  - **amac**: hangi kanıt/kart ilgi çekiyor: ODTÜ (u_panel, t=60), CE/A1 (t=97), kireç tesisi (t=74, 114), tır (t=20–22, 110), kitalar (t=130)
-
  - **tur**: olay
  - **olay**: ege_cta_gor
  - **ne_zaman**: Bir CTA penceresi ilk kez görünür olduğunda (p aralığına girince; IntersectionObserver gerekmez)
  - **t_film**: 0, 23, 38, 64, 99, 115, 131, 142, 143
  - **sahne**: ilgili perde
  - **parametreler**:
    - cta (cta_zaman_cizelgesi.id)
    - t
    - tur
  - **amac**: pencere başına tıklanma oranı = ege_tik / ege_cta_gor
-
  - **tur**: olay
  - **olay**: ege_tik
  - **ne_zaman**: [data-iz] tıklaması (MEVCUT olay, arayuz.js; geriye dönük uyumlu genişletme)
  - **t_film**: her
  - **sahne**: her
  - **parametreler**:
    - hedef (data-iz)
    - dil
    - + t
    - + sahne
    - + urun (varsa)
    - + kitle (varsa)
    - + hiz
  - **amac**: tüm CTA tıklamaları; mevcut ust_teklif, giris_teklif, giris_katalog, giris_foyler, kitle_*, hikaye_atla, son_teklif, son_katalog adları korunur (son_foyler: finaldeki ayrı düğme kaldırıldı, mimar çipi son_kitle_mimar); yeni adlar cta tablosundaki olcum_data_iz
-
  - **tur**: olay
  - **olay**: ege_kitle
  - **ne_zaman**: Hero/finale kitle çipi tıklandığında
  - **t_film**: 0–2 ve 143–146
  - **sahne**: s0/son
  - **parametreler**:
    - kitle sahip|mimar|bayi
    - yer giris|son
    - t
  - **amac**: kitle dağılımı; hero ile finale çipi tercihi farkı
-
  - **tur**: olay
  - **olay**: ege_atla
  - **ne_zaman**: "Hikâyeyi atla" / yolculuk çubuğunda "Teklif"
  - **t_film**: 0–146
  - **sahne**: her
  - **parametreler**:
    - nokta giris|yol
    - t_atlanan (atlanılan en yüksek ulaşılmış t)
    - gecen_sn
  - **amac**: atlayanların dönüşümü ile izleyenlerin dönüşümü kıyası (hikâyenin değeri)
-
  - **tur**: olay
  - **olay**: ege_dil
  - **ne_zaman**: TR/EN düğmesi
  - **t_film**: her
  - **sahne**: her
  - **parametreler**:
    - dil
    - t
  - **amac**: ihracat ilgisi göstergesi
-
  - **tur**: olay
  - **olay**: ege_baglam
  - **ne_zaman**: urun çözüldüğünde ve değiştiğinde (ilk kez t≥64 ya da finalde)
  - **t_film**: 64–146
  - **sahne**: s1/son
  - **parametreler**:
    - urun
    - kaynak sure|nokta|tik
  - **amac**: bağlam doğruluğu kontrolü; teklif formundaki urun ile karşılaştırılır
-
  - **tur**: olay
  - **olay**: ege_son_gor
  - **ne_zaman**: Finale CTA grubu görünür (akış p ≥ 0,60)
  - **t_film**: 142
  - **sahne**: son
  - **parametreler**:
    - urun (varsa)
    - gecen_sn
    - atladi 0|1
  - **amac**: EYLEM aşamasının tabanı: kaç kişi düğmeyi gördü?
-
  - **tur**: olay
  - **olay**: ege_tekrar
  - **ne_zaman**: "Hikâyeyi baştan izle"
  - **t_film**: 145–146
  - **sahne**: son
  - **parametreler**:
    - gecen_sn
  - **amac**: paylaşılabilirlik/değer sinyali
-
  - **tur**: olay
  - **olay**: ege_kare_hiz
  - **ne_zaman**: Sahneden çıkışta, oturum başına en çok 4 örnek (s0, s1, s4, s5)
  - **t_film**: 32, 70, 120, 136
  - **sahne**: s0, s1, s4, s5
  - **parametreler**:
    - sahne
    - fps_p50
    - fps_p5
    - yavas_oran (>25 ms kare oranı, %)
    - varyant
    - dpr (≤1,25)
  - **amac**: ≥50 fps kuralının sahadaki doğrulaması; yalnız kaydırma sırasındaki karelerden (rAF boştayken ölçülmez)
-
  - **tur**: olay
  - **olay**: ege_kare_hata
  - **ne_zaman**: Kare indirme hatası (kuyruk)
  - **t_film**: her
  - **sahne**: her
  - **parametreler**:
    - sahne
    - kare_kova (10'lu)
  - **amac**: bozuk/eksik kare ve CDN sorunu; çevrimdışı file:// sınamasında da çalışır
-
  - **tur**: olay
  - **olay**: ege_cikis
  - **ne_zaman**: visibilitychange→hidden / pagehide (dataLayer'a push; iletim garanti değil)
  - **t_film**: her
  - **sahne**: her
  - **parametreler**:
    - t_maks (ulaşılan en yüksek)
    - sahne
    - sure_sn (kovalı)
    - cta_gordu 0|1
  - **amac**: terk noktası haritası (hangi saniyede çıkıldı)
-
  - **tur**: zaman_cizelgesi
  - **ad**: Hangi film saniyesinde / sahnede ne ölçülür
  - **noktalar**:
    -
      - **t**: 0
      - **sahne**: s0
      - **olay**: ege_hikaye_gor + ege_cta_gor(giris_teklif, ust_teklif)
    -
      - **t**: 0–2
      - **sahne**: s0
      - **olay**: ege_hikaye_basla (bekleme_ms); ege_tik giris_* / kitle_* / hikaye_atla
    -
      - **t**: 5
      - **sahne**: s0
      - **olay**: ege_ilerleme (plan çizimi başladı)
    -
      - **t**: 10
      - **sahne**: s0
      - **olay**: ege_ilerleme — DUYGU TUTMA eşiği: eskiz tamam
    -
      - **t**: 20–22
      - **sahne**: s0
      - **olay**: ege_ilerleme t=20; ege_nokta tir/palet
    -
      - **t**: 23
      - **sahne**: s0
      - **olay**: ege_cta_gor s0_tir_urunler
    -
      - **t**: 28
      - **sahne**: s0
      - **olay**: ege_ilerleme (soru anı); ege_nokta yuva
    -
      - **t**: 32
      - **sahne**: s1
      - **olay**: ege_sahne s1, ege_ilerleme — KANIT başlar
    -
      - **t**: 36–65
      - **sahne**: s1
      - **olay**: ege_durak (6 çıkış: t=40,45,50,55,60,65), ege_nokta u_*; t=38 ege_cta_gor s1_duvar_hesapla; t=60 ODTÜ kartı
    -
      - **t**: 64
      - **sahne**: s1
      - **olay**: ege_baglam + ege_cta_gor s1_sistem_teklif (ilk ANA CTA)
    -
      - **t**: 70
      - **sahne**: s2
      - **olay**: ege_sahne s2; t=72–77 hammadde kartları, 80 kabarma, 83 kesim, 85 otoklav (ege_nokta)
    -
      - **t**: 90
      - **sahne**: s3
      - **olay**: ege_sahne s3; t=91 hucre; t=96 λ kartı; t=97 A1/CE kartı; t=99 ege_cta_gor s3_muhur_foy
    -
      - **t**: 104
      - **sahne**: s4
      - **olay**: ege_ilerleme + ege_sahne s4 — GÜÇ başlar; ege_kare_hiz (s3 çıkışı)
    -
      - **t**: 106–113
      - **sahne**: s4
      - **olay**: ege_nokta palet / fabrika / tir (t=110 kahraman kare)
    -
      - **t**: 114–115
      - **sahne**: s4
      - **olay**: ege_nokta kirec/otoklav; ege_cta_gor s4_olcek_bayi
    -
      - **t**: 120
      - **sahne**: s5
      - **olay**: ege_sahne s5; ege_kare_hiz (s4 çıkışı)
    -
      - **t**: 130–131
      - **sahne**: s5
      - **olay**: ege_ilerleme t=130; ege_nokta kitalar; ege_cta_gor s5_ihracat
    -
      - **t**: 136
      - **sahne**: son
      - **olay**: ege_sahne son — EYLEM başlar
    -
      - **t**: 140
      - **sahne**: son
      - **olay**: ege_ilerleme (logo + slogan göründü)
    -
      - **t**: 142
      - **sahne**: son
      - **olay**: ege_son_gor + ege_cta_gor son_teklif/son_katalog
    -
      - **t**: 143
      - **sahne**: son
      - **olay**: ege_cta_gor son_kitle_* (tek sıra kitle çipleri)
    -
      - **t**: 144–146
      - **sahne**: son
      - **olay**: kanıt kartları t=144 (statik, olay yok); ege_tekrar (t=145: ince bağlantı); ege_cta_gor sonra_urun_kartlari (bırakma sonrası); ege_ilerleme t=146
    -
      - **t**: sürekli
      - **sahne**: —
      - **olay**: ege_kare_hiz, ege_kare_hata, ege_cikis, ege_dil
-
  - **tur**: rapor
  - **ad**: Huni raporu (GA4/GTM keşif: olay → yüzde)
  - **tanimlar**:
    - Duygu tutma = ege_ilerleme(t=10) / ege_hikaye_gor
    - Kanıta geçiş = ege_ilerleme(t=32) / ege_ilerleme(t=10)
    - Kanıtı bitirme = ege_ilerleme(t=104) / ege_ilerleme(t=32)
    - Güce ulaşma = ege_ilerleme(t=136) / ege_ilerleme(t=104)
    - Eylem görme = ege_son_gor / ege_ilerleme(t=136)  (atlayanlar ayrı kesit: atladi=1)
    - Eylem = ege_tik(hedef ∈ son_teklif, son_katalog, son_kitle_*) / ege_son_gor  (son_foyler kaldırıldı; son_bar_* alt çubuk ertelendi: numara teyidi gelene dek yok)
    - Gerçek dönüşüm (site): /teklif/ formu gönderimi, kaynak=hikaye; nokta kırılımı = hangi CTA (site tarafı GA4 generate_lead + gizli alanlar)
    - Atlayan vs izleyen dönüşüm farkı = hikâyenin net katkısı
-
  - **tur**: rapor
  - **ad**: İçgörü soruları
  - **tanimlar**:
    - Hangi ürün durağında en çok kalınıyor / hangi ürün teklifle sonuçlanıyor? (ege_durak.sure_sn × urun × teklifte urun)
    - ODTÜ (u_panel) ve CE/A1 (hucre/A1) kartını açan, teklife daha mı çok gidiyor?
    - Tır noktasına/etiketine dokunan oranı = marka ilgisi (ege_nokta nokta=tir)
    - Terk haritası: ege_cikis.t_maks dağılımı; ≥3 saniyelik tepe = sorunlu an
    - Telefon/masaüstü kırılımı; dil=en oranı; hız sınıfı (hizli ziyaretçi teklif veriyor mu)
    - Hangi CTA penceresi en çok tıklanıyor, hangisi hiç (ege_tik/ege_cta_gor)? Tıklanmayan pencere kaldırılır.
-
  - **tur**: rapor
  - **ad**: Hedefler
  - **tanimlar**:
    - Sayısal hedef YOK (kaynaksız rakam konmaz). İlk 4 hafta taban çizgisi ölçülür; hedef sonra belirlenir.
    - Teknik hedef (kuraldan): ege_kare_hiz.fps_p50 ≥ 50; hareket azaltma/veri tasarrufu kullanıcılarında CTA'lar hemen görünür.
    - İsteğe bağlı kontrol grubu: hikâyesiz (durağan sütun, ?az benzeri) sürüm trafiğin küçük bir bölümüne; atamanın çerezsiz yapılabilmesi KVKK açısından teyit gerekli.
-
  - **tur**: uygulama
  - **ad**: Kod yerleri
  - **tanimlar**:
    - src/hikaye/arayuz.js: "Analitik" bloğundaki ege_tik push'u izle.js'e taşınır (iz(olay, veri): Array.isArray(window.dataLayer) kontrolü, ortak alanlar dil/t/sahne/urun/kitle/hiz).
    - src/hikaye/main.js frame(): yVh zaten hesaplanıyor → tFilm = yVh/22; eşik ve hız sınıfı burada; push kuyruğa.
    - src/hikaye/baglam.js (yeni, finale ajanıyla ortak): skor, href güncelleme, ege_baglam.
    - index.html: yeni data-iz adları (cta tablosu olcum_data_iz); CTA pencereleri .eg-vurus gibi data-bas/data-son (sahne p aralığı: cta tablosu p_bas/p_son).
    - tools/sinama.mjs: kaydırma kontrol noktalarında (t=0,10,32,64,104,142) beklenen olay dizisini ve konsol hatası olmadığını doğrular; ?debug HUD son 5 olayı gösterir.
    - GTM/GA4: olay adları tek sözlükte (bu dosya); sitedeki mevcut dataLayer adı "dataLayer" varsayıldı (teyit gerekli).

### Marka görünürlüğü
-
  - **konu**: LİME KURALI (özet)
  - **kural**: Lime = BİZİM: yalnız Ege Gazbeton ürünü, ambalajı, şeridi ve tıklanır "bizim" noktaları. UI'da lime yalnız: ana düğme (lime dolgu, koyu #0c161c yazı = kontrast 8,76:1; beyaz yazı 2,09:1 ile YETERSİZ), Ege ögelerinin tıklanır halkası, ilerleme dolgusu, logo köşe işaretleri.
  - **uygula**: 3B: palet streç filmi, tır kabin şeridi, fabrika/baca bandı, saha halkası, s1 ürün kenar ışıltısı, İzmir/Söke iğneleri, Türkiye poligonu. Lime OLAMAZ: donatı, çelik, kayış (amber), tuğla, bitki (doğal, koyu/mavimsi yeşil), tüm üçüncü taraf araçlar ve nesneler. Nötr bilgi noktaları (bahçe, sokak, giriş) beyaz halka; yalnız Ege ögelerinin noktaları lime halka.
  - **olcut**: Ölçüm (önizlemeden): marka lime #a2bf37 H≈73°; tır önizlemesinde palet filmi H≈76–77°, S≈0,7 ama V≈0,47 (gölgede zeytin yeşiline düşüyor). t=22 hero karesinde film güneşle V≥0,65 okunmalı; yoksa marka tanınırlığı zayıflar. Bitki ve çimen lime'dan ≥25° uzak ton, düşük doygunluk.
-
  - **konu**: TIR = HAREKETLİ REKLAM PANOSU
  - **t**: 19–25, 105–113, 117
  - **kural**: Tır hikâyenin tek "markalı araç"ı. Kullanıcı şikâyeti (ayrıntı az) pazarlama açısından da kritik: marka tırdan okunuyor. Önce 0,5 sn'de okunan şeyler doğru olmalı: ① iki sıra lime streçli palet düzeni (kütle) ② kabin lime şeridi ③ amber kayışlar ④ HTML etiket.
  - **uygula**: Kabin: ızgara, aynalar, spoyler, güneşlik, projektörler, jant somunları, cam yansıması. Dorse: yan koruma, reflektör bantları, çamurluk, ikiz lastik, stop lambaları. Palet: streç kırışığı + güneş çizgileri, kayış, köşe koruyucu, alt taban. Tüm bunlar zaten s0/s4 planlarında; pazarlama önceliği: yan boydan görünüm (t=21–22) ve t=110 kahraman kare karelerinin ayrıntısı diğer karelerden yüksek olsun.
  - **olcut**: Siluet testi: t=22 karesi 320 px genişlikte, gri tonda dahi iki sıra palet + kabin şeridi seçilmeli. Renk testi: lime ekranın en büyük keskin renk lekesi olmalı.
-
  - **konu**: TIR ETİKETİ
  - **t**: 20–22, 110–113
  - **kural**: HTML etiket "Ege Gazbeton" (≤2 sözcük), tırı kare başına çapayla izler (±8 px), koyu zemin + beyaz yazı + lime nokta (lime yalnız nokta). Dokununca kart: "Lime streçli paletler: Söke ve İzmir'den sahaya." Kabinde logo çıkartması YOK: 3B içinde yazı yok kuralı + logo en sonda kuralı. SVG üst katmanla kabine logo basmak teknik olarak mümkün ama "logo en sonda" ile çelişir: açık soru 10.
  - **olcut**: ege_nokta(nokta=tir) sayısı
-
  - **konu**: LİME RİTMİ (marka tekrarı)
  - **kural**: Lime vuruşları: t=17–18 ilk lime (silme çizgisi) · 19–25 tır · 36/41/46/51/56/61 ürün durağı kenar ışıltıları · 101–103 palet · 104–117 saha, palet ızgarası, tır, saha halkası · 120–135 İzmir/Söke iğneleri, Türkiye, damla · 138–141 L köşeleri, logo. ÖNERİ: s2/s3 (t=70–100) lime'sız 30 sn'lik boşluk; bloğa ince lime kenar ışıltısı t=70 ve t=87'de (blok = bizim ürün), s3 mühür şeridinde lime alt çizgi.
  - **olcut**: Hiçbir 25 sn'lik pencerede lime yok olmasın (t=0–17 ve 25–36 hariç: duygu ve soru ayrıcalığı).
-
  - **konu**: İLK LİME ANI = ÖDÜL
  - **t**: 17–18
  - **kural**: t=0–17 lime YOK: ışık amber, kâğıt bej; bu yüzden t=17'deki lime tarama çizgisi ilk marka vuruşu olarak güçlü okunur ve tırdaki lime (t=19) ile bağlanır.
  - **olcut**: ege_ilerleme t=20 / t=10 oranı (marka anına ulaşan)
-
  - **konu**: ARAÇLAR (otomobil, bisiklet, forklift)
  - **kural**: Kırmızı otomobil, mavi araç, bisiklet: nötr, markasız, lime'sız (kırmızı arabanın ön yüzü düzeltmesi kalite işi). Şirket araçları (forklift, saha aracı) lime şeritli; üçüncü taraf hiçbir araçta lime yok.
  - **olcut**: —
-
  - **konu**: LOGO
  - **t**: 140–146
  - **kural**: Logo YALNIZ t=140–141'de doğar (kıvılcım → L köşeleri → EGE / GAZBETON), t=141'de üst çubuğa iner; sonrasında (Ürün grupları, alt bilgi) kalıcı. Hikâye boyunca üst çubuk sol yuvasında logo SVG YOK: yerinde düz metin "Ege Gazbeton" bağlantısı (ana sayfa, erişilebilirlik, yön bulma) — bu bir logo değil. Mevcut index.html yer tutucu logosu hikâyede gizlenir (açık soru 2).
  - **olcut**: —
-
  - **konu**: SLOGAN
  - **t**: 138–141 ve <title>
  - **kural**: "Bugünden Yarına Güvenle" yalnız finalde (t=140) ve <title>/OG'de. ÖNERİ: açılış H1 slogan olmasın ("Her yuva bir çizgiyle başlar."); slogan finalde "Güven." sözcüğünü devralınca ödül olur. s0 ve son ajanlarının planlarından sapma: hero H1 ile t=2 vuruşu tek öğe olur (açık soru 1).
  - **olcut**: —
-
  - **konu**: MARKA ADI İLK EKRANDA
  - **t**: 0
  - **kural**: Eyebrow "EGE GAZBETON · Söke & İzmir" (düz metin, hero paneli) + tarayıcı sekmesi başlığı + üst çubuk metin bağlantısı: logo olmadan marka adı ilk saniyede okunur.
  - **olcut**: 10 sn testi soru 1: "Hangi firma?"
-
  - **konu**: REKLAM / PAYLAŞIM KARELERİ
  - **t**: 22, 110, 28, 131
  - **kural**: Dört "marka karesi" kodla Blender'dan hazır olacak şekilde seçilir: t=22 tır yan görünüm (OG varsayılanı), t=110 yüklü tır kahraman karesi (kayış + streç çipleri çizilmeden temiz sürüm), t=28 akşam pencereleri (duygu), t=131 küre 25+ ülke (ihracat sayfası). Hepsi 3B yazısız; metin gerekiyorsa PIL/HTML ile sonradan.
  - **olcut**: og_uret.py çıktısı; paylaşım tıklaması (UTM değil, site paylaşım kaynağı)
-
  - **konu**: AMBALAJ MESAJI
  - **t**: 106–110
  - **kural**: "Her palet lime streçle sarılır." ambalajı marka yapar: lime streç, kayış, köşe koruyucu. Kopya: ambalaj özenini söyler, kapasite/dayanım rakamı vermez.
  - **olcut**: ege_nokta(nokta=palet)
-
  - **konu**: MARKA SESİ
  - **kural**: "Biz" dili ve sahiplik: "kendi kireç tesisimiz", "iki fabrikamız". Süs sözcük yok. Etiketler ≤2 sözcük.
  - **olcut**: —
-
  - **konu**: EN KOPYADA "LIME" ÇİFT ANLAMI
  - **kural**: dil.js EN: "Pallets in lime stretch film" ve "Lime — the binder": İngilizcede "lime" hem kireç hem renk. İlk geçişte "lime-green stretch film" yazılmalı; kireç için "lime (quicklime)" teyit gerekli.
  - **olcut**: —
-
  - **konu**: SONRASI KARTLARDA MARKA
  - **t**: 145–146
  - **kural**: Yalnız sticky bırakıldıktan sonra (finale ekranında değil): hikâyede en çok bakılan ürün kartı lime kenar + "Hikâyede baktığınız" etiketi: lime yine ürünle birlikte.
  - **olcut**: sonra_urun_* tıklaması

### SEO ve paylaşım
-
  - **konu**: <title> TR
  - **oneri**: Ege Gazbeton | Gazbeton Blok, Lento ve Panel · Söke & İzmir
  - **uzunluk**: 59
  - **not**: Mevcut: "Ege Gazbeton | Hammaddeden Binaya Gazbeton" (42). Yeni sürüm ürün anahtar sözcüklerini (blok, lento, panel) ve yeri taşır; hikâye adı (hammaddeden binaya) description'a.
-
  - **konu**: <title> EN
  - **oneri**: Ege Gazbeton | AAC Blocks, Lintels and Panels · Söke & İzmir
  - **uzunluk**: 60
  - **not**: dil.js sayfa.baslik şu an "AAC from raw material to building": değiştir.
-
  - **konu**: meta description TR
  - **oneri**: Gazbeton blok, lento, panel ve tutkal Söke ve İzmir'deki iki fabrikada üretilir. Hayalden yuvaya hikâyeyi izleyin, projeniz için teklif alın.
  - **uzunluk**: 141
-
  - **konu**: meta description EN
  - **oneri**: AAC blocks, lintels, panels and adhesive made in two plants in Söke and İzmir. Follow the story from idea to home and get a quote for your project.
  - **uzunluk**: 147
-
  - **konu**: H1 ve başlık yapısı
  - **oneri**: Tek H1: hero "Her yuva bir çizgiyle başlar." (HTML'de, JS beklemeden). Marka adı eyebrow + title + ilk cümlede ("Gazbeton blok, lento, panel ve tutkal; Söke ve İzmir'deki iki fabrikada…"). Perde başlıkları H2 (mevcut). Slogan H1'de değil.
  - **not**: H1 anahtar sözcük içermiyor ama title ve ilk paragraf taşıyor. Bu kararın SEO etkisini site ekibi onaylamalı (açık soru 1).
-
  - **konu**: JS'siz / hareket azaltma içeriği
  - **oneri**: Tüm TR metin HTML'de (zaten); durağan sütun her sahnenin son karesi + başlığı + rakamı + kaynağı gösterir. Botlar ve yardımcı teknolojiler hikâyenin tamamını metin olarak okur. EN metin dil.js'te: arama motoru için EN ayrı URL gerekir (açık soru 12).
-
  - **konu**: Canonical ve parametreler
  - **oneri**: <link rel="canonical" href="https://www.egegazbeton.com.tr/"> (ana sayfa kök adresi — adres teyit gerekli). ?kaynak=hikaye&dil=…&urun=… gibi parametreli adresler kanonik ile birleşir; bağlantılar JS ile parametrelendiği için taranan HTML temiz kalır.
-
  - **konu**: OG görseli (varsayılan)
  - **kare**: t=22 tır yan görünüm (s0d)
  - **oneri**: og:image 1200×630 JPEG ≤300 KB (WhatsApp önizlemesi için pratik sınır, test et). Kaynak 1600×900 kare, 16:9 → 1,91:1 kırpma (üst/alttan ~30 px); sağ alt köşeye lime şeritli "EGE GAZBETON" alt bandı PIL ile (tools/og_uret.py, yeni). Gerekçe: besleme akışında lime tek keskin renk leke; "gazbeton + lime ambalaj" bir bakışta; insan yüzü yok.
  - **not**: OG kartında logo/slogan metni "logo en sonda" kuralıyla çelişmez (hikâye dışı), ama müşteri onayı gerekir (açık soru 13). Görsel Blender karesi; yapay zekâ yok.
-
  - **konu**: OG görseli (alternatifler)
  - **kareler**:
    -
      - **t**: 28
      - **kare**: akşam, pencereler yanık
      - **kullan**: duygu odaklı sosyal paylaşım (Instagram/Facebook gönderisi); /duvar-tasarla/ yapı sahibi kampanyası
    -
      - **t**: 131
      - **kare**: küre, 25+ ülke · 5 kıta (metinsiz)
      - **kullan**: /ihracat/ sayfası OG görseli ve LinkedIn B2B paylaşımı
    -
      - **t**: 110
      - **kare**: yüklü tır kahraman karesi
      - **kullan**: bayi/dağıtıcı iletişimi, WhatsApp B2B paylaşımı
-
  - **konu**: og/twitter etiketleri
  - **oneri**: og:type=website, og:site_name="Ege Gazbeton", og:locale=tr_TR (+ og:locale:alternate=en_US), og:title="Her yuva bir çizgiyle başlar — Ege Gazbeton", og:description=meta description, og:image + og:image:width=1200 + og:image:height=630 + og:image:alt="Üç katlı gazbeton binanın önünden geçen, lime streçli gazbeton paletler taşıyan Ege Gazbeton tırı"; twitter:card=summary_large_image.
-
  - **konu**: Yapılandırılmış veri
  - **oneri**: JSON-LD: Organization (name "Ege Gazbeton", legalName "Akkuş Mimarlık İnşaat Turizm San. ve Tic. A.Ş." [alt bilgi metninden; teyit gerekli], url, logo = GERÇEK logo dosyası [henüz yer tutucu], sameAs = teyit gerekli) + WebSite + ItemList (altı ürün sayfası bağlantısı). Ürün özelliği (λ, G sınıfı) JSON-LD'ye YALNIZ doğrulanmış kaynaktan.
-
  - **konu**: "Hikâyeyi atla" bağlantısı
  - **oneri**: Üç yer: (1) sayfanın ilk odaklanılan öğesi gizli "Ana içeriğe geç" (.eg-atla-link → #icerik, mevcut); (2) hero içi görünür "Hikâyeyi atla" (.eg-atla → #teklif); (3) yolculuk çubuğunda "Teklif". Hepsi aynı finale gider (sahneyeGit('son'), akış p=0,62). #teklif kancası JS'siz ve botlar için gerçek bölüme çapa. data-iz: hikaye_atla / yol_son.
-
  - **konu**: Derin bağlantı ve paylaşım
  - **oneri**: Yolculuk çubuğundaki bölüm adreslerine (#sahne-s1 …) ek olarak: sayfa açılışında #sahne-sX (ya da #t=90) algılanırsa sahneyeGit; böylece "ürün turunu göster" gibi doğrudan paylaşım mümkün. Web Share API "Paylaş" yolculuk çubuğu menüsünde (finale ekranında ayrı düğme yok: sadeleştirme): temiz URL + hash. Paylaşılan adrese kaynak parametresi eklenmez.
-
  - **konu**: Çekirdek web verileri
  - **oneri**: LCP öğesi = poster (kareler/s0/poster.webp): <link rel="preload" as="image" fetchpriority="high"> ve d/m için media koşullu iki preload; CLS: sabit sahne yüksekliği (svh), INP: pasif scroll dinleyicileri (mevcut). Hedef (varsayım, ölçülecek): 4G'de LCP ≤ 2,5 sn.
-
  - **konu**: Anahtar sözcük ve içerik derinliği
  - **oneri**: "Ürün grupları" bölümüne "Gazbeton nedir?" kısa bloğu: yalnız doğrulanmış metinle (kum, kireç, çimento, alçı, alüminyum tozu; kabarma; tel kesim; otoklavda buharla sertleşme; kapalı hava hücresi). İkincil anahtar sözcükler: gazbeton blok, gazbeton lento, gazbeton panel, gazbeton tutkalı, U blok, EGEPOR. Söke ve İzmir yer adları doğrulu. Fiyat/"ucuz" sözcüğü yok.
-
  - **konu**: Görsel alt metni
  - **oneri**: Sahne posterleri alt="" aria-hidden (mevcut) kalır; her sahne aria-label ile anlatılır. OG ve basın görselinin alt metni yukarıdaki cümle.

### Mobil
-
  - **konu**: Kalıcı CTA yok (hata)
  - **durum**: hikaye.css ≤760 px: .eg-ust__sag .eg-dugme--kucuk {display:none}
  - **oneri**: Hikâye boyunca logo gizli olduğundan (marka_gorunurlugu → LOGO) üst çubukta yer var: logo yuvasına düz metin marka adı, sağda [TR/EN] + kompakt lime [Teklif] (min 44×44 px) + menü. 360 px genişlikte dar sığar (16+16 gutter → 328 px; marka metni ≈110 + dil ≈64 + Teklif ≈84 + menü 44 + 3×8 boşluk = ≈326): sığmazsa dil düğmesi menü içine alınır. Logo t=141'de yerine dönünce Teklif düğmesi gizlenir (finalde ana CTA var), sonrası bölümde tekrar görünür.
-
  - **konu**: Kaydırma ipucu telefonda gizli (hata)
  - **durum**: .eg-giris__alt .eg-kaydir {display:none} (≤760 px)
  - **oneri**: Tüm anlatım kaydırmaya bağlı; ilk kez gelen telefon kullanıcısı bunu bilmeyebilir. Hero altında orta: büyük ok + parmak mikro animasyonu, ilk hareketle sönsün. t=3 sn'de kıvılcım çizgisi (s0 planı) ek ipucu.
-
  - **konu**: Hero ekranı
  - **oneri**: 360×640 ve 390×844'te 100 svh içinde: eyebrow + H1 + (yükseklik ≤700 px ise cümle gizli, mevcut kural) + 1 lime düğme (tam genişlik, 48 px) + çipler (tek satır başlığı + 3 çip iki satıra sarılabilir) + "Hikâyeyi atla". Başlık clamp(38,11vw,52). Üst çubuk 64 px.
-
  - **konu**: Başparmak bölgesi
  - **oneri**: Telefonda anlatım üst %40, 3B konu alt yarı. Otomatik CTA pencereleri (t=38–40, 64–67, 99–101, 115–118, 131–134) 3B konuyu örtmeden anlatım sütununun altına, finale ise akış içi tam genişlik düğmelere konur (alt sabit çubuk son_bar_mobil ertelendi: numara teyidi gelene dek yok). Kadraj sınaması: her pencere için alt %14 şerit konudan boş olmalı (kareler kontrol edilir).
-
  - **konu**: Dokunma hedefleri
  - **oneri**: Tıklanır nokta: görsel halka 18–22 px, vurulabilir alan 48×48 px; komşu noktalar arası ≥ 8 px. Çip, bağlantı, kart düğmeleri ≥44 px. İlk noktada "dokunun" nabzı (s2 t=72) bir kez.
-
  - **konu**: Kart = alt sayfa
  - **oneri**: Nokta kartı telefonda noktanın yanında değil ekran altında alt sayfa (bottom sheet); başlık, tek cümle, kaynak, iki bağlantı yan yana (Ürün sayfası | Teknik föy). Kaydırma kartı kapatır (kartta kalırken film ilerlemez karışıklığı olmaz). Arka plan scrim'i opaklık ile (backdrop-filter yok).
-
  - **konu**: Kaynak satırı gizleniyor (kural ihlali)
  - **durum**: .eg-rakam small {display:none} (≤760 px)
  - **oneri**: "Her sayının kaynağı kartta yazılı" kuralı telefonda da geçerli: kaynağı rakamın altında 12 px tek satır göster ya da kartta tek dipnot satırı (finale ajanı da aynı karara varmış: gizlenmez). Kontrast ≥4,5:1.
-
  - **konu**: Veri ve ağ
  - **oneri**: navigator.connection.saveData veya effectiveType ≤ 3g: "hafif mod" = poster + durağan sütun (az-hareket gibi) + tüm CTA'lar görünür + "Hikâyeyi izle" isteğe bağlı düğme. Kare indirme zaten yakın sahneyle sınırlı; m seti her 2. kare (EGE_MINSTEP=2). Tahmini indirme boyutu sınama sonrası yazılır (rakam şimdi yok).
-
  - **konu**: iOS/Android adres çubuğu
  - **oneri**: Adres çubuğu açılıp kapanınca innerHeight değişir; main.js resize → akisBoyu() akış yüksekliğini her seferinde yeniden yazıyor: yalnız genişlik/yön değişince ya da yükseklik değişimi >%15 ise yeniden hesapla; konumlar svh tabanlı. Aksi hâlde kaydırma sırasında sahne sıçrar (dönüşümü doğrudan bozar).
-
  - **konu**: Başparmakla kaydırma uzunluğu
  - **oneri**: Toplam akış 3212 vh ≈ 32 ekran. Yolculuk çubuğu (bölüm adı + ilerleme) t=2'den itibaren görünür; adından dokununca bölüm listesi + "Teklif" atlaması açılır: uzun kaydırmada yorulan ziyaretçi için kaçış yolu.
-
  - **konu**: Tel / WhatsApp
  - **oneri**: ERTELENDİ: numara teyidi gelene dek finalde WhatsApp düğmesi ve alt sabit çubuk konmaz (son_whatsapp_mobil, son_bar_mobil → finale_cikarilan_ertelenen). Teyit gelirse (önceden dolu "Hikâyeden geliyorum: {ürün}") finaldeki ≤7 etkileşimli öğe sınırı korunarak yeniden değerlendirilir. Numara ve çalışma saati teyit gerekli: uydurma numara konmaz.
  - **teyit_gerekli**: True
-
  - **konu**: Teklif formu el değmesi
  - **oneri**: Site işi: urun ön seçili; ölçü alanında inputmode="decimal"; ≤3 zorunlu alan (ad, telefon/e-posta, ölçü/açıklama); "Hikâyede baktığınız: EGEPOR ×" çipi; gönderim sonrası aynı sayfada teşekkür + katalog PDF bağlantısı.
-
  - **konu**: Paylaşma
  - **oneri**: navigator.share ile "Paylaş" (yalnız yolculuk çubuğu menüsü; finale ekranında yok): başlık + temiz URL; WhatsApp B2B'de baskın olduğundan OG görseli ≤300 KB.
-
  - **konu**: Performans ve erişilebilirlik
  - **oneri**: DPR ≤1,25, ≥50 fps (ege_kare_hiz); prefers-reduced-motion: tek kare + metin + tüm CTA'lar görünür; yatay telefon (oran ≥0,82) d kare setini kullanır: CTA'lar masaüstü yerleşimine geçer.
-
  - **konu**: Dil algısı
  - **oneri**: navigator.language Türkçe değilse hero'da (çip satırında) "View in English" mikro bağlantısı; otomatik geçiş yok.

### İlk 10 saniye testi

AMAÇ: 10 gerçek (duvar saati) saniyede ziyaretçi şunları bilmeli: (1) hangi firma, (2) ne satıyor, (3) nasıl devam edeceği, (4) bu firma özenli ve güvenilir hissi, (5) eylem/çıkış yolu. Hikâye kaydırmaya bağlı olduğu için üç izleyici tipi var; üçü de test edilir.

ÖN KOŞUL: poster (s0 F000) ilk boyamada; H1 + cümle HTML'de; LCP ≤2,5 sn (4G, hedef).

PASİF İZLEYİCİ (10 sn kaydırmıyor), masaüstü 1600×900:
 0,0–0,8 sn  Bej kâğıt, koyu vinyet; makro kadrajda kapı konumunda tek sıcak (amber) ışık noktası nabız atar, kâğıt lifleri eğik ışıkta. Solda: "EGE GAZBETON · Söke & İzmir" / "Her yuva bir çizgiyle başlar." / tek cümle (gazbeton blok, lento, panel, tutkal; iki fabrika). Üst çubuk: marka adı (düz metin) + çizgili "Teklif Al" (hero ana düğmesi ekrandayken ikincil; hero çıkınca küçük lime). Hissi: sakin, sıcak, el yapımı; "sıradan bir üretici sitesi değil".
 0,8–2,5 sn  Göz ışık noktası → başlık → tek lime düğme. Lime bu karedeki tek keskin renk (ışık bilerek amber). 2 sn'de: firma = Ege Gazbeton, ürün = gazbeton.
 2,5–3 sn    Kıvılcım nabzı (1 Hz) sürer; imleç kâğıtta grafit iz bırakır (1 sn'de silinir).
 3,0–4,5 sn  Kaydırmayan kullanıcıya otomatik sinyal: kıvılcım kısa bir çizgi çeker, "Kaydırın" oku nabız atar (telefonda da görünür). Hissi: "bir şey olacak, kontrol bende".
 4,5–10 sn   Hero yerinde; çıkış yolları açık: Teklif Al, 3 kitle çipi, "Hikâyeyi atla", yolculuk çubuğu. Dikkat dağıtan ikinci düğme yok.

AKTİF İZLEYİCİ (referans hız 22 vh/sn; 10 sn ≈ film t=10):
 sn 0–1  Hero düğme/çip/atla soluklaşır (H1 + cümle kalır); ışınlar kâğıdı boydan boya uzar.
 sn 2–5  Kalem vaziyet planını çizer; "Önce fikir, sonra plan: güneşe, sokağa ve bahçeye göre." (alt çizgiler çizim anında).
 sn 5–8  Kamera eğilir; çizgiler hacme döner: bina kâğıttan YÜKSELMEZ, kalemle ÇİZİLİR.
 sn 8–10 "Çizgi hacme dönüşür." eskiz tamam, kalem kalkar.
 Hissi: merak + hayranlık ("nasıl yapmışlar?"); güven: titiz çizgi = titiz üretici. Brand kuyruğu: eyebrow, sekme başlığı, üst çubuk metni.

HIZLI İZLEYİCİ (3× ≈ 66 vh/sn): 10 sn'de t≈30: sokak, lime tır, akşam, "Peki bu evi iyi yapan ne?" — soru merak kancası olarak çalışır; kaçırdığını yolculuk çubuğundan geri alır.

TELEFON (390×844): hero 100 svh'de: eyebrow, H1, 1 lime düğme (tam genişlik), çip satırı, "Hikâyeyi atla" ve (YENİ) alt ortada büyük "Kaydırın" oku. Başparmakla ilk kaydırma ≤3 sn hedefi. Anlatım üstte, kâğıt/ev altta.

10. SANİYENİN SONUNDA ZİYARETÇİ BİLİR: Ege Gazbeton gazbeton (blok, lento, panel, tutkal) üretiyor; iki fabrikası var; bu iş ustalık ve çizgiyle başlıyor; kaydırarak ilerleniyor; teklife/föye/ihracata tek tıkla gidilebiliyor.
HİSSEDER: sakinlik, merak, "burada acele ettirilmiyorum", ilk güven kıvılcımı.

GEÇME ÖLÇÜTLERİ (5 sn ve 10 sn testi; segment başına ≥5 kişi: yapı sahibi, mimar/mühendis, bayi/ihracat; her biri telefon + masaüstü; 5 sn sonra ekran kapatılır):
 1. "Hangi firma?" → doğru ad (5/5 hedef).
 2. "Ne satıyor?" → gazbeton/yapı malzemesi (kitle farkı: mimar kolay, yapı sahibi "gazbeton" dediğinde ek puan).
 3. "Şimdi ne yapardın?" → kaydırırım / Teklif Al / atla (bilmeyen = başarısız).
 4. "Bir sıfat söyle." → sıcak/özenli/profesyonel (satıcı/reklam sıfatı = uyarı).
 5. "Hangi renk aklında?" 10 sn'de lime hatırlanmamalı (lime ilk kez t=17'de, ödül); yalnız düğme.
BAŞARISIZLIK İŞARETLERİ: boş/gecikmeli poster (>1 sn); H1 okunmuyor; kaydırma yapılacağı anlaşılmıyor (telefon!); 3'ten fazla düğme; hareket kaybı (<50 fps) ya da ilk kaydırmada atlama; "bu kimin sitesi?".
CANLI ÖLÇÜM: ege_hikaye_gor → ege_hikaye_basla (bekleme_ms): ilk eylem süresi; 10 sn içinde ege_atla oranı; ege_ilerleme t=10 oranı; ege_kare_hiz.

