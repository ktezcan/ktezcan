/**
 * GLSL gölgelendiricileri.
 * Tüm hareket GPU'da hesaplanır; CPU her karede yalnızca birkaç uniform
 * ve (etkileşim varsa) küçük bir yükseklik dokusu gönderir.
 */

/*
 * 3B Simplex gürültü — Ian McEwan, Stefan Gustavson (Ashima Arts)
 * MIT Lisansı · https://github.com/stegu/webgl-noise
 */
const SIMPLEX_3D = /* glsl */ `
vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec4 mod289(vec4 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec4 permute(vec4 x) { return mod289(((x * 34.0) + 10.0) * x); }
vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }

float snoise(vec3 v) {
  const vec2 C = vec2(1.0 / 6.0, 1.0 / 3.0);
  const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);

  vec3 i  = floor(v + dot(v, C.yyy));
  vec3 x0 = v - i + dot(i, C.xxx);

  vec3 g  = step(x0.yzx, x0.xyz);
  vec3 l  = 1.0 - g;
  vec3 i1 = min(g.xyz, l.zxy);
  vec3 i2 = max(g.xyz, l.zxy);

  vec3 x1 = x0 - i1 + C.xxx;
  vec3 x2 = x0 - i2 + C.yyy;
  vec3 x3 = x0 - D.yyy;

  i = mod289(i);
  vec4 p = permute(permute(permute(
            i.z + vec4(0.0, i1.z, i2.z, 1.0))
          + i.y + vec4(0.0, i1.y, i2.y, 1.0))
          + i.x + vec4(0.0, i1.x, i2.x, 1.0));

  float n_ = 0.142857142857;
  vec3 ns = n_ * D.wyz - D.xzx;

  vec4 j  = p - 49.0 * floor(p * ns.z * ns.z);
  vec4 x_ = floor(j * ns.z);
  vec4 y_ = floor(j - 7.0 * x_);

  vec4 x = x_ * ns.x + ns.yyyy;
  vec4 y = y_ * ns.x + ns.yyyy;
  vec4 h = 1.0 - abs(x) - abs(y);

  vec4 b0 = vec4(x.xy, y.xy);
  vec4 b1 = vec4(x.zw, y.zw);

  vec4 s0 = floor(b0) * 2.0 + 1.0;
  vec4 s1 = floor(b1) * 2.0 + 1.0;
  vec4 sh = -step(h, vec4(0.0));

  vec4 a0 = b0.xzyw + s0.xzyw * sh.xxyy;
  vec4 a1 = b1.xzyw + s1.xzyw * sh.zzww;

  vec3 p0 = vec3(a0.xy, h.x);
  vec3 p1 = vec3(a0.zw, h.y);
  vec3 p2 = vec3(a1.xy, h.z);
  vec3 p3 = vec3(a1.zw, h.w);

  vec4 norm = taylorInvSqrt(vec4(dot(p0, p0), dot(p1, p1), dot(p2, p2), dot(p3, p3)));
  p0 *= norm.x;
  p1 *= norm.y;
  p2 *= norm.z;
  p3 *= norm.w;

  vec4 m = max(0.5 - vec4(dot(x0, x0), dot(x1, x1), dot(x2, x2), dot(x3, x3)), 0.0);
  m = m * m;
  return 105.0 * dot(m * m, vec4(dot(p0, x0), dot(p1, x1), dot(p2, x2), dot(p3, x3)));
}
`;

/* ------------------------------------------------------------------ */
/*  Gözenek yüzeyi (ana katman)                                        */
/* ------------------------------------------------------------------ */
export const PORE_VERTEX = /* glsl */ `
uniform float uTime;
uniform float uIntro;
uniform float uPixelRatio;
uniform float uSize;
uniform float uFade;
uniform float uIdleAmp;
uniform float uHeightScale;
uniform float uCell;
uniform sampler2D uHeight;
uniform vec4 uSimRect;      // xMin, zMin, 1/genişlik, 1/derinlik
uniform vec4 uPointer;      // x, z, güç, yarıçap
uniform float uFocus;
uniform vec2 uFog;
uniform vec3 uColorBase;
uniform vec3 uColorAccent;
uniform vec3 uColorWarm;
uniform vec3 uLightDir;

attribute vec2 aOffset;     // gözenek merkezine göre çeper konumu
attribute vec4 aSeed;       // x: ritim, y: boyut, z: tür (0 çeper, 1 tane), w: açılış gecikmesi

varying vec3 vColor;
varying float vAlpha;

${SIMPLEX_3D}

float simHeight(vec2 p) {
  return texture2D(uHeight, (p - uSimRect.xy) * uSimRect.zw).r;
}

// Fare dururken de süren sakin, doğal dalgalanma
float idleHeight(vec2 p, float t) {
  float n = snoise(vec3(p * 0.105, t * 0.065));
#if IDLE_OCTAVES > 1
  n = n * 0.72 + snoise(vec3(p * 0.29 + 11.0, t * 0.11)) * 0.28;
#endif
  n += sin(p.x * 0.21 - p.y * 0.16 + t * 0.42) * 0.22;
  return n;
}

float surface(vec2 p, float t) {
  return idleHeight(p, t) * uIdleAmp + simHeight(p) * uHeightScale;
}

float easeOutCubic(float x) { float y = 1.0 - x; return 1.0 - y * y * y; }
float easeOutBack(float x) { float y = x - 1.0; return 1.0 + 2.55 * y * y * y + 1.55 * y * y; }

void main() {
  float t = uTime;
  float rnd = aSeed.x;

  // Açılış hikâyesi: gazlanma (gözenek şişer) → kabarma → yerleşme
  float local = clamp((uIntro - aSeed.w * 0.58) / 0.42, 0.0, 1.0);
  float grow = easeOutBack(local);
  float rise = easeOutCubic(local);

  // Gözenekler yavaşça "nefes alır"
  float breathe = 1.0 + 0.05 * sin(t * (0.55 + rnd * 0.5) + rnd * 6.2831);
  vec2 xz = position.xz + aOffset * grow * breathe;

  float e = uCell;
  float h = surface(xz, t);
  vec2 slope = vec2(surface(xz + vec2(e, 0.0), t) - h, surface(xz + vec2(0.0, e), t) - h) / e;
  float energy = clamp(abs(simHeight(xz)) * 2.4, 0.0, 1.0);

  // Sıkışma dalgası: noktalar tepeden çukura kayar → yoğunluk dalgası
  xz -= slope * 0.11;
  vec3 pos = vec3(xz.x, h - (1.0 - rise) * 1.1, xz.y);

  vec4 mv = modelViewMatrix * vec4(pos, 1.0);
  gl_Position = projectionMatrix * mv;
  float dist = -mv.z;

  // Işık: yüzey normali + kameraya yansıyan parıltı
  vec3 n = normalize(vec3(-slope.x, 1.0, -slope.y));
  vec3 L = normalize(uLightDir);
  vec3 V = normalize(cameraPosition - pos);
  float diff = max(dot(n, L), 0.0);
  float spec = pow(max(dot(n, normalize(L + V)), 0.0), 28.0);

  // İmleç ışığı
  vec2 pd = xz - uPointer.xy;
  float glow = uPointer.z * exp(-dot(pd, pd) / (uPointer.w * uPointer.w));

  vec3 col = uColorBase * (0.42 + diff * 0.58 + spec * 1.35);
  float accentMix = clamp(glow * 0.9 + energy * 0.75 + uFocus * 0.12, 0.0, 0.92);
  col = mix(col, uColorAccent * (0.85 + spec * 1.2 + glow * 0.6), accentMix);
  // Otoklav ısısı: sıcak tonla doğar, soğuyarak mineral beyaza döner
  float heat = 1.0 - local;
  col = mix(col, uColorWarm * 1.3, heat * heat);

  float fog = 1.0 - smoothstep(uFog.x, uFog.y, dist);
  float alpha = (aSeed.z < 0.5 ? 0.78 : 0.34) * (0.62 + 0.38 * rnd) * fog * rise * uFade;
  alpha *= 1.0 + glow * 0.8;

  float size = uSize * aSeed.y * uPixelRatio * (10.0 / dist) * (1.0 + glow * 0.55 + energy * 0.35);
  // Alt-piksel noktalar sabit boyutta çizilir, opaklık kapsama alanıyla ölçeklenir → titreme yok
  float minSize = 1.25 * uPixelRatio;
  float cover = clamp(size / minSize, 0.0, 1.0);
  alpha *= cover * cover;
  gl_PointSize = clamp(size, minSize, 42.0 * uPixelRatio);

  vColor = col;
  vAlpha = alpha;
}
`;

export const PORE_FRAGMENT = /* glsl */ `
varying vec3 vColor;
varying float vAlpha;

void main() {
  float d = length(gl_PointCoord - 0.5) * 2.0;
  float a = 1.0 - smoothstep(0.5, 1.0, d);
  gl_FragColor = vec4(vColor, vAlpha * a);
  #include <colorspace_fragment>
}
`;

/* ------------------------------------------------------------------ */
/*  Yükselen gaz kabarcıkları (ön plan, alan derinliği)                */
/* ------------------------------------------------------------------ */
export const MOTE_VERTEX = /* glsl */ `
uniform float uTime;
uniform float uIntro;
uniform float uPixelRatio;
uniform float uSize;
uniform float uFade;
uniform float uAspect;
uniform vec3 uPointerNdc;   // x, y, güç
uniform vec2 uFog;
uniform vec3 uColorBase;
uniform vec3 uColorAccent;

attribute vec4 aSeed;       // x: faz, y: hız, z: boyut, w: salınım

varying vec3 vColor;
varying float vAlpha;
varying float vSoft;

void main() {
  const float H = 5.4;
  float y = mod(position.y + uTime * (0.07 + aSeed.y * 0.11), H);
  float edge = smoothstep(0.0, 0.9, y) * (1.0 - smoothstep(H - 1.4, H, y));
  float sway = uTime * (0.15 + aSeed.w * 0.12) + aSeed.x * 6.2831;
  vec3 p = vec3(position.x + sin(sway) * 0.4, y, position.z + cos(sway * 0.8) * 0.3);

  vec4 mv = modelViewMatrix * vec4(p, 1.0);
  vec4 clip = projectionMatrix * mv;

  // Ekran uzayında imleçten nazikçe kaçış
  vec2 ndc = clip.xy / clip.w;
  vec2 d = (ndc - uPointerNdc.xy) * vec2(uAspect, 1.0);
  float push = uPointerNdc.z * exp(-dot(d, d) * 9.0) * 0.12;
  clip.xy += normalize(d + 1e-5) * push * clip.w / vec2(uAspect, 1.0);
  gl_Position = clip;

  float dist = -mv.z;
  float near = 1.0 - smoothstep(1.5, 5.5, dist);
  vSoft = mix(0.45, 1.0, near);
  float size = uSize * aSeed.z * uPixelRatio * (10.0 / max(dist, 0.5)) * (1.0 + near * 2.2);
  gl_PointSize = min(size, 96.0 * uPixelRatio);

  float fog = 1.0 - smoothstep(uFog.x, uFog.y, dist);
  vAlpha = edge * fog * mix(0.5, 0.13, near) * uIntro * uFade;
  vColor = mix(uColorBase, uColorAccent, 0.2 + 0.35 * aSeed.w);
}
`;

export const MOTE_FRAGMENT = /* glsl */ `
varying vec3 vColor;
varying float vAlpha;
varying float vSoft;

void main() {
  float d = length(gl_PointCoord - 0.5) * 2.0;
  float a = 1.0 - smoothstep(1.0 - vSoft, 1.0, d);
  gl_FragColor = vec4(vColor, vAlpha * a);
  #include <colorspace_fragment>
}
`;
