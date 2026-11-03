---
name: qwen-local-image
description: 이 Mac에 설치된 Qwen-Image-2.1(~/DEV/qwen-image-studio)로 이미지를 무료·오프라인 생성/편집한다. 한글 글자가 들어간 포스터·주보 표지·썸네일·슬라이드 배경, 비용 없는 초안, 개인 사진 편집(외부 전송 금지) 맥락에서 발동. "로컬 이미지 / qwen 이미지 / 무료로 이미지 / 한글 포스터" 트리거. 유료 고품질이 필요하면 media-gen-image.
---

# qwen-local-image

로컬 Qwen-Image-2.1(ComfyUI + GGUF Q8_0 + int8 인코더). 비용 0, 파일이 Mac 밖으로 나가지 않는다.
설명서: `~/Desktop/cysjavis/매뉴얼/영상_이미지도구/QwenImageStudio_사용설명서.html`

## 절차

1. **서버 확인** → `curl -s -m 2 127.0.0.1:8188/system_stats`. 꺼져 있으면
   `cd ~/DEV/qwen-image-studio && ./run-comfyui.sh >> comfyui.log 2>&1` 를 백그라운드로 실행하고 응답까지 대기(1분 안팎).
   `~/ComfyUI`(별도 빈 설치)를 켜지 말 것 — 포트 8188 충돌.
2. **프롬프트 재작성** → 주제 → 구도 → 조명 → 스타일 → 글자 순서의 영어 문장. 넣을 글자는 큰따옴표로 정확히(한글 가능, 짧을수록 정확).
3. **초안** → 640×896 / 896×640 / 640² 중 비율에 맞춰 12스텝, 시드 여러 개(M5 Pro 48GB 실측 약 50초/장):
   ```bash
   cd ~/DEV/qwen-image-studio
   python3 comfy-generate.py "<prompt>" --steps 12 --width 640 --height 896 --seed 42 -o outputs/<작업>/draft-42.png
   ```
4. **육안 검증** → Read로 결과를 보고 글자 오탈자·방향 확인. 틀리면 시드를 바꾸거나 글자를 더 짧게.
5. **확정** → 고른 시드로 `--steps 40 --width 1024 --height 1024`(또는 1280×720 등 32의 배수) 재생성. 5분 안팎.

## 편집(참조 이미지)

CLI는 텍스트→이미지만 된다. 편집은 웹 앱 API를 쓴다(`./run-web.sh`, 127.0.0.1:3210):
`POST /api/uploads`(multipart `file`) → 반환 id를 `POST /api/jobs` 의 `params.references: [id]` 에 넣고 prompt에 지시문("배경만 흰 스튜디오로, 인물은 그대로").
결과는 `GET /api/images/{jobId}` 또는 `outputs/web/<jobId>.png`.

## 금지

- Heretic(거부 완화) 인코더를 설치·사용하지 않는다(사용자 명시 요청 없이는).
- mflux와 ComfyUI 동시 실행 금지(둘 다 느려짐).
- 끝나면 메모리 회수가 필요할 때 `pkill -f "ComfyUI/main.py"`.
