# -*- coding: utf-8 -*-
import json
OUT="/sessions/lucid-blissful-curie/mnt/outputs"
INK="#1c2431";MUT="#5b6572";CYAN="#0891b2";AMBER="#d97706";ROSE="#db2777";SLATE="#64748b";BLUE="#2563eb";VIOLET="#7c3aed";GREEN="#16a34a";MAROON="#9f1239"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def T(x,y,t,fs=11,fill=INK,anc="middle",fw=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anc}" fill="{fill}" font-size="{fs}" font-weight="{fw}" font-family="Helvetica,Arial,sans-serif">{esc(t)}</text>'
def band(xa,yat,yab,xb,ybt,ybb,color,op=0.40):
    mx=(xa+xb)/2
    return (f'<path d="M{xa:.1f},{yat:.1f} C{mx:.1f},{yat:.1f} {mx:.1f},{ybt:.1f} {xb:.1f},{ybt:.1f} '
            f'L{xb:.1f},{ybb:.1f} C{mx:.1f},{ybb:.1f} {mx:.1f},{yab:.1f} {xa:.1f},{yab:.1f} Z" fill="{color}" opacity="{op}"/>')

# node meta: id -> (label, color, column)
META={
 "carbs":("Carbs",CYAN,0),"fat":("Fat",AMBER,0),"protein":("Protein 130 g",ROSE,0),
 "run":("Run body (BMR+NEAT)",SLATE,1),"train":("Train + recover",BLUE,1),"atp":("ATP to BUILD",VIOLET,1),
 "horm":("Hormone support",GREEN,1),"fstore":("Fat store",MAROON,1),"pool":("Amino-acid pool",ROSE,1),
 "muscle":("MUSCLE-building",GREEN,2),"spent":("Spent / burned",SLATE,2),"stored":("Stored as fat",MAROON,2)}
ORDER={0:["carbs","fat","protein"],1:["run","train","atp","horm","fstore","pool"],2:["muscle","spent","stored"]}
COLX={0:(90,116),1:(470,494),2:(830,854)}   # (left,right) x of node rects
SCALE=0.156; GAP=22; TOP=70; MAXKC=2310

def make(F):  # F: dict of flow magnitudes
    # node values from flows
    nv={
     "carbs":F["c_train"]+F["c_atp"]+F["c_run"]+F.get("c_fstore",0),
     "fat":F["f_horm"]+F["f_run"]+F.get("f_fstore",0),
     "protein":520,
     "run":F["c_run"]+F["f_run"],"train":F["c_train"],"atp":F["c_atp"],"horm":F["f_horm"],
     "fstore":F.get("c_fstore",0)+F.get("f_fstore",0),"pool":520,
     "muscle":F["c_atp"]+F["f_horm"]+F["bricks"],"spent":(F["c_run"]+F["f_run"])+F["c_train"]+F["pool_spent"],
     "stored":F.get("c_fstore",0)+F.get("f_fstore",0)}
    flows=[("carbs","run",F["c_run"]),("carbs","train",F["c_train"]),("carbs","atp",F["c_atp"]),
           ("fat","horm",F["f_horm"]),("fat","run",F["f_run"]),("protein","pool",520),
           ("run","spent",nv["run"]),("train","spent",F["c_train"]),
           ("atp","muscle",F["c_atp"]),("horm","muscle",F["f_horm"]),
           ("pool","spent",F["pool_spent"]),("pool","muscle",F["bricks"])]
    if nv["fstore"]>0:
        flows+=[("carbs","fstore",F.get("c_fstore",0)),("fat","fstore",F.get("f_fstore",0)),("fstore","stored",nv["fstore"])]
    # positions
    pos={}
    for col,ids in ORDER.items():
        y=TOP
        for nid in ids:
            v=nv[nid]
            if v<=0: continue
            h=v*SCALE; pos[nid]=[y,h]; y+=h+GAP
    # out/in segment offsets with ordering to reduce crossings
    def center(nid): return pos[nid][0]+pos[nid][1]/2
    outoff={}; inoff={}
    for nid in pos: outoff[nid]=pos[nid][0]; inoff[nid]=pos[nid][0]
    # order flows for each source by target center, each target by source center — assign segments
    from collections import defaultdict
    outs=defaultdict(list); ins=defaultdict(list)
    for i,(s,t,v) in enumerate(flows): outs[s].append(i); ins[t].append(i)
    seg={}  # i -> (s_top,s_bot,t_top,t_bot)
    for s,lst in outs.items():
        lst.sort(key=lambda i: center(flows[i][1]))
        for i in lst:
            v=flows[i][2]*SCALE; seg[i]=[outoff[s],outoff[s]+v,None,None]; outoff[s]+=v
    for t,lst in ins.items():
        lst.sort(key=lambda i: center(flows[i][0]))
        for i in lst:
            v=flows[i][2]*SCALE; seg[i][2]=inoff[t]; seg[i][3]=inoff[t]+v; inoff[t]+=v
    s=[]
    for i,(a,b,v) in enumerate(flows):
        col=META[a][1]; xa=COLX[META[a][2]][1]; xb=COLX[META[b][2]][0]
        st_,sb_,tt_,tb_=seg[i]; s.append(band(xa,st_,sb_,xb,tt_,tb_,col))
    # nodes + labels
    for nid,(y,h) in pos.items():
        lab,col,c=META[nid]; lx,rx=COLX[c]
        s.append(f'<rect x="{lx}" y="{y:.1f}" width="{rx-lx}" height="{h:.1f}" rx="3" fill="{col}"/>')
        if c==0:
            s.append(T(lx-8,y+h/2-3,lab,11.5,INK,"end",700)); s.append(T(lx-8,y+h/2+12,f"{int(nv[nid])} kcal",10.5,MUT,"end"))
        elif c==1:
            s.append(T((lx+rx)/2,y-6,lab,10.5,INK,"middle",700))
        else:
            extra="  ▲" if nid=="muscle" else ""
            s.append(T(rx+8,y+h/2-3,lab+extra,11.5,(GREEN if nid=="muscle" else INK),"start",700)); s.append(T(rx+8,y+h/2+12,f"{int(nv[nid])} kcal",10.5,MUT,"start"))
    return "".join(s),nv

W,H=980,600
CFG={
 "cut":dict(title="Cut · 1,680 kcal",c_run=375,c_train=250,c_atp=40,f_horm=45,f_run=450,pool_spent=508,bricks=12),
 "maintenance":dict(title="Maintenance · 2,100 kcal",c_run=630,c_train=320,c_atp=90,f_horm=55,f_run=485,pool_spent=506,bricks=14),
 "bulk":dict(title="Lean bulk · 2,310 kcal",c_run=575,c_train=420,c_atp=180,f_horm=70,f_run=485,c_fstore=30,f_fstore=30,pool_spent=500,bricks=20),
}
svgs={}
for k,F in CFG.items():
    body,nv=make(F)
    hdr=T(W/2,40,F["title"]+"  —  where each macro's energy goes, and where the 130 g protein goes",13,INK,"middle",700)
    foot=T(W/2,H-14,"Muscle-building needs BOTH: ATP labour (energy) + amino-acid bricks (protein) + hormone support. Surplus funds all three; a deficit starves them.",11,MUT,"middle")
    svgs[k]=f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}">{hdr}{body}{foot}</svg>'
    print(k,"muscle kcal:",int(nv["muscle"]))
json.dump(svgs,open(f"{OUT}/mech_sk.json","w"),ensure_ascii=False)
import cairosvg
order=["cut","maintenance","bulk"];parts=[]
for i,k in enumerate(order):
    inner=svgs[k].split(">",1)[1].rsplit("</svg>",1)[0]; parts.append(f'<g transform="translate(0,{i*H})">{inner}</g>')
comp=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" viewBox="0 0 {W} {H*3}"><rect width="{W}" height="{H*3}" fill="#fff"/>'+"".join(parts)+"</svg>"
cairosvg.svg2png(bytestring=comp.encode(),write_to=f"{OUT}/mech_verify.png",output_width=W,output_height=H*3)
print("rendered")
