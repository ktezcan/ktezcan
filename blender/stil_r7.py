"""
Stil R7 — referans video dili ("konseptten gerçeğe"): fotogerçekçi final + sunum kareleri.

  gercek  : gerçek gökyüzü (bulutlu), güneş, ön bahçe (çim telleri, çalı, lavanta, giriş yolu,
            alçak duvar, bank), sokak, insanlar; göz hizası geniş açı
  aksam7  : aynı kadraj, gün batımı sonrası: pencereler yanar, lambalar
  plan    : tepeden vaziyet (koyu sunum zemini için ham kare)
  kafes   : siyah zeminde karkas beyaz, gazbeton duvarlar ışıyan tel kafes
  eskiz   : bej kâğıt üzerinde el çizimi (Freestyle, titrek çizgi)

Kullanım: python stil_r7.py --sahne <ad> --out DIR [--samples N]
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
import stil_r as R  # noqa: E402
import stil_r3 as T  # noqa: E402
import stil_r6 as K  # noqa: E402
import bina_detay as B  # noqa: E402
import sokak as S  # noqa: E402
import insan as I  # noqa: E402

Y_SOKAK = -8.6  # bahçe: bina önü (−4.6) ile kaldırım arası


def dunya_gok(sc, elev=34.0, rot=200.0, guc=0.2, bulut=True):
    import s3_bina as s3
    w = s3.sky_world(strength=guc, sun_elev=elev, sun_rot=rot)
    if bulut:
        nt = w.node_tree
        sky = nt.nodes['Sky Texture']
        bg = [n for n in nt.nodes if n.type == 'BACKGROUND'][0]
        tc = nt.nodes.new('ShaderNodeTexCoord')
        mp = nt.nodes.new('ShaderNodeMapping')
        mp.inputs['Scale'].default_value = (1.6, 1.6, 7.0)  # yassı bulut katmanları
        nt.links.new(tc.outputs['Generated'], mp.inputs['Vector'])
        nz = nt.nodes.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = 3.5
        nz.inputs['Detail'].default_value = 12.0
        nz.inputs['Roughness'].default_value = 0.62
        nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
        ramp = nt.nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].position = 0.48
        ramp.color_ramp.elements[1].position = 0.66
        nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac'])
        sep = nt.nodes.new('ShaderNodeSeparateXYZ')
        nt.links.new(tc.outputs['Generated'], sep.inputs[0])
        yuk = nt.nodes.new('ShaderNodeMapRange')  # ufka yakın bulut yok
        yuk.inputs['From Min'].default_value = 0.03
        yuk.inputs['From Max'].default_value = 0.25
        nt.links.new(sep.outputs['Z'], yuk.inputs['Value'])
        mul = nt.nodes.new('ShaderNodeMath')
        mul.operation = 'MULTIPLY'
        nt.links.new(ramp.outputs['Color'], mul.inputs[0])
        nt.links.new(yuk.outputs['Result'], mul.inputs[1])
        mix = nt.nodes.new('ShaderNodeMix')
        mix.data_type = 'RGBA'
        renk_giris = [i for i in mix.inputs if i.type == 'RGBA']  # A, B (renk soketleri)
        renk_cikis = [o for o in mix.outputs if o.type == 'RGBA'][0]
        bw = nt.nodes.new('ShaderNodeRGBToBW')  # bulut parlaklığı: göğün kendi parlaklığının 1.6 katı, beyaz
        nt.links.new(sky.outputs[0], bw.inputs[0])
        k = nt.nodes.new('ShaderNodeMath')
        k.operation = 'MULTIPLY'
        k.inputs[1].default_value = 1.6
        nt.links.new(bw.outputs[0], k.inputs[0])
        nt.links.new(k.outputs[0], renk_giris[1])
        nt.links.new(mul.outputs[0], mix.inputs['Factor'])
        nt.links.new(sky.outputs[0], renk_giris[0])
        nt.links.new(renk_cikis, bg.inputs['Color'])
    sd = bpy.data.lights.new('Gunes', 'SUN')
    sd.energy = 5.5
    sd.angle = math.radians(0.8)
    sd.color = (1.0, 0.95, 0.88)
    so = bpy.data.objects.new('Gunes', sd)
    so.rotation_euler = (math.radians(90 - max(elev, 5)), 0, math.radians(-32))  # ön soldan: gölgeler kameradan uzağa
    kit.link(so)
    sc.view_settings.look = 'AgX - Medium High Contrast'
    sc.view_settings.exposure = -0.35
    return w, so


def arazi():
    """Uzak zemin: kuru Ege toprağı/ot (gürültülü), puslu tepeler."""
    m = bpy.data.materials.new('Arazi')
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 0.08
    nz.inputs['Detail'].default_value = 10.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = kit.srgb('#8c8a5e')
    ramp.color_ramp.elements[1].color = kit.srgb('#b3a477')
    nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.95
    kit.box('Arazi', (1600, 1600, 0.1), (0, 0, -0.06), m)
    rnd = random.Random(7)
    for dist, renk, h in ((260, '#7f8a7a', 22), (420, '#95a0a3', 34), (600, '#aab5bc', 48)):
        mt = S.pbr('Tepe' + renk, renk, 1.0)
        for i in range(9):
            x = (i - 4) * 150 + rnd.uniform(-50, 50)
            bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1.0, location=(x, dist, -2.0))
            o = bpy.context.active_object
            o.scale = (rnd.uniform(90, 150), 50, h * rnd.uniform(0.6, 1.2))
            o.data.materials.append(mt)
            bpy.ops.object.shade_smooth()


def cimen(x0, x1, y0, y1, yogun=900, seed=1):
    """Çim telleri: ince dikey kartlar, üç ton yeşil."""
    rnd = random.Random(seed)
    alan = (x1 - x0) * (y1 - y0)
    n = int(alan * yogun)
    renk = ['#4f6b2f', '#62803a', '#7a9447']
    kit.box('CimTaban', (x1 - x0, y1 - y0, 0.04), ((x0 + x1) / 2, (y0 + y1) / 2, 0.14), S.pbr('CimTaban', '#4a5f2c', 0.9))
    for k in range(3):
        mer, b, d = [], [], []
        for _ in range(n // 3):
            h = rnd.uniform(0.05, 0.11)
            mer.append((rnd.uniform(x0, x1), rnd.uniform(y0, y1), 0.16 + h / 2))
            b.append((0.006, 0.0015, h))
            d.append((rnd.uniform(-0.35, 0.35), rnd.uniform(-0.35, 0.35), rnd.uniform(0, 6.3)))
        kit.toplu_mesh(f'Cim{k}', kit.sablon('kup'), mer, b, d, S.pbr(f'Cim{k}', renk[k], 0.55))


def cali(c, r=0.5, h=0.6, seed=0, renk='#3f5a2c'):
    rnd = random.Random(seed)
    mer, b, d = [], [], []
    for _ in range(int(2600 * r)):
        v = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), abs(rnd.gauss(0, 1)) * 0.8)).normalized()
        q = Vector(c) + Vector((v.x * r, v.y * r, v.z * h)) * rnd.random() ** 0.3
        mer.append(tuple(q))
        s = rnd.uniform(0.03, 0.055)
        b.append((s, s * 0.6, 0.003))
        d.append((rnd.uniform(0, 6.3), rnd.uniform(0, 6.3), rnd.uniform(0, 6.3)))
    kit.toplu_mesh('Cali', kit.sablon('kup'), mer, b, d, S.pbr('Cali' + renk, renk, 0.6))


def lavanta(c, r=0.35, seed=0):
    rnd = random.Random(seed)
    sap, bas = [], []
    for _ in range(int(500 * r)):
        a, rr = rnd.uniform(0, 6.3), r * math.sqrt(rnd.random())
        x, y = c[0] + rr * math.cos(a), c[1] + rr * math.sin(a)
        h = rnd.uniform(0.3, 0.5)
        sap.append(((x, y, c[2] + h / 2), (0.004, 0.004, h)))
        bas.append(((x, y, c[2] + h + 0.03), (0.012, 0.012, 0.07)))
    kit.toplu_mesh('LavSap', kit.sablon('kup'), [m for m, _ in sap], [s for _, s in sap], None, S.pbr('LavSap', '#6d7f52', 0.7))
    kit.toplu_mesh('LavBas', kit.sablon('kup'), [m for m, _ in bas], [s for _, s in bas], None, S.pbr('LavBas', '#7c6aa8', 0.6))


def bahce():
    yb = B.YS[0] - B.WT / 2 - 0.05  # bina ön yüzü
    tas = bpy.data.materials.get('KaldirimTas')
    yol = S.pbr('GirisYolu', '#d6d0c5', 0.7)
    kit.box('GirisYolu', (1.6, abs(Y_SOKAK - yb), 0.16), (0, (yb + Y_SOKAK) / 2, 0.08), yol)
    duvar = S.pbr('BahceDuvar', '#ece7de', 0.85)
    for s in (-1, 1):  # alçak bahçe duvarı (sıvalı gazbeton), girişte açıklık
        kit.box('BahceDuvar', (8.0, 0.2, 0.55), (s * 4.9, Y_SOKAK + 0.15, 0.275), duvar)
        kit.box('DuvarBaslik', (8.05, 0.26, 0.05), (s * 4.9, Y_SOKAK + 0.15, 0.575), S.pbr('Baslik', '#bdb7ad', 0.6))
        cimen(s * 0.85 if s > 0 else -8.9, 8.9 if s > 0 else -0.85, Y_SOKAK + 0.3, yb - 0.6, seed=3 + s)
        for i in range(5):
            cali((s * (1.6 + i * 1.5), Y_SOKAK + 0.75, 0.16), r=0.45, h=0.55, seed=10 + i + (s > 0) * 7,
                 renk=['#3f5a2c', '#4b6633', '#556b38'][i % 3])
        lavanta((s * 1.3, yb - 0.9, 0.16), r=0.4, seed=s + 5)
        lavanta((s * 7.6, yb - 1.1, 0.16), r=0.5, seed=s + 9)
    # bank
    ah = S.pbr('BankAhsap', '#9a6b43', 0.6)
    kit.box('Bank', (1.6, 0.42, 0.05), (-4.5, yb - 1.4, 0.62), ah)
    kit.box('BankSirt', (1.6, 0.05, 0.42), (-4.5, yb - 1.2, 0.86), ah)
    for x in (-5.2, -3.8):
        kit.box('BankAyak', (0.06, 0.4, 0.46), (x, yb - 1.4, 0.37), S.pbr('Demir', '#2d3135', 0.5, 0.6))
    S.agac((-6.8, yb - 2.2, 0.16), boy=7.5, seed=31)
    S.agac((7.0, yb - 2.0, 0.16), boy=6.8, seed=32)


def insanlar_bahce():
    yb = B.YS[0] - B.WT / 2 - 0.05
    I.insan('kadin', 'yuru', 0.3, dict(ust='#e7dfd2', alt='#3b4a5c', sac='#2b1e15'), konum=(0.2, yb - 1.6, 0.16), yon=0.15, ad='Bahce1')
    I.insan('kiz', 'yuru', 0.8, dict(ust='#d97a5a', alt='#2f3c4c', sac='#2b1e15'), konum=(0.75, yb - 1.9, 0.16), yon=0.1, ad='Bahce2')
    I.insan('yasli', 'otur', 0.0, dict(ust='#6f6a5f', alt='#3f3b36', sac='#c9c4bb', kol='uzun'), konum=(-4.4, yb - 1.42, -0.14), yon=0.0, ad='Bankta')


def komsular():
    """Komşu evler (sıva + kiremit) ve arkada ağaç dizisi: çevre boş kalmasın."""
    import stil_g as G
    M = G.Mahalle()
    sv = M.m['sivalar']
    for (x, y, w, d, k, i) in ((-24, -1, 9, 8, 2, 0), (23, -1, 8, 9, 3, 1), (-8, 22, 11, 8, 2, 2), (12, 21, 8, 8, 2, 0),
                               (-28, 20, 8, 8, 3, 1), (32, 18, 9, 8, 2, 2), (-44, 4, 10, 8, 2, 0), (44, 2, 9, 9, 3, 1)):
        M.ev(x, y, w, d, k, sv[i])
    rnd = random.Random(12)
    for i in range(14):
        S.agac((rnd.uniform(-60, 60), rnd.uniform(28, 55), 0.0), boy=rnd.uniform(7, 11), seed=100 + i)


def sahne_gercek(sc, aksam=False):
    P = K.bina_ve_odalar(sc, isik=aksam)
    for ob in bpy.data.objects:  # stüdyo ışıkları kapalı: gerçek gök + güneş
        if ob.type == 'LIGHT' and ob.data.type == 'AREA':
            ob.data.energy = 0
    K.sokak_doldur(Y_SOKAK, yakin=(-17.0, -9.5, 20.0), uzak=(-20.0, -30.0))
    K.temel_gizle()
    bahce()
    insanlar_bahce()
    arazi()
    komsular()
    if aksam:
        dunya_gok(sc, elev=-2.0, rot=250.0, guc=0.5, bulut=False)
        for ob in bpy.data.objects:
            if ob.name == 'Gunes':
                ob.data.energy = 0.0
        sc.view_settings.exposure = 1.6
        for ob in bpy.data.objects:
            if ob.name.startswith('LambaCam') and ob.data.materials:
                ob.data.materials[0] = S.pbr('LambaCamYanik', '#fff4dc', 0.2, 0.0, '#ffd59a', 14.0)
                ld = bpy.data.lights.new('SokakLamba', 'SPOT')
                ld.energy = 1200
                ld.spot_size = math.radians(120)
                ld.color = (1.0, 0.8, 0.55)
                lo = bpy.data.objects.new('SokakLamba', ld)
                lo.location = ob.matrix_world.translation - Vector((0, 0, 0.1))
                kit.link(lo)
        kit.sinematik(bloom=0.4, esik=1.2, boyut=0.6)
    else:
        dunya_gok(sc)
    cam = R.kamera(hedef=(-0.5, -4.0, 4.6), yon=(0.62, -1.0, 0.02), uzak=24.0, lens=24, fstop=11, kayma=0.0)
    return cam


def sahne_aksam7(sc):
    sahne_gercek(sc, aksam=True)


SAHNELER = {k[6:]: v for k, v in globals().items() if k.startswith('sahne_')}


def main():
    kit.reset()
    sc = kit.setup_render(1280, 720, samples=ARGS.samples, threshold=0.02, bounces=(6, 3, 3, 4))
    sc.cycles.transparent_max_bounces = 16
    R.studyo(sc)
    SAHNELER[ARGS.sahne](sc)
    os.makedirs(ARGS.out, exist_ok=True)
    kit.render_to(os.path.join(ARGS.out, f'{ARGS.sahne}.png'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--sahne', default='gercek')
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=48)
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
