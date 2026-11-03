---
name: scribble-cityscape
description: 'Use when the user wants a cityscape / street image drawn in dense chaotic scribble line art — 수천 개의 가는 선을 겹쳐 형태·명암·빛·속도를 만드는 도시 풍경(볼펜 낙서풍, 크로스해칭, 1점 투시, 보색 대비). Triggers "스크리블 도시", "낙서풍 도시", "선으로 그린 도시", "볼펜 도시 그림", "scribble cityscape", "chaotic line art city", "/scribble-cityscape". Not for: 졸라맨 개념 그림(concept-doodle), 사진→캐릭터(character-style-prompts), 일반 사진풍 이미지(media-gen-image).'
---

# scribble-cityscape — 선만 겹친 도시 풍경 1장

장소(+선택: 시간대·팔레트·비율)를 받아 이미지 1장을 만든다. 되묻지 않고 끝까지 간다.
설명서(연습 순서·기법 대응표): `~/Desktop/cysjavis/매뉴얼/영상_이미지도구/스크리블도시화_연습순서와프롬프트.md`

## 절차

### 1. 장면 설계
- **장소·랜드마크**: 사용자가 준 도시/거리. 없으면 이름 없는 도심 대로.
- **시간대**: 기본 dusk(해질녘). 불빛이 있어야 기법이 산다.
- **주인공 건물 1개 + 보조 요소 2~3개**(차량 불빛·전선·간판·인파·택시).
- **팔레트**: 아래 프리셋에서 장면에 맞게 고른다. 기본 `dusk-burst`.
- **비율**: 기본 세로 3:4(올려다보는 로우 앵글에 유리). 가로 요청이면 16:9.

### 2. 프롬프트 조립 (영어, 스타일 블록 고정)

```
A {place} street scene at {time}, viewed from the middle of the road at low eye level.
{hero building} towering on {position}, {2-3 supporting elements}.
Style: dense chaotic scribble line art, thousands of thin uniform-width pen strokes,
form built only from overlapping lines (no filled areas, no paint),
vertical hatching for buildings, cross-hatching for shadows,
radiating speed lines on the road converging to a single vanishing point,
tangled loose scribbles in the sky that fray and thin out toward the edges,
limited palette of {palette}, colors mixed only by layering strokes on white paper,
glowing lights made of clustered short warm strokes, white paper left showing as highlights,
dramatic low-angle one-point perspective, energetic, digital ballpoint-pen drawing.
{variant line}
No text, no signature, no watermark, no smooth gradients, no photorealism, no 3D render.
```

| 프리셋 | {palette} | {variant line} |
|---|---|---|
| blue-mono | deep navy blue and grey with tiny amber dots | (없음) |
| red-tower | crimson red and steel blue with taxi yellow | (없음) |
| wire-street | black ink, burnt orange road, pale yellow | Dozens of tangled power lines crossing the sky from a wooden utility pole. |
| night-market | indigo, neon orange, magenta | Crowds and glowing shop signs rendered as short scribbles. |
| grid-skyline | brick red, rose, cream white | Buildings drawn as a rigid grid of horizontal and vertical lines, frontal skyline view. |
| swirl-sky | cyan, violet, molten orange | The sky is a huge swirling vortex of curved strokes. |
| dusk-burst | navy, rust red, golden orange | Light bursts from the street center as an explosion of orange strokes. |

**금지**: 프롬프트에 생존 작가 이름("in the style of …")을 넣지 않는다. 기법만 묘사한다.

### 3. 렌더
산출 폴더: `~/Desktop/cysjavis/이미지/스크리블도시/` (없으면 만든다). 파일명 `<영문slug>_<프리셋>.png`.

1순위 codex(무료, concept-doodle과 같은 방식):
```
codex exec --sandbox workspace-write --skip-git-repo-check -o <로그.md> \
  "Using the image_generation tool, create ONE {비율} image. {한 줄로 편 프롬프트}. Save to ./<slug>.png"
```
codex 샌드박스는 작업 폴더 밖에 못 쓴다 → 렌더 후 `ls -dt ~/.codex/generated_images/*/ | head -1` 폴더의 최신 PNG를 산출 폴더로 `cp`.

2순위 `qwen-local-image`(무료·오프라인, 640×896 초안 → 확정). 3순위 `media-gen-image`(유료, 비용 확인 절차 따름).

### 3-B. 기존 이미지(사진·포스터·카드)를 변환할 때
1. webp 등은 `sips -s format png`로 PNG 변환.
2. codex에 원본 첨부: `codex exec ... -i src.png "Using the image_generation tool, edit the attached image ... keeping the exact same composition ..."` + 장면 묘사 + 스타일 블록. 원본의 **글자 자리는 비워 두라**고 지시한다(이미지 모델은 한글 손글씨를 망가뜨린다).
3. 글자는 원본 픽셀을 그대로 되살린다(Pillow — 없으면 스크래치패드에 `python3 -m venv venv && venv/bin/pip install pillow numpy`):
   - 밝은 바탕 위 글자: 바탕색과의 색 거리 마스크(경계 −18, 폭 40)로 원본 글자만 붙인다. 원본 테두리·바닥선 그림자 행은 마스크에서 뺀다.
   - 어두운 사진 위 흰 글자: 글자 상자 안 밝기 마스크로 붙이고, 뒤 배경을 0.3배로 어둡게 한 번진 후광을 깔아 판독성을 지킨다.
   - 생성 비율이 원본과 다르면(3:4 등) 원본 폭에 맞춰 늘리고, 그림과 글자 사이 기준선(지면선 등)을 맞춰 세로 오프셋을 정한다.

### 4. 검수 (Read로 이미지를 직접 본다)
- 면이 칠해졌거나 사진처럼 매끈하면 → `Every surface must be made of visible individual pen strokes.` 추가 후 1회 재생성.
- 소실점이 2개거나 앵글이 높으면 → `single vanishing point at the center of the road, camera at knee height` 강조.
- 글자·서명이 생겼으면 → no-text 줄을 맨 앞으로 옮겨 재생성.
- 재생성은 최대 2회. 그래도 안 되면 결과와 남은 문제를 보고한다.
