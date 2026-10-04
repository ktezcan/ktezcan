#!/bin/bash
# Yeni hikâyenin (6 sahne) tüm render'ları, sırayla. Yarım kalırsa tekrar çalıştırın (--skip-existing).
# Ortam: EGE_TEX (gazbeton dokuları + kara_noktalari.json), EGE_MH (tools/mh_indir.sh), PY (bpy 5.0 python)
# Kullanım: tools/render_hepsi.sh <render_kök>
set -e
K=$(cd "$(dirname "$0")/.." && pwd); R=${1:?render kökü}; PY=${PY:-python3}
cd "$K/blender"
for v in d m; do
  for kip in egim dolum sokak; do $PY s0_hayal.py --kip $kip --variant $v --out "$R/s0src/$v" --skip-existing; done
  $PY s0_hayal.py --kip plaka --variant $v --frames 0,1,2,3,4,5 --out "$R/s0src/$v" --skip-existing
  $PY s0_hayal.py --kip plaka --variant $v --frames 6 --out "$R/s0src/$v" --skip-existing   # akşam, ışıklar kapalı
  $PY s0_hayal.py --kip plaka --variant $v --frames 7 --out "$R/s0src/$v" --skip-existing   # akşam, ışıklar açık
done
$PY "$K/tools/s0_birlestir.py" "$R/s0src" "$R" d m
$PY s1_urun.py --variant d --out "$R/s1d" --skip-existing
EGE_MINSTEP=2 $PY s1_urun.py --variant m --out "$R/s1m" --skip-existing
# s2 doğuş = s1_dogus.py, s3 gözenek = s2_gozenek.py (önceki teslimin betikleri, çıktı klasörünü s2/s3 olarak verin)
$PY s4_yol.py --variant d --out "$R/s4d" --skip-existing
EGE_MINSTEP=2 $PY s4_yol.py --variant m --out "$R/s4m" --skip-existing
$PY s4_dunya.py --variant d --out "$R/s5d" --skip-existing
EGE_MINSTEP=2 $PY s4_dunya.py --variant m --out "$R/s5m" --skip-existing
echo "Bitti. Sonra: python tools/kareler.py $R && node tools/derle.mjs <node_modules>"
