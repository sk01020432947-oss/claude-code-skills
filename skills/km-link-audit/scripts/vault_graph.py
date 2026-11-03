#!/usr/bin/env python3
"""
vault_graph.py — Obsidian 볼트의 wikilink 그래프를 한 번의 파일 순회로 계산한다.

왜 스크립트인가: 7,000개 노트의 링크 그래프를 LLM이 Glob+Grep+Read로 만들려면
수천 번의 도구 호출이 든다. 같은 일을 여기서는 몇 초에 끝낸다.
km-link-audit / km-link-strengthening 두 스킬이 공유한다.

사용법:
  python vault_graph.py --vault "/Users/kbg1023/obsidian/Obsidian 2025"
  python vault_graph.py --vault ... --folder "1004. sermon"
  python vault_graph.py --vault ... --json > graph.json
  python vault_graph.py --vault ... --note "노트제목"     # 그 노트의 이웃만
  python vault_graph.py --selftest                        # 의존성 없는 자가검증

출력은 사람이 읽는 요약(기본) 또는 --json(스킬이 소비하는 구조화 데이터).
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

# ── 링크 문법 ────────────────────────────────────────────────────────────
# [[대상]] / [[대상|별칭]] / [[대상#섹션]] / [[폴더/대상]] / ![[임베드]]
LINK_RE = re.compile(r'(!?)\[\[([^\]\[|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]')
TAG_RE = re.compile(r'^tags:\s*(?:\[(.*?)\]|(.*))$', re.MULTILINE)
FENCE_RE = re.compile(r'```.*?```|~~~.*?~~~|`[^`\n]*`', re.DOTALL)

# 링크처럼 생겼지만 링크가 아닌 것.
# 웹 클리퍼가 CSS를 긁어오며 `fill: [[e4e4e7]] !important;` 꼴을 만든다.
# 이 볼트에서만 1,100건 — 걸러내지 않으면 깨진 링크 통계가 통째로 망가진다.
NOT_A_LINK_RE = re.compile(r'^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$')

# 노트가 아닌 것 — 세면 결과가 흐려진다. --exclude로 덮어쓸 수 있다.
# Tags/ 는 태그 노트가 링크 대상일 수 있어 기본 제외에서 뺐다.
DEFAULT_EXCLUDES = [
    '.obsidian', '.trash', '.git', '.smart-env', '.space',
    '008. 첨부자료', '009. 설정', '100. Themes',
    '999-Attachments', 'attachments', 'Excalidraw',
]

# 미분류 원자료. 큐레이션 상태를 볼 때는 빼는 게 맞다 (--no-raw).
RAW_FOLDERS = ['001. inbox', 'inbox', 'Clippings', '002. Folder/FastCampus/Clippings']


def norm(s):
    """링크 대상과 파일명을 같은 잣대로 비교하기 위한 정규화."""
    return s.strip().lower().replace('\\', '/')


def parse_frontmatter_tags(text):
    """frontmatter의 tags를 뽑는다. YAML 파서 없이 흔한 세 형태를 모두 받는다.

        tags: [a, b]        인라인 배열
        tags: a, b          쉼표 나열
        tags:               블록 목록
          - a
          - b
    """
    if not text.startswith('---'):
        return []
    end = text.find('\n---', 3)
    if end == -1:
        return []
    fm = text[3:end]

    out, in_block = [], False
    for line in fm.split('\n'):
        if in_block:
            m = re.match(r'^\s+-\s*(.+?)\s*$', line)
            if m:
                out.append(m.group(1))
                continue
            in_block = False
        m = re.match(r'^tags:\s*(.*)$', line)
        if m:
            rest = m.group(1).strip()
            if not rest:
                in_block = True          # 다음 줄부터 블록 목록
            else:
                out += re.split(r'\s*,\s*', rest.strip('[]'))

    clean = []
    for t in out:
        t = t.strip().strip('"\'').lstrip('#').strip()
        if t:
            clean.append(t)
    return clean


def extract_links(text):
    """본문에서 진짜 wikilink만 뽑는다.

    코드 펜스/인라인 코드를 먼저 지우고, 색상코드처럼 링크가 아닌 것을 버린다.
    이 두 단계를 건너뛰면 웹 클리핑이 많은 볼트에서 통계가 무의미해진다.
    """
    clean = FENCE_RE.sub(' ', text)
    links, embeds = [], []
    for bang, target in LINK_RE.findall(clean):
        t = target.strip()
        if not t or NOT_A_LINK_RE.match(t):
            continue
        (embeds if bang else links).append(t)
    return links, embeds


def scan(vault, excludes=None):
    """볼트를 한 번 걸으며 노트별 링크·태그를 수집한다.

    항상 볼트 전체를 색인한다. 폴더 좁히기는 보고 단계에서 한다 —
    색인을 좁히면 폴더 밖을 가리키는 정상 링크가 전부 깨진 것으로 잡힌다.
    """
    excludes = set(norm(e) for e in (excludes if excludes is not None else DEFAULT_EXCLUDES))
    root = vault

    notes = {}          # rel_path -> {name, folder, links, embeds, tags, size}
    by_name = defaultdict(list)   # 정규화된 basename -> [rel_path]
    by_path = {}        # 정규화된 확장자 없는 전체 경로 -> rel_path

    for dirpath, dirnames, filenames in os.walk(root):
        # 제외 폴더는 통째로 가지치기 — 들어가지도 않는다
        dirnames[:] = [d for d in dirnames if norm(d) not in excludes]
        for fn in filenames:
            if not fn.lower().endswith('.md'):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, vault).replace('\\', '/')
            if any(norm(part) in excludes for part in rel.split('/')[:-1]):
                continue
            try:
                with open(full, 'r', encoding='utf-8', errors='replace') as f:
                    text = f.read()
            except OSError:
                continue

            stem = fn[:-3]
            links, embeds = extract_links(text)

            notes[rel] = {
                'name': stem,
                'folder': os.path.dirname(rel) or '(root)',
                'links': links,
                'embeds': embeds,
                'tags': parse_frontmatter_tags(text),
                'size': len(text),
            }
            by_name[norm(stem)].append(rel)
            by_path[norm(rel[:-3])] = rel

    # 동명 노트는 경로가 짧은 쪽이 이긴다 — 미리 정렬해 두면 해석이 O(1)
    for k in by_name:
        by_name[k].sort(key=lambda p: (p.count('/'), len(p)))

    return notes, by_name, by_path


def resolve(target, by_name, by_path):
    """wikilink 대상을 실제 노트 경로로 해석. Obsidian 규칙 근사.

    1) 경로째 일치 ([[폴더/노트]])
    2) basename 일치 ([[노트]]) — 동명이 여럿이면 경로가 짧은 쪽

    두 조회 모두 dict 색인이라 상수 시간. 링크마다 전체 노트를 훑으면
    7,000개 볼트에서 1억 회 비교가 되어 2분을 넘긴다.
    """
    t = norm(target)
    if t.endswith('.md'):
        t = t[:-3]
    hit = by_path.get(t)
    if hit:
        return hit
    cands = by_name.get(t.split('/')[-1], [])
    return cands[0] if cands else None


def build(notes, by_name, by_path, concept_threshold=3):
    """해석·집계. 링크 그래프의 모든 지표가 여기서 나온다.

    해석 실패 링크는 두 갈래로 나눈다:
      · 여러 노트가 같은 대상을 가리킴 → 개념 허브를 미리 걸어둔 것 (의도적)
      · 한두 노트만 가리킴            → 오타이거나 파일이 옮겨진 것 (고칠 것)
    섞어 세면 후자가 전자에 묻혀 안 보인다.
    """
    out_links = defaultdict(set)
    in_links = defaultdict(set)
    unresolved = defaultdict(set)   # 대상 -> {출처 노트}

    for rel, meta in notes.items():
        for target in meta['links']:
            hit = resolve(target, by_name, by_path)
            if hit is None:
                unresolved[target].add(rel)
            elif hit != rel:
                out_links[rel].add(hit)
                in_links[hit].add(rel)

    broken, concepts = [], []
    for target, srcs in unresolved.items():
        if len(srcs) >= concept_threshold:
            concepts.append((target, len(srcs), sorted(srcs)))
        else:
            for s in srcs:
                broken.append((s, target))

    orphans, dead_ends, hubs, one_way = [], [], [], []
    for rel in notes:
        o, i = len(out_links[rel]), len(in_links[rel])
        if o == 0 and i == 0:
            orphans.append(rel)
        elif o == 0:
            dead_ends.append(rel)
        if o + i > 10:
            hubs.append((rel, o + i))
        for tgt in out_links[rel]:
            if rel not in out_links[tgt]:
                one_way.append((rel, tgt))

    # 폴더별 평균 링크 수 대비 절반 이하 = 연결 부족
    folder_tot, folder_cnt = defaultdict(int), defaultdict(int)
    for rel, meta in notes.items():
        folder_tot[meta['folder']] += len(out_links[rel]) + len(in_links[rel])
        folder_cnt[meta['folder']] += 1
    folder_avg = {f: folder_tot[f] / folder_cnt[f] for f in folder_cnt}

    under = []
    for rel, meta in notes.items():
        avg = folder_avg[meta['folder']]
        deg = len(out_links[rel]) + len(in_links[rel])
        if avg >= 2 and deg < avg * 0.5 and rel not in orphans:
            under.append((rel, deg, round(avg, 1)))

    # 태그가 5개 이상 모였는데 그 주제의 MOC가 없으면 허브 부재
    tag_notes = defaultdict(list)
    for rel, meta in notes.items():
        for t in meta['tags']:
            tag_notes[t].append(rel)
    moc_names = {norm(m['name']) for m in notes.values() if 'moc' in norm(m['name'])}
    missing_hubs = [
        (t, len(v), v) for t, v in tag_notes.items()
        if len(v) >= 5 and not any(norm(t) in mn for mn in moc_names)
    ]

    return {
        'out_links': out_links, 'in_links': in_links, 'broken': broken,
        'concepts': sorted(concepts, key=lambda x: -x[1]),
        'orphans': orphans, 'dead_ends': dead_ends, 'hubs': hubs,
        'one_way': one_way, 'under': under, 'missing_hubs': missing_hubs,
        'folder_avg': folder_avg, 'folder_cnt': folder_cnt,
    }


def in_scope(rel, folder):
    """보고 대상인가. folder가 None이면 전부."""
    return folder is None or rel == folder or rel.startswith(folder.rstrip('/') + '/')


# 제목에서 뽑아도 아무것도 구분해 주지 않는 말들
STOP_KW = {'무제', 'untitled', '노트', 'note', '정리', '메모', '자료', '내용', '관련', '복사본'}
DATE_KW = re.compile(r'^\d{2,14}$')


def title_keywords(name):
    """제목에서 식별력 있는 키워드만. 날짜·불용어·한 글자는 버린다."""
    parts = re.split(r'[\s\-_·,()\[\]{}/]+', name.lower())
    return {p for p in parts
            if len(p) >= 2 and p not in STOP_KW and not DATE_KW.match(p)}


def summarize(notes, g, top, folder=None):
    scoped = [r for r in notes if in_scope(r, folder)]
    total = len(scoped)
    if not total:
        return f"'{folder}' 안에 노트가 없습니다. 폴더명을 확인하세요."
    S = set(scoped)
    total_links = sum(len(g['out_links'][r]) for r in scoped)
    orphans = [r for r in g['orphans'] if r in S]
    dead = [r for r in g['dead_ends'] if r in S]
    broken = [(s, t) for s, t in g['broken'] if s in S]
    oneway = [(a, b) for a, b in g['one_way'] if a in S]
    under = [u for u in g['under'] if u[0] in S]
    hubs = [h for h in g['hubs'] if h[0] in S]
    # 개념링크·태그군도 범위 안 노트가 관여한 것만 — 안 그러면 폴더를 좁혀도 전체 값이 나온다
    concepts = [(t, sum(1 for s in srcs if s in S)) for t, _, srcs in g['concepts']]
    concepts = sorted([c for c in concepts if c[1] > 0], key=lambda x: -x[1])
    mhubs = [(t, sum(1 for n in ns if n in S)) for t, _, ns in g['missing_hubs']]
    mhubs = sorted([m for m in mhubs if m[1] >= 5], key=lambda x: -x[1])

    L = []
    A = L.append
    if folder:
        A(f"범위: {folder}   (색인은 볼트 전체 {len(notes):,}개 — 폴더 밖 링크도 정상 해석)")
    A(f"노트 {total:,}개 · 해석된 링크 {total_links:,}개 · "
      f"평균 {total_links / total:.2f}개/노트")
    A("")
    A(f"고아(양쪽 0)        {len(orphans):>6,}   {len(orphans) / total * 100:.1f}%")
    A(f"데드엔드(나감 0)    {len(dead):>6,}")
    A(f"깨진 링크 ★고칠것   {len(broken):>6,}")
    A(f"미해결 개념링크     {len(concepts):>6,}   여러 노트가 가리킴 = 대체로 의도적")
    A(f"단방향 링크         {len(oneway):>6,}")
    A(f"연결 부족           {len(under):>6,}")
    A(f"허브(연결 10+)      {len(hubs):>6,}")
    A(f"MOC 없는 태그군     {len(mhubs):>6,}")
    A("")

    fc = {f: c for f, c in g['folder_cnt'].items()
          if folder is None or in_scope(f + '/_', folder)}
    if fc:
        A(f"── 폴더별 (노트 많은 순 상위 {top}) ──")
        A(f"{'폴더':<44}{'노트':>7}{'평균연결':>9}")
        for f, c in sorted(fc.items(), key=lambda x: -x[1])[:top]:
            A(f"{f[:43]:<44}{c:>7,}{g['folder_avg'][f]:>9.2f}")

    if broken:
        A("")
        A(f"── 깨진 링크 · 오타이거나 옮겨진 파일 (상위 {top}) ──")
        for src, tgt in broken[:top]:
            A(f"  [[{tgt}]]  ← {src}")

    if concepts:
        A("")
        A(f"── 미해결 개념링크 · 만들면 곧바로 허브가 될 노트 (상위 {top}) ──")
        for tgt, n in concepts[:top]:
            A(f"  {n:>4}개 노트가 가리킴   [[{tgt}]]")

    if hubs:
        A("")
        A(f"── 허브 (상위 {top}) ──")
        for rel, deg in sorted(hubs, key=lambda x: -x[1])[:top]:
            A(f"  {deg:>4}  {rel}")

    if mhubs:
        A("")
        A(f"── MOC 만들 만한 태그 (상위 {top}) ──")
        for t, n in mhubs[:top]:
            A(f"  {n:>4}개  #{t}")

    return "\n".join(L)


def neighbors(note, notes, by_name, by_path, g, top):
    """한 노트의 이웃 — km-link-strengthening이 후보를 고를 때 쓴다."""
    rel = resolve(note, by_name, by_path)
    if rel is None:
        return f"노트를 찾지 못함: {note}"
    meta = notes[rel]
    L = [f"기준 노트: {rel}", f"태그: {', '.join(meta['tags']) or '(없음)'}", ""]
    L.append(f"이 노트가 가리킴 ({len(g['out_links'][rel])}):")
    for t in sorted(g['out_links'][rel])[:top]:
        L.append(f"  → {t}")
    L.append(f"이 노트를 가리킴 ({len(g['in_links'][rel])}):")
    for s in sorted(g['in_links'][rel])[:top]:
        L.append(f"  ← {s}")

    # 연결 후보. 같은 폴더라는 사실만으로는 아무 뜻이 없다 —
    # 제목 키워드나 태그가 겹쳐야 후보로 올린다. (스킬의 점수표와 같은 배점)
    my_kw = title_keywords(meta['name'])
    cand = []
    linked = g['out_links'][rel] | g['in_links'][rel]
    for other, om in notes.items():
        if other == rel or other in linked:
            continue
        shared_kw = my_kw & title_keywords(om['name'])
        shared_tag = set(om['tags']) & set(meta['tags'])
        if not shared_kw and not shared_tag:
            continue                      # 폴더만 같은 것은 신호가 아니다
        score = 3 * bool(shared_kw) + 2 * bool(shared_tag)
        score += 2 * (om['folder'] == meta['folder'])
        why = []
        if shared_kw:
            why.append('키워드 ' + ','.join(sorted(shared_kw)[:3]))
        if shared_tag:
            why.append('태그 ' + ','.join(sorted(shared_tag)[:2]))
        if om['folder'] == meta['folder']:
            why.append('같은 폴더')
        cand.append((score, other, ' · '.join(why)))

    L.append("")
    if cand:
        L.append(f"연결 후보 · 사전 점수 (상위 {top}) — 최종 판단은 본문을 보고:")
        for score, other, why in sorted(cand, key=lambda x: (-x[0], x[1]))[:top]:
            L.append(f"  {score}점  {other}")
            L.append(f"        {why}")
    else:
        L.append("연결 후보 없음 — 제목 키워드도 태그도 겹치는 노트가 없습니다.")
    return "\n".join(L)


def selftest():
    """의존성 없는 자가검증. 링크 파싱과 그래프 계산이 깨지면 여기서 잡힌다."""
    got = LINK_RE.findall(
        "[[A]] [[B|별칭]] [[C#섹션]] [[폴더/D]] ![[E.png]] [[F#s|별칭]]"
    )
    assert [t.strip() for _, t in got] == ['A', 'B', 'C', '폴더/D', 'E.png', 'F'], got
    assert [b for b, _ in got] == ['', '', '', '', '!', ''], got

    notes = {
        'x/A.md': {'name': 'A', 'folder': 'x', 'links': ['B', '없는노트'],
                   'embeds': [], 'tags': ['t1'], 'size': 10},
        'x/B.md': {'name': 'B', 'folder': 'x', 'links': ['A'],
                   'embeds': [], 'tags': ['t1'], 'size': 10},
        'y/C.md': {'name': 'C', 'folder': 'y', 'links': [],
                   'embeds': [], 'tags': [], 'size': 10},
    }
    by_name = defaultdict(list)
    by_path = {}
    for rel, m in notes.items():
        by_name[norm(m['name'])].append(rel)
        by_path[norm(rel[:-3])] = rel

    g = build(notes, by_name, by_path)
    assert g['orphans'] == ['y/C.md'], g['orphans']
    assert len(g['broken']) == 1 and g['broken'][0][1] == '없는노트', g['broken']
    assert g['one_way'] == [], g['one_way']          # A↔B는 상호 링크
    assert 'x/A.md' not in g['dead_ends'], g['dead_ends']

    # 단방향 검출: B가 A를 안 가리키게 바꾸면 A→B가 단방향으로 잡혀야 한다
    notes['x/B.md']['links'] = []
    g2 = build(notes, by_name, by_path)
    assert g2['one_way'] == [('x/A.md', 'x/B.md')], g2['one_way']
    assert 'x/B.md' in g2['dead_ends'], g2['dead_ends']

    # 경로 지정 링크가 basename 링크보다 우선 해석되는지
    assert resolve('x/A', by_name, by_path) == 'x/A.md'
    assert resolve('A', by_name, by_path) == 'x/A.md'
    assert resolve('없음', by_name, by_path) is None

    # frontmatter 태그 세 형태 — 목록형에서 앞 공백·하이픈이 남으면 태그가 안 맞는다
    assert parse_frontmatter_tags('---\ntags: [a, b]\n---\n') == ['a', 'b']
    assert parse_frontmatter_tags('---\ntags: a, b\n---\n') == ['a', 'b']
    assert parse_frontmatter_tags('---\ntags:\n  - a\n  - b\ntitle: x\n---\n') == ['a', 'b']
    assert parse_frontmatter_tags('---\ntags:\n  - "#c"\n---\n') == ['c']
    assert parse_frontmatter_tags('본문만 있음') == []

    # 잡음 제거: CSS 색상값과 코드 블록 안의 대괄호는 링크가 아니다
    lk, em = extract_links('fill: [[e4e4e7]] !important; [[진짜노트]] ![[그림.png]]')
    assert lk == ['진짜노트'], lk
    assert em == ['그림.png'], em
    assert extract_links('```\n[[코드안]]\n```\n[[밖]]')[0] == ['밖']
    assert extract_links('`[[인라인]]` [[밖]]')[0] == ['밖']

    # 미해결 링크 분류: 3개 이상이 가리키면 개념링크, 아니면 깨진 링크
    n2 = {f'n{i}.md': {'name': f'n{i}', 'folder': '.', 'links': ['공통개념'],
                       'embeds': [], 'tags': [], 'size': 1} for i in range(4)}
    n2['solo.md'] = {'name': 'solo', 'folder': '.', 'links': ['오타노트'],
                     'embeds': [], 'tags': [], 'size': 1}
    bn2, bp2 = defaultdict(list), {}
    for rel, m in n2.items():
        bn2[norm(m['name'])].append(rel)
        bp2[norm(rel[:-3])] = rel
    g3 = build(n2, bn2, bp2, concept_threshold=3)
    assert [(t, c) for t, c, _ in g3['concepts']] == [('공통개념', 4)], g3['concepts']
    assert g3['broken'] == [('solo.md', '오타노트')], g3['broken']

    # 제목 키워드: 날짜와 불용어는 신호가 아니다
    assert title_keywords('로마서 강해 - 2026-01-03') == {'로마서', '강해'}
    assert title_keywords('무제 8') == set()
    assert 'graphrag' in title_keywords('GraphRAG 아키텍처 분석')

    # 보고 범위: 색인은 전체, 필터는 경로 접두사
    assert in_scope('a/b/c.md', 'a/b') and in_scope('a/b/c.md', None)
    assert not in_scope('ab/c.md', 'a')      # 접두사 부분일치에 속으면 안 된다

    print("selftest OK")


def main():
    p = argparse.ArgumentParser(description="Obsidian 볼트 링크 그래프 분석")
    p.add_argument('--vault', help='볼트 루트 경로')
    p.add_argument('--folder', help='이 폴더만 보고 (색인은 항상 볼트 전체)')
    p.add_argument('--note', help='이 노트의 이웃과 연결 후보만 출력')
    p.add_argument('--exclude', nargs='*', default=None, help='제외 폴더명 (기본값 대체)')
    p.add_argument('--no-raw', action='store_true',
                   help=f'미분류 원자료 폴더 제외: {", ".join(RAW_FOLDERS)}')
    p.add_argument('--concept-threshold', type=int, default=3,
                   help='이 수 이상의 노트가 가리키는 미해결 링크는 의도적 개념링크로 분류 (기본 3)')
    p.add_argument('--top', type=int, default=20, help='목록 출력 개수')
    p.add_argument('--json', action='store_true', help='구조화 출력')
    p.add_argument('--selftest', action='store_true')
    a = p.parse_args()

    if a.selftest:
        selftest()
        return
    if not a.vault:
        p.error('--vault 가 필요합니다 (또는 --selftest)')
    if not os.path.isdir(a.vault):
        p.error(f'볼트 경로가 없습니다: {a.vault}')

    excl = a.exclude if a.exclude is not None else list(DEFAULT_EXCLUDES)
    if a.no_raw:
        excl += RAW_FOLDERS

    notes, by_name, by_path = scan(a.vault, excl)
    if not notes:
        print("md 파일을 찾지 못했습니다. --vault/--exclude 를 확인하세요.")
        return
    g = build(notes, by_name, by_path, a.concept_threshold)

    if a.note:
        print(neighbors(a.note, notes, by_name, by_path, g, a.top))
        return

    if a.json:
        S = {r for r in notes if in_scope(r, a.folder)}
        total_links = sum(len(g['out_links'][r]) for r in S)
        json.dump({
            'scope': a.folder or '(볼트 전체)',
            'indexed_notes': len(notes),
            'scoped_notes': len(S),
            'total_links': total_links,
            'avg_links': round(total_links / len(S), 3) if S else 0,
            'orphans': [r for r in g['orphans'] if r in S],
            'dead_ends': [r for r in g['dead_ends'] if r in S],
            'broken': [{'source': s, 'target': t} for s, t in g['broken'] if s in S],
            'unresolved_concepts': [{'target': t, 'referenced_by': n} for t, n in g['concepts']],
            'one_way': [{'from': f, 'to': t} for f, t in g['one_way'] if f in S],
            'under_connected': [{'note': n, 'degree': d, 'folder_avg': av}
                                for n, d, av in g['under'] if n in S],
            'hubs': [{'note': n, 'degree': d}
                     for n, d in sorted(g['hubs'], key=lambda x: -x[1]) if n in S],
            'missing_hubs': [{'tag': t, 'count': c} for t, c in g['missing_hubs']],
            'folders': {f: {'notes': c, 'avg_links': round(g['folder_avg'][f], 3)}
                        for f, c in g['folder_cnt'].items()},
        }, sys.stdout, ensure_ascii=False, indent=2)
    else:
        print(summarize(notes, g, a.top, a.folder))


if __name__ == '__main__':
    main()
