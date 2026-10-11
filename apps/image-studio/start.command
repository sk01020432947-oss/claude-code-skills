#!/bin/bash
# Image Studio 시작: 웹 앱을 켜고 브라우저를 연다. Finder 에서 더블클릭해도 된다.
# 이미 켜져 있으면 브라우저만 연다. 끄려면 이 창에서 Ctrl+C, 또는 ./stop.sh
cd "$(dirname "$0")"
PORT="${PORT:-3210}"
URL="http://127.0.0.1:$PORT"

if [[ ! -d ComfyUI ]]; then
  echo "아직 설치되지 않았습니다. 먼저 터미널에서 ./install.sh 를 실행하세요."
  read -r -p "엔터를 누르면 창을 닫습니다." _
  exit 1
fi

if curl -fs "$URL/api/status" >/dev/null 2>&1; then
  echo "이미 실행 중입니다: $URL"
  open "$URL"
  exit 0
fi

# 서버가 응답하면 브라우저를 연다 (최대 2분 대기)
(
  for _ in $(seq 1 120); do
    if curl -fs "$URL/api/status" >/dev/null 2>&1; then open "$URL"; exit 0; fi
    sleep 1
  done
) &

echo "Image Studio 를 시작합니다: $URL  (끄려면 Ctrl+C)"
exec ./run-web.sh
