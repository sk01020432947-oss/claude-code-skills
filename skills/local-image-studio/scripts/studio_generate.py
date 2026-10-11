#!/usr/bin/env python3
"""맥북의 로컬 Image Studio(apps/image-studio)에 이미지 생성 작업을 넣고 결과 PNG 를 받아 온다.

웹 앱의 대기열 API 를 쓰므로, 여기서 만든 이미지도 브라우저 갤러리에 그대로 쌓인다.
웹 앱이 꺼져 있으면 ~/.image-studio-root 에 적힌 설치 폴더에서 자동으로 켠다.

사용 예:
  studio_generate.py "갈릴리 호숫가의 새벽" --style bible-scene --ratio 16:9 --preset turbo --count 4
  studio_generate.py "..." --preset standard --seed 1234567 --ratio 16:9
  studio_generate.py "배경을 늦가을로 바꿔 줘" --ref photo.jpg --preset draft
  studio_generate.py --status
"""
import argparse
import json
import math
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime
from pathlib import Path

URL = os.environ.get("IMAGE_STUDIO_URL", "http://127.0.0.1:3210").rstrip("/")
ROOT_FILE = Path.home() / ".image-studio-root"

# web/src/lib/presets.ts 의 QUALITY_PRESETS 와 같게 유지한다
PRESETS = {
    "turbo": {"steps": 12, "mp": 0.39, "gguf": "Q8_0", "label": "초고속 초안 (약 1분)"},
    "draft": {"steps": 20, "mp": 0.5, "gguf": "Q8_0", "label": "빠른 초안 (1~2분)"},
    "standard": {"steps": 40, "mp": 1.0, "gguf": "Q8_0", "label": "표준 (5~6분)"},
    "high": {"steps": 40, "mp": 2.25, "gguf": "Q8_0", "label": "고해상도 (15분 이상)"},
    "lowmem": {"steps": 30, "mp": 1.0, "gguf": "Q4_K_M", "label": "저메모리 (Q4)"},
}
GGUF_FILES = {"Q8_0": "qwen-image-2.1-Q8_0.gguf", "Q4_K_M": "qwen-image-2.1-Q4_K_M.gguf"}
TEXT_ENCODER = "qwen3vl_8b_int8_convrot.safetensors"
RATIOS = {"1:1": (1, 1), "16:9": (16, 9), "9:16": (9, 16), "4:3": (4, 3), "3:4": (3, 4),
          "3:2": (3, 2), "2:3": (2, 3), "21:9": (21, 9)}
# web/src/lib/presets.ts 의 STYLE_PRESETS 와 같게 유지한다
STYLES = {
    "none": "",
    "photo": "photorealistic photograph, natural lighting, realistic skin and material texture, shot on a full-frame camera",
    "cinematic": "cinematic still, dramatic lighting, shallow depth of field, anamorphic lens, subtle film grain",
    "illustration": "digital illustration, clean line art, flat shading, vibrant color palette",
    "watercolor": "watercolor painting on textured paper, soft edges, pigment blooms, light washes",
    "3d": "3D render, soft studio lighting, subsurface scattering, high detail materials",
    "poster": "graphic poster design, bold typography, strong composition, print-ready layout",
    "bible-scene": "historically grounded ancient Near East setting, period-accurate clothing and architecture, natural Levant landscape, painterly realism, reverent mood, no halos, no text",
    "sermon-slide": "calm background image for a presentation slide, large empty negative space on one side for text, soft muted tones, low contrast, no text, no letters",
    "devotional": "gentle watercolor and gouache illustration, warm morning light, quiet and hopeful atmosphere, soft paper texture, simple composition, no text",
    "bulletin": "clean editorial illustration for a church bulletin cover, seasonal motif, balanced composition with space at the top for a title, print-friendly colors, no text",
    "webtoon": "Korean webtoon panel, clean line art, cel shading, expressive characters, clear staging, vertical comic composition",
    "thumbnail": "eye-catching YouTube thumbnail background, strong focal subject, high contrast, vivid but natural colors, empty area for headline text, no text",
}
PHASES = {"queued": "대기", "starting": "시작", "loading": "모델 로딩", "encoding": "프롬프트 처리",
          "sampling": "생성", "decoding": "디코딩", "saving": "저장", "finished": "완료"}


def request(path, data=None, timeout=30, content_type="application/json"):
    body = None
    if data is not None:
        body = data if isinstance(data, bytes) else json.dumps(data).encode()
    req = urllib.request.Request(f"{URL}{path}", data=body, headers={"Content-Type": content_type})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            msg = json.load(e).get("error", str(e))
        except Exception:
            msg = str(e)
        sys.exit(f"Image Studio 오류 ({e.code}): {msg}")


def reachable():
    try:
        urllib.request.urlopen(f"{URL}/api/status", timeout=5).close()
        return True
    except Exception:
        return False


def install_root():
    if ROOT_FILE.exists():
        root = Path(ROOT_FILE.read_text().strip())
        if (root / "run-web.sh").exists():
            return root
    return None


def ensure_server():
    if reachable():
        return
    root = install_root()
    if root is None:
        sys.exit("Image Studio 가 켜져 있지 않고 설치 폴더도 찾지 못했습니다.\n"
                 "apps/image-studio 에서 ./install.sh 를 먼저 실행하거나, start.command 로 켠 뒤 다시 시도하세요.")
    print(f"Image Studio 를 켭니다 ({root}) ...", flush=True)
    log = open(root / "web.log", "a")
    subprocess.Popen(["/bin/zsh", str(root / "run-web.sh")], cwd=root, stdout=log, stderr=log,
                     start_new_session=True)
    for _ in range(180):
        if reachable():
            print("켜졌습니다.", flush=True)
            return
        time.sleep(1)
    sys.exit(f"3분 안에 켜지지 않았습니다. {root / 'web.log'} 를 확인하세요.")


def low_memory_install():
    root = install_root()
    env = root / "web" / ".env.local" if root else None
    return bool(env and env.exists() and "NEXT_PUBLIC_LOW_MEMORY=1" in env.read_text())


def round32(n):
    return min(2048, max(256, int(round(n / 32)) * 32))


def resolution(ratio, mp):
    w, h = RATIOS[ratio]
    pixels = mp * 1024 * 1024
    r = w / h
    return round32(math.sqrt(pixels * r)), round32(math.sqrt(pixels / r))


def upload(path):
    p = Path(path).expanduser()
    if not p.exists():
        sys.exit(f"참조 이미지를 찾을 수 없습니다: {p}")
    boundary = uuid.uuid4().hex
    ext = p.suffix.lower().lstrip(".")
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp",
            "heic": "image/heic", "heif": "image/heif", "gif": "image/gif", "avif": "image/avif"}.get(ext, "image/png")
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{p.name}\"\r\n"
            f"Content-Type: {mime}\r\n\r\n").encode() + p.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    info = request("/api/uploads", body, timeout=120, content_type=f"multipart/form-data; boundary={boundary}")
    return info["id"]


def show_status():
    if not reachable():
        print(f"꺼져 있음 ({URL})")
        root = install_root()
        print(f"설치 폴더: {root}" if root else "설치 폴더: 찾지 못함 (~/.image-studio-root 없음)")
        return
    s = request("/api/status")
    comfy = s.get("comfy", {})
    print(f"웹 앱: 켜짐 ({URL})")
    print(f"ComfyUI: {'켜짐' if comfy.get('reachable') else ('켜는 중' if comfy.get('starting') else '꺼짐 (첫 생성 때 자동으로 켜짐)')}")
    print(f"대기열: 실행 {1 if s.get('worker', {}).get('runningJobId') else 0}, 대기 {s.get('worker', {}).get('queued', 0)}")
    print(f"저메모리 설치: {'예' if low_memory_install() else '아니오'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompt", nargs="?")
    ap.add_argument("--style", choices=STYLES, default="none")
    ap.add_argument("--preset", choices=PRESETS, default=None, help="기본: draft (저메모리 설치면 lowmem 의 해상도·모델)")
    ap.add_argument("--ratio", choices=RATIOS, default="1:1")
    ap.add_argument("--width", type=int)
    ap.add_argument("--height", type=int)
    ap.add_argument("--steps", type=int)
    ap.add_argument("--seed", type=int, help="고정 시드. --count 와 함께 쓰면 seed, seed+1, ... 로 생성")
    ap.add_argument("--count", type=int, default=1, help="연속 생성 수 (1~8)")
    ap.add_argument("--negative", default="", help="부정 프롬프트. 쓰면 CFG 를 2.5 로 올린다 (시간 2배)")
    ap.add_argument("--cfg", type=float)
    ap.add_argument("--ref", action="append", default=[], help="참조(편집 원본) 이미지 경로, 최대 3개")
    ap.add_argument("--out", default="outputs/studio", help="결과 저장 폴더 (기본: ./outputs/studio)")
    ap.add_argument("--no-wait", action="store_true", help="대기열에 넣기만 하고 바로 끝낸다")
    ap.add_argument("--status", action="store_true", help="스튜디오 상태만 보여 준다")
    a = ap.parse_args()

    if a.status:
        show_status()
        return
    if not a.prompt:
        ap.error("프롬프트를 입력하세요.")
    if len(a.ref) > 3:
        ap.error("참조 이미지는 최대 3개입니다.")

    low = low_memory_install()
    preset_id = a.preset or "draft"
    preset = dict(PRESETS[preset_id])
    if low:
        preset["gguf"] = "Q4_K_M"  # 32GB 미만 설치에서는 모든 프리셋을 Q4 로 돌려 메모리를 아낀다
    width, height = resolution(a.ratio, preset["mp"])
    width = round32(a.width) if a.width else width
    height = round32(a.height) if a.height else height
    cfg = a.cfg if a.cfg is not None else (2.5 if a.negative else 1.0)
    suffix = STYLES[a.style]
    prompt = f"{a.prompt.strip()}, {suffix}" if suffix else a.prompt.strip()

    ensure_server()
    refs = [upload(r) for r in a.ref]
    params = {
        "prompt": prompt, "negativePrompt": a.negative, "width": width, "height": height,
        "steps": a.steps or preset["steps"], "cfg": cfg, "seed": a.seed, "sampler": "euler", "scheduler": "simple",
        "engine": "comfyui", "gguf": GGUF_FILES[preset["gguf"]], "textEncoder": TEXT_ENCODER, "quantize": 8,
        "references": refs, "followReferenceSize": not (a.width or a.height), "imageStrength": 0.6,
        "presetId": preset_id, "ratioId": a.ratio, "styleId": a.style,
    }
    jobs = request("/api/jobs", {"params": params, "count": max(1, min(8, a.count))})["jobs"]
    print(f"대기열에 {len(jobs)}개 추가: {PRESETS[preset_id]['label']} · {width}x{height} · {params['steps']}스텝 · "
          f"{preset['gguf']}{' · 참조 ' + str(len(refs)) + '장' if refs else ''}")
    print(f"브라우저에서 진행 상황 보기: {URL}")
    if a.no_wait:
        for j in jobs:
            print(f"  작업 {j['id'][:8]} 시드 {j['params']['seed']}")
        return

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    pending = {j["id"]: j for j in jobs}
    results = []
    t0 = time.time()
    last_line = ""
    while pending:
        for jid in list(pending):
            job = request(f"/api/jobs/{jid}")["job"]
            if job["status"] == "done":
                seed = job["params"]["seed"]
                dst = out / f"{datetime.now():%Y%m%d-%H%M%S}_seed{seed}_{jid[:8]}.png"
                with urllib.request.urlopen(f"{URL}/api/images/{jid}", timeout=60) as r:
                    dst.write_bytes(r.read())
                results.append((seed, dst))
                del pending[jid]
                print(f"\n완료 시드 {seed} → {dst}", flush=True)
            elif job["status"] in ("failed", "cancelled"):
                del pending[jid]
                print(f"\n{'실패' if job['status'] == 'failed' else '취소'} 시드 {job['params']['seed']}: "
                      f"{job.get('error') or ''}", flush=True)
            elif job["status"] == "running":
                pr = job.get("progress", {})
                eta = pr.get("etaMs")
                line = (f"\r[{len(results) + 1}/{len(jobs)}] {PHASES.get(pr.get('phase'), pr.get('phase'))} "
                        f"{pr.get('step', 0)}/{pr.get('total', 0)}"
                        f"{f' · 남은 시간 약 {int(eta / 1000)}초' if eta else ''} · 경과 {int(time.time() - t0)}초")
                if line != last_line:
                    print(line.ljust(70), end="", flush=True)
                    last_line = line
        if pending:
            time.sleep(3)

    if results:
        log = out / "seeds.md"
        new = not log.exists()
        with log.open("a", encoding="utf-8") as f:
            if new:
                f.write("| 시각 | 시드 | 크기 | 스텝 | 스타일 | 파일 | 프롬프트 |\n|---|---|---|---|---|---|---|\n")
            for seed, dst in results:
                f.write(f"| {datetime.now():%Y-%m-%d %H:%M} | {seed} | {width}x{height} | {params['steps']} | "
                        f"{a.style} | {dst.name} | {a.prompt.strip().replace('|', '/')} |\n")
        print(f"\n시드 기록: {log}")
    if len(results) < len(jobs):
        sys.exit(1)


if __name__ == "__main__":
    main()
