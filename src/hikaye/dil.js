/**
 * TR / EN metinler.
 * Sayfadaki Türkçe metinler HTML'de durur (arama motoru ve JS'siz görünüm için);
 * İngilizce karşılıklar burada. Tıklanır nokta metinleri iki dilde de burada.
 * Kurallar: ülke adı yok · "25+ ülke" · A1 "yangına tepki sınıfı" (yanmaz denmez) ·
 * her sayının kaynağı kartta yazılı.
 */
export const EN = {
  'nav.urunler': 'Products',
  'nav.teknik': 'Technical data',
  'nav.araclar': 'Tools',
  'nav.projeler': 'Projects',
  'nav.blog': 'Blog',
  'nav.iletisim': 'Contact',
  'cta.teklif': 'Get a quote',
  'cta.katalog': 'Product catalogue',
  'cta.foyler': 'Technical sheets',
  'cta.hesapla': 'Calculate your walls',
  'giris.ust': 'EGE GAZBETON · Söke & İzmir',
  'giris.baslik': 'Built on trust —<br><em>today and tomorrow</em>',
  'giris.metin': 'AAC blocks, lintels and panels from two plants with one standard of quality. Scroll to follow the journey from raw material to building.',
  'giris.kitle': 'Find your way:',
  'kitle.sahip': 'I am building',
  'kitle.mimar': 'Architect / engineer',
  'kitle.bayi': 'Export buyer / dealer',
  'giris.kaydir': 'Scroll · from raw material to building',
  'giris.atla': 'Skip the story',
  'yol.s0': 'Block',
  'yol.s1': 'Production',
  'yol.s2': 'Structure',
  'yol.s3': 'System',
  'yol.s4': 'World',
  'yol.son': 'Quote',
  'i0.ust': '01 · Product',
  'i0.baslik': 'It all starts with <em>a single block.</em>',
  'i0.metin': 'AAC block with a 60 × 25 cm face: light, easy to work and laid with thin joints. Made in our two plants in Söke and İzmir.',
  'i0.k1': 'plants · Söke & İzmir',
  'i0.k2': 'm³ production capacity',
  'i0.k3': 'AAC masonry units standard',
  'i1.ust': '02 · Production',
  'i1.baslik': 'Sand, lime, cement and gypsum — <em>and a little aluminium.</em>',
  'i1.a1': 'Mixing',
  'i1.a1m': 'The raw materials are mixed with water and poured into the mould.',
  'i1.a2': 'Rising',
  'i1.a2m': 'Aluminium powder reacts and the mix rises, forming countless small air cells inside.',
  'i1.a3': 'Cutting & autoclave',
  'i1.a3m': 'Wires cut the cake to precise sizes; high-pressure steam in the autoclave hardens it.',
  'i2.ust': '03 · Structure',
  'i2.baslik': 'The insulation is <em>the air inside.</em>',
  'i2.metin': 'Closed air cells slow down the flow of heat. The mineral structure is in reaction-to-fire class A1.',
  'i2.k1': 'design value for G2/350 walls',
  'i2.k2': 'reaction to fire · EN 13501-1',
  'i2.k3': 'density range (G1–G4)',
  'i3.ust': '04 · System',
  'i3.baslik': 'One system, <em>in the right order.</em>',
  'i3.metin': 'The frame comes first, then the AAC walls rise course by course; lintels span the openings and panels close the roof.',
  'i3.k1': 'building mass',
  'i3.k2': 'base shear',
  'i3.kaynak': 'METU study, calculation for an 8-storey sample building',
  'i4.ust': '05 · World',
  'i4.baslik': 'From the Aegean <em>to the world.</em>',
  'i4.metin': 'Pallets loaded in Söke and İzmir, close to the ports of Aliağa and Alsancak, reach five continents.',
  'i4.k1': 'countries',
  'i4.k2': 'continents',
  'son.baslik': 'Get a quote <em>for your project.</em>',
  'son.metin': 'Tell us the size and type of your walls; our team prepares the right AAC solution.',
  'son.slogan': 'Built on trust — today and tomorrow',
  'kaynak': 'Source',
  'kapat': 'Close',
  'sonra.baslik': 'Product groups',
  'sonra.metin': 'Blocks, lintels, panels and adhesive: everything an AAC wall and roof system needs, from one manufacturer.',
  'dil.tr': 'TR',
  'dil.en': 'EN',
  'yol.baslik': 'Story',
  'urun.duvar': 'Wall blocks',
  'urun.duvarm': 'Plain and tongue-and-groove blocks, 5–35 cm',
  'urun.lento': 'Lintels',
  'urun.lentom': 'Over openings, up to 4.50 m',
  'urun.ublok': 'U-blocks and corner blocks',
  'urun.ublokm': 'Bond beam and corner details',
  'urun.panel': 'Panels',
  'urun.panelm': 'Wall, floor and roof panels',
  'urun.tutkal': 'AAC adhesive',
  'urun.tutkalm': 'Thin-joint mortar',
  'urun.egeporm': 'Mineral thermal insulation board',
  'alt.kvkk': 'Privacy (KVKK)',
  'kaynak.ortak': 'Ege Gazbeton shared figures',
  'kaynak.ce': 'CE certificates',
  'kaynak.siniflar': 'Product classes G1/300 – G4/600',
  'kaynak.odtu': 'METU',
  'kaynak.ihracat': 'Ege Gazbeton export department',
  'sayfa.baslik': 'Ege Gazbeton | AAC from raw material to building',
  'aria.logo': 'Ege Gazbeton home',
  'aria.menu': 'Main menu',
  'aria.menuac': 'Menu',
  'aria.yol': 'Story chapters',
  'aria.s1': 'Production: from raw material to block',
  'aria.s2': 'Structure: diving into a pore',
  'aria.s3': 'System: the building rises in the right order',
  'aria.s4': 'World: from the Aegean to five continents',
};

/** Tıklanır noktalar: başlık, kısa açıklama, kaynak (TR / EN). */
export const NOKTALAR = {
  kum: {
    tr: ['Kum', 'Silis kumu: gazbetonun ana hammaddesi.'],
    en: ['Sand', 'Silica sand: the main raw material of AAC.'],
  },
  kirec: {
    tr: ['Kireç', 'Karışımın bağlayıcısı. Söke\'de günde 200 ton kapasiteli kendi kireç tesisimiz var.', 'Ege Gazbeton ortak rakamlar'],
    en: ['Lime', 'The binder of the mix. Our own lime plant in Söke produces 200 tonnes a day.', 'Ege Gazbeton shared figures'],
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
  kabarma: {
    tr: ['Kabarma', 'Kalıptaki karışım kabarır ve ön sertleşme kazanır.'],
    en: ['Rising', 'The mix rises in the mould and pre-hardens.'],
  },
  kesim: {
    tr: ['Tel kesim', 'Teller keki hassas ölçüde keser; yüzeyler düz ve gönyede olur.'],
    en: ['Wire cutting', 'Wires cut the cake precisely; faces come out flat and square.'],
  },
  hucre: {
    tr: ['Kapalı hava hücresi', 'Hücredeki hava hareket etmez; ısı kolay geçemez.'],
    en: ['Closed air cell', 'The air in the cell does not move; heat cannot pass easily.'],
  },
  matris: {
    tr: ['Mineral matris', 'Otoklavda buharla sertleşen kalsiyum silikat yapı.'],
    en: ['Mineral matrix', 'A calcium silicate structure hardened by steam in the autoclave.'],
  },
  duvar: {
    tr: ['Duvar blokları', '60 × 25 cm yüz, 1–3 mm ince derz ile örülür.', 'Ürün föyleri'],
    en: ['Wall blocks', '60 × 25 cm face, laid with 1–3 mm thin joints.', 'Product sheets'],
  },
  lento: {
    tr: ['Lentolar', 'Açıklık üstünde, duvarla aynı malzeme; 4,50 m\'ye kadar.', 'Ürün föyleri'],
    en: ['Lintels', 'Over openings, in the same material as the wall; up to 4.50 m.', 'Product sheets'],
  },
  cati: {
    tr: ['Çatı panelleri', 'Gazbeton döşeme ve çatı panelleri 6 m\'ye varan açıklığı geçer.', 'Ürün föyleri'],
    en: ['Roof panels', 'AAC floor and roof panels span up to 6 m.', 'Product sheets'],
  },
  kaynak: {
    tr: ['Söke & İzmir', 'İki fabrika; Aliağa ve Alsancak limanlarına yakın.'],
    en: ['Söke & İzmir', 'Two plants, close to the ports of Aliağa and Alsancak.'],
  },
  kitalar: {
    tr: ['5 kıta', '5 kıtada 25\'ten fazla ülkeye ihracat.', 'Ege Gazbeton ihracat bölümü'],
    en: ['5 continents', 'Exports to more than 25 countries on five continents.', 'Ege Gazbeton export department'],
  },
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
  for (const b of document.querySelectorAll('[data-dil-sec]')) {
    b.setAttribute('aria-pressed', String(b.dataset.dilSec === current));
  }
  document.dispatchEvent(new CustomEvent('ege:dil', { detail: current }));
}
