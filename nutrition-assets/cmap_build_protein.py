# -*- coding: utf-8 -*-
import math, json
OUT="/sessions/lucid-blissful-curie/mnt/outputs"
def mix(h1,t,h2="#ffffff"):
    a=[int(h1[i:i+2],16) for i in (1,3,5)];b=[int(h2[i:i+2],16) for i in (1,3,5)]
    return "#%02x%02x%02x"%tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
ORANGE="#EA580C";BLUE="#2563EB";ROSE="#DB2777";AMBER="#D97706";GREEN="#15A34A"
VIOLET="#7C3AED";TEAL="#0D9488";CYAN="#0E7490";MAROON="#9F1239";DARK="#1F2937";SUN="#CA8A04";CY2="#0891B2"

M={}
def N(id,x,y,color,title,sub,r=66): M[id]=dict(id=id,x=x,y=y,color=color,title=title,sub=sub,r=r,child=False,parent=None)
N("prot",180,660,ORANGE,"Dietary protein","what you eat")
N("aa",500,660,ROSE,"Amino acids","after digestion")
N("fp",820,660,GREEN,"Gut + liver","first-pass toll")
N("pool",1140,660,BLUE,"Amino-acid pool","small, circulating")
N("turn",1140,320,CY2,"Turnover river","~250–300 g/day")
N("synth",1470,440,TEAL,"Protein synthesis","all tissues")
N("musc",1800,440,CYAN,"Muscle","MPS − MPB")
N("other",1470,680,VIOLET,"Other molecules","creatine, etc.")
N("burn",1470,1000,AMBER,"Oxidised for fuel","deaminated")
N("urea",1800,1000,DARK,"Urea","N out in urine")
N("target",500,300,MAROON,"Your target","~140 g = 2 g/kg")
N("ex",820,1000,SUN,"40 g meal","worked example")

CH={
 "prot":[("4 kcal/g",-30,-160),("~16% nitrogen",140,-130),("NO storage tank",120,150)],
 "aa":[("20 types",-30,-165),("9 essential",150,-120)],
 "fp":[("gut burns\nglutamine",-40,-170),("liver: albumin,\nurea",150,-130),("~20–50%\ntaken here",190,60)],
 "pool":[("small &\ntransient",-30,175),("kept low",180,120)],
 "turn":[("~250–300\ng/day",-40,-160),("mostly\nrecycled",170,-90)],
 "synth":[("switch =\nleucine",30,-175),("saturates\n~0.4 g/kg/meal",-30,-185)],
 "musc":[("net ~3 g/day",120,-150),("sensitised\n24–48 h",170,60),("spread\nyour meals",120,175)],
 "burn":[("deaminate:\nstrip N",-40,175),("carbon → ATP\n/ glucose",180,110),("only the\nsurplus",180,-60)],
 "other":[("creatine",190,-60),("neuro-\ntransmitters",200,60),("glutathione",120,170)],
 "target":[("RDA 0.8 g/kg\n(minimum)",-40,-165),("optimal\n1.6–2.2 g/kg",150,-130),("cut → 2.2",180,60),("nitrogen\nbalance",120,170)],
 "ex":[("~10–15 g\ngut/liver",-40,175),("~25–30 g\nto blood",170,140),("net ~1–3 g\nmuscle",200,20),("rest →\nfuel/turnover",120,-165)],
}
_mains=[n for n in M.values() if not n["child"]]
_cx=sum(n["x"] for n in _mains)/len(_mains); _cy=sum(n["y"] for n in _mains)/len(_mains)
def _child_layout(p,k):
    ang0=math.atan2(p["y"]-_cy, p["x"]-_cx)
    span=math.radians(40*(k-1)+30) if k>1 else 0
    Rc=150+25*(k-1)
    return [ang0 + (-span/2 + (i*span/(k-1) if k>1 else 0)) for i in range(k)], Rc
for pid,lst in CH.items():
    p=M[pid]; angs,Rc=_child_layout(p,len(lst))
    for i,item in enumerate(lst):
        cid=pid+"_c"+str(i); a=angs[i]
        M[cid]=dict(id=cid,x=p["x"]+Rc*math.cos(a),y=p["y"]+Rc*math.sin(a),
            color=p["color"],title=item[0],sub="",r=46,child=True,parent=pid)

E=[]
def ed(a,b,label,curve=0.12,color=None,dash=None,parent=None): E.append(dict(a=a,b=b,label=label,curve=curve,color=color,dash=dash,parent=parent))
ed("prot","aa","digest (pepsin, proteases)",0.10)
ed("aa","fp","portal → liver",0.0)
ed("fp","pool","what passes through",0.10)
ed("fp","burn","gut/liver use + disposal",0.16,color=GREEN)
ed("pool","synth","MPS · leucine switch",0.14)
ed("pool","other","precursors",0.0)
ed("pool","burn","excess (no store)",-0.14,color=AMBER)
ed("synth","musc","training amplifies",0.0)
ed("musc","turn","MPB · constant breakdown",0.22,dash="6 6")
ed("turn","pool","recycled amino acids",0.14,color=CY2)
ed("burn","urea","nitrogen → urea",0.0)
ed("prot","target","how much to eat?",-0.16,color=MAROON,dash="5 5")
ed("aa","ex","e.g. 40 g",0.22,color=SUN)
for pid,lst in CH.items():
    for i in range(len(lst)):
        ed(pid,pid+"_c"+str(i),"",0.0,color=mix(M[pid]["color"],0.35),parent=pid)

W,H=2040,1360
def node_svg(n):
    x,y,R,col=n["x"],n["y"],n["r"],n["color"];ring=mix(col,0.55);s=[]
    if n["child"]:
        s.append(f'<circle cx="{x}" cy="{y}" r="{R+6}" fill="none" stroke="{mix(col,0.6)}" stroke-width="4"/>')
        s.append(f'<circle cx="{x}" cy="{y}" r="{R+2}" fill="#f7f8fa"/>')
        s.append(f'<circle cx="{x}" cy="{y}" r="{R}" fill="{mix(col,0.16)}"/>')
        lines=n["title"].split("\n");ty=y-(len(lines)-1)*9+4
        for i,ln in enumerate(lines):
            s.append(f'<text x="{x}" y="{ty+i*17}" text-anchor="middle" fill="#fff" font-size="13" font-weight="700" font-family="Helvetica,Arial,sans-serif">{esc(ln)}</text>')
        return "".join(s)
    s.append(f'<circle cx="{x}" cy="{y}" r="{R+9}" fill="none" stroke="{ring}" stroke-width="5"/>')
    s.append(f'<circle cx="{x}" cy="{y}" r="{R+4}" fill="#f7f8fa"/>')
    s.append(f'<circle cx="{x}" cy="{y}" r="{R}" fill="{col}"/>')
    lines=n["title"].split("\n");nl=len(lines);ty=y-(10 if n["sub"] else 4)-(nl-1)*9
    for i,ln in enumerate(lines):
        s.append(f'<text x="{x}" y="{ty+i*18}" text-anchor="middle" fill="#fff" font-size="16" font-weight="700" font-family="Helvetica,Arial,sans-serif">{esc(ln)}</text>')
    if n["sub"]:
        s.append(f'<text x="{x}" y="{ty+nl*18+2}" text-anchor="middle" fill="{mix(col,0.78)}" font-size="12" font-style="italic" font-family="Helvetica,Arial,sans-serif">{esc(n["sub"])}</text>')
    bx,by=x+R*0.72,y-R*0.72
    s.append(f'<circle cx="{bx}" cy="{by}" r="12" fill="#fff" stroke="{mix(col,0.35)}"/><text x="{bx}" y="{by+5}" text-anchor="middle" fill="{col}" font-size="16" font-weight="700" font-family="Helvetica,Arial,sans-serif">+</text>')
    return "".join(s)
def edge_svg(e):
    A=M[e["a"]],;A=M[e["a"]];B=M[e["b"]];x1,y1,x2,y2=A["x"],A["y"],B["x"],B["y"]
    dx,dy=x2-x1,y2-y1;d=math.hypot(dx,dy) or 1;ux,uy=dx/d,dy/d
    sx,sy=x1+ux*(A["r"]+9),y1+uy*(A["r"]+9);ex,ey=x2-ux*(B["r"]+16),y2-uy*(B["r"]+16)
    mx,my=(sx+ex)/2,(sy+ey)/2;px,py=-uy,ux;off=e["curve"]*d;cxp,cyp=mx+px*off,my+py*off
    col=e["color"] or A["color"];dash=f' stroke-dasharray="{e["dash"]}"' if e["dash"] else "";w=2.0 if e["parent"] else 2.6
    s=[f'<path d="M{sx:.1f},{sy:.1f} Q{cxp:.1f},{cyp:.1f} {ex:.1f},{ey:.1f}" fill="none" stroke="{col}" stroke-width="{w}"{dash} marker-end="url(#tip)" opacity="0.9"/>']
    if e["label"]:
        lx=0.25*sx+0.5*cxp+0.25*ex;ly=0.25*sy+0.5*cyp+0.25*ey;wd=len(e["label"])*6.6+18
        s.append(f'<rect x="{lx-wd/2:.1f}" y="{ly-12:.1f}" width="{wd:.1f}" height="23" rx="6" fill="#fff" stroke="#e3e5ea"/><text x="{lx:.1f}" y="{ly+4:.1f}" text-anchor="middle" fill="#5b6270" font-size="12.5" font-family="Helvetica,Arial,sans-serif">{esc(e["label"])}</text>')
    return "".join(s)
def render(expanded):
    vis=set(k for k,n in M.items() if not n["child"]) | set(k for k,n in M.items() if n["child"] and n["parent"] in expanded)
    eds=[e for e in E if (e["parent"] is None) or (e["parent"] in expanded)]
    dots='<pattern id="dots" width="30" height="30" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="#e6e8ee"/></pattern>'
    tip='<marker id="tip" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1.5 1.5L8 5L1.5 8.5" fill="none" stroke="context-stroke" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker>'
    body="".join(edge_svg(e) for e in eds if e["a"] in vis and e["b"] in vis)+"".join(node_svg(M[k]) for k in M if k in vis)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}"><defs>{dots}{tip}</defs>'
            f'<rect width="{W}" height="{H}" fill="#f7f8fa"/><rect width="{W}" height="{H}" fill="url(#dots)"/>'+body+"</svg>")
import cairosvg
cairosvg.svg2png(bytestring=render(set()).encode(),write_to=f"{OUT}/cmap_protein_collapsed.png",output_width=W,output_height=H)
cairosvg.svg2png(bytestring=render(set(CH.keys())).encode(),write_to=f"{OUT}/cmap_protein_all.png",output_width=W,output_height=H)
json.dump({"W":W,"H":H,"nodes":list(M.values()),"edges":E},open(f"{OUT}/cmap_protein_data.json","w"),ensure_ascii=False)
print("protein map rendered; nodes",len(M),"edges",len(E))
