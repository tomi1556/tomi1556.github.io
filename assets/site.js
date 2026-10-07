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

  // ── アドレスのコピー ──
  $$('[data-copy]').forEach(function (btn) {
    var label = btn.textContent;
    var note = btn.closest('.addr') && btn.closest('.addr').nextElementSibling;
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy') || ADDRESS;
      var done = function (ok) {
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
    $$('[data-fest-date]').forEach(function (el) { el.textContent = f.month + '月' + f.day + '日（土）21:00'; });
    $$('[data-fest-lead]').forEach(function (el) { el.textContent = live ? 'ただいま開催中です。今すぐログインして参加できます。' : '21時になると、120秒の募集が始まります。何もしなければ参加です。'; });
    $$('[data-fest-cd]').forEach(function (el) { ['d', 'h', 'm', 's'].forEach(function (k) { var b = $('[data-u="' + k + '"]', el); if (b) b.textContent = fc[k]; }); });
    $$('[data-fest-game]').forEach(function (el) { el.textContent = f.game.name; });
    $$('[data-fest-desc]').forEach(function (el) { el.textContent = f.game.desc; });
    $$('[data-rot]').forEach(function (el) { el.setAttribute('data-now', String(f.week % 4)); $$('[data-g]', el).forEach(function (r) { r.classList.toggle('cur', r.getAttribute('data-g') === String(f.week % 4)); }); });
  }
  tick(); setInterval(tick, 1000);

  // ── いまの参加人数（サーバーが動いているときだけ表示） ──
  var on = $('[data-online]');
  if (on && window.fetch) {
    fetch('https://api.mcsrvstat.us/3/' + ADDRESS).then(function (r) { return r.json(); }).then(function (d) {
      if (d && d.online && d.players) { on.querySelector('b').textContent = d.players.online; on.classList.add('on'); }
    }).catch(function () {});
  }

  // ── 星 ──
  $$('.stars').forEach(function (box) {
    var n = window.innerWidth < 760 ? 36 : 64, h = '';
    for (var i = 0; i < n; i++) {
      var z = rnd() > 0.85 ? 4 : 2, d = 0.4 + rnd() * 1.8;
      h += '<span class="star" style="left:' + (rnd() * 100).toFixed(2) + '%;top:' + (rnd() * 70).toFixed(2) + '%;width:' + z + 'px;height:' + z + 'px;animation-delay:' + d.toFixed(2) + 's,' + (d + rnd() * 3).toFixed(2) + 's;animation-duration:1s,' + (2 + rnd() * 3).toFixed(2) + 's"></span>';
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
    for (var i = 0; i < 48; i++) {
      var hh = Math.max(3, Math.round(4 + 1.6 * Math.sin(i * 0.42) + 1.2 * Math.sin(i * 0.19 + 2) + (rnd() > 0.8 ? 1 : 0)));
      var li = at[i], has = li !== undefined, d2 = 2.6 + (has ? li : 0) * 0.3;
      cols += '<div class="col" style="height:' + (hh * 26) + 'px">' + (has ? '<div class="lan"><div class="lan-glow" style="animation-delay:' + d2.toFixed(2) + 's,' + (d2 + 0.8).toFixed(2) + 's"></div><div class="lan-cap"></div><div class="lan-head" style="animation-delay:' + d2.toFixed(2) + 's"></div><div class="lan-post"></div></div>' : '') + '</div>';
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

  // ── 体験：灯籠を置く、夜にする、灯喰いから守る ──
  var demo = $('[data-demo]');
  if (demo) {
    var W = 16, H = 7, MAX = 10, LINK = 4.3;
    var grid = $('.grid', demo), msg = $('[data-msg]', demo), nightBtn = $('[data-night]', demo), resetBtn = $('[data-reset]', demo);
    var kinds = [];
    for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) { var dx = x - 12, dy = y - 4.4; kinds.push(dx * dx / 6 + dy * dy / 2.2 < 1.5 ? 'w' : 'g'); }
    var st = { lan: [], night: false, saved: 0, lost: 0, shard: 0, eater: null };
    var START = [34, 38, 53];
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
