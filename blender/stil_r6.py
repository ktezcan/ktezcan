"""
Stil R — sokak sahnesi: ayrıntılı bina (her pencerede farklı oda) + kaldırım, yol, ağaçlar,
lambalar, park etmiş ve geçen arabalar, bisikletli, yürüyen insanlar.

Kullanım: python stil_r6.py --sahne sokak|pencere --out DIR [--samples N]
"""
import argparse
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
import stil_r as R  # noqa: E402
import stil_r3 as T  # noqa: E402
import stil_r4 as F  # noqa: E402
import bina_detay as B  # noqa: E402
import sokak as S  # noqa: E402
import insan as I  # noqa: E402


def cam_gercek():
    m = bpy.data.materials.new('CamGercek')
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = kit.srgb('#dfe9ec')
    b.inputs['Transmission Weight'].default_value = 1.0
    b.inputs['Roughness'].default_value = 0.02
    b.inputs['IOR'].default_value = 1.5
    return m


def bina_ve_odalar(sc, isik=True):
    P, mats = T.bina_hazir()
    mats['cam'] = cam_gercek()
    B.kur(P, mats)
    rnd = random.Random(7)
    tipler = S.ODA_TIPLERI[:]
    for p in P:
        if p['tur'] != 'cam' or p['n'] == (0, 1, 0):
            continue
        gen = (B.XS[1] - B.XS[0] - B.COL - 0.1) if p['n'][1] != 0 else (B.YS[1] - B.YS[0] - B.COL - 0.1)
        if not tipler:
            tipler = S.ODA_TIPLERI[:]
        tip = tipler.pop(rnd.randrange(len(tipler)))
        S.oda(p['c'], p['n'], gen, B.FH - B.SLAB - 0.05, tip, rnd, isik=isik and rnd.random() < 0.8)
    return P


def sokak_doldur(y0):
    S.yol(y0)
    rnd = random.Random(3)
    for i, x in enumerate((-17.0, -9.5, 8.5, 16.0)):
        S.agac((x, y0 - 2.6, 0.15), boy=rnd.uniform(6.5, 8.0), seed=i)
    for i, x in enumerate((-20.0, 13.0, 24.0)):
        S.agac((x, y0 - 12.9, 0.15), boy=rnd.uniform(6.0, 7.5), seed=10 + i)
    for x in (-11.0, 4.5, 18.0):
        S.lamba((x, y0 - 3.1, 0.15), yon=-math.pi / 2)
    S.araba((-6.5, y0 - 4.6, 0.05), 0.0, '#8f1f1a', 'Park1')
    S.araba((13.5, y0 - 4.6, 0.05), 0.0, '#e9e9e6', 'Park2')
    S.araba((2.0, y0 - 9.2, 0.05), math.pi, '#24364f', 'Gecen')
    S.bisiklet((-1.5, y0 - 5.6, 0.05), 0.0, '#c24a2c', 'Bisiklet', pedal=0.6)
    I.insan('erkek', 'bisiklet', 0.2, dict(ust='#2e4a63', alt='#2b2d30', sac='#1d1712', ten='#c49274'),
            konum=(-1.62, y0 - 5.6, 0.05), yon=math.pi / 2, ad='Bisikletli')
    kisiler = [
        ('kadin', 0.15, dict(ust='#d9cbb4', alt='#2f3c4c', sac='#3b2a1d', ten='#d2a688'), (-3.5, y0 - 1.6), math.pi / 2),
        ('cocuk', 0.55, dict(ust='#e0b23a', alt='#3a4a6a', sac='#2a1d14', ten='#d2a688'), (-2.8, y0 - 1.3), math.pi / 2),
        ('erkek', 0.4, dict(ust='#5f6f5a', alt='#3a3530', sac='#2a2018', ten='#b98a6a', kol='uzun'), (6.5, y0 - 2.0), -math.pi / 2),
        ('yasli', 0.7, dict(ust='#7a7468', alt='#4a4540', sac='#bdb8b0', kol='uzun'), (10.5, y0 - 1.5), math.pi / 2),
        ('kadin', 0.85, dict(ust='#b9583f', alt='#26303d', sac='#1d1712', ten='#c49274'), (-9.0, y0 - 12.3), -math.pi / 2),
        ('erkek', 0.05, dict(ust='#f0eee9', alt='#4f6a85', sac='#3b2a1d'), (5.0, y0 - 13.0), math.pi / 2),
    ]
    for i, (tip, faz, g, (x, y), yon) in enumerate(kisiler):
        I.insan(tip, 'yuru', faz, g, konum=(x, y, 0.15), yon=yon, ad=f'Yaya{i}')


def temel_gizle():
    for ob in bpy.data.objects:
        if ob.name.startswith('Bina_temel'):
            ob.hide_render = True  # gölge tutucu zeminin altında kalan temel görünmesin


def ege_fon(sc):
    """Arkada puslu Ege tepeleri + ufuk gradyanı (stil_r4.arka_ege ile aynı dil)."""
    F.gok_gradyan(sc, alt='#f1e8dd', ust='#dfe4ea')
    rnd = random.Random(7)
    for dist, renk, h in ((220, '#d2ccc4', 8), (330, '#dcd7d1', 11), (460, '#e5e1dc', 15)):
        m = S.pbr('Tepe' + renk, renk, 1.0, 0.0, renk, 1.1)
        for i in range(7):
            x = (i - 3) * 120 + rnd.uniform(-40, 40)
            bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1.0, location=(x, dist, 0.0))
            o = bpy.context.active_object
            o.scale = (rnd.uniform(80, 130), 40, h * rnd.uniform(0.7, 1.2))
            o.data.materials.append(m)
            o.visible_shadow = False
            bpy.ops.object.shade_smooth()


def gunes():
    sd = bpy.data.lights.new('Gunes', 'SUN')
    sd.energy = 2.2
    sd.angle = math.radians(2.0)
    sd.color = (1.0, 0.93, 0.84)
    so = bpy.data.objects.new('Gunes', sd)
    so.rotation_euler = (math.radians(55), 0, math.radians(-35))
    kit.link(so)


def sahne_sokak(sc):
    bina_ve_odalar(sc)
    y0 = B.YS[0] - B.WT / 2 - 0.4
    sokak_doldur(y0)
    F.zemin(0.0)
    temel_gizle()
    ege_fon(sc)
    gunes()
    R.kamera(hedef=(1.0, -6.0, 3.6), yon=(0.35, -1.0, 0.22), uzak=30, lens=35, fstop=11, kayma=0.0)


def sahne_aksam(sc):
    """Akşam sokağı: her pencere başka bir oda olarak yanar, lambalar ve farlar açık."""
    bina_ve_odalar(sc, isik=True)
    y0 = B.YS[0] - B.WT / 2 - 0.4
    sokak_doldur(y0)
    F.zemin(0.0)
    temel_gizle()
    import stil_r2 as Q2
    Q2.aksam_studyo(sc, koyu='#26303d', olcek=14, hedef=(0, 0, 4.5))
    for ob in bpy.data.objects:
        if ob.name.startswith('LambaCam') and ob.data.materials:
            ob.data.materials[0] = S.pbr('LambaCamYanik', '#fff4dc', 0.2, 0.0, '#ffd59a', 12.0)
            ld = bpy.data.lights.new('SokakLamba', 'SPOT')
            ld.energy = 900
            ld.spot_size = math.radians(110)
            ld.color = (1.0, 0.8, 0.55)
            lo = bpy.data.objects.new('SokakLamba', ld)
            lo.location = ob.matrix_world.translation - Vector((0, 0, 0.1))
            kit.link(lo)
    kit.sinematik(bloom=0.45, esik=1.0, boyut=0.6)
    R.kamera(hedef=(1.0, -6.0, 3.6), yon=(0.35, -1.0, 0.22), uzak=30, lens=35, fstop=11, kayma=0.0)


def sahne_pencere(sc):
    bina_ve_odalar(sc)
    y0 = B.YS[0] - B.WT / 2 - 0.4
    sokak_doldur(y0)
    F.zemin(0.0)
    temel_gizle()
    gunes()
    R.kamera(hedef=(-1.2, -4.0, 4.4), yon=(0.45, -1.0, -0.05), uzak=6.5, lens=28, fstop=5.6, kayma=0.0)


SAHNELER = {k[6:]: v for k, v in globals().items() if k.startswith('sahne_')}


def main():
    kit.reset()
    sc = kit.setup_render(1280, 720, samples=ARGS.samples, threshold=0.02, bounces=(6, 3, 3, 4))
    sc.cycles.transparent_max_bounces = 16
    R.studyo(sc)
    SAHNELER[ARGS.sahne](sc)
    os.makedirs(ARGS.out, exist_ok=True)
    kit.render_to(os.path.join(ARGS.out, f'{ARGS.sahne}.png'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--sahne', default='sokak')
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=48)
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
