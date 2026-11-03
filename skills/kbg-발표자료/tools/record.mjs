#!/usr/bin/env node
// kbg 발표자료 녹화기 — 의존성 없음(Node 22+ 내장 WebSocket + 크롬 + ffmpeg).
//   node record.mjs 발표.html 발표.mp4 [--fps 30] [--audio 음성.mp3] [--nosubs]
//   node record.mjs 발표.html 유인물.pdf              (장면마다 한 쪽, 마지막 박자 상태)
//   node record.mjs 발표.html --shots 폴더      (장면마다 마지막 박자 PNG — 검수용, --beats 붙이면 박자마다)
// 엔진의 KBG_seek(t)로 프레임을 하나씩 결정적으로 그려 찍는다. 실시간 화면 녹화가 아니라 프레임이 빠지지 않는다.
import { spawn } from 'node:child_process';
import { mkdtempSync, mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve, join } from 'node:path';

const a = process.argv.slice(2), opt = k => { const i = a.indexOf(k); return i < 0 ? null : (a[i + 1] ?? true); };
const html = resolve(a[0]), out = a[1] && !a[1].startsWith('--') ? resolve(a[1]) : null;
const fps = +(opt('--fps') || 30), audio = opt('--audio'), shots = opt('--shots');
if (!existsSync(html) || (!out && !shots)) { console.error('사용: node record.mjs 발표.html 발표.mp4 | --shots 폴더'); process.exit(1); }
const CHROME = process.env.CHROME || ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium', '/Applications/Aside.app/Contents/MacOS/Aside'].find(existsSync);
const port = 9400 + Math.floor(Math.random() * 400);
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${mkdtempSync(join(tmpdir(), 'kbgrec-'))}`,
  '--hide-scrollbars', '--window-size=1920,1080', '--force-device-scale-factor=1', '--disable-gpu', '--no-first-run', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let list; for (let i = 0; i < 100 && !list; i++) { await sleep(150); list = await fetch(`http://127.0.0.1:${port}/json/list`).then(r => r.json()).catch(() => null); }
const ws = new WebSocket(list.find(t => t.type === 'page').webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);
let id = 0; const wait = new Map(), events = [];
ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id) wait.get(d.id)?.(d); else events.push(d.method); };
const cdp = (method, params = {}) => new Promise((ok, no) => { const i = ++id; wait.set(i, d => d.error ? no(new Error(method + ': ' + d.error.message)) : ok(d.result)); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async js => (await cdp('Runtime.evaluate', { expression: js, awaitPromise: true, returnByValue: true })).result.value;

await cdp('Page.enable');
await cdp('Emulation.setDeviceMetricsOverride', { width: 1920, height: 1080, deviceScaleFactor: 1, mobile: false });
await cdp('Page.navigate', { url: 'file://' + html + '?seek=1' + (a.includes('--nosubs') ? '&nosubs' : '') });
while (!events.includes('Page.loadEventFired')) await sleep(50);
const total = await ev('document.fonts.ready.then(()=>new Promise(r=>setTimeout(r,400))).then(()=>window.KBG_TOTAL)');
if (!total) throw new Error('KBG 엔진이 없는 HTML입니다');
const shot = async (fmt = 'jpeg') => Buffer.from((await cdp('Page.captureScreenshot', { format: fmt, quality: 92 })).data, 'base64');

const pdf = out?.toLowerCase().endsWith('.pdf');
if (shots || pdf) {
  if (shots) mkdirSync(shots, { recursive: true });
  const tl = await ev('KBG_TL.map(b=>[b.si,b.t,b.d])'), last = {};
  // --beats: 박자마다 한 장 (카메라 이동 검수용)
  if (process.argv.includes('--beats')) tl.forEach(([si, t, d], k) => last[`${si}-${k}`] = t + d - 0.05);
  else for (const [si, t, d] of tl) last[si] = t + d - 0.05;
  const pages = [];
  for (const [si, t] of Object.entries(last)) {
    await ev(`KBG_seek(${t})`); await sleep(60); const png = await shot('png');
    if (shots) writeFileSync(join(shots, `장면${String(parseInt(si) + 1).padStart(2, '0')}${si.includes('-') ? '-' + si.split('-')[1].padStart(3, '0') : ''}.png`), png);
    else pages.push(png.toString('base64'));
  }
  if (pdf) { // 찍은 장면을 한 쪽씩 붙여 PDF로 — 화면과 똑같이 나온다
    const doc = join(mkdtempSync(join(tmpdir(), 'kbgpdf-')), 'p.html');
    writeFileSync(doc, `<style>@page{size:1920px 1080px;margin:0}body{margin:0}img{display:block;width:1920px;height:1080px;break-after:page}</style>` + pages.map(b => `<img src="data:image/png;base64,${b}">`).join(''));
    events.length = 0; await cdp('Page.navigate', { url: 'file://' + doc }); while (!events.includes('Page.loadEventFired')) await sleep(50);
    writeFileSync(out, Buffer.from((await cdp('Page.printToPDF', { printBackground: true, preferCSSPageSize: true, marginTop: 0, marginBottom: 0, marginLeft: 0, marginRight: 0 })).data, 'base64'));
  }
  console.log(`${Object.keys(last).length}장 → ${shots || out}`);
} else {
  const n = Math.ceil(total * fps);
  const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-', ...(audio ? ['-i', resolve(audio), '-c:a', 'aac', '-shortest'] : []),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = 0; f < n; f++) {
    await ev(`KBG_seek(${(f / fps).toFixed(4)})`);
    if (!ff.stdin.write(await shot())) await new Promise(r => ff.stdin.once('drain', r));
    if (f % (fps * 10) === 0) process.stdout.write(`\r${(f / fps).toFixed(0)}s / ${total.toFixed(0)}s`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  console.log(`\n완료 ${total.toFixed(1)}초 → ${out}`);
}
ws.close(); chrome.kill();
