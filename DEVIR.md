# DEVİR — Ege Gazbeton giriş animasyonu (işyerindeki Claude için)

> İlk mesaj önerisi: **"DEVIR.md'yi oku, kaldığı yerden devam et."**
> Depo: `ktezcan/ktezcan`, dal: `claude/ege-gazbeton-site-animation-cxwzho`. Bu dosya tek doğru kaynaktır;
> önceki oturumun geçici klasörü (scratchpad) yoktur, gereken her şey depodadır ya da bir betikle yeniden üretilir.

## 1. Ne yapıyoruz

egegazbeton.com.tr ana sayfasının **giriş bölümü**: kaydırmaya bağlı, sinematik hikâye. Kareler Blender Cycles
ile önceden hesaplanır (WebP dizileri), sayfa yalnız kare oynatır + HTML etiket/kart gösterir. TR + EN.
Masaüstü (1600×900, `d`) ve dikey telefon (768×1366, `m`). Teslim: çift tıkla açılan maket (`giris-hikaye/`) + zip.

## 2. Değişmez kurallar (müşteri kararı)

- Her sayının **kaynağı kartta yazılı** olur (Ürün föyleri, Ege Gazbeton ortak rakamlar, CE belgeleri, ODTÜ, ihracat bölümü).
- İhracat: **"25+ ülke · 5 kıta"**. Ülke adı, ülke sınırı, müşteri sayısı, fiyat **yok**. Türkiye vurgusu yalnız gerçek Türkiye poligonu.
- A1 = **"yangına tepki sınıfı"** (EN 13501-1). Asla "yanmaz" denmez.
- **YEŞİL = BİZİM**: lime yalnız bizim ürüne (streç film, tutkal bandı, fabrika şeridi, lime halka, ürün vurgusu).
- **Yapay zekâ görseli yok.** Her kare Blender'da kodla üretilir.
- **3B render içine yazı/rakam yok.** Etiketler sitede HTML/SVG (TR/EN). Panolarda PIL ile önizleme.
- Kanvas üzerinde `backdrop-filter` / `mix-blend` yok; DPR ≤ 1,25; ≥ 50 fps; `file://` ile çevrimdışı çalışmalı.
- Natro FTP `.js` yüklemeyi engelliyor → zip olarak yükle, sunucuda aç.
- Logo her zaman en sonda. Seri render öncesi **altın kare** onayı. Maket (sayfa) Artifact olarak yayınlanmaz.
- Depo herkese açık: şirket iç dosyası/fotoğrafı konmaz. MakeHuman verisi konmaz (`tools/mh_indir.sh` ile indirilir).
- Yakın planda insan yüzü yok (manken gibi duruyor) — insanlar orta/uzak planda.

## 3. Hikâye kararları (müşteri "başlat" ile onayladı)

Ana karar: **hikâye evle başlar** (önce duygu, sonra kanıt, en sonda güç). Akış = 6 sahne, `src/hikaye/ayarlar.js`:

| id | Sahne | Betik | İçerik |
|---|---|---|---|
| s0 | **Hayalden yuvaya** (ana giriş) | `blender/s0_hayal.py` + `tools/s0_birlestir.py` | kıvılcım → kâğıtta vaziyet planı kendini çizer → kamera eğilir, bina kâğıttan yükselir (eskiz) → binadan açılan karanlık daire → tel kafes → gazbeton bloklar sıra sıra iner → lime çizgili çapraz silme → fotogerçekçi sokak (geçen araba, **eller gidonda bisikletli**, yayalar, **Ege Gazbeton tırı** lime streçli paletlerle) → gün ilerler → akşam, pencereler tek tek yanar |
| s1 | **Ürün turu** "Bu evi iyi yapan ne?" | `blender/s1_urun.py` | maket stüdyo; kamera evin etrafında döner; duraklar: duvar blokları → lento → U blok (çatı hatılı) → gazbeton tutkalı (derz) → panel → EGEPOR (kolon/kiriş kaplaması). Durakta ürün gerçek malzemede + lime kenar ışıltısı, gerisi röntgen. Son: kamera ön cephedeki tek bloğa iner, blok dışarı çıkar, gerisi beyaza erir |
| s2 | Doğuş | `blender/s1_dogus.py` (önceki teslim) | blok hammaddeye çözülür, kabarma, tel kesim |
| s3 | Gözenek | `blender/s2_gozenek.py` (önceki teslim) | kapalı hava hücresi, λ 0,08 · A1 · 300–600 |
| s4 | **Yol** | `blender/s4_yol.py` | Söke fabrikası sabah ışığında; Ege tırı sahadan çıkar, kamera yandan izler, sonra tepeye yükselir |
| s5 | Dünya | `blender/s4_dunya.py` | tepeden İzmir → küre; 5 kıtaya yaylar, yay başında ilerleyen ışık damlası, varışta kıta ışır |

Sonra: SON bölümü (teklif + logo + slogan "Bugünden Yarına Güvenle").

Geçiş kuralı: bir sahnenin son şekli, sonrakinin ilk şekli olur (çizgi→plan, aks→kolon, kafes→blok, blok→gözenek, tepeden fabrika→tepeden İzmir).
Sahne arası erime: `GECIS` (ayarlar.js).

### Teyitli bilgiler (müşteri onayı + egegazbeton.com.tr ürün sayfaları)
- **EGEPOR**: kolon ve kiriş kaplaması (müşteri onayladı). Sayfa: dış cephe, otopark ve bodrum tavanı, kolon/kiriş kaplaması;
  60 × 25–50 cm, 5–35 cm; λkuru 0,051–0,062 W/mK; 150–200 kg/m³. Kaynak: https://www.egegazbeton.com.tr/urunlerimiz/egepor/
- **U blok** (ürün turu 3. durak, çatı hatılı = parapet üst sırası, U kesit + donatı + dolan hatıl betonu): hatıllarda ahşap kalıp yerine;
  yüksek duvar ara hatılı, çatı hizası, yatay/düşey betonarme hatıl, gizli baca, yağmur iniş borusunu gizleme.
  G4/06: 60 × 25 cm, 20–25 cm; λkuru 0,16 W/mK; 50 kgf/cm²; 600 kg/m³. Kaynak: https://egegazbeton.com.tr/urunlerimiz/u-bloklar/
- Not: üretici sayfası "A1 Hiç Yanmaz" yazıyor; bizim kuralımız yine **"A1 yangına tepki sınıfı"**.
- Ürün kataloğu (PDF): https://www.egegazbeton.com.tr/wp-content/uploads/2025/10/Ege-Gazbeton_%C3%9Cr%C3%BCn-Katalo%C4%9Fu-22.09.25.pdf
  (bu ortamdan erişilemedi; işyerinde rakamları buradan da teyit edin)

### Teyit bekleyenler (müşteriye sor)
1. **Gerçek logo dosyası**: tır kabinine çıkartma için `EGE_LOGO=/yol/logo.png` verilirse `s0_hayal.ege_tiri()` kapılara basar.
   Şu an logosuz (sitede tırı takip eden "Ege Gazbeton" etiketi var). Sayfadaki logolar da YER TUTUCU (`LP\img\logo_white.svg` ile değiştir).
2. **Köşe bloğu** ürün turunda yok (istenirse eklenir).

### Saniye saniye hikâye planı (yeni, onay bekliyor)

`docs/HIKAYE_OZET.md` (kısa özet + karar listesi), `docs/HIKAYE_PLANI.md` (146 saniyenin her biri), kaynak `docs/plan/*.json`
(`python tools/plan_md.py` ile belge üretilir). Plan onaylanmadan yeni render serisi başlatılmaz. Planın yakaladığı kod hataları
(ürün turunda donatıya lime, kamera ayna kayması, panel 8,8 m, dünyada Amerika/Okyanusya arka yüzde) uygulama sırasında düzeltilecek.

## 4. Kurulum

```bash
pip install bpy==5.0.1 numpy pillow scikit-image        # Blender 5.0 (Python 3.11)
python blender/dokular.py tex && export EGE_TEX=$PWD/tex  # gazbeton dokuları
node tools/kure_noktalari.mjs <node_modules_kökü>         # tex/kara_noktalari.json (world-atlas, topojson-client)
tools/mh_indir.sh ~/mh && export EGE_MH=~/mh              # insan modeli (CC0)
npm i esbuild three @fontsource/barlow @fontsource/barlow-condensed world-atlas topojson-client   # tools/ için
```

## 5. Üretim hattı

```bash
PY=python tools/render_hepsi.sh ~/render        # tüm yeni sahneler (saatler sürer; yarıda kalırsa tekrar çalıştır)
EGE_PREVIEW=30 python blender/s1_urun.py --variant d --frames 0,40 --out /tmp/t --samples 8   # hızlı önizleme
python tools/s0_birlestir.py ~/render/s0src ~/render d m   # s0: kaynak kareler + 2B geçişler → s0d/, s0m/
python tools/kareler.py ~/render                # PNG → WebP + kareler-meta.js (render kökünde s0d..s5m klasörleri)
node tools/derle.mjs <node_modules>             # src/hikaye → giris-hikaye/assets/js/hikaye.js
node tools/sinama.mjs sinama                    # başsız tarayıcı sınaması
tools/paketle.sh ~/render <node_modules> ~/teslim   # zip
```

Render kökü düzeni: `s0d s0m` (birleştirilmiş), `s1d s1m` (ürün turu), `s2d s2m` (doğuş), `s3d s3m` (gözenek), `s4d s4m` (yol), `s5d s5m` (dünya).
Telefon setleri `EGE_MINSTEP=2` ile her 2. kare; oynatıcı aradaki kareyi erimeyle doldurur.

Süreler (4 çekirdek CPU, tam çözünürlük): s0 eğim ~25 sn/kare, dolum ~45–70, sokak ~70, plaka ~150; s1 ~40; s4 ~40; s5 ~30.

## 6. Dosya haritası (yeni)

| Dosya | Görev |
|---|---|
| `blender/s0_hayal.py` | Perde 1 kaynak kipleri: `egim`, `dolum`, `sokak`, `plaka`. Tek kamera C (göz hizası). Etiket çapaları `meta.json` |
| `tools/s0_birlestir.py` | Perde 1 son dizi (162 kare): kıvılcım, plan çizimi, dairesel silme, çapraz silme, gün erimesi, pencere maskeleri |
| `blender/s1_urun.py` | Ürün turu: geçiş malzemesi (gerçek ↔ röntgen ↔ saydam + lime kenar), Egepor levhaları, son dalış |
| `blender/s4_yol.py` | Fabrika + tır + kamera yükselişi |
| `blender/insan.py` | `bisikletli()` (IK: eller gidonda, ayaklar pedalda), `yuru_kare()` (kare kare yürüyüş), at kuyruğu başa bağlı |
| `blender/stil_r*.py`, `sokak.py`, `bina_detay.py` | Stil denemeleri ve ortak sahne parçaları (bina, sokak, araba, ağaç, oda, gök) |
| `src/hikaye/dil.js` | EN metinler + tıklanır nokta kartları (TR/EN, kaynaklı) |

## 7. Durum ve sıradaki işler (güncel — oturum sonu)

**Karar özeti (müşteri onayladı):** süre 146 sn (1 film sn = 22 vh); slogan "Bugünden Yarına Güvenle" yalnız finalde, açılış başlığı
"Her yuva bir çizgiyle başlar."; tır kabininde logo yok; A1 alev/"serin yüz" ve "suda yüzer" sahneleri yok (A1 = yalnız sınıf kartı);
"25+ ülke · 5 kıta" güncel; Türkiye poligonu lime olabilir; Aliağa/Alsancak limanı ifadesi kaynaksız → kullanma; kaydırma kilidi yok;
tarayıcı depolaması yok; fabrika temsilî. Teslim video DEĞİL: çift tıkla açılan sayfa maketi + kareler + kod.

**Tamam ve depoda**
- Kod: `blender/s0_hayal.py` (egim/dolum/sokak/plaka), `s1_urun.py`, `s4_yol.py`, `s4_dunya.py`, `s1_dogus.py` (Doğuş), `s2_gozenek.py` (Gözenek),
  `insan.py` (bisikletli IK, yürüyüş), `sokak.py` (araba detayları WIP), `stil_r5.py` (tır ayrıntıları WIP), `tools/s0_birlestir.py`.
- Plan: `docs/HIKAYE_OZET.md` (kısa özet + 10 karar), `docs/HIKAYE_PLANI.md` (146 saniyenin her biri), kaynak `docs/plan/*.json`
  (akt-s0..akt-son, moduller, pazarlama, denetim). `python tools/plan_md.py` belgeleri yeniden üretir.
- Altyapı: `tools/render_kuyruk.py` (aşama-öncelikli render kuyruğu; `blender/spec/<id>.json` ile iş tanımı; docstring'e bak),
  `tools/kare_taklit.py` (yer tutucu kareler: sayfa sınaması için), kayıt noktaları `src/hikaye/moduller/index.js`, `src/hikaye/final.js`.
- `docs/uretim/is-akislari/*.js`: sahne sahne / web işi için hazır görev tanımları (bkz. OKU.txt) — yerel Claude'a olduğu gibi verilebilir.

**Yapılmadı (sıradaki işler, öncelik sırasıyla)**
1. Sahne betiklerini plana göre uygulamak: (s0) eskiz zeminden yükselmesin, ÇİZİLSİN; park halindeki kırmızı arabanın önü hatalı olabilir
   (sokak.py araba() WIP, görsel doğrulanmadı); tır/araç ayrıntısı; (s1) donatıya lime uygulanıyor (KURAL İHLALİ), kamera başlangıç azimutu
   s0 ile ayna kaymış (−32° ↔ +32°), panel modelde 8,8 m (kart 6 m), 152 kare ve render hızlandırma (transparent_max_bounces 32→12);
   (s5) Amerika/Okyanusya küre dönmediği için arka yüzde, Amerika hedefi denizde; (s2/s3/s4) plandaki ayrıntılar. Her sahne bitince
   `blender/spec/<id>.json` yazılır, kuyruk otomatik render eder.
2. Render: `python tools/render_kuyruk.py --root <kök> --python <bpy python>` (EGE_TEX, EGE_MH ortam değişkenleri gerekir). ≈1230 kare, ≈26 saat
   (4 çekirdek). Aşamalar sayesinde her an kesilebilir; sayfa seyrek karelerle de çalışır. Paylaşılan geçiş kareleri (s1[151]←s2[000],
   s3[084]←s4[000], s4[095]←s5[000]) paketlemede kopyalanır (`tools/dikis_kopyala.py` henüz yazılmadı).
3. Web: `index.html` hâlâ ESKİ 6 sahne vuruşlarını taşıyor; plana göre 7 parçalı akış (boylar vh: 704/836/440/308/352/352 + finale 220), GECIS=0
   (eşleşen kare dikişleri), pencereli kare belleği (ImageBitmap; en kötü durumda ≈2,9 GB çözülmüş kare tutuluyor), finale (`final.js`),
   CTA'lar ve etkileşimli modüller (MVP: ürün seçici, duvar hesap, maket blok sayacı, önce/sonra, kesit gezgini) yapılacak.
4. Paket: `tools/paketle.sh <render_kök> <node_modules> <çıktı> [python]`; iki zip hedefi (maket + kaynak) için `tools/teslim.sh` yazılacak.

**Teyit bekleyenler:** gerçek logo dosyası (yer tutucu logolar kalır); duvar bloğu 5–35 cm; ODTÜ −%17 kapsamı; 1.100.000 m³ süre ibaresi;
otoklav/gözenek rakamları (ekranda yok). Denetim bulguları: `docs/plan/denetim.json`.

**Bu oturumda teslim edilen önizleme maketi:** mevcut karelerle çalışır (eksik sahneler boş/eski karelerle görünür; Perde 1 yalnız masaüstü).

## 8. Oturum notu — 2026-10-04 (bulut oturumu) ve MÜŞTERİ KARARLARI v2

**Bu oturumda yapılanlar (dalda):** ürün turu dalış lekesi giderildi (`s1_urun.py`: dalışta saydam sıçrama 32, ev tam saydamlaşınca gizlenir);
dünya (`s4_dunya.py`): 193 kare, küre boylam/eğim dönüşü (Amerika/Okyanusya ön yüzde), Amerika hedefi (15°, −88°) karada, varış dalgası,
ufuk testli çapalar, zemin lime halkası + lime kontur ışığı kaldırıldı; eskiz (`s0_hayal.py egim`): **bina yükselmez, kalemle sırayla çizilir**
(38 kare; üç render S/E/B + kenar maskesi; kalem ucu `meta.pen`; `s0_birlestir.py` ve `kareler.py` uyumlu).
Render ortamı: `EGE_RES=<yüzde>` (kit.py) küçük çözünürlük, örnek sayısı aynı; `EGE_PREVIEW` ise örnek ≤ 8.

**Müşteri kararları v2 (tıklamalı soru-cevap):**
- s0 sokak: Ege atmosferi VAR (uzak tepeler, deniz sisi, zeytin/servi, taş duvar, bugenvil). Pencereler yalnız zamanla yansın; "ışığı sen yak" ve kapı/aile-girer animasyonu YOK.
- s1 ürün turu: röntgen = mavi-beyaz teknik çizim; 152 kare (plana göre).
- s2 doğuş: koyu fabrika havası kalsın; kalıp/tel kesme/otoklav temsilî tasarım.
- s3 gözenek: bilimsel makro (küçük düzensiz hücreler, ince zarlar); ölçek/mm/hücre sayısı ekranda YOK.
- s4 yol: Söke fabrikası için kullanıcı referans verecek (gelene dek temsilî); tır çıkışı 8 kare/sn (128 kare).
- s5 dünya: Türkiye lime (marka vurgusu); kıta etiketleri VAR (HTML, ülke adı yok).
- son: üst çubuk logosu baştan görünür. Süre 146 sn. Ses YOK. Bu oturumda seyrek set (her 8. kare, küçük çözünürlük) render edilir; tam render kuyruğu işyerinde.
