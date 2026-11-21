/* ============================================================
   통합 SNS 수집기 v1  (쓰레드 수집기 v5 = 수집기.js 를 여러 사이트용으로 넓힌 것)
   지금 보고 있는 화면의 글을 자동 스크롤하며 담는다.
   ------------------------------------------------------------
   지원: 쓰레드 · X(트위터) · 인스타그램 · 페이스북 · 그 밖의 사이트(article 기준)
   유튜브·블로그·카톡은 이 북마클릿이 아니라 통합정리.py 가 직접 가져온다.

   하는 일 / 안 하는 일
     · 내 브라우저에 이미 보이는 글자를 옮겨 적는 것뿐이다.
     · 로그인 대행, 차단 우회, 서버 요청을 하지 않는다 (fetch 없음).

   [수집기.js 의 설계 규칙 6개를 그대로 지킨다 — 건드리지 말 것]
     1. MutationObserver 금지  2. 패널은 documentElement 에  3. textContent 만 교체
     4. 백업은 스로틀  5. 나머지 연산자와 퍼센트 글자 금지(북마클릿 URL 이 깨진다)
     6. render() 에서 패널 크기를 바꾸지 않는다

   쓰는 법: 프로필(또는 모으고 싶은 화면)을 열고 북마클릿 클릭 → [▶ 시작]
           → 다 되면 [저장] → 클로드에게 "통합 정리해"
   ============================================================ */

(() => {
  if (window.__snsCollector) {
    console.log('이미 실행 중입니다. 우측 상단 상자를 확인하세요.');
    return;
  }

  // ---- 숫자만 바꾸면 되는 설정 ----
  const SPEEDS = [
    { label: '보통', ms: 1200, amount: 0.8 },
    { label: '천천히', ms: 2000, amount: 0.6 }, // 글을 놓치는 것 같으면 이쪽
  ];
  const STAGNANT_LIMIT = 6;             // 이만큼 연속 안 늘면 자동 정지
  const MAX_ACTIVE_MS = 15 * 60 * 1000; // 실제로 돌아간 시간 기준 15분이면 정지
  const HARVEST_MS = 1500;
  const BACKUP_EVERY = 25;
  const BACKUP_MS = 20000;

  // ---------- 사이트별 읽는 법 ----------

  const host = window.__snsHost || location.hostname;   // __snsHost·__snsPath 는 점검용
  const path = window.__snsPath || location.pathname;
  const seg1 = path.split('/')[1] || '';
  const NOT_USER = ['', 'home', 'explore', 'search', 'i', 'notifications', 'messages',
    'settings', 'compose', 'p', 'reel', 'reels', 'stories', 'direct', 'accounts', 'saved', 'liked'];
  const profile = NOT_USER.includes(seg1) ? null : seg1;

  const txt = (e) => ((e && e.innerText) || '').trim();
  const href = (a) => a.getAttribute('href') || '';
  const iso = (box) => {
    const t = box.querySelector('time');
    return (t && t.getAttribute('datetime')) || '';
  };
  const hash = (s) => {
    let h = 0;
    for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
    return 'h' + (h >>> 0).toString(36);
  };
  const nested = (box, sel) => box.parentElement && box.parentElement.closest(sel);

  // 링크에서 위로 올라가며 '날짜가 있는 글 상자'를 찾는다 (수집기.js 와 같은 방식)
  function findContainer(linkEl) {
    let el = linkEl;
    let best = null;
    for (let i = 0; i < 12 && el; i++) {
      el = el.parentElement;
      if (!el) break;
      const t = txt(el);
      if (t.length > 20 && el.querySelector('time')) {
        best = el;
        if (t.length > 60) break;
      }
    }
    return best;
  }

  // sel 로 찾은 요소마다 read() 가 글 하나(또는 null)를 돌려준다.
  // user 가 있으면 그 계정 글만 담는다.
  const SITES = {
    threads: {
      host: /threads\.(com|net)$/,
      user: (path.match(/^\/@([^/]+)/) || [])[1] || null,
      sel: 'a[href*="/post/"]',
      read(a) {
        const m = href(a).match(/\/@([^/]+)\/post\/([A-Za-z0-9_-]+)/);
        const box = m && findContainer(a);
        return box && { id: m[2], username: m[1], created_at: iso(box), raw_text: txt(box),
          url: `https://www.threads.com/@${m[1]}/post/${m[2]}` };
      },
    },
    x: {
      host: /(^|\.)(x|twitter)\.com$/,
      user: profile,
      sel: 'article a[href*="/status/"]',
      read(a) {
        if (!a.querySelector('time')) return null; // 날짜 링크 = 그 글의 고유주소
        const m = href(a).match(/^\/([^/]+)\/status\/(\d+)/);
        const box = m && a.closest('article');
        return box && { id: m[2], username: m[1], created_at: iso(a),
          raw_text: txt(box.querySelector('[data-testid="tweetText"]')) || txt(box),
          url: `https://x.com/${m[1]}/status/${m[2]}` };
      },
    },
    instagram: {
      host: /instagram\.com$/,
      user: null,
      min: 0,
      sel: 'a[href*="/p/"], a[href*="/reel/"]',
      // ponytail: 프로필 격자에는 본문이 없어 사진 설명(alt)만 담긴다.
      //           전문이 필요하면 글을 하나씩 연 화면(article)에서 실행.
      read(a) {
        const m = href(a).match(/\/(p|reel)\/([A-Za-z0-9_-]+)/);
        if (!m) return null;
        const art = a.closest('article');
        const img = (art || a).querySelector('img[alt]');
        return { id: m[2], username: profile || '', created_at: iso(art || a),
          raw_text: txt(art) || (img ? img.alt : ''),
          url: `https://www.instagram.com/${m[1]}/${m[2]}/` };
      },
    },
    facebook: {
      host: /facebook\.com$/,
      user: null, // 표시 이름과 주소 이름이 달라 계정으로 거를 수 없다 → 화면에 뜬 글 전부
      sel: 'div[role="article"]',
      // ponytail: 날짜는 화면에서 읽을 수 없어 비워 둔다(페이스북이 숨김).
      //           정확한 날짜가 필요하면 기존 최주훈_페이스북/수집.py 결과를 --import.
      // '공유하기'로 올린 글(남의 글을 내 타임라인에 공유한 것)은 facebook_shared 로 따로 담는다:
      // 글쓴이 = 원래 글쓴이, 본문 = 내가 덧붙인 말 + 원래 글, 주소 = 원래 글.
      // ponytail: 공유 여부는 '글 상자 안에 글쓴이 이름이 둘' 또는 머리말의 '공유' 낱말로 짐작한다.
      //           가짜 화면(수집기_점검.html)으로만 점검했다. 실제 화면에서 공유글이 0개로 나오거나
      //           그룹 글이 공유글로 잡히면 그 화면의 구조를 보고 여기를 고칠 것.
      read(box) {
        if (nested(box, '[role="article"]')) return null; // 댓글
        box.querySelectorAll('div[role="button"]').forEach((b) => {
          const t = b.textContent.trim();
          if (t === '더 보기' || t === 'See more') b.click(); // 긴 글 펼치기
        });
        const own = (sel) => [...box.querySelectorAll(sel)].filter((e) => e.closest('[role="article"]') === box); // 댓글 속은 뺀다
        const heads = own('h2, h3, h4').map(txt).filter(Boolean);
        const msgs = own('[data-ad-preview="message"], [data-ad-comet-preview="message"]').map(txt).filter(Boolean);
        const links = own('a[href]').map((a) => a.href)
          .filter((h) => /\/posts\/|story_fbid=|\/permalink|\/videos\/|\/reel\//.test(h))
          .map((h) => h.split('__cft__')[0].replace(/[?&]$/, ''));
        const who = heads[0] || '';
        const from = heads.find((h) => h !== who); // 공유한 글 속의 원래 글쓴이
        const shared = !!from || /공유했|shared/i.test(who);
        const raw = !shared ? msgs[0] || txt(box)
          : msgs.length > 1 ? msgs[0] + '\n\n— 공유한 글 —\n' + msgs.slice(1).join('\n') : txt(box);
        const name = from || who;
        const it = { id: hash(name + raw.slice(0, 80)), username: name, created_at: '', raw_text: raw,
          url: (shared && links.find((h) => h !== links[0])) || links[0] || '' };
        if (shared) it.platform = 'facebook_shared';
        return it;
      },
    },
    etc: {
      host: /./,
      user: null,
      sel: 'article, [role="article"]',
      read(box) {
        if (nested(box, 'article, [role="article"]')) return null;
        const t = box.querySelector('time');
        const a = (t && t.closest('a[href]')) || box.querySelector('h1 a, h2 a, h3 a');
        const raw = txt(box);
        return { id: a ? a.href : hash(raw.slice(0, 80)), username: '', created_at: iso(box),
          raw_text: raw, url: a ? a.href : '' };
      },
    },
  };

  const siteKey = Object.keys(SITES).find((k) => SITES[k].host.test(host));
  const site = SITES[siteKey];
  // 쓰레드 '저장됨' 화면(threads.com/saved)은 남의 글 모음이라 내 글과 섞이지 않게 이름을 따로 붙인다.
  const platform = siteKey === 'etc' ? host : (siteKey === 'threads' && seg1 === 'saved') ? 'threads_saved' : siteKey;
  const pageUser = site.user;
  const minLen = site.min == null ? 15 : site.min;
  const BACKUP_KEY = '__snsCollector:' + platform + ':' + (pageUser || profile || 'all');

  const store = new Map();
  const filteredIds = new Set();

  let started = false;
  let running = false;
  let stagnantTicks = 0;
  let lastTotal = 0;
  let autoStopped = false;
  let activeMs = 0;
  let speedIdx = 0;
  let collapsed = false;
  let textTotal = 0;     // 글이 펼쳐져 길어진 것도 '진행'으로 친다
  let oldestDate = '';
  let lastPreview = '';
  let restoredCount = 0;
  let backupState = '';
  let backupFailed = false;
  let lastBackupSize = -1;
  let lastBackupAt = 0;

  function noteDate(d) {
    if (!d) return;
    d = d.slice(0, 10);
    if (!oldestDate || d < oldestDate) oldestDate = d;
  }

  function harvest() {
    document.querySelectorAll(site.sel).forEach((node) => {
      const it = site.read(node);
      if (!it || !it.id) return;
      if (pageUser && it.username !== pageUser) {
        filteredIds.add(it.id);
        return;
      }
      if (it.raw_text.length < minLen) return;
      const old = store.get(it.id);
      // 같은 글이면 더 길어졌거나(펼침) 주소가 새로 잡혔을 때만 갈아끼운다
      if (old && it.raw_text.length <= old.raw_text.length && !(it.url && !old.url)) return;
      it.platform = it.platform || platform; // 페이스북 공유글은 read() 가 이름을 따로 붙여 온다
      it.url = it.url || (old && old.url) || '';
      textTotal += it.raw_text.length - (old ? old.raw_text.length : 0);
      store.set(it.id, it);
      noteDate(it.created_at);
      const line = it.raw_text.split('\n').find((l) => l.trim().length > 3) || '';
      lastPreview = line.length > 60 ? line.slice(0, 60) + '…' : line;
    });
  }

  // ---------- 백업 (브라우저 저장소) ----------

  function backup(force) {
    if (!force) {
      const grew = store.size - lastBackupSize >= BACKUP_EVERY;
      const stale = Date.now() - lastBackupAt >= BACKUP_MS && store.size !== lastBackupSize;
      if (!grew && !stale) return;
    }
    if (store.size === 0) return;
    try {
      localStorage.setItem(BACKUP_KEY, JSON.stringify([...store.values()]));
      lastBackupSize = store.size;
      lastBackupAt = Date.now();
      backupFailed = false;
      backupState = '백업됨 ✓ ' + new Date().toLocaleTimeString('ko-KR', { hour12: false });
    } catch (e) {
      backupFailed = true; // 조용히 실패하면 안 된다
      backupState = '⚠ 백업 실패 — 수동 저장 필요';
      console.warn('백업 실패:', e);
    }
  }

  try {
    const arr = JSON.parse(localStorage.getItem(BACKUP_KEY) || 'null');
    if (Array.isArray(arr)) {
      arr.forEach((p) => {
        if (p && p.id) store.set(p.id, p);
      });
      restoredCount = store.size;
      lastBackupSize = store.size;
      lastBackupAt = Date.now();
      store.forEach((p) => {
        noteDate(p.created_at);
        textTotal += (p.raw_text || '').length;
      });
    }
  } catch (e) {
    console.warn('백업 복구 실패:', e);
  }

  // ---------- 화면 (한 번만 조립, 이후엔 글자만 교체) ----------

  const LINE = 'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;';

  function el(tag, css, text) {
    const e = document.createElement(tag);
    if (css) e.style.cssText = css;
    if (text != null) e.textContent = text;
    return e;
  }

  const panel = el('div', [
    'box-sizing:border-box', 'width:272px',
    'position:fixed', 'top:16px', 'right:16px', 'z-index:2147483647',
    'background:#1f4e79', 'color:#fff', 'padding:12px 14px',
    'border-radius:10px', 'font:13px/1.55 -apple-system,sans-serif',
    'font-variant-numeric:tabular-nums', 'box-shadow:0 4px 18px rgba(0,0,0,.35)',
  ].join(';'));
  document.documentElement.appendChild(panel);

  const head = el('div', 'display:flex;align-items:center;justify-content:space-between;gap:10px');
  head.appendChild(el('div', 'font-weight:700;' + LINE, 'KBG-통합자료수집기 · ' + platform));
  const foldBtn = el('button',
    'background:transparent;color:#fff;border:0;cursor:pointer;font:700 13px sans-serif;padding:0 3px;opacity:.8',
    '▾');
  head.appendChild(foldBtn);
  panel.appendChild(head);

  const countLine = el('div', 'font-size:22px;font-weight:800;margin-top:2px;' + LINE);
  const countNum = el('span', '', '0');
  countLine.appendChild(countNum);
  countLine.appendChild(el('span', 'font-size:12px;font-weight:400', ' 개'));
  panel.appendChild(countLine);

  const body = el('div', '');
  panel.appendChild(body);

  const rule = () => el('div', 'height:1px;background:rgba(255,255,255,.22);margin:8px 0');
  const statCss = 'font-size:11.5px;opacity:.92;' + LINE;
  const statusEl = el('div', 'opacity:.9;margin:2px 0 1px;' + LINE);
  const scopeEl = el('div', 'opacity:.7;font-size:11px;' + LINE,
    pageUser ? '@' + pageUser + ' 글만 수집' : '화면에 보이는 글 전부 수집');
  const dateEl = el('div', 'font-size:12.5px;font-weight:700;' + LINE);
  const timeEl = el('div', statCss);
  const filteredEl = el('div', statCss);
  const backupEl = el('div', statCss);
  const restoredEl = el('div', 'font-size:11.5px;color:#cfe6ff;font-weight:600;' + LINE);
  const previewEl = el('div', 'font-size:11px;opacity:.72;margin-top:5px;' + LINE);
  if (!restoredCount) restoredEl.style.display = 'none';
  else restoredEl.textContent = `이전 수집분 ${restoredCount}개 복구됨`;

  [statusEl, scopeEl, rule(), dateEl, timeEl, filteredEl, backupEl, restoredEl, previewEl, rule()]
    .forEach((e) => body.appendChild(e));

  function mkBtn(label, bg, width) {
    return el('button', [
      'box-sizing:border-box', 'width:' + width + 'px', 'text-align:center',
      'background:' + bg, 'color:#fff', 'border:0', 'border-radius:6px',
      'padding:6px 0', 'margin:0 6px 5px 0', 'cursor:pointer',
      'font:600 12px -apple-system,sans-serif',
    ].join(';'), label);
  }

  const saveBtn = mkBtn('저장', '#1c1c1e', 64);
  const toggleBtn = mkBtn('▶ 시작', '#2f5d62', 78);
  const stopBtn = mkBtn('종료', '#8a1c1c', 56);
  const speedBtn = mkBtn('속도: 보통', '#16395a', 92);
  const clearBtn = mkBtn('백업 비우기', '#16395a', 92);
  const row1 = el('div', 'margin-top:2px');
  const row2 = el('div', '');
  [saveBtn, toggleBtn, stopBtn].forEach((b) => row1.appendChild(b));
  [speedBtn, clearBtn].forEach((b) => row2.appendChild(b));
  body.appendChild(row1);
  body.appendChild(row2);

  function fmtMs(ms) {
    const s = Math.floor(ms / 1000);
    const m = Math.floor(s / 60);
    return m > 0 ? `${m}분 ${s - m * 60}초` : `${s}초`;
  }

  function render() {
    countNum.textContent = String(store.size);
    statusEl.textContent = !started ? '대기 중 — [시작]을 누르세요'
      : running ? '자동 스크롤 중…'
      : autoStopped ? '새 글이 더 안 보입니다' : '일시정지됨';
    toggleBtn.textContent = !started ? '▶ 시작' : running ? '일시정지' : '계속';
    dateEl.textContent = oldestDate ? `지금 ▸ ${oldestDate} 지점` : '지금 ▸ —';
    const gained = store.size - restoredCount;
    const perMin = activeMs > 0 ? Math.round(gained / (activeMs / 60000)) : 0;
    timeEl.textContent = `${fmtMs(activeMs)} · 분당 ${perMin}개`;
    filteredEl.textContent = siteKey === 'facebook'
      ? `그중 공유한 글 ${[...store.values()].filter((p) => p.platform === 'facebook_shared').length}개`
      : `남의 글 ${filteredIds.size}개 걸러냄`;
    backupEl.textContent = backupState || '백업 대기 중';
    backupEl.style.color = backupFailed ? '#ffd4d4' : '';
    backupEl.style.fontWeight = backupFailed ? '700' : '';
    previewEl.textContent = lastPreview ? `방금: ${lastPreview}` : '방금: —';
    speedBtn.textContent = `속도: ${SPEEDS[speedIdx].label}`;
  }

  // ---------- 버튼 ----------

  foldBtn.onclick = () => {
    collapsed = !collapsed;
    body.style.display = collapsed ? 'none' : '';
    foldBtn.textContent = collapsed ? '▸' : '▾';
  };

  saveBtn.onclick = () => {
    const data = [...store.values()].sort((a, b) =>
      (a.created_at || '').localeCompare(b.created_at || ''));
    const who = (pageUser || profile || 'all').replace(/[^\w.-]/g, '_');
    const a = document.createElement('a');
    a.href = URL.createObjectURL(
      new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' }));
    a.download = `sns_${platform}_${who}_${data.length}posts.json`;
    a.click();
    backup(true);
    saveBtn.textContent = '저장 ✓';
    setTimeout(() => {
      saveBtn.textContent = '저장';
    }, 1500);
  };

  toggleBtn.onclick = () => {
    if (!started) {
      started = true;
      running = true;
      harvest();
    } else {
      running = !running;
      if (!running) backup(true);
    }
    stagnantTicks = 0;
    autoStopped = false;
    render();
  };

  speedBtn.onclick = () => {
    speedIdx = speedIdx + 1 >= SPEEDS.length ? 0 : speedIdx + 1;
    clearInterval(scrollTimer);
    scrollTimer = setInterval(scrollTick, SPEEDS[speedIdx].ms);
    render();
  };

  clearBtn.onclick = () => {
    if (!confirm('브라우저에 저장된 백업과 지금까지 모은 목록을 모두 지웁니다.\n되돌릴 수 없습니다. 저장(다운로드)한 파일은 그대로 남습니다.\n\n지울까요?')) return;
    try {
      localStorage.removeItem(BACKUP_KEY);
    } catch (e) {
      console.warn(e);
    }
    store.clear();
    filteredIds.clear();
    restoredCount = 0;
    restoredEl.style.display = 'none';
    lastBackupSize = -1;
    textTotal = 0;
    oldestDate = '';
    lastPreview = '';
    backupState = '백업 비웠음';
    backupFailed = false;
    render();
  };

  stopBtn.onclick = () => {
    backup(true);
    clearInterval(scrollTimer);
    clearInterval(harvestTimer);
    panel.remove();
    delete window.__snsCollector;
    console.log('수집기를 종료했습니다. (백업은 남아 있습니다)');
  };

  // ---------- 타이머 ----------

  function stopAuto(msg) {
    running = false;
    autoStopped = true;
    backup(true);
    render();
    if (msg) console.log(msg);
  }

  function scrollTick() {
    if (!running) return;
    activeMs += SPEEDS[speedIdx].ms;
    if (activeMs >= MAX_ACTIVE_MS) {
      stopAuto('안전장치: 작동 시간 15분이 지나 자동으로 멈췄습니다.');
      return;
    }
    harvest();
    if (textTotal === lastTotal) {
      stagnantTicks++;
      if (stagnantTicks >= STAGNANT_LIMIT) {
        stopAuto(null);
        return;
      }
    } else {
      stagnantTicks = 0;
    }
    lastTotal = textTotal;
    backup(false);
    render();
    window.scrollBy(0, window.innerHeight * SPEEDS[speedIdx].amount);
  }

  // 정해진 간격에만 확인한다 (감시자 없음). [시작] 전에는 아무것도 하지 않는다.
  const harvestTimer = setInterval(() => {
    if (!started) return;
    harvest();
    render();
  }, HARVEST_MS);
  let scrollTimer = setInterval(scrollTick, SPEEDS[speedIdx].ms);

  window.__snsCollector = { store, harvest, backup, platform };
  render();
  console.log(`KBG-통합자료수집기 준비됨 (${platform}) — [▶ 시작]을 누르면 시작합니다.`);
})();
