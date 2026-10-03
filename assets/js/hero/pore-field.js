/**
 * Gözenek alanı üretimi — gazbetonun hücresel iç yapısının soyut modeli.
 * Three.js'ten bağımsızdır; yalnızca typed array üretir.
 *
 * 1) Farklı çaplarda, birbirine değmeyen "hava gözenekleri" yerleştirilir
 *    (azalan yarıçaplı rastgele yerleştirme → doğal köpük dağılımı).
 * 2) Parçacıklar gözenek çeperlerine dizilir. Nokta aralığı kameraya
 *    uzaklıkla büyür: bütçe, ekranda görünen yere harcanır.
 * 3) Gözenekler arasına seyrek "matris tanesi" parçacıkları serpilir.
 * 4) Dizi karıştırılır: drawRange ile parçacık sayısı azaltıldığında
 *    yoğunluk her yerde eşit oranda düşer (çalışma anı kalite ayarı).
 */

/** Tohumlu, hızlı sözde-rastgele üreteç (her açılışta aynı kompozisyon). */
export function mulberry32(seed) {
  let a = seed >>> 0;
  return function rand() {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const TAU = Math.PI * 2;

/**
 * @param {object} o
 * @param {{zNear:number, zFar:number, halfNear:number, halfFar:number}} o.region
 *        Kameranın düzlemde gördüğü yamuk alan (dünya birimi, zNear > zFar)
 * @param {number[]} o.eye       Kamera konumu [x, y, z]
 * @param {number}   o.budget    Toplam parçacık bütçesi
 * @param {number}   o.attempts  Gözenek yerleştirme deneme sayısı
 * @param {(u:number, v:number, out:{x:number,z:number}) => boolean} o.unproject
 *        Ekran koordinatını (0..1) düzleme izdüşürür
 * @param {number[]} o.focus     Açılış animasyonunun yayıldığı merkez [x, z]
 * @param {number}   o.seed
 */
export function buildPoreField(o) {
  const rand = mulberry32(o.seed);
  const { zNear, zFar, halfNear, halfFar } = o.region;
  const depth = zNear - zFar;
  const halfAt = (z) => halfNear + (halfFar - halfNear) * ((zNear - z) / depth);
  const [ex, ey, ez] = o.eye;
  const distTo = (x, z) => Math.sqrt((x - ex) * (x - ex) + ey * ey + (z - ez) * (z - ez));
  const dRef = distTo(0, zNear - 2);

  // ---------------------------------------------------------------
  // 1) Gözenek yerleşimi
  // ---------------------------------------------------------------
  const rMax = 0.95;
  const rMin = 0.12;
  const gap = 0.07;
  // Uzak bölgede gözenekler biraz büyür: ekranda küçülen alan için
  // parçacık israf edilmez, perspektif derinliği de güçlenir.
  const growAt = (z) => 1 + Math.max(0, zNear - z - 7) * 0.055;

  const cell = 1.0;
  const gx0 = -halfFar - 2;
  const gz0 = zFar - 2;
  const gCols = Math.ceil((halfFar * 2 + 4) / cell);
  const gRows = Math.ceil((depth + 4) / cell);
  const grid = Array.from({ length: gCols * gRows }, () => []);

  const px = [];
  const pz = [];
  const pr = [];

  const cellOf = (x, z) => [Math.floor((x - gx0) / cell), Math.floor((z - gz0) / cell)];

  const fits = (x, z, r) => {
    const [ci, cj] = cellOf(x, z);
    const reach = Math.ceil((r + gap) / cell);
    for (let j = cj - reach; j <= cj + reach; j++) {
      if (j < 0 || j >= gRows) continue;
      for (let i = ci - reach; i <= ci + reach; i++) {
        if (i < 0 || i >= gCols) continue;
        const list = grid[j * gCols + i];
        for (let k = 0; k < list.length; k++) {
          const q = list[k];
          const dx = px[q] - x;
          const dz = pz[q] - z;
          const min = pr[q] + r + gap;
          if (dx * dx + dz * dz < min * min) return false;
        }
      }
    }
    return true;
  };

  const insert = (x, z, r) => {
    const id = px.length;
    px.push(x);
    pz.push(z);
    pr.push(r);
    // Gözenek, kapladığı tüm hücrelere kaydedilir → sorgu yalnızca komşu hücrelere bakar.
    const [i0, j0] = cellOf(x - r, z - r);
    const [i1, j1] = cellOf(x + r, z + r);
    for (let j = Math.max(0, j0); j <= Math.min(gRows - 1, j1); j++) {
      for (let i = Math.max(0, i0); i <= Math.min(gCols - 1, i1); i++) grid[j * gCols + i].push(id);
    }
  };

  const attempts = o.attempts;
  for (let a = 0; a < attempts; a++) {
    // Yamuk içinde düzgün dağılımlı aday nokta
    let z;
    do {
      z = zFar + rand() * depth;
    } while (rand() > halfAt(z) / halfFar);
    const x = (rand() * 2 - 1) * halfAt(z);

    // Büyükten küçüğe azalan yarıçap programı (+ hafif sapma)
    const t = a / attempts;
    const base = rMax * Math.pow(rMin / rMax, Math.pow(t, 0.55));
    const r = base * (0.82 + rand() * 0.36) * growAt(z);
    if (fits(x, z, r)) insert(x, z, r);
  }

  const poreCount = px.length;

  // ---------------------------------------------------------------
  // 2) Çeper parçacık bütçesi (ekranda görünen boyuta göre)
  // ---------------------------------------------------------------
  const ringBudget = Math.round(o.budget * 0.86);
  const weights = new Float32Array(poreCount);
  let wSum = 0;
  for (let p = 0; p < poreCount; p++) {
    const w = (TAU * pr[p] * dRef) / distTo(px[p], pz[p]);
    weights[p] = w;
    wSum += w;
  }
  const minPts = 5;
  let spacing = wSum / Math.max(1, ringBudget - poreCount * 1.5);

  const counts = new Uint16Array(poreCount);
  let ringTotal = 0;
  for (let p = 0; p < poreCount; p++) {
    const n = Math.max(minPts, Math.min(160, Math.round(weights[p] / spacing)));
    counts[p] = n;
    ringTotal += n;
  }
  // Bütçeyi aşarsa tek geçişte orantılı düzelt
  if (ringTotal > ringBudget) {
    const f = ringBudget / ringTotal;
    ringTotal = 0;
    for (let p = 0; p < poreCount; p++) {
      counts[p] = Math.max(minPts, Math.round(counts[p] * f));
      ringTotal += counts[p];
    }
  }

  const dustTarget = Math.max(0, o.budget - ringTotal);
  const total = ringTotal + dustTarget;

  const position = new Float32Array(total * 3);
  const offset = new Float32Array(total * 2);
  const seed = new Float32Array(total * 4);

  // Karıştırılmış yazma sırası (Fisher–Yates)
  const order = new Uint32Array(total);
  for (let i = 0; i < total; i++) order[i] = i;
  for (let i = total - 1; i > 0; i--) {
    const j = Math.floor(rand() * (i + 1));
    const tmp = order[i];
    order[i] = order[j];
    order[j] = tmp;
  }

  // Açılış animasyonu: odaktan dışa doğru yayılan gecikme
  const [fx, fz] = o.focus;
  const maxFocus = Math.hypot(halfFar + Math.abs(fx), depth);
  const staggerAt = (x, z) => Math.min(1, (Math.hypot(x - fx, z - fz) / maxFocus) * 1.35);

  let w = 0;
  const write = (cx, cz, ox, oz, s0, s1, kind, s3) => {
    const k = order[w++];
    position[k * 3] = cx;
    position[k * 3 + 1] = 0;
    position[k * 3 + 2] = cz;
    offset[k * 2] = ox;
    offset[k * 2 + 1] = oz;
    seed[k * 4] = s0;
    seed[k * 4 + 1] = s1;
    seed[k * 4 + 2] = kind;
    seed[k * 4 + 3] = s3;
  };

  for (let p = 0; p < poreCount; p++) {
    const n = counts[p];
    const r = pr[p];
    const phase = rand() * TAU;
    const stagger = Math.min(1, staggerAt(px[p], pz[p]) * 0.85 + rand() * 0.15);
    const poreRnd = rand();
    for (let k = 0; k < n; k++) {
      const ang = phase + (k / n) * TAU + (rand() - 0.5) * (0.35 / n);
      const rr = r * (0.97 + rand() * 0.06);
      // seed: x = gözenek ritmi (aynı gözenekteki noktalar birlikte nefes alır)
      write(px[p], pz[p], Math.cos(ang) * rr, Math.sin(ang) * rr, poreRnd, 0.85 + rand() * 0.45, 0, stagger);
    }
  }

  // ---------------------------------------------------------------
  // 3) Matris taneleri — ekran uzayında düzgün dağılım, gözenek içine düşmez
  // ---------------------------------------------------------------
  const hit = { x: 0, z: 0 };
  const insidePore = (x, z) => {
    const [ci, cj] = cellOf(x, z);
    if (ci < 0 || cj < 0 || ci >= gCols || cj >= gRows) return false;
    const list = grid[cj * gCols + ci];
    for (let k = 0; k < list.length; k++) {
      const q = list[k];
      const dx = px[q] - x;
      const dz = pz[q] - z;
      const lim = pr[q] - 0.04;
      if (dx * dx + dz * dz < lim * lim) return true;
    }
    return false;
  };

  for (let d = 0; d < dustTarget; d++) {
    let placed = false;
    for (let tries = 0; tries < 6 && !placed; tries++) {
      if (!o.unproject(-0.06 + rand() * 1.12, -0.04 + rand() * 1.08, hit)) continue;
      if (hit.z > zNear || hit.z < zFar || Math.abs(hit.x) > halfAt(hit.z)) continue;
      if (insidePore(hit.x, hit.z) && tries < 5) continue;
      placed = true;
    }
    if (!placed) {
      // Son çare: yamuk içinde rastgele bir nokta
      hit.z = zFar + rand() * depth;
      hit.x = (rand() * 2 - 1) * halfAt(hit.z);
    }
    write(hit.x, hit.z, 0, 0, rand(), 0.45 + rand() * 0.4, 1, staggerAt(hit.x, hit.z));
  }

  return { count: total, poreCount, position, offset, seed };
}

/**
 * Havada yükselen "gaz kabarcıkları" — derinlik hissi için ön plan katmanı.
 * @returns {{count:number, position:Float32Array, seed:Float32Array}}
 */
export function buildMotes({ count, seed, spanX = 8, zNear = 6.5, zFar = -9, height = 5.4 }) {
  const rand = mulberry32(seed * 7 + 3);
  const position = new Float32Array(count * 3);
  const data = new Float32Array(count * 4);
  for (let i = 0; i < count; i++) {
    const z = zFar + rand() * (zNear - zFar);
    const spread = spanX * (0.55 + 0.45 * ((zNear - z) / (zNear - zFar)));
    position[i * 3] = (rand() * 2 - 1) * spread;
    position[i * 3 + 1] = rand() * height;
    position[i * 3 + 2] = z;
    data[i * 4] = rand(); // faz
    data[i * 4 + 1] = rand(); // yükselme hızı
    data[i * 4 + 2] = 0.6 + rand() * 1.1; // boyut
    data[i * 4 + 3] = rand(); // salınım
  }
  return { count, position, seed: data };
}
