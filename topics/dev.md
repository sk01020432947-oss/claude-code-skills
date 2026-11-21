# 개발·자동화 (48개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/dev.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-dev && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-dev && cd /tmp/ccs-dev && git sparse-checkout set skills/agent-native-app-harness skills/appbuild skills/appbuild-orchestrate skills/appbuild-orchestrate-delegate skills/appbuild-orchestrate-route skills/appbuild-orchestrate-verify skills/appbuild-plan skills/appbuild-plan-debate skills/appbuild-plan-interview skills/appbuild-plan-quick skills/appbuild-screen-spec skills/appbuild-screen-spec-detail skills/appbuild-screen-spec-flow skills/appbuild-supervisor skills/appbuild-supervisor-collect skills/appbuild-supervisor-fix skills/appbuild-supervisor-gate skills/appbuild-supervisor-verify skills/appbuild-tasks skills/appbuild-tasks-order skills/appbuild-tasks-slice skills/aside-browser skills/context-recovery skills/context7-docs skills/docs-guide skills/ego-browser skills/fakechat-dashboard-agent skills/gemini-agents-api skills/gemini-api skills/gemini-interactions-api skills/git-teacher skills/github skills/goaljaby skills/graphify skills/harness skills/harness-engineering skills/hycli skills/hycli-recipes skills/iam-recommendations-fetcher skills/qa-inspector skills/replica-diff skills/replica-entrepreneur skills/replica-recon skills/reverse-engineer-anything skills/scrapling-adaptive skills/security-audit skills/show-me-the-prd skills/work-tool-tailor && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [agent-native-app-harness](../skills/agent-native-app-harness) | Agent Native Agent(ANA) 하네스 — 대시보드를 '보면서' 코딩 에이전트와 '대화하며' 운영하는 에이전트 네이티브 앱/에이전트를 만들고 발전시키는 스킬. '에이전트 네이티브 에이전트', 'ANA', 'ANL', '보면서 대화하는 운영  |  |
| [appbuild](../skills/appbuild) | 웹/앱을 기획→검증→자율빌드로 만드는 대표 오케스트레이터 스킬. 기획(plan)→화면명세(screen-spec)→작업목록(tasks)→★감독관 검증루프(supervisor)→게이트 통과까지 자율빌드(orchestrate)를 순서대로 굴린다. cysja |  |
| [appbuild-orchestrate](../skills/appbuild-orchestrate) | 완료 게이트를 통과할 때까지 멀티페인으로 자율 빌드하는 대표 스킬 — master가 백/프론트 페인에 위임하고 다른 페인이 E2E 증거 검증, 메인은 절대 직접 수정 않고 문제를 해당 모듈로 라우팅하는 루프. appbuild 5단계. "자율 빌드 /  |  |
| [appbuild-orchestrate-delegate](../skills/appbuild-orchestrate-delegate) | master가 빌드 작업을 백엔드·프론트엔드 페인에 위임하는 하위 스킬 — 04-tasks 슬라이스를 적합한 페인·모델에 분배하고 메인은 모니터링·조정만 한다. appbuild-orchestrate 위임 관문. "작업 위임 / 멀티페인 분배 / 백엔드 | 작업 위임 / 멀티페인 분배 / 백엔드 프론트엔드 위임 |
| [appbuild-orchestrate-route](../skills/appbuild-orchestrate-route) | 검증이 보고한 문제를 프론트/백 판별해 해당 페인에 수정 위임하는 하위 스킬 — 메인 오케스트레이터가 직접 고치지 않고 원인 모듈로 라우팅하고 재검증을 시킨다. appbuild-orchestrate 라우팅 관문. "문제 라우팅 / 수정 위임 / 프론트 | 문제 라우팅 / 수정 위임 / 프론트 백 판별 / 메인은 수정 안 함 |
| [appbuild-orchestrate-verify](../skills/appbuild-orchestrate-verify) | 만든 페인이 아닌 다른 페인이 완성물을 E2E로 직접 검증해 증거를 수집하는 하위 스킬 — 게이트 체크리스트를 들고 실행하고 문제는 고치지 말고 리포트만 한다(producer≠evaluator). appbuild-orchestrate 검증 관문. "E | E2E 검증 / 증거 검증 / 다른 페인 검증 / 체크리스트 실행 |
| [appbuild-plan](../skills/appbuild-plan) | 웹/앱 기획 산출물(01-prd·03-architecture)을 만드는 대표 스킬 — 인터뷰/디베이트/퀵 3모드로 요구·스택·데이터모델을 도출한다. appbuild 1단계(소크라테스 기획). "앱 기획 / PRD 작성 / 요구 도출 / 기획 모드" 트 | 앱 기획 / PRD 작성 / 요구 도출 / 기획 모드 |
| [appbuild-plan-debate](../skills/appbuild-plan-debate) | AI 2명(gemini·codex)이 10턴+ 스스로 토론해 웹/앱 기획을 좁히는 기획 모드 하위 스킬 — 인간 개입 없이 시장·차별점·기술 합의를 도출한다(§6 LLM 라운드 배선). appbuild-plan 모드 2. "기획 디베이트 / AI 토론 | 기획 디베이트 / AI 토론 기획 / 자동 기획 |
| [appbuild-plan-interview](../skills/appbuild-plan-interview) | 소크라테스식 인터뷰로 웹/앱 요구를 캐내는 기획 모드 하위 스킬 — 분기 질문으로 가정·모서리·완료 조건을 합의에 이를 때까지 끌어낸다(grill-me 배선). appbuild-plan 모드 1. "기획 인터뷰 / 요구 캐기 / 소크라테스 기획" 맥락 | 기획 인터뷰 / 요구 캐기 / 소크라테스 기획 |
| [appbuild-plan-quick](../skills/appbuild-plan-quick) | 질문을 최소로 해서 바로 기획 산출물을 작성하는 기획 모드 하위 스킬 — 명확한 아이디어·숙련 사용자를 위해 핵심 결정만 빠르게 확정하고 PRD·아키텍처를 즉시 만든다. appbuild-plan 모드 3. "빠른 기획 / 퀵 PRD / 질문 최소 기획 | 빠른 기획 / 퀵 PRD / 질문 최소 기획 |
| [appbuild-screen-spec](../skills/appbuild-screen-spec) | 웹/앱 화면 명세(02-screens)를 만드는 대표 스킬 — 화면 흐름·내비게이션과 화면별 상세(레이아웃·상태·컴포넌트·데이터)를 하위 스킬로 작성한다. appbuild 2단계. "화면 명세 / 스크린 스펙 / UI 명세 / 화면 설계" 트리거, 또 | 화면 명세 / 스크린 스펙 / UI 명세 / 화면 설계 |
| [appbuild-screen-spec-detail](../skills/appbuild-screen-spec-detail) | 화면별 상세(레이아웃·상태·컴포넌트·데이터)를 명세하는 하위 스킬 — 정상/빈/에러/로딩 상태를 빠짐없이, 참조 데이터를 아키텍처 모델과 일치시킨다. appbuild-screen-spec 상세 관문. "화면 상세 / 화면 상태 / 컴포넌트 명세 / 빈 | 화면 상세 / 화면 상태 / 컴포넌트 명세 / 빈 상태 에러 상태 |
| [appbuild-screen-spec-flow](../skills/appbuild-screen-spec-flow) | 화면 목록과 내비게이션/사용자 흐름(정보 구조)을 설계하는 하위 스킬 — PRD 기능을 화면에 매핑하고 화면 간 이동·진입점을 정의한다. appbuild-screen-spec 흐름 관문. "화면 흐름 / 내비게이션 / 정보구조 / 사용자 플로우" 맥락 | 화면 흐름 / 내비게이션 / 정보구조 / 사용자 플로우 |
| [appbuild-supervisor](../skills/appbuild-supervisor) | 이미 만든 기획 문서(01~04)를 다시 읽고 검증하는 대표 감독관 스킬 — 수집→13항목 검증→반자동 수정(승인 후·빠진 곳만·최대 3회)→완료 게이트 파생을 하위 스킬로 굴린다. 문서를 만드는 게 아니라 검증한다. appbuild 4단계·빌드 전  |  |
| [appbuild-supervisor-collect](../skills/appbuild-supervisor-collect) | 감독관 검증의 입력을 수집·정규화하는 하위 스킬 — 01~04 문서와 기능↔화면↔데이터↔작업 매핑·ID를 모아 검증 가능한 형태로 만든다. appbuild-supervisor 수집 관문. "기획 문서 수집 / 매핑 정규화 / 검증 입력 준비" 맥락에서 | 기획 문서 수집 / 매핑 정규화 / 검증 입력 준비 |
| [appbuild-supervisor-fix](../skills/appbuild-supervisor-fix) | 검증에서 발견된 결함을 반자동으로 교정하는 하위 스킬 — 사용자 승인을 받고, 빠진 곳만, 최대 3회 원본 스킬로 되돌려 고친 뒤 재검증한다. appbuild-supervisor 수정 관문. "반자동 수정 / 빠진 곳 교정 / 승인 후 수정 / 최대  | 반자동 수정 / 빠진 곳 교정 / 승인 후 수정 / 최대 3회 |
| [appbuild-supervisor-gate](../skills/appbuild-supervisor-gate) | 검증된 스펙에서 프로젝트별 완료 게이트(05-gate.md)를 파생하는 하위 스킬 — 기능별 수용(RTM)·전역 DoD·비기능·교차정합을 증거 기반 통과 기준으로 만든다. appbuild-supervisor 게이트 관문·빌드 종료 기준. "완료 게이트 |  |
| [appbuild-supervisor-verify](../skills/appbuild-supervisor-verify) | 기획 문서 세트를 13항목(일관성·추적성·갭·품질)으로 기계 검증하는 하위 스킬 — spec-kit analyze·RTM·INVEST·EARS 근거의 체크리스트로 교차정합·고아·누락·테스트가능성을 심각도 태깅한다. appbuild-supervisor  | 13항목 검증 / 일관성 추적성 갭 품질 / 교차 검증 / analyze |
| [appbuild-tasks](../skills/appbuild-tasks) | 기획·화면을 AI가 실제 구현할 작업목록(04-tasks)으로 분해하는 대표 스킬 — 엔드투엔드 가치 슬라이스 분해와 의존 순서·크기 산정을 하위 스킬로 만든다(to-issues 배선). appbuild 3단계. "작업 목록 / 태스크 분해 / tas | 작업 목록 / 태스크 분해 / tasks 생성 / 작업 분할 |
| [appbuild-tasks-order](../skills/appbuild-tasks-order) | 작업을 의존 순서로 정렬하고 INVEST 기준으로 크기·테스트 가능성을 다듬는 하위 스킬 — 각 작업에 수용 기준을 달아 검증 가능하게 만든다. appbuild-tasks 순서 관문. "작업 순서 / 의존 정렬 / INVEST / 수용 기준" 맥락에서 | 작업 순서 / 의존 정렬 / INVEST / 수용 기준 |
| [appbuild-tasks-slice](../skills/appbuild-tasks-slice) | 기능을 엔드투엔드 수직 슬라이스(트레이서 불릿)로 분해하는 하위 스킬 — 화면+데이터+로직이 함께 도는 데모 가능한 작업으로 자른다(수평 레이어 금지). appbuild-tasks 슬라이스 관문. "수직 슬라이스 / 트레이서 불릿 / 작업 분해" 맥락 | 수직 슬라이스 / 트레이서 불릿 / 작업 분해 |
| [aside-browser](../skills/aside-browser) | Prioritize Aside over all other browser tools for browsing, online research, website interaction, screenshots, downloads, and browser QA. Re |  |
| [context-recovery](../skills/context-recovery) | 세션 컴팩션(압축) 후 또는 문맥이 사라진 채 이어서 작업해야 할 때 작업 컨텍스트를 자동 복구. Discord, Slack, Telegram, Signal 등 지원 채널 전반에서 작동. |  |
| [context7-docs](../skills/context7-docs) | 라이브러리·프레임워크·SDK·CLI의 최신 공식 문서를 Context7 REST로 가져와 코드를 쓴다. Remotion·python-pptx·python-hwpx·Obsidian API·MCP SDK·FastMCP·Mermaid·Reveal.js·Ma | context7·최신 문서로·use context7 |
| [docs-guide](../skills/docs-guide) | 어떤 라이브러리든 공식 문서를 가져와 설명해주는 스킬. |  |
| [ego-browser](../skills/ego-browser) | When you need a browser, read this Skill by default. Use it to open and operate websites, fill forms, click buttons, take screenshots, extra |  |
| [fakechat-dashboard-agent](../skills/fakechat-dashboard-agent) | '대시보드 에이전트' 구축 — 사용자가 Claude Code 세션과 대화하면서 동시에 실시간 데이터(일정·지표·주문·대기열)를 화면으로 보는 웹 대시보드. 채팅은 fakechat 채널로 라우팅되고, Claude가 대시보드의 데이터 API를 읽어 사용자 | dashboard agent·fakechat dashboard·채팅만 말고 화면 보면서 |
| [gemini-agents-api](../skills/gemini-agents-api) | Gemini Enterprise Agent Platform의 커스텀 Agent 리소스 관리. 대화 실행 전에 서버 관리형 상태 유지 Agent 리소스를 프로그램으로 생성·설정·조회·수정·삭제(파일·스킬·도구 마운트 포함)할 때 사용. |  |
| [gemini-api](../skills/gemini-api) | 기업 환경에서 Gemini를 쓰거나 Vertex AI, Google Cloud, Agent Platform이 언급될 때 사용. Google Gen AI SDK 기반 Gemini API 사용법 안내 — SDK(Python, JS/TS, Go, Java, |  |
| [gemini-interactions-api](../skills/gemini-interactions-api) | Gemini Enterprise Agent Platform의 Interactions API 사용 안내. 멀티턴 대화, 백그라운드 실행, 스트리밍, 구조화 출력, 함수 호출을 서버 관리형 상태 유지 API로 쓰고 싶을 때 사용. |  |
| [git-teacher](../skills/git-teacher) | 바르다 깃선생 — Git/GitHub를 쉽게 도와주는 명령어 비개발자용으로 Git 설치·GitHub 연결(시작), 상태 보기, 저장(커밋), 올리기(푸시), 검토 요청(PR), 용어 도움말을 한국어로 안내한다. 트리거: '깃선생', '/git-teac |  |
| [github](../skills/github) | GitHub Desktop | GitHub,·GitHub SEO,·GitHub parasite SEO, |
| [goaljaby](../skills/goaljaby) | PRD 폴더를 받아 한국어 검토 문서 5종을 자동 생성하고, 검토 요약을 대화창에 띄운 뒤 사용자 승인을 받으면 어시스턴트가 응답 마지막 줄로 /goal을 보내 다음 턴에서 골 작업을 시작한다 (Claude Code 전용). |  |
| [graphify](../skills/graphify) | Use for any question about a codebase, its architecture, file relationships, or project content — especially when graphify-out/ exists, wher |  |
| [harness](../skills/harness) | 프로젝트에 맞는 하네스를 설계하고, 전문 에이전트와 각 에이전트가 사용할 스킬을 만든다. 사용자가 '하네스 구성해줘', '하네스 구축해줘', '하네스 설계', '하네스 엔지니어링', '에이전트 팀 만들어줘'라고 요청할 때 사용한다. 새로운 분야나 프로 |  |
| [harness-engineering](../skills/harness-engineering) | ／ ## TLDR — 하네스(AI 에이전트를 사람 개입 없이 오래 자율주행시키는 장치)를 자비스에서 운영하는 7기법 대표 스킬. 핵심 철학은 "구체화는 사람이, 구현·검증은 자율 하네스" — 개발 4단계(요구구체화→설계→구현→검증) 중 뒤 두 단계(구 | 구체화는 사람이, 구현·검증은 자율 하네스·쓸모없는 정보는 안 주고 알아야 할 것만·하네스 엔지니어링 |
| [hycli](../skills/hycli) | Prepare a website as local CLI and MCP actions, reuse its saved sign-in, and complete website tasks through Hycli. Use when a user wants to  |  |
| [hycli-recipes](../skills/hycli-recipes) | 김병곤 목사·교수의 Hycli 실행 레시피 모음. "복지 보도자료 모아줘", "블로그 임시저장", "hycli 점검", "사이트 도구로 만들어줘", "교회 홈페이지 공지", "LMS 공지 확인" 등 Hycli로 웹사이트 작업을 할 때 사용. 일반 동작 | 복지 보도자료 모아줘·블로그 임시저장·hycli 점검 |
| [iam-recommendations-fetcher](../skills/iam-recommendations-fetcher) | Google Cloud에서 지정한 범위(조직·폴더·프로젝트)의 원시 IAM 권한 추천과 보안 인사이트를 가져온다. 추천을 분석·적용하기 전 조회 용도 — 적용은 별도 스킬이 담당. |  |
| [qa-inspector](../skills/qa-inspector) | 완성된 산출물(설교 원고·강의안·보고서·HTML·공문)을 내보내기 직전에 검수한다. 요청 항목 누락, 출처 없는 수치, 존재 확인 안 된 인용·링크, 사실/추정 혼동, 개인정보 노출, 형식 규칙 위반을 찾아 PASS/FIX/BLOCK으로 판정한다. " | @qa-inspector·검수해줘·QA |
| [replica-diff](../skills/replica-diff) | >- Compares an app clone against the original: a feature parity score from the feature matrix (weighted by must, should, could) with the mis | how close is my clone·compare it to the original·what's missing |
| [replica-entrepreneur](../skills/replica-entrepreneur) | >- Researches the app being cloned and reads what its real users say in public reviews (App Store, Google Play, G2, Capterra, Trustpilot, Re | what do people hate about X·read the reviews·how do I make mine better |
| [replica-recon](../skills/replica-recon) | >- Reverse-engineers any app into a recon map: screen inventory, user flows, component list, inferred data model and a feature matrix, from  | clone this app·reverse engineer X·how does X work |
| [reverse-engineer-anything](../skills/reverse-engineer-anything) | Reverse engineer native, managed, Electron/JavaScript, packaged, firmware, and browser targets with REA, and build agent environments (Agent |  |
| [scrapling-adaptive](../skills/scrapling-adaptive) | 공개 웹페이지를 정기적으로 수집하는 스크립트에서, 사이트 개편으로 CSS 선택자가 깨져도 같은 항목을 다시 찾게 할 때 사용. "개편돼도 안 깨지는 크롤러", "공지 변경 감시", "scrapling", "적응형 선택자" 요청에 쓴다. 차단 우회용이  | 개편돼도 안 깨지는 크롤러·공지 변경 감시·scrapling |
| [security-audit](../skills/security-audit) | Security guidance and vulnerability review for codebases, APIs, services, CLI tools, libraries, and daemons. Use for security questions, foc |  |
| [show-me-the-prd](../skills/show-me-the-prd) | 인터뷰 기반 PRD 생성 -- 한 문장에서 4종 디자인 문서까지 아이디어 한 문장을 인터뷰(AskUserQuestion)로 구체화해 PRD 등 디자인 문서 4종으로 만든다. 트리거: '/show-me-the-prd', 'PRD 써줘', '앱 아이디어  |  |
| [work-tool-tailor](../skills/work-tool-tailor) | >- 검토표(적용 함/적용 안 함)로 내 상황을 먼저 받아 적은 뒤, 로그인·DB 없는 단일 HTML 업무 도구를 맞춤 제작한다. 김지백 「업무 도구 주문 사전」(nondev-thinking.web.app/tools) 방식. 트리거: "○○ 도구 주문 | 업무 도구 주문 사전·○○ 도구 주문·업무 도구 맞춤 제작 |
