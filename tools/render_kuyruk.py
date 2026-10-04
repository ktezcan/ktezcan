#!/usr/bin/env python3
"""Render kuyruğu: blender/spec/*.json dosyalarındaki sahne işlerini AŞAMA-ÖNCELİKLİ sırayla koşturur.

Neden aşama öncelikli: her sahnenin kareleri 4 geçişte (8'de bir → 4 → 2 → hepsi) üretilir; oynatıcı seyrek kareler
arasını eritir. Kuyruk istenen her an kesilse sayfa eksiksiz çalışır, geçiş ilerledikçe akıcılaşır.
Telefon (m) kareleri yalnız çift numaralı kareler + son karedir.

Spec biçimi (blender/spec/<id>.json) — sahne betiği HAZIR olunca yazılır:
{
  "id": "s1",
  "jobs": [ {
      "script": "s1_urun.py",              # blender/ altında
      "args": ["--kip", "egim"],           # betiğe ek argümanlar (isteğe bağlı)
      "out": "{root}/s1{v}",               # --out değeri; {root} = çıktı kökü, {v} = d|m
      "png_dir": "{root}/s1{v}",           # kare PNG'lerinin düştüğü klasör (var-mı denetimi); yoksa out
      "frames": 152,                       # toplam kare sayısı (aşamalara bölünür)   VEYA
      "frame_list": [0,1,2],               # açık liste (tek aşama, bölünmez)
      "variants": ["d", "m"],              # isteğe bağlı (varsayılan ikisi de)
      "env": {}                            # isteğe bağlı ortam değişkenleri
  } ],
  "post": {"cmd": ["python", "tools/s0_birlestir.py", "{root}/s0src", "{root}", "{v}"], "after_passes": [1, 3]}
}
Kullanım: python tools/render_kuyruk.py --root ~/render3 --python <bl/bin/python> [--once] [--dry-run]
Durdurmak için <root>/STOP dosyası oluşturun.
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNK = 6


def asamalar(n, v):
    """Kare sayısı n için 4 aşamalı kare listeleri (m: yalnız çift + son)."""
    kume = [i for i in range(n) if v == 'd' or i % 2 == 0]
    if n - 1 not in kume:
        kume.append(n - 1)
    p0 = [i for i in kume if i % 8 == 0 or i == n - 1]
    r = [i for i in kume if i not in p0]
    p1 = [i for i in r if i % 4 == 0]
    r = [i for i in r if i not in p1]
    p2 = [i for i in r if i % 2 == 0]
    p3 = [i for i in r if i not in p2]
    return [p0, p1, p2, p3]


def aç(s, kok, v):
    return s.replace('{root}', kok).replace('{v}', v)


def yukle(spec_dir):
    out = []
    for p in sorted(glob.glob(os.path.join(spec_dir, '*.json'))):
        try:
            s = json.load(open(p, encoding='utf-8'))
            if s.get('enabled', True) is not False:
                out.append(s)
        except Exception as e:  # yarım yazılmış dosya: sonraki turda
            print('spec okunamadı', p, e, flush=True)
    return out


def isler(specs, kok, hatali):
    """(öncelik, spec_sırası, iş_sırası, v, aşama, [kare...], spec, iş) — eksik karesi olanlar."""
    liste = []
    for si, sp in enumerate(specs):
        for ji, j in enumerate(sp['jobs']):
            for v in j.get('variants', ['d', 'm']):
                pdir = aç(j.get('png_dir', j['out']), kok, v)
                if 'frame_list' in j:
                    ps = [list(j['frame_list']), [], [], []]
                else:
                    ps = asamalar(j['frames'], v)
                for pi, fr in enumerate(ps):
                    eksik = [f for f in fr if not os.path.exists(os.path.join(pdir, f'{f:03d}.png'))
                             and (sp['id'], ji, v, f) not in hatali]
                    if eksik:
                        liste.append((pi + (0.5 if v == 'm' else 0.0), si, ji, v, pi, eksik, sp, j))
    liste.sort(key=lambda x: x[:3])
    return liste


def post_gerek(specs, kok, post_yapildi):
    """Bir aşama (spec, v) için tamamlandıysa ve post tanımlıysa çalıştırılacakları döndür."""
    gerek = []
    for sp in specs:
        po = sp.get('post')
        if not po:
            continue
        for v in ('d', 'm'):
            for pi in po.get('after_passes', [1, 3]):
                anahtar = (sp['id'], v, pi)
                if anahtar in post_yapildi:
                    continue
                tamam = True
                for j in sp['jobs']:
                    if v not in j.get('variants', ['d', 'm']):
                        continue
                    pdir = aç(j.get('png_dir', j['out']), kok, v)
                    ps = [list(j['frame_list'])] if 'frame_list' in j else asamalar(j['frames'], v)[:pi + 1]
                    for fr in ps:
                        if any(not os.path.exists(os.path.join(pdir, f'{f:03d}.png')) for f in fr):
                            tamam = False
                if tamam:
                    gerek.append((anahtar, po, v))
    return gerek


def calistir(cmd, env, log, dry):
    print('$', ' '.join(cmd), flush=True)
    if dry:
        return 0
    with open(log, 'a') as lf:
        lf.write('\n$ ' + ' '.join(cmd) + '\n')
        lf.flush()
        return subprocess.call(cmd, stdout=lf, stderr=subprocess.STDOUT, env=env, cwd=os.path.join(REPO, 'blender'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--python', required=True)
    ap.add_argument('--spec-dir', default=os.path.join(REPO, 'blender', 'spec'))
    ap.add_argument('--once', action='store_true', help='iş kalmayınca çık (varsayılan: yeni spec için bekle)')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    kok = os.path.abspath(a.root)
    os.makedirs(kok, exist_ok=True)
    log = os.path.join(kok, 'kuyruk.log')
    hatali, deneme, post_yapildi = set(), {}, set()
    while True:
        if os.path.exists(os.path.join(kok, 'STOP')):
            print('STOP', flush=True)
            return
        specs = yukle(a.spec_dir)
        gerek = post_gerek(specs, kok, post_yapildi)
        if gerek:
            anahtar, po, v = gerek[0]
            cmd = [aç(c, kok, v) for c in po['cmd']]
            cmd = [a.python if c == 'python' else c for c in cmd]
            rc = calistir(cmd, dict(os.environ), log, a.dry_run)
            post_yapildi.add(anahtar)
            print('post', anahtar, 'rc', rc, flush=True)
            continue
        liste = isler(specs, kok, hatali)
        if not liste:
            if a.once or a.dry_run:
                print('KUYRUK BITTI', flush=True)
                return
            time.sleep(60)
            continue
        pr, si, ji, v, pi, eksik, sp, j = liste[0]
        parca = eksik[:CHUNK]
        env = dict(os.environ)
        env.update({k: str(x) for k, x in j.get('env', {}).items()})
        cmd = [a.python, os.path.join(REPO, 'blender', j['script'])] + list(j.get('args', [])) + [
            '--variant', v, '--out', aç(j['out'], kok, v), '--frames', ','.join(str(f) for f in parca), '--skip-existing']
        rc = calistir(['nice', '-n', '5'] + cmd, env, log, a.dry_run)
        print(f"[{sp['id']} iş{ji} {v} aşama{pi}] {parca[0]}..{parca[-1]} rc={rc}", flush=True)
        if a.dry_run:
            return
        if rc != 0:
            k = (sp['id'], ji, v, parca[0])
            deneme[k] = deneme.get(k, 0) + 1
            if deneme[k] >= 2:
                for f in parca:
                    hatali.add((sp['id'], ji, v, f))
                print('KARELER ATLANDI (2 hata):', k, flush=True)


if __name__ == '__main__':
    main()
