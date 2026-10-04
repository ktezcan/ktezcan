/**
 * TR / EN metinler.
 * Sayfadaki Türkçe metinler HTML'de durur (arama motoru ve JS'siz görünüm için; her vuruş plan satırının metin_tr'sidir);
 * İngilizce karşılıklar (plan metin_en) burada, aynı data-i18n anahtarıyla. Tıklanır nokta kartları iki dilde de burada.
 * Kurallar: ülke adı yok · "25+ ülke · 5 kıta" · A1 "yangına tepki sınıfı" (yanmaz denmez) · liman adı yok ·
 * kaynaksız çoğunluk iddiası yok · her sayının kaynağı kartta yazılı · EN'de "lime" = kireç ise "Lime (binder)",
 * streç film için "lime-green stretch film".
 */
export const EN = {
  // Menü, düğmeler, sayfa
  'nav.urunler': 'Products',
  'nav.teknik': 'Technical data',
  'nav.araclar': 'Tools',
  'nav.projeler': 'Projects',
  'nav.blog': 'Blog',
  'nav.iletisim': 'Contact',
  // Açılış (hero) ve Hayal sahnesi (s0, 0–32 sn)
  'giris.ust': 'EGE GAZBETON · Söke &amp; İzmir',
  'giris.baslik': 'Every home starts <em>with a line.</em>',
  'giris.metin': 'AAC blocks, lintels, panels and adhesive from our two plants in Söke and İzmir, built to one standard of quality.',
  'cta.teklif': 'Get a quote',
  'kitle.sahip': 'I am building',
  'kitle.mimar': 'Architect / engineer',
  'kitle.bayi': 'Export buyer / dealer',
  'giris.kitle': 'Find your way:',
  'giris.kaydir': 'Scroll · from idea to home',
  'giris.atla': 'Skip the story',
  's0a.ust': '01 · Idea',
  's0a.baslik': 'First the idea, <em>then the plan.</em>',
  's0a.metin': 'Shaped by the <span class="eg-cizgi">sun</span>, the <span class="eg-cizgi eg-cizgi--2">street</span> and the <span class="eg-cizgi eg-cizgi--3">garden</span>.',
  's0b.ust': '01 · Idea',
  's0b.baslik': 'Lines become <em>volume.</em>',
  's0c.r1.k': 'block face',
  'kaynak.foy': 'Product sheets',
  's0c.r2.k': 'thin joint',
  's0c.ust': '01 · Idea',
  's0c.baslik': 'AAC walls, <em>course by course.</em>',
  's0c.metin': 'Block by block, with 1–3 mm joints.',
  's0d.ust': '01 · Idea',
  's0d.baslik': 'From drawing <em>to reality.</em>',
  's0e.ust': '01 · Idea',
  's0e.baslik': 'Life starts <em>on the street.</em>',
  's0e.metin': 'On the truck: AAC pallets from Söke and İzmir.',
  's0f.ust': '01 · Idea',
  's0f.baslik': 'The day ends, <em>the lights come on.</em>',
  'cta.urunler': 'See the products',
  's0g.soz': 'So what makes this <em>home so good?</em>',
  // Ürün turu (s1, 32–70 sn)
  'aria.s1': 'Products: six products, one system',
  'durak.duvar': 'Walls',
  'durak.lento': 'Lintels',
  'durak.ublok': 'U-blocks',
  'durak.tutkal': 'Adhesive',
  'durak.panel': 'Panels',
  'durak.egepor': 'EGEPOR',
  'aria.durak': 'Product stops',
  's1a.ust': '02 · Products',
  's1a.baslik': 'Six products. <em>One system.</em>',
  's1a.metin': 'One product at every stop.',
  's1b.etiket': 'Plain · Tongue-and-groove',
  's1b.r1.k': 'face',
  's1b.r2.k': 'thin joint',
  'cta.hesapla': 'Calculate your walls',
  's1b.ust': '02 · Products · 1/6',
  's1b.baslik': 'Wall blocks',
  's1b.metin': 'For exterior and interior walls; slows heat, light, quick to lay.',
  's1c.r1.b': '4.50 m',
  's1c.r1.k': 'span, up to',
  's1c.ust': '02 · Products · 2/6',
  's1c.baslik': 'Lintels',
  's1c.metin': 'Bridges the openings; the same material as the wall.',
  's1u.r1.k': 'cm length × height · 20–25 cm thick',
  's1u.r2.b': 'λ 0.16',
  's1u.r2.k': 'W/mK, dry (G4/06)',
  's1u.ust': '02 · Products · 3/6',
  's1u.baslik': 'U-blocks',
  's1u.metin': 'Ready-made formwork for bond beams: pour concrete, no timber formwork.',
  's1d.r1.k': 'joint thickness',
  's1d.ust': '02 · Products · 4/6',
  's1d.baslik': 'AAC adhesive',
  's1d.metin': 'Thin-joint mortar: the wall stays flat and uniform.',
  's1e.r1.k': 'span, up to (floor / roof panel)',
  's1e.ust': '02 · Products · 5/6',
  's1e.baslik': 'Panels',
  's1e.metin': 'For roofs, floors and walls.',
  's1k.r1.b': '−17%',
  's1k.r1.k': 'building mass',
  'kaynak.odtu': 'METU study, calculation for an 8-storey sample building',
  's1k.ust': '02 · Products',
  's1k.baslik': 'A lighter building, <em>a lower seismic load.</em>',
  's1f.r1.b': 'λ 0.051–0.062',
  's1f.r1.k': 'W/mK, dry',
  's1f.r2.k': 'kg/m³ dry density',
  's1f.ust': '02 · Products · 6/6',
  's1f.baslik': 'EGEPOR',
  's1f.metin': 'Cladding for columns and beams; also on facades, car park and basement ceilings.',
  's1g.soz': 'One mineral material <em>from wall to roof.</em>',
  's1h.soz': 'So how is this block <em>born?</em>',
  'cta.sistem': 'Six products, one quote',
  'cta.katalog': 'Product catalogue',
  // Doğuş (s2, 70–90 sn)
  'aria.s2': 'Production: from raw material to block',
  's2a.ust': '03 · Production',
  's2a.baslik': 'One block, <em>five raw materials.</em>',
  's2a.metin': 'Tap the dots.',
  's2m.kum': 'Sand',
  's2m.kumk': 'Main raw material.',
  's2m.kirec': 'Lime (binder)',
  's2m.kireck': 'Binder.',
  's2m.cimento': 'Cement',
  's2m.cimentok': 'Adds strength.',
  's2m.alci': 'Gypsum',
  's2m.alcik': 'Controls setting.',
  's2m.aluminyum': 'Aluminium powder',
  's2m.aluminyumk': 'Makes it rise.',
  's2b.ust': '03 · Production',
  's2c.ust': '03 · Production',
  's2c.baslik': 'Mixing — <em>water is added.</em>',
  's2c.metin': 'The mould fills.',
  's2d.ust': '03 · Production',
  's2d.baslik': 'Rising — <em>hydrogen bubbles.</em>',
  's2d.metin': 'The mix swells, air cells remain.',
  's2e.ust': '03 · Production',
  's2e.baslik': 'Wire cutting.',
  's2e.metin': 'Faces flat and square.',
  's2f.ust': '03 · Production',
  's2f.baslik': 'Autoclave — <em>pressurised steam.</em>',
  's2f.metin': 'A mineral structure forms.',
  's2g.ust': '03 · Production',
  's2g.baslik': 'Hardened.',
  's2h.soz': 'Cell by cell, <em>trapped air.</em>',
  // Gözenek (s3, 90–104 sn)
  'aria.s3': 'Structure: diving into a pore',
  's3a.etiket': 'Closed air cell',
  's3a.ust': '04 · Structure',
  's3a.baslik': 'The insulation is <em>the air inside.</em>',
  's3a.metin': 'Air trapped in every pore.',
  's3b.etiket': 'hot · cold',
  's3b.ust': '04 · Structure',
  's3b.baslik': 'Heat winds around the pores <em>and slows.</em>',
  'cta.foyler': 'Technical specifications',
  's3c.r1.b': 'λ 0.08',
  's3c.r1.k': 'W/mK · design value for G2/350 walls',
  'kaynak.ortak': 'Ege Gazbeton shared figures',
  's3c.r2.k': 'reaction-to-fire class · EN 13501-1',
  'kaynak.ce': 'CE certificates',
  's3c.r3.k': 'kg/m³ · density range (G1–G4)',
  'kaynak.siniflar': 'Product classes G1/300 – G4/600',
  's3c.ust': '04 · Structure',
  // Yol (s4, 104–120 sn)
  'aria.s4': 'On the road: from the plant to the site',
  's4a.ust': '05 · On the road',
  's4a.baslik': 'From the plant <em>to the site.</em>',
  's4a.metin': 'Every pallet is wrapped in lime-green stretch film.',
  's4b.r1.k': 'plants · Söke &amp; İzmir',
  's4c.metin': 'Load secured, the truck rolls out.',
  's4d.r1.k': 'lime plant capacity per day',
  's4e.r1.b': '1,100,000',
  's4e.r1.k': 'm³ production capacity',
  'cta.toplu': 'Enquire about bulk orders',
  's4f.metin': 'The truck is on its way.',
  // Dünya (s5, 120–136 sn)
  'aria.s5': 'World: from the Aegean to five continents',
  's5a.ust': '06 · World',
  's5a.baslik': 'From the Aegean <em>to the world.</em>',
  's5a.metin': 'Pallets loaded in Söke and İzmir reach five continents.',
  's5b.r1.k': 'countries',
  'kaynak.ihracat': 'Ege Gazbeton export department',
  's5b.r2.k': 'continents',
  'cta.ihracat': 'Contact our export team',
  'kita.kita': 'continents',
  // Finale (136–146 sn): Güven → logo → slogan → teklif
  'son.guven': 'Trust.',
  'son.slogan': 'Built on trust — today and tomorrow',
  'son.baslik': 'Get a quote <em>for your project.</em>',
  'baglam.baktiginiz': 'You looked at:',
  'baglam.sil': 'Remove product context',
  'son.metin': 'Send your wall dimensions; we prepare the solution.',
  'son.k1': 'plants · Söke &amp; İzmir',
  'son.k2': 'reaction-to-fire class · EN 13501-1',
  'son.k3': 'countries · 5 continents',
  'son.tekrar': 'Watch the story again',
  'aria.akis': 'From idea to home, from products to the world: the Ege Gazbeton story',
  'aria.yol': 'Story chapters',
  'aria.menu': 'Main menu',
  'aria.logo': 'Ege Gazbeton home',
  'aria.menuac': 'Menu',
  'kapat': 'Close',
  'yol.baslik': 'Story',
  'atla.icerik': 'Skip to main content',
  'sonra.baslik': 'Product groups',
  'sonra.metin': 'Blocks, lintels, panels and adhesive: everything an AAC wall and roof system needs, from a single supplier.',
  'sonra.baktiginiz': 'You looked at this',
  'alt.kvkk': 'Privacy (KVKK)',
  'kart.urun': 'Product page',
  'kart.foy': 'Technical sheet',
  'kaynak': 'Source',
  'dil.oneri': 'Türkçe göster',
  'sayfa.baslik': 'Ege Gazbeton | AAC Blocks, Lintels and Panels · Söke & İzmir',
  'sayfa.aciklama': 'AAC blocks, lintels, panels and adhesive made in two plants in Söke and İzmir. Follow the story from idea to home and get a quote for your project.',
  'aria.kita': 'Five continents counter',
  'aria.kitalar': 'Continents',
  'yol.s0': 'Idea',
  'yol.s1': 'Products',
  'yol.s2': 'Production',
  'yol.s3': 'Structure',
  'yol.s4': 'On the road',
  'yol.s5': 'World',
  'yol.son': 'Quote',
  'yol.paylas': 'Share',
  'urun.duvar': 'Wall blocks',
  'urun.duvarm': 'Plain and tongue-and-groove blocks',
  'urun.lento': 'Lintels',
  'urun.lentom': 'Over openings, up to 4.50 m',
  'urun.ublok': 'U-blocks and corner blocks',
  'urun.ublokm': 'Formwork for bond beams, hidden chimneys and downpipes',
  'urun.panel': 'Panels',
  'urun.panelm': 'Wall, floor and roof panels',
  'urun.tutkal': 'AAC adhesive',
  'urun.tutkalm': 'Thin-joint mortar',
  'urun.egeporm': 'Mineral thermal insulation board; column and beam cladding',
};

/** Ürün kodları (?urun=) → ad (TR/EN) ve sayfa yolu; ürün grupları bölümüyle aynı adresler. */
export const URUN = {
  duvar: { tr: 'Duvar blokları', en: 'Wall blocks', yol: '/urunler/duvar-bloklari/' },
  lento: { tr: 'Lentolar', en: 'Lintels', yol: '/urunler/lentolar/' },
  ublok: { tr: 'U bloklar', en: 'U-blocks', yol: '/urunler/u-blok-kose/' },
  tutkal: { tr: 'Gazbeton tutkalı', en: 'AAC adhesive', yol: '/urunler/tutkal/' },
  panel: { tr: 'Paneller', en: 'Panels', yol: '/urunler/paneller/' },
  egepor: { tr: 'EGEPOR', en: 'EGEPOR', yol: '/urunler/egepor/' },
};

/** Kıta etiketleri (dünya sahnesi; ülke adı yok): varış çapası = kareler-meta hotspots anahtarı; p = varış karesi / (n−1). */
export const KITA = {
  v_avrupa: { tr: 'Avrupa', en: 'Europe', varis: 50 },
  v_afrika: { tr: 'Afrika', en: 'Africa', varis: 59 },
  v_amerika: { tr: 'Amerika', en: 'The Americas', varis: 73 },
  v_asya: { tr: 'Asya', en: 'Asia', varis: 103 },
  v_okyanusya: { tr: 'Okyanusya', en: 'Oceania', varis: 124 },
};
/** s5 kare sayısı (193): varış kareleri bu ölçekte p'ye çevrilir; meta farklı n verirse p yine aynı kalır. */
export const KITA_KARE = 193;
/** Kıta etiketinin ekranda kalma süresi (film sn); dünya parçası 16 sn → p = 1,6 / 16. */
export const KITA_SURE_SN = 1.6;

/**
 * Tıklanır noktalar: [başlık, kısa açıklama, kaynak?] (TR / EN); `urun` varsa kartta "Ürün sayfası → · Teknik föy" bağlantıları çıkar.
 * Anahtarlar kareler-meta.js hotspots adlarıyla BİREBİR aynıdır (blender/*.py meta.json).
 */
export const NOKTALAR = {
  // --- s0 · Hayal ---
  sokak: {
    tr: ['Sokak', 'Kaldırım, ağaçlar ve yol: ev sokağıyla birlikte düşünülür.'],
    en: ['Street', 'Pavement, trees and road: the home is planned with its street.'],
  },
  eskiz: {
    tr: ['Eskiz', 'İlk çizgiler: kütle, pencereler, bahçe duvarı.'],
    en: ['Sketch', 'The first lines: volume, windows, garden wall.'],
  },
  tir: {
    tr: ['Ege Gazbeton', "Lime streçli paletler: Söke ve İzmir'den sahaya."],
    en: ['Ege Gazbeton', 'Pallets in lime-green stretch film: from Söke and İzmir to the site.'],
  },
  giris: {
    tr: ['Giriş', 'Bahçe yolundan kapıya: sokağa açılan ön cephe.'],
    en: ['Entrance', 'From the garden path to the door: the front facing the street.'],
  },
  bahce: {
    tr: ['Bahçe', 'Çim, çalı ve lavanta: güneşe bakan ön bahçe.'],
    en: ['Garden', 'Grass, shrubs and lavender: a front garden facing the sun.'],
  },
  yuva: {
    tr: ['Yuva', 'Akşam olur; her pencerede başka bir hayat.'],
    en: ['Home', 'Evening comes; a different life behind every window.'],
  },
  blok: {
    tr: ['Gazbeton blok', '60 × 25 cm yüz; sıra sıra, şaşırtmalı örülür.', 'Ürün föyleri'],
    en: ['AAC block', '60 × 25 cm face; laid course by course in a staggered bond.', 'Product sheets'],
  },
  lento: {
    tr: ['Lentolar', "Açıklık üstünde, duvarla aynı malzeme; 4,50 m'ye kadar.", 'Ürün föyleri'],
    en: ['Lintels', 'Over openings, in the same material as the wall; up to 4.50 m.', 'Product sheets'],
  },
  panel: {
    tr: ['Çatı panelleri', "Gazbeton döşeme ve çatı panelleri 6 m'ye varan açıklığı geçer.", 'Ürün föyleri'],
    en: ['Roof panels', 'AAC floor and roof panels span up to 6 m.', 'Product sheets'],
  },
  derz: {
    tr: ['İnce derz', 'Bloklar 1–3 mm gazbeton tutkalıyla birleşir.', 'Ürün föyleri'],
    en: ['Thin joint', 'Blocks are bonded with 1–3 mm AAC adhesive.', 'Product sheets'],
  },
  // --- s1 · Ürün turu (durak adı = u_<ürün>) ---
  u_duvar: {
    tr: ['Duvar blokları', 'Düz ve geçmeli bloklar; 60 × 25 cm yüz, 1–3 mm ince derzle örülür.', 'Ürün föyleri'],
    en: ['Wall blocks', 'Plain and tongue-and-groove blocks; 60 × 25 cm face, laid with 1–3 mm thin joints.', 'Product sheets'],
    urun: 'duvar',
  },
  u_lento: {
    tr: ['Lentolar', "Açıklık üstünde, duvarla aynı malzeme; 4,50 m'ye kadar.", 'Ürün föyleri'],
    en: ['Lintels', 'Over openings, in the same material as the wall; up to 4.50 m.', 'Product sheets'],
    urun: 'lento',
  },
  u_ublok: {
    tr: ['U bloklar', 'Hatıl için kalıp: kanala donatı konur, beton dökülür; çatı hizası, yüksek duvar ara hatılı, gizli baca ve yağmur iniş borusu için. 60 × 25 cm, 20–25 cm kalınlık.', 'Ürün föyleri'],
    en: ['U-blocks', 'Formwork for bond beams: reinforcement in the channel, then concrete; for roof level, intermediate beams in tall walls, hidden chimneys and rainwater downpipes. 60 × 25 cm, 20–25 cm thick.', 'Product sheets'],
    urun: 'ublok',
  },
  u_tutkal: {
    tr: ['Gazbeton tutkalı', 'İnce derz harcı: 1–3 mm.', 'Ürün föyleri'],
    en: ['AAC adhesive', 'Thin-joint mortar: 1–3 mm.', 'Product sheets'],
    urun: 'tutkal',
  },
  u_panel: {
    tr: ['Paneller', "Döşeme ve çatı panelleri; 6 m'ye varan açıklık. ODTÜ çalışması: 8 katlı örnek bina hesabında yapı kütlesi −%17.", 'Ürün föyleri · ODTÜ çalışması'],
    en: ['Panels', 'Floor and roof panels; spans up to 6 m. METU study: building mass −17% in the calculation for an 8-storey sample building.', 'Product sheets · METU study'],
    urun: 'panel',
  },
  u_egepor: {
    tr: ['EGEPOR', 'Mineral ısı yalıtım levhası: kolon ve kiriş kaplaması, dış cephe, otopark ve bodrum tavanı. λ 0,051–0,062 W/mK.', 'Ürün föyleri'],
    en: ['EGEPOR', 'Mineral thermal insulation board: column and beam cladding, facades, car park and basement ceilings. λ 0.051–0.062 W/mK.', 'Product sheets'],
    urun: 'egepor',
  },
  u_blok: {
    tr: ['Tek blok', 'Bu blok nasıl doğuyor? Kaydırın.'],
    en: ['One block', 'How is this block born? Keep scrolling.'],
  },
  // --- s2 · Doğuş ---
  kum: {
    tr: ['Kum', 'Silis kumu: gazbetonun ana hammaddesi.'],
    en: ['Sand', 'Silica sand: the main raw material of AAC.'],
  },
  kirec: {
    tr: ['Kireç', "Karışımın bağlayıcısı. Söke'de günde 200 ton kapasiteli kendi kireç tesisimiz var.", 'Ege Gazbeton ortak rakamlar'],
    en: ['Lime (binder)', 'The binder of the mix. Our own lime plant in Söke produces 200 tonnes a day.', 'Ege Gazbeton shared figures'],
  },
  cimento: {
    tr: ['Çimento', 'Dayanımı destekleyen bağlayıcı.'],
    en: ['Cement', 'A binder that supports strength.'],
  },
  alci: {
    tr: ['Alçı', 'Prizlenmeyi düzenler.'],
    en: ['Gypsum', 'Regulates setting.'],
  },
  aluminyum: {
    tr: ['Alüminyum tozu', 'Kireçle tepkimeye girip hidrojen açığa çıkarır: karışım kabarır, hava hücreleri oluşur.'],
    en: ['Aluminium powder', 'Reacts with lime and releases hydrogen: the mix rises and air cells form.'],
  },
  kalip: {
    tr: ['Çelik kalıp', 'Karışım çelik kalıba dökülür; kabarma burada olur.'],
    en: ['Steel mould', 'The mix is poured into a steel mould; the rise happens here.'],
  },
  kabarma: {
    tr: ['Kabarma', 'Kalıptaki karışım kabarır ve ön sertleşme kazanır.'],
    en: ['Rising', 'The mix rises in the mould and pre-hardens.'],
  },
  kesim: {
    tr: ['Tel kesim', 'Teller keki hassas ölçüde keser; yüzeyler düz ve gönyede olur.'],
    en: ['Wire cutting', 'Wires cut the cake precisely; faces come out flat and square.'],
  },
  otoklav: {
    tr: ['Otoklav', 'Yüksek basınçlı buhar: kek burada sertleşir, mineral yapıya kavuşur.'],
    en: ['Autoclave', 'High-pressure steam: the cake hardens here and gains its mineral structure.'],
  },
  // --- s3 · Gözenek ---
  hucre: {
    tr: ['Kapalı hava hücresi', 'Hücredeki hava hareket etmez; ısı kolay geçemez.'],
    en: ['Closed air cell', 'The air in the cell does not move; heat cannot pass easily.'],
  },
  matris: {
    tr: ['Mineral matris', 'Otoklavda buharla sertleşen kalsiyum silikat yapı.'],
    en: ['Mineral matrix', 'A calcium silicate structure hardened by steam in the autoclave.'],
  },
  palet: {
    tr: ['Lime streç', 'Her palet lime renkli streç filmle sarılır ve kayışla bağlanır.'],
    en: ['Lime-green stretch film', 'Every pallet is wrapped in lime-green stretch film and strapped down.'],
  },
  // --- s4 · Yol ve s5 · Dünya ---
  fabrika: {
    tr: ['Söke fabrikası', 'Üretim holü, otoklavlar, silolar ve günde 200 ton kapasiteli kendi kireç tesisimiz. Görsel temsilîdir.', 'Ege Gazbeton ortak rakamlar'],
    en: ['Söke plant', 'Production hall, autoclaves, silos and our own lime plant producing 200 tonnes a day. The image is a representation.', 'Ege Gazbeton shared figures'],
  },
  kaynak: {
    tr: ['Söke & İzmir', 'İki fabrika, tek kalite anlayışı.', 'Ege Gazbeton ortak rakamlar'],
    en: ['Söke & İzmir', 'Two plants, one standard of quality.', 'Ege Gazbeton shared figures'],
  },
  kitalar: {
    tr: ['5 kıta', "5 kıtada 25'ten fazla ülkeye ihracat.", 'Ege Gazbeton ihracat bölümü'],
    en: ['5 continents', 'Exports to more than 25 countries on five continents.', 'Ege Gazbeton export department'],
  },
};

/**
 * Sahneye bağlı nokta kuralı: sahnede yalnız burada listelenen kareler-meta anahtarları görünür (diğerleri gizli kalır).
 *  nokta     = nabız halkası + etiket, tıklanınca kart
 *  etiket    = yalnız ad etiketi (nesneyi izler), tıklanmaz
 *  etiket-tik = ad etiketi, tıklanınca kart
 *  kita      = kıta etiketi (varışta 1,6 sn; tıklanmaz)
 * s0'da en çok 2 nokta (Sokak, Eskiz) + tırı izleyen marka etiketi; "ışığı sen yak" ve kapı etkileşimi yok.
 */
export const NOKTA_SAHNE = {
  s0: { sokak: 'nokta', eskiz: 'nokta', tir: 'etiket' },
  s1: { u_duvar: 'nokta', u_lento: 'nokta', u_ublok: 'nokta', u_tutkal: 'nokta', u_panel: 'nokta', u_egepor: 'nokta', u_blok: 'nokta' },
  s2: { kum: 'nokta', kirec: 'nokta', cimento: 'nokta', alci: 'nokta', aluminyum: 'nokta', kalip: 'nokta', kabarma: 'nokta', kesim: 'nokta', otoklav: 'nokta', blok: 'nokta' },
  s3: { hucre: 'nokta', matris: 'nokta', palet: 'nokta', fabrika: 'nokta' },
  s4: { tir: 'etiket-tik', fabrika: 'nokta', palet: 'nokta', kirec: 'nokta', otoklav: 'nokta', kaynak: 'nokta' },
  s5: { kaynak: 'nokta', kitalar: 'nokta', v_avrupa: 'kita', v_afrika: 'kita', v_amerika: 'kita', v_asya: 'kita', v_okyanusya: 'kita' },
};

let current = 'tr';

export function dil() {
  return current;
}

/** Sayfadaki [data-i18n] öğelerini seçilen dile çevirir; Türkçe asıllar ilk geçişte saklanır. */
export function dilUygula(lang) {
  current = lang === 'en' ? 'en' : 'tr';
  document.documentElement.lang = current;
  if (document.documentElement.dataset.trTitle === undefined) document.documentElement.dataset.trTitle = document.title;
  document.title = current === 'en' ? EN['sayfa.baslik'] : document.documentElement.dataset.trTitle;
  const aciklama = document.querySelector('meta[name="description"]');
  if (aciklama) {
    if (aciklama.dataset.tr === undefined) aciklama.dataset.tr = aciklama.content;
    aciklama.content = current === 'en' ? EN['sayfa.aciklama'] : aciklama.dataset.tr;
  }
  for (const el of document.querySelectorAll('[data-i18n]')) {
    if (el.dataset.tr === undefined) el.dataset.tr = el.innerHTML;
    const key = el.dataset.i18n;
    el.innerHTML = current === 'en' && EN[key] !== undefined ? EN[key] : el.dataset.tr;
  }
  for (const el of document.querySelectorAll('[data-i18n-aria]')) {
    if (el.dataset.trAria === undefined) el.dataset.trAria = el.getAttribute('aria-label') || '';
    const key = el.dataset.i18nAria;
    el.setAttribute('aria-label', current === 'en' && EN[key] ? EN[key] : el.dataset.trAria);
  }
  for (const b of document.querySelectorAll('[data-dil-sec], [data-dil-menu]')) {
    b.setAttribute('aria-pressed', String((b.dataset.dilSec || b.dataset.dilMenu) === current));
  }
  document.dispatchEvent(new CustomEvent('ege:dil', { detail: current }));
}
