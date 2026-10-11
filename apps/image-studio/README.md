# Image Studio (맥북 로컬 이미지 생성)

맥북 안에서 오픈 이미지 모델 [Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1) 을 돌리는 이미지 스튜디오입니다.
장당 비용이 없고, 사진을 외부 서버에 올리지 않고 편집할 수 있습니다.

[revfactory/qwen-image-studio](https://github.com/revfactory/qwen-image-studio) (MIT, 커밋 b3f93b7) 를 바탕으로 아래를 바꿨습니다.

| 바뀐 점 | 내용 |
| --- | --- |
| 한 번에 설치 | `install.sh` 가 맥 사양(칩·메모리·디스크·도구)을 점검하고, 메모리에 맞춰 설치 방식을 고릅니다 |
| 더블클릭 실행 | `start.command` 를 Finder 에서 더블클릭하면 켜지고 브라우저가 열립니다. 끌 때는 `stop.sh` |
| 사역용 스타일 6종 | 성경 장면 · 설교 배경 · 묵상 카드 · 주보 표지 · 웹툰 초안 · 썸네일 배경 |
| 저메모리 자동 설정 | 통합 메모리 32GB 미만이면 Q4 모델을 받고 첫 화면 기본값을 저메모리 프리셋으로 둡니다 |
| 안전한 기본값 | 안전 필터를 제거한 텍스트 인코더(Heretic 등)의 설치 스크립트를 뺐고, 그런 인코더는 목록에서 숨기며 요청이 와도 기본 인코더로 바꿉니다 |
| Claude Code 연동 | `skills/local-image-studio` 스킬로 "로컬로 그려 줘" 라고 말하면 이 스튜디오로 생성합니다 |

## 필요한 것

| 항목 | 기준 |
| --- | --- |
| 맥 | Apple Silicon(M1~M4), macOS 14 이상 |
| 통합 메모리 | 32GB 이상 권장. 24GB 는 저메모리 모드로 쓸 만하고, 16GB 는 작은 초안 위주로만 가능합니다 |
| 디스크 여유 | 30GB 이상 (모델 약 18GB, 저메모리 모드는 +4.6GB) |
| 인터넷 | 처음 설치할 때 모델을 내려받습니다. 그다음부터는 오프라인으로 씁니다 |

내 맥의 메모리는 화면 왼쪽 위 애플 메뉴 → 이 Mac에 관하여 → "메모리" 항목에서 볼 수 있습니다.

## 설치 (처음 한 번)

터미널을 열고 차례로 실행합니다.

```bash
git clone https://github.com/sk01020432947-oss/claude-code-skills.git
cd claude-code-skills/apps/image-studio
./install.sh --check     # 1. 점검만 (아무것도 설치하지 않음)
./install.sh             # 2. 설치 (모델 다운로드로 30분 이상 걸릴 수 있음)
```

- git·uv·Node.js 가 없으면 Homebrew 로 설치할지 묻습니다. Homebrew 도 없으면 설치 명령을 알려 주고 멈춥니다.
- 중간에 끊겨도 `./install.sh` 를 다시 실행하면 이미 받은 것은 건너뛰고 이어서 진행합니다.

## 사용

1. Finder 에서 `start.command` 를 더블클릭합니다 (또는 터미널에서 `./start.command`).
2. 브라우저에 http://127.0.0.1:3210 이 열립니다. 첫 생성 때 엔진을 켜는 데 1분 안팎 걸립니다.
3. 다 쓰면 `./stop.sh` 로 끕니다. 웹 앱을 꺼도 엔진(ComfyUI)은 백그라운드에 남기 때문에 `stop.sh` 가 둘 다 끕니다.

처음 `start.command` 를 더블클릭할 때 macOS 가 "확인되지 않은 개발자" 경고를 띄우면, 파일을 우클릭 → 열기를 한 번 누르면 됩니다.

### 쓰는 요령

- **작게 여러 장 → 좋은 시드만 크게.** 품질을 "초고속 초안"(약 1분)으로 두고 4장쯤 뽑은 뒤, 마음에 드는 그림을 열어 "설정 불러오기"를 누르고, 시드를 고정한 채 품질만 "표준"(5~6분)으로 바꿔 다시 생성합니다.
- **용도 스타일을 먼저 고릅니다.** 설교 배경·주보 표지·썸네일 배경은 글자 들어갈 자리를 비워 두도록 되어 있습니다. 제목과 성구는 이미지에 넣지 말고 슬라이드나 디자인 도구에서 얹으세요.
- **사진 편집**은 참조 이미지를 끌어다 놓고 "배경을 늦가을로 바꿔 줘"처럼 지시합니다. 사진은 이 맥 밖으로 나가지 않습니다. 사람 얼굴이 있는 사진은 결과를 꼭 확인하세요.
- **메모리가 속도를 좌우합니다.** 생성 중에는 브라우저 탭·영상 편집기 같은 무거운 앱을 닫아 두세요.

### 실측 속도 (원본 저장소, M4 Max 36GB)

| 품질 | 설정 | 한 장 |
| --- | --- | --- |
| 초고속 초안 | 640² 급, 12스텝 | 약 1분 |
| 빠른 초안 | 약 736², 20스텝 | 75~100초 |
| 표준 | 1024², 40스텝 | 5~6분 (스왑이 생기면 8분 이상) |

메모리가 적은 맥은 이보다 느립니다.

## Claude Code 에서 쓰기

`skills/local-image-studio` 를 `~/.claude/skills/` 에 복사하면, 맥의 Claude Code 에서 이렇게 말할 수 있습니다.

```
갈릴리 호숫가 새벽 장면을 설교 배경으로 로컬에서 초안 4장 뽑아 줘
```

스킬이 프롬프트를 다듬어 보여 주고, 초안을 시드별로 뽑아 고르게 한 뒤, 고른 시드만 표준 품질로 다시 만듭니다.
결과는 작업 폴더의 `outputs/studio/` 와 브라우저 갤러리 양쪽에 남고, 시드는 `outputs/studio/seeds.md` 에 기록됩니다.

터미널에서 직접 부를 수도 있습니다.

```bash
python3 ~/.claude/skills/local-image-studio/scripts/studio_generate.py --status
python3 ~/.claude/skills/local-image-studio/scripts/studio_generate.py "들꽃 핀 시골 교회 오솔길" --style devotional --preset turbo --count 4
```

## 폴더 구성

| 경로 | 내용 |
| --- | --- |
| `install.sh` | 맥 사양 점검과 전체 설치 |
| `start.command` / `stop.sh` | 켜기(브라우저 열기) / 끄기 |
| `setup-comfyui.sh` | ComfyUI·노드·가상환경·모델·웹 앱 의존성 구성 (`install.sh` 가 부름) |
| `run-web.sh`, `run-comfyui.sh` | 웹 앱 / ComfyUI 직접 실행 |
| `comfy-generate.py`, `generate.sh` | 터미널 생성 도구 (ComfyUI / mflux) |
| `web/` | 웹 앱 (Next.js 16 + shadcn/ui). 사역용 스타일은 `web/src/lib/presets.ts` |
| `custom_nodes/` | GGUF 인코더에 비전 타워를 붙이는 ComfyUI 보완 모듈 |
| `docs/UPSTREAM-README.md` | 원본 저장소의 상세 설명 (엔진 비교, 옵션, 메모리 안내) |
| `ComfyUI/`, `outputs/`, `web/data/` | 설치 후 생기는 실행 환경·결과·작업 기록. git 에 올라가지 않음 |

## 라이선스

이 폴더의 코드는 MIT 라이선스입니다(원본 저작권 표시는 `LICENSE`). ComfyUI(GPL-3.0), ComfyUI-GGUF(Apache-2.0), mflux(MIT) 와
Qwen-Image-2.1 모델 가중치는 각자의 라이선스를 따릅니다. 교회 출판물이나 유료 콘텐츠에 쓰기 전에 모델 라이선스를 확인하세요.
