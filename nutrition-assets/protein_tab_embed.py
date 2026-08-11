# -*- coding: utf-8 -*-
import re, json, zlib, base64, os
REPO="/sessions/lucid-blissful-curie/mnt/davinci-library"
HUB=os.path.join(REPO,"knowledge-hub.html")
OUT="/sessions/lucid-blissful-curie/mnt/outputs"
ROSE="#DB2777";TEAL="#0D9488";AMBER="#D97706";GREEN="#16A34A";BLUE="#2563EB"

dose=open(f"{OUT}/pc_dose.svg").read().strip()
daily=open(f"{OUT}/pc_daily.svg").read().strip()
timeline=open(f"{OUT}/pc_timeline.svg").read().strip()
sankey_svg=open(f"{OUT}/pc_sankey.svg").read().strip()
for s in (dose,daily,timeline,sankey_svg): assert "`" not in s and "${" not in s and "</script" not in s

FNS=("function genPCDose(){return `"+dose+"`;}\n"
     "function genPCDaily(){return `"+daily+"`;}\n"
     "function genPCTimeline(){return `"+timeline+"`;}\n"
     "function genPCSankey136(){return `"+sankey_svg+"`;}\n")

# interactive 4-goal sankey toggle
sk4=json.load(open(f"{OUT}/pc_sk4.json"))
for v in sk4.values(): assert "`" not in v and "</script" not in v
PSK_JS=("var PSK_SVG="+json.dumps(sk4,ensure_ascii=False)+";\n"
 "var PSK_META={order:[\"minimum\",\"build\",\"solid\",\"cutting\"],labels:{minimum:\"Minimum · 0.8\",build:\"Build / keep · 1.6\",solid:\"Solid · 2.0\",cutting:\"Cutting · 2.2\"}};\n"
 "function PSK_mount(){document.querySelectorAll('.psankey-root[data-psk]').forEach(function(r){if(r.__psk)return;r.__psk=1;"
 "var btns=PSK_META.order.map(function(k){return '<button class=\"psk-btn\" data-k=\"'+k+'\">'+PSK_META.labels[k]+'</button>';}).join('');"
 "r.innerHTML='<div class=\"psk-tabs\">'+btns+'</div><div class=\"psk-chart\"></div>';"
 "var chart=r.querySelector('.psk-chart');"
 "function show(k){chart.innerHTML=PSK_SVG[k];[].forEach.call(r.querySelectorAll('.psk-btn'),function(b){b.classList.toggle('on',b.getAttribute('data-k')===k);});}"
 "r.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.psk-btn');if(b)show(b.getAttribute('data-k'));});"
 "show('solid');});}\n")
FNS=FNS+PSK_JS
PSK_CSS=("/*PSKCSS*/.psankey-root{margin:14px 0}.psk-tabs{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 12px}"
 ".psk-btn{cursor:pointer;border:1px solid #e7e9ee;background:#fff;border-radius:20px;padding:8px 16px;font-size:13px;color:#334;font-family:inherit}"
 ".psk-btn:hover{background:#f1f3f6}.psk-btn.on{background:#1c2431;color:#fff;border-color:#1c2431}"
 ".psk-chart svg{display:block;width:100%;height:auto}/*ENPSKCSS*/")

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

# idempotent strip + inject gen fns
page=re.sub(r'/\*PCJS\*/.*?/\*ENPCJS\*/\n?','',page,flags=re.S)
anchor=page.find("var DATA=")
page=page[:anchor]+"/*PCJS*/"+FNS+"/*ENPCJS*/\n"+page[anchor:]

# PSK css + block type + mount hook (idempotent)
page=re.sub(r'/\*PSKCSS\*/.*?/\*ENPSKCSS\*/','',page,flags=re.S)
page=page.replace("</style>",PSK_CSS+"</style>",1)
page=page.replace('case "psankey": return \'<div class="psankey-root" data-psk="1"></div>\';\n   ','')
page=page.replace('try{PSK_mount();}catch(_){}','')
page=page.replace('case "p":','case "psankey": return \'<div class="psankey-root" data-psk="1"></div>\';\n   case "p":',1)
page=page.replace('try{NCM.mountAll();}catch(_){}','try{NCM.mountAll();}catch(_){}try{PSK_mount();}catch(_){}')

# build/replace tab
ob=page.find("{",page.find("var DATA="));close=find_obj_end(page,ob)
data=json.loads(page[ob:close+1]);after=page[close+1:]

def p(x):return {"t":"p","x":x}
def h(x):return {"t":"h","x":x}
def call(x):return {"t":"call","x":x}
def fig(g,cap):return {"t":"fig","gen":g,"cap":cap,"args":[]}
def cards(items):return {"t":"cards","items":items}
def table(head,rows):return {"t":"table","head":head,"rows":rows}

sankey=fig("genPCSankey136","Your 136 g/day in grams: ~34 g is taken by the gut & liver on first pass; of the ~102 g that reaches the body, ~60 g is oxidised for energy (nitrogen out as urea), ~28 g renews existing proteins (upkeep), ~11 g becomes other molecules, and only ~3 g is NET new muscle. Grams illustrative for a weight-stable 68 kg trainee.")

blocks=[
 p("<b>“0.4 g/kg” = grams of protein per kg of your BODYWEIGHT</b> — nothing to do with the weight of the food. At 68 kg: one meal ≈ 0.4×68 ≈ <b>27 g protein</b>; the daily target uses the same anchor. Formula: <b>g/day = g/kg × bodyweight</b>."),
 table(["Goal (g/kg)","Daily protein (68 kg)","Per meal (×4)"],
   [["Minimum · RDA 0.8","54 g","—"],["Build / keep · 1.6","109 g","27 g"],["Solid · 2.0","136 g","34 g"],["Cutting · 2.2","150 g","38 g"]]),
 h("The per-meal ceiling (“muscle full”)"),
 fig("genPCDose","One meal switches MPS on, but it maxes out at ~0.4 g/kg (~25–30 g). Past the ceiling, MPS doesn’t climb — the extra amino acids are oxidised."),
 call("<b>Ceiling.</b> A bigger single dose does NOT build faster — it maxes the switch, and the surplus is burned. This is why one giant protein meal wastes most of it."),
 h("Where your 136 g/day actually goes (in grams)"),
 sankey,
 h("Why 160 g ≠ 12 g deposited"),
 fig("genPCDaily","Muscle-building drive vs TOTAL daily protein. It rises to ~1.6 g/kg then plateaus — past ~1.6–2.2 g/kg, more protein does not add muscle."),
 call("<b>Two separate ceilings.</b> (1) Per-meal MPS caps at ~0.4 g/kg. (2) Per-DAY, net muscle is capped by your biological growth rate (~2–4 g/day). So eating 160 g instead of 130 g still deposits ~3 g — the surplus is upkeep + fuel. Training + time drive deposition, not extra grams."),
 h("Keeping MPS elevated all day (and all week)"),
 fig("genPCTimeline","A workout raises/sensitises MPS for ~24–48 h (the shaded envelope). Each protein feeding spikes MPS for ~2–3 h. Spread 3–4 feeds across the day to keep re-triggering it; train again next day to re-lift the envelope."),
 p("<b>Spreading logic:</b> each meal maxes MPS for ~2–3 h, then it falls back and needs a dip (~3–5 h) before it responds again. So 3–4 meals of ~0.4 g/kg beat one huge meal (maxes once, wastes the rest) or six tiny ones (each may miss the threshold). Over a week of near-daily training + regular protein, MPS stays chronically elevated → muscle accrues."),
 h("The thumb rule"),
 cards([
   {"h":"Minimum — RDA 0.8 g/kg","x":"Only avoids deficiency (sedentary). 68 kg → 54 g. Not enough for training."},
   {"h":"Optimal — 1.6–2.2 g/kg","x":"Build &amp; keep muscle. 68 kg → 109–150 g. ~1.6 covers most; go higher when lean/advanced."},
   {"h":"Cutting — ~2.2 g/kg","x":"In a deficit, the high end protects muscle. 68 kg → ~150 g."}]),
 call("<b>Cue.</b> Hit ~0.4 g/kg protein at 3–4 meals, total ~1.6–2.2 g/kg/day, train regularly. That keeps MPS maxed all day and rides the training envelope — the actual recipe for the ~3 g/day of new muscle."),
]

# interactive toggle section (before the final cue)
blocks.insert(len(blocks)-1, h("See each target as a flow — toggle the four goals"))
blocks.insert(len(blocks)-1, {"t":"psankey"})

tab={"id":"pdose","name":"Protein · dosing & MPS","icon":"\U0001F373",
  "intro":"What 0.4 g/kg means, the per-meal ceiling, and how to keep MPS elevated — with the graphs.",
  "topics":[{"id":"main","name":"Dosing & MPS","blurb":"g/kg, the ceiling, spreading, and the thumb rule.","blocks":blocks}]}
data["tabs"]=[t for t in data["tabs"] if t.get("id")!="pdose"]
# insert right after the protein concept map (pmap) if present, else append
ids=[t["id"] for t in data["tabs"]]
if "pmap" in ids:
    data["tabs"].insert(ids.index("pmap")+1, tab)
else:
    data["tabs"].append(tab)

page=page[:ob]+json.dumps(data,ensure_ascii=False)+after
open(os.path.join(REPO,"nutrition.html"),"w",encoding="utf-8").write(page)
co=zlib.compressobj(9,zlib.DEFLATED,-15);raw=co.compress(page.encode())+co.flush()
newval="RAW:"+base64.b64encode(raw).decode()
src2=re.sub(r'("nutrition\.html":\s*")RAW:[^"]*(")',lambda m:m.group(1)+newval+m.group(2),src,count=1)
open(HUB,"w",encoding="utf-8",errors="surrogatepass").write(src2)

back=zlib.decompress(base64.b64decode(re.search(r'"nutrition\.html":\s*"RAW:([^"]*)"',open(HUB,encoding="utf-8",errors="surrogatepass").read()).group(1)),-15).decode()
ob2=back.find("{",back.find("var DATA="));d2=json.loads(back[ob2:find_obj_end(back,ob2)+1])
print("tabs:",[t["id"] for t in d2["tabs"]])
print("PC gens:", all(g in back for g in ("function genPCDose(","function genPCDaily(","function genPCTimeline(")))
print("OK")
