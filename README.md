# Da Vinci — Personal Library

A single, self-contained knowledge hub gathering ~4 months of notes into one place:
personality, social mastery, swimming, the brain as a system, media, systems thinking,
workout, nutrition, humor, sports mindset, cricket, NCR outings, travel and board games.

Everything lives in one file — **`knowledge-hub.html`** — which embeds every section,
diagram and page. Open it in a browser (best from the hosted site; works locally too).

## Structure

- `knowledge-hub.html` — the built, self-contained app (open this)
- `src/build_master.py` — the generator that assembles the hub from the sources below
- `src/vizlib.js` — the SVG diagram library used across sections
- `src/templates/` — the section apps (humor, workout, cricket, sports mindset, nutrition)
- `src/data/` — structured content: taxonomies, checklists, café/venue data, nutrition data
- `src/assets/` — images (source boards)
- `src/embeds/` — original framework pages embedded into sections

## How it's built

`build_master.py` reads the templates, data and section pages, injects the diagram
library and content, and writes `knowledge-hub.html`. Build paths are specific to the
authoring environment; this repo is the versioned record of the work.

## Focus

Actively worked on: Minimum Viable Personality · Social Mastery · Swimming.
The rest are structured references, revisited as needed.
