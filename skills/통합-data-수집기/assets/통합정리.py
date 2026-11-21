#!/usr/bin/env python3
"""여러 곳에서 모은 글을 한 파일(통합자료.jsonl)과 한 화면(KBG-통합자료수집기.html)으로 합친다.

    python3 통합정리.py                              # 북마클릿으로 받은 파일(다운로드 폴더)만 정리
    python3 통합정리.py --youtube 채널주소 --limit 30   # 유튜브 제목·설명 (--subs 를 붙이면 자막까지)
    python3 통합정리.py --blog 블로그주소               # 블로그 새 글 (--full 은 네이버 글 전문)
    python3 통합정리.py --kakao                       # 다운로드 폴더의 카톡 '대화 내보내기' 파일
    python3 통합정리.py --import 파일.json --platform facebook --author 이름   # 이미 모아 둔 자료
    python3 통합정리.py --inbox                       # 옵시디언 inbox 노트 (유튜브 자막·스크랩·글)
    python3 통합정리.py --bookmarks                   # 브라우저 북마크 (폴더 이름까지)
    python3 통합정리.py --artifacts                   # 발행한 Claude 아티팩트 (발행 장부 + 아티팩트_목록.csv)
    python3 통합정리.py --all                         # 북마클릿 + 카톡 + inbox + 북마크 + 아티팩트를 한 번에
    python3 통합정리.py --selfcheck                   # 스스로 점검
    (옵션은 한 번에 여러 개 써도 된다. --open 을 붙이면 끝나고 화면을 연다.)

돌릴 때마다 통합자료.jsonl 에 '더한다'. 같은 글(platform+id)은 한 번만 남기고 더 긴 쪽을 둔다.
공개 글·내 대화를 내 컴퓨터에 보관하는 용도다. 로그인 대행·차단 우회는 하지 않는다.
"""
import argparse, csv, fcntl, hashlib, html, importlib.util, json, os, plistlib, re, sqlite3, subprocess, sys, time, unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime
from itertools import islice
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
OUT = HERE / "통합자료.jsonl"
VIEW = HERE / "KBG-통합자료수집기.html"
NOTES = HERE / "메모태그.json"          # 보기 화면에서 단 메모·태그·별표 (글 자료와 따로 둔다)
TRASH = HERE / "보관" / "지운자료.jsonl"   # 보기 화면에서 지운 글이 옮겨지는 곳 (버리지 않고 여기 쌓는다)
STATE = HERE / "자동수집_상태.json"       # 자동 수집이 마지막으로 본 파일들의 크기·시각
AGENT = Path.home() / "Library/LaunchAgents/com.kbg.tonghap-auto.plist"   # 자동 수집을 돌리는 macOS 등록 파일
DL = Path.home() / "Downloads"
BUILD_JS = HERE / "tonghap_build.js"      # 보기 화면이 "새 판이 나왔나" 를 물어보는 한 줄짜리 파일 (판 번호와 시각만 든다)
LINKS = HERE / "연결출처.json"            # --blog · --youtube 로 한 번 가져온 주소. 다음부터 저절로 다시 본다
# 발행한 Claude 아티팩트 목록 (날짜,제목,정본 파일,주소). 앞 = 손으로 적는 장부, 뒤 = 발행할 때마다 훅(~/.claude/hooks/artifact-ledger.py)이 한 줄 더하는 파일
ARTIFACTS = [Path.home() / "Desktop/cysjavis/ledger/artifact_urls.csv", HERE / "아티팩트_목록.csv"]
KAKAO_PY = HERE.parent / "카카오톡_자료정리" / "카카오톡_자료정리.py"
NAVER_PY = Path.home() / ".claude/skills/naver-blog-research/scripts/naver_read.py"
UA = {"User-Agent": "Mozilla/5.0 (personal-archive)"}
INBOX_DIRS = ["~/obsidian/Obsidian 2025/00. Inbox", "~/obsidian/Obsidian 2025/PKM/00 inbox",
              "~/DEV/my-llm-wiki/00. Inbox"]
# 주소를 보고 어느 묶음에 넣을지 정한다 (위에서부터 먼저 맞는 것)
HOSTS = [("youtube", r"youtube\.com|youtu\.be"), ("blog", r"blog\.naver\.com|tistory\.com|brunch\.co\.kr|velog\.io"),
         ("facebook", r"facebook\.com|fb\.watch"), ("threads_saved", r"threads\.(com|net)"),
         ("instagram", r"instagram\.com"), ("x", r"//(www\.)?(x|twitter)\.com")]
LABEL = {"kakao": "카톡", "facebook": "페이스북", "facebook_shared": "페이스북 공유글", "youtube": "유튜브", "blog": "블로그", "bookmark": "북마크",
         "inbox": "인박스", "threads": "쓰레드", "threads_saved": "쓰레드 저장글", "instagram": "인스타", "x": "X", "manual": "직접 추가", "claude_artifact": "Claude 아티팩트",
         "phone_sms": "문자", "phone_call": "통화기록", "phone_note": "폰 메모", "phone_voice": "음성녹음", "phone_callrec": "통화 녹음", "phone_photo": "사진",
         "phone": "스마트폰", "thr": "쓰레드", "disk": "연결"}   # phone · thr = 보기 화면에서 phone_* · threads* 를 한데 모은 묶음 이름
BM_SHELVES = ("추천자료_inbox", "in box_임시저장")   # 북마크 가운데 따로 떼어 보여 줄 폴더 (하위 폴더까지 그 이름으로 센다)
# '옵시디언 위키로 보내기' 가 새 노트를 두는 곳. 볼트 규칙(Obsidian 2025/CLAUDE.md)에서 에이전트가 써도 되는 대기실이다.
VAULT_INBOX = Path.home() / "obsidian/Obsidian 2025/PKM/00 inbox/통합자료"
VAULT_AUTHOR = "김병곤"                     # 볼트 규칙(PKM/CLAUDE.md 5번)이 정한 author 값
# 주제: 볼트의 domain 목록(PKM/02 나의 핵심 맥락 §6)을 그대로 쓴다. 위에서부터 먼저 맞는 것, 아무것도 안 맞으면 '기타'.
# ponytail: 낱말 맞추기 경험칙이라 틀린 분류가 섞인다. 틀린 글은 태그로 바로잡고,
#           정밀하게 나누려면 볼트의 ingest(LLM)에 맡길 것.
TOPICS = [(n, re.compile(p, re.I)) for n, p in [
    ("설교", r"설교|강해|sermon|preach|예화|말씀카드"),
    ("성경", r"성경|성서|구약|신약|복음서|창세기|시편|로마서|주석|헬라어|히브리어|큐티|묵상|bible"),
    ("신학", r"신학|교리|칼빈|칼뱅|루터|바빙크|개혁주의|교회사|삼위일체|기독론|구원론|종말론|theolog"),
    ("목회", r"목회|교회|목사|예배|찬양|심방|제자훈련|주일학교|소그룹|전도|선교|성도|church"),
    ("논문", r"논문|학위|dissertation|thesis|선행연구|학술|paper"),
    ("연구방법", r"연구방법|질적 ?연구|양적 ?연구|통계|설문|근거이론"),
    ("PKM/옵시디언", r"옵시디언|obsidian|제텔카스텐|PKM|세컨드 ?브레인|second brain|노션|notion|LLM ?위키|지식 ?관리"),
    ("AI/도구", r"(?<![a-z])AI(?![a-z])|인공지능|GPT|클로드|claude|gemini|제미나이|프롬프트|에이전트|agent|LLM"
                r"|코딩|자동화|MCP|확장프로그램|PPT|영상 ?제작|모션|앱|github"),
    ("교육", r"교육|강의|수업|학교|대학|학습|교사|커리큘럼"),
    ("사회복지", r"사회복지|복지|돌봄|상담|장애인|노인|아동"),
    ("경영/행정", r"경영|행정|회계|세무|과세|재정|마케팅|창업|사업|리더십|조직"),
    ("개인", r"쇼핑|가구|의자|여행|건강|운동|요리|일기|가족|유니폼")]]


def load(path):
    """다른 폴더의 파이썬 파일을 그대로 불러 쓴다 (같은 기능을 다시 짜지 않으려고)."""
    spec = importlib.util.spec_from_file_location(Path(path).stem, path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(Path(path).parent))
    spec.loader.exec_module(mod)
    return mod


def norm_date(v):
    """갖가지 날짜 표기를 '2026-01-02T03:04:05' 꼴로. 못 읽으면 빈 문자열."""
    s = str(v or "").strip()
    if re.fullmatch(r"\d{8}", s):                                   # 유튜브 20260102
        return f"{s[:4]}-{s[4:6]}-{s[6:]}"
    if re.fullmatch(r"\d{10}(\d{3})?(\.\d+)?", s):                  # 초/밀리초 숫자
        n = float(s)
        return datetime.fromtimestamp(n / 1000 if n > 1e11 else n).isoformat(timespec="seconds")
    if re.match(r"\d{4}-\d{2}-\d{2}", s):
        # ponytail: 표준시(Z)와 한국시간이 섞여 저장된다. 날짜 단위 정렬에는 충분 —
        #           시각까지 맞춰야 하면 여기서 한 시간대로 바꿀 것.
        return s[:19]
    if m := re.search(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일", s):
        return "%s-%02d-%02d" % (m[1], int(m[2]), int(m[3]))
    try:
        return parsedate_to_datetime(s).isoformat(timespec="seconds")[:19]   # 블로그 RSS
    except (TypeError, ValueError):
        return ""


def code_date(code):
    """쓰레드·인스타 글 주소의 코드(DaroS9WiSGS)에는 올린 시각이 들어 있다. 화면에서 날짜를 못 읽었을 때 쓴다."""
    A = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    if not code or any(c not in A for c in code):
        return ""
    n = 0
    for c in code:
        n = n * 64 + A.index(c)
    ms = (n >> 23) + 1314220021721
    # ponytail: 공개된 적 없는 규칙(경험칙)이다. 말이 안 되는 해가 나오면 빈칸으로 둔다.
    return str((ms / 1000)) if 1.4e12 < ms < 2.2e12 else ""


def rec(platform, id, text, author="", url="", date="", title=""):
    text = str(text or "").strip()
    if not norm_date(date) and platform.startswith(("threads", "instagram")):
        date = code_date(str(id or ""))
    id = str(id or "") or hashlib.sha1(f"{author}|{date}|{text[:80]}".encode()).hexdigest()[:16]
    return {"platform": platform, "id": id, "author": str(author or ""), "url": str(url or ""),
            "date": norm_date(date), "title": str(title or "").strip(), "text": text}


# ---------- 1. 북마클릿(통합수집기·쓰레드 수집기)으로 받은 파일 ----------

def from_collector():
    pm = load(HERE / "parse_manual.py")
    pm.DOWNLOAD_PATTERN = "sns_*posts*.json"      # '다운로드 폴더 → raw' 이동을 그대로 빌려 쓴다
    pm.pull_from_downloads(RAW)
    out = []
    for f in sorted(RAW.glob("*.json")):
        name = unicodedata.normalize("NFC", f.name)
        data = json.loads(f.read_text(encoding="utf-8"))
        if not isinstance(data, list) or not data:
            continue
        if name.endswith("_parsed.json"):         # 쓰레드 원래 절차(parse_manual.py)가 이미 정리한 것
            out += [rec("threads", p["id"], p["text"], p.get("username"), p.get("url"),
                        p.get("created_at")) for p in data]
        elif name.startswith("sns_"):             # 통합수집기 원본
            threads = [p for p in data if p.get("platform") == "threads"]
            if threads:                           # 쓰레드는 머리말·숫자 찌꺼기를 parse_manual 로 걷어낸다
                who = Counter(p["username"] for p in threads).most_common(1)[0][0]
                parsed = [pm.parse_one(p, who) for p in threads if p["username"] == who]
                out += [rec("threads", p["id"], p["text"], p["username"], p["url"], p["created_at"])
                        for p in pm.merge_chains([p for p in parsed if not p["is_comment"]])]
            # 쓰레드 '저장됨' 화면: 글쓴이가 제각각이라 글마다 그 글쓴이 기준으로 찌꺼기를 걷어낸다
            out += [rec("threads_saved", q["id"], q["text"], q["username"], q["url"], q["created_at"])
                    for q in (pm.parse_one(p, p["username"]) for p in data if p.get("platform") == "threads_saved")]
            out += [rec(p.get("platform", "etc"), p["id"], p.get("raw_text"), p.get("username"),
                        p.get("url"), p.get("created_at"))
                    for p in data if p.get("platform") not in ("threads", "threads_saved")]
    return out


# ---------- 2. 유튜브 (yt-dlp) ----------

def vtt_text(s):
    """자막 파일에서 시간표·태그를 걷어내고, 자동자막의 겹치는 줄을 한 번만 남긴다."""
    out = []
    for line in s.splitlines():
        line = html.unescape(re.sub(r"<[^>]+>", "", line)).strip()
        if not line or "-->" in line or line.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        if not out or out[-1] != line:
            out.append(line)
    return " ".join(out)


def from_youtube(url, limit, subs):
    if re.search(r"youtube\.com/(@[^/]+|channel/[^/]+|c/[^/]+)/?$", url):
        url = url.rstrip("/") + "/videos"         # 채널 첫 화면이면 '동영상' 탭으로
    subdir = RAW / "youtube"
    cmd = ["yt-dlp", "--dump-json", "--no-simulate", "--skip-download", "--ignore-errors",
           "--no-warnings", "--playlist-end", str(limit), "-o", str(subdir / "%(id)s.%(ext)s")]
    if subs:
        cmd += ["--write-subs", "--write-auto-subs", "--sub-langs", "ko,en", "--sub-format", "vtt"]
    print(f"▶ 유튜브 가져오는 중 (최대 {limit}개, 영상마다 몇 초): {url}")
    r = subprocess.run(cmd + [url], capture_output=True, text=True)
    out = []
    for line in r.stdout.splitlines():
        try:
            v = json.loads(line)
        except ValueError:
            continue
        text = v.get("description") or ""
        sub = next((p for lang in ("ko", "en") if (p := subdir / f"{v['id']}.{lang}.vtt").exists()), None)
        if sub:
            text += "\n\n[자막]\n" + vtt_text(sub.read_text(encoding="utf-8", errors="ignore"))
        out.append(rec("youtube", v["id"], text, v.get("channel") or v.get("uploader"),
                       v.get("webpage_url"), v.get("upload_date"), v.get("title")))
    if not out:
        print("  ⚠ 받은 영상 없음:", r.stderr.strip()[-300:])
    return out


# ---------- 3. 블로그 (RSS·Atom) ----------

def fetch(url):
    return urlopen(Request(url, headers=UA), timeout=20).read()


def strip_html(s):
    s = re.sub(r"(?i)<(br|/p|/div|/li|/h\d)[^>]*>", "\n", s or "")
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    return re.sub(r"\n\s*\n+", "\n\n", s).strip()


def parse_feed(body):
    tag = lambda e: e.tag.rsplit("}", 1)[-1]
    root = ET.fromstring(body)
    site = next(("".join(c.itertext()).strip() for c in root.iter() if tag(c) == "title"), "")
    out = []
    for it in root.iter():
        if tag(it) not in ("item", "entry"):
            continue
        d = {}
        for c in it:
            if tag(c) == "link" and c.get("rel") not in (None, "alternate"):
                continue
            d.setdefault(tag(c), "".join(c.itertext()).strip() or c.get("href", ""))
        d["link"] = d.get("link", "").split("?fromRss")[0]          # 네이버가 붙이는 추적 꼬리 제거
        body_html = d.get("encoded") or d.get("content") or d.get("description") or d.get("summary")
        out.append(rec("blog", d.get("link") or d.get("guid") or d.get("id"), strip_html(body_html),
                       d.get("creator") or d.get("author") or site, d.get("link"),
                       d.get("pubDate") or d.get("published") or d.get("updated") or d.get("date"),
                       strip_html(d.get("title"))))
    return out


def from_blog(url, full):
    m = re.match(r"https?://(?:m\.)?blog\.naver\.com/([\w-]+)/?$", url)
    tries = [f"https://rss.blog.naver.com/{m[1]}.xml"] if m else [url, url.rstrip("/") + "/rss",
                                                                   url.rstrip("/") + "/feed"]
    body = None
    for t in tries:
        try:
            got = fetch(t)
        except OSError:
            continue
        if re.search(rb"<(rss|feed|rdf:RDF)[\s>]", got[:3000]):
            body = got
            break
        if link := re.search(rb'<link[^>]+application/(?:rss|atom)\+xml[^>]*href="([^"]+)"', got):
            body = fetch(urljoin(t, link[1].decode()))
            break
    if body is None:
        print(f"  ⚠ 블로그 새 글 목록(RSS)을 못 찾음: {url}")
        return []
    out = parse_feed(body)
    # ponytail: RSS 는 보통 최근 글 10~50개만 준다. 옛 글까지 필요하면 글 목록 화면에서
    #           통합수집기(북마클릿)를 쓰거나 주소 목록을 --import 로 넣을 것.
    if full and NAVER_PY.exists():                # 네이버는 RSS 가 요약뿐이라 글마다 전문을 읽는다
        nv = load(NAVER_PY)
        for r in out:
            if "blog.naver.com" in r["url"]:
                try:
                    r["text"] = nv.read_blog(r["url"], include_images=False)["content"] or r["text"]
                except Exception as e:            # 한 글 실패로 전체를 버리지 않는다
                    print(f"  ⚠ 전문 못 읽음: {r['url']} — {e}")
                time.sleep(1)
    print(f"▶ 블로그 {len(out)}건: {url}")
    return out


# ---------- 4. 카카오톡 ('대화 내보내기' 파일) ----------

def kakao_files(k, paths=()):
    files = []
    # 기본 위치는 기존 스크립트가 쓰던 곳 그대로. 단, 클라우드 드라이브는 파일을 내려받느라
    # 멈춰 설 수 있어 기본에서 뺀다 (필요하면 --kakao 뒤에 경로를 직접 적는다).
    for p in paths or [d for d in k.DEFAULT_DIRS if "CloudStorage" not in d]:
        p = Path(p).expanduser()
        files += [f for f in (sorted(p.iterdir()) if p.is_dir() else [p] if p.exists() else [])
                  if f.is_file() and k.is_export(str(f))]
    return files


def from_kakao(paths):
    k = load(KAKAO_PY)
    files = kakao_files(k, paths)
    out = []
    for f in files:
        room, msgs = (k.parse_csv if f.suffix.lower() == ".csv" else k.parse_txt)(str(f))
        # 링크·첨부·긴 글만 '자료'로 친다 — 기존 카카오톡_자료정리.py 의 기준(row)을 그대로 쓴다
        keep = [rec("kakao", None, text, who, "", when.isoformat(), room)
                for when, who, text in msgs if k.row(room, when, who, text)]
        print(f"▶ 카톡 {unicodedata.normalize('NFC', f.name)}: 대화 {len(msgs)}줄 중 자료 {len(keep)}건")
        out += keep
    if not files:
        print("  ⚠ 카톡 내보내기 파일을 못 찾음 (카톡 채팅방 메뉴 → 대화 내용 내보내기 → 다운로드 폴더)")
    return out


# ---------- 5. 이미 모아 둔 JSON·JSONL ----------

def from_import(path, platform, author):
    s = Path(path).expanduser().read_text(encoding="utf-8")
    rows = json.loads(s) if s.lstrip().startswith("[") else [json.loads(l) for l in s.split("\n") if l.strip()]
    pick = lambda r, *ks: next((r[k] for k in ks if r.get(k) not in (None, "", "None")), "")
    return [rec(platform or pick(r, "platform") or Path(path).stem, pick(r, "id", "url"),
                pick(r, "text", "msg", "raw_text", "content", "body"),
                pick(r, "author", "username", "who") or author, pick(r, "url"),
                pick(r, "date", "time", "created_at", "timestamp"), pick(r, "title"))
            for r in rows if isinstance(r, dict)]


# ---------- 5-1. Claude 아티팩트 (발행 목록) ----------

def from_artifacts(paths=None):
    """발행한 Claude 아티팩트. 목록의 한 줄(날짜,제목,정본 파일,주소)이 글 하나 — 정본 파일이 이 컴퓨터에 있으면 그 글자를 본문으로 읽는다."""
    out = []
    for p in paths or ARTIFACTS:
        if not Path(p).exists():
            continue
        for row in csv.reader(Path(p).read_text(encoding="utf-8").split("\n")):
            if len(row) < 4 or not row[-1].strip().startswith("https://claude.ai/"):
                continue
            date, title, src, url = row[0].strip(), ",".join(row[1:-2]).strip(), row[-2].strip(), row[-1].strip()   # 제목 속 쉼표는 다시 붙인다
            body = ""
            try:
                f = Path(src).expanduser()
                # ponytail: 3MB 넘는 화면(자료가 통째로 박힌 것)은 제목만 담는다. 본문까지 찾으려면 한도를 올린다
                if src and f.is_file() and f.stat().st_size < 3_000_000:
                    body = strip_html(re.sub(r"(?is)<(script|style)\b.*?</\1>", "", f.read_text(encoding="utf-8", errors="replace")))[:20000]
            except OSError:
                pass
            out.append(rec("claude_artifact", url, body or title, "Claude 아티팩트", url, date, title))
    print(f"▶ Claude 아티팩트: {len(out)}건 (같은 주소는 하나로 합쳐진다)")
    return out


# ---------- 6. 옵시디언 inbox 노트 ----------

def front(s):
    """노트 머리말(--- 와 --- 사이)에서 'key: 값' 한 줄짜리만 읽는다. (머리말, 본문)을 돌려준다."""
    m = re.match(r"---\n(.*?)\n---\n?", s, re.S)
    if not m:
        return {}, s
    meta = {}
    for line in m[1].split("\n"):
        # ponytail: 여러 줄 값·목록은 건너뛴다. 태그 목록까지 쓰려면 PyYAML 로 바꿀 것.
        k, sep, v = line.partition(":")
        if sep and k and k[0] not in " -#":
            meta[k.strip()] = v.strip().strip("\"'").replace("[[", "").replace("]]", "")
    return meta, s[m.end():]


def from_inbox(paths):
    out = []
    for base in (Path(p).expanduser() for p in paths or INBOX_DIRS):
        notes = [f for f in base.rglob("*.md") if not any(part.startswith(".") for part in f.parts)]
        kept = 0
        for f in notes:
            meta, body = front(f.read_text(encoding="utf-8", errors="replace"))
            if not body.strip() or meta.get("sns_key"):   # sns_key = 이 도구가 옵시디언으로 보낸 노트. 다시 읽어 들이면 같은 글이 둘이 된다
                continue
            url = next((meta[k] for k in ("source_url", "source", "url") if meta.get(k, "").startswith("http")), "")
            plat = next((p for p, pat in HOSTS if re.search(pat, url)), "inbox")
            name = unicodedata.normalize("NFC", f.stem)
            # 노트 하나가 글 하나다. 주소만으로 묶으면 'facebook.com/' 처럼 뭉뚱그린 주소를 가진 서로 다른
            # 노트가 하나로 합쳐진다. 같은 글을 날짜만 달리 여러 번 스크랩한 것은 하나로 본다.
            id = (url or "inbox") + "#" + re.sub(r"^\d{4}-\d{2}-\d{2}[-_ ]*", "", name)
            date = next((meta[k] for k in ("published", "date_clipped", "date created", "created")
                         if norm_date(meta.get(k))), "") or f.stat().st_mtime
            r = rec(plat, id, body, meta.get("channel") or meta.get("author"), url, date,
                    meta.get("title") or name)
            r["file"] = str(f)                    # 보기 화면의 '노트 열기' 가 이 경로로 옵시디언을 연다
            out.append(r)
            kept += 1
        print(f"▶ inbox {unicodedata.normalize('NFC', base.name)}: 노트 {len(notes)}개 중 내용 있는 {kept}개")
    return out


# ---------- 7. 브라우저 북마크 ----------

def bookmark_files():
    apps = Path.home() / "Library/Application Support"   # 크롬·웨일·엣지·아크 등은 형식이 같다. 폴더 깊이만 조금씩 다르다
    return sorted(g for depth in ("*/*", "*/*/*", "*/*/*/*") for g in apps.glob(depth + "/Bookmarks"))


def from_bookmarks():
    """크롬 계열 브라우저와 사파리의 북마크. 글쓴이 자리에 폴더 경로를 넣어 폴더 이름으로도 찾게 한다."""
    out = []

    def chromium(node, path):
        for c in node.get("children", []):
            if c.get("type") == "url":
                when = int(c.get("date_added") or 0) / 1e6 - 11644473600      # 1601년 기준 마이크로초 → 유닉스 초
                out.append(rec("bookmark", c["url"], c["url"], " / ".join(path), c["url"],
                               int(when) if when > 1e9 else "", c.get("name")))
            else:
                chromium(c, path + [c.get("name", "")])

    def safari(node, path):
        for c in node.get("Children", []):
            if c.get("URLString"):
                out.append(rec("bookmark", c["URLString"], c["URLString"], " / ".join(path), c["URLString"],
                               "", c.get("URIDictionary", {}).get("title")))
            else:
                safari(c, path + [c.get("Title", "")])

    for f in bookmark_files():
        n = len(out)
        try:
            for name, root in json.loads(f.read_text(encoding="utf-8"))["roots"].items():
                if isinstance(root, dict):
                    chromium(root, [root.get("name") or name])
        except (OSError, ValueError, KeyError):
            continue
        print(f"▶ 북마크 {f.parent.parent.name}: {len(out) - n}건")
    try:
        n = len(out)
        safari(plistlib.loads((Path.home() / "Library/Safari/Bookmarks.plist").read_bytes()), [])
        print(f"▶ 북마크 Safari: {len(out) - n}건")
    except OSError:                               # 사파리 북마크는 '전체 디스크 접근' 권한이 없으면 못 읽는다
        pass
    return out


# ---------- 8. 폰 자료 (문자 · 통화기록 · 메모 · 음성녹음 · 사진) ----------
# 길이 둘이다. ① 아이폰·아이패드: iCloud 로 이 맥에 동기화된 앱 자료를 읽기 전용으로 연다(고치지 않는다).
# ② 갤럭시 등: 폰에서 꺼낸 파일을 폰자료/ 폴더에 두면 읽는다. 무엇을 어디서 꺼내는지는 스마트폰_자료_목록.md.

APPLE = 978307200                       # 애플 시각(2001-01-01 부터 센 초) → 보통 시각
LIB = Path.home() / "Library"
PHONE_DIR = HERE / "폰자료"
AUDIO = {".m4a", ".mp3", ".wav", ".amr", ".3gp", ".aac", ".ogg", ".flac"}
IMAGE = {".jpg", ".jpeg", ".png", ".heic", ".gif", ".webp", ".mp4", ".mov"}


def adate(x):
    """애플 시각 → '2026-01-02T03:04:05'. 문자 앱은 나노초로 적는다."""
    return datetime.fromtimestamp((x / 1e9 if x > 1e11 else x) + APPLE).isoformat(timespec="seconds") if x else ""


def mmss(sec):
    n = int(float(sec or 0))
    return f"{n // 60}분 {n % 60}초"


def attr_text(b):
    """문자 앱은 본문을 text 칸 대신 attributedBody(묶음 자료)에만 두기도 한다. 거기서 글자만 꺼낸다."""
    # ponytail: 묶음 형식을 정식으로 풀지 않고 'NSString' 바로 뒤의 길이+글자만 읽는다. 못 읽으면 빈칸.
    try:
        b = bytes(b).split(b"NSString")[1][5:]
        n, b = (int.from_bytes(b[1:3], "little"), b[3:]) if b[0] == 0x81 else (b[0], b[1:])
        return b[:n].decode("utf-8", "replace")
    except (IndexError, TypeError):
        return ""


def _call(id, date, dur, addr, name, out, answered):
    who = name or (addr.decode("utf-8", "replace") if isinstance(addr, bytes) else addr) or "알 수 없음"
    return rec("phone_call", id, f"{who} · {mmss(dur)}", who, "", adate(date),
               "건 전화" if out else "받은 전화" if answered else "부재중 전화")


def _photo(id, date, kind, lat, lon, name, title, desc, cam):
    cam = (cam or "").strip()
    where = f"위치 {lat:.4f}, {lon:.4f}" if lat is not None and lon is not None and abs(lat) <= 90 and (lat or lon) else ""
    return rec("phone_photo", id, " · ".join(x for x in ("영상" if kind else "사진", cam, where, desc) if x),
               cam, "", adate(date), title or name)


PHONE_DB = [   # (저장소, 파일, 읽는 문장, 한 줄 → 글)
    ("phone_sms", LIB / "Messages/chat.db",
     "select m.guid, m.text, m.attributedBody, m.date, m.is_from_me, coalesce(h.id, m.cache_roomnames, '') "
     "from message m left join handle h on h.ROWID = m.handle_id",
     lambda id, text, body, date, me, who: rec("phone_sms", id, text or attr_text(body), who, "", adate(date),
                                               "보낸 문자" if me else "받은 문자")),
    ("phone_call", LIB / "Application Support/CallHistoryDB/CallHistory.storedata",
     "select ZUNIQUE_ID, ZDATE, ZDURATION, ZADDRESS, ZNAME, ZORIGINATED, ZANSWERED from ZCALLRECORD", _call),
    # ponytail: 메모는 제목 + 앞부분(스니펫)만 읽는다 — 본문 전체는 압축된 묶음(ZICNOTEDATA.ZDATA)이라
    #           실제 메모가 동기화되면 그때 풀어 읽는 코드를 더한다. 잠근 메모·지운 메모는 읽지 않는다.
    ("phone_note", LIB / "Group Containers/group.com.apple.notes/NoteStore.sqlite",
     "select ZIDENTIFIER, ZTITLE1, ZSNIPPET, coalesce(ZMODIFICATIONDATE1, ZCREATIONDATE3, ZCREATIONDATE1) "
     "from ZICCLOUDSYNCINGOBJECT where ZTITLE1 is not null and coalesce(ZMARKEDFORDELETION, 0) = 0 "
     "and coalesce(ZISPASSWORDPROTECTED, 0) = 0",
     lambda id, title, snip, date: rec("phone_note", id, snip or title, "메모 앱", "", adate(date), title)),
    # ponytail: 녹음은 이름·날짜·길이만 담는다. 말소리를 글로 옮기는 일(whisper-cli)은 아직 안 한다.
    ("phone_voice", LIB / "Group Containers/group.com.apple.VoiceMemos.shared/Recordings/CloudRecordings.db",
     "select ZUNIQUEID, ZCUSTOMLABEL, ZDATE, ZDURATION, ZPATH from ZCLOUDRECORDING",
     lambda id, label, date, dur, path: rec("phone_voice", id, f"음성 녹음 · {mmss(dur)} · {Path(path or '').name}",
                                            "음성 메모 앱", "", adate(date), label or Path(path or "녹음").stem)),
    # ponytail: 사진은 찍은 날·기기·위치·설명글만 담는다(그림 자체는 안 옮긴다). 가린 사진·지운 사진은 뺀다.
    ("phone_photo", Path.home() / "Pictures/Photos Library.photoslibrary/database/Photos.sqlite",
     "select a.ZUUID, a.ZDATECREATED, a.ZKIND, a.ZLATITUDE, a.ZLONGITUDE, x.ZORIGINALFILENAME, x.ZTITLE, "
     "d.ZLONGDESCRIPTION, e.ZCAMERAMODEL from ZASSET a "
     "left join ZADDITIONALASSETATTRIBUTES x on x.Z_PK = a.ZADDITIONALATTRIBUTES "
     "left join ZASSETDESCRIPTION d on d.Z_PK = x.ZASSETDESCRIPTION "
     "left join ZEXTENDEDATTRIBUTES e on e.Z_PK = a.ZEXTENDEDATTRIBUTES "
     "where a.ZTRASHEDSTATE = 0 and a.ZHIDDEN = 0", _photo),
]


PICS = HERE / "사진미리보기"                 # 사진 앱 사진의 미리보기 사본. 개인 사진이다 — 밖으로 올리지 않는다
WEBIMG = {".jpg", ".jpeg", ".png", ".gif", ".webp"}   # 브라우저가 바로 그리는 그림


def photo_previews(rows):
    """사진 앱에서 들어온 사진(phone_photo, 주소 없음)의 미리보기를 사진미리보기/ 로 베낀다 — 보기 화면(브라우저)은 사진 보관함을 직접 못 읽는다.
    원본이 아니라 사진 앱이 만들어 둔 미리보기(jpeg) 가운데 가장 큰 것을 쓴다. 이미 있으면 건너뛴다. 자료에 든 사진만(가린·지운 사진은 애초에 자료에 없다)."""
    want = {r["id"] for r in rows if r["platform"] == "phone_photo" and not r["url"]} - {f.stem for f in PICS.glob("*.jpg")}
    best = {}
    try:
        for f in (Path.home() / "Pictures/Photos Library.photoslibrary/resources/derivatives").rglob("*.jpeg") if want else []:
            id, size = f.name[:36], f.stat().st_size
            if id in want and size > best.get(id, (0,))[0]:
                best[id] = (size, f)
    except OSError as e:
        print(f"  ! 사진 보관함을 읽지 못함 ({e})")
    for id, (_, f) in best.items():
        PICS.mkdir(exist_ok=True)
        (PICS / f"{id}.jpg").write_bytes(f.read_bytes())
    return len(best)


def pic(r):
    """보기 화면에 바로 그릴 그림의 주소(없으면 빈칸). 사진 앱 사진은 미리보기 사본, 폰자료/ 의 그림 파일은 그 파일."""
    if r["platform"] not in ("phone_photo", "disk"):
        return ""
    if not r["url"]:
        return f"{PICS.name}/{r['id']}.jpg" if (PICS / f"{r['id']}.jpg").exists() else ""
    # ponytail: heic·영상 파일은 그리지 않는다(사파리만 heic 를 그린다). 갤럭시 사진이 heic 로 들어오면 sips 로 jpg 미리보기를 만들 것
    return r["url"] if Path(urlparse(r["url"]).path).suffix.lower() in WEBIMG else ""


def from_phone_files(base=None):
    """폰에서 꺼내 폰자료/ 에 둔 파일. xml = 'SMS Backup & Restore' 앱의 문자·통화 백업,
    txt·md = 글로 내보낸 메모, 그 밖은 녹음·사진 파일(이름·날짜·크기만 담고 '원문 열기'로 파일을 연다)."""
    base, out = Path(base or PHONE_DIR), []
    for f in sorted(p for p in base.rglob("*") if p.is_file() and not p.name.startswith(".")) if base.is_dir() else []:
        ext, name = f.suffix.lower(), unicodedata.normalize("NFC", f.stem)
        id = unicodedata.normalize("NFC", str(f.relative_to(base)))
        if ext == ".xml":
            # ponytail: 파일을 통째로 읽는다(사진이 든 수백 MB 백업이면 iterparse 로 바꿀 것). 사진 문자(MMS)는 아직 안 읽는다.
            try:
                items = list(ET.parse(f).getroot())
            except ET.ParseError as e:
                print(f"  ! {f.name}: 읽지 못함 ({e})")
                continue
            for e in items:
                num = e.get("address") or e.get("number") or ""
                who = e.get("contact_name") if e.get("contact_name") not in (None, "", "(Unknown)") else num
                if e.tag == "sms":
                    out.append(rec("phone_sms", f'{num}|{e.get("date")}', e.get("body"), who, "", e.get("date"),
                                   "보낸 문자" if e.get("type") == "2" else "받은 문자"))
                elif e.tag == "call":
                    kind = {"1": "받은 전화", "2": "건 전화", "3": "부재중 전화"}.get(e.get("type"), "통화")
                    out.append(rec("phone_call", f'{num}|{e.get("date")}', f'{who} · {mmss(e.get("duration"))}',
                                   who, "", e.get("date"), kind))
        elif ext in (".txt", ".md"):
            out.append(rec("phone_note", id, f.read_text(encoding="utf-8", errors="replace"), "폰 메모",
                           f.as_uri(), f.stat().st_mtime, name))
        elif ext in AUDIO | IMAGE:
            what = ("phone_photo", "사진·영상") if ext in IMAGE else ("phone_voice", "음성 녹음")
            if ext in AUDIO and "통화녹음" in id.split("/")[:-1]:      # 폰자료/통화녹음/ 아래 녹음은 종류를 따로 둔다
                what = ("phone_callrec", "통화 녹음")
            out.append(rec(what[0], id, f"{what[1]} 파일 · {f.stat().st_size // 1024:,} KB", "폰 파일",
                           f.as_uri(), f.stat().st_mtime, name))
    return out


def from_phone():
    out = []

    def say(name, where, got):
        ds = sorted(r["date"][:10] for r in got if r["date"])
        print(f"▶ {name} — {where}: {len(got):,}건" + (f"  {ds[0]} ~ {ds[-1]}" if ds else ""))
        out.extend(got)

    for plat, path, sql, row in PHONE_DB:
        if not path.exists():
            print(f"▶ {LABEL[plat]} — 맥에 동기화된 것: 없음 (파일이 없거나 접근이 막혀 있음)")
            continue
        try:
            con = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)      # 읽기 전용 — 앱 자료는 건드리지 않는다
            got = [row(*r) for r in con.execute(sql)]
            con.close()
        except sqlite3.Error as e:
            print(f"▶ {LABEL[plat]} — 맥에 동기화된 것: 읽지 못함 ({e})")
            continue
        say(LABEL[plat], "맥에 동기화된 것", got)
    files = from_phone_files()
    for plat in sorted({r["platform"] for r in files}):
        say(LABEL[plat], "폰자료 폴더", [r for r in files if r["platform"] == plat])
    if not files:
        print(f"▶ 폰자료 폴더: 비어 있음 ({PHONE_DIR})")
    return out


# ---------- 9. 연결한 디스크 (외장하드 · USB · NAS 폴더) ----------
# 보기 화면 왼쪽 「연결」 줄의 「＋ 디스크 연결 · 끊기」 로 고르거나 --disk 폴더 로 한 번 연결하면 연결출처.json 에 적어 두고, 정리할 때마다 다시 읽는다.
# 파일의 이름·종류·크기·날짜·놓인 자리만 담는다(내용은 읽지 않는다 — '원문 열기'로 그 파일을 연다). 디스크를 빼도 전에 읽은 카드는 남는다.

VOLS = Path("/Volumes")
DISK_KIND = [("문서", {".pdf", ".hwp", ".hwpx", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".txt", ".md", ".rtf", ".csv", ".epub", ".pages", ".numbers"}),
             ("그림", {".jpg", ".jpeg", ".png", ".heic", ".gif", ".webp"}), ("소리", AUDIO), ("영상", {".mp4", ".mov", ".avi", ".mkv", ".m4v", ".wmv"})]
DISK_MAX = 20000                         # 연결 하나에 담는 파일 수의 상한 — 보기 화면 파일이 너무 커지지 않게. 넘으면 더 작은 폴더로 나눠 연결한다
DISK_SKIP = {"System Volume Information", "NPKI", "GPKI", "신분증", "node_modules"}   # 인증서·신분증 폴더는 읽지 않는다


def _dirs(names):
    """읽을 폴더만: 숨김·시스템·앱 묶음·인증서 폴더는 뺀다."""
    return sorted(x for x in names if not x.startswith((".", "$", "@", "#")) and not x.endswith((".app", ".photoslibrary"))
                  and unicodedata.normalize("NFC", x) not in DISK_SKIP)


def disk_name(p):
    """연결의 이름: '디스크 이름/폴더' (/Volumes 밖의 폴더는 폴더 이름)."""
    p = Path(p)
    return unicodedata.normalize("NFC", str(p.relative_to(VOLS)) if p.is_relative_to(VOLS) else p.name)


def disk_files(base):
    kinds = set().union(*(k for _, k in DISK_KIND))
    for d, ds, fs in os.walk(base):                  # 바로가기(심볼릭 링크) 폴더는 따라가지 않는다
        ds[:] = _dirs(ds)
        for f in sorted(fs):
            if not f.startswith(".") and os.path.splitext(f)[1].lower() in kinds:
                yield Path(d, f)


def from_disks(paths):
    out = []
    for p in paths:
        base, name = Path(p), disk_name(p)
        if not base.is_dir():
            print(f"▶ 연결 {name}: 지금 붙어 있지 않음 — 전에 읽은 자료는 그대로 둔다")
            continue
        got = list(islice(disk_files(base), DISK_MAX + 1))
        for f in got[:DISK_MAX]:
            try:
                st = f.stat()
            except OSError:
                continue
            rel = unicodedata.normalize("NFC", str(f.relative_to(base)))
            kind = next(k for k, exts in DISK_KIND if f.suffix.lower() in exts)
            out.append(rec("disk", f"{name}/{rel}", f"{kind} 파일 · {st.st_size // 1024:,} KB · {name}/{rel}", name,
                           f.as_uri(), st.st_mtime, unicodedata.normalize("NFC", f.stem)))
        # ponytail: 디스크에서 지운 파일의 카드는 저절로 빠지지 않는다 — 화면에서 지우거나, 연결을 끊었다 다시 연결한다
        print(f"▶ 연결 {name}: {min(len(got), DISK_MAX):,}건"
              + (f"  ⚠ 파일이 더 있습니다 — {DISK_MAX:,}건까지만 담았습니다. 더 작은 폴더로 나눠 연결하세요" if len(got) > DISK_MAX else ""))
    return out


def volumes():
    """지금 맥에 붙어 있는 디스크와 그 맨 위 폴더 이름 — 보기 화면의 연결 창이 보여 준다. 설치용 디스크 이미지(읽기 전용)와 시동 디스크는 뺀다."""
    out = []
    for v in sorted(VOLS.iterdir()) if VOLS.is_dir() else []:
        try:
            if v.is_symlink() or not v.is_dir() or os.statvfs(v).f_flag & os.ST_RDONLY:
                continue
            out.append({"p": str(v), "sub": _dirs(x.name for x in v.iterdir() if x.is_dir())})
        except OSError:
            pass
    return out


# ---------- 합치기 · 저장 · 화면 ----------

def merge(store, new):
    """같은 글은 더 긴 본문을 남기고, 빈 칸(날짜·주소 등)은 서로 채운다. 새로 들어온 수를 돌려준다."""
    added = 0
    for r in new:
        if not (r["text"] or r["title"]):
            continue
        key = (r["platform"], r["id"])
        old = store.get(key)
        if old is None:
            store[key] = r
            added += 1
            continue
        long, short = (r, old) if len(r["text"]) > len(old["text"]) else (old, r)
        store[key] = {k: long.get(k) or short.get(k, "") for k in {**short, **long}}
    return added


def take_added(data):
    """보기 화면의 '+ 자료 추가' 로 적어 넣은 글. 메모 파일·위키 파일의 "+추가" 칸에 실려 온다 (꺼내고 그 칸은 지운다)."""
    rows = data.pop("+추가", []) if isinstance(data, dict) else []
    return [rec("manual", p.get("id"), p.get("text"), p.get("author"), p.get("url"), p.get("date"), p.get("title"))
            for p in (rows if isinstance(rows, list) else []) if isinstance(p, dict)]


def merge_notes(notes, new):
    """같은 글의 메모는 나중에 고친 쪽(t 가 큰 쪽)을 남긴다."""
    for k, n in new.items():
        if isinstance(n, dict) and n.get("t", 0) > notes.get(k, {}).get("t", 0):
            notes[k] = n
    return notes


def topic(r):
    """주제. 제목·글쓴이(북마크는 폴더 이름)에서 먼저 찾고, 없으면 본문 앞부분에서 찾는다.
    카톡은 대화방 이름만 본다 — 보낸이 별명('상담하는 ○○')이 주제로 잡히면 안 된다."""
    for where in (r["title"] if r["platform"] == "kakao" else f'{r["title"]} {r["author"]}', r["text"][:600]):
        for name, pat in TOPICS:
            if pat.search(where):
                return name
    return "기타"


def shelf(r):
    """저장소: 보통은 platform 그대로. 북마크의 BM_SHELVES 폴더는 폴더 이름으로 따로 센다."""
    if r["platform"] == "disk":                      # 연결한 디스크는 연결 하나가 한 줄
        return "disk_" + r["author"]
    if r["platform"] != "bookmark":
        return r["platform"]
    return next((f for f in r["author"].split(" / ") if f in BM_SHELVES), "bookmark")


def origin(r):
    """출처: 카톡은 대화방, 북마크는 사이트, 나머지는 글쓴이(없으면 사이트)."""
    host = urlparse(r["url"]).netloc.removeprefix("www.")
    if r["platform"] == "kakao":
        return r["title"] or "카톡"
    return (host if r["platform"] == "bookmark" else r["author"] or host) or "알 수 없음"


def put_away(files):
    """다 읽은 내려받기 파일을 메모백업/ 으로 옮긴다."""
    keep = HERE / "메모백업"
    keep.mkdir(exist_ok=True)
    for f in files:
        f.replace(keep / f.name)


def note_md(r, n, k):
    """글 하나를 옵시디언 노트(파일 이름, 내용)로. 머리말은 볼트의 source 형식(PKM/01 가이드 §4)을 따른다.
    본문은 한 글자도 고치지 않고 그대로 싣는다."""
    q = lambda v: json.dumps(str(v), ensure_ascii=False)          # YAML 에서도 안전한 따옴표 문자열
    clean = lambda v, size: re.sub(r"\s+", " ", re.sub(r'[/\\:*?"<>|#^\[\]]', " ", v)).strip()[:size]
    first = (r["text"].strip().splitlines() or [""])[0]
    title = (first if r["platform"] == "kakao" or not r["title"] else r["title"])   # 카톡의 제목 칸은 대화방 이름이다
    title = re.sub(r"^\d{4}-\d{2}-\d{2}[-\s]*", "", title).strip() or "제목 없음"
    today, where, dom = datetime.now().strftime("%Y-%m-%d"), LABEL.get(shelf(r), shelf(r).removeprefix("disk_")), topic(r)
    memo, tags = (n.get("m") or "").strip(), [clean(g, 40) for g in n.get("g", [])]
    head = ["---", "type: source", "aliases: []",
            f"description: {q(f'KBG-통합자료수집기에서 고른 {where} 자료 — {clean(title, 60)}')}",
            f"author: {VAULT_AUTHOR}", f"date created: {today}", f"date modified: {today}", "tags:", "  - 통합자료"]
    head += [f"  - {q(g.replace(' ', '-'))}" for g in tags]
    head += [f"source_type: {'youtube' if 'youtu' in r['url'] else 'article' if r['url'] else 'note'}",
             f"channel: {q(origin(r))}", f"source: {q(r['url'])}",
             f"why: {q(memo.splitlines()[0]) if memo else ''}", "use_for:"]
    head += [f"domain: {dom}"] * (dom != "기타") + ["status: inbox", f"sns_key: {q(k)}", "---"]
    info = [where, origin(r), r["author"] if r["author"] != origin(r) else "", r["date"][:10] or "날짜 없음",
            f"[원문]({r['url']})" if r["url"] else ""]
    body = [f"# {title}", "", "> [!info] 출처", "> " + " · ".join(x for x in info if x), ""]
    body += ["## 내 메모", memo, ""] * bool(memo)
    body += ["## 연결", " · ".join(f"[[{g}]]" for g in tags), ""] * bool(tags)
    name = f"{(r['date'] or today)[:10]} {clean(title, 60)} ({clean(origin(r), 30)})"
    return name, "\n".join(head + body + ["## 원문", r["text"], ""])


def write_new(folder, name, text, mark):
    """새 파일로만 쓴다. 같은 이름이 있으면 — 같은 글(mark 가 들어 있음)이면 건너뛰고, 다른 글이면 이름 뒤에 번호를 붙인다.
    새로 쓴 파일의 경로를 돌려준다 (안 썼으면 None)."""
    for i in range(1, 30):
        p = folder / f"{name}{'' if i == 1 else f' {i}'}.md"
        try:
            with open(p, "x", encoding="utf-8") as fh:               # 'x': 있는 파일은 절대 덮어쓰지 않는다
                fh.write(text)
            return p
        except FileExistsError:
            if mark in p.read_text(encoding="utf-8", errors="ignore"):
                return None
    return None


def to_obsidian(store, notes, folder=None):
    """보기 화면의 '옵시디언 위키로 보내기' 로 내려받은 파일(tonghap_wiki_*.json)의 글을 옵시디언 노트로 만든다.
    새 노트만 만든다 — 있던 노트는 고치지도 옮기지도 않는다. 새로 만든 노트의 경로들을 돌려준다."""
    folder = folder or VAULT_INBOX
    files = sorted(DL.glob("tonghap_wiki_*.json"))
    if not files:
        return []
    if not folder.parent.is_dir():
        print(f"⚠ 옵시디언 폴더가 없어 보내지 못함: {folder.parent} (내려받은 파일은 그대로 둠)")
        return []
    folder.mkdir(exist_ok=True)
    made, had, lost = [], 0, 0
    done = []
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            merge(store, take_added(data))                           # 방금 적어 넣은 글을 고른 경우
            keys = [str(k) for k in data["keys"]]
            merge_notes(notes, data.get("notes", {}))                # 고른 글의 메모·태그가 같이 온다
        except (ValueError, AttributeError, KeyError, TypeError, OSError) as e:
            print(f"⚠ 위키 파일을 못 읽음: {f.name} ({e})")
            continue
        for k in keys:
            r = store.get(tuple(k.split("|", 1)))
            if not r:
                lost += 1
            elif r.get("file"):                                      # 옵시디언 노트에서 읽어 온 글은 이미 노트다
                had += 1
            elif p := write_new(folder, *note_md(r, notes.get(k, {}), k), f"sns_key: {json.dumps(k, ensure_ascii=False)}"):
                made.append(p)
            else:
                had += 1
        done.append(f)
    if done:
        NOTES.write_text(json.dumps(notes, ensure_ascii=False), encoding="utf-8")
        put_away(done)
    print(f"▶ 옵시디언으로 보냄: 새 노트 {len(made)}건 · 이미 있는 글 {had}건 · 자료에서 못 찾은 글 {lost}건 → {folder}")
    return made


def purge(store, notes, trash=None):
    """보기 화면에서 지운 글(메모의 x 표시)을 자료에서 빼 보관/지운자료.jsonl 에 옮겨 적는다. 뺀 수를 돌려준다.
    x 표시는 메모태그.json 에 남는다 — 같은 글이 다시 수집돼도 들어오지 않게 하려는 것이다."""
    gone = [store.pop(k) for k in [k for k in store if notes.get("|".join(k), {}).get("x")]]
    if gone:
        trash = trash or TRASH
        trash.parent.mkdir(exist_ok=True)
        with open(trash, "a", encoding="utf-8") as fh:
            fh.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in gone)
    return len(gone)


def stamp():
    """자동 수집이 지켜보는 파일들의 [경로, 크기, 고친 시각]. 지난번과 같으면 새로 읽을 것이 없다."""
    fs = [f for pat in ("sns_*posts*.json", "tonghap_memo_*.json", "tonghap_wiki_*.json", "tonghap_now_*.json") for f in DL.glob(pat)]
    fs += kakao_files(load(KAKAO_PY)) + bookmark_files() + ARTIFACTS
    fs += [f for d in INBOX_DIRS for f in Path(d).expanduser().rglob("*.md") if not any(p.startswith(".") for p in f.parts)]
    out = []
    for f in fs:
        try:
            st = f.stat()
            out.append([str(f), st.st_size, int(st.st_mtime)])
        except OSError:
            pass
    # 폰자료 폴더(2026-11-14 사용자 "폰도 넣어"): ponytail: 파일이 만 개가 넘어 낱낱이 적지 않고 전체 크기·가장 최근 시각만 본다 — 0바이트 파일만 바뀌면 못 잡는다
    ph = [f.stat() for f in PHONE_DIR.rglob("*") if f.is_file() and not f.name.startswith(".")] if PHONE_DIR.is_dir() else []
    if ph:
        out.append([str(PHONE_DIR), sum(x.st_size for x in ph), int(max(x.st_mtime for x in ph))])
    # 디스크: 꽂거나 뺀 것(연결 창의 목록이 바뀐다)과, 연결한 폴더 바로 아래의 변화만 본다. ponytail: 깊은 폴더 속 변화는 다른 일로 정리가 돌 때 같이 잡힌다
    links = json.loads(LINKS.read_text(encoding="utf-8")).get("disk", []) if LINKS.exists() else []
    for p in [v["p"] for v in volumes()] + links:
        if Path(p).is_dir():
            out.append([p, 0, int(Path(p).stat().st_mtime) if p in links else 0])
    return sorted(out)


def agent(on):
    """자동 수집을 켜고 끄는 등록 파일. 켜면 macOS 가 지켜보는 곳이 바뀔 때(그리고 10분마다) `통합정리.py --auto` 를 돌린다.
    등록(bootstrap)은 main 이 한 번 정리를 마친 뒤에 한다."""
    subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}/{AGENT.stem}"], capture_output=True)
    if not on:
        AGENT.unlink(missing_ok=True)
        return
    log = str(Path.home() / "Library/Logs/tonghap-auto.log")
    watch = [DL] + [Path(d).expanduser() for d in INBOX_DIRS] + bookmark_files() + ARTIFACTS + [PHONE_DIR, PHONE_DIR / "통화녹음", VOLS]   # 폴더는 바로 아래 변화만 알린다 — 나머지는 10분 주기가 잡는다
    AGENT.write_bytes(plistlib.dumps({
        "Label": AGENT.stem, "ProgramArguments": [sys.executable, str(Path(__file__).resolve()), "--auto"],
        "WatchPaths": [str(p) for p in watch if p.exists()], "StartInterval": 600, "ThrottleInterval": 20, "RunAtLoad": True,
        "StandardOutPath": log, "StandardErrorPath": log, "EnvironmentVariables": {"PYTHONUTF8": "1", "PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"},   # PATH: yt-dlp 를 찾으려고
        "ProcessType": "Background", "LowPriorityIO": True}))


def load_notes(store):
    """보기 화면의 '메모 파일로 저장' 으로 내려받은 파일을 메모태그.json 에 합친다. 같이 실려 온 '+ 자료 추가' 글은 store 에 더한다."""
    notes = json.loads(NOTES.read_text(encoding="utf-8")) if NOTES.exists() else {}
    done = []
    for f in sorted(DL.glob("tonghap_memo_*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            got = merge(store, take_added(data))
            if got:
                print(f"▶ 직접 추가한 자료 {got}건")
            merge_notes(notes, data)
            done.append(f)
        except (ValueError, AttributeError, OSError) as e:      # 깨진 파일은 건드리지 않고 넘어간다
            print(f"⚠ 메모 파일을 못 읽음: {f.name} ({e})")
    if done:
        NOTES.write_text(json.dumps(notes, ensure_ascii=False), encoding="utf-8")   # 먼저 쓰고 나서 옮긴다
        put_away(done)
        print(f"▶ 메모 파일 {len(done)}개 합침")
    return notes


PAGE = """<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KBG-통합자료수집기</title>
<style>
/* 구성: 띠 색 상단바 + 큰 제목 + 단추 줄 + 왼쪽 칸 + 카드 격자 + 펼침 창 (KBG DATA Labs 화면을 본뜸). 글꼴은 이 컴퓨터 것만 쓴다(밖으로 요청 없음). */
:root{--ink:#111;--ink-soft:#3A3733;--paper:#F4F2ED;--card:#fff;--muted:#6F695F;--line:#E2DED4;--hover:#EBE7DE;--used:#FDFCF9;--used-line:#D9D2C2;--mark:#FBE9AE;
--foot:#111;--foot-text:#EDE9E1;--foot-muted:#9C968A;--foot-line:#2A2724;
--sans:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",system-ui,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,monospace;--rail:250px;
--band:#FEC200;--band-deep:#E5A800;--pop:#E8734A;--on-band:#3B2E00;--on-band-2:#5C4A00;--brand-sub:#6B5400;--band-ink:#111}
@media(prefers-color-scheme:dark){:root{--ink:#F1EEE6;--ink-soft:#D7D2C7;--paper:#171614;--card:#201F1C;--muted:#A39C8E;--line:#35322C;--hover:#2A2824;--used:#1B1A17;--used-line:#3F3B33;--mark:#5A4A12;--foot:#0E0D0C;color-scheme:dark}}
:root[data-accent="coral"]{--band:#F26B4E;--band-deep:#D5583D;--pop:#1F4E9C;--on-band:#3B1208;--on-band-2:#5C2412;--brand-sub:#6E2A16}
:root[data-accent="blue"]{--band:#8EC5FF;--band-deep:#5FA8F5;--on-band:#0B2A4A;--on-band-2:#1E4470;--brand-sub:#1E4470}
:root[data-accent="green"]{--band:#A8E05F;--band-deep:#8CC84B;--on-band:#1F3A08;--on-band-2:#2F5410;--brand-sub:#2F5410}
:root[data-accent="violet"]{--band:#C9B6FF;--band-deep:#A98CF5;--on-band:#2A1A5E;--on-band-2:#3E2A80;--brand-sub:#3E2A80}
*{box-sizing:border-box}[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 var(--sans);-webkit-font-smoothing:antialiased}
a{color:inherit}button,input,textarea,select{font-family:inherit}button{cursor:pointer}
:focus-visible{outline:3px solid var(--pop);outline-offset:2px}
.in{max-width:1320px;margin:0 auto;padding:0 16px}
/* 상단바 */
.bar{position:sticky;top:0;z-index:50;background:var(--band);border-bottom:2px solid var(--band-ink)}
.bar-in{padding-block:10px;display:flex;align-items:center;gap:16px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;flex-shrink:0;color:var(--band-ink)}
.brand .mk{width:30px;height:30px;border-radius:6px;background:var(--band-ink);color:var(--band);font:700 11px var(--mono);display:flex;align-items:center;justify-content:center;letter-spacing:-.04em}
.brand b{font-size:15px;letter-spacing:-.02em;font-weight:800;display:block;line-height:1.3}
.brand small{display:block;font:9.5px var(--mono);letter-spacing:.14em;color:var(--brand-sub)}
.search{flex:1;display:flex;align-items:center;gap:9px;background:var(--card);border:2px solid var(--band-ink);border-radius:999px;padding:7px 16px;min-width:0}
.search input{border:0;outline:0;background:transparent;font-size:14px;width:100%;color:var(--ink);min-width:0}
.search input::placeholder{color:var(--muted)}
.search:focus-within{outline:3px solid var(--pop);outline-offset:2px}
.search kbd{font:10px var(--mono);border:1px solid var(--line);border-radius:4px;padding:1px 5px;color:var(--muted);flex-shrink:0}
.counter{flex-shrink:0;font:11px var(--mono);letter-spacing:.06em;background:var(--band-ink);color:var(--band);padding:8px 13px;border-radius:999px;white-space:nowrap;font-variant-numeric:tabular-nums}
.counter b{color:#fff}
/* 큰 제목 */
.hero{background:var(--band);border-bottom:2px solid var(--band-ink);overflow:hidden;color:var(--band-ink)}
.hero-in{padding-block:44px 38px;position:relative}
.aster{position:absolute;right:34px;top:10px;font-size:160px;line-height:1;color:var(--pop);opacity:.9;user-select:none;pointer-events:none}
.hero h1{font-size:clamp(34px,6vw,70px);line-height:1;letter-spacing:-.035em;font-weight:800;margin:0 0 14px;word-break:keep-all}
.hero h1 em{font-style:normal;font-family:var(--mono);font-weight:700;letter-spacing:-.04em}
.hero .lead{font-size:clamp(15px,2vw,19px);font-weight:600;margin:0 0 6px;color:var(--on-band)}
.hero .sub{font-size:14px;color:var(--on-band-2);max-width:60ch;margin:0 0 20px;word-break:keep-all}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{background:var(--band-ink);color:var(--band);border-radius:999px;padding:7px 15px;font-size:12.5px;font-weight:600;text-decoration:none;border:1.5px solid var(--band-ink)}
.chip.ghost{background:transparent;color:var(--band-ink)}a.chip.ghost:hover{background:var(--band-ink);color:var(--band)}
/* 단추 줄 */
.tools{position:sticky;top:var(--bh,56px);z-index:40;background:var(--paper);border-bottom:1px solid var(--line)}
.tools-in{padding-block:10px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.tg{border:1.5px solid var(--line);background:var(--card);color:var(--ink-soft);border-radius:999px;padding:6px 14px;font-size:12.5px;font-weight:600;white-space:nowrap;transition:.14s}
.tg:hover{border-color:var(--ink)}
.cathead{scroll-margin-top:calc(var(--bh,0px) + var(--th,0px) + 12px)}
.pc .ph{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:8px;background:var(--line);margin-top:10px}
.lv .pc .ph{width:44px;height:44px;aspect-ratio:auto;margin:0;border-radius:6px;flex-shrink:0}
.grid.pics{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:6px}
.tile{position:relative;aspect-ratio:1;border:0;padding:0;border-radius:8px;overflow:hidden;background:var(--line);cursor:pointer;min-width:0}
.tile img{width:100%;height:100%;object-fit:cover;display:block}
.tile span{position:absolute;left:0;right:0;bottom:0;padding:16px 7px 5px;font:10.5px var(--mono);color:#fff;text-align:left;background:linear-gradient(transparent,rgba(0,0,0,.62))}
.tile.on{outline:3px solid var(--ink);outline-offset:-3px}
.d .shot{display:block;max-width:100%;max-height:72vh;margin:14px auto 0;border-radius:10px}
.d .shotw{position:relative;margin-top:14px}.d .shotw .shot{margin-top:0}
.d .nav{position:absolute;top:50%;transform:translateY(-50%);width:42px;height:42px;border-radius:50%;border:0;background:rgba(0,0,0,.55);color:#fff;font-size:24px;line-height:1;cursor:pointer}
.d .nav:hover{background:rgba(0,0,0,.82)}.d .nav.pv{left:8px}.d .nav.nx{right:8px}
.d .shotw .at{position:absolute;left:50%;bottom:8px;transform:translateX(-50%);padding:2px 10px;border-radius:999px;background:rgba(0,0,0,.55);color:#fff;font:11px var(--mono)}.d .more{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px}
.pager{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;align-items:center;margin:26px 0 10px}.pager .tg{min-width:38px;padding:6px 10px}.pager .tg:disabled{opacity:.35}.pager span{color:var(--muted);font-size:12.5px}
.tg[aria-pressed="true"]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.tg.star[aria-pressed="true"]{background:var(--pop);border-color:var(--pop);color:#fff}
.tg.add{background:var(--band);border-color:var(--band-ink);color:var(--band-ink)}.tg.add:hover{background:var(--band-deep)}
select.tg{appearance:none;-webkit-appearance:none;padding-right:26px;background-image:linear-gradient(45deg,transparent 50%,currentColor 50%),linear-gradient(135deg,currentColor 50%,transparent 50%);background-position:calc(100% - 14px) 50%,calc(100% - 10px) 50%;background-size:4px 4px;background-repeat:no-repeat}
.spacer{flex:1;min-width:8px}.sep{width:1px;height:22px;background:var(--line);flex-shrink:0}
.pal{display:flex;align-items:center;gap:6px;padding:0 4px}
.pal button{width:24px;height:24px;border-radius:50%;border:2px solid var(--line);background:var(--c);padding:0;transition:.14s}
.pal button:hover{transform:scale(1.15);border-color:var(--ink)}
.pal button[aria-pressed="true"]{border-color:var(--ink);box-shadow:inset 0 0 0 2px var(--card)}
/* 배치 */
.wrap{padding-block:24px 70px;display:grid;grid-template-columns:var(--rail) 1fr;gap:30px;align-items:start}.wrap>*{min-width:0}
.rail{position:sticky;top:calc(var(--bh,56px) + var(--th,52px) + 16px);max-height:calc(100vh - var(--bh,56px) - var(--th,52px) - 32px);overflow-y:auto;padding-right:4px}
.rail summary{font:10px var(--mono);letter-spacing:.16em;color:var(--muted);margin:16px 0 8px;cursor:pointer}
.rail details:first-child summary{margin-top:0}
.rail .src{display:flex;gap:9px;align-items:baseline;padding:6px 10px;border-radius:8px;border:0;border-left:2px solid transparent;width:100%;background:transparent;color:var(--ink);text-align:left;font-size:13.5px;transition:.14s}
.rail .src:hover{background:var(--hover)}
.rail .src[aria-pressed="true"]{background:var(--card)}
.rail .src i{font:11px var(--mono);font-style:normal;color:var(--muted);width:22px;flex-shrink:0}
.rail .src[aria-pressed="true"] i{color:var(--pop)}
.rail .src b{font-weight:600;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rail .src .n{font:11px var(--mono);color:var(--muted);font-variant-numeric:tabular-nums}
.rail .src.sub{padding-left:22px;font-size:13px}
.rail .src .tw{display:inline-block;padding:0 9px;font-size:11px;color:var(--muted);cursor:pointer}
.rail .src .tw:hover{color:var(--pop)}
.tagrail{display:flex;flex-wrap:wrap;gap:5px}
.tagrail button{border:1px solid var(--line);background:var(--card);color:var(--ink-soft);border-radius:999px;padding:2px 9px;font-size:11.5px;font-weight:600}
.tagrail button[aria-pressed="true"]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.tagrail button i{font:10.5px var(--mono);font-style:normal;color:var(--muted);margin-left:4px}
.tagrail button[aria-pressed="true"] i{color:var(--paper);opacity:.75}
.tagrail .ren{border-style:dashed;color:var(--ink)}
.note{display:block;font:11.5px var(--mono);color:var(--muted);margin:6px 0 0 10px}
.cathead{display:flex;align-items:baseline;flex-wrap:wrap;gap:6px 14px;border-bottom:2px solid var(--ink);padding-bottom:9px;margin:0 0 16px}
.cathead .num{font:700 13px var(--mono);color:var(--pop)}
.cathead h2{font-size:21px;margin:0;letter-spacing:-.02em;font-weight:800;word-break:keep-all}
.cathead .sub{margin-left:auto;font-size:12.5px;color:var(--muted);text-align:right}
#bulk{position:sticky;top:calc(var(--bh,56px) + var(--th,52px));z-index:30;background:var(--paper);display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:8px 0;margin:-8px 0 8px}
#bulk span{font-size:13px;font-weight:700}
#bulk input{flex:1;min-width:180px;border:1.5px solid var(--line);border-radius:999px;padding:6px 14px;font-size:13px;background:var(--card);color:var(--ink)}
#warn{color:#b3261e;font-size:13px;font-weight:600;margin-bottom:10px}#warn:empty{display:none}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:14px}
/* 카드 */
.pc{position:relative;background:var(--card);border:1.5px solid var(--line);border-radius:12px;padding:14px 16px 46px;transition:transform .13s,box-shadow .13s,border-color .13s;min-width:0;cursor:pointer}
.pc:hover{border-color:var(--ink);transform:translateY(-2px);box-shadow:5px 6px 0 rgba(17,17,17,.1)}
.pc.used{border-color:var(--used-line);background:var(--used)}
.pc .top{display:flex;align-items:center;gap:7px;min-width:0}
.pc .pick{width:16px;height:16px;margin:0;flex-shrink:0;accent-color:var(--ink)}
.pc .no{font:11px var(--mono);color:var(--muted);margin-left:auto;white-space:nowrap}
.badge{font:11px var(--mono);letter-spacing:.04em;border:1px solid var(--line);border-radius:4px;padding:1px 6px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.badge.st{background:var(--ink);border-color:var(--ink);color:var(--paper)}
.pc h3{margin:9px 0 0;font-size:15.5px;line-height:1.35;letter-spacing:-.01em;font-weight:700;overflow-wrap:anywhere;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.pc .tx{margin:7px 0 0;font-size:13.4px;line-height:1.6;color:var(--ink-soft);overflow-wrap:anywhere;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
mark{background:var(--band);color:var(--band-ink);padding:0 2px;border-radius:2px}
.pc .mine{margin-top:8px;display:flex;flex-wrap:wrap;gap:5px}.pc .mine:empty{display:none}
.tags span,.pc .mine span{border:1px solid var(--line);border-radius:999px;padding:1px 9px;font-size:11.5px;color:var(--ink-soft)}
.pc .mine div{flex-basis:100%;border-left:3px solid var(--pop);padding-left:9px;font-size:13px;overflow-wrap:anywhere;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.pc .meta{display:flex;flex-wrap:wrap;gap:4px 12px;margin-top:9px;font:11px var(--mono);color:var(--muted)}
.pc .meta span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:100%}
.pc .act{position:absolute;left:16px;right:12px;bottom:9px;display:flex;align-items:center;justify-content:space-between;gap:8px}
.pc .act>span{display:flex;gap:4px;align-items:center}
.pc .hint{border:0;background:transparent;padding:2px 0;font-size:11.5px;color:var(--muted);font-weight:600}
.pc .cp{border:1.5px solid var(--line);background:transparent;color:var(--ink-soft);border-radius:999px;padding:2px 10px;font-size:11.5px;font-weight:600;text-decoration:none}
.pc .cp:hover{border-color:var(--ink);color:var(--ink)}
.fav{border:0;background:transparent;font-size:16px;line-height:1;padding:4px;color:var(--muted);transition:.14s}
.fav:hover,.fav.on{color:var(--pop)}
/* 목록 보기 */
.grid.lv{grid-template-columns:1fr;gap:6px}
.lv .pc{display:flex;align-items:center;gap:12px;padding:8px 14px;border-radius:8px}
.lv .pc:hover{transform:none;box-shadow:none}
.lv .pc .top{flex-shrink:0}.lv .pc .no{margin-left:0}
.lv .pc h3{margin:0;font-size:14px;flex:0 1 auto;max-width:45%;-webkit-line-clamp:1}
.lv .pc .tx{margin:0;flex:1;min-width:0;-webkit-line-clamp:1}
.lv .pc .mine,.lv .pc .meta,.lv .pc .hint{display:none}
.lv .pc .act{position:static;flex-shrink:0}
.empty{padding:60px 10px;text-align:center;color:var(--muted)}.empty b{display:block;color:var(--ink);font-size:17px;margin-bottom:6px}
/* 펼침 창 */
.ov{position:fixed;inset:0;background:rgba(17,17,17,.55);z-index:80;display:flex;align-items:center;justify-content:center;padding:24px 16px}
.md{background:var(--card);color:var(--ink);border:2px solid var(--ink);border-radius:14px;width:100%;max-width:780px;max-height:100%;display:flex;flex-direction:column;box-shadow:8px 10px 0 rgba(17,17,17,.18)}
.md-h{display:flex;align-items:center;gap:10px;padding:14px 18px;border-bottom:2px solid var(--ink);background:var(--band);color:var(--band-ink);border-radius:12px 12px 0 0}
.md-h b{font-size:16px;letter-spacing:-.01em;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.md-h .x{border:0;background:transparent;font-size:22px;line-height:1;color:var(--band-ink);padding:2px 8px}
.md-b{padding:18px;overflow-y:auto;flex:1;min-height:0}
.md-f{display:flex;gap:8px;flex-wrap:wrap;padding:12px 18px;border-top:1px solid var(--line);align-items:center}
.btn{border:1.5px solid var(--ink);background:var(--card);color:var(--ink);border-radius:999px;padding:7px 15px;font-size:13px;font-weight:700;text-decoration:none}
.btn.pri{background:var(--ink);color:var(--paper)}.btn.danger{border-color:#b3261e;color:#b3261e}
dialog.ask{border:0;border-radius:14px;padding:22px;width:min(460px,90vw);background:var(--card);color:var(--ink);box-shadow:0 18px 60px rgba(0,0,0,.3)}
dialog.ask::backdrop{background:rgba(0,0,0,.45)}
dialog.ask p{white-space:pre-wrap;overflow-wrap:anywhere;margin:0 0 18px;line-height:1.55;font-size:14px}
dialog.ask div{display:flex;gap:8px;justify-content:flex-end}
dialog.link{width:min(560px,92vw)}dialog.link p{margin:8px 0 12px;font-size:13px;color:var(--muted)}
dialog.link ul{list-style:none;margin:0 0 16px;padding:0;max-height:52vh;overflow-y:auto;border-top:1px solid var(--line)}
dialog.link li{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:7px 2px;border-bottom:1px solid var(--line);font-size:14px;font-weight:600}
dialog.link li.sub{padding-left:22px;font-weight:400;font-size:13px}dialog.link li span{overflow-wrap:anywhere}
.d .k{font:11px var(--mono);letter-spacing:.16em;color:var(--muted);margin:18px 0 6px}
.d .metal{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font:11px var(--mono);color:var(--muted)}
.d .warn{margin-top:16px;padding:10px 12px;border:1.5px solid #b3261e;border-radius:8px;color:#b3261e;font-size:13px;line-height:1.55;word-break:keep-all}
.d input,.d textarea,.d select{display:block;width:100%;border:1.5px solid var(--line);border-radius:8px;padding:9px 11px;background:var(--paper);color:var(--ink);font-size:14px;line-height:1.55}
.d textarea{margin-top:8px;min-height:84px;resize:vertical}
.d .body{white-space:pre-wrap;overflow-wrap:anywhere;font-size:14px;line-height:1.7;color:var(--ink-soft)}
/* 바닥 */
footer{background:var(--foot);color:var(--foot-text);border-top:2px solid var(--ink)}
.fin{padding-block:44px 36px;display:flex;flex-wrap:wrap;gap:32px;justify-content:space-between;align-items:flex-start}
footer h5{margin:0 0 8px;font-size:15px;color:#fff}footer p{margin:0;font-size:13px;color:var(--foot-muted);max-width:52ch;word-break:keep-all}
.sig{border-top:1px solid var(--foot-line);padding:16px 0 30px;font:11px var(--mono);color:var(--foot-muted);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
#toast{position:fixed;left:50%;bottom:26px;transform:translate(-50%,260%);background:var(--band-ink);color:var(--band);padding:12px 20px;border-radius:999px;font-size:13.5px;font-weight:700;z-index:99;transition:transform .24s cubic-bezier(.6,0,.2,1);box-shadow:0 8px 24px rgba(0,0,0,.22);max-width:90vw;text-align:center}
#toast.show{transform:translate(-50%,0)}
@media(max-width:960px){
.wrap{grid-template-columns:1fr;gap:18px;padding-top:16px}
.tools{position:static}#bulk{top:var(--bh,56px)}
.rail{position:static;max-height:none;overflow:visible;border-bottom:1px solid var(--line);padding:0 0 14px}
.aster{font-size:100px;right:10px;top:6px;opacity:.75}.hero-in{padding-block:32px 28px}
.bar-in{flex-wrap:wrap;gap:10px}.search{order:3;flex-basis:100%}.search kbd{display:none}
.cathead .sub{margin-left:0;text-align:left;flex-basis:100%}.grid{grid-template-columns:1fr}
.lv .pc{flex-wrap:wrap}.lv .pc h3{max-width:100%}.lv .pc .tx{flex-basis:100%}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
<header class="bar" id="bar"><div class="in bar-in">
<a class="brand" href="#top"><span class="mk">KBG</span><span><b>KBG-통합자료수집기</b><small>SNS · BOOKMARK · ARCHIVE</small></span></a>
<label class="search"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
<input id="q" type="search" placeholder="찾기 — 내용·제목·글쓴이·출처·북마크 폴더·메모·태그" aria-label="검색" autocomplete="off"><kbd>/</kbd></label>
<div class="counter">자료 <b id="cnt">0</b> · ★ <b id="favcnt">0</b></div>
</div></header>
<div class="hero" id="top"><div class="in hero-in"><div class="aster" aria-hidden="true">✳</div>
<h1><em>KBG</em> 통합<br>자료수집기</h1>
<p class="lead">카톡·페이스북·북마크·쓰레드·유튜브·인박스·Claude 아티팩트 자료를 한곳에.</p>
<p class="sub">__SUB__. 카드를 누르면 전체 내용이 펼쳐지고 메모·태그를 달 수 있습니다. 왼쪽 칸에서 저장소·주제·일시·출처로 나누어 보고, 체크한 자료는 옵시디언 위키로 보냅니다.</p>
<div class="chips"><span class="chip" id="chipS"></span><span class="chip" id="chipN"></span><span class="chip" id="chipA"></span>
<a class="chip ghost" href="obsidian://open?vault=Obsidian%202025">◈ 옵시디언 열기</a>
<a class="chip ghost" href="https://www.threads.com/saved" target="_blank" rel="noopener">@ 쓰레드 저장 목록</a>
<a class="chip ghost" href="https://www.facebook.com/" target="_blank" rel="noopener">f 페이스북</a></div>
</div></div>
<nav class="tools" id="tools" aria-label="기간·보기·저장"><div class="in tools-in" id="chipbar"></div></nav>
<div class="in wrap">
<aside class="rail" aria-label="나누어 보기">
<details open><summary>STORE · 저장소</summary><div id="rs"></div></details>
<details open><summary>TOPIC · 주제</summary><div id="rk"></div></details>
<details open><summary>DATE · 일시</summary><div id="rd"></div></details>
<details><summary>SOURCE · 출처</summary><div id="ro"></div></details>
<details open><summary>TAGS · 태그</summary><div id="tagrail" class="tagrail"></div></details>
</aside>
<main>
<div id="warn" role="alert"></div>
<div class="cathead"><span class="num" id="hn"></span><h2 id="ht"></h2><button type="button" class="tg" id="hr">필터 모두 풀기</button><span class="sub" id="hs"></span></div>
<div id="bulk"></div>
<div id="list" class="grid"></div>
<nav id="pager" class="pager" aria-label="쪽 번호" hidden></nav>
</main>
</div>
<footer><div class="in fin">
<div><h5>KBG-통합자료수집기</h5><p>카톡 내보내기, 페이스북, 브라우저 북마크, 쓰레드 저장글, 유튜브 자막, 옵시디언 인박스, 블로그를 한 화면에 모읍니다. 이 화면에는 다른 사람의 글·대화가 들어 있습니다 — 내보내거나 공유할 때는 받는 사람과 보낼 곳을 꼭 확인하세요.</p></div>
<div><h5>사용 방법</h5><p>① 왼쪽 칸과 기간 단추로 거른다 → ② 카드를 눌러 읽고 메모·태그·별표를 단다(직접 적어 넣을 글은 「+ 자료 추가」) → ③ 「메모 파일로 저장」을 누른다 → ④ 옵시디언에 둘 자료는 체크하고 「옵시디언 위키로 보내기」 → ⑤ Claude 에게 「통합 정리해」(자동 수집이 켜져 있으면 저절로). 밖으로 꺼낼 때는 「⇪ 내보내기·공유」, 필요 없는 자료는 체크하고 「삭제」(휴지통에서 되살릴 수 있음).</p></div>
</div><div class="in"><div class="sig"><span>-by KBG-</span><span>KBG-통합자료수집기 · 이 컴퓨터 안에서만 봅니다</span></div></div></footer>
<div id="toast" role="status" aria-live="polite"></div>
<div id="modal" hidden></div>
<script>
const D = __DATA__, N0 = __NOTES__, PP = 20;   // 한 쪽에 보이는 카드 수 (2026-11-14 사용자 요청: 20개씩, 나머지는 아래 번호로)
const NAME = __NAME__, AUTO = __AUTO__, BUILD = __BUILD__, DISKS = __DISKS__;   // AUTO: 자동 수집이 켜져 있는가 (내려받은 파일이 저절로 반영된다)
const NEXT = AUTO ? '자동 수집이 켜져 있어 잠시 뒤 저절로 반영되고 이 화면도 스스로 바뀝니다.' : "Claude 에게 '통합 정리해' 라고 하면 반영됩니다.";
const nm = (p) => NAME[p] || p.replace(/^disk_/, '');   // 연결한 디스크의 줄 이름은 '디스크/폴더'
const $ = (id) => document.getElementById(id);
const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
const btn = (cls, text) => { const b = el('button', cls, text); b.type = 'button'; return b; };
// 그림 한 장. 화면에 들어올 때만 읽고(lazy), 파일이 없으면 자리만 치운다
const img = (src, cls, alt) => { const m = el('img', cls); m.loading = 'lazy'; m.referrerPolicy = 'no-referrer'; m.alt = alt || ''; m.onerror = () => m.remove(); m.src = src; return m; };
const press = (b, on) => b.setAttribute('aria-pressed', String(!!on));
const ls = (k, v) => { try { return v === undefined ? localStorage.getItem(k) : localStorage.setItem(k, v); } catch (e) { return null; } };
let only = false, onlyN = false, trash = false, pic = false, tag = '', days = 0, dname = '', sort = ls('통합자료:정렬') || 'new', view = ls('통합자료:보기') || 'card';
// 왼쪽 칸의 네 가지 나눔(저장소·주제·일시·출처): v = 고른 값, key = 글이 드는 묶음. 서로, 그리고 검색·기간·태그와 함께 쓴다.
const F = { s: { v: '', key: (d) => d.s }, k: { v: '', key: (d) => d.k }, d: { v: '', key: (d) => (d.date ? d.date.slice(0, 7) : '날짜없음') }, o: { v: '', key: (d) => d.o } };
const FK = Object.keys(F);
// 묶음: 저장소 여러 개를 왼쪽 칸에서 한 줄 아래에 모은다 (phone = 폰 자료 전부, thr = 쓰레드 내 글 + 저장글)
const GRP = { phone: (s) => s.startsWith('phone_'), thr: (s) => s.startsWith('threads'), disk: (s) => s.startsWith('disk_') };
const inG = (s) => Object.keys(GRP).find((g) => GRP[g](s));
const inF = (f, d) => !F[f].v || (f === 'd' ? F.d.key(d).startsWith(F.d.v) : f === 's' && GRP[F.s.v] ? GRP[F.s.v](d.s) : F[f].key(d) === F[f].v);   // 일시는 해(2026)·달(2026-03) 둘 다 고를 수 있다
// 메모·태그·별표: {글 열쇠: {m: 메모, g: [태그], s: 별표, t: 고친 시각}}.
// 파일(메모태그.json → N0)에 든 것과 이 브라우저에 든 것 중 나중에 고친 쪽을 쓴다. 지운 것도 빈 칸으로 남겨야 파일 쪽 옛 값이 되살아나지 않는다.
let notes = {};
try { notes = JSON.parse(localStorage.getItem('통합자료:메모') || '{}'); } catch (e) {}
Object.keys(N0).forEach((k) => { if (!notes[k] || N0[k].t > notes[k].t) notes[k] = N0[k]; });
try {  // 예전 방식으로 찍어 둔 별표를 옮겨 온다
  const old = JSON.parse(localStorage.getItem('통합자료:별표') || '{}');
  Object.keys(old).forEach((k) => { if (!(notes[k] || {}).s) notes[k] = Object.assign({}, notes[k], { s: 1, t: Date.now() }); });
  if (Object.keys(old).length) { localStorage.setItem('통합자료:메모', JSON.stringify(notes)); localStorage.removeItem('통합자료:별표'); }
} catch (e) {}
const key = (d) => d.platform + '|' + d.id;
const note = (d) => notes[key(d)] || {};
// 자료 추가: 직접 적어 넣은 글. 우선 이 브라우저에 두고 화면에 바로 보이며, 내려받는 파일의 "+추가" 칸에 실려 다음 "통합 정리해" 때 통합자료.jsonl 에 들어간다.
let pend = [];
try { pend = JSON.parse(localStorage.getItem('통합자료:추가') || '[]'); } catch (e) {}
{ const have = new Set(D.map(key)); pend = pend.filter((d) => d && !have.has(key(d))); pend.forEach((d) => D.unshift(d)); }   // 자료 파일에 들어간 것은 대기 목록에서 뺀다
function keepPend() {
  try { localStorage.setItem('통합자료:추가', JSON.stringify(pend)); }
  catch (e) { $('warn').textContent = "이 브라우저에 저장하지 못했습니다. 창을 닫기 전에 '메모 파일로 저장' 을 눌러 두세요."; }
}
keepPend();
let tt;
// 확인 창. 브라우저의 confirm() 은 쓰지 않는다 — 앱 안 브라우저 등에서는 창이 뜨지 않고 곧바로 '아니오'가 되어 삭제가 먹지 않았다(2026-11-14).
function ask(msg, yesText, yes) {
  const dg = el('dialog', 'ask'), row = el('div'), no = btn('btn', '취소'), ok = btn('btn danger', yesText);
  no.onclick = () => dg.close(); ok.onclick = () => { dg.close(); yes(); }; dg.onclose = () => dg.remove();
  row.append(no, ok); dg.append(el('p', '', msg), row); document.body.appendChild(dg); dg.showModal();   // 처음 초점은 '취소' — Enter 를 잘못 눌러도 지워지지 않는다
}
function say(msg) { const t = $('toast'); t.textContent = msg; t.classList.add('show'); clearTimeout(tt); tt = setTimeout(() => t.classList.remove('show'), 3200); }
// 되돌리기: 한 번의 조작(저장·별표·한꺼번에 달기/떼기·이름 바꾸기)으로 바뀐 글들의 이전 값을 한 묶음으로 쌓아 둔다.
// ponytail: 화면을 닫거나 새로 고치면 되돌리기 기록은 사라진다. 오래 남겨야 하면 묶음을 localStorage 에 둘 것.
const undo = [], redo = []; let batch = {};
const setNote = (k, patch) => { if (!(k in batch)) batch[k] = notes[k]; notes[k] = Object.assign({}, notes[k], patch, { t: Date.now() }); };
function store() {
  try { localStorage.setItem('통합자료:메모', JSON.stringify(notes)); }
  catch (e) { $('warn').textContent = "이 브라우저에 저장하지 못했습니다. 창을 닫기 전에 '메모 파일로 저장' 을 눌러 두세요."; }
}
function commit() {  // 여러 건을 고친 뒤 한 번만 저장한다
  if (Object.keys(batch).length) { undo.push(batch); redo.length = 0; }   // 새로 고치면 '다시 하기' 는 비운다
  batch = {}; store(); bar();
}
function put(d, patch) { setNote(key(d), patch); commit(); }
const tagsOf = (v) => [...new Set(v.split(/[,#]/).map((x) => x.trim()).filter(Boolean))];
const dl = (name, blob) => { const a = el('a'); a.href = URL.createObjectURL(blob); a.download = name; a.click(); };
// 파일로 내려받는다. 다음 "통합 정리해"(또는 자동 수집) 때 통합정리.py 가 읽어 간다
const down = (name, obj) => dl(name + Date.now() + '.json', new Blob([JSON.stringify(obj)], { type: 'application/json' }));
function step(from, to) {  // 묶음 하나를 꺼내 그 값으로 돌리고, 지금 값은 반대쪽에 쌓는다 (되돌리기 ↔ 다시 하기)
  const b = from.pop(), now = {};
  if (!b) return;
  // 시각(t)을 지금으로 새로 찍어야, 이미 파일로 옮긴 값보다 돌린 값이 이긴다
  Object.keys(b).forEach((k) => { now[k] = notes[k]; notes[k] = Object.assign({}, b[k], { t: Date.now() }); });
  to.push(now); store(); bar(); draw();
}
function copy(text) {
  if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
  return new Promise((ok, bad) => {
    const ta = el('textarea'); ta.value = text; ta.style.cssText = 'position:fixed;opacity:0'; document.body.appendChild(ta); ta.select();
    let done = false; try { done = document.execCommand('copy'); } catch (e) {}
    ta.remove(); done ? ok() : bad();
  });
}
function hl(e, text, q) {  // 검색어가 든 자리를 칠한다. 남의 글이므로 글자로만 넣는다(innerHTML 안 씀)
  if (!q) { e.textContent = text; return e; }
  const low = text.toLowerCase(); let i = 0, j;
  while ((j = low.indexOf(q, i)) > -1) { e.append(text.slice(i, j), el('mark', '', text.slice(j, j + q.length))); i = j + q.length; }
  e.append(text.slice(i)); return e;
}
// ---------- 단추 줄: 기간 · 별표/메모만 · 정렬 · 보기 · 되돌리기 · 저장 · 색 ----------
// 기간: 글의 날짜가 오늘부터 며칠 안인 것만 본다. 날짜가 없는 글은 기간을 고르면 빠진다.
const PER = [['전체 기간', 0], ['최근 3일', 3], ['최근 1주일', 7], ['최근 1달', 30], ['최근 3개월', 90]].map(([t, n]) => {
  const b = btn('tg', t); b.dataset.n = n; b.onclick = () => { days = n; dname = n ? t : ''; draw(); }; return b;
});
const sb = btn('tg star'), nb = btn('tg'), pb = btn('tg'), xb = btn('tg'), ub = btn('tg'), rb = btn('tg'), vb = btn('tg'), tb = btn('tg'), eb = btn('tg', '⇪ 내보내기·공유'), gb = btn('tg', '⟳ 지금 업데이트');
sb.onclick = () => { only = !only; draw(); };
nb.onclick = () => { onlyN = !onlyN; draw(); };
pb.onclick = () => { pic = !pic; draw(); };   // 사진 모아보기: 그림이 있는 자료만 바둑판으로
tb.onclick = () => { trash = !trash; sel.clear(); draw(); };   // 휴지통: 지운 글만 본다
eb.onclick = () => exportForm();
xb.onclick = () => {  // → 메모태그.json 에 합쳐진다 (새로 적어 넣은 글은 통합자료.jsonl 로, 지운 글은 자료에서 빠진다)
  down('tonghap_memo_', pend.length ? Object.assign({ '+추가': pend }, notes) : notes);
  say('메모 파일을 내려받았습니다 — ' + NEXT);
};
ub.onclick = () => step(undo, redo);
rb.onclick = () => step(redo, undo);
vb.title = '카드/목록 보기'; vb.onclick = () => { view = view === 'list' ? 'card' : 'list'; ls('통합자료:보기', view); draw(); };
const ss = el('select', 'tg'); ss.setAttribute('aria-label', '정렬');
[['new', '최신순'], ['old', '오래된순'], ['star', '별표 먼저']].forEach(([v, t]) => { const o = el('option', '', t); o.value = v; ss.appendChild(o); });
ss.value = sort; ss.onchange = () => { sort = ss.value; ls('통합자료:정렬', sort); draw(); };
const pal = el('span', 'pal'); pal.title = '메인 컬러';
const setTheme = (id) => { document.documentElement.dataset.accent = id; ls('통합자료:색', id); [...pal.children].forEach((x) => press(x, x.dataset.th === id)); };
[['yellow', '옐로', '#FEC200'], ['coral', '코랄', '#F26B4E'], ['blue', '블루', '#8EC5FF'], ['green', '그린', '#A8E05F'], ['violet', '바이올렛', '#C9B6FF']].forEach(([id, l, c]) => {
  const b = btn(); b.dataset.th = id; b.title = l; b.setAttribute('aria-label', l + ' 색'); b.style.setProperty('--c', c); b.onclick = () => setTheme(id); pal.appendChild(b);
});
setTheme(ls('통합자료:색') || 'yellow');
const ab = btn('tg add', '+ 자료 추가'); ab.onclick = () => addForm();
$('chipbar').append(ab, el('span', 'sep'), ...PER, el('span', 'sep'), sb, nb, pb, tb, el('span', 'spacer'), ss, vb, ub, rb, gb, eb, xb, pal);
// ---------- 한꺼번에: 카드의 체크 상자로 고른다. 검색·필터를 바꿔도 고른 것은 남는다 ----------
const sel = new Set(); let shown = [];
const ba = btn('tg', '보이는 카드 모두 선택'), bn = el('span'), bi = el('input'), bo = btn('tg add', '태그 달기'), br = btn('tg', '태그 떼기'), bw = btn('tg add', '옵시디언 위키로 보내기'), bc = btn('tg', '선택 해제');
const be = btn('tg', '⇪ 내보내기·공유'), bd = btn('tg');
be.onclick = () => exportForm();
const short = (d) => (d.title || d.text.slice(0, 50) || nm(d.s)).replace(/\\s+/g, ' ').slice(0, 50);
bd.onclick = () => {  // 고른 글을 휴지통으로 (휴지통을 보고 있을 때는 되살린다). 지우기 전에 무엇을 지우는지 보여 주고 묻는다
  const n = sel.size;
  const go = () => {
    sel.forEach((k) => setNote(k, { x: trash ? 0 : 1 }));
    commit(); sel.clear(); draw();
    say(trash ? n + '건을 되살렸습니다' : n + '건을 휴지통으로 옮겼습니다 — 잘못 지웠으면 「↩ 되돌리기」');
  };
  if (trash) return go();
  const some = D.filter((d) => sel.has(key(d))).slice(0, 8).map((d) => '· ' + short(d)).join('\\n');
  ask('고른 ' + n + '건을 지울까요?\\n\\n' + some + (n > 8 ? '\\n… 외 ' + (n - 8) + '건' : '') + '\\n\\n휴지통으로 옮겨집니다. 「메모 파일로 저장」을 누르기 전에는 휴지통에서 되살릴 수 있습니다.', '🗑 삭제', go);
};
bi.placeholder = '고른 카드에 달거나 뗄 태그 (쉼표로 나눔)'; bi.setAttribute('aria-label', '고른 카드에 달거나 뗄 태그');
ba.onclick = () => { shown.forEach((d) => sel.add(key(d))); draw(); };
bc.onclick = () => { sel.clear(); draw(); };
const apply = (fn) => {  // 고른 카드의 태그를 fn 으로 고친다. 달라진 카드만 건드린다
  const t = tagsOf(bi.value);
  if (!t.length) return bi.focus();
  sel.forEach((k) => { const g = (notes[k] || {}).g || [], ng = fn(g, t); if (ng.join() !== g.join()) setNote(k, { g: ng }); });
  commit(); sel.clear(); bi.value = ''; draw();
};
bo.onclick = () => apply((g, t) => [...new Set(g.concat(t))]);   // 이미 달린 태그는 그대로 두고 더한다
br.onclick = () => apply((g, t) => g.filter((x) => !t.includes(x)));
function rename(from) {  // 태그 이름을 전체 자료에서 한 번에 바꾼다. 이미 있는 이름이면 그 태그와 합쳐진다
  const to = tagsOf(prompt("'#" + from + "' 태그의 새 이름을 적으세요.\\n이미 있는 태그 이름을 적으면 그 태그와 합쳐집니다.", from) || '')[0];
  if (!to || to === from) return;
  Object.keys(notes).forEach((k) => { const g = notes[k].g || []; if (g.includes(from)) setNote(k, { g: [...new Set(g.map((x) => (x === from ? to : x)))] }); });
  tag = to; commit(); draw();
}
bi.onkeydown = (ev) => { if (ev.key === 'Enter' && !ev.isComposing) bo.click(); };
bw.onclick = () => {  // 고른 글의 열쇠와 그 글의 메모·태그를 내려받는다 → 옵시디언 PKM/00 inbox/통합자료 에 노트로 만들어진다
  const ns = {}; sel.forEach((k) => { if (notes[k]) ns[k] = notes[k]; });
  down('tonghap_wiki_', Object.assign({ keys: [...sel], notes: ns }, pend.length ? { '+추가': pend } : {}));
  say(sel.size + '건을 옵시디언으로 보냅니다 — ' + (AUTO ? "잠시 뒤 'PKM/00 inbox/통합자료' 에 노트가 만들어지고 옵시디언이 열립니다." : "Claude 에게 '통합 정리해' 라고 하면 'PKM/00 inbox/통합자료' 에 노트가 만들어지고 옵시디언이 열립니다."));
  sel.clear(); draw();
};
$('bulk').append(ba, bn, bi, bo, br, bw, be, bd, bc);
function bulk() {
  bn.textContent = sel.size + '건 선택'; bd.textContent = trash ? '↺ 되살리기' : '🗑 삭제';
  [bn, bi, bo, br, bw, be, bd, bc].forEach((x) => { x.hidden = !sel.size; });
}
function bar() {  // 별표·메모 개수와 태그 단추를 다시 그린다
  const all = Object.values(notes).filter((n) => !n.x), tc = {}, dead = D.filter((d) => note(d).x).length;
  tb.textContent = '🗑 휴지통 ' + dead; tb.hidden = !dead && !trash; count();
  all.forEach((n) => (n.g || []).forEach((g) => { tc[g] = (tc[g] || 0) + 1; }));
  const stars = all.filter((n) => n.s).length;
  $('favcnt').textContent = stars.toLocaleString();
  sb.textContent = '★ 별표 ' + stars;
  nb.textContent = '✎ 메모 ' + all.filter((n) => n.m).length;
  const np = D.filter((d) => d.i && !note(d).x).length;
  pb.textContent = '🖼 사진 ' + np.toLocaleString(); pb.hidden = !np && !pic;
  const fresh = Object.keys(notes).filter((k) => !N0[k] || notes[k].t > N0[k].t).length;
  xb.textContent = '메모 파일로 저장' + (pend.length ? ' · 새 자료 ' + pend.length + '건' : '') + (fresh ? ' · 새로 고친 ' + fresh + '건' : ''); xb.classList.toggle('add', !!(fresh || pend.length));
  ub.textContent = '↩ 되돌리기 ' + undo.length; ub.hidden = !undo.length;
  rb.textContent = '↪ 다시 하기 ' + redo.length; rb.hidden = !redo.length;
  if (tag && !tc[tag]) tag = '';
  const box = $('tagrail'); box.textContent = '';
  Object.keys(tc).sort((a, b) => tc[b] - tc[a] || a.localeCompare(b)).forEach((g) => {
    const b = btn('', '#' + g); press(b, g === tag); b.appendChild(el('i', '', tc[g]));
    b.onclick = () => { tag = tag === g ? '' : g; bar(); draw(); };
    box.appendChild(b);
  });
  if (tag) { const r = btn('ren', "✎ '#" + tag + "' 이름 바꾸기"); r.onclick = () => rename(tag); box.appendChild(r); }
  if (!box.firstChild) box.appendChild(el('span', 'note', '카드에 태그를 달면 여기에 모입니다'));
  fit();
}
// ---------- 왼쪽 칸: 저장소 · 주제 · 일시 · 출처. 건수는 다른 조건을 다 적용한 뒤의 수 ----------
const ICON = { kakao: 'K', facebook: 'f', facebook_shared: 'f↗', bookmark: '▤', threads: '@', threads_saved: '@★', youtube: '▶', inbox: '◈', blog: '✎', instagram: '◎', x: 'X', manual: '+', claude_artifact: '◆', phone_sms: '✉', phone_call: '☎', phone_note: '✐', phone_voice: '♪', phone_callrec: '☏', phone_photo: '▣', phone: '☎', thr: '@', disk: '⛁' };
let shut = { phone: ls('통합자료:폰접기') === '1', thr: true };   // 접힌 묶음 (이 브라우저에 기억). 쓰레드는 처음에 접어 둔다
try { Object.assign(shut, JSON.parse(ls('통합자료:접기') || '{}')); } catch (e) {}
function side(c) {
  FK.forEach((f) => { if (F[f].v && !(F[f].v in c[f])) c[f][F[f].v] = 0; });   // 고른 묶음은 0건이어도 보여서 다시 끌 수 있게 한다
  if (F.d.v.length > 4 && !(F.d.v.slice(0, 4) in c.d)) c.d[F.d.v.slice(0, 4)] = 0;
  const by = (f) => Object.keys(c[f]).sort((a, b) => c[f][b] - c[f][a] || a.localeCompare(b));
  const fill = (id, f, ks, icon) => {
    const box = $(id); box.textContent = '';
    ks.forEach((k, i) => {
      const y = f === 'd' && k.length === 4, on = y ? F.d.v.slice(0, 4) === k : F[f].v === k;   // 해는 그 해의 달을 골라도 켜진 것으로 본다
      const b = btn('src' + ((f === 'd' && !y) || (f === 's' && inG(k)) ? ' sub' : '')); press(b, on); b.dataset.k = k;
      const name = el('b', '', f === 's' ? nm(k) : k);
      b.append(el('i', '', icon(k, i)), name, el('span', 'n', c[f][k].toLocaleString()));
      if (f === 's' && GRP[k]) {   // 묶음 줄: 이름 옆 화살표로 아랫줄을 접고 편다 (자판은 그 줄에서 → 펴기, ← 접기)
        const flip = () => { shut[k] = !shut[k]; ls('통합자료:접기', JSON.stringify(shut)); draw(); };
        const tw = el('span', 'tw', shut[k] ? '▸' : '▾'); tw.title = shut[k] ? '아랫줄 보이기' : '아랫줄 숨기기';
        tw.onclick = (e) => { e.stopPropagation(); flip(); };
        name.append(tw); b.setAttribute('aria-expanded', String(!shut[k]));
        b.onkeydown = (e) => { if (e.key === (shut[k] ? 'ArrowRight' : 'ArrowLeft')) { flip(); const again = [...box.children].find((x) => x.dataset.k === k); if (again) again.focus(); } };
      }
      b.onclick = (e) => {
        if (k === 'disk' && f === 's' && !c.s.disk && F.s.v !== k) return linkForm();   // 아직 연결한 것이 없으면 바로 연결 창
        F[f].v = F[f].v === k ? (f === 'd' && !y ? k.slice(0, 4) : '') : k;   // 다시 누르면 끈다 (달은 그 해로 돌아간다)
        draw();
        // 자판으로 눌렀을 때만(e.detail 0) 그 줄에 초점을 돌려준다 — 마우스로 누르면 초점 테두리(빨간 선)가 생기지 않게
        const again = [...box.children].find((x) => x.dataset.k === k); if (again && !e.detail) again.focus();
      };
      box.appendChild(b);
      if (f === 's' && k === 'disk') {   // 「연결」 줄 바로 아래: 외장하드·USB·NAS 폴더를 연결하거나 끊는 창을 여는 줄
        const lb = btn('src sub'); lb.append(el('i', '', '＋'), el('b', '', '디스크 연결 · 끊기')); lb.onclick = linkForm; box.appendChild(lb);
      }
    });
    return box;
  };
  // 스마트폰 자료(문자·통화기록·통화 녹음·음성녹음·사진·폰 메모)는 '스마트폰' 한 줄 아래에 모아 둔다. 그 줄을 누르면 폰 자료 전부, 아랫줄은 종류 하나만.
  const total = Object.values(c.s).reduce((a, b) => a + b, 0);
  Object.keys(GRP).forEach((g) => { const m = Object.keys(c.s).filter((k) => GRP[g](k)); if (m.length) c.s[g] = m.reduce((a, k) => a + c.s[k], 0); });
  c.s.disk = c.s.disk || 0;   // 「연결」 줄은 0건이어도 늘 보인다 — 거기서 디스크를 연결한다
  const sk = by('s').filter((k) => !inG(k)).flatMap((k) => (GRP[k] ? [k].concat(by('s').filter((p) => GRP[k](p) && (!shut[k] || F.s.v === p))) : [k]));   // 접어도 골라 둔 종류 한 줄은 남겨서 끌 수 있게 한다
  const sbox = fill('rs', 's', sk, (k) => ICON[k] || (k.startsWith('disk_') ? '⛁' : '·')), all = btn('src');
  press(all, !F.s.v); all.append(el('i', '', '∑'), el('b', '', '전체'), el('span', 'n', total.toLocaleString()));
  all.onclick = () => { F.s.v = ''; draw(); }; sbox.prepend(all);
  fill('rk', 'k', by('k'), (k, i) => String(i + 1).padStart(2, '0'));
  const dk = Object.keys(c.d), dl = [];
  dk.filter((k) => /^\\d{4}$/.test(k)).sort().reverse().forEach((y) => {
    dl.push(y);
    if (F.d.v.slice(0, 4) === y) dl.push(...dk.filter((k) => k.length > 4).sort().reverse());   // 고른 해의 달
  });
  if ('날짜없음' in c.d) dl.push('날짜없음');
  fill('rd', 'd', dl, (k) => (k.length > 4 ? '└' : '▪'));
  const ok = by('o'), top = ok.slice(0, 40);   // ponytail: 출처는 큰 것 40개만 단추로 둔다. 나머지는 검색창에 이름을 쳐서 찾는다
  if (F.o.v && !top.includes(F.o.v)) top.push(F.o.v);
  const obox = fill('ro', 'o', top, () => '·');
  if (ok.length > top.length) obox.appendChild(el('span', 'note', '외 ' + (ok.length - top.length).toLocaleString() + '곳 — 검색창에 이름을 치면 찾습니다'));
}
// ---------- 카드와 펼침 창 ----------
function card(d, q) {
  const k = key(d), n = note(d), a = el('article', 'pc' + (n.s ? ' used' : '')), top = el('div', 'top'), c = el('input', 'pick');
  a.dataset.k = k;
  c.type = 'checkbox'; c.checked = sel.has(k); c.setAttribute('aria-label', '선택');
  c.onclick = (ev) => ev.stopPropagation();
  c.onchange = () => { if (c.checked) sel.add(k); else sel.delete(k); bulk(); };
  top.append(c, el('span', 'badge st', nm(d.s)), el('span', 'badge', d.k), el('span', 'no', d.date ? d.date.slice(0, 10) : '날짜 없음'));
  a.appendChild(top);
  if (d.title) a.appendChild(hl(el('h3'), d.title, q));
  if (d.i) a.appendChild(img(d.i, 'ph', d.title));
  const at = q ? d.text.toLowerCase().indexOf(q) : -1;   // 검색어가 뒤쪽에 있으면 그 언저리를 보여 준다
  a.appendChild(hl(el('p', 'tx'), at > 200 ? '… ' + d.text.slice(at - 80, at + 320) : d.text.slice(0, 400), q));
  const mine = el('div', 'mine');
  (n.g || []).forEach((g) => mine.appendChild(el('span', '', '#' + g)));
  if (n.m) mine.appendChild(el('div', '', n.m));
  a.appendChild(mine);
  const meta = el('div', 'meta');
  if (d.author) meta.appendChild(el('span', '', d.author));
  meta.appendChild(el('span', '', d.text.length.toLocaleString() + '자'));
  a.appendChild(meta);
  const act = el('div', 'act'), right = el('span'), open = btn('hint', '눌러서 열기'), s = btn('fav' + (n.s ? ' on' : ''), n.s ? '★' : '☆');
  open.setAttribute('aria-label', (d.title || d.text.slice(0, 40) || nm(d.s)) + ' 열기');
  if (/^https?:/.test(d.url)) { const l = el('a', 'cp', '원문 ↗'); l.href = d.url; l.target = '_blank'; l.rel = 'noopener'; l.onclick = (ev) => ev.stopPropagation(); right.appendChild(l); }
  s.setAttribute('aria-label', '별표');
  s.onclick = (ev) => {
    ev.stopPropagation(); put(d, { s: note(d).s ? 0 : 1 });
    if (only || sort === 'star') return draw();
    const on = !!note(d).s; s.textContent = on ? '★' : '☆'; s.classList.toggle('on', on); a.classList.toggle('used', on);
  };
  right.appendChild(s); act.append(open, right); a.appendChild(act);
  a.onclick = () => detail(d);
  return a;
}
function tile(d) {  // 사진 모아보기의 한 칸. 누르면 펼침 창에서 크게 본다
  const b = btn('tile' + (sel.has(key(d)) ? ' on' : ''));
  b.setAttribute('aria-label', (d.title || '사진') + ' ' + d.date.slice(0, 10) + ' 열기');
  b.append(img(d.i, '', ''), el('span', '', d.date ? d.date.slice(0, 10) : '날짜 없음'));
  b.onclick = () => detail(d);
  return b;
}
let closeModal = () => {};
let nextPic = () => {};   // 펼침 창에서 이전(-1)·다음(+1) 사진으로. 사진이 열려 있을 때만 일한다
function detail(d) {
  const k = key(d), q = $('q').value.trim().toLowerCase(), box = $('modal');
  const ov = el('div', 'ov'), md = el('div', 'md'), mh = el('div', 'md-h'), mb = el('div', 'md-b d'), mf = el('div', 'md-f');
  const title = d.title || d.text.slice(0, 50) || nm(d.s), x = btn('x', '×'), metal = el('div', 'metal'), gi = el('input'), mi = el('textarea');
  md.setAttribute('role', 'dialog'); md.setAttribute('aria-modal', 'true'); md.setAttribute('aria-label', title);
  x.setAttribute('aria-label', '닫기'); mh.append(el('b', '', title), x);
  metal.append(el('span', 'badge st', nm(d.s)), el('span', 'badge', d.k), el('span', '', d.date ? d.date.slice(0, 16).replace('T', ' ') : '날짜 없음'));
  if (d.author) metal.appendChild(el('span', '', d.author));
  metal.appendChild(el('span', '', d.text.length.toLocaleString() + '자'));
  gi.value = (note(d).g || []).join(', '); gi.placeholder = '태그 (쉼표로 나눔 — 예: 설교, 나중에 읽기)'; gi.setAttribute('aria-label', '태그');
  mi.value = note(d).m || ''; mi.placeholder = '메모'; mi.setAttribute('aria-label', '메모');
  mb.append(metal, el('div', 'k', '태그 · 메모'), gi, mi, el('div', 'k', '내용'), hl(el('div', 'body'), d.text, q));
  if (d.i) {
    const w = el('div', 'shotw'), l = el('a'); l.href = d.i; l.target = '_blank'; l.rel = 'noopener'; l.title = '새 창에서 크게 보기'; l.appendChild(img(d.i, 'shot', title)); w.appendChild(l);
    // 이전·다음: 지금 조건에 맞는 글 가운데 그림이 있는 것끼리 넘긴다(자판은 ← →). 넘길 때도 고친 메모·태그는 저장된다
    const ps = found.filter((x) => x.i), at = ps.indexOf(d);
    nextPic = (n) => { const to = at < 0 ? null : ps[at + n]; if (to) { closeModal(); detail(to); } };
    [[-1, 'pv', '‹', '이전 사진'], [1, 'nx', '›', '다음 사진']].forEach(([n, cls, t, name]) => {
      if (at < 0 || !ps[at + n]) return;
      const b = btn('nav ' + cls, t); b.setAttribute('aria-label', name); b.title = name; b.onclick = () => nextPic(n); w.appendChild(b);
    });
    if (at >= 0 && ps.length > 1) w.appendChild(el('span', 'at', (at + 1).toLocaleString() + ' / ' + ps.length.toLocaleString()));
    metal.after(w);
  }
  // 글 속 인터넷 그림 주소: 저절로 불러오지 않는다(이 화면은 밖과 통신하지 않는다) — 사용자가 단추를 눌렀을 때만 그 한 장을 가져온다
  const far = [...new Set(d.text.match(/https?:\\/\\/[^\\s)\\]"'<>]+\\.(?:jpe?g|png|gif|webp)(?:\\?[^\\s)\\]"'<>]*)?/gi) || [])].slice(0, 12);
  if (far.length) {
    const more = el('div', 'more');
    far.forEach((u, n) => { const b = btn('tg', '🖼 그림 ' + (n + 1) + ' 보기'); b.title = u; b.onclick = () => more.before(img(u, 'shot', '')) || b.remove(); more.appendChild(b); });
    mb.appendChild(more);
  }
  const keep = () => {  // 고친 메모·태그가 있을 때만 저장한다
    const m = mi.value.trim(), g = tagsOf(gi.value), o = note(d);
    if (m === (o.m || '') && g.join() === (o.g || []).join()) return false;
    put(d, { m, g }); return true;
  };
  closeModal = () => {  // 닫으면 고친 메모·태그가 저장된다 (잘못 닫아 잃지 않게. 되돌리기로 물릴 수 있다)
    const saved = keep();
    box.hidden = true; box.textContent = ''; document.body.style.overflow = ''; closeModal = () => {}; nextPic = () => {};
    draw();
    if (saved) say('메모·태그를 저장했습니다');
    const back = [...$('list').children].find((a) => a.dataset.k === k);
    if (back) back.querySelector('.hint').focus({ preventScroll: true });
  };
  const ok = btn('btn pri', '저장하고 닫기'), fav = btn('btn'), pick = btn('btn');
  const face = () => { fav.textContent = note(d).s ? '★ 별표 풀기' : '☆ 별표'; pick.textContent = sel.has(k) ? '✓ 선택됨 (빼기)' : '☐ 선택에 담기'; };
  ok.onclick = x.onclick = () => closeModal();
  fav.onclick = () => { put(d, { s: note(d).s ? 0 : 1 }); face(); };
  pick.onclick = () => { if (sel.has(k)) sel.delete(k); else sel.add(k); bulk(); face(); };
  face(); mf.append(ok, fav);
  if (/^https?:/.test(d.url)) { const l = el('a', 'btn', '원문 열기 ↗'); l.href = d.url; l.target = '_blank'; l.rel = 'noopener'; mf.appendChild(l); }
  if (d.file) { const l = el('a', 'btn', '◈ 노트 열기'); l.href = 'obsidian://open?path=' + encodeURIComponent(d.file); mf.appendChild(l); }
  if (d.url) { const u = btn('btn', '주소 복사'); u.onclick = () => copy(d.url).then(() => say('주소를 복사했습니다'), () => say('복사가 막혔습니다')); mf.appendChild(u); }
  if (pend.includes(d)) {  // 아직 자료 파일에 안 들어간, 방금 적어 넣은 글만 지울 수 있다
    const del = btn('btn danger', '추가 취소');
    del.onclick = () => {
      gi.value = mi.value = ''; if (notes[k]) put(d, { m: '', g: [], s: 0 });
      pend.splice(pend.indexOf(d), 1); D.splice(D.indexOf(d), 1); sel.delete(k); keepPend(); count(); bar(); closeModal(); say('추가한 자료를 지웠습니다');
    };
    mf.appendChild(del);
  } else {  // 자료 파일에 든 글: 휴지통으로 보낸다 (휴지통에서 연 글은 되살린다)
    const gone = !!note(d).x, del = btn('btn danger', gone ? '↺ 되살리기' : '🗑 삭제');
    del.onclick = () => {
      const go = () => {
        keep(); put(d, { x: gone ? 0 : 1 }); sel.delete(k); closeModal();
        say(gone ? '되살렸습니다' : '휴지통으로 옮겼습니다 — 잘못 지웠으면 「↩ 되돌리기」');
      };
      if (gone) return go();
      ask("이 자료를 지울까요?\\n\\n· " + short(d) + "\\n\\n휴지통으로 옮겨집니다. 「메모 파일로 저장」을 누르기 전에는 휴지통에서 되살릴 수 있습니다.", '🗑 삭제', go);
    };
    mf.appendChild(del);
  }
  mf.append(el('span', 'spacer'), pick);
  ov.onclick = (ev) => { if (ev.target === ov) closeModal(); };
  md.append(mh, mb, mf); ov.appendChild(md); box.textContent = ''; box.appendChild(ov); box.hidden = false;
  document.body.style.overflow = 'hidden'; x.focus();
}
function addForm() {
  const box = $('modal'), ov = el('div', 'ov'), md = el('div', 'md'), mh = el('div', 'md-h'), mb = el('div', 'md-b d'), mf = el('div', 'md-f'), x = btn('x', '×'), f = {};
  md.setAttribute('role', 'dialog'); md.setAttribute('aria-modal', 'true'); md.setAttribute('aria-label', '자료 추가');
  x.setAttribute('aria-label', '닫기'); mh.append(el('b', '', '+ 자료 추가'), x);
  [['title', '제목', 'input'], ['url', '주소 (https://…)', 'input'], ['author', '글쓴이 · 출처', 'input'], ['text', '내용', 'textarea'], ['g', '태그 (쉼표로 나눔)', 'input'], ['m', '메모 — 왜 저장하는지', 'textarea']].forEach(([k, name, t]) => {
    f[k] = el(t); f[k].setAttribute('aria-label', name); mb.append(el('div', 'k', name), f[k]);
  });
  f.text.style.minHeight = '160px';
  const v = (k) => f[k].value.trim(), ok = btn('btn pri', '추가'), no = btn('btn', '취소');
  let done = false;
  closeModal = (sure) => {
    if (!done && sure !== true && Object.keys(f).some(v)) return ask('적던 내용을 버릴까요?', '버리기', () => closeModal(true));
    box.hidden = true; box.textContent = ''; document.body.style.overflow = ''; closeModal = () => {}; ab.focus();
  };
  ok.onclick = () => {
    const url = v('url');
    if (!(v('title') || v('text') || url)) return f.title.focus();   // 셋 다 비면 넣을 것이 없다
    let host = ''; try { host = new URL(url).hostname.replace('www.', ''); } catch (e) {}
    const d = { platform: 'manual', id: 'm' + Date.now().toString(36), author: v('author'), url, date: new Date().toLocaleString('sv').replace(' ', 'T'),
      title: v('title'), text: v('text') || url, k: '기타', o: v('author') || host || '알 수 없음', s: 'manual' };   // 주제(k)는 다음 "통합 정리해" 때 매겨진다
    pend.push(d); D.unshift(d); keepPend();
    if (v('m') || v('g')) setNote(key(d), { m: v('m'), g: tagsOf(v('g')) });
    done = true; closeModal(); count(); commit(); draw();
    say("자료를 추가했습니다 — '메모 파일로 저장' 을 누르면 자료 파일에 들어갑니다. " + NEXT);
  };
  no.onclick = x.onclick = () => closeModal();
  mf.append(ok, no); md.append(mh, mb, mf); ov.appendChild(md); box.textContent = ''; box.appendChild(ov); box.hidden = false;
  document.body.style.overflow = 'hidden'; f.title.focus();
}
// ---------- 내보내기 · 공유: 고른 글 / 조건에 맞는 글 / 전체를 여러 형식의 파일로, 원하는 곳에 ----------
let found = [];   // 지금 조건에 맞는 글 전부 (화면에는 한 쪽 PP 건만 그린다)
let pg = 0, sig = '';   // 지금 쪽(0부터) · 조건 지문 — 검색·필터·정렬이 바뀌면 1쪽으로 돌아간다
function pager(pages) {  // 목록 아래 쪽 번호: ‹ 이전 · 1 … 앞뒤 2쪽 … 끝 · 다음 ›
  const p = $('pager'); p.textContent = ''; p.hidden = pages < 2; if (pages < 2) return;
  const add = (text, n, name) => {
    const b = btn('tg', text); b.disabled = n < 0 || n >= pages; b.setAttribute('aria-label', name || (n + 1) + '쪽');
    if (n === pg && !name) { b.setAttribute('aria-pressed', 'true'); b.setAttribute('aria-current', 'page'); }
    b.onclick = (e) => { pg = n; draw(); $('hn').parentNode.scrollIntoView(); if (!e.detail) $('pager').querySelector('[aria-current]').focus({ preventScroll: true }); };   // 목록 머리로 올라간다. 초점은 자판으로 눌렀을 때만 되돌린다
    p.appendChild(b);
  };
  add('‹ 이전', pg - 1, '이전 쪽');
  let last = -1;
  [...new Set([0, pg - 2, pg - 1, pg, pg + 1, pg + 2, pages - 1])].filter((n) => n >= 0 && n < pages).forEach((n) => {
    if (n - last > 1) p.appendChild(el('span', '', '…'));
    add((n + 1).toLocaleString(), n); last = n;
  });
  add('다음 ›', pg + 1, '다음 쪽');
}
const COLS = [['저장소', (d) => nm(d.s)], ['주제', (d) => d.k], ['날짜', (d) => d.date], ['제목', (d) => d.title], ['글쓴이', (d) => d.author], ['출처', (d) => d.o], ['주소', (d) => d.url],
  ['내용', (d) => d.text], ['태그', (d) => (note(d).g || []).join(', ')], ['메모', (d) => note(d).m || ''], ['별표', (d) => (note(d).s ? '★' : '')]];
// 표 한 칸. = + - @ 로 시작하는 남의 글이 엑셀에서 수식으로 돌지 않게 앞에 ' 를 붙인다
const cell = (v) => { v = String(v == null ? '' : v); if (/^[=+@-]/.test(v)) v = "'" + v; return '"' + v.replace(/"/g, '""') + '"'; };
const esc = (v) => String(v).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const info = (d) => [nm(d.s), d.date.slice(0, 16).replace('T', ' '), d.author, d.o !== d.author && d.o].filter(Boolean).join(' · ');
const mine = (d) => { const n = note(d); return [(n.g || []).length ? '태그: ' + n.g.map((g) => '#' + g).join(' ') : '', n.m ? '메모: ' + n.m : ''].filter(Boolean); };
const FMT = {  // 형식: [이름, 종류, 글 목록 → 파일 내용]
  csv: ['엑셀 · 넘버스 표 (.csv)', 'text/csv', (r) => '\\ufeff' + [COLS.map((c) => cell(c[0])).join(',')].concat(r.map((d) => COLS.map((c) => cell(c[1](d))).join(','))).join('\\r\\n')],
  md: ['마크다운 — 옵시디언 · 노션 (.md)', 'text/markdown', (r) => r.map((d) => ['## ' + short(d), '', '- ' + info(d)].concat(d.url ? ['- ' + d.url] : [], mine(d).map((x) => '- ' + x), ['', d.text, '']).join('\\n')).join('\\n---\\n\\n')],
  txt: ['글 (.txt)', 'text/plain', (r) => r.map((d) => [short(d), info(d)].concat(d.url ? [d.url] : [], mine(d), ['', d.text]).join('\\n')).join('\\n\\n' + '─'.repeat(30) + '\\n\\n')],
  html: ['웹 문서 — 보기 · 인쇄용 (.html)', 'text/html', (r) => '<!doctype html><meta charset="utf-8"><title>KBG-통합자료 ' + r.length + '건</title>'
    + '<style>body{font:15px/1.7 -apple-system,"Apple SD Gothic Neo",sans-serif;max-width:760px;margin:32px auto;padding:0 18px;color:#111}h2{font-size:18px;margin:28px 0 4px}small{color:#666}p{white-space:pre-wrap;overflow-wrap:anywhere}article{border-bottom:1px solid #ddd;padding-bottom:14px;break-inside:avoid-page}</style>'
    + r.map((d) => '<article><h2>' + esc(short(d)) + '</h2><small>' + esc(info(d)) + (/^https?:/.test(d.url) ? ' · <a href="' + esc(d.url) + '">원문</a>' : '') + '</small>'
      + mine(d).map((x) => '<br><small>' + esc(x) + '</small>').join('') + '<p>' + esc(d.text) + '</p></article>').join('')],
  json: ['자료 그대로 — 다른 프로그램용 (.json)', 'application/json', (r) => JSON.stringify(r.map((d) => Object.assign({}, d, { 태그: note(d).g || [], 메모: note(d).m || '', 별표: !!note(d).s })), null, 1)],
};
function exportForm() {
  const box = $('modal'), ov = el('div', 'ov'), md = el('div', 'md'), mh = el('div', 'md-h'), mb = el('div', 'md-b d'), mf = el('div', 'md-f'), x = btn('x', '×');
  md.setAttribute('role', 'dialog'); md.setAttribute('aria-modal', 'true'); md.setAttribute('aria-label', '내보내기 · 공유');
  x.setAttribute('aria-label', '닫기'); mh.append(el('b', '', '⇪ 내보내기 · 공유'), x);
  const live = D.filter((d) => !note(d).x);
  const SETS = [['고른 카드', live.filter((d) => sel.has(key(d)))], [trash ? '휴지통에 있는 글' : '지금 조건에 맞는 글', found], ['전체 자료', live]];
  const ws = el('select'), fs = el('select'), warn = el('div', 'warn'), how = el('div', 'note');
  SETS.forEach(([t, r], i) => { const o = el('option', '', t + ' — ' + r.length.toLocaleString() + '건'); o.value = i; o.disabled = !r.length; ws.appendChild(o); });
  ws.value = sel.size ? 0 : found.length ? 1 : 2; ws.setAttribute('aria-label', '무엇을 내보낼까');
  Object.keys(FMT).forEach((k) => { const o = el('option', '', FMT[k][0]); o.value = k; fs.appendChild(o); });
  fs.value = FMT[ls('통합자료:형식')] ? ls('통합자료:형식') : 'csv'; fs.setAttribute('aria-label', '파일 형식');
  const rows = () => SETS[ws.value][1];
  const face = () => {
    const p = rows().filter((d) => /^(kakao|phone_)/.test(d.platform)).length;
    warn.textContent = (p ? '⚠ 이 안에 카톡·폰 자료 ' + p.toLocaleString() + '건(다른 사람의 대화·연락처·통화 기록)이 들어 있습니다. ' : '다른 사람이 쓴 글이 들어 있습니다. ') + '밖으로 보내기 전에 받는 사람과 보낼 곳을 확인하세요.';
  };
  ws.onchange = face; face();
  how.textContent = '「저장할 곳 고르기」를 누르면 저장 창이 뜹니다 — 왼쪽 목록에서 맥북 폴더 · 외장 디스크 · NAS(Home) · Google Drive 를 고르면 그곳에 바로 저장됩니다. (사파리에서는 다운로드 폴더에 저장됩니다.)';
  mb.append(el('div', 'k', '무엇을'), ws, el('div', 'k', '파일 형식'), fs, warn, how);
  closeModal = () => { box.hidden = true; box.textContent = ''; document.body.style.overflow = ''; closeModal = () => {}; };
  const file = (k) => { k = k || fs.value; ls('통합자료:형식', fs.value); return ['KBG-통합자료_' + new Date().toLocaleDateString('sv') + '_' + rows().length + '건.' + k, new Blob([FMT[k][2](rows())], { type: FMT[k][1] + ';charset=utf-8' })]; };
  const text = () => FMT.txt[2](rows());
  const sv = btn('btn pri', '저장할 곳 고르기…'), cp = btn('btn', '글로 복사'), ml = btn('btn', '메일로'), pr = btn('btn', '인쇄 · PDF'), sh = btn('btn', '공유…');
  sv.onclick = async () => {
    const [name, blob] = file();
    if (!window.showSaveFilePicker) { dl(name, blob); return say('다운로드 폴더에 저장했습니다 — ' + name); }
    try { const h = await showSaveFilePicker({ suggestedName: name }), w = await h.createWritable(); await w.write(blob); await w.close(); say('저장했습니다 — ' + h.name); }
    catch (e) { if (e.name !== 'AbortError') { dl(name, blob); say('고른 곳에 쓰지 못해 다운로드 폴더에 저장했습니다 — ' + name); } }
  };
  cp.onclick = () => copy(text()).then(() => say(rows().length + '건을 복사했습니다 — 카톡·메모·문서에 붙여넣으세요'), () => say('복사가 막혔습니다'));
  ml.onclick = () => {  // 받는 사람은 메일 창에서 직접 적는다. 긴 글은 주소에 다 못 실어 복사해 두고 붙여넣게 한다
    const t = text(), long = t.length > 1500, go = () => { location.href = 'mailto:?subject=' + encodeURIComponent('KBG-통합자료 ' + rows().length + '건') + '&body=' + encodeURIComponent(long ? '(내용은 복사해 두었습니다 — 여기에 붙여넣으세요)' : t); };
    if (!long) return go();
    copy(t).then(() => { say('내용이 길어 복사해 두었습니다 — 메일 본문에 붙여넣으세요'); go(); }, () => say('복사가 막혔습니다 — 「저장할 곳 고르기」로 파일을 만들어 붙이세요'));
  };
  pr.onclick = () => {  // 인쇄 창에서 'PDF로 저장' 을 고르면 PDF 가 된다
    const tail = '<scr' + 'ipt>addEventListener("load", () => print())</scr' + 'ipt>';
    if (!window.open(URL.createObjectURL(new Blob([FMT.html[2](rows()) + tail], { type: 'text/html;charset=utf-8' })))) say('새 창이 막혔습니다 — 팝업을 허용해 주세요');
  };
  sh.onclick = () => {  // 맥의 공유 창(에어드롭·메시지·메일…). 파일을 못 받는 브라우저는 글로 넘긴다
    const [name, blob] = file(), f = new File([blob], name, { type: blob.type });
    navigator.share(navigator.canShare && navigator.canShare({ files: [f] }) ? { files: [f], title: name } : { title: name, text: text().slice(0, 20000) }).catch(() => {});
  };
  x.onclick = () => closeModal();
  mf.append(sv, cp, ml, pr); if (navigator.share) mf.appendChild(sh);
  ov.onclick = (ev) => { if (ev.target === ov) closeModal(); };
  md.append(mh, mb, mf); ov.appendChild(md); box.textContent = ''; box.appendChild(ov); box.hidden = false;
  document.body.style.overflow = 'hidden'; sv.focus();
}
function draw() {
  const q = $('q').value.trim().toLowerCase();
  const cut = days ? new Date(Date.now() - days * 864e5).toLocaleDateString('sv') : '';   // 'sv' 는 2026-11-14 꼴로 적는다
  const c = { s: {}, k: {}, d: {}, o: {} }, hit = [], add = (f, k) => { c[f][k] = (c[f][k] || 0) + 1; };
  D.forEach((d) => {
    const n = note(d);
    if (!!n.x !== trash) return;   // 지운 글은 휴지통에서만 보인다
    if (!((!cut || d.date.slice(0, 10) >= cut) && (!only || n.s) && (!onlyN || n.m) && (!pic || d.i) && (!tag || (n.g || []).includes(tag))
      && (!q || (d.title + '\\n' + d.author + '\\n' + d.o + '\\n' + d.text + '\\n' + (n.m || '') + '\\n#' + (n.g || []).join(' #')).toLowerCase().includes(q)))) return;
    const bad = FK.filter((f) => !inF(f, d));
    if (bad.length > 1) return;
    if (!bad.length) hit.push(d);
    // 왼쪽 칸 건수: 그 칸에서 고른 것만 빼고 나머지 조건을 다 맞춘 글을 센다 (그래야 다른 묶음으로 갈아탈 때의 건수가 보인다)
    (bad.length ? bad : FK).forEach((f) => {
      const k = F[f].key(d);
      if (f !== 'd') return add(f, k);
      add('d', k.slice(0, 4));                                                    // 해 ('날짜없음' 도 네 글자)
      if (k.length > 4 && F.d.v && k.startsWith(F.d.v.slice(0, 4))) add('d', k);   // 고른 해의 달
    });
  });
  side(c);
  PER.forEach((b) => press(b, +b.dataset.n === days)); press(sb, only); press(nb, onlyN); press(pb, pic); press(tb, trash);
  vb.textContent = view === 'list' ? '▦ 카드' : '☰ 목록';
  const names = [trash && '🗑 휴지통', dname, F.s.v && nm(F.s.v), F.k.v, F.d.v, F.o.v, tag && '#' + tag, only && '★ 별표', onlyN && '✎ 메모', pic && '🖼 사진', q && '"' + q + '"'].filter(Boolean);
  $('hn').textContent = hit.length.toLocaleString() + '건';
  $('ht').textContent = names.length ? names.join(' · ') : '전체 자료';
  $('hr').hidden = !names.length;
  let out = hit;   // D 는 최신순으로 들어 있다 (날짜 없는 글은 맨 뒤)
  if (sort === 'old') out = hit.filter((d) => d.date).reverse().concat(hit.filter((d) => !d.date));
  if (sort === 'star') out = hit.filter((d) => note(d).s).concat(hit.filter((d) => !note(d).s));
  const now = [q, days, only, onlyN, pic, trash, tag, sort].concat(FK.map((f) => F[f].v)).join('|');
  if (now !== sig) { sig = now; pg = 0; }
  const per = pic ? 500 : PP;   // 사진 모아보기는 한눈에 보도록 한 쪽에 500장
  const pages = Math.ceil(out.length / per) || 1; pg = Math.min(pg, pages - 1);   // 마지막 쪽을 다 지우면 앞 쪽으로 당긴다
  $('hs').textContent = pages > 1 ? pages.toLocaleString() + '쪽 가운데 ' + (pg + 1).toLocaleString() + '쪽 — 한 쪽에 ' + per + '건' : '';
  found = out; shown = out.slice(pg * per, pg * per + per);
  const list = $('list'); list.textContent = ''; list.className = 'grid' + (pic ? ' pics' : view === 'list' ? ' lv' : '');
  shown.forEach((d) => list.appendChild(pic ? tile(d) : card(d, q)));
  if (!shown.length) list.appendChild(el('div', 'empty', trash ? '휴지통이 비었습니다 — 「필터 모두 풀기」를 누르면 돌아갑니다.' : '조건에 맞는 자료가 없습니다 — 검색어를 줄이거나 「필터 모두 풀기」를 누르세요.'));
  pager(pages); bulk(); fit();
}
$('hr').onclick = () => { FK.forEach((f) => { F[f].v = ''; }); tag = ''; only = onlyN = pic = trash = false; days = 0; dname = ''; $('q').value = ''; bar(); draw(); };
// 상단바·단추 줄 높이를 재서 그 아래에 붙는 것들(단추 줄, 왼쪽 칸, 한꺼번에 줄)의 자리를 맞춘다
function fit() { const r = document.documentElement.style; r.setProperty('--bh', $('bar').offsetHeight + 'px'); r.setProperty('--th', $('tools').offsetHeight + 'px'); }
addEventListener('resize', fit);
let qt;
$('q').oninput = () => { clearTimeout(qt); qt = setTimeout(draw, 120); };
document.addEventListener('keydown', (ev) => {
  if (document.querySelector('dialog[open]')) return;   // 확인 창이 떠 있으면 Esc 는 그 창만 닫는다
  if (ev.key === 'Escape' && !$('modal').hidden) return closeModal();
  if (/^Arrow(Left|Right)$/.test(ev.key) && !$('modal').hidden && !/INPUT|TEXTAREA|SELECT/.test(ev.target.tagName)) return nextPic(ev.key === 'ArrowLeft' ? -1 : 1);
  if (ev.key === '/' && $('modal').hidden && !/INPUT|TEXTAREA|SELECT/.test(ev.target.tagName)) { ev.preventDefault(); $('q').focus(); }
});
function count() {  // 상단의 자료 수·저장소 수 (자료를 추가하거나 지울 때 다시 센다. 휴지통의 글은 세지 않는다)
  const live = D.filter((d) => !note(d).x);
  $('cnt').textContent = live.length.toLocaleString();
  $('chipS').textContent = new Set(live.map((d) => d.s)).size + '곳 저장소';
  $('chipN').textContent = live.length.toLocaleString() + '건 자료';
}
$('chipA').textContent = AUTO ? '⟳ 자동 수집 켜짐' : '자동 수집 꺼짐';
// ---------- 연결: 외장하드 · USB · NAS 폴더 ----------
// 화면은 디스크를 직접 읽지 못한다. 여기서는 부탁 파일만 내려놓고, 읽는 일은 자동 수집(통합정리.py)이 한다. 목록은 화면을 만들 때 붙어 있던 디스크다.
function linkForm() {
  const dg = el('dialog', 'ask link'), list = el('ul'), row = el('div'), no = btn('btn', '닫기');
  const send = (what, p) => {
    if (!AUTO) return say("자동 수집이 꺼져 있어 여기서 바로 연결할 수 없습니다 — Claude 에게 '외장하드 연결해' 라고 하세요.");
    wantAt = Date.now(); down('tonghap_now_', { [what]: p }); dg.close();
    say(what === 'disk' ? '연결을 시작했습니다 — 파일이 많으면 몇 분 걸립니다. 끝나면 화면이 저절로 바뀝니다' : '연결을 끊는 중입니다 — 잠시 뒤 화면이 저절로 바뀝니다');
  };
  const line = (label, p, sub) => {
    const li = el('li', sub ? 'sub' : ''), on = DISKS.on.includes(p), b = btn('tg', on ? '끊기' : '연결');
    press(b, on); b.setAttribute('aria-label', label + (on ? ' 연결 끊기' : ' 연결')); b.onclick = () => send(on ? 'undisk' : 'disk', p);
    li.append(el('span', '', label), b); list.appendChild(li);
  };
  const tail = (p) => p.split('/').pop().normalize('NFC');
  DISKS.v.forEach((v) => { line('⛁ ' + tail(v.p) + ' — 통째로', v.p); v.sub.forEach((s) => line(s.normalize('NFC'), v.p + '/' + s, true)); });
  DISKS.on.filter((p) => !DISKS.v.some((v) => p === v.p || p.startsWith(v.p + '/'))).forEach((p) => line(p.split('/').slice(2).join('/').normalize('NFC') + ' — 지금 붙어 있지 않음', p));
  if (!list.firstChild) list.appendChild(el('li', '', '지금 붙어 있는 외장 디스크가 없습니다. 꽂고 1분쯤 뒤에 다시 열어 보세요.'));
  no.onclick = () => dg.close(); dg.onclose = () => dg.remove(); row.appendChild(no);
  dg.append(el('b', '', '⛁ 연결 — 외장하드 · USB · NAS'), el('p', '', '연결하면 그 폴더의 문서·사진·소리·영상 파일이 이름·날짜·크기로 카드가 됩니다(내용은 읽지 않습니다). 연결 하나에 20,000개까지 — 큰 디스크는 통째로 말고 폴더를 골라 연결하세요.'), list, row);
  document.body.appendChild(dg); dg.showModal();
}
// ---------- 새 판 알아채기 · 지금 업데이트 ----------
// 통합정리.py 는 화면을 다시 만들 때마다 옆 파일 tonghap_build.js 에 onBuild("판 번호", 시각) 한 줄을 적는다. 15초마다 그 파일을 읽어 본다.
// 판이 바뀌었으면: 아무것도 고르거나 거르지 않은 상태에서는 스스로 새로 고치고, 무언가 하던 중이면 상단에 알림만 띄운다(하던 일을 날리지 않게).
let wantAt = 0;   // 「지금 업데이트」를 누른 시각
window.onBuild = (b, t) => {
  if (b === BUILD) { if (wantAt && t > wantAt) { wantAt = 0; say('새로 들어온 자료가 없습니다 — 이미 최신입니다'); } return; }
  if (wantAt || ($('modal').hidden && !sel.size && $('hr').hidden)) { closeModal(); return location.reload(); }
  const c = $('chipA');
  if (!c.onclick) say('새 자료가 들어왔습니다 — 상단의 「새로 고침」 표시를 누르면 보입니다');
  c.textContent = '⟳ 새 자료가 들어왔습니다 — 눌러서 새로 고침'; c.style.cursor = 'pointer'; c.onclick = () => { closeModal(); location.reload(); };
};
setInterval(() => { const s = el('script'); s.src = 'tonghap_build.js?' + Date.now(); s.onload = s.onerror = () => s.remove(); document.head.appendChild(s); }, 15000);
gb.onclick = () => {  // 빈 신호 파일을 내려받는다 → 자동 수집이 그것을 보고 바로 한 번 정리한다 → 판이 바뀌면 위에서 새로 고친다
  if (!AUTO) return say("자동 수집이 꺼져 있어 여기서 바로 업데이트할 수 없습니다 — Claude 에게 '자동 수집 켜' 또는 '통합 정리해' 라고 하세요.");
  wantAt = Date.now(); down('tonghap_now_', {});
  say('업데이트를 시작했습니다 — 30초쯤 뒤 화면이 저절로 바뀝니다');
  setTimeout(() => { if (wantAt) say("아직 정리 중이거나 자동 수집이 멈춰 있습니다 — 조금 더 기다려도 그대로면 Claude 에게 '통합 정리해' 라고 하세요."); }, 90000);
};
if (matchMedia('(max-width:960px)').matches) document.querySelectorAll('.rail details').forEach((x, i) => { x.open = !i; });   // 좁은 화면은 저장소만 펼쳐 둔다
bar(); draw();
</script>
"""


def save(store, notes):
    rows = sorted(store.values(), key=lambda r: r["date"], reverse=True)   # 날짜 없는 글은 맨 뒤
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    dates = sorted(r["date"][:10] for r in rows if r["date"])
    sub = f"{len(rows):,}건 · {dates[0]} ~ {dates[-1]}" if dates else f"{len(rows):,}건"
    # 보기 화면용으로만 주제(k)·출처(o)·저장소(s)를 붙인다. 통합자료.jsonl 에는 넣지 않는다 (규칙을 고치면 다음 실행 때 다시 매겨진다)
    live = {r["id"] for r in rows if r["platform"] == "phone_photo"}
    for f in PICS.glob("*.jpg"):                     # 자료에서 빠진(지운) 사진의 미리보기 사본은 같이 치운다. 다시 필요하면 --photos 로 만든다
        if f.stem not in live:
            f.unlink()
    # 그림이 있는 글에는 그 주소(i)도 붙인다
    data = json.dumps([dict(r, k=topic(r), o=origin(r), s=shelf(r), **({"i": pic(r)} if pic(r) else {})) for r in rows],
                      ensure_ascii=False).replace("</", "<\\/")
    parts = {"SUB": sub, "DATA": data, "NOTES": json.dumps(notes, ensure_ascii=False).replace("</", "<\\/"),
             "NAME": json.dumps(LABEL, ensure_ascii=False), "AUTO": "true" if AGENT.exists() else "false"}
    on = json.loads(LINKS.read_text(encoding="utf-8")).get("disk", []) if LINKS.exists() else []
    parts["DISKS"] = json.dumps({"v": volumes(), "on": on}, ensure_ascii=False).replace("</", "<\\/")   # 연결 창: 붙어 있는 디스크 · 이미 연결한 폴더
    # 판 번호: 내용이 같으면 번호도 같다 — 열려 있는 화면은 번호가 달라졌을 때만 스스로 새로 고친다
    build = hashlib.sha1((PAGE + data + parts["NOTES"] + parts["AUTO"] + parts["DISKS"]).encode("utf-8")).hexdigest()[:12]
    parts["BUILD"] = json.dumps(build)
    VIEW.write_text(re.sub(r"__(SUB|DATA|NOTES|NAME|AUTO|BUILD|DISKS)__", lambda m: parts[m.group(1)], PAGE), encoding="utf-8")
    BUILD_JS.write_text(f'onBuild("{build}", {int(time.time() * 1000)})\n', encoding="utf-8")   # 화면을 다 쓴 뒤에 적는다
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--youtube", nargs="+", default=[], metavar="주소")
    ap.add_argument("--limit", type=int, default=30, help="유튜브에서 가져올 최근 영상 수 (기본 30)")
    ap.add_argument("--subs", action="store_true", help="유튜브 자막(한국어→영어)도 받는다")
    ap.add_argument("--blog", nargs="+", default=[], metavar="주소")
    ap.add_argument("--full", action="store_true", help="네이버 블로그 글 전문까지 읽는다")
    ap.add_argument("--kakao", nargs="*", default=None, metavar="파일·폴더")
    ap.add_argument("--inbox", nargs="*", default=None, metavar="폴더", help="옵시디언 inbox 노트")
    ap.add_argument("--bookmarks", action="store_true", help="브라우저 북마크")
    ap.add_argument("--artifacts", action="store_true", help="발행한 Claude 아티팩트")
    ap.add_argument("--all", action="store_true", help="북마클릿 + 카톡 + inbox + 북마크 + 아티팩트를 한 번에")
    ap.add_argument("--phone", action="store_true", help="폰 자료(문자·통화·메모·녹음·사진)를 더한다")
    ap.add_argument("--phone-check", action="store_true", help="폰 자료가 얼마나 있는지만 본다 (넣지 않는다)")
    ap.add_argument("--photos", action="store_true", help="이미 들어온 사진 앱 사진의 미리보기를 만든다 (새 자료는 읽지 않는다)")
    ap.add_argument("--disk", nargs="*", default=None, metavar="폴더", help="외장하드·USB·NAS 폴더를 연결한다 (폴더 없이 쓰면 연결해 둔 곳만 다시 읽는다)")
    ap.add_argument("--undisk", nargs="+", default=[], metavar="폴더", help="연결을 끊고 그 자료를 뺀다")
    ap.add_argument("--import", dest="imports", nargs="+", default=[], metavar="파일")
    ap.add_argument("--platform", default="", help="--import 자료의 출처 이름 (예: facebook)")
    ap.add_argument("--author", default="", help="--import 자료에 글쓴이가 없을 때 넣을 이름")
    ap.add_argument("--open", action="store_true", help="끝나고 화면을 연다")
    ap.add_argument("--auto", action="store_true", help="지켜보는 곳에 바뀐 것이 있을 때만 --all 처럼 정리한다 (자동 수집이 부르는 방식)")
    ap.add_argument("--auto-on", action="store_true", help="자동 수집 켜기: 출처에 자료가 생기면 저절로 정리한다")
    ap.add_argument("--auto-off", action="store_true", help="자동 수집 끄기")
    ap.add_argument("--selfcheck", action="store_true")
    a = ap.parse_args()
    if a.selfcheck:
        return selfcheck()
    if a.phone_check:
        from_phone()
        return print("\n점검만 했습니다 — 통합자료에는 넣지 않았습니다. 넣으려면 --phone")

    # 한 번에 하나만 돈다 (자동 수집과 "통합 정리해" 가 겹치면 자료 파일이 꼬인다). 자동 쪽은 기다리지 않고 물러난다.
    lock = open(HERE / ".lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | (fcntl.LOCK_NB if a.auto else 0))
    except BlockingIOError:
        return
    if a.auto_on or a.auto_off:
        agent(a.auto_on)
    seen = None
    # 연결된 출처: 한 번 가져온 블로그·유튜브 주소를 기억해 두고, 새 글·새 영상이 올라왔는지 다시 본다
    links = json.loads(LINKS.read_text(encoding="utf-8")) if LINKS.exists() else {"blog": [], "youtube": [], "t": 0}
    for k, urls in (("blog", a.blog), ("youtube", a.youtube)):
        links[k] += [u for u in urls if u not in links[k]]
    # 디스크 연결·끊기: 명령줄, 또는 보기 화면의 연결 창이 내려놓은 부탁 파일(tonghap_now_*: {"disk": 폴더} · {"undisk": 폴더})
    for f in DL.glob("tonghap_now_*.json"):
        try:
            ask = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for k in ("disk", "undisk") if isinstance(ask, dict) else ():
            p = ask.get(k)
            if isinstance(p, str) and Path(p).resolve().is_relative_to(VOLS) and Path(p).resolve() != VOLS:   # 내려받은 파일의 부탁은 /Volumes 아래 폴더만 받는다
                setattr(a, k, (getattr(a, k) or []) + [p])
    links.setdefault("disk", [])
    for p in a.disk or []:
        p = str(Path(p).expanduser())
        if not Path(p).is_dir():
            print(f"  ⚠ 연결 못 함 — 폴더가 없음: {p}")
        elif p not in links["disk"]:
            links["disk"].append(p)
    links["disk"] = [p for p in links["disk"] if p not in a.undisk]
    if a.auto or a.auto_on or a.auto_off or a.all:
        a.all = True
        seen = stamp()
        # 다시 볼 때: 사람이 돌렸을 때 · 화면의 「지금 업데이트」(tonghap_now_*) · 자동은 6시간에 한 번 (인터넷을 쓰는 일이라 자주 하지 않는다)
        due = bool(links["blog"] or links["youtube"]) and (not a.auto or any(DL.glob("tonghap_now_*.json")) or time.time() - links["t"] > 6 * 3600)
        if a.auto and not due and STATE.exists() and seen == json.loads(STATE.read_text(encoding="utf-8")):
            return                                   # 바뀐 것 없음 — 아무것도 하지 않는다
        if due:
            a.blog, a.youtube, links["t"] = list(links["blog"]), list(links["youtube"]), time.time()
    if links["blog"] or links["youtube"] or links["disk"] or LINKS.exists():
        LINKS.write_text(json.dumps(links, ensure_ascii=False, indent=1), encoding="utf-8")
    if a.auto:
        print(f"\n── 자동 수집 {datetime.now():%Y-%m-%d %H:%M} ──")

    store = {}
    if OUT.exists():
        # splitlines() 금지: 본문 속 특수 줄바꿈 문자(U+2028 등)에서도 잘라 버린다
        for line in OUT.read_text(encoding="utf-8").split("\n"):
            if not line:
                continue
            r = json.loads(line)
            store[(r["platform"], r["id"])] = r
    before = len(store)

    new = from_collector()
    for fn, urls, args in ((from_youtube, a.youtube, (a.limit, a.subs)), (from_blog, a.blog, (a.full,))):
        for u in urls:
            try:
                new += fn(u, *args)
            except Exception as e:                   # 인터넷이 끊겼거나 yt-dlp 가 없어도 나머지 정리는 계속한다
                print(f"  ⚠ 못 가져옴 {u}: {e}")
    if a.kakao is not None or a.all:
        new += from_kakao(a.kakao or [])
    if a.inbox is not None or a.all:
        new += from_inbox(a.inbox or [])
    if a.bookmarks or a.all:
        new += from_bookmarks()
    if a.artifacts or a.all:
        new += from_artifacts()
    if a.phone:
        new += from_phone()
    elif a.all:                                      # 폰자료/ 폴더에 둔 파일만. 맥의 메시지·통화·사진 앱 자료는 여전히 --phone 이라고 할 때만 읽는다
        new += from_phone_files()
    if a.disk is not None or a.all:
        new += from_disks(links["disk"])
    for name in map(disk_name, a.undisk):            # 끊은 연결의 자료는 뺀다 (지운자료.jsonl 로 옮기지 않는다 — 파일은 디스크에 그대로 있다)
        for k in [k for k, r in store.items() if k[0] == "disk" and r["author"] == name]:
            del store[k]
        print(f"▶ 연결 끊음: {name}")
    for f in a.imports:
        got = from_import(f, a.platform, a.author)
        print(f"▶ 가져오기 {Path(f).name}: {len(got)}건")
        new += got

    notes = load_notes(store)
    dead = lambda r: notes.get(f'{r["platform"]}|{r["id"]}', {}).get("x")
    merge(store, [r for r in new if not dead(r)])    # 지운 글은 다시 수집돼도 넣지 않는다
    made = to_obsidian(store, notes)
    gone = purge(store, notes)
    if a.phone or a.photos:
        print(f"▶ 사진 미리보기 {photo_previews(store.values())}장 새로 만듦")
    rows = save(store, notes)
    added = len(rows) + gone - before
    for f in DL.glob("tonghap_now_*.json"):          # 「지금 업데이트」 단추가 내려놓은 빈 신호 파일. 할 일을 했으니 치운다
        f.unlink()
    if seen is not None:
        # 정리하기 '전'에 본 모습을 적어 둔다(옮겨 치운 파일은 뺀다) — 정리 도중에 생긴 파일은 다음 번에 잡힌다
        STATE.write_text(json.dumps([x for x in seen if Path(x[0]).exists()], ensure_ascii=False), encoding="utf-8")
    if a.auto_on:
        r = subprocess.run(["launchctl", "bootstrap", f"gui/{os.getuid()}", str(AGENT)], capture_output=True, text=True)
        print("▶ 자동 수집 켬 — 출처에 자료가 생기면 저절로 정리합니다" if r.returncode == 0 else f"⚠ 자동 수집 등록 실패: {r.stderr.strip()}")
    if a.auto_off:
        print("▶ 자동 수집 끔")
    if made:                                         # 방금 만든 노트를 옵시디언에서 바로 연다
        subprocess.run(["open", "obsidian://open?path=" + quote(str(made[0]))], capture_output=True)
    if a.auto and (added or made or gone):           # 알림에는 건수만 싣는다 (남의 글·이름은 넣지 않는다)
        msg = " · ".join(t for t, n in ((f"새 자료 {added}건", added), (f"옵시디언 노트 {len(made)}건", made), (f"지운 글 {gone}건", gone)) if n)
        subprocess.run(["osascript", "-e", f'display notification "{msg} — 열려 있는 화면은 저절로 바뀝니다" with title "KBG-통합자료수집기"'],
                       capture_output=True)

    print("\n" + "=" * 56)
    print(f"이번에 읽은 글 {len(new):,}건 → 새로 더해진 글 {added:,}건 (기존 {before:,} → 지금 {len(rows):,})"
          + (f" · 지운 글 {gone:,}건은 보관/지운자료.jsonl 로" if gone else ""))
    for p, n in Counter(r["platform"] for r in rows).most_common():
        ds = sorted(r["date"][:10] for r in rows if r["platform"] == p and r["date"])
        nodate = sum(1 for r in rows if r["platform"] == p and not r["date"])
        span = f"{ds[0]} ~ {ds[-1]}" if ds else "날짜 없음"
        print(f"  · {p:<10} {n:>6,}건  {span}" + (f"  (날짜 없는 글 {nodate})" if nodate and ds else ""))
    live = [n for n in notes.values() if n.get("m") or n.get("g") or n.get("s")]
    print(f"  메모 {sum(1 for n in live if n.get('m'))}건 · 태그 단 글 {sum(1 for n in live if n.get('g'))}건"
          f" · 별표 {sum(1 for n in live if n.get('s'))}건 (파일에 보존된 것)")
    print(f"\n출력:\n  {OUT}\n  {VIEW}")
    if a.open:
        import webbrowser
        webbrowser.open(VIEW.as_uri())


def selfcheck():
    assert norm_date("20260102") == "2026-01-02"
    assert norm_date("2026-01-02T03:04:05.000Z") == "2026-01-02T03:04:05"
    assert norm_date("2021년 12월 31일") == "2021-12-31"
    assert norm_date("Fri, 02 Jan 2026 03:04:05 +0900") == "2026-01-02T03:04:05"
    assert norm_date(1792825116)[:4] == "2026" and norm_date("3시간") == ""
    assert rec("threads_saved", "DaroS9WiSGS", "글")["date"][:7] == "2026-07" and code_date("없음") == ""
    assert rec("facebook", "DaroS9WiSGS", "글")["date"] == ""
    meta, body = front('---\nsource: "https://youtu.be/abcdefghijk"\nauthor: "[[홍길동]]"\ntags:\n  - a\n---\n본문\n')
    assert (meta["source"], meta["author"], meta["tags"], body) == ("https://youtu.be/abcdefghijk", "홍길동", "", "본문\n")
    assert front("머리말 없는 노트") == ({}, "머리말 없는 노트")
    s = {}
    merge(s, [dict(rec("inbox", "1", "짧음"), file="/a.md"), rec("inbox", "1", "더 긴 본문")])
    assert s[("inbox", "1")]["file"] == "/a.md" and s[("inbox", "1")]["text"] == "더 긴 본문"
    rss = ('<rss xmlns:content="http://purl.org/rss/1.0/modules/content/"><channel><title>내 블로그</title>'
           '<item><title>첫 글</title><link>https://b.example/1</link><pubDate>Fri, 02 Jan 2026 03:04:05 +0900</pubDate>'
           '<description>요약</description><content:encoded><![CDATA[<p>본문 <b>전체</b></p><p>둘째 줄</p>]]>'
           '</content:encoded></item></channel></rss>')
    r, = parse_feed(rss)
    assert (r["title"], r["url"], r["author"], r["date"][:10]) == ("첫 글", "https://b.example/1", "내 블로그", "2026-01-02")
    assert r["text"] == "본문 전체\n둘째 줄", r["text"]
    atom = ('<feed xmlns="http://www.w3.org/2005/Atom"><title>A</title><entry><title>글</title>'
            '<link rel="alternate" href="https://a.example/x"/><link rel="edit" href="https://a.example/edit"/>'
            '<published>2026-03-01T00:00:00Z</published><summary>아톰 요약</summary></entry></feed>')
    r, = parse_feed(atom)
    assert (r["url"], r["text"], r["date"]) == ("https://a.example/x", "아톰 요약", "2026-03-01T00:00:00")
    vtt = "WEBVTT\nKind: captions\n\n00:00.000 --> 00:02.000\n안녕하세요\n\n00:02.000 --> 00:04.000\n안녕하세요\n<c>반갑습니다</c>\n"
    assert vtt_text(vtt) == "안녕하세요 반갑습니다"
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", encoding="utf-8") as t:
        t.write('{"id":"1","time":"1792825116","text":"가져온 글","url":"https://f.example/1","shared":"None"}\n')
        t.flush()
        r, = from_import(t.name, "facebook", "홍길동")
    assert (r["platform"], r["id"], r["author"], r["text"]) == ("facebook", "1", "홍길동", "가져온 글")
    store = {}
    assert merge(store, [rec("x", "1", "짧다", url="u"), rec("x", "1", "더 긴 본문", date="20260102"),
                         rec("x", "2", ""), rec("y", "1", "다른 곳")]) == 2
    assert store[("x", "1")] == rec("x", "1", "더 긴 본문", url="u", date="20260102")
    line = json.dumps(rec("x", "3", "줄\u2028바꿈"), ensure_ascii=False)      # 저장 한 줄이 한 줄로 읽히는가
    assert len((line + "\n").split("\n")) == 2 and json.loads(line)["text"] == "줄\u2028바꿈"
    n = merge_notes({"a": {"m": "옛", "t": 5}, "b": {"m": "그대로", "t": 9}},
                    {"a": {"m": "새", "t": 7}, "b": {"m": "더 옛", "t": 1}, "c": "깨진 값"})
    assert (n["a"]["m"], n["b"]["m"], "c" in n) == ("새", "그대로", False)
    d = {"a": {"m": "x", "t": 1}, "+추가": [{"id": "m1", "title": "제목", "text": "본문", "date": "2026-11-14T10:20:30"}, "깨진 값"]}
    r, = take_added(d)
    assert (r["platform"], r["id"], r["title"], r["date"], "+추가" in d) == ("manual", "m1", "제목", "2026-11-14T10:20:30", False)
    assert take_added({"+추가": "깨진 값"}) == [] and take_added([]) == [] and shelf(r) == "manual"
    # 폰 자료. 문자 본문 묶음은 맥이 실제로 만든 것(NSArchiver)이다.
    ts = bytes.fromhex("040b73747265616d747970656481e803840140848484124e5341747472696275746564537472696e67008484084e534f"
                       "626a656374008592848484084e53537472696e67019484012b13eca7a7ec9d8020ebacb8ec9e902068656c6c6f8684026949"
                       "010b928484840c4e5344696374696f6e6172790094840169008686")
    assert attr_text(ts) == "짧은 문자 hello" and attr_text(b"x") == "" and attr_text(None) == ""
    assert adate(0) == "" and adate(1e9) == adate(1e18) == datetime.fromtimestamp(1e9 + APPLE).isoformat(timespec="seconds")
    rows = {p: row for p, _, _, row in PHONE_DB}
    r = rows["phone_sms"]("g1", None, ts, 1e18, 0, "+821012345678")
    assert (r["text"], r["title"], r["author"], r["date"][:4]) == ("짧은 문자 hello", "받은 문자", "+821012345678", "2032")
    r = rows["phone_call"]("c1", 1e9, 125.4, b"01012345678", None, 0, 0)
    assert (r["text"], r["title"], r["author"]) == ("01012345678 · 2분 5초", "부재중 전화", "01012345678")
    r = rows["phone_photo"]("p1", 1e9, 0, 37.5, 127.0, "IMG_1.HEIC", None, "설명", " iPad ")
    assert (r["text"], r["title"]) == ("사진 · iPad · 위치 37.5000, 127.0000 · 설명", "IMG_1.HEIC")
    assert rows["phone_photo"]("p2", 1e9, 1, -180.0, -180.0, "a.mov", None, None, None)["text"] == "영상"
    assert rows["phone_voice"]("v1", None, 1e9, 61, "20261102 101500.m4a")["title"] == "20261102 101500"
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "sms.xml").write_text('<smses count="2"><sms address="010" date="1794000000000" type="2" body="보냄" '
                                         'contact_name="(Unknown)"/><mms address="010" date="1"/></smses>', encoding="utf-8")
        (Path(d) / "calls.xml").write_text('<calls><call number="02" duration="65" date="1794000000000" type="3" '
                                           'contact_name="교회"/></calls>', encoding="utf-8")
        (Path(d) / "깨진.xml").write_text("<smses>", encoding="utf-8")
        (Path(d) / "메모.txt").write_text("메모 본문", encoding="utf-8")
        (Path(d) / "녹음 1.m4a").write_bytes(b"0" * 2048)
        (Path(d) / "모름.bin").write_bytes(b"0")
        (Path(d) / "통화녹음/Call").mkdir(parents=True)
        (Path(d) / "통화녹음/Call/통화 1.m4a").write_bytes(b"0" * 2048)
        got = {(r["platform"], r["title"]): r for r in from_phone_files(d)}
        assert set(got) == {("phone_sms", "보낸 문자"), ("phone_call", "부재중 전화"), ("phone_note", "메모"), ("phone_voice", "녹음 1"),
                            ("phone_callrec", "통화 1")}, set(got)
        assert got["phone_sms", "보낸 문자"]["author"] == "010" and got["phone_call", "부재중 전화"]["text"] == "교회 · 1분 5초"
        assert got["phone_voice", "녹음 1"]["text"] == "음성 녹음 파일 · 2 KB" and got["phone_voice", "녹음 1"]["url"].startswith("file://")
        assert from_phone_files(Path(d) / "없는 폴더") == []
    with tempfile.TemporaryDirectory() as d:           # 연결한 디스크: 문서·그림만, 숨김·인증서 폴더는 빼고, 상한까지만
        for f in ("가.pdf", "나.jpg", ".숨김.pdf", "다.exe", "NPKI/라.pdf", "아래/마.hwp"):
            (Path(d) / f).parent.mkdir(exist_ok=True)
            (Path(d) / f).write_bytes(b"x")
        got = {r["title"]: r for r in from_disks([d, str(Path(d) / "없는 디스크")])}
        assert set(got) == {"가", "나", "마"} and all(r["platform"] == "disk" for r in got.values()), got
        assert shelf(got["가"]) == "disk_" + Path(d).name and pic(got["나"]) == got["나"]["url"] and pic(got["가"]) == ""
        assert "아래/마.hwp" in got["마"]["text"] and got["마"]["url"].startswith("file://")
        globals()["DISK_MAX"] = 2
        assert len(from_disks([d])) == 2
        globals()["DISK_MAX"] = 20000
    assert "__DISKS__" in PAGE and "linkForm" in PAGE and LABEL["disk"] == "연결"
    assert topic(rec("x", "1", "본문", title="AI로 논문 쓰기")) == "논문" and topic(rec("x", "1", "said hello")) == "기타"
    assert topic(rec("kakao", "1", "링크", title="에이전트코리아")) == "AI/도구" and topic(rec("x", "1", "경기도 날씨")) == "기타"
    assert topic(rec("kakao", "1", "안녕하세요", author="상담하는 죠르디", title="방")) == "기타"      # 카톡 보낸이 별명은 안 본다
    assert origin(rec("kakao", "1", "글", author="보낸이", title="대화방")) == "대화방"
    assert origin(rec("bookmark", "1", "글", author="북마크바 / 신학", url="https://www.youtube.com/watch?v=1")) == "youtube.com"
    assert origin(rec("x", "1", "글")) == "알 수 없음"
    assert shelf(rec("bookmark", "1", "글", author="북마크바 / 추천자료_inbox / obsidian")) == "추천자료_inbox"
    assert shelf(rec("bookmark", "1", "글", author="북마크바 / in box_임시저장")) == "in box_임시저장"
    assert shelf(rec("bookmark", "1", "글", author="북마크바 / 신학")) == "bookmark" and shelf(rec("kakao", "1", "글")) == "kakao"
    r = rec("kakao", "a|b", '첫 줄: "따옴표"\n둘째 줄', author="보낸이", date="20260102", title="대화방/이름")
    name, md = note_md(r, {"m": "왜 저장했나\n둘째", "g": ["나중에 읽기"]}, "kakao|a|b")
    assert name == "2026-01-02 첫 줄 따옴표 (대화방 이름)", name
    assert 'why: "왜 저장했나"' in md and '  - "나중에-읽기"' in md and "[[나중에 읽기]]" in md and md.endswith('둘째 줄\n')
    with tempfile.TemporaryDirectory() as d:
        mark = 'sns_key: "kakao|a|b"'
        assert mark in md and write_new(Path(d), name, md, mark) and not write_new(Path(d), name, md, mark)   # 같은 글은 한 번만
        assert write_new(Path(d), name, "다른 글", "sns_key: 다름") and len(list(Path(d).iterdir())) == 2   # 다른 글은 번호를 붙여 따로
        assert (Path(d) / f"{name}.md").read_text(encoding="utf-8") == md                                    # 먼저 있던 노트는 그대로
        assert write_new(Path(d), "새 노트", md, mark) == Path(d) / "새 노트.md"                               # 새로 쓴 경로를 돌려준다
        (Path(d) / "내 노트.md").write_text("---\ntitle: 내 글\n---\n본문", encoding="utf-8")
        got = [r["title"] for r in from_inbox([d])]
        assert len(got) == 2 and "내 글" in got                                                              # 노트 4개 중 이 도구가 보낸 노트(sns_key) 2개는 다시 읽지 않는다
        st = {("x", "1"): rec("x", "1", "지울 글"), ("x", "2"): rec("x", "2", "둘 글"), ("kakao", "a|b"): r}
        t = Path(d) / "보관" / "지운자료.jsonl"
        assert purge(st, {"x|1": {"x": 1, "t": 1}, "kakao|a|b": {"x": 1}, "x|2": {"x": 0, "m": "메모"}}, t) == 2 and list(st) == [("x", "2")]
        assert [json.loads(l)["id"] for l in t.read_text(encoding="utf-8").split("\n") if l] == ["1", "a|b"]
        assert purge(st, {}, t) == 0
    import tempfile
    with tempfile.TemporaryDirectory() as d:        # 아티팩트 목록: 제목 속 쉼표 · 깨진 줄 · 없는 파일
        c = Path(d) / "a.csv"
        c.write_text("2026-11-14,제목, 쉼표,,https://claude.ai/artifact/abc\n깨진 줄\n", encoding="utf-8")
        got = from_artifacts([c, Path(d) / "없음.csv"])
        assert [(r["platform"], r["id"], r["title"], r["date"], r["text"]) for r in got] == [("claude_artifact", "https://claude.ai/artifact/abc", "제목, 쉼표", "2026-11-14", "제목, 쉼표")]
        assert shelf(got[0]) == "claude_artifact" and origin(got[0]) == "Claude 아티팩트" and "claude_artifact" in LABEL
    # 화면이 새 판을 알아채는 짝(판 번호 자리 · 신호 파일 이름 · 스마트폰 묶음)이 화면과 파이썬 양쪽에 다 있는지
    assert pic(rec("phone_photo", "a/b.JPG", "", "", "file:///x/a/b.JPG", 0, "b")) == "file:///x/a/b.JPG"
    assert pic(rec("phone_photo", "b.heic", "", "", "file:///x/b.heic", 0, "b")) == "" and pic(rec("kakao", "1", "", "", "", 0, "")) == ""
    assert "PP = 20" in PAGE and 'id="pager"' in PAGE and "MAX" not in PAGE
    try:   # node 가 있으면 화면 스크립트 문법까지 본다 — 같은 이름을 두 번 선언해 화면이 통째로 멈춘 적이 있다(2026-11-14)
        r = subprocess.run(["node", "--check"], input=re.search(r"<script>(.*)</script>", PAGE, re.S).group(1), text=True, capture_output=True)
        assert r.returncode == 0, r.stderr[:400]
    except FileNotFoundError:
        pass
    assert PAGE.count("__BUILD__") == 1 and "tonghap_now_" in PAGE and "tonghap_build.js" in PAGE and LABEL["phone"] == "스마트폰"
    assert any(x[0] == str(PHONE_DIR) for x in stamp()) == any(f.is_file() and not f.name.startswith(".") for f in PHONE_DIR.rglob("*"))
    print("selfcheck OK")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
