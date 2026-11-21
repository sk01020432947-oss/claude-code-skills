#!/usr/bin/env python3
"""정본 도구 폴더의 코드를 이 스킬의 assets/ 로 베낀다(스냅숏 새로 뜨기). 자료 파일은 하나도 베끼지 않는다.

    python3 묶기.py          # 베끼고, 정본과 글자 하나까지 같은지 확인
"""
import filecmp, shutil, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent
TOOL = SKILL.parent                                  # 통합수집기/
# 코드만 — 이름을 하나씩 적는다(글롭을 쓰면 자료 파일이 딸려 올 수 있다)
CODE = ["통합정리.py", "통합수집기.js", "통합수집기-북마클릿.txt", "수집기.js", "수집기-북마클릿.txt",
        "수집기_점검.html", "parse_manual.py", "make_review_page.py"]
SIDE = [TOOL.parent / "카카오톡_자료정리" / "카카오톡_자료정리.py", Path.home() / ".claude/hooks/artifact-ledger.py"]
pairs = [(TOOL / n, SKILL / "assets" / n) for n in CODE] + [(p, SKILL / "assets" / "곁도구" / p.name) for p in SIDE]
pairs.append((TOOL / "CLAUDE.md", SKILL / "references" / "기능명세.md"))   # 이름을 바꾼다: 하위 폴더의 CLAUDE.md 는 지침으로 읽힌다

bad = []
for src, dst in pairs:
    if not src.is_file():
        bad.append(f"없음: {src.name}")
        continue
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    if not filecmp.cmp(src, dst, shallow=False):
        bad.append(f"다름: {src.name}")

# 자료가 섞여 들어오지 않았는지: assets 에는 위에 적은 이름만 있어야 한다
want = {d.relative_to(SKILL) for _, d in pairs}
have = {f.relative_to(SKILL) for sub in ("assets", "references") for f in (SKILL / sub).rglob("*") if f.is_file()}
extra = have - want - {Path("references/구조.md")}
bad += [f"적지 않은 파일: {e}" for e in sorted(map(str, extra))]
big = [str(f) for f in have if (SKILL / f).stat().st_size > 400_000]   # 코드는 다 400KB 아래다 — 넘으면 자료다
bad += [f"너무 큼: {b}" for b in big]

print(f"베낀 파일 {len(pairs) - sum(b.startswith('없음') for b in bad)}개")
if bad:
    sys.exit("\n".join(bad))
print("정본과 같음 · 자료 파일 없음")
