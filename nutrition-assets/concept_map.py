# -*- coding: utf-8 -*-
import math, os
OUT="/sessions/lucid-blissful-curie/mnt/outputs"

def mix(hex1, t, hex2="#ffffff"):
    a=[int(hex1[i:i+2],16) for i in (1,3,5)]; b=[int(hex2[i:i+2],16) for i in (1,3,5)]
    c=[round(a[i]+(b[i]-a[i])*t) for i in range(3)]
    return "#%02x%02x%02x"%tuple(c)
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

NODES={}
def N(id,x,y,color,title,sub,R=62):
    NODES[id]=dict(x=x,y=y,color=color,title=title,sub=sub,R=R)

def node_svg(n):
    x,y,R,col=n["x"],n["y"],n["R"],n["color"]
    ring=mix(col,0.55); s=[]
    s.append(f'<circle cx="{x}" cy="{y}" r="{R+9}" fill="none" stroke="{ring}" stroke-width="5"/>')
    s.append(f'<circle cx="{x}" cy="{y}" r="{R+4}" fill="#f7f8fa"/>')
    s.append(f'<circle cx="{x}" cy="{y}" r="{R}" fill="{col}"/>')
    # title (1-2 lines)
    lines=n["title"].split("\n"); n_l=len(lines)
    ty=y-(4 if not n["sub"] else 10)-(n_l-1)*9
    for i,ln in enumerate(lines):
        s.append(f'<text x="{x}" y="{ty+i*18}" text-anchor="middle" fill="#ffffff" font-size="16" font-weight="700" font-family="Helvetica,Arial,sans-serif">{esc(ln)}</text>')
    if n["sub"]:
        s.append(f'<text x="{x}" y="{ty+n_l*18+2}" text-anchor="middle" fill="{mix(col,0.78)}" font-size="12" font-style="italic" font-family="Helvetica,Arial,sans-serif">{esc(n["sub"])}</text>')
    # + badge
    bx,by=x+R*0.72, y-R*0.72
    s.append(f'<circle cx="{bx}" cy="{by}" r="11" fill="#ffffff" stroke="{mix(col,0.35)}" stroke-width="1"/>')
    s.append(f'<text x="{bx}" y="{by+4}" text-anchor="middle" fill="{col}" font-size="15" font-weight="700" font-family="Helvetica,Arial,sans-serif">+</text>')
    return "".join(s)

EDGES=[]
def E(a,b,label,curve=0.16,color=None,dash=None):
    EDGES.append(dict(a=a,b=b,label=label,curve=curve,color=color,dash=dash))

def edge_svg(e):
    A,B=NODES[e["a"]],NODES[e["b"]]
    x1,y1,x2,y2=A["x"],A["y"],B["x"],B["y"]
    dx,dy=x2-x1,y2-y1; d=math.hypot(dx,dy) or 1; ux,uy=dx/d,dy/d
    r1=A["R"]+11; r2=B["R"]+18
    sx,sy=x1+ux*r1, y1+uy*r1
    ex,ey=x2-ux*r2, y2-uy*r2
    mx,my=(sx+ex)/2,(sy+ey)/2
    # perpendicular control offset
    px,py=-uy,ux; off=e["curve"]*d
    cxp,cyp=mx+px*off, my+py*off
    col=e["color"] or A["color"]
    dash=f' stroke-dasharray="{e["dash"]}"' if e["dash"] else ""
    s=[f'<path d="M{sx:.1f},{sy:.1f} Q{cxp:.1f},{cyp:.1f} {ex:.1f},{ey:.1f}" fill="none" stroke="{col}" stroke-width="2.6"{dash} marker-end="url(#tip)" opacity="0.9"/>']
    # label pill at quad midpoint t=0.5
    lx=0.25*sx+0.5*cxp+0.25*ex; ly=0.25*sy+0.5*cyp+0.25*ey
    if e["label"]:
        w=len(e["label"])*6.6+18
        s.append(f'<rect x="{lx-w/2:.1f}" y="{ly-12:.1f}" width="{w:.1f}" height="23" rx="6" fill="#ffffff" stroke="#e3e5ea" stroke-width="1"/>')
        s.append(f'<text x="{lx:.1f}" y="{ly+4:.1f}" text-anchor="middle" fill="#5b6270" font-size="12.5" font-family="Helvetica,Arial,sans-serif">{esc(e["label"])}</text>')
    return "".join(s)

# ---- palette ----
ORANGE="#EA580C"; BLUE="#2563EB"; ROSE="#DB2777"; AMBER="#D97706"; GREEN="#15A34A"
VIOLET="#7C3AED"; TEAL="#0D9488"; CYAN="#0E7490"; MAROON="#9F1239"; DARK="#1F2937"

W,H=1330,1000
# ---- nodes (metabolism, clustered: food | molecules | switch+fuel | stores) ----
N("food",   150,470, ORANGE,"Food","what you eat")
N("glu",    420,200, BLUE,  "Glucose","from carbs")
N("aa",     430,480, ROSE,  "Amino acids","from protein")
N("fa",     405,760, AMBER, "Fatty acids","from fat")
N("ins",    700,150, GREEN, "Insulin","fed switch")
N("gly",    735,375, TEAL,  "Glycogen","carb store")
N("fuel",   890,530, VIOLET,"Fuel pool","ATP · BMR · NEAT",78)
N("musc",   735,790, CYAN,  "Muscle","protein built")
N("fat",   1105,610, MAROON,"Body fat","the big store")
N("def",   1205,345, DARK,  "Deficit","fasted state")

# ---- edges ----
E("food","glu","digests to",0.12)
E("food","aa","digests to",0.02)
E("food","fa","digests to",-0.12)
E("glu","ins","raises",0.12)
E("glu","gly","stored as",0.12)
E("glu","fuel","burned for ATP",0.22)
E("ins","gly","promotes store",0.0,color=GREEN)
E("aa","musc","if training",0.16)
E("aa","fuel","else burned",-0.10)
E("fa","fat","stored: insulin blocks burn",0.52,color=AMBER)
E("gly","fuel","when needed",0.10)
E("fat","fuel","burned",-0.12)
E("def","fat","mobilise",0.14,color=MAROON)
E("musc","fuel","if unprotected",-0.10,dash="5 5")

dots='<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="#e6e8ee"/></pattern>'
tip='<marker id="tip" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1.5 1.5L8 5L1.5 8.5" fill="none" stroke="context-stroke" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker>'
body=[edge_svg(e) for e in EDGES]+[node_svg(NODES[k]) for k in NODES]
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}">'
     f'<defs>{dots}{tip}</defs>'
     f'<rect x="0" y="0" width="{W}" height="{H}" fill="#f7f8fa"/>'
     f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#dots)"/>'
     +"".join(body)+"</svg>")
open(f"{OUT}/concept_map.svg","w").write(svg)
import cairosvg
cairosvg.svg2png(bytestring=svg.encode(),write_to=f"{OUT}/concept_map.png",output_width=W,output_height=H)
print("rendered concept map",W,"x",H,"| bytes",len(svg))
