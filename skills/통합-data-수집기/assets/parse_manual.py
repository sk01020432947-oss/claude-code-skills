#!/usr/bin/env python3
"""
수집기(manual/수집기.js)가 뽑아낸 원본 JSON을 정리하는 스크립트.

수집기는 화면에 보이는 덩어리를 통째로 raw_text에 담기 때문에
본문 앞뒤에 계정명·태그·날짜·좋아요 수 같은 화면 요소가 섞여 있다.
이 스크립트가 하는 일:

  1. 여러 번에 나눠 수집한 파일을 합치고 같은 글(id 중복)을 하나로 정리
  2. 대상 계정 글만 남기고 나머지는 별도 파일로 분리 (삭제 안 함)
  3. 머리말(계정명/태그/날짜)과 꼬리(좋아요·댓글·리포스트 숫자) 분리
  4. 같은 시각에 올라온 연속 발행 체인을 하나로 병합
  5. 규칙에 안 맞는 항목은 버리지 않고 경고를 달아 남김

사용법:
    python parse_manual.py raw/manual_2026-08-01_254.json      # 파일 하나
    python parse_manual.py raw                                  # raw 폴더 전체 합치기
    python parse_manual.py raw/A.json raw/B.json --account 계정명

계정명은 안 줘도 된다. 안 주면 수집한 데이터에서 가장 많이 나온
계정을 자동으로 찾아 쓴다 (수집기가 한 계정만 담기 때문에 안전하다).
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

DEFAULT_ACCOUNT = None   # 안 주면 수집한 데이터에서 자동으로 찾는다

DATE_LINE = re.compile(r"^20\d\d-\d\d-\d\d$")
RELATIVE_TIME = re.compile(r"^\d+\s*(분|시간|일|주|개월|년)$")
CHAIN_MARK = re.compile(r"(\d{1,2})\s*/\s*(\d{1,2})")
NUM_ONLY = re.compile(r"^[\d,]+$")


def split_head(lines, account):
    """머리말(계정명·태그·날짜)을 걷어내고 본문 시작 위치를 돌려준다."""
    i = 0
    tags = []
    saw_date = False

    while i < len(lines) and i < 5:
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line == account:
            i += 1
            continue
        if DATE_LINE.match(line) or RELATIVE_TIME.match(line):
            saw_date = True
            i += 1
            continue
        # 날짜를 아직 못 만났고 짧으면 태그로 본다 (예: "AI Threads", "구글")
        if not saw_date and len(line) <= 20:
            tags.append(line)
            i += 1
            continue
        break

    return i, tags, saw_date


def split_tail(lines):
    """끝에 붙은 숫자들(좋아요·댓글·리포스트·공유)과 체인 표시를 분리한다.

    화면에서 '1/2'는 세 줄('1', '/', '2')로 쪼개져 들어온다. 그래서
    꼬리를 걷어내면서 '숫자 / 숫자' 패턴을 만나면 그게 체인 표시다.
    반환: (본문 끝 위치, engagement 숫자들, 체인표시 or None)
    """
    end = len(lines)
    trailing = []  # 뒤에서부터 걷어낸 토큰들 (역순)

    while end > 0:
        line = lines[end - 1].strip()
        if not line:
            end -= 1
            continue
        if NUM_ONLY.match(line) or line == "/":
            trailing.insert(0, line)
            end -= 1
            continue
        break

    # 걷어낸 토큰 안에서 '숫자 / 숫자' 를 찾으면 그게 체인 표시
    chain = None
    for i in range(len(trailing) - 2):
        if trailing[i + 1] == "/" and NUM_ONLY.match(trailing[i]) and NUM_ONLY.match(trailing[i + 2]):
            a, b = int(trailing[i]), int(trailing[i + 2])
            if 1 <= a <= b <= 20:
                chain = (a, b)
                # 체인 표시 뒤에 오는 것들만 engagement 숫자
                trailing = trailing[i + 3:]
                break

    nums = [int(t.replace(",", "")) for t in trailing if NUM_ONLY.match(t)]
    return end, nums, chain


def parse_one(post, account):
    raw = post.get("raw_text", "")
    warnings = []

    # 남의 글이 통째로 딸려온 경우 먼저 잘라낸다 (남의 글에 단 답글 카드)
    raw, foreign = strip_foreign_card(raw, account)
    if foreign:
        warnings.append(f"남의 글(@{foreign}) 부분 잘라냄")

    # 중첩 카드로 부모 글이 통째로 딸려온 경우 잘라낸다
    raw, was_nested = strip_nested_duplicate(raw, account)
    if was_nested:
        warnings.append("중첩 카드에서 앞부분(부모 글) 잘라냄")

    lines = raw.split("\n")
    if len(lines) == 1:
        warnings.append("줄바꿈 없음 — 머리말/꼬리 분리 못 함")
        body = raw.strip()
        counts = []
        tags = []
        chain = None
    else:
        start, tags, saw_date = split_head(lines, account)
        end, counts, chain = split_tail(lines)
        if not saw_date:
            warnings.append("머리말에서 날짜를 못 찾음")
        if start >= end:
            warnings.append("본문이 비어 보임 — 원문 확인 필요")
            body = raw.strip()
            counts = []
        else:
            body = "\n".join(lines[start:end]).strip()

    # 본문에 남은 찌꺼기 검사
    if account in body:
        warnings.append("본문에 계정명이 남아있음")
    if re.search(r"20\d\d-\d\d-\d\d", body):
        warnings.append("본문에 날짜가 남아있음")
    if not body:
        warnings.append("본문 없음")

    # 댓글 카드 판별: 화면의 댓글 영역은 '인증된 계정', '좋아요 취소',
    # '답글을 달았습니다' 같은 UI 문구가 본문에 통째로 섞여 들어온다.
    # 이건 본인이 남의 글에 단 답글이므로 도메인 지식 정리 대상이 아니다.
    is_comment = any(
        k in body for k in ("인증된 계정", "좋아요 취소", "답글을 달았습니다")
    )
    # 남의 글을 잘라내고 남은 게 한두 줄뿐이면, 그건 글이 아니라
    # 남의 글에 단 짧은 답글이다 ("너무 귀여워서", "좋은정보라 공유해♡")
    if foreign and len(body) < 60:
        is_comment = True

    return {
        "id": post.get("id"),
        "username": post.get("username"),
        "url": post.get("url"),
        "created_at": post.get("created_at"),
        "text": body,
        "tags": tags,
        "counts": counts,          # [좋아요, 댓글, 리포스트, 공유] 순서로 추정 (미확정)
        "chain": list(chain) if chain else None,
        "is_comment": is_comment,
        "_warnings": warnings,
        "_raw": raw,
    }


USERNAME = re.compile(r"^[a-z][a-z0-9._]{2,29}$")


def strip_foreign_card(text, account):
    """남의 글이 통째로 딸려온 부분을 잘라낸다.

    본인이 남의 글에 답글을 달면, 화면 카드에 원글(남의 글)이 함께 그려진다.
    그 경우 본문 중간에 '남의 계정명 → (태그) → 날짜' 블록이 나타난다.
    거기서부터 끝까지가 남의 글이므로 잘라낸다.

    2025년 상반기(맞팔·이벤트 활동기) 글에서 주로 나온다. 2026년 표본
    254개만 볼 때는 안 보이던 패턴이라 뒤늦게 발견했다 (2026-08-01).
    """
    lines = text.split("\n")
    for i, raw_line in enumerate(lines):
        line = raw_line.strip()
        if not USERNAME.match(line) or line == account:
            continue
        # 계정명 바로 다음이나 그다음 줄이 날짜면 카드 머리말이다
        for j in (i + 1, i + 2):
            if j < len(lines) and DATE_LINE.match(lines[j].strip()):
                return "\n".join(lines[:i]).strip(), line
    return text, None


def strip_nested_duplicate(text, account):
    """중첩 카드로 인해 통째로 딸려온 앞부분을 잘라낸다.

    화면에서 체인 글은 1/2 카드 안에 2/2 카드가 중첩 렌더링된다.
    그래서 2/2 항목을 수확할 때 부모(1/2 전체)까지 딸려 들어온다.
    그 경우 raw_text 중간에 계정명 머리말이 다시 나타나므로,
    '마지막 머리말' 이후만 남기면 자기 몫의 본문만 얻는다.
    """
    marker = "\n" + account + "\n"
    idx = text.rfind(marker)
    if idx <= 0:
        return text, False
    return text[idx + 1:], True


def merge_chains(items):
    """진짜 연속 발행 체인만 하나로 합친다.

    같은 시각이라도 내용이 겹치면 체인이 아니라 중복이므로,
    체인 표시(n/m)가 서로 다른 번호일 때만 병합한다.
    """
    groups = defaultdict(list)
    for it in items:
        groups[it["created_at"]].append(it)

    merged = []
    for ts, group in groups.items():
        if len(group) == 1:
            it = group[0]
            it["parts"] = 1
            merged.append(it)
            continue

        group = sorted(group, key=lambda x: x["chain"][0] if x["chain"] else 99)
        marks = [tuple(x["chain"]) if x["chain"] else None for x in group]

        # 체인 번호가 모두 있고 서로 다르면 진짜 체인
        nums = [m[0] for m in marks if m]
        is_real_chain = len(nums) == len(group) and len(set(nums)) == len(group)

        if not is_real_chain:
            # 체인이 아님 — 각각 독립 글로 남기고 경고만 단다
            for x in group:
                x["parts"] = 1
                x["_warnings"] = x["_warnings"] + [
                    f"같은 시각에 다른 글이 있으나 체인 번호가 불완전: {marks}"
                ]
                merged.append(x)
            continue

        parts_text = []
        for x in group:
            t = re.sub(r"\s*\d{1,2}\s*/\s*\d{1,2}\s*$", "", x["text"]).strip()
            parts_text.append(t)

        head = group[0]
        merged.append({
            "id": head["id"],
            "username": head["username"],
            "url": head["url"],
            "created_at": ts,
            "text": "\n\n".join(t for t in parts_text if t),
            "tags": head["tags"],
            "counts": [x["counts"] for x in group],
            "chain": None,
            "parts": len(group),
            "part_urls": [x["url"] for x in group],
            "_warnings": sum((x["_warnings"] for x in group), []),
            "_raw": "\n<<<체인 구분>>>\n".join(x["_raw"] for x in group),
        })

    merged.sort(key=lambda x: x["created_at"] or "")
    return merged


# 이 스크립트가 만들어낸 파일은 다시 입력으로 먹지 않는다
DERIVED = ("_parsed", "_제외됨", "_검토용")

# 수집기가 브라우저에서 다운로드시키는 파일 이름 패턴
# (크롬이 중복 시 붙이는 " (1)" 까지 잡히도록 뒤에 * 를 하나 더 둔다)
DOWNLOAD_PATTERN = "threads_manual_*posts*.json"


def pull_from_downloads(rawdir):
    """다운로드 폴더에 있는 수집 파일을 raw 폴더로 옮긴다.

    사용자가 손으로 파일을 옮기지 않아도 되게 하는 게 목적이다.
    복사가 아니라 '이동'인 이유: 다운로드 폴더에 남겨두면 다음 회차에
    같은 파일을 또 가져와 무엇이 새 것인지 헷갈린다.
    """
    downloads = Path.home() / "Downloads"
    if not downloads.is_dir():
        print(f"⚠ 다운로드 폴더를 못 찾음: {downloads}")
        return []

    rawdir.mkdir(parents=True, exist_ok=True)
    moved = []
    for src in sorted(downloads.glob(DOWNLOAD_PATTERN)):
        dst = rawdir / src.name
        n = 2
        while dst.exists():                      # 이름이 겹치면 덮어쓰지 않는다
            dst = rawdir / f"{src.stem}_{n}{src.suffix}"
            n += 1
        try:
            src.replace(dst)                     # 같은 드라이브면 즉시 이동
        except OSError:
            import shutil                        # 드라이브가 다르면 복사 후 삭제
            shutil.copy2(src, dst)
            src.unlink()
        moved.append(dst)

    if moved:
        print(f"📥 다운로드 폴더에서 {len(moved)}개 가져옴:")
        for m in moved:
            print(f"   · {m.name}")
    else:
        print("📥 다운로드 폴더에 새 수집 파일 없음 (이미 가져왔거나 아직 저장 안 함)")
    return moved


def collect_sources(inputs):
    """파일 경로와 폴더 경로를 섞어 받아 '수집기 원본 JSON' 목록만 돌려준다."""
    files = []
    for raw in inputs:
        p = Path(raw)
        if p.is_dir():
            for f in sorted(p.glob("*.json")):
                if any(d in f.name for d in DERIVED):
                    continue
                files.append(f)
        else:
            files.append(p)

    good = []
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"⚠ 건너뜀 (읽기 실패): {f.name} — {e}")
            continue
        if not isinstance(data, list) or not data or "raw_text" not in data[0]:
            print(f"⚠ 건너뜀 (수집기 원본 형식이 아님): {f.name}")
            continue
        good.append((f, data))
    return good


def dedupe(sources):
    """여러 파일을 합치면서 같은 글(id)이 겹치면 더 긴 쪽을 남긴다.

    이어서 수집하면 화면을 처음부터 다시 훑기 때문에 앞부분이 겹친다.
    겹친 게 정상이므로 조용히 버리지 말고 몇 건이 겹쳤는지 보고한다.
    """
    store = {}
    dup = 0
    for _, data in sources:
        for post in data:
            pid = post.get("id")
            if pid is None:
                continue
            prev = store.get(pid)
            if prev is None:
                store[pid] = post
                continue
            dup += 1
            if len(post.get("raw_text", "")) > len(prev.get("raw_text", "")):
                store[pid] = post
    merged = sorted(store.values(), key=lambda p: p.get("created_at") or "")
    return merged, dup


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", nargs="+",
                    help="수집기가 만든 JSON 파일들 (폴더를 주면 그 안의 원본 전부)")
    ap.add_argument("--account", default=DEFAULT_ACCOUNT,
                    help="남길 계정명 (안 주면 데이터에서 자동 감지)")
    ap.add_argument("--outdir", default=None, help="출력 폴더 (기본: 입력 파일과 같은 곳)")
    ap.add_argument("--name", default=None,
                    help="출력 파일 이름 앞부분 (기본: 파일 1개면 그 이름, 여러 개면 '전체합본')")
    ap.add_argument("--from-downloads", action="store_true",
                    help="다운로드 폴더의 수집 파일을 첫 입력 폴더로 먼저 옮긴다")
    args = ap.parse_args()

    if args.from_downloads:
        first_dir = next((Path(i) for i in args.input if Path(i).is_dir()), None)
        if first_dir is None:
            first_dir = Path(args.input[0]).parent
        pull_from_downloads(first_dir)
        print()

    sources = collect_sources(args.input)
    if not sources:
        print("❌ 읽을 수 있는 수집기 원본 JSON이 없습니다.")
        sys.exit(1)

    first = sources[0][0]
    outdir = Path(args.outdir) if args.outdir else first.parent
    outdir.mkdir(parents=True, exist_ok=True)

    print("=" * 56)
    print(f"입력 파일 {len(sources)}개")
    for f, d in sources:
        print(f"  · {f.name}: {len(d)}건")

    data, dup_count = dedupe(sources)
    total_in = len(data)
    if len(sources) > 1:
        print(f"  → 합치니 {sum(len(d) for _, d in sources)}건 중 {dup_count}건이 중복 "
              f"(같은 글) → 고유 {total_in}건")

    if not args.account:
        names = defaultdict(int)
        for p in data:
            if p.get("username"):
                names[p["username"]] += 1
        if not names:
            print("✗ 수집 데이터에 계정명(username)이 없다. --account 로 직접 지정할 것")
            return
        args.account = max(names, key=names.get)
        share = names[args.account] / max(len(data), 1) * 100
        print(f"  → 계정 자동 감지: {args.account} ({names[args.account]}건, {share:.0f}%)")
        if len(names) > 1:
            rest = ", ".join(f"{n}({c})" for n, c in
                             sorted(names.items(), key=lambda kv: -kv[1])[1:4])
            print(f"    (같이 잡힌 다른 계정: {rest} — 틀렸으면 --account 로 지정)")

    mine = [p for p in data if p.get("username") == args.account]
    others = [p for p in data if p.get("username") != args.account]

    parsed_all = [parse_one(p, args.account) for p in mine]

    # 남의 글에 단 답글(댓글 카드)은 도메인 지식 대상이 아니므로 분리
    comments = [p for p in parsed_all if p["is_comment"]]
    parsed = [p for p in parsed_all if not p["is_comment"]]

    merged = merge_chains(parsed)

    stem = args.name or (first.stem if len(sources) == 1 else "전체합본")
    out_main = outdir / f"{stem}_parsed.json"
    out_others = outdir / f"{stem}_제외됨_타계정.json"
    out_comments = outdir / f"{stem}_제외됨_댓글.json"

    # 저장할 땐 _raw 는 뺀다 (원본은 입력 파일에 그대로 있음)
    clean = [{k: v for k, v in m.items() if k != "_raw"} for m in merged]
    out_main.write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")
    out_others.write_text(json.dumps(others, ensure_ascii=False, indent=2), encoding="utf-8")
    out_comments.write_text(
        json.dumps([{k: v for k, v in c.items() if k != "_raw"} for c in comments],
                   ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- 검증 보고 ----
    warned = [m for m in merged if m["_warnings"]]
    chains = [m for m in merged if m.get("parts", 1) > 1]
    body_chars = sum(len(m["text"]) for m in merged)

    print()
    print("=" * 56)
    print(f"입력 총 건수(중복 제거 후): {total_in}")
    print(f"  ├ 대상 계정({args.account}) : {len(mine)}")
    print(f"  │   ├ 본인 게시물   : {len(parsed)}")
    print(f"  │   └ 남의 글 댓글(제외): {len(comments)}")
    print(f"  └ 타 계정(제외)     : {len(others)}")
    ok = len(parsed) + len(comments) + len(others) == total_in
    print(f"검산: {len(parsed)} + {len(comments)} + {len(others)} = "
          f"{len(parsed) + len(comments) + len(others)}"
          f"  {'✅ 일치' if ok else '❌ 불일치 — 확인 필요'}")
    print()
    print(f"체인 병합 후 건수    : {len(merged)}  (병합된 체인 {len(chains)}쌍)")
    print(f"본문 총 글자수       : {body_chars:,}")
    if merged:
        lens = [len(m["text"]) for m in merged]
        print(f"본문 길이 min/평균/max: {min(lens)} / {sum(lens)//len(lens)} / {max(lens)}")
        dates = sorted(m["created_at"][:10] for m in merged if m["created_at"])
        if dates:
            print(f"기간                : {dates[0]} ~ {dates[-1]}")
    print()
    print(f"⚠ 경고 달린 항목     : {len(warned)}")
    if warned:
        reasons = defaultdict(int)
        for m in warned:
            for w in set(m["_warnings"]):
                reasons[w] += 1
        for r, c in sorted(reasons.items(), key=lambda x: -x[1]):
            print(f"    - {r}: {c}건")
    print()
    print("출력:")
    print(f"  {out_main}   ← 정리 대상")
    print(f"  {out_others}")
    print(f"  {out_comments}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
