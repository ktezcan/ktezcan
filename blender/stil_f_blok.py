"""
Stil F+I — blok sahnesi: izometrik kaide üstünde tek gazbeton blok.
--tarama X: x < X bölgesi röntgen; blok saydamlaşır ve içindeki binlerce küçük
kapalı hava hücresi görünür ("hafif, çünkü içi hava"). Opak yarı içeriyi örter.

Kullanım: python stil_f_blok.py --out DIR [--tarama 0.0] [--ad blok_FI]
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
import stil_f as F  # noqa: E402


def gozenekler(L, T, H, sayi, seed=7):
    """Bloğun içinde rastgele küçük küreler (hava hücreleri) — tek ağ."""
    rnd = random.Random(seed)
    mer, boy = [], []
    for _ in range(sayi):
        r = min(0.0075, 0.0012 * rnd.lognormvariate(0.6, 0.45))
        mer.append((rnd.uniform(-L / 2 + r, L / 2 - r), rnd.uniform(-T / 2 + r, T / 2 - r), rnd.uniform(r, H - r)))
        boy.append(r)
    ob = kit.toplu_mesh('Gozenek', kit.sablon('ico', 2), mer, boy, None, None, yumusak=True)
    m = bpy.data.materials.new('FGozenek')
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    N, Ln = nt.nodes.new, nt.links.new
    out = N('ShaderNodeOutputMaterial')
    lw = N('ShaderNodeLayerWeight')
    lw.inputs['Blend'].default_value = 0.5
    mul = N('ShaderNodeMath')
    mul.operation = 'MULTIPLY'
    mul.inputs[1].default_value = 4.0
    Ln(lw.outputs['Facing'], mul.inputs[0])
    add = N('ShaderNodeMath')  # opak boncuk: merkez sönük, kenar parlak (saydamlık maliyeti yok)
    add.inputs[1].default_value = 0.8
    Ln(mul.outputs[0], add.inputs[0])
    em = N('ShaderNodeEmission')
    em.inputs['Color'].default_value = kit.srgb('#d9ef8a')
    Ln(add.outputs[0], em.inputs['Strength'])
    Ln(em.outputs[0], out.inputs['Surface'])
    ob.data.materials.append(m)
    ob.visible_shadow = False
    return ob


def main():
    kit.reset()
    sc = kit.setup_render(1280, 720, samples=ARGS.samples, threshold=0.02, bounces=(4, 2, 2, 2))
    sc.cycles.transparent_max_bounces = 16
    x0 = ARGS.tarama
    L, H, T = 0.60, 0.25, 0.25
    urun = F.karisik('F_urun', F.URUN_RENK[0], F.URUN_RENK[1], *F.I_RENK['urun'], x0, bant=0.0025)
    blk = kit.gecmeli_blok('Gazbeton', L, H, T, urun)
    if x0 is not None:
        gozenekler(L - 0.004, T - 0.004, H - 0.002, ARGS.gozenek)
    # kaide (yuvarlak köşeli tabla) + arka zemin
    kaide = kit.box('Kaide', (1.5, 1.2, 0.08), (0, 0, -0.04), F.mat_basit('FKaide', '#f1e4d1', 0.92))
    kit.bevel(kaide, width=0.03, segments=4, angle=60)
    kk = kit.box('KaideKenar', (1.5, 1.2, 0.12), (0, 0, -0.12), F.mat_basit('FKaideKenar', '#d4ad85', 0.9))
    kit.bevel(kk, width=0.04, segments=4, angle=60)
    kit.box('Arka', (60, 60, 0.01), (0, 0, -0.6), F.mat_basit('FArka', '#e8d3bb', 1.0))
    kit.halo_ring('Hale', radius=0.48, width=0.008, strength=6.0, z=0.001)
    if x0 is not None:
        kit.box('TaramaHat', (0.004, 1.1, 0.002), (x0, 0, 0.001), F.mat_basit('FTarama', F.LIME, 0.5, F.LIME, 10.0))
    # ışık: yumuşak güneş + sıcak gök
    sd = bpy.data.lights.new('Gunes', 'SUN')
    sd.energy = 3.2
    sd.angle = math.radians(7)
    sd.color = (1.0, 0.93, 0.85)
    sun = bpy.data.objects.new('Gunes', sd)
    sun.rotation_euler = (math.radians(50), 0, math.radians(-28))
    kit.link(sun)
    w = bpy.data.worlds.new('FDunya')
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get('Background')
    bg.inputs['Color'].default_value = (*kit.srgb('#f6e2c8')[:3], 1.0)
    bg.inputs['Strength'].default_value = 0.6
    sc.view_settings.look = 'AgX - Punchy'
    sc.view_settings.exposure = -0.1
    kit.sinematik(bloom=0.3, esik=1.4, boyut=0.6)
    # izometrik kamera
    target = Vector((0.0, 0.0, 0.1))
    cam = kit.camera('Kamera', lens=50, loc=(5, -5, 4.1), target=target)
    cam.location = target + Vector((1, -1, 0.82)).normalized() * 8
    kit.aim(cam, target)
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = ARGS.olcek
    cam.data.clip_end = 100
    cam.data.shift_x = -0.17 if ARGS.variant == 'd' else 0.0
    sc.camera = cam
    os.makedirs(ARGS.out, exist_ok=True)
    kit.render_to(os.path.join(ARGS.out, f'{ARGS.ad}.png'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--tarama', type=float, default=None)
    ap.add_argument('--olcek', type=float, default=1.15)
    ap.add_argument('--gozenek', type=int, default=4000)
    ap.add_argument('--variant', default='')
    ap.add_argument('--ad', default='blok_FI')
    ap.add_argument('--samples', type=int, default=48)
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
