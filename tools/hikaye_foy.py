"""
Hikâye föyü: her sahneden seçilmiş kareleri, sahne adı ve kısa açıklamayla
tek bir dikey görselde toplar (telefonda bakmak için). Sahne başına birden
çok kare verilirse yan yana dizilir (giriş → gelişme → sonuç).

Kullanım: python tools/hikaye_foy.py <render_kök> <çıktı.jpg> s0:0,30,59 s1:8,48,88 ...
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ADLAR = {
    's0': ('0 · BLOK', 'Video bloğun ön yüzüne küçülür, blok döner'),
    's1': ('1 · ÜRETİM', 'Hammaddeler kaidelerde → girdap → kabarma → tel kesim'),
    's2': ('2 · YAPI', 'Gözeneğe dalış: kapalı hava hücresi, numune küpü'),
    's3': ('3 · SİSTEM', 'Apartman doğru sırayla: karkas → duvar → lento → çatı'),
    's4': ('4 · DÜNYA', "Söke/İzmir'den 5 kıtaya · 25+ ülke"),
}
F_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F_R = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def main(kok, cikti, secimler):
    W = 1200
    gap = 6
    rows = []
    for sec in secimler:
        sid, kareler = sec.split(':')
        ims = []
        for k in kareler.split(','):
            p = os.path.join(kok, f'{sid}d', f'{int(k):03d}.png')
            if os.path.exists(p):
                ims.append(Image.open(p).convert('RGB'))
        if not ims:
            continue
        n = len(ims)
        w = (W - gap * (n - 1)) // n
        ims = [im.resize((w, int(w * im.height / im.width)), Image.LANCZOS) for im in ims]
        rows.append((sid, ims))
    if not rows:
        print('kare yok')
        return
    bh = 64
    H = sum(bh + max(im.height for im in ims) for _, ims in rows) + gap * len(rows)
    sheet = Image.new('RGB', (W, H), (12, 22, 28))
    d = ImageDraw.Draw(sheet)
    fb = ImageFont.truetype(F_B, 30)
    fr = ImageFont.truetype(F_R, 22)
    y = 0
    for sid, ims in rows:
        ad, aciklama = ADLAR.get(sid, (sid, ''))
        d.rectangle([24, y + 18, 30, y + 46], fill=(162, 191, 55))
        d.text((44, y + 16), ad, font=fb, fill=(255, 255, 255))
        d.text((44 + d.textlength(ad, font=fb) + 24, y + 22), aciklama, font=fr, fill=(201, 211, 217))
        y += bh
        x = 0
        for im in ims:
            sheet.paste(im, (x, y))
            x += im.width + gap
        y += max(im.height for im in ims) + gap
    sheet.save(cikti, quality=86)
    print('föy:', cikti, sheet.size)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
