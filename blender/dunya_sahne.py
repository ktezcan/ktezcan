"""
Dünya (s5) sahne parçaları: dünya (gök), küre gövdesi, çift atmosfer, bulut kabuğu, arka ışıma, kıta noktaları (Geometry
Nodes), yaylar (kare kare kurulan ışık tüpleri), halkalar, iğneler. Hepsi kodla; yazı/rakam yok.

Kural: lime yalnız yay / fabrika iğnesi / halka / Türkiye noktaları (marka vurgusu, müşteri onaylı). Gövde, atmosfer, bulut,
yıldız lime DEĞİL.
"""
import math

import numpy as np
import bpy
from mathutils import Vector, Matrix

import kit

R = 1.0


# ---------------------------------------------------------------------------
#  Dünya (gök): kamera koyu degrade görür; çevre ışığı çok zayıf (gece yarısı karanlık kalsın)
# ---------------------------------------------------------------------------
def dunya_world(ust='#0a121a', alt='#020406', ortam=0.010):
    world = bpy.data.worlds.new('Dunya')
    bpy.context.scene.world = world
    world.use_nodes = True
    nt = kit.NT(world.node_tree)
    nt.n.clear()
    out = nt.node('ShaderNodeOutputWorld', (900, 0))
    lp = nt.node('ShaderNodeLightPath', (0, 300))
    mix = nt.node('ShaderNodeMixShader', (700, 0))
    nt.link(lp.outputs['Is Camera Ray'], mix.inputs[0])
    amb = nt.node('ShaderNodeBackground', (300, -150))
    amb.inputs['Color'].default_value = (0.50, 0.62, 0.85, 1.0)
    amb.inputs['Strength'].default_value = ortam
    nt.link(amb.outputs[0], mix.inputs[1])
    tc = nt.node('ShaderNodeTexCoord', (-500, 300))
    sep = nt.node('ShaderNodeSeparateXYZ', (-300, 300))
    nt.link(tc.outputs['Window'], sep.inputs[0])
    ramp = nt.node('ShaderNodeValToRGB', (-100, 300))
    ramp.color_ramp.elements[0].color = kit.srgb(alt)
    ramp.color_ramp.elements[1].color = kit.srgb(ust)
    ramp.color_ramp.interpolation = 'EASE'
    nt.link(sep.outputs['Y'], ramp.inputs['Fac'])
    bg = nt.node('ShaderNodeBackground', (300, 150))
    nt.link(ramp.outputs['Color'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = 1.0
    nt.link(bg.outputs[0], mix.inputs[2])
    nt.link(mix.outputs[0], out.inputs['Surface'])
    return world


def gunes_isigi():
    ld = bpy.data.lights.new('Gunes', 'SUN')
    ld.energy = 4.0
    ld.angle = math.radians(0.6)
    ld.color = (1.0, 0.93, 0.82)
    ob = bpy.data.objects.new('Gunes', ld)
    kit.link(ob)
    return ob


def gunes_yonlendir(ob, sun_to):
    """sun_to: güneşe yön (dünya). Işık bu yönün tersine gider."""
    d = -Vector(sun_to)
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


# ---------------------------------------------------------------------------
#  Küre gövdesi (koyu arduvaz; cam evresinde yarı saydam), çift atmosfer, bulut
# ---------------------------------------------------------------------------
def govde():
    bpy.ops.mesh.primitive_uv_sphere_add(segments=160, ring_count=80, radius=R)
    g = bpy.context.active_object
    g.name = 'Kure'
    bpy.ops.object.shade_smooth()
    mat = bpy.data.materials.new('KureGovde')
    mat.use_nodes = True
    nt = kit.NT(mat.node_tree)
    b = nt.n.get('Principled BSDF')
    # ince gürültüyle hafif renk oynaması: yakın planda (bölge) boş zemin düz görünmesin
    tc = nt.node('ShaderNodeTexCoord', (-900, 0))
    n1 = nt.node('ShaderNodeTexNoise', (-650, 100))
    n1.inputs['Scale'].default_value = 520.0     # ≈ 12 km öbekler
    n1.inputs['Detail'].default_value = 5.0
    nt.link(tc.outputs['Object'], n1.inputs['Vector'])
    n2 = nt.node('ShaderNodeTexNoise', (-650, -150))
    n2.inputs['Scale'].default_value = 7.0       # ≈ 900 km öbekler
    n2.inputs['Detail'].default_value = 3.0
    nt.link(tc.outputs['Object'], n2.inputs['Vector'])
    m1 = nt.node('ShaderNodeMix', (-350, 0), data_type='RGBA')
    nt.link(n1.outputs['Fac'], m1.inputs['Factor'])
    m1.inputs['A'].default_value = kit.srgb('#2a4252')
    m1.inputs['B'].default_value = kit.srgb('#36546a')
    m2 = nt.node('ShaderNodeMix', (-150, 0), data_type='RGBA')
    nt.link(n2.outputs['Fac'], m2.inputs['Factor'])
    m2.inputs['Factor'].default_value = 1.0
    nt.link(m1.outputs['Result'], m2.inputs['A'])
    m2.inputs['B'].default_value = kit.srgb('#3d5e75')
    mf = nt.math('MULTIPLY', n2.outputs['Fac'], 0.35, loc=(-350, -250))
    nt.link(mf, m2.inputs['Factor'])
    nt.link(m2.outputs['Result'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.6
    b.inputs['Coat Weight'].default_value = 0.12
    b.inputs['Coat Roughness'].default_value = 0.4
    b.inputs['Specular IOR Level'].default_value = 0.35
    g.data.materials.append(mat)
    return g, b


def atmosfer(ad, yaricap, renk, guc, a, b, c, gunes_orani=0.25):
    """Kabuk atmosfer: emisyon = guc · bump(cos) · (gunes_orani + (1-gunes_orani)·gündüz).
    bump(cos) = smooth(cos/a) · (1 − smooth((cos−b)/c)); cos = |normal·gelen|. Dönenler: nesne, düğüm sözlüğü."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=yaricap)
    ob = bpy.context.active_object
    ob.name = ad
    bpy.ops.object.shade_smooth()
    mat = bpy.data.materials.new(ad)
    mat.use_nodes = True
    nt = kit.NT(mat.node_tree)
    nt.n.clear()
    out = nt.node('ShaderNodeOutputMaterial', (1500, 0))
    geo = nt.node('ShaderNodeNewGeometry', (-900, 0))
    dot = nt.node('ShaderNodeVectorMath', (-650, 0), operation='DOT_PRODUCT')
    nt.link(geo.outputs['Normal'], dot.inputs[0])
    nt.link(geo.outputs['Incoming'], dot.inputs[1])
    cs = nt.math('ABSOLUTE', dot.outputs['Value'], loc=(-450, 0))
    # smooth(cos / a)
    m1 = nt.node('ShaderNodeMapRange', (-250, 150), interpolation_type='SMOOTHSTEP')
    nt.link(cs, m1.inputs['Value'])
    m1.inputs['From Min'].default_value = 0.0
    m1.inputs['From Max'].default_value = a
    # 1 − smooth((cos − b)/c)
    m2 = nt.node('ShaderNodeMapRange', (-250, -100), interpolation_type='SMOOTHSTEP')
    nt.link(cs, m2.inputs['Value'])
    m2.inputs['From Min'].default_value = b
    m2.inputs['From Max'].default_value = b + c
    m2.inputs['To Min'].default_value = 1.0
    m2.inputs['To Max'].default_value = 0.0
    bump = nt.math('MULTIPLY', m1.outputs['Result'], m2.outputs['Result'], loc=(0, 0))
    # güneş yönü: gündüz yarıda güçlü
    sx = nt.node('ShaderNodeCombineXYZ', (-650, -300))
    dn = nt.node('ShaderNodeVectorMath', (-450, -300), operation='DOT_PRODUCT')
    nt.link(geo.outputs['Normal'], dn.inputs[0])
    nt.link(sx.outputs['Vector'], dn.inputs[1])
    gd = nt.node('ShaderNodeMapRange', (-250, -300), interpolation_type='SMOOTHSTEP')
    nt.link(dn.outputs['Value'], gd.inputs['Value'])
    gd.inputs['From Min'].default_value = -0.30
    gd.inputs['From Max'].default_value = 0.55
    gd.inputs['To Min'].default_value = gunes_orani
    gd.inputs['To Max'].default_value = 1.0
    ef = nt.math('MULTIPLY', bump, gd.outputs['Result'], loc=(250, 0), clamp=True)
    gv = nt.node('ShaderNodeValue', (250, -200))
    gv.outputs[0].default_value = guc
    em = nt.node('ShaderNodeEmission', (700, 100))
    em.inputs['Color'].default_value = renk
    nt.link(gv.outputs[0], em.inputs['Strength'])
    tr = nt.node('ShaderNodeBsdfTransparent', (700, -100))
    mx = nt.node('ShaderNodeMixShader', (1000, 0))
    nt.link(ef, mx.inputs[0])
    nt.link(tr.outputs[0], mx.inputs[1])
    nt.link(em.outputs[0], mx.inputs[2])
    nt.link(mx.outputs[0], out.inputs['Surface'])
    ob.data.materials.append(mat)
    ob.visible_shadow = False
    ob.visible_glossy = False
    ob.visible_diffuse = False
    return ob, {'guc': gv.outputs[0], 'gunes': sx, 'em': em}


def bulut_kabugu(ad, yaricap, olcek=3.2, ege_delik=True):
    """İnce bulut kabuğu: Noise alfa + Ege üstü açık (küreye sabit delik), gürültü deseni kürenin üstünde ayrıca döner."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=1.0)
    ob = bpy.context.active_object
    ob.name = ad
    bpy.ops.object.shade_smooth()
    ob.scale = (yaricap, yaricap, yaricap)
    mat = bpy.data.materials.new(ad)
    mat.use_nodes = True
    nt = kit.NT(mat.node_tree)
    nt.n.clear()
    out = nt.node('ShaderNodeOutputMaterial', (1400, 0))
    tc = nt.node('ShaderNodeTexCoord', (-1100, 0))
    mp = nt.node('ShaderNodeMapping', (-900, 0))
    nt.link(tc.outputs['Object'], mp.inputs['Vector'])
    nz = nt.node('ShaderNodeTexNoise', (-650, 100))
    nz.inputs['Scale'].default_value = olcek
    nz.inputs['Detail'].default_value = 6.0
    nz.inputs['Roughness'].default_value = 0.55
    nz.inputs['Distortion'].default_value = 0.7
    nt.link(mp.outputs['Vector'], nz.inputs['Vector'])
    cov = nt.node('ShaderNodeMapRange', (-400, 100), interpolation_type='SMOOTHSTEP')
    nt.link(nz.outputs['Fac'], cov.inputs['Value'])
    cov.inputs['From Min'].default_value = 0.54
    cov.inputs['From Max'].default_value = 0.78
    alfa = cov.outputs['Result']
    if ege_delik:
        # Ege (İzmir) üstü açık: nesne uzayında İzmir yönüyle iç çarpım (küreye sabit)
        import dunya_veri as dv
        iz = dv.birim(*dv.IZMIR)
        sab = nt.node('ShaderNodeCombineXYZ', (-900, -300))
        sab.inputs[0].default_value, sab.inputs[1].default_value, sab.inputs[2].default_value = float(iz[0]), float(iz[1]), float(iz[2])
        dt = nt.node('ShaderNodeVectorMath', (-650, -300), operation='DOT_PRODUCT')
        nt.link(tc.outputs['Object'], dt.inputs[0])
        nt.link(sab.outputs['Vector'], dt.inputs[1])
        hole = nt.node('ShaderNodeMapRange', (-400, -300), interpolation_type='SMOOTHSTEP')
        nt.link(dt.outputs['Value'], hole.inputs['Value'])
        hole.inputs['From Min'].default_value = math.cos(math.radians(26))   # 26° dışında bulut tam
        hole.inputs['From Max'].default_value = math.cos(math.radians(9))    # 9° içinde tamamen açık
        hole.inputs['To Min'].default_value = 1.0
        hole.inputs['To Max'].default_value = 0.0
        alfa = nt.math('MULTIPLY', alfa, hole.outputs['Result'], loc=(-100, 0))
    mx_node = nt.node('ShaderNodeValue', (-100, -150))
    mx_node.outputs[0].default_value = 0.55
    alfa2 = nt.math('MULTIPLY', alfa, mx_node.outputs[0], loc=(100, 0), clamp=True)
    df = nt.node('ShaderNodeBsdfDiffuse', (500, 100))
    df.inputs['Color'].default_value = (0.86, 0.90, 0.95, 1.0)
    em = nt.node('ShaderNodeEmission', (500, -50))
    em.inputs['Color'].default_value = (0.55, 0.65, 0.80, 1.0)
    em.inputs['Strength'].default_value = 0.012      # gece yarıda da çok hafif okunsun
    ad_ = nt.node('ShaderNodeAddShader', (750, 50))
    nt.link(df.outputs[0], ad_.inputs[0])
    nt.link(em.outputs[0], ad_.inputs[1])
    tr = nt.node('ShaderNodeBsdfTransparent', (750, -150))
    mx = nt.node('ShaderNodeMixShader', (1100, 0))
    nt.link(alfa2, mx.inputs[0])
    nt.link(tr.outputs[0], mx.inputs[1])
    nt.link(ad_.outputs[0], mx.inputs[2])
    nt.link(mx.outputs[0], out.inputs['Surface'])
    ob.data.materials.append(mat)
    ob.visible_shadow = False
    return ob, {'maks': mx_node.outputs[0], 'harita': mp, 'gurultu': nz}


def arka_isima():
    """Kürenin arkasında yumuşak sıcak ışıma diski (çıkış karelerinde açılır)."""
    bpy.ops.mesh.primitive_plane_add(size=2.0)
    ob = bpy.context.active_object
    ob.name = 'ArkaIsima'
    ob.rotation_euler = (math.radians(90), 0, 0)   # normal −Y: kameraya bakar
    mat = bpy.data.materials.new('ArkaIsima')
    mat.use_nodes = True
    nt = kit.NT(mat.node_tree)
    nt.n.clear()
    out = nt.node('ShaderNodeOutputMaterial', (900, 0))
    tc = nt.node('ShaderNodeTexCoord', (-700, 0))
    vm = nt.node('ShaderNodeVectorMath', (-500, 0), operation='SUBTRACT')
    nt.link(tc.outputs['UV'], vm.inputs[0])
    vm.inputs[1].default_value = (0.5, 0.5, 0.0)
    ln = nt.node('ShaderNodeVectorMath', (-300, 0), operation='LENGTH')
    nt.link(vm.outputs['Vector'], ln.inputs[0])
    m1 = nt.node('ShaderNodeMapRange', (-100, 150), interpolation_type='SMOOTHSTEP')
    nt.link(ln.outputs['Value'], m1.inputs['Value'])
    m1.inputs['From Min'].default_value = 0.20
    m1.inputs['From Max'].default_value = 0.29
    m2 = nt.node('ShaderNodeMapRange', (-100, -50), interpolation_type='SMOOTHSTEP')
    nt.link(ln.outputs['Value'], m2.inputs['Value'])
    m2.inputs['From Min'].default_value = 0.30
    m2.inputs['From Max'].default_value = 0.50
    m2.inputs['To Min'].default_value = 1.0
    m2.inputs['To Max'].default_value = 0.0
    sq0 = nt.math('MULTIPLY', m1.outputs['Result'], m2.outputs['Result'], loc=(100, 100))
    sq = nt.math('POWER', sq0, 1.6, loc=(250, 100))
    gv = nt.node('ShaderNodeValue', (100, -200))
    gv.outputs[0].default_value = 0.0
    em = nt.node('ShaderNodeEmission', (400, 100))
    em.inputs['Color'].default_value = (1.0, 0.70, 0.42, 1.0)
    nt.link(gv.outputs[0], em.inputs['Strength'])
    tr = nt.node('ShaderNodeBsdfTransparent', (400, -100))
    mx = nt.node('ShaderNodeMixShader', (650, 0))
    nt.link(sq, mx.inputs[0])
    nt.link(tr.outputs[0], mx.inputs[1])
    nt.link(em.outputs[0], mx.inputs[2])
    nt.link(mx.outputs[0], out.inputs['Surface'])
    ob.data.materials.append(mat)
    ob.visible_shadow = False
    ob.visible_glossy = False
    ob.visible_diffuse = False
    return ob, gv.outputs[0]


# ---------------------------------------------------------------------------
#  Kıta noktaları (Geometry Nodes ile örneklenmiş küçük küreler; 'olcek' ≤ 0 olanlar silinir)
# ---------------------------------------------------------------------------
_NOKTA_GN = {}


def nokta_nesnesi(S, kaldirma):
    n = S.n
    pos = S.u * (R + kaldirma)
    me = bpy.data.meshes.new('Kara_' + S.ad)
    me.vertices.add(n)
    me.vertices.foreach_set('co', pos.astype(np.float32).ravel())
    me.attributes.new('renk', 'FLOAT_COLOR', 'POINT')
    me.attributes.new('isik', 'FLOAT', 'POINT')
    me.attributes.new('olcek', 'FLOAT', 'POINT')
    me.update()
    ob = bpy.data.objects.new('Kara_' + S.ad, me)
    kit.link(ob)

    if 'mat' not in _NOKTA_GN:
        mat = bpy.data.materials.new('Nokta')
        mat.use_nodes = True
        nt = kit.NT(mat.node_tree)
        bsdf = nt.n.get('Principled BSDF')
        a = nt.node('ShaderNodeAttribute', (-500, 200), attribute_type='INSTANCER', attribute_name='renk')
        nt.link(a.outputs['Color'], bsdf.inputs['Base Color'])
        nt.link(a.outputs['Color'], bsdf.inputs['Emission Color'])
        e = nt.node('ShaderNodeAttribute', (-500, -100), attribute_type='INSTANCER', attribute_name='isik')
        nt.link(e.outputs['Fac'], bsdf.inputs['Emission Strength'])
        bsdf.inputs['Roughness'].default_value = 0.45
        _NOKTA_GN['mat'] = mat
    mat = _NOKTA_GN['mat']

    ng = bpy.data.node_groups.new('NoktaGN_' + S.ad, 'GeometryNodeTree')
    ng.interface.new_socket(name='Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    gi = ng.nodes.new('NodeGroupInput')
    go = ng.nodes.new('NodeGroupOutput')
    na = ng.nodes.new('GeometryNodeInputNamedAttribute')
    na.data_type = 'FLOAT'
    na.inputs['Name'].default_value = 'olcek'
    cmp_ = ng.nodes.new('FunctionNodeCompare')
    cmp_.data_type = 'FLOAT'
    cmp_.operation = 'LESS_EQUAL'
    cmp_.inputs['B'].default_value = 1e-9
    ng.links.new(na.outputs['Attribute'], cmp_.inputs['A'])
    dl = ng.nodes.new('GeometryNodeDeleteGeometry')
    dl.domain = 'POINT'
    ng.links.new(gi.outputs['Geometry'], dl.inputs['Geometry'])
    ng.links.new(cmp_.outputs['Result'], dl.inputs['Selection'])
    ico = ng.nodes.new('GeometryNodeMeshIcoSphere')
    ico.inputs['Radius'].default_value = 1.0
    ico.inputs['Subdivisions'].default_value = 2
    sh = ng.nodes.new('GeometryNodeSetShadeSmooth')
    ng.links.new(ico.outputs['Mesh'], sh.inputs['Geometry'])
    sm_ = ng.nodes.new('GeometryNodeSetMaterial')
    sm_.inputs['Material'].default_value = mat
    ng.links.new(sh.outputs['Geometry'], sm_.inputs['Geometry'])
    iop = ng.nodes.new('GeometryNodeInstanceOnPoints')
    ng.links.new(dl.outputs['Geometry'], iop.inputs['Points'])
    ng.links.new(sm_.outputs['Geometry'], iop.inputs['Instance'])
    nb = ng.nodes.new('GeometryNodeInputNamedAttribute')
    nb.data_type = 'FLOAT'
    nb.inputs['Name'].default_value = 'olcek'
    ng.links.new(nb.outputs['Attribute'], iop.inputs['Scale'])
    ng.links.new(iop.outputs['Instances'], go.inputs['Geometry'])
    ob.modifiers.new('Noktalar', 'NODES').node_group = ng
    return ob


def nokta_guncelle(ob, col, glow, olcek):
    me = ob.data
    me.attributes['renk'].data.foreach_set('color', col.astype(np.float32).ravel())
    me.attributes['isik'].data.foreach_set('value', glow.astype(np.float32))
    me.attributes['olcek'].data.foreach_set('value', olcek.astype(np.float32))
    me.update()


# ---------------------------------------------------------------------------
#  Yaylar: kare kare kurulan ışık tüpü (çekirdek) + geniş yumuşak ışıma tüpü; kuyruklu damla
# ---------------------------------------------------------------------------
YAN = 8      # tüp kesit kenar sayısı
NYOL = 168   # yol noktası


def _yay_yolu(a, b, ang_yukseklik=0.16, tavan=0.11):
    """İzmir → hedef büyük daire yayı; yükseklik mesafeyle orantılı. Dönen: (NYOL,3) küre yerel koordinatları."""
    import dunya_veri as dv
    va, vb = dv.birim(*a).astype(np.float64), dv.birim(*b).astype(np.float64)
    ang = math.acos(max(-1.0, min(1.0, float(va @ vb))))
    u = np.linspace(0.0, 1.0, NYOL)
    p = (va[None, :] * np.sin((1 - u) * ang)[:, None] + vb[None, :] * np.sin(u * ang)[:, None]) / math.sin(ang)
    p /= np.linalg.norm(p, axis=1, keepdims=True)
    h = 1.0 + 0.004 + min(tavan, ang_yukseklik * ang / math.pi) * 4 * u * (1 - u)
    return p * h[:, None], ang


class Yay:
    """Tek yay: iki ağ nesnesi (çekirdek, ışıma) — her karede yarıçap/parlaklık dizileri yeniden yazılır."""

    def __init__(self, ad, a, b, mat_cekirdek, mat_isima):
        self.ad = ad
        self.yol, self.ang = _yay_yolu(a, b)
        n = NYOL
        tan = np.gradient(self.yol, axis=0)
        tan /= np.linalg.norm(tan, axis=1, keepdims=True) + 1e-12
        rad = self.yol / np.linalg.norm(self.yol, axis=1, keepdims=True)
        bn = np.cross(tan, rad)
        bn /= np.linalg.norm(bn, axis=1, keepdims=True) + 1e-12
        self.rad, self.bn = rad, bn
        a_ = np.linspace(0, 2 * math.pi, YAN, endpoint=False)
        self.cs, self.sn = np.cos(a_), np.sin(a_)
        loops = []
        for i in range(n - 1):
            for k in range(YAN):
                k2 = (k + 1) % YAN
                loops += [i * YAN + k, (i + 1) * YAN + k, (i + 1) * YAN + k2, i * YAN + k2]
        self.loops = np.array(loops, dtype=np.int32)
        self.nobjs = []
        for tag, mat in (('c', mat_cekirdek), ('i', mat_isima)):
            me = bpy.data.meshes.new(f'{ad}_{tag}')
            me.vertices.add(n * YAN)
            me.loops.add(len(self.loops))
            me.loops.foreach_set('vertex_index', self.loops)
            npoly = (n - 1) * YAN
            me.polygons.add(npoly)
            me.polygons.foreach_set('loop_start', np.arange(npoly, dtype=np.int32) * 4)
            me.update(calc_edges=True)
            me.polygons.foreach_set('use_smooth', np.ones(npoly, dtype=bool))
            me.attributes.new('isik', 'FLOAT', 'POINT')
            me.attributes.new('beyaz', 'FLOAT', 'POINT')
            ob = bpy.data.objects.new(f'{ad}_{tag}', me)
            kit.link(ob)
            ob.data.materials.append(mat)
            ob.visible_shadow = False
            self.nobjs.append(ob)
        self.cek, self.isi = self.nobjs
        self.u = np.linspace(0.0, 1.0, NYOL)

    def konum(self, e):
        """Yol üzerinde parametre e (0..1) noktası (küre yerel)."""
        x = float(np.clip(e, 0, 1)) * (NYOL - 1)
        j = min(NYOL - 2, int(x))
        fr = x - j
        return self.yol[j] * (1 - fr) + self.yol[j + 1] * fr

    def guncelle(self, iz_son, bas, kuyruk_uz, r_iz, r_cek, r_isima, isik_iz, isik_cek, gorunur=True):
        """iz_son: kalıcı iz [0, iz_son]; bas: kuyruklu parlak pencerenin baş konumu (None = kuyruk yok; 1'i aşabilir),
        kuyruk_uz: pencere uzunluğu (yol oranı). Yarıçaplar R birimi (yakınlaştırma çarpanı uygulanmış gelir)."""
        u = self.u
        mask = u <= iz_son
        w = np.zeros_like(u)
        if bas is not None:
            w = np.clip((u - (bas - kuyruk_uz)) / max(kuyruk_uz, 1e-6), 0, 1)
            w = w * w * (3 - 2 * w) * (u <= bas)
        r = np.where(mask, r_iz + (r_cek - r_iz) * w, 1e-7)
        ri = np.where(mask, r_isima * (0.20 + 0.80 * w), 1e-7)
        isik = isik_iz + (isik_cek - isik_iz) * w
        isik_i = 0.10 + 0.90 * w
        for ob, rr, ii in ((self.cek, r, isik), (self.isi, ri, isik_i)):
            co = self.yol[:, None, :] + rr[:, None, None] * (self.cs[None, :, None] * self.rad[:, None, :] +
                                                             self.sn[None, :, None] * self.bn[:, None, :])
            ob.data.vertices.foreach_set('co', co.astype(np.float32).ravel())
            ob.data.attributes['isik'].data.foreach_set('value', np.repeat(ii, YAN).astype(np.float32))
            ob.data.attributes['beyaz'].data.foreach_set('value', np.repeat(w, YAN).astype(np.float32))
            ob.data.update()
            ob.hide_render = not gorunur


def yay_malzemeleri():
    """(çekirdek, ışıma) malzemeleri. 'isik' ve 'beyaz' köşe öznitelikleri."""
    # çekirdek: lime → başta sıcak beyaz; şiddet = 'isik'
    m1 = bpy.data.materials.new('YayCekirdek')
    m1.use_nodes = True
    nt = kit.NT(m1.node_tree)
    nt.n.clear()
    out = nt.node('ShaderNodeOutputMaterial', (700, 0))
    ai = nt.node('ShaderNodeAttribute', (-500, 100), attribute_type='GEOMETRY', attribute_name='isik')
    ab = nt.node('ShaderNodeAttribute', (-500, -150), attribute_type='GEOMETRY', attribute_name='beyaz')
    mx = nt.node('ShaderNodeMix', (-200, -50), data_type='RGBA')
    nt.link(ab.outputs['Fac'], mx.inputs['Factor'])
    mx.inputs['A'].default_value = kit.LIME_HI
    mx.inputs['B'].default_value = (1.0, 1.0, 0.86, 1.0)
    em = nt.node('ShaderNodeEmission', (300, 0))
    nt.link(mx.outputs['Result'], em.inputs['Color'])
    nt.link(ai.outputs['Fac'], em.inputs['Strength'])
    nt.link(em.outputs[0], out.inputs['Surface'])
    # ışıma: yumuşak kenarlı (yüzey bakışı) şeffaf lime
    m2 = bpy.data.materials.new('YayIsima')
    m2.use_nodes = True
    nt = kit.NT(m2.node_tree)
    nt.n.clear()
    out = nt.node('ShaderNodeOutputMaterial', (900, 0))
    ai = nt.node('ShaderNodeAttribute', (-500, 100), attribute_type='GEOMETRY', attribute_name='isik')
    geo = nt.node('ShaderNodeNewGeometry', (-700, -200))
    dot = nt.node('ShaderNodeVectorMath', (-500, -200), operation='DOT_PRODUCT')
    nt.link(geo.outputs['Normal'], dot.inputs[0])
    nt.link(geo.outputs['Incoming'], dot.inputs[1])
    ab = nt.math('ABSOLUTE', dot.outputs['Value'], loc=(-300, -200))
    pw = nt.math('POWER', ab, 2.6, loc=(-100, -200))
    al = nt.math('MULTIPLY', pw, ai.outputs['Fac'], loc=(100, -100), clamp=True)
    em = nt.node('ShaderNodeEmission', (300, 100))
    em.inputs['Color'].default_value = kit.LIME_HI
    em.inputs['Strength'].default_value = 3.2
    tr = nt.node('ShaderNodeBsdfTransparent', (300, -100))
    mx2 = nt.node('ShaderNodeMixShader', (600, 0))
    nt.link(al, mx2.inputs[0])
    nt.link(tr.outputs[0], mx2.inputs[1])
    nt.link(em.outputs[0], mx2.inputs[2])
    nt.link(mx2.outputs[0], out.inputs['Surface'])
    return m1, m2


def damla(ad, yaricap=0.0065):
    """Yay başı: parlak çekirdek (küçük) + yumuşak ışıma küresi. İkisi de tek 'ışıma' malzemesiyle."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=1.0)
    b = bpy.context.active_object
    b.name = ad
    bpy.ops.object.shade_smooth()
    b.data.materials.append(kit.emission_material(ad + '_m', (1.0, 1.0, 0.86, 1.0), 40.0))
    b.visible_shadow = False
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.0)
    g = bpy.context.active_object
    g.name = ad + '_isima'
    bpy.ops.object.shade_smooth()
    mat = bpy.data.materials.new(ad + '_gm')
    mat.use_nodes = True
    nt = kit.NT(mat.node_tree)
    nt.n.clear()
    out = nt.node('ShaderNodeOutputMaterial', (900, 0))
    geo = nt.node('ShaderNodeNewGeometry', (-700, 0))
    dot = nt.node('ShaderNodeVectorMath', (-500, 0), operation='DOT_PRODUCT')
    nt.link(geo.outputs['Normal'], dot.inputs[0])
    nt.link(geo.outputs['Incoming'], dot.inputs[1])
    ab = nt.math('ABSOLUTE', dot.outputs['Value'], loc=(-300, 0))
    pw = nt.math('POWER', ab, 3.0, loc=(-100, 0))
    em = nt.node('ShaderNodeEmission', (300, 100))
    em.inputs['Color'].default_value = kit.LIME_HI
    em.inputs['Strength'].default_value = 6.0
    tr = nt.node('ShaderNodeBsdfTransparent', (300, -100))
    mx = nt.node('ShaderNodeMixShader', (600, 0))
    nt.link(pw, mx.inputs[0])
    nt.link(tr.outputs[0], mx.inputs[1])
    nt.link(em.outputs[0], mx.inputs[2])
    nt.link(mx.outputs[0], out.inputs['Surface'])
    g.data.materials.append(mat)
    g.visible_shadow = False
    return b, g


# ---------------------------------------------------------------------------
#  İğne (fabrika): ince ışık direği; halka: birim yarıçaplı, her karede ölçeklenir
# ---------------------------------------------------------------------------
def igne(ad, guc=14.0):
    """Fabrika iğnesi: tabanı parlak, tepeye doğru sönen ince koni (z=0..1). Boy/kalınlık nesne ölçeğiyle."""
    bpy.ops.mesh.primitive_cone_add(vertices=14, radius1=1.0, radius2=0.12, depth=1.0, end_fill_type='NOTHING')
    ob = bpy.context.active_object
    ob.name = ad
    for v in ob.data.vertices:   # tabanı z=0, tepesi z=1
        v.co.z += 0.5
    bpy.ops.object.shade_smooth()
    mat = bpy.data.materials.new(ad + '_m')
    mat.use_nodes = True
    nt = kit.NT(mat.node_tree)
    nt.n.clear()
    out = nt.node('ShaderNodeOutputMaterial', (900, 0))
    tc = nt.node('ShaderNodeTexCoord', (-700, 0))
    sp = nt.node('ShaderNodeSeparateXYZ', (-500, 0))
    nt.link(tc.outputs['Object'], sp.inputs[0])
    inv = nt.math('SUBTRACT', 1.0, sp.outputs['Z'], loc=(-300, 0), clamp=True)
    pw = nt.math('POWER', inv, 1.6, loc=(-100, 0))
    mul = nt.node('ShaderNodeMath', (100, 0), operation='MULTIPLY')
    nt.link(pw, mul.inputs[0])
    mul.inputs[1].default_value = guc
    em = nt.node('ShaderNodeEmission', (400, 0))
    em.inputs['Color'].default_value = kit.LIME_HI
    nt.link(mul.outputs[0], em.inputs['Strength'])
    nt.link(em.outputs[0], out.inputs['Surface'])
    ob.data.materials.append(mat)
    ob.visible_shadow = False
    ob['_mul'] = mul.name
    ob['_guc'] = guc
    return ob


def igne_guc(ob, k):
    nt = ob.data.materials[0].node_tree
    nt.nodes[ob['_mul']].inputs[1].default_value = ob['_guc'] * k


def halka_birim(ad, kalinlik=0.10, guc=7.0, renk=None):
    """Birim yarıçaplı düz halka (XY düzlemi); sahnede nesne ölçeğiyle büyütülür."""
    return kit.halo_ring(ad, radius=1.0, width=kalinlik, color=renk or kit.LIME, strength=guc, segments=128, z=0.0)


def yerel_matris(rot, lat, lon, yukseklik=0.0):
    """Küre yüzeyinde (lat, lon) noktasında, normali +Z olan yerel çerçeve (dünya matrisi). rot: küre dönüşü."""
    import dunya_veri as dv
    n = Vector(tuple(float(x) for x in dv.birim(lat, lon))) * (R + yukseklik)
    q = n.normalized().to_track_quat('Z', 'Y').to_matrix().to_4x4()
    return rot @ Matrix.Translation(n) @ q
