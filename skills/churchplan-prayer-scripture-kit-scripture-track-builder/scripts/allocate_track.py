#!/usr/bin/env python3
"""allocate_track.py — 연간 통독 트랙의 일별 권·장 배정(결정론).

정경 권·장 수(bible_validator.BOOK_CHAPTERS)로 트랙별 일별 배정을 *결정론* 생성한다.
권 경계를 존중하고(한 portion은 한 권 안의 연속 장), 장을 누락·중복 없이 모두 배정한다.
LLM 자연어 추론이 아니라 산술로 schedule[]을 만든다(권 경계 침범·장 오산 차단).

지원 트랙(references/scripture-track-catalog.md §1):
  1년 통독   — 창세기→요한계시록 1189장 / days(기본 365)
  신약 1년   — 마태복음→요한계시록 260장 / days(기본 365, 장보다 날이 많으면 절 단위 배정)
  시편잠언   — 시편 150편 + 잠언 31장 / days

사용:
  python3 allocate_track.py "1년 통독" [일수]            # JSON schedule[] 출력
  python3 allocate_track.py "신약 1년" 365
종료코드: 0 = 성공, 2 = 알 수 없는 트랙/인자 오류
"""
from __future__ import annotations
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bible_validator as bv  # noqa: E402

# 정경 권 순서(BOOK_CHAPTERS 삽입 순서 = 창세기…요한계시록). OT 39 + NT 27.
ALL_BOOKS = list(bv.BOOK_CHAPTERS.keys())
NT_BOOKS = ALL_BOOKS[39:]  # 마태복음부터
OT_BOOKS = ALL_BOOKS[:39]

# 트랙명 → (책 목록, 기본 일수). 동의어 허용.
TRACKS = {
    "1년 통독": (ALL_BOOKS, 365),
    "1년통독": (ALL_BOOKS, 365),
    "신약 1년": (NT_BOOKS, 365),
    "신약1년": (NT_BOOKS, 365),
    "시편잠언": (["시편", "잠언"], 181),
    "시편·잠언": (["시편", "잠언"], 181),
}


def _flatten_chapters(books):
    """[(책, 장번호), ...] 정경 순서대로."""
    seq = []
    for b in books:
        for ch in range(1, len(bv.BOOK_CHAPTERS[b]) + 1):
            seq.append((b, ch))
    return seq


def _portions_from_run(run):
    """연속 run을 권 경계로 끊어 표기로. 원소는 (책,장)=장 전체 또는 (책,장,절)=절 하나.
    통째인 장은 '책 a-b'로 묶고, 일부만 든 장은 '책 장:a-b'로 쓴다."""
    # 1) 장 단위로 모은다: [(책, 장, 시작절|None, 끝절|None)] — None은 장 전체
    chunks = []
    for u in run:
        book, ch = u[0], u[1]
        if len(u) == 2:
            chunks.append([book, ch, None, None])
        elif chunks and chunks[-1][:2] == [book, ch] and chunks[-1][3] == u[2] - 1:
            chunks[-1][3] = u[2]
        else:
            chunks.append([book, ch, u[2], u[2]])
    for c in chunks:  # 1절부터 마지막 절까지 다 들었으면 장 전체로 취급
        if c[2] == 1 and c[3] == bv.BOOK_CHAPTERS[c[0]][c[1] - 1]:
            c[2] = c[3] = None
    # 2) 같은 권의 연속된 '장 전체'끼리 묶어 표기
    portions = []
    i = 0
    while i < len(chunks):
        book, start, v1, v2 = chunks[i]
        if v1 is not None:
            portions.append(f"{book} {start}:{v1}" if v1 == v2 else f"{book} {start}:{v1}-{v2}")
            i += 1
            continue
        end = start
        j = i + 1
        while j < len(chunks) and chunks[j][0] == book and chunks[j][1] == end + 1 and chunks[j][2] is None:
            end = chunks[j][1]
            j += 1
        portions.append(f"{book} {start}" if start == end else f"{book} {start}-{end}")
        i = j
    return portions


def allocate_track(track: str, days: int | None = None):
    """트랙·일수 → schedule[] = [{'unit':'N일','portions':[...]}]. 결정론."""
    if track not in TRACKS:
        raise ValueError(f"알 수 없는 트랙: {track} (지원: {', '.join(sorted(set(TRACKS)))})")
    books, default_days = TRACKS[track]
    # days=None(미지정) → 기본값. days=0·음수(명시) → 오류(0 or default 누수 차단).
    n_days = default_days if days is None else days
    if n_days < 1:
        raise ValueError(f"일수는 1 이상: {n_days}")
    seq = _flatten_chapters(books)
    total = len(seq)
    if n_days > total:  # 장보다 날이 많으면 절 단위로 나눈다(예: 신약 260장을 365일에) — 일수를 줄이지 않는다
        seq = [(b, ch, v) for b, ch in seq for v in range(1, bv.BOOK_CHAPTERS[b][ch - 1] + 1)]
        total = len(seq)
        if n_days > total:
            raise ValueError(f"일수({n_days})가 이 트랙의 총 절 수({total})보다 많음")
    schedule = []
    pos = 0
    for d in range(n_days):
        remaining_days = n_days - d
        take = (total - pos + remaining_days - 1) // remaining_days  # 남은 장 균등 올림 분배
        run = seq[pos:pos + take]
        pos += take
        schedule.append({"unit": f"{d + 1}일", "portions": _portions_from_run(run)})
    return schedule


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    track = sys.argv[1]
    try:
        days = int(sys.argv[2]) if len(sys.argv) > 2 else None
        sched = allocate_track(track, days)
    except ValueError as ex:
        print(f"[오류] {ex}")
        return 2
    print(json.dumps(sched, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
