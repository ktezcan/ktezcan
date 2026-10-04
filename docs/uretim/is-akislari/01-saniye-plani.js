export const meta = {
  name: 'ege-hikaye-saniye-plani',
  description: 'Tüm Ege Gazbeton giriş hikâyesini (146 sn) saniye saniye planla: 7 perde + etkileşim modülleri + pazarlama, denetim ve düzeltme',
  phases: [
    { title: 'Taslak', detail: 'perde başına saniye saniye plan (JSON), etkileşim/öğretici modülleri, pazarlama akışı' },
    { title: 'Denetim', detail: 'geçişler, kurallar, okuma süresi, render maliyeti' },
    { title: 'Düzeltme', detail: 'denetimin bulduğu sorunları ilgili perdede gider' },
  ],
}

const SP = '/tmp/claude-0/-home-user-ktezcan/c8c14d5b-13a3-504d-8378-fcae1d923068/scratchpad'
const REPO = '/home/user/ktezcan'
const PLAN = SP + '/plan'

const ZAMAN = `ZAMAN BÜTÇESİ (film saniyesi; toplam 146 sn). 1 film saniyesi = 22 vh kaydırma (referans hız; satırdaki vh = t*22, akış başından).
  s0  Hayalden yuvaya   t=0–32    (32 sn)
  s1  Ürün turu         t=32–70   (38 sn: giriş 4 + 6 ürün x 5 + çıkış 4)
  s2  Doğuş             t=70–90   (20 sn)
  s3  Gözenek           t=90–104  (14 sn)
  s4  Yol               t=104–120 (16 sn)
  s5  Dünya             t=120–136 (16 sn)
  son Teklif / finale   t=136–146 (10 sn)
Her perdenin SON 3 SANİYESİ "çıkış geçişi"dir (o perdenin satırlarına yazılır); sonraki perde bu görselle birebir devam eder. Satır başına tam 1 saniye: t, t+1 ... (kendi aralığın boyunca eksiksiz, ardışık). Sessiz/boş saniye yok: her saniyede ekranda değişen en az bir şey (kamera, ışık, nesne, çizgi, metin, sayaç, etkileşim ipucu) olsun.`

const GECIS = `GEÇİŞ SÖZLEŞMELERİ (iki taraf da buna uyar; değiştirmek istersen satırın "risk" alanına yaz):
  s0→s1: s0'ın son karesi akşam, pencereleri yanık ev, 3/4 ön cephe. Gökyüzü ve sokak beyaz stüdyoya erir, ev merkezde kalır, gerçek malzemeden röntgen/hayalet malzemeye döner. s1'in ilk karesi = stüdyoda hayalet ev, aynı kadraj.
  s1→s2: kamera ön cephedeki tek bloğa dalar, blok evden ayrılıp tek başına kalır, gerisi beyaza erir. s2'nin ilk karesi = beyaz fonda tek gazbeton blok, merkezde.
  s2→s3: kesilmiş/sertleşmiş blok yüzeyine yaklaşım; yüzey gözeneklerine makro dalış. s3'ün ilk karesi = blok yüzeyi makro, gözenekler.
  s3→s4: gözenekten geri çekilme → blok → paletteki bloklar → Söke fabrikası stok sahası sabah ışığı. s4'ün ilk karesi = streç filmli palet yığını, kamera geri çekilmeye devam eder.
  s4→s5: kamera tepeden yükselir: fabrika sahası → İzmir/Söke bölgesi tepeden → küre. s5'in ilk karesi = tepeden İzmir bölgesi (kıyı, körfez), küreye doğru geri çekilmeye başlar.
  s5→son: küre uzaklaşır, kıtalar ışıklı, arka plan koyu; logo ve slogan belirir. Logo YALNIZ son bölümde.`

const KURAL = `DEĞİŞMEZ KURALLAR: her sayının kaynağı kartta yazılı (Ürün föyleri / Ege Gazbeton ortak rakamlar / CE belgeleri / ODTÜ çalışması / ihracat bölümü; doğrulanamayan rakam "teyit gerekli" diye işaretlenir, uydurma rakam YOK); ihracat yalnız "25+ ülke · 5 kıta" (ülke adı, ülke sınırı, müşteri sayısı, fiyat YOK; Türkiye vurgusu yalnız gerçek Türkiye poligonu); A1 = "yangına tepki sınıfı" (asla "yanmaz"); YEŞİL (lime) = BİZİM: yalnız Ege Gazbeton ürünleri/ambalajı/şeridi (donatı, çelik, kayış, tuğla yeşil olamaz); yapay zekâ görseli YOK (her kare Blender'da kodla); 3B render içinde yazı/rakam YOK (etiket HTML/SVG, TR/EN); kanvas üstünde backdrop-filter/mix-blend YOK; DPR<=1,25; >=50 fps; file:// çevrimdışı çalışmalı; logo en sonda; yakın plan insan yüzü YOK; kare tabanlı oynatıcı (WebP dizisi + HTML/SVG/CSS/2B canvas efekti; WebGL yok, canlı gözenek katmanı yalnız son bölümde). Reels/kısa video sürümü İSTENMİYOR.`

const MEVCUT = `MEVCUT DURUM: önce ${REPO}/DEVIR.md oku (hikâye tablosu, dosya haritası, doğrulanmış bilgiler). Kod: ${REPO}/blender/*.py, ${REPO}/tools/*.py, ${REPO}/src/hikaye/*.js, ${REPO}/giris-hikaye/index.html. Geçici klasör ${SP} (önizleme/render kareleri; ör. ${SP}/onizle/ozet.jpg Perde 1 özeti; find ile ${SP}/render* altında s1/s4/s5 kareleri). Resimleri Read ile gör. Python/Blender: ${SP}/bl/bin/python. AĞIR RENDER YOK (arka planda tam render kuyruğu var; gerekirse EGE_PREVIEW=25 samples<=8 tek kare). Dosya düzenleme YOK; yalnızca ${PLAN}/ altına kendi çıktını yazarsın.`

const SATIR = `SATIR BİÇİMİ (JSON; her saniye bir nesne, Türkçe, kısa: alan başına en fazla ~25 kelime):
{ "t": <tam sayı sn>, "vh": <t*22>, "p": <perde içi ilerleme 0..1, 2 hane>, "kare": "<Blender kip + kare aralığı veya 2B/SVG/JS>", "gorsel": "<kamera, özne, hareket; ne görülüyor>", "efekt": "<ışık/atmosfer/parçacık/geçiş/gölgelendirici efekti; yoksa ''>", "metin_tr": "<ekranda beliren metin; yoksa ''>", "metin_en": "<İngilizcesi; yoksa ''>", "rakam": "<rakam + kaynak; yoksa ''>", "etkilesim": "<tıklanır nokta/mikro etkileşim/ipucu; yoksa ''>", "pazarlama": "<marka/güven/CTA rolü; yoksa ''>", "uretim": "<nasıl üretilir + yaklaşık maliyet (kare başı sn, efor)>", "mobil": "<dikey telefonda farkı; aynıysa ''>", "risk": "<kural/performans/üretim riski; yoksa ''>" }
Dosya biçimi: { "akt": "<id>", "t_bas": N, "t_son": N, "baslik": "...", "amac": "...(duygu ve mesaj)", "gecis_notu": "...", "satirlar": [ ... ], "yeni_isler": ["..."] (bu planın gerektirdiği yeni Blender/2B/web işleri, kısa), "acik_sorular": ["..."] (yalnız kullanıcının karar vermesi gereken en fazla 3 soru) }.
Dosyayı Write ile yaz, sonra "${SP}/bl/bin/python -c 'import json;d=json.load(open(...));print(len(d[\\"satirlar\\"]))'" ile geçerliliğini ve satır sayısını doğrula. Yanıt olarak yalnız kısa özet nesnesi döndür.`

const KALITE = `KALİTE ÇITASI: sinematik, etkileyici, ayrıntılı, öğretici ve pazarlamaya hizmet eden bir hikâye. Her saniyenin amacı olsun. Genel geçer klişe yazma: bu projenin gerçek ürünleri, gerçek sahneleri ve mevcut kodu üzerinden somut kamera/efekt/metin yaz. Ekran metni kısa ve vurucu olsun (okuma hızı: Türkçe en fazla ~3 kelime/sn; aynı anda ekranda en fazla 1 başlık + 1 cümle). Önceki oturumda kullanıcı şikâyetleri: tır ve araçlarda ayrıntı az, eskiz "yerden yükselmesin ÇİZİLSİN", kırmızı arabanın önü hatalı; detay/gerçekçilik/efekt/etkileşim/öğreticilik/pazarlama artırılsın.`

const ONERGE = (id, ad, bas, son, ozel, dosyalar) => `${MEVCUT}

GÖREV: "${ad}" perdesinin ${bas}–${son}. saniyelerini (${son - bas} satır) saniye saniye planla ve ${PLAN}/akt-${id}.json dosyasına yaz.
${ZAMAN}

${GECIS}

${KURAL}

${KALITE}

BU PERDEYE ÖZEL: ${ozel}
Önce oku: ${dosyalar}

${SATIR}`

const AKTLER = [
  { id: 's0', ad: 'Hayalden yuvaya (ana giriş)', bas: 0, son: 32,
    ozel: `Mevcut 162 karelik dizi: kıvılcım 8, plan çizimi 16, eğim 18 (bina kâğıttan zeminden YÜKSELİYOR; kullanıcı bunu istemiyor, eskiz ÇİZİLEREK belirmeli: kalem çizgisi bina köşelerinden/akslardan başlayıp yüzeyleri doldurmalı), dairesel silme, tel kafes+gazbeton dolumu 28, çapraz lime silme, sokak 36 (geçen araba, bisikletli, yayalar, Ege Gazbeton tırı lime streçli paletlerle = reklam), gün ilerleyişi, akşam pencereler tek tek yanar. İlk 3 saniye kanca olmalı; tır reklamı net okunmalı (ama 3B içinde yazı yok; sitede tırı takip eden etiket HTML). Yeni efekt fırsatları (ışık huzmesi, atmosfer, alan derinliği, hareket bulanıklığı, yaprak/kuş, ıslak asfalt, pencere ışığı, kıvılcım parçacıkları) için kare başı maliyet ver. Kullanıcı eskiz "çizim"inin gerçek çizim hissi vermesini istiyor.`,
    dosyalar: `${REPO}/blender/s0_hayal.py, ${REPO}/tools/s0_birlestir.py, ${REPO}/tools/cizim_gecis.py, ${REPO}/blender/sokak.py, ${REPO}/blender/insan.py; src/hikaye/dil.js h0.* anahtarları; index.html SAHNE 0 bölümü.` },
  { id: 's1', ad: 'Ürün turu (bu evi iyi yapan ne?)', bas: 32, son: 70,
    ozel: `Ev etrafında dönen kamera; 6 durak: duvar blokları, lento, U blok (çatı hatılı), gazbeton tutkalı, paneller, EGEPOR (kolon/kiriş kaplaması). Giriş 4 sn (s0'dan geçiş + soru), her ürün 5 sn, çıkış 4 sn (tek bloğa dalış). Her durakta: ürün gerçek malzemede + lime kenar parlaması, gerisi röntgen; ürünün NEREDE kullanıldığı ve NE KAZANDIRDIĞI (öğretici) görsel olarak anlatılsın (ısı akışı okları, açıklık ölçüsü, beton dolumu, derz çizgisi, hafiflik/ağırlık, kaplama). Ürün çeşitleri "spotlight". Kullanıcı: "ürünlerin özelliklerini tanıtan animasyonlar, evin etrafında dönebilir". Teyitli bilgiler DEVIR.md'de (Egepor, U blok; köşe bloğu yok). Her duraktaki rakam ve kaynağı yaz. Etkileşim: ürün çipleriyle durağa atlama, tıklanır noktalar.`,
    dosyalar: `${REPO}/blender/s1_urun.py, ${REPO}/giris-hikaye/index.html (SAHNE 1), ${REPO}/giris-hikaye/assets/css/hikaye.css (.eg-ozellik), src/hikaye/dil.js (h1*, NOKTALAR u_*); ${SP}/render/s1urund altında varsa kareler.` },
  { id: 's2', ad: 'Doğuş: hammaddeden bloğa', bas: 70, son: 90,
    ozel: `Tek blok beyaz fonda → hammaddelerine çözülür: kum, kireç, çimento, alçı, alüminyum tozu (beş hammadde, her birinin görevi) → karışım/kalıp → kabarma (hidrojen kabarcıkları) → tel kesim → otoklav (yüksek basınçlı buhar) → sertleşmiş blok. Gerçek üretim hissi için fabrikadan görüntüler (kalıp, tel kesme makinesi, otoklav) nasıl Blender'da inandırıcı kurulur? Etkileşim: hammadde noktaları ve kartlar (görevleri). Öğretici: neden gazbeton hafif/yalıtkan (kimya basit anlatım). Seam: s3'e (makro dalış) hazırlık.`,
    dosyalar: `${REPO}/blender/s1_dogus.py, ${REPO}/blender/stil_r2.py, ${REPO}/blender/stil_r4.py, src/hikaye/dil.js (i1.*, NOKTALAR), index.html SAHNE 2. Eski kareler için ${SP} altında find.` },
  { id: 's3', ad: 'Gözenek: ısıyı tutan hava', bas: 90, son: 104,
    ozel: `Makro gözenek dünyası: kapalı hava hücreleri; λ 0,08 (G2/350 duvar tasarım değeri) · A1 yangına tepki sınıfı (EN 13501-1) · 300–600 kg/m³ (G1–G4). Öğretici + etkileyici: ısı akışı çizgilerinin hücre ağında yavaşlaması, A1 alev testi (alev duvarın bir yüzünü yalar, diğer yüz serin; "yanmaz" DENMEZ), hafiflik (blok suda yüzer; kaynaklı mı kontrol et). Mevcut taslak sahneler: stil_r4.sahne_isi, stil_r5.sahne_alev/yuzer/derz/testere. Etkileşim: gözenek hücresine dokun (SVG). Seam: s4'e geri çekilme (gözenek→blok→palet→fabrika).`,
    dosyalar: `${REPO}/blender/s2_gozenek.py, ${REPO}/blender/stil_r4.py, ${REPO}/blender/stil_r5.py (sahne_alev, sahne_yuzer), src/hikaye/dil.js (i2.*), index.html SAHNE 3. Eski kareler için ${SP} altında find.` },
  { id: 's4', ad: 'Yol: fabrikadan sahaya', bas: 104, son: 120,
    ozel: `Söke fabrikası sabah ışığında: stok sahası (lime streçli paletler), forklift, yükleme, Ege Gazbeton tırı sahadan çıkar (reklam), kamera yandan izler sonra tepeye yükselir. Fabrika şu an beyaz maket kütleleri: daha gerçekçi cephe/malzeme/ekipman (otoklav, silo, konveyör, kireç tesisi, buhar, insan/forklift) ve taşıma grafiği (yük bağlama, streç, kayış, plaka) için somut Blender önerileri. Rakamlar: 2 fabrika (Söke & İzmir), 1.100.000 m³ kapasite, 200 t/gün kireç tesisi (kaynak: Ege Gazbeton ortak rakamlar). Etkileşim: tır etiketi, fabrika noktası. Seam: s5'e tepeden yükseliş.`,
    dosyalar: `${REPO}/blender/s4_yol.py, ${REPO}/blender/stil_r5.py (tir, tir_ayrinti, sahne_fabrika2), ${REPO}/blender/s0_hayal.py (ege_tiri), src/hikaye/dil.js (h4.*), index.html SAHNE 4.` },
  { id: 's5', ad: 'Dünya: Ege\'den 5 kıtaya', bas: 120, son: 136,
    ozel: `Tepeden İzmir → küre; Söke/İzmir'den 5 kıtaya yaylar, yay başında ilerleyen ışık damlası, varışta kıta ışır. KURAL: ülke adı/sınırı yok; Türkiye vurgusu yalnız gerçek Türkiye poligonu; "25+ ülke · 5 kıta" (kaynak: ihracat bölümü); limanlar Aliağa ve Alsancak yakınından (metinde var; doğrula). Grafiği "daha iyi" yap: atmosfer parıltısı, gece ışıkları, bulut katmanı, yay izi, kıta aydınlanması, sayaç (25+) animasyonu, kıta etiketleri (kıta adı serbest mi? "teyit" olarak işaretle). Seam: s5→son (küre uzaklaşır, logo).`,
    dosyalar: `${REPO}/blender/s4_dunya.py, ${REPO}/tools/kure_noktalari.mjs, src/hikaye/dil.js (i4.*), index.html SAHNE 5.` },
  { id: 'son', ad: 'Finale: teklif, logo, slogan', bas: 136, son: 146,
    ozel: `Hikâyenin kapanışı ve dönüşüm: koyu küre/gece → logo (YALNIZ burada) + "Bugünden Yarına Güvenle" + teklif çağrısı. Canlı gözenek katmanı (three.js, src/canli) bu bölümde. 10 saniye: duygusal kapanış + net CTA (Teklif Al, Ürün Kataloğu PDF, Teknik Özellikler) + kitle yolları (yapı sahibi / mimar-mühendis / ihracat alıcısı-bayi) + hikâyede izlenen ürüne göre teklif bağlantısına bağlam (ör. /teklif/?urun=...&kaynak=hikaye). Güven işaretleri: CE belgeleri vb. (yalnız doğrulanmış). Hikâyeden sonraki "Ürün grupları" bölümüne yumuşak geçiş.`,
    dosyalar: `${REPO}/giris-hikaye/index.html (eg-son, eg-sonrasi), ${REPO}/src/canli/*.js, ${REPO}/src/hikaye/arayuz.js (kitle, analitik), dil.js (son.*, kitle.*, cta.*).` },
]

const MODUL = `${MEVCUT}

GÖREV: Hikâye boyunca eklenecek ETKİLEŞİMLİ + ÖĞRETİCİ modül kataloğunu tasarla ve ${PLAN}/moduller.json dosyasına yaz. Sayfada render gerektirmeyen (HTML/SVG/CSS/2B canvas/JS; çevrimdışı; >=50 fps) 10–14 modül öner. Fikir havuzu (kendi fikirlerinle genişlet/ele): ürün seçici ("nerede kullanıyorsun?"), duvar hesaplayıcı (alan→blok adedi; 60x25 cm blok), ağırlık karşılaştırması (yoğunluk 300–600 kg/m³ ve kalınlıktan hesap), ısı yolculuğu kaydırıcısı (λ'dan U değeri; yalnız doğrulanmış λ), A1 yangın demosu, hücre dokun (gözenek), kesit gezgini (blok kesiti, U blok donatısı, Egepor kolon kaplaması), üretim zinciri zaman çizelgesi, "bu evde kaç blok var" (maket modelinden hesap; kaynak="maket modeli"), mini bilgi yarışması (3 soru), ihracat kıtaları, tır takibi etiketi, karşılaştırmalı "önce/sonra" kaydırıcı. Her modül: {"id","ad","nerede": "<film saniyesi aralığı ve perde>","ne_yapar","ogretici_deger","pazarlama_degeri","veri_ve_kaynak": "<kullanılan sayılar ve kaynakları; doğrulanamayan 'teyit gerekli'>","teknik": "<HTML/SVG/JS; fps ve bellek notu; çevrimdışı>","tr_metin","en_metin","dataLayer_olayi","efor": "kucuk|orta|buyuk","kural_riski"}. Dosya biçimi: {"moduller":[...], "oncelik_sirasi":["id",...], "acik_sorular":[...]} . Mevcut arayüz: src/hikaye/arayuz.js, main.js, ayarlar.js, index.html, hikaye.css (.eg-ozellik SVG animasyonları). Rakam uydurma: yalnız DEVIR.md ve dil.js'teki doğrulanmış rakamlar + bu verilerden hesap.
${KURAL}
${KALITE}
Dosyayı yazdıktan sonra json geçerliliğini doğrula; yanıt olarak kısa özet nesnesi döndür.`

const PAZ = `${MEVCUT}

GÖREV: Hikâyenin PAZARLAMA ve DÖNÜŞÜM akışını tasarla ve ${PLAN}/pazarlama.json dosyasına yaz. Ege Gazbeton (üretici, B2B/B2C karışık: yapı sahibi, mimar/mühendis, müteahhit, bayi, ihracat alıcısı) için: (1) duygu→kanıt→güç→eylem hunisi ve her aşamanın film saniyesi aralığı, (2) kitle yolları (yapı sahibi / mimar-mühendis / bayi-ihracat) ve her biri için hikâye içi CTA yerleşimi ve dili, (3) CTA yerleşim zaman çizelgesi (ilk CTA ne zaman görünür, hangi saniyede hangi bağlantı: /teklif/, /katalog/ PDF, /teknik-foyler/, /duvar-tasarla/, /ihracat/), bağlam taşıyan bağlantı şeması (?urun=&kaynak=hikaye&dil=), (4) güven işaretleri ve doğrulanmış kanıtlar (CE belgeleri, ODTÜ çalışması vb.; yalnız DEVIR.md/dil.js'teki doğrulanmış olanlar; eksikleri "teyit gerekli"), (5) ölçüm planı (dataLayer olay adları: hangi saniyede/sahnede ne ölçülür; ayrıntı: izleme/çerez eklemeyen mevcut yapıya uygun), (6) tır/araç reklamı ve marka görünürlüğü (lime kuralı), (7) SEO ve paylaşım (title/description/OG görseli için hangi kare; hikâyeyi atla bağlantısı), (8) mobil dönüşüm detayları, (9) 10 saniyelik ilk izlenim testi: ilk 10 sn'de ne görülür ve kullanıcı ne hisseder. Dosya: {"huni":[...], "kitle_yollari":[...], "cta_zaman_cizelgesi":[{"t":..,"yer":..,"metin_tr":..,"metin_en":..,"baglanti":..}], "baglanti_semasi":"...", "guven_isaretleri":[...], "olcum":[...], "marka_gorunurlugu":[...], "seo_paylasim":[...], "mobil":[...], "ilk_10_sn":"...", "acik_sorular":[...]}.
${ZAMAN}
${KURAL}
${KALITE}
Dosyayı yazdıktan sonra json geçerliliğini doğrula; yanıt olarak kısa özet nesnesi döndür.`

const OZET = {
  type: 'object',
  properties: {
    dosya: { type: 'string' },
    satir_sayisi: { type: 'number' },
    ozet: { type: 'string', description: 'Plan özeti, en fazla 4 cümle' },
    acik_sorular: { type: 'array', items: { type: 'string' } },
  },
  required: ['dosya', 'ozet'],
}

phase('Taslak')
const isler = [
  ...AKTLER.map(a => () => agent(ONERGE(a.id, a.ad, a.bas, a.son, a.ozel, a.dosyalar), { label: 'plan:' + a.id, phase: 'Taslak', schema: OZET })),
  () => agent(MODUL, { label: 'plan:moduller', phase: 'Taslak', schema: OZET }),
  () => agent(PAZ, { label: 'plan:pazarlama', phase: 'Taslak', schema: OZET }),
]
const taslak = await parallel(isler)
const adlar = [...AKTLER.map(a => a.id), 'moduller', 'pazarlama']
const ozetler = {}
adlar.forEach((k, i) => { ozetler[k] = taslak[i] })
log('Taslak tamam: ' + adlar.filter(k => ozetler[k]).join(', ') + (adlar.filter(k => !ozetler[k]).length ? ' | EKSİK: ' + adlar.filter(k => !ozetler[k]).join(', ') : ''))

phase('Denetim')
const DENETIM = {
  type: 'object',
  properties: {
    genel: { type: 'string' },
    sorunlar: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          akt: { type: 'string', description: 's0|s1|s2|s3|s4|s5|son|moduller|pazarlama|genel' },
          onem: { type: 'string', enum: ['blocker', 'high', 'medium', 'low'] },
          sorun: { type: 'string' },
          duzeltme: { type: 'string' },
        },
        required: ['akt', 'onem', 'sorun', 'duzeltme'],
      },
    },
    render_maliyeti: {
      type: 'object',
      properties: {
        toplam_yeni_kare: { type: 'number' },
        tahmini_saat_4cekirdek: { type: 'number' },
        not: { type: 'string' },
      },
      required: ['not'],
    },
  },
  required: ['genel', 'sorunlar'],
}
const denetim = await agent(`${MEVCUT}

GÖREV: ${PLAN}/ altındaki akt-s0.json ... akt-son.json, moduller.json, pazarlama.json dosyalarını (yazılabildiyse) OKU ve bağımsız bir yapım yönetmeni/denetçi olarak şunları denetle:
1) Her akt dosyası geçerli JSON mu, satırlar t_bas..t_son-1 arası eksiksiz ve ardışık mı, vh=t*22 mi, hiç boş/yinelenen saniye var mı?
2) Geçişler: her perdenin son 3 saniyesi ile sonraki perdenin ilk saniyesi sözleşmeye (aşağıda) ve birbirine görsel olarak uyuyor mu?
3) Kural ihlali: "yanmaz", ülke adı/sınırı, fiyat/müşteri sayısı, kaynaksız rakam, lime'ın bizim olmayan nesnede kullanımı, 3B içinde yazı, logo sonda dışı, yapay zekâ görseli, kanvas üstü backdrop-filter/mix-blend, WebGL, Reels.
4) Okuma süresi: ekran metni yoğunluğu (aynı anda >1 başlık+1 cümle? 3 kelime/sn aşımı?).
5) Etkileşim modüllerinin zaman çizelgesindeki yerleri akt dosyalarındaki "etkilesim" alanlarıyla ve pazarlama CTA çizelgesiyle tutarlı mı?
6) Üretim gerçekçiliği: yeni kare sayısı ve tahmini render süresi (4 çekirdek CPU; Cycles; log: ${SP}/render/s*.log'dan kare başı saniye al), disk (PNG/WebP), oynatıcı bellek (sahne başına kare), vh toplamı (146 sn x 22 = 3212 vh) kullanıcı için makul mü?
7) Sahneler arası tekrar/zayıf anlar: hikâyenin tempo eğrisi (duygu→kanıt→güç→eylem) ve etkileyicilik; gereksiz uzun/sıkıcı bölümler.
Sorunları önem sırasıyla, hangi dosyada ne düzeltileceğiyle yaz. Dosya düzenleme YOK.
${ZAMAN}
${GECIS}
${KURAL}`, { label: 'denetim', phase: 'Denetim', schema: DENETIM })

phase('Düzeltme')
const sert = (denetim && denetim.sorunlar || []).filter(s => s.onem === 'blocker' || s.onem === 'high')
const duzeltilen = []
const kume = {}
for (const s of sert) (kume[s.akt] = kume[s.akt] || []).push(s)
const dzl = await parallel(Object.keys(kume).filter(k => adlar.includes(k)).map(k => () =>
  agent(`${MEVCUT}

GÖREV: ${PLAN}/${k === 'moduller' || k === 'pazarlama' ? k : 'akt-' + k}.json dosyasını OKU ve denetimde bulunan şu sorunları gider (dosyayı yerinde güncelle; geçerli JSON ve satır bütünlüğü korunur; yalnız gereken satırları değiştir):
${kume[k].map((s, i) => `${i + 1}. [${s.onem}] ${s.sorun}\n   Düzeltme: ${s.duzeltme}`).join('\n')}

${ZAMAN}
${GECIS}
${KURAL}
Bittiğinde json geçerliliğini doğrula; yanıt olarak neyi değiştirdiğini kısaca özetle.`, { label: 'duzelt:' + k, phase: 'Düzeltme', schema: OZET }).then(r => ({ akt: k, r }))))
for (const x of dzl.filter(Boolean)) duzeltilen.push(x)

return { ozetler, denetim, duzeltilen: duzeltilen.map(x => ({ akt: x.akt, ozet: x.r && x.r.ozet })), dosya_dizini: PLAN }
