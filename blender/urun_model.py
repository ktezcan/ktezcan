"""
Ürün turu (Perde 2) sahne parçaları: iç bölme duvarı, öne çıkan bloklar, kesit parçası, ısı/yük okları,
U blok detayı (kanal + donatı + dolan beton), tutkal torbası, panel şeritleri, Egepor levha grupları.

Kural hatırlatma: lime YALNIZ Ege Gazbeton ürününe (blok, lento, U blok, tutkal, panel, Egepor); donatı, çelik, beton,
ısı oku lime OLAMAZ. Render içinde yazı yok. Tüm 'teknik çizim' (G.teknik_malzeme) nesneleri G.cizgili_mesh ile
kurulur (bk/bh öznitelikleri), başka yolla kurulan ağlar yalnız düz malzeme alır.
"""
import math
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
import stil_r2 as Q  # noqa: E402
import bina_detay as B  # noqa: E402
import urun_gorunum as G  # noqa: E402

IC_T = 0.10  # iç bölme duvarı kalınlığı
STEEL = '#8d949b'


# ---------------------------------------------------------------------------
#  Şablonlar (silindir, koni) ve yön
# ---------------------------------------------------------------------------
def silindir_sablon(n=10, koni=False):
    """z ekseninde, yarıçap 0,5, boy 1 (z −0,5..0,5). koni: tabanı z=−0,5, ucu z=+0,5."""
    a = [2 * math.pi * i / n for i in range(n)]
    alt = [(0.5 * math.cos(t), 0.5 * math.sin(t), -0.5) for t in a]
    if koni:
        v = alt + [(0.0, 0.0, 0.5)]
        f = [list(range(n - 1, -1, -1))] + [[i, (i + 1) % n, n] for i in range(n)]
    else:
        ust = [(x, y, 0.5) for (x, y, _) in alt]
        v = alt + ust
        f = [list(range(n - 1, -1, -1)), list(range(n, 2 * n))]
        for i in range(n):
            j = (i + 1) % n
            f.append([i, j, n + j, n + i])
    return np.array(v, dtype=np.float32), f


def yon_donme(d):
    """Yerel +Z'yi d yönüne çeviren Euler XYZ."""
    return tuple(Vector(d).normalized().to_track_quat('Z', 'Y').to_euler('XYZ'))


def silindirler(ad, liste, mat, n=10):
    """liste: [(p0, p1, çap)] — p0→p1 arası silindir (donatı gibi)."""
    mer, ol, dn = [], [], []
    for p0, p1, d in liste:
        a, b = Vector(p0), Vector(p1)
        v = b - a
        mer.append(tuple((a + b) / 2))
        ol.append((d, d, v.length))
        dn.append(yon_donme(v))
    return kit.toplu_mesh(ad, silindir_sablon(n), mer, ol, dn, mat, yumusak=True)


def oklar(ad, liste, mat, n=10):
    """liste: [(p0, p1, yarıçap)] — gövde p0→uç; ucunda koni başlık. Dönüş: [gövde_ob, baş_ob]."""
    gm, go, gd, bm_, bo, bd = [], [], [], [], [], []
    for p0, p1, r in liste:
        a, b = Vector(p0), Vector(p1)
        v = b - a
        L = v.length
        dn = v / L
        hl = min(L * 0.45, r * 6.5)
        gl = L - hl
        e = yon_donme(v)
        gm.append(tuple(a + dn * gl / 2))
        go.append((2 * r, 2 * r, gl))
        gd.append(e)
        bm_.append(tuple(a + dn * (gl + hl / 2)))
        bo.append((5.2 * r, 5.2 * r, hl))
        bd.append(e)
    g = kit.toplu_mesh(ad + '_g', silindir_sablon(n), gm, go, gd, mat, yumusak=True)
    b = kit.toplu_mesh(ad + '_b', silindir_sablon(n, koni=True), bm_, bo, bd, mat, yumusak=True)
    return [g, b]


def ok_malzemesi(ad, renk, guc=3.0):
    """Yalnız ışıyan ok malzemesi; 'S' düğümü şiddeti (ayarla ile kare kare)."""
    m = bpy.data.materials.new(ad)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = kit.srgb(renk)
    s = nt.nodes.new('ShaderNodeValue')
    s.name = 'S'
    s.outputs[0].default_value = guc
    nt.links.new(s.outputs[0], em.inputs['Strength'])
    nt.links.new(em.outputs[0], out.inputs['Surface'])
    return m


def ok_guc(m, x):
    m.node_tree.nodes['S'].outputs[0].default_value = x


def perde_malzemesi(ad, renk, alfa=0.1, guc=1.0):
    """Yumuşak ışık perdesi (yarı saydam düzlem): saydam ↔ ışıma karışımı."""
    m = bpy.data.materials.new(ad)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = kit.srgb(renk)
    em.inputs['Strength'].default_value = guc
    mx = nt.nodes.new('ShaderNodeMixShader')
    mx.name = 'A'
    mx.inputs['Fac'].default_value = alfa
    nt.links.new(tr.outputs[0], mx.inputs[1])
    nt.links.new(em.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])
    return m


def perde_alfa(m, a):
    m.node_tree.nodes['A'].inputs['Fac'].default_value = a


def kenar_oznitelikleri(ob, yari):
    """Kutu olmayan (geçmeli blok gibi) ağa bk/bh öznitelikleri: kenar çizgisi sınırlayıcı kutuya göre çizilir."""
    me = ob.data
    n = len(me.vertices)
    co = np.empty(n * 3, dtype=np.float32)
    me.vertices.foreach_get('co', co)
    for ad, dizi in (('bk', co), ('bh', np.tile(np.asarray(yari, dtype=np.float32), n))):
        a = me.attributes.new(name=ad, type='FLOAT_VECTOR', domain='POINT')
        a.data.foreach_set('vector', dizi)


# ---------------------------------------------------------------------------
#  Harç çizgisi (derz ağı): kutu kenarları = derz hatları
# ---------------------------------------------------------------------------
def harc_cizgi_malzemesi(asil, ad):
    """Derz hatları: harç kutularının kenarları tam derz ortasına denk gelir. Yalnız ince lime çizgi; iç saydam.
    Parametreler: H (parlaklık), CZH (yatay derzler z < CZH çizilir), CZV (düşey derzler), K (piksel boyu)."""
    m = asil.copy()
    m.name = ad
    nt = m.node_tree
    nt.nodes.clear()
    N = kit.NT(nt)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    H = G._deger(nt, 'H', 0.0)
    CZH = G._deger(nt, 'CZH', -99.0)
    CZV = G._deger(nt, 'CZV', -99.0)
    K = G._deger(nt, 'K', 0.0008)
    HW = G._deger(nt, 'HW', 1.5)
    bk = nt.nodes.new('ShaderNodeAttribute')
    bk.attribute_type = 'GEOMETRY'
    bk.attribute_name = 'bk'
    bh = nt.nodes.new('ShaderNodeAttribute')
    bh.attribute_type = 'GEOMETRY'
    bh.attribute_name = 'bh'
    sk = nt.nodes.new('ShaderNodeSeparateXYZ')
    sh = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(bk.outputs['Vector'], sk.inputs[0])
    nt.links.new(bh.outputs['Vector'], sh.inputs[0])
    d = [N.math('SUBTRACT', sh.outputs[ax], N.math('ABSOLUTE', sk.outputs[ax])) for ax in ('X', 'Y', 'Z')]
    yan = N.math('MAXIMUM', d[0], d[1])  # düşey derz çizgisi: yan kenara uzaklık (ön yüz düzlemindeki eksen)
    geo = nt.nodes.new('ShaderNodeNewGeometry')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(geo.outputs['Position'], sep.inputs[0])
    z = sep.outputs['Z']
    cam = nt.nodes.new('ShaderNodeCameraData')
    pp = N.math('MAXIMUM', N.math('MULTIPLY', cam.outputs['View Distance'], K), 1e-5)

    def cizgi(uzak, esik):
        px = N.math('DIVIDE', uzak, pp)
        maske = N.math('SUBTRACT', N.math('ADD', HW, 0.5), px, clamp=True)
        cizim = G._ma(N, N.math('SUBTRACT', esik, z), 4.0, 0.5, clamp=True)  # alttan yukarı çizilir
        return N.math('MULTIPLY', maske, cizim)
    mh = cizgi(d[2], CZH)
    mv = cizgi(yan, CZV)
    mask = N.math('MULTIPLY', N.math('MINIMUM', N.math('ADD', mh, mv), 1.0), H, clamp=True)
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = kit.srgb(G.LIME_DOYGUN)
    em.inputs['Strength'].default_value = 3.2
    mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(mask, mx.inputs['Fac'])
    nt.links.new(tr.outputs[0], mx.inputs[1])
    nt.links.new(em.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])
    return m


def harc_ayarla(m, h=None, czh=None, czv=None):
    nodes = m.node_tree.nodes
    for ad, x in (('H', h), ('CZH', czh), ('CZV', czv)):
        if x is not None:
            nodes[ad].outputs[0].default_value = x


# ---------------------------------------------------------------------------
#  İç bölme duvarı (y=0 aksı; ürün hem dışta hem içte)
# ---------------------------------------------------------------------------
def ic_duvar_parcalari():
    P = []
    for kat in range(B.KAT):
        z0 = kat * B.FH
        for xa, xb in zip(B.XS[:-1], B.XS[1:]):
            a0, a1 = xa + B.COL / 2, xb - B.COL / 2
            m = (a0 + a1) / 2
            for sira in range(B.SIRA):
                z = z0 + (sira + 0.5) * B.BH
                kay = 0.0 if sira % 2 == 0 else B.BL / 2
                dolu = [(a0, m - 0.45), (m + 0.45, a1)] if sira < 8 else [(a0, a1)]  # kapı boşluğu 0,9 m
                for (p0, p1) in dolu:
                    u = a0 - kay
                    while u < p1 - 1e-6:
                        b0, b1 = max(u, p0), min(u + B.BL, p1)
                        if b1 - b0 > 0.02:
                            P.append(B._p(((b0 + b1) / 2, 0.0, z), ((b1 - b0) - B.DERZ, IC_T, B.BH - B.DERZ), 'icblok',
                                          kat=kat, sira=sira))
                        u += B.BL
    return P


# ---------------------------------------------------------------------------
#  Öne çıkan bloklar (düz + geçmeli) ve tek odak bloğu
# ---------------------------------------------------------------------------
def duvardan_blok_sec(P, yuz, kat, sira, y_hedef, sayi=2):
    """Belirli cephe/kat/sıradaki, y_hedef'e en yakın `sayi` bitişik bloğu (duvar parçaları) döndür."""
    adaylar = sorted((p for p in P if p['tur'] == 'blok' and p['yuz'] == yuz and p['kat'] == kat and p['sira'] == sira),
                     key=lambda p: abs(p['c'][1] - y_hedef))
    secim = adaylar[:sayi]
    return sorted(secim, key=lambda p: p['c'][1])


def gecmeli_blok_nesne(ad, mat, L=0.6, H=0.25, T=0.25):
    """Geçmeli blok (kit.gecmeli_blok) + kenar çizgisi öznitelikleri; merkez=yerel orijin."""
    ob = kit.gecmeli_blok(ad, L, H, T, mat)
    # yerel orijin z=H/2'de (kit.box loc); köşe koordinatları orijin merkezli
    kenar_oznitelikleri(ob, (L / 2, T / 2, H / 2))
    return ob


# ---------------------------------------------------------------------------
#  U blok detayı: kanal (taban + 2 cidar), donatı (silindir), dolan hatıl betonu
# ---------------------------------------------------------------------------
def u_blok_detay(sahte, t=0.05):
    """sahte: dict listesi (c, s, n...). Dönüş: kabuk parçaları, donatı [(p0,p1,çap)], hatıl [(c,s)]."""
    kabuk, donati, hatil = [], [], []
    for p in sahte:
        (cx, cy, cz), (sx, sy, sz) = p['c'], p['s']
        xe = sx > sy
        L, W = (sx, sy) if xe else (sy, sx)

        def yer(dw, dz):
            return (cx + (0 if xe else dw), cy + (dw if xe else 0), cz + dz)

        def boy(l, w, h):
            return (l, w, h) if xe else (w, l, h)

        kabuk.append(dict(c=yer(0, -sz / 2 + t / 2), s=boy(L, W, t), tur='ublok', n=p['n']))
        for sd in (-1, 1):
            kabuk.append(dict(c=yer(sd * (W / 2 - t / 2), t / 2), s=boy(L, t, sz - t), tur='ublok', n=p['n']))
            for dz in (-0.03, 0.045):  # her yanda iki donatı (dört çubuk)
                c = Vector(yer(sd * 0.045, dz))
                e = Vector((1, 0, 0)) if xe else Vector((0, 1, 0))
                donati.append((tuple(c - e * (L / 2 + 0.03)), tuple(c + e * (L / 2 + 0.03)), 0.022))
        hatil.append((yer(0, t / 2 - 0.01), boy(L + 0.012, W - 2 * t, sz - t - 0.02)))
    return kabuk, donati, hatil


# ---------------------------------------------------------------------------
#  Kesit parçası (ısı akışı): 20 cm duvar kesiti, 6 sıra blok, kesit yüzü +x'e bakar
# ---------------------------------------------------------------------------
def kesit_parcalari(c, derinlik=1.2, sira=6, kalinlik=0.2):
    """Eksen: derinlik x boyunca (kesit yüzü x_max'ta), kalınlık y, yükseklik z. c: orta nokta."""
    P = []
    gap = 0.004
    h0 = c[2] - sira * B.BH / 2
    for s in range(sira):
        kay = 0.0 if s % 2 == 0 else 0.3
        x0 = c[0] - derinlik / 2
        u = x0 - kay
        while u < x0 + derinlik - 1e-6:
            a0, a1 = max(u, x0), min(u + 0.6, x0 + derinlik)
            if a1 - a0 > 0.02:
                P.append(B._p(((a0 + a1) / 2, c[1], h0 + (s + 0.5) * B.BH), ((a1 - a0) - gap, kalinlik, B.BH - gap), 'blok'))
            u += 0.6
    return P


def isi_oklari(c, kalinlik=0.2, sira=5, ek_x=0.02):
    """Isı oku kümesi (y yönünde, içeriden dışarıya). Üç aşama: güçlü (iç), orta (duvar içinde), soluk (dış).
    Dönüş: (güçlü, orta, soluk) liste: [(p0, p1, r)]. Oklar kesit yüzünün hemen önünde (x_max + ek_x)."""
    guclu, orta, soluk = [], [], []
    xf = c[0] + 0.6 + ek_x
    for j in range(sira):
        z = c[2] + (j - (sira - 1) / 2) * 0.27
        guclu.append(((xf, c[1] - 0.95, z), (xf, c[1] - kalinlik / 2 - 0.02, z), 0.026))
        orta.append(((xf, c[1] - kalinlik / 2 + 0.01, z), (xf, c[1] + kalinlik / 2 - 0.01, z), 0.015))
        soluk.append(((xf, c[1] + kalinlik / 2 + 0.03, z), (xf, c[1] + 0.42, z), 0.007))
    return guclu, orta, soluk


# ---------------------------------------------------------------------------
#  Tutkal torbası (lime şeritli beyaz ambalaj, yazısız)
# ---------------------------------------------------------------------------
def torba(ad='Torba', olcek=1.0):
    """Yastık biçimli torba: merkez zeminde, boy ≈ 0,60 m. Lime bant gölgelendiricide (z aralığı)."""
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=9, use_grid_fill=True)
    W, D, Hh = 0.40, 0.15, 0.62
    for v in bm.verts:
        x, y, z = v.co
        nx, nz = x / 0.5, z / 0.5
        yast = 0.35 + 0.65 * max(0.0, (1 - nx * nx)) ** 0.7 * max(0.0, (1 - nz * nz)) ** 0.55  # kenarlar ince, orta şişkin
        v.co = Vector((x * W, y * D * yast, (z + 0.5) * Hh))
        # üst ve alt dikişe doğru hafif sıkışma
        if z > 0.46 or z < -0.46:
            v.co.y *= 0.45
    me = bpy.data.meshes.new(ad)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    m = bpy.data.materials.new(ad + 'M')
    m.use_nodes = True
    nt = m.node_tree
    N = kit.NT(nt)
    b = nt.nodes['Principled BSDF']
    b.inputs['Roughness'].default_value = 0.62
    b.inputs['Specular IOR Level'].default_value = 0.35
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs[0])
    band = nt.nodes.new('ShaderNodeMapRange')
    band.interpolation_type = 'SMOOTHSTEP'
    band.inputs['From Min'].default_value = 0.30
    band.inputs['From Max'].default_value = 0.31
    nt.links.new(sep.outputs['Z'], band.inputs['Value'])
    ust = nt.nodes.new('ShaderNodeMapRange')
    ust.interpolation_type = 'SMOOTHSTEP'
    ust.inputs['From Min'].default_value = 0.43
    ust.inputs['From Max'].default_value = 0.44
    nt.links.new(sep.outputs['Z'], ust.inputs['Value'])
    maske = N.math('SUBTRACT', band.outputs['Result'], ust.outputs['Result'], clamp=True)
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    nt.links.new(maske, mix.inputs['Factor'])
    mix.inputs['A'].default_value = kit.srgb('#f3f1ec')
    mix.inputs['B'].default_value = kit.srgb(G.LIME)
    nt.links.new(mix.outputs['Result'], b.inputs['Base Color'])
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 38.0
    nz.inputs['Detail'].default_value = 5.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    bp = nt.nodes.new('ShaderNodeBump')
    bp.inputs['Strength'].default_value = 0.18
    bp.inputs['Distance'].default_value = 0.01
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    me.materials.append(m)
    ob = bpy.data.objects.new(ad, me)
    kit.link(ob)
    ob.scale = (olcek, olcek, olcek)
    return ob


# ---------------------------------------------------------------------------
#  Panel şeritleri (parça başına nesne: piyano tuşu) ve Egepor grupları
# ---------------------------------------------------------------------------
def panel_seritleri(P, mat):
    """Çatı panelleri x konumuna göre gruplanır; her şerit (iki açıklık) tek nesne. Dönüş: [(x, nesne)]."""
    gruplar = {}
    for p in P:
        if p['tur'] == 'panel':
            gruplar.setdefault(round(p['c'][0], 3), []).append(p)
    out = []
    for i, x in enumerate(sorted(gruplar)):
        lst = gruplar[x]
        ob = G.cizgili_mesh(f'Panel_{i:02d}', [p['c'] for p in lst], [p['s'] for p in lst], mat)
        out.append((x, ob))
    return out


def egepor_gruplari(EP, sirala, adet, mats_kopya):
    """EP parçaları `sirala(p)` anahtarıyla sıralanıp `adet` gruba bölünür; her grup kendi malzemesiyle ayrı nesne.
    Dönüş: [(nesne, malzeme, parçalar)]."""
    srt = sorted(EP, key=sirala)
    n = len(srt)
    out = []
    for g in range(adet):
        lst = srt[g * n // adet:(g + 1) * n // adet]
        if not lst:
            continue
        m = mats_kopya(g)
        ob = G.cizgili_mesh(f'Egepor_{g}', [p['c'] for p in lst], [p['s'] for p in lst], m)
        out.append((ob, m, lst))
    return out


# ---------------------------------------------------------------------------
#  Yük okları (lento): nötr mavi-gri; lime/turuncu değil
# ---------------------------------------------------------------------------
def yuk_oklari(c_lento, yuzn, yarim_boy, z_ust=0.95):
    """Lentonun üstünden inen 5 ok + iki yana (oturma noktalarına) yayılan 2 eğik ok. yuzn: dış normal (x ya da y)."""
    n = Vector(yuzn)
    t = Vector((-n.y, n.x, 0))  # cephe boyunca birim
    c = Vector(c_lento) + n * 0.16  # lentonun hemen önünde
    ust, yay = [], []
    for k in range(5):
        o = (k - 2) * 0.28 * (yarim_boy / 0.85)
        ust.append((tuple(c + t * o + Vector((0, 0, z_ust))), tuple(c + t * o + Vector((0, 0, 0.17))), 0.016))
    for sd in (-1, 1):
        yay.append((tuple(c + t * sd * 0.22 + Vector((0, 0, 0.0))), tuple(c + t * sd * (yarim_boy + 0.05) + Vector((0, 0, -0.42))), 0.016))
    return ust, yay
