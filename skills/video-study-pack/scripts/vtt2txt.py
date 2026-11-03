#!/usr/bin/env python3
"""유튜브 VTT 자막 → [MM:SS] 한 줄 텍스트. 사용: vtt2txt.py in.vtt out.txt | --selftest"""
import re, sys

def convert(vtt: str) -> list[str]:
    out, t, last = [], "00:00", ""
    for line in vtt.split("\n"):
        m = re.match(r"(\d\d):(\d\d):(\d\d)\.\d+ -->", line)
        if m:
            t = f"{int(m[1]) * 60 + int(m[2]):02d}:{m[3]}"
            continue
        if not line.strip() or line.startswith(("WEBVTT", "Kind", "Language")) or "<c>" in line:
            continue  # 자동자막의 단어별 타이밍 줄(<c>)은 중복이라 버린다
        txt = re.sub(r"<[^>]+>", "", line).strip().replace("&gt;", ">").replace("&amp;", "&")
        if txt and txt != last:
            out.append(f"[{t}] {txt}")
            last = txt
    return out

if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        s = "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\n안녕<c> 하세요</c>\n안녕\n\n00:01:05.000 --> 00:01:06.000\n안녕\n반갑습니다\n"
        assert convert(s) == ["[00:01] 안녕", "[01:05] 반갑습니다"], convert(s)
        print("ok")
    else:
        lines = convert(open(sys.argv[1], encoding="utf-8").read())
        open(sys.argv[2], "w", encoding="utf-8").write("\n".join(lines))
        print(len(lines), "lines")
