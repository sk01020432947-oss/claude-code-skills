#!/usr/bin/env python3
"""Claude 스킬 폴더 → 제미나이 앱 '스킬' 업로드용 .zip 변환·점검.

제미나이 규격(Google 도움말 17094296, 2026-10 기준):
- 루트에 SKILL.md, name은 소문자-하이픈, description ≤ 1024자, 전체 ≤ 100MB
- .docx/.doc/.xlsx 등 바이너리 불가, 스크립트는 외부 웹 접속 불가
사용: python3 export.py <스킬이름|경로> ... [--out DIR] [--nested]
"""
import argparse, os, re, sys, unicodedata, zipfile
import yaml

ALLOW = {'.txt', '.md', '.rst', '.rtf', '.tex', '.log', '.py', '.sh', '.json', '.yaml', '.yml',
         '.csv', '.toml', '.xml', '.sql', '.html', '.css', '.svg', '.pdf', '.jpg', '.jpeg', '.png'}
SKILLS = os.path.expanduser('~/.claude/skills')
OUT = os.path.expanduser('~/Desktop/cysjavis/AI동향_검토/제미나이스킬_업로드팩')
NAME_RE = re.compile(r'[a-z0-9]+(-[a-z0-9]+)*')
# Claude Code 전용 의존: 제미나이에서는 동작하지 않는다
CLAUDE_ONLY = re.compile(r'mcp__|\bBash\b|AskUserQuestion|\bAgent\b 도구|Skill 도구|~/\.claude|subagent')
MAX_DESC, MAX_BYTES = 1024, 100 * 1024 * 1024


def split_front(text):
    m = re.match(r'^---\n(.*?)\n---\n?(.*)$', text, re.S)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def fix_front(meta, folder):
    """제미나이 규격에 맞게 name/description만 고친다. 고친 항목 목록을 돌려준다."""
    notes = []
    name = str(meta.get('name') or folder)
    if not NAME_RE.fullmatch(name):
        name = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-') or re.sub(r'[^a-z0-9]+', '-', folder.lower()).strip('-')
        notes.append(f'name → {name}')
    desc = ' '.join(str(meta.get('description') or '').split())
    if len(desc) > MAX_DESC:
        desc = desc[:MAX_DESC - 1] + '…'
        notes.append(f'description {MAX_DESC}자로 절단')
    if not desc:
        notes.append('경고: description 없음 — 자동 호출이 안 됨')
    return {'name': name, 'description': desc}, notes


def export(src, out_dir, nested=False):
    folder = os.path.basename(os.path.normpath(src))
    with open(os.path.join(src, 'SKILL.md'), encoding='utf-8') as f:
        meta, body = split_front(f.read())
    front, notes = fix_front(meta, folder)
    if CLAUDE_ONLY.search(body):
        notes.append('주의: 본문에 Claude Code 전용 도구(MCP/Bash/에이전트) 언급 — 제미나이에서 그 단계는 텍스트 지침으로만 작동')
    skill_md = '---\n' + yaml.safe_dump(front, allow_unicode=True, sort_keys=False, width=10**6) + '---\n' + body
    prefix = front['name'] + '/' if nested else ''
    zpath = os.path.join(out_dir, front['name'] + '.zip')
    total, skipped, scripts = len(skill_md.encode()), [], 0
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr(prefix + 'SKILL.md', skill_md)
        for root, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if not d.startswith(('.', '__'))]
            for fn in files:
                p = os.path.join(root, fn)
                rel = os.path.relpath(p, src)
                if rel == 'SKILL.md' or fn.startswith('.'):
                    continue
                ext = os.path.splitext(fn)[1].lower()
                if ext not in ALLOW:
                    skipped.append(rel)
                    continue
                scripts += ext in ('.py', '.sh')
                total += os.path.getsize(p)
                z.write(p, unicodedata.normalize('NFC', prefix + rel))  # 맥 NFD 파일명 → NFC
    if total > MAX_BYTES:
        os.remove(zpath)
        return None, notes + [f'실패: {total/1e6:.0f}MB > 100MB']
    if skipped:
        notes.append(f'제외(미지원 형식) {len(skipped)}개: ' + ', '.join(skipped[:5]) + (' …' if len(skipped) > 5 else ''))
    if scripts:
        notes.append(f'스크립트 {scripts}개 포함 — 제미나이는 외부 웹 접속 차단, 실행 보장 없음(영상 권고: 텍스트 지침으로)')
    return zpath, notes


def demo():
    meta, body = split_front('---\nname: My Skill\ndescription: ' + 'x' * 1100 + '\n---\n본문 mcp__foo')
    front, notes = fix_front(meta, 'my-skill')
    assert front['name'] == 'my-skill' and len(front['description']) == MAX_DESC, front
    assert NAME_RE.fullmatch('sermon-to-blog') and not NAME_RE.fullmatch('Sermon_Blog')
    assert CLAUDE_ONLY.search(body)
    print('demo ok')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('skills', nargs='*')
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--nested', action='store_true', help='zip 안에 <name>/SKILL.md 폴더 구조로 넣기(평면 업로드가 거부될 때)')
    ap.add_argument('--demo', action='store_true')
    a = ap.parse_args()
    if a.demo or not a.skills:
        demo(); sys.exit(0)
    os.makedirs(a.out, exist_ok=True)
    for s in a.skills:
        src = s if os.path.isdir(s) else os.path.join(SKILLS, s)
        if not os.path.isfile(os.path.join(src, 'SKILL.md')):
            print(f'✗ {s}: SKILL.md 없음'); continue
        z, notes = export(src, a.out, a.nested)
        print(('✓ ' + z) if z else f'✗ {s}')
        for n in notes:
            print('   - ' + n)
