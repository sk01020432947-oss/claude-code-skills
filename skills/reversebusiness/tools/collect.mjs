#!/usr/bin/env node
// 가벼운 수집기: 공개 페이지 몇 장을 한 번씩 받아 report.json 초안을 만든다. 의존성 없음, Node 18 이상.
//
// 사용:
//   node collect.mjs <주소> [--out <폴더>] [--pages 5] [--own] [--no-render] [--light]
//
// 지키는 것:
//   - robots.txt 를 가장 먼저 받는다. 금지된 주소는 받지 않고 멈춘다.
//   - 첫 페이지 한 장 + 그 페이지에 걸린 가격, 약관, 환불 링크까지 최대 5장.
//   - 요청과 요청 사이 2초 이상 (robots.txt 의 Crawl-delay 가 더 길면 그 값).
//   - GET 만 한다. 로그인, 가입, 결제, 폼 제출을 하지 않는다. 로그인이나 결제로 가는 링크는 열지 않는다.
//   - 쿠키와 토큰을 저장하지도 보내지도 않는다.
//   - 받은 HTML 에 글이 얇으면(스크립트로 그리는 페이지), 이 컴퓨터의 Chrome 계열 브라우저를 임시 프로필로 잠깐 띄워
//     그려진 화면을 한 번 읽는다 (render.mjs). 같은 한도 안에서만, 누르기와 입력 없이. --no-render 로 끈다.
//   - 정밀 모드: REA(별개의 도구)가 있으면 세 깊이로 읽는다. --light 로 끈다.
//       겉 읽기   그려진 화면의 글과 구조 (REA inspect-web-page)
//       흐름 읽기 펼치기만 누르고(자주 묻는 질문, 탭, 더 보기), 페이지가 요청을 보내려던 호스트 이름만 모은다
//       속 읽기   이미 내려온 스크립트에서 화면 경로 이름, 결제 모듈 이름, 가격처럼 보이는 글자를 찾는다 (REA analyze-web-bundle).
//                 약관이 코드 분석을 금지하거나 약관을 읽지 못했으면 하지 않는다 (내 것이면 한다). 찾은 주소는 부르지 않는다.
//   - 누가 읽는지 숨기지 않는다 (User-Agent 에 이름과 저장소 주소).
//   - 401, 403, 429 나 봇 확인 화면을 만나면 넘지 않고 멈춘다.
// 채울 수 있는 것만 관찰로 적고, 나머지는 모름으로 둔다. 해석(고객, 문제, 내 버전)은 하지 않는다.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseHtml, walk, find, byTag, textOf, rawText, textLines, isEl } from './html-lite.mjs';
import { scrub, cleanUrl, PRICE, recordsOf, readInspect, dropSecrets } from './from-rea.mjs';
import { reaRunner, runRea } from './rea-bridge.mjs';
import { classifyHosts, scanScripts, readBundleFacts, termsForbidCodeReading, looksBehindLogin, SERVICE_KINDS } from './deep.mjs';
import { findBrowser, openRenderer, isTracker } from './render.mjs';
import { KIND_NAME } from './kinds.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const REPO_URL = 'https://github.com/wonseokjung/reversebusiness';
export const LIMITS = { maxPages: 5, delayMs: 2000, maxDelayMs: 60000, timeoutMs: 15000, maxBytes: 2_000_000, maxRequests: 14, maxRedirects: 3, renderBudgetMs: 75000, reaInspectMs: 60000, reaBundleMs: 150000, flowClicks: 8 };
// 받은 HTML 의 글이 이보다 적으면 얇다고 본다.
export const THIN_CHARS = 1500;
export const userAgent = (version = '0') => `rebiz/${version} (+${REPO_URL}; reads a few public pages, 2s apart, no login)`;

export class Stop extends Error {
  constructor(code, message, detail = {}) { super(message); this.code = code; this.detail = detail; }
}

// ---------- robots.txt (RFC 9309) ----------
export function parseRobots(text) {
  const groups = [];
  let cur = null;
  let lastAgent = false;
  for (const raw of String(text).split(/\r?\n/)) {
    const line = raw.replace(/#.*$/, '').trim();
    const i = line.indexOf(':');
    if (!line || i < 0) continue;
    const k = line.slice(0, i).trim().toLowerCase();
    const v = line.slice(i + 1).trim();
    if (k === 'user-agent') {
      if (!cur || !lastAgent) { cur = { agents: [], rules: [], delay: null }; groups.push(cur); }
      cur.agents.push(v.toLowerCase());
      lastAgent = true;
      continue;
    }
    lastAgent = false;
    if (!cur) continue;
    if (k === 'allow' || k === 'disallow') cur.rules.push({ allow: k === 'allow', path: v });
    else if (k === 'crawl-delay') { const s = Number(v); if (s >= 0) cur.delay = s; }
  }
  return groups;
}
// 내 이름(rebiz)을 부른 묶음이 있으면 그것만, 없으면 * 묶음을 따른다.
export function rulesFor(groups, token = 'rebiz') {
  let mine = groups.filter((g) => g.agents.includes(token));
  if (!mine.length) mine = groups.filter((g) => g.agents.includes('*'));
  const delays = mine.map((g) => g.delay).filter((d) => d != null);
  return { rules: mine.flatMap((g) => g.rules), delay: delays.length ? Math.max(...delays) : null, named: mine.some((g) => g.agents.includes(token)) };
}
function matchLen(pattern, p) {
  const end = pattern.endsWith('$');
  const pat = end ? pattern.slice(0, -1) : pattern;
  const re = new RegExp(`^${pat.split('*').map((s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('.*')}${end ? '$' : ''}`);
  return re.test(p) ? pattern.length : -1;
}
// 같은 주소를 다르게 적은 것(%70 과 p, %2f 와 %2F)을 한 모양으로 맞춘다.
const normPath = (p) => String(p).replace(/%([0-9a-fA-F]{2})/g, (m, h) => {
  const ch = String.fromCharCode(parseInt(h, 16));
  return /[A-Za-z0-9\-._~]/.test(ch) ? ch : `%${h.toUpperCase()}`;
});
// 가장 길게 맞는 규칙을 따르고, 길이가 같으면 허용이 이긴다.
export function isAllowed(rules, pathAndQuery) {
  let best = null;
  const target = normPath(pathAndQuery);
  for (const r of rules) {
    if (!r.path) continue;
    const len = matchLen(normPath(r.path), target);
    if (len < 0) continue;
    if (!best || len > best.len || (len === best.len && r.allow)) best = { len, allow: r.allow };
  }
  return best ? best.allow : true;
}

// ---------- 받기 ----------
const realSleep = (ms) => new Promise((r) => setTimeout(r, ms));
const BLOCK_STATUS = new Set([401, 403, 407, 429, 451]);
const HARD_STOP = new Set(['blocked', 'challenge', 'request-limit', 'timeout', 'network', 'robots-blocked', 'robots-unreachable', 'crawl-delay-too-long']);
const CHALLENGE = /(just a moment\.\.\.|attention required|verify you are (a )?human|are you a robot|captcha|cf-chl-|challenge-platform|access denied|보안 문자|자동 접속|로봇이 아닙니다)/i;
// 열지 않는 링크: 로그인, 가입, 결제, 계정, 관리. 주소의 마디 단위로 본다.
const NEVER_SEG = /^(log-?in|sign-?in|sign-?up|register|join|auth|oauth|sso|accounts?|my-?page|cart|basket|checkout|orders?|payments?|pay|billing|admin|dashboard|logout|password)$/i;
const NEVER_KO = /(로그인|회원가입|결제|장바구니|주문)/;
export function neverOpen(pathname) {
  let p = String(pathname || '');
  try { p = decodeURIComponent(p); } catch { /* 그대로 본다 */ }
  return NEVER_KO.test(p) || p.split('/').filter(Boolean).some((seg) => NEVER_SEG.test(seg.replace(/\.[a-z0-9]+$/i, '')));
}
const LINK_KINDS = [
  { kind: 'pricing', re: /(pricing|prices?\b|plans?\b|요금|가격|멤버십|membership|이용권)/i },
  { kind: 'terms', re: /(terms|\btos\b|conditions|이용\s?약관|서비스\s?약관|약관)/i },
  { kind: 'refund', re: /(refund|환불|취소\s?정책|cancellation)/i },
];

// 약관 링크로 보고 연 페이지가 정말 약관인지 본다: 주소나 제목이 약관을 가리키거나, 본문에 약관에서 쓰는 말이 여럿 있어야 한다.
// 약관이 아닌 글을 약관으로 읽으면 "금지하는 말이 없다"고 잘못 판단해 속 읽기를 하게 되므로 엄격하게 본다.
const TERMS_WHERE = /(terms|\btos\b|legal|conditions|agreement|약관)/i;
const TERMS_WORDS = [/terms of (service|use)|terms and conditions|이용\s?약관|서비스\s?약관/i, /liabilit|면책|책임을 지지/i, /governing law|jurisdiction|준거법|관할/i, /terminat|계약의? 해지|이용 계약/i, /warrant|보증하지/i, /intellectual property|지식재산|저작권/i, /you agree|동의한 것으로|동의합니다/i];
export function looksLikeTerms(pg) {
  let where = String((pg && pg.title) || '');
  try { where += ` ${decodeURIComponent(new URL(pg.url).pathname)}`; } catch { /* 주소를 못 읽으면 제목만 본다 */ }
  const text = ((pg && pg.lines) || []).join(' ');
  return TERMS_WHERE.test(where) || TERMS_WORDS.filter((re) => re.test(text)).length >= 4;
}

export function createFetcher({ version = '0', fetchImpl = globalThis.fetch, sleep = realSleep, now = () => Date.now(), limits = {} } = {}) {
  const L = { ...LIMITS, ...limits };
  const log = [];
  let lastEnd = null;
  let delayMs = L.delayMs;
  const ua = userAgent(version);
  async function get(url, { accept = 'text/html,application/xhtml+xml;q=0.9,text/plain;q=0.5', kind = 'page' } = {}) {
    if (log.length >= L.maxRequests) throw new Stop('request-limit', `요청 한도(${L.maxRequests}번)에 닿아 멈췄어요.`);
    if (lastEnd != null) {
      const wait = lastEnd + delayMs - now();
      if (wait > 0) await sleep(wait);
    }
    const started = now();
    const ctl = new AbortController();
    const timer = setTimeout(() => ctl.abort(), L.timeoutMs);
    const entry = { n: log.length + 1, kind, method: 'GET', url: cleanUrl(url), started_at: new Date(started).toISOString(), status: 0, bytes: 0 };
    log.push(entry);
    try {
      // 쿠키, 인증 머리말을 보내지 않는다. 넘겨받은 쿠키도 저장하지 않는다.
      const res = await fetchImpl(url, { method: 'GET', redirect: 'manual', credentials: 'omit', signal: ctl.signal, headers: { 'user-agent': ua, accept, 'accept-language': 'ko,en;q=0.8' } });
      entry.status = res.status;
      const type = res.headers.get('content-type') || '';
      const location = res.headers.get('location') || '';
      let buf = Buffer.alloc(0);
      let truncated = false;
      if (res.body && res.status >= 200 && res.status < 300) {
        const reader = res.body.getReader();
        for (;;) {
          const { done, value } = await reader.read();
          if (done) break;
          buf = Buffer.concat([buf, Buffer.from(value)]);
          if (buf.length > L.maxBytes) { truncated = true; try { await reader.cancel(); } catch { /* 이미 닫힘 */ } break; }
        }
      } else if (res.body) { try { await res.body.cancel(); } catch { /* 닫힘 */ } }
      entry.bytes = buf.length;
      const charset = (/charset=([^;\s]+)/i.exec(type) || [])[1] || (/<meta[^>]+charset=["']?([\w-]+)/i.exec(buf.subarray(0, 2048).toString('latin1')) || [])[1] || 'utf-8';
      let body;
      try { body = new TextDecoder(charset.toLowerCase()).decode(buf); } catch { body = buf.toString('utf8'); }
      const headers = {};
      for (const k of ['server', 'x-powered-by', 'via', 'content-type', 'x-robots-tag', 'x-generator']) { const v = res.headers.get(k); if (v) headers[k] = scrub(v).slice(0, 120); }
      return { url, status: res.status, type, location, body, truncated, headers };
    } catch (e) {
      entry.error = e && e.name === 'AbortError' ? 'timeout' : 'network';
      throw new Stop(entry.error, entry.error === 'timeout' ? `응답이 ${L.timeoutMs / 1000}초 안에 오지 않아 멈췄어요: ${cleanUrl(url)}` : `연결하지 못했어요: ${cleanUrl(url)}`);
    } finally {
      clearTimeout(timer);
      lastEnd = now();
    }
  }
  // 브라우저로 그려 읽는 한 번도 요청 한 번으로 치고, 같은 간격을 지킨다.
  async function paced(kind, url, run) {
    if (log.length >= L.maxRequests) throw new Stop('request-limit', `요청 한도(${L.maxRequests}번)에 닿아 멈췄어요.`);
    if (lastEnd != null) {
      const wait = lastEnd + delayMs - now();
      if (wait > 0) await sleep(wait);
    }
    const entry = { n: log.length + 1, kind, method: 'GET', url: cleanUrl(url), started_at: new Date(now()).toISOString(), status: 0, bytes: 0 };
    log.push(entry);
    try { return await run(entry); } finally { lastEnd = now(); }
  }
  return { get, paced, log, ua, limits: L, setDelay: (ms) => { delayMs = Math.min(Math.max(ms, L.delayMs), L.maxDelayMs); }, delay: () => delayMs };
}

export function normalizeUrl(input) {
  let s = String(input || '').trim();
  if (!s) throw new Stop('bad-url', '주소가 비었어요.');
  if (!/^[a-z][a-z0-9+.-]*:\/\//i.test(s)) s = `https://${s}`;
  let u;
  try { u = new URL(s); } catch { throw new Stop('bad-url', `주소로 읽을 수 없어요: ${input}`); }
  if (!/^https?:$/.test(u.protocol)) throw new Stop('bad-url', 'http 나 https 주소만 읽어요.');
  if (u.username || u.password) throw new Stop('bad-url', '아이디나 비밀번호가 들어 있는 주소는 읽지 않아요.');
  u.hash = '';
  return u;
}
const sameSite = (a, b) => a.hostname.replace(/^www\./, '') === b.hostname.replace(/^www\./, '');

// ---------- 한 장 읽기 ----------
const SIGNUP = /(회원\s?가입|가입하기|무료\s?가입|무료로\s?시작|sign\s?up|register|create\s+(an\s+)?account|get\s+started|start\s+free|try\s+(it\s+)?free)/i;
const PAY = /(수강\s?신청|구매|결제|구독|신청하기|주문|buy|checkout|subscribe|purchase|order\s+now|enroll|upgrade|get\s+access)/i;
const LOGIN = /(로그인|log\s?in|sign\s?in|내\s?강의실|마이\s?페이지|my\s?account|dashboard)/i;
const RETURN_HINT = /(뉴스레터|newsletter|소식\s?받기|커뮤니티|community|discord|디스코드|카카오\s?채널|오픈\s?채팅|알림\s?받기|rss|블로그|blog|유튜브|youtube|instagram|인스타)/i;
const short = (s, n = 40) => { const t = scrub(s); return t.length > n ? `${t.slice(0, n - 1)}…` : t; };
const uniq = (a) => [...new Set(a)];
const q = (s, n = 40) => `"${short(s, n)}"`;

const TECH_HINTS = [
  [/\/_next\/|__NEXT_DATA__/i, 'Next.js'],
  [/\/_nuxt\/|__NUXT__/i, 'Nuxt'],
  [/\/static\/js\/main\.[0-9a-f]+\.js/i, 'React 계열 묶음(해시 붙은 main 파일)'],
  [/\/assets\/index-[\w-]+\.js/i, 'Vite 계열 묶음(해시 붙은 index 파일)'],
  [/wp-content|wp-includes/i, 'WordPress'],
  [/cdn\.shopify\.com|shopify/i, 'Shopify'],
  [/static\.wixstatic\.com|wix\.com/i, 'Wix'],
  [/webflow/i, 'Webflow'],
  [/framerusercontent|framer\.com/i, 'Framer'],
  [/imweb/i, '아임웹'],
  [/cafe24/i, '카페24'],
  [/googletagmanager\.com|gtag\/js|google-analytics/i, 'Google 태그'],
  [/js\.stripe\.com/i, 'Stripe'],
  [/paypal\.com\/sdk|paypalobjects/i, 'PayPal'],
  [/tosspayments/i, '토스페이먼츠'],
  [/portone|iamport/i, '포트원'],
  [/polar\.sh/i, 'Polar'],
  [/lemonsqueezy/i, 'Lemon Squeezy'],
  [/channel\.io|channelio/i, '채널톡'],
  [/firebase/i, 'Firebase'],
  [/supabase/i, 'Supabase'],
];

export function readPage(html, pageUrl, { rects = null } = {}) {
  const root = parseHtml(html);
  const head = byTag(root, 'head')[0] || root;
  const body = byTag(root, 'body')[0] || root;
  const htmlEl = byTag(root, 'html')[0];
  const metas = {};
  for (const m of byTag(root, 'meta')) {
    const k = (m.attrs.property || m.attrs.name || '').toLowerCase();
    if (k && m.attrs.content && !/verification|token|csrf|nonce/i.test(k)) metas[k] = scrub(m.attrs.content);
  }
  const title = scrub(rawText(byTag(head, 'title')[0] || { children: [] }));
  const lines = uniq(textLines(body).map(scrub).filter((l) => l.length >= 2));
  const visible = lines.join(' ');
  const headings = find(body, (c) => /^h[1-3]$/.test(c.tag)).map((h) => ({ level: Number(h.tag[1]), text: scrub(textOf(h)) })).filter((h) => h.text);
  const base = new URL(pageUrl);
  const links = [];
  for (const a of byTag(body, 'a')) {
    const text = scrub(textOf(a) || a.attrs['aria-label'] || a.attrs.title || '');
    const href = a.attrs.href || '';
    let abs = null;
    if (href && !/^(#|javascript:|mailto:|tel:|data:)/i.test(href)) { try { abs = new URL(href, base); abs.hash = ''; } catch { abs = null; } }
    links.push({ text, href: abs ? abs.href : '', same: !!abs && sameSite(abs, base) && /^https?:$/.test(abs.protocol), path: abs ? abs.pathname : '' });
  }
  const buttons = byTag(body, 'button').map((b) => scrub(textOf(b) || b.attrs['aria-label'] || '')).filter(Boolean);
  const actions = [...links.map((l) => l.text), ...buttons].filter(Boolean);
  const hit = (re) => uniq(actions.filter((t) => t.length <= 60 && re.test(t)));
  const NOT_PAY = /(뉴스레터|newsletter|소식)/i;
  const prices = uniq(lines.filter((l) => PRICE.test(l)).map((l) => (PRICE.exec(l) || [])[0]).filter(Boolean)).slice(0, 8);
  const ld = [];
  for (const s of find(root, (c) => c.tag === 'script' && /ld\+json/i.test(c.attrs.type || ''))) {
    try {
      const each = (o) => {
        if (Array.isArray(o)) return o.forEach(each);
        if (!o || typeof o !== 'object') return;
        if (o['@graph']) each(o['@graph']);
        if (o['@type']) {
          const offers = [].concat(o.offers || []).filter((x) => x && typeof x === 'object' && x.price != null).map((x) => ({ price: scrub(x.price), currency: scrub(x.priceCurrency || '') }));
          ld.push({ type: [].concat(o['@type']).join(', '), offers });
        }
      };
      each(JSON.parse(rawText(s)));
    } catch { /* 깨진 JSON-LD 는 건너뛴다 */ }
  }
  const scripts = byTag(root, 'script').map((s) => s.attrs.src || '').filter(Boolean);
  const scriptHosts = uniq(scripts.map((s) => { try { return new URL(s, base).hostname; } catch { return ''; } }).filter(Boolean));
  const markers = `${scripts.join(' ')} ${byTag(root, 'link').map((l) => l.attrs.href || '').join(' ')} ${metas.generator || ''} ${find(root, (c) => c.tag === 'script' && c.attrs.id).map((c) => c.attrs.id).join(' ')}`;
  const tech = uniq(TECH_HINTS.filter(([re]) => re.test(markers)).map(([, name]) => name));
  const forms = byTag(body, 'form');
  const assets = uniq([
    ...byTag(body, 'img').map((x) => x.attrs.src || ''), ...byTag(body, 'video').map((x) => x.attrs.poster || x.attrs.src || ''), ...byTag(body, 'source').map((x) => x.attrs.src || ''),
    ...byTag(root, 'link').filter((l) => /icon|preload|image/i.test(l.attrs.rel || '')).map((l) => l.attrs.href || ''), metas['og:image'] || '',
  ].filter((u) => u && !u.startsWith('data:')).map((u) => { try { return cleanUrl(new URL(u, base).href); } catch { return ''; } }).filter((u) => /\.(png|jpe?g|webp|gif|svg|ico|avif|mp4|webm|mov|woff2?|ttf|otf)$/i.test(u)));
  return {
    url: cleanUrl(pageUrl), title, lang: htmlEl ? htmlEl.attrs.lang || '' : '', metas, lines, textLength: visible.length, headings, links, buttons,
    signup: hit(SIGNUP), pay: hit(PAY).filter((t) => !NOT_PAY.test(t)), login: hit(LOGIN), back: hit(RETURN_HINT).filter((t) => t.length <= 20), prices, ld,
    counts: { img: byTag(body, 'img').length, video: byTag(body, 'video').length, iframe: byTag(body, 'iframe').length, form: forms.length, password: find(body, (c) => c.tag === 'input' && (c.attrs.type || '').toLowerCase() === 'password').length, script: scripts.length, scriptTags: byTag(root, 'script').filter((x) => !/json/i.test(x.attrs.type || '')).length, links: links.length, buttons: buttons.length },
    scriptHosts, tech, generator: metas.generator || '', assets, challenge: CHALLENGE.test(`${title} ${visible.slice(0, 600)}`) && visible.length < 1500,
    skeleton: rects && rects.length >= 2 ? skeletonFromRects(root, rects) : buildSkeleton(body),
    measured: !!(rects && rects.length >= 2),
  };
}

// ---------- 뼈대: 페이지의 구역을 위에서 아래로 ----------
const NOISE = new Set(['script', 'style', 'link', 'meta', 'noscript', 'template', 'br', 'hr', 'head', 'title', 'base']);
const BOX = new Set(['div', 'section', 'article', 'main', 'header', 'footer', 'nav', 'aside']);
const count = (node, ...tags) => byTag(node, ...tags).length + (tags.includes(node.tag) ? 1 : 0);
function weightOf(node) {
  const t = textOf(node).length;
  const media = count(node, 'video', 'iframe') * 900 + count(node, 'img', 'picture', 'svg', 'canvas') * 220;
  return t * 1.4 + media + count(node, 'h1', 'h2', 'h3') * 90 + count(node, 'li', 'details') * 30 + count(node, 'a', 'button') * 14;
}
const meaningful = (node) => node.children.filter((c) => isEl(c) && !NOISE.has(c.tag) && !('hidden' in c.attrs) && weightOf(c) >= 40);
function kindOf(node) {
  const text = textOf(node);
  const tag = node.tag;
  const role = (node.attrs.role || '').toLowerCase();
  const acts = [...byTag(node, 'a', 'button').map((x) => textOf(x))];
  if (tag === 'footer' || role === 'contentinfo') return 'footer';
  if (PRICE.test(text) && text.length < 2500) return 'price';
  if (count(node, 'details', 'summary') >= 2 || /(faq|자주\s?묻는|궁금한|questions)/i.test(text.slice(0, 300))) return 'faq';
  if (count(node, 'blockquote') >= 1 || /(후기|리뷰|reviews?|testimonials?|what (people|customers) say)/i.test(text.slice(0, 300))) return 'quotes';
  if (tag === 'nav' || role === 'navigation' || (acts.length >= 3 && text.length < 220 && !count(node, 'h1'))) return 'nav';
  if (count(node, 'video', 'iframe') >= 1 && text.length < 500) return 'media';
  if (count(node, 'h1') >= 1) return 'headline';
  const nums = textLines(node).filter((l) => /^[\d,.+%\s]{1,9}[A-Za-z가-힣+%]{0,3}$/.test(l)).length;
  if (nums >= 3 && text.length < 900) return 'numbers';
  if (acts.some((a) => PAY.test(a) || SIGNUP.test(a)) && text.length < 320) return 'cta';
  if (count(node, 'li') >= 4 || count(node, 'h2', 'h3', 'h4') >= 3) return 'list';
  if (count(node, 'img', 'picture') >= 1 && text.length < 160) return 'media';
  return 'text';
}
export function buildSkeleton(body) {
  let list = meaningful(body);
  for (let step = 0; step < 10; step += 1) {
    if (list.length === 1) { const kids = meaningful(list[0]); if (kids.length >= 1 && kids[0] !== list[0]) { list = kids; continue; } break; }
    if (!list.length || list.length >= 12) break;
    const total = list.reduce((s, x) => s + weightOf(x), 0) || 1;
    const big = list.map((x, i) => ({ x, i, w: weightOf(x) })).sort((a, b) => b.w - a.w)[0];
    const kids = meaningful(big.x);
    // 안에 다시 구역(통)이 둘 이상 들어 있을 때만 펼친다. 제목, 문단, 그림 같은 낱개로는 쪼개지 않는다.
    const boxes = kids.filter((k) => BOX.has(k.tag)).length;
    if (big.w / total < 0.42 || kids.length < 2 || boxes < 2 || big.x.tag === 'footer' || big.x.tag === 'nav') break;
    list = [...list.slice(0, big.i), ...kids, ...list.slice(big.i + 1)];
  }
  return labelBlocks(list.slice(0, 16).map((node) => ({ kind: kindOf(node), weight: Math.round(Math.min(Math.max(weightOf(node), 120), 2600)), back: RETURN_HINT.test(textOf(node)) || LOGIN.test(textOf(node)) })));
}
// 구역마다 내 말로 이름을 붙이고, 하는 일로 층을 추정한다.
function labelBlocks(blocks) {
  const firstPay = blocks.findIndex((b) => b.kind === 'price' || b.kind === 'cta');
  const seen = {};
  return blocks.map((b, i) => {
    let role = 'value';
    if (['price', 'cta', 'faq', 'quotes'].includes(b.kind)) role = 'pay';
    else if (b.kind === 'footer') role = b.back ? 'return' : 'other';
    else if (b.kind === 'nav') role = 'other';
    else if ((b.kind === 'media' || b.kind === 'headline') && (firstPay < 0 ? i <= 1 : i <= firstPay)) role = 'attract';
    seen[b.kind] = (seen[b.kind] || 0) + 1;
    return { name: `${KIND_NAME[b.kind]}${seen[b.kind] > 1 ? ` ${seen[b.kind]}` : ''}`, role, weight: b.weight, kind: b.kind, status: 'inferred' };
  });
}
// 브라우저가 그린 화면에서 잰 구역(위치와 높이)으로 뼈대를 만든다. 길이는 실제로 잰 값이다.
export function skeletonFromRects(root, rects) {
  const nodes = new Map();
  for (const n of find(root, (c) => 'data-rebiz-b' in c.attrs)) nodes.set(String(n.attrs['data-rebiz-b']), n);
  const blocks = [];
  for (const r of [...rects].sort((a, b) => a.top - b.top)) {
    const node = nodes.get(String(r.i));
    if (!node || !(r.height > 0)) continue;
    const text = textOf(node);
    blocks.push({ kind: kindOf(node), weight: Math.round(r.height), back: RETURN_HINT.test(text) || LOGIN.test(text) });
  }
  return labelBlocks(blocks);
}

// ---------- 모으기 ----------
export async function collect(input, { version = '0', maxPages = LIMITS.maxPages, fetchImpl, sleep, now, limits, onStep = () => {}, render = 'auto', browser, mode = 'auto', rea, relation = 'third-party', evidenceDir = '', externalRequests = 'allow', headless } = {}) {
  const start = normalizeUrl(input);
  const f = createFetcher({ version, fetchImpl, sleep, now, limits });
  const pagesMax = Math.min(Math.max(1, maxPages), LIMITS.maxPages);
  const result = { start: cleanUrl(start.href), origin: start.origin, robots: null, pages: [], skipped: [], stop: null, log: f.log, ua: f.ua, delayMs: f.delay(), pagesMax, render: { mode: render === 'off' ? 'off' : 'not-needed', browser: '', pages: 0, allowed: 0, blocked: 0, why: {} }, deep: { mode: 'light', why: '', surface: { state: 'done', note: '' }, flow: { state: 'skipped', note: '' }, code: { state: 'skipped', note: '' } } };
  const robotsCache = new Map();

  async function robotsOf(origin) {
    if (robotsCache.has(origin)) return robotsCache.get(origin);
    onStep(`robots.txt 확인: ${origin}/robots.txt`);
    let res = await f.get(`${origin}/robots.txt`, { accept: 'text/plain,*/*;q=0.5', kind: 'robots' });
    for (let hop = 0; hop < 3 && res.status >= 300 && res.status < 400 && res.location; hop += 1) {
      let next;
      try { next = new URL(res.location, res.url); } catch { break; }
      // robots.txt 가 다른 사이트나 로그인 주소로 넘기면 따라가지 않는다.
      if (!/^https?:$/.test(next.protocol) || !sameSite(next, new URL(origin)) || neverOpen(next.pathname)) throw new Stop('robots-unreachable', 'robots.txt 가 다른 곳으로 넘겨져서 허용 여부를 알 수 없어요. 멈춥니다.', { to: next.hostname });
      res = await f.get(next.href, { accept: 'text/plain,*/*;q=0.5', kind: 'robots' });
    }
    if (res.status >= 300 && res.status < 400) throw new Stop('robots-unreachable', 'robots.txt 가 계속 다른 주소로 넘겨져서 허용 여부를 알 수 없어요. 멈춥니다.', { status: res.status });
    if (res.status >= 200 && res.status < 300 && CHALLENGE.test(res.body.slice(0, 4000)) && res.body.length < 60000) throw new Stop('challenge', 'robots.txt 자리에 사람인지 확인하는 화면이 나왔어요. 풀지 않고 멈춥니다.');
    let info;
    if (res.status >= 200 && res.status < 300 && !/text\/html/i.test(res.type)) {
      const r = rulesFor(parseRobots(res.body));
      info = { status: res.status, found: true, rules: r.rules, delay: r.delay, named: r.named, allow: uniq(r.rules.filter((x) => x.allow && x.path).map((x) => x.path)), disallow: uniq(r.rules.filter((x) => !x.allow && x.path).map((x) => x.path)) };
      if (r.delay != null && r.delay * 1000 > f.limits.maxDelayMs) throw new Stop('crawl-delay-too-long', `robots.txt 가 요청 사이 ${r.delay}초를 요구해요. 이 도구의 한도(${f.limits.maxDelayMs / 1000}초)보다 길어서 멈춥니다.`, { delay: r.delay });
      if (r.delay != null) f.setDelay(r.delay * 1000);
    } else if (BLOCK_STATUS.has(res.status)) {
      throw new Stop('robots-blocked', `robots.txt 가 ${res.status} 로 막혀 있어요. 접근 제한으로 보고 멈춥니다.`, { status: res.status });
    } else if (res.status >= 500) {
      throw new Stop('robots-unreachable', `robots.txt 를 받지 못했어요 (${res.status}). 허용 여부를 알 수 없어 멈춥니다.`, { status: res.status });
    } else {
      // 404 같은 4xx, 또는 robots.txt 자리에 HTML 이 오는 경우: 규칙 없음으로 본다 (RFC 9309).
      info = { status: res.status, found: false, rules: [], delay: null, named: false, allow: [], disallow: [] };
    }
    robotsCache.set(origin, info);
    if (!result.robots) result.robots = { url: `${origin}/robots.txt`, ...info, rules: undefined };
    return info;
  }

  async function page(u, kind) {
    let cur = u;
    for (let hop = 0; hop <= f.limits.maxRedirects; hop += 1) {
      if (neverOpen(cur.pathname)) throw new Stop('login-wall', `로그인, 가입, 결제, 계정 화면으로 보이는 주소는 열지 않아요: ${short(cur.pathname, 40)}`, { path: cur.pathname });
      const rb = await robotsOf(cur.origin);
      if (!isAllowed(rb.rules, cur.pathname + cur.search)) throw new Stop('robots-disallow', `robots.txt 가 이 주소를 막고 있어요: ${cur.pathname}. 받지 않고 멈춥니다.`, { path: cur.pathname });
      onStep(`읽기: ${cleanUrl(cur.href)}`);
      const res = await f.get(cur.href, { kind });
      if (res.status >= 300 && res.status < 400 && res.location) {
        let next;
        try { next = new URL(res.location, cur); } catch { throw new Stop('bad-redirect', '이동할 주소를 읽을 수 없어 멈췄어요.'); }
        next.hash = '';
        if (!/^https?:$/.test(next.protocol) || !sameSite(next, start)) throw new Stop('offsite-redirect', `다른 사이트(${next.hostname})로 넘기는 주소라 따라가지 않았어요.`, { to: next.hostname });
        if (neverOpen(next.pathname)) throw new Stop('login-wall', '로그인이나 가입 화면으로 넘기는 주소예요. 넘지 않고 멈춥니다.', { to: next.pathname });
        cur = next;
        continue;
      }
      if (BLOCK_STATUS.has(res.status)) throw new Stop('blocked', `이 주소는 ${res.status} 로 막혀 있어요. 넘지 않고 멈춥니다.`, { status: res.status });
      if (res.status < 200 || res.status >= 300) throw new Stop('http-error', `페이지를 받지 못했어요 (${res.status}).`, { status: res.status });
      if (!/html|xml/i.test(res.type) && !/^\s*</.test(res.body)) throw new Stop('not-html', `HTML 이 아니에요 (${short(res.type, 40) || '종류 모름'}).`);
      let p;
      try { p = readPage(res.body, cur.href); } catch { throw new Stop('parse-error', '이 페이지의 HTML 을 읽지 못했어요.'); }
      if (p.challenge) throw new Stop('challenge', '사람인지 확인하는 화면이 나왔어요. 풀지 않고 멈춥니다.');
      return { ...p, kind, status: res.status, headers: res.headers, truncated: res.truncated };
    }
    throw new Stop('too-many-redirects', '주소가 너무 여러 번 넘어가서 멈췄어요.');
  }

  // 받은 HTML 이 얇은지: 스크립트가 있고 글이 적거나, 가격과 누르는 곳이 하나도 안 보일 때.
  const needsRender = (p) => p.counts.scriptTags > 0 && (p.textLength < THIN_CHARS || (!p.prices.length && !p.pay.length && !p.signup.length && p.textLength < THIN_CHARS * 2));
  let renderer = null;
  let mainTab = null;
  const renderStarted = (now || Date.now)();
  // 브라우저 안에서 나가는 요청마다 같은 선을 적용한다.
  async function allowInBrowser(reqUrl, { isMain }) {
    let u;
    try { u = new URL(reqUrl); } catch { return { ok: false, why: '읽을 수 없는 주소' }; }
    if (isMain) {
      if (!sameSite(u, start)) return { ok: false, why: '다른 사이트로 넘어가기' };
      if (neverOpen(u.pathname)) return { ok: false, why: '로그인이나 결제 주소' };
    }
    if (sameSite(u, start)) {
      const rb = robotsCache.get(u.origin) || robotsCache.get(start.origin);
      if (rb && !isAllowed(rb.rules, u.pathname + u.search)) return { ok: false, why: 'robots.txt 금지' };
      if (!isMain && neverOpen(u.pathname)) return { ok: false, why: '로그인이나 결제 주소' };
      return { ok: true, sameSite: true };
    }
    if (isTracker(u.hostname)) return { ok: false, why: '분석과 광고 도구' };
    // externalRequests 'block': 다른 사이트로는 아무 요청도 보내지 않는다 (호스트 이름만 적는다). 시험에서 바깥으로 나가지 않으려고 쓴다.
    if (externalRequests === 'block') return { ok: false, why: '다른 사이트 자원' };
    return { ok: true };
  }
  // 한 장을 브라우저로 그려 읽는다. 미리 주소와 robots.txt 를 확인하고, 요청 한 번으로 쳐서 간격을 지킨다.
  // keep 을 주면 탭을 닫지 않고 돌려준다 (정밀 모드에서 같은 탭을 흐름 읽기와 속 읽기에 이어 쓴다).
  async function rendered(u, kind, { keep = false } = {}) {
    if (neverOpen(u.pathname)) throw new Stop('login-wall', `로그인, 가입, 결제, 계정 화면으로 보이는 주소는 열지 않아요: ${short(u.pathname, 40)}`, { path: u.pathname });
    const rb = await robotsOf(u.origin);
    if (!isAllowed(rb.rules, u.pathname + u.search)) throw new Stop('robots-disallow', `robots.txt 가 이 주소를 막고 있어요: ${u.pathname}. 받지 않고 멈춥니다.`, { path: u.pathname });
    onStep(`그려서 읽기: ${cleanUrl(u.href)}`);
    return f.paced('render', u.href, async (entry) => {
      let pg;
      try { pg = await renderer.open(u.href, { allow: allowInBrowser, keepScripts: keep }); } catch { throw new Stop('render-failed', '브라우저로 그려 읽지 못했어요.'); }
      let kept = false;
      try {
        const r = await pg.read();
        const st = pg.stats;
        entry.status = pg.status; entry.bytes = Buffer.byteLength(r.html || ''); entry.browser_requests = st.allowed; entry.browser_blocked = st.blocked;
        result.render.allowed += st.allowed; result.render.blocked += st.blocked;
        for (const [k, v] of Object.entries(st.why)) result.render.why[k] = (result.render.why[k] || 0) + v;
        if (BLOCK_STATUS.has(pg.status)) throw new Stop('blocked', `이 주소는 ${pg.status} 로 막혀 있어요. 넘지 않고 멈춥니다.`, { status: pg.status });
        if (st.mainBlocked && !r.html) throw new Stop(st.mainBlocked.includes('로그인') ? 'login-wall' : 'offsite-redirect', `페이지가 다른 곳으로 넘기려 해서 따라가지 않았어요 (${st.mainBlocked}).`);
        let final;
        try { final = new URL(r.url); } catch { final = u; }
        if (!/^https?:$/.test(final.protocol) || !sameSite(final, start)) final = u;
        let p;
        try { p = readPage(r.html, final.href, { rects: r.blocks }); } catch { throw new Stop('parse-error', '그려진 화면을 읽지 못했어요.'); }
        if (p.challenge) throw new Stop('challenge', '사람인지 확인하는 화면이 나왔어요. 풀지 않고 멈춥니다.');
        result.render.pages += 1;
        for (const h of pg.hosts()) hostsSeen.set(h.host, { host: h.host, count: (hostsSeen.get(h.host)?.count || 0) + h.count, sent: (hostsSeen.get(h.host)?.sent || 0) + h.sent });
        const out = { ...p, kind, status: pg.status || 200, headers: {}, truncated: false, rendered: true, browserStats: st, renderTimedOut: pg.timedOut };
        if (keep) { kept = true; Object.defineProperty(out, 'tab', { value: pg, enumerable: false }); }
        return out;
      } finally { if (!kept) await pg.close(); }
    });
  }
  const hostsSeen = new Map();

  // ---------- 정밀 모드: 이미 있는 REA 를 눈으로 쓴다 (깔린 실행 파일, 또는 사용자가 확인하고 설치한 공식 패키지) ----------
  const reaRun = mode === 'light' ? null : rea !== undefined ? rea : reaRunner();
  const saveEvidence = (name, text) => { if (!evidenceDir) return ''; try { fs.mkdirSync(evidenceDir, { recursive: true }); fs.writeFileSync(path.join(evidenceDir, name), text); return `evidence/${name}`; } catch { return ''; } };
  // 겉 읽기: REA 가 같은 탭에 붙어서 글과 구조, 저장소 키 이름을 읽는다. 누르지 않는다.
  async function reaSurface(tab) {
    const d = result.deep.surface;
    if (!renderer.endpoint) { d.note = 'REA 가 붙을 디버깅 주소를 열지 못해 우리 읽기만 썼다'; return; }
    if (tab.hud) await tab.hud('reversebusiness · REA Surface', 'Reading visible DOM & storage keys…');
    onStep('겉 읽기: REA inspect-web-page (그려진 화면의 글, 구조, 저장소 키 이름)');
    const r = await runRea(reaRun, ['inspect-web-page', renderer.endpoint, tab.targetId, '--allowed-origins', start.origin, '--observation-ms', '1000', '--include-accessibility-text', '--include-storage-keys', '--format', 'json'], { timeoutMs: f.limits.reaInspectMs });
    if (r.code !== 0 || r.timedOut) { d.note = r.timedOut ? 'REA 겉 읽기가 시간 한도를 넘어 우리 읽기만 썼다' : 'REA 겉 읽기가 실패해 우리 읽기만 썼다'; d.rea = 'failed'; return; }
    try {
      // 쿠키, 토큰처럼 비밀 값이 실릴 수 있는 칸은 저장하기 전에 버린다.
      const clean = dropSecrets(JSON.parse(r.stdout));
      const rec = recordsOf(clean).find((x) => x.operation === 'inspect_web_page');
      const pg = readInspect(rec);
      d.rea = 'done';
      d.file = saveEvidence('01_inspect_page.json', JSON.stringify(clean));
      d.storage = pg.storage || { local: [], session: [], idb: [], cache: [] };
      d.scripts = pg.scripts.length;
      d.biggestScript = pg.scripts.reduce((m, x) => Math.max(m, x.length || 0), 0);
      d.a11y = { headings: pg.headings.length, buttons: pg.buttons.length, links: pg.links.length, prices: pg.prices.slice(0, 6) };
    } catch { d.note = 'REA 겉 읽기의 결과를 읽지 못해 우리 읽기만 썼다'; d.rea = 'failed'; }
  }
  // 흐름 읽기: 펼치기만 누르고, 펼친 뒤에 새로 보이는 글과 요청이 나가려던 호스트 이름을 모은다.
  async function flowRead(tab, mainPage) {
    const d = result.deep.flow;
    onStep('흐름 읽기: 펼치기만 누릅니다 (자주 묻는 질문, 탭, 더 보기). 폼, 로그인, 결제 단추는 누르지 않습니다');
    try {
      const fl = await tab.flow({ max: f.limits.flowClicks });
      const after = await tab.read();
      let newLines = [];
      try { const p2 = readPage(after.html, mainPage.url); const before = new Set(mainPage.lines); newLines = p2.lines.filter((l) => !before.has(l)); } catch { /* 새 글 없음 */ }
      d.state = 'done';
      d.clicks = fl.clicks; d.kinds = fl.kinds; d.moved = fl.moved;
      d.newChars = newLines.join(' ').length;
      d.newPrices = uniq(newLines.filter((l) => PRICE.test(l)).map((l) => (PRICE.exec(l) || [])[0]).filter(Boolean)).filter((x) => !mainPage.prices.includes(x)).slice(0, 8);
      d.note = fl.clicks ? '' : '펼칠 곳을 찾지 못해 누른 것은 없다';
      for (const h of tab.hosts()) hostsSeen.set(h.host, { host: h.host, count: Math.max(hostsSeen.get(h.host)?.count || 0, h.count), sent: Math.max(hostsSeen.get(h.host)?.sent || 0, h.sent) });
    } catch { d.state = 'failed'; d.note = '흐름 읽기 도중 멈췄다'; }
  }
  // 속 읽기: 약관이 막지 않을 때만. 스크립트는 이미 내려온 것만 읽고, 찾은 주소는 부르지 않는다.
  async function codeRead(tab) {
    const d = result.deep.code;
    const terms = result.pages.find((p) => p.kind === 'terms');
    if (relation !== 'own') {
      if (!terms) { d.note = '이용약관을 읽지 못해 속 읽기(코드 읽기)는 하지 않았다'; return; }
      const t = termsForbidCodeReading(terms.lines.join(' '));
      if (t.forbids) { d.state = 'blocked'; d.note = `이용약관에 코드 분석을 금지하는 말("${t.word}")이 있어 속 읽기는 하지 않았다`; return; }
      d.termsNote = '이용약관에서 코드 분석을 금지하는 말을 찾지 못했다 (낱말로 찾아본 것이며 법률 검토가 아니다)';
    }
    if (tab.hud) await tab.hud('reversebusiness · Code Scan', 'Inspecting downloaded bundle routes & providers…');
    onStep('속 읽기: 이미 내려온 스크립트에서 화면 경로 이름과 결제 모듈 이름을 찾습니다 (찾은 주소는 부르지 않습니다)');
    let scan = { files: 0, bytes: 0, routes: [], endpoints: [], payments: [], prices: [], plans: [] };
    try { scan = scanScripts(await tab.scripts()); } catch { /* 스크립트를 못 읽음 */ }
    let bundle = null;
    if (renderer.endpoint && evidenceDir) {
      onStep('속 읽기: REA analyze-web-bundle (큰 스크립트는 시간 한도에서 멈춥니다)');
      const file = path.join(evidenceDir, '02_bundle_evidence.json');
      try { fs.mkdirSync(evidenceDir, { recursive: true }); fs.rmSync(file, { force: true }); } catch { /* 폴더 문제는 아래에서 실패로 남는다 */ }
      const r = await runRea(reaRun, ['analyze-web-bundle', renderer.endpoint, tab.targetId, '--allowed-origins', start.origin, '--detail', 'summary', '--evidence_output', file, '--view', '{"kind":"web-bundle","collection":"summary"}', '--analysis-timeout-ms', '30000', '--total-analysis-timeout-ms', '100000', '--format', 'json'], { timeoutMs: f.limits.reaBundleMs });
      try {
        const rec = recordsOf(JSON.parse(fs.readFileSync(file, 'utf8'))).find((x) => x.operation === 'analyze_web_bundle');
        if (rec) { bundle = readBundleFacts(rec); d.file = 'evidence/02_bundle_evidence.json'; }
      } catch { /* 결과 파일이 없으면 실패로 남긴다 */ }
      if (!bundle) d.reaNote = r.timedOut ? 'REA 스크립트 분석이 시간 한도를 넘었다' : 'REA 스크립트 분석이 결과를 내지 못했다';
    } else d.reaNote = 'REA 가 붙을 디버깅 주소나 저장할 폴더가 없어 REA 스크립트 분석은 하지 않았다';
    d.rea = bundle ? { scripts: bundle.scripts, parsed: bundle.parsed, status: bundle.status, endpoints: bundle.endpoints } : null;
    d.routes = uniq([...(bundle ? bundle.routes : []), ...scan.routes]).sort();
    d.endpoints = scan.endpoints; d.payments = scan.payments; d.prices = scan.prices; d.plans = scan.plans; d.files = scan.files; d.bytes = scan.bytes;
    if (!bundle && !scan.files) { d.state = 'failed'; d.note = '스크립트를 읽지 못했다'; return; }
    d.state = bundle && bundle.scripts > bundle.parsed ? 'partial' : 'done';
    d.note = bundle && bundle.scripts > bundle.parsed ? `스크립트 ${bundle.scripts}개 가운데 ${bundle.scripts - bundle.parsed}개는 REA 분석이 끝나지 않았다` : (d.reaNote || '');
  }

  try {
    let main = await page(start, 'main');
    result.pages.push(main);
    const found = render === 'off' ? null : browser === undefined ? findBrowser() : browser;
    const precise = !!reaRun && !!found;
    result.deep.why = mode === 'light' ? '가벼운 모드로 실행했다 (--light)' : !reaRun ? 'REA 를 찾지 못해 가벼운 모드로 읽었다' : !found ? (render === 'off' ? '그려 읽기를 꺼 두어 가벼운 모드로 읽었다' : 'Chrome 계열 브라우저가 없어 가벼운 모드로 읽었다') : '';
    if (render !== 'off' && (render === 'force' || precise || needsRender(main))) {
      if (!found) result.render.mode = 'unavailable';
      else {
        try {
          onStep(precise ? `정밀 모드: REA 를 찾았습니다. ${found.name} 을(를) 임시 프로필로 잠깐 띄워 세 깊이로 읽습니다.` : `받은 HTML 의 글이 ${main.textLength}자로 얇아요. ${found.name} 을(를) 임시 프로필로 잠깐 띄워 그려진 화면을 읽습니다.`);
          renderer = await openRenderer({ browser: found, version, repo: REPO_URL, debugPort: precise, headless });
          result.render.browser = found.name;
          const drawn = await rendered(new URL(main.url), 'main', { keep: precise });
          drawn.plainTextLength = main.textLength;
          drawn.headers = main.headers;
          if (precise) {
            mainTab = drawn.tab;
            result.deep.mode = 'precise';
            await reaSurface(mainTab);
            await flowRead(mainTab, drawn);
          }
          // 그려 읽은 쪽에 글이 더 많을 때만 그것으로 바꾼다.
          if (drawn.textLength > main.textLength || precise) { main = drawn; result.pages[0] = drawn; result.render.mode = 'used'; } else result.render.mode = 'no-gain';
        } catch (e) {
          if (e instanceof Stop && HARD_STOP.has(e.code)) throw e;
          result.render.mode = 'failed';
          result.render.error = e instanceof Stop ? e.message : '브라우저를 띄우지 못했어요.';
        }
      }
    }
    const useBrowser = result.render.mode === 'used';
    // 가격, 약관, 환불 링크만 고른다. 같은 사이트, 로그인/결제가 아닌 것, 한 종류에 하나.
    const picked = [];
    const mainPath = new URL(main.url).pathname;
    for (const { kind, re } of LINK_KINDS) {
      const ok = (l) => l.same && l.href && l.path !== mainPath && !picked.some((x) => x.path === l.path) && !neverOpen(l.path) && !/\.(pdf|zip|png|jpe?g|mp4|docx?)$/i.test(l.path);
      // 주소가 맞는 링크를 먼저 고르고, 없을 때만 링크 글자로 고른다 (글자만 보면 엉뚱한 소개 페이지가 잡힌다).
      const cand = main.links.find((l) => ok(l) && re.test(l.path)) || main.links.find((l) => ok(l) && re.test(l.text));
      if (cand) picked.push({ ...cand, kind });
    }
    for (const l of picked) {
      if (result.pages.length >= pagesMax) { result.skipped.push({ url: cleanUrl(l.href), why: `한도 ${pagesMax}장` }); continue; }
      if (useBrowser && (now || Date.now)() - renderStarted > f.limits.renderBudgetMs) { result.skipped.push({ url: cleanUrl(l.href), why: '그려 읽는 시간 한도' }); continue; }
      try {
        // 첫 페이지를 그려서 읽었다면 같은 사이트의 다음 장도 그려서 읽는다 (한 장에 한 번만 연다).
        const pg = useBrowser ? await rendered(new URL(l.href), l.kind) : await page(new URL(l.href), l.kind);
        // 약관 링크로 보고 열었는데 약관이 아니면 약관으로 치지 않는다 (약관을 못 읽은 것으로 남는다).
        if (l.kind === 'terms' && !looksLikeTerms(pg)) pg.kind = 'other';
        result.pages.push(pg);
      } catch (e) {
        if (!(e instanceof Stop)) throw e;
        result.skipped.push({ url: cleanUrl(l.href), why: e.message });
        // 막힘, 사람 확인, 연결 문제를 만나면 남은 링크도 받지 않고 거기서 끝낸다.
        if (HARD_STOP.has(e.code)) { result.stop = { code: e.code, message: e.message }; break; }
      }
    }
    // 약관까지 읽은 다음에야 속 읽기를 할지 정한다.
    if (mainTab && result.deep.mode === 'precise' && !result.stop) await codeRead(mainTab);
  } catch (e) {
    if (!(e instanceof Stop)) throw e;
    result.stop = { code: e.code, message: e.message };
  } finally {
    result.deep.hosts = [...hostsSeen.values()];
    if (result.deep.mode === 'precise') {
      // 근거로 남기는 것은 호스트 이름과 누른 종류, 코드에서 찾은 짧은 이름뿐이다. 본문, 쿠키, 스크립트 글은 남기지 않는다.
      const fl = result.deep.flow;
      if (fl.state === 'done') fl.file = saveEvidence('03_flow.json', `${JSON.stringify({ clicks: fl.clicks, kinds: fl.kinds, moved: fl.moved, hosts: result.deep.hosts.map((h) => ({ host: h.host, requests: h.count, sent: h.sent })) }, null, 2)}\n`) || 'evidence/03_flow.json';
      const cd = result.deep.code;
      if (['done', 'partial'].includes(cd.state)) cd.scanFile = saveEvidence('04_code_scan.json', `${JSON.stringify({ files: cd.files, bytes: cd.bytes, routes: cd.routes, endpoints: cd.endpoints, payments: cd.payments, prices: cd.prices, plans: cd.plans }, null, 2)}\n`) || 'evidence/04_code_scan.json';
    }
    if (mainTab) { try { await mainTab.close(); } catch { /* 닫는 중 오류는 넘어간다 */ } }
    if (renderer) { try { result.render.closed = await renderer.close(); } catch { /* 닫는 중 오류는 넘어간다 */ } }
  }
  result.delayMs = f.delay();
  return result;
}

// ---------- 초안 만들기 ----------
const PAGE_LABEL = { main: '첫 페이지', pricing: '가격 페이지', terms: '이용약관', refund: '환불 정책', other: '그 밖의 페이지' };
export function buildDraftFromPages(c, { relation = 'third-party', today = new Date().toISOString().slice(0, 10), version = '0' } = {}) {
  const main = c.pages[0];
  if (!main) throw new Error('읽은 페이지가 없어요');
  const host = new URL(main.url).hostname;
  const evidence = [];
  const add = (type, ref, note, seen) => { const id = `E${evidence.length + 1}`; evidence.push({ id, type, ref, note, seen_at: today, ...(seen ? { seen } : {}) }); return id; };
  const ev = new Map();
  for (const p of c.pages) ev.set(p, add('url', p.url, p.rendered
    ? `${PAGE_LABEL[p.kind] || '페이지'}. 헤드리스 브라우저(임시 프로필)로 한 번 열어 그려진 화면의 글자와 구조, 구역의 위치를 읽음 (응답 ${p.status}, 글자 ${p.textLength}자). 누르기와 입력 없음, 화면 캡처 없음`
    : `${PAGE_LABEL[p.kind] || '페이지'}. 공개 HTML 을 한 번 받아 글자와 구조만 읽음 (응답 ${p.status}, 글자 ${p.textLength}자${p.truncated ? ', 크기 한도에서 잘림' : ''}). 스크립트는 실행하지 않음`));
  const E = ev.get(main);
  const R = c.robots ? add('url', c.robots.url, c.robots.found ? `robots.txt. 따른 규칙: Allow ${c.robots.allow.join(' ') || '없음'}, Disallow ${c.robots.disallow.slice(0, 8).join(' ') || '없음'}${c.robots.delay != null ? `, Crawl-delay ${c.robots.delay}` : ''}` : `robots.txt 자리에 규칙이 없음 (응답 ${c.robots.status})`) : null;
  // 정밀 모드에서 얻은 것: 흐름에서 본 것과 코드에서 본 것은 근거를 따로 둔다.
  const dp = c.deep || { mode: 'light', why: '', surface: { state: 'done' }, flow: { state: 'skipped' }, code: { state: 'skipped' }, hosts: [] };
  const precise = dp.mode === 'precise';
  const flowDone = precise && dp.flow.state === 'done';
  const codeDone = precise && ['done', 'partial'].includes(dp.code.state);
  const kindWord = { tab: '탭', details: '접힌 글', expand: '펼침 단추', more: '더 보기' };
  const clicksText = flowDone && dp.flow.clicks ? `펼치기 ${dp.flow.clicks}번 (${Object.entries(dp.flow.kinds).map(([k, v]) => `${kindWord[k] || k} ${v}`).join(', ')})` : '누른 것 없음';
  const F = flowDone ? add('doc', dp.flow.file || 'evidence/03_flow.json', `흐름 읽기 기록. ${clicksText}. 폼, 로그인, 가입, 결제, 구매 단추는 누르지 않음. 페이지가 요청을 보내려던 호스트 이름 ${(dp.hosts || []).length}개 (본문, 쿠키, 토큰은 남기지 않음)`, 'flow') : null;
  const C = codeDone ? add('doc', dp.code.file || dp.code.scanFile || 'evidence/04_code_scan.json', `속 읽기 기록. 이미 내려온 스크립트 ${dp.code.files || (dp.code.rea ? dp.code.rea.scripts : 0)}개에서 이름만 찾음${dp.code.rea ? ` (REA analyze-web-bundle: ${dp.code.rea.scripts}개 가운데 ${dp.code.rea.parsed}개 분석)` : ''}. 찾은 주소는 하나도 부르지 않음`, 'code') : null;
  const code = (text, ...e) => ({ text, status: 'code', evidence: e.filter(Boolean) });
  const services = precise ? classifyHosts(dp.hosts || [], host) : [];
  const obs = (text, ...e) => ({ text, status: 'observed', evidence: e.filter(Boolean) });
  const inf = (text, ...e) => ({ text, status: 'inferred', evidence: e.filter(Boolean) });
  const unk = (text) => ({ text, status: 'unknown', evidence: [] });
  const seenOn = `${today} 에 읽은 값`;
  const all = c.pages;
  // 읽은 글이 얇은지, 브라우저로 그려 읽었는지.
  const rs = c.render || { mode: 'off', browser: '', pages: 0, allowed: 0, blocked: 0, why: {} };
  const drawn = !!main.rendered;
  const chars = main.textLength;
  const htmlChars = main.plainTextLength ?? main.textLength;
  const thin = chars < THIN_CHARS;
  const whyNotDrawn = { unavailable: '이 컴퓨터에서 Chrome 계열 브라우저(Chrome, Chromium, Edge, Brave)를 찾지 못해 그려진 화면은 읽지 못했다', off: '그려 읽기를 꺼 두어(--no-render) 그려진 화면은 읽지 않았다', failed: '브라우저로 그려 읽으려 했으나 실패했다', 'no-gain': '브라우저로 그려 봐도 글이 늘지 않았다', 'not-needed': '받은 HTML 만 읽었다' }[rs.mode] || '받은 HTML 만 읽었다';
  const nextStep = drawn
    ? '로그인 뒤에 내용이 있거나 그림 위주의 페이지일 수 있다. 직접 본 화면을 메모해 에이전트와 함께 채운다.'
    : rs.mode === 'unavailable' ? 'Chrome 계열 브라우저가 있는 컴퓨터에서 다시 실행하거나, REA 가 있으면 에이전트의 정밀 모드로 읽는다. 둘 다 없으면 직접 본 화면을 메모해 에이전트와 함께 채운다.'
      : rs.mode === 'off' ? '--no-render 를 빼고 다시 실행하면 그려진 화면까지 읽는다.'
        : '에이전트에게 이 초안을 넘겨 화면을 직접 보고 채우게 한다.';

  // 1. 돈
  const price = [];
  for (const p of all) {
    if (p.prices.length) price.push(obs(`${PAGE_LABEL[p.kind] || '페이지'}에 가격 모양의 글자가 보인다: ${p.prices.slice(0, 5).map((x) => q(x, 24)).join(', ')} (${seenOn}).`, ev.get(p)));
    for (const j of p.ld) for (const o of j.offers) price.push(obs(`HTML 의 JSON-LD(${short(j.type, 30)})에 가격 ${o.price} ${o.currency} 이 적혀 있다 (${seenOn}).`, ev.get(p)));
  }
  if (flowDone && (dp.flow.newPrices || []).length) price.push(obs(`펼친 뒤에 가격 모양의 글자가 더 보인다: ${dp.flow.newPrices.slice(0, 5).map((x) => q(x, 24)).join(', ')} (${seenOn}).`, F));
  if (codeDone) {
    // 화면에서 이미 본 값과 숫자가 같은 것은 빼고, 코드에서만 보이는 것만 흔적으로 적는다.
    const digits = (x) => String(x).replace(/\D/g, '');
    const onScreen = new Set([...all.flatMap((p) => p.prices), ...(dp.flow.newPrices || [])].map(digits));
    const only = (dp.code.prices || []).filter((x) => !onScreen.has(digits(x)));
    if (only.length) price.push(code(`코드 안에 가격처럼 보이는 숫자나 글자가 있다: ${only.slice(0, 6).map((x) => q(x, 20)).join(', ')}. 화면에서는 보지 못했으므로 지금 파는 가격인지는 모른다.`, C));
  }
  if (!price.length) price.push(unk('받은 페이지에서 가격 모양의 글자를 찾지 못했다. 다른 곳에 있는지, 스크립트로 그려지는지는 모른다.'));

  // 2. 흐름
  const steps = [];
  const h1 = main.headings.find((h) => h.level === 1);
  steps.push(main.title || h1
    ? { stage: 'arrive', label: '유입', ...obs(`첫 페이지의 제목은 ${q(main.title || h1.text, 40)} 이고${main.metas.description ? ' 검색용 소개 글이 있으며' : ''}${main.metas['og:title'] || main.metas['og:image'] ? ' 공유용 메타가 있다' : ' 공유용 메타는 보이지 않는다'}. 사람들이 어디서 들어오는지는 밖에서 보이지 않는다.`, E) }
    : { stage: 'arrive', label: '유입', ...unk('첫 페이지에서 제목을 읽지 못했다. 어디서 사람이 들어오는지 모른다.') });
  steps.push({ stage: 'first_value', label: '첫 가치', ...unk('처음 값을 느끼는 순간이 무엇인지는 자동으로 정하지 않는다. 사람이나 에이전트가 페이지를 읽고 채운다.') });
  const signup = uniq(all.flatMap((p) => p.signup));
  const login = uniq(all.flatMap((p) => p.login));
  const pay = uniq(all.flatMap((p) => p.pay));
  const back = uniq(all.flatMap((p) => p.back));
  steps.push(signup.length || login.length
    ? { stage: 'signup', label: '가입', ...obs(`가입이나 로그인으로 가는 누르는 곳이 보인다: ${[...signup, ...login].slice(0, 3).map((x) => q(x, 20)).join(', ')}. 열어 보지 않았다.`, E) }
    : { stage: 'signup', label: '가입', ...unk('받은 페이지에서 가입으로 가는 누르는 곳을 찾지 못했다.') });
  steps.push(pay.length || price[0].status === 'observed'
    ? { stage: 'payment', label: '결제', ...obs(`${pay.length ? `결제나 신청으로 이어지는 문구가 보인다: ${pay.slice(0, 3).map((x) => q(x, 20)).join(', ')}.` : '가격 글자는 보이지만 결제로 가는 누르는 곳은 찾지 못했다.'} 결제 화면은 열지 않았다.`, E) }
    : { stage: 'payment', label: '결제', ...unk('받은 페이지에서 결제로 이어지는 누르는 곳을 찾지 못했다.') });
  steps.push(back.length
    ? { stage: 'return', label: '다시 오기', ...obs(`다시 오게 하는 데 쓰일 수 있는 링크가 보인다: ${back.slice(0, 4).map((x) => q(x, 16)).join(', ')}. 실제로 어떻게 쓰이는지는 보지 않았다.`, E) }
    : { stage: 'return', label: '다시 오기', ...unk('다시 오게 하는 장치(알림, 구독, 커뮤니티)는 받은 페이지에서 찾지 못했다. 로그인 뒤에 있는지는 모른다.') });

  // 3. 화면
  const screens = all.map((p) => ({
    name: `${PAGE_LABEL[p.kind] || '페이지'} (${short(new URL(p.url).pathname, 40)})`,
    purpose: '자동 초안이다. 구역의 수와 누르는 곳의 수만 옮겼고, 목적은 사람이나 에이전트가 읽고 고쳐 쓴다.',
    features: [
      `큰 제목과 중간 제목 ${p.headings.length}개`,
      `링크 ${p.counts.links}개, 단추 ${p.counts.buttons}개 (가입 문구 ${p.signup.length}, 결제 문구 ${p.pay.length}, 로그인 문구 ${p.login.length})`,
      `그림 ${p.counts.img}개, 영상 ${p.counts.video}개, 끼워 넣은 틀 ${p.counts.iframe}개`,
      p.counts.form ? `입력 폼 ${p.counts.form}개 (${p.counts.password ? '비밀번호 칸 있음, ' : ''}아무것도 넣거나 보내지 않음)` : '입력 폼 없음',
      p === main && p.skeleton.length ? `위에서 아래로 구역 ${p.skeleton.length}개` : '',
    ].filter(Boolean),
    status: 'observed', evidence: [ev.get(p)],
  }));

  // 코드에서만 이름이 보인 화면: 링크로 보이지도 않고 읽지도 않은 경로. 열어 보지 않는다.
  let codeOnlyRoutes = [];
  if (codeDone) {
    const shown = new Set([...all.map((p) => new URL(p.url).pathname), ...all.flatMap((p) => p.links.filter((l) => l.same).map((l) => l.path))]);
    codeOnlyRoutes = (dp.code.routes || []).filter((r) => r !== '/' && !shown.has(r) && !shown.has(`${r}/`));
    // 로그인이나 결제 뒤로 보이는 경로를 앞에 둔다.
    const behind = (r) => (looksBehindLogin(r) || neverOpen(r) || /(payment|player|checkout|admin)/i.test(r) ? 1 : 0);
    codeOnlyRoutes.sort((x, y) => behind(y) - behind(x) || x.localeCompare(y));
    for (const r of codeOnlyRoutes.slice(0, 14)) screens.push({ name: short(r, 48), purpose: looksBehindLogin(r) || neverOpen(r) ? '코드에서만 이름이 보인 화면. 로그인이나 결제 뒤로 보이는 경로다. 열어 보지 않았다.' : '코드에서만 이름이 보인 화면. 어디서 이어지는지 화면에서는 보지 못했다. 열어 보지 않았다.', features: [], status: 'code', evidence: [C] });
  }

  // 4. 기술
  const tech = [];
  if (main.counts.script) tech.push({ layer: '스크립트', ...obs(`첫 페이지가 스크립트 파일 ${main.counts.script}개를 부른다. 부르는 곳: ${main.scriptHosts.slice(0, 6).map((h) => (h === host ? '같은 주소' : h)).join(', ') || '같은 주소'}.`, E) });
  if (main.tech.length) tech.push({ layer: '만든 도구 단서', ...inf(`파일 이름과 주소의 모양으로 보아 ${main.tech.slice(0, 6).join(', ')} 을(를) 쓰는 것으로 추정한다.`, E) });
  if (main.generator) tech.push({ layer: '만든 도구 단서', ...obs(`HTML 머리말의 generator 값: ${q(main.generator, 40)}.`, E) });
  const hd = Object.entries(main.headers || {}).filter(([k]) => ['server', 'x-powered-by', 'via'].includes(k));
  if (hd.length) tech.push({ layer: '응답 머리말', ...obs(`응답 머리말에 ${hd.map(([k, v]) => `${k}: ${short(v, 30)}`).join(', ')} 이 있다.`, E) });
  const ldTypes = uniq(all.flatMap((p) => p.ld.map((j) => j.type)));
  tech.push({ layer: '검색용 HTML', ...obs(`스크립트를 실행하지 않고 받은 HTML 에 글자가 ${main.plainTextLength ?? main.textLength}자 있다${ldTypes.length ? `. JSON-LD ${ldTypes.length}종 (${ldTypes.slice(0, 4).map((x) => short(x, 24)).join(', ')})` : ''}${main.lang ? `. lang=${short(main.lang, 8)}` : ''}.`, E) });
  if (drawn) tech.push({ layer: '그리는 방식', ...obs(`스크립트를 실행하지 않고 받은 HTML 의 글은 ${htmlChars}자였고, 브라우저가 그린 뒤에는 ${chars}자다. 화면을 브라우저에서 스크립트로 그리는 페이지다.`, E) });
  else if (thin && main.counts.scriptTags > 0) tech.push({ layer: '그리는 방식', ...unk(`받은 HTML 의 글이 ${chars}자로 적다. ${whyNotDrawn}. 스크립트가 화면에 무엇을 더 그리는지는 모른다.`) });
  if (drawn && rs.blocked) tech.push({ layer: '브라우저 안에서 거른 요청', ...obs(`그려 읽는 동안 페이지가 보내려던 요청 가운데 ${rs.blocked}개는 보내지 않았다 (${Object.entries(rs.why).map(([k, v]) => `${k} ${v}`).join(', ')}). 그 응답으로 그려지는 부분은 화면에 없을 수 있다.`, E) });
  if (precise && dp.surface.storage) {
    const st = dp.surface.storage;
    const parts = [st.local.length ? `localStorage 키 이름 ${st.local.length}개` : '', st.session.length ? `sessionStorage 키 이름 ${st.session.length}개` : '', st.idb.length ? `IndexedDB 이름 ${st.idb.length}개 (${st.idb.slice(0, 3).map((x) => short(x, 28)).join(', ')})` : ''].filter(Boolean);
    if (parts.length) tech.push({ layer: '브라우저 저장소', ...obs(`${parts.join(', ')}. 값은 읽지 않았다.`, E) });
  }
  if (flowDone) {
    const named = services.filter((x) => x.kind !== 'other');
    const others = services.filter((x) => x.kind === 'other');
    if (services.length) tech.push({ layer: '바깥 서비스', ...obs(`페이지가 요청을 보내려던 바깥 호스트 ${services.reduce((n, x) => n + x.hosts.length, 0)}곳${named.length ? `: ${named.slice(0, 10).map((x) => `${SERVICE_KINDS[x.kind]} ${x.name}`).join(', ')}` : ''}${others.length ? `${named.length ? ', 그 밖 ' : ': 그 밖 '}${others.length}곳` : ''}. 호스트 이름만 적었고 주고받은 내용은 보지 않았다.`, F) });
  }
  if (codeDone) {
    if ((dp.code.payments || []).length) tech.push({ layer: '결제 모듈', ...code(`코드 안에 결제 모듈 이름이 보인다: ${dp.code.payments.join(', ')}. 실제로 그 결제사로 결제되는지는 결제 화면을 열지 않아 모른다.`, C) });
    if ((dp.code.routes || []).length) tech.push({ layer: '화면 경로', ...code(`코드 안에 화면 경로 이름이 ${dp.code.routes.length}개 있다. 이 가운데 ${codeOnlyRoutes.length}개는 화면에서 링크로 보이지 않았다${codeOnlyRoutes.length ? ` (예: ${codeOnlyRoutes.slice(0, 5).map((x) => short(x, 24)).join(', ')})` : ''}. 하나도 열어 보지 않았다.`, C) });
    if ((dp.code.endpoints || []).length) tech.push({ layer: '서버 호출 이름', ...code(`코드 안에 서버 호출 주소처럼 보이는 이름이 ${dp.code.endpoints.length}개 있다 (예: ${dp.code.endpoints.slice(0, 4).map((x) => short(x, 28)).join(', ')}). 하나도 불러 보지 않았다.`, C) });
    if ((dp.code.plans || []).length) tech.push({ layer: '요금제 이름', ...code(`코드 안에 요금제나 상품 이름처럼 보이는 글자가 있다: ${dp.code.plans.slice(0, 6).map((x) => q(x, 20)).join(', ')}. 지금 파는 것인지는 화면에서 확인되지 않았다.`, C) });
    if (dp.code.state === 'partial') tech.push({ layer: '읽지 못한 스크립트', ...unk(`${dp.code.note}. 그 안의 경로와 이름은 모른다.`) });
  }
  tech.push({ layer: '서버', ...unk('서버, 데이터 저장소, 결제 연동은 밖에서 보이지 않는다.') });

  // 5. 모르는 것
  const unknowns = [
    { question: '누가 사는가, 어떤 문제를 푸는가', why: '자동 수집기는 해석을 하지 않는다. 본 것만 옮긴다.', next: '에이전트에게 이 초안을 넘겨 reversebusiness 스킬 절차대로 읽고 채우게 한다.' },
    { question: '매출, 구매자 수, 전환율', why: '공개된 숫자를 찾지 않았다. 계산해서 만들지 않는다.', next: '대상이 직접 공개한 자료가 있을 때만 주소와 함께 적는다. 없으면 비워 둔다.' },
    { question: '가입과 결제 뒤의 화면', why: '로그인, 가입, 결제는 열지 않는다.', next: '공개 도움말이나 대상이 공개한 영상이 있으면 그것만 본다.' },
    { question: '이용약관이 자동 열람과 복제를 어떻게 다루는가', why: all.some((p) => p.kind === 'terms') ? '약관 페이지를 받아 두었지만 조항을 해석하지 않았다.' : '약관 링크를 찾지 못했다.', next: '약관을 사람이 직접 읽고 meta.terms 에 한 줄로 적는다.' },
  ];
  if (thin && !drawn) unknowns.push({ question: '스크립트로 그려지는 화면의 내용', why: `${whyNotDrawn}.`, next: nextStep });
  if (thin && drawn) unknowns.push({ question: '그려진 화면에도 글이 적은 까닭', why: `브라우저로 그린 뒤에도 글이 ${chars}자뿐이다.`, next: nextStep });
  if (precise && !codeDone) unknowns.push({ question: '코드 안에 있는 화면 경로와 결제 모듈 이름', why: `${dp.code.note || '속 읽기를 하지 않았다'}.`, next: dp.code.state === 'blocked' ? '약관이 막고 있으므로 하지 않는다. 화면과 흐름에서 본 것만으로 정리한다.' : relation === 'own' ? '다시 실행해 본다.' : '이용약관을 사람이 직접 읽어 코드 분석을 금지하는지 확인한 뒤에 정한다. 내 것이면 --own 을 붙인다.' });
  for (const s of c.skipped) unknowns.push({ question: `받지 않은 페이지: ${short(s.url, 60)}`, why: short(s.why, 120), next: '필요하면 사람이 직접 연다.' });

  const termsPage = all.find((p) => p.kind === 'terms');
  // 흐름과 코드에서 본 바깥 서비스. 이름만 적는다.
  const serviceList = [
    ...['payment', 'analytics', 'video', 'auth', 'data', 'chat'].map((k) => ({ kind: k, label: SERVICE_KINDS[k], names: services.filter((x) => x.kind === k).map((x) => x.name), seen: 'flow', evidence: [F].filter(Boolean) })).filter((x) => x.names.length && F),
    ...(codeDone ? [{ kind: 'payment', label: SERVICE_KINDS.payment, names: (dp.code.payments || []).filter((n) => !services.some((x) => x.kind === 'payment' && x.name === n)), seen: 'code', evidence: [C] }].filter((x) => x.names.length) : []),
  ];
  const report = {
    schema: 'rebiz/report@1',
    meta: {
      target: { name: short(main.title, 80) || host, kind: 'web-service', url: main.url, relation },
      analyzed_at: today,
      analyst: precise ? `rebiz ${version} 정밀 모드 (REA 로 읽은 자동 초안, 해석 없음)` : `rebiz ${version} 가벼운 수집기 (자동 초안, 해석 없음)`,
      depth: {
        mode: precise ? 'precise' : 'light',
        reached: codeDone ? 'code' : flowDone ? 'flow' : 'surface',
        steps: [
          { key: 'surface', state: 'done', note: precise ? (dp.surface.rea === 'done' ? `그려진 화면의 글과 구조를 읽음 (REA inspect-web-page, 글자 ${chars}자)` : `${dp.surface.note || 'REA 겉 읽기 없이 우리 읽기만 씀'} (글자 ${chars}자)`) : `${drawn ? '브라우저가 그린 화면을 읽음' : '받은 HTML 만 읽음'} (글자 ${chars}자)` },
          { key: 'flow', state: precise ? dp.flow.state : 'skipped', note: flowDone ? `${clicksText}, 바깥 호스트 ${services.reduce((n, x) => n + x.hosts.length, 0)}곳${dp.flow.moved ? '. 누른 뒤 다른 화면으로 넘어가서 거기서 멈춤' : ''}` : precise ? (dp.flow.note || '흐름 읽기를 하지 못했다') : (dp.why || 'REA 를 찾지 못해 가벼운 모드로 읽었다') },
          { key: 'code', state: precise ? dp.code.state : 'skipped', note: codeDone ? `화면 경로 이름 ${(dp.code.routes || []).length}개 (코드에서만 ${codeOnlyRoutes.length}개), 결제 모듈 이름 ${(dp.code.payments || []).length}개${dp.code.state === 'partial' ? `. ${dp.code.note}` : ''}${dp.code.termsNote ? `. ${dp.code.termsNote}` : ''}` : precise ? (dp.code.note || '속 읽기를 하지 않았다') : (dp.why || 'REA 를 찾지 못해 가벼운 모드로 읽었다') },
        ],
      },
      read: { mode: drawn ? 'rendered' : 'html', chars, html_chars: htmlChars, thin, ...(thin ? { note: `읽은 글이 ${chars}자뿐이라 모름이 많다. ${drawn ? '브라우저로 그려 읽은 결과다' : whyNotDrawn}.`, next: nextStep } : {}) },
      scope: `공개 페이지 ${all.length}장을 읽었다 (요청 ${c.log.length}번, 요청 사이 ${Math.round(c.delayMs / 100) / 10}초 이상). ${rs.pages ? `받은 HTML 의 글이 얇아 ${rs.pages}장은 헤드리스 브라우저(${rs.browser}, 임시 프로필)로 한 번씩 열어 그려진 화면을 읽었다. 누르기, 입력, 화면 캡처는 하지 않았고, 브라우저 안에서 GET 이 아닌 요청, robots.txt 가 막은 주소, 분석 도구는 보내지 않았다. ` : '스크립트를 실행하지 않았다. '}로그인, 가입, 결제, 폼 제출을 하지 않았고, 쿠키를 저장하지 않았다.`,
      method: uniq(['robots.txt 를 먼저 확인', '공개 HTML 을 GET 으로 받기 (스크립트 실행 없음)', precise && dp.surface.rea === 'done' ? 'REA inspect-web-page (겉 읽기: 글, 구조, 저장소 키 이름. 값은 읽지 않음)' : '', flowDone ? '흐름 읽기: 펼치기만 누르고 요청 호스트 이름만 모음' : '', codeDone ? `속 읽기: 이미 내려온 스크립트에서 이름만 찾음${dp.code.rea ? ' (REA analyze-web-bundle)' : ''}. 찾은 주소는 부르지 않음` : '', rs.pages ? `그려진 화면 읽기: 헤드리스 ${rs.browser}, 임시 프로필, 끝나면 브라우저를 끄고 프로필 삭제` : '', `읽은 것: ${all.map((p) => PAGE_LABEL[p.kind] || '페이지').join(', ')}`, 'collect.mjs 로 초안 만들기'].filter(Boolean)),
      terms: {
        // checked 는 약관 조항까지 사람이 읽었을 때만 쓴다. 자동 초안은 거기까지 가지 않는다.
        status: relation === 'own' ? 'not-applicable' : (termsPage || (c.robots && c.robots.found)) ? 'robots-only' : 'not-found',
        note: `${relation === 'own' ? '내 것이라 약관 확인은 해당 없다. ' : ''}${c.robots && c.robots.found ? `robots.txt 를 받았고 읽은 주소는 모두 허용 범위였다 (Disallow ${c.robots.disallow.length}줄).` : 'robots.txt 에 규칙이 없었다.'}${relation === 'own' ? '' : termsPage ? ' 이용약관 페이지를 받아 두었으나 조항은 아직 읽지 않았다. 사람이 읽은 뒤 checked 로 바꾼다.' : ' 이용약관 링크는 찾지 못했다. 사람이 찾아 읽은 뒤 checked 로 바꾼다.'}`,
        evidence: [R, termsPage ? ev.get(termsPage) : null].filter(Boolean),
      },
      one_line: '',
      draft: true,
    },
    evidence,
    sections: {
      money: {
        customer: [unk('누가 사는지는 자동으로 정하지 않는다. 사람이나 에이전트가 채운다.')],
        problem: [unk('어떤 문제를 푸는지는 자동으로 정하지 않는다. 사람이나 에이전트가 채운다.')],
        price,
        revenue: [],
      },
      flow: { steps, ...(serviceList.length ? { services: serviceList } : {}) },
      map: { screens },
      tech: { items: tech },
      unknowns,
      my_version: { working_name: '', same_problem: '', who: '', mvp: [], differences: [{ title: '', text: '' }, { title: '', text: '' }, { title: '', text: '' }], not_taken: [] },
    },
  };
  if (main.skeleton.length >= 2) report.skeleton = { note: main.measured ? '브라우저가 그린 화면에서 구역의 위치와 길이를 잰 뼈대. 순서와 길이는 잰 값이고, 층 이름은 규칙으로 붙인 추정이다. 화면 캡처는 저장하지 않았고, 원본의 글과 그림은 들어 있지 않다.' : '받은 HTML 의 구역 순서를 위에서 아래로 옮긴 뼈대. 길이는 글과 그림의 양으로 어림했고, 층 이름은 규칙으로 붙인 추정이다. 원본의 글과 그림은 들어 있지 않다.', evidence: [E], blocks: main.skeleton };

  // 겹침 검사용 원본 글 묶음. 리포트에는 들어가지 않는다.
  const bare = host.replace(/^www\./, '');
  const names = uniq([...main.title.split(/[|·\-–:]/).map((s) => s.trim()), main.metas['og:site_name'] || '', main.metas['application-name'] || ''].filter((s) => s && s.length >= 3));
  const source = {
    schema: 'rebiz/source@1',
    note: '원본에서 모은 글과 자원 주소. 내 버전과 겹치는지 보는 데만 쓴다. 다른 곳에 올리지 않는다.',
    url: main.url,
    brand: { names, domains: uniq([host, bare, bare.split('.')[0]].filter((s) => s && s.length >= 3)) },
    texts: uniq([...all.flatMap((p) => p.lines), ...all.flatMap((p) => ['description', 'og:title', 'og:description', 'og:site_name', 'twitter:title', 'twitter:description'].map((k) => p.metas[k] || ''))].map(scrub).filter((t) => t.length >= 2)),
    assets: uniq(all.flatMap((p) => p.assets)),
  };
  return { report, source, thin, read: report.meta.read };
}

// 설치된 스킬 폴더의 표식 파일이나 저장소의 package.json 에서 판 번호를 읽는다.
export function toolVersion() {
  for (const f of [path.join(HERE, '..', '.rebiz.json'), path.join(HERE, '..', '..', '..', 'package.json')]) {
    try { const v = JSON.parse(fs.readFileSync(f, 'utf8')).version; if (v) return String(v); } catch { /* 다음 후보 */ }
  }
  return '0';
}

function parseArgs(argv) {
  const o = { out: '', pages: LIMITS.maxPages, relation: 'third-party', render: 'auto' };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    const next = () => String(argv[++i] ?? '');
    if (a === '--out') o.out = next();
    else if (a === '--pages') o.pages = Number(next());
    else if (a === '--relation') o.relation = next();
    else if (a === '--own') o.relation = 'own';
    else if (a === '--no-render') o.render = 'off';
    else if (a === '--render') o.render = 'force';
    else if (a === '--help' || a === '-h') o.help = true;
    else if (a.startsWith('--')) o.bad = a;
    else if (!o.url) o.url = a;
    else o.bad = a;
  }
  return o;
}

export function outDirFor(url) {
  const u = normalizeUrl(url);
  return `rebiz-${u.hostname.replace(/^www\./, '').replace(/[^a-z0-9.-]/gi, '-')}`;
}

// 폴더에 report.json, source.json, requests.json 을 쓴다.
export function writeOutputs(dir, c, built) {
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'report.json'), `${JSON.stringify(built.report, null, 2)}\n`);
  fs.writeFileSync(path.join(dir, 'source.json'), `${JSON.stringify(built.source, null, 2)}\n`);
  fs.writeFileSync(path.join(dir, 'requests.json'), `${JSON.stringify({ user_agent: c.ua, delay_ms: c.delayMs, pages_max: c.pagesMax, render: c.render, requests: c.log, skipped: c.skipped }, null, 2)}\n`);
}

async function main() {
  const o = parseArgs(process.argv.slice(2));
  const usage = '사용: node collect.mjs <주소> [--out <폴더>] [--pages 1~5] [--own] [--no-render]';
  if (o.help) { console.log(usage); return; }
  if (o.bad || !o.url || !(o.pages >= 1) || !['own', 'third-party'].includes(o.relation)) { if (o.bad) console.error(`모르는 인자: ${o.bad}`); console.error(usage); process.exit(2); }
  const version = toolVersion();
  let c;
  try { c = await collect(o.url, { version, maxPages: o.pages, render: o.render, onStep: (s) => console.log(`  ${s}`) }); } catch (e) { console.error(`멈춤  ${e.message}`); process.exit(e instanceof Stop ? 3 : 1); }
  if (!c.pages.length) { console.error(`멈춤  ${c.stop ? c.stop.message : '읽은 페이지가 없어요.'}`); process.exit(3); }
  const built = buildDraftFromPages(c, { relation: o.relation, version });
  const dir = path.resolve(o.out || outDirFor(o.url));
  writeOutputs(dir, c, built);
  console.log(`초안: ${path.join(dir, 'report.json')}  (요청 ${c.log.length}번, 페이지 ${c.pages.length}장)`);
  if (c.stop) console.log(`알림  ${c.stop.message}`);
  if (built.thin) console.log(`알림  ${built.read.note} 다음: ${built.read.next}`);
  console.log('source.json 과 requests.json 은 내 컴퓨터에만 둡니다. 초안은 본 것만 옮긴 것이고, 해석은 스킬 절차대로 채웁니다.');
}

// 바로 실행했을 때만 돈다. 경로에 심볼릭 링크가 끼어 있어도 알아보도록 실제 경로로 견준다.
const direct = (() => { try { return fs.realpathSync(process.argv[1]) === fs.realpathSync(fileURLToPath(import.meta.url)); } catch { return false; } })();
if (direct) await main();
