"""
Sahne 1 — "Doğuş": blok hammaddelerine çözülür → girdap → kalıpta kabarır → tel kesim.

Giriş   (0,00–0,24) Blok üstten alta lime bir ışık cephesiyle çözülür; taneler kopar
                    ve dört gazbeton kaidenin üstünde hammadde bulutlarına ayrışır:
                    kum · kireç · çimento · alçı (+ ortada alüminyum parıltısı).
Gelişme (0,40–0,64) Bulutlar tek, dar bir girdapta karışarak kalıba iner.
Sonuç   (0,62–1,00) Karışım kalıpta kabarır, teller keser, bloklar ayrılır;
                    kamera ön bloğun yüzüne yaklaşır (Sahne 2 gözeneğe dalar).

Sahne 0'ın son karesiyle aynı kamera ve ışıkla başlar → kesintisiz geçiş.

Kullanım: python s1_dogus.py --variant d|m --frames all|0,40 --out DIR
"""
import argparse
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import s0_video_blok as s0  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

FRAMES = 96
L, H, T = s0.L, s0.H, s0.T
N_GRAIN = 4800

# Kalıp (temsilî ölçek): iç ölçü
MOLD_L, MOLD_W, MOLD_H = 0.95, 0.44, 0.27
MOLD_C = Vector((0.0, 0.02, 0.0))
# Hammadde kaideleri (gazbeton kaideler, yay biçiminde) — x, y, yükseklik
PEDESTALS = [(-0.86, 0.42, 0.26), (-0.30, 0.62, 0.34), (0.30, 0.62, 0.34), (0.86, 0.42, 0.26)]
ALU_CLOUD = (0.0, 0.50, 0.62)
CUT_N = 5  # kek 5 bloğa kesilir (uzunluk boyunca)

TYPES = [  # ad, renk, oran, metal, pürüz, boy çarpanı
    ('kum', kit.SAND, 0.40, 0.0, 0.75, 1.0),
    ('kirec', kit.LIMEWASH, 0.17, 0.0, 0.6, 0.9),
    ('cimento', kit.CEMENT, 0.28, 0.0, 0.8, 0.85),
    ('alci', kit.GYPSUM, 0.10, 0.0, 0.7, 0.95),
    ('aluminyum', kit.ALU, 0.05, 1.0, 0.25, 0.7),
]


def grain_setup(n, seed=29):
    rng = np.random.default_rng(seed)
    probs = np.array([t[2] for t in TYPES])
    kind = rng.choice(len(TYPES), size=n, p=probs / probs.sum())
    u = rng.random((n, 3))
    home = np.stack([(u[:, 0] - 0.5) * L, (u[:, 1] - 0.5) * T, u[:, 2] * H], 1)
    birth = 0.03 + (1 - home[:, 2] / H) * 0.17 + rng.random(n) * 0.05
    # her tür kendi kaidesinin üstünde küresel bulut; alüminyum ortada havada
    centers = np.array([[px, py, ph + 0.17] for (px, py, ph) in PEDESTALS] + [list(ALU_CLOUD)])
    cc = centers[kind]
    dirs = rng.normal(size=(n, 3))
    dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    rad = np.where(kind == 4, 0.07, 0.115) * rng.random(n) ** (1 / 3)
    cloud = cc + dirs * rad[:, None]
    # karışım girdabı: kalıp merkezinde dar sarmal, yukarıdan aşağı
    mix_start = 0.40 + rng.random(n) * 0.10 + kind * 0.012
    helix_r = 0.05 + rng.random(n) * 0.13
    helix_phase = rng.random(n) * 6.283
    tgt = np.stack([(rng.random(n) - 0.5) * (MOLD_L - 0.08) + MOLD_C.x,
                    (rng.random(n) - 0.5) * (MOLD_W - 0.06) + MOLD_C.y,
                    rng.random(n) * 0.06 + 0.02], 1)
    size = np.array([t[5] for t in TYPES])[kind] * (0.0028 + rng.random(n) * 0.0026)
    col = np.array([t[1] for t in TYPES])[kind]
    metal = np.array([t[3] for t in TYPES])[kind]
    return dict(kind=kind, home=home, birth=birth, cloud=cloud, cc=cc, mix_start=mix_start,
                helix_r=helix_r, helix_phase=helix_phase, tgt=tgt, size=size, col=col, metal=metal)


def grain_state(g, t):
    """t (0..1) → konumlar ve ölçekler. Hiçbir aşama sıçramaz (hepsi yumuşak geçiş)."""
    b = g['birth']
    # 1) blokdan buluta (yay çizerek)
    k1 = np.clip((t - b) / 0.13, 0, 1)
    k1 = k1 * k1 * (3 - 2 * k1)
    arc = np.sin(k1 * np.pi)[:, None] * np.array([0.0, -0.05, 0.22])
    # bulut kendi ekseninde yavaşça döner
    ang = (t - 0.2) * 1.6
    rel = g['cloud'] - g['cc']
    rot = np.stack([rel[:, 0] * np.cos(ang) - rel[:, 1] * np.sin(ang), rel[:, 0] * np.sin(ang) + rel[:, 1] * np.cos(ang), rel[:, 2]], 1)
    cloud = g['cc'] + rot
    p = g['home'] * (1 - k1[:, None]) + cloud * k1[:, None] + arc
    # 2) buluttan girdaba → kalıba
    k2 = np.clip((t - g['mix_start']) / 0.16, 0, 1)
    tv = np.clip(t - g['mix_start'], 0, None)
    hz = np.clip(0.95 - tv * 3.6, 0.08, None)
    th = g['helix_phase'] + tv * 26.0
    hr = g['helix_r'] * (0.45 + 0.55 * np.clip(hz / 0.95, 0, 1))
    helix = np.stack([MOLD_C.x + np.cos(th) * hr, MOLD_C.y + np.sin(th) * hr, hz], 1)
    k2s = k2 * k2 * (3 - 2 * k2)
    p = p * (1 - k2s[:, None]) + helix * k2s[:, None]
    k3 = np.clip((t - g['mix_start'] - 0.17) / 0.06, 0, 1)
    k3s = k3 * k3 * (3 - 2 * k3)
    p = p * (1 - k3s[:, None]) + g['tgt'] * k3s[:, None]
    grow = np.clip((t - b) / 0.03, 0, 1) * (t >= b)
    fade = 1 - np.clip((t - g['mix_start'] - 0.20) / 0.05, 0, 1)
    return p, g['size'] * grow * fade


def build_pedestals(aac):
    """Hammadde bulutlarının durduğu gazbeton kaideler (Kutay 30.09: 'kaide')."""
    obs = []
    for i, (px, py, ph) in enumerate(PEDESTALS):
        b = kit.box(f'Kaide{i}', (0.22, 0.22, ph), (px, py, ph / 2), aac)
        kit.bevel(b, 0.003, 2)
        obs.append(b)
    return obs


def make_grain_object(g):
    n = len(g['kind'])
    me = bpy.data.meshes.new('Taneler')
    me.vertices.add(n)
    me.update()
    ob = bpy.data.objects.new('Taneler', me)
    kit.link(ob)
    me.attributes.new('olcek', 'FLOAT', 'POINT')
    me.attributes.new('renk', 'FLOAT_COLOR', 'POINT')
    me.attributes.new('metal', 'FLOAT', 'POINT')
    me.attributes['renk'].data.foreach_set('color', g['col'].astype(np.float32).ravel())
    me.attributes['metal'].data.foreach_set('value', g['metal'].astype(np.float32))

    mat = bpy.data.materials.new('Tane')
    mat.use_nodes = True
    nt = kit.NT(mat.node_tree)
    bsdf = nt.n.get('Principled BSDF')
    a = nt.node('ShaderNodeAttribute', (-400, 200), attribute_type='INSTANCER', attribute_name='renk')
    nt.link(a.outputs['Color'], bsdf.inputs['Base Color'])
    m = nt.node('ShaderNodeAttribute', (-400, -100), attribute_type='INSTANCER', attribute_name='metal')
    nt.link(m.outputs['Fac'], bsdf.inputs['Metallic'])
    rr = nt.node('ShaderNodeMapRange', (-200, -250))
    nt.link(m.outputs['Fac'], rr.inputs['Value'])
    rr.inputs['To Min'].default_value = 0.72
    rr.inputs['To Max'].default_value = 0.22
    nt.link(rr.outputs['Result'], bsdf.inputs['Roughness'])
    # alüminyum tozu karanlık stüdyoda kararmasın: metal oranında hafif ışıma
    em = nt.node('ShaderNodeMath', (-200, -450), operation='MULTIPLY')
    nt.link(m.outputs['Fac'], em.inputs[0])
    em.inputs[1].default_value = 0.9
    bsdf.inputs['Emission Color'].default_value = (0.92, 0.95, 1.0, 1)
    nt.link(em.outputs[0], bsdf.inputs['Emission Strength'])

    ng = bpy.data.node_groups.new('TaneGN', 'GeometryNodeTree')
    ng.interface.new_socket(name='Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    gi = ng.nodes.new('NodeGroupInput')
    go = ng.nodes.new('NodeGroupOutput')
    ico = ng.nodes.new('GeometryNodeMeshIcoSphere')
    ico.inputs['Radius'].default_value = 1.0
    ico.inputs['Subdivisions'].default_value = 2
    sm = ng.nodes.new('GeometryNodeSetMaterial')
    sm.inputs['Material'].default_value = mat
    ng.links.new(ico.outputs['Mesh'], sm.inputs['Geometry'])
    iop = ng.nodes.new('GeometryNodeInstanceOnPoints')
    ng.links.new(gi.outputs['Geometry'], iop.inputs['Points'])
    ng.links.new(sm.outputs['Geometry'], iop.inputs['Instance'])
    sc = ng.nodes.new('GeometryNodeInputNamedAttribute')
    sc.data_type = 'FLOAT'
    sc.inputs['Name'].default_value = 'olcek'
    ng.links.new(sc.outputs['Attribute'], iop.inputs['Scale'])
    rv = ng.nodes.new('FunctionNodeRandomValue')
    rv.data_type = 'FLOAT_VECTOR'
    rv.inputs['Max'].default_value = (6.283, 6.283, 6.283)
    ng.links.new(rv.outputs['Value'], iop.inputs['Rotation'])
    # düzensiz tane biçimi: örneklere hafif basık ölçek
    ng.links.new(iop.outputs['Instances'], go.inputs['Geometry'])
    mod = ob.modifiers.new('Taneler', 'NODES')
    mod.node_group = ng
    return ob


def update_grains(ob, pos, scale):
    me = ob.data
    me.vertices.foreach_set('co', pos.astype(np.float32).ravel())
    me.attributes['olcek'].data.foreach_set('value', scale.astype(np.float32))
    me.update()


def dissolve_material(base_mat):
    """Gazbeton malzemesine çözülme maskesi + lime ışık cephesi ekler (eşik = 'cephe' değeri)."""
    mat = base_mat.copy()
    mat.name = 'GazbetonCozulen'
    nt = kit.NT(mat.node_tree)
    out = [n for n in nt.n if n.type == 'OUTPUT_MATERIAL'][0]
    bsdf = [n for n in nt.n if n.type == 'BSDF_PRINCIPLED'][0]
    tc = nt.node('ShaderNodeTexCoord', (-200, -700))
    sep = nt.node('ShaderNodeSeparateXYZ', (0, -700))
    nt.link(tc.outputs['Object'], sep.inputs[0])
    noise = nt.node('ShaderNodeTexNoise', (0, -900))
    noise.inputs['Scale'].default_value = 7.0
    noise.inputs['Detail'].default_value = 4.0
    nt.link(tc.outputs['Object'], noise.inputs['Vector'])
    nz = nt.math('MULTIPLY_ADD', noise.outputs['Fac'], 0.09, loc=(200, -900))
    nz.node.inputs[2].default_value = -0.045
    zz = nt.math('ADD', sep.outputs['Z'], nz, loc=(400, -750))  # yerel z (−H/2..H/2) + gürültü
    val = nt.node('ShaderNodeValue', (400, -550))
    val.name = 'cephe'
    val.outputs[0].default_value = 1.0
    diff = nt.math('SUBTRACT', zz, val.outputs[0], loc=(600, -700))  # >0 → çözülmüş
    keep = nt.math('LESS_THAN', diff, 0.0, loc=(800, -700))
    band = nt.math('ABSOLUTE', diff, loc=(800, -900))
    glow = nt.node('ShaderNodeMapRange', (1000, -900))
    nt.link(band, glow.inputs['Value'])
    glow.inputs['From Min'].default_value = 0.0
    glow.inputs['From Max'].default_value = 0.012
    glow.inputs['To Min'].default_value = 1.0
    glow.inputs['To Max'].default_value = 0.0
    em = nt.node('ShaderNodeEmission', (1200, -600))
    em.inputs['Color'].default_value = kit.LIME_HI
    em.inputs['Strength'].default_value = 14.0
    add = nt.node('ShaderNodeMixShader', (1400, -300))
    nt.link(glow.outputs['Result'], add.inputs[0])
    nt.link(bsdf.outputs[0], add.inputs[1])
    nt.link(em.outputs[0], add.inputs[2])
    tr = nt.node('ShaderNodeBsdfTransparent', (1400, -600))
    mix = nt.node('ShaderNodeMixShader', (1600, -300))
    nt.link(keep, mix.inputs[0])
    nt.link(tr.outputs[0], mix.inputs[1])
    nt.link(add.outputs[0], mix.inputs[2])
    nt.link(mix.outputs[0], out.inputs['Surface'])
    return mat, val


def steel_material():
    mat = bpy.data.materials.new('Kalip')
    mat.use_nodes = True
    nt = kit.NT(mat.node_tree)
    bsdf = nt.n.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = kit.srgb('#2b3236')
    bsdf.inputs['Metallic'].default_value = 0.85
    bsdf.inputs['Roughness'].default_value = 0.38
    noise = nt.node('ShaderNodeTexNoise', (-500, -200))
    noise.inputs['Scale'].default_value = 18.0
    mr = nt.node('ShaderNodeMapRange', (-300, -200))
    nt.link(noise.outputs['Fac'], mr.inputs['Value'])
    mr.inputs['To Min'].default_value = 0.3
    mr.inputs['To Max'].default_value = 0.5
    nt.link(mr.outputs['Result'], bsdf.inputs['Roughness'])
    return mat


def build_mold(steel):
    th = 0.025
    parts = {}
    cx, cy = MOLD_C.x, MOLD_C.y
    parts['taban'] = kit.box('KalipTaban', (MOLD_L + 2 * th, MOLD_W + 2 * th, th), (cx, cy, -th / 2 + 0.0005), steel)
    parts['on'] = kit.box('KalipOn', (MOLD_L + 2 * th, th, MOLD_H), (cx, cy - MOLD_W / 2 - th / 2, MOLD_H / 2), steel)
    parts['arka'] = kit.box('KalipArka', (MOLD_L + 2 * th, th, MOLD_H), (cx, cy + MOLD_W / 2 + th / 2, MOLD_H / 2), steel)
    parts['sol'] = kit.box('KalipSol', (th, MOLD_W, MOLD_H), (cx - MOLD_L / 2 - th / 2, cy, MOLD_H / 2), steel)
    parts['sag'] = kit.box('KalipSag', (th, MOLD_W, MOLD_H), (cx + MOLD_L / 2 + th / 2, cy, MOLD_H / 2), steel)
    for p in parts.values():
        kit.bevel(p, 0.004, 2)
    return parts


def build_cake(aac):
    """Kek: CUT_N blok (bitişik) + kabarık üst deri (ızgara, gürültülü kubbe)."""
    blocks = []
    bl = MOLD_L / CUT_N
    for i in range(CUT_N):
        x = MOLD_C.x - MOLD_L / 2 + bl * (i + 0.5)
        b = kit.box(f'Kek{i}', (bl, MOLD_W, 1.0), (x, MOLD_C.y, 0.5), aac)
        blocks.append(b)
    # üst deri
    nx, ny = 90, 44
    rng = np.random.default_rng(5)
    verts, faces = [], []
    xs = np.linspace(-MOLD_L / 2, MOLD_L / 2, nx)
    ys = np.linspace(-MOLD_W / 2, MOLD_W / 2, ny)
    bumps = rng.random((ny, nx))
    from numpy.fft import fft2, ifft2
    sm = np.real(ifft2(fft2(bumps) * np.exp(-((np.fft.fftfreq(nx)[None, :] ** 2 + np.fft.fftfreq(ny)[:, None] ** 2) / 0.004))))
    sm = (sm - sm.mean()) / (sm.std() + 1e-9)
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            dome = (1 - (2 * x / MOLD_L) ** 2) * (1 - (2 * y / MOLD_W) ** 2)
            verts.append((x, y, 0.022 * dome + 0.003 * sm[j, i]))
    for j in range(ny - 1):
        for i in range(nx - 1):
            a = j * nx + i
            faces.append((a, a + 1, a + nx + 1, a + nx))
    skin = kit.mesh_object('KekDeri', verts, faces, aac)
    for p in skin.data.polygons:
        p.use_smooth = True
    skin.location = (MOLD_C.x, MOLD_C.y, 0.0)
    return blocks, skin


def build_wires():
    mat = kit.emission_material('Tel', (1.0, 1.0, 1.0, 1), 6.0)
    wires = []
    for i in range(1, CUT_N):
        x = MOLD_C.x - MOLD_L / 2 + (MOLD_L / CUT_N) * i
        bpy.ops.mesh.primitive_cylinder_add(radius=0.0009, depth=MOLD_W + 0.05, location=(x, MOLD_C.y, 1.0), rotation=(math.pi / 2, 0, 0))
        w = bpy.context.active_object
        w.data.materials.append(mat)
        wires.append(w)
    return wires


def cam_pose(t, variant):
    """Sahne 0'ın son pozundan başlar; girdabı görmek için açılır, sonunda kesit yüzüne iner."""
    v = s0.VARIANTS[variant]
    e = v['end']

    def sph(target, dist, yaw, pitch):
        yaw, pitch = math.radians(yaw), math.radians(pitch)
        d = Vector((math.sin(yaw) * math.cos(pitch), -math.cos(yaw) * math.cos(pitch), math.sin(pitch)))
        return Vector(target) + d * dist

    keys = [  # (t, hedef, mesafe, yaw, pitch)
        (0.00, (e['tx'], 0.0, e['tz']), e['dist'], e['yaw'], e['pitch']),
        (0.14, (0.0, 0.2, 0.30), e['dist'] * 1.30, e['yaw'] - 12, e['pitch'] + 3),
        (0.26, (0.0, 0.38, 0.42), e['dist'] * 1.48, 6, 14),
        (0.40, (0.0, 0.40, 0.44), e['dist'] * 1.40, -6, 16),
        (0.56, (MOLD_C.x, MOLD_C.y, 0.38), e['dist'] * 1.32, -14, 24),
        (0.72, (MOLD_C.x, MOLD_C.y, 0.20), e['dist'] * 1.02, -20, 38),
        (0.86, (MOLD_C.x, MOLD_C.y - 0.05, 0.22), e['dist'] * 0.92, -10, 26),
        (1.00, (MOLD_C.x + 0.01, MOLD_C.y - MOLD_W / 2, 0.14), e['dist'] * 0.15, -3, 5),
    ]
    for (ta, A, da, ya, pa), (tb, B, db, yb, pb) in zip(keys, keys[1:]):
        if t <= tb:
            u = kit.smoother((t - ta) / (tb - ta))
            target = Vector(kit.vlerp(A, B, u))
            return sph(target, kit.lerp(da, db, u), kit.lerp(ya, yb, u), kit.lerp(pa, pb, u)), target
    return sph(keys[-1][1], keys[-1][2], keys[-1][3], keys[-1][4]), Vector(keys[-1][1])


def main():
    os.makedirs(ARGS.out, exist_ok=True)
    # Sahne 0 stüdyosunu aynen kur, sonra bu sahnenin nesnelerini ekle
    s0.ARGS = ARGS
    cam, blk, dust = s0.build(ARGS.variant)
    base = blk.data.materials[0]
    dmat, front = dissolve_material(base)
    blk.data.materials[0] = dmat
    blk.rotation_euler[2] = math.radians(6.0)  # Sahne 0 son karesiyle aynı

    g = grain_setup(N_GRAIN)
    grains = make_grain_object(g)
    peds = build_pedestals(base)
    steel = steel_material()
    mold = build_mold(steel)
    near = kit.aac_material('GazbetonYakin', bump=1.1)
    cake, skin = build_cake(near)
    wires = build_wires()

    env_mix = None  # Sahne 0 artık baştan yumuşak ortamla render ediliyor (süreklilik)
    frames = s0.pass_order(FRAMES) if ARGS.frames == 'all' else [int(x) for x in ARGS.frames.split(',')]
    meta_path = os.path.join(ARGS.out, 'meta.json')
    meta = {'frames': FRAMES, 'res': s0.VARIANTS[ARGS.variant]['res'], 'hotspots': {}}
    for f in frames:
        t = f / (FRAMES - 1)
        # Sahne 0 ile aynı başlar; sonra HDRI yansıması lekesiz yumuşak ortama devredilir
        if env_mix:
            env_mix.outputs[0].default_value = kit.smooth(kit.seg(t, 0.0, 0.14))
        # çözülme cephesi: yerel z (−H/2..H/2) üstten alta
        cz = H / 2 + 0.06 - kit.smooth(kit.seg(t, 0.03, 0.27)) * (H + 0.14)
        front.outputs[0].default_value = cz
        blk.hide_render = t > 0.28
        pos, sc = grain_state(g, t)
        # kaideler: hammaddeler ayrışırken zeminden yükselir, karışımdan sonra iner
        k_p = kit.smoother(kit.seg(t, 0.08, 0.22)) * (1 - kit.smoother(kit.seg(t, 0.56, 0.68)))
        for (px, py, ph), pob in zip(PEDESTALS, peds):
            pob.hide_render = k_p < 0.002
            pob.location.z = ph / 2 - ph * (1 - k_p) * 1.02
        update_grains(grains, pos, sc)

        # kalıp: girdap inerken görünür (zeminden yükselir)
        k_m = kit.smoother(kit.seg(t, 0.42, 0.54))
        k_open = kit.smoother(kit.seg(t, 0.88, 0.96))
        for name, p in mold.items():
            p.hide_render = k_m <= 0.001
            p.scale = (1, 1, max(0.001, k_m)) if name != 'taban' else (1, 1, 1)
            if name in ('on', 'sol', 'sag', 'arka'):
                p.location.z = (MOLD_H / 2) * k_m - MOLD_H * 1.02 * k_open
        # dolum + kabarma: seviye 0 → %45 (dolum) → %100 (kabarma, hafif taşma)
        fill = 0.45 * kit.smooth(kit.seg(t, 0.58, 0.68))
        rise = kit.ease_out(kit.seg(t, 0.68, 0.82), 3)
        level = MOLD_H * (fill + 0.55 * rise) + 0.010 * math.sin(kit.seg(t, 0.68, 0.86) * math.pi)
        show_cake = level > 0.004
        for i, b in enumerate(cake):
            b.hide_render = not show_cake
            b.scale = (1, 1, max(level, 0.001))
            b.location.z = max(level, 0.001) / 2
        skin.hide_render = not show_cake
        skin.location.z = level
        skin.scale = (1, 1, 0.2 + 0.8 * rise)
        # tel kesim: teller üstten alta iner; geçtikten sonra bloklar 3 mm ayrılır
        k_cut = kit.smooth(kit.seg(t, 0.80, 0.90))
        for w in wires:
            w.hide_render = not (0.79 < t < 0.92)
            w.location.z = MOLD_H + 0.06 - k_cut * (MOLD_H + 0.1)
        k_sep = kit.smoother(kit.seg(t, 0.88, 0.97))
        for i, b in enumerate(cake):
            off = (i - (CUT_N - 1) / 2) * 0.012 * k_sep
            b.location.x = MOLD_C.x - MOLD_L / 2 + (MOLD_L / CUT_N) * (i + 0.5) + off
        skin.hide_render = skin.hide_render or k_sep > 0.5  # kesim sonrası kubbe kesilip alınır

        loc, target = cam_pose(t, ARGS.variant)
        cam.location = loc
        kit.aim(cam, target)
        cam.data.dof.focus_distance = (Vector(target) - loc).length
        kit.move_dust(dust, 3.0 + t * 4.0)
        # tıklanır noktalar: hammadde bulutları (yalnız ayrışmış göründükleri aralıkta)
        if 0.20 <= t <= 0.44:
            ids = ['kum', 'kirec', 'cimento', 'alci', 'aluminyum']
            pts = [(px, py, ph + 0.17) for (px, py, ph) in PEDESTALS] + [ALU_CLOUD]
            proj = kit.project(cam, pts)
            meta['hotspots'][str(f)] = {i: p for i, p in zip(ids, proj) if p and 0.02 < p[0] < 0.98 and 0.04 < p[1] < 0.96}
        elif 0.70 <= t <= 0.84:
            proj = kit.project(cam, [(MOLD_C.x, MOLD_C.y, MOLD_H * 0.9)])
            meta['hotspots'][str(f)] = {'kabarma': proj[0]} if proj[0] else {}
        elif 0.80 < t <= 0.92:
            proj = kit.project(cam, [(MOLD_C.x + MOLD_L * 0.3, MOLD_C.y, MOLD_H * 0.6)])
            meta['hotspots'][str(f)] = {'kesim': proj[0]} if proj[0] else {}
        path = os.path.join(ARGS.out, f'{f:03d}.png')
        if ARGS.skip_existing and os.path.exists(path):
            continue
        t0 = time.time()
        kit.render_to(path)
        print(f'KARE {f} {time.time() - t0:.1f}s', flush=True)
        kit.write_json(meta_path, meta)
    kit.write_json(meta_path, meta)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--variant', default='d')
    ap.add_argument('--frames', default='all')
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=24)
    ap.add_argument('--skip-existing', action='store_true')
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
