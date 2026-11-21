/* ============================================================
   쓰레드 글 수집기 v5
   지금 보고 있는 프로필 계정의 글을 담는다 (계정 고정 없음)
   ------------------------------------------------------------
   v5에서 바뀐 것 (2026-08-01)
     · 북마크를 눌러도 바로 출발하지 않는다. 상자만 뜨고 대기 →
       위치를 잡은 뒤 [▶ 시작]을 눌러야 수집·스크롤이 시작된다.
       (시작 전에는 아무것도 담지 않는다 — 완전 대기)
     · 상자 크기를 고정했다. 글자가 길어져도, 버튼 라벨이 바뀌어도
       상자가 커졌다 작아졌다 하지 않는다.

   v4에서 들어온 것
     · 브라우저 저장소 자동 백업 → 탭이 닫혀도 다음 실행 때 복구
     · 날짜 진행 표시 / 경과시간·속도 / 걸러낸 수 / 미리보기
     · 저장 ✓ 피드백 / 속도 조절 / 접기

   [성능·안정성 설계 — 건드리지 말 것]
     1. MutationObserver 를 절대 쓰지 않는다.
        v1에서 "패널을 다시 그리는 것"을 스스로 감지해 무한 반복 →
        브라우저 탭이 멈추는 사고가 있었다.
     2. 패널은 body 가 아니라 documentElement(html)에 붙인다.
     3. 화면 갱신은 innerHTML 통째 교체가 아니라 textContent 만 바꾼다.
     4. 백업(localStorage 쓰기)은 스로틀한다.
     5. 나머지 연산자(%)를 쓰지 않는다 — 북마클릿 URL 안에서 브라우저가
        '%60' 같은 걸 퍼센트 인코딩으로 잘못 풀어 코드를 깨뜨린다.
     6. 패널 크기를 바꾸는 값을 render() 에서 만들지 않는다.
        모든 글자 줄은 한 줄로 강제(nowrap+ellipsis)하고, 버튼은 폭을
        고정한다. 안 그러면 상자가 계속 요동친다.

   쓰는 법:
   1. 크롬에서 https://www.threads.com/@계정명 열기
   2. 북마클릿 클릭 → 우측 상단에 초록 상자가 뜬다 (아직 아무 일도 안 함)
   3. 수집을 시작하고 싶은 위치까지 화면을 맞춘다
   4. [▶ 시작] 클릭 → 자동 스크롤·수집 시작
   5. 15분(실제 작동 시간)이 지나면 안전장치로 멈춘다 → [저장] 후 [계속]
   6. 다 됐으면 [저장] → 다운로드된 JSON 은 그대로 두고
      클로드에게 "정리해" 라고만 하면 된다
   ============================================================ */

(() => {
  if (window.__threadsCollector) {
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
  const HARVEST_MS = 1500;              // 화면 훑는 주기
  const BACKUP_EVERY = 25;              // 새 글 이만큼 쌓이면 백업
  const BACKUP_MS = 20000;              // 또는 이 시간이 지나면 백업

  // 지금 보고 있는 프로필 계정명 (/@계정명 → 계정명)
  // 프로필 페이지가 아니면 null → 그때는 필터 없이 전부 담는다
  const pageUser = (location.pathname.match(/^\/@([^/]+)/) || [])[1] || null;
  const BACKUP_KEY = '__threadsCollector:' + (pageUser || 'unknown');

  const store = new Map();
  const filteredIds = new Set();

  let started = false;   // [시작]을 한 번이라도 눌렀는가 (이게 false면 아무것도 안 담는다)
  let running = false;   // 지금 자동 스크롤 중인가
  let stagnantTicks = 0;
  let lastSize = 0;
  let autoStopped = false;
  let activeMs = 0;
  let speedIdx = 0;
  let collapsed = false;

  let oldestDate = '';
  let lastPreview = '';
  let restoredCount = 0;

  let backupState = '';
  let backupFailed = false;
  let lastBackupSize = -1;
  let lastBackupAt = 0;

  // ---------- 수집 ----------

  function noteDate(iso) {
    if (!iso) return;
    const d = iso.slice(0, 10);
    if (!oldestDate || d < oldestDate) oldestDate = d;
  }

  function firstLine(raw) {
    const lines = raw.split('\n');
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line || line.length <= 3) continue;
      if (pageUser && line === pageUser) continue;
      if (/^20\d\d-\d\d-\d\d$/.test(line)) continue;
      return line.length > 60 ? line.slice(0, 60) + '…' : line;
    }
    return '';
  }

  function findContainer(linkEl) {
    let el = linkEl;
    let best = null;
    for (let i = 0; i < 12 && el; i++) {
      el = el.parentElement;
      if (!el) break;
      const t = (el.innerText || '').trim();
      if (t.length > 20 && el.querySelector('time')) {
        best = el;
        if (t.length > 60) break;
      }
    }
    return best;
  }

  function harvest() {
    document.querySelectorAll('a[href*="/post/"]').forEach((a) => {
      const href = a.getAttribute('href') || '';
      const m = href.match(/\/@([^/]+)\/post\/([A-Za-z0-9_-]+)/);
      if (!m) return;
      const [, username, id] = m;
      if (store.has(id)) return;
      // 프로필 페이지면 그 계정 글만 담는다 (사이드바 추천·알림에 뜬 남의 글 제외)
      if (pageUser && username !== pageUser) {
        filteredIds.add(id);
        return;
      }

      const box = findContainer(a);
      if (!box) return;

      const timeEl = box.querySelector('time');
      const raw = (box.innerText || '').trim();
      if (raw.length < 15) return;

      const created = timeEl ? timeEl.getAttribute('datetime') || '' : '';
      store.set(id, {
        id,
        username,
        url: `https://www.threads.com/@${username}/post/${id}`,
        created_at: created,
        raw_text: raw,
      });
      noteDate(created);
      lastPreview = firstLine(raw);
    });
  }

  // ---------- 백업 (브라우저 저장소) ----------

  function backup(force) {
    if (!force) {
      const grew = store.size - lastBackupSize >= BACKUP_EVERY;
      const stale =
        Date.now() - lastBackupAt >= BACKUP_MS && store.size !== lastBackupSize;
      if (!grew && !stale) return;
    }
    if (store.size === 0) return;
    try {
      localStorage.setItem(BACKUP_KEY, JSON.stringify([...store.values()]));
      lastBackupSize = store.size;
      lastBackupAt = Date.now();
      backupFailed = false;
      backupState =
        '백업됨 ✓ ' + new Date().toLocaleTimeString('ko-KR', { hour12: false });
    } catch (e) {
      // 용량 초과 등 — 조용히 실패하면 안 된다. 눈에 보이게 알린다.
      backupFailed = true;
      backupState = '⚠ 백업 실패 — 수동 저장 필요';
      console.warn('백업 실패:', e);
    }
  }

  // 이전 회차 백업이 있으면 복구한다
  try {
    const saved = localStorage.getItem(BACKUP_KEY);
    if (saved) {
      const arr = JSON.parse(saved);
      if (Array.isArray(arr)) {
        arr.forEach((p) => {
          if (p && p.id) store.set(p.id, p);
        });
        restoredCount = store.size;
        lastBackupSize = store.size;
        lastBackupAt = Date.now();
        store.forEach((p) => noteDate(p.created_at));
      }
    }
  } catch (e) {
    console.warn('백업 복구 실패:', e);
  }

  // ---------- 화면 (한 번만 조립, 이후엔 글자만 교체) ----------
  // 크기 고정 원칙: 모든 글자 줄은 nowrap + ellipsis 로 한 줄에 가둔다.
  // 넘치면 줄바꿈이 아니라 '…' 로 잘리므로 세로 크기가 절대 안 변한다.

  const LINE = 'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;';

  function el(tag, css, text) {
    const e = document.createElement(tag);
    if (css) e.style.cssText = css;
    if (text != null) e.textContent = text;
    return e;
  }

  const panel = el(
    'div',
    [
      'box-sizing:border-box', 'width:272px',   // 폭 고정 (내용폭 244px)
      'position:fixed', 'top:16px', 'right:16px', 'z-index:2147483647',
      'background:#0b7a3b', 'color:#fff', 'padding:12px 14px',
      'border-radius:10px', 'font:13px/1.55 -apple-system,sans-serif',
      'font-variant-numeric:tabular-nums',      // 숫자 폭을 모두 같게
      'box-shadow:0 4px 18px rgba(0,0,0,.35)',
    ].join(';')
  );
  document.documentElement.appendChild(panel);

  const head = el(
    'div',
    'display:flex;align-items:center;justify-content:space-between;gap:10px'
  );
  head.appendChild(el('div', 'font-weight:700', '쓰레드 수집기'));
  const foldBtn = el(
    'button',
    'background:transparent;color:#fff;border:0;cursor:pointer;font:700 13px sans-serif;padding:0 3px;opacity:.8',
    '▾'
  );
  head.appendChild(foldBtn);
  panel.appendChild(head);

  const countLine = el('div', 'font-size:22px;font-weight:800;margin-top:2px;' + LINE);
  const countNum = el('span', '', '0');
  countLine.appendChild(countNum);
  countLine.appendChild(el('span', 'font-size:12px;font-weight:400', ' 개'));
  panel.appendChild(countLine);

  const body = el('div', '');
  panel.appendChild(body);

  const statusEl = el('div', 'opacity:.9;margin:2px 0 1px;' + LINE);
  const scopeEl = el(
    'div',
    'opacity:.7;font-size:11px;' + LINE,
    pageUser ? '@' + pageUser + ' 글만 수집' : '⚠ 프로필 페이지 아님 — 전부 수집'
  );
  body.appendChild(statusEl);
  body.appendChild(scopeEl);

  const rule = () =>
    el('div', 'height:1px;background:rgba(255,255,255,.22);margin:8px 0');
  body.appendChild(rule());

  const statCss = 'font-size:11.5px;opacity:.92;' + LINE;
  const dateEl = el('div', 'font-size:12.5px;font-weight:700;' + LINE);
  const timeEl = el('div', statCss);
  const filteredEl = el('div', statCss);
  const backupEl = el('div', statCss);
  const restoredEl = el(
    'div',
    'font-size:11.5px;color:#c9f5d5;font-weight:600;' + LINE
  );
  const previewEl = el(
    'div',
    'font-size:11px;opacity:.72;margin-top:5px;' + LINE
  );
  // 복구 줄은 세션 중 값이 안 변한다 → 시작할 때 한 번만 보일지 정하고 끝낸다
  if (!restoredCount) restoredEl.style.display = 'none';
  else restoredEl.textContent = `이전 수집분 ${restoredCount}개 복구됨`;

  body.appendChild(dateEl);
  body.appendChild(timeEl);
  body.appendChild(filteredEl);
  body.appendChild(backupEl);
  body.appendChild(restoredEl);
  body.appendChild(previewEl);
  body.appendChild(rule());

  // 버튼은 폭을 고정한다 — 라벨이 바뀌어도 줄이 안 밀리게
  function mkBtn(label, bg, width) {
    return el(
      'button',
      [
        'box-sizing:border-box', 'width:' + width + 'px', 'text-align:center',
        'background:' + bg, 'color:#fff', 'border:0', 'border-radius:6px',
        'padding:6px 0', 'margin:0 6px 5px 0', 'cursor:pointer',
        'font:600 12px -apple-system,sans-serif',
      ].join(';'),
      label
    );
  }

  const saveBtn = mkBtn('저장', '#1c1c1e', 64);
  const toggleBtn = mkBtn('▶ 시작', '#2f5d62', 78);
  const stopBtn = mkBtn('종료', '#8a1c1c', 56);
  const speedBtn = mkBtn('속도: 보통', '#255c33', 92);
  const clearBtn = mkBtn('백업 비우기', '#255c33', 92);

  const row1 = el('div', 'margin-top:2px');
  row1.appendChild(saveBtn);
  row1.appendChild(toggleBtn);
  row1.appendChild(stopBtn);
  const row2 = el('div', '');
  row2.appendChild(speedBtn);
  row2.appendChild(clearBtn);
  body.appendChild(row1);
  body.appendChild(row2);

  function fmtMs(ms) {
    const s = Math.floor(ms / 1000);
    const m = Math.floor(s / 60);
    return m > 0 ? `${m}분 ${s - m * 60}초` : `${s}초`;
  }

  function statusText() {
    if (!started) return '대기 중 — [시작]을 누르세요';
    if (running) return '자동 스크롤 중…';
    if (autoStopped) return '새 글이 더 안 보입니다';
    return '일시정지됨';
  }

  function toggleLabel() {
    if (!started) return '▶ 시작';
    return running ? '일시정지' : '계속';
  }

  // DOM 을 새로 만들지 않는다 — 글자만 갈아끼운다
  function render() {
    countNum.textContent = String(store.size);
    statusEl.textContent = statusText();
    toggleBtn.textContent = toggleLabel();
    dateEl.textContent = oldestDate ? `지금 ▸ ${oldestDate} 지점` : '지금 ▸ —';
    const gained = store.size - restoredCount;
    const perMin = activeMs > 0 ? Math.round(gained / (activeMs / 60000)) : 0;
    timeEl.textContent = `${fmtMs(activeMs)} · 분당 ${perMin}개`;
    filteredEl.textContent = `남의 글 ${filteredIds.size}개 걸러냄`;
    backupEl.textContent = backupState || '백업 대기 중';
    backupEl.style.color = backupFailed ? '#ffd4d4' : '';
    backupEl.style.fontWeight = backupFailed ? '700' : '';
    // 빈 값이면 줄이 사라져 상자 높이가 변하므로 항상 뭔가를 채운다
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
      (a.created_at || '').localeCompare(b.created_at || '')
    );
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: 'application/json',
    });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `threads_manual_${data.length}posts.json`;
    a.click();
    backup(true);
    saveBtn.textContent = '저장 ✓';
    setTimeout(() => {
      saveBtn.textContent = '저장';
    }, 1500);
  };

  toggleBtn.onclick = () => {
    if (!started) {
      // 첫 클릭 = 진짜 시작. 여기서부터 수확 타이머도 일하기 시작한다.
      started = true;
      running = true;
      stagnantTicks = 0;
      autoStopped = false;
      harvest();
      render();
      return;
    }
    running = !running;
    if (running) {
      stagnantTicks = 0;
      autoStopped = false;
    } else {
      backup(true);
    }
    render();
  };

  speedBtn.onclick = () => {
    speedIdx = speedIdx + 1 >= SPEEDS.length ? 0 : speedIdx + 1;
    clearInterval(scrollTimer);
    scrollTimer = setInterval(scrollTick, SPEEDS[speedIdx].ms);
    render();
  };

  clearBtn.onclick = () => {
    if (
      !confirm(
        '브라우저에 저장된 백업과 지금까지 모은 목록을 모두 지웁니다.\n되돌릴 수 없습니다. 저장(다운로드)한 파일은 그대로 남습니다.\n\n지울까요?'
      )
    )
      return;
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
    delete window.__threadsCollector;
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

    if (store.size === lastSize) {
      stagnantTicks++;
      if (stagnantTicks >= STAGNANT_LIMIT) {
        stopAuto(null);
        return;
      }
    } else {
      stagnantTicks = 0;
    }
    lastSize = store.size;

    backup(false);
    render();
    window.scrollBy(0, window.innerHeight * SPEEDS[speedIdx].amount);
  }

  // 정해진 간격에만 확인한다 (감시자 없음 — 자기 자신을 볼 일이 없음)
  // [시작] 전에는 아무것도 하지 않는다 — 완전 대기
  const harvestTimer = setInterval(() => {
    if (!started) return;
    harvest();
    render();
  }, HARVEST_MS);
  let scrollTimer = setInterval(scrollTick, SPEEDS[speedIdx].ms);

  window.__threadsCollector = { store, harvest, backup };
  render();
  console.log(
    `수집기 v5 준비됨 — [▶ 시작]을 누르면 시작합니다.${
      restoredCount ? ` 이전 백업 ${restoredCount}개를 복구했습니다.` : ''
    }`
  );
})();
