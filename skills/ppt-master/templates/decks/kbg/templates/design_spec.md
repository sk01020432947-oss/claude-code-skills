---
deck_id: kbg
kind: deck
category: brand
summary: 김병곤 목사 개인 강의·설교 덱 — AI·미래시대 외부 강의, 사회복지 교과목, 연구 발표, 교회 교육·소그룹
keywords: [강의, 설교, 교육, 연구발표, 교회]
canvas_format: ppt169
canvas_width: 1280
canvas_height: 720
canvas_viewbox: "0 0 1280 720"
source_canvas_width: 1280
source_canvas_height: 720
source_viewbox: "0 0 1280 720"
replication_mode: standard
native_structure_mode: structured
page_count: 6
primary_color: "#1F4E79"
placeholders:
  01_cover: ["{{EYEBROW}}", "{{TITLE}}", "{{SUBTITLE}}", "{{AUTHOR}}", "{{DATE}}"]
  02_toc: ["{{PAGE_TITLE}}", "{{TOC_ITEM_1_TITLE}}", "{{TOC_ITEM_1_DESC}}", "{{PAGE_NUM}}"]
  02_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}", "{{CHAPTER_DESC}}", "{{PAGE_NUM}}"]
  03_content: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{PAGE_SUBTITLE}}", "{{AUTHOR}}", "{{PAGE_NUM}}"]
  03a_content_quote: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{QUOTE}}", "{{QUOTE_SOURCE}}", "{{PAGE_NUM}}"]
  04_ending: ["{{CLOSING_MESSAGE}}", "{{ENDING_SUBTITLE}}", "{{CONTACT_INFO}}"]
---

# KBG Lecture & Sermon Deck — Design Specification

> Created 2026-10-09 from the `my-ppt` personal branding rules (type D, verbal brief). Quiet paper-white page, one deep-blue accent, fixed header chrome so every content slide reads from the same eye line.

## I. Template Overview

| Property | Description |
| --- | --- |
| **Template Name** | kbg |
| **Display Name** | KBG 강의·설교 덱 |
| **Use Cases** | AI·미래시대 외부 강의(교사·학부모·목회자), 사회복지 교과목 주차 강의, 기후·삶의 질 연구 발표, 설교 요약·소그룹·새가족 교육 |
| **Design Tone** | Calm, explanatory, trustworthy — a teacher's handout, not a marketing keynote |
| **Theme Mode** | Light (warm paper `#FBFAF7`) + monochrome text + single deep-blue accent |
| **Affiliation** | 우리동네작은교회 · 김병곤 목사 (default `{{AUTHOR}}`) |

**Litmus test**: printed in grayscale for a classroom handout, every slide must still read correctly.

## II. Color Scheme — LOCKED

Only these hex values may appear in generated SVGs:

| Role | HEX | Purpose |
| --- | --- | --- |
| Background | `#FBFAF7` | Page |
| Surface | `#FFFFFF` | Card |
| Surface alt | `#F3F1EC` | Grouped row, table header |
| Text primary | `#1D1F24` | Body and titles |
| Text secondary | `#5D6370` | Subtitles, descriptions |
| Text tertiary | `#9AA0A8` | Footer, page number, captions |
| Border | `#E3E0D8` | Hairlines |
| Accent | `#1F4E79` | Section name, numbers, the one focal element |
| Accent soft | `#E4ECF4` | Highlight band / recommended column / quote band |
| Accent ink | `#163A5C` | Accent on accent-soft |
| Positive / Negative / Warning | `#1F7A4D` / `#B83232` / `#A5671A` | Data meaning only |

Rules: accent events ≤ 2 per content slide; charts use the accent opacity ladder (0.85 / 0.60 / 0.40 / 0.25), never multi-hue; no gradients, shadows, glow or 3D.

## III. Typography

Pretendard only (installed locally; recipients need it too). Title Bold/ExtraBold, body Regular, captions Light/Medium.

Sized for a 24px body (`balanced` delivery: projected and read). Rescaled 2026-10-09 after the first test deck showed the 17.6px chrome was too small for a lecture room.

| Role | Size | Weight |
| --- | --- | --- |
| Cover title | 60 | 700 (placeholder titles use Pretendard + bold; an ExtraBold cut on a title placeholder exports as regular weight) |
| Chapter number / title | 96 / 48 | 800 (number, slide-local) / 700 (title placeholder) |
| Content title | 40 | 700 |
| Page subtitle (lead) | 26 | 500, secondary |
| TOC item title / description | 26 / 18 | 700 / 400 |
| Quote text / source | 30 / 20 | 600 |
| Body | 24 (default) / 20 (dense handout) | 400 |
| Caption | 18 | 400–500 |
| Section name, footer, page number | 14 | 500–600; section name in accent |

## IV. Signature Design Elements

- **Fixed header chrome (non-negotiable)**: section name baseline y=62 → title baseline y=114 → subtitle baseline y=154 → hairline y=176. Identical on every content and quote page; only cover / TOC / chapter / ending differ.
- **Fixed footer**: hairline y=656, `{{AUTHOR}}` bottom-left (y=686), page number bottom-right `03 / 18`.
- **Vertical accent bar** (6 px) as the only ornament on cover, ending and quote; chapter pages carry a full-height 16 px accent edge.
- **Body density**: body region x=56, y=196, w=1168, h=440. Do not leave the lower third empty — add a diagram, table or supporting note, or merge slides; never cram past the footer rule.
- **Quote page** for scripture, citations and definitions: soft band with source line (`{{QUOTE_SOURCE}}`, e.g. `로마서 1:1-3 (개역개정)`). Quote text must be verbatim from the user's material; never invent wording or references.
- **No logo yet**: `my-ppt/assets/logo.png` does not exist. Do not add any logo or mark until the user supplies one.
- Image/design prompts are written in English; slide text is Korean.

## V. Page Roster

| File | Role | Description / content fit |
| --- | --- | --- |
| `01_cover.svg` | cover | Event or course label, title, subtitle, presenter and date |
| `02_toc.svg` | toc | Up to 5 indexed items (number + title + one-line description); delete unused rows |
| `02_chapter.svg` | chapter | Large chapter number, chapter title, one-line summary; use every 4–6 content slides |
| `03_content.svg` | content | Fixed header/footer chrome; body composed freely |
| `03a_content_quote.svg` | content | Scripture, quotation or definition with source line and one interpretive note |
| `04_ending.svg` | ending | Closing message, subtitle (e.g. discussion prompt), contact line |

## VI. Usage

1. Pass this workspace root to SKILL.md Step 3: `.claude/skills/ppt-master/templates/decks/kbg/`.
2. Numbers, quotes and scripture references come only from the user's sources; where missing, write `[자료 필요]`.
3. Recommended adherence: `adaptive` for lectures (new body layouts allowed), `strict` for weekly church slides.
