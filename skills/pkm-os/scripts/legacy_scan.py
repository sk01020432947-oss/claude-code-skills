#!/usr/bin/env python3
"""묵은 메모 일괄 스캔 (읽기 전용) — LLM 분류 전에 규모·중복·묻힌 할 일을 센다.

usage: python3 legacy_scan.py <폴더> <출력.csv> [--exclude 이름 ...]
       python3 legacy_scan.py --selftest
출력: 파일별 CSV(경로·최상위폴더·연도·글자수·본문해시·중복그룹·열린체크박스·바람표현) + 요약 출력.
파일을 고치거나 옮기지 않는다.
"""
import csv, hashlib, os, re, sys, tempfile, unicodedata
from collections import Counter, defaultdict
from datetime import datetime

FM = re.compile(r'\A---\n.*?\n---\n', re.S)
DATE = re.compile(r'^(?:date created|created|date):\s*["\']?(\d{4})', re.M | re.I)
OPEN_TASK = re.compile(r'^\s*[-*] \[ \]', re.M)
# ponytail: 바람 표현은 정규식 휴리스틱. 놓치는 문장은 LLM 단계에서 잡는다.
WISH = re.compile(r'읽어야|읽고 싶|가 ?보고 싶|가 ?봐야|해 ?봐야|해 ?보자|해야지|하고 싶|언젠가|나중에|TODO', re.I)


def norm(s):
    return unicodedata.normalize('NFC', s)


def scan(root, exclude=()):
    rows = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if not d.startswith('.') and norm(d) not in exclude]
        for f in fns:
            if not f.endswith('.md'):
                continue
            p = os.path.join(dp, f)
            try:
                t = open(p, encoding='utf-8', errors='replace').read()
            except OSError:
                continue
            m = FM.match(t)
            fm, body = (m.group(0), t[m.end():]) if m else ('', t)
            y = DATE.search(fm)
            st = os.stat(p)
            year = y.group(1) if y else datetime.fromtimestamp(getattr(st, 'st_birthtime', st.st_mtime)).strftime('%Y')
            key = re.sub(r'\s+', '', body).lower()
            rel = norm(os.path.relpath(p, root))
            rows.append({
                'path': rel, 'top': rel.split(os.sep)[0] if os.sep in rel else '(루트)', 'year': year,
                'chars': len(key), 'hash': hashlib.sha1(key.encode()).hexdigest()[:12] if len(key) >= 50 else '',
                'open_tasks': len(OPEN_TASK.findall(body)), 'wish': len(WISH.findall(body)),
            })
    groups = defaultdict(list)
    for r in rows:
        if r['hash']:
            groups[r['hash']].append(r)
    n = 0
    for g in groups.values():
        n += len(g) > 1
        for r in g:
            r['dup_group'] = n if len(g) > 1 else ''
    return rows


def summary(rows):
    dups = [r for r in rows if r.get('dup_group')]
    return {
        'total': len(rows),
        'dup_files': len(dups),
        'dup_groups': len({r['dup_group'] for r in dups}),
        'extra_copies': len(dups) - len({r['dup_group'] for r in dups}),
        'with_open_tasks': sum(r['open_tasks'] > 0 for r in rows),
        'open_tasks': sum(r['open_tasks'] for r in rows),
        'with_wish': sum(r['wish'] > 0 for r in rows),
        'by_top': Counter(r['top'] for r in rows).most_common(),
        'by_year': sorted(Counter(r['year'] for r in rows).items()),
    }


def selftest():
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(f'{d}/a'); os.makedirs(f'{d}/skip')
        body = '이 책 꼭 읽어야지. ' * 10
        open(f'{d}/a/1.md', 'w').write('---\ndate created: 2013-01-01\n---\n' + body)
        open(f'{d}/a/2.md', 'w').write(body.replace(' ', '  '))
        open(f'{d}/b.md', 'w').write('- [ ] 할 일\n- [x] 끝난 일\n' + 'x' * 60)
        open(f'{d}/skip/c.md', 'w').write(body)
        s = summary(scan(d, exclude={'skip'}))
        assert s['total'] == 3, s
        assert s['dup_groups'] == 1 and s['extra_copies'] == 1, s
        assert s['open_tasks'] == 1 and s['with_wish'] == 2, s
        assert ('2013', 1) in s['by_year'], s
    print('selftest ok')


if __name__ == '__main__':
    if sys.argv[1:2] == ['--selftest']:
        selftest(); sys.exit()
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    ex = set(sys.argv[sys.argv.index('--exclude') + 1:]) if '--exclude' in sys.argv else set()
    rows = scan(sys.argv[1], {norm(e) for e in ex})
    with open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, ['path', 'top', 'year', 'chars', 'hash', 'dup_group', 'open_tasks', 'wish'])
        w.writeheader(); w.writerows(rows)
    s = summary(rows)
    for k, v in s.items():
        print(f'{k}: {v}')
