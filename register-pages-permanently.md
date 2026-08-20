_Paste this into the Cowork session that builds the knowledge hub (the one whose `build_master.py` regenerates `knowledge-hub.html`) — the same session used to add the Offsite and Sopranos tabs._

---

The generated `knowledge-hub.html` keeps **dropping three pages every time you rebuild**, because they aren't in your build's page list. They exist as finished HTML files but you regenerate the manifest without them, so their nav items vanish. Please register them **permanently** so rebuilds keep them.

**The three pages** (finished files, committed in the `davinci-library` repo root):

| id | file | name | icon |
|----|------|------|------|
| `comm` | `communication.html` | Communication | 💬 |
| `grapevine` | `company-grapevine.html` | Company Grapevine | 🍇 |
| `content` | `content-creation.html` | Content Creation | 🎬 |

**What to do in `build_master.py`:**

1. Open `build_master.py` and find the `TOP_PAGES` list (the tuples of `(id, relpath, display name, icon, blurb)` — the same list that holds `mvp`, `social`, `swimming`, etc.).
2. Add these three entries, **matching the exact `relpath` convention your other standalone pages use** (i.e. the path is relative to your `BASE`, wherever the build reads page source from). If these three files aren't already under that `BASE`, copy them there first from the `davinci-library` repo root.

```python
    ("comm",      "<path-under-your-BASE>/communication.html",     "Communication",     "💬", "Talking to people — declining cleanly, bakaiti, the operating system, and building how you conduct yourself."),
    ("grapevine", "<path-under-your-BASE>/company-grapevine.html", "Company Grapevine", "🍇", "A trusted insider plus the first-principles of workplace influence, visibility, sponsorship, referrals and building an app."),
    ("content",   "<path-under-your-BASE>/content-creation.html",  "Content Creation",  "🎬", "Blueprints for content I'd love to make — starting with a cinematic history of the Indian subcontinent."),
```

3. Rebuild the hub and commit.

**Important — don't overwrite these files' contents.** `communication.html`, `company-grapevine.html`, and `content-creation.html` in the repo are the source of truth and contain lots of hand-built sections (Personality Building, Talking & connecting, the Operating System, Build an App, the Grapevine theory, etc.). Register them and embed them **as-is**; do not regenerate their inner content from a template.

Also, two pages in `my-learnings.html` — the **Time Approximation** and **I Know a Guy / Do What You Can · My Life Philosophy** sections — and the **Home "Do What You Can · My Life Philosophy"** sub-tab were hand-added the same way. If your build regenerates `my-learnings.html` or the Home shell from its own source, please pull those additions in from the repo versions too, so they stop getting reverted.

After this, a rebuild should keep all of them, and we won't have to re-wire them by hand again.
