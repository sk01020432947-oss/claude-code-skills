---
name: recording-to-series
description: 녹화 한 편(설교·강의·라이브·세미나·회의 영상이나 자막)을 받아, 따로 볼 만한 롱폼 N편과 쇼츠 M편을 Claude가 직접 판단해 편성표(제목·원본 구간·첫 문장·시청자가 얻는 것)로 만들고, 모든 구간이 실제 자막 시각과 맞는지·서로 겹치지 않는지 스크립트로 검증한다. "녹화로 쇼츠 뽑아줘", "라이브 한 편으로 몇 편 나와?", "설교 영상 클립 나눠줘", "강의 녹화 편성표", "롱폼 쇼츠 편수 알아서" 요청에 쓴다. 편집·자막·음성·썸네일 자체는 하지 않고 기존 스킬에 넘긴다.
---

# recording-to-series — 녹화 1편 → 롱폼·쇼츠 편성표

2026-10-25 설치. 근거: 커리어해커 알렉스 「영상 하나에 30시간 작업하던 일을 전부 자동화한 방법」(라이브 1편 → 롱폼 5·쇼츠 22). 기존 `source-to-channels`는 쇼츠 **대본**을 새로 쓰고, `sermon-to-youtube`는 메타데이터를 만든다. 이 스킬은 그 앞 단계, **원본 녹화를 실제 타임코드로 쪼개는 편성**만 맡는다.

## 0. 시작 전
- 산출물이 쇼츠·영상이므로 `awesome-ai-motion` 사용 여부를 **한 번만** 묻는다(CLAUDE.md 8번).
- 결과물 폴더: `~/Desktop/cysjavis/<주제폴더>/<녹화이름>_편성/` (한글 이름).

## 1. 자막 확보
- 유튜브: `yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs "ko-orig,ko" --sub-format vtt -o 원본 <URL>`
- 로컬 영상: `whisper-cli`로 VTT 생성(`which whisper-cli`로 확인 후).
- 정리: `python3 ~/.claude/skills/recording-to-series/scripts/series.py clean 원본.ko.vtt 대본.txt --window 30`
  (자동자막의 롤링 중복을 걷어내고 30초 단위 `[hh:mm:ss]` 대본을 만든다.)

## 2. 편성 (편수는 Claude가 정한다)
대본 전체를 읽고 편수를 **직접 판단**한다. 사용자가 편수를 말하지 않았으면 묻지 않는다.

규칙
1. 각 편은 앞뒤 맥락 없이 이해돼야 한다. 대명사("이거", "아까 말한")로 시작하는 구간은 시작점을 당기거나 버린다.
2. 같은 이야기가 두 편에 겹치지 않는다(롱폼끼리, 쇼츠끼리). 쇼츠는 롱폼 구간 안에서 뽑아도 된다.
3. 쇼츠: 30–60초, 첫 3초에 결론이나 질문. 롱폼: 하나의 질문에 하나의 답.
4. 설교·강의는 본문·출처 인용 구간을 자르지 않는다(인용이 중간에 끊기면 의미가 바뀐다).

`편성표.json`으로 저장:
```json
[{"type":"long","title":"…","start":"00:03:10","end":"00:11:40","first_line":"…","gain":"시청자가 얻는 것 한 줄"},
 {"type":"short","title":"…","start":"00:05:02","end":"00:05:48","first_line":"…","gain":"…"}]
```
`first_line`은 자막에 실제로 있는 말 그대로(앞 12자로 대조한다).

## 3. 검증 (통과 전 넘기지 않는다)
```bash
python3 ~/.claude/skills/recording-to-series/scripts/series.py check 편성표.json 원본.ko.vtt
```
범위 밖·겹침·첫 문장 불일치를 고친 뒤 다시 돌려 `OK`가 나와야 한다. 검증 결과를 편성표 옆에 붙인다.

## 4. 넘기기 (집필·편집은 기존 스킬)
| 할 일 | 스킬 |
|---|---|
| 구간 컷·자막 굽기 | `video-use` → `video-stitch-captions` |
| 설교 영상 제목·설명·태그 | `sermon-to-youtube` |
| 썸네일 | `media-gen-thumbnail` |
| 모션그래픽·차트 | `awesome-ai-motion`(동의 시) 또는 `remotion-*` |
| 업로드 전 검수 | `video-verify` |
| 유료 API(ElevenLabs·HeyGen·fal) | `cost-preview-confirm`으로 예상 비용 확인 후 |

## 5. 하지 않는 것
- 업로드·발행·결제(사람 확인 지점).
- 남의 영상을 편성하는 일. 남의 영상은 해설·인터뷰 방식(자기 의견이 중심)으로만 다루고 원본 클립은 짧게.
