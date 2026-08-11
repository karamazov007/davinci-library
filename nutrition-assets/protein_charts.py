# -*- coding: utf-8 -*-
import math
OUT="/sessions/lucid-blissful-curie/mnt/outputs"
INK="#1c2431";MUT="#5b6572";GRID="#e6e8ee";ROSE="#DB2777";TEAL="#0D9488";AMBER="#D97706";GREEN="#16A34A";VIOLET="#7C3AED"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def T(x,y,t,fs=12,fill=MUT,anc="middle",fw=400,it=False,tr=""):
    style=' font-style="italic"' if it else ''
    trs=(' transform="'+tr+'"') if tr else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anc}" fill="{fill}" font-size="{fs}" font-weight="{fw}"{style} font-family="Helvetica,Arial,sans-serif"{trs}>{esc(t)}</text>'

# ---------- Chart 1: MPS vs single-meal dose ----------
def chart_dose():
    W,H=680,360; x0,x1,yb,yt=90,620,300,54; s=[]
    def X(g): return x0+(x1-x0)*(g/60)
    def Y(v): return yb+(yt-yb)*(v/100)
    # axes + grid
    for v in (0,25,50,75,100):
        s.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="{GRID}" stroke-width="1"/>')
        s.append(T(x0-10,Y(v)+4,str(v)+"%",11,MUT,"end"))
    for g in (0,10,20,30,40,50,60):
        s.append(T(X(g),yb+20,str(g),11,MUT))
    s.append(f'<line x1="{x0}" y1="{yt}" x2="{x0}" y2="{yb}" stroke="{INK}" stroke-width="1.5"/>')
    s.append(f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{INK}" stroke-width="1.5"/>')
    # ceiling band (extra oxidised) beyond 27g
    s.append(f'<rect x="{X(27):.1f}" y="{yt}" width="{x1-X(27):.1f}" height="{yb-yt}" fill="{AMBER}" opacity="0.07"/>')
    # curve
    pts=[]
    for gi in range(0,61):
        v=100*(1-math.exp(-gi/7.0))
        pts.append(f"{X(gi):.1f},{Y(v):.1f}")
    s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{ROSE}" stroke-width="3"/>')
    # ceiling marker at 27g
    s.append(f'<line x1="{X(27):.1f}" y1="{yt}" x2="{X(27):.1f}" y2="{yb}" stroke="{ROSE}" stroke-width="1.4" stroke-dasharray="5 4"/>')
    s.append(T(X(27),yt-8,"ceiling ≈ 0.4 g/kg (68 kg → 27 g)",11.5,ROSE,"middle",700))
    s.append(T(X(46),Y(88),"extra → oxidised",12,"#a15a12","middle",700))
    s.append(T((x0+x1)/2,H-14,"protein in ONE meal (g)",12.5,INK,"middle",700))
    s.append(T(26,(yt+yb)/2,"MPS rate",12.5,INK,"middle",700,tr=f"rotate(-90 26 {(yt+yb)/2:.0f})"))
    return "".join(s),H

# ---------- Chart 2: daily muscle-building vs total intake (plateau) ----------
def chart_daily():
    W,H=680,360; x0,x1,yb,yt=90,620,300,54; s=[]
    def X(g): return x0+(x1-x0)*(g/2.6)
    def Y(v): return yb+(yt-yb)*(v/100)
    for v in (0,25,50,75,100):
        s.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="{GRID}" stroke-width="1"/>')
        s.append(T(x0-10,Y(v)+4,str(v)+"%",11,MUT,"end"))
    for g in (0,0.4,0.8,1.2,1.6,2.0,2.4):
        s.append(T(X(g),yb+20,f"{g:g}",11,MUT))
    s.append(f'<line x1="{x0}" y1="{yt}" x2="{x0}" y2="{yb}" stroke="{INK}" stroke-width="1.5"/>')
    s.append(f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{INK}" stroke-width="1.5"/>')
    # optimal band 1.6-2.2
    s.append(f'<rect x="{X(1.6):.1f}" y="{yt}" width="{X(2.2)-X(1.6):.1f}" height="{yb-yt}" fill="{GREEN}" opacity="0.10"/>')
    s.append(T((X(1.6)+X(2.2))/2,yt+16,"optimal",11.5,"#0f7a3c","middle",700))
    # curve: rises, plateaus ~1.6
    pts=[]
    for i in range(0,131):
        g=i*2.6/130; v=100*(1-math.exp(-g/0.55)); v=min(v,100)
        pts.append(f"{X(g):.1f},{Y(v):.1f}")
    s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{TEAL}" stroke-width="3"/>')
    # RDA marker 0.8
    s.append(f'<line x1="{X(0.8):.1f}" y1="{Y(100*(1-math.exp(-0.8/0.55))):.1f}" x2="{X(0.8):.1f}" y2="{yb}" stroke="{MUT}" stroke-width="1.2" stroke-dasharray="4 4"/>')
    s.append(T(X(0.8),Y(100*(1-math.exp(-0.8/0.55)))-8,"RDA 0.8 = minimum",11,MUT,"middle",700))
    s.append(T(X(2.35),Y(97),"more ≠ more muscle",11.5,"#0f7a3c","middle",700))
    s.append(T((x0+x1)/2,H-14,"TOTAL daily protein (g per kg bodyweight)",12.5,INK,"middle",700))
    s.append(T(26,(yt+yb)/2,"muscle-building drive",12.5,INK,"middle",700,tr=f"rotate(-90 26 {(yt+yb)/2:.0f})"))
    return "".join(s),H

# ---------- Chart 3: MPS timeline over 48 h (training envelope + feeding spikes) ----------
def chart_timeline():
    W,H=680,380; x0,x1,yb,yt=70,650,300,60; s=[]
    def X(t): return x0+(x1-x0)*(t/48)
    def Y(v): return yb+(yt-yb)*(v/100)
    workouts=[0,24]; feeds=[1.5,5.5,9.5,13.5,25.5,29.5,33.5,37.5]
    def env(t):
        e=15
        for w in workouts:
            if t>=w: e+=42*math.exp(-(t-w)/26.0)
        return e
    def mps(t):
        v=env(t)
        for f in feeds:
            v+=34*math.exp(-((t-f)/1.15)**2)
        return min(v,100)
    # grid
    for v in (0,25,50,75,100):
        s.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="{GRID}" stroke-width="1"/>')
    for t in range(0,49,6):
        s.append(T(X(t),yb+20,str(t)+"h",10.5,MUT))
    s.append(f'<line x1="{X(24):.1f}" y1="{yt}" x2="{X(24):.1f}" y2="{yb}" stroke="{GRID}" stroke-width="1.5" stroke-dasharray="3 4"/>')
    s.append(T(X(12),yt-24,"DAY 1",11,MUT,"middle",700));s.append(T(X(36),yt-24,"DAY 2",11,MUT,"middle",700))
    s.append(f'<line x1="{x0}" y1="{yt}" x2="{x0}" y2="{yb}" stroke="{INK}" stroke-width="1.5"/>')
    s.append(f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{INK}" stroke-width="1.5"/>')
    # training envelope (area)
    epts=[f"{X(0):.1f},{Y(0):.1f}"]+[f"{X(t*0.5):.1f},{Y(env(t*0.5)):.1f}" for t in range(0,97)]+[f"{X(48):.1f},{Y(0):.1f}"]
    s.append(f'<polygon points="{" ".join(epts)}" fill="{VIOLET}" opacity="0.10"/>')
    epts2=[f"{X(t*0.5):.1f},{Y(env(t*0.5)):.1f}" for t in range(0,97)]
    s.append(f'<polyline points="{" ".join(epts2)}" fill="none" stroke="{VIOLET}" stroke-width="1.6" stroke-dasharray="6 4" opacity="0.7"/>')
    # composite MPS line
    mpts=[f"{X(t*0.25):.1f},{Y(mps(t*0.25)):.1f}" for t in range(0,193)]
    s.append(f'<polyline points="{" ".join(mpts)}" fill="none" stroke="{ROSE}" stroke-width="2.6"/>')
    # workout arrows
    for w in workouts:
        s.append(f'<line x1="{X(w):.1f}" y1="{yb}" x2="{X(w):.1f}" y2="{yb-26}" stroke="{VIOLET}" stroke-width="2.4"/>')
        s.append(f'<polygon points="{X(w)-5:.1f},{yb-22:.1f} {X(w)+5:.1f},{yb-22:.1f} {X(w):.1f},{yb-32:.1f}" fill="{VIOLET}"/>')
        s.append(T(X(w)+2,yb-38,"train",10.5,VIOLET,"middle",700))
    # feed ticks
    for f in feeds:
        s.append(f'<circle cx="{X(f):.1f}" cy="{Y(mps(f)):.1f}" r="3.4" fill="{ROSE}"/>')
    s.append(T(X(f),Y(mps(f))-12,"protein feed",10.5,ROSE,"middle",700))
    s.append(T(X(3),yt+2,"envelope: training raises MPS ~24–48 h",11,"#5b45b0","start",700))
    s.append(T((x0+x1)/2,H-14,"time (hours over two days)",12.5,INK,"middle",700))
    s.append(T(24,(yt+yb)/2,"MPS rate",12.5,INK,"middle",700,tr=f"rotate(-90 24 {(yt+yb)/2:.0f})"))
    return "".join(s),H

charts=[("pc_dose",chart_dose),("pc_daily",chart_daily),("pc_timeline",chart_timeline)]
# save individual full svgs (responsive)
for name,fn in charts:
    body,h=fn()
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 680 {h}">{body}</svg>'
    open(f"{OUT}/{name}.svg","w").write(svg)
# stacked verify png
import cairosvg
off=0;parts=[];total=0
for name,fn in charts:
    body,h=fn();parts.append(f'<g transform="translate(0,{off})">{body}</g>');off+=h+16;total=off
verify=f'<svg xmlns="http://www.w3.org/2000/svg" width="680" viewBox="0 0 680 {total}"><rect width="680" height="{total}" fill="#ffffff"/>'+"".join(parts)+"</svg>"
cairosvg.svg2png(bytestring=verify.encode(),write_to=f"{OUT}/protein_charts_verify.png",output_width=680,output_height=total)
print("charts rendered; total height",total)
