// Hikâye betiğini tek dosyalık, klasik (IIFE) betiğe derler → file:// ile de açılır,
// FTP/panelden yüklemede derleme adımı gerekmez. Kullanım: node tools/derle.mjs <node_modules yolu>
// Çıktı klasörü varsayılan giris-hikaye/; EGE_SITE=<klasör> ile başka bir kopyaya (örn. sınama için) derlenebilir.
// Kaynak kökü varsayılan src/; EGE_SRC=<klasör> ile başka bir src kopyasından (hikaye/ ve canli/ altında) derlenebilir.
import { createRequire } from 'node:module';
import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const kok = join(dirname(fileURLToPath(import.meta.url)), '..');
const nm = process.argv[2] || join(kok, 'node_modules');
const site = process.env.EGE_SITE || join(kok, 'giris-hikaye');
const src = process.env.EGE_SRC || join(kok, 'src');
const { build } = createRequire(join(nm, 'x.js'))('esbuild');
await build({
  entryPoints: [join(src, 'hikaye/main.js')],
  bundle: true,
  format: 'iife',
  target: ['es2019'],
  minify: true,
  legalComments: 'none',
  outfile: join(site, 'assets/js/hikaye.js'),
  banner: { js: '/* Ege Gazbeton — giriş hikâyesi · kaynak: src/hikaye/ */' },
});

// Canlı katman (three.js gömülü, yalnız teklif bölümü yaklaşınca yüklenir)
await build({
  entryPoints: [join(src, 'canli/giris.js')],
  bundle: true,
  format: 'iife',
  target: ['es2019'],
  minify: true,
  legalComments: 'none',
  nodePaths: [nm],
  outfile: join(site, 'assets/js/canli.js'),
  banner: { js: '/* Ege Gazbeton — canlı gözenek katmanı · three.js (MIT) · kaynak: src/canli/ */' },
});

// Yazı tipleri (yerel; dış servis yok — KVKK ve çevrimdışı maket için)
const fontDir = join(site, 'assets/fonts');
mkdirSync(fontDir, { recursive: true });
for (const [pkg, file] of [
  ['barlow', 'barlow-latin-400-normal.woff2'], ['barlow', 'barlow-latin-ext-400-normal.woff2'],
  ['barlow', 'barlow-latin-500-normal.woff2'], ['barlow', 'barlow-latin-ext-500-normal.woff2'],
  ['barlow', 'barlow-latin-600-normal.woff2'], ['barlow', 'barlow-latin-ext-600-normal.woff2'],
  ['barlow-condensed', 'barlow-condensed-latin-600-normal.woff2'], ['barlow-condensed', 'barlow-condensed-latin-ext-600-normal.woff2'],
  ['barlow-condensed', 'barlow-condensed-latin-700-normal.woff2'], ['barlow-condensed', 'barlow-condensed-latin-ext-700-normal.woff2'],
]) {
  copyFileSync(join(nm, '@fontsource', pkg, 'files', file), join(fontDir, file));
}
console.log(`derlendi: ${site}/assets/js/hikaye.js + canli.js + yazı tipleri`);
