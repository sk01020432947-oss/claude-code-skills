---
name: youtube-wiki-ingest
description: "Ingest YouTube videos (a channel, playlist, or single URL) into an LLM Wiki / Obsidian vault as timestamped raw transcripts plus concept pages, so answers cite the source video title, URL and exact start–end time. One video per run by default; does nothing when there is no unprocessed video. Triggers: 유튜브 위키 적재, 채널 대본 위키로, youtube wiki ingest, 영상 지식베이스, 타임스탬프 출처 위키."
---

# YouTube → LLM Wiki Ingest

Turns a YouTube source into wiki knowledge whose every claim points back to
`video title + URL + start–end timestamp`. Deterministic work (collect, clean,
chunk, link) is done by `scripts/yt_wiki.py`; judgement work (which concept, which
tag, what the claim is) is done by you.

**Design rule from the source method: never architect first.** Pull real data →
mine the questions people will actually ask → derive the schema from those
questions → ingest exactly one video → verify a timestamp by clicking it → only
then automate. See `references/schema-template.md`.

## Setup (once per wiki)

```bash
WIKI="/Users/kbg1023/DEV/my-llm-wiki"      # or any vault root
RAW="$WIKI/10. Raw Sources/youtube"
```

`yt-dlp` and `python` must be on PATH (both already are on this machine; on
Windows call `python`, not `python3`).

## Step 1 — Collect (deterministic)

```bash
python scripts/yt_wiki.py list "<channel or playlist URL>" --out "$RAW" --min-duration 120
```

Writes `videos.json` (id, title, duration, url), shorts excluded. Skip this step
for a one-off video and go straight to Step 3 with its URL.

## Step 2 — Mine expected questions (do this before any schema)

Read 3–5 of the collected titles plus one full transcript, then draft 15–25
questions a real user of this wiki would ask, split into:

- **정확 히트형** — the answer lives in one video at one timestamp.
- **교차 검색형** — the answer must be assembled from several videos.

Prefer the cross-search set: it is what a wiki does that a search box does not.
Show the list to the user and get agreement before writing `SCHEMA.md`. For a
team wiki this is the consensus step, not a formality.

## Step 3 — Derive `SCHEMA.md`

If `$WIKI/SCHEMA.md` does not exist, create it from `references/schema-template.md`,
filling `domain` and a 10–20 tag taxonomy **derived from the question list**, not
invented. If it exists, extend it — never rewrite silently.

The source rule that makes this pipeline worth running lives in the schema's
출처 규약 section: every synthesized claim carries video title, `watch?v=ID&t=Ns`,
start–end time, and a short verbatim quote. Keep it.

## Step 4 — Ingest exactly one video

```bash
VID=$(python scripts/yt_wiki.py next --out "$RAW")   # empty output = nothing to do, stop here
python scripts/yt_wiki.py fetch "$VID" --out "$RAW" --lang ko --window 45
```

`fetch` writes `$RAW/<id>.md`: YAML frontmatter (title, video_id, source_url,
channel, upload_date, duration, ingested date, sha256 of the caption file) and
~45-second blocks, each headed with `[HH:MM:SS–HH:MM:SS] <url>&t=Ns`. Use
`--trim-head/--trim-tail` seconds to drop intro/outro boilerplate, `--lang en`
when Korean captions are absent.

Raw files are immutable. Never edit them; they are the evidence layer.

Then, as the agent:

1. Read the raw file. Identify concepts that appear in 2+ sources **or** are
   central to this one. Passing mentions get no page.
2. Create/update `$WIKI/20. Wiki/<concept>.md` with frontmatter (type, tags from
   the declared taxonomy only, sources) and at least 2 outbound `[[wikilinks]]`.
3. Under each claim, write the 출처 line in the schema's format.
4. Append one line to `index.md` and one entry to `log.md`.
5. `python scripts/yt_wiki.py mark "$VID" --out "$RAW"`

## Step 5 — Verify before scaling

Ask the wiki one of the Step 2 questions. Open a returned `&t=Ns` link and check
the speaker is actually saying that there. If not, fix `SCHEMA.md`'s source rule
and re-ingest — do not patch the page by hand. Only after a clean verification
should more videos be ingested.

## Step 6 — Automate one per day

One video per run, on a schedule. Backlog drains slowly on purpose: when an
ingest goes wrong you can see which one broke it.

```
Use the youtube-wiki-ingest skill. Ingest one unprocessed video from
"$RAW/videos.json" into "$WIKI". If there is none, change nothing.
Report: new video count, pages created, pages updated, remaining backlog.
```

Register it with the scheduled-tasks MCP (or Hermes cron on a Hermes profile).
Never bulk-ingest 30 videos in one run.

## Report format

Always close a run with: 새 영상 수 / 만든 페이지 / 수정한 페이지 / 남은 영상 수 /
검증한 타임스탬프 1건.

## Files

- `scripts/yt_wiki.py` — list · next · fetch · mark · selftest (`python scripts/yt_wiki.py selftest`)
- `references/schema-template.md` — SCHEMA.md skeleton with the source rule
