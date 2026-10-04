# Oynatıcı/motor + paketleme — kalan işler

Durum: oynatıcı (7 parça, GECIS=0, pencereli bellek, seyrek set erimesi), `kareler.py` (bütçe, seyrek set, poster, `res`/`pen` meta), `dikis_kopyala.py`, `teslim.sh` (iki zip) ve `sinama.mjs` yer tutucu karelerle (tam + `--adim 8 --yarim` seyrek, http + file://) sınandı: konsol hatası yok, harici istek yok, depolama yok, kanvas DPR ≤ 1,25, normal hızlı sarma ≥ 50 fps, teslim zip'i açılıp file:// ile çalışıyor.

Ölçümler (yer tutucu kare, başsız Chromium, makine paylaşımlı): masaüstü 1600×900 çözülmüş kare tepe ≈ 0,65 GB (eski ≈ 2,9 GB), dikey telefon ≈ 0,35 GB; ilk boyama < 0,2 sn; normal sarma 51–59 fps (makine yüküne göre), uç hızlı sarma (~320 vh/sn) 40–58 fps.

## Yetişmeyenler / dikkat

1. **Gerçek karelerle bütçe**: yer tutucu kareler düz renk olduğundan WebP boyutları gerçek değil. Gerçek render gelince `tools/teslim.sh` bütçe raporunu (`butce-raporu_*.txt`) kontrol et: toplam ≤ 100 MB değilse kalite otomatik 4'er puan düşer (s5 baştan q≈70); en düşük q=50 de yetmezse rapor UYARI verir.
2. **Dikiş kopyaları**: `blender/spec/*.json` içinde henüz `"kopya"` girdisi yok (klasör boş). Sahne ajanları girdileri yazınca `dikis_kopyala.py` çalışır; girdi yoksa dikişte sıçrama olur. `sinama.mjs` (http kipi) dikişleri görüntü farkıyla denetler (eşik 12); gerçek karelerle yeniden çalıştır.
3. **file:// dikiş denetimi**: file:// kipinde kanvas piksel okuması engellenir, dikiş görüntü denetimi yalnız http kipinde yapılır (sınama tek uyarı verir).
4. **Gerçek cihaz sınaması**: başsız Chromium yazılımsal çizer; gerçek GPU'lu masaüstü, Android orta sınıf ve iOS Safari'de fps/bellek ölçülmeli (özellikle `createImageBitmap` küçültme seçenekleri; desteklenmezse kod tam çözüme düşer).
5. **Derlenmiş çıktılar**: depodaki `giris-hikaye/assets/js/hikaye.js`, `canli.js`, `kareler-meta.js` eski olabilir; `teslim.sh` (ya da `derle.mjs` + `kareler.py`) her seferinde yeniden üretir. Sahip ajanlar commit etmedi.
6. **Daha düşük bellek istenirse**: `ayarlar.js` içinde `PENCERE` (16) ve `KOMSU_KARE` (12) küçültülür; her kare masaüstünde ≈ 5,8 MB.
7. `src/hikaye/homografi.js` kullanılmıyor (eski video-yüzü yaklaşımı); istenirse silinebilir.
