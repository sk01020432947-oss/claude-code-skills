#!/usr/bin/env python3
"""PAX(공공AX 사례 아카이브) 로컬 미러 검색. 캐시가 8시간보다 오래되면 원본에서 자동 갱신."""
import json, sys, time, unicodedata, urllib.request, argparse
from pathlib import Path

URL = "https://raw.githubusercontent.com/hollobit/PAX/main/data/cases.json"
CACHE = Path(__file__).with_name("cases.json")
MAX_AGE = 8 * 3600  # PAX 원본 수집 주기와 같음

def load(force=False):
    if force or not CACHE.exists() or time.time() - CACHE.stat().st_mtime > MAX_AGE:
        try:
            data = urllib.request.urlopen(URL, timeout=30).read()
            json.loads(data)  # 깨진 응답으로 캐시를 덮어쓰지 않게
            CACHE.write_bytes(data)
        except Exception as e:
            if not CACHE.exists():
                sys.exit(f"PAX 다운로드 실패, 캐시 없음: {e}")
            print(f"[경고] 갱신 실패, 기존 캐시 사용: {e}", file=sys.stderr)
    return json.loads(CACHE.read_text())

SITE = "https://hollobit.github.io/PAX/data/"
# 사례 외 아카이브: 이름 -> (파일, 레코드 목록 키 | None=통째로 출력)
ARCH = {"news": ("news.json", "articles"), "videos": ("videos.json", "videos"),
        "mcp": ("mcp-review.json", "reviews"), "champions": ("champions.json", "champions"),
        "unattributed": ("champions.json", "unattributed"), "evals": ("evaluations.json", "cases"),
        "changelog": ("changelog.json", "entries"), "community": ("community.json", None),
        "index": ("index.json", None), "dashboard": ("dashboard-history.json", None)}

def load_arch(fname, force=False):
    f = CACHE.with_name("data") / fname
    if force or not f.exists() or time.time() - f.stat().st_mtime > MAX_AGE:
        try:
            data = urllib.request.urlopen(SITE + fname, timeout=60).read()
            json.loads(data)
            f.parent.mkdir(exist_ok=True)
            f.write_bytes(data)
        except Exception as e:
            if not f.exists():
                sys.exit(f"PAX {fname} 다운로드 실패, 캐시 없음: {e}")
            print(f"[경고] {fname} 갱신 실패, 기존 캐시 사용: {e}", file=sys.stderr)
    return json.loads(f.read_text())

def nfc(s):
    return unicodedata.normalize("NFC", str(s or "")).lower()

def search(cases, terms, org_type=None):
    terms = [nfc(t) for t in terms]
    hits = []
    for c in cases:
        if org_type and nfc(org_type) not in nfc(c.get("org_type")):
            continue
        hay = nfc(" ".join(str(c.get(k, "")) for k in
                  ("title", "summary", "org", "org_type", "tags", "task_category", "transition_stage", "region")))
        score = sum(hay.count(t) for t in terms)
        if score or not terms:
            hits.append((score, c.get("date", ""), c))
    hits.sort(key=lambda h: (h[0], h[1]), reverse=True)
    return [h[2] for h in hits]

def cite(i, c):
    tags = ", ".join(c.get("tags") or [])
    stage = c.get("transition_stage") or ""
    return (f"[{i}] {c.get('title')}\n"
            f"    기관: {c.get('org')} ({c.get('org_type')}) · 날짜: {c.get('date')} · 수집: {c.get('collected_at')}"
            + (f" · 단계: {stage}" if stage else "") + "\n"
            f"    요약: {c.get('summary')}\n"
            f"    태그: {tags}\n"
            f"    사례: {c.get('case_url') or '-'}\n"
            f"    출처: {c.get('link')} (PAX id {c.get('id')})")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("terms", nargs="*")
    p.add_argument("-n", type=int, default=10)
    p.add_argument("--org-type")
    p.add_argument("--refresh", action="store_true")
    p.add_argument("--in", dest="arch", choices=["cases", *ARCH], default="cases")
    a = p.parse_args()
    if a.arch != "cases":
        fname, key = ARCH[a.arch]
        d = load_arch(fname, a.refresh)
        stamp = d.get("updated_at") or d.get("generated_at") or d.get("evaluated_at") or "-"
        if key is None:
            print(f"PAX {a.arch} 기준: {stamp} · 출처 {SITE}{fname}\n")
            print(json.dumps(d, ensure_ascii=False, indent=1)[:20000])
            return
        recs = d[key]
        terms = [nfc(t) for t in a.terms]
        hits = [r for r in recs if all(t in nfc(json.dumps(r, ensure_ascii=False)) for t in terms)]
        print(f"PAX {a.arch} 기준: {stamp} · 전체 {len(recs)}건 · 일치 {len(hits)}건 · 출처 {SITE}{fname}\n")
        for i, r in enumerate(hits[:a.n], 1):
            print(f"[{i}] " + json.dumps(r, ensure_ascii=False)[:1500] + "\n")
        return
    d = load(a.refresh)
    hits = search(d["cases"], a.terms, a.org_type)
    print(f"PAX 원본 갱신: {d.get('updated_at')} · 전체 {len(d['cases'])}건 · 일치 {len(hits)}건\n")
    for i, c in enumerate(hits[:a.n], 1):
        print(cite(i, c) + "\n")

if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        cs = [{"title": "돌봄 AI", "date": "2026-01-01"}, {"title": "교통", "date": "2026-02-01"},
              {"title": "돌봄 돌봄", "date": "2025-01-01"}]
        r = search(cs, [unicodedata.normalize("NFD", "돌봄")])
        assert [c["title"] for c in r] == ["돌봄 돌봄", "돌봄 AI"], r
        print("ok")
    else:
        main()
