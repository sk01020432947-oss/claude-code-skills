# folder-tidy-recipes R1: 읽기 전용 분류표. 아무것도 옮기거나 지우지 않는다.
import os, re, sys, time, hashlib, unicodedata
from collections import defaultdict

SRC = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/Downloads")
OUT = os.path.expanduser(sys.argv[2])
NOW = time.time()
N = lambda s: unicodedata.normalize("NFC", s)

TOPICS = [  # (키워드 정규식, 주제폴더)
    (r"설교|성경|주석|본문|묵상|qt|bible|sermon|commentary", "설교연구"),
    (r"강의|교안|강의안|syllabus|수업|중간고사|기말|과제|사회복지(학|론|정책론)", "강의_발표"),
    (r"논문|thesis|dissertation|학위|학술|journal|kci|riss|\.bib$|\.ris$", "논문"),
    (r"총회|노회|헌법|당회|제직", "교회_총회자료"),
    (r"교회학교|주일학교|유초등|중고등부|청년부", "교회학교"),
    (r"조례|의회|회의록|입법예고", "지방의회조례"),
    (r"통합돌봄|돌봄", "통합돌봄"),
    (r"복지|정책|보건복지", "복지정책"),
    (r"통계|kosis|지표", "정책통계_조사"),
    (r"소송|판결|법원|고소|내용증명|변호", "법률_대응"),
    (r"출판|원고|isbn|교정지", "책_출판"),
    (r"모션|motion|remotion|\.aep$", "모션그래픽"),
    (r"팔레트|palette|design|디자인|\.fig$", "디자인_팔레트"),
    (r"독서|서평|epub$", "독서"),
    (r"장학|성안나", "기타"),
    (r"claude|클로드|gpt|gemini|mcp|에이전트|agent|hermes|llm|생성형|\bai\b|_ai|ai_|프롬프트|prompt|notebooklm|코덱스|codex", "AI동향_검토"),
    (r"청소년|아동|노인|장애인|가족복지|사례관리", "강의_발표"),
]
INSTALLER = (".dmg", ".pkg", ".msi", ".exe", ".appimage")
ARCHIVE = (".zip", ".7z", ".rar", ".tar", ".tar.gz", ".tgz")
SHOT = re.compile(r"스크린샷|screen ?shot|화면 ?기록|screen recording|capture|캡처", re.I)
DUPMARK = re.compile(r"^(.*?)(?: ?\((\d+)\)| copy| 복사본)(\.[^.]+)?$", re.I)
PHONE = re.compile(r"01[016-9][-. ]?\d{3,4}[-. ]?\d{4}")
RRN = re.compile(r"\d{6}[- ]?[1-4]\d{6}")

def mask(name):
    return RRN.sub("******-*******", PHONE.sub("010-****-****", name))

def size_of(p):
    if os.path.isfile(p) or os.path.islink(p):
        return os.lstat(p).st_size
    t = 0
    for r, _, fs in os.walk(p):
        for f in fs:
            try: t += os.lstat(os.path.join(r, f)).st_size
            except OSError: pass
    return t

def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024: return f"{n:.0f}{u}" if u == "B" else f"{n:.1f}{u}"
        n /= 1024
    return f"{n:.1f}TB"

def sha(p, _c={}):
    if p not in _c:
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
        _c[p] = h.hexdigest()
    return _c[p]

def stem_archive(n):
    l = n.lower()
    for e in sorted(ARCHIVE, key=len, reverse=True):
        if l.endswith(e): return n[: -len(e)]
    return None

entries = sorted(e for e in os.listdir(SRC) if not e.startswith("."))
names_nfc = {N(e): e for e in entries}
rows = []
by_size = defaultdict(list)
for e in entries:
    p = os.path.join(SRC, e)
    if os.path.isfile(p): by_size[os.path.getsize(p)].append(p)

for e in entries:
    p = os.path.join(SRC, e); n = N(e); low = n.lower()
    st = os.lstat(p); isdir = os.path.isdir(p)
    sz = size_of(p); age = (NOW - st.st_mtime) / 86400
    cls, why, dest = None, "", ""
    ext = os.path.splitext(low)[1]

    if not isdir and low.endswith(INSTALLER):
        cls, why = "삭제후보", "설치 파일"
    elif not isdir and (s := stem_archive(n)) is not None and (N(s) in names_nfc or N(s.rstrip()) in names_nfc):
        cls, why = "삭제후보", "압축 푼 폴더가 옆에 있음"
    elif not isdir and SHOT.search(n) and age > 30:
        cls, why = "삭제후보", f"{int(age)}일 지난 스크린샷"
    elif not isdir and (m := DUPMARK.match(n)):
        base = (m.group(1) + (m.group(3) or "")).strip()
        bp = names_nfc.get(N(base))
        if bp and os.path.isfile(os.path.join(SRC, bp)):
            same = os.path.getsize(os.path.join(SRC, bp)) == st.st_size and sha(os.path.join(SRC, bp)) == sha(p)
            cls, why = ("삭제후보", f"'{mask(N(bp))}'와 내용 동일") if same else ("확인필요", f"'{mask(N(bp))}'와 이름만 같고 내용 다름")
    if cls is None and not isdir and len(by_size[st.st_size]) > 1 and st.st_size > 0:
        twins = [q for q in by_size[st.st_size] if q != p and sha(q) == sha(p)]
        if twins:
            older = min(twins + [p], key=lambda q: (os.path.getmtime(q), q))
            if older != p:
                cls, why = "삭제후보", f"'{mask(N(os.path.basename(older)))}'와 내용 동일(사본)"
    if cls is None:
        for rx, folder in TOPICS:
            if re.search(rx, low):
                cls, why, dest = "보관추천", "이름에 주제어", f"cysjavis/{folder}/"
                break
    if cls is None:
        cls, why = "확인필요", "주제를 이름으로 판단 불가" + (" (폴더)" if isdir else "")
    rows.append((cls, mask(n) + ("/" if isdir else ""), sz, time.strftime("%Y-%m-%d", time.localtime(st.st_mtime)), why, dest or "—"))

order = {"삭제후보": 0, "보관추천": 1, "확인필요": 2}
rows.sort(key=lambda r: (order[r[0]], -r[2]))
cnt = defaultdict(int); tot = defaultdict(int)
for r in rows: cnt[r[0]] += 1; tot[r[0]] += r[2]

esc = lambda s: s.replace("|", "\\|")
with open(OUT, "w") as f:
    f.write(f"---\ntype: ledger\nrecipe: folder-tidy-recipes R1\ntarget: {SRC}\ncreated: {time.strftime('%Y-%m-%d %H:%M')}\nstatus: 승인 대기 (아무것도 옮기거나 지우지 않음)\n---\n\n")
    f.write(f"# 다운로드 폴더 정리 후보 — {time.strftime('%Y-%m-%d')}\n\n")
    f.write(f"대상 `{SRC}` 최상위 {len(rows)}개. 읽기만 했고 파일은 그대로다. 전화번호·주민번호 형태는 파일명에서 가렸다.\n\n")
    f.write("| 분류 | 개수 | 용량 |\n|---|---:|---:|\n")
    for k in order: f.write(f"| {k} | {cnt[k]} | {human(tot[k])} |\n")
    f.write(f"| 합계 | {len(rows)} | {human(sum(tot.values()))} |\n\n")
    f.write("기준 — 삭제후보: 설치파일(.dmg/.pkg), 압축 푼 폴더가 옆에 있는 zip, 30일 지난 스크린샷, 내용이 같은 사본(해시 비교). 보관추천: 이름에 주제어가 있어 cysjavis 주제폴더 제안. 나머지는 확인필요.\n\n")
    for k in order:
        f.write(f"## {k} ({cnt[k]})\n\n| # | 파일명 | 크기 | 수정일 | 이유 | 옮길 곳 제안 |\n|---:|---|---:|---|---|---|\n")
        i = 0
        for r in rows:
            if r[0] != k: continue
            i += 1
            f.write(f"| {i} | {esc(r[1])} | {human(r[2])} | {r[3]} | {esc(r[4])} | {r[5]} |\n")
        f.write("\n")
print({k: (cnt[k], human(tot[k])) for k in order}, len(rows))
