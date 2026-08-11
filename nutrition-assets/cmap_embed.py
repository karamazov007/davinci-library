# -*- coding: utf-8 -*-
import re, json, zlib, base64, os
REPO="/sessions/lucid-blissful-curie/mnt/davinci-library"
HUB=os.path.join(REPO,"knowledge-hub.html")
OUT="/sessions/lucid-blissful-curie/mnt/outputs"

engine=open(f"{OUT}/cmap_engine.js").read()
dj_nutri=open(f"{OUT}/cmap_data.json").read().strip()
dj_prot=open(f"{OUT}/cmap_protein_data.json").read().strip()
JSBLOCK=("/*NCMJS*/var NCM_DATA_nutrition="+dj_nutri+";\nvar NCM_DATA_protein="+dj_prot
         +";\nvar NCM_MAPS={nutrition:NCM_DATA_nutrition,protein:NCM_DATA_protein};\n"+engine+"/*ENCMJS*/\n")
assert "</script" not in JSBLOCK

CSS=("/*NCMCSS*/"
".ncm-root{position:relative;width:100%;height:70vh;background:#f7f8fa;overflow:hidden}"
".ncm-bleed{position:fixed;left:0;right:0;bottom:0;top:var(--ncm-top,58px);width:auto;height:auto;z-index:45;background:#f7f8fa}"
".ncm-stage{position:absolute;inset:0}"
".ncm-svg{width:100%;height:100%;display:block;touch-action:none;cursor:grab;background:#f7f8fa}"
".ncm-svg.grab{cursor:grabbing}"
".ncm-toolbar{position:absolute;top:14px;right:18px;display:flex;gap:10px;align-items:center;background:#fff;border:1px solid #e7e9ee;border-radius:22px;padding:8px 16px;box-shadow:0 2px 12px rgba(20,25,40,.10)}"
".ncm-zlabel{font-size:12px;color:#8b93a1;font-family:Helvetica,Arial,sans-serif}"
".ncm-slider{width:170px;accent-color:#7c3aed}"
".ncm-hint{position:absolute;left:18px;bottom:16px;font-size:12px;color:#8b93a1;background:#fff;border:1px solid #e7e9ee;border-radius:8px;padding:6px 11px}"
"body.cmap-active .ntoc{display:none!important}"
"body.cmap-active .nmain{padding:0!important}"
".ncm-node text,.ncm-edge text{font-family:Helvetica,Arial,sans-serif}"
".ncm-child,.ncm-cedge{transition:opacity .18s ease}"
"/*ENCMCSS*/")

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

def rep(s,a,b,n=1):
    assert s.count(a)>=n, "missing: "+a[:40]
    return s.replace(a,b,n)

# idempotency: strip ALL prior cmap injections
page=re.sub(r'/\*NCMCSS\*/.*?/\*ENCMCSS\*/','',page,flags=re.S)
page=re.sub(r'/\*NCMJS\*/.*?/\*ENCMJS\*/\n?','',page,flags=re.S)
page=re.sub(r'var NCM_DATA=[\s\S]*?\}\)\(\);\n?','',page,count=1)  # migrate old single-map engine
page=re.sub(r'case "cmap": return \'<div class="ncm-root" data-cmap="[\s\S]*?</div>\';\n   ','',page)
page=page.replace('try{NCM.mountAll();}catch(_){}','')

# 1 CSS
page=rep(page,"</style>",CSS+"</style>")
# 2 engine + both datasets + registry
if "/*NCMJS*/" not in page:
    page=rep(page,"var DATA=",JSBLOCK+"var DATA=")
# 3 block type (map key from block, default nutrition)
page=rep(page,'case "p":','case "cmap": return \'<div class="ncm-root" data-cmap="\'+((b.map)||"nutrition")+\'"></div>\';\n   case "p":')
# 4 mount hooks
page=rep(page,"stage.innerHTML=renderTab(tabById(id));","stage.innerHTML=renderTab(tabById(id));try{NCM.mountAll();}catch(_){}")
page=rep(page,"stage.innerHTML=renderTab(T);","stage.innerHTML=renderTab(T);try{NCM.mountAll();}catch(_){}")

# 5 add tab
ob=page.find("{",page.find("var DATA="));close=find_obj_end(page,ob)
data=json.loads(page[ob:close+1]);after=page[close+1:]
data["tabs"]=[t for t in data["tabs"] if t.get("id") not in ("cmap","pmap")]
data["tabs"].append({"id":"cmap","name":"Nutrition Concept Map","icon":"\U0001F5FA️",
  "intro":"Pan, zoom, and click the + on any node to open it up.",
  "topics":[{"id":"map","name":"Interactive map","blurb":"Food to molecules to fates to stores — fully explorable.","blocks":[{"t":"cmap","map":"nutrition"}]}]})
data["tabs"].append({"id":"pmap","name":"Protein Concept Map","icon":"\U0001F9EC",
  "intro":"Follow a gram of protein from plate to muscle (or fuel). Pan, zoom, click the + on any node.",
  "topics":[{"id":"map","name":"Interactive map","blurb":"Protein → amino acids → build / burn / recycle.","blocks":[{"t":"cmap","map":"protein"}]}]})
page=page[:ob]+json.dumps(data,ensure_ascii=False)+after
open(os.path.join(REPO,"nutrition.html"),"w",encoding="utf-8").write(page)

# re-embed
co=zlib.compressobj(9,zlib.DEFLATED,-15);raw=co.compress(page.encode())+co.flush()
newval="RAW:"+base64.b64encode(raw).decode()
src2=re.sub(r'("nutrition\.html":\s*")RAW:[^"]*(")',lambda m:m.group(1)+newval+m.group(2),src,count=1)
open(HUB,"w",encoding="utf-8",errors="surrogatepass").write(src2)

# verify
back=zlib.decompress(base64.b64decode(re.search(r'"nutrition\.html":\s*"RAW:([^"]*)"',open(HUB,encoding="utf-8",errors="surrogatepass").read()).group(1)),-15).decode()
ob2=back.find("{",back.find("var DATA="));d2=json.loads(back[ob2:find_obj_end(back,ob2)+1])
print("tabs:",[t["id"] for t in d2["tabs"]])
print("engine:", back.count("var NCM=(function()"),"| nutri data:", "var NCM_DATA_nutrition=" in back,"| protein data:", "var NCM_DATA_protein=" in back,"| registry:", "var NCM_MAPS=" in back)
print("css markers:", back.count("/*NCMCSS*/"),"| js markers:", back.count("/*NCMJS*/"),"| hooks:", back.count("NCM.mountAll()"))
print("OK")
