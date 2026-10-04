export const meta = {
  name: 'ege-web-maketi-uygula',
  description: 'Onaylanan plana göre sayfa maketi: oynatıcı/motor, içerik+finale+pazarlama, etkileşimli modüller; entegrasyon testi ve düzeltme',
  phases: [
    { title: 'Uygula', detail: 'motor, içerik+finale, modüller (dosya sahipliği ayrık)' },
    { title: 'Entegrasyon', detail: 'derle, yer tutucu karelerle başsız tarayıcı sınaması, ekran görüntüleri, kural taraması' },
    { title: 'Düzelt', detail: 'entegrasyon bulgularını gider' },
  ],
}

const SP = '/tmp/claude-0/-home-user-ktezcan/c8c14d5b-13a3-504d-8378-fcae1d923068/scratchpad'
const REPO = '/home/user/ktezcan'
const PY = SP + '/bl/bin/python'
const NM = SP + '/tools/node_modules'

const BAGLAM = `PROJE: Ege Gazbeton (egegazbeton.com.tr) giriş sayfası MAKETİ. Teslim bir video DEĞİL: çift tıkla (file://) açılan, kaydırmaya bağlı sinematik hikâye sayfası + kareler (WebP dizileri; Blender'da önceden hesaplanır, sayfa yalnız kare oynatır + HTML/SVG/2B canvas etiket/efekt gösterir) + kod. TR+EN. Masaüstü (1600x900) ve dikey telefon (768x1366). Önce ${REPO}/DEVIR.md ve ${REPO}/docs/HIKAYE_OZET.md oku; ayrıntılı plan: ${REPO}/docs/plan/akt-s0..akt-son.json (her saniyenin metin_tr/metin_en/rakam/etkilesim/pazarlama alanları), moduller.json (modül kataloğu), pazarlama.json (CTA, kitle yolları, ölçüm), denetim.json (denetçinin bulduğu sorunlar: bunlara uy).
KULLANICI PLANI ONAYLADI; kararlar: süre 146 sn kalsın (1 film sn = 22 vh; sahne boyları vh: s0 704, s1 836, s2 440, s3 308, s4 352, s5 352, finale 220); slogan "Bugünden Yarına Güvenle" YALNIZ finalde (açılış başlığı "Her yuva bir çizgiyle başlar."); tır kabininde logo yok; A1 alev/"serin yüz" ve "suda yüzer" yok (A1 yalnız "yangına tepki sınıfı · EN 13501-1 · CE belgeleri" kartı); "25+ ülke · 5 kıta" güncel; Türkiye lime olabilir; Aliağa/Alsancak limanı ifadesi kaynaksız → metinlerden ÇIKAR; "Hacmin çoğu hava" gibi kaynaksız çoğunluk iddiası yok; kaydırma kilidi YOK (modül panelleri kilitsiz, kaydırınca kapanır/küçülür); tarayıcı depolaması (localStorage/sessionStorage/çerez) KULLANMA (bağlam yalnız bellekte ve bağlantı parametresiyle); gerçek logo yok → yer tutucu logo kalır (LP\\img\\logo_white.svg ile değiştirilecek notu).
KURALLAR: her sayının kaynağı kartta yazılı (Ürün föyleri / Ege Gazbeton ortak rakamlar / CE belgeleri / ODTÜ çalışması / ihracat bölümü); doğrulanamayan rakam ekranda YOK; ihracatta ülke adı/sınırı/müşteri sayısı/fiyat yok; A1 = "yangına tepki sınıfı" (asla "yanmaz"); YEŞİL (lime) = BİZİM (yalnız Ege ürünü/ambalajı/şeridi/marka vurgusu); kanvas üstünde backdrop-filter / mix-blend YOK; DPR ≤ 1,25; ≥ 50 fps; file:// çevrimdışı çalışmalı (harici istek yok); logo en sonda; WebGL yalnız finaldeki canlı gözenek katmanında (src/canli) ve orada da DPR ≤ 1,25; erişilebilirlik (prefers-reduced-motion, klavye, aria); TR/EN anahtarı (dil.js).
ARAÇLAR: derleme: node ${REPO}/tools/derle.mjs ${NM} (src/hikaye → giris-hikaye/assets/js/hikaye.js); karelere dönüştürme: ${PY} ${REPO}/tools/kareler.py <render_kök> 90; başsız tarayıcı sınaması: node ${REPO}/tools/sinama.mjs <çıktı> [file] (Playwright; Chromium /opt/pw-browsers; "playwright install" ÇALIŞTIRMA). YER TUTUCU KARELER (gerçek render henüz yok): ${PY} ${REPO}/tools/kare_taklit.py <kök> [--kucuk] [--adim N] → <kök>/s0d..s5m (plandaki kare sayılarıyla; --adim 8 seyrek set); sonra kareler.py bu kökten giris-hikaye/kareler'e dönüştürür. Gerçek render'lar ilerledikçe ${SP}/render3'e düşecek ama onu KULLANMA/SİLME (kuyruk yazıyor). Arka planda Blender render kuyruğu CPU'yu kullanıyor: ağır testlerde "nice -n 10", aynı anda tek Chromium.
GIT: commit/push YAPMA (ben yaparım). YALNIZ SAHİP olduğun dosyalara yaz; başkasının dosyasını okuyabilirsin. Üç agent paralel çalışıyor; çakışmamak için sahiplik kesin.
ARAYÜZ SÖZLEŞMELERİ (kayıt noktaları zaten var): src/hikaye/moduller/index.js → export function modullerKur({ sahneler, ortak, ui }) (main.js çağırıyor; modül agent'ı doldurur); src/hikaye/final.js → export function finalKur(ortak) → { konumla(p), ciz(ctx, w, h, p) } (finale 2B kanvas efektleri; içerik agent'ı doldurur, motor agent'ı çağırır: finale segmenti akışın 7. parçası, boyu 220 vh, ana kanvasta s5'in SON karesini (F192) çizmeye devam ederken ciz() 2B efektini üstüne çizer).
ZAMAN: hedef ≤ 90-120 dakika. Çalışan, kurallara uyan, plana sadık sürüm; yetişmeyenleri ${REPO}/docs/uretim/<ad>-kalan.md dosyasına kısa maddelerle yaz. Her şey Türkçe (kod yorumları dahil) ve mevcut kodun üslubuyla (yorum yoğunluğu, adlandırma) uyumlu olsun.`

const IS = [
  { id: 'motor', ad: 'Oynatıcı/motor + paketleme',
    dosya: `src/hikaye/main.js, src/hikaye/sahne.js, src/hikaye/ayarlar.js, src/hikaye/homografi.js, tools/kareler.py, tools/derle.mjs, tools/sinama.mjs, tools/paketle.sh, yeni tools/teslim.sh, giris-hikaye/OKU-BENI.txt`,
    gorev: `1) ayarlar.js: SAHNELER boyları plana göre (s0 704, s1 836, s2 440, s3 308, s4 352, s5 352) + finale segmenti (220 vh, ayrı tür: finalKur ile). Eşleşen-kare dikişlerinde (son kare = sonraki ilk kare; paketlemede kopyalanır) GECIS=0: dagit() dikiş bölgesini kaldırsın, sınırda kare seti anında (kayıpsız) değişsin; toplam ≈ 3212 vh ≈ vh=t*22 ile plan saniyelerine birebir otursun (ortak.saniyeyeGit(t) yardımcısı ekle: pazarlama/modüller saniye→kaydırma için kullanacak). 2) BELLEK (denetim, high): yukle()/ensure() etkin sahne+komşunun TÜM karelerini çözüp tutuyor (en kötü ≈ 2,9 GB). Pencereli yükleme yap: etkin sahnede ±16 kare createImageBitmap ile çözülmüş tutulur, pencere dışı bitmap.close(); komşu sahneler için yalnız anahtar kareler (her 8.) ve ilk kareler; sayfa açılışında yalnız s0'ın ilk 24 karesi + her 8. kare önce (hızlı ilk boyama); s1 yüklemesi s0 p>0,6 sonrasına ertelensin. Seyrek kare setinde (kareler eksikse; pass-major render sırasında paket seyrek olabilir) ara kare erimesi çalışmaya devam etsin; hızlı kaydırmada hayalet için hareket yönünde kısa erime. 3) kanvas DPR ≤ 1,25 (tüm kanvaslar). 4) tools/kareler.py: WebP boyut/kalite bütçesi (s5 için q≈70/method 6, toplam hedef ≤ 100 MB), kareler-meta.js kare sayıları ve MEVCUT kare indeksleri, bütçe raporu; seyrek set desteği; poster.webp her sahne için. 5) tools/sinama.mjs: bellek ölçümü (performance.memory veya CDP), hızlı sarma fps testi, yeni akış (7 parça) ekran görüntüleri, DPR ve backdrop-filter taraması, konsol hatası; file:// modu. 6) tools/teslim.sh <render_kök> <node_modules> <çıktı_klasörü> [python]: ÇIKTI İKİ ZİP: (a) Ege-Gazbeton-giris-maket_<tarih>.zip = giris-hikaye/ (kareler + js + css + yazı tipleri + OKU-BENI.txt: çift tıkla index.html, Natro'ya yükleme için zip'i sunucuda aç notu) ve (b) Ege-Gazbeton-kaynak_<tarih>.zip = depo kaynağı (git archive HEAD veya dosya listesi; DEVIR.md, docs, blender, tools, src; MakeHuman verisi/tex/WebP kareler HARİÇ). Ayrıca seam kopyalarını yapan tools/dikis_kopyala.py <render_kök> (blender/spec/*.json içindeki "kopya" girdilerini okuyup PNG'leri kopyalar; hedef zaten varsa üzerine yazar; kaynak yoksa atlar) yaz ve teslim.sh bunu kareler.py'den ÖNCE çağırsın. 7) Test: yer tutucu karelerle (tam ve --adim 8 seyrek) derle + sinama; konsol hatası yok, fps ≥ 50.` },
  { id: 'icerik', ad: 'İçerik + finale + pazarlama',
    dosya: `giris-hikaye/index.html, giris-hikaye/assets/css/hikaye.css, src/hikaye/dil.js, src/hikaye/arayuz.js, src/hikaye/final.js, src/canli/*.js (+ derle.mjs'in canli kısmı gerekiyorsa DEĞİL: tools/derle.mjs motor agent'ının; canli derlemesi için yalnız komutu çalıştır)`,
    gorev: `1) index.html: 7 parçalı akış (s0..s5 + finale) ve vuruşlar (data-bas/data-son = plan satırlarındaki t'den perde içi ilerleme p; ardışık saniyelerdeki metinleri tek vuruşa birleştir; her vuruşta en fazla 1 başlık + 1 cümle; okuma hızı ≤ 3 kelime/sn). Tüm TR metinler plan satırlarından (metin_tr), EN dil.js'te (metin_en); data-i18n anahtarları. Denetim düzeltmeleri geçerli (s0 açılış başlığı "Her yuva bir çizgiyle başlar.", slogan yalnız finalde; 4 kez tekrar eden "Peki..." kalıbını plan/denetimin önerdiği biçimde azalt; kicker numaraları; EN'de lime=kireç çift anlamı: 'Quicklime'/'Lime (binder)', streç için 'lime-green stretch film'). Aliağa/Alsancak ifadesi dil.js ve index.html'den ÇIKAR. 2) NOKTALAR (tıklanır noktalar + kartlar, TR/EN, kaynaklı) plandaki etkilesim alanlarına göre; sahneye bağlı data-sahne ve etiket meta anahtarları s0_birlestir.py/blender çıktısıyla (hotspots anahtarları: giris, bahce, sokak, eskiz, blok, lento, panel, derz, tir, yuva ve plandaki yeni olanlar; render tarafı yeni çapa adlarını plan 'etkilesim'/'kare' alanlarında belirtiyor: meta.json'daki adları EXACT kullan; belirsizse NOKTALAR'a ekle, kareler gelince eşleşir). 3) FİNALE (akt-son.json, denetim düzeltmeleriyle): finale.js içinde 2B kanvas efektleri (s5 son karesi üzerinde küre → Ege'de tek kıvılcım → logo köşe çizgileri), logo YALNIZ burada, slogan, tek ana CTA + tek ikincil CTA (t=142), kitle çipleri (t=143), 3 kanıt kartı (t=144; yalnız doğrulanmış kanıtlar), 'Hikâyeyi baştan izle'; canlı gözenek katmanı (src/canli) yaşam döngüsü: WebGL bağlamı yalnız finale etkinken ve idle'da, DPR ≤ 1,25 (TIERS dprMax), ilk render t≥138; bundle'ı derle (node tools/derle.mjs ${NM}). 4) Pazarlama/CTA (pazarlama.json): kitle yolları, CTA zaman çizelgesi, bağlantı şeması (?kaynak=hikaye&dil=&urun=&nokta=; urun bağlamı yalnız bellekte), dataLayer olayları (mevcut data-iz altyapısı; çerez/depolama YOK), 'Hikâyeyi atla', üst çubuk 'Teklif Al', yolculuk çubuğu 7 öğe, mobil CTA düzeni. 5) SEO/paylaşım: title/description/og meta (görsel dosya adı yer tutucu), lang. 6) hikaye.css: vuruş/rakam kartı/CTA bileşenleri, finale; prefers-reduced-motion yedeği; telefon düzeni (anlatım üstte). backdrop-filter/mix-blend kanvas üstünde YOK. 7) Test: yer tutucu karelerle derle + sinama (motor agent'ının kareler/derle araçlarını kullan, onların dosyalarını DEĞİŞTİRME).` },
  { id: 'moduller', ad: 'Etkileşimli ve öğretici modüller (MVP)',
    dosya: `src/hikaye/moduller/** (index.js dahil; kayıt noktası zaten bağlı), yeni giris-hikaye klasörüne dosya YOK (CSS'i JS içinden <style> olarak enjekte et; dil metinleri modül dosyalarında TR/EN sözlük + dil() ve 'ege:dil' olayı ile)`,
    gorev: `moduller.json kataloğundan MVP dalgası (denetim önerisi): urun_secici ("Evde nerede?" ürün seçici + kalıcı 'Araçlar' çekmecesi), duvar_hesap (alan → blok adedi: 60×25 cm yüz = 0,15 m² → yaklaşık 6,67 adet/m²; 'yaklaşık' ibaresi, kaynak = Ürün föyleri 60×25 cm; teklif bağlantısına bağlam taşır), maket_blok_sayaci ("bu evde kaç blok var": sayıyı maket modelinden HESAPLA: ${PY} ile blender/bina_detay.py uret() çıktısında tur=='blok' parça sayısı veya blok boyutlarından hacim hesabı; kaynak etiketi "maket modelinden hesap"; kendin çalıştır ve sayıyı koda göm), once_sonra (planın tanımına göre; yalnız doğrulanmış bilgi), kesit_gezgini (blok / U blok (donatı + dolgu betonu) / EGEPOR kolon kaplaması SVG kesitleri; bilgiler DEVIR.md ve dil.js'teki teyitli föy bilgileri), isterse agirlik (yoğunluk 300–600 kg/m³ ve kalınlıktan kütle; yalnız hesap, karşılaştırma yapıyorsan doğrulanmış kaynak). Plan satırlarının 'etkilesim' alanlarında geçen modül çipleri/zamanlar (örn. t=34-35 ürün seçici, t=56-57 yarışma sorusu vb.) ile uyumlu zamanlar (ortak.saniyeyeGit(t) motor tarafından eklenecek; yoksa kendi vh=t*22 hesabını kullan, görünürlük için sahne ilerlemesini oku). Kurallar: KAYDIRMA KİLİDİ YOK (paneller kilitsiz, kenar paneli/alt şerit; kaydırınca kapanır/küçülür), depolama yok (yalnız bellek), tüm sayılar kaynaklı ve yalnız doğrulanmış (föy: 60×25 cm, 5–35 cm (teyit bekleyen: kaydırıcıda 20 ve 25 cm örnek kullan), λ 0,16 (U blok G4/06), λ 0,051–0,062 (Egepor), λ 0,08 G2/350, 300–600 kg/m³ vb.), dataLayer olayları (data-iz altyapısı), 50 fps, erişilebilir (klavye/aria), TR/EN, prefers-reduced-motion. 'Araçlar n/N' çekmecesi: yolculuk çubuğunun yanında, t<34'te gizli (s1 çip çubuğuyla belirir), finale'de yok. Hesaplayıcı sonuç bağlantıları: /teklif/?kaynak=hikaye&dil=&urun=&nokta= şemasıyla (pazarlama.json baglanti_semasi). Test: yer tutucu karelerle derle + sinama; modül açma/kapama/kaydırma etkileşimini Playwright ile dene.` },
]

const SONUC = {
  type: 'object',
  properties: {
    ozet: { type: 'string' },
    dosyalar: { type: 'array', items: { type: 'string' } },
    kalan: { type: 'array', items: { type: 'string' } },
  },
  required: ['ozet'],
}
const ENT = {
  type: 'object',
  properties: {
    ok: { type: 'boolean' },
    ozet: { type: 'string' },
    sorunlar: { type: 'array', items: { type: 'object', properties: { onem: { type: 'string', enum: ['blocker', 'high', 'medium', 'low'] }, sorun: { type: 'string' }, dosya: { type: 'string' }, duzeltme: { type: 'string' } }, required: ['onem', 'sorun'] } },
    ekran_goruntuleri: { type: 'array', items: { type: 'string' } },
  },
  required: ['ok', 'ozet'],
}

phase('Uygula')
const uyg = await parallel(IS.map(s => () => agent(`${BAGLAM}

GÖREV: "${s.ad}" işini uygula.
SAHİP OLDUĞUN DOSYALAR (yalnız bunlara yaz): ${s.dosya}
YAPILACAKLAR: ${s.gorev}
Bittiğinde (derlenir, sınanır) kısa özet nesnesi döndür.`, { label: 'uygula:' + s.id, phase: 'Uygula', schema: SONUC })))
const ozetler = {}
IS.forEach((s, i) => { ozetler[s.id] = uyg[i] })
log('Uygula bitti: ' + IS.filter((s, i) => uyg[i]).map(s => s.id).join(', '))

phase('Entegrasyon')
const ent = await agent(`${BAGLAM}

GÖREV: ENTEGRASYON DENETÇİSİ. Üç agent (motor, içerik+finale, modüller) paralel çalıştı; özetleri:
${IS.map(s => `- ${s.id}: ${ozetler[s.id] ? ozetler[s.id].ozet : '(sonuç yok)'}`).join('\n')}
Şimdi hepsinin birlikte çalıştığını doğrula (ve küçük çakışmaları düzeltebilirsin: bu aşamada tüm web dosyalarını düzenleyebilirsin): 1) node tools/derle.mjs ${NM} hatasız; 2) yer tutucu kare kökü üret (${PY} tools/kare_taklit.py /tmp/kt_web --kucuk) → kareler.py → giris-hikaye/kareler; 3) node tools/sinama.mjs /tmp/sinama_ent (http) ve file modu: konsol hatası yok, kaydırma, rAF boşta durur, fps; 4) masaüstü ve telefon ekran görüntüleri: sahne geçişleri, s0 açılış, ürün turu çipleri/Araçlar çekmecesi, bir modül açık, finale (logo, CTA); görüntüleri Read ile gör ve sorunları yaz; 5) TR/EN geçişi; 6) kural taraması: kanvas üstünde backdrop-filter/mix-blend, DPR>1,25, localStorage/sessionStorage/çerez kullanımı, harici URL isteği, 'yanmaz', 'Aliağa', 'Alsancak', ülke adı, kaynaksız rakam, lime kullanımı (ürün dışı), slogan açılışta görünüyor mu, logo finalden önce görünüyor mu (üst çubuktaki yer tutucu logo hariç: planın kararını oku: akt-son açık sorusu; üst çubuk logosu hikâye boyunca VAR kalsın); 7) plan uyumu: s0..finale vuruş metinleri ve zamanları (vh=t*22) ile index.html data-bas/data-son uyumu, CTA çizelgesi, modül zamanları. Sorunları önem sırasıyla yaz; blocker/high olanları ve kolay medium'ları KENDİN düzelt, kalanı raporla. Düzelttikten sonra yeniden derle+sına. ok=true yalnız blocker/high kalmadıysa. giris-hikaye/kareler yer tutucu kareleri içerir: BİTİRİRKEN giris-hikaye/kareler klasörünü TEMİZLE (rm -rf giris-hikaye/kareler/*; boş klasör bırak) ki repoya yer tutucu girmesin.`, { label: 'entegrasyon', phase: 'Entegrasyon', schema: ENT })

phase('Düzelt')
let duz = null
if (ent && !ent.ok) {
  duz = await agent(`${BAGLAM}

GÖREV: Entegrasyon denetimi blocker/high sorun buldu; hepsini gider. Tüm web dosyalarını düzenleyebilirsin.
DENETİM: ${ent.ozet}
SORUNLAR:
${(ent.sorunlar || []).map((q, i) => `${i + 1}. [${q.onem}] ${q.sorun}${q.dosya ? ' (' + q.dosya + ')' : ''}${q.duzeltme ? '\n   Öneri: ' + q.duzeltme : ''}`).join('\n')}
Düzelt, derle (${NM}), yer tutucu karelerle sına; bittiğinde giris-hikaye/kareler içeriğini TEMİZLE. Kısa özet döndür.`, { label: 'duzelt', phase: 'Düzelt', schema: ENT })
}
return { ozetler, ent, duz }
