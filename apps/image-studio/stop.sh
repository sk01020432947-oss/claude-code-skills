#!/bin/bash
# Image Studio 종료: 웹 앱(3210)과 웹 앱이 자동으로 켠 ComfyUI(8188)를 모두 끈다.
# 생성 중인 작업은 다음에 켤 때 실패로 표시되며, 갤러리의 "같은 시드로 재생성"으로 다시 만들 수 있다.
PORT="${PORT:-3210}"
stopped=0
for port in "$PORT" 8188; do
  pids="$(lsof -ti "tcp:$port" -sTCP:LISTEN 2>/dev/null || true)"
  if [[ -n "$pids" ]]; then
    kill $pids 2>/dev/null && echo "종료: 포트 $port (PID $pids)" && stopped=1
  fi
done
pkill -f "ComfyUI/main.py" 2>/dev/null && stopped=1
(( stopped )) || echo "실행 중인 Image Studio 가 없습니다."
