// Dünya kara noktaları (world-atlas land-110m, Natural Earth — kamu malı) → ızgara noktaları + kıta kimliği.
// Ülke sınırı/ülke adı YOK (yalnız kara). Çıktı: JSON [[lat, lon, kita], ...]
// kita: 0 Avrupa, 1 Asya, 2 Afrika, 3 Amerika, 4 Okyanusya, 5 Türkiye (kaynak), 8 nötr (parlamaz), 9 Antarktika (atlanır)
import { readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const base = process.argv[2];
const topo = JSON.parse(readFileSync(`${base}/node_modules/world-atlas/land-110m.json`, 'utf8'));
const { feature } = require(`${base}/node_modules/topojson-client`);
const land = feature(topo, topo.objects.land);
const polys = [];
for (const f of land.features ?? [land]) {
  const g = f.geometry;
  const list = g.type === 'Polygon' ? [g.coordinates] : g.coordinates;
  for (const p of list) polys.push(p.map(hazirla));
}
function inRing(lon, lat, ring) {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i], [xj, yj] = ring[j];
    if ((yi > lat) !== (yj > lat) && lon < ((xj - xi) * (lat - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}
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
function icinde(lon, lat, h) {
  if (!h.wrap) return inRing(lon, lat, h.ring);
  return inRing(lon, lat, h.ring) || inRing(lon + 360, lat, h.ring) || inRing(lon - 360, lat, h.ring);
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
// Kıta: noktanın içinde bulunduğu ülkenin kıtası (Natural Earth countries-110m; sınır/ad ÇİZİLMEZ,
// yalnız varış parıltısı için). Türkiye vurgusu YALNIZ Türkiye sınırı içindeki noktalar (kutu değil:
// kutu komşu ülkelerden toprak kapsar → yanlış/siyasi okunur). Kıbrıs nötr (hiçbir gruba parlamaz).
const ctopo = JSON.parse(readFileSync(`${base}/node_modules/world-atlas/countries-110m.json`, 'utf8'));
const countries = feature(ctopo, ctopo.objects.countries).features;
const KITA = {
  0: ['Norway', 'France', 'Sweden', 'Belarus', 'Ukraine', 'Poland', 'Austria', 'Hungary', 'Moldova', 'Romania', 'Lithuania',
    'Latvia', 'Estonia', 'Germany', 'Bulgaria', 'Greece', 'Albania', 'Croatia', 'Switzerland', 'Luxembourg', 'Belgium',
    'Netherlands', 'Portugal', 'Spain', 'Ireland', 'Italy', 'Denmark', 'United Kingdom', 'Iceland', 'Slovenia', 'Finland',
    'Slovakia', 'Czechia', 'Bosnia and Herz.', 'Macedonia', 'Serbia', 'Montenegro', 'Kosovo', 'Russia'],
  1: ['Kazakhstan', 'Uzbekistan', 'Indonesia', 'Timor-Leste', 'Israel', 'Lebanon', 'Palestine', 'Jordan', 'United Arab Emirates',
    'Qatar', 'Kuwait', 'Iraq', 'Oman', 'Cambodia', 'Thailand', 'Laos', 'Myanmar', 'Vietnam', 'North Korea', 'South Korea',
    'Mongolia', 'India', 'Bangladesh', 'Bhutan', 'Nepal', 'Pakistan', 'Afghanistan', 'Tajikistan', 'Kyrgyzstan', 'Turkmenistan',
    'Iran', 'Syria', 'Armenia', 'Sri Lanka', 'China', 'Taiwan', 'Azerbaijan', 'Georgia', 'Philippines', 'Malaysia', 'Brunei',
    'Japan', 'Yemen', 'Saudi Arabia'],
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
  8: ['Cyprus', 'N. Cyprus', 'Fr. S. Antarctic Lands'],
  9: ['Antarctica'],
};
const kitaAdi = new Map();
for (const [k, adlar] of Object.entries(KITA)) for (const a of adlar) kitaAdi.set(a, Number(k));
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
  if (lon <= -25) return 3;
  if (lat < -10 && lon >= 110) return 4;
  if (lon >= -25 && lon <= 52 && lat < 30 && !(lon > 43 && lat > 12)) return 2;
  if (lon < 40 && lat >= 36) return 0;
  return 8;
}
const step = Number(process.argv[3] || 1.25);
const out = [];
for (let lat = -58; lat <= 82; lat += step) {
  // enlemle seyrekleşen boylam aralığı → küre üstünde eşit yoğunluk
  const dlon = step / Math.max(0.25, Math.cos((lat * Math.PI) / 180));
  for (let lon = -180; lon < 180; lon += dlon) {
    if (isLand(lon, lat)) {
      const k = continent(lat, lon);
      if (k !== 9) out.push([+lat.toFixed(3), +lon.toFixed(3), k]);
    }
  }
}
writeFileSync(process.argv[4], JSON.stringify(out));
console.log('nokta', out.length, 'kıta sayıları (0..5, 8)', [0, 1, 2, 3, 4, 5, 8].map((k) => out.filter((p) => p[2] === k).length).join(' '), 'ülkesiz', ulkesiz);
