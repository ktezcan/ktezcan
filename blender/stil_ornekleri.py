"""
Stil örnekleri: aynı iki sahne (blok, bina) beş farklı görsel dilde.
Amaç: tüm hikâye için TEK bir stil seçmek.

  A  Fotogerçekçi   — sinematik ışık, gerçek malzeme (mevcut yön)
  B  Kil maket      — mat beyaz mimari maket, yumuşak gün ışığı, lime vurgu
  C  Teknik çizim   — açık zemin + ince kontur çizgileri (mimar/mühendis dili)
  D  Gece neon      — koyu grafit dünya, lime ışıldayan kenar çizgileri
  E  Minyatür       — fotogerçekçi, yüksek açı + güçlü alan derinliği (diorama)
  F  İzometrik      — ortografik kamera, pastel düz renkler (web illüstrasyonu dili)
  G  Çizgi roman    — Toon BSDF ile cel gölge + koyu kontur (ligne claire)
  H  Mavi kopya     — lacivert zemin, beyaz çizgi (blueprint)
  I  Röntgen        — saydam gövde, kenarda lime parıltı; iç yapı görünür
  J  Editoryal S/B  — siyah-beyaz, sert güneş gölgesi; renk yalnız üründe (lime)

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


URUN = ('Duvar', 'Lento', 'CatiPaneli', 'Istif', 'Gazbeton')


def urun_mu(mn):
    return mn.startswith(URUN)


def mat_toon(name, hexcol, golge=0.55):
    """Cel gölge: iki ton (aydınlık / gölge) + az ortam."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    toon = nt.nodes.new('ShaderNodeBsdfToon')
    toon.component = 'DIFFUSE'
    toon.inputs['Size'].default_value = 0.62
    toon.inputs['Smooth'].default_value = 0.015
    c = kit.srgb(hexcol)
    toon.inputs['Color'].default_value = c
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = (c[0] * golge, c[1] * golge, c[2] * golge, 1)
    em.inputs['Strength'].default_value = 1.0
    add = nt.nodes.new('ShaderNodeAddShader')
    nt.links.new(toon.outputs[0], add.inputs[0])
    nt.links.new(em.outputs[0], add.inputs[1])
    nt.links.new(add.outputs[0], out.inputs['Surface'])
    return m


def mat_duz_isik(name, hexcol, guc=1.0):
    """Işıktan bağımsız düz renk (mavi kopya zemini vb.)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = kit.srgb(hexcol)
    em.inputs['Strength'].default_value = guc
    nt.links.new(em.outputs[0], out.inputs['Surface'])
    return m


def mat_rontgen(name, hexcol, guc, saydam=0.88):
    """Saydam gövde + açıya bağlı (fresnel) kenar parıltısı."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.blend_method = 'BLEND' if hasattr(m, 'blend_method') else None
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    lw = nt.nodes.new('ShaderNodeLayerWeight')
    lw.inputs['Blend'].default_value = 0.35
    ramp = nt.nodes.new('ShaderNodeMapRange')
    ramp.inputs['From Min'].default_value = 0.0
    ramp.inputs['From Max'].default_value = 1.0
    ramp.inputs['To Min'].default_value = 0.0
    ramp.inputs['To Max'].default_value = 1.0
    nt.links.new(lw.outputs['Facing'], ramp.inputs['Value'])
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = kit.srgb(hexcol)
    mul = nt.nodes.new('ShaderNodeMath')
    mul.operation = 'MULTIPLY'
    mul.inputs[1].default_value = guc
    nt.links.new(ramp.outputs[0], mul.inputs[0])
    nt.links.new(mul.outputs[0], em.inputs['Strength'])
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    add = nt.nodes.new('ShaderNodeAddShader')
    nt.links.new(em.outputs[0], add.inputs[0])
    nt.links.new(tr.outputs[0], add.inputs[1])
    mix = nt.nodes.new('ShaderNodeMixShader')
    mix.inputs['Fac'].default_value = saydam
    em2 = nt.nodes.new('ShaderNodeEmission')
    em2.inputs['Color'].default_value = kit.srgb(hexcol)
    em2.inputs['Strength'].default_value = guc * 0.04
    nt.links.new(em2.outputs[0], mix.inputs[1])
    nt.links.new(add.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs['Surface'])
    return m


def bolge_renk(mn, tablo, varsayilan):
    for onek, m in tablo:
        if mn.startswith(onek) or onek in mn:
            return m
    return varsayilan


def isiklari_kapat(tur=('AREA', 'POINT', 'SPOT'), haric=('Lamba',)):
    for ob in bpy.data.objects:
        if ob.type == 'LIGHT' and ob.data.type in tur and not any(h in ob.name for h in haric):
            ob.data.energy = 0


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
    elif stil == 'F':  # izometrik pastel
        tablo = [('Cam', mat_duz('PCam', '#9fc3d6', 0.2)),
                 ('Beton', mat_duz('PBeton', '#c9b8a6', 0.9)),
                 ('Tabla', mat_duz('PTabla', '#e8d9c4', 0.95)),
                 ('Zemin', mat_duz('PZemin', '#f0e2cf', 0.95)),
                 ('SahaZemin', mat_duz('PSaha', '#f0e2cf', 0.95)),
                 ('Tepe', mat_duz('PTepe', '#e9c9a8', 0.95)),
                 ('Vinc', mat_duz('PVinc', '#f2b33d', 0.6)),
                 ('Ahsap', mat_duz('PAhsap', '#c98f5a', 0.8)),
                 ('Dograma', mat_duz('PDog', '#4a5a66', 0.5)),
                 ('Siluet', mat_duz('PSil', '#4a5a66', 0.9))]
        urun = mat_duz('PUrun', '#fbf7f0', 0.8)
        malzeme_degistir(lambda mn, on: urun if urun_mu(mn) else bolge_renk(mn, tablo, mat_duz('PDiger', '#d8cfc4', 0.8)))
        dunya_renk((0.98, 0.9, 0.82), 0.9)
        isiklar_yumusat(1.0)
        if sahne == 'bina':
            isiklari_kapat()
        sc.view_settings.look = 'AgX - Base Contrast'
        sc.view_settings.exposure = 0.15 if sahne == 'bina' else -0.6
    elif stil == 'G':  # çizgi roman
        tablo = [('Cam', mat_toon('TCam', '#7fb4cf', 0.7)),
                 ('Beton', mat_toon('TBeton', '#a7a39b')),
                 ('Tabla', mat_toon('TTabla', '#bdb6a8')),
                 ('Zemin', mat_toon('TZemin', '#d9c9a3')),
                 ('SahaZemin', mat_toon('TSaha', '#d9c9a3')),
                 ('Tepe', mat_toon('TTepe', '#b9a27c')),
                 ('Vinc', mat_toon('TVinc', '#f4b51e')),
                 ('Ahsap', mat_toon('TAhsap', '#b87a45')),
                 ('Dograma', mat_toon('TDog', '#33414c')),
                 ('Siluet', mat_toon('TSil', '#22282d'))]
        urun = mat_toon('TUrun', '#f6f2ea', 0.62)
        malzeme_degistir(lambda mn, on: urun if urun_mu(mn) else bolge_renk(mn, tablo, mat_toon('TDiger', '#c8c2b8')))
        dunya_renk((0.55, 0.78, 0.92), 1.0)
        for ob in bpy.data.objects:
            if ob.type == 'LIGHT' and ob.data.type == 'SUN':
                ob.data.angle = math.radians(0.5)
        if sahne == 'bina':
            isiklari_kapat()
        cizgi((0.07, 0.09, 0.11), 1.8 if sahne == 'bina' else 2.4)
        sc.view_settings.view_transform = 'Standard'
        sc.view_settings.exposure = -0.2 if sahne == 'bina' else -1.0
    elif stil == 'H':  # mavi kopya
        zem = mat_duz_isik('MZemin', '#123a6b', 1.0)
        gov = mat_duz_isik('MGovde', '#16467f', 1.0)
        urun = mat_duz_isik('MUrun', '#1d5694', 1.0)
        malzeme_degistir(lambda mn, on: urun if urun_mu(mn) else (zem if mn.startswith(('Zemin', 'SahaZemin', 'Tabla', 'Tepe')) else gov))
        dunya_renk(tuple(kit.srgb('#0f3360')[:3]), 1.0)
        sil(['Tepe'])
        isiklari_kapat(tur=('AREA', 'POINT', 'SPOT', 'SUN'), haric=())
        cizgi((0.9, 0.95, 1.0), 1.0 if sahne == 'bina' else 1.4)
        sc.view_settings.view_transform = 'Standard'
        sc.view_settings.exposure = 0.0
    elif stil == 'I':  # röntgen / hologram
        lime = '#b8d84a'
        tablo = [('Beton', mat_rontgen('RBeton', '#6fb7d9', 0.9, 0.97))]
        urun = mat_rontgen('RUrun', lime, 1.1, 0.95)
        zem = mat_duz_isik('RZemin', '#05080a', 1.0)
        malzeme_degistir(lambda mn, on: urun if urun_mu(mn) else (zem if mn.startswith(('Zemin', 'SahaZemin', 'Tabla')) else bolge_renk(mn, tablo, mat_rontgen('RDiger', '#5d7b8c', 0.6, 0.97))))
        sil(['Tepe', 'Strec'])
        dunya_renk((0.003, 0.005, 0.007), 1.0)
        isiklari_kapat(tur=('AREA', 'POINT', 'SPOT', 'SUN'), haric=())
        sc.cycles.transparent_max_bounces = 64
        kit.sinematik(bloom=0.45, esik=0.8, boyut=0.7)
        sc.view_settings.exposure = 0.0
    elif stil == 'J':  # editoryal siyah-beyaz
        tablo = [('Cam', mat_duz('JCam', '#2b2b2b', 0.05)),
                 ('Beton', mat_duz('JBeton', '#7a7a7a', 0.85)),
                 ('Zemin', mat_duz('JZemin', '#b9b9b9', 0.9)),
                 ('SahaZemin', mat_duz('JSaha', '#b9b9b9', 0.9)),
                 ('Tabla', mat_duz('JTabla', '#9a9a9a', 0.9)),
                 ('Tepe', mat_duz('JTepe', '#6a6a6a', 1.0)),
                 ('Vinc', mat_duz('JVinc', '#4a4a4a', 0.6)),
                 ('Ahsap', mat_duz('JAhsap', '#5a5a5a', 0.8)),
                 ('Dograma', mat_duz('JDog', '#1e1e1e', 0.4)),
                 ('Siluet', mat_duz('JSil', '#0a0a0a', 0.9))]
        urun = mat_duz('JUrun', '#efefec', 0.85)
        malzeme_degistir(lambda mn, on: urun if urun_mu(mn) else bolge_renk(mn, tablo, mat_duz('JDiger', '#8a8a8a', 0.8)))
        dunya_renk((0.55, 0.55, 0.55), 0.35)
        for ob in bpy.data.objects:
            if ob.type == 'LIGHT' and ob.data.type == 'SUN':
                ob.data.angle = math.radians(0.4)
                ob.data.color = (1, 1, 1)
                ob.data.energy *= 1.6
        if sahne == 'bina':
            isiklari_kapat(haric=('Lamba',))
        sc.view_settings.look = 'AgX - Very High Contrast'
        sc.view_settings.exposure = 0.0 if sahne == 'bina' else -0.8


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
        if ARGS.stil == 'F':
            d = (Vector(target) - loc).length
            cam.data.ortho_scale = d * 36.0 / cam.data.lens * 1.15
            cam.data.type = 'ORTHO'
            cam.data.dof.use_dof = False
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
        if ARGS.stil == 'F':  # izometrik: 45° yatay, ~35° eğim, ortografik
            target = Vector((-2.5, 0.0, 9.0))
            loc = target + Vector((1, -1, 0.82)).normalized() * 120
            cam.data.type = 'ORTHO'
            cam.data.ortho_scale = 54.0
            cam.data.clip_end = 1000
        if ARGS.stil == 'E':  # minyatür: yüksekten bak, sığ alan derinliği
            d = loc - target
            loc = target + Vector((d.x * 1.35, d.y * 1.35, d.z + 26.0))
        cam.location = loc
        kit.aim(cam, target)
        if ARGS.stil != 'F':
            kit.kaydir(cam, 'd', 1.0)
        cam.data.dof.use_dof = ARGS.stil != 'F'
        cam.data.dof.focus_distance = (target - loc).length
        cam.data.dof.aperture_fstop = 0.06 if ARGS.stil == 'E' else 11.0
        if ARGS.stil == 'E':
            cam.data.lens = 50.0
    stil_uygula(ARGS.stil, ARGS.sahne)
    if ARGS.sahne == 'blok' and ARGS.stil in ('F', 'G', 'J'):
        sc0 = bpy.context.scene
        sc0.view_settings.exposure = {'F': -1.6, 'G': -1.9, 'J': -1.5}[ARGS.stil]
        for ob in bpy.data.objects:
            if ob.type == 'LIGHT' and 'Kontur' in ob.name:
                ob.data.energy *= 0.15
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
