"""
Stil R — hikâye panosu için ek sahneler (stil_r.py'nin devamı).

  kumeler : 5 hammadde kümesi havada (kum, kireç, çimento, alçı, alüminyum)
  girdap  : hammaddeler sarmal girdapta karışır
  dogus   : hücreler içeri akar, blok yeniden doğar
  kalem   : bina mimar kalemiyle çizilir; ilk sıralar gerçeğe dönmüş
  bina2   : tamamlanmış bina (cam, doğrama, kolon, döşeme) gün ışığında
  aksam   : gün biter — pencereler yanar, lime güven halkası, aile silüeti
  deprem  : 'güvenli, çünkü hafif' — zeminde sakin dalga halkaları, bina dingin
  dunya   : nokta küre, Türkiye lime, 5 kıtaya yaylar (akşam zemini)

Kullanım: python stil_r2.py --sahne <ad> --out DIR [--samples N]
"""
import argparse
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402
import stil_r as R  # noqa: E402

KAM_YON = Vector((0.75, -1.0, 0.42)).normalized()
HAM = [  # ad, renk, pürüz, metal, pay
    ('kum', '#d6c29a', 0.85, 0.0, 0.42),
    ('kirec', '#f5f3ee', 0.9, 0.0, 0.2),
    ('cimento', '#9ea3a4', 0.8, 0.0, 0.16),
    ('alci', '#e6dcd3', 0.9, 0.0, 0.12),
    ('aluminyum', '#d9dee2', 0.22, 1.0, 0.10),
]


def pbr(name, hexcol, rough=0.7, metal=0.0, emis=None, es=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = kit.srgb(hexcol)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if emis:
        b.inputs['Emission Color'].default_value = kit.srgb(emis)
        b.inputs['Emission Strength'].default_value = es
    return m


def baz():
    """Kamera tabanı: sağ ve yukarı vektörleri (kümeleri ekran düzleminde dizmek için)."""
    sag = KAM_YON.cross(Vector((0, 0, 1))).normalized() * -1
    yuk = sag.cross(KAM_YON).normalized() * -1
    return sag, yuk


def kume(name, merkez, n, r, boy, mat, rnd, yassi=False):
    mer, b, d = [], [], []
    for _ in range(n):
        v = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1)))
        v = v.normalized() * r * (rnd.random() ** 0.6)
        mer.append(tuple(Vector(merkez) + v))
        s = boy * rnd.uniform(0.55, 1.3)
        b.append((s, s, s * 0.18) if yassi else (s, s * rnd.uniform(0.7, 1.0), s * rnd.uniform(0.7, 1.0)))
        d.append((rnd.uniform(0, 6.3), rnd.uniform(0, 6.3), rnd.uniform(0, 6.3)))
    return kit.toplu_mesh(name, kit.sablon('kup'), mer, b, d, mat)


def sahne_kumeler(sc):
    rnd = random.Random(2)
    sag, yuk = baz()
    for k, (ad, renk, pr, mt, _) in enumerate(HAM):
        c = sag * ((k - 2) * 0.19 - 0.07) + yuk * (0.06 * math.cos((k - 2) * 1.1))
        kume(ad, c, 2200, 0.1, 0.008, pbr('M_' + ad, renk, pr, mt), rnd, yassi=(ad == 'aluminyum'))
    R.kamera(hedef=(0, 0, 0), uzak=2.6, lens=55, fstop=6.0)
    kit.sinematik(bloom=0.2, esik=1.6, boyut=0.5)


def sahne_girdap(sc):
    """Sarmal girdap: dışta seyrek ve hızlı (teğete uzamış), merkezde yoğun karışım topu."""
    rnd = random.Random(5)
    mats = [pbr('M_' + h[0], h[1], h[2], h[3]) for h in HAM]
    for k, (ad, renk, pr, mt, pay) in enumerate(HAM):
        mer, b, d = [], [], []
        for i in range(int(9000 * pay)):
            r = 0.04 + 0.62 * rnd.random() ** 1.6
            kol = rnd.randrange(3)
            th = kol * 2.094 + 2.6 * math.log(r / 0.04) + rnd.gauss(0, 0.22)
            z = rnd.gauss(0, 0.025) + 0.05 * math.sin(th * 2) * r
            mer.append((r * math.cos(th), r * math.sin(th), z))
            s = 0.008 * rnd.uniform(0.6, 1.2)
            uz = 1.0 + 3.5 * min(1.0, r / 0.5)  # dışta hız izi
            b.append((s * uz, s * 0.8, s * 0.8))
            d.append((0.0, 0.0, th + math.pi / 2))
        kit.toplu_mesh('Girdap_' + ad, kit.sablon('kup'), mer, b, d, mats[k])
    # merkezde yoğun karışım
    kume('Karisim', (0, 0, 0), 2600, 0.07, 0.007, pbr('M_karisim', '#e2ded6', 0.8), rnd)
    R.kamera(hedef=(0, 0, 0), yon=(0.55, -1.0, 0.85), uzak=3.1, lens=55, fstop=5.6)
    kit.sinematik(bloom=0.2, esik=1.6, boyut=0.5)


def kabuk_noktalari(n=3800, R0=0.5, acik=0.55, rnd=None):
    rnd = rnd or random.Random(9)
    ga = math.pi * (3 - math.sqrt(5))
    out = []
    for i in range(n):
        y = 1 - 2 * (i + 0.5) / n
        r = math.sqrt(1 - y * y)
        d = Vector((math.cos(ga * i) * r, math.sin(ga * i) * r, y))
        if d.dot(KAM_YON) > acik:
            continue
        out.append(d * R0)
    return out


def sahne_dogus(sc):
    """Hücreler kabuktan içeri akar; ortada gerçek blok belirir (yüzeyine yapışan son hücreler)."""
    rnd = random.Random(11)
    mat = kit.aac_material('Gazbeton', bump=1.0)
    blk = kit.gecmeli_blok('Blok', 0.6, 0.25, 0.25, mat)
    blk.location = (0, 0, -0.125)
    hucre = pbr('Hucre', '#f1ece6', 0.55)
    mer, b = [], []
    for p in kabuk_noktalari(n=1700, rnd=rnd):
        w = rnd.random() ** 0.3  # 0 kabukta … 1 blok yüzeyinde
        hedef = Vector((rnd.uniform(-0.3, 0.3), rnd.uniform(-0.125, 0.125), rnd.uniform(-0.125, 0.125)))
        ax = rnd.randrange(3)
        hedef[ax] = math.copysign((0.3, 0.125, 0.125)[ax] + 0.006, hedef[ax] or 1)
        p2 = p * 1.25
        q = p2.lerp(hedef, w)
        mer.append(tuple(q))
        b.append(0.02 * (1 - 0.6 * w) * rnd.uniform(0.8, 1.2))
    kit.toplu_mesh('Hucreler', kit.sablon('ico', 2), mer, b, None, hucre, yumusak=True)
    # içten sönen sıcak ışık (otoklavın son ısısı)
    ld = bpy.data.lights.new('Iz', 'POINT')
    ld.energy = 25
    ld.color = R.AMBER
    lo = bpy.data.objects.new('Iz', ld)
    lo.location = (0, -0.25, 0.25)
    kit.link(lo)
    R.kamera(hedef=(0, 0, 0), uzak=3.2, lens=55, fstop=5.6)


# ------------------------------------------------------------------ bina (maket ölçeği)
S = 0.1
BL, BH, BT = 0.6 * S, 0.25 * S, 0.25 * S
W, D = 7.2 * S, 4.8 * S
KAT, SIRA = 3, 11
FH = SIRA * BH + 0.2 * S
Z0 = -0.38
PENCERE_U = (-0.22, 0.0, 0.22)
PW = 0.05  # pencere yarı genişliği


def duvar_bloklari(sinir=1.0, rnd=None, ucus=0.0):
    """Tüm duvar blokları (merkez, boyut, dönme, ilerleme). sinir: bu ilerlemeden sonrası yok;
    ucus > 0: üst sıralar havada (iniyor)."""
    rnd = rnd or random.Random(4)
    mer, boy, don = [], [], []
    for kat in range(KAT):
        zk = Z0 + kat * FH
        for sira in range(SIRA):
            ilerleme = (kat * SIRA + sira) / (KAT * SIRA)
            if ilerleme > sinir:
                continue
            z = zk + (sira + 0.5) * BH
            for yuz in range(4):
                uzun = W if yuz % 2 == 0 else D
                for i in range(int(uzun / BL) + 1):
                    u = -uzun / 2 + (i + (0.5 if sira % 2 else 0.0)) * BL
                    a0, a1 = max(u, -uzun / 2), min(u + BL, uzun / 2)
                    if a1 - a0 < 0.004:
                        continue
                    parca = [(a0, a1)]
                    if 3 <= sira <= 8 and yuz % 2 == 0:
                        for wc in PENCERE_U:
                            yeni = []
                            for (p0, p1) in parca:
                                w0, w1 = wc - PW, wc + PW
                                if p1 <= w0 or p0 >= w1:
                                    yeni.append((p0, p1))
                                    continue
                                if p0 < w0:
                                    yeni.append((p0, w0))
                                if p1 > w1:
                                    yeni.append((w1, p1))
                            parca = yeni
                    for (p0, p1) in parca:
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
                        if ucus and ilerleme > sinir - ucus:
                            e = (ilerleme - (sinir - ucus)) / ucus
                            c = c + Vector((rnd.uniform(-0.04, 0.04) * e, rnd.uniform(-0.04, 0.04) * e, (0.04 + rnd.uniform(0, 0.4)) * e ** 1.3))
                            r = (rnd.uniform(-0.5, 0.5) * e, rnd.uniform(-0.5, 0.5) * e, rnd.uniform(-0.7, 0.7) * e)
                        mer.append(tuple(c))
                        boy.append(sz)
                        don.append(r)
    return mer, boy, don


def iskelet(beton, katlar=KAT, cati=True):
    """Betonarme: döşemeler, köşe + ara kolonlar, çatı döşemesi."""
    for kat in range(katlar + (1 if cati else 0)):
        zk = Z0 + kat * FH
        kit.box('Doseme', (W + 0.3 * S, D + 0.3 * S, 0.2 * S), (0, 0, zk - 0.1 * S), beton)
    for x in (-W / 2, -W / 6, W / 6, W / 2):
        for y in (-D / 2, D / 2):
            kit.box('Kolon', (0.32 * S, 0.32 * S, katlar * FH), (x, y, Z0 + katlar * FH / 2), beton)
    for y in (0.0,):  # köşeler yukarıda; burada yalnız yan cephe ortası
        for x in (-W / 2, W / 2):
            kit.box('Kolon', (0.32 * S, 0.32 * S, katlar * FH), (x, y, Z0 + katlar * FH / 2), beton)


def pencereler(cam_m, dograma_m, katlar=KAT, isikli=None, rnd=None):
    """Her cephede (±Y) pencere: beyaz doğrama + cam; isikli: yanan pencere malzemesi."""
    rnd = rnd or random.Random(8)
    yanan = []
    for kat in range(katlar):
        zc = Z0 + kat * FH + 6 * BH
        for y in (-D / 2, D / 2):
            for wc in PENCERE_U:
                kit.box('Dograma', (2 * PW, BT * 0.3, 6 * BH), (wc, y, zc), dograma_m)
                m = isikli if (isikli and rnd.random() < 0.75) else cam_m
                g = kit.box('Cam', (2 * PW - 0.008, BT * 0.34, 6 * BH - 0.008), (wc, y, zc), m)
                if m is isikli:
                    yanan.append(g)
    return yanan


def bina_malzeme():
    return (kit.aac_material('Gazbeton', bump=0.4, tex_size=0.24), pbr('Beton', '#a9a7a2', 0.8),
            pbr('Cam', '#2a333b', 0.04, 0.0), pbr('DogramaM', '#f2f1ec', 0.45))


def sahne_bina2(sc, aksam=False):
    aac, beton, cam_m, dog = bina_malzeme()
    mer, boy, don = duvar_bloklari(1.0)
    kit.toplu_mesh('Bloklar', kit.sablon('kup'), mer, boy, don, aac)
    iskelet(beton)
    isik = pbr('CamIsik', '#2a333b', 0.1, 0.0, '#ffb978', 6.0) if aksam else None
    pencereler(cam_m, dog, isikli=isik)
    R.kamera(hedef=(0, 0, 0.12), uzak=4.6, lens=55, fstop=8.0)


def aksam_studyo(sc, koyu='#2f3846'):
    """Gün biter: zemin akşam mavisi, anahtar ışık sıcak ve alçak, dolgu soğuk."""
    w = sc.world.node_tree
    for n in w.nodes:
        if n.type == 'BACKGROUND':
            n.inputs['Color'].default_value = (*kit.srgb(koyu)[:3], 1)
            n.inputs['Strength'].default_value = 0.9 if n.inputs['Strength'].default_value > 1 else 0.1
    for ob in bpy.data.objects:
        if ob.type != 'LIGHT':
            continue
        if ob.name.startswith('Anahtar'):
            ob.location = (-2.4, -0.6, 0.55)
            kit.aim(ob, (0, 0, 0))
            ob.data.color = (1.0, 0.62, 0.36)
            ob.data.energy *= 0.55
        elif ob.name.startswith('Dolgu'):
            ob.data.color = (0.55, 0.65, 0.9)
            ob.data.energy *= 1.4
        elif ob.name.startswith('Kontur'):
            ob.data.color = (0.75, 0.82, 1.0)
            ob.data.energy *= 0.7


def siluetler(m):
    """1. kat ön pencerede aile: iki yetişkin, bir çocuk (düz siyah)."""
    zc = Z0 + 1 * FH
    for x, boy in ((-0.012, 1.78), (0.006, 1.62), (0.02, 1.1)):
        k = boy / 1.75 * S
        kit.box('Siluet', (0.34 * k, 0.02, 0.62 * k), (x, -D / 2 + 0.02, zc + 0.95 * k + 0.2 * S), m)
        kit.box('Siluet', (0.28 * k, 0.02, 0.8 * k), (x, -D / 2 + 0.02, zc + 0.4 * k + 0.2 * S), m)
        kit.box('Siluet', (0.18 * k, 0.02, 0.2 * k), (x, -D / 2 + 0.02, zc + 1.42 * k + 0.2 * S), m)


def sahne_aksam(sc):
    sahne_bina2(sc, aksam=True)
    aksam_studyo(sc)
    siluetler(pbr('Siluet', '#141414', 0.9))
    halka = kit.halo_ring('Halka', radius=0.62, width=0.01, strength=9.0, segments=256, z=Z0 - 0.02)
    halka.location.z = 0
    # iç ışık: pencerelerden sızan sıcaklık
    for x in (-0.22, 0.0, 0.22):
        for kat in range(KAT):
            ld = bpy.data.lights.new('Ic', 'POINT')
            ld.energy = 0.6
            ld.color = (1.0, 0.7, 0.42)
            ld.shadow_soft_size = 0.05
            lo = bpy.data.objects.new('Ic', ld)
            lo.location = (x, -D / 2 + 0.06, Z0 + kat * FH + 6 * BH)
            kit.link(lo)
    kit.sinematik(bloom=0.45, esik=1.0, boyut=0.65)


def sahne_deprem(sc):
    """Güvenli, çünkü hafif: bina dingin, zeminde lime dalga halkaları yayılır (sakin, yük azlığı)."""
    sahne_bina2(sc)
    for i, r in enumerate((0.7, 0.95, 1.25, 1.6)):
        h = kit.halo_ring(f'Dalga{i}', radius=r, width=0.006 + 0.003 * i, strength=6.0 * (1 - i * 0.22), segments=256, z=0)
        h.location.z = Z0 - 0.02
    R.kamera(hedef=(0, 0, -0.02), yon=(0.75, -1.0, 0.62), uzak=5.4, lens=55, fstop=8.0)
    kit.sinematik(bloom=0.35, esik=1.2, boyut=0.6)


def sahne_kalem(sc):
    """Kalem çizimi: tüm bina grafit çizgilerle; alt sıralar gerçeğe dönmüş (sol alttan başlar)."""
    aac, beton, cam_m, dog = bina_malzeme()
    grafit = pbr('Grafit', '#2a3035', 0.6)
    t = 0.0036  # çizgi kalınlığı
    seg = []  # (a, b)

    def kutu_kenar(cx, cy, cz, sx, sy, sz):
        x0, x1, y0, y1, z0, z1 = cx - sx / 2, cx + sx / 2, cy - sy / 2, cy + sy / 2, cz - sz / 2, cz + sz / 2
        P = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        for a, b in ((0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)):
            seg.append((P[a], P[b]))
    H = KAT * FH
    kutu_kenar(0, 0, Z0 + H / 2, W, D, H)
    for kat in range(KAT + 1):
        kutu_kenar(0, 0, Z0 + kat * FH - 0.1 * S, W + 0.3 * S, D + 0.3 * S, 0.2 * S)
    for kat in range(KAT):
        zc = Z0 + kat * FH + 6 * BH
        for y in (-D / 2, D / 2):
            for wc in PENCERE_U:
                kutu_kenar(wc, y, zc, 2 * PW, 0.0005, 6 * BH)
    for x in (-W / 6, W / 6):
        seg.append(((x, -D / 2, Z0), (x, -D / 2, Z0 + H)))
    # ölçü çizgileri (mimari çizim dili; yazı yok)
    for (a, b) in (((-W / 2, -D / 2 - 0.12, Z0), (W / 2, -D / 2 - 0.12, Z0)), ((W / 2 + 0.12, -D / 2, Z0), (W / 2 + 0.12, D / 2, Z0))):
        seg.append((a, b))
    mer, boy = [], []
    for a, b in seg:
        a, b = Vector(a), Vector(b)
        c = (a + b) / 2
        d = b - a
        ax = max(range(3), key=lambda i: abs(d[i]))
        sz = [t, t, t]
        sz[ax] = abs(d[ax]) + t
        mer.append(tuple(c))
        boy.append(tuple(sz))
    kit.toplu_mesh('Cizgiler', kit.sablon('kup'), mer, boy, None, grafit)
    # gerçeğe dönen ilk sıralar + zemin döşemesi
    mer, boy, don = duvar_bloklari(0.16, ucus=0.06)
    kit.toplu_mesh('Bloklar', kit.sablon('kup'), mer, boy, don, aac)
    kit.box('Doseme', (W + 0.3 * S, D + 0.3 * S, 0.2 * S), (0, 0, Z0 - 0.1 * S), beton)
    R.kamera(hedef=(0, 0, 0.12), uzak=4.6, lens=55, fstop=8.0)


def sahne_dunya(sc):
    """Akşam zemininde nokta küre: kara noktaları beyaz, Türkiye lime; 5 kıtaya lime yaylar."""
    import s4_dunya as G
    aksam_studyo(sc, koyu='#232b36')
    pts = json.load(open(os.path.join(kit.TEX_DIR, 'kara_noktalari.json')))
    rot = G.globe_rotation()
    beyaz = pbr('Nokta', '#eeeae4', 0.6)
    lime = pbr('NoktaTR', '#b8d84a', 0.5, 0.0, '#b8d84a', 3.0)
    for grup, m in ((False, beyaz), (True, lime)):
        mer = [tuple(rot @ G.ll2v(la, lo, 1.0)) for la, lo, k in pts if (k == 5) == grup]
        kit.toplu_mesh('Kara' + ('TR' if grup else ''), kit.sablon('ico', 1), mer, [0.0055] * len(mer), None, m, yumusak=True)
    # okyanus: mat koyu küre (noktalar öne çıksın)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=0.985)
    o = bpy.context.active_object
    o.data.materials.append(pbr('Okyanus', '#2b3440', 0.55))
    bpy.ops.object.shade_smooth()
    yay = pbr('Yay', '#b8d84a', 0.4, 0.0, '#b8d84a', 6.0)
    for i, (_, la, lo, _) in enumerate(G.TARGETS):
        a = G.arc_object(f'Yay{i}', G.IZMIR, (la, lo), rot, yay)
        a.data.bevel_factor_end = 1.0
    src = kit.halo_ring('IzmirHalka', radius=0.05, width=0.004, strength=8.0, segments=96)
    from mathutils import Matrix
    n_ = G.ll2v(*G.IZMIR, 1.004)
    src.matrix_world = rot @ Matrix.Translation(n_) @ n_.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    R.kamera(hedef=(0, 0, 0), yon=(0.0, -1.0, 0.25), uzak=4.4, lens=55, fstop=11.0)
    kit.sinematik(bloom=0.45, esik=1.0, boyut=0.6)


SAHNELER = {
    'kumeler': sahne_kumeler, 'girdap': sahne_girdap, 'dogus': sahne_dogus, 'kalem': sahne_kalem,
    'bina2': sahne_bina2, 'aksam': sahne_aksam, 'deprem': sahne_deprem, 'dunya': sahne_dunya,
}


def main():
    kit.reset()
    sc = kit.setup_render(1280, 720, samples=ARGS.samples, threshold=0.015, bounces=(6, 3, 3, 2))
    R.studyo(sc)
    SAHNELER[ARGS.sahne](sc)
    os.makedirs(ARGS.out, exist_ok=True)
    kit.render_to(os.path.join(ARGS.out, f'{ARGS.sahne}.png'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--sahne', default='kumeler')
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=48)
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
