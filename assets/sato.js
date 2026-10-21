/* 灯里：里の土地の体験。里灯から灯路でつながった灯籠の守りだけが、里の土地になる。 */
(function () {
  'use strict';
  var root = document.querySelector('[data-sato]');
  if (!root) return;
  var $ = function (s, el) { return (el || root).querySelector(s); };
  var narrow = window.matchMedia('(max-width: 640px)').matches;
  var W = narrow ? 10 : 16, H = narrow ? 10 : 8, LINK = 3.2, MAX = 40;
  var CORE = narrow ? [5, 5] : [7, 4];
  var START = narrow
    ? [[2, 5], [1, 3], [8, 5], [8, 8], [5, 2], [3, 7], [9, 1]]
    : [[4, 4], [2, 3], [10, 4], [12, 5], [13, 2], [7, 1], [5, 6], [15, 7]];
  var PLOT = narrow ? { x: 7, y: 7, w: 3, h: 3 } : { x: 11, y: 4, w: 3, h: 3 };
  var grid = $('.hs-grid'), msg = $('[data-msg]');
  var st = { lan: [] };
  grid.style.gridTemplateColumns = 'repeat(' + W + ', minmax(0, 1fr))';
  var html = '';
  for (var i = 0; i < W * H; i++) html += '<button type="button" class="tile" data-i="' + i + '"></button>';
  html += '<svg class="links" viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none" aria-hidden="true"><path class="on" d="M0 0"/><path class="cut" d="M0 0"/></svg>';
  html += '<div class="hs-plot" style="left:' + (PLOT.x / W * 100) + '%;top:' + (PLOT.y / H * 100) + '%;width:' + (PLOT.w / W * 100) + '%;height:' + (PLOT.h / H * 100) + '%"><span>屋敷</span></div>';
  grid.innerHTML = html;
  var tiles = Array.prototype.slice.call(grid.querySelectorAll('.tile'));
  var pOn = grid.querySelector('path.on'), pCut = grid.querySelector('path.cut'), plot = grid.querySelector('.hs-plot');
  var say = function (t) { msg.textContent = t; };
  var X = function (i) { return i % W; }, Y = function (i) { return Math.floor(i / W); };
  var idx = function (x, y) { return y * W + x; };
  var coreI = idx(CORE[0], CORE[1]);
  var find = function (i) { for (var k = 0; k < st.lan.length; k++) if (st.lan[k].i === i) return st.lan[k]; return null; };
  var near = function (a, b) { var dx = X(a) - X(b), dy = Y(a) - Y(b); return dx * dx + dy * dy <= LINK * LINK; };

  // 里灯から、喰われていない灯籠を灯路でたどる
  var reach = function (all) {
    var lit = st.lan.filter(function (l) { return all || !l.out; });
    var seen = {}, q = [coreI], land = [];
    seen[coreI] = true;
    while (q.length) {
      var c = q.shift();
      lit.forEach(function (l) { if (!seen[l.i] && near(c, l.i)) { seen[l.i] = true; land.push(l); q.push(l.i); } });
    }
    return land;
  };
  var cover = function (land) {
    var m = {};
    var put = function (c, r) {
      for (var dy = -r; dy <= r; dy++) for (var dx = -r; dx <= r; dx++) {
        var x = X(c) + dx, y = Y(c) + dy;
        if (x >= 0 && y >= 0 && x < W && y < H) m[idx(x, y)] = true;
      }
    };
    put(coreI, 2);
    land.forEach(function (l) { put(l.i, 1); });
    return m;
  };
  var count = function (m) { return Object.keys(m).length; };

  var draw = function () {
    var land = reach(false), inLand = {}, lit = st.lan.filter(function (l) { return !l.out; });
    land.forEach(function (l) { inLand[l.i] = true; });
    var L = cover(land), ideal = cover(reach(true));
    var light = {};
    lit.forEach(function (l) {
      if (inLand[l.i]) return;
      for (var dy = -1; dy <= 1; dy++) for (var dx = -1; dx <= 1; dx++) {
        var x = X(l.i) + dx, y = Y(l.i) + dy;
        if (x >= 0 && y >= 0 && x < W && y < H) light[idx(x, y)] = true;
      }
    });
    tiles.forEach(function (t, i) {
      var l = find(i), isLand = !!L[i], near1 = isLand && (i === coreI || land.some(function (x) { return Math.max(Math.abs(X(x.i) - X(i)), Math.abs(Y(x.i) - Y(i))) === 0; }));
      t.style.backgroundColor = isLand ? (near1 ? '#9A7642' : '#7A5C30') : light[i] ? '#3D5E2C' : '#16241A';
      t.classList.toggle('land', isLand);
      if (i === coreI) t.innerHTML = '<span class="hs-core"></span>';
      else t.innerHTML = l ? '<span class="mini' + (l.out ? ' out' : '') + '"></span>' : '';
      t.setAttribute('aria-label', (Y(i) + 1) + '行' + (X(i) + 1) + '列、' + (i === coreI ? '里灯' : l ? (l.out ? '喰われた灯籠。押すと灯し直す' : (inLand[i] ? '里の土地の灯籠。押すと喰わせる' : '里につながっていない灯籠')) : (isLand ? '里の土地' : light[i] ? '灯りの中' : '灯りの外')));
    });
    // 灯路：里の網はながれる線、つながっていない灯籠どうしは点線
    var nodes = [coreI].concat(lit.map(function (l) { return l.i; })), on = [], cut = [];
    for (var a = 0; a < nodes.length; a++) for (var b = a + 1; b < nodes.length; b++) {
      if (!near(nodes[a], nodes[b])) continue;
      var seg = 'M' + (X(nodes[a]) + 0.5) + ' ' + (Y(nodes[a]) + 0.5) + 'L' + (X(nodes[b]) + 0.5) + ' ' + (Y(nodes[b]) + 0.5);
      var ia = nodes[a] === coreI || inLand[nodes[a]], ib = nodes[b] === coreI || inLand[nodes[b]];
      (ia && ib ? on : cut).push(seg);
    }
    pOn.setAttribute('d', on.join(' ') || 'M0 0');
    pCut.setAttribute('d', cut.join(' ') || 'M0 0');
    var whole = true;
    for (var py = PLOT.y; py < PLOT.y + PLOT.h; py++) for (var px = PLOT.x; px < PLOT.x + PLOT.w; px++) if (!L[idx(px, py)]) whole = false;
    plot.classList.toggle('keep', !whole);
    root.querySelector('[data-s="lan"]').textContent = land.length;
    root.querySelector('[data-s="land"]').textContent = count(L);
    root.querySelector('[data-s="lost"]').textContent = Math.max(0, count(ideal) - count(L));
    return { land: land, whole: whole };
  };

  grid.addEventListener('click', function (ev) {
    var t = ev.target.closest('.tile'); if (!t) return;
    var i = Number(t.getAttribute('data-i')), l = find(i);
    if (i === coreI) { say('里灯です。灯喰いには喰われず、壊せるのは里長だけ。里の土地は、ここから始まります。'); return; }
    if (l && l.out) { l.out = false; draw(); say('灯し直しました。そこから先の土地が戻ります。本番では、灯守がこの仕事で育ちます。'); return; }
    if (l) {
      var before = reach(false).length;
      l.out = true; var r = draw();
      var lostN = before - r.land.length;
      say(lostN > 1 ? '灯籠が喰われて、灯路が切れました。その先の ' + (lostN - 1) + ' 基は里の土地から外れます。' + (!r.whole ? '屋敷の守りは、欠けているあいだも持ち主に残ります。' : '') : '灯籠が喰われました。押すと灯し直せます。');
      return;
    }
    if (st.lan.length >= MAX) { say('集落の土地に数える灯籠は ' + MAX + ' 基までです。格が上がると増えます。'); return; }
    st.lan.push({ i: i, out: false });
    var joined = reach(false).some(function (x) { return x.i === i; });
    draw();
    say(joined ? '灯籠をつなぎました。里の土地が広がります。' : '灯路がつながっていないので、この灯籠の守りは里の土地には入りません（個人の灯りのまま）。');
  });
  $('[data-eat]').addEventListener('click', function () {
    // いちばん多くの土地を欠けさせる灯籠を、灯喰いが狙う
    var base = reach(false), best = null, bestLoss = -1;
    base.forEach(function (l) {
      l.out = true; var n = reach(false).length; l.out = false;
      var loss = base.length - n;
      if (loss > bestLoss) { bestLoss = loss; best = l; }
    });
    if (!best) { say('喰われる灯籠がありません。'); return; }
    best.out = true; var r = draw();
    say('灯喰いの夜。灯路の要の灯籠が喰われ、土地が ' + bestLoss + ' 基ぶん欠けました。' + (!r.whole ? '屋敷の守りは持ち主に残っています。' : '') + '「遠灯し」か、青い灯籠を押して灯し直してください。');
  });
  $('[data-far]').addEventListener('click', function () {
    var n = 0; st.lan.forEach(function (l) { if (l.out) { l.out = false; n++; } });
    draw();
    say(n ? '灯守の匠の奉仕「遠灯し」。里灯に触れて、喰われた里の灯籠 ' + n + ' 基をまとめて灯し直しました（夜に1回）。' : '喰われた灯籠はありません。');
  });
  $('[data-reset]').addEventListener('click', function () {
    st.lan = START.map(function (p) { return { i: idx(p[0], p[1]), out: false }; });
    draw(); say('最初の形に戻しました。');
  });
  st.lan = START.map(function (p) { return { i: idx(p[0], p[1]), out: false }; });
  draw();
})();
