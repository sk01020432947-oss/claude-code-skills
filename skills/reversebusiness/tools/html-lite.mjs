// 아주 작은 HTML 읽기 도구. 의존성 없음. 스크립트를 실행하지 않고 글자와 구조만 읽는다.
// 브라우저만큼 정확하지 않다. 닫히지 않은 태그는 너그럽게 넘어간다.

const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']);
const RAW = new Set(['script', 'style', 'textarea', 'title']);
const SKIP_TEXT = new Set(['script', 'style', 'noscript', 'template', 'svg', 'head', 'iframe', 'object']);
const SELF_NEST = new Set(['li', 'p', 'option', 'tr', 'td', 'th', 'dt', 'dd']);
const MAX_DEPTH = 200; // 이보다 깊이 겹친 요소는 더 내려가지 않고 옆에 붙인다

const NAMED = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', middot: '·', hellip: '…', copy: '©', reg: '®', trade: '™', laquo: '«', raquo: '»', ndash: '-', mdash: '-', rarr: '→', larr: '←' };
export function decode(s) {
  return String(s).replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, k) => {
    if (k[0] === '#') {
      const code = k[1] === 'x' || k[1] === 'X' ? parseInt(k.slice(2), 16) : parseInt(k.slice(1), 10);
      try { return Number.isFinite(code) ? String.fromCodePoint(code) : m; } catch { return m; }
    }
    return NAMED[k.toLowerCase()] ?? m;
  });
}

function parseAttrs(src) {
  const attrs = {};
  const re = /([^\s"'<>/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g;
  let m;
  while ((m = re.exec(src))) attrs[m[1].toLowerCase()] = decode(m[2] ?? m[3] ?? m[4] ?? '');
  return attrs;
}

export function parseHtml(html) {
  const src = String(html);
  const lower = src.toLowerCase();
  const root = { tag: '#root', attrs: {}, children: [], parent: null, depth: 0 };
  let cur = root;
  let i = 0;
  const n = src.length;
  const addText = (t) => { if (t) cur.children.push({ text: decode(t) }); };
  while (i < n) {
    const lt = src.indexOf('<', i);
    if (lt < 0) { addText(src.slice(i)); break; }
    if (lt > i) addText(src.slice(i, lt));
    if (src.startsWith('<!--', lt)) { const e = src.indexOf('-->', lt + 4); i = e < 0 ? n : e + 3; continue; }
    if (src[lt + 1] === '!' || src[lt + 1] === '?') { const e = src.indexOf('>', lt); i = e < 0 ? n : e + 1; continue; }
    const m = /^<\/?([a-zA-Z][a-zA-Z0-9:-]*)/.exec(src.slice(lt, lt + 80));
    if (!m) { addText('<'); i = lt + 1; continue; }
    let j = lt + m[0].length;
    let q = null;
    while (j < n) {
      const c = src[j];
      if (q) { if (c === q) q = null; } else if (c === '"' || c === "'") q = c; else if (c === '>') break;
      j += 1;
    }
    const raw = src.slice(lt, j + 1);
    i = j + 1;
    const tag = m[1].toLowerCase();
    if (raw[1] === '/') {
      let p = cur;
      while (p && p.tag !== tag) p = p.parent;
      if (p && p.parent) cur = p.parent;
      continue;
    }
    if (SELF_NEST.has(tag) && cur.tag === tag && cur.parent) cur = cur.parent;
    const selfClose = raw.endsWith('/>');
    const node = { tag, attrs: parseAttrs(raw.slice(m[0].length, selfClose ? -2 : -1)), children: [], parent: cur, depth: cur.depth + 1 };
    cur.children.push(node);
    if (VOID.has(tag) || selfClose) continue;
    if (RAW.has(tag)) {
      const e = lower.indexOf(`</${tag}`, i);
      const body = e < 0 ? src.slice(i) : src.slice(i, e);
      node.children.push({ text: tag === 'title' || tag === 'textarea' ? decode(body) : body });
      if (e < 0) { i = n; } else { const g = src.indexOf('>', e); i = g < 0 ? n : g + 1; }
      continue;
    }
    if (node.depth < MAX_DEPTH) cur = node;
  }
  return root;
}

export const isEl = (x) => x && typeof x.tag === 'string';
const hidden = (node) => 'hidden' in node.attrs || /display\s*:\s*none/i.test(node.attrs.style || '') || node.attrs['aria-hidden'] === 'true' && node.tag !== 'svg';

export function walk(node, fn) {
  for (const c of node.children || []) {
    if (!isEl(c)) continue;
    if (fn(c) === false) continue;
    walk(c, fn);
  }
}
export function find(node, test) {
  const out = [];
  walk(node, (c) => { if (test(c)) out.push(c); });
  return out;
}
export const byTag = (node, ...tags) => find(node, (c) => tags.includes(c.tag));

// 사람이 읽는 글자만 이어 붙인다. 스크립트, 스타일, 숨긴 요소는 건너뛴다.
export function textOf(node) {
  if (!isEl(node)) return node && node.text ? node.text : '';
  if (SKIP_TEXT.has(node.tag) || hidden(node)) return '';
  let out = '';
  for (const c of node.children) out += isEl(c) ? ` ${textOf(c)} ` : c.text;
  return out.replace(/\s+/g, ' ').trim();
}
export const rawText = (node) => (node.children || []).map((c) => (isEl(c) ? '' : c.text)).join('');

const BLOCK = new Set(['p', 'div', 'section', 'article', 'header', 'footer', 'main', 'nav', 'aside', 'li', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table', 'tr', 'td', 'th', 'blockquote', 'figure', 'figcaption', 'details', 'summary', 'form', 'br', 'hr', 'dl', 'dt', 'dd', 'button', 'label', 'option', 'pre', 'address', 'body']);
// 줄 단위 글자. 블록 요소에서 줄을 끊는다.
export function textLines(node) {
  const lines = [];
  let buf = '';
  const flush = () => { const t = buf.replace(/\s+/g, ' ').trim(); if (t) lines.push(t); buf = ''; };
  const go = (x) => {
    if (!isEl(x)) { buf += x.text; return; }
    if (SKIP_TEXT.has(x.tag) || hidden(x)) return;
    const block = BLOCK.has(x.tag);
    if (block) flush();
    for (const c of x.children) go(c);
    if (block) flush();
  };
  go(node);
  flush();
  return lines;
}
