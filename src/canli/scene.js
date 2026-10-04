/**
 * HeroScene — Ege Gazbeton ana sayfa WebGL sahnesi.
 *
 * Performans sözleşmesi:
 *  • requestAnimationFrame YALNIZCA hero görüş alanındayken ve sekme
 *    görünürken çalışır (IntersectionObserver + visibilitychange + pagehide).
 *    Kullanıcı aşağı kaydırdığında döngü iptal edilir (cancelAnimationFrame);
 *    işaretçi dinleyicileri de sökülür → sayfanın geri kalanına sıfır yük.
 *  • Kare süresi izlenir; cihaz zorlanırsa önce piksel oranı, sonra parçacık
 *    sayısı kademeli düşürülür. En alt kademe de yetmezse animasyon tek kareye
 *    sabitlenir (asla takılan bir sayfa bırakmaz).
 *  • Dalga simülasyonu etkileşim yokken uyur; rölanti hareketi tamamen GPU'dadır.
 *  • Döngü içinde bellek ayırma yapılmaz (çöp toplayıcı takılması yok).
 */
import { WaveField } from './wave-field.js';
import { buildPoreField, buildMotes } from './pore-field.js';
import { PORE_VERTEX, PORE_FRAGMENT, MOTE_VERTEX, MOTE_FRAGMENT } from './shaders.js';
import { TIERS, PHYSICS, LOOK } from './config.js';

const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
const lerp = (a, b, t) => a + (b - a) * t;
/** Kare hızından bağımsız üstel yumuşatma */
const damp = (a, b, lambda, dt) => lerp(a, b, 1 - Math.exp(-lambda * dt));

/** Koşulsuz kararlı, kritik sönümlü yay (kamera paralaksı için) */
function spring(s, target, omega, dt) {
  const f = 1 + 2 * dt * omega;
  const oo = omega * omega;
  const hoo = dt * oo;
  const hhoo = dt * hoo;
  const inv = 1 / (f + hhoo);
  const x = (f * s.x + dt * s.v + hhoo * target) * inv;
  s.v = (s.v + hoo * (target - s.x)) * inv;
  s.x = x;
}

export class HeroScene {
  /**
   * @param {typeof import('three')} THREE  CDN'den yüklenen Three.js modülü
   * @param {object} o
   * @param {HTMLElement} o.root     Hero <section> öğesi
   * @param {HTMLCanvasElement} o.canvas
   * @param {'low'|'mid'|'high'} o.tier
   * @param {'live'|'static'} o.mode
   * @param {boolean} [o.reducedMotion]  static modun nedeni hareket azaltma mı
   * @param {HTMLElement|null} [o.debugEl]
   * @param {boolean} [o.aktif]  false ise döngü yalnız setAktif(true) ile başlar (finale yaşam döngüsü: hikâye finali yönetir)
   */
  constructor(THREE, { root, canvas, tier = 'mid', mode = 'live', reducedMotion = false, debugEl = null, aktif = true }) {
    this.THREE = THREE;
    this.root = root;
    this.canvas = canvas;
    this.tierName = TIERS[tier] ? tier : 'mid';
    this.tier = TIERS[this.tierName];
    this.staticMode = mode === 'static';
    this.staticByMotion = this.staticMode && reducedMotion;
    this.debugEl = debugEl;

    this.running = false;
    this.aktif = aktif; // dışarıdan açılıp kapanan etkinlik (finale etkin değilken hiçbir kare çizilmez)
    this.introBekliyor = !aktif; // açılış (gazlanma) animasyonu ac() ile başlar: ilk render hazırlıktır, perde açılışına denk gelir
    this.destroyed = false;
    this.raf = 0;
    this.inView = false;
    this.pageVisible = document.visibilityState !== 'hidden';
    this.contextLost = false;
    this.ready = false;

    this.lastNow = 0;
    this.time = 0;
    this.intro = this.staticMode ? 1 : 0;
    this.frames = 0;
    this.scroll = 0;

    this.pointer = { x: -1, y: -1, active: false, moved: 0 };
    this.ndc = { x: 0, y: 0 };
    this.follow = { x: 0, z: 0, vx: 0, vz: 0, tx: 0, tz: 0, ready: false };
    this.camX = { x: 0, v: 0 };
    this.camY = { x: 0, v: 0 };
    this.glow = 0;
    this.focus = 0;
    this.focusTarget = 0;

    this.rect = { left: 0, top: 0, width: 1, height: 1 };
    this.size = { w: 1, h: 1 };
    this.levels = [];
    this.level = 0;
    this.gov = { sum: 0, n: 0, cooldown: 90, strikes: 0 };
    this.dbg = { last: 0, frames: 0, fps: 0, simMs: 0 };

    this._hit = { x: 0, z: 0 };
    this._rebuildTimer = 0;

    // Bağlı işleyiciler (dinleyici ekle/çıkar için sabit referans)
    this._frame = this._frame.bind(this);
    this._onPointerMove = this._onPointerMove.bind(this);
    this._onPointerDown = this._onPointerDown.bind(this);
    this._onPointerOut = this._onPointerOut.bind(this);
    this._onBlur = this._onBlur.bind(this);
    this._onVisibility = this._onVisibility.bind(this);
    this._onPageHide = this._onPageHide.bind(this);
    this._onPageShow = this._onPageShow.bind(this);
    this._onPulse = this._onPulse.bind(this);
    this._onFocus = this._onFocus.bind(this);
    this._onContextLost = this._onContextLost.bind(this);
    this._onContextRestored = this._onContextRestored.bind(this);
    this._onMotionPref = this._onMotionPref.bind(this);
  }

  /* ================================================================ */
  /*  Kurulum                                                          */
  /* ================================================================ */

  init() {
    const THREE = this.THREE;
    const css = getComputedStyle(this.root);
    const color = (name, fallback) => new THREE.Color((css.getPropertyValue(name) || '').trim() || fallback);
    this.colors = {
      bg: color('--eg-bg', '#0b0d10'),
      base: color('--eg-particle', '#e9e4da'),
      accent: color('--eg-accent', '#4f9dff'),
      warm: color('--eg-warm', '#ff9d5c'),
    };

    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: false, // noktalar gölgelendiricide yumuşatılıyor; MSAA gereksiz yük
      alpha: false, // opak tuval: tarayıcı birleştirmesi daha ucuz
      depth: false,
      stencil: false,
      powerPreference: 'default',
    });
    this.renderer.setClearColor(this.colors.bg, 1);

    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(LOOK.fov, 1, 0.1, 80);
    this._v = new THREE.Vector3();

    this.uniforms = {
      uTime: { value: 0 },
      uIntro: { value: this.intro },
      uPixelRatio: { value: 1 },
      uFade: { value: 1 },
      uFog: { value: new THREE.Vector2(LOOK.fog[0], LOOK.fog[1]) },
      uColorBase: { value: this.colors.base },
      uColorAccent: { value: this.colors.accent },
    };

    this._measure();
    this._layoutCamera();
    this._buildLevels();
    this._applyLevel(0);
    this._buildWorld();
    this._bind();

    if (this.staticMode) this._renderStatic();
    return this;
  }

  /** Kameranın düzlemde gördüğü yamuk alan (+ paralaks payı) */
  _computeRegion() {
    const cam = this.camera;
    const hit = { x: 0, z: 0 };
    const fogReach = Math.sqrt(Math.max(1, LOOK.fog[1] ** 2 - cam.position.y ** 2));
    const zFog = cam.position.z - fogReach;

    let zNear = -Infinity;
    let halfNear = 0;
    for (const nx of [-1.15, 1.15]) {
      if (this._ndcToPlane(nx, -1.12, hit)) {
        zNear = Math.max(zNear, hit.z);
        halfNear = Math.max(halfNear, Math.abs(hit.x));
      }
    }
    if (!Number.isFinite(zNear)) zNear = cam.position.z - 2;

    let zFar = Infinity;
    let halfFar = 0;
    for (const nx of [-1.15, 1.15]) {
      if (this._ndcToPlane(nx, 1.08, hit)) {
        zFar = Math.min(zFar, hit.z);
        halfFar = Math.max(halfFar, Math.abs(hit.x));
      }
    }
    if (!Number.isFinite(zFar) || zFar < zFog) {
      // Ufuk görünüyorsa ya da kesişim sisin ötesindeyse sis sınırında kes
      const hfov = Math.atan(Math.tan((cam.fov * Math.PI) / 360) * cam.aspect);
      zFar = zFog;
      halfFar = Math.max(halfFar ? Math.min(halfFar, Math.tan(hfov) * LOOK.fog[1] * 1.1) : 0, Math.tan(hfov) * fogReach);
    }

    return {
      zNear: zNear + 1.4,
      zFar: zFar - 1,
      halfNear: halfNear * 1.12 + 0.9,
      halfFar: Math.min(halfFar * 1.08 + 1.5, 26),
    };
  }

  _buildWorld() {
    const THREE = this.THREE;
    this.region = this._computeRegion();
    const R = this.region;

    // --- Dalga simülasyonu (yakın-orta bölge; uzak bölge yalnızca rölanti) ---
    const zSimFar = Math.max(R.zFar, this.camera.position.z - 20);
    const halfSim = Math.min(14, R.halfNear + (R.halfFar - R.halfNear) * ((R.zNear - zSimFar) / (R.zNear - R.zFar)));
    this.wave = new WaveField({
      xMin: -halfSim,
      zMin: zSimFar,
      width: halfSim * 2,
      depth: R.zNear - zSimFar,
      cell: this.tier.cell,
      speed: PHYSICS.waveSpeed,
      damping: PHYSICS.damping,
      viscosity: PHYSICS.viscosity,
      sponge: PHYSICS.sponge,
      sleepEpsilon: PHYSICS.sleepEpsilon,
    });

    // Yarım hassasiyetli (R16F) doku: WebGL2'de her cihazda doğrusal süzgeçlenebilir
    this.heightData = new Uint16Array(this.wave.cols * this.wave.rows);
    this.heightTex = new THREE.DataTexture(this.heightData, this.wave.cols, this.wave.rows, THREE.RedFormat, THREE.HalfFloatType);
    this.heightTex.magFilter = THREE.LinearFilter;
    this.heightTex.minFilter = THREE.LinearFilter;
    this.heightTex.generateMipmaps = false;
    this.heightTex.needsUpdate = true;

    // --- Gözenek alanı ---
    const field = buildPoreField({
      region: R,
      eye: this.camera.position.toArray(),
      budget: this.tier.particles,
      attempts: this.tier.attempts,
      unproject: (u, v, out) => this._ndcToPlane(u * 2 - 1, v * 2 - 1, out),
      focus: [1.2, -2.5],
      seed: LOOK.seed,
    });
    this.poreCount = field.count;

    const poreGeo = new THREE.BufferGeometry();
    poreGeo.setAttribute('position', new THREE.BufferAttribute(field.position, 3));
    poreGeo.setAttribute('aOffset', new THREE.BufferAttribute(field.offset, 2));
    poreGeo.setAttribute('aSeed', new THREE.BufferAttribute(field.seed, 4));
    poreGeo.setDrawRange(0, Math.floor(this.poreCount * this.frac));

    const u = this.uniforms;
    this.poreMat =
      this.poreMat ||
      new THREE.ShaderMaterial({
        vertexShader: PORE_VERTEX,
        fragmentShader: PORE_FRAGMENT,
        defines: { IDLE_OCTAVES: this.tier.octaves },
        uniforms: {
          ...u,
          uSize: { value: LOOK.pointSize },
          uIdleAmp: { value: LOOK.idleAmplitude },
          uHeightScale: { value: LOOK.heightScale },
          uCell: { value: this.tier.cell },
          uHeight: { value: null },
          uSimRect: { value: new THREE.Vector4() },
          uPointer: { value: new THREE.Vector4(0, 0, 0, 1.7) },
          uFocus: { value: 0 },
          uColorWarm: { value: this.colors.warm },
          uLightDir: { value: new THREE.Vector3(0.38, 0.62, -1.0) },
        },
        transparent: true,
        depthTest: false,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
      });
    const pu = this.poreMat.uniforms;
    pu.uHeight.value = this.heightTex;
    pu.uSimRect.value.set(this.wave.xMin, this.wave.zMin, 1 / this.wave.width, 1 / this.wave.depth);
    pu.uCell.value = Math.max(this.wave.dx, this.wave.dz);

    this.pores = new THREE.Points(poreGeo, this.poreMat);
    this.pores.frustumCulled = false; // konumlar gölgelendiricide değişiyor
    this.scene.add(this.pores);

    // --- Yükselen kabarcıklar ---
    const motes = buildMotes({ count: this.tier.motes, seed: LOOK.seed });
    const moteGeo = new THREE.BufferGeometry();
    moteGeo.setAttribute('position', new THREE.BufferAttribute(motes.position, 3));
    moteGeo.setAttribute('aSeed', new THREE.BufferAttribute(motes.seed, 4));
    this.moteMat =
      this.moteMat ||
      new THREE.ShaderMaterial({
        vertexShader: MOTE_VERTEX,
        fragmentShader: MOTE_FRAGMENT,
        uniforms: {
          ...u,
          uSize: { value: LOOK.pointSize * 1.15 },
          uAspect: { value: 1 },
          uPointerNdc: { value: new THREE.Vector3() },
        },
        transparent: true,
        depthTest: false,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
      });
    this.motes = new THREE.Points(moteGeo, this.moteMat);
    this.motes.frustumCulled = false;
    this.scene.add(this.motes);
  }

  _disposeWorld() {
    if (this.pores) {
      this.scene.remove(this.pores);
      this.pores.geometry.dispose();
      this.pores = null;
    }
    if (this.motes) {
      this.scene.remove(this.motes);
      this.motes.geometry.dispose();
      this.motes = null;
    }
    if (this.heightTex) {
      this.heightTex.dispose();
      this.heightTex = null;
    }
  }

  /* ================================================================ */
  /*  Boyut, kamera, kalite kademeleri                                 */
  /* ================================================================ */

  _measure() {
    const r = this.root.getBoundingClientRect();
    this.rect.left = r.left;
    this.rect.top = r.top;
    this.rect.width = Math.max(1, r.width);
    this.rect.height = Math.max(1, r.height);
    this.size.w = Math.max(1, Math.round(this.canvas.clientWidth || r.width));
    this.size.h = Math.max(1, Math.round(this.canvas.clientHeight || r.height));
  }

  _layoutCamera() {
    const aspect = this.size.w / this.size.h;
    // Dikey ekranlarda yatay kapsamı korumak için görüş açısı ve kamera uyarlanır
    const portrait = clamp((1.25 - aspect) / 0.75, 0, 1);
    this.camera.aspect = aspect;
    this.camera.fov = lerp(LOOK.fov, LOOK.fovPortrait, portrait);
    this.camera.updateProjectionMatrix();
    this.base = LOOK.camera.map((v, i) => lerp(v, LOOK.cameraPortrait[i], portrait));
    this._placeCamera();
  }

  _placeCamera() {
    const [bx, by, bz] = this.base;
    const s = this.scroll;
    this.camera.position.set(bx + this.camX.x * LOOK.parallax[0], by + this.camY.x * LOOK.parallax[1] + s * 1.4, bz - s * 0.6);
    this.camera.lookAt(LOOK.target[0] + this.camX.x * 0.25, LOOK.target[1], LOOK.target[2] - s * 2.2);
    this.camera.updateMatrixWorld();
  }

  _buildLevels() {
    const dpr = Math.min(window.devicePixelRatio || 1, this.tier.dprMax);
    const raw = [
      [dpr, 1],
      [Math.max(1, dpr * 0.8), 1],
      [1, 0.8],
      [1, 0.62],
      [0.85, 0.5],
    ];
    this.levels = raw.filter((l, i) => i === 0 || l[0] !== raw[i - 1][0] || l[1] !== raw[i - 1][1]);
  }

  _applyLevel(i) {
    this.level = clamp(i, 0, this.levels.length - 1);
    const [dpr, frac] = this.levels[this.level];
    this.dpr = dpr;
    this.frac = frac;
    this.renderer.setPixelRatio(dpr);
    this.renderer.setSize(this.size.w, this.size.h, false);
    this.uniforms.uPixelRatio.value = dpr;
    if (this.pores) this.pores.geometry.setDrawRange(0, Math.floor(this.poreCount * frac));
  }

  _onResize() {
    if (this.destroyed) return;
    const prevW = this.size.w;
    const prevH = this.size.h;
    this._measure();
    if (prevW === this.size.w && prevH === this.size.h) return;
    this._layoutCamera();
    this.renderer.setSize(this.size.w, this.size.h, false);
    if (this.moteMat) this.moteMat.uniforms.uAspect.value = this.camera.aspect;

    // Görünen alan üretilen alanı aşıyorsa (ör. telefon döndürme) yeniden üret
    const need = this._computeRegion();
    const have = this.region;
    if (need.halfNear > have.halfNear + 0.3 || need.halfFar > have.halfFar + 0.6 || need.zNear > have.zNear + 0.3 || need.zFar < have.zFar - 0.6) {
      clearTimeout(this._rebuildTimer);
      this._rebuildTimer = setTimeout(() => {
        if (this.destroyed) return;
        this._disposeWorld();
        this._buildWorld();
        if (!this.running) this._renderOnce();
      }, 220);
    }
    if (!this.running) this._renderOnce();
  }

  /* ================================================================ */
  /*  Görünürlük → döngü kontrolü                                      */
  /* ================================================================ */

  _bind() {
    this._io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) this.inView = e.isIntersecting;
        this._sync();
      },
      { threshold: 0 }
    );
    this._io.observe(this.root);

    let pending = 0;
    this._ro = new ResizeObserver(() => {
      cancelAnimationFrame(pending);
      pending = requestAnimationFrame(() => this._onResize());
    });
    this._ro.observe(this.root);

    document.addEventListener('visibilitychange', this._onVisibility);
    window.addEventListener('pagehide', this._onPageHide);
    window.addEventListener('pageshow', this._onPageShow);
    this.root.addEventListener('eg:pulse', this._onPulse);
    this.root.addEventListener('eg:focus', this._onFocus);
    this.canvas.addEventListener('webglcontextlost', this._onContextLost);
    this.canvas.addEventListener('webglcontextrestored', this._onContextRestored);

    this._motionMq = window.matchMedia?.('(prefers-reduced-motion: reduce)');
    this._motionMq?.addEventListener?.('change', this._onMotionPref);
  }

  /** Döngünün çalışması gerekip gerekmediğine karar veren tek yer. */
  _sync() {
    const shouldRun = this.inView && this.aktif && this.pageVisible && !this.contextLost && !this.staticMode && !this.destroyed;
    if (shouldRun && !this.running) this._start();
    else if (!shouldRun && this.running) this._stop();
    this._debugState();
  }

  /** Etkinliği dışarıdan aç/kapat (kapalıyken rAF iptal, işaretçi dinleyicileri sökülür). */
  setAktif(v) {
    this.aktif = !!v;
    this._sync();
  }

  /** Açılış animasyonunu başlat (hazırlıkta intro 0'da bekler). */
  introBaslat() {
    this.introBekliyor = false;
  }

  /** İlk (görünmez) render: gölgelendirici derleme ve GPU yüklemesi önceden yapılır, ilk karede takılma olmaz. */
  hazirla() {
    if (this.staticMode) return;
    this._renderOnce();
  }

  _start() {
    this.running = true;
    this.lastNow = 0;
    this.gov.sum = 0;
    this.gov.n = 0;
    this.gov.cooldown = 45; // devam ederken ilk kareler ölçüme katılmaz
    // İşaretçi dinleyicileri yalnızca animasyon çalışırken bağlıdır
    window.addEventListener('pointermove', this._onPointerMove, { passive: true });
    window.addEventListener('pointerdown', this._onPointerDown, { passive: true });
    document.addEventListener('pointerout', this._onPointerOut, { passive: true });
    window.addEventListener('blur', this._onBlur);
    this.raf = requestAnimationFrame(this._frame);
  }

  _stop() {
    this.running = false;
    cancelAnimationFrame(this.raf);
    this.raf = 0;
    window.removeEventListener('pointermove', this._onPointerMove);
    window.removeEventListener('pointerdown', this._onPointerDown);
    document.removeEventListener('pointerout', this._onPointerOut);
    window.removeEventListener('blur', this._onBlur);
    this.pointer.active = false;
  }

  _onVisibility() {
    this.pageVisible = document.visibilityState !== 'hidden';
    this._sync();
  }

  _onPageHide() {
    this.pageVisible = false;
    this._sync();
  }

  _onPageShow() {
    this.pageVisible = document.visibilityState !== 'hidden';
    this._sync();
  }

  _onContextLost(e) {
    e.preventDefault();
    this.contextLost = true;
    this._sync();
  }

  _onContextRestored() {
    this.contextLost = false;
    if (this.heightTex) this.heightTex.needsUpdate = true;
    if (this.staticMode) this._renderOnce();
    this._sync();
  }

  _onMotionPref(e) {
    if (e.matches) {
      this.staticByMotion = true;
      this.staticMode = true;
      this._sync();
      this._renderStatic();
    } else if (this.staticByMotion) {
      this.staticByMotion = false;
      this.staticMode = false;
      this._sync();
    }
  }

  /* ================================================================ */
  /*  Girdi                                                            */
  /* ================================================================ */

  _onPointerMove(e) {
    const p = this.pointer;
    p.x = e.clientX;
    p.y = e.clientY;
    p.active = true;
    p.moved = performance.now();
  }

  _onPointerDown(e) {
    this._onPointerMove(e);
    // Dokunmatik ekranda dokunuş = yüzeye damla
    if (this.wave && this._clientToPlane(e.clientX, e.clientY, this._hit)) {
      this.wave.impulse(this._hit.x, this._hit.z, -PHYSICS.pulseGain * 0.8, PHYSICS.pulseRadius * 0.8);
    }
  }

  _onPointerOut(e) {
    if (!e.relatedTarget) this.pointer.active = false; // imleç pencereden çıktı
  }

  _onBlur() {
    this.pointer.active = false;
  }

  _onPulse(e) {
    this.pulse(e.detail || {});
  }

  _onFocus(e) {
    this.focusTarget = clamp(Number(e.detail?.value) || 0, 0, 1);
  }

  /**
   * Arayüzden dalga tetikler (buton üzerine gelme, rol seçimi vb.).
   * @param {{x?:number, y?:number, strength?:number}} o  Ekran (client) koordinatı
   */
  pulse({ x, y, strength = 1 } = {}) {
    if (!this.wave || this.staticMode || !this.running) return;
    const r = this.rect;
    const cx = x ?? r.left + r.width * 0.5;
    const cy = y ?? r.top + r.height * 0.7;
    if (this._clientToPlane(cx, cy, this._hit)) {
      this.wave.impulse(this._hit.x, this._hit.z, -PHYSICS.pulseGain * strength, PHYSICS.pulseRadius);
    }
  }

  _clientToPlane(cx, cy, out) {
    const r = this.rect;
    const nx = ((cx - r.left) / r.width) * 2 - 1;
    const ny = -(((cy - r.top) / r.height) * 2 - 1);
    if (nx < -1.05 || nx > 1.05 || ny < -1.05 || ny > 1.05) return false;
    return this._ndcToPlane(nx, ny, out);
  }

  /** Ekran (NDC) → y = 0 düzlemi ışın kesişimi; bellek ayırmaz. */
  _ndcToPlane(nx, ny, out) {
    const o = this.camera.position;
    const v = this._v.set(nx, ny, 0.5).unproject(this.camera);
    const dx = v.x - o.x;
    const dy = v.y - o.y;
    const dz = v.z - o.z;
    if (dy > -1e-6) return false; // ufkun üstü
    const t = -o.y / dy;
    out.x = o.x + dx * t;
    out.z = o.z + dz * t;
    return true;
  }

  /* ================================================================ */
  /*  Döngü                                                            */
  /* ================================================================ */

  _frame(now) {
    if (!this.running) return;
    const rawDt = this.lastNow ? (now - this.lastNow) / 1000 : 1 / 60;
    this.lastNow = now;
    const dt = clamp(rawDt, 0.001, 1 / 24); // sekme dönüşü vb. büyük sıçramaları kırp

    try {
      this._update(dt);
      this.renderer.render(this.scene, this.camera);
    } catch (err) {
      this._fail(err);
      return;
    }

    this.frames++;
    if (!this.ready) this._markReady();
    this._govern(rawDt);
    if (this.debugEl) this._debugTick(now);
    if (this.running) this.raf = requestAnimationFrame(this._frame);
  }

  _update(dt) {
    this.time += dt;
    if (this.intro < 1 && !this.introBekliyor) this.intro = Math.min(1, this.intro + dt / LOOK.introDuration);

    // Yerleşim okuması karenin başında, hiçbir DOM yazımından önce (layout thrash yok)
    const b = this.root.getBoundingClientRect();
    const r = this.rect;
    r.left = b.left;
    r.top = b.top;
    r.width = Math.max(1, b.width);
    r.height = Math.max(1, b.height);
    this.scroll = damp(this.scroll, clamp(-r.top / r.height, 0, 1), 10, dt);

    // İmleç → NDC
    const p = this.pointer;
    const inside = p.active && p.x >= r.left && p.x <= r.left + r.width && p.y >= r.top && p.y <= r.top + r.height;
    if (inside) {
      this.ndc.x = ((p.x - r.left) / r.width) * 2 - 1;
      this.ndc.y = -(((p.y - r.top) / r.height) * 2 - 1);
    }

    // Kamera: ağır, kritik sönümlü paralaks
    spring(this.camX, inside ? this.ndc.x : 0, 2.6, dt);
    spring(this.camY, inside ? this.ndc.y : 0, 2.6, dt);
    this._placeCamera();

    // İmleç takipçisi: kütle-yay-sönüm → fiziksel ağırlık hissi
    const f = this.follow;
    const hit = inside && this._ndcToPlane(this.ndc.x, this.ndc.y, this._hit);
    if (hit) {
      if (!f.ready) {
        f.x = this._hit.x;
        f.z = this._hit.z;
        f.ready = true;
      }
      f.tx = this._hit.x;
      f.tz = this._hit.z;
    }
    const k = PHYSICS.followStiffness;
    const c = 2 * Math.sqrt(k) * PHYSICS.followDamping;
    f.vx += (k * (f.tx - f.x) - c * f.vx) * dt;
    f.vz += (k * (f.tz - f.z) - c * f.vz) * dt;
    f.x += f.vx * dt;
    f.z += f.vz * dt;
    const speed = Math.min(Math.hypot(f.vx, f.vz), PHYSICS.maxSpeed);

    const resting = performance.now() - p.moved > 2500;
    this.glow = damp(this.glow, hit ? (resting ? 0.45 : 1) : 0, hit ? 5 : 2.2, dt);

    // Hareket izi → dalga alanı
    if (hit && speed > 0.05 && this.intro > 0.35) {
      this.wave.impulse(f.x, f.z, -PHYSICS.wakeGain * speed * dt, PHYSICS.wakeRadius);
    }

    // Fizik adımı + (gerekirse) GPU'ya yükseklik yüklemesi
    const t0 = this.debugEl ? performance.now() : 0;
    if (this.wave.step(dt)) this._uploadHeight();
    if (this.debugEl) this.dbg.simMs = lerp(this.dbg.simMs, performance.now() - t0, 0.1);

    this.focus = damp(this.focus, this.focusTarget, 4, dt);

    const u = this.uniforms;
    u.uTime.value = this.time;
    u.uIntro.value = this.intro;
    u.uFade.value = 1 - this.scroll * 0.6;
    const pu = this.poreMat.uniforms;
    pu.uPointer.value.set(f.x, f.z, this.glow, 1.7);
    pu.uFocus.value = this.focus;
    const mu = this.moteMat.uniforms;
    mu.uPointerNdc.value.set(this.ndc.x, this.ndc.y, this.glow);
    mu.uAspect.value = this.camera.aspect;
  }

  _uploadHeight() {
    const src = this.wave.h;
    const dst = this.heightData;
    const toHalf = this.THREE.DataUtils.toHalfFloat;
    for (let i = 0; i < src.length; i++) dst[i] = toHalf(src[i]);
    this.heightTex.needsUpdate = true;
    this.wave.dirty = false;
  }

  /** Kare bütçesi denetçisi: zorlanan cihazda kaliteyi kademeli düşürür. */
  _govern(rawDt) {
    const g = this.gov;
    if (g.cooldown > 0) {
      g.cooldown--;
      return;
    }
    if (rawDt > 0.25) return; // sekme/arka plan sıçraması, ölçüme katma
    g.sum += rawDt;
    g.n++;
    if (g.n < 50) return;
    const avg = g.sum / g.n;
    g.sum = 0;
    g.n = 0;
    if (avg <= 1 / 46) {
      g.strikes = 0;
      return;
    }
    if (this.level < this.levels.length - 1) {
      this._applyLevel(this.level + 1);
      g.cooldown = 40;
    } else if (avg > 1 / 26 && ++g.strikes >= 3) {
      // En düşük kademe de yetmiyor: animasyonu sabitle, sayfayı asla yorma
      this.staticMode = true;
      this._sync();
      this._renderOnce();
    }
  }

  _markReady() {
    this.ready = true;
    this.root.classList.add('is-live');
    this.root.dispatchEvent(new CustomEvent('eg:ready', { bubbles: true, detail: { tier: this.tierName, static: this.staticMode } }));
  }

  _renderOnce() {
    if (!this.renderer || this.contextLost) return;
    this._measure();
    this._placeCamera();
    this.renderer.render(this.scene, this.camera);
  }

  /** Hareket azaltma / yazılımsal GPU: güzel bir anı tek kare olarak çiz. */
  _renderStatic() {
    this.intro = 1;
    this.time = 14;
    this.uniforms.uTime.value = this.time;
    this.uniforms.uIntro.value = 1;
    this.uniforms.uFade.value = 1;
    this._renderOnce();
    if (!this.ready) this._markReady();
    this._debugState();
  }

  _fail(err) {
    console.warn('[EgeHero] Sahne durduruldu, statik görünüme geçildi.', err);
    this.staticMode = true;
    this._stop();
    this.root.classList.remove('is-live');
    this.root.dataset.egScene = 'fallback';
  }

  /* ================================================================ */
  /*  Hata ayıklama paneli (?debug)                                    */
  /* ================================================================ */

  _debugTick(now) {
    const d = this.dbg;
    d.frames++;
    if (!d.last) d.last = now;
    if (now - d.last < 500) return;
    d.fps = Math.round((d.frames * 1000) / (now - d.last));
    d.frames = 0;
    d.last = now;
    this._debugState();
  }

  _debugState() {
    if (!this.debugEl) return;
    const state = this.staticMode ? '◆ STATİK (tek kare)' : this.running ? '● ÇALIŞIYOR' : '■ DURDU — rAF iptal';
    const why = this.running || this.staticMode ? '' : !this.inView ? ' (görüş alanı dışında)' : !this.pageVisible ? ' (sekme gizli)' : '';
    const drawn = Math.floor((this.poreCount || 0) * (this.frac || 1));
    this.debugEl.textContent =
      `${state}${why}\n` +
      `fps ${this.running ? this.dbg.fps : 0} · kare ${this.frames}\n` +
      `kademe ${this.tierName} · seviye ${this.level} · dpr ${this.dpr}\n` +
      `parçacık ${drawn.toLocaleString('tr-TR')} · sim ${this.wave?.awake ? 'aktif' : 'uyku'} ${this.dbg.simMs.toFixed(2)} ms`;
    this.debugEl.dataset.state = this.staticMode ? 'static' : this.running ? 'running' : 'paused';
  }

  /* ================================================================ */
  /*  Temizlik (SPA / sayfa geçişleri için)                            */
  /* ================================================================ */

  destroy() {
    this.destroyed = true;
    this._stop();
    clearTimeout(this._rebuildTimer);
    this._io?.disconnect();
    this._ro?.disconnect();
    document.removeEventListener('visibilitychange', this._onVisibility);
    window.removeEventListener('pagehide', this._onPageHide);
    window.removeEventListener('pageshow', this._onPageShow);
    this.root.removeEventListener('eg:pulse', this._onPulse);
    this.root.removeEventListener('eg:focus', this._onFocus);
    this.canvas.removeEventListener('webglcontextlost', this._onContextLost);
    this.canvas.removeEventListener('webglcontextrestored', this._onContextRestored);
    this._motionMq?.removeEventListener?.('change', this._onMotionPref);
    this._disposeWorld();
    this.poreMat?.dispose();
    this.moteMat?.dispose();
    this.renderer?.dispose();
    this.renderer?.forceContextLoss?.(); // WebGL bağlamı bırakılır (finale bitince GPU belleği serbest)
    this.root.classList.remove('is-live');
  }
}
