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
| [bgpt-paper-search](../skills/bgpt-paper-search) | Searches BGPT scientific papers by topic or DOI and retrieves claim-level evidence extracted from full text, including experiments, reported<br>주제나 DOI로 BGPT 과학 논문을 검색하고, 전문에서 추출한 주장 단위 근거(실험, 보고된 통계, 범위, 한계, 출처 정보)를 가져온다. 문헌 고찰, 근거 종합, 초록 이상의 실험 세부 정보를 찾을 때 사용. |  |
| [citation-gate](../skills/citation-gate) | 저자 책 학술 신뢰성 cross-cutting 가드. M2 HallucinationDetector + M3 AuthorityGrader + M4 QuantitativeAnchorExtractor 결정론 호출. 5 신호 자동 감지 — Critical 시 |  |
| [hypogenic](../skills/hypogenic) | Plans and audits use of ChicagoHAI HypoGeniC/HypoRefine for LLM-assisted hypothesis generation from labeled text datasets. Use for the `hypo<br>레이블된 텍스트 데이터셋에서 LLM 보조 가설 생성을 위한 ChicagoHAI HypoGeniC/HypoRefine 사용을 계획하고 감사한다. `hypogenic` 패키지, 그 과제 설정, 가설 뱅크, HypoBench 데이터셋에 사용 — 수동 가설  |  |
| [hypothesis-generation](../skills/hypothesis-generation) | Formulates evidence-bounded scientific questions, candidate hypotheses, rival explanations, causal or associational claims, discriminating p<br>근거 범위 안에서 과학 질문, 후보 가설, 경쟁 설명, 인과 또는 연관 주장, 판별 예측, 측정, 사전등록 가능한 분석 계획을 수립한다. 관찰이나 예비 결과를 가설을 사실로 취급하지 않고 투명하고 검증 가능한 연구 계획으로 바꿀 때 사용. |  |
| [kci-journal-finder](../skills/kci-journal-finder) | KCI 등재지·등재후보지 2,888종에서 투고할 학술지를 고르는 스킬. 분야·등급(우수등재/등재/등재후보)·연 발행 횟수·발행 주체·언어로 거르고, 게재료·심사료·투고 마감·투고 시스템(JAMS 등)·대학원생 감면 정보(215종 채움)를 함께 보여 준 | 어디에 투고\·학술지 추천\·등재지 목록\ |
| [keris-academic-search](../skills/keris-academic-search) | Use when the user asks to search Korean theses, academic articles, research reports, journals, or university-library catalog metadata throug |  |
| [paper-critical-review](../skills/paper-critical-review) | 학술 논문을 까다로운 Reviewer 2 관점에서 적대적으로 심사하거나, 저자·학생을 지도하기 위해 논문의 약점을 사전 진단하는 전문 논문점검 스킬. 초록·본문·결론을 읽고 contribution 요약 → 주장-근거 매핑 → 실험설계 공격 → 재현성  | 논문 심사·논문 리뷰·reviewer 2 |
| [paper-lookup](../skills/paper-lookup) | Searches 18 scholarly APIs for papers, preprints, citations, open-access full text, repository records, and journal OA status, and returns r<br>18개 학술 API에서 논문, 프리프린트, 인용, 오픈액세스 전문, 리포지토리 기록, 저널 OA 상태를 검색하고 재현 가능한 출처 정보와 함께 결과를 반환한다. PubMed, PMC, Europe PMC, bioRxiv, medRxiv, arXiv,  | find papers on X·look up this DOI·who cites this paper |
| [paper-study](../skills/paper-study) | 논문을 "능동적으로" 학습하고 마크다운 위키에 축적하는 스킬. 로컬 PDF 논문을 읽고 능동 회상 질문·파인만식 재설명·기존 위키와의 연결을 통해 기억에 정착시킨 뒤, 사용자의 재설명과 연구 적용 아이디어를 포함한 .md 노트로 저장하고 논문/개념 간 | 능동적으로 |
| [paper-writing-master](../skills/paper-writing-master) | 논문작성 전 과정(준비·주제·선행연구·연구문제·설계·뼈대·서론·이론적 배경·방법·분석·결론·초록·윤리·심사·투고)을 한국 대학원 학위논문·학술지 논문 기준으로 코칭하고 산출물을 함께 만드는 총괄 스킬. 논준모연구소(김성하) 공개 영상 1,080편 종합 | 논문 써야 해\·논문 처음부터 끝까지\·학위논문 지도\ |
| [paper-writing-order](../skills/paper-writing-order) | 논문 13편을 쓴 저자의 '논문 쓰기 순서' 방법론을 기반으로, 논문이 안 써지는 원인을 '쓰는 순서의 오류'로 진단하고 5단계 기획 순서(넓은 주제 → 발췌독 → 인용문 3분류 → 뼈대 세우기 → 서론·결론 쌍)로 논문 작성을 코칭하는 스킬. 사용자 | 논문이 안 써져요\·논문 어디서부터 시작\·주제를 못 잡겠어요\ |
| [paperclip](../skills/paperclip) | Searches and reads biomedical papers, FDA/PMDA/EMA documents, clinical trials, and protein records with the GXL Paperclip CLI and Python SDK<br>GXL Paperclip CLI와 Python SDK로 생의학 논문, FDA/PMDA/EMA 문서, 임상시험, 단백질 기록을 검색하고 읽는다. 소스 범위 검색, 전문 grep, 메타데이터 SQL, map/reduce 추출, 그림 분석, 선택적 리포지토 |  |
| [paperzilla](../skills/paperzilla) | Reads projects, searches project feeds, and retrieves recommendations and canonical papers in Paperzilla through the pz CLI. Supports recent<br>pz CLI로 Paperzilla의 프로젝트를 읽고, 프로젝트 피드를 검색하며, 추천과 정본 논문을 가져온다. 최근 추천, 논문 상세, 마크다운 기반 요약, 추천 피드백, JSON 내보내기, Atom 피드 URL을 지원. |  |
| [peer-review](../skills/peer-review) | Prepares evidence-bounded, constructive peer-review drafts and structured manuscript assessments. Supports authorized review of scientific m<br>근거 범위 내에서 건설적인 동료 심사 초안과 구조화된 원고 평가를 준비한다. 과학 원고, 프로토콜, 프리프린트, 연구 제안서의 권한 있는 심사; 보고 지침 선택; 주장-근거 점검; 방법론, 통계, 재현성, 윤리, 그림·표, 인용 비평; 수정 응답 계획 |  |
| [pyzotero](../skills/pyzotero) | >- Manages Zotero reference libraries using the pyzotero Python client: retrieves, creates, updates, and deletes items, collections, tags, a<br>pyzotero Python 클라이언트로 Zotero 참고문헌 라이브러리를 관리한다: Zotero Web API v3 또는 로컬 API로 항목, 컬렉션, 태그, 첨부 파일을 조회·생성·수정·삭제. Zotero 라이브러리를 프로그래밍 방식으로 다루거나, |  |
| [reading-craft](../skills/reading-craft) | 책과 긴 글을 "읽고 나서 남게" 읽는 법을 코칭하는 독서 훈련 스킬. 책의 성격을 먼저 판정(지나가는 책·써먹을 책·바꿀 책)하고, 존 스튜어트 밀의 7단계 독서법(해설서→통독→정독→필사→주제 확장→가르치기→쓰기)과 문해력 4단계(낱말 세우기→문장  | 읽고 나서 남게·책을 읽어도 남는 게 없어·독서법 알려줘 |
| [ref-toolkit](../skills/ref-toolkit) | 박사논문 레퍼런스 수집 도구 안내·라우팅 스킬. 사용자가 "레퍼런스 수집", "문헌 검색 도구", "Consensus/Elicit/SciSpace 뭐 쓸까", "논문 자료 조사 도구", "레퍼런스 대시보드", "/ref-toolkit"을 요청하면 발동 | 레퍼런스 수집·문헌 검색 도구·Consensus/Elicit/SciSpace 뭐 쓸까 |
| [research-grants](../skills/research-grants) | Supports research proposal preparation and review for NSF, NIH, DOE, DARPA, and Taiwan NSTC, including opportunity-specific requirements, ai<br>NSF, NIH, DOE, DARPA, 대만 NSTC 연구 제안서의 준비와 검토를 지원한다. 공고별 요건, 연구 목표, 심사 기준, 예산, 광범위한 파급효과(broader impacts), 서식, 재제출을 포함. 연구자가 직접 작성하는 연구비 제안서  |  |
| [scholar-evaluation](../skills/scholar-evaluation) | Provides qualitative-first, evidence-traceable developmental review of scholarly works and audit low-stakes research-assessment rubrics with<br>학술 저작에 대해 질적 평가 우선, 증거 추적이 가능한 발전적 검토를 제공하고, 선택적 로컬 품질 관리와 함께 부담이 낮은 연구 평가 루브릭을 감사한다. 사람의 순위를 매기거나 중대한 결정을 내리는 데에는 절대 사용하지 않는다. |  |
| [scientific-brainstorming](../skills/scientific-brainstorming) | Facilitates evidence-aware scientific ideation with independent generation, structured discussion, explicit assumptions, transparent evaluat<br>독립적 아이디어 생성, 구조화된 토론, 명시적 가정, 투명한 평가, 적대적 검토, 결정 기록을 갖춘 증거 기반 과학 아이디어 발상을 돕는다. 초기 단계 연구 브레인스토밍이나 후보 방향의 우선순위 결정에 사용. 실증 검증, 연구 설계, 윤리·규제 검토, |  |
| [scientific-critical-thinking](../skills/scientific-critical-thinking) | Evaluates scientific claims and evidence quality. Applies to experimental design validity, biases and confounders, statistical interpretatio<br>과학적 주장과 증거의 질을 평가한다. 실험 설계 타당성, 편향과 교란 요인, 통계 해석, 증거 등급 체계(GRADE, Cochrane Risk of Bias), 비판적 분석 교육에 적용. 증거 평가와 결함 식별을 지원하며, 정식 동료 심사 작성은 pe |  |
| [scientific-writing](../skills/scientific-writing) | Drafts, revises, and audits scientific manuscripts or reports with explicit evidence provenance, reporting-guideline coverage, authorship ac<br>명시적 증거 출처, 보고 지침 충족, 저자 책임, 기밀 관리, 로컬 일관성 점검을 갖추고 과학 원고나 보고서를 작성·수정·감사한다. 과학적 정확성과 추적 가능성이 중요한 원고 섹션, 참고문헌, 선언문, 표, 그림, 투고 준비에 사용. |  |
| [talk-to-my-books](../skills/talk-to-my-books) | 사용자의 자료(책·설교·주석·강의안 등)를 talk-to-algorithms.vercel.app 방식의 "책과 대화" 형식으로 변환·등록하고, 등록된 자료와 본문 근거 기반 대화를 수행하는 스킬. 두 가지 모드로 작동한다. (1) 등록 모드 — 사용자 | 책과 대화·이 책 등록해줘·이 자료 학습시켜줘 |
| [venue-templates](../skills/venue-templates) | Prepares journal manuscripts, conference papers, research posters, and grant documents using venue-specific formatting guidance and bundled <br>투고처별 서식 지침과 번들 LaTeX 골격으로 학술지 원고, 학회 논문, 연구 포스터, 연구비 문서를 준비한다. 공식 템플릿 선택, 최신 페이지 수·익명성 규칙 확인, 학술 글을 투고처에 맞게 조정, 투고 PDF 점검을 지원. |  |
| [zotero](../skills/zotero) | 사용자의 로컬 Zotero 라이브러리(/Users/kbg1023/Zotero)를 직접 조회·진단·내보내기 하는 스킬. 논문 연구 중 "내 조테로에서 찾아줘", "참고문헌 몇 편이야", "서지정보 진단", "BibTeX 뽑아줘", "그 논문 PDF 읽어<br>문헌 관리·인용 | 내 조테로에서 찾아줘·참고문헌 몇 편이야·서지정보 진단 |
