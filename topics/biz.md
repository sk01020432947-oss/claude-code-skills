# 비즈니스·재무·법무·HR (20개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/biz.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-biz && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-biz && cd /tmp/ccs-biz && git sparse-checkout set skills/agent-visa-lens skills/biz-health-check skills/contract-review-kr skills/corporate-registration-consulting skills/court-payment-order-assistant skills/expense-receipts skills/fsc-corporate-info skills/iros-registry-automation skills/jangbu-connect skills/jangbu-dash skills/jangbu-import skills/jangbu-jongso skills/jangbu-tag skills/jangbu-tax skills/korean-jangbu-for skills/korean-privacy-terms skills/notice-letter-kr skills/popbill skills/reversebusiness skills/subscription-arrears-audit && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [agent-visa-lens](../skills/agent-visa-lens) | 에이전트 커머스(대신 사고·예약하고·송금하는 AI 에이전트) 아이디어, 제품, 뉴스, 투자 건을 "신원·위임·보증" 세 축과 "마지막 클릭은 누구의 권한인가" 질문으로 진단한다. 사용자가 에이전트 결제/예약/송금/구매 대행, 플랫폼의 에이전트 차단,  | 신원·위임·보증·마지막 클릭은 누구의 권한인가·비자 렌즈로 봐줘 |
| [biz-health-check](../skills/biz-health-check) | 사업자등록번호 하나로 "이 사업자, 실제 문제 없나"를 확인한다 — 국세청 사업자등록 상태·국민연금 가입 사업장·국세 체납 명단·금융위 법인개요·조달청 부정당제재·지방행정 인허가 영업상태를 무료 공공 데이터로 교차 조회해 사실만 병렬하는 실사 리포트( | 이 사업자, 실제 문제 없나 |
| [contract-review-kr](../skills/contract-review-kr) | 한국 계약서(용역·강의 위촉·출판·임대차·협약서·MOU)를 조항별로 검토해 위험도(높음·중간·낮음) 보고서와 원본 보존형 수정 제안본을 만든다. 근거 조문은 korean-law MCP로 조회·검증한다. "계약서 검토해줘", "이 계약 괜찮아?", "불 | 계약서 검토해줘·이 계약 괜찮아?·불리한 조항 |
| [corporate-registration-consulting](../skills/corporate-registration-consulting) | 법인등기소/인터넷등기소 상업등기 신청을 처음 하는 사용자를 위해 일반 영리 주식회사 발기설립 절차, 정관·첨부서류 실제 HWP 양식 작성, 등록면허세·과밀억제권역 중과 체크, rhwp 기반 순차 검토 흐름을 참고용으로 안내한다. 돌쇠에서는 가능한 가장 |  |
| [court-payment-order-assistant](../skills/court-payment-order-assistant) | 법원 전자소송 지급명령 신청을 위해 채권자·채무자·청구금액·청구원인·증빙 정보를 인터뷰하고, 신청서 초안과 공식 전자소송 브라우저 입력 handoff를 준비한다. 돌쇠에서는 가능한 가장 가까운 합법적 공식 단계까지 준비한다. |  |
| [expense-receipts](../skills/expense-receipts) | 영수증 사진을 읽어 경비 정리표(엑셀, 분류별 원그래프 포함)를 만든다. "영수증 정리", "경비 정리표", "경비 청구", "교회 지출 정리", "부서 회계 정리" 요청이나 영수증 사진 여러 장이 올라왔을 때 사용. 원본: 혼잡스 「모조리 자동화 # | 영수증 정리·경비 정리표·경비 청구 |
| [fsc-corporate-info](../skills/fsc-corporate-info) | 금융위원회 기업기본정보(법인 개요)를 공공데이터포털 API(k-skill-proxy 경유)로 조회한다. 법인명으로 대표자·설립일·업종 등 법인 개요를 확인하고, 응답에 사업자번호가 있으면 입력 번호와 교차검증한다. |  |
| [iros-registry-automation](../skills/iros-registry-automation) | 인터넷등기소(IROS)에서 법인/부동산 등기부등본(등기사항증명서) 발급을 준비하고, 사용자가 직접 로그인·결제한 브라우저 흐름 안에서 장바구니·열람·저장을 안전하게 보조한다. 돌쇠에서는 가능한 가장 가까운 합법적 공식 단계까지 준비한다. |  |
| [jangbu-connect](../skills/jangbu-connect) | 홈택스·은행·카드사 데이터를 자동 수집하기 위한 CODEF API 자격증명 발급·설정 가이드 스킬. 사용자가 직접 CODEF(developer.codef.io)에 무료 가입해 받은 Client ID/Secret을 로컬(macOS Keychain 또는  |  |
| [jangbu-dash](../skills/jangbu-dash) | 스타트업·1인 법인 대표용 경영 리포트 자동 생성 스킬. 월별 손익 추이, 현금흐름(일별 net), cash burn rate(최근 N개월 평균 순지출), 비용 구조 분석. 공식 재무제표와 별개로 의사결정용 가공 리포트 제공. |  |
| [jangbu-import](../skills/jangbu-import) | 원본 재무 데이터(엑셀·은행 CSV·카드 내역 CSV·영수증 이미지·세금계산서 PDF·카드명세서 PDF)를 표준 거래내역 13개 필드로 변환하는 스킬. PaddleOCR 로컬 처리로 영수증·세금계산서·카드명세서에서 거래 자동 추출, Level 2 민감 |  |
| [jangbu-jongso](../skills/jangbu-jongso) | 한국 종합소득세·법인세 신고 준비를 위한 서류 체크리스트 자동 생성 스킬. 개인사업자(일반·간이·면세)·프리랜서·1인 법인·겸업·성실신고확인대상 5가지 유형별로 필요 서류 목록을 제공하고, korean-jangbu-for에서 자동 생성 가능한 항목을  |  |
| [jangbu-tag](../skills/jangbu-tag) | 표준 거래내역에 계정과목을 매핑하는 스킬. 룰 기반 분류 우선(80%+), 실패 건만 LLM fallback(마스킹 뷰), 사용자 확인 루프. 한국 거래처 100개 시드 룰 포함, 내부 계정 ↔ 국세청 표준계정 이중 구조. |  |
| [jangbu-tax](../skills/jangbu-tax) | 세무용 재무제표(재무상태표·손익계산서) 자동 생성 스킬. 국세청 표준계정과목 매핑, 일반기업회계기준(K-GAAP) 간소화 버전. 분류 완료된 거래내역을 기간 지정해 BS·PL로 집계하고 JSON·CSV 파일로 출력. |  |
| [korean-jangbu-for](../skills/korean-jangbu-for) | kimlawtech/korean-jangbu-for (Apache-2.0) 업스트림을 중심으로 한국 스타트업·1인 법인·프리랜서·개인사업자 장부 자동화와 사업자 세무 자료 정리, 원본 데이터 가져오기, 계정과목 태깅, 세무사 전달 CSV, 경영 리포트 |  |
| [korean-privacy-terms](../skills/korean-privacy-terms) | kimlawtech/korean-privacy-terms (Apache-2.0) 업스트림을 경유해 Next.js 프로젝트에 한국 법령(개인정보보호법·약관규제법·전자상거래법) 기반 개인정보처리방침·이용약관·쿠키 배너·동의 모달을 생성하는 thin wra |  |
| [notice-letter-kr](../skills/notice-letter-kr) | 대금 미지급·계약 불이행·반환 요구 거부 등에서 사실 기반 내용증명 초안, 사실확인표, 발송 전 점검표 3종을 만든다. 근거 조문은 korean-law MCP로 검증한다. "내용증명 써줘", "돈을 못 받았어", "최고서", "이행 촉구" 요청 시 발 | 내용증명 써줘·돈을 못 받았어·최고서 |
| [popbill](../skills/popbill) | 팝빌 전자세금계산서·전자명세서·현금영수증·문자·카카오톡·팩스·휴폐업/기업정보·계좌조회·홈택스 수집을 테스트/운영 환경에서 안전하게 호출한다. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한다. |  |
| [reversebusiness](../skills/reversebusiness) | 사업 웹사이트 주소 하나를 받아 그 사업을 해부한다(reversebusiness, rebiz). 사용자가 "이 사업 해부해 줘", "이 서비스 분석해 줘", "이 사업 어떻게 돈 버는지 읽어 줘", "역공학으로 비즈니스 읽기", "똑같이 만들어 줘", | 이 사업 해부해 줘·이 서비스 분석해 줘·이 사업 어떻게 돈 버는지 읽어 줘 |
| [subscription-arrears-audit](../skills/subscription-arrears-audit) | Gmail 최근 N개월(기본 3개월) 영수증·구독·결제실패 메일을 읽기 전용으로 훑어 ①새는 구독료 ②결제 실패·연체·독촉 ③무료체험 종료·갱신 예정을 표로 정리한다. "구독료 점검", "안 쓰는 구독 찾아줘", "미납·연체 확인", "결제 실패 메일 | 구독료 점검·안 쓰는 구독 찾아줘·미납·연체 확인 |
