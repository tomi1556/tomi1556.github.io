/* 灯原：動きの仕組み（どのブラウザでも）。動きを減らす設定の人には何もしない。 */
(function () {
  'use strict';
  var root = document.documentElement;
  if (root.classList.contains('rm')) return;
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
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
  items.forEach(function (it) { it[0].classList.add('rv'); it[0].style.setProperty('--d', (it[1] * 70) + 'ms'); });
  // 見出しは一文字ずつ灯す
  $$('.stratum .h2, .phead .h1-sub, .foot-cta h2').forEach(function (h) {
    var n = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (c) {
        if (c.nodeType === 3) {
          var frag = document.createDocumentFragment();
          Array.from(c.textContent).forEach(function (ch) {
            if (/\s/.test(ch)) { frag.appendChild(document.createTextNode(ch)); return; }
            var s = document.createElement('span');
            s.className = 'ltr'; s.style.setProperty('--i', n++); s.textContent = ch;
            frag.appendChild(s);
          });
          c.parentNode.replaceChild(frag, c);
        } else if (c.nodeType === 1 && !/^(BR|WBR|SVG)$/i.test(c.tagName)) walk(c);
      });
    })(h);
    h.classList.add('lit-h');
    h.setAttribute('aria-label', h.textContent);
  });
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
    $$('.lit-h').forEach(function (h) { io.observe(h); });
  } else {
    items.forEach(function (it) { it[0].classList.add('in'); });
    $$('.lit-h').forEach(function (h) { h.classList.add('in'); });
  }

  // いちばん下まで来たら、残りを全部灯す（それ以上スクロールできないため）
  var endT = 0;
  window.addEventListener('scroll', function () {
    if (endT) return;
    endT = setTimeout(function () {
      endT = 0;
      if (window.innerHeight + window.scrollY < document.documentElement.scrollHeight - 8) return;
      $$('.rv:not(.in), .lit-h:not(.in)').forEach(function (el) {
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

  // ── 3. 札が手に吸いつく（PC）：傾きと、灯りの照り返し ──
  if (fine) {
    $$('.ch,.wpc,.akc,.cc,.pg,.perk,.wiki-band,.path,.tt').forEach(function (el) {
      el.classList.add('tilt');
      var g = document.createElement('i');
      g.className = 'glare'; g.setAttribute('aria-hidden', 'true');
      el.appendChild(g);
      var raf = 0, ev = null;
      el.addEventListener('pointermove', function (e) {
        ev = e;
        if (raf) return;
        raf = requestAnimationFrame(function () {
          raf = 0;
          var r = el.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width, y = (ev.clientY - r.top) / r.height;
          el.style.setProperty('--rx', ((0.5 - y) * 7).toFixed(2) + 'deg');
          el.style.setProperty('--ry', ((x - 0.5) * 9).toFixed(2) + 'deg');
          el.style.setProperty('--gx', (x * 100).toFixed(1) + '%');
          el.style.setProperty('--gy', (y * 100).toFixed(1) + '%');
        });
      });
      el.addEventListener('pointerleave', function () { el.style.removeProperty('--rx'); el.style.removeProperty('--ry'); });
    });
  }

  // ── 4. 押すと火の粉が散る ──
  document.addEventListener('pointerdown', function (e) {
    var b = e.target.closest('.pbtn,.gbtn,.chip-f,.tab,.bd-tab,.qs-k button,.live-c,.film-play');
    if (!b) return;
    var r = b.getBoundingClientRect();
    var x = e.clientX || r.left + r.width / 2, y = e.clientY || r.top + r.height / 2;
    for (var i = 0; i < 9; i++) {
      var s = document.createElement('i');
      s.className = 'spark';
      var a = Math.random() * Math.PI * 2, d = 26 + Math.random() * 34;
      s.style.left = x + 'px'; s.style.top = y + 'px';
      s.style.setProperty('--dx', (Math.cos(a) * d).toFixed(1) + 'px');
      s.style.setProperty('--dy', (Math.sin(a) * d - 14).toFixed(1) + 'px');
      if (i % 3 === 0) s.style.background = '#FFF1C4';
      document.body.appendChild(s);
      setTimeout(function (n) { n.remove(); }.bind(null, s), 700);
    }
  }, { passive: true });

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
})();
