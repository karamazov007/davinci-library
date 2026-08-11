# -*- coding: utf-8 -*-
OUT="/sessions/lucid-blissful-curie/mnt/outputs"
INK="#1c2431";MUT="#5b6572";GRID="#e6e8ee";CYAN="#0891b2";AMBER="#d97706";ROSE="#db2777";SLATE="#64748b";BLUE="#2563eb";VIOLET="#7c3aed";GREEN="#16a34a";MAROON="#9f1239";TEAL="#0d9488";SUN="#ca8a04"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def T(x,y,t,fs=12,fill=INK,anc="middle",fw=400,it=False):
    st=' font-style="italic"' if it else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anc}" fill="{fill}" font-size="{fs}" font-weight="{fw}"{st} font-family="Helvetica,Arial,sans-serif">{esc(t)}</text>'
def R(x,y,w,h,fill,rx=4,op=1.0,stroke="",sw=0):
    stk=f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" opacity="{op}"{stk}/>'

def meal_bars():
    W,H=760,330; x0=90; bottom=250; top=60; s=[]
    meals=[("Breakfast",46,780,SUN),("Lunch",35,620,GREEN),("Post-workout",34,300,VIOLET),("Dinner",33,760,ROSE)]
    def Y(v): return bottom-(v/50.0)*(bottom-top)
    for g in (0,10,20,30,40,50):
        s.append(f'<line x1="{x0}" y1="{Y(g):.1f}" x2="{690}" y2="{Y(g):.1f}" stroke="{GRID}" stroke-width="1"/>')
        s.append(T(x0-10,Y(g)+4,f"{g}",10.5,MUT,"end"))
    cx=[180,340,500,620]; bw=90
    for i,(name,p,k,col) in enumerate(meals):
        x=cx[i]-bw/2
        s.append(R(x,Y(p),bw,bottom-Y(p),col,6))
        s.append(T(cx[i],Y(p)-22,f"{p} g",13,col,"middle",700)); s.append(T(cx[i],Y(p)-7,f"{k} kcal",10.5,MUT))
        s.append(T(cx[i],bottom+20,name,11.5,INK,"middle",700))
    s.append(T((x0+690)/2,40,"Protein spread across the day — 33–46 g hits per meal (~148 g total, ~2,460 kcal)",12.5,INK,"middle",700))
    s.append(T(30,(top+bottom)/2,"protein (g)",11.5,MUT,"middle"))
    s.append(T((x0+690)/2,H-14,"+ optional on-the-go seeds/nuts, or a 2nd whey scoop only on low-protein days.",11,MUT,"middle",False,True))
    return "".join(s),H

def toolbox():
    items=[("Whey 1 scoop",24,120,"dairy",CYAN,80,"4/5"),("Low-fat paneer 100 g",20,200,"dairy",CYAN,20,"1/5"),
           ("Soy chunks 30 g dry",15,110,"legume",GREEN,52,"1/2"),("Greek/hung curd 150 g",15,130,"dairy",CYAN,10,"1/10"),
           ("Kabuli chana 1 katori",9,180,"legume",GREEN,20,"1/5"),("Rajma 1 katori",8,160,"legume",GREEN,22,"1/5"),
           ("Dal 1 katori",8,150,"legume",GREEN,22,"1/5"),("Tofu 100 g",8,80,"legume",GREEN,8,"1/12"),
           ("Peanuts 30 g",7.5,170,"nut",AMBER,25,"1/4"),("Moong sprouts 1 cup",7,100,"legume",GREEN,9,"1/10"),
           ("Almonds 30 g",6,170,"nut",AMBER,21,"1/5"),("1 egg",6,70,"egg",SUN,13,"1/8"),
           ("Green peas 100 g",5,130,"legume",GREEN,5,"1/20"),("Peanut butter 1 tbsp",4,95,"nut",AMBER,25,"1/4"),
           ("Pumpkin seeds 1 tbsp",3,55,"seed",VIOLET,30,"1/3"),("Flax/chia 1 tbsp",2,55,"seed",VIOLET,18,"1/6")]
    row=30; W,H=760,len(items)*row+116; x0=210; xmax=540; s=[]
    s.append(T(20,30,"Protein toolbox — per serving (bar) · calories · protein as a fraction of weight",13,INK,"start",700))
    lg=[("legumes",GREEN),("dairy",CYAN),("nuts",AMBER),("seeds",VIOLET),("egg",SUN)]
    for i,(l,c) in enumerate(lg):
        s.append(R(20+i*95,46,12,12,c,3)); s.append(T(36+i*95,56,l,10.5,MUT,"start"))
    s.append(T(744,56,"fraction by weight →",10.5,MUT,"end",700))
    def pc(v): return "#0f7a3c" if v>=40 else (INK if v>=15 else MUT)
    for i,(name,p,k,grp,c,pct,frac) in enumerate(items):
        y=78+i*row
        s.append(T(x0-8,y+13,name,11,INK,"end",600))
        bw=(xmax-x0)*(p/24.0)
        s.append(R(x0,y,bw,18,c,4))
        s.append(T(x0+bw+8,y+13,f"{p:g} g · {k} kcal",10.5,MUT,"start"))
        s.append(T(744,y+13,frac,12.5,pc(pct),"end",800))
    s.append(T(20,H-14,"Fraction = protein per gram of food (soy/legumes measured dry). E.g. 100 g soy ≈ 50 g protein · 100 g paneer ≈ 20 g · 200 g Greek curd ≈ 20 g.",10.5,MUT,"start",400,True))
    return "".join(s),H

def swap():
    W,H=760,340; s=[]
    rows=[("Gourd veg","2 g",MAROON,"soy 15g · rajma 8g · chana 9g · paneer 18g · beans+corn 5g",GREEN),
          ("Plain potato sabzi","3 g",MAROON,"rajma 8g · chana 9g · moong sprouts 7g",GREEN),
          ("Regular dahi","5 g",MAROON,"Greek / hung curd  15 g",GREEN),
          ("Peanut butter (plain spoon)","sticky!",AMBER,"PB on 1 slice bread — easy, no teeth-stick",GREEN)]
    s.append(T(20,32,"Upgrade the weak spots — swap for more protein",13,INK,"start",700))
    y0=64; dy=66
    for i,(bl,bv,bc,af,ac) in enumerate(rows):
        y=y0+i*dy
        s.append(R(30,y,190,46,"#fbeaea",10,1,bc,1.2)); s.append(T(125,y+20,bl,11.5,INK,"middle",700)); s.append(T(125,y+37,bv,11,bc,"middle",700))
        s.append(f'<line x1="228" y1="{y+23}" x2="286" y2="{y+23}" stroke="{MUT}" stroke-width="2" marker-end="url(#mar)"/>')
        s.append(R(296,y,434,46,"#eafaf1",10,1,ac,1.2)); s.append(T(513,y+28,af,11.5,"#0f7a3c","middle",700))
    defs='<defs><marker id="mar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1.5 1.5L8 5L1.5 8.5" fill="none" stroke="context-stroke" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>'
    return defs+"".join(s),H

def addons():
    items=[("Whey + milk (backup)",34,"no-cook","1 scoop + 300 ml — the universal plug"),
           ("Raw paneer cubes 100 g",20,"no-cook","cube + chaat masala — zero cooking"),
           ("Boiled soy chunks 30 g",15,"batch","boil a batch; toss into any dish"),
           ("2 boiled eggs",12,"quick","keep a few boiled ready"),
           ("Boiled chana / rajma 1 katori",9,"batch","chana chaat, or add to any sabzi"),
           ("Curd / Greek curd 50–150 g",8,"no-cook","a bowl on the side; Greek = 3× protein"),
           ("Sprouted moong 1 cup",7,"batch","raw salad + lemon + onion")]
    prepc={"no-cook":("#eafaf1","#0f7a3c"),"batch":("#e6f1fb","#185fa5"),"quick":("#fdf0d9","#a15a12")}
    rowh=56; W,H=760,len(items)*rowh+72; s=[]
    s.append(T(20,30,"Quick protein add-ons — grab ONE for any lunch/dinner",13,INK,"start",700))
    s.append(T(20,50,"green = no cooking   ·   blue = batch-prep (weekly)   ·   amber = 2-minute",11,MUT,"start"))
    for i,(name,p,prep,how) in enumerate(items):
        y=66+i*rowh
        s.append(R(20,y,720,48,"#f7f8fa",10,1,"#eef0f4",1))
        s.append(T(38,y+21,name,12.5,INK,"start",700)); s.append(T(38,y+38,how,10.5,MUT,"start"))
        s.append(T(575,y+30,f"{p} g",17,ROSE,"end",800))
        bg,tc=prepc[prep]; s.append(R(600,y+13,120,22,bg,11,1,tc,1)); s.append(T(660,y+28,prep,11,tc,"middle",700))
    return "".join(s),H

def heuristics():
    panels=[
     ("PROTEIN",ROSE,"#fdf2f8",["Each meal ≈ 35–40 g (1–2 sources)","Lunch & dinner ALWAYS get a protein add-on",
        "Daily total rules (~1.6–2.2 g/kg)","Per-meal ceiling ~0.4 g/kg (~27 g) → spread","Protein = fixed rail; carbs & fat flex"]),
     ("ENERGY & GOALS",VIOLET,"#f5f0fe",["Maintenance ≈ bodyweight(kg) × 30–33","Lean bulk ×1.10  ·  cut ×0.80",
        "The weekly scale is the real calculator","Calories = direction; protein+train = tissue","Definition = body-fat %, not scale weight"]),
     ("FOOD QUALITY",GREEN,"#eefaf0",["Complete: egg · milk · whey · paneer · soy","Combine dal + rice/roti (completes plants)",
        "Add-ons: no-cook · batch · quick (30 min/wk)","Seeds/nuts = micros + omega-3 (measure)","PB on bread · curd ~50 g · muesli low-sugar"]),
     ("TRAINING & RECOVERY",BLUE,"#eef4fd",["Progressive overload drives growth","Sleep = the anabolic window",
        "Surplus funds the build; maintenance = stuck","Two dials: cut to reveal, build to grow","Food can't fix a flat training stimulus"]),
    ]
    W,H=760,566; s=[T(20,32,"Heuristics — the thinking behind the plan",14,INK,"start",700)]
    pos=[(20,52),(390,52),(20,308),(390,308)]; pw,ph=350,238
    for (name,col,bg,bl),(px,py) in zip(panels,pos):
        s.append(R(px,py,pw,ph,bg,12,1,col,1.3))
        s.append(T(px+20,py+30,name,12.5,col,"start",800))
        s.append(f'<line x1="{px+20}" y1="{py+40}" x2="{px+pw-20}" y2="{py+40}" stroke="{col}" stroke-width="1" opacity="0.4"/>')
        for j,b in enumerate(bl):
            by=py+64+j*33
            s.append(f'<circle cx="{px+24}" cy="{by-4:.0f}" r="3.2" fill="{col}"/>')
            s.append(T(px+36,by,b,11.5,INK,"start"))
    return "".join(s),H

def brands():
    rows=[
     ("Paneer","HIGH","#dc2626","#fdeaea",
        "Amul · Mother Dairy · Nandini · Milky Mist · Gowardhan · Heritage",
        "loose / unbranded · suspiciously cheap · restaurant ‘analogue’ paneer"),
     ("Curd","LOW–MOD","#d97706","#fdf0d9",
        "Amul · Mother Dairy · Nandini · Milky Mist · (Greek) Epigamia / Nestlé a+",
        "loose curd from unknown sources"),
     ("Soya chunks","LOW","#16a34a","#eafaf1",
        "Nutrela · Fortune · Saffola · Urban Platter",
        "no-brand loose chunks"),
     ("Chana / rajma / dal","LOWEST","#0d9488","#e1f5ee",
        "Tata Sampann · 24 Mantra Organic · Organic Tattva · Fortune",
        "over-polished shiny loose stock (rinse; check for stones)"),
    ]
    rowh=80; W,H=760,len(rows)*rowh+64; s=[]
    s.append(T(20,32,"Trusted brands (India) — buy sealed & branded; paneer is the one to be strict about",13,INK,"start",700))
    for i,(food,risk,rc,rbg,trust,avoid) in enumerate(rows):
        y=52+i*rowh
        s.append(R(20,y,720,rowh-12,"#f7f8fa",10,1,"#eef0f4",1))
        s.append(T(36,y+24,food,12.5,INK,"start",700))
        s.append(R(36,y+34,116,22,rbg,11,1,rc,1)); s.append(T(94,y+49,"risk: "+risk,10.5,rc,"middle",700))
        s.append(T(200,y+24,"✓ Trust:",11,"#0f7a3c","start",700)); s.append(T(264,y+24,trust,10.5,INK,"start"))
        s.append(T(200,y+48,"✕ Avoid:",11,"#a12626","start",700)); s.append(T(264,y+48,avoid,10.5,MUT,"start"))
    return "".join(s),H

def mealmath():
    W,H=760,300; x0,x1=150,700; s=[]
    def X(g): return x0+(x1-x0)*(g/38.0)
    s.append(T(20,30,"Lunch & dinner — your staples' protein 'base', and the gap a pick must fill",13,INK,"start",700))
    tx=X(35)
    s.append(f'<line x1="{tx:.1f}" y1="56" x2="{tx:.1f}" y2="250" stroke="{INK}" stroke-width="1.4" stroke-dasharray="5 4"/>')
    s.append(T(tx,50,"~35 g target",11,INK,"middle",700))
    bars=[("LUNCH",[("rice",4,"#0891b2"),("dal",11,"#16a34a"),("salad",2,"#0d9488")],
             "fill ~+18 g:  soy chunks 15  ·  or paneer 18  ·  or chana 9 + curd"),
          ("DINNER",[("roti",9,"#d97706"),("veg",3,"#16a34a"),("mango",1.5,"#db2777")],
             "fill ~+21 g:  paneer 20  ·  or soy 15 + 1 egg  ·  or rajma 8 + whey/egg")]
    barh=34
    for bi,(meal,stap,pick) in enumerate(bars):
        y=90+bi*100
        s.append(T(24,y+22,meal,12.5,INK,"start",800))
        cur=x0; base=0
        for name,g,col in stap:
            w=g*(x1-x0)/38.0
            s.append(R(cur,y,w,barh,col,3)); base+=g
            if w>26: s.append(T(cur+w/2,y+21,f"{g:g}",11,"#fff","middle",700))
            s.append(T(cur+w/2,y+barh+15,name,9.5,MUT,"middle"))
            cur+=w
        s.append(T(x0+(cur-x0)/2,y-8,f"≈ {base:g} g from staples",10.5,MUT,"middle",700))
        gw=tx-cur
        s.append(f'<rect x="{cur:.1f}" y="{y}" width="{gw:.1f}" height="{barh}" rx="3" fill="#fdeaf2" stroke="{ROSE}" stroke-width="1.3" stroke-dasharray="5 3"/>')
        s.append(T(cur+gw/2,y+21,f"+{35-base:g} g → your PICK",11,"#a11d54","middle",700))
        s.append(T(24,y+barh+34,pick,10.5,MUT,"start"))
    return "".join(s),H

def simplified():
    W,H=760,400; s=[T(20,30,"Your simplified protein system — what's automatic vs what you add",13,INK,"start",700)]
    s.append(T(700,30,"day ≈ 137 g",11.5,MUT,"end",700))
    rows=[("Breakfast","FIXED","3–4 eggs · oats · milk · PB","~40–46 g"),
          ("Post-workout","FIXED","whey + 300 ml milk","~34 g"),
          ("Lunch","ADD","rice · dal   +   soy chunks 30 g","~32 g"),
          ("Dinner","ADD","roti · veg · mango   +   3 eggs","~31 g")]
    y0=52; rowh=52
    for i,(meal,tag,foods,prot) in enumerate(rows):
        y=y0+i*(rowh+10)
        s.append(R(20,y,720,rowh,"#f7f8fa",10,1,"#eef0f4",1))
        s.append(T(36,y+31,meal,12.5,INK,"start",700))
        bg,tc=("#eafaf1","#0f7a3c") if tag=="FIXED" else ("#fdf0d9","#a15a12")
        s.append(R(150,y+15,70,22,bg,11,1,tc,1)); s.append(T(185,y+30,tag,11,tc,"middle",700))
        s.append(T(250,y+31,foods,11.5,INK,"start"))
        s.append(T(704,y+31,prot,12.5,ROSE,"end",800))
    py=y0+4*(rowh+10)+6
    s.append(R(120,py,520,50,"#f5f0fe",12,1,VIOLET,1.3))
    s.append(T(380,py+22,"whey + milk (or water) = universal plug",12,"#5b45b0","middle",700))
    s.append(T(380,py+40,"swap in whenever you miss the Lunch soy or the Dinner eggs",10.5,MUT,"middle"))
    return "".join(s),H

def costprotein():
    items=[("Soy chunks",0.5),("Chana / rajma (dry)",0.55),("Peanuts",0.6),("Dal (dry)",0.65),
           ("Milk (toned)",0.9),("Eggs",1.1),("Paneer",1.7),("Whey",2.7),("Greek yogurt (branded)",6.0)]
    def col(v): return GREEN if v<0.75 else ("#65a30d" if v<1.05 else (AMBER if v<2.0 else "#dc2626"))
    row=34; W,H=760,len(items)*row+80; x0=210; xmax=690; s=[]
    s.append(T(20,30,"Cost per gram of protein (Rs) — soy is the champion, Greek yogurt the priciest",13,INK,"start",700))
    s.append(T(20,50,"shorter bar = more protein per rupee",11,MUT,"start"))
    for i,(name,v) in enumerate(items):
        y=70+i*row
        s.append(T(x0-8,y+13,name,11,INK,"end",600))
        bw=(xmax-x0)*(v/6.0)
        s.append(R(x0,y,bw,18,col(v),4))
        s.append(T(x0+bw+8,y+13,f"Rs {v:g}/g",10.5,MUT,"start",700))
    return "".join(s),H

def valuemap():
    # each food: (name, cost Rs/g protein, protein density % of weight, group color, label dx, dy, anchor)
    pts=[("Soy chunks",0.5,52,GREEN,11,4,"start"),
         ("Whey",2.7,80,CYAN,11,4,"start"),
         ("Paneer",1.7,20,CYAN,11,4,"start"),
         ("Greek yogurt (branded)",6.0,10,CYAN,-11,4,"end"),
         ("Chana / rajma (dry)",0.55,21,GREEN,13,16,"start"),
         ("Peanuts",0.6,25,AMBER,13,-9,"start"),
         ("Dal (dry)",0.65,22,GREEN,15,5,"start"),
         ("Milk",0.9,3.3,CYAN,11,4,"start"),
         ("Eggs",1.1,13,SUN,11,4,"start")]
    W,H=760,520; L,Rt,Tp,Bt=90,690,66,440
    cmin,cmax=0.3,6.3; dmax=85.0
    def sx(c): return L+(c-cmin)/(cmax-cmin)*(Rt-L)
    def sy(d): return Bt-(d/dmax)*(Bt-Tp)
    s=[T(20,30,"Value map — protein density vs price (top-left corner = best deal)",13,INK,"start",700)]
    s.append(T(20,48,"protein per gram of food (up) vs rupees per gram of protein (right)",10.5,MUT,"start"))
    # quadrant tints
    s.append(R(L,Tp,sx(1.25)-L,sy(35)-Tp,"#eafaf1",0,1))       # top-left best
    s.append(R(sx(2.6),sy(28),Rt-sx(2.6),Bt-sy(28),"#fdeaea",0,1))  # bottom-right worst
    s.append(T(L+10,Tp+18,"BEST: protein-dense & cheap",10.5,"#0f7a3c","start",700))
    s.append(T(Rt-8,Bt-10,"worst: dilute & pricey",10.5,"#b42318","end",700))
    # axes
    s.append(f'<line x1="{L}" y1="{Bt}" x2="{Rt}" y2="{Bt}" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="{L}" y1="{Tp}" x2="{L}" y2="{Bt}" stroke="{INK}" stroke-width="1.3"/>')
    for c in (0.5,1,2,3,4,5,6):
        x=sx(c); s.append(f'<line x1="{x:.1f}" y1="{Bt}" x2="{x:.1f}" y2="{Bt+5}" stroke="{MUT}" stroke-width="1"/>')
        s.append(T(x,Bt+18,f"Rs {c:g}",9.5,MUT,"middle"))
    for d in (0,20,40,60,80):
        y=sy(d); s.append(f'<line x1="{L-5}" y1="{y:.1f}" x2="{L}" y2="{y:.1f}" stroke="{MUT}" stroke-width="1"/>')
        s.append(T(L-9,y+3,f"{d}%",9.5,MUT,"end"))
    s.append(T((L+Rt)/2,Bt+36,"cost per gram of protein  →  (cheaper on the left)",11,INK,"middle",700))
    s.append(f'<text x="26" y="{(Tp+Bt)/2:.1f}" text-anchor="middle" fill="{INK}" font-size="11" font-weight="700" font-family="Helvetica,Arial,sans-serif" transform="rotate(-90 26 {(Tp+Bt)/2:.1f})">protein per gram of food  →  (denser at the top)</text>')
    # points
    for name,c,d,col,dx,dy,anc in pts:
        x,y=sx(c),sy(d)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{col}" stroke="#fff" stroke-width="1.6"/>')
        s.append(T(x+dx,y+dy,name,10.5,INK,anc,700))
    lg=[("legumes",GREEN),("dairy",CYAN),("nuts",AMBER),("egg",SUN)]
    for i,(l,c) in enumerate(lg):
        s.append(R(430+i*80,44,11,11,c,3)); s.append(T(445+i*80,54,l,10,MUT,"start"))
    return "".join(s),H

def looks18():
    TC={"engine":ROSE,"support":BLUE,"decoration":SLATE}
    pts=[("Soy chunks (dry)",35,"engine","≈ 35 g dry"),
         ("Paneer (low-fat)",90,"engine","≈ 90 g"),
         ("Eggs",150,"engine","3 eggs"),
         ("Chana / rajma",200,"support","2 katori"),
         ("Masoor dal",200,"support","2 katori"),
         ("Tofu",225,"engine","≈ 225 g"),
         ("Moong (cooked)",260,"support","2½ katori"),
         ("Green peas",360,"decoration","3+ katori"),
         ("Broccoli",700,"decoration","≈ 700 g"),
         ("Green beans",1000,"decoration","≈ 1 kg")]
    row=34; W,H=760,len(pts)*row+120; x0=150; xmax=610; mg=1000.0; s=[]
    s.append(T(20,28,"The SAME 18 g of protein — how much food you'd have to eat",13,INK,"start",700))
    s.append(T(20,47,"every bar = 18 g protein · bar length = grams of that food needed",10.5,MUT,"start"))
    lg=[("engine",ROSE),("support",BLUE),("decoration",SLATE)]
    for i,(l,c) in enumerate(lg):
        s.append(R(430+i*110,38,11,11,c,3)); s.append(T(445+i*110,48,l,10,MUT,"start"))
    for i,(name,g,tier,meas) in enumerate(pts):
        y=70+i*row
        s.append(T(x0-8,y+13,name,11,INK,"end",600))
        bw=(xmax-x0)*(g/mg)
        s.append(R(x0,y,bw,18,TC[tier],4))
        s.append(T(x0+bw+8,y+13,f"{g} g · {meas}",10.5,MUT,"start",700))
    s.append(T(20,H-16,"Soy needs 35 g. Green beans need 1 kg — ~28× more food for the exact same 18 g of protein.",11,MAROON,"start",700))
    return "".join(s),H

def tiers():
    W,H=760,384
    rows=[("THE ENGINE",ROSE,"#fdeef5","soy · paneer · eggs · whey · tofu · curd",
           "Protein without the volume or the calories — put most of your protein here."),
          ("THE SUPPORT",BLUE,"#eaf1fd","dal · chana · rajma · moong · masoor",
           "Real protein (~2 katori ≈ 18 g) but bulky & carb-heavy — the base, not the whole meal."),
          ("DECORATIONS",SLATE,"#eef1f5","broccoli · green beans · green peas · most sabzi",
           "Trace protein in a huge volume — eat for fibre & fullness, never for protein.")]
    s=[T(20,30,"Three tiers of vegetarian protein — where to actually get it",13,INK,"start",700)]
    ph=92; gap=16; y0=54
    for i,(title,col,tint,foods,why) in enumerate(rows):
        y=y0+i*(ph+gap)
        s.append(R(20,y,700,ph,tint,12))
        s.append(R(20,y,10,ph,col,0))
        s.append(T(44,y+32,title,15,col,"start",800))
        s.append(T(44,y+58,foods,13,INK,"start",700))
        s.append(T(44,y+80,why,11,MUT,"start",400,True))
    s.append(f'<text x="742" y="{y0+ph+gap+ph/2:.1f}" text-anchor="middle" fill="{MUT}" font-size="10.5" font-weight="700" font-family="Helvetica,Arial,sans-serif" transform="rotate(-90 742 {y0+ph+gap+ph/2:.1f})">protein density: high → low</text>')
    return "".join(s),H

def core():
    W,H=760,392
    s=[T(20,32,"Your 3 daily non-negotiables",15,INK,"start",800)]
    s.append(T(20,52,"eat these almost every day — everything else is optional",11,MUT,"start"))
    cards=[(30,"🥚 Eggs",SUN,"DAILY","6 eggs","~36 g","safe · your floor"),
           (285,"🫘 Soya chunks",GREEN,"DAILY","40 g dry","~20 g","cheap & lean · ~Rs 12"),
           (540,"🧀 Paneer",CYAN,"SWAP","90–100 g","~18–20 g","a few days/wk · ~Rs 35")]
    for x,name,col,tag,amt,prot,note in cards:
        s.append(R(x,66,205,150,"#ffffff",14,1,col,1.6))
        s.append(R(x+14,80,58,20,col,10)); s.append(T(x+43,94,tag,10,"#fff","middle",800))
        s.append(T(x+16,128,name,14.5,col,"start",800))
        s.append(T(x+16,160,amt,20,INK,"start",800))
        s.append(T(x+16,184,prot+" protein",13,col,"start",700))
        s.append(T(x+16,205,note,10.5,MUT,"start"))
    s.append(f'<circle cx="515" cy="141" r="17" fill="#fff" stroke="{VIOLET}" stroke-width="1.6"/>')
    s.append(T(515,146,"⇄",15,VIOLET,"middle",800))
    s.append(T(515,178,"some days",9.5,VIOLET,"middle",700))
    s.append(R(30,238,715,48,"#f7f8fa",12,1,"#eef0f4",1))
    s.append(T(387,259,"6 eggs (36) + 40 g soya (20) + whey + 300 ml milk (34) + dal & staples (~40)",12,INK,"middle",600))
    s.append(T(387,277,"≈ 140 g protein / day",13,ROSE,"middle",800))
    s.append(R(30,300,715,50,"#fdeef5",12,1,ROSE,1))
    s.append(T(387,322,"Everything else — sabzi · salad · fruit — is DECORATION",12.5,MAROON,"middle",800))
    s.append(T(387,340,"eat it for fibre & fullness, never for protein",11,MUT,"middle"))
    return "".join(s),H

def looksall():
    # (name, grams-of-food for 18 g protein, group color, household measure)
    pts=[("Whey",22,CYAN,"¾ scoop"),
         ("Soy chunks (dry)",35,GREEN,"35 g dry"),
         ("Pumpkin seeds",60,VIOLET,"~6 tbsp"),
         ("Peanut butter",72,AMBER,"~5 tbsp"),
         ("Peanuts",72,AMBER,"~72 g"),
         ("Almonds",86,AMBER,"~65 nuts"),
         ("Low-fat paneer",90,CYAN,"~90 g"),
         ("Flax / chia",100,VIOLET,"~100 g"),
         ("Eggs",150,SUN,"3 eggs"),
         ("Greek / hung curd",180,CYAN,"~180 g"),
         ("Kabuli chana",200,GREEN,"2 katori"),
         ("Rajma",200,GREEN,"2 katori"),
         ("Tofu",225,GREEN,"~225 g"),
         ("Dal (cooked)",230,GREEN,"2 katori"),
         ("Moong (cooked)",260,GREEN,"2½ katori"),
         ("Green peas",360,GREEN,"3+ katori")]
    row=30; W,H=760,len(pts)*row+118; x0=175; xmax=560; mg=360.0; s=[]
    s.append(T(20,28,"18 g of protein from every toolbox food — how much you'd eat",13,INK,"start",700))
    s.append(T(20,47,"every bar = 18 g protein · bar length = grams of that food · concentrated at top",10.5,MUT,"start"))
    lg=[("legumes",GREEN),("dairy",CYAN),("nuts",AMBER),("seeds",VIOLET),("egg",SUN)]
    for i,(l,c) in enumerate(lg):
        s.append(R(430+i*66,38,10,10,c,3)); s.append(T(444+i*66,47,l,9.5,MUT,"start"))
    for i,(name,g,col,meas) in enumerate(pts):
        y=72+i*row
        s.append(T(x0-8,y+13,name,11,INK,"end",600))
        bw=(xmax-x0)*(g/mg)
        s.append(R(x0,y,bw,18,col,4))
        s.append(T(x0+bw+8,y+13,f"{g} g · {meas}",10.5,MUT,"start",700))
    s.append(T(20,H-16,"Same 18 g everywhere: whey/soy need a handful; legumes need ~2 katori; green peas need 3+ katori. Concentrated = less food, fewer calories.",10.5,MAROON,"start",700))
    return "".join(s),H

charts=[("m_core",core),("m_looksall",looksall),("m_heur",heuristics),("m_bars",meal_bars),("m_tool",toolbox),("m_swap",swap),("m_addons",addons),("m_brands",brands),("m_math",mealmath),("m_simple",simplified),("m_cost",costprotein),("m_value",valuemap),("m_looks",looks18),("m_tiers",tiers)]
for name,fn in charts:
    body,h=fn(); open(f"{OUT}/{name}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 760 {h}">{body}</svg>')
import cairosvg
off=0;parts=[]
for name,fn in charts:
    body,h=fn();parts.append(f'<g transform="translate(0,{off})">{body}</g>');off+=h+16
comp=f'<svg xmlns="http://www.w3.org/2000/svg" width="760" viewBox="0 0 760 {off}"><rect width="760" height="{off}" fill="#fff"/>'+"".join(parts)+"</svg>"
cairosvg.svg2png(bytestring=comp.encode(),write_to=f"{OUT}/meal_verify.png",output_width=760,output_height=off)
print("meal charts rendered",off)
