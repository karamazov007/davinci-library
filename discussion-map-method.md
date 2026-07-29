# The Discussion Map — Method & Instruction Manual

A reusable system for having **long, deep, branching discussions** with an AI collaborator
without losing threads. Portable to any Cowork / project. This document is the spec.

---

## 1. The problem it solves

Your thinking is a **tree**; chat is a **line**.

A rich answer has many important points. You want to go deep on one — but that dive itself
branches, and by the time you surface, the *other* points from the original answer have scrolled
away and faded. They were never *resolved*; they were just *buried*. Two instinctive workarounds
both fail:

- **Rushing** through each point so it doesn't fade → kills the depth, which was the whole point.
- **Stopping to build a document/HTML mid-flow** → kills momentum and interest, costs too much time.

The fix is not more mental discipline. It's to **move the tree outside your head** into a
lightweight external structure, so your attention is free to go deep while the structure holds
breadth.

---

## 2. Core principles

1. **Externalize the tree.** A persistent file holds every branch so memory doesn't have to.
2. **Stable addresses.** Every point gets a permanent handle that never expires, so you can jump
   back to it 20 messages later with zero ambiguity.
3. **Depth without loss of breadth.** You can rabbit-hole freely because unexplored siblings are
   parked, visible, and safe.
4. **Lightweight, always-on.** Updating the map costs seconds and never interrupts flow.
5. **Separation of layers.** *Discussion navigation* (the map) is automatic and cheap. *Polished
   deliverables* (HTML, docs, decks) are built **only on explicit request** — never mid-flow.

---

## 3. The three components

**A. Numbered points.**
Every substantive reply carries a response ID (`D1`, `D2`, …) and numbers its key points
`【1】【2】【3】…`. To go deeper, you name the address ("go deep on **D2·3**"). Sub-discussions
nest as `D2·3a`, `D2·3.1`, etc.

**B. The map file.**
One markdown file (`<topic>-discussion-map.md`) kept in your folder, updated **silently in the
background** every turn. It is the tree: every thread as a node with an address, a one-line gist,
and a status marker. This is your durable memory — walk away for a week, open it, and you know
exactly where you were and what's still owed.

**C. The open-threads footer.**
Every substantive reply ends with a compact `🧵 Open threads` list — the branches still
unexplored — so you pick the next one without scrolling up. This is the guarantee that nothing
silently drops.

---

## 4. Addressing scheme

```
D2          → the 2nd substantive discussion-response
D2·3        → point 【3】 of that response
D2·3a       → a named sub-branch opened while discussing D2·3
D2·3.1      → a numbered child of that sub-branch
T1·x        → a node tied to an external artifact (e.g. Tab 1 of a built HTML page)
BUILD       → a pending "render this into a deliverable" node
```

Rule: **addresses never change and never expire.** Once assigned, `D2·3` points to the same idea
forever, even after hundreds of messages.

---

## 5. Status markers

| Marker | Meaning |
|--------|---------|
| ● | **closed** — discussed to satisfaction; build-ready |
| ◐ | **mid-discussion** — partially explored |
| ○ | **open** — raised or offered, not yet explored |

Status is the **build signal**: `●` nodes are ripe to render into a deliverable; `○` nodes would
render thin, so they wait.

---

## 6. The map file template

```markdown
# <Topic> — Discussion Map

A living tree of our conversation so nothing fades.

**How to use it**
- Numbered points in every answer: 【1】【2】…  · address like "D2·3"
- Status: ● closed · ◐ mid · ○ open
- Deliverables built only on explicit request; this file stays lightweight.

## ⚡ Open threads at a glance (pick your next branch)
- ○ **D1·4** — <one-line gist>
- ○ **D2·3** — <one-line gist>
- ○ **BUILD** — <what to render, when ready>

## The tree
### D1 — <topic of first response>
- ● **D1·1** — <gist>
- ◐ **D1·2** — <gist>
  - ○ **D1·2a** — <sub-branch gist>
- ○ **D1·3** — <gist>
    - ▸ (you) <a point or question you dictated into this node>

### D2 — <topic of second response>
- ● **D2·1** — <gist>
- ○ **D2·2** — <gist>

## 🎯 Cues / takeaways collected
1. "<a distilled takeaway from the discussion>"

---
*Structure only — full reasoning lives in chat. This map tells you where we are and what we owe.*
```

---

## 7. Operating rules (what the AI does every turn)

1. **Number** the key points of each substantive reply under a response ID.
2. **Update the map file silently** — add new nodes, update gists, flip statuses. No fanfare.
3. **End with the `🧵 Open threads` footer.**
4. **Never build polished HTML/docs unless explicitly asked.** The map is the only automatic
   artifact.
5. When a thread is discussed to satisfaction, **flip it to ●** so it becomes build-ready.
6. Pull from **both** the map (structure) and the live chat (depth) when eventually rendering —
   the map is the skeleton, the conversation is the substance.

---

## 8. User controls

- **Dictate into any node:** "add to **D2·3**: <points>" → placed there, tagged **▸ (you)** so your
  notes/questions stay distinct from the AI's synthesis.
- **New questions become nodes** automatically, marked ○ open.
- **Jump anywhere:** "back to **D1·7**" reopens that branch with full context.
- **Reorder / reprioritise:** ask, and the "Open threads at a glance" list is resequenced.
- **Collect cues/takeaways:** distilled one-liners accumulate in their own section.

---

## 9. The build bridge (map → deliverable)

The map is the **blueprint** for any later deliverable (HTML tab, doc, deck). When you say
"build X" or "render D3":

- Only `●` (or ripe `◐`) nodes are rendered — open nodes wait.
- Each concept becomes its own diagram/illustration + description; bullets where a list genuinely
  helps, prose where reasoning matters; sources where relevant.
- The richer the *discussion* was, the more the build is **translation, not invention.**

---

## 10. Adapting to any domain

This isn't specific to one topic. It fits any **long, multi-session, branching exploration**:
research projects, learning a hard subject, designing a system, writing a book, therapy-style
self-work, strategy. Wherever you'll have many nested conversations over time and don't want early
insights to evaporate, run a Discussion Map.

Minimal setup per project: one map file named for the topic, and the rules below active from
message one.

---

## 11. Bootstrap — paste this into a new Cowork to start

> **Run a "Discussion Map" for this project.**
> 1. Number the key points in every substantive reply as 【1】【2】… under a response ID (D1, D2…).
> 2. Maintain a markdown file `<topic>-discussion-map.md` in my folder; update it silently each turn.
> 3. Track every thread as a node with a stable address (e.g. `D2·3`), a one-line gist, and a status
>    marker (● closed · ◐ mid · ○ open). Sub-branches nest as `D2·3a`.
> 4. End every substantive reply with a compact `🧵 Open threads` footer.
> 5. I can dictate my own points/questions into any node — tag mine with **▸ (you)**. New questions
>    I ask become new ○ nodes.
> 6. Build polished HTML/docs **only when I explicitly ask**; keep the map lightweight.
> 7. When a thread is discussed to satisfaction, flip it to ● (build-ready). When I say "build", render
>    the ● nodes into the deliverable, pulling depth from our chat.

---

## 12. Cheat-sheet

| You want to… | Say… |
|---|---|
| Go deep on a point | "go deep on **D2·3**" |
| Return to a buried thread | "back to **D1·7**" |
| Add your own notes | "add to **D2·3**: …" |
| See what's left | (it's in the footer every turn) |
| Render a deliverable | "build tab ③" / "render **D3**" |
| Reprioritise | "move **D3·8** to the top" |

---

*Method summary: externalize the tree, give every idea a permanent address, keep a live map, surface
open threads every turn, and build deliverables only on demand.*
