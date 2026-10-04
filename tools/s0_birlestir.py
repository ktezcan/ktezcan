"""
Perde 1 ("Hayalden yuvaya") son kare dizisini kaynak render'lardan birleştirir.
Blender'ın yapmadığı geçişler burada 2B olarak üretilir (ucuz, kare kare aynı kadraj):

  A kıvılcım  : bej kâğıtta ışık noktası doğar, ince ışınlar saçılır
  B plan      : vaziyet planı kıvılcımdan dışa doğru kendini çizer (zaman haritası + gürültü)
  C eğim      : (Blender) kamera tepeden göz hizasına iner, bina kâğıttan yükselir → eskiz
  D karanlık  : eskiz → tel kafes: binadan açılan dairesel silme, sınırda ışık halkası
  E dolum     : (Blender) gazbeton bloklar sıra sıra yerine iner
  F gerçek    : çapraz silme + lime tarama çizgisi → fotogerçekçi gündüz
  G sokak     : (Blender) araba, bisikletli, yayalar, Ege Gazbeton tırı
  H gün       : güneş alçalır (plakalar arası erime), akşam: pencereler tek tek yanar

Kullanım: python tools/s0_birlestir.py <kaynak_kök (içinde d/, m/)> <render_kök> [d m]
Çıktı: <render_kök>/s0<v>/NNN.png + meta.json (kareler.py'nin beklediği biçim)
"""
import json
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cizim_gecis import gecis  # noqa: E402

# sitede karşılığı (TR/EN kart metni) olan noktalar; diğerleri pakete girmez
ETIKETLI = {'giris', 'bahce', 'sokak', 'eskiz', 'blok', 'lento', 'panel', 'derz', 'tir', 'yuva'}
LIME = np.array([184, 216, 74], np.float32)
SICAK = np.array([255, 214, 150], np.float32)


def yukle(p):
    return np.asarray(Image.open(p).convert('RGB'), np.float32)


def kaydet(a, p):
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(p, compress_level=3)


def ss(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def gurultu(h, w, olcek, seed):
    rnd = np.random.default_rng(seed)
    k = rnd.random((max(2, h // olcek), max(2, w // olcek))).astype(np.float32)
    return np.asarray(Image.fromarray((k * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255


class Dizi:
    def __init__(self, kaynak, v):
        self.k = os.path.join(kaynak, v)
        self.meta = {}
        for kip in ('egim', 'dolum', 'sokak', 'plaka'):
            p = os.path.join(self.k, kip, 'meta.json')
            self.meta[kip] = json.load(open(p)) if os.path.exists(p) else {}
        self.kareler = []  # (üretici, noktalar)

    def kaynak(self, kip, i):
        return os.path.join(self.k, kip, f'{i:03d}.png')

    def var(self, kip, i):
        return os.path.exists(self.kaynak(kip, i))

    def oku(self, kip, i):
        """Eksik ara kare: en yakın iki mevcut karenin erimesi (telefon setinde seyrek render)."""
        if self.var(kip, i):
            return yukle(self.kaynak(kip, i))
        a = next((j for j in range(i, -1, -1) if self.var(kip, j)), None)
        b = next((j for j in range(i, i + 40) if self.var(kip, j)), None)
        if a is None and b is None:
            raise FileNotFoundError(self.kaynak(kip, i))
        if a is None or b is None:
            return yukle(self.kaynak(kip, a if b is None else b))
        t = (i - a) / (b - a)
        return yukle(self.kaynak(kip, a)) * (1 - t) + yukle(self.kaynak(kip, b)) * t

    def nokta(self, kip, i):
        return self.meta[kip].get(str(i), {})

    def ekle(self, fn, nokta=None):
        self.kareler.append((fn, nokta or {}))


def kur(d):
    plan = d.oku('egim', 0)
    h, w = plan.shape[:2]
    kagit = plan[2:6, 2:6].reshape(-1, 3).mean(0)
    n0 = d.nokta('egim', 0)
    gx, gy = n0.get('giris', [0.5, 0.45])
    kv = np.array([gx * w, (gy - 0.06) * h])  # kıvılcım: bina ayak izinin önü
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.hypot(xx - kv[0], yy - kv[1])
    rmax = r.max()
    tmap = 0.78 * r / rmax + 0.22 * gurultu(h, w, 24, 3)
    rnd = random.Random(5)
    isinlar = [(rnd.uniform(0, 2 * math.pi), rnd.uniform(0.25, 0.9), rnd.uniform(0.6, 1.4)) for _ in range(46)]

    def isik(a, k, kuv=1.0):
        g = np.exp(-(r / (0.012 * w + 0.05 * w * k)) ** 2)[..., None] * kuv
        return a * (1 - g * 0.6) + SICAK * g

    def isin_ciz(a, k, alfa):
        im = Image.new('L', (w, h), 0)
        dr = ImageDraw.Draw(im)
        for (ang, uz, kal) in isinlar:
            L = uz * rmax * 0.55 * k
            L0 = max(0.0, L - 0.18 * rmax)
            dr.line([(kv[0] + math.cos(ang) * L0, kv[1] + math.sin(ang) * L0),
                     (kv[0] + math.cos(ang) * L, kv[1] + math.sin(ang) * L)], fill=255, width=max(1, int(kal * w / 900)))
        m = np.asarray(im.filter(ImageFilter.GaussianBlur(1.2)), np.float32)[..., None] / 255 * alfa
        return a * (1 - m * 0.75) + np.array([60, 52, 44], np.float32) * m * 0.75

    # A: kıvılcım (8)
    for i in range(8):
        k = i / 7

        def f(k=k):
            a = np.ones((h, w, 3), np.float32) * kagit
            a = isik(a, 0.2 + 0.8 * k, ss(0, 0.4, k))
            return isin_ciz(a, ss(0.3, 1.0, k), ss(0.3, 0.6, k))
        d.ekle(f)
    # B: plan kendini çizer (16)
    for i in range(16):
        t = (i + 1) / 16

        def f(t=t):
            m = ss(t * 1.1 - 0.08, t * 1.1, tmap)[..., None]
            a = kagit * (1 - m) + plan * m
            a = isin_ciz(a, 1.0 + 0.6 * t, 1 - ss(0.0, 0.5, t))
            return isik(a, 1.0 - 0.6 * t, 1 - ss(0.2, 0.9, t))
        d.ekle(f, n0 if t > 0.55 else {})
    # C: eğim + kalemle çizim (Blender, plan: 38 kare; bina yükselmez, çizilir)
    n_e = int(d.meta['egim'].get('_n', 18))
    for i in range(n_e):
        d.ekle(lambda i=i: d.oku('egim', i), d.nokta('egim', i))
    # D: eskiz → tel kafes, binadan açılan daire (6)
    k0 = d.oku('dolum', 0)
    lum = k0.mean(2)
    ys, xs = np.nonzero(lum > 40)
    bm = np.array([xs.mean(), ys.mean()]) if len(xs) else np.array([w * 0.6, h * 0.5])
    rb = np.hypot(xx - bm[0], yy - bm[1])
    rbm = rb.max()
    eskiz = d.oku('egim', n_e - 1)
    for i in range(6):
        t = (i + 1) / 7

        def f(t=t):
            R = rbm * ss(0, 1, t) * 1.05
            m = ss(R + 0.02 * w, R - 0.02 * w, rb)[..., None]
            a = eskiz * (1 - m) + k0 * m
            halka = np.exp(-((rb - R) / (0.006 * w)) ** 2)[..., None] * (1 - ss(0.8, 1, t))
            return a * (1 - halka) + np.array([233, 242, 255], np.float32) * halka
        d.ekle(f)
    # E: dolum (Blender 28)
    for i in range(28):
        d.ekle(lambda i=i: d.oku('dolum', i), d.nokta('dolum', i))
    # F: gerçeğe dönüşüm (12)
    son_dolum = Image.open(d.kaynak('dolum', 27))
    gun0 = Image.open(d.kaynak('sokak', 0)) if d.var('sokak', 0) else Image.fromarray(d.oku('sokak', 0).astype(np.uint8))
    for i in range(12):
        p = (i + 1) / 13
        d.ekle(lambda p=p: np.asarray(gecis(son_dolum, gun0, p, egim=0.35, yumusak=0.004), np.float32))
    # G: sokak (36)
    for i in range(36):
        d.ekle(lambda i=i: d.oku('sokak', i), d.nokta('sokak', i))
    # H: gün ilerler (4 + 5×4 + 4) + pencereler (10)
    zincir = [('sokak', 35)] + [('plaka', j) for j in range(7)]
    for (ka, ia), (kb, ib) in zip(zincir[:-1], zincir[1:]):
        for s in range(4):
            t = ss(0, 1, (s + 1) / 4)
            d.ekle(lambda ka=ka, ia=ia, kb=kb, ib=ib, t=t: d.oku(ka, ia) * (1 - t) + d.oku(kb, ib) * t)
    pen = d.meta['plaka'].get('pencereler', [])
    rnd = random.Random(11)
    sira = sorted(range(len(pen)), key=lambda j: (rnd.random() * 0.8 + pen[j]['kat'] * 0.1))
    bas = {j: 0.65 * n / max(1, len(sira) - 1) for n, j in enumerate(sira)}
    maske = []
    for j, p in enumerate(pen):
        im = Image.new('L', (w, h), 0)
        c = np.mean(p['k'], 0)
        pts = [tuple(((np.array(q) - c) * 1.15 + c) * [w, h]) for q in p['k']]
        ImageDraw.Draw(im).polygon(pts, fill=255)
        maske.append(np.asarray(im.filter(ImageFilter.GaussianBlur(w / 400)), np.float32) / 255)
    yuva = {}
    if pen:
        jy = sira[len(sira) // 2]
        yuva = {'yuva': [round(float(x), 4) for x in np.mean(pen[jy]['k'], 0)]}
    for s in range(10):
        t = (s + 1) / 10

        def f(t=t):
            off, on = d.oku('plaka', 6), d.oku('plaka', 7)
            M = np.zeros((h, w), np.float32)
            g = 0.0
            for j, m in enumerate(maske):
                wj = ss(bas[j], bas[j] + 0.3, t)
                M = np.maximum(M, m * wj)
                g += wj / max(1, len(maske))
            k = np.clip(M + g * (1 - M), 0, 1)[..., None]
            return off + (on - off) * k
        d.ekle(f, yuva if t > 0.5 else {})


def main(kaynak, render_kok, variants):
    for v in variants:
        d = Dizi(kaynak, v)
        kur(d)
        out = os.path.join(render_kok, f's0{v}')
        os.makedirs(out, exist_ok=True)
        meta = {'frames': len(d.kareler), 'res': None, 'hotspots': {}}
        for i, (fn, nk) in enumerate(d.kareler):
            a = fn()
            meta['res'] = [a.shape[1], a.shape[0]]
            kaydet(a, os.path.join(out, f'{i:03d}.png'))
            meta['hotspots'][str(i)] = {k: q for k, q in nk.items() if k in ETIKETLI}
            if 'pen' in nk:  # kalem ucu (ekran 0..1): sitedeki kalem sprite'ı için
                meta.setdefault('pen', {})[str(i)] = nk['pen']
        json.dump(meta, open(os.path.join(out, 'meta.json'), 'w'))
        print(v, len(d.kareler), 'kare')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3:] or ['d', 'm'])
