"""
Perde 3 sonu — "Fabrikadan yola": Söke tesisi sabah ışığında (gerçek gök, güneş).
Lime streçli paletlerle yüklü Ege Gazbeton tırı sahadan çıkıp yola koyulur; kamera önce tırı
yandan izler, sonra yükselip tepeden bakışa geçer (→ dünya sahnesinin tepeden girişiyle eşleşir).

Kullanım: python s4_yol.py --variant d|m --out DIR [--frames all|0,40] [--samples N]
"""
import argparse
import math
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
import stil_r as R  # noqa: E402
import stil_r5 as T5  # noqa: E402
import stil_r7 as G  # noqa: E402
import sokak as S  # noqa: E402
import s0_hayal as H  # noqa: E402

FRAMES = 48
RES = {'d': (1600, 900), 'm': (768, 1366)}
YOL_Y = -46.0


def sahne(sc):
    T5.sahne_fabrika2(sc)
    for ob in list(bpy.data.objects):
        if ob.type == 'LIGHT' and ob.data.type == 'AREA':
            ob.data.energy = 0
        if ob.type == 'CAMERA':
            bpy.data.objects.remove(ob, do_unlink=True)
    for ob in bpy.data.objects:  # stüdyo gölge yakalayıcı zemin yerine gerçek arazi
        if getattr(ob, 'is_shadow_catcher', False):
            ob.hide_render = True
    G.arazi()
    w, gunes = G.dunya_gok(sc, elev=22.0, rot=120.0, guc=0.22)
    gunes.rotation_euler = (math.radians(68), 0, math.radians(35))
    gunes.data.color = (1.0, 0.9, 0.78)
    sc.view_settings.exposure = -0.2
    rnd = random.Random(8)
    # tesis çevresi: ağaç dizisi, çit
    for i in range(18):
        S.agac((-80 + i * 9.5 + rnd.uniform(-2, 2), 58 + rnd.uniform(-2, 2), 0.1), boy=rnd.uniform(7, 10), seed=200 + i)
    for i in range(10):
        S.agac((-84 + rnd.uniform(-2, 2), -40 + i * 10, 0.1), boy=rnd.uniform(7, 10), seed=230 + i)
    cit = S.pbr('Cit', '#8a9096', 0.5, 0.6)
    kit.box('Cit', (170, 0.06, 1.8), (0, -41.2, 0.9), cit)
    # stok sahası: daha büyük, nizami lime streçli palet blokları
    st = T5.strec_m()
    mer, boy = [], []
    for i in range(24):
        for j in range(8):
            if 6 <= i <= 7:
                continue  # forklift koridoru
            mer.append((-8 + i * 1.45, -30 + j * 1.3, 0.72))
            boy.append((1.25, 1.05, 1.3))
    kit.toplu_mesh('StokStrec', kit.sablon('kup'), mer, boy, None, st)


def main():
    kit.reset()
    v = ARGS.variant
    sc = kit.setup_render(*RES[v], samples=ARGS.samples, threshold=0.02, bounces=(6, 3, 3, 4))
    sc.render.use_persistent_data = True
    if os.environ.get('EGE_PREVIEW'):
        sc.render.resolution_percentage = int(os.environ['EGE_PREVIEW'])
    R.studyo(sc)
    sahne(sc)
    tir = H.ege_tiri()
    cam = kit.camera('Kamera', lens=30 if v == 'd' else 34, loc=(0, -80, 5), target=(0, YOL_Y, 2), fstop=11, focus=30)
    cam.data.dof.use_dof = False
    cam.data.clip_end = 3000
    frames = H_pass(FRAMES) if ARGS.frames == 'all' else [int(x) for x in ARGS.frames.split(',')]
    os.makedirs(ARGS.out, exist_ok=True)
    meta_path = os.path.join(ARGS.out, 'meta.json')
    meta = {'frames': FRAMES, 'res': list(RES[v]), 'hotspots': {}}
    for f in frames:
        u = f / (FRAMES - 1)
        # tır: kapıdan çıkar (dönüş), yolda hızlanır
        a = kit.smooth(kit.seg(u, 0.0, 0.25))
        tx = kit.lerp(8, 15, a) + 110 * kit.ease_in_out(kit.seg(u, 0.2, 1.0)) ** 1.4
        ty = kit.lerp(-35, YOL_Y + 2, a)
        tir.location = (tx, ty, 0.0)
        tir.rotation_euler[2] = kit.lerp(math.radians(-60), 0.0, a)
        hedef = Vector((tx - 2, ty, 2.0))
        # kamera: yandan takip → vinç yükselişi → tepeden
        y = kit.smoother(kit.seg(u, 0.45, 1.0))
        yan = hedef + Vector((9, -21, 4.0))
        ust_hedef = Vector((20, -10, 0))
        ust = ust_hedef + Vector((0, -0.01, 1)) * (420 if v == 'd' else 520)
        loc = yan.lerp(ust, y)
        bak = hedef.lerp(ust_hedef, y)
        cam.location = loc
        kit.aim(cam, bak)
        kit.kaydir(cam, v, 1.0 - y)
        hs = {}
        if u < 0.6:
            q = kit.project(cam, [tir.matrix_world @ Vector((-4.0, 0, 3.6))])[0]
            if q and 0 < q[0] < 1:
                hs['tir'] = q
        if 0.15 < u < 0.7:
            q = kit.project(cam, [Vector((0, 6, 14))])[0]
            if q and 0 < q[0] < 1 and 0 < q[1] < 1:
                hs['fabrika'] = q
        meta['hotspots'][str(f)] = hs
        kit.write_json(meta_path, meta)
        path = os.path.join(ARGS.out, f'{f:03d}.png')
        if ARGS.skip_existing and os.path.exists(path):
            continue
        t0 = time.time()
        kit.render_to(path)
        print(f'KARE {f} {time.time() - t0:.1f}s', flush=True)


def H_pass(n):
    import s1_urun
    return s1_urun.pass_order(n)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--variant', default='d')
    ap.add_argument('--frames', default='all')
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=24)
    ap.add_argument('--skip-existing', action='store_true')
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
