"""
Stil örnekleri: aynı iki sahne (blok, bina) beş farklı görsel dilde.
Amaç: tüm hikâye için TEK bir stil seçmek.

  A  Fotogerçekçi   — sinematik ışık, gerçek malzeme (mevcut yön)
  B  Kil maket      — mat beyaz mimari maket, yumuşak gün ışığı, lime vurgu
  C  Teknik çizim   — açık zemin + ince kontur çizgileri (mimar/mühendis dili)
  D  Gece neon      — koyu grafit dünya, lime ışıldayan kenar çizgileri
  E  Minyatür       — fotogerçekçi, yüksek açı + güçlü alan derinliği (diorama)

Kullanım: python stil_ornekleri.py --stil A|B|C|D|E --sahne blok|bina --out DIR
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

KORU = ('Strec', 'Hale', 'SahaHalka', 'Lamba', 'IcM', 'Toz', 'Yildiz', 'Huzme', 'Video')


def mat_duz(name, hexcol, rough=0.6, emis=None, es=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = kit.srgb(hexcol)
    b.inputs['Roughness'].default_value = rough
    if emis:
        b.inputs['Emission Color'].default_value = kit.srgb(emis)
        b.inputs['Emission Strength'].default_value = es
    return m


def malzeme_degistir(fn):
    """Korunacaklar dışındaki tüm malzemeleri fn(eski_ad) → yeni malzeme ile değiştir."""
    for ob in bpy.data.objects:
        if ob.type != 'MESH':
            continue
        for i, slot in enumerate(ob.material_slots):
            m = slot.material
            if m is None or any(k in m.name for k in KORU):
                continue
            yeni = fn(m.name, ob.name)
            if yeni:
                ob.material_slots[i].material = yeni


def sil(prefixes):
    for ob in list(bpy.data.objects):
        if any(ob.name.startswith(p) for p in prefixes):
            bpy.data.objects.remove(ob, do_unlink=True)


def dunya_renk(rgb, guc):
    w = bpy.data.worlds.new('StilDunya')
    bpy.context.scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get('Background')
    bg.inputs['Color'].default_value = (*rgb, 1.0)
    bg.inputs['Strength'].default_value = guc


def isiklar_yumusat(enerji_carpan=1.0):
    for ob in bpy.data.objects:
        if ob.type == 'LIGHT' and ob.data.type == 'SUN':
            ob.data.angle = math.radians(9)
            ob.data.energy *= enerji_carpan


def cizgi(renk, kalinlik):
    sc = bpy.context.scene
    sc.render.use_freestyle = True
    sc.render.line_thickness_mode = 'ABSOLUTE'
    vl = sc.view_layers[0]
    vl.use_freestyle = True
    ls = vl.freestyle_settings.linesets[0] if len(vl.freestyle_settings.linesets) else vl.freestyle_settings.linesets.new('Cizgi')
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new('CizgiStil')
    ls.select_by_visibility = True
    ls.select_silhouette = True
    ls.select_border = True
    ls.select_crease = True
    ls.linestyle.color = renk
    ls.linestyle.thickness = kalinlik
    vl.freestyle_settings.crease_angle = math.radians(140)


def stil_uygula(stil, sahne):
    sc = bpy.context.scene
    if stil == 'A':
        return
    sil(['Sis', 'Tepe'] if stil in ('C', 'D') else ['Sis'])
    for ob in bpy.data.objects:
        if ob.type == 'LIGHT' and ob.name.startswith('Huzme'):
            ob.data.energy = 0
    if stil in ('B', 'C'):
        kil = mat_duz('Kil', '#ebe7e1', 0.65)
        kil_koyu = mat_duz('KilKoyu', '#d6d1c9', 0.75)
        cam_m = mat_duz('KilCam', '#aebcc4', 0.15)
        def fn(mn, on):
            if 'Cam' in mn:
                return cam_m
            if mn.startswith(('Zemin', 'SahaZemin', 'Tabla', 'Tepe')):
                return kil_koyu
            return kil
        malzeme_degistir(fn)
        if stil == 'B':
            dunya_renk((0.62, 0.68, 0.74), 0.55)
            isiklar_yumusat(1.0)
            sc.view_settings.exposure = -0.1
            sc.view_settings.look = 'AgX - Medium High Contrast'
        else:
            dunya_renk((0.93, 0.95, 0.96), 1.25)
            isiklar_yumusat(0.45)
            sc.view_settings.exposure = 0.45
            cizgi((0.19, 0.27, 0.32), 1.1)
    elif stil == 'D':
        graf = mat_duz('Grafit', '#1a1f23', 0.42)
        zem = mat_duz('GrafitZemin', '#0c0f11', 0.3)
        cam_m = mat_duz('NeonCam', '#20262a', 0.1)
        def fn(mn, on):
            if 'Cam' in mn:
                return cam_m
            if mn.startswith(('Zemin', 'SahaZemin', 'Tabla', 'Tepe')):
                return zem
            return graf
        malzeme_degistir(fn)
        dunya_renk((0.004, 0.006, 0.008), 1.0)
        for ob in bpy.data.objects:
            if ob.type == 'LIGHT' and ob.data.type == 'SUN':
                ob.data.energy *= 0.08
        cizgi((0.72, 0.84, 0.29), 1.3)
        sc.view_settings.exposure = 0.3
    elif stil == 'E':
        sc.view_settings.look = 'AgX - Punchy'


def main():
    out = ARGS.out
    os.makedirs(out, exist_ok=True)
    if ARGS.sahne == 'blok':
        import s0_video_blok as s
        s.ARGS = argparse.Namespace(samples=ARGS.samples)
        cam, blk, dust = s.build('d')
        loc, target = s.cam_pose(1.0, 'd')
        cam.location = loc
        kit.aim(cam, target)
        kit.kaydir(cam, 'd', 1.0)
        cam.data.dof.focus_distance = (Vector(target) - loc).length
        blk.rotation_euler[2] = math.radians(6.0)
        kit.move_dust(dust, 3.0)
    else:
        import s3_bina as s
        s.ARGS = argparse.Namespace(samples=ARGS.samples)
        cam, objs, wall_mats, dusk = s.build('d')
        u = ARGS.u
        t = s.yapim_t(u)
        for mat in wall_mats.values():
            for n in mat.node_tree.nodes:
                if n.type == 'MATH' and n.operation == 'SUBTRACT' and not n.inputs[0].is_linked and abs(n.inputs[1].default_value - s.T_WALL0) < 1e-6:
                    n.inputs[0].default_value = t
        s.apply_state(objs, t)
        s.alacakaranlik(dusk, u)
        loc, target = s.sahne_kamera(u, 'd')
        if ARGS.stil == 'E':  # minyatür: yüksekten bak, sığ alan derinliği
            d = loc - target
            loc = target + Vector((d.x * 1.35, d.y * 1.35, d.z + 26.0))
        cam.location = loc
        kit.aim(cam, target)
        kit.kaydir(cam, 'd', 1.0)
        cam.data.dof.use_dof = True
        cam.data.dof.focus_distance = (target - loc).length
        cam.data.dof.aperture_fstop = 0.06 if ARGS.stil == 'E' else 11.0
        if ARGS.stil == 'E':
            cam.data.lens = 50.0
    stil_uygula(ARGS.stil, ARGS.sahne)
    if ARGS.sahne == 'blok' and ARGS.stil in ('B', 'C'):
        # beyaz maket bloğu: stüdyo ışıkları beyaz zeminde fazla; lime kontur ışığı kısılır
        sc0 = bpy.context.scene
        sc0.view_settings.exposure = -1.3 if ARGS.stil == 'B' else -1.0
        for ob in bpy.data.objects:
            if ob.type == 'LIGHT' and 'Kontur' in ob.name:
                ob.data.energy *= 0.25
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = 1280, 720
    kit.render_to(os.path.join(out, f'{ARGS.sahne}_{ARGS.stil}.png'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--stil', default='A')
    ap.add_argument('--sahne', default='bina')
    ap.add_argument('--u', type=float, default=0.78)
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=40)
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
