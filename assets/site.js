/* 灯原 公式サイト：動きのある部分だけをここで足します。読めなくても本文は読めます。 */
(function () {
  'use strict';
  var ADDRESS = 'tomoshibara.life';
  var SEASON_START = Date.parse('2026-11-07T21:00:00+09:00');
  var GAMES = [
    { name: '灯籠リレー', desc: '2組に分かれ、出発点から終点まで、自分の組の灯籠だけで先に灯路を通した組の勝ち。' },
    { name: '闇かくれんぼ', desc: '鬼に触れられたら負け。朝まで隠れきれば勝ち。灯籠を置くと、10秒間 体が光ります。' },
    { name: '建築早押し', desc: 'お題の建物を15分で建て、最後に参加者全員の投票で決めます。' },
    { name: '夜明けまで', desc: '朱月の夜を呼び、倒れたら脱落。朝まで生き延びた人の勝ち。' }
  ];
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var pad = function (n) { return String(n).padStart(2, '0'); };
  var split = function (ms) {
    var t = Math.max(0, Math.floor(ms / 1000));
    return { d: String(Math.floor(t / 86400)), h: pad(Math.floor(t / 3600) % 24), m: pad(Math.floor(t / 60) % 60), s: pad(t % 60) };
  };
  var seed = 11;
  var rnd = function () { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; };

  // ── ヘッダー：スクロールしたら背景をつけ、スマホでは下へ進むと隠して、少し戻すと出す ──
  var hdr = $('.hdr');
  if (hdr) {
    var lastY = window.scrollY, up = 0, ticking = false;
    var mobile = window.matchMedia('(max-width: 760px)');
    var onScroll = function () {
      ticking = false;
      var y = Math.max(0, window.scrollY), dy = y - lastY;
      hdr.classList.toggle('solid', y > 8);
      if (!mobile.matches || y < 80) { hdr.classList.remove('hide'); up = 0; }
      else if (dy > 0) { up = 0; if (y > 120) hdr.classList.add('hide'); }
      else if (dy < 0) { up -= dy; if (up > 24) hdr.classList.remove('hide'); }
      lastY = y;
    };
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
    hdr.addEventListener('focusin', function () { hdr.classList.remove('hide'); });
    onScroll();
  }

  // ── 灯籠の知らせ（画面の下に、ぽっと灯る） ──
  var toastEl = null, toastT = 0;
  function toast(title, sub) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'toast'; toastEl.setAttribute('role', 'status');
      document.body.appendChild(toastEl);
    }
    toastEl.innerHTML = '<i class="toast-l" aria-hidden="true"></i><span><b>' + title + '</b>' + (sub ? '<small>' + sub + '</small>' : '') + '</span>';
    toastEl.classList.remove('on'); void toastEl.offsetWidth; toastEl.classList.add('on');
    clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove('on'); }, 2600);
  }
  window.tomoToast = toast;

  // ── アドレスのコピー ──
  $$('[data-copy]').forEach(function (btn) {
    var label = btn.textContent;
    var note = btn.closest('.addr') && btn.closest('.addr').nextElementSibling;
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy') || ADDRESS;
      var done = function (ok) {
        if (ok) toast('アドレスをコピーしました', 'マインクラフトの「サーバーを追加」に貼り付けてください。');
        btn.classList.toggle('done', ok);
        btn.textContent = ok ? 'コピーしました' : '長押しでコピーしてください';
        if (note && note.hasAttribute('data-note')) note.textContent = ok ? 'マインクラフトの「サーバーを追加」に貼り付けてください。' : '';
        setTimeout(function () { btn.classList.remove('done'); btn.textContent = label; }, 2200);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
      else {
        var ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select();
        var ok = false; try { ok = document.execCommand('copy'); } catch (e) {}
        document.body.removeChild(ta); done(ok);
      }
    });
  });

  // ── 次の夜祭（毎週土曜21時・日本時間）と今週のゲーム ──
  function nextFest(now) {
    var J = 9 * 3600000;
    var j = new Date(now + J); // 日本時間を UTC の入れ物で扱う
    var f = new Date(Date.UTC(j.getUTCFullYear(), j.getUTCMonth(), j.getUTCDate(), 21, 0, 0));
    f.setUTCDate(f.getUTCDate() + ((6 - j.getUTCDay() + 7) % 7));
    if (now + J > f.getTime() + 90 * 60000) f.setUTCDate(f.getUTCDate() + 7);
    var first = Date.UTC(2026, 10, 7, 21, 0, 0); // 最初の夜祭は開幕の夜
    if (f.getTime() < first) f = new Date(first);
    var week = Math.max(0, Math.floor((Date.UTC(f.getUTCFullYear(), f.getUTCMonth(), f.getUTCDate()) - Date.UTC(2026, 0, 5)) / 604800000));
    return { at: f.getTime() - J, month: f.getUTCMonth() + 1, day: f.getUTCDate(), game: GAMES[week % 4], week: week };
  }

  function tick() {
    var now = Date.now();
    var left = SEASON_START - now;
    var sc = split(left);
    $$('[data-season-short]').forEach(function (el) { el.textContent = left <= 0 ? '開催中' : '開幕まで ' + sc.d + '日 ' + sc.h + ':' + sc.m + ':' + sc.s; });
    $$('[data-season-cd]').forEach(function (el) {
      if (left <= 0) { el.hidden = true; return; }
      ['d', 'h', 'm', 's'].forEach(function (k) { var b = $('[data-u="' + k + '"]', el); if (b) b.textContent = sc[k]; });
    });
    $$('[data-season-live]').forEach(function (el) { el.hidden = left > 0; });
    var f = nextFest(now), fc = split(f.at - now), live = now >= f.at;
    $$('[data-fest-date]').forEach(function (el) { el.innerHTML = '次の夜祭は <span style="white-space:nowrap">' + f.month + '月' + f.day + '日（土）21:00</span>'; });
    // 開幕の夜がそのまま最初の夜祭のときは、同じ秒読みを2回並べない（シーズンの秒読みがあるページだけ）
    var twin = !live && Math.abs(f.at - SEASON_START) < 60000 && !!$('[data-season-cd]');
    $$('[data-fest-lead]').forEach(function (el) { el.textContent = live ? 'ただいま開催中です。今すぐログインして参加できます。' : twin ? '開幕の夜が、最初の夜祭です。21時の開幕と同時に、120秒の募集が始まります。' : '21時になると、120秒の募集が始まります。何もしなければ参加です。'; });
    $$('[data-fest-cd]').forEach(function (el) { if (twin && el.closest('[data-twin-hide]')) { el.hidden = true; return; } el.hidden = false; ['d', 'h', 'm', 's'].forEach(function (k) { var b = $('[data-u="' + k + '"]', el); if (b) b.textContent = fc[k]; }); });
    $$('[data-fest-game]').forEach(function (el) { el.textContent = f.game.name; });
    $$('[data-fest-desc]').forEach(function (el) { el.textContent = f.game.desc; });
    liveBar(f, now);
    $$('[data-rot]').forEach(function (el) { el.setAttribute('data-now', String(f.week % 4)); $$('[data-g]', el).forEach(function (r) { r.classList.toggle('cur', r.getAttribute('data-g') === String(f.week % 4)); }); });
  }
  // ── 夜祭の帯：開始30分前から「まもなく」、開催中は「いま」 ──
  var bar = null, barOff = false;
  try { barOff = sessionStorage.getItem('liveOff') === '1'; } catch (e) {}
  function liveBar(f, now) {
    var left = f.at - now, live = now >= f.at && now < f.at + 90 * 60000, soon = left > 0 && left <= 30 * 60000;
    if (!(live || soon) || barOff) { if (bar) bar.hidden = true; return; }
    if (!bar) {
      bar = document.createElement('div');
      bar.className = 'live';
      bar.innerHTML = '<span class="live-i" aria-hidden="true"></span><span class="live-t"></span><a href="events.html" class="live-a">夜祭について</a><button type="button" class="live-c" data-copy="' + ADDRESS + '">アドレスをコピー</button><button type="button" class="live-x" aria-label="この帯を閉じる">×</button>';
      document.body.appendChild(bar);
      bar.querySelector('.live-x').addEventListener('click', function () { barOff = true; bar.hidden = true; try { sessionStorage.setItem('liveOff', '1'); } catch (e) {} });
      bar.querySelector('.live-c').addEventListener('click', function () {
        if (navigator.clipboard) navigator.clipboard.writeText(ADDRESS).then(function () { toast('アドレスをコピーしました', ADDRESS); });
      });
    }
    bar.hidden = false;
    bar.classList.toggle('now', live);
    var s = split(left);
    bar.querySelector('.live-t').innerHTML = live ? '<b>いま夜祭を開催中</b><span>今夜のゲーム「' + f.game.name + '」</span>' : '<b>今夜21時から夜祭</b><span class="dot">あと ' + s.m + ':' + s.s + '</span>';
  }

  tick(); setInterval(tick, 1000);

  // ── いまの参加人数（サーバーが動いているときだけ表示） ──
  var on = $('[data-online]');
  if (on && window.fetch) {
    fetch('https://api.mcsrvstat.us/3/' + ADDRESS).then(function (r) { return r.json(); }).then(function (d) {
      if (d && d.online && d.players) { on.querySelector('b').textContent = d.players.online; on.classList.add('on'); }
    }).catch(function () {});
  }

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(pointer: fine)').matches;

  // ── 予告編：再生すると劇場のように、まわりを暗くする ──
  $$('[data-film]').forEach(function (box) {
    var v = $('video', box), btn = $('.film-play', box);
    var exit = function () { document.body.classList.remove('theater'); };
    var play = function () { v.controls = true; v.play(); };
    btn.addEventListener('click', play);
    v.addEventListener('play', function () { box.classList.add('on'); document.body.classList.add('theater'); });
    v.addEventListener('pause', exit);
    v.addEventListener('ended', function () { exit(); box.classList.remove('on'); v.controls = false; });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && document.body.classList.contains('theater')) v.pause(); });
    document.addEventListener('click', function (e) { if (document.body.classList.contains('theater') && !box.contains(e.target)) v.pause(); });
  });

  // ── 深さの目盛り（PC）：いま読んでいる地層の Y を右端に ──
  var alt = $('.alt'), depths = $$('.stratum .depth');
  if (alt && depths.length > 1 && 'IntersectionObserver' in window) {
    var altT = $('.alt-t', alt), al = $('.alt-l', alt);
    var secs = depths.map(function (d) { return { el: d.closest('.stratum'), t: d.textContent.trim() }; });
    var pick = function () {
      var y = window.innerHeight * 0.45, cur = null;
      secs.forEach(function (s) { var r = s.el.getBoundingClientRect(); if (r.top < y && r.bottom > y) cur = s; });
      var doc = document.documentElement, p = Math.min(1, Math.max(0, window.scrollY / Math.max(1, doc.scrollHeight - window.innerHeight)));
      al.style.top = altT.style.top = (p * 100).toFixed(2) + '%';
      alt.classList.toggle('on', !!cur);
      if (cur && altT.textContent !== cur.t) { altT.textContent = cur.t; altT.classList.remove('pop'); void altT.offsetWidth; altT.classList.add('pop'); }
    };
    var tk = false;
    window.addEventListener('scroll', function () { if (!tk) { tk = true; requestAnimationFrame(function () { tk = false; pick(); }); } }, { passive: true });
    pick();
  }

  // ── 灯りを持って歩く（PC）：マウスのまわりだけ、ほんのり明るい ──
  var glow = $('.glow');
  if (glow && fine && !reduce) {
    var gx = 0, gy = 0, gt = false;
    window.addEventListener('pointermove', function (e) {
      gx = e.clientX; gy = e.clientY;
      if (!gt) { gt = true; requestAnimationFrame(function () { gt = false; glow.style.transform = 'translate(' + gx + 'px,' + gy + 'px)'; glow.classList.add('on'); }); }
    }, { passive: true });
    document.addEventListener('pointerleave', function () { glow.classList.remove('on'); });
  }

  // ── 星 ──
  $$('.stars').forEach(function (box) {
    // トップの3Dの夜空と同じ：小さな四角い星を多めに、明るい星だけ少しにじませる
    var n = window.innerWidth < 760 ? 70 : 140, h = '';
    for (var i = 0; i < n; i++) {
      var r0 = rnd(), z = r0 > 0.93 ? 3 : r0 > 0.55 ? 2 : 1, d = 0.4 + rnd() * 1.8, y = Math.pow(rnd(), 1.4) * 72;
      h += '<span class="star' + (z === 3 ? ' big' : '') + '" style="left:' + (rnd() * 100).toFixed(2) + '%;top:' + y.toFixed(2) + '%;width:' + z + 'px;height:' + z + 'px;--o:' + (0.45 + rnd() * 0.5).toFixed(2) + ';animation-delay:' + d.toFixed(2) + 's,' + (d + rnd() * 3).toFixed(2) + 's;animation-duration:1s,' + (2 + rnd() * 4).toFixed(2) + 's"></span>';
    }
    box.innerHTML = h;
  });

  // ── トップの景色（地形・灯籠・灯路） ──
  var scene = $('[data-scene]');
  if (scene) {
    var hills = function (w, h, step, base, amp, f1, f2) {
      var p = '0,' + h;
      for (var x = 0; x < w; x += step) {
        var y = Math.max(4, Math.round((h - (base + amp * Math.sin(x / f1) + amp * 0.55 * Math.sin(x / f2 + 1.3))) / 8) * 8);
        p += ' ' + x + ',' + y + ' ' + (x + step) + ',' + y;
      }
      return p + ' ' + w + ',' + h;
    };
    var at = { 4: 0, 10: 1, 17: 2, 24: 3, 30: 4, 37: 5, 44: 6 }, cols = '', road = [];
    var tpl = $('#tpl-cast'), who = tpl ? $$('.who', tpl.content) : [];
    var put = { 13: who[0], 41: who[1] };
    for (var i = 0; i < 48; i++) {
      var hh = Math.max(3, Math.round(4 + 1.6 * Math.sin(i * 0.42) + 1.2 * Math.sin(i * 0.19 + 2) + (rnd() > 0.8 ? 1 : 0)));
      var li = at[i], has = li !== undefined, d2 = 2.6 + (has ? li : 0) * 0.3;
      cols += '<div class="col" style="height:' + (hh * 26) + 'px">' + (has ? '<div class="lan"><div class="lan-glow" style="animation-delay:' + d2.toFixed(2) + 's,' + (d2 + 0.8).toFixed(2) + 's"></div><div class="lan-cap"></div><div class="lan-head" style="animation-delay:' + d2.toFixed(2) + 's"></div><div class="lan-post"></div></div>' : '') + (put[i] ? put[i].outerHTML : '') + '</div>';
      if (has) road.push(((i + 0.5) * 30).toFixed(0) + ',' + (300 - hh * 26 - 40));
    }
    scene.innerHTML =
      '<div class="layer" style="height:260px"><svg viewBox="0 0 960 250" preserveAspectRatio="none"><polygon points="' + hills(960, 250, 32, 150, 40, 120, 53) + '" fill="#17274E"/></svg></div>' +
      '<div class="layer" style="height:210px"><svg viewBox="0 0 960 200" preserveAspectRatio="none"><polygon points="' + hills(960, 200, 20, 96, 30, 80, 37) + '" fill="#1F3460"/></svg></div>' +
      '<div class="layer" style="height:300px"><div class="terrain">' + cols + '</div><svg class="road" viewBox="0 0 1440 300" preserveAspectRatio="none"><polyline class="road-base" points="' + road.join(' ') + '" pathLength="100"/><polyline class="road-flow" points="' + road.join(' ') + '" pathLength="100"/></svg></div>';
  }

  // ── 夜祭の提灯 ──
  $$('[data-garland]').forEach(function (g) {
    var h = '<svg viewBox="0 0 100 40" preserveAspectRatio="none" style="position:absolute;left:0;top:0;width:100%;height:60px"><path d="M0 2 Q50 40 100 2" fill="none" stroke="rgba(238,234,248,.35)" stroke-width="0.4"/></svg>';
    for (var i = 0; i < 11; i++) {
      var t = (i + 0.5) / 11, sag = 1 - Math.pow(2 * t - 1, 2), pink = i % 2 === 1;
      h += '<div class="gl" style="left:calc(' + (t * 100).toFixed(2) + '% - 11px);animation-delay:' + (-i * 0.37).toFixed(2) + 's"><s style="height:' + (6 + sag * 46 + (i % 3) * 10).toFixed(0) + 'px"></s><u></u><b style="background:' + (pink ? '#F29BB8' : '#F2B544') + ';box-shadow:0 0 22px 6px ' + (pink ? 'rgba(242,155,184,.5)' : 'rgba(242,181,68,.55)') + '"></b></div>';
    }
    g.innerHTML = h;
  });

  // ── 機種の切り替え ──
  $$('[role="tablist"]').forEach(function (list) {
    var tabs = $$('[role="tab"]', list);
    var show = function (tab, focus) {
      tabs.forEach(function (t) {
        var onNow = t === tab;
        t.setAttribute('aria-selected', onNow ? 'true' : 'false');
        t.tabIndex = onNow ? 0 : -1;
        var p = document.getElementById(t.getAttribute('aria-controls'));
        if (p) p.hidden = !onNow;
      });
      if (focus) tab.focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { show(t); });
      t.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); show(tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length], true); }
      });
    });
  });

  // ── #名前 でそのタブを開く（遊び方を選ぶ など） ──
  var openHash = function () { var h = location.hash.slice(1); if (!h) return; var t = document.getElementById('t-' + h); if (t && t.getAttribute('role') === 'tab') t.click(); };
  openHash(); window.addEventListener('hashchange', openHash);

  // ── はじめる：スマホ・ゲーム機で開いたら、その機種のタブを先に開く ──
  (function () {
    var ua = navigator.userAgent || '';
    var mob = /iPhone|iPad|iPod|Android/i.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
    var con = /Nintendo|PlayStation|Xbox/i.test(ua);
    var id = con ? 't-con' : mob ? 't-mob' : null;
    var t = id && document.getElementById(id);
    if (t && !location.hash) t.click();
    if (t) { var h = document.querySelector('[data-device-note]'); if (h) h.hidden = false; }
  })();

  // ── サイト内を探す（Ctrl+K / ⌘K / 虫めがね） ──
  (function () {
    var IDX = null, box = null, input, list, cur = 0, kind = 'すべて', hits = [];
    var KINDS = ['すべて', '技', '灯魚', '証', 'コマンド', 'ページ'];
    var norm = function (s) {
      return (s || '').toLowerCase().replace(/[Ａ-Ｚａ-ｚ０-９]/g, function (c) { return String.fromCharCode(c.charCodeAt(0) - 0xFEE0); })
        .replace(/[ァ-ヶ]/g, function (c) { return String.fromCharCode(c.charCodeAt(0) - 0x60); });
    };
    function load() {
      if (IDX) return Promise.resolve(IDX);
      return fetch('assets/search.json').then(function (r) { return r.json(); }).then(function (d) {
        IDX = d.map(function (x) { x._t = norm(x.t); x._s = norm(x.s); return x; }); return IDX;
      });
    }
    function build() {
      box = document.createElement('div');
      box.className = 'qs'; box.hidden = true;
      box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-label', 'サイト内を探す');
      box.innerHTML = '<div class="qs-in"><label class="qs-f"><span class="sr">探す</span><input type="search" placeholder="技・灯魚・証・コマンド・ページを探す" autocomplete="off"><kbd class="dot">Esc</kbd></label>' +
        '<div class="qs-k">' + KINDS.map(function (k) { return '<button type="button" data-k="' + k + '"' + (k === kind ? ' aria-pressed="true"' : ' aria-pressed="false"') + '>' + k + '</button>'; }).join('') + '</div>' +
        '<ul class="qs-l" role="listbox"></ul><p class="qs-h mu"><span>↑↓ でえらぶ</span><span>Enter でひらく</span><span>Esc で閉じる</span></p></div>';
      document.body.appendChild(box);
      input = box.querySelector('input'); list = box.querySelector('.qs-l');
      input.addEventListener('input', function () { cur = 0; run(); });
      box.addEventListener('click', function (e) {
        if (e.target === box) close();
        var k = e.target.closest('[data-k]');
        if (k) { kind = k.getAttribute('data-k'); box.querySelectorAll('[data-k]').forEach(function (b) { b.setAttribute('aria-pressed', b === k ? 'true' : 'false'); }); cur = 0; run(); input.focus(); }
      });
      list.addEventListener('mousemove', function (e) { var li = e.target.closest('li[data-i]'); if (li) { cur = +li.getAttribute('data-i'); mark(); } });
      box.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { e.preventDefault(); close(); }
        else if (e.key === 'ArrowDown') { e.preventDefault(); cur = Math.min(hits.length - 1, cur + 1); mark(true); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); cur = Math.max(0, cur - 1); mark(true); }
        else if (e.key === 'Enter' && hits[cur]) { e.preventDefault(); location.href = hits[cur].u; close(); }
      });
    }
    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    function run() {
      var q = norm(input.value.trim()), words = q.split(/\s+/).filter(Boolean);
      var pool = IDX.filter(function (x) { return kind === 'すべて' || x.k === kind; });
      if (!words.length) { hits = kind === 'すべて' ? IDX.filter(function (x) { return x.k === 'ページ'; }).slice(0, 12) : pool.slice(0, 40); }
      else {
        hits = pool.map(function (x) {
          var sc = 0;
          for (var i = 0; i < words.length; i++) {
            var w = words[i], a = x._t.indexOf(w), b = x._s.indexOf(w);
            if (a < 0 && b < 0) return null;
            sc += a === 0 ? 30 : a > 0 ? 15 : 4;
          }
          return [sc - x.t.length * 0.1, x];
        }).filter(Boolean).sort(function (a, b) { return b[0] - a[0]; }).slice(0, 40).map(function (a) { return a[1]; });
      }
      list.innerHTML = hits.length ? hits.map(function (x, i) {
        return '<li data-i="' + i + '" role="option"><a href="' + x.u + '" style="--c:' + (x.c || 'var(--amber)') + '"><span class="qs-kd">' + x.k + '</span><b>' + esc(x.t) + '</b><small>' + esc(x.s) + '</small></a></li>';
      }).join('') : '<li class="qs-0">見つかりませんでした。ことばを短くしてみてください。</li>';
      mark();
    }
    function mark(scroll) {
      list.querySelectorAll('li[data-i]').forEach(function (li) {
        var on = +li.getAttribute('data-i') === cur;
        li.classList.toggle('on', on);
        if (on && scroll) li.scrollIntoView({ block: 'nearest' });
      });
    }
    var last = null;
    function open() {
      if (!box) build();
      last = document.activeElement;
      box.hidden = false; document.body.classList.add('qs-open');
      input.value = ''; input.focus();
      list.innerHTML = '<li class="qs-0">読みこみ中…</li>';
      load().then(run).catch(function () { list.innerHTML = '<li class="qs-0">読みこめませんでした。</li>'; });
    }
    function close() { if (!box) return; box.hidden = true; document.body.classList.remove('qs-open'); if (last && last.focus) last.focus(); }
    $$('[data-qs]').forEach(function (b) { b.addEventListener('click', open); });
    document.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) { e.preventDefault(); if (box && !box.hidden) close(); else open(); }
    });
  })();

  // ── 体験：灯籠を置く、夜にする、灯喰いから守る ──
  var demo = $('[data-demo]');
  if (demo) {
    var narrow = window.matchMedia('(max-width: 640px)').matches;
    var W = narrow ? 10 : 16, H = narrow ? 9 : 7, MAX = 10, LINK = 4.3;
    var grid = $('.grid', demo), msg = $('[data-msg]', demo), nightBtn = $('[data-night]', demo), resetBtn = $('[data-reset]', demo);
    var kinds = [];
    var LX = narrow ? 7.4 : 12, LY = narrow ? 6.8 : 4.4;
    for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) { var dx = x - LX, dy = y - LY; kinds.push(dx * dx / 6 + dy * dy / 2.2 < 1.5 ? 'w' : 'g'); }
    var st = { lan: [], night: false, saved: 0, lost: 0, shard: 0, eater: null };
    var START = narrow ? [22, 26, 35] : [34, 38, 53];
    grid.style.gridTemplateColumns = 'repeat(' + W + ', minmax(0, 1fr))';
    var say = function (t) { msg.textContent = t; };
    var X = function (i) { return i % W; }, Y = function (i) { return Math.floor(i / W); };
    var find = function (i) { for (var k = 0; k < st.lan.length; k++) if (st.lan[k].i === i) return st.lan[k]; return null; };
    var edges = function () {
      var out = [], L = st.lan.filter(function (l) { return !l.out; });
      for (var a = 0; a < L.length; a++) for (var b = a + 1; b < L.length; b++) {
        var ddx = X(L[a].i) - X(L[b].i), ddy = Y(L[a].i) - Y(L[b].i);
        if (ddx * ddx + ddy * ddy <= LINK * LINK) out.push([L[a], L[b]]);
      }
      return out;
    };
    var linksOf = function (l, es) { return es.filter(function (e) { return e[0] === l || e[1] === l; }).length; };
    var COLOR = { g: ['#16241A', '#3D5E2C', '#6FA347'], w: ['#0E1930', '#2A4C82', '#4F7FB8'] };
    var COLOR_DAY = { g: ['#5E8E3F', '#67994A', '#6FA347'], w: ['#3F6CA8', '#4775B0', '#4F7FB8'] };
    var tiles = [];
    grid.innerHTML = kinds.map(function (k, i) { return '<button type="button" class="tile" data-i="' + i + '"></button>'; }).join('') + '<svg class="links" viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none" aria-hidden="true"><path d="M0 0"/></svg>';
    tiles = $$('.tile', grid);
    var path = $('.links path', grid);
    var draw = function () {
      var es = edges(), safe = 0;
      tiles.forEach(function (t, i) {
        var dmin = 99;
        st.lan.forEach(function (l) { if (l.out) return; var d = Math.max(Math.abs(X(l.i) - X(i)), Math.abs(Y(l.i) - Y(i))); if (d < dmin) dmin = d; });
        var lvl = dmin <= 1 ? 2 : dmin === 2 ? 1 : 0, k = kinds[i], l = find(i);
        if (lvl > 0 && k !== 'w') safe++;
        t.style.backgroundColor = (st.night ? COLOR : COLOR_DAY)[k][lvl];
        t.innerHTML = l ? '<span class="mini' + (l.out ? ' out' : '') + '"></span>' : '';
        t.setAttribute('aria-label', (Y(i) + 1) + '行' + (X(i) + 1) + '列、' + (k === 'w' ? '水' : '草地') + (l ? (l.out ? '、消えた灯籠。押すと灯し直す' : '、灯籠あり') : (lvl > 0 ? '、灯りの中' : '、灯りの外')));
      });
      path.setAttribute('d', es.map(function (e) { return 'M' + (X(e[0].i) + 0.5) + ' ' + (Y(e[0].i) + 0.5) + 'L' + (X(e[1].i) + 0.5) + ' ' + (Y(e[1].i) + 0.5); }).join(' ') || 'M0 0');
      $('[data-s="lan"]', demo).textContent = st.lan.length;
      $('[data-s="road"]', demo).textContent = es.length;
      $('[data-s="saved"]', demo).textContent = st.saved;
      $('[data-s="shard"]', demo).textContent = st.shard;
      nightBtn.textContent = st.night ? '朝にする' : '夜にする';
      nightBtn.setAttribute('aria-pressed', st.night ? 'true' : 'false');
    };
    var killEater = function (byPlayer) {
      var e = st.eater; if (!e) return;
      clearInterval(e.timer); e.el.remove(); st.eater = null;
      if (byPlayer) { st.saved++; st.shard++; say('灯喰いを倒して、灯りを守りました。欠片をひとつ手に入れました。欠片を集めると、加護を解放できます。'); draw(); }
    };
    var spawn = function () {
      if (!st.night || st.eater) return;
      var es = edges(), lit = st.lan.filter(function (l) { return !l.out; });
      if (lit.length < 3) { say('灯籠が3基より少ないあいだは、灯喰いは来ません。小さな拠点は狙われないきまりです。'); return; }
      lit.sort(function (a, b) { return linksOf(a, es) - linksOf(b, es); });
      var t = lit[0], n = linksOf(t, es), need = 3200 + n * 1800, t0 = Date.now();
      var el = document.createElement('button');
      el.type = 'button'; el.className = 'eater'; el.setAttribute('aria-label', '灯喰い。押して倒す');
      el.innerHTML = '<span></span><em><b></b></em>';
      el.style.width = (100 / W) + '%';
      el.style.left = ((X(t.i) + (X(t.i) < W - 1 ? 1.5 : -0.5)) / W * 100) + '%';
      el.style.top = ((Y(t.i) + 0.5) / H * 100) + '%';
      grid.appendChild(el);
      var e = { el: el, target: t };
      el.addEventListener('click', function (ev) { ev.stopPropagation(); killEater(true); });
      say('灯喰いが、灯路の少ない端の灯籠を喰いはじめました。灯喰いを押して倒してください。灯路が ' + n + ' 本つながっているので、喰い終わるまで ' + (need / 1000).toFixed(1) + ' 秒です。');
      e.timer = setInterval(function () {
        var p = (Date.now() - t0) / need;
        el.querySelector('b').style.width = Math.min(100, p * 100) + '%';
        if (p >= 1) {
          t.out = true; st.lost++; killEater(false);
          say('灯籠が喰われて、青い冷たい火になりました。そこを通っていた灯路も消えています。青い灯籠を押すと、灯し直せます。');
          draw();
        }
      }, 80);
      st.eater = e;
    };
    grid.addEventListener('click', function (ev) {
      var t = ev.target.closest('.tile'); if (!t) return;
      var i = Number(t.getAttribute('data-i')), l = find(i);
      if (l && l.out) { l.out = false; say('灯し直しました。本番では、他の人の灯籠を灯し直すと経験値がもらえます。'); draw(); return; }
      if (l) {
        if (st.eater && st.eater.target === l) killEater(false);
        st.lan.splice(st.lan.indexOf(l), 1); say('灯籠を取り除きました。'); draw(); return;
      }
      if (kinds[i] === 'w') { say('水の上には灯籠を置けません。'); return; }
      if (st.lan.length >= MAX) { say('この体験では、灯籠は ' + MAX + ' 基までです。どれかを取り除いてください。'); return; }
      var before = edges().length; st.lan.push({ i: i, out: false }); var after = edges().length;
      say(after > before ? '灯路がつながりました。灯路の上は足が速くなり、つながるほど灯喰いに喰われにくくなります。' : '灯籠を置きました。近くにもう1基置くと、灯路でつながります。');
      draw();
    });
    nightBtn.addEventListener('click', function () {
      st.night = !st.night;
      if (!st.night) { killEater(false); say('朝になりました。本番では、夜明けに、つながっている灯籠へ火が戻ります。'); }
      else say('夜になりました。まもなく灯喰いが来ます。');
      draw();
      if (st.night) setTimeout(spawn, 1200);
    });
    resetBtn.addEventListener('click', function () {
      killEater(false);
      st.lan = START.map(function (i) { return { i: i, out: false }; }); st.night = false; st.saved = 0; st.lost = 0; st.shard = 0;
      say('最初の配置に戻しました。'); draw();
    });
    setInterval(function () { if (st.night && !st.eater) spawn(); }, 3800);
    st.lan = START.map(function (i) { return { i: i, out: false }; });
    draw();
  }
})();
