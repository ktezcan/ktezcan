export const meta = {
  name: 'ege-blender-sahneleri-uygula',
  description: 'Onaylanan saniye-saniye planı Blender sahnelerine uygula (s0–s5), bağımsız doğrula, hazır olanın render spec dosyasını yaz (kuyruk otomatik alır)',
  phases: [
    { title: 'Uygula', detail: 'sahne betiklerini plana göre yaz/düzelt, önizleme ile dene' },
    { title: 'Doğrula', detail: 'bağımsız denetçi: altın kareler, kurallar, geçiş sözleşmesi, spec; geçerse spec yayımlanır' },
    { title: 'Düzelt', detail: 'denetimin bulduğu sorunları gider, spec yayımla' },
  ],
}

const SP = '/tmp/claude-0/-home-user-ktezcan/c8c14d5b-13a3-504d-8378-fcae1d923068/scratchpad'
const REPO = '/home/user/ktezcan'
const PY = SP + '/bl/bin/python'
const TASLAK = SP + '/spec_taslak'

const BAGLAM = `PROJE: Ege Gazbeton giriş sayfası (maket) için kaydırmaya bağlı sinematik hikâye; kareler Blender 5.0.1 Cycles (CPU, 4 çekirdek) ile önceden hesaplanır, sayfa kare oynatır + HTML/SVG etiket gösterir. TESLİM BİR VİDEO DEĞİL: çift tıkla açılan sayfa maketi + kareler (zip) + kod. Önce ${REPO}/DEVIR.md oku.
KULLANICI PLANI ONAYLADI; kararlar: süre 146 sn kalsın; slogan "Bugünden Yarına Güvenle" yalnız finalde; tır kabininde LOGO YOK (lime şerit + sitede HTML etiket); A1 alev/"serin yüz" sahnesi YOK (yalnız "A1 · yangına tepki sınıfı · EN 13501-1 · CE belgeleri" kartı + nötr tezgâh); "suda yüzer" YOK; "25+ ülke · 5 kıta" güncel; Türkiye poligonu LİME olabilir (marka vurgusu olarak onaylandı); Aliağa/Alsancak limanı ifadesi kaynaksız → kullanma; kaydırma kilidi yok; fabrika temsilî (gerçek fotoğraf yok).
KURALLAR: her sayının kaynağı kartta (render içinde YAZI/RAKAM YOK; etiketler HTML/SVG); ihracatta ülke adı/sınırı yok; A1 = "yangına tepki sınıfı" (asla "yanmaz"); YEŞİL (lime) = BİZİM: yalnız Ege Gazbeton ürünü/ambalajı/şeridi (donatı, çelik, kayış, tuğla lime OLAMAZ); yapay zekâ görseli yok (her şey Blender'da kodla); yakın plan insan yüzü yok (insanlar orta/uzak plan, yüzsüz silüet/arkadan); kanvas üstünde backdrop-filter/mix-blend yok.
ÇALIŞMA ORTAMI: Blender python: ${PY}  ; ortam: export EGE_TEX=${SP}/tex EGE_MH=${SP}/mh ; betikler ${REPO}/blender/ altında, ortak kit blender/kit.py. Önizleme: EGE_PREVIEW=25 (çözünürlük %25) samples<=8; altın kare için EGE_PREVIEW=50 samples<=16, en fazla 6 kare. AYNI ANDA YALNIZ 1 Blender süreci, "nice -n 10" ile çalıştır (makine 4 çekirdek ve arka planda tam render kuyruğu da çalışacak). Resimleri Read aracıyla gör; çoklu kare için ${SP}/kontak.py <çıkış.jpg> <png...> kontak sayfası.
GIT: commit/push YAPMA (ben yaparım). Yalnız SAHİP olduğun dosyalara yaz; başka dosyayı okuyabilirsin ama değiştirme.
ZAMAN: hedef ≤ 90 dakika. Mükemmeliyetçilik yerine çalışan, kurallara uyan, planın ruhunu taşıyan sürüm; yetişmeyen/yan iyileştirmeleri ${REPO}/docs/uretim/<id>-kalan.md dosyasına yaz (kısa maddeler). Plan çok büyükse önceliği: (1) kullanıcı şikâyetleri ve planın kanca/etki anları, (2) geçiş sözleşmeleri, (3) ayrıntı/efekt.
KARE SÖZLEŞMESİ: kareler ${'{root}'}/<sahne><v>/NNN.png (v = d|m; d 1600x900, m 768x1366) + meta.json (betikler zaten yazar). Geçiş karesi sahibi = SONRAKİ perde: s1[151]←s2[000], s3[084]←s4[000], s4[095]←s5[000] paketlemede KOPYALANIR; önceki perde bu kareyi render ETMEZ (spec'e "kopya" yaz, aşağıda). Sahne betiğinin kare sayısı sabiti (FRAMES) plandaki TOPLAM kare sayısı olsun (u = f/(FRAMES-1)); spec'teki "frames" ise render edilecek kare sayısıdır (kopya kareler hariç).
SPEC (en SON adım): ${TASLAK}/<id>.json (taslak). Biçim ve örnek için ${REPO}/tools/render_kuyruk.py başındaki docstring'i oku. Alanlar: {"id","jobs":[{"script","args","out":"{root}/<sahne>{v}","png_dir","frames" | "frame_list","variants","env"}],"post":{...} (isteğe bağlı),"kopya":[{"hedef":"{root}/s1{v}/151.png","kaynak":"{root}/s2{v}/000.png"}] (isteğe bağlı)}. Betik argümanları: --variant d|m --out DIR --frames a,b,c --skip-existing --samples N (betiğin kendi varsayılanı kare başına ≈ ≤ 90 sn (d) hedefle ayarlanmalı; örnek sayısı spec args içinde "--samples" ile verilebilir). Spec yazmadan önce: python3 ${REPO}/tools/render_kuyruk.py --root /tmp/kt_<id> --python ${PY} --spec-dir ${TASLAK} --dry-run ile komutu dene (spec dizinindeki tüm taslakları okur; yalnız kendininkine bak).`

const ONAYLI = (id) => `Plan: ${REPO}/docs/plan/akt-${id}.json (TAM oku: her saniye satırının gorsel/efekt/uretim alanları, gecis_notu, yeni_isler) ve ilgili denetim sorunları ${REPO}/docs/plan/denetim.json (akt=${id} ve genel). Bitişik perdelerin planları geçiş sözleşmesi için okunabilir.`

const SAHNELER = [
  { id: 's0', ad: 'Perde 1 · Hayalden yuvaya (ana giriş)',
    dosya: `blender/s0_hayal.py, blender/sokak.py, blender/insan.py, blender/stil_r5.py (YALNIZ tir/tekerlek/tir_ayrinti/strec_m = tır kısmı), tools/s0_birlestir.py, tools/cizim_gecis.py, yeni blender/s0_*.py`,
    ozel: `ÖNCELİKLİ KULLANICI ŞİKÂYETLERİ: (1) Eskiz zeminden YÜKSELMEZ, ÇİZİLİR: kalem çizgisi akslardan/kolonlardan başlayıp bina kenarlarını ve yüzeyleri çizerek doldurur (plandaki tasarımı uygula; Freestyle çizgilerini zaman haritasıyla kademeli göstermek / çizgi geometrisini kademeli çizdirmek / 2B draw-on'dan en iyisini seç; hiçbir şey scale.z ile büyümesin). (2) Park halindeki KIRMIZI arabanın önü hatalı: commit 75fdab2'deki sokak.py araba() düzenlemesi (cam atama, far/stop/sinyal vb.) görsel olarak doğrulanmadı; sokak karelerinde yakın kırpmayla kontrol et, gerekirse düzelt. (3) Tır ve diğer öğelerde ayrıntı az: stil_r5.tir_ayrinti (WIP) görsel doğrula ve plan/ürünler gerekirse ayrıntı ekle (kabin silueti kare kutu görünmesin, jantlar, perde/kayış, lime streçli paletler net okunsun; logo YOK). (4) bisikletli, yayalar, lamba, ağaç ayrıntısı; gerçekçilik/etkileyici efekt (planın efekt alanları). ÇIKTI: kaynak kip kareleri ${'{root}'}/s0src/{v}/<kip>/NNN.png (kip sayıları plana göre; plaka gündüz 0-5 / akşam 6 / 7 AYRI koşular → spec'te ayrı iş + frame_list) ve tools/s0_birlestir.py ile nihai ${'{root}'}/s0{v}/NNN.png (d: plandaki 256 kare; m: yalnız çift kareler + son). Birleştirici seyrek kaynakla (eksik kareleri komşu kareler arası erime) çalışmalı; son kare(ler) s1'in ilk karesine birebir geçer (s1 f000 = ${'{root}'}/s1{v}/000.png okunur; yoksa o kareler atlanır). Spec'te "post": {"cmd":["python","tools/s0_birlestir.py","{root}/s0src","{root}","{v}"],"after_passes":[1,3]} kullan. Kıvılcım/plan çizimi/silme gibi 2B aşamalar birleştiricide üretilir.`,
    kare: 'd: 256 nihai kare (kaynak Blender kareleri ≈167)' },
  { id: 's1', ad: 'Perde 2 · Ürün turu',
    dosya: `blender/s1_urun.py, yeni blender/urun_*.py`,
    ozel: `PLANIN YAKALADIĞI HATALAR (düzelt): donatıya lime uygulanıyor (lime yalnız Ege ürünü; donatı çelik gri/koyu); kamera başlangıç azimutu s0 C kamerasıyla ayna kaymış (s0: az +32°, 24 mm, 24 m, hedef (-0,5; -4; 4,6); s1 -32° ile başlıyor); panel modelde 8,8 m ama kartta 6 m (modeli 6 m'ye çek); 152 kare (u=(t-32)/38); durak zamanları plandaki saniyelerden; makro derz sahnesi (+8 kare); çıkış dalışı. RENDER HIZLANDIRMA (planın "uretim" notları, seri öncesi ön koşul): transparent_max_bounces 32→12, V≥0,995 ise V=1 yaz ve V≥0,98 nesneleri hide_render, samples/threshold ayarı; hedef: normal kare ≤ 100 sn (d), dalış kareleri ≤ 150 sn. Ghosting azaltma: hareketli yörünge saniyelerinde kare yoğunluğu planda varsa uygula. U blok ve Egepor bilgileri DEVIR.md'deki teyitli bilgilerle (ürün föyleri) tutarlı kalsın; render içinde yazı yok.`,
    kare: 'f0–f150 render (f151 = s2 f000 kopya), toplam 152' },
  { id: 's5', ad: 'Perde 6 · Dünya',
    dosya: `blender/s4_dunya.py, tools/kure_noktalari.mjs, yeni blender/dunya_*.py`,
    ozel: `PLANIN YAKALADIĞI HATALAR (düzelt): Amerika ve Okyanusya küre dönmediği için arka yüzde kalıyor (küre dönüşü planı: Avrupa→Afrika→Amerika→Asya→Okyanusya sırası uygulanabilir olmalı); Amerika hedef noktası (18°,-86°) denizde → karada bir noktaya taşı. Türkiye poligonu LİME serbest; yaylar/fabrika iğneleri lime. s4→s5 geçiş karesi (F000) tanımı: "beyaz-gri kara noktaları + iki lime halka (Söke, İzmir)"; Türkiye lime dalgası t=122'de. 193 kare (F0–F192; F192 = finale ilk karesi, metinsiz). Render maliyeti: eski sahne 72-79 sn/kare ölçüldü; nokta sayısını/bulut/atmosfer maliyetini kontrol ederek hedef ≤ 80 sn/kare (d). Ülke adı/sınırı yok; kıta adı etiketleri HTML (render dışı). "25+" sayaç animasyonu HTML'de (render'da rakam yok).`,
    kare: 'F0–F192 (193 kare)' },
  { id: 's4', ad: 'Perde 5 · Yol (fabrika + tır)',
    dosya: `blender/s4_yol.py, yeni blender/fabrika_*.py (stil_r5.sahne_fabrika2'yi DEĞİŞTİRME; gerekirse kopyalayıp fabrika_kit.py'de geliştir; tırı stil_r5.tir/s0_hayal.ege_tiri ile kullan — tır dosyaları s0 işine ait, değiştirme)`,
    ozel: `Plandaki fabrika/taşıma ayrıntıları: temsilî Söke tesisi (cephe malzemesi, silo, otoklav, konveyör, kireç tesisi, buhar, forklift ve palet, streç/kayış, kantar); sahne ilk karesi: lime streçli palet yığını makro (s3 sonundan geri çekilmeyle birebir devam: s4 F000 = s3 F84 paylaşılan kare, sahibi s4); tır çıkışı + yan takip + vinç yükselişi; son kare F095 = s5 F000 (s5 sahibi; sen F095'i render ETME → spec kopya: s4[095]←s5[000]). t=109 kayış sahnesinde insan yüzü/yakın plan yok (omuz altı veya kadraj dışı). 96 kare toplam (F0–F94 render). Altın kareler: F036–F041 (t=110 kahraman kare) özellikle detaylı olsun. Rakamlar render dışı.`,
    kare: 'F0–F94 render (F95 = s5 F000 kopya), toplam 96' },
  { id: 's2', ad: 'Perde 3 · Doğuş',
    dosya: `blender/s1_dogus.py (bu dosya Doğuş sahnesidir), yeni blender/uretim_*.py`,
    ozel: `Plan: blok beş hammaddeye çözülür (kum, kireç, çimento, alçı, alüminyum tozu; su 6. madde gibi okunmasın → su "musluk/ekleme" olarak), karışım, kalıp, kabarma (hidrojen kabarcıkları), tel kesim, otoklav (rakam YOK: sıcaklık/basınç kaynaksız), sertleşmiş blok; son 3 sn gözenek makro dalışı (s3 başlangıcı). İlk kare: beyaz fonda tek gazbeton blok (s1 dalışından devam; s2 F000 paylaşılan kare sahibi s2). 100 kare (F0–F99 hepsi render). Lime yalnız ürün/ambalaj. "Hacmin çoğu hava" gibi kaynaksız çoğunluk iddiası görselde/metinde olmasın (denetim). Kalıp/tel kesme makinesi/otoklav inandırıcı ama temsilî (Blender'da kodla).`,
    kare: 'F0–F99 (100 kare)' },
  { id: 's3', ad: 'Perde 4 · Gözenek',
    dosya: `blender/s2_gozenek.py (bu dosya Gözenek sahnesidir), yeni blender/gozenek_*.py`,
    ozel: `Plan + DENETİM DÜZELTMESİ: A1 alev/"serin yüz"/ısıl degrade YOK ve suda yüzme/tank/su YOK; t=97-98: nötr tezgâhta duvar parçaları + (kart/etiket HTML tarafında); t=99-100: tezgâhta yan yana G1/G2/G4 blok (G3 yok) durağan kareler. Isı akış çizgileri gerçek gözenek kesitinden hesaplanır (prototip: ${SP}/plan/_gz/ — isi_test3.png ve betikler; kullanabilirsin). Makro dalış girişi (s2 sonu), çıkış: gözenekten geri çekilme → blok → paletteki bloklar (s3 F84 = s4 F000, sahibi s4; sen F084'ü render ETME → spec kopya: s3[084]←s4[000]). 85 kare toplam (F0–F83 render). Rakam/etiket render içinde yok. "Isıyı tutan, içindeki hava" metni kalır; "Hacmin çoğu hava" yok.`,
    kare: 'F0–F83 render (F84 = s4 F000 kopya), toplam 85' },
]

const SONUC = {
  type: 'object',
  properties: {
    ozet: { type: 'string', description: 'Ne yapıldı, ne yapılamadı (en fazla 6 cümle)' },
    taslak_spec: { type: 'string' },
    kare_sayisi: { type: 'string' },
    kare_basi_sn_d: { type: 'string', description: 'Önizlemeden tam çözünürlük kare başı süre tahmini' },
    kalan: { type: 'array', items: { type: 'string' } },
  },
  required: ['ozet'],
}
const KARAR = {
  type: 'object',
  properties: {
    ok: { type: 'boolean' },
    ozet: { type: 'string' },
    sorunlar: { type: 'array', items: { type: 'object', properties: { onem: { type: 'string', enum: ['blocker', 'high', 'medium', 'low'] }, sorun: { type: 'string' }, duzeltme: { type: 'string' } }, required: ['onem', 'sorun'] } },
    spec_yayimlandi: { type: 'boolean' },
  },
  required: ['ok', 'ozet'],
}

const sonuc = await pipeline(
  SAHNELER,
  s => agent(`${BAGLAM}

GÖREV: "${s.ad}" sahnesinin Blender tarafını onaylanan plana göre UYGULA.
${ONAYLI(s.id)}
SAHİP OLDUĞUN DOSYALAR (yalnız bunlara yaz): ${s.dosya}
SAHNEYE ÖZEL: ${s.ozel}
KARE: ${s.kare}
ADIMLAR: 1) planı ve mevcut kodu oku; 2) uygula; 3) önizleme karelerini (başlangıç, bitiş, geçiş, 4-6 kilit an) üret ve kontak sayfasıyla gözle; sorunları düzelt; 4) kare başı süreyi ölç/tahmin et, kuyruğa uygun örnek sayısı seç; 5) ${TASLAK}/${s.id}.json taslak spec dosyasını yaz (mkdir -p); 6) kalan işleri docs/uretim/${s.id}-kalan.md dosyasına yaz. Yanıt olarak kısa özet nesnesi döndür.`,
    { label: 'uygula:' + s.id, phase: 'Uygula', schema: SONUC }),
  async (r, s) => {
    if (!r) return null
    const k = await agent(`${BAGLAM}

GÖREV: BAĞIMSIZ DENETÇİ olarak "${s.ad}" sahnesinin yapılan uygulamasını denetle; GEÇERSE spec'i yayımla.
${ONAYLI(s.id)}
Uygulayıcının özeti: ${r.ozet}
Taslak spec: ${TASLAK}/${s.id}.json ; sahip olunan dosyalar: ${s.dosya}. Değişiklikleri git diff ile gör (commit edilmemiş değişiklikler).
DENETİM: (a) altın kareler: kendin 5-6 kilit kareyi önizlemeyle (EGE_PREVIEW=25..50, samples<=8..16, nice) üret ve gör: plan satırlarındaki görsel/efekt var mı? kareler güzel/ayrıntılı/gerçekçi mi? bariz hata (kırık geometri, boş kadraj, yazı/rakam, lime yanlış nesnede, yakın plan yüz, A1/yanmaz çağrışımı) var mı? (b) geçiş sözleşmesi: ilk/son kare komşu perdeyle uyuyor mu (planın gecis_notu)? (c) spec geçerli mi: python3 ${REPO}/tools/render_kuyruk.py --root /tmp/kt_v_${s.id} --python ${PY} --spec-dir ${TASLAK} --dry-run; frames/frame_list/png_dir/out doğru mu, komutlar betiğe uyuyor mu, kare başı süre hedefi makul mü (tahmin ≤ ~100 sn d)? (d) beklenmedik: tek kareyle eksik kalan --frames/--skip-existing davranışı, meta.json yazımı. KARAR: blocker/high sorun YOKSA: spec'i ${REPO}/blender/spec/${s.id}.json olarak KOPYALA (mkdir -p; kuyruk bunu otomatik alıp render'a başlar) ve ok=true döndür. Blocker/high VARSA kopyalama; sorunları yaz, ok=false. Küçük (medium/low) sorunları kendin düzeltebilirsin ama yalnız sahip olunan dosyalarda ve kısaca.`,
      { label: 'dogrula:' + s.id, phase: 'Doğrula', schema: KARAR })
    return { sahne: s, uygula: r, karar: k }
  },
  async (x, s) => {
    if (!x) return null
    if (x.karar && x.karar.ok) return x
    const iss = x.karar ? (x.karar.sorunlar || []) : []
    const d = await agent(`${BAGLAM}

GÖREV: "${s.ad}" sahnesinin denetimde bulunan sorunlarını gider ve spec'i yayımla.
${ONAYLI(s.id)}
Sahip olunan dosyalar: ${s.dosya}.
DENETİM SONUCU: ${x.karar ? x.karar.ozet : '(denetim sonuç vermedi: sahneyi baştan doğrula)'}
SORUNLAR:
${iss.map((q, i) => `${i + 1}. [${q.onem}] ${q.sorun}${q.duzeltme ? '\n   Öneri: ' + q.duzeltme : ''}`).join('\n') || '(ayrıntı yok)'}
Düzelt, ilgili kilit kareleri önizlemeyle yeniden dene, sonra spec'i doğrula (dry-run) ve ${REPO}/blender/spec/${s.id}.json olarak yayımla (kuyruk otomatik alır). Hâlâ blocker kalıyorsa YAYIMLAMA ve nedenini yaz.`,
      { label: 'duzelt:' + s.id, phase: 'Düzelt', schema: KARAR })
    return { ...x, duzeltme: d }
  },
)

return { sonuc: sonuc.filter(Boolean).map(x => ({ id: x.sahne.id, uygula: x.uygula, karar: x.karar, duzeltme: x.duzeltme || null })) }
