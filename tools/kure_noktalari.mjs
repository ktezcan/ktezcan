// Dünya kara noktaları (world-atlas, Natural Earth — kamu malı) → ızgara noktaları + kıta kimliği.
// Ülke sınırı/ülke adı YOK (yalnız kara). Çıktı: JSON [[lat, lon, kita], ...]
// kita: 0 Avrupa, 1 Asya, 2 Afrika, 3 Amerika, 4 Okyanusya, 5 Türkiye (kaynak), 8 nötr (parlamaz), 9 Antarktika (atlanır)
//
// Kullanım:  node tools/kure_noktalari.mjs <node_modules_kökü> <adım|bolge|l1> <çıkış.json>
//   <adım> (sayı, örn. 1.25)  L2 küre: land-110m + countries-110m           → tex/kara_noktalari.json
//   bolge                     L0 bölge: land-10m + countries-10m (Türkiye 10 m poligonu), 36,3-40,0 K / 24,5-29,7 D,
//                             ≈1,25 km altıgen ızgara                       → tex/bolge_L0.json
//   l1                        L1: land-50m + countries-50m, 28-48 K / 12-48 D, 0,09° (≈10 km) altıgen ızgara
//                                                                           → tex/kara_L1.json
//   l15                       L1.5: land-110m, 0,4° (≈44 km) ızgara, yalnız İzmir'e 82° içindeki kap (küre doğuşu)
//                                                                           → tex/kara_L15.json
// Kıta kimlikleri üç seviyede aynıdır (küre dönerken seviyeler arası geçişte renk/dalga tutarlı kalsın).
// Bölge/L1 kipinde kara + ülke maskeleri satır tarama (scanline) ile çıkarılır: 10 m halkalar (>80 bin köşe) için hızlı.
import { readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const base = process.argv[2];
const mod = process.argv[3] || '1.25';
const cikis = process.argv[4];
const { feature } = require(`${base}/node_modules/topojson-client`);
const atlas = (ad) => JSON.parse(readFileSync(`${base}/node_modules/world-atlas/${ad}.json`, 'utf8'));

const KITA = {
  0: ['Norway', 'France', 'Sweden', 'Belarus', 'Ukraine', 'Poland', 'Austria', 'Hungary', 'Moldova', 'Romania', 'Lithuania',
    'Latvia', 'Estonia', 'Germany', 'Bulgaria', 'Greece', 'Albania', 'Croatia', 'Switzerland', 'Luxembourg', 'Belgium',
    'Netherlands', 'Portugal', 'Spain', 'Ireland', 'Italy', 'Denmark', 'United Kingdom', 'Iceland', 'Slovenia', 'Finland',
    'Slovakia', 'Czechia', 'Bosnia and Herz.', 'Macedonia', 'Serbia', 'Montenegro', 'Kosovo', 'Russia', 'Malta',
    'Liechtenstein', 'Andorra', 'San Marino', 'Vatican', 'Monaco'],
  1: ['Kazakhstan', 'Uzbekistan', 'Indonesia', 'Timor-Leste', 'Israel', 'Lebanon', 'Palestine', 'Jordan', 'United Arab Emirates',
    'Qatar', 'Kuwait', 'Iraq', 'Oman', 'Cambodia', 'Thailand', 'Laos', 'Myanmar', 'Vietnam', 'North Korea', 'South Korea',
    'Mongolia', 'India', 'Bangladesh', 'Bhutan', 'Nepal', 'Pakistan', 'Afghanistan', 'Tajikistan', 'Kyrgyzstan', 'Turkmenistan',
    'Iran', 'Syria', 'Armenia', 'Sri Lanka', 'China', 'Taiwan', 'Azerbaijan', 'Georgia', 'Philippines', 'Malaysia', 'Brunei',
    'Japan', 'Yemen', 'Saudi Arabia', 'Bahrain'],
  2: ['Tanzania', 'W. Sahara', 'Dem. Rep. Congo', 'Somalia', 'Kenya', 'Sudan', 'Chad', 'South Africa', 'Lesotho', 'Zimbabwe',
    'Botswana', 'Namibia', 'Senegal', 'Mali', 'Mauritania', 'Benin', 'Niger', 'Nigeria', 'Cameroon', 'Togo', 'Ghana',
    "Côte d'Ivoire", 'Guinea', 'Guinea-Bissau', 'Liberia', 'Sierra Leone', 'Burkina Faso', 'Central African Rep.', 'Congo',
    'Gabon', 'Eq. Guinea', 'Zambia', 'Malawi', 'Mozambique', 'eSwatini', 'Angola', 'Burundi', 'Madagascar', 'Gambia',
    'Tunisia', 'Algeria', 'Morocco', 'Egypt', 'Libya', 'Ethiopia', 'Djibouti', 'Somaliland', 'Uganda', 'Rwanda', 'Eritrea',
    'S. Sudan'],
  3: ['Canada', 'United States of America', 'Argentina', 'Chile', 'Haiti', 'Dominican Rep.', 'Bahamas', 'Falkland Is.',
    'Greenland', 'Mexico', 'Uruguay', 'Brazil', 'Bolivia', 'Peru', 'Colombia', 'Panama', 'Costa Rica', 'Nicaragua',
    'Honduras', 'El Salvador', 'Guatemala', 'Belize', 'Venezuela', 'Guyana', 'Suriname', 'Ecuador', 'Puerto Rico',
    'Jamaica', 'Cuba', 'Paraguay', 'Trinidad and Tobago'],
  4: ['Fiji', 'Papua New Guinea', 'Vanuatu', 'New Caledonia', 'Solomon Is.', 'New Zealand', 'Australia'],
  5: ['Turkey'],
  8: ['Cyprus', 'N. Cyprus', 'Fr. S. Antarctic Lands', 'Cyprus U.N. Buffer Zone', 'Akrotiri', 'Dhekelia'],
  9: ['Antarctica'],
};
const kitaAdi = new Map();
for (const [k, adlar] of Object.entries(KITA)) for (const a of adlar) kitaAdi.set(a, Number(k));

// 180. boylamı kesen halkalar (Fiji, Wrangel, Afrika-Avrasya'nın Çukotka ucu…): ardışık köşeler
// arasında >180° sıçrama varsa boylamlar birikimli açılır (halka sürekli olur, 180°'yi aşabilir);
// nokta lon, lon±360 ile sınanır. Açılmazsa çift-tek kuralı o enlemlerde dünyayı saran sahte
// "kara" bantları üretir (Fiji enleminde Pasifik'i geçen nokta çizgisi gibi).
function hazirla(ring) {
  let off = 0;
  let wrap = false;
  const out = [[ring[0][0], ring[0][1]]];
  for (let i = 1; i < ring.length; i++) {
    const d = ring[i][0] - ring[i - 1][0];
    if (d > 180) { off -= 360; wrap = true; } else if (d < -180) { off += 360; wrap = true; }
    out.push([ring[i][0] + off, ring[i][1]]);
  }
  return wrap ? { ring: out, wrap } : { ring, wrap };
}
function inRing(lon, lat, ring) {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i], [xj, yj] = ring[j];
    if ((yi > lat) !== (yj > lat) && lon < ((xj - xi) * (lat - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}
function icinde(lon, lat, h) {
  if (!h.wrap) return inRing(lon, lat, h.ring);
  return inRing(lon, lat, h.ring) || inRing(lon + 360, lat, h.ring) || inRing(lon - 360, lat, h.ring);
}

// ---------------------------------------------------------------------------
//  L2 küre (110 m): önceki oturumdaki davranış aynen
// ---------------------------------------------------------------------------
function kureKipi(step, kapak = 0) {
  const topo = atlas('land-110m');
  const land = feature(topo, topo.objects.land);
  const polys = [];
  for (const f of land.features ?? [land]) {
    const g = f.geometry;
    const list = g.type === 'Polygon' ? [g.coordinates] : g.coordinates;
    for (const p of list) polys.push(p.map(hazirla));
  }
  function isLand(lon, lat) {
    for (const p of polys) {
      if (icinde(lon, lat, p[0])) {
        let hole = false;
        for (let h = 1; h < p.length; h++) if (icinde(lon, lat, p[h])) { hole = true; break; }
        if (!hole) return true;
      }
    }
    return false;
  }
  // Kıta: noktanın içinde bulunduğu ülkenin kıtası (sınır/ad ÇİZİLMEZ, yalnız varış parıltısı için).
  // Türkiye vurgusu YALNIZ Türkiye sınırı içindeki noktalar (kutu değil). Kıbrıs nötr.
  const ctopo = atlas('countries-110m');
  const countries = feature(ctopo, ctopo.objects.countries).features;
  const ulkeler = countries.map((f) => {
    const g = f.geometry;
    const list = (g.type === 'Polygon' ? [g.coordinates] : g.coordinates).map((p) => p.map(hazirla));
    let x0 = 180, y0 = 90, x1 = -180, y1 = -90;
    let wrap = false;
    for (const p of list) {
      wrap = wrap || p[0].wrap;
      for (const [x, y] of p[0].ring) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
    }
    const ad = f.properties.name;
    if (!kitaAdi.has(ad)) console.warn('kıtası tanımsız ülke:', ad);
    return { ad, list, bbox: wrap ? null : [x0, y0, x1, y1], ylat: [y0, y1] };
  });
  function ulke(lon, lat) {
    for (const u of ulkeler) {
      if (lat < u.ylat[0] || lat > u.ylat[1]) continue;
      if (u.bbox) {
        const [x0, , x1] = u.bbox;
        if (lon < x0 || lon > x1) continue;
      }
      for (const p of u.list) {
        if (icinde(lon, lat, p[0])) {
          let hole = false;
          for (let h = 1; h < p.length; h++) if (icinde(lon, lat, p[h])) { hole = true; break; }
          if (!hole) return u.ad;
        }
      }
    }
    return null;
  }
  let ulkesiz = 0;
  function continent(lat, lon) {
    if (lat < -60) return 9;
    const ad = ulke(lon, lat);
    if (ad === 'Russia') return lon >= 60 || lon < -100 ? 1 : 0; // Ural ayrımı (Çukotka 180° ötesinde)
    if (ad === 'France' && lon < -30) return 3; // Fransız Guyanası
    if (ad && kitaAdi.has(ad)) return kitaAdi.get(ad);
    // ülke poligonları ile kara poligonu arasındaki kıyı farkı: kaba kural (asla 5 = Türkiye döndürmez)
    ulkesiz++;
    return kabaKita(lat, lon);
  }
  const out = [];
  for (let lat = -58; lat <= 82; lat += step) {
    // enlemle seyrekleşen boylam aralığı → küre üstünde eşit yoğunluk
    const dlon = step / Math.max(0.25, Math.cos((lat * Math.PI) / 180));
    for (let lon = -180; lon < 180; lon += dlon) {
      if (kapak > 0 && acisalUzaklik(lat, lon, 38.42, 27.14) > kapak) continue;
      if (isLand(lon, lat)) {
        const k = continent(lat, lon);
        if (k !== 9) out.push([+lat.toFixed(3), +lon.toFixed(3), k]);
      }
    }
  }
  yaz(out, ulkesiz);
}

function acisalUzaklik(la1, lo1, la2, lo2) {
  const r = Math.PI / 180;
  const c = Math.sin(la1 * r) * Math.sin(la2 * r) + Math.cos(la1 * r) * Math.cos(la2 * r) * Math.cos((lo1 - lo2) * r);
  return (Math.acos(Math.max(-1, Math.min(1, c))) * 180) / Math.PI;
}

function kabaKita(lat, lon) {
  if (lon <= -25) return 3;
  if (lat < -10 && lon >= 110) return 4;
  if (lon >= -25 && lon <= 52 && lat < 30 && !(lon > 43 && lat > 12)) return 2;
  if (lon < 40 && lat >= 36) return 0;
  return 8;
}

function yaz(out, ulkesiz) {
  writeFileSync(cikis, JSON.stringify(out));
  console.log('nokta', out.length, 'kıta sayıları (0..5, 8)', [0, 1, 2, 3, 4, 5, 8].map((k) => out.filter((p) => p[2] === k).length).join(' '),
    'ülkesiz', ulkesiz);
}

// ---------------------------------------------------------------------------
//  Bölge (L0, 10 m) ve L1 (50 m): satır tarama maskeleri
// ---------------------------------------------------------------------------
/** Halkalar (çokgen dış + iç halkalar, çift-tek kuralı) → her ızgara satırı için sıralı kesişim boylamları. */
function satirKesisimleri(halkalar, lat0, dlat, n) {
  const xs = Array.from({ length: n }, () => []);
  for (const ring of halkalar) {
    for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
      let [x1, y1] = ring[j];
      let [x2, y2] = ring[i];
      if (y1 === y2) continue;
      if (y1 > y2) { [x1, y1, x2, y2] = [x2, y2, x1, y1]; }
      // lat_r = lat0 + r*dlat, y1 <= lat_r < y2
      const r0 = Math.max(0, Math.ceil((y1 - lat0) / dlat));
      const r1 = Math.min(n - 1, Math.ceil((y2 - lat0) / dlat) - 1);
      for (let r = r0; r <= r1; r++) {
        const lat = lat0 + r * dlat;
        xs[r].push(x1 + ((x2 - x1) * (lat - y1)) / (y2 - y1));
      }
    }
  }
  for (const a of xs) a.sort((p, q) => p - q);
  return xs;
}
function icindeSatir(xs, lon) {
  // lon'dan küçük kesişim sayısı tek ise içeride
  let lo = 0, hi = xs.length;
  while (lo < hi) {
    const m = (lo + hi) >> 1;
    if (xs[m] < lon) lo = m + 1; else hi = m;
  }
  return (lo & 1) === 1;
}
function pencereHalkalari(feat, pen) {
  const g = feat.geometry;
  const list = g.type === 'Polygon' ? [g.coordinates] : g.coordinates;
  const out = [];
  for (const poly of list) {
    for (const ring of poly) {
      let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
      for (const [x, y] of ring) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
      if (x1 < pen.lon0 || x0 > pen.lon1 || y1 < pen.lat0 || y0 > pen.lat1) continue;
      out.push(ring);
    }
  }
  return out;
}

function bolgeKipi(tur) {
  // pencere ve ızgara: bolge = 1,25 km, l1 = 0,09° ≈ 10 km. Satırlar altıgen düzende (tek satırlar yarım adım kayık).
  const P = tur === 'bolge'
    ? { lat0: 36.3, lat1: 40.0, lon0: 24.5, lon1: 29.7, dlat: 1.25 / 111.19, km: 1.25, kara: 'land-10m', ulke: 'countries-10m' }
    : { lat0: 28.0, lat1: 48.0, lon0: 12.0, lon1: 48.0, dlat: 0.09, km: 10.0, kara: 'land-50m', ulke: 'countries-50m' };
  const n = Math.floor((P.lat1 - P.lat0) / P.dlat) + 1;
  const kt = atlas(P.kara);
  const kara = feature(kt, kt.objects.land);
  const karaH = [];
  for (const f of kara.features ?? [kara]) karaH.push(...pencereHalkalari(f, P));
  const karaX = satirKesisimleri(karaH, P.lat0, P.dlat, n);
  const ct = atlas(P.ulke);
  const ulkeler = [];
  for (const f of feature(ct, ct.objects.countries).features) {
    const hal = pencereHalkalari(f, P);
    if (!hal.length) continue;
    const ad = f.properties.name;
    if (!kitaAdi.has(ad)) console.warn('kıtası tanımsız ülke:', ad);
    ulkeler.push({ ad, xs: satirKesisimleri(hal, P.lat0, P.dlat, n) });
  }
  console.log(tur, 'satır', n, 'kara halkası', karaH.length, 'ülke', ulkeler.map((u) => u.ad).join(','));
  const out = [];
  let ulkesiz = 0;
  for (let r = 0; r < n; r++) {
    const lat = P.lat0 + r * P.dlat;
    const dlon = P.km / (111.32 * Math.cos((lat * Math.PI) / 180));
    const ofs = (r & 1) ? dlon / 2 : 0;
    for (let lon = P.lon0 + ofs; lon <= P.lon1; lon += dlon) {
      if (!icindeSatir(karaX[r], lon)) continue;
      let k = null;
      let ad = null;
      for (const u of ulkeler) if (icindeSatir(u.xs[r], lon)) { ad = u.ad; break; }
      if (ad === 'Russia') k = lon >= 60 ? 1 : 0;
      else if (ad && kitaAdi.has(ad)) k = kitaAdi.get(ad);
      if (k === null) { ulkesiz++; k = kabaKita(lat, lon); }
      if (k === 9) continue;
      out.push([+lat.toFixed(4), +lon.toFixed(4), k]);
    }
  }
  yaz(out, ulkesiz);
}

if (mod === 'bolge' || mod === 'l1') bolgeKipi(mod);
else if (mod === 'l15') kureKipi(0.4, 82);
else kureKipi(Number(mod));
