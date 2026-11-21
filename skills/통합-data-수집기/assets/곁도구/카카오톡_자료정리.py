#!/usr/bin/env python3
"""카카오톡 '대화 내보내기' 파일(txt/csv)을 읽어 자료 목록을 최신순으로 정리한다.

사용: python3 카카오톡_자료정리.py [폴더 ...]   (기본: DEFAULT_DIRS, 하위 폴더 포함)
출력: 이 스크립트 옆에 카카오톡_자료목록.csv(엑셀용), 카카오톡_자료목록.md

'자료'로 뽑는 메시지: 링크가 있거나, 파일·동영상 첨부이거나, 80자 이상 글. (사진·이모티콘만 있는 메시지는 제외)
모든 처리는 로컬에서만 한다(외부 전송 없음).
"""
import csv, os, re, sys, unicodedata
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
YEARS = 10
_DRIVE = '~/Library/CloudStorage/GoogleDrive-sk010-****-****@gmail.com/다른 컴퓨터/내 노트북/Downloads/'
DEFAULT_DIRS = ['~/Downloads', '~/Desktop/cysjavis/AI도구/카톡브리핑/내보내기',
                _DRIVE + 'KakaoTalk_20260827_1344_46_932_group.txt',
                _DRIVE + 'cysjavis_KakaoTalk_20260829_1743_18_721_group.txt']
MIN_LEN = 80
URL = re.compile(r'https?://[^\s<>"\]\)]+')
ATTACH = re.compile(r'^(동영상|파일)(\s*:|$)|^파일: |\.(pdf|hwpx?|docx?|xlsx?|pptx?|zip|jpg|png|mp4)$', re.I)

# 날짜 구분선: "--------------- 2025년 11월 12일 수요일 ---------------" 또는 "2025년 11월 12일 수요일"
DAY = re.compile(r'^-*\s*(\d{4})년 (\d{1,2})월 (\d{1,2})일 \S+요일\s*-*$')
# PC 형식: "[이름] [오후 1:44] 내용"
PC = re.compile(r'^\[(.+?)\] \[(오전|오후) (\d{1,2}):(\d{2})\] ?(.*)$')
# 모바일/맥 형식: "2025년 11월 12일 오후 1:44, 이름 : 내용" / "2025. 11. 12. 오후 1:44, 이름 : 내용"
MOB = re.compile(r'^(\d{4})(?:년 |\. )(\d{1,2})(?:월 |\. )(\d{1,2})(?:일|\.) (오전|오후) (\d{1,2}):(\d{2}),? (.+?) : (.*)$')


def hm(ampm, h, m):
    h = int(h) % 12 + (12 if ampm == '오후' else 0)
    return h, int(m)


def parse_txt(path):
    msgs, day, cur = [], None, None
    with open(path, encoding='utf-8-sig', errors='ignore') as f:
        lines = f.read().splitlines()
    room = re.sub(r'\s*님과 카카오톡 대화$', '', lines[0].strip()) if lines else ''
    for line in lines[1:]:
        if m := DAY.match(line.strip()):
            day = tuple(map(int, m.groups())); cur = None; continue
        if (m := PC.match(line)) and day:
            h, mi = hm(*m.group(2, 3, 4))
            cur = [datetime(*day, h, mi), m.group(1), m.group(5)]; msgs.append(cur); continue
        if m := MOB.match(line):
            y, mo, d, ap, h, mi, who, txt = m.groups()
            h, mi = hm(ap, h, mi)
            cur = [datetime(int(y), int(mo), int(d), h, mi), who, txt]; msgs.append(cur); continue
        if cur is not None and not line.startswith('저장한 날짜'):
            cur[2] += '\n' + line  # 여러 줄 메시지 이어붙이기
    return room, msgs


def parse_csv(path):
    msgs = []
    with open(path, encoding='utf-8-sig', errors='ignore', newline='') as f:
        for r in csv.DictReader(f):
            try:
                msgs.append([datetime.fromisoformat(r['Date'][:19]), r.get('User', ''), r.get('Message', '')])
            except (KeyError, ValueError):
                continue
    name = unicodedata.normalize('NFC', os.path.splitext(os.path.basename(path))[0])
    return re.sub(r'^KakaoTalk_Chat_|_\d{4}-\d{2}-\d{2}(-\d{2}-\d{2}-\d{2})?$', '', name), msgs


def is_export(path):
    name = unicodedata.normalize('NFC', os.path.basename(path))
    if 'Longtxt' in name or not name.lower().endswith(('.txt', '.csv')):
        return False
    if not re.search(r'kakao|talk|카카오', name, re.I):
        return False
    with open(path, encoding='utf-8-sig', errors='ignore') as f:
        head = f.read(4000)
    return '카카오톡 대화' in head or head.startswith('Date,User,Message') or bool(MOB.search(head))


def row(room, when, who, text):
    text = text.strip()
    links = list(dict.fromkeys(u.rstrip('.,') for u in URL.findall(text)))
    body = URL.sub('', text).strip()
    attach = bool(ATTACH.search(body))
    if not (links or attach or len(body) >= MIN_LEN):
        return None
    first = next((l.strip() for l in body.splitlines() if l.strip()), '')
    if not first and links:
        first = re.sub(r'^https?://(www\.)?', '', links[0]).split('/')[0]
    one = re.sub(r'\s+', ' ', body)
    return {
        '일시': when.strftime('%Y-%m-%d %H:%M'),
        '제목': first[:40],
        '주요내용': (one[:150] + '…') if len(one) > 150 else one,
        '링크': ' '.join(links),
        '채팅방': room,
        '보낸사람': who,
    }


def main(dirs):
    since = datetime.now() - timedelta(days=365 * YEARS)
    paths = [os.path.expanduser(d) for d in dirs]
    files = sorted({p for p in paths if os.path.isfile(p)} |
                   {os.path.join(r, f) for p in paths for r, _, fs in os.walk(p) for f in fs})
    files = [f for f in files if is_export(f)]
    if not files:  # 빈 결과로 기존 목록을 덮어쓰지 않는다
        print(f'내보내기 파일을 찾지 못했습니다. 기존 목록은 그대로 둡니다. 찾은 폴더: {dirs}')
        return
    rows, seen, spans = [], set(), {}
    for f in files:
        room, msgs = (parse_csv if f.lower().endswith('.csv') else parse_txt)(f)
        if msgs:
            ts = [m[0] for m in msgs]
            lo, hi = spans.get(room, (min(ts), max(ts)))
            spans[room] = (min(lo, *ts), max(hi, *ts))
        for when, who, text in msgs:
            if when < since or (r := row(room, when, who, text)) is None:
                continue
            key = (r['일시'], r['보낸사람'], r['주요내용'])  # 같은 방을 여러 번 내보낸 경우 중복 제거
            if key not in seen:
                seen.add(key); rows.append(r)
        print(f'읽음: {room} — 메시지 {len(msgs)}개')
    rows.sort(key=lambda r: r['일시'], reverse=True)
    # 입장 안내처럼 같은 방에 반복되는 같은 글은 최신 1건만 남긴다(첨부만 있는 메시지는 건드리지 않음)
    once, kept = set(), []
    for r in rows:
        # 안내문은 이름만 바뀌어 반복되므로, 링크 없는 글은 첫 줄(10자 이상)이 같으면 같은 글로 본다
        same = r['제목'] if not r['링크'] and len(r['제목']) >= 10 else r['주요내용']
        key = (r['채팅방'], same, r['링크'])
        if ATTACH.search(r['제목']) or key not in once:
            once.add(key); kept.append(r)
    rows = kept

    cols = ['일시', '제목', '주요내용', '링크', '채팅방', '보낸사람']
    with open(os.path.join(HERE, '카카오톡_자료목록.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(rows)
    esc = lambda s: s.replace('|', '\\|').replace('\n', ' ')
    with open(os.path.join(HERE, '카카오톡_자료목록.md'), 'w', encoding='utf-8') as f:
        f.write(f'# 카카오톡 자료 목록 (최신순, {len(rows)}건)\n\n')
        f.write(f'생성: {datetime.now():%Y-%m-%d %H:%M} · 원본 파일 {len(files)}개 · 최근 {YEARS}년\n\n')
        f.write('| 일시 | 제목 | 주요내용 | 링크 | 채팅방 |\n|---|---|---|---|---|\n')
        for r in rows:
            links = ' '.join(f'[링크]({u})' for u in r['링크'].split())
            f.write(f"| {r['일시']} | {esc(r['제목'])} | {esc(r['주요내용'])} | {links} | {esc(r['채팅방'])} |\n")
    print(f'\n원본 {len(files)}개 → 자료 {len(rows)}건 저장: {HERE}')
    print('\n방별 기간:')
    for room, (lo, hi) in sorted(spans.items(), key=lambda x: x[1][0]):
        print(f'  {lo:%Y-%m-%d} ~ {hi:%Y-%m-%d}  {room}')


def _selfcheck():
    assert PC.match('[이건희] [오전 9:22] 반갑습니다~')
    assert hm('오후', '12', '05') == (12, 5) and hm('오전', '12', '05') == (0, 5)
    m = MOB.match('2025. 11. 12. 오후 1:44, 홍길동 : https://a.com 보세요')
    assert m and m.group(7) == '홍길동'
    assert row('방', datetime(2025, 1, 1), '나', '보세요 https://a.com/x.') ['링크'] == 'https://a.com/x'
    assert row('방', datetime(2025, 1, 1), '나', '네 감사합니다') is None


if __name__ == '__main__':
    _selfcheck()
    main(sys.argv[1:] or DEFAULT_DIRS)
