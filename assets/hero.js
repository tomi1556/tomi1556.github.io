/* 灯原：トップの開幕。暗闇に最初の灯籠がともり、灯路が地平線まで伝わって「灯ノ海」になる。
   WebGL2 で描く立方体の世界。使えない端末では、これまでの絵のまま。 */
(function () {
  'use strict';
  var hero = document.querySelector('.hero-top');
  if (!hero) return;
  var RM = document.documentElement.classList.contains('rm');
  var FIX = /[?&]heroT=([\d.]+)/.exec(location.search); FIX = FIX ? parseFloat(FIX[1]) : null;
  var coarse = window.matchMedia('(pointer: coarse)').matches;
  var cv = document.createElement('canvas');
  cv.className = 'gl-cv';
  cv.setAttribute('aria-hidden', 'true');
  var gl = null;
  try { gl = cv.getContext('webgl2', { antialias: !coarse, alpha: false, powerPreference: 'high-performance' }); } catch (e) { gl = null; }
  if (!gl) return;

  // ───────── 世界をつくる ─────────
  var W = 140, D = 120, SEED = 7.31;
  function h2(x, z) { var s = Math.sin(x * 127.1 + z * 311.7 + SEED) * 43758.5453; return s - Math.floor(s); }
  function vn(x, z) {
    var xi = Math.floor(x), zi = Math.floor(z), xf = x - xi, zf = z - zi;
    var u = xf * xf * (3 - 2 * xf), v = zf * zf * (3 - 2 * zf);
    var a = h2(xi, zi), b = h2(xi + 1, zi), c = h2(xi, zi + 1), d = h2(xi + 1, zi + 1);
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
  }
  function fbm(x, z) { return vn(x, z) * 0.55 + vn(x * 2.1, z * 2.1) * 0.3 + vn(x * 4.3, z * 4.3) * 0.15; }
  var HT = new Float32Array(W * D), WATER = new Uint8Array(W * D);
  for (var z = 0; z < D; z++) for (var x = 0; x < W; x++) {
    var h = 1.2 + fbm(x / 16, z / 16) * 4.6 + Math.max(0, fbm(x / 9 + 4, z / 9) - 0.55) * 6;
    var far = Math.max(0, (z - D * 0.74) / (D * 0.26));
    h += far * far * 13 * (0.4 + fbm(x / 8 + 9, z / 8));
    var lx = (x - W * 0.53) / 24, lz = (z - D * 0.46) / 13;
    var r = Math.sqrt(lx * lx + lz * lz) + (vn(x / 6, z / 6) - 0.5) * 0.7;
    if (r < 1.3) h -= (1.3 - r) * 5.2;
    if (z < 10) h = h * 0.6 + 1.8 * 0.4;
    var i = z * W + x;
    if (h < 0.9) { WATER[i] = 1; HT[i] = 0.78; } else HT[i] = Math.round(h);
  }
  function ground(x, z) {
    var xi = Math.floor(x), zi = Math.floor(z);
    if (xi < 0 || zi < 0 || xi >= W || zi >= D) return -1;
    return HT[zi * W + xi];
  }

  // 灯籠を散らす（間隔をあけて、水辺は多めに）
  var rnd = (function (s) { return function () { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }; })(20261107);
  var LAN = [];
  function nearLan(x, z, d) { for (var k = 0; k < LAN.length; k++) { var dx = LAN[k].cx - x, dz = LAN[k].cz - z; if (dx * dx + dz * dz < d * d) return true; } return false; }
  function shore(x, z) { for (var dz = -2; dz <= 2; dz++) for (var dx = -2; dx <= 2; dx++) { var g = ground(x + dx, z + dz); if (g > 0 && WATER[(z + dz) * W + x + dx]) return true; } return false; }
  for (var tries = 0; tries < 30000 && LAN.length < 230; tries++) {
    var x = 2 + Math.floor(rnd() * (W - 4)), z = 3 + Math.floor(rnd() * (D - 10));
    var i = z * W + x;
    if (WATER[i]) continue;
    var sp = shore(x, z) ? 4.6 : 6.8;
    if (HT[i] > 9) sp += 2;
    if (z < 26) sp += (26 - z) * 0.1;
    if (nearLan(x + 0.5, z + 0.5, sp)) continue;
    LAN.push(mkLan(x, z, z > 28 && rnd() < 0.16 ? [0.95, 0.61, 0.72] : [0.95, 0.71, 0.27]));
  }
  function mkLan(x, z, col) {
    return { x: x, z: z, cx: x + 0.5, cz: z + 0.5, y: HT[z * W + x], col: col, on: 1e9, eat: 0, user: false, par: -1 };
  }
  // 最初の灯籠：右手前（題字にかからない場所）
  var startI = 0, best = 1e9, aspect0 = (hero.clientWidth || 1200) / (hero.clientHeight || 800);
  var sx = aspect0 > 1.2 ? W * 0.4 : W * 0.5, sz = aspect0 > 1.2 ? 20 : 17;
  LAN.forEach(function (l, k) { var d = Math.hypot(l.cx - sx, l.cz - sz); if (d < best) { best = d; startI = k; } });
  // 灯路：最初の灯籠から木を伸ばす（プリム法）。ともる時刻は道の長さで決まる
  var EDGE = [];
  (function () {
    var n = LAN.length, inT = new Uint8Array(n), dist = new Float32Array(n).fill(1e9), par = new Int32Array(n).fill(-1), path = new Float32Array(n);
    dist[startI] = 0;
    for (var it = 0; it < n; it++) {
      var u = -1, m = 1e9;
      for (var k = 0; k < n; k++) if (!inT[k] && dist[k] < m) { m = dist[k]; u = k; }
      if (u < 0) break;
      inT[u] = 1;
      if (par[u] >= 0) { path[u] = path[par[u]] + Math.hypot(LAN[u].cx - LAN[par[u]].cx, LAN[u].cz - LAN[par[u]].cz); LAN[u].par = par[u]; }
      for (var k = 0; k < n; k++) if (!inT[k]) {
        var d = Math.hypot(LAN[u].cx - LAN[k].cx, LAN[u].cz - LAN[k].cz);
        if (d < dist[k]) { dist[k] = d; par[k] = u; }
      }
    }
    var mx = 0; for (var k = 0; k < n; k++) mx = Math.max(mx, path[k]);
    for (var k = 0; k < n; k++) LAN[k].path = path[k] / mx;
    // 木の枝に加えて、近い灯籠どうしも結ぶ
    for (var k = 0; k < n; k++) {
      if (LAN[k].par >= 0) EDGE.push({ a: LAN[k].par, b: k, tree: true });
    }
    for (var a = 0; a < n; a++) for (var b = a + 1; b < n; b++) {
      if (LAN[a].par === b || LAN[b].par === a) continue;
      var d = Math.hypot(LAN[a].cx - LAN[b].cx, LAN[a].cz - LAN[b].cz);
      if (d < 7.2) EDGE.push({ a: a, b: b, tree: false });
    }
  })();
  var T0 = 1.95, SPREAD = 6.4;
  function setTimes() {
    LAN.forEach(function (l, k) { if (!l.user) l.on = k === startI ? T0 : T0 + 0.55 + SPREAD * Math.pow(l.path, 0.8); });
    EDGE.forEach(function (e) {
      var A = LAN[e.a], B = LAN[e.b];
      e.len = Math.hypot(A.cx - B.cx, A.cz - B.cz);
      if (e.tree) { e.t0 = A.on; e.t1 = B.on; } else { e.t0 = Math.max(A.on, B.on); e.t1 = e.t0 + e.len / 9; }
    });
  }
  setTimes();

  // 闇の中の目（灯りから遠いところ）
  var EYES = [];
  for (var tries = 0; tries < 8000 && EYES.length < 34; tries++) {
    var x = 1 + Math.floor(rnd() * (W - 2)), z = 8 + Math.floor(rnd() * (D * 0.6));
    if (WATER[z * W + x] || nearLan(x + 0.5, z + 0.5, 11.5)) continue;
    EYES.push({ x: x + 0.5, z: z + 0.5, y: HT[z * W + x] + 1.45, ph: rnd() * 20, sp: 0.6 + rnd() });
  }

  // ───────── GL の道具 ─────────
  function sh(type, src) {
    var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  }
  function prog(vs, fs) {
    var p = gl.createProgram();
    gl.attachShader(p, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fs));
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
    var u = {}, n = gl.getProgramParameter(p, gl.ACTIVE_UNIFORMS);
    for (var k = 0; k < n; k++) { var a = gl.getActiveUniform(p, k); u[a.name] = gl.getUniformLocation(p, a.name); }
    return { p: p, u: u };
  }
  function buf(data, usage) { var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, data, usage || gl.STATIC_DRAW); return b; }
  function attr(loc, b, size, stride, off, div) {
    gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, size, gl.FLOAT, false, stride * 4, off * 4);
    if (div) gl.vertexAttribDivisor(loc, div);
  }
  // 立方体（底なし）: 位置 0..1 と法線
  function cube(x0, y0, z0, x1, y1, z1, part, out) {
    var F = [
      [[0, 1, 0], [[x0, y1, z0], [x0, y1, z1], [x1, y1, z1], [x1, y1, z0]]],
      [[1, 0, 0], [[x1, y0, z0], [x1, y1, z0], [x1, y1, z1], [x1, y0, z1]]],
      [[-1, 0, 0], [[x0, y0, z1], [x0, y1, z1], [x0, y1, z0], [x0, y0, z0]]],
      [[0, 0, 1], [[x1, y0, z1], [x1, y1, z1], [x0, y1, z1], [x0, y0, z1]]],
      [[0, 0, -1], [[x0, y0, z0], [x0, y1, z0], [x1, y1, z0], [x1, y0, z0]]]
    ];
    F.forEach(function (f) {
      var q = f[1];
      [0, 1, 2, 0, 2, 3].forEach(function (k) { out.push(q[k][0], q[k][1], q[k][2], f[0][0], f[0][1], f[0][2], part); });
    });
  }

  var HDR = '#version 300 es\nprecision highp float;\n';
  var FOG = 'vec3 fogc(vec3 w){vec3 d=normalize(w-uCam);float hz=exp(-abs(d.y)*7.0);return mix(vec3(0.02,0.035,0.09),vec3(0.1,0.13,0.25)+vec3(0.6,0.33,0.12)*uWarm*0.45,hz);}\n';
  var HASH = 'float h21(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}\n';

  // 地形
  var pT = prog(HDR +
    'layout(location=0) in vec3 aP;layout(location=1) in vec3 aN;layout(location=2) in vec4 aI;\n' +
    'uniform mat4 uVP;out vec3 vW;flat out vec3 vN;flat out float vT;flat out float vTop;\n' +
    'void main(){float top=aI.z;vec3 w=vec3(aI.x+aP.x,mix(-10.0,top,aP.y),aI.y+aP.z);vW=w;vN=aN;vT=aI.w;vTop=top;gl_Position=uVP*vec4(w,1.0);}',
    HDR + 'in vec3 vW;flat in vec3 vN;flat in float vT;flat in float vTop;\n' +
    'uniform sampler2D uL;uniform vec2 uWD;uniform vec3 uCam;uniform float uTime;uniform float uWarm;uniform float uAmb;uniform float uFlash;out vec4 o;\n' +
    HASH + FOG +
    'vec3 L(vec2 c){return texture(uL,(clamp(c,vec2(0.0),uWD-1.0)+0.5)/uWD).rgb*2.0;}\n' +
    'void main(){vec3 n=vN;vec2 cell=floor(vW.xz+n.xz*0.5);\n' +
    ' if(n.y>0.5)cell=floor(vW.xz);\n' +
    ' vec3 li=L(cell);\n' +
    ' vec2 uv=n.y>0.5?vW.xz:(abs(n.x)>0.5?vec2(vW.z,vW.y):vec2(vW.x,vW.y));\n' +
    ' vec2 px=floor(uv*8.0);float r=h21(px+floor(vW.xz)*7.13+floor(vW.y)*3.1);\n' +
    ' float face=n.y>0.5?1.0:(abs(n.x)>0.5?0.74:0.6);\n' +
    ' vec3 base;\n' +
    ' if(vT>0.5){\n' +
    '  vec2 q=floor(vW.xz*5.0);float rip=h21(q+floor(uTime*2.0+h21(q)*4.0));\n' +
    '  vec3 v=normalize(uCam-vW);float fr=pow(1.0-max(v.y,0.0),3.0);\n' +
    '  vec3 c=vec3(0.012,0.03,0.08)*uAmb+li*(0.22+0.8*step(0.74,rip))*vec3(1.0,0.9,0.75);\n' +
    '  c+=fogc(vW*vec3(1.0,-1.0,1.0)+vec3(0.0,1.6,0.0))*fr*0.7*uAmb;\n' +
    '  float d=length(vW-uCam);c=mix(c,fogc(vW),(1.0-exp(-d*0.012))*0.95);o=vec4(1.0-exp(-c*1.25),1.0);return;}\n' +
    ' if(n.y>0.5){base=mix(vec3(0.24,0.42,0.16),vec3(0.34,0.55,0.21),r);if(r>0.93)base=vec3(0.45,0.62,0.27);}\n' +
    ' else{float dy=vTop-vW.y;if(dy<0.2)base=mix(vec3(0.25,0.43,0.17),vec3(0.31,0.5,0.19),r);else if(dy<3.0)base=mix(vec3(0.29,0.2,0.13),vec3(0.37,0.26,0.17),r);else base=mix(vec3(0.27,0.28,0.31),vec3(0.38,0.39,0.42),r);}\n' +
    ' vec3 amb=vec3(0.04,0.06,0.15)*(0.45+0.55*face)*uAmb;\n' +
    ' vec3 c=base*(amb*0.9+li*1.7*face)+li*li*0.06+vec3(0.6,0.38,0.15)*uFlash*0.3*face;\n' +
    ' float d=length(vW-uCam);c=mix(c,fogc(vW),(1.0-exp(-d*0.012))*0.95);\n' +
    ' o=vec4(1.0-exp(-c*1.25),1.0);}');

  // 灯籠
  var pL = prog(HDR +
    'layout(location=0) in vec3 aP;layout(location=1) in vec3 aN;layout(location=2) in float aPart;layout(location=3) in vec4 aI;layout(location=4) in vec4 aC;\n' +
    'uniform mat4 uVP;out vec3 vW;out vec3 vLoc;flat out vec3 vN;flat out float vPart;flat out vec4 vI;flat out vec4 vC;\n' +
    'void main(){vec3 w=vec3(aI.x,aI.y,aI.z)+aP;vW=w;vLoc=aP;vN=aN;vPart=aPart;vI=aI;vC=aC;gl_Position=uVP*vec4(w,1.0);}',
    HDR + 'in vec3 vW;in vec3 vLoc;flat in vec3 vN;flat in float vPart;flat in vec4 vI;flat in vec4 vC;uniform vec3 uCam;uniform float uWarm;uniform float uAmb;out vec4 o;\n' + FOG +
    'void main(){float face=vN.y>0.5?1.0:(abs(vN.x)>0.5?0.76:0.6);vec3 wood=vec3(0.16,0.11,0.08)*face;\n' +
    ' vec3 c=wood*(0.35*uAmb+vI.w*1.2);\n' +
    ' if(vPart>0.5){vec2 q=vN.y>0.5?vLoc.xz:(abs(vN.x)>0.5?vec2(vLoc.z,vLoc.y):vec2(vLoc.x,vLoc.y));\n' +
    '  vec2 e=abs(fract((q-vec2(-0.25,1.1))/vec2(0.5,0.62))-0.5);float inner=step(max(e.x,e.y),0.32);\n' +
    '  c=mix(c,vC.rgb*(0.03+2.4*vI.w),inner);}\n' +
    ' float d=length(vW-uCam);c=mix(c,fogc(vW),(1.0-exp(-d*0.012))*0.85);o=vec4(1.0-exp(-c*1.3),1.0);}');

  // 光の粒（灯りのにじみ・灯路・火の粉・目）
  var pB = prog(HDR +
    'layout(location=0) in vec2 aQ;layout(location=1) in vec4 aC;layout(location=2) in vec4 aK;\n' +
    'uniform mat4 uV;uniform mat4 uP;out vec2 vQ;out vec4 vK;out float vF;\n' +
    'void main(){vec4 v=uV*vec4(aC.xyz,1.0);float s=abs(aC.w);v.xy+=aQ*s;vQ=aQ;vK=aK;vK.a*=sign(aC.w);vF=exp(-max(-v.z,0.0)*0.005);gl_Position=uP*v;}',
    HDR + 'in vec2 vQ;in vec4 vK;in float vF;out vec4 o;\n' +
    'void main(){float a;if(vK.a<0.0){a=1.0;}else{float r=length(vQ);a=max(0.0,1.0-r);a=a*a*a;}\n' +
    ' o=vec4(vK.rgb*abs(vK.a)*a*vF,1.0);}');

  // 空
  var pS = prog(HDR + 'layout(location=0) in vec2 aQ;out vec2 vU;void main(){vU=aQ;gl_Position=vec4(aQ,0.9999,1.0);}',
    HDR + 'in vec2 vU;uniform vec3 uR;uniform vec3 uU;uniform vec3 uF;uniform vec2 uTan;uniform float uShift;uniform float uTime;uniform float uWarm;uniform float uAmb;uniform vec3 uMd;out vec4 o;\n' + HASH +
    'void main(){vec3 d=normalize(uF+uR*vU.x*uTan.x+uU*(vU.y-uShift)*uTan.y);\n' +
    ' float t=clamp(d.y*1.7+0.04,0.0,1.0);vec3 c=mix(vec3(0.15,0.21,0.37),vec3(0.025,0.045,0.11),pow(t,0.7));\n' +
    ' c+=vec3(0.75,0.42,0.16)*uWarm*exp(-max(d.y,0.0)*16.0)*0.42;\n' +
    ' c*=uAmb;\n' +
    ' vec2 g=vec2(atan(d.x,d.z),asin(clamp(d.y,-1.0,1.0)))*57.3*1.6;vec2 ce=floor(g);vec2 f=fract(g)-0.5;float h=h21(ce);\n' +
    ' if(h>0.955&&d.y>0.03){float s=0.06+0.1*h21(ce+3.1)*h21(ce+3.1);float tw=0.55+0.45*sin(uTime*(0.8+h*3.0)+h*60.0);c+=vec3(0.9,0.93,1.0)*step(max(abs(f.x),abs(f.y)),s)*tw*smoothstep(0.03,0.2,d.y)*uAmb;}\n' +
    ' vec3 md=uMd;vec3 mr=normalize(cross(vec3(0.0,1.0,0.0),md));vec3 mu=cross(md,mr);\n' +
    ' vec2 q=vec2(dot(d,mr),dot(d,mu));float mq=max(abs(q.x),abs(q.y));\n' +
    ' if(dot(d,md)>0.0){c+=vec3(0.55,0.62,0.8)*exp(-length(q)*22.0)*0.18*uAmb;\n' +
    '  if(mq<0.021){vec2 k=floor((q+0.021)/0.00525);float cr=(k.x==2.0&&k.y==5.0)||(k.x==3.0&&k.y==5.0)||(k.x==5.0&&k.y==2.0)||(k.x==2.0&&k.y==6.0)?1.0:0.0;c=mix(vec3(0.8,0.83,0.88),vec3(0.55,0.59,0.67),cr)*mix(0.3,1.0,uAmb);}}\n' +
    ' o=vec4(1.0-exp(-c*1.25),1.0);}');

  // ── 形をGPUへ ──
  var cubeV = []; cube(0, 0, 0, 1, 1, 1, 0, cubeV);
  var cubeB = buf(new Float32Array(cubeV));
  var nCube = cubeV.length / 7;
  var inst = [];
  for (var z = 0; z < D; z++) for (var x = 0; x < W; x++) { var i = z * W + x; inst.push(x, z, HT[i], WATER[i]); }
  var instB = buf(new Float32Array(inst));
  var vaoT = gl.createVertexArray(); gl.bindVertexArray(vaoT);
  attr(0, cubeB, 3, 7, 0); attr(1, cubeB, 3, 7, 3); attr(2, instB, 4, 4, 0, 1);

  var lanV = [];
  cube(-0.07, 0, -0.07, 0.07, 1.1, 0.07, 0, lanV);
  cube(-0.25, 1.1, -0.25, 0.25, 1.72, 0.25, 1, lanV);
  cube(-0.31, 1.72, -0.31, 0.31, 1.84, 0.31, 0, lanV);
  var lanB = buf(new Float32Array(lanV)), nLan = lanV.length / 7;
  var MAXL = 300;
  var lanI = new Float32Array(MAXL * 8), lanIB = buf(lanI, gl.DYNAMIC_DRAW);
  var vaoL = gl.createVertexArray(); gl.bindVertexArray(vaoL);
  attr(0, lanB, 3, 7, 0); attr(1, lanB, 3, 7, 3); attr(2, lanB, 1, 7, 6);
  attr(3, lanIB, 4, 8, 0, 1); attr(4, lanIB, 4, 8, 4, 1);

  var quadB = buf(new Float32Array([-1, -1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1]));
  var MAXB = 14000;
  var bb = new Float32Array(MAXB * 8), bbB = buf(bb, gl.DYNAMIC_DRAW);
  var vaoB = gl.createVertexArray(); gl.bindVertexArray(vaoB);
  attr(0, quadB, 2, 2, 0); attr(1, bbB, 4, 8, 0, 1); attr(2, bbB, 4, 8, 4, 1);
  var vaoS = gl.createVertexArray(); gl.bindVertexArray(vaoS);
  attr(0, buf(new Float32Array([-1, -1, 3, -1, -1, 3])), 2, 2, 0);
  gl.bindVertexArray(null);

  var lightTex = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, lightTex);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, W, D, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  var LF = new Float32Array(W * D * 3), LB = new Uint8Array(W * D * 4);


  // ── 仕上げの光（にじみ）：画面外に描いて、明るいところをぼかして重ねる ──
  var VQ = HDR + 'layout(location=0) in vec2 aQ;out vec2 vU;void main(){vU=aQ*0.5+0.5;gl_Position=vec4(aQ,0.0,1.0);}';
  var pBright = prog(VQ, HDR + 'in vec2 vU;uniform sampler2D uT;uniform vec2 uPx;out vec4 o;\n' +
    'void main(){vec3 c=vec3(0.0);for(int i=0;i<4;i++){vec2 d=vec2(float(i%2)-0.5,float(i/2)-0.5)*uPx*2.0;vec3 s=texture(uT,vU+d).rgb;float l=max(s.r,max(s.g,s.b));c+=s*smoothstep(0.55,0.95,l);}o=vec4(c*0.25,1.0);}');
  var pBlur = prog(VQ, HDR + 'in vec2 vU;uniform sampler2D uT;uniform vec2 uDir;out vec4 o;\n' +
    'void main(){vec3 c=texture(uT,vU).rgb*0.227;c+=(texture(uT,vU+uDir*1.385).rgb+texture(uT,vU-uDir*1.385).rgb)*0.316;c+=(texture(uT,vU+uDir*3.23).rgb+texture(uT,vU-uDir*3.23).rgb)*0.07;o=vec4(c,1.0);}');
  var pComp = prog(VQ, HDR + 'in vec2 vU;uniform sampler2D uT;uniform sampler2D uB;uniform sampler2D uB2;uniform float uTime;uniform float uK;uniform vec2 uAsp;uniform float uDig;uniform float uGY;uniform float uCell;uniform vec2 uRes;uniform float uOff;uniform float uTun;uniform float uR0;out vec4 o;\n' + HASH +
    'void main(){vec2 c0=vU-0.5;float r2=dot(c0*uAsp,c0*uAsp);\n' +
    ' vec2 ca=c0*r2*0.006;vec3 c=vec3(texture(uT,vU+ca).r,texture(uT,vU).g,texture(uT,vU-ca).b);\n' +
    ' vec3 b=texture(uB,vU).rgb*1.1+texture(uB2,vU).rgb*1.5;c+=b*uK;\n' +
    ' c=mix(c,c*vec3(0.92,0.97,1.12),smoothstep(0.35,0.0,max(c.r,max(c.g,c.b))));\n' +
    ' c*=1.0-r2*0.55;\n' +
    ' c+=(h21(vU*vec2(1913.0,1771.0)+fract(uTime*7.0)*91.0)-0.5)*0.035*(1.0-uDig);\n' +
    ' if(uDig>0.0){vec2 px=vec2(gl_FragCoord.x,uRes.y-gl_FragCoord.y);vec2 q=vec2(px.x,px.y-uGY-uOff);vec2 cell=floor(q/uCell);vec2 f=q-cell*uCell;\n' +
    '  float yb=clamp((uRes.y-(cell.y*uCell+uGY+uOff))/uRes.y,0.0,1.0);float th=h21(cell+7.0)*0.55+yb*0.45;\n' +
    '  float k=smoothstep(th*0.9,th*0.9+0.12,uDig*1.1);\n' +
    '  vec3 soil=vec3(0.2275,0.1647,0.1255);float ln=(f.x<uCell/26.0||f.y<uCell/26.0)?0.91:1.0;\n' +
    '  if(cell.y<-uR0){float band=floor(cell.y/3.0);float bt=h21(vec2(band,5.0));float deep=clamp((-cell.y-uR0)/12.0,0.0,1.0);\n' +
    '   vec2 sp=floor(f/(uCell/8.0));float n=h21(sp+cell*17.3);\n' +
    '   vec3 b=bt<0.4?soil:(bt<0.75?vec3(0.27,0.28,0.3):vec3(0.2,0.21,0.23));b=mix(soil,b,deep)*(0.92+0.1*n);\n' +
    '   soil=b;}\n' +
    '  soil*=ln;\n' +
    '  float pre=smoothstep(th*0.9-0.2,th*0.9,uDig*1.1);c*=1.0-0.45*pre;\n' +
    '  c=mix(c,soil,k);}\n' +
    ' o=vec4(c,1.0);}');
  var vaoQ = gl.createVertexArray(); gl.bindVertexArray(vaoQ);
  attr(0, buf(new Float32Array([-1, -1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1])), 2, 2, 0);
  gl.bindVertexArray(null);
  function tex(w, h) {
    var t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, w, h, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    var f = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, f);
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, t, 0);
    return { t: t, f: f, w: w, h: h };
  }
  var RT = null, MS = 0;
  try { MS = coarse ? 0 : Math.min(4, gl.getParameter(gl.MAX_SAMPLES) || 0); } catch (e) { MS = 0; }
  function targets() {
    if (RT) { [RT.a, RT.b1, RT.b2, RT.c1, RT.c2].forEach(function (x) { gl.deleteTexture(x.t); gl.deleteFramebuffer(x.f); }); if (RT.ms) { gl.deleteFramebuffer(RT.ms); gl.deleteRenderbuffer(RT.mc); } gl.deleteRenderbuffer(RT.dep); }
    RT = {};
    RT.a = tex(cw, ch);
    if (MS > 1) {
      RT.ms = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, RT.ms);
      RT.mc = gl.createRenderbuffer(); gl.bindRenderbuffer(gl.RENDERBUFFER, RT.mc); gl.renderbufferStorageMultisample(gl.RENDERBUFFER, MS, gl.RGBA8, cw, ch);
      gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.RENDERBUFFER, RT.mc);
      RT.dep = gl.createRenderbuffer(); gl.bindRenderbuffer(gl.RENDERBUFFER, RT.dep); gl.renderbufferStorageMultisample(gl.RENDERBUFFER, MS, gl.DEPTH_COMPONENT24, cw, ch);
      gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, RT.dep);
      if (gl.checkFramebufferStatus(gl.FRAMEBUFFER) !== gl.FRAMEBUFFER_COMPLETE) { MS = 0; return targets(); }
    } else {
      gl.bindFramebuffer(gl.FRAMEBUFFER, RT.a.f);
      RT.dep = gl.createRenderbuffer(); gl.bindRenderbuffer(gl.RENDERBUFFER, RT.dep); gl.renderbufferStorage(gl.RENDERBUFFER, gl.DEPTH_COMPONENT24, cw, ch);
      gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, RT.dep);
    }
    var w4 = Math.max(1, cw >> 2), h4 = Math.max(1, ch >> 2), w8 = Math.max(1, cw >> 3), h8 = Math.max(1, ch >> 3);
    RT.b1 = tex(w4, h4); RT.b2 = tex(w4, h4); RT.c1 = tex(w8, h8); RT.c2 = tex(w8, h8);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  }
  function pass(p, dst, srcs, set) {
    gl.bindFramebuffer(gl.FRAMEBUFFER, dst ? dst.f : null);
    gl.viewport(0, 0, dst ? dst.w : cw, dst ? dst.h : ch);
    gl.useProgram(p.p);
    srcs.forEach(function (s, k) { gl.activeTexture(gl.TEXTURE0 + k); gl.bindTexture(gl.TEXTURE_2D, s.t); });
    if (set) set(p.u);
    gl.bindVertexArray(vaoQ); gl.drawArrays(gl.TRIANGLES, 0, 6);
  }
  function blur(a, b) {
    pass(pBlur, b, [a], function (u) { gl.uniform1i(u.uT, 0); gl.uniform2f(u.uDir, 1 / a.w, 0); });
    pass(pBlur, a, [b], function (u) { gl.uniform1i(u.uT, 0); gl.uniform2f(u.uDir, 0, 1 / a.h); });
  }
  function compU(t) { return function (u) { gl.uniform1i(u.uT, 0); gl.uniform1i(u.uB, 1); gl.uniform1i(u.uB2, 2); gl.uniform1f(u.uTime, t); gl.uniform1f(u.uK, 1.0); gl.uniform2f(u.uAsp, Math.min(1, aspect), Math.min(1, 1 / aspect)); gl.uniform1f(u.uDig, dig); gl.uniform1f(u.uGY, gridY); gl.uniform1f(u.uOff, tunOff); gl.uniform1f(u.uTun, tun); gl.uniform1f(u.uR0, rowsR0); gl.uniform1f(u.uCell, 52 * dpr0); gl.uniform2f(u.uRes, cw, ch); }; }
  function post(t) {
    if (dig >= 1) { gl.disable(gl.DEPTH_TEST); gl.disable(gl.BLEND); pass(pComp, null, [RT.a, RT.b1, RT.c1], compU(t)); return; }
    if (RT.ms) {
      gl.bindFramebuffer(gl.READ_FRAMEBUFFER, RT.ms); gl.bindFramebuffer(gl.DRAW_FRAMEBUFFER, RT.a.f);
      gl.blitFramebuffer(0, 0, cw, ch, 0, 0, cw, ch, gl.COLOR_BUFFER_BIT, gl.NEAREST);
      gl.bindFramebuffer(gl.READ_FRAMEBUFFER, null); gl.bindFramebuffer(gl.DRAW_FRAMEBUFFER, null);
    }
    gl.disable(gl.DEPTH_TEST); gl.disable(gl.BLEND);
    pass(pBright, RT.b1, [RT.a], function (u) { gl.uniform1i(u.uT, 0); gl.uniform2f(u.uPx, 1 / cw, 1 / ch); });
    blur(RT.b1, RT.b2); blur(RT.b1, RT.b2);
    pass(pBlur, RT.c1, [RT.b1], function (u) { gl.uniform1i(u.uT, 0); gl.uniform2f(u.uDir, 0, 0); });
    blur(RT.c1, RT.c2); blur(RT.c1, RT.c2);
    pass(pComp, null, [RT.a, RT.b1, RT.c1], compU(t));
  }

  // ───────── 行列 ─────────
  function norm(v) { var l = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / l, v[1] / l, v[2] / l]; }
  function cross(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
  function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function mul(a, b) { var o = new Float32Array(16); for (var c = 0; c < 4; c++) for (var r = 0; r < 4; r++) { var s = 0; for (var k = 0; k < 4; k++) s += a[k * 4 + r] * b[c * 4 + k]; o[c * 4 + r] = s; } return o; }
  var cam = { e: [0, 0, 0], f: [0, 0, 1], s: [1, 0, 0], u: [0, 1, 0], tanY: 0.4, tanX: 0.6, shift: 0, V: null, P: null, VP: null };

  // ───────── 大きさ ─────────
  var spacer = hero.querySelector('.scene');
  var quality = 1, slow = 0, frames = 0;
  var cw = 0, ch = 0, aspect = 1.5, wide = true, dpr0 = 1;
  // 掘り進む：トップのあとの余白（.dive）と、その下の土の章
  var dive = hero.nextElementSibling && hero.nextElementSibling.classList.contains('dive') ? hero.nextElementSibling : null;
  var soil = dive ? dive.nextElementSibling : null;
  var dig = 0, gridY = 0, tun = 0, tunOff = 0, rowsR0 = 20;
  var depthEl = null;
  function size() {
    var w = cv.clientWidth || window.innerWidth, h = cv.clientHeight || window.innerHeight;
    var dpr = Math.min(window.devicePixelRatio || 1, coarse ? 1.5 : 1.75) * quality;
    if (w * h * dpr * dpr > 3.2e6 * quality) dpr = Math.sqrt(3.2e6 * quality / (w * h));
    cw = Math.round(w * dpr); ch = Math.round(h * dpr);
    cv.width = cw; cv.height = ch;
    targets();
    aspect = w / h; wide = aspect > 1.2;
    var sp = spacer ? spacer.offsetHeight : 260;
    cam.frac = wide ? 0.6 : 0.58;
    cam.moon = 1 - 2 * (wide ? 0.17 : 0.24);
    dpr0 = dpr;
    if (RM || !running) draw(now());
  }

  // ───────── 状態 ─────────
  var start = performance.now();
  function now() { return FIX !== null ? FIX : RM ? 60 : (performance.now() - start) / 1000; }
  var running = false, visible = true, scrollP = 0;
  var ptr = { on: false, x: 0, y: 0, sx: 0, sy: 0, cell: null };
  var flash = [], embers = [], user = 0;
  var ev = { next: T0 + SPREAD + 6, j: -1, ph: 0, t: 0, ex: 0, ez: 0 };
  var hud = document.createElement('div');
  hud.className = 'gl-hud dot';
  hud.setAttribute('aria-hidden', 'true');
  hud.innerHTML = '<span>灯籠 <b data-h="l">0</b></span><span>灯路 <b data-h="r">0</b></span><em data-h="e"></em>';
  var hl = hud.querySelector('[data-h=l]'), hr = hud.querySelector('[data-h=r]'), he = hud.querySelector('[data-h=e]');
  var lastL = -1, lastR = -1, evT = 0;
  function say(t) { he.textContent = t; he.classList.remove('on'); void he.offsetWidth; he.classList.add('on'); evT = now(); }

  function ign(l, t) {
    if (t < l.on) return 0;
    var k = Math.min(1, (t - l.on) / 0.35);
    return k * (1 + 0.9 * Math.exp(-(t - l.on) * 5));
  }
  function flick(k, t) { return 0.9 + 0.06 * Math.sin(t * 7.3 + k * 1.7) + 0.04 * Math.sin(t * 13.1 + k * 3.3); }
  function edgeOk(e) { return LAN[e.a].eat < 0.5 && LAN[e.b].eat < 0.5; }

  function lightMap(t) {
    LF.fill(0);
    var R = 6.8;
    function add(cx, cz, I, c, R) {
      var x0 = Math.max(0, Math.floor(cx - R)), x1 = Math.min(W - 1, Math.floor(cx + R)), z0 = Math.max(0, Math.floor(cz - R)), z1 = Math.min(D - 1, Math.floor(cz + R));
      for (var z = z0; z <= z1; z++) for (var x = x0; x <= x1; x++) {
        var dx = Math.abs(x + 0.5 - cx), dz = Math.abs(z + 0.5 - cz);
        var d = (Math.max(dx, dz) + dx + dz) * 0.5;
        var v = 1 - d / R; if (v <= 0) continue;
        v = Math.round(Math.pow(v, 1.8) * 15) / 15 * I;
        var i = (z * W + x) * 3; LF[i] += c[0] * v; LF[i + 1] += c[1] * v; LF[i + 2] += c[2] * v;
      }
    }
    for (var k = 0; k < LAN.length; k++) {
      var l = LAN[k], I = ign(l, t);
      if (I <= 0) continue;
      var e = l.eat, c = [l.col[0] * (1 - e) + 0.35 * e, l.col[1] * (1 - e) + 0.62 * e, l.col[2] * (1 - e) + 1.0 * e];
      add(l.cx, l.cz, I * flick(k, t) * (1 - 0.55 * e), c, R * (1 - 0.3 * e));
    }
    for (var k = 0; k < flash.length; k++) { var f = flash[k], a = t - f.t; if (a > 0 && a < 1.2) add(f.x, f.z, (1 - a / 1.2) * f.I, f.c, 12); }
    if (ptr.cell && !coarse) add(ptr.cell[0], ptr.cell[1], 0.55, [1, 0.86, 0.62], 6);
    for (var i = 0, j = 0; i < W * D; i++, j += 3) {
      LB[i * 4] = Math.min(255, LF[j] * 127); LB[i * 4 + 1] = Math.min(255, LF[j + 1] * 127); LB[i * 4 + 2] = Math.min(255, LF[j + 2] * 127); LB[i * 4 + 3] = 255;
    }
    gl.bindTexture(gl.TEXTURE_2D, lightTex);
    gl.texSubImage2D(gl.TEXTURE_2D, 0, 0, 0, W, D, gl.RGBA, gl.UNSIGNED_BYTE, LB);
  }
  function lightAt(x, z) { var xi = Math.floor(x), zi = Math.floor(z); if (xi < 0 || zi < 0 || xi >= W || zi >= D) return 0; var j = (zi * W + xi) * 3; return Math.max(LF[j], LF[j + 1], LF[j + 2]); }

  // カメラ
  function camera(t) {
    var k = RM ? 1 : Math.min(1, t / 9), e = 1 - Math.pow(1 - k, 3);
    var tx = wide ? W * 0.55 : W * 0.53, tz = wide ? D * 0.42 : D * 0.4;
    var ex = wide ? W * 0.46 : W * 0.51, ey = wide ? 15 : 19, ez = wide ? -3 : -8;
    var b0 = norm([tx - ex, 1 - ey, tz - ez]), bs = norm(cross(b0, [0, 1, 0])), bu = cross(bs, b0);
    ex += (1 - e) * -4; ey += (1 - e) * 9; ez += (1 - e) * -14;
    if (!RM) { ex += Math.sin(t * 0.11) * 1.4; ey += Math.sin(t * 0.17) * 0.4; }
    ptr.sx += (ptr.x - ptr.sx) * 0.04; ptr.sy += (ptr.y - ptr.sy) * 0.04;
    if (!coarse) { ex += ptr.sx * 2.2; ey -= ptr.sy * 1.0; }
    var ty = 1;
    // 下へ：最初の灯籠の足もとへ降りていき、真上から見下ろす
    var dp = !dive || scrollP < 0.03 ? 0 : Math.min(1, (scrollP - 0.03) / 0.37), de = dp * dp * (3 - 2 * dp);
    if (de > 0) {
      var L0 = LAN[startI];
      var dx = L0.cx + 0.2, dy = L0.y + 2.6, dz = L0.cz - 1.1;
      ex += (dx - ex) * de; ey += (dy - ey) * de; ez += (dz - ez) * de;
      tx += (L0.cx - tx) * de; ty += (L0.y - ty) * de; tz += (L0.cz + 0.35 - tz) * de;
    }
    var eye = [ex, ey, ez], f = norm([tx - ex, ty - ey, tz - ez]), s = norm(cross(f, [0, 1, 0])), u = cross(s, f);
    var fov = wide ? 44 : 58;
    if (!wide && aspect < 0.7) fov = 64;
    var tanY = Math.tan(fov * Math.PI / 360), n = 0.3, fr = 320;
    var ff = 1 / tanY, shift = 1 - 2 * cam.frac;
    var P = new Float32Array([ff / aspect, 0, 0, 0, 0, ff, 0, 0, 0, -shift, (fr + n) / (n - fr), -1, 0, 0, 2 * fr * n / (n - fr), 0]);
    var V = new Float32Array([s[0], u[0], -f[0], 0, s[1], u[1], -f[1], 0, s[2], u[2], -f[2], 0, -dot(s, eye), -dot(u, eye), dot(f, eye), 1]);
    var mx = wide ? 0.52 : 0.52, my = cam.moon - shift, tX = tanY * aspect;
    cam.md = norm([b0[0] + bs[0] * mx * tX + bu[0] * my * tanY, b0[1] + bs[1] * mx * tX + bu[1] * my * tanY, b0[2] + bs[2] * mx * tX + bu[2] * my * tanY]);
    cam.e = eye; cam.f = f; cam.s = s; cam.u = u; cam.tanY = tanY; cam.tanX = tanY * aspect; cam.shift = shift; cam.V = V; cam.P = P; cam.VP = mul(P, V);
  }
  function ray(nx, ny) {
    var d = norm([cam.f[0] + cam.s[0] * nx * cam.tanX + cam.u[0] * (ny - cam.shift) * cam.tanY, cam.f[1] + cam.s[1] * nx * cam.tanX + cam.u[1] * (ny - cam.shift) * cam.tanY, cam.f[2] + cam.s[2] * nx * cam.tanX + cam.u[2] * (ny - cam.shift) * cam.tanY]);
    var p = cam.e.slice();
    for (var k = 0; k < 900; k++) {
      p[0] += d[0] * 0.2; p[1] += d[1] * 0.2; p[2] += d[2] * 0.2;
      var g = ground(p[0], p[2]);
      if (g >= 0 && p[1] <= g) return [Math.floor(p[0]), Math.floor(p[2])];
      if (p[1] < -2) return null;
    }
    return null;
  }

  // 光の粒を積む
  var nb = 0;
  function B(x, y, z, s, r, g, b, a, sq) {
    if (nb >= MAXB) return;
    var o = nb++ * 8;
    bb[o] = x; bb[o + 1] = y; bb[o + 2] = z; bb[o + 3] = sq ? -s : s; bb[o + 4] = r; bb[o + 5] = g; bb[o + 6] = b; bb[o + 7] = a;
  }
  function road(t) {
    var nr = 0;
    for (var k = 0; k < EDGE.length; k++) {
      var e = EDGE[k];
      if (t < e.t0) continue;
      var p = Math.min(1, (t - e.t0) / Math.max(0.05, e.t1 - e.t0));
      var A = LAN[e.a], Bn = LAN[e.b], ok = edgeOk(e);
      if (p >= 1 && ok) nr++;
      var n = Math.max(2, Math.round(e.len * 2.4)), base = ok ? 1 : 0.22;
      var cr = ok ? 0.98 : 0.35, cg = ok ? 0.74 : 0.6, cb = ok ? 0.36 : 1;
      for (var q = 0; q <= n; q++) {
        var s = q / n; if (s > p) break;
        var x = A.cx + (Bn.cx - A.cx) * s, z = A.cz + (Bn.cz - A.cz) * s;
        var y = Math.max(A.y + (Bn.y - A.y) * s, ground(x, z)) + 0.12;
        var fl = 0.55 + 0.45 * Math.sin((s * e.len - t * 2.2) * 1.6);
        B(x, y, z, 0.055, cr, cg, cb, base * (0.6 + 0.9 * fl * ok), true);
      }
      if (p < 1) {
        var x = A.cx + (Bn.cx - A.cx) * p, z = A.cz + (Bn.cz - A.cz) * p, y = Math.max(A.y + (Bn.y - A.y) * p, ground(x, z)) + 0.35;
        B(x, y, z, 1.5, 1, 0.78, 0.4, 0.75);
        B(x, y, z, 0.12, 1, 0.95, 0.8, 2, true);
      }
    }
    return nr;
  }

  function step(t, dt) {
    // 灯喰いの出来事
    if (!RM && t > ev.next && ev.ph === 0) {
      var cand = [];
      LAN.forEach(function (l, k) { if (k !== startI && !l.user && l.eat === 0 && t > l.on + 1 && l.cz > 14 && l.cz < 44) cand.push(k); });
      if (cand.length) {
        ev.j = cand[Math.floor(Math.random() * cand.length)];
        var a = Math.random() * Math.PI * 2, l = LAN[ev.j];
        ev.ex = l.cx + Math.cos(a) * 7; ev.ez = l.cz + Math.sin(a) * 7; ev.ph = 1; ev.t = t;
      } else ev.next = t + 5;
    }
    if (ev.ph) {
      var l = LAN[ev.j], a = t - ev.t;
      if (ev.ph === 1 && a > 2.4) { ev.ph = 2; ev.t = t; say('灯喰いが、灯籠を喰った'); for (var k = 0; k < 26; k++) embers.push(ember(l.cx, l.y + 1.4, l.cz, [0.7, 0.42, 1], 2.2)); }
      if (ev.ph === 2) { l.eat = Math.min(1, a / 0.4); if (a > 4.6) { ev.ph = 3; ev.t = t; flash.push({ x: l.cx, z: l.cz, t: t, I: 1.4, c: l.col }); say('だれかが、灯し直した'); } }
      if (ev.ph === 3) { l.eat = Math.max(0, 1 - a / 0.25); if (a > 0.3) { l.eat = 0; ev.ph = 0; ev.next = t + 7 + Math.random() * 5; } }
    }
    // 火の粉
    if (!RM && embers.length < 260) {
      for (var k = 0; k < 4; k++) {
        var j = Math.floor(Math.random() * LAN.length), l = LAN[j];
        if (t > l.on + 0.3 && l.eat < 0.5) embers.push(ember(l.cx + (Math.random() - 0.5) * 0.4, l.y + 1.6, l.cz + (Math.random() - 0.5) * 0.4, l.col, 1));
      }
    }
    for (var k = embers.length - 1; k >= 0; k--) {
      var m = embers[k]; m.a += dt;
      if (m.a > m.life) { embers.splice(k, 1); continue; }
      m.x += (m.vx + Math.sin(m.a * 2 + m.ph) * 0.25) * dt; m.y += m.vy * dt; m.z += m.vz * dt;
    }
    flash = flash.filter(function (f) { return t - f.t < 1.3; });
  }
  function ember(x, y, z, c, burst) {
    var b = burst > 1;
    return { x: x, y: y, z: z, vx: b ? (Math.random() - 0.5) * 3 : 0, vy: b ? 0.6 + Math.random() * 2 : 0.4 + Math.random() * 0.7, vz: b ? (Math.random() - 0.5) * 3 : 0, a: 0, life: b ? 0.8 + Math.random() * 0.6 : 1.8 + Math.random() * 2.2, ph: Math.random() * 6, c: c };
  }

  var last = 0;
  function draw(t) {
    var dt = Math.min(0.05, Math.max(0, t - last)); last = t;
    if (!RM) step(t, dt);
    camera(t);
    if (dig >= 1) { gl.bindVertexArray(null); post(t); return; }
    lightMap(t);
    var amb = RM ? 1 : Math.min(1, Math.max(0.12, (t - 0.5) / 1.6));
    var litN = 0;
    for (var k = 0; k < LAN.length; k++) if (t >= LAN[k].on && LAN[k].eat < 0.5) litN++;
    var warm = Math.min(1, litN / 50);
    var f0 = t - T0, flashG = f0 > 0 && f0 < 1.6 ? Math.exp(-f0 * 3) : 0;

    gl.bindFramebuffer(gl.FRAMEBUFFER, RT.ms || RT.a.f);
    gl.viewport(0, 0, cw, ch);
    gl.clearColor(0, 0, 0, 1);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.enable(gl.DEPTH_TEST); gl.depthMask(true); gl.disable(gl.BLEND);
    gl.disable(gl.CULL_FACE);

    // 地形
    gl.useProgram(pT.p);
    gl.uniformMatrix4fv(pT.u.uVP, false, cam.VP);
    gl.uniform2f(pT.u.uWD, W, D); gl.uniform3fv(pT.u.uCam, cam.e);
    gl.uniform1f(pT.u.uTime, t); gl.uniform1f(pT.u.uWarm, warm); gl.uniform1f(pT.u.uAmb, amb); gl.uniform1f(pT.u.uFlash, flashG);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, lightTex); gl.uniform1i(pT.u.uL, 0);
    gl.bindVertexArray(vaoT);
    gl.drawArraysInstanced(gl.TRIANGLES, 0, nCube, W * D);

    // 灯籠
    var nl = 0;
    for (var k = 0; k < LAN.length && nl < MAXL; k++) {
      var l = LAN[k], I = Math.min(1.4, ign(l, t)) * (1 - 0.6 * l.eat), o = nl++ * 8, e = l.eat;
      lanI[o] = l.cx; lanI[o + 1] = l.y; lanI[o + 2] = l.cz; lanI[o + 3] = I * (I > 0 ? flick(k, t) : 1);
      lanI[o + 4] = l.col[0] * (1 - e) + 0.35 * e; lanI[o + 5] = l.col[1] * (1 - e) + 0.66 * e; lanI[o + 6] = l.col[2] * (1 - e) + 1 * e; lanI[o + 7] = 1;
    }
    gl.useProgram(pL.p);
    gl.uniformMatrix4fv(pL.u.uVP, false, cam.VP); gl.uniform3fv(pL.u.uCam, cam.e); gl.uniform1f(pL.u.uWarm, warm); gl.uniform1f(pL.u.uAmb, amb);
    gl.bindBuffer(gl.ARRAY_BUFFER, lanIB); gl.bufferSubData(gl.ARRAY_BUFFER, 0, lanI.subarray(0, nl * 8));
    gl.bindVertexArray(vaoL);
    gl.drawArraysInstanced(gl.TRIANGLES, 0, nLan, nl);

    // 空（いちばん奥）
    gl.disable(gl.CULL_FACE);
    gl.depthFunc(gl.LEQUAL);
    gl.useProgram(pS.p);
    gl.uniform3fv(pS.u.uR, cam.s); gl.uniform3fv(pS.u.uU, cam.u); gl.uniform3fv(pS.u.uF, cam.f);
    gl.uniform2f(pS.u.uTan, cam.tanX, cam.tanY); gl.uniform1f(pS.u.uShift, cam.shift);
    gl.uniform1f(pS.u.uTime, t); gl.uniform1f(pS.u.uWarm, warm); gl.uniform1f(pS.u.uAmb, amb); gl.uniform3fv(pS.u.uMd, cam.md);
    gl.bindVertexArray(vaoS);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    gl.depthFunc(gl.LESS);

    // 光の粒
    nb = 0;
    for (var k = 0; k < LAN.length; k++) {
      var l = LAN[k], I = ign(l, t);
      if (I <= 0) continue;
      var e = l.eat, c0 = l.col[0] * (1 - e) + 0.35 * e, c1 = l.col[1] * (1 - e) + 0.62 * e, c2 = l.col[2] * (1 - e) + e;
      var fI = I * flick(k, t) * (1 - 0.5 * e);
      B(l.cx, l.y + 1.42, l.cz, 3.4, c0, c1 * 0.9, c2 * 0.75, 0.5 * fI);
      B(l.cx, l.y + 1.42, l.cz, 1.0, c0, c1, c2, 1.1 * fI);
      if (t - l.on < 0.6) B(l.cx, l.y + 1.42, l.cz, 6 * (t - l.on + 0.2), 1, 0.85, 0.55, 0.9 * (1 - (t - l.on) / 0.6));
    }
    if (flashG > 0) { var s0 = LAN[startI]; B(s0.cx, s0.y + 1.4, s0.cz, 14, 1, 0.8, 0.45, flashG * 0.9); }
    flash.forEach(function (f) { var a = t - f.t; if (a < 0.9) B(f.x, ground(f.x, f.z) + 1.4, f.z, 2 + a * 9, f.c[0], f.c[1], f.c[2], (1 - a / 0.9) * 0.9); });
    var nr = road(t);
    embers.forEach(function (m) { var k = m.a / m.life, a = Math.sin(Math.PI * Math.min(1, k)) * 1.6; B(m.x, m.y, m.z, 0.045, m.c[0], m.c[1] * 0.95, m.c[2] * 0.8, a, true); });
    // 目
    EYES.forEach(function (y) {
      var dark = Math.max(0, 1 - lightAt(y.x, y.z) * 3);
      var bl = Math.sin(t * y.sp + y.ph) > 0.96 ? 0 : 1, a = dark * bl * Math.min(1, Math.max(0, (t - 1.2) / 1.5)) * (0.5 + 0.5 * Math.sin(t * 0.3 + y.ph));
      if (a > 0.02) { B(y.x - 0.16, y.y, y.z, 0.06, 1, 0.23, 0.19, a * 1.6, true); B(y.x + 0.16, y.y, y.z, 0.06, 1, 0.23, 0.19, a * 1.6, true); }
    });
    if (ev.ph === 1 || ev.ph === 2) {
      var a = t - ev.t, l = LAN[ev.j], k = ev.ph === 1 ? Math.min(1, a / 2.4) : 1, ke = 1 - Math.pow(1 - k, 2);
      var ex = ev.ex + (l.cx - ev.ex) * ke * 0.82, ez = ev.ez + (l.cz - ev.ez) * ke * 0.82, ey = Math.max(0.8, ground(ex, ez)) + 1.5;
      var al = ev.ph === 1 ? Math.min(1, a / 0.6) : Math.max(0, 1 - a / 1.2);
      B(ex - 0.15, ey, ez, 0.06, 0.71, 0.42, 1, al * 2.2, true); B(ex + 0.15, ey, ez, 0.06, 0.71, 0.42, 1, al * 2.2, true);
      B(ex, ey, ez, 1.1, 0.5, 0.25, 0.9, al * 0.25);
    }
    if (ptr.cell && !coarse) { var g = ground(ptr.cell[0] + 0.5, ptr.cell[1] + 0.5); B(ptr.cell[0] + 0.5, g + 0.9, ptr.cell[1] + 0.5, 1.2, 1, 0.86, 0.62, 0.22); }

    gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE); gl.depthMask(false);
    gl.useProgram(pB.p);
    gl.uniformMatrix4fv(pB.u.uV, false, cam.V); gl.uniformMatrix4fv(pB.u.uP, false, cam.P);
    gl.bindBuffer(gl.ARRAY_BUFFER, bbB); gl.bufferSubData(gl.ARRAY_BUFFER, 0, bb.subarray(0, nb * 8));
    gl.bindVertexArray(vaoB);
    gl.drawArraysInstanced(gl.TRIANGLES, 0, 6, nb);
    gl.depthMask(true); gl.disable(gl.BLEND);
    post(t);
    gl.bindVertexArray(null);

    // 数
    if (litN !== lastL) { hl.textContent = litN; lastL = litN; }
    if (nr !== lastR) { hr.textContent = nr; lastR = nr; }
    if (evT && t - evT > 3.2) { he.classList.remove('on'); evT = 0; }
    if (!lit1 && t >= T0) { lit1 = true; hero.classList.add('lit'); }
    if (!lit2 && t >= T0 + SPREAD + 0.6) { lit2 = true; hero.classList.add('lit-all'); }
  }
  var lit1 = false, lit2 = false;

  var lastF = 0;
  function loop(ts) {
    if (!running) return;
    if (lastF && ts) {
      var ft = ts - lastF;
      if (ft < 200) { frames++; if (ft > 26) slow++; }
      if (frames >= 90) { if (slow > 45 && quality > 0.5) { quality *= 0.75; size(); } frames = 0; slow = 0; }
    }
    lastF = ts || 0;
    draw(now());
    requestAnimationFrame(loop);
  }
  function setRun() {
    var want = !RM && FIX === null && visible && !document.hidden;
    if (want && !running) { running = true; last = now(); requestAnimationFrame(loop); }
    else if (!want) running = false;
  }

  // ───────── 仕上げ ─────────
  try {
    hero.insertBefore(cv, hero.firstChild);
    hero.appendChild(hud);
    if (dive) { depthEl = document.createElement('div'); depthEl.className = 'dive-y dot'; depthEl.setAttribute('aria-hidden', 'true'); depthEl.innerHTML = '<b>Y=64</b>'; dive.appendChild(depthEl); }
    hero.classList.add('webgl');
    // 題字を一文字ずつにする（灯りと同時にともる）
    var h1 = hero.querySelector('.h1');
    if (h1 && !RM) {
      var n = 0;
      (function walk(node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (c) {
          if (c.nodeType === 3) {
            var fr = document.createDocumentFragment();
            Array.from(c.textContent).forEach(function (chx) {
              if (/\s/.test(chx)) { fr.appendChild(document.createTextNode(chx)); return; }
              var s = document.createElement('span'); s.className = 'hc'; s.style.setProperty('--i', n++); s.textContent = chx; fr.appendChild(s);
            });
            c.parentNode.replaceChild(fr, c);
          } else if (c.nodeType === 1 && c.tagName !== 'BR') walk(c);
        });
      })(h1);
      h1.setAttribute('aria-label', h1.textContent);
    }
    size();
    if (RM) { hero.classList.add('lit', 'lit-all'); draw(60); }
    if (FIX !== null) { draw(FIX); window.__heroPNG = cv.toDataURL('image/png'); }
  } catch (err) {
    if (cv.parentNode) cv.parentNode.removeChild(cv);
    if (hud.parentNode) hud.parentNode.removeChild(hud);
    hero.classList.remove('webgl');
    if (window.console) console.warn('hero gl', err);
    return;
  }
  var hint = hero.querySelector('.sky-hint');
  if (hint) hint.textContent = (coarse ? '地面をタップ' : '地面をクリック') + 'すると、灯籠を置けます';

  window.addEventListener('resize', function () { size(); }, { passive: true });
  function onScroll() {
    var vh = window.innerHeight || 800, y = window.scrollY;
    var span = hero.offsetHeight + (dive ? dive.offsetHeight : 0);
    // 1 = 土の章の上端が画面の下に届くとき
    scrollP = Math.min(1, Math.max(0, y / Math.max(1, span - vh)));
    // 土の章の上端（画面上の位置）。掘った土の目地を、章の目地とそろえる
    var top = soil ? soil.getBoundingClientRect().top : span - y;
    gridY = top * dpr0;
    dig = RM || !dive ? 0 : Math.min(1, Math.max(0, (scrollP - 0.38) / 0.16));
    // 掘り抜けたあと：土と石の層を落ちていく。最後はゆっくり止まり、章の目地にぴたりと合う
    var tr = RM || !dive ? 0 : Math.min(1, Math.max(0, (scrollP - 0.52) / 0.48));
    tun = 1 - (1 - tr) * (1 - tr);
    tunOff = (1 - tun) * vh * dpr0 * 3;
    rowsR0 = Math.ceil(vh / 52) + 2;
    if (depthEl) {
      var show = dig > 0.7 && top > vh * 0.55;
      depthEl.style.opacity = show ? Math.min(1, (dig - 0.7) / 0.3) * Math.min(1, (top - vh * 0.55) / (vh * 0.3)) : 0;
      var yv = Math.round(64 - 16 * tun);
      if (depthEl._v !== yv) { depthEl._v = yv; depthEl.firstChild.textContent = 'Y=' + yv; }
    }
    var fade = Math.max(0, 1 - scrollP * 2.2);
    hud.style.opacity = fade < 1 ? fade : '';
    if (hint) hint.style.opacity = fade < 1 ? fade * 0.9 : '';
    var v = y < span + 4;
    if (v !== visible) { visible = v; setRun(); }
    if (RM || !running) draw(now());
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  document.addEventListener('visibilitychange', setRun);
  onScroll();
  hero.addEventListener('pointermove', function (e) {
    var r = cv.getBoundingClientRect();
    var nx = (e.clientX - r.left) / r.width * 2 - 1, ny = 1 - (e.clientY - r.top) / r.height * 2;
    ptr.x = nx; ptr.y = ny;
    if (e.pointerType === 'mouse' && cam.V) ptr.cell = ray(nx, ny);
  }, { passive: true });
  hero.addEventListener('pointerleave', function () { ptr.cell = null; ptr.x = 0; ptr.y = 0; });
  hero.addEventListener('click', function (e) {
    if (e.target.closest('a,button,input,label,.addr,.chip,h1,p,.btns,.online')) return;
    if (scrollP > 0.3) return;
    var r = cv.getBoundingClientRect();
    var c = ray((e.clientX - r.left) / r.width * 2 - 1, 1 - (e.clientY - r.top) / r.height * 2);
    if (!c) return;
    var i = c[1] * W + c[0];
    if (WATER[i] || nearLan(c[0] + 0.5, c[1] + 0.5, 1.6)) return;
    var t = now(), l = mkLan(c[0], c[1], [1, 0.8, 0.45]);
    l.user = true; l.on = t + 0.05;
    if (LAN.filter(function (q) { return q.user; }).length >= 30) {
      var old = LAN.findIndex(function (q) { return q.user; });
      EDGE = EDGE.filter(function (e2) { return e2.a !== old && e2.b !== old; }).map(function (e2) { return { a: e2.a > old ? e2.a - 1 : e2.a, b: e2.b > old ? e2.b - 1 : e2.b, tree: e2.tree, t0: e2.t0, t1: e2.t1, len: e2.len }; });
      LAN.splice(old, 1);
      if (startI > old) startI--;
      if (ev.j > old) ev.j--; else if (ev.j === old) ev.ph = 0;
    }
    LAN.push(l);
    var me = LAN.length - 1, near = [];
    LAN.forEach(function (q, k) { if (k !== me && t >= q.on) { var d = Math.hypot(q.cx - l.cx, q.cz - l.cz); if (d < 9.5) near.push([d, k]); } });
    near.sort(function (a, b) { return a[0] - b[0]; });
    near.slice(0, 3).forEach(function (p) { EDGE.push({ a: me, b: p[1], tree: false, len: p[0], t0: t + 0.1, t1: t + 0.1 + p[0] / 11 }); });
    flash.push({ x: l.cx, z: l.cz, t: t, I: 1.2, c: l.col });
    user++;
    if (hint) { hint.classList.remove('on'); hint.classList.add('gone'); }
    say(near.length ? 'あなたの灯籠が、灯路でつながった' : 'あなたの灯籠が、ともった');
    if (RM) draw(60);
  });
  setRun();
})();
