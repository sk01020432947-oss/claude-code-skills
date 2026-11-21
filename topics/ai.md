# AI·에이전트·LLM (35개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/ai.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-ai && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-ai && cd /tmp/ccs-ai && git sparse-checkout set skills/agency-agents skills/agent-gap-router skills/agent-leadership skills/agents-md skills/aios-map skills/autoresearch-loop skills/book-to-skill skills/compact-timing skills/config-gc skills/context-budget skills/dots-delegate skills/gemini-skill-export skills/harness-evolve skills/jev-judge skills/k-skill-cleaner skills/k-skill-setup skills/kkirikkiri skills/laya-decide skills/own-the-output skills/parallel-task skills/phone-harness skills/pi-agent skills/planner skills/repeat-to-skill skills/rules-distill skills/santa-method skills/skill-comply skills/skill-finder skills/skill-install skills/skill-scout skills/skill-stocktake skills/skillers-suda skills/task-orchestrator skills/think skills/vibe-sunsang && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [agency-agents](../skills/agency-agents) | 전문가 페르소나 283명(18개 분야: 개발·마케팅·디자인·보안·테스트·영업·제품·재무·학술·GIS·게임 등, msitarzewski/agency-agents, MIT) 카탈로그에서 맞는 전문가를 골라 그 역할 문서대로 일하거나 서브에이전트에 입힌다. |  |
| [agent-gap-router](../skills/agent-gap-router) | 에이전트 작업의 네 빈틈(시키기·만들기·보고받기·확인하기)마다 이미 설치된 스킬을 골라 붙이는 라우터. 외부 5종(Ouroboros·img2threejs·UI Skills·Chisle·Reticle)의 핵심 장치만 빌려 와 설치 없이 쓴다. "빈틈 라 | 빈틈 라우터·다섯 스킬 흐름·시키기부터 확인까지 |
| [agent-leadership](../skills/agent-leadership) | ／ ## TLDR — 비즈니스 리더가 "AI를 쓰는 사람"에서 "에이전트 조직을 경영하는 사람"으로 넘어가게 하는 방법론 스킬. 강정구(라이너 AI전략 총괄) 인터뷰(티타임즈TV, 2026-08-12) 기반. 핵심 4장치: (1) AX 3축 지도 —  | AI를 쓰는 사람·에이전트 조직을 경영하는 사람·개인의 증강 → 조직의 증폭(암묵지 증류) |
| [agents-md](../skills/agents-md) | AGENTS.md 거버넌스 시스템을 분석·생성하는 마스터 프롬프트. 현재 프로젝트를 분석하여 루트 AGENTS.md와 하위 AGENTS.md를 즉시 생성하고, CLAUDE.md에 @AGENTS.md 링크를 추가한다. "AGENTS.md 만들어줘", " | AGENTS.md 만들어줘·에이전트 규칙 만들어줘·/agents-md |
| [aios-map](../skills/aios-map) | 나를 아는 AI를 만드는 맥락 지도(MAP)를 점검·보강하고, 작업마다 '관련된 맥락만' 골라 컨텍스트 팩으로 묶어 준다. Meaning(나는 누구인가)·Asset(내 지식)은 PKM 볼트의 기존 문서를 재사용하고, 비어 있는 Action(AI가 쓸  |  |
| [autoresearch-loop](../skills/autoresearch-loop) | Domain-agnostic metric-driven improvement loop, generalizing Karpathy's autoresearch. Use when you want an agent to discover what to measure<br>Karpathy의 autoresearch를 일반화한 도메인 불문 지표 기반 개선 루프. 프로젝트/목표에 대해 무엇을 측정할지 스스로 발견한 뒤, 변경 제안→측정→개선은 유지·퇴보는 되돌리는 keep-or-revert 실험 루프를 돌리고 구현된 개선을  |  |
| [book-to-skill](../skills/book-to-skill) | Converts books and documents (PDF, EPUB, DOCX, HTML, Markdown, plain text, RTF, MOBI/AZW with Calibre) into structured agent skills, extract<br>책·문서(PDF, EPUB, DOCX, HTML, Markdown, 텍스트, RTF, Calibre 경유 MOBI/AZW)를 구조화된 에이전트 스킬로 변환 — 프레임워크·멘탈모델·원칙·기법·안티패턴을 추출한다. 문서를 스킬로 학습시키거나 저자의 프레임 |  |
| [compact-timing](../skills/compact-timing) | 긴 세션에서 /clear, /compact, 새 세션 중 무엇을 언제 쓸지 정하고, /compact에 붙일 보존 지시문을 작업 유형별로 만들어 준다. "압축해도 돼?", "컨텍스트 정리", "세션 너무 길어", "컴팩트 타이밍", "여기서 끊을까" 요 | 압축해도 돼?·컨텍스트 정리·세션 너무 길어 |
| [config-gc](../skills/config-gc) | Garbage collection for your Claude Code configuration. Periodically scans ~/.claude (skills, memory, hooks, permissions, MCP servers, caches<br>Claude Code 설정 가비지 컬렉션. ~/.claude(스킬·메모리·훅·권한·MCP 서버·캐시)를 주기적으로 스캔해 중복·낡음·고아·저가치 항목을 찾고, 건별 확인을 거치는 정리 절차를 안내한다. "설정 정리해줘", "스킬이 너무 많아", "내  | clean up my config·config GC·too many skills |
| [context-budget](../skills/context-budget) | Audits Claude Code context window consumption across agents, skills, MCP servers, and rules. Identifies bloat, redundant components, and pro<br>Claude Code 컨텍스트 윈도우 소비를 에이전트·스킬·MCP 서버·규칙 단위로 감사. 비대한 항목과 중복 구성요소를 식별하고 우선순위화된 토큰 절약 권고안을 산출한다. |  |
| [dots-delegate](../skills/dots-delegate) | 에이전트(OpenAI Dots, 클로드 코드, 서브에이전트 등)에게 일을 맡기기 전 위임 브리프(결과·조건·완료 증거·사람 결정·보고·실패 시)를 만들고, 결과를 받은 뒤 '준비됨/완료'를 증거로 판정한다. 생활 에이전트(피클·Muse 등)에게 어디까 |  |
| [gemini-skill-export](../skills/gemini-skill-export) | 설치된 Claude 스킬(~/.claude/skills/<이름>)을 제미나이 앱 '스킬'(설정 > 스킬 > 업로드)에 올릴 수 있는 .zip으로 변환하고 규격을 점검한다. name 소문자-하이픈, description 1024자, 100MB, 미지원  | 제미나이 스킬로 옮겨·Gemini 스킬 업로드용으로·스킬을 폰에서도 쓰게 |
| [harness-evolve](../skills/harness-evolve) | 하네스 진화 스킬. 사용 중인 하네스의 실행 결과에 대한 피드백을 수집·일반화하여 에이전트/스킬/오케스트레이터에 반영하고, 초기 구성 대비 델타를 포착해 변경 이력을 갱신한다. '하네스 회고', '하네스 진화', '하네스 피드백 반영', '하네스 개선 |  |
| [jev-judge](../skills/jev-judge) | 클라우드 Jev(TypeSafe System One)로 많은 텍스트를 닫힌 선택지(choice·score·noul)로 빠르고 싸게 일괄 판정하고, 신뢰도 게이트로 애매한 건만 사람/Claude 검토로 넘긴다. "Jev 써서", "jev로 판정", "전 | Jev 써서·jev로 판정·전수 점검 |
| [k-skill-cleaner](../skills/k-skill-cleaner) | Interview the user and inspect coding-agent skill trigger counts to recommend unused K-skills for removal.<br>사용자를 인터뷰하고 코딩 에이전트 스킬 트리거 횟수를 조사해 사용하지 않는 K-skill의 제거를 추천한다. |  |
| [k-skill-setup](../skills/k-skill-setup) | Install the k-skill bundle, use the unified CLI, resolve credentials, verify the runtime, and optionally configure update checks and GitHub <br>k-skill 번들을 설치하고, 통합 CLI를 사용하며, 자격 증명을 해결하고, 런타임을 검증하며, 선택적으로 업데이트 확인과 GitHub 별표를 설정한다. |  |
| [kkirikkiri](../skills/kkirikkiri) | 자연어 한마디로 AI 에이전트 팀을 자동 구성하고 실행합니다. 리서치, 개발, 분석, 콘텐츠 — 목적에 맞는 팀을 만들어보세요. 흐름: 의도 파악→인터뷰→팀 생성→실행. 트리거: '끼리끼리', '/kkirikkiri', '에이전트 팀 만들어줘', '팀 |  |
| [laya-decide](../skills/laya-decide) | 로컬 무료 의사결정 모델 Laya(Jev 오픈소스 대안)로 텍스트를 빠르게 분류·라우팅·점수화한다. 메일/문서/메모/댓글 대량 분류, 폴더·태그 자동 배정, 트리아지, 프롬프트 가드, "Jev", "Laya", "빠른 분류", "라우팅", "syste | Jev·Laya·빠른 분류 |
| [own-the-output](../skills/own-the-output) | AI 결과물을 '내 것'으로 만드는 7단계 점검(Jay Choi 「AI 결과물 100배 좋아지는 7가지」·Addy Osmani 인지적 항복·이해 부채 정리). 맡기기 전 내 예상 적기·누구/금지/끝 정하기, 진행 중 실행 증거 먼저 보기, 끝난 뒤 " | AI 결과물 100배 좋아지는 7가지·네가 대신 정한 것·가정한 것·내가 놓친 것 |
| [parallel-task](../skills/parallel-task) | Coordinate plan files by launching multiple parallel subagents for unblocked tasks. Triggers on explicit "/parallel-task" commands.<br>계획 파일을 조율해 막히지 않은 작업들에 병렬 서브에이전트를 여럿 띄운다. '/parallel-task' 명시 호출로 발동. | /parallel-task |
| [phone-harness](../skills/phone-harness) | Control the user's phone - an iPhone through the Mac's iPhone Mirroring window, an Android over adb, a rented cloud Android, or a cloud iPho<br>사용자의 휴대폰을 제어한다 — Mac의 iPhone 미러링 창을 통한 iPhone, adb를 통한 Android, 대여한 클라우드 Android, HTTPS를 통한 클라우드 iPhone: 앱 열기, 탭, 입력, 스와이프, 화면 읽기. |  |
| [pi-agent](../skills/pi-agent) | Builds with and operates Pi, the minimal terminal coding harness. Use for installing Pi, configuring providers/models/settings/environment v<br>최소한의 터미널 코딩 하네스인 Pi로 개발하고 운용한다. Pi 설치, 제공자·모델·설정·환경 변수 구성, Pi 스킬·확장·패키지·테마·프롬프트 템플릿 제작, SDK로 Pi 내장, RPC나 JSON 이벤트 스트림 연동, 세션 파싱, llama.cpp 라 |  |
| [planner](../skills/planner) | Create structured plans for multi-task projects that can be used by the task-orchestrator skill. Use when breaking down complex work into pa<br>task-orchestrator 스킬이 사용할 수 있는 다중 작업 프로젝트의 구조화된 계획 수립. 복잡한 작업을 의존성 있는 병렬·순차 작업으로 분해할 때 사용. |  |
| [repeat-to-skill](../skills/repeat-to-skill) | 지난 N일 Claude Code 세션 기록(~/.claude/projects/*.jsonl)에서 내가 3번 이상 비슷하게 입력한 요청을 찾아 "스킬 후보"로 뽑고, 이미 설치된 스킬과 겹치는지 함께 보여준다. "같은 말 세 번 했으면 스킬로 빼라"는  | 스킬 후보·같은 말 세 번 했으면 스킬로 빼라·반복 요청 찾아줘 |
| [rules-distill](../skills/rules-distill) | Scan skills to extract cross-cutting principles and distill them into rules — append, revise, or create new rule files. Use when the same pr<br>스킬을 훑어 여러 스킬에 걸친 공통 원칙을 추출하고 규칙으로 증류한다. 규칙 파일에 추가·수정하거나 새로 만든다. 같은 원칙이 여러 스킬에 반복되어 규칙 파일에 두는 편이 맞을 때 사용. |  |
| [santa-method](../skills/santa-method) | Multi-agent adversarial verification: two independent reviewers with the same rubric must both pass before output ships, with a fix-and-re-r<br>다중 에이전트 적대적 검증. 같은 루브릭을 쓰는 독립 검토자 두 명이 모두 통과시켜야 산출물이 나가며, 수정 후 재검토 수렴 루프와 사람에게 넘기는 상한을 둔다. 게시, 운영 배포, 규정 준수·브랜드 민감 콘텐츠, 환각이 생기기 쉬운 주장을 내보내기  |  |
| [skill-comply](../skills/skill-comply) | Visualize whether skills, rules, and agent definitions are actually followed — auto-generates scenarios at 3 prompt strictness levels, runs <br>스킬, 규칙, 에이전트 정의가 실제로 지켜지는지 시각화한다. 3단계 프롬프트 엄격도로 시나리오를 자동 생성하고 에이전트를 실행해 행동 순서를 분류한 뒤, 전체 도구 호출 타임라인과 함께 준수율을 보고. 에이전트가 받은 스킬·규칙·정의를 실제로 따르는지 |  |
| [skill-finder](../skills/skill-finder) | 이 좌석 목록에 없는 전역 스킬 830여 개를 찾아 꺼내 쓴다. 할 일에 맞는 스킬이 목록에 없을 때 먼저 쓴다. |  |
| [skill-install](../skills/skill-install) | 깃허브 URL이나 마켓플레이스로 받은 Claude Code 스킬·플러그인을 설치하기 전에 중복 판정·보안 점검·의존성 확인을 하고, 범위(user/project/local)를 정해 설치한 뒤 작동을 확인한다. "이 스킬 설치해 줘", "깃허브 스킬 깔 | 이 스킬 설치해 줘·깃허브 스킬 깔아 줘·플러그인 추가해 줘 |
| [skill-scout](../skills/skill-scout) | Search existing local, marketplace, GitHub, and web skill sources before creating a new skill. Use when the user wants to create, build, for<br>새 스킬을 만들기 전에 로컬·마켓플레이스·GitHub·웹의 기존 스킬을 먼저 검색. 스킬을 만들거나 포크하거나 찾고 싶을 때 사용. |  |
| [skill-stocktake](../skills/skill-stocktake) | Use when auditing Claude skills and commands for quality. Supports Quick Scan (changed skills only) and Full Stocktake modes with sequential<br>Claude 스킬·명령의 품질 감사. Quick Scan(변경된 스킬만)과 Full Stocktake 모드를 지원하며 서브에이전트 순차 배치 평가로 진행. |  |
| [skillers-suda](../skills/skillers-suda) | 스킬러들의 수다 — 4명의 전문가가 수다 떨면서 바이브코더의 아이디어를 동작하는 스킬로 변환 인자 없이 실행하면 메뉴, 스킬 설명을 주면 인터뷰 후 스킬 생성, '분석 [경로]'를 주면 기존 스킬·에이전트를 분석한다. 트리거: '/skillers-su |  |
| [task-orchestrator](../skills/task-orchestrator) | Autonomous multi-agent task orchestration with dependency analysis, parallel tmux/Codex execution, and self-healing heartbeat monitoring. Us<br>의존성 분석, 병렬 tmux/Codex 실행, 자가 치유 하트비트 모니터링을 갖춘 자율 멀티에이전트 작업 오케스트레이션. 조율된 병렬 실행이 필요한 여러 이슈/작업의 대형 프로젝트에 사용. |  |
| [think](../skills/think) | Apply the Fable-derived 10-stage OBSERVE, OBSERVE, LISTEN, THINK, CONNECT, CONNECT, FEEL, ACCEPT, CREATE, GROW loop to consequential or ambi<br>Fable에서 파생된 10단계 OBSERVE, OBSERVE, LISTEN, THINK, CONNECT, CONNECT, FEEL, ACCEPT, CREATE, GROW 루프를 중대하거나 모호한 추론과 결정에 적용한다. think this throug |  |
| [vibe-sunsang](../skills/vibe-sunsang) | 바선생 — AI 활용 성장 멘토 에이전트 인자에 따라 초기 설정(onboard)·대화 로그 변환과 회고(retro)·AI 활용 코칭(mentor)·성장 리포트(growth)·개념 학습(knowledge)으로 분기한다. 트리거: '바선생', '/vibe |  |
