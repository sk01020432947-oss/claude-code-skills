#!/usr/bin/env python3
"""논고 마크다운 → 아티팩트용 읽기 페이지(차례 고정, 라이트/다크). pandoc 필요.
사용: md2web.py 논고.md 사본.html "페이지 제목" "부제" "저자 · 소속" "날짜"
md의 첫 '# 제목'과 바로 아래 저자/날짜 줄·첫 '---'는 머리말로 대체된다."""
import re, subprocess, sys

CSS = open(__file__.replace("md2web.py", "essay.css"), encoding="utf-8").read()

def build(md_path, title, sub, byline, date):
    b = subprocess.run(["pandoc", "-f", "markdown", "-t", "html5", md_path], capture_output=True, text=True, check=True).stdout
    b = re.sub(r"<h1[^>]*>.*?</h1>", "", b, count=1, flags=re.S)
    b = re.sub(r"^\s*<p>[^<]*?\d{4}-\d{2}-\d{2}\s*</p>\s*<hr\s*/?>", "", b, count=1, flags=re.S)
    b = b.replace("<table", '<div class="tw"><table').replace("</table>", "</table></div>")
    toc = "".join(f'<li><a href="#{a}">{re.sub(r"<[^>]+>|\s+", " ", t).strip()}</a></li>'
                  for a, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', b, re.S))
    head = (f'<header class="t"><div class="kicker">논고 · {date}</div><h1>{title}</h1>'
            f"<p>{sub}</p><p>{byline}</p></header>")
    return (f"<title>{title} 논고</title>\n" + CSS +
            f'<div class="wrap"><nav aria-label="차례"><b>차례</b><ol>{toc}</ol></nav><article>{head}{b}</article></div>\n')

if __name__ == "__main__":
    src, dst, *meta = sys.argv[1:]
    open(dst, "w", encoding="utf-8").write(build(src, *meta))
    print("written", dst)
