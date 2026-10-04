"""
Perde 1 — "Hayalden yuvaya" (ana giriş). Tek kamera dili (C: göz hizası, sokaktan), kaynak kareler.

Kipler (her biri bir kare dizisi üretir; son birleştirme tools/s0_birlestir.py ile yapılır):
  egim  : bej kâğıt, el çizimi (Freestyle). Kare 0 tepeden vaziyet planı; kamera C'ye eğilirken
          bina zeminden yükselir. Son kare = eskiz.
  dolum : siyah zemin; karkas beyaz, duvarlar ışıyan tel kafes; gazbeton bloklar sıra sıra yerine
          iner (nizami), lento, doğrama, cam, çatı paneli.
  sokak : fotogerçekçi gündüz; geçen araba, bisikletli (eller gidonda), yayalar, Ege Gazbeton tırı.
  plaka : aynı kadraj, güneş alçalır (gün ilerler); son iki kare: akşam ışıksız / ışıklı.

Etiket yok (kural): çapa noktaları <kip>/meta.json'a ekran koordinatı olarak yazılır.

Kullanım: python s0_hayal.py --kip egim|dolum|sokak|plaka --variant d|m --out DIR [--frames all|0,5]
"""
import argparse
import json
import math
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
import stil_r as R  # noqa: E402
import stil_r3 as T  # noqa: E402
import stil_r6 as K  # noqa: E402
import stil_r7 as G  # noqa: E402
import stil_r8 as E  # noqa: E402
import bina_detay as B  # noqa: E402
import sokak as S  # noqa: E402
import insan as I  # noqa: E402

KARE = {'egim': 38, 'dolum': 28, 'sokak': 36, 'plaka': 8}
RES = {'d': (1600, 900), 'm': (768, 1366)}
LENS = {'d': 24.0, 'm': 30.0}
C_HEDEF = Vector((-0.5, -4.0, 4.6))
C_YON = Vector((0.62, -1.0, 0.02)).normalized()
C_UZAK = 24.0
UST_HEDEF = Vector((0.0, -5.0, 0.0))
UST_UZAK = {'d': 40.0, 'm': 46.0}
YB = B.YS[0] - B.WT / 2 - 0.05  # bina ön yüzü
Y0 = G.Y_SOKAK  # kaldırım başlangıcı (bahçe duvarı)
# gün ilerler: (güneş yüksekliği, güneş yönü, gök gücü, pozlama)
PLAKA = [(34, 200, 0.20, -0.35), (24, 215, 0.20, -0.30), (15, 228, 0.22, -0.15), (8, 238, 0.25, 0.05),
         (3, 245, 0.30, 0.35), (0.5, 250, 0.38, 0.8), (-2, 250, 0.5, 1.6), (-2, 250, 0.5, 1.6)]


def kamera(variant, u=1.0):
    """u=0 tepeden plan, u=1 göz hizası C. Ara değerlerde yön ve uzaklık yumuşak geçer."""
    w = kit.smoother(u)
    yon = Vector((0, -0.02, 1.0)).normalized().lerp(C_YON, w).normalized()
    hedef = UST_HEDEF.lerp(C_HEDEF, w)
    uzak = math.exp(kit.lerp(math.log(UST_UZAK[variant]), math.log(C_UZAK), w))
    cam = bpy.data.objects.get('Kamera')
    if cam is None:
        cam = kit.camera('Kamera', lens=LENS[variant], loc=hedef + yon * uzak, target=hedef, fstop=11, focus=uzak)
    cam.location = hedef + yon * uzak
    kit.aim(cam, hedef)
    cam.data.lens = LENS[variant]
    cam.data.dof.use_dof = False
    kit.kaydir(cam, variant, w)
    return cam


# ------------------------------------------------------------------ egim: kâğıt üstünde plan → eskiz
# Bina HİÇ yükselmez: tam boy kâğıt malzeme, çizgiler kalemle SIRAYLA çizilir (kullanıcı şikâyeti).
# Her karede üç render: S (çizgisiz kâğıt), E (yalnız çevre çizgileri), B (yalnız bina çizgileri). Bina çizgileri,
# kenar listesinin ekrana izdüşümünden kurulan "çizilmiş kısım" maskesiyle açılır: çıktı = S − dE − dB·M.
EGIM_N = 38  # plan: E00–E37 (8 kare/sn)
SAG_ON = (B.XS[-1], B.YS[0])  # kamerayla aynı yöndeki (sağ-ön) köşe: kalem ilk oraya gider
PLAN_KARE = 6  # E00–E05: üstten plan, bina yok (yalnız zemin çizgileri); E06'dan sonra bina çizilir
CU_ANAHTAR = [(0, 0.0), (5, 0.18), (13, 0.80), (21, 0.95), (37, 1.0)]  # kamera eğimi (kare, 0..1)
ZEMIN_Z = 0.06


def _cu(f):
    k = CU_ANAHTAR
    if f <= k[0][0]:
        return k[0][1]
    for (f0, v0), (f1, v1) in zip(k, k[1:]):
        if f <= f1:
            return kit.lerp(v0, v1, kit.smoother(kit.seg(f, f0, f1)))
    return k[-1][1]


def egim_cizelge(P):
    """Çizilecek parçaların kalem sırası: [(c, s, t0, süre)] — t0/süre E kare cinsinden.
    Dikmeler tek kalemle SIRALI (sağ-ön köşe önce), sonra kat hizaları, pencere/kapı kutuları, çatı."""
    out = []
    kol = sorted({(p['c'][0], p['c'][1]) for p in P if p['tur'] == 'kolon'},
                 key=lambda xy: (xy[0] - SAG_ON[0]) ** 2 + (xy[1] - SAG_ON[1]) ** 2)
    slot = {xy: i for i, xy in enumerate(kol)}
    kir = sorted((p for p in P if p['tur'] in ('kiris', 'doseme')),
                 key=lambda p: (p['kat'], p['tur'] != 'doseme', p['c'][1], p['c'][0]))
    kir_i = {id(p): i for i, p in enumerate(kir)}
    pen = [p for p in P if p['tur'] in ('lento', 'denizlik', 'dograma', 'kapi')]

    def bay(p):
        n = p['n']
        return (p['kat'], tuple(round(x) for x in n), round((p['c'][0] if abs(n[1]) > 0.5 else p['c'][1]) / 1.5))
    gruplar = sorted({bay(p) for p in pen}, key=lambda g: (g[0], g[1] != (0, -1, 0), g[1], g[2]))
    gi = {g: i for i, g in enumerate(gruplar)}
    panel = [p for p in P if p['tur'] == 'panel']
    panel_i = {id(p): i for i, p in enumerate(sorted(panel, key=lambda p: (p['c'][0], p['c'][1])))}
    for p in P:
        t = p['tur']
        if t == 'kolon':
            t0, d = 6.2 + slot[(p['c'][0], p['c'][1])] * 0.62 + p['kat'] * 0.2, 0.22
        elif t in ('kiris', 'doseme'):
            t0, d = 11.0 + kir_i[id(p)] * (6.5 / max(1, len(kir))), 0.7
        elif t in ('lento', 'denizlik', 'dograma', 'kapi'):
            ek = {'lento': 0.0, 'denizlik': 0.12, 'dograma': 0.18, 'kapi': 0.15}[t]
            t0, d = 14.0 + gi[bay(p)] * (11.5 / max(1, len(gruplar))) + ek, 0.3
        elif t == 'panel':
            t0, d = 26.0 + panel_i[id(p)] * (3.5 / max(1, len(panel))), 0.3
        else:
            t0, d = 30.0, 0.3
        out.append((p['c'], p['s'], t0, d))
    return out


def kutu_kenarlari(c, s, t0, d):
    """Eksen hizalı kutunun 12 kenarı: [(p0, p1, t0, süre)]; dikmeler alttan üste, diğerleri soldan sağa."""
    cx, cy, cz = c
    hx, hy, hz = s[0] / 2, s[1] / 2, s[2] / 2
    k = []
    for ax in range(3):
        o = [i for i in range(3) if i != ax]
        for a in (-1, 1):
            for b in (-1, 1):
                p0 = [cx, cy, cz]
                h = (hx, hy, hz)
                p0[o[0]] += a * h[o[0]]
                p0[o[1]] += b * h[o[1]]
                p1 = list(p0)
                p0[ax] -= h[ax]
                p1[ax] += h[ax]
                if ax != 2 and (p0[0], p0[1]) > (p1[0], p1[1]):
                    p0, p1 = p1, p0
                if max(p0[2], p1[2]) <= ZEMIN_Z:  # zemin çizgileri plandan beri çizili
                    k.append((p0, p1, -5.0, 1.0))
                else:
                    k.append((p0, p1, t0, d))
    return k


def kip_egim(sc, variant, frames):
    import numpy as np
    from PIL import Image, ImageDraw
    P, mats = T.bina_hazir()
    kagit = E.duz_malzeme('#ebe3d5')
    CIZ = ('harc', 'cam', 'blok', 'sove', 'temel')
    Pc = [p for p in P if p['tur'] not in CIZ]
    bina = B.kur(P, {k: kagit for k in mats}, lambda p: None if p['tur'] in CIZ else (p['c'], p['s'], (0, 0, 0)))
    duvar_s = (B.XS[-1] - B.XS[0] - 0.02, B.YS[-1] - B.YS[0] - 0.02, B.KAT * B.FH - 0.1)
    duvar = kit.box('DuvarKutle', duvar_s, (0, 0, B.KAT * B.FH / 2), kagit)
    bina_obs = list(bina.values()) + [duvar]
    koleksiyon = bpy.data.collections.new('Bina')
    sc.collection.children.link(koleksiyon)
    for o in bina_obs:
        koleksiyon.objects.link(o)
    # kenar listesi (bir kez): parçalar + duvar kütlesi (kat hizalarıyla birlikte çizilir)
    kenar = []
    for (c, s, t0, d) in egim_cizelge(Pc) + [((0, 0, B.KAT * B.FH / 2), duvar_s, 16.0, 0.8)]:
        kenar += kutu_kenarlari(c, s, t0, d)
    K0 = np.array([e[0] for e in kenar], np.float64)
    K1 = np.array([e[1] for e in kenar], np.float64)
    KT0 = np.array([e[2] for e in kenar], np.float64)
    KD = np.array([e[3] for e in kenar], np.float64)

    # vaziyet: yol, bordür, kaldırım, bahçe duvarı, giriş yolu, ağaç taçları, lavanta, komşu ev izleri
    def kutu(ad, s, c):
        return kit.box(ad, s, c, kagit)
    kutu('GirisYolu', (1.6, abs(Y0 - YB), 0.12), (0, (YB + Y0) / 2, 0.06))
    for s in (-1, 1):
        kutu('BahceDuvar', (8.0, 0.2, 0.55), (s * 4.9, Y0 + 0.15, 0.275))
    kutu('Kaldirim', (90, 3.4, 0.15), (0, Y0 - 1.7, 0.075))
    kutu('Asfalt', (90, 7.4, 0.04), (0, Y0 - 7.2, 0.02))
    kutu('KarsiKaldirim', (90, 3.4, 0.15), (0, Y0 - 12.7, 0.075))
    for i in range(-8, 8):
        kutu('Serit', (2.8, 0.14, 0.05), (i * 6.0, Y0 - 7.2, 0.05))
    rnd = random.Random(4)
    for (x, y, r) in ((-6.8, YB - 2.2, 2.2), (7.0, YB - 2.0, 2.0), (-17, Y0 - 2.6, 2.4), (-9.5, Y0 - 2.6, 2.2),
                      (20, Y0 - 2.6, 2.3), (-20, Y0 - 12.9, 2.3), (-30, Y0 - 12.9, 2.1)):
        bpy.ops.mesh.primitive_cylinder_add(vertices=28, radius=r, depth=0.2, location=(x, y, 0.1 + rnd.random() * 0.05))
        bpy.context.active_object.data.materials.append(kagit)
    for (x, y, r) in ((-1.3, YB - 0.9, 0.4), (1.3, YB - 0.9, 0.4), (-7.6, YB - 1.1, 0.5), (7.6, YB - 1.1, 0.5)):
        bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=r, depth=0.12, location=(x, y, 0.06))
        bpy.context.active_object.data.materials.append(kagit)
    # tepeden bakış için düz ayak izi (dikey kenar yok: Freestyle uçları uzatınca çizgi saçmasın)
    iz = []
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 0, 0.02))
    o = bpy.context.active_object
    o.scale = (B.XS[-1] - B.XS[0], B.YS[-1] - B.YS[0], 1)
    o.data.materials.append(kagit)
    iz.append(o)
    for x in B.XS:
        for y in B.YS:
            bpy.ops.mesh.primitive_plane_add(size=B.COL, location=(x, y, 0.03))
            bpy.context.active_object.data.materials.append(kagit)
            iz.append(bpy.context.active_object)
    # komşu evler yalnız İZ: sabit alçak (yükselmez)
    for (x, y, w, d, k) in ((-24, -1, 9, 8, 2), (23, -1, 8, 9, 3), (-8, 22, 11, 8, 2), (12, 21, 8, 8, 2),
                            (-28, 20, 8, 8, 3), (32, 18, 9, 8, 2)):
        kutu('KomsuIz', (w, d, 0.06), (x, y, 0.03))
    for ob in bpy.data.objects:
        if ob.type == 'LIGHT':
            ob.hide_render = True
    E.kagit_dunya(sc)
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
    ls.select_by_collection = True
    ls.collection = koleksiyon
    st = ls.linestyle
    st.color = (0.16, 0.15, 0.14)
    st.thickness = 1.3 if variant == 'd' else 1.1
    st.alpha = 0.85
    gm = st.geometry_modifiers
    gm.new('Uzat', 'BACKBONE_STRETCHER').backbone_length = 9.0
    pn = gm.new('Titrek', 'PERLIN_NOISE_1D')
    pn.frequency, pn.amplitude, pn.octaves = 12.0, 1.6, 3
    tm = st.thickness_modifiers.new('Baski', 'ALONG_STROKE')
    tm.mapping = 'CURVE'
    tm.value_min, tm.value_max = 0.4, 1.4
    sc.compositing_node_group = None
    meta = {'_n': EGIM_N}
    durum = {'f': 0, 'plan': True, 'proj': None}

    def izdusum(pts):
        """Dünya noktaları (N,3) → piksel (N,2) ve derinlik işareti; kamera matrisi o karenin."""
        M = durum['proj']
        h4 = np.concatenate([pts, np.ones((len(pts), 1))], 1) @ M.T
        w = h4[:, 3]
        iyi = w > 0.05
        w = np.where(iyi, w, 1.0)
        W, H = durum['W'], durum['H']
        return np.stack([(h4[:, 0] / w * 0.5 + 0.5) * W, (1 - (h4[:, 1] / w * 0.5 + 0.5)) * H], 1), iyi

    def maske(f):
        """Kalemin o kareye kadar çizdiği kısım: kenar boyunca ilerleyen kalın şerit (+ uç aşımı payı)."""
        W, H = durum['W'], durum['H']
        r = np.clip((f - KT0) / KD, 0.0, 1.0)
        act = r > 0
        a = K0[act]
        b = a + (K1[act] - a) * r[act, None]
        pa, ia = izdusum(a)
        pb, ib = izdusum(b)
        tam = (r[act] >= 1.0)
        im = Image.new('L', (W, H), 0)
        dr = ImageDraw.Draw(im)
        gen = max(4, int(round(8 * W / 1600)))
        pay = 11 * W / 1600
        for q0, q1, i0, i1, t in zip(pa, pb, ia, ib, tam):
            if not (i0 and i1):
                continue
            v = q1 - q0
            n = float(np.hypot(*v))
            if n > 1e-6 and t:  # tamamlanmış çizgi: 'Uzat' uç aşımı da görünsün
                u = v / n
                q0, q1 = q0 - u * pay, q1 + u * pay
            dr.line([tuple(q0), tuple(q1)], fill=255, width=gen)
            dr.ellipse([q0[0] - gen / 2, q0[1] - gen / 2, q0[0] + gen / 2, q0[1] + gen / 2], fill=255)
            dr.ellipse([q1[0] - gen / 2, q1[1] - gen / 2, q1[0] + gen / 2, q1[1] + gen / 2], fill=255)
        return np.asarray(im, np.float32) / 255.0

    def kalem_ucu(f):
        """Kalemin o anki ucu (ekran 0..1) — sitedeki kalem sprite'ı için: etkin vuruşların en son başlayanı."""
        r = (f - KT0) / KD
        act = np.nonzero((r > 0) & (r < 1) & (KT0 > 0))[0]
        if len(act) == 0:
            return None
        i = act[np.argmax(KT0[act])]
        q, ok = izdusum((K0[i] + (K1[i] - K0[i]) * r[i])[None, :])
        if not ok[0]:
            return None
        return [round(float(q[0, 0]) / durum['W'], 4), round(float(q[0, 1]) / durum['H'], 4)]

    def kare(f):
        u = f / (EGIM_N - 1)
        cam = kamera(variant, _cu(f))
        plan = f < PLAN_KARE
        for o in bina_obs:
            o.hide_render = plan
        for o in iz:
            o.hide_render = not plan
        durum.update(f=f, plan=plan)
        sc.render.use_freestyle = True
        ls.select_by_collection = False
        dg = bpy.context.evaluated_depsgraph_get()
        rw, rh = sc.render.resolution_x, sc.render.resolution_y
        pct = sc.render.resolution_percentage / 100.0
        durum['W'], durum['H'] = int(rw * pct), int(rh * pct)
        P4 = cam.calc_matrix_camera(dg, x=rw, y=rh)
        V = cam.matrix_world.inverted()
        durum['proj'] = np.array(P4 @ V, np.float64)
        cpa = {'giris': (0.0, YB - 1.5, 0.2), 'bahce': (-4.6, YB - 2.6, 0.2), 'sokak': (-12.0, Y0 - 7.2, 0.1)}
        if u > 0.8:
            cpa = {'eskiz': (B.XS[0] + 0.5, YB, B.KAT * B.FH * 0.8)}
        pr = kit.project(cam, list(cpa.values()))
        meta[str(f)] = {k: p for k, p in zip(cpa, pr) if p}
        if plan:  # kalem plandan sağ-ön köşe kolonuna doğru yürür
            if f >= 3:
                q = kit.project(cam, [(SAG_ON[0], SAG_ON[1], 0.0)])[0]
                if q:
                    meta[str(f)]['pen'] = q
        else:
            k = kalem_ucu(f)
            if k:
                meta[str(f)]['pen'] = k

    def render(path):
        f = durum['f']
        if durum['plan']:
            ls.select_by_collection = False
            kit.render_to(path)
            return
        tmp = path[:-4]

        def oku(p):
            im = np.asarray(Image.open(p).convert('RGB'), np.float32)
            os.remove(p)
            return im
        sc.render.use_freestyle = False
        kit.render_to(tmp + '_s.png')
        sc.render.use_freestyle = True
        ls.select_by_collection = True
        ls.collection = koleksiyon
        ls.collection_negation = 'EXCLUSIVE'  # yalnız çevre çizgileri
        kit.render_to(tmp + '_e.png')
        ls.collection_negation = 'INCLUSIVE'  # yalnız bina çizgileri
        kit.render_to(tmp + '_b.png')
        S, Ec, Bc = oku(tmp + '_s.png'), oku(tmp + '_e.png'), oku(tmp + '_b.png')
        M = maske(f)[..., None]
        dE = np.clip(S - Ec, 0, 255)
        dB = np.clip(S - Bc, 0, 255)
        out = np.clip(S - dE - dB * M, 0, 255).astype(np.uint8)
        Image.fromarray(out).save(path, compress_level=3)
    return kare, meta, render


# ------------------------------------------------------------------ dolum: tel kafes → gazbeton
def kip_dolum(sc, variant, frames):
    P, mats = T.bina_hazir()
    beyaz = S.pbr('KarkasBeyaz', '#f2f1ee', 0.6)
    karkas = ('kolon', 'kiris', 'doseme')
    B.kur(P, {k: beyaz for k in mats}, lambda p: (p['c'], p['s'], (0, 0, 0)) if p['tur'] in karkas else None, ad='Karkas')
    duvar_tur = ('blok', 'lento', 'panel', 'harc', 'sove', 'denizlik', 'dograma', 'cam', 'kapi')
    W = [p for p in P if p['tur'] in duvar_tur]
    # zaman: duvar parçalarının kendi sırası (kat kat, sıra sıra), 0..1'e yayılır
    zs = sorted(set(round(p['zaman'], 5) for p in W))
    zmin, zmax = zs[0], zs[-1]
    for p in W:
        p['z01'] = (p['zaman'] - zmin) / (zmax - zmin)
    tel = S.pbr('TelKafes', '#ffffff', 0.4, 0.0, '#e9f2ff', 0.55)
    w = bpy.data.worlds.new('Siyah')
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.004, 0.005, 0.006, 1)
    for ob in bpy.data.objects:
        if ob.type == 'LIGHT' and ob.data.type == 'AREA':
            ob.data.energy *= 1.1
    kit.box('Zemin', (300, 300, 0.1), (0, 0, -0.05), kit.glossy_floor('KoyuZemin', '#0b0d0f', 0.22))
    kit.sinematik(bloom=0.3, esik=1.2, boyut=0.6)
    mats['cam'] = K.cam_gercek()
    kamera(variant, 1.0)
    D = 0.045  # bir parçanın inişi (zaman birimi)
    meta = {}
    state = {'obs': []}

    def kare(f):
        u = f / (KARE['dolum'] - 1)
        t = kit.lerp(-0.04, 1.0 + D, kit.seg(u, 0.06, 0.94))
        for o in state['obs']:
            bpy.data.objects.remove(o, do_unlink=True)
        yerli, bekleyen = [], []
        for p in W:
            k = kit.ease_out(kit.seg(t, p['z01'], p['z01'] + D), 3)
            (yerli if k > 0 else bekleyen).append((p, k))

        def don(pk):
            p, k = pk
            c = Vector(p['c']) + Vector((0, 0, 0.9 * (1 - k)))
            return (tuple(c), p['s'], (0, 0, 0))
        obs = list(B.kur([p for p, _ in yerli], mats, lambda p, _m={id(p): k for p, k in yerli}: don((p, _m[id(p)])),
                         ad='Duvar').values())
        if bekleyen:
            obs.append(T.cizgi_kur([p for p, _ in bekleyen], filtre=lambda p: p['tur'] in ('blok', 'lento', 'panel', 'dograma'),
                                   mat=tel, kalin=0.014))
        state['obs'] = obs
        cam = bpy.data.objects['Kamera']
        cpa = {}
        if 0.15 < u < 0.6:
            cpa['blok'] = (-3.0, B.YS[0] - 0.1, 1.2)
        if 0.35 < u < 0.85:
            cpa['lento'] = (B.XS[0] + 2.0, B.YS[0] - 0.1, B.FH + 2.4)
        if u > 0.8:
            cpa['panel'] = (1.5, 0.0, B.KAT * B.FH + 0.25)
            cpa['derz'] = (-4.5, B.YS[0] - 0.1, 0.75)
        pr = kit.project(cam, list(cpa.values()))
        meta[str(f)] = {k: p for k, p in zip(cpa, pr) if p}
    return kare, meta


# ------------------------------------------------------------------ sokak: gerçek gündüz, hareket
def sahne_gercek_bos(sc, aksam=False, isik=True):
    """stil_r7.sahne_gercek ile aynı dünya; hareketli öğeler hariç (onları kip kurar)."""
    K.bina_ve_odalar(sc, isik=aksam and isik)
    for ob in bpy.data.objects:
        if ob.type == 'LIGHT' and ob.data.type == 'AREA':
            ob.data.energy = 0
    S.yol(Y0)
    rnd = random.Random(3)
    for i, x in enumerate((-17.0, -9.5, 20.0)):
        S.agac((x, Y0 - 2.6, 0.15), boy=rnd.uniform(6.5, 8.0), seed=i)
    for i, x in enumerate((-20.0, -30.0)):
        S.agac((x, Y0 - 12.9, 0.15), boy=rnd.uniform(6.0, 7.5), seed=10 + i)
    for x in (-11.0, 4.5, 18.0):
        S.lamba((x, Y0 - 3.1, 0.15), yon=-math.pi / 2)
    S.araba((13.5, Y0 - 4.6, 0.05), 0.0, '#e9e9e6', 'Park2')
    K.temel_gizle()
    G.bahce()
    I.insan('yasli', 'otur', 0.0, dict(ust='#6f6a5f', alt='#3f3b36', sac='#c9c4bb', kol='uzun'),
            konum=(-4.4, YB - 1.42, -0.14), yon=0.0, ad='Bankta')
    G.arazi()
    G.komsular()


def ege_tiri():
    import stil_r5 as T5
    once = set(bpy.data.objects)
    T5.tir()
    e = bpy.data.objects.new('EgeTir', None)
    kit.link(e)
    for o in bpy.data.objects:
        if o not in once and o is not e and o.parent is None:
            o.parent = e
    logo = os.environ.get('EGE_LOGO')  # gerçek logo dosyası verilirse kabin kapılarına çıkartma
    if logo and os.path.exists(logo):
        img = bpy.data.images.load(logo)
        m = bpy.data.materials.new('TirLogo')
        m.use_nodes = True
        nt = m.node_tree
        b = nt.nodes['Principled BSDF']
        tx = nt.nodes.new('ShaderNodeTexImage')
        tx.image = img
        nt.links.new(tx.outputs['Color'], b.inputs['Base Color'])
        nt.links.new(tx.outputs['Alpha'], b.inputs['Alpha'])
        oran = img.size[1] / max(1, img.size[0])
        for s in (-1, 1):
            bpy.ops.mesh.primitive_plane_add(size=1.0, location=(4.5, s * 1.262, 2.4), rotation=(math.pi / 2, 0, 0 if s < 0 else math.pi))
            pl = bpy.context.active_object
            pl.scale = (1.6, 1.6 * oran, 1)
            pl.data.materials.append(m)
            pl.parent = e
    return e


def kip_sokak(sc, variant, frames):
    sahne_gercek_bos(sc)
    G.dunya_gok(sc)
    S.araba((-6.5, Y0 - 4.6, 0.05), 0.0, '#8f1f1a', 'Park1')
    araba = S.araba((0, 0, 0.05), math.pi, '#24364f', 'Gecen')
    bis, _ = I.bisikletli((0, 0, 0.05), 0.0, '#c24a2c', dict(ust='#2e4a63', alt='#2b2d30', sac='#1d1712', ten='#c49274'))
    tir = ege_tiri()
    yayalar = []
    for i, (tip, g, x0, y, yon, hiz) in enumerate([
        ('kadin', dict(ust='#d9cbb4', alt='#2f3c4c', sac='#3b2a1d', ten='#d2a688'), -9.0, Y0 - 1.5, 0.0, 1.25),
        ('cocuk', dict(ust='#e0b23a', alt='#3a4a6a', sac='#2a1d14', ten='#d2a688'), -8.4, Y0 - 1.0, 0.0, 1.25),
        ('erkek', dict(ust='#5f6f5a', alt='#3a3530', sac='#2a2018', ten='#b98a6a', kol='uzun'), 9.5, Y0 - 2.1, math.pi, 1.35),
        ('yasli', dict(ust='#7a7468', alt='#4a4540', sac='#bdb8b0', kol='uzun'), 14.0, Y0 - 1.4, math.pi, 0.9),
    ]):
        ao, _ = I.insan(tip, 'yuru', 0.0, g, konum=(x0, y, 0.15), yon=yon + math.pi / 2, ad=f'Yaya{i}')
        yayalar.append((ao, tip, x0, 1 if yon == 0 else -1, hiz))
    bahce = []
    for i, (tip, g, x) in enumerate([('kadin', dict(ust='#e7dfd2', alt='#3b4a5c', sac='#2b1e15'), 0.2),
                                     ('kiz', dict(ust='#d97a5a', alt='#2f3c4c', sac='#2b1e15'), 0.75)]):
        ao, _ = I.insan(tip, 'yuru', 0.0, g, konum=(x, YB - 3.0, 0.16), yon=math.pi, ad=f'Bahce{i}')
        bahce.append((ao, tip, x))
    kamera(variant, 1.0)
    SURE = 8.0  # dizinin temsil ettiği saniye
    meta = {}

    def kare(f):
        u = f / (KARE['sokak'] - 1)
        sn = u * SURE
        araba.location = (kit.lerp(30, -34, kit.seg(u, 0.0, 0.5)), Y0 - 9.0, 0.05)
        araba.hide_render = not (0 < u < 0.5)
        for o in araba.children_recursive:
            o.hide_render = araba.hide_render
        bis.location = (kit.lerp(-26, 30, u), Y0 - 5.9, 0.05)
        tu = kit.seg(u, 0.36, 1.0)
        tir.location = (kit.lerp(46, -62, tu), Y0 - 8.95, 0.0)
        tir.rotation_euler[2] = math.pi
        for o in [tir] + list(tir.children_recursive):
            o.hide_render = not (0 < tu < 1)
        for ao, tip, x0, d, hiz in yayalar:
            yol = hiz * sn
            ao.location.x = x0 + d * yol
            I.yuru_kare(ao, tip, (yol / 1.35) % 1.0)
        for ao, tip, x in bahce:  # bahçe yolundan kapıya yürür
            yol = 0.95 * sn
            ao.location.y = YB - 3.0 + min(yol, 2.2)
            ao.location.x = x
            I.yuru_kare(ao, tip, (yol / 1.2) % 1.0)
        cam = bpy.data.objects['Kamera']
        cpa = {}
        if 0 < tu < 1:
            cpa['tir'] = tuple(tir.matrix_world @ Vector((-4.0, 0, 3.4)))
        if u < 0.5:
            cpa['bisiklet'] = tuple(bis.matrix_world @ Vector((0, 0, 1.9)))
        pr = kit.project(cam, list(cpa.values()))
        meta[str(f)] = {k: p for k, p in zip(cpa, pr) if p and 0 <= p[0] <= 1}
    return kare, meta


# ------------------------------------------------------------------ plaka: gün ilerler
def kip_plaka(sc, variant, frames):
    son = max(frames) if frames else 0
    aksam = any(f >= len(PLAKA) - 2 for f in frames)
    if aksam and min(frames) < len(PLAKA) - 2:
        raise SystemExit('plaka: gündüz (0-5) ve akşam (6-7) kareleri ayrı çalıştırılmalı')
    isik = son == len(PLAKA) - 1
    sahne_gercek_bos(sc, aksam=aksam, isik=isik)
    S.araba((-6.5, Y0 - 4.6, 0.05), 0.0, '#8f1f1a', 'Park1')
    cam = kamera(variant, 1.0)
    meta = {}
    if aksam:
        G.dunya_gok(sc, elev=-2.0, rot=250.0, guc=0.5, bulut=False)
        bpy.data.objects['Gunes'].data.energy = 0.0
        sc.view_settings.exposure = 1.6
        if isik:
            for ob in list(bpy.data.objects):
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
        w, gunes = G.dunya_gok(sc)
    # pencere çokgenleri (ekran): akşam karelerinde pencereler tek tek yanar
    P = B.uret()
    pen = []
    for p in P:
        if p['tur'] != 'cam' or p['n'] == (0, 1, 0):
            continue
        c, s = Vector(p['c']), Vector(p['s'])
        n = Vector(p['n'])
        ax = Vector((1, 0, 0)) if abs(n.y) > 0.5 else Vector((0, 1, 0))
        wv = ax * (s.x if abs(n.y) > 0.5 else s.y) / 2
        hv = Vector((0, 0, s.z / 2))
        kose = [c - wv - hv, c + wv - hv, c + wv + hv, c - wv + hv]
        pr = kit.project(cam, kose)
        if all(pr):
            pen.append({'kat': p['kat'], 'x': round(c.x, 2), 'k': pr})
    meta['pencereler'] = pen

    def kare(f):
        if aksam:
            return
        el, rot, guc, poz = PLAKA[f]
        nt = sc.world.node_tree
        sky = nt.nodes['Sky Texture']
        sky.sun_elevation = math.radians(el)
        sky.sun_rotation = math.radians(rot)
        [n for n in nt.nodes if n.type == 'BACKGROUND'][0].inputs['Strength'].default_value = guc
        g = bpy.data.objects['Gunes']
        g.rotation_euler = (math.radians(90 - max(el, 1.5)), 0, math.radians(-32 - (rot - 200) * 0.6))
        sicak = kit.smooth(kit.seg(34 - el, 10, 32))
        g.data.color = (1.0, kit.lerp(0.95, 0.62, sicak), kit.lerp(0.88, 0.38, sicak))
        g.data.energy = 5.5 * kit.lerp(1.0, 0.35, kit.smooth(kit.seg(34 - el, 14, 34)))
        sc.view_settings.exposure = poz
    return kare, meta


KIPLER = {'egim': kip_egim, 'dolum': kip_dolum, 'sokak': kip_sokak, 'plaka': kip_plaka}
ORNEK = {'egim': 8, 'dolum': 28, 'sokak': 28, 'plaka': 48}


def main():
    kit.reset()
    w, h = RES[ARGS.variant]
    sc = kit.setup_render(w, h, samples=ARGS.samples or ORNEK[ARGS.kip], threshold=0.02, bounces=(6, 3, 3, 4))
    sc.cycles.transparent_max_bounces = 16
    sc.render.use_persistent_data = True
    if os.environ.get('EGE_PREVIEW'):
        sc.render.resolution_percentage = int(os.environ['EGE_PREVIEW'])
    R.studyo(sc)
    n = KARE[ARGS.kip]
    frames = list(range(n)) if ARGS.frames == 'all' else [int(x) for x in ARGS.frames.split(',')]
    out = os.path.join(ARGS.out, ARGS.kip)
    os.makedirs(out, exist_ok=True)
    sonuc = KIPLER[ARGS.kip](sc, ARGS.variant, frames)
    kare, meta = sonuc[0], sonuc[1]
    render = sonuc[2] if len(sonuc) > 2 else kit.render_to  # egim: çizgi maskesiyle çok geçişli render
    mp = os.path.join(out, 'meta.json')
    eski = json.load(open(mp)) if os.path.exists(mp) else {}
    eski.update(meta)
    for f in frames:
        path = os.path.join(out, f'{f:03d}.png')
        kare(f)
        eski.update(meta)
        kit.write_json(mp, eski)
        if ARGS.skip_existing and os.path.exists(path):
            continue
        t0 = time.time()
        render(path)
        print(f'KARE {ARGS.kip} {f} {time.time() - t0:.1f}s', flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--kip', required=True)
    ap.add_argument('--variant', default='d')
    ap.add_argument('--frames', default='all')
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=0)
    ap.add_argument('--skip-existing', action='store_true')
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
