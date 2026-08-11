# -*- coding: utf-8 -*-
OUT="/sessions/lucid-blissful-curie/mnt/outputs"
INK="#1c2431";MUT="#5b6572";GREEN="#16A34A";AMBER="#D97706";BLUE="#2563EB";VIOLET="#7C3AED";ROSE="#DB2777";SLATE="#64748b"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def band(xa,yat,yab,xb,ybt,ybb,color,op=0.42):
    mx=(xa+xb)/2
    return (f'<path d="M{xa:.1f},{yat:.1f} C{mx:.1f},{yat:.1f} {mx:.1f},{ybt:.1f} {xb:.1f},{ybt:.1f} '
            f'L{xb:.1f},{ybb:.1f} C{mx:.1f},{ybb:.1f} {mx:.1f},{yab:.1f} {xa:.1f},{yab:.1f} Z" fill="{color}" opacity="{op}"/>')
def rectn(x,y,w,h,color):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h:.1f}" rx="3" fill="{color}"/>'
def T(x,y,t,fs=12,fill=INK,anc="start",fw=400,it=False):
    st=' font-style="italic"' if it else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anc}" fill="{fill}" font-size="{fs}" font-weight="{fw}"{st} font-family="Helvetica,Arial,sans-serif">{esc(t)}</text>'

W,H=900,540
s=2.55; y0=70
sx0,sx1=64,90; c1x0,c1x1=330,356; c2x0,c2x1=560,586; gap=12
FP=34; BODY=102; TOT=FP+BODY
OX=60; UP=28; OTH=11; MUS=3
el=[]
# source bar
src_h=TOT*s
el.append(rectn(sx0,y0,sx1-sx0,src_h,SLATE))
el.append(T((sx0+sx1)/2,y0-26,"136 g",13,INK,"middle",700))
el.append(T((sx0+sx1)/2,y0-11,"eaten / day",11,MUT,"middle"))
# source segments
fp_t=y0; fp_b=y0+FP*s
body_t=y0+FP*s; body_b=y0+TOT*s
# col1 nodes
g_t=y0; g_b=y0+FP*s
b_t=y0+FP*s+gap; b_b=b_t+BODY*s
el.append(rectn(c1x0,g_t,c1x1-c1x0,g_b-g_t,GREEN))
el.append(rectn(c1x0,b_t,c1x1-c1x0,b_b-b_t,BLUE))
# bands source->col1
el.append(band(sx1,fp_t,fp_b,c1x0,g_t,g_b,GREEN))
el.append(band(sx1,body_t,body_b,c1x0,b_t,b_b,BLUE))
# col1 labels
el.append(T(c1x1+8,g_t+ (g_b-g_t)/2 -2,"Gut + liver",12,INK,"start",700))
el.append(T(c1x1+8,g_t+ (g_b-g_t)/2 +14,"first-pass · 34 g",11,MUT,"start"))
el.append(T(c1x1+8,b_t+18,"Into the body · 102 g",12,INK,"start",700))
# col2 fate nodes (gutfate, ox, upkeep, other, muscle)
fates=[("Gut/liver use → urea",FP,GREEN,"g"),
       ("Oxidised for energy → urea",OX,AMBER,"b"),
       ("Renew body proteins (upkeep)",UP,BLUE,"b"),
       ("Other molecules (creatine…)",OTH,VIOLET,"b"),
       ("NET new muscle",MUS,ROSE,"b")]
cur=y0; nodes=[]
for i,(lab,val,col,src) in enumerate(fates):
    ht=val*s; nodes.append((lab,val,col,src,cur,cur+ht)); cur+=ht+gap
for lab,val,col,src,t,b in nodes:
    el.append(rectn(c2x0,t,c2x1-c2x0,b-t,col))
# bands into col2
# gut -> gutfate
gf=nodes[0]; el.append(band(c1x1,g_t,g_b,c2x0,gf[4],gf[5],GREEN))
# body right edge sub-segments for ox,up,other,muscle
cb=b_t
for lab,val,col,src,t,b in nodes[1:]:
    seg_t=cb; seg_b=cb+val*s; cb=seg_b
    el.append(band(c1x1,seg_t,seg_b,c2x0,t,b,col))
# col2 labels
for lab,val,col,src,t,b in nodes:
    mid=(t+b)/2
    el.append(T(c2x1+10,mid-1,lab,12,INK,"start",700))
    el.append(T(c2x1+10,mid+15,f"{val} g",11.5,col,"start",700))
# footnote
el.append(T(W/2,H-16,"Grams are illustrative for a weight-stable 68 kg trainee. Only ~3 g becomes NEW muscle; the rest renews proteins or is burned (N → urea).",11,MUT,"middle",False,True))
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}">{"".join(el)}</svg>'
open(f"{OUT}/pc_sankey.svg","w").write(svg)
import cairosvg;cairosvg.svg2png(bytestring=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#fff"/>'+"".join(el)+"</svg>").encode(),write_to=f"{OUT}/pc_sankey.png",output_width=W,output_height=H)
print("sankey rendered; check sums:",FP+OX+UP+OTH+MUS,"=136?")
