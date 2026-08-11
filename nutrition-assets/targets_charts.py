# -*- coding: utf-8 -*-
import math
OUT="/sessions/lucid-blissful-curie/mnt/outputs"; BASE=2100
INK="#1c2431";MUT="#5b6572";GRID="#e6e8ee";GREEN="#16a34a";TEAL="#0d9488";BLUE="#2563eb";AMBER="#d97706";ROSE="#db2777";CYAN="#0891b2";RED="#dc2626";SLATE="#64748b"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def T(x,y,t,fs=12,fill=INK,anc="middle",fw=400,it=False,tr=""):
    st=' font-style="italic"' if it else ''; trs=(' transform="'+tr+'"') if tr else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anc}" fill="{fill}" font-size="{fs}" font-weight="{fw}"{st} font-family="Helvetica,Arial,sans-serif"{trs}>{esc(t)}</text>'
def R(x,y,w,h,fill,rx=4,op=1.0,stroke="",sw=0):
    st=f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" opacity="{op}"{st}/>'

def dial():
    W,H=760,280; x0,x1=70,690; y=120; hb=40
    def X(m): return x0+(x1-x0)*((m-0.75)/0.45)
    s=[R(X(0.75),y,X(1.0)-X(0.75),hb,"#f6d3ad",0), R(X(1.0),y,X(1.20)-X(1.0),hb,"#bfe8cf",0)]
    s.append(f'<line x1="{X(1.0):.1f}" y1="{y-6}" x2="{X(1.0):.1f}" y2="{y+hb+6}" stroke="{INK}" stroke-width="1.5"/>')
    for m in (0.8,0.9,1.0,1.1,1.2):
        s.append(T(X(m),y+hb+16,f"×{m:.2f}",11,MUT))
    s.append(T((X(0.75)+X(1.0))/2,y-14,"DEFICIT (cut)",11.5,"#a15a12","middle",700))
    s.append(T((X(1.0)+X(1.20))/2,y-14,"SURPLUS (bulk)",11.5,"#0f7a3c","middle",700))
    def mark(m,col,lab,above=True,big=False):
        x=X(m); k=round(BASE*m/5)*5
        dash='' if big else ' stroke-dasharray="4 3"'
        s.append(f'<line x1="{x:.1f}" y1="{y}" x2="{x:.1f}" y2="{y+hb}" stroke="{col}" stroke-width="{3 if big else 1.6}"{dash}/>')
        yy=y-30 if above else y+hb+34
        w=124 if big else 104
        s.append(R(x-w/2,yy-18,w,34,"#fff",8,1,col,2 if big else 1))
        s.append(T(x,yy-2,lab,11.5,col,"middle",700)); s.append(T(x,yy+13,f"{k:,} kcal",11,INK,"middle",700))
    mark(0.80,AMBER,"Standard cut",above=False)
    mark(1.00,SLATE,"Maintenance",above=False)
    mark(1.10,GREEN,"LEAN BULK ← you",above=True,big=True)
    return "".join(s),H

def macros():
    W,H=760,440; s=[]; base=380; top=64;
    def h(k): return k*(base-top)/2310.0
    cols=[("Cut",1680,166,55),("Maintenance",2100,260,60),("Lean bulk",2310,301,65)]
    xs=[180,380,580]; bw=120
    P=520
    for i,(name,kcal,cg,fg) in enumerate(cols):
        x=xs[i]-bw/2; fk=fg*9; ck=cg*4
        yp=base-h(P); s.append(R(x,yp,bw,h(P),ROSE,4)); s.append(T(xs[i],yp+h(P)/2+4,"130 g",11,"#fff",fw=700))
        yf=yp-h(fk); s.append(R(x,yf,bw,h(fk),AMBER,4)); s.append(T(xs[i],yf+h(fk)/2+4,f"{fg} g",10.5,"#fff",fw=700))
        yc=yf-h(ck); s.append(R(x,yc,bw,h(ck),CYAN,4)); s.append(T(xs[i],yc+h(ck)/2+4,f"{cg} g",11,"#fff",fw=700))
        s.append(T(xs[i],base+18,name,12.5,INK,fw=700)); s.append(T(xs[i],base+34,f"{kcal:,} kcal",11,MUT))
    yr=base-h(P)
    s.append(f'<line x1="{110}" y1="{yr:.1f}" x2="{650}" y2="{yr:.1f}" stroke="{ROSE}" stroke-width="1.6" stroke-dasharray="6 4"/>')
    s.append(T(660,yr+4,"protein rail",11,ROSE,"start",700))
    for i,(lab,c) in enumerate([("Protein",ROSE),("Fat",AMBER),("Carbs",CYAN)]):
        s.append(R(120+i*120,30,13,13,c,3)); s.append(T(140+i*120,41,lab,11.5,MUT,"start"))
    s.append(T(W/2,H-12,"Protein stays fixed (the rail); carbs & fat flex down to cut, up to bulk.",11.5,MUT))
    return "".join(s),H

def rate():
    W,H=760,230; x0,x1=70,690; y=118
    def X(v): return x0+(x1-x0)*((v+0.9)/1.5)
    s=[R(X(-0.9),y,X(-0.7)-X(-0.9),34,"#f6b8b8",0), R(X(-0.7),y,X(-0.35)-X(-0.7),34,"#bfe8cf",0),
       R(X(-0.35),y,X(0.2)-X(-0.35),34,"#e7e9ee",0), R(X(0.2),y,X(0.35)-X(0.2),34,"#bfe8cf",0),
       R(X(0.35),y,X(0.6)-X(0.35),34,"#f7d9ad",0)]
    for v in (-0.7,-0.35,0,0.2,0.35):
        s.append(T(X(v),y+52,f"{v:+.2f}".rstrip('0').rstrip('.') if v!=0 else "0",11,MUT))
    s.append(T((X(-0.7)+X(-0.35))/2,y+22,"CUT",11.5,"#0f7a3c","middle",800))
    s.append(T((X(0.2)+X(0.35))/2,y+22,"BULK",11.5,"#0f7a3c","middle",800))
    s.append(T((X(-0.9)+X(-0.7))/2,y-10,"too fast",10.5,"#a12626","middle",700))
    s.append(T((X(0.35)+X(0.6))/2,y-10,"fat creeping",10.5,"#a15a12","middle",700))
    s.append(T((X(-0.35)+X(0.2))/2,y-10,"stall / maintenance",10.5,MUT,"middle",700))
    s.append(T(W/2,44,"Weekly weight change (kg) — you at 68 kg. Adjust ±150 kcal to stay in the green.",12,INK,"middle",700))
    return "".join(s),H

charts=[("t_dial",dial),("t_macros",macros),("t_rate",rate)]
for name,fn in charts:
    body,h=fn(); open(f"{OUT}/{name}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 760 {h}">{body}</svg>')
import cairosvg
off=0;parts=[]
for name,fn in charts:
    body,h=fn();parts.append(f'<g transform="translate(0,{off})">{body}</g>');off+=h+16
comp=f'<svg xmlns="http://www.w3.org/2000/svg" width="760" viewBox="0 0 760 {off}"><rect width="760" height="{off}" fill="#fff"/>'+"".join(parts)+"</svg>"
cairosvg.svg2png(bytestring=comp.encode(),write_to=f"{OUT}/targets_verify.png",output_width=760,output_height=off)
print("targets rendered", off)
