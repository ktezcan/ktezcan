"""
Stil R — zenginleştirilmiş hikâye: arka plan seçenekleri + yeni öğeler.

  arka_cyc   : stüdyo zemini (yumuşak yansıma, temas gölgesi, havada toz)
  arka_ege   : arkada puslu Ege silüeti (katman katman tepeler, deniz şeridi, ufuk ışığı)
  arka_kagit : mimari çizim kâğıdı (ızgara) — çizim sahneleri için
  isi        : ısı kalkanı — sıcak içeriden gelen ısı okları gazbeton duvarda söner
  kis        : kış gecesi — çatıda kar, yağan kar, sıcak pencereler
  urunler    : ürün ailesi kaidelerde — duvar bloğu, lento, U blok, panel, yapıştırıcı
  palet      : lime streçli paletler kamyonda (yeşil = bizim)
  fabrika    : fabrika minyatürü — otoklavlar, silolar, üretim holü

Kullanım: python stil_r4.py --sahne <ad> --out DIR [--samples N]
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
import stil_r2 as Q  # noqa: E402
import stil_r3 as T  # noqa: E402
import bina_detay as B  # noqa: E402

LIME = '#b8d84a'


def zemin(z, renk='#e4dfd8', boyut=600, parlak=0.12, golge_tutucu=True):
    """Zemin: varsayılan gölge tutucu — stüdyo fonu kesintisiz kalır, nesne temas gölgesiyle oturur."""
    m = Q.pbr('Zemin', renk, 0.55)
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Coat Weight'].default_value = parlak
    b.inputs['Coat Roughness'].default_value = 0.25
    ob = kit.box('Zemin', (boyut, boyut, 0.02), (0, 0, z - 0.01), m)
    ob.is_shadow_catcher = golge_tutucu
    return ob


def gok_gradyan(sc, alt='#efe6dc', ust='#d6dce3'):
    """Kameranın gördüğü gök: ekran yüksekliğine göre ufuk → üst geçişi (aydınlatmayı değiştirmez)."""
    nt = sc.world.node_tree
    gor = [n for n in nt.nodes if n.type == 'BACKGROUND' and n.inputs['Strength'].default_value > 1][0]
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Window'], sep.inputs[0])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[0].color = kit.srgb(alt)
    ramp.color_ramp.elements[1].color = kit.srgb(ust)
    nt.links.new(sep.outputs['Y'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], gor.inputs['Color'])


def toz(n=900, kutu=((-25, 25), (-20, 30), (0, 16)), r=0.03, guc=1.2):
    rnd = random.Random(1)
    pts = [(rnd.uniform(*kutu[0]), rnd.uniform(*kutu[1]), rnd.uniform(*kutu[2])) for _ in range(n)]
    kit.toplu_mesh('Toz', kit.sablon('ico', 1), pts, [r * rnd.uniform(0.5, 1.4) for _ in pts], None,
                   R.isiltili('Toz', (1.0, 0.97, 0.9), guc), yumusak=True)


def bina_tam(aksam=False):
    P, mats = T.bina_hazir(aksam)
    B.kur(P, mats)
    return P, mats


def sahne_arka_cyc(sc):
    bina_tam()
    zemin(-0.4)
    T.bina_kamera()


def sahne_arka_ege(sc):
    bina_tam()
    zemin(-0.4, renk='#e3dccf', parlak=0.0)
    gok_gradyan(sc, alt='#f1e8dd', ust='#dfe4ea')
    rnd = random.Random(7)
    # katman katman tepeler: uzaklaştıkça göğe karışan tonlar (hava perspektifi)
    katman = [(220, '#d2ccc4', 7), (330, '#dcd7d1', 10), (460, '#e5e1dc', 14)]
    for dist, renk, h in katman:
        m = Q.pbr('Tepe', renk, 1.0, 0.0, renk, 1.1)
        for i in range(7):
            x = (i - 3) * 120 + rnd.uniform(-40, 40)
            bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1.0, location=(x, dist, -0.4))
            o = bpy.context.active_object
            o.scale = (rnd.uniform(80, 130), 40, h * rnd.uniform(0.7, 1.2))
            o.data.materials.append(m)
            o.visible_shadow = False
            bpy.ops.object.shade_smooth()
    # deniz şeridi (ufuk ışığını yansıtır)
    dm = Q.pbr('Deniz', '#c9d3d8', 0.1, 0.0, '#c9d3d8', 0.8)
    kit.box('Deniz', (2000, 140, 0.02), (0, 150, -0.39), dm)
    T.bina_kamera(yon=(0.75, -1.0, 0.16), uzak=56, hedef=(0, 0, 5.5))


def sahne_arka_kagit(sc):
    P, mats = T.bina_hazir()
    T.cizgi_kur(P)
    m = bpy.data.materials.new('Kagit')
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    b.inputs['Roughness'].default_value = 0.9
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs[0])

    def cizgi(eksen, aralik, kalin):
        mod = nt.nodes.new('ShaderNodeMath')
        mod.operation = 'PINGPONG'
        mod.inputs[1].default_value = aralik / 2
        nt.links.new(sep.outputs[eksen], mod.inputs[0])
        lt = nt.nodes.new('ShaderNodeMath')
        lt.operation = 'LESS_THAN'
        lt.inputs[1].default_value = kalin
        nt.links.new(mod.outputs[0], lt.inputs[0])
        return lt
    a = cizgi('X', 1.0, 0.02)
    b2 = cizgi('Y', 1.0, 0.02)
    c = cizgi('X', 5.0, 0.05)
    d = cizgi('Y', 5.0, 0.05)
    mx = nt.nodes.new('ShaderNodeMath')
    mx.operation = 'MAXIMUM'
    nt.links.new(a.outputs[0], mx.inputs[0])
    nt.links.new(b2.outputs[0], mx.inputs[1])
    mx2 = nt.nodes.new('ShaderNodeMath')
    mx2.operation = 'MAXIMUM'
    nt.links.new(c.outputs[0], mx2.inputs[0])
    nt.links.new(d.outputs[0], mx2.inputs[1])
    sum_ = nt.nodes.new('ShaderNodeMath')
    sum_.operation = 'ADD'
    nt.links.new(mx.outputs[0], sum_.inputs[0])
    nt.links.new(mx2.outputs[0], sum_.inputs[1])
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.clamp_factor = True
    mix.inputs['A'].default_value = kit.srgb('#f3f1ec')
    mix.inputs['B'].default_value = kit.srgb('#a9c3d3')
    mul = nt.nodes.new('ShaderNodeMath')
    mul.operation = 'MULTIPLY'
    mul.inputs[1].default_value = 0.55
    nt.links.new(sum_.outputs[0], mul.inputs[0])
    nt.links.new(mul.outputs[0], mix.inputs['Factor'])
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Strength'].default_value = 1.0
    nt.links.new(mix.outputs['Result'], em.inputs['Color'])
    nt.links.new(em.outputs[0], nt.nodes['Material Output'].inputs['Surface'])
    kit.box('Kagit', (300, 300, 0.02), (0, 0, -0.41), m)
    sc.view_settings.view_transform = 'Standard'
    sc.view_settings.look = 'None'
    for n in sc.world.node_tree.nodes:
        if n.type == 'BACKGROUND' and n.inputs['Strength'].default_value > 1:
            n.inputs['Color'].default_value = kit.srgb('#f3f1ec')
            n.inputs['Strength'].default_value = 1.0
    T.bina_kamera()


def sahne_isi(sc):
    """Duvar kesiti: solda soğuk dış, sağda sıcak iç; ısı okları duvara girer ve söner."""
    aac = kit.aac_material('Gazbeton', bump=0.6)
    harc = Q.pbr('Harc', '#77736d', 0.95)
    mer, boy = [], []
    for sira in range(4):
        kay = 0.0 if sira % 2 == 0 else 0.3
        for i in range(-1, 3):
            x0 = -0.6 + i * 0.6 - kay
            a0, a1 = max(x0, -0.6), min(x0 + 0.6, 0.6)
            if a1 - a0 < 0.02:
                continue
            mer.append((0.0, (a0 + a1) / 2, -0.5 + (sira + 0.5) * 0.25))
            boy.append((0.2, a1 - a0 - 0.008, 0.242))
    kit.toplu_mesh('Duvar', kit.sablon('kup'), mer, boy, None, aac)
    kit.box('Harc', (0.12, 1.2, 1.0), (0, 0, 0), harc)
    # ısı okları: sağdan (+x, içerisi) gelir; duvara girince incelir ve söner
    rnd = random.Random(2)
    for j in range(5):
        z = -0.36 + j * 0.18
        y = rnd.uniform(-0.3, 0.3)
        for k in range(26):
            x = 1.0 - k * 0.04
            guc = 5.0 if x > 0.1 else max(0.0, 5.0 * (1 - (0.1 - x) / 0.18) ** 2)
            if guc <= 0.05:
                break
            r = 0.016 * (1.0 if x > 0.1 else max(0.25, 1 - (0.1 - x) / 0.18))
            bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=r, depth=0.045, location=(x, y, z), rotation=(0, math.pi / 2, 0))
            bpy.context.active_object.data.materials.append(Q.pbr(f'Ok{j}{k}', '#ff8a3c', 0.5, 0.0, '#ff8a3c', guc))
    # soğuk taraf: buz zerreleri + mavi ışık; sıcak taraf: amber ışık
    pts = [(rnd.uniform(-1.2, -0.15), rnd.uniform(-0.8, 0.8), rnd.uniform(-0.6, 0.6)) for _ in range(400)]
    kit.toplu_mesh('Buz', kit.sablon('ico', 1), pts, [0.004] * len(pts), None, R.isiltili('Buz', (0.75, 0.88, 1.0), 2.0), yumusak=True)
    for ad, loc, renk, e in (('Soguk', (-2.0, 0, 0.6), (0.6, 0.75, 1.0), 300), ('Sicak', (2.0, 0, 0.4), (1.0, 0.65, 0.35), 300)):
        ld = bpy.data.lights.new(ad, 'AREA')
        ld.energy = e
        ld.size = 1.5
        ld.color = renk
        lo = bpy.data.objects.new(ad, ld)
        lo.location = loc
        kit.link(lo)
        kit.aim(lo, (0, 0, 0))
    R.kamera(hedef=(0.1, 0, 0), yon=(0.2, -1.0, 0.28), uzak=4.6, lens=55, fstop=5.6)
    kit.sinematik(bloom=0.3, esik=1.2, boyut=0.55)


def sahne_kis(sc):
    P, mats = T.bina_hazir(aksam=True)
    B.kur(P, mats)
    Q.aksam_studyo(sc, koyu='#26303d', olcek=14, hedef=(0, 0, 4.5))
    kar = Q.pbr('Kar', '#f6f8fb', 0.6)
    W, D = B.XS[-1] - B.XS[0], B.YS[-1] - B.YS[0]
    kit.box('KarCati', (W - 0.2, D - 0.2, 0.18), (0, 0, B.KAT * B.FH + 0.28), kar)
    for (yuz, ax, k, a0, a1, n) in B.bolmeler():  # parapet üstü kar
        c = ((a0 + a1) / 2, k, B.KAT * B.FH + 0.82) if ax == 'X' else (k, (a0 + a1) / 2, B.KAT * B.FH + 0.82)
        s = (a1 - a0 + 0.4, 0.26, 0.08) if ax == 'X' else (0.26, a1 - a0 + 0.4, 0.08)
        kit.box('KarParapet', s, c, kar)
    zemin(-0.4, renk='#eef1f5', parlak=0.05)
    rnd = random.Random(4)
    pts = [(rnd.uniform(-22, 22), rnd.uniform(-22, 22), rnd.uniform(-0.3, 18)) for _ in range(3500)]
    kit.toplu_mesh('Kar', kit.sablon('ico', 1), pts, [0.035 * rnd.uniform(0.5, 1.3) for _ in pts], None,
                   Q.pbr('KarTane', '#ffffff', 0.5, 0.0, '#ffffff', 0.6), yumusak=True)
    T.bina_kamera()
    kit.sinematik(bloom=0.45, esik=1.0, boyut=0.65)


def sahne_urunler(sc):
    """Ürün ailesi: duvar bloğu, lento, U blok, döşeme/çatı paneli, yapıştırıcı torbası."""
    aac = kit.aac_material('Gazbeton', bump=0.6)
    kaide = Q.pbr('Kaide', '#f4f1ed', 0.6)
    sag, yuk = Q.baz()
    yer = [sag * ((k - 2) * 0.62) for k in range(5)]
    rz = math.atan2(sag.y, sag.x)
    for k, p in enumerate(yer):
        kd = kit.box('Kaide', (0.5, 0.5, 0.5), (p.x, p.y, -0.55), kaide)
        kd.rotation_euler[2] = rz
    # 1 duvar bloğu
    b = kit.gecmeli_blok('Blok', 0.6, 0.25, 0.25, aac)
    b.location = (yer[0].x, yer[0].y, -0.3)
    b.rotation_euler[2] = rz
    b.scale = (0.75, 0.75, 0.75)
    # 2 lento (uzun)
    l_ = kit.box('Lento', (0.9, 0.2, 0.2), (yer[1].x, yer[1].y, -0.2), aac)
    l_.rotation_euler[2] = rz
    # 3 U blok
    for (dx, dz, sx, sz) in ((-0.1, 0.0, 0.05, 0.25), (0.1, 0.0, 0.05, 0.25), (0.0, -0.1, 0.25, 0.05)):
        u = kit.box('UBlok', (0.45, sx, sz), (yer[2].x, yer[2].y, -0.175 + dz), aac)
        u.location = (yer[2].x + dx * math.cos(rz + math.pi / 2), yer[2].y + dx * math.sin(rz + math.pi / 2), -0.175 + dz)
        u.rotation_euler[2] = rz
    # 4 panel (dikine)
    pn = kit.box('Panel', (0.45, 0.15, 0.9), (yer[3].x, yer[3].y, 0.15), aac)
    pn.rotation_euler[2] = rz
    # 5 yapıştırıcı torbası (bizim ürün: lime bant)
    tb = kit.box('Torba', (0.34, 0.12, 0.46), (yer[4].x, yer[4].y, -0.07), Q.pbr('TorbaM', '#f1efea', 0.75))
    kit.bevel(tb, 0.03, 4)
    tb.rotation_euler[2] = rz
    bt = kit.box('TorbaBant', (0.345, 0.125, 0.08), (yer[4].x, yer[4].y, -0.02), Q.pbr('Bant', LIME, 0.6))
    bt.rotation_euler[2] = rz
    zemin(-0.8)
    R.kamera(hedef=(0.1, 0, -0.2), yon=(0.75, -1.0, 0.3), uzak=6.2, lens=50, fstop=8.0)


def sahne_palet(sc):
    """Lime streçli paletler, kamyon kasasında (yeşil = bizim)."""
    aac = kit.aac_material('Gazbeton', bump=0.4, tex_size=0.24)
    ahsap = Q.pbr('Ahsap', '#b68a5c', 0.8)
    strec = bpy.data.materials.new('Strec')
    strec.use_nodes = True
    sb = strec.node_tree.nodes['Principled BSDF']
    sb.inputs['Base Color'].default_value = kit.srgb(LIME)
    sb.inputs['Roughness'].default_value = 0.25
    sb.inputs['Transmission Weight'].default_value = 0.55
    sb.inputs['Alpha'].default_value = 0.85
    beyaz = Q.pbr('Kamyon', '#f2f1ee', 0.35)
    koyu = Q.pbr('Lastik', '#1d1f21', 0.8)
    cam = Q.pbr('KamyonCam', '#1a2228', 0.04)
    # kasa + kabin + şasi + tekerler (sade, stüdyo maketi)
    kit.box('Kasa', (6.0, 2.4, 0.2), (0, 0, 1.1), beyaz)
    kit.box('Sasi', (8.4, 1.2, 0.35), (1.0, 0, 0.75), koyu)
    kab = kit.box('Kabin', (1.9, 2.4, 2.2), (4.1, 0, 2.0), beyaz)
    kit.bevel(kab, 0.12, 3)
    kit.box('OnCam', (0.05, 2.0, 0.9), (5.06, 0, 2.5), cam)
    for x in (-2.2, -1.0, 4.0):
        for y in (-1.05, 1.05):
            bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.5, depth=0.35, location=(x, y, 0.5), rotation=(math.pi / 2, 0, 0))
            bpy.context.active_object.data.materials.append(koyu)
    # paletler: 2×4, her biri 1.2×1.0 taban, 5 sıra blok, streçli
    for i in range(4):
        for j in range(2):
            x, y = -2.3 + i * 1.45, -0.6 + j * 1.2
            kit.box('PaletTaban', (1.2, 1.0, 0.14), (x, y, 1.27), ahsap)
            mer, boy = [], []
            for s in range(5):
                for a in range(2):
                    for c in range(4):
                        mer.append((x - 0.3 + a * 0.6, y - 0.375 + c * 0.25, 1.34 + (s + 0.5) * 0.25))
                        boy.append((0.595, 0.245, 0.245))
            kit.toplu_mesh('PaletBlok', kit.sablon('kup'), mer, boy, None, aac)
            st = kit.box('Strec', (1.24, 1.04, 1.18), (x, y, 1.34 + 0.62), strec)
            kit.bevel(st, 0.04, 3)
    zemin(0.0)
    T.olcekle(6, (0, 0, 1.5), guc=0.6)
    R.kamera(hedef=(1.4, 0, 1.6), yon=(0.75, -1.0, 0.38), uzak=24, lens=55, fstop=8.0)


def sahne_fabrika(sc):
    """Fabrika minyatürü: üretim holü, otoklav tüpleri, silolar, kireç tesisi bacası."""
    beyaz = Q.pbr('Hol', '#eeece8', 0.6)
    gri = Q.pbr('Gri', '#b9bcbf', 0.45, 0.6)
    lime = Q.pbr('Serit', LIME, 0.5)
    kit.box('Hol', (40, 18, 9), (0, 0, 4.5), beyaz)
    kit.box('Cati', (40.6, 18.6, 0.4), (0, 0, 9.2), Q.pbr('CatiM', '#d6d4d0', 0.5))
    kit.box('Serit', (40.05, 18.05, 0.5), (0, 0, 7.6), lime)  # bizim: kurumsal lime şerit
    for i in range(4):  # otoklavlar
        bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=1.4, depth=24, location=(-6 + i * 4.0, -16, 1.6), rotation=(math.pi / 2, 0, 0))
        bpy.context.active_object.data.materials.append(gri)
        bpy.ops.object.shade_smooth()
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.4, location=(0, 0, 0))
        o = bpy.context.active_object
        o.location = (-6 + i * 4.0, -16 - 12.0, 1.6)
        o.scale = (1, 0.35, 1)
        o.data.materials.append(gri)
        bpy.ops.object.shade_smooth()
    for i in range(3):  # silolar
        bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=2.2, depth=16, location=(26, -5 + i * 5, 8))
        bpy.context.active_object.data.materials.append(beyaz)
        bpy.ops.object.shade_smooth()
        bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=2.2, radius2=0.3, depth=2.0, location=(26, -5 + i * 5, 17))
        bpy.context.active_object.data.materials.append(gri)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.9, depth=28, location=(-24, 6, 14))
    bpy.context.active_object.data.materials.append(beyaz)
    kit.box('Bant', (2.0, 18, 0.6), (-24, 6, 26), lime)
    zemin(0.0)
    T.olcekle(40, (0, 0, 4), guc=0.6)
    R.kamera(hedef=(4, -4, 6), yon=(0.75, -1.0, 0.5), uzak=165, lens=55, fstop=11.0)


SAHNELER = {k[6:]: v for k, v in globals().items() if k.startswith('sahne_')}


def main():
    kit.reset()
    sc = kit.setup_render(1280, 720, samples=ARGS.samples, threshold=0.015, bounces=(6, 3, 3, 2))
    R.studyo(sc)
    SAHNELER[ARGS.sahne](sc)
    os.makedirs(ARGS.out, exist_ok=True)
    kit.render_to(os.path.join(ARGS.out, f'{ARGS.sahne}.png'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--sahne', default='arka_cyc')
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=48)
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
