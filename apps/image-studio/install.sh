#!/bin/bash
# Image Studio 맥북 설치기
#
# 하는 일:
#   1. 이 맥이 Apple Silicon 인지, 통합 메모리와 디스크 여유가 충분한지 점검한다
#   2. git·uv·Node.js 20+ 가 없으면 Homebrew 로 설치할지 묻는다
#   3. setup-comfyui.sh 로 ComfyUI·모델(약 18GB)·웹 앱 의존성을 구성한다
#      (메모리 32GB 미만이면 Q4 모델을 함께 받고 웹 앱 기본값을 저메모리 프리셋으로 둔다)
#   4. 웹 앱을 빌드하고, Claude Code 스킬이 이 폴더를 찾을 수 있게 ~/.image-studio-root 에 경로를 적는다
#
# 사용법:
#   ./install.sh          # 점검 → 설치
#   ./install.sh --check  # 점검만 하고 끝낸다
#
# 다시 실행해도 안전하다. 이미 된 단계는 건너뛴다.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
CHECK_ONLY=0
[[ "${1:-}" == "--check" ]] && CHECK_ONLY=1

NEED_DISK_GB=30
blue=$'\033[34m'; green=$'\033[32m'; yellow=$'\033[33m'; red=$'\033[31m'; reset=$'\033[0m'
info() { printf '%s▸%s %s\n' "$blue" "$reset" "$*"; }
ok()   { printf '%s✓%s %s\n' "$green" "$reset" "$*"; }
warn() { printf '%s!%s %s\n' "$yellow" "$reset" "$*"; }
fail() { printf '%s✗%s %s\n' "$red" "$reset" "$*" >&2; exit 1; }
ask()  { local reply; read -r -p "$1 [y/N] " reply; [[ "$reply" == "y" || "$reply" == "Y" ]]; }

echo
echo "Image Studio 설치 점검"
echo "────────────────────────"

# ---- 1. 장비 ----
[[ "$(uname -s)" == "Darwin" ]] || fail "macOS 전용입니다. (현재: $(uname -s))"
[[ "$(uname -m)" == "arm64" ]] || fail "Apple Silicon(M1~M4) 맥이 필요합니다. 인텔 맥은 GPU 가속을 쓸 수 없습니다."
CHIP="$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo "Apple Silicon")"
ok "칩: $CHIP"

MACOS="$(sw_vers -productVersion)"
MACOS_MAJOR="${MACOS%%.*}"
(( MACOS_MAJOR >= 14 )) || fail "macOS 14 이상이 필요합니다. (현재: $MACOS)"
ok "macOS $MACOS"

RAM_GB=$(( $(sysctl -n hw.memsize) / 1024 / 1024 / 1024 ))
LOW_MEMORY=0
if (( RAM_GB >= 32 )); then
  ok "통합 메모리 ${RAM_GB}GB: 표준 프리셋으로 씁니다"
elif (( RAM_GB >= 24 )); then
  LOW_MEMORY=1
  warn "통합 메모리 ${RAM_GB}GB: 저메모리 모드(Q4 모델)로 설치합니다. 표준 품질 한 장에 10분 안팎 걸릴 수 있습니다."
elif (( RAM_GB >= 16 )); then
  LOW_MEMORY=1
  warn "통합 메모리 ${RAM_GB}GB: 권장(32GB)의 절반입니다. 스왑이 많아 한 장에 15분 이상 걸리거나 실패할 수 있습니다."
  warn "작은 크기(초고속 초안·빠른 초안)로만 쓰는 것을 전제로 설치합니다."
  if (( ! CHECK_ONLY )); then ask "그래도 설치할까요?" || { echo "설치를 취소했습니다."; exit 0; }; fi
else
  fail "통합 메모리 ${RAM_GB}GB 로는 실행할 수 없습니다. 16GB 이상이 필요합니다."
fi

FREE_GB=$(df -g "$ROOT" | awk 'NR==2 {print $4}')
if (( FREE_GB < NEED_DISK_GB )); then
  fail "디스크 여유 ${FREE_GB}GB. 최소 ${NEED_DISK_GB}GB 가 필요합니다 (모델 약 18~23GB + 실행 환경)."
fi
ok "디스크 여유 ${FREE_GB}GB"

# ---- 2. 도구 ----
missing=()
command -v git >/dev/null 2>&1 || missing+=("git")
command -v uv  >/dev/null 2>&1 || missing+=("uv")
NODE_OK=0
if command -v node >/dev/null 2>&1; then
  NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
  (( NODE_MAJOR >= 20 )) && NODE_OK=1
fi
(( NODE_OK )) || missing+=("node")

if (( ${#missing[@]} == 0 )); then
  ok "도구: git · uv · Node.js $(node -v)"
else
  warn "없는 도구: ${missing[*]}"
fi

if (( CHECK_ONLY )); then
  echo
  if (( ${#missing[@]} )); then
    echo "점검 결과: 설치 가능. ./install.sh 를 실행하면 없는 도구부터 설치합니다."
  else
    echo "점검 결과: 설치 가능. ./install.sh 로 진행하세요."
  fi
  exit 0
fi

if (( ${#missing[@]} )); then
  if ! command -v brew >/dev/null 2>&1; then
    echo
    echo "Homebrew 가 필요합니다. 터미널에 아래 한 줄을 붙여 넣어 설치한 뒤 ./install.sh 를 다시 실행하세요."
    echo '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    exit 1
  fi
  ask "Homebrew 로 ${missing[*]} 를 설치할까요?" || fail "필요한 도구가 없어 중단합니다."
  for tool in "${missing[@]}"; do
    info "brew install $tool"
    brew install "$tool"
  done
  if [[ " ${missing[*]} " == *" node "* ]] && ! node -v >/dev/null 2>&1; then
    fail "Node.js 설치 뒤에도 node 를 찾지 못했습니다. 터미널을 새로 열고 다시 실행하세요."
  fi
fi

# ---- 3. ComfyUI · 모델 · 웹 앱 의존성 ----
echo
info "ComfyUI 와 모델을 구성합니다. 처음에는 약 18GB 를 내려받아 30분 이상 걸릴 수 있습니다."
SETUP_ARGS=()
(( LOW_MEMORY )) && SETUP_ARGS+=("--q4")
zsh "$ROOT/setup-comfyui.sh" ${SETUP_ARGS[@]+"${SETUP_ARGS[@]}"}

# ---- 4. 웹 앱 설정과 빌드 ----
ENV_FILE="$ROOT/web/.env.local"
if (( LOW_MEMORY )); then
  echo "NEXT_PUBLIC_LOW_MEMORY=1" > "$ENV_FILE"
  ok "웹 앱 기본값: 저메모리 프리셋 (web/.env.local)"
else
  rm -f "$ENV_FILE"
fi
info "웹 앱 빌드"
( cd "$ROOT/web" && npm run build >/dev/null ) || fail "웹 앱 빌드에 실패했습니다. web/ 에서 npm run build 를 실행해 오류를 확인하세요."
ok "웹 앱 빌드 완료"

chmod +x "$ROOT/start.command" "$ROOT/stop.sh" "$ROOT/run-web.sh" "$ROOT/run-comfyui.sh" "$ROOT/comfy-generate.py" "$ROOT/generate.sh" 2>/dev/null || true
echo "$ROOT" > "$HOME/.image-studio-root"
ok "Claude Code 스킬용 경로 기록: ~/.image-studio-root"

cat <<GUIDE

설치 완료
  시작: Finder 에서 start.command 를 더블클릭하거나, 터미널에서 ./start.command
        → 브라우저에 http://127.0.0.1:3210 이 열립니다. 첫 생성 때 엔진이 켜지는 데 1분 안팎 걸립니다.
  종료: ./stop.sh
  Claude Code: "로컬로 그려 줘" 처럼 말하면 local-image-studio 스킬이 이 스튜디오로 생성합니다.
GUIDE
