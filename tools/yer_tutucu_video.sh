#!/bin/bash
# Gerçek tanıtım videosu gelene kadar dürüst bir yer tutucu üretir (6 sn döngü, ~150 KB).
# Gerçek dosya: kod\public\video\tanitim-hero-720.mp4 → giris-hikaye/assets/video/tanitim-hero.mp4
set -e
OUT=${1:-giris-hikaye/assets/video}
mkdir -p "$OUT"
T1=$(mktemp); T2=$(mktemp)
printf 'TANITIM VİDEOSU (YER TUTUCU)' > "$T1"
printf 'gerçek video: assets/video/tanitim-hero.mp4' > "$T2"
F=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
F2=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
ffmpeg -y -loglevel error -f lavfi -i "color=c=0x14212a:s=1280x720:d=6:r=25" -vf "\
drawbox=x=0:y=ih*0.5-1:w=iw*mod(t\,6)/6:h=2:color=0xa2bf37@0.9:t=fill,\
drawbox=x=40:y=40:w=70:h=8:color=0xa2bf37:t=fill,drawbox=x=40:y=40:w=8:h=70:color=0xa2bf37:t=fill,\
drawbox=x=iw-110:y=40:w=70:h=8:color=0xa2bf37:t=fill,drawbox=x=iw-48:y=40:w=8:h=70:color=0xa2bf37:t=fill,\
drawbox=x=40:y=ih-48:w=70:h=8:color=0xa2bf37:t=fill,drawbox=x=40:y=ih-110:w=8:h=70:color=0xa2bf37:t=fill,\
drawbox=x=iw-110:y=ih-48:w=70:h=8:color=0xa2bf37:t=fill,drawbox=x=iw-48:y=ih-110:w=8:h=70:color=0xa2bf37:t=fill,\
drawtext=fontfile=$F:textfile=$T1:fontcolor=white@0.85:fontsize=40:x=w-text_w-140:y=150,\
drawtext=fontfile=$F2:textfile=$T2:fontcolor=0xc9d3d9:fontsize=20:x=w-text_w-140:y=205" \
  -c:v libx264 -pix_fmt yuv420p -crf 30 -preset slow -movflags +faststart -an "$OUT/tanitim-hero.mp4"
ffmpeg -y -loglevel error -ss 3 -i "$OUT/tanitim-hero.mp4" -frames:v 1 -q:v 4 "$OUT/tanitim-hero.jpg"
rm -f "$T1" "$T2"
ls -la "$OUT"
