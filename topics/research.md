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
| [agent-reach](../skills/agent-reach) | 인터넷에서 무언가를 조사·검색해야 할 때 사용하는 스킬. 특정 플랫폼(샤오홍슈, 트위터/X, 빌리빌리, Reddit, Facebook, Instagram, V2EX, LinkedIn, YouTube, GitHub 코드검색, 팟캐스트, 주식 시세, RS |  |
| [autoresearch](../skills/autoresearch) | Run a bounded, source-grounded research loop, draft a cited dossier, and optionally propose a separately reviewed canonical vault merge. Use |  |
| [consciousness-council](../skills/consciousness-council) | Structures a multi-perspective council exercise for decisions, research trade-offs, and creative challenges. Simulates thinking archetypes,  | mind council |
| [council](../skills/council) | 지성 위원회 소집 — 역사적 사상가들의 다중 페르소나 숙의로 복잡한 문제를 더 깊이 분석. |  |
| [daily-radar-magazine](../skills/daily-radar-magazine) | 관심 대상(브랜드·조례/입법예고·정책·교계 소식·학술지·시세)을 매일 정해진 시각에 자동 조사하고, 공식 출처로 교차 확인한 뒤 '오늘의 매거진' HTML 한 장으로 묶어 같은 아티팩트 URL에 갱신 발행하는 레시피. "매일 아침 9시에 ~ 모아서 알 | 매일 아침 9시에 ~ 모아서 알려줘·신제품/새 조례/입법예고 레이더·모니터링 결과를 매거진 웹으로 |
| [deep-interview](../skills/deep-interview) | ／ 모호한 요청을 소크라테스식 질문으로 인터뷰해 실행 가능한 요구사항으로 정리한다. 사용자가 deep-interview, 심층 인터뷰, 요구사항 명확화, 생각 정리를 요청하거나 목표, 범위, 제약, 완료 기준이 흐릿할 때 사용한다. 요청이 이미 구체적 |  |
| [deep-research](../skills/deep-research) | AI 딥리서치 -- 멀티에이전트 기반 종합 리서치 시스템 주제를 받아 범위 설정→멀티에이전트 검색→출처 검증→종합 보고서로 진행하고, resume·status로 이전 리서치 세션을 이어 간다. 트리거: '딥리서치', '깊게 조사해줘', '종합 리서치' |  |
| [deep-research-pro](../skills/deep-research-pro) | 출처 있는 심층조사와 판단 브리프가 필요할 때 사용하는 OpenClaw 맞춤 리서치 스킬. 단순 검색 답변이 아니라 정책·시장·기업·기술·제도·문헌·공공기관 보고서 근거를 여러 출처로 교차확인하고, 출처 등급·첨부 PDF 확인·반대검토·합의점/쟁점·의 |  |
| [exa-search](../skills/exa-search) | Searches scientific and technical web content with Exa and extracts page or PDF text from URLs in batches. Supports scholarly discovery with |  |
| [geeknews-search](../skills/geeknews-search) | GeekNews public RSS/Atom feed로 긱뉴스 게시물을 조회, 검색, 상세 확인하는 읽기 전용 스킬. 공개 RSS 피드로 최신 글 목록·키워드 검색·항목 상세를 읽기 전용으로 조회한다. 트리거: ''긱뉴스 오늘 뭐 올라왔어'', ''긱 |  |
| [grill-me](../skills/grill-me) | 지시·계획의 의도 파악이 불충분할 때 합의에 이를 때까지 구조화 질문을 반복하는 의도 합의 스킬(work management 앵커 c). "의도 확인 / 의도 합의 / grill me / 계획 검증 질문 / 뭘 원하는지 모르겠다" 트리거로 발동 |  |
| [insane-search](../skills/insane-search) | 차단된 웹사이트 적응형 접근 — 되는 방법이 나올 때까지 모든 수단을 시도. WebFetch가 402/403/차단될 때, X/Twitter·Reddit·YouTube·GitHub·Medium·Substack·네이버·쿠팡·LinkedIn 등 WAF/봇  |  |
| [last30days](../skills/last30days) | 최근 30일의 Reddit + X + 웹에서 어떤 주제든 조사해 종합하고, 복붙 가능한 프롬프트로 정리. '요즘 사람들이 X에 대해 뭐라고 해?', 최신 모범 사례 학습 요청 시 사용. 전체 기능엔 OPENAI_API_KEY/XAI_API_KEY 필요 | what are people saying about X |
| [market-research-reports](../skills/market-research-reports) | Builds evidence-traceable market research reports and assumption-driven market sizing or forecast scenarios. Use for market definition, indu |  |
| [parallel-web](../skills/parallel-web) | Uses Parallel CLI for web search, URL extraction, deep research, structured data enrichment, entity discovery, and recurring web monitoring. |  |
| [research-sources](../skills/research-sources) | When the user wants to find information sources for content ideation, competitor monitoring, or industry tracking. Also use when the user me | research sources,·information sources,·content ideation, |
| [what-if-oracle](../skills/what-if-oracle) | Supports structured what-if scenario analysis for research planning, experimental contingencies, and scientific project decisions. Explores  |  |
