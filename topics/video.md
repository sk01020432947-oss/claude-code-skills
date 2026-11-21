# 영상·음성·이미지 (49개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/video.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-video && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-video && cd /tmp/ccs-video && git sparse-checkout set skills/audio-post skills/audio-post-mix skills/audio-post-music skills/codex-image skills/cost-preview-confirm skills/explainer-video skills/heygen-avatar-render skills/heygen-avatar-render-api skills/heygen-avatar-render-gate skills/history-shorts-mcp skills/media-gen skills/media-gen-edit skills/media-gen-image skills/media-gen-thumbnail skills/media-gen-upscale skills/media-gen-video skills/object-separation skills/photo-retouch skills/pumasi skills/qwen-local-image skills/rea-video skills/recording-to-series skills/script-writer skills/script-writer-factcheck skills/script-writer-research skills/script-writer-structure skills/script-writer-voice-prep skills/shorts-series skills/slop-feedback-ledger skills/sound-effects skills/suite-runtime-keys skills/video-stitch skills/video-stitch-broll skills/video-stitch-captions skills/video-stitch-compositing skills/video-study-pack skills/video-to-playbook skills/video-verify skills/video-verify-audio-sync skills/video-verify-final-gate skills/video-verify-timing skills/video-verify-visual skills/voice-clone-elevenlabs skills/voice-clone-elevenlabs-chunk skills/voice-clone-elevenlabs-synth-qc skills/voice-gate skills/voicebox-local-tts skills/youtube-video-pipeline skills/youtube-wiki-ingest && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [audio-post](../skills/audio-post) | 영상의 배경음악·효과음을 마련하고 나레이션 아래로 믹싱하는 대표 오디오 포스트 스킬 — 음악 베드 선택/생성과 덕킹·레벨 정규화를 하위 스킬로 오케스트레이션한다. 프로페셔널 영상 감의 핵심 레이어. "배경음악 / 음악 믹스 / 덕킹 / 오디오 포스트  | 배경음악 / 음악 믹스 / 덕킹 / 오디오 포스트 / bgm |
| [audio-post-mix](../skills/audio-post-mix) | 배경음악을 나레이션 아래로 덕킹하고 라우드니스를 정규화하는 하위 스킬 — 사이드체인 덕킹·구간 페이드·유튜브 라우드니스 타깃(약 -14 LUFS)으로 최종 믹스 사양을 만든다. audio-post 믹스 관문. "오디오 믹스 / 덕킹 / 라우드니스 정규 | 오디오 믹스 / 덕킹 / 라우드니스 정규화 / 페이드 |
| [audio-post-music](../skills/audio-post-music) | 영상 톤에 맞는 배경음악 베드를 저작권 안전하게 마련하는 하위 스킬 — 생성 음악(ElevenLabs Music 등)·로열티프리·보유 라이선스 중에서 확보하고 출처·라이선스를 기록한다. audio-post 음악 관문. "배경음악 선택 / 음악 생성 / | 배경음악 선택 / 음악 생성 / 로열티프리 / bgm 소스 |
| [codex-image](../skills/codex-image) | ／ Generate images via Codex CLI's built-in image_gen tool (gpt-image-2). OAuth auth — no API key needed. Codex CLI의 내장 image_gen 도구로 이미지 생성. |  |
| [cost-preview-confirm](../skills/cost-preview-confirm) | 종량제 외부 API(HeyGen 분당·ElevenLabs·fal.ai 초당/장당)를 실행하기 전에 예상 비용을 산출·표시하고 사용자 확인을 받는 공통 규약 스킬. 평판 리스크 옆의 비용 리스크를 막는다. "비용 미리보기 / 사전 비용 확인 / 종량제  |  |
| [explainer-video](../skills/explainer-video) | 유튜브 정보성 해설 영상(바이브랩스 스타일)을 대본+내레이션에서 완성 mp4까지 자동 제작하는 스킬. 대본을 장면으로 분할하고, 내레이션 오디오(본인 녹음 또는 edge-tts)에 whisper로 자막 타이밍을 맞추고, codex-image로 장면 일 |  |
| [heygen-avatar-render](../skills/heygen-avatar-render) | ElevenLabs 나레이션 오디오를 HeyGen Avatar V로 말하는 아바타 영상으로 렌더하는 대표 스킬 — 오디오 자산 업로드, v3 API의 avatar_v 엔진·audio_asset_id 구동, 적격성 확인, 폴링·다운로드·립싱크 QC. " |  |
| [heygen-avatar-render-api](../skills/heygen-avatar-render-api) | HeyGen v3 API로 오디오 구동 아바타 영상을 생성하는 하위 스킬 — 오디오 자산 업로드, POST /v3/videos(engine avatar_v + audio_asset_id), 상태 폴링, 결과 다운로드의 canonical 호출 절차. h |  |
| [heygen-avatar-render-gate](../skills/heygen-avatar-render-gate) | HeyGen 아바타 렌더의 적격성·완결성 게이트 하위 스킬 — 아바타 look의 supported_api_engines로 avatar_v 적격 확인, 렌더 폴링 재시도 정책, 립싱크·길이·완결 QC를 담당한다. heygen-avatar-render 품 | 아바타 적격성 / 렌더 QC / 립싱크 검수 |
| [history-shorts-mcp](../skills/history-shorts-mcp) | 주제 한 줄 → 60~90초 '근거 등급' 역사·성경·지역사 해설 쇼츠를 생성형 영상 커넥터(MCP)로 한 번에 만드는 얇은 오케스트레이터. 사실 장부(A/B/C/X 등급) → 질문형 제목·장면표 → 크레딧 견적 게이트(1회 승인) → 음성 오디션(후 | 신비한 역사 사전? 영상 한번에 힉스필드로 제작! |
| [media-gen](../skills/media-gen) | fal.ai 애그리게이터로 생성형 비주얼을 만드는 대표 스킬 — 텍스트→이미지·참조 편집·이미지→영상(시네마틱 B-roll)·업스케일·썸네일을 하위 스킬로 오케스트레이션한다. 모델을 경로로 지정해 새 모델도 코드 변경 없이 채택. "이미지 생성 / B |  |
| [media-gen-edit](../skills/media-gen-edit) | 참조 이미지를 보존·편집하는 하위 스킬 — 입력 이미지를 URL로 전달해 정체성(얼굴 등)을 유지한 채 편집/합성한다(nano-banana-pro/edit, image_urls 배열). media-gen 편집 관문. "이미지 편집 / 참조 이미지 /  |  |
| [media-gen-image](../skills/media-gen-image) | 텍스트 설명에서 이미지를 생성하는 하위 스킬 — 사용자의 거친 의도를 모델 최적 프롬프트로 재작성한 뒤 fal.ai 이미지 모델(nano-banana-pro 등)로 생성한다. media-gen 이미지 관문. "이미지 생성 / text to image  |  |
| [media-gen-thumbnail](../skills/media-gen-thumbnail) | 유튜브 썸네일을 생성하는 하위 스킬 — 영상 주제·톤에서 클릭을 유도하는 이미지를 생성하고 가독성 높은 텍스트 오버레이를 얹는다(이미지 생성 + 편집 조합). media-gen 썸네일 관문. "썸네일 / 유튜브 썸네일 / thumbnail / 클릭 유 | 썸네일 / 유튜브 썸네일 / thumbnail / 클릭 유도 이미지 |
| [media-gen-upscale](../skills/media-gen-upscale) | 영상·이미지를 고해상도로 업스케일하는 하위 스킬 — fal.ai Topaz 모델로 저해상 클립을 선명하게(배율 기반). 생성 B-roll뿐 아니라 임의 저화질 소스에도 적용. media-gen 업스케일 관문. "업스케일 / 화질 향상 / 해상도 올리기 | 업스케일 / 화질 향상 / 해상도 올리기 / topaz upscale |
| [media-gen-video](../skills/media-gen-video) | 이미지를 시네마틱 영상 클립(B-roll)으로 애니메이트하는 하위 스킬 — fal.ai 영상 모델(Kling·Seedance 등)로 이미지→영상, 초당 종량제라 길이·비용을 정밀 제어한다. media-gen 영상 관문. "이미지를 영상으로 / B-ro |  |
| [object-separation](../skills/object-separation) | Separate a person, product or hand from the background in a video, on the user's own computer with SAM 2. Scans the machine first to pick th |  |
| [photo-retouch](../skills/photo-retouch) | 스튜디오급 사진 보정(리터칭) 워크플로 — 진단(색 균형·노이즈·선명도·조명·구도) → 보정 경로 선택(로컬 무료 vs 생성형) → 실행 → 개선 목록 보고. 스타일 프리셋(내추럴/시네마틱/비비드/미니멀/인물/제품). 사용자가 "사진 보정", "리터칭 | 사진 보정·리터칭·화질 개선 |
| [pumasi](../skills/pumasi) | Codex /imagen으로 이미지 생성 — 모드 자동 감지 + image-studio 프롬프트 + 후처리 금지 가드 인자 없이 실행하면 어떤 이미지를 만들지 묻는다. 트리거: '/pumasi:image', 'Codex로 이미지 만들어줘', 'imag |  |
| [qwen-local-image](../skills/qwen-local-image) | 이 Mac에 설치된 Qwen-Image-2.1(~/DEV/qwen-image-studio)로 이미지를 무료·오프라인 생성/편집한다. 한글 글자가 들어간 포스터·주보 표지·썸네일·슬라이드 배경, 비용 없는 초안, 개인 사진 편집(외부 전송 금지) 맥락에 | 로컬 이미지 / qwen 이미지 / 무료로 이미지 / 한글 포스터 |
| [rea-video](../skills/rea-video) | 逆向拆解一条视频是怎么做出来的——逐镜头判断实拍 / 影视片段 / AI 生成 / 3D 渲染 / 2D 动画 / 定格动画 / 代码模板渲染 / 录屏截图 / 静态图推拉 / 静帧，以及实拍是否经过 AI 加工（换脸、对口型、风格化），标出后期叠加层（逐句字幕时间轴、花字、标题 |  |
| [recording-to-series](../skills/recording-to-series) | 녹화 한 편(설교·강의·라이브·세미나·회의 영상이나 자막)을 받아, 따로 볼 만한 롱폼 N편과 쇼츠 M편을 Claude가 직접 판단해 편성표(제목·원본 구간·첫 문장·시청자가 얻는 것)로 만들고, 모든 구간이 실제 자막 시각과 맞는지·서로 겹치지 않는 | 녹화로 쇼츠 뽑아줘·라이브 한 편으로 몇 편 나와?·설교 영상 클립 나눠줘 |
| [script-writer](../skills/script-writer) | 영상 주제 한 문장 → 사실 기반의 2~4분 유튜브 나레이션 대본을 만드는 대표 스킬. 리서치→구조 설계→사실검증→음성 청크 분절 4단계를 하위 스킬로 오케스트레이션한다. "영상 대본 / 스크립트 작성 / 나레이션 대본 / youtube script" |  |
| [script-writer-factcheck](../skills/script-writer-factcheck) | 완성된 대본의 모든 단정 문장을 출처 대조로 검증하는 하위 스킬 — hallucination-guard 4문(출처 진실성·근거 적합성·논리오류·팩트체크)을 대본에 적용해 무근거 단정을 차단한다. script-writer 5단계·출고 게이트. "대본 팩 | 대본 팩트체크 / 사실 검증 / 환각 차단 |
| [script-writer-research](../skills/script-writer-research) | 영상 대본의 사실 토대를 수집하는 하위 스킬 — 주제에 대해 검색·교차검증으로 검증된 사실과 출처를 모은다. 학습지식 단독 단정 금지. script-writer 1단계. "대본 리서치 / 주제 사실 수집 / 출처 조사" 맥락에서 발동. | 대본 리서치 / 주제 사실 수집 / 출처 조사 |
| [script-writer-structure](../skills/script-writer-structure) | 유튜브 나레이션의 리텐션 구조를 설계하는 하위 스킬 — 훅(0~15초)·본론 세그먼트·CTA를 분량에 맞게 배치하고 각 세그먼트에 시각 큐를 단다. script-writer 2단계. "영상 구조 / 훅 설계 / 리텐션 구성 / 아웃라인" 맥락에서 발동 | 영상 구조 / 훅 설계 / 리텐션 구성 / 아웃라인 |
| [script-writer-voice-prep](../skills/script-writer-voice-prep) | 검증된 대본을 음성 합성용 청크로 분절하는 하위 스킬 — 자연스러운 문장·절 경계에서 쪼개고 연속성 메타(prev/next 텍스트)와 시각 큐를 보존한다. script-writer 6단계, voice-clone-elevenlabs의 입력 생성. "대본 | 대본 청크 분절 / 음성 준비 / 나레이션 분할 |
| [shorts-series](../skills/shorts-series) | Shorts를 한 편씩이 아니라 '시리즈'로 만들고, 시리즈마다 SERIES.md(형식·단계·검사·피드백·발행규칙)와 편별 수정 장부를 두어 '최근 3–4편 무수정이면 자동 발행 후보'를 기계로 판정하는 스킬. 렌더는 HyperFrames/Remoti |  |
| [slop-feedback-ledger](../skills/slop-feedback-ledger) | AI가 만든 시각 결과물(코드형 모션그래픽 푸티지·덱·카드뉴스·광고 소재)을 "AI 슬롭" 기준 12개로 판정하고, 피드백을 "번호·대상·지시·이유(원칙ID)" 한 줄로 써서 프로젝트 원칙장부(원칙장부.md)에 쌓는 스킬. 이유를 함께 주면 같은 문서 | AI 슬롭·번호·대상·지시·이유(원칙ID)·클로드 코드로 감도높은 영상 만드는 법 |
| [sound-effects](../skills/sound-effects) | Add a measured sound pass to a motion-graphics video made with Claude Code (HyperFrames, Remotion, GSAP, Claude Motion or the motion-broll s |  |
| [suite-runtime-keys](../skills/suite-runtime-keys) | 영상 파이프라인 공통 규약 — 외부 서비스 API 키(ElevenLabs·HeyGen 등)를 하드코딩하지 않고 런타임에 받고, 없으면 deny-by-default로 멈춰 정확히 안내하는 패턴. 보급용 배포 전제. "API 키 처리 / BYOK / 런타 | API 키 처리 / BYOK / 런타임 키 / 키 누락 안내 |
| [video-stitch](../skills/video-stitch) | 아바타 클립·HyperFrames 모션그래픽·생성형 B-roll·자막·배경음악을 하나의 완성 영상으로 합성하는 대표 편집 스킬 — 컴포지팅(아바타 항상 노출)·B-roll 배치·자막 번인을 하위 스킬로 오케스트레이션하고 FFmpeg로 마스터 렌더한다. | 영상 합성 / 편집 / 클립 결합 / 컴포지팅 / 자막 |
| [video-stitch-broll](../skills/video-stitch-broll) | media-gen이 생성한 B-roll(이미지·영상 클립)을 편집 타임라인의 적소에 배치하는 하위 스킬 — 시각 큐에 맞춰 삽입하고 아바타 노출 규칙·길이·전환과 충돌 없게 조율한다. video-stitch B-roll 관문. "B-roll 배치 /  | B-roll 배치 / 생성 클립 삽입 / 보조영상 편집 |
| [video-stitch-captions](../skills/video-stitch-captions) | 나레이션 타임스탬프 기반으로 동기 자막을 영상에 번인하는 하위 스킬 — ElevenLabs 문자 정렬(timestamps.json)로 단어 단위 동기, 가독성·세이프영역·아바타 비가림을 보장한다. video-stitch 자막 관문. "자막 번인 / 동 | 자막 번인 / 동기 캡션 / 서브타이틀 / synced captions |
| [video-stitch-compositing](../skills/video-stitch-compositing) | 아바타를 모든 구간에 노출시키는 컴포지팅 하위 스킬 — 좌측 카드 슬라이드인 / 드롭섀도 둥근 크롭 모드, 전환·이징·페이싱을 사람 편집자 수준으로 적용한다. video-stitch 컴포지팅 관문. "아바타 컴포지팅 / 카드 슬라이드인 / 둥근 크롭  | 아바타 컴포지팅 / 카드 슬라이드인 / 둥근 크롭 / 전환 페이싱 |
| [video-study-pack](../skills/video-study-pack) | 유튜브 영상 하나를 '연구·강의 패키지'로 만드는 오케스트레이터. 자막 확보 → 공통골격 → (병렬) 응용가이드 HTML·전문 논고·A5 소책자·강의안(슬라이드+강사노트) → 옵시디언 PKM 저장 → 스킬화 점검 → 웹페이지(아티팩트) 발행까지 한 번 |  |
| [video-to-playbook](../skills/video-to-playbook) | 유튜브 영상 여러 편(또는 1편)을 받아 영상별 노트 → 교차 분석 → 응용·확장 아이디어와 "내게 쓰는 법" → 스킬·설치 점검 → HTML 정본 + 옵시디언 노트 + 자비스 학습지시문까지 한 번에 정리한다. "영상들 정리하고 분석해서 설명서 만들어 | 내게 쓰는 법·영상들 정리하고 분석해서 설명서 만들어줘·응용 아이디어와 사용 실례 |
| [video-verify](../skills/video-verify) | 완성 영상을 업로드 전 시각적으로 검증·승인하는 대표 스킬 — 프레임 추출 후 비전 검수로 시각 품질·모션그래픽 타이밍·오디오 싱크·대본 사실성 4관문을 돌려 전부 GO일 때만 출고한다. "영상 검증 / 시각 검수 / 영상 QA / 업로드 전 확인 / |  |
| [video-verify-audio-sync](../skills/video-verify-audio-sync) | 영상의 오디오 정합을 검증하는 하위 스킬 — 아바타 립싱크가 나레이션과 맞는지, 오디오 끊김·중복·무음 구간이 없는지, 청크 경계가 매끄러운지 판정한다. video-verify 3관문. "오디오 싱크 / 립싱크 검증 / 음성 정합 점검" 맥락에서 발동 | 오디오 싱크 / 립싱크 검증 / 음성 정합 점검 |
| [video-verify-final-gate](../skills/video-verify-final-gate) | 출고 직전 최종 관문 하위 스킬 — 화면 자막·텍스트의 사실성을 대본 사실대장과 재대조하고, 앞 3관문 결과를 종합해 업로드 go/no-go를 판정한다. video-verify 4관문·출고 게이트. "최종 검증 / 사실성 재확인 / 업로드 승인 / g | 최종 검증 / 사실성 재확인 / 업로드 승인 / go no-go |
| [video-verify-timing](../skills/video-verify-timing) | 모션그래픽의 진입·퇴장 타이밍이 나레이션·타임라인과 정확히 맞는지 검증하는 하위 스킬 — 그래픽이 해당 발화 지점에 맞춰 들어오고 나가는지, 너무 이르거나 늦지 않은지 판정한다. video-verify 2관문. "타이밍 검증 / 모션 싱크 / 그래픽  | 타이밍 검증 / 모션 싱크 / 그래픽 진입 점검 |
| [video-verify-visual](../skills/video-verify-visual) | 완성 영상의 시각 품질을 프레임 단위 비전 검수로 판정하는 하위 스킬 — 화면 밖 이탈·요소 겹침·아바타 미노출·잘린 텍스트·미적 결함을 프레임에서 잡는다. video-verify 1관문. "시각 검수 / 프레임 QA / 화면 이탈 점검 / 레이아웃  | 시각 검수 / 프레임 QA / 화면 이탈 점검 / 레이아웃 검증 |
| [voice-clone-elevenlabs](../skills/voice-clone-elevenlabs) | 검증된 대본 청크를 ElevenLabs로 일관된 나레이션 오디오로 합성하는 대표 스킬 — 음성 클론(voice_id) 확보, 글자수 한도 청킹, request stitching 연속성, 잠금된 settings·seed, 문자 타임스탬프까지. "음성 합 | 음성 합성 / 보이스 클론 / 나레이션 / elevenlabs tts |
| [voice-clone-elevenlabs-chunk](../skills/voice-clone-elevenlabs-chunk) | 대본 세그먼트를 ElevenLabs 모델 글자수 한도에 맞춰 확정하고 request stitching 체인(순서·이웃 관계)을 구성하는 하위 스킬. 시간이 아니라 글자수로 자르고 문장 경계를 지킨다. voice-clone-elevenlabs 1단계.  | 음성 청킹 / stitching 체인 / 글자수 분할 |
| [voice-clone-elevenlabs-synth-qc](../skills/voice-clone-elevenlabs-synth-qc) | 청크 계획을 ElevenLabs로 실제 합성하는 하위 스킬 — request stitching(previous_request_ids·prev/next_text), 잠금된 voice_settings·seed로 일관성을 강제하고, with-timestam | 음성 합성 실행 / stitching 합성 / 경계 QC |
| [voice-gate](../skills/voice-gate) | 저자 voice·통찰·문장 패턴 cross-cutting 가드. 모든 단계 마스터 출력에 자동 발동. M1 VoiceScorer 결정론 호출 — LLM 추론 영구 금지. 임계 0.7+ 미달 시 1회 재작성·실패 시 저자 묶음. 저자 진북 #4 (작가성 |  |
| [voicebox-local-tts](../skills/voicebox-local-tts) | 로컬 음성 스튜디오 Voicebox(jamiepine/voicebox)를 REST·MCP로 부려 한국어 TTS·내 목소리 클론 낭독·Whisper 전사·에이전트 음성 알림을 처리한다. ElevenLabs의 무료·오프라인 대안. "voicebox / 로 |  |
| [youtube-video-pipeline](../skills/youtube-video-pipeline) | 주제 한 문장 → 완성된 유튜브 영상(아바타 + 모션그래픽 + 생성형 B-roll + 음악 + 썸네일)을 end-to-end로 자동 제작하는 대표 오케스트레이터 스킬. 대본→음성→아바타→생성형 비주얼→모션그래픽→음악→합성→검증의 기둥을 순서대로 굴린다 |  |
| [youtube-wiki-ingest](../skills/youtube-wiki-ingest) | Ingest YouTube videos (a channel, playlist, or single URL) into an LLM Wiki / Obsidian vault as timestamped raw transcripts plus concept pag |  |
