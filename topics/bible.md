# 성경 연구·묵상 (6개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/bible.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-bible && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-bible && cd /tmp/ccs-bible && git sparse-checkout set skills/bible-study-lesson-plan skills/pauline-law-hermeneutics skills/pbs-easy-study skills/pbs-graduate-study skills/pbs-personal-bible-study skills/romans-meditation-study && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [bible-study-lesson-plan](../skills/bible-study-lesson-plan) | 활동이 아니라 본문이 먼저인 60분 성경공부 교안(도입5-관찰15-해석15-적용15-기도10)을 설계하는 보조 스킬. 교사가 확정한 8개 입력(본문 범위·번역본, 앞뒤 문맥 2문장, 교사가 직접 관찰한 3가지, 본문 핵심 주장 1문장, 하나님이 하신  | 성경공부 교안·성경공부 교재/커리큘럼·60분 성경공부 |
| [pauline-law-hermeneutics](../skills/pauline-law-hermeneutics) | 이진섭 교수의 「바울과 율법」(Canon & Culture 5/2, 2011)·「'새 관점'과 '옛 관점'」(성경과 교회 9/1, 2011)과 박사논문("The Law of Faith in Romans", Brunel 2006)에 기반한 율법 해석·적 | 바울과 율법·'새 관점'과 '옛 관점'·The Law of Faith in Romans |
| [pbs-easy-study](../skills/pbs-easy-study) | 이재천 저 『개인성경연구핸드북』(IVP)의 PBS(Personal Bible Study) 방법론을 짧은 시간 안에 부담 없이 실천하도록 돕는 간편 코칭 스킬. 관찰(개관→탐색→흐름정리) → 해석(배경→내용전개→핵심메시지) → 적용(적용상황분석→적용점정 | 개인성경연구·PBS·관찰 해석 적용 |
| [pbs-graduate-study](../skills/pbs-graduate-study) | 이재천 저 『개인성경연구핸드북』(IVP)의 PBS(Personal Bible Study) 방법론을 신대원 주해 세미나 수준으로 전체 구현한 심화 코칭 스킬. 문예적-역사적-신학적 해석 원리, 귀납법/연역법을 절충한 "관찰-해석-적용" 해석학적 틀, 성 | 관찰-해석-적용·대학원 수준 성경연구·정식으로 제대로 |
| [pbs-personal-bible-study](../skills/pbs-personal-bible-study) | 이용세 『개인성경연구』(PBS, 성서유니온)의 귀납적 방법으로 성경 본문을 5단계(외부관찰→내부관찰→객관적 해석→적용적 해석→적용)로 직접 연구해 연구노트를 완성하도록 돕는 코칭 스킬. 단계별 관찰·해석·적용 방법(해석 원리, 적용 원리와 잘못된 적용 | 개인성경연구·PBS·귀납적 성경연구 |
| [romans-meditation-study](../skills/romans-meditation-study) | 라종렬 편저 《묵상을 위한 로마서 주해》(대구부광교회)와 이진섭 교수(에스라성경대학원대학교 신약학)의 ''믿음의 법''(νόμος πίστεως) 신학 체계를 기반으로, 로마서(및 갈라디아서) 본문의 묵상 주해·설교 준비·본문 분석을 수행하는 전문 스 | 로마서 묵상·로마서 주해·로마서 ○장 분석/설교 |
