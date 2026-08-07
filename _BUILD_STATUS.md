# Da Vinci Library — Build Status & Resume Guide

**Goal:** deep, visual life-guides; each figure reaches genuinely-researched, well-SOURCED events.

## >>> STRATEGY: DEPTH-FIRST, one at a time (per the user) <<<
The user switched from breadth-first to DEPTH-FIRST: take ONE personality all the way to
≥100 genuinely-researched, SOURCED events before moving to the next. No vague filler — real names,
dates, places, numbers (Wikipedia, Shiji/Book of Han, biographies, open sources).

Method that works well (proven on Arnold & Liu Bang):
1. Launch 5–6 parallel general-purpose subagents, each researching ONE life-phase and writing a
   self-contained part-file `content_<name>_pN.py` exposing `EVENTS = [E(...), ...]` — each part
   file does `from engine import svg_row, svg_stack, svg_compare, esc`, defines its own local E()
   helper and AC accent, and validates its own SVGs (xml.dom.minidom) → 0 bad.
2. Main content file does `from content_<name>_pN import EVENTS as PN` and adds one timeline tab per
   part (or appends PN into an existing phase list, e.g. `PHASE_X + PN`).
3. For a NEW figure, also write OVERVIEW_HTML, WHO, KEY_EVENTS, MASTER, SOURCES + build_meta, and
   register in assemble.py (import + GUIDES dict) and landings.py (correct group).
4. Validate whole guide (render_guide, parse every <svg>, check no duplicate ids), then assemble,
   deliver, commit + refresh backup AFTER EACH FIGURE (recycle costs at most one figure).

## Quality / SVG rules (per event)
- `E(id, time, title, tags, summary, svg, bg, people, what, crux, conseq, matters)`.
- 6 branches packed with specific sourced facts; one SVG via svg_row / svg_stack / svg_compare.
- svg_row/svg_compare take edge_labels/verdict; **svg_stack does NOT take edge_labels**.
- Apostrophes as typographic ’ (U+2019) in single-quoted strings. SOURCES = 2-tuples (name,url).
- Living/contested figures (e.g. Modi): present controversy fairly / both sides.

## DONE depth-first
- **Arnold Schwarzenegger — 106 events** (was 32; +74 via content_arnold_p1..p5, merged into phases).
- **Liu Bang / Emperor Gaozu of Han — 109 events** (NEW; content_liubang.py + content_liubang_p1..p6;
  registered in assemble.py + landings.py under "Asian Greats").
- **Oda Nobunaga — 120 events** (was 16; +104 via content_nobunaga_p1..p6, merged into phases).
- **Toyotomi Hideyoshi — 114 events** (content_hideyoshi_p1..p6). REBUILT after a sandbox revert wiped it.
- **Babur — 108 events** (content_babur_p1..p6). REBUILT after a sandbox revert wiped it.
- **Shivaji — 113 events** (content_shivaji_p1..p6). REBUILT after a sandbox revert wiped it.

## Hub features added
- Search box on the Great Men landing (engine.py render_landing + SEARCH_JS; filters cards by
  name/place/era/role, matches blurbs, collapses empty groups).
- Refresh persistence: the viewer's current page (incl. guides reached via the __dvhNav bridge) is
  saved to localStorage 'khub.viewer' and restored on load (assemble.py DVH_NAV + DVH_DEEP).
- Master Timeline is now AUTO-GENERATED from every timeline event (engine.py: master tab with
  'auto': True rebuilds rows from all events) — it can never drift from the events again.
  The six depth-first guides have 'auto': True set on their master tab.

## !! SANDBOX REVERT WARNING
This cloud session has repeatedly rolled the filesystem back to earlier snapshots, silently deleting
newly-created content_*_p*.py part-files and un-wiring mains. ALWAYS re-verify event counts in the
freshly-ASSEMBLED knowledge-hub.new.html (decompress gm-*.html, count class="ev") before trusting a
build, and verify the backup tar actually contains the part-files (tarfile.getnames) before committing.
Consider running this task "on your computer" (desktop app) to avoid the ephemeral-disk reverts.

## Library state
- 90 guides total, organised into 12 thematic categories (Ancient Greats, Religious Founders,
  Sages/Poets & Philosophers, European Greats, Asian Greats, Ottoman Sultans, Indian Greats,
  Independence & Nation-Building, Statesmen & Politicians, Diplomats & Strategists,
  Business & Industry, Artists & Filmmakers) + Great Eras (Sengoku).

## NEXT depth-first target
Ask the user which personality is next. Easiest high-quality exemplars to push to 100:
Napoleon (45→100), Alexander (42→100), Julius Caesar (35→100). Thinly-documented figures
(Buddha, Patanjali, Kalidasa, Nagarjuna): target "as deep as the sources truly allow," not a forced 100.

## Resume after container recycle — ALWAYS restore fresh (recycles happen; container reverts)
1. Stage `/Users/satyam/Documents/GitHub/davinci-library/_generator_backup.tar.gz`, then
   `rm -rf /home/claude/greats && mkdir -p /home/claude/greats && tar -xzf <staged> -C /home/claude/greats`.
   Backup is self-sufficient (includes *.txt). Verify: `cd /home/claude/greats && python3 assemble.py` → VERIFY OK.
   NOTE: the backup does NOT contain this .md file (backup globs *.py *.txt only) — recreate it if missing.
2. `cp knowledge-hub.new.html deliver/knowledge-hub.html`; SendUserFile; device_commit_files (force) →
   `/Users/satyam/Documents/GitHub/davinci-library/knowledge-hub.html`.
3. Refresh backup (MUST include *.txt): `tar -czf /home/claude/greats_generator_backup.tar.gz --exclude=__pycache__ *.py *.txt package.json package-lock.json hub_original.html node_modules/pako` → commit `_generator_backup.tar.gz` (force).
