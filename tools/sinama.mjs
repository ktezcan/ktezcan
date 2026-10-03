// Başsız Chromium sınaması: konsol hatası, kaydırma, rAF'ın boşta durması, ekran görüntüleri.
// Kullanım: node tools/sinama.mjs <çıktı klasörü> [file]
import { createServer } from 'node:http';
import { existsSync } from 'node:fs';
import { readFile, mkdir } from 'node:fs/promises';
import { extname, join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const kok = join(dirname(fileURLToPath(import.meta.url)), '..', 'giris-hikaye');
const out = process.argv[2] || 'sinama';
const fileMode = process.argv[3] === 'file';
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

async function oturum(ad, viewport, extra = '') {
  const ctx = await browser.newContext({ viewport, deviceScaleFactor: 1, reducedMotion: extra.includes('az') ? 'reduce' : 'no-preference' });
  const page = await ctx.newPage();
  const hatalar = [];
  // 'GPU stall due to ReadPixels': başsız Chromium'un yazılımsal birleştirmesi her WebGL karesini geri okur
  // (en basit WebGL sayfasında da çıkar) → sayfa hatası değil, raporlanmaz
  page.on('console', (m) => { if ((m.type() === 'error' || m.type() === 'warning') && !/GPU stall due to ReadPixels/.test(m.text())) hatalar.push(`${m.type()}: ${m.text()}`); });
  page.on('pageerror', (e) => hatalar.push(`pageerror: ${e.message}`));
  await page.goto(base + '?debug' + (extra ? '&' + extra : ''), { waitUntil: 'load' });
  await page.waitForTimeout(1500);
  const shots = [];
  async function shot(name) {
    const f = join(out, `${ad}_${name}.png`);
    await page.screenshot({ path: f });
    shots.push(f);
  }
  await shot('0_giris');
  const H = await page.evaluate(() => document.documentElement.scrollHeight);
  const s0 = await page.evaluate(() => { const r = document.querySelector('[data-akis]').getBoundingClientRect(); return { top: r.top + scrollY, h: r.height }; });
  const vh = viewport.height;
  for (const p of [0.06, 0.12, 0.2, 0.35, 0.55, 0.8, 1.0]) {
    await page.evaluate((y) => window.scrollTo(0, y), s0.top + (s0.h - vh) * p);
    await page.waitForTimeout(900);
    await shot(`s0_${String(Math.round(p * 100)).padStart(3, '0')}`);
  }
  // boşta rAF durmalı
  await page.waitForTimeout(1200);
  const bosta = await page.evaluate(() => ({ calisiyor: window.__ege.calisiyor, sayac: window.__ege.raf }));
  await page.waitForTimeout(1500);
  const bosta2 = await page.evaluate(() => window.__ege.raf);
  // hikâyenin sonrası: rAF hiç çalışmamalı
  await page.evaluate(() => document.getElementById('urunler').scrollIntoView());
  await page.waitForTimeout(1500);
  const sonra1 = await page.evaluate(() => window.__ege.raf);
  await page.mouse.move(200, 200);
  await page.mouse.move(400, 300);
  await page.waitForTimeout(1500);
  const sonra2 = await page.evaluate(() => window.__ege.raf);
  await shot('urunler');
  // dil
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.click('[data-dil-sec="en"]');
  await page.waitForTimeout(600);
  await shot('en');
  sonuc[ad] = {
    hatalar,
    yukseklik: H,
    bostaCalisiyor: bosta.calisiyor,
    bostaKareArtisi: bosta2 - bosta.sayac,
    hikayeSonrasiKareArtisi: sonra2 - sonra1,
    shots: shots.length,
  };
  await ctx.close();
}

await oturum('masaustu', { width: 1440, height: 900 });
await oturum('telefon', { width: 390, height: 844 });
await oturum('az', { width: 1280, height: 800 }, 'az');
console.log(JSON.stringify(sonuc, null, 2));
await browser.close();
server.close();
