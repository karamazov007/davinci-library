_Paste this into the Cowork session that builds the knowledge hub (the one whose `build_master.py` regenerates `knowledge-hub.html`) — same session used for Communication, Company Grapevine, Content Creation._

---

New standalone page to register **permanently** in `build_master.py`'s `TOP_PAGES` list, same as `comm` / `grapevine` / `content`.

**The page** (finished file, committed in the `davinci-library` repo root):

| id | file | name | icon |
|----|------|------|------|
| `findcontent` | `finding-content.html` | Finding Content | 🔎 |

**What to do in `build_master.py`:**

1. Copy `finding-content.html` from the `davinci-library` repo root into wherever `BASE` reads standalone page source from, matching the same `relpath` convention as `communication.html` etc.
2. Add this entry to `TOP_PAGES`:

```python
    ("findcontent", "<path-under-your-BASE>/finding-content.html", "Finding Content", "🔎", "How to actually find things — Telegram (and any platform) as a discovery ecosystem: channel networks, search architecture, hashtags-as-database, bots, and a personal media-library infrastructure."),
```

3. Rebuild the hub and commit.

**Important — don't overwrite this file's contents.** `finding-content.html` in the repo is the source of truth: 14 sections, all-visual (SVG diagrams + inline sidebar nav), covering the full Telegram discovery framework — object types, the object-vs-ecosystem mistake, search architecture, channel networks, the broaden-then-narrow technique, filtering good channels, bots and their risks, internet↔Telegram discovery, hashtags as a database, personal infrastructure (folders + Saved Messages), the end-to-end pipeline, the legal/ethical boundary, and a five-level learning roadmap. Register and embed it as-is; do not regenerate its inner content from a template.

This is a living page — expect follow-up edits/additions as Satyam refines the discovery model in conversation.
