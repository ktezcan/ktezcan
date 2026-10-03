"""
Stil G — gerçekçi mahalle (F'nin gerçekçi hâli).

Bina gerçek bir Ege mahallesinin içinde: asfalt yol, kaldırım taşı, bordür,
komşu evler (sıva + kiremit), ağaçlar, park etmiş arabalar, yayalar.
Malzemeler gerçek (gazbeton dokusu, cam yansıması, araba boyası), ışık
seçeneklidir. --cizim ile aynı kare "mimar çizimi" olarak çizilir (kâğıt +
grafit çizgi); çizim → gerçek geçişi bu iki geçişin silmeli karışımıdır.

Kullanım: python stil_g.py --out DIR [--isik altin|yumusak|mavi] [--cizim] [--u 0.78] [--ad ...]
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


def pbr(name, hexcol, rough=0.6, metal=0.0, coat=0.0, noise=0.0, nscale=4.0, bump=0.0):
    """Principled + isteğe bağlı renk/pürüz gürültüsü ve kabartı (gerçekçi kirlilik)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes.get('Principled BSDF')
    c = kit.srgb(hexcol)
    b.inputs['Base Color'].default_value = c
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if coat:
        b.inputs['Coat Weight'].default_value = coat
        b.inputs['Coat Roughness'].default_value = 0.05
    if noise or bump:
        tc = nt.nodes.new('ShaderNodeTexCoord')
        nz = nt.nodes.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = nscale
        nz.inputs['Detail'].default_value = 8.0
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        if noise:
            mix = nt.nodes.new('ShaderNodeMix')
            mix.data_type = 'RGBA'
            mix.blend_type = 'MULTIPLY'
            mix.inputs['Factor'].default_value = noise
            mix.inputs['A'].default_value = c
            nt.links.new(nz.outputs['Color'], mix.inputs['B'])
            nt.links.new(mix.outputs['Result'], b.inputs['Base Color'])
        if bump:
            bp = nt.nodes.new('ShaderNodeBump')
            bp.inputs['Strength'].default_value = bump
            bp.inputs['Distance'].default_value = 0.02
            nt.links.new(nz.outputs['Fac'], bp.inputs['Height'])
            nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m


def tugla(name, c1, c2, harc, olcek=2.2, rough=0.85):
    """Kaldırım taşı: Brick dokusu (nesne uzayı, üstten)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes.get('Principled BSDF')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    br = nt.nodes.new('ShaderNodeTexBrick')
    br.inputs['Color1'].default_value = kit.srgb(c1)
    br.inputs['Color2'].default_value = kit.srgb(c2)
    br.inputs['Mortar'].default_value = kit.srgb(harc)
    br.inputs['Scale'].default_value = olcek
    br.inputs['Mortar Size'].default_value = 0.012
    br.inputs['Brick Width'].default_value = 0.5
    br.inputs['Row Height'].default_value = 0.25
    nt.links.new(tc.outputs['Object'], br.inputs['Vector'])
    nt.links.new(br.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough
    bp = nt.nodes.new('ShaderNodeBump')
    bp.inputs['Strength'].default_value = 0.3
    bp.invert = True
    nt.links.new(br.outputs['Fac'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m


def kutu(name, size, loc, mat, rot=0.0, bev=0.0):
    ob = kit.box(name, size, loc, mat)
    if bev:
        kit.bevel(ob, width=bev, segments=2, angle=50)
    ob.rotation_euler[2] = rot
    return ob


class Mahalle:
    def __init__(self):
        self.m = dict(
            asfalt=pbr('GAsfalt', '#3b3c3e', 0.88, noise=0.35, nscale=9.0, bump=0.15),
            kaldirim=tugla('GKaldirim', '#bdb5a8', '#aaa294', '#8a8377'),
            bordur=pbr('GBordur', '#b2aea6', 0.8, noise=0.15, nscale=6.0),
            cizgi=pbr('GCizgi', '#e9e7df', 0.6),
            cim=pbr('GKuruOt', '#c2ad78', 0.95, noise=0.6, nscale=1.2, bump=0.4),
            sivalar=[pbr('GSiva1', '#ecdfc9', 0.9, noise=0.08, nscale=2.0), pbr('GSiva2', '#e2c7a3', 0.9, noise=0.08, nscale=2.0),
                     pbr('GSiva3', '#dcdfd9', 0.9, noise=0.08, nscale=2.0)],
            kiremit=pbr('GKiremit', '#b4552f', 0.7, noise=0.25, nscale=12.0, bump=0.3),
            pcam=pbr('GPencere', '#20282e', 0.06, metal=0.2),
            pisik=pbr('GPencereIsik', '#20282e', 0.06, metal=0.2),
            cerceve=pbr('GCerceve', '#f2f0ea', 0.5),
            govde=pbr('GAgacGovde', '#5b4835', 0.9),
            yaprak=[pbr('GYaprak1', '#6e7450', 0.75, noise=0.35, nscale=6.0), pbr('GYaprak2', '#7d7b52', 0.75, noise=0.35, nscale=6.0),
                    pbr('GYaprak3', '#8a8a62', 0.75, noise=0.35, nscale=6.0)],
            lastik=pbr('GLastik', '#1b1b1c', 0.8),
            otocam=pbr('GOtoCam', '#1d2328', 0.04),
            krom=pbr('GKrom', '#c9cccf', 0.2, metal=1.0),
        )
        self.boyalar = [pbr('GBoya1', '#9f2a22', 0.35, coat=1.0), pbr('GBoya2', '#e8e8e4', 0.35, coat=1.0),
                        pbr('GBoya3', '#24364f', 0.35, coat=1.0), pbr('GBoya4', '#8f9398', 0.3, metal=0.6, coat=1.0)]
        self.kiyafet = [pbr(f'GKiyafet{i}', h, 0.85) for i, h in enumerate(['#2f3e57', '#c9b79a', '#7a2f2a', '#3c3c3c', '#d8d2c4', '#5c6b7c'])]
        self.ten = pbr('GTen', '#c99a77', 0.6)
        self.rnd = random.Random(21)

    def zemin(self):
        m = self.m
        for ob in list(bpy.data.objects):
            if ob.name.startswith(('Tepe',)):
                bpy.data.objects.remove(ob, do_unlink=True)
        kutu('Ot', (400, 400, 0.1), (0, 60, -0.06), m['cim'])
        # yol (x boyunca), iki kaldırım, bordürler
        kutu('Asfalt', (400, 8.0, 0.1), (0, -13.5, -0.03), m['asfalt'])
        kutu('Kaldirim', (400, 2.8, 0.16), (0, -8.1, 0.02), m['kaldirim'])
        kutu('Kaldirim', (400, 3.0, 0.16), (0, -19.0, 0.02), m['kaldirim'])
        kutu('Bordur', (400, 0.2, 0.2), (0, -9.5, 0.04), m['bordur'])
        kutu('Bordur', (400, 0.2, 0.2), (0, -17.5, 0.04), m['bordur'])
        for i in range(-24, 25):
            kutu('YolCizgi', (2.6, 0.14, 0.02), (i * 6.0, -13.5, 0.025), m['cizgi'])
        # yaya geçidi
        for j in range(7):
            kutu('Zebra', (0.5, 6.4, 0.02), (14.0 + j * 0.9, -13.5, 0.026), m['cizgi'])

    def ev(self, x, y, w, d, kat, sv, rot=0.0):
        m = self.m
        h = kat * 3.0
        kutu('Ev', (w, d, h), (x, y, h / 2), sv, rot, bev=0.04)
        # kırma çatı: piramit
        ust = h + 0.02
        r = 0.45
        verts = [(x - w / 2 - r, y - d / 2 - r, ust), (x + w / 2 + r, y - d / 2 - r, ust), (x + w / 2 + r, y + d / 2 + r, ust),
                 (x - w / 2 - r, y + d / 2 + r, ust), (x - max(0, (w - d) / 2) * 1.0, y, ust + min(w, d) * 0.32),
                 (x + max(0, (w - d) / 2), y, ust + min(w, d) * 0.32)]
        faces = [(0, 1, 5, 4), (1, 2, 5), (2, 3, 4, 5), (3, 0, 4), (0, 3, 2, 1)]
        kit.mesh_object('Cati', verts, faces, m['kiremit'])
        # pencereler (ön ve yan cepheler)
        for k in range(kat):
            zc = k * 3.0 + 1.6
            n = max(2, int(w / 2.6))
            for i in range(n):
                xc = x - w / 2 + (i + 0.5) * w / n
                kutu('EvCerceve', (1.24, 0.08, 1.44), (xc, y - d / 2 - 0.02, zc), m['cerceve'])
                kutu('EvPencere', (1.1, 0.1, 1.3), (xc, y - d / 2 - 0.03, zc), m['pisik'] if self.rnd.random() < 0.55 else m['pcam'])
            nn = max(2, int(d / 2.6))
            for i in range(nn):
                yc = y - d / 2 + (i + 0.5) * d / nn
                for sx in (-1, 1):
                    kutu('EvCerceve', (0.08, 1.24, 1.44), (x + sx * (w / 2 + 0.02), yc, zc), m['cerceve'])
                    kutu('EvPencere', (0.1, 1.1, 1.3), (x + sx * (w / 2 + 0.03), yc, zc), m['pisik'] if self.rnd.random() < 0.55 else m['pcam'])

    def agac(self, x, y, boy):
        m, rnd = self.m, self.rnd
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.14 * boy / 6, depth=boy * 0.55, location=(x, y, boy * 0.275))
        bpy.context.active_object.data.materials.append(m['govde'])
        tex = bpy.data.textures.get('GYaprakTex') or bpy.data.textures.new('GYaprakTex', 'CLOUDS')
        tex.noise_scale = 0.35
        yap = rnd.choice(m['yaprak'])
        for _ in range(5):
            r = boy * rnd.uniform(0.16, 0.24)
            p = (x + rnd.uniform(-0.25, 0.25) * boy * 0.3, y + rnd.uniform(-0.25, 0.25) * boy * 0.3, boy * rnd.uniform(0.6, 0.82))
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=r, location=p)
            ob = bpy.context.active_object
            ob.name = 'Yaprak'
            dm = ob.modifiers.new('Dis', 'DISPLACE')
            dm.texture = tex
            dm.strength = r * 0.45
            dm.texture_coords = 'GLOBAL'
            ob.data.materials.append(yap)
            bpy.ops.object.shade_smooth()

    def araba(self, x, y, yon, boya):
        m = self.m
        c, s_ = math.cos(yon), math.sin(yon)

        def yer(dx, dy, z):
            return (x + dx * c - dy * s_, y + dx * s_ + dy * c, z)
        kutu('Araba', (4.3, 1.8, 0.72), yer(0, 0, 0.62), boya, yon, bev=0.18)
        kutu('ArabaKabin', (2.3, 1.62, 0.58), yer(-0.25, 0, 1.22), m['otocam'], yon, bev=0.16)
        kutu('ArabaTampon', (0.08, 1.7, 0.18), yer(2.17, 0, 0.42), m['krom'], yon)
        for dx in (-1.38, 1.38):
            for dy in (-0.84, 0.84):
                bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.34, depth=0.24, location=yer(dx, dy, 0.34), rotation=(math.pi / 2, 0, yon))
                bpy.context.active_object.data.materials.append(m['lastik'])

    def insan(self, x, y, boy=1.72, yon=0.0):
        rnd = self.rnd
        k = boy / 1.75
        ust, alt = rnd.sample(self.kiyafet, 2)
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.17 * k, depth=0.82 * k, location=(x, y, 0.41 * k + 0.1))
        bpy.context.active_object.data.materials.append(alt)
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.21 * k, depth=0.6 * k, location=(x, y, 1.12 * k + 0.1))
        bpy.context.active_object.data.materials.append(ust)
        bpy.ops.object.shade_smooth()
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=10, radius=0.115 * k, location=(x, y, 1.58 * k + 0.1))
        bpy.context.active_object.data.materials.append(self.ten)
        bpy.ops.object.shade_smooth()

    def kur(self):
        self.zemin()
        sv = self.m['sivalar']
        # komşu evler: binanın iki yanında ve arkasında
        self.ev(-24.0, 0.0, 9.0, 8.0, 2, sv[0])
        self.ev(23.0, -1.0, 8.0, 9.0, 3, sv[1])
        self.ev(-6.0, 22.0, 11.0, 8.0, 2, sv[2])
        self.ev(12.0, 21.0, 8.0, 8.0, 2, sv[0])
        self.ev(-26.0, 20.0, 8.0, 8.0, 3, sv[1])
        self.ev(-34.0, -28.0, 10.0, 8.0, 2, sv[2])
        # kaldırım ağaçları
        for xx in (-30, -19, -14.5, 9.5, 17, 30):
            self.agac(xx, -8.4, self.rnd.uniform(5.5, 7.0))
        for xx in (-25, -6, 4, 21):
            self.agac(xx, -19.3, self.rnd.uniform(5.0, 6.5))
        for p in ((-17, 9), (17.5, 10), (-31, 8), (4, 14)):
            self.agac(*p, self.rnd.uniform(6.0, 8.0))
        # arabalar
        b = self.boyalar
        self.araba(-22.0, -10.7, 0.0, b[0])
        self.araba(-4.0, -10.7, 0.0, b[1])
        self.araba(26.0, -10.7, 0.0, b[3])
        self.araba(6.0, -15.6, math.pi, b[2])
        # yayalar
        for (x, y) in ((-9.0, -8.3), (-8.4, -7.9), (8.0, -19.0), (19.0, -8.0), (2.0, -7.6)):
            self.insan(x, y, self.rnd.uniform(1.6, 1.85))
        self.insan(-7.8, -8.1, 1.1)


def isik(sc, dusk, tur, u):
    import s3_bina as s
    sun = dusk['sun']
    sky = dusk['world'].node_tree.nodes['Sky Texture']
    bg = [n for n in dusk['world'].node_tree.nodes if n.type == 'BACKGROUND'][0]
    if tur == 'altin':  # altın saat: alçak sıcak güneş, uzun gölge
        sun.data.energy = 4.6
        sun.data.angle = math.radians(1.0)
        sun.data.color = (1.0, 0.7, 0.45)
        sun.rotation_euler = (math.radians(78), 0, math.radians(-50))
        sky.sun_elevation = math.radians(10)
        sky.sun_rotation = math.radians(220)
        bg.inputs['Strength'].default_value = 0.22
        sc.view_settings.exposure = -0.45
    elif tur == 'yumusak':  # bulutlu öğle: maket fotoğrafı gibi yumuşak, gölgeler hafif
        sun.data.energy = 2.2
        sun.data.angle = math.radians(18)
        sun.data.color = (1.0, 0.97, 0.94)
        sun.rotation_euler = (math.radians(38), 0, math.radians(-30))
        sky.sun_elevation = math.radians(50)
        bg.inputs['Strength'].default_value = 0.42
        sc.view_settings.exposure = -0.55
    if tur != 'mavi':
        r = bpy.data.objects.get('SahaHalka')
        if r:
            r.hide_render = True
    if tur == 'mavi':  # mavi saat: güneş batmış, pencereler ve lambalar yanar
        s.alacakaranlik(dusk, 0.97)
        sc.view_settings.exposure += 1.0
        pi = bpy.data.materials['GPencereIsik'].node_tree.nodes['Principled BSDF']
        pi.inputs['Emission Color'].default_value = (1.0, 0.7, 0.4, 1.0)
        pi.inputs['Emission Strength'].default_value = 3.0


def cizim_yap(sc):
    """Mimar çizimi: her şey kâğıt beyazı, gölge yok, grafit kontur."""
    kagit = bpy.data.materials.new('GKagit')
    kagit.use_nodes = True
    nt = kagit.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = kit.srgb('#f6f3ec')
    em.inputs['Strength'].default_value = 1.0
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(em.outputs[0], out.inputs['Surface'])
    for ob in bpy.data.objects:
        if ob.type == 'MESH':
            ob.data.materials.clear() if ob.data.users == 1 else None
            if len(ob.material_slots) == 0:
                ob.data.materials.append(kagit)
            for sl in ob.material_slots:
                sl.material = kagit
            if ob.name.startswith(('Sis', 'SahaHalka', 'Toz', 'Siluet', 'Govde', 'Bacak', 'Ot')):
                ob.hide_render = True
        if ob.type == 'LIGHT':
            ob.hide_render = True
    w = bpy.data.worlds.new('Kagit')
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (*kit.srgb('#f6f3ec')[:3], 1)
    sc.view_settings.view_transform = 'Standard'
    sc.view_settings.look = 'None'
    sc.view_settings.exposure = 0.0
    sc.render.use_freestyle = True
    sc.render.line_thickness_mode = 'ABSOLUTE'
    vl = sc.view_layers[0]
    vl.use_freestyle = True
    fs = vl.freestyle_settings
    fs.crease_angle = math.radians(135)
    ls = fs.linesets[0] if len(fs.linesets) else fs.linesets.new('Cizgi')
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new('Grafit')
    ls.select_silhouette = ls.select_border = ls.select_crease = True
    ls.linestyle.color = (0.16, 0.19, 0.22)
    ls.linestyle.thickness = 1.1
    sc.compositing_node_group = None


def main():
    import s3_bina as s
    s.ARGS = argparse.Namespace(samples=ARGS.samples)
    cam, objs, wall_mats, dusk = s.build('d')
    t = s.yapim_t(ARGS.u)
    for mat in wall_mats.values():
        for n in mat.node_tree.nodes:
            if n.type == 'MATH' and n.operation == 'SUBTRACT' and not n.inputs[0].is_linked and abs(n.inputs[1].default_value - s.T_WALL0) < 1e-6:
                n.inputs[0].default_value = t
    s.apply_state(objs, t)
    sc = bpy.context.scene
    # şantiye zemini yalnız arsada kalsın
    z = bpy.data.objects.get('Zemin')
    if z:
        z.scale = (30.0 / 600, 19.0 / 600, 1.0)
        z.location = (0.0, 3.0, -0.08)
    Mahalle().kur()
    for ob in bpy.data.objects:
        if ob.name.startswith('Sis'):
            bpy.data.objects.remove(ob, do_unlink=True)
    isik(sc, dusk, ARGS.isik, ARGS.u)
    if ARGS.cizim:
        cizim_yap(sc)
    # kamera: yüksek 3/4 bakış, hafif tele (maket fotoğrafı hissi)
    target = Vector((-1.0, -3.0, 4.0))
    cam.location = target + Vector((0.62, -1.0, 0.62)).normalized() * 64
    kit.aim(cam, target)
    cam.data.lens = 42
    cam.data.shift_x = cam.data.shift_y = 0.0
    cam.data.dof.use_dof = not ARGS.cizim
    cam.data.dof.focus_distance = 64
    cam.data.dof.aperture_fstop = 5.6
    cam.data.clip_end = 2000
    sc.render.resolution_x, sc.render.resolution_y = 1280, 720
    os.makedirs(ARGS.out, exist_ok=True)
    kit.render_to(os.path.join(ARGS.out, f'{ARGS.ad}.png'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--u', type=float, default=0.78)
    ap.add_argument('--isik', default='altin')
    ap.add_argument('--cizim', action='store_true')
    ap.add_argument('--ad', default='bina_G')
    ap.add_argument('--samples', type=int, default=64)
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
