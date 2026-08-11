# -*- coding: utf-8 -*-
import re, json, zlib, base64, os
REPO="/sessions/lucid-blissful-curie/mnt/davinci-library"; HUB=os.path.join(REPO,"knowledge-hub.html"); OUT="/sessions/lucid-blissful-curie/mnt/outputs"
ROSE="#DB2777";TEAL="#0D9488";AMBER="#D97706";GREEN="#16A34A";BLUE="#2563EB";CYAN="#0E7490";VIOLET="#7C3AED";INK="#1c2431";SL="#64748b"

bf=open(f"{OUT}/y_bodyfat.svg").read().strip(); rev=open(f"{OUT}/y_reveal.svg").read().strip(); mp=open(f"{OUT}/y_map.svg").read().strip()
for s in (bf,rev,mp): assert "`" not in s and "</script" not in s
YFNS=("function genYBodyFat(){return `"+bf+"`;}\nfunction genYReveal(){return `"+rev+"`;}\nfunction genYMap(){return `"+mp+"`;}\n")
td=open(f"{OUT}/t_dial.svg").read().strip(); tm=open(f"{OUT}/t_macros.svg").read().strip(); trr=open(f"{OUT}/t_rate.svg").read().strip()
for s in (td,tm,trr): assert "`" not in s and "</script" not in s
YFNS+=("function genTgtDial(){return `"+td+"`;}\nfunction genTgtMacros(){return `"+tm+"`;}\nfunction genTgtRate(){return `"+trr+"`;}\n")
ff=open(f"{OUT}/f_frame.svg").read().strip(); fa=open(f"{OUT}/f_arm.svg").read().strip()
for s in (ff,fa): assert "`" not in s and "</script" not in s
YFNS+=("function genFrameScale(){return `"+ff+"`;}\nfunction genArmRunway(){return `"+fa+"`;}\n")
wn=open(f"{OUT}/w_net.svg").read().strip(); ww=open(f"{OUT}/w_why.svg").read().strip()
for s in (wn,ww): assert "`" not in s and "</script" not in s
YFNS+=("function genNetByEnergy(){return `"+wn+"`;}\nfunction genWhySurplus(){return `"+ww+"`;}\n")
mech=json.load(open(f"{OUT}/mech_sk.json"))
for v in mech.values(): assert "`" not in v and "</script" not in v
YFNS+=("var MECH_SVG="+json.dumps(mech,ensure_ascii=False)+";\n"
 "var MECH_META={order:[\"cut\",\"maintenance\",\"bulk\"],labels:{cut:\"Cut · 1,680\",maintenance:\"Maintenance · 2,100\",bulk:\"Lean bulk · 2,310\"}};\n"
 "function MECH_mount(){document.querySelectorAll('.psankey-root[data-mech]').forEach(function(r){if(r.__mech)return;r.__mech=1;"
 "var b=MECH_META.order.map(function(k){return '<button class=\"psk-btn\" data-mk=\"'+k+'\">'+MECH_META.labels[k]+'</button>';}).join('');"
 "r.innerHTML='<div class=\"psk-tabs\">'+b+'</div><div class=\"psk-chart\"></div>';var c=r.querySelector('.psk-chart');"
 "function show(k){c.innerHTML=MECH_SVG[k];[].forEach.call(r.querySelectorAll('.psk-btn'),function(x){x.classList.toggle('on',x.getAttribute('data-mk')===k);});}"
 "r.addEventListener('click',function(e){var x=e.target.closest&&e.target.closest('.psk-btn');if(x)show(x.getAttribute('data-mk'));});show('bulk');});}\n")

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
page=re.sub(r'/\*YJS\*/.*?/\*ENYJS\*/\n?','',page,flags=re.S)
anchor=page.find("var DATA=")
page=page[:anchor]+"/*YJS*/"+YFNS+"/*ENYJS*/\n"+page[anchor:]

def p(x):return{"t":"p","x":x}
def h(x):return{"t":"h","x":x}
def call(x):return{"t":"call","x":x}
def cards(i):return{"t":"cards","items":i}
def table(hd,rw):return{"t":"table","head":hd,"rows":rw}
def fig(g,cap,args=None):return{"t":"fig","gen":g,"cap":cap,"args":args or []}
def gnode(id,x,y,label,fill,w=120,h=48,shape="round"):return{"id":id,"x":x,"y":y,"label":label,"fill":fill,"w":w,"h":h,"shape":shape}

fork=fig("genGraph","You're lean and early in training — so build first. Cutting now reveals abs on a small frame; lean-bulking builds the muscle, then a short cut shows a lean AND muscular you.",
 [[gnode("you",0.1,0.5,"YOU\nlean ~15%\nearly trainee",BLUE,140,66),
   gnode("cut",0.48,0.2,"Cut now\n→ 65 kg · abs\nbut small",AMBER,150,60),
   gnode("lb",0.46,0.8,"LEAN-BULK\nnow",GREEN,140,54),
   gnode("goal",0.84,0.55,"build ~5 kg muscle\n→ short cut →\nLEAN + MUSCULAR ~70 kg",TEAL,200,76)],
  [{"from":"you","to":"cut"},{"from":"you","to":"lb","label":"recommended","color":GREEN,"lc":GREEN},{"from":"lb","to":"goal"}],
  {"w":720,"h":420}])

macros=fig("genTreemap","Your lean-bulk day (~2,350 kcal): protein stays where you already are; carbs fuel the extra training; a modest surplus drives growth.",
 [[{"label":"Carbs ~311 g","weight":1244,"color":CYAN},{"label":"Protein 130 g","weight":520,"color":ROSE},{"label":"Fat ~65 g","weight":585,"color":AMBER}],{"w":700,"h":400}])

timeline=fig("genTimeline","The arc: a slow lean-bulk adds muscle over a year (staying under ~18% BF), then a short cut reveals a lean, muscular physique — heavier than now but defined.",
 [[{"when":"Now","label":"68 kg · 15%"},{"when":"Mo 3","label":"~70 kg\nbuilding"},{"when":"Mo 6","label":"~71 kg"},
   {"when":"Mo 9","label":"~72 kg"},{"when":"Mo 12","label":"~73 kg\n<18% BF"},{"when":"Cut","label":"~70 kg\nlean+defined"}],{"w":780,"h":420}])

pyramid=fig("genPyramid","What actually moves the needle for you, in order. The base is everything — the apex barely matters.",
 [[{"label":"Supplements","sub":"minor"},{"label":"Meal timing / spread"},{"label":"Sleep & recovery"},
   {"label":"Protein ~130 g/day"},{"label":"Slight surplus +250 kcal"},{"label":"Progressive overload + consistency","sub":"foundation"}],{"w":700,"h":460}])

blocks=[
 p("Here's your exact place, and the plan — all in pictures. Snapshot: <b>23 yr · 175 cm · 68 kg</b>, waist <b>32″ (81 cm)</b>, roughly <b>~15% body fat</b>, lean mass ~58 kg. Verdict: a <b>lean, athletic, early-intermediate</b> — healthy weight, genuinely lean, just under-muscled for your potential (only 5–6 months trained)."),
 cards([{"h":"23 yr · 175 cm · 68 kg","x":"BMI 22.2 — healthy weight, mid-normal."},
        {"h":"Waist 32″ (81 cm)","x":"waist-to-height 0.46 — lean (under 0.5)."},
        {"h":"~15% body fat","x":"lean mass ~58 kg — athletic, early-intermediate."}]),
 h("Where you sit on the body-fat spectrum"),
 fig("genYBodyFat","You're at ~15% — athletic, just outside the 12–15% 'visible definition' zone. Only ~2–3 kg of fat sits between you and clear definition."),
 call("<b>Key insight.</b> You're already lean — the thing missing from the 'wow' look is <b>muscle</b>, not fat. So the priority is building, not cutting."),
 h("The map: where you are → where you're going"),
 fig("genYMap","Two levers: horizontal = body fat, vertical = muscle. You're 'lean but small'; the goal is up-and-slightly-left → 'lean & muscular'. You get there by building muscle while staying lean."),
 p("<b>Definition</b> is set by body fat (go leaner → more visible). <b>Size</b> is set by muscle (train + eat → bigger). They're separate dials — which is why 'do I need to be 70 kg to look defined?' is the wrong question."),
 h("Leaner = lighter AND more defined (same you)"),
 fig("genYReveal","Hold your muscle and just strip fat: you get a touch lighter and much more defined. Clear abs show around ~12–13% (~65–66 kg) — you'd LOSE weight to reveal them, not gain."),
 h("Your frame & arm potential"),
 p("Your <b>wrist (6.5″)</b> is a proxy for your bone frame; forearm 11″, biceps <b>12.7″ flexed</b>. Slim-boned — which means a lean, proportionate ceiling (not a mass frame), and small joints that make muscle look bigger by contrast."),
 cards([{"h":"Wrist 6.5″ — slim frame","x":"Lean natural ceiling ~mid-70s kg. Small joints = aesthetic advantage."},
        {"h":"Forearm 11″","x":"1.7× wrist — solid base, room to grow."},
        {"h":"Biceps 12.7″ flexed","x":"1.95× wrist — early-intermediate, ~average+."}]),
 fig("genFrameScale","Your 6.5″ wrist sits at the small/medium line for 5'9″ — a lean, proportionate build. Frame sets absolute size, not how good you can look."),
 call("<b>Slim frame is an advantage.</b> Narrow wrists + a small waist make a lean, muscular physique read as ‘sculpted’. Your game is proportion + leanness, not raw bulk — build shoulders &amp; back for width, and arms."),
 h("Arm runway — where you are vs your potential"),
 fig("genArmRunway","A well-built natural arm is ~2.3–2.5× the wrist → for you ~15–16″. You're at 1.95× (12.7″), so there's ~3″ of runway — years of growth from big lifts (rows, chins, presses) + direct work in a small surplus."),
 call("<b>Arm milestones:</b> 13.5″ = good · 14.5″ = strong for your frame · 15–16″ = excellent, near potential. A lean 72–73 kg with 15″ arms looks genuinely impressive on a slim frame."),
 h("Cut now, or build first? (the fork)"),
 fork,
 call("<b>My recommendation: lean-bulk now.</b> You're lean enough (15%) and early enough in training that this is prime muscle-building time. Cutting now just makes you a smaller version of what you already are — build the muscle, reveal it later."),
 h("Why a surplus builds muscle (even with protein constant)"),
 p("The confusing bit: if protein is fixed, how does eating more build muscle? Because the <b>“~3 g net” is not a constant — it depends on your energy state.</b> The surplus doesn't <i>become</i> muscle; it makes the environment that lets your fixed protein actually get built."),
 fig("genNetByEnergy","Same 130 g of protein → different net muscle depending on energy: a deficit nets ~0 or negative, maintenance ~+1 g (you, stuck), a surplus ~+3 g. Energy state flips the MPS − MPB balance."),
 fig("genWhySurplus","Same bricks, opposite result. In a deficit MPS is low and breakdown (MPB) high → muscle lost. In a surplus MPS is high and MPB low → muscle built. The protein is identical; the energy decides."),
 cards([{"h":"1 · Pays the ATP bill","x":"Assembling muscle is expensive; a deficit can't afford it, a surplus can."},
        {"h":"2 · Spares your protein","x":"A deficit burns your amino acids for fuel; a surplus lets them build instead."},
        {"h":"3 · Anabolic hormones","x":"Surplus keeps insulin / testosterone / IGF-1 up and cortisol down."},
        {"h":"4 · Fuels training + recovery","x":"Full glycogen → harder overload; more energy → better repair."}]),
 call("<b>So:</b> the small fat gain of a bulk is the <i>toll</i> you pay for an anabolic environment that turns your constant 130 g from “~0 at maintenance” into “~3 g of muscle.” This is exactly why 2 months at maintenance built nothing — add the surplus and the same protein finally works."),
 h("Follow the fuel — how each mechanism gets funded (toggle)"),
 p("In kcal: each macro's energy flows to its jobs (run the body · train + recover · <b>ATP to BUILD</b> · hormone support), and your 130 g protein flows to its fates. Toggle cut → maintenance → lean bulk and watch <b>MUSCLE-building grow 97 → 159 → 270</b> as the surplus funds the labour, spares the protein, and tops up hormones."),
 {"t":"mechflow"},
 call("<b>How to read it:</b> the thin rose ribbon into MUSCLE = the amino-acid <i>bricks</i> (small); the violet (ATP labour) + green (hormones) = the <i>energy that lets those bricks get laid</i>. A cut starves all three; a lean bulk funds them — same 130 g protein, far more muscle."),
 h("Calorie targets — the thumb rules"),
 p("<b>Maintenance ≈ bodyweight(kg) × 30–33</b> (desk + gym ~30–31; active ~33). You: 68 × 31 ≈ <b>2,100</b> — your stable weight confirms it. Then just <b>multiply</b> to pick a goal."),
 fig("genTgtDial","Multiply maintenance: standard cut ×0.80, lean bulk ×1.10. Left of ×1.00 = deficit, right = surplus. Your lean-bulk target ≈ 2,310 kcal."),
 table(["Goal","× maintenance","Change","You (2,100)"],
   [["Aggressive cut","×0.75","−25%","~1,575"],["Standard cut","×0.80","−20%","~1,680"],["Gentle cut","×0.85","−15%","~1,785"],
    ["Maintenance","×1.00","0","~2,100"],["Lean bulk","×1.10","+10%","~2,310"],["Aggressive bulk","×1.20","+20%","~2,520 (skip)"]]),
 h("Protein stays fixed; carbs & fat flex"),
 fig("genTgtMacros","Protein is the constant rail (~130 g) whether you cut or bulk — only carbs and fat move: trim them to cut, add them to bulk."),
 h("The scale is the real calculator (rate check)"),
 fig("genTgtRate","The multiplier is only a starting guess — the weekly-average scale confirms it. Stay in the green: cut −0.35 to −0.7 kg/wk, bulk +0.2 to +0.35 kg/wk. Off-target → adjust ±150 kcal."),
 call("<b>Cue.</b> Maintenance = kg × 30–33. Cut = ×0.80, lean bulk = ×1.10. Hold protein fixed, flex carbs/fat, and let the weekly scale fine-tune."),
 h("Your lean-bulk plan"),
 cards([{"h":"~2,350 kcal / day","x":"+250 over ~2,100 maintenance — a LEAN bulk, not a dirty one."},
        {"h":"Protein ~130 g","x":"you already hit this (whey + eggs + milk). Don't add more."},
        {"h":"Gain 0.25–0.5 kg / month","x":"mostly muscle at your stage. Weigh weekly; if gaining too fast, trim ~150 kcal."}]),
 macros,
 h("The 12-month arc"),
 timeline,
 h("What actually drives it (in order)"),
 pyramid,
 h("Your current day — why you've been stuck"),
 table(["Food","Protein","Calories"],
   [["3 eggs","18 g","210"],["Whey ×3 scoops (72 g)","72 g","360"],["Milk 600 ml","20 g","360"],
    ["Rice (lunch)","5 g","260"],["Dal (1 katori)","7 g","150"],["Potato sabzi","3 g","200"],
    ["2 roti","6 g","240"],["Gourd veg","2 g","90"],["Mango (1½)","1.5 g","200"],
    ["Total","≈ 134 g","≈ 2,070"]]),
 call("<b>Why stuck 2 months:</b> ~2,100 kcal ≈ your maintenance, so weight (and everything) sits still. Protein is already plenty (~2 g/kg). The fix isn't more protein — it's a <b>small surplus (+250)</b> + <b>progressive overload</b> + <b>sleep</b>."),
 call("<b>Your move.</b> Add ~250 kcal (an extra PB sandwich or a bowl of oats), keep protein ~130 g, push your lifts up every week, weigh weekly. Build to ~72–73 kg over the year, then a short cut → lean and muscular."),
]

# mechflow block type + mount hook (idempotent)
page=page.replace('case "mechflow": return \'<div class="psankey-root" data-mech="1"></div>\';\n   ','')
page=page.replace('try{MECH_mount();}catch(_){}','')
page=page.replace('case "p":','case "mechflow": return \'<div class="psankey-root" data-mech="1"></div>\';\n   case "p":',1)
page=page.replace('try{NCM.mountAll();}catch(_){}','try{NCM.mountAll();}catch(_){}try{MECH_mount();}catch(_){}')

ob=page.find("{",page.find("var DATA="));close=find_obj_end(page,ob)
data=json.loads(page[ob:close+1]);after=page[close+1:]
def split_topics(blocks, sections):
    idxs=[]
    for sid,name,blurb,htext in sections:
        found=None
        for i,b in enumerate(blocks):
            if b.get("t")=="h" and b.get("x")==htext: found=i;break
        idxs.append(found)
    assert all(x is not None for x in idxs[1:]), "missing section heading: "+str([s[3] for s,x in zip(sections,idxs) if x is None])
    tops=[]
    for k,(sid,name,blurb,htext) in enumerate(sections):
        start=0 if k==0 else idxs[k]
        end=idxs[k+1] if (k+1<len(sections)) else len(blocks)
        tops.append({"id":sid,"name":name,"blurb":blurb,"blocks":blocks[start:end]})
    return tops

you_sections=[
 ("stand","Where you stand","BMI · waist · body-fat %","Where you sit on the body-fat spectrum"),
 ("map","Composition & reveal","lean-but-small → lean & muscular","The map: where you are → where you're going"),
 ("frame","Frame & arm potential","wrist · arm runway","Your frame & arm potential"),
 ("fork","Cut or build first?","the decision","Cut now, or build first? (the fork)"),
 ("whybulk","Why a surplus builds","same protein, more muscle","Why a surplus builds muscle (even with protein constant)"),
 ("fuel","Follow the fuel","macros → jobs → muscle","Follow the fuel — how each mechanism gets funded (toggle)"),
 ("targets","Calorie targets","the multiplier thumb-rules","Calorie targets — the thumb rules"),
 ("plan","Lean-bulk plan","numbers · macros · 12-mo arc","Your lean-bulk plan"),
 ("stuck","Why you're stuck","current-day audit","Your current day — why you've been stuck"),
]

data["tabs"]=[t for t in data["tabs"] if t.get("id")!="youplan"]
tab={"id":"youplan","name":"You · body & plan","icon":"\U0001F3AF",
 "intro":"Your exact place and your plan, in pictures — where you sit, and how to get lean & muscular.",
 "topics":split_topics(blocks, you_sections)}
# insert right after gym
ids=[t["id"] for t in data["tabs"]]
data["tabs"].insert(ids.index("gym")+1 if "gym" in ids else len(data["tabs"]), tab)
page=page[:ob]+json.dumps(data,ensure_ascii=False)+after
open(os.path.join(REPO,"nutrition.html"),"w",encoding="utf-8").write(page)
co=zlib.compressobj(9,zlib.DEFLATED,-15);raw=co.compress(page.encode())+co.flush()
src2=re.sub(r'("nutrition\.html":\s*")RAW:[^"]*(")',lambda m:m.group(1)+"RAW:"+base64.b64encode(raw).decode()+m.group(2),src,count=1)
open(HUB,"w",encoding="utf-8",errors="surrogatepass").write(src2)
back=zlib.decompress(base64.b64decode(re.search(r'"nutrition\.html":\s*"RAW:([^"]*)"',open(HUB,encoding="utf-8",errors="surrogatepass").read()).group(1)),-15).decode()
ob2=back.find("{",back.find("var DATA="));d2=json.loads(back[ob2:find_obj_end(back,ob2)+1])
print("tabs:",[t["id"] for t in d2["tabs"]])
print("Y gens:", all(g in back for g in ("function genYBodyFat(","function genYReveal(","function genYMap(")))
print("OK")
