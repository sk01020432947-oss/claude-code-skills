#!/usr/bin/env python
"""kr-api-catalog lookup: search the local public-apis-4Kr index (Korean + global).
Usage:
  python lookup.py 키워드 [키워드...]        # Korean list (README.md), AND-match on name/desc/category
  python lookup.py --global 키워드 [...]     # GLOBAL_PUBLIC_APIS_KR.md
  python lookup.py --cat                     # list categories with counts
  python lookup.py --cat 교통                # dump one category
  python lookup.py --update                  # git pull + rebuild index
"""
import sys, re, json, subprocess, os
REPO = r"/Users/kbg1023/DEV/public-apis-4Kr"
IDX = os.path.join(REPO, "kr_apis_index.json")

def parse(md_path, start_marker, end_marker=None):
    txt = open(md_path, encoding="utf-8").read()
    body = txt[txt.index(start_marker):]
    if end_marker and end_marker in body: body = body[:body.index(end_marker)]
    cats, cur = [], None
    for line in body.splitlines():
        m = re.match(r"^### (.+)$", line)
        if m:
            cur = {"name": m.group(1).strip(), "items": []}; cats.append(cur); continue
        if cur and line.startswith("|") and not re.match(r"^\|\s*-", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3: continue
            lm = re.match(r"\[(.+?)\]\((.+?)\)", cells[0])
            if not lm: continue
            cur["items"].append({"name": lm.group(1), "url": lm.group(2), "desc": cells[1], "auth": cells[2].replace("`", "")})
    return cats

def rebuild():
    kr = parse(os.path.join(REPO, "README.md"), "### 정부 & 공공기관", "## 기여하기")
    json.dump(kr, open(IDX, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return kr

def load(global_=False):
    if global_:
        return parse(os.path.join(REPO, "GLOBAL_PUBLIC_APIS_KR.md"), "## Public API 목록")
    src = os.path.join(REPO, "README.md")
    # 인덱스가 없거나 README 가 더 새로우면 다시 만든다 (git pull 후 자동 반영)
    if not os.path.exists(IDX) or os.path.getmtime(src) > os.path.getmtime(IDX):
        return rebuild()
    return json.load(open(IDX, encoding="utf-8"))

def main(argv):
    if "--update" in argv:
        print(subprocess.run(["git", "-C", REPO, "pull", "--ff-only"], capture_output=True, text=True).stdout.strip())
        kr = rebuild(); print(f"index rebuilt: {sum(len(c['items']) for c in kr)} items"); return
    g = "--global" in argv; argv = [a for a in argv if a != "--global"]
    cats = load(g)
    if "--cat" in argv:
        rest = [a for a in argv if a != "--cat"]
        if not rest:
            for c in cats: print(f"{len(c['items']):3d}  {c['name']}")
            return
        for c in cats:
            if any(r in c["name"] for r in rest):
                print(f"## {c['name']}")
                for it in c["items"]: print(f"- {it['name']} [{it['auth']}] — {it['desc']}\n  {it['url']}")
        return
    kws = [k.lower() for k in argv]
    if not kws: print(__doc__); return
    n = 0
    for c in cats:
        for it in c["items"]:
            hay = f"{c['name']} {it['name']} {it['desc']}".lower()
            if all(k in hay for k in kws):
                n += 1; print(f"[{c['name']}] {it['name']} [{it['auth']}] — {it['desc']}\n  {it['url']}")
    print(f"-- {n} hit(s) ({'global' if g else 'korea'} list)")

if __name__ == "__main__": main(sys.argv[1:])
