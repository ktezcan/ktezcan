"""
Render karelerini web'e hazırlar:
  PNG → WebP (giris-hikaye/kareler/<sahne>/<d|m>/NNN.webp), sahne posteri,
  ve tüm metaları (mevcut kareler, video yüzü köşeleri, tıklanır noktalar)
  tek bir klasik betikte toplar: giris-hikaye/assets/js/kareler-meta.js
  (fetch gerekmez → maket file:// ile de çalışır).

Kullanım: python tools/kareler.py <render_kök> [kalite]
"""
import json
import os
import sys

from PIL import Image

KOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
HEDEF = os.path.join(KOK, 'giris-hikaye', 'kareler')
META_JS = os.path.join(KOK, 'giris-hikaye', 'assets', 'js', 'kareler-meta.js')
SAHNELER = ['s0', 's1', 's2', 's3', 's4']


def yuvarla(o, n=4):
    if isinstance(o, float):
        return round(o, n)
    if isinstance(o, list):
        return [yuvarla(x, n) for x in o]
    if isinstance(o, dict):
        return {k: yuvarla(v, n) for k, v in o.items()}
    return o


def main(render_kok, kalite=80):
    hepsi = {}
    toplam = 0
    for sid in SAHNELER:
        for var in ('d', 'm'):
            src = os.path.join(render_kok, f'{sid}{var}')
            meta_p = os.path.join(src, 'meta.json')
            if not os.path.isdir(src) or not os.path.exists(meta_p):
                continue
            meta = json.load(open(meta_p, encoding='utf-8'))
            out = os.path.join(HEDEF, sid, var)
            os.makedirs(out, exist_ok=True)
            mevcut = []
            for name in sorted(os.listdir(src)):
                if not name.endswith('.png'):
                    continue
                i = int(name[:-4])
                png = os.path.join(src, name)
                webp = os.path.join(out, f'{i:03d}.webp')
                if not os.path.exists(webp) or os.path.getmtime(webp) < os.path.getmtime(png):
                    try:
                        im = Image.open(png)
                        im.load()
                    except Exception:
                        continue  # yazılmakta olan kare
                    im.convert('RGB').save(webp, 'WEBP', quality=kalite, method=6)
                mevcut.append(i)
                toplam += 1
            if not mevcut:
                continue
            ent = {'n': meta['frames'], 'res': meta['res'], 'mevcut': sorted(mevcut)}
            if 'face' in meta:
                ent['face'] = yuvarla(meta['face'])
            if 'hotspots' in meta:
                ent['hotspots'] = {k: v for k, v in yuvarla(meta['hotspots']).items() if v}
            hepsi.setdefault(sid, {})[var] = ent
            # poster: masaüstü dizisinin ilk karesi (yoksa ilk mevcut)
            if var == 'd':
                first = os.path.join(src, f'{sorted(mevcut)[0]:03d}.png')
                Image.open(first).convert('RGB').resize((960, 540), Image.LANCZOS).save(
                    os.path.join(HEDEF, sid, 'poster.webp'), 'WEBP', quality=70, method=6)
    os.makedirs(os.path.dirname(META_JS), exist_ok=True)
    with open(META_JS, 'w', encoding='utf-8') as f:
        f.write('/* Otomatik üretilir: tools/kareler.py — elle düzenlemeyin */\n')
        f.write('window.EGE_KARELER=' + json.dumps(hepsi, ensure_ascii=False, separators=(',', ':')) + ';\n')
    ozet = {s: {v: len(d['mevcut']) for v, d in vs.items()} for s, vs in hepsi.items()}
    print('kareler hazır:', toplam, ozet)


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 80)
