---
name: kr-api-catalog
description: 한국에서 쓸 수 있는 공개 API·데이터 포털 300+건(yybmion/public-apis-4Kr, 로컬 클론)과 글로벌 API 780+건을 키워드로 검색해 "이 일에는 어떤 API가 있나"를 답한다. 키 없이 즉시 조회. 사용자가 "한국 API 뭐 있어", "이런 데이터 주는 API", "공공/민간 API 목록", "public-apis-4Kr"을 말할 때, 또는 새 스킬·앱 설계 전에 데이터 소스 후보를 고를 때 사용. 실제 데이터 호출은 전용 스킬(kosis-stats·korea-weather·kakao-map 등 k-skill 계열)이나 public-data-finder로 넘긴다.
---

# kr-api-catalog

로컬 클론 `/Users/kbg1023/DEV/public-apis-4Kr`의 목록을 검색하는 **카탈로그 조회** 스킬. 데이터를 직접 호출하지 않는다.

## 명령

```bash
python3 ~/.claude/skills/kr-api-catalog/lookup.py 복지 노인        # AND 키워드(이름·설명·카테고리)
python3 ~/.claude/skills/kr-api-catalog/lookup.py --cat            # 카테고리 37개 목록
python3 ~/.claude/skills/kr-api-catalog/lookup.py --cat 통계       # 한 카테고리 전체
python3 ~/.claude/skills/kr-api-catalog/lookup.py --global weather # 글로벌 목록
python3 ~/.claude/skills/kr-api-catalog/lookup.py --update         # git pull + 인덱스 재생성
```

## 답변 규칙

1. 결과는 `이름 [인증] — 설명 / URL` 그대로 인용하고, 인증 종류(`apiKey`·`OAuth`·`Login`·`✕`=별도 절차 없음)를 반드시 밝힌다.
2. 후보가 나오면 **이미 설치된 전용 스킬이 있는지** 먼저 짚는다. 대표 매핑:
   - 기상청 단기예보 → `korea-weather` / 에어코리아 → `fine-dust-location`
   - KOSIS → `kosis-stats` / 한국은행 ECOS → `bok-ecos-stats` / DART → `k-dart`
   - 카카오맵·모빌리티 → `kakao-map`, `korean-transit-route` / 나라장터 → `g2b-bid-search`
   - 열린국회 → `national-assembly-tracker`, `assembly-bill-vote-search` / KIPRIS → `korean-patent-search`
   - 국세청 사업자 → `nts-business-registration` / 실거래가 → `real-estate-search` / LH → `lh-notice-search`
   - 법제처 → `korean-law-search`(korean-law MCP) / 공공데이터포털 목록 검색 → `public-data-finder`, `public-data-lens` MCP
3. 전용 스킬이 없으면 URL의 활용신청 절차(공공데이터포털은 로그인 → 활용신청 → 서비스키, 보통 즉시 승인)를 안내하고, 키는 환경변수로 받는다. 키 값을 대화에 적지 않는다.
4. 목록 갱신일은 README 하단 "마지막 업데이트"에서 읽어 함께 말한다. 링크 사망 여부는 `reports/` 최신 JSON의 `is_working`으로 확인할 수 있다.
