#!/usr/bin/env python3
"""Context7 REST 호출기 (표준 라이브러리만). npm/ctx7 없이 최신 라이브러리 문서를 가져온다.

  python3 c7.py search "<질문>" [--lib 이름]... [--lang TypeScript]
  python3 c7.py lib <라이브러리명> "<질문>"
  python3 c7.py docs </org/project[/버전]> "<질문>" [--lang Python]
CONTEXT7_API_KEY 환경변수가 있으면 Bearer 로 보낸다(없으면 IP 기준 저한도).
"""
import json, os, sys, urllib.error, urllib.parse, urllib.request

BASE = "https://context7.com/api"


def call(path, params):
    url = f"{BASE}{path}?{urllib.parse.urlencode(params, doseq=True)}"
    req = urllib.request.Request(url, headers={"User-Agent": "c7.py"})
    key = os.environ.get("CONTEXT7_API_KEY")
    if key:
        req.add_header("Authorization", f"Bearer {key}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")


def pop_opts(args, name):
    vals, rest, i = [], [], 0
    while i < len(args):
        if args[i] == name and i + 1 < len(args):
            vals.append(args[i + 1]); i += 2
        else:
            rest.append(args[i]); i += 1
    return vals, rest


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    cmd, args = argv[0], argv[1:]
    langs, args = pop_opts(args, "--lang")
    libs, args = pop_opts(args, "--lib")
    extra = {"language": langs[0]} if langs else {}
    if cmd == "search":
        status, body = call("/v3/search", {"query": args[0], "library": libs, **extra})
    elif cmd == "lib":
        status, body = call("/v2/libs/search", {"libraryName": args[0], "query": args[1]})
        if status == 200:
            rows = json.loads(body).get("results", [])[:5]
            body = "\n".join(f"{r['id']} | {r.get('title')} | 스니펫 {r.get('totalSnippets')} | 점수 {r.get('benchmarkScore')} | 버전 {','.join(r.get('versions') or [])[:80]}" for r in rows) or "결과 없음"
    elif cmd == "docs":
        status, body = call("/v2/context", {"libraryId": args[0], "query": args[1], **extra})
    else:
        sys.exit(__doc__)
    if status == 429:
        sys.exit("한도 초과(429): CONTEXT7_API_KEY 를 설정하라. 학습 데이터로 대체할 때는 사용자에게 알린다.")
    if status == 404:
        print("문서 없음(404) — 빈 결과로 취급"); return
    if status != 200:
        sys.exit(f"HTTP {status}: {body[:300]}")
    print(body)


if __name__ == "__main__":
    main(sys.argv[1:])
