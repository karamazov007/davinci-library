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
def g(nodes,edges,w=700,hh=420): return [nodes,edges,{"w":w,"h":hh}]

accounting=fig("genGraph","Energy from every macro pours into ONE shared fuel pool (fungible). Building blocks are separate and macro-specific. In - out = change in stores.",
  g([{"id":"cin","x":0.5,"y":0.12,"label":"Calories in\n4P + 4C + 9F","fill":Ink,"w":168,"h":54},
     {"id":"fuel","x":0.27,"y":0.45,"label":"Fuel pool\n(fungible)","fill":V,"w":150,"h":52},
     {"id":"brick","x":0.73,"y":0.45,"label":"Building blocks\n(material)","fill":Fi,"w":160,"h":52},
     {"id":"spent","x":0.27,"y":0.82,"label":"Spent\nBMR·NEAT·TEF·train","fill":Sl,"w":184,"h":52},
     {"id":"stored","x":0.73,"y":0.82,"label":"Stored\nmuscle·glycogen·fat","fill":Sl,"w":184,"h":52}],
    [{"from":"cin","to":"fuel"},{"from":"cin","to":"brick"},
     {"from":"fuel","to":"spent"},{"from":"brick","to":"stored"}],700,430))

muscle=fig("genGraph","Two things build muscle: BRICKS (amino acids, only from protein) + LABOUR (ATP, from the shared pool - mostly carbs/fat).",
  g([{"id":"prot","x":0.12,"y":0.32,"label":"Dietary\nprotein","fill":P,"w":120,"h":50},
     {"id":"aa","x":0.4,"y":0.32,"label":"Amino\nacids","fill":P,"w":110,"h":50},
     {"id":"musc","x":0.72,"y":0.32,"label":"Muscle\nprotein","fill":Fi,"w":130,"h":50},
     {"id":"atp","x":0.4,"y":0.82,"label":"ATP\n(carbs/fat)","fill":V,"w":150,"h":50}],
    [{"from":"prot","to":"aa"},{"from":"aa","to":"musc"},
     {"from":"atp","to":"musc","label":"powers","color":V,"lc":V}],700,360))

trainfuel=fig("genSpectrum","A working set (10s-2min) runs mostly on muscle glycogen = carbohydrate. Fat contributes at rest/after, not during the set.",
  ["0-10 s · instant","rest / after",
   [{"pos":0.06,"label":"ATP-PC","color":V},
    {"pos":0.4,"label":"Glycogen\n(carbs)","color":Cb},
    {"pos":0.9,"label":"Fat","color":F}],
   {"w":780,"h":300,"title":"Fuel during a lift, by set duration"}])

themath={"id":"themath","name":"The math / accounting",
  "blurb":"Where every calorie goes, and how muscle is actually built.","blocks":[
   p("One misconception hides in “protein calories build muscle.” The fix: <b>energy is fungible; material is not.</b> Every macro has two jobs — a <b>fuel</b> role (calories → one shared ATP pool that powers anything) and a <b>material</b> role (bricks that are macro-specific: only protein makes muscle)."),
   accounting,
   call("<b>The equations.</b> Intake: C_in = 4·P + 4·C + 9·F. Out: C_out = BMR + TEF + NEAT + training. Balance: <b>C_in − C_out = Δstored</b>, where Δstored = 9·Δfat + 4·Δglycogen + 4·Δmuscle-protein (water ≈ 0 kcal). Nothing overrides this line."),
   h("Building muscle = bricks + labour"),
   muscle,
   call("<b>Why 140 g protein ≠ 140 g muscle.</b> 1 kg of muscle ≈ 200 g protein + 750 g water. Gaining a strong 0.5 kg/month = ~100 g protein/month ≈ <b>~3 g/day</b> actually deposited. The rest of your intake is burned for fuel or recycled into other proteins — you eat the big number to keep MPS maxed and cover inefficiency, not because muscle costs that much material."),
   h("What training actually burns"),
   trainfuel,
   cards([{"h":"“Protein calories go into muscle” — half right","x":"The amino-acid <b>material</b> that’s net-retained becomes muscle (and stores ~4 kcal/g). But the <b>energy</b> to build it is ATP from carbs/fat, and most protein you eat is burned or recycled — not deposited."},
          {"h":"“Training burns carbohydrate” — correct","x":"Lifting is fuelled by phosphocreatine then muscle glycogen (carbs). Fat/protein contribute little <b>during</b> the sets."}]),
   call("<b>Unified model.</b> One shared energy pool (calories in from any macro, calories out for everything incl. training) · separate macro-specific bricks (only protein makes muscle) · net muscle = MPS − MPB, protein supplies bricks, carbs/fat pay the ATP labour bill.")]}

# ---- load, brace-match DATA, inject topic into gym tab ----
def find_obj_end(s,start):
    depth=0;in_str=False;esc=False
    for i in range(start,len(s)):
        c=s[i]
        if in_str:
            if esc:esc=False
            elif c=='\\':esc=True
            elif c=='"':in_str=False
        else:
            if c=='"':in_str=True
            elif c=='{':depth+=1
            elif c=='}':
                depth-=1
                if depth==0:return i
    raise ValueError("no match")

src=open(HUB,"r",encoding="utf-8",errors="surrogatepass").read()
m=re.search(r'"nutrition\.html":\s*"RAW:([^"]*)"',src)
page=zlib.decompress(base64.b64decode(m.group(1)),-15).decode("utf-8")
obrace=page.find("{",page.find("var DATA="))
close=find_obj_end(page,obrace)
data=json.loads(page[obrace:close+1])
after=page[close+1:]

gym=[t for t in data["tabs"] if t["id"]=="gym"]
assert gym, "gym tab missing!"
gym=gym[0]
gym["topics"]=[tp for tp in gym["topics"] if tp.get("id")!="themath"]
# insert right after 'bigpicture'
idx=next((i for i,tp in enumerate(gym["topics"]) if tp["id"]=="bigpicture"),-1)
gym["topics"].insert(idx+1, themath)
print("gym topics now:",[tp["id"] for tp in gym["topics"]])

new_json=json.dumps(data,ensure_ascii=False)
page2=page[:obrace]+new_json+after
open(os.path.join(REPO,"nutrition.html"),"w",encoding="utf-8").write(page2)

co=zlib.compressobj(9,zlib.DEFLATED,-15)
raw=co.compress(page2.encode("utf-8"))+co.flush()
newval="RAW:"+base64.b64encode(raw).decode()
src2=re.sub(r'("nutrition\.html":\s*")RAW:[^"]*(")',lambda mm:mm.group(1)+newval+mm.group(2),src,count=1)
open(HUB,"w",encoding="utf-8",errors="surrogatepass").write(src2)

# verify roundtrip
back=zlib.decompress(base64.b64decode(re.search(r'"nutrition\.html":\s*"RAW:([^"]*)"',open(HUB,encoding="utf-8",errors="surrogatepass").read()).group(1)),-15).decode()
ob=back.find("{",back.find("var DATA="))
d2=json.loads(back[ob:find_obj_end(back,ob)+1])
print("roundtrip tabs:",[t["id"] for t in d2["tabs"]])
g2=[t for t in d2["tabs"] if t["id"]=="gym"][0]
print("themath present:", any(tp["id"]=="themath" for tp in g2["topics"]))
print("OK")
