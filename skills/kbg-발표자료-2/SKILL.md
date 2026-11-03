---
name: kbg-발표자료-2
description: kbg 발표자료 2 — 라인아트 내레이션형. 혼잡스(@honjobs) 이야기형 영상의 화면 문법을 실측한 HTML 모션 덱. 흰 바탕에 거친 손그림 선의 인물(흰 셔츠·검은 넥타이 내레이터)·로봇·노트북·책 라인아트, 화면 위쪽 큰 자막(52px)과 노랑 형광펜, 말풍선, 기울어진 스티커가 툭 떨어지는 등장, 5색 티어 리스트, 80/20 분할 막대, 켄번스 줌과 흔들림. "kbg 발표자료 2", "kbg-발표자료-2", "/kbg-발표자료-2", "라인아트 발표자료", "손그림 인물 영상", "이야기형 발표자료" 요청 시 발동. 설교·사례·동기부여 영상에 맞다.
---

# kbg 발표자료 2 — 라인아트 내레이션

출처: 유튜브 혼잡스(@honjobs) 발표 영상 프레임 실측(2026-10-28). 다른 스타일과 비교·선택은 라우터 [kbg-발표자료](../kbg-발표자료/SKILL.md)에서 한다.
[template.html](template.html)이 정본 틀이다(엔진·CSS 인라인, 단독 실행). **구조와 클래스는 그대로 두고 내용만 바꾼다.**

## 0. 시작 전

- 발표자료이므로 **작업 시작 전 한 번** 묻는다: "`awesome-ai-motion` 스킬도 함께 쓸까요?" (CLAUDE.md 8번). 승낙해도 이 스킬의 시각 규칙이 우선이다.
- [template.html](template.html)을 `~/Desktop/cysjavis/<주제폴더>/<한글이름>.html`로 복사한 뒤 고친다(정본). 아티팩트는 사본이다.
- 통계는 출처 있는 값만 쓴다. 없으면 자막이나 라벨에 "(예시)"를 붙인다.
- 공용 마크업(`data-in`, `data-cams`, `data-count` 등)과 진행 키는 라우터 [kbg-발표자료](../kbg-발표자료/SKILL.md) 2·3절에 있다.

## 1. 스타일 사양 (영상 실측)

| 토큰 | 값 | 쓰임 |
|---|---|---|
| `--bg` | `#FFFFFF` | 순백 |
| `--ink` | `#111` | 라인아트 선, 제목 |
| `--yellow` | `#FADC46` | 자막 `mark` 형광펜, `.hl` 아래쪽 반 형광 |
| `--red` / `--blue` | `#E8342A` / `#2A6CF0` | 손글씨 주석, 화살표 |
| `--t1`~`--t5` | `#E8342A` `#F5782A` `#FAC31E` `#5DBB7A` `#6F8FD8` | 티어 리스트 줄 색 |

| 글꼴 | 쓰임 |
|---|---|
| Pretendard 500/800 | **상단 자막** 52px(핵심어는 `<mark>`), 본문 |
| Black Han Sans | 표지 제목 `.title`, 분할 막대 숫자 |
| Gaegu 700 | 손글씨 주석 `.hand` ("↳ 수치는 예시") |

화면 구성: 자막이 **화면 위쪽**에 크게 놓이고 그림이 가운데를 차지한다. 그림은 한두 개, 여백이 많다. 선은 `#rough` SVG 필터로 손떨림을 준다.

## 2. 부품

| 클래스·심볼 | 모양 |
|---|---|
| `<use href="#guy">` | 내레이터: 흰 셔츠·검은 넥타이·검은 머리 |
| `#bot` `#laptop` `#book` | 로봇, 노트북, 책 라인아트 |
| `img.art` | 생성한 라인아트 이미지 슬롯(아래 프롬프트) |
| `.ill` (`.kb` `.sway`) | 그림 묶음. `.kb` 천천히 확대, `.sway` 살짝 흔들림 |
| `.bubble` | 꼬리 달린 말풍선 |
| `.sticker.drop` (`--r:-8deg`) | 기울어진 스티커가 위에서 툭 떨어짐 |
| `dl.tier` | 5색 티어 표, `dd` 안에 스티커 |
| `.split > i + i` | 80/20 분할 막대 + `.lab` 라벨 |
| `.stmt` 96px | 한 문장 결론 |
| `.hand` | 손글씨 주석 |

예시 장면 7개: 표지(내레이터+제목) → 말풍선 질문 → 사람 vs 로봇 → 티어 리스트 → 80/20(예시) → 책상 소품 → 마무리 한 문장.

## 3. 모션 어휘

| 움직임 | 구현 | 쓸 때 |
|---|---|---|
| 켄번스 | `.kb` (`scale` 속성) | 그림이 오래 머무는 장면 |
| 흔들림 | `.sway` (`rotate` 속성) | 인물이 말하는 느낌 |
| 스티커 낙하 | `.sticker.drop` | 목록 항목을 하나씩 |
| 형광펜 | 자막 `<mark>` | 박자마다 핵심어 하나 |
| 말풍선 팝 | `.bubble` | 질문·인용 |

`.kb`·`.sway`는 `transform`이 아니라 `scale`·`rotate` 속성을 쓴다. `transform`을 쓰면 가운데 정렬(`translateX`)이 깨진다.

## 4. 라인아트 새로 그리기

내장 심볼로 부족하면 이미지를 만들어 `img.art`에 넣는다. 무료는 `qwen-local-image`, 유료 `media-gen-image`는 **비용을 먼저 묻는다**.

> minimalist black ink line art illustration, single continuous rough pen stroke, white background, no shading, no color, [사람이 책상에서 성경을 읽는 모습], simple cartoon style, flat, lots of white space

배경이 흰색이 아니면 투명 PNG로 받아 `mix-blend-mode:multiply`를 준다.

## 절차

1. 원고를 **장면 → 박자**로 쪼갠다. 박자 하나 = 자막 한 줄 = 화면 변화 하나. 자막은 25자 안팎.
2. 템플릿 예시 장면 중 가장 가까운 것을 복제해 내용만 바꾼다. 쓰지 않는 예시 장면은 지운다.
3. 브라우저로 열어 →로 넘기며 확인한다. 넘침·겹침은 글자 크기보다 **박자를 나눠서** 푼다.
4. 장면별 확인 사진: `node ~/.claude/skills/kbg-발표자료/tools/record.mjs 발표.html --shots 확인 --beats`

## 산출

```bash
node ~/.claude/skills/kbg-발표자료/tools/record.mjs 발표.html 발표.mp4 --fps 30
```
```bash
node ~/.claude/skills/kbg-발표자료/tools/record.mjs 발표.html 유인물.pdf
```
- 음성이 있으면 `--audio 음성.mp3`, 자막 없는 영상은 `--nosubs`. 박자 길이는 `li[data-dur]`로 음성에 맞춘다.
- 강의 현장에서는 HTML을 그대로 연다(F 전체화면, S 자막 토글, `?auto` 자동재생).
