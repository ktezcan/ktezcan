"""
Stil R — ayrıntılı araç ve fabrika + özellik canlandırmaları (ısı kalkanı dilinde).

  tir      : çekici + dorse, lime streçli paletler, kayışlar (yeşil = bizim)
  fabrika2 : üretim holü (testere dişi çatı), otoklavlar + raylar, silolar + konveyör,
             kireç tesisi kulesi, stok sahası (lime streçli paletler), sahada tırlar
  alev     : A1 — alevler duvarın bir yüzünü yalar; diğer yüz serin kalır
  yuzer    : hafiflik — blok cam tanktaki suda yüzer (yoğunluk < su)
  derz     : ince derz — lime lazer çizgisi boyunca kusursuz sıra, 1–3 mm yapıştırıcı
  testere  : kolay işlenir — el testeresi, tesisat kanalı, delikler, talaş

Kullanım: python stil_r5.py --sahne <ad> --out DIR [--samples N]
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
import stil_r2 as Q  # noqa: E402
import stil_r3 as T  # noqa: E402
import stil_r4 as F  # noqa: E402

LIME = '#b8d84a'
P = Q.pbr


def silindir(r, d, loc, rot=(0, 0, 0), m=None, v=32, smooth=True):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=loc, rotation=rot)
    o = bpy.context.active_object
    if m:
        o.data.materials.append(m)
    if smooth:
        bpy.ops.object.shade_smooth()
    return o


def kutu(name, s, c, m, bev=0.0, rz=0.0):
    o = kit.box(name, s, c, m)
    if bev:
        kit.bevel(o, bev, 3, 50)
    o.rotation_euler[2] = rz
    return o


def strec_m():
    m = bpy.data.materials.new('Strec')
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = kit.srgb(LIME)
    b.inputs['Roughness'].default_value = 0.22
    b.inputs['Transmission Weight'].default_value = 0.5
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nz = nt.nodes.new('ShaderNodeTexNoise')  # streç kırışıkları: yatay uzamış gürültü
    nz.inputs['Scale'].default_value = 6.0
    nz.inputs['Detail'].default_value = 6.0
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1.0, 1.0, 9.0)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    bp = nt.nodes.new('ShaderNodeBump')
    bp.inputs['Strength'].default_value = 0.25
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m


def tekerlek(x, y, z, M, r=0.52, w=0.32):
    s = 1 if y > 0 else -1
    silindir(r, w, (x, y, z), (math.pi / 2, 0, 0), M['lastik'], 40)
    silindir(r * 0.62, 0.02, (x, y + s * w / 2, z), (math.pi / 2, 0, 0), M['jant'], 40)
    silindir(r * 0.22, 0.05, (x, y + s * (w / 2 + 0.02), z), (math.pi / 2, 0, 0), M['krom'], 24)
    silindir(r * 0.5, 0.025, (x, y + s * (w / 2 + 0.008), z), (math.pi / 2, 0, 0), M['sasi'], 32, smooth=False)
    for k in range(10):  # bijon somunları
        a = k * 2 * math.pi / 10
        silindir(0.022, 0.05, (x + 0.17 * r * 2 * math.cos(a) / 2, y + s * (w / 2 + 0.035), z + 0.17 * r * 2 * math.sin(a) / 2),
                 (math.pi / 2, 0, 0), M['krom'], 6, smooth=False)


def tir_ayrinti(M):
    """Kabin ve dorse ayrıntıları: cam çerçevesi, güneşlik, tepe lambaları, silecek, tutamak, egzoz,
    kapı derzi, çamur paçalığı, bijon somunları, yan koruma, yan ve arka lambalar."""
    amber = P('Amber', '#d98a1c', 0.2, 0.0, '#ffa030', 1.5)
    kirmizi = P('TirStop', '#7a0d0d', 0.2, 0.0, '#ff2a1a', 1.0)
    beyaz = P('TirPlaka', '#f2f2f0', 0.4)
    kutu('CamCerceve', (0.05, 2.24, 1.14), (5.6, 0, 2.95), M['koyu'], 0.03)
    kutu('OnCam', (0.06, 2.1, 1.0), (5.625, 0, 2.95), M['cam'])
    kutu('Gunesluk', (0.4, 2.3, 0.08), (5.78, 0, 3.5), M['koyu'], 0.02)
    for k in range(5):
        kutu('TepeLamba', (0.08, 0.14, 0.06), (5.82, -0.6 + k * 0.3, 3.56), amber)
    for y in (-0.5, 0.45):
        kutu('Silecek', (0.03, 0.9, 0.03), (5.67, y, 2.5), M['koyu']).rotation_euler[0] = 0.35
    for y in (-1, 1):
        s = y * 1.255
        kutu('KapiDerz', (0.02, 0.02, 1.9), (5.45, s, 2.3), M['koyu'])
        kutu('KapiDerz', (0.02, 0.02, 1.9), (4.0, s, 2.3), M['koyu'])
        kutu('KapiKolu', (0.18, 0.04, 0.05), (4.2, y * 1.27, 2.3), M['krom'])
        silindir(0.025, 1.2, (3.95, y * 1.29, 2.0), (0, 0, 0), M['krom'], 12)  # tutamak
        kutu('YanEtek', (1.2, 0.06, 0.55), (4.55, y * 1.24, 1.05), M['boya'], 0.02)
        kutu('KoseLamba', (0.12, 0.06, 0.22), (5.55, y * 1.24, 1.5), amber)
        kutu('Pacalik', (0.04, 0.5, 0.55), (3.7, y * 1.05, 0.55), M['koyu'])
        kutu('Pacalik', (0.04, 0.5, 0.55), (0.55, y * 1.05, 0.55), M['koyu'])
        kutu('Pacalik', (0.04, 0.5, 0.55), (-11.3, y * 1.05, 0.55), M['koyu'])
        # egzoz bacası ve hava tankı
        silindir(0.09, 2.4, (3.28, y * 1.15, 3.0), (0, 0, 0), M['krom'], 20)
        silindir(0.18, 0.9, (2.2, y * 0.95, 0.85), (0, math.pi / 2, 0), M['sasi'], 20)
        # dorse yan koruma rayı ve yan işaret lambaları
        for z in (0.95, 0.65):
            kutu('YanKoruma', (6.6, 0.04, 0.08), (-4.4, y * 1.2, z), M['krom'])
        for k in range(7):
            kutu('YanLamba', (0.1, 0.03, 0.06), (1.2 - k * 1.95, y * 1.265, 1.35), amber)
        kutu('ArkaStop', (0.05, 0.4, 0.14), (-10.92, y * 0.95, 1.05), kirmizi)
        kutu('ArkaSinyal', (0.05, 0.16, 0.14), (-10.92, y * 0.65, 1.05), amber)
    kutu('ArkaKoruma', (0.12, 2.3, 0.14), (-10.95, 0, 0.6), M['koyu'])
    kutu('Plaka', (0.02, 0.52, 0.12), (5.77, 0, 1.0), beyaz)
    kutu('Plaka', (0.02, 0.52, 0.12), (-10.99, 0, 0.82), beyaz)
    for y in (-0.95, 0.95):
        kutu('FarCerceve', (0.04, 0.55, 0.26), (5.62, y, 1.35), M['krom'], 0.02)
        kutu('GunduzLed', (0.05, 0.42, 0.03), (5.655, y, 1.48), M['far'])


def tir(ox=0.0, oy=0.0, rz=0.0, palet=True, M=None, aac=None):
    """Çekici +x yönüne bakar. Tüm parçalar (ox, oy) etrafında rz kadar döner."""
    M = M or dict(boya=P('TirBoya', '#f2f2ef', 0.3), lime=P('TirLime', LIME, 0.4), koyu=P('TirKoyu', '#2b2f33', 0.5),
                  lastik=P('Lastik', '#18191b', 0.85), jant=P('Jant', '#c9ccd0', 0.25, 1.0), krom=P('Krom', '#e4e6e8', 0.12, 1.0),
                  cam=P('TirCam', '#151c22', 0.03), far=P('Far', '#fff7e6', 0.2, 0.0, '#fff7e6', 3.0),
                  ahsap=P('Ahsap', '#b68a5c', 0.8), kayis=P('Kayis', '#e0a12a', 0.6), sasi=P('Sasi', '#3a3e42', 0.6))
    aac = aac or kit.aac_material('Gazbeton', bump=0.4, tex_size=0.24)
    once = set(bpy.data.objects)
    # çekici kabini
    kutu('Kabin', (2.2, 2.5, 2.5), (4.5, 0, 2.35), M['boya'], 0.16)
    kutu('Spoiler', (1.2, 2.3, 0.6), (4.1, 0, 3.85), M['boya'], 0.2)
    kutu('OnCam', (0.06, 2.1, 1.0), (5.62, 0, 2.95), M['cam'])
    for y in (-1.26, 1.26):
        kutu('YanCam', (0.9, 0.04, 0.8), (5.0, y, 2.95), M['cam'])
        kutu('LimeSerit', (2.0, 0.03, 0.18), (4.5, y * 1.002, 1.75), M['lime'])  # bizim: lime şerit
        kutu('AynaKol', (0.5, 0.05, 0.05), (5.75, y * 1.08, 2.9), M['koyu'])
        kutu('Ayna', (0.08, 0.22, 0.5), (5.95, y * 1.2, 2.8), M['koyu'], 0.02)
        kutu('Basamak', (0.6, 0.25, 0.08), (4.9, y * 1.08, 0.95), M['koyu'])
        silindir(0.32, 1.2, (3.2, y * 1.0, 1.1), (0, math.pi / 2, 0), M['krom'], 32)  # yakıt tankı
    kutu('Izgara', (0.06, 1.7, 0.8), (5.62, 0, 1.75), M['koyu'])
    for k in range(5):
        kutu('Lamel', (0.07, 1.68, 0.04), (5.64, 0, 1.45 + k * 0.15), M['krom'])
    for y in (-0.95, 0.95):
        kutu('Far', (0.05, 0.45, 0.18), (5.64, y, 1.35), M['far'])
    kutu('Tampon', (0.3, 2.5, 0.35), (5.6, 0, 0.95), M['koyu'], 0.05)
    kutu('CekiciSasi', (5.0, 1.0, 0.35), (3.0, 0, 0.85), M['sasi'])
    kutu('Besinci', (1.2, 1.4, 0.15), (1.8, 0, 1.15), M['koyu'])
    for x in (4.6, 2.3, 1.2):
        for y in (-1.05, 1.05):
            tekerlek(x, y, 0.52, M)
    for x in (4.6,):
        for y in (-1.2, 1.2):
            kutu('Camurluk', (1.3, 0.35, 0.1), (x, y, 1.12), M['koyu'], 0.04)
    # dorse
    kutu('Dorse', (12.6, 2.5, 0.22), (-4.6, 0, 1.45), M['boya'], 0.03)
    for y in (-1.22, 1.22):
        kutu('DorseKenar', (12.6, 0.08, 0.32), (-4.6, y, 1.3), M['koyu'])
    kutu('DorseSasi', (12.0, 1.0, 0.35), (-4.6, 0, 1.12), M['sasi'])
    for x in (-8.0, -9.3, -10.6):
        for y in (-1.05, 1.05):
            tekerlek(x + 0.6, y, 0.52, M)
    for y in (-1.25, 1.25):
        kutu('Camurluk', (4.2, 0.35, 0.08), (-9.0, y, 1.15), M['koyu'])
        kutu('Ayak', (0.12, 0.12, 0.9), (0.4, y * 0.6, 0.7), M['sasi'])
    tir_ayrinti(M)
    # yük: 2 sıra × 8 palet, 5 sıra blok, streç + kayış
    if palet:
        mer, boy = [], []
        st = strec_m()
        for i in range(8):
            for j in (-0.62, 0.62):
                x = -10.2 + i * 1.32
                kutu('PaletTaban', (1.2, 1.0, 0.14), (x, j, 1.63), M['ahsap'])
                for s in range(5):
                    for a in range(2):
                        for c in range(4):
                            mer.append((x - 0.3 + a * 0.6, j - 0.375 + c * 0.25, 1.70 + (s + 0.5) * 0.25))
                            boy.append((0.595, 0.245, 0.245))
                kutu('Strec', (1.23, 1.03, 1.2), (x, j, 1.70 + 0.62), st, 0.05)
            kutu('Kayis', (0.06, 2.56, 0.04), (-10.2 + i * 1.32, 0, 2.95), M['kayis'])
            for y in (-1.29, 1.29):
                kutu('Kayis', (0.06, 0.03, 1.5), (-10.2 + i * 1.32, y, 2.2), M['kayis'])
        kit.toplu_mesh('Yuk', kit.sablon('kup'), mer, boy, None, aac)
    # hepsini döndür / taşı
    yeni = [o for o in bpy.data.objects if o not in once and o.type == 'MESH']
    if rz or ox or oy:
        c, s_ = math.cos(rz), math.sin(rz)
        for o in yeni:
            p = o.location
            o.location = (ox + p.x * c - p.y * s_, oy + p.x * s_ + p.y * c, p.z)
            o.rotation_euler[2] += rz
    return yeni


def sahne_tir(sc):
    tir()
    F.zemin(0.0)
    T.olcekle(10, (-2, 0, 1.8), guc=0.6)
    R.kamera(hedef=(-0.6, 0, 1.7), yon=(0.95, -1.0, 0.3), uzak=33, lens=55, fstop=9.0, kayma=-0.12)


def sahne_fabrika2(sc):
    rnd = random.Random(3)
    beyaz = P('Hol', '#efede9', 0.6)
    gri = P('Celik', '#b8bcc0', 0.35, 0.7)
    koyu = P('Koyu', '#3a3f44', 0.5)
    cam = P('FabCam', '#1b242b', 0.05)
    lime = P('Lime', LIME, 0.5)
    beton = P('Saha', '#d8d4cd', 0.85)
    asfalt = P('Yol', '#a9a8a5', 0.9)
    F.zemin(0.0)
    kutu('Saha', (170, 110, 0.1), (0, 0, 0.05), beton)
    kutu('Yol', (170, 9, 0.12), (0, -46, 0.06), asfalt)
    # üretim holü: duvarlar + testere dişi çatı
    HX, HY, HZ = 64.0, 30.0, 12.0
    kutu('Hol', (HX, HY, HZ), (0, 6, HZ / 2), beyaz)
    kutu('HolBant', (HX + 0.06, HY + 0.06, 0.8), (0, 6, HZ - 2.0), lime)  # bizim: lime şerit
    kutu('HolPencere', (HX + 0.04, HY + 0.04, 1.6), (0, 6, 6.0), cam)
    for i in range(0, 6, 2):  # yükleme kapıları (doğu cephe)
        kutu('Kapi', (0.2, 5.0, 6.0), (HX / 2 + 0.05, -6 + i * 4.8, 3.0), koyu)
    n = 8
    w = HX / n
    for i in range(n):
        x0 = -HX / 2 + i * w
        v = [(x0, -HY / 2 + 6, HZ), (x0 + w, -HY / 2 + 6, HZ), (x0 + w, HY / 2 + 6, HZ), (x0, HY / 2 + 6, HZ),
             (x0 + w, -HY / 2 + 6, HZ + 4.0), (x0 + w, HY / 2 + 6, HZ + 4.0)]
        f = [(0, 1, 4), (3, 5, 2), (0, 4, 5, 3), (1, 2, 5, 4), (0, 3, 2, 1)]
        kit.mesh_object('Dis', v, f, beyaz)
        kutu('DisCam', (0.12, HY - 0.6, 3.4), (x0 + w - 0.08, 6, HZ + 2.0), cam)
    # otoklavlar: hol önünde, raylı
    for i in range(5):
        y = -24.0
        x = -26 + i * 6.2
        silindir(1.5, 32, (x, y - 16, 1.9), (math.pi / 2, 0, 0), gri, 48)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.5, location=(x, y - 32, 1.9))
        o = bpy.context.active_object
        o.scale = (1, 0.4, 1)
        o.data.materials.append(gri)
        bpy.ops.object.shade_smooth()
        bpy.ops.mesh.primitive_torus_add(major_radius=1.55, minor_radius=0.18, location=(x, y, 1.9), rotation=(math.pi / 2, 0, 0))
        bpy.context.active_object.data.materials.append(koyu)
        for k in range(5):
            kutu('Ayak', (2.2, 0.5, 0.6), (x, y - 3 - k * 7, 0.4), koyu)
        for dx in (-0.6, 0.6):
            kutu('Ray', (0.12, 22, 0.12), (x + dx, y + 11 - 0.5, 0.18), gri)
    # silolar + konveyör köprüsü
    for i in range(4):
        sx, sy = 46.0, -6 + i * 7.0
        silindir(2.6, 18, (sx, sy, 14), m=beyaz, v=48)
        bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=2.6, radius2=0.4, depth=2.2, location=(sx, sy, 24.1))
        bpy.context.active_object.data.materials.append(gri)
        bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=0.5, radius2=2.6, depth=3.0, location=(sx, sy, 3.5))
        bpy.context.active_object.data.materials.append(gri)
        for dx, dy in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
            kutu('SiloAyak', (0.35, 0.35, 5.0), (sx + dx, sy + dy, 2.5), koyu)
    kon = kutu('Konveyor', (20, 2.0, 1.6), (35.5, 4.5, 19.0), gri)
    kon.rotation_euler[1] = math.radians(14)
    # kireç tesisi: kule + baca (bacada lime bant)
    kutu('Kule', (8, 8, 26), (-56, 22, 13), beyaz)
    silindir(1.1, 40, (-50, 28, 20), m=beyaz, v=40)
    silindir(1.13, 2.0, (-50, 28, 36.5), m=lime, v=40)
    # stok sahası: lime streçli paletler
    st = strec_m()
    aac = kit.aac_material('Gazbeton', bump=0.3, tex_size=0.24)
    for i in range(10):
        for j in range(4):
            x, y = 40 + i * 1.6, -30 + j * 1.5
            if x > 80:
                continue
            kutu('Strec', (1.25, 1.05, 1.3), (x - 30, y, 0.75), st, 0.05)
    # sahada tırlar
    tir(ox=-46, oy=-46, rz=0.0, M=None, aac=aac)
    tir(ox=60, oy=-34, rz=math.pi, aac=aac)
    T.olcekle(60, (0, 0, 8), guc=0.6)
    R.kamera(hedef=(6, -8, 8), yon=(0.75, -1.0, 0.62), uzak=300, lens=55, fstop=16.0, kayma=-0.1)


def duvar_parcasi(aac, harc, L=1.2, sira=4, x=0.0, eksen='y'):
    mer, boy = [], []
    for s in range(sira):
        kay = 0.0 if s % 2 == 0 else 0.3
        for i in range(-1, int(L / 0.6) + 1):
            a0 = -L / 2 + i * 0.6 - kay
            a0, a1 = max(a0, -L / 2), min(a0 + 0.6, L / 2)
            if a1 - a0 < 0.02:
                continue
            mer.append((x, (a0 + a1) / 2, -0.5 + (s + 0.5) * 0.25))
            boy.append((0.2, a1 - a0 - 0.006, 0.244))
    kit.toplu_mesh('Duvar', kit.sablon('kup'), mer, boy, None, aac)
    kit.box('Harc', (0.12, L, sira * 0.25), (x, 0, -0.5 + sira * 0.125), harc)


def sahne_alev(sc):
    """A1 yangına tepki sınıfı: soldaki yüzü alevler yalar, sağ yüz serin; kor zerreleri."""
    rnd = random.Random(5)
    aac = kit.aac_material('Gazbeton', bump=0.6)
    duvar_parcasi(aac, P('Harc', '#77736d', 0.95))
    Q.aksam_studyo(sc, koyu='#1a1f26')
    renkler = [('#fff3c4', 9.0), ('#ffc25a', 7.0), ('#ff8a2a', 5.0), ('#e2541c', 3.0)]
    mats = [P(f'Alev{i}', c, 0.5, 0.0, c, g) for i, (c, g) in enumerate(renkler)]
    diller = [(rnd.uniform(-0.5, 0.5), rnd.uniform(0.35, 0.8)) for _ in range(16)]  # (y, boy)
    for i, m in enumerate(mats):
        mer, boy, don = [], [], []
        for (yd, H) in diller:
            for _ in range(70):
                h = rnd.random() ** (0.8 + 0.35 * i)  # dış renkler daha yukarı uzanır
                genis = 0.07 * (1 - h) ** 0.8 + 0.01
                z = -0.5 + h * H * (0.7 + 0.12 * i)
                y = yd + rnd.gauss(0, genis) + 0.03 * math.sin(z * 14 + yd * 5)
                x = -0.13 - rnd.random() * (0.05 + 0.06 * i) * (1 - h * 0.5)
                mer.append((x, y, z))
                r = 0.012 * (1 - h * 0.6) * (1 + 0.3 * i)
                boy.append((r, r, r * 4.0))
                don.append((0, rnd.uniform(-0.15, 0.15), 0))
        kit.toplu_mesh(f'Alev{i}', kit.sablon('ico', 1), mer, boy, don, m, yumusak=True)
    pts = [(rnd.uniform(-0.6, -0.15), rnd.uniform(-0.6, 0.6), rnd.uniform(-0.2, 0.7)) for _ in range(160)]
    kit.toplu_mesh('Kor', kit.sablon('ico', 1), pts, [0.004] * len(pts), None, R.isiltili('Kor', (1.0, 0.5, 0.15), 8.0), yumusak=True)
    ld = bpy.data.lights.new('AlevIsik', 'AREA')
    ld.energy = 120
    ld.size = 1.0
    ld.color = (1.0, 0.5, 0.2)
    lo = bpy.data.objects.new('AlevIsik', ld)
    lo.location = (-0.6, 0, -0.1)
    kit.link(lo)
    kit.aim(lo, (0, 0, -0.1))
    R.kamera(hedef=(0.0, 0, -0.1), yon=(-0.3, -1.0, 0.22), uzak=4.4, lens=55, fstop=5.6)
    kit.sinematik(bloom=0.55, esik=0.9, boyut=0.6)


def sahne_yuzer(sc):
    """Hafiflik: blok cam tankta yüzer (yoğunluk sudan az); su yüzeyinde halkalar."""
    sc.cycles.transmission_bounces = 10
    sc.cycles.max_bounces = 12
    cam = bpy.data.materials.new('TankCam')
    cam.use_nodes = True
    b = cam.node_tree.nodes['Principled BSDF']
    b.inputs['Transmission Weight'].default_value = 1.0
    b.inputs['Roughness'].default_value = 0.02
    b.inputs['IOR'].default_value = 1.45
    su = bpy.data.materials.new('Su')
    su.use_nodes = True
    nt = su.node_tree
    b2 = nt.nodes['Principled BSDF']
    b2.inputs['Base Color'].default_value = kit.srgb('#cfe6ee')
    b2.inputs['Transmission Weight'].default_value = 1.0
    b2.inputs['Roughness'].default_value = 0.03
    b2.inputs['IOR'].default_value = 1.33
    tc = nt.nodes.new('ShaderNodeTexCoord')
    wv = nt.nodes.new('ShaderNodeTexWave')
    wv.wave_type = 'RINGS'
    wv.inputs['Scale'].default_value = 6.0
    wv.inputs['Distortion'].default_value = 0.4
    nt.links.new(tc.outputs['Object'], wv.inputs['Vector'])
    bp = nt.nodes.new('ShaderNodeBump')
    bp.inputs['Strength'].default_value = 0.08
    nt.links.new(wv.outputs['Fac'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], b2.inputs['Normal'])
    TX, TY, TZ, e = 1.3, 0.75, 0.7, 0.012
    z0 = -0.5
    kit.box('TankTaban', (TX, TY, e), (0, 0, z0 + e / 2), cam)
    for sx in (-1, 1):
        kit.box('TankYan', (e, TY, TZ), (sx * TX / 2, 0, z0 + TZ / 2), cam)
        kit.box('TankYan', (TX, e, TZ), (0, sx * TY / 2, z0 + TZ / 2), cam)
    zs = z0 + 0.48
    kit.box('Su', (TX - 2 * e, TY - 2 * e, 0.48 - e), (0, 0, z0 + e + (0.48 - e) / 2), su)
    aac = kit.aac_material('Gazbeton', bump=0.6)
    blk = kit.gecmeli_blok('Blok', 0.6, 0.25, 0.25, aac)
    blk.location = (0.02, 0, zs - 0.25 * 0.38)  # ~%38 batık (yoğunluk ~380 kg/m³)
    blk.rotation_euler = (math.radians(2), math.radians(-1.5), math.radians(12))
    F.zemin(z0)
    fon = kit.box('Fon', (12, 0.05, 8), (-2.5, 3.0, 2.0), P('FonM', '#efe9e4', 1.0, 0.0, '#efe9e4', 1.0))
    fon.rotation_euler[2] = math.radians(-37)
    fon.visible_camera = False  # yalnız cam/su içinden görünür
    R.kamera(hedef=(0, 0, -0.2), yon=(0.75, -1.0, 0.32), uzak=3.8, lens=55, fstop=6.0)


def sahne_derz(sc):
    """İnce derz: köşe duvarı, 1–3 mm yapıştırıcı; lime lazer çizgisi sıra üstünü kusursuz izler."""
    aac = kit.aac_material('Gazbeton', bump=0.6)
    yap = P('Yapistirici', '#9b9891', 0.9)
    mer, boy = [], []
    d = 0.003  # 3 mm derz
    for s in range(3):
        kay = 0.3 if s % 2 else 0.0
        for i in range(5):
            a0, a1 = max(-1.2, -1.2 + i * 0.6 - kay), min(1.2, -1.2 + (i + 1) * 0.6 - kay)
            if a1 - a0 < 0.05:
                continue
            mer.append(((a0 + a1) / 2, 0.0, -0.5 + s * (0.25 + d) + 0.125))
            boy.append((a1 - a0 - d, 0.2, 0.25))
    kit.toplu_mesh('Sira', kit.sablon('kup'), mer, boy, None, aac)
    for s in range(3):
        kit.box('Derz', (2.4, 0.19, d), (0.0, 0, -0.5 + s * (0.25 + d) + 0.25 + d / 2), yap)
    # 4. sıra: yerine iniyor
    b = kit.box('YeniBlok', (0.6 - d, 0.2, 0.25), (-0.6, 0, -0.5 + 3 * (0.25 + d) + 0.125 + 0.12), aac)
    b.rotation_euler[2] = math.radians(3)
    lm = P('Lazer', LIME, 0.3, 0.0, LIME, 12.0)
    zl = -0.5 + 3 * (0.25 + d) + 0.004
    kit.box('LazerCizgi', (3.2, 0.006, 0.006), (0.2, -0.101, zl), lm)
    kit.box('LazerCizgi', (0.006, 0.6, 0.006), (1.8, -0.4, zl), lm)
    kit.box('LazerCihaz', (0.12, 0.12, 0.16), (1.8, -0.7, zl), P('Cihaz', '#30353a', 0.4))
    for k, ang in enumerate((0, 2.1, 4.2)):
        a = kit.box('Ayak', (0.02, 0.02, 0.9), (1.8 + 0.12 * math.cos(ang), -0.7 + 0.12 * math.sin(ang), zl - 0.5), P('CihazAyak', '#30353a', 0.4))
    F.zemin(-0.95)
    R.kamera(hedef=(0.35, -0.2, -0.1), yon=(0.55, -1.0, 0.32), uzak=4.6, lens=55, fstop=5.6)
    kit.sinematik(bloom=0.35, esik=1.0, boyut=0.55)


def sahne_testere(sc):
    """Kolay işlenir: testere bloğu keser (talaş), yüzde tesisat kanalı ve delikler."""
    rnd = random.Random(2)
    aac = kit.aac_material('Gazbeton', bump=0.8)
    koyu = P('Oyuk', '#7d7a74', 0.95)
    celik = P('Bicak', '#cfd3d6', 0.2, 1.0)
    sap = P('Sap', '#2b2f33', 0.5)
    kit.box('BlokA', (0.42, 0.25, 0.25), (-0.09, 0, 0), aac)
    kit.box('BlokB', (0.176, 0.25, 0.25), (0.212, 0, 0), aac)
    kit.box('Yarik', (0.004, 0.252, 0.13), (0.122, 0, 0.06), koyu)  # yarım kalmış kesik
    kit.box('Kanal', (0.42, 0.006, 0.03), (-0.09, -0.126, 0.06), koyu)  # ön yüzde tesisat kanalı
    for x in (-0.22, -0.12):
        silindir(0.018, 0.004, (x, -0.1265, -0.05), (math.pi / 2, 0, 0), koyu, 24)
    b = kit.box('Bicak', (0.5, 0.0015, 0.09), (0.3, 0.0, 0.2), celik)
    b.rotation_euler[1] = math.radians(-32)
    s_ = kit.box('Sap', (0.13, 0.035, 0.1), (0.53, 0.0, 0.35), P('SapAhsap', '#8a5a35', 0.6))
    s_.rotation_euler[1] = math.radians(-32)
    kit.bevel(s_, 0.012, 3)
    pts, boy, don = [], [], []
    for _ in range(1400):
        t = rnd.random()
        pts.append((0.13 + rnd.gauss(0, 0.03), rnd.gauss(0, 0.12) * (0.3 + t), -0.13 - t * 0.25 + rnd.gauss(0, 0.02)))
        r = 0.003 * rnd.uniform(0.5, 1.5)
        boy.append(r)
        don.append((rnd.uniform(0, 6), rnd.uniform(0, 6), rnd.uniform(0, 6)))
    for _ in range(1800):
        rr = 0.14 * math.sqrt(rnd.random())
        th = rnd.uniform(0, 6.28)
        pts.append((0.15 + rr * math.cos(th), rr * math.sin(th) * 0.8, -0.4 + 0.04 * (1 - rr / 0.14) * rnd.random()))
        boy.append(0.003 * rnd.uniform(0.5, 1.5))
        don.append((rnd.uniform(0, 6), rnd.uniform(0, 6), rnd.uniform(0, 6)))
    kit.toplu_mesh('Talas', kit.sablon('kup'), pts, boy, don, P('TalasM', '#ecebe7', 0.9))
    F.zemin(-0.41)
    R.kamera(hedef=(0.05, 0, -0.08), yon=(0.55, -1.0, 0.45), uzak=2.4, lens=55, fstop=5.6)


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
    ap.add_argument('--sahne', default='tir')
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=48)
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
