#!/usr/bin/env python3
"""인쇄용 원본 HTML → 아티팩트 발행용 사본(_웹발행/). 문서 껍데기·meta 제거, 제목 교체, 인쇄 버튼·P키 제거.
사용: webcopy.py 원본.html 사본.html "페이지 제목"   (마크다운 논고는 references/web-publish.md의 pandoc 절차)"""
import re, sys

def webify(s: str, title: str) -> str:
    head = re.search(r"<head>(.*?)</head>", s, re.S)
    body = re.search(r"<body[^>]*>(.*?)</body>", s, re.S)
    head, body = (head.group(1) if head else ""), (body.group(1) if body else s)
    head = re.sub(r"<meta[^>]*>\s*", "", head)
    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, flags=re.S) if "<title>" in head else f"<title>{title}</title>\n" + head
    body = re.sub(r'<button[^>]*id="pr"[^>]*>.*?</button>', "", body)          # 인쇄 버튼
    body = re.sub(r"else if\(k=='p'\|\|k=='P'\)print\(\)", "", body)          # P 키
    body = re.sub(r"\w+\.onclick=\(\)=>print\(\);?", "", body)
    return head.strip() + "\n" + body.strip() + "\n"

if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        r = webify('<!doctype html><html><head><meta charset="utf-8"><title>a</title><style>x</style></head><body><p>hi</p><button id="pr">인쇄</button></body></html>', "새 제목")
        assert "<title>새 제목</title>" in r and "<meta" not in r and "인쇄" not in r and "<body" not in r, r
        print("ok")
    else:
        src, dst, title = sys.argv[1:4]
        open(dst, "w", encoding="utf-8").write(webify(open(src, encoding="utf-8").read(), title))
        print("written", dst)
