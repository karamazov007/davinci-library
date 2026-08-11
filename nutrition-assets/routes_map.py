# -*- coding: utf-8 -*-
import math
OUT="/sessions/lucid-blissful-curie/mnt/outputs"
def mix(h1,t,h2="#ffffff"):
    a=[int(h1[i:i+2],16) for i in (1,3,5)];b=[int(h2[i:i+2],16) for i in (1,3,5)]
    return "#%02x%02x%02x"%tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
NODES={}
def N(id,x,y,color,title,sub,R=64): NODES[id]=dict(x=x,y=y,color=color,title=title,sub=sub,R=R)
def node_svg(n):
    x,y,R,col=n["x"],n["y"],n["R"],n["color"];ring=mix(col,0.55);s=[]
    s.append(f'<circle cx="{x}" cy="{y}" r="{R+9}" fill="none" stroke="{ring}" stroke-width="5"/>')
    s.append(f'<circle cx="{x}" cy="{y}" r="{R+4}" fill="#f7f8fa"/>')
    s.append(f'<circle cx="{x}" cy="{y}" r="{R}" fill="{col}"/>')
    lines=n["title"].split("\n");nl=len(lines);ty=y-(10)-(nl-1)*9
    for i,ln in enumerate(lines):
        s.append(f'<text x="{x}" y="{ty+i*18}" text-anchor="middle" fill="#fff" font-size="16" font-weight="700" font-family="Helvetica,Arial,sans-serif">{esc(ln)}</text>')
    s.append(f'<text x="{x}" y="{ty+nl*18+2}" text-anchor="middle" fill="{mix(col,0.78)}" font-size="12" font-style="italic" font-family="Helvetica,Arial,sans-serif">{esc(n["sub"])}</text>')
    bx,by=x+R*0.72,y-R*0.72
    s.append(f'<circle cx="{bx}" cy="{by}" r="11" fill="#fff" stroke="{mix(col,0.35)}" stroke-width="1"/><text x="{bx}" y="{by+4}" text-anchor="middle" fill="{col}" font-size="15" font-weight="700" font-family="Helvetica,Arial,sans-serif">+</text>')
    return "".join(s)
EDGES=[]
def E(a,b,label,curve=0.16,color=None,dash=None): EDGES.append(dict(a=a,b=b,label=label,curve=curve,color=color,dash=dash))
def edge_svg(e):
    A,B=NODES[e["a"]],NODES[e["b"]];x1,y1,x2,y2=A["x"],A["y"],B["x"],B["y"]
    dx,dy=x2-x1,y2-y1;d=math.hypot(dx,dy) or 1;ux,uy=dx/d,dy/d
    sx,sy=x1+ux*(A["R"]+11),y1+uy*(A["R"]+11);ex,ey=x2-ux*(B["R"]+18),y2-uy*(B["R"]+18)
    mx,my=(sx+ex)/2,(sy+ey)/2;px,py=-uy,ux;off=e["curve"]*d;cxp,cyp=mx+px*off,my+py*off
    col=e["color"] or A["color"];dash=f' stroke-dasharray="{e["dash"]}"' if e["dash"] else ""
    s=[f'<path d="M{sx:.1f},{sy:.1f} Q{cxp:.1f},{cyp:.1f} {ex:.1f},{ey:.1f}" fill="none" stroke="{col}" stroke-width="2.6"{dash} marker-end="url(#tip)" opacity="0.9"/>']
    lx=0.25*sx+0.5*cxp+0.25*ex;ly=0.25*sy+0.5*cyp+0.25*ey
    w=len(e["label"])*6.6+18
    s.append(f'<rect x="{lx-w/2:.1f}" y="{ly-12:.1f}" width="{w:.1f}" height="23" rx="6" fill="#fff" stroke="#e3e5ea"/><text x="{lx:.1f}" y="{ly+4:.1f}" text-anchor="middle" fill="#5b6270" font-size="12.5" font-family="Helvetica,Arial,sans-serif">{esc(e["label"])}</text>')
    return "".join(s)
BLUE="#2563EB";AMBER="#D97706";VIOLET="#7C3AED";MAROON="#9F1239"
W,H=1200,780
N("dfat",250,180,AMBER,"Dietary fat","from your meal")
N("dcarb",870,180,BLUE,"Dietary carbs","glucose")
N("dnl",1010,470,VIOLET,"DNL","carbs → fat")
N("fat",560,650,MAROON,"Body fat","the surplus lands here")
E("dcarb","dfat","spares fat (insulin blocks its burn)",0.14)
E("dfat","fat","direct & cheap (~3% lost)",0.12)
E("dcarb","dnl","only if glycogen full / fructose",0.14)
E("dnl","fat","costly (~25% lost)",0.14)
dots='<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="#e6e8ee"/></pattern>'
tip='<marker id="tip" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1.5 1.5L8 5L1.5 8.5" fill="none" stroke="context-stroke" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker>'
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}"><defs>{dots}{tip}</defs>'
     f'<rect width="{W}" height="{H}" fill="#f7f8fa"/><rect width="{W}" height="{H}" fill="url(#dots)"/>'
     +"".join(edge_svg(e) for e in EDGES)+"".join(node_svg(NODES[k]) for k in NODES)+"</svg>")
open(f"{OUT}/routes_map.svg","w").write(svg)
import cairosvg;cairosvg.svg2png(bytestring=svg.encode(),write_to=f"{OUT}/routes_map.png",output_width=W,output_height=H)
print("rendered routes",W,"x",H)
