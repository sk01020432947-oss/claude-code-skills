#!/usr/bin/env python3
"""녹화 자막(VTT) → 타임코드 대본, 편성표(JSON) 검증.

  python3 series.py clean in.vtt out.txt [--window 30]
  python3 series.py check plan.json in.vtt
  python3 series.py demo
"""
import json, re, sys

TS = re.compile(r'(\d+):(\d\d):(\d\d)[.,](\d+)\s*-->\s*(\d+):(\d\d):(\d\d)')


def sec(h, m, s):
    return int(h) * 3600 + int(m) * 60 + int(s)


def hms(t):
    return f"{t // 3600:02d}:{t % 3600 // 60:02d}:{t % 60:02d}"


def parse(vtt):
    """자동자막의 롤링 중복(앞 줄 반복)을 걷어낸 (시작초, 끝초, 새 텍스트) 목록."""
    out, last = [], ''
    for block in vtt.split('\n\n'):
        m = TS.search(block)
        if not m:
            continue
        lines = [re.sub(r'<[^>]+>', '', l).strip() for l in block.split('\n') if '-->' not in l]
        txt = ' '.join(l for l in lines[1:] if l) if lines and lines[0].isdigit() else ' '.join(l for l in lines if l)
        if not txt or txt == last:
            continue
        new = txt[len(last):].strip() if txt.startswith(last) else txt
        # 롤링 자막: 이전 줄의 마지막 줄이 이번 줄 앞에 붙어 나온다
        tail = last.split(' ')[-8:]
        for k in range(len(tail), 0, -1):
            pre = ' '.join(tail[-k:])
            if new.startswith(pre):
                new = new[len(pre):].strip()
                break
        if new:
            g = m.groups()
            out.append((sec(*g[0:3]), sec(*g[4:7]), new))
        last = txt
    return out


def clean(vtt, window=30):
    rows, buf, start = [], [], None
    for s, e, t in parse(vtt):
        if start is None:
            start = s
        buf.append(t)
        if s - start >= window:
            rows.append(f"[{hms(start)}] " + ' '.join(buf))
            buf, start = [], None
    if buf:
        rows.append(f"[{hms(start)}] " + ' '.join(buf))
    return '\n'.join(rows)


def to_sec(x):
    p = [int(v) for v in x.split(':')]
    return sum(v * 60 ** i for i, v in enumerate(reversed(p)))


def check(plan, vtt):
    """편성표 각 편의 구간이 자막 범위 안인지, 같은 종류끼리 겹치지 않는지, 첫 문장이 구간에 있는지."""
    cues = parse(vtt)
    end = max(e for _, e, _ in cues)
    errs = []
    for kind in ('long', 'short'):
        items = sorted((it for it in plan if it['type'] == kind), key=lambda it: to_sec(it['start']))
        for i, it in enumerate(items):
            a, b = to_sec(it['start']), to_sec(it['end'])
            if not (0 <= a < b <= end + 1):
                errs.append(f"{it['title']}: 구간 {it['start']}–{it['end']}이 자막 범위(0–{hms(end)}) 밖")
            if i and a < to_sec(items[i - 1]['end']):
                errs.append(f"{it['title']}: 앞 편 '{items[i - 1]['title']}'과 구간이 겹침")
            first = it.get('first_line', '')[:12]
            # 첫 문장은 구간 시작 ±5초 안에 있어야 한다(구간 중간에 있으면 시작점이 틀린 것)
            said = ' '.join(t for s, _, t in cues if a - 5 <= s <= min(a + 5, b))
            if first and first.replace(' ', '') not in said.replace(' ', ''):
                errs.append(f"{it['title']}: 첫 문장이 구간 시작 5초 안 자막에 없음")
    return errs


DEMO_VTT = """WEBVTT

00:00:00.000 --> 00:00:04.000
오늘은 은혜에 대해 말씀드리겠습니다

00:00:04.000 --> 00:00:08.000
오늘은 은혜에 대해 말씀드리겠습니다
첫째 은혜는 선물입니다

00:01:00.000 --> 00:01:05.000
둘째 은혜는 관계입니다
"""


def demo():
    cues = parse(DEMO_VTT)
    assert [t for *_, t in cues] == ['오늘은 은혜에 대해 말씀드리겠습니다', '첫째 은혜는 선물입니다', '둘째 은혜는 관계입니다'], cues
    ok = [{'type': 'short', 'title': 'A', 'start': '0:00', 'end': '0:30', 'first_line': '첫째 은혜는'},
          {'type': 'short', 'title': 'B', 'start': '0:58', 'end': '1:05', 'first_line': '둘째 은혜는'}]
    assert check(ok, DEMO_VTT) == [], check(ok, DEMO_VTT)
    bad = [dict(ok[0], end='1:00'), dict(ok[1], first_line='셋째')]
    assert len(check(bad, DEMO_VTT)) == 2, check(bad, DEMO_VTT)
    print('demo ok')


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['clean']:
        w = int(a[a.index('--window') + 1]) if '--window' in a else 30
        open(a[2], 'w').write(clean(open(a[1]).read(), w))
    elif a[:1] == ['check']:
        errs = check(json.load(open(a[1])), open(a[2]).read())
        print('\n'.join(errs) or 'OK: 모든 구간이 자막과 맞고 겹침 없음')
        sys.exit(1 if errs else 0)
    elif a[:1] == ['demo']:
        demo()
    else:
        print(__doc__)
