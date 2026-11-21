# 발표자료·슬라이드 (40개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/deck.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-deck && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-deck && cd /tmp/ccs-deck && git sparse-checkout set skills/airbnb-deck skills/apple-deck skills/biz-infographic-deck skills/blueprint-deck skills/bmw-m-deck skills/boneun-deck skills/claude-ppt skills/darkdoc-deck skills/dell96-deck skills/doodle-deck skills/editorial-mono-deck skills/figma-deck skills/genie-deck skills/ibm-deck 'skills/kbg-발표자료' 'skills/kbg-발표자료(1)' 'skills/kbg-발표자료(영상)' 'skills/kbg-발표자료-1' 'skills/kbg-발표자료-2' 'skills/kbg-발표자료-3' 'skills/kbg-발표자료-4' 'skills/kbg-발표자료-5' skills/linear-deck skills/monoline-deck skills/my-ppt skills/native-enhance-pptx skills/nike-deck skills/nintendo01-deck skills/notion-deck skills/ppt-maestro skills/ppt-master skills/ppt-master-v6 skills/ppt-template-fill skills/pptx-posters skills/sketch-deck skills/spotify-deck skills/starbucks-deck skills/stepwire-deck skills/stripe-deck skills/wired-deck && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [airbnb-deck](../skills/airbnb-deck) | 원고/자료를 주면 "따뜻한 소비자 마켓플레이스형 발표자료"(HTML 덱)를 자동 생성. 순백 캔버스 + Rausch 산호빛 빨강(#ff385c) 단일 브랜드 전압 + 14px 라운딩 사진 카드 그리드 + 알약형 검색바와 원형 오브 + 부드러운 그림자  | 따뜻한 소비자 마켓플레이스형 발표자료·에어비앤비 스타일·따뜻한 소비자 덱 |
| [apple-deck](../skills/apple-deck) | 원고/자료를 주면 "애플 제품 페이지형 발표자료"(HTML 덱)를 자동 생성. 밝은 타일(#fff·#f5f5f7)과 어두운 타일(#272729)을 번갈아 놓아 색 전환 자체를 구분선으로 삼고, 중앙 정렬 초대형 헤드라인(600 웨이트·음수 자간)에 액 | 애플 제품 페이지형 발표자료·애플 스타일·제품 발표 페이지 |
| [biz-infographic-deck](../skills/biz-infographic-deck) | 원고를 주면 네이비·플럼·레드·앰버 팔레트의 비즈니스 인포그래픽 PPTX를 생성. SMART 스텝 체인, 불스아이 타깃, 허브 다이어그램, 피라미드, 통계 카드, 간트 액션플랜, 2×2 매트릭스, 컬러 테이블, 다크 섹션 디바이더가 특징. 사용자가 " | 인포그래픽 덱·마케팅 플랜 PPT·비즈니스 다이어그램 발표자료 |
| [blueprint-deck](../skills/blueprint-deck) | 원고/자료를 주면 "모눈종이 블루프린트 인포그래픽 발표자료"(HTML 덱)를 자동 생성. 옅은 회백 종이(#F6F6F3) + 청회색 모눈 격자 + 도면 프레임과 치수선 + 디자인툴 선택 핸들 + 흰 카드·표·배지 + 테라코타/슬레이트/세이지 3악센트  | 모눈종이 블루프린트 인포그래픽 발표자료·블루프린트 발표자료·모눈종이 슬라이드 |
| [bmw-m-deck](../skills/bmw-m-deck) | 원고/자료를 주면 "BMW M 모터스포츠 발표자료"(HTML 덱)를 자동 생성. 순검정(#000) 배경 + 풀블리드 자동차/제품 사진 + 대문자 초굵은(700) 헤드라인 + 초가는(300) 본문의 극단 대비 + M 트라이컬러 4px 스트라이프 + 라운 | BMW M 모터스포츠 발표자료·BMW M 스타일·모터스포츠 발표자료 |
| [boneun-deck](../skills/boneun-deck) | 원고/자료를 주면 "읽지 않고 보는 PPT"(오빠두엑셀×윤춘근 직장인 PPT 디자인 강의의 원칙 전체)를 적용한 발표자료(HTML 덱→PPTX)를 자동 생성. 특정 비주얼 스타일 재현이 아니라 제작 원칙 스킬 — 문단→문장→키워드 압축, 폰트 한 가족 | 읽지 않고 보는 PPT·직장인 PPT·실무 PPT |
| [claude-ppt](../skills/claude-ppt) | > Anthropic(클로드) 톤앤매너의 투자제안서·실적발표(IR) 파워포인트 슬라이드를 만드는 스킬. 베이지 배경 + 테라코타 메인 + 카드 레이아웃 + 거버닝 메시지 + 직각 차트의 5+2 타입 모듈을 제공하고, "데이터 정교화 → 레퍼런스 등록  | 의 4단계 워크플로로 진행한다. 사용자가·, |
| [darkdoc-deck](../skills/darkdoc-deck) | 원고/자료를 주면 "다크 시네마틱 다큐멘터리 발표자료"(HTML 덱)를 자동 생성. 근사흑(#0D0E13) 배경 + 어둡게 깐 풀블리드 영상/사진 + 좌측 정보블록(악센트 점 키커·2줄 볼드 헤드라인·회색 보조문장) + 씬당 단일 악센트색(호박/블루/ | 다크 시네마틱 다큐멘터리 발표자료·다크 발표자료·시네마틱 덱 |
| [dell96-deck](../skills/dell96-deck) | 원고/자료를 주면 "1996년 카탈로그 웹 발표자료"(HTML 덱)를 자동 생성. 순백 종이 + 8px 검정 액자 프레임 + 여덟 가지 카탈로그 색(세이지·살몬·피치·라임·스카이·스틸·페리윙클·올리브) 리본카드 + Arial Black 900 대문자  | 1996년 카탈로그 웹 발표자료·Dell 1996·90년대 웹 스타일 |
| [doodle-deck](../skills/doodle-deck) | 원고/자료를 주면 "화이트보드 손그림 애니메이션 발표자료"(HTML 덱)를 자동 생성. 미색 종이 배경(#F5F3EF) + 소프트블랙 마커 선이 연필 쥔 손을 따라 그려지는 효과 + 파스텔 6색 채색 + 손글씨 글꼴(Gaegu) + 하단 알약형 자막에 | 화이트보드 손그림 애니메이션 발표자료·손그림 발표자료·화이트보드 애니메이션 |
| [editorial-mono-deck](../skills/editorial-mono-deck) | 원고를 주면 흑백 편집 매거진(에디토리얼) 스타일 PPTX를 생성. 웜 오프화이트 종이+잉크 블랙, 초대형 헤비 대문자 타이틀, 그레이스케일 사진, 넘버 서클·헤어라인 룰·메타 행이 특징. 사용자가 "에디토리얼 덱", "흑백 매거진 PPT", "잡지  | 에디토리얼 덱·흑백 매거진 PPT·잡지 스타일 발표자료 |
| [figma-deck](../skills/figma-deck) | 원고/자료를 주면 "흑백 에디토리얼 + 파스텔 컬러블록 발표자료"(HTML 덱)를 자동 생성. 순백·순흑의 엄격한 무채색 프레임에 라임·라일락·크림·민트·핑크·코랄·네이비 대형 색면(둥근 24px 블록)을 섹션마다 하나씩 끼워 넣고, 모든 CTA는 p | 흑백 에디토리얼 + 파스텔 컬러블록 발표자료·피그마 스타일·컬러블록 덱 |
| [genie-deck](../skills/genie-deck) | 원고/자료를 주면 "딥퍼플 머티리얼 컨설팅 슬라이드"(HTML 덱)를 자동 생성. 옅은 회색 캔버스(#F2F5F7) + 흰 라운드 카드 + 딥퍼플(#562EA1) 단일 악센트 + 상단 파트 브레드크럼 + 헤드라인·거버닝 메시지 컨설팅 문법 + 카드 호 | 딥퍼플 머티리얼 컨설팅 슬라이드·제미나이 바이브 코딩 프레젠테이션·딥퍼플 발표자료 |
| [ibm-deck](../skills/ibm-deck) | 원고/자료를 주면 "기업 그리드형 발표자료"(HTML 덱)를 자동 생성. IBM Carbon 디자인 시스템 재현 — 순백 캔버스 + 차콜(#161616) 타입 + IBM 블루(#0f62fe) 단일 악센트 + 모든 모서리 0px 각진 형태 + 16컬럼  | 기업 그리드형 발표자료·IBM 스타일·Carbon 디자인 |
| [kbg-발표자료](../skills/kbg-발표자료) | kbg 발표자료 선택 라우터. 유튜브 혼잡스(@honjobs) 채널 발표 영상의 화면 문법을 실측해 만든 5가지 HTML 모션 발표자료(1 클린 도식, 2 라인아트 내레이션, 3 손글씨 한 장 지도, 4 데스크톱 창 타임라인, 5 보드게임 로드맵) 가 | kbg 발표자료·kbg-발표자료·/kbg-발표자료 |
| [kbg-발표자료(1)](../skills/kbg-발표자료(1)) | kbg-발표자료(1). 코드팩토리 영상 「Laya 진짜 추천합니다」(youtu.be/ZktfWXfOwIY)의 발표 화면 스타일을 추출한 HTML 모션 덱. 오프화이트 캔버스(#F3F1E9) 위에 앱 아이콘형 다크/라이트 타일 노드, 헤어라인 연결선과  | Laya 진짜 추천합니다·kbg-발표자료(1)·kbg 발표자료(1) |
| [kbg-발표자료(영상)](../skills/kbg-발표자료(영상)) | kbg-발표자료(영상). 바이브랩스 영상 「녹음/녹화/편집/모션 그래픽까지 클로드 코드에게 완전히 맡겨봤습니다」(youtu.be/C-rzmH3571c)의 영상 제작 방식과 화면 스타일을 추출한 발표 영상 스킬. 크림 캔버스(#F2EEE7)·네이비 터미 | 녹음/녹화/편집/모션 그래픽까지 클로드 코드에게 완전히 맡겨봤습니다·kbg-발표자료(영상)·kbg 발표 영상 |
| [kbg-발표자료-1](../skills/kbg-발표자료-1) | kbg 발표자료 1 — 클린 도식형. 혼잡스(@honjobs) 개념 설명 영상의 화면 문법을 실측한 HTML 모션 덱. 순백 바탕, 검정 굵은 고딕(Pretendard 800), 검은 2.5px 테두리의 둥근 박스 도식과 화살표, 빨강·파랑 단일 강조 | kbg 발표자료 1·kbg-발표자료-1·/kbg-발표자료-1 |
| [kbg-발표자료-2](../skills/kbg-발표자료-2) | kbg 발표자료 2 — 라인아트 내레이션형. 혼잡스(@honjobs) 이야기형 영상의 화면 문법을 실측한 HTML 모션 덱. 흰 바탕에 거친 손그림 선의 인물(흰 셔츠·검은 넥타이 내레이터)·로봇·노트북·책 라인아트, 화면 위쪽 큰 자막(52px)과  | kbg 발표자료 2·kbg-발표자료-2·/kbg-발표자료-2 |
| [kbg-발표자료-3](../skills/kbg-발표자료-3) | kbg 발표자료 3 — 손글씨 한 장 지도형. 혼잡스(@honjobs) 요약 영상의 화면 문법을 실측한 HTML 모션 덱. 3600×2100 큰 종이 한 장에 손글씨(나눔펜·Gaegu) 제목과 구역을 배치하고 카메라가 구역마다 팬·줌하다 마지막에 전체 | kbg 발표자료 3·kbg-발표자료-3·/kbg-발표자료-3 |
| [kbg-발표자료-4](../skills/kbg-발표자료-4) | kbg 발표자료 4 — 데스크톱 창 타임라인형. 혼잡스(@honjobs) 회고·작업 과정 영상의 화면 문법을 실측한 HTML 모션 덱. 모눈종이 바탕, 왼쪽 앱 독(모션그래픽·음악·Ai·Notion), 오른쪽 1~12월 레일이 장면마다 켜지고, 맥 창 | kbg 발표자료 4·kbg-발표자료-4·/kbg-발표자료-4 |
| [kbg-발표자료-5](../skills/kbg-발표자료-5) | kbg 발표자료 5 — 보드게임 로드맵형. 혼잡스(@honjobs) 로드맵 영상의 화면 문법을 실측한 HTML 모션 덱. 크레용 질감 굵은 제목(Black Han Sans + 줄무늬 채움 + 7px 외곽선), 구불구불한 검정 트랙 위 색 구간·빗금·흰 | kbg 발표자료 5·kbg-발표자료-5·/kbg-발표자료-5 |
| [linear-deck](../skills/linear-deck) | 원고/자료를 주면 "딥다크 SaaS 제품 발표자료"(HTML 덱)를 자동 생성. 푸른 기가 도는 근사흑 캔버스(#010102) + surface 4단 사다리(#0f1011→#191a1b) + 라벤더블루(#5e6ad2) 악센트 하나 + 초대형 헤드라인의 | 딥다크 SaaS 제품 발표자료·다크 SaaS 덱·개발자 제품 발표 |
| [monoline-deck](../skills/monoline-deck) | 원고/자료를 주면 "흑백 라인아트 모션 발표자료"(HTML 덱)를 자동 생성. 순백 배경+잉크블랙, 프리텐다드 부분볼드 자막형 제목, 좌측 세로 스테퍼, 라인아트·목업·오프셋 그림자 박스, 순차 등장 모션. 영·한 토글(N키 한국어 패널) 변형, 강의 | 흑백 라인아트 모션 발표자료·흑백 발표자료·모노라인 덱 |
| [my-ppt](../skills/my-ppt) | > 사용자 개인 브랜딩 규칙(Pretendard 폰트, 자기 로고, 16:9, 고정 레이아웃, 밀도 있는 본문, 영어 디자인 프롬프트)을 적용하는 PPT/슬라이드 제작 스킬. 사용자가 "/my-ppt", "내 스타일로", "내 브랜딩으로", "김병곤  | /my-ppt·내 스타일로·내 브랜딩으로 |
| [native-enhance-pptx](../skills/native-enhance-pptx) | > Enhance a finished PPTX while keeping visible content and layout stable. Use for adding or replacing speaker notes, narration audio, auto-<br>완성된 PPTX를 보이는 내용과 레이아웃은 그대로 둔 채 보강한다. 직접 OOXML 편집으로 발표자 노트, 내레이션 오디오, 자동 넘김 타이밍, 슬라이드 전환을 추가하거나 교체할 때 사용. 재디자인, 원본 템플릿 채우기, SVG 생성 프로젝트 내레이션 |  |
| [nike-deck](../skills/nike-deck) | 원고/자료를 주면 "스포츠 캠페인형 발표자료"(HTML 덱)를 자동 생성. 풀블리드 편집 사진 위에 96px 대문자 푸투라 락업(행간 0.9)을 태우고, 그 아래는 검정 pill CTA와 회색 칩·여백 0 라운딩 0 제품 카드로 이루어진 중성 크롬이  | 스포츠 캠페인형 발표자료·나이키 스타일·캠페인 덱 |
| [nintendo01-deck](../skills/nintendo01-deck) | 원고/자료를 주면 "Y2K 콘솔 하드웨어형 발표자료"(HTML 덱)를 자동 생성. 2001년 Nintendo.com 재현 — 브러시드 페리윙클 금속판(#7a8aba)을 베벨(위쪽 밝은 모서리 + 크롬인디고 그림자선)로 쌓아 올리고, 카본 상단바 + 페 | Y2K 콘솔 하드웨어형 발표자료·닌텐도 2001·Y2K 스타일 |
| [notion-deck](../skills/notion-deck) | 원고/자료를 주면 "일러스트 친화형 워크스페이스 발표자료"(HTML 덱)를 자동 생성. 딥네이비(#0a1530) 히어로 밴드에 브랜드색 스티키 도트를 흩뿌리고, 흰 캔버스 위에 아홉 가지 파스텔 틴트 카드(피치·로즈·민트·라벤더·스카이·옐로)를 아낌없 | 일러스트 친화형 워크스페이스 발표자료·노션 스타일·파스텔 카드 덱 |
| [ppt-maestro](../skills/ppt-maestro) | 회사·개인 서식 기반 PPT 총괄 스킬. (1) 샘플 PDF/PPTX/이미지에서 브랜드 스펙을 추출해 일관된 PPTX를 대량 생성, (2) 기존 PPTX 템플릿의 레이아웃을 유지한 채 내용만 교체(오토필), (3) 완성된 PPTX의 수정·리페어(오탈자 | 회사 양식으로 PPT·우리 폼에 맞게·템플릿 채워줘/오토필 |
| [ppt-master](../skills/ppt-master) | > Post-router owner for authoring or regenerating presentation visuals through the PPT Master SVG pipeline: new decks from source material o<br>PPT Master SVG 파이프라인으로 발표 시각물을 작성하거나 재생성하는 라우터 이후 담당 스킬: 원자료나 주제로 새 덱 만들기, PPTX 재구성, 이미 만들어진 재사용 SVG 템플릿 작업 공간으로부터 생성, 엄격한 1:1 beautify 워크플로 |  |
| [ppt-master-v6](../skills/ppt-master-v6) | > AI-driven presentation workflow for generating editable PPTX decks and slides, reconstructing page visuals, creating reusable Brand/Style/<br>편집 가능한 PPTX 덱과 슬라이드 생성, 페이지 시각물 재구성, 재사용 가능한 Brand/Style/Layout/Deck 작업 공간 생성, 네이티브 PPTX 템플릿 채우기, 완성된 PPTX 파일 보강을 위한 AI 기반 프레젠테이션 워크플로. 사용자가 |  |
| [ppt-template-fill](../skills/ppt-template-fill) | Fill a raw PowerPoint (.pptx) template with new content by cloning and patching native slides — no SVG conversion, original design preserved<br>원본 PowerPoint(.pptx) 템플릿에 네이티브 슬라이드를 복제·패치해 새 내용을 채운다 — SVG 변환 없음, 원래 디자인 보존, 필수 OfficeCLI 넘침·렌더 루프로 검증. 사용자가 기존 .pptx 템플릿이나 덱과 함께 새 자료나 주제를 | template·use this PPT template to generate a PPTX·fill this deck with the new content |
| [pptx-posters](../skills/pptx-posters) | Creates and audits editable scientific posters in macro-free PowerPoint (.pptx) from author-approved local content and assets. Used when the<br>저자가 승인한 로컬 콘텐츠와 에셋으로 매크로 없는 PowerPoint(.pptx) 편집 가능 과학 포스터를 만들고 감사한다. 요청 산출물이 PowerPoint 연구·학회 포스터이고 정확한 물리 규격, 프린터, 접근성, 출처, 패키지 보안 점검이 필요할 |  |
| [sketch-deck](../skills/sketch-deck) | Use when the user wants a "미색 종이 + 손그림 캐릭터 + 파랑 한 색 + 하단 대형 자막" explainer deck — 감자나라ai류 유튜브 설명영상(qNQ6fGB-cWA)처럼 내레이션 한 문장마다 화면 아래 자막이 바뀌고 손 | 미색 종이 + 손그림 캐릭터 + 파랑 한 색 + 하단 대형 자막·스케치 덱·손그림 캐릭터 발표 |
| [spotify-deck](../skills/spotify-deck) | 원고/자료를 주면 "다크 몰입형 플레이어 발표자료"(HTML 덱)를 자동 생성. 근사흑 3단(#121212·#181818·#1f1f1f) 위에 아트 타일이 유일한 색을 담당하고, 스포티파이 그린(#1ed760)은 재생·활성·주 CTA에만 쓰는 기능색으 | 다크 몰입형 플레이어 발표자료·스포티파이 스타일·다크 몰입형 덱 |
| [starbucks-deck](../skills/starbucks-deck) | 원고/자료를 주면 "따뜻한 리테일 플래그십형 발표자료"(HTML 덱)를 자동 생성. 크림 캔버스(#f2f0eb·#edebe9, 순백 아님) 위에 역할이 다른 네 가지 초록(#006241 제목 · #00754A CTA · #1E3932 밴드 · #2b5 | 따뜻한 리테일 플래그십형 발표자료·스타벅스 스타일·따뜻한 크림 덱 |
| [stepwire-deck](../skills/stepwire-deck) | 원고/자료를 주면 "스텝 파이프라인 해설 발표자료"(HTML 덱)를 자동 생성. 청흑(#061017) 배경 + 상단 ①—②—③ 스텝퍼·하단 진행 점의 단계 크롬 + 재료→도구→산출 3덩어리 흐름 + 데이터 구조 다이어그램(표 크로스헤어·타일 그리드·검 | 스텝 파이프라인 해설 발표자료·스텝 발표자료·파이프라인 덱 |
| [stripe-deck](../skills/stripe-deck) | 원고/자료를 주면 "밝은 핀테크 제품 발표자료"(HTML 덱)를 자동 생성. 순백 캔버스 상단 1/3에 크림·셔벗오렌지·라벤더·인디고·루비핑크 그라디언트 메시를 깔고, 그 위에 weight 300 초박 디스플레이(음수 자간 -1.4px)와 인디고(#5 | 밝은 핀테크 제품 발표자료·스트라이프 스타일·그라디언트 메시 |
| [wired-deck](../skills/wired-deck) | 원고/자료를 주면 "테크 매거진 에디토리얼 발표자료"(HTML 덱)를 자동 생성. WIRED 지면 재현 — 흰 지면 + 순검정 잉크 + 고대비 좁은 세리프 디스플레이(항상 weight 400) + 세리프 본문 + 산세리프 내비/버튼의 3서체 체계, 모 | 테크 매거진 에디토리얼 발표자료·와이어드 스타일·매거진 발표자료 |
