/* kbg 발표자료 엔진 — 5개 템플릿 공용. 박자(beat) 진행·자막·레일·카메라·카운트업·자동재생·녹화(seek). PDF·MP4는 tools/record.mjs로 만든다.
   마크업: <section class="scene" data-ch="아이콘" data-cams="x,y,k|..."> <ol class="caps"><li>자막</li>…</ol> <요소 data-in="박자" data-out="박자">
   장면의 data-mark 값은 #stage[data-mark]로 복사된다(장면 밖 고정 요소 강조용). 박자는 .scene[data-beat]로 CSS에서 쓸 수 있다.
   URL: ?auto=1 자동재생 · ?rec 안내 숨김 · ?nosubs 자막 없이 · ?seek 녹화용(KBG_seek(t)) · #장면번호 */
(() => {
  const Q = new URLSearchParams(location.search);
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const stage = $('#stage'), cap = $('#cap'), rail = $('#rail'), hud = $('#hud');
  const scenes = $$('.scene', stage);
  const ICON = {
    home:'M3 11 12 3l9 8v10H3z M9 21v-6h6v6', crown:'M3 8l4 4 5-7 5 7 4-4-2 11H5z', book:'M4 4h7a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z M20 4h-5 M20 4v14h-6',
    chart:'M4 20V10 M10 20V4 M16 20v-7 M3 20h18', users:'M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z M2 21c0-4 3-6 7-6s7 2 7 6 M17 3a4 4 0 0 1 0 8 M22 21c0-3-2-5-4-6',
    bulb:'M9 18h6 M10 21h4 M12 3a6 6 0 0 0-4 10c1 1 1 2 1 3h6c0-1 0-2 1-3a6 6 0 0 0-4-10z', shield:'M12 3l8 3v6c0 5-4 8-8 9-4-1-8-4-8-9V6z',
    clock:'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z M12 7v5l3 2', cross:'M10 3h4v6h6v4h-6v8h-4v-8H4V9h6z', heart:'M12 20s-8-5-8-11a4 4 0 0 1 8-1 4 4 0 0 1 8 1c0 6-8 11-8 11z',
    check:'M4 12l5 5L20 6', flag:'M5 21V4 M5 4h12l-2 4 2 4H5', star:'M12 3l3 6 6 1-4.5 4 1 6-5.5-3-5.5 3 1-6L3 10l6-1z', chat:'M4 5h16v11H9l-5 4z',
    gear:'M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z M12 2v3 M12 19v3 M2 12h3 M19 12h3 M5 5l2 2 M17 17l2 2 M5 19l2-2 M17 7l2-2', pen:'M4 20l4-1L19 8l-3-3L5 16z M14 7l3 3',
    map:'M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z M9 4v14 M15 6v14', gift:'M3 9h18v4H3z M5 13v8h14v-8 M12 9v12 M12 9c-3 0-5-1-5-3s3-2 5 3c2-5 5-5 5-3s-2 3-5 3',
    target:'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z M12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8z', coin:'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z M9 9h4.5a1.5 1.5 0 0 1 0 3H10a1.5 1.5 0 0 0 0 3H15 M12 7v2 M12 15v2',
    calendar:'M4 6h16v15H4z M4 10h16 M8 3v5 M16 3v5', search:'M10 17a7 7 0 1 0 0-14 7 7 0 0 0 0 14z M15 15l6 6', music:'M9 18V5l11-2v13 M9 18a3 3 0 1 1-3-3 3 3 0 0 1 3 3z M20 16a3 3 0 1 1-3-3 3 3 0 0 1 3 3z',
    folder:'M3 6h6l2 2h10v11H3z', phone:'M7 3h10v18H7z M11 18h2', school:'M2 9l10-5 10 5-10 5z M6 11v5c3 2 9 2 12 0v-5'
  };
  const icon = n => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="${ICON[n] || ICON.star}"/></svg>`;
  $$('[data-icon]').forEach(e => e.insertAdjacentHTML('afterbegin', icon(e.dataset.icon)));

  // 장면별 박자 수 · 자막 · 카메라
  let ch = -1; const chapters = [];
  scenes.forEach((s, i) => {
    if (s.dataset.ch || i === 0) { ch++; chapters.push(s.dataset.ch || 'star'); }
    s._ch = ch;
    const caps = $$(':scope > .caps > li', s);
    s._caps = caps.map(li => li.innerHTML);
    s._durs = caps.map(li => +li.dataset.dur || Math.max(1.6, li.textContent.trim().length * 0.13));
    s._cams = (s.dataset.cams || '').split('|').filter(Boolean).map(c => c.split(',').map(Number));
    let n = Math.max(caps.length, s._cams.length, 1);
    $$('[data-in]', s).forEach(e => n = Math.max(n, +e.dataset.in + 1));
    s._n = n; s._world = $('.world', s);
  });
  if (rail) rail.innerHTML = chapters.map((c, k) => `<i style="--k:${k}">${icon(c)}</i>`).join('');

  // 타임라인(자동재생·녹화 공용)
  const tl = []; let T = 0;
  scenes.forEach((s, si) => { for (let b = 0; b < s._n; b++) { const d = s._durs[b] ?? 1.8; tl.push({ si, b, t: T, d }); T += d; } });
  window.KBG_TOTAL = T + 1.5; window.KBG_TL = tl;

  let clock = () => performance.now() / 1000, si = -1, bi = 0;
  const counters = [];
  function show(nsi, nbi) {
    const s = scenes[nsi];
    if (nsi !== si) { scenes.forEach((x, k) => x.classList.toggle('cur', k === nsi)); scenes.forEach((x, k) => x.classList.toggle('past', k < nsi)); }
    si = nsi; bi = nbi;
    $$('[data-in]', s).forEach(e => {
      const on = +e.dataset.in <= bi && !(e.dataset.out && +e.dataset.out <= bi);
      if (on && !e.classList.contains('on') && e.dataset.count != null) counters.push({ e, t0: clock() });
      e.classList.toggle('on', on);
    });
    s.dataset.beat = bi;
    stage.dataset.scene = nsi + 1; stage.dataset.mark = s.dataset.mark || '';
    if (s._world && s._cams.length) { const [x, y, k] = s._cams[Math.min(bi, s._cams.length - 1)]; s._world.style.transform = `translate(960px,540px) scale(${k || 1}) translate(${-x}px,${-y}px)`; }
    if (cap) { const c = s._caps[Math.min(bi, s._caps.length - 1)] || ''; cap.innerHTML = c ? `<span>${c}</span>` : ''; }
    if (rail) { rail.style.setProperty('--c', s._ch); $$('i', rail).forEach((e, k) => e.dataset.d = Math.min(3, Math.abs(k - s._ch))); }
    if (hud) hud.textContent = `${nsi + 1}/${scenes.length} · ${bi + 1}/${s._n}`;
    location.replace('#' + (nsi + 1));
  }
  function tick() {
    const now = clock();
    for (const c of counters) {
      const p = Math.min(1, (now - c.t0) / (+c.e.dataset.dur || 1.2)), v = +c.e.dataset.count * (1 - Math.pow(1 - p, 3));
      const dec = (c.e.dataset.count.split('.')[1] || '').length;
      c.e.textContent = v.toLocaleString('ko-KR', { minimumFractionDigits: dec, maximumFractionDigits: dec });
    }
  }
  const step = d => {
    let s = si, b = bi + d;
    if (b >= scenes[s]._n) { if (s + 1 >= scenes.length) return; s++; b = 0; }
    if (b < 0) { if (s === 0) return; s--; b = scenes[s]._n - 1; }
    show(s, b);
  };

  // 녹화용: 시간 t의 화면을 결정적으로 그린다 (tools/record.mjs가 호출)
  window.KBG_seek = t => {
    clock = () => t;
    let k = tl.length - 1; while (k > 0 && tl[k].t > t) k--;
    const cur = tl[k];
    if (cur.si !== si || cur.b !== bi) { show(cur.si, cur.b); document.body.offsetWidth; document.getAnimations().forEach(a => a._born ??= cur.t); }
    document.getAnimations().forEach(a => { a._born ??= 0; a.pause(); a.currentTime = Math.max(0, (t - a._born) * 1000); });
    tick();
  };

  function fit() { const k = Math.min(innerWidth / 1920, innerHeight / 1080); stage.style.transform = `translate(-50%,-50%) scale(${k})`; }
  const B = document.body.classList;
  if (Q.has('rec') || Q.has('auto') || Q.has('seek')) B.add('rec');
  if (Q.has('nosubs')) B.add('nosubs');
  addEventListener('resize', fit); fit();
  if (!Q.has('seek')) (function loop() { tick(); requestAnimationFrame(loop); })();
  const start = Math.max(0, Math.min(scenes.length - 1, (parseInt(location.hash.slice(1)) || 1) - 1));
  show(start, 0);
  if (Q.has('seek')) { show(0, 0); return; }
  addEventListener('keydown', e => {
    if (['ArrowRight', ' ', 'PageDown', 'Enter'].includes(e.key)) { e.preventDefault(); step(1); }
    else if (['ArrowLeft', 'PageUp', 'Backspace'].includes(e.key)) step(-1);
    else if (e.key === 'f' || e.key === 'F') document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
    else if (e.key === 's' || e.key === 'S') B.toggle('nosubs');
    else if (e.key === 'Home') show(0, 0);
  });
  addEventListener('click', e => { if (!e.target.closest('a')) step(e.clientX < innerWidth * 0.2 ? -1 : 1); });
  if (Q.has('auto')) (function next() { const s = scenes[si]; setTimeout(() => { if (si === scenes.length - 1 && bi === s._n - 1) return B.add('done'); step(1); next(); }, (s._durs[bi] ?? 1.8) * 1000); })();
})();
