"""
Çizim → gerçek geçişi: aynı karenin "mimar çizimi" ve "gerçek" render'larını
çapraz bir silme ile birleştirir; sınırda ince lime tarama çizgisi + hafif ışıltı.
p = 0 → tamamen çizim, p = 1 → tamamen gerçek.

Kullanım: python tools/cizim_gecis.py <cizim.png> <gercek.png> <p> <cikti.png>
"""
import sys

import numpy as np
from PIL import Image

LIME = np.array([184, 216, 74], dtype=np.float32)


def gecis(cizim, gercek, p, egim=0.35, yumusak=0.004):
    a = np.asarray(cizim.convert('RGB'), dtype=np.float32)
    b = np.asarray(gercek.convert('RGB'), dtype=np.float32)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u = (xx / w) + egim * (1 - yy / h) * (h / w)  # sol alttan sağ üste ilerleyen çapraz cephe
    umin, umax = u.min(), u.max()
    sinir = umin + (umax - umin) * p
    m = np.clip((sinir - u) / yumusak + 0.5, 0, 1)[..., None]  # 1 → gerçek
    out = a * (1 - m) + b * m
    d = np.abs(u - sinir)
    cizgi = np.clip(1 - d / 0.0018, 0, 1)
    hale = np.exp(-(d / 0.02) ** 2) * 0.35
    k = np.clip(cizgi + hale, 0, 1)[..., None] if 0 < p < 1 else 0
    out = out * (1 - k) + LIME * k
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


if __name__ == '__main__':
    im = gecis(Image.open(sys.argv[1]), Image.open(sys.argv[2]), float(sys.argv[3]))
    im.save(sys.argv[4])
