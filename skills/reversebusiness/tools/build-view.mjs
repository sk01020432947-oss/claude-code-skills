#!/usr/bin/env node
// report.json 을 한 파일짜리 해부 화면(report.html)으로 만든다. 의존성 없음, 인터넷 없이 열린다.
// 사용: node build-view.mjs <report.json> [--mine <내 버전 폴더>] [--out <report.html>] [--lang en] [--open]
//
// --mine 을 주면 내 버전 페이지를 화면 안에 미리보기로 넣는다 (스크립트는 꺼진 채로 보인다).
// 내 버전 폴더 옆에 <폴더 이름>.preview.jpg 와 <폴더 이름>.preview.json 이 있으면 영상 저장에도 쓴다.
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const MAX_IMAGE = 3_000_000;
const IMAGE_TYPES = { '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif', '.svg': 'image/svg+xml' };

// 설치된 스킬 폴더(reversebusiness/viewer)와 저장소(viewer/) 두 배치를 모두 찾는다.
export function findViewerDir() {
  const tries = [path.join(HERE, '..', 'viewer'), path.join(HERE, '..', '..', '..', 'viewer')];
  return tries.find((d) => fs.existsSync(path.join(d, 'index.html'))) || null;
}

const safeJson = (v) => JSON.stringify(v).replace(/</g, '\\u003c').replace(/[\u2028\u2029]/g, '');
const closeSafe = (js) => js.replace(/<\/script/gi, '<\\/script');

// 내 버전 폴더를 미리보기 재료로 바꾼다: 같은 폴더의 스타일은 안으로 넣고, 스크립트는 뺀다.
export function loadMine(dir) {
  const root = path.resolve(dir);
  if (!fs.existsSync(root) || !fs.statSync(root).isDirectory()) throw new Error(`내 버전 폴더를 찾지 못했어요: ${dir}`);
  const page = ['index.html', 'index.htm'].map((f) => path.join(root, f)).find((f) => fs.existsSync(f))
    || fs.readdirSync(root).filter((f) => /\.html?$/i.test(f)).map((f) => path.join(root, f))[0];
  if (!page) throw new Error(`내 버전 폴더에 HTML 파일이 없어요: ${dir}`);
  let html = fs.readFileSync(page, 'utf8');
  html = html.replace(/<script\b[\s\S]*?<\/script>/gi, '').replace(/<link\b[^>]*>/gi, (tag) => {
    if (!/rel\s*=\s*["']?stylesheet/i.test(tag)) return tag;
    const href = (/href\s*=\s*["']([^"']+)["']/i.exec(tag) || [])[1] || '';
    if (!href || /^([a-z]+:)?\/\//i.test(href) || href.startsWith('data:')) return tag;
    const file = path.resolve(path.dirname(page), href.split(/[?#]/)[0]);
    if (!file.startsWith(root + path.sep) || !fs.existsSync(file)) return tag;
    return `<style>\n${fs.readFileSync(file, 'utf8').replace(/<\/style/gi, '<\\/style')}\n</style>`;
  });
  // 같은 폴더의 작은 그림은 안으로 넣는다. 바깥 주소의 자원은 미리보기에서 불러오지 않는다.
  html = html.replace(/(<img\b[^>]*?\bsrc\s*=\s*)(["'])([^"']+)\2/gi, (m, head, q, src) => {
    if (/^(data:|[a-z]+:|\/\/)/i.test(src)) return m;
    const file = path.resolve(path.dirname(page), src.split(/[?#]/)[0]);
    const type = IMAGE_TYPES[path.extname(file).toLowerCase()];
    if (!type || !file.startsWith(root + path.sep) || !fs.existsSync(file) || fs.statSync(file).size > 400_000) return m;
    return `${head}${q}data:${type};base64,${fs.readFileSync(file).toString('base64')}${q}`;
  });
  // 미리보기 안에서는 스크립트, 바깥 자원, 저절로 다른 주소로 넘어가기를 막는다.
  html = html.replace(/<meta\b[^>]*http-equiv\s*=\s*["']?refresh[^>]*>/gi, '').replace(/<base\b[^>]*>/gi, '');
  const guard = `<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src data:; font-src data:; media-src data:; form-action 'none'; base-uri 'none'">`;
  html = /<head\b[^>]*>/i.test(html) ? html.replace(/<head\b[^>]*>/i, (m) => `${m}\n${guard}`) : `${guard}\n${html}`;
  const mine = { html };
  const base = root.replace(/[\\/]+$/, '');
  const meta = `${base}.preview.json`;
  const shot = ['.preview.jpg', '.preview.jpeg', '.preview.png', '.preview.webp'].map((e) => base + e).find((f) => fs.existsSync(f));
  if (shot && fs.existsSync(meta) && fs.statSync(shot).size <= MAX_IMAGE) {
    try {
      const j = JSON.parse(fs.readFileSync(meta, 'utf8'));
      const ext = path.extname(shot).toLowerCase();
      const type = ext === '.png' ? 'image/png' : ext === '.webp' ? 'image/webp' : 'image/jpeg';
      mine.image = `data:${type};base64,${fs.readFileSync(shot).toString('base64')}`;
      mine.rects = j.rects && typeof j.rects === 'object' ? j.rects : {};
    } catch { /* 미리보기 그림 없이 진행 */ }
  }
  return mine;
}

export function buildView(reportPath, outPath, { mine = '', lang = '' } = {}) {
  const dir = findViewerDir();
  if (!dir) throw new Error('viewer 폴더를 찾지 못했어요');
  const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
  let html = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
  const css = fs.readFileSync(path.join(dir, 'viewer.css'), 'utf8');
  const data = { report };
  if (mine) data.mine = loadMine(mine);
  if (lang === 'en' || lang === 'ko') data.lang = lang;
  html = html.replace(/<link rel="stylesheet" href="viewer\.css"\s*\/?>/, () => `<style>\n${css}\n</style>`);
  html = html.replace(/<script src="viewer\.js"><\/script>/, () => `<script>window.__REBIZ__ = ${safeJson(data)};</script>\n<script src="viewer.js"></script>`);
  html = html.replace(/<script src="(viewer|stage|sections)\.js"><\/script>/g, (m, name) => `<script>\n${closeSafe(fs.readFileSync(path.join(dir, `${name}.js`), 'utf8'))}\n</script>`);
  const out = outPath || path.join(path.dirname(path.resolve(reportPath)), 'report.html');
  fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
  fs.writeFileSync(out, html);
  return out;
}

export function openFile(file) {
  const cmd = process.platform === 'darwin' ? 'open' : process.platform === 'win32' ? 'cmd' : 'xdg-open';
  const args = process.platform === 'win32' ? ['/c', 'start', '', file] : [file];
  try {
    const child = spawn(cmd, args, { stdio: 'ignore', detached: true });
    child.on('error', () => {});
    child.unref();
    return true;
  } catch { return false; }
}

function main() {
  const args = process.argv.slice(2);
  const o = { open: false };
  for (let i = 0; i < args.length; i += 1) {
    const a = args[i];
    if (a === '--out') o.out = args[++i];
    else if (a === '--mine') o.mine = args[++i];
    else if (a === '--lang') o.lang = args[++i];
    else if (a === '--open') o.open = true;
    else if (!a.startsWith('--') && !o.file) o.file = a;
  }
  if (!o.file) {
    console.error('사용: node build-view.mjs <report.json> [--mine <내 버전 폴더>] [--out <report.html>] [--lang en] [--open]');
    process.exit(2);
  }
  try {
    const out = buildView(o.file, o.out, { mine: o.mine, lang: o.lang });
    console.log(`해부 화면: ${out}`);
    if (o.open) openFile(out);
    else console.log('브라우저로 이 파일을 열면 돼요 (더블클릭).');
  } catch (e) {
    console.error(`만들지 못했어요: ${e.message}`);
    process.exit(1);
  }
}

// 바로 실행했을 때만 돈다. 경로에 심볼릭 링크가 끼어 있어도 알아보도록 실제 경로로 견준다.
const direct = (() => { try { return fs.realpathSync(process.argv[1]) === fs.realpathSync(fileURLToPath(import.meta.url)); } catch { return false; } })();
if (direct) main();
