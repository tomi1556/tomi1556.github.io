/* 灯技 Wiki：技の検索・しぼりこみ、灯魚図鑑のしぼりこみ */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // 全角・半角、ひらがな・カタカナを同じに見る
  function norm(s) {
    return (s || '').toLowerCase()
      .replace(/[Ａ-Ｚａ-ｚ０-９]/g, function (c) { return String.fromCharCode(c.charCodeAt(0) - 0xFEE0); })
      .replace(/[ァ-ヶ]/g, function (c) { return String.fromCharCode(c.charCodeAt(0) - 0x60); })
      .replace(/\s+/g, ' ').trim();
  }

  function setup(opts) {
    var list = $(opts.list);
    if (!list) return;
    var items = $$(opts.item, list);
    var input = opts.input ? $(opts.input) : null;
    var count = $(opts.count), clear = $(opts.clear), empty = opts.empty ? $(opts.empty) : null;
    var chips = $$('.chip-f', list.closest('.finder'));
    var on = {};
    items.forEach(function (el) { el._q = norm(el.getAttribute('data-q') || el.textContent); });

    function apply() {
      var words = input ? norm(input.value).split(' ').filter(Boolean) : [];
      var n = 0;
      items.forEach(function (el) {
        var ok = true;
        for (var f in on) {
          if (!on[f].length) continue;
          if (on[f].indexOf(el.getAttribute('data-' + f)) < 0) { ok = false; break; }
        }
        if (ok) for (var i = 0; i < words.length; i++) if (el._q.indexOf(words[i]) < 0) { ok = false; break; }
        el.hidden = !ok;
        if (ok) n++;
      });
      if (count) count.textContent = n;
      var any = words.length > 0 || Object.keys(on).some(function (f) { return on[f].length; });
      if (clear) clear.hidden = !any;
      if (empty) empty.hidden = n > 0;
    }

    chips.forEach(function (b) {
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-f'), v = b.getAttribute('data-v');
        on[f] = on[f] || [];
        var i = on[f].indexOf(v);
        if (i < 0) on[f].push(v); else on[f].splice(i, 1);
        b.setAttribute('aria-pressed', i < 0 ? 'true' : 'false');
        apply();
      });
    });
    if (input) {
      input.addEventListener('input', apply);
      document.addEventListener('keydown', function (e) {
        if (e.key === '/' && document.activeElement !== input && !/input|textarea/i.test(document.activeElement.tagName)) { e.preventDefault(); input.focus(); }
        if (e.key === 'Escape' && document.activeElement === input) { input.value = ''; apply(); input.blur(); }
      });
      var q = new URLSearchParams(location.search).get('q');
      if (q) input.value = q;
    }
    if (clear) clear.addEventListener('click', function () {
      on = {};
      chips.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
      if (input) input.value = '';
      apply();
    });
    apply();
  }

  setup({ list: '#wl', item: '.sk', input: '#wq', count: '#wn', clear: '#wclear', empty: '#wempty' });
  setup({ list: '#fl', item: '.fc', count: '#fn', clear: '#fclear' });

  // 技の木のタイルを押したら、説明の札を光らせる
  function flash() {
    var id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    var el = document.getElementById(id);
    if (!el || !el.classList.contains('nc')) return;
    el.classList.remove('flash');
    void el.offsetWidth;
    el.classList.add('flash');
  }
  window.addEventListener('hashchange', flash);
  flash();
})();
