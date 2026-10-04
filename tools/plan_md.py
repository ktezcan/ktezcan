"""docs/plan/*.json (saniye saniye hikâye planı) → docs/HIKAYE_PLANI.md (okunabilir belge).
Kullanım: python tools/plan_md.py [docs/plan] [çıktı.md]"""
import json
import os
import sys

KOK = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'docs', 'plan')
CIKTI = sys.argv[2] if len(sys.argv) > 2 else os.path.join(KOK, '..', 'HIKAYE_PLANI.md')
SIRA = ['s0', 's1', 's2', 's3', 's4', 's5', 'son']
AD = {'s0': 'Hayalden yuvaya', 's1': 'Ürün turu', 's2': 'Doğuş', 's3': 'Gözenek', 's4': 'Yol', 's5': 'Dünya', 'son': 'Finale'}


def yukle(ad):
    return json.load(open(os.path.join(KOK, ad + '.json'), encoding='utf-8'))


def kisalt(s, n):
    s = str(s).strip()
    return s if len(s) <= n else s[:n].rsplit(' ', 1)[0] + ' …'


def gen(v, d=0, n=700):
    """Serbest biçimli JSON değerini madde imli metne çevirir."""
    pad = '  ' * d
    out = []
    if isinstance(v, dict):
        for k, x in v.items():
            if isinstance(x, (dict, list)):
                out.append(f'{pad}- **{k}**:')
                out += gen(x, d + 1, n)
            else:
                out.append(f'{pad}- **{k}**: {kisalt(x, n)}')
    elif isinstance(v, list):
        for x in v:
            if isinstance(x, (dict, list)):
                out += gen(x, d, n) if isinstance(x, list) else [f'{pad}-'] + gen(x, d + 1, n)
            else:
                out.append(f'{pad}- {kisalt(x, n)}')
    else:
        out.append(f'{pad}{kisalt(v, n)}')
    return out


def sn(t):
    return f'{t // 60}:{t % 60:02d}'


akt = {k: yukle('akt-' + k) for k in SIRA}
mod = yukle('moduller')
paz = yukle('pazarlama')
L = []
w = L.append

w('# Ege Gazbeton giriş hikâyesi — saniye saniye plan')
w('')
w('Bu belge `docs/plan/*.json` dosyalarından `tools/plan_md.py` ile üretilir (JSON kaynaktır; belgeyi elle değiştirmeyin).')
w('')
w('**Okuma kılavuzu.** Hikâye 146 film saniyesidir (2:26). 1 saniye = 22 vh kaydırma (referans hız); toplam 3212 vh. '
  'Her saniye bir blok: görsel, efekt, ekran metni (TR/EN), rakam ve kaynağı, etkileşim, pazarlama rolü, üretim ve maliyet. '
  'Her perdenin son 3 saniyesi bir sonraki perdeye geçiştir; sonraki perde o görüntüyle birebir başlar.')
w('')
w('## 1. Genel yapı')
w('')
w('| Perde | Süre | Saniye | vh | Amaç |')
w('|---|---|---|---|---|')
for k in SIRA:
    a = akt[k]
    w(f"| **{k} · {a['baslik']}** | {a['t_son'] - a['t_bas']} sn | {a['t_bas']}–{a['t_son']} ({sn(a['t_bas'])}–{sn(a['t_son'])}) | {a['t_bas'] * 22}–{a['t_son'] * 22} | {kisalt(a['amac'], 260)} |")
w('')
w('Tempo eğrisi: duygu %22 (0–32 sn) → kanıt %49 (32–104) → güç %22 (104–136) → eylem %7 (136–146).')
w('')

w('## 2. Senin kararına bırakılanlar')
w('')
for k in SIRA:
    for q in akt[k].get('acik_sorular', []):
        w(f'- **{k}** — {q}')
for q in mod.get('acik_sorular', []):
    w(f'- **modüller** — {q if isinstance(q, str) else json.dumps(q, ensure_ascii=False)}')
for q in paz.get('acik_sorular', []):
    w(f'- **pazarlama** — {q if isinstance(q, str) else json.dumps(q, ensure_ascii=False)}')
w('')

w('## 3. Saniye saniye plan')
ALAN = [('gorsel', 'Görsel'), ('efekt', 'Efekt'), ('rakam', 'Rakam · kaynak'), ('etkilesim', 'Etkileşim'),
        ('pazarlama', 'Pazarlama'), ('uretim', 'Üretim'), ('mobil', 'Telefon'), ('risk', 'Risk')]
for k in SIRA:
    a = akt[k]
    w('')
    w(f"### {k} · {a['baslik']} — {a['t_bas']}–{a['t_son']} sn")
    w('')
    w(f"**Amaç.** {a['amac']}")
    w('')
    for r in a['satirlar']:
        w(f"#### t={r['t']} ({sn(r['t'])}) · {r['vh']} vh · p={r['p']}")
        if r.get('kare'):
            w(f"- **Kare:** {r['kare']}")
        for f, ad in ALAN[:1]:
            if r.get(f):
                w(f'- **{ad}:** {r[f]}')
        if r.get('metin_tr') or r.get('metin_en'):
            w(f"- **Metin:** {r.get('metin_tr', '')}" + (f"  \n  *EN:* {r['metin_en']}" if r.get('metin_en') else ''))
        for f, ad in ALAN[1:]:
            if r.get(f):
                w(f'- **{ad}:** {r[f]}')
    w('')
    w(f'**Geçiş ve üretim notu ({k}).** {a["gecis_notu"]}')
    if a.get('yeni_isler'):
        w('')
        w(f'**Gereken yeni işler ({k}):**')
        for i in a['yeni_isler']:
            w(f'- {i}')

w('')
w('## 4. Etkileşimli ve öğretici modüller')
w('')
w(f"{mod.get('aciklama', '')}")
w('')
sirasi = {m: i for i, m in enumerate(mod.get('oncelik_sirasi', []))}
for m in sorted(mod['moduller'], key=lambda m: sirasi.get(m['id'], 99)):
    w(f"### {m['ad']} (`{m['id']}`) — efor: {m.get('efor', '?')}")
    for f, ad in (('nerede', 'Nerede'), ('ne_yapar', 'Ne yapar'), ('ogretici_deger', 'Öğretici değer'),
                  ('pazarlama_degeri', 'Pazarlama değeri'), ('veri_ve_kaynak', 'Veri ve kaynak'), ('teknik', 'Teknik'),
                  ('tr_metin', 'TR metin'), ('en_metin', 'EN metin'), ('kural_riski', 'Kural riski')):
        v = m.get(f)
        if v:
            w(f'- **{ad}:** {v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)}')
    w('')
if mod.get('dogrulanamayanlar'):
    w('**Doğrulanamayanlar (ekranda kullanılmaz / teyit gerekli):**')
    w('')
    for x in gen(mod['dogrulanamayanlar'], 0, 400):
        w(x)
    w('')

w('## 5. Pazarlama ve dönüşüm akışı')
w('')
w(f"{paz.get('ozet', '')}")
w('')
w('### Huni')
for h in paz.get('huni', []):
    w(f"- **{h.get('asama')}** ({h.get('t_bas')}–{h.get('t_son')} sn, %{h.get('film_payi_yuzde')}): {h.get('ana_mesaj', '')} — izleyici: {h.get('izleyici_hissi', '')}")
w('')
w('### Kitle yolları')
for y in paz.get('kitle_yollari', []):
    hc = y.get('hero_cipi', {})
    w(f"- **{y.get('ad')}** — çip: “{hc.get('tr', '')}” → `{hc.get('baglanti', '')}`")
    for x in y.get('ne_arar', [])[:3]:
        w(f'  - arar: {x}')
w('')
w('### CTA zaman çizelgesi')
w('')
w('| Saniye | Yer | Metin (TR) | Bağlantı |')
w('|---|---|---|---|')
for c in paz.get('cta_zaman_cizelgesi', []):
    w(f"| {c.get('t')}–{c.get('t_son')} | {kisalt(c.get('yer', ''), 90)} | {c.get('metin_tr', '')} | `{c.get('baglanti', '')}` |")
w('')
w(f"**Bağlantı şeması.** {paz.get('baglanti_semasi', '')}")
w('')
for baslik, anahtar in (('Güven işaretleri', 'guven_isaretleri'), ('Ölçüm', 'olcum'), ('Marka görünürlüğü', 'marka_gorunurlugu'),
                        ('SEO ve paylaşım', 'seo_paylasim'), ('Mobil', 'mobil')):
    w(f'### {baslik}')
    for x in gen(paz.get(anahtar, []), 0, 500):
        w(x)
    w('')
w('### İlk 10 saniye testi')
w('')
w(str(paz.get('ilk_10_sn', '')))
w('')

os.makedirs(os.path.dirname(os.path.abspath(CIKTI)), exist_ok=True)
open(CIKTI, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print(CIKTI, len(L), 'satır')
