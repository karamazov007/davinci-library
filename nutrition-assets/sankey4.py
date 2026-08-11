# -*- coding: utf-8 -*-
OUT="/sessions/lucid-blissful-curie/mnt/outputs"
INK="#1c2431";MUT="#5b6572";GREEN="#16A34A";AMBER="#D97706";BLUE="#2563EB";VIOLET="#7C3AED";ROSE="#DB2777";SLATE="#64748b"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def band(xa,yat,yab,xb,ybt,ybb,color,op=0.42):
    mx=(xa+xb)/2
    return (f'<path d="M{xa:.1f},{yat:.1f} C{mx:.1f},{yat:.1f} {mx:.1f},{ybt:.1f} {xb:.1f},{ybt:.1f} '
            f'L{xb:.1f},{ybb:.1f} C{mx:.1f},{ybb:.1f} {mx:.1f},{yab:.1f} {xa:.1f},{yab:.1f} Z" fill="{color}" opacity="{op}"/>')
def rectn(x,y,w,h,color): return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h:.1f}" rx="3" fill="{color}"/>'
def T(x,y,t,fs=12,fill=INK,anc="start",fw=400,it=False):
    st=' font-style="italic"' if it else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anc}" fill="{fill}" font-size="{fs}" font-weight="{fw}"{st} font-family="Helvetica,Arial,sans-serif">{esc(t)}</text>'

W,H=920,560; s=2.4; y0=110
sx0,sx1=64,90; c1x0,c1x1=340,366; c2x0,c2x1=584,610; gap=12
def build(cfg):
    intake=cfg["intake"];fp=cfg["fp"];body=intake-fp
    el=[]
    el.append(T(64,44,cfg["title"],17,INK,"start",700))
    el.append(T(64,66,cfg["sub"]+"  ·  68 kg",13,MUT,"start"))
    # source
    el.append(rectn(sx0,y0,sx1-sx0,intake*s,SLATE))
    el.append(T((sx0+sx1)/2,y0-10,f"{intake} g",12.5,INK,"middle",700))
    fp_t=y0;fp_b=y0+fp*s; body_t=fp_b; body_b=y0+intake*s
    g_t=y0;g_b=y0+fp*s; b_t=g_b+gap; b_b=b_t+body*s
    el.append(rectn(c1x0,g_t,c1x1-c1x0,g_b-g_t,GREEN))
    el.append(rectn(c1x0,b_t,c1x1-c1x0,b_b-b_t,BLUE))
    el.append(band(sx1,fp_t,fp_b,c1x0,g_t,g_b,GREEN))
    el.append(band(sx1,body_t,body_b,c1x0,b_t,b_b,BLUE))
    el.append(T(c1x1+8,(g_t+g_b)/2+4,f"Gut + liver first-pass · {fp} g",11.5,INK,"start",700))
    el.append(T(c1x1+8,b_t+18,f"Into the body · {body} g",11.5,INK,"start",700))
    # col2 fates
    fates=[("Gut/liver use → urea",fp,GREEN,"g")]
    for lab,val,col in [("Oxidised for energy → urea",cfg["ox"],AMBER),
                        ("Renew body proteins (upkeep)",cfg["up"],BLUE),
                        ("Other molecules (creatine…)",cfg["oth"],VIOLET),
                        ("NET new muscle",cfg["mus"],ROSE)]:
        if val>0: fates.append((lab,val,col,"b"))
    cur=y0;nodes=[]
    for lab,val,col,srcn in fates:
        ht=val*s;nodes.append((lab,val,col,srcn,cur,cur+ht));cur+=ht+gap
    for lab,val,col,srcn,t,b in nodes: el.append(rectn(c2x0,t,c2x1-c2x0,b-t,col))
    gf=nodes[0]; el.append(band(c1x1,g_t,g_b,c2x0,gf[4],gf[5],GREEN))
    cb=b_t
    for lab,val,col,srcn,t,b in nodes[1:]:
        st_=cb;sb_=cb+val*s;cb=sb_
        el.append(band(c1x1,st_,sb_,c2x0,t,b,col))
    for lab,val,col,srcn,t,b in nodes:
        mid=(t+b)/2
        el.append(T(c2x1+10,mid-1,lab,12,INK,"start",700))
        el.append(T(c2x1+10,mid+15,f"{val} g",11.5,col,"start",700))
    el.append(T(W/2,H-20,cfg["note"],11.5,MUT,"middle",False,True))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}">{"".join(el)}</svg>'

CFG={
 "minimum":dict(intake=54,fp=13,ox=2,up=28,oth=11,mus=0,title="Minimum · RDA 0.8 g/kg",sub="54 g/day",
    note="Barely covers obligatory upkeep — almost no spare, no growth. For a trainee this risks losing muscle."),
 "build":dict(intake=109,fp=27,ox=40,up=28,oth=11,mus=3,title="Build / keep · 1.6 g/kg",sub="109 g/day",
    note="Enough to max MPS and build ~3 g/day of new muscle; the modest surplus is oxidised."),
 "solid":dict(intake=136,fp=34,ox=60,up=28,oth=11,mus=3,title="Solid · 2.0 g/kg",sub="136 g/day",
    note="Comfortable headroom; still ~3 g net muscle. Protein above ~1.6 g/kg mostly gets oxidised."),
 "cutting":dict(intake=150,fp=38,ox=72,up=28,oth=11,mus=1,title="Cutting · 2.2 g/kg",sub="150 g/day",
    note="In a deficit more protein is burned for fuel (high oxidation) but muscle is protected (net ≈ maintained)."),
}
import json,cairosvg
svgs={k:build(v) for k,v in CFG.items()}
json.dump(svgs,open(f"{OUT}/pc_sk4.json","w"),ensure_ascii=False)
# verify composite (stack 4)
order=["minimum","build","solid","cutting"];parts=[]
for i,k in enumerate(order):
    inner=svgs[k].split(">",1)[1].rsplit("</svg>",1)[0]
    parts.append(f'<g transform="translate(0,{i*H})">{inner}</g>')
comp=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" viewBox="0 0 {W} {H*4}"><rect width="{W}" height="{H*4}" fill="#fff"/>'+"".join(parts)+"</svg>"
cairosvg.svg2png(bytestring=comp.encode(),write_to=f"{OUT}/pc_sk4_verify.png",output_width=W,output_height=H*4)
print("built 4 sankeys; sums:",{k:CFG[k]["fp"]+CFG[k]["ox"]+CFG[k]["up"]+CFG[k]["oth"]+CFG[k]["mus"] for k in order})
