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
    # saç: kafa üstü ve arkası (alın çizgisinin üstü)
    kafa = jt['head____head'] if 'head____head' in jt else v.max(axis=0)
    ust_kafa = v[:, 1].max()
    on_z = v[:, 2]
    sac = (bolge == 'ten') & (v[:, 1] > kafa[1] + (ust_kafa - kafa[1]) * (0.30 if tip in ('kadin', 'kiz') else 0.40)) & ~((on_z > kafa[2] + 0.55) & (v[:, 1] < kafa[1] + (ust_kafa - kafa[1]) * 0.75))
    if tip in ('kadin', 'kiz'):  # uzun saç: ense ve omuz arkası
        sac |= (bolge != 'ayakkabi') & (v[:, 1] > kafa[1] - 1.6) & (v[:, 1] < kafa[1] + 0.4) & (on_z < kafa[2] - 0.35) & (np.abs(v[:, 0]) < 1.0)
    bolge[sac] = 'sac'
    # giysi şişirme (köşe normalleri yaklaşık: merkezden uzaklık yönünde)
    yuzler = [(f, gr) for f, gr in zip(D['f'], D['g']) if gr == 'body']
    vb = _mh2bl(v)
    me = bpy.data.meshes.new(ad)
    me.from_pydata(vb.tolist(), [], [f for f, _ in yuzler])
    me.update()
    # normal yönünde şişir (giysi kalınlığı)
    nrm = np.zeros((len(me.vertices), 3))
    me.vertices.foreach_get('normal', nrm.ravel())
    kal = {'ust': 0.007, 'alt': 0.006, 'ayakkabi': 0.014, 'sac': 0.016, 'ten': 0.0}
    off = np.array([kal.get(b, 0.0) for b in bolge])[:, None] * nrm
    me.vertices.foreach_set('co', (vb + off).ravel())
    me.update()
    ob = bpy.data.objects.new(ad, me)
    kit.link(ob)
    mats = {
        'ten': _mat('Ten_' + g['ten'], g['ten'], 0.45),
        'ust': _mat('Ust_' + g['ust'], g['ust'], 0.8, 0.3),
        'alt': _mat('Alt_' + g['alt'], g['alt'], 0.75, 0.2),
        'ayakkabi': _mat('Ayak_' + g['ayakkabi'], g['ayakkabi'], 0.4),
        'sac': _mat('Sac_' + g['sac'], g['sac'], 0.55, 0.4),
    }
    sira = list(mats)
    for k in sira:
        ob.data.materials.append(mats[k])
    fb = []
    for f, _ in yuzler:
        oy = {}
        for i in f:
            oy[bolge[i]] = oy.get(bolge[i], 0) + 1
        fb.append(sira.index(max(oy, key=oy.get)))
    me.polygons.foreach_set('material_index', np.array(fb, dtype=np.int32))
    me.polygons.foreach_set('use_smooth', np.ones(len(me.polygons), dtype=bool))
    # kullanılmayan köşeleri at
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
    md = ob.modifiers.new('Iskelet', 'ARMATURE')
    md.object = ao
    ob.parent = ao
    _poz(ao, poz, faz, tip)
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
