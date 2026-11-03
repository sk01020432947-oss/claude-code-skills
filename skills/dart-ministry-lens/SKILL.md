---
name: dart-ministry-lens
description: '목회·총회·사회복지 연구·강의·지역 브리프에 금융감독원 전자공시(DART)를 끼워 넣는 레시피 스킬. korean-dart MCP(chrisryugj/korean-dart-mcp, 18도구)로 ① 교회 건축 시공사·협력업체 사전 실사 ② 교단 연금·기금 운용처 공시 위험 점검표 ③ 상장사 기부금·사회공헌 논문 데이터 ④ 돌봄·헬스케어 상장사 재무 읽기 강의 ⑤ 지역 기업 공시 기반 정책 브리프 ⑥ 공시+법조문 교차검증 보고서를 만든다. "시공사 재무 확인", "건설사 부도 이력", "연금재단 투자처 점검", "기부금 공시", "사회공헌 지출", "요양 상장사 재무", "여수 광양 기업 공시", "감사인 교체 법조문" 요청 시 발동. 목회 맥락 없이 공시·재무제표 원자료만 조회할 때는 k-dart를 쓴다.'
---

# dart-ministry-lens

데이터는 전부 `korean-dart` MCP 도구로 조회한다. 이 스킬은 순서·검증·출력 형식만 정한다. 새 코드·키 없음.
설명서: `~/Desktop/cysjavis/매뉴얼/KoreanDART_MCP_설명서.html`

## 0. 전제 확인
- `korean-dart` MCP 도구(`resolve_corp_code` 등)가 보이지 않으면 멈추고 설치 안내만 한다: 사용자가 직접 `npx -y korean-dart-mcp setup` 실행 + OpenDART 키 입력. 키를 채팅으로 받지 않는다.
- MCP가 없고 기본 조회만 필요하면 `k-dart` 스킬(`API_K_DART`)로 내려간다. 분석 프레임(점수·시그널)은 k-dart에 없다고 알린다.
- 입력: 회사명 목록, 기간(기본 3년), 용도.

## 1. 레시피

| 용도 | 호출 순서 | 산출 |
|---|---|---|
| 시공사·협력업체 실사 | `resolve_corp_code` → `get_financials(scope=summary)` → `disclosure_anomaly` → `search_disclosures(preset=litigation)`·`(preset=insolvency)` | 회사별 비교표(매출·영업이익·부채비율·점수·소송/회생 공시) + 접수번호 링크 |
| 연금·기금 운용처 점검 | 회사 목록마다 `disclosure_anomaly` → watch 이상만 `get_corporate_event(mode=timeline)` | 점수순 표, 비적정 감사의견 최상단, 근거 공시 3개씩 |
| 기부금·사회공헌 논문 데이터 | `search_disclosures(preset=annual_report)` → `get_xbrl(format=markdown_full)`에서 '기부금' 계정 → 없으면 `get_attachments(mode=extract)` 본문 탐색 | 회사×연도 표 + 매출 대비 비율 + "미분리" 회사 목록(표본 편향 설명용) |
| 돌봄·헬스케어 강의 | `get_financial_indicators(category=all)` → `get_attachments` '사업의 내용' 발췌 | 수익성·안정성 비교표 + 장기요양보험 의존 서술 인용 |
| 지역 기업 정책 브리프 | `search_disclosures(preset=split\|business_transfer\|merger)` → `get_company` 주소 필터 → `korean-stats`·`local-government` | 지역 기업 이벤트 연표 + 지역 통계·예산 병치 |
| 공시+법조문 교차검증 | `disclosure_anomaly` flag → `korean-law` `search_law`·`get_law_text`·`legal_analysis` | 사실(공시)·근거(조문)·인용검증 3열 표 |

드문 엔드포인트는 `dart_raw`로 직접 부른다.

## 2. 검증 규칙
- **투자 권유 금지.** 점수·시그널은 "들여다볼 이유"로만 쓰고, 사거나 팔라는 문장을 만들지 않는다. 기금 판단은 운용위원회 몫이라고 적는다.
- 모든 핵심 수치 뒤에 `rcept_no`와 원문 링크 `https://dart.fss.or.kr/dsaf001/main.do?rcpNo=<rcept_no>`를 붙인다.
- `disclosure_anomaly`가 높으면 `evidence` 공시 원문을 열어 이유(단순 오기 정정인지)를 확인한 뒤 서술한다.
- DART에 없는 회사(외감 대상 아닌 소형 비상장)는 "DART 미등재"로 표시하고 추측하지 않는다.
- 사업보고서 첨부 추출은 섹션을 지정한다(전문은 90만 자 이상 가능).
- 조회하지 않은 값은 쓰지 않는다. 통계·수치가 출처 없으면 "예시" 표기(CLAUDE.md 규칙 8).
- 특정 기업을 설교·광고에서 비난 대상으로 쓰지 않는다.

## 3. 출력
- 저장: `~/Desktop/cysjavis/<주제폴더>/<한글이름>` (CLAUDE.md 규칙 4). 발표자료로 만들면 시작 전 `awesome-ai-motion` 사용 여부를 1회 묻는다.
- 표 머리에 조회일과 기준 공시 기간을 적는다.
