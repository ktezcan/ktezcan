"""
Sahne 0 — "Video bloğa dönüşür"

Açılış videosu (DOM'da oynayan gerçek fabrika filmi) bloğun ön yüzüne
oturur; kamera geri çekilip bloğun etrafında döner, geçmeli dil-yuva ucu
ve üst yüz görünür. Her kare için ön yüzün 4 köşesi JSON'a yazılır →
web tarafı videoyu CSS matrix3d homografisiyle bu yüze yapıştırır
(boyut sıçraması olmadan, kesintisiz).

Kullanım:
  python s0_video_blok.py --variant d|m --frames all|0,10,71 --out DIR [--samples N]
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

FRAMES = 60
L, H, T = 0.60, 0.25, 0.25
FACE_Y = -T / 2

VARIANTS = {
    # masaüstü 16:9 — 1600×900
    'd': dict(res=(1600, 900), lens=50.0,
              start=dict(dist=L * 50.0 / 36.0, yaw=0.0, pitch=0.0, tz=H / 2, tx=0.0),
              end=dict(dist=1.95, yaw=34.0, pitch=17.0, tz=0.12, tx=-0.04)),
    # telefon 9:16 — 768×1366 (ayrı kadraj)
    'm': dict(res=(768, 1366), lens=34.0,
              start=dict(dist=L * 34.0 / 36.0, yaw=0.0, pitch=0.0, tz=H / 2, tx=0.0),
              end=dict(dist=1.22, yaw=30.0, pitch=24.0, tz=0.11, tx=-0.02)),
}


def build(variant):
    kit.reset()
    v = VARIANTS[variant]
    kit.setup_render(*v['res'], samples=ARGS.samples, threshold=0.012)
    world = kit.studio_world(hdri='studio.exr', hdri_strength=0.32, rot=math.radians(30))
    # zeminin uzak kısmı HDRI'deki softbox'ı yansıtıp parlak leke yapmasın: lekesiz yumuşak ortam
    kit.replace_reflection_env(world, 1.0)

    floor = kit.box('Zemin', (40, 40, 0.02), (0, 0, -0.01), kit.glossy_floor())
    floor.visible_shadow = True

    aac = kit.aac_material('Gazbeton')
    blk = kit.gecmeli_blok('Blok', L, H, T, aac)

    kit.halo_ring('Hale', radius=0.56, width=0.0035, strength=5.0)

    # Işık: yumuşak, nötre yakın ana ışık + arkadan iki kontur şeridi (spot YOK)
    k = kit.area_light('Ana', (-1.5, -1.8, 1.6), (0, 0, 0), (1.8, 1.2), 150, (1.0, 0.975, 0.95))
    kit.aim(k, (0, 0, 0.12))
    f = kit.area_light('Dolgu', (1.6, -1.4, 0.6), (0, 0, 0), (1.2, 1.2), 35, (0.92, 0.96, 1.0))
    kit.aim(f, (0, 0, 0.12))
    r1 = kit.area_light('KonturSol', (-0.9, 1.15, 0.42), (0, 0, 0), (0.12, 1.2), 130, kit.LIME_HI)
    kit.aim(r1, (0, 0, 0.13))
    r2 = kit.area_light('KonturSag', (0.95, 1.1, 0.5), (0, 0, 0), (0.12, 1.2), 120, (0.86, 0.93, 1.0))
    kit.aim(r2, (0, 0, 0.13))
    for ob in (r1, r2):
        ob.visible_glossy = False  # zeminde dev şerit yansıması olmasın

    cam = kit.camera('Kamera', lens=v['lens'], loc=(0, -3, 0.2), target=(0, 0, 0.12), fstop=4.0)
    dust = kit.dust(count=36, bounds=((-1.0, 1.0), (-0.3, 1.2), (0.05, 0.9)), seed=11, size=(0.0008, 0.0016), strength=0.6)
    return cam, blk, dust


def cam_pose(t, variant):
    """t: 0..1 → kamera konumu ve hedefi (yumuşak, sıçramasız)."""
    v = VARIANTS[variant]
    s, e = v['start'], v['end']
    # İlk %8: tam ön yüz (video yüzü dolduruyor) → sonra geri çekil + dön
    u = kit.ease_in_out(kit.seg(t, 0.06, 0.92))
    dist = kit.lerp(s['dist'], e['dist'], kit.smoother(kit.seg(t, 0.06, 0.8)))
    yaw = math.radians(kit.lerp(s['yaw'], e['yaw'], u))
    pitch = math.radians(kit.lerp(s['pitch'], e['pitch'], kit.smoother(kit.seg(t, 0.12, 0.95))))
    tz = kit.lerp(s['tz'], e['tz'], u)
    tx = kit.lerp(s['tx'], e['tx'], u)
    # yüz merkezinden hedefe: başlangıçta ön yüz merkezi, sonra blok merkezi
    ty = kit.lerp(FACE_Y, 0.0, u)
    target = Vector((tx, ty, tz))
    # küresel koordinat: yaw z ekseni etrafında, pitch yukarı
    d = Vector((math.sin(yaw) * math.cos(pitch), -math.cos(yaw) * math.cos(pitch), math.sin(pitch)))
    return target + d * dist, target


def pass_order(n):
    """Önce kaba geçiş (her 8. kare), sonra aralar: süre biterse bile dizi kullanılabilir."""
    order, seen = [], set()
    min_step = int(os.environ.get('EGE_MINSTEP', '1'))  # telefon seti: her 2. kare
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


def main():
    os.makedirs(ARGS.out, exist_ok=True)
    cam, blk, dust = build(ARGS.variant)
    frames = pass_order(FRAMES) if ARGS.frames == 'all' else [int(x) for x in ARGS.frames.split(',')]
    meta_path = os.path.join(ARGS.out, 'meta.json')
    meta = {'frames': FRAMES, 'res': VARIANTS[ARGS.variant]['res'], 'face': {}}
    if os.path.exists(meta_path):
        import json
        meta = json.load(open(meta_path))
    # blok nesnesinin yerel orijini gövde merkezinde (z = H/2): köşeler yerel koordinatta
    corners = [(-L / 2, FACE_Y, H / 2), (L / 2, FACE_Y, H / 2), (L / 2, FACE_Y, -H / 2), (-L / 2, FACE_Y, -H / 2)]
    for f in frames:
        t = f / (FRAMES - 1)
        loc, target = cam_pose(t, ARGS.variant)
        cam.location = loc
        kit.aim(cam, target)
        cam.data.dof.focus_distance = (Vector(target) - loc).length
        kit.move_dust(dust, t * 3.0)
        # blok kendi ekseninde çok az döner (kamera hareketine eşlik)
        blk.rotation_euler[2] = math.radians(6.0 * kit.smooth(kit.seg(t, 0.3, 1.0)))
        bpy.context.view_layer.update()
        world_corners = [tuple(blk.matrix_world @ Vector(c)) for c in corners]
        meta['face'][str(f)] = kit.project(cam, world_corners)
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
    ap.add_argument('--samples', type=int, default=32)
    ap.add_argument('--skip-existing', action='store_true')
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
