#!/usr/bin/env python3
"""PostToolUse(Artifact) — 아티팩트를 발행하면 통합자료수집기의 아티팩트_목록.csv 에 한 줄(날짜,제목,정본,주소) 더한다.

통합정리.py 가 이 파일을 읽어 "Claude 아티팩트" 저장소로 모은다 (자동 수집이 켜져 있으면 10분 안에 저절로).
같은 주소는 한 번만 적는다. 어떤 경우에도 exit 0 — 기록 실패가 발행을 막지 않는다.

자가검증:  python3 artifact-ledger.py --self-test
"""
import csv
import json
import os
import re
import sys
import time

LEDGER = os.path.expanduser("~/Desktop/cysjavis/SNS_기록/통합수집기/아티팩트_목록.csv")
URL_RE = re.compile(r"https://claude\.ai/(?:code/)?artifact/[A-Za-z0-9-]+")


def row_for(payload):
    """적을 한 줄 [날짜, 제목, 정본, 주소]. 발행이 아니거나 주소를 못 찾으면 None."""
    if payload.get("tool_name") != "Artifact":
        return None
    ti = payload.get("tool_input") or {}
    if (ti.get("action") or "publish") != "publish" or ti.get("asset"):
        return None
    # 갱신이면 넘긴 주소, 새 발행이면 결과에 적힌 주소
    m = URL_RE.search(str(ti.get("url") or "")) or URL_RE.search(json.dumps(payload.get("tool_response"), ensure_ascii=False))
    if not m:
        return None
    path = str(ti.get("file_path") or "")
    title = str(ti.get("title") or "")
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            t = re.search(r"(?is)<title>(.*?)</title>", fh.read(8192))
        title = t.group(1).strip() if t else title
    except OSError:
        pass
    title = title or os.path.splitext(os.path.basename(path))[0] or "제목 없음"
    home = os.path.expanduser("~")
    return [time.strftime("%Y-%m-%d"), title, "~" + path[len(home):] if path.startswith(home) else path, m.group(0)]


def add(row, ledger=LEDGER):
    """새 주소면 적고 True."""
    try:
        with open(ledger, encoding="utf-8") as fh:
            if row[3] in fh.read():
                return False
    except OSError:
        pass
    with open(ledger, "a", encoding="utf-8", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerow(row)
    return True


def self_test():
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        page, led = os.path.join(d, "p.html"), os.path.join(d, "l.csv")
        with open(page, "w", encoding="utf-8") as fh:
            fh.write("<title>제목, 쉼표</title>")
        new = {"tool_name": "Artifact", "tool_input": {"file_path": page},
               "tool_response": [{"type": "text", "text": "Published: https://claude.ai/artifact/AbC123 ok"}]}
        r = row_for(new)
        assert r[1:] == ["제목, 쉼표", page, "https://claude.ai/artifact/AbC123"], r
        assert add(r, led) and not add(r, led)                      # 같은 주소는 한 번만
        assert next(csv.reader(open(led, encoding="utf-8")))[1] == "제목, 쉼표"
        upd = dict(new, tool_input={"file_path": page, "url": "https://claude.ai/artifact/Zz9"}, tool_response="")
        assert row_for(upd)[3].endswith("/Zz9")                     # 갱신은 넘긴 주소
        assert row_for(dict(new, tool_input={"action": "list"})) is None
        assert row_for(dict(new, tool_response="주소 없음")) is None
        assert row_for({"tool_name": "Write"}) is None
    print("self-test OK")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        try:
            row = row_for(json.load(sys.stdin))
            if row:
                add(row)
        except Exception:
            pass    # fail-open
    sys.exit(0)
