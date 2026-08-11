# -*- coding: utf-8 -*-
import re, json, zlib, base64, os

REPO="/sessions/lucid-blissful-curie/mnt/davinci-library"
HUB=os.path.join(REPO,"knowledge-hub.html")

# colours (match page palette)
E="#4f46e5"; P="#db2777"; Cb="#0891b2"; F="#ea580c"; Fi="#16a34a"; V="#9333ea"; Am="#d97706"; Ink="#1c2431"; Sl="#64748b"

# ---- block helpers ----
def p(x): return {"t":"p","x":x}
def h(x): return {"t":"h","x":x}
def call(x): return {"t":"call","x":x}
def cards(items): return {"t":"cards","items":items}
def table(head,rows): return {"t":"table","head":head,"rows":rows}
def fig(gen,cap,args): return {"t":"fig","gen":gen,"cap":cap,"args":args}

# ---- figures (reused from mount.js, hex inlined) ----
def g(nodes,edges,w=700,hh=420): return [nodes,edges,{"w":w,"h":hh}]

ov_machine=fig("genGraph","The master switch: energy balance sets gain vs lose; protein + training set muscle vs fat.",
  g([{"id":"in","x":0.09,"y":0.42,"label":"Calories\nIN","fill":E,"w":96,"h":52},
     {"id":"out","x":0.34,"y":0.42,"label":"Calories OUT\n(TDEE)","fill":Sl,"w":120,"h":52},
     {"id":"gap","x":0.58,"y":0.42,"label":"The gap","fill":Am,"shape":"diamond","w":104,"h":64},
     {"id":"lose","x":0.88,"y":0.2,"label":"LOSE\nweight","fill":F,"w":96,"h":50},
     {"id":"gain","x":0.88,"y":0.62,"label":"GAIN\nweight","fill":Fi,"w":96,"h":50},
     {"id":"qual","x":0.34,"y":0.86,"label":"Protein +\nTraining","fill":P,"w":120,"h":50}],
    [{"from":"in","to":"out"},{"from":"out","to":"gap"},
     {"from":"gap","to":"lose","label":"deficit","color":F,"lc":F},
     {"from":"gap","to":"gain","label":"surplus","color":Fi,"lc":Fi},
     {"from":"qual","to":"lose","label":"keep muscle","color":P,"lc":P,"curve":40,"dash":"5 4"},
     {"from":"qual","to":"gain","label":"build muscle","color":P,"lc":P,"dash":"5 4"}],700,420))

ov_mindmap=fig("genMindMap","Five systems: energy balance, macros, training, fiber & micros, and the goals they combine into.",
  ["Nutrition",[
    {"label":"Energy balance","children":["TDEE","Deficit","Surplus"]},
    {"label":"Macros","children":["Protein","Carbs","Fat"]},
    {"label":"Training","children":["Tension","Overload","Recovery"]},
    {"label":"Fiber & micros","children":["Gut","Satiety","Vitamins"]},
    {"label":"Goals","children":["Cut","Recomp","Lean gain"]}],{"w":800,"h":560}])

en_treemap=fig("genTreemap","BMR (staying alive) dominates; NEAT (daily movement) is the swing factor; TEF is the digestion tax, highest for protein.",
  [[{"label":"BMR — staying alive","weight":65,"color":E},
    {"label":"NEAT — daily movement","weight":15,"color":Fi},
    {"label":"EAT — exercise","weight":10,"color":V},
    {"label":"TEF — digestion","weight":10,"color":P}],{"w":700,"h":420}])

en_spectrum=fig("genSpectrum","Where you sit vs maintenance sets direction; the size of the gap sets speed (and collateral muscle/fat).",
  ["DEFICIT · lose","SURPLUS · gain",
   [{"pos":0.1,"label":"Aggressive cut\n-25%","color":F},
    {"pos":0.3,"label":"Cut\n-15/20%","color":F},
    {"pos":0.5,"label":"Maintenance","color":Ink},
    {"pos":0.72,"label":"Lean gain\n+10%","color":Fi},
    {"pos":0.92,"label":"Dirty bulk\n+25%","color":Am}],
   {"w":780,"h":280,"title":"Size of the gap = speed"}])

en_sankey=fig("genSankey","At maintenance, intake is fully spent on these. Surplus is stored; a deficit is pulled from fat (and muscle if protein/training are missing).",
  ["Calories eaten",
   [{"label":"Basal / organs (BMR)","value":65,"color":E},
    {"label":"Everyday movement (NEAT)","value":15,"color":Fi},
    {"label":"Exercise (EAT)","value":10,"color":V},
    {"label":"Digestion (TEF)","value":10,"color":P}],{"w":740,"h":420}])

mn_flow=fig("genGraph","Body stats -> BMR (Mifflin-St Jeor) -> x activity multiplier -> TDEE / maintenance.",
  g([{"id":"w","x":0.08,"y":0.2,"label":"Weight","fill":Sl,"w":92,"h":40},
     {"id":"ht","x":0.08,"y":0.5,"label":"Height","fill":Sl,"w":92,"h":40},
     {"id":"a","x":0.08,"y":0.8,"label":"Age · sex","fill":Sl,"w":92,"h":40},
     {"id":"bmr","x":0.42,"y":0.5,"label":"BMR","fill":E,"w":120,"h":56},
     {"id":"act","x":0.68,"y":0.5,"label":"x Activity","fill":Am,"shape":"diamond","w":110,"h":60},
     {"id":"tdee","x":0.9,"y":0.5,"label":"TDEE\n(maintenance)","fill":Fi,"w":120,"h":56}],
    [{"from":"w","to":"bmr"},{"from":"ht","to":"bmr"},{"from":"a","to":"bmr"},
     {"from":"bmr","to":"act"},{"from":"act","to":"tdee"}],700,400))

mn_activity=fig("genSpectrum","Pick honestly. Most desk-workers who train 3-4x/week are ~1.4-1.55, not 1.7.",
  ["1.2 · sedentary","1.9 · athlete",
   [{"pos":0.0,"label":"Desk, no gym\n1.2","color":Sl},
    {"pos":0.25,"label":"Light 1-3x\n1.375","color":Cb},
    {"pos":0.5,"label":"Moderate 3-5x\n1.55","color":Fi},
    {"pos":0.75,"label":"Hard 6-7x\n1.725","color":V},
    {"pos":1.0,"label":"Physical job\n1.9","color":Am}],
   {"w":780,"h":280,"title":"Over-picking is why a cut stalls"}])

mc_mind=fig("genMindMap","Fixed colours: protein = rose, carbs = cyan, fat = orange.",
  ["Macros",[
    {"label":"Protein","children":["Amino acids","Muscle (MPS)","Satiety","High TEF"]},
    {"label":"Carbs","children":["Glucose","Glycogen","Fuel","Fiber"]},
    {"label":"Fat","children":["Hormones","Cell walls","Vit A/D/E/K","Essential FAs"]}],{"w":780,"h":560}])

mc_order=fig("genGraph","Lock protein -> set a fat floor -> carbs fill the rest. The % is a read-out, not the plan.",
  g([{"id":"pr","x":0.12,"y":0.5,"label":"1 · Protein\ng per kg","fill":P,"w":120,"h":56},
     {"id":"ft","x":0.38,"y":0.5,"label":"2 · Fat\nfloor g/kg","fill":F,"w":120,"h":56},
     {"id":"cb","x":0.63,"y":0.5,"label":"3 · Carbs\nremainder","fill":Cb,"w":120,"h":56},
     {"id":"pct","x":0.88,"y":0.5,"label":"4 · % =\nread-out","fill":Ink,"shape":"rect","w":110,"h":56}],
    [{"from":"pr","to":"ft"},{"from":"ft","to":"cb"},{"from":"cb","to":"pct"}],720,220))

mc_protein=fig("genGraph","Protein -> amino acids -> MPS. You grow when MPS outpaces breakdown (MPB); training + protein tilt it.",
  g([{"id":"prot","x":0.08,"y":0.55,"label":"Protein\n(food)","fill":P,"w":100,"h":50},
     {"id":"aa","x":0.32,"y":0.55,"label":"Amino\nacids","fill":Sl,"w":92,"h":50},
     {"id":"train","x":0.32,"y":0.14,"label":"Training","fill":V,"w":100,"h":44},
     {"id":"mps","x":0.6,"y":0.3,"label":"MPS\nbuild","fill":Fi,"w":96,"h":48},
     {"id":"mpb","x":0.6,"y":0.8,"label":"MPB\nbreak","fill":F,"w":96,"h":48},
     {"id":"net","x":0.9,"y":0.55,"label":"Net\nmuscle","fill":P,"w":96,"h":52}],
    [{"from":"prot","to":"aa"},{"from":"aa","to":"mps"},{"from":"aa","to":"mpb","dash":"4 4"},
     {"from":"train","to":"mps","label":"signal","color":V,"lc":V},
     {"from":"mps","to":"net","label":"+","color":Fi,"lc":Fi},
     {"from":"mpb","to":"net","label":"-","color":F,"lc":F}],720,420))

mc_carb=fig("genGraph","Carbs -> glucose -> insulin stores it as glycogen or burns it now. Only a chronic surplus routes the excess to fat.",
  g([{"id":"carb","x":0.08,"y":0.5,"label":"Carbs","fill":Cb,"w":92,"h":48},
     {"id":"glu","x":0.34,"y":0.5,"label":"Glucose\n(blood)","fill":Sl,"w":100,"h":50},
     {"id":"gly","x":0.7,"y":0.24,"label":"Glycogen\nfuel store","fill":Fi,"w":110,"h":50},
     {"id":"burn","x":0.7,"y":0.55,"label":"Burned\nnow","fill":E,"w":100,"h":48},
     {"id":"fat","x":0.86,"y":0.86,"label":"Fat\n(surplus only)","fill":F,"w":110,"h":48}],
    [{"from":"carb","to":"glu"},
     {"from":"glu","to":"gly","label":"insulin","color":Am,"lc":Am},
     {"from":"glu","to":"burn","label":"energy"},
     {"from":"glu","to":"fat","label":"surplus only","color":F,"lc":F,"dash":"4 4","curve":30}],720,420))

mc_fat=fig("genSpectrum","Type is a spectrum: trans = harmful; unsaturated (nuts, oils, eggs) = protective; saturated from whole foods is fine in moderation.",
  ["TRANS · avoid","UNSATURATED · best",
   [{"pos":0.05,"label":"Trans\nfried/packaged","color":F},
    {"pos":0.34,"label":"Saturated\nmoderation","color":Am},
    {"pos":0.68,"label":"Mono\nolive, peanuts","color":Fi},
    {"pos":0.95,"label":"Poly · Omega-3\nfish, walnuts","color":Cb}],{"w":780,"h":280}])

fl_cycle=fig("genCycle","Deficit -> insulin falls -> lipolysis releases fatty acids -> burned (beta-oxidation) -> fat cell shrinks -> repeat.",
  [[{"label":"Calorie\ndeficit","note":"eat < TDEE"},
    {"label":"Insulin\nfalls","note":"storage off"},
    {"label":"Lipolysis","note":"fat released"},
    {"label":"Fatty\nacids","note":"into blood"},
    {"label":"Beta-\noxidation","note":"burned -> ATP"},
    {"label":"Fat cell\nshrinks","note":"repeat"}],{"w":620,"h":560,"center":"Fat loss"}])

fl_where=fig("genGraph","Most fat leaves as CO2 you exhale, the rest as water. You literally breathe your fat out.",
  g([{"id":"fat","x":0.1,"y":0.5,"label":"Stored fat\ntriglyceride","fill":F,"w":110,"h":52},
     {"id":"burn","x":0.42,"y":0.5,"label":"Burned with\noxygen","fill":E,"w":120,"h":52},
     {"id":"co2","x":0.8,"y":0.26,"label":"CO2\nexhaled","fill":Cb,"w":100,"h":50},
     {"id":"h2o","x":0.8,"y":0.74,"label":"Water\nurine/sweat","fill":Sl,"w":110,"h":50}],
    [{"from":"fat","to":"burn"},
     {"from":"burn","to":"co2","label":"~84%","color":Cb,"lc":Cb},
     {"from":"burn","to":"h2o","label":"~16%"}],700,380))

fl_timeline=fig("genTimeline","Week 1's big drop is mostly water/glycogen; then a steady grind, an inevitable plateau, and a small adjustment.",
  [[{"when":"Wk 1","label":"Big drop\nwater/glycogen"},
    {"when":"Wk 2-5","label":"Steady\nfat loss"},
    {"when":"Wk 6","label":"Plateau\nadaptation"},
    {"when":"Wk 7","label":"+steps /\n-150 kcal"},
    {"when":"Wk 8+","label":"Loss\nresumes"}],{"w":780,"h":420}])

ms_balance=fig("genGraph","Muscle = synthesis (MPS) - breakdown (MPB). Training raises MPS; protein supplies material; net positive = growth.",
  g([{"id":"eat","x":0.1,"y":0.3,"label":"Protein","fill":P,"w":100,"h":46},
     {"id":"train","x":0.1,"y":0.72,"label":"Training","fill":V,"w":100,"h":46},
     {"id":"mps","x":0.46,"y":0.3,"label":"MPS up\nbuild","fill":Fi,"w":104,"h":50},
     {"id":"mpb","x":0.46,"y":0.72,"label":"MPB\nbreak","fill":F,"w":104,"h":50},
     {"id":"net","x":0.82,"y":0.5,"label":"Net growth\nif MPS>MPB","fill":P,"w":120,"h":56}],
    [{"from":"eat","to":"mps"},{"from":"train","to":"mps","color":V},
     {"from":"mps","to":"net","label":"+","color":Fi,"lc":Fi},
     {"from":"mpb","to":"net","label":"-","color":F,"lc":F}],720,400))

ms_cycle=fig("genCycle","Stress the muscle -> recover (this is when you grow) -> adapt -> add a little next time.",
  [[{"label":"Train\ntension","note":"stimulus"},
    {"label":"Fatigue","note":"micro-damage"},
    {"label":"Recover","note":"sleep + food"},
    {"label":"Adapt","note":"grow back bigger"},
    {"label":"Add load","note":"progress"}],{"w":620,"h":560,"center":"Overload"}])

rc_recomp=fig("genGraph","Not a conversion - a redistribution run by two independent dials. The scale can barely move while the body changes.",
  g([{"id":"now","x":0.1,"y":0.5,"label":"Now\nlow muscle\n+ central fat","fill":Sl,"w":118,"h":64},
     {"id":"musc","x":0.5,"y":0.22,"label":"Build muscle up","fill":Fi,"w":140,"h":48},
     {"id":"fat","x":0.5,"y":0.78,"label":"Shed fat down","fill":F,"w":140,"h":48},
     {"id":"goal","x":0.88,"y":0.5,"label":"Recomposition","fill":Fi,"w":140,"h":56}],
    [{"from":"now","to":"musc","label":"train + protein","color":Fi,"lc":Fi},
     {"from":"now","to":"fat","label":"deficit","color":F,"lc":F},
     {"from":"musc","to":"goal"},{"from":"fat","to":"goal"}],720,420))

rc_matrix=fig("genMatrix","Your body-fat x muscle position points to the smart move: cut, lean-gain, or recomp.",
  ["Body fat  ->","Muscle  ->",
   {"tl":{"title":"Lean & muscular","items":["Lean-gain to grow","or maintain"]},
    "tr":{"title":"Big but soft","items":["Cut to reveal it"]},
    "bl":{"title":"Skinny","items":["Lean-gain / eat more","build first"]},
    "br":{"title":"Skinny-fat","items":["Recomp","or short cut, then gain"]}},{"w":700,"h":560}])

st_pyramid=fig("genPyramid","Consistency > progressive overload > enough volume > hard-enough sets > exercise choice > the small stuff.",
  [[{"label":"Tempo · rest · hacks","sub":"minor"},
    {"label":"Exercise selection"},
    {"label":"Intensity (near failure)"},
    {"label":"Enough volume"},
    {"label":"Progressive overload"},
    {"label":"Consistency / adherence","sub":"foundation"}],{"w":700,"h":460}])

st_reps=fig("genSpectrum","All rep ranges build muscle if taken near failure - the bias shifts: low->strength, mid->size, high->endurance.",
  ["HEAVY · few reps","LIGHT · many reps",
   [{"pos":0.12,"label":"1-5 reps\nstrength","color":V},
    {"pos":0.48,"label":"6-12 reps\nhypertrophy","color":P},
    {"pos":0.85,"label":"15+ reps\nendurance","color":Cb}],{"w":780,"h":280,"title":"Near failure is what counts"}])

dt_radar=fig("genRadar","Further out = easier/better on that axis. No diet wins everything.",
  [["Protein ease","Fiber","Micros (B12/iron)","Fat quality","Omega-3","Cost / ease"],
   [{"name":"Vegetarian","color":Fi,"vals":[0.55,0.95,0.55,0.7,0.4,0.8]},
    {"name":"Mediterranean","color":Cb,"vals":[0.7,0.85,0.9,0.95,0.9,0.6]},
    {"name":"Non-veg","color":P,"vals":[0.95,0.5,0.9,0.7,0.8,0.55]}],{"w":640,"h":560}])

you_protein=fig("genTreemap","Your staples get you most of the way; the labelled levers close the gap to ~140g without changing how you eat.",
  [[{"label":"Paneer / soy / whey","weight":44,"color":V},
    {"label":"6 eggs","weight":36,"color":P},
    {"label":"Dal + roti","weight":24,"color":Fi},
    {"label":"600 ml milk","weight":20,"color":Cb},
    {"label":"2 PB sandwiches","weight":16,"color":F}],{"w":700,"h":420}])

# ---- topics ----
topics=[
 {"id":"bigpicture","name":"The big picture","blurb":"Calories set direction; protein + training set what you become.","blocks":[
   p("Your body runs on an <b>energy budget</b>. Eat under it and you shrink; eat over it and you grow. <b>Which tissue</b> you gain or lose — fat or muscle — is decided by <b>protein</b> and <b>resistance training</b>, not by the calories alone."),
   ov_machine,
   call("<b>The one cue.</b> Calories = direction. Protein + lifting = quality. Everything else is detail."),
   h("The territory, one map"),
   ov_mindmap,
   cards([{"h":"Direction — energy balance","x":"Intake vs TDEE. Deficit → lose, surplus → gain. The non-negotiable law."},
          {"h":"Quality — protein + training","x":"Tell the body to keep/build muscle while the scale moves."},
          {"h":"Health floor — fiber & micros","x":"Gut, satiety, and the vitamins/minerals that keep the machine running."}])]},

 {"id":"energy","name":"Energy balance","blurb":"Intake vs TDEE - the law of direction.","blocks":[
   p("Your weight is a running total of <b>energy in</b> (food) minus <b>energy out</b> (everything you burn, called <b>TDEE</b>). The gap, over time, is what changes on the scale."),
   h("Where your daily burn actually goes"),
   en_treemap,
   h("The one dial: deficit ↔ surplus"),
   en_spectrum,
   cards([{"h":"~7,700 kcal","x":"≈ 1 kg of body fat."},
          {"h":"−500 / day","x":"≈ 0.5 kg fat lost per week."},
          {"h":"+250 / day","x":"a lean-gain surplus — slow, clean."}]),
   h("How the calories you eat get spent"),
   en_sankey,
   call("<b>Common trap.</b> The “out” side isn’t fixed — eat less for weeks and NEAT quietly drops and BMR eases down. That’s the plateau, and why crash deficits stall.")]},

 {"id":"maintenance","name":"Maintenance & activity","blurb":"The intake where weight holds - your anchor number.","blocks":[
   p("“Maintenance calories” = the intake where your weight holds. It’s your <b>BMR</b> scaled up by how much you move. Nail this and every goal is just “this ± a bit.”"),
   h("How to build the number"),
   mn_flow,
   cards([{"h":"BMR (men) = 10·kg + 6.25·cm − 5·age + 5","x":"Women use −161 instead of +5. This is the “engine idling” cost before any movement."}]),
   h("Activity raises the number"),
   mn_activity,
   call("<b>How activity adds calories.</b> A hard gym hour ≈ 300–500 kcal. The bigger lever is <b>NEAT</b> — steps, standing, fidgeting — which can swing 400–800 kcal/day. “Walk more” beats “cardio harder.”"),
   call("<b>Cue.</b> Estimate maintenance, then let the scale correct it: weigh daily, average weekly. Flat = found it; drifting = adjust ~150–200 kcal.")]},

 {"id":"macros","name":"Setting your macros","blurb":"Protein, carbs, fat - and how to split them for a goal.","blocks":[
   p("Three nutrients carry energy: <b>protein</b>, <b>carbohydrate</b>, <b>fat</b>. Calories decide direction; <b>how you split these three</b> decides whether you keep muscle, train well, and feel full."),
   cards([{"h":"Protein — 4 kcal/g","x":"Builds & repairs; most filling."},
          {"h":"Carbs — 4 kcal/g","x":"Training fuel."},
          {"h":"Fat — 9 kcal/g","x":"Dense; runs hormones."}]),
   h("What each macro is for"),
   mc_mind,
   h("How you set them (order of operations)"),
   p("Never chase percentages first — they float with your calorie total. Anchor protein & fat to <b>bodyweight in grams</b>; carbs get the rest."),
   mc_order,
   table(["Macro","Set it to","Why","Veg + egg sources"],
     [["Protein","1.6–2.2 g/kg","Protects/builds muscle; most filling; highest TEF","eggs, milk, paneer, dal, soy, whey"],
      ["Carbs","the remainder","Training fuel; spares protein; fiber lives here","rice, roti, oats, potato, fruit"],
      ["Fat","0.6–1.0 g/kg floor","Hormones, cell walls, absorbs vit A/D/E/K","eggs, peanuts, PB, oil, milk"]]),
   h("Protein — the mechanism"),
   mc_protein,
   call("<b>Veg lens · protein.</b> Plant proteins are often “incomplete” (dal low in methionine, rice/wheat low in lysine). Combine across the day (dal+rice, roti+milk) and it evens out. Eggs, milk, paneer, soy, whey are complete. Hitting ~140g on veg+egg is the real challenge — paneer/soy/whey are the easy levers."),
   h("Carbs — the mechanism"),
   mc_carb,
   call("<b>Carbs are not the enemy.</b> Surplus calories make you fat, not carbs. Carbs fill glycogen so you train hard, and are “protein-sparing” — the body burns them instead of chewing up muscle."),
   h("Fat — quality over quantity"),
   mc_fat,
   call("<b>Don’t cut fat too low.</b> Below ~0.5 g/kg, testosterone and other hormones suffer and you stop absorbing fat-soluble vitamins. Fat is a floor, never zero.")]},

 {"id":"fatloss","name":"Fat loss","blurb":"How stored fat is actually spent - and what a real cut looks like.","blocks":[
   p("Fat loss is your body <b>spending its own stored energy</b> to cover a shortfall. Fat cells don’t vanish — they <b>empty and shrink</b>."),
   h("The mechanism, step by step"),
   fl_cycle,
   h("Where does the fat actually go?"),
   fl_where,
   h("What a real cut looks like over time"),
   fl_timeline,
   cards([{"h":"Protect muscle","x":"High protein + keep lifting. In a deficit the body strips muscle too — unless you give it a reason (training) and the bricks (protein)."},
          {"h":"The plateau","x":"Burn drops as you shrink (less mass, less NEAT). Fix: add steps or trim ~150 kcal — don’t slash harder."}]),
   call("<b>Cue.</b> Modest deficit, high protein, keep lifting, walk more. Slow fat loss keeps muscle; crash diets burn both.")]},

 {"id":"muscle","name":"Muscle building","blurb":"Challenge, feed, rest - and why it is slow.","blocks":[
   p("Muscle grows when you repeatedly <b>challenge it</b> (mechanical tension), then <b>feed and rest</b> it. Growth is the body over-building to be ready for next time. It is <b>slow</b> — and that’s normal."),
   h("The core balance: build vs break"),
   ms_balance,
   h("The engine: progressive overload"),
   ms_cycle,
   cards([{"h":"0.25–0.5 kg / month","x":"Realistic natural muscle gain, good case."},
          {"h":"1.6–2.2 g/kg","x":"Daily protein target."},
          {"h":"+10% calories","x":"A lean-gain surplus — no more."}]),
   call("<b>Reality check.</b> A bigger surplus doesn’t build muscle faster — it just adds fat faster. Beyond a small surplus, the extra is storage."),
   call("<b>Veg lens · building.</b> Works fine on veg+egg — the only lever needing attention is <b>total protein</b>. Front-load eggs/milk/paneer/soy; a whey scoop closes most gaps.")]},

 {"id":"recomp","name":"Muscle ↔ fat","blurb":"They don't convert - the honest picture.","blocks":[
   p("The biggest myth: “turning fat into muscle.” They’re <b>different tissues</b> — one is stored energy, one is contractile protein. “Recomposition” is <b>two separate processes at once</b>: losing fat while building muscle."),
   rc_recomp,
   h("Which goal fits which starting body"),
   rc_matrix,
   cards([{"h":"Recomp works best if…","x":"Beginner · returning · higher body-fat. The body funds new muscle from your own fat stores — big newbie window."},
          {"h":"Otherwise…","x":"Trained & lean? Two dials fighting is slow. Alternate: cut to lean, then lean-gain."}]),
   call("<b>Cue.</b> Chase composition, not the scale. Track waist, lifts, and the mirror. ‘70 kg lean & strong’ beats ‘70 kg softer.’")]},

 {"id":"strength","name":"Strength training","blurb":"The signal that decides which way you change.","blocks":[
   p("Training is the <b>signal</b> that tells your body which way to change. Diet supplies the material; the barbell writes the instructions. Without it, a surplus is just fat and a deficit costs you muscle."),
   h("What matters, in order"),
   st_pyramid,
   h("Reps map to different adaptations"),
   st_reps,
   cards([{"h":"Tension","x":"Take sets near failure (~1–3 reps in reserve). Junk volume grows little."},
          {"h":"Overload","x":"Add a little over time — more reps, weight, or better form."},
          {"h":"Recover","x":"Sleep is the anabolic window. Growth happens between sessions."}]),
   call("<b>Cue.</b> Show up, get a little stronger, sleep, repeat. Progressive overload + protein + recovery is 90% of it.")]},

 {"id":"diets","name":"Diet lenses","blurb":"Same physics, three plates - veg / Mediterranean / non-veg.","blocks":[
   p("The physics never changes — calories, protein, training. What changes between diets is <b>how easily each plate hits the targets</b> and which nutrients need attention."),
   h("Vegetarian · Mediterranean · Non-veg"),
   dt_radar,
   cards([{"h":"Vegetarian (+egg)","x":"High fiber & antioxidants; protein needs work. Watch: total protein, B12, omega-3, iron, D3. Your setup — solved with paneer/soy/whey + a small stack."},
          {"h":"Mediterranean","x":"Best-studied for long-term health. Fish, olive oil, legumes, veg, whole grains. Excellent fat quality & omega-3."},
          {"h":"Non-veg (omnivore)","x":"Complete protein, B12, iron, omega-3 built-in. Watch: fiber can fall low; fat quality of processed/red meat."}]),
   call("<b>Takeaway.</b> Every diet can build muscle and lose fat. Pick the one you’ll actually stick to, then patch its known gaps.")]},

 {"id":"plan","name":"Your plan (68 kg)","blurb":"Worked numbers for a veg + eggs 68 kg body.","blocks":[
   p("Worked from your stats, using an <b>assumed</b> 175 cm / 27 yr / moderately-active profile → maintenance ≈ <b>2,400 kcal</b>. Give me your real height, age & activity and I’ll lock these exactly."),
   call("<b>Placeholder assumption.</b> The TDEE below is an estimate. The method is fixed; only the numbers shift with your real stats. Let the scale confirm over 2 weeks, then adjust ~150 kcal."),
   h("Three routes from 68 kg"),
   table(["Goal","Calories","Protein","Fat","Carbs","Use when"],
     [["Cut (lose fat)","~2,000","150 g","55 g","~226 g","see the abs first, then build"],
      ["Recomp (hold)","~2,400","140 g","60 g","~325 g","lean-ish now; slow both-at-once"],
      ["Lean gain → 70","~2,600","140 g","65 g","~365 g","add size with minimal fat"]]),
   h("Hitting ~140g protein on your plate"),
   you_protein,
   cards([{"h":"Already covered","x":"6 eggs (~36g), 600ml milk (~20g), dal, 2 PB sandwiches, peanuts — a strong protein & fat floor, big fiber."},
          {"h":"Levers to add","x":"Paneer, soy chunks, or 1 whey scoop add 20–25g each. Mg glycinate + K2 join your stack per the audit."}]),
   call("<b>Standing constraint.</b> Bananas are excluded from all recommendations per your medical restriction — carb sources here are rice, roti, oats, potato."),
   call("<b>Your cue.</b> Pick one route. Hit protein daily. Lift 3–4×/week, progressing. Let the weekly-average scale steer the calories.")]},
]

gym_tab={"id":"gym","name":"Gym / Body Comp","icon":"\U0001F3CB️",
  "intro":"Calories, macros, and training — how to lose fat, build muscle, and recomposition, applied to a veg + eggs diet.",
  "topics":topics}

# ---- load original nutrition page from CURRENT hub, inject tab ----
src=open(HUB,"r",encoding="utf-8",errors="surrogatepass").read()
m=re.search(r'"nutrition\.html":\s*"RAW:([^"]*)"',src)
page=zlib.decompress(base64.b64decode(m.group(1)),-15).decode("utf-8")

def find_obj_end(s,start):
    # start points at the opening '{'
    depth=0; in_str=False; esc=False
    for i in range(start,len(s)):
        c=s[i]
        if in_str:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c=='"': in_str=False
        else:
            if c=='"': in_str=True
            elif c=='{': depth+=1
            elif c=='}':
                depth-=1
                if depth==0: return i
    raise ValueError("no match")

start=page.find("var DATA=")+len("var DATA=")
obrace=page.find("{",start)
close=find_obj_end(page,obrace)
json_text=page[obrace:close+1]
data=json.loads(json_text)
after=page[close+1:]  # should begin with ';'
assert after[0]==';', repr(after[:20])

# guard: don't double-add
data["tabs"]=[t for t in data["tabs"] if t.get("id")!="gym"]
data["tabs"].append(gym_tab)
print("tabs now:",[ (t['id'],t['name']) for t in data['tabs']])

new_json=json.dumps(data,ensure_ascii=False)
page2=page[:obrace]+new_json+after

# write standalone
open(os.path.join(REPO,"nutrition.html"),"w",encoding="utf-8").write(page2)
print("standalone nutrition.html bytes:",len(page2.encode()))

# re-embed into hub
co=zlib.compressobj(9,zlib.DEFLATED,-15)
raw=co.compress(page2.encode("utf-8"))+co.flush()
newval="RAW:"+base64.b64encode(raw).decode()
src2=re.sub(r'("nutrition\.html":\s*")RAW:[^"]*(")',lambda mm:mm.group(1)+newval+mm.group(2),src,count=1)
open(HUB,"w",encoding="utf-8",errors="surrogatepass").write(src2)

# verify roundtrip
chk=re.search(r'"nutrition\.html":\s*"RAW:([^"]*)"',open(HUB,encoding="utf-8",errors="surrogatepass").read()).group(1)
back=zlib.decompress(base64.b64decode(chk),-15).decode("utf-8")
ob=back.find("{",back.find("var DATA="))
d2=json.loads(back[ob:find_obj_end(back,ob)+1])
print("roundtrip tabs:",[t['id'] for t in d2['tabs']])
print("gym topics:",[tp['id'] for t in d2['tabs'] if t['id']=='gym' for tp in t['topics']])
print("OK")
