# 글쓰기·윤문 (30개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/writing.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-writing && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-writing && cd /tmp/ccs-writing && git sparse-checkout set skills/adult-vocabulary-writing-coach skills/blank-page-cowrite skills/classic-sentence-writing-coach skills/copy-editing skills/copywriting skills/dhdna-profiler skills/final-report-lint skills/frontline-writing-coach skills/godowon-writing-coach skills/humanize skills/humanize-korean skills/humanize-redo skills/humanize-scan skills/korean-character-count skills/korean-humanizer skills/korean-middle-korean skills/korean-slang-writing skills/korean-spell-check skills/markdown-mermaid-writing skills/my-writing-master-prompt skills/parkjooyeon-lyric-writing-coach skills/redteam skills/seeing-writing-lens skills/soul-distill skills/ste-korean skills/technique-transfer skills/toego-korean skills/token-diet skills/writing-analytical-essay skills/yuhongjun-writing-coach && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [adult-vocabulary-writing-coach](../skills/adult-vocabulary-writing-coach) | 유선경 작가의 《어른의 어휘력》(앤의서재)에 담긴 어휘력·글쓰기 철학을 기반으로, 한국어 글(에세이, 칼럼, 자기소개서, 논술, 블로그, 발표문 등)을 정확한 어휘와 단단한 구성으로 다듬거나 새로 쓰도록 돕는 코칭 스킬. 사용자가 "어른의 어휘력 스타 | 어른의 어휘력 스타일로 써줘·정확한 어휘로 다듬어줘·곁가지 서술 줄여줘 |
| [blank-page-cowrite](../skills/blank-page-cowrite) | 빈 문서 한 줄씩 같이 쓰기. AI가 만든 긴 보고서·리서치 결과를 사용자에게 그대로 넘기지 않고, 빈 양식에서 섹션→문단 단위로 같이 써 가며 사용자를 인터뷰해 이해시키는 스킬(커리어해커 알렉스의 '미트 프록시' 탈출법). 트리거: '한 줄씩 같이  |  |
| [classic-sentence-writing-coach](../skills/classic-sentence-writing-coach) | 주인님 소장 자료(일당백 에세이집 47편·시즌1 고전·명언/첫 문장 강의·글쓰기 강의, 상세 102권·압축 72권)에서 뽑은 「고전·명언 문장사전」을 근거로, 설교·칼럼·강의 도입·축사·묵상글·카드뉴스에 들어갈 고전 문장을 골라 주고, 그 책의 문체( | 고전·명언 문장사전·고전 인용 넣어줘·명언 하나 찾아줘 |
| [copy-editing](../skills/copy-editing) | When the user wants to edit, tighten, proofread, or refresh existing copy, or asks whether to keep, cut, or change a line in it, without rew |  |
| [copywriting](../skills/copywriting) | When the user wants to write or rewrite page copy (homepage, landing, pricing, feature), or asks which headline, promise, or message to lead |  |
| [dhdna-profiler](../skills/dhdna-profiler) | Applies the DHDNA framework as an exploratory rubric for reasoning and writing patterns in supplied text. Used for explicit requests for DHD |  |
| [final-report-lint](../skills/final-report-lint) | 에이전트가 사용자에게 보내는 마지막 메시지(작업 완료 보고·결과 요약·조사 결론)를 Claude Mythos 5.1 시스템 프롬프트의 'Writing for the user'·'Delivering work' 규칙으로 린트하고 고쳐 쓴다. 검사 항목은  | 원하시면 ~할까요?·~하겠습니다·최종보고 점검 |
| [frontline-writing-coach](../skills/frontline-writing-coach) | 은유 작가의 《글쓰기의 최전선》(메멘토)에 담긴 글쓰기 철학과 실제 수업 방식을 기반으로, 한국어 에세이·자기서사·후기·인터뷰 원고 등을 정직하고 구체적인 문장으로 다듬거나 새로 쓰도록 돕는 코칭 스킬. 사용자가 "은유 작가처럼", "글쓰기의 최전선  | 은유 작가처럼·글쓰기의 최전선 스타일로·관념적인 표현 좀 구체적으로 바꿔줘 |
| [godowon-writing-coach](../skills/godowon-writing-coach) | 고도원의 《누구든 글쓰기 - 고도원의 인생작법》(해냄)에 담긴 글쓰기 철학과 실전 기법을 기반으로, 한국어 글(에세이, 편지, 아침편지/뉴스레터, 자기소개서, 연설문, 칼럼, 치유 글쓰기 등)을 쓰거나 다듬도록 돕는 코칭 스킬. 사용자가 "고도원 스타 | 고도원 스타일로·인생작법처럼·아침편지 스타일로 써줘 |
| [humanize](../skills/humanize) | AI가 쓴 한글 텍스트를 자연스럽게 윤문하는 진입 명령. humanize-korean 파이프라인을 shim 의 route_hint 가 정한 경로(light 1콜 · standard 2콜 · heavy 3+콜)로 실행하고 `--strict`면 heavy | /humanize |
| [humanize-korean](../skills/humanize-korean) | AI(ChatGPT·Claude·Gemini 등)가 쓴 한글 텍스트를 "사람이 쓴 글처럼" 윤문해주는 오케스트레이터 스킬. 번역투·영어 인용 과다·기계적 병렬·관용구·피동태 남용·접속사 남발·리듬 균일성·이모지/불릿 과다 등 10대 카테고리 85개 A | 사람이 쓴 글처럼·AI 티 없애줘·AI 같은 글 자연스럽게 |
| [humanize-redo](../skills/humanize-redo) | 가장 최근 윤문 결과를 2차로 다시 다듬는다 — 특정 카테고리·문단·강도 조정도 가능. humanize-korean strict 윤문(Phase B)을 기존 run_id에 재실행해 잔존 finding을 처리한다. 트리거 — "/humanize-redo | /humanize-redo |
| [humanize-scan](../skills/humanize-scan) | 한글 글에 AI 티가 얼마나 있는지 재고, 실제로 고치면 어떻게 되는지 표본으로 보여주는 정찰 스킬. 실측 판별력 상위 6개만 본다. 워크스페이스·진단·게이트·서브에이전트 없이 이 대화 안에서 끝낸다(파일 0개, 서브에이전트 0회). 손볼 게 많다고  | 이 글 AI 같아?·AI 티 있나 봐줘·스캔해줘 |
| [korean-character-count](../skills/korean-character-count) | Count Korean text deterministically with exact grapheme, line, and byte contracts for self-intros and form limits. |  |
| [korean-humanizer](../skills/korean-humanizer) | AI가 쓴 티가 나는 한국어 글을 자연스러운 사람 글로 고친다. 번역체, AI 상투어, 과도한 명사화·피동, 3의 법칙, 과장된 의의 부여, 마무리 상투구, 챗봇 잔재, 줄표·곡선따옴표 같은 한국어 특유의 AI 흔적을 심각도(S1/S2/S3)로 분류해 | 1000자로·AI 티 안 나게·사람이 쓴 것처럼 |
| [korean-middle-korean](../skills/korean-middle-korean) | Convert incoming Korean text into a deterministic Korean Middle Korean-style rewrite with archaic particles, endings, Hanja hints, and tone- |  |
| [korean-slang-writing](../skills/korean-slang-writing) | Use curated Korean trending-slang candidates plus best-effort Namu Wiki lookups to write witty Korean text with up-to-date slang, with conse |  |
| [korean-spell-check](../skills/korean-spell-check) | Use Nara/PNU Korean spell-check surfaces conservatively to proofread Korean text, chunk long input, and return change-focused correction sug |  |
| [markdown-mermaid-writing](../skills/markdown-mermaid-writing) | Writes scientific Markdown documentation and Mermaid diagrams for workflows, relationships, timelines, and schemas. Provides syntax referenc |  |
| [my-writing-master-prompt](../skills/my-writing-master-prompt) | 우석지니의 "AI가 나처럼 글을 쓰는 마스터 프롬프트 역설계" 방법론을 기반으로, AI 초안과 사용자의 수정본을 쌍(pair)으로 비교 분석하여 사용자만의 글쓰기 규칙을 역설계하고, 이를 마스터 프롬프트로 축적·적용하는 스킬. 제안서·보고서·발표문 등 | AI가 나처럼 글을 쓰는 마스터 프롬프트 역설계·내 문체로 써줘·나처럼 써줘 |
| [parkjooyeon-lyric-writing-coach](../skills/parkjooyeon-lyric-writing-coach) | 작사가 박주연(〈입영열차 안에서〉〈너에게로 또 다시〉〈오래전 그날〉〈외워두세요〉 등 KOMCA 등록 300여 곡)의 작사법을 기반으로 노래 가사·찬양 가사·설교 도입 장면·짧은 글을 쓰거나 다듬도록 돕는 코칭 스킬. 사용자가 "박주연 스타일로", "박 | 박주연 스타일로·박주연처럼·작사해줘 |
| [redteam](../skills/redteam) | 기획서·글·설교문·전략을 목적별 전문 레드팀이 프레임워크로 공격하고, 요청 시 조언까지 하는 확증편향 파괴 스킬. 스쿼드 3종(business 기획·writing 글쓰기·sermon 설교) 중 자동 또는 지목 소집한다. 사용자가 "레드팀", "악마의  | 레드팀·악마의 변호인·비판해줘 |
| [seeing-writing-lens](../skills/seeing-writing-lens) | 진서·버거·손택 세 렌즈로 글과 이미지를 점검하는 코치. (1) 진서 렌즈 — 『글쓰기 생각쓰기』의 군더더기 4종(일 안 하는 단어·긴 단어·동사와 겹치는 부사·행위자 숨긴 피동)을 표시하고 "무엇을 말하려는가/제대로 말했나/처음 읽는 사람에게 명료한 | 무엇을 말하려는가/제대로 말했나/처음 읽는 사람에게 명료한가·군더더기 빼줘·진서처럼 퇴고 |
| [soul-distill](../skills/soul-distill) | 사용자 본인이 직접 쓴 글·메시지·설교·메일 묶음에서 "분신 에이전트용 soul.md 초안"을 증류한다 — ①말투 ②개입 시점(언제 답하고 언제 침묵) ③판단 기준·거절 방식 ④금지선(자기 이름으로 하지 않는 일)을 근거 문장과 함께 뽑는다. "내 분 | 분신 에이전트용 soul.md 초안·내 분신 만들어줘·soul.md 증류 |
| [ste-korean](../skills/ste-korean) | 한국어 통제어(STE100식) 글쓰기. ASD-STE100(항공 정비 문서용 통제어) 규칙을 한국어에 맞게 옮긴 12개 규칙으로 설명·요약·절차서·공문·AI 지시서를 짧고 오해 없는 문장으로 쓰거나 고친다. 모드: 엄격 / 80%(기본) / 절차 /  | STE로 써 줘·통제어로·STE100 80%로 |
| [technique-transfer](../skills/technique-transfer) | 남이 쓴 글이나 책을 넣으면 그 안에 쓰인 글쓰기 기법을 10개 영역 97개 항목의 분류 체계로 체계적으로 분석해 ''기법 프로파일''로 뽑아내고, 그 프로파일을 사용자 자신의 글에 이식해 같은 기법으로 다시 쓰게 해 주는 기법 채굴·이식 스킬. 세  | 이 글 기법 분석해줘·이 작가처럼 쓰고 싶어·이 책 문체 분석 |
| [toego-korean](../skills/toego-korean) | 사람이 직접 쓴 한국어 글(에세이·블로그·보고서·자기소개서·편지·일기·칼럼·아이의 글)을 구조 → 문단 → 문장 → 처음과 끝의 순서로 고쳐 주는 퇴고 전담 스킬. 유시민의 '나쁜 글 고치는 여섯 가지'(소리 내어 읽기·짧게 쓰기·군더더기 빼기·흐린  | 이 글 좀 고쳐줘·퇴고해줘·다듬어줘 |
| [token-diet](../skills/token-diet) | 지침 파일(SKILL.md·CLAUDE.md·AGENTS.md·시스템 프롬프트)에서 토큰을 태우는 문구를 린트하고 고쳐 쓴다. 검사 항목은 '매번·항상 읽어'식 상시 읽기, 부정 트리거가 없는 스킬 description, 종료 조건 누락, 우선순위 없 | 토큰 다이어트·지침 린트·스킬 설명 점검 |
| [writing-analytical-essay](../skills/writing-analytical-essay) | Use when the user gives a one-line topic (책·논문·행사·제품·정책·기술·시사·개인 경험) and wants a finished Korean SNS·블로그용 분석형 글, 서평, 행사 후기, 기술 분석, 시사 논평, 칼럼 | 이 주제로 글 써줘·블로그 글·SNS 글 |
| [yuhongjun-writing-coach](../skills/yuhongjun-writing-coach) | 유홍준 교수(『나의 문화유산답사기』, 『나의 인생만사 답사기』 부록 '좋은 글쓰기를 위한 15가지 조언')의 글쓰기 원리로 한국어 산문·칼럼·답사기·설교 예화·주보 글·강의 원고를 쓰거나 퇴고하는 코칭 스킬. "유홍준처럼", "답사기 스타일로", "쉽 | 유홍준처럼·답사기 스타일로·쉽게 읽히게 |
