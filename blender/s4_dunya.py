"""
Perde 6 — "Ege'den dünyaya": tepeden Ege bölgesi → küre, İzmir'den 5 kıtaya lime yaylar. Blender 5.0, Cycles.

Kurallar: ülke adı / ülke sınırı / ülke boyalı harita YOK. Yalnız kara noktaları (Natural Earth, kamu malı) ve kıtalar.
Türkiye noktaları lime (marka vurgusu, müşteri onaylı); yaylar, Söke/İzmir iğneleri ve halkaları lime; yay ulaştığında
kıta noktaları yumuşakça sıcak beyaza aydınlanır. Render içinde yazı/rakam yok (kıta etiketleri sitede HTML/SVG).

Plan (docs/plan/akt-s5.json): 193 kare (12 kare/sn), F000–F192.
  bolge (F000–F035)  F000 = s4'ün son karesi (s5 sahibi): tepeden Ege (≈250 km), sabah ışığı (13°, 125°), beyaz-gri kara
                     noktaları, İzmir/Söke lime halka + iğne, İzmir'den halka dalgası; yükselirken nokta aralığı L0→L1→L15,
                     bulut örtüsü geçişi saklar; F022'den Türkiye lime dolar; kürenin doğuşu.
  kure   (F036–F155) küre boylam/eğim dönüşü (Amerika ve Okyanusya ön yüzde); yaylar sırayla Avrupa, Afrika, Amerika, Asya,
                     Okyanusya; varışta kıta jeodezik dalgayla sıcak beyaza yanar; gece yarıda stilize şehir ışıkları.
  cikis  (F156–F192) kamera uzaklaşır, gövde camlaşır (arka yüz ışıkları görünür), küre sağ-ortada durur (F192 = finale ilk karesi).
Veri/zaman: blender/dunya_veri.py, sahne parçaları: blender/dunya_sahne.py.

Kullanım: python s4_dunya.py --variant d|m --frames all|0,40 --out DIR   (önizleme: EGE_PREVIEW=25)
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector, Matrix  # noqa: E402
import dunya_veri as dv  # noqa: E402
import dunya_sahne as ds  # noqa: E402

FRAMES = 193
R = 1.0
IZMIR = dv.IZMIR
SOKE = dv.SOKE
TARGETS = dv.TARGETS
VARIANTS = {
    'd': dict(res=(1600, 900), lens=50.0),
    'm': dict(res=(768, 1366), lens=36.0),
}
KITALAR_NOKTA = (-10.0, 70.0)   # Hint Okyanusu açığı: '5 kıta' kartı noktası (hiçbir kıtaya ait değil)
KUYRUK = 0.18                    # yay kuyruğu (yol oranı)
AKIS_DONGU = 17.0                # damla akış döngüsü (kare): 1,4 sn
ATM_IC, ATM_DIS = 1.6, 0.9      # atmosfer şiddetleri (iç, dış)


def ll2v(lat, lon, r=R):
    la, lo = math.radians(lat), math.radians(lon)
    return Vector((math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))) * r


def globe_rotation(c=None, egim=None):
    """Boylamı c olan meridyen kameraya (−Y) bakacak, kuzey yukarı kalacak dönüş (varsayılan: İzmir).
    egim: kuzey kutbunun kameraya eğimi (derece); egim = enlem verilirse o nokta tam kameraya (nadir) bakar."""
    lat, lon = IZMIR
    if c is not None:
        lon = c
    rz = Matrix.Rotation(math.radians(-90 - lon), 4, 'Z')  # boylam → −Y
    rx = Matrix.Rotation(math.radians(lat * 0.62 if egim is None else egim), 4, 'X')
    return rx @ rz


def ufuk_gorunur(cam_loc, rot, lat, lon, esik=0.08):
    """Küre noktası (lat, lon) kameraya bakan yüzde mi? (ufuk testi: arka yüzdeki çapa null olur)"""
    n = (rot.to_3x3() @ ll2v(lat, lon, 1.0)).normalized()
    return n.dot((cam_loc - rot @ ll2v(lat, lon, R)).normalized()) > esik


# ---------------------------------------------------------------------------
#  Sahne
# ---------------------------------------------------------------------------
class Sahne:
    pass


def build(variant):
    kit.reset()
    ds._NOKTA_GN.clear()
    v = VARIANTS[variant]
    sc = kit.setup_render(*v['res'], samples=ARGS.samples, threshold=0.02)
    sc.cycles.transparent_max_bounces = 14      # bulut + çift atmosfer + ışıma tüpleri üst üste
    S = Sahne()
    S.variant = variant
    S.world = ds.dunya_world()
    S.gunes = ds.gunes_isigi()

    S.govde, S.govde_bsdf = ds.govde()
    # çift atmosfer: iç (ince, mavi-arduvaz) + dış (geniş yumuşak hale); ikisi de gündüz yarıda güçlü
    S.atm_ic, S.atm_ic_n = ds.atmosfer('AtmosferIc', R * 1.028, kit.srgb('#6a93b0'), ATM_IC, 0.232, 0.232, 0.45, 0.20)
    S.atm_dis, S.atm_dis_n = ds.atmosfer('AtmosferDis', R * 1.085, kit.srgb('#5f86b8'), ATM_DIS, 0.388, 0.388, 0.07, 0.28)
    S.bulut, S.bulut_n = ds.bulut_kabugu('Bulut', R * 1.011, olcek=5.0, ege_delik=True)
    S.ortu, S.ortu_n = ds.bulut_kabugu('BulutOrtusu', R * 1.01, olcek=40.0, ege_delik=False)
    S.arka, S.arka_guc = ds.arka_isima()

    # kıta noktaları: dört seviye
    S.sev, S.maxang = dv.seviyeleri_yukle()
    S.dots = {}
    for ad, Sv in S.sev.items():
        rr = dv.SEV[ad]['km'] * dv.KM * dv.SEV[ad]['rmax']
        S.dots[ad] = ds.nokta_nesnesi(Sv, kaldirma=0.45 * rr)

    # yaylar + damla + varış halkaları
    m_cek, m_isi = ds.yay_malzemeleri()
    S.yaylar = [ds.Yay(f'Yay{i}', IZMIR, (T[1], T[2]), m_cek, m_isi) for i, T in enumerate(TARGETS)]
    S.damlalar = [ds.damla(f'Damla{i}') for i in range(len(TARGETS))]
    S.varis = []
    for i, T in enumerate(TARGETS):
        p = ds.halka_birim(f'Varis{i}', 0.10, 6.0, renk=kit.LIME_HI)
        S.varis.append(p)
    # Ege fabrika iğneleri: halka + ince ışık direği (İzmir, Söke)
    S.halka_iz = ds.halka_birim('IzmirHalka', 0.10, 7.0, renk=kit.LIME_HI)
    S.halka_so = ds.halka_birim('SokeHalka', 0.10, 7.0, renk=kit.LIME_HI)
    S.igne_iz = ds.igne('IzmirIgne')
    S.igne_so = ds.igne('SokeIgne')

    # yıldız alanı (kare sürüklenmesi için taban konumlar saklanır)
    S.yildiz = kit.dust('Yildiz', count=900, bounds=((-10, 10), (8, 14), (-6, 6)), seed=23, size=(0.005, 0.013), strength=2.2)
    kit.sinematik(bloom=0.4, esik=1.4, boyut=0.6)
    S.cam = kit.camera('Kamera', lens=v['lens'], loc=(0, -2, 0), target=(0, 0, 0))
    S.cam.data.clip_start = 0.0008
    S.cam.data.clip_end = 200
    S.cam.data.dof.use_dof = False
    return S


def anahtar(F, keys):
    return dv.pchip(F, keys)


def kare_genislik_R(D, lens):
    """Kamera D uzaklıkta iken yüzeydeki kare genişliği (R): 2·tan(yarı FOV)·(D−1)."""
    return 2.0 * (18.0 / lens) * max(D - 1.0, 0.01)


def goruntule(S, f):
    """Kare f için sahneyi ayarlar; hotspot sözlüğünü ve kare bilgilerini döndürür."""
    v = S.variant
    lens = VARIANTS[v]['lens']
    res = VARIANTS[v]['res']
    c = anahtar(f, dv.BOYLAM)
    eg = anahtar(f, dv.EGIM)
    rot = globe_rotation(c, eg)
    rot3 = np.array(rot.to_3x3(), dtype=np.float32)
    D = dv.kam_uzaklik(f, v)
    h = D - 1.0
    cam = S.cam
    cam.location = (0.0, -D, 0.0)
    kit.aim(cam, (0, 0, 0))
    kit.kaydir(cam, v, 1.0)
    fw = kare_genislik_R(D, lens)
    zm = 0.7 + 0.1 * float(np.clip(D, 3.0, 9.0))      # uzaklaştıkça yay/damla kalınlığı büyür (okunsun)
    if v == 'm':
        zm *= 1.3                                       # telefon: yay ve damla ×1,3
    cam_loc = Vector(cam.location)

    # --- ışık: alçak sabah güneşi → sağ-ön
    sun = dv.gunes_yonu(f)
    ds.gunes_yonlendir(S.gunes, sun)
    k_gun = float(dv.sm(dv.sg(f, 0, 30)))
    S.gunes.data.energy = kit.lerp(3.6, 4.6, k_gun)
    S.gunes.data.color = kit.vlerp((1.0, 0.74, 0.48), (1.0, 0.94, 0.86), k_gun)
    S.gunes.data.angle = math.radians(kit.lerp(0.5, 0.9, k_gun))

    # --- gövde (cam evresi: saydamlık 0 → 0,35)
    cam_k = float(dv.sm(dv.sg(f, 156, 167)))
    S.govde_bsdf.inputs['Alpha'].default_value = 1.0 - 0.35 * cam_k
    S.govde.hide_render = False

    # --- atmosfer (çift) — küre açılırken doğar; cam evresinde kenar parıltısı artar; nefes (±%6, 2 sn)
    nefes = 1.0 + 0.06 * math.sin(2 * math.pi * (f - 144) / 24.0) * float(dv.sm(dv.sg(f, 136, 148)))
    atm_k = float(dv.sm(dv.sg(f, 24, 46)))
    kenar = 1.0 + 0.30 * float(dv.sm(dv.sg(f, 160, 176)))
    sx, sy, sz = (float(sun[0]), float(sun[1]), float(sun[2]))
    for ob, nd, g0 in ((S.atm_ic, S.atm_ic_n, ATM_IC), (S.atm_dis, S.atm_dis_n, ATM_DIS)):
        ob.hide_render = atm_k < 0.01
        nd['guc'].default_value = g0 * atm_k * nefes * kenar
        nd['gunes'].inputs[0].default_value, nd['gunes'].inputs[1].default_value, nd['gunes'].inputs[2].default_value = sx, sy, sz

    # --- bulut kabuğu (küre) ve bulut örtüsü (bölge, kameranın önünden geçip L0→L1 geçişini saklar)
    bk = float(dv.sm(dv.sg(f, 30, 48)))
    S.bulut.hide_render = bk < 0.01
    S.bulut.matrix_world = rot @ Matrix.Scale(R * 1.011, 4)
    S.bulut_n['maks'].default_value = 0.42 * bk
    S.bulut_n['harita'].inputs['Rotation'].default_value[2] = math.radians(0.35 * f)     # küreden ayrı hızda kayar
    S.bulut_n['harita'].inputs['Location'].default_value = (0.0, 0.0, 0.004 * f)
    ok_ = float(dv.sm(dv.sg(f, 6, 15)) * (1.0 - dv.sm(dv.sg(f, 19, 29))))
    S.ortu.hide_render = ok_ < 0.01
    ro = R * (1.0 + 0.45 * h)
    S.ortu.matrix_world = rot @ Matrix.Scale(ro, 4)
    S.ortu_n['maks'].default_value = 0.40 * ok_
    S.ortu_n['gurultu'].inputs['Scale'].default_value = float(np.clip(5.5 / max(h, 1e-3) / ro, 6.0, 900.0))
    S.ortu_n['harita'].inputs['Location'].default_value = (0.31 * f / max(h, 0.03) * 0.02, 0.0, 0.0)

    # --- arka ışıma (cam evresi)
    ak = float(dv.sm(dv.sg(f, 150, 176)))
    S.arka.hide_render = ak < 0.01
    S.arka_guc.default_value = 0.30 * ak
    sr = 1.55 * (D + 1.6) / max(D, 1.0)
    S.arka.location = (0, 1.6, 0)
    S.arka.scale = (sr, sr, sr)

    # --- yıldızlar: yavaş sürüklenir, çıkışta parlar
    for ob in S.yildiz:
        bx, by, bz = ob['base']
        ob.location = (bx + 0.006 * f, by, bz + 0.0015 * f)
    S.yildiz[0].data.materials[0].node_tree.nodes['Emission'].inputs['Strength'].default_value = 2.2 * (1.0 + 0.7 * float(dv.sm(dv.sg(f, 156, 180))))
    for ob in S.yildiz:
        ob.hide_render = D < 1.6

    # --- kıta noktaları
    for ad, Sv in S.sev.items():
        ob = S.dots[ad]
        kz = dv.seviye_zaman(ad, f)
        if kz <= 0.004:
            ob.hide_render = True
            continue
        ob.hide_render = False
        ob.matrix_world = rot
        P = (Sv.u @ rot3.T)                                             # dünya yönü (n,3)
        camv = np.array(cam_loc, dtype=np.float32)[None, :] - P         # kamera − nokta
        mesafe = np.linalg.norm(camv, axis=1) + 1e-9
        ndv = np.einsum('ij,ij->i', P, camv) / mesafe
        col, glow = dv.boya(Sv, f, rot3, sun, ndv, arka_zayif=cam_k, nefes=nefes)
        rr = dv.seviye_yaricap(ad, fw)
        if v == 'm':
            rr *= 1.25
        ol = rr * kz * (0.88 + 0.24 * Sv.jit)
        if cam_k > 0:   # cam gövde: arka yüz noktaları da çizilir (zayıf), ufuk gerisi
            vis = (ndv > -1.0).astype(np.float32)
            ol = ol * (0.75 + 0.25 * (ndv > -0.02))
        else:
            vis = (ndv > -0.035).astype(np.float32)
        if ad != 'L2' or D < 1.5:   # bölge/L1/L15: görüş alanı dışını ele (ışın sayısı azalsın)
            depth = P[:, 1] + D
            x = P[:, 0] / np.maximum(depth, 1e-6)
            y = P[:, 2] / np.maximum(depth, 1e-6)
            tw = 18.0 / lens
            th = tw * res[1] / res[0]
            vis = vis * ((depth > 1e-4) & (np.abs(x) < tw * 1.30) & (np.abs(y) < th * 1.30)).astype(np.float32)
        ds.nokta_guncelle(ob, col, glow, ol * vis)

    # --- yaylar (çift eğri: çekirdek + ışıma), kuyruk, damla (ilk uçuş + sonrasında akış), varış halkaları
    izf = 1.0 - 0.4 * float(dv.sm(dv.sg(f, 156, 167))) - 0.1 * float(dv.sm(dv.sg(f, 168, 179)))   # çıkışta izler %50'ye soluyor
    for i, (kid, lat, lon, fa, fb, fw_) in enumerate(TARGETS):
        yay = S.yaylar[i]
        dm = S.damlalar[i]
        u = kit.seg(f, fa, fb)
        ue = kit.ease_in_out(u)
        bas = None
        iz_son = 0.0
        gor = f > fa
        if f > fa:
            if f < fb:
                iz_son, bas = ue, ue
            else:
                iz_son = 1.0
                baslangic = fb + 8
                if f >= baslangic:
                    ph = ((f - baslangic) / AKIS_DONGU + i * 0.23) % 1.0
                    bas = ph * (1.0 + KUYRUK)
        kfl = 1.0 if f < fb else (0.35 + 0.65 * float(dv.sm(dv.sg(f, 100, 132))))
        if f >= fb:
            # akış gücü: ilk uçuştan sonra sakin, F132'de tam
            pass
        yay.guncelle(iz_son, bas, KUYRUK, 0.0016 * zm, 0.0034 * zm, 0.012 * zm, 3.0 * izf, 14.0 * (1.0 if f < fb else kfl), gorunur=gor)
        # damla: yay başı
        b, g = dm
        gb = (bas is not None) and (0.004 < bas < 0.998)
        b.hide_render = not gb
        g.hide_render = not gb
        if gb:
            p = rot @ Vector(tuple(float(x) for x in yay.konum(bas)))
            fk = 1.0 if f < fb else kfl
            b.location = p
            g.location = p
            rb = 0.0058 * zm * (0.7 + 0.3 * fk)
            b.scale = (rb, rb, rb)
            rg = 0.021 * zm * (0.6 + 0.4 * fk)
            g.scale = (rg, rg, rg)
        yay.cek.matrix_world = rot
        yay.isi.matrix_world = rot
        # varış halkası (kıtada dışa açılan lime halka)
        pr = kit.seg(f, fb - 1, fb + 11)
        hl = S.varis[i]
        hl.hide_render = not (0 < pr < 1)
        if 0 < pr < 1:
            rad = 0.035 * (0.5 + 2.0 * pr) * max(1.0, 0.8 * zm)
            hl.matrix_world = ds.yerel_matris(rot, lat, lon, 0.5 * rad * rad + 0.003) @ Matrix.Diagonal((rad, rad, 1.0, 1.0))
            hl.data.materials[0].node_tree.nodes['Emission'].inputs['Strength'].default_value = 6.5 * (1 - pr) ** 1.3

    # --- Ege iğneleri: halka + ışık direği (F000–F040), Türkiye lime dolarken sönerler
    ks = 1.0 - float(dv.sm(dv.sg(f, 22, 40)))
    nab = 1.0 + 0.16 * math.sin(2 * math.pi * f / 12.0)
    for (hl, ig, (lat, lon), gecik) in ((S.halka_iz, S.igne_iz, IZMIR, 0), (S.halka_so, S.igne_so, SOKE, 4)):
        hl.hide_render = ks < 0.01
        ig.hide_render = ks < 0.01
        if ks < 0.01:
            continue
        rad = (0.0010 + 0.0025 * float(dv.sm(dv.sg(f, 0, 24)))) * nab
        hl.matrix_world = ds.yerel_matris(rot, lat, lon, 0.5 * rad * rad + 0.02 * rad) @ Matrix.Diagonal((rad, rad, 1.0, 1.0))
        hl.data.materials[0].node_tree.nodes['Emission'].inputs['Strength'].default_value = 8.0 * ks * (0.85 + 0.3 * (nab - 0.84) / 0.32)
        hp = min(0.14 * h, 0.09)
        rp = 0.0022 * fw
        ig.matrix_world = ds.yerel_matris(rot, lat, lon, 0.0) @ Matrix.Diagonal((rp, rp, hp, 1.0))
        ds.igne_guc(ig, ks)

    # --- kamera izdüşümü: tıklanır noktalar (ufuk testiyle)
    cam.data.dof.use_dof = False
    pts_w = {}
    if f <= 60:
        if ufuk_gorunur(cam_loc, rot, *IZMIR):
            pts_w['kaynak'] = rot @ ll2v(IZMIR[0], IZMIR[1], R * 1.003)
        if ufuk_gorunur(cam_loc, rot, *SOKE):
            pts_w['soke'] = rot @ ll2v(SOKE[0], SOKE[1], R * 1.003)
    if f >= 125 and ufuk_gorunur(cam_loc, rot, *KITALAR_NOKTA):
        pts_w['kitalar'] = rot @ ll2v(KITALAR_NOKTA[0], KITALAR_NOKTA[1], R * 1.01)
    for (kid, lat, lon, fa, fb, fw_), ad in zip(TARGETS, dv.AD):
        if f >= fb and ufuk_gorunur(cam_loc, rot, lat, lon):
            pts_w['v_' + ad] = rot @ ll2v(lat, lon, R * 1.01)
    hs = {}
    if pts_w:
        bpy.context.view_layer.update()
        proj = kit.project(cam, list(pts_w.values()))
        hs = {k: p for k, p in zip(pts_w.keys(), proj) if p}
    return hs, dict(D=round(D, 4), h_km=round(h * 6371.0, 1), c=round(c, 2), egim=round(eg, 2))


def main():
    os.makedirs(ARGS.out, exist_ok=True)
    S = build(ARGS.variant)
    frames = pass_order(FRAMES) if ARGS.frames == 'all' else [int(x) for x in ARGS.frames.split(',')]
    meta_path = os.path.join(ARGS.out, 'meta.json')
    meta = {'_n': FRAMES, 'frames': FRAMES, 'res': VARIANTS[ARGS.variant]['res'], 'hotspots': {}}
    if os.path.exists(meta_path):  # kısmi işler (kaba/ara/ince geçiş) birbirinin noktalarını silmesin
        _eski = json.load(open(meta_path, encoding='utf-8'))
        if _eski.get('frames') == FRAMES:
            meta['hotspots'].update(_eski.get('hotspots', {}))
    for f in frames:
        path = os.path.join(ARGS.out, f'{f:03d}.png')
        t0 = time.time()
        hs, info = goruntule(S, f)
        meta['hotspots'][str(f)] = hs
        if ARGS.skip_existing and os.path.exists(path):
            continue
        t1 = time.time()
        c1 = time.process_time()
        kit.render_to(path)
        print(f'KARE {f} {time.time() - t1:.1f}s cpu {time.process_time() - c1:.0f}s (hazırlık {t1 - t0:.1f}s) {info}', flush=True)
        kit.write_json(meta_path, meta)
    kit.write_json(meta_path, meta)


def pass_order(n):
    order, seen = [], set()
    min_step = int(os.environ.get('EGE_MINSTEP', '1'))
    for step in [x for x in (8, 4, 2, 1) if x >= min_step]:
        for f in range(0, n, step):
            if f not in seen:
                seen.add(f)
                order.append(f)
    # son kare (sahnenin "sonuç" karesi) ilk kareden hemen sonra: erken teslimde de var olsun
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
    ap.add_argument('--skip-existing', action='store_true')
    ARGS = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    main()
