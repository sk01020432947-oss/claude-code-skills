#!/usr/bin/env python3
"""Find requests you typed 3+ times across Claude Code sessions -> skill candidates.
usage: scan.py [--days 30] [--min 3] [--sim 0.45] [--top 15]"""
import argparse, glob, json, os, re, time

def words(s):
    s = re.sub(r'https?://[\x21-\x7e]+', ' URL ', s)
    return {w for w in re.findall(r'[가-힣]{2,}|[A-Za-z]{3,}', s.lower())}

def jacc(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0

NOISE = ('<', '[', '#', 'Caveat', 'Another Claude session', 'This session is being continued',
         'Your response above', 'The app was quit', 'You are ', '너는 ')  # harness/agent text, not the user

def load(days):
    cut = time.time() - days * 86400
    out = []
    for f in glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')):
        if os.path.getmtime(f) < cut: continue
        for line in open(f, errors='ignore'):
            try: d = json.loads(line)
            except ValueError: continue
            c = d.get('message', {}).get('content') if d.get('type') == 'user' else None
            if not isinstance(c, str) or len(c) < 15 or len(c) > 1500 or c.startswith(NOISE): continue
            out.append((c.strip()[:300], os.path.basename(f)[:8], d.get('timestamp', '')[:10]))
    return out

def cluster(msgs, sim):
    groups = []  # [rep_words, [msgs]]
    for m in msgs:
        w = words(m[0])
        if len(w) < 3: continue
        for g in groups:
            if jacc(w, g[0]) >= sim: g[1].append(m); break
        else: groups.append([w, [m]])
    return groups  # ponytail: O(n*groups) greedy clustering; fine for a few thousand prompts

def skill_overlap(w):
    best = (0, '')
    for f in glob.glob(os.path.expanduser('~/.claude/skills/*/SKILL.md')):
        head = open(f, errors='ignore').read(1500)
        s = jacc(w, words(head))
        if s > best[0]: best = (s, f.split('/')[-2])
    return best

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=30); ap.add_argument('--min', type=int, default=3)
    ap.add_argument('--sim', type=float, default=0.45); ap.add_argument('--top', type=int, default=15)
    a = ap.parse_args()
    groups = [g for g in cluster(load(a.days), a.sim) if len({m[1] for m in g[1]}) >= a.min and len(g[1]) < 50]
    groups.sort(key=lambda g: -len(g[1]))
    for w, ms in groups[:a.top]:
        s, name = skill_overlap(w)
        print(f"\n## {len(ms)}회 · 세션 {len({m[1] for m in ms})}곳 · {min(m[2] for m in ms)}~{max(m[2] for m in ms)}")
        print(f"   예: {ms[0][0][:160]!r}")
        print(f"   가장 가까운 스킬: {name} (겹침 {s:.2f}) -> {'이미 있음, 그 스킬 호출' if s >= 0.25 else '스킬 후보'}")

def demo():
    g = cluster([("영상 html로 만들고 응용 아이디어 옵시디언 저장", 'a', '1'),
                 ("이 영상 html로 만들고 응용 아이디어 사례 옵시디언 저장해줘", 'b', '2'),
                 ("오늘 날씨 알려줘 서울 부탁", 'c', '3')], 0.45)
    assert len(g) == 2 and len(g[0][1]) == 2, g

if __name__ == '__main__':
    demo(); main()
