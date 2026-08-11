# -*- coding: utf-8 -*-
import math
OUT="/sessions/lucid-blissful-curie/mnt/outputs"
INK="#1c2431";MUT="#5b6572";GRID="#e6e8ee";GREEN="#16a34a";TEAL="#0d9488";BLUE="#2563eb";AMBER="#d97706";ROSE="#db2777";RED="#dc2626";YEL="#ca8a04"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def T(x,y,t,fs=12,fill=INK,anc="middle",fw=400,it=False,tr=""):
    st=' font-style="italic"' if it else ''; trs=(' transform="'+tr+'"') if tr else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anc}" fill="{fill}" font-size="{fs}" font-weight="{fw}"{st} font-family="Helvetica,Arial,sans-serif"{trs}>{esc(t)}</text>'
def R(x,y,w,h,fill,rx=4,op=1.0): return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" opacity="{op}"/>'

# ---------- A: body-fat spectrum with YOU marker ----------
def y_bodyfat():
    W,H=760,250; x0,x1=70,690; y=118; hb=44
    def X(bf): return x0+(x1-x0)*((bf-8)/20.0)
    zones=[(8,10,"#0f766e","shredded"),(10,12,TEAL,"very lean"),(12,15,GREEN,"lean · defined"),
           (15,19,YEL,"athletic"),(19,24,AMBER,"soft"),(24,28,RED,"high")]
    s=[]
    for a,b,c,lab in zones:
        s.append(R(X(a),y,X(min(b,28))-X(a),hb,c,0))
        s.append(T((X(a)+X(min(b,28)))/2,y+hb+18,lab,11.5,MUT,"middle",700))
    for bf in (8,12,16,20,24,28):
        s.append(T(X(bf),y-10,f"{bf}%",11,MUT))
    # target band highlight 12-15 already green; mark target ~13
    s.append(f'<line x1="{X(13):.1f}" y1="{y}" x2="{X(13):.1f}" y2="{y+hb}" stroke="#fff" stroke-width="2" stroke-dasharray="4 3"/>')
    s.append(T(X(13),y+hb+40,"target ~13%",11,"#0f7a3c","middle",700))
    # YOU marker
    xy=X(15)
    s.append(f'<polygon points="{xy-8:.1f},{y-16:.1f} {xy+8:.1f},{y-16:.1f} {xy:.1f},{y-4:.1f}" fill="{INK}"/>')
    s.append(R(xy-40,y-46,80,26,INK,8))
    s.append(T(xy,y-28,"YOU ~15%",12.5,"#fff","middle",700))
    return "".join(s),H

# ---------- B: leaner = more defined ladder ----------
def y_reveal():
    W,H=760,324; s=[]
    rows=[(15,68,0.50,"definition when flexed","NOW",YEL),
          (13,67,0.70,"abs emerging","",GREEN),
          (12,66,0.80,"clear abs — defined ✓","TARGET",GREEN),
          (11,65,0.90,"lean / shredded-ish","",TEAL)]
    y0=54; dy=62; mx0,mx1=250,660
    for i,(bf,wt,fill,look,tag,col) in enumerate(rows):
        y=y0+i*dy
        if tag=="TARGET": s.append(R(24,y-6,712,dy-8,"#f0fdf4",10))
        s.append(f'<circle cx="80" cy="{y+16:.0f}" r="22" fill="{col}"/>')
        s.append(T(80,y+21,f"{bf}%",13,"#fff","middle",700))
        s.append(T(120,y+21,f"≈ {wt} kg",13,INK,"start",700))
        if tag: s.append(T(120,y-2,tag,10.5,("#0f7a3c" if tag=="TARGET" else MUT),"start",700))
        s.append(R(mx0,y+8,mx1-mx0,16,"#eceef2",8))
        s.append(R(mx0,y+8,(mx1-mx0)*fill,16,GREEN,8))
        s.append(T(mx0,y+42,look,11.5,MUT,"start"))
    s.append(T(760/2,H-12,"Same you — as body fat falls you get a little lighter and much more defined.",11.5,MUT,"middle",False))
    return "".join(s),H

# ---------- C: composition map YOU -> GOAL ----------
def y_map():
    W,H=680,470; s=[]; x0,x1,yb,yt=90,620,410,54
    def X(bf): return x0+(x1-x0)*((bf-8)/(26-8))
    def Y(m): return yb+(yt-yb)*m   # m 0..1 muscle
    midx=X(17); midy=(yb+yt)/2
    s.append(R(x0,yt,x1-x0,yb-yt,"#fafbfc",6))
    s.append(f'<rect x="{x0}" y="{yt}" width="{x1-x0}" height="{yb-yt}" fill="none" stroke="{GRID}" stroke-width="1"/>')
    s.append(f'<line x1="{midx:.0f}" y1="{yt}" x2="{midx:.0f}" y2="{yb}" stroke="{GRID}" stroke-width="1" stroke-dasharray="4 4"/>')
    s.append(f'<line x1="{x0}" y1="{midy:.0f}" x2="{x1}" y2="{midy:.0f}" stroke="{GRID}" stroke-width="1" stroke-dasharray="4 4"/>')
    s.append(R((x0+midx)/2-92,yt+14,184,30,"#eafaf1",8))
    s.append(T((x0+midx)/2,yt+34,"LEAN & MUSCULAR — goal",12,"#0f7a3c","middle",700))
    s.append(T((midx+x1)/2,yt+30,"big & soft",12,MUT,"middle",700))
    s.append(T((x0+midx)/2,yb-16,"lean but small",12,MUT,"middle",700))
    s.append(T((midx+x1)/2,yb-16,"skinny-fat",12,MUT,"middle",700))
    # arrow YOU -> GOAL
    ux,uy=X(15),Y(0.42); gx,gy=X(12.5),Y(0.80)
    s.append(f'<line x1="{ux:.1f}" y1="{uy:.1f}" x2="{gx:.1f}" y2="{gy:.1f}" stroke="{GREEN}" stroke-width="3" stroke-dasharray="7 5" marker-end="url(#yar)"/>')
    s.append(R((ux+gx)/2-92,(uy+gy)/2-13,150,24,"#fff",6)); s.append(f'<rect x="{(ux+gx)/2-92:.0f}" y="{(uy+gy)/2-13:.0f}" width="150" height="24" rx="6" fill="#fff" stroke="{GREEN}"/>')
    s.append(T((ux+gx)/2-17,(uy+gy)/2+4,"build muscle · stay lean",11,"#0f7a3c","middle",700))
    s.append(f'<circle cx="{ux:.1f}" cy="{uy:.1f}" r="12" fill="#fff" stroke="{BLUE}" stroke-width="3"/>'); s.append(T(ux+2,uy+30,"YOU",12.5,BLUE,"middle",800))
    s.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="12" fill="{GREEN}"/>'); s.append(T(gx,gy-20,"GOAL",12.5,"#0f7a3c","middle",800))
    s.append(T((x0+x1)/2,H-16,"← leaner        body fat        fatter →",12,INK,"middle",700))
    s.append(T(24,(yt+yb)/2,"muscle →",12,INK,"middle",700,tr=f"rotate(-90 24 {(yt+yb)/2:.0f})"))
    defs='<defs><marker id="yar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1.5 1.5L8 5L1.5 8.5" fill="none" stroke="context-stroke" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>'
    return defs+"".join(s),H

charts=[("y_bodyfat",y_bodyfat),("y_reveal",y_reveal),("y_map",y_map)]
for name,fn in charts:
    body,h=fn()
    open(f"{OUT}/{name}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {760 if name!="y_map" else 680} {h}">{body}</svg>')
import cairosvg
off=0;parts=[]
for name,fn in charts:
    body,h=fn();parts.append(f'<g transform="translate(0,{off})">{body}</g>');off+=h+16
comp=f'<svg xmlns="http://www.w3.org/2000/svg" width="760" viewBox="0 0 760 {off}"><rect width="760" height="{off}" fill="#fff"/>'+"".join(parts)+"</svg>"
cairosvg.svg2png(bytestring=comp.encode(),write_to=f"{OUT}/you_charts_verify.png",output_width=760,output_height=off)
print("you charts rendered; total",off)
