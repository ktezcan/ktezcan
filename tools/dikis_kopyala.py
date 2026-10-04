#!/usr/bin/env python3
"""Sahne dikiş karelerini kopyalar: önceki sahnenin son karesi = sonraki sahnenin ilk karesi.

Render kuyruğu bu kareleri bir kez (sonraki sahne sahibi olarak) üretir; blender/spec/*.json içindeki "kopya"
girdileri diğer sahnedeki karşılığını tanımlar:
  "kopya": [ {"hedef": "{root}/s1{v}/151.png", "kaynak": "{root}/s2{v}/000.png"} ]
{root} = render kökü, {v} = d ve m (girdide {v} varsa her iki varyant için ayrı ayrı genişler).
Hedef zaten varsa ÜZERİNE YAZILIR; kaynak yoksa (henüz render edilmemiş) atlanır. teslim.sh bunu kareler.py'den ÖNCE çağırır.

Kullanım: python tools/dikis_kopyala.py <render_kök> [--spec blender/spec]
"""
import argparse
import glob
import json
import os
import shutil
import sys

KOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
VARYANTLAR = ('d', 'm')


def ac(s, kok, v):
    return s.replace('{root}', kok).replace('{v}', v)


def main():
    ap = argparse.ArgumentParser(description='Spec "kopya" girdilerinden dikiş karelerini kopyalar')
    ap.add_argument('render_kok')
    ap.add_argument('--spec', default=os.path.join(KOK, 'blender', 'spec'))
    a = ap.parse_args()
    kok = os.path.abspath(a.render_kok)
    kopyalanan = atlanan = 0
    for yol in sorted(glob.glob(os.path.join(a.spec, '*.json'))):
        try:
            spec = json.load(open(yol, encoding='utf-8'))
        except Exception as e:  # bozuk taslak paketi durdurmasın
            print(f'atlandı (okunamadı): {yol}: {e}')
            continue
        for g in spec.get('kopya', []):
            hedef_s, kaynak_s = g.get('hedef'), g.get('kaynak')
            if not hedef_s or not kaynak_s:
                continue
            for v in VARYANTLAR if '{v}' in hedef_s or '{v}' in kaynak_s else (None,):
                kaynak = ac(kaynak_s, kok, v or '')
                hedef = ac(hedef_s, kok, v or '')
                if not os.path.exists(kaynak):
                    atlanan += 1
                    print(f'kaynak yok, atlandı: {os.path.relpath(kaynak, kok)} → {os.path.relpath(hedef, kok)}')
                    continue
                os.makedirs(os.path.dirname(hedef), exist_ok=True)
                shutil.copy2(kaynak, hedef)
                kopyalanan += 1
                print(f'kopyalandı: {os.path.relpath(kaynak, kok)} → {os.path.relpath(hedef, kok)}')
    print(f'dikiş kopyaları: {kopyalanan} kopyalandı, {atlanan} atlandı')


if __name__ == '__main__':
    sys.exit(main())
