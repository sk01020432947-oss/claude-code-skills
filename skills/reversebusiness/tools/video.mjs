#!/usr/bin/env node
// 해부 영상(9:16, 1080x1920)을 사람이 브라우저를 열지 않아도 파일로 뽑는다. 의존성 없음.
// 사용: node video.mjs <report.json> [--out <파일>] [--mine <내 버전 폴더>] [--lang en]
//
// 하는 일: 해부 화면(report.html)을 임시 폴더에 만들고, 이 컴퓨터의 Chrome 계열 브라우저를 임시 프로필의 헤드리스 창으로 띄워
// 화면의 "영상으로 저장" 단추를 대신 누른다. 영상은 뷰어가 그리는 것 그대로이고, 길이만큼(약 30초) 걸린다.
// 지키는 것: 바깥으로 나가는 요청은 0. 브라우저의 이름 풀이를 막고, 페이지가 보내려는 http 요청도 모두 막는다.
// 끝나면 브라우저를 끄고 임시 프로필과 임시 폴더를 지운다. ffmpeg 를 쓰지 않는다.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { buildView } from './build-view.mjs';
import { findBrowser, launchBrowser } from './render.mjs';

export const VIDEO_LIMITS = { loadMs: 15000, recordMs: 90000, downloadMs: 20000 };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export class VideoStop extends Error {
  constructor(code, message) { super(message); this.code = code; }
}

// 파일 머리말을 읽어 형식과 크기를 확인한다 (mp4 의 tkhd, webm 의 PixelWidth/PixelHeight). 길이는 mp4 일 때만 잰다.
export function probeVideo(file) {
  const buf = fs.readFileSync(file);
  const out = { format: '', width: 0, height: 0, seconds: 0, bytes: buf.length };
  if (buf.length >= 12 && buf.toString('latin1', 4, 8) === 'ftyp') {
    out.format = 'mp4';
    let timescale = 0, total = 0, defDur = 0, trackHasVideo = false, videoScale = 0, whole = 0;
    const walk = (start, end, depth) => {
      let p = start;
      while (p + 8 <= end) {
        let size = buf.readUInt32BE(p);
        const type = buf.toString('latin1', p + 4, p + 8);
        let head = 8;
        if (size === 1 && p + 16 <= end) { size = Number(buf.readBigUInt64BE(p + 8)); head = 16; } else if (size === 0) size = end - p;
        if (size < head || p + size > end) break;
        const body = p + head;
        if (['moov', 'trak', 'mdia', 'moof', 'traf', 'mvex'].includes(type) && depth < 6) {
          if (type === 'trak') { trackHasVideo = false; timescale = 0; }
          walk(body, p + size, depth + 1);
          if (type === 'trak' && trackHasVideo && timescale) videoScale = timescale;
        } else if (type === 'tkhd') {
          const w = buf.readUInt32BE(p + size - 8) / 65536, h = buf.readUInt32BE(p + size - 4) / 65536;
          if (w > 0 && h > 0) { out.width = Math.round(w); out.height = Math.round(h); trackHasVideo = true; }
        } else if (type === 'mdhd') {
          const v = buf[body];
          timescale = buf.readUInt32BE(body + (v === 1 ? 20 : 12));
          const dur = v === 1 ? Number(buf.readBigUInt64BE(body + 24)) : buf.readUInt32BE(body + 16);
          if (trackHasVideo && timescale && dur && dur !== 0xffffffff) whole = Math.max(whole, dur / timescale);
        } else if (type === 'tfhd') {
          const flags = buf.readUInt32BE(body) & 0xffffff;
          let q = body + 8;
          if (flags & 0x1) q += 8;
          if (flags & 0x2) q += 4;
          defDur = flags & 0x8 ? buf.readUInt32BE(q) : 0;
        } else if (type === 'trun') {
          const flags = buf.readUInt32BE(body) & 0xffffff;
          const n = buf.readUInt32BE(body + 4);
          let q = body + 8;
          if (flags & 0x1) q += 4;
          if (flags & 0x4) q += 4;
          const step = (flags & 0x100 ? 4 : 0) + (flags & 0x200 ? 4 : 0) + (flags & 0x400 ? 4 : 0) + (flags & 0x800 ? 4 : 0);
          if (flags & 0x100) { for (let i = 0; i < n && q + 4 <= p + size; i += 1, q += step) total += buf.readUInt32BE(q); } else total += n * defDur;
        }
        p += size;
      }
    };
    try { walk(0, buf.length, 0); } catch { /* 읽은 데까지만 */ }
    // 조각으로 나뉜 파일(브라우저가 녹화한 것)은 조각마다 적힌 길이를 더한 값이 맞다. 조각이 없으면 머리말의 길이를 쓴다.
    out.seconds = total && videoScale ? total / videoScale : whole;
  } else if (buf.length >= 4 && buf.readUInt32BE(0) === 0x1a45dfa3) {
    out.format = 'webm';
    // Video 요소(0xE0) 안의 PixelWidth(0xB0), PixelHeight(0xBA) 를 앞부분에서 찾는다.
    const end = Math.min(buf.length, 65536);
    for (let p = 0; p + 8 < end && !(out.width && out.height); p += 1) {
      if (buf[p] === 0xb0 && buf[p + 1] === 0x82 && buf[p + 4] === 0xba && buf[p + 5] === 0x82) { out.width = buf.readUInt16BE(p + 2); out.height = buf.readUInt16BE(p + 6); }
    }
  }
  out.seconds = Math.round(out.seconds * 10) / 10;
  return out;
}

// 영상을 뽑는다. 돌려주는 것: { file, format, width, height, seconds, bytes, browser, blocked, closed }
export async function recordVideo(reportPath, { out = '', mine = '', lang = '', browser = findBrowser(), limits = {}, onStep = () => {} } = {}) {
  if (!browser) throw new VideoStop('no-browser', 'Chrome 계열 브라우저(Chrome, Chromium, Edge, Brave)를 찾지 못했어요.');
  const L = { ...VIDEO_LIMITS, ...limits };
  const work = fs.mkdtempSync(path.join(os.tmpdir(), 'rebiz-video-'));
  const dl = path.join(work, 'dl');
  fs.mkdirSync(dl);
  let B = null, closed = null;
  try {
    const page = buildView(reportPath, path.join(work, 'report.html'), { mine, lang });
    onStep(`${browser.name} 를 임시 프로필로 띄우는 중`);
    B = await launchBrowser({
      browser, limits: { width: 1280, height: 900 }, headless: true,
      // 그리기가 느려지지 않게 하고, 브라우저가 바깥 이름을 아예 풀지 못하게 한다.
      args: ['--autoplay-policy=no-user-gesture-required', '--disable-background-timer-throttling', '--disable-renderer-backgrounding', '--disable-backgrounding-occluded-windows', '--host-resolver-rules=MAP * ~NOTFOUND'],
    });
    const { cdp } = B;
    const withTimeout = (p, ms, what) => Promise.race([p, new Promise((_, no) => setTimeout(() => no(new Error(`${what} 시간 초과`)), ms))]);
    const stat = { blocked: 0, errors: [], download: null, done: false };
    await withTimeout(cdp.send('Browser.setDownloadBehavior', { behavior: 'allow', downloadPath: dl, eventsEnabled: true }), L.loadMs, '브라우저 초기화');
    const { targetId } = await withTimeout(cdp.send('Target.createTarget', { url: 'about:blank' }), L.loadMs, '새 탭 열기');
    const { sessionId } = await withTimeout(cdp.send('Target.attachToTarget', { targetId, flatten: true }), L.loadMs, '탭 연결');
    const S = (method, params) => withTimeout(cdp.send(method, params, sessionId), L.loadMs, method);
    let loaded = false;
    cdp.on((m) => {
      const p = m.params || {};
      if (m.method === 'Browser.downloadWillBegin') stat.download = { guid: p.guid, name: path.basename(String(p.suggestedFilename || 'video')) };
      else if (m.method === 'Browser.downloadProgress' && p.state === 'completed') stat.done = true;
      else if (m.method === 'Browser.downloadProgress' && p.state === 'canceled') stat.errors.push('저장이 취소됐어요');
      if (m.sessionId !== sessionId) return;
      if (m.method === 'Page.loadEventFired') loaded = true;
      else if (m.method === 'Runtime.exceptionThrown') stat.errors.push(String((p.exceptionDetails && (p.exceptionDetails.exception && p.exceptionDetails.exception.description || p.exceptionDetails.text)) || '화면 오류').split('\n')[0]);
      else if (m.method === 'Fetch.requestPaused') {
        // 내 컴퓨터의 파일이 아닌 요청은 보내지 않는다.
        const local = /^(file|data|blob|about):/i.test(String((p.request || {}).url || ''));
        if (!local) stat.blocked += 1;
        S(local ? 'Fetch.continueRequest' : 'Fetch.failRequest', local ? { requestId: p.requestId } : { requestId: p.requestId, errorReason: 'BlockedByClient' }).catch(() => {});
      }
    });
    const evaluate = async (expression) => { const r = await S('Runtime.evaluate', { expression, returnByValue: true, userGesture: true }); return r.result ? r.result.value : undefined; };
    await S('Page.enable');
    await S('Runtime.enable');
    await S('Fetch.enable', { patterns: [{ urlPattern: '*' }] });
    await S('Page.navigate', { url: pathToFileURL(page).href });
    for (let t = 0; !loaded && t < L.loadMs; t += 100) await sleep(100);
    let ready = false;
    for (let t = 0; !ready && t < L.loadMs; t += 200) { ready = !!(await evaluate('!!(window.RebizStage && window.RebizSections && document.getElementById("stage-save") && RebizSections.state && RebizSections.state().model)').catch(() => false)); if (!ready) await sleep(200); }
    if (!ready) throw new VideoStop('view-failed', `해부 화면을 열지 못했어요${stat.errors.length ? `: ${stat.errors[0]}` : '.'}`);
    if (!(await evaluate('RebizStage.canRecord()'))) throw new VideoStop('unsupported', '이 브라우저는 영상 저장(MediaRecorder)을 할 수 없어요.');
    const dur = Number(await evaluate('RebizStage.DUR')) || 30;
    onStep(`영상을 그리는 중 (약 ${Math.round(dur)}초 걸립니다)`);
    await evaluate('document.getElementById("stage-save").click()');
    let info = null, last = -1;
    for (let t = 0; !info && t < L.recordMs; t += 500) {
      await sleep(500);
      info = await evaluate('window.__rebizLastVideo || null');
      const pct = Number(await evaluate('parseInt(document.getElementById("rec-fill").style.width, 10) || 0'));
      const tenth = Math.floor(pct / 25);
      if (!info && tenth > last && pct < 100) { last = tenth; if (tenth > 0) onStep(`  ${tenth * 25}%`); }
      if (!info && t > 3000 && !(await evaluate('!document.getElementById("rec").hidden'))) throw new VideoStop('record-failed', `영상을 그리다 멈췄어요: ${(await evaluate('document.getElementById("stage-msg").textContent')) || '까닭을 알 수 없음'}`);
    }
    if (!info) throw new VideoStop('timeout', '영상 저장이 시간 한도를 넘었어요.');
    for (let t = 0; !stat.done && t < L.downloadMs; t += 200) await sleep(200);
    const name = stat.download ? stat.download.name : info.name;
    const got = [path.join(dl, name), ...fs.readdirSync(dl).filter((f) => !/\.crdownload$/i.test(f)).map((f) => path.join(dl, f))].find((f) => fs.existsSync(f));
    if (!got) throw new VideoStop('no-file', '브라우저가 영상 파일을 내려 주지 않았어요.');
    const ext = path.extname(got).toLowerCase() || '.mp4';
    // --out 이 폴더면 그 안에, 파일이면 그 이름으로. 확장자는 실제 형식에 맞춘다.
    let dest = out ? path.resolve(out) : path.join(path.dirname(path.resolve(reportPath)), path.basename(got));
    if (out && ((fs.existsSync(dest) && fs.statSync(dest).isDirectory()) || /[\\/]$/.test(out))) dest = path.join(dest, path.basename(got));
    let renamed = false;
    if (path.extname(dest).toLowerCase() !== ext) { dest = `${dest.replace(/\.[a-z0-9]{2,5}$/i, '')}${ext}`; renamed = !!out; }
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    const overwrote = fs.existsSync(dest);
    fs.copyFileSync(got, dest);
    closed = await B.close();
    B = null;
    return { file: dest, ...probeVideo(dest), expectedSeconds: dur, browser: browser.name, blocked: stat.blocked, errors: stat.errors, renamed, overwrote, closed };
  } finally {
    if (B) { try { await B.close(); } catch { /* 이미 꺼짐 */ } }
    try { fs.rmSync(work, { recursive: true, force: true }); } catch { /* 임시 폴더는 운영체제가 지운다 */ }
  }
}

async function main() {
  const args = process.argv.slice(2);
  const o = {};
  for (let i = 0; i < args.length; i += 1) {
    const a = args[i];
    if (a === '--out') o.out = args[++i];
    else if (a === '--mine') o.mine = args[++i];
    else if (a === '--lang') o.lang = args[++i];
    else if (!a.startsWith('--') && !o.file) o.file = a;
    else o.bad = a;
  }
  const usage = '사용: node video.mjs <report.json> [--out <파일>] [--mine <내 버전 폴더>] [--lang en]';
  if (o.bad || !o.file) { if (o.bad) console.error(`모르는 인자: ${o.bad}`); console.error(usage); process.exit(2); }
  try {
    const r = await recordVideo(o.file, { out: o.out, mine: o.mine, lang: o.lang, onStep: (s) => console.log(s) });
    console.log(`영상: ${r.file}  (${r.format}, ${r.width}x${r.height}${r.seconds ? `, ${r.seconds}초` : ''}, ${(r.bytes / 1048576).toFixed(1)} MB)`);
  } catch (e) {
    console.error(`영상을 뽑지 못했어요: ${e.message}`);
    if (e.code === 'no-browser' || e.code === 'unsupported') console.error('대신: build-view.mjs 로 해부 화면을 열고 "영상으로 저장 (9:16)" 단추를 누르세요.');
    process.exit(e.code === 'no-browser' ? 3 : 1);
  }
}

// 바로 실행했을 때만 돈다. 경로에 심볼릭 링크가 끼어 있어도 알아보도록 실제 경로로 견준다.
const direct = (() => { try { return fs.realpathSync(process.argv[1]) === fs.realpathSync(fileURLToPath(import.meta.url)); } catch { return false; } })();
if (direct) await main();
