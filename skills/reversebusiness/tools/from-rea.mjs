#!/usr/bin/env node
// REA 근거(Evidence JSON)에서 reversebusiness report.json 초안을 만든다. 의존성 없음.
//
// 사용:
//   node from-rea.mjs <REA Evidence JSON ...> [옵션]
//   rebiz <주소> 의 정밀 모드가 남긴 03_flow.json(흐름 읽기 기록)과 04_code_scan.json(속 읽기 기록)도 함께 줄 수 있다.
//   코드에서만 본 것(analyze-web-bundle, 04_code_scan.json)은 관찰이 아니라 코드 흔적(status: code)으로 들어간다.
//
//   --html <파일>        공개 HTML 한 장(선택). 머리말 메타와 JSON-LD 를 읽는다
//   --robots <파일>      robots.txt 사본(선택). 내용 요약을 meta.terms 에 적는다
//   --shot <png>         화면 캡처 파일(선택, 여러 번). 근거 장부에 screen 으로 올린다
//   --relation <값>      third-party(기본) 또는 own
//   --name <이름>        대상 이름. 없으면 페이지 제목을 쓴다
//   --brand <이름>       원본 브랜드 이름(여러 번). source.json 의 brand.names 에 더한다
//   --out <파일>         초안 위치. 기본 report.draft.json
//   --source-out <파일>  원본에서 모은 글 묶음(check-clone 입력). 기본 source.json
//   --base <폴더>        근거 장부에 적을 상대 경로의 기준 폴더. 기본은 --out 이 있는 폴더
//
// 하는 일: 본 것만 관찰로 채운다(제목, 가격 문구, 섹션 순서, 누르는 곳, 기술 흔적, 근거 장부 E1...).
// 고객, 문제, 첫 가치, 매출, 내 버전 명세는 채우지 않는다. 사람이 채울 칸은 모름이나 빈칸으로 남는다.
// 쿠키, 토큰, 인증 헤더 값은 옮기지 않는다. 저장소는 키 이름만 적고, 키 모양 글자는 가린다.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { classifyHosts, looksBehindLogin, SERVICE_KINDS } from './deep.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
// 겹침 검사에 넣을 메타는 사람이 읽는 글만. viewport 같은 설정 값은 어느 페이지나 같아서 뺀다.
const HUMAN_META = /^(description|keywords|author|application-name|apple-mobile-web-app-title|og:(title|description|site_name)|twitter:(title|description))$/i;

// ---------- 가리기 ----------
const SECRET_KEY = /(cookie|token|authorization|auth[_-]?header|secret|password|passwd|session[_-]?id|api[_-]?key|bearer|credential|signature|jwt)/i;
const EMAIL = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;
const KEYLIKE = /(sk-[A-Za-z0-9_-]{16,}|AKIA[0-9A-Z]{12,}|AIza[0-9A-Za-z_-]{20,}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}|\b[A-Fa-f0-9]{32,}\b|\b[A-Za-z0-9+/_-]{48,}={0,2})/g;
const KR_BIZ_NO = /\b\d{3}-\d{2}-\d{5}\b/g;
const PHONE = /\b0\d{1,2}[-.\s]\d{3,4}[-.\s]\d{4}\b/g;

export function scrub(s) {
  return String(s ?? '')
    .replace(EMAIL, '[이메일 가림]')
    .replace(KR_BIZ_NO, '[번호 가림]')
    .replace(PHONE, '[전화 가림]')
    .replace(KEYLIKE, '[키 모양 글자 가림]')
    .replace(/\s+/g, ' ')
    .trim();
}
// 주소는 물음표 뒤(쿼리)와 # 뒤를 떼고 적는다. 쿼리에 식별자가 실릴 수 있다.
export function cleanUrl(u) {
  try {
    const x = new URL(u);
    return scrub(`${x.origin}${x.pathname}`);
  } catch { return ''; }
}
const short = (s, n = 90) => (s.length > n ? `${s.slice(0, n - 1)}…` : s);
const uniq = (a) => [...new Set(a)];
const quote = (s) => `"${short(scrub(s))}"`;

// ---------- Evidence 읽기 ----------
// REA 는 한 건짜리 Evidence({operation, normalized_result})와 묶음({records:[...]}), 요약({summary:{...}})을 낸다.
export function recordsOf(json) {
  if (!json || typeof json !== 'object') return [];
  if (Array.isArray(json.records)) return json.records;
  if (json.summary && json.summary.operation) return [json.summary];
  if (json.operation) return [json];
  return [];
}

// 금지 키 아래의 값은 통째로 버린다. Evidence 를 리포트로 옮기기 전에 한 번 거른다.
export function dropSecrets(v, dropped = new Set()) {
  if (Array.isArray(v)) return v.map((x) => dropSecrets(x, dropped));
  if (v && typeof v === 'object') {
    const o = {};
    for (const [k, val] of Object.entries(v)) {
      // 키 이름 목록(local_storage_keys 등)은 이름만 담겨 있으므로 남긴다.
      const nameList = /_(keys|names)$/.test(k);
      if (SECRET_KEY.test(k) && !nameList) { dropped.add(k); continue; }
      o[k] = dropSecrets(val, dropped);
    }
    return o;
  }
  return v;
}

// 접근성 트리를 문서 순서로 편다. REA 는 parent_id 만 주므로 목록 순서를 자식 순서로 쓴다.
function a11yTree(nodes) {
  const kids = new Map();
  for (const n of nodes) {
    const p = n.parent_id ?? '__root__';
    if (!kids.has(p)) kids.set(p, []);
    kids.get(p).push(n);
  }
  const textOf = (n) => {
    if (n.role === 'InlineTextBox') return '';
    if (n.role === 'StaticText') return n.name || '';
    return (kids.get(n.node_id) || []).map(textOf).filter(Boolean).join(' ');
  };
  const order = [];
  const walk = (n, landmark) => {
    if (n.role === 'InlineTextBox') return;
    const here = ['banner', 'main', 'contentinfo', 'navigation', 'region', 'complementary'].includes(n.role) && !n.ignored
      ? { role: n.role, name: n.name || '' } : landmark;
    order.push({ node: n, landmark: here });
    for (const c of kids.get(n.node_id) || []) walk(c, here);
  };
  for (const r of kids.get('__root__') || []) walk(r, null);
  return { order, textOf, kids };
}

// 가격 모양: 통화 기호가 붙은 숫자, 쉼표가 있거나 세 자리 이상인 숫자 뒤의 원, 만원, 통화 약자.
export const PRICE = /((?:₩|￦|\$|€|£|¥)\s?\d(?:[\d,.]*\d)?|\d{1,3}(?:,\d{3})+\s?(?:원|달러)|\d{3,}\s?(?:원|달러)|\d+(?:\.\d+)?\s?만\s?원|\d(?:[\d,.]*\d)?\s?(?:USD|KRW|EUR|JPY)\b)/;
const SIGNUP = /(회원\s?가입|가입하기|무료\s?가입|sign\s?up|register|create\s+(an\s+)?account|get\s+started)/i;
const PAY = /(수강\s?신청|구매|결제|구독|신청하기|주문|buy|checkout|subscribe|purchase|order\s+now|enroll)/i;
const LOGIN = /(로그인|log\s?in|sign\s?in)/i;

export function readInspect(rec) {
  const n = rec.normalized_result || {};
  const nodes = (n.accessibility && n.accessibility.nodes) || [];
  const { order, textOf, kids } = a11yTree(nodes);
  const page = {
    url: cleanUrl((n.target || {}).url || ''),
    origin: (n.target || {}).origin || '',
    title: scrub((n.target || {}).title || ''),
    evidence_id: rec.evidence_id || '',
    captured_at: ((n.capture_window || {}).started_at || '').slice(0, 10),
    hasText: nodes.length > 0 && ((n.accessibility || {}).text_capture || {}).status === 'included',
    sections: [], headings: [], buttons: [], links: [], prices: [], faqs: [], lines: [],
    counts: {}, scripts: [], storage: null, resources: {}, excluded: [], limitations: n.limitations || rec.limitations || [],
  };
  const count = (k) => { page.counts[k] = (page.counts[k] || 0) + 1; };
  const lineSet = new Set();
  const addLine = (s) => { const t = String(s || '').replace(/\s+/g, ' ').trim(); if (t.length >= 2) lineSet.add(t); };
  for (const { node, landmark } of order) {
    if (node.ignored) continue;
    const r = node.role;
    count(r);
    const name = node.name || '';
    if (['region', 'navigation', 'complementary', 'banner', 'main', 'contentinfo'].includes(r)) page.sections.push({ role: r, name: scrub(name) });
    if (r === 'heading') page.headings.push({ text: scrub(name || textOf(node)), inside: landmark ? landmark.role : '' });
    if (r === 'button') page.buttons.push({ text: scrub(name || textOf(node)), inside: landmark ? landmark.role : '' });
    if (r === 'link') page.links.push({ text: scrub(name || textOf(node)), inside: landmark ? landmark.role : '' });
    if (r === 'DisclosureTriangle') page.faqs.push(scrub(name || textOf(node)));
    if (r === 'StaticText') addLine(name);
    // 문단, 제목, 목록 항목은 안쪽 글자를 이어 붙인 것도 한 줄로 남긴다(겹침 검사용).
    if (['paragraph', 'heading', 'listitem', 'blockquote', 'button', 'link', 'term', 'definition', 'Figcaption'].includes(r)) {
      const t = textOf(node);
      if (t.length <= 400) addLine(t);
    }
  }
  // 가격 문구: 가격 모양이 들어간 가장 안쪽 덩어리만 고른다.
  const hasPrice = (t) => PRICE.test(t);
  const seenPrice = new Set();
  const priceWalk = (n) => {
    if (n.role === 'InlineTextBox') return false;
    const t = textOf(n);
    if (!hasPrice(t)) return false;
    let deeper = false;
    for (const c of kids.get(n.node_id) || []) deeper = priceWalk(c) || deeper;
    if (!deeper && t.length <= 160) {
      const s = scrub(t);
      if (!seenPrice.has(s)) { seenPrice.add(s); page.prices.push(s); }
    }
    return true;
  };
  for (const r of kids.get('__root__') || []) priceWalk(r);

  page.lines = [...lineSet];
  page.scripts = ((n.scripts || {}).items || []).map((s) => ({ url: cleanUrl(s.url || ''), length: s.length || 0 })).filter((s) => s.url);
  if (n.storage) {
    page.storage = {
      local: (n.storage.local_storage_keys || []).map(scrub),
      session: (n.storage.session_storage_keys || []).map(scrub),
      idb: (n.storage.indexed_db_names || []).map(scrub),
      cache: (n.storage.cache_names || []).map(scrub),
    };
  }
  for (const r of n.resources || []) {
    const k = r.mime_type || r.type || '기타';
    page.resources[k] = (page.resources[k] || 0) + 1;
  }
  page.assets = uniq([
    ...(n.resources || []).filter((r) => /^(Image|Media|Font)$/.test(r.type || '')).map((r) => cleanUrl(r.url || '')),
    ...(((n.metadata || {}).dom_urls) || []).filter((u) => /\.(png|jpe?g|webp|gif|svg|ico|avif|mp4|webm|mov|woff2?|ttf|otf)$/i.test(String(u.url || '').split('?')[0])).map((u) => cleanUrl(u.url)),
  ].filter(Boolean));
  page.dom = (n.dom || {}).total_nodes || 0;
  page.excluded = ((n.completeness || {}).excluded || []).filter((e) => e.count).map((e) => ({ section: e.section, reason: e.reason, count: e.count }));
  return page;
}

function readBundle(rec) {
  const n = rec.normalized_result || {};
  const inv = n.route_inventory || {};
  return {
    evidence_id: rec.evidence_id || '',
    url: cleanUrl((n.capture || {}).target_url || n.target_url || ''),
    scripts: (n.capture || {}).scripts_observed || 0,
    parsed: (n.completeness || {}).parsed_scripts || 0,
    status: (n.completeness || {}).status || '',
    routes: uniq([...(inv.routes || []).map((r) => r.path), ...(((n.observations || {}).routes) || []).map((r) => r.value)].filter((p) => typeof p === 'string' && p.startsWith('/'))).map(scrub),
    endpoints: (((n.observations || {}).endpoints) || []).length,
    unknowns: (n.unknowns || []).map((u) => `${u.dimension}: ${String(u.reason || '').split('. Worker detail')[0]}`),
  };
}

// ---------- 공개 HTML (선택) ----------
function readHtml(file) {
  const html = fs.readFileSync(file, 'utf8');
  const head = (html.match(/<head[\s\S]*?<\/head>/i) || [html.slice(0, 20000)])[0];
  const attr = (tag, name) => { const m = tag.match(new RegExp(`${name}\\s*=\\s*("([^"]*)"|'([^']*)')`, 'i')); return m ? (m[2] ?? m[3] ?? '') : ''; };
  const metas = {};
  for (const tag of head.match(/<meta\b[^>]*>/gi) || []) {
    const k = attr(tag, 'property') || attr(tag, 'name');
    const v = attr(tag, 'content');
    if (k && v && !SECRET_KEY.test(k) && !/verification/i.test(k)) metas[k.toLowerCase()] = scrub(v);
  }
  const title = scrub(((html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1]) || '');
  const lang = attr((html.match(/<html\b[^>]*>/i) || [''])[0], 'lang');
  const ld = [];
  for (const m of html.matchAll(/<script\b[^>]*type\s*=\s*["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)) {
    try {
      const j = JSON.parse(m[1]);
      const each = (o) => {
        if (Array.isArray(o)) return o.forEach(each);
        if (!o || typeof o !== 'object') return;
        if (o['@graph']) each(o['@graph']);
        if (o['@type']) {
          const offers = [].concat(o.offers || []).filter((x) => x && typeof x === 'object').map((x) => ({ price: x.price, currency: x.priceCurrency })).filter((x) => x.price != null);
          ld.push({ type: [].concat(o['@type']).join(', '), name: scrub(o.name || ''), offers });
        }
      };
      each(j);
    } catch { /* 깨진 JSON-LD 는 건너뛴다 */ }
  }
  const text = html.replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<style[\s\S]*?<\/style>/gi, ' ').replace(/<[^>]+>/g, '\n');
  const bodyLines = uniq(text.split('\n').map((l) => l.replace(/\s+/g, ' ').trim()).filter((l) => l.length >= 2));
  const assets = uniq([...html.matchAll(/(?:src|href|content|poster)\s*=\s*["']([^"']+\.(?:png|jpe?g|webp|gif|svg|ico|avif|mp4|webm|woff2?|ttf|otf))(?:\?[^"']*)?["']/gi)].map((m) => m[1]));
  return { title, lang, metas, ld, bodyLines, assets, bytes: Buffer.byteLength(html) };
}

function readRobots(file) {
  const lines = fs.readFileSync(file, 'utf8').split('\n').map((l) => l.trim()).filter((l) => l && !l.startsWith('#'));
  const pick = (k) => lines.filter((l) => l.toLowerCase().startsWith(`${k}:`)).map((l) => l.slice(k.length + 1).trim());
  return { allow: uniq(pick('allow')), disallow: uniq(pick('disallow')), agents: uniq(pick('user-agent')).length, sitemap: pick('sitemap').map(cleanUrl) };
}

// ---------- 초안 만들기 ----------
export function buildDraft({ evidenceFiles, htmlFile, robotsFile, shots = [], relation = 'third-party', name = '', brands = [], base }) {
  const dropped = new Set();
  const inspects = [];
  const bundles = [];
  const others = [];
  const flowFiles = [];
  const scanFiles = [];
  for (const f of evidenceFiles) {
    const json = dropSecrets(JSON.parse(fs.readFileSync(f, 'utf8')), dropped);
    // 정밀 모드가 남긴 우리 기록: 흐름(호스트 이름과 누른 종류), 속(코드에서 찾은 이름)
    if (json && Array.isArray(json.hosts) && !json.records && !json.operation) { flowFiles.push({ file: path.relative(base, f).split(path.sep).join('/'), j: json }); continue; }
    if (json && Array.isArray(json.routes) && Array.isArray(json.payments) && !json.records) { scanFiles.push({ file: path.relative(base, f).split(path.sep).join('/'), j: json }); continue; }
    for (const rec of recordsOf(json)) {
      const op = rec.operation || '';
      const rel = path.relative(base, f).split(path.sep).join('/');
      if (op === 'inspect_web_page') inspects.push({ file: rel, page: readInspect(rec) });
      else if (op === 'analyze_web_bundle') bundles.push({ file: rel, b: readBundle(rec) });
      else if (op === 'capture_web_screenshot') {
        const n = rec.normalized_result || {};
        others.push({ kind: 'shot', file: rel, url: cleanUrl((n.target || {}).url || ''), viewport: n.viewport || {}, evidence_id: rec.evidence_id || '', at: (n.captured_at || '').slice(0, 10) });
      } else if (op === 'inspect_analysis_view') {
        // 요약 보기는 묶음 파일이 따로 있으므로 근거로 올리지 않는다.
      } else others.push({ kind: 'other', file: rel, op, evidence_id: rec.evidence_id || '' });
    }
  }
  if (!inspects.length) throw new Error('inspect-web-page Evidence 가 하나도 없어요. REA 로 페이지를 먼저 읽어 주세요.');
  const main = inspects[0].page;
  const html = htmlFile ? readHtml(htmlFile) : null;
  const robots = robotsFile ? readRobots(robotsFile) : null;
  const today = new Date().toISOString().slice(0, 10);
  const termsPage = inspects.map((x) => x.page).find((p) => /(이용\s?약관|terms)/i.test(`${p.title} ${p.url}`));
  const seen = main.captured_at || today;

  // 근거 장부
  const evidence = [];
  const add = (type, ref, note, at = seen, where = '') => { const id = `E${evidence.length + 1}`; evidence.push({ id, type, ref, note, seen_at: at, ...(where ? { seen: where } : {}) }); return id; };
  const pageEv = new Map();
  for (const { file, page } of inspects) {
    const id = add('url', page.url, `REA inspect-web-page 로 읽은 공개 페이지. 제목 ${quote(page.title)}. 기록 ${file}${page.evidence_id ? ` (${page.evidence_id.slice(0, 14)}…)` : ''}`, page.captured_at || seen);
    pageEv.set(page, id);
  }
  const E = pageEv.get(main);
  const shotEv = []; // { id, url }
  for (const o of others.filter((x) => x.kind === 'shot')) shotEv.push({ id: add('screen', o.file, `REA capture-web-screenshot 기록. 보이는 화면 ${o.viewport.width || '?'}x${o.viewport.height || '?'}. 대상 ${o.url}`, o.at || seen), url: o.url });
  for (const s of shots) shotEv.push({ id: add('screen', path.relative(base, s).split(path.sep).join('/'), '화면 캡처 파일'), url: main.url });
  const bundleEv = bundles.map(({ file, b }) => add('doc', file, `REA analyze-web-bundle 기록. 스크립트 ${b.scripts}개 가운데 ${b.parsed}개를 실행 없이 읽음 (${b.status || '상태 모름'})`, seen, 'code'));
  const flowEv = flowFiles.map(({ file, j }) => add('doc', file, `흐름 읽기 기록. 펼치기 ${j.clicks || 0}번, 페이지가 요청을 보내려던 호스트 이름 ${j.hosts.length}개 (본문, 쿠키, 토큰은 없음)`, seen, 'flow'));
  const scanEv = scanFiles.map(({ file, j }) => add('doc', file, `속 읽기 기록. 이미 내려온 스크립트 ${j.files || 0}개에서 이름만 찾음. 찾은 주소는 부르지 않음`, seen, 'code'));
  const htmlEv = html ? add('doc', path.relative(base, htmlFile).split(path.sep).join('/'), `공개 HTML 한 장 사본 (${html.bytes} 바이트). 머리말 메타와 JSON-LD 만 읽음`) : null;
  const robotsEv = robots ? add('doc', path.relative(base, robotsFile).split(path.sep).join('/'), `robots.txt 사본. Allow ${robots.allow.join(' ') || '없음'}, Disallow ${robots.disallow.join(' ') || '없음'}`) : null;

  const obs = (text, ...ev) => ({ text, status: 'observed', evidence: ev.filter(Boolean) });
  const unk = (text) => ({ text, status: 'unknown', evidence: [] });
  const trace = (text, ...ev) => ({ text, status: 'code', evidence: ev.filter(Boolean) });

  // 1번 칸
  const price = [];
  // 긴 문단이면 가격이 들어 있는 문장만 남긴다.
  const priceBit = (p) => {
    if (p.length <= 90) return p;
    const hit = p.split(/(?<=[.!?。])\s+/).filter((x) => PRICE.test(x)).join(' ');
    return hit || p;
  };
  for (const p of main.prices.slice(0, 8)) price.push(obs(`화면에 가격 문구가 보인다: "${short(scrub(priceBit(p)), 150)}"`, E));
  if (html) for (const j of html.ld) for (const of of j.offers) price.push(obs(`HTML 의 JSON-LD(${j.type})에 가격 ${scrub(of.price)} ${scrub(of.currency || '')} 이 적혀 있다`, htmlEv));
  if (!price.length) price.push(unk('이 페이지에서 가격 문구를 찾지 못했다. 다른 곳에 있는지는 모른다.'));

  // 2번 칸
  const hit = (list, re) => uniq(list.map((x) => x.text).filter((t) => re.test(t)));
  const signupBtn = hit([...main.buttons, ...main.links], SIGNUP);
  const loginBtn = hit([...main.buttons, ...main.links], LOGIN);
  const payBtn = hit([...main.buttons, ...main.links], PAY);
  const steps = [];
  steps.push(signupBtn.length
    ? { stage: 'signup', label: '가입', ...obs(`가입으로 가는 누르는 곳이 보인다: ${signupBtn.slice(0, 3).map(quote).join(', ')}. 가입 절차 자체는 열어 보지 않았다.`, E) }
    : { stage: 'signup', label: '가입', ...unk('가입으로 가는 누르는 곳을 이 페이지에서 찾지 못했다.') });
  steps.push({ stage: 'first_value', label: '첫 가치', ...unk('처음 값을 느끼는 순간이 무엇인지는 아직 읽지 않았다. 사람이 채운다.') });
  steps.push(payBtn.length
    ? { stage: 'payment', label: '결제', ...obs(`결제나 신청으로 이어지는 문구가 보인다: ${payBtn.slice(0, 4).map(quote).join(', ')}. 결제 화면은 열지 않았다.`, E) }
    : { stage: 'payment', label: '결제', ...unk('결제로 이어지는 누르는 곳을 이 페이지에서 찾지 못했다.') });

  // 3번 칸
  const screens = inspects.map(({ page }) => {
    const order = [];
    let i = 0;
    for (const s of page.sections) if (s.name) order.push(`구역 ${++i}: ${short(s.name, 40)} (${s.role})`);
    const feats = [
      ...order,
      page.headings.length ? `제목 ${page.headings.length}개. 순서대로: ${page.headings.slice(0, 12).map((h) => short(h.text, 24)).join(' / ')}` : '',
      page.buttons.length ? `버튼 ${page.buttons.length}개: ${uniq(page.buttons.map((b) => short(b.text, 24))).slice(0, 10).join(' / ')}` : '',
      page.faqs.length ? `접었다 펴는 항목 ${page.faqs.length}개` : '',
      `링크 ${page.links.length}개`,
    ].filter(Boolean);
    return { name: page.title || page.url, purpose: '아직 쓰지 않음. 구역 순서와 누르는 곳만 옮겼다.', features: feats, status: 'observed', evidence: [pageEv.get(page), ...shotEv.filter((x) => x.url === page.url).map((x) => x.id)] };
  });

  // 4번 칸
  const tech = [];
  if (main.scripts.length) {
    const names = uniq([...main.scripts].sort((a, b) => b.length - a.length).map((s) => s.url.split('/').pop())).filter((x) => /\.m?js$/.test(x)).slice(0, 3).join(', ');
    tech.push({ layer: '스크립트', ...obs(`같은 출처에서 스크립트 ${main.scripts.length}개가 실렸다. 파일 이름 예: ${names}`, E) });
  }
  if (main.storage) {
    const parts = [];
    if (main.storage.local.length) parts.push(`localStorage 키 이름 ${main.storage.local.join(', ')}`);
    if (main.storage.session.length) parts.push(`sessionStorage 키 이름 ${main.storage.session.join(', ')}`);
    if (main.storage.idb.length) parts.push(`IndexedDB 이름 ${main.storage.idb.join(', ')}`);
    if (parts.length) tech.push({ layer: '브라우저 저장소', ...obs(`${parts.join('. ')}. 값은 읽지 않았다.`, E) });
  }
  const res = Object.entries(main.resources);
  if (res.length) tech.push({ layer: '실린 자원', ...obs(`같은 출처 자원 종류: ${res.map(([k, v]) => `${k} ${v}개`).join(', ')}`, E) });
  for (const [i, { b }] of bundles.entries()) {
    if (b.routes.length) tech.push({ layer: '경로 후보', ...trace(`스크립트 글자 안에 경로 모양이 보인다: ${b.routes.slice(0, 14).join(', ')}. 열어 보지는 않았다.`, bundleEv[i]) });
    const codes = uniq(b.unknowns.map((u) => (u.match(/\(([a-z_]+)\)/) || [])[1]).filter(Boolean));
    if (b.scripts > b.parsed) tech.push({ layer: '읽지 못한 스크립트', ...unk(`스크립트 ${b.scripts}개 가운데 ${b.scripts - b.parsed}개는 정적 분석이 끝나지 않았다${codes.length ? ` (REA 가 적은 사유: ${codes.join(', ')})` : ''}. 그 안의 경로와 호출은 모른다.`) });
  }
  if (html) {
    const keys = Object.keys(html.metas);
    const og = keys.filter((k) => k.startsWith('og:') || k.startsWith('twitter:'));
    tech.push({ layer: '머리말 메타', ...obs(`HTML 머리말에 메타 ${keys.length}개 (공유용 ${og.length}개), JSON-LD ${html.ld.length}건${html.ld.length ? ` (${uniq(html.ld.map((j) => j.type)).join(', ')})` : ''}. lang=${html.lang || '없음'}`, htmlEv) });
  }
  const ext = main.excluded.filter((e) => e.reason === 'disallowed_origin');
  if (ext.length) tech.push({ layer: '다른 출처', ...unk(`REA 가 기록에서 뺀 다른 출처 항목: ${ext.map((e) => `${e.section} ${e.count}개`).join(', ')}. 어느 서비스의 것인지는 모른다.`) });
  // 정밀 모드의 기록: 흐름에서 본 바깥 서비스, 코드에서만 본 이름
  const mainHost = (() => { try { return new URL(main.url).hostname; } catch { return ''; } })();
  const services = [];
  flowFiles.forEach(({ j }, i) => {
    const groups = classifyHosts(j.hosts.map((h) => ({ host: h.host, sent: h.sent })), mainHost);
    const named = groups.filter((g) => g.kind !== 'other');
    if (groups.length) tech.push({ layer: '바깥 서비스', ...obs(`페이지가 요청을 보내려던 바깥 호스트 ${groups.reduce((n, g) => n + g.hosts.length, 0)}곳${named.length ? `: ${named.slice(0, 10).map((g) => `${SERVICE_KINDS[g.kind]} ${g.name}`).join(', ')}` : ''}. 호스트 이름만 적었고 주고받은 내용은 보지 않았다.`, flowEv[i]) });
    for (const k of ['payment', 'analytics', 'video', 'auth', 'data', 'chat']) { const names = groups.filter((g) => g.kind === k).map((g) => g.name); if (names.length) services.push({ kind: k, label: SERVICE_KINDS[k], names, seen: 'flow', evidence: [flowEv[i]] }); }
  });
  const shownPaths = new Set(inspects.flatMap(({ page }) => [(() => { try { return new URL(page.url).pathname; } catch { return ''; } })()]));
  const codeRoutes = uniq([...bundles.flatMap(({ b }) => b.routes), ...scanFiles.flatMap(({ j }) => j.routes)]).filter((r) => r !== '/' && !shownPaths.has(r));
  const codeEv = scanEv[0] || bundleEv[0] || null;
  scanFiles.forEach(({ j }, i) => {
    if ((j.payments || []).length) { tech.push({ layer: '결제 모듈', ...trace(`코드 안에 결제 모듈 이름이 보인다: ${j.payments.map(scrub).join(', ')}. 실제로 그 결제사로 결제되는지는 결제 화면을 열지 않아 모른다.`, scanEv[i]) }); const names = j.payments.map(scrub).filter((n) => !services.some((x) => x.kind === 'payment' && x.names.includes(n))); if (names.length) services.push({ kind: 'payment', label: SERVICE_KINDS.payment, names, seen: 'code', evidence: [scanEv[i]] }); }
    if ((j.endpoints || []).length) tech.push({ layer: '서버 호출 이름', ...trace(`코드 안에 서버 호출 주소처럼 보이는 이름이 ${j.endpoints.length}개 있다 (예: ${j.endpoints.slice(0, 4).map((x) => short(scrub(x), 28)).join(', ')}). 하나도 불러 보지 않았다.`, scanEv[i]) });
    if ((j.prices || []).length) price.push(trace(`코드 안에 가격처럼 보이는 숫자나 글자가 있다: ${j.prices.slice(0, 6).map((x) => quote(String(x))).join(', ')}. 화면에서 같은 값을 봤는지 견주어 보고, 못 봤으면 지금 파는 가격이라고 쓰지 않는다.`, scanEv[i]));
    if ((j.plans || []).length) tech.push({ layer: '요금제 이름', ...trace(`코드 안에 요금제나 상품 이름처럼 보이는 글자가 있다: ${j.plans.slice(0, 6).map((x) => quote(String(x))).join(', ')}. 지금 파는 것인지는 화면에서 확인되지 않았다.`, scanEv[i]) });
  });
  if (codeEv) for (const r of codeRoutes.slice(0, 14)) screens.push({ name: short(scrub(r), 48), purpose: looksBehindLogin(r) ? '코드에서만 이름이 보인 화면. 로그인이나 결제 뒤로 보이는 경로다. 열어 보지 않았다.' : '코드에서만 이름이 보인 화면. 화면에서 링크로 이어지는지는 사람이 확인한다. 열어 보지 않았다.', features: [], status: 'code', evidence: [codeEv] });
  tech.push({ layer: '서버', ...unk('서버 쪽 구성과 데이터 저장 방식은 밖에서 보이지 않는다.') });

  // 5번 칸
  const unknowns = [
    { question: '누가 사는가', why: '페이지 문구만으로 고객을 정하지 않았다. 초안은 본 것만 옮긴다.', next: '페이지가 직접 말하는 대상 문구를 근거로 붙여 사람이 채운다.' },
    { question: '어떤 문제를 푸는가', why: '초안은 해석을 하지 않는다.', next: '소개 문단을 읽고 내 말로 한 줄 쓴다.' },
    { question: '매출, 구매자 수, 전환율', why: '공개된 숫자를 찾지 못했다.', next: '대상이 직접 공개한 자료가 있을 때만 적는다. 없으면 비워 둔다.' },
    { question: '가입과 결제 뒤 화면', why: '로그인과 결제 뒤는 열지 않는다.', next: '공개 도움말이나 대상이 공개한 영상이 있으면 그것만 본다.' },
  ];
  if (main.limitations.some((l) => /prior network/i.test(l))) unknowns.push({ question: '페이지가 처음 뜰 때 오간 요청', why: 'REA 는 붙은 뒤의 요청만 기록한다. 붙기 전 요청은 기록에 없다.', next: 'REA 를 먼저 붙인 뒤 페이지를 다시 여는 방법이 있으나, 요청 수 한도 안에서만 한다.' });
  if (!robots) unknowns.push({ question: '이용약관과 robots.txt', why: '초안을 만들 때 받지 않았다.', next: '다른 페이지를 보기 전에 먼저 읽고 meta.terms 에 적는다.' });

  // meta
  const methods = uniq([
    ...inspects.map(() => 'REA inspect-web-page (접근성 글자, 구조, 저장소 키 이름)'),
    ...others.filter((x) => x.kind === 'shot').map(() => 'REA capture-web-screenshot (보이는 화면 한 장)'),
    ...bundles.map(() => 'REA analyze-web-bundle (스크립트를 실행 없이 읽기)'),
    html ? '공개 HTML 한 장 (머리말 메타 보충)' : '',
    robots ? 'robots.txt 읽기' : '',
    'from-rea.mjs 로 초안 만들기',
  ].filter(Boolean));
  const report = {
    schema: 'rebiz/report@1',
    meta: {
      target: { name: scrub(name) || main.title || main.url, kind: 'web-service', url: main.url, relation },
      analyzed_at: seen,
      analyst: 'from-rea 초안 (사람이나 에이전트가 완성한다)',
      depth: {
        mode: 'precise', reached: codeEv ? 'code' : flowFiles.length ? 'flow' : 'surface',
        steps: [
          { key: 'surface', state: 'done', note: `REA inspect-web-page 로 공개 페이지 ${inspects.length}개의 글과 구조를 읽음` },
          { key: 'flow', state: flowFiles.length ? 'done' : 'skipped', note: flowFiles.length ? `흐름 읽기 기록 ${flowFiles.length}개 (펼치기 ${flowFiles.reduce((n, x) => n + (x.j.clicks || 0), 0)}번)` : '흐름 읽기 기록을 받지 않았다. REA 는 페이지를 누르지 않는다' },
          { key: 'code', state: codeEv ? (bundles.some(({ b }) => b.scripts > b.parsed) ? 'partial' : 'done') : 'skipped', note: codeEv ? `코드에서 화면 경로 이름 ${codeRoutes.length}개${bundles.some(({ b }) => b.scripts > b.parsed) ? '. 일부 스크립트는 분석이 끝나지 않았다' : ''}` : '속 읽기 기록(analyze-web-bundle 근거나 04_code_scan.json)을 받지 않았다' },
        ],
      },
      scope: `공개 페이지 ${inspects.length}개를 REA 로 읽었다. 로그인, 결제, 잠긴 화면은 보지 않았다.`,
      method: methods,
      terms: {
        status: robots ? 'checked' : 'not-found',
        note: robots
          ? `robots.txt: Allow ${robots.allow.join(' ') || '없음'}, Disallow ${robots.disallow.join(' ') || '없음'}. ${termsPage ? '이용약관 페이지를 받아 두었다. 자동 열람과 복제에 관한 조항은 사람이 읽고 여기에 덧붙인다.' : '이용약관은 아직 읽지 않았다. 읽고 여기에 덧붙인다.'}`
          : '초안: 이용약관과 robots.txt 를 아직 확인하지 않았다.',
        evidence: [robotsEv, termsPage ? pageEv.get(termsPage) : null].filter(Boolean),
      },
      one_line: '',
    },
    evidence,
    sections: {
      money: {
        customer: [unk('누가 사는지는 아직 읽지 않았다. 사람이 채운다.')],
        problem: [unk('어떤 문제를 푸는지는 아직 읽지 않았다. 사람이 채운다.')],
        price,
        revenue: [],
      },
      flow: { steps, ...(services.length ? { services } : {}) },
      map: { screens },
      tech: { items: tech },
      unknowns,
      my_version: { working_name: '', same_problem: '', who: '', mvp: [], differences: [{ title: '', text: '' }, { title: '', text: '' }, { title: '', text: '' }], not_taken: [] },
    },
  };

  // 원본에서 모은 글 묶음: check-clone 의 입력. 리포트에는 들어가지 않는다.
  let host = '';
  try { host = new URL(main.url).hostname; } catch { /* 주소 없음 */ }
  const bare = host.replace(/^www\./, '');
  const nameGuess = uniq([
    ...main.title.split(/[|·\-–:]/).map((s) => s.trim()),
    html ? html.metas['og:site_name'] || '' : '',
    html ? html.metas['application-name'] || '' : '',
    ...brands,
  ].filter((s) => s && s.length >= 3));
  const source = {
    schema: 'rebiz/source@1',
    note: '원본에서 모은 글과 자원 주소. 내 버전과 겹치는지 보는 데만 쓴다. 다른 곳에 올리지 않는다.',
    url: main.url,
    brand: { names: nameGuess, domains: uniq([host, bare, bare.split('.')[0]].filter((s) => s && s.length >= 3)) },
    texts: uniq([...inspects.flatMap(({ page }) => page.lines), ...(html ? html.bodyLines : []), ...(html ? Object.entries(html.metas).filter(([k]) => HUMAN_META.test(k)).map(([, v]) => v) : [])].map(scrub).filter((t) => t.length >= 2)),
    assets: uniq([...inspects.flatMap(({ page }) => page.assets), ...(html ? html.assets : [])]),
  };
  return { report, source, stats: { pages: inspects.length, lines: source.texts.length, assets: source.assets.length, dropped: [...dropped], hasText: main.hasText } };
}

function parseArgs(argv) {
  const o = { files: [], shots: [], brands: [], relation: 'third-party', out: 'report.draft.json', sourceOut: '' };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => String(argv[++i] ?? '');
    if (a === '--html') o.html = next();
    else if (a === '--robots') o.robots = next();
    else if (a === '--shot') o.shots.push(next());
    else if (a === '--relation') o.relation = next();
    else if (a === '--name') o.name = next();
    else if (a === '--brand') o.brands.push(next());
    else if (a === '--out') o.out = next();
    else if (a === '--source-out') o.sourceOut = next();
    else if (a === '--base') o.base = next();
    else if (a === '--force') o.force = true;
    else if (a === '--help' || a === '-h') o.help = true;
    else if (a.startsWith('--')) { o.bad = a; }
    else o.files.push(a);
  }
  return o;
}

async function main() {
  const o = parseArgs(process.argv.slice(2));
  if (o.help || o.bad || !o.files.length) {
    if (o.bad) console.error(`모르는 옵션: ${o.bad}`);
    console.error('사용: node from-rea.mjs <REA Evidence JSON ...> [--html 파일] [--robots 파일] [--shot png] [--relation third-party|own] [--name 이름] [--brand 이름] [--out report.draft.json] [--source-out source.json] [--force]');
    process.exit(o.help ? 0 : 2);
  }
  if (!['own', 'third-party'].includes(o.relation)) { console.error('--relation 은 own 또는 third-party'); process.exit(2); }
  const out = path.resolve(o.out);
  const base = path.resolve(o.base || path.dirname(out));
  const sourceOut = path.resolve(o.sourceOut || path.join(path.dirname(out), 'source.json'));
  for (const f of [out, sourceOut]) {
    if (fs.existsSync(f) && !o.force) { console.error(`이미 있어요: ${path.basename(f)}. 덮어쓰려면 --force`); process.exit(2); }
  }
  let built;
  try {
    built = buildDraft({ evidenceFiles: o.files.map((f) => path.resolve(f)), htmlFile: o.html && path.resolve(o.html), robotsFile: o.robots && path.resolve(o.robots), shots: o.shots.map((s) => path.resolve(s)), relation: o.relation, name: o.name, brands: o.brands, base });
  } catch (e) { console.error(`만들지 못했어요: ${e.message}`); process.exit(1); }
  const { report, source, stats } = built;
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.mkdirSync(path.dirname(sourceOut), { recursive: true });
  fs.writeFileSync(out, JSON.stringify(report, null, 2) + '\n');
  fs.writeFileSync(sourceOut, JSON.stringify(source, null, 2) + '\n');

  const { checkReport } = await import(pathToFileURL(path.join(HERE, 'check-report.mjs')).href);
  const { errors, counts } = checkReport(report);
  console.log(`초안: ${path.relative(process.cwd(), out) || out}`);
  console.log(`원본 글 묶음: ${path.relative(process.cwd(), sourceOut) || sourceOut}  (글 ${stats.lines}줄, 자원 주소 ${stats.assets}개. 겹침 검사에만 쓴다)`);
  console.log(`읽은 페이지 ${stats.pages}개 · 근거 ${report.evidence.length}개 · 관찰 ${counts.observed} · 추정 ${counts.inferred} · 모름 ${counts.unknown}`);
  if (!stats.hasText) console.log('알림  접근성 글자가 없는 Evidence 예요. inspect-web-page 에 --include-accessibility-text 를 주고 다시 받으면 제목과 가격 문구가 채워져요.');
  if (stats.dropped.length) console.log(`가림  비밀 값이 실릴 수 있는 키를 버렸어요: ${stats.dropped.join(', ')}`);
  console.log(`남은 일 ${errors.length}개 (검사기가 알려 주는 빈칸):`);
  for (const e of errors) console.log(`  - ${e}`);
  console.log('초안은 본 것만 옮긴 것이에요. 고객, 문제, 첫 가치, 내 버전 명세는 스킬 절차대로 채워 주세요.');
}

// 바로 실행했을 때만 돈다. 경로에 심볼릭 링크가 끼어 있어도 알아보도록 실제 경로로 견준다.
const direct = (() => { try { return fs.realpathSync(process.argv[1]) === fs.realpathSync(fileURLToPath(import.meta.url)); } catch { return false; } })();
if (direct) await main();
