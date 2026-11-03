// 고품질 렌더: 1080p(배율) + 서브프레임 모션블러 + music.wav 자동 합성
// 사용: node render_hq.mjs <샘플폴더|index.html> [--scale 1.5] [--sub 4] [--shutter 0.5] [--crf 16] [--fps 30] [--card 톤카드] [--no-qa]  (4K60: --scale 3 --fps 60)
// 출력: <폴더>/clip_hq.mp4 (music.wav가 있으면 소리 포함)
import { createRequire } from 'module';
import { createServer } from 'http';
import { spawn, spawnSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import os from 'os';

const require = createRequire(path.join(os.homedir(), 'DEV/awesome-ai-motion/package.json'));
const { chromium } = require('playwright');
const LIB = path.join(os.homedir(), 'DEV/awesome-ai-motion/lib');

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
let target = path.resolve(args.find((a, i) => !a.startsWith('--') && !(args[i - 1] || '').startsWith('--') || args[i - 1] === '--no-qa') || '.');  // 옵션 값(--card 이름 등)은 건너뜀
if (fs.statSync(target).isDirectory()) target = path.join(target, 'index.html');
const dir = path.dirname(target);
const SCALE = +opt('scale', 1.5), SUB = +opt('sub', 4), SHUTTER = +opt('shutter', 0.5), CRF = opt('crf', '16'), FPS = +opt('fps', 30);

const mime = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.ttf': 'font/ttf', '.otf': 'font/otf', '.woff2': 'font/woff2', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg' };
const html = fs.readFileSync(target, 'utf8').replace(/\b(src|href)\s*=\s*(["'])(?:\/|(?:\.{1,2}\/)*)lib\/([^"']+)\2/gi, (_, a, q, r) => `${a}=${q}/__lib/${r}${q}`);
const server = createServer((req, res) => {
  const p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p === '/' || p === '/index.html') { res.writeHead(200, { 'Content-Type': mime['.html'] }); return res.end(html); }
  const base = p.startsWith('/__lib/') ? LIB : dir, rel = p.startsWith('/__lib/') ? p.slice(7) : p.slice(1);
  const f = path.resolve(base, rel);
  if (!f.startsWith(base) || !fs.existsSync(f) || !fs.statSync(f).isFile()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': mime[path.extname(f)] || 'application/octet-stream' }); res.end(fs.readFileSync(f));
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const url = `http://127.0.0.1:${server.address().port}/index.html?render=1&embed=1`;

const browser = await chromium.launch();
let page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: SCALE });
await page.goto(url);
await page.waitForFunction(() => window.__ready === true, null, { timeout: 30000 });
const { dur, size } = await page.evaluate(() => ({ dur: window.__dur, size: window.__size || [1280, 720] }));
if (size[0] !== 1280 || size[1] !== 720) await page.setViewportSize({ width: size[0], height: size[1] });
const W = Math.round(size[0] * SCALE / 2) * 2, H = Math.round(size[1] * SCALE / 2) * 2;
const frames = Math.round(dur * FPS);

const out = path.join(dir, 'clip_hq.mp4'), music = path.join(dir, 'music.wav');
const vf = SUB > 1
  ? `scale=${W}:${H},tmix=frames=${SUB},select='eq(mod(n\\,${SUB})\\,${SUB - 1})',setpts=N/${FPS}/TB`
  : `scale=${W}:${H}`;
const ff = ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS * SUB), '-i', '-'];
if (fs.existsSync(music)) ff.push('-i', music);
ff.push('-vf', vf, '-r', String(FPS), '-c:v', 'libx264', '-preset', 'slow', '-crf', CRF, '-pix_fmt', 'yuv420p');
if (fs.existsSync(music)) ff.push('-c:a', 'aac', '-b:a', '192k', '-shortest');
ff.push('-movflags', '+faststart', out);
const proc = spawn('ffmpeg', ff, { stdio: ['pipe', 'inherit', 'inherit'] });

const t0 = Date.now();
for (let f = 0; f < frames; f++) {
  for (let s = 0; s < SUB; s++) {
    // 셔터: 마지막 서브프레임이 정확히 f/FPS → 정지 화면은 선명하게 남는다
    const t = Math.max(0, (f + (SUB > 1 ? (s / (SUB - 1) - 1) * SHUTTER : 0)) / FPS);
    await page.evaluate(x => window.__seek(x), t);
    const buf = await page.screenshot({ type: 'jpeg', quality: 94 });
    if (!proc.stdin.write(buf)) await new Promise(r => proc.stdin.once('drain', r));
  }
}
proc.stdin.end();
await new Promise((r, j) => proc.on('close', c => c === 0 ? r() : j(new Error('ffmpeg ' + c))));
await browser.close(); server.close();
console.log(`OK ${out}  ${W}x${H} ${frames}f sub${SUB}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);

// 렌더 후 숫자 검수(motion-tone-qa). 톤 카드: --card 이름 > 폴더의 tone_card.txt. 끄기: --no-qa
// FIX가 나와도 렌더는 성공으로 둔다. 결과는 <폴더>/tone_qa.txt, 24컷은 clip_hq_24컷.png
const QA = path.join(os.homedir(), '.claude/skills/motion-tone-qa/scripts/measure.py');
if (!args.includes('--no-qa') && fs.existsSync(QA)) {
  const cardFile = path.join(dir, 'tone_card.txt');
  const card = opt('card', fs.existsSync(cardFile) ? fs.readFileSync(cardFile, 'utf8').trim() : '');
  const r = spawnSync('python3', [QA, out, '--sheet', ...(card ? ['--card', card] : [])], { encoding: 'utf8' });
  fs.writeFileSync(path.join(dir, 'tone_qa.txt'), (r.stdout || '') + (r.stderr || ''));
  const verdict = !card ? '톤 카드 없음, 측정만'
    : (r.stdout || '').match(/(PASS|FIX)[\s\S]*/)?.[0].trim() || `오류: ${(r.stderr || '').trim().split('\n').pop()}`;
  console.log(`QA ${card || '-'}: ${verdict}`);
}
