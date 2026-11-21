# 논문·학술·독서 (25개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/academic.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-academic && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-academic && cd /tmp/ccs-academic && git sparse-checkout set skills/bgpt-paper-search skills/citation-gate skills/hypogenic skills/hypothesis-generation skills/kci-journal-finder skills/keris-academic-search skills/paper-critical-review skills/paper-lookup skills/paper-study skills/paper-writing-master skills/paper-writing-order skills/paperclip skills/paperzilla skills/peer-review skills/pyzotero skills/reading-craft skills/ref-toolkit skills/research-grants skills/scholar-evaluation skills/scientific-brainstorming skills/scientific-critical-thinking skills/scientific-writing skills/talk-to-my-books skills/venue-templates skills/zotero && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [bgpt-paper-search](../skills/bgpt-paper-search) | Searches BGPT scientific papers by topic or DOI and retrieves claim-level evidence extracted from full text, including experiments, reported |  |
| [citation-gate](../skills/citation-gate) | 저자 책 학술 신뢰성 cross-cutting 가드. M2 HallucinationDetector + M3 AuthorityGrader + M4 QuantitativeAnchorExtractor 결정론 호출. 5 신호 자동 감지 — Critical 시 |  |
| [hypogenic](../skills/hypogenic) | Plans and audits use of ChicagoHAI HypoGeniC/HypoRefine for LLM-assisted hypothesis generation from labeled text datasets. Use for the `hypo |  |
| [hypothesis-generation](../skills/hypothesis-generation) | Formulates evidence-bounded scientific questions, candidate hypotheses, rival explanations, causal or associational claims, discriminating p |  |
| [kci-journal-finder](../skills/kci-journal-finder) | KCI 등재지·등재후보지 2,888종에서 투고할 학술지를 고르는 스킬. 분야·등급(우수등재/등재/등재후보)·연 발행 횟수·발행 주체·언어로 거르고, 게재료·심사료·투고 마감·투고 시스템(JAMS 등)·대학원생 감면 정보(215종 채움)를 함께 보여 준 | 어디에 투고\·학술지 추천\·등재지 목록\ |
| [keris-academic-search](../skills/keris-academic-search) | Use when the user asks to search Korean theses, academic articles, research reports, journals, or university-library catalog metadata throug |  |
| [paper-critical-review](../skills/paper-critical-review) | 학술 논문을 까다로운 Reviewer 2 관점에서 적대적으로 심사하거나, 저자·학생을 지도하기 위해 논문의 약점을 사전 진단하는 전문 논문점검 스킬. 초록·본문·결론을 읽고 contribution 요약 → 주장-근거 매핑 → 실험설계 공격 → 재현성  | 논문 심사·논문 리뷰·reviewer 2 |
| [paper-lookup](../skills/paper-lookup) | Searches 18 scholarly APIs for papers, preprints, citations, open-access full text, repository records, and journal OA status, and returns r | find papers on X·look up this DOI·who cites this paper |
| [paper-study](../skills/paper-study) | 논문을 "능동적으로" 학습하고 마크다운 위키에 축적하는 스킬. 로컬 PDF 논문을 읽고 능동 회상 질문·파인만식 재설명·기존 위키와의 연결을 통해 기억에 정착시킨 뒤, 사용자의 재설명과 연구 적용 아이디어를 포함한 .md 노트로 저장하고 논문/개념 간 | 능동적으로 |
| [paper-writing-master](../skills/paper-writing-master) | 논문작성 전 과정(준비·주제·선행연구·연구문제·설계·뼈대·서론·이론적 배경·방법·분석·결론·초록·윤리·심사·투고)을 한국 대학원 학위논문·학술지 논문 기준으로 코칭하고 산출물을 함께 만드는 총괄 스킬. 논준모연구소(김성하) 공개 영상 1,080편 종합 | 논문 써야 해\·논문 처음부터 끝까지\·학위논문 지도\ |
| [paper-writing-order](../skills/paper-writing-order) | 논문 13편을 쓴 저자의 '논문 쓰기 순서' 방법론을 기반으로, 논문이 안 써지는 원인을 '쓰는 순서의 오류'로 진단하고 5단계 기획 순서(넓은 주제 → 발췌독 → 인용문 3분류 → 뼈대 세우기 → 서론·결론 쌍)로 논문 작성을 코칭하는 스킬. 사용자 | 논문이 안 써져요\·논문 어디서부터 시작\·주제를 못 잡겠어요\ |
| [paperclip](../skills/paperclip) | Searches and reads biomedical papers, FDA/PMDA/EMA documents, clinical trials, and protein records with the GXL Paperclip CLI and Python SDK |  |
| [paperzilla](../skills/paperzilla) | Reads projects, searches project feeds, and retrieves recommendations and canonical papers in Paperzilla through the pz CLI. Supports recent |  |
| [peer-review](../skills/peer-review) | Prepares evidence-bounded, constructive peer-review drafts and structured manuscript assessments. Supports authorized review of scientific m |  |
| [pyzotero](../skills/pyzotero) | >- Manages Zotero reference libraries using the pyzotero Python client: retrieves, creates, updates, and deletes items, collections, tags, a |  |
| [reading-craft](../skills/reading-craft) | 책과 긴 글을 "읽고 나서 남게" 읽는 법을 코칭하는 독서 훈련 스킬. 책의 성격을 먼저 판정(지나가는 책·써먹을 책·바꿀 책)하고, 존 스튜어트 밀의 7단계 독서법(해설서→통독→정독→필사→주제 확장→가르치기→쓰기)과 문해력 4단계(낱말 세우기→문장  | 읽고 나서 남게·책을 읽어도 남는 게 없어·독서법 알려줘 |
| [ref-toolkit](../skills/ref-toolkit) | 박사논문 레퍼런스 수집 도구 안내·라우팅 스킬. 사용자가 "레퍼런스 수집", "문헌 검색 도구", "Consensus/Elicit/SciSpace 뭐 쓸까", "논문 자료 조사 도구", "레퍼런스 대시보드", "/ref-toolkit"을 요청하면 발동 | 레퍼런스 수집·문헌 검색 도구·Consensus/Elicit/SciSpace 뭐 쓸까 |
| [research-grants](../skills/research-grants) | Supports research proposal preparation and review for NSF, NIH, DOE, DARPA, and Taiwan NSTC, including opportunity-specific requirements, ai |  |
| [scholar-evaluation](../skills/scholar-evaluation) | Provides qualitative-first, evidence-traceable developmental review of scholarly works and audit low-stakes research-assessment rubrics with |  |
| [scientific-brainstorming](../skills/scientific-brainstorming) | Facilitates evidence-aware scientific ideation with independent generation, structured discussion, explicit assumptions, transparent evaluat |  |
| [scientific-critical-thinking](../skills/scientific-critical-thinking) | Evaluates scientific claims and evidence quality. Applies to experimental design validity, biases and confounders, statistical interpretatio |  |
| [scientific-writing](../skills/scientific-writing) | Drafts, revises, and audits scientific manuscripts or reports with explicit evidence provenance, reporting-guideline coverage, authorship ac |  |
| [talk-to-my-books](../skills/talk-to-my-books) | 사용자의 자료(책·설교·주석·강의안 등)를 talk-to-algorithms.vercel.app 방식의 "책과 대화" 형식으로 변환·등록하고, 등록된 자료와 본문 근거 기반 대화를 수행하는 스킬. 두 가지 모드로 작동한다. (1) 등록 모드 — 사용자 | 책과 대화·이 책 등록해줘·이 자료 학습시켜줘 |
| [venue-templates](../skills/venue-templates) | Prepares journal manuscripts, conference papers, research posters, and grant documents using venue-specific formatting guidance and bundled  |  |
| [zotero](../skills/zotero) | 문헌 관리·인용 | 내 조테로에서 찾아줘·참고문헌 몇 편이야·서지정보 진단 |
