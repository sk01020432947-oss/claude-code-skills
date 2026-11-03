---
name: kbg-발표자료
description: kbg 발표자료 선택 라우터. 유튜브 혼잡스(@honjobs) 채널 발표 영상의 화면 문법을 실측해 만든 5가지 HTML 모션 발표자료(1 클린 도식, 2 라인아트 내레이션, 3 손글씨 한 장 지도, 4 데스크톱 창 타임라인, 5 보드게임 로드맵) 가운데 하나를 골라 만든다. 공용 엔진(박자 진행·자막·카메라 팬줌·카운트업·자동재생)과 녹화 도구(MP4·PDF·PNG)가 들어 있다. "kbg 발표자료", "kbg-발표자료", "/kbg-발표자료", "혼잡스 스타일 발표자료", "발표자료 스타일 골라줘", "모션 발표자료 만들어줘" 요청 시 발동. 번호가 정해져 있으면 kbg-발표자료-1~5를 바로 쓴다.
---

# kbg 발표자료 — 스타일 선택 라우터

출처: 유튜브 혼잡스(@honjobs) 발표 영상 9편 프레임·자막 실측(2026-10-28). 분석 메모는 [references/혼잡스_분석.md](references/혼잡스_분석.md)에 있고, 키 프레임은 [references/frames/](references/frames/)에 있다.

## 0. 시작 전

- 발표자료이므로 **작업 시작 전 한 번** 묻는다: "`awesome-ai-motion` 스킬도 함께 쓸까요?" (CLAUDE.md 8번). 승낙해도 고른 스타일의 시각 규칙이 우선이다.
- 스타일 번호가 없으면 아래 표로 **하나를 추천**하고 바로 진행한다. 사용자가 고르게 하려면 AskUserQuestion으로 5개 보기를 낸다.
- 결과물은 `~/Desktop/cysjavis/<주제폴더>/<한글이름>.html`(정본)으로 만든다.
- 통계는 출처 있는 값만 쓴다. 없으면 "(예시)"를 붙인다.

## 1. 어느 스타일을 쓸까

| 번호 | 스킬 | 화면 | 잘 맞는 내용 | 예시 장면 수 |
|---|---|---|---|---|
| 1 | [kbg-발표자료-1](../kbg-발표자료-1/SKILL.md) | 흰 바탕 · 검은 굵은 고딕 · 둥근 박스 도식 · 막대 비교 | 개념 정리, 구조·과정 설명, 비교, 강의 | 10 |
| 2 | [kbg-발표자료-2](../kbg-발표자료-2/SKILL.md) | 흰 바탕 · 손그림 인물(라인아트) · 상단 큰 자막 · 노랑 형광펜 | 이야기·사례 중심 설교, 동기부여, 해설 영상 | 7 |
| 3 | [kbg-발표자료-3](../kbg-발표자료-3/SKILL.md) | 큰 종이 한 장에 손글씨 지도 · 카메라가 구역을 옮겨 다님 · 빨간 동그라미 | 전체 개관 → 부분 확대, 체크리스트, 단계 요약 | 3(한 장 지도 7박자) |
| 4 | [kbg-발표자료-4](../kbg-발표자료-4/SKILL.md) | 모눈 바탕 · 맥 창 · 달력 · 커서 클릭 · 오른쪽 월 레일 | 일정·연간 계획, 도구 사용법, 회고, 작업 과정 | 6 |
| 5 | [kbg-발표자료-5](../kbg-발표자료-5/SKILL.md) | 보드게임 트랙 · 자동차가 정거장 이동 · 크레용 제목 | 로드맵, 커리큘럼, 학기·사역 단계, 여정 | 4(트랙 6정거장) |

이미 있던 스타일도 함께 고를 수 있다: [kbg-발표자료(1)](../kbg-발표자료(1)/SKILL.md)(코드팩토리풍 오프화이트 타일 노드), [kbg-발표자료(영상)](../kbg-발표자료(영상)/SKILL.md).

빠른 판정: **설명 → 1**, **이야기 → 2**, **한 장 요약 → 3**, **시간·도구 → 4**, **단계·여정 → 5**.

## 2. 공용 엔진 마크업 (5종 모두 같다)

각 스킬의 `template.html`은 엔진·CSS가 인라인된 단독 파일이다. **구조와 클래스는 두고 내용만 바꾼다.**

```html
<section class="scene" data-ch="book" data-mark="2" data-cams="x,y,k|x,y,k">
  <ol class="caps"><li data-dur="3">박자 1 자막</li><li>박자 2 자막</li></ol>
  <div data-in="1" data-out="3">박자 1에 나타나 3에 사라지는 요소</div>
  <b data-count="1250" data-dur="1.4">0</b>   <!-- 카운트업 -->
  <div class="world">…카메라가 움직이는 큰 캔버스…</div>
</section>
```

| 속성 | 뜻 |
|---|---|
| `section.scene` | 장면 1개. 박자 수 = 자막 수·카메라 수·최대 `data-in`+1 중 큰 값 |
| `ol.caps li[data-dur]` | 박자별 자막. `data-dur` 초(없으면 글자 수 × 0.13초, 최소 1.6초) |
| `data-in` / `data-out` | 요소가 켜지는/꺼지는 박자(0부터). 켜지면 `.on` 클래스 |
| `data-count` | 숫자 카운트업(소수 자리 유지, ko-KR 천 단위 쉼표) |
| `data-cams` | `.world`를 박자마다 (x,y) 중심·배율 k로 팬·줌 |
| `data-ch` | 새 챕터 시작 + 왼쪽 레일 아이콘 이름 |
| `data-mark` | `#stage[data-mark]`로 복사 → 장면 밖 고정 요소(월 레일 등) 강조 |
| `data-icon` | 내장 아이콘 삽입: home crown book chart users bulb shield clock cross heart check flag star chat gear pen map gift target coin calendar search music folder phone school |
| `.scene[data-beat]` | 현재 박자. CSS에서 박자별 위치를 줄 때 쓴다 |

## 3. 진행 키 · URL

- 다음: → Space PageDown Enter, 화면 오른쪽 80% 클릭 / 이전: ← PageUp Backspace, 왼쪽 20% 클릭
- F 전체화면 · S 자막 켜고 끄기 · Home 처음으로
- `?auto` 자동재생 · `?nosubs` 자막 없이 · `#3` 3번 장면부터

## 4. 산출 (공용 녹화 도구)

Node와 ffmpeg, Google Chrome이 있으면 된다(추가 설치 없음).

```bash
node ~/.claude/skills/kbg-발표자료/tools/record.mjs 발표.html 발표.mp4 --fps 30
```
```bash
node ~/.claude/skills/kbg-발표자료/tools/record.mjs 발표.html 유인물.pdf
```
```bash
node ~/.claude/skills/kbg-발표자료/tools/record.mjs 발표.html --shots 장면들 --beats
```

- MP4: 1920×1080, 결정적 시간 탐색으로 프레임을 찍는다. `--audio 음성.mp3`로 음성 합성, `--nosubs`로 자막 제외.
- PDF: 장면마다 마지막 박자 1쪽(16:9). 박자별 쪽이 필요하면 `--shots … --beats`로 PNG를 받는다.
- 브라우저 인쇄(⌘P)는 카메라 장면이 깨지므로 쓰지 않는다.

## 5. 엔진 고치기

엔진 원본은 [engine/](engine/)에 있다(`engine.js`, `base.css`, `src/t1~t5.html`). 고친 뒤 `python3 engine/build.py engine/src/t3.html`처럼 돌리면 같은 자리에 `t3.built.html`이 생긴다. 그것을 각 스킬의 `template.html`로 복사한다.
