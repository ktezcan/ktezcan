"""
Perde 2 — "Bu evi iyi yapan ne?" Ürün turu.

Ev parlak stüdyoda (maket dili); kamera evin etrafında bir tur atar. Her durakta o ürünün
parçaları gerçek malzemesinde kalır ve kenarında lime ışıltı belirir; geri kalan her şey
röntgen gibi saydamlaşır. Ürün adları ve özellik kartları sitede (HTML, TR/EN, kaynaklı).

Duraklar: duvar blokları → lento → U blok (çatı hatılı: kalıp yerine, içinde donatı + beton) → gazbeton tutkalı (derz)
          → çatı paneli → Egepor (kolon/kiriş kaplaması)
Kaynak: egegazbeton.com.tr ürün sayfaları (U Bloklar, Egepor).
Sonuç   : ev bütünleşir, kamera ön cephedeki tek bloğa iner; blok dışarı çıkar, gerisi beyaza erir
          ("Bu blok nasıl doğdu?" → doğuş sahnesi).

Kullanım: python s1_urun.py --variant d|m --out DIR [--frames all|0,40] [--samples N]
"""
import argparse
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
import stil_r as R  # noqa: E402
import stil_r3 as T  # noqa: E402
import stil_r4 as F  # noqa: E402
import bina_detay as B  # noqa: E402

FRAMES = 96
LIME = '#b8d84a'
RES = {'d': (1600, 900), 'm': (768, 1366)}
LENS = {'d': 35.0, 'm': 35.0}
UZAK = {'d': 34.0, 'm': 31.0}
HEDEF = Vector((0, 0, 4.6))
# (ad, türler, başla, bitir, kamera uzaklık çarpanı, yükseklik açısı)
DURAK = [
    ('duvar', ('blok',), 0.06, 0.17, 0.82, 14),
    ('lento', ('lento',), 0.185, 0.295, 0.80, 12),
    ('ublok', ('ublok', 'donati'), 0.31, 0.42, 0.09, 56),
    ('tutkal', ('harc',), 0.435, 0.545, 0.55, 8),
    ('panel', ('panel',), 0.56, 0.67, 0.95, 42),
    ('egepor', ('egepor',), 0.685, 0.795, 0.85, 16),
]
# durağa özel bakış noktası (U blok: çatı hatılı, parapet üstü)
DURAK_HEDEF = {'ublok': Vector((0.0, 0.0, B.KAT * B.FH + 0.35))}
ODAK_BLOK = (-3.0, 0)  # son dalış: ön cephe, zemin kat, x≈−3 civarı blok


def gecis_malzeme(asil, ad):
    """asil → (röntgen hayalet) → (tam saydam) karışımı; lime kenar ışıltısı ayrı değer."""
    m = asil.copy()
    m.name = ad
    nt = m.node_tree
    out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
    kaynak = out.inputs['Surface'].links[0].from_socket
    lw = nt.nodes.new('ShaderNodeLayerWeight')
    lw.inputs['Blend'].default_value = 0.3
    ham = nt.nodes.new('ShaderNodeEmission')  # hayalet: açık gri gövde + kenarda koyu çizgi hissi
    ham.inputs['Color'].default_value = kit.srgb('#dbe7f0')
    ham.inputs['Strength'].default_value = 1.15
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    hayalet = nt.nodes.new('ShaderNodeMixShader')
    pw = nt.nodes.new('ShaderNodeMath')
    pw.operation = 'POWER'
    pw.inputs[1].default_value = 1.5
    nt.links.new(lw.outputs['Facing'], pw.inputs[0])
    sk = nt.nodes.new('ShaderNodeMath')  # saydamlık: yüze dik bakışta çok saydam, kenarda daha opak
    sk.operation = 'MULTIPLY_ADD'
    sk.inputs[1].default_value = 0.6
    sk.inputs[2].default_value = 0.04
    nt.links.new(pw.outputs[0], sk.inputs[0])
    nt.links.new(sk.outputs[0], hayalet.inputs['Fac'])
    nt.links.new(tr.outputs[0], hayalet.inputs[1])
    nt.links.new(ham.outputs[0], hayalet.inputs[2])
    m1 = nt.nodes.new('ShaderNodeMixShader')
    m1.name = 'G'
    nt.links.new(kaynak, m1.inputs[1])
    nt.links.new(hayalet.outputs[0], m1.inputs[2])
    m2 = nt.nodes.new('ShaderNodeMixShader')
    m2.name = 'V'
    tr2 = nt.nodes.new('ShaderNodeBsdfTransparent')
    nt.links.new(m1.outputs[0], m2.inputs[1])
    nt.links.new(tr2.outputs[0], m2.inputs[2])
    # lime kenar ışıltısı (yalnız bizim ürün vurgusunda)
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = kit.srgb(LIME)
    hl = nt.nodes.new('ShaderNodeMath')
    hl.name = 'H'
    hl.operation = 'MULTIPLY'
    hl.inputs[1].default_value = 0.0
    pw2 = nt.nodes.new('ShaderNodeMath')
    pw2.operation = 'POWER'
    pw2.inputs[1].default_value = 4.0
    nt.links.new(lw.outputs['Facing'], pw2.inputs[0])
    nt.links.new(pw2.outputs[0], hl.inputs[0])
    nt.links.new(hl.outputs[0], em.inputs['Strength'])
    add = nt.nodes.new('ShaderNodeAddShader')
    nt.links.new(m2.outputs[0], add.inputs[0])
    nt.links.new(em.outputs[0], add.inputs[1])
    nt.links.new(add.outputs[0], out.inputs['Surface'])
    return m


def ayarla(m, g, v, h):
    nt = m.node_tree
    nt.nodes['G'].inputs['Fac'].default_value = g
    nt.nodes['V'].inputs['Fac'].default_value = 1.0 if v > 0.995 else v  # 0,999 ≈ görünmez: ham malzeme hesaplanmasın (koyu leke + yavaşlık)
    nt.nodes['H'].inputs[1].default_value = h


def egepor_parcalari():
    """Dış kolon ve kiriş önlerine 5 cm Egepor levha (ısı köprüsü yalıtımı)."""
    P = []
    t = 0.05
    for kat in range(B.KAT):
        z0 = kat * B.FH
        hz = B.FH - B.KIRIS_D
        for x in B.XS:
            for y, ny in ((B.YS[0], -1), (B.YS[-1], 1)):
                P.append(dict(c=(x, y + ny * (B.COL / 2 + t / 2), z0 + hz / 2), s=(B.COL + 0.04, t, hz), n=(0, ny, 0), tur='egepor'))
        for y in B.YS:
            for x, nx in ((B.XS[0], -1), (B.XS[-1], 1)):
                P.append(dict(c=(x + nx * (B.COL / 2 + t / 2), y, z0 + hz / 2), s=(t, B.COL + 0.04, hz), n=(nx, 0, 0), tur='egepor'))
        zk = z0 + B.FH - B.KIRIS_D / 2
        for y, ny in ((B.YS[0], -1), (B.YS[-1], 1)):
            P.append(dict(c=(0, y + ny * (B.COL / 2 + t / 2), zk), s=(B.XS[-1] - B.XS[0] + B.COL + 0.04, t, B.KIRIS_D), n=(0, ny, 0), tur='egepor'))
        for x, nx in ((B.XS[0], -1), (B.XS[-1], 1)):
            P.append(dict(c=(x + nx * (B.COL / 2 + t / 2), 0, zk), s=(t, B.YS[-1] - B.YS[0] + B.COL + 0.04, B.KIRIS_D), n=(nx, 0, 0), tur='egepor'))
    return P


def u_blok_parcalari(ub):
    """U blok: taban + iki yan cidar (U kesit); kanalda 4 donatı ve hatıl betonu."""
    out = []
    t = 0.05
    for p in ub:
        (cx, cy, cz), (sx, sy, sz) = p['c'], p['s']
        x_ekseni = sx > sy
        L, W = (sx, sy) if x_ekseni else (sy, sx)

        def k(du, dw, dz, l, w, h, tur):
            c = (cx + (0 if x_ekseni else dw), cy + (dw if x_ekseni else 0), cz + dz)
            s_ = (l, w, h) if x_ekseni else (w, l, h)
            out.append(dict(c=c, s=s_, tur=tur, n=p['n'], kat=p['kat'], sira=p['sira'], yuz=p['yuz'], zaman=p['zaman'], ana=p['c']))
        k(0, 0, -sz / 2 + t / 2, L, W, t, 'ublok')
        for sd in (-1, 1):
            k(0, sd * (W / 2 - t / 2), t / 2, L, t, sz - t, 'ublok')
            for dz in (-0.035, 0.045):
                k(0, sd * 0.035, dz, L + 0.012, 0.014, 0.014, 'donati')
        k(0, 0, t / 2 - 0.01, L + 0.012, W - 2 * t, sz - t - 0.02, 'hatil')
    return out


def kamera_pozu(u, variant):
    """Tur: −32°'den başlayıp 360° döner; duraklarda yavaşlar, yaklaşır."""
    # duraklarda yavaşlayan açı: hız fonksiyonunun integrali (sayısal)
    def hiz(x):
        v = 1.0
        for (_, _, a, b, _, _) in DURAK:
            v -= 0.75 * kit.smooth(kit.seg(x, a - 0.03, a + 0.02)) * (1 - kit.smooth(kit.seg(x, b - 0.02, b + 0.03)))
        return v
    N = 400
    toplam = sum(hiz(i / N) for i in range(N))
    kis = sum(hiz(i / N) for i in range(int(u * 0.86 / 1.0 * N)))  # 0.86'da tur tamam
    az = 32 + 360 * min(1.0, kis / (toplam * 0.86 + 1e-9))
    k_uz, k_el = 1.0, 18.0
    hedef = HEDEF.copy()
    for (ad, _, a, b, ku, el) in DURAK:
        w = kit.smooth(kit.seg(u, a - 0.04, a + 0.02)) * (1 - kit.smooth(kit.seg(u, b - 0.02, b + 0.04)))
        k_uz = kit.lerp(k_uz, ku, w)
        k_el = kit.lerp(k_el, el, w)
        if ad in DURAK_HEDEF:
            hedef = hedef.lerp(DURAK_HEDEF[ad], w)
    yon = Vector((math.sin(math.radians(az)) * math.cos(math.radians(k_el)),
                  -math.cos(math.radians(az)) * math.cos(math.radians(k_el)), math.sin(math.radians(k_el))))
    loc = hedef + yon * UZAK[variant] * k_uz
    # son: ön cephedeki odak bloğa dalış
    d = kit.smoother(kit.seg(u, 0.86, 1.0))
    if d > 0:
        hb = Vector((ODAK_BLOK[0], B.YS[0] - 0.4, 1.0))
        lb = hb + Vector((0.35, -1.0, 0.18)).normalized() * 2.4
        loc = loc.lerp(lb, d)
        hedef = hedef.lerp(hb, d)
    return loc, hedef, az


def main():
    kit.reset()
    v = ARGS.variant
    sc = kit.setup_render(*RES[v], samples=ARGS.samples, threshold=0.02, bounces=(6, 3, 3, 6))
    sc.cycles.transparent_max_bounces = 12
    sc.render.use_persistent_data = True
    if os.environ.get('EGE_PREVIEW'):
        sc.render.resolution_percentage = int(os.environ['EGE_PREVIEW'])
    R.studyo(sc)
    P, mats = T.bina_hazir()
    P = [p for p in P if p['tur'] != 'temel']
    EP = egepor_parcalari()
    mats['egepor'] = bpy.data.materials.get('Egepor') or bpy.data.materials.new('Egepor')
    mats['egepor'].use_nodes = True
    b = mats['egepor'].node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = kit.srgb('#f2efe7')
    b.inputs['Roughness'].default_value = 0.9
    # odak blok: ayrı nesne (son dalışta dışarı çıkar)
    odak = min((p for p in P if p['tur'] == 'blok' and p['kat'] == 0 and p['yuz'] == 'on' and p['sira'] == 3),
               key=lambda p: abs(p['c'][0] - ODAK_BLOK[0]))
    P.remove(odak)
    # çatı hatılı: parapetin üst sırası U blok (kanal içinde donatı + hatıl betonu)
    for p in P:
        if p['tur'] == 'blok' and p['kat'] == B.KAT and p['sira'] == 2:
            p['tur'] = 'ublok'
    UB = u_blok_parcalari([p for p in P if p['tur'] == 'ublok'])
    mats['ublok'] = mats['blok']
    mats['hatil'] = mats['kolon']
    mats['donati'] = bpy.data.materials.new('Donati')
    mats['donati'].use_nodes = True
    bd = mats['donati'].node_tree.nodes['Principled BSDF']
    bd.inputs['Base Color'].default_value = kit.srgb('#3b3530')
    bd.inputs['Metallic'].default_value = 0.8
    bd.inputs['Roughness'].default_value = 0.45
    turler = sorted(set(p['tur'] for p in P) | {'hatil', 'donati'}) + ['egepor']
    gm = {t: gecis_malzeme(mats[t], 'Gecis_' + t) for t in turler}
    # detay: kameraya bakan cephenin ortasındaki 3 U blok durakta havaya kalkar (açık kesit)
    um = sum(DURAK[2][2:4]) / 2
    _, _, az_m = kamera_pozu(um, v)
    gz = Vector((math.sin(math.radians(az_m)), -math.cos(math.radians(az_m)), 0))
    yuzn = max({tuple(p['n']) for p in UB}, key=lambda n: Vector(n).dot(gz))
    # kameraya bakan parapetin önünde, havada 3'lü U blok kesiti (kanal, donatı, dolan hatıl betonu)
    x_ekseni = abs(yuzn[1]) > 0.5
    eksen = Vector((1, 0, 0)) if x_ekseni else Vector((0, 1, 0))
    yuz_k = (B.YS[0] if yuzn[1] < 0 else B.YS[-1]) if x_ekseni else (B.XS[0] if yuzn[0] < 0 else B.XS[-1])
    UT = Vector((0, yuz_k, 0)) if x_ekseni else Vector((yuz_k, 0, 0))
    UT = UT + Vector(yuzn) * 2.2 + Vector((0, 0, B.KAT * B.FH + 1.2))
    sahte = []
    for i in range(3):
        c = UT + eksen * (i - 1) * 0.6
        sz = (0.588, 0.25, 0.238) if x_ekseni else (0.25, 0.588, 0.238)
        sahte.append(dict(c=tuple(c), s=sz, tur='ublok', n=yuzn, kat=B.KAT, sira=2, yuz='', zaman=0))
    DETAY = u_blok_parcalari(sahte)
    UB_kalan = UB
    DURAK_HEDEF['ublok'] = UT
    obs = B.kur([p for p in P if p['tur'] != 'ublok'] + UB_kalan, gm, ad='Ev')
    detay_obs = list(B.kur([p for p in DETAY if p['tur'] != 'hatil'], gm, ad='UDetay').values())
    dh = [p for p in DETAY if p['tur'] == 'hatil']
    hatil_ob = kit.toplu_mesh('UDetay_hatil', kit.sablon('kup'), [p['c'] for p in dh], [p['s'] for p in dh], None, gm['hatil'])
    hz0 = min(p['c'][2] - p['s'][2] / 2 for p in dh)
    odak_m = gecis_malzeme(mats['blok'], 'Gecis_odak')
    odak_ob = kit.toplu_mesh('OdakBlok', kit.sablon('kup'), [odak['c']], [odak['s']], None, odak_m)
    ep_ob = kit.toplu_mesh('Ev_egepor', kit.sablon('kup'), [p['c'] for p in EP], [p['s'] for p in EP], None, gm['egepor'])
    F.zemin(0.0)
    cam = kit.camera('Kamera', lens=LENS[v], loc=(0, -30, 8), target=HEDEF, fstop=11, focus=30)
    cam.data.dof.use_dof = False
    kit.sinematik(bloom=0.25, esik=1.3, boyut=0.5)

    frames = pass_order(FRAMES) if ARGS.frames == 'all' else [int(x) for x in ARGS.frames.split(',')]
    os.makedirs(ARGS.out, exist_ok=True)
    meta_path = os.path.join(ARGS.out, 'meta.json')
    meta = {'frames': FRAMES, 'res': list(RES[v]), 'hotspots': {}}
    if os.path.exists(meta_path):
        import json
        eski = json.load(open(meta_path))
        if eski.get('frames') == FRAMES:
            meta['hotspots'].update(eski.get('hotspots', {}))
    for f in frames:
        u = f / (FRAMES - 1)
        loc, hedef, az = kamera_pozu(u, v)
        cam.location = loc
        kit.aim(cam, hedef)
        kit.kaydir(cam, v, 1.0 - kit.smooth(kit.seg(u, 0.88, 1.0)))
        # vurgu ağırlıkları
        vurgu = {t: 0.0 for t in turler}
        for (ad, tl, a, b_, _, _) in DURAK:
            w = kit.smooth(kit.seg(u, a, a + 0.035)) * (1 - kit.smooth(kit.seg(u, b_ - 0.035, b_)))
            for t in tl:
                vurgu[t] = max(vurgu[t], w)
        herhangi = max(vurgu.values())
        dal = kit.smooth(kit.seg(u, 0.88, 0.97))
        # dalış: kamera yığılı saydam katmanların içinden geçer; 12 sıçrama yetmez (siyah leke) → 32.
        # Ev tamamen saydamlaşınca (dal ≥ 0,995) nesneler hiç çizilmesin (hem leke hem hız)
        sc.cycles.transparent_max_bounces = 32 if dal > 0.02 else 12
        ev_gizli = dal >= 0.995
        for o in list(obs.values()):
            o.hide_render = ev_gizli
        for t in turler:
            g = herhangi * (1 - vurgu[t])
            if t in ('harc', 'donati'):  # içte kalan parçalar: hayalet olmaz, vurguda lime
                g = 0.0
            # lime yalnız Ege ürünü: donatı (çelik) çerçevelenmez
            ayarla(gm[t], g, dal, 0.0 if t == 'donati' else 6.0 * vurgu[t])
        # harç vurgusu: bloklar hayalete döner, harç ağı görünür
        if vurgu['harc'] > 0:
            ayarla(gm['blok'], vurgu['harc'] * 0.92, dal, 0.0)
        ayarla(odak_m, herhangi, 0.0, 6.0 * dal)
        # Egepor: durağında levhalar dışarıdan uçarak yerine oturur, sonra kalır
        ea = kit.ease_out(kit.seg(u, 0.68, 0.74), 3)
        ep_ob.hide_render = ea <= 0 or ev_gizli
        ep_ob.location = (0, 0, 0)
        ep_ob.scale = (1, 1, 1)
        if 0 < ea < 1:
            s = 1 + 0.35 * (1 - ea)
            ep_ob.scale = (s, s, 1 + 0.1 * (1 - ea))
        # U blok detayı: durakta parapetten kalkar, sonra yerine oturur
        a_, b_ = DURAK[2][2], DURAK[2][3]
        kalk = kit.smoother(kit.seg(u, a_ - 0.01, a_ + 0.04)) * (1 - kit.smoother(kit.seg(u, b_ - 0.04, b_)))
        for o in detay_obs + [hatil_ob]:
            o.hide_render = kalk <= 0.001
        for o in detay_obs:
            o.location = UT * (1 - kalk)
            o.scale = (kalk, kalk, kalk)
        # hatıl betonu: kanal boş görünür, sonra dolar (U blok kalıp görevi görür)
        dol = 1.0 - kalk * (1 - kit.smooth(kit.seg(u, a_ + 0.065, b_ - 0.01)))
        dol = max(dol, 0.002)
        S_ = Vector((kalk, kalk, kalk * dol))
        Q = Vector((UT.x, UT.y, hz0))  # pivot: kanal tabanı (beton aşağıdan yukarı dolar)
        hatil_ob.scale = S_
        hatil_ob.location = Q - Vector((S_.x * Q.x, S_.y * Q.y, S_.z * Q.z))
        ayarla(gm['hatil'], 0.0 if kalk > 0.01 else gm['hatil'].node_tree.nodes['G'].inputs['Fac'].default_value, dal, 0.0)
        # odak blok dışarı çıkar
        cik = kit.smoother(kit.seg(u, 0.92, 1.0))
        odak_ob.location = (0, -0.45 * cik, 0)
        # noktalar
        hs = {}
        if 0.0 < herhangi:
            for (ad, tl, a, b_, _, _) in DURAK:
                if a + 0.02 <= u <= b_ - 0.01:
                    kaynak = EP if ad == 'egepor' else [q for q in DETAY if q['tur'] == 'ublok'] if ad == 'ublok' else [p for p in P if p['tur'] in tl]
                    goz = cam.location
                    adaylar = [p for p in kaynak if Vector(p['n']).dot(goz - Vector(p['c'])) > 0] or kaynak
                    pr = kit.project(cam, [p['c'] for p in adaylar])
                    hedef_ekran = (0.68, 0.42) if v == 'd' else (0.5, 0.62)
                    en = min(((q, p) for q, p in zip(pr, adaylar) if q and 0.05 < q[0] < 0.95 and 0.08 < q[1] < 0.92),
                             key=lambda qp: (qp[0][0] - hedef_ekran[0]) ** 2 + (qp[0][1] - hedef_ekran[1]) ** 2, default=None)
                    if en:
                        hs['u_' + ad] = en[0]
        if u > 0.95:
            q = kit.project(cam, [Vector(odak['c']) + Vector((0, -0.45 - 0.13, 0))])[0]
            if q:
                hs['u_blok'] = q
        meta['hotspots'][str(f)] = hs
        path = os.path.join(ARGS.out, f'{f:03d}.png')
        kit.write_json(meta_path, meta)
        if ARGS.skip_existing and os.path.exists(path):
            continue
        t0 = time.time()
        kit.render_to(path)
        print(f'KARE {f} {time.time() - t0:.1f}s', flush=True)
    kit.write_json(meta_path, meta)


def pass_order(n):
    order, seen = [], set()
    min_step = int(os.environ.get('EGE_MINSTEP', '1'))
    for step in [x for x in (8, 4, 2, 1) if x >= min_step]:
        for f in range(0, n, step):
            if f not in seen:
                seen.add(f)
                order.append(f)
    if n - 1 in order:
        order.remove(n - 1)
    order.insert(1, n - 1)
    return order


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--variant', default='d')
    ap.add_argument('--frames', default='all')
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=28)
    ap.add_argument('--skip-existing', action='store_true')
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
