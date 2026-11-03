---
name: voicebox-local-tts
description: 로컬 음성 스튜디오 Voicebox(jamiepine/voicebox)를 REST·MCP로 부려 한국어 TTS·내 목소리 클론 낭독·Whisper 전사·에이전트 음성 알림을 처리한다. ElevenLabs의 무료·오프라인 대안. "voicebox / 로컬 TTS / 내 목소리로 읽어줘 / 무료 음성 합성 / 녹음 전사 / 작업 끝나면 말로 알려줘" 트리거, 또는 voice-clone-elevenlabs 대신 로컬 백엔드를 쓸 때.
---

# voicebox-local-tts

Voicebox 데스크톱 앱이 띄우는 로컬 서버(`http://127.0.0.1:17493`)를 호출한다. 모델·음성·녹음이 맥 밖으로 나가지 않는다.
상세 매뉴얼: `~/Desktop/cysjavis/매뉴얼/AI도구/Voicebox_로컬음성스튜디오_매뉴얼.html`

## 0. 게이트 (매번)

1. **서버 확인**: `curl -s http://127.0.0.1:17493/health` — 실패하면 "Voicebox 앱을 먼저 실행하세요"라고 말하고 멈춘다. 앱 설치·모델 다운로드는 사용자가 한다.
2. **음성 권리 확인**: 클론 대상이 사용자 본인 목소리이거나 화자의 명시적 동의가 있는가. 아니면 멈춘다(RESPONSIBLE_USE.md). 고인·유명인·교인 목소리를 동의 없이 클론하지 않는다.
3. **공개 배포물은 AI 음성 고지**를 붙이도록 안내한다.

## 1. 한국어 기본값

| 목적 | engine | 비고 |
|---|---|---|
| 내 목소리 클론 낭독 | `qwen` (1.7B) | `language: "ko"`, `instruct`로 "천천히, 차분하게" 지시 가능 |
| 샘플 없이 한국어 | `qwen_custom_voice` | 프리셋 `Sohee`(따뜻한 한국어 여성) |
| 23개 언어 번역 낭독 | `chatterbox` | 다국어 |
| `[laugh]` 등 감정 태그 | `chatterbox_turbo` | **영어 전용** — 한국어에 쓰지 않는다 |

## 2. 레시피

```bash
B=http://127.0.0.1:17493
curl -s $B/profiles                       # 프로필 목록(id·name)

# 긴 원고 생성(최대 5만 자, 자동 청킹+크로스페이드)
curl -s -X POST $B/generate -H 'Content-Type: application/json' -d '{
  "profile_id":"<ID>","text":"<원고>","language":"ko","engine":"qwen",
  "instruct":"차분하고 천천히","max_chunk_chars":800,"crossfade_ms":50,"seed":42}'
curl -s $B/generate/<GEN_ID>/status       # 완료까지 폴링
curl -s -o out.wav $B/audio/<GEN_ID>      # 오디오 저장

# 짧은 알림(스피커 재생, 1만 자 한도)
curl -s -X POST $B/speak -H 'Content-Type: application/json' \
  -H 'X-Voicebox-Client-Id: claude-code' -d '{"text":"작업 끝났습니다","profile":"<이름>","language":"ko"}'

# 전사(Whisper)
curl -s -X POST $B/transcribe -F "file=@녹음.m4a" -F "model=turbo"
```

- 같은 시리즈는 `seed`·`engine`·`instruct`를 고정해 음색을 맞춘다.
- 결과 파일은 `~/Desktop/cysjavis/<주제폴더>/`에 한글 이름으로 저장한다.
- 원고 출처가 성경 본문이면 번역본 저작권(개역개정 등)을 확인한다.

> ⚠ v0.5.0: `/transcribe`가 MLX 스레드 오류("no Stream(gpu, N)") 후 서버를 죽일 수 있다. 실패하면 재시도하지 말고 `open -a Voicebox`로 재실행 후 앱 UI 전사를 권한다. 다음 릴리스에서 수정 예정.

## 3. MCP로 쓰기 (선택)

```bash
claude mcp add -s user voicebox --transport http http://127.0.0.1:17493/mcp --header "X-Voicebox-Client-Id: claude-code"
```
도구 4종: `voicebox_speak`, `voicebox_transcribe`, `voicebox_list_captures`, `voicebox_list_profiles`.

## 관련
- `[[voice-clone-elevenlabs]]` — 클라우드 고품질 대안(유료). 파이프라인 정책(청킹·설정 잠금)은 그쪽 것을 따른다.
- `[[youtube-video-pipeline]]` 2단계, `[[sermon-to-youtube]]`, `[[midweek-devotional]]` 낭독본.
