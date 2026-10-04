"""
Perde 2 — "Bu evi iyi yapan ne?" Ürün turu (v2: 152 kare, 4 kare/sn, t=32..69,75).

Ev parlak, sıcak gri stüdyoda (maket dili). Röntgen = mavi-beyaz TEKNİK ÇİZİM (urun_gorunum). Kamera evin etrafında
bir tur atar; her durakta o ürünün parçaları gerçek malzemede kalır, kenarlarında lime çizgi/ışıltı belirir.
Her durak kendi görsel mekanizmasıyla anlatılır:
  duvar bloğu : dolgu duvar lime kenarlı, iç bölme duvarı da yanar, düz + geçmeli iki blok duvardan çıkar,
                20 cm duvar kesitinde turuncu ısı okları (içeriden dışarıya, duvarda incelir)
  lento       : lentolar kat kat yanar, pencere üstü köprü, yük okları iki yana oturma noktalarına yayılır,
                lento duvardan 10 cm kayar (aynı gözenekli doku), yerine oturur
  U blok      : parapet üst sırası; üç U blok havaya kalkar, kanalda çelik donatı, gri beton aşağıdan yukarı dolar
  tutkal      : bloklar neredeyse saydam; derz ağı lime çizgilerle (önce yatay, sonra düşey), tutkal torbası
  panel       : çatı şeritleri (piyano tuşu), iki açıklık
  EGEPOR      : çıplak kolon/kiriş turuncu ısı sızıntısı; beyaz levhalar kolonlara oturur; önce/sonra
Çıkış: altı ürün birlikte lime; kamera ön cephedeki tek bloğa dalar, ev beyaza erir, blok stüdyo zeminine iner
(f151 = Perde 3 f000: poz, ölçek ve ışık oraya yaklaştırılır).

Kipler: --kip ana (varsayılan: 152 kare), --kip once (f124–127 'önce' durumu: çıplak kolon/kiriş, turuncu ısı sızıntısı).
Kullanım: python s1_urun.py --variant d|m --out DIR [--frames all|0,40] [--samples N] [--kip ana|once]
Render içinde yazı/rakam yok; etiketler sitede (HTML/SVG).
"""
import argparse
import bisect
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
import stil_r2 as Q  # noqa: E402
import stil_r3 as T3  # noqa: E402
import stil_r4 as F  # noqa: E402
import bina_detay as B  # noqa: E402
import urun_gorunum as G  # noqa: E402
import urun_model as M  # noqa: E402

FRAMES = 152          # plan: 4 kare/sn × 38 sn (f151 = Perde 3 f000, burada render edilmez)
FPS = 4.0
T0 = 32.0             # perdenin mutlak başlangıç saniyesi
RES = {'d': (1600, 900), 'm': (768, 1366)}
LENS0 = {'d': 24.0, 'm': 30.0}   # Perde 1 C kamerası (s0_hayal) ile aynı
LENS = {'d': 35.0, 'm': 35.0}
UZAK = {'d': 34.0, 'm': 27.0}
S0_UZAK = 24.0
S0_HEDEF = Vector((-0.5, -4.0, 4.6))
HEDEF = Vector((0, 0, 4.6))
S0_G = 0.6            # f000: hayalet karışımı (plan: G≈0,6)
S0_SICAK = 0.15       # pencerelerde kalan sıcak ışık (Perde 1 çıkışı)
ZIRVE = B.KAT * B.FH  # çatı kotu
SON_POZ = {  # Perde 3 f000 (s0_video_blok.VARIANTS['end']): blok zeminde, 3/4 sağ-ön
    'd': dict(lens=50.0, dist=2.15, yaw=34.0, pitch=17.0, tx=-0.04, tz=0.12),
    'm': dict(lens=34.0, dist=1.22, yaw=30.0, pitch=24.0, tx=-0.02, tz=0.11),
}
ODAK_BLOK = (-3.0, 0)  # son dalış: ön cephe, zemin kat, x≈−3 civarı blok


def zaman(f):
    return T0 + f / FPS


# ---------------------------------------------------------------------------
#  Eğri yardımcıları (monoton kübik: duraklarda taşma yok)
# ---------------------------------------------------------------------------
def pchip(keys, x):
    xs = [k[0] for k in keys]
    ys = [k[1] for k in keys]
    if x <= xs[0]:
        return ys[0]
    if x >= xs[-1]:
        return ys[-1]
    n = len(xs)
    h = [xs[i + 1] - xs[i] for i in range(n - 1)]
    d = [(ys[i + 1] - ys[i]) / h[i] for i in range(n - 1)]
    m = [0.0] * n
    m[0], m[-1] = d[0], d[-1]
    for i in range(1, n - 1):
        if d[i - 1] * d[i] <= 0:
            m[i] = 0.0
        else:
            w1, w2 = 2 * h[i] + h[i - 1], h[i] + 2 * h[i - 1]
            m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i])
    i = bisect.bisect_right(xs, x) - 1
    t = (x - xs[i]) / h[i]
    h00 = 2 * t ** 3 - 3 * t ** 2 + 1
    h10 = t ** 3 - 2 * t ** 2 + t
    h01 = -2 * t ** 3 + 3 * t ** 2
    h11 = t ** 3 - t ** 2
    return h00 * ys[i] + h10 * h[i] * m[i] + h01 * ys[i + 1] + h11 * h[i] * m[i + 1]


def agirlik(T, a0, a1, b0, b1):
    """[a0,a1] yükselir, [b0,b1] söner (yumuşak)."""
    return kit.smooth(kit.seg(T, a0, a1)) * (1 - kit.smooth(kit.seg(T, b0, b1)))


def darbe(T, tc, w=0.3):
    """tc çevresinde üçgen darbe (0..1)."""
    return max(0.0, 1.0 - abs(T - tc) / w)


# ---------------------------------------------------------------------------
#  Kamera anahtarları: (T mutlak sn, azimut°, yükseklik°, uzaklık m (d), hedef)
#  Azimut: plan tablosu (az +32° → +380°); duraklarda yavaşlar, geçişlerde 12°/sn'yi geçmez.
# ---------------------------------------------------------------------------
UT = Vector((0.0, B.YS[-1] + 2.2, ZIRVE + 1.2))     # havadaki U blok kümesi (arka cephe parapetinin önü)
KESIT_C = Vector((7.4, 0.9, 2.2))                    # duvar kesiti parçası (sağ cephenin önünde)
KESIT_YUZ = KESIT_C.x + 0.6                          # kesit yüzü x'i (+x'e bakar)
PEN_C = Vector((B.XS[-1], 2.25, 5.375))              # öne çıkan lento (sağ cephe, 2. kat, ön pencere)
KOL_BIRLESIM = Vector((-2.0, B.YS[0], 2.75))        # kolon-kiriş birleşimi (önce/sonra)

CAM = [
    (32.0, 32.0, 1.0, 24.0, S0_HEDEF),
    (33.0, 33.0, 5.0, 27.5, Vector((-0.3, -2.8, 4.6))),
    (34.0, 34.5, 9.0, 30.5, Vector((-0.1, -1.2, 4.6))),
    (35.0, 36.5, 14.0, 34.0, HEDEF),
    (36.0, 40.0, 15.0, 32.0, Vector((2.0, 0.0, 4.3))),
    (37.0, 52.0, 14.0, 17.0, Vector((6.0, 0.8, 2.8))),
    (38.0, 62.0, 12.0, 10.5, Vector((7.0, 0.6, 1.9))),
    (39.0, 70.0, 11.0, 3.0, Vector((KESIT_YUZ, KESIT_C.y, KESIT_C.z))),
    (39.75, 71.0, 11.0, 3.2, Vector((KESIT_YUZ, KESIT_C.y, KESIT_C.z))),
    (40.5, 76.0, 12.0, 17.0, Vector((6.3, 0.5, 3.2))),
    (41.0, 92.0, 14.0, 27.0, Vector((6.0, 0.8, 4.2))),
    (42.0, 111.0, 12.0, 12.0, Vector((PEN_C.x, PEN_C.y, PEN_C.z - 0.3))),
    (43.0, 119.0, 10.0, 6.8, Vector((PEN_C.x, PEN_C.y, PEN_C.z - 0.2))),
    (44.0, 127.0, 10.0, 4.1, Vector((PEN_C.x, PEN_C.y - 0.2, PEN_C.z))),
    (45.0, 133.0, 12.0, 4.2, Vector((PEN_C.x, PEN_C.y - 0.2, PEN_C.z))),
    (46.0, 148.0, 30.0, 17.0, Vector((0.0, 3.0, ZIRVE - 0.5))),
    (47.0, 165.0, 52.0, 7.5, UT),
    (48.0, 177.0, 56.0, 3.1, UT),
    (49.0, 180.0, 56.0, 3.1, UT),
    (50.0, 182.0, 56.0, 3.4, UT),
    (51.0, 198.0, 38.0, 14.0, Vector((-3.0, 2.0, 6.0))),
    (52.0, 205.0, 22.0, 20.0, Vector((-5.0, 1.0, 4.2))),
    (53.0, 218.0, 16.0, 13.6, Vector((-5.5, 0.0, 3.2))),
    (54.0, 236.0, 14.0, 20.0, Vector((-3.0, 0.0, 4.2))),
    (55.0, 252.0, 12.0, 24.0, Vector((-1.0, 0.0, 5.5))),
    (56.0, 264.0, 33.0, 32.0, Vector((0.0, 0.0, 8.0))),
    (57.0, 276.0, 52.0, 30.0, Vector((0.0, 0.0, 9.0))),
    (58.0, 291.0, 63.0, 17.0, Vector((0.0, 0.0, 9.2))),
    (59.0, 301.0, 48.0, 33.0, Vector((0.0, 0.0, 7.5))),
    (60.0, 311.0, 44.0, 33.0, Vector((0.0, 0.0, 6.0))),
    (61.0, 318.0, 16.0, 29.0, Vector((-1.0, -2.0, 4.6))),
    (62.0, 330.0, 16.0, 18.7, Vector((-2.0, -3.0, 4.0))),
    (63.0, 342.0, 14.0, 10.2, KOL_BIRLESIM),
    (63.75, 349.0, 14.0, 11.0, KOL_BIRLESIM),
    (64.0, 356.0, 14.0, 24.0, Vector((0.0, -2.0, 4.6))),
    (65.0, 368.0, 14.0, 30.6, HEDEF),
    (66.0, 380.0, 15.0, 30.6, HEDEF),
    (70.0, 380.0, 15.0, 30.6, HEDEF),
]


def _kanal(j):
    return [(k[0], k[j]) for k in CAM]


def tur_pozu(Tz, v):
    """Dalış öncesi tur kamerası: (azimut, yükseklik, uzaklık, hedef, lens)."""
    az = pchip(_kanal(1), Tz)
    el = pchip(_kanal(2), Tz)
    dist = pchip(_kanal(3), Tz)
    h = Vector((pchip([(k[0], k[4].x) for k in CAM], Tz), pchip([(k[0], k[4].y) for k in CAM], Tz),
                pchip([(k[0], k[4].z) for k in CAM], Tz)))
    if v == 'm':  # dikey kadraj: uzak çekimlerde biraz daha yakın
        dist *= kit.lerp(UZAK['m'] / UZAK['d'], 1.0, 1 - kit.smooth(kit.seg(dist, 8.0, 22.0)))
    w = kit.smooth(kit.seg(Tz, 32.0, 35.0))
    lens = kit.lerp(LENS0[v], LENS[v], w)
    return az, el, dist, h, lens


def odak_konum(Tz, rest):
    """Odak bloğun merkezi: duvardan 45 cm öne kayar, sonra stüdyo zeminine iner."""
    k1 = kit.smoother(kit.seg(Tz, 67.9, 68.7))
    k2 = kit.smoother(kit.seg(Tz, 68.6, 69.65))
    z = kit.lerp(rest.z, 0.125, k2)
    return Vector((rest.x, rest.y - 0.45 * k1, z)), k1, k2


def kamera_pozu(Tz, v, rest):
    az, el, dist, h, lens = tur_pozu(Tz, v)
    loc = h + Vector((math.sin(math.radians(az)) * math.cos(math.radians(el)),
                      -math.cos(math.radians(az)) * math.cos(math.radians(el)), math.sin(math.radians(el)))) * dist
    d = kit.smoother(kit.seg(Tz, 67.0, 68.4))
    kayma = 1.0 - kit.smooth(kit.seg(Tz, 67.6, 69.6))
    if d > 0:
        bpos, _, _ = odak_konum(Tz, rest)
        s = SON_POZ[v]
        w2 = kit.smoother(kit.seg(Tz, 68.2, 69.75))
        yaw = kit.lerp(20.0, s['yaw'], w2)
        pit = kit.lerp(10.0, s['pitch'], w2)
        dd = kit.lerp(2.4, s['dist'], w2)
        hb = bpos + Vector((s['tx'] * w2, 0.0, (s['tz'] - 0.125) * w2))
        yon = Vector((math.sin(math.radians(yaw)) * math.cos(math.radians(pit)), -math.cos(math.radians(yaw)) * math.cos(math.radians(pit)),
                      math.sin(math.radians(pit))))
        lb = hb + yon * dd
        # uzaklık logaritmik (görünür büyütme eşit hızda), konum doğrusal değil: loc → lb
        r0 = (loc - h).length
        r1 = dd
        oran = math.exp(kit.lerp(math.log(max(r0, 1e-3)), math.log(r1), d))
        hedef_t = h.lerp(hb, d)
        yon_t = (loc - h).normalized().lerp(yon, d).normalized()
        loc = hedef_t + yon_t * oran
        h = hedef_t
        lens = kit.lerp(lens, s['lens'], kit.smoother(kit.seg(Tz, 67.5, 69.75)))
    return loc, h, lens, kayma


# ---------------------------------------------------------------------------
#  Sahne kurulumu
# ---------------------------------------------------------------------------
def egepor_parcalari():
    """Dış kolon ve kiriş önlerine 5 cm Egepor levha (kolon/kiriş kaplaması)."""
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


class Sahne:
    """Nesneler, malzemeler ve kare başına güncelleme."""

    def __init__(self, v, kip):
        self.v = v
        self.kip = kip
        self.ayar_tur = {'icblok': 'blok', 'harc': 'blok'}
        sc = bpy.context.scene
        self.sc = sc
        G.studyo(sc)
        P, mats = T3.bina_hazir()
        P = [p for p in P if p['tur'] != 'temel']
        self.mats = mats
        # --- Egepor malzemesi (beyaz levha)
        mats['egepor'] = bpy.data.materials.new('Egepor')
        mats['egepor'].use_nodes = True
        b = mats['egepor'].node_tree.nodes['Principled BSDF']
        b.inputs['Base Color'].default_value = kit.srgb('#f2efe7')
        b.inputs['Roughness'].default_value = 0.9
        mats['icblok'] = mats['blok']
        # --- öne çıkan parçalar duvardan ayrılır (blok + arkasındaki harç kutusu birlikte silinir)
        def sil(parca):
            nonlocal P
            P = [p for p in P if not (p is parca or (p['tur'] == 'harc' and all(abs(p['c'][i] - parca['c'][i]) < 1e-6 for i in range(3))))]
        kucuk = M.duvardan_blok_sec(P, 'sag', 0, 2, -1.0, 2)
        self.hero_rest = [Vector(p['c']) for p in kucuk]
        self.hero_s = [p['s'] for p in kucuk]
        for p in kucuk:
            sil(p)
        # odak blok (dalış): ön cephe, zemin kat, sira 3
        odak = min((p for p in P if p['tur'] == 'blok' and p['kat'] == 0 and p['yuz'] == 'on' and p['sira'] == 3),
                   key=lambda p: abs(p['c'][0] - ODAK_BLOK[0]))
        sil(odak)
        self.odak_rest = Vector(odak['c'])
        # öne çıkan lento (sağ cephe, 2. kat) ve bitişik duvar bloğu
        ln = min((p for p in P if p['tur'] == 'lento' and p['yuz'] == 'sag' and p['kat'] == 1 and p['c'][1] > 0),
                 key=lambda p: abs(p['c'][1] - PEN_C.y))
        sil(ln)
        self.lento_c, self.lento_s = Vector(ln['c']), ln['s']
        kom = min((p for p in P if p['tur'] == 'blok' and p['yuz'] == 'sag' and p['kat'] == 1 and p['sira'] == 9 and p['c'][1] > self.lento_c.y + 0.5),
                  key=lambda p: p['c'][1], default=None)
        if kom:
            sil(kom)
            self.kom_c, self.kom_s = Vector(kom['c']), kom['s']
        else:
            self.kom_c, self.kom_s = Vector(ln['c']) + Vector((0, 1.0, 0)), ln['s']
        # çatı hatılı: parapetin üst sırası U blok (kabuk)
        for p in P:
            if p['tur'] == 'blok' and p['kat'] == B.KAT and p['sira'] == 2:
                p['tur'] = 'ublok'
        mats['ublok'] = mats['blok']
        # --- panel şeritleri ayrı nesne
        panel_P = [p for p in P if p['tur'] == 'panel']
        P = [p for p in P if p['tur'] != 'panel']
        # --- türe göre teknik malzemeler
        turler = sorted(set(p['tur'] for p in P) | {'icblok'})
        self.gm = {}
        for t in turler:
            if t == 'harc':
                self.gm[t] = M.harc_cizgi_malzemesi(mats['harc'], 'T_harc')
            else:
                self.gm[t] = G.teknik_malzeme(mats[t], 'T_' + t, self.ayar_tur.get(t, t))
        self.gm['panel'] = G.teknik_malzeme(mats['panel'], 'T_panel', 'panel')
        ic = M.ic_duvar_parcalari()
        # --- ana ev
        self.obs = G.kur(P + ic, self.gm, ad='Ev')
        self.panel_obs = M.panel_seritleri(panel_P, self.gm['panel'])
        self.panel_x = [x for x, _ in self.panel_obs]
        # --- öne çıkan bloklar (aynı 'blok' malzemesi; duvarda oturan hâlleri kalıcı)
        self.heroes = []
        s0 = self.hero_s[0]
        h1 = G.kutu_nesne('HeroDuz', (0, 0, 0), s0, self.gm['blok'])
        h2 = M.gecmeli_blok_nesne('HeroGecmeli', self.gm['blok'], L=s0[1] + B.DERZ, H=s0[2] + B.DERZ, T=s0[0])
        h2.rotation_euler = (0, 0, math.pi / 2)  # uzunluk sağ cephe boyunca (y)
        self.heroes = [h1, h2]
        for ob, c in zip(self.heroes, self.hero_rest):
            ob.location = c
        # --- lento + bitişik blok (ayrı: kayma ve eşzamanlı lime)
        self.lento_ob = G.kutu_nesne('LentoOne', (0, 0, 0), self.lento_s, self.gm['lento'])
        self.lento_ob.location = self.lento_c
        self.gm_kom = G.teknik_malzeme(mats['blok'], 'T_bitisik', 'blok')
        self.kom_ob = G.kutu_nesne('BitisikBlok', (0, 0, 0), self.kom_s, self.gm_kom)
        self.kom_ob.location = self.kom_c
        # --- odak blok (geçmeli, 0,6×0,25×0,25)
        self.gm_odak = G.teknik_malzeme(mats['blok'], 'T_odak', 'blok')
        self.odak_ob = M.gecmeli_blok_nesne('OdakBlok', self.gm_odak, 0.6, 0.25, 0.25)
        self.odak_ob.location = self.odak_rest
        # --- U blok detayı
        az_m = tur_pozu(47.5, v)[0]
        gz = Vector((math.sin(math.radians(az_m)), -math.cos(math.radians(az_m)), 0))
        ub_n = {tuple(p['n']) for p in P if p['tur'] == 'ublok'}
        self.yuzn = max(ub_n, key=lambda n: Vector(n).dot(gz))
        xe = abs(self.yuzn[1]) > 0.5
        self.u_eksen = Vector((1, 0, 0)) if xe else Vector((0, 1, 0))
        yuz_k = (B.YS[0] if self.yuzn[1] < 0 else B.YS[-1]) if xe else (B.XS[0] if self.yuzn[0] < 0 else B.XS[-1])
        ut = (Vector((0, yuz_k, 0)) if xe else Vector((yuz_k, 0, 0))) + Vector(self.yuzn) * 2.2 + Vector((0, 0, ZIRVE + 1.2))
        self.ut = ut
        for i, k in enumerate(CAM):  # kamera anahtarlarında U blok hedefi gerçek konuma
            if k[4] is UT:
                CAM[i] = (k[0], k[1], k[2], k[3], ut)
        sahte = []
        for i in range(3):
            c = ut + self.u_eksen * (i - 1) * 0.6
            sz = (0.588, 0.25, 0.238) if xe else (0.25, 0.588, 0.238)
            sahte.append(dict(c=tuple(c), s=sz, tur='ublok', n=self.yuzn))
        kab, don, hat = M.u_blok_detay(sahte)
        self.u_kabuk = list(G.kur(kab, self.gm, ad='UDetay').values())
        self.celik = Q.pbr('Celik', M.STEEL, 0.32, 0.9)
        self.u_donati = M.silindirler('UDonati', don, self.celik)
        self.hatil_mat = mats['kolon']
        self.hatil_ob = kit.toplu_mesh('UHatil', kit.sablon('kup'), [h[0] for h in hat], [h[1] for h in hat], None, self.hatil_mat)
        self.hz0 = min(h[0][2] - h[1][2] / 2 for h in hat)
        self.u_parca_n = len(sahte)
        # parapetin üst sırası, yüzeyde yüzen kümeyle aynı yükseklik farkı (kalkış başlangıç ofseti)
        self.u_ofset = -(Vector(self.yuzn) * 2.2 + Vector((0, 0, ZIRVE + 1.2 - (ZIRVE + 0.625))))
        # --- kesit parçası + ısı okları
        kp = M.kesit_parcalari(KESIT_C)
        self.gm_kesit = G.teknik_malzeme(mats['blok'], 'T_kesit', 'blok')
        self.kesit_ob = G.cizgili_mesh('Kesit', [p['c'] for p in kp], [p['s'] for p in kp], self.gm_kesit)
        gu, ort, sol = M.isi_oklari(KESIT_C)
        self.ok_m = [M.ok_malzemesi('IsiGuclu', '#ff7a2e', 4.0), M.ok_malzemesi('IsiOrta', '#ff7a2e', 2.2),
                     M.ok_malzemesi('IsiSoluk', '#7fa9d6', 0.9)]
        self.isi_obs = M.oklar('IsiGuclu', gu, self.ok_m[0]) + M.oklar('IsiOrta', ort, self.ok_m[1]) + M.oklar('IsiSoluk', sol, self.ok_m[2])
        self.perde_ic = M.perde_malzemesi('PerdeIc', '#ffb070', 0.10, 1.0)
        self.perde_dis = M.perde_malzemesi('PerdeDis', '#9ec4ee', 0.10, 1.0)
        self.perdeler = []
        for ad, y, mm in (('PerdeIc', KESIT_C.y - 0.5, self.perde_ic), ('PerdeDis', KESIT_C.y + 0.5, self.perde_dis)):
            v_ = [(KESIT_C.x - 0.5, y, KESIT_C.z - 0.85), (KESIT_C.x + 0.9, y, KESIT_C.z - 0.85),
                  (KESIT_C.x + 0.9, y, KESIT_C.z + 0.85), (KESIT_C.x - 0.5, y, KESIT_C.z + 0.85)]
            ob = kit.mesh_object(ad, v_, [(0, 1, 2, 3)], mm)
            ob.visible_shadow = False
            self.perdeler.append(ob)
        # --- yük okları (lento): nötr mavi-gri
        self.yuk_m = M.ok_malzemesi('Yuk', '#355f93', 2.6)
        self.lento_n = Vector((1, 0, 0))
        ust, yay = M.yuk_oklari(self.lento_c, (1, 0, 0), self.lento_s[1] / 2)
        self.yuk_ust = M.oklar('YukUst', ust, self.yuk_m)
        self.yuk_yay = M.oklar('YukYay', yay, self.yuk_m)
        # --- tutkal torbası
        self.torba = M.torba('Torba', 1.0)
        # --- Egepor grupları (kolon kolon, soldan sağa)
        EP = egepor_parcalari()
        cam_sag = Vector((math.cos(math.radians(336)), math.sin(math.radians(336)), 0))

        def sira(p):
            return Vector(p['c']).dot(cam_sag)
        self.ep = M.egepor_gruplari(EP, sira, 6, lambda g: G.teknik_malzeme(mats['egepor'], f'T_egepor{g}', 'egepor'))
        self.ep_gm = [m for _, m, _ in self.ep]
        self.EP = EP
        # --- gölge vekili: hayalet kütle gölge ışınlarını katman katman geçmesin (hız); zemine tek yumuşak temas gölgesi düşer
        self.g_son = {}
        self.golge_m = bpy.data.materials.new('GolgeVekil')
        self.golge_m.use_nodes = True
        self.golge_b = self.golge_m.node_tree.nodes['Principled BSDF']
        self.golge_b.inputs['Base Color'].default_value = (0, 0, 0, 1)
        self.golge_ob = kit.box('GolgeVekil', (12.4, 9.4, 9.3), (0, 0, 4.65), self.golge_m)
        for a in ('visible_camera', 'visible_diffuse', 'visible_glossy', 'visible_transmission', 'visible_volume_scatter'):
            setattr(self.golge_ob, a, False)
        # --- zemin, kamera, sinema
        F.zemin(0.0)
        self.cam = kit.camera('Kamera', lens=LENS[v], loc=(0, -30, 8), target=HEDEF)
        self.cam.data.dof.use_dof = False
        kit.sinematik(bloom=0.28, esik=0.95, boyut=0.5)
        # her teknik malzeme (piksel ölçeği için)
        self.tum_mat = [m for m in self.gm.values()] + [self.gm_kom, self.gm_odak, self.gm_kesit] + self.ep_gm
        self.ana_turler = turler

    # ------------------------------------------------------------------ gölge
    def golge_ayarla(self, dal, g_taban, ev_gizli):
        """Yalnız gerçek (G<0,5) nesneler gölge düşürür; hayalet kütlenin zemin gölgesi tek vekil kutudan gelir.
        Hayalet katmanların her gölge ışınını onlarca saydam yüzeyden geçirmesi render süresinin ~%25'iydi."""
        gs = self.g_son
        for t, ob in self.obs.items():
            ob.visible_shadow = gs.get(t, g_taban) < 0.5 and not ev_gizli
        for ob in self.heroes + [self.lento_ob, self.kom_ob, self.odak_ob, self.kesit_ob]:
            ob.visible_shadow = True
        for ob in self.u_kabuk:
            ob.visible_shadow = gs.get('ublok', 1.0) < 0.5
        self.u_donati.visible_shadow = True
        self.hatil_ob.visible_shadow = True
        for _, ob in self.panel_obs:
            ob.visible_shadow = gs.get('panel', 1.0) < 0.5
        for ob, mm, _ in self.ep:
            ob.visible_shadow = mm.node_tree.nodes['G'].outputs[0].default_value < 0.5
        a = (0.30 + 0.30 * (1.0 - kit.seg(g_taban, 0.6, 1.0))) * (1.0 - kit.smooth(kit.seg(dal, 0.0, 0.9)))
        self.golge_b.inputs['Alpha'].default_value = a
        self.golge_ob.hide_render = a < 0.01

    # ------------------------------------------------------------------ kare
    def uygula(self, f):
        Tz = zaman(f)
        v = self.v
        sc = self.sc
        once = self.kip == 'once'
        gm = self.gm
        # ----- kamera
        loc, hedef, lens, kayma = kamera_pozu(Tz, v, self.odak_rest)
        cam = self.cam
        cam.location = loc
        kit.aim(cam, hedef)
        cam.data.lens = lens
        kit.kaydir(cam, v, kayma)
        G.piksel_olcegi(self.tum_mat, lens, RES[v][0])
        # ----- ağırlıklar
        w_duvar = agirlik(Tz, 35.7, 36.3, 41.0, 41.6)
        w_ic = agirlik(Tz, 36.9, 37.4, 38.7, 39.1)
        dip = agirlik(Tz, 38.9, 39.2, 39.8, 40.2)
        w_blok = w_duvar * (1 - 0.6 * w_ic - 0.88 * dip)
        w_lento = agirlik(Tz, 40.7, 41.3, 45.6, 46.2)
        w_ub = agirlik(Tz, 45.8, 46.3, 50.3, 50.9)
        w_harc = agirlik(Tz, 50.8, 51.1, 55.2, 55.6)
        w_panel = agirlik(Tz, 55.7, 56.2, 60.2, 60.8)
        w_son = agirlik(Tz, 65.7, 66.3, 99.0, 99.5)  # çıkış koro: hepsi lime
        dal = kit.smooth(kit.seg(Tz, 67.0, 68.5))  # ev kaybolur
        ev_gizli = dal >= 0.995
        tarama_bas, tarama_son = 33.0, 34.0
        taranmis = kit.smooth(kit.seg(Tz, tarama_bas, tarama_son))
        if Tz < tarama_bas:
            g_taban, gu_taban, tz = S0_G, S0_G, -99.0
        elif Tz < tarama_son:
            g_taban, gu_taban = 1.0, S0_G
            tz = 12.5 - 13.5 * kit.smooth(kit.seg(Tz, tarama_bas, tarama_son))
        else:
            g_taban, gu_taban, tz = 1.0, 1.0, -99.0
        # soluk (V) ve ısı
        solgun = agirlik(Tz, 60.9, 61.4, 64.0, 64.6) * 0.5
        isi = 1.0 if once else agirlik(Tz, 60.9, 61.4, 62.2, 63.3)
        sicak = S0_SICAK * (1 - kit.smooth(kit.seg(Tz, 32.0, 33.0)))
        herhangi = max(w_blok, w_lento, w_ub, w_harc, w_panel, w_son)
        g_diger = kit.lerp(g_taban, 1.0, herhangi)  # saf teknik çizim: gerçek gazbeton gölgelendiricisi hesaplanmaz (hız + temiz görünüm)

        def hizala(t, w, h, hz, hd=(0, 0, 1), g_ek=None, v_=None):
            g = g_diger if w < 0.001 else kit.lerp(g_diger, 0.0, w)
            if g_ek is not None:
                g = g_ek
            gu = g if Tz >= tarama_son else (gu_taban if w < 0.001 else g)
            self.g_son[t] = g
            G.ayarla(gm[t], g=g, gu=gu, tz=tz, v=(dal if v_ is None else max(dal, v_)), h=h, hz=hz, hd=hd)
        wallV = solgun
        # duvar bloğu: dalga alttan üste (36→37,2)
        hz_duvar = -1.0 + 13.0 * kit.seg(Tz, 36.0, 37.2)
        h_blok = (kit.lerp(6.0, 3.0, kit.smooth(kit.seg(Tz, 40.0, 41.0))) if Tz > 39.5 else 6.0) * w_blok
        tutkal_v = 0.28 * w_harc
        hizala('blok', w_blok, h_blok, hz_duvar, v_=max(wallV, tutkal_v))
        # lento: kat gecikmeli dalga
        hz_lento = -1.0 + 12.5 * kit.seg(Tz, 41.0, 42.1)
        hizala('lento', w_lento, 6.0 * w_lento, hz_lento, v_=wallV)
        # parapet U blok
        hizala('ublok', w_ub, 6.0 * w_ub, 99.0)
        # panel: şerit dalgası (x yönü)
        hz_panel = -6.5 + 13.0 * kit.seg(Tz, 56.0, 57.5)
        hizala('panel', w_panel, 6.0 * w_panel, hz_panel, hd=(1, 0, 0))
        # sove: lento durağında beyaz kontur
        w_sove = agirlik(Tz, 41.8, 42.2, 45.2, 45.6)
        hizala('sove', 0.0, 0.0, 99.0, g_ek=g_diger * (1 - w_sove), v_=wallV)
        for t in ('denizlik', 'dograma', 'kapi'):
            hizala(t, 0.0, 0.0, 99.0, v_=wallV)
        # cam: pencere ışığı söner
        G.ayarla(gm['cam'], g=g_diger, gu=g_diger if Tz >= tarama_son else gu_taban, tz=tz, v=max(dal, wallV), sicak=sicak)
        # kolon/kiriş/döşeme: karkas (ısı sızıntısı)
        for t in ('kolon', 'kiris', 'doseme'):
            G.ayarla(gm[t], g=g_diger, gu=g_diger if Tz >= tarama_son else gu_taban, tz=tz, v=dal, h=0.0, isi=isi)
        # iç bölme duvarı
        ic_gor = max(w_ic, w_son * 0.0)
        G.ayarla(gm['icblok'], g=(1 - ic_gor) * g_diger, gu=(1 - ic_gor) * g_diger, tz=-99, v=max(dal, 1 - agirlik(Tz, 36.9, 37.3, 38.8, 39.1)),
                 h=5.0 * ic_gor, hz=-1.0 + 12.5 * kit.seg(Tz, 37.0, 37.9), hd=(0, 0, 1))
        self.obs['icblok'].hide_render = ev_gizli or not (36.85 < Tz < 39.2)
        # harç çizgileri (derz ağı): yalnız tutkal durağında ve çıkış koroda
        harc_gor = w_harc
        koro_derz = darbe(Tz, 65.55, 0.35) + w_son * 0.7
        h_h = max(harc_gor, min(1.0, koro_derz))
        M.harc_ayarla(gm['harc'], h=h_h, czh=(-1.0 + 12.5 * kit.seg(Tz, 51.0, 51.45)) if Tz < 56 else 99.0,
                      czv=(-1.0 + 12.5 * kit.seg(Tz, 51.45, 51.85)) if Tz < 56 else 99.0)
        self.obs['harc'].hide_render = ev_gizli or h_h < 0.01
        # çıkış koro: altı ürün sırayla (blok, lento, U, derz, panel, EGEPOR), sonra hepsi birden
        koro = {}
        for k, t in enumerate(('blok', 'lento', 'ublok', 'harc', 'panel', 'egepor')):
            koro[t] = darbe(Tz, 65.1 + 0.16 * k, 0.28)
        # blok/lento/U/panel için H'yi çıkış durumuna uygula
        if Tz >= 64.9:
            hz_son = -1.0 + 14.0 * kit.seg(Tz, 66.0, 66.9)
            for t, h_k in (('blok', 6.0), ('lento', 6.0), ('ublok', 6.0), ('panel', 6.0)):
                pulse = koro[t]
                dalga_hz = hz_son if Tz >= 65.9 else 99.0
                gtmp = kit.lerp(g_diger, 0.4, w_son)
                hh = max(h_k * pulse, h_k * w_son)
                hh = max(hh, {'blok': h_blok, 'lento': 6.0 * w_lento, 'ublok': 6.0 * w_ub, 'panel': 6.0 * w_panel}[t])
                G.ayarla(gm[t], g=gtmp, gu=gtmp, tz=-99, v=dal, h=hh, hz=dalga_hz if (t != 'panel') else (-7.0 + 14.0 * kit.seg(Tz, 66.0, 66.9) if Tz >= 65.9 else 99.0),
                         hd=(0, 0, 1) if t != 'panel' else (1, 0, 0))
        # ----- öne çıkan bloklar (düz + geçmeli)
        k_cik = kit.smoother(kit.seg(Tz, 37.7, 38.5)) * (1 - kit.smoother(kit.seg(Tz, 38.9, 39.6)))
        yaw = math.radians(20.0) * kit.seg(Tz, 38.0, 39.0)
        mid = (self.hero_rest[0] + self.hero_rest[1]) / 2
        flo = Vector((B.XS[-1] + 1.3, mid.y, mid.z + 0.95))
        for k, (ob, rest) in enumerate(zip(self.heroes, self.hero_rest)):
            fy = flo.y + (-0.5 if k == 0 else 0.5)
            fz = Vector((flo.x, fy, flo.z))
            ob.location = rest.lerp(fz, k_cik)
            ob.rotation_euler = (0, 0, (math.pi / 2 if k == 1 else 0.0) + yaw * k_cik * (1 if k == 0 else -1))
            ob.hide_render = ev_gizli
        # ----- kesit parçası + ısı okları
        k_kes = kit.smoother(kit.seg(Tz, 38.95, 39.35)) * (1 - kit.smoother(kit.seg(Tz, 39.8, 40.25)))
        gor_kes = 0.002 < k_kes
        self.kesit_ob.hide_render = not gor_kes
        self.kesit_ob.location = (-1.3 * (1 - k_kes), 0, 0)
        G.ayarla(self.gm_kesit, g=0.0, gu=0.0, tz=-99, v=0.0, h=5.0 * k_kes * w_duvar)
        for ob in self.isi_obs:
            ob.hide_render = not (39.3 < Tz < 40.25)
            ob.location = (-1.3 * (1 - k_kes), 0, 0)
        ok_ac = [kit.smooth(kit.seg(Tz, 39.3 + 0.12 * i, 39.6 + 0.12 * i)) for i in range(3)]
        for m, a, guc in zip(self.ok_m, ok_ac, (4.0, 2.2, 0.9)):
            M.ok_guc(m, guc * a * (0.85 + 0.15 * math.sin(Tz * 9.0)))
        for ob, mm in zip(self.perdeler, (self.perde_ic, self.perde_dis)):
            ob.hide_render = not (39.2 < Tz < 40.2)
            M.perde_alfa(mm, 0.12 * kit.smooth(kit.seg(Tz, 39.3, 39.7)))
            ob.location = (-1.3 * (1 - k_kes), 0, 0)
        # ----- lento: duvardan 10 cm kayar; bitişik blok eşzamanlı lime
        kay = kit.smoother(kit.seg(Tz, 44.0, 44.5)) * (1 - kit.smoother(kit.seg(Tz, 45.0, 45.5)))
        self.lento_ob.location = self.lento_c + Vector((0.10 * kay, 0, 0))
        w_bit = agirlik(Tz, 44.2, 44.7, 45.3, 45.8)
        G.ayarla(self.gm_kom, g=g_diger * (1 - w_bit), gu=g_diger * (1 - w_bit), tz=tz, v=max(dal, wallV), h=6.0 * w_bit if True else 0.0, hz=99.0)
        if Tz < 44.2 or Tz > 45.8:  # diğer zamanlarda 'blok' ile aynı davransın
            G.ayarla(self.gm_kom, g=gm['blok'].node_tree.nodes['G'].outputs[0].default_value,
                     gu=gm['blok'].node_tree.nodes['GU'].outputs[0].default_value, tz=tz, v=max(dal, wallV),
                     h=gm['blok'].node_tree.nodes['H'].outputs[0].default_value,
                     hz=gm['blok'].node_tree.nodes['HZ'].outputs[0].default_value)
        self.lento_ob.hide_render = ev_gizli
        self.kom_ob.hide_render = ev_gizli
        # yük okları: üstten iner, sonra iki yana yayılır
        ac_ust = kit.smooth(kit.seg(Tz, 43.0, 43.45)) * (1 - kit.smooth(kit.seg(Tz, 44.4, 44.8)))
        ac_yay = kit.smooth(kit.seg(Tz, 43.5, 44.0)) * (1 - kit.smooth(kit.seg(Tz, 44.4, 44.8)))
        for ob in self.yuk_ust:
            ob.hide_render = ac_ust < 0.01
        for ob in self.yuk_yay:
            ob.hide_render = ac_yay < 0.01
        M.ok_guc(self.yuk_m, 2.6 * max(ac_ust, ac_yay))
        # ----- U blok detayı: parapetten kalkar, kanal açık; donatı; beton dolar
        kalk = kit.smoother(kit.seg(Tz, 46.7, 47.6)) * (1 - kit.smoother(kit.seg(Tz, 50.1, 50.7)))
        ofs = self.u_ofset * (1 - kalk)
        gor_u = kalk > 0.002 and not ev_gizli
        for ob in self.u_kabuk:
            ob.hide_render = not gor_u
            ob.location = ofs
        self.u_donati.hide_render = not gor_u or kalk < 0.5
        self.u_donati.location = ofs
        dol = max(0.002, 0.3 * kit.smooth(kit.seg(Tz, 48.0, 48.6)) + 0.65 * kit.smooth(kit.seg(Tz, 48.9, 50.0)))  # %30 → %95
        self.hatil_ob.hide_render = not gor_u or Tz < 48.0 or kalk < 0.4  # geri oturunca beton blokların içinde kalır
        self.hatil_ob.scale = (1, 1, dol)
        self.hatil_ob.location = Vector((ofs.x, ofs.y, ofs.z + self.hz0 * (1 - dol)))
        # ----- tutkal torbası (kameraya göre sabit: torba kamera önünde yavaş döner)
        k_tb = kit.smoother(kit.seg(Tz, 51.9, 52.4)) * (1 - kit.smoother(kit.seg(Tz, 53.0, 53.35)))
        self.torba.hide_render = k_tb < 0.01 or ev_gizli
        if k_tb >= 0.01:
            ileri = (hedef - loc).normalized()
            sag = ileri.cross(Vector((0, 0, 1))).normalized()
            yuk = sag.cross(ileri).normalized()
            kon = loc + ileri * 6.2 + sag * 0.0 + yuk * (-1.9)
            sk = 1.6 * k_tb
            self.torba.scale = (sk, sk, sk)
            self.torba.location = kon - Vector((0, 0, 0.30 * sk))
            self.torba.rotation_euler = (math.radians(4), 0, math.radians(35 + 55 * (Tz - 52.0)))
        # ----- panel şeritleri: piyano tuşu (T 57–58,3), sonra hafif yüzme
        for i, (x, ob) in enumerate(self.panel_obs):
            ti = 57.0 + i * 0.045
            kalk_p = 0.34 * math.sin(math.pi * kit.clamp01((Tz - ti) / 0.45)) if 57.0 <= Tz <= 58.4 else 0.0
            yuz_p = 0.12 * math.sin(Tz * 3.0 + i * 0.5) * agirlik(Tz, 58.6, 59.0, 59.9, 60.3)
            ob.location = (0, 0, kalk_p + yuz_p)
            ob.hide_render = ev_gizli
        # ----- Egepor levhaları (kolon kolon, dışarıdan kayarak oturur)
        for g, (ob, mm, lst) in enumerate(self.ep):
            t0 = 62.0 + 0.14 * g
            ea = kit.ease_out(kit.seg(Tz, t0, t0 + 0.55), 3)
            if once:
                ea = 0.0
            ob.hide_render = ea <= 0 or ev_gizli
            s = 1 + 0.38 * (1 - ea)
            ob.scale = (s, s, 1 + 0.10 * (1 - ea))
            ob.location = (0, 0, 0)
            temas = darbe(Tz, t0 + 0.55, 0.28) if not once else 0.0
            g_e = 0.0 if Tz < 66 else kit.lerp(0.0, 0.3, w_son)
            h_e = 6.0 * max(temas, darbe(Tz, 64.4, 0.4), koro['egepor'] * 1.0, w_son)
            G.ayarla(mm, g=g_e, gu=g_e, tz=-99, v=dal, h=h_e, hz=99.0)
        # ----- odak blok (dalış): duvardan öne kayar, zemine iner
        bpos, k1, k2 = odak_konum(Tz, self.odak_rest)
        self.odak_ob.location = bpos
        self.odak_ob.rotation_euler = (0, 0, math.radians(6.0) * kit.smoother(kit.seg(Tz, 68.4, 69.6)))
        sx = kit.lerp(0.98, 1.0, k1)
        self.odak_ob.scale = (sx, kit.lerp(0.8, 1.0, k1), kit.lerp(0.952, 1.0, k1))
        if Tz < 66.4:
            # odak, duvar bloklarıyla aynı davranır
            n = gm['blok'].node_tree.nodes
            G.ayarla(self.gm_odak, g=n['G'].outputs[0].default_value, gu=n['GU'].outputs[0].default_value, tz=tz, v=0.0,
                     h=n['H'].outputs[0].default_value, hz=n['HZ'].outputs[0].default_value)
        else:
            go = kit.lerp(gm['blok'].node_tree.nodes['G'].outputs[0].default_value, 0.0, kit.smooth(kit.seg(Tz, 66.4, 67.6)))
            ho = 6.0 + 2.0 * kit.smooth(kit.seg(Tz, 67.4, 68.4))
            ho *= 1 - kit.smooth(kit.seg(Tz, 68.8, 69.5))
            G.ayarla(self.gm_odak, g=go, gu=go, tz=-99, v=0.0, h=ho, hz=99.0)
        # ----- görünürlük: ev tamamen kaybolunca çizilmesin (hız + leke)
        for t, ob in self.obs.items():
            if t in ('icblok', 'harc'):
                continue
            ob.hide_render = ev_gizli
        self.golge_ayarla(dal, g_taban, ev_gizli)
        sc.cycles.transparent_max_bounces = 12
        return Tz, loc, hedef, cam


def noktalar(S, f, Tz, cam, loc, hedef):
    """Tıklanır noktalar / SVG çapaları (ekran 0..1, sol üst köşe 0,0)."""
    hs = {}
    P = lambda *pts: kit.project(cam, [tuple(p) for p in pts])  # noqa: E731

    def ekle(ad, p):
        if p and 0.02 < p[0] < 0.98 and 0.04 < p[1] < 0.96:
            hs[ad] = p
    if 33.0 <= Tz <= 34.05:  # tarama çizgisi: ev merkezindeki yükseklik
        zt = 12.5 - 13.5 * kit.smooth(kit.seg(Tz, 33.0, 34.0))
        p = P((0, 0, zt))[0]
        if p:
            hs['tarama'] = p
    if 36.2 <= Tz < 41.0:
        ekle('u_duvar', P(S.hero_rest[0])[0] if Tz < 37.5 else P((6.1, 0.2, 2.8))[0])
    if 37.7 <= Tz <= 39.2:
        for k, ad in enumerate(('u_duvar_duz', 'u_duvar_gecmeli')):
            ekle(ad, P(S.heroes[k].location)[0])
    if 39.3 <= Tz <= 40.2:
        ekle('u_isi', P((KESIT_YUZ + 0.02, KESIT_C.y - 0.35, KESIT_C.z))[0])
        ekle('kesit_ic', P((KESIT_YUZ, KESIT_C.y - 0.6, KESIT_C.z))[0])
        ekle('kesit_dis', P((KESIT_YUZ, KESIT_C.y + 0.6, KESIT_C.z))[0])
    if 41.6 <= Tz < 46.0:
        c = S.lento_c
        yarim = S.lento_s[1] / 2
        ekle('u_lento', P(c)[0])
        # pencere boşluğunun iki ucu (ölçü çizgisi) ve oturma noktaları
        ekle('u_lento_a', P((c.x + 0.12, c.y - 0.6, c.z - 0.13))[0])
        ekle('u_lento_b', P((c.x + 0.12, c.y + 0.6, c.z - 0.13))[0])
        ekle('olcu_a', P((c.x + 0.12, c.y - 0.6, c.z - 0.5))[0])
        ekle('olcu_b', P((c.x + 0.12, c.y + 0.6, c.z - 0.5))[0])
        ekle('oturma_a', P((c.x + 0.12, c.y - 0.85, c.z))[0])
        ekle('oturma_b', P((c.x + 0.12, c.y + 0.85, c.z))[0])
    if 46.5 <= Tz < 50.7:
        ut = S.ut
        ekle('u_ublok', P(ut)[0])
        ekle('u_ublok_cati', P(ut + Vector((0, 0, -0.4)))[0])
        ekle('u_ublok_ara', P((0, B.YS[-1] + 0.15, 2 * B.FH - 0.25))[0])  # yüksek duvar ara hatılı (2. kat kirişi)
        ekle('u_ublok_baca', P((B.XS[0] + 0.5, B.YS[-1] - 0.5, ZIRVE + 0.9))[0])
        ekle('donati', P(ut + Vector((0, 0, 0.0)))[0])
    if 51.0 <= Tz < 55.6:
        ekle('u_tutkal', P((B.XS[0], 0.0, 4.0))[0])
        ekle('u_tutkal_derz', P((B.XS[0] - 0.12, 2.3, 4.25))[0])
    if 52.0 <= Tz <= 53.4 and not S.torba.hide_render:
        ekle('torba', P(S.torba.location + Vector((0, 0, 0.45)))[0])
    if 56.0 <= Tz < 61.0:
        ekle('u_panel', P((0, 0, ZIRVE + 0.2))[0])
        ekle('u_panel_aciklik', P((0, B.YS[1] - 2.2, ZIRVE + 0.25))[0])
        ekle('olcu_panel_a', P((B.XS[0] + 0.2, B.YS[0] + 0.1, ZIRVE + 0.25))[0])
        ekle('olcu_panel_b', P((B.XS[0] + 0.2, B.YS[1] - 0.1, ZIRVE + 0.25))[0])
    if 61.0 <= Tz < 66.5:
        ekle('u_egepor', P((-2.0, B.YS[0] - 0.2, 1.4))[0])
        ekle('bolme', P(KOL_BIRLESIM)[0])
    if Tz >= 67.4:
        ekle('u_blok', P(S.odak_ob.location + Vector((0, -0.15, 0)))[0])
    return hs


def main():
    kit.reset()
    v = ARGS.variant
    sc = kit.setup_render(*RES[v], samples=ARGS.samples, threshold=ARGS.esik, bounces=(6, 3, 3, 6))
    sc.cycles.transparent_max_bounces = 12
    sc.cycles.adaptive_min_samples = 6
    S = Sahne(v, ARGS.kip)
    if ARGS.kip == 'once':
        frames = [int(x) for x in ARGS.frames.split(',')] if ARGS.frames != 'all' else [124, 125, 126, 127]
    else:
        frames = pass_order(FRAMES) if ARGS.frames == 'all' else [int(x) for x in ARGS.frames.split(',')]
    os.makedirs(ARGS.out, exist_ok=True)
    meta_path = os.path.join(ARGS.out, 'meta.json')
    meta = {'frames': FRAMES, 'res': list(RES[v]), 'hotspots': {}}
    if os.path.exists(meta_path):
        import json
        eski = json.load(open(meta_path, encoding='utf-8'))
        if eski.get('frames') == FRAMES:
            meta['hotspots'].update(eski.get('hotspots', {}))
    for f in frames:
        Tz, loc, hedef, cam = S.uygula(f)
        meta['hotspots'][str(f)] = noktalar(S, f, Tz, cam, loc, hedef)
        path = os.path.join(ARGS.out, f'{f:03d}.png')
        kit.write_json(meta_path, meta)
        if ARGS.skip_existing and os.path.exists(path):
            continue
        t0 = time.time()
        c0 = os.times()
        kit.render_to(path)
        c1 = os.times()
        print(f'KARE {f} {time.time() - t0:.1f}s cpu={c1.user + c1.system - c0.user - c0.system:.0f}s', flush=True)
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
    ap.add_argument('--samples', type=int, default=24)
    ap.add_argument('--esik', type=float, default=0.03)
    ap.add_argument('--kip', default='ana')
    ap.add_argument('--skip-existing', action='store_true')
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
