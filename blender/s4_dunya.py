"""
Sahne 4 — "Ege'den dünyaya": küre, İzmir'den 5 kıtaya lime yaylar.

Kurallar: ülke adı / ülke sınırı / ülke boyalı harita YOK. Yalnız kara
noktaları (Natural Earth, kamu malı) ve kıtalar. Türkiye noktaları lime
(kaynak = biz), yay ulaştığında o kıtanın noktaları yumuşakça aydınlanır.
Kartlarda: 25+ ülke · 5 kıta (sahneden sonra, metinde).

Plan (docs/plan/akt-s5.json): 193 kare (12 kare/sn), kare numarası F. Küre boylamı c(F) ile DÖNER (27° → −22° → 78° → 40°)
ki Amerika ve Okyanusya ön yüzde yansın; kıta ışıması varış noktasından jeodezik dalgayla yayılır.
Giriş   (F0–36)    Kamera İzmir'e bakan küreye yaklaşır; Türkiye lime yanar.
Gelişme (F40–138)  Yaylar sırayla Avrupa, Afrika, Amerika, Asya, Okyanusya'ya uzanır; küre kıtaya döner.
Sonuç   (F126–192) Kamera geri çekilir: tüm yaylar ve kıtalar (F192 = finale ilk karesi, metinsiz).

Kullanım: python s4_dunya.py --variant d|m --frames all|0,40 --out DIR
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector, Matrix  # noqa: E402

FRAMES = 193
R = 1.0
IZMIR = (38.42, 27.14)
# yay hedefleri: kıtanın iç bölgesi (ülke işaretlemez; varışta tüm kıta aydınlanır)
TARGETS = [  # (kıta id, lat, lon, yay başı F, yay bitişi F, varış dalgası bitişi F) — plan kare programı
    (0, 50.5, 12.0, 40, 50, 62),     # Avrupa
    (2, 6.0, 21.0, 46, 59, 71),      # Afrika
    (3, 15.0, -88.0, 53, 73, 88),    # Amerika (Orta Amerika: kara üstü; eski hedef 18°,−86° değil, denizde kalıyordu)
    (1, 40.0, 92.0, 88, 103, 115),   # Asya
    (4, -25.0, 134.0, 102, 124, 138),  # Okyanusya
]
GIRIS_F = 36  # nadir İzmir → küre doğuşu
# küre dönüşü: (F, merkez boylamı c°). Aralar ease-in-out; tepe hız ≤ 33°/sn (12 kare/sn)
BOYLAM = [(0, IZMIR[1]), (36, IZMIR[1]), (73, -22.0), (126, 78.0), (192, 40.0)]
# küre eğimi (F, derece): İzmir enlemi → ekvatora yaklaş (Okyanusya'nın güneyi de görünsün) → hafif geri
EGIM = [(0, 38.42 * 0.62), (73, 18.0), (112, 7.0), (192, 12.0)]
# kamera uzaklığı anahtarları (F, d çarpanı: d0=1 → d1 → d2)
D_ANAHTAR = [(36, 0.0), (132, 1.0), (192, 2.0)]
H_GIRIS = {'d': 0.42, 'm': 0.5}  # girişte İzmir'in üstündeki kamera yüksekliği

YEREL = {}  # varış halkası adı → (kıta noktası, yönelim matrisi)
VARIANTS = {
    'd': dict(res=(1600, 900), lens=50.0, d0=3.5, d1=6.3, d2=9.0),
    'm': dict(res=(768, 1366), lens=36.0, d0=2.9, d1=4.1, d2=5.9),
}


def ll2v(lat, lon, r=R):
    la, lo = math.radians(lat), math.radians(lon)
    return Vector((math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))) * r


def globe_rotation(c=None, egim=None):
    """Boylamı c olan meridyen kameraya (−Y) bakacak, kuzey yukarı kalacak dönüş (varsayılan: İzmir).
    egim: kuzey kutbunun kameraya eğimi (derece); varsayılan İzmir'i merkeze getiren değer."""
    lat, lon = IZMIR
    if c is not None:
        lon = c
    rz = Matrix.Rotation(math.radians(-90 - lon), 4, 'Z')  # boylam → −Y
    rx = Matrix.Rotation(math.radians(lat * 0.62 if egim is None else egim), 4, 'X')  # İzmir'i merkeze yaklaştır (kuzey yukarı)
    return rx @ rz


def dots_object(points, rot):
    n = len(points)
    lat = np.radians(points[:, 0])
    lon = np.radians(points[:, 1])
    pos = np.stack([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)], 1) * (R * 1.002)
    me = bpy.data.meshes.new('Kara')
    me.vertices.add(n)
    me.vertices.foreach_set('co', pos.astype(np.float32).ravel())
    me.attributes.new('renk', 'FLOAT_COLOR', 'POINT')
    me.attributes.new('isik', 'FLOAT', 'POINT')
    me.update()
    ob = bpy.data.objects.new('Kara', me)
    kit.link(ob)
    ob.matrix_world = rot

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

    ng = bpy.data.node_groups.new('NoktaGN', 'GeometryNodeTree')
    ng.interface.new_socket(name='Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    gi = ng.nodes.new('NodeGroupInput')
    go = ng.nodes.new('NodeGroupOutput')
    ico = ng.nodes.new('GeometryNodeMeshIcoSphere')
    ico.inputs['Radius'].default_value = 0.0052
    ico.inputs['Subdivisions'].default_value = 1
    sm = ng.nodes.new('GeometryNodeSetMaterial')
    sm.inputs['Material'].default_value = mat
    ng.links.new(ico.outputs['Mesh'], sm.inputs['Geometry'])
    iop = ng.nodes.new('GeometryNodeInstanceOnPoints')
    ng.links.new(gi.outputs['Geometry'], iop.inputs['Points'])
    ng.links.new(sm.outputs['Geometry'], iop.inputs['Instance'])
    ng.links.new(iop.outputs['Instances'], go.inputs['Geometry'])
    ob.modifiers.new('Noktalar', 'NODES').node_group = ng
    return ob


def globe_body(rot):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=R)
    g = bpy.context.active_object
    g.name = 'Kure'
    bpy.ops.object.shade_smooth()
    mat = bpy.data.materials.new('KureGovde')
    mat.use_nodes = True
    b = mat.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = kit.srgb('#14212a')
    b.inputs['Roughness'].default_value = 0.55
    b.inputs['Coat Weight'].default_value = 0.15
    b.inputs['Coat Roughness'].default_value = 0.35
    g.data.materials.append(mat)
    g.matrix_world = rot
    # atmosfer: kenarda yumuşak slate-mavi parıltı
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=R * 1.045)
    at = bpy.context.active_object
    at.name = 'Atmosfer'
    bpy.ops.object.shade_smooth()
    am = bpy.data.materials.new('Atmosfer')
    am.use_nodes = True
    nt = kit.NT(am.node_tree)
    nt.n.clear()
    out = nt.node('ShaderNodeOutputMaterial', (600, 0))
    lw = nt.node('ShaderNodeLayerWeight', (-400, 0))
    lw.inputs['Blend'].default_value = 0.35
    pw = nt.math('POWER', lw.outputs['Facing'], 3.2, loc=(-200, 0))
    em = nt.node('ShaderNodeEmission', (0, 100))
    em.inputs['Color'].default_value = kit.srgb('#5f86a0')
    em.inputs['Strength'].default_value = 3.0
    tr = nt.node('ShaderNodeBsdfTransparent', (0, -100))
    mx = nt.node('ShaderNodeMixShader', (300, 0))
    nt.link(pw, mx.inputs[0])
    nt.link(tr.outputs[0], mx.inputs[1])
    nt.link(em.outputs[0], mx.inputs[2])
    nt.link(mx.outputs[0], out.inputs['Surface'])
    at.data.materials.append(am)
    at.visible_shadow = False
    return g


def arc_object(name, a, b, rot, mat):
    """Büyük daire yayı, mesafeyle orantılı yükselen; eğri + kalınlık; bevel_factor_end ile büyür."""
    va, vb = ll2v(*a), ll2v(*b)
    ang = va.angle(vb)
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = 0.0042
    cu.bevel_resolution = 3
    cu.use_fill_caps = True
    sp = cu.splines.new('POLY')
    n = 96
    sp.points.add(n - 1)
    for i in range(n):
        u = i / (n - 1)
        # slerp
        p = (va * math.sin((1 - u) * ang) + vb * math.sin(u * ang)) / math.sin(ang)
        h = 1.0 + min(0.075, 0.11 * ang / math.pi) * 4 * u * (1 - u) + 0.004
        p = p.normalized() * R * h
        sp.points[i].co = (p.x, p.y, p.z, 1.0)
    ob = bpy.data.objects.new(name, cu)
    kit.link(ob)
    ob['pts'] = [c for i in range(n) for c in sp.points[i].co[:3]]
    ob.data.materials.append(mat)
    ob.matrix_world = rot
    cu.bevel_factor_mapping_end = 'SPLINE'
    cu.bevel_factor_end = 0.0
    return ob


def build(variant):
    kit.reset()
    v = VARIANTS[variant]
    kit.setup_render(*v['res'], samples=ARGS.samples, threshold=0.02)
    world = kit.studio_world(hdri='studio.exr', hdri_strength=0.3)
    kit.replace_reflection_env(world, 1.0)
    floor = kit.box('Zemin', (200, 200, 0.1), (0, 0, -1.65), kit.glossy_floor())
    # plan: zemin lime halkası ve KonturLime ışığı kaldırıldı (kürede lime sızıntısı olmasın; lime yalnız yay/fabrika iğnesi)

    rot = globe_rotation()
    pts = np.array(json.load(open(os.path.join(kit.TEX_DIR, 'kara_noktalari.json'))), dtype=np.float32)
    globe_body(rot)
    dots = dots_object(pts, rot)
    arc_mat = kit.emission_material('Yay', kit.LIME_HI, 7.0)
    arcs = [arc_object(f'Yay{i}', IZMIR, (T[1], T[2]), rot, arc_mat) for i, T in enumerate(TARGETS)]
    # yay başı: ilerleyen ışık damlası (yolculuk hissi)
    bas_mat = kit.emission_material('YayBasi', (1.0, 1.0, 0.92, 1.0), 40.0)
    for i, a in enumerate(arcs):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.011)
        b = bpy.context.active_object
        b.name = f'YayBasi{i}'
        b.data.materials.append(bas_mat)
        b.visible_shadow = False
        a['bas'] = b.name
    # varış halkaları (kıtada yumuşak dalga)
    pulses = []
    for i, T in enumerate(TARGETS):
        p = kit.halo_ring(f'Varis{i}', radius=0.035, width=0.003, strength=6.0, segments=64)
        n = ll2v(T[1], T[2], R * 1.004)
        YEREL[p.name] = (n, n.to_track_quat('Z', 'Y').to_matrix().to_4x4())  # küre dönünce rot @ T @ yerel yeniden kurulur
        p.matrix_world = rot @ Matrix.Translation(n) @ YEREL[p.name][1]
        pulses.append(p)

    k = kit.area_light('Ana', (-3.5, -4.0, 3.2), (0, 0, 0), 3.2, 200, (1.0, 0.97, 0.94), shape='DISK')
    kit.aim(k, (0, 0, 0))
    r1 = kit.area_light('Kontur', (2.6, 3.4, 1.6), (0, 0, 0), (0.6, 3.0), 380, (0.86, 0.93, 1.0))
    kit.aim(r1, (0, 0, 0))
    r1.visible_glossy = False
    # Sinematik: arka planda yıldız alanı, ışıldayan yaylar ve atmosfer
    kit.dust('Yildiz', count=1400, bounds=((-26, 26), (6, 14), (-12, 15)), seed=23, size=(0.005, 0.014), strength=2.2)
    kit.sinematik(bloom=0.4, esik=1.4, boyut=0.6)
    cam = kit.camera('Kamera', lens=v['lens'], loc=(0, -v['d0'], 0.3), target=(0, 0, 0), fstop=8.0)
    return cam, dots, pts, arcs, pulses


def anahtar(F, keys):
    """(F, değer) anahtarları arasında ease-in-out ara değer."""
    if F <= keys[0][0]:
        return keys[0][1]
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if F <= f1:
            return kit.lerp(v0, v1, kit.smoother(kit.seg(F, f0, f1)))
    return keys[-1][1]


def cam_pose(F, variant):
    v = VARIANTS[variant]
    k = anahtar(F, D_ANAHTAR)  # 0..1: d0→d1, 1..2: d1→d2
    d = kit.lerp(v['d0'], v['d1'], min(k, 1.0)) if k <= 1.0 else kit.lerp(v['d1'], v['d2'], k - 1.0)
    t = F / (FRAMES - 1)
    yaw = math.radians(kit.lerp(-6, 14, kit.smoother(t)))
    pitch = math.radians(kit.lerp(10, 18, kit.smooth(kit.seg(t, 0.5, 1.0))))
    tz = kit.lerp(0.25, -0.05, kit.smooth(kit.seg(t, 0.4, 1.0)))
    target = Vector((0, 0, tz))
    dirv = Vector((math.sin(yaw) * math.cos(pitch), -math.cos(yaw) * math.cos(pitch), math.sin(pitch)))
    return target + dirv * d, target


def gorunur(cam_loc, rot, lat, lon):
    """Küre noktası (lat, lon) kameraya bakan yüzde mi? (ufuk testi: arka yüzdeki çapa null olur)"""
    n = (rot.to_3x3() @ ll2v(lat, lon, 1.0)).normalized()
    return n.dot((cam_loc - rot @ ll2v(lat, lon, R)).normalized()) > 0.08


def main():
    os.makedirs(ARGS.out, exist_ok=True)
    cam, dots, pts, arcs, pulses = build(ARGS.variant)
    rot0 = globe_rotation()
    src = kit.halo_ring('IzmirHalka', radius=0.045, width=0.004, strength=7.0, segments=96)
    n_ = ll2v(*IZMIR, R * 1.004)
    src.matrix_world = rot0 @ Matrix.Translation(n_) @ n_.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    kita = pts[:, 2].astype(int)
    base = np.tile(np.array([0.78, 0.80, 0.80, 1.0], dtype=np.float32), (len(pts), 1))
    lime = np.array(kit.LIME_HI, dtype=np.float32)
    # varış dalgası: kıtanın noktaları, varış noktasına jeodezik uzaklıkla sırayla yanar
    la_, lo_ = np.radians(pts[:, 0]), np.radians(pts[:, 1])
    uvec = np.stack([np.cos(la_) * np.cos(lo_), np.cos(la_) * np.sin(lo_), np.sin(la_)], 1)
    dalga = []
    for (kid, lat, lon, _, _, _) in TARGETS:
        tv = np.array(ll2v(lat, lon, 1.0), dtype=np.float32)
        ang = np.arccos(np.clip(uvec @ tv, -1, 1))
        m = kita == kid
        dn = np.zeros(len(pts), dtype=np.float32)
        if m.any():
            dn[m] = ang[m] / max(float(ang[m].max()), 1e-6)
        dalga.append((m, dn))
    frames = pass_order(FRAMES) if ARGS.frames == 'all' else [int(x) for x in ARGS.frames.split(',')]
    meta_path = os.path.join(ARGS.out, 'meta.json')
    meta = {'frames': FRAMES, 'res': VARIANTS[ARGS.variant]['res'], 'hotspots': {}}
    if os.path.exists(meta_path):  # kısmi işler (kaba/ara/ince geçiş) birbirinin noktalarını silmesin
        import json
        _eski = json.load(open(meta_path, encoding='utf-8'))
        if _eski.get('frames') == FRAMES:
            meta['hotspots'].update(_eski.get('hotspots', {}))
    for f in frames:
        # küre dönüşü: tüm küreye bağlı nesneler aynı dönüşle (Amerika ve Okyanusya ön yüzde yansın)
        rot = globe_rotation(anahtar(f, BOYLAM), anahtar(f, EGIM))
        dots.matrix_world = rot
        src.matrix_world = rot @ Matrix.Translation(n_) @ n_.to_track_quat('Z', 'Y').to_matrix().to_4x4()
        for ob in arcs:
            ob.matrix_world = rot
        col = base.copy()
        glow = np.full(len(pts), 0.05, dtype=np.float32)
        # Türkiye: kaynak, lime
        k_tr = 1.0  # tek akış: sahne 3'ün lime saha halkasıyla eşleşir — Türkiye baştan yanık
        tr = kita == 5
        col[tr] = base[tr] * (1 - k_tr) + lime * k_tr
        glow[tr] = 0.05 + 1.3 * k_tr
        for i, (kid, lat, lon, fa, fb, fw) in enumerate(TARGETS):
            u = kit.seg(f, fa, fb)
            arcs[i].data.bevel_factor_end = kit.ease_in_out(u)
            arcs[i].hide_render = u <= 0.0
            bas = bpy.data.objects[arcs[i]['bas']]
            ue = kit.ease_in_out(u)
            bas.hide_render = not (0.0 < u < 1.0)
            pp = list(arcs[i]['pts'])
            m_ = len(pp) // 3
            x = ue * (m_ - 1)
            j = min(m_ - 2, int(x))
            fr = x - j
            pa = Vector(pp[3 * j:3 * j + 3])
            pb = Vector(pp[3 * j + 3:3 * j + 6])
            bas.location = arcs[i].matrix_world @ pa.lerp(pb, fr)
            m, dn = dalga[i]
            ti = fb + dn[m] * max(fw - fb - 5, 1)
            glow[m] = 0.05 + 0.75 * np.array([kit.smooth(kit.seg(f, a_, a_ + 5)) for a_ in ti], dtype=np.float32)
            pr = kit.seg(f, fb - 1, fb + 10)
            yn, yq = YEREL[pulses[i].name]
            pulses[i].matrix_world = rot @ Matrix.Translation(yn) @ yq
            pulses[i].hide_render = not (0 < pr < 1)
            sc = 0.5 + 1.8 * pr
            pulses[i].scale = (sc, sc, 1)
            pulses[i].data.materials[0].node_tree.nodes['Emission'].inputs['Strength'].default_value = 6.0 * (1 - pr)
        me = dots.data
        me.attributes['renk'].data.foreach_set('color', col.ravel())
        me.attributes['isik'].data.foreach_set('value', glow)
        me.update()
        loc, target = cam_pose(f, ARGS.variant)
        w = kit.smoother(kit.seg(f, 0, GIRIS_F))
        if f < GIRIS_F:
            # giriş: İzmir'e tepeden yakın plan (sahne 3 çıkışındaki tepeden şantiye karesiyle eşleşir),
            # sonra küre açılır
            pA = rot @ ll2v(*IZMIR, R)
            nA = pA.normalized()
            dB = loc - target
            dirv = nA.lerp(dB.normalized(), w).normalized()
            dist = math.exp(kit.lerp(math.log(H_GIRIS[ARGS.variant]), math.log(dB.length), w))
            target = pA.lerp(target, w)
            loc = target + dirv * dist
        cam.location = loc
        kit.aim(cam, target)
        kit.kaydir(cam, ARGS.variant, 1.0)
        cam.data.dof.focus_distance = max(0.1, (target - loc).length - R * 0.6 * (1 if f >= GIRIS_F else w))
        # kaynak halkası: İzmir'de, girişte parlak, küre açılınca söner
        src.hide_render = f > 61
        src.data.materials[0].node_tree.nodes['Emission'].inputs['Strength'].default_value = 7.0 * (1 - kit.smooth(kit.seg(f, 30, 61)))
        hs = {}
        pts_w = {}
        if f <= 60 and gorunur(cam.location, rot, *IZMIR):
            pts_w['kaynak'] = rot @ ll2v(*IZMIR, R * 1.01)
        if f >= 125 and gorunur(cam.location, rot, 0.0, -30.0):
            pts_w['kitalar'] = rot @ ll2v(0.0, -30.0, R * 1.01)  # Atlantik açığı: kıta kartı noktası
        # varış çapaları: ufuk testiyle (arka yüzdeki çapa yok)
        for (kid, lat, lon, fa, fb, fw), ad in zip(TARGETS, ('avrupa', 'afrika', 'amerika', 'asya', 'okyanusya')):
            if f >= fb and gorunur(cam.location, rot, lat, lon):
                pts_w['v_' + ad] = rot @ ll2v(lat, lon, R * 1.01)
        if pts_w:
            proj = kit.project(cam, list(pts_w.values()))
            hs = {k: p for k, p in zip(pts_w.keys(), proj) if p}
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
