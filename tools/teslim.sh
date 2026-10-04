#!/bin/bash
# Teslim paketi: render karelerinden İKİ zip üretir.
#   (a) Ege-Gazbeton-giris-maket_<tarih>.zip   giris-hikaye/ = çift tıkla açılan maket (kareler + js + css + yazı tipleri + OKU-BENI.txt)
#   (b) Ege-Gazbeton-kaynak_<tarih>.zip        depo kaynağı (DEVIR.md, docs, blender, tools, src, giris-hikaye kaynakları);
#                                              MakeHuman verisi, tex/ ve WebP kareler HARİÇ
# Kullanım: tools/teslim.sh <render_kök> <node_modules> <çıktı_klasörü> [python]
# Ortam değişkenleri: EGE_KALITE (temel WebP kalitesi, 90), EGE_BUTCE_MB (tam paket hedefi, 100),
#                     EGE_YERINDE=1 (hazırlığı depodaki giris-hikaye/ içinde yap; varsayılan: <çıktı>/_hazir/ — depo temiz kalır)
# Sıra: dikiş kopyaları (dikis_kopyala.py) → PNG→WebP + meta + poster (kareler.py) → betik derleme (derle.mjs) → zip.
# <çıktı>/_hazir/ kalıcıdır: yeniden çalıştırmada yalnız değişen kareler yeniden kodlanır.
set -euo pipefail

if [ $# -lt 3 ]; then
  echo "Kullanım: tools/teslim.sh <render_kök> <node_modules> <çıktı_klasörü> [python]" >&2
  exit 1
fi
KOK=$(cd "$(dirname "$0")/.." && pwd)
RENDER=$(cd "$1" && pwd)
NM=$(cd "$2" && pwd)
mkdir -p "$3"
OUT=$(cd "$3" && pwd)
PY=${4:-python3}
KALITE=${EGE_KALITE:-90}
BUTCE=${EGE_BUTCE_MB:-100}
TARIH=$(date +%Y-%m-%d_%H%M)
ZIP_MAKET="$OUT/Ege-Gazbeton-giris-maket_$TARIH.zip"
ZIP_KAYNAK="$OUT/Ege-Gazbeton-kaynak_$TARIH.zip"
RAPOR="$OUT/butce-raporu_$TARIH.txt"

# 1) dikiş kopyaları: önceki sahnenin son karesi = sonraki sahnenin ilk karesi (kareler.py'den ÖNCE)
echo "== 1/5 dikiş kopyaları"
"$PY" "$KOK/tools/dikis_kopyala.py" "$RENDER"

# 2) hazırlık klasörü: giris-hikaye kaynakları (kareler ve derlenen betikler hariç) kopyalanır
if [ "${EGE_YERINDE:-0}" = "1" ]; then
  HAZIR="$KOK/giris-hikaye"
  echo "== 2/5 hazırlık: yerinde ($HAZIR)"
else
  HAZIR="$OUT/_hazir/giris-hikaye"
  echo "== 2/5 hazırlık: $HAZIR"
  mkdir -p "$HAZIR"
  # kareler/ korunur (artımlı kodlama); kaynak dosyalar her seferinde yenilenir
  (cd "$KOK/giris-hikaye" && tar cf - --exclude=./kareler --exclude=./assets/js/hikaye.js --exclude=./assets/js/canli.js --exclude=./assets/js/kareler-meta.js .) | (cd "$HAZIR" && tar xf -)
fi

# 3) kareler: PNG → WebP (bütçeye göre kalite), kareler-meta.js, posterler
echo "== 3/5 kareler (WebP, bütçe $BUTCE MB)"
"$PY" "$KOK/tools/kareler.py" "$RENDER" "$KALITE" --site "$HAZIR" --butce-mb "$BUTCE" --rapor "$RAPOR"

# 4) betikler (hikaye.js, canli.js) ve yazı tipleri
echo "== 4/5 betik derleme"
EGE_SITE="$HAZIR" node "$KOK/tools/derle.mjs" "$NM"

# bütünlük: maket açılmak için gerekenler var mı
for f in index.html assets/css/hikaye.css assets/js/hikaye.js assets/js/kareler-meta.js OKU-BENI.txt; do
  [ -s "$HAZIR/$f" ] || { echo "HATA: eksik dosya giris-hikaye/$f" >&2; exit 1; }
done
for s in s0 s1 s2 s3 s4 s5; do
  [ -s "$HAZIR/kareler/$s/poster.webp" ] || echo "UYARI: $s posteri yok" >&2
  [ -d "$HAZIR/kareler/$s/d" ] || echo "UYARI: $s masaüstü karesi yok (sahne boş/poster ile görünür)" >&2
done

# 5) zip'ler
echo "== 5/5 zip"
rm -f "$ZIP_MAKET" "$ZIP_KAYNAK"
# (a) maket: üst klasör giris-hikaye/ (HAZIR klasörünün adı); .kalite işaret dosyaları girmez
(cd "$(dirname "$HAZIR")" && zip -qr -X -6 "$ZIP_MAKET" "$(basename "$HAZIR")" -x '*/.kalite' '*/.DS_Store' '*/__pycache__/*')

# (b) kaynak: izlenen + yeni (git'in yok saymadığı) dosyalar; elle silinmiş izlenen dosyalar atlanır
KAYNAK_GECICI=$(mktemp -d)
trap 'rm -rf "$KAYNAK_GECICI"' EXIT
mkdir -p "$KAYNAK_GECICI/Ege-Gazbeton-kaynak"
if git -C "$KOK" rev-parse --git-dir >/dev/null 2>&1; then
  LISTE=$(cd "$KOK" && git ls-files -co --exclude-standard)
else
  LISTE=$(cd "$KOK" && find . -type f -not -path './.git/*' -not -path '*/node_modules/*' | sed 's#^\./##')
fi
(cd "$KOK" && printf '%s\n' "$LISTE" \
  | grep -v -E '^giris-hikaye/kareler/|\.webp$|(^|/)__pycache__/|(^|/)node_modules/|(^|/)(mh|tex)/' \
  | while IFS= read -r f; do [ -f "$f" ] && printf '%s\n' "$f"; done \
  | tar -cf - -T -) | (cd "$KAYNAK_GECICI/Ege-Gazbeton-kaynak" && tar -xf -)
(cd "$KAYNAK_GECICI" && zip -qr -X -9 "$ZIP_KAYNAK" Ege-Gazbeton-kaynak)

echo
echo "== teslim"
cat "$RAPOR" | tail -4
ls -la "$ZIP_MAKET" "$ZIP_KAYNAK"
echo "maket   : $ZIP_MAKET"
echo "kaynak  : $ZIP_KAYNAK"
echo "rapor   : $RAPOR"
