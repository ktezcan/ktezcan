// Başsız Chromium sınaması: konsol hatası, kaydırma, rAF'ın boşta durması, 7 parçalı akışın ekran görüntüleri,
// hızlı ileri/geri sarmada kare hızı (fps), kare belleği (çözülmüş bitmap MB + tarayıcı süreç RSS),
// kanvas DPR'ı, backdrop-filter / mix-blend taraması, depolama kullanımı.
// Kullanım: node tools/sinama.mjs <çıktı klasörü> [file] [--site <klasör>] [--kisa]
//   file    : http yerine file:// ile aç (çift tıkla açılışı)
//   --site  : sınanacak site klasörü (varsayılan giris-hikaye/; EGE_SITE ile de verilebilir)
//   --kisa  : yalnız masaüstü, az ekran görüntüsü
//   --sarma : yalnız masaüstü, plan saniyelerine gitmeden hızlı sarma (fps/bellek) testi
// Çıkış kodu: 0 = tüm denetimler geçti, 1 = en az biri başarısız.
import { createServer } from 'node:http';
import { existsSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { loadavg } from 'node:os';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { extname, join, dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const argv = process.argv.slice(2);
const bayrak = (ad) => argv.includes(ad);
const siteIdx = argv.indexOf('--site');
const siteArg = siteIdx >= 0 ? argv[siteIdx + 1] : undefined;
const pozisyonel = argv.filter((a, i) => !a.startsWith('--') && (siteIdx < 0 || i !== siteIdx + 1));
const kok = resolve(siteArg || process.env.EGE_SITE || join(dirname(fileURLToPath(import.meta.url)), '..', 'giris-hikaye'));
const out = pozisyonel[0] || 'sinama';
const fileMode = pozisyonel[1] === 'file';
const sarmaYalniz = bayrak('--sarma');
const kisa = bayrak('--kisa') || sarmaYalniz;
await mkdir(out, { recursive: true });

const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.mp4': 'video/mp4', '.woff2': 'font/woff2', '.svg': 'image/svg+xml' };
const server = createServer(async (req, res) => {
  const p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  try {
    const f = p === '/' ? '/index.html' : p;
    const body = await readFile(join(kok, f));
    res.writeHead(200, { 'content-type': TYPES[extname(f)] || 'application/octet-stream' });
    res.end(body);
  } catch {
    res.writeHead(404);
    res.end('yok');
  }
}).listen(0);
const base = fileMode ? pathToFileURL(join(kok, 'index.html')).href : `http://127.0.0.1:${server.address().port}/`;

// Playwright sürümü kurulu tarayıcıyla eşleşmezse hazır Chromium'u kullan (CHROME_YOLU ile değiştirilebilir)
const chromeYolu = process.env.CHROME_YOLU || (existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined);
const browser = await chromium.launch({ executablePath: chromeYolu, args: ['--autoplay-policy=no-user-gesture-required'] });
const sonuc = {};
const basarisiz = [];
const uyari = [];

/** Bu betiğin alt süreçleri (Chromium ve çocukları) toplam RSS, MB. */
function surecRss() {
  try {
    const satirlar = execSync('ps -eo pid=,ppid=,rss=', { encoding: 'utf8' }).trim().split('\n');
    const cocuk = new Map();
    const rss = new Map();
    for (const s of satirlar) {
      const [pid, ppid, r] = s.trim().split(/\s+/).map(Number);
      rss.set(pid, r);
      if (!cocuk.has(ppid)) cocuk.set(ppid, []);
      cocuk.get(ppid).push(pid);
    }
    let top = 0;
    const yigin = [...(cocuk.get(process.pid) || [])];
    while (yigin.length) {
      const p = yigin.pop();
      top += rss.get(p) || 0;
      yigin.push(...(cocuk.get(p) || []));
    }
    return top / 1024;
  } catch {
    return 0;
  }
}

/** Plan saniyeleri (docs/plan): 7 parçalı akışın sınır ve orta noktaları, dikişin iki yanı. */
const SANIYELER = [0.5, 12, 24, 31.5, 32.5, 45, 62, 69.5, 70.5, 80, 89.5, 90.5, 97, 103.5, 104.5, 112, 119.5, 120.5, 128, 135.5, 136.5, 141, 145.8];
const SANIYELER_KISA = [0.5, 31.5, 32.5, 50, 100, 112, 128, 141, 145.8];
/** Parça dikişleri (saniye): iki yanındaki görüntü aynı kare olmalı (son kare = sonraki ilk kare), motor araya boşluk/parıltı koymamalı. */
const DIKISLER = [32, 70, 90, 104, 120, 136];
const DIKIS_ESIK = 12; // 32×18 küçültülmüş RGB ortalama mutlak fark (0..255); dikişsiz (farklı çekim) ≥ 30, yer tutucuda komşu kare farkı ≈ 7

async function oturum(ad, viewport, { dsf = 1, extra = '', tamTur = true } = {}) {
  const az = extra.includes('az');
  const ctx = await browser.newContext({ viewport, deviceScaleFactor: dsf, reducedMotion: az ? 'reduce' : 'no-preference' });
  const page = await ctx.newPage();
  const hatalar = [];
  // 'GPU stall due to ReadPixels': başsız Chromium'un yazılımsal birleştirmesi her WebGL karesini geri okur
  // (en basit WebGL sayfasında da çıkar) → sayfa hatası değil, raporlanmaz
  page.on('console', (m) => {
    if ((m.type() === 'error' || m.type() === 'warning') && !/GPU stall due to ReadPixels/.test(m.text())) hatalar.push(`${m.type()}: ${m.text()}`);
  });
  page.on('pageerror', (e) => hatalar.push(`pageerror: ${e.message}`));
  const dis = [];
  page.on('request', (r) => {
    const u = r.url();
    if (!u.startsWith('data:') && !u.startsWith('blob:') && !u.startsWith(base.startsWith('file:') ? 'file:' : base)) dis.push(u);
  });
  const rss0 = surecRss();
  let rssMax = rss0;
  const zamanlayici = setInterval(() => {
    rssMax = Math.max(rssMax, surecRss());
  }, 400);

  await page.goto(base + '?debug' + (extra ? '&' + extra : ''), { waitUntil: 'load' });
  await page.waitForFunction(() => window.__ege, null, { timeout: 15000 });

  /** Yükleme kuyruğu boşalıp döngü duruncaya dek (en çok `ms`) bekle. */
  async function hazirBekle(ms = 15000) {
    const t0 = Date.now();
    let art = 0;
    while (Date.now() - t0 < ms) {
      const h = await page.evaluate(() => window.__ege.hazir());
      art = h ? art + 1 : 0;
      if (art >= 3) return true;
      await page.waitForTimeout(80);
    }
    return false;
  }
  const bellekler = [];
  async function belleklerEkle(etiket) {
    const b = await page.evaluate(() => window.__ege.bellek());
    bellekler.push({ etiket, adet: b.adet, mb: b.mb });
    return b;
  }

  // ilk boyama: s0 kanvasına ilk kare çizilene dek (poster ile gelen boyama sayılmaz)
  const ilkT0 = Date.now();
  const ilkBoyamaOk = await page.waitForFunction(() => document.querySelector('[data-sahne="s0"].is-hazir'), null, { timeout: 15000 }).then(() => true, () => false);
  const ilkBoyamaMs = Date.now() - ilkT0;
  await hazirBekle();
  const acilisBellek = await page.evaluate(() => window.__ege.bellek());
  const shots = [];
  async function shot(name) {
    const f = join(out, `${ad}_${name}.png`);
    await page.screenshot({ path: f });
    shots.push(f);
  }
  await shot('00_acilis');
  const plan = await page.evaluate(() => ({ bas: window.__ege.bas, toplamVh: window.__ege.toplamVh, saniye: window.__ege.ortak.toplamSaniye }));
  const vh = viewport.height;

  // 1) 7 parçalı akış: plan saniyelerine git, kare belleği ve görüntü al
  const liste = az || sarmaYalniz ? [] : kisa ? SANIYELER_KISA : tamTur ? SANIYELER : SANIYELER_KISA;
  for (const t of liste) {
    await page.evaluate((s) => window.__ege.ortak.saniyeyeGit(s), t);
    await page.waitForTimeout(120);
    await hazirBekle(12000);
    await page.waitForTimeout(az ? 100 : 900); // vuruş geçişleri (CSS)
    await belleklerEkle(`t=${t}`);
    await shot(`t${String(Math.round(t * 10)).padStart(4, '0')}`);
  }

  // 1b) dikişler: önceki parçanın son karesi ile sonrakinin ilk karesi aynı görüntü olmalı (kanvas özeti karşılaştırılır)
  const dikis = [];
  if (!az) {
    const ozet = () => {
      const s = window.__ege.sahneler.find((x) => x.visible && x.canvas);
      if (!s) return { hata: 'görünen kanvas yok' };
      try {
        const c = document.createElement('canvas');
        c.width = 32;
        c.height = 18;
        const g = c.getContext('2d');
        g.drawImage(s.canvas, 0, 0, 32, 18);
        return { id: s.id, v: Array.from(g.getImageData(0, 0, 32, 18).data) };
      } catch (e) {
        return { hata: String(e.message || e) };
      }
    };
    for (const t of DIKISLER) {
      const ornek = [];
      for (const d of [-0.004, 0.004]) { // dikişe çok yakın: yoğun kare aralarındaki doğrusal erime farkı yok sayılabilir
        await page.evaluate((x) => window.__ege.ortak.saniyeyeGit(x), t + d);
        await page.waitForTimeout(150);
        await hazirBekle(8000);
        await page.waitForTimeout(250);
        ornek.push(await page.evaluate(ozet));
      }
      const [A, B] = ornek;
      if (A.hata || B.hata) dikis.push({ t, atlandi: A.hata || B.hata });
      else {
        let top = 0;
        for (let i = 0; i < A.v.length; i += 4) top += Math.abs(A.v[i] - B.v[i]) + Math.abs(A.v[i + 1] - B.v[i + 1]) + Math.abs(A.v[i + 2] - B.v[i + 2]);
        dikis.push({ t, once: A.id, sonra: B.id, fark: +(top / (A.v.length / 4) / 3).toFixed(2) });
      }
    }
  }

  // 2) rAF boşta durmalı (kaydırma bitti → döngü duruyor)
  await page.waitForTimeout(1200);
  const bosta = await page.evaluate(() => ({ calisiyor: window.__ege.calisiyor, sayac: window.__ege.raf }));
  await page.waitForTimeout(1500);
  const bosta2 = await page.evaluate(() => window.__ege.raf);

  // 3) hızlı ileri + geri sarma: kare hızı (ölçüm döngüsü sayfanın kendi rAF'ıyla aynı karede koşar) ve bellek
  let hiz = null;
  if (!az) {
    await page.evaluate(() => window.scrollTo(0, 0));
    await hazirBekle(8000);
    hiz = await page.evaluate(async () => {
      const akis = document.querySelector('[data-akis]');
      const top = akis.getBoundingClientRect().top + window.scrollY;
      const vhPx = window.innerHeight;
      const son = top + (window.__ege.toplamVh * vhPx) / 100;
      const faz = (from, to, ms) =>
        new Promise((bit) => {
          const dt = [];
          let enBellek = 0;
          let hizliKare = 0;
          let prev = performance.now();
          const t0 = prev;
          window.__ege.sureler(true);
          const f = (now) => {
            const u = Math.min(1, (now - t0) / ms);
            window.scrollTo(0, from + (to - from) * u);
            dt.push(now - prev);
            if (window.__ege.ortak.cokHizli) hizliKare++;
            prev = now;
            if (dt.length % 10 === 0) enBellek = Math.max(enBellek, window.__ege.bellek().mb);
            if (u < 1) requestAnimationFrame(f);
            else {
              enBellek = Math.max(enBellek, window.__ege.bellek().mb);
              dt.shift();
              const s = [...dt].sort((a, b) => a - b);
              bit({
                kare: dt.length,
                ortFps: +(1000 / (dt.reduce((a, b) => a + b, 0) / dt.length)).toFixed(1),
                p95Ms: +s[Math.floor(s.length * 0.95)].toFixed(1),
                enKotuMs: +s[s.length - 1].toFixed(1),
                yavas33: dt.filter((x) => x > 33.4).length,
                enBellekMB: enBellek,
                hizliOran: +(hizliKare / dt.length).toFixed(2), // kayıtta 'çok hızlı' (pencere yüklemesi duraklatılmış) kare oranı
                betik: window.__ege.sureler(true), // kare başına betik süresi (ms): yavaşlık betikten mi tarayıcıdan mı
              });
            }
          };
          requestAnimationFrame(f);
        });
      // normal: ≈ 80 vh/sn (hızlı ama gerçekçi okuma; s0 → s1 dikişini geçer); ileri/geri: ≈ 320 vh/sn (uç durum, bayrak çevirme)
      const normal = await faz(0, top + (800 * vhPx) / 100, 10000);
      window.scrollTo(0, 0);
      await new Promise((r) => setTimeout(r, 800));
      const ileri = await faz(0, son, 10000);
      const geri = await faz(son, 0, 5000);
      return { normal, ileri, geri };
    });
    await hazirBekle(8000);
    await belleklerEkle('sarma sonrası');
  }

  // 4) kanvas DPR'ı, backdrop-filter / mix-blend taraması, depolama, harici istek
  await page.evaluate(() => window.__ege.ortak.saniyeyeGit(141));
  await hazirBekle(8000);
  const tarama = await page.evaluate(() => {
    const kanvaslar = [...document.querySelectorAll('canvas')].map((c) => {
      const r = c.getBoundingClientRect();
      return { sinif: c.className || c.parentElement.className || 'canvas', px: c.width, css: Math.round(r.width), oran: r.width ? +(c.width / r.width).toFixed(3) : 0, gorunur: r.width > 0 && r.height > 0 };
    });
    const kr = [...document.querySelectorAll('canvas')].map((c) => c.getBoundingClientRect()).filter((r) => r.width > 0 && r.height > 0);
    const kesisir = (r) => kr.some((k) => r.left < k.right && r.right > k.left && r.top < k.bottom && r.bottom > k.top);
    const efektler = [];
    for (const el of document.querySelectorAll('*')) {
      const cs = getComputedStyle(el);
      const bf = cs.backdropFilter || cs.webkitBackdropFilter;
      const mb = cs.mixBlendMode;
      if ((bf && bf !== 'none') || (mb && mb !== 'normal')) {
        const r = el.getBoundingClientRect();
        efektler.push({ el: `${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''}${el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : ''}`, backdrop: bf, mix: mb, kanvasUstunde: r.width > 0 && r.height > 0 && kesisir(r) });
      }
    }
    let ls = -1;
    let ss = -1;
    try {
      ls = localStorage.length;
      ss = sessionStorage.length;
    } catch {}
    return { kanvaslar, efektler, depolama: { localStorage: ls, sessionStorage: ss, cerez: document.cookie.length } };
  });

  // 5) hikâyenin sonrası: rAF hiç çalışmamalı
  await page.evaluate(() => document.getElementById('urunler').scrollIntoView());
  await page.waitForTimeout(1500);
  const sonra1 = await page.evaluate(() => window.__ege.raf);
  await page.mouse.move(200, 200);
  await page.mouse.move(400, 300);
  await page.waitForTimeout(1500);
  const sonra2 = await page.evaluate(() => window.__ege.raf);
  await shot('urunler');

  // 6) dil (not: düğme arayuz.js'te tarayıcı depolamasına yazıyorsa aşağıda uyarı verilir)
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.click('[data-dil-sec="en"]');
  await page.waitForTimeout(600);
  await shot('en');
  const depolamaDilSonrasi = await page.evaluate(() => {
    try {
      return localStorage.length + sessionStorage.length;
    } catch {
      return -1;
    }
  });

  clearInterval(zamanlayici);
  const enBitmap = Math.max(0, ...bellekler.map((b) => b.mb), hiz ? hiz.normal.enBellekMB : 0, hiz ? hiz.ileri.enBellekMB : 0, hiz ? hiz.geri.enBellekMB : 0);
  const r = {
    hatalar,
    disIstek: dis.slice(0, 10),
    plan,
    bostaCalisiyor: bosta.calisiyor,
    bostaKareArtisi: bosta2 - bosta.sayac,
    hikayeSonrasiKareArtisi: sonra2 - sonra1,
    ilkBoyama: { ms: ilkBoyamaMs, tamam: ilkBoyamaOk, acilisBellek: acilisBellek.sahne },
    dikis,
    sarma: hiz,
    enBitmapMB: +enBitmap.toFixed(1),
    surecRssMB: { basta: +rss0.toFixed(0), enFazla: +rssMax.toFixed(0) },
    bellekler: bellekler.map((b) => `${b.etiket}: ${b.adet} kare ${b.mb} MB`),
    kanvaslar: tarama.kanvaslar,
    efektler: tarama.efektler,
    depolama: tarama.depolama,
    depolamaDilSonrasi,
    shots: shots.length,
  };
  sonuc[ad] = r;

  // denetimler
  if (r.hatalar.length) basarisiz.push(`${ad}: konsol hatası/uyarısı ${r.hatalar.length} (${r.hatalar[0].slice(0, 120)})`);
  if (r.disIstek.length) basarisiz.push(`${ad}: harici istek ${r.disIstek[0]}`);
  if (!az) {
    if (r.bostaKareArtisi !== 0) basarisiz.push(`${ad}: rAF boşta durmuyor (${r.bostaKareArtisi} kare)`);
    if (r.hikayeSonrasiKareArtisi !== 0) basarisiz.push(`${ad}: hikâye sonrası rAF çalışıyor (${r.hikayeSonrasiKareArtisi})`);
    if (JSON.stringify(plan.bas) !== JSON.stringify([0, 704, 1540, 1980, 2288, 2640, 2992]) || plan.toplamVh !== 3212) basarisiz.push(`${ad}: akış boyları plana uymuyor ${JSON.stringify(plan)}`);
    if (hiz) {
      // başsız Chromium yazılımsal çizer (her yeni kare "GPU"ya yazılımla yüklenir) ve makine paylaşımlı olabilir:
      // normal hızda 50 fps altı yalnız makine boşken (yük < 3) başarısızlık sayılır; uç hızlı sarmada yalnız uyarı
      const yuk = loadavg()[0];
      if (hiz.normal.ortFps < 50) (yuk < 3 ? basarisiz : uyari).push(`${ad}: normal hızlı sarma ${hiz.normal.ortFps} fps (< 50; makine yükü ${yuk.toFixed(1)})`);
      for (const k of ['ileri', 'geri']) if (hiz[k].ortFps < 50) uyari.push(`${ad}: ${k} uç hızlı sarma (~320 vh/sn) ortalama ${hiz[k].ortFps} fps (< 50; başsız yazılımsal tarayıcıda her yeni kare yüklemesi pahalı)`);
    }
    // açılışta bant genişliği yalnız s0'a gider (komşu yüklemesi s0 ilerlemesi > 0,6 sonrasına ertelenir)
    const baskaYuklu = Object.entries(acilisBellek.sahne).filter(([id, b]) => id !== 's0' && b.adet > 0);
    if (baskaYuklu.length) basarisiz.push(`${ad}: açılışta s0 dışında kare yüklenmiş ${JSON.stringify(baskaYuklu)}`);
    if (acilisBellek.adet > 72) basarisiz.push(`${ad}: açılışta ${acilisBellek.adet} kare çözülü (> 72)`);
    if (!ilkBoyamaOk) basarisiz.push(`${ad}: s0 kanvasına ilk kare çizilmedi`);
    for (const d of dikis) {
      if (d.atlandi) uyari.push(`${ad}: dikiş ${d.t} sn denetimi atlandı (${d.atlandi})`);
      else if (d.fark > DIKIS_ESIK) basarisiz.push(`${ad}: dikiş ${d.t} sn görüntü sıçraması ${d.fark} (> ${DIKIS_ESIK}; ${d.once} → ${d.sonra})`);
    }
    if (r.enBitmapMB > 700) basarisiz.push(`${ad}: çözülmüş kare belleği ${r.enBitmapMB} MB (> 700)`);
  }
  for (const c of r.kanvaslar) if (c.gorunur && c.oran > 1.26) basarisiz.push(`${ad}: kanvas DPR ${c.oran} > 1,25 (${c.sinif})`);
  for (const e of r.efektler) if (e.kanvasUstunde) basarisiz.push(`${ad}: kanvas üstünde ${e.backdrop !== 'none' ? 'backdrop-filter' : 'mix-blend'} → ${e.el}`);
  if (r.depolama.localStorage > 0 || r.depolama.sessionStorage > 0 || r.depolama.cerez > 0) basarisiz.push(`${ad}: tarayıcı depolaması kullanılıyor ${JSON.stringify(r.depolama)}`);
  if (depolamaDilSonrasi > 0) uyari.push(`${ad}: dil düğmesi tarayıcı depolamasına yazıyor (src/hikaye/arayuz.js localStorage.setItem; kural: depolama yok)`);
  await ctx.close();
}

await oturum('masaustu', { width: 1600, height: 900 }, { dsf: 1 });
if (!kisa) {
  await oturum('telefon', { width: 768, height: 1366 }, { dsf: 2, tamTur: false });
  await oturum('az', { width: 1280, height: 800 }, { extra: 'az' });
}
sonuc.denetim = { basarisiz, uyari, mod: fileMode ? 'file' : 'http', site: kok };
await writeFile(join(out, 'sinama.json'), JSON.stringify(sonuc, null, 2));
console.log(JSON.stringify(sonuc, null, 2));
console.log(basarisiz.length ? `\nBAŞARISIZ (${basarisiz.length}):\n - ${basarisiz.join('\n - ')}` : '\nTÜM DENETİMLER GEÇTİ');
if (uyari.length) console.log(`UYARI (${uyari.length}):\n - ${uyari.join('\n - ')}`);
await browser.close();
server.close();
process.exitCode = basarisiz.length ? 1 : 0;
