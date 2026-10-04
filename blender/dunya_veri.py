"""
Dünya (s5) verisi ve zaman yardımcıları — Blender'sız, numpy ile.

Nokta seviyeleri (tools/kure_noktalari.mjs ile üretilir, EGE_TEX klasöründe):
  L0  bolge_L0.json   ≈1,25 km altıgen ızgara, İzmir çevresi (10 m poligon)     F000–F013
  L1  kara_L1.json    ≈10 km, 28–48 K / 12–48 D (50 m)                          F005–F038
  L15 kara_L15.json   ≈44 km, İzmir'e 82° kap (110 m)                           F025–F058
  L2  kara_noktalari.json 1,25° (≈139 km) küre (110 m)                          F046–F192
Her seviyenin kıta kimlikleri aynıdır (0 Avrupa, 1 Asya, 2 Afrika, 3 Amerika, 4 Okyanusya, 5 Türkiye, 8 nötr).
Renk/ışık fonksiyonu (`boya`) tüm seviyelerde aynı olduğundan seviyeler arası geçişte dalga ve renk tutarlı kalır.
"""
import json
import math
import os

import numpy as np

import kit

R = 1.0
KM = 1.0 / 6371.0            # 1 km kaç R
IZMIR = (38.42, 27.14)
SOKE = (37.76, 27.40)        # Söke çevresi (temsilî nokta: fabrika konumu iddia edilmez)

# yay hedefleri: (kıta id, lat, lon, yay başı F, yay bitişi F, varış dalgası bitişi F) — plan kare programı
TARGETS = [
    (0, 50.5, 12.0, 40, 50, 62),     # Avrupa
    (2, 6.0, 21.0, 46, 59, 71),      # Afrika
    (3, 15.0, -88.0, 53, 73, 88),    # Amerika (Orta Amerika: kara üstü)
    (1, 40.0, 92.0, 88, 103, 115),   # Asya
    (4, -25.0, 134.0, 102, 124, 138),  # Okyanusya
]
AD = ('avrupa', 'afrika', 'amerika', 'asya', 'okyanusya')

SOGUK = np.array([0.66, 0.72, 0.76, 1.0], dtype=np.float32)    # kara noktası: serin gri-beyaz
SICAK = np.array([1.0, 0.90, 0.72, 1.0], dtype=np.float32)     # varış sonrası: sıcak beyaz
SEHIR = np.array([1.0, 0.78, 0.46, 1.0], dtype=np.float32)     # gece ışıkları (sıcak beyaz, lime değil)


# ---------------------------------------------------------------------------
#  Vektörleştirilmiş zamanlama yardımcıları
# ---------------------------------------------------------------------------
def sm(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def sg(t, a, b):
    """numpy: t'nin [a, b] aralığındaki ilerlemesi (a, b dizi olabilir)."""
    return np.clip((t - a) / np.maximum(b - a, 1e-6), 0.0, 1.0)


def pchip(x, keys):
    """Tekdüze kübik Hermite (Fritsch–Carlson): anahtarlar arası yumuşak, aşım yok. keys: [(x, y), ...]"""
    xs = np.array([k[0] for k in keys], dtype=float)
    ys = np.array([k[1] for k in keys], dtype=float)
    if x <= xs[0]:
        return float(ys[0])
    if x >= xs[-1]:
        return float(ys[-1])
    h = np.diff(xs)
    dl = np.diff(ys) / h
    m = np.zeros(len(xs))
    for i in range(1, len(xs) - 1):
        if dl[i - 1] * dl[i] > 0:
            w1, w2 = 2 * h[i] + h[i - 1], h[i] + 2 * h[i - 1]
            m[i] = (w1 + w2) / (w1 / dl[i - 1] + w2 / dl[i])
    m[0], m[-1] = 0.0, 0.0  # uçlarda yavaş başla/dur
    i = int(np.searchsorted(xs, x) - 1)
    t = (x - xs[i]) / h[i]
    h00 = (1 + 2 * t) * (1 - t) ** 2
    h10 = t * (1 - t) ** 2
    h01 = t * t * (3 - 2 * t)
    h11 = t * t * (t - 1)
    return float(h00 * ys[i] + h10 * h[i] * m[i] + h01 * ys[i + 1] + h11 * h[i] * m[i + 1])


def birim(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], -1).astype(np.float32)


def aci(u, v):
    """Birim vektör dizisi u (n,3) ile v (3,) arası açı (radyan)."""
    return np.arccos(np.clip(u @ np.asarray(v, dtype=np.float32), -1.0, 1.0))


# ---------------------------------------------------------------------------
#  Nokta seviyeleri
# ---------------------------------------------------------------------------
class Seviye:
    """Bir nokta ızgarası: konumlar, kıta, rastgele sapma, İzmir'e açı, gece ışığı bayrakları."""

    def __init__(self, ad, dosya, tohum, sehir=True):
        yol = os.path.join(kit.TEX_DIR, dosya)
        self.ad = ad
        pts = np.array(json.load(open(yol)), dtype=np.float32)
        self.n = len(pts)
        self.lat, self.lon = pts[:, 0], pts[:, 1]
        self.kita = pts[:, 2].astype(int)
        self.u = birim(self.lat, self.lon)
        rng = np.random.default_rng(tohum)
        self.jit = rng.random(self.n).astype(np.float32)
        self.dI = aci(self.u, birim(*IZMIR))          # İzmir'e açı (radyan): Türkiye lime dalgası
        self.dS = aci(self.u, birim(*SOKE))
        # stilize gece ışıkları: kümeli (gürültü) + rastgele; toplam oran ≤ %8, sıcak beyaz
        self.sehir = np.zeros(self.n, dtype=np.float32)
        if sehir:
            u = self.u
            g = (np.sin(7.3 * u[:, 0] + 1.1 * u[:, 1] + 0.4) * np.sin(5.9 * u[:, 1] - 2.3 * u[:, 2] + 0.9)
                 + 0.6 * np.sin(13.1 * u[:, 2] + 3.7 * u[:, 0]) * np.sin(9.7 * u[:, 0] - 4.1 * u[:, 1]))
            g = (g - g.min()) / (g.max() - g.min())
            p = np.clip(0.02 + 0.26 * sm((g - 0.45) / 0.45), 0.0, 0.2)
            bayrak = (rng.random(self.n) < p) & (self.kita != 5) & (self.kita != 8)
            oran = bayrak.mean() if self.n else 0
            if oran > 0.075:  # ≤ %8 sınırı (plan)
                bayrak &= rng.random(self.n) < (0.075 / oran)
            self.sehir[bayrak] = (0.45 + 0.55 * rng.random(int(bayrak.sum()))).astype(np.float32)
        self.dn = []   # hedef başına (maske, normalleştirilmiş uzaklık) — MAXANG ile doldurulur
        self.hedefa = []

    def dalga_hazirla(self, maxang):
        self.hedefa = []
        for (kid, lat, lon, *_), mx in zip(TARGETS, maxang):
            a = aci(self.u, birim(lat, lon))
            m = self.kita == kid
            self.hedefa.append((m, np.minimum(a / mx, 1.0).astype(np.float32), a.astype(np.float32)))


def seviyeleri_yukle():
    L2 = Seviye('L2', 'kara_noktalari.json', 11)
    # her hedef için kıtanın en uzak noktası (küre seviyesinden): tüm seviyelerde aynı dalga tabanı
    maxang = []
    for (kid, lat, lon, *_) in TARGETS:
        a = aci(L2.u, birim(lat, lon))
        m = L2.kita == kid
        maxang.append(float(a[m].max()) if m.any() else 1.0)
    L2.dalga_hazirla(maxang)
    out = {'L2': L2}
    for ad, dosya, tohum in (('L0', 'bolge_L0.json', 3), ('L1', 'kara_L1.json', 5), ('L15', 'kara_L15.json', 7)):
        try:
            S = Seviye(ad, dosya, tohum, sehir=(ad != 'L0'))
            S.dalga_hazirla(maxang)
            out[ad] = S
        except OSError as e:  # eski EGE_TEX: bölge/L1 yoksa doğrudan küre
            print('UYARI: seviye yok', dosya, e, flush=True)
    return out, maxang


# ---------------------------------------------------------------------------
#  Renk / ışık: tüm seviyelerde aynı fonksiyon
# ---------------------------------------------------------------------------
def boya(S, f, rot3, sun, ndv, cam_gece=1.0, arka_zayif=0.0, nefes=1.0):
    """Seviye S için kare f'de (renk (n,4), ışık (n,)).
    rot3: küre dönüşü 3x3 (numpy), sun: güneşe yön (dünya, birim), ndv: nokta normali · kameraya yön (n,) (ufuk testi),
    arka_zayif: 0..1 cam gövde evresi (arka yüzdeki noktalar %40 ışığa iner)."""
    n = S.n
    col = np.tile(SOGUK, (n, 1))
    glow = np.full(n, 0.05, dtype=np.float32)
    # gece yarımküresi: güneşe göre
    nrm = S.u @ rot3.T
    ns = nrm @ sun
    gece = sm((0.06 - ns) / 0.32).astype(np.float32)           # 0 gündüz … 1 gece
    glow += 0.07 * gece                                          # karanlıkta kıta silüeti okunsun
    # Türkiye: kaynak, lime. İzmir'den dışa dolan dalga (F022 → F040)
    tr = S.kita == 5
    if tr.any():
        ta = 22.0 + 14.0 * np.minimum(S.dI[tr] / 0.26, 1.0)
        k = sm(sg(f, ta, ta + 6.0))
        col[tr] = SOGUK * (1 - k)[:, None] + np.array(kit.LIME_HI, dtype=np.float32) * k[:, None]
        glow[tr] = 0.05 + 1.25 * k + 0.1 * gece[tr]
    # kıta varış dalgaları: serin gri → sıcak beyaz, dalga ucu parlak
    wave_boost = np.zeros(n, dtype=np.float32)
    for (kid, lat, lon, fa, fb, fw), (m, dn, ang) in zip(TARGETS, S.hedefa):
        if f < fb or not m.any():
            continue
        ti = fb + dn[m] * max(fw - fb - 5, 1)
        pr = sg(f, ti, ti + 5.0)
        p = sm(pr)
        uc = col[m]
        col[m] = uc * (1 - p)[:, None] + SICAK * p[:, None]
        on = np.sin(np.pi * np.clip(pr, 0, 1)).astype(np.float32)       # dalga ucu: 1,6 parlaklık
        glow[m] = glow[m] + 0.62 * p + 1.0 * on
        wave_boost[m] = np.maximum(wave_boost[m], on)
    # gece ışıkları (stilize, ≤ %8): yalnız karanlık yarıda; varış dalgasıyla parlar
    if S.sehir.any():
        yan = np.clip(0.6 + 0.4 * np.sin(f * 0.21 + S.jit * 40.0), 0, 1)   # hafif titreme
        c = S.sehir * gece * (0.9 + 1.4 * wave_boost) * yan
        c = c * (1.0 + 0.0 * ns)
        col = col * (1 - np.clip(c * 0.9, 0, 1)[:, None]) + SEHIR * np.clip(c * 0.9, 0, 1)[:, None]
        glow = glow + 1.1 * c
    # cam gövde evresi: arka yüzdeki noktalar zayıflar (%40)
    if arka_zayif > 0:
        arka = sm((0.06 - ndv) / 0.22)
        glow = glow * (1 - 0.6 * arka * arka_zayif)
        col = col * (1 - 0.35 * (arka * arka_zayif))[:, None]
    glow = glow * nefes
    return col.astype(np.float32), glow.astype(np.float32)
