# Nutrition — Discussion Map

A living tree of our nutrition conversation so nothing fades. Chat is linear; our thinking
branches. This file holds the branches — kept brief and token-light, ready to pour into the
**nutrition tab of `knowledge-hub.html`** (visually, with diagrams + structure) when you say so.

**How to use it**
- Every substantive answer has numbered points: 【1】【2】【3】…
- To go deeper, name the address — e.g. "go deep on **N2·3**" or "back to **N1·4**".
- Addresses never expire. Ten messages later, "N1·2" still points here.
- Status: ● closed · ◐ mid-discussion · ○ open (raised, not yet explored)
- This doc stays lightweight. Content only goes into the hub HTML when you explicitly ask.

**Standing constraints (from project memory)**
- North-Indian veg-leaning diet; eggs = primary animal protein. **Bananas medically restricted — never recommend.**
- First-principles, mechanistic only. Analogies supplement, never substitute. Blunt is fine.
- Visuals for the hub: full-width header rows, multi-column boxes, per-item status indicators; flowcharts for processes.

---

## 🎯 WORKFLOW (Satyam's instruction, 2026-08-11)
- **Log everything now (concepts + diagram specs/scripts); do the big "convert it all into visuals in the HTML" pass LATER, only when Satyam says.** Until then, keep discussing and recording; don't over-embed.
- **Visual style = the reference concept-map look** (circular ringed nodes + "+" badges, curved gradient edges, white pill labels, dotted bg). Reusable renderer: `nutrition-assets/concept_map.py` (raster-verify with cairosvg before embedding).
- **All diagram sources persisted in `nutrition-assets/`** (scratch is wiped between sessions): `concept_map.py/.svg/.png`, `routes_map.py/.svg/.png`, embed scripts `add_flowmap.py`, `add_math_topic.py`, `add_allocation.py`, `build_gym_tab.py`, retired `master_map.py`.
- **Embed target:** Gym / Body Comp tab → data model in `nutrition.html` (RAW blob inside `knowledge-hub.html`). New pretty diagrams go in as `genFlowMap`-style arg-less generator functions. Persistence caveat: the app can re-save the hub and revert edits — verify after embedding.

### 🔧 Child auto-layout fix (no overlapping expansions)
- Replaced hand-placed child offsets with **auto arc placement** (`_child_layout`): children fan OUTWARD from graph centroid on an arc, radius/angle scaled by child count → **guaranteed no child–child overlap** for any node in BOTH maps. Verified programmatically: 0 child-child, 0 child-main overlaps. (Fixes "Protein synthesis stacked its two bubbles".)

### 🧬 Protein Concept Map tab (BUILT 2026-08-11)
- New top-tab **"Protein Concept Map"** (🧬) beside Nutrition Concept Map. Same interactive full-bleed engine (now a **registry**: `NCM_MAPS={nutrition,protein}`, keyed by block's `map` field → `data-cmap`). Built from N8.
- Nodes: Dietary protein → Amino acids → **Gut + liver (first-pass toll)** → **Amino-acid pool** → {Protein synthesis → Muscle (MPS−MPB), Other molecules, Oxidised for fuel → Urea}; **Turnover river** (~250–300 g/day) loops back to pool; Muscle→Turnover (MPB); **Your target** (~140 g = 2 g/kg) off Dietary protein; **40 g meal** worked-example node. Each expands to detail children (first-pass %, leucine/MPS saturation, net ~3 g/day, RDA vs optimal, nitrogen balance, deaminate→urea, etc.).
- Engine refactored to `buildOne(root,D)` + `NCM_MAPS[key]`; block type now `data-cmap="<map>"`. Sources: `nutrition-assets/cmap_build_protein.py`, `cmap_protein_data.json`, updated `cmap_engine.js` + `cmap_embed.py`. Raster-verified collapsed + all-expanded. Tabs now 9; 42 figures still render; engine parses.

### 🕸️ Nutrition Concept Map tab (BUILT 2026-08-11)
- New top-tab **"Nutrition Concept Map"** (🗺️) added beside Gym / Body Comp. **Interactive** self-contained engine (`nutrition-assets/cmap_engine.js`): drag-pan, wheel-zoom, zoom slider, zoom ±, fit, **fullscreen**, and **click-the-+-to-expand** child detail nodes. Same concept-map aesthetic (circular ringed nodes, curved gradient edges, pill labels, dotted bg).
- Content: Food → (Carbohydrates / Protein / Fat) → digests to (Glucose / Amino acids / Fatty acids) → Insulin switch, Glycogen, Fuel pool, Muscle, Body fat, DNL, Deficit. Each main node has 1–3 expandable children (kcal/g, brain fuel, GLUT4, MPS gate, deaminate→urea, store ~3%, structural, DNL cost, BMR/NEAT/training, near-unlimited, ketones/gluconeogenesis, glucagon/adrenaline, etc.).
- Layout raster-verified (cairosvg) collapsed + all-expanded: `nutrition-assets/cmap_collapsed.png`, `cmap_all.png`. Data model: `cmap_data.json`. Embed script: `cmap_embed.py` (idempotent; injects CSS + engine + `cmap` block type + mount hooks + tab). All 42 figures still render; engine parses OK.
- **Spread-out layout (Satyam: use the full canvas, nothing hidden):** widened canvas to 1980×1360, respaced the crowded top-right cluster; **DNL now hangs off Glycogen** ("when full / fructose") instead of Glucose — de-clutters Glucose's fan-out and clears the label collisions with "promotes"/"raises". Raster-verified collapsed + all-expanded.
- **Full-bleed (Satyam's request):** map is NOT a boxed card — engine reparents a fixed overlay to `<body>` covering everything below the top tab bar (`--ncm-top` measured from `.htabs`), hides `.ntoc`, no border/box. Toolbar reduced to just the **zoom slider** (+ drag-pan, scroll-zoom, node **+** expanders); removed the −/+/fit/fullscreen/close buttons. `body.cmap-active` toggles on mount; overlay torn down on tab switch.
- ⏳ To deepen later: add more child layers (hormone cascade, mTOR/AMPK, tissue GLUT4 detail) as more nodes in `cmap_build.py` → re-run build + embed.

### 🗂️ Convert-to-HTML backlog (what to (re)build as visuals when Satyam gives the word)
- ✅ Already in tab: master metabolism concept map (`genFlowMap`), two-pool accounting, allocation switchboard + 3 dials, muscle = bricks+labour, training-fuel spectrum, plus the whole Gym tab (11 topics).
- ⏳ Pending embed: **N6 "Two routes to body fat"** (routes_map) → add to fat-loss/math topic; fold a **DNL / fructose** node into the master concept map.
- ⏳ Redo-as-pretty-concept-map candidates (currently genGraph/boxy): two-pool accounting, switchboard — optionally restyle to the circular look for consistency.
- ⏳ Any future N-branches with diagrams get added here as we go.

---

## ⚡ Open threads at a glance (pick your next branch)
- ○ **N2·4** — Nutrient partitioning / p-ratio: what actually shifts the deficit-draw toward fat vs muscle (protein, training, sleep, being a beginner)
- ○ **N2·5** — Recomp as the two-dials-cooperating case: energy for new muscle borrowed from fat stores — when/why it works
- ○ **N1·9** — Exact numbers pending Satyam's height / age / activity / body-fat % (blocks locking the "Your plan" tab numbers)
- ○ **N1·10** — Cut-first vs recomp: which path Satyam picks for 68→70kg
- ○ **N1·5** — Protein sources: how to realistically hit ~140g on veg+egg (paneer/soy/whey levers)
- ○ **BUILD·next** — Deep-dive each tab further (each is currently reference-depth); add per-topic discussion branches as we go

---

### N18 — Base protein from staples + the gap to fill (lunch/dinner)
- ● **Lunch base ≈ 17 g** (rice ~4 + 1½ dal ~11 + salad ~2) → need **~+18 g** pick (soy 15 / paneer 18 / chana 9 + curd). **Dinner base ≈ 13–14 g** (3 roti ~9 + veg ~3 + mango ~1.5) → need **~+21 g** pick (paneer 20 / soy 15 + egg / rajma 8 + whey/egg).
- ● Rule: staples quietly give ~15 g; the pick must add ~18–21 g → one BIG pick, or a medium pick + small helper.
- ● **BUILT** `genMealMath` into Meal Plan → "The day": bars showing staple base (coloured) + dashed-pink gap to ~35 g target, for lunch & dinner. 67 figures render.

### N17 — Trusted brands (India) + fake-paneer detection → Meal Plan "Trusted brands" topic
- **Web-verified (Aug 2026):** FSSAI/police drives on **analogue paneer** (veg oil + starch sold as milk paneer); Maharashtra mandates restaurants disclose analogue from May 2026; large seizures (Patiala ~1,300 kg, Lucknow–Agra ~4,810 kg).
- ● **Risk ranking:** Paneer HIGH · Curd LOW–MOD · Soya LOW · Chana/rajma/dal LOWEST. Paneer is the ONLY strict one; eggs/milk/whey/soya/dal low-risk.
- ● **Trusted brands:** Paneer/Curd → Amul · Mother Dairy · Nandini · Milky Mist · Gowardhan · Heritage (Greek curd: Epigamia, Nestlé a+ Grekyo). Soya → Nutrela · Fortune · Saffola · Urban Platter. Pulses → Tata Sampann (lab-tested) · 24 Mantra · Organic Tattva · Fortune.
- ● **Spot fake paneer:** smell/taste (sour/chemical/chalky=bad) · texture (rubbery/over-stretchy=analogue) · **iodine test** (boil+cool+iodine → blue-black = starch=fake) · label (made from milk + FSSAI no.; "analogue/non-dairy" = not paneer). Heuristic: sealed+branded+FSSAI+big dairy; cheap paneer = suspicious. Zero-worry route: soya+curd+eggs+whey.
- ● **BUILT:** Meal Plan "Trusted brands" topic (7th) — `genMealBrands` risk board + fake-paneer cards + buying-heuristic call. 66 figures render. Also updated breakfast → **4-egg omelette** (46g/780; day ~148g/2,460), and added **Heuristics** topic (1st) with `genMealHeur` 4-panel board.

### N16 — Meal plan tab + left-panel TOC fix
- ● **BUILT new tab "Meal Plan" (🍽️)** after You tab. Lean-bulk day ~2,390 kcal / ~142 g protein, 4 even feedings. Custom charts (`nutrition-assets/meal_charts.py` → genMealBars protein-per-meal, genMealTool ranked protein-per-serving toolbox colour-coded by group, genMealSwap before→after upgrades) + meal cards + itemised table + rules cards. Split into 4 topics (The day · Protein toolbox · Upgrade weak spots · Rules & flex). Embed `meal_tab_embed.py`.
- **Satyam's refinements baked in:** PB on 1 slice bread (no teeth-stick); curd 50 g not 100 g; kachumber salad named; whey rule = default 1 PW scoop, 2nd only on low-protein days (no 2+2); muesli OK if low-sugar; lunch/dinner "pick one" protein options with grams; on-the-go seeds/nuts.
- ● **N16·b — "Quick add-ons" topic** added to Meal Plan (5th TOC section): the "protein insurance" system — don't depend on what's cooked; keep always-ready add-ons and drop ONE onto any lunch/dinner. Custom chart `genMealAddons` (whey/paneer/soy/eggs/chana/curd/sprouts ranked, with no-cook/batch/quick prep badges) + toolkit cards + batch-prep note + lunch/dinner specifics + system call. Soy daily = batch-boil & toss (no curry); dinner fix = raw paneer / boiled eggs / chana chaat / whey. Dal already counts at lunch. Mealplan now 5 topics; 64 figures render.
- ● **TOC FIX (Satyam):** left panel = a tab's TOPICS. The You tab had 1 topic → 1 item. Added `split_topics()` splitting by section headings → **You tab now 9 topics** (Where you stand · Composition & reveal · Frame & arm · Cut or build? · Why a surplus builds · Follow the fuel · Calorie targets · Lean-bulk plan · Why you're stuck); Meal Plan 4 topics. Left panel now a real clickable TOC. 12 tabs, 63 figures render.

### N14 — Frame & arm potential (wrist/forearm/biceps measurements)
- **Measurements:** wrist 6.5″, forearm 11″ (thickest), biceps 12.7″ flexed.
- ● **N14·1 — Frame:** wrist 6.5″ at 5'9″ = **small-to-medium (slim-boned)**. Absolute natural ceiling modest → fully-built lean bodyweight potential ~**mid-70s kg** (aligns with build-to-72–74-then-cut plan). Wrist/ankle = classic natural-potential inputs.
- ● **N14·2 — Slim joints = aesthetic ADVANTAGE:** small wrist makes forearm/biceps look bigger by contrast; narrow waist + small joints = "sculpted" look. Steer toward proportion + leanness, not raw bulk.
- ● **N14·3 — Arm ratios:** biceps/wrist = 1.95× now (early-intermediate, ~avg+). Well-built natural ~2.3–2.5× → **target ~15–16″ arm** = ~+3″ runway over years. Growth mainly from big lifts (rows/chins/presses) + direct work in the surplus.
- ● **N14·4 — Game plan:** build shoulders + back (width flatters small waist) + arms; stay lean. Lean 72–73 kg with 15″ arms looks impressive ON his frame (joints stay small as muscle grows). Milestones: 13.5″ good · 14.5″ strong · 15–16″ excellent.
- ● **N14·5 — BUILT into "You · body & plan" tab** — "Your frame & arm potential" section: custom charts (`nutrition-assets/frame_charts.py` → genFrameScale wrist→small/med/large w/ YOU@6.5, genArmRunway 12.7″→~16″ with milestones + ratios) + measurement cards + calls. Tabs 11; 58 figures render.

### N15 — "If protein is constant, how does a surplus build muscle?" (the key mechanism)
- ● **N15·1 — Hidden wrong premise fixed:** the "~3 g net muscle" is NOT fixed — it's ENERGY-STATE dependent. Same 130 g protein → deficit ~0/negative · maintenance ~1 g · surplus ~2–4 g. Surplus flips MPS−MPB positive.
- ● **N15·2 — Muscle needs TWO things:** bricks (protein, constant) + permissive energy-rich anabolic environment (the surplus). Surplus doesn't BECOME muscle; it enables the bricks to be laid.
- ● **N15·3 — 4 mechanisms surplus works through:** (1) pays ATP cost of synthesis (deficit down-regulates expensive building); (2) **protein-sparing** — deficit burns more of your AAs for fuel; surplus spares them → more of 130g → muscle; (3) hormones tilt anabolic (insulin/T/IGF-1/leptin up, cortisol down); (4) fuels harder training (glycogen→overload) + recovery.
- ● **N15·4 — "extra carbs just become fat" = wrong:** most surplus carbs burned / →glycogen / spare protein (all anabolic work); only a bit → DNL. Dietary fat also = testosterone raw material. Surplus does anabolic labor.
- ● **N15·5 — Analogy:** protein=bricks; surplus=cash to pay the crew/lights/weather/rested-workers. Broke (deficit) → can't build, may sell bricks (burn protein). Small fat gain = the toll for the anabolic environment.
- ● **N15·6 — Ties to his plateau (N11):** stuck at maintenance = net ~0. Surplus is the missing lever; same protein then builds.
- ● **N15·7 — BUILT into "You · body & plan" tab** — "Why a surplus builds muscle" section: custom charts (`nutrition-assets/why_charts.py` → genNetByEnergy bar: same 130g → deficit −1 / maint +1 / surplus +3 g; genWhySurplus deficit-vs-surplus MPS/MPB panels fed by constant protein) + 4-lever cards + tie-to-plateau call.
- ● **N15·8 — Meaningful multi-flow Sankey (Satyam wanted the mechanisms mapped)** — `nutrition-assets/mech_sankey.py` (proper 3-column Sankey w/ ribbon ordering) + toggle (MECH_SVG/MECH_mount, block "mechflow"). Sources P/F/C → jobs (run body · train+recover · **ATP-to-BUILD** · hormone support · [fat store] · amino-acid pool) → outcomes (**MUSCLE-building** · spent/burned · [stored fat]). Toggle cut/maint/bulk: MUSCLE-building grows **97→159→270 kcal**, ATP+hormone ribbons thicken, protein constant 520, fat-store only in bulk. Muscle receives bricks(rose, thin)+ATP labour(violet)+hormones(green). Tabs 11; 60 figures render.

### N13 — Thumb rules: maintenance → lean bulk / cut (multipliers)
- ● **N13·1 — Maintenance (fast):** bodyweight(kg) × **30–33** (lbs ×14–15). Desk+gym ~30–31; active ~33; very active ~35+. Satyam 68kg → ~2,100 (×31, confirmed by stable weight). Then **scale is the real calculator** — flat 2 wks = maintenance; else ±150.
- ● **N13·2 — Multipliers off maintenance:** cut ×0.80 (−20%), gentle cut ×0.85, aggressive cut ×0.75 (high BF only); lean bulk **×1.10** (+10%, +200–300); aggressive bulk ×1.20 (skip, adds fat). Satyam: lean bulk ~2,310; standard cut ~1,680.
- ● **N13·3 — Rate check validates it:** bulk +0.25–0.5%/wk BW (~+0.2–0.35 kg); cut −0.5–1%/wk (~−0.35–0.7 kg). Faster bulk→trim 150; faster cut→add 150.
- ● **N13·4 — Constant across all:** protein ~1.6–2.2 g/kg (fixed rail); only carbs/fat flex. 
- ● **BUILT into "You · body & plan" tab** — new "Calorie targets" section: custom charts (`nutrition-assets/targets_charts.py` → genTgtDial multiplier dial ×0.75–1.20 w/ kcal, genTgtMacros stacked cut/maint/bulk showing protein RAIL constant + carbs/fat flex, genTgtRate weekly-weight-change gauge) + multiplier table. 56 figures render.
- ○ **N13·5** — NEXT: deep dive lean bulk, then cutting (macro setup, food choices, adjustments, plateaus).

### N12 — Satyam's body placement + plan (waist 32″) → BUILT "You · body & plan" tab
- **Stats:** 23 yr · 175 cm · 68 kg · BMI 22.2 (healthy) · waist 32″/81 cm · WHtR 0.46 (lean) · **~15% body fat** · lean mass ~58 kg.
- ● **Placement:** trains 4–5×/wk for ~5–6 mo, real definition when flexed (delts/traps/arms). NOT skinny-fat → **lean, athletic, early-intermediate; under-muscled for potential.** Missing piece = MUSCLE, not fat.
- ● **Definition = body-fat %, not scale weight.** Clear abs ~12–13% → he'd be **~65–66 kg** (LIGHTER, losing ~2–3 kg fat) with his current muscle. "Need 70 kg for definition" is backwards.
- ● **Two levers:** definition = fat↓ ; size = muscle↑. Goal physique = **~70–72 kg @ ~12–13%** reached by building ~5 kg muscle over 1–2 yr, THEN short cut.
- ● **Recommendation = LEAN-BULK now** (lean enough @15% + early trainee = prime build window; cutting now = smaller version). ~2,350 kcal (+250 over ~2,100 maint), protein ~130 g (already there), progressive overload, sleep, weigh weekly, 0.25–0.5 kg/mo. Fixes the maintenance plateau.
- ● **BUILT tab "You · body & plan" (🎯)** after Gym. Custom charts (`nutrition-assets/you_charts.py` → genYBodyFat spectrum w/ YOU@15% + target, genYMap composition scatter YOU→GOAL, genYReveal leaner=more-defined ladder) + native figs (genGraph cut/bulk fork, genTreemap lean-bulk macros, genTimeline 12-mo arc, genPyramid priorities) + stat cards + diet-audit table + calls. Embed `you_tab_embed.py`. Tabs now 11; 53 figures render.

### N11 — Satyam's ACTUAL diet audit + why he's stuck 2 months
- **His described daily diet:** 3 whey scoops/day (24g each = 72g), split 1.5+1.5 in 300ml milk ×2 (600ml milk total); 3 eggs (some days 6); lunch rice + potato sabzi + dal; dinner 2 roti + gourd veg (ridge/bitter/sponge gourd) + 1–1.5 mango. (Note: differs from old memory audit — no PB sandwiches/peanuts mentioned now.)
- ● **N11·1 — Protein estimate ~134g (3-egg) to ~150g (6-egg) ≈ 2.0–2.2 g/kg → GENEROUS, not deficient.** Whey stacked at 2 feedings (36g each, fine); lunch(~15g)/dinner(~8g) are the protein-poor meals → move protein THERE (paneer/soy/egg), not a 3rd shake.
- ● **N11·2 — Calories ~2,000–2,300 ≈ maintenance.** Proof: weight-stable 2 months = maintenance by definition.
- ● **N11·3 — Why "stuck" (no fat, no muscle, no definition):** he's at energy balance. No surplus → no gain; no deficit → fat not dropping → no new definition. Physics, not malnourishment. Recomp at maintenance is too slow to show.
- ● **N11·4 — Fix = pick a direction & leave maintenance.** For DEFINITION (his goal): small **cut** −300–400 kcal (trim mango to ½–1, less oil, 1 roti some nights), keep protein high, keep lifting, walk more. For SIZE: +250–300 surplus. Also: definition needs fat loss; growth needs progressive overload + sleep. Standardise eggs (~4–5/day).
- ● **N11·5 — Whey note:** 36g/sitting slightly above ~27g near-max (few g oxidised, not wasted); could even drop a scoop. 3×24g marginally better MPS frequency but total already ample.

### N10 — "Why eat 136 vs 109 if both deposit only ~3 g muscle?" (Satyam is right)
- ● **N10·1** — **Validated:** past ~1.6 g/kg, extra protein ≈ NO extra muscle (Morton et al. plateau). 109g vs 136g → same ~3g net muscle. Skepticism correct; the extra 27g is mostly first-pass + oxidation.
- ● **N10·2** — **Correction to "wasted → urea":** only the NITROGEN leaves as urea. The carbon skeleton is **burned for ATP** = ~4 kcal/g usable energy (~108 kcal from 27g). It becomes FUEL, not trash.
- ● **N10·3** — **Real (modest) reasons for the higher end — none are "more muscle":** (1) insurance — 1.6 is an average; aim 2.0 so bad days don't dip below the line; (2) satiety + TEF (~20-30% burned) → appetite/calorie control; (3) **cutting exception** — deficit raises breakdown, so 2.0–2.2 protects muscle (the real justification); (4) individual variation.
- ● **N10·4** — **Practical for Satyam (veg+egg, protein is hard macro):** ~**1.6 g/kg (≈109g)** captures ~95% of muscle benefit — nail that reliably. Push toward 2.0 mainly when **cutting** or for appetite control. Don't chase 136+ daily for a few g of oxidation.
- ● **N10·5** — Caveat: toggle Sankey held upkeep/other constant for readability; real higher intake nudges whole-body synthesis slightly, but net muscle still caps → conclusion unchanged.

### N9 — Protein dosing / MPS (0.4 g/kg meaning, ceilings, spreading) + new tab
- ● **N9·1** — **"0.4 g/kg" = g protein per kg BODYWEIGHT** (NOT per kg food). 68kg → ~27g/meal. g/day = g/kg × bodyweight.
- ● **N9·2** — **CORRECTION (Satyam caught it): 160g ≠ 12g deposited.** Don't multiply per-meal net by meals. TWO ceilings: (1) per-meal MPS caps ~0.4 g/kg (~25–30g) — "muscle full"; (2) per-DAY net muscle capped by biological growth rate (~2–4 g/day). Surplus = upkeep + fuel. Training + time drive deposition, not extra grams.
- ● **N9·3** — **Spreading:** each meal maxes MPS ~2–3h then falls back; needs a dip (~3–5h) before re-responding → 3–4 meals of ~0.4 g/kg beat 1 huge (maxes once) or 6 tiny (miss threshold).
- ● **N9·4** — **Training envelope:** workout raises/sensitises MPS ~24–48h; feedings during it hit harder. Near-daily training + regular protein = MPS chronically elevated over the week.
- ● **N9·5** — **Thumb rule:** RDA 0.8 (min, 54g) < optimal 1.6–2.2 g/kg (109–150g) ; cutting → ~2.2 (protect muscle).
- ● **BUILT — new tab "Protein · dosing & MPS" (🍳)** after pmap. Custom chart generators (`nutrition-assets/protein_charts.py` + `sankey136.py` → `genPCDose`/`genPCDaily`/`genPCTimeline`/`genPCSankey136`, raster-verified): (1) **MPS-vs-single-meal-dose** ceiling curve; (2) **136 g/day grams Sankey** (Satyam wanted grams not %): 136 → first-pass 34 g → {oxidised→urea 60, renew proteins/upkeep 28, other 11, NET muscle 3}; (3) **daily-intake plateau** (160≠12); (4) **MPS timeline over 48h** (training envelope + feeding spikes). Plus worked table + thumb-rule cards. Embed: `protein_tab_embed.py`. Tabs now 10; 46 figures render.
- ● **Interactive 4-goal toggle Sankey (Satyam request):** new `psankey` block + JS (`PSK_SVG`/`PSK_mount`, in PCJS block) + CSS (`/*PSKCSS*/`). Four toggle buttons — **Minimum 0.8 (54g) · Build 1.6 (109g) · Solid 2.0 (136g) · Cutting 2.2 (150g)** — each swaps to that goal's grams Sankey (same shared scale so totals are visually comparable; Minimum has no muscle band, Cutting shows a huge oxidation slab + muscle preserved). Source `nutrition-assets/sankey4.py` → `pc_sk4.json`; raster-verified `pc_sk4_verify.png`. Mounts via the same render hooks as the concept maps.

### N8 — PROTEIN, full mental model (start → end, with worked example)
- ● **N8·1** — **Anchor fact: protein has NO storage tank** (unlike glycogen pantry / fat freezer). All body protein is actively doing a job; only a tiny transient free-AA pool. ⇒ AAs not used promptly are **oxidised**, not saved.
- ● **N8·2** — **Turnover river:** body breaks down + rebuilds ~**250–300 g protein/day**, mostly **recycled**. Dietary ~100–140g just **tops up losses** + keeps the build signal on. Not filling an empty tank. (Analogy: workforce hired/laid off daily, can't stockpile.)
- ● **N8·3** — **Journey:** digest (pepsin/proteases → AAs) → portal to **liver first** → **first-pass toll ~20–50%** taken by gut (glutamine fuel) + liver (own/plasma proteins, urea disposal) → only ~25–30g of a 40g meal reaches circulation.
- ● **N8·4** — **3 fates of circulating AAs:** (1) build proteins (ALL tissues, muscle is big but not only); (2) burn — **deaminate → N as urea (urine)**, carbon → ATP / gluconeogenesis / (rarely) fat; (3) other molecules (creatine, neurotransmitters, glutathione).
- ● **N8·5** — **Muscle = MPS − MPB.** Leucine flips MPS on for a few hrs; **saturates ~0.4 g/kg/meal (~25–30g)** — extra oxidised. Training sensitises muscle 24–48h, amplifies MPS.
- ● **N8·6** — **Worked ex (40g post-training):** ~10–15g gut/liver first-pass; ~25–30g to circulation, maxes MPS (capped); **net new muscle ~1–3g** over hours; rest replaces turnover / other tissues / burned. You do NOT bank 40g into muscle → **spread protein 3–4 meals** to re-trigger MPS.
- ● **N8·7** — **~3g/day net vs 140g intake reconciled:** 0.5kg muscle/mo ≈ 100g protein/mo (muscle ~20% protein, 75% water) ÷30 ≈ **~3g/day NET**. 140g = **throughput** to keep MPS maxed + replace losses + cover first-pass/inefficiency. Small deposition, large flow — both true.
- ● **N8·8** — **140g target calc:** RDA 0.8 g/kg (68kg→~54g, just non-deficient) < optimal **1.6–2.2 g/kg** (68kg→~109–150; ~2.0→~136≈140) ; cutting → high end (~2.2) to protect muscle. Anchored to **bodyweight**, not %cal. Basis = **nitrogen balance** (protein ~16% N; +/0/− = build/maintain/lose). Maintenance still needs ~1.2–1.6 g/kg (turnover never stops).
- **Mental model one-liner:** no store → constant 250–300g/day recycle river; 140g tops up + keeps MPS firing; eaten protein taxed by gut/liver then split build/burn/other; each meal maxes MPS (spread it); training amplifies; net gain tiny (~3g/day) but throughput is the point.
- ○ **N8·9** — Candidate visual for tab: protein-fate flow (40g meal → first-pass toll → circulation → build/burn/other; MPS saturation curve; nitrogen balance).

### N7 — Fructose metabolism (correcting "fructose always → DNL → fat")
- ● **N7·0** — term fix: **DNL** = de novo lipogenesis (not "DNA").
- ● **N7·1** — **Satyam's claim wrong:** fructose does NOT skip glucose/glycogen and "always" become fat. Reality: fructose is a distinct monosaccharide, handled mainly by the **liver** (first-pass), **insulin-independent**, barely raises blood glucose/insulin directly.
- ● **N7·2** — **Liver fructose fates (roughly):** large share → **glucose** (released to blood); some → **lactate**; some → **liver glycogen**; a portion → **fat via DNL**. So it CAN become glucose & glycogen.
- ● **N7·3** — **Why fructose is more fat-prone than glucose:** fructokinase (KHK) rushes it past the PFK "brake" → enters glycolysis **unregulated**; liver-bound + insulin-independent; DNL propensity higher, esp. when dose large / liver glycogen full. → drives **NAFLD (fatty liver)** + high **triglycerides**. This is the map's "when full / fructose → DNL" edge.
- ● **N7·4** — **Practical:** whole fruit fine (modest dose + fiber slows it); problem = **large liquid/added fructose** (soda, juice, HFCS). "Body mobilises → fuel" = generic deficit reversal, not fructose-specific.
- **One-liner:** fructose → mostly liver → glucose/lactate/liver-glycogen/fat; not "always fat," but more fat-prone than glucose (unregulated, liver-bound, insulin-independent); worst when liquid & large.

### N6 — Getting fat: dietary fat vs carbs (which becomes body fat?)
- ● **N6·1** — **Q1 (dietary fat stored directly) = correct.** On a mixed diet in surplus, most NEW body fat = the dietary fat eaten, stored ~directly. Mechanism: carbs → insulin ↑ → (a) burn glucose first, (b) suppress fat oxidation → the meal's fat isn't burned, shunted to adipose. Storing dietary fat is cheap (~3% energy lost).
- ● **N6·2** — **Q2 (do carbs convert to fat?) = yes, but usually minor.** Pathway = **de novo lipogenesis (DNL)**. Small on normal diets because: carbs burned first, surplus tops up glycogen (~400–500g tank), and glucose→fat is costly (~25% lost). DNL significant only when: glycogen full + chronic carb overfeed, OR high **fructose/sugar** (hepatic DNL → liver fat/NAFLD); alcohol similar.
- ● **N6·3** — **Reconciliation:** carbs mostly make you fat *indirectly* (burned → spare dietary fat → fat stored); direct carb→fat (DNL) stays small until carb-stuffed/fructose-heavy. **Law: body fat comes from a CALORIE SURPLUS, any source — source changes route & efficiency, not outcome.**
- ● **N6·4** — Visual delivered: "Two routes to body fat" concept map (dietary fat → direct/cheap; carbs → spare fat, or → DNL if glycogen full/fructose → costly). `outputs/routes_map.py`.
- ○ **N6·5** — Candidate to add into the Gym tab (fat-loss or math topic) + fold DNL/fructose node into the master map as the next deeper layer.

### N5 — Master metabolism map (the big exhaustive start-to-end diagram)
- ● **N5·1** — Built a single **master flow map** (`genFlowMap`, programmatic, raster-verified for overlaps via cairosvg): foods (carb/protein/fat) → molecules → insulin switch → per-macro fates → shared FUEL POOL + 3 stores (glycogen/muscle/body-fat) → deficit reversal band. Shows the key mechanisms Satyam asked for: insulin ✕ blocks fat-burn & reroutes dietary fat to storage; protein "training signal?" gate (YES→MPS→muscle, NO→deaminate→urea + fuel); glucose→burn and →glycogen.
- ● **N5·2** — Embedded as the OPENING visual of Gym → "The math / accounting" ("The whole picture — one map"). 42 page figures render clean.
- ○ **N5·3** — **ITERATE deeper (Satyam wants exhaustive):** candidate additions — glucose surplus→de-novo-lipogenesis/fat-sparing; ketones/gluconeogenesis in deficit; hormonal layer (glucagon, cortisol, adrenaline, leptin); mTOR/AMPK/leucine detail on the protein gate; per-tissue GLUT4; TEF; brain's obligate glucose. Add layer by layer.
- ● **N5·4 — REDESIGNED (Satyam: boxy version looked awful).** Rebuilt as a proper **concept map** matching his reference style: circular ringed nodes + "+" badges, curved gradient edges, white pill labels, dotted background. Reusable renderer `outputs/concept_map.py` (raster-verified via cairosvg to kill edge/label overlaps). Embedded as `genFlowMap`, replacing the boxy one, at top of "The math / accounting". Nodes: Food · Glucose · Amino acids · Fatty acids · Insulin · Glycogen · Fuel pool · Muscle · Body fat · Deficit.
- Source scripts: `outputs/concept_map.py` (pretty renderer+raster), `outputs/add_flowmap.py` (embed), `outputs/master_map.py` (old boxy, retired).
- **Renderer is reusable** → future deeper layers (surplus/DNL, ketones/gluconeogenesis, hormone layer, mTOR/AMPK) get added as more circular nodes in the same style.

### N4 — How the body DECIDES fuel-vs-building-block allocation (partitioning mechanism)
- ● **N4·1** — **Not sequential.** No daily "fuel takes its lot, leftovers → storage." Allocation is **concurrent + continuous**: at any instant some cells burn glucose while others store it. Decided cell-by-cell, minute-by-minute.
- ● **N4·2** — **Three live dials:** (1) cellular energy charge (AMPK low-energy→burn / mTOR high→store-build); (2) hormones — insulin (fed) = store & build, suppresses fat-burn; glucagon/adrenaline/cortisol (fasted/deficit) = mobilise & burn; (3) tissue demand + tank space.
- ● **N4·3** — **Tank facts:** glycogen = small fixed tank (~100g liver + ~400g muscle), fills fast, overflows. Fat = ~unlimited tank. **Muscle protein = NO storage tank** (use-it-or-lose-it).
- ● **N4·4** — **Carb cascade:** 1 burn for ATP (brain ~120g/day obligate) → 2 top up glycogen (insulin) → 3 overflow to fat (surplus only; direct DNL limited in humans — more often carbs burned → dietary fat stored instead = "fat-sparing").
- ● **N4·5** — **Protein cascade (the key case):** no store → build now where there's a demand signal (muscle = recent **training** ↑ uptake+MPS+leucine/mTOR) OR deaminate → N→urea (out), carbon skeleton burned / →glucose. Why protein must be daily & why same protein = muscle in trained / fuel in untrained.
- ● **N4·6** — **Fat cascade:** fed/high-insulin → mostly stored (fat-burn suppressed, carbs burned preferentially) + small structural (membranes/hormones); deficit/fasted → mobilised & burned.
- ● **N4·7** — **Each store = own bricks + own switch:** glycogen←glucose (insulin+empty tank) · fat←fatty acids/excess (insulin/surplus) · muscle←amino acids (**training**).
- **Visual delivered (chat):** allocation switchboard (master insulin switch + 3 macro priority cascades).
- ● **ADDED to Gym tab:** "How the split is decided" section folded into the existing **"The math / accounting"** topic (after the equations) — switchboard rebuilt with genGraph + 3 "dials" cards + each-store-switch callout. themath now 15 blocks / 4 figures; all 41 page figures render clean; existing 6 tabs untouched. (No new tab, per Satyam.)

### N3 — The math: calories, macros, muscle building, training fuel (mechanistic)
- ● **N3·1** — **Core fix: energy is fungible, material is NOT.** Every macro has two roles: FUEL (calories → one shared ATP/substrate pool, powers anything) and MATERIAL (bricks, macro-specific: protein→amino acids→muscle; carb→glucose→glycogen; fat→fatty acids→membranes). Body does NOT tag "protein calories → muscle."
- ● **N3·2** — **Equations.** Intake: C_in = 4·P + 4·C + 9·F. Expenditure: C_out = BMR + TEF + NEAT + training. Balance: C_in − C_out = Δstored, where Δstored = 9·Δfat + 4·Δglycogen + 4·Δmuscle-protein (water ~0 kcal). The law nothing overrides.
- ● **N3·3** — **Muscle build needs two things:** bricks = amino acids (only protein) + labor = ATP (shared pool, mostly carbs/fat). net muscle = ∫(MPS − MPB)dt.
- ● **N3·4** — **Why 140g protein ≠ 140g muscle:** 1 kg muscle ≈ 200 g protein + 750 g water. Gaining 0.5 kg/mo = ~100 g protein/mo ≈ ~3 g/day net deposited. Tiny vs intake; the rest is burned/recycled. High intake keeps MPS maxed + covers inefficiency.
- ● **N3·5** — **Training fuel (a set):** 0–10s ATP-PC → 10s–2min anaerobic glycolysis = muscle glycogen (CARBS) dominant → fat rises at rest/after. Lifting ≈ carb-fueled; protein/fat minimal during sets.
- ● **N3·6** — **Verdicts on Satyam's hypotheses:** "protein calories → muscle" = half-right (amino-acid *material* becomes muscle & stores ~4 kcal/g; but assembly energy = ATP from carbs/fat, and most protein is fuel/recycled). "training burns carbs" = correct.
- **Visuals delivered (chat widgets):** (1) two-pool accounting, (2) muscle = bricks+labor + MPS−MPB, (3) training fuel-by-duration bar.
- ● **ADDED to Gym tab:** new topic **"The math / accounting"** (inserted after "big picture") rebuilt with the page's own generators (genGraph accounting, genGraph muscle build, genSpectrum training fuel) + equation/verdict callouts. All 40 page figures render clean; existing 6 tabs untouched. Gym topics now 11.

### N2 — Reading the "master switch" diagram: two questions
- ● **N2·1** — **"Calories out" = total daily expenditure (TDEE), not the food you ate.** It runs continuously regardless of intake. Satyam correct: in a deficit you burn *all* the food PLUS draw the shortfall from stored energy (mostly fat; some glycogen early; some muscle if unprotected). You can't erase intake — you out-spend it by tapping reserves.
- ● **N2·1a** — Cue/model: **fat = a battery.** Deficit = running on battery (draining). Surplus = charging. Maintenance = plugged in, drawing exactly what you use.
- ● **N2·2** — **Protein+training vs calories: NOT "no relation" — correction.** Energy balance = *how much* total mass changes; protein+training = *what it's made of* (**nutrient partitioning**). Calories set direction; the 2nd dial steers which tissue moves (surplus → fat vs muscle; deficit → strip muscle vs spare it).
- ● **N2·3** — **Three couplings** (why not fully independent): (1) protein *is* calories (4 kcal/g → counts as "in"); (2) protein has highest TEF (nudges "out" up); (3) training burns energy (nudges "out" up). But they **don't override the law** — no net tissue gain in a deep deficit / no fat loss in a big surplus by protein alone. They ride on top.
- ● **N2·3a** — Exception where dials interact: **recomposition** — beginner in a small deficit builds muscle using energy borrowed from fat stores. Why "fat→muscle" *feels* true though it isn't a conversion.
- **Takeaway model:** two dials, mostly independent — *calories = how much · protein+training = made of what* — with minor cross-talk.

---

## 🏗️ BUILD LOG
- ⚠️ **Correction (my mistake):** first pass I misread "it's already built" and created a *separate* nutrition page, trying to replace the whole nutrition blob — wrong. The real nutrition page (6 tabs: Overview · Energy & Metabolism · Macronutrients · Micronutrients · Body Systems · Medical Terms) already existed embedded in the hub. That original was left intact; nothing lost.
- ● **Correct integration:** added ONE new top-tab **"Gym / Body Comp"** (🏋️) into the existing nutrition page's `var DATA` model, in its native block schema (p/h/fig/call/cards/table), reusing the page's own vizlib generators. Existing 6 tabs verified content byte-identical; palette unchanged. New tab = 10 left-TOC topics: big picture · energy balance · maintenance & activity · setting macros · fat loss · muscle building · muscle↔fat · strength training · diet lenses · your plan (68kg). 23 figures, all render clean. Re-embedded as nutrition.html RAW blob; standalone `nutrition.html` also written. Builder: `outputs/build_gym_tab.py`.
- 🔁 **Persistence note:** an earlier hub edit reverted ~16s later (the app appears to re-save the hub, clobbering external edits). If the new tab vanishes after reload, the app rewrote the file — flag it and re-apply (ideally with the hub closed).

- ● **Nutrition tab built** → standalone `nutrition.html` (left-rail TOC + 11 tabbed panels, flat scrollable, colour-coded per concept: energy=indigo, protein=rose, carbs=cyan, fat=orange, fiber/veg=green, recomp/strength=violet). Reuses `src/vizlib.js` generators (26 diagrams: mindmap, treemap, sankey, spectrum, venn, concentric, cycle, graph-flows, timeline, pyramid, radar, matrix + prebuilt genRecomp/genBodyType). Embedded into `knowledge-hub.html` as the `nutrition.html` RAW blob (rawDeflate+base64, roundtrip verified); 🥗 Nutrition card now opens it. Hub backed up: `knowledge-hub.backup-nutrition-20260811-004358.html`.
- Tabs: Overview · Energy balance · Maintenance & activity · Macronutrients · Fiber & micros · Fat loss · Muscle building · Muscle↔fat · Strength training · Diet lenses · Your plan (68kg). Veg lens woven into each topic (per Satyam's choice).

---

## The tree

### N1 — Body recomposition: calories, macros, how to set up a diet (68kg, fat→muscle goal)
- ● **N1·1** — **Reframe:** fat ≠ muscle; they don't convert. "Recomp" = two separate processes at once: *fat loss* (needs energy deficit) + *muscle gain* (needs training + protein + energy). They pull opposite directions → recomp is possible but slow; easiest for beginners / returnees / higher body-fat (body funds muscle from its own fat). Expect scale flat while body changes.
- ● **N1·2** — **Master switch = energy balance.** TDEE = BMR(60–70%) + TEF(~10%, protein highest) + NEAT + EAT. Intake < TDEE → lose; = → hold; > → gain. Calories set *direction*; macros set *quality*.
- ● **N1·3** — **Order of operations (the missing mental model):** (1) find TDEE; (2) set calories vs TDEE by goal — cut −15/20%, recomp ≈maintenance, lean gain +10% (bigger surplus just adds fat); (3) protein first in g/kg; (4) fat as a floor in g/kg; (5) carbs = leftover calories; (6) % is an *output*, checked last.
- ● **N1·4** — **Why g/kg > %:** percentages float with total calories (30% = different grams at 2000 vs 2600). Anchor protein & fat to bodyweight; % (~30P/25-30F/40-45C) just falls out.
- ◐ **N1·5** — **Macro rules of thumb:** protein 1.6–2.2 g/kg (high end when cutting, protects muscle); fat floor 0.6–1.0 g/kg (hormones, vit A/D/E/K, cell membranes); carbs = flex, training fuel + protein-sparing. Fat = 9 kcal/g, protein/carb = 4.
- ● **N1·6** — **Formulas:** BMR(men)=10×kg+6.25×cm−5×age+5; TDEE=BMR×activity(1.2/1.375/1.55/1.725).
- ● **N1·7** — **Worked example (assumed 175cm/27yr/moderate → TDEE~2400, P~140g, F~55-65g):** Cut ~2000 (150P/55F/226C); Recomp ~2400 (140P/60F/325C); Lean-gain→70kg ~2600 (140P/65F/365C).
- ● **N1·8** — **Sources (veg+egg):** protein weak point — 6 eggs ~36g, 600ml milk ~20g, dal/peanuts/roti; levers = paneer, soy chunks, whey. Fat easy (watch overshoot). Carbs = rice/roti/bread/potato, time around training.
- ○ **N1·9** — Exact numbers pending height/age/activity/body-fat.
- ● **N1·10** — **"68→70" cue:** chase composition not scale (scale can't separate fat/muscle/water/glycogen). Signals: waist, lift progression, mirror. Real muscle gain ~0.25–0.5 kg/month max → 2kg = multi-month. Path A: cut lean → then lean-gain. Path B: recomp at maintenance, protein ~150g, scale stays flat for weeks.

## N19 — Meal Plan: Swaps, portions & cost + protein-fraction column (build log)
- Toolbox chart: added a right-hand **fraction-of-weight** column (soy ≈ 1/2, whey 4/5, paneer 1/5, Greek curd 1/10, egg 1/8, green peas 1/20, etc.), colour-graded, with a worked-example caption. Fractions, not percentages, per Satyam's request. Lets him eyeball protein = weight × fraction.
- New left-panel topic **"Swaps, portions & cost"** in Meal Plan tab:
  - `genMealSimple` — fixed-vs-add daily board: eggs+whey+milk = automatic (green); soy@lunch, eggs/pick@dinner = the only "add" moves (amber); whey+milk (or water) = universal plug; day ≈ 137 g.
  - Pick-portions table — grams of each pick for ~15 g / ~20 g top-up (soy 30/40, paneer 75/100, chana 1½/2 katori, rajma, tofu 180/250, Greek curd 150/200, eggs 2–3/3–4, whey ½/1).
  - Backup cards: whey+milk = forgot-the-pick plug; 3 eggs@dinner = the pick (6 eggs/day safe); don't over-optimise; soy daily / paneer a treat.
  - `genMealCost` — cost per gram of protein ranked bar (Rs): soy 0.5 → dal/chana ~0.6 → milk 0.9 → eggs 1.1 → paneer 1.7 → whey 2.7 → branded Greek yogurt 6.0. Budget engine = soy+dal+eggs+milk; paneer/whey = premium.
- Verified: 9/9 meal gens valid; toolbox raster clean; sources copied to nutrition-assets/.

## N20 — Meal Plan: the "value map" (density vs price scatter)
- New `genMealValue` scatter added to "Swaps, portions & cost" topic: X = cost per gram of protein (Rs, cheaper left), Y = protein density (% of food's weight, denser up). Top-left green zone = best (dense+cheap), bottom-right red = worst.
- Points: soy (0.5, 52%) alone in the green corner = everyday base; whey (2.7, 80%) densest but pricier; dal/chana/rajma/peanuts/eggs cluster = good-value volume; paneer (1.7, 20%) mid; branded Greek yogurt (6.0, 10%) stranded bottom-right. Value cue + cost cue added.
- Verified: 10/10 meal gens valid; scatter raster clean; sources → nutrition-assets/.

## N21 — Meal Plan: veg-protein tiers + "18 g looks like…"
- `genMealLooks`: every bar = same 18 g protein, length = grams of food needed. Soy 35 g → green beans 1 kg (~28×). Colour by tier (engine rose / support blue / decoration slate).
- `genMealTiers`: 3-tier board — ENGINE (soy·paneer·eggs·whey·tofu·curd) / SUPPORT (dal·chana·rajma·moong·masoor) / DECORATIONS (broccoli·beans·peas·sabzi), each with a why-line. Core insight: concentrated protein beats two ceilings at once — stomach volume + calorie budget.
- Added to "Swaps, portions & cost" topic as "Why soy, paneer & eggs win" with tier cue. 12/12 meal gens valid; rasters clean; sources → nutrition-assets/.

## N22 — Meal Plan: "Your 3 daily non-negotiables" core card (now first topic)
- `genMealCore`: 3 pillar cards — Eggs (6/day ~36g, DAILY), Soya (40g dry ~20g, DAILY, ~Rs12), Paneer (90–100g ~18–20g, SWAP, ~Rs35) with ⇄ swap between soya↔paneer; summary formula ≈140 g/day; decoration banner.
- Inserted as new FIRST left-panel topic "Daily core" in Meal Plan (topics now: core·heur·day·toolbox·swaps·rules·quickadd·brands·swapcost). 13/13 meal gens valid; raster clean; sources→nutrition-assets/.

## N23 — Protein toolbox: full "18 g looks like" for every toolbox food
- `genMealLooksAll`: 16 toolbox foods, each bar = 18 g protein, length = grams of that food to eat. Sorted asc: whey 22g → soy 35 → pumpkin seeds 60 → PB/peanuts 72 → almonds 86 → paneer 90 → flax/chia 100 → eggs 150 (3) → greek curd 180 → chana/rajma 200 (2 katori) → tofu 225 → dal 230 → moong 260 → green peas 360 (3+ katori). Colour by group.
- Added into "Protein toolbox — pick your swaps" topic under genMealTool (the flip-side of the fraction column). 14/14 meal gens valid; raster clean; sources→nutrition-assets/.
