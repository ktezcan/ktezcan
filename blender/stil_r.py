"""
Stil R — referans: açık stüdyo zemini üzerinde tek kahraman nesne, fotogerçekçi;
kaydırdıkça nesne dönüşür (blok → parçacıklara dağılma → içi parlayan hücre küresi
→ havada birleşen bloklardan bina). Zemin sıcak açık gri; nesne yüzer, gölge yok.

Kullanım: python stil_r.py --sahne blok|dagilma|kure|bina --out DIR [--ad ...]
"""
import argparse
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

ZEMIN = '#ddd6d0'  # sıcak açık gri (referanstaki pembe-bej stüdyo)
AMBER = (1.0, 0.55, 0.18)


def studyo(sc, anahtar=650.0):
    w = bpy.data.worlds.new('Studyo')
    sc.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes['Background']  # aydınlatma: düşük, nötr
    bg.inputs['Color'].default_value = (*kit.srgb(ZEMIN)[:3], 1)
    bg.inputs['Strength'].default_value = 0.12
    gor = nt.nodes.new('ShaderNodeBackground')  # kameranın gördüğü zemin: parlak, sıcak açık
    gor.inputs['Color'].default_value = (*kit.srgb('#efe9e4')[:3], 1)
    gor.inputs['Strength'].default_value = 1.75
    lp = nt.nodes.new('ShaderNodeLightPath')
    mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(lp.outputs['Is Camera Ray'], mx.inputs['Fac'])
    nt.links.new(bg.outputs[0], mx.inputs[1])
    nt.links.new(gor.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], nt.nodes['World Output'].inputs['Surface'])
    # anahtar: sol üstten büyük yumuşak; dolgu: sağ önden; kontur: arkadan
    kit.area_light('Anahtar', (-1.3, -0.4, 2.1), (0, 0, 0), 1.0, anahtar, (1.0, 0.97, 0.93))
    kit.area_light('Dolgu', (2.6, -2.2, 0.4), (0, 0, 0), 3.0, anahtar * 0.08, (0.95, 0.97, 1.0))
    kit.area_light('Kontur', (1.4, 2.0, 1.2), (0, 0, 0), 0.8, anahtar * 0.6, (1.0, 0.98, 0.95))
    for ob in bpy.data.objects:
        if ob.type == 'LIGHT':
            kit.aim(ob, (0, 0, 0))
    sc.view_settings.look = 'AgX - Medium High Contrast'
    sc.view_settings.exposure = 0.0


def kamera(hedef=(0, 0, 0), yon=(0.75, -1.0, 0.42), uzak=3.0, lens=70, fstop=4.0, kayma=-0.17):
    t = Vector(hedef)
    loc = t + Vector(yon).normalized() * uzak
    cam = kit.camera('Kamera', lens=lens, loc=loc, target=t, fstop=fstop, focus=uzak)
    cam.data.shift_x = kayma
    return cam


def voksel_blok(L=0.6, T=0.25, H=0.25, a=0.0125):
    """Bloğu küçük küplere ayır (merkez listesi)."""
    nx, ny, nz = round(L / a), round(T / a), round(H / a)
    pts = []
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                pts.append(Vector((-L / 2 + (i + 0.5) * a, -T / 2 + (j + 0.5) * a, -H / 2 + (k + 0.5) * a)))
    return pts


def kupler(name, merkezler, boyutlar, donmeler, mat):
    return kit.toplu_mesh(name, kit.sablon('kup'), [tuple(c) for c in merkezler], boyutlar, donmeler, mat)


def isiltili(name, renk, guc, ornekle=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*renk, 1)
    b.inputs['Emission Color'].default_value = (*renk, 1)
    b.inputs['Emission Strength'].default_value = guc
    if not ornekle:
        m.cycles.emission_sampling = 'NONE'  # binlerce ışıyan parçacık ışık ağacına girmesin (hız)
    return m


def sahne_blok(sc):
    mat = kit.aac_material('Gazbeton', bump=1.1)
    b = kit.gecmeli_blok('Blok', 0.6, 0.25, 0.25, mat)
    b.location = (0, 0, 0)
    b.rotation_euler = (math.radians(4), math.radians(-6), math.radians(18))
    kamera(uzak=2.15, lens=60, fstop=4.0)


def sahne_dagilma(sc):
    """Sol yarı sağlam blok; sağa doğru küpler ayrılır, küçülür, savrulur; uçta ince toz."""
    mat = kit.aac_material('Gazbeton', bump=0.4)
    rnd = random.Random(3)
    a = 0.0125
    pts = voksel_blok(a=a)
    mer, boy, don = [], [], []
    toz = []
    for p in pts:
        f = (p.x + 0.3) / 0.6  # 0 sol … 1 sağ
        e = max(0.0, (f - 0.38) / 0.62 + rnd.uniform(-0.12, 0.12))  # dağılma miktarı
        if e <= 0:
            if p.x > -0.15:  # sınır bölgesi: tek tek küp (pürüzlü kırık yüz)
                mer.append(p)
                boy.append(a)
                don.append((0, 0, 0))
            continue
        e = min(e, 1.0) ** 1.4
        if e > 0.75 and rnd.random() < 0.6:
            toz.append(p + Vector((e * 0.9, rnd.uniform(-0.3, 0.3) * e, rnd.uniform(0.0, 0.45) * e)))
            continue
        yon = Vector((1.0, rnd.uniform(-0.6, 0.6), rnd.uniform(-0.2, 0.9))).normalized()
        mer.append(p + yon * e * rnd.uniform(0.25, 0.85))
        boy.append(a * (1 - 0.65 * e))
        don.append((rnd.uniform(-3, 3) * e, rnd.uniform(-3, 3) * e, rnd.uniform(-3, 3) * e))
    ob = kupler('Dagilan', mer, boy, don, mat)
    ob.rotation_euler = (0, 0, math.radians(14))
    govde = kit.box('SaglamGovde', (0.15 - 0.0005, 0.25, 0.25), (-0.3 + 0.075, 0, 0), mat)  # sağlam kısım: tek parça
    kit.bevel(govde, 0.003, 3)
    govde.parent = ob
    tm = isiltili('TozIsik', AMBER, 6.0)
    tob = kupler('Toz', toz, [a * 0.22] * len(toz), [(0, 0, 0)] * len(toz), tm)
    tob.rotation_euler = ob.rotation_euler
    kamera(hedef=(0.22, 0, 0.05), uzak=2.15, lens=55, fstop=4.0)
    kit.sinematik(bloom=0.35, esik=1.2, boyut=0.6)


def sahne_kure(sc):
    """Hücre küresi: binlerce beyaz hücre (küre kabuğunda, merkeze doğru), ön dilim açık,
    çekirdekte sıcak ışık — 'içi hava, otoklav ısısı'."""
    rnd = random.Random(9)
    m = bpy.data.materials.new('Hucre')
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = kit.srgb('#f1ece6')
    b.inputs['Roughness'].default_value = 0.55
    mer, boy = [], []
    R = 0.5
    n = 3800
    ga = math.pi * (3 - math.sqrt(5))
    kam = Vector((0.75, -1.0, 0.42)).normalized()
    for i in range(n):
        y = 1 - 2 * (i + 0.5) / n
        r = math.sqrt(1 - y * y)
        d = Vector((math.cos(ga * i) * r, y, math.sin(ga * i) * r))
        d = Vector((d.x, d.z, d.y))
        if d.dot(kam) > 0.55:  # kameraya bakan dilim açık: çekirdek görünür
            continue
        # her yönde içe doğru 2–4 hücre (dışta büyük, içte küçük)
        for k in range(rnd.randint(2, 4)):
            rr = R * (1 - k * 0.11) * rnd.uniform(0.97, 1.03)
            s = 0.022 * (1 - k * 0.22) * rnd.uniform(0.8, 1.2)
            mer.append(tuple(d * rr))
            boy.append(s)
    kit.toplu_mesh('Hucreler', kit.sablon('ico', 2), mer, boy, None, m, yumusak=True)
    # çekirdek: sıcak ışık küresi + nokta ışık
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.13, location=(0, 0, 0))
    c = bpy.context.active_object
    c.data.materials.append(isiltili('Cekirdek', (1.0, 0.55, 0.16), 5.0, ornekle=True))
    bpy.ops.object.shade_smooth()
    ld = bpy.data.lights.new('CekirdekIsik', 'POINT')
    ld.energy = 120
    ld.color = AMBER
    ld.shadow_soft_size = 0.12
    lo = bpy.data.objects.new('CekirdekIsik', ld)
    kit.link(lo)
    # kıvılcım tozları
    tm = isiltili('Kivilcim', (1.0, 0.7, 0.3), 10.0)
    pts = [Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1))).normalized() * rnd.uniform(0.15, 0.85) for _ in range(180)]
    kupler('Kivilcim', pts, [0.004] * len(pts), [(0, 0, 0)] * len(pts), tm)
    kamera(uzak=4.0, lens=60, fstop=5.6)
    if not os.environ.get('EGE_BLOOMSUZ'):
        kit.sinematik(bloom=0.6, esik=1.0, boyut=0.7)


def sahne_bina(sc):
    """Havada birleşen bloklardan bina: alt katlar tamam, üst sıralar yukarıdan iner."""
    mat = kit.aac_material('Gazbeton', bump=0.4, tex_size=0.24)
    beton = bpy.data.materials.new('Beton')
    beton.use_nodes = True
    bb = beton.node_tree.nodes['Principled BSDF']
    bb.inputs['Base Color'].default_value = kit.srgb('#a7a5a1')
    bb.inputs['Roughness'].default_value = 0.8
    rnd = random.Random(4)
    S = 0.1  # maket ölçeği: 1 m → 0.1
    BL, BH, BT = 0.6 * S, 0.25 * S, 0.25 * S
    W, D = 7.2 * S, 4.8 * S
    KAT, SIRA = 3, 11
    FH = SIRA * BH + 0.2 * S
    mer, boy, don = [], [], []
    z0 = -0.38
    for kat in range(KAT):
        zk = z0 + kat * FH
        kit.box('Doseme', (W + 0.2 * S, D + 0.2 * S, 0.2 * S), (0, 0, zk - 0.1 * S), beton)
        for sira in range(SIRA):
            z = zk + (sira + 0.5) * BH
            ilerleme = (kat * SIRA + sira) / (KAT * SIRA)
            for yuz in range(4):
                uzun = W if yuz % 2 == 0 else D
                n = int(uzun / BL)
                for i in range(n + 1):
                    u = -uzun / 2 + (i + (0.5 if sira % 2 else 0.0)) * BL
                    a0, a1 = max(u, -uzun / 2), min(u + BL, uzun / 2)
                    if a1 - a0 < 0.004:
                        continue
                    parcalar = [(a0, a1)]
                    if 3 <= sira <= 8 and yuz % 2 == 0:  # pencere boşlukları: bloklar düzgün kesilir
                        for wc in (-0.22, 0.0, 0.22):
                            yeni = []
                            for (p0, p1) in parcalar:
                                w0, w1 = wc - 0.05, wc + 0.05
                                if p1 <= w0 or p0 >= w1:
                                    yeni.append((p0, p1))
                                    continue
                                if p0 < w0:
                                    yeni.append((p0, w0))
                                if p1 > w1:
                                    yeni.append((w1, p1))
                            parcalar = yeni
                    for (p0, p1) in parcalar:
                        if p1 - p0 < 0.003:
                            continue
                        uc, ul = (p0 + p1) / 2, (p1 - p0) - 0.0012
                        if yuz == 0:
                            c, sz = Vector((uc, -D / 2, z)), (ul, BT, BH * 0.97)
                        elif yuz == 2:
                            c, sz = Vector((uc, D / 2, z)), (ul, BT, BH * 0.97)
                        elif yuz == 1:
                            c, sz = Vector((W / 2, uc, z)), (BT, ul, BH * 0.97)
                        else:
                            c, sz = Vector((-W / 2, uc, z)), (BT, ul, BH * 0.97)
                        r = (0, 0, 0)
                        if ilerleme > 0.62:  # üst sıralar: yukarıdan iniyor, dağınık
                            e = (ilerleme - 0.62) / 0.38
                            c = c + Vector((rnd.uniform(-0.05, 0.05) * e, rnd.uniform(-0.05, 0.05) * e, (0.05 + rnd.uniform(0, 0.5)) * e ** 1.3))
                            r = (rnd.uniform(-0.6, 0.6) * e, rnd.uniform(-0.6, 0.6) * e, rnd.uniform(-0.8, 0.8) * e)
                        mer.append(c)
                        boy.append(sz)
                        don.append(r)
    kit.toplu_mesh('Bloklar', kit.sablon('kup'), [tuple(c) for c in mer], boy, don, mat)
    for x in (-W / 2, W / 2):
        for y in (-D / 2, D / 2):
            kit.box('Kolon', (0.35 * S, 0.35 * S, KAT * FH * 0.68), (x, y, z0 + KAT * FH * 0.34 - 0.1 * S), beton)
    kamera(hedef=(0, 0, 0.26), uzak=4.9, lens=55, fstop=8.0)


def cizim(sc):
    """Mimar çizimi: her şey kâğıt beyazı (ışıksız), grafit kontur; zemin aynı."""
    kagit = bpy.data.materials.new('Kagit')
    kagit.use_nodes = True
    nt = kagit.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = kit.srgb('#f7f4f0')
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(em.outputs[0], out.inputs['Surface'])
    for ob in bpy.data.objects:
        if ob.type == 'MESH':
            ob.data.materials.clear()
            ob.data.materials.append(kagit)
        if ob.type == 'LIGHT':
            ob.hide_render = True
    sc.view_settings.view_transform = 'Standard'
    sc.view_settings.look = 'None'
    w = sc.world.node_tree
    for n in w.nodes:
        if n.type == 'BACKGROUND':
            n.inputs['Color'].default_value = (*kit.srgb('#f7f4f0')[:3], 1)
            n.inputs['Strength'].default_value = 1.0
    sc.render.use_freestyle = True
    sc.render.line_thickness_mode = 'ABSOLUTE'
    vl = sc.view_layers[0]
    vl.use_freestyle = True
    fs = vl.freestyle_settings
    ls = fs.linesets[0] if len(fs.linesets) else fs.linesets.new('Cizgi')
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new('Grafit')
    ls.select_silhouette = ls.select_border = ls.select_crease = True
    ls.linestyle.color = (0.2, 0.23, 0.26)
    ls.linestyle.thickness = 0.9
    sc.compositing_node_group = None
    for c in bpy.data.cameras:
        c.dof.use_dof = False


def main():
    kit.reset()
    sc = kit.setup_render(1280, 720, samples=ARGS.samples, threshold=0.015, bounces=(6, 3, 3, 2))
    studyo(sc)
    {'blok': sahne_blok, 'dagilma': sahne_dagilma, 'kure': sahne_kure, 'bina': sahne_bina}[ARGS.sahne](sc)
    if ARGS.cizim:
        cizim(sc)
    os.makedirs(ARGS.out, exist_ok=True)
    kit.render_to(os.path.join(ARGS.out, f'{ARGS.ad or ARGS.sahne}.png'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--sahne', default='blok')
    ap.add_argument('--out', required=True)
    ap.add_argument('--ad', default='')
    ap.add_argument('--samples', type=int, default=64)
    ap.add_argument('--cizim', action='store_true')
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
