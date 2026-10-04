"""
Stil R8 — sunum kareleri (referans: konseptten gerçeğe):

  eskiz : bej kâğıt, el çizimi (Freestyle: uzayan çizgi uçları + titreme), gerçek kareyle aynı kadraj
  plan  : tepeden ortografik vaziyet (gündüz) — üstüne koyu sunum katmanı/etiketler sonra eklenir
  kafes : siyah zemin; karkas beyaz katı, gazbeton duvarlar ışıyan tel kafes; etiket çapaları JSON

Etiketler 3B'ye yazılmaz (kural): çapa noktaları ekran koordinatı olarak <ad>.json'a yazılır;
yazılar web'de HTML/SVG, panoda PIL ile eklenir.
"""
import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
import stil_r as R  # noqa: E402
import stil_r3 as T  # noqa: E402
import stil_r6 as K  # noqa: E402
import stil_r7 as G  # noqa: E402
import bina_detay as B  # noqa: E402
import sokak as S  # noqa: E402


def gercek_kamera():
    return R.kamera(hedef=(-0.5, -4.0, 4.6), yon=(0.62, -1.0, 0.02), uzak=24.0, lens=24, fstop=11, kayma=0.0)


def kagit_dunya(sc, renk='#ebe3d5'):
    w = bpy.data.worlds.new('Kagit')
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (*kit.srgb(renk)[:3], 1)
    bg.inputs['Strength'].default_value = 1.0
    sc.view_settings.view_transform = 'Standard'
    sc.view_settings.look = 'None'
    sc.view_settings.exposure = 0.0


def duz_malzeme(renk, guc=1.0):
    m = bpy.data.materials.new('Duz' + renk)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = kit.srgb(renk)
    em.inputs['Strength'].default_value = guc
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(em.outputs[0], out.inputs['Surface'])
    return m


def sahne_eskiz(sc):
    P, mats = T.bina_hazir()
    kagit = duz_malzeme('#ebe3d5')
    # eskiz sade olsun: bloklar tek tek çizilmez, duvar tek yüzey; karkas, doğrama, lento çizilir
    B.kur(P, {k: kagit for k in mats}, lambda p: None if p['tur'] in ('harc', 'cam', 'blok', 'sove') else (p['c'], p['s'], (0, 0, 0)))
    kit.box('DuvarKutle', (B.XS[-1] - B.XS[0] - 0.02, B.YS[-1] - B.YS[0] - 0.02, B.KAT * B.FH - 0.1), (0, 0, B.KAT * B.FH / 2), kagit)
    yb = B.YS[0] - B.WT / 2 - 0.05
    kit.box('Yol', (1.6, 4.0, 0.16), (0, yb - 2.0, 0.08), kagit)
    kit.box('BahceDuvar', (16, 0.2, 0.55), (0, G.Y_SOKAK + 0.15, 0.275), kagit)
    for ob in bpy.data.objects:
        if ob.type == 'LIGHT':
            ob.hide_render = True
    kagit_dunya(sc)
    sc.render.use_freestyle = True
    sc.render.line_thickness_mode = 'ABSOLUTE'
    vl = sc.view_layers[0]
    vl.use_freestyle = True
    fs = vl.freestyle_settings
    fs.crease_angle = math.radians(130)
    ls = fs.linesets[0] if len(fs.linesets) else fs.linesets.new('Eskiz')
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new('Kalem')
    ls.select_silhouette = ls.select_border = ls.select_crease = True
    st = ls.linestyle
    st.color = (0.16, 0.15, 0.14)
    st.thickness = 1.3
    st.alpha = 0.85
    gm = st.geometry_modifiers
    bs = gm.new('Uzat', 'BACKBONE_STRETCHER')
    bs.backbone_length = 9.0
    pn = gm.new('Titrek', 'PERLIN_NOISE_1D')
    pn.frequency = 12.0
    pn.amplitude = 1.6
    pn.octaves = 3
    tm = st.thickness_modifiers.new('Baski', 'ALONG_STROKE')
    tm.mapping = 'CURVE'
    tm.value_min, tm.value_max = 0.4, 1.4
    sc.compositing_node_group = None
    gercek_kamera()


def sahne_plan(sc):
    G.sahne_gercek(sc)
    c = bpy.context.scene.camera
    c.location = (0.0, -5.0, 120.0)
    c.rotation_euler = (0, 0, 0)
    c.data.type = 'ORTHO'
    c.data.ortho_scale = 46.0
    c.data.dof.use_dof = False
    c.data.shift_x = c.data.shift_y = 0


def sahne_kafes(sc):
    P, mats = T.bina_hazir()
    beyaz = S.pbr('KarkasBeyaz', '#f2f1ee', 0.6)
    karkas = ('temel', 'kolon', 'kiris', 'doseme')
    B.kur(P, {k: beyaz for k in mats}, lambda p: (p['c'], p['s'], (0, 0, 0)) if p['tur'] in karkas else None)
    T.cizgi_kur(P, filtre=lambda p: p['tur'] in ('blok', 'lento', 'panel', 'dograma'),
                mat=S.pbr('TelKafes', '#ffffff', 0.4, 0.0, '#e9f2ff', 0.55), kalin=0.014)
    w = bpy.data.worlds.new('Siyah')
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.0, 0.0, 0.0, 1)
    for ob in bpy.data.objects:
        if ob.type == 'LIGHT' and ob.data.type == 'AREA':
            ob.data.energy *= 0.35
    kit.sinematik(bloom=0.3, esik=1.2, boyut=0.6)
    cam = T.bina_kamera(yon=(0.85, -1.0, 0.32), uzak=44)
    # etiket çapaları (dünya → ekran)
    xs, ys = B.XS, B.YS
    capa = {
        'blok': Vector((-3.0, ys[0] - 0.1, 1.2)),
        'lento': Vector((0.0, ys[0] - 0.1, B.FH + 2.4)),
        'karkas': Vector((xs[-1], ys[0], 2 * B.FH + 1.2)),
        'panel': Vector((1.5, 0.0, B.KAT * B.FH + 0.25)),
        'derz': Vector((-4.5, ys[0] - 0.1, 2 * B.FH + 0.75)),
    }
    pr = kit.project(cam, list(capa.values()))
    json.dump({k: p for k, p in zip(capa, pr)}, open(os.path.join(ARGS.out, 'kafes.json'), 'w'))


SAHNELER = {k[6:]: v for k, v in globals().items() if k.startswith('sahne_')}


def main():
    kit.reset()
    sc = kit.setup_render(1280, 720, samples=ARGS.samples, threshold=0.02, bounces=(6, 3, 3, 4))
    sc.cycles.transparent_max_bounces = 16
    R.studyo(sc)
    os.makedirs(ARGS.out, exist_ok=True)
    SAHNELER[ARGS.sahne](sc)
    kit.render_to(os.path.join(ARGS.out, f'{ARGS.sahne}.png'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--sahne', default='eskiz')
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=48)
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
