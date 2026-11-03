#!/usr/bin/env python
"""yt_wiki.py - YouTube -> LLM Wiki raw transcript ingester (deterministic half).

Subcommands:
  list <channel_or_playlist_url> --out DIR   collect video metadata -> videos.json
  next --out DIR                             print one unprocessed video id (empty if none)
  fetch <video_id_or_url> --out DIR          write raw/<id>.md with timestamped blocks
  mark <video_id> --out DIR                  record id as processed
  selftest                                   run assertions, no network

The LLM half (concept pages, tags, index/log) is done by the agent per SKILL.md.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import date

STATE = "state.json"


# ---------- helpers ----------

def run(args):
    p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        sys.stderr.write(p.stderr[-2000:])
        raise SystemExit(f"command failed: {' '.join(args[:3])}...")
    return p.stdout


def state_path(out):
    return os.path.join(out, STATE)


def load_state(out):
    try:
        with open(state_path(out), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"processed": []}


def save_state(out, st):
    os.makedirs(out, exist_ok=True)
    with open(state_path(out), "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=2)


def hhmmss(sec):
    sec = int(sec)
    return f"{sec // 3600:02d}:{sec % 3600 // 60:02d}:{sec % 60:02d}"


def to_seconds(ts):
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


# ---------- vtt parsing ----------

def parse_vtt(raw):
    """YouTube auto-caption VTT -> [(start_seconds, text)] with rolling duplicates removed."""
    cur, out = None, []
    for line in raw.split("\n"):
        m = re.match(r"(\d\d:\d\d:\d\d)\.\d+ --> ", line)
        if m:
            cur = to_seconds(m.group(1))
            continue
        t = re.sub(r"<[^>]+>", "", line).strip()
        if not t or t.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        if cur is None:
            continue
        if out and (t.startswith(out[-1][1]) or out[-1][1].startswith(t)):
            # same caption line re-rendered as it grows; keep the longer form
            if len(t) > len(out[-1][1]):
                out[-1] = (out[-1][0], t)
            continue
        if out and out[-1][1] == t:
            continue
        out.append((cur, t))
    return out


def blockify(lines, window=45, max_chars=700):
    """Group caption lines into ~window-second blocks -> [(start, end, text)]."""
    blocks, buf, start = [], [], None
    for i, (sec, txt) in enumerate(lines):
        if start is None:
            start = sec
        buf.append(txt)
        nxt = lines[i + 1][0] if i + 1 < len(lines) else sec + 3
        if nxt - start >= window or len(" ".join(buf)) >= max_chars or i == len(lines) - 1:
            blocks.append((start, nxt, " ".join(buf)))
            buf, start = [], None
    return blocks


# ---------- commands ----------

def cmd_list(a):
    os.makedirs(a.out, exist_ok=True)
    raw = run(["yt-dlp", "--flat-playlist", "--dump-json", "--ignore-errors", a.url])
    vids = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            d = json.loads(line)
        except ValueError:
            continue
        dur = d.get("duration") or 0
        if dur < a.min_duration:      # shorts and stubs out
            continue
        vids.append({
            "id": d.get("id"),
            "title": d.get("title"),
            "duration": dur,
            "url": d.get("url") or f"https://www.youtube.com/watch?v={d.get('id')}",
        })
    with open(os.path.join(a.out, "videos.json"), "w", encoding="utf-8") as f:
        json.dump(vids, f, ensure_ascii=False, indent=2)
    print(f"{len(vids)} videos -> {os.path.join(a.out, 'videos.json')}")


def cmd_next(a):
    with open(os.path.join(a.out, "videos.json"), encoding="utf-8") as f:
        vids = json.load(f)
    done = set(load_state(a.out)["processed"])
    for v in vids:
        if v["id"] not in done:
            print(v["id"])
            return
    # no output = nothing to do; the agent must then change nothing


def cmd_fetch(a):
    vid = a.video
    if "watch?v=" in vid:
        vid = re.search(r"watch\?v=([\w-]+)", vid).group(1)
    elif "youtu.be/" in vid:
        vid = vid.rsplit("/", 1)[1].split("?")[0]
    url = f"https://www.youtube.com/watch?v={vid}"
    work = os.path.join(a.out, ".work")
    os.makedirs(work, exist_ok=True)

    meta = json.loads(run(["yt-dlp", "--skip-download", "--dump-json", url]))
    langs = f"{a.lang}-orig,{a.lang}"
    run(["yt-dlp", "--skip-download", "--write-auto-subs", "--write-subs",
         "--sub-langs", langs, "--sub-format", "vtt",
         "-o", os.path.join(work, f"{vid}.%(ext)s"), url])

    vtt = next((os.path.join(work, f) for f in sorted(os.listdir(work))
                if f.startswith(vid) and f.endswith(".vtt")), None)
    if not vtt:
        raise SystemExit(f"no captions for {vid} (lang={a.lang}); try --lang en")

    with open(vtt, encoding="utf-8") as f:
        text = f.read()
    lines = parse_vtt(text)
    dur = meta.get("duration") or (lines[-1][0] if lines else 0)
    lines = [(s, t) for s, t in lines if a.trim_head <= s <= dur - a.trim_tail]
    blocks = blockify(lines, a.window)

    body = [
        "---",
        f"title: {json.dumps(meta.get('title', ''), ensure_ascii=False)}",
        f"video_id: {vid}",
        f"source_url: {url}",
        f"channel: {json.dumps(meta.get('channel', ''), ensure_ascii=False)}",
        f"upload_date: {meta.get('upload_date', '')}",
        f"duration_sec: {dur}",
        f"ingested: {date.today().isoformat()}",
        f"sha256: {hashlib.sha256(text.encode('utf-8')).hexdigest()}",
        "type: transcript",
        "---",
        "",
        f"# {meta.get('title', vid)}",
        "",
        f"원본: {url}",
        "",
    ]
    for s, e, t in blocks:
        body.append(f"## [{hhmmss(s)}–{hhmmss(e)}] {url}&t={int(s)}s")
        body.append("")
        body.append(t)
        body.append("")

    dst = os.path.join(a.out, f"{vid}.md")
    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n".join(body))
    print(dst)
    print(f"blocks={len(blocks)} duration={hhmmss(dur)} title={meta.get('title','')}")


def cmd_mark(a):
    st = load_state(a.out)
    if a.video not in st["processed"]:
        st["processed"].append(a.video)
    save_state(a.out, st)
    print(f"processed={len(st['processed'])}")


def cmd_selftest(_a):
    vtt = """WEBVTT
Kind: captions
Language: ko

00:00:01.000 --> 00:00:03.000
안녕하세요

00:00:03.000 --> 00:00:05.000
안녕하세요 반갑습니다

00:01:00.000 --> 00:01:02.000
두 번째 블록
"""
    lines = parse_vtt(vtt)
    assert lines == [(1, "안녕하세요 반갑습니다"), (60, "두 번째 블록")], lines
    blocks = blockify(lines, window=45)
    assert len(blocks) == 2, blocks
    assert blocks[0][0] == 1 and blocks[1][0] == 60, blocks
    assert hhmmss(3661) == "01:01:01"
    assert to_seconds("01:01:01") == 3661
    print("selftest ok")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("list"); q.add_argument("url")
    q.add_argument("--out", required=True); q.add_argument("--min-duration", type=int, default=120)
    q.set_defaults(fn=cmd_list)

    q = sub.add_parser("next"); q.add_argument("--out", required=True); q.set_defaults(fn=cmd_next)

    q = sub.add_parser("fetch"); q.add_argument("video")
    q.add_argument("--out", required=True); q.add_argument("--lang", default="ko")
    q.add_argument("--window", type=int, default=45)
    q.add_argument("--trim-head", type=int, default=0)
    q.add_argument("--trim-tail", type=int, default=0)
    q.set_defaults(fn=cmd_fetch)

    q = sub.add_parser("mark"); q.add_argument("video")
    q.add_argument("--out", required=True); q.set_defaults(fn=cmd_mark)

    q = sub.add_parser("selftest"); q.set_defaults(fn=cmd_selftest)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
