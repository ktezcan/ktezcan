"""
Sahne 4 — "Ege'den dünyaya": küre, İzmir'den 5 kıtaya lime yaylar.

Kurallar: ülke adı / ülke sınırı / ülke boyalı harita YOK. Yalnız kara
noktaları (Natural Earth, kamu malı) ve kıtalar. Türkiye noktaları lime
(kaynak = biz), yay ulaştığında o kıtanın noktaları yumuşakça aydınlanır.
Kartlarda: 25+ ülke · 5 kıta (sahneden sonra, metinde).

Giriş   (0,00–0,25) Kamera İzmir'e bakan küreye yaklaşır; Türkiye lime yanar.
Gelişme (0,22–0,72) Yaylar sırayla Avrupa, Afrika, Asya, Amerika, Okyanusya'ya uzanır.
Sonuç   (0,72–1,00) Kamera geri çekilir: tüm yaylar ve kıtalar, zeminde lime hale.

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

FRAMES = 72
R = 1.0
IZMIR = (38.42, 27.14)
# yay hedefleri: kıtanın iç bölgesi (ülke işaretlemez; varışta tüm kıta aydınlanır)
TARGETS = [  # (kıta id, lat, lon, başlangıç t)
    (0, 50.5, 12.0, 0.24),
    (2, 6.0, 21.0, 0.32),
    (1, 40.0, 92.0, 0.40),
    (3, 18.0, -86.0, 0.48),
    (4, -25.0, 134.0, 0.56),
]
ARC_DUR = 0.14

VARIANTS = {
    'd': dict(res=(1600, 900), lens=50.0, d0=3.5, d1=5.0),
    'm': dict(res=(768, 1366), lens=36.0, d0=3.9, d1=6.0),
}


def ll2v(lat, lon, r=R):
    la, lo = math.radians(lat), math.radians(lon)
    return Vector((math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))) * r


def globe_rotation():
    """İzmir kameraya (−Y) bakacak, kuzey yukarı kalacak dönüş."""
    lat, lon = IZMIR
    rz = Matrix.Rotation(math.radians(-90 - lon), 4, 'Z')  # boylam → −Y
    rx = Matrix.Rotation(math.radians(lat * 0.62), 4, 'X')  # İzmir'i merkeze yaklaştır (kuzey yukarı)
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
    em.inputs['Strength'].default_value = 2.2
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
    ring = kit.halo_ring('Hale', radius=1.55, width=0.008, strength=5.0, z=0.0)
    ring.location = (0, 0, -1.599)

    rot = globe_rotation()
    pts = np.array(json.load(open(os.path.join(kit.TEX_DIR, 'kara_noktalari.json'))), dtype=np.float32)
    globe_body(rot)
    dots = dots_object(pts, rot)
    arc_mat = kit.emission_material('Yay', kit.LIME_HI, 7.0)
    arcs = [arc_object(f'Yay{i}', IZMIR, (lat, lon), rot, arc_mat) for i, (_, lat, lon, _) in enumerate(TARGETS)]
    # varış halkaları (kıtada yumuşak dalga)
    pulses = []
    for i, (_, lat, lon, _) in enumerate(TARGETS):
        p = kit.halo_ring(f'Varis{i}', radius=0.035, width=0.003, strength=6.0, segments=64)
        n = ll2v(lat, lon, R * 1.004)
        p.matrix_world = rot @ Matrix.Translation(n) @ n.to_track_quat('Z', 'Y').to_matrix().to_4x4()
        pulses.append(p)

    k = kit.area_light('Ana', (-3.5, -4.0, 3.2), (0, 0, 0), 3.2, 200, (1.0, 0.97, 0.94), shape='DISK')
    kit.aim(k, (0, 0, 0))
    r1 = kit.area_light('Kontur', (2.6, 3.4, 1.6), (0, 0, 0), (0.6, 3.0), 380, (0.86, 0.93, 1.0))
    kit.aim(r1, (0, 0, 0))
    r2 = kit.area_light('KonturLime', (-3.0, 2.8, -0.4), (0, 0, 0), (0.5, 2.6), 160, kit.LIME_HI)
    kit.aim(r2, (0, 0, 0))
    for ob in (r1, r2):
        ob.visible_glossy = False
    cam = kit.camera('Kamera', lens=v['lens'], loc=(0, -v['d0'], 0.3), target=(0, 0, 0), fstop=8.0)
    return cam, dots, pts, arcs, pulses


def cam_pose(t, variant):
    v = VARIANTS[variant]
    d = kit.lerp(v['d0'], v['d1'], kit.smoother(kit.seg(t, 0.55, 1.0)))
    yaw = math.radians(kit.lerp(-6, 14, kit.smoother(t)))
    pitch = math.radians(kit.lerp(10, 18, kit.smooth(kit.seg(t, 0.5, 1.0))))
    tz = kit.lerp(0.25, -0.05, kit.smooth(kit.seg(t, 0.4, 1.0)))
    target = Vector((0, 0, tz))
    dirv = Vector((math.sin(yaw) * math.cos(pitch), -math.cos(yaw) * math.cos(pitch), math.sin(pitch)))
    return target + dirv * d, target


def main():
    os.makedirs(ARGS.out, exist_ok=True)
    cam, dots, pts, arcs, pulses = build(ARGS.variant)
    kita = pts[:, 2].astype(int)
    base = np.tile(np.array([0.78, 0.80, 0.80, 1.0], dtype=np.float32), (len(pts), 1))
    lime = np.array(kit.LIME_HI, dtype=np.float32)
    frames = pass_order(FRAMES) if ARGS.frames == 'all' else [int(x) for x in ARGS.frames.split(',')]
    meta_path = os.path.join(ARGS.out, 'meta.json')
    meta = {'frames': FRAMES, 'res': VARIANTS[ARGS.variant]['res'], 'hotspots': {}}
    for f in frames:
        t = f / (FRAMES - 1)
        col = base.copy()
        glow = np.full(len(pts), 0.05, dtype=np.float32)
        # Türkiye: kaynak, lime
        k_tr = kit.smooth(kit.seg(t, 0.06, 0.18))
        tr = kita == 5
        col[tr] = base[tr] * (1 - k_tr) + lime * k_tr
        glow[tr] = 0.05 + 1.3 * k_tr
        for i, (kid, lat, lon, ts) in enumerate(TARGETS):
            u = kit.seg(t, ts, ts + ARC_DUR)
            arcs[i].data.bevel_factor_end = kit.ease_in_out(u)
            arcs[i].hide_render = u <= 0.0
            arrive = kit.smooth(kit.seg(t, ts + ARC_DUR * 0.85, ts + ARC_DUR + 0.08))
            m = kita == kid
            glow[m] = 0.05 + 0.75 * arrive
            pr = kit.seg(t, ts + ARC_DUR * 0.85, ts + ARC_DUR + 0.12)
            pulses[i].hide_render = not (0 < pr < 1)
            sc = 0.5 + 1.8 * pr
            pulses[i].scale = (sc, sc, 1)
            pulses[i].data.materials[0].node_tree.nodes['Emission'].inputs['Strength'].default_value = 6.0 * (1 - pr)
        me = dots.data
        me.attributes['renk'].data.foreach_set('color', col.ravel())
        me.attributes['isik'].data.foreach_set('value', glow)
        me.update()
        loc, target = cam_pose(t, ARGS.variant)
        cam.location = loc
        kit.aim(cam, target)
        cam.data.dof.focus_distance = (target - loc).length - R * 0.6
        rot = dots.matrix_world
        hs = {}
        if t >= 0.12:
            pts_w = {'kaynak': rot @ ll2v(*IZMIR, R * 1.01)}
            if t >= 0.80:
                pts_w['kitalar'] = rot @ ll2v(18.0, -40.0, R * 1.01)
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
