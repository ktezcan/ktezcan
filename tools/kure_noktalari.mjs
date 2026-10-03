// Dünya kara noktaları (world-atlas land-110m, Natural Earth — kamu malı) → ızgara noktaları + kıta kimliği.
// Ülke sınırı/ülke adı YOK (yalnız kara). Çıktı: JSON [[lat, lon, kita], ...]
// kita: 0 Avrupa, 1 Asya, 2 Afrika, 3 Amerika, 4 Okyanusya, 5 Türkiye (kaynak), 9 diğer (Antarktika vb. — atlanır)
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
  for (const p of list) polys.push(p);
}
function inRing(lon, lat, ring) {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i], [xj, yj] = ring[j];
    if ((yi > lat) !== (yj > lat) && lon < ((xj - xi) * (lat - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}
function isLand(lon, lat) {
  for (const p of polys) {
    if (inRing(lon, lat, p[0])) {
      let hole = false;
      for (let h = 1; h < p.length; h++) if (inRing(lon, lat, p[h])) { hole = true; break; }
      if (!hole) return true;
    }
  }
  return false;
}
function continent(lat, lon) {
  if (lat < -60) return 9;
  if (lat >= 35.8 && lat <= 42.2 && lon >= 26 && lon <= 44.8) return 5; // Türkiye bölgesi (yaklaşık kutu)
  if (lon <= -25) return 3;
  if (lat < -10 && lon >= 110) return 4;
  if (lat < 0 && lon >= 150) return 4;
  if (lon >= -25 && lon <= 52 && lat < 37 && !(lon > 34 && lat > 12)) return 2;
  if (lon >= -25 && lon < 45 && lat >= 35) return lon > 26 && lat < 42 ? 1 : 0;
  if (lon >= 26 && lat >= 42 && lon < 60 && lat > 45) return 0;
  return 1;
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
console.log('nokta', out.length, 'kıta sayıları', [0, 1, 2, 3, 4, 5].map((k) => out.filter((p) => p[2] === k).length).join(' '));
