# Da Vinci Library — Overnight Build Status & Resume Guide

**Goal:** every personality guide reaches ~100 detailed, specific, well-SOURCED events.
The number is not arbitrary padding — these lives genuinely had 100+ important events.
Capture the concrete texture: names, dates, places, numbers, the actual chain of what
happened (e.g. for Arnold: Marnul → army AWOL → Reg Park blueprint → 1966 loss to
Chet Yorton → Munich stone-lift → 1967 Mr Universe + Reg Park's South Africa invite →
Weider's call + Miami loss to Zane → 1969 Oliva loss → 1970 double win → mind games →
1980 comeback). RESEARCH each figure with WebSearch/WebFetch before writing.

## Quality standard (per event)
- Use the `E(id, time, title, tags, summary, svg, bg, people, what, crux, conseq, matters)` helper.
- 6 branches: bg / people / what / crux / conseq / matters — packed with SPECIFIC sourced facts.
- One concept-map SVG via `svg_row` / `svg_stack` / `svg_compare` (from engine).
  - `svg_row(title, boxes, edge_labels=None, takeaway, accent)` and `svg_compare(...)` take edge_labels/verdict.
  - `svg_stack(title, boxes, takeaway, accent)` does NOT take edge_labels.
- Escape apostrophes with the typographic ’ (U+2019) inside single-quoted Python strings; escape & as &amp; only in raw SVG `<text>` (helpers auto-escape).
- Living/modern figures: research from current sources; be accurate; present controversy fairly / both-sides.

## Resume procedure (fresh session / after container recycle)
1. `ls /home/claude/greats/assemble.py` — if missing, restore:
   stage `/Users/satyam/Documents/GitHub/davinci-library/_generator_backup.tar.gz` from the device,
   then `mkdir -p /home/claude/greats && tar -xzf <staged> -C /home/claude/greats`.
2. Pick the guide with FEWEST events under 100 (see counts below), OR build a NEW queued figure.
3. Research → add ≥10 detailed sourced events (edit the content_*.py; for new figures write a full
   content_<name>.py with build_meta(), then register in assemble.py (import + GUIDES dict) and add a
   landing card in landings.py with ready:True and the right group).
4. Validate: import the module, render_guide, parse every `<svg>` with xml.dom.minidom — proceed only if 0 bad.
5. `python3 assemble.py` → `cp knowledge-hub.new.html deliver/knowledge-hub.html`.
6. SendUserFile the delivered file; device_commit_files it to
   `/Users/satyam/Documents/GitHub/davinci-library/knowledge-hub.html` (force=true).
7. Refresh backup tarball and commit it to `_generator_backup.tar.gz`. Repeat. Never ship an unvalidated/broken file.

## Existing guides — event counts (target 100 each) — updated
hideyoshi 14, qinshihuang 14, subutai 15, nobunaga 16, cleopatra 17, augustus 18, hannibal 20,
lky 20, jobs 21, musk 21, sengoku 22, lincoln 23, suleiman 23, lenin 28, selim1 28, stalin 28,
tamerlane 28, ashoka 29, ieyasu 29, carnegie 30, churchill 30, akbar 32, arnold 32, genghis 32,
mehmed2 32, caesar 35, alexander 42, napoleon 45.  (28 guides now exist.)

## NEW figures still to BUILD (Round-1 guide, then deepen to 100)
Marco Polo, Miyamoto Musashi, Zhuge Liang, Chandragupta Maurya, Chanakya,
Emperor Wu of Han, Tang Taizong, Kangxi Emperor, Otto von Bismarck, Talleyrand, Cardinal Richelieu,
Metternich, Casanova, Rodrigo Borgia (Alexander VI), Giovanni de' Medici (Leo X), Antoine-Henri Jomini,
B. H. Liddell Hart, Deng Xiaoping, Henry Kissinger, Lyndon B. Johnson, Robert Moses, John D. Rockefeller,
Warren Buffett & Charlie Munger, Bernard Arnault, Michael Jackson.
(Already built this run: Hannibal, Augustus, Cleopatra, Nobunaga, Hideyoshi, Subutai, Qin Shi Huang.)

## PENDING repo commit
If the device bridge was down when guides were built, the latest knowledge-hub.html and
_generator_backup.tar.gz may be one or more versions ahead in the CONVERSATION (delivered via
SendUserFile) vs the repo. When the bridge returns, re-assemble and commit to sync the repo.

## Groups for landing cards
Ancient Greats / European Greats / Asian Greats / Ottoman Sultans / Indian Greats / Modern Greats.
