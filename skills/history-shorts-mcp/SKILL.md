---
name: history-shorts-mcp
description: "주제 한 줄 → 60~90초 '근거 등급' 역사·성경·지역사 해설 쇼츠를 생성형 영상 커넥터(MCP)로 한 번에 만드는 얇은 오케스트레이터. 사실 장부(A/B/C/X 등급) → 질문형 제목·장면표 → 크레딧 견적 게이트(1회 승인) → 음성 오디션(후보 3개 중 선택) → 장면 생성·나레이션 길이 실측 → ffmpeg 합성 → 컨택트 시트·QA 리포트. 경로는 힉스필드 커넥터(연결 시) → ElevenLabs Creative MCP(creative_*) → media-gen(fal.ai) 순. 출처 - AI 겸임교수 이종범 「신비한 역사 사전? 영상 한번에 힉스필드로 제작!」(2026-10-04, yF-oXXEwI-A). 트리거 - '역사 쇼츠', '신비한 역사 사전', '힉스필드로 영상', '석굴암 영상처럼', '성경 역사 쇼츠', '교회사 1분 영상', '지역사 홍보 영상', '커넥터로 영상 만들어', '드라마 쇼츠', '시니어 사연 쇼츠', '사이다 숏드라마'(→ references/drama-mode.md). 대본 심화는 script-writer, 아바타·롱폼은 youtube-video-pipeline, 출고 전 정밀 검수는 video-verify, 모션 효과 선택은 awesome-ai-motion."
---

# history-shorts-mcp

생성은 커넥터에 맡기고, 이 스킬은 **사실·예산·검수 세 관문**만 지킨다. 원본 영상에서 결과가 좋았던 이유는 모델보다 이 세 가지였다: 나레이션이 "확인되지 않는다"를 말할 줄 알았고, 크레딧 초과 시 장면을 줄였고, 결과물에 컨택트 시트와 QA 리포트를 붙였다.

## 입력 (없으면 기본값으로 진행)
| 항목 | 기본값 |
|---|---|
| 주제 | (필수) |
| 길이 | 75초, 장면 8~10개 |
| 비율 | 9:16 (가로 영상이면 16:9) |
| 대상 | 일반 성인 (교회학교면 어휘 낮춤) |
| 크레딧 상한 | 사용자가 말한 값. 모르면 견적만 내고 승인 받는다 |
| 저장 | `~/Desktop/cysjavis/<주제폴더>/<한글이름>/` |

## 모드
- 해설(기본): 아래 순서.
- 드라마: 대사형 숏드라마. `references/drama-mode.md`의 차이표대로 0단계(트렌드 조사)·인물 카드·화질 두 안·마감 오버레이를 더한다.

## 순서

1. **사실 장부 `사실장부.md`** — 나레이션 문장마다 근거와 등급을 단다.
   - A: 1차 사료·공식 기관(국가유산청, 법령, 성경 본문 장절) · B: 학계 통설·주석 · C: 전승·설화 · X: 확인 못 함
   - X는 지우거나 "기록으로는 확인되지 않는다"로 말한다. C는 "~라고 전한다"로 말한다.
   - 근거 도구: 성경은 `logos-bible-research` MCP·`sermon-history-culture-geo-context`, 법·조례는 `korean-law`·`local-government` MCP, 그 밖은 웹 검색. 심화는 `script-writer-factcheck`.
2. **기획 `기획.md`** — 질문형 제목 3개("~였을까?"), 장면표(장면번호·초·나레이션·화면 묘사·등급). 첫 장면은 질문, 끝 장면은 답 한 문장.
3. **견적 게이트** — 장면별 이미지+영상 비용을 `estimate_only`(ElevenLabs Creative) 또는 서비스 단가로 합산. 상한을 넘으면 장면 수·길이를 줄인 안을 같이 제시하고 **한 번** 승인받는다. 승인 전에는 생성 호출 금지.
4. **음성 오디션** — 첫 두 문장으로 한국어 음성 3개를 만들어 들려주고 사용자가 고른다. 고른 voice_id를 기록.
5. **생성** — 나레이션 전체를 먼저 만들고 `ffprobe`로 길이를 잰 뒤 장면 초를 맞춘다. 장면은 이미지 → 이미지→영상 순(인물·유물 일관성).
6. **합성** — `ffmpeg` concat + 나레이션. 자막이 필요하면 `video-stitch-captions`.
7. **QA** — 컨택트 시트와 `QA리포트.md`(사실장부 대조, 시대착오, 이미지 속 한글 깨짐, 실존 인물 얼굴, 길이).

## 경로 선택
1. 힉스필드 커넥터가 연결돼 있으면 그것(이미지·영상·ElevenLabs 음성이 한곳). 사용자가 claude.ai 설정 → 커넥터에서 연결해야 한다.
2. 아니면 ElevenLabs Creative MCP: `creative_create_flow` → `creative_generate_image` → `creative_generate_video`(connect_from, 모델 예 `bytedance-seedance-v2.5`) → `creative_list_voices`·`creative_generate_speech`. 재시도는 과금이 두 번 되므로 같은 호출을 반복하지 않는다.
3. 둘 다 없으면 `media-gen`(fal.ai) + `voice-clone-elevenlabs` 또는 `voicebox-local-tts`.

## 명령
```bash
# 나레이션 길이(초)
ffprobe -v error -show_entries format=duration -of csv=p=0 narration.mp3
# 장면 이어 붙이기 (list.txt: file 'scene01.mp4' ...)
ffmpeg -f concat -safe 0 -i list.txt -i narration.mp3 -map 0:v -map 1:a -c:v libx264 -c:a aac -shortest final.mp4
# 컨택트 시트: 2초마다 1프레임, 5열
ffmpeg -i final.mp4 -vf "fps=1/2,scale=320:-1,tile=5x8" -frames:v 1 contact_sheet.png
```

## 금지
- 사실장부에 없는 연도·이름·숫자를 나레이션에 넣지 않는다.
- 성경 인물 얼굴 클로즈업, 실존 현대 인물 얼굴 생성은 피한다(실루엣·뒷모습·유물·지도로 대체).
- 통계 수치는 출처 있는 값만. 없으면 화면에 "예시"로 표시.
