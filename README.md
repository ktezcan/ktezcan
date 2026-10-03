# Ege Gazbeton — giriş sayfası hikâyesi ("Hammaddeden binaya")

Ana sayfanın yalnız **giriş bölümü** için kaydırmaya bağlı, sinematik hikâye:
önceden hesaplanmış Blender (Cycles) kareleri + tıklanır noktalar + içerik kartları.
Hikâye bitince sayfanın geri kalanında animasyon döngüsü çalışmaz.

| Klasör | İçerik |
|---|---|
| `giris-hikaye/` | Teslim edilen, çift tıkla açılan maket (`index.html`). Kurulum notu: `OKU-BENI.txt` |
| `src/hikaye/` | Sayfa betiğinin kaynak modülleri (kare oynatıcı, video→blok homografisi, TR/EN, yolculuk çubuğu) |
| `src/canli/` | Teklif bölümündeki canlı gözenek katmanı (three.js, yalnız görünürken çalışır) |
| `blender/` | Sahne betikleri (bpy 5.x): `kit.py` ortak stüdyo, `s0`…`s4` sahneler, `dokular.py` gazbeton dokusu |
| `tools/` | `kareler.py` (PNG→WebP + meta), `derle.mjs` (esbuild → tek dosyalık betik), `sinama.mjs` (başsız tarayıcı sınaması), `paketle.sh`, `hikaye_foy.py` |

## Sahneler

| | Sahne | Kare (masaüstü / telefon) | İçerik kartı |
|---|---|---|---|
| s0 | Video → blok (gerçek video, bloğun ön yüzüne CSS `matrix3d` ile oturur) | 60 / 30 | 2 fabrika · 1.100.000 m³ · TS EN 771-4 |
| s1 | Doğuş: blok çözülür, hammadde kaideleri, girdap, kabarma, tel kesim | 96 / 48 | karışım → kabarma → kesim ve otoklav |
| s2 | Gözenek: 12 mm makro numune, kapalı hava hücresi | 72 / 36 | λ 0,08 · A1 · 300–600 kg/m³ |
| s3 | Bina: temel → karkas → duvarlar (sıra sıra) → lento → çatı paneli → doğrama | 96 / 48 | ODTÜ: −%17 kütle, −%14 taban kesme |
| s4 | Dünya: Söke/İzmir'den 5 kıtaya yaylar (ülke adı/sınırı yok) | 72 / 36 | 25+ ülke · 5 kıta |

## Komutlar

```bash
# Blender (bpy 5.0, Python 3.11): pip install bpy==5.0.1 numpy pillow scikit-image
python blender/dokular.py tex                     # gazbeton dokuları
EGE_TEX=tex python blender/s1_dogus.py --variant d --frames all --out render/s1d --skip-existing
EGE_PREVIEW=30 ...                               # hızlı önizleme (%30 çözünürlük, 8 örnek)
EGE_MINSTEP=2 ... --variant m                    # telefon seti (her 2. kare)

python tools/kareler.py render                   # → giris-hikaye/kareler + assets/js/kareler-meta.js
node tools/derle.mjs <node_modules>              # esbuild, three, @fontsource/barlow(-condensed)
node tools/sinama.mjs sinama                     # konsol hatası, rAF boşta durma, ekran görüntüleri
```

## Astro sitesine taşıma (kod\ deposu)

- `giris-hikaye/index.html` içindeki `.eg-hikaye` bloğu bir Astro bileşenine (`GirisHikaye.astro`) aynen taşınabilir;
  `assets/css/hikaye.css` ve `src/hikaye/*.js` modülleri Vite ile doğrudan paketlenir (IIFE gerekmez).
- `kareler/` → `public/kareler/` ; `kareler-meta.js` yerine `import meta from './kareler-meta.json'`.
- Kurallar korunmuştur: 3B görüntüde yazı/rakam yok · ülke adı yok · "yanmaz" denmez (A1) ·
  yeşil yalnız bizim ürüne · backdrop-filter/blend yok · DPR ≤ 1,25 · hareket azaltmada tek kare.
