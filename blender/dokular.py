"""
Gazbeton yüzey dokuları (döşenebilir, prosedürel — yapay zekâ görseli değil).

Çıktı (2048×2048, 24 cm × 24 cm yüzey → ~0,12 mm/piksel):
  gazbeton_renk.png    sRGB renk (gözenek gölgesi + ince lekelenme)
  gazbeton_yukseklik.png  16 bit yükseklik (kabartma için)

Gözenek dağılımı: çoğunluk 0,25–0,8 mm yarıçap, daha az 0,8–1,6 mm,
seyrek 1,6–2,6 mm. Kenarlar sarmalanır (tekrar sınırı görünmez).
Not: Gerçek kesit fotoğrafı (cut-surface.jpg) gelince renk dokusu
onunla değiştirilmelidir; bu dosya geçici, kurala uygun yer tutucudur.
"""
import os
import sys

import numpy as np
from PIL import Image

N = 2048
SIZE_M = 0.24
PX = SIZE_M / N  # metre / piksel


def stamp_pits(height, rng, count, rmin, rmax, depth_k, power=1.0):
    radii = rmin + (rmax - rmin) * rng.random(count) ** power
    xs = rng.random(count) * N
    ys = rng.random(count) * N
    for r_m, cx, cy in zip(radii, xs, ys):
        r = r_m / PX
        R = int(np.ceil(r)) + 1
        ix = np.arange(int(cx) - R, int(cx) + R + 1)
        iy = np.arange(int(cy) - R, int(cy) + R + 1)
        dx = ix[None, :] + 0.5 - cx
        dy = iy[:, None] + 0.5 - cy
        d2 = dx * dx + dy * dy
        inside = d2 < r * r
        if not inside.any():
            continue
        # küresel çanak profili (yükseklik metre cinsinden, derinlik ∝ yarıçap)
        prof = -np.sqrt(np.clip(r * r - d2, 0, None)) * PX * depth_k
        sub = height[np.ix_(iy % N, ix % N)]
        height[np.ix_(iy % N, ix % N)] = np.minimum(sub, np.where(inside, prof, 0.0))


def fbm(rng, octaves=5, base=8):
    """Döşenebilir değer gürültüsü (FFT ile filtrelenmiş beyaz gürültü)."""
    acc = np.zeros((N, N))
    amp, tot = 1.0, 0.0
    fx = np.fft.fftfreq(N)[None, :]
    fy = np.fft.fftfreq(N)[:, None]
    f = np.sqrt(fx * fx + fy * fy) + 1e-9
    for o in range(octaves):
        cutoff = base * (2 ** o) / N
        spec = np.fft.fft2(rng.standard_normal((N, N))) * np.exp(-(f / cutoff) ** 2)
        layer = np.real(np.fft.ifft2(spec))
        layer /= layer.std() + 1e-9
        acc += amp * layer
        tot += amp
        amp *= 0.5
    return acc / tot


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    rng = np.random.default_rng(1907)
    h = np.zeros((N, N), dtype=np.float64)
    area = SIZE_M * SIZE_M
    # gözenek sayıları alan başına (göz kararı, gerçek kesit fotoğraflarına benzer yoğunluk)
    stamp_pits(h, rng, int(area * 3.0e5), 0.00018, 0.00065, 0.9, power=1.8)
    stamp_pits(h, rng, int(area * 1.2e4), 0.00065, 0.00130, 0.8, power=1.5)
    stamp_pits(h, rng, int(area * 9.0e2), 0.00130, 0.00210, 0.7, power=1.3)

    # ince yüzey pürüzü (kum tanesi) — yüksekliğe çok az katkı
    grain = fbm(rng, octaves=3, base=180)
    h += grain * 0.00004

    pit = np.clip(-h / 0.0006, 0, 1)  # 0 yüzey → 1 derin çukur

    # renk: açık gri, hafif sıcak; çukurlar gölgeli; geniş ölçekte lekelenme
    blot = fbm(rng, octaves=4, base=3)
    speck = rng.random((N, N))
    base = np.array([0.765, 0.762, 0.748])  # sRGB ≈ #bebdb9 (V8: "yüzey 0,47 gri" lineer)
    k = 1.0 - 0.17 * pit ** 1.3
    k *= 1.0 + 0.035 * blot
    k *= 1.0 + np.where(speck > 0.996, 0.10, 0.0) - np.where(speck < 0.003, 0.12, 0.0)
    rgb = np.clip(base[None, None, :] * k[:, :, None], 0, 1)
    Image.fromarray((rgb * 255 + 0.5).astype(np.uint8), 'RGB').save(os.path.join(out_dir, 'gazbeton_renk.png'), optimize=True)

    hn = (h - h.min()) / (h.max() - h.min())
    Image.fromarray((hn * 65535 + 0.5).astype(np.uint16)).save(os.path.join(out_dir, 'gazbeton_yukseklik.png'))
    with open(os.path.join(out_dir, 'gazbeton_yukseklik.txt'), 'w') as f:
        f.write(f'{h.min():.8f} {h.max():.8f} {SIZE_M}\n')
    print('dokular hazir', h.min(), h.max())


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'tex')
