# -*- coding: utf-8 -*-
import math, json
OUT="/sessions/lucid-blissful-curie/mnt/outputs"
def mix(h1,t,h2="#ffffff"):
    a=[int(h1[i:i+2],16) for i in (1,3,5)];b=[int(h2[i:i+2],16) for i in (1,3,5)]
    return "#%02x%02x%02x"%tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

ORANGE="#EA580C";BLUE="#2563EB";ROSE="#DB2777";AMBER="#D97706";GREEN="#15A34A"
VIOLET="#7C3AED";TEAL="#0D9488";CYAN="#0E7490";MAROON="#9F1239";DARK="#1F2937";SUN="#CA8A04"

# main nodes: id -> dict
M={}
def N(id,x,y,color,title,sub,r=66): M[id]=dict(id=id,x=x,y=y,color=color,title=title,sub=sub,r=r,child=False,parent=None)
N("food",170,650,ORANGE,"Food","what you eat")
N("carb",470,350,BLUE,"Carbohydrates","")
N("prot",490,650,ROSE,"Protein","")
N("fat",470,950,AMBER,"Fat","")
N("glu",820,260,BLUE,"Glucose","blood sugar")
N("aa",840,650,ROSE,"Amino acids","")
N("fa",820,1010,AMBER,"Fatty acids","")
N("ins",1180,160,GREEN,"Insulin","fed switch")
N("gly",1120,500,TEAL,"Glycogen","carb store")
N("dnl",1520,500,VIOLET,"DNL","carbs → fat")
N("fuel",1360,760,VIOLET,"Fuel pool","ATP · BMR · NEAT",84)
N("musc",1150,1040,CYAN,"Muscle","protein built")
N("fat_b",1760,690,MAROON,"Body fat","the big store")
N("def",1860,470,DARK,"Deficit","fasted state")

# children: parent -> list of (title, dx, dy)
CH={
 "carb":[("4 kcal/g",-20,-150),("fibre subset",150,-120)],
 "prot":[("4 kcal/g",-160,110),("no storage\ntank",30,175)],
 "fat":[("9 kcal/g",-175,70),("essential\nfatty acids",-70,185)],
 "glu":[("brain fuel\n~120 g/day",-95,-190),("muscle uptake\n(GLUT4)",100,-200)],
 "aa":[("MPS gate\nmTOR · leucine",40,-175),("deaminate\n→ urea",220,-30)],
 "fa":[("store ~3%\n(cheap)",-40,190),("structural\nmembranes",-210,90)],
 "ins":[("fed = store\n& build",180,-110),("blocks fat\noxidation",210,50)],
 "gly":[("~400–500 g\ntank",-185,-15)],
 "dnl":[("costly\n~25% lost",70,-150)],
 "fuel":[("BMR 60–70%",40,175),("NEAT",210,140),("training\n(glycogen)",215,0)],
 "musc":[("hypertrophy\nMPS − MPB",70,175),("contractile\nprotein",-175,95)],
 "fat_b":[("near-\nunlimited",130,-150),("deficit →\nCO₂ + H₂O",160,130)],
 "def":[("glucagon &\nadrenaline ↑",-30,-170),("ketones &\ngluconeogen.",-160,110)],
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

# edges: (a,b,label,curve,color,dash,parent)  parent=None -> main; else shown with parent expand
E=[]
def ed(a,b,label,curve=0.14,color=None,dash=None,parent=None): E.append(dict(a=a,b=b,label=label,curve=curve,color=color,dash=dash,parent=parent))
ed("food","carb","contains",0.10);ed("food","prot","contains",0.0);ed("food","fat","contains",-0.10)
ed("carb","glu","digests to",0.10);ed("prot","aa","digests to",0.0);ed("fat","fa","digests to",-0.10)
ed("glu","ins","raises",0.10);ed("glu","gly","insulin stores",0.12);ed("glu","fuel","burns for ATP",0.22)
ed("gly","dnl","when full / fructose",0.0);ed("dnl","fat_b","carbs → fat",0.12,color=VIOLET)
ed("ins","gly","promotes",0.0,color=GREEN)
ed("aa","musc","if training",0.14);ed("aa","fuel","else burned",-0.10)
ed("fa","fat_b","stored: insulin blocks burn",0.52,color=AMBER)
ed("gly","fuel","when needed",0.16)
ed("fat_b","fuel","burned",-0.12)
ed("def","fat_b","mobilise",0.12,color=MAROON)
ed("musc","fuel","if unprotected",-0.10,dash="6 6")
# child edges
for pid,lst in CH.items():
    for i in range(len(lst)):
        ed(pid,pid+"_c"+str(i),"",0.0,color=mix(M[pid]["color"],0.35),parent=pid)

W,H=1980,1360
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
    A,B=M[e["a"]],M[e["b"]];x1,y1,x2,y2=A["x"],A["y"],B["x"],B["y"]
    dx,dy=x2-x1,y2-y1;d=math.hypot(dx,dy) or 1;ux,uy=dx/d,dy/d
    sx,sy=x1+ux*(A["r"]+9),y1+uy*(A["r"]+9);ex,ey=x2-ux*(B["r"]+16),y2-uy*(B["r"]+16)
    mx,my=(sx+ex)/2,(sy+ey)/2;px,py=-uy,ux;off=e["curve"]*d;cxp,cyp=mx+px*off,my+py*off
    col=e["color"] or A["color"];dash=f' stroke-dasharray="{e["dash"]}"' if e["dash"] else ""
    w= 2.0 if e["parent"] else 2.6
    s=[f'<path d="M{sx:.1f},{sy:.1f} Q{cxp:.1f},{cyp:.1f} {ex:.1f},{ey:.1f}" fill="none" stroke="{col}" stroke-width="{w}"{dash} marker-end="url(#tip)" opacity="0.9"/>']
    if e["label"]:
        lx=0.25*sx+0.5*cxp+0.25*ex;ly=0.25*sy+0.5*cyp+0.25*ey;wd=len(e["label"])*6.6+18
        s.append(f'<rect x="{lx-wd/2:.1f}" y="{ly-12:.1f}" width="{wd:.1f}" height="23" rx="6" fill="#fff" stroke="#e3e5ea"/><text x="{lx:.1f}" y="{ly+4:.1f}" text-anchor="middle" fill="#5b6270" font-size="12.5" font-family="Helvetica,Arial,sans-serif">{esc(e["label"])}</text>')
    return "".join(s)

def render(expanded):
    vis=set(k for k,n in M.items() if not n["child"]) | set(k for k,n in M.items() if n["child"] and n["parent"] in expanded)
    eds=[e for e in E if (e["parent"] is None) or (e["parent"] in expanded)]
    dots='<pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="#e6e8ee"/></pattern>'
    tip='<marker id="tip" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1.5 1.5L8 5L1.5 8.5" fill="none" stroke="context-stroke" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker>'
    body="".join(edge_svg(e) for e in eds if e["a"] in vis and e["b"] in vis)+"".join(node_svg(M[k]) for k in M if k in vis)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}"><defs>{dots}{tip}</defs>'
            f'<rect width="{W}" height="{H}" fill="#f7f8fa"/><rect width="{W}" height="{H}" fill="url(#dots)"/>'+body+"</svg>")

import cairosvg
open(f"{OUT}/cmap_collapsed.svg","w").write(render(set()))
cairosvg.svg2png(bytestring=render(set()).encode(),write_to=f"{OUT}/cmap_collapsed.png",output_width=W,output_height=H)
allp=set(CH.keys())
cairosvg.svg2png(bytestring=render(allp).encode(),write_to=f"{OUT}/cmap_all.png",output_width=W,output_height=H)
# emit DATA for the JS engine
json.dump({"W":W,"H":H,"nodes":list(M.values()),"edges":E},open(f"{OUT}/cmap_data.json","w"),ensure_ascii=False)
print("rendered collapsed + all; nodes",len(M),"edges",len(E))
