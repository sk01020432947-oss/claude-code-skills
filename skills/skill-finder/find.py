#!/usr/bin/env python3
"""전역 스킬을 이름·설명으로 찾는다. 사용: find.py 검색어 [검색어 ...]"""
import os, re, sys, unicodedata as u

ROOTS = ["~/.claude/skills", "~/.cys/claude/skills"]


def norm(s):
    return u.normalize("NFC", s).lower()  # 맥 파일명은 NFD


def skills():
    seen = set()
    for root in map(os.path.expanduser, ROOTS):
        for n in sorted(os.listdir(root)) if os.path.isdir(root) else []:
            p = os.path.join(root, n, "SKILL.md")
            if n in seen or not os.path.isfile(p):
                continue
            seen.add(n)
            with open(p, encoding="utf-8", errors="replace") as f:
                m = re.search(r"^description:\s*(.*(?:\n[ \t]+.*)*)", f.read(8000), re.M)
            yield n, " ".join(m.group(1).split()) if m else "", p


def search(terms):
    terms = [norm(t) for t in terms]
    hits = []
    for n, d, p in skills():
        name, text = norm(n), norm(d)
        score = sum((3 if t in name else 0) + (1 if t in text else 0) for t in terms)
        if score:
            hits.append((-score, n, d, p))
    return sorted(hits)[:10]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    hits = search(sys.argv[1:])
    for _, n, d, p in hits:
        print(f"{n}\n  {d[:160]}\n  {p}")
    if not hits:
        print("맞는 스킬 없음")
