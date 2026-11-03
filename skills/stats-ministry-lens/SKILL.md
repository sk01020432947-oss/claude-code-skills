---
name: stats-ministry-lens
description: '목회·사회복지·강의·지역 브리프에 국가 공식 통계를 끼워 넣는 레시피 스킬. 이미 설치된 korean-stats MCP(KOSIS, mcp.gomdori.app/stats)로 ① 설교 서론·예화용 통계 한 줄+각주 ② 교회 소재지 지역 목회 현황 브리프 ③ 통합돌봄·복지 강의 슬라이드 수치 ④ 교회 연간계획·비전 환경분석(STEEP 사회지표) ⑤ 지방의회·정책 브리프 비교표를 만든다. "설교에 넣을 통계", "출산율 예화", "우리 지역 현황", "순천 고령화", "통합돌봄 강의 수치", "교회 환경분석", "지역 비교표", "통계 각주" 요청 시 발동. 목회 맥락 없이 KOSIS 통계표 검색·수치 조회만 할 때는 kosis-stats를 쓴다.'
---

# stats-ministry-lens

데이터는 전부 `korean-stats` MCP 도구로 조회한다. 이 스킬은 순서·검증·출력 형식만 정한다. 새 코드·키 없음.

## 0. 입력 확인
- 지역(시도/시군구), 용도(설교·강의·브리프·계획), 기간(기본 10년).
- 동명 시군구(중구·남구 등)는 "부산 중구"처럼 광역명을 붙인다.

## 1. 레시피

| 용도 | 호출 순서 | 산출 |
|---|---|---|
| 설교 서론·예화 | `quick_trend(keyword)` → `explain_statistic(keyword)` | 한 문장 수치 + 변화율 + 각주 1줄. 잠정치면 "잠정" 표기 |
| 지역 목회 현황 | `quick_rank(출산율, 시군구)` → `quick_stats` 개별 지표 → (보조) `chain_region_brief(detail)` | 1쪽 브리프: 지표·기준시점·전국 순위·목회 시사점 3개 |
| 통합돌봄·복지 강의 | `chain_policy_indicator(aging\|lowFertility)` → `chain_compare_regions` | 슬라이드용 표 + 그래프용 연도별 값 |
| 연간계획·비전 환경분석 | `chain_policy_indicator` 2~3개 영역 → `churchplan-diagnostics`/`vision-foresight-environmental-scanning` 스킬로 넘김 | STEEP의 S(사회) 칸 근거 수치 |
| 의회·정책 비교표 | `chain_compare_regions(regions[], keywords[])` (+ `local-government` MCP 예산, `korean-law` 조례) | 지역×지표 매트릭스 + 비교가능성 경고 |

키워드에 없으면 `search_statistics` → `get_statistics_data`, 그래도 없으면 `kosis-stats` 스킬(원 API)로 내려간다.

## 2. 검증 규칙 (실측에서 확인된 함정 · 2026-10-04)
- **응답의 `message`·`note`를 반드시 읽는다.** `chain_region_brief(format=speech)`는 시군구가 미수록일 때 광역값(예: 전남 인구 1,779,135명)을 "순천시의 …" 문장에 섞는다. 시군구 브리프에 speech 모드 문장을 그대로 쓰지 않는다.
- 광역 대체값은 "○○시 미수록, 참고: 전남 …"으로 고쳐 쓴다.
- `trend` 라벨("안정적" 등)은 휴리스틱이다. 시작·끝 값과 변곡점을 직접 본다(예: 혼인건수 2022 저점 후 2년 반등).
- 인구동향(출생·사망·혼인·이혼) 최근 연도는 잠정치 — 설교·보도에 "잠정" 표기.
- 2026 행정구역 개편 지역명이 인식되지 않으면 종전 시도명(전남·광주)으로 조회하고 결과에 그 사실을 적는다.
- 수치는 조회 결과만 쓰고 통계표 ID와 조회일을 붙인다. 출처 없는 수치는 "예시"로 표시(CLAUDE.md 규칙 8).
- 지역 순위를 설교·광고에서 우열·낙인으로 쓰지 않는다.

## 3. 출력
- 각주 형식: `explain_statistic`의 `citation` 그대로.
- 저장: `~/Desktop/cysjavis/<주제폴더>/<한글이름>` (CLAUDE.md 규칙 4). 발표자료로 만들면 시작 전 `awesome-ai-motion` 사용 여부를 1회 묻는다.
