---
name: context7-docs
description: 라이브러리·프레임워크·SDK·CLI의 최신 공식 문서를 Context7 REST로 가져와 코드를 쓴다. Remotion·python-pptx·python-hwpx·Obsidian API·MCP SDK·FastMCP·Mermaid·Reveal.js·Marp 등으로 코드를 짜거나 설정·버전 이전·API 시그니처를 확인할 때, "context7", "최신 문서로", "use context7" 요청 시 사용. npm·MCP 설치 없이 python3만으로 동작. 일반 개념 설명·리팩터링·비즈니스 로직 디버깅에는 쓰지 않는다.
---

# Context7 최신 문서 조회 (npm 불필요판)

공식 `find-docs` 스킬(ctx7 CLI)과 같은 절차를 `scripts/c7.py`(표준 라이브러리) 하나로 수행한다.

## 절차
1. 라이브러리 ID 확인 — 사용자가 `/org/project`를 줬으면 생략.
   `python3 ~/.claude/skills/context7-docs/scripts/c7.py lib <공식이름> "<찾을 내용>"`
   - 이름은 공식 표기("Next.js", "python-pptx"). 고르는 기준: 이름 일치 → 스니펫 수 → 점수(100 만점).
   - 버전을 말했으면 결과의 버전 목록에서 `/org/project/<버전>`을 쓴다.
2. 문서 조회 — 개념 하나당 한 번.
   `python3 .../c7.py docs <ID> "<구체적 질문>" [--lang Python]`
3. 빠른 길: 라이브러리를 몰라도 되면 한 번에
   `python3 .../c7.py search "<질문>" [--lib 이름 ...] [--lang TypeScript]`
4. 가져온 스니펫으로 답하고, 쓴 라이브러리 ID·버전·Source URL을 밝힌다.

## 규칙
- 질문당 호출은 3회 이내. 못 찾으면 가진 최선의 결과를 쓴다.
- 질의는 영어 문장이 정확도가 높다("auth" ✗ → "How to set up JWT auth in Express" ✓).
- 질의에 API 키·비밀번호·개인정보·비공개 코드를 넣지 않는다(질의는 Context7 서버로 전송된다).
- 429(한도 초과)·오류로 못 가져오면 조용히 학습 데이터로 바꾸지 말고 "Context7 미사용, 내용이 낡았을 수 있음"을 알린다.
- 한도를 올리려면 사용자가 context7.com/dashboard 에서 키를 받아 `CONTEXT7_API_KEY`로 설정한다(Claude가 대신 입력하지 않는다).

## 자주 쓰는 ID (2026-10-16 실측)
| 용도 | ID |
|---|---|
| 모션그래픽 | `/remotion-dev/remotion` |
| PPT 생성 | `/scanny/python-pptx` |
| 한글 HWPX | `/airmang/python-hwpx` |
| 옵시디언 플러그인 | `/obsidianmd/obsidian-api`, `/obsidianmd/obsidian-developer-docs` |
| MCP 서버 개발 | `/modelcontextprotocol/typescript-sdk`, `/prefecthq/fastmcp` |
| 다이어그램·슬라이드 | `/mermaid-js/mermaid`, `/reveal/revealjs.com`, `/marp-team/marp-cli` |
