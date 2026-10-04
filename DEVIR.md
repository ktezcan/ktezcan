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

## 7. Durum ve sıradaki işler

- [x] Hikâye kararları, 6 sahne yapısı, TR/EN metinler, etiketler
- [x] Perde 1, 2, yol, dünya betikleri ve önizleme testleri
- [ ] Tam render'ların bitmesi (`tools/render_hepsi.sh`) → `kareler.py` → `derle.mjs` → sınama → zip
- [ ] Müşteri geri bildirimi turu (aşağıdaki "bilinen eksikler" ile birlikte)

Bilinen eksikler / geliştirme önerileri:
- Özellik animasyonları (ısı akışı, A1 alev, yüzme/hafiflik, testere) şimdilik ürün turunda kart olarak; `stil_r4.sahne_isi`,
  `stil_r5.sahne_alev/yuzer/derz/testere` hazır taslaklar — her durağa kısa ek sahne olarak bağlanabilir.
- Fabrika hâlâ "maket" dili (beyaz kütleler); daha gerçekçi cephe/malzeme istenebilir.
- Yakın plan yüzler zayıf (bkz. kural). Bisikletli pedal çevirmez (serbest sürüş).
- Sayfadaki logo ve tanıtım bağlantıları yer tutucu.
