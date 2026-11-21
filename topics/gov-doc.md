# 오피스·한글(HWP)·공공문서 (27개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/gov-doc.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-gov-doc && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-gov-doc && cd /tmp/ccs-gov-doc && git sparse-checkout set skills/elegant-reports skills/genie-report skills/gongik-seosik skills/gov-meeting-minutes skills/gov-overseas-trip-report skills/haengbok-case-record skills/hop-desktop skills/hwpx skills/hwpx-gongmun-standardizer skills/hwpx-mouseco skills/hwpxskill skills/ieumoffice 'skills/kbg-문서양식(1)' skills/korean-doc-corpus skills/liteparse skills/markitdown skills/new-hwpx-master-v5-1-20260720 skills/nudocs skills/nutrient-openclaw skills/officecli skills/official-report-skillset skills/read-hwp skills/reporting-guideline-router skills/rhwp-advanced skills/rhwp-edit skills/sungahna-foundation skills/transport-receipt-collector && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [elegant-reports](../skills/elegant-reports) | 북유럽 감성의 아름다운 PDF 보고서 생성. 마크다운·HTML로부터 Nutrient DWS를 거쳐 세련된 경영진 브리핑, 분석 보고서, 프레젠테이션형 PDF를 만들 때 사용. |  |
| [genie-report](../skills/genie-report) | 원고/자료를 주면 "그레이스케일 A4 세로 보고서"를 HTML과 편집 가능한 PPTX 두 형식으로 생성. 텍스트가 많고 복잡한 보고서·제안서 전용 — A4 210×297mm 페이지 구분 + 헤더(제목·쪽번호)/푸터 + 프리텐다드 + 무채색 그레이스케일 | 그레이스케일 A4 세로 보고서·AI 보고서·제안서 PPTX 작성 워크플로우·A4 보고서 |
| [gongik-seosik](../skills/gongik-seosik) | 서울특별시교육청 「2026 공익법인 실무지침서」 기반 공익법인 행정서식 작성 스킬. 사용자가 제공한 법인 정보·메모·회의 내용을 지침서의 공식 서식에 맞게 정리해 완성본을 만든다. 법인설립허가, 해산·청산, 기본재산 처분/담보·장기차입/기부금사용승인/ | 2026 공익법인 실무지침서·공익법인 서식·설립허가 신청서 |
| [gov-meeting-minutes](../skills/gov-meeting-minutes) | 공공기관 회의 메모, 녹취록, ClovaNote 전사, 참석자 발언 기록을 바탕으로 담백한 공문서형 회의록 PDF를 만들 때 사용한다. 1쪽에는 회의록 요약본을, 2쪽 이후에는 시간순 상세 발언록을 배치하며, 익명 발언자는 사용자에게 이름·직함을 확인 |  |
| [gov-overseas-trip-report](../skills/gov-overseas-trip-report) | 선관위·권익위·정보공개포털·주요 지방의회 등 검증된 공개 표면에서 공무국외출장/국외훈련 보고서·현황을 조회하고, 첨부 원문이 있으면 kordoc으로 사실·공개성·검토 신호만 구조화한다. 부정부패 판정 도구가 아니다. |  |
| [haengbok-case-record](../skills/haengbok-case-record) | 공공 통합사례관리(행복이음·사회보장정보시스템) 상담일지·사례기록을 복지부 업무안내 기준으로 작성·검토·분석한다. 상담 녹취·메모를 행복이음 입력용 상담일지로 정리할 때, 초기상담지·욕구조사표·위기도 조사지·서비스 제공계획·모니터 상담지 항목을 채우거나 |  |
| [hop-desktop](../skills/hop-desktop) | HOP(golbin/hop, 오픈소스 HWP/HWPX 데스크톱 앱)로 한글 문서를 사람 눈으로 열람·확인·PDF 내보내기 할 때 사용. "HOP로 열어줘", "hwp 미리보기", "만든 hwpx 화면으로 확인", "Finder에서 hwp 썸네일", " | HOP로 열어줘·hwp 미리보기·만든 hwpx 화면으로 확인 |
| [hwpx](../skills/hwpx) | 한글 HWP/HWPX 파일의 변환·읽기·편집과 편집 가능한 .hwpx 문서 생성. 한글 파일, HWP 변환, HWPX 공문·보고서·계획서·활동지, 기존 한글 양식 채우기 요청에 사용한다. |  |
| [hwpx-gongmun-standardizer](../skills/hwpx-gongmun-standardizer) | 우석진 「클로드.ai 공공기관 아래한글 .hwpx 공문서 표준화 생성 반자동화 워크플로우」 방법론. 기관의 기존 공문·보고서 2~3건(PDF)을 역추출해 "글쓰기 마스터 프롬프트.md"(무엇을 어떤 순서·문체로 쓸지)를 만들고, HWPX+PDF 쌍을  | 글쓰기 마스터 프롬프트.md·HWPX 템플릿 스킬·공문 표준화 |
| [hwpx-mouseco](../skills/hwpx-mouseco) | 한국 공공문서용 HWPX(.hwpx) 보고서 양식을 분석·작성·검증할 때 사용한다. 공개 배포용 원페이퍼, 다중페이퍼, 장문 보고서 프로파일과 템플릿을 기준으로 report JSON을 만들고, HWPX 내부 XML을 보존하면서 문서를 생성한다. 레거시 |  |
| [hwpxskill](../skills/hwpxskill) | 한글 HWPX 문서 생성/읽기/편집 스킬. .hwpx 파일, Hancom, OWPML 관련 요청 시 사용. .hwp 바이너리 파일 작성/생성/직접 편집 요청은 거부한다. |  |
| [ieumoffice](../skills/ieumoffice) | Create, convert, read and edit Office documents locally with IeumOffice's command line: build pptx decks (checked outline, per-page spec, re |  |
| [kbg-문서양식(1)](../skills/kbg-문서양식(1)) | kbg-문서양식(1). 「한 장으로 읽는 가톨릭 성경 73권」 판매 페이지(gatollik-seonggyeong73.impultienda.ar, 2026-11-18 열람)에 실린 견본 PDF의 문서 양식을 추출한 A4 한 장 정리 시트. 둥근 테마색  | 한 장으로 읽는 가톨릭 성경 73권·kbg-문서양식(1)·kbg 문서양식(1) |
| [korean-doc-corpus](../skills/korean-doc-corpus) | > 한국 공공문서(PDF·HWP·HWPX·DOCX)를 AI가 읽을 수 있는 **하나의 구조화 마크다운 코퍼스**로 수렴시킬 때 사용한다. 핵심 3가지 — ①포맷 판별 후 적절한 도구로 라우팅 ②**스캔 PDF의 OCR 깨짐 글자 보정**(사전+정규식+ |  |
| [liteparse](../skills/liteparse) | Local document and PDF parsing that returns spatial text with bounding boxes. Use for extracting text from PDFs, DOCX, Office files, and ima |  |
| [markitdown](../skills/markitdown) | Converts heterogeneous documents and selected URIs to Markdown with Microsoft MarkItDown for text analysis, search, and LLM/RAG ingestion. C |  |
| [new-hwpx-master-v5-1-20260720](../skills/new-hwpx-master-v5-1-20260720) | hwpx 공문/기안문 양식을 첨부하면 주제에 맞춰 공문 내용을 자동 작성. 작성 전 반드시 사용자에게 ①목표 분량(페이지 수) ②문체(개조식/서술식) ③내용 중점 방향을 3단계로 질문·확정한 뒤, 확정값에 근사하게 본문을 설계·검증한다 (v5.1, 2 |  |
| [nudocs](../skills/nudocs) | Nudocs.ai로 문서 업로드·편집·내보내기. 협업 편집용 공유 문서 링크 생성, 마크다운 업로드, 편집된 내용 회수 시 사용. | send to nudocs·upload to nudocs·edit in nudocs |
| [nutrient-openclaw](../skills/nutrient-openclaw) | Nutrient DWS용 OpenClaw 네이티브 문서 처리 스킬. 파일 변환, 텍스트·표 추출, 스캔 OCR, 개인정보 마스킹, PDF 워터마크, 전자서명, 크레딧 사용량 확인. | OpenClaw plugin·Nutrient OpenClaw |
| [officecli](../skills/officecli) | officecli CLI 도구로 Office 문서(.docx, .xlsx, .pptx)를 생성·분석·교정·수정. 문서 생성, 검사, 서식 확인, 문제 찾기, 차트 추가, 수정 요청 시 사용. |  |
| [official-report-skillset](../skills/official-report-skillset) | 공공기관 보고서, 결과보고, 계획보고, 검토보고, 회의결과 보고, 공문서 초안 작성에 사용하는 스킬. 사용자가 메모, 개요, 추진 경과, 계약 내용, 수요조사, 운영계획, 배분안, 붙임 자료 등을 주고 공공기관 결재문서 형태로 정리해 달라고 할 때 사 |  |
| [read-hwp](../skills/read-hwp) | HWP/HWPX 문서의 에이전트 네이티브 파싱은 kordoc 사용 — JSON 추출, 문서 비교(diff), 서식 필드 추출, 마크다운→HWPX 역변환. 읽기/변환 전용 — 바이너리 편집은 rhwp-edit 사용. |  |
| [reporting-guideline-router](../skills/reporting-guideline-router) | 논문 투고 직전, reporting guideline(CONSORT·STROBE·PRISMA·SRQR·COREQ·TRIPOD+AI 등)을 '유명한 checklist 고르기'가 아니라 '연구 설계와 보고 항목의 대응 증명'으로 선택하게 하는 라우팅 스킬 | reporting guideline 골라줘\·어떤 체크리스트 써야 해\·CONSORT/STROBE/PRISMA 맞나\ |
| [rhwp-advanced](../skills/rhwp-advanced) | Debug HWP layout, dump document IR, compare versions, extract thumbnails, and unlock read-only HWPs with the upstream rhwp Rust CLI (export- |  |
| [rhwp-edit](../skills/rhwp-edit) | Edit HWP documents — insert/delete text, replace-all, create tables, set cell text — with the k-skill-rhwp CLI that wraps the @rhwp/core WAS |  |
| [sungahna-foundation](../skills/sungahna-foundation) | (재)성안나장학재단(재단법인, 서울특별시교육청 평생교육과 관할 공익법인) 실무 문서를 작성할 때 사용한다. 이사회 회의록, 사업계획서·예산서, 사업실적·결산서, 정관변경, 예결산보고, 재산목록, 감사서, 임원현황 등 서울특별시교육청 소관 비영리법인이  | 2026 공익법인 실무지침서·장학재단·성안나 |
| [transport-receipt-collector](../skills/transport-receipt-collector) | 공공기관 출장·여비·교통비 정산에 필요한 하이패스, 코레일, SRT 영수증을 공식 사이트 또는 승인된 제공자 경로에서 수집하고 PDF와 PNG 증빙 파일로 정리할 때 사용한다. |  |
