// 그려진 화면 읽기: 이 컴퓨터의 Chrome 계열 브라우저를 임시 프로필로 잠깐 띄워, 스크립트가 그린 뒤의 화면을 읽는다.
// 의존성 없음. macOS/Linux 에서는 파이프(--remote-debugging-pipe)로, Windows 에서는 127.0.0.1 루프백 웹소켓으로만 말한다.
//
// 지키는 것:
//   - 임시 프로필만 쓴다. 평소 브라우저의 쿠키, 로그인, 확장 프로그램을 쓰지 않는다. 끝나면 브라우저를 끄고 임시 폴더를 지운다.
//   - 입력하지 않고, 내려받지 않는다. 화면 캡처를 찍지 않는다. 누르는 것은 정밀 모드의 흐름 읽기에서만,
//     그것도 펼치기(자주 묻는 질문, 탭, 더 보기)뿐이다. 폼, 로그인, 가입, 결제, 구매 단추와 다른 페이지로 가는 링크는 누르지 않는다.
//   - 브라우저 안에서 나가는 요청도 거른다: GET 이 아닌 요청, robots.txt 가 막은 주소, 로그인과 결제 주소,
//     다른 사이트로 넘어가기, 분석과 광고 도구, 끼워 넣은 다른 페이지, 영상 파일은 보내지 않는다.
//   - 쿠키를 돌려보내지 않는다 (요청을 내보내기 직전마다 쿠키를 비우고, 페이지 스크립트의 쿠키 쓰기를 끈다).
//   - 저장소의 값을 읽지 않는다. 읽는 것은 그려진 화면의 글자, 구조, 구역의 위치와 크기뿐이다.
import fs from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import { randomBytes } from 'node:crypto';
import { spawn, spawnSync } from 'node:child_process';

export const RENDER_LIMITS = { startMs: 25000, navMs: 20000, settleMs: 5000, idleMs: 700, growMs: 2500, maxRequests: 300, maxHeight: 12000, width: 1440, height: 900, flowClicks: 8, clickSettleMs: 1500, scriptBytes: 8_000_000 };

const MAC = [
  ['Google Chrome', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'],
  ['Chromium', '/Applications/Chromium.app/Contents/MacOS/Chromium'],
  ['Microsoft Edge', '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'],
  ['Brave', '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'],
];
const LINUX = [['Google Chrome', 'google-chrome'], ['Google Chrome', 'google-chrome-stable'], ['Chromium', 'chromium'], ['Chromium', 'chromium-browser'], ['Microsoft Edge', 'microsoft-edge'], ['Brave', 'brave-browser']];
const WIN = [
  ['Google Chrome', 'Google\\Chrome\\Application\\chrome.exe'],
  ['Microsoft Edge', 'Microsoft\\Edge\\Application\\msedge.exe'],
  ['Brave', 'BraveSoftware\\Brave-Browser\\Application\\brave.exe'],
  ['Chromium', 'Chromium\\Application\\chrome.exe'],
];
const isFile = (p) => { try { return fs.statSync(p).isFile(); } catch { return false; } };

// 이 컴퓨터에서 쓸 수 있는 브라우저를 찾는다. REBIZ_BROWSER=none 이면 없는 것으로 본다.
export function findBrowser({ env = process.env, platform = process.platform, home = os.homedir() } = {}) {
  const forced = env.REBIZ_BROWSER || env.CHROME_PATH || '';
  if (forced === 'none') return null;
  if (forced) return isFile(forced) ? { name: path.basename(forced), path: forced } : null;
  if (platform === 'darwin') {
    for (const [name, p] of MAC) for (const base of ['', home]) if (isFile(base + p)) return { name, path: base + p };
  } else if (platform === 'win32') {
    const roots = [env.PROGRAMFILES, env['PROGRAMFILES(X86)'], env.PROGRAMW6432, env.LOCALAPPDATA].filter(Boolean);
    for (const [name, p] of WIN) for (const r of roots) if (isFile(path.join(r, p))) return { name, path: path.join(r, p) };
  } else {
    const dirs = String(env.PATH || '').split(path.delimiter).filter(Boolean);
    for (const [name, bin] of LINUX) for (const d of dirs) if (isFile(path.join(d, bin))) return { name, path: path.join(d, bin) };
  }
  return null;
}

// 분석, 광고, 채팅 도구: 화면을 읽는 데 필요 없고, 방문 통계를 흐리지 않도록 부르지 않는다.
const TRACKERS = /(^|\.)(google-analytics\.com|googletagmanager\.com|doubleclick\.net|googlesyndication\.com|googleadservices\.com|facebook\.net|connect\.facebook\.com|clarity\.ms|hotjar\.com|hotjar\.io|segment\.(io|com)|amplitude\.com|mixpanel\.com|sentry\.io|fullstory\.com|intercom\.io|intercomcdn\.com|channel\.io|criteo\.(com|net)|analytics\.tiktok\.com|analytics\.twitter\.com|ads-twitter\.com|px\.ads\.linkedin\.com|snap\.licdn\.com|wcs\.naver\.(net|com)|datadoghq\.com|newrelic\.com|nr-data\.net|posthog\.com|plausible\.io|braze\.com|airbridge\.io|appsflyer\.com)$/i;
export const isTracker = (hostname) => TRACKERS.test(String(hostname || ''));

// 그려진 화면에서 글자와 구조, 구역의 위치와 크기를 읽는 짧은 스크립트. 아무것도 누르지 않는다.
const EXTRACT = `(() => {
  const de = document.documentElement, body = document.body;
  const out = { html: '', blocks: [], docH: 0, docW: innerWidth, url: location.href };
  if (!de || !body) return out;
  const W = innerWidth;
  out.docH = Math.max(de.scrollHeight, body.scrollHeight);
  const rect = (el) => el.getBoundingClientRect();
  const vis = (el) => {
    if (!(el instanceof HTMLElement) || /^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE|LINK|META)$/.test(el.tagName)) return false;
    const r = rect(el), cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || Number(cs.opacity) === 0) return false;
    if (r.height < 20 || r.width < W * 0.3) return false;
    if (cs.position === 'fixed' || cs.position === 'sticky') return r.top + scrollY < 8 && r.height < 220;
    return true;
  };
  let list = [...body.children].filter(vis);
  for (let step = 0; step < 16 && list.length && list.length < 14; step++) {
    let big = null;
    for (const el of list) { const h = rect(el).height; if (!big || h > big.h) big = { el, h }; }
    const kids = [...big.el.children].filter(vis);
    if (list.length === 1) { if (!kids.length) break; list = kids; continue; }
    const sum = kids.reduce((a, k) => a + rect(k).height, 0);
    if (big.h / out.docH < 0.3 || kids.length < 2 || sum > big.h * 1.3 || sum < big.h * 0.5) break;
    list.splice(list.indexOf(big.el), 1, ...kids);
  }
  list.sort((a, b) => rect(a).top - rect(b).top);
  out.blocks = list.slice(0, 18).map((el, i) => { el.setAttribute('data-rebiz-b', String(i)); const r = rect(el); return { i, top: Math.round(r.top + scrollY), height: Math.round(r.height) }; });
  out.html = de.outerHTML.slice(0, 3000000);
  return out;
})()`;

function cdpPipe(child) {
  const toBrowser = child.stdio[3], fromBrowser = child.stdio[4];
  let seq = 0, buf = Buffer.alloc(0), closed = false;
  const pending = new Map();
  const handlers = new Set();
  fromBrowser.on('data', (chunk) => {
    buf = Buffer.concat([buf, chunk]);
    for (let i = buf.indexOf(0); i >= 0; i = buf.indexOf(0)) {
      const raw = buf.subarray(0, i).toString('utf8');
      buf = buf.subarray(i + 1);
      let m;
      try { m = JSON.parse(raw); } catch { continue; }
      if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); if (m.error) p.no(new Error(m.error.message)); else p.ok(m.result); } else for (const h of handlers) h(m);
    }
  });
  const fail = () => { closed = true; for (const p of pending.values()) p.no(new Error('browser closed')); pending.clear(); };
  fromBrowser.on('close', fail);
  toBrowser.on('error', fail);
  child.on('exit', fail);
  return {
    send(method, params = {}, sessionId) {
      if (closed) return Promise.reject(new Error('browser closed'));
      return new Promise((ok, no) => {
        const id = ++seq;
        pending.set(id, { ok, no });
        try { toBrowser.write(`${JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) })}\0`); } catch (e) { pending.delete(id); no(e); }
      });
    },
    on(fn) { handlers.add(fn); return () => handlers.delete(fn); },
    close: fail,
  };
}

// Windows 등 파이프를 못 쓰는 환경에서 127.0.0.1 루프백 웹소켓으로만 CDP 통신을 연다. 의존성 없음.
export function connectCdpWs(port, wsPath, timeoutMs = 12000) {
  return new Promise((resolve, reject) => {
    let seq = 0, closed = false, upgraded = false, buf = Buffer.alloc(0), frag = [];
    const pending = new Map();
    const handlers = new Set();
    const sock = net.connect(port, '127.0.0.1');
    const timer = setTimeout(() => { sock.destroy(); reject(new Error('브라우저 WebSocket 시간 초과')); }, timeoutMs);
    const fail = () => {
      if (closed) return;
      closed = true;
      for (const p of pending.values()) p.no(new Error('browser closed'));
      pending.clear();
      sock.destroy();
    };
    const sendFrame = (opcode, data) => {
      const payload = Buffer.isBuffer(data) ? data : Buffer.from(String(data), 'utf8');
      const mask = randomBytes(4);
      const len = payload.length;
      const hdr = len < 126 ? Buffer.alloc(6) : len < 65536 ? Buffer.alloc(8) : Buffer.alloc(14);
      hdr[0] = 0x80 | opcode;
      let off = 2;
      if (len < 126) hdr[1] = 0x80 | len;
      else if (len < 65536) { hdr[1] = 0x80 | 126; hdr.writeUInt16BE(len, 2); off = 4; }
      else { hdr[1] = 0x80 | 127; hdr.writeBigUInt64BE(BigInt(len), 2); off = 10; }
      mask.copy(hdr, off);
      const masked = Buffer.allocUnsafe(len);
      for (let i = 0; i < len; i += 1) masked[i] = payload[i] ^ mask[i & 3];
      sock.write(Buffer.concat([hdr, masked]));
    };
    const drain = () => {
      while (buf.length >= 2) {
        const b0 = buf[0], b1 = buf[1], fin = (b0 & 0x80) !== 0, opcode = b0 & 0x0f;
        let len = b1 & 0x7f, off = 2;
        if (len === 126) { if (buf.length < 4) return; len = buf.readUInt16BE(2); off = 4; }
        else if (len === 127) { if (buf.length < 10) return; len = Number(buf.readBigUInt64BE(2)); off = 10; }
        const maskOff = (b1 & 0x80) ? 4 : 0;
        if (buf.length < off + maskOff + len) return;
        let body = buf.subarray(off + maskOff, off + maskOff + len);
        if (maskOff) { const m = buf.subarray(off, off + 4); body = Buffer.from(body); for (let i = 0; i < len; i += 1) body[i] ^= m[i & 3]; }
        buf = buf.subarray(off + maskOff + len);
        if (opcode === 0x8) { fail(); return; }
        if (opcode === 0x9) { sendFrame(0xA, body); continue; }
        if (opcode === 0xA) continue;
        frag.push(body);
        if (!fin) continue;
        const raw = Buffer.concat(frag).toString('utf8');
        frag = [];
        let m;
        try { m = JSON.parse(raw); } catch { continue; }
        if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); if (m.error) p.no(new Error(m.error.message)); else p.ok(m.result); }
        else for (const h of handlers) h(m);
      }
    };
    sock.on('error', (e) => { clearTimeout(timer); if (!upgraded) reject(e); fail(); });
    sock.on('close', () => { clearTimeout(timer); if (!upgraded) reject(new Error('browser closed')); fail(); });
    sock.on('connect', () => {
      const key = randomBytes(16).toString('base64');
      sock.write(`GET ${wsPath} HTTP/1.1\r\nHost: 127.0.0.1:${port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: ${key}\r\nSec-WebSocket-Version: 13\r\n\r\n`);
    });
    sock.on('data', (chunk) => {
      buf = Buffer.concat([buf, chunk]);
      if (!upgraded) {
        const idx = buf.indexOf('\r\n\r\n');
        if (idx < 0) return;
        const head = buf.subarray(0, idx).toString('utf8');
        if (!/^HTTP\/1\.1 101\b/i.test(head)) { clearTimeout(timer); sock.destroy(); reject(new Error('WebSocket 연결 실패')); return; }
        upgraded = true;
        clearTimeout(timer);
        buf = buf.subarray(idx + 4);
        resolve({
          send(method, params = {}, sessionId) {
            if (closed) return Promise.reject(new Error('browser closed'));
            return new Promise((ok, no) => {
              const id = ++seq;
              pending.set(id, { ok, no });
              try { sendFrame(0x1, JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) })); } catch (e) { pending.delete(id); no(e); }
            });
          },
          on(fn) { handlers.add(fn); return () => handlers.delete(fn); },
          close: fail,
        });
      }
      drain();
    });
  });
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const withTimeout = (p, ms, what) => Promise.race([p, new Promise((_, no) => setTimeout(() => no(new Error(`${what} 시간 초과`)), ms))]);

// 흐름 읽기에서 누를 곳을 고른다: 접힌 글, 고르지 않은 탭, 펼침 단추, "더 보기". 그 밖의 것은 누르지 않는다.
const PICK = (max) => `(() => {
  const BAD = /(로그인|log\\s?in|sign\\s?in|sign\\s?up|가입|결제|구매|주문|신청|구독|장바구니|담기|buy|purchase|checkout|subscribe|order|pay|cart|submit|send|제출|보내기|전송|다운로드|download|삭제|delete|동의|accept|agree|공유|share|문의|contact|예약|book|시작하기|get started|start|try|체험|로그아웃|logout)/i;
  const GOOD = /(가격|요금|플랜|plan|pricing|월간|연간|monthly|yearly|annual|더\\s?보기|see more|show more|read more|view more|자주\\s?묻는|faq|자세히|펼치기)/i;
  const seen = new Set(), picks = [], cap = { details: 4, tab: 3, expand: 2, more: 2 }, used = {};
  const label = (el) => (el.innerText || el.getAttribute('aria-label') || '').trim().slice(0, 60);
  const ok = (el) => {
    if (!(el instanceof HTMLElement) || el.closest('form') || el.disabled) return false;
    if (el.tagName === 'A' || el.closest('a[href]')) { const a = el.tagName === 'A' ? el : el.closest('a[href]'); const h = a.getAttribute('href') || ''; if (h && !h.startsWith('#')) return false; }
    if (el.form || el.getAttribute('type') === 'submit' || el.getAttribute('type') === 'reset') return false; // 폼에 딸린 단추는 누르지 않는다
    if (el.tagName === 'INPUT' || el.tagName === 'SELECT' || el.tagName === 'TEXTAREA') return false;
    const r = el.getBoundingClientRect();
    if (r.width < 8 || r.height < 8) return false;
    return !BAD.test(label(el));
  };
  const add = (el, kind) => { if (seen.has(el) || (used[kind] || 0) >= cap[kind] || !ok(el)) return; seen.add(el); used[kind] = (used[kind] || 0) + 1; picks.push({ el, kind }); };
  document.querySelectorAll('[role="tab"][aria-selected="false"]').forEach((el) => add(el, 'tab'));
  document.querySelectorAll('summary').forEach((el) => { if (el.parentElement && !el.parentElement.open) add(el, 'details'); });
  document.querySelectorAll('button[aria-expanded="false"], [role="button"][aria-expanded="false"]').forEach((el) => add(el, 'expand'));
  document.querySelectorAll('button, [role="button"]').forEach((el) => { const t = label(el); if (el.getAttribute('role') !== 'tab' && t.length <= 24 && GOOD.test(t)) add(el, 'more'); });
  window.__rebizPicks = picks.slice(0, ${max});
  return window.__rebizPicks.map((p) => p.kind);
})()`;
const CLICK = (i) => `(() => { const p = (window.__rebizPicks || [])[${i}]; if (!p || !p.el.isConnected) return false; p.el.click(); return true; })()`;

// 창 띄우기 여부: 명시값 > REBIZ_HEADLESS/CI 환경 > 디스플레이 없는 Linux 면 헤드리스, 데스크톱에서는 기본적으로 실제 Chrome 창을 띄운다.
export function shouldBeHeadless({ headless, env = process.env, platform = process.platform } = {}) {
  if (typeof headless === 'boolean') return headless;
  if (env.REBIZ_HEADLESS === '1' || env.CI === 'true' || env.GITHUB_ACTIONS === 'true') return true;
  if (platform === 'linux' && !env.DISPLAY && !env.WAYLAND_DISPLAY) return true;
  return false;
}

const VISUAL_HUD = (title, sub = '') => `(() => {
  if (!document.body) return;
  let st = document.getElementById('rebiz-hud-style');
  if (!st) {
    st = document.createElement('style');
    st.id = 'rebiz-hud-style';
    st.textContent = \`
      @keyframes rebizPulse { 0%,100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.4); opacity: 0.45; } }
      #rebiz-hud { position: fixed; right: 20px; bottom: 20px; z-index: 2147483647; pointer-events: none; display: flex; align-items: center; gap: 11px; padding: 11px 16px; border-radius: 12px; background: rgba(12,13,18,0.92); color: #f3efe6; border: 1px solid rgba(228,186,117,0.48); box-shadow: 0 12px 32px rgba(0,0,0,0.45); font: 500 13px/1.35 ui-sans-serif, -apple-system, BlinkMacSystemFont, sans-serif; backdrop-filter: blur(10px); max-width: 360px; }
      #rebiz-hud .rebiz-dot { width: 9px; height: 9px; border-radius: 50%; background: #e4ba75; flex: 0 0 auto; animation: rebizPulse 1.2s ease-in-out infinite; }
      #rebiz-hud .rebiz-kicker { font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase; color: #e4ba75; font-weight: 700; }
      #rebiz-hud .rebiz-msg { color: #f3efe6; font-size: 13px; margin-top: 2px; }
      [data-rebiz-ring] { outline: 2px solid rgba(228,186,117,0.9) !important; outline-offset: 3px !important; box-shadow: 0 0 0 6px rgba(228,186,117,0.16) !important; transition: box-shadow 0.25s ease, outline-color 0.25s ease !important; }
    \`;
    (document.head || document.documentElement).appendChild(st);
  }
  let hud = document.getElementById('rebiz-hud');
  if (!hud) {
    hud = document.createElement('div');
    hud.id = 'rebiz-hud';
    hud.innerHTML = '<span class="rebiz-dot"></span><div><div class="rebiz-kicker"></div><div class="rebiz-msg"></div></div>';
    document.body.appendChild(hud);
  }
  hud.querySelector('.rebiz-kicker').textContent = ${JSON.stringify(String(title || 'reversebusiness'))};
  hud.querySelector('.rebiz-msg').textContent = ${JSON.stringify(String(sub || ''))};
})()`;

const VISUAL_SCAN = `(() => {
  const nodes = [...document.querySelectorAll('header, main > section, section, article, footer')].filter((el) => {
    const r = el.getBoundingClientRect();
    return r.height >= 48 && r.width >= innerWidth * 0.35;
  }).slice(0, 7);
  nodes.forEach((el, idx) => setTimeout(() => { el.setAttribute('data-rebiz-ring', '1'); }, idx * 90));
  window.scrollTo({ top: Math.min(Math.max(0, document.documentElement.scrollHeight - innerHeight), Math.round(innerHeight * 0.75)), behavior: 'smooth' });
  setTimeout(() => { window.scrollTo({ top: 0, behavior: 'smooth' }); }, 460);
  return nodes.length;
})()`;

const VISUAL_MARK_CLICK = (i) => `(() => {
  document.querySelectorAll('[data-rebiz-ring]').forEach((n) => n.removeAttribute('data-rebiz-ring'));
  const p = (window.__rebizPicks || [])[${i}];
  if (!p || !p.el || !p.el.isConnected) return false;
  p.el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  p.el.setAttribute('data-rebiz-ring', '1');
  return true;
})()`;

const VISUAL_CLEANUP = `(() => {
  document.querySelectorAll('[data-rebiz-ring]').forEach((n) => n.removeAttribute('data-rebiz-ring'));
  const hud = document.getElementById('rebiz-hud'); if (hud) hud.remove();
  const st = document.getElementById('rebiz-hud-style'); if (st) st.remove();
  window.scrollTo(0, 0);
})()`;

// 브라우저만 띄운다: 임시 프로필, 헤드리스(또는 데스크톱 라이브 창), 연결. close() 가 브라우저를 끄고 임시 프로필을 지운다.
// 그려 읽기(openRenderer)와 영상 뽑기(video.mjs)가 함께 쓴다.
export async function launchBrowser({ browser = findBrowser(), limits = {}, debugPort = false, headless, args = [] } = {}) {
  if (!browser) throw new Error('브라우저를 찾지 못했어요');
  const L = { ...RENDER_LIMITS, ...limits };
  const isHeadless = shouldBeHeadless({ headless });
  const rawProfile = fs.mkdtempSync(path.join(os.tmpdir(), 'rebiz-render-'));
  const profile = process.platform === 'win32' ? (fs.realpathSync.native ? fs.realpathSync.native(rawProfile) : fs.realpathSync(rawProfile)) : rawProfile;
  const childEnv = { ...process.env };
  if (process.platform === 'win32' && childEnv.LOCALAPPDATA && /[\\/]AppData[\\/]Local$/i.test(childEnv.LOCALAPPDATA)) {
    // 테스트 등에서 USERPROFILE 만 임시 폴더로 바꿨을 때 Chrome 136+ 의 기본 데이터 폴더 검증이 실패하지 않게 맞춘다 (프로필은 --user-data-dir 로 격리됨).
    childEnv.USERPROFILE = path.resolve(childEnv.LOCALAPPDATA, '..', '..');
  }
  const usePipe = process.platform !== 'win32';
  const needPort = !usePipe || debugPort;
  const child = spawn(browser.path, [
    ...(isHeadless ? ['--headless=new'] : ['--new-window', '--window-position=80,60']),
    ...(usePipe ? ['--remote-debugging-pipe'] : []),
    ...(needPort ? ['--remote-debugging-port=0', '--remote-debugging-address=127.0.0.1'] : []),
    `--user-data-dir=${profile}`, `--window-size=${isHeadless ? `${L.width},${L.height}` : '1360,900'}`,
    '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--disable-sync', '--disable-background-networking', '--disable-component-update',
    '--disable-default-apps', '--disable-dev-shm-usage', '--disable-client-side-phishing-detection', '--metrics-recording-only', '--no-pings', '--mute-audio', ...(isHeadless ? ['--hide-scrollbars'] : []),
    ...(process.platform === 'win32' ? ['--disable-gpu'] : []),
    '--password-store=basic', '--use-mock-keychain', '--disable-features=Translate,MediaRouter,OptimizationHints,AutofillServerCommunication', ...args, 'about:blank',
  ], { env: childEnv, stdio: usePipe ? ['ignore', 'ignore', 'ignore', 'pipe', 'pipe'] : ['ignore', 'ignore', 'pipe'], windowsHide: isHeadless });
  let exited = false, exitCode = null, errLog = '';
  if (!usePipe && child.stderr) {
    child.stderr.setEncoding('utf8');
    child.stderr.on('data', (d) => { errLog = (errLog + d).slice(-4000); });
  }
  child.on('exit', (code) => { exited = true; exitCode = code; });
  child.on('error', (e) => { exited = true; errLog += ` ${e && e.message}`; });
  const killTree = () => {
    if (process.platform === 'win32' && child.pid) {
      try { spawnSync('taskkill', ['/pid', String(child.pid), '/T', '/F'], { stdio: 'ignore', windowsHide: true }); } catch { /* 이미 끝남 */ }
    }
    try { child.kill('SIGKILL'); } catch { /* 이미 끝남 */ }
  };
  const onExit = () => killTree();
  process.on('exit', onExit);
  let cdp = null;

  async function close() {
    process.removeListener('exit', onExit);
    if (!exited) {
      if (cdp) try { await withTimeout(cdp.send('Browser.close'), 2000, '끄기'); } catch { /* 아래에서 끈다 */ }
      for (let i = 0; i < 20 && !exited; i += 1) await sleep(100);
      if (!exited) { killTree(); for (let i = 0; i < 20 && !exited; i += 1) await sleep(100); }
    }
    if (cdp) cdp.close();
    try { child.stderr?.destroy(); } catch { /* 이미 닫힘 */ }
    if (usePipe) try { child.stdio[3]?.destroy(); child.stdio[4]?.destroy(); } catch { /* 이미 닫힘 */ }
    try { fs.rmSync(profile, { recursive: true, force: true, maxRetries: 8, retryDelay: 150 }); } catch { /* 임시 폴더는 운영체제가 지운다 */ }
    return { exited, profileRemoved: !fs.existsSync(profile) };
  }

  try {
    if (usePipe) {
      cdp = cdpPipe(child);
    } else {
      const portFile = path.join(profile, 'DevToolsActivePort');
      let port = 0, wsPath = '';
      const deadline = Date.now() + L.startMs;
      while (Date.now() < deadline) {
        const m = /DevTools listening on ws:\/\/(?:127\.0\.0\.1|localhost):(\d+)(\/devtools\/\S+)/i.exec(errLog);
        if (m) { port = Number(m[1]); wsPath = m[2]; break; }
        if (fs.existsSync(portFile)) {
          try {
            const lines = fs.readFileSync(portFile, 'utf8').split(/\r?\n/).map((s) => s.trim()).filter(Boolean);
            if (lines.length >= 2 && Number(lines[0]) > 0) { port = Number(lines[0]); wsPath = lines[1]; break; }
          } catch { /* Windows 에서 Chrome 이 DevToolsActivePort 를 막 쓰는 중일 수 있다 */ }
        }
        if (exited) break;
        await sleep(50);
      }
      if (!(port > 0) || !wsPath) throw new Error(`브라우저 디버깅 포트를 찾지 못했어요 (code=${exitCode}): ${errLog.trim()}`);
      let lastErr = null;
      while (Date.now() < deadline && !exited) {
        try { cdp = await connectCdpWs(port, wsPath, Math.max(1000, deadline - Date.now())); break; }
        catch (e) { lastErr = e; await sleep(80); }
      }
      if (!cdp) throw lastErr || new Error('브라우저 WebSocket 연결 실패');
    }
  } catch (e) { await close(); throw e; }

  return { cdp, child, profile, close, browser, limits: L, headless: isHeadless };
}

// 브라우저를 띄운다. open(url, { allow }) 로 한 장을 열어 읽고, 끝나면 close() 를 꼭 부른다.
// debugPort 를 켜면 내 컴퓨터 안(127.0.0.1)에서만 닿는 디버깅 주소도 함께 연다 (REA 가 붙어서 읽을 때 쓴다).
export async function openRenderer({ browser = findBrowser(), version = '0', repo = '', limits = {}, debugPort = false, headless } = {}) {
  if (!browser) throw new Error('브라우저를 찾지 못했어요');
  let started = null;
  for (let attempt = 0; attempt < 2; attempt += 1) {
    let launched = null;
    try {
      launched = await launchBrowser({ browser, limits, debugPort, headless });
      const { cdp, profile, limits: L } = launched;
      const v = await withTimeout(cdp.send('Browser.getVersion'), L.startMs, '브라우저 시작');
      // 누가 읽는지 숨기지 않는다: 헤드리스 브라우저라는 것과 이 도구의 이름을 함께 밝힌다.
      const ua = `${v.userAgent} rebiz/${version}${repo ? ` (+${repo})` : ''}`;
      try { await cdp.send('Browser.setDownloadBehavior', { behavior: 'deny' }); } catch { /* 옛 브라우저 */ }
      let endpoint = '';
      if (debugPort) {
        const file = path.join(profile, 'DevToolsActivePort');
        for (let i = 0; i < 40; i += 1) {
          let port = 0;
          try { if (fs.existsSync(file)) port = Number(fs.readFileSync(file, 'utf8').split(/\r?\n/)[0]); } catch { /* 쓰기 잠금 중 */ }
          if (port > 0) { endpoint = `http://127.0.0.1:${port}`; break; }
          await sleep(100);
        }
      }
      started = { ...launched, ua, endpoint };
      break;
    } catch (e) {
      if (launched) await launched.close();
      if (attempt === 1) throw e;
      await sleep(200);
    }
  }
  const { cdp, child, profile, close, limits: L, ua, endpoint, headless: isHeadless } = started;

  // 한 장을 연다. 돌려주는 것으로 읽고(read), 펼치고(flow), 닫는다(close).
  async function open(url, { allow = async () => ({ ok: true }), keepScripts = false } = {}) {
    const stats = { allowed: 0, blocked: 0, why: {}, status: 0, mainBlocked: '', cookiesDropped: 0 };
    const hosts = new Map(); // 호스트 이름 -> { count, types, sent } (본문과 쿠키는 남기지 않는다)
    const scripts = new Map(); // 같은 사이트 스크립트의 요청 번호 -> 주소
    const note = (why) => { stats.blocked += 1; stats.why[why] = (stats.why[why] || 0) + 1; };
    const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
    const { sessionId } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });
    const S = (method, params) => cdp.send(method, params, sessionId);
    const inflight = new Set();
    let loaded = false, mainSeen = !/^https?:/i.test(url), pausing = 0, lastActivity = Date.now(), mainFrame = '', first = true, locked = false;
    const off = cdp.on((m) => {
      if (m.sessionId !== sessionId) return;
      const p = m.params || {};
      if (m.method === 'Network.responseReceivedExtraInfo') {
        // 응답이 쿠키를 심으면 바로 지운다.
        if (Object.keys(p.headers || {}).some((k) => /^set-cookie$/i.test(k))) { stats.cookiesDropped += 1; S('Network.clearBrowserCookies').catch(() => {}); }
      } else if (m.method === 'Fetch.requestPaused') {
        lastActivity = Date.now();
        pausing += 1;
        (async () => {
          try {
            const req = p.request || {};
            const isMain = p.resourceType === 'Document' && p.frameId === mainFrame;
            if (isMain && /^https?:/i.test(req.url)) mainSeen = true;
            let verdict, host = '';
            try { host = new URL(req.url).hostname; } catch { /* 주소가 아님 */ }
            if (!/^https?:/i.test(req.url)) verdict = { ok: true };
            else if (stats.allowed >= L.maxRequests) verdict = { ok: false, why: '요청 한도' };
            else if (isMain && locked) verdict = { ok: false, why: '펼친 뒤 다른 페이지로 넘어가기' };
            else if (req.method !== 'GET') verdict = { ok: false, why: 'GET 이 아닌 요청' };
            else if (p.resourceType === 'Document' && !isMain) verdict = { ok: false, why: '끼워 넣은 다른 페이지' };
            else if (['Ping', 'CSPViolationReport', 'Media', 'EventSource', 'WebSocket'].includes(p.resourceType)) verdict = { ok: false, why: p.resourceType === 'Media' ? '영상 파일' : '알림 신호' };
            else {
              try { verdict = await allow(req.url, { isMain, first: isMain && first, type: p.resourceType }); } catch { verdict = { ok: false, why: '확인 실패' }; }
            }
            if (isMain) first = false;
            if (host) {
              const h = hosts.get(host) || { count: 0, types: new Set(), sent: 0 };
              h.count += 1; h.types.add(p.resourceType); if (verdict.ok) h.sent += 1;
              hosts.set(host, h);
            }
            try {
              if (verdict.ok) {
                stats.allowed += 1;
                if (p.networkId) inflight.add(p.networkId);
                if (keepScripts && p.resourceType === 'Script' && p.networkId && verdict.sameSite) scripts.set(p.networkId, req.url);
                // 받은 쿠키를 돌려보내지 않도록, 요청을 내보내기 직전에 쿠키를 비운다.
                try { await S('Network.clearBrowserCookies'); } catch { /* 그대로 보낸다 */ }
                await S('Fetch.continueRequest', { requestId: p.requestId });
              } else {
                note(verdict.why || '막음');
                if (isMain && !locked) stats.mainBlocked = verdict.why || '막음';
                await S('Fetch.failRequest', { requestId: p.requestId, errorReason: 'BlockedByClient' });
              }
            } catch { /* 탭이 이미 닫힘 */ }
          } finally { pausing -= 1; lastActivity = Date.now(); }
        })();
      } else if (m.method === 'Network.loadingFinished' || m.method === 'Network.loadingFailed') { inflight.delete(p.requestId); lastActivity = Date.now(); } else if (m.method === 'Network.responseReceived') {
        if (p.type === 'Document' && p.frameId === mainFrame && p.response && !locked) { mainSeen = true; stats.status = p.response.status; }
      } else if (m.method === 'Page.loadEventFired') { if (mainSeen) { loaded = true; lastActivity = Date.now(); } } else if (m.method === 'Page.javascriptDialogOpening') { S('Page.handleJavaScriptDialog', { accept: false }).catch(() => {}); }
    });
    const idle = async (maxMs) => {
      const until = Date.now() + maxMs;
      while (Date.now() < until) { if (pausing === 0 && inflight.size === 0 && Date.now() - lastActivity >= L.idleMs) return true; await sleep(100); }
      return false;
    };
    const evaluate = async (expression, ms = 8000) => {
      const r = await withTimeout(S('Runtime.evaluate', { expression, returnByValue: true, userGesture: true }), ms, '화면 읽기');
      return r.result ? r.result.value : undefined;
    };
    let closed = false;
    const closePage = async () => {
      if (closed) return;
      closed = true;
      off();
      try { await withTimeout(cdp.send('Target.closeTarget', { targetId }), 2000, '탭 닫기'); } catch { /* 브라우저를 끌 때 같이 닫힌다 */ }
    };
    const started = Date.now();
    let timedOut = false;
    try {
      await S('Page.enable');
      await S('Network.enable');
      await S('Emulation.setUserAgentOverride', { userAgent: ua });
      if (isHeadless) await S('Emulation.setDeviceMetricsOverride', { width: L.width, height: L.height, deviceScaleFactor: 1, mobile: false });
      else try { await S('Page.bringToFront'); } catch { /* 창 포커스 실패는 무시 */ }
      mainFrame = (await S('Page.getFrameTree')).frameTree.frame.id;
      try { await S('Emulation.setDocumentCookieDisabled', { disabled: true }); } catch { /* 옛 브라우저 */ }
      await S('Fetch.enable', { patterns: [{ urlPattern: '*' }] });
      loaded = false;
      lastActivity = Date.now();
      S('Page.navigate', { url }).catch(() => {});
      while (!loaded && Date.now() - started < L.navMs && !stats.mainBlocked) await sleep(100);
      timedOut = !loaded && !stats.mainBlocked;
      if (!stats.mainBlocked || !first) await idle(L.settleMs);
      if (isHeadless) {
        // 아래쪽이 화면에 들어와야 그려지는 구역이 있으므로, 누르거나 굴리지 않고 창만 길게 늘인다.
        try {
          const h = (await evaluate('Math.max(document.documentElement ? document.documentElement.scrollHeight : 0, document.body ? document.body.scrollHeight : 0)')) || 0;
          if (h > L.height) { await S('Emulation.setDeviceMetricsOverride', { width: L.width, height: Math.min(h, L.maxHeight), deviceScaleFactor: 1, mobile: false }); lastActivity = Date.now(); await idle(L.growMs); }
        } catch { /* 길이를 못 재면 그대로 읽는다 */ }
      } else if (!stats.mainBlocked) {
        try {
          await evaluate(VISUAL_HUD('reversebusiness · Live Dissection', `Scanning ${new URL(url).hostname}…`), 2500);
          await evaluate(VISUAL_SCAN, 2500);
          await sleep(950);
        } catch { /* 오버레이 표시 실패는 읽기에 영향 없음 */ }
      }
    } catch (e) { await closePage(); throw e; }

    const showHud = async (title, sub = '') => {
      if (isHeadless) return;
      try { await evaluate(VISUAL_HUD(title, sub), 2000); } catch { /* 무시 */ }
    };

    return {
      targetId, stats, userAgent: ua,
      get status() { return stats.status; },
      get timedOut() { return timedOut; },
      get ms() { return Date.now() - started; },
      hud: showHud,
      // 그려진 화면의 글자, 구조, 구역의 위치와 크기
      async read() {
        if (!isHeadless) try { await evaluate(VISUAL_CLEANUP, 2000); } catch { /* 무시 */ }
        let page = { html: '', blocks: [], docH: 0, docW: L.width, url };
        try { const v = await evaluate(EXTRACT); if (v) page = v; } catch { /* 읽지 못하면 빈 결과 */ }
        return page;
      },
      // 흐름 읽기: 펼치기만 한다. 누른 종류와 횟수만 돌려준다.
      async flow({ max = L.flowClicks } = {}) {
        const out = { clicks: 0, kinds: {}, moved: false };
        locked = true; // 여기서부터 다른 페이지로 넘어가는 요청은 막는다
        let kinds = [];
        let before = '';
        try { before = await evaluate('location.pathname'); kinds = (await evaluate(PICK(Math.max(0, Math.min(max, 12))))) || []; } catch { return out; }
        if (!isHeadless && kinds.length) await showHud('reversebusiness · Flow Probe', `Checking ${kinds.length} expandable element(s)…`);
        for (let i = 0; i < kinds.length; i += 1) {
          try {
            if (!isHeadless) {
              await showHud('reversebusiness · Flow Probe', `Expanding ${kinds[i]} (${i + 1}/${kinds.length})…`);
              await evaluate(VISUAL_MARK_CLICK(i), 2000);
              await sleep(240);
            }
            if (!(await evaluate(CLICK(i), 3000))) continue;
            out.clicks += 1; out.kinds[kinds[i]] = (out.kinds[kinds[i]] || 0) + 1;
            lastActivity = Date.now();
            await idle(L.clickSettleMs);
            if ((await evaluate('location.pathname')) !== before) { out.moved = true; break; }
          } catch { break; }
        }
        if (!isHeadless) try { await evaluate(VISUAL_CLEANUP, 2000); } catch { /* 무시 */ }
        return out;
      },
      // 요청이 나가려던 호스트 이름과 종류. 본문, 쿠키, 주소의 뒷부분은 담지 않는다.
      hosts() { return [...hosts.entries()].map(([host, h]) => ({ host, count: h.count, sent: h.sent, types: [...h.types].sort() })).sort((a, b) => b.count - a.count); },
      // 속 읽기에 쓰는 같은 사이트 스크립트의 글. 메모리에서만 훑고 저장하지 않는다.
      async scripts() {
        const out = [];
        let total = 0;
        for (const [requestId, src] of scripts) {
          if (total > L.scriptBytes) break;
          try {
            const r = await withTimeout(S('Network.getResponseBody', { requestId }), 5000, '스크립트 읽기');
            const text = r.base64Encoded ? Buffer.from(r.body, 'base64').toString('utf8') : r.body;
            total += text.length;
            out.push({ url: src, text });
          } catch { /* 이미 비워진 것은 건너뛴다 */ }
        }
        return out;
      },
      close: closePage,
    };
  }

  // 한 장을 열어 읽고 닫는다.
  async function render(url, opts = {}) {
    const pg = await open(url, opts);
    try {
      const page = await pg.read();
      return { ...page, status: pg.status, stats: pg.stats, timedOut: pg.timedOut, userAgent: ua, ms: pg.ms, hosts: pg.hosts() };
    } finally { await pg.close(); }
  }

  return { open, render, close, browser, userAgent: ua, profile, pid: child.pid, endpoint, headless: isHeadless };
}
