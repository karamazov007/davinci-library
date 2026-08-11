# -*- coding: utf-8 -*-
import re, json, zlib, base64, os
REPO="/sessions/lucid-blissful-curie/mnt/davinci-library"
HUB=os.path.join(REPO,"knowledge-hub.html")
OUT="/sessions/lucid-blissful-curie/mnt/outputs"
svg=open(f"{OUT}/concept_map.svg").read().strip()
assert "`" not in svg and "${" not in svg, "svg has template-literal-breaking chars"

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

# 1) inject generator function before 'var DATA=' (only once)
fn="function genFlowMap(){return `"+svg+"`;}\n"
if "function genFlowMap()" not in page:
    anchor=page.find("var DATA=")
    page=page[:anchor]+fn+page[anchor:]
else:
    page=re.sub(r'function genFlowMap\(\)\{return `.*?`;\}\n', fn, page, count=1, flags=re.S)

# 2) add fig block into themath (after intro paragraph), only once
ob=page.find("{",page.find("var DATA="))
close=find_obj_end(page,ob)
data=json.loads(page[ob:close+1]); after=page[close+1:]
gym=[t for t in data["tabs"] if t["id"]=="gym"][0]
tm=[tp for tp in gym["topics"] if tp["id"]=="themath"][0]
# remove old flowmap fig + its heading if present
tm["blocks"]=[b for b in tm["blocks"] if not (b.get("t")=="fig" and b.get("gen")=="genFlowMap")
              and not (b.get("t")=="h" and b.get("x","").startswith("The whole picture"))]
flow_h={"t":"h","x":"The whole picture — one map, start to end"}
flow_fig={"t":"fig","gen":"genFlowMap","cap":"The whole loop: food digests to glucose / amino acids / fatty acids; insulin (fed) promotes storage and blocks fat-burn (so dietary fat is stored); glucose burns for ATP or fills glycogen; protein builds muscle only if a training signal is present, else it's burned; in a deficit the stores reverse and feed the fuel pool. A living map — we keep making it more exhaustive."}
tm["blocks"]=[tm["blocks"][0], flow_h, flow_fig]+tm["blocks"][1:]

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
print("genFlowMap in page:", "function genFlowMap()" in back)
ob2=back.find("{",back.find("var DATA="))
d2=json.loads(back[ob2:find_obj_end(back,ob2)+1])
tm2=[tp for tp in [t for t in d2["tabs"] if t["id"]=="gym"][0]["topics"] if tp["id"]=="themath"][0]
print("themath first blocks:",[ (b["t"], b.get("gen") or (b.get("x","")[:28])) for b in tm2["blocks"][:4]])
print("OK")
