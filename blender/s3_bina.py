"""
Sahne 3 — "Bina": betonarme apartman doğru sırayla kurulur.

Sıra (Kutay: "doğru sıra ile evi yapınca ev olsun, önce çatı yapılmaz"):
  temel → kat kat karkas (kolon, kiriş, döşeme) → gazbeton duvarlar
  (kat kat, sıra sıra örülür) → lentolar → çatı panelleri → doğramalar.
Yeşil yalnız bizim ürüne: sahadaki paletlerin streç örtüsü.

Duvarlar tek parça nesnedir; örülme, gölgelendiricide dünya yüksekliğine
göre "sıra sıra" açılan bir maskeyle yapılır (60 × 25 cm derz düzeni).

Kullanım: python s3_bina.py --variant d|m --frames all|0,40 --out DIR
"""
import argparse
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

FRAMES = 120
# Tek akış: giriş (palet bloğu yakın planı → şantiye) + yapım + çıkış (alacakaranlık, tepeden).
U_GIRIS, U_CIKIS = 0.12, 0.80  # u (sahne zamanı) → t (yapım zamanı) eşlemesi
LOOSE = (-10.8, -13.8, 0.0)  # sahne 2'deki numune küpüyle eşleşen gevşek blok (zeminde)


def yapim_t(u):
    return min(1.0, max(0.0, (u - U_GIRIS) / (U_CIKIS - U_GIRIS)))
XS = [-6.0, -2.0, 2.0, 6.0]  # kolon aksları (m)
YS = [-4.5, 0.0, 4.5]
FLOORS = 4
FH = 3.0  # kat yüksekliği
SLAB = 0.15
BEAM_D = 0.45
COL = 0.35
WT = 0.25  # duvar kalınlığı
COURSE = 0.25
CLEAR = FH - SLAB - BEAM_D  # duvar net yüksekliği (döşeme üstü → kiriş altı)

# zaman çizelgesi (t: 0..1)
T_FOUND = (0.02, 0.08)
T_FRAME0, T_FRAME_STEP = 0.08, 0.07
T_WALL0, T_WALL_STAGGER, T_WALL_DUR = 0.37, 0.055, 0.15
T_LINTEL = (0.60, 0.72)
T_ROOF = (0.70, 0.82)
T_WIN = (0.80, 0.90)

VARIANTS = {
    'd': dict(res=(1600, 900), lens=32.0, dist=31.0),
    'm': dict(res=(768, 1366), lens=40.0, dist=27.0),
}


def concrete_material(name='Beton', base='#8d8f8c'):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = kit.NT(mat.node_tree)
    bsdf = nt.n.get('Principled BSDF')
    tc = nt.node('ShaderNodeTexCoord', (-900, 0))
    nz = nt.node('ShaderNodeTexNoise', (-700, 0))
    nz.inputs['Scale'].default_value = 1.8
    nz.inputs['Detail'].default_value = 7.0
    nz.inputs['Roughness'].default_value = 0.62
    nt.link(tc.outputs['Object'], nz.inputs['Vector'])
    mr = nt.node('ShaderNodeMapRange', (-450, 0))
    nt.link(nz.outputs['Fac'], mr.inputs['Value'])
    mr.inputs['To Min'].default_value = 0.86
    mr.inputs['To Max'].default_value = 1.08
    mix = nt.node('ShaderNodeMix', (-200, 100), data_type='RGBA', blend_type='MULTIPLY')
    mix.inputs['Factor'].default_value = 1.0
    mix.inputs['A'].default_value = kit.srgb(base)
    cc = nt.node('ShaderNodeCombineColor', (-350, -100))
    for i in range(3):
        nt.link(mr.outputs['Result'], cc.inputs[i])
    nt.link(cc.outputs[0], mix.inputs['B'])
    nt.link(mix.outputs['Result'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.82
    bmp = nt.node('ShaderNodeBump', (-200, -300))
    bmp.inputs['Strength'].default_value = 0.15
    nt.link(nz.outputs['Fac'], bmp.inputs['Height'])
    nt.link(bmp.outputs['Normal'], bsdf.inputs['Normal'])
    return mat


def wall_material(axis, zaman):
    """Gazbeton duvar: blok derzi (60×25) + 'sıra sıra örülme' maskesi (zaman değerine bağlı)."""
    mat = kit.aac_material(f'Duvar{axis}', bump=0.5, tex_size=0.24)
    nt = kit.NT(mat.node_tree)
    out = [n for n in nt.n if n.type == 'OUTPUT_MATERIAL'][0]
    bsdf = [n for n in nt.n if n.type == 'BSDF_PRINCIPLED'][0]
    geo = nt.node('ShaderNodeNewGeometry', (-1600, -900))
    sep = nt.node('ShaderNodeSeparateXYZ', (-1400, -900))
    nt.link(geo.outputs['Position'], sep.inputs[0])
    along = sep.outputs['X'] if axis == 'X' else sep.outputs['Y']
    z = sep.outputs['Z']
    # derz düzeni
    v2 = nt.node('ShaderNodeCombineXYZ', (-1200, -700))
    nt.link(along, v2.inputs['X'])
    nt.link(z, v2.inputs['Y'])
    br = nt.node('ShaderNodeTexBrick', (-1000, -700))
    br.offset = 0.5
    br.offset_frequency = 2
    br.inputs['Scale'].default_value = 1.0
    br.inputs['Mortar Size'].default_value = 0.0045
    br.inputs['Mortar Smooth'].default_value = 0.3
    br.inputs['Brick Width'].default_value = 0.60
    br.inputs['Row Height'].default_value = COURSE
    br.inputs['Color1'].default_value = (1, 1, 1, 1)
    br.inputs['Color2'].default_value = (0.94, 0.94, 0.94, 1)
    br.inputs['Mortar'].default_value = (0.62, 0.62, 0.61, 1)
    nt.link(v2.outputs['Vector'], br.inputs['Vector'])
    base_col = bsdf.inputs['Base Color'].links[0].from_socket
    mul = nt.node('ShaderNodeMix', (-600, -500), data_type='RGBA', blend_type='MULTIPLY')
    mul.inputs['Factor'].default_value = 1.0
    nt.link(base_col, mul.inputs['A'])
    nt.link(br.outputs['Color'], mul.inputs['B'])
    nt.link(mul.outputs['Result'], bsdf.inputs['Base Color'])

    # örülme maskesi
    m = nt.math
    fl = m('FLOOR', m('DIVIDE', z, FH, loc=(-1200, -1100)), loc=(-1050, -1100))  # kat no
    local = m('SUBTRACT', z, m('MULTIPLY', fl, FH, loc=(-900, -1250)), loc=(-600, -1150))  # duvar tabanı = döşeme üstü
    course = m('MAXIMUM', m('FLOOR', m('DIVIDE', local, COURSE, loc=(-450, -1150)), loc=(-300, -1150)), 0.0, loc=(-150, -1150))
    # ilerleme (sıra cinsinden): kat başına gecikmeli
    tt = m('SUBTRACT', m('SUBTRACT', zaman, T_WALL0, loc=(-900, -1450)), m('MULTIPLY', fl, T_WALL_STAGGER, loc=(-900, -1600)), loc=(-700, -1500))
    prog = m('MULTIPLY', m('DIVIDE', tt, T_WALL_DUR, loc=(-550, -1500)), CLEAR / COURSE + 0.999, loc=(-400, -1500))
    prog = m('MAXIMUM', prog, 0.0, loc=(-250, -1500))
    full = m('LESS_THAN', course, m('FLOOR', prog, loc=(-100, -1450)), loc=(50, -1300))
    same = m('COMPARE', course, m('FLOOR', prog, loc=(-100, -1600)), loc=(50, -1500))
    same.node.inputs[2].default_value = 0.5
    seg_ = m('FRACT', m('DIVIDE', along, 1.2, loc=(-100, -1750)), loc=(50, -1750))
    part = m('MULTIPLY', same, m('LESS_THAN', seg_, m('FRACT', prog, loc=(50, -1900)), loc=(200, -1750)), loc=(350, -1550))
    vis = m('MAXIMUM', full, part, loc=(500, -1400))
    tr = nt.node('ShaderNodeBsdfTransparent', (600, -200))
    mx = nt.node('ShaderNodeMixShader', (800, 0))
    nt.link(vis, mx.inputs[0])
    nt.link(tr.outputs[0], mx.inputs[1])
    nt.link(bsdf.outputs[0], mx.inputs[2])
    nt.link(mx.outputs[0], out.inputs['Surface'])
    return mat


def stretch_material():
    """Paletlerin yeşil streç örtüsü (YEŞİL = BİZİM). 3B'de yazı yok."""
    mat = bpy.data.materials.new('Strec')
    mat.use_nodes = True
    nt = kit.NT(mat.node_tree)
    bsdf = nt.n.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = kit.srgb('#8fae2a')
    bsdf.inputs['Roughness'].default_value = 0.22
    bsdf.inputs['Transmission Weight'].default_value = 0.72
    bsdf.inputs['IOR'].default_value = 1.35
    bsdf.inputs['Alpha'].default_value = 0.9
    nz = nt.node('ShaderNodeTexNoise', (-500, -200))
    nz.inputs['Scale'].default_value = 14.0
    bmp = nt.node('ShaderNodeBump', (-250, -200))
    bmp.inputs['Strength'].default_value = 0.08
    nt.link(nz.outputs['Fac'], bmp.inputs['Height'])
    nt.link(bmp.outputs['Normal'], bsdf.inputs['Normal'])
    return mat


def simple_material(name, hexcol, rough=0.5, metal=0.0, transmission=0.0, ior=1.45):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    b = mat.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = kit.srgb(hexcol)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    b.inputs['Transmission Weight'].default_value = transmission
    b.inputs['IOR'].default_value = ior
    return mat


def bays():
    """(eksen, sabit koordinat, başlangıç, bitiş) — dış cephe bölmeleri."""
    out = []
    for y in (YS[0], YS[-1]):
        for a, b in zip(XS, XS[1:]):
            out.append(('X', y, a + COL / 2, b - COL / 2))
    for x in (XS[0], XS[-1]):
        for a, b in zip(YS, YS[1:]):
            out.append(('Y', x, a + COL / 2, b - COL / 2))
    return out


def sky_world(strength=0.34, sun_elev=28.0, sun_rot=215.0):
    """Gerçek gökyüzü (çoklu saçılım). Güneş diski kapalı: gölgeyi güneş lambası verir."""
    world = bpy.data.worlds.new('Gok')
    bpy.context.scene.world = world
    world.use_nodes = True
    nt = kit.NT(world.node_tree)
    nt.n.clear()
    out = nt.node('ShaderNodeOutputWorld', (600, 0))
    sky = nt.node('ShaderNodeTexSky', (0, 0))
    sky.sky_type = 'MULTIPLE_SCATTERING'
    sky.sun_disc = False
    sky.sun_elevation = math.radians(sun_elev)
    sky.sun_rotation = math.radians(sun_rot)
    sky.altitude = 120.0
    sky.air_density = 1.0
    sky.aerosol_density = 1.8
    sky.ozone_density = 1.0
    bg = nt.node('ShaderNodeBackground', (300, 0))
    bg.inputs['Strength'].default_value = strength
    nt.link(sky.outputs[0], bg.inputs['Color'])
    nt.link(bg.outputs[0], out.inputs['Surface'])
    return world


def site_ground_material():
    """Şantiye zemini: sıkıştırılmış toprak + ince çakıl; bina çevresinde beton tabla ayrı."""
    mat = bpy.data.materials.new('SahaZemin')
    mat.use_nodes = True
    nt = kit.NT(mat.node_tree)
    bsdf = nt.n.get('Principled BSDF')
    tc = nt.node('ShaderNodeTexCoord', (-1100, 0))
    n1 = nt.node('ShaderNodeTexNoise', (-850, 150))
    n1.inputs['Scale'].default_value = 0.35
    n1.inputs['Detail'].default_value = 6.0
    nt.link(tc.outputs['Object'], n1.inputs['Vector'])
    vor = nt.node('ShaderNodeTexVoronoi', (-850, -150))
    vor.inputs['Scale'].default_value = 28.0
    nt.link(tc.outputs['Object'], vor.inputs['Vector'])
    ramp = nt.node('ShaderNodeValToRGB', (-600, 150))
    ramp.color_ramp.elements[0].color = kit.srgb('#6e6152')
    ramp.color_ramp.elements[1].color = kit.srgb('#8c7e6a')
    nt.link(n1.outputs['Fac'], ramp.inputs['Fac'])
    gr = nt.node('ShaderNodeMix', (-350, 100), data_type='RGBA', blend_type='MULTIPLY')
    gr.inputs['Factor'].default_value = 0.22
    nt.link(ramp.outputs['Color'], gr.inputs['A'])
    nt.link(vor.outputs['Color'], gr.inputs['B'])
    nt.link(gr.outputs['Result'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.95
    bmp = nt.node('ShaderNodeBump', (-300, -250))
    bmp.inputs['Strength'].default_value = 0.35
    nt.link(vor.outputs['Distance'], bmp.inputs['Height'])
    nt.link(bmp.outputs['Normal'], bsdf.inputs['Normal'])
    return mat


def window_unit(axis, c, mid, fz, ow, oh, frame_mat, glass_mat):
    """Gerçekçi doğrama: kasa (4 çubuk) + orta kayıt + cam; duvar dış yüzünden 6 cm içeride."""
    parts = []
    t = 0.065  # kasa kesiti
    d = 0.07  # kasa derinliği
    inset = -0.06 if c < 0 else 0.06  # dış yüzden içeri
    face = c + (-WT / 2 if c < 0 else WT / 2) - (-1 if c < 0 else 1) * 0.0
    pos = face - inset + (d / 2 if c < 0 else -d / 2)
    bars = [
        (0, oh / 2 - t / 2, ow, t), (0, -oh / 2 + t / 2, ow, t),
        (-ow / 2 + t / 2, 0, t, oh), (ow / 2 - t / 2, 0, t, oh),
        (0, 0, t * 0.8, oh - 2 * t),
    ]
    for (u, v, bw, bh) in bars:
        if axis == 'X':
            parts.append(kit.box('Kasa', (bw, d, bh), (mid + u, pos, fz + v), frame_mat))
        else:
            parts.append(kit.box('Kasa', (d, bw, bh), (pos, mid + u, fz + v), frame_mat))
    gpos = pos + (0.01 if c < 0 else -0.01)
    if axis == 'X':
        parts.append(kit.box('Cam', (ow - 2 * t + 0.01, 0.008, oh - 2 * t + 0.01), (mid, gpos, fz), glass_mat))
    else:
        parts.append(kit.box('Cam', (0.008, ow - 2 * t + 0.01, oh - 2 * t + 0.01), (gpos, mid, fz), glass_mat))
    return parts


def build(variant):
    kit.reset()
    v = VARIANTS[variant]
    sc = kit.setup_render(*v['res'], samples=ARGS.samples, threshold=0.02, bounces=(5, 3, 3, 4))
    sc.cycles.transparent_max_bounces = 32
    sc.view_settings.exposure = -0.55
    world = sky_world(strength=0.26)

    # güneş: ön-soldan, alçak öğleden sonra ışığı (yumuşak ama belirgin gölge)
    sun_d = bpy.data.lights.new('Gunes', 'SUN')
    sun_d.energy = 3.6
    sun_d.angle = math.radians(1.2)
    sun_d.color = (1.0, 0.88, 0.74)
    sun = bpy.data.objects.new('Gunes', sun_d)
    sun.rotation_euler = (math.radians(66), 0, math.radians(-42))
    kit.link(sun)

    ground = kit.box('Zemin', (600, 600, 0.2), (0, 0, -0.1), site_ground_material())
    conc = concrete_material()
    apron = kit.box('BetonTabla', (16.5, 13.5, 0.06), (0, 0, 0.03), concrete_material('Tabla', base='#9a9890'))

    wall_mats = {}  # duvar malzemeleri; 'zaman' girişi main() içinde her karede güncellenir
    objs = {'found': None, 'cols': [], 'slabs': [], 'beams': [], 'walls': [], 'lintels': [], 'roof': [], 'wins': [], 'ic': []}
    objs['found'] = kit.box('Temel', (13.0, 10.0, 0.5), (0, 0, -0.13), conc)

    # iç hacim: gündüz koyu, alacakaranlıkta sıcak ışık (pencerelerden yanan iç mekân)
    ic_mat = simple_material('IcM', '#2a2b2a', rough=0.95)
    icb = ic_mat.node_tree.nodes.get('Principled BSDF')
    icb.inputs['Emission Color'].default_value = (1.0, 0.72, 0.42, 1.0)
    icb.inputs['Emission Strength'].default_value = 0.0
    ex, ey = XS[-1] + WT / 2, YS[-1] + WT / 2  # dış yüz (duvar dış yüzü ile kiriş/döşeme aynı hizada)
    for k in range(FLOORS):
        z0 = k * FH
        for x in XS:
            for y in YS:
                c = kit.box(f'Kolon{k}_{x}_{y}', (COL, COL, FH), (x, y, z0 + FH / 2), conc)
                c['k'] = k
                objs['cols'].append(c)
        zt = z0 + FH
        s_ = kit.box(f'Doseme{k + 1}', (2 * ex, 2 * ey, SLAB), (0, 0, zt - SLAB / 2), conc)
        s_['k'] = k
        objs['slabs'].append(s_)
        for y in YS:
            b = kit.box(f'KirisX{k}_{y}', (2 * ex, WT, BEAM_D), (0, y, zt - SLAB - BEAM_D / 2), conc)
            b['k'] = k
            objs['beams'].append(b)
        for x in XS:
            b = kit.box(f'KirisY{k}_{x}', (WT, 2 * ey, BEAM_D), (x, 0, zt - SLAB - BEAM_D / 2), conc)
            b['k'] = k
            objs['beams'].append(b)
        # iç karanlık hacim: camdan bakınca boş karkas değil, gölgeli iç mekân görünsün
        ic = kit.box(f'Ic{k}', (2 * ex - 3.0, 2 * ey - 3.0, FH - SLAB - 0.05), (0, 0, z0 + SLAB + (FH - SLAB) / 2), ic_mat)
        ic['k'] = k
        objs['ic'].append(ic)

    lintel_mat = kit.aac_material('Lento', bump=0.5)
    frame_mat = simple_material('Dograma', '#3a3f43', rough=0.32)
    glass_mat = simple_material('Cam', '#dde6ea', rough=0.015, transmission=1.0, ior=1.52)
    for axis in ('X', 'Y'):
        wall_mats[axis] = wall_material(axis, None)
    win_w, win_h, sill = 1.5, 1.4, 0.9
    for k in range(FLOORS):
        zb = k * FH + (0.12 if k == 0 else 0.0)  # duvar tabanı = döşeme (zeminde temel) üstü
        top = (k + 1) * FH - SLAB - BEAM_D - zb  # kiriş altına kadar: boşluk da çakışma da yok
        for (axis, c, a, b) in bays():
            mid = (a + b) / 2
            is_door = (k == 0 and axis == 'X' and c == YS[0] and abs(mid) < 0.1)
            ow, oh, os_ = (1.3, 2.1, 0.0) if is_door else (win_w, win_h, sill)
            o0, o1 = mid - ow / 2, mid + ow / 2
            pieces = [(a, o0, 0.0, top), (o1, b, 0.0, top)]
            if os_ > 0:
                pieces.append((o0, o1, 0.0, os_))
            top0 = os_ + oh
            pieces.append((o0, o1, top0, top))
            for (p0, p1, h0, h1) in pieces:
                L = p1 - p0
                cx = (p0 + p1) / 2
                if axis == 'X':
                    w = kit.box('Duvar', (L, WT, h1 - h0), (cx, c, zb + (h0 + h1) / 2), wall_mats['X'])
                else:
                    w = kit.box('Duvar', (WT, L, h1 - h0), (c, cx, zb + (h0 + h1) / 2), wall_mats['Y'])
                w['k'] = k
                objs['walls'].append(w)
            # lento: açıklığın üstünde, iki yana 20 cm oturur (duvar yüzünden 5 mm taşar)
            lz = zb + top0 + 0.1
            if axis == 'X':
                lt = kit.box('Lento', (ow + 0.4, WT + 0.01, 0.2), (mid, c, lz), lintel_mat)
            else:
                lt = kit.box('Lento', (WT + 0.01, ow + 0.4, 0.2), (c, mid, lz), lintel_mat)
            lt['k'] = k
            lt['z'] = lz
            objs['lintels'].append(lt)
            if not is_door:
                fz = zb + os_ + oh / 2
                parts = window_unit(axis, c, mid, fz, ow, oh, frame_mat, glass_mat)
                for p_ in parts:
                    p_['k'] = k
                objs['wins'].append(parts)

    # çatı panelleri (gazbeton çatı paneli, 60 cm genişlik)
    roof_mat = kit.aac_material('CatiPaneli', bump=0.5)
    zr = FLOORS * FH + 0.1
    for row, y0 in enumerate((-ey / 2, ey / 2)):
        for i in range(20):
            x = -ex + 0.3 + i * (2 * ex - 0.6) / 19
            p = kit.box('Panel', (0.595, ey - 0.02, 0.2), (x, y0, zr), roof_mat)
            p['z'] = zr
            p['i'] = row * 20 + i
            objs['roof'].append(p)

    # sahadaki paletler: ahşap palet + blok istifi + yarı saydam yeşil streç (YEŞİL = BİZİM)
    pal_mat = simple_material('Ahsap', '#8a6a46', rough=0.85)
    stack = kit.aac_material('Istif', bump=0.4)
    strec = stretch_material()
    for (px, py, rz) in [(-10.4, -2.6, 0.08), (-10.2, -4.3, -0.05), (-11.8, -3.4, 0.15)]:  # giriş yolunun dışında
        grp = []
        for sx in (-0.5, 0.0, 0.5):
            grp.append(kit.box('PaletKiris', (0.1, 1.0, 0.1), (px + sx, py, 0.05), pal_mat))
        for sy in (-0.45, -0.22, 0.0, 0.22, 0.45):
            grp.append(kit.box('PaletTahta', (1.2, 0.09, 0.025), (px, py + sy, 0.1125), pal_mat))
        for r in range(5):
            for j in range(2):
                grp.append(kit.box('IstifBlok', (0.596, 0.996, 0.246), (px - 0.3 + j * 0.6, py, 0.125 + 0.125 + r * 0.25), stack))
        film = kit.box('PaletStrec', (1.212, 1.012, 1.24), (px, py, 0.125 + 0.62), strec)
        kit.bevel(film, 0.02, 3)
        grp.append(film)
        for g in grp:
            g.rotation_euler[2] = rz

    # giriş: sahne 2'nin numune küpüyle eşleşen gevşek blok (paletlerin yanında, zeminde)
    loose = kit.gecmeli_blok('GevsekBlok', 0.60, 0.25, 0.25, stack)
    loose.location = (LOOSE[0], LOOSE[1], 0.125)
    loose.rotation_euler[2] = math.radians(-24)
    # çıkış: şantiyeyi çevreleyen lime halka (diğer sahnelerdeki halka motifi; küre sahnesinde
    # İzmir'deki halkayla eşleşir)
    ring = kit.halo_ring('SahaHalka', radius=12.5, width=0.22, strength=0.0, segments=256, z=0.08)
    # --- Çevre: uzak tepeler (hava perspektifi), kule vinç, sokak lambaları, aile silüeti ---
    import random
    rnd = random.Random(11)
    tepe_m = simple_material('Tepe', '#5f6b57', rough=1.0)
    tb = tepe_m.node_tree.nodes.get('Principled BSDF')
    tb.inputs['Emission Color'].default_value = (0.62, 0.70, 0.78, 1.0)  # uzaklık pusu (gök rengine yaklaşır)
    tb.inputs['Emission Strength'].default_value = 0.07
    for i in range(34):
        a = math.radians(rnd.uniform(-180, 180))
        r = rnd.uniform(320, 520)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.0, location=(math.cos(a) * r, math.sin(a) * r, -6.0))
        h = bpy.context.active_object
        h.name = 'Tepe'
        h.scale = (rnd.uniform(70, 150), rnd.uniform(50, 100), rnd.uniform(9, 22))
        h.rotation_euler[2] = a
        h.data.materials.append(tepe_m)
        h.visible_shadow = False
        bpy.ops.object.shade_smooth()
    # kule vinç (sarı; yeşil yalnız bizim ürüne): kafes görünümü tel kafes değiştiricisiyle
    vinc_m = simple_material('Vinc', '#d9a520', rough=0.55, metal=0.3)
    def kafes(name, size, loc, kalin=0.07):
        """Kafes kiriş: 4 köşe çubuğu + aralıklı çapraz bağlar (değiştirici/düzen modu yok)."""
        ax = max(range(3), key=lambda i: size[i])  # uzun eksen
        L = size[ax]
        oth = [i for i in range(3) if i != ax]
        w = [size[i] for i in oth]
        for c0 in (-0.5, 0.5):
            for c1 in (-0.5, 0.5):
                p = list(loc)
                p[oth[0]] += c0 * w[0]
                p[oth[1]] += c1 * w[1]
                d = [kalin] * 3
                d[ax] = L
                kit.box(name, tuple(d), tuple(p), vinc_m)
        n = max(2, int(L / 1.8))
        for j in range(n + 1):
            p = list(loc)
            p[ax] += -L / 2 + L * j / n
            for c0, c1 in ((0.0, -0.5), (0.0, 0.5), (-0.5, 0.0), (0.5, 0.0)):
                q = list(p)
                d = [kalin] * 3
                if c0 == 0.0:
                    q[oth[1]] += c1 * w[1]
                    d[oth[0]] = w[0]
                else:
                    q[oth[0]] += c0 * w[0]
                    d[oth[1]] = w[1]
                kit.box(name, tuple(d), tuple(q), vinc_m)
    VX, VY = -15.0, 13.0
    kafes('VincDirek', (1.6, 1.6, 34.0), (VX, VY, 17.0))
    kafes('VincBom', (42.0, 1.4, 1.6), (VX - 12.0, VY, 34.8))
    kafes('VincKarsiBom', (12.0, 1.4, 1.2), (VX + 9.5, VY, 34.7))
    kit.box('VincAgirlik', (3.0, 2.0, 2.2), (VX + 13.5, VY, 33.4), simple_material('VincBeton', '#8a8a86', rough=0.9))
    kit.box('VincKabin', (2.0, 2.0, 2.0), (VX - 1.6, VY, 33.6), vinc_m)
    kit.box('VincTepe', (1.2, 1.2, 6.0), (VX, VY, 38.0), vinc_m)
    halat = simple_material('Halat', '#222222', rough=0.6)
    kit.box('VincHalat', (0.04, 0.04, 22.0), (VX - 22.0, VY, 23.6), halat)
    # sokak lambaları (gece yanar)
    lamba_m = simple_material('Direk', '#3a3d40', rough=0.5, metal=0.6)
    lamba_isik = []
    for (lx, ly) in [(-10.5, -9.0), (10.5, -9.5), (12.5, 3.5)]:
        kit.box('LambaDirek', (0.14, 0.14, 6.0), (lx, ly, 3.0), lamba_m)
        kit.box('LambaKol', (1.2, 0.12, 0.12), (lx + 0.5, ly, 6.0), lamba_m)
        bas = kit.box('LambaBas', (0.5, 0.25, 0.12), (lx + 1.0, ly, 5.92), simple_material('LambaCam', '#fff2d0', rough=0.3))
        bb = bas.data.materials[0].node_tree.nodes.get('Principled BSDF')
        bb.inputs['Emission Color'].default_value = (1.0, 0.82, 0.55, 1.0)
        ld_ = bpy.data.lights.new('Lamba', 'POINT')
        ld_.energy = 0.0
        ld_.color = (1.0, 0.8, 0.55)
        ld_.shadow_soft_size = 0.3
        lo_ = bpy.data.objects.new('Lamba', ld_)
        lo_.location = (lx + 1.0, ly, 5.6)
        kit.link(lo_)
        lamba_isik.append((ld_, bb))
    # aile silüeti: 1. kat ön cephe, sağ pencerenin arkasında (iç ışık yanınca belirir)
    sil_m = simple_material('Siluet', '#0b0b0c', rough=0.9)
    siluetler = []
    def insan(x, y, boy):
        z0 = FH  # 1. kat döşeme üstü
        siluetler.append(kit.box('Govde', (0.42 * boy / 1.75, 0.26, 0.62 * boy / 1.75), (x, y, z0 + 0.95 * boy / 1.75), sil_m))
        siluetler.append(kit.box('Bacak', (0.34 * boy / 1.75, 0.22, 0.8 * boy / 1.75), (x, y, z0 + 0.4 * boy / 1.75), sil_m))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12 * boy / 1.75, location=(x, y, z0 + 1.42 * boy / 1.75))
        bpy.context.active_object.data.materials.append(sil_m)
        siluetler.append(bpy.context.active_object)
    insan(3.6, YS[0] + 0.75, 1.78)
    insan(4.15, YS[0] + 0.8, 1.62)
    insan(4.55, YS[0] + 0.7, 1.12)
    dusk = dict(world=world, sun=sun, ic=icb, ring=ring, lambalar=lamba_isik, siluet=siluetler)
    kit.sinematik(bloom=0.35, esik=1.8, boyut=0.6)
    cam = kit.camera('Kamera', lens=v['lens'], loc=(0, -30, 8), target=(0, 0, 5), fstop=11.0)
    return cam, objs, wall_mats, dusk


def cam_pose(t, variant):
    v = VARIANTS[variant]
    d = v['dist']
    yaw = math.radians(kit.lerp(-50, 30, kit.smoother(t)))
    # temel ve karkas: yukarıdan; çatı panelleri (0,70–0,82): yükselir; son: alçak kahraman açısı
    h = kit.lerp(11.0, 8.5, kit.smooth(kit.seg(t, 0.05, 0.4)))
    h += 9.0 * kit.smooth(kit.seg(t, 0.62, 0.74)) * (1 - kit.smooth(kit.seg(t, 0.84, 0.96)))
    h -= 3.6 * kit.smooth(kit.seg(t, 0.86, 1.0))
    dist = d * kit.lerp(0.95, 1.0, kit.smooth(kit.seg(t, 0.0, 0.4))) * kit.lerp(1.0, 0.93, kit.smooth(kit.seg(t, 0.86, 1.0)))
    tz = kit.lerp(2.5, 6.0, kit.smooth(kit.seg(t, 0.05, 0.5)))
    loc = Vector((math.sin(yaw) * dist, -math.cos(yaw) * dist, h))
    return loc, Vector((0, 0, tz))


def _kure(target, loc):
    v_ = loc - target
    dist = v_.length
    return dist, math.atan2(v_.x, -v_.y), math.asin(max(-1.0, min(1.0, v_.z / dist)))


def _konum(target, dist, yaw, pitch):
    return target + Vector((math.sin(yaw) * math.cos(pitch), -math.cos(yaw) * math.cos(pitch), math.sin(pitch))) * dist


def _ara(A, B, w):
    """İki küresel poz arası: hedef doğrusal, uzaklık logaritmik, açılar doğrusal."""
    (ta, da, ya, pa), (tb, db, yb, pb) = A, B
    if yb - ya > math.pi:
        yb -= 2 * math.pi
    elif ya - yb > math.pi:
        yb += 2 * math.pi
    target = ta.lerp(tb, w)
    dist = math.exp(kit.lerp(math.log(da), math.log(db), w))
    return _konum(target, dist, kit.lerp(ya, yb, w), kit.lerp(pa, pb, w)), target


def sahne_kamera(u, variant):
    t = yapim_t(u)
    loc, target = cam_pose(t, variant)
    if u < U_GIRIS + 0.06:
        # giriş: gevşek bloğun yakın planından (numune küpü karesi) şantiye genel planına
        b = Vector((LOOSE[0], LOOSE[1], 0.14))
        d_loc, d_tg = cam_pose(0.0, variant)
        dist0, yaw0, pitch0 = _kure(d_tg, d_loc)
        A = (b, 1.55 if variant == 'd' else 1.45, yaw0 + math.radians(8), math.radians(20))
        B = (d_tg, dist0, yaw0, pitch0)
        w = kit.smoother(kit.seg(u, 0.0, U_GIRIS + 0.06))
        return _ara(A, B, w)
    if u > U_CIKIS + 0.02:
        # çıkış: kahraman açısından tepeye yükselir, aşağı bakar (küre sahnesinde İzmir'e eşleşir)
        e_loc, e_tg = cam_pose(1.0, variant)
        dist1, yaw1, pitch1 = _kure(e_tg, e_loc)
        A = (e_tg, dist1, yaw1, pitch1)
        B = (Vector((0, 0, 0)), 62.0 if variant == 'd' else 74.0, yaw1 + math.radians(40), math.radians(80))
        w = kit.smoother(kit.seg(u, U_CIKIS + 0.02, 1.0))
        return _ara(A, B, w)
    return loc, target


def alacakaranlik(dusk, u):
    """Çıkışta gün batar: güneş alçalır ve söner, gök kararır, pencereler ve saha halkası yanar."""
    k = kit.smooth(kit.seg(u, U_CIKIS, 0.96))
    sky = dusk['world'].node_tree.nodes['Sky Texture']
    sky.sun_elevation = math.radians(kit.lerp(22.0, -2.0, k))
    dusk['world'].node_tree.nodes['Background'].inputs['Strength'].default_value = kit.lerp(0.26, 0.11, k)
    dusk['sun'].data.energy = kit.lerp(3.6, 0.0, kit.smooth(kit.seg(u, U_CIKIS, 0.93)))
    dusk['sun'].rotation_euler[0] = math.radians(kit.lerp(66.0, 88.0, k))
    dusk['ic'].inputs['Emission Strength'].default_value = 4.0 * kit.smooth(kit.seg(u, 0.84, 0.97))
    ring_m = dusk['ring'].data.materials[0].node_tree.nodes['Emission']
    ring_m.inputs['Strength'].default_value = 7.0 * kit.smooth(kit.seg(u, 0.86, 0.98))
    dusk['ring'].hide_render = u < 0.855
    for ob in dusk.get('siluet', []):
        ob.hide_render = u < 0.83  # aile ev bitince gelir
    kl = kit.smooth(kit.seg(u, 0.83, 0.92))
    for ld_, bb in dusk.get('lambalar', []):
        ld_.energy = 140.0 * kl
        bb.inputs['Emission Strength'].default_value = 25.0 * kl
    bpy.context.scene.view_settings.exposure = kit.lerp(-0.55, 0.7, k)


def apply_state(objs, t):
    # temel
    kf = kit.smoother(kit.seg(t, *T_FOUND))
    objs['found'].location.z = -0.13 - 0.6 * (1 - kf)
    objs['found'].hide_render = kf <= 0.0
    # karkas
    for c in objs['cols']:
        k = c['k']
        a = T_FRAME0 + k * T_FRAME_STEP
        u = kit.smoother(kit.seg(t, a, a + 0.035))
        c.hide_render = u <= 0.0
        c.scale = (1, 1, max(u, 0.001))
        c.location.z = k * FH + FH * max(u, 0.001) / 2
    for s in objs['slabs'] + objs['beams']:
        k = s['k']
        a = T_FRAME0 + k * T_FRAME_STEP + 0.03
        u = kit.smoother(kit.seg(t, a, a + 0.04))
        s.hide_render = u <= 0.0
        s.scale = (max(u, 0.001), max(u, 0.001), 1)
    # duvarlar: o katın örülmesi başlamadıysa nesne tamamen gizli
    # (saydam maskeli çok sayıda yüzey üst üste binince ışın sınırı aşılıp kara çizgi olmasın)
    for w in objs['walls']:
        w.hide_render = t <= T_WALL0 + w['k'] * T_WALL_STAGGER
    # lentolar: yukarıdan oturur
    for lt in objs['lintels']:
        k = lt['k']
        a = T_LINTEL[0] + k * 0.025
        u = kit.smoother(kit.seg(t, a, a + 0.035))
        lt.hide_render = u <= 0.0
        lt.location.z = lt['z'] + 1.2 * (1 - u)
    # çatı panelleri: sırayla kayarak yerleşir
    n = len(objs['roof'])
    for p in objs['roof']:
        a = T_ROOF[0] + (T_ROOF[1] - T_ROOF[0] - 0.03) * p['i'] / n
        u = kit.smoother(kit.seg(t, a, a + 0.03))
        p.hide_render = u <= 0.0
        p.location.z = p['z'] + 2.0 * (1 - u)
    # doğramalar
    for i, parts in enumerate(objs['wins']):
        a = T_WIN[0] + (parts[0]['k'] * 0.02) + (i % 10) * 0.003
        u = kit.smoother(kit.seg(t, a, a + 0.03))
        for p_ in parts:
            p_.hide_render = u <= 0.0
    # iç karanlık hacim: o katın döşemesi gelince
    for ic in objs['ic']:
        a = T_FRAME0 + ic['k'] * T_FRAME_STEP + 0.07
        ic.hide_render = t < a


def main():
    os.makedirs(ARGS.out, exist_ok=True)
    cam, objs, wall_mats, dusk = build(ARGS.variant)
    # zaman düğümü: duvar malzemelerinde 'zaman' girişini bul (wall_material'a None verildi → ilk SUBTRACT girişi)
    time_inputs = []
    for mat in wall_mats.values():
        for n in mat.node_tree.nodes:
            if n.type == 'MATH' and n.operation == 'SUBTRACT' and not n.inputs[0].is_linked and abs(n.inputs[1].default_value - T_WALL0) < 1e-6:
                time_inputs.append(n.inputs[0])
    assert time_inputs, 'zaman girişi bulunamadı'
    frames = pass_order(FRAMES) if ARGS.frames == 'all' else [int(x) for x in ARGS.frames.split(',')]
    meta_path = os.path.join(ARGS.out, 'meta.json')
    meta = {'frames': FRAMES, 'res': VARIANTS[ARGS.variant]['res'], 'hotspots': {}}
    if os.path.exists(meta_path):  # kısmi işler (kaba/ara/ince geçiş) birbirinin noktalarını silmesin
        import json
        _eski = json.load(open(meta_path, encoding='utf-8'))
        if _eski.get('frames') == FRAMES:
            meta['hotspots'].update(_eski.get('hotspots', {}))
    for f in frames:
        u = f / (FRAMES - 1)
        t = yapim_t(u)
        for inp in time_inputs:
            inp.default_value = t
        apply_state(objs, t)
        alacakaranlik(dusk, u)
        loc, target = sahne_kamera(u, ARGS.variant)
        cam.location = loc
        kit.aim(cam, target)
        kit.kaydir(cam, ARGS.variant, 1.0)
        cam.data.dof.focus_distance = (target - loc).length
        hs = {}
        pts = {}
        if t >= 0.5:
            pts['duvar'] = (-4.0, YS[0] - WT / 2, 1.6)
        if t >= 0.66:
            pts['lento'] = (0.0, YS[0] - WT / 2, FH + SLAB + 0.9 + 1.4 + 0.1)
        if t >= 0.80:
            pts['cati'] = (2.4, -2.25, FLOORS * FH + 0.2)
        if u > 0.86:
            pts = {}
        if pts:
            proj = kit.project(cam, list(pts.values()))
            hs = {k: p for k, p in zip(pts.keys(), proj) if p and 0.03 < p[0] < 0.97 and 0.05 < p[1] < 0.95}
        meta['hotspots'][str(f)] = hs
        path = os.path.join(ARGS.out, f'{f:03d}.png')
        if ARGS.skip_existing and os.path.exists(path):
            continue
        t0 = time.time()
        kit.render_to(path)
        print(f'KARE {f} {time.time() - t0:.1f}s', flush=True)
        kit.write_json(meta_path, meta)
    kit.write_json(meta_path, meta)


def pass_order(n):
    order, seen = [], set()
    min_step = int(os.environ.get('EGE_MINSTEP', '1'))
    for step in [x for x in (8, 4, 2, 1) if x >= min_step]:
        for f in range(0, n, step):
            if f not in seen:
                seen.add(f)
                order.append(f)
    # son kare (sahnenin "sonuç" karesi) ilk kareden hemen sonra: erken teslimde de var olsun
    if n - 1 in order:
        order.remove(n - 1)
    order.insert(1, n - 1)
    return order


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--variant', default='d')
    ap.add_argument('--frames', default='all')
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=24)
    ap.add_argument('--skip-existing', action='store_true')
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
