---
name: analog-diary
description: 어떤 자료든(사진·그림·유튜브·영상·짧은 글·아이디어) 낡은 종이 위 손판화 스탬프 카드로 변환해 일기장 "스쳐가는 일상"에 발행하는 스킬. 카드 하단에 Location/No./Keywords/Year 타자기 메타를 찍고, Documents\analog-diary\diary.html 타임라인에 시간순 등록한다. "그림일기", "아날로그 일기", "스탬프 일기", "판화일기", "일기 카드로 만들어줘" 맥락에서 발동.
---

# analog-diary — 스쳐가는 일상 (구명 판화일기)

어떤 입력이든 **낡은 종이 + 손판화 스탬프 일러스트 + 타자기 메타** 카드 한 장으로 만들어
일기장(diary.html)에 시간순으로 쌓는다. 사용자가 자료만 툭 던져도 끝까지 자동 발행한다.

## 고정 경로

- 일기장 정본: `/Users/kbg1023/Documents\analog-diary\diary.html` (ENTRIES 배열 내장)
- 카드 이미지: `/Users/kbg1023/Documents\analog-diary\cards\YYYY-MM-DD-NN.png`
- 아티팩트 URL: `/Users/kbg1023/Documents\analog-diary\artifact-url.txt` — **재발행 시 이 URL 재사용 필수**

## 화풍 10종 (STYLE 프롬프트 — 항목의 style 키에 따라 선택 주입)

기본은 **watercolor**. 페이지 화풍 선택기(state.style)와 inbox 항목의 style 키가 이 표의
키와 일치한다. 사용자가 대화로 직접 요청할 때도 아래 라벨로 판별한다.

| 키 | 라벨 | 프롬프트 |
|---|---|---|
| watercolor | 수채화 스케치(기본) | Loose travel-journal watercolor sketch: light pencil underdrawing still visible, transparent watercolor washes with soft blooming edges, color bleeding slightly outside the lines, generous white paper margins, warm natural palette, spontaneous and charming urban-sketch feel. |
| woodblock | 판화 | Hand-carved rubber stamp / woodblock print on aged cream paper: rough ink edges with visible carving marks, slightly misregistered color layers like a vintage multi-block print, limited muted palette only (olive green, ochre, faded dusty blue, brick red, ink black), subtle paper grain showing through the ink, flat naive traveler's-journal-stamp look. |
| illust | 일러스트 | Flat modern illustration: clean simplified shapes, minimal detail, soft harmonious palette, subtle grain texture, editorial picture-book charm. |
| comic | 만화 | Korean webtoon/comic panel style: crisp expressive ink outlines, lively faces, screentone-style shading, dynamic but warm composition. |
| character | 캐릭터 | Cute chibi character reinterpretation: big heads and small bodies, simple charming faces, pastel colors, clean simple background, sticker-like appeal. |
| pencil | 색연필 | Colored pencil drawing on textured paper: visible directional strokes and layered hatching, soft warm colors, hand-drawn sketchbook warmth. |
| oil | 유화 | Impressionist oil painting: thick visible brushstrokes, rich light and shadow, vivid but harmonious color, canvas texture. |
| pixel | 픽셀아트 | Retro 16-bit pixel art scene: limited palette, clean dithering, charming video-game composition. |
| miniature | 미니어처 | Isometric miniature diorama illustration: tilt-shift toy-like feel, soft shadows, pastel tones, tiny lovable details. |
| inkpen | 펜화(흑백) | Black ink pen sketch: expressive line work and cross-hatching, no color, energetic sketchbook drawing. |

**공통 접미**(모든 화풍에 항상 덧붙임):
```
Keep the composition and key objects of the reference. Absolutely no text, no
letters, no numbers inside the illustration. Square 1:1, composition fills the frame.
```

메타(Location/Keywords/Year)는 이미지에 굽지 않는다 — 카드 프레임(HTML)이 타자기 폰트로 찍는다.
entries에도 style 키를 기록해 카드 배지에 화풍이 표시되게 한다.

## 절차

1. **입력 판별 → 소스 이미지/장면 확보**
   | 입력 | 처리 |
   |---|---|
   | 사진·그림 파일 | 그대로 소스 이미지로 사용 |
   | 유튜브 URL | `[[watch]]` 스킬로 내용 파악 + 대표 프레임 1장 추출(또는 `yt-dlp --write-thumb`) |
   | 로컬 영상 | `ffmpeg -ss <가장 상징적 시점> -frames:v 1`로 대표 프레임 추출 |
   | 짧은 글·아이디어·기록 | 글에서 **시각적 장면 1개**를 뽑아 장면 묘사문 작성(소스 이미지 없음) |
   여러 장 받으면 장수만큼 카드를 각각 만든다(하루 여러 카드 허용).

2. **스탬프 변환** — 경로 선택(실측 2026-08-28):
   - **기본 경로(검증됨): codex-image** — `FAL_KEY` 미설정 환경에서 작동 확인. 참조 있으면:
     ```
     codex exec --sandbox workspace-write --skip-git-repo-check -i <참조.jpg> -o <log.md> \
       "Using the image_generation tool, create ONE square 1:1 image ... {구도·오브제 서술} ... {STYLE[항목.style] + 공통 접미} ... Save to ./cards/YYYY-MM-DD-NN.png"
     ```
     참조 없으면(글·아이디어) `-i` 생략하고 장면 묘사문 + 선택 화풍 프롬프트. codex 내부 sandbox
     exec가 CreateProcessAsUserW 오류를 내도 node_repl 폴백으로 저장까지 완료됨(로그 오류는 무시 가능).
     결과가 `~/.codex/generated_images/`에만 남으면 직접 복사.
   - 대체 경로: `FAL_KEY`가 설정돼 있으면 `[[media-gen-edit]]`(참조)·`[[media-gen-image]]`(t2i),
     유료 규약(cost-preview-confirm·manifest 체크포인트)은 media-gen 내부 규약.
   - 산출 PNG를 `cards\YYYY-MM-DD-NN.png`로 저장 (NN = 그날의 2자리 순번).

3. **메타 추출 (자동, 질문 금지)**
   - `location`: 내용에서 추정(장소 불명이면 주제어로 대체 — 예: "Kitchen Table", "YouTube · 채널명")
   - `keywords`: 분위기·핵심어 정확히 3개, 소문자, `/` 구분 표시용
   - `date`: 사용자가 말한 날짜 > EXIF/영상 게시일 > 오늘. `year`는 date에서 파생.
   - `no`: diary.html ENTRIES의 최대 no + 1 (전역 일련번호)
   - `note`: 사용자가 글을 줬으면 원문 1~2문장 발췌, 없으면 생략
   - `source`: `photo | video | youtube | text | idea | art`

4. **일기장 등록**
   - 상태는 diary.html의 `<script id="state" type="application/json">` 블록 하나가 단일
     진실원천 — `{entries, inbox, memos}`. entries에 항목 추가:
     ```json
     {"no":7,"date":"2026-08-28","location":"Da Nang, Vietnam","keywords":["blue door","whitewash","together"],"img":"data:image/jpeg;base64,...","source":"photo","note":""}
     ```
   - **img는 data URI로 내장한다**(1200px JPEG q86, 카드당 ~0.5MB) — diary.html 단일 파일로
     완결되어 로컬·아티팩트 계약이 같아진다. 원본 PNG는 `cards\`에 아카이브.
   - 정렬은 뷰어가 date 내림차순으로 처리하므로 append만 하면 된다.
   - 샘플 카드(no:0)는 첫 실제 카드 등록 시 entries에서 제거한다.
   - JSON 안의 `</`는 `<\/`로 이스케이프 유지.

5. **발행**
   - 로컬 정본: img는 `cards/` 상대경로 — 파일로 열면 바로 보임.
   - 아티팩트(가족 공유): scratchpad 사본에서 `cards/*.png`를 base64 data URI로 치환 후,
     `artifact-url.txt`의 기존 URL로 재발행. **`capabilities: {artifact: {}}` 를 함께 선언**
     (페이지의 소스 투입구·멘트 저장이 이 능력에 의존 — 누락 시 입력 UI가 사라짐).
     16MB 초과 시 최신 카드부터 역순으로 담고 초과분은 생략 사실을 사용자에게 보고.
   - 완료 보고: 카드 이미지 + 일기장 링크를 제시.

## 페이지 인박스 자동 정리 (소스 투입구)

페이지 상단 📁/📋/✏로 사용자가 넣은 재료는 `state.inbox`에 저장되고 페이지가 스스로 새
버전을 발행한다(artifact capability). 이 재발행이 세션에 도착하면(재발행 알림, 또는 사용자가
"일기 정리" 언급 시 아티팩트 read로 수동 확인):

1. `Artifact read`로 최신 버전을 받아 `#state` JSON을 추출한다(내 로컬 파일은 뒤처진 상태).
2. inbox 각 항목을 절차 1~4로 카드화한다 — `kind:"image"`(base64)는 파일로 저장 후
   media-gen-edit 경로, `kind:"text"`는 유튜브 URL이면 watch 경로·아니면 t2i 경로.
3. 처리한 항목은 inbox에서 제거, entries에 추가, memos는 그대로 보존.
4. 로컬 diary.html의 `#state`를 병합 갱신 → 절차 5로 재발행(반드시 기존 URL,
   capabilities 유지). 병합 없이 force 금지.

`state.memos`(하단 멘트)는 사용자 기록이므로 삭제·수정 금지. 멘트가 클로드에게 하는 부탁
형태면(예: "이 사진 크게 해줘") 수행 후 결과를 보고한다.

## 자동화 모드

"텍스트만 툭" 들어와도 위 절차를 질문 없이 끝까지 실행한다(자율 완결).
예약 확인이 필요하면 scheduled-tasks로 "매일 인박스 확인 → 카드화"를 제안할 수 있다
(사용자 요청 시에만 생성).
