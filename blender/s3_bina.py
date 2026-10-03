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

FRAMES = 96
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
    'd': dict(res=(1600, 900), lens=35.0, dist=27.5),
    'm': dict(res=(768, 1366), lens=40.0, dist=22.0),
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
    local = m('SUBTRACT', m('SUBTRACT', z, m('MULTIPLY', fl, FH, loc=(-900, -1250)), loc=(-750, -1150)), SLAB, loc=(-600, -1150))
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


def build(variant):
    kit.reset()
    v = VARIANTS[variant]
    kit.setup_render(*v['res'], samples=ARGS.samples, threshold=0.02, bounces=(4, 2, 2, 4))
    world = kit.studio_world(hdri='studio.exr', hdri_strength=0.3)
    kit.replace_reflection_env(world, 1.0)

    floor = kit.box('Zemin', (400, 400, 0.2), (0, 0, -0.1), kit.glossy_floor(rough=0.22))
    ring = kit.halo_ring('Hale', radius=11.5, width=0.06, strength=4.0, segments=256)

    sun_d = bpy.data.lights.new('Gunes', 'SUN')
    sun_d.energy = 3.2
    sun_d.angle = math.radians(2.5)
    sun_d.color = (1.0, 0.95, 0.88)
    sun = bpy.data.objects.new('Gunes', sun_d)
    sun.rotation_euler = (math.radians(52), 0, math.radians(-38))
    kit.link(sun)
    r1 = kit.area_light('KonturSol', (-22, 20, 14), (0, 0, 0), (4, 16), 2600, kit.LIME_HI)
    kit.aim(r1, (0, 0, 5))
    r2 = kit.area_light('KonturSag', (24, 18, 12), (0, 0, 0), (4, 16), 8000, (0.86, 0.93, 1.0))
    kit.aim(r2, (0, 0, 5))
    for ob in (r1, r2):
        ob.visible_glossy = False
    fill = kit.area_light('Dolgu', (6, -30, 10), (0, 0, 0), (20, 10), 5200, (0.92, 0.95, 1.0))
    kit.aim(fill, (0, 0, 5))

    conc = concrete_material()
    wall_mats = {}  # duvar malzemeleri; 'zaman' girişi main() içinde her karede güncellenir

    objs = {'found': None, 'cols': [], 'slabs': [], 'beams': [], 'walls': [], 'lintels': [], 'roof': [], 'wins': []}
    objs['found'] = kit.box('Temel', (13.2, 10.2, 0.5), (0, 0, -0.25), conc)

    for k in range(FLOORS):
        z0 = k * FH
        for x in XS:
            for y in YS:
                c = kit.box(f'Kolon{k}_{x}_{y}', (COL, COL, FH), (x, y, z0 + FH / 2), conc)
                c['k'] = k
                objs['cols'].append(c)
        zt = z0 + FH
        s = kit.box(f'Doseme{k + 1}', (12.6, 9.6, SLAB), (0, 0, zt - SLAB / 2), conc)
        s['k'] = k
        objs['slabs'].append(s)
        for y in YS:
            b = kit.box(f'KirisX{k}_{y}', (12.3, 0.3, BEAM_D), (0, y, zt - SLAB - BEAM_D / 2), conc)
            b['k'] = k
            objs['beams'].append(b)
        for x in XS:
            b = kit.box(f'KirisY{k}_{x}', (0.3, 9.3, BEAM_D), (x, 0, zt - SLAB - BEAM_D / 2), conc)
            b['k'] = k
            objs['beams'].append(b)

    # duvarlar (pencere boşluklu parçalar) + lentolar + doğramalar
    lintel_mat = kit.aac_material('Lento', bump=0.5)
    frame_mat = simple_material('Dograma', '#2b3034', rough=0.35)
    glass_mat = simple_material('Cam', '#c8d4da', rough=0.02, transmission=1.0, ior=1.5)
    for axis in ('X', 'Y'):
        wall_mats[axis] = wall_material(axis, None)
    win_w, win_h, sill = 1.5, 1.4, 0.9
    for k in range(FLOORS):
        zb = k * FH + SLAB  # duvar tabanı
        for (axis, c, a, b) in bays():
            mid = (a + b) / 2
            is_door = (k == 0 and axis == 'X' and c == YS[0] and abs(mid) < 0.1)
            ow, oh, os_ = (1.3, 2.2, 0.0) if is_door else (win_w, win_h, sill)
            o0, o1 = mid - ow / 2, mid + ow / 2
            pieces = [(a, o0, 0.0, CLEAR), (o1, b, 0.0, CLEAR)]
            if os_ > 0:
                pieces.append((o0, o1, 0.0, os_))
            top0 = os_ + oh
            pieces.append((o0, o1, top0, CLEAR))
            for (p0, p1, h0, h1) in pieces:
                L = p1 - p0
                cx = (p0 + p1) / 2
                if axis == 'X':
                    w = kit.box('Duvar', (L, WT, h1 - h0), (cx, c, zb + (h0 + h1) / 2), wall_mats['X'])
                else:
                    w = kit.box('Duvar', (WT, L, h1 - h0), (c, cx, zb + (h0 + h1) / 2), wall_mats['Y'])
                objs['walls'].append(w)
            # lento: açıklığın üstünde, iki yana 20 cm oturur
            lz = zb + top0 + 0.1
            if axis == 'X':
                lt = kit.box('Lento', (ow + 0.4, WT + 0.01, 0.2), (mid, c, lz), lintel_mat)
            else:
                lt = kit.box('Lento', (WT + 0.01, ow + 0.4, 0.2), (c, mid, lz), lintel_mat)
            lt['k'] = k
            lt['z'] = lz
            objs['lintels'].append(lt)
            # doğrama + cam
            fz = zb + os_ + oh / 2
            if axis == 'X':
                fr = kit.box('Kasa', (ow - 0.02, 0.07, oh - 0.02), (mid, c - 0.03, fz), frame_mat)
                gl = kit.box('Cam', (ow - 0.16, 0.012, oh - 0.16), (mid, c - 0.07, fz), glass_mat)
            else:
                fr = kit.box('Kasa', (0.07, ow - 0.02, oh - 0.02), (c + (0.03 if c < 0 else -0.03), mid, fz), frame_mat)
                gl = kit.box('Cam', (0.012, ow - 0.16, oh - 0.16), (c + (-0.07 if c < 0 else 0.07), mid, fz), glass_mat)
            fr['k'] = gl['k'] = k
            objs['wins'].append((fr, gl))
            if is_door:
                fr['door'] = True
                fr.hide_render = gl.hide_render = True

    # çatı panelleri (gazbeton döşeme/çatı paneli 60 cm genişlik)
    roof_mat = kit.aac_material('CatiPaneli', bump=0.5)
    zr = FLOORS * FH + 0.1
    for row, y0 in enumerate((-2.25, 2.25)):
        for i in range(20):
            x = -5.7 + i * 0.6
            p = kit.box('Panel', (0.595, 4.45, 0.2), (x, y0, zr), roof_mat)
            p['z'] = zr
            p['i'] = row * 20 + i
            objs['roof'].append(p)

    # sahadaki paletler (yeşil streç)
    pal_mat = simple_material('Ahsap', '#8a6a46', rough=0.8)
    strec = stretch_material()
    stack = kit.aac_material('Istif', bump=0.4)
    for i, (px, py) in enumerate([(-9.2, -7.4), (-7.8, -7.6), (-9.0, -9.0)]):
        kit.box('Palet', (1.2, 1.0, 0.14), (px, py, 0.07), pal_mat)
        # bloklar 5 sıra × 2 (60 × 25): sıra aralarında ince derz gölgesi
        for r in range(5):
            for j in range(2):
                kit.box('IstifBlok', (0.598, 0.998, 0.248), (px - 0.3 + j * 0.6, py, 0.14 + 0.125 + r * 0.25), stack)
        b = kit.box('PaletStrec', (1.215, 1.015, 1.255), (px, py, 0.14 + 0.6275), strec)
        kit.bevel(b, 0.015, 3)

    cam = kit.camera('Kamera', lens=v['lens'], loc=(0, -30, 8), target=(0, 0, 5), fstop=11.0)
    return cam, objs, wall_mats


def cam_pose(t, variant):
    v = VARIANTS[variant]
    d = v['dist']
    # yavaş yörünge: sol önden sağ öne; sonunda hafif alçak, etkileyici açı
    yaw = math.radians(kit.lerp(-48, 28, kit.smoother(t)))
    h = kit.lerp(7.0, 9.5, kit.smooth(kit.seg(t, 0.0, 0.5))) - 2.5 * kit.smooth(kit.seg(t, 0.75, 1.0))
    dist = d * kit.lerp(0.92, 1.0, kit.smooth(kit.seg(t, 0.0, 0.4))) * kit.lerp(1.0, 0.9, kit.smooth(kit.seg(t, 0.8, 1.0)))
    tz = kit.lerp(3.0, 6.0, kit.smooth(kit.seg(t, 0.05, 0.5)))
    loc = Vector((math.sin(yaw) * dist, -math.cos(yaw) * dist, h))
    return loc, Vector((0, 0, tz))


def apply_state(objs, t):
    # temel
    kf = kit.smoother(kit.seg(t, *T_FOUND))
    objs['found'].location.z = -0.25 - 0.6 * (1 - kf)
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
    for i, (fr, gl) in enumerate(objs['wins']):
        if fr.get('door'):
            continue
        a = T_WIN[0] + (fr['k'] * 0.02) + (i % 10) * 0.003
        u = kit.smoother(kit.seg(t, a, a + 0.03))
        fr.hide_render = gl.hide_render = u <= 0.0


def main():
    os.makedirs(ARGS.out, exist_ok=True)
    cam, objs, wall_mats = build(ARGS.variant)
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
    for f in frames:
        t = f / (FRAMES - 1)
        for inp in time_inputs:
            inp.default_value = t
        apply_state(objs, t)
        loc, target = cam_pose(t, ARGS.variant)
        cam.location = loc
        kit.aim(cam, target)
        cam.data.dof.focus_distance = (target - loc).length
        hs = {}
        pts = {}
        if t >= 0.5:
            pts['duvar'] = (-4.0, YS[0] - WT / 2, 1.6)
        if t >= 0.66:
            pts['lento'] = (0.0, YS[0] - WT / 2, FH + SLAB + 0.9 + 1.4 + 0.1)
        if t >= 0.80:
            pts['cati'] = (2.4, -2.25, FLOORS * FH + 0.2)
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
    if n - 1 not in seen:
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
