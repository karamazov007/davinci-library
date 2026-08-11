# -*- coding: utf-8 -*-
import re, json, zlib, base64, os
REPO="/sessions/lucid-blissful-curie/mnt/davinci-library"; HUB=os.path.join(REPO,"knowledge-hub.html"); OUT="/sessions/lucid-blissful-curie/mnt/outputs"
rd=lambda n: open(f"{OUT}/{n}.svg").read().strip()
mb,mt,ms,ma,mh,mbr,mm,msi,mc,mv=(rd("m_bars"),rd("m_tool"),rd("m_swap"),rd("m_addons"),rd("m_heur"),rd("m_brands"),rd("m_math"),rd("m_simple"),rd("m_cost"),rd("m_value"))
for s in (mb,mt,ms,ma,mh,mbr,mm,msi,mc,mv): assert "`" not in s and "</script" not in s
ml,mtr,mco,mla=(rd("m_looks"),rd("m_tiers"),rd("m_core"),rd("m_looksall"))
for s in (ml,mtr,mco,mla): assert "`" not in s and "</script" not in s
MJS=("function genMealCore(){return `"+mco+"`;}\nfunction genMealLooksAll(){return `"+mla+"`;}\nfunction genMealBars(){return `"+mb+"`;}\nfunction genMealTool(){return `"+mt+"`;}\nfunction genMealSwap(){return `"+ms+"`;}\nfunction genMealAddons(){return `"+ma+"`;}\nfunction genMealHeur(){return `"+mh+"`;}\nfunction genMealBrands(){return `"+mbr+"`;}\nfunction genMealMath(){return `"+mm+"`;}\nfunction genMealSimple(){return `"+msi+"`;}\nfunction genMealCost(){return `"+mc+"`;}\nfunction genMealValue(){return `"+mv+"`;}\nfunction genMealLooks(){return `"+ml+"`;}\nfunction genMealTiers(){return `"+mtr+"`;}\n")

def find_obj_end(s,start):
    d=0;q=False;e=False
    for i in range(start,len(s)):
        c=s[i]
        if q:
            if e:e=False
            elif c=='\\':e=True
            elif c=='"':q=False
        else:
            if c=='"':q=True
            elif c=='{':d+=1
            elif c=='}':
                d-=1
                if d==0:return i
    raise ValueError

src=open(HUB,"r",encoding="utf-8",errors="surrogatepass").read()
page=zlib.decompress(base64.b64decode(re.search(r'"nutrition\.html":\s*"RAW:([^"]*)"',src).group(1)),-15).decode()
page=re.sub(r'/\*MEALJS\*/.*?/\*ENMEALJS\*/\n?','',page,flags=re.S)
anchor=page.find("var DATA=")
page=page[:anchor]+"/*MEALJS*/"+MJS+"/*ENMEALJS*/\n"+page[anchor:]

def p(x):return{"t":"p","x":x}
def h(x):return{"t":"h","x":x}
def call(x):return{"t":"call","x":x}
def cards(i):return{"t":"cards","items":i}
def table(hd,rw):return{"t":"table","head":hd,"rows":rw}
def fig(g,cap):return{"t":"fig","gen":g,"cap":cap,"args":[]}

blocks=[
 h("Your 3 daily non-negotiables"),
 p("The one-glance summary of everything we worked out. Do what you like with the rest — but <b>eggs, soya and paneer</b> are the spine of the plan. Eggs and soya every day; paneer as the swap-in when you want a change (it's the same protein, just ~3× the cost)."),
 fig("genMealCore","Eggs + soya carry your protein every single day; paneer swaps in for the soya a few days a week. Stack them with a whey-and-milk shake and your usual dal & staples and the day lands ~140 g. Everything else is decoration."),
 call("<b>The one cue that survives everything:</b> eat your eggs, eat your soya, swap in paneer sometimes. If a day falls apart, protect <i>those</i> — the rest is optional."),

 h("Heuristics — the thinking behind the plan"),
 p("The rules-of-thumb the whole plan runs on — so you can always see <i>why</i> a choice is made, not just what to eat."),
 fig("genMealHeur","Your operating heuristics, grouped: protein · energy & goals · food quality · training. Read these first — everything else is just applying them."),
 cards([
   {"h":"Each meal 35–40 g protein","x":"Hit it with 1–2 sources combined. This re-triggers muscle-building (MPS) ~4× a day instead of once."},
   {"h":"Lunch & dinner always get a protein anchor","x":"No matter what the main sabzi is — drop in a quick add-on (soy/paneer/egg/whey). These two meals are the danger zones."},
   {"h":"Daily total is king","x":"~1.6–2.2 g/kg/day is what matters; the per-meal spread is the optimizer, not a hard rule."},
   {"h":"Protein is the fixed rail","x":"Keep protein constant whether you cut or bulk; only carbs & fat flex up or down."}]),
 call("<b>Meta-rule:</b> calories set the <i>direction</i> (gain/lose), protein + training set <i>what tissue</i> (muscle/fat), and the weekly scale is the only judge of whether your numbers are right."),

 h("The day, meal by meal"),
 p("Your <b>lean-bulk day</b>: ~<b>2,460 kcal · ~148 g protein</b>, spread across 4 feedings (33–46 g each). Flex it with the toolbox and swaps below — the goal is a <i>clean</i> bulk. If the scale climbs faster than ~0.35 kg/wk, trim ~150 kcal."),
 fig("genMealBars","33–46 g protein per meal — re-triggers MPS ~4× a day. Total ~148 g / ~2,460 kcal (a clean surplus over maintenance)."),
 cards([
   {"h":"🌅 Breakfast · ~46 g · 780 kcal","x":"<b>4-egg omelette</b> · 40 g oats (or low-sugar muesli) in 250 ml milk · <b>1 tbsp peanut butter on 1 slice bread</b> · 1 tbsp ground flax/chia. (PB on bread = easy, no teeth-stick.)"},
   {"h":"🍛 Lunch · ~35 g · 620 kcal","x":"1 cup rice · 1½ katori dal · <b>ONE protein pick</b> · kachumber (cucumber + onion + tomato + coriander, lemon, rock salt) · ~50 g curd (optional — 100 g is too much). Pick: soy chunks 30 g (15 g) / kabuli chana 100 g (9 g) / rajma 100 g (8 g) / green peas (5 g) / paneer 80 g (16 g)."},
   {"h":"🏋️ Post-workout · ~34 g · 300 kcal","x":"1 scoop whey + 300 ml milk. <b>Add a 2nd scoop ONLY</b> on days lunch/dinner had no big protein pick — you don't need 2+2."},
   {"h":"🌙 Dinner · ~33 g · 760 kcal","x":"3 roti · <b>ONE protein pick</b>: low-fat paneer 100 g (20 g) / rajma 1 katori (8 g) / soy (15 g) / chana (9 g) · green beans or sweet-corn sabzi · 1 mango. If both lunch+dinner were light on protein, top off with 1 whey scoop + 250 ml milk."},
   {"h":"🥜 On-the-go (optional)","x":"Travelling / studying: 1 tbsp pumpkin/hemp/flax/chia, or 20–30 g peanuts/almonds (~6–8 g / 150–170 kcal). Fill gaps — don't stack; keep the bulk lean."}]),
 h("Lunch & dinner — base protein & the gap to fill"),
 p("Your staples already carry some protein; one <b>pick</b> tops it up to ~35 g. <b>Lunch:</b> rice ~4 g + 1½ katori dal ~11 g + salad ~2 g ≈ <b>17 g base → need ~+18 g</b>. <b>Dinner:</b> 3 roti ~9 g + veg ~3 g + 1 mango ~1.5 g ≈ <b>~13 g base → need ~+21 g</b>. So subtract the base from 35 and cover the rest with your protein pick."),
 fig("genMealMath","The solid coloured bars = protein already in your staples; the dashed-pink 'gap' is what your pick must add to reach ~35 g. Lunch takes one big pick (soy/paneer); dinner takes a big pick, or a medium one (rajma/chana) + an egg or whey."),
 h("Full day, itemised"),
 table(["Meal","Foods","Protein","Calories"],
   [["Breakfast","4-egg omelette · oats + 250 ml milk · PB on 1 bread · flax","46 g","780"],
    ["Lunch","rice · 1½ dal · soy chunks · kachumber · 50 g curd","35 g","620"],
    ["Post-workout","1 scoop whey + 300 ml milk","34 g","300"],
    ["Dinner","3 roti · paneer/rajma · beans/corn · 1 mango","33 g","760"],
    ["Total","","≈ 148 g","≈ 2,460"]]),
 h("Protein toolbox — pick your swaps"),
 fig("genMealTool","Protein per serving, ranked and colour-coded by group, with the fraction of each food's weight that is protein. Soy chunks, low-fat paneer, whey and Greek/hung curd are your highest-value picks; legumes add fibre + micros; seeds add omega-3."),
 p("Flip it around: instead of protein per serving, here's <b>how much of each food you'd have to eat to get the same 18 g</b> — the flip-side of the fraction column. Whey and soy take a handful; legumes take ~2 katori; green peas take 3+ katori."),
 fig("genMealLooksAll","Every bar is 18 g of protein — the length is grams of that food you'd eat to get there. Concentrated foods (whey, soy, paneer, seeds, nuts) sit at the top with tiny amounts; bulky legumes and peas run down the bottom. Same protein, wildly different volume on your plate."),
 h("Upgrade the weak spots"),
 fig("genMealSwap","The biggest single win: swap the plain gourd/potato veg for a protein pick. Greek/hung curd triples the protein of regular dahi."),
 h("Rules & flex"),
 cards([
   {"h":"Whey scoops","x":"Default 1 post-workout scoop. 2nd scoop only on low-protein days. No 2+2 shakes — total daily protein is what matters, and you're already there."},
   {"h":"Curd","x":"~50 g (2–3 tbsp) is plenty with rice; 100 g is too much. Optional — the lemony kachumber does the job."},
   {"h":"Muesli vs oats","x":"Fine if it's low/no-added-sugar (<5 g sugar/serving). It's ~oats + a bit more carbs/fat — just count the extra."},
   {"h":"Keep it lean","x":"PB, nuts and seeds are calorie-dense — measure them so you land ~2,350–2,400, not 2,800."}]),
 call("<b>Cue.</b> 4 feedings of 33–40 g protein · one real protein pick at lunch AND dinner · whey fills the gaps · seeds/nuts on the go · land ~2,390 kcal · progressively overload · weigh weekly (+0.2–0.35 kg/wk = perfect)."),

 h("Quick protein add-ons"),
 p("Don't depend on what's cooked — keep your own quick add-ons ready and drop <b>ONE</b> onto any lunch or dinner. Breakfast &amp; post-workout are already sorted; these cover the two danger zones. Rule: <b>every lunch and dinner gets one protein anchor (~15–25 g)</b>, whatever else is on the table."),
 fig("genMealAddons","Grab one for any meal. Green = no cooking · blue = batch-prep once/twice a week · amber = 2-minute. Paneer cubes and a whey shake need zero prep; soy chunks and chana just need a weekly batch-boil."),
 cards([
   {"h":"🥤 Whey + milk","x":"1 scoop + 300 ml = ~34 g. The universal backup for any meal that falls short."},
   {"h":"🧀 Raw paneer cubes","x":"80–100 g = ~18–20 g. Cube + chaat masala, eat as-is. The laziest dinner fix — zero cooking."},
   {"h":"🫘 Boiled soy chunks","x":"30 g dry = ~15 g. Batch-boil, then toss into dal/sabzi/rice/curd or dry-roast as a snack — no separate curry needed."},
   {"h":"🥚 Boiled eggs","x":"2–3 = ~12–18 g. Keep a few boiled in the fridge; add instantly."},
   {"h":"🫛 Boiled chana / rajma","x":"1 katori = ~8–9 g. Pressure-cook + freeze in portions; 2-min chana chaat or add to anything."},
   {"h":"🌱 Sprouted moong","x":"1 cup = ~7 g. Roll a jar every 2 days; eat raw with lemon + onion."},
   {"h":"🥣 Curd / Greek curd","x":"~50 g side; Greek/hung curd triples the protein of regular dahi."}]),
 h("Batch-prep — once or twice a week"),
 p("Pressure-cook a big lot of chana/rajma and freeze in portions · boil a batch of soy chunks (keeps 3–4 days in the fridge) · start a sprout jar every 2 days. Paneer, eggs, curd and whey need <b>zero</b> prep. That's ~30 minutes a week for a whole week of protein insurance."),
 h("Lunch & dinner — the specifics"),
 cards([
   {"h":"🍛 Lunch is almost sorted","x":"Dal already gives ~8–11 g. Add ONE — soy chunks tossed in, a boiled egg, or curd — and you're at ~30 g."},
   {"h":"🌙 Dinner with no protein sabzi","x":"Just add raw paneer cubes, 2 boiled eggs, a chana chaat, or a whey shake. One of them, every night."}]),
 call("<b>The system:</b> whatever your mother cooks + <b>pick ONE add-on</b> = protein sorted. You're never dependent on the menu. Ask her for a protein dish a few times a week if you like — but your batch-prepped add-ons are the real insurance."),

 h("Trusted brands"),
 p("Given the FSSAI drives on <b>‘analogue paneer’</b> (vegetable oil + starch sold as milk paneer), here's what to trust. Good news: <b>paneer is the only anchor you need to be strict about</b> — eggs, branded milk, whey, soya and dal are all low-risk."),
 fig("genMealBrands","Buy sealed & branded, with an FSSAI licence number. For paneer & curd, stick to big milk co-ops/dairies; for soya and legumes any reputable sealed brand is fine."),
 h("Spotting fake / analogue paneer"),
 cards([
   {"h":"👃 Smell &amp; taste","x":"Real paneer = mild, creamy, slightly sweet. A sour / chemical / detergent-like smell, or a chalky-bland taste, means adulterated."},
   {"h":"✋ Texture","x":"Real paneer crumbles softly; analogue is oddly rubbery / over-stretchy."},
   {"h":"🧪 Starch test","x":"Boil a piece, cool it, add a drop of iodine tincture — turns blue-black = starch added (fake)."},
   {"h":"🏷️ Label","x":"Must say made from milk + carry an FSSAI licence number. If it says ‘analogue’ / ‘non-dairy’, it isn't real paneer."}]),
 call("<b>Buying heuristic:</b> sealed + branded + FSSAI number + a big-name dairy for anything milk-based; real paneer isn't cheap (cheap = suspicious). Want zero paneer worry? Lean on <b>soya chunks + curd + eggs + whey</b> — all low-risk protein anchors."),

 h("Swaps, portions & cost"),
 p("The whole plan in one place: what's <b>automatic</b> vs what you <b>add</b>, exactly <b>how much</b> of each pick, the <b>backups</b> when you miss one, and what it all <b>costs</b>. This is the flexibility layer — use it to swap freely without ever dropping below your daily protein."),
 fig("genMealSimple","Green = automatic (eggs + whey + milk run themselves). Amber = your only two 'add' moves: soy at lunch, eggs (or a pick) at dinner. If you miss either, the violet plug — whey + milk (or water at night) — covers it. Day lands ≈ 137 g even on a lazy day."),
 h("How much of each pick"),
 p("Your lunch/dinner staples give ~13–17 g on their own; one pick tops it to ~30–35 g. Here's the portion of each pick for a <b>~15 g</b> or <b>~20 g</b> top-up:"),
 table(["Protein pick","for ~15 g","for ~20 g"],
   [["Soy chunks (dry)","30 g","40 g"],
    ["Low-fat paneer","75 g","100 g"],
    ["Kabuli chana (cooked)","1½ katori","2 katori"],
    ["Rajma (cooked)","2 katori","2 katori + 1 egg"],
    ["Tofu","180 g","250 g"],
    ["Greek / hung curd","150 g","200 g"],
    ["Eggs","2–3","3–4"],
    ["Whey","½ scoop","1 scoop"]]),
 call("<b>Fast mental math:</b> soy is ~1/2 protein, paneer ~1/5, Greek curd ~1/10. So grams-of-protein ≈ weight × that fraction — 40 g soy ≈ 20 g, 100 g paneer ≈ 20 g, 200 g Greek curd ≈ 20 g."),
 h("Why soy, paneer &amp; eggs win — the veg-protein tiers"),
 p("The blunt truth about vegetarian protein: most vegetables are <b>decoration</b> — trace protein locked in a huge volume of water and fibre. You'd have to eat an <i>enormous</i> amount to hit your target, filling your belly and blowing your calories before you get there. Concentrated sources sidestep <b>both</b> ceilings — stomach volume <i>and</i> calorie budget — at once."),
 fig("genMealLooks","Every bar is the <b>same 18 g of protein</b> — the length is how much of that food you'd have to eat to get it. Soy needs 35 g; green beans need a full kilogram. That ~28× gap is the whole argument for concentrated protein."),
 fig("genMealTiers","Three tiers: the <b>engine</b> (soy · paneer · eggs · whey · tofu · curd) carries most of your protein · the <b>support</b> (dal · chana · rajma · moong) is real protein but bulky, so it's the base not the whole meal · <b>decorations</b> (broccoli · beans · peas · sabzi) are for fibre &amp; fullness, never counted on for protein."),
 call("<b>Tier cue:</b> get protein from the <b>engine</b>, build the plate on the <b>support</b>, enjoy <b>decorations</b> for fibre — never try to hit protein with vegetables."),
 h("Backups & compromises"),
 cards([
   {"h":"Forgot the pick? → whey + milk","x":"1 scoop + 300 ml (or water at night) ≈ 34 g. The <b>universal plug</b> for a missed lunch soy or dinner pick — never go to bed short."},
   {"h":"3 eggs at dinner = the pick","x":"~18 g on top of roti + veg + mango → ~31 g. Then paneer/soy aren't needed at dinner. 6 eggs across a day is perfectly safe for you."},
   {"h":"Don't over-optimise","x":"~15 g from a pick is fine; a meal at ~30 g still lands the day near ~137 g. Precision isn't the point — <b>not skipping</b> is."},
   {"h":"Soy daily · paneer a treat","x":"Same protein, but paneer costs ~3× and whey ~5× per gram. Use paneer 2–3×/week for taste; let soy + dal + eggs carry the load."}]),
 h("Cost per gram of protein"),
 p("Where your protein rupees go. This is why the plan leans on soy, dal, eggs and milk for the bulk of it, and treats paneer &amp; whey as premium extras."),
 fig("genMealCost","Per gram of protein: soy, chana/rajma, peanuts, dal and milk are the cheap engine; eggs sit mid; paneer ~3× and whey ~5× the price of soy; branded Greek yogurt is priciest — make hung curd at home instead."),
 h("The value map — density vs price, together"),
 p("The two ideas on one picture. <b>Up</b> = protein-dense (more protein per gram of food, so less to eat). <b>Right</b> = costs more per gram of protein. So the <b>top-left corner is the sweet spot</b>: dense <i>and</i> cheap."),
 fig("genMealValue","Each food plotted by protein density (up) vs cost per gram of protein (right). <b>Soy</b> sits alone in the green corner — dense and dirt-cheap, your everyday base. <b>Whey</b> is the densest but pricier. <b>Dal, chana, peanuts, eggs</b> cluster in the good-value band. <b>Branded Greek yogurt</b> is stranded bottom-right — dilute and expensive."),
 call("<b>Value cue:</b> read the corner — <b>soy = eat daily</b> (dense + cheap); whey when you need dense-and-fast; dal/chana/eggs for cheap volume; paneer as a tasty splurge; branded Greek yogurt only if you love it (or make hung curd)."),
 call("<b>Cost cue:</b> budget engine = <b>soy + dal + eggs + milk</b>. Paneer &amp; whey = premium extras for taste + convenience. Skip branded Greek yogurt — hung curd at home is a fraction of the price for the same protein."),
]

def split_topics(blocks, sections):
    idxs=[]
    for sid,name,blurb,htext in sections:
        found=None
        for i,b in enumerate(blocks):
            if b.get("t")=="h" and b.get("x")==htext: found=i;break
        idxs.append(found)
    assert all(x is not None for x in idxs[1:]), "missing section heading"
    tops=[]
    for k,(sid,name,blurb,htext) in enumerate(sections):
        start=0 if k==0 else idxs[k]
        end=idxs[k+1] if (k+1<len(sections)) else len(blocks)
        tops.append({"id":sid,"name":name,"blurb":blurb,"blocks":blocks[start:end]})
    return tops

meal_sections=[
 ("core","Daily core","your 3 non-negotiables","Your 3 daily non-negotiables"),
 ("heur","Heuristics","the thinking behind it","Heuristics — the thinking behind the plan"),
 ("day","The day","meal by meal + itemised","The day, meal by meal"),
 ("toolbox","Protein toolbox","ranked, colour-coded","Protein toolbox — pick your swaps"),
 ("swaps","Upgrade weak spots","before → after","Upgrade the weak spots"),
 ("rules","Rules & flex","curd, whey, muesli","Rules & flex"),
 ("quickadd","Quick add-ons","always-ready protein","Quick protein add-ons"),
 ("brands","Trusted brands","what to buy in India","Trusted brands"),
 ("swapcost","Swaps, portions & cost","system · portions · price","Swaps, portions & cost"),
]

ob=page.find("{",page.find("var DATA="));close=find_obj_end(page,ob)
data=json.loads(page[ob:close+1]);after=page[close+1:]
data["tabs"]=[t for t in data["tabs"] if t.get("id")!="mealplan"]
tab={"id":"mealplan","name":"Meal Plan","icon":"\U0001F37D️",
 "intro":"Your lean-bulk meal plan — the day, the protein toolbox, and the swaps.",
 "topics":split_topics(blocks, meal_sections)}
ids=[t["id"] for t in data["tabs"]]
data["tabs"].insert(ids.index("youplan")+1 if "youplan" in ids else len(data["tabs"]), tab)
page=page[:ob]+json.dumps(data,ensure_ascii=False)+after
open(os.path.join(REPO,"nutrition.html"),"w",encoding="utf-8").write(page)
co=zlib.compressobj(9,zlib.DEFLATED,-15);raw=co.compress(page.encode())+co.flush()
src2=re.sub(r'("nutrition\.html":\s*")RAW:[^"]*(")',lambda m:m.group(1)+"RAW:"+base64.b64encode(raw).decode()+m.group(2),src,count=1)
open(HUB,"w",encoding="utf-8",errors="surrogatepass").write(src2)
back=zlib.decompress(base64.b64decode(re.search(r'"nutrition\.html":\s*"RAW:([^"]*)"',open(HUB,encoding="utf-8",errors="surrogatepass").read()).group(1)),-15).decode()
ob2=back.find("{",back.find("var DATA="));d2=json.loads(back[ob2:find_obj_end(back,ob2)+1])
print("tabs:",[t["id"] for t in d2["tabs"]])
print("meal gens:", all(g in back for g in ("function genMealBars(","function genMealTool(","function genMealSwap(")))
print("OK")
