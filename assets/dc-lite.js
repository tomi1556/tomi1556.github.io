/*
 * dc-lite.js — 灯原サイト用の小さな描画エンジン
 * <template id="dc"> のテンプレートと <script type="text/x-dc"> のロジックから画面を描画する。
 * 対応: {{path}} の差し込み / sc-for / sc-if / onClick・onMouseMove / ref / helmet
 * 差分更新には morphdom を使い、CSSアニメーションを途切れさせない。
 */
(function () {
  'use strict';

  class DCLogic {
    constructor(props) { this.props = props || {}; this.state = {}; }
    setState(patch) {
      const u = typeof patch === 'function' ? patch(this.state, this.props) : patch;
      this.state = Object.assign({}, this.state, u);
      if (this.__schedule) this.__schedule();
    }
    forceUpdate() { if (this.__schedule) this.__schedule(); }
  }

  const HOLE = /\{\{\s*([^}]+?)\s*\}\}/g;
  const WHOLE = /^\s*\{\{\s*([^}]+?)\s*\}\}\s*$/;
  const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']);
  const EVENTS = { onclick: 'click', onmousemove: 'mousemove' };

  const escText = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const escAttr = (s) => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');

  function lookup(path, scopes) {
    if (path === 'true') return true;
    if (path === 'false') return false;
    if (/^-?\d+(\.\d+)?$/.test(path)) return Number(path);
    const parts = path.split('.');
    for (let i = 0; i < scopes.length; i++) {
      const sc = scopes[i];
      if (sc != null && Object.prototype.hasOwnProperty.call(sc, parts[0])) {
        let v = sc[parts[0]];
        for (let k = 1; k < parts.length; k++) v = v == null ? undefined : v[parts[k]];
        return v;
      }
    }
    return undefined;
  }

  const show = (v) => (v == null ? '' : String(v));

  function renderNodes(nodes, scopes, ctx) {
    let out = '';
    for (let i = 0; i < nodes.length; i++) out += renderNode(nodes[i], scopes, ctx);
    return out;
  }

  function renderNode(node, scopes, ctx) {
    if (node.nodeType === 3) return escText(node.nodeValue.replace(HOLE, (_, p) => show(lookup(p, scopes))));
    if (node.nodeType !== 1) return '';
    const tag = node.localName;

    if (tag === 'sc-for') {
      const m = WHOLE.exec(node.getAttribute('list') || '');
      const list = m ? lookup(m[1], scopes) : null;
      const as = node.getAttribute('as') || 'item';
      if (!Array.isArray(list)) return '';
      let out = '';
      list.forEach((item, idx) => {
        const local = { $index: idx }; local[as] = item;
        out += renderNodes(node.childNodes, [local].concat(scopes), ctx);
      });
      return out;
    }
    if (tag === 'sc-if') {
      const m = WHOLE.exec(node.getAttribute('value') || '');
      return (m ? lookup(m[1], scopes) : false) ? renderNodes(node.childNodes, scopes, ctx) : '';
    }

    let attrs = '';
    for (let i = 0; i < node.attributes.length; i++) {
      const a = node.attributes[i];
      const name = a.name;
      if (name.indexOf('hint-') === 0) continue;
      const whole = WHOLE.exec(a.value);
      if (whole) {
        const v = lookup(whole[1], scopes);
        const lower = name.toLowerCase();
        if (lower === 'ref') {
          if (typeof v === 'function') { const id = 'r' + ctx.n++; ctx.refs[id] = v; attrs += ' data-dc-ref="' + id + '"'; }
          continue;
        }
        if (EVENTS[lower]) {
          if (typeof v === 'function') { const id = 'h' + ctx.n++; ctx.handlers[id] = v; attrs += ' data-dc-' + EVENTS[lower] + '="' + id + '"'; }
          continue;
        }
        if (v == null || v === false && name.indexOf('aria-') !== 0) continue;
        attrs += ' ' + name + '="' + escAttr(v) + '"';
      } else {
        attrs += ' ' + name + '="' + escAttr(a.value.replace(HOLE, (_, p) => show(lookup(p, scopes)))) + '"';
      }
    }
    if (VOID.has(tag)) return '<' + tag + attrs + '>';
    const inner = (tag === 'style' || tag === 'script') ? node.textContent : renderNodes(node.childNodes, scopes, ctx);
    return '<' + tag + attrs + '>' + inner + '</' + tag + '>';
  }

  function mount() {
    const tpl = document.getElementById('dc');
    const logicEl = document.querySelector('script[type="text/x-dc"]');
    const app = document.getElementById('app');
    if (!tpl || !logicEl || !app) return;

    const frag = tpl.content;
    const helmet = frag.querySelector('helmet');
    if (helmet) {
      Array.from(helmet.children).forEach((el) => document.head.appendChild(el.cloneNode(true)));
      helmet.remove();
    }

    let defaults = {};
    try {
      const spec = JSON.parse(logicEl.getAttribute('data-props') || '{}');
      Object.keys(spec).forEach((k) => { if (k[0] !== '$' && spec[k] && 'default' in spec[k]) defaults[k] = spec[k].default; });
    } catch (e) { console.error(e); }

    const Component = new Function('DCLogic', logicEl.textContent + '\n;return Component;')(DCLogic);
    const comp = new Component(defaults);
    if (!comp.props || !Object.keys(comp.props).length) comp.props = defaults;

    let handlers = {};
    let pending = false;
    let mounted = false;

    const render = () => {
      pending = false;
      const ctx = { n: 0, handlers: {}, refs: {} };
      const vals = comp.renderVals ? comp.renderVals() : {};
      const html = renderNodes(frag.childNodes, [vals], ctx);
      handlers = ctx.handlers;
      if (!mounted) {
        app.innerHTML = html;
      } else {
        window.morphdom(app, '<div>' + html + '</div>', {
          childrenOnly: true,
          onBeforeElUpdated(fromEl, toEl) {
            if (fromEl.isEqualNode(toEl)) return false;
            const s = fromEl.style;
            if (s) {
              for (let i = 0; i < s.length; i++) {
                const n = s[i];
                if (n.indexOf('--') === 0 && !toEl.style.getPropertyValue(n)) toEl.style.setProperty(n, s.getPropertyValue(n));
              }
            }
            return true;
          }
        });
      }
      app.querySelectorAll('[data-dc-ref]').forEach((el) => {
        const fn = ctx.refs[el.getAttribute('data-dc-ref')];
        if (fn) fn(el);
      });
    };
    comp.__schedule = () => {
      if (pending) return;
      pending = true;
      Promise.resolve().then(render);
    };

    const delegate = (type) => app.addEventListener(type, (e) => {
      let el = e.target;
      const attr = 'data-dc-' + type;
      while (el && el !== app) {
        if (el.nodeType === 1 && el.hasAttribute(attr)) {
          const fn = handlers[el.getAttribute(attr)];
          if (fn) fn(e);
          return;
        }
        el = el.parentNode;
      }
    });
    delegate('click');
    delegate('mousemove');

    render();
    mounted = true;
    if (comp.componentDidMount) comp.componentDidMount();
    window.addEventListener('pagehide', () => { if (comp.componentWillUnmount) comp.componentWillUnmount(); });
  }

  window.DCLogic = DCLogic;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
