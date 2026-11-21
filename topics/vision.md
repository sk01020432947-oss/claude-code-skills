# 비전 코칭·진단 (28개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/vision.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-vision && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-vision && cd /tmp/ccs-vision && git sparse-checkout set skills/vision-career-recommendation skills/vision-clarity-coaching skills/vision-cys-competence-visioncoding skills/vision-eight-training-areas skills/vision-enneagram-visioncoding skills/vision-financial-3shields-3windows skills/vision-financial-coach skills/vision-five-stages skills/vision-follow-through-habits skills/vision-four-futures skills/vision-future-needs-prediction skills/vision-future-promise-five-criteria skills/vision-futures-timeline-map skills/vision-goal-reframing skills/vision-grill-with-docs skills/vision-mbti-visioncoding skills/vision-mission-frame skills/vision-multipleintel-visioncoding skills/vision-personal-future-research skills/vision-progress-review skills/vision-readiness-visioncoding skills/vision-school-major-info skills/vision-smart-five-competence skills/vision-statement-writer skills/vision-strategy-coach skills/vision-strong-visioncoding skills/vision-three-realm-balance skills/vision-values-visioncoding && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [vision-career-recommendation](../skills/vision-career-recommendation) | 사용자의 *가치 단어·관심사·심리검사 결과(에니어그램·MBTI·다중지능·STRONG/RIASEC) + 나이·학력*을 종합하여 적합한 직업을 4가지 유형으로 각 5개씩 총 20개 추천하는 진로 매칭 스킬. 4유형 분류는 원본 지침 그대로 — ① 미래 직 | 직업 추천·진로 추천·어떤 직업이 좋을까 |
| [vision-clarity-coaching](../skills/vision-clarity-coaching) | 비전이 *막연하거나 막힌* 사용자가 *비전의 핵심*을 한 문장으로 끄집어내도록 돕는 1:1 깊이 코칭 스킬. 소크라테스 산파술(maieutics) 방식으로 답을 가르치지 않고 *질문으로* 사용자가 스스로 비전 핵심에 도달하게 한다. 5단계 깊이 코칭  | 비전이 모르겠어요·내가 뭘 하고 싶은지·비전 명료화 |
| [vision-cys-competence-visioncoding](../skills/vision-cys-competence-visioncoding) | 최윤식 박사가 직접 개발한 *CYS 비전 역량 진단 검사*(『미래준비학교』)를 그대로 구현한 비전 역량 진단 스킬. 박사님의 200여 개 질문 평가지를 토대로 한 *10개 비전 코드 진단* — ① **비전 방향성** ② **비전 가치 방향**(가치 성 | CYS 비전 역량 검사·비전 역량 진단·비전 코드 |
| [vision-eight-training-areas](../skills/vision-eight-training-areas) | 최윤식 박사 『미래준비학교』(2016)의 *비전 훈련 8대 영역*을 그대로 구현한 미래인재 습관 훈련 코칭 스킬. 박사님 인용 *"비전 훈련을 평가하는 기준은 무엇일까? 비전 훈련의 최종 결과물은 무엇일까? 바로 기술의 향상과 습관의 형성이다. 미래준 | 비전 훈련 8대 영역·박사님 SMART Habit·미래인재 습관 |
| [vision-enneagram-visioncoding](../skills/vision-enneagram-visioncoding) | 에니어그램(Enneagram) 9유형의 *핵심 동기(Core Desire)와 핵심 두려움(Core Fear)*을 검사 문항의 중심으로 삼는 자가 진단 스킬. 27문항 카탈로그(각 유형 3문항)를 *층화 무작위 셔플*(블록 A 각 유형 2문항×9=18, | 에니어그램 검사·Enneagram type test·내 에니어그램 유형 |
| [vision-financial-3shields-3windows](../skills/vision-financial-3shields-3windows) | 최윤식 박사 『미래준비학교』(2016) + 『부의 정석』(2011)의 *3개의 방패와 3개의 창* 재정 전략 모델을 그대로 구현한 비전 재정 코칭 스킬. 박사님 고유 모델 — **3개의 방패(자산 보존)**: ① 보험·연금·빚 등 *금융 관련 자산 리 | 박사님 재정 전략·3개 방패 3개 창·자산 리모델링 |
| [vision-financial-coach](../skills/vision-financial-coach) | Dave Ramsey(『The Total Money Makeover』·7 Baby Steps·스노우볼 방식)와 Suze Orman(『The Money Book for the Young, Fabulous & Broke』·"People First, the | People First, then Money, then Things·재정 분석 시작해줘·재정 코칭 |
| [vision-five-stages](../skills/vision-five-stages) | 최윤식 박사 『미래준비학교』(2016)의 *미래준비학교 비전 5단계*를 그대로 구현한 통합 비전 코칭 스킬. 박사님 고유 5단계 — ① **비전 스케치(자기 인식)** — 비전 역량 검사·미래 변화 통찰·가치 정립으로 비전의 *밑그림*을 그림 ② ** | 박사님 5단계·비전 스케치 디자인 훈련 재인식 재생산·미래준비학교 5단계 |
| [vision-follow-through-habits](../skills/vision-follow-through-habits) | 결심·계획이 *습관·일상 시스템*으로 정착하도록 설계하는 실행 지속력 코칭 스킬. BJ Fogg(Tiny Habits, 2019) + James Clear(Atomic Habits, 2018) + Charles Duhigg(The Power of Ha | 습관 설계·작심삼일·실행이 안 돼요 |
| [vision-four-futures](../skills/vision-four-futures) | 최윤식 박사 『미래준비학교』(2016, 지식노마드, ISBN 9788993322972)의 *4가지 미래 가능성*을 그대로 구현한 비전 미래학 코칭 스킬. 박사님 미래학자 본업의 핵심 분류 — ① **Plausible Future (기본미래)** — 발 | 하나의 미래(a Future)·그 미래(the Future)·대안적 미래들(Alternative Futures) |
| [vision-future-needs-prediction](../skills/vision-future-needs-prediction) | 미래 사회 변화로부터 발생할 *잠재적 기회·위기·문제·필요·결핍*을 현실적이고 분석적으로 예측·분해하는 미래필요 예측 전문가 스킬. 사용자가 던진 변화 주제(AGI 도래·인구절벽·기후위기·디지털화폐·통일·고령화·플랫폼 경제 등)를 받아 **3축 분석  | 미래 필요 예측·사회 변화 분석·기회와 위기 |
| [vision-future-promise-five-criteria](../skills/vision-future-promise-five-criteria) | 최윤식 박사 『미래준비학교』(2016)의 *미래 유망성 판단 5가지 기준*을 그대로 구현한 비전 영역 평가 스킬. 박사님이 미래준비학교에서 *비전 영역을 선택*할 때 사용하는 판단 도구로, 사용자가 자신의 관심사·재능 중 *미래에 유망한 것*을 객관적 | * 사용자가·, |
| [vision-futures-timeline-map](../skills/vision-futures-timeline-map) | 최윤식 박사 『미래준비학교』(2016)의 *미래지도(Futures Timeline Map)* 작성 도구를 그대로 구현한 비전 코칭 스킬. 박사님 미래학자 본업의 시그니처 도구로, 사용자가 자신의 비전 영역에 대한 *맞춤 미래지도*를 작성하도록 코칭한다 | * 사용자가·, |
| [vision-goal-reframing](../skills/vision-goal-reframing) | 사용자의 *영감·꿈·소망*을 측정 가능한 *현실 목표*로 변환하는 워크북 스킬. 명료해진 비전 한 문장(vision-clarity-coaching 산출물 또는 사용자 입력)을 받아 SMART 원칙 + Backcasting + OKR 3가지 검증된 프레 | 꿈을 목표로·영감 변환·SMART 목표 |
| [vision-grill-with-docs](../skills/vision-grill-with-docs) | **vision 시리즈 *마스터 진입 스킬*** + 미래비전코칭의 모든 단계에서 사용자가 난관에 부딪히거나 생각이 정리되지 않을 때 호출하는 *다목적 인터뷰 엔진* 스킬. 박사님 28개 vision 스킬의 *cross-stage 진입로* — 사용자가  | 비전 grill·비전 인터뷰·내 비전 무너뜨려봐 |
| [vision-mbti-visioncoding](../skills/vision-mbti-visioncoding) | MBTI 전문가·심리측정학자 페르소나로 사용자가 자신의 MBTI 16유형을 발견하도록 돕는 자가 진단 스킬. 4축(E/I 외향-내향, S/N 감각-직관, T/F 사고-감정, J/P 판단-인식) 각 5문항씩 총 20문항을 *순차 제시*하고 사용자 응답을 | MBTI 검사·MBTI 진단·내 MBTI 찾기 |
| [vision-mission-frame](../skills/vision-mission-frame) | 최윤식 박사 『미래준비학교』(2016)의 핵심 도식 *비전 프레임(Mission Frame)*을 단독 도구로 구현한 비전 코칭 스킬. 비전이 자라기 위해 필요한 2개의 중심축 — ① **영적 직관력(Spiritual Intuition)** = 영감(D | 가치 있는·시대적·소명 |
| [vision-multipleintel-visioncoding](../skills/vision-multipleintel-visioncoding) | Howard Gardner의 다중지능 이론(Theory of Multiple Intelligences, 1983 『Frames of Mind』 + 1995 자연친화 추가 + Existential 잠정)을 토대로 9가지 지능 — ① Linguistic( | 다중지능 검사·Multiple Intelligences test·Howard Gardner 검사 |
| [vision-personal-future-research](../skills/vision-personal-future-research) | 사용자의 *Vision Coding 진단 7종 결과*(CYS 비전 역량·MBTI·에니어그램·STRONG/RIASEC·다중지능·가치·준비도)를 입력받아, 그 사용자에게 *직접 연관된 미래 변화*를 최윤식 박사 미래학 프레임의 STEEPS 6영역(Soci | 내 진단 결과를 가지고 미래 변화 정리해줘·나와 연관된 미래 변화 수집·맞춤 미래 자극 |
| [vision-progress-review](../skills/vision-progress-review) | 사용자의 비전·목표·행동 계획 진척을 *주간·월간·분기·연간* 4단위 정기 점검으로 추적·평가·재조정하는 진척 추적 스킬. **결정론 환원** — 날짜 계산·다음 점검 일정 산출·달성률 분류(✓/△/✗)·OKR 점수 분류(0.0-0.3/0.4-0.6/ | 정기 점검·주간/월간/분기 회고·progress review |
| [vision-readiness-visioncoding](../skills/vision-readiness-visioncoding) | 사용자의 *꿈 달성 준비도(Dream Readiness)*를 20문항 자가 진단으로 평가하고 영어 축 막대 그래프로 시각화하는 비전 코칭 스킬. **결정론 환원** — 점수 파싱·범위/누락 검증·능력별 평균·Composite·레벨 매핑·강점/성장 분류 | I am good at [skill]·비전 준비도·꿈 달성 능력 |
| [vision-school-major-info](../skills/vision-school-major-info) | 한국 대학·학과·진로 정보(공공데이터포털 7개 API 통합)와 미국 직업 정보(O*NET)를 *결정론적*으로 조회·매핑·진로 추천에 활용하는 미래비전코칭 데이터 스킬. 박사님 vision-career-recommendation·vision-strong | 한국 대학 검색·전공 정보·이 학과의 관련 직업 |
| [vision-smart-five-competence](../skills/vision-smart-five-competence) | 최윤식 박사 『미래준비학교』(2016)의 *SMART 미래인재 5역량 훈련*을 그대로 구현한 비전 훈련 코칭 스킬. 박사님 고유 5역량 — ① **S**ense(사물·현상에 대한 감각·판단력·통찰을 기르라) — 직관적 통찰력·훈련된 통찰력 ② **M* | SMART 5역량·Sense Method Art Relationship Technology·박사님 SMART 훈련 |
| [vision-statement-writer](../skills/vision-statement-writer) | 최윤식 박사 『최윤식의 미래준비학교』(2016, 지식노마드, ISBN 9788993322972)의 *Vision Statement 비전 선언문* 양식을 그대로 구현한 비전 선언문 작성 코칭 스킬. 박사님 책 양식 빈칸 그대로 채워가는 1:1 코칭 —  | 비전 선언문·Vision Statement·비전 임무 선언 |
| [vision-strategy-coach](../skills/vision-strategy-coach) | 사용자의 *비전(Vision)을 구체적·단계별 행동(Action)*으로 변환하는 통합 전략 코칭 스킬. 전략 계획·코칭 실무에서 널리 통용되는 5단계 흐름을 따른다 — ① **비전의 핵심(Core) 식별** — 표면 욕망과 본질 가치를 분리해 비전을  | 전략 코치·비전을 행동으로·5단계 메소드 |
| [vision-strong-visioncoding](../skills/vision-strong-visioncoding) | STRONG 직업흥미도 검사(Strong Interest Inventory®) 간이 시뮬레이션 스킬. Holland(1959, 1997)의 RIASEC 6유형 모델 기반 — Realistic(현실형 R)·Investigative(탐구형 I)·Artis | STRONG 직업흥미도 검사·직업 흥미 검사·RIASEC 검사 |
| [vision-three-realm-balance](../skills/vision-three-realm-balance) | 최윤식 박사 『미래준비학교』(2016)의 *비전 영역 3겹 다이어그램*을 그대로 구현한 비전 건강도 점검 스킬. 박사님 책 다이어그램의 3개 원이 교집합을 이루는 핵심 — ① **나만 기쁘게 함 = 개인 욕망** (한 영역만 극대화 시 자기중심·이기적 | 비전 영역 3겹·3영역 교집합·박사님 비전 다이어그램 |
| [vision-values-visioncoding](../skills/vision-values-visioncoding) | 사용자의 MBTI 16유형·에니어그램 9유형·다중지능(Multiple Intelligences) 8지능 결과를 *가치 단어(value words)*에 매핑하여 사용자가 본능적으로 추구하는 *비전 가치 프로파일*을 도출하는 통합 가치 검사 스킬. 가치  | 비전 가치 검사·내 핵심 가치·MBTI·에니어그램·다중지능 통합 |
