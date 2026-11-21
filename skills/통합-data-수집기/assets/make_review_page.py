#!/usr/bin/env python3
"""
파싱 결과를 검색·필터 가능한 검토용 HTML 페이지로 만든다.

JSON은 기계용, 마크다운은 152개를 훑기엔 길다.
이 페이지는 '이상한 걸 찾아내는' 작업에 맞춰 설계했다:
검색 / 연속발행만 보기 / 짧은 글만 보기 / 메모 있는 글만 보기.

사용법:
    python make_review_page.py raw/manual_2026-08-01_254_parsed.json
"""

import argparse
import html
import json
import sys
from pathlib import Path

CSS = """
:root{
  --paper:#f6f6f4; --panel:#fff; --ink:#16202b; --ink-2:#3c4653;
  --muted:#6b7480; --rule:#d9dad6; --rule-soft:#e8e9e5;
  --accent:#2f5d62; --accent-soft:#e4ecec;
  --caution:#9a5b16; --caution-soft:#f6ecdd;
  --sans:"Pretendard","Segoe UI","Malgun Gothic","맑은 고딕","Apple SD Gothic Neo",system-ui,sans-serif;
  --mono:"Cascadia Mono","Consolas","D2Coding","Menlo",ui-monospace,monospace;
}
@media (prefers-color-scheme:dark){:root{
  --paper:#12171c; --panel:#171d24; --ink:#e4e7e5; --ink-2:#b3bac0;
  --muted:#8b949e; --rule:#2b333b; --rule-soft:#222931;
  --accent:#7fb3b7; --accent-soft:#1d2c2e;
  --caution:#d59a53; --caution-soft:#2c2418;
}}
:root[data-theme="dark"]{
  --paper:#12171c; --panel:#171d24; --ink:#e4e7e5; --ink-2:#b3bac0;
  --muted:#8b949e; --rule:#2b333b; --rule-soft:#222931;
  --accent:#7fb3b7; --accent-soft:#1d2c2e;
  --caution:#d59a53; --caution-soft:#2c2418;
}
:root[data-theme="light"]{
  --paper:#f6f6f4; --panel:#fff; --ink:#16202b; --ink-2:#3c4653;
  --muted:#6b7480; --rule:#d9dad6; --rule-soft:#e8e9e5;
  --accent:#2f5d62; --accent-soft:#e4ecec;
  --caution:#9a5b16; --caution-soft:#f6ecdd;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:var(--sans);font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:820px;margin:0 auto;padding:0 20px 100px}

header{padding:40px 0 0}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--accent);margin-bottom:12px}
h1{font-size:clamp(24px,4vw,32px);line-height:1.25;font-weight:800;
  letter-spacing:-.02em;margin:0 0 12px;text-wrap:balance}
.lede{font-size:16px;color:var(--ink-2);margin:0 0 20px}

.howto{background:var(--panel);border-left:3px solid var(--accent);
  padding:14px 18px;margin:0 0 22px;font-size:14.5px}
.howto ol{margin:8px 0 0;padding-left:20px}
.howto li{margin-bottom:5px}

.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));
  gap:1px;background:var(--rule);border:1px solid var(--rule);margin:0 0 26px}
.stat{background:var(--panel);padding:12px 14px}
.stat dt{font-family:var(--mono);font-size:10px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--muted);margin-bottom:4px}
.stat dd{margin:0;font-size:19px;font-weight:700;font-variant-numeric:tabular-nums}

/* 상단 고정 툴바 */
.toolbar{position:sticky;top:0;z-index:20;background:var(--paper);
  border-bottom:1px solid var(--rule);padding:12px 0;margin-bottom:6px}
.searchrow{display:flex;gap:8px;align-items:center;margin-bottom:9px}
.searchbox{flex:1;display:flex;align-items:center;gap:7px;border:1px solid var(--rule);
  background:var(--panel);border-radius:6px;padding:8px 11px}
.searchbox input{flex:1;min-width:0;border:0;outline:0;background:transparent;
  color:var(--ink);font-family:var(--sans);font-size:15px}
.searchbox input::placeholder{color:var(--muted)}
.hitcount{font-family:var(--mono);font-size:11px;color:var(--muted);white-space:nowrap}
.pills{display:flex;flex-wrap:wrap;gap:6px}
.pill{font-family:var(--mono);font-size:11px;letter-spacing:.03em;padding:5px 11px;
  border-radius:999px;cursor:pointer;background:transparent;border:1px solid var(--rule);
  color:var(--ink-2);transition:background .15s,color .15s,border-color .15s}
.pill:hover{border-color:var(--accent);color:var(--accent)}
.pill.on{background:var(--accent);border-color:var(--accent);color:var(--panel)}
.pill.warn.on{background:var(--caution);border-color:var(--caution)}
.pill:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

/* 글 카드 */
.card{background:var(--panel);border:1px solid var(--rule);border-radius:6px;
  padding:16px 18px;margin:14px 0}
.card.chain{border-left:3px solid var(--accent)}
.card-head{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:baseline;
  margin-bottom:10px;padding-bottom:9px;border-bottom:1px solid var(--rule-soft)}
.idx{font-family:var(--mono);font-size:12px;color:var(--muted);font-weight:700}
.date{font-family:var(--mono);font-size:12px;color:var(--ink-2)}
.tag{font-family:var(--mono);font-size:10.5px;padding:1px 7px;border-radius:2px;
  background:var(--accent-soft);color:var(--accent)}
.eng{font-family:var(--mono);font-size:11px;color:var(--muted);
  font-variant-numeric:tabular-nums;margin-left:auto}
.card-body{white-space:pre-wrap;font-size:15px;line-height:1.75}
.card-foot{margin-top:11px;padding-top:9px;border-top:1px solid var(--rule-soft);
  display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;
  font-family:var(--mono);font-size:11px;color:var(--muted)}
.card-foot a{color:var(--muted)}
.badge{font-family:var(--mono);font-size:10px;padding:2px 7px;border-radius:2px;
  background:var(--accent-soft);color:var(--accent);border:1px solid var(--accent)}
.badge.warn{background:var(--caution-soft);color:var(--caution);border-color:var(--caution)}
a{color:var(--accent);text-underline-offset:2px}
mark{background:var(--accent-soft);color:var(--ink);padding:0 1px;border-radius:2px}

.empty{text-align:center;color:var(--muted);padding:50px 20px;font-size:15px}
footer{margin-top:50px;padding-top:20px;border-top:2px solid var(--ink);
  font-size:13px;color:var(--muted)}
footer code{font-family:var(--mono);font-size:12px;background:var(--panel);
  padding:1px 5px;border:1px solid var(--rule)}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

JS = """
(function(){
  var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
  var input = document.getElementById('q');
  var count = document.getElementById('hits');
  var empty = document.getElementById('empty');
  var pills = Array.prototype.slice.call(document.querySelectorAll('.pill'));
  var activeFilter = null;

  function textOf(c){ return c.getAttribute('data-text') || ''; }

  function apply(){
    var q = (input.value || '').trim().toLowerCase();
    var shown = 0;
    cards.forEach(function(c){
      var okFilter = !activeFilter || c.hasAttribute('data-' + activeFilter);
      var okQuery = !q || textOf(c).indexOf(q) !== -1;
      var show = okFilter && okQuery;
      c.style.display = show ? '' : 'none';
      if (show) shown++;
      // 하이라이트
      var body = c.querySelector('.card-body');
      var orig = c.getAttribute('data-orig');
      if (!q) { body.textContent = orig; }
      else if (show) {
        var lower = orig.toLowerCase(), out = '', last = 0, i = lower.indexOf(q);
        while (i !== -1) {
          out += escapeHtml(orig.slice(last, i)) + '<mark>' +
                 escapeHtml(orig.substr(i, q.length)) + '</mark>';
          last = i + q.length; i = lower.indexOf(q, last);
        }
        out += escapeHtml(orig.slice(last));
        body.innerHTML = out;
      }
    });
    count.textContent = shown + ' / ' + cards.length;
    empty.style.display = shown ? 'none' : '';
  }

  function escapeHtml(s){
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  pills.forEach(function(p){
    p.addEventListener('click', function(){
      var f = p.getAttribute('data-filter');
      activeFilter = (activeFilter === f) ? null : f;
      pills.forEach(function(x){ x.classList.toggle('on', x.getAttribute('data-filter') === activeFilter); });
      apply();
    });
  });

  var t;
  input.addEventListener('input', function(){ clearTimeout(t); t = setTimeout(apply, 120); });
  input.addEventListener('keydown', function(e){
    if (e.key === 'Escape'){ input.value=''; apply(); input.blur(); }
  });
  document.addEventListener('keydown', function(e){
    if (e.key === '/' && document.activeElement !== input){ e.preventDefault(); input.focus(); }
  });
  apply();
})();
"""


def fmt_counts(counts):
    labels = ["♥", "댓", "리포", "공유"]

    def one(nums):
        if not nums:
            return ""
        return " ".join(f"{labels[i] if i < len(labels) else '?'}{n}"
                        for i, n in enumerate(nums))

    if counts and isinstance(counts[0], list):
        return "  +  ".join(x for x in (one(c) for c in counts) if x)
    return one(counts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--open", action="store_true",
                    help="만든 뒤 바로 브라우저로 연다")
    args = ap.parse_args()

    src = Path(args.input)
    data = json.loads(src.read_text(encoding="utf-8"))
    data = sorted(data, key=lambda x: x.get("created_at") or "", reverse=True)

    total_chars = sum(len(d["text"]) for d in data)
    n_chain = sum(1 for d in data if d.get("parts", 1) > 1)
    n_warn = sum(1 for d in data if d.get("_warnings"))
    n_short = sum(1 for d in data if len(d["text"]) < 40)
    dates = sorted(d["created_at"][:10] for d in data if d.get("created_at"))

    P = []
    A = P.append
    accounts = {d.get("username") for d in data if d.get("username")}
    who = accounts.pop() if len(accounts) == 1 else src.stem
    A(f"<title>파싱 결과 검토 — {html.escape(who)}</title>")
    A(f"<style>{CSS}</style>")
    A('<div class="wrap">')

    A("<header>")
    A('<div class="eyebrow">파싱 결과 검토 · 2026-08-01</div>')
    A("<h1>수집한 글이 제대로 정리됐는지 확인</h1>")
    A('<p class="lede">수집기가 화면에서 긁어온 덩어리에서 계정명·날짜·좋아요 숫자를 걷어내고, '
      '연속 발행된 글을 하나로 합친 결과입니다. 아래에서 이상한 게 없는지 봐주세요.</p>')

    A('<div class="howto"><strong>이것만 확인하면 됩니다</strong><ol>'
      "<li>본문이 <strong>중간에 잘렸거나</strong>, 엉뚱하게 이어붙은 글이 있는지</li>"
      "<li>본문에 <strong>계정명·날짜·숫자 같은 부스러기</strong>가 남았는지</li>"
      "<li><strong>연속 발행</strong>으로 합친 글에서 두 조각이 자연스럽게 이어지는지</li>"
      "</ol>이상한 걸 찾으면 <strong>글 번호</strong>를 알려주시면 됩니다.</div>")

    A('<dl class="stats">')
    A(f'<div class="stat"><dt>글 수</dt><dd>{len(data)}</dd></div>')
    A(f'<div class="stat"><dt>총 글자수</dt><dd>{total_chars:,}</dd></div>')
    A(f'<div class="stat"><dt>연속발행 병합</dt><dd>{n_chain}</dd></div>')
    if dates:
        A(f'<div class="stat"><dt>기간</dt><dd style="font-size:13px">'
          f"{dates[0]}<br>~ {dates[-1]}</dd></div>")
    A("</dl>")
    A("</header>")

    A('<div class="toolbar">')
    A('<div class="searchrow"><div class="searchbox">'
      '<input type="text" id="q" placeholder="내용 검색…  ( / 키로 이동 )" aria-label="내용 검색">'
      '</div><span class="hitcount" id="hits"></span></div>')
    A('<div class="pills">')
    A(f'<button type="button" class="pill" data-filter="chain">🔗 연속발행만 ({n_chain})</button>')
    A(f'<button type="button" class="pill" data-filter="short">짧은 글만 ({n_short})</button>')
    A(f'<button type="button" class="pill warn" data-filter="warn">메모 있는 글 ({n_warn})</button>')
    A("</div></div>")

    for i, d in enumerate(data, 1):
        text = d["text"]
        date = (d.get("created_at") or "")[:10]
        is_chain = d.get("parts", 1) > 1
        is_short = len(text) < 40
        has_warn = bool(d.get("_warnings"))

        attrs = ['class="card' + (" chain" if is_chain else "") + '"']
        attrs.append(f'data-text="{html.escape(text.lower(), quote=True)}"')
        attrs.append(f'data-orig="{html.escape(text, quote=True)}"')
        if is_chain:
            attrs.append("data-chain")
        if is_short:
            attrs.append("data-short")
        if has_warn:
            attrs.append("data-warn")

        A(f"<article {' '.join(attrs)}>")
        A('<div class="card-head">')
        A(f'<span class="idx">#{i}</span>')
        A(f'<span class="date">{date}</span>')
        for t in d.get("tags", []):
            A(f'<span class="tag">{html.escape(t)}</span>')
        eng = fmt_counts(d.get("counts"))
        if eng:
            A(f'<span class="eng">{html.escape(eng)}</span>')
        A("</div>")

        A(f'<div class="card-body">{html.escape(text)}</div>')

        A('<div class="card-foot">')
        if is_chain:
            A(f'<span class="badge">🔗 {d["parts"]}개 합침</span>')
        A(f'<a href="{d.get("url")}" target="_blank" rel="noopener">원문 →</a>')
        A(f"<span>{len(text)}자</span>")
        if has_warn:
            for w in sorted(set(d["_warnings"])):
                A(f'<span class="badge warn">{html.escape(w)}</span>')
        A("</div>")
        A("</article>")

    A('<div class="empty" id="empty" style="display:none">'
      "조건에 맞는 글이 없습니다.</div>")

    A("<footer><p>"
      f"원본 데이터 <code>{src.name}</code><br>"
      "이 페이지는 검토용 사본입니다 — 판정 후 원본을 기준으로 작업합니다."
      "</p></footer>")
    A("</div>")
    A(f"<script>{JS}</script>")

    out = src.parent / f"{src.stem}_검토용.html"
    out.write_text("\n".join(P), encoding="utf-8")
    print(f"생성: {out}")
    print(f"  글 {len(data)} · 연속발행 {n_chain} · 짧은글 {n_short} · 메모 {n_warn}")

    if args.open:
        import webbrowser
        webbrowser.open(out.resolve().as_uri())


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
