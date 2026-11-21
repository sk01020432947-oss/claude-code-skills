# 지식관리·노트 (25개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/pkm.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-pkm && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-pkm && cd /tmp/ccs-pkm && git sparse-checkout set skills/alda-report skills/analog-diary skills/canvas skills/km-archive-reorganization skills/km-link-audit skills/km-link-strengthening skills/kordoc-obsidian-bridge skills/memory-four-cells skills/nlm-skill skills/notebooklm skills/pkm-os skills/save skills/url-manual-forge skills/weekly-review skills/wiki skills/wiki-cli skills/wiki-fold skills/wiki-ingest skills/wiki-lint skills/wiki-mode skills/wiki-query skills/wiki-recall skills/wiki-retrieve skills/zettelkasten-note 'skills/통합-data-수집기' && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [alda-report](../skills/alda-report) | 알다 로컬 위키(옵시디언 메인 볼트의 내 노트·설교·문헌을 로컬 qwen3:8b·bge-m3로 색인한 것)를 먼저 조회하고 웹검색으로 보강해, 빈틈 분석과 mermaid 개념 지도를 담은 보고서 초안을 PKM/30 output/에 status draf | 알다로 보고서·내 노트 기반 리서치 보고서·알다 리포트 |
| [analog-diary](../skills/analog-diary) | 어떤 자료든(사진·그림·유튜브·영상·짧은 글·아이디어) 낡은 종이 위 손판화 스탬프 카드로 변환해 일기장 "스쳐가는 일상"에 발행하는 스킬. 카드 하단에 Location/No./Keywords/Year 타자기 메타를 찍고, Documents\analo | 스쳐가는 일상·그림일기·아날로그 일기 |
| [canvas](../skills/canvas) | Create, inspect, and update Obsidian JSON Canvas boards with text, file, link, group, and edge nodes. Use for canvas status, canvas lists, v |  |
| [km-archive-reorganization](../skills/km-archive-reorganization) | Use when needing Archive Reorganization Mode (Mode R) - 대규모 vault 폴더 재편을 위한 6-Phase 반복 적용 워크플로우. 얼룩소 프로젝트 4단계를 일반화. |  |
| [km-link-audit](../skills/km-link-audit) | Use when needing Knowledge Manager 링크 감사 스킬. Obsidian vault의 broken links, orphan notes, 미해결 참조 감지 및 수정. |  |
| [km-link-strengthening](../skills/km-link-strengthening) | Use when needing Knowledge Manager 링크 강화 스킬. Obsidian vault 노트 간 의미적 wikilink 연결 생성 및 백링크 보강. |  |
| [kordoc-obsidian-bridge](../skills/kordoc-obsidian-bridge) | 옵시디언 노트와 한글(HWP/HWPX)·PDF 문서를 kordoc으로 왕복시킨다. "hwp를 옵시디언 노트로", "이 공문 노트로 저장", "노트를 hwpx 공문으로", "옵시디언 노트로 보고서 만들어줘" 요청 시 사용. 일반 파싱·생성 자체는 kor | hwp를 옵시디언 노트로·이 공문 노트로 저장·노트를 hwpx 공문으로 |
| [memory-four-cells](../skills/memory-four-cells) | 작업 피드백·회의 메모·세션 기록을 교훈·상태·결정·선호 네 칸으로 나눠 ~/Desktop/cysjavis/기억장치/에 쌓고, 거기서 "최근 결정"·"다음 할 일"을 근거 인용과 함께 꺼낸다. "피드백 기록해", "네 칸으로 정리", "최근 결정 정리 | 최근 결정·다음 할 일·피드백 기록해 |
| [nlm-skill](../skills/nlm-skill) | Expert guide for the NotebookLM CLI (`nlm`) and MCP server - interfaces for Google NotebookLM. Use this skill when users want to interact wi | nlm\·notebooklm\·notebook lm\ |
| [notebooklm](../skills/notebooklm) | Google NotebookLM 완전 API — 웹 UI에 없는 기능까지 프로그래밍 방식으로 접근. 노트북 생성, 소스 추가, 모든 아티팩트 유형 생성, 다양한 형식 다운로드. /notebooklm 명시 호출 또는 "X에 대해 팟캐스트 만들어줘" 같은 |  |
| [pkm-os](../skills/pkm-os) | 김병곤의 옵시디언 지식 OS(PKM 폴더: raw→wiki→output 3층 + MOC) 운영 스킬. 유튜브·논문·도서·클리핑·설교자료를 raw에 넣고(ingest), wiki를 근거로 답하고(query), 건강 검진(lint), 세이브 포인트(log |  |
| [save](../skills/save) | Save a user-selected answer, decision, insight, or session summary into an Obsidian vault as one reviewed transaction. Use only when the use |  |
| [url-manual-forge](../skills/url-manual-forge) | URL 한 줄(YouTube·GitHub·X·웹 글)을 받아 따라 하는 매뉴얼 HTML → 응용·확장 아이디어와 사례 → 나에게 적용하는 법과 사용 실례 → 스킬·설치 가치 판정표 → 옵시디언 노트 → 비공개 아티팩트 발행까지 한 번에 끝낸다. 트리거 | 이 URL로 메뉴얼 만들어줘·메뉴얼 html+응용+나의 적용·스킬 점검하고 옵시디언에 저장 |
| [weekly-review](../skills/weekly-review) | 한 주를 데이터 기반으로 회고한다. LLM 위키의 세션 로그·질의 결과·새 자료와 옵시디언 모선 볼트의 이번 주 노트를 모아, 7 재활용 축(설교·목회·논문·강의·저술·AI시스템·인문교양)별 진척과 이번 주의 원싱, 다음 주 우선순위를 정리한다. "주 | 주간 회고·이번 주 회고·한 주 정리 |
| [wiki](../skills/wiki) | Initialize, adopt, and route work for a separate Obsidian knowledge vault through the portable claude-obsidian core. Use for vault setup, sc |  |
| [wiki-cli](../skills/wiki-cli) | Detect and use the official Obsidian command-line interface for read-only vault access; use for wiki-cli, Obsidian CLI, Obsidian read, Obsid |  |
| [wiki-fold](../skills/wiki-fold) | Create a bounded, extractive, structurally idempotent rollup of recent Obsidian wiki log entries, with dry-run preview by default and one op |  |
| [wiki-ingest](../skills/wiki-ingest) | Ingest supplied source material into an Obsidian vault with provenance and claim tracking: pasted text, files staged in the selected vault's |  |
| [wiki-lint](../skills/wiki-lint) | Run a deterministic, read-only health check on an Obsidian wiki. Use for lint, vault health check, audit wiki health, find orphans, find dea |  |
| [wiki-mode](../skills/wiki-mode) | Read or configure the vault filing methodology and suggest destinations for planned knowledge creation under Generic, LYT, PARA, or Zettelka |  |
| [wiki-query](../skills/wiki-query) | Answer an explicitly vault-scoped question from an Obsidian wiki without changing it. Use when the user selects the vault as the evidence so |  |
| [wiki-recall](../skills/wiki-recall) | 설교·논문·강의·저술 준비를 시작할 때, 백지에서 시작하지 않도록 내 LLM 위키와 옵시디언 모선 볼트에 이미 축적된 지식을 먼저 조회한다. 본문·주제·개념을 받아 관련 위키 페이지·원본 자료·과거 설교/강의 노트를 찾아 요약해 준다. "설교 준비", | 설교 준비·본문 연구·논문 쓰자 |
| [wiki-retrieve](../skills/wiki-retrieve) | Build and query a vault-local contextual BM25 retrieval index with optional multilingual Nomic cosine reranking; use for retrieve, hybrid re |  |
| [zettelkasten-note](../skills/zettelkasten-note) | Obsidian/Markdown 노트를 제텔카스텐 원칙(원자적 노트·permanent/literature/MOC 구분·wikilink 연결)으로 작성하는 표준 템플릿과 규칙. 자료를 노트로 정리하거나, 노트 형식·frontmatter·태그 체계를 잡거 | 제텔카스텐으로 정리해줘 |
| [통합-data-수집기](../skills/통합-data-수집기) | 여러 곳에 흩어진 개인 자료(쓰레드·X·인스타·페이스북·유튜브·블로그·카톡·브라우저 북마크·옵시디언 노트·Claude 아티팩트·폰 자료·외장하드/USB/NAS 파일)를 한 파일로 모으고, 검색·메모·태그·별표·삭제·내보내기가 되는 단일 HTML 보기  | 통합 DATA 수집기·통합 DATA 수집기 만들어줘·통합자료수집기 만들어줘 |
