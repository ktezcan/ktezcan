// Tanıtım kaydı: sayfayı baştan sona sabit hızla kaydırır, her video karesinde
// ekran görüntüsü alır ve ffmpeg ile MP4 yapar (gerçek zamanlı kayıt değil →
// makine yavaş da olsa takılmasız). Sayfa ?kayit ile açılır: kaydırma
// yumuşatılmaz, her kare tam konumunda ve tüm kareler inmiş olarak çizilir.
//
// Kullanım: node tools/kayit.mjs <çıktı klasörü> [masaustu|telefon|ikisi] [fps]
// Gerekli: playwright (NODE_PATH ya da tools/node_modules), ffmpeg
import { createServer } from 'node:http';
import { existsSync } from 'node:fs';
import { readFile, mkdir, rm } from 'node:fs/promises';
import { extname, join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const kok = join(dirname(fileURLToPath(import.meta.url)), '..', 'giris-hikaye');
const out = process.argv[2] || 'kayit';
const hangi = process.argv[3] || 'ikisi';
const FPS = Number(process.argv[4] || 25);
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
const base = `http://127.0.0.1:${server.address().port}/`;

const PROFIL = {
  masaustu: { viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 },
  telefon: { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true },
};

// Hız: sahnelerde ekran yüksekliği/saniye, içerik kartlarında daha hızlı + okuma molası
const SAHNE_VH_SN = 0.27;
const GECIS_VH_SN = 0.9;
const ACILIS_MOLA = 2.0;
const SON_MOLA = 3.5;

const ease = (x) => (x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2);

/** Sayfa yerleşiminden kaydırma planı: [{ y0, y1, sure, egri }] — tek akış boyunca sabit hız */
async function plan(page) {
  const d = await page.evaluate(() => {
    const vh = innerHeight;
    const top = (el) => el.getBoundingClientRect().top + scrollY;
    const akis = document.querySelector('[data-akis]');
    const son = document.getElementById('teklif');
    const baslik = son && son.querySelector('h2');
    return {
      vh,
      akisSon: akis ? top(akis) + akis.offsetHeight - vh : 0,
      son: son ? Math.min(top(son) + son.offsetHeight / 2 - vh / 2, baslik ? top(baslik) - 110 : Infinity) : null,
    };
  });
  const adim = [];
  let y = 0;
  const git = (hedef, hiz, egri = true) => {
    const mesafe = Math.abs(hedef - y) / d.vh;
    if (mesafe < 1e-3) return;
    adim.push({ y0: y, y1: hedef, sure: Math.max(0.6, mesafe / hiz), egri });
    y = hedef;
  };
  const bekle = (sure) => adim.push({ y0: y, y1: y, sure, egri: false });
  bekle(ACILIS_MOLA);
  git(d.akisSon, SAHNE_VH_SN, false);
  if (d.son !== null) {
    git(d.son, GECIS_VH_SN);
    bekle(SON_MOLA);
  }
  return adim;
}

function konum(adim, t) {
  for (const a of adim) {
    if (t <= a.sure) {
      const u = t / a.sure;
      return a.y0 + (a.y1 - a.y0) * (a.egri ? ease(u) : u);
    }
    t -= a.sure;
  }
  return adim.length ? adim[adim.length - 1].y1 : 0;
}

// Playwright sürümü kurulu tarayıcıyla eşleşmezse hazır Chromium'u kullan (CHROME_YOLU ile değiştirilebilir)
const chromeYolu = process.env.CHROME_YOLU || (existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined);
const browser = await chromium.launch({ executablePath: chromeYolu, args: ['--autoplay-policy=no-user-gesture-required', '--hide-scrollbars'] });

async function kaydet(ad) {
  const ctx = await browser.newContext({ ...PROFIL[ad], reducedMotion: 'no-preference' });
  const page = await ctx.newPage();
  const hatalar = [];
  page.on('pageerror', (e) => hatalar.push(e.message));
  await page.goto(base + '?kayit', { waitUntil: 'load' });
  await page.waitForTimeout(1200);
  const adim = await plan(page);
  const toplam = adim.reduce((a, b) => a + b.sure, 0);
  const n = Math.round(toplam * FPS);
  const kl = join(out, `kareler_${ad}`);
  await rm(kl, { recursive: true, force: true });
  await mkdir(kl, { recursive: true });
  console.log(`${ad}: ${toplam.toFixed(1)} sn, ${n} kare`);
  for (let i = 0; i < n; i++) {
    const y = Math.round(konum(adim, i / FPS));
    await page.evaluate((yy) => window.scrollTo(0, yy), y);
    // çizim + kare inişi bitsin (en fazla 4 sn bekle)
    await page.evaluate(
      () =>
        new Promise((res) => {
          const t0 = performance.now();
          const tick = () => {
            const e = window.__ege;
            if ((e && e.hazir()) || performance.now() - t0 > 4000) requestAnimationFrame(() => res());
            else setTimeout(tick, 16);
          };
          requestAnimationFrame(() => requestAnimationFrame(tick));
        })
    );
    await page.screenshot({ path: join(kl, `${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 90 });
    if (i % 250 === 0) console.log(`  ${ad} ${i}/${n}`);
  }
  await ctx.close();
  const mp4 = join(out, `ege-gazbeton-giris-${ad}.mp4`);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', join(kl, '%05d.jpg'), '-c:v', 'libx264', '-preset', 'slow', '-crf', '21', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', mp4]);
  console.log(`  → ${mp4}${hatalar.length ? '  HATALAR: ' + hatalar.join(' | ') : ''}`);
  return mp4;
}

const sirala = hangi === 'ikisi' ? ['masaustu', 'telefon'] : [hangi];
for (const ad of sirala) await kaydet(ad);
await browser.close();
server.close();
