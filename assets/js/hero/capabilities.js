/**
 * Cihaz yetenek tespiti → çalışma modu ve kalite kademesi.
 *
 *  mode: 'live'   → tam etkileşimli animasyon
 *        'static' → tek kare çizilir, döngü hiç başlamaz
 *                   (hareket azaltma tercihi, yazılımsal GPU)
 *        'off'    → WebGL yüklenmez, CSS yedeği kalır
 *                   (WebGL2 yok, veri tasarrufu modu)
 *  tier: 'low' | 'mid' | 'high'
 *
 * Test için URL parametreleri: ?quality=low|mid|high|static|off
 */
const TIER_NAMES = new Set(['low', 'mid', 'high']);

export function detectCapabilities(win = window) {
  const params = new URLSearchParams(win.location.search);
  const forced = (params.get('quality') || '').toLowerCase();
  const media = (q) => !!(win.matchMedia && win.matchMedia(q).matches);
  const nav = win.navigator || {};
  const conn = nav.connection || {};

  const reducedMotion = media('(prefers-reduced-motion: reduce)');
  const saveData = conn.saveData === true || /(^|-)2g$/.test(conn.effectiveType || '');
  const coarse = media('(pointer: coarse)');
  const memory = nav.deviceMemory; // yalnızca Chromium; Safari/Firefox'ta tanımsız
  const cores = nav.hardwareConcurrency || 4;
  const shortSide = Math.min(win.screen?.width || 1280, win.screen?.height || 800);

  const gl = probeWebGL2();

  let tier = 'high';
  if (coarse || shortSide < 700 || (memory && memory <= 4) || cores <= 4) tier = 'mid';
  if ((memory && memory <= 2) || (coarse && cores <= 4) || (coarse && memory && memory <= 3)) tier = 'low';

  let mode = 'live';
  if (!gl.ok || saveData) mode = 'off';
  else if (reducedMotion || gl.software) mode = 'static';

  if (mode === 'static') tier = 'low'; // tek kare için hafif üretim yeterli

  // Manuel geçersiz kılma (test / hata ayıklama)
  if (forced === 'off') mode = 'off';
  else if (forced === 'static' && gl.ok) mode = 'static';
  else if (TIER_NAMES.has(forced) && gl.ok) {
    tier = forced;
    mode = reducedMotion ? 'static' : 'live';
  }

  return { mode, tier, reducedMotion, saveData, coarse, gl };
}

/** WebGL2 desteğini ve yazılımsal (CPU) çizim olup olmadığını yoklar. */
function probeWebGL2() {
  const result = { ok: false, software: false, renderer: '' };
  try {
    const canvas = document.createElement('canvas');
    // Donanım hızlandırması yoksa tarayıcı burada null döndürür.
    let ctx = canvas.getContext('webgl2', { failIfMajorPerformanceCaveat: true });
    if (!ctx) {
      ctx = canvas.getContext('webgl2');
      if (ctx) result.software = true;
    }
    if (!ctx) return result;
    result.ok = true;

    result.renderer = String(ctx.getParameter(ctx.RENDERER) || '');
    // Chromium genel bir ad döndürür; gerçek adı yalnızca orada sorgula
    // (Firefox bu eklenti için konsola uyarı basar).
    if (/^webkit webgl$/i.test(result.renderer)) {
      const info = ctx.getExtension('WEBGL_debug_renderer_info');
      if (info) result.renderer = String(ctx.getParameter(info.UNMASKED_RENDERER_WEBGL) || '');
    }
    if (/swiftshader|llvmpipe|softpipe|software|basic render/i.test(result.renderer)) {
      result.software = true;
    }
    ctx.getExtension('WEBGL_lose_context')?.loseContext();
  } catch {
    result.ok = false;
  }
  return result;
}
