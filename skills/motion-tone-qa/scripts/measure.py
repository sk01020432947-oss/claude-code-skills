#!/usr/bin/env python3
"""모션 영상 숫자 검수 — 밝기·컷 간격·움직임·음량·정지 구간·숫자 대조·24컷 밀착 인화.

사용:
  python3 measure.py 영상.mp4                         # 측정만
  python3 measure.py 참고1.mp4 참고2.mp4 --save-card 설교묵상   # 참고 영상으로 톤 카드 목표값 만들기
  python3 measure.py 결과.mp4 --card 설교묵상 --script 대본.txt --source index.html
톤 카드는 ~/.claude/skills/motion-tone-qa/cards/<이름>.json 에 저장된다.
"""
import argparse, json, os, re, statistics, subprocess, sys, tempfile

CARDS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cards")
TOL = {"brightness": 0.25, "cut_sec": 0.30, "motion": 0.40}  # 목표 대비 허용 오차(비율). 컷 30%는 영상 J4PbF8_u6pY 기준


def ff(args):
    return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *args],
                          capture_output=True, text=True).stderr


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return float(out.strip() or 0)


def measure(path, sheet=None):
    dur = duration(path)
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as t:
        stats = t.name
    # 밝기(YAVG)·움직임(YDIF) — 30fps·축소본으로 맞춰 해상도·프레임수와 무관하게
    ff(["-i", path, "-vf", f"fps=30,scale=320:-2,signalstats,metadata=mode=print:file={stats}", "-an", "-f", "null", "-"])
    yavg, ydif = [], []
    for line in open(stats):
        m = re.search(r"signalstats\.(YAVG|YDIF)=([\d.]+)", line)
        if m:
            (yavg if m[1] == "YAVG" else ydif).append(float(m[2]))
    os.unlink(stats)
    # 장면 전환
    log = ff(["-i", path, "-vf", "scale=320:-2,select='gt(scene,0.3)',showinfo", "-an", "-f", "null", "-"])
    cuts = [float(x) for x in re.findall(r"pts_time:([\d.]+)", log)]
    # 1초 넘게 멈춘 구간
    log = ff(["-i", path, "-vf", "freezedetect=n=0.003:d=1", "-an", "-f", "null", "-"])
    starts = re.findall(r"freeze_start: ([\d.]+)", log)
    durs = re.findall(r"freeze_duration: ([\d.]+)", log)
    freezes = [(round(float(s), 2), round(float(d), 2)) for s, d in zip(starts, durs)]
    # 통합 음량
    log = ff(["-i", path, "-af", "ebur128", "-f", "null", "-"])
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", log)
    if sheet:
        n = 24
        fps = n / dur if dur else 1
        ff(["-y", "-i", path, "-vf", f"fps={fps:.5f},scale=480:-2,tile=6x4", "-frames:v", "1", sheet])
    return {
        "file": os.path.basename(path),
        "duration": round(dur, 2),
        "brightness": round(statistics.mean(yavg), 1) if yavg else None,
        "motion": round(statistics.mean(ydif), 2) if ydif else None,
        "cuts": len(cuts),
        "cut_sec": round(dur / (len(cuts) + 1), 2) if dur else None,
        "lufs": float(lufs[-1]) if lufs else None,
        "freezes_over_1s": freezes,
    }


def numbers(text):
    return {n.replace(",", "") for n in re.findall(r"\d[\d,]*(?:\.\d+)?", text)}


def check(m, card, script=None, source=None):
    issues = []
    if card.get("cut_sec") is None and m["cuts"] > card.get("max_cuts", 0) + 1:
        issues.append(f"끊지 않는 톤인데 컷 {m['cuts']}개")
    for k, tol in TOL.items():
        target, got = card.get(k), m.get(k)
        if not target or got is None:
            continue
        lo, hi = card.get(k + "_range", [target, target])  # 참고 영상들의 최소~최대
        if not lo * (1 - tol) <= got <= hi * (1 + tol):
            issues.append(f"{k}: {got} (허용 {round(lo*(1-tol),2)}~{round(hi*(1+tol),2)})")
    lo, hi = card.get("lufs_range", [-16, -12])
    if m["lufs"] is not None and not lo <= m["lufs"] <= hi:
        issues.append(f"lufs: {m['lufs']} (기준 {lo}~{hi})")
    limit = max(1.0, round(card.get("freeze_max", 1.0) * 1.1, 2))  # 해상도에 따른 흔들림 10% 여유  # 느린 톤은 참고 영상의 정지 길이까지 허용
    long = [f for f in m["freezes_over_1s"] if f[1] > limit]
    if long:
        issues.append(f"{limit}초 넘는 정지: {long}")
    if script and source:
        extra = numbers(open(source, encoding="utf-8").read()) - numbers(open(script, encoding="utf-8").read())
        # 코드 속 숫자(px·ms 등)도 섞이므로 화면 문구 파일을 따로 주는 편이 정확하다
        if extra:
            issues.append(f"대본에 없는 숫자 {len(extra)}개: {sorted(extra)[:20]}")
    return issues


def main():
    p = argparse.ArgumentParser()
    p.add_argument("videos", nargs="+")
    p.add_argument("--save-card")
    p.add_argument("--card")
    p.add_argument("--script", help="대본 텍스트 (숫자 대조 기준)")
    p.add_argument("--source", help="화면 문구 또는 HTML 소스 (대조 대상)")
    p.add_argument("--sheet", action="store_true", help="24컷 밀착 인화 PNG 저장")
    a = p.parse_args()

    results = []
    for v in a.videos:
        sheet = os.path.splitext(v)[0] + "_24컷.png" if a.sheet else None
        results.append(measure(v, sheet))
    print(json.dumps(results, ensure_ascii=False, indent=2))

    if a.save_card:
        os.makedirs(CARDS, exist_ok=True)
        card = {k: round(statistics.mean(r[k] for r in results if r[k] is not None), 2)
                for k in ("brightness", "motion", "cut_sec")}
        for k in ("brightness", "motion", "cut_sec"):
            vals = [r[k] for r in results if r[k] is not None]
            card[k + "_range"] = [min(vals), max(vals)]
        if all(r["cuts"] == 0 for r in results):  # 컷 없는 톤: 길이/(컷+1)은 영상 길이일 뿐이라 쓰지 않는다
            card["cut_sec"], card["max_cuts"] = None, 0
        card["freeze_max"] = max([f[1] for r in results for f in r["freezes_over_1s"]], default=1.0)
        card["lufs_range"] = [-16, -12]
        card["source"] = [r["file"] for r in results]
        path = os.path.join(CARDS, a.save_card + ".json")
        json.dump(card, open(path, "w"), ensure_ascii=False, indent=2)
        print(f"톤 카드 저장: {path}")

    if a.card:
        card = json.load(open(os.path.join(CARDS, a.card + ".json")))
        bad = False
        for r in results:
            issues = check(r, card, a.script, a.source)
            print(f"\n[{r['file']}] " + ("PASS" if not issues else "FIX"))
            for i in issues:
                print("  -", i)
            bad |= bool(issues)
        sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
