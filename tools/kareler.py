"""
Render karelerini web'e hazırlar:
  PNG → WebP (giris-hikaye/kareler/<sahne>/<d|m>/NNN.webp), sahne posteri (her sahne için),
  ve tüm metaları (kare sayısı, MEVCUT kare indeksleri, video yüzü köşeleri, kalem ucu, tıklanır noktalar)
  tek bir klasik betikte toplar: giris-hikaye/assets/js/kareler-meta.js
  (fetch gerekmez → maket file:// ile de çalışır).

Boyut bütçesi: tam paketin (tüm kareler) toplamı --butce-mb'yi (varsayılan 100 MB) aşmasın diye kalite, örnek kareler
kodlanarak ölçülür ve gerekirse sahne sahne düşürülür (s5 baştan 10 puan düşüktür: q≈70). Seyrek set (render sürerken
her 8. kare vb.) desteklenir: yalnız var olan kareler kodlanır, meta 'mevcut' listesi oynatıcıya bunu bildirir.
Render yarım çözünürlükte olabilir: meta 'res' tam çözünürlük sayılır, oynatıcı kanvasa ölçekler; karelere dokunulmaz.

Kullanım: python tools/kareler.py <render_kök> [kalite] [--site giris-hikaye] [--butce-mb 100] [--isci 4] [--nice 5] [--rapor dosya]
  kalite: temel WebP kalitesi (varsayılan 80)
"""
import argparse
import io
import json
import os
import shutil
import sys
from multiprocessing import Pool

from PIL import Image

KOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SAHNELER = ['s0', 's1', 's2', 's3', 's4', 's5']
SAHNE_KALITE_FARKI = {'s5': -10}  # s5 (dünya, çok ince nokta dokusu) daha düşük kalitede de temiz kalır: q≈70
KALITE_MIN = 50
POSTER_ENBOY = 960
NOTR = (12, 22, 28)  # kare olmayan sahne için koyu poster (404 çıkmasın)


def yuvarla(o, n=4):
    if isinstance(o, float):
        return round(o, n)
    if isinstance(o, list):
        return [yuvarla(x, n) for x in o]
    if isinstance(o, dict):
        return {k: yuvarla(v, n) for k, v in o.items()}
    return o


def tam_kume(n, var):
    """Tam paketteki kare indeksleri: d hepsi, m her 2. kare + son (render_kuyruk.py ile aynı kural)."""
    if var == 'd':
        return set(range(n))
    return set(range(0, n, 2)) | {n - 1}


def png_listesi(src):
    """Klasördeki NNN.png dosyaları: [(indeks, yol)] sıralı."""
    out = []
    for name in os.listdir(src):
        if name.endswith('.png') and name[:-4].isdigit():
            out.append((int(name[:-4]), os.path.join(src, name)))
    return sorted(out)


def isci_baslat(nice):
    if nice:
        try:
            os.nice(nice)
        except OSError:
            pass


def kodla(gorev):
    """(png, webp, kalite) → (webp, bayt) ya da None (yazılmakta olan kare)."""
    png, webp, kalite = gorev
    try:
        im = Image.open(png)
        im.load()
    except Exception:
        return None
    im.convert('RGB').save(webp, 'WEBP', quality=kalite, method=6)
    return webp, os.path.getsize(webp)


def ornek_bayt(png, kalite):
    """Bir PNG'nin WebP boyutu (bayt), diske yazmadan."""
    try:
        im = Image.open(png)
        im.load()
    except Exception:
        return None
    b = io.BytesIO()
    im.convert('RGB').save(b, 'WEBP', quality=kalite, method=6)
    return b.tell()


def kume_kalitesi(sid, taban, dusus):
    return max(KALITE_MIN, min(95, taban + SAHNE_KALITE_FARKI.get(sid, 0) - dusus))


def tahmin(kumeler, ornekler, taban, dusus):
    """Tam paket tahmini (bayt): her küme için örnek kare ortalaması × tam kare sayısı."""
    top = 0
    for k in kumeler:
        q = kume_kalitesi(k['sid'], taban, dusus)
        anahtar = (k['sid'], k['var'], q)
        if anahtar not in ornekler:
            ks = k['pngs']
            adet = min(3, len(ks))
            sec = [ks[round(j * (len(ks) - 1) / max(1, adet - 1))][1] for j in range(adet)]
            olc = [b for b in (ornek_bayt(p, q) for p in sec) if b]
            ornekler[anahtar] = sum(olc) / len(olc) if olc else 0
        tam = max(len(tam_kume(k['n'], k['var'])), len(k['pngs']))
        top += ornekler[anahtar] * tam
    return top


def main():
    ap = argparse.ArgumentParser(description='Render karelerini WebP + meta olarak web klasörüne hazırlar')
    ap.add_argument('render_kok')
    ap.add_argument('kalite', nargs='?', type=int, default=80)
    ap.add_argument('--site', default=os.environ.get('EGE_SITE') or os.path.join(KOK, 'giris-hikaye'))
    ap.add_argument('--butce-mb', type=float, default=100, help='tam paket hedefi (MB); 0 = sınırsız')
    ap.add_argument('--isci', type=int, default=min(4, os.cpu_count() or 2))
    ap.add_argument('--nice', type=int, default=5)
    ap.add_argument('--rapor', default='')
    a = ap.parse_args()
    hedef = os.path.join(a.site, 'kareler')
    meta_js = os.path.join(a.site, 'assets', 'js', 'kareler-meta.js')

    # 1) kümeleri tara: render kökünde <sahne><d|m>/ + meta.json olanlar
    kumeler = []
    for sid in SAHNELER:
        for var in ('d', 'm'):
            src = os.path.join(a.render_kok, f'{sid}{var}')
            meta_p = os.path.join(src, 'meta.json')
            if not os.path.isdir(src) or not os.path.exists(meta_p):
                # kaynağı kalmamış (yeniden render için kenara alınmış) eski set pakete girmesin
                eski = os.path.join(hedef, sid, var)
                if os.path.isdir(eski):
                    shutil.rmtree(eski)
                continue
            pngs = png_listesi(src)
            if not pngs:
                continue
            meta = json.load(open(meta_p, encoding='utf-8'))
            kumeler.append({'sid': sid, 'var': var, 'src': src, 'meta': meta, 'pngs': pngs, 'n': int(meta['frames'])})

    # 2) kalite bütçesi: tam paket tahmini bütçeyi aşıyorsa kaliteyi 4'er puan düşür
    ornekler = {}
    dusus = 0
    butce = a.butce_mb * 1048576
    tahmini = tahmin(kumeler, ornekler, a.kalite, 0) if kumeler else 0
    if butce > 0:
        while tahmini > butce and any(kume_kalitesi(k['sid'], a.kalite, dusus) > KALITE_MIN for k in kumeler):
            dusus += 4
            tahmini = tahmin(kumeler, ornekler, a.kalite, dusus)

    # 3) kodlama görevleri (kalite değiştiyse ya da PNG yenisiyse); çok işlemli
    gorevler = []
    for k in kumeler:
        out = os.path.join(hedef, k['sid'], k['var'])
        os.makedirs(out, exist_ok=True)
        q = kume_kalitesi(k['sid'], a.kalite, dusus)
        k['q'] = q
        k['out'] = out
        isaret = os.path.join(out, '.kalite')
        eski_k = open(isaret).read().strip() if os.path.exists(isaret) else ''
        yeniden = eski_k != str(q)
        for i, png in k['pngs']:
            webp = os.path.join(out, f'{i:03d}.webp')
            if yeniden or not os.path.exists(webp) or os.path.getmtime(webp) < os.path.getmtime(png):
                gorevler.append((png, webp, q))
    if gorevler:
        if a.isci > 1 and len(gorevler) > 4:
            with Pool(a.isci, initializer=isci_baslat, initargs=(a.nice,)) as havuz:
                havuz.map(kodla, gorevler, chunksize=4)
        else:
            for g in gorevler:
                kodla(g)

    # 4) meta, posterler, rapor
    hepsi = {}
    satirlar = []
    toplam_bayt = 0
    for k in kumeler:
        sid, var, out = k['sid'], k['var'], k['out']
        mevcut = []
        bayt = 0
        for i, png in k['pngs']:
            webp = os.path.join(out, f'{i:03d}.webp')
            if os.path.exists(webp) and os.path.getsize(webp) > 0:  # yazılmakta olan kare atlanmış olabilir
                mevcut.append(i)
                bayt += os.path.getsize(webp)
        with open(os.path.join(out, '.kalite'), 'w') as f:
            f.write(str(k['q']))
        # render klasöründe karşılığı kalmayan eski kareleri sil (pakete girmesin)
        for name in os.listdir(out):
            if name.endswith('.webp') and int(name[:-5]) not in mevcut:
                os.remove(os.path.join(out, name))
        if not mevcut:
            continue
        meta = k['meta']
        gercek = Image.open(k['pngs'][0][1]).size
        res = meta.get('res') or list(gercek)
        if abs(res[0] / res[1] - gercek[0] / gercek[1]) > 0.01:  # en-boy oranı tutmuyorsa karenin kendisine güven
            res = list(gercek)
        ent = {'n': k['n'], 'res': res, 'mevcut': sorted(mevcut)}
        if 'face' in meta:
            ent['face'] = yuvarla(meta['face'])
        if 'pen' in meta:  # kalem ucu konumu (eskiz çizimi): sitedeki kalem sprite'ı
            ent['pen'] = yuvarla(meta['pen'])
        if 'hotspots' in meta:
            ent['hotspots'] = {kk: v for kk, v in yuvarla(meta['hotspots']).items() if v}
        hepsi.setdefault(sid, {})[var] = ent
        toplam_bayt += bayt
        tam = max(len(tam_kume(k['n'], var)), len(mevcut))
        ort = bayt / len(mevcut)
        seyrek = 'tam' if len(mevcut) >= tam else f'seyrek ({len(mevcut)}/{tam})'
        satirlar.append((f'{sid}{var}', len(mevcut), k['n'], seyrek, k['q'], ort / 1024, bayt / 1048576, ort * tam / 1048576))

    # poster: masaüstü dizisinin ilk karesi (yoksa telefonun); en uzun kenar POSTER_ENBOY
    for sid in SAHNELER:
        pdir = os.path.join(hedef, sid)
        os.makedirs(pdir, exist_ok=True)
        kay = None
        for v in ('d', 'm'):
            if v in hepsi.get(sid, {}):
                kay = next(k for k in kumeler if k['sid'] == sid and k['var'] == v)
                break
        if kay:
            im = Image.open(kay['pngs'][0][1]).convert('RGB')
            im.thumbnail((POSTER_ENBOY, POSTER_ENBOY), Image.LANCZOS)
        else:
            im = Image.new('RGB', (POSTER_ENBOY, POSTER_ENBOY * 9 // 16), NOTR)
        im.save(os.path.join(pdir, 'poster.webp'), 'WEBP', quality=70, method=6)

    os.makedirs(os.path.dirname(meta_js), exist_ok=True)
    with open(meta_js, 'w', encoding='utf-8') as f:
        f.write('/* Otomatik üretilir: tools/kareler.py — elle düzenlemeyin */\n')
        f.write('window.EGE_KARELER=' + json.dumps(hepsi, ensure_ascii=False, separators=(',', ':')) + ';\n')

    rapor = ['küme   kare  /n     set            q   ort KB   set MB   tam paket MB']
    for ad, say, n, seyrek, q, ort, mb, tam_mb in satirlar:
        rapor.append(f'{ad:<6} {say:>4} / {n:<4} {seyrek:<14} {q:>3} {ort:>8.1f} {mb:>8.2f} {tam_mb:>10.1f}')
    rapor.append(f'şu an pakette: {toplam_bayt / 1048576:.1f} MB; tam paket tahmini: {tahmini / 1048576:.1f} MB; bütçe: '
                 + (f'{a.butce_mb:.0f} MB' if a.butce_mb else 'yok') + f'; kalite düşüşü: -{dusus}')
    if butce > 0 and tahmini > butce:
        rapor.append(f'UYARI: tam paket tahmini bütçeyi aşıyor (en düşük kalite q={KALITE_MIN} de yetmedi)')
    metin = '\n'.join(rapor)
    print(metin)
    if a.rapor:
        with open(a.rapor, 'w', encoding='utf-8') as f:
            f.write(metin + '\n')
    print('kareler hazır:', sum(s[1] for s in satirlar), 'kare,', f'{len(gorevler)} kare (yeniden) kodlandı')


if __name__ == '__main__':
    sys.exit(main())
