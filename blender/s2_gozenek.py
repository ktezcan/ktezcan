"""
Sahne 2 — "Gözeneğe dalış": gazbetonun hücresel iç yapısı.

Makro ölçek: 1 Blender birimi = 1 cm. 12 mm'lik bir numune küpü:
gerçekçi gözenek dağılımı (0,2–3 mm), pürüzlü hücre duvarları.
Kesilmiş yüzden (Sahne 1'in son karesiyle eşleşen gri gözenekli yüzey)
kamera büyük bir yüzey gözeneğine girer: kapalı bir hava hücresi; küçük
bir pencereden komşu hücrenin zayıf lime ışığı görünür (hapsolmuş hava).
Sonra geri çekilir, yükselir ve numune küpünün tamamını gösterir.

Giriş   (0,00–0,28) Yüzeye yaklaşma, büyük gözeneğe giriş.
Gelişme (0,28–0,62) Hücrenin içi — kapalı hava hücresi, ince duvarlar.
Sonuç   (0,62–1,00) Geri çekilme, numune küpü stüdyoda (λ 0,08 · A1 kartları sahneden sonra).

Geometri: işaretli uzaklık alanı (küp − gözenek küreleri, pürüzlü) →
marching cubes (scikit-image). Önbellek: tex/gozenek_mesh.npz

Kullanım: python s2_gozenek.py --variant d|m --frames all|0,40 --out DIR
"""
import argparse
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

FRAMES = 72
# Numune: x ∈ [−0.6, 0.6], y ∈ [0, 1.2] (derinlik; ön yüz y = 0), z ∈ [−0.6, 0.6]  (cm)
BX, BY0, BY1, BZ = 0.6, 0.0, 1.2, 0.6
VOX = 0.0075
# Dalış hücresi (yüzeyde açılan büyük gözenek) ve penceresinden görünen komşu hücre
CHAIN = [((0.0, 0.07, 0.03), 0.17), ((0.12, 0.29, 0.09), 0.12)]

VARIANTS = {
    'd': dict(res=(1600, 900), lens=32.0),
    'm': dict(res=(768, 1366), lens=24.0),
}


def value_noise3(shape, cells, rng):
    """Döşenmeyen 3B değer gürültüsü (üç doğrusal ara değer)."""
    g = rng.random((cells + 2, cells + 2, cells + 2)).astype(np.float32)
    idx = [np.linspace(0, cells, n, dtype=np.float32) for n in shape]
    ix, iy, iz = np.meshgrid(*idx, indexing='ij')
    x0, y0, z0 = ix.astype(int), iy.astype(int), iz.astype(int)
    fx, fy, fz = ix - x0, iy - y0, iz - z0
    fx, fy, fz = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy), fz * fz * (3 - 2 * fz)

    def at(dx, dy, dz):
        return g[x0 + dx, y0 + dy, z0 + dz]
    c00 = at(0, 0, 0) * (1 - fx) + at(1, 0, 0) * fx
    c10 = at(0, 1, 0) * (1 - fx) + at(1, 1, 0) * fx
    c01 = at(0, 0, 1) * (1 - fx) + at(1, 0, 1) * fx
    c11 = at(0, 1, 1) * (1 - fx) + at(1, 1, 1) * fx
    c0 = c00 * (1 - fy) + c10 * fy
    c1 = c01 * (1 - fy) + c11 * fy
    return (c0 * (1 - fz) + c1 * fz) * 2 - 1


def build_sdf(seed=1907):
    rng = np.random.default_rng(seed)
    pad = 3 * VOX
    xs = np.arange(-BX - pad, BX + pad, VOX, dtype=np.float32)
    ys = np.arange(BY0 - pad, BY1 + pad, VOX, dtype=np.float32)
    zs = np.arange(-BZ - pad, BZ + pad, VOX, dtype=np.float32)
    shape = (len(xs), len(ys), len(zs))
    M = np.full(shape, 1e3, dtype=np.float32)

    spheres = [(np.array(c), r) for c, r in CHAIN]
    # zincir yolundan uzak rastgele gözenekler (azalan yarıçap)
    path = np.array([c for c, _ in CHAIN])

    def path_dist(p):
        best = 1e9
        for a, b in zip(path, path[1:]):
            ab = b - a
            t = np.clip(np.dot(p - a, ab) / np.dot(ab, ab), 0, 1)
            best = min(best, np.linalg.norm(p - (a + ab * t)))
        return best

    placed = list(spheres)
    C = np.zeros((20000, 3))
    R = np.zeros(20000)
    n = 0
    for c, r in spheres:
        C[n], R[n] = c, r
        n += 1
    tries = 26000
    for k in range(tries):
        tk = k / tries
        r = 0.135 * (0.012 / 0.135) ** (tk ** 0.55) * (0.85 + 0.3 * rng.random())
        c = np.array([rng.uniform(-BX - 0.05, BX + 0.05), rng.uniform(BY0 - 0.04, BY1 + 0.05), rng.uniform(-BZ - 0.05, BZ + 0.05)])
        # yüzeye 'zar zor' değen gözenekler kesilince tırtıklı kara yarık bırakır:
        # ya belirgin açılsın ya hiç açılmasın
        for ax, lo_, hi_ in ((0, -BX, BX), (1, BY0, BY1), (2, -BZ, BZ)):
            for wall, sgn in ((lo_, 1), (hi_, -1)):
                gap_ = (c[ax] - wall) * sgn - r  # >0: duvar kalınlığı, <0: açılma derinliği
                if 0 <= gap_ < 0.012:
                    c[ax] += sgn * (0.012 - gap_)
                elif -0.35 * r < gap_ < 0:
                    c[ax] -= sgn * (0.35 * r + gap_)
        if path_dist(c) < r + 0.05:
            continue
        d = np.linalg.norm(C[:n] - c, axis=1)
        if np.all(d >= (R[:n] + r) + 0.0075):  # kapalı hücreler, delinmeyen duvarlar (gerçek gazbeton)
            C[n], R[n] = c, r
            n += 1
            placed.append((c, r))
    print('gozenek sayisi', len(placed))

    for c, r in placed:
        lo = [np.searchsorted(a, v - r - VOX) for a, v in zip((xs, ys, zs), c)]
        hi = [np.searchsorted(a, v + r + VOX) for a, v in zip((xs, ys, zs), c)]
        if any(h <= l for l, h in zip(lo, hi)):
            continue
        sx, sy, sz = xs[lo[0]:hi[0]], ys[lo[1]:hi[1]], zs[lo[2]:hi[2]]
        d = np.sqrt((sx[:, None, None] - c[0]) ** 2 + (sy[None, :, None] - c[1]) ** 2 + (sz[None, None, :] - c[2]) ** 2) - r
        sub = M[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
        np.minimum(sub, d.astype(np.float32), out=sub)

    # küp SDF
    qx = np.abs(xs)[:, None, None] - BX
    qy = np.abs(ys - (BY0 + BY1) / 2)[None, :, None] - (BY1 - BY0) / 2
    qz = np.abs(zs)[None, None, :] - BZ
    q = np.maximum(np.maximum(qx, qy), qz)
    rough = value_noise3(shape, 36, rng) * 0.0024 + value_noise3(shape, 110, rng) * 0.0010
    f = np.maximum(q, -(M + rough))
    return f, (xs[0], ys[0], zs[0]), placed


def get_mesh(cache):
    if os.path.exists(cache):
        z = np.load(cache)
        return z['v'], z['f'], z['n'], z['pores']
    from skimage.measure import marching_cubes
    f, origin, placed = build_sdf()
    v, fa, n, _ = marching_cubes(f, level=0.0, spacing=(VOX, VOX, VOX), step_size=1, allow_degenerate=False, gradient_direction='ascent')
    v = v + np.array(origin)
    pores = np.array([[c[0], c[1], c[2], r] for c, r in placed], dtype=np.float32)
    np.savez_compressed(cache, v=v.astype(np.float32), f=fa.astype(np.int32), n=n.astype(np.float32), pores=pores)
    return v, fa, n, pores


def macro_material():
    mat = bpy.data.materials.new('GazbetonMakro')
    mat.use_nodes = True
    nt = kit.NT(mat.node_tree)
    bsdf = nt.n.get('Principled BSDF')
    # ince matris taneciği: küçük ölçekli gürültü kabartması
    tc = nt.node('ShaderNodeTexCoord', (-900, -300))
    nz = nt.node('ShaderNodeTexNoise', (-700, -300))
    nz.inputs['Scale'].default_value = 26.0
    nz.inputs['Detail'].default_value = 8.0
    nz.inputs['Roughness'].default_value = 0.65
    nt.link(tc.outputs['Object'], nz.inputs['Vector'])
    bmp = nt.node('ShaderNodeBump', (-300, -300))
    bmp.inputs['Strength'].default_value = 0.45
    bmp.inputs['Distance'].default_value = 0.02
    nt.link(nz.outputs['Fac'], bmp.inputs['Height'])
    nt.link(bmp.outputs['Normal'], bsdf.inputs['Normal'])
    # içbükey bölgeler biraz koyu (sivrilik)
    geo = nt.node('ShaderNodeNewGeometry', (-900, 200))
    mr = nt.node('ShaderNodeMapRange', (-650, 200))
    nt.link(geo.outputs['Pointiness'], mr.inputs['Value'])
    mr.inputs['From Min'].default_value = 0.44
    mr.inputs['From Max'].default_value = 0.56
    mr.inputs['To Min'].default_value = 0.78
    mr.inputs['To Max'].default_value = 1.0
    col = nt.node('ShaderNodeMix', (-350, 200), data_type='RGBA', blend_type='MULTIPLY')
    col.inputs['Factor'].default_value = 1.0
    col.inputs['A'].default_value = kit.srgb('#c4c3be')
    cc = nt.node('ShaderNodeCombineColor', (-500, 100))
    for i in range(3):
        nt.link(mr.outputs['Result'], cc.inputs[i])
    nt.link(cc.outputs[0], col.inputs['B'])
    nt.link(col.outputs['Result'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.92
    bsdf.inputs['Specular IOR Level'].default_value = 0.3
    return mat


def build(variant):
    kit.reset()
    v = VARIANTS[variant]
    kit.setup_render(*v['res'], samples=ARGS.samples, threshold=0.02, bounces=(6, 4, 2, 2))
    world = kit.studio_world(hdri='studio.exr', hdri_strength=0.3, rot=math.radians(30))
    kit.replace_reflection_env(world, 1.0)

    cache = os.path.join(kit.TEX_DIR, 'gozenek_mesh.npz')
    verts, faces, normals, pores = get_mesh(cache)
    me = bpy.data.meshes.new('Numune')
    me.vertices.add(len(verts))
    me.vertices.foreach_set('co', verts.ravel())
    me.loops.add(len(faces) * 3)
    me.loops.foreach_set('vertex_index', faces.ravel())
    me.polygons.add(len(faces))
    me.polygons.foreach_set('loop_start', np.arange(0, len(faces) * 3, 3, dtype=np.int32))
    me.polygons.foreach_set('use_smooth', np.ones(len(faces), dtype=bool))
    me.update(calc_edges=True)
    me.validate()
    ob = bpy.data.objects.new('Numune', me)
    kit.link(ob)
    ob.data.materials.append(macro_material())

    # stüdyo zemini ve hale (makro ölçek: 1 birim = 1 cm)
    floor = kit.box('Zemin', (200, 200, 0.1), (0, 0.6, -BZ - 0.55), kit.glossy_floor())
    ring = kit.halo_ring('Hale', radius=1.25, width=0.012, strength=5.0, z=0.0)
    ring.location = (0, 0.6, -BZ - 0.499)

    # ışık: yumuşak ana ışık (gözeneğin ağzından içeri düşer) + arkadan kontur
    k = kit.area_light('Ana', (-2.6, -3.4, 3.2), (0, 0, 0), (3.0, 2.0), 900, (1.0, 0.975, 0.95))
    kit.aim(k, (0, 0.2, 0))
    r1 = kit.area_light('Kontur', (2.2, 3.6, 1.6), (0, 0, 0), (0.5, 3.0), 520, (0.86, 0.93, 1.0))
    kit.aim(r1, (0, 0.6, 0))
    r1.visible_glossy = False
    r2 = kit.area_light('KonturLime', (-2.4, 3.2, 0.6), (0, 0, 0), (0.4, 2.4), 300, kit.LIME_HI)
    kit.aim(r2, (0, 0.6, 0))
    r2.visible_glossy = False
    # komşu hücrede hapsolmuş hava: pencereden görünen zayıf lime parıltı
    c1, rr1 = CHAIN[1]
    ld = bpy.data.lights.new('Hava', 'POINT')
    ld.energy = 0.10
    ld.color = (0.80, 0.92, 0.45)
    ld.shadow_soft_size = 0.025
    lo = bpy.data.objects.new('Hava', ld)
    # hücrenin arka-üst köşesinde: duvarlarda ışık düşüşü (düz disk görünmez)
    lo.location = (c1[0] + 0.05, c1[1] + 0.07, c1[2] + 0.05)
    lo.visible_camera = False
    kit.link(lo)
    front = kit.area_light('OnDolgu', (0.4, -3.2, 0.8), (0, 0, 0), (2.5, 2.5), 140, (0.95, 0.97, 1.0))
    kit.aim(front, (0, 0, 0))  # gözenek içleri simsiyah kalmasın (gerçekte sekme ışığı var)
    fill = kit.area_light('Dolgu', (0.0, -0.6, 0.0), (0, 0, 0), 0.04, 0.02, (1.0, 0.98, 0.95))
    kit.aim(fill, (0, 1.0, 0))
    cam = kit.camera('Kamera', lens=50, loc=(0, -3, 0), target=(0, 1, 0), fstop=11.0)
    cam.data.clip_start = 0.002
    return cam, fill


def cam_pose(t, variant):
    """(konum, hedef, objektif mm). Ön yüz ekranı doldurarak başlar (Sahne 1 sonuyla eşleşen kesme)."""
    c0 = Vector(CHAIN[0][0])
    c1 = Vector(CHAIN[0][0]).lerp(Vector(CHAIN[1][0]), 1.0)
    portrait = variant == 'm'
    d0 = 1.45 if not portrait else 0.95
    far = 4.6 if not portrait else 5.8
    lens_in = 15.0 if not portrait else 12.0
    keys = [
        (0.00, Vector((0.0, -d0, 0.02)), Vector((0.0, 0.0, 0.02)), 50.0),
        (0.16, Vector((0.0, -0.55, 0.03)), c0, 42.0),
        (0.28, Vector((0.0, -0.10, 0.03)), c0 + Vector((0, 0.2, 0)), 24.0),
        (0.38, c0 + Vector((0.0, -0.03, 0.0)), c1, lens_in),
        (0.50, c0 + Vector((0.02, -0.01, -0.02)), c0 + Vector((-0.16, 0.13, 0.15)), lens_in),
        (0.60, c0 + Vector((-0.01, -0.03, 0.01)), c0 + Vector((0.17, 0.12, -0.10)), lens_in * 1.2),
        (0.70, Vector((0.05, -0.55, 0.12)), c0, 30.0),
        (0.84, Vector((far * 0.45, -far * 0.70, far * 0.38)), Vector((0, 0.6, -0.05)), 45.0),
        (1.00, Vector((far * 0.62, -far * 0.58, far * 0.40)), Vector((0, 0.6, -0.1)), 50.0),
    ]
    for (ta, pa, qa, la), (tb, pb, qb, lb) in zip(keys, keys[1:]):
        if t <= tb:
            u = kit.smoother((t - ta) / (tb - ta))
            return pa.lerp(pb, u), qa.lerp(qb, u), kit.lerp(la, lb, u)
    return keys[-1][1], keys[-1][2], keys[-1][3]


def main():
    os.makedirs(ARGS.out, exist_ok=True)
    cam, fill = build(ARGS.variant)
    frames = pass_order(FRAMES) if ARGS.frames == 'all' else [int(x) for x in ARGS.frames.split(',')]
    meta_path = os.path.join(ARGS.out, 'meta.json')
    meta = {'frames': FRAMES, 'res': VARIANTS[ARGS.variant]['res'], 'hotspots': {}}
    for f in frames:
        t = f / (FRAMES - 1)
        loc, target, lens = cam_pose(t, ARGS.variant)
        cam.location = loc
        kit.aim(cam, target)
        cam.data.lens = lens
        cam.data.dof.focus_distance = max(0.05, (target - loc).length * 0.7)
        # hücre içindeyken kameraya eşlik eden çok zayıf dolgu (karanlıkta kaybolmasın)
        fill.location = loc - (target - loc).normalized() * 0.01
        kit.aim(fill, target)
        fill.data.energy = 0.012 * kit.smooth(kit.seg(t, 0.26, 0.36)) * (1 - kit.smooth(kit.seg(t, 0.62, 0.70)))
        if t >= 0.86:
            proj = kit.project(cam, [CHAIN[0][0], (0.25, 0.6, BZ)])
            meta['hotspots'][str(f)] = {k: p for k, p in zip(('hucre', 'matris'), proj) if p}
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
    min_step = int(os.environ.get('EGE_MINSTEP', '1'))  # telefon seti: her 2. kare
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
