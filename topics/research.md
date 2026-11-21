# 리서치·심층조사 (17개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/research.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-research && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-research && cd /tmp/ccs-research && git sparse-checkout set skills/agent-reach skills/autoresearch skills/consciousness-council skills/council skills/daily-radar-magazine skills/deep-interview skills/deep-research skills/deep-research-pro skills/exa-search skills/geeknews-search skills/grill-me skills/insane-search skills/last30days skills/market-research-reports skills/parallel-web skills/research-sources skills/what-if-oracle && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [agent-reach](../skills/agent-reach) | > MUST USE when user wants to 调研/research/搜索/search/查/找/look up anything on the internet — e.g. 全网调研 X / 帮我调研一下 X / 查一下 X / 搜搜 X / 看看大家怎么评价 <br>인터넷에서 무언가를 조사·검색해야 할 때 사용하는 스킬. 특정 플랫폼(샤오홍슈, 트위터/X, 빌리빌리, Reddit, Facebook, Instagram, V2EX, LinkedIn, YouTube, GitHub 코드검색, 팟캐스트, 주식 시세, RS |  |
| [autoresearch](../skills/autoresearch) | Run a bounded, source-grounded research loop, draft a cited dossier, and optionally propose a separately reviewed canonical vault merge. Use<br>범위가 정해진 출처 기반 조사 루프를 실행해 인용이 달린 자료집을 작성하고, 선택적으로 별도 검토를 거치는 정본 볼트 병합을 제안한다. 사용자가 공개 웹에 접근할 수 있는 자율 조사나 심층 조사를 원할 때 사용. 트리거: /autoresearch, a |  |
| [consciousness-council](../skills/consciousness-council) | Structures a multi-perspective council exercise for decisions, research trade-offs, and creative challenges. Simulates thinking archetypes, <br>의사결정, 연구상의 트레이드오프, 창의적 과제를 위한 다관점 위원회 연습을 구성한다. 사고 원형들을 시뮬레이션하고, 근거와 가정·가치를 구분하며, 조건부 권고안을 종합한다. 사용자가 위원회, 패널, 반대 논거(devil's advocate) 분석, " | mind council |
| [council](../skills/council) | Convene the Council of High Intelligence — multi-persona deliberation with historical thinkers for deeper analysis of complex problems.<br>지성 위원회 소집 — 역사적 사상가들의 다중 페르소나 숙의로 복잡한 문제를 더 깊이 분석. |  |
| [daily-radar-magazine](../skills/daily-radar-magazine) | 관심 대상(브랜드·조례/입법예고·정책·교계 소식·학술지·시세)을 매일 정해진 시각에 자동 조사하고, 공식 출처로 교차 확인한 뒤 '오늘의 매거진' HTML 한 장으로 묶어 같은 아티팩트 URL에 갱신 발행하는 레시피. "매일 아침 9시에 ~ 모아서 알 | 매일 아침 9시에 ~ 모아서 알려줘·신제품/새 조례/입법예고 레이더·모니터링 결과를 매거진 웹으로 |
| [deep-interview](../skills/deep-interview) | ／ 모호한 요청을 소크라테스식 질문으로 인터뷰해 실행 가능한 요구사항으로 정리한다. 사용자가 deep-interview, 심층 인터뷰, 요구사항 명확화, 생각 정리를 요청하거나 목표, 범위, 제약, 완료 기준이 흐릿할 때 사용한다. 요청이 이미 구체적 |  |
| [deep-research](../skills/deep-research) | AI 딥리서치 -- 멀티에이전트 기반 종합 리서치 시스템 주제를 받아 범위 설정→멀티에이전트 검색→출처 검증→종합 보고서로 진행하고, resume·status로 이전 리서치 세션을 이어 간다. 트리거: '딥리서치', '깊게 조사해줘', '종합 리서치' |  |
| [deep-research-pro](../skills/deep-research-pro) | 출처 있는 심층조사와 판단 브리프가 필요할 때 사용하는 OpenClaw 맞춤 리서치 스킬. 단순 검색 답변이 아니라 정책·시장·기업·기술·제도·문헌·공공기관 보고서 근거를 여러 출처로 교차확인하고, 출처 등급·첨부 PDF 확인·반대검토·합의점/쟁점·의 |  |
| [exa-search](../skills/exa-search) | Searches scientific and technical web content with Exa and extracts page or PDF text from URLs in batches. Supports scholarly discovery with<br>Exa로 과학·기술 웹 콘텐츠를 검색하고 URL에서 페이지나 PDF 텍스트를 일괄 추출한다. 출판물 카테고리와 학술 도메인 필터로 학술 자료 탐색을 지원한다. Exa로 웹 검색, 최신 연구 조회, 페이지 가져오기, 기사 추출을 요청할 때 적용. |  |
| [geeknews-search](../skills/geeknews-search) | GeekNews public RSS/Atom feed로 긱뉴스 게시물을 조회, 검색, 상세 확인하는 읽기 전용 스킬. 공개 RSS 피드로 최신 글 목록·키워드 검색·항목 상세를 읽기 전용으로 조회한다. 트리거: ''긱뉴스 오늘 뭐 올라왔어'', ''긱 |  |
| [grill-me](../skills/grill-me) | 지시·계획의 의도 파악이 불충분할 때 합의에 이를 때까지 구조화 질문을 반복하는 의도 합의 스킬(work management 앵커 c). "의도 확인 / 의도 합의 / grill me / 계획 검증 질문 / 뭘 원하는지 모르겠다" 트리거로 발동 |  |
| [insane-search](../skills/insane-search) | > Auto-bypass for blocked websites — tries every method until one works. Use when WebFetch returns 402/403/blocked, or when accessing X/Twit<br>차단된 웹사이트 적응형 접근 — 되는 방법이 나올 때까지 모든 수단을 시도. WebFetch가 402/403/차단될 때, X/Twitter·Reddit·YouTube·GitHub·Medium·Substack·네이버·쿠팡·LinkedIn 등 WAF/봇  |  |
| [last30days](../skills/last30days) | Research any topic from the last 30 days on Reddit + X + Web, synthesize findings, and write copy-paste-ready prompts. Use when the user wan<br>최근 30일의 Reddit + X + 웹에서 어떤 주제든 조사해 종합하고, 복붙 가능한 프롬프트로 정리. '요즘 사람들이 X에 대해 뭐라고 해?', 최신 모범 사례 학습 요청 시 사용. 전체 기능엔 OPENAI_API_KEY/XAI_API_KEY 필요 | what are people saying about X |
| [market-research-reports](../skills/market-research-reports) | Builds evidence-traceable market research reports and assumption-driven market sizing or forecast scenarios. Use for market definition, indu<br>근거를 추적할 수 있는 시장 조사 보고서와 가정 기반 시장 규모 산정·전망 시나리오를 만든다. 시장 정의, 산업·고객 근거, 경쟁 구도, TAM/SAM/SOM 조정, 전망 민감도, 감사 가능한 보고서 골격에 사용. |  |
| [parallel-web](../skills/parallel-web) | Uses Parallel CLI for web search, URL extraction, deep research, structured data enrichment, entity discovery, and recurring web monitoring.<br>Parallel CLI로 웹 검색, URL 추출, 심층 리서치, 구조화 데이터 보강, 개체 발견, 반복 웹 모니터링을 수행한다. 최신 웹 근거, 학술 출처 발견, 반복 개체 조회, 망라적 보고서, 지속적 변경 추적이 명시적으로 필요한 요청에 가장 적합 |  |
| [research-sources](../skills/research-sources) | When the user wants to find information sources for content ideation, competitor monitoring, or industry tracking. Also use when the user me<br>콘텐츠 아이디어 발굴, 경쟁사 모니터링, 업계 동향 추적을 위한 정보원을 찾으려 할 때 사용. "research sources," "information sources," "content ideation," "industry monitoring," " | research sources,·information sources,·content ideation, |
| [what-if-oracle](../skills/what-if-oracle) | Supports structured what-if scenario analysis for research planning, experimental contingencies, and scientific project decisions. Explores <br>연구 계획, 실험 비상 대책, 과학 프로젝트 결정을 위한 구조화된 가정(what-if) 시나리오 분석을 지원한다. 명시적 가정·증거·결정 트리거와 함께 유리, 기준, 불리, 와일드카드, 역발상, 2차 시나리오를 탐색. 불확실성 아래에서 연구 계획을 스 |  |
