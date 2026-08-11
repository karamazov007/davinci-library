# -*- coding: utf-8 -*-
OUT="/sessions/lucid-blissful-curie/mnt/outputs"
INK="#1c2431";MUT="#5b6572";GRID="#e6e8ee";GREEN="#16a34a";TEAL="#0d9488";BLUE="#2563eb";AMBER="#d97706";ROSE="#db2777";SL="#64748b"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def T(x,y,t,fs=12,fill=INK,anc="middle",fw=400,it=False):
    st=' font-style="italic"' if it else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anc}" fill="{fill}" font-size="{fs}" font-weight="{fw}"{st} font-family="Helvetica,Arial,sans-serif">{esc(t)}</text>'
def R(x,y,w,h,fill,rx=4,op=1.0,stroke="",sw=0):
    stk=f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" opacity="{op}"{stk}/>'

def frame():
    W,H=760,240; x0,x1=70,690; y=110; hb=40
    def X(w): return x0+(x1-x0)*((w-5.5)/2.5)
    zones=[(5.5,6.5,TEAL,"small"),(6.5,7.5,GREEN,"medium"),(7.5,8.0,BLUE,"large")]
    s=[]
    for a,b,c,lab in zones:
        s.append(R(X(a),y,X(b)-X(a),hb,c,0))
        s.append(T((X(a)+X(b))/2,y+hb+18,lab,12,MUT,"middle",700))
    for w in (5.5,6.0,6.5,7.0,7.5,8.0):
        s.append(T(X(w),y-10,f'{w:g}"',11,MUT))
    xy=X(6.5)
    s.append(f'<polygon points="{xy-8:.1f},{y-16:.1f} {xy+8:.1f},{y-16:.1f} {xy:.1f},{y-4:.1f}" fill="{INK}"/>')
    s.append(R(xy-56,y-46,112,26,INK,8)); s.append(T(xy,y-28,'YOU · 6.5″ wrist',12,"#fff","middle",700))
    s.append(T(W/2,H-14,"Wrist = your bone frame. 6.5″ at 5'9″ = slim-to-medium — a lean, proportionate build (not a mass frame).",11.5,MUT,"middle"))
    return "".join(s),H

def arm():
    W,H=760,280; x0,x1=70,690; y=140; hb=30; wr=6.5
    def X(a): return x0+(x1-x0)*((a-11.5)/(16.5-11.5))
    now=12.7; pot=16.0
    s=[R(X(11.5),y,X(pot)-X(11.5),hb,"#eef7f0",8)]          # runway track
    s.append(R(X(11.5),y,X(now)-X(11.5),hb,ROSE,8))          # achieved
    s.append(R(X(now),y,X(pot)-X(now),hb,"#bfe8cf",8))       # runway
    for a in (11.5,12.5,13.5,14.5,15.5,16.5):
        s.append(T(X(a),y+hb+18,f'{a:g}"',11,MUT))
    def mk(a,col,lab,sub,above=True):
        x=X(a)
        s.append(f'<line x1="{x:.1f}" y1="{y-6}" x2="{x:.1f}" y2="{y+hb+6}" stroke="{col}" stroke-width="2"/>')
        yy=y-44 if above else y+hb+34
        s.append(R(x-64,yy,128,32,"#fff",8,1,col,1.5))
        s.append(T(x,yy+13,lab,11.5,col,"middle",700)); s.append(T(x,yy+27,sub,10.5,MUT,"middle"))
    mk(now,ROSE,'NOW · 12.7″','1.95× wrist',above=True)
    mk(13.5,SL,'good','2.1×',above=False)
    mk(14.5,SL,'strong','2.2×',above=False)
    mk(pot,GREEN,'potential · ~16″','~2.4× wrist',above=True)
    s.append(T((X(now)+X(pot))/2,y+hb/2+4,"≈ +3″ runway",11.5,"#0f7a3c","middle",700))
    s.append(T(W/2,H-12,"Aesthetic natural arm ≈ 2.3–2.5× wrist. You're at 1.95× — years of runway from big lifts + a small surplus.",11.5,MUT,"middle"))
    return "".join(s),H

charts=[("f_frame",frame),("f_arm",arm)]
for name,fn in charts:
    body,h=fn(); open(f"{OUT}/{name}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 760 {h}">{body}</svg>')
import cairosvg
off=0;parts=[]
for name,fn in charts:
    body,h=fn();parts.append(f'<g transform="translate(0,{off})">{body}</g>');off+=h+16
comp=f'<svg xmlns="http://www.w3.org/2000/svg" width="760" viewBox="0 0 760 {off}"><rect width="760" height="{off}" fill="#fff"/>'+"".join(parts)+"</svg>"
cairosvg.svg2png(bytestring=comp.encode(),write_to=f"{OUT}/frame_verify.png",output_width=760,output_height=off)
print("frame charts rendered",off)
