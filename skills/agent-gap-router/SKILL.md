---
name: agent-gap-router
description: 에이전트 작업의 네 빈틈(시키기·만들기·보고받기·확인하기)마다 이미 설치된 스킬을 골라 붙이는 라우터. 외부 5종(Ouroboros·img2threejs·UI Skills·Chisle·Reticle)의 핵심 장치만 빌려 와 설치 없이 쓴다. "빈틈 라우터", "다섯 스킬 흐름", "시키기부터 확인까지", "모호함 점수", "3줄 보고", "통과/실패/확인불가 판정" 요청 시 사용.
---

# 에이전트 빈틈 라우터

출처: Layperson 영상 「클로드 코드 종결 미친 스킬 5가지」(2026-09-17) + 각 저장소 README(2026-10-09 확인).
외부 도구를 새로 깔지 않고, 각 도구의 **핵심 장치 하나씩**을 이 환경의 기존 스킬에 얹는다.

## 1. 시키기 — 모호함 게이트 (Ouroboros에서 빌림)

작업 착수 전 요청을 5개 축으로 채점한다. 각 축 0(명확)~1(모름), 평균이 **모호함 점수**.

| 축 | 질문 |
|---|---|
| 대상 | 누가 읽고/쓰나? |
| 산출물 | 형식·분량·저장 위치는? |
| 범위 | 무엇을 빼나? |
| 완료 조건 | 무엇을 보면 끝났다고 하나? |
| 제약 | 마감·출처·금지 사항은? |

- 점수 **≥ 0.2** → `grill-me` 또는 `deep-interview`로 질문 3개씩 묻고 재채점.
- 점수 **< 0.2** → 숨은 가정 목록을 한 줄씩 적고 착수.
- 웹/앱이면 `appbuild-plan-interview`.
- CLAUDE.md 3번(중간에 묻지 않기)과 충돌하지 않게 **착수 전 1회만** 묻는다.

## 2. 만들기 — 결과물 종류별 라우팅

| 결과물 | 스킬 |
|---|---|
| 사진 속 물체를 웹 3D로 | `img2threejs` (설치됨) |
| 화면 UI 다듬기 | `impeccable` → `design-audit` → `better-typography`/`better-colors`/`better-accessibility` |
| 레퍼런스 스타일 찾기 | `refero-design`, `design-pick` |
| UI 규칙 1~3개만 고르기 | UI Skills MCP(`https://www.ui-skills.com/mcp`)가 연결돼 있으면 `list_skills` → 가장 작은 것 1개 `get_skill` |

원칙(UI Skills에서 빌림): 디자인 스킬은 **목적에 맞는 가장 작은 것 1개, 많아야 3개**만 불러온다.

## 3. 보고받기 — 3줄 보고 (Chisle에서 빌림)

`ponytail`이 이미 켜져 있으므로 Chisle은 설치하지 않는다. 최종 보고만 이 형식으로:

```
했다: <결과 + 링크>
바꿨다: <수정한 파일/설정>
뺐다: <의도적으로 안 한 것, 추가 시점>
```

## 4. 확인하기 — 3값 판정 (Reticle에서 빌림)

"완료" 선언 전 실제로 열어 보고 판정한다.

- **통과**: 실제 동작/화면/수치를 근거로 확인.
- **실패**: 근거 + 고칠 위치(`파일:줄`).
- **확인불가**: 왜 못 봤는지. 확인불가를 통과로 바꿔 쓰지 않는다.

도구: 웹 페이지는 내장 브라우저(`mcp__Claude_Browser__*`)로 열어 클릭·콘솔·네트워크 확인, 문서는 `qa-inspector`, 영상은 `video-verify`, 코드는 `superpowers:verification-before-completion`.
React/Vue 앱 프로젝트에서 상태·네트워크까지 봐야 하면 그 프로젝트에만 Reticle을 설치한다:
`claude mcp add reticle -s project -- npx @reticlehq/server mcp`
