"""
Ayrıntılı bina üreticisi (gerçek ölçü, metre) — stüdyo hikâyesi için.

Betonarme karkas (temel, kolon, kiriş, döşeme) + kolonlar arasında nizami gazbeton
dolgu duvar: 60×25 cm yüz, 20 cm kalınlık, şaşırtmalı (yarım blok kaydırmalı) örgü,
bölme sonunda kesik blok, ince derz (derz arkasında koyu harç yüzeyi görünür).
Pencere: gazbeton lento (üstte, iki yana 25 cm oturur), denizlik, beyaz doğrama, cam.
Kapı: zemin kat ön cephe orta bölme. Çatı: parapet (3 sıra blok) + gazbeton çatı panelleri.

Her parça bir sözlük: c (merkez), s (boyut), tur, kat, sira, n (dış normal), zaman (yapım sırası 0..1).
Malzemeler türe göre toplu ağ olarak kurulur (kit.toplu_mesh) — binlerce parça saniyeler içinde.
"""
import math
import random

import bpy
from mathutils import Vector

import kit

XS = [-6.0, -2.0, 2.0, 6.0]
YS = [-4.5, 0.0, 4.5]
KAT = 3
FH = 3.0
SLAB = 0.15
KIRIS_D = 0.50  # döşeme dahil
KIRIS_W = 0.25
COL = 0.35
WT = 0.20
BL, BH = 0.60, 0.25
DERZ = 0.012  # görünür derz (stüdyo mesafesinde okunsun diye)
SIRA = 10  # (FH - KIRIS_D) / BH


def _p(c, s, tur, **kw):
    d = dict(c=tuple(c), s=tuple(s), tur=tur, kat=kw.get('kat', 0), sira=kw.get('sira', 0),
             n=tuple(kw.get('n', (0, 0, 0))), zaman=kw.get('zaman', 0.0), yuz=kw.get('yuz', ''))
    return d


def bolmeler():
    """Dış cephe bölmeleri: (yüz, eksen, sabit koordinat, a0, a1, normal)."""
    out = []
    for y, n in ((YS[0], (0, -1, 0)), (YS[-1], (0, 1, 0))):
        for xa, xb in zip(XS[:-1], XS[1:]):
            out.append(('on' if y < 0 else 'arka', 'X', y, xa + COL / 2, xb - COL / 2, n))
    for x, n in ((XS[0], (-1, 0, 0)), (XS[-1], (1, 0, 0))):
        for ya, yb in zip(YS[:-1], YS[1:]):
            out.append(('sol' if x < 0 else 'sag', 'Y', x, ya + COL / 2, yb - COL / 2, n))
    return out


def acikliklar(yuz, kat, a0, a1):
    """Bölmedeki boşluklar: [(u0, u1, sira0, sira1, tur)] — sira1 dahil değil; lento sira1'de."""
    m = (a0 + a1) / 2
    if yuz in ('on', 'arka'):
        if yuz == 'on' and kat == 0 and abs(m) < 0.5:
            return [(m - 0.6, m + 0.6, 0, 9, 'kapi')]
        return [(m - 0.75, m + 0.75, 4, 9, 'pencere')]
    return [(m - 0.6, m + 0.6, 4, 9, 'pencere')]


def uret(kat_sayisi=KAT, cati=True):
    P = []
    toplam = kat_sayisi + (1 if cati else 0)
    # temel
    P.append(_p((0, 0, -0.2), (XS[-1] - XS[0] + 0.9, YS[-1] - YS[0] + 0.9, 0.4), 'temel', zaman=0.0))
    for kat in range(kat_sayisi):
        z0 = kat * FH
        tk = kat / toplam  # bu katın yapım başlangıcı
        dt = 1.0 / toplam
        for x in XS:
            for y in YS:
                P.append(_p((x, y, z0 + FH / 2), (COL, COL, FH), 'kolon', kat=kat, zaman=tk + 0.02 * dt))
        # kirişler (çevre) + döşeme
        zk = z0 + FH - KIRIS_D / 2
        for y in YS:
            P.append(_p((0, y, zk), (XS[-1] - XS[0], KIRIS_W, KIRIS_D), 'kiris', kat=kat, zaman=tk + 0.12 * dt))
        for x in XS:
            P.append(_p((x, 0, zk), (KIRIS_W, YS[-1] - YS[0], KIRIS_D), 'kiris', kat=kat, zaman=tk + 0.12 * dt))
        P.append(_p((0, 0, z0 + FH - SLAB / 2), (XS[-1] - XS[0] + 0.5, YS[-1] - YS[0] + 0.5, SLAB), 'doseme', kat=kat, zaman=tk + 0.18 * dt))
        # duvarlar
        for (yuz, ax, k, a0, a1, n) in bolmeler():
            acik = acikliklar(yuz, kat, a0, a1)
            for sira in range(SIRA):
                z = z0 + (sira + 0.5) * BH
                ts = tk + (0.25 + 0.55 * sira / SIRA) * dt
                # bu sıradaki dolu aralıklar
                dolu = [(a0, a1)]
                for (u0, u1, s0, s1, _) in acik:
                    if s0 <= sira < s1 or (sira == s1 and True):
                        w0, w1 = (u0, u1) if sira < s1 else (u0 - 0.25, u1 + 0.25)  # lento sırası: lento boyu kadar boş
                        yeni = []
                        for (p0, p1) in dolu:
                            if p1 <= w0 or p0 >= w1:
                                yeni.append((p0, p1))
                                continue
                            if p0 < w0:
                                yeni.append((p0, w0))
                            if p1 > w1:
                                yeni.append((w1, p1))
                        dolu = yeni
                kay = 0.0 if sira % 2 == 0 else BL / 2
                for (p0, p1) in dolu:
                    u = a0 - kay
                    while u < p1 - 1e-6:
                        b0, b1 = max(u, p0), min(u + BL, p1)
                        if b1 - b0 > 0.02:
                            uc, ul = (b0 + b1) / 2, (b1 - b0) - DERZ
                            if ax == 'X':
                                c, s = (uc, k, z), (ul, WT, BH - DERZ)
                            else:
                                c, s = (k, uc, z), (WT, ul, BH - DERZ)
                            zb = ts + 0.02 * dt * (uc - a0) / max(0.1, a1 - a0)
                            P.append(_p(c, s, 'blok', kat=kat, sira=sira, n=n, zaman=zb, yuz=yuz))
                            # derz arkası harç (yalnız blok arkasında; boşlukları kapatmaz)
                            hs = (ul + DERZ, WT * 0.6, BH) if ax == 'X' else (WT * 0.6, ul + DERZ, BH)
                            P.append(_p(c, hs, 'harc', kat=kat, sira=sira, n=n, zaman=zb, yuz=yuz))
                        u += BL
            # lento, denizlik, doğrama, cam
            for (u0, u1, s0, s1, tur) in acik:
                um = (u0 + u1) / 2
                zl = z0 + (s1 + 0.5) * BH
                ll = (u1 - u0) + 0.5
                c, s = ((um, k, zl), (ll - DERZ, WT, BH - DERZ)) if ax == 'X' else ((k, um, zl), (WT, ll - DERZ, BH - DERZ))
                P.append(_p(c, s, 'lento', kat=kat, n=n, zaman=tk + 0.8 * dt, yuz=yuz))
                hs = (ll + DERZ, WT * 0.6, BH) if ax == 'X' else (WT * 0.6, ll + DERZ, BH)
                P.append(_p(c, hs, 'harc', kat=kat, n=n, zaman=tk + 0.8 * dt, yuz=yuz))
                # söve: boşluğun iç yüzleri (sıva) — derz/köşe boşluklarını kapatır
                zb0, zt0 = z0 + s0 * BH, z0 + s1 * BH
                w0 = u1 - u0
                um0 = (u0 + u1) / 2
                for (du, dz, sw, sh) in ((0, zt0 - 0.01, w0, 0.02), (0, zb0 + 0.01, w0, 0.02), (-w0 / 2 + 0.01, (zb0 + zt0) / 2, 0.02, zt0 - zb0),
                                         (w0 / 2 - 0.01, (zb0 + zt0) / 2, 0.02, zt0 - zb0)):
                    if ax == 'X':
                        P.append(_p((um0 + du, k, dz), (sw, WT - 0.01, sh), 'sove', kat=kat, n=n, zaman=tk + 0.82 * dt, yuz=yuz))
                    else:
                        P.append(_p((k, um0 + du, dz), (WT - 0.01, sw, sh), 'sove', kat=kat, n=n, zaman=tk + 0.82 * dt, yuz=yuz))
                zb, zt = z0 + s0 * BH, z0 + s1 * BH
                hh = zt - zb
                zm = (zb + zt) / 2
                nn = Vector(n)
                dis = nn * (WT / 2 - 0.05)  # doğrama dış yüzden 5 cm içeride
                cc = (Vector((um, k, zm)) if ax == 'X' else Vector((k, um, zm))) + dis
                w = u1 - u0
                t = 0.06
                if tur == 'pencere':
                    db = (Vector((um, k, zb - 0.025)) if ax == 'X' else Vector((k, um, zb - 0.025))) + nn * (WT / 2 + 0.02)
                    ds = (w + 0.1, WT * 0.5 + 0.04, 0.05) if ax == 'X' else (WT * 0.5 + 0.04, w + 0.1, 0.05)
                    P.append(_p(db, ds, 'denizlik', kat=kat, n=n, zaman=tk + 0.85 * dt))
                # profiller uç uca (köşede çakışmasın: aynı düzlemde üst üste yüz siyah görünür)
                cer = [(0, hh / 2 - t / 2, w, t), (0, -hh / 2 + t / 2, w, t), (-w / 2 + t / 2, 0, t, hh - 2 * t - 0.002), (w / 2 - t / 2, 0, t, hh - 2 * t - 0.002)]
                if tur == 'pencere':
                    cer.append((0, 0, t * 0.8, hh - 2 * t - 0.002))
                for (du, dz, bw, bh) in cer:
                    if ax == 'X':
                        P.append(_p(cc + Vector((du, 0, dz)), (bw, 0.07, bh), 'dograma', kat=kat, n=n, zaman=tk + 0.9 * dt))
                    else:
                        P.append(_p(cc + Vector((0, du, dz)), (0.07, bw, bh), 'dograma', kat=kat, n=n, zaman=tk + 0.9 * dt))
                gs = (w - 2 * t + 0.01, 0.012, hh - 2 * t + 0.01) if ax == 'X' else (0.012, w - 2 * t + 0.01, hh - 2 * t + 0.01)
                P.append(_p(cc, gs, 'cam' if tur == 'pencere' else 'kapi', kat=kat, n=n, zaman=tk + 0.92 * dt, yuz=yuz))
    if cati:
        z0 = kat_sayisi * FH
        tk = kat_sayisi / toplam
        dt = 1.0 / toplam
        # parapet: 3 sıra blok, döşeme kenarında
        for (yuz, ax, k, a0, a1, n) in bolmeler():
            for sira in range(3):
                z = z0 + (sira + 0.5) * BH
                kay = 0.0 if sira % 2 == 0 else BL / 2
                u = a0 - COL / 2 - kay
                while u < a1 + COL / 2 - 1e-6:
                    b0, b1 = max(u, a0 - COL / 2), min(u + BL, a1 + COL / 2)
                    if b1 - b0 > 0.02:
                        uc, ul = (b0 + b1) / 2, (b1 - b0) - DERZ
                        c, s = ((uc, k, z), (ul, WT, BH - DERZ)) if ax == 'X' else ((k, uc, z), (WT, ul, BH - DERZ))
                        P.append(_p(c, s, 'blok', kat=kat_sayisi, sira=sira, n=n, zaman=tk + (0.1 + 0.2 * sira) * dt, yuz=yuz))
                    u += BL
        # çatı panelleri: 60 cm şeritler, y boyunca
        x = XS[0] + WT / 2 + 0.01
        i = 0
        while x < XS[-1] - WT / 2 - 0.05:
            w = min(0.6, XS[-1] - WT / 2 - x) - 0.008
            # iki açıklık (ara aks y=0'da): her panel ≈ 4,4 m, kartta yazan "6 m'ye kadar" ile uyumlu
            for ya, yb in ((YS[0] + WT / 2, YS[1] - 0.01), (YS[1] + 0.01, YS[-1] - WT / 2)):
                P.append(_p((x + w / 2, (ya + yb) / 2, z0 + 0.1), (w, yb - ya, 0.2), 'panel', kat=kat_sayisi,
                            zaman=tk + (0.7 + 0.25 * i / 20) * dt))
            x += 0.6
            i += 1
    return P


def malzemeler(aksam=False):
    def pbr(name, hexcol, rough=0.7, metal=0.0, emis=None, es=0.0, noise=0.0):
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        nt = m.node_tree
        b = nt.nodes['Principled BSDF']
        c = kit.srgb(hexcol)
        b.inputs['Base Color'].default_value = c
        b.inputs['Roughness'].default_value = rough
        b.inputs['Metallic'].default_value = metal
        if emis:
            b.inputs['Emission Color'].default_value = kit.srgb(emis)
            b.inputs['Emission Strength'].default_value = es
        if noise:
            tc = nt.nodes.new('ShaderNodeTexCoord')
            nz = nt.nodes.new('ShaderNodeTexNoise')
            nz.inputs['Scale'].default_value = 3.0
            nz.inputs['Detail'].default_value = 8.0
            nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
            mx = nt.nodes.new('ShaderNodeMix')
            mx.data_type = 'RGBA'
            mx.blend_type = 'MULTIPLY'
            mx.inputs['Factor'].default_value = noise
            mx.inputs['A'].default_value = c
            nt.links.new(nz.outputs['Color'], mx.inputs['B'])
            nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
        return m
    aac = kit.aac_material('Gazbeton', bump=0.5, tex_size=0.24)
    beton = pbr('Beton', '#a39f97', 0.82, noise=0.22)
    return {
        'blok': aac, 'lento': aac, 'panel': aac,
        'harc': pbr('Harc', '#6f6b65', 0.95),
        'temel': beton, 'kolon': beton, 'kiris': beton, 'doseme': beton,
        'denizlik': pbr('Denizlik', '#d9d6cf', 0.5),
        'sove': pbr('Sove', '#e9e5de', 0.85),
        'dograma': pbr('Dograma', '#f3f2ee', 0.4),
        'cam': pbr('Cam', '#141b21', 0.02, 0.0, '#ffb978' if aksam else None, 22.0 if aksam else 0.0),
        'kapi': pbr('Kapi', '#5a4636', 0.6),
    }


def kur(P, mats, donustur=None, ad='Bina'):
    """Parçaları türe göre toplu ağ olarak kur. donustur(p) → (c, s, rot) ya da None (gizle)."""
    gruplar = {}
    for p in P:
        r = donustur(p) if donustur else (p['c'], p['s'], (0, 0, 0))
        if r is None:
            continue
        gruplar.setdefault(p['tur'], []).append(r)
    obs = {}
    for tur, lst in gruplar.items():
        obs[tur] = kit.toplu_mesh(f'{ad}_{tur}', kit.sablon('kup'), [x[0] for x in lst], [x[1] for x in lst],
                                  [x[2] for x in lst], mats[tur])
    return obs


def kenarlar(P, kalin=0.03, filtre=None, ilerleme=None):
    """Kutuların 12 kenarı → ince çubuk listesi (kalem çizimi için). ilerleme(p) 0..1: çizgi boyu."""
    mer, boy = [], []
    for p in P:
        if filtre and not filtre(p):
            continue
        k = ilerleme(p) if ilerleme else 1.0
        if k <= 0:
            continue
        (cx, cy, cz), (sx, sy, sz) = p['c'], p['s']
        for ax in range(3):
            o = [i for i in range(3) if i != ax]
            for a in (-0.5, 0.5):
                for b in (-0.5, 0.5):
                    c = [cx, cy, cz]
                    c[o[0]] += a * (sx, sy, sz)[o[0]]
                    c[o[1]] += b * (sx, sy, sz)[o[1]]
                    L = (sx, sy, sz)[ax] * min(1.0, k)
                    c[ax] += -(sx, sy, sz)[ax] / 2 + L / 2
                    s = [kalin, kalin, kalin]
                    s[ax] = L + kalin
                    mer.append(tuple(c))
                    boy.append(tuple(s))
    return mer, boy


def merkez():
    return Vector((0, 0, (KAT * FH) / 2))
