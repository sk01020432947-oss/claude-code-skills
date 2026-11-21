# 특허·지식재산 (11개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/patent.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-patent && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-patent && cd /tmp/ccs-patent && git sparse-checkout set skills/claim-drafting skills/filing-strategy skills/fto-analysis skills/invention-disclosure skills/korean-patent-search skills/patent-orchestrator skills/patent-qa skills/patent-report skills/patentability-analysis skills/prior-art-search skills/spec-drafting && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [claim-drafting](../skills/claim-drafting) | 한국 특허 청구범위 작성·보정 절차. 독립항에 넣을 필수 구성 선정, 종속항 단계 배치, 물건·방법·용도 범주 설계, 한국 청구항 문체('~를 포함하고, ~를 특징으로 하는'), 선행 근거('상기'), 수치 한정과 측정법 연결, 거절 이유에 맞춘 보정 |  |
| [filing-strategy](../skills/filing-strategy) | 특허 출원 전략과 일정 수립 절차. 권리 형태(특허·실용신안·디자인) 선택, 국내·PCT·파리조약 경로와 국가 선택, 우선권·공지예외·심사청구·국내단계 기한 계산, 우선심사 검토, 출원 전 공개 통제와 실시권자 접촉 순서를 날짜가 들어간 일정표와 체크 |  |
| [fto-analysis](../skills/fto-analysis) | 자유실시(FTO)·침해 위험 분석 절차. 존속 중인 특허·실용신안·디자인을 국가별로 추리고, 청구항 구성과 실시 예정 제품을 구성요소 완비 원칙과 균등 요건으로 대비해 위험 등급, 회피 설계, 자유롭게 쓸 수 있는 소멸 기술을 정리한다. FTO 분석, |  |
| [invention-disclosure](../skills/invention-disclosure) | 발명 발굴과 발명신고서(직무발명 신고서) 작성 절차. 아이디어 메모·회의록·기술 문서·기존 조사 보고서에서 기술 과제, 해결 구성, 작동 원리, 효과, 변형 실시 형태를 뽑고, 발명 단위를 나누며, 발명 후보를 재료·구조·공정·용도 축으로 넓힌다. 발 |  |
| [korean-patent-search](../skills/korean-patent-search) | Search Korean patent and utility-model publications through the official KIPRIS Plus Open API with keyword search plus application-number de |  |
| [patent-orchestrator](../skills/patent-orchestrator) | 특허 발굴과 특허 출원 준비를 15개 전문 에이전트로 조율한다. 기존 선행기술 조사 보고서(PDF·Markdown) 검토·정리, 아이디어·기술 문서에서 발명 발굴, 선행기술 조사와 인용 문헌 검증, 신규성·진보성 판단, 자유실시 위험 분석, 발명신고서 |  |
| [patent-qa](../skills/patent-qa) | 특허 출원 서류 형식·일관성 검사 절차. 청구항 번호·종속 관계·다중 종속·선행 근거('상기')·불명확 표현·수치 한정을 스크립트로 검사하고, 명세서의 필수 항목·문단 번호·도면 부호·도면 언급·청구항 용어 뒷받침을 대조하며, 청구항-명세서-도면 대응 |  |
| [patent-report](../skills/patent-report) | 특허 발굴·출원 결과 보고서 편집 절차. 검증 원장, 특허성 판단, 자유실시 분석, 청구항, 모의 심사, 시험 계획, 출원 일정을 모아 의사결정자와 변리사가 읽을 한국어 보고서(기존 보고서 검토 결과, 발굴 결과 요약, 출원 준비 패키지 안내)를 만든 |  |
| [patentability-analysis](../skills/patentability-analysis) | 특허 신규성·진보성 판단 절차와 기준. 발명을 구성 요소로 나누고 선행문헌 대비표(클레임 차트)를 만들어 한국 심사기준(특허법 제29조)으로 신규성·진보성을 판단하고, 심사관 결합 논리와 출원인 반론, 필요한 증거, 후보 간 비교 등급을 정리한다. 특 |  |
| [prior-art-search](../skills/prior-art-search) | 특허 선행기술 검색과 인용 문헌 서지 검증 절차. 키워드·분류코드(IPC/CPC/F-term)·출원인·인용 추적으로 KR·JP·US·CN·EP·WO 문헌을 찾고, Google Patents 원문에서 번호·출원인·날짜·법적 상태·청구항을 스크립트로 가져 |  |
| [spec-drafting](../skills/spec-drafting) | 한국 특허 출원 명세서와 도면 작성 절차. 발명의 명칭, 기술분야, 배경기술, 선행기술문헌, 해결하려는 과제, 과제의 해결 수단, 발명의 효과, 도면의 간단한 설명, 발명을 실시하기 위한 구체적인 내용(실시예·비교예), 부호의 설명, 요약서를 서식 순 |  |
