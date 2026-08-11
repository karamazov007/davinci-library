# -*- coding: utf-8 -*-
import re, json, zlib, base64, os
REPO="/sessions/lucid-blissful-curie/mnt/davinci-library"
HUB=os.path.join(REPO,"knowledge-hub.html")
E="#4f46e5"; P="#db2777"; Cb="#0891b2"; F="#ea580c"; Fi="#16a34a"; V="#9333ea"; Am="#d97706"; Ink="#1c2431"; Sl="#64748b"

def p(x): return {"t":"p","x":x}
def h(x): return {"t":"h","x":x}
def call(x): return {"t":"call","x":x}
def cards(items): return {"t":"cards","items":items}
def fig(gen,cap,args): return {"t":"fig","gen":gen,"cap":cap,"args":args}

# ---- the switchboard, built with the page's genGraph ----
N=[
 {"id":"sw","x":0.5,"y":0.07,"label":"Master switch\ninsulin = store · glucagon = burn","fill":Ink,"shape":"rect","w":330,"h":48},
 {"id":"ch","x":0.17,"y":0.30,"label":"Carbs\n→ glucose","fill":Cb,"w":150,"h":50},
 {"id":"c1","x":0.17,"y":0.52,"label":"1 · burn for ATP","fill":Cb,"w":158,"h":46},
 {"id":"c2","x":0.17,"y":0.72,"label":"2 · glycogen\nsmall tank","fill":Cb,"w":158,"h":52},
 {"id":"c3","x":0.17,"y":0.93,"label":"3 · overflow → fat\nsurplus only","fill":Cb,"w":168,"h":52},
 {"id":"ph","x":0.5,"y":0.30,"label":"Protein\n→ amino acids","fill":P,"w":160,"h":50},
 {"id":"p1","x":0.5,"y":0.52,"label":"1 · build proteins\nif training","fill":P,"w":168,"h":52},
 {"id":"p2","x":0.5,"y":0.72,"label":"2 · burn / → glucose","fill":P,"w":168,"h":46},
 {"id":"p3","x":0.5,"y":0.93,"label":"no storage tank\nuse it or lose it","fill":Sl,"w":168,"h":52},
 {"id":"fh","x":0.83,"y":0.30,"label":"Fat\n→ fatty acids","fill":F,"w":150,"h":50},
 {"id":"f1","x":0.83,"y":0.52,"label":"1 · structural\nsmall, ongoing","fill":F,"w":158,"h":52},
 {"id":"f2","x":0.83,"y":0.72,"label":"2 · store\nfed / insulin","fill":F,"w":158,"h":52},
 {"id":"f3","x":0.83,"y":0.93,"label":"3 · burn\ndeficit / fasted","fill":F,"w":158,"h":52},
]
Ed=[
 {"from":"sw","to":"ch"},{"from":"sw","to":"ph"},{"from":"sw","to":"fh"},
 {"from":"ch","to":"c1"},{"from":"c1","to":"c2"},{"from":"c2","to":"c3"},
 {"from":"ph","to":"p1"},{"from":"p1","to":"p2"},{"from":"p2","to":"p3"},
 {"from":"fh","to":"f1"},{"from":"f1","to":"f2"},{"from":"f2","to":"f3"},
]
switchboard=fig("genGraph","Allocation is live, not a daily queue: hormones + each cell's energy need + tank space decide the split minute-by-minute. Muscle only grabs amino acids when training flips its switch on.",
  [N,Ed,{"w":700,"h":600}])

alloc_blocks=[
  h("How the split is decided (fuel vs building blocks)"),
  p("It is <b>not sequential</b> — the fuel pool doesn’t take its share for the day and hand leftovers to storage. Allocation runs <b>continuously and in parallel</b>: at any instant some cells burn glucose while others store it. Three live dials decide the split — <b>cellular energy charge</b>, <b>hormones (insulin vs glucagon)</b>, and <b>tissue demand + tank space</b>."),
  switchboard,
  cards([
    {"h":"Dial 1 · energy charge","x":"Each cell senses its own ATP. Low (AMPK) → burn incoming fuel now. High (mTOR) → store or build."},
    {"h":"Dial 2 · insulin","x":"Fed → insulin rises = store &amp; build, and it switches fat-burning OFF. Fasted/deficit → glucagon/adrenaline = mobilise &amp; burn."},
    {"h":"Dial 3 · tank + demand","x":"Glycogen = small fixed tank (fills fast, overflows). Fat = near-unlimited. Muscle protein = NO tank — build now or the amino acids get burned."}]),
  call("<b>Each store has its own bricks AND its own switch:</b> glycogen ← glucose (switch: insulin + empty tank) · fat ← fatty acids / excess (switch: insulin / surplus) · muscle ← amino acids (switch: <b>training</b>). That last one is why the same protein becomes muscle in a trained person and fuel in an untrained one."),
]

# ---- load, brace-match, rebuild themath topic with allocation inserted after equations ----
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
    raise ValueError("no end")

src=open(HUB,"r",encoding="utf-8",errors="surrogatepass").read()
m=re.search(r'"nutrition\.html":\s*"RAW:([^"]*)"',src)
page=zlib.decompress(base64.b64decode(m.group(1)),-15).decode("utf-8")
ob=page.find("{",page.find("var DATA="))
close=find_obj_end(page,ob)
data=json.loads(page[ob:close+1]); after=page[close+1:]

gym=[t for t in data["tabs"] if t["id"]=="gym"][0]
tm=[tp for tp in gym["topics"] if tp["id"]=="themath"][0]

# guard: if allocation already added, remove old copy first
tm["blocks"]=[b for b in tm["blocks"] if not (b.get("t")=="h" and b.get("x","").startswith("How the split is decided"))
              and not (b.get("t")=="fig" and b.get("gen")=="genGraph" and isinstance(b.get("args"),list) and any(isinstance(n,dict) and n.get("id")=="sw" for n in (b["args"][0] if b["args"] else [])))
              and not (b.get("t")=="p" and b.get("x","").startswith("It is <b>not sequential"))
              and not (b.get("t")=="cards" and any(it.get("h","").startswith("Dial 1") for it in b.get("items",[])))
              and not (b.get("t")=="call" and b.get("x","").startswith("<b>Each store has its own bricks"))]

# find index of the equations call block (starts with "<b>The equations")
idx=next((i for i,b in enumerate(tm["blocks"]) if b.get("t")=="call" and b.get("x","").startswith("<b>The equations")), None)
if idx is None: idx=1  # fallback after intro
for j,blk in enumerate(alloc_blocks):
    tm["blocks"].insert(idx+1+j, blk)

print("themath block sequence:")
for b in tm["blocks"]:
    tag=b["t"]; lbl=b.get("x") or b.get("gen") or (b.get("items") and b["items"][0].get("h"))
    print("  -",tag,":",str(lbl)[:52])

new_json=json.dumps(data,ensure_ascii=False)
page2=page[:ob]+new_json+after
open(os.path.join(REPO,"nutrition.html"),"w",encoding="utf-8").write(page2)

co=zlib.compressobj(9,zlib.DEFLATED,-15)
raw=co.compress(page2.encode("utf-8"))+co.flush()
newval="RAW:"+base64.b64encode(raw).decode()
src2=re.sub(r'("nutrition\.html":\s*")RAW:[^"]*(")',lambda mm:mm.group(1)+newval+mm.group(2),src,count=1)
open(HUB,"w",encoding="utf-8",errors="surrogatepass").write(src2)

# verify
back=zlib.decompress(base64.b64decode(re.search(r'"nutrition\.html":\s*"RAW:([^"]*)"',open(HUB,encoding="utf-8",errors="surrogatepass").read()).group(1)),-15).decode()
ob2=back.find("{",back.find("var DATA="))
d2=json.loads(back[ob2:find_obj_end(back,ob2)+1])
print("tabs:",[t["id"] for t in d2["tabs"]])
print("OK")
