"""
Sokak öğeleri (kod ile, gerçek ölçü): araba, bisiklet, ağaç, sokak lambası, kaldırım/yol,
ve binadaki her pencereye ayrı bir oda (salon, mutfak, yatak, çalışma, çocuk, perde kapalı, jaluzi).
"""
import math
import random

import bpy
import numpy as np
from mathutils import Vector

import kit


def pbr(name, hexcol, rough=0.6, metal=0.0, emis=None, es=0.0, coat=0.0, trans=0.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = kit.srgb(hexcol)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if emis:
        b.inputs['Emission Color'].default_value = kit.srgb(emis)
        b.inputs['Emission Strength'].default_value = es
    if coat:
        b.inputs['Coat Weight'].default_value = coat
        b.inputs['Coat Roughness'].default_value = 0.03
    if trans:
        b.inputs['Transmission Weight'].default_value = trans
    return m


def boru(a, b, r, m, v=12, ad='Boru'):
    """İki nokta arasında silindir."""
    a, b = Vector(a), Vector(b)
    d = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d.length, location=(a + b) / 2)
    o = bpy.context.active_object
    o.name = ad
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = d.to_track_quat('Z', 'Y')
    o.data.materials.append(m)
    bpy.ops.object.shade_smooth()
    return o


def _grupla(objs, ad, konum, yon):
    """Nesneleri boş bir ebeveyne bağla, sonra taşı/döndür."""
    e = bpy.data.objects.new(ad, None)
    kit.link(e)
    for o in objs:
        o.parent = e
    e.location = konum
    e.rotation_euler[2] = yon
    return e


# ------------------------------------------------------------------ araba
def araba(konum=(0, 0, 0), yon=0.0, renk='#8f1f1a', ad='Araba'):
    """Hatchback: kesitlerden örülmüş gövde (alt bölümlemeli), çamurluk kemerleri, cam, farlar, jantlar."""
    once = set(bpy.data.objects)
    L, W = 4.25, 1.80
    xs = np.linspace(-L / 2, L / 2, 34)

    def profil(x):
        u = (x + L / 2) / L  # 0 arka … 1 ön
        alt = 0.22
        # bel çizgisi ve tavan
        bel = np.interp(u, [0, 0.06, 0.2, 0.7, 0.9, 1.0], [0.62, 0.92, 0.98, 0.94, 0.80, 0.55])
        tavan = np.interp(u, [0, 0.05, 0.13, 0.26, 0.55, 0.68, 0.74, 1.0], [0.70, 1.08, 1.38, 1.47, 1.46, 1.08, 0.96, 0.6])
        tavan = max(tavan, bel)
        gen = np.interp(u, [0, 0.04, 0.12, 0.9, 0.97, 1.0], [0.82, 0.95, 1.0, 1.0, 0.93, 0.8]) * W / 2
        return alt, bel, tavan, gen
    halkalar = []
    for x in xs:
        alt, bel, tavan, gen = profil(x)
        ust_gen = gen * 0.74
        p = [(x, 0, alt), (x, gen * 0.8, alt), (x, gen, alt + 0.12), (x, gen, bel - 0.15), (x, gen * 0.99, bel),
             (x, ust_gen + (gen - ust_gen) * 0.25, bel + (tavan - bel) * 0.55), (x, ust_gen, tavan - 0.04), (x, ust_gen * 0.6, tavan),
             (x, 0, tavan + 0.01)]
        tam = p + [(q[0], -q[1], q[2]) for q in reversed(p[1:-1])]
        halkalar.append(tam)
    n = len(halkalar[0])
    verts = [v for h in halkalar for v in h]
    faces = []
    for i in range(len(halkalar) - 1):
        for j in range(n):
            a, b = i * n + j, i * n + (j + 1) % n
            faces.append((a, b, b + n, a + n))
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple((len(halkalar) - 1) * n + j for j in range(n)))
    boya = pbr(f'Boya{renk}', renk, 0.32, 0.4, coat=1.0)
    cam = pbr('OtoCam', '#0f1418', 0.02, coat=0.5)
    govde = kit.mesh_object(ad + 'Govde', verts, faces, boya)
    govde.data.materials.append(cam)
    # cam bölgesi: bel çizgisinin üstü, kabin aralığında (yan + ön + arka cam)
    for pf in govde.data.polygons:
        c = pf.center
        u = (c.x + L / 2) / L
        _, bel, tavan, _ = profil(c.x)
        nx, nz = pf.normal.x, pf.normal.z
        yan = c.z > bel + 0.05 and c.z < tavan - 0.03 and 0.07 < u < 0.7 and abs(nz) < 0.7
        on_cam = 0.62 < u < 0.8 and c.z > bel + 0.04 and nx > 0.25 and abs(pf.normal.y) < 0.75
        arka_cam = u < 0.14 and c.z > bel + 0.08 and nx < -0.25 and abs(pf.normal.y) < 0.75
        if yan or on_cam or arka_cam:
            pf.material_index = 1
    for pf in govde.data.polygons:
        pf.use_smooth = True
    sb = govde.modifiers.new('Ince', 'SUBSURF')
    sb.levels = 1
    sb.render_levels = 2
    # çamurluk kemerleri
    for xw in (-1.33, 1.38):
        bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.38, depth=W + 0.3, location=(xw, 0, 0.33), rotation=(math.pi / 2, 0, 0))
        k = bpy.context.active_object
        k.name = 'Kemer'
        bo = govde.modifiers.new('Kemer', 'BOOLEAN')
        bo.object = k
        bo.operation = 'DIFFERENCE'
        k.hide_render = True
        k.hide_viewport = True
    # tekerlekler
    lastik = pbr('Lastik', '#151617', 0.85)
    jant = pbr('Jant', '#b9bcc0', 0.22, 1.0)
    for xw in (-1.33, 1.38):
        for s in (-1, 1):
            y = s * (W / 2 - 0.12)
            bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=0.31, depth=0.2, location=(xw, y, 0.31), rotation=(math.pi / 2, 0, 0))
            t = bpy.context.active_object
            t.data.materials.append(lastik)
            kit.bevel(t, 0.05, 4, 30)
            bpy.ops.object.shade_smooth()
            bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.2, depth=0.02, location=(xw, y + s * 0.1, 0.31), rotation=(math.pi / 2, 0, 0))
            bpy.context.active_object.data.materials.append(jant)
            for k5 in range(5):
                a = k5 * 2 * math.pi / 5
                sp = kit.box('Kol', (0.035, 0.03, 0.17), (xw + 0.08 * math.sin(a), y + s * 0.108, 0.31 + 0.08 * math.cos(a)), jant)
                sp.rotation_euler[1] = a
    # farlar, stoplar, plaka, ayna, tampon çizgisi
    far = pbr('Far', '#f4f6f8', 0.1, 0.0, '#ffffff', 2.0)
    stop = pbr('Stop', '#7a0d0d', 0.2, 0.0, '#ff2a1a', 1.2)
    beyaz = pbr('Plaka', '#f2f2f0', 0.4)
    koyu = pbr('OtoKoyu', '#1d2024', 0.5)
    sinyal = pbr('Sinyal', '#c87a1a', 0.2, 0.0, '#ff9a2a', 0.4)
    plastik = pbr('OtoPlastik', '#232528', 0.7)
    krom = pbr('OtoKrom', '#d6d8db', 0.15, 1.0)
    for s in (-1, 1):
        # farlar: ön köşeye sarılan ince camlı gövde + gündüz ışığı şeridi
        f = kit.box('Far', (0.22, 0.38, 0.11), (L / 2 - 0.2, s * 0.6, 0.66), far)
        f.rotation_euler[2] = s * math.radians(14)
        kit.bevel(f, 0.03, 3)
        kit.box('Sinyal', (0.1, 0.12, 0.05), (L / 2 - 0.26, s * 0.8, 0.6), sinyal)
        # stoplar: arka yüze gömülü, yandan taşmaz
        st = kit.box('Stop', (0.1, 0.32, 0.12), (-L / 2 + 0.06, s * 0.5, 0.74), stop)
        kit.bevel(st, 0.02, 2)
        kit.box('Ayna', (0.14, 0.18, 0.11), (0.65, s * (W / 2 + 0.06), 1.05), boya)
        kit.box('AynaCam', (0.012, 0.15, 0.08), (0.58, s * (W / 2 + 0.07), 1.05), cam)
        kit.box('KapiKolu', (0.12, 0.02, 0.03), (-0.1, s * (W / 2 + 0.005), 0.9), krom)
        kit.box('KapiKolu', (0.12, 0.02, 0.03), (0.9, s * (W / 2 + 0.005), 0.9), krom)
        # kapı derzleri (ince koyu çizgi), marşpiyel, camı çevreleyen siyah fitil
        for xd in (-0.45, 0.62):
            kit.box('Derz', (0.012, 0.012, 0.62), (xd, s * (W / 2 + 0.001), 0.62), koyu)
        kit.box('Marspiyel', (2.0, 0.05, 0.1), (0.03, s * (W / 2 - 0.03), 0.27), plastik)
        kit.box('Fitil', (2.65, 0.02, 0.025), (0.2, s * (W / 2 * 0.98), 0.955), plastik)
        kit.box('Direk', (0.08, 0.02, 0.4), (0.2, s * (W / 2 * 0.86), 1.18), plastik)
    kit.box('Plaka', (0.02, 0.5, 0.11), (L / 2 + 0.03, 0, 0.42), beyaz)
    kit.box('Plaka', (0.02, 0.5, 0.11), (-L / 2 - 0.0, 0, 0.55), beyaz)
    kit.box('Izgara', (0.04, 0.8, 0.12), (L / 2 - 0.02, 0, 0.56), koyu)
    kit.box('IzgaraKrom', (0.045, 0.82, 0.02), (L / 2 - 0.015, 0, 0.63), krom)
    kit.box('AltIzgara', (0.06, 1.2, 0.12), (L / 2 - 0.05, 0, 0.32), plastik)
    kit.box('ArkaTampon', (0.08, 1.5, 0.1), (-L / 2 + 0.02, 0, 0.36), plastik)
    kit.box('Silecek', (0.02, 0.5, 0.02), (L * 0.2, 0.25, 1.0), plastik).rotation_euler[2] = 0.25
    kit.box('Silecek', (0.02, 0.5, 0.02), (L * 0.2, -0.3, 1.0), plastik).rotation_euler[2] = 0.25
    for s in (-1, 1):
        kit.box('TavanRayi', (1.7, 0.04, 0.04), (-0.35, s * 0.55, 1.465), plastik)
    yeni = [o for o in bpy.data.objects if o not in once]
    return _grupla(yeni, ad, konum, yon)


# ------------------------------------------------------------------ bisiklet
def bisiklet(konum=(0, 0, 0), yon=0.0, renk='#2d5f8a', ad='Bisiklet', pedal=0.0):
    once = set(bpy.data.objects)
    kadro = pbr(f'Kadro{renk}', renk, 0.3, 0.3, coat=0.6)
    siyah = pbr('BisSiyah', '#141516', 0.6)
    krom = pbr('BisKrom', '#cfd2d5', 0.18, 1.0)
    R = 0.34
    arka, on = Vector((-0.52, 0, R)), Vector((0.55, 0, R))
    gm = Vector((0.0, 0, 0.3))  # orta göbek
    sele = Vector((-0.16, 0, 0.86))
    gidon_ust, gidon_alt = Vector((0.43, 0, 0.88)), Vector((0.46, 0, 0.72))
    for c in (arka, on):
        bpy.ops.mesh.primitive_torus_add(major_radius=R - 0.015, minor_radius=0.017, major_segments=64, minor_segments=12,
                                         location=c, rotation=(math.pi / 2, 0, 0))
        bpy.context.active_object.data.materials.append(siyah)
        bpy.ops.object.shade_smooth()
        bpy.ops.mesh.primitive_torus_add(major_radius=R - 0.04, minor_radius=0.008, major_segments=64, minor_segments=8,
                                         location=c, rotation=(math.pi / 2, 0, 0))
        bpy.context.active_object.data.materials.append(krom)
        for k in range(24):  # teller
            a = k * 2 * math.pi / 24
            uc = c + Vector((math.cos(a) * (R - 0.045), 0.0, math.sin(a) * (R - 0.045)))
            boru(c + Vector((0, 0.025 if k % 2 else -0.025, 0)), uc, 0.0012, krom, 4, 'Tel')
        boru(c - Vector((0, 0.05, 0)), c + Vector((0, 0.05, 0)), 0.018, krom, 12, 'Gobek')
    for (a, b) in ((gm, sele), (sele, gidon_ust), (gm, gidon_alt), (gidon_alt, gidon_ust)):
        boru(a, b, 0.018, kadro)
    for s in (-0.055, 0.055):
        boru(gm + Vector((0, s * 0.6, 0)), arka + Vector((0, s, 0)), 0.011, kadro)
        boru(sele + Vector((0, s * 0.4, -0.06)), arka + Vector((0, s, 0)), 0.01, kadro)
        boru(gidon_alt + Vector((0, s * 0.5, 0)), on + Vector((0, s, 0)), 0.012, kadro)
    boru(sele, sele + Vector((-0.03, 0, 0.1)), 0.013, krom)  # sele borusu
    s = kit.box('Sele', (0.26, 0.13, 0.05), sele + Vector((-0.04, 0, 0.12)), siyah)
    kit.bevel(s, 0.02, 3)
    st = gidon_ust + Vector((0.08, 0, 0.05))
    boru(gidon_ust, st, 0.014, krom)
    boru(st + Vector((0, -0.28, 0)), st + Vector((0, 0.28, 0)), 0.012, krom, 12, 'Gidon')
    for yy in (-0.27, 0.27):
        boru(st + Vector((0, yy - 0.05, 0)), st + Vector((0, yy + 0.05, 0)), 0.016, siyah, 12, 'Elcik')
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.095, depth=0.008, location=gm + Vector((0, -0.07, 0)), rotation=(math.pi / 2, 0, 0))
    bpy.context.active_object.data.materials.append(krom)
    for k, s_ in ((0, -1), (math.pi, 1)):
        a = pedal + k
        uc = gm + Vector((math.cos(a) * 0.17, s_ * 0.09, math.sin(a) * 0.17))
        boru(gm + Vector((0, s_ * 0.08, 0)), uc, 0.01, krom, 8, 'Kol')
        kit.box('Pedal', (0.1, 0.08, 0.02), uc + Vector((0, s_ * 0.04, 0)), siyah)
    boru(gm + Vector((0, -0.07, 0.095)), arka + Vector((0, -0.07, 0.04)), 0.003, siyah, 6, 'Zincir')
    boru(gm + Vector((0, -0.07, -0.095)), arka + Vector((0, -0.07, -0.04)), 0.003, siyah, 6, 'Zincir')
    yeni = [o for o in bpy.data.objects if o not in once]
    return _grupla(yeni, ad, konum, yon)


# ------------------------------------------------------------------ ağaç, lamba
def agac(konum, boy=7.0, seed=0, renk=('#5d6a3e', '#6f7b48', '#7c8550')):
    """Gövde + dallar + yaprak kümeleri (binlerce küçük yaprak kartı)."""
    rnd = random.Random(seed)
    x, y, z = konum
    govde_m = pbr('AgacGovde', '#4e3d2e', 0.85)
    yaprak_m = [pbr(f'Yaprak{i}', c, 0.6) for i, c in enumerate(renk)]
    boru((x, y, z), (x + rnd.uniform(-0.2, 0.2), y + rnd.uniform(-0.2, 0.2), z + boy * 0.5), 0.12 * boy / 7, govde_m, 10, 'Govde')
    tepe = Vector((x, y, z + boy * 0.5))
    kumeler = []
    for i in range(7):
        a = rnd.uniform(0, 2 * math.pi)
        r = rnd.uniform(0.5, 1.6) * boy / 7
        uc = tepe + Vector((math.cos(a) * r, math.sin(a) * r, rnd.uniform(0.6, 2.2) * boy / 7))
        boru(tepe, uc, 0.05 * boy / 7, govde_m, 8, 'Dal')
        kumeler.append((uc, rnd.uniform(0.9, 1.4) * boy / 7))
    kumeler.append((tepe + Vector((0, 0, 2.0 * boy / 7)), 1.5 * boy / 7))
    for k in range(3):
        mer, b, d = [], [], []
        for (c, r) in kumeler:
            for _ in range(700):
                v = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 0.8))).normalized() * r * rnd.random() ** 0.35
                mer.append(tuple(c + v))
                s = rnd.uniform(0.06, 0.11)
                b.append((s, s * 0.6, 0.004))
                d.append((rnd.uniform(0, 6.3), rnd.uniform(0, 6.3), rnd.uniform(0, 6.3)))
        kit.toplu_mesh(f'Yaprak{k}', kit.sablon('kup'), mer[k::3], b[k::3], d[k::3], yaprak_m[k])


def lamba(konum, yon=0.0, yanik=False):
    x, y, z = konum
    m = pbr('Direk', '#3a3e42', 0.45, 0.7)
    boru((x, y, z), (x, y, z + 5.5), 0.07, m, 12, 'Direk')
    kol_uc = (x + 0.9 * math.cos(yon), y + 0.9 * math.sin(yon), z + 5.6)
    boru((x, y, z + 5.4), kol_uc, 0.04, m, 8, 'Kol')
    c = kit.box('LambaBas', (0.5, 0.22, 0.1), kol_uc, m)
    c.rotation_euler[2] = yon
    g = kit.box('LambaCam', (0.42, 0.16, 0.02), (kol_uc[0], kol_uc[1], kol_uc[2] - 0.06),
                pbr('LambaCam' + str(yanik), '#fff4dc', 0.2, 0.0, '#ffd59a', 8.0 if yanik else 0.0))
    g.rotation_euler[2] = yon


def yol(y_bina, uzun=80):
    """Bina önünde: kaldırım (taş), bordür, asfalt (şerit çizgili), karşı kaldırım."""
    tas = bpy.data.materials.get('KaldirimTas') or bpy.data.materials.new('KaldirimTas')
    tas.use_nodes = True
    nt = tas.node_tree
    b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    br = nt.nodes.new('ShaderNodeTexBrick')
    br.inputs['Color1'].default_value = kit.srgb('#c4bcb0')
    br.inputs['Color2'].default_value = kit.srgb('#b3aa9c')
    br.inputs['Mortar'].default_value = kit.srgb('#8f877b')
    br.inputs['Scale'].default_value = 2.5
    br.inputs['Mortar Size'].default_value = 0.01
    nt.links.new(tc.outputs['Object'], br.inputs['Vector'])
    nt.links.new(br.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.85
    asfalt = bpy.data.materials.new('Asfalt')
    asfalt.use_nodes = True
    nt = asfalt.node_tree
    b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 40.0
    nz.inputs['Detail'].default_value = 10.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    mx = nt.nodes.new('ShaderNodeMix')
    mx.data_type = 'RGBA'
    mx.blend_type = 'MULTIPLY'
    mx.inputs['Factor'].default_value = 0.35
    mx.inputs['A'].default_value = kit.srgb('#4a4b4d')
    nt.links.new(nz.outputs['Color'], mx.inputs['B'])
    nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.88
    bp = nt.nodes.new('ShaderNodeBump')
    bp.inputs['Strength'].default_value = 0.2
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    bordur = pbr('Bordur', '#b1ada6', 0.8)
    cizgi = pbr('YolCizgi', '#ecebe6', 0.6)
    y0 = y_bina
    kit.box('Kaldirim', (uzun, 3.4, 0.15), (0, y0 - 1.7, 0.075), tas)
    kit.box('Bordur', (uzun, 0.18, 0.18), (0, y0 - 3.45, 0.09), bordur)
    kit.box('Asfalt', (uzun, 7.4, 0.05), (0, y0 - 7.2, 0.025), asfalt)
    for i in range(-int(uzun / 6), int(uzun / 6)):
        kit.box('Serit', (2.8, 0.14, 0.01), (i * 6.0, y0 - 7.2, 0.055), cizgi)
    kit.box('Bordur', (uzun, 0.18, 0.18), (0, y0 - 10.95, 0.09), bordur)
    kit.box('Kaldirim', (uzun, 3.4, 0.15), (0, y0 - 12.7, 0.075), tas)


# ------------------------------------------------------------------ pencere arkası odalar
ODA_TIPLERI = ['salon', 'mutfak', 'yatak', 'calisma', 'cocuk', 'perde', 'jaluzi', 'salon2']
DUVAR = ['#efe6d8', '#e6ece8', '#f1e3d3', '#e3e7ee', '#f2ece1', '#e9dfe6', '#ebe6dc']
KUMAS = ['#b9583f', '#4f6a85', '#c9a46a', '#7b5a73', '#5f6f5a', '#d9cbb4', '#2f3c4c']


def oda(cam_c, n, gen, yuk, tip, rnd, isik=True):
    """Pencerenin arkasında 'gen' genişliğinde, 1.7 m derin bir oda: duvar, döşeme, mobilya, perde, ışık."""
    nn = Vector(n)
    ic = -nn  # içeri
    c = Vector(cam_c)
    yan = Vector((-nn.y, nn.x, 0))
    D = 1.7
    taban_z = c.z - 1.0 - 0.625  # pencere alt kotunun ~1 m altı
    merkez = c + ic * (D / 2 + 0.12)
    duvar = pbr('Duvar' + DUVAR[rnd.randrange(len(DUVAR))], DUVAR[rnd.randrange(len(DUVAR))], 0.9)
    zemin = pbr('Parke' if rnd.random() < 0.7 else 'Fayans', '#9c7752' if rnd.random() < 0.7 else '#d8d3cb', 0.55)

    def kutu_(ad, boyut_y, boyut_ic, h, ofs_yan, ofs_ic, z, m):
        s = (abs(yan.x) * boyut_y + abs(ic.x) * boyut_ic, abs(yan.y) * boyut_y + abs(ic.y) * boyut_ic, h)
        p = c + ic * (0.12 + ofs_ic) + yan * ofs_yan
        return kit.box(ad, s, (p.x, p.y, z + h / 2), m)
    kutu_('OdaArka', gen, 0.05, yuk, 0, D, taban_z, duvar)
    kutu_('OdaZemin', gen, D, 0.03, 0, D / 2, taban_z, zemin)
    kutu_('OdaTavan', gen, D, 0.03, 0, D / 2, taban_z + yuk, pbr('Tavan', '#f3f1ed', 0.9))
    for s in (-1, 1):
        kutu_('OdaYan', 0.05, D, yuk, s * gen / 2, D / 2, taban_z, duvar)
    k1 = pbr('Kumas' + str(rnd.randrange(7)), KUMAS[rnd.randrange(len(KUMAS))], 0.85)
    ah = pbr('Ahsap2', '#8a6646', 0.5)
    ak = pbr('Beyaz2', '#f0eee9', 0.4)
    if tip in ('salon', 'salon2'):
        kutu_('Kanepe', 1.9, 0.8, 0.42, 0.2, D - 0.5, taban_z, k1)
        kutu_('KanepeSirt', 1.9, 0.2, 0.85, 0.2, D - 0.15, taban_z, k1)
        kutu_('Sehpa', 0.9, 0.5, 0.4, 0.2, D - 1.2, taban_z, ah)
        kutu_('Tablo', 0.9, 0.03, 0.6, 0.2, D - 0.03, taban_z + 1.4, pbr('Tablo' + str(rnd.randrange(5)), KUMAS[rnd.randrange(7)], 0.6))
        kutu_('Abajur', 0.3, 0.3, 0.3, -gen / 2 + 0.4, D - 0.4, taban_z + 1.3, pbr('AbajurIsik', '#fff1d6', 0.5, 0.0, '#ffd59a', 6.0 if isik else 0.0))
        kutu_('AbajurAyak', 0.04, 0.04, 1.3, -gen / 2 + 0.4, D - 0.4, taban_z, ah)
        if tip == 'salon2':
            kutu_('TV', 1.1, 0.05, 0.62, -0.5, 0.35, taban_z + 0.9, pbr('TVIsik', '#1a2230', 0.2, 0.0, '#6f9fd8', 2.5))
    elif tip == 'mutfak':
        kutu_('Tezgah', gen - 0.2, 0.6, 0.9, 0, D - 0.3, taban_z, ak)
        kutu_('UstDolap', gen - 0.2, 0.35, 0.7, 0, D - 0.18, taban_z + 1.5, ak)
        kutu_('Tezgahust', gen - 0.2, 0.62, 0.04, 0, D - 0.31, taban_z + 0.9, pbr('Tezgahust', '#4a4642', 0.3))
        kutu_('Sarkit', 0.35, 0.35, 0.2, 0, D - 0.9, taban_z + 2.0, pbr('SarkitIsik', '#fff1d6', 0.4, 0.0, '#ffe2b0', 7.0 if isik else 0.0))
    elif tip == 'yatak':
        kutu_('Yatak', 1.6, 1.4, 0.5, 0.0, D - 0.75, taban_z, ak)
        kutu_('Yorgan', 1.62, 1.0, 0.08, 0.0, D - 0.9, taban_z + 0.5, k1)
        kutu_('Basucu', 1.7, 0.1, 1.0, 0.0, D - 0.05, taban_z, ah)
        kutu_('Lamba', 0.25, 0.25, 0.25, 1.1, D - 0.3, taban_z + 0.65, pbr('LambaIsik', '#fff1d6', 0.5, 0.0, '#ffc77a', 5.0 if isik else 0.0))
    elif tip == 'calisma':
        kutu_('Masa', 1.4, 0.7, 0.75, 0.3, D - 0.4, taban_z, ah)
        kutu_('Ekran', 0.6, 0.04, 0.38, 0.3, D - 0.55, taban_z + 0.95, pbr('EkranIsik', '#101820', 0.2, 0.0, '#9cc4f0', 3.0))
        mer, b = [], []
        for r_ in range(4):
            for k in range(14):
                p = c + ic * (0.12 + D - 0.2) + yan * (-gen / 2 + 0.25 + k * 0.05)
                mer.append((p.x, p.y, taban_z + 0.4 + r_ * 0.42 + 0.14))
                b.append((abs(yan.x) * 0.04 + abs(ic.x) * 0.22, abs(yan.y) * 0.04 + abs(ic.y) * 0.22, rnd.uniform(0.2, 0.3)))
        kit.toplu_mesh('Kitaplar', kit.sablon('kup'), mer, b, None, pbr('Kitap' + str(rnd.randrange(4)), KUMAS[rnd.randrange(7)], 0.6))
    elif tip == 'cocuk':
        kutu_('Ranza', 1.0, 1.9, 0.4, 0.4, D - 0.5, taban_z, pbr('Ranza', '#e9c46a', 0.5))
        for k in range(6):
            kutu_('Oyuncak', 0.18, 0.18, 0.18, -0.6 + k * 0.15, D - 1.2, taban_z, pbr('Oyuncak' + str(k % 4), ['#e76f51', '#2a9d8f', '#e9c46a', '#457b9d'][k % 4], 0.4))
        kutu_('Yildiz', 0.3, 0.3, 0.3, -0.3, D - 0.8, taban_z + 2.1, pbr('YildizIsik', '#fff1d6', 0.5, 0.0, '#ffd59a', 5.0 if isik else 0.0))
    # perdeler (çoğu odada iki yanda; 'perde' tipinde kapalı; 'jaluzi' yatay lameller)
    if tip == 'perde':
        kutu_('Perde', gen - 0.2, 0.04, yuk - 0.2, 0, 0.1, taban_z + 0.1, pbr('PerdeIsik' + str(rnd.randrange(3)), KUMAS[rnd.randrange(7)], 0.8, 0.0, '#ffb878', 0.6 if isik else 0.0))
    elif tip == 'jaluzi':
        for k in range(16):
            kutu_('Lamel', gen - 0.3, 0.06, 0.012, 0, 0.12, taban_z + 1.0 + k * 0.08, pbr('Jaluzi', '#ece8e0', 0.5))
    else:
        for s in (-1, 1):
            kutu_('Perde', 0.45, 0.06, yuk - 0.25, s * (gen / 2 - 0.4), 0.12, taban_z + 0.15, k1)
    if isik and tip not in ('perde',):
        ld = bpy.data.lights.new('Oda', 'POINT')
        ld.energy = 170 if tip != 'calisma' else 110
        ld.color = (1.0, 0.76, 0.5)
        ld.shadow_soft_size = 0.3
        lo = bpy.data.objects.new('Oda', ld)
        lo.location = merkez + Vector((0, 0, 0)) + Vector((0, 0, taban_z + yuk - 0.4 - merkez.z))
        kit.link(lo)
