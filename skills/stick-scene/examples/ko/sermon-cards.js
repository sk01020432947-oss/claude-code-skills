// 실습 예제: 설교 원고를 기계에 넣고 버튼을 누르면 카드뉴스 3장이 나온다.
// Load after stick.js. Use as <stick-scene scene="sermon-cards" play="view"></stick-scene>.
(function () {
  const SC = (window.SCENES = window.SCENES || {});
  const R = window.RIG;
  const { C, E, P, mix, legs, walkSeg, fig, inkFill, rr, ln, text, seg, breathe, pulse, lp, sparks, tickBadge, bubble, words, circle } = R;

  const M = { x: -20, y: -150, w: 112, h: 104 };   // 기계 몸통
  const BTN = { x: M.x + 4, y: M.y + 66 };          // 왼쪽 옆면 버튼
  const HOME = -150, AT = -64;
  const CARDS = [118, 144, 170];                     // 나오는 카드 3장의 x
  // Gaegu는 같은 px에서 라틴 글꼴보다 작아 보여 한글 라벨은 약 1.25배로 키운다.
  const REST = P({ hF: [12, -60], hB: [-4, -52] });

  function machine(g, busy, t) {
    ln(g, M.x + 18, M.y + M.h, M.x + 10, 0, 2.2);
    ln(g, M.x + M.w - 18, M.y + M.h, M.x + M.w - 10, 0, 2.2);
    rr(g, M.x, M.y, M.w, M.h, 7);
    inkFill(g, C.paper, 1.7);
    text(g, '설교 → 카드뉴스', M.x + M.w / 2, M.y + 18, 12, C.umber);
    ln(g, M.x + 10, M.y + 27, M.x + M.w - 10, M.y + 27, 1, C.faint);
    for (let i = 0; i < 4; i++) {                   // 일하는 동안 차례로 깜빡이는 전구
      const on = busy > 0 && Math.sin(t * 9 - i * 1.3) > 0 ? busy : 0;
      circle(g, M.x + 26 + i * 20, M.y + 44, 5);
      inkFill(g, on > 0.5 ? C.butter : C.paper, 1.3);
    }
    words(g, M.x + 16, M.y + 62, M.w - 32, 2);
    rr(g, M.x + M.w - 6, M.y + M.h - 30, 10, 18, 3);  // 오른쪽 배출구
    inkFill(g, C.ink, 1.2);
    rr(g, BTN.x - 6, BTN.y - 6, 12, 12, 3);
    inkFill(g, C.red, 1.3);
  }

  function sheet(g, k) {                             // 원고 한 장이 위 투입구로 빨려 들어간다
    const y = M.y - 34 + 42 * k;
    rr(g, M.x + 36, y, 40, 46, 3);
    inkFill(g, C.paper, 1.4);
    text(g, '원고', M.x + 56, y + 12, 11, C.muted);
    words(g, M.x + 42, y + 20, 28, 3);
  }

  function card(g, x, k, n) {
    if (k <= 0) return;
    const y = -86 + (1 - k) * 18;
    g.save();
    g.translate(x, y);
    g.rotate((n - 1) * 0.06);
    g.scale(0.4 + 0.6 * k, 0.4 + 0.6 * k);
    rr(g, -11, -15, 22, 30, 3);
    inkFill(g, C.butterSoft, 1.4);
    text(g, String(n + 1), 0, -4, 10, C.umber);
    ln(g, -6, 6, 6, 6, 1.2, C.umber);
    g.restore();
  }

  SC['sermon-cards'] = {
    dur: 6.5,
    width: 380,
    label: '사람이 설교 원고를 기계에 넣고 버튼을 누르자 요점 카드 세 장이 나온다.',
    draw(g, S) {
      const T = S.on ? S.u * this.dur : -1;
      const t = S.t;
      let x = HOME, gait = { ph: 0, amp: 0 };
      let pose = breathe(REST, t);
      let busy = 0, sk = 0, ck = [0, 0, 0], done = 0, fade = 1;
      if (T < 0) {
        pose = mix(pose, P({ hF: [10, -96], head: [7, -116], hB: [-4, -54] }), pulse(t, 6, 2, 2.2));
      } else {
        fade = 1 - seg(T, this.dur - 0.45, this.dur);
        const ws = T < 3.5 ? walkSeg(T, 0, 0.8, HOME, AT) : walkSeg(T, 5.0, 5.9, AT, HOME);
        x = ws.x;
        gait = ws.dir < 0 ? { ph: -ws.ph, amp: ws.amp, stride: ws.stride } : ws;  // 뒤로 걸어 돌아갈 때 발 미끄러짐 방지
        const press = E.soft(seg(T, 0.8, 1.15)) * (1 - E.soft(seg(T, 1.5, 1.8)));
        const think = E.soft(seg(T, 1.9, 2.2)) * (1 - E.soft(seg(T, 2.9, 3.2)));
        const cheer = E.soft(seg(T, 3.6, 4.0)) * (1 - E.soft(seg(T, 4.5, 4.9)));
        pose = mix(pose, P({ hF: lp([BTN.x - 2, BTN.y], x, 0, 1), hB: [-4, -54], head: [9, -114], chest: [3, -90] }), press);
        pose = mix(pose, P({ hF: [10, -96], head: [7, -116], hB: [-4, -54] }), think);
        pose = mix(pose, P({ hF: [14, -132], hB: [-10, -130], head: [3, -118] }), cheer);
        sk = E.in(seg(T, 1.2, 1.9)) * fade;  // 끝에서 원고가 다시 올라와 idle과 맞춘다
        busy = seg(T, 1.6, 1.8) * (1 - seg(T, 3.0, 3.2));
        ck = CARDS.map((_, i) => E.back(seg(T, 2.6 + i * 0.3, 2.95 + i * 0.3)) * fade);
        done = seg(T, 3.4, 3.7) * fade;
      }
      pose = legs(pose, gait.ph, gait.amp, { arms: false, stride: gait.stride });

      if (sk < 1) { g.save(); g.globalAlpha = 1 - sk * sk; sheet(g, sk); g.restore(); }
      machine(g, busy, t);
      CARDS.forEach((cx, i) => card(g, cx, ck[i], i));
      tickBadge(g, M.x + M.w - 8, M.y + 8, done);
      fig(g, pose, x, 0, { wave: S.wave, wt: S.wt });
      sparks(g, CARDS[1], -118, seg(T, 3.4, 4.0), 16, 6);
      bubble(g, x + 4, -136, '음…', seg(T, 1.9, 2.1) * (1 - seg(T, 2.8, 3.0)), { tail: 8 });
    },
  };
})();
