# 모션그래픽·애니메이션 (22개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/motion.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-motion && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-motion && cd /tmp/ccs-motion && git sparse-checkout set skills/aimotion skills/animate skills/claude-animation-base skills/claude-motion-studio skills/design-to-motion skills/explainer-default skills/explainer-engaging skills/explainer-high-energy skills/manim-video skills/mg-styles-15 skills/motion-broll skills/motion-design skills/motion-order-sheet skills/motion-tone-qa skills/motion-video-production skills/opus-motion-playbook skills/raea skills/raea-bevy skills/remotion skills/remotion-kr skills/stick-scene skills/vox-paper-motion && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [aimotion](../skills/aimotion) | 웹 그래픽 표현 기법 참고서 aimotion — 기법 하나당 데모 하나, 데모 166편의 구현 노트와 소스와 그림이 이 스킬 안에 모두 들어 있다. 장면에 맞는 기법을 찾아 원리와 소스를 읽고 지금 만드는 영상에 옮긴다. Use when buildin |  |
| [animate](../skills/animate) | UI에 자연스러운 애니메이션·마이크로 인터랙션을 붙이는 스킬. 사용자가 "애니메이션 넣어줘", "호버 효과", "부드럽게 움직이게", "마이크로 인터랙션", "페이지 전환", "스크롤 등장", "Framer Motion", "GSAP", "이징", " | 애니메이션 넣어줘·호버 효과·부드럽게 움직이게 |
| [claude-animation-base](../skills/claude-animation-base) | ClaudeAnimationBase 키트로 p5.js와 p5.brush를 써서 손으로 칠한 듯한 수채화풍 캐릭터 단편 영상을 만든다. 기본 캐릭터는 Clawd이고 다른 캐릭터로 바꿀 수 있다. 사용자가 "/claude-animation-base", " | /claude-animation-base·Clawd 애니메이션·p5.brush 영상 |
| [claude-motion-studio](../skills/claude-motion-studio) | 편집 프로그램 없이 Claude가 코드(HTML+GSAP)로 모션그래픽 영상을 만드는 작업대. 입력 5종(대사+초 / 참고 영상 / 음악 / 나레이션+이미지 / 광고 브리프·웹사이트)과 프롬프트 사다리(한 문장 → 4블록 구조 프롬프트 → 스타일 팩  | 모션그래픽 만들어줘·대사에 맞춰 모션·음악에 맞춰 모션 |
| [design-to-motion](../skills/design-to-motion) | Turns a static design (a Figma frame, dashboard, card set, app screen, or a UI on a photo background) into a pixel exact HTML replica that l | animate this\ |
| [explainer-default](../skills/explainer-default) | Make a clean 45–90 second product demo video for any software product, rendered from code to MP4 with music. Airy light canvas, short centre | how it works |
| [explainer-engaging](../skills/explainer-engaging) | Make a 10–30 second continuous-shot explainer for any product, rendered from code to MP4 with sound. One hero element (a ball, a cursor, a f |  |
| [explainer-high-energy](../skills/explainer-high-energy) | Make a 12–20 second high-energy motion-graphics promo for any product, rendered from code to MP4 with synthesised music. Fast beat-locked sc |  |
| [manim-video](../skills/manim-video) | Production pipeline for mathematical and technical animations using Manim Community Edition. Creates 3Blue1Brown-style explainer videos, alg |  |
| [mg-styles-15](../skills/mg-styles-15) | mg-styles-15 저장소의 15가지 스타일 프롬프트로 코드만 써서 약 10초 모션 디자인 영상을 만든다. 플랫 벡터, 라인 아트, 아이소메트릭, 3D, 셀 애니메이션, 콜라주, 리퀴드, 모프, 바우하우스, 신스웨이브, 오로라 글래스, 예능 자막, | /mg-styles-15·mg-styles |
| [motion-broll](../skills/motion-broll) | Turn a talking-head video and its transcript into motion-graphic B-roll timed to the speaker's words, in a continuous one-shape style (one e |  |
| [motion-design](../skills/motion-design) | Code-only motion design pipeline (no After Effects) for Raphaël / Howseen: launch films, showreels, product promos, LinkedIn/X videos, meme  | remake this video\·make a 15s motion graphics video…\ |
| [motion-order-sheet](../skills/motion-order-sheet) | 모션그래픽 "주문서"(촬영대본식 영상 생성 프롬프트)를 쓰는 스킬. 내 내용을 넣어 장면 순서·초 단위 타이밍·움직임·모양·색·금지 조건까지 적은 '자세히' 프롬프트를 만들고, 참고 영상(URL·파일)을 역분석해 같은 스타일의 프롬프트로 바꾼다. 결과 | 주문서·모션 주문서·키네틱 타이포 프롬프트 |
| [motion-tone-qa](../skills/motion-tone-qa) | 코드로 만든 모션 영상을 "톤 카드 + 숫자 검수"로 출고 전에 재는 스킬. 참고 영상 몇 편을 재서 톤 카드(밝기·컷 간격·움직임·정지 허용·음량 목표)를 저장하고, 결과물을 같은 자로 재서 PASS/FIX를 낸다. 1초 넘는 정지, 대본에 없는 숫 | 톤 카드 + 숫자 검수·톤 카드 / 숫자 검수 / 톤 측정 / 영상 수치 검사 / 컷 속도 확인 |
| [motion-video-production](../skills/motion-video-production) | Plan and assemble 30–90 second motion graphics and character videos with six production stages, media gates, and visual review. Use for vide |  |
| [opus-motion-playbook](../skills/opus-motion-playbook) | Claude Opus 5.5로 모션그래픽을 만드는 원리 74개 플레이북. 프로젝트 지침 8섹션(고정 규칙/변수 분리·제작 전 검증 관문), 박자 계층(128BPM 8마디=15초, 강박·박·8분·16분·히트), seek(t) 렌더 공학(순수함수·닫힌형  | 모션그래픽 원리·오퍼스 모션·박자에 맞춰 |
| [raea](../skills/raea) | Make video, motion graphics, games and 3D scenes with raea, the Render Anything Engine, by writing React/TypeScript compositions with raea a |  |
| [raea-bevy](../skills/raea-bevy) | Writing 3D scenes and 3D games in raea's TypeScript SDK (raea/3d), which Bevy 0.20 draws, and extending that SDK. Use when writing or fixing |  |
| [remotion](../skills/remotion) | React 기반 Remotion 영상 제작 모범 사례 — 컴포지션, 시퀀스, 애니메이션, 타이밍, 렌더링. Remotion 영상을 만들거나 리뷰·디버깅할 때 사용. |  |
| [remotion-kr](../skills/remotion-kr) | 공식 Remotion 스킬(remotion-best-practices 등 12종)을 보완하는 한국어 로컬 보강. 한국어 예제 갤러리 44개 지도·Pretendard 고정·"참고 코드 + :: 정확 명령" 요청 틀, 그리고 공식 스킬에 없는 차트·텍스트 | 참고 코드 + :: 정확 명령 |
| [stick-scene](../skills/stick-scene) | Make small hand-drawn stick-figure scenes for landing pages and sites, where a stick figure works a machine or prop that shows what a produc | worker·crew·like the stick figures on my story page |
| [vox-paper-motion](../skills/vox-paper-motion) | Vox식 종이 콜라주 모션그래픽(찢어진 종이·4색 팔레트·주인공 강조·신문 조각·2.5D 패럴랙스·점선 항로·지도 기울이기·망점 마감)을 "이미지는 AI로 몇 장, 영상은 코드로 조립"하는 방식으로 만든다. 원리 60여 개(영상 출처+확장)와 도감 2 | 이미지는 AI로 몇 장, 영상은 코드로 조립·Vox 스타일·복스 스타일 |
