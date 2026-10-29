/* 灯原：動きの仕組み（どのブラウザでも）。動きを減らす設定の人には何もしない。 */
(function () {
  'use strict';
  var root = document.documentElement;
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var RM = root.classList.contains('rm');
  // 動きを減らす設定でも、灯路の背骨は「ともった状態」で出す（動きはなし）
  if (RM) { if (document.body.classList.contains('spined') && 'IntersectionObserver' in window) spine(); return; }
  var fine = window.matchMedia('(pointer: fine)').matches;

  // ── 1. 現れる：画面に入ったものから、順に灯る ──
  var GROUPS = '.chs,.three,.two,.facts,.perks,.flow,.paths,.wpcs,.akcs,.acs,.ncs,.castrow,.tts,.rks,.pager,.fcs,.tks,.rars,.conds,.cmdg,.ladder,.rules,.night,.steps,.gtiles,.lvsteps,.bd-sum,.foot-map,.wall';
  var items = [];
  $$('.stratum > .wrap > *, .stratum .wk-main > *, .foot-cta > *').forEach(function (el) {
    if (el.matches(GROUPS)) return;
    if (el.matches('script,style,.edge,[hidden],[role=tabpanel],noscript')) return;
    items.push([el, 0]);
  });
  $$(GROUPS).forEach(function (g) {
    var kids = Array.prototype.slice.call(g.children);
    kids.forEach(function (k, i) { items.push([k, Math.min(i, 9)]); });
  });
  // 灯路の背骨があるページでは、ふわっと出す代わりに「灯りがともる」（下の 7）
  if (document.body.classList.contains('spined')) items = items.filter(function (it) { return it[0].closest('.foot-map'); });
  items.forEach(function (it) { it[0].classList.add('rv'); it[0].style.setProperty('--d', (it[1] * 70) + 'ms'); });
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target;
      el.classList.add('in');
      io.unobserve(el);
      $$('[data-count]', el).concat(el.hasAttribute('data-count') ? [el] : []).forEach(count);
    });
  }, { rootMargin: '0px 0px -3% 0px', threshold: 0.02 }) : null;
  if (io) {
    items.forEach(function (it) { io.observe(it[0]); });
  } else {
    items.forEach(function (it) { it[0].classList.add('in'); });
  }

  // いちばん下まで来たら、残りを全部灯す（それ以上スクロールできないため）
  var endT = 0;
  window.addEventListener('scroll', function () {
    if (endT) return;
    endT = setTimeout(function () {
      endT = 0;
      if (window.innerHeight + window.scrollY < document.documentElement.scrollHeight - 8) return;
      $$('.rv:not(.in)').forEach(function (el) {
        if (el.getBoundingClientRect().top < window.innerHeight) { el.classList.add('in'); $$('[data-count]', el).forEach(count); }
      });
    }, 200);
  }, { passive: true });

  // ── 2. 数が数え上がる ──
  $$('.wk-stats b, .fact-n, .akc-n, .tt-n, .lvsteps b, .gt b, .wall-n b').forEach(function (el) {
    var t = el.firstChild;
    if (!t || t.nodeType !== 3) return;
    var m = t.textContent.match(/^(\s*)([\d,]+)(.*)$/);
    if (!m) return;
    var v = parseInt(m[2].replace(/,/g, ''), 10);
    if (!(v > 1)) return;
    el.setAttribute('data-count', '');
    el._c = { node: t, pre: m[1], post: m[3], v: v, comma: m[2].indexOf(',') >= 0 || v >= 1000 };
    t.textContent = m[1] + (el._c.comma ? '0' : '0') + m[3];
    // まわりの札が見張られていなければ、自分で見張る
    if (io && !el.closest('.rv')) io.observe(el);
  });
  function count(el) {
    var c = el._c;
    if (!c || c.done) return;
    c.done = true;
    var t0 = performance.now(), dur = 900 + Math.min(700, c.v);
    (function step(now) {
      var k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      var n = Math.round(c.v * e);
      c.node.textContent = c.pre + (c.comma ? n.toLocaleString('en-US') : n) + c.post;
      if (k < 1) requestAnimationFrame(step);
    })(t0);
  }

  // ── 5. トップの夜空：押すと天灯（てんとう）が上っていく ──
  var hero = document.querySelector('.hero-top');
  if (hero) {
    var hint = document.createElement('p');
    hint.className = 'sky-hint dot';
    hint.textContent = (fine ? '夜空をクリック' : '夜空をタップ') + 'すると、灯りを放てます';
    hero.appendChild(hint);
    setTimeout(function () { hint.classList.add('on'); }, 4200);
    var n = 0;
    hero.addEventListener('click', function (e) {
      if (hero.classList.contains('webgl')) return;
      if (e.target.closest('a,button,input,label,.addr,.chip,.scene')) return;
      if (hero.querySelectorAll('.tento').length > 14) return;
      hint.classList.remove('on'); hint.classList.add('gone');
      var r = hero.getBoundingClientRect();
      var t = document.createElement('i');
      t.className = 'tento';
      t.style.left = (e.clientX - r.left) + 'px'; t.style.top = (e.clientY - r.top) + 'px';
      t.style.setProperty('--sw', (Math.random() * 2 - 1).toFixed(2));
      t.style.setProperty('--h', (n++ % 5 === 3 ? '#F29BB8' : '#F2B544'));
      hero.appendChild(t);
      setTimeout(function () { t.remove(); }, 9000);
    });
  }

  // ── 6. 体験のマス：灯籠を置くと、灯りの輪が広がる ──
  var grid = document.querySelector('[data-demo] .grid');
  if (grid) {
    grid.addEventListener('click', function (e) {
      var t = e.target.closest('.tile');
      if (!t) return;
      setTimeout(function () {
        if (!t.querySelector('.mini')) return;
        var w = document.createElement('i');
        w.className = 'ripple';
        var gr = grid.getBoundingClientRect(), tr = t.getBoundingClientRect();
        w.style.left = (tr.left - gr.left + tr.width / 2) + 'px'; w.style.top = (tr.top - gr.top + tr.height / 2) + 'px';
        grid.appendChild(w);
        setTimeout(function () { w.remove(); }, 900);
      }, 0);
    });
  }

  // ── 7. 灯路の背骨：読み進めるほど節がともり、次の節へ点線がのびる（spined のページ） ──
  if (document.body.classList.contains('spined') && 'IntersectionObserver' in window) spine();
  function spine() {
    var body = document.body;
    var LAN = '<svg viewBox="0 0 12 12" aria-hidden="true"><rect x="4" y="0" width="4" height="1"/><rect x="3" y="1" width="6" height="1"/><rect x="3" y="2" width="1" height="4"/><rect x="8" y="2" width="1" height="4"/><rect class="o" x="4" y="2" width="4" height="4"/><rect x="3" y="6" width="6" height="1"/><rect x="5" y="7" width="2" height="4"/><rect x="4" y="11" width="4" height="1"/></svg>';
    var heads = $$('main .stratum > .wrap > .h2, main .stratum > .wrap > h2.disp, main .stratum > .wrap > div > .h2, main .stratum .wall-h > .h2, main .ps-panel > .h2, main .s-stone > .wrap > .h2, .foot-cta h2');
    var nodes = heads.map(function (h, i) {
      var n = document.createElement('i');
      n.className = 'sp-n' + (h.closest('.foot-cta') ? ' end' : '');
      n.setAttribute('aria-hidden', 'true');
      n.innerHTML = LAN;
      h.classList.add('sp-h');
      h.insertBefore(n, h.firstChild);
      return n;
    });
    // 背骨の線（広い画面だけ）。節の位置から計算し、のびる線は transform だけで動かす
    var layer = document.createElement('div');
    layer.className = 'sp-layer';
    layer.setAttribute('aria-hidden', 'true');
    body.appendChild(layer);
    var segs = [];
    function layout() {
      layer.innerHTML = '';
      segs = [];
      var wide = window.matchMedia('(min-width: 1280px)').matches;
      layer.hidden = !wide;
      if (!wide) return;
      var sy = window.scrollY;
      var vis = nodes.filter(function (n) { return n.getBoundingClientRect().height > 0; });
      var pts = vis.map(function (n) { var r = n.getBoundingClientRect(); return [r.left + r.width / 2 + window.scrollX, r.top + sy + r.height / 2]; });
      for (var i = 0; i < pts.length - 1; i++) {
        var a = pts[i], b = pts[i + 1];
        var s = document.createElement('i');
        s.className = 'sp-s';
        s.style.left = (a[0] - 1.5) + 'px';
        s.style.top = (a[1] + 16) + 'px';
        s.style.height = Math.max(0, b[1] - a[1] - 32) + 'px';
        s.innerHTML = '<b></b>';
        s._from = vis[i];
        if (vis[i].classList.contains('on')) s.classList.add('on');
        layer.appendChild(s);
        segs.push(s);
      }
    }
    // 光るもの：アイコン・カード・手順・時系列・棒・数字
    var lights = $$('main .vi, main .vc, main .vsteps > li, main .vtl > li, main .vbars > li, main .vstats > li, main .vgames > li, main .vtiers > li, main .vfact, main .vscale > li');
    if (RM) {
      nodes.forEach(function (n, i) { n.classList.add('on'); if (i > 0) n.parentElement.classList.add('lit'); });
      layout();
      segs.forEach(function (sg) { sg.classList.add('on'); });
      var rt0 = 0;
      window.addEventListener('resize', function () { clearTimeout(rt0); rt0 = setTimeout(function () { layout(); segs.forEach(function (sg) { sg.classList.add('on'); }); }, 150); }, { passive: true });
      window.addEventListener('load', function () { layout(); segs.forEach(function (sg) { sg.classList.add('on'); }); });
      return;
    }
    body.classList.add('ldim');
    // はじめから画面にあるものは、すぐともす（待たせない）
    var vh = window.innerHeight;
    function delayOf(el) {
      var p = el.parentElement, k = p ? Array.prototype.indexOf.call(p.children, el) : 0;
      if (el.classList.contains('vi')) { var li = el.closest('li, .vfact'); if (li && li.parentElement) k = Array.prototype.indexOf.call(li.parentElement.children, li); }
      return Math.min(Math.max(k, 0), 8) * 60;
    }
    function on(el) {
      if (el._on) return;
      el._on = true;
      el.style.setProperty('--ld', delayOf(el) + 'ms');
      el.classList.add('on');
      if (el.matches('.vbars > li, .vstats > li')) $$('.vb-v, b', el).slice(0, 1).forEach(tick);
    }
    function tick(el) {
      var t = el.firstChild;
      if (!t || t.nodeType !== 3) return;
      var m = t.textContent.match(/^([^\d]*)([\d,]+(?:\.\d+)?)(.*)$/);
      if (!m) return;
      var raw = m[2], v = parseFloat(raw.replace(/,/g, '')), dec = (raw.split('.')[1] || '').length;
      if (!(v > 0)) return;
      var i = 0, N = 8;
      var id = setInterval(function () {
        i++;
        var x = v * i / N;
        var s = dec ? x.toFixed(dec) : Math.round(x).toString();
        if (raw.indexOf(',') >= 0) s = Number(s).toLocaleString('en-US');
        t.textContent = m[1] + (i >= N ? raw : s) + m[3];
        if (i >= N) clearInterval(id);
      }, 60);
    }
    lights.forEach(function (el) { var r = el.getBoundingClientRect(); if (r.top < vh && r.bottom > 0) on(el); });
    var lio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { on(e.target); lio.unobserve(e.target); } });
    }, { rootMargin: '100000px 0px -8% 0px', threshold: 0 });
    lights.forEach(function (el) { if (!el._on) lio.observe(el); });
    // 節：画面の6割の高さを越えたらともり、次への線がのびる
    function lightNode(i) {
      var n = nodes[i];
      if (n.classList.contains('on')) return;
      n.classList.add('on');
      if (n.parentElement && i > 0) n.parentElement.classList.add('lit');
      setTimeout(function () { segs.forEach(function (sg) { if (sg._from === n) sg.classList.add('on'); }); }, 240);
      if (n.classList.contains('end')) { var ft = n.closest('.foot-cta'); if (ft) ft.classList.add('arrived'); }
    }
    var nio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { lightNode(nodes.indexOf(e.target)); nio.unobserve(e.target); } });
    }, { rootMargin: '100000px 0px -40% 0px', threshold: 0 });
    nodes.forEach(function (n) { nio.observe(n); });
    layout();
    var rt = 0;
    window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(layout, 150); }, { passive: true });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(layout);
    window.addEventListener('load', layout);
    // タブの切りかえ・「くわしく」の開け閉めで高さが変わったら、線を引き直す
    document.addEventListener('toggle', function () { clearTimeout(rt); rt = setTimeout(layout, 60); }, true);
    document.addEventListener('click', function (e) { if (e.target.closest('[role=tab]')) { clearTimeout(rt); rt = setTimeout(layout, 60); } });
  }
})();
