# 설교·강단 (35개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/sermon.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-sermon && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-sermon && cd /tmp/ccs-sermon && git sparse-checkout set skills/canon-propagate skills/dwelling-sermon-coach skills/kangjunmin-sermon-writing-coach skills/sermon-audience-feedback-persona skills/sermon-augustine-coaching skills/sermon-bavinck-coaching skills/sermon-bible-dictionary skills/sermon-bible-history-matcher skills/sermon-bible-research-writing skills/sermon-brainstorm skills/sermon-calvin-institutes skills/sermon-calvin-style-insight skills/sermon-christian-history-interpreter skills/sermon-commentary-recommendations skills/sermon-doctrinal-planner skills/sermon-emotive-writing-coach skills/sermon-expository-daeji skills/sermon-greek-grammar-machen skills/sermon-history-culture-geo-context skills/sermon-lloyd-jones-coaching skills/sermon-luther-coaching skills/sermon-multi-bible-version-compare skills/sermon-pipeline skills/sermon-planner-52week skills/sermon-prompter skills/sermon-qt-original-text-based skills/sermon-research skills/sermon-series skills/sermon-text-analysis-multimethod skills/sermon-textual-criticism skills/sermon-to-blog skills/sermon-to-youtube skills/sermon-toego-revision skills/sermon-topic-message-coach skills/sermon-topic-research-multidisciplinary && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [canon-propagate](../skills/canon-propagate) | 정본(설교 본문·성경 구절·핵심 문구)을 고치면 그 정본에서 파생된 모든 사본(발표자료·설교문·프롬프터·도식·인포그래픽·손그림·리포트·종합본·hwpx·Obsidian 노트·NotebookLM 소스·아티팩트)을 먼저 목록화하고 한 번에 교체한 뒤 "바꾼 | 바꾼 것 / 못 바꾼 것·정본 고쳤어 사본도·3-5절 개역개정으로 교체 |
| [dwelling-sermon-coach](../skills/dwelling-sermon-coach) | > 한 주 동안 성경 본문과 동행하며 묵상 중심으로 설교를 준비하는 7단계 워크플로우 코치 스킬. 트리거: "머무르는 설교", "동행 설교", "한 주 묵상", "뭉근한 설교 준비", "천천히 설교", "본문에 머무르기", "살아있는 설교", "dwe | 머무르는 설교·동행 설교·한 주 묵상 |
| [kangjunmin-sermon-writing-coach](../skills/kangjunmin-sermon-writing-coach) | 강준민 목사의 《목회자의 글쓰기》(두란노, 2015)에 담긴 원리를 기반으로, 설교 준비와 설교문 작성을 돕는 코칭 스킬. 사용자가 "설교 준비해줘", "설교문 써줘/다듬어줘", "강준민 목사 글쓰기 원리로", "목회자의 글쓰기 스타일로", "다독다상 | 설교 준비해줘·설교문 써줘/다듬어줘·강준민 목사 글쓰기 원리로 |
| [sermon-audience-feedback-persona](../skills/sermon-audience-feedback-persona) | 설교문 초안을 가상의 회중 8명(워킹맘·미혼 청년·중년 사업가·은퇴 직전 권사·결혼 2년차 새신자 자영업·이혼 후 홀로 양육·고3 입시생·1세대 홀몸 권사)이 강단 아래에서 듣는 것처럼, 각자의 삶·신앙 연륜·신학 수준에서 솔직한 속마음(의문·반발·위 | 회중 입장에서 들어줘·워킹맘/청년/새신자/은퇴 권사 시각·여러 페르소나 비교 피드백 |
| [sermon-augustine-coaching](../skills/sermon-augustine-coaching) | 히포의 어거스틴(Augustine of Hippo, 354–430)의 신학과 설교론으로 설교 주제를 잡고 메시지를 깊게 다듬도록 돕는 코칭 스킬. 은혜의 우선성·사랑의 질서(ordo amoris)·두 도성·악의 결핍·삼위일체 같은 핵심 신학과 『기독교 | 어거스틴·Augustine·히포 |
| [sermon-bavinck-coaching](../skills/sermon-bavinck-coaching) | 헤르만 바빙크(Herman Bavinck, 1854–1921)의 신학으로 설교 주제를 잡고 메시지를 깊게 다듬도록 돕는 코칭 스킬. 『개혁교의학(Reformed Dogmatics)』을 1차 자료로 삼고, 거기 없으면 Our Reasonable Fait | 바빙크·Bavinck·개혁교의학 |
| [sermon-bible-dictionary](../skills/sermon-bible-dictionary) | 성경 인물·지명·단어·신학적 개념을 성경 주석서·성경 지도·성경사전·개론서 수준의 깊이로 풀어주는 성경사전 도우미. 원어(히브리어/헬라어) 분석, 어원 추적, 성경 전체 용례 점검, 신학적 의미 해석을 한 응답에 종합하여 제공한다. 사용자가 "성경 단 | 성경 단어 뜻·원어 분석·헬라어/히브리어로 무슨 뜻 |
| [sermon-bible-history-matcher](../skills/sermon-bible-history-matcher) | 성경의 특정 인물·사건·본문 내용을 입력하면 세계사 자료(고고학적 유물, 고대 문헌, 학술 연구)에서 동일하게 매칭되는 역사적 사실을 찾아 제시하는 스킬. 할루시네이션 없는 검증된 증거만 제시하며 학계 주류 의견과 물리적 증거(유물 소장 정보 포함)를 | 성경 인물을 세계사에서 찾아줘·이 성경 사건의 역사적 증거는?·성경과 역사의 교차점 |
| [sermon-bible-research-writing](../skills/sermon-bible-research-writing) | 논문 연구 방법론(체계적 자료 수집·출처 등급·교차 검증·문헌 매트릭스·구조화 집필·인용 전수 점검)을 설교 준비에 적용하여, 성경 본문 연구부터 설교문 완성까지 학술적 엄밀성으로 동행하는 스킬. 트리거 — "설교를 위한 성경연구", "논문식 설교 준 | 설교를 위한 성경연구·논문식 설교 준비·학술적 설교 연구 |
| [sermon-brainstorm](../skills/sermon-brainstorm) | Interactive brainstorming partner for sermon preparation. Asks guided questions to help pastors clarify their message, identify the core ten<br>설교 준비를 위한 인터랙티브 브레인스토밍 파트너. 유도 질문으로 메시지를 명확히 하고 핵심 긴장을 찾아 설교 브리프를 만든다. 목회자와 '함께' 생각하며, 설교를 대신 써주지 않는다. |  |
| [sermon-calvin-institutes](../skills/sermon-calvin-institutes) | 존 칼빈(John Calvin, 1509–1564)의 『기독교 강요(Institutes of the Christian Religion, 1559년 최종판)』 4권 80장 전체를 깊이 있게 분석·해설하고 학습을 지원하는 조직신학 도우미. 1559판 4권 |  |
| [sermon-calvin-style-insight](../skills/sermon-calvin-style-insight) | 존 칼빈(John Calvin, 1509–1564)의 설교 스타일을 연구하고 실제 칼빈식 설교문을 작성하도록 돕는 개혁주의 설교 도우미. 칼빈의 lectio continua(연속 강해) 전통, 본문 충실성, 교리·주해·적용의 통합, 절제된 수사, 목회 | 칼빈식 설교·Calvin sermon·개혁주의 설교 |
| [sermon-christian-history-interpreter](../skills/sermon-christian-history-interpreter) | 고대부터 현대까지의 역사적 사건·인물·사회 흐름을 기독교적 관점에서 해석하고 신학적 통찰을 제공하는 학술 도우미. 로마 제국의 기독교 박해, 콘스탄티누스의 회심, 동서 교회 분열, 십자군 전쟁, 르네상스, 종교개혁(루터·칼빈·츠빙글리), 30년 전쟁, | 기독교 관점에서 ○○를 어떻게 보는가·기독교적 역사 해석·○○ 사건의 신학적 의미 |
| [sermon-commentary-recommendations](../skills/sermon-commentary-recommendations) | 성경 66권 각 권별로 신학적으로 신뢰할 만한 추천 주석(Ligonier Ministries·Keith Mathison 선정 목록 기반, WBC·NICOT·NICNT·TOTC·BST·NIVAC·PNTC 등 표준 시리즈 병합)을 제공하는 공용 참고 자료 | 주석 추천·이 본문 주석 뭐 볼까·성경주석추천 |
| [sermon-doctrinal-planner](../skills/sermon-doctrinal-planner) | 성경 본문 또는 설교 주제의 핵심 문장을 입력받아 체계적인 교리설교(doctrinal preaching) 기획안을 자동 생성하는 스킬. 본문 분석·교리적 함의 도출·역사적 교리 정립(니케아·웨스트민스터·하이델베르크 표준 참조)·교리설교 고유의 4단계  | 교리설교·교리설교 기획안·doctrinal sermon |
| [sermon-emotive-writing-coach](../skills/sermon-emotive-writing-coach) | 설득력 있고 감동적인 설교문 작성을 글쓰기 차원에서 돕는 인터랙티브 코칭 스킬. 주제·목차가 어느 정도 잡힌 설교자가 실제 설교문을 쓸 때 (1) 설교문 전체 구조 제안과 서론·본론·결론별 전개 아이디어 제시, (2) 문장·문단·전체 글의 3계층에서  | 감동적인 설교문 써줘·설득력 있는 설교문·설교 글쓰기 코칭 |
| [sermon-expository-daeji](../skills/sermon-expository-daeji) | 강해설교의 3단계 작성법(주제 결정 → 대지 결정 → 대지 채우기)과 우산질문 방법론을 토대로 대지설교(3대지 설교)를 설계·작성·진단하는 스킬. 해돈 로빈슨의 10단계를 3단계로 통합한 실전 모델을 따르며, (1) 본문에서 한 문장 주제 확보(해석→ | 강해설교·대지설교·3대지 |
| [sermon-greek-grammar-machen](../skills/sermon-greek-grammar-machen) | J. G. 메이첸(J. Gresham Machen, 1881–1937)의 표준 교과서 『New Testament Greek for Beginners』(1923, 33강)를 토대로 신약 헬라어 문법을 가르치는 학습 도우미. 알파벳·발음·격(주격·대격·속 |  |
| [sermon-history-culture-geo-context](../skills/sermon-history-culture-geo-context) | 성경 본문의 역사적·문화적·지리적·사회적 배경을 학문적 깊이로 풀어주는 성경 배경 해설 도우미. 고대근동·이스라엘 왕국·바벨론 포로기·페르시아·헬라·로마 제국 시대의 정치 상황, 유대인의 일상 문화·사회 구조·종교 관습, 성경 무대의 지리·기후·교역로 | 성경 배경·역사적 배경·문화적 맥락 |
| [sermon-lloyd-jones-coaching](../skills/sermon-lloyd-jones-coaching) | 마틴 로이드 존스(Martyn Lloyd-Jones, 1899–1981) 'The Doctor'의 명저 『설교와 설교자(Preaching and Preachers, 1971)』를 토대로 설교자를 코칭하는 스킬. MLJ 고유의 강조점인 'Logic on |  |
| [sermon-luther-coaching](../skills/sermon-luther-coaching) | 마틴 루터(Martin Luther, 1483–1546)의 신학과 설교론으로 설교 주제를 잡고 메시지를 깊게 다듬도록 돕는 코칭 스킬. 이신칭의·오직 은혜·오직 성경·만인제사장·두 왕국·법과 복음·노예의지·십자가 신학·은폐된 하나님 등 핵심 신학과 평 | 루터·Luther·마틴 루터 |
| [sermon-multi-bible-version-compare](../skills/sermon-multi-bible-version-compare) | 성경 한 구절을 9개 필수 번역본·종교 문헌으로 다층 비교 분석하는 다중 번역 비교 도우미. 개역개정·NIV·헬라어 원문·히브리어 원문·라틴어 Vulgata·천주교 성경(공동번역/200주년)·기타 한국어 또는 영어 추가 번역 + 코란·탈무드 대응 본문 | 번역본 비교·여러 번역으로 보고 싶다·이 구절 NIV는 어떻게 |
| [sermon-pipeline](../skills/sermon-pipeline) | 설교 사역 전체를 한 구조로 돌리고 싶을 때 쓴다. 설교 이전의 기획(연간·시리즈) → 설교 준비 6단계(본문개론→개요→주해→주제선택→설교문작성→퇴고) → 설교 이후의 활용(프롬프터·발표자료·블로그·유튜브·소그룹·QT)을 서브에이전트로 단계별 실행하고 | /sermon-pipeline·설교 파이프라인·종합 파이프라인 |
| [sermon-planner-52week](../skills/sermon-planner-52week) | 키워드 1개를 입력받아 52주 연간 설교 계획을 자동 생성하는 설교 기획 도우미. 각 주차별로 설교 주제, 핵심 성경구절 5개, 핵심 포인트 3개, 세부 주제 5개, 연관 찬송가 5곡을 제시하며, 절기(부활절/성탄절/맥추감사절 등)와 한국교회 트렌드( | 52주 설교 계획·연간 설교 주제·설교 시리즈 기획 |
| [sermon-prompter](../skills/sermon-prompter) | > 완성된 설교 원고를 강단용 텔레프롬프터(프롬프터) HTML 파일로 출력하는 스킬. 일정한 속도로 화면이 위로 자동 스크롤되며, 스크롤 속도를 조절하는 옵션 버튼(느림·보통·빠름과 미세 ＋/−)을 제공한다. 글꼴 선택(리디바탕·애플고딕), 글자 크기 |  |
| [sermon-qt-original-text-based](../skills/sermon-qt-original-text-based) | 성경 본문을 입력받아 원어 분석 기반의 완성된 큐티(QT)를 자동 생성하는 말씀묵상 도우미. '생명의 삶'·'매일성경' 스타일의 짧은 설교형 큐티를 산출하며, 핵심 구조는 (1) 예화 기반 서론 — 최신 신문기사·시·영화·도서·예화모음을 웹 검색으로  | 큐티 만들어줘·QT 작성·말씀 묵상 |
| [sermon-research](../skills/sermon-research) | Deep research assistant for weekly sermon preparation. Provide a scripture passage, topic, and questions -- get back commentary insights, hi<br>주간 설교 준비용 심층 리서치 도우미. 본문·주제·질문을 주면 주석 통찰, 역사적 배경, 원어 노트, 생각거리를 돌려준다. 리서치 전용 — 개요·설교문 작성은 하지 않는다. |  |
| [sermon-series](../skills/sermon-series) | Plan a multi-week sermon series. Provide a theme or book of the Bible and number of weeks. Get back series title options, weekly breakdown w<br>여러 주에 걸친 설교 시리즈 기획. 주제나 성경 책과 주차 수를 주면 시리즈 제목 후보, 주차별 본문·제목·핵심 아이디어를 돌려준다. |  |
| [sermon-text-analysis-multimethod](../skills/sermon-text-analysis-multimethod) | 성경 본문 한 단위(절·단락·장)를 입력받아 7가지 핵심 분석법(원문 언어·구조·평행 본문·키아스무스·신학·문학·역사문화)을 자동으로 동시 산출하고, 추가 10가지 분석법(문맥적 배경·수사학·사회정치·심리·해석사·신비·묵상·페미니스트·윤리·포스트콜로니 | ○○○ 본문 분석·이 구절 다각도 분석·본문 종합 분석 |
| [sermon-textual-criticism](../skills/sermon-textual-criticism) | 성경 한 구절을 신·구약 주요 고대 사본으로 비교하여 본문비평(textual criticism)적 차이를 분석하는 학술 도우미. 신약은 파피루스(P46·P52·P66·P75)·대문자(uncial) 사본(시내 사본 ℵ·바티칸 사본 B·알렉산드리아 사본  |  |
| [sermon-to-blog](../skills/sermon-to-blog) | Turn a sermon transcript into a readable 800-1200 word blog post. Not a transcript. A standalone article. SEO-friendly title, meta descripti<br>설교 녹취록을 읽기 좋은 800~1200단어 블로그 글로 변환. 단순 녹취가 아닌 독립된 아티클. SEO 친화적 제목, 메타 설명, 웹 서식 본문. |  |
| [sermon-to-youtube](../skills/sermon-to-youtube) | Optimize a sermon video for YouTube. Provide the title and transcript. Get back optimized titles, description with timestamps, tags, thumbna<br>설교 영상 유튜브 최적화. 제목과 녹취록을 주면 최적화된 제목, 타임스탬프 포함 설명, 태그, 썸네일 컨셉, 숏폼 클립 추천을 돌려준다. |  |
| [sermon-toego-revision](../skills/sermon-toego-revision) | 채경락 교수(고려신학대학원)의 『퇴고설교학』(성서유니온선교회, 2013)을 토대로, 1차 완성된 설교문을 '바르고 힘센 설교'로 다듬는 설교 퇴고(推敲) 전문 스킬. 설교학 교수의 관점에서 4대 평가 범주 — ① 본문에 기초한 선명한 주제, ② 전략적 |  |
| [sermon-topic-message-coach](../skills/sermon-topic-message-coach) | 설교 주제 설정과 핵심 전달 메시지 정립이 막힌 설교자를 6단계 대화로 코칭하는 인터랙티브 스킬. 사용자에게 단계별 질문을 던지며 (1) 주제 명확화 → (2) 설교 목적 구체화 → (3) 핵심 전달 메시지 추천 5개 → (4) 메시지 선택과 핵심 단 | 설교 주제를 못 정하겠다·어떻게 시작해야 할지 모르겠다·설교 코칭 |
| [sermon-topic-research-multidisciplinary](../skills/sermon-topic-research-multidisciplinary) | 설교 주제 한 단어(예: "고난", "용서", "정의", "가난", "노동", "결혼", "환경", "AI", "전쟁", "외로움") 또는 한 문장을 입력받아, 11개 학문 분야(사회·기술·산업·경제·환경·정치·국제관계·법·제도·심리·영성)에서 학제간 | 고난·용서·정의 |
