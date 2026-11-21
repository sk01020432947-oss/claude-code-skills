#!/usr/bin/env node
// 배운 뼈대를 이미 있는 내 프로젝트의 첫 화면과 견주어 빈칸 목록을 만든다. 의존성 없음.
// 사용: node apply-plan.mjs <report.json> --to <내 프로젝트 폴더> [--page <파일>] [--url http://localhost:3000]
//
// 하는 일: 내 첫 화면을 수집기와 같은 구역 분류로 읽고, 리포트의 뼈대(구역 종류와 순서)와 견준다.
//   - 대상에는 있는데 내 것에는 없는 구역 (빈칸)
//   - 둘 다 있지만 순서가 다른 구역
// 결과는 <내 프로젝트 폴더>/rebiz-apply/plan.md 와 plan.json 에 남긴다. 코드는 고치지 않는다.
// 읽는 곳: 내 컴퓨터의 파일, 또는 내 컴퓨터 주소(localhost, 127.0.0.1)뿐이다. 바깥 주소는 받지 않는다.
// 계획에는 대상의 문구가 들어가지 않는다. 구역은 종류 이름(이 도구의 말)과 리포트에 내 말로 붙인 이름으로만 적는다.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { readPage } from './collect.mjs';
import { findBrowser, openRenderer } from './render.mjs';
import { KINDS, kindName, kindWrite, roleName, targetNames, nameProblem } from './kinds.mjs';

export const PLAN_DIR = 'rebiz-apply';
const PAGE_TRIES = ['index.html', 'index.htm', 'public/index.html', 'docs/index.html', 'site/index.html', 'www/index.html', 'src/index.html'];
const FRAMEWORKS = [['next', 'Next.js'], ['nuxt', 'Nuxt'], ['astro', 'Astro'], ['@sveltejs/kit', 'SvelteKit'], ['svelte', 'Svelte'], ['@remix-run/react', 'Remix'], ['gatsby', 'Gatsby'], ['vue', 'Vue'], ['react', 'React'], ['vite', 'Vite']];
const SOURCE_TRIES = ['app/page.tsx', 'app/page.jsx', 'app/page.js', 'src/app/page.tsx', 'src/app/page.jsx', 'pages/index.tsx', 'pages/index.jsx', 'pages/index.js', 'src/pages/index.tsx', 'src/pages/index.jsx', 'src/pages/index.astro', 'src/routes/+page.svelte', 'pages/index.vue', 'src/App.tsx', 'src/App.jsx', 'src/App.vue', 'src/App.svelte'];

const isObj = (v) => v && typeof v === 'object' && !Array.isArray(v);
const str = (v) => (typeof v === 'string' ? v.trim() : '');
const arr = (v) => (Array.isArray(v) ? v : []);
const isFile = (p) => { try { return fs.statSync(p).isFile(); } catch { return false; } };
const posix = (p) => p.split(path.sep).join('/');

export class PlanStop extends Error {
  constructor(code, message, extra = {}) { super(message); this.code = code; Object.assign(this, extra); }
}

// 내 컴퓨터 주소인지: localhost, 127.x.x.x, [::1], 그리고 *.localhost
export function isLocalUrl(input) {
  let u;
  try { u = new URL(String(input)); } catch { return false; }
  if (!/^https?:$/.test(u.protocol) || u.username || u.password) return false;
  const h = u.hostname.toLowerCase();
  return h === 'localhost' || h.endsWith('.localhost') || /^127(\.\d{1,3}){3}$/.test(h) || h === '[::1]' || h === '::1';
}

// 프로젝트가 어떤 틀로 만들어졌는지 package.json 의 이름만 보고 짐작한다.
export function guessFramework(root) {
  try {
    const pkg = JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf8'));
    const deps = { ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}) };
    const hit = FRAMEWORKS.find(([name]) => name in deps);
    return hit ? hit[1] : '';
  } catch { return ''; }
}

// 첫 화면 파일을 찾는다. page 를 주면 그 파일만 본다 (프로젝트 폴더 안이어야 한다).
export function findFirstPage(root, { page = '' } = {}) {
  if (page) {
    const file = path.resolve(root, page);
    if (file !== root && !file.startsWith(root + path.sep)) throw new PlanStop('page-outside', `--page 는 프로젝트 폴더 안의 파일이어야 해요: ${page}`);
    if (!isFile(file)) throw new PlanStop('page-missing', `--page 파일을 찾지 못했어요: ${page}`);
    return { file, rel: posix(path.relative(root, file)), given: true };
  }
  const rel = PAGE_TRIES.find((f) => isFile(path.join(root, f)));
  return rel ? { file: path.join(root, rel), rel, given: false } : null;
}

// 내 첫 화면을 읽어 구역으로 나눈다. 돌려주는 것: { blocks, how, ref, measured, textLength, exact }
export async function readMine(root, { page = '', url = '', render = 'auto', browser } = {}) {
  if (url) {
    if (!isLocalUrl(url)) throw new PlanStop('url-not-local', '--url 은 내 컴퓨터 주소만 받아요 (http://localhost:포트, http://127.0.0.1:포트). 바깥 주소는 rebiz <주소> 로 해부하세요.');
    const u = new URL(url);
    const found = render === 'off' ? null : (browser === undefined ? findBrowser() : browser);
    if (found) {
      const renderer = await openRenderer({ browser: found });
      try {
        // 브라우저 안에서 나가는 요청도 내 컴퓨터 주소로만 보낸다.
        const r = await renderer.render(u.href, { allow: async (reqUrl) => (isLocalUrl(reqUrl) ? { ok: true, sameSite: true } : { ok: false, why: '내 컴퓨터 밖 주소' }) });
        if (!r.html) throw new PlanStop('url-unreachable', `주소를 열지 못했어요: ${u.origin}${u.pathname}. 개발 서버가 떠 있는지 확인하세요.`);
        const p = readPage(r.html, u.href, { rects: r.blocks });
        return { blocks: p.skeleton, how: 'url-rendered', ref: `${u.origin}${u.pathname}`, measured: p.measured, textLength: p.textLength, exact: true, blockedOutside: r.stats.blocked };
      } finally { await renderer.close(); }
    }
    let res;
    try { res = await fetch(u.href, { redirect: 'manual', headers: { accept: 'text/html' } }); } catch { throw new PlanStop('url-unreachable', `주소를 열지 못했어요: ${u.origin}${u.pathname}. 개발 서버가 떠 있는지 확인하세요.`); }
    if (res.status >= 300 && res.status < 400) throw new PlanStop('url-redirect', `주소가 다른 곳으로 넘깁니다 (${res.status}). 넘어간 뒤의 주소를 --url 로 주세요.`);
    if (!res.ok) throw new PlanStop('url-unreachable', `주소가 ${res.status} 를 돌려줬어요: ${u.origin}${u.pathname}`);
    const p = readPage(await res.text(), u.href);
    return { blocks: p.skeleton, how: 'url-html', ref: `${u.origin}${u.pathname}`, measured: false, textLength: p.textLength, exact: true, scripts: p.counts.scriptTags };
  }
  const found = findFirstPage(root, { page });
  if (!found) {
    const fw = guessFramework(root);
    const hints = SOURCE_TRIES.filter((f) => isFile(path.join(root, f))).slice(0, 3);
    throw new PlanStop('no-page', fw ? `첫 화면의 정적 HTML 파일을 찾지 못했어요. ${fw} 프로젝트로 보입니다.` : '첫 화면의 정적 HTML 파일(index.html)을 찾지 못했어요.', { framework: fw, hints });
  }
  const html = fs.readFileSync(found.file, 'utf8');
  const p = readPage(html, pathToFileURL(found.file).href);
  const isHtml = /\.html?$/i.test(found.file);
  // 스크립트가 화면을 그리는 껍데기 HTML: 글이 거의 없고 스크립트만 있다.
  if (isHtml && !found.given && p.textLength < 80 && p.counts.scriptTags > 0) {
    const fw = guessFramework(root);
    throw new PlanStop('shell-page', `${found.rel} 은 스크립트가 화면을 그리는 껍데기라서 구역을 읽을 수 없어요${fw ? ` (${fw} 프로젝트로 보입니다)` : ''}.`, { framework: fw, hints: SOURCE_TRIES.filter((f) => isFile(path.join(root, f))).slice(0, 3), page: found.rel });
  }
  return { blocks: p.skeleton, how: isHtml ? 'file' : 'source-file', ref: found.rel, measured: false, textLength: p.textLength, exact: isHtml };
}

// 리포트의 뼈대에서 견줄 구역을 뽑는다. 이름은 리포트에 내 말로 붙인 것만, 대상의 이름이 섞였으면 종류 이름으로 바꾼다.
export function targetBlocks(report, source = null) {
  const names = targetNames(report, source);
  return arr(report && report.skeleton && report.skeleton.blocks).filter(isObj).map((b, i) => {
    const kind = KINDS.includes(b.kind) ? b.kind : 'text';
    const own = str(b.name);
    return { n: i + 1, kind, role: str(b.role) || 'other', name: own && !nameProblem(own, names) ? own : kindName(kind), taken: b.taken !== false };
  });
}

// 두 구역 순서를 견준다. 같은 종류끼리 순서를 지키며 짝을 짓고(가장 긴 공통 순서), 남은 것은 순서가 다른 곳과 빈칸으로 나눈다.
export function comparePlan(target, mine) {
  const T = target.filter((b) => b.taken);
  const M = mine.map((b, j) => ({ n: j + 1, kind: KINDS.includes(b.kind) ? b.kind : 'text', role: b.role || 'other', name: kindName(b.kind) }));
  const dp = Array.from({ length: T.length + 1 }, () => new Array(M.length + 1).fill(0));
  for (let i = T.length - 1; i >= 0; i -= 1) for (let j = M.length - 1; j >= 0; j -= 1) dp[i][j] = T[i].kind === M[j].kind ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
  const pair = new Map(); // 대상 구역 -> 내 구역
  const usedM = new Set();
  for (let i = 0, j = 0; i < T.length && j < M.length;) {
    if (T[i].kind === M[j].kind) { pair.set(T[i], { m: M[j], state: 'same' }); usedM.add(M[j]); i += 1; j += 1; } else if (dp[i + 1][j] >= dp[i][j + 1]) i += 1; else j += 1;
  }
  for (const t of T) {
    if (pair.has(t)) continue;
    const m = M.find((x) => x.kind === t.kind && !usedM.has(x));
    if (m) { pair.set(t, { m, state: 'moved' }); usedM.add(m); }
  }
  const rows = [];
  let anchor = null; // 바로 앞에서 제자리에 짝지어진 내 구역
  for (const t of target) {
    if (!t.taken) { rows.push({ target: t, state: 'not-taken', mine: null, after: null }); continue; }
    const p = pair.get(t);
    if (p && p.state === 'same') { rows.push({ target: t, state: 'same', mine: p.m, after: null }); anchor = p.m; } else if (p) rows.push({ target: t, state: 'moved', mine: p.m, after: anchor });
    else rows.push({ target: t, state: 'missing', mine: null, after: anchor });
  }
  const extra = M.filter((m) => !usedM.has(m));
  const count = (s) => rows.filter((r) => r.state === s).length;
  return { rows, extra, mine: M, counts: { target: T.length, mine: M.length, same: count('same'), moved: count('moved'), missing: count('missing'), notTaken: count('not-taken'), extra: extra.length } };
}

const STATE = { same: '있음', moved: '순서 다름', missing: '없음', 'not-taken': '가져오지 않음' };
const HOW = { file: '내 컴퓨터의 HTML 파일을 읽음', 'source-file': '소스 파일을 글자로만 읽음 (어림입니다. 정확히 보려면 --url 로 내 개발 서버 주소를 주세요)', 'url-rendered': '내 컴퓨터 주소를 브라우저로 그려서 읽음', 'url-html': '내 컴퓨터 주소에서 받은 HTML 을 읽음' };
const where = (r) => (r.after ? `내 ${r.after.n}번째 구역(${r.after.name}) 다음` : '맨 위');
export const stateName = (s) => STATE[s] || s;
export const howName = (h) => HOW[h] || h;

// 사람이 읽는 계획. 절대 경로, 대상의 주소와 문구는 넣지 않는다.
export function planMarkdown(plan) {
  const { cmp } = plan;
  const missing = cmp.rows.filter((r) => r.state === 'missing');
  const moved = cmp.rows.filter((r) => r.state === 'moved');
  const L = [];
  L.push('# 적용 계획: 배운 뼈대와 내 첫 화면', '');
  L.push(`- 만든 때: ${plan.made_at} (rebiz ${plan.tool})`);
  L.push(`- 리포트: ${plan.report}`);
  L.push(`- 내 첫 화면: ${plan.page.ref}`);
  L.push(`- 읽은 방식: ${howName(plan.page.how)}`);
  L.push(`- 견준 결과: 배운 구역 ${cmp.counts.target}개 가운데 있음 ${cmp.counts.same}, 순서 다름 ${cmp.counts.moved}, 없음 ${cmp.counts.missing}. 내 구역은 ${cmp.counts.mine}개.`, '');
  L.push('구역의 종류와 층은 규칙으로 붙인 추정입니다. 틀린 곳이 있으면 화면을 직접 보고 이 계획을 고쳐 쓰세요.', '');
  L.push(`## 빈칸: 배운 뼈대에는 있는데 내 첫 화면에는 없는 구역 ${missing.length}곳`, '');
  if (!missing.length) L.push('없습니다.', '');
  missing.forEach((r, i) => {
    L.push(`${i + 1}. **${r.target.name}** (${kindName(r.target.kind)}, ${roleName(r.target.role)})`);
    L.push(`   - 넣을 자리: ${where(r)}`);
    L.push(`   - 쓸 것: ${kindWrite(r.target.kind)}`);
  });
  if (missing.length) L.push('');
  L.push(`## 순서가 다른 곳 ${moved.length}곳`, '');
  if (!moved.length) L.push('없습니다.', '');
  moved.forEach((r, i) => {
    L.push(`${i + 1}. **${r.target.name}** (${kindName(r.target.kind)}): 지금은 내 ${r.mine.n}번째 구역입니다. 배운 순서로는 ${where(r)}에 옵니다.`);
  });
  if (moved.length) L.push('', '순서는 꼭 맞출 필요가 없습니다. 내 이야기의 흐름에 맞을 때만 옮깁니다.', '');
  L.push('## 견준 표', '', '| 배운 순서 | 배운 구역 | 종류 | 층 | 내 첫 화면 | 상태 |', '|---|---|---|---|---|---|');
  for (const r of cmp.rows) L.push(`| ${r.target.n} | ${r.target.name.replace(/\|/g, '/')} | ${kindName(r.target.kind)} | ${roleName(r.target.role)} | ${r.mine ? `${r.mine.n}번째 (${r.mine.name})` : ''} | ${stateName(r.state)} |`);
  L.push('');
  if (cmp.extra.length) {
    L.push('## 내 첫 화면에만 있는 구역', '');
    for (const m of cmp.extra) L.push(`- ${m.n}번째: ${m.name}`);
    L.push('', '그대로 둡니다. 배운 뼈대에 없다고 지우지 않습니다.', '');
  }
  L.push('## 지킬 것', '');
  L.push('- 새 구역의 문구, 이름, 그림, 색은 내 것으로 새로 씁니다. 다른 사이트의 글과 그림을 옮기지 않습니다.');
  L.push('- 가격, 숫자, 후기는 지어내지 않습니다. 아직 없으면 "여기에 쓸 것" 자리로 남깁니다.');
  L.push('- 이 프로젝트의 지금 디자인(색, 글꼴, 클래스 이름을 붙이는 방식)을 따릅니다.');
  L.push('- 새 브랜치에서만 고칩니다. 커밋, push, 배포는 사람이 바뀐 것을 본 뒤에 합니다.', '');
  return `${L.join('\n')}`;
}

// 계획을 만든다 (파일은 쓰지 않는다).
export async function makePlan(reportPath, root, { page = '', url = '', render = 'auto', browser, version = '0', source = null, today = new Date().toISOString().slice(0, 10) } = {}) {
  const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
  const target = targetBlocks(report, source);
  if (!target.filter((b) => b.taken).length) throw new PlanStop('no-skeleton', '리포트에 배운 뼈대(skeleton.blocks)가 없어요. rebiz <주소> 로 해부한 리포트이거나, 스킬 3단계의 뼈대를 적은 리포트여야 합니다.');
  const abs = path.resolve(root);
  if (!fs.existsSync(abs) || !fs.statSync(abs).isDirectory()) throw new PlanStop('no-project', `프로젝트 폴더를 찾지 못했어요: ${root}`);
  const mine = await readMine(abs, { page, url, render, browser });
  const cmp = comparePlan(target, mine.blocks);
  const rel = path.relative(abs, path.resolve(reportPath));
  return {
    schema: 'rebiz/apply-plan@1', made_at: today, tool: version,
    report: rel && !rel.startsWith('..') && !path.isAbsolute(rel) ? posix(rel) : path.basename(reportPath),
    page: { ref: mine.ref, how: mine.how, measured: mine.measured, exact: mine.exact, text_length: mine.textLength },
    cmp,
  };
}

// 계획을 프로젝트 폴더의 rebiz-apply/ 에 쓴다.
export function writePlan(root, plan) {
  const dir = path.join(path.resolve(root), PLAN_DIR);
  fs.mkdirSync(dir, { recursive: true });
  const md = path.join(dir, 'plan.md');
  const json = path.join(dir, 'plan.json');
  const row = (r) => ({ order: r.target.n, name: r.target.name, kind: r.target.kind, role: r.target.role, state: r.state, mine: r.mine ? r.mine.n : null, after: r.after ? r.after.n : null, write: r.state === 'missing' ? kindWrite(r.target.kind) : '' });
  fs.writeFileSync(md, planMarkdown(plan));
  fs.writeFileSync(json, `${JSON.stringify({ schema: plan.schema, made_at: plan.made_at, tool: plan.tool, report: plan.report, page: plan.page, counts: plan.cmp.counts, rows: plan.cmp.rows.map(row), mine: plan.cmp.mine, extra: plan.cmp.extra.map((m) => m.n) }, null, 2)}\n`);
  return { dir, md, json };
}

async function main() {
  const args = process.argv.slice(2);
  const o = {};
  for (let i = 0; i < args.length; i += 1) {
    const a = args[i];
    if (a === '--to') o.to = args[++i];
    else if (a === '--page') o.page = args[++i];
    else if (a === '--url') o.url = args[++i];
    else if (a === '--no-render') o.render = 'off';
    else if (!a.startsWith('--') && !o.file) o.file = a;
    else o.bad = a;
  }
  const usage = '사용: node apply-plan.mjs <report.json> --to <내 프로젝트 폴더> [--page <파일>] [--url http://localhost:3000]';
  if (o.bad || !o.file || !o.to) { if (o.bad) console.error(`모르는 인자: ${o.bad}`); console.error(usage); process.exit(2); }
  let plan;
  try { plan = await makePlan(o.file, o.to, { page: o.page, url: o.url, render: o.render }); } catch (e) {
    console.error(`계획을 만들지 못했어요: ${e.message}`);
    if (e.code === 'no-page' || e.code === 'shell-page') console.error('첫 화면 파일을 --page 로 알려 주거나, 개발 서버를 띄우고 --url http://localhost:포트 를 주세요.');
    process.exit(e instanceof PlanStop ? 2 : 1);
  }
  const out = writePlan(o.to, plan);
  const c = plan.cmp.counts;
  console.log(`배운 구역 ${c.target}개: 있음 ${c.same}, 순서 다름 ${c.moved}, 없음 ${c.missing}`);
  console.log(`계획: ${out.md}`);
}

// 바로 실행했을 때만 돈다. 경로에 심볼릭 링크가 끼어 있어도 알아보도록 실제 경로로 견준다.
const direct = (() => { try { return fs.realpathSync(process.argv[1]) === fs.realpathSync(fileURLToPath(import.meta.url)); } catch { return false; } })();
if (direct) await main();
