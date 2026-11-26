/* サーバーが自動で書きかえる data/live/*.json を読んで、ページに出す（運営の手はいらない）。
   読めなかったときは、ページに最初から書いてある中身のまま。 */
(function () {
  var bust = '?t=' + Math.floor(Date.now() / 600000); // 10分ごとに新しく読む
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function get(path, done) {
    fetch(path + bust, { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (j) { if (j) done(j); }).catch(function () {});
  }

  // ── 支え手の壁 ──
  var wall = document.getElementById('live-wall');
  if (wall) get('data/live/supporters.json', function (list) {
    if (!Array.isArray(list)) return;
    var face = wall.getAttribute('data-face') || '';
    var items = list.filter(function (s) { return s && String(s.mcid || '').trim(); });
    if (!items.length) return;
    var html = items.map(function (s) {
      var m = String(s.mcid).trim();
      var src = m.charAt(0) === '.' ? face : 'https://mc-heads.net/avatar/' + encodeURIComponent(m) + '/64';
      var since = String(s.since || '').slice(0, 7).replace('-', '.');
      return '<li class="sup"><img class="face" src="' + esc(src) + '" alt="" width="64" height="64" loading="lazy" decoding="async"><b class="dot">' + esc(m) + '</b><small>' + esc(since) + ' から</small></li>';
    }).join('');
    wall.innerHTML = '<ul class="wall">' + html + '</ul>';
    Array.prototype.forEach.call(wall.querySelectorAll('img.face'), function (img) {
      img.onerror = function () { img.onerror = null; img.src = face; };
      if (img.complete && img.naturalWidth === 0) img.src = face;
    });
    var n = document.getElementById('live-wall-n');
    if (n) n.textContent = items.length;
  });

  // ── 里の一覧 ──
  var grid = document.getElementById('sato-grid');
  if (grid) get('data/live/satos.json', function (d) {
    var satos = (d && d.satos) || [];
    var meta = document.getElementById('sato-meta');
    if (meta) meta.innerHTML = '<b class="dot">' + satos.length + '</b> の里' + (d.updated ? '<span class="mu">（' + esc(d.updated) + ' 時点）</span>' : '');
    if (!satos.length) {
      grid.innerHTML = '<p class="wall-msg"><b>まだ里はありません。</b>最初の里を開くのは、あなたかもしれません。ひとりなら「庵」から。</p>';
    } else {
      grid.innerHTML = satos.map(function (s) {
        var col = esc(s.color || '#55FFFF');
        var grade = s.iori ? '庵' : esc(s.grade);
        var badges = (s.recruiting ? '<span class="sato-tag on">民を募集中</span>' : '') + (s.streak > 0 ? '<span class="sato-tag">続く灯 ' + s.streak + '日</span>' : '');
        var fac = (s.facilities || []).length ? '<p class="sato-row"><span>施設</span>' + s.facilities.map(esc).join('・') + '</p>' : '';
        var lm = (s.landmarks || []).length ? '<p class="sato-row"><span>名所</span>' + s.landmarks.map(function (x) { return esc(x.name); }).join('・') + '</p>' : '';
        var jobs = s.jobs ? Object.keys(s.jobs).filter(function (k) { return s.jobs[k] > 0; }).map(function (k) { return esc(k) + ' ' + s.jobs[k]; }).join('・') : '';
        var ch = (s.chronicle || []).slice().reverse();
        var chron = ch.length ? '<details class="sato-chron"><summary>里の年代記（' + ch.length + '）</summary><ul class="chron">' + ch.map(function (h) { return '<li>' + esc(h) + '</li>'; }).join('') + '</ul></details>' : '';
        return '<article class="sato-card" style="--c:' + col + '">'
          + '<div class="sato-top"><span class="sato-grade g' + (s.iori ? 'i' : esc(s.gradeIndex)) + '">' + grade + '</span><h3 class="disp">' + esc(s.name) + '</h3></div>'
          + (s.motto ? '<p class="sato-motto">「' + esc(s.motto) + '」</p>' : '')
          + '<div class="sato-nums"><p><b class="dot">' + esc(s.people) + '</b><span>民</span></p><p><b class="dot">' + esc(s.lanterns) + '</b><span>土地の灯籠</span></p><p><b class="dot">' + Number(s.power || 0).toLocaleString() + '</b><span>里の力</span></p></div>'
          + '<p class="sato-row"><span>里長</span>' + esc(s.leader) + '<span class="sep">・</span><span>開いた日</span>' + esc(s.founded) + '</p>'
          + (jobs ? '<p class="sato-row"><span>職</span>' + jobs + '</p>' : '') + fac + lm
          + '<div class="sato-tags">' + badges + '</div>' + chron + '</article>';
      }).join('');
    }
    var wc = document.getElementById('world-chron');
    if (wc) {
      var h = (d.history || []).slice(-40).reverse();
      wc.innerHTML = h.length ? h.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') : '<li class="mu">まだ書きとめた出来事はありません。</li>';
    }
  });
})();
