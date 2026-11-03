---
name: claude-animation-base
description: ClaudeAnimationBase 키트로 p5.js와 p5.brush를 써서 손으로 칠한 듯한 수채화풍 캐릭터 단편 영상을 만든다. 기본 캐릭터는 Clawd이고 다른 캐릭터로 바꿀 수 있다. 사용자가 "/claude-animation-base", "Clawd 애니메이션", "p5.brush 영상", "손그림 캐릭터 애니메이션"을 말할 때 쓴다.
argument-hint: "[영상 내용과 길이]"
---

# claude-animation-base

키트 원본: `~/DEV/ClaudeAnimationBase`. 원본은 고치지 않고 복사본에서 작업한다.

## 만들기

1. 복사본을 만든다.
   ```bash
   W="$HOME/Desktop/cysjavis/모션영상/<한글 작품명>"
   mkdir -p "$W" && rsync -a --exclude .git --exclude node_modules --exclude out ~/DEV/ClaudeAnimationBase/ "$W/"
   cd "$W" && npm install
   ```
2. `ANIMATION_GUIDE.md`를 끝까지 읽는다. 제작 규칙, 작업 순서, API가 모두 여기 있다. `docs/emotions.jpg`와 `docs/views.jpg`도 본다.
3. 가이드 순서대로 스토리보드부터 만들고, 장면별로 `src/scenes/`에 작성하며, 길이와 템포는 `src/config.js`에서 정한다. 예시 장면은 `src/scenes/demo.js`.
4. 렌더링하면서 확인한다.
   ```bash
   node render.mjs --sheet=0,1,2,3,4,5 --out=out/sheet.jpg
   node render.mjs --clip --out=out/video.mp4
   ```
5. 보고할 때 `out/video.mp4` 경로를 준다. 미리보기는 `studio.html`을 Chrome으로 연다.

## 필요한 것과 주의

- Node, Google Chrome, ffmpeg.
- 사용자가 요청한 내용이 가이드 규칙과 다르면 사용자 요청을 따른다(가이드도 그렇게 정한다).
- 수채화 채우기는 GPU가 없으면 프레임당 수 초가 걸린다. 너무 느리면 다른 채우기로 바꾸자고 제안한다.
