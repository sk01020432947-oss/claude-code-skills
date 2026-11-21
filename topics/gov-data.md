# 공공데이터·법령·생활정보 (43개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/gov-data.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-gov-data && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-gov-data && cd /tmp/ccs-gov-data && git sparse-checkout set skills/alio skills/arch-ministry-lens skills/assembly-bill-vote-search skills/bok-ecos-stats skills/building-register-search skills/court-auction-notice-search skills/d2b-notice-search skills/dart-ministry-lens skills/g2b-bid-search skills/g2b-order-plan-search skills/g2b-sanctioned-supplier skills/hankookilbo-news skills/ip-ministry-lens skills/joseon-sillok-search skills/k-dart skills/k-schoollunch-menu skills/kakao-map skills/korean-cinema-search skills/korean-heritage-search skills/korean-law-search skills/korean-scholarship-search skills/korean-transit-route skills/kosis-stats skills/kr-api-catalog skills/kr-whois-lookup skills/kstartup-search skills/library-book-search skills/localdata-business-status skills/mfds-drug-safety skills/mfds-food-safety skills/national-assembly-tracker skills/national-pension-workplace skills/naver-blog-research skills/naver-news-search skills/naver-shopping-search skills/nhis-care-checkup-search skills/nts-business-registration skills/nts-tax-delinquency skills/pax skills/policy-brief skills/public-data-finder skills/s2b-notice-search skills/stats-ministry-lens && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [alio](../skills/alio) | ALIO 공공기관 경영정보 공개시스템(alio.go.kr)의 기관별 공시에서 공공기관별 공시 상세내용을 확인하고, k-dart처럼 기관 식별 → 공시 항목 선택 → 상세 공시 확인 → 출처 포함 요약으로 정리할 때 사용한다. 특정 공공기관의 일반현황, |  |
| [arch-ministry-lens](../skills/arch-ministry-lens) | 목회·통합돌봄·교회 건물 실사·강의·지역 브리프에 국토교통부 건축물대장 데이터를 쓰는 레시피 스킬. 이미 설치된 korean-archhub MCP(건축HUB, mcp.gomdori.app/archhub, 도구 12종)로 ① 교회 예배당 매입·임대 전  | 건물 정보·건축물대장·예배당 매입 |
| [assembly-bill-vote-search](../skills/assembly-bill-vote-search) | 열린국회정보 Open API를 k-skill-proxy 경유로 호출해 의안 검색·상세와 국회의원 본회의 표결정보를 조회한다. 조회 전용. 트리거: ''○○법 의안 검색'', ''BILL_ID 의안 상세'', ''본회의 표결 의원별 찬반''. |  |
| [bok-ecos-stats](../skills/bok-ecos-stats) | 한국은행 ECOS Open API로 기준금리, 환율, 소비자물가지수, 통화량 등 중앙은행 경제통계 시계열과 100대 핵심지표를 조회한다. Use when the user asks 기준금리, 환율 추이, 물가지수, M2, 국고채 금리, 거시경제 통계.  |  |
| [building-register-search](../skills/building-register-search) | Use when the user asks to look up a Korean building-register title record by address, PNU, legal-dong code, or parcel number. 예배당 매입 실사·통합돌봄 |  |
| [court-auction-notice-search](../skills/court-auction-notice-search) | Browse 대법원경매정보(courtauction.go.kr) 부동산 매각공고 by 매각기일·법원·기일/기간 입찰, expand each notice into 사건번호·용도·주소·감정평가액·최저매각가, search property items by fr |  |
| [d2b-notice-search](../skills/d2b-notice-search) | 국방전자조달시스템(D2B) 공개 입찰공고 검색 화면에서 공고건명·공고구분·공고/개찰일·G2B공고번호·발주기관 조건으로 공고를 조회한다. 돌쇠에서는 가능한 가장 가까운 합법적 공식 단계까지 준비한다. |  |
| [dart-ministry-lens](../skills/dart-ministry-lens) | 목회·총회·사회복지 연구·강의·지역 브리프에 금융감독원 전자공시(DART)를 끼워 넣는 레시피 스킬. korean-dart MCP(chrisryugj/korean-dart-mcp, 18도구)로 ① 교회 건축 시공사·협력업체 사전 실사 ② 교단 연금·기 | 시공사 재무 확인·건설사 부도 이력·연금재단 투자처 점검 |
| [g2b-bid-search](../skills/g2b-bid-search) | 나라장터(g2b.go.kr) 입찰공고 Open API로 용역·물품·공사 공고를 검색하고 공고명, 수요기관, 공고기관, 추정가격·배정예산, 입찰마감, 개찰일시, 계약방법, 낙찰방법, 첨부 규격서 URL, 상세 URL을 정리한다. Use when the  |  |
| [g2b-order-plan-search](../skills/g2b-order-plan-search) | 조달청 나라장터 발주계획현황서비스로 물품·공사·용역·외자 발주계획 목록을 검색한다. 돌쇠에서는 가능한 가장 가까운 합법적 공식 단계까지 준비한다. |  |
| [g2b-sanctioned-supplier](../skills/g2b-sanctioned-supplier) | 조달청 나라장터 부정당제재업체정보를 공공데이터포털 API(k-skill-proxy 경유)로 조회한다. 사업자등록번호 정확 일치로 조회시점 현재 유효한 입찰참가자격 제한(부정당제재)의 기간·제재기관·근거법률을 확인한다. |  |
| [hankookilbo-news](../skills/hankookilbo-news) | 한국일보 공식 원격 MCP 서버(mcp.hankookilbo.com)를 인증 없이 직접 호출해 편집 헤드라인·많이 본·꼼꼼히 본·최신 기사·섹션별 편집 추천·주제 검색·오늘의 운세를 기사 메타데이터(제목·발행시각·원문 링크) 중심으로 조회한다. |  |
| [ip-ministry-lens](../skills/ip-ministry-lens) | 목회·출판·사역·AI도구 개발·복지 강의에 특허청 KIPRIS 데이터를 쓰는 레시피 스킬. 이미 설치된 korean-patent MCP(mcp.gomdori.app/patent, 도구 7종)로 ① 사역·프로그램·책·채널 이름 상표 사전점검 ② 교회 굿 | 상표 있나·이름 써도 되나·책 제목 등록 |
| [joseon-sillok-search](../skills/joseon-sillok-search) | Search Joseon Dynasty Annals records from the official sillok.history.go.kr site with keyword search plus optional king/year narrowing. |  |
| [k-dart](../skills/k-dart) | 금융감독원 전자공시시스템(DART) OpenAPI로 공시검색, 기업개황, 재무제표, 주요사항보고서를 조회한다. 사용자의 API_K_DART 환경변수를 직접 사용한다. 교회 건축 시공사 실사·교단 기금 점검·기부금 공시처럼 목회 맥락 적용은 dart-m |  |
| [k-schoollunch-menu](../skills/k-schoollunch-menu) | Use when the user asks for Korean school meal menus (급식 식단) by natural-language education office and school name, via k-skill-proxy NEIS sch |  |
| [kakao-map](../skills/kakao-map) | Kakao Local (장소 검색·주소-좌표 변환) + Kakao Mobility (자동차 길찾기) 를 k-skill-proxy 경유로 조회한다. 사용자 키 불필요. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한다. |  |
| [korean-cinema-search](../skills/korean-cinema-search) | CGV, 메가박스, 롯데시네마 영화관 검색, 상영작, 시간표, 잔여석 조회가 필요할 때 사용한다. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한다. |  |
| [korean-heritage-search](../skills/korean-heritage-search) | Search official Korean national heritage records, details, locations, and monthly heritage events from the Korea Heritage Service Open API. |  |
| [korean-law-search](../skills/korean-law-search) | 한국 법령 조회는 korean-law-mcp를 우선 사용하고, 기본 서비스가 안 될 때 법망(Beopmang)으로 폴백. | OO법 제N조·판례 찾아줘·인용 맞는지 검증 |
| [korean-scholarship-search](../skills/korean-scholarship-search) | Search Korean scholarship announcements across official KOSAF, university, foundation, company, and public-sector sources, extract amount an |  |
| [korean-transit-route](../skills/korean-transit-route) | Korean door-to-door public transit routing (subway + bus + walking) via ODsay LIVE API with Kakao geocoding for address-to-address queries.  |  |
| [kosis-stats](../skills/kosis-stats) | 국가데이터처가 운영하는 KOSIS(국가통계포털, kosis.kr) Open API로 한국 공식 통계표를 검색하고 메타데이터·데이터·대용량 자료를 조회한다. Use when the user asks for 한국 공식 통계 수치 조회, 특히 공공기관·공무 |  |
| [kr-api-catalog](../skills/kr-api-catalog) | 한국에서 쓸 수 있는 공개 API·데이터 포털 300+건(yybmion/public-apis-4Kr, 로컬 클론)과 글로벌 API 780+건을 키워드로 검색해 "이 일에는 어떤 API가 있나"를 답한다. 키 없이 즉시 조회. 사용자가 "한국 API 뭐 | 이 일에는 어떤 API가 있나·한국 API 뭐 있어·이런 데이터 주는 API |
| [kr-whois-lookup](../skills/kr-whois-lookup) | 공공데이터포털 WHOIS 도메인/IP 정보 API를 k-skill-proxy 경유로 호출해 .kr/.한국 도메인, IP 주소, AS 번호의 공개 등록정보를 조회한다. 조회 전용. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한다. |  |
| [kstartup-search](../skills/kstartup-search) | 공공데이터포털 창업진흥원 K-Startup Open API(15125364)로 통합 공고 사업 정보·지원사업 공고·창업 콘텐츠·통계보고서를 k-skill-proxy 경유로 조회한다. 검색 전용. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한다. |  |
| [library-book-search](../skills/library-book-search) | Use when the user asks to search Korean library books, book details, library holdings, or whether a Korean public library owns a book via k- |  |
| [localdata-business-status](../skills/localdata-business-status) | 지방행정 인허가데이터(LOCALDATA)로 동네 사업장(식당·카페·숙박·약국·미용실·학원 등 인허가 업종 208종)의 영업/휴업/폐업 상태, 인허가일자(업력), 폐업일자, 업태, 주소를 조회한다. 상호+시군구로 검색하며 인증키 불필요. |  |
| [mfds-drug-safety](../skills/mfds-drug-safety) | 식약처 공공 OpenAPI를 k-skill-proxy 경유로 조회하기 전에 증상·복용상황을 반드시 되묻는 인터뷰형 의약품 안전 체크 스킬. e약은요 의약품개요와 안전상비의약품 정보를 조회한다. 트리거: ''이 약 효능·주의사항'', ''편의점 상비약  |  |
| [mfds-food-safety](../skills/mfds-food-safety) | 식약처/식품안전나라 공개 표면을 k-skill-proxy 경유로 조회하기 전에 증상·섭취상황을 반드시 되묻는 인터뷰형 식품 안전 체크 스킬. 건강기능식품 원료 인정·개별인정·품목신고, 검사부적합·부적합 식품, 회수·판매중지 목록을 조회한다. 트리거:  |  |
| [national-assembly-tracker](../skills/national-assembly-tracker) | 열린국회정보 Open API와 국회 공식 시스템으로 특정 키워드 관련 법률안·의안 진행상태를 검색하고 제안일, 소관위원회, 처리결과, 대표발의자, 공동발의자, 상세 의안정보 링크, 회의록·입법예고 확인 링크를 정리한다. Use when the user |  |
| [national-pension-workplace](../skills/national-pension-workplace) | 국민연금공단 국민연금 가입 사업장 내역을 공공데이터포털 API(k-skill-proxy 경유)로 조회한다. 사업장명으로 가입자수·당월 고지금액·월별 취득/상실 추이를 확인해 그 회사의 직원 규모와 변화를 본다. |  |
| [naver-blog-research](../skills/naver-blog-research) | Search Naver blogs, read full post content, and download images using only python3 stdlib — no API key required. |  |
| [naver-news-search](../skills/naver-news-search) | 네이버 검색 Open API 뉴스 검색(news.json)을 k-skill-proxy 경유로 조회해 최신 뉴스 기사 제목·발행시각·링크·요약을 보수적으로 정리한다. 사용자는 별도 API 키 발급 없이 호출한다. |  |
| [naver-shopping-search](../skills/naver-shopping-search) | 네이버 쇼핑 공개 BFF JSON을 k-skill-proxy로 조회해 상품 후보, 최저가, 판매처 링크를 보수적으로 가격비교한다. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한다. |  |
| [nhis-care-checkup-search](../skills/nhis-care-checkup-search) | 국민건강보험공단 장기요양기관·건강검진기관을 조회하고, 돌쇠에서는 공식 연락·예약 가능 표면까지 이어간다. 장기요양기관과 건강검진기관 후보(주소·전화)를 조회한다. 트리거: ''○○ 장기요양기관 찾아줘'', ''요양원 후보'', ''주말 검진 가능한 검 |  |
| [nts-business-registration](../skills/nts-business-registration) | 국세청 사업자등록정보 진위확인 및 사업자등록 상태조회를 공공데이터포털 API(k-skill-proxy 경유)로 수행한다. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한다. |  |
| [nts-tax-delinquency](../skills/nts-tax-delinquency) | 국세청 고액·상습체납자 명단공개를 nts.go.kr 공개 검색으로 조회한다. 상호·법인명으로 법인 명단과 개인 명단을 대조해 공개된 체납 사실(총 체납액·세목·체납요지 등)을 나열한다. 인증키 불필요. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한 |  |
| [pax](../skills/pax) | 공공AX 사례 아카이브(PAX, hollobit.github.io/PAX) 검색·인용. 사용자가 공공부문 AI 도입·AI전환(AX) 사례, 지자체·중앙부처·공공기관·교육청·복지·돌봄·상담 현장의 AI 활용 사례, 공무원이 만든 AI 도구·MCP, AX |  |
| [policy-brief](../skills/policy-brief) | 정책 주제 하나를 받아 KOSIS 통계 추세 + 근거 법령 조문 + 인용 검증을 엮은 정책 브리프(마크다운·HWPX)를 만든다. "OO 정책 브리프", "OO 정책 현황 보고서", "OO 통계랑 법적 근거 정리해줘", 사회복지정책론 원고용 정책 요약이 | OO 정책 브리프·OO 정책 현황 보고서·OO 통계랑 법적 근거 정리해줘 |
| [public-data-finder](../skills/public-data-finder) | 공공데이터포털(data.go.kr) 목록개방현황 API로 공공기관이 개방한 파일데이터·오픈API·표준데이터를 키워드, 제공기관, 분류체계 기준으로 검색하고 목록유형, API 유형, 갱신주기, 조회수, 목록 URL, 설명을 출처와 함께 정리한다. Use |  |
| [s2b-notice-search](../skills/s2b-notice-search) | S2B 학교장터 공개 고객 공고/견적요청 목록을 브라우저 우선으로 조회하고 fixture HTML을 파싱해 공고 메타데이터를 정리한다. 돌쇠에서는 가능한 가장 가까운 합법적 공식 단계까지 준비한다. |  |
| [stats-ministry-lens](../skills/stats-ministry-lens) | 목회·사회복지·강의·지역 브리프에 국가 공식 통계를 끼워 넣는 레시피 스킬. 이미 설치된 korean-stats MCP(KOSIS, mcp.gomdori.app/stats)로 ① 설교 서론·예화용 통계 한 줄+각주 ② 교회 소재지 지역 목회 현황 브리 | 설교에 넣을 통계·출산율 예화·우리 지역 현황 |
