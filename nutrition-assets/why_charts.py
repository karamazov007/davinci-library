# -*- coding: utf-8 -*-
OUT="/sessions/lucid-blissful-curie/mnt/outputs"
INK="#1c2431";MUT="#5b6572";GRID="#e6e8ee";GREEN="#16a34a";TEAL="#0d9488";BLUE="#2563eb";AMBER="#d97706";ROSE="#db2777";RED="#dc2626";SL="#64748b"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def T(x,y,t,fs=12,fill=INK,anc="middle",fw=400,it=False):
    st=' font-style="italic"' if it else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anc}" fill="{fill}" font-size="{fs}" font-weight="{fw}"{st} font-family="Helvetica,Arial,sans-serif">{esc(t)}</text>'
def R(x,y,w,h,fill,rx=4,op=1.0,stroke="",sw=0):
    stk=f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" opacity="{op}"{stk}/>'

def net_by_energy():
    W,H=760,360; x0,x1=100,690; top=70; bot=300
    def Y(v): return bot-(v-(-2))/6.0*(bot-top)
    s=[]
    for v in (-2,-1,0,1,2,3,4):
        yy=Y(v); s.append(f'<line x1="{x0}" y1="{yy:.1f}" x2="{x1}" y2="{yy:.1f}" stroke="{GRID}" stroke-width="1"/>')
        s.append(T(x0-10,yy+4,f"{v:+d}".replace("+0","0"),11,MUT,"end"))
    s.append(f'<line x1="{x0}" y1="{Y(0):.1f}" x2="{x1}" y2="{Y(0):.1f}" stroke="{INK}" stroke-width="1.6"/>')
    bars=[("Deficit (cut)",-1,RED),("Maintenance",1,AMBER),("Surplus (bulk)",3,GREEN)]
    cx=[220,395,570]; bw=110
    for i,(lab,v,col) in enumerate(bars):
        x=cx[i]-bw/2
        if v>=0: s.append(R(x,Y(v),bw,Y(0)-Y(v),col,5))
        else: s.append(R(x,Y(0),bw,Y(v)-Y(0),col,5))
        vy=Y(v)-8 if v>=0 else Y(v)+20
        s.append(T(cx[i],vy,f"{v:+d} g",12.5,col,"middle",700))
        s.append(T(cx[i],bot+22,lab,12,INK,"middle",700))
    s.append(T((x0+x1)/2,44,"Same 130 g protein — net muscle depends on ENERGY STATE",13,INK,"middle",700))
    my=(top+bot)/2
    s.append(f'<text x="34" y="{my:.0f}" text-anchor="middle" fill="{INK}" font-size="12" font-weight="700" font-family="Helvetica,Arial,sans-serif" transform="rotate(-90 34 {my:.0f})">net muscle (g/day)</text>')
    return "".join(s),H

def why_surplus():
    W,H=760,430; s=[]
    # top protein box
    s.append(R(300,20,160,44,ROSE,10)); s.append(T(380,40,"130 g protein",12.5,"#fff","middle",700)); s.append(T(380,57,"(the bricks) — constant",10.5,"#ffd9e8","middle"))
    panels=[("DEFICIT",70,RED,0.40,0.72,"NET: muscle ↓","#fdeaea"),("SURPLUS",410,GREEN,0.82,0.42,"NET: muscle ↑","#eafaf1")]
    for name,px,col,mps,mpb,net,bg in panels:
        s.append(R(px,90,280,300,bg,14,1,col,1.5))
        s.append(T(px+140,120,name,14,col,"middle",800))
        s.append(f'<line x1="{380 if px<300 else 380}" y1="64" x2="{px+140}" y2="88" stroke="{ROSE}" stroke-width="1.6" stroke-dasharray="5 4"/>')
        base=330; bh=180
        for j,(blab,val,bc) in enumerate([("MPS",mps,GREEN),("MPB",mpb,"#e0793a")]):
            bx=px+70+j*90
            s.append(R(bx,base-bh*val,54,bh*val,bc,5))
            s.append(T(bx+27,base+18,blab,11.5,INK,"middle",700))
            s.append(T(bx+27,base-bh*val-8,("build" if blab=="MPS" else "break"),10,MUT,"middle"))
        s.append(R(px+60,base+30,160,26,"#fff",8,1,col,1.2)); s.append(T(px+140,base+47,net,12,col,"middle",700))
    s.append(T(W/2,H-12,"Same bricks, opposite result — the surplus pays the build & spares the protein.",11.5,MUT,"middle"))
    return "".join(s),H

charts=[("w_net",net_by_energy),("w_why",why_surplus)]
for name,fn in charts:
    body,h=fn(); open(f"{OUT}/{name}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 760 {h}">{body}</svg>')
import cairosvg
off=0;parts=[]
for name,fn in charts:
    body,h=fn();parts.append(f'<g transform="translate(0,{off})">{body}</g>');off+=h+16
comp=f'<svg xmlns="http://www.w3.org/2000/svg" width="760" viewBox="0 0 760 {off}"><rect width="760" height="{off}" fill="#fff"/>'+"".join(parts)+"</svg>"
cairosvg.svg2png(bytestring=comp.encode(),write_to=f"{OUT}/why_verify.png",output_width=760,output_height=off)
print("why charts rendered",off)
