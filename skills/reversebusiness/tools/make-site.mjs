#!/usr/bin/env node
// 리포트의 6번 칸(내 버전 명세)과 배운 구역의 순서, 짜임만 보고 새 정적 사이트의 출발점을 만든다. 의존성 없음.
// 사용: node make-site.mjs <report.json> [--out <폴더>] [--topic "내 사업 주제"] [--force]
//
// 만드는 것: index.html 과 style.css 두 파일. 바깥 글꼴, 스크립트, 그림을 부르지 않아 바로 열린다.
// 쓰는 재료: 6번 칸에 내 말로 쓴 명세, 뼈대의 구역 종류와 순서, 그리고 이 도구의 안내 문구와 중립 디자인뿐이다.
// 쓰지 않는 것: 대상의 문구, 이미지, 이름, 색, 로고. 뼈대에 붙인 구역 이름도 쓰지 않는다(종류만 쓴다).
// 문구 자리는 "여기에 무엇을 쓸지" 안내로 채운다. 가격, 숫자, 후기는 지어내지 않고 빈자리로 둔다.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { checkReport } from './check-report.mjs';
import { checkClone, loadSource } from './check-clone.mjs';
import { KINDS, kindName, kindWrite, roleName, targetNames, nameProblem } from './kinds.mjs';

export const GENERATOR = 'rebiz build';
const DEFAULT_ORDER = ['nav', 'headline', 'list', 'price', 'faq', 'cta', 'footer'];
const NAV_WORD = { headline: '소개', media: '소개', price: '가격', numbers: '숫자', list: '구성', notice: '안내', quotes: '받은 말', faq: '물음', cta: '신청', text: '이야기' };
const ROLES = ['attract', 'value', 'pay', 'return', 'other'];

const isObj = (v) => v && typeof v === 'object' && !Array.isArray(v);
const str = (v) => (typeof v === 'string' ? v.trim() : '');
const arr = (v) => (Array.isArray(v) ? v : []);
const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const two = (n) => String(n).padStart(2, '0');

// 리포트 옆의 원본 글 묶음을 찾는다 (rebiz <주소> 가 남긴 source.json). 없으면 null.
export function findSource(reportPath) {
  const dir = path.dirname(path.resolve(reportPath));
  const file = [path.join(dir, 'source.json'), path.join(dir, 'evidence', 'source.json')].find((f) => fs.existsSync(f));
  if (!file) return null;
  try { return { file, source: loadSource({ sources: [file] }) }; } catch { return null; }
}

// 6번 칸이 쓸 만한지 본다. blank: 비어 있음, errors: 고칠 곳.
export function specState(report) {
  const { errors, myVersion } = checkReport(report);
  const mine = errors.filter((e) => /my_version/.test(e));
  return { blank: myVersion === 'empty', errors: mine };
}

// 뼈대에서 만들 구역을 고른다: 가져오지 않기로 한 구역은 빼고, 종류와 층만 남긴다.
export function planBlocks(report) {
  const blocks = arr(report && report.skeleton && report.skeleton.blocks).filter(isObj);
  let synthesized = false;
  let list = blocks.map((b, i) => ({ i, kind: KINDS.includes(b.kind) ? b.kind : 'text', role: ROLES.includes(b.role) ? b.role : 'other', taken: b.taken !== false, mine: str(b.mine) })).filter((b) => b.taken);
  if (!list.length) {
    synthesized = true;
    list = DEFAULT_ORDER.map((kind, i) => ({ i: -1 - i, kind, role: ['price', 'faq', 'cta'].includes(kind) ? 'pay' : kind === 'headline' ? 'attract' : kind === 'list' ? 'value' : 'other', taken: true, mine: '' }));
  }
  const usedIds = new Set();
  list.forEach((b, n) => {
    b.n = n + 1;
    const m = /^([.#])([A-Za-z_][\w-]*)$/.exec(b.mine);
    // 리포트에 내 구역의 선택자가 이미 적혀 있으면 그 이름을 그대로 달아 준다. 없으면 #rb-N 을 붙인다.
    b.id = m && m[1] === '#' && !usedIds.has(m[2]) ? m[2] : `rb-${b.n}`;
    b.cls = m && m[1] === '.' && !/^(rb-|slot)/.test(m[2]) ? m[2] : '';
    b.sel = (m && m[1] === '.' && b.cls) || (m && m[1] === '#' && b.id === m[2]) ? b.mine : `#${b.id}`;
    b.link = !m && !b.mine && b.i >= 0; // 리포트에 선택자를 적어 줄 구역
    usedIds.add(b.id);
  });
  return { blocks: list, synthesized };
}

// 채울 자리. 제목 안에 들어가는 것(inline)은 span 으로 쓴다.
const slot = (text, cls = '') => { const el = cls === 'inline' ? 'span' : 'p'; return `<${el} class="slot${cls ? ` ${cls}` : ''}"><span class="slot-k">여기에</span> ${esc(text)}</${el}>`; };
const tag = (b) => `<p class="rb-tag"><span>${two(b.n)}</span> ${esc(roleName(b.role))} · ${esc(kindName(b.kind))}</p>`;

function renderBlock(b, ctx) {
  const { mv, title, blocks } = ctx;
  const cls = ['rb', `rb-${b.kind}`, b.cls].filter(Boolean).join(' ');
  const wrap = (el, inner) => `<${el} class="${cls}" id="${esc(b.id)}" data-role="${b.role}">\n${tag(b)}\n${inner}\n</${el}>`;
  const h1 = () => {
    if (ctx.titleDone) return `<h2 class="rb-h2">${esc(title)}</h2>`;
    ctx.titleDone = true;
    return `<h1 class="rb-h1">${esc(title)}</h1>`;
  };
  const jumps = () => blocks.filter((x) => x !== b && NAV_WORD[x.kind]).filter((x, i, a) => a.findIndex((y) => NAV_WORD[y.kind] === NAV_WORD[x.kind]) === i).slice(0, 4)
    .map((x) => `<a href="#${esc(x.id)}">${NAV_WORD[x.kind]}</a>`).join('\n      ');
  switch (b.kind) {
    case 'nav': {
      if (!ctx.navDone) {
        ctx.navDone = true;
        return wrap('header', `  <div class="rb-bar">\n    <span class="rb-brand"><i></i>${esc(mv.working_name)}</span>\n    <nav class="rb-links" aria-label="페이지 안 이동">\n      ${jumps()}\n    </nav>\n  </div>`);
      }
      return wrap('nav', `  <div class="rb-chips" aria-label="페이지 안 이동">\n      ${jumps()}\n  </div>`);
    }
    case 'media':
      return wrap('section', `  <div class="rb-frame" role="img" aria-label="한 장면이 들어갈 자리">\n    <span class="rb-frame-k">한 장면</span>\n    ${slot(kindWrite('media'))}\n  </div>`);
    case 'headline':
      return wrap('section', `  ${h1()}\n  ${slot(kindWrite('headline'), 'lead')}\n  <p class="rb-spec"><span>명세</span> ${esc(mv.who)}</p>`);
    case 'price':
      return wrap('section', `  <div class="rb-split">\n    <div>\n      ${h1()}\n      ${slot('이것을 사면 무엇이 달라지는지 한두 문장으로.', 'lead')}\n      <p class="rb-spec"><span>명세</span> ${esc(mv.same_problem)}</p>\n    </div>\n    <div class="rb-pricebox">\n      <p class="rb-k">가격</p>\n      ${slot('지금 가격. 숫자는 내 것으로 정합니다.', 'big')}\n      ${slot('가격에 들어 있는 것, 가격이 바뀐다면 그 날짜.')}\n      <button type="button" class="rb-btn">신청 단추에 쓸 말</button>\n      ${slot('환불 안내 한 줄.', 'small')}\n    </div>\n  </div>`);
    case 'numbers':
      return wrap('section', `  <h2 class="rb-h2">${slot('숫자로 보여 줄 것의 제목.', 'inline')}</h2>\n  <div class="rb-grid3">\n${[1, 2, 3].map((k) => `    <div class="rb-num"><b>숫자 ${k}</b>${slot('이 숫자가 무엇인지.', 'small')}</div>`).join('\n')}\n  </div>\n  <p class="rb-note">${esc(kindWrite('numbers'))}</p>`);
    case 'list': {
      const first = !ctx.listDone;
      ctx.listDone = true;
      const items = first && arr(mv.mvp).length ? arr(mv.mvp).map(str).filter(Boolean) : [];
      const cards = items.length
        ? items.map((t, k) => `    <li class="rb-card"><span class="rb-no">${two(k + 1)}</span><p class="rb-spec"><span>명세</span> ${esc(t)}</p>${slot('이 항목을 받는 사람의 말로 한 줄.', 'small')}</li>`)
        : [1, 2, 3].map((k) => `    <li class="rb-card"><span class="rb-no">${two(k)}</span>${slot('항목 하나와, 그것으로 얻는 결과 한 줄.', 'small')}</li>`);
      return wrap('section', `  <h2 class="rb-h2">${slot(first ? '무엇을 주는지 묶는 제목.' : '이 목록의 제목.', 'inline')}</h2>\n  <ol class="rb-cards">\n${cards.join('\n')}\n  </ol>`);
    }
    case 'notice':
      return wrap('section', `  <div class="rb-box">\n    <p class="rb-k">알려 둘 것</p>\n    ${slot(kindWrite('notice'))}\n  </div>`);
    case 'quotes':
      return wrap('section', `  <h2 class="rb-h2">${slot('먼저 써 본 사람의 말을 묶는 제목.', 'inline')}</h2>\n  <div class="rb-grid3">\n${[1, 2, 3].map(() => `    <figure class="rb-quote"><blockquote>${slot('받은 말을 그대로. 아직 없으면 비워 둡니다.', 'small')}</blockquote><figcaption>${slot('누가 한 말인지.', 'small')}</figcaption></figure>`).join('\n')}\n  </div>\n  <p class="rb-note">${esc(kindWrite('quotes'))}</p>`);
    case 'faq':
      return wrap('section', `  <h2 class="rb-h2">${slot('물음과 답을 묶는 제목.', 'inline')}</h2>\n  <div class="rb-faq">\n${[1, 2, 3, 4].map((k) => `    <details${k === 1 ? ' open' : ''}><summary>물음 ${k}: 사기 전에 걱정하는 것을 물음으로</summary>${slot('솔직한 답 두세 문장.', 'small')}</details>`).join('\n')}\n  </div>`);
    case 'cta':
      return wrap('section', `  <div class="rb-last">\n    ${slot('마지막으로 한 번 더 권하는 한 문장.', 'lead')}\n    <button type="button" class="rb-btn">신청 단추에 쓸 말</button>\n  </div>`);
    case 'footer':
      return wrap('footer', `  <div class="rb-foot">\n    <span class="rb-brand"><i></i>${esc(mv.working_name)}</span>\n    ${slot(kindWrite('footer'), 'small')}\n  </div>`);
    default:
      return wrap('section', `  <h2 class="rb-h2">${slot('이 구역의 짧은 제목.', 'inline')}</h2>\n  ${slot(kindWrite('text'))}`);
  }
}

// 리포트에서 페이지를 그린다. 돌려주는 것: { html, css, blocks, synthesized, title }
export function renderSite(report, { topic = '' } = {}) {
  const mvRaw = (report.sections && report.sections.my_version) || {};
  const mv = { working_name: str(mvRaw.working_name), same_problem: str(mvRaw.same_problem), who: str(mvRaw.who), mvp: arr(mvRaw.mvp), differences: arr(mvRaw.differences).filter(isObj), not_taken: arr(mvRaw.not_taken) };
  const { blocks, synthesized } = planBlocks(report);
  const title = str(topic) || mv.working_name;
  const ctx = { mv, title, blocks, titleDone: false, navDone: false, listDone: false };
  const body = blocks.map((b) => renderBlock(b, ctx));
  const mvpPlaced = ctx.listDone && mv.mvp.length > 0;
  const guide = [
    '<aside class="rb-guide" id="rb-guide">',
    '  <p class="rb-guide-t">출발점입니다</p>',
    `  <p>배운 구역의 순서와 짜임만 옮겼습니다${synthesized ? ' (리포트에 뼈대가 없어 기본 순서로 만들었습니다)' : ''}. 점선 자리의 안내를 내 말로 바꾸고, 그림과 색도 내 것으로 정하세요. 다 쓰면 이 상자를 지웁니다.</p>`,
    '  <dl>',
    `    <dt>가칭</dt><dd>${esc(mv.working_name)}</dd>`,
    ...(str(topic) ? [`    <dt>주제</dt><dd>${esc(str(topic))}</dd>`] : []),
    `    <dt>같은 문제</dt><dd>${esc(mv.same_problem)}</dd>`,
    `    <dt>누구에게</dt><dd>${esc(mv.who)}</dd>`,
    ...(!mvpPlaced && mv.mvp.length ? [`    <dt>최소 기능</dt><dd><ul>${mv.mvp.map((t) => `<li>${esc(str(t))}</li>`).join('')}</ul></dd>`] : []),
    `    <dt>다른 점 세 가지</dt><dd><ol>${mv.differences.map((d) => `<li><b>${esc(str(d.title))}</b> ${esc(str(d.text))}</li>`).join('')}</ol></dd>`,
    `    <dt>가져오지 않는 것</dt><dd><ul>${mv.not_taken.map((t) => `<li>${esc(str(t))}</li>`).join('')}</ul></dd>`,
    '  </dl>',
    '</aside>',
  ].join('\n');
  const html = `<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="generator" content="${GENERATOR}">
<title>${esc(title)}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
${guide}
${body.join('\n\n')}
</body>
</html>
`;
  return { html, css: CSS, blocks, synthesized, title };
}

// 폴더에 쓴다. 이미 무언가 들어 있는 폴더는 --force 없이는 건드리지 않는다.
export function buildSite(reportPath, outDir, { topic = '', force = false } = {}) {
  const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
  const state = specState(report);
  if (state.blank) { const e = new Error('6번 칸(내 버전 명세)이 비어 있어요'); e.code = 'spec-empty'; throw e; }
  if (state.errors.length) { const e = new Error('6번 칸(내 버전 명세)에 고칠 곳이 있어요'); e.code = 'spec-errors'; e.errors = state.errors; throw e; }
  const src = findSource(reportPath);
  const names = targetNames(report, src && src.source);
  const mv = report.sections.my_version;
  const spoken = [['--topic', topic], ['가칭', mv.working_name], ['같은 문제', mv.same_problem], ['누구에게', mv.who], ...arr(mv.mvp).map((t) => ['최소 기능', t]), ...arr(mv.differences).flatMap((d) => [['다른 점', d && d.title], ['다른 점', d && d.text]])];
  const bad = spoken.map(([where, text]) => ({ where, why: nameProblem(text, names) })).filter((x) => x.why);
  if (bad.length) { const e = new Error('명세나 주제에 쓰면 안 되는 말이 들어 있어요'); e.code = 'names'; e.errors = [...new Set(bad.map((x) => `${x.where}: ${x.why}이 들어 있어요`))]; throw e; }
  const dir = path.resolve(outDir || path.join(path.dirname(path.resolve(reportPath)), 'my-version'));
  if (fs.existsSync(dir) && fs.readdirSync(dir).filter((f) => f !== '.DS_Store').length && !force) { const e = new Error(`폴더에 이미 파일이 있어요: ${dir}`); e.code = 'exists'; e.dir = dir; throw e; }
  const site = renderSite(report, { topic });
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), site.html);
  fs.writeFileSync(path.join(dir, 'style.css'), site.css);
  // 해부 화면의 비교 칸이 내 구역을 찾을 수 있게, 선택자가 비어 있던 뼈대 구역에만 적어 준다. 적혀 있던 것은 바꾸지 않는다.
  const link = site.blocks.filter((b) => b.link);
  if (link.length) {
    for (const b of link) report.skeleton.blocks[b.i].mine = b.sel;
    fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
  }
  let clone = null;
  if (src) clone = { file: src.file, ...checkClone(dir, src.source) };
  return { dir, files: ['index.html', 'style.css'], sections: site.blocks.length, synthesized: site.synthesized, linked: link.length, title: site.title, clone, kinds: site.blocks.map((b) => b.kind) };
}

// 중립 디자인: 검정 바탕, 얇은 산세리프, 금색은 강조에만. 바깥 글꼴과 그림을 부르지 않는다.
const CSS = `/* rebiz build 가 만든 출발점의 스타일. 색과 글꼴은 내 것으로 바꿔 쓰세요. */
:root {
  --bg: #07080A;
  --panel: #0D0F12;
  --line: rgba(214, 137, 42, 0.24);
  --line-soft: rgba(235, 226, 210, 0.12);
  --ivory: #EBE2D2;
  --dim: #B9B1A3;
  --mute: #8A8478;
  --gold: #D6892A;
  --gold-hi: #F2B45A;
  --sans: "Pretendard Variable", Pretendard, "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "Helvetica Neue", system-ui, sans-serif;
  --mono: "SF Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  --gutter: clamp(18px, 5vw, 56px);
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
body { margin: 0; background: var(--bg); color: var(--ivory); font-family: var(--sans); font-weight: 300; font-size: 16px; line-height: 1.65; -webkit-font-smoothing: antialiased; word-break: keep-all; overflow-wrap: anywhere; }
a { color: inherit; text-decoration: none; }
p { margin: 0; }
:focus-visible { outline: 1px solid var(--gold-hi); outline-offset: 3px; }

/* 구역: 위에서 아래로, 배운 순서 그대로 */
.rb { max-width: 1120px; margin: 0 auto; padding: clamp(36px, 7vw, 84px) var(--gutter); border-bottom: 1px solid var(--line-soft); }
.rb-tag { font-family: var(--mono); font-size: 11px; letter-spacing: 0.14em; color: var(--mute); margin-bottom: 18px; }
.rb-tag span { color: var(--gold); margin-right: 8px; }
/* 다 쓴 뒤에는 아래 줄의 주석을 풀어 구역 꼬리표를 숨깁니다. */
/* .rb-tag, .rb-guide { display: none; } */

.rb-h1 { margin: 0 0 20px; font-size: clamp(32px, 6vw, 68px); font-weight: 200; line-height: 1.14; letter-spacing: -0.02em; }
.rb-h2 { margin: 0 0 24px; font-size: clamp(22px, 3.4vw, 34px); font-weight: 200; line-height: 1.25; letter-spacing: -0.01em; }
.rb-k { font-family: var(--mono); font-size: 11px; letter-spacing: 0.2em; color: var(--gold); margin-bottom: 12px; }
.rb-note { margin-top: 18px; font-size: 13px; color: var(--mute); }
.rb-spec { margin-top: 14px; font-size: 14px; color: var(--dim); }
.rb-spec span { font-family: var(--mono); font-size: 10px; letter-spacing: 0.16em; color: var(--gold); border: 1px solid var(--line); padding: 2px 6px; margin-right: 8px; white-space: nowrap; }

/* 채울 자리: 점선 상자 안의 안내를 내 말로 바꿉니다 */
.slot { border: 1px dashed rgba(235, 226, 210, 0.26); border-radius: 2px; padding: 10px 14px; color: var(--dim); font-size: 14px; font-weight: 300; line-height: 1.55; letter-spacing: 0; }
.slot + .slot { margin-top: 10px; }
.slot-k { font-family: var(--mono); font-size: 10px; letter-spacing: 0.16em; color: var(--gold-hi); margin-right: 6px; }
.slot.lead { font-size: clamp(15px, 1.8vw, 18px); max-width: 44em; }
.slot.big { font-size: 20px; color: var(--ivory); }
.slot.small { font-size: 13px; }
.slot.inline { display: block; margin: 0; font-size: 15px; }

/* 머리말과 페이지 안 이동 */
.rb-nav { padding-top: 18px; padding-bottom: 18px; }
.rb-nav .rb-tag { margin-bottom: 10px; }
.rb-bar { display: flex; align-items: center; justify-content: space-between; gap: 12px 24px; flex-wrap: wrap; }
.rb-brand { display: inline-flex; align-items: center; gap: 10px; font-size: 14px; letter-spacing: 0.04em; color: var(--ivory); }
.rb-brand i { width: 3px; height: 14px; background: var(--gold); flex: none; }
.rb-links, .rb-chips { display: flex; flex-wrap: wrap; gap: 8px 20px; font-size: 13px; color: var(--dim); }
.rb-chips a { border: 1px solid var(--line-soft); padding: 6px 14px; border-radius: 999px; }
.rb-links a:hover, .rb-chips a:hover { color: var(--gold-hi); }

/* 한 장면 */
.rb-frame { aspect-ratio: 16 / 9; max-height: 560px; width: 100%; display: flex; flex-direction: column; justify-content: flex-end; gap: 12px; padding: clamp(16px, 3vw, 32px); border: 1px solid var(--line); background: linear-gradient(160deg, rgba(214, 137, 42, 0.10), rgba(13, 15, 18, 0) 60%), var(--panel); }
.rb-frame-k { font-family: var(--mono); font-size: 11px; letter-spacing: 0.2em; color: var(--gold); }

/* 제목과 가격 상자 */
.rb-split { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: clamp(24px, 5vw, 64px); align-items: start; }
.rb-pricebox, .rb-box { border: 1px solid var(--line); background: var(--panel); padding: clamp(18px, 3vw, 30px); }
.rb-btn { display: block; width: 100%; margin: 16px 0 12px; padding: 15px 20px; font: inherit; font-weight: 400; color: #07080A; background: var(--gold); border: 0; border-radius: 2px; cursor: pointer; }
.rb-btn:hover { background: var(--gold-hi); }

/* 세 칸, 카드, 물음 */
.rb-grid3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
.rb-num { border-top: 1px solid var(--line); padding-top: 18px; }
.rb-num b { display: block; margin-bottom: 12px; font-size: clamp(28px, 4.6vw, 52px); font-weight: 200; color: var(--gold-hi); letter-spacing: -0.02em; }
.rb-cards { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }
.rb-card { border: 1px solid var(--line-soft); background: var(--panel); padding: 20px; }
.rb-card .rb-spec { margin: 10px 0 12px; }
.rb-no { font-family: var(--mono); font-size: 11px; letter-spacing: 0.2em; color: var(--gold); }
.rb-quote { margin: 0; border-left: 1px solid var(--line); padding-left: 16px; }
.rb-quote blockquote { margin: 0 0 10px; }
.rb-faq details { border-bottom: 1px solid var(--line-soft); padding: 16px 0; }
.rb-faq summary { cursor: pointer; font-size: 16px; color: var(--ivory); }
.rb-faq details .slot { margin-top: 12px; }
.rb-last { max-width: 640px; margin: 0 auto; text-align: center; }
.rb-last .rb-btn { max-width: 360px; margin-left: auto; margin-right: auto; }
.rb-foot { display: grid; gap: 14px; }
.rb-footer { border-bottom: 0; color: var(--mute); }

/* 만드는 사람만 보는 안내 */
.rb-guide { max-width: 1120px; margin: 0 auto; padding: 22px var(--gutter); border-bottom: 1px solid var(--line); font-size: 13px; color: var(--dim); }
.rb-guide-t { font-family: var(--mono); font-size: 11px; letter-spacing: 0.2em; color: var(--gold); margin-bottom: 8px; }
.rb-guide dl { display: grid; grid-template-columns: 9em minmax(0, 1fr); gap: 6px 16px; margin: 14px 0 0; }
.rb-guide dt { color: var(--mute); }
.rb-guide dd { margin: 0; }
.rb-guide ol, .rb-guide ul { margin: 0; padding-left: 1.2em; }
.rb-guide b { font-weight: 400; color: var(--ivory); margin-right: 6px; }

@media (max-width: 760px) {
  .rb-split, .rb-grid3 { grid-template-columns: minmax(0, 1fr); }
  .rb-guide dl { grid-template-columns: minmax(0, 1fr); gap: 2px; }
  .rb-guide dt { margin-top: 8px; }
}
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
`;

function main() {
  const args = process.argv.slice(2);
  const o = { force: false };
  for (let i = 0; i < args.length; i += 1) {
    const a = args[i];
    if (a === '--out') o.out = args[++i];
    else if (a === '--topic') o.topic = args[++i];
    else if (a === '--force') o.force = true;
    else if (!a.startsWith('--') && !o.file) o.file = a;
    else o.bad = a;
  }
  const usage = '사용: node make-site.mjs <report.json> [--out <폴더>] [--topic "내 사업 주제"] [--force]';
  if (o.bad || !o.file) { if (o.bad) console.error(`모르는 인자: ${o.bad}`); console.error(usage); process.exit(2); }
  let r;
  try { r = buildSite(o.file, o.out, { topic: o.topic, force: o.force }); } catch (e) {
    console.error(`만들지 못했어요: ${e.message}`);
    for (const m of e.errors || []) console.error(`  ${m}`);
    if (e.code === 'spec-empty') console.error('6번 칸을 먼저 채우세요 (SKILL.md 의 5단계). 채운 뒤 다시 실행합니다.');
    if (e.code === 'exists') console.error('다른 폴더를 --out 으로 주거나, 덮어써도 되면 --force 를 붙이세요.');
    process.exit(e.code === 'exists' || e.code === 'spec-empty' ? 2 : 1);
  }
  console.log(`새 사이트의 출발점: ${r.dir}  (구역 ${r.sections}개, ${r.files.join(', ')})`);
  if (r.linked) console.log(`report.json 의 뼈대 ${r.linked}곳에 내 구역의 선택자를 적었어요.`);
  if (!r.clone) console.log('겹침 검사는 건너뛰었어요: 리포트 옆에 source.json 이 없어요.');
  else {
    for (const f of r.clone.fails) console.log(`실패  [${f.rule}] ${f.file}: ${f.msg}`);
    console.log(r.clone.fails.length ? `겹침 ${r.clone.fails.length}건.` : `겹침 검사 통과 (경고 ${r.clone.warns.length}건).`);
    if (r.clone.fails.length) process.exit(1);
  }
}

// 바로 실행했을 때만 돈다. 경로에 심볼릭 링크가 끼어 있어도 알아보도록 실제 경로로 견준다.
const direct = (() => { try { return fs.realpathSync(process.argv[1]) === fs.realpathSync(fileURLToPath(import.meta.url)); } catch { return false; } })();
if (direct) main();
