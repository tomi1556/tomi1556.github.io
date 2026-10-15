/* 灯技の組み立て：道の Lv と技を選ぶと、技点と条件を計算する。組み立ては URL の # に入る。 */
(function () {
  'use strict';
  var root = document.querySelector('[data-builder]');
  var src = document.getElementById('bd-data');
  if (!root || !src) return;
  var D = JSON.parse(src.textContent);
  var $ = function (s, r) { return (r || root).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || root).querySelectorAll(s)); };
  var TIER = ['', '一の段', '二の段', '三の段', '奥義'];
  var ROMAN = ['', 'Ⅰ', 'Ⅱ', 'Ⅲ'];
  var KIND = D.kind;
  var KC = ['k0', 'k1', 'k2'];
  var N = D.paths.length;

  // 状態：道ごとの Lv と、技ごとの段
  var st = { cur: 0, sel: null, trial: true, lv: [], rk: [] };
  function reset(i) { st.lv[i] = 25; st.rk[i] = D.paths[i].nodes.map(function () { return 0; }); }
  for (var i = 0; i < N; i++) reset(i);

  // ── URL：#b=道:Lv:段…,…  ──
  function encode() {
    var parts = [];
    for (var i = 0; i < N; i++) {
      var r = st.rk[i].join('');
      if (/^0+$/.test(r) && st.lv[i] === 25) continue;
      parts.push(D.paths[i].id + ':' + st.lv[i] + ':' + r);
    }
    return '#b=' + parts.join(',') + '&p=' + D.paths[st.cur].id + (st.trial ? '' : '&t=0');
  }
  function decode() {
    var h = location.hash.slice(1);
    if (h.indexOf('b=') < 0) return;
    h.split('&').forEach(function (kv) {
      var k = kv.split('=')[0], v = decodeURIComponent(kv.slice(k.length + 1));
      if (k === 'b' && v) v.split(',').forEach(function (e) {
        var a = e.split(':'), pi = D.paths.findIndex(function (p) { return p.id === a[0]; });
        if (pi < 0) return;
        var lv = Math.max(1, Math.min(50, parseInt(a[1], 10) || 25));
        st.lv[pi] = lv;
        var s = a[2] || '';
        st.rk[pi] = D.paths[pi].nodes.map(function (n, j) { return Math.max(0, Math.min(n.req.length, parseInt(s.charAt(j), 10) || 0)); });
      });
      if (k === 'p') { var pi = D.paths.findIndex(function (p) { return p.id === v; }); if (pi >= 0) st.cur = pi; }
      if (k === 't') st.trial = v !== '0';
    });
    for (var i = 0; i < N; i++) fix(i);
  }

  // ── 計算 ──
  function P() { return D.paths[st.cur]; }
  function idx(p, id) { return p.nodes.findIndex(function (n) { return n.id === id; }); }
  function used(i) {
    var p = D.paths[i], s = 0;
    p.nodes.forEach(function (n, j) { for (var r = 0; r < st.rk[i][j]; r++) s += n.cost[r]; });
    return s;
  }
  function top3(i) { var p = D.paths[i], c = 0; p.nodes.forEach(function (n, j) { if (n.t === 3 && st.rk[i][j] > 0) c++; }); return c; }
  /** 次の段を覚えられない理由（覚えられるなら null）。 */
  function why(i, j) {
    var p = D.paths[i], n = p.nodes[j], r = st.rk[i][j];
    if (r >= n.req.length) return '極めました';
    if (n.parent && st.rk[i][idx(p, n.parent)] === 0) return '先に「' + p.nodes[idx(p, n.parent)].name + '」を覚える';
    if (n.t === 4 && top3(i) < D.capNeeds) return '三の段の技を ' + D.capNeeds + ' つ覚える（いま ' + top3(i) + '）';
    if (n.t === 4 && r === 0 && !st.trial) return '奥義の試練「' + p.trial + '」を果たす';
    if (st.lv[i] < n.req[r]) return 'Lv' + n.req[r] + ' で覚えられる';
    if (st.lv[i] - used(i) < n.cost[r]) return '技点が ' + n.cost[r] + ' 要る（残り ' + (st.lv[i] - used(i)) + '）';
    return null;
  }
  /** 外したときに、つながっている技も外す。 */
  function cascade(i) {
    var p = D.paths[i], changed = true;
    while (changed) {
      changed = false;
      p.nodes.forEach(function (n, j) {
        if (st.rk[i][j] === 0) return;
        var bad = (n.parent && st.rk[i][idx(p, n.parent)] === 0) || (n.t === 4 && (top3(i) < D.capNeeds || !st.trial));
        if (bad) { st.rk[i][j] = 0; changed = true; }
      });
    }
  }
  /** Lv を下げたとき：その Lv では届かない段を外し、技点が足りなければ上の段から外す。 */
  function fix(i) {
    var p = D.paths[i];
    p.nodes.forEach(function (n, j) { while (st.rk[i][j] > 0 && n.req[st.rk[i][j] - 1] > st.lv[i]) st.rk[i][j]--; });
    cascade(i);
    var order = p.nodes.map(function (n, j) { return j; }).sort(function (a, b) { return p.nodes[b].t - p.nodes[a].t; });
    while (used(i) > st.lv[i]) {
      var k = order.find(function (j) { return st.rk[i][j] > 0; });
      if (k === undefined) break;
      st.rk[i][k]--;
      cascade(i);
    }
  }

  // ── 描く ──
  var tree = $('[data-tree]'), info = $('[data-info]'), msg = $('[data-msg]');
  function tile(p, n, j) {
    var i = st.cur, r = st.rk[i][j], w = why(i, j), max = n.req.length;
    var state = r >= max ? 'max' : r > 0 ? 'has' : !w ? 'can' : 'no';
    var pips = '';
    for (var k = 0; k < max; k++) pips += '<i class="' + (k < r ? 'on' : '') + '"></i>';
    var next = r < max ? '<small class="dot">次 Lv' + n.req[r] + '・' + n.cost[r] + '点</small>' : '<small class="dot">極み</small>';
    return '<button type="button" class="tn bdn ' + state + (st.sel === j ? ' sel' : '') + ' ' + KC[n.kind] + '" data-j="' + j + '" style="--c:' + p.c + '" aria-pressed="' + (r > 0) + '">' +
      '<span class="tn-k">〔' + KIND[n.kind] + '〕</span><b>' + n.name + '</b>' + next + '<span class="tn-r">' + pips + '</span></button>';
  }
  function draw() {
    var p = P(), i = st.cur;
    root.style.setProperty('--c', p.c);
    $$('.bd-tab').forEach(function (b, k) {
      b.setAttribute('aria-selected', k === i ? 'true' : 'false');
      var u = used(k);
      $('[data-sum="' + k + '"]', b).textContent = 'Lv' + st.lv[k] + (u ? '・' + u + '点' : '');
      b.classList.toggle('used', u > 0);
    });
    $('[data-lv]').value = st.lv[i];
    $('[data-lvn]').textContent = st.lv[i];
    var u = used(i), left = st.lv[i] - u;
    $('[data-used]').textContent = u;
    $('[data-have]').textContent = st.lv[i];
    $('[data-left]').textContent = '残り ' + left;
    $('[data-barfill]').style.width = Math.min(100, u / Math.max(1, st.lv[i]) * 100) + '%';
    $('[data-trial]').checked = st.trial;
    var h = '<div class="tg-h"></div>';
    for (var b = 0; b < 4; b++) h += '<div class="tg-b"><span class="dot">枝' + '一二三四'.charAt(b) + '</span><b>' + p.branches[b] + '</b></div>';
    for (var t = 1; t <= 3; t++) {
      h += '<div class="tg-t dot">' + TIER[t] + '</div>';
      for (b = 0; b < 4; b++) {
        var j = p.nodes.findIndex(function (n) { return n.b === b && n.t === t; });
        h += '<div class="tg-c">' + (j >= 0 ? tile(p, p.nodes[j], j) : '') + '</div>';
      }
    }
    var cj = p.nodes.findIndex(function (n) { return n.t === 4; });
    h += '<div class="tg-t dot cap">奥義</div><div class="tg-cap">' + tile(p, p.nodes[cj], cj) + '<p class="mu">三の段を ' + D.capNeeds + ' つ ＋ 試練「' + p.trial + '」</p></div>';
    tree.innerHTML = h;
    drawInfo();
    drawSummary();
    history.replaceState(null, '', encode());
  }
  function drawInfo() {
    var p = P(), i = st.cur, j = st.sel;
    if (j === null || j < 0) { info.innerHTML = '<p class="mu">技を押すと、ここに説明と「覚える／外す」が出ます。</p>'; return; }
    var n = p.nodes[j], r = st.rk[i][j], w = why(i, j);
    var rows = n.eff.map(function (e, k) {
      return '<li class="' + (k < r ? 'on' : k === r ? 'next' : '') + '"><span class="dot">' + (n.eff.length > 1 ? ROMAN[k + 1] : '—') + '</span><b>' + e + '</b><small class="dot">Lv' + n.req[k] + '・' + n.cost[k] + '点</small></li>';
    }).join('');
    var parent = n.parent ? p.nodes[idx(p, n.parent)].name : null;
    info.innerHTML = '<p class="bd-ik ' + KC[n.kind] + '">〔' + KIND[n.kind] + '〕 ' + TIER[n.t] + (parent ? ' ・ 前の技「' + parent + '」' : '') + '</p>' +
      '<h3 class="disp">' + n.name + '</h3><ul class="bd-ranks">' + rows + '</ul>' +
      '<div class="btns"><button type="button" class="pbtn sm" data-add' + (w ? ' disabled' : '') + '>＋ 覚える</button><button type="button" class="gbtn sm" data-sub' + (r ? '' : ' disabled') + '>－ 外す</button></div>' +
      '<p class="bd-why">' + (w ? (w === '極めました' ? '✔ すべての段を覚えました' : '× ' + w) : '▶ 次の段を覚えられます') + '</p>' +
      '<p class="mu bd-link"><a href="wiki-' + p.id + '.html#' + n.id + '">この技の説明（Wiki）</a></p>';
  }
  function drawSummary() {
    var h = '', any = false;
    D.paths.forEach(function (p, i) {
      var list = p.nodes.map(function (n, j) { return [n, st.rk[i][j]]; }).filter(function (x) { return x[1] > 0; });
      if (!list.length) return;
      any = true;
      h += '<div class="bd-sp" style="--c:' + p.c + '"><p class="bd-sh"><span class="ws-k">' + p.k + '</span><b>' + p.name + '</b><small class="dot">Lv' + st.lv[i] + '・技点 ' + used(i) + '/' + st.lv[i] + '</small></p><ul>' +
        list.map(function (x) { return '<li><b>' + x[0].name + (x[0].eff.length > 1 ? ' ' + ROMAN[x[1]] : '') + '</b><span>' + x[0].eff[x[1] - 1] + '</span></li>'; }).join('') + '</ul></div>';
    });
    $('[data-summary]').innerHTML = any ? h : '<p class="mu">まだ何も選んでいません。上の技の木から選んでください。</p>';
  }
  function say(t) { msg.textContent = t; clearTimeout(say.t); say.t = setTimeout(function () { msg.textContent = ''; }, 2600); }

  // ── 操作 ──
  root.addEventListener('click', function (e) {
    var tab = e.target.closest('.bd-tab');
    if (tab) { st.cur = +tab.getAttribute('data-p'); st.sel = null; draw(); return; }
    var t = e.target.closest('.bdn');
    if (t) { st.sel = +t.getAttribute('data-j'); draw(); return; }
    var i = st.cur, j = st.sel;
    if (e.target.closest('[data-add]') && j !== null && !why(i, j)) { st.rk[i][j]++; draw(); return; }
    if (e.target.closest('[data-sub]') && j !== null && st.rk[i][j] > 0) { st.rk[i][j]--; cascade(i); draw(); return; }
    if (e.target.closest('[data-resetp]')) { reset(i); st.sel = null; draw(); say('この道をはじめからにしました。'); return; }
    if (e.target.closest('[data-resetall]')) { for (var k = 0; k < N; k++) reset(k); st.sel = null; draw(); say('すべての道をはじめからにしました。'); return; }
    if (e.target.closest('[data-share]')) {
      var url = location.href.split('#')[0] + encode();
      var ok = function () { say('リンクをコピーしました。Discord に貼ると、同じ組み立てが開きます。'); };
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(ok, function () { say(url); }); else say(url);
    }
  });
  // 技を右クリックで外す（PC）
  root.addEventListener('contextmenu', function (e) {
    var t = e.target.closest('.bdn'); if (!t) return;
    e.preventDefault();
    var i = st.cur, j = +t.getAttribute('data-j');
    st.sel = j;
    if (st.rk[i][j] > 0) { st.rk[i][j]--; cascade(i); }
    draw();
  });
  // 技をダブルクリックで覚える（PC）
  root.addEventListener('dblclick', function (e) {
    var t = e.target.closest('.bdn'); if (!t) return;
    var i = st.cur, j = +t.getAttribute('data-j');
    if (!why(i, j)) { st.rk[i][j]++; draw(); }
  });
  $('[data-lv]').addEventListener('input', function (e) { st.lv[st.cur] = +e.target.value; fix(st.cur); draw(); });
  $('[data-trial]').addEventListener('change', function (e) { st.trial = e.target.checked; for (var k = 0; k < N; k++) cascade(k); draw(); });

  decode();
  draw();
})();
