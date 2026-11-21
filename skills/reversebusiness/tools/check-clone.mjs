#!/usr/bin/env node
// 내 버전이 원본과 겹치는지 본다. 의존성 없음.
//
// 사용:
//   node check-clone.mjs <내 버전 폴더> --source <source.json> [옵션]
//
//   --source <파일>   from-rea.mjs 가 만든 원본 글 묶음(source.json). 여러 번 줄 수 있다
//   --text <파일>     원본 글을 담은 텍스트 파일(한 줄에 한 문장). source.json 대신이나 함께
//   --brand <이름>    원본 브랜드 이름을 더한다(여러 번)
//   --domain <주소>   원본 도메인을 더한다(여러 번)
//   --words <수>      몇 낱말이 연달아 같으면 겹침으로 볼지. 기본 5
//   --allow <문구>    겹쳐도 되는 문구(여러 번). 법으로 정해진 고지 문구 같은 것만
//
// 실패로 보는 것 세 가지:
//   1. 원본과 다섯 낱말 이상 연달아 같은 구간
//   2. 원본 브랜드 이름이나 도메인 (글, 코드, 파일 이름 어디든)
//   3. 원본 이미지, 아이콘, 영상, 글꼴 주소
// 경고로 알리는 것: 원본의 한 줄과 통째로 같은 짧은 문구(3~4 낱말), 원본과 같은 자원 파일 이름, 바깥 주소에서 불러오는 자원.
// 보지 않는 것: 색, 글꼴 모양, 배치의 닮음. 그것은 두 화면을 나란히 놓고 사람이 본다.
// 종료 코드: 통과 0, 실패 1, 잘못 쓴 경우 2.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const TEXT_EXT = new Set(['.html', '.htm', '.css', '.js', '.mjs', '.ts', '.tsx', '.jsx', '.json', '.md', '.txt', '.svg', '.vue', '.astro', '.xml', '.yml', '.yaml']);
const SKIP_DIR = new Set(['node_modules', '.git', 'dist', '.next', '.cache']);
const ASSET_EXT = /\.(png|jpe?g|webp|gif|svg|ico|avif|mp4|webm|mov|woff2?|ttf|otf)$/i;

// 낱말: 한글 덩어리, 영문과 숫자 덩어리. 문장부호와 기호는 버린다.
export const words = (t) => String(t).toLowerCase().match(/[a-z0-9]+(?:['’][a-z]+)?|[가-힣]+|[぀-ヿ一-鿿]+/g) || [];
// 띄어쓰기, 기호를 뗀 모양. "AI CITY", "ai-city", "AiCity" 를 같게 본다.
export const squash = (t) => String(t).toLowerCase().replace(/[^a-z0-9가-힣぀-ヿ一-鿿]+/g, '');

export const HUMAN_META = /^(description|keywords|author|application-name|apple-mobile-web-app-title|og:(title|description|site_name)|twitter:(title|description))$/i;
const INLINE = 'a|abbr|b|bdi|bdo|cite|code|data|dfn|em|i|kbd|mark|q|s|samp|small|span|strong|sub|sup|time|u|var|wbr|font|label';
// HTML 에서 사람이 읽는 글을 줄 단위로 뽑는다. 글자 사이에 낀 꾸밈 태그는 문장을 끊지 않는다.
export function htmlLines(html) {
  // 속성 글자: 사람이 읽는 것만. 메타는 소개, 제목, 열쇠말처럼 글로 쓴 것만 보고 viewport 같은 설정 값은 건너뛴다.
  const val = (tag, name) => { const m = tag.match(new RegExp(`\\b${name}\\s*=\\s*("([^"]*)"|'([^']*)')`, 'i')); return m ? (m[2] ?? m[3] ?? '') : ''; };
  const attrs = [];
  for (const tag of html.match(/<[a-z][^>]*>/gi) || []) {
    if (/^<meta\b/i.test(tag)) {
      if (HUMAN_META.test(val(tag, 'name') || val(tag, 'property'))) attrs.push(val(tag, 'content'));
      continue;
    }
    for (const k of ['alt', 'title', 'aria-label', 'placeholder', 'value']) { const v = val(tag, k); if (v) attrs.push(v); }
  }
  const body = html
    .replace(/<!--[\s\S]*?-->/g, '\n')
    .replace(/<script\b[\s\S]*?<\/script>/gi, '\n')
    .replace(/<style\b[\s\S]*?<\/style>/gi, '\n')
    .replace(new RegExp(`</?(?:${INLINE})\\b[^>]*>`, 'gi'), ' ')
    .replace(/<[^>]+>/g, '\n')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'");
  return [...body.split('\n'), ...attrs].map((l) => l.replace(/\s+/g, ' ').trim()).filter(Boolean);
}
function fileLines(file, raw) {
  const ext = path.extname(file).toLowerCase();
  if (ext === '.html' || ext === '.htm' || ext === '.svg' || ext === '.vue' || ext === '.astro') {
    // 태그 밖 글에 더해 스크립트 안의 글자도 본다(문구를 스크립트에 숨겨도 잡히게).
    const scripts = [...raw.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)].map((m) => m[1]).join('\n');
    return [...htmlLines(raw), ...scripts.split('\n').map((l) => l.trim()).filter(Boolean)];
  }
  return raw.split('\n').map((l) => l.trim()).filter(Boolean);
}

function listFiles(root) {
  const out = [];
  const walk = (dir) => {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      if (e.name === '.DS_Store') continue;
      const p = path.join(dir, e.name);
      if (e.isDirectory()) { if (!SKIP_DIR.has(e.name)) walk(p); } else if (e.isFile()) out.push(p);
    }
  };
  walk(root);
  return out.sort();
}

// 원본 글 묶음을 읽는다. o: { sources: [source.json ...], texts: [글 파일 ...], brands: [], domains: [] }
export function loadSource(o) {
  o = { sources: [], texts: [], brands: [], domains: [], ...o };
  const src = { texts: [], names: [...o.brands], domains: [...o.domains], assets: [] };
  for (const f of o.sources) {
    const j = JSON.parse(fs.readFileSync(f, 'utf8'));
    src.texts.push(...(j.texts || []));
    src.names.push(...((j.brand || {}).names || []));
    src.domains.push(...((j.brand || {}).domains || []));
    src.assets.push(...(j.assets || []));
  }
  for (const f of o.texts) src.texts.push(...fs.readFileSync(f, 'utf8').split('\n'));
  const u = (a) => [...new Set(a.map((s) => String(s).trim()).filter(Boolean))];
  return { texts: u(src.texts), names: u(src.names), domains: u(src.domains), assets: u(src.assets) };
}

// only 를 주면 그 파일들만 본다 (폴더 기준 상대 경로). 이미 있는 프로젝트에서 바뀐 파일만 볼 때 쓴다.
export function checkClone(root, source, { n = 5, allow = [], only = null } = {}) {
  const fails = [];
  const warns = [];
  const notes = [];
  const fail = (rule, file, msg) => fails.push({ rule, file, msg });
  const warn = (rule, file, msg) => warns.push({ rule, file, msg });
  const allowSq = allow.map(squash).filter(Boolean);
  const allowed = (phrase) => allowSq.some((a) => a.includes(squash(phrase)) || squash(phrase).includes(a));

  // 원본 쪽 준비
  const grams = new Map(); // 낱말 n개 구간 -> 원본 줄
  const shortLines = new Map(); // 3~4 낱말짜리 원본 줄(통째로 같을 때만 경고)
  for (const line of source.texts) {
    const w = words(line);
    for (let i = 0; i + n <= w.length; i++) { const g = w.slice(i, i + n).join(' '); if (!grams.has(g)) grams.set(g, line); }
    if (w.length >= 3 && w.length < n && squash(line).length >= 8) shortLines.set(w.join(' '), line);
  }
  const brandSq = [];
  for (const name of [...source.names, ...source.domains]) {
    const sq = squash(name);
    if (sq.length < 3) { notes.push(`브랜드 이름 "${name}" 은 너무 짧아 보지 않았어요.`); continue; }
    if (!brandSq.some((b) => b.sq === sq)) brandSq.push({ name, sq });
  }
  const assetUrls = new Set(source.assets);
  const assetNames = new Map();
  for (const a of source.assets) { const b = a.split('?')[0].split('/').pop().toLowerCase(); if (b && ASSET_EXT.test(b)) assetNames.set(b, a); }
  const domainRe = source.domains.filter((d) => d.includes('.')).map((d) => d.toLowerCase());

  const files = Array.isArray(only) ? [...new Set(only.map((f) => path.resolve(root, f)))].filter((f) => { try { return fs.statSync(f).isFile(); } catch { return false; } }).sort() : listFiles(root);
  let textFiles = 0;
  let checkedWords = 0;
  for (const file of files) {
    const rel = path.relative(root, file).split(path.sep).join('/');
    // 2. 파일 이름에 원본 이름
    for (const b of brandSq) if (squash(rel).includes(b.sq)) fail('이름', rel, `파일 이름에 원본 이름 "${b.name}" 이 들어 있어요.`);
    const base = path.basename(file).toLowerCase();
    if (assetNames.has(base)) warn('자원', rel, `원본 자원과 파일 이름이 같아요 (${base}). 원본 파일을 받아 넣은 것이 아닌지 확인하세요.`);
    if (!TEXT_EXT.has(path.extname(file).toLowerCase())) continue;
    const raw = fs.readFileSync(file, 'utf8');
    textFiles += 1;

    // 1. 다섯 낱말 이상 연달아 같은 구간
    const seenRuns = new Set();
    for (const line of fileLines(file, raw)) {
      const w = words(line);
      checkedWords += w.length;
      let i = 0;
      while (i + n <= w.length) {
        const g = w.slice(i, i + n).join(' ');
        if (!grams.has(g)) { i += 1; continue; }
        // 같은 구간을 끝까지 늘려 한 번만 알린다.
        let j = i + n;
        while (j < w.length && grams.has(w.slice(j - n + 1, j + 1).join(' '))) j += 1;
        const run = w.slice(i, j).join(' ');
        if (!seenRuns.has(run) && !allowed(run)) {
          seenRuns.add(run);
          fail('문장', rel, `원본과 ${j - i}낱말이 연달아 같아요: "${run}"  (원본: "${cut(grams.get(g))}")`);
        }
        i = j;
      }
      const key = w.join(' ');
      if (shortLines.has(key) && !allowed(key)) warn('문장', rel, `원본의 한 줄과 통째로 같은 짧은 문구예요: "${line}"`);
    }

    // 2. 원본 브랜드 이름, 도메인
    // 긴 이름부터 본다. 긴 이름에 이미 잡힌 자리는 짧은 이름으로 다시 세지 않는다.
    let sq = squash(raw);
    for (const b of [...brandSq].sort((x, y) => y.sq.length - x.sq.length)) {
      if (!sq.includes(b.sq)) continue;
      const at = raw.split('\n').findIndex((l) => squash(l).includes(b.sq));
      fail('이름', rel, `원본 이름 "${b.name}" 이 들어 있어요${at >= 0 ? ` (${at + 1}번째 줄)` : ''}.`);
      sq = sq.split(b.sq).join('\u0000');
    }

    // 3. 원본 자원 주소
    const urls = [...raw.matchAll(/(?:https?:)?\/\/[^\s"'()<>]+|url\(\s*["']?([^"')]+)["']?\s*\)|(?:src|href|poster|srcset)\s*=\s*["']([^"']+)["']/gi)].map((m) => (m[1] || m[2] || m[0]).trim());
    const seenUrl = new Set();
    for (const u of urls) {
      if (seenUrl.has(u)) continue;
      seenUrl.add(u);
      const low = u.toLowerCase();
      const clean = u.split('?')[0].split('#')[0];
      const onOrigin = domainRe.some((d) => low.includes(`//${d}`) || low.includes(`.${d}`));
      if (assetUrls.has(clean) || assetUrls.has(u)) fail('자원', rel, `원본 자원 주소를 그대로 써요: ${u}`);
      else if (onOrigin && ASSET_EXT.test(clean)) fail('자원', rel, `원본 도메인의 자원을 불러와요: ${u}`);
      else if (/^(https?:)?\/\//i.test(u) && !onOrigin && /\.(css|js|mjs|png|jpe?g|webp|gif|svg|ico|avif|mp4|webm|woff2?|ttf|otf)$/i.test(clean)) warn('자원', rel, `바깥 주소에서 자원을 불러와요: ${u}`);
    }
  }
  return { fails, warns, notes, stats: { files: files.length, textFiles, checkedWords, sourceLines: source.texts.length, grams: grams.size, brands: brandSq.length, assets: source.assets.length, n } };
}
const cut = (s, k = 70) => (String(s).length > k ? `${String(s).slice(0, k - 1)}…` : String(s));

function parseArgs(argv) {
  const o = { sources: [], texts: [], brands: [], domains: [], allow: [], n: 5 };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => String(argv[++i] ?? '');
    if (a === '--source') o.sources.push(next());
    else if (a === '--text') o.texts.push(next());
    else if (a === '--brand') o.brands.push(next());
    else if (a === '--domain') o.domains.push(next());
    else if (a === '--allow') o.allow.push(next());
    else if (a === '--words') o.n = Number(next());
    else if (a === '--help' || a === '-h') o.help = true;
    else if (a.startsWith('--')) o.bad = a;
    else if (!o.dir) o.dir = a;
    else o.bad = a;
  }
  return o;
}

function main() {
  const o = parseArgs(process.argv.slice(2));
  const usage = '사용: node check-clone.mjs <내 버전 폴더> --source <source.json> [--text 파일] [--brand 이름] [--domain 주소] [--words 5] [--allow 문구]';
  if (o.help) { console.log(usage); process.exit(0); }
  if (o.bad || !o.dir || (!o.sources.length && !o.texts.length) || !(o.n >= 3)) {
    if (o.bad) console.error(`모르는 인자: ${o.bad}`);
    else if (!(o.n >= 3)) console.error('--words 는 3 이상');
    else if (o.dir) console.error('원본 글이 필요해요. --source 또는 --text 를 주세요.');
    console.error(usage);
    process.exit(2);
  }
  let source;
  let result;
  try {
    if (!fs.statSync(o.dir).isDirectory()) throw new Error('내 버전은 폴더로 주세요');
    source = loadSource(o);
    if (!source.texts.length) throw new Error('원본 글이 비어 있어요. 빈 원본으로는 통과시킬 수 없어요');
    result = checkClone(path.resolve(o.dir), source, { n: o.n, allow: o.allow });
  } catch (e) { console.error(`검사하지 못했어요: ${e.message}`); process.exit(2); }
  const { fails, warns, notes, stats } = result;
  console.log(`내 버전: 파일 ${stats.files}개 (글 파일 ${stats.textFiles}개, 낱말 ${stats.checkedWords}개)`);
  console.log(`원본: 글 ${stats.sourceLines}줄, 이름과 도메인 ${stats.brands}개, 자원 주소 ${stats.assets}개. 기준: ${stats.n}낱말 연속`);
  if (!stats.textFiles) { console.log('실패  볼 글 파일이 없어요. 폴더가 맞는지 확인하세요.'); process.exit(1); }
  const count = (rule) => fails.filter((f) => f.rule === rule).length;
  console.log(`  1. 같은 문장 구간     ${count('문장') ? `실패 ${count('문장')}건` : '없음'}`);
  console.log(`  2. 원본 이름, 도메인  ${count('이름') ? `실패 ${count('이름')}건` : '없음'}`);
  console.log(`  3. 원본 자원 주소     ${count('자원') ? `실패 ${count('자원')}건` : '없음'}`);
  for (const f of fails) console.log(`실패  [${f.rule}] ${f.file}: ${f.msg}`);
  for (const w of warns) console.log(`경고  [${w.rule}] ${w.file}: ${w.msg}`);
  for (const m of notes) console.log(`알림  ${m}`);
  console.log(fails.length
    ? `겹침 ${fails.length}건. 그 부분을 내 말, 내 이름, 내 자원으로 바꾼 뒤 다시 검사하세요.`
    : `통과 (경고 ${warns.length}건). 색, 글꼴, 배치의 닮음은 이 검사가 보지 않아요. 두 화면을 나란히 놓고 한 번 더 보세요.`);
  process.exit(fails.length ? 1 : 0);
}

// 바로 실행했을 때만 돈다. 경로에 심볼릭 링크가 끼어 있어도 알아보도록 실제 경로로 견준다.
const direct = (() => { try { return fs.realpathSync(process.argv[1]) === fs.realpathSync(fileURLToPath(import.meta.url)); } catch { return false; } })();
if (direct) main();
