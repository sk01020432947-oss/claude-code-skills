# -*- coding: utf-8 -*-
"""genie-report HTML -> editable PPTX (A4 portrait).

Usage:  python report2pptx.py report.html [--accent "#5B2D90"]

Parses the genie-report template structure (known classes only) and rebuilds
each .page as one A4-portrait slide with native text boxes, tables and shapes,
so the deck stays editable in PowerPoint (tone & manner step).

# ponytail: block heights are estimated from char counts, not rendered metrics.
# Slight vertical drift vs the HTML is accepted; upgrade path is a headless
# text-measurement pass if drift ever exceeds a page.
"""
import sys, re, html as htmlmod
from html.parser import HTMLParser
from pptx import Presentation
from pptx.util import Mm, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---------- geometry ----------
PAGE_W, PAGE_H = 210, 297
MARG_L, MARG_R, TOP = 18, 18, 24
CONTENT_W = PAGE_W - MARG_L - MARG_R
PT2MM = 0.3528

INK, BODY, MUTE, LINE, FILL = "1A1A1A", "333333", "777777", "DDDDDD", "F4F4F4"
ACCENT = "1A1A1A"
FONT = "Pretendard"

def rgb(h): return RGBColor.from_string(h.lstrip("#").upper())

# ---------- tiny DOM ----------
class Node:
    def __init__(self, tag, attrs):
        self.tag = tag
        self.attrs = dict(attrs)
        self.cls = (self.attrs.get("class") or "").split()
        self.children = []
    def texts(self):
        out = []
        for c in self.children:
            out.append(c if isinstance(c, str) else c.texts())
        return "".join(out)
    def find_all(self, pred, out=None):
        out = [] if out is None else out
        for c in self.children:
            if isinstance(c, Node):
                if pred(c): out.append(c)
                c.find_all(pred, out)
        return out

class Dom(HTMLParser):
    VOID = {"br", "img", "meta", "link", "hr", "input"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root", []); self.stack = [self.root]
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs); self.stack[-1].children.append(n)
        if tag not in self.VOID: self.stack.append(n)
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag: del self.stack[i:]; break
    def handle_data(self, data):
        if data.strip() or (self.stack[-1].tag in ("p", "li", "b", "em", "span", "i", "small")):
            self.stack[-1].children.append(data)

def parse(path):
    with open(path, encoding="utf-8") as f: text = f.read()
    text = re.sub(r"<script.*?</script>", "", text, flags=re.S)
    text = re.sub(r"<style.*?</style>", "", text, flags=re.S)
    d = Dom(); d.feed(text); return d.root

# ---------- inline runs: (text, bold, accent) ----------
def runs_of(node):
    out = []
    def walk(n, bold=False, accent=False):
        for c in n.children:
            if isinstance(c, str):
                t = re.sub(r"\s+", " ", c)
                if t: out.append((t, bold, accent))
            elif c.tag == "b": walk(c, True, accent)
            elif c.tag == "em": walk(c, bold, True)
            elif c.tag in ("span", "i", "small"): walk(c, bold, accent)
    walk(node)
    return out

def plain(node): return re.sub(r"\s+", " ", node.texts()).strip()

def est_h(text, size_pt, width_mm, lh=1.65):
    cpl = max(8, int(width_mm / (size_pt * PT2MM * 0.92)))
    lines = max(1, -(-len(text) // cpl))
    return lines * size_pt * PT2MM * lh

# ---------- pptx helpers ----------
def _noautofit(tf):
    el = tf._txBody.find(qn("a:bodyPr"))
    for t in ("a:normAutofit", "a:spAutoFit"):
        e = el.find(qn(t))
        if e is not None: el.remove(e)

def tbox(slide, x, y, w, h):
    b = slide.shapes.add_textbox(Mm(x), Mm(y), Mm(w), Mm(h))
    tf = b.text_frame; tf.word_wrap = True; _noautofit(tf)
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    return tf

def para(tf, first=True):
    return tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()

def add_runs(p, runs, size, color=BODY, base_bold=False, accent=ACCENT):
    for t, bold, acc in runs:
        r = p.add_run(); r.text = t
        r.font.name = FONT; r.font.size = Pt(size)
        r.font.bold = bold or base_bold
        r.font.color.rgb = rgb(accent if acc else (INK if bold else color))
    return p

def rect(slide, x, y, w, h, fill=None, line=None, line_w=0.5):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Mm(x), Mm(y), Mm(w), Mm(h))
    s.shadow.inherit = False
    if fill: s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
    else: s.fill.background()
    if line: s.line.color.rgb = rgb(line); s.line.width = Pt(line_w)
    else: s.line.fill.background()
    return s

# ---------- block renderers (each returns height used, mm) ----------
def r_titleblock(slide, n, x, y, w):
    y0 = y
    for c in n.children:
        if not isinstance(c, Node): continue
        if "kicker" in c.cls:
            p = para(tbox(slide, x, y, w, 6))
            add_runs(p, [(plain(c), False, True)], 10, base_bold=True)
            y += 7
        elif c.tag == "h1":
            t = plain(c); h = est_h(t, 26, w, 1.3)
            p = para(tbox(slide, x, y, w, h))
            add_runs(p, [(t, True, False)], 26)
            y += h + 3
        elif "sub" in c.cls:
            t = plain(c); h = est_h(t, 12.5, w, 1.5)
            add_runs(para(tbox(slide, x, y, w, h)), [(t, False, False)], 12.5)
            y += h + 5
        elif "meta" in c.cls:
            rect(slide, x, y, w, 0.5, fill=INK)
            cells = [d for d in c.children if isinstance(d, Node)]
            cw = w / max(1, len(cells))
            for i, d in enumerate(cells):
                lab = next((plain(b) for b in d.children if isinstance(b, Node) and b.tag == "b"), "")
                val = "".join(s for s in d.children if isinstance(s, str)).strip()
                tf = tbox(slide, x + i * cw, y + 2, cw - 2, 10)
                add_runs(para(tf), [(lab, False, False)], 8, color=MUTE)
                add_runs(tf.add_paragraph(), [(val, False, False)], 9)
            y += 13
            rect(slide, x, y, w, 0.2, fill=LINE)
            y += 3
    return y - y0

def r_h2(slide, n, x, y, w):
    p = para(tbox(slide, x, y + 3, w, 8))
    rs = runs_of(n)
    if rs and rs[0][2]:  # CSS margin on <em> has no pptx equivalent — pad with spaces
        rs[0] = (rs[0][0] + "  ", rs[0][1], rs[0][2])
    add_runs(p, rs, 13.5, base_bold=True)
    rect(slide, x, y + 10.5, w, 0.35, fill=INK)
    return 14.5

def r_h3(slide, n, x, y, w):
    add_runs(para(tbox(slide, x, y, w, 6)), [(plain(n), True, False)], 11)
    return 7.5

def r_p(slide, n, x, y, w):
    t = plain(n); h = est_h(t, 10.5, w)
    p = para(tbox(slide, x, y, w, h)); p.alignment = PP_ALIGN.JUSTIFY
    add_runs(p, runs_of(n), 10.5)
    return h + 2.5

def r_ul(slide, n, x, y, w):
    items = [c for c in n.children if isinstance(c, Node) and c.tag == "li"]
    tf = tbox(slide, x + 1, y, w - 1, 6); h = 0; first = True
    for li in items:
        p = para(tf, first); first = False
        add_runs(p, [("▪ ", False, False)] + runs_of(li), 10.5)
        h += est_h(plain(li), 10.5, w - 5, 1.62) + 0.8
    return h + 2.5

def r_callout(slide, n, x, y, w):
    t = plain(n); h = est_h(t, 10, w - 11, 1.6) + 9
    rect(slide, x, y, w, h, fill=FILL, line=LINE, line_w=0.5)
    tf = tbox(slide, x + 5.5, y + 4, w - 11, h - 8)
    rs = runs_of(n)
    if rs and rs[0][1]:  # leading <b> becomes its own heading line
        add_runs(para(tf), [rs[0]], 10.5)
        add_runs(tf.add_paragraph(), rs[1:], 10)
    else:
        add_runs(para(tf), rs, 10)
    return h + 4

def r_table(slide, n, x, y, w):
    rows = n.find_all(lambda c: c.tag == "tr")
    if not rows: return 0
    ncol = len([c for c in rows[0].children if isinstance(c, Node) and c.tag in ("th", "td")])
    rh = 8.5
    gt = slide.shapes.add_table(len(rows), ncol, Mm(x), Mm(y), Mm(w), Mm(rh * len(rows)))
    tbl = gt.table
    tbl.first_row = False; tbl.horz_banding = False
    for ri, tr in enumerate(rows):
        cells = [c for c in tr.children if isinstance(c, Node) and c.tag in ("th", "td")]
        for ci, cell in enumerate(cells):
            if ci >= ncol: break
            pc = tbl.cell(ri, ci)
            pc.fill.solid()
            pc.fill.fore_color.rgb = rgb(FILL if cell.tag == "th" else "FFFFFF")
            pc.margin_left = Mm(2.6); pc.margin_right = Mm(2); pc.margin_top = Mm(1.6); pc.margin_bottom = Mm(1.2)
            tf = pc.text_frame; tf.word_wrap = True
            hl = "hl" in cell.cls
            col = ACCENT if hl else (INK if cell.tag == "th" else BODY)
            p = tf.paragraphs[0]
            r = p.add_run(); r.text = plain(cell)
            r.font.name = FONT; r.font.size = Pt(9.5)
            r.font.bold = (cell.tag == "th") or hl
            r.font.color.rgb = rgb(col)
    return rh * len(rows) + 3

def r_kpirow(slide, n, x, y, w):
    kpis = [c for c in n.children if isinstance(c, Node) and "kpi" in c.cls]
    if not kpis: return 0
    gap = 4; kw = (w - gap * (len(kpis) - 1)) / len(kpis); kh = 27
    for i, k in enumerate(kpis):
        kx = x + i * (kw + gap)
        rect(slide, kx, y, kw, kh, line=LINE, line_w=0.5)
        rect(slide, kx, y, kw, 0.5, fill=ACCENT)
        tf = tbox(slide, kx + 1.5, y + 4, kw - 3, kh - 7)
        num = lab = cap = ""
        for c in k.children:
            if not isinstance(c, Node): continue
            if c.tag == "b": num = plain(c)
            elif c.tag == "i": lab = plain(c)
            elif c.tag == "small": cap = plain(c)
        for txt, sz, col, bold in ((num, 19, ACCENT, True), (lab, 9.5, INK, True), (cap, 8, MUTE, False)):
            p = para(tf, txt == num); p.alignment = PP_ALIGN.CENTER
            add_runs(p, [(txt, False, False)], sz, color=col, base_bold=bold)
    return kh + 4

def r_barchart(slide, n, x, y, w):
    rows = [c for c in n.children if isinstance(c, Node) and "brow" in c.cls]
    lbl_w, val_w, bh, gap = 34, 20, 6.5, 2.4
    track_w = w - lbl_w - val_w - 6
    for i, br in enumerate(rows):
        ry = y + i * (bh + gap)
        lbl = val = ""; pct = 0
        for c in br.children:
            if not isinstance(c, Node): continue
            if "lbl" in c.cls: lbl = plain(c)
            elif "val" in c.cls: val = plain(c)
            elif "track" in c.cls:
                for bar in c.children:
                    if isinstance(bar, Node) and "bar" in bar.cls:
                        m = re.search(r"width:\s*([\d.]+)%", bar.attrs.get("style", ""))
                        if m: pct = float(m.group(1))
        p = para(tbox(slide, x, ry + 1, lbl_w, 5)); p.alignment = PP_ALIGN.RIGHT
        add_runs(p, [(lbl, False, False)], 9)
        rect(slide, x + lbl_w + 3, ry, track_w, bh, fill=FILL)
        if pct: rect(slide, x + lbl_w + 3, ry, track_w * pct / 100, bh, fill=ACCENT)
        add_runs(para(tbox(slide, x + lbl_w + 3 + track_w + 3, ry + 1, val_w, 5)),
                 [(val, False, False)], 9, base_bold=True)
    return len(rows) * (bh + gap) + 2

def r_small(slide, n, x, y, w, size=8):
    t = plain(n)
    add_runs(para(tbox(slide, x, y, w, 5)), [(t, False, False)], size, color=MUTE)
    return 6.5

def r_grid2(slide, n, x, y, w):
    cols = [c for c in n.children if isinstance(c, Node) and "col" in c.cls]
    if not cols: return 0
    gap = 6; cw = (w - gap * (len(cols) - 1)) / len(cols)
    maxh = 0
    for i, col in enumerate(cols):
        cy = y
        for c in col.children:
            if isinstance(c, Node):
                cy += render_block(slide, c, x + i * (cw + gap), cy, cw)
        maxh = max(maxh, cy - y)
    return maxh + 2

def render_block(slide, n, x, y, w):
    if "titleblock" in n.cls: return r_titleblock(slide, n, x, y, w)
    if n.tag == "h2": return r_h2(slide, n, x, y, w)
    if n.tag == "h3": return r_h3(slide, n, x, y, w)
    if n.tag == "p": return r_p(slide, n, x, y, w)
    if n.tag == "ul": return r_ul(slide, n, x, y, w)
    if n.tag == "table": return r_table(slide, n, x, y, w)
    if "callout" in n.cls: return r_callout(slide, n, x, y, w)
    if "kpirow" in n.cls: return r_kpirow(slide, n, x, y, w)
    if "barchart" in n.cls: return r_barchart(slide, n, x, y, w)
    if "chartcap" in n.cls or "src" in n.cls: return r_small(slide, n, x, y, w)
    if "grid2" in n.cls: return r_grid2(slide, n, x, y, w)
    if "phead" in n.cls or "pfoot" in n.cls: return 0  # rendered separately
    h = 0  # unknown wrapper: recurse
    for c in n.children:
        if isinstance(c, Node): h += render_block(slide, c, x, y + h, w)
    return h

def r_frame(slide, page, npage, total):
    rect(slide, 0, 0, PAGE_W, 1.2, fill=ACCENT)
    head = next((c for c in page.children if isinstance(c, Node) and "phead" in c.cls), None)
    if head is not None:
        title = next((plain(c) for c in head.children if isinstance(c, Node) and c.tag == "b"), plain(head))
        add_runs(para(tbox(slide, MARG_L, 7, CONTENT_W - 25, 5)), [(title, False, False)], 8.5, color=MUTE)
        p = para(tbox(slide, PAGE_W - MARG_R - 25, 7, 25, 5)); p.alignment = PP_ALIGN.RIGHT
        add_runs(p, [("%d / %d" % (npage, total), False, False)], 8.5, color=MUTE)
        rect(slide, MARG_L, 12.2, CONTENT_W, 0.15, fill=LINE)
    foot = next((c for c in page.children if isinstance(c, Node) and "pfoot" in c.cls), None)
    if foot is not None:
        spans = [plain(c) for c in foot.children if isinstance(c, Node)]
        rect(slide, MARG_L, PAGE_H - 10.5, CONTENT_W, 0.15, fill=LINE)
        if spans:
            add_runs(para(tbox(slide, MARG_L, PAGE_H - 9, CONTENT_W / 2, 5)), [(spans[0], False, False)], 8, color=MUTE)
        if len(spans) > 1:
            p = para(tbox(slide, PAGE_W / 2, PAGE_H - 9, CONTENT_W / 2 - 0, 5)); p.alignment = PP_ALIGN.RIGHT
            add_runs(p, [(spans[-1], False, False)], 8, color=MUTE)

def main():
    global ACCENT
    args = sys.argv[1:]
    if "--accent" in args:
        i = args.index("--accent"); ACCENT = args[i + 1].lstrip("#").upper(); del args[i:i + 2]
    if not args:
        print(__doc__); sys.exit(1)
    src = args[0]
    root = parse(src)
    pages = root.find_all(lambda n: "page" in n.cls and n.tag in ("section", "div"))
    prs = Presentation()
    prs.slide_width = Mm(PAGE_W); prs.slide_height = Mm(PAGE_H)
    blank = prs.slide_layouts[6]
    for i, page in enumerate(pages):
        slide = prs.slides.add_slide(blank)
        r_frame(slide, page, i + 1, len(pages))
        y = TOP
        for c in page.children:
            if isinstance(c, Node):
                mt = re.search(r"margin-top:\s*0", c.attrs.get("style", ""))
                y += render_block(slide, c, MARG_L, y, CONTENT_W)
        if y > PAGE_H - 12:
            print(f"[warn] page {i+1}: estimated content {y:.0f}mm exceeds A4 — check in PowerPoint")
    out = re.sub(r"\.html?$", "", src) + ".pptx"
    prs.save(out)
    print(f"saved: {out}  ({len(pages)} slides, accent #{ACCENT})")

if __name__ == "__main__":
    main()
