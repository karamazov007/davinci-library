# -*- coding: utf-8 -*-
import os
OUT="/sessions/lucid-blissful-curie/mnt/outputs"

# palette: (fill, stroke, text)
PAL={
 "carb":("#E6F1FB","#185FA5","#0C447C"),
 "prot":("#FBEAF0","#993556","#72243E"),
 "fat": ("#FAEEDA","#854F0B","#633806"),
 "fuel":("#EEEDFE","#534AB7","#3C3489"),
 "ins": ("#EAF3DE","#3B6D11","#27500A"),
 "store":("#E1F5EE","#0F6E56","#085041"),
 "def":("#FAECE7","#993C1D","#712B13"),
 "gate":("#F1EFE8","#5F5E5A","#2C2C2A"),
}
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def box(cx,cy,w,h,ramp,title,sub=None,rx=8):
    f,s,t=PAL[ramp]; x=cx-w/2; y=cy-h/2
    o=f'<rect x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" rx="{rx}" fill="{f}" stroke="{s}" stroke-width="1.2"/>'
    if sub:
        o+=f'<text x="{cx:.0f}" y="{cy-6:.0f}" text-anchor="middle" fill="{t}" font-size="14" font-weight="500" font-family="sans-serif">{esc(title)}</text>'
        o+=f'<text x="{cx:.0f}" y="{cy+12:.0f}" text-anchor="middle" fill="{t}" font-size="12" font-family="sans-serif">{esc(sub)}</text>'
    else:
        o+=f'<text x="{cx:.0f}" y="{cy+1:.0f}" text-anchor="middle" dominant-baseline="middle" fill="{t}" font-size="14" font-weight="500" font-family="sans-serif">{esc(title)}</text>'
    return o

def arr(x1,y1,x2,y2,color="#5F5E5A",dash=None,w=1.6):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{color}" stroke-width="{w}"{d} marker-end="url(#ar)"/>'
def path(dd,color="#5F5E5A",dash=None,w=1.6):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{dd}" fill="none" stroke="{color}" stroke-width="{w}"{d} marker-end="url(#ar)"/>'
def lbl(x,y,txt,color="#5F5E5A"):
    return f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" fill="{color}" font-size="12" font-family="sans-serif">{esc(txt)}</text>'

W=680; H=712
C,Px,Fx=100,285,470   # lane centers
BW=132
s=[]
# --- nodes ---
# row0 food
s+=[box(C,54,BW,48,"carb","Carbohydrates"),box(Px,54,BW,48,"prot","Protein"),box(Fx,54,BW,48,"fat","Fat")]
# row1 molecules + insulin
s+=[box(C,142,BW,46,"carb","Glucose"),box(Px,142,BW,46,"prot","Amino acids"),box(Fx,142,BW,46,"fat","Fatty acids")]
s+=[box(598,142,92,56,"ins","Insulin ↑","(fed state)")]
# row2 fate1
s+=[box(C,246,BW,54,"carb","Burn for ATP","immediate need"),
    box(Px,246,150,54,"gate","Training signal?","the gate"),
    box(Fx,246,BW,54,"fat","Fat-burn blocked","✕ by insulin")]
s+=[box(598,246,92,50,"fat","Structural","small")]
# row3 fate2
s+=[box(C,356,BW,54,"carb","Glycogen","limited tank"),
    box(228,356,116,50,"prot","MPS ↑","build (YES)"),
    box(Fx,356,BW,54,"fat","Store as body fat","(rerouted)")]
s+=[box(598,356,92,50,"gate","N → urea","excreted")]
# fuel pool (central wide)
s+=[box(288,464,344,56,"fuel","FUEL POOL → ATP","BMR · NEAT · training")]
# row5 stores
s+=[box(C,576,BW,52,"store","Glycogen store"),box(Px,576,BW,52,"store","Muscle"),box(Fx,576,BW,52,"store","Body-fat store")]
# deficit band
s+=[box(340,668,560,46,"def","Fasted / deficit: insulin ↓, glucagon & adrenaline ↑ → mobilise & burn")]

# --- arrows ---
G="#5F5E5A"; RED="#993C1D"; GRN="#3B6D11"
# food -> molecule
for cx in (C,Px,Fx): s.append(arr(cx,78,cx,119))
# molecule -> fate1
s.append(arr(C,165,C,219)); s.append(arr(Px,165,Px,219)); s.append(arr(Fx,165,Fx,219))
# CARB: glucose -> burn (row2) ; glucose -> glycogen (curve left) ; burn -> fuel ; glycogen -> store ; glycogen -> body fat (surplus)
s.append(path(f"M78,165 C24,235 24,300 70,331"))          # glucose -> glycogen (left curve)
s.append(path(f"M{C+66},250 L{C+66},300 L196,438"))       # burn for ATP -> fuel pool
s.append(arr(C,383,C,550))                                # glycogen -> glycogen store
# FAT: fatty acids -> blocked -> body fat -> store ; structural side
s.append(arr(Fx,273,Fx,329))                              # F2 -> F3
s.append(arr(Fx,383,Fx,550))                              # body fat -> store
s.append(path(f"M{Fx+40},165 L598,165 L598,221"))         # fatty acids -> structural
# PROTEIN gate: YES -> MPS -> muscle ; NO -> fuel ; NO -> urea (routed below fat-burn box)
s.append(path(f"M{Px-30},273 L{Px-30},322 L228,331"))     # gate YES -> MPS
s.append(arr(228,381,262,551))                            # MPS -> muscle
s.append(path(f"M{Px+40},273 L{Px+40},430 L300,438"))     # gate NO -> fuel
s.append(lbl(Px+70,296,"no signal ↓"))
s.append(path(f"M{Px+62},273 V308 H560 V331"))            # gate NO -> urea (below fat-burn)
s.append(lbl(430,320,"deaminate",color=G))
# INSULIN influence (dashed green): blocks fat-burn
s.append(path(f"M560,158 L{Fx+64},214",color=GRN,dash="4 3"))
s.append(lbl(556,206,"✕ fat-burn",color=GRN))
# DEFICIT mobilise (dashed coral, stores -> fuel)
s.append(path(f"M120,550 L120,496",color=RED,dash="4 3"))
s.append(path(f"M{Px},550 L{Px},496",color=RED,dash="4 3"))
s.append(path(f"M492,550 L470,496",color=RED,dash="4 3"))
s.append(lbl(Px,538,"when deficit: mobilise → fuel",color=RED))

svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" viewBox="0 0 {W} {H}">'\
    f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'\
    f'<path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>'\
    f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>'+"".join(s)+"</svg>"
open(f"{OUT}/master_map.svg","w").write(svg)
import cairosvg
cairosvg.svg2png(bytestring=svg.encode(),write_to=f"{OUT}/master_map.png",output_width=W,output_height=H)
# embed variant: responsive width, transparent bg
svg_embed=svg.replace(f'width="{W}" viewBox','width="100%" viewBox').replace(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>','')
open(f"{OUT}/master_map_embed.svg","w").write(svg_embed)
print("rendered",W,"x",H,"| embed bytes",len(svg_embed))
