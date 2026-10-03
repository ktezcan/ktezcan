/**
 * Dört köşe eşlemesi → CSS matrix3d (projektif dönüşüm).
 * Video öğesini, render edilmiş bloğun ön yüzüne piksel piksel oturtmak için.
 * Öğe transform-origin: 0 0 olmalı.
 */
function adj(m) {
  return [
    m[4] * m[8] - m[5] * m[7], m[2] * m[7] - m[1] * m[8], m[1] * m[5] - m[2] * m[4],
    m[5] * m[6] - m[3] * m[8], m[0] * m[8] - m[2] * m[6], m[2] * m[3] - m[0] * m[5],
    m[3] * m[7] - m[4] * m[6], m[1] * m[6] - m[0] * m[7], m[0] * m[4] - m[1] * m[3],
  ];
}

function mulMM(a, b) {
  const c = new Array(9);
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      c[3 * i + j] = a[3 * i] * b[j] + a[3 * i + 1] * b[3 + j] + a[3 * i + 2] * b[6 + j];
    }
  }
  return c;
}

function mulMV(m, v) {
  return [
    m[0] * v[0] + m[1] * v[1] + m[2] * v[2],
    m[3] * v[0] + m[4] * v[1] + m[5] * v[2],
    m[6] * v[0] + m[7] * v[1] + m[8] * v[2],
  ];
}

function basis(p) {
  const m = [p[0], p[2], p[4], p[1], p[3], p[5], 1, 1, 1];
  const v = mulMV(adj(m), [p[6], p[7], 1]);
  return mulMM(m, [v[0], 0, 0, 0, v[1], 0, 0, 0, v[2]]);
}

/**
 * @param {number} w  öğe genişliği (px)
 * @param {number} h  öğe yüksekliği (px)
 * @param {number[][]} q  hedef köşeler [[x,y] sol-üst, sağ-üst, sağ-alt, sol-alt] (px)
 * @returns {string} CSS transform değeri
 */
export function matrix3d(w, h, q) {
  const src = [0, 0, w, 0, 0, h, w, h];
  const dst = [q[0][0], q[0][1], q[1][0], q[1][1], q[3][0], q[3][1], q[2][0], q[2][1]];
  const t = mulMM(basis(dst), adj(basis(src)));
  for (let i = 0; i < 9; i++) t[i] /= t[8];
  return `matrix3d(${t[0]},${t[3]},0,${t[6]},${t[1]},${t[4]},0,${t[7]},0,0,1,0,${t[2]},${t[5]},0,${t[8]})`;
}
