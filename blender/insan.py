"""
Gerçekçi insan üreticisi (MakeHuman CC0 temel ağı + iskelet + ağırlıklar, kod ile).

Veri (CC0, MakeHuman topluluğu): base.obj, default.mhskel, default_weights.mhw,
targets.npz (pip makehuman paketi). Yol: EGE_MH ortam değişkeni (klasör).

  insan(tip, poz, faz, giysi, konum, yon, boy)
    tip  : 'erkek' | 'kadin' | 'cocuk' | 'yasli' | 'kiz'
    poz  : 'yuru' (faz 0..1 adım döngüsü) | 'dur' | 'bisiklet' (faz: pedal açısı) | 'otur'
    giysi: dict(ust, alt, ayakkabi, sac, ten, kol='kisa'|'uzun')

Giysi ayrı ağ değil: yüzler baskın kemiğe göre bölgelere ayrılır (ten, üst, alt, ayakkabı,
saç); üst/alt hafifçe dışa şişirilir. Sokak mesafesinde gerçek giysi gibi okunur.
"""
import json
import math
import os

import bpy
import numpy as np
from mathutils import Matrix, Vector

import kit

MH = os.environ.get('EGE_MH', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mh'))
_VERI = {}


def _veri():
    if _VERI:
        return _VERI
    v, f, g = [], [], []
    grup = None
    for satir in open(os.path.join(MH, 'base.obj'), encoding='utf-8'):
        if satir.startswith('v '):
            v.append([float(x) for x in satir.split()[1:4]])
        elif satir.startswith('g '):
            grup = satir.split()[1]
        elif satir.startswith('f '):
            f.append([int(x.split('/')[0]) - 1 for x in satir.split()[1:]])
            g.append(grup)
    _VERI['v'] = np.array(v, dtype=np.float64)
    _VERI['f'] = f
    _VERI['g'] = g
    _VERI['skel'] = json.load(open(os.path.join(MH, 'default.mhskel')))
    _VERI['w'] = json.load(open(os.path.join(MH, 'default_weights.mhw')))['weights']
    _VERI['t'] = np.load(os.path.join(MH, 'targets.npz'))
    return _VERI


def _hedef(v, ad, w):
    d = _veri()['t']
    i = d[f'targets/{ad}.index']
    if len(i) == 0 or w == 0:
        return
    v[i.astype(np.int64)] += d[f'targets/{ad}.vector'].astype(np.float64) / 1000.0 * w


TIP = {  # (cinsiyet, yaş, kilo) → hedefler
    'erkek': [('macrodetails/caucasian-male-young', 1.0), ('macrodetails/universal-male-young-averagemuscle-maxweight', 0.15)],
    'kadin': [('macrodetails/caucasian-female-young', 1.0), ('macrodetails/universal-female-young-averagemuscle-minweight', 0.25)],
    'cocuk': [('macrodetails/caucasian-male-child', 1.0)],
    'kiz': [('macrodetails/caucasian-female-child', 1.0)],
    'yasli': [('macrodetails/caucasian-male-old', 1.0), ('macrodetails/universal-male-old-averagemuscle-maxweight', 0.3)],
}
BOY = {'erkek': 1.78, 'kadin': 1.65, 'cocuk': 1.25, 'kiz': 1.2, 'yasli': 1.72}

BOLGE = {  # kemik → bölge
    'foot': 'ayakkabi', 'toe': 'ayakkabi',
    'upperleg': 'alt', 'lowerleg': 'alt', 'pelvis': 'alt',
    'spine': 'ust', 'clavicle': 'ust', 'shoulder': 'ust', 'breast': 'ust', 'upperarm': 'ust',
    'lowerarm': 'kol', 'wrist': 'ten', 'finger': 'ten', 'metacarpal': 'ten',
    'neck': 'ten', 'head': 'ten', 'jaw': 'ten',
}


def _mh2bl(p):
    p = np.asarray(p)
    return np.stack([p[..., 0], -p[..., 2], p[..., 1]], axis=-1) * 0.1


def _mat(ad, hexcol, rough=0.7, sheen=0.0):
    m = bpy.data.materials.get(ad)
    if m:
        return m
    m = bpy.data.materials.new(ad)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = kit.srgb(hexcol)
    b.inputs['Roughness'].default_value = rough
    if sheen:
        b.inputs['Sheen Weight'].default_value = sheen
    return m


def _ten(ad, hexcol):
    m = bpy.data.materials.get(ad)
    if m:
        return m
    m = _mat(ad, hexcol, 0.42)
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Subsurface Weight'].default_value = 0.12
    b.inputs['Subsurface Radius'].default_value = (0.012, 0.005, 0.003)
    b.inputs['Subsurface Scale'].default_value = 0.4
    return m


def _kumas(ad, hexcol, rough=0.85, sheen=0.3):
    """Kumaş: sheen + uzamış gürültüyle hafif kırışık kabartısı."""
    m = bpy.data.materials.get(ad)
    if m:
        return m
    m = _mat(ad, hexcol, rough, sheen)
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (14.0, 14.0, 4.0)
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 3.0
    nz.inputs['Detail'].default_value = 6.0
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    bp = nt.nodes.new('ShaderNodeBump')
    bp.inputs['Strength'].default_value = 0.18
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m


def _insan_mat(g):
    """Tek malzeme: ten tabanı üzerine köşe özniteliklerine göre yumuşak sınırlı katmanlar
    (pantolon, gömlek, ayakkabı, taban, saç, kaş, dudak). Kumaş ve saçta kabartı."""
    ad = 'Insan_' + '_'.join(g[k] for k in ('ten', 'ust', 'alt', 'ayakkabi', 'sac'))
    m = bpy.data.materials.get(ad)
    if m:
        return m
    m = bpy.data.materials.new(ad)
    m.use_nodes = True
    nt = m.node_tree
    N, L = nt.nodes.new, nt.links.new
    b = nt.nodes['Principled BSDF']
    b.inputs['Subsurface Weight'].default_value = 0.1
    b.inputs['Subsurface Radius'].default_value = (0.012, 0.005, 0.003)
    b.inputs['Subsurface Scale'].default_value = 0.35
    renk = N('ShaderNodeRGB')
    renk.outputs[0].default_value = kit.srgb(g['ten'])
    cur_c, cur_r, cur_s = renk.outputs[0], None, None
    pr = N('ShaderNodeValue')
    pr.outputs[0].default_value = 0.55  # ten pürüzü (plastik parlaklık yok)
    cur_r = pr.outputs[0]
    sh = N('ShaderNodeValue')
    sh.outputs[0].default_value = 0.0
    cur_s = sh.outputs[0]
    tc = N('ShaderNodeTexCoord')
    mp = N('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (14.0, 14.0, 4.0)
    L(tc.outputs['Object'], mp.inputs['Vector'])
    nz = N('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 3.0
    nz.inputs['Detail'].default_value = 8.0
    L(mp.outputs['Vector'], nz.inputs['Vector'])
    mp2 = N('ShaderNodeMapping')
    mp2.inputs['Scale'].default_value = (90.0, 90.0, 8.0)
    L(tc.outputs['Object'], mp2.inputs['Vector'])
    nz2 = N('ShaderNodeTexNoise')  # saç telleri
    nz2.inputs['Scale'].default_value = 4.0
    nz2.inputs['Detail'].default_value = 10.0
    L(mp2.outputs['Vector'], nz2.inputs['Vector'])
    kabart = None
    for at, hexcol, rough, sheen, tur in (('r_alt', g['alt'], 0.8, 0.2, 'kumas'), ('r_ust', g['ust'], 0.85, 0.35, 'kumas'),
                                          ('r_ayak', g['ayakkabi'], 0.35, 0.0, ''), ('r_taban', g.get('taban', '#ece9e3'), 0.6, 0.0, ''),
                                          ('r_sac', g['sac'], 0.4, 0.08, 'sac'), ('r_kas', g['sac'], 0.6, 0.2, ''),
                                          ('r_dudak', '#ad6a5b', 0.45, 0.0, '')):
        a_ = N('ShaderNodeAttribute')
        a_.attribute_name = at
        mr = N('ShaderNodeMapRange')
        mr.interpolation_type = 'SMOOTHSTEP'
        mr.inputs['From Min'].default_value = 0.38
        mr.inputs['From Max'].default_value = 0.62
        L(a_.outputs['Fac'], mr.inputs['Value'])
        f = mr.outputs['Result']
        c = N('ShaderNodeRGB')
        c.outputs[0].default_value = kit.srgb(hexcol)
        cc = c.outputs[0]
        if tur == 'sac':  # tellere göre ton farkı
            mm = N('ShaderNodeMix')
            mm.data_type = 'RGBA'
            mm.blend_type = 'MULTIPLY'
            mm.inputs['Factor'].default_value = 0.35
            L(cc, mm.inputs['A'])
            L(nz2.outputs['Color'], mm.inputs['B'])
            cc = mm.outputs['Result']
        mx = N('ShaderNodeMix')
        mx.data_type = 'RGBA'
        L(f, mx.inputs['Factor'])
        L(cur_c, mx.inputs['A'])
        L(cc, mx.inputs['B'])
        cur_c = mx.outputs['Result']
        for val, cur_name in ((rough, 'r'), (sheen, 's')):
            vv = N('ShaderNodeValue')
            vv.outputs[0].default_value = val
            mf = N('ShaderNodeMix')
            mf.data_type = 'FLOAT'
            L(f, mf.inputs['Factor'])
            L(cur_r if cur_name == 'r' else cur_s, mf.inputs['A'])
            L(vv.outputs[0], mf.inputs['B'])
            if cur_name == 'r':
                cur_r = mf.outputs['Result']
            else:
                cur_s = mf.outputs['Result']
        if tur:
            src = nz.outputs['Fac'] if tur == 'kumas' else nz2.outputs['Fac']
            mul = N('ShaderNodeMath')
            mul.operation = 'MULTIPLY'
            L(f, mul.inputs[0])
            L(src, mul.inputs[1])
            if kabart is None:
                kabart = mul.outputs[0]
            else:
                ad_ = N('ShaderNodeMath')
                L(kabart, ad_.inputs[0])
                L(mul.outputs[0], ad_.inputs[1])
                kabart = ad_.outputs[0]
    L(cur_c, b.inputs['Base Color'])
    L(cur_r, b.inputs['Roughness'])
    L(cur_s, b.inputs['Sheen Weight'])
    if kabart is not None:
        bp = N('ShaderNodeBump')
        bp.inputs['Strength'].default_value = 0.25
        L(kabart, bp.inputs['Height'])
        L(bp.outputs['Normal'], b.inputs['Normal'])
    return m


def _sac_kabuk(ad, hexcol):
    """Saç kabuğu malzemesi: dikey tel bantları (dalga dokusu) + parlak şerit, hafif koyu kökler."""
    m = bpy.data.materials.get(ad)
    if m:
        return m
    m = _mat(ad, hexcol, 0.42, 0.6)
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    b.inputs['Coat Weight'].default_value = 0.25
    b.inputs['Coat Roughness'].default_value = 0.3
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (60.0, 60.0, 6.0)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 4.0
    nz.inputs['Detail'].default_value = 10.0
    nz.inputs['Distortion'].default_value = 0.6
    nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    bp = nt.nodes.new('ShaderNodeBump')
    bp.inputs['Strength'].default_value = 0.45
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    mx = nt.nodes.new('ShaderNodeMix')
    mx.data_type = 'RGBA'
    mx.blend_type = 'MULTIPLY'
    mx.inputs['Factor'].default_value = 0.5
    mx.inputs['A'].default_value = kit.srgb(hexcol)
    nt.links.new(nz.outputs['Color'], mx.inputs['B'])
    nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
    return m


def _sac_mat(ad, hexcol):
    m = bpy.data.materials.get(ad)
    if m:
        return m
    m = bpy.data.materials.new(ad)
    m.use_nodes = True
    nt = m.node_tree
    for x in list(nt.nodes):
        nt.nodes.remove(x)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    h = nt.nodes.new('ShaderNodeBsdfHairPrincipled')
    h.parametrization = 'COLOR'
    h.inputs['Color'].default_value = kit.srgb(hexcol)
    h.inputs['Roughness'].default_value = 0.35
    nt.links.new(h.outputs[0], out.inputs['Surface'])
    return m


def _sac(ob, ao, tip, g, v, bolge, kafa):
    """Tel saç (parçacık): kafa derisinden; kadın/kız: topuz ya da at kuyruğu hacmi."""
    uzun = tip in ('kadin', 'kiz')
    if uzun:  # at kuyruğu: başın arkasından omuz arasına inen, uca doğru incelen hacim
        arka = v[(bolge == 'sac')]
        p0 = arka[arka[:, 2] < np.percentile(arka[:, 2], 8)].mean(axis=0)
        p0 = _mh2bl(p0)
        cu = bpy.data.curves.new('AtKuyrugu', 'CURVE')
        cu.dimensions = '3D'
        cu.bevel_depth = 0.032 if tip == 'kadin' else 0.026
        cu.bevel_resolution = 6
        sp = cu.splines.new('BEZIER')
        sp.bezier_points.add(2)
        uz = 0.28 if tip == 'kadin' else 0.2
        pts = [Vector(p0.tolist()) + Vector((0, 0.01, 0.02)), Vector(p0.tolist()) + Vector((0, 0.06, -uz * 0.45)),
               Vector(p0.tolist()) + Vector((0, 0.05, -uz))]
        for bp, p, r in zip(sp.bezier_points, pts, (0.9, 1.0, 0.25)):
            bp.co = p
            bp.handle_left_type = bp.handle_right_type = 'AUTO'
            bp.radius = r
        ko = bpy.data.objects.new('AtKuyrugu', cu)
        kit.link(ko)
        ko.data.materials.append(_sac_kabuk('SacKabuk_' + g['sac'], g['sac']))
        ko.parent = ao  # başa bağlı: baş eğilince at kuyruğu da gelir
        ko.parent_type = 'BONE'
        ko.parent_bone = 'head'
        hb = ao.data.bones['head']
        Mh = hb.matrix_local.copy()
        Mh.translation = hb.tail_local
        ko.matrix_parent_inverse = Mh.inverted()


def insan(tip='erkek', poz='yuru', faz=0.0, giysi=None, konum=(0, 0, 0), yon=0.0, boy=None, ad='Insan'):
    D = _veri()
    g = dict(ust='#3b4d66', alt='#2e2f33', ayakkabi='#1d1d1f', sac='#2a2018', ten='#c99b7a', kol='kisa')
    g.update(giysi or {})
    v = D['v'].copy()
    for h, w in TIP[tip]:
        _hedef(v, h, w)
    # eklem konumları (değişmiş ağdan)
    jt = {k: v[idx].mean(axis=0) for k, idx in D['skel']['joints'].items()}
    # baskın kemik → bölge
    n = len(v)
    agir = np.zeros(n)
    bolge = np.array(['ten'] * n, dtype=object)
    for kemik, lst in D['w'].items():
        a = np.array(lst)
        if len(a) == 0:
            continue
        idx = a[:, 0].astype(np.int64)
        ww = a[:, 1]
        b = 'ten'
        for onek, bb in BOLGE.items():
            if kemik.startswith(onek):
                b = bb
                break
        if kemik == 'root':
            b = 'alt'
        m = ww > agir[idx]
        agir[idx[m]] = ww[m]
        bolge[idx[m]] = b
    bel = (jt['spine04____head'][1] + jt['spine05____head'][1]) / 2  # bel çizgisi: düz yatay sınır
    govde = np.isin(bolge, ['ust', 'alt'])
    bolge[govde & (v[:, 1] >= bel)] = 'ust'
    bolge[govde & (v[:, 1] < bel)] = 'alt'
    if g['kol'] == 'uzun':
        bolge[bolge == 'kol'] = 'ust'
    else:
        bolge[bolge == 'kol'] = 'ten'
    # saç (kafa derisi): kafa üstü ve arkası, alın çizgisinin üstü
    kafa = jt['head____head']
    ust_kafa = v[:, 1].max()
    on_z = v[:, 2]
    hk = ust_kafa - kafa[1]
    esik = 0.24 if tip in ('kadin', 'kiz') else 0.3
    sac = (bolge == 'ten') & (v[:, 1] > kafa[1] + hk * esik) & ~((on_z > kafa[2] + 0.45) & (v[:, 1] < kafa[1] + hk * 0.74))
    bolge[sac] = 'sac'
    # yüz: kaşlar ve dudaklar (boyama)
    eL, eR = jt['eye.L____head'], jt['eye.R____head']
    ey, ez = (eL[1] + eR[1]) / 2, max(eL[2], eR[2])
    kas = (bolge == 'ten') & (v[:, 1] > ey + 0.22) & (v[:, 1] < ey + 0.31) & (on_z > ez) & \
        ((np.abs(v[:, 0] - eL[0]) < 0.3) | (np.abs(v[:, 0] - eR[0]) < 0.3))
    bolge[kas] = 'kas'
    dud = (bolge == 'ten') & (v[:, 1] > ey - 0.95) & (v[:, 1] < ey - 0.86) & (np.abs(v[:, 0]) < 0.19) & (on_z > ez + 0.1)
    bolge[dud] = 'dudak'
    # gömlek eteği: bel çizgisinin biraz altına iner (pantolon kemerini örter)
    etek = jt['spine05____head'][1] - 0.25
    bolge[(bolge == 'alt') & (v[:, 1] >= etek) & (v[:, 1] < bel)] = 'ust'
    # yüzler: gövde + gözler + kirpikler
    gruplar = {'body': None, 'helper-l-eye': 'goz', 'helper-r-eye': 'goz'}
    yuzler = [(f, gr) for f, gr in zip(D['f'], D['g']) if gr in gruplar or gr.startswith('helper-l-eyelashes') or gr.startswith('helper-r-eyelashes')]
    vb = _mh2bl(v)
    me = bpy.data.meshes.new(ad)
    me.from_pydata(vb.tolist(), [], [f for f, _ in yuzler])
    me.update()
    ob = bpy.data.objects.new(ad, me)
    kit.link(ob)
    # bölgeler köşe özniteliği olarak (yumuşak sınır: alt bölümlemede eğriye dönüşür)
    ayak_min = v[bolge == 'ayakkabi', 1].min() if np.any(bolge == 'ayakkabi') else 0
    taban = (bolge == 'ayakkabi') & (v[:, 1] < ayak_min + 0.12)
    katman = {'r_alt': bolge == 'alt', 'r_ust': bolge == 'ust', 'r_ayak': bolge == 'ayakkabi', 'r_taban': taban,
              'r_sac': bolge == 'sac', 'r_kas': bolge == 'kas', 'r_dudak': bolge == 'dudak'}
    for k, mask in katman.items():
        at = me.attributes.new(k, 'FLOAT', 'POINT')
        at.data.foreach_set('value', mask.astype(np.float32))
    ob.data.materials.append(_insan_mat(g))
    ob.data.materials.append(_mat('Goz', '#2a1f18', 0.05))
    ob.data.materials.append(_mat('Kirpik', '#16110d', 0.6))
    fb = [1 if gr in ('helper-l-eye', 'helper-r-eye') else (0 if gr == 'body' else 2) for _, gr in yuzler]
    me.polygons.foreach_set('material_index', np.array(fb, dtype=np.int32))
    me.polygons.foreach_set('use_smooth', np.ones(len(me.polygons), dtype=bool))
    # iskelet
    arm = bpy.data.armatures.new(ad + '_Iskelet')
    ao = bpy.data.objects.new(ad + '_Iskelet', arm)
    kit.link(ao)
    bpy.context.view_layer.objects.active = ao
    bpy.ops.object.mode_set(mode='EDIT')
    bones = D['skel']['bones']
    for name, b in bones.items():
        eb = arm.edit_bones.new(name)
        eb.head = Vector(_mh2bl(jt[b['head']]).tolist())
        eb.tail = Vector(_mh2bl(jt[b['tail']]).tolist())
        if (eb.tail - eb.head).length < 1e-4:
            eb.tail = eb.head + Vector((0, 0, 0.01))
    for name, b in bones.items():
        if b['parent']:
            arm.edit_bones[name].parent = arm.edit_bones[b['parent']]
    bpy.ops.object.mode_set(mode='OBJECT')
    for kemik, lst in D['w'].items():
        vg = ob.vertex_groups.new(name=kemik)
        for i, w in lst:
            vg.add([int(i)], float(w), 'REPLACE')
    # giysi: kas/vücut ayrıntısını sil (yumuşat), kalınlık ver (bol kesim: etekte ve paçada daha bol)
    giyim = np.isin(bolge, ['ust', 'alt', 'ayakkabi'])
    ymin, ymax = v[:, 1].min(), v[:, 1].max()
    yk = (v[:, 1] - ymin) / (ymax - ymin)
    kal = np.zeros(n)
    kal[bolge == 'ust'] = 0.35 + 0.6 * np.clip((bel + 0.6 - v[bolge == 'ust', 1]) / 1.2, 0, 1)
    kal[bolge == 'alt'] = 0.3 + 0.5 * np.clip((0.5 - yk[bolge == 'alt']) / 0.45, 0, 1)
    kal[bolge == 'ayakkabi'] = 0.75
    kal[bolge == 'sac'] = 1.0 if tip in ('kadin', 'kiz') else (0.35 if tip == 'yasli' else 0.6)
    vg_d = ob.vertex_groups.new(name='G_duz')
    vg_k = ob.vertex_groups.new(name='G_kal')
    vg_s = ob.vertex_groups.new(name='G_sac')
    for i in np.nonzero(giyim)[0]:
        vg_d.add([int(i)], 1.0, 'REPLACE')
    for i in np.nonzero(kal > 0)[0]:
        vg_k.add([int(i)], float(kal[i]), 'REPLACE')
    for i in np.nonzero(bolge == 'sac')[0]:
        vg_s.add([int(i)], 1.0, 'REPLACE')
    ls = ob.modifiers.new('KumasDuz', 'SMOOTH')  # kas ve göğüs ayrıntısını sil
    ls.vertex_group = 'G_duz'
    ls.factor = 0.7
    ls.iterations = 14
    dp = ob.modifiers.new('KumasKal', 'DISPLACE')
    dp.vertex_group = 'G_kal'
    dp.strength = 0.026
    dp.mid_level = 0.0
    dp.direction = 'NORMAL'
    md = ob.modifiers.new('Iskelet', 'ARMATURE')
    md.object = ao
    ob.parent = ao
    sb = ob.modifiers.new('Ince', 'SUBSURF')
    sb.levels = 1
    sb.render_levels = 2
    _poz(ao, poz, faz, tip)
    _sac(ob, ao, tip, g, v, bolge, kafa)
    # boy ve konum: ayak tabanı z=0
    zmin = vb[:, 2].min()
    h = vb[:, 2].max() - zmin
    s = (boy or BOY[tip]) / h
    ao.scale = (s, s, s)
    ao.location = (konum[0], konum[1], konum[2] - zmin * s)
    ao.rotation_euler[2] = yon
    return ao, ob


def _don(ao, kemik, eksen, aci):
    """Kemiği iskelet uzayındaki bir eksen etrafında döndür (ebeveyne göre)."""
    pb = ao.pose.bones.get(kemik)
    if pb is None or aci == 0:
        return
    M = pb.bone.matrix_local.to_3x3()
    R = Matrix.Rotation(math.radians(aci), 3, eksen)
    q = (M.inverted() @ R @ M).to_quaternion()
    pb.rotation_mode = 'QUATERNION'
    pb.rotation_quaternion = q @ pb.rotation_quaternion


def _poz(ao, poz, faz, tip):
    X, Z = 'X', 'Z'
    if poz == 'yuru':
        a = math.sin(faz * 2 * math.pi)
        b = math.sin(faz * 2 * math.pi + math.pi)
        _don(ao, 'upperleg01.L', X, -26 * a)
        _don(ao, 'upperleg01.R', X, -26 * b)
        _don(ao, 'lowerleg01.L', X, 32 * max(0.0, -math.cos(faz * 2 * math.pi)) + 6)
        _don(ao, 'lowerleg01.R', X, 32 * max(0.0, math.cos(faz * 2 * math.pi)) + 6)
        _don(ao, 'upperarm01.L', 'Y', 38)
        _don(ao, 'upperarm01.R', 'Y', -38)
        _don(ao, 'upperarm01.L', X, 18 * b)
        _don(ao, 'upperarm01.R', X, 18 * a)
        _don(ao, 'lowerarm01.L', X, -14)
        _don(ao, 'lowerarm01.R', X, -14)
        _don(ao, 'spine03', Z, 4 * a)
    elif poz == 'dur':
        _don(ao, 'upperarm01.L', 'Y', 40)
        _don(ao, 'upperarm01.R', 'Y', -40)
        _don(ao, 'lowerarm01.L', X, -10)
        _don(ao, 'lowerarm01.R', X, -10)
    elif poz in ('bisiklet', 'otur'):
        p = faz * 2 * math.pi
        if poz == 'bisiklet':
            _don(ao, 'spine02', X, -28)
            _don(ao, 'neck01', X, 18)
            _don(ao, 'upperarm01.L', 'Y', 20)
            _don(ao, 'upperarm01.R', 'Y', -20)
            _don(ao, 'upperarm01.L', X, -55)
            _don(ao, 'upperarm01.R', X, -55)
            _don(ao, 'lowerarm01.L', X, -15)
            _don(ao, 'lowerarm01.R', X, -15)
            _don(ao, 'upperleg01.L', X, -62 - 24 * math.sin(p))
            _don(ao, 'upperleg01.R', X, -62 + 24 * math.sin(p))
            _don(ao, 'lowerleg01.L', X, 70 + 30 * math.cos(p))
            _don(ao, 'lowerleg01.R', X, 70 - 30 * math.cos(p))
        else:
            _don(ao, 'upperleg01.L', X, -88)
            _don(ao, 'upperleg01.R', X, -88)
            _don(ao, 'lowerleg01.L', X, 88)
            _don(ao, 'lowerleg01.R', X, 88)
            _don(ao, 'upperarm01.L', 'Y', 38)
            _don(ao, 'upperarm01.R', 'Y', -38)
            _don(ao, 'lowerarm01.L', X, -45)
            _don(ao, 'lowerarm01.R', X, -45)


def _poz_sifirla(ao):
    for pb in ao.pose.bones:
        pb.rotation_mode = 'QUATERNION'
        pb.rotation_quaternion = (1, 0, 0, 0)


def yuru_kare(ao, tip, faz):
    """Yürüyüş döngüsünü kare kare güncelle (ağ yeniden kurulmaz; yalnız kemikler)."""
    _poz_sifirla(ao)
    _poz(ao, 'yuru', faz, tip)


def bisikletli(konum=(0, 0, 0), yon=0.0, bis_renk='#c24a2c', giysi=None, tip='erkek', ad='Bisikletli', pedal=0.6):
    """Bisiklet + sürücü: eller gidon elciklerinde, ayaklar pedalda (IK), kalça selede.
    Döner: (bisiklet ebeveyni, iskelet). İkisi birlikte taşınacaksa bisiklet ebeveyni kullanılır."""
    import sokak as S
    bis = S.bisiklet((0, 0, 0), 0.0, bis_renk, ad + '_Bis', pedal=pedal)
    ao, ob = insan(tip, 'dur', 0.0, giysi, konum=(0, 0, 0), yon=math.pi / 2, ad=ad)
    _poz_sifirla(ao)
    # gövde öne eğik, baş ileri bakar
    # (iskelet uzayında öne = −Y; X ekseni etrafında + açı gövdeyi öne eğer)
    _don(ao, 'spine04', 'X', 12)
    _don(ao, 'spine03', 'X', 18)
    _don(ao, 'spine02', 'X', 16)
    _don(ao, 'neck01', 'X', -22)
    _don(ao, 'head', 'X', -14)
    _don(ao, 'upperarm01.L', 'Y', 50)
    _don(ao, 'upperarm01.R', 'Y', -50)
    bpy.context.view_layer.update()
    # kalça selenin üstüne
    sele = Vector((-0.20, 0.0, 1.005 + 0.07))
    kok = ao.matrix_world @ ao.pose.bones['root'].head
    ao.location += sele - kok
    st = Vector((0.43 + 0.08, 0, 0.88 + 0.05))
    hedefler = {
        'lowerarm02.L': st + Vector((0, 0.25, 0.01)), 'lowerarm02.R': st + Vector((0, -0.25, 0.01)),
    }
    gm = Vector((0.0, 0, 0.3))
    for k, s_, kem in ((0, -1, 'lowerleg02.R'), (math.pi, 1, 'lowerleg02.L')):
        a = pedal + k
        hedefler[kem] = gm + Vector((math.cos(a) * 0.17, s_ * 0.13, math.sin(a) * 0.17 + 0.06))
    kutup = {'lowerarm02.L': Vector((-0.3, 0.7, 0.6)), 'lowerarm02.R': Vector((-0.3, -0.7, 0.6)),
             'lowerleg02.L': Vector((1.2, 0.2, 1.2)), 'lowerleg02.R': Vector((1.2, -0.2, 1.2))}
    for kem, p in hedefler.items():
        e = bpy.data.objects.new(f'{ad}_IK_{kem}', None)
        kit.link(e)
        e.location = p
        e.parent = bis
        pe = bpy.data.objects.new(f'{ad}_Kutup_{kem}', None)
        kit.link(pe)
        pe.location = kutup[kem]
        pe.parent = bis
        c = ao.pose.bones[kem].constraints.new('IK')
        c.target = e
        c.pole_target = pe
        c.pole_angle = math.radians(-90)
        c.chain_count = 4
        c.use_stretch = False
    ao.parent = bis
    bis.location = konum
    bis.rotation_euler[2] = yon
    return bis, ao
