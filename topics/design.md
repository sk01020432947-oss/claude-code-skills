# 디자인·UI·웹 (23개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/design.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-design && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-design && cd /tmp/ccs-design && git sparse-checkout set skills/10k-websites skills/astryx skills/better-accessibility skills/better-colors skills/better-typography skills/character-style-prompts skills/clone-website skills/concept-doodle skills/concept-first-web skills/design-audit skills/design-dna skills/design-pick skills/design-taste-frontend skills/diagram-design skills/frontend-design skills/insane-design skills/kbg-infographic skills/layout-design-coach skills/palette-forge skills/scandinavian-design skills/scribble-cityscape skills/ui-ux-pro-max skills/uxui-design-system && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [10k-websites](../skills/10k-websites) | Guide a beginner from a brief and simple creative choices to a cinematic scroll-driven website, original OpenArt imagery and video, and a li<br>초보자를 간단한 브리프와 쉬운 창작 선택에서 출발시켜 영화 같은 스크롤 기반 웹사이트, OpenArt 오리지널 이미지·영상, 실제 운영되는 Hostinger 사이트까지 안내한다. Focused budget, Studio, Full throttle 세  |  |
| [astryx](../skills/astryx) | Astryx, a design system and UI library, is available on this computer through the astryx command; use it when building or changing UI, choos<br>디자인 시스템이자 UI 라이브러리인 Astryx를 이 컴퓨터에서 astryx 명령으로 쓸 수 있다. UI를 만들거나 바꿀 때, 컴포넌트·레이아웃·스타일링·테마를 고를 때, 디자인 시스템을 다룰 때, 또는 @astryxdesign 패키지에 의존하거나 A |  |
| [better-accessibility](../skills/better-accessibility) | Helps your project comply with accessibility standards and best practices. Covers native elements first, visible focus rings, full keyboard <br>프로젝트가 접근성 표준과 모범 사례를 따르도록 돕는다. 네이티브 요소 우선, 보이는 포커스 링, 완전한 키보드 지원, 포커스 트랩과 복원, 최소 터치 영역, 레이블이 달린 양식 컨트롤과 오류 안내를 다룬다. 접근성(WCAG, 키보드, 스크린 리더) 관 |  |
| [better-colors](../skills/better-colors) | Helps you build a color system and answer anything about color in your project. You can generate palettes, use semantic tokens, convert betw<br>색상 시스템을 구축하고 프로젝트의 색상에 관한 모든 질문에 답하도록 돕는다. 팔레트 생성, 시맨틱 토큰 사용, 형식 간 변환, 대비 점검 등을 할 수 있다. |  |
| [better-typography](../skills/better-typography) | Focuses on type scale, spacing, sizing, variable fonts, OpenType features, wrapping, truncation and other details that make typography feel <br>타입 스케일, 간격, 크기, 가변 폰트, OpenType 기능, 줄바꿈, 말줄임 등 제품 전반에서 타이포그래피를 훌륭하게 느끼게 하는 세부 요소에 집중한다. |  |
| [character-style-prompts](../skills/character-style-prompts) | 사진 한 장을 손그림·공작물·인쇄물·기계 출력·게임 화면 캐릭터로 바꾸는 한국어 프롬프트 110개(11시리즈×10) 아카이브. 원본 revfactory/character-comic. "사진을 ~스타일로", "캐릭터 프롬프트", "낙서/질감/변주/유행/ | 사진을 ~스타일로·캐릭터 프롬프트·낙서/질감/변주/유행/시대/기호/도해/기계/거리/무대/게임 스타일 |
| [clone-website](../skills/clone-website) | Rebuild existing web pages as working local code, matching their real content, assets, responsive layout, and interactions. Use for website <br>기존 웹페이지를 실제 콘텐츠, 에셋, 반응형 레이아웃, 상호작용까지 맞춰 동작하는 로컬 코드로 재구축한다. Framer 사이트와 애니메이션 페이지를 포함한 웹사이트 복제, 재현, 리버스 엔지니어링에 사용. |  |
| [concept-doodle](../skills/concept-doodle) | Use when the user wants a single black-ink doodle / stick-figure concept illustration that explains one topic at a glance — 흰 배경·검은 펜 손그림·졸라 | 개념 일러스트·졸라맨 그림·화이트보드 낙서 |
| [concept-first-web](../skills/concept-first-web) | 코드를 쓰기 전에 이미지 모델로 페이지 전체 시안과 움직임 참고를 먼저 만들고, 그것을 HTML/CSS로 다시 지은 뒤 스크립트로 "붙여넣지 않았는지" 검사하는 웹페이지 제작 절차. "시안 먼저", "이미지 먼저 그리고 코드로", "뻔하지 않은 랜딩페 | 붙여넣지 않았는지·시안 먼저·이미지 먼저 그리고 코드로 |
| [design-audit](../skills/design-audit) | Premium UI/UX design auditor with Jobs/Ive philosophy. Use when reviewing, evaluating, or elevating existing UI — triggers on "audit my desi<br>Jobs/Ive 철학의 프리미엄 UI/UX 디자인 감사관. 기존 UI를 검토·평가·격상할 때 사용 — '디자인 검토해줘', 'UI 리뷰', '프리미엄 느낌으로', 'UX 감사', '기능은 그대로 두고 시각 품질만 올려줘' 요청 시 발동. | audit my design·review UI·make it feel premium |
| [design-dna](../skills/design-dna) | >- 레퍼런스 디자인(포스터·스크린샷·이미지·영상 스타일 등 CSS가 없는 시각물)을 "측정 → 논쟁 → 규칙화 → 불량복제 테스트 → 규칙만으로 재현 → 누락 규칙 보강" 루프로 역설계해, 언제든 같은 스타일을 재현할 수 있는 재사용 스킬(~/.cl | 이 디자인 DNA 뽑아줘·이 포스터 스타일 스킬로 만들어줘·이 스타일 복제/재현 가능하게 |
| [design-pick](../skills/design-pick) | >- Claude로 PPT·발표자료나 웹사이트를 만들 때, AI 기본 미감(보라 그라디언트·둥근 카드·천편일률)으로 수렴하지 않도록 80가지 검증된 디자인 스타일 팩 중 하나를 골라 그 명세대로 생성하게 하는 스킬. 사용자가 "PPT/슬라이드/덱/발표 | PPT/슬라이드/덱/발표자료·웹사이트/랜딩페이지/UI·디자인 팩 |
| [design-taste-frontend](../skills/design-taste-frontend) | tasteskill v2, the anti-slop frontend skill. Art direction for websites, distilled from a study of 247 curated gallery sites (One Page Love,<br>tasteskill v2, 저품질(slop) 방지 프런트엔드 스킬. 엄선된 갤러리 사이트 247곳(One Page Love, Awwwards Sites of the Day) 연구에서 추출한 웹사이트 아트 디렉션. 라이브러리에서 연구된 방향(아이디어,  | AI-made |
| [diagram-design](../skills/diagram-design) | > Diagram design reference library (14 types — architecture, flowchart, sequence, state, ER, timeline, swimlane, quadrant, nested, tree, org<br>다이어그램 디자인 참고 라이브러리(14종 — 아키텍처, 순서도, 시퀀스, 상태, ER, 타임라인, 스윔레인, 사분면, 중첩, 트리, 조직도, 레이어, 벤, 피라미드). ppt-master에서는 Executor가 다이어그램형 SVG 페이지를 직접 작성할 |  |
| [frontend-design](../skills/frontend-design) | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typog<br>새 UI를 만들거나 기존 UI를 재구성할 때 개성 있고 의도적인 시각 디자인을 위한 지침. 미적 방향, 타이포그래피, 그리고 템플릿 기본값처럼 보이지 않는 선택을 돕는다. |  |
| [insane-design](../skills/insane-design) | URL 하나로 실제 CSS 기반 디자인 시스템 분석 — design.md + HTML 리포트 생성 인자 없이 실행하면 URL을 묻고, URL을 받으면 실제 CSS를 분석해 design.md와 report.ko.html을 만든다. 트리거: '/insan |  |
| [kbg-infographic](../skills/kbg-infographic) | kbg-인포그래픽. 설교 원고·강의 자료·논문을 학회 포스터(EMNLP식 1장 인포그래픽)로 만든다 — 질문형 큰 제목, 다크 히어로 밴드(핵심 숫자 1개+비교 막대+지표 3개+TL;DR), 번호 섹션 2단 그리드, 큰 숫자 콜아웃, 기대 vs 실제  | kbg-인포그래픽·인포그래픽 포스터로·학회 포스터처럼 |
| [layout-design-coach](../skills/layout-design-coach) | 디자이너를 위한 레이아웃·구성 가이드(시각적 움직임과 흐름 6단계, 그리드 시스템 13종, LIFT 시스템)를 기반으로 포스터·웹페이지·PPT·배너·인쇄물 등 모든 시각물의 레이아웃을 설계·진단·개선하는 코칭 스킬. 사용자가 "레이아웃 잡아줘", "구 | 레이아웃 잡아줘·구도/구성 봐줘·시선 흐름 |
| [palette-forge](../skills/palette-forge) | > 이미지·제품 사진·와디즈 등 커머스 페이지에서 브랜드/제품별 고유 컬러를 추출해 ① 팔레트 HTML 보고서(변형 4단계·대비율·CMYK·PPTX 활용 분석)와 ② 테마 색이 패치된 7슬라이드 PPTX 테마 덱을 만드는 스킬. 사용자가 "팔레트 추출 | 팔레트 추출·컬러 추출해서 정리·이 이미지 색 뽑아줘 |
| [scandinavian-design](../skills/scandinavian-design) | Apply a refined Scandinavian visual system with a neutral black-and-white foundation, restrained sans-serif typography, purposeful product i<br>중립적인 흑백 기반, 절제된 산세리프 타이포그래피, 목적 있는 제품 이미지, 넉넉한 여백, 명확한 페이지 단락, 최소한의 장식으로 이루어진 정제된 스칸디나비아 시각 체계를 적용한다. 사용자가 /scandinavian-design을 호출하거나 북유럽풍· |  |
| [scribble-cityscape](../skills/scribble-cityscape) | Use when the user wants a cityscape / street image drawn in dense chaotic scribble line art — 수천 개의 가는 선을 겹쳐 형태·명암·빛·속도를 만드는 도시 풍경(볼펜 낙서풍, 크 | 스크리블 도시·낙서풍 도시·선으로 그린 도시 |
| [ui-ux-pro-max](../skills/ui-ux-pro-max) | UI/UX design intelligence for web, mobile, and desktop. This skill should be used when designing, building, reviewing, or fixing interfaces,<br>웹, 모바일, 데스크톱용 UI/UX 디자인 인텔리전스. 페이지, 컴포넌트, 디자인 시스템, 접근성, 상호작용, 반응형 레이아웃, 타이포그래피, 색상, 차트, 스택별 UI 구현을 포함해 인터페이스를 디자인·구축·검토·수정할 때 사용. 검색 가능한 로컬  |  |
| [uxui-design-system](../skills/uxui-design-system) | Design and implement a cohesive, Toss-style (clean fintech) UX/UI design system for a web app with zero UI dependencies — token taxonomy (co<br>UI 의존성 제로로 토스 스타일(클린 핀테크) UX/UI 디자인 시스템을 설계·구현 — 토큰 체계(색·타이포·형태·엘리베이션), 컴포넌트 패턴, 반응형/다크모드/접근성 규칙, 빌드 워크플로우. 새 웹 UI 시작, 일관성 없는 UI 통일, '디자인 시스 | design system·디자인 시스템 |
