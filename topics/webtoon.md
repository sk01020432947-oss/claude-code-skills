# 웹툰 제작 (7개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/webtoon.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-webtoon && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-webtoon && cd /tmp/ccs-webtoon && git sparse-checkout set skills/insta-toon skills/webtoon-assembly skills/webtoon-orchestrator skills/webtoon-panel-breakdown skills/webtoon-panel-render skills/webtoon-scenario skills/webtoon-trend-research && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [insta-toon](../skills/insta-toon) | 어떤 글이든(설교·묵상·강의·아이디어·기록) 1~4컷 인스타툰(4:5)으로 변환하는 스킬. 말풍선과 한글 대사를 이미지에 함께 굽고(in-image 베이크), 렌더 후 스스로 눈으로 검수해 오탈자·일관성 미달이면 재생성한다. 스타일 앵커 이미지를 주면 | 인스타툰·네컷 만화·카드툰 |
| [webtoon-assembly](../skills/webtoon-assembly) | 웹툰 조립·레터링·검수·패키징 방법론. 렌더된 패널 PNG(말풍선·한글 대사가 이미지에 베이크됨)를 세로 스크롤 뷰어(index.html)로 오버레이 없이 조립하고, letterer의 말풍선/레터링 베이크 명세(대사·생각·외침·나레이션)를 설계하며,  |  |
| [webtoon-orchestrator](../skills/webtoon-orchestrator) | 웹툰 제작 에이전트 팀(27명)을 조율하는 메인 오케스트레이터. 인기 웹툰 트렌드 조사 → 대사 위주·고긴장·매 회차 반전 시나리오 작성 → 캐릭터 다각도 레퍼런스 시트를 먼저 렌더 → 회차당 50+ 패널을 말풍선·한글 대사 in-image 베이크로  |  |
| [webtoon-panel-breakdown](../skills/webtoon-panel-breakdown) | 웹툰 대본을 50+ 패널 샷리스트로 분해하고, 작화 스타일 가이드와 캐릭터 일관성 토큰을 정제하는 비주얼 프로덕션 방법론. 패널 분해, 샷리스트, 웹툰 콘티/연출, 세로 스크롤 구성, 카메라 앵글/구도 어휘, 스타일 가이드(스타일 바이블), 캐릭터 시 |  |
| [webtoon-panel-render](../skills/webtoon-panel-render) | 웹툰 패널 이미지를 codex-image(codex exec image_generation)로 동시 5장씩 병렬 렌더링하는 스킬. 패널 렌더 전 캐릭터 다각도 레퍼런스 시트를 먼저 렌더해 일관성 기준을 만들고, 패널 프롬프트 목록(ep{NN}_prom |  |
| [webtoon-scenario](../skills/webtoon-scenario) | 웹툰 시나리오·스토리·대본을 설계/집필할 때 반드시 사용한다. 하이콘셉트/로그라인, 세계관, 캐릭터, 시리즈 아크와 회차 맵, 매 회차 반전 설계와 복선, 긴장 곡선과 클리프행어, 대사 위주 회차 대본, 50+ 패널 비트 분할, 캐릭터 외형 토큰화를  |  |
| [webtoon-trend-research](../skills/webtoon-trend-research) | 웹툰 트렌드 리서치 방법론. 웹툰 트렌드 조사, 인기 웹툰 분석, 장르 동향 파악, 플랫폼 랭킹·연재 구조 조사, 독자층·댓글 반응 분석, 후킹·클리프행어·반전 메커니즘 역설계, 기획 인사이트 브리프 종합을 수행할 때 반드시 사용한다. '웹툰 트렌드  |  |
