"""
Stil R — 12 vuruşun her biri için ikinci efekt önerisi (B) + ayrıntılı binayla yenilenen A'lar.

Kullanım: python stil_r3.py --sahne <ad> --out DIR [--samples N]
Sahneler: makro kumsaati kaideler kalip telkesim otoklav cizim isikcizim kalem2 tarama
          insa patlatma bitmis dalga yukyolu aksam2 kesit blokkure
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
from mathutils import Vector, Matrix  # noqa: E402
import stil_r as R  # noqa: E402
import stil_r2 as Q  # noqa: E402
import bina_detay as B  # noqa: E402

LIME = '#b8d84a'


def olcekle(k, hedef=(0, 0, 0), guc=0.56):
    """Stüdyo ışıklarını sahne ölçeğine büyüt (bina ~14×)."""
    for ob in bpy.data.objects:
        if ob.type == 'LIGHT' and ob.data.type == 'AREA':
            ob.location = ob.location * k + Vector(hedef)
            ob.data.energy *= k * k * guc
            ob.data.size *= k
            kit.aim(ob, hedef)


def bina_kamera(uzak=48, yon=(0.75, -1.0, 0.42), hedef=(0, 0, 4.6), fstop=11, lens=55):
    return R.kamera(hedef=hedef, yon=yon, uzak=uzak, lens=lens, fstop=fstop)


def grafit_m():
    return Q.pbr('Grafit', '#2a3035', 0.6)


def lime_m(g=4.0):
    return Q.pbr('LimeIsik', LIME, 0.4, 0.0, LIME, g)


# ------------------------------------------------------------------ 1–6: blok ve üretim
def sahne_makro(sc):
    mat = kit.aac_material('Gazbeton', bump=1.4)
    b = kit.gecmeli_blok('Blok', 0.6, 0.25, 0.25, mat)
    b.location = (0, 0, -0.125)
    for ob in bpy.data.objects:
        if ob.name.startswith('Anahtar'):  # sıyırma ışığı: yüzeye çok yatık → gözenek dokusu
            ob.location = (1.3, -0.32, 0.18)
            kit.aim(ob, (0.1, -0.125, 0.05))
            ob.data.size = 0.4
            ob.data.energy = 60
    R.kamera(hedef=(0.22, -0.125, 0.06), yon=(0.55, -1.0, 0.35), uzak=0.8, lens=85, fstop=4.0, kayma=-0.12)


def sahne_kumsaati(sc):
    """Bloğun altı akıp kum saati gibi aşağıda yığın olur."""
    rnd = random.Random(3)
    mat = kit.aac_material('Gazbeton', bump=0.8)
    govde = kit.box('Govde', (0.6, 0.25, 0.17), (0, 0, 0.085 + 0.04), mat)
    kit.bevel(govde, 0.003, 3)
    a = 0.0125
    mer, boy, don = [], [], []
    for i in range(48):  # alt sıra: düzensiz kopan küpler
        for j in range(20):
            for k in range(3):
                if rnd.random() < 0.55 - 0.15 * k:
                    mer.append((-0.3 + (i + 0.5) * a, -0.125 + (j + 0.5) * a, 0.04 - (k + 0.5) * a + 0.02 * rnd.random()))
                    boy.append(a * 0.95)
                    don.append((0, 0, 0))
    # akan sütun
    for _ in range(4200):
        t = rnd.random() ** 0.8
        z = 0.0 - t * 0.5
        r = 0.02 + 0.13 * (1 - t) ** 2 * rnd.random()
        th = rnd.uniform(0, 6.283)
        mer.append((r * math.cos(th) * 1.8, r * math.sin(th), z))
        s = 0.006 * rnd.uniform(0.6, 1.3)
        boy.append((s, s, s * (1 + 2.5 * t)))
        don.append((rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), rnd.uniform(0, 6)))
    # yığın (koni)
    for _ in range(9000):
        rr = 0.24 * math.sqrt(rnd.random())
        th = rnd.uniform(0, 6.283)
        h = 0.14 * (1 - rr / 0.24) * rnd.random() ** 0.3
        mer.append((rr * math.cos(th), rr * math.sin(th), -0.62 + h))
        s = 0.006 * rnd.uniform(0.6, 1.3)
        boy.append(s)
        don.append((rnd.uniform(0, 6), rnd.uniform(0, 6), rnd.uniform(0, 6)))
    kit.toplu_mesh('Tanecik', kit.sablon('kup'), mer, boy, don, mat)
    R.kamera(hedef=(0, 0, -0.2), yon=(0.75, -1.0, 0.25), uzak=3.4, lens=55, fstop=6.0)


def sahne_kaideler(sc):
    """Beş beyaz kaide üstünde beş hammadde yığını (müze vitrini)."""
    rnd = random.Random(4)
    kaide = Q.pbr('Kaide', '#f4f1ed', 0.6)
    sag, yuk = Q.baz()
    for k, (ad, renk, pr, mt, _) in enumerate(Q.HAM):
        c = sag * ((k - 2) * 0.2 - 0.05)
        h = 0.32 + 0.05 * math.cos(k * 1.3)
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.07, depth=h, location=(c.x, c.y, -0.3 + h / 2))
        o = bpy.context.active_object
        o.data.materials.append(kaide)
        bpy.ops.object.shade_smooth()
        kit.bevel(o, 0.004, 3, 30)
        m = Q.pbr('M_' + ad, renk, pr, mt)
        mer, boy, don = [], [], []
        top = -0.3 + h
        for _ in range(2600):
            rr = 0.062 * math.sqrt(rnd.random())
            th = rnd.uniform(0, 6.283)
            hz = 0.075 * (1 - rr / 0.062) ** 1.2 * rnd.random() ** 0.25
            mer.append((c.x + rr * math.cos(th), c.y + rr * math.sin(th), top + hz + 0.003))
            s = 0.0045 * rnd.uniform(0.6, 1.3)
            boy.append((s, s, s * 0.2) if ad == 'aluminyum' else s)
            don.append((rnd.uniform(0, 6), rnd.uniform(0, 6), rnd.uniform(0, 6)))
        kit.toplu_mesh('Yigin_' + ad, kit.sablon('kup'), mer, boy, don, m)
    R.kamera(hedef=(0, 0, 0.0), yon=(0.75, -1.0, 0.32), uzak=2.4, lens=55, fstop=5.6)


def sahne_kalip(sc):
    """Beş hammadde şerit şerit akarak çelik döküm kalıbına dolar."""
    rnd = random.Random(6)
    celik = Q.pbr('Celik', '#60666b', 0.35, 0.8)
    L, T, H, e = 0.8, 0.36, 0.26, 0.012
    z0 = -0.3
    kit.box('KalipTaban', (L, T, e), (0, 0, z0), celik)
    for sx in (-1, 1):
        kit.box('KalipYan', (e, T, H), (sx * L / 2, 0, z0 + H / 2), celik)
        kit.box('KalipYan', (L, e, H), (0, sx * T / 2, z0 + H / 2), celik)
    kit.box('Bulamac', (L - e, T - e, 0.006), (0, 0, z0 + 0.13), Q.pbr('Bulamac', '#d8d4cc', 0.18))
    sag, yuk = Q.baz()
    for k, (ad, renk, pr, mt, _) in enumerate(Q.HAM):
        m = Q.pbr('M_' + ad, renk, pr, mt)
        p0 = sag * ((k - 2) * 0.32) + Vector((0, 0, 0.75))
        p2 = Vector(((k - 2) * 0.09, rnd.uniform(-0.05, 0.05), z0 + 0.13))
        p1 = (p0 + p2) / 2 + Vector((0, 0, 0.25))
        mer, boy, don = [], [], []
        for _ in range(1600):
            t = rnd.random()
            q = p0 * (1 - t) ** 2 + p1 * 2 * t * (1 - t) + p2 * t * t
            q = q + Vector((rnd.gauss(0, 0.012), rnd.gauss(0, 0.012), rnd.gauss(0, 0.008))) * (0.4 + t)
            mer.append(tuple(q))
            s = 0.005 * rnd.uniform(0.6, 1.3)
            boy.append((s, s, s * 0.2) if ad == 'aluminyum' else s)
            don.append((rnd.uniform(0, 6), rnd.uniform(0, 6), rnd.uniform(0, 6)))
        kit.toplu_mesh('Serit_' + ad, kit.sablon('kup'), mer, boy, don, m)
    R.kamera(hedef=(0, 0, 0.18), yon=(0.7, -1.0, 0.5), uzak=3.6, lens=55, fstop=6.0)


def sahne_telkesim(sc):
    """Kabarmış kek, gergin çelik tellerle bloklara kesilir (sağ yarı kesilmiş, sol yarı bütün)."""
    mat = kit.aac_material('Gazbeton', bump=0.7)
    celik = Q.pbr('Tel', '#d6dadd', 0.18, 1.0)
    Lx, Ty, Hz = 1.2, 0.5, 0.5
    x_tel = 0.05  # tellerin şu anki konumu
    kit.box('KekButun', (x_tel + Lx / 2, Ty, Hz), ((-Lx / 2 + x_tel) / 2, 0, 0), mat)
    # kesilmiş kısım: 60×25×(kalınlık) bloklar, aralar açılmış
    nx = int((Lx / 2 - x_tel) / 0.2)
    for i in range(nx):
        for k in range(2):
            gx = x_tel + (i + 0.5) * 0.2 + i * 0.006
            gz = -Hz / 4 + k * Hz / 2 + k * 0.006
            b = kit.box('KekBlok', (0.2 - 0.004, Ty, Hz / 2 - 0.004), (gx + 0.006, 0, gz), mat)
            kit.bevel(b, 0.002, 2)
    # teller: dikey (konumda) ve yatay; üstte çerçeve
    for y in [-Ty / 2 + i * Ty / 6 for i in range(7)]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.0012, depth=Hz + 0.5, location=(x_tel, y, 0))
        bpy.context.active_object.data.materials.append(celik)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.0012, depth=Lx + 0.4, location=(0, 0, 0), rotation=(0, math.pi / 2, 0))
    bpy.context.active_object.data.materials.append(celik)
    kit.box('Cerceve', (0.03, Ty + 0.2, 0.03), (x_tel, 0, Hz / 2 + 0.25), celik)
    kit.box('Cerceve', (0.03, Ty + 0.2, 0.03), (x_tel, 0, -Hz / 2 - 0.25), celik)
    R.kamera(hedef=(0.1, 0, 0.0), yon=(0.8, -1.0, 0.45), uzak=3.4, lens=55, fstop=6.0)


def sahne_otoklav(sc):
    """Blok, sıcak ışık halkasından (otoklav) geçer; arkada sönen ikinci halka, buhar zerreleri."""
    rnd = random.Random(8)
    mat = kit.aac_material('Gazbeton', bump=0.8)
    b = kit.gecmeli_blok('Blok', 0.6, 0.25, 0.25, mat)
    b.location = (0.12, 0, -0.125)
    for i, (x, g, r) in enumerate(((0.0, 7.0, 0.36), (-0.55, 2.5, 0.33), (-1.1, 0.9, 0.3))):
        bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.012, major_segments=128, minor_segments=16,
                                         location=(x, 0, 0), rotation=(0, math.pi / 2, 0))
        o = bpy.context.active_object
        o.data.materials.append(Q.pbr(f'Halka{i}', '#ffb070', 0.5, 0.0, '#ffa860', g))
    pts = [(rnd.uniform(-1.2, 0.3), rnd.gauss(0, 0.2), rnd.gauss(0, 0.2)) for _ in range(500)]
    kit.toplu_mesh('Buhar', kit.sablon('ico', 1), pts, [0.0035] * len(pts), None,
                   R.isiltili('Buhar', (1.0, 0.85, 0.7), 2.5), yumusak=True)
    R.kamera(hedef=(-0.15, 0, 0), yon=(0.45, -1.0, 0.2), uzak=3.0, lens=55, fstop=5.6)
    kit.sinematik(bloom=0.5, esik=1.0, boyut=0.65)


# ------------------------------------------------------------------ 7–11: bina
def bina_hazir(aksam=False):
    P = B.uret()
    mats = B.malzemeler(aksam)
    olcekle(14, (0, 0, 4.5), guc=110 / 196)
    sc = bpy.context.scene
    sc.view_settings.exposure = -0.3
    return P, mats


def cizgi_kur(P, filtre=None, mat=None, kalin=0.022):
    mer, boy = B.kenarlar(P, kalin, filtre=lambda p: p['tur'] not in ('harc',) and (filtre is None or filtre(p)))
    return kit.toplu_mesh('Cizgiler', kit.sablon('kup'), mer, boy, None, mat or grafit_m())


def sahne_cizim(sc):
    P, mats = bina_hazir()
    cizgi_kur(P)
    bina_kamera()


def sahne_isikcizim(sc):
    P, mats = bina_hazir()
    Q.aksam_studyo(sc, koyu='#161c23', olcek=14, hedef=(0, 0, 4.5))
    cizgi_kur(P, mat=lime_m(2.2), kalin=0.02)
    bina_kamera()
    kit.sinematik(bloom=0.5, esik=0.9, boyut=0.6)


def sahne_kalem2(sc):
    P, mats = bina_hazir()
    T = 0.3
    B.kur(P, mats, lambda p: (p['c'], p['s'], (0, 0, 0)) if p['zaman'] < T else None)
    cizgi_kur(P, filtre=lambda p: p['zaman'] >= T)
    bina_kamera()


def sahne_tarama(sc):
    P, mats = bina_hazir()
    zc = 4.6

    def alt(p):
        return p['c'][2] < zc
    B.kur(P, mats, lambda p: (p['c'], p['s'], (0, 0, 0)) if alt(p) else None)
    cizgi_kur(P, filtre=lambda p: not alt(p))
    lm = lime_m(8.0)
    W, D = B.XS[-1] - B.XS[0] + 1.6, B.YS[-1] - B.YS[0] + 1.6
    for (c, s) in (((0, -D / 2, zc), (W, 0.06, 0.06)), ((0, D / 2, zc), (W, 0.06, 0.06)),
                   ((-W / 2, 0, zc), (0.06, D, 0.06)), ((W / 2, 0, zc), (0.06, D, 0.06))):
        kit.box('Tarama', s, c, lm)
    bina_kamera()
    kit.sinematik(bloom=0.4, esik=1.0, boyut=0.6)


def sahne_insa(sc):
    P, mats = bina_hazir()
    rnd = random.Random(12)
    T0, T1 = 0.6, 0.72

    def d(p):
        z = p['zaman']
        if z < T0:
            return p['c'], p['s'], (0, 0, 0)
        if z > T1:
            return None
        e = (z - T0) / (T1 - T0)
        c = Vector(p['c']) + Vector((rnd.uniform(-0.3, 0.3) * e, rnd.uniform(-0.3, 0.3) * e, 0.6 + 5.5 * e ** 1.4))
        return tuple(c), p['s'], (rnd.uniform(-0.5, 0.5) * e, rnd.uniform(-0.5, 0.5) * e, rnd.uniform(-0.8, 0.8) * e)
    B.kur(P, mats, d)
    bina_kamera(hedef=(0, 0, 5.6), uzak=52)


def sahne_patlatma(sc):
    """Patlatılmış aksonometri: katlar ayrılır, duvarlar dışa açılır, çatı panelleri yükselir."""
    P, mats = bina_hazir()
    duvar = ('blok', 'harc', 'lento', 'cam', 'dograma', 'denizlik', 'kapi')

    def d(p):
        c = Vector(p['c'])
        c.z += p['kat'] * 2.6
        if p['tur'] == 'temel':
            c.z -= 1.6
        if p['tur'] in duvar and p['kat'] < B.KAT:
            c += Vector(p['n']) * 1.8
        if p['tur'] == 'panel':
            c.z += 2.4
        return tuple(c), p['s'], (0, 0, 0)
    B.kur(P, mats, d)
    bina_kamera(hedef=(0, 0, 7.5), uzak=78, yon=(0.75, -1.0, 0.5))


def sahne_bitmis(sc):
    P, mats = bina_hazir()
    B.kur(P, mats)
    bina_kamera()


def sahne_dalga(sc):
    P, mats = bina_hazir()
    B.kur(P, mats)
    for i, r in enumerate((10.0, 13.5, 17.5, 22.0)):
        h = kit.halo_ring(f'Dalga{i}', radius=r, width=0.09 + 0.04 * i, strength=6.0 * (1 - i * 0.2), segments=256, z=-0.42)
    bina_kamera(uzak=62, yon=(0.75, -1.0, 0.6), hedef=(0, 0, 3.0))
    kit.sinematik(bloom=0.35, esik=1.2, boyut=0.6)


def sahne_yukyolu(sc):
    """Yük yolu: döşemeden kirişe, kolondan temele lime çizgiler; altta aşağı oklar."""
    P, mats = bina_hazir()
    B.kur(P, mats)
    lm = lime_m(6.0)
    for x in B.XS:
        for y in (B.YS[0],):
            kit.box('Yuk', (0.12, 0.04, B.KAT * B.FH + 0.4), (x, y - B.COL / 2 - 0.03, (B.KAT * B.FH) / 2 - 0.2), lm)
    for k in range(B.KAT):
        kit.box('Yuk', (B.XS[-1] - B.XS[0], 0.04, 0.08), (0, B.YS[0] - B.KIRIS_W / 2 - 0.03, (k + 1) * B.FH - 0.3), lm)
    for x in B.XS:
        bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.35, radius2=0.0, depth=0.6, location=(x, B.YS[0] - 0.4, -0.95),
                                        rotation=(math.pi, 0, 0))
        bpy.context.active_object.data.materials.append(lm)
    bina_kamera()
    kit.sinematik(bloom=0.35, esik=1.1, boyut=0.6)


def siluet(m, x, y, z, boy=1.75, n=(0, -1, 0)):
    k = boy / 1.75
    for (dz, w, h) in ((0.95, 0.42, 0.62), (0.4, 0.34, 0.8), (1.42, 0.22, 0.24)):
        kit.box('Siluet', (w * k, 0.05, h * k), (x, y, z + dz * k), m)


def sahne_aksam2(sc):
    P, mats = bina_hazir(aksam=True)
    rnd = random.Random(5)
    mats['camkoyu'] = Q.pbr('CamKoyu', '#141b21', 0.02)
    aile = None
    for p in P:
        if p['tur'] == 'cam' and p['kat'] == 1 and p['n'] == (0, -1, 0) and abs(p['c'][0]) < 0.5:
            aile = p  # aile penceresi: cam yok, silüetler arkadan aydınlanır
        elif p['tur'] == 'cam' and rnd.random() < 0.25:
            p['tur'] = 'camkoyu'
    B.kur(P, mats, lambda p: None if p is aile else (p['c'], p['s'], (0, 0, 0)))
    Q.aksam_studyo(sc, olcek=14, hedef=(0, 0, 4.5))
    kit.halo_ring('Halka', radius=10.5, width=0.16, strength=9.0, segments=256, z=-0.42)
    sm = Q.pbr('Siluet', '#111111', 0.9)
    for x, boy in ((-0.35, 1.78), (0.15, 1.62), (0.5, 1.1)):  # aile: 1. kat ön, orta bölme
        siluet(sm, x, B.YS[0] + 0.35, B.FH, boy)
    ld = bpy.data.lights.new('AileArka', 'AREA')
    ld.energy = 900
    ld.size = 2.0
    ld.color = (1.0, 0.7, 0.42)
    lo = bpy.data.objects.new('AileArka', ld)
    lo.location = (0, B.YS[0] + 3.0, B.FH + 1.3)
    kit.link(lo)
    kit.aim(lo, (0, B.YS[0], B.FH + 1.2))
    for p in P:
        if p['tur'] == 'cam':
            ld = bpy.data.lights.new('Ic', 'POINT')
            ld.energy = 60
            ld.color = (1.0, 0.68, 0.4)
            ld.shadow_soft_size = 0.4
            lo = bpy.data.objects.new('Ic', ld)
            lo.location = Vector(p['c']) - Vector(p['n']) * 1.2
            kit.link(lo)
    bina_kamera()
    kit.sinematik(bloom=0.45, esik=1.0, boyut=0.65)


def sahne_kesit(sc):
    """Ön cephe kaldırılmış 'bebek evi' kesiti: sıcak odalar, mobilya, aile."""
    P, mats = bina_hazir(aksam=True)
    duvar = ('blok', 'harc', 'lento', 'cam', 'dograma', 'denizlik', 'kapi')
    B.kur(P, mats, lambda p: None if (p['tur'] in duvar and p['n'] == (0, -1, 0) and p['kat'] < B.KAT) else (p['c'], p['s'], (0, 0, 0)))
    Q.aksam_studyo(sc, olcek=14, hedef=(0, 0, 4.5))
    rnd = random.Random(3)
    parke = Q.pbr('Parke', '#b48a62', 0.5)
    siva = Q.pbr('Siva', '#efe8de', 0.9)
    mob = [Q.pbr('Mob1', '#7d6a5a', 0.7), Q.pbr('Mob2', '#c9b9a3', 0.8), Q.pbr('Mob3', '#4f5d6b', 0.7)]
    sm = Q.pbr('Siluet', '#111111', 0.9)
    for k in range(B.KAT):
        z = k * B.FH
        for xa, xb in zip(B.XS[:-1], B.XS[1:]):
            xm = (xa + xb) / 2
            kit.box('Parke', (xb - xa - B.COL, B.YS[-1] - B.YS[0] - 0.4, 0.04), (xm, 0, z + 0.02), parke)
            if xa > B.XS[0]:
                kit.box('Bolme', (0.12, B.YS[-1] - B.YS[0] - 0.4, 2.5), (xa + B.COL / 2 + 0.06, 0, z + 1.25), siva)
            kit.box('Mobilya', (1.8, 0.8, 0.75), (xm - 0.4, 2.8, z + 0.4), mob[rnd.randrange(3)])
            kit.box('Masa', (1.0, 0.7, 0.05), (xm + 0.6, 0.2, z + 0.75), mob[1])
            ld = bpy.data.lights.new('Oda', 'POINT')
            ld.energy = 220
            ld.color = (1.0, 0.7, 0.42)
            ld.shadow_soft_size = 0.3
            lo = bpy.data.objects.new('Oda', ld)
            lo.location = (xm, 0.5, z + 2.3)
            kit.link(lo)
    for x, boy in ((-0.5, 1.78), (0.0, 1.62), (0.45, 1.1)):
        siluet(sm, x, -1.0, B.FH + 0.04, boy)
    bina_kamera(yon=(0.35, -1.0, 0.3), uzak=46)
    kit.sinematik(bloom=0.4, esik=1.1, boyut=0.6)


# ------------------------------------------------------------------ 12
def sahne_blokkure(sc):
    """Kıtalar küçük gazbeton bloklardan; Türkiye lime blok; açık stüdyo."""
    import s4_dunya as G
    pts = json.load(open(os.path.join(kit.TEX_DIR, 'kara_noktalari.json')))
    rot = G.globe_rotation()
    aac = kit.aac_material('Gazbeton', bump=0.3, tex_size=0.05)
    lime = Q.pbr('BlokTR', LIME, 0.5, 0.0, LIME, 2.5)
    for grup, m in ((False, aac), (True, lime)):
        mer, don = [], []
        for la, lo, k in pts:
            if (k == 5) != grup:
                continue
            v = rot @ G.ll2v(la, lo, 1.006)
            mer.append(tuple(v))
            don.append(tuple(v.normalized().to_track_quat('Z', 'Y').to_euler()))
        kit.toplu_mesh('Kara' + ('TR' if grup else ''), kit.sablon('kup'), mer, [(0.012, 0.0085, 0.012)] * len(mer), don, m)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=1.0)
    o = bpy.context.active_object
    o.data.materials.append(Q.pbr('Okyanus', '#cfd6db', 0.45))
    bpy.ops.object.shade_smooth()
    yay = lime_m(5.0)
    for i, (_, la, lo, _) in enumerate(G.TARGETS):
        a = G.arc_object(f'Yay{i}', G.IZMIR, (la, lo), rot, yay)
        a.data.bevel_factor_end = 1.0
    R.kamera(hedef=(0, 0, 0), yon=(0.0, -1.0, 0.25), uzak=4.4, lens=55, fstop=11.0)
    kit.sinematik(bloom=0.3, esik=1.2, boyut=0.6)


SAHNELER = {k[6:]: v for k, v in globals().items() if k.startswith('sahne_')}


def main():
    kit.reset()
    sc = kit.setup_render(1280, 720, samples=ARGS.samples, threshold=0.015, bounces=(6, 3, 3, 2))
    R.studyo(sc)
    SAHNELER[ARGS.sahne](sc)
    os.makedirs(ARGS.out, exist_ok=True)
    kit.render_to(os.path.join(ARGS.out, f'{ARGS.sahne}.png'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--sahne', default='bitmis')
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=48)
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
