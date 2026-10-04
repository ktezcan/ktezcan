/**
 * Finale (son bölüm) kanvas katmanı kayıt noktası: s5'in son karesi üzerine 2B efektler (küre → Ege'de kıvılcım → logo çizgisi).
 * Bu dosya finale işi yapılırken doldurulur; motor (main.js/sahne.js) yalnızca bu arayüzü çağırır:
 *   const f = finalKur(ortak);  f.konumla(p /*0..1 finale ilerlemesi*/); f.ciz(ctx, w, h, p);
 */
export function finalKur(/* ortak */) {
  return {
    konumla() {},
    ciz() {},
  };
}
