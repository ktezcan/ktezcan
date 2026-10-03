#!/bin/bash
# Teslim paketi: kareleri dönüştür, betikleri derle, zip'le.
# Kullanım: tools/paketle.sh <render_kök> <node_modules> <çıktı_klasörü> [python]
set -e
KOK=$(cd "$(dirname "$0")/.." && pwd)
RENDER=$1; NM=$2; OUT=$3; PY=${4:-python3}
"$PY" "$KOK/tools/kareler.py" "$RENDER" 80
node "$KOK/tools/derle.mjs" "$NM"
mkdir -p "$OUT"
TARIH=$(date +%Y-%m-%d_%H%M)
ZIP="$OUT/Ege-Gazbeton-giris-hikaye_$TARIH.zip"
TMP=$(mktemp -d)
cp -r "$KOK/giris-hikaye" "$TMP/Ege-Gazbeton-giris-hikaye"
(cd "$TMP" && zip -qr -9 "$ZIP" "Ege-Gazbeton-giris-hikaye")
rm -rf "$TMP"
ls -la "$ZIP"
echo "$ZIP"
