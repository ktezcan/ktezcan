#!/usr/bin/env python3
"""Sayfa/oynatıcı sınamaları için yer tutucu kare kökü üretir (gerçek render yok).
Kare sayıları docs/plan'daki son planla aynıdır; her karede sahne adı ve kare numarası yazar (yer tutucu: yazı serbest).
Kullanım: python tools/kare_taklit.py <çıktı_kök> [--adim N] [--sahneler s0,s1] [--kucuk]
  --adim N : yalnız her N. kare (seyrek set; oynatıcının ara kare erimesini sınamak için).
             Telefon (m) seti tam sette her 2. kare, seyrek sette (N ≥ 8) aynı N: oynatıcı en çok 16 kare boşluklu seti kabul eder.
  --kucuk  : 1/4 çözünürlük (hızlı)
"""
import argparse
import json
import os

from PIL import Image, ImageDraw

SAYI = {'s0': 256, 's1': 152, 's2': 100, 's3': 85, 's4': 128, 's5': 193}
RENK = {'s0': (235, 227, 213), 's1': (240, 243, 246), 's2': (226, 232, 236), 's3': (214, 222, 228), 's4': (196, 214, 232), 's5': (12, 22, 32)}
RES = {'d': (1600, 900), 'm': (768, 1366)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cikti')
    ap.add_argument('--adim', type=int, default=1)
    ap.add_argument('--sahneler', default=','.join(SAYI))
    ap.add_argument('--kucuk', action='store_true')
    a = ap.parse_args()
    for s in a.sahneler.split(','):
        n = SAYI[s]
        for v in ('d', 'm'):
            w, h = RES[v]
            if a.kucuk:
                w, h = w // 4, h // 4
            adim = a.adim * (2 if v == 'm' and a.adim < 8 else 1)
            d = os.path.join(a.cikti, f'{s}{v}')
            os.makedirs(d, exist_ok=True)
            idx = sorted(set(list(range(0, n, adim)) + [n - 1]))
            for i in idx:
                t = i / (n - 1)
                c = tuple(int(x * (0.75 + 0.25 * t)) for x in RENK[s])
                im = Image.new('RGB', (w, h), c)
                dr = ImageDraw.Draw(im)
                # sağda/üstte "özne" (kamera kaymasına benzer): kare ilerledikçe hareket eden daire
                cx = int(w * (0.55 + 0.25 * t)) if v == 'd' else int(w * 0.5)
                cy = int(h * 0.5) if v == 'd' else int(h * (0.6 + 0.2 * t))
                r = int(min(w, h) * (0.12 + 0.1 * t))
                dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(184, 216, 74) if s != 's5' else (60, 120, 200))
                dr.text((20, 20), f'{s}{v} kare {i}/{n - 1}', fill=(30, 30, 30) if s != 's5' else (240, 240, 240))
                im.save(os.path.join(d, f'{i:03d}.png'), compress_level=1)
            meta = {'frames': n, 'res': [w, h], 'hotspots': {}}
            if s == 's0':  # eskiz kalemi: kalem ucu (0..1) ilk 40 kare boyunca köşegende gezer (meta.pen geçişini sınamak için)
                meta['pen'] = {str(i): [round(0.25 + 0.5 * i / 40, 4), round(0.3 + 0.4 * i / 40, 4)] for i in idx if 6 <= i <= 44}
            json.dump(meta, open(os.path.join(d, 'meta.json'), 'w'))
            print(s, v, len(idx), 'kare')


if __name__ == '__main__':
    main()
