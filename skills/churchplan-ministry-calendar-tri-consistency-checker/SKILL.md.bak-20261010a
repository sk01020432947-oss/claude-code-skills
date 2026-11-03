---
name: churchplan-ministry-calendar-tri-consistency-checker
disable-model-invocation: true
description: >-
  ## TLDR — [INTERNAL 하위 스킬] churchplan-ministry-calendar 대표 스킬 전용. "한 방향을 잇는 자" AI Agent. 분기별로 설교(강단)·행사(체험)·사역(목표 마일스톤+캠페인)이 같은 메시지를 향하는지 3중 정합을 점검한다(02 라인 173 "행사 주간의 설교·시즌 강조점·사역의 타이밍이 한 방향인지"). 한 방향이면 힘이 모이고, 어긋나면 간극(gap)을 드러낸다 — 정죄가 아니라 거울.

  ## Triggers — 모델 자동 발동 금지(disable-model-invocation). 대표 스킬 churchplan-ministry-calendar가 layer-merger의 격자 통합 직후 호출한다(먼저 「흡수한 역할」의 시즌 정렬 `season_alignment`를 채우고 3중 정합으로 간다).

  ## Detailed Methodology — 입력: calendar.json weeks[](sermon·events·campaigns·milestones)+season_alignment+meta.season_frame. 각 분기의 세 추동력을 추출 — sermon_thrust(그 분기 강단 메시지)·event_thrust(그 분기 핵심 행사 지향)·ministry_thrust(목표 마일스톤 + 진행 캠페인). 셋이 한 방향인가? 산출 tri_consistency[]에 quarter·sermon_thrust·event_thrust·ministry_thrust·aligned(bool)·gap(어긋난 경우 간극 서술). 박사님 시즌제 철학 — 같은 분기 설교·행사·사역이 한 메시지를 동시에 전하면 "힘이 모인다". 어긋남은 차단이 아니라 경고(gap 서술). 사역=목표+캠페인(보완2 명명, action-planner #7의 분해와 다름 — 여기선 방향 정합만).
---

# churchplan-ministry-calendar-tri-consistency-checker — 한 방향을 잇는 자 (INTERNAL)

> 대표 스킬 `churchplan-ministry-calendar`가 호출하는 INTERNAL 하위 스킬. **AI Agent 역할: 한 방향을 잇는 자.** 강단·행사·사역이 같은 곳을 보게 한다.

## 역할 (한 방향이면 힘이 모인다)
박사님 프레임워크(02 라인 173): *"행사 주간의 설교, 시즌의 강조점, 사역의 타이밍이 한 방향인지."* 분기별로 설교·행사·사역(목표 마일스톤+캠페인) 세 추동력이 같은 메시지를 향하는지 점검한다.

## 입력
- `calendar.json`의 `weeks[]`(sermon·events·campaigns·milestones)·`season_alignment`·`meta.season_frame`
- **정렬 판정 결정론 근거**: `weeks[].sermon.purpose`(layer-merger가 #4 series.purpose 전사)·`weeks[].events[].serves_axes`(layer-merger가 #5 serves_axes 전사) — title 추측이 아니라 전사된 필드로 추동력을 잡는다.

## 세 추동력 (보완2 — "사역"=목표+캠페인)
1. **`sermon_thrust`**: 그 분기 강단이 전하는 핵심 메시지(`weeks[].sermon.purpose` 전사 근거).
2. **`event_thrust`**: 그 분기 핵심 행사가 지향하는 체험(`weeks[].events[].serves_axes` 전사 근거).
3. **`ministry_thrust`**: 그 분기의 목표 마일스톤(어느 축 점검) + 진행 캠페인(통독·기도시즌). ← 이것이 "사역"이다.

## 방법
1. 분기별로 세 추동력을 한 줄씩 요약한다.
2. 셋이 한 방향인가? 한 방향이면 `aligned:true`, `gap:null`.
3. 어긋나면 `aligned:false` + `gap`에 무엇이 어긋나는지(예: "2Q 설교는 양육인데 핵심 행사는 전도 — 강단과 행사가 다른 곳을 봄").

## 가드레일
- **거울이지 정죄가 아니다.** 간극은 목사가 보도록 드러낼 뿐, 임의로 재배치하지 않는다(재배치는 목사 HITL).
- **방향 정합만.** 여기서는 세 추동력의 *방향*이 한지만 본다. 마일스톤 분해·담당은 action-planner(#7), 자원은 resource-aligner(#8).

## 산출
`calendar.json`의 `tri_consistency[]`(각: `quarter`·`sermon_thrust`·`event_thrust`·`ministry_thrust`·`aligned`·`gap`). 형식은 대표 스킬 `references/calendar-schema.md`. 이어 overload-marker가 밀집 주간을 비춘다.

## 흡수한 역할: season-aligner (2026-10-09 합침)

> 아래는 옛 하위 스킬 `churchplan-ministry-calendar-season-aligner`의 내용이다. 산출 필드 이름은 그대로라 스키마·검증기는 바뀌지 않는다. **이 스킬의 본래 단계(3중 정합)보다 먼저 수행한다** — 3중 정합이 `season_alignment`를 입력으로 쓴다.

### 역할 (시즌제로 힘이 모인다)
박사님 프레임워크(01 라인 265): 1Q 영성·기초 / 2Q 전도·성장 / 3Q 양육·리더 / 4Q 공동체·감사 — 같은 분기에 설교·행사·사역이 한 방향이면 "힘이 모인다". 통합 격자가 이 시즌제에 정렬되는지 점검한다.

### 입력
- `calendar.json`의 `weeks[]`(분기별 sermon·events) — **정렬 판정 결정론 근거**: `weeks[].sermon.purpose`(layer-merger가 #4 series.purpose 전사)·`weeks[].events[].serves_axes`(layer-merger가 #5 serves_axes 전사)
- `meta.season_frame`(시즌제 — sermon-plan/목사 상속, **단일 진실**)
- 시즌 모델·정렬 기준: 대표 스킬 `references/season-frame-catalog.md`

### 방법
1. **분기별 묶기**: weeks를 1Q(1~13)·2Q(14~26)·3Q(27~39)·4Q(40~52)로 묶는다.
2. **강조 추출**: 각 분기의 실제 설교 강조(`weeks[].sermon.purpose` — title 문자열 추측이 아니라 전사된 purpose)와 행사(`weeks[].events[].serves_axes`)를 요약한다. purpose/serves_axes가 격자에 없으면 layer-merger 전사 누락이므로 정렬을 단언하지 말고 앞 단계로 돌린다.
3. **정렬 점검**: 그 강조가 `season_frame[Q]`와 한 방향인가? 한 방향이면 `aligned:true`. 어긋나면 `aligned:false` + `note`(어떤 점이 어긋나는지).

### 가드레일
- **차단하지 않는다.** 어긋남은 *경고*다 — 교회 형편상 의도된 시즌 배치일 수 있다(예: 2Q에 양육). `meta.season_frame`이 진실이고, 점검은 목사의 분별을 돕는 거울이다.
- **시즌은 처방이 아니라 정렬 기준.** catalog의 1Q~4Q는 기본값이며, season_frame이 다르면 그 frame으로 점검한다.

### 산출
`calendar.json`의 `season_alignment[]`(각: `quarter`·`intended`·`actual_sermon`·`actual_events`·`aligned`·`note`). 형식은 대표 스킬 `references/calendar-schema.md`. 이어 이 스킬의 본래 단계(설교–행사–사역 3중 정합)로 간다.
