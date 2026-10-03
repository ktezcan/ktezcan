"""
Stil F (izometrik pastel) — geliştirilmiş + I (röntgen) karışımı.

Bina sahnesi bir diorama karosunun üstünde, ortografik izometrik kamerayla.
--tarama X verilirse x < X bölgesi röntgen (saydam gövde, lime gazbeton,
mavi karkas) olur; sınırda ince lime tarama çizgisi çizilir. Tarama
animasyonda soldan sağa süpürülerek binanın içini gösterir.

Kullanım: python stil_f.py --out DIR [--u 0.78] [--tarama 1.5] [--ad bina_F2]
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

LIME = '#b8d84a'
URUN = ('Duvar', 'Lento', 'CatiPaneli', 'Istif', 'Gazbeton', 'GevsekBlok')
KORU = ('Strec', 'Hale', 'SahaHalka', 'Lamba', 'IcM', 'Toz', 'Yildiz', 'Huzme', 'Video')

# F paleti: (renk, pürüzlülük) — yeşil yalnız bizim üründe (streç)
PALET = [
    ('Cam', ('#a9cddd', 0.12)),
    ('Beton', ('#e0a98a', 0.85)),
    ('Tabla', ('#dcc6aa', 0.9)),
    ('Vinc', ('#f2b33d', 0.55)),
    ('Ahsap', ('#c98f5a', 0.8)),
    ('Dograma', ('#55636e', 0.45)),
    ('Siluet', ('#55636e', 0.9)),
    ('Direk', ('#8d969c', 0.5)),
    ('Halat', ('#55636e', 0.6)),
]
URUN_RENK = ('#fbf7f0', 0.82)
# röntgen renkleri: ürün lime, karkas mavi, diğer gri-mavi
I_RENK = {'urun': (LIME, 1.0, 0.95), 'Beton': ('#79bfe0', 0.8, 0.97), 'diger': ('#7d97a6', 0.5, 0.975)}


def urun_mu(mn):
    return mn.startswith(URUN)


def karisik(name, f_hex, f_rough, i_hex, i_guc, i_saydam, x0, bant=0.07):
    """F (mat pastel) ile I (röntgen) karışımı: dünya x < x0 → röntgen; sınırda lime çizgi."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    N = nt.nodes.new
    L = nt.links.new
    out = N('ShaderNodeOutputMaterial')
    f = N('ShaderNodeBsdfPrincipled')
    f.inputs['Base Color'].default_value = kit.srgb(f_hex)
    f.inputs['Roughness'].default_value = f_rough
    if 'Coat Weight' in f.inputs:
        f.inputs['Coat Weight'].default_value = 0.0
    if x0 is None:
        L(f.outputs[0], out.inputs['Surface'])
        return m
    # röntgen kısmı: fresnel kenar parıltısı + saydamlık
    lw = N('ShaderNodeLayerWeight')
    lw.inputs['Blend'].default_value = 0.35
    mul = N('ShaderNodeMath')
    mul.operation = 'MULTIPLY'
    mul.inputs[1].default_value = i_guc
    L(lw.outputs['Facing'], mul.inputs[0])
    em = N('ShaderNodeEmission')
    em.inputs['Color'].default_value = kit.srgb(i_hex)
    L(mul.outputs[0], em.inputs['Strength'])
    tr = N('ShaderNodeBsdfTransparent')
    add = N('ShaderNodeAddShader')
    L(em.outputs[0], add.inputs[0])
    L(tr.outputs[0], add.inputs[1])
    em2 = N('ShaderNodeEmission')
    em2.inputs['Color'].default_value = kit.srgb(i_hex)
    em2.inputs['Strength'].default_value = i_guc * 0.05
    ix = N('ShaderNodeMixShader')
    ix.inputs['Fac'].default_value = i_saydam
    L(em2.outputs[0], ix.inputs[1])
    L(add.outputs[0], ix.inputs[2])
    # bölge maskesi
    geo = N('ShaderNodeNewGeometry')
    sep = N('ShaderNodeSeparateXYZ')
    L(geo.outputs['Position'], sep.inputs[0])
    lt = N('ShaderNodeMath')
    lt.operation = 'LESS_THAN'
    lt.inputs[1].default_value = x0
    L(sep.outputs['X'], lt.inputs[0])
    mix = N('ShaderNodeMixShader')
    L(lt.outputs[0], mix.inputs['Fac'])
    L(f.outputs[0], mix.inputs[1])
    L(ix.outputs[0], mix.inputs[2])
    # tarama çizgisi: |x - x0| < 0.07 → lime ışık
    sub = N('ShaderNodeMath')
    sub.operation = 'SUBTRACT'
    sub.inputs[1].default_value = x0
    L(sep.outputs['X'], sub.inputs[0])
    ab = N('ShaderNodeMath')
    ab.operation = 'ABSOLUTE'
    L(sub.outputs[0], ab.inputs[0])
    band = N('ShaderNodeMath')
    band.operation = 'LESS_THAN'
    band.inputs[1].default_value = bant
    L(ab.outputs[0], band.inputs[0])
    eb = N('ShaderNodeEmission')
    eb.inputs['Color'].default_value = kit.srgb(LIME)
    eb.inputs['Strength'].default_value = 14.0
    mix2 = N('ShaderNodeMixShader')
    L(band.outputs[0], mix2.inputs['Fac'])
    L(mix.outputs[0], mix2.inputs[1])
    L(eb.outputs[0], mix2.inputs[2])
    L(mix2.outputs[0], out.inputs['Surface'])
    return m


def mat_basit(name, hexcol, rough=0.8, emis=None, es=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = kit.srgb(hexcol)
    b.inputs['Roughness'].default_value = rough
    if emis:
        b.inputs['Emission Color'].default_value = kit.srgb(emis)
        b.inputs['Emission Strength'].default_value = es
    return m


def malzemeler(x0):
    onbellek = {}

    def al(mn):
        if urun_mu(mn):
            key, (fh, fr), (ih, ig, isy) = 'urun', URUN_RENK, I_RENK['urun']
        else:
            key, (fh, fr) = 'diger', ('#d8cfc4', 0.8)
            for onek, deger in PALET:
                if mn.startswith(onek) or onek in mn:
                    key, (fh, fr) = onek, deger
                    break
            ih, ig, isy = I_RENK.get(key, I_RENK['diger'])
        if key not in onbellek:
            xx = x0 if key in ('urun', 'Beton', 'Cam', 'Dograma') else None  # röntgen yalnız binada
            onbellek[key] = karisik(f'F_{key}', fh, fr, ih, ig, isy, xx)
        return onbellek[key]

    for ob in bpy.data.objects:
        if ob.type != 'MESH':
            continue
        for i, slot in enumerate(ob.material_slots):
            mt = slot.material
            if mt is None or any(k in mt.name for k in KORU) or mt.name.startswith('F'):
                continue
            ob.material_slots[i].material = al(mt.name)


def sil(onekler):
    for ob in list(bpy.data.objects):
        if ob.name.startswith(onekler):
            bpy.data.objects.remove(ob, do_unlink=True)


def agac(konum, boy, renk_m, govde_m, tip):
    x, y = konum
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.16, depth=boy * 0.35, location=(x, y, boy * 0.175))
    g = bpy.context.active_object
    g.name = 'AgacGovde'
    g.data.materials.append(govde_m)
    if tip == 'koni':
        bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=boy * 0.32, radius2=0.0, depth=boy * 0.8, location=(x, y, boy * 0.3 + boy * 0.4))
    else:
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=boy * 0.33, location=(x, y, boy * 0.35 + boy * 0.3))
    t = bpy.context.active_object
    t.name = 'AgacTac'
    t.data.materials.append(renk_m)
    bpy.ops.object.shade_flat()


def diorama():
    """Karo kaide + arka zemin + pastel ağaçlar + yol."""
    sil(('Zemin', 'Tepe'))
    kaide_m = mat_basit('FKaide', '#f1e4d1', 0.92)
    kenar_m = mat_basit('FKaideKenar', '#d4ad85', 0.9)
    k = kit.box('Kaide', (40.0, 34.0, 0.2), (-3.0, -1.0, -0.1), kaide_m)
    kit.bevel(k, width=0.1, segments=2, angle=60)
    kk = kit.box('KaideKenar', (40.0, 34.0, 1.6), (-3.0, -1.0, -1.0), kenar_m)
    kit.bevel(kk, width=0.5, segments=4, angle=60)
    arka = kit.box('Arka', (900, 900, 0.1), (0, 0, -4.0), mat_basit('FArka', '#e8d3bb', 1.0))
    arka.visible_glossy = False
    # yol: kaidenin önünde, kesik çizgili
    yol_m = mat_basit('FYol', '#cdbfae', 0.95)
    cizgi_m = mat_basit('FYolCizgi', '#fbf6ee', 0.8)
    kit.box('Yol', (40.0, 4.2, 0.04), (-3.0, -14.6, 0.02), yol_m)
    for i in range(10):
        kit.box('YolCizgi', (1.6, 0.18, 0.05), (-21.0 + i * 4.0, -14.6, 0.04), cizgi_m)
    # ağaçlar: şeftali/mercan/kum tonları (yeşil yalnız bizim)
    tac = [mat_basit('FAgac1', '#f29466', 0.85), mat_basit('FAgac2', '#e4704f', 0.85), mat_basit('FAgac3', '#f0b45e', 0.85)]
    govde = mat_basit('FGovde', '#a7795a', 0.9)
    rnd = random.Random(5)
    yerler = [(-20, 12), (-17, 13.5), (-21, 8.5), (12, 13), (14.5, 10.5), (15, 6), (-20.5, -8), (14.5, -9), (11.5, -11.2),
              (-14, 14), (8.5, 14), (-21, 2.5)]
    for i, p in enumerate(yerler):
        agac(p, rnd.uniform(2.6, 4.2), tac[i % 3], govde, 'koni' if i % 2 else 'top')
    araba(-13.0, -13.6, 0.0, '#7fa7c9')
    araba(7.5, -15.6, math.pi, '#f0d9a8')


def araba(x, y, yon, renk_hex):
    g = mat_basit(f'FAraba{renk_hex}', renk_hex, 0.4)
    koyu = mat_basit('FTeker', '#3d4449', 0.7)
    cam_m = mat_basit('FArabaCam', '#a9cddd', 0.15)
    c, s_ = math.cos(yon), math.sin(yon)

    def yer(dx, dy, z):
        return (x + dx * c - dy * s_, y + dx * s_ + dy * c, z)
    parcalar = [kit.box('Araba', (4.0, 1.8, 0.75), yer(0, 0, 0.6), g),
                kit.box('ArabaKabin', (2.1, 1.6, 0.62), yer(-0.2, 0, 1.28), cam_m),
                kit.box('ArabaTavan', (2.0, 1.62, 0.1), yer(-0.2, 0, 1.62), g)]
    for dx in (-1.3, 1.3):
        for dy in (-0.82, 0.82):
            bpy.ops.mesh.primitive_cylinder_add(vertices=14, radius=0.36, depth=0.24, location=yer(dx, dy, 0.36), rotation=(math.pi / 2, 0, yon))
            w = bpy.context.active_object
            w.name = 'ArabaTeker'
            w.data.materials.append(koyu)
    for p in parcalar[:1] + parcalar[2:]:
        kit.bevel(p, width=0.12, segments=3, angle=60)
    for p in parcalar:
        p.rotation_euler[2] = yon


def vinc_kucult(k=0.42, merkez=(-15.0, 13.0), yeni=(-11.0, 8.5)):
    """Vinci küçült ve izometrik kadraja sığacak yere taşı (binanın sol arkası)."""
    for ob in bpy.data.objects:
        if ob.name.startswith('Vinc'):
            p = ob.location
            ob.location = (yeni[0] + (p.x - merkez[0]) * k, yeni[1] + (p.y - merkez[1]) * k, p.z * k)
            ob.scale = (ob.scale.x * k, ob.scale.y * k, ob.scale.z * k)


def tarama_zemini(x0):
    """Kaide üstünde tarama hattı (lime) — taranan bölge hafif lime ışıltılı."""
    if x0 is None:
        return
    m = mat_basit('FTarama', LIME, 0.5, LIME, 10.0)
    kit.box('TaramaHat', (0.08, 30.0, 0.03), (x0, -1.0, 0.015), m)


def main():
    import s3_bina as s
    s.ARGS = argparse.Namespace(samples=ARGS.samples)
    cam, objs, wall_mats, dusk = s.build('d')
    u = ARGS.u
    t = s.yapim_t(u)
    for mat in wall_mats.values():
        for n in mat.node_tree.nodes:
            if n.type == 'MATH' and n.operation == 'SUBTRACT' and not n.inputs[0].is_linked and abs(n.inputs[1].default_value - s.T_WALL0) < 1e-6:
                n.inputs[0].default_value = t
    s.apply_state(objs, t)
    s.alacakaranlik(dusk, u)
    sc = bpy.context.scene

    x0 = ARGS.tarama
    diorama()
    vinc_kucult()
    malzemeler(x0)
    tarama_zemini(x0)
    for ob in bpy.data.objects:  # sis/hüzme yok; yumuşak güneş + gök
        if ob.type == 'LIGHT' and ob.data.type in ('AREA', 'POINT', 'SPOT') and not ob.name.startswith('Lamba'):
            ob.data.energy = 0
        if ob.type == 'LIGHT' and ob.data.type == 'SUN':
            ob.data.angle = math.radians(7)
            ob.data.color = (1.0, 0.93, 0.85)
            ob.rotation_euler = (math.radians(52), 0, math.radians(-28))
    sil(('Sis',))
    w = bpy.data.worlds.new('FDunya')
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get('Background')
    bg.inputs['Color'].default_value = (*kit.srgb('#f6e2c8')[:3], 1.0)
    bg.inputs['Strength'].default_value = 0.6
    sc.view_settings.look = 'AgX - Punchy'
    sc.view_settings.exposure = ARGS.pozlama
    if x0 is not None:
        sc.cycles.transparent_max_bounces = 64
        kit.sinematik(bloom=0.3, esik=1.4, boyut=0.6)

    # izometrik kamera
    target = Vector((-3.0, -1.0, 4.5))
    cam.location = target + Vector((1, -1, 0.82)).normalized() * 140
    kit.aim(cam, target)
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = ARGS.olcek
    cam.data.clip_end = 1000
    cam.data.shift_x = cam.data.shift_y = 0.0
    if ARGS.variant == 'd':
        cam.data.shift_x = -0.17  # anlatım sütunu solda
    cam.data.dof.use_dof = False
    sc.render.resolution_x, sc.render.resolution_y = 1280, 720
    os.makedirs(ARGS.out, exist_ok=True)
    kit.render_to(os.path.join(ARGS.out, f'{ARGS.ad}.png'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--u', type=float, default=0.78)
    ap.add_argument('--tarama', type=float, default=None)
    ap.add_argument('--olcek', type=float, default=50.0)
    ap.add_argument('--variant', default='')
    ap.add_argument('--pozlama', type=float, default=-0.1)
    ap.add_argument('--ad', default='bina_F2')
    ap.add_argument('--samples', type=int, default=48)
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
