"""
Ürün turu görünümü (Perde 2): teknik çizim röntgeni, kenar çizgili toplu ağ, stüdyo.

Röntgen = mavi-beyaz TEKNİK ÇİZİM: kutuların kenarlarında ince mavi çizgi, iç yüzey hafif saydam beyaz.
(Camsı / gürültülü eski röntgen kalktı.) Çizgi, kutu kenarına olan uzaklıktan shader'da hesaplanır:
her kutunun köşelerine yerel konum (bk) ve yarı boyut (bh) öznitelikleri yazılır; yüzeyde en küçük
ikinci (yüz düzlemi sıfır) kenar uzaklığıdır. Genişlik piksel cinsinden sabit (kamera uzaklığına oranlı).
Wireframe düğümü kullanılmaz: dörtgenlerin köşegenini de çizer.

Malzeme parametreleri (ayarla ile kare başına):
  G   hayalet miktarı (0 gerçek, 1 teknik çizim)     GU/TZ  tarama: z>TZ olan kısım GU kadar hayalet
  V   kaybolma (1 = tam saydam)                      H      lime vurgu (kenar çizgisi + hale) ; HZ/HD dalga eşiği ve yönü
  ISI turuncu ısı sızıntısı (yalnız kolon/kiriş)     CZ     harç çizgisi çizim eşiği (z)
  SICAK pencere sıcak ışığı (yalnız cam)

Lime YALNIZ Ege Gazbeton ürününe verilir (donatı, çelik, beton lime olamaz); bu kural çağıran tarafta.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import bpy  # noqa: E402
import stil_r as R  # noqa: E402

LIME = '#b8d84a'
LIME_DOYGUN = '#a2d52c'  # ışıyan çizgi için: ton eşlemesi açığa kaçırdığından biraz doygun
CIZGI_MAVI = '#2d6fc7'  # teknik çizim çizgisi
DOLGU = '#f6f9ff'  # hafif saydam beyaz iç
ISI_TURUNCU = '#ff7a2e'
SICAK_PENCERE = (1.0, 0.70, 0.42)

# tür → (çizgi opaklığı, dolgu opaklığı, çizgi genişliği çarpanı)
TUR_AYAR = {
    'kolon': (0.95, 0.20, 1.15), 'kiris': (0.95, 0.20, 1.15), 'doseme': (0.9, 0.16, 1.15), 'temel': (0.9, 0.16, 1.15),
    'blok': (0.30, 0.05, 0.8), 'ublok': (0.55, 0.06, 1.0), 'hatil': (0.7, 0.12, 1.0), 'lento': (0.75, 0.10, 1.0),
    'panel': (0.62, 0.09, 1.0), 'egepor': (0.8, 0.14, 1.0),
    'sove': (0.45, 0.06, 0.8), 'denizlik': (0.55, 0.08, 0.9), 'dograma': (0.6, 0.08, 0.9),
    'cam': (0.3, 0.10, 0.8), 'kapi': (0.6, 0.10, 0.9), 'donati': (0.7, 0.10, 1.0),
}


def _deger(nt, ad, v):
    n = nt.nodes.new('ShaderNodeValue')
    n.name = n.label = ad
    n.outputs[0].default_value = v
    return n.outputs[0]


def _ma(N, a, b, c, clamp=False):
    """a*b + c (düğüm ya da sayı)."""
    m = N.node('ShaderNodeMath', operation='MULTIPLY_ADD', use_clamp=clamp)
    for i, v in enumerate((a, b, c)):
        if isinstance(v, (int, float)):
            m.inputs[i].default_value = v
        else:
            N.link(v, m.inputs[i])
    return m.outputs[0]


def cizgili_mesh(name, merkez, olcek, mat=None, donme=None):
    """kit.toplu_mesh + kenar çizgisi öznitelikleri (bk: kutu merkezine göre yerel konum, bh: yarı boyut)."""
    merkez = np.asarray(merkez, dtype=np.float32).reshape(-1, 3)
    n = len(merkez)
    ol = np.asarray([(o, o, o) if np.ndim(o) == 0 else tuple(o) for o in olcek], dtype=np.float32).reshape(n, 3)
    ob = kit.toplu_mesh(name, kit.sablon('kup'), merkez, ol, donme, mat)
    tv, _ = kit.sablon('kup')
    k = len(tv)
    yerel = (tv[None, :, :] * ol[:, None, :]).reshape(-1, 3)
    yari = np.repeat(ol / 2.0, k, axis=0)
    me = ob.data
    for ad, dizi in (('bk', yerel), ('bh', yari)):
        a = me.attributes.new(name=ad, type='FLOAT_VECTOR', domain='POINT')
        a.data.foreach_set('vector', dizi.astype(np.float32).ravel())
    return ob


def kutu_nesne(name, c, s, mat, donme=None):
    """Tek kutu (çizgili öznitelikli) — parça başına animasyon gereken yerde."""
    return cizgili_mesh(name, [tuple(c)], [tuple(s)], mat, None if donme is None else [tuple(donme)])


def kur(P, mats, ad='Ev', donustur=None):
    """bina_detay.kur gibi: türe göre toplu ağ; fark: kenar çizgisi öznitelikli."""
    gruplar = {}
    for p in P:
        r = donustur(p) if donustur else (p['c'], p['s'], (0, 0, 0))
        if r is None:
            continue
        gruplar.setdefault(p['tur'], []).append(r)
    obs = {}
    for tur, lst in gruplar.items():
        obs[tur] = cizgili_mesh(f'{ad}_{tur}', [x[0] for x in lst], [x[1] for x in lst], mats[tur], [x[2] for x in lst])
    return obs


def _kenar_mesafesi(N):
    """Yüzey noktasının en yakın kutu kenarına uzaklığı (m)."""
    nt = N.t
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
    d = []
    for ax in ('X', 'Y', 'Z'):
        a = N.math('ABSOLUTE', sk.outputs[ax])
        d.append(N.math('SUBTRACT', sh.outputs[ax], a))
    mn_ab = N.math('MINIMUM', d[0], d[1])
    mx_ab = N.math('MAXIMUM', d[0], d[1])
    t = N.math('MINIMUM', mx_ab, d[2])
    return N.math('MAXIMUM', mn_ab, t)  # ikinci küçük = kenar uzaklığı


def teknik_malzeme(asil, ad, tur='blok', harc=False):
    """asil (gerçek malzeme) → [gerçek ↔ teknik çizim] karışımı + kaybolma + lime vurgu + (ısı | sıcak pencere)."""
    m = asil.copy()
    m.name = ad
    nt = m.node_tree
    N = kit.NT(nt)
    out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
    kaynak = out.inputs['Surface'].links[0].from_socket
    ca, da, gen = TUR_AYAR.get(tur, (0.6, 0.08, 1.0))

    G = _deger(nt, 'G', 0.0)
    GU = _deger(nt, 'GU', 0.0)
    TZ = _deger(nt, 'TZ', -99.0)
    V = _deger(nt, 'V', 0.0)
    H = _deger(nt, 'H', 0.0)
    HZ = _deger(nt, 'HZ', 99.0)
    K = _deger(nt, 'K', 0.0008)  # bir piksel = K × kamera uzaklığı (ayarla ile)
    HW = _deger(nt, 'HW', 0.6 * gen)  # mavi çizgi yarı genişliği (piksel)
    ISI = _deger(nt, 'ISI', 0.0)
    CZ = _deger(nt, 'CZ', 99.0)
    SICAK = _deger(nt, 'SICAK', 0.0)
    hd = nt.nodes.new('ShaderNodeCombineXYZ')
    hd.name = 'HD'
    hd.inputs['Z'].default_value = 1.0

    geo = nt.nodes.new('ShaderNodeNewGeometry')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(geo.outputs['Position'], sep.inputs[0])
    z = sep.outputs['Z']
    cam = nt.nodes.new('ShaderNodeCameraData')
    pp = N.math('MULTIPLY', cam.outputs['View Distance'], K)  # piksel boyu (m)
    pp = N.math('MAXIMUM', pp, 1e-5)

    # --- tarama: z > TZ olan kısım henüz taranmamış (GU), altı taranmış (G)
    t = _ma(N, N.math('SUBTRACT', z, TZ), 5.0, 0.5, clamp=True)
    g_eff = N.math('ADD', G, N.math('MULTIPLY', N.math('SUBTRACT', GU, G), t))

    if harc:
        # harç (derz arkası): gerçek koyu harç ↔ saydam; lime çizgi alttan yukarı çizilir (z < CZ)
        tr = nt.nodes.new('ShaderNodeBsdfTransparent')
        m1 = nt.nodes.new('ShaderNodeMixShader')
        nt.links.new(g_eff, m1.inputs['Fac'])
        nt.links.new(kaynak, m1.inputs[1])
        nt.links.new(tr.outputs[0], m1.inputs[2])
        m2 = nt.nodes.new('ShaderNodeMixShader')
        tr2 = nt.nodes.new('ShaderNodeBsdfTransparent')
        nt.links.new(V, m2.inputs['Fac'])
        nt.links.new(m1.outputs[0], m2.inputs[1])
        nt.links.new(tr2.outputs[0], m2.inputs[2])
        em = nt.nodes.new('ShaderNodeEmission')
        em.inputs['Color'].default_value = kit.srgb(LIME)
        cizim = _ma(N, N.math('SUBTRACT', CZ, z), 6.0, 0.5, clamp=True)
        nt.links.new(N.math('MULTIPLY', N.math('MULTIPLY', H, cizim), 3.2), em.inputs['Strength'])
        add = nt.nodes.new('ShaderNodeAddShader')
        nt.links.new(m2.outputs[0], add.inputs[0])
        nt.links.new(em.outputs[0], add.inputs[1])
        nt.links.new(add.outputs[0], out.inputs['Surface'])
        return m

    d2 = _kenar_mesafesi(N)
    oran = N.math('DIVIDE', d2, pp)  # kenara piksel cinsinden uzaklık
    mavi = N.math('SUBTRACT', N.math('ADD', HW, 0.5), oran, clamp=True)
    # lime dalga: c = P·HD; c < HZ olan yerde vurgu (alttan üste ya da soldan sağa)
    pdot = nt.nodes.new('ShaderNodeVectorMath')
    pdot.operation = 'DOT_PRODUCT'
    nt.links.new(geo.outputs['Position'], pdot.inputs[0])
    nt.links.new(hd.outputs['Vector'], pdot.inputs[1])
    dalga = _ma(N, N.math('SUBTRACT', HZ, pdot.outputs['Value']), 1.4, 0.5, clamp=True)
    hh = N.math('MULTIPLY', H, dalga)
    hmix = N.math('MULTIPLY', hh, 0.5, clamp=True)  # çizgi rengi maviden limea

    # --- hayalet: hafif saydam beyaz iç + mavi çizgi
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    dolgu = nt.nodes.new('ShaderNodeEmission')
    dolgu.inputs['Color'].default_value = kit.srgb(DOLGU)
    dolgu.inputs['Strength'].default_value = 1.0
    fill = nt.nodes.new('ShaderNodeMixShader')
    fill.inputs['Fac'].default_value = da
    nt.links.new(tr.outputs[0], fill.inputs[1])
    nt.links.new(dolgu.outputs[0], fill.inputs[2])
    cb = nt.nodes.new('ShaderNodeEmission')
    cb.inputs['Color'].default_value = kit.srgb(CIZGI_MAVI)
    nt.links.new(N.math('SUBTRACT', 1.0, hmix), cb.inputs['Strength'])
    cl = nt.nodes.new('ShaderNodeEmission')
    cl.inputs['Color'].default_value = kit.srgb(LIME)
    nt.links.new(N.math('MULTIPLY', hmix, 3.0), cl.inputs['Strength'])
    cs = nt.nodes.new('ShaderNodeAddShader')
    nt.links.new(cb.outputs[0], cs.inputs[0])
    nt.links.new(cl.outputs[0], cs.inputs[1])
    hay = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(N.math('MULTIPLY', mavi, ca), hay.inputs['Fac'])
    nt.links.new(fill.outputs[0], hay.inputs[1])
    nt.links.new(cs.outputs[0], hay.inputs[2])

    m1 = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(g_eff, m1.inputs['Fac'])
    nt.links.new(kaynak, m1.inputs[1])
    nt.links.new(hay.outputs[0], m1.inputs[2])
    m2 = nt.nodes.new('ShaderNodeMixShader')
    tr2 = nt.nodes.new('ShaderNodeBsdfTransparent')
    nt.links.new(V, m2.inputs['Fac'])
    nt.links.new(m1.outputs[0], m2.inputs[1])
    nt.links.new(tr2.outputs[0], m2.inputs[2])

    # --- lime vurgu: kenar çizgisi (yüzeyi örter: doygun lime) + yumuşak hale (ışıma)
    HWL = 1.7
    kenar = N.math('SUBTRACT', HWL + 0.5, oran, clamp=True)
    hale = N.math('SUBTRACT', 1.0, N.math('DIVIDE', oran, 5.0), clamp=True)
    hale = N.math('MULTIPLY', hale, hale)
    vgm = N.math('SUBTRACT', 1.0, V, clamp=True)
    hv = N.math('MULTIPLY', hh, vgm)
    lcizgi = nt.nodes.new('ShaderNodeEmission')
    lcizgi.inputs['Color'].default_value = kit.srgb(LIME_DOYGUN)
    lcizgi.inputs['Strength'].default_value = 1.35
    ml = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(N.math('MULTIPLY', N.math('MINIMUM', hv, 1.0), kenar), ml.inputs['Fac'])
    nt.links.new(m2.outputs[0], ml.inputs[1])
    nt.links.new(lcizgi.outputs[0], ml.inputs[2])
    lem = nt.nodes.new('ShaderNodeEmission')  # hale
    lem.inputs['Color'].default_value = kit.srgb(LIME_DOYGUN)
    nt.links.new(N.math('MULTIPLY', N.math('MULTIPLY', hv, hale), 0.16), lem.inputs['Strength'])
    add = nt.nodes.new('ShaderNodeAddShader')
    nt.links.new(ml.outputs[0], add.inputs[0])
    nt.links.new(lem.outputs[0], add.inputs[1])
    son = add.outputs[0]

    if tur in ('kolon', 'kiris', 'doseme'):
        # termal kamera: parçalı turuncu sızıntı (düşük frekans gürültü), kenarlara yakın biraz güçlü
        nz = nt.nodes.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = 0.9
        nz.inputs['Detail'].default_value = 2.0
        nt.links.new(geo.outputs['Position'], nz.inputs['Vector'])
        yog = _ma(N, nz.outputs['Fac'], 1.6, 0.25, clamp=True)
        kenar_a = N.math('SUBTRACT', 1.0, N.math('DIVIDE', oran, 30.0), clamp=True)
        isg = N.math('MULTIPLY', N.math('MULTIPLY', ISI, vgm), N.math('MULTIPLY', yog, _ma(N, kenar_a, 0.5, 0.5)))
        iem = nt.nodes.new('ShaderNodeEmission')
        iem.inputs['Color'].default_value = kit.srgb(ISI_TURUNCU)
        nt.links.new(N.math('MULTIPLY', isg, 1.5), iem.inputs['Strength'])
        add2 = nt.nodes.new('ShaderNodeAddShader')
        nt.links.new(son, add2.inputs[0])
        nt.links.new(iem.outputs[0], add2.inputs[1])
        son = add2.outputs[0]
    if tur == 'cam':
        sem = nt.nodes.new('ShaderNodeEmission')
        sem.inputs['Color'].default_value = (*SICAK_PENCERE, 1.0)
        nt.links.new(N.math('MULTIPLY', SICAK, vgm), sem.inputs['Strength'])
        add3 = nt.nodes.new('ShaderNodeAddShader')
        nt.links.new(son, add3.inputs[0])
        nt.links.new(sem.outputs[0], add3.inputs[1])
        son = add3.outputs[0]
    nt.links.new(son, out.inputs['Surface'])
    return m


def ayarla(m, g=None, v=None, h=None, hz=None, hd=None, isi=None, gu=None, tz=None, cz=None, sicak=None):
    """Malzeme parametrelerini yaz (None = dokunma). v≈1: 0,999 yerine tam 1 (ham malzeme hesaplanmasın)."""
    nodes = m.node_tree.nodes

    def yaz(ad, x):
        if x is not None and ad in nodes:
            nodes[ad].outputs[0].default_value = x
    yaz('G', g)
    if v is not None:
        yaz('V', 1.0 if v > 0.995 else v)
    yaz('H', h)
    yaz('HZ', hz)
    yaz('ISI', isi)
    yaz('GU', g if gu is None and g is not None else gu)
    yaz('TZ', tz)
    yaz('CZ', cz)
    yaz('SICAK', sicak)
    if hd is not None and 'HD' in nodes:
        for ax, val in zip('XYZ', hd):
            nodes['HD'].inputs[ax].default_value = val


def piksel_olcegi(malzemeler, lens, genislik_px, sensor=36.0):
    """Kenar çizgisi için piksel boyu çarpanı: 1 piksel = K × kamera uzaklığı."""
    k = (sensor / lens) / float(genislik_px)
    for m in malzemeler:
        if 'K' in m.node_tree.nodes:
            m.node_tree.nodes['K'].outputs[0].default_value = k


# ---------------------------------------------------------------------------
#  Stüdyo: hafif sıcak gri gradyan (beyaz ev öne çıksın), yumuşak ortam ışığı
# ---------------------------------------------------------------------------
def studyo(sc, anahtar=650.0, alt='#d9d3cb', orta='#cbc4bc', ust='#b4aea8', merkez=(0.62, 0.55), guc=1.45):
    """R.studyo ışıkları + kameranın gördüğü sıcak gri gradyan (ekran y'sine göre) ve çok hafif ışık lekesi."""
    R.studyo(sc, anahtar)
    nt = sc.world.node_tree
    gor = [n for n in nt.nodes if n.type == 'BACKGROUND' and n.inputs['Strength'].default_value > 1][0]
    gor.inputs['Strength'].default_value = guc
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Window'], sep.inputs[0])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.interpolation = 'EASE'
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = kit.srgb(alt)
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = kit.srgb(ust)
    e = ramp.color_ramp.elements.new(0.45)
    e.color = kit.srgb(orta)
    nt.links.new(sep.outputs['Y'], ramp.inputs['Fac'])
    # ışık lekesi: merkez çevresinde %10 daha açık (kenarlara doğru yumuşak düşer)
    dx = nt.nodes.new('ShaderNodeMath')
    dx.operation = 'SUBTRACT'
    dx.inputs[1].default_value = merkez[0]
    nt.links.new(sep.outputs['X'], dx.inputs[0])
    dy = nt.nodes.new('ShaderNodeMath')
    dy.operation = 'SUBTRACT'
    dy.inputs[1].default_value = merkez[1]
    nt.links.new(sep.outputs['Y'], dy.inputs[0])
    vm = nt.nodes.new('ShaderNodeVectorMath')
    vm.operation = 'LENGTH'
    cb = nt.nodes.new('ShaderNodeCombineXYZ')
    nt.links.new(dx.outputs[0], cb.inputs['X'])
    nt.links.new(dy.outputs[0], cb.inputs['Y'])
    nt.links.new(cb.outputs[0], vm.inputs[0])
    lk = nt.nodes.new('ShaderNodeMapRange')
    lk.interpolation_type = 'SMOOTHSTEP'
    lk.inputs['From Min'].default_value = 0.0
    lk.inputs['From Max'].default_value = 0.8
    lk.inputs['To Min'].default_value = 1.10
    lk.inputs['To Max'].default_value = 0.92
    nt.links.new(vm.outputs['Value'], lk.inputs['Value'])
    mul = nt.nodes.new('ShaderNodeMix')
    mul.data_type = 'RGBA'
    mul.blend_type = 'MULTIPLY'
    mul.inputs[0].default_value = 1.0  # Factor
    nt.links.new(ramp.outputs['Color'], mul.inputs[6])  # A (renk)
    # B: gri skala çarpanı
    comb = nt.nodes.new('ShaderNodeCombineColor')
    for ch in ('Red', 'Green', 'Blue'):
        nt.links.new(lk.outputs['Result'], comb.inputs[ch])
    nt.links.new(comb.outputs['Color'], mul.inputs[7])  # B (renk)
    nt.links.new(mul.outputs[2], gor.inputs['Color'])
    return sc.world
