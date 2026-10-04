"""
Ege Gazbeton — giriş hikâyesi Blender sahne kiti (Cycles, tamamen kod).

Ortak parçalar: render ayarları, gazbeton malzemesi, koyu parlak stüdyo,
"kontur + zayıf hale" ışığı, toz, kamera yardımcıları ve her kare için
ekran izdüşümü (tıklanır nokta / video köşeleri) dışa aktarımı.

Kurallar (Kutay'ın kararları):
  • Yapay zekâ görseli yok — her şey prosedürel.
  • Spot ışık yok → ürün çevresinde kontur + zayıf hale (lime halka).
  • Yeşil (lime) yalnız bizim ürüne / marka ışığına.
  • 3B görüntüde yazı ve rakam yok (çeviri kartlarda).
  • Hareket bulanıklığı kapalı; sinema rengi AgX Medium High Contrast.
"""
import math
import os
import json

import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

# Marka renkleri (sRGB hex → lineer)
def srgb(hexstr, k=1.0):
    h = hexstr.lstrip('#')
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255.0
        out.append((c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4) * k)
    return (*out, 1.0)


LIME = srgb('#a2bf37')
LIME_HI = srgb('#b8d54a')
NIGHT = srgb('#0c161c')
SLATE = srgb('#314551')
# Hammaddeler (sitedeki 3B ile aynı)
SAND = srgb('#d8c49b')
LIMEWASH = srgb('#f4f2ec')
CEMENT = srgb('#9ea3a4')
GYPSUM = srgb('#e2d8cf')
WATER = srgb('#5aaad8')
ALU = srgb('#e7eef3')

DATAFILES = bpy.utils.system_resource('DATAFILES')


# ---------------------------------------------------------------------------
#  Sahne ve render
# ---------------------------------------------------------------------------
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras, bpy.data.images):
        for b in list(coll):
            if b.users == 0:
                coll.remove(b)


def setup_render(w, h, samples=48, threshold=0.02, bounces=(4, 2, 2, 2), clamp=3.0):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    cy = sc.cycles
    cy.device = 'CPU'
    cy.samples = samples
    cy.use_adaptive_sampling = True
    cy.adaptive_threshold = threshold
    cy.adaptive_min_samples = 0
    cy.use_denoising = True
    cy.denoiser = 'OPENIMAGEDENOISE'
    cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
    cy.denoising_prefilter = 'ACCURATE'
    cy.max_bounces, cy.diffuse_bounces, cy.glossy_bounces, cy.transmission_bounces = bounces[0], bounces[1], bounces[2], bounces[3]
    cy.transparent_max_bounces = 8
    cy.volume_bounces = 0
    cy.caustics_reflective = False
    cy.caustics_refractive = False
    cy.blur_glossy = 0.6
    cy.sample_clamp_indirect = clamp
    cy.use_light_tree = True
    sc.render.use_persistent_data = True  # dizide BVH yeniden kurulmaz
    sc.render.resolution_x = w
    sc.render.resolution_y = h
    sc.render.resolution_percentage = int(os.environ.get('EGE_PREVIEW', '100'))
    if os.environ.get('EGE_PREVIEW'):
        cy.samples = min(cy.samples, 8)
    sc.render.use_motion_blur = False
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGB'
    sc.render.image_settings.color_depth = '8'
    sc.render.image_settings.compression = 15
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.look = 'AgX - Medium High Contrast'
    sc.view_settings.exposure = 0.0
    sc.view_settings.gamma = 1.0
    sc.render.threads_mode = 'AUTO'
    return sc


def render_to(path):
    sc = bpy.context.scene
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)


# ---------------------------------------------------------------------------
#  Düğüm yardımcıları
# ---------------------------------------------------------------------------
class NT:
    """Kısa düğüm ağacı kurucu."""

    def __init__(self, tree):
        self.t = tree
        self.n = tree.nodes
        self.l = tree.links

    def node(self, kind, loc=(0, 0), **props):
        nd = self.n.new(kind)
        nd.location = loc
        for k, v in props.items():
            setattr(nd, k, v)
        return nd

    def link(self, a, b):
        self.l.new(a, b)

    def math(self, op, a=None, b=None, loc=(0, 0), clamp=False):
        m = self.node('ShaderNodeMath', loc, operation=op, use_clamp=clamp)
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                m.inputs[i].default_value = v
            else:
                self.link(v, m.inputs[i])
        return m.outputs[0]


TEX_DIR = os.environ.get('EGE_TEX', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tex'))


def aac_material(name='Gazbeton', rough=0.9, bump=0.55, tex_size=0.24, tint=None, blend=0.18):
    """
    Gazbeton yüzeyi: dokular.py'nin ürettiği döşenebilir renk + yükseklik
    dokusu, nesne uzayında kutu izdüşümüyle (UV gerekmez, ölçek metre).
    Prosedürel Voronoi'ye göre ~10× hızlı render.
    Not: Gerçek kesit fotoğrafı (cut-surface.jpg) gelince renk dokusu onunla değiştirilmelidir.
    """
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = NT(mat.node_tree)
    nt.n.clear()
    out = nt.node('ShaderNodeOutputMaterial', (900, 0))
    bsdf = nt.node('ShaderNodeBsdfPrincipled', (600, 0))
    nt.link(bsdf.outputs[0], out.inputs['Surface'])
    tc = nt.node('ShaderNodeTexCoord', (-900, 0))
    mp = nt.node('ShaderNodeMapping', (-700, 0))
    s = 1.0 / tex_size
    mp.inputs['Scale'].default_value = (s, s, s)
    nt.link(tc.outputs['Object'], mp.inputs['Vector'])

    def img(file, colorspace, loc):
        node = nt.node('ShaderNodeTexImage', loc)
        node.image = bpy.data.images.load(os.path.join(TEX_DIR, file), check_existing=True)
        node.image.colorspace_settings.name = colorspace
        node.projection = 'BOX'
        node.projection_blend = blend
        node.interpolation = 'Linear'
        nt.link(mp.outputs['Vector'], node.inputs['Vector'])
        return node

    col = img('gazbeton_renk.png', 'sRGB', (-400, 200))
    hgt = img('gazbeton_yukseklik.png', 'Non-Color', (-400, -200))
    if tint is not None:
        mix = nt.node('ShaderNodeMix', (200, 250), data_type='RGBA', blend_type='MULTIPLY')
        mix.inputs['Factor'].default_value = 1.0
        nt.link(col.outputs['Color'], mix.inputs['A'])
        mix.inputs['B'].default_value = tint
        nt.link(mix.outputs['Result'], bsdf.inputs['Base Color'])
    else:
        nt.link(col.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Specular IOR Level'].default_value = 0.3
    rng = 0.002
    try:
        lo, hi, _ = open(os.path.join(TEX_DIR, 'gazbeton_yukseklik.txt')).read().split()
        rng = float(hi) - float(lo)
    except OSError:
        pass
    bmp = nt.node('ShaderNodeBump', (300, -200))
    bmp.inputs['Strength'].default_value = bump
    bmp.inputs['Distance'].default_value = rng
    nt.link(hgt.outputs['Color'], bmp.inputs['Height'])
    nt.link(bmp.outputs['Normal'], bsdf.inputs['Normal'])
    return mat


def glossy_floor(name='Zemin', color='#070a0c', rough=0.16):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = NT(mat.node_tree)
    bsdf = nt.n.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = srgb(color)
    bsdf.inputs['Specular IOR Level'].default_value = 0.55
    tc = nt.node('ShaderNodeTexCoord', (-900, 0))
    noise = nt.node('ShaderNodeTexNoise', (-650, 0))
    noise.inputs['Scale'].default_value = 1.2
    noise.inputs['Detail'].default_value = 3.0
    nt.link(tc.outputs['Object'], noise.inputs['Vector'])
    mr = nt.node('ShaderNodeMapRange', (-400, 0))
    nt.link(noise.outputs['Fac'], mr.inputs['Value'])
    mr.inputs['From Min'].default_value = 0.35
    mr.inputs['From Max'].default_value = 0.65
    mr.inputs['To Min'].default_value = rough * 0.85
    mr.inputs['To Max'].default_value = rough * 1.2
    nt.link(mr.outputs['Result'], bsdf.inputs['Roughness'])
    return mat


def emission_material(name, color, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = NT(mat.node_tree)
    nt.n.clear()
    out = nt.node('ShaderNodeOutputMaterial', (300, 0))
    em = nt.node('ShaderNodeEmission', (0, 0))
    em.inputs['Color'].default_value = color
    em.inputs['Strength'].default_value = strength
    nt.link(em.outputs[0], out.inputs['Surface'])
    return mat


def studio_world(bg_top='#0c161c', bg_bottom='#030506', hdri='studio.exr', hdri_strength=0.35, rot=0.0):
    """Kamera koyu degrade görür; yansımalar stüdyo HDRI'sinden gelir."""
    world = bpy.data.worlds.new('Studyo')
    bpy.context.scene.world = world
    world.use_nodes = True
    nt = NT(world.node_tree)
    nt.n.clear()
    out = nt.node('ShaderNodeOutputWorld', (900, 0))
    lp = nt.node('ShaderNodeLightPath', (0, 300))
    mix = nt.node('ShaderNodeMixShader', (700, 0))
    nt.link(lp.outputs['Is Camera Ray'], mix.inputs[0])

    # yansıma/aydınlatma: HDRI
    tc = nt.node('ShaderNodeTexCoord', (-700, -200))
    mp = nt.node('ShaderNodeMapping', (-500, -200))
    mp.inputs['Rotation'].default_value[2] = rot
    nt.link(tc.outputs['Generated'], mp.inputs['Vector'])
    env = nt.node('ShaderNodeTexEnvironment', (-250, -200))
    path = os.path.join(DATAFILES, 'studiolights', 'world', hdri)
    env.image = bpy.data.images.load(path, check_existing=True)
    nt.link(mp.outputs['Vector'], env.inputs['Vector'])
    bg1 = nt.node('ShaderNodeBackground', (300, -150))
    nt.link(env.outputs['Color'], bg1.inputs['Color'])
    bg1.inputs['Strength'].default_value = hdri_strength
    nt.link(bg1.outputs[0], mix.inputs[1])

    # kameranın gördüğü: dikey degrade (ekran uzayı)
    tc2 = nt.node('ShaderNodeTexCoord', (-500, 300))
    sep = nt.node('ShaderNodeSeparateXYZ', (-300, 300))
    nt.link(tc2.outputs['Window'], sep.inputs[0])
    ramp = nt.node('ShaderNodeValToRGB', (-100, 300))
    ramp.color_ramp.elements[0].color = srgb(bg_bottom)
    ramp.color_ramp.elements[1].color = srgb(bg_top)
    ramp.color_ramp.interpolation = 'EASE'
    nt.link(sep.outputs['Y'], ramp.inputs['Fac'])
    bg2 = nt.node('ShaderNodeBackground', (300, 150))
    nt.link(ramp.outputs['Color'], bg2.inputs['Color'])
    bg2.inputs['Strength'].default_value = 1.0
    nt.link(bg2.outputs[0], mix.inputs[2])
    nt.link(mix.outputs[0], out.inputs['Surface'])
    return world


def soft_env_node(nt, loc=(0, -500), top=(0.55, 0.62, 0.70), horizon=(0.004, 0.006, 0.008), strength=0.6):
    """HDRI yerine yumuşak, lekesiz ortam: tepe hafif aydınlık, ufuk karanlık (zeminde parlak leke yapmaz)."""
    x, y = loc
    tc = nt.node('ShaderNodeTexCoord', (x - 600, y))
    sep = nt.node('ShaderNodeSeparateXYZ', (x - 400, y))
    nt.link(tc.outputs['Generated'], sep.inputs[0])
    # Generated (dünya) = yön vektörü: z yukarı
    mr = nt.node('ShaderNodeMapRange', (x - 200, y), interpolation_type='SMOOTHSTEP')
    nt.link(sep.outputs['Z'], mr.inputs['Value'])
    mr.inputs['From Min'].default_value = 0.0
    mr.inputs['From Max'].default_value = 0.9
    mix = nt.node('ShaderNodeMix', (x, y), data_type='RGBA')
    nt.link(mr.outputs['Result'], mix.inputs['Factor'])
    mix.inputs['A'].default_value = (*horizon, 1)
    mix.inputs['B'].default_value = (*top, 1)
    bg = nt.node('ShaderNodeBackground', (x + 200, y))
    nt.link(mix.outputs['Result'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = strength
    return bg


def replace_reflection_env(world, fac_value=0.0):
    """Var olan stüdyo dünyasında HDRI yansımasını yumuşak ortamla karıştırır; dönen 'Value' ile canlandırılır."""
    nt = NT(world.node_tree)
    mix_cam = [n for n in nt.n if n.type == 'MIX_SHADER'][0]
    hdri_bg = mix_cam.inputs[1].links[0].from_node
    soft = soft_env_node(nt)
    mx = nt.node('ShaderNodeMixShader', (500, -300))
    val = nt.node('ShaderNodeValue', (300, -100))
    val.outputs[0].default_value = fac_value
    nt.link(val.outputs[0], mx.inputs[0])
    nt.link(hdri_bg.outputs[0], mx.inputs[1])
    nt.link(soft.outputs[0], mx.inputs[2])
    nt.link(mx.outputs[0], mix_cam.inputs[1])
    return val


# ---------------------------------------------------------------------------
#  Nesneler
# ---------------------------------------------------------------------------
def link(obj):
    bpy.context.scene.collection.objects.link(obj)
    return obj


def mesh_object(name, verts, faces, mat=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    if mat:
        ob.data.materials.append(mat)
    return link(ob)


def box(name, size, loc=(0, 0, 0), mat=None):
    sx, sy, sz = (s / 2 for s in size)
    v = [(-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
         (-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    ob = mesh_object(name, v, f, mat)
    ob.location = loc
    return ob


def prism_x(name, profile_yz, x0, x1, mat=None):
    """YZ düzleminde kapalı profil, X boyunca uzatılır (dil / yuva için)."""
    n = len(profile_yz)
    v = [(x0, y, z) for (y, z) in profile_yz] + [(x1, y, z) for (y, z) in profile_yz]
    f = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        f.append((i, j, n + j, n + i))
    return mesh_object(name, v, f, mat)


def prism_z(name, profile_xy, z0, z1, mat=None):
    """XY düzleminde kapalı profil, Z boyunca uzatılır."""
    n = len(profile_xy)
    v = [(x, y, z0) for (x, y) in profile_xy] + [(x, y, z1) for (x, y) in profile_xy]
    f = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        f.append((i, j, n + j, n + i))
    return mesh_object(name, v, f, mat)


def apply_modifiers(ob):
    bpy.context.view_layer.objects.active = ob
    for m in list(ob.modifiers):
        bpy.ops.object.modifier_apply(modifier=m.name)


def boolean(ob, cutter, op='DIFFERENCE'):
    m = ob.modifiers.new('bool', 'BOOLEAN')
    m.operation = op
    m.solver = 'EXACT'
    m.object = cutter
    apply_modifiers(ob)
    bpy.data.objects.remove(cutter, do_unlink=True)


def bevel(ob, width=0.0025, segments=3, angle=40):
    m = ob.modifiers.new('bevel', 'BEVEL')
    m.width = width
    m.segments = segments
    m.limit_method = 'ANGLE'
    m.angle_limit = math.radians(angle)
    m.harden_normals = False
    apply_modifiers(ob)
    # pah yüzleri yumuşak, düz yüzler keskin: açıya göre yumuşatma
    bpy.ops.object.select_all(action='DESELECT')
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))


def gecmeli_blok(name='Blok', L=0.60, H=0.25, T=0.25, mat=None, tongues=True, grip=True):
    """
    Geçmeli duvar bloğu: ön yüz L×H (60×25 cm), kalınlık T.
    +X ucunda iki dikey yamuk dil, −X ucunda eş yuvalar; üstte tutma cebi yok
    (sitedeki kesim görseline göre). Ölçüler metre.
    Yerel eksen: X uzunluk, Y kalınlık (ön yüz −Y), Z yükseklik; taban z = 0.
    """
    body = box(name, (L, T, H), (0, 0, H / 2), mat)
    if tongues:
        d = 0.016  # dil çıkıntısı
        wb, wt = 0.034, 0.022  # yamuk taban / uç genişliği
        for yc in (-T * 0.24, T * 0.24):
            prof = [(L / 2 - 0.001, yc - wb / 2), (L / 2 + d, yc - wt / 2), (L / 2 + d, yc + wt / 2), (L / 2 - 0.001, yc + wb / 2)]
            t = prism_z(name + '_dil', prof, 0.0, H, mat)
            boolean(body, t, 'UNION')
            prof2 = [(-L / 2 - 0.01, yc - (wb + 0.004) / 2), (-L / 2 + d + 0.002, yc - (wt + 0.004) / 2),
                     (-L / 2 + d + 0.002, yc + (wt + 0.004) / 2), (-L / 2 - 0.01, yc + (wb + 0.004) / 2)]
            g = prism_z(name + '_yuva', prof2, -0.01, H + 0.01, None)
            boolean(body, g, 'DIFFERENCE')
    if grip:
        # uçlarda el tutma cepleri (yarım silindir oyuklar)
        pass
    bevel(body, 0.003, 3)
    body.data.materials.clear()
    if mat:
        body.data.materials.append(mat)
    return body


def halo_ring(name='Hale', radius=0.62, width=0.004, color=LIME, strength=9.0, segments=192, z=0.0015):
    """Zeminde ürün çevresinde ince ışık halkası (videolardaki lime döner tabla halkası)."""
    v, f = [], []
    r0, r1 = radius - width / 2, radius + width / 2
    for i in range(segments):
        a = 2 * math.pi * i / segments
        c, s = math.cos(a), math.sin(a)
        v += [(r0 * c, r0 * s, z), (r1 * c, r1 * s, z)]
    for i in range(segments):
        j = (i + 1) % segments
        f.append((2 * i, 2 * j, 2 * j + 1, 2 * i + 1))
    ob = mesh_object(name, v, f, emission_material(name + '_m', color, strength))
    ob.visible_shadow = False
    return ob


def area_light(name, loc, rot, size, energy, color=(1, 1, 1), shape='RECTANGLE', spread=180):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.shape = shape
    if isinstance(size, (tuple, list)):
        ld.size, ld.size_y = size
    else:
        ld.size = size
        ld.size_y = size
    ld.energy = energy
    ld.color = color[:3]
    ld.spread = math.radians(spread)
    ob = bpy.data.objects.new(name, ld)
    ob.location = loc
    ob.rotation_euler = rot
    ob.visible_camera = False
    return link(ob)


def aim(ob, target):
    d = Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def camera(name='Kamera', lens=50, sensor=36, loc=(0, -3, 1), target=(0, 0, 0), fstop=None, focus=None):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_width = sensor
    cd.sensor_fit = 'HORIZONTAL'
    cd.clip_start = 0.005
    cd.clip_end = 400
    ob = bpy.data.objects.new(name, cd)
    link(ob)
    ob.location = loc
    aim(ob, target)
    if fstop:
        cd.dof.use_dof = True
        cd.dof.aperture_fstop = fstop
        cd.dof.focus_distance = focus if focus else (Vector(target) - Vector(loc)).length
    bpy.context.scene.camera = ob
    return ob


# Tek akış düzeni: anlatım alanı masaüstünde solda (~%36), telefonda üstte (~%40).
# Konu, objektif kaydırmasıyla (perspektif değişmez) boş alanın karşısına alınır.
KAYMA = {'d': (-0.17, 0.0), 'm': (0.0, 0.16)}


def kaydir(cam, variant, k=1.0):
    """Kamera objektif kaydırması; k: 0 (ortada) … 1 (tam kayık), kare kare canlandırılabilir."""
    sx, sy = KAYMA.get(variant, (0.0, 0.0))
    cam.data.shift_x = sx * k
    cam.data.shift_y = sy * k


def dust(name='Toz', count=260, bounds=((-2, 2), (-1.5, 2.5), (0.05, 1.8)), seed=3, size=(0.0012, 0.0035), strength=1.4):
    """Işıkta asılı ince toz (her kare yeniden konumlanır: move_dust)."""
    import random
    rnd = random.Random(seed)
    mat = bpy.data.materials.new(name + '_m')
    mat.use_nodes = True
    nt = NT(mat.node_tree)
    nt.n.clear()
    out = nt.node('ShaderNodeOutputMaterial', (400, 0))
    mix = nt.node('ShaderNodeAddShader', (200, 0))
    em = nt.node('ShaderNodeEmission', (0, 100))
    em.inputs['Color'].default_value = (1.0, 0.97, 0.92, 1)
    em.inputs['Strength'].default_value = strength
    tr = nt.node('ShaderNodeBsdfTransparent', (0, -100))
    nt.link(em.outputs[0], mix.inputs[0])
    nt.link(tr.outputs[0], mix.inputs[1])
    nt.link(mix.outputs[0], out.inputs['Surface'])
    obs = []
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0)
    proto = bpy.context.active_object
    proto.name = name + '_proto'
    proto.data.materials.append(mat)
    me = proto.data
    bpy.data.objects.remove(proto, do_unlink=True)
    for i in range(count):
        ob = bpy.data.objects.new(f'{name}_{i}', me)
        r = rnd.uniform(*size)
        ob.scale = (r, r, r)
        p = [rnd.uniform(*b) for b in bounds]
        ob['base'] = p
        ob['phase'] = rnd.random() * 6.283
        ob['spd'] = rnd.uniform(0.2, 0.6)
        ob.location = p
        ob.visible_shadow = False
        obs.append(link(ob))
    return obs


def move_dust(obs, t):
    for ob in obs:
        bx, by, bz = ob['base']
        ph, sp = ob['phase'], ob['spd']
        ob.location = (bx + 0.08 * math.sin(t * sp + ph), by + 0.06 * math.cos(t * sp * 0.7 + ph), bz + 0.05 * math.sin(t * sp * 1.3 + ph * 2) + t * 0.01)


# ---------------------------------------------------------------------------
#  İzdüşüm: tıklanır noktalar, video köşeleri
# ---------------------------------------------------------------------------
def project(cam, points):
    """Dünya noktaları → ekran (sol üst köşe 0,0; sağ alt 1,1). Kamera arkasında ise None."""
    sc = bpy.context.scene
    bpy.context.view_layer.update()
    out = []
    for p in points:
        v = world_to_camera_view(sc, cam, Vector(p))
        out.append(None if v.z <= 0 else [round(v.x, 5), round(1 - v.y, 5)])
    return out


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))


# ---------------------------------------------------------------------------
#  Zamanlama yardımcıları
# ---------------------------------------------------------------------------
def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def smooth(x):
    x = clamp01(x)
    return x * x * (3 - 2 * x)


def smoother(x):
    x = clamp01(x)
    return x * x * x * (x * (x * 6 - 15) + 10)


def ease_out(x, p=3):
    return 1 - (1 - clamp01(x)) ** p


def ease_in_out(x):
    x = clamp01(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def seg(t, a, b):
    """t'nin [a, b] aralığındaki yerel ilerlemesi (0..1)."""
    return clamp01((t - a) / (b - a)) if b > a else float(t >= b)


def lerp(a, b, t):
    return a + (b - a) * t


def vlerp(a, b, t):
    return tuple(lerp(x, y, t) for x, y in zip(a, b))


# ---------------------------------------------------------------------------
#  Sinematik bitiş: parlama (bloom), hafif kenar kararması; hacimli ışık (sis)
# ---------------------------------------------------------------------------
def sinematik(bloom=0.55, esik=0.9, boyut=0.55, vinyet=0.0):
    """Kompozitör: ışık kaynakları (lime halka, yanan pencereler, yaylar) hafifçe ışıldar;
    kenarlar çok az kararır. Blender 5 kompozitör düğüm grubu."""
    sc = bpy.context.scene
    ng = bpy.data.node_groups.new('Sinematik', 'CompositorNodeTree')
    ng.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')
    sc.compositing_node_group = ng
    n, ln = ng.nodes, ng.links
    rl = n.new('CompositorNodeRLayers')
    gl = n.new('CompositorNodeGlare')
    gl.inputs['Type'].default_value = 'Bloom'
    gl.inputs['Quality'].default_value = 'High'
    gl.inputs['Threshold'].default_value = esik
    gl.inputs['Strength'].default_value = bloom
    gl.inputs['Size'].default_value = boyut
    ln.new(rl.outputs['Image'], gl.inputs['Image'])
    son = gl.outputs['Image']
    if vinyet > 0:
        em = n.new('CompositorNodeEllipseMask')
        em.inputs['Size'].default_value = (1.35, 1.35)
        bl = n.new('CompositorNodeBlur')
        bl.inputs['Size'].default_value = (300, 300) if 'Size' in bl.inputs and bl.inputs['Size'].type == 'VECTOR' else bl.inputs['Size'].default_value
        mx = n.new('CompositorNodeMixRGB') if 'CompositorNodeMixRGB' in dir(bpy.types) else None
        try:
            mul = n.new('ShaderNodeMix')
            mul.data_type = 'RGBA'
            mul.blend_type = 'MULTIPLY'
            mul.inputs['Factor'].default_value = vinyet
            ln.new(son, mul.inputs['A'])
            ln.new(em.outputs['Mask'], bl.inputs['Image'])
            ln.new(bl.outputs['Image'], mul.inputs['B'])
            son = mul.outputs['Result']
        except Exception as e:  # vinyet isteğe bağlı
            print('vinyet atlandı:', e)
    go = n.new('NodeGroupOutput')
    ln.new(son, go.inputs[0])
    return ng


def sis(boyut, konum, yogunluk=0.012, renk=(1.0, 1.0, 1.0), yonlu=0.55):
    """Hacimli hafif sis kutusu: ışık huzmeleri ve derinlik (tek saçılım, volume_bounces 0)."""
    mat = bpy.data.materials.new('Sis')
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    pv = nt.nodes.new('ShaderNodeVolumePrincipled')
    pv.inputs['Density'].default_value = yogunluk
    pv.inputs['Color'].default_value = (*renk, 1.0)
    pv.inputs['Anisotropy'].default_value = yonlu
    nt.links.new(pv.outputs[0], out.inputs['Volume'])
    ob = box('Sis', boyut, konum, mat)
    ob.visible_shadow = False
    bpy.context.scene.cycles.volume_step_rate = 4.0
    bpy.context.scene.cycles.volume_max_steps = 256
    return ob


def sablon(tur='ico', subdiv=2):
    """Tek bir şablon ağın (köşe, yüz) dizileri: 'ico' (r=1) ya da 'kup' (kenar=1)."""
    import bmesh
    import numpy as np
    bm = bmesh.new()
    if tur == 'ico':
        bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    else:
        bmesh.ops.create_cube(bm, size=1.0)
    v = np.array([x.co[:] for x in bm.verts], dtype=np.float32)
    f = [[x.index for x in fc.verts] for fc in bm.faces]
    bm.free()
    return v, f


def toplu_mesh(name, sablon_vf, merkez, olcek, donme=None, mat=None, yumusak=False):
    """Şablonu N kez kopyalayıp tek ağ yapar (numpy; bmesh'in O(N²) yavaşlığı yok).
    merkez: (N,3); olcek: (N,) ya da (N,3); donme: (N,3) Euler XYZ (radyan) ya da None."""
    import numpy as np
    tv, tf = sablon_vf
    merkez = np.asarray(merkez, dtype=np.float32)
    n, k = len(merkez), len(tv)
    if isinstance(olcek, (list, tuple)) and any(np.ndim(o) for o in olcek):
        olcek = [(o, o, o) if np.ndim(o) == 0 else o for o in olcek]  # karışık ölçek listesi
    olcek = np.asarray(olcek, dtype=np.float32)
    if olcek.ndim == 1:
        olcek = np.repeat(olcek[:, None], 3, axis=1)
    v = tv[None, :, :] * olcek[:, None, :]
    if donme is not None:
        e = np.asarray(donme, dtype=np.float32)
        cx, sx = np.cos(e[:, 0]), np.sin(e[:, 0])
        cy, sy = np.cos(e[:, 1]), np.sin(e[:, 1])
        cz, sz = np.cos(e[:, 2]), np.sin(e[:, 2])
        # R = Rz @ Ry @ Rx (Blender XYZ Euler)
        R = np.empty((n, 3, 3), dtype=np.float32)
        R[:, 0, 0] = cz * cy
        R[:, 0, 1] = cz * sy * sx - sz * cx
        R[:, 0, 2] = cz * sy * cx + sz * sx
        R[:, 1, 0] = sz * cy
        R[:, 1, 1] = sz * sy * sx + cz * cx
        R[:, 1, 2] = sz * sy * cx - cz * sx
        R[:, 2, 0] = -sy
        R[:, 2, 1] = cy * sx
        R[:, 2, 2] = cy * cx
        v = np.einsum('nij,nkj->nki', R, v)
    v = (v + merkez[:, None, :]).reshape(-1, 3)
    fl = [len(x) for x in tf]
    tf_flat = np.array([i for x in tf for i in x], dtype=np.int32)
    loops = (tf_flat[None, :] + (np.arange(n, dtype=np.int32) * k)[:, None]).reshape(-1)
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(v))
    me.vertices.foreach_set('co', v.ravel())
    me.loops.add(len(loops))
    me.loops.foreach_set('vertex_index', loops)
    me.polygons.add(n * len(tf))
    sizes = np.tile(np.array(fl, dtype=np.int32), n)
    starts = np.concatenate([[0], np.cumsum(sizes)[:-1]]).astype(np.int32)
    me.polygons.foreach_set('loop_start', starts)
    me.update(calc_edges=True)
    me.validate()
    # Blender 4.1+: yeni yüzler varsayılan yumuşak gölgeli; kutular için açıkça düz yap
    me.polygons.foreach_set('use_smooth', np.full(len(me.polygons), bool(yumusak)))
    ob = bpy.data.objects.new(name, me)
    link(ob)
    if mat:
        ob.data.materials.append(mat)
    return ob
