const C={ink:'#1f2933',mut:'#5b6572',line:'#c3cbd8',a1:'#4f46e5',a2:'#0891b2',a3:'#db2777',a4:'#ea580c',a5:'#16a34a',a6:'#9333ea'};

const MK=`<defs>
<marker id="mA" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6z" fill="${C.mut}"/></marker>
<marker id="mR" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6z" fill="${C.a3}"/></marker>
<marker id="mB" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6z" fill="${C.a1}"/></marker></defs>`;

const escT=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

const P=[C.a1,C.a2,C.a4,C.a5,C.a6,C.a3];

function SV(inner,w=680,h=460){return `<svg viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">${MK}${inner}</svg>`;}
function T(x,y,txt,{fill=C.ink,fs=12,fw=400,anchor='middle',tr=''}={}){return `<text x="${x}" y="${y}" text-anchor="${anchor}" fill="${fill}" font-size="${fs}" font-weight="${fw}"${tr?` transform="${tr}"`:''}>${escT(txt)}</text>`;}
function ML(x,y,label,o={}){const lines=String(label).split('\n');const lh=o.lh||13;const off=(lines.length-1)*lh/2;return lines.map((ln,i)=>T(x,y-off+i*lh,ln,o)).join('');}
function boxN(x,y,w,h,label,{fill=C.a1,tc='#fff',fs=12,r=9,stroke='',sw=0}={}){const lines=String(label).split('\n');const startY=y+h/2-((lines.length-1)*7)+4;return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}"${stroke?` stroke="${stroke}" stroke-width="${sw}"`:''}/>`+lines.map((ln,i)=>T(x+w/2,startY+i*14,ln,{fill:tc,fs,fw:600})).join('');}

function genGraph(nodes,edges,{w=700,h=460,pad=26}={}){
  const px=n=>pad+n.x*(w-2*pad), py=n=>pad+n.y*(h-2*pad); const byId={}; nodes.forEach(n=>byId[n.id]=n); let s='';
  (edges||[]).forEach(e=>{const a=byId[e.from],b=byId[e.to]; if(!a||!b)return; let x1=px(a),y1=py(a),x2=px(b),y2=py(b);
    const dx=x2-x1,dy=y2-y1,d=Math.hypot(dx,dy)||1;
    const o1=(a.r||(a.w?Math.max(a.w,a.h)/2:26))+2, o2=(b.r||(b.w?Math.max(b.w,b.h)/2:26))+7;
    x1+=dx/d*o1; y1+=dy/d*o1; x2-=dx/d*o2; y2-=dy/d*o2;
    const mk=e.arrow===false?'':`marker-end="url(#${e.mk||'mA'})"`, col=e.color||C.mut; let lmx,lmy;
    if(e.curve){const mxp=(x1+x2)/2-dy/d*e.curve, myp=(y1+y2)/2+dx/d*e.curve; s+=`<path d="M${x1},${y1} Q${mxp},${myp} ${x2},${y2}" fill="none" stroke="${col}" stroke-width="${e.w||1.7}" ${e.dash?`stroke-dasharray="${e.dash}"`:''} ${mk}/>`; lmx=(x1+2*mxp+x2)/4; lmy=(y1+2*myp+y2)/4;}
    else {s+=`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${e.w||1.7}" ${e.dash?`stroke-dasharray="${e.dash}"`:''} ${mk}/>`; lmx=(x1+x2)/2; lmy=(y1+y2)/2;}
    if(e.label){const lw=String(e.label).length*6+8; s+=`<rect x="${lmx-lw/2}" y="${lmy-9}" width="${lw}" height="16" rx="4" fill="#fff" opacity=".92"/>`+T(lmx,lmy+3,e.label,{fill:e.lc||C.mut,fs:e.label.length<3?12:9.5,fw:e.label.length<3?800:400});}
  });
  nodes.forEach((n,i)=>{const cx=px(n),cy=py(n),fill=n.fill||P[i%P.length],tc=n.tc||'#fff',shape=n.shape||'round';
    if(shape==='circle'){const r=n.r||30; s+=`<circle cx="${cx}" cy="${cy}" r="${r}" fill="${n.hollow?'#fff':fill}"${n.hollow?` stroke="${fill}" stroke-width="2.5"`:''}/>`+ML(cx,cy+4,n.label,{fill:n.hollow?C.ink:tc,fs:n.fs||11,fw:600});}
    else if(shape==='diamond'){const ww=n.w||96,hh=n.h||64; s+=`<polygon points="${cx},${cy-hh/2} ${cx+ww/2},${cy} ${cx},${cy+hh/2} ${cx-ww/2},${cy}" fill="${n.hollow?'#fff':fill}"${n.hollow?` stroke="${fill}" stroke-width="2.5"`:''}/>`+ML(cx,cy+4,n.label,{fill:n.hollow?C.ink:tc,fs:n.fs||10,fw:600});}
    else {const ww=n.w||110,hh=n.h||44; s+=boxN(cx-ww/2,cy-hh/2,ww,hh,n.label,{fill,tc,fs:n.fs||11,r:shape==='rect'?4:12});}
  });
  return SV(s,w,h);
}
function genMindMap(center,branches,{w=780,h=540}={}){const cx=w/2,cy=h/2,R1=Math.min(w,h)*0.29,rr=Math.min(w,h)*0.185,n=branches.length; let s='';
  branches.forEach((br,i)=>{const ang=-Math.PI/2+i*2*Math.PI/n,bx=cx+Math.cos(ang)*R1,by=cy+Math.sin(ang)*R1,col=P[i%P.length];
    s+=`<path d="M${cx},${cy} Q${(cx+bx)/2},${(cy+by)/2} ${bx},${by}" fill="none" stroke="${col}" stroke-width="2.5"/>`;
    const kids=br.children||[],spread=Math.PI/2.6;
    kids.forEach((k,j)=>{const ka=ang+(kids.length>1?(-spread/2+j*spread/(kids.length-1)):0),kx=bx+Math.cos(ka)*rr,ky=by+Math.sin(ka)*rr;
      s+=`<line x1="${bx}" y1="${by}" x2="${kx}" y2="${ky}" stroke="${col}" stroke-width="1.4" opacity=".65"/>`;
      s+=`<rect x="${kx-48}" y="${ky-13}" width="96" height="26" rx="13" fill="#fff" stroke="${col}" stroke-width="1.4"/>`+ML(kx,ky+4,k,{fill:C.ink,fs:9.5,fw:600});});
    s+=boxN(bx-58,by-19,116,38,br.label,{fill:col,fs:11,r:19});});
  s+=`<circle cx="${cx}" cy="${cy}" r="48" fill="${C.ink}"/>`+ML(cx,cy+4,center,{fill:'#fff',fs:13,fw:700});
  return SV(s,w,h);}
function genTree(root,{w=720,h=440,pad=44,boxW=118,boxH=40}={}){let leaves=[];const levels=[];
  (function walk(n,d){n._d=d;levels[d]=1;if(!n.children||!n.children.length)leaves.push(n);else n.children.forEach(c=>walk(c,d+1));})(root,0);
  const maxD=levels.length-1;
  w=Math.max(w, pad*2+boxW+(Math.max(1,leaves.length-1))*(boxW+26));
  const xGap=(w-2*pad-boxW)/Math.max(1,leaves.length-1);
  leaves.forEach((lf,i)=>lf._x=leaves.length===1?w/2:pad+boxW/2+i*xGap);
  const yGap=(h-2*pad-boxH)/Math.max(1,maxD);
  (function setx(n){if(n.children&&n.children.length){n.children.forEach(setx);n._x=(n.children[0]._x+n.children[n.children.length-1]._x)/2;}n._y=pad+n._d*yGap;})(root);
  let s='';const pal=[C.a2,C.a4,C.a5,C.a6,C.a3];
  (function ed(n){if(n.children)n.children.forEach(c=>{s+=`<path d="M${n._x},${n._y+boxH} C${n._x},${(n._y+boxH+c._y)/2} ${c._x},${(n._y+boxH+c._y)/2} ${c._x},${c._y}" fill="none" stroke="${C.line}" stroke-width="1.6"/>`;ed(c);});})(root);
  (function nd(n){const col=n._d===0?C.a1:pal[(n._d-1)%pal.length];s+=boxN(n._x-boxW/2,n._y,boxW,boxH,n.label,{fill:n._d===0?C.a1:'#fff',tc:n._d===0?'#fff':C.ink,stroke:n._d===0?'':col,sw:1.8,fs:10.5,r:8});if(n.children)n.children.forEach(nd);})(root);
  return SV(s,w,h);}
function genPyramid(levels,{w=680,h=460}={}){const n=levels.length,top=44,botW=w-160,ax=w/2,H=h-100,lh=H/n;let s='';
  levels.forEach((lv,i)=>{const y0=top+i*lh,y1=top+(i+1)*lh,wt=botW*i/n,wb=botW*(i+1)/n;
    s+=`<polygon points="${ax-wt/2},${y0} ${ax+wt/2},${y0} ${ax+wb/2},${y1} ${ax-wb/2},${y1}" fill="${lv.color||P[i%P.length]}"/>`;
    s+=ML(ax,(y0+y1)/2+4,lv.label,{fill:'#fff',fs:12,fw:700});
    if(lv.sub)s+=T(ax+wb/2+10,(y0+y1)/2+4,lv.sub,{fill:C.mut,fs:10,anchor:'start'});});
  return SV(s,w,h);}
function genTreemap(items,{w=680,h=440,pad=8}={}){const total=items.reduce((a,b)=>a+b.weight,0);let it=items.slice().sort((a,b)=>b.weight-a.weight);
  const x=pad,rw=w-2*pad,rh=h-2*pad;let curY=pad,s='',rem=it.slice();
  while(rem.length){const rc=Math.min(rem.length,rem.length<=3?rem.length:2),row=rem.splice(0,rc),rowW=row.reduce((a,b)=>a+b.weight,0),rowH=rh*(rowW/total);let curX=x;
    row.forEach(item=>{const cw=rw*(item.weight/rowW);s+=`<rect x="${curX}" y="${curY}" width="${cw-4}" height="${rowH-4}" rx="6" fill="${item.color||C.a1}"/>`;
      s+=ML(curX+(cw-4)/2,curY+rowH/2-2,item.label,{fill:'#fff',fs:11.5,fw:700});
      s+=T(curX+(cw-4)/2,curY+rowH/2+16,Math.round(item.weight/total*100)+'%',{fill:'rgba(255,255,255,.85)',fs:10});curX+=cw;});curY+=rowH;}
  return SV(s,w,h);}
function genTimeline(events,{w=780,h=420}={}){const y=h/2,x0=54,x1=w-54,n=events.length;let s=`<line x1="${x0}" y1="${y}" x2="${x1}" y2="${y}" stroke="${C.line}" stroke-width="3"/>`;
  events.forEach((e,i)=>{const x=x0+(x1-x0)*(n===1?0.5:i/(n-1)),dir=i%2===0?-1:1,col=P[i%P.length];
    s+=`<circle cx="${x}" cy="${y}" r="7" fill="${col}"/>`;const ly=y+dir*74;
    s+=`<line x1="${x}" y1="${y}" x2="${x}" y2="${ly+(dir<0?24:-24)}" stroke="${col}" stroke-width="1.6"/>`;
    s+=`<rect x="${x-72}" y="${ly-24}" width="144" height="54" rx="9" fill="#fff" stroke="${col}" stroke-width="1.6"/>`;
    s+=T(x,ly-6,e.when,{fill:col,fs:11.5,fw:700})+ML(x,ly+13,e.label,{fill:C.ink,fs:9.5,fw:600,lh:11});});
  return SV(s,w,h);}
function genCycle(stages,{w=620,h=560,center=''}={}){const cx=w/2,cy=h/2,R=Math.min(w,h)*0.30,n=stages.length;let s=`<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="${C.line}" stroke-width="1.5" stroke-dasharray="5 5"/>`;
  const pts=stages.map((st,i)=>{const a=-Math.PI/2+i*2*Math.PI/n;return{x:cx+Math.cos(a)*R,y:cy+Math.sin(a)*R,a};});
  for(let i=0;i<n;i++){const p=pts[i],q=pts[(i+1)%n],a1=p.a+0.44,a2=q.a-0.44,x1=cx+Math.cos(a1)*R,y1=cy+Math.sin(a1)*R,x2=cx+Math.cos(a2)*R,y2=cy+Math.sin(a2)*R;
    s+=`<path d="M${x1},${y1} A${R},${R} 0 0 1 ${x2},${y2}" fill="none" stroke="${C.mut}" stroke-width="2" marker-end="url(#mA)"/>`;}
  stages.forEach((st,i)=>{const p=pts[i],col=P[i%P.length];s+=`<circle cx="${p.x}" cy="${p.y}" r="46" fill="${col}"/>`+ML(p.x,p.y+4,st.label,{fill:'#fff',fs:11,fw:700});
    if(st.note){const ox=cx+(p.x-cx)*1.62,oy=cy+(p.y-cy)*1.62;s+=ML(ox,oy,st.note,{fill:C.mut,fs:9,lh:10});}});
  if(center)s+=ML(cx,cy,center,{fill:C.ink,fs:12,fw:700});
  return SV(s,w,h);}
function genSankey(source,flows,{w=740,h=460}={}){const total=flows.reduce((a,b)=>a+b.value,0),pad=34,barX=64,barW=28,sy0=pad,sy1=h-pad,H=sy1-sy0;
  let s=`<rect x="${barX}" y="${sy0}" width="${barW}" height="${H}" rx="5" fill="${C.a1}"/>`+ML(barX+barW/2,sy0-14,source,{fill:C.ink,fs:12,fw:700,lh:12});
  const rightX=w-250;let cur=sy0;
  flows.forEach((f,i)=>{const th=H*(f.value/total),col=f.color||P[i%P.length],x1=barX+barW,x2=rightX;
    s+=`<path d="M${x1},${cur} C${(x1+x2)/2},${cur} ${(x1+x2)/2},${cur} ${x2},${cur} L${x2},${cur+th} C${(x1+x2)/2},${cur+th} ${(x1+x2)/2},${cur+th} ${x1},${cur+th} Z" fill="${col}" opacity=".5"/>`;
    s+=`<rect x="${x2}" y="${cur}" width="15" height="${th}" fill="${col}"/>`;
    s+=T(x2+24,cur+th/2+4,`${f.label} (${Math.round(f.value/total*100)}%)`,{fill:C.ink,fs:11,anchor:'start',fw:600});cur+=th;});
  return SV(s,w,h);}
function genFishbone(effect,bones,{w=800,h=470}={}){const y=h/2,x0=40,xEnd=w-170;let s=`<line x1="${x0}" y1="${y}" x2="${xEnd}" y2="${y}" stroke="${C.ink}" stroke-width="2.5"/>`;
  s+=`<polygon points="${xEnd},${y-9} ${xEnd+22},${y} ${xEnd},${y+9}" fill="${C.ink}"/>`+boxN(xEnd+26,y-27,132,54,effect,{fill:C.a4,fs:11});
  const ups=bones.filter((_,i)=>i%2===0),downs=bones.filter((_,i)=>i%2===1);
  const place=(arr,dir)=>{const m=arr.length;arr.forEach((b,k)=>{const bx=x0+90+(xEnd-x0-150)*((k+0.5)/m),tipx=bx-64,tipy=y+dir*150,col=P[bones.indexOf(b)%P.length];
    s+=`<line x1="${bx}" y1="${y}" x2="${tipx}" y2="${tipy}" stroke="${col}" stroke-width="2.2"/>`+T(tipx,tipy+(dir<0?-9:20),b.name,{fill:col,fs:11,fw:700});
    (b.causes||[]).forEach((c,j)=>{const t=(j+1)/(b.causes.length+1),cxp=bx+(tipx-bx)*t,cyp=y+(tipy-y)*t;s+=`<line x1="${cxp}" y1="${cyp}" x2="${cxp+28}" y2="${cyp}" stroke="${col}" stroke-width="1.1" opacity=".7"/>`+T(cxp+32,cyp+3,c,{fill:C.ink,fs:9,anchor:'start'});});});};
  place(ups,-1);place(downs,1);return SV(s,w,h);}
function genVenn3(sets,regions={},title,{w=640,h=560}={}){const cx=w/2,cy=h/2-16,R=142,pos=[[cx,cy-72],[cx-82,cy+62],[cx+82,cy+62]];let s='';
  sets.forEach((st,i)=>{s+=`<circle cx="${pos[i][0]}" cy="${pos[i][1]}" r="${R}" fill="${st.color||P[i]}" opacity=".28"/>`;});
  const lp=[[cx,cy-198],[cx-208,cy+156],[cx+208,cy+156]];
  sets.forEach((st,i)=>{s+=ML(lp[i][0],lp[i][1],st.label,{fill:st.color||P[i],fs:14,fw:700});});
  const RT=(x,y,t)=>t?ML(x,y,t,{fill:C.ink,fs:10.5,fw:700,lh:11}):'';
  s+=RT(cx,cy-96,regions.a)+RT(cx-118,cy+96,regions.b)+RT(cx+118,cy+96,regions.c);
  s+=RT(cx-74,cy-2,regions.ab)+RT(cx+74,cy-2,regions.ca)+RT(cx,cy+98,regions.bc)+RT(cx,cy+18,regions.abc);
  if(title)s+=ML(cx,h-22,title,{fill:C.mut,fs:12,fw:700});
  return SV(s,w,h);}
function genMatrix(xLab,yLab,quads,{w=690,h=560}={}){const pad=76,gx=w-24,gy0=44,gy1=h-72,cw=(gx-pad)/2,ch=(gy1-gy0)/2,midX=pad+cw,midY=gy0+ch;let s='';
  const cells=[['tl',pad,gy0,C.a4],['tr',midX,gy0,C.a3],['bl',pad,midY,C.a2],['br',midX,midY,C.a5]];
  cells.forEach(([k,x,y,col])=>{const q=quads[k]||{};s+=`<rect x="${x}" y="${y}" width="${cw}" height="${ch}" fill="${col}" opacity=".12" stroke="#fff" stroke-width="2"/>`;
    s+=ML(x+12,y+22,q.title||'',{fill:col,fs:12,fw:700,anchor:'start'});
    (q.items||[]).forEach((it,i)=>{s+=T(x+12,y+44+i*15,'• '+it,{fill:C.ink,fs:10,anchor:'start'});});});
  s+=`<line x1="${pad}" y1="${gy0}" x2="${pad}" y2="${gy1}" stroke="${C.ink}" stroke-width="1.6"/>`;
  s+=`<line x1="${pad}" y1="${gy1}" x2="${gx}" y2="${gy1}" stroke="${C.ink}" stroke-width="1.6"/>`;
  s+=`<line x1="${pad}" y1="${midY}" x2="${gx}" y2="${midY}" stroke="${C.line}" stroke-width="1.2"/>`;
  s+=`<line x1="${midX}" y1="${gy0}" x2="${midX}" y2="${gy1}" stroke="${C.line}" stroke-width="1.2"/>`;
  s+=T((pad+gx)/2,gy1+32,xLab,{fill:C.mut,fs:12,fw:700});
  s+=T(pad-48,midY,yLab,{fill:C.mut,fs:12,fw:700,tr:`rotate(-90 ${pad-48} ${midY})`});
  return SV(s,w,h);}
function genRadar(axes,series,{w=620,h=560}={}){const cx=w/2,cy=h/2+6,R=Math.min(w,h)*0.30,n=axes.length;let s='';
  [0.25,0.5,0.75,1].forEach(f=>{let p=[];for(let i=0;i<n;i++){const a=-Math.PI/2+i*2*Math.PI/n;p.push(`${cx+Math.cos(a)*R*f},${cy+Math.sin(a)*R*f}`);}s+=`<polygon points="${p.join(' ')}" fill="none" stroke="${C.line}" stroke-width="1"/>`;});
  for(let i=0;i<n;i++){const a=-Math.PI/2+i*2*Math.PI/n,x=cx+Math.cos(a)*R,y=cy+Math.sin(a)*R;s+=`<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="${C.line}" stroke-width="1"/>`;
    const lx=cx+Math.cos(a)*(R+30),ly=cy+Math.sin(a)*(R+22);s+=ML(lx,ly+4,axes[i],{fill:C.mut,fs:10,fw:600});}
  series.forEach(se=>{let p=[];for(let i=0;i<n;i++){const a=-Math.PI/2+i*2*Math.PI/n;p.push(`${cx+Math.cos(a)*R*se.vals[i]},${cy+Math.sin(a)*R*se.vals[i]}`);}s+=`<polygon points="${p.join(' ')}" fill="${se.color}" opacity=".22" stroke="${se.color}" stroke-width="2.5"/>`;});
  series.forEach((se,k)=>{s+=`<rect x="26" y="${26+k*20}" width="12" height="12" rx="3" fill="${se.color}"/>`+T(44,36+k*20,se.name,{fill:C.ink,fs:11,anchor:'start'});});
  return SV(s,w,h);}
function genSpectrum(left,right,markers,{w=780,h=300,title=''}={}){const y=h/2,x0=64,x1=w-64;let s=`<defs><linearGradient id="spg" x1="0" x2="1"><stop offset="0" stop-color="${C.a2}"/><stop offset="1" stop-color="${C.a3}"/></linearGradient></defs>`;
  s+=`<rect x="${x0}" y="${y-9}" width="${x1-x0}" height="18" rx="9" fill="url(#spg)"/>`;
  s+=T(x0,y-26,left,{fill:C.ink,fs:13,fw:700,anchor:'start'})+T(x1,y-26,right,{fill:C.ink,fs:13,fw:700,anchor:'end'});
  markers.forEach((m,i)=>{const x=x0+(x1-x0)*m.pos,dir=i%2===0?1:-1;s+=`<circle cx="${x}" cy="${y}" r="8" fill="#fff" stroke="${m.color||C.a1}" stroke-width="2.5"/>`;
    s+=`<line x1="${x}" y1="${y+dir*10}" x2="${x}" y2="${y+dir*36}" stroke="${C.mut}" stroke-width="1"/>`+ML(x,y+dir*52,m.label,{fill:C.ink,fs:10,fw:600,lh:11});});
  if(title)s+=T(w/2,h-16,title,{fill:C.mut,fs:12,fw:700});
  return SV(s,w,h);}
function genTriad(corners,el={},center,{w=620,h=540}={}){const cx=w/2,top=74,bot=h-96,A=[cx,top],B=[w-96,bot],Cc=[96,bot],pts=[A,B,Cc];let s='';
  s+=`<polygon points="${A[0]},${A[1]} ${B[0]},${B[1]} ${Cc[0]},${Cc[1]}" fill="none" stroke="${C.line}" stroke-width="1.8"/>`;
  const mid=(p,q)=>[(p[0]+q[0])/2,(p[1]+q[1])/2];const eL=(p,q,t)=>{if(!t)return'';const m=mid(p,q);return `<rect x="${m[0]-t.length*3.3-5}" y="${m[1]-9}" width="${t.length*6.6+10}" height="17" rx="4" fill="#fff"/>`+T(m[0],m[1]+3,t,{fill:C.mut,fs:9.5});};
  s+=eL(A,B,el.ab)+eL(B,Cc,el.bc)+eL(Cc,A,el.ca);
  corners.forEach((c,i)=>{const p=pts[i];s+=`<circle cx="${p[0]}" cy="${p[1]}" r="48" fill="${c.color||P[i]}"/>`+ML(p[0],p[1]+4,c.label,{fill:'#fff',fs:12,fw:700});});
  if(center)s+=ML(cx,(top+bot)/2+70,center,{fill:C.ink,fs:12,fw:700,lh:13});
  return SV(s,w,h);}
function genConcentric(rings,{w=600,h=560,caption=''}={}){const cx=w/2,cy=h/2-8,n=rings.length,Rmax=Math.min(w,h)*0.35;let s='';
  rings.forEach((r,i)=>{const rad=Rmax*(n-i)/n,op=(0.2+0.62*(i/Math.max(1,n-1))).toFixed(2);s+=`<circle cx="${cx}" cy="${cy}" r="${rad}" fill="${r.color||C.a1}" opacity="${op}"/>`;});
  rings.forEach((r,i)=>{const rad=Rmax*(n-i)/n,y=i===n-1?cy:cy-rad+(Rmax/n)/2+8;s+=ML(cx,y+4,r.label,{fill:i>=n-2?'#fff':C.ink,fs:12,fw:700});});
  if(caption)s+=T(cx,h-22,caption,{fill:C.mut,fs:12,fw:700});
  return SV(s,w,h);}

function genHeadMap(){
  const ink=C.ink, mut=C.mut, line=C.line, acc=C.a4;
  const L=(x,y,anc,t,s)=>`<text x="${x}" y="${y}" text-anchor="${anc}" fill="${ink}" font-size="16.5" font-weight="700">${escT(t)}</text><text x="${x}" y="${y+18}" text-anchor="${anc}" fill="${mut}" font-size="12">${escT(s)}</text>`;
  return `<svg viewBox="0 0 900 560" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <path d="M 350 95 C 430 55, 530 70, 575 155 C 610 220, 605 300, 555 360 C 535 388, 535 420, 530 450 L 530 495 L 440 495 L 440 450 C 380 452, 330 430, 318 392 C 308 360, 300 300, 305 240 C 310 175, 300 130, 350 95 Z" fill="#fafafb" stroke="${line}" stroke-width="2"/>
  <ellipse cx="360" cy="330" rx="20" ry="30" fill="#fff" stroke="${line}" stroke-width="1.6"/>
  <path d="M 322 175 C 330 140, 365 112, 410 106 C 450 102, 480 104, 500 112" fill="none" stroke="${acc}" stroke-width="2.4" stroke-dasharray="5 4"/>
  <circle cx="525" cy="128" r="12" fill="none" stroke="${mut}" stroke-width="1.6"/><circle cx="525" cy="128" r="4" fill="${mut}"/>
  <circle cx="382" cy="110" r="3.6" fill="${ink}"/><path d="M 382 110 L 250 96 L 210 96" fill="none" stroke="${line}" stroke-width="1.4"/>${L(202,92,'end','Fringe / hairline','front edge + the bit that hangs')}
  <circle cx="326" cy="168" r="4.6" fill="${acc}"/><path d="M 326 168 L 235 205 L 205 205" fill="none" stroke="${acc}" stroke-width="1.8"/><text x="197" y="201" text-anchor="end" fill="${acc}" font-size="16.5" font-weight="800">Temples / corners</text><text x="197" y="219" text-anchor="end" fill="${mut}" font-size="12">where recession usually starts</text>
  <circle cx="330" cy="300" r="3.6" fill="${ink}"/><path d="M 330 300 L 235 345 L 205 345" fill="none" stroke="${line}" stroke-width="1.4"/>${L(197,341,'end','Sides / above the ear','taken short by a fade or taper')}
  <circle cx="455" cy="78" r="3.6" fill="${ink}"/><path d="M 455 78 L 700 70 L 735 70" fill="none" stroke="${line}" stroke-width="1.4"/>${L(742,62,'start','Top / mid-scalp','the main length you style')}
  <path d="M 537 128 L 700 175 L 735 175" fill="none" stroke="${line}" stroke-width="1.4"/>${L(742,168,'start','Crown','the swirl at the back-top')}
  <circle cx="570" cy="290" r="3.6" fill="${ink}"/><path d="M 570 290 L 700 300 L 735 300" fill="none" stroke="${line}" stroke-width="1.4"/>${L(742,293,'start','Back / occipital','rounded bone at the back')}
  <circle cx="500" cy="470" r="3.6" fill="${ink}"/><path d="M 500 470 L 700 460 L 735 460" fill="none" stroke="${line}" stroke-width="1.4"/>${L(742,453,'start','Nape / neckline','hairline at the back of the neck')}
  </svg>`;
}

/* ============ BODY ANALYSIS DIAGRAMS ============ */
function _bodyFront(f){ f=f||{}; const S="#c3cbd8", D="#e9ecf1"; const g=(k,d)=>f[k]||d;
  return `
  <ellipse cx="150" cy="46" rx="25" ry="29" fill="${g('head',D)}" stroke="${S}" stroke-width="1.4"/>
  <rect x="141" y="72" width="18" height="16" rx="6" fill="${g('neck',D)}" stroke="${S}" stroke-width="1"/>
  <ellipse cx="108" cy="106" rx="22" ry="15" fill="${g('delt',D)}" stroke="${S}" stroke-width="1.2"/>
  <ellipse cx="192" cy="106" rx="22" ry="15" fill="${g('delt',D)}" stroke="${S}" stroke-width="1.2"/>
  <path d="M116,100 Q150,92 184,100 L182,150 Q150,160 118,150 Z" fill="${g('chest',D)}" stroke="${S}" stroke-width="1.2"/>
  <path d="M120,150 Q150,158 180,150 L172,250 Q150,258 128,250 Z" fill="${g('abs',D)}" stroke="${S}" stroke-width="1.2"/>
  <rect x="84" y="112" width="20" height="92" rx="10" fill="${g('arm',D)}" stroke="${S}" stroke-width="1.2"/>
  <rect x="196" y="112" width="20" height="92" rx="10" fill="${g('arm',D)}" stroke="${S}" stroke-width="1.2"/>
  <rect x="82" y="200" width="17" height="86" rx="8" fill="${g('forearm',D)}" stroke="${S}" stroke-width="1.2"/>
  <rect x="201" y="200" width="17" height="86" rx="8" fill="${g('forearm',D)}" stroke="${S}" stroke-width="1.2"/>
  <path d="M126,248 Q150,256 174,248 L182,300 Q150,312 118,300 Z" fill="${g('pelvis',D)}" stroke="${S}" stroke-width="1.2"/>
  <rect x="120" y="300" width="27" height="112" rx="12" fill="${g('leg',D)}" stroke="${S}" stroke-width="1.2"/>
  <rect x="153" y="300" width="27" height="112" rx="12" fill="${g('leg',D)}" stroke="${S}" stroke-width="1.2"/>
  <rect x="122" y="410" width="24" height="96" rx="11" fill="${g('calf',D)}" stroke="${S}" stroke-width="1.2"/>
  <rect x="154" y="410" width="24" height="96" rx="11" fill="${g('calf',D)}" stroke="${S}" stroke-width="1.2"/>`;
}

function genBodyType(){
  const ink=C.ink,mut=C.mut;const x0=70,x1=470,y0=360,y1=54;
  const px=p=>x0+(x1-x0)*p, py=p=>y0-(y0-y1)*p;
  const you=[px(.46),py(.28)], goal=[px(.34),py(.82)];
  return `<svg viewBox="0 0 520 430" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <defs><marker id="mGoal" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6z" fill="${C.a5}"/></marker></defs>
  <rect x="${x0}" y="${y1}" width="${x1-x0}" height="${y0-y1}" fill="#fafbfc" stroke="${C.line}" stroke-width="1"/>
  <line x1="${(x0+x1)/2}" y1="${y1}" x2="${(x0+x1)/2}" y2="${y0}" stroke="${C.line}" stroke-width="1" stroke-dasharray="4 4"/>
  <line x1="${x0}" y1="${(y0+y1)/2}" x2="${x1}" y2="${(y0+y1)/2}" stroke="${C.line}" stroke-width="1" stroke-dasharray="4 4"/>
  <text x="${x0+92}" y="${y1+26}" text-anchor="middle" fill="${mut}" font-size="12" font-weight="600">Lean &amp; muscular</text>
  <text x="${x1-84}" y="${y1+26}" text-anchor="middle" fill="${mut}" font-size="12" font-weight="600">Big &amp; soft (bulk)</text>
  <text x="${x0+70}" y="${y0-14}" text-anchor="middle" fill="${mut}" font-size="12" font-weight="600">Skinny</text>
  <text x="${x1-84}" y="${y0-14}" text-anchor="middle" fill="${mut}" font-size="12" font-weight="600">Skinny-fat</text>
  <text x="260" y="404" text-anchor="middle" fill="${ink}" font-size="12" font-weight="700">Body fat  →</text>
  <text x="30" y="207" text-anchor="middle" fill="${ink}" font-size="12" font-weight="700" transform="rotate(-90 30 207)">Muscle mass  →</text>
  <line x1="${you[0]}" y1="${you[1]}" x2="${goal[0]}" y2="${goal[1]}" stroke="${C.a5}" stroke-width="2.4" stroke-dasharray="6 4" marker-end="url(#mGoal)"/>
  <circle cx="${you[0]}" cy="${you[1]}" r="9" fill="#fff" stroke="${C.a4}" stroke-width="3"/><text x="${you[0]+14}" y="${you[1]+5}" fill="${C.a4}" font-size="12.5" font-weight="800">You</text>
  <circle cx="${goal[0]}" cy="${goal[1]}" r="9" fill="${C.a5}"/><text x="${goal[0]+14}" y="${goal[1]+5}" fill="#0f7a3c" font-size="12.5" font-weight="800">Goal (recomp)</text>
  </svg>`;
}

function genFrame(){
  const ink=C.ink,mut=C.mut,acc=C.a1;
  return `<svg viewBox="0 0 340 320" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <g transform="translate(20,-8)">${_bodyFront({delt:'#dfe3ea'})}</g>
  <line x1="106" y1="98" x2="234" y2="98" stroke="${ink}" stroke-width="1.2"/><line x1="106" y1="92" x2="106" y2="104" stroke="${ink}" stroke-width="1.2"/><line x1="234" y1="92" x2="234" y2="104" stroke="${ink}" stroke-width="1.2"/>
  <text x="170" y="84" text-anchor="middle" fill="${ink}" font-size="11.5" font-weight="600">current shoulder width</text>
  <line x1="150" y1="240" x2="196" y2="240" stroke="${ink}" stroke-width="1.2"/><line x1="150" y1="234" x2="150" y2="246" stroke="${ink}" stroke-width="1.2"/><line x1="196" y1="234" x2="196" y2="246" stroke="${ink}" stroke-width="1.2"/>
  <text x="173" y="262" text-anchor="middle" fill="${ink}" font-size="11.5" font-weight="600">waist</text>
  <path d="M92,98 L150,240 M244,98 L196,240" fill="none" stroke="${mut}" stroke-width="1" stroke-dasharray="3 3" opacity=".6"/>
  <path d="M78,100 A70,70 0 0 1 262,100" fill="none" stroke="${acc}" stroke-width="2" stroke-dasharray="6 5"/>
  <text x="170" y="150" text-anchor="middle" fill="${acc}" font-size="11.5" font-weight="700">target: broaden shoulders</text>
  <text x="170" y="166" text-anchor="middle" fill="${mut}" font-size="10.5">wider delts shrink the waist by contrast</text>
  </svg>`;
}

function genMuscleMap(){
  const hi=C.a1, med="#9aa2ee", base="#dfe3ea", mut=C.mut, ink=C.ink;
  const parts={delt:hi, chest:med, arm:med, forearm:base, abs:med, leg:base, calf:base, pelvis:base, head:base, neck:base};
  return `<svg viewBox="0 0 470 540" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <g transform="translate(-10,10)">${_bodyFront(parts)}</g>
  <line x1="188" y1="116" x2="300" y2="96" stroke="${hi}" stroke-width="1"/><text x="304" y="93" fill="${hi}" font-size="12" font-weight="800">Shoulders — build first</text><text x="304" y="108" fill="${mut}" font-size="10.5">biggest payoff for your frame</text>
  <line x1="180" y1="130" x2="300" y2="150" stroke="${med}" stroke-width="1"/><text x="304" y="147" fill="#5b62c9" font-size="12" font-weight="700">Upper back &amp; chest</text><text x="304" y="162" fill="${mut}" font-size="10.5">the rest of the V-taper</text>
  <line x1="180" y1="210" x2="300" y2="212" stroke="${med}" stroke-width="1"/><text x="304" y="209" fill="#5b62c9" font-size="12" font-weight="700">Arms &amp; core</text><text x="304" y="224" fill="${mut}" font-size="10.5">grow alongside the big lifts</text>
  <line x1="180" y1="360" x2="300" y2="330" stroke="${mut}" stroke-width="1"/><text x="304" y="327" fill="${ink}" font-size="12" font-weight="700">Legs — decent base</text><text x="304" y="342" fill="${mut}" font-size="10.5">maintain, don't neglect</text>
  <rect x="20" y="512" width="13" height="13" rx="3" fill="${hi}"/><text x="38" y="522" fill="${mut}" font-size="11">Priority</text>
  <rect x="120" y="512" width="13" height="13" rx="3" fill="${med}"/><text x="138" y="522" fill="${mut}" font-size="11">Secondary</text>
  <rect x="235" y="512" width="13" height="13" rx="3" fill="${base}"/><text x="253" y="522" fill="${mut}" font-size="11">Base / maintain</text>
  </svg>`;
}

function genFatMap(){
  const mut=C.mut,ink=C.ink,fat=C.a4,lean=C.a5;
  const parts={arm:'#e2f0e8',forearm:'#e2f0e8',leg:'#e2f0e8',calf:'#e2f0e8',delt:'#e9ecf1',chest:'#e9ecf1'};
  return `<svg viewBox="0 0 530 540" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <g transform="translate(-6,10)">${_bodyFront(parts)}</g>
  <ellipse cx="144" cy="235" rx="34" ry="30" fill="${fat}" opacity=".38"/>
  <line x1="176" y1="232" x2="286" y2="215" stroke="${fat}" stroke-width="1"/><text x="290" y="212" fill="#a94e12" font-size="12" font-weight="800">Central fat</text><text x="290" y="227" fill="${mut}" font-size="10.5">lower belly, sits forward</text>
  <line x1="96" y1="250" x2="54" y2="292" stroke="${lean}" stroke-width="1"/><text x="10" y="308" text-anchor="start" fill="#0f7a3c" font-size="12" font-weight="700">Limbs lean</text>
  <text x="290" y="300" fill="${ink}" font-size="12" font-weight="700">Side view — the "push"</text>
  <path d="M340,270 C356,275 360,300 356,325 C368,332 372,352 360,366 C356,382 356,400 350,414" fill="none" stroke="${mut}" stroke-width="2"/>
  <path d="M356,325 C374,330 380,348 372,360" fill="${fat}" opacity=".3" stroke="none"/>
  <line x1="340" y1="262" x2="340" y2="420" stroke="${mut}" stroke-width="1" stroke-dasharray="4 4"/>
  <text x="384" y="352" fill="#a94e12" font-size="10.5">protrudes</text>
  <text x="290" y="450" fill="${mut}" font-size="10.5">Normal-weight central adiposity: the</text>
  <text x="290" y="465" fill="${mut}" font-size="10.5">most responsive fat type to fix.</text>
  </svg>`;
}

function genPosture(){
  const mut=C.mut,ink=C.ink,acc=C.a3,ok=C.a5;
  return `<svg viewBox="0 0 580 480" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <line x1="150" y1="30" x2="150" y2="450" stroke="${C.line}" stroke-width="1.4" stroke-dasharray="5 5"/>
  <text x="150" y="470" text-anchor="middle" fill="${mut}" font-size="10.5">ideal plumb line</text>
  <circle cx="176" cy="60" r="22" fill="#e9ecf1" stroke="#c3cbd8" stroke-width="1.4"/>
  <path d="M168,82 C150,120 150,150 156,175 C150,205 150,235 166,260 C150,285 150,320 150,360 L150,440" fill="none" stroke="${ink}" stroke-width="3"/>
  <path d="M168,175 C196,190 200,225 168,258" fill="${acc}" opacity=".18" stroke="none"/>
  <circle cx="176" cy="60" r="3" fill="${acc}"/><line x1="176" y1="60" x2="300" y2="60" stroke="${acc}" stroke-width="1"/><text x="304" y="57" fill="${acc}" font-size="12" font-weight="800">Forward head</text><text x="304" y="72" fill="${mut}" font-size="10.5">ear sits ahead of the line</text>
  <circle cx="156" cy="175" r="3" fill="${mut}"/><line x1="156" y1="175" x2="300" y2="150" stroke="${mut}" stroke-width="1"/><text x="304" y="147" fill="${ink}" font-size="12" font-weight="700">Rounded upper back</text>
  <circle cx="190" cy="222" r="3" fill="${acc}"/><line x1="190" y1="222" x2="300" y2="238" stroke="${acc}" stroke-width="1"/><text x="304" y="235" fill="${acc}" font-size="12" font-weight="800">Anterior pelvic tilt</text><text x="304" y="250" fill="${mut}" font-size="10.5">pelvis tips forward, low back arches</text>
  <line x1="190" y1="230" x2="300" y2="300" stroke="${acc}" stroke-width="1"/><text x="304" y="303" fill="#a94e12" font-size="12" font-weight="700">→ belly pushed forward</text><text x="304" y="318" fill="${mut}" font-size="10.5">exaggerates the stomach look</text>
  <text x="150" y="430" text-anchor="middle" fill="#0f7a3c" font-size="10.5">fixable with core + hip work</text>
  </svg>`;
}

function genRecomp(){
  const ink=C.ink,mut=C.mut,up=C.a5,down=C.a4,acc=C.a1;
  const chip=(x,y,w,t1,t2)=>`<rect x="${x}" y="${y}" width="${w}" height="52" rx="10" fill="#fff" stroke="${C.line}" stroke-width="1.3"/><text x="${x+14}" y="${y+22}" fill="${ink}" font-size="12.5" font-weight="700">${escT(t1)}</text><text x="${x+14}" y="${y+40}" fill="${mut}" font-size="11">${escT(t2)}</text>`;
  return `<svg viewBox="0 0 640 400" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <defs><marker id="mUp" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6z" fill="${up}"/></marker><marker id="mDn" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6z" fill="${down}"/></marker></defs>
  <rect x="30" y="40" width="150" height="70" rx="12" fill="#f6f7f9" stroke="${C.line}" stroke-width="1.3"/>
  <text x="105" y="70" text-anchor="middle" fill="${ink}" font-size="13" font-weight="800">Now</text>
  <text x="105" y="90" text-anchor="middle" fill="${mut}" font-size="11">low muscle + central fat</text>
  <rect x="460" y="40" width="150" height="70" rx="12" fill="#eef7f1" stroke="${up}" stroke-width="1.6"/>
  <text x="535" y="70" text-anchor="middle" fill="#0f7a3c" font-size="13" font-weight="800">Recomposition</text>
  <text x="535" y="90" text-anchor="middle" fill="${mut}" font-size="11">muscle ↑   central fat ↓</text>
  <line x1="182" y1="62" x2="456" y2="62" stroke="${up}" stroke-width="2.6" marker-end="url(#mUp)"/><text x="318" y="54" text-anchor="middle" fill="#0f7a3c" font-size="11" font-weight="700">build muscle</text>
  <line x1="182" y1="90" x2="456" y2="90" stroke="${down}" stroke-width="2.6" marker-end="url(#mDn)"/><text x="318" y="106" text-anchor="middle" fill="#a94e12" font-size="11" font-weight="700">shed central fat</text>
  <text x="320" y="160" text-anchor="middle" fill="${acc}" font-size="12.5" font-weight="800">The four levers</text>
  ${chip(30,180,290,"1 · Progressive resistance training","get stronger; bias shoulders, back, legs")}
  ${chip(330,180,280,"2 · Protein-forward eating","~1.6–2 g per kg bodyweight")}
  ${chip(30,246,290,"3 · Core + hip mobility","planks, dead-bugs; fix the pelvic tilt")}
  ${chip(330,246,280,"4 · Sleep · steps · stress","the multipliers for central fat")}
  <text x="320" y="330" text-anchor="middle" fill="${mut}" font-size="11.5">Not a diet — a redistribution. Don't crash-cut; you'd lose the muscle you have.</text>
  <text x="320" y="352" text-anchor="middle" fill="${mut}" font-size="10.5" font-style="italic">Guidance, not a medical or nutrition prescription.</text>
  </svg>`;
}

/* ============ EYEWEAR FRAME ANATOMY DIAGRAMS ============ */
function genFrameAnatomy(){
  const ink="#2a3340", lens="#eaf1fb", acc=C.a1, mut=C.mut, hw="#8a93a0";
  const lead=(x1,y1,x2,y2,c)=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c||acc}" stroke-width="1.1"/>`;
  const L=(x,y,t,c)=>`<text x="${x}" y="${y}" text-anchor="middle" fill="${c||acc}" font-size="13" font-weight="700">${escT(t)}</text>`;
  return `<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <rect x="170" y="140" width="150" height="110" rx="30" fill="${lens}" stroke="${ink}" stroke-width="6"/>
  <rect x="360" y="140" width="150" height="110" rx="30" fill="${lens}" stroke="${ink}" stroke-width="6"/>
  <path d="M320,158 Q340,144 360,158" fill="none" stroke="${ink}" stroke-width="6" stroke-linecap="round"/>
  <ellipse cx="330" cy="204" rx="4" ry="9" fill="#dfe6f2" stroke="${mut}" stroke-width="1"/>
  <ellipse cx="350" cy="204" rx="4" ry="9" fill="#dfe6f2" stroke="${mut}" stroke-width="1"/>
  <rect x="154" y="150" width="16" height="14" rx="3" fill="${ink}"/>
  <rect x="510" y="150" width="16" height="14" rx="3" fill="${ink}"/>
  <circle cx="530" cy="158" r="6" fill="${hw}" stroke="${ink}" stroke-width="1.4"/>
  <path d="M536,160 L720,178" fill="none" stroke="${ink}" stroke-width="6" stroke-linecap="round"/>
  <path d="M720,178 Q742,182 744,212" fill="none" stroke="${ink}" stroke-width="6" stroke-linecap="round"/>
  ${lead(340,150,340,74,ink)}${L(340,64,"Bridge",ink)}
  ${lead(230,196,200,98,ink)}${L(200,88,"Lens",ink)}
  ${lead(174,214,110,300,ink)}${L(100,316,"Rim / eyewire",ink)}
  ${lead(340,210,340,332)}${L(340,348,"Nose pads")}
  ${lead(516,152,560,88)}${L(580,80,"End piece")}
  ${lead(530,158,636,112)}${L(658,106,"Hinge")}
  ${lead(640,172,640,302)}${L(640,318,"Temple (arm)")}
  ${lead(742,212,742,322)}${L(742,338,"Temple tip")}
  </svg>`;
}

function genFrameMeasure(){
  const ink="#2a3340", lens="#eaf1fb", mut=C.mut;
  const hb=(x1,x2,y,t)=>`<line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}" stroke="${ink}" stroke-width="1.2"/><line x1="${x1}" y1="${y-5}" x2="${x1}" y2="${y+5}" stroke="${ink}" stroke-width="1.2"/><line x1="${x2}" y1="${y-5}" x2="${x2}" y2="${y+5}" stroke="${ink}" stroke-width="1.2"/><text x="${(x1+x2)/2}" y="${y+18}" text-anchor="middle" fill="${ink}" font-size="12" font-weight="600">${escT(t)}</text>`;
  return `<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <rect x="190" y="120" width="140" height="100" rx="26" fill="${lens}" stroke="${ink}" stroke-width="4"/>
  <rect x="350" y="120" width="140" height="100" rx="26" fill="${lens}" stroke="${ink}" stroke-width="4"/>
  <path d="M330,138 Q340,128 350,138" fill="none" stroke="${ink}" stroke-width="4"/>
  <path d="M490,140 L650,152" fill="none" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>
  <path d="M650,152 Q668,155 670,178" fill="none" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>
  ${hb(190,490,98,"total frame width")}
  ${hb(190,330,244,"lens width (52)")}
  <line x1="330" y1="150" x2="350" y2="150" stroke="${ink}" stroke-width="1.2"/><line x1="340" y1="150" x2="340" y2="272" stroke="${ink}" stroke-width="1" stroke-dasharray="3 3"/><text x="340" y="288" text-anchor="middle" fill="${ink}" font-size="12" font-weight="600">bridge (18)</text>
  ${hb(490,650,192,"temple length (145)")}
  <line x1="168" y1="120" x2="168" y2="220" stroke="${ink}" stroke-width="1.2"/><line x1="163" y1="120" x2="173" y2="120" stroke="${ink}" stroke-width="1.2"/><line x1="163" y1="220" x2="173" y2="220" stroke="${ink}" stroke-width="1.2"/><text x="150" y="172" text-anchor="middle" fill="${ink}" font-size="12" font-weight="600" transform="rotate(-90 150 172)">lens height</text>
  <text x="360" y="312" text-anchor="middle" fill="${ink}" font-size="22" font-weight="800">52  □  18  –  145</text>
  <text x="360" y="336" text-anchor="middle" fill="${mut}" font-size="11.5">the numbers printed inside the temple</text>
  </svg>`;
}

function _fLens(type,lx,cy){
  const ink="#2a3340", lens="#eaf1fb"; const S=`fill="${lens}" stroke="${ink}" stroke-width="2.5"`;
  switch(type){
    case "rectangle": return `<rect x="${lx-22}" y="${cy-15}" width="44" height="30" rx="6" ${S}/>`;
    case "square":    return `<rect x="${lx-19}" y="${cy-17}" width="38" height="34" rx="6" ${S}/>`;
    case "round":     return `<circle cx="${lx}" cy="${cy}" r="17" ${S}/>`;
    case "oval":      return `<ellipse cx="${lx}" cy="${cy}" rx="22" ry="14" ${S}/>`;
    case "panto":     return `<rect x="${lx-22}" y="${cy-16}" width="44" height="32" rx="14" ${S}/>`;
    case "aviator":   return `<path d="M${lx-22},${cy-8} Q${lx-22},${cy-15} ${lx-2},${cy-14} Q${lx+20},${cy-13} ${lx+22},${cy-6} Q${lx+20},${cy+12} ${lx+2},${cy+15} Q${lx-14},${cy+16} ${lx-22},${cy-8} Z" ${S}/>`;
    case "cateye":    return `<path d="M${lx-22},${cy+6} Q${lx-25},${cy-16} ${lx-3},${cy-13} Q${lx+18},${cy-12} ${lx+22},${cy-4} Q${lx+20},${cy+13} ${lx+2},${cy+15} Q${lx-16},${cy+15} ${lx-22},${cy+6} Z" ${S}/>`;
    case "geometric": return `<polygon points="${lx-22},${cy} ${lx-11},${cy-15} ${lx+11},${cy-15} ${lx+22},${cy} ${lx+11},${cy+15} ${lx-11},${cy+15}" ${S}/>`;
    case "wayfarer":  return `<path d="M${lx-22},${cy-13} L${lx+22},${cy-13} L${lx+16},${cy+14} L${lx-16},${cy+14} Z" ${S}/>`;
    case "browline":  return `<rect x="${lx-22}" y="${cy-13}" width="44" height="26" rx="6" fill="${lens}" stroke="${ink}" stroke-width="1.4"/><path d="M${lx-23},${cy-13} L${lx+23},${cy-13}" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`;
    default: return "";
  }
}
function genFrameShapes(){
  const ink="#2a3340", mut=C.mut;
  const cells=[["rectangle","Rectangle"],["round","Round"],["oval","Oval"],["aviator","Aviator"],["cateye","Cat-eye"],
               ["panto","Panto"],["browline","Browline"],["geometric","Geometric"],["wayfarer","Wayfarer"],["square","Square"]];
  const cx=[70,210,350,490,630]; let s="";
  cells.forEach((c,i)=>{ const col=i%5, row=Math.floor(i/5); const x=cx[col], y=row===0?86:216;
    s+=_fLens(c[0],x-30,y)+_fLens(c[0],x+30,y)
      +`<line x1="${x-8}" y1="${y-8}" x2="${x+8}" y2="${y-8}" stroke="${ink}" stroke-width="2.5"/>`
      +`<text x="${x}" y="${y+40}" text-anchor="middle" fill="${mut}" font-size="12" font-weight="600">${escT(c[1])}</text>`;
  });
  return `<svg viewBox="0 0 700 288" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">${s}</svg>`;
}

function genRimStyles(){
  const ink="#2a3340", lens="#eaf1fb", mut=C.mut, hw="#8a93a0";
  function pair(cx,cy,mode){ let g="";
    [-30,30].forEach(dx=>{ const lx=cx+dx;
      if(mode==="full"){ g+=`<rect x="${lx-26}" y="${cy-18}" width="52" height="36" rx="9" fill="${lens}" stroke="${ink}" stroke-width="4"/>`; }
      else if(mode==="semi"){ g+=`<rect x="${lx-26}" y="${cy-18}" width="52" height="36" rx="9" fill="${lens}" stroke="none"/>`
        +`<path d="M${lx-26},${cy-6} L${lx-26},${cy-18} L${lx+26},${cy-18} L${lx+26},${cy-6}" fill="none" stroke="${ink}" stroke-width="4" stroke-linejoin="round"/>`
        +`<path d="M${lx-26},${cy-6} Q${lx-26},${cy+18} ${lx},${cy+18} Q${lx+26},${cy+18} ${lx+26},${cy-6}" fill="none" stroke="${mut}" stroke-width="1.4" stroke-dasharray="3 3"/>`; }
      else { g+=`<rect x="${lx-26}" y="${cy-18}" width="52" height="36" rx="9" fill="#eef3fb" stroke="#c3cbd8" stroke-width="1.2" stroke-dasharray="3 3"/>`
        +`<circle cx="${lx+(dx<0?24:-24)}" cy="${cy}" r="2.4" fill="${hw}"/>`; }
    });
    g+=`<line x1="${cx-8}" y1="${cy-14}" x2="${cx+8}" y2="${cy-14}" stroke="${mode==='rimless'?hw:ink}" stroke-width="${mode==='rimless'?2:4}"/>`;
    return g;
  }
  const cx=[100,280,460], labels=["Full-rim","Semi-rimless","Rimless"], modes=["full","semi","rimless"];
  let s=""; cx.forEach((x,i)=>{ s+=pair(x,80,modes[i])+`<text x="${x}" y="150" text-anchor="middle" fill="${mut}" font-size="13" font-weight="700">${labels[i]}</text>`; });
  return `<svg viewBox="0 0 560 176" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">${s}</svg>`;
}

function genBridgeTypes(){
  const ink="#2a3340", mut=C.mut, lens="#eaf1fb";
  function unit(cx,cy,mode){
    let g=`<path d="M${cx-46},${cy-8} Q${cx-52},${cy+22} ${cx-40},${cy+30}" fill="none" stroke="${ink}" stroke-width="3"/>`
         +`<path d="M${cx+46},${cy-8} Q${cx+52},${cy+22} ${cx+40},${cy+30}" fill="none" stroke="${ink}" stroke-width="3"/>`;
    if(mode==="saddle"){ g+=`<path d="M${cx-24},${cy-2} Q${cx},${cy-22} ${cx+24},${cy-2}" fill="none" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`; }
    else if(mode==="keyhole"){ g+=`<path d="M${cx-24},${cy-2} Q${cx-14},${cy-20} ${cx-5},${cy-9} Q${cx},${cy-2} ${cx+5},${cy-9} Q${cx+14},${cy-20} ${cx+24},${cy-2}" fill="none" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`; }
    else { g+=`<path d="M${cx-24},${cy-2} Q${cx},${cy-16} ${cx+24},${cy-2}" fill="none" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`
      +`<line x1="${cx-26}" y1="${cy-22}" x2="${cx+26}" y2="${cy-22}" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`; }
    return g;
  }
  const cx=[100,280,460], labels=["Saddle","Keyhole","Double / top bar"], modes=["saddle","keyhole","double"];
  let s=""; cx.forEach((x,i)=>{ s+=unit(x,70,modes[i])+`<text x="${x}" y="150" text-anchor="middle" fill="${mut}" font-size="13" font-weight="700">${escT(labels[i])}</text>`; });
  return `<svg viewBox="0 0 560 172" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">${s}</svg>`;
}

function genTempleStyles(){
  const ink="#2a3340", mut=C.mut, hw="#8a93a0", ear="#d6dce6";
  function unit(cx,cy,mode){
    let g=`<path d="M${cx+40},${cy+28} a14,16 0 1 0 0.1,0" fill="none" stroke="${ear}" stroke-width="3"/>`
         +`<circle cx="${cx-72}" cy="${cy}" r="5" fill="${hw}" stroke="${ink}" stroke-width="1.2"/>`;
    if(mode==="skull"){ g+=`<path d="M${cx-66},${cy} L${cx+38},${cy} Q${cx+64},${cy} ${cx+66},${cy+40}" fill="none" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`; }
    else if(mode==="library"){ g+=`<path d="M${cx-66},${cy} L${cx+66},${cy}" fill="none" stroke="${ink}" stroke-width="5" stroke-linecap="round"/><line x1="${cx+66}" y1="${cy-7}" x2="${cx+66}" y2="${cy+7}" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`; }
    else { g+=`<path d="M${cx-66},${cy} L${cx+30},${cy} Q${cx+58},${cy} ${cx+56},${cy+34} Q${cx+54},${cy+56} ${cx+38},${cy+48}" fill="none" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>`; }
    return g;
  }
  const cx=[130,330,520], labels=["Skull","Library / paddle","Cable"], modes=["skull","library","cable"];
  let s=""; cx.forEach((x,i)=>{ s+=unit(x,64,modes[i])+`<text x="${x}" y="150" text-anchor="middle" fill="${mut}" font-size="13" font-weight="700">${escT(labels[i])}</text>`; });
  return `<svg viewBox="0 0 640 176" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">${s}</svg>`;
}

/* ============ FACE -> FRAME MAPPING DIAGRAMS ============ */
function genFrameRules(){
  const ink=C.ink, mut=C.mut;
  const cards=[["Contrast the shape","frame opposes the face's lines",C.a1],
               ["Harmonise the colour","frame agrees with your undertone",C.a4],
               ["Match the scale","size & thickness to the features",C.a5],
               ["Jewellery for the eyes","top rim on the brow, eyes centred",C.a6]];
  let s=""; cards.forEach((c,i)=>{ const x=12+i*177;
    s+=`<rect x="${x}" y="14" width="165" height="118" rx="12" fill="#fff" stroke="${C.line}" stroke-width="1.3"/>`
      +`<circle cx="${x+22}" cy="42" r="8" fill="${c[2]}"/><text x="${x+38}" y="47" fill="${ink}" font-size="13.5" font-weight="800">${i+1}</text>`
      +ML(x+82,74,c[0],{fill:ink,fs:13,fw:700,lh:15})
      +ML(x+82,104,c[1],{fill:mut,fs:11,lh:13});
  });
  return `<svg viewBox="0 0 720 150" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">${s}</svg>`;
}

function genFaceFrameMap(){
  const ink=C.ink, mut=C.mut, acc=C.a1, warm=C.a4;
  const rows=[["Face shape","Frame shape — the opposite"],
              ["Length : width","Lens height + horizontal line"],
              ["Feature scale","Frame size + thickness"],
              ["Cheekbone width","Max frame width (fit ceiling)"],
              ["Brow line","Top-rim height"],
              ["Nose length","Bridge height / keyhole"],
              ["Eye spacing","Bridge width"],
              ["Deep-set eyes","Lens depth + lighter rim"],
              ["Colouring","Frame colour + how bold"]];
  let s=`<text x="150" y="28" text-anchor="middle" fill="${warm}" font-size="12" font-weight="800" letter-spacing="1.5">THE FACE</text>`
       +`<text x="590" y="28" text-anchor="middle" fill="${acc}" font-size="12" font-weight="800" letter-spacing="1.5">THE FRAME</text>`
       +`<defs><marker id="mMap" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6z" fill="${acc}"/></marker></defs>`;
  rows.forEach((r,i)=>{ const y=42+i*54, mid=y+21;
    s+=`<rect x="24" y="${y}" width="252" height="42" rx="10" fill="#f6efe4" stroke="#e0cba9" stroke-width="1.3"/>`
      +`<text x="150" y="${mid+5}" text-anchor="middle" fill="${ink}" font-size="13" font-weight="700">${escT(r[0])}</text>`
      +`<line x1="280" y1="${mid}" x2="460" y2="${mid}" stroke="${acc}" stroke-width="2" marker-end="url(#mMap)"/>`
      +`<rect x="464" y="${y}" width="252" height="42" rx="10" fill="#eef0fb" stroke="#c7cef2" stroke-width="1.3"/>`
      +`<text x="590" y="${mid+5}" text-anchor="middle" fill="${ink}" font-size="13" font-weight="700">${escT(r[1])}</text>`;
  });
  return `<svg viewBox="0 0 740 ${42+rows.length*54+16}" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">${s}</svg>`;
}

function _faceIcon(type,cx,cy){
  const S=`fill="#f6efe4" stroke="#c9a86f" stroke-width="2.2"`;
  switch(type){
    case "round":  return `<circle cx="${cx}" cy="${cy}" r="26" ${S}/>`;
    case "oblong": return `<rect x="${cx-20}" y="${cy-30}" width="40" height="60" rx="18" ${S}/>`;
    case "square": return `<rect x="${cx-25}" y="${cy-25}" width="50" height="50" rx="10" ${S}/>`;
    case "heart":  return `<path d="M${cx-26},${cy-22} Q${cx},${cy-30} ${cx+26},${cy-22} Q${cx+18},${cy+6} ${cx},${cy+30} Q${cx-18},${cy+6} ${cx-26},${cy-22} Z" ${S}/>`;
    default: return "";
  }
}
function genShapeContrast(){
  const ink=C.ink, mut=C.mut, acc=C.a1;
  const cells=[["round","rectangle","Round → angular"],
               ["oblong","wayfarer","Long → wide + deep"],
               ["square","round","Square → round"],
               ["heart","oval","Heart → light / oval"]];
  const cx=[175,495], cy=[92,232]; let s="";
  cells.forEach((c,i)=>{ const x=cx[i%2], y=cy[Math.floor(i/2)];
    s+=_faceIcon(c[0],x-78,y-8)
      +`<line x1="${x-44}" y1="${y-8}" x2="${x-6}" y2="${y-8}" stroke="${acc}" stroke-width="2" marker-end="url(#mSC)"/>`
      +_fLens(c[1],x+26,y-8)+_fLens(c[1],x+74,y-8)
      +`<line x1="${x+44}" y1="${y-16}" x2="${x+56}" y2="${y-16}" stroke="#2a3340" stroke-width="2"/>`
      +`<text x="${x}" y="${y+44}" text-anchor="middle" fill="${mut}" font-size="12.5" font-weight="700">${escT(c[2])}</text>`;
  });
  return `<svg viewBox="0 0 660 300" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial"><defs><marker id="mSC" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6z" fill="${acc}"/></marker></defs>${s}</svg>`;
}

function genFrameColourMap(){
  const ink=C.ink, mut=C.mut;
  const warm=[["Tortoise","#8a5a2b"],["Warm brown","#6f4a2e"],["Honey","#c8912f"],["Olive","#6b6a34"],["Gunmetal","#4a4f57"],["Warm navy","#2b3a55"]];
  const cool=[["Black","#1a1a1a"],["Silver","#b8bcc4"],["Blue","#2f4f8f"],["Blue-grey","#566173"],["Charcoal","#333a42"]];
  function row(list,y){ let g=""; list.forEach((c,i)=>{ const x=140+i*82;
    g+=`<rect x="${x}" y="${y}" width="68" height="34" rx="7" fill="${c[1]}"/><text x="${x+34}" y="${y+50}" text-anchor="middle" fill="${mut}" font-size="10">${escT(c[0])}</text>`; }); return g; }
  return `<svg viewBox="0 0 660 250" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <rect x="16" y="42" width="640" height="60" rx="10" fill="#f4fbf6" stroke="${C.a5}" stroke-width="1.6"/>
  <text x="26" y="34" fill="#0f7a3c" font-size="12.5" font-weight="800">Warm / olive undertone — you ✓</text>
  ${row(warm,50)}
  <text x="26" y="150" fill="${ink}" font-size="12.5" font-weight="800">Cool undertone</text>
  ${row(cool,158)}
  <text x="26" y="228" fill="${mut}" font-size="11">Depth of colouring → how dark you can go.  Personal contrast (hair vs skin) → how bold.</text>
  </svg>`;
}

function genDecisionOrder(){
  const ink=C.ink, mut=C.mut, acc=C.a1;
  const steps=[["1","Fit",C.a4],["2","Shape",acc],["3","Scale",acc],["4","Position",acc],["5","Colour",acc],["6","Statement",C.a6]];
  let s=`<defs><marker id="mDO" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6z" fill="${mut}"/></marker></defs>`;
  steps.forEach((st,i)=>{ const x=12+i*120;
    s+=`<rect x="${x}" y="40" width="104" height="46" rx="10" fill="${i===0?'#fdf1e7':'#eef0fb'}" stroke="${st[2]}" stroke-width="1.6"/>`
      +`<circle cx="${x+20}" cy="63" r="11" fill="${st[2]}"/><text x="${x+20}" y="67" text-anchor="middle" fill="#fff" font-size="12" font-weight="800">${st[0]}</text>`
      +`<text x="${x+64}" y="67" text-anchor="middle" fill="${ink}" font-size="12.5" font-weight="700">${escT(st[1])}</text>`;
    if(i<steps.length-1) s+=`<line x1="${x+104}" y1="63" x2="${x+120}" y2="63" stroke="${mut}" stroke-width="1.6" marker-end="url(#mDO)"/>`;
  });
  s+=`<text x="370" y="112" text-anchor="middle" fill="${mut}" font-size="11.5">Fit is non-negotiable and comes first; the statement is the last 10%.</text>`;
  return `<svg viewBox="0 0 740 132" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">${s}</svg>`;
}

/* ============ DETAILED CROSS-DOMAIN EXAMPLES ============ */

/* ============ FACE ANALYSIS DIAGRAMS ============ */
const FACE_FRONT="M150,32 C198,32 218,62 218,112 C218,156 202,200 176,234 C166,254 158,266 150,274 C142,266 134,254 124,234 C98,200 82,156 82,112 C82,62 102,32 150,32 Z";

function genFaceShape(){
  const ink=C.ink,mut=C.mut,acc=C.a1;
  return `<svg viewBox="0 0 300 340" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <rect x="82" y="30" width="136" height="252" rx="4" fill="none" stroke="#c3cbd8" stroke-width="1.4" stroke-dasharray="5 5"/>
  <path d="${FACE_FRONT}" fill="#f7f8fa" stroke="${mut}" stroke-width="2"/>
  <line x1="82" y1="122" x2="218" y2="122" stroke="${acc}" stroke-width="1" stroke-dasharray="4 4" opacity=".5"/>
  <line x1="82" y1="196" x2="218" y2="196" stroke="${acc}" stroke-width="1" stroke-dasharray="4 4" opacity=".5"/>
  <text x="150" y="82" text-anchor="middle" fill="${mut}" font-size="11">forehead — broad &amp; tall</text>
  <text x="150" y="162" text-anchor="middle" fill="${mut}" font-size="11">midface — parallel sides</text>
  <text x="150" y="242" text-anchor="middle" fill="${mut}" font-size="11">lower — soft taper to chin</text>
  <line x1="82" y1="302" x2="218" y2="302" stroke="${ink}" stroke-width="1.2"/>
  <line x1="82" y1="296" x2="82" y2="308" stroke="${ink}" stroke-width="1.2"/>
  <line x1="218" y1="296" x2="218" y2="308" stroke="${ink}" stroke-width="1.2"/>
  <text x="150" y="322" text-anchor="middle" fill="${ink}" font-size="11.5" font-weight="600">width</text>
  <line x1="64" y1="32" x2="64" y2="282" stroke="${ink}" stroke-width="1.2"/>
  <line x1="58" y1="32" x2="70" y2="32" stroke="${ink}" stroke-width="1.2"/>
  <line x1="58" y1="282" x2="70" y2="282" stroke="${ink}" stroke-width="1.2"/>
  <text x="30" y="160" text-anchor="middle" fill="${ink}" font-size="11.5" font-weight="600" transform="rotate(-90 30 160)">length &gt; width</text>
  </svg>`;
}

function genFaceFeatures(){
  const ink=C.ink,mut=C.mut,acc=C.a1;
  const lab=(x,y,t)=>`<text x="${x}" y="${y}" text-anchor="start" fill="${acc}" font-size="11" font-weight="600">${escT(t)}</text>`;
  const lead=(x1,y1,x2,y2)=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${acc}" stroke-width="1"/>`;
  return `<svg viewBox="0 0 400 340" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <path d="${FACE_FRONT}" fill="#f7f8fa" stroke="#c3cbd8" stroke-width="1.6"/>
  <path d="M108,116 q16,-8 34,-2" fill="none" stroke="#3a3128" stroke-width="4" stroke-linecap="round"/>
  <path d="M158,114 q16,-6 34,2" fill="none" stroke="#3a3128" stroke-width="4" stroke-linecap="round"/>
  <path d="M110,132 q15,-9 30,0 q-15,9 -30,0 Z" fill="#fff" stroke="${mut}" stroke-width="1.2"/><circle cx="125" cy="132" r="4.6" fill="#4a3726"/>
  <path d="M160,132 q15,-9 30,0 q-15,9 -30,0 Z" fill="#fff" stroke="${mut}" stroke-width="1.2"/><circle cx="175" cy="132" r="4.6" fill="#4a3726"/>
  <path d="M112,142 q13,6 26,1" fill="none" stroke="#9a7d86" stroke-width="2.4" stroke-linecap="round" opacity=".8"/>
  <path d="M162,143 q13,5 26,0" fill="none" stroke="#9a7d86" stroke-width="2.4" stroke-linecap="round" opacity=".8"/>
  <path d="M150,138 L150,178 q-9,6 -16,3 M150,178 q9,6 16,3" fill="none" stroke="#b79a78" stroke-width="2"/>
  <path d="M131,203 q19,-9 38,0 q-19,13 -38,0 Z" fill="#b07766" stroke="#8a5648" stroke-width="1"/><line x1="131" y1="203" x2="169" y2="203" stroke="#8a5648" stroke-width="1"/>
  <ellipse cx="104" cy="150" rx="12" ry="20" fill="${acc}" opacity=".12" transform="rotate(12 104 150)"/>
  <line x1="150" y1="60" x2="150" y2="44" stroke="${acc}" stroke-width="1"/><text x="150" y="36" text-anchor="middle" fill="${acc}" font-size="11" font-weight="600">broad, tall forehead</text>
  ${lead(196,116,250,104)}${lab(254,107,'heavy, straight brow')}
  ${lead(190,132,250,130)}${lab(254,133,'deep-set, hooded eyes')}
  ${lead(188,144,250,158)}<text x="254" y="161" text-anchor="start" fill="#9a7d86" font-size="11" font-weight="600">under-eye shadow</text>
  ${lead(196,152,250,186)}${lab(254,189,'cheekbones read')}
  ${lead(164,175,250,210)}${lab(254,213,'long, straight nose')}
  ${lead(169,205,250,236)}${lab(254,239,'balanced lips')}
  <line x1="104" y1="116" x2="66" y2="106" stroke="${acc}" stroke-width="1"/><text x="62" y="104" text-anchor="end" fill="${acc}" font-size="11" font-weight="600">hairline</text>
  <line x1="150" y1="266" x2="150" y2="296" stroke="${acc}" stroke-width="1"/><text x="150" y="312" text-anchor="middle" fill="${acc}" font-size="11" font-weight="600">narrow, defined chin</text>
  </svg>`;
}

function genTzone(){
  const ink=C.ink,mut=C.mut,oil=C.a4,cheek=C.a5;
  return `<svg viewBox="0 0 300 360" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <path d="${FACE_FRONT}" fill="#f7f8fa" stroke="#c3cbd8" stroke-width="1.6"/>
  <ellipse cx="112" cy="168" rx="26" ry="34" fill="${cheek}" opacity=".16"/>
  <ellipse cx="188" cy="168" rx="26" ry="34" fill="${cheek}" opacity=".16"/>
  <rect x="98" y="52" width="104" height="34" rx="10" fill="${oil}" opacity=".28"/>
  <rect x="136" y="80" width="28" height="120" rx="12" fill="${oil}" opacity=".28"/>
  <ellipse cx="150" cy="238" rx="26" ry="18" fill="${oil}" opacity=".28"/>
  <circle cx="150" cy="66" r="3" fill="#e0a94f"/><circle cx="150" cy="150" r="3" fill="#e0a94f"/><circle cx="150" cy="238" r="3" fill="#e0a94f"/>
  <rect x="40" y="324" width="13" height="13" rx="3" fill="${oil}" opacity=".55"/><text x="58" y="334" fill="${mut}" font-size="11.5">Oiliest — forehead, nose, chin (the "T")</text>
  <rect x="40" y="342" width="13" height="13" rx="3" fill="${cheek}" opacity=".4"/><text x="58" y="352" fill="${mut}" font-size="11.5">Cheeks — some shine, less</text>
  </svg>`;
}

function genSkinMap(){
  const ink=C.ink,mut=C.mut,dark="#7d5566",pih="#8a5a3c",act=C.a3,tex=C.a4;
  return `<svg viewBox="0 0 300 372" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <path d="${FACE_FRONT}" fill="#f7f8fa" stroke="#c3cbd8" stroke-width="1.6"/>
  <path d="M110,140 q15,9 30,2" fill="none" stroke="${dark}" stroke-width="5" stroke-linecap="round" opacity=".55"/>
  <path d="M160,141 q15,8 30,1" fill="none" stroke="${dark}" stroke-width="5" stroke-linecap="round" opacity=".55"/>
  <circle cx="104" cy="176" r="4" fill="${pih}" opacity=".7"/><circle cx="116" cy="192" r="3.4" fill="${pih}" opacity=".7"/><circle cx="120" cy="210" r="3" fill="${pih}" opacity=".7"/>
  <circle cx="196" cy="180" r="4" fill="${pih}" opacity=".7"/><circle cx="188" cy="198" r="3.2" fill="${pih}" opacity=".7"/><circle cx="182" cy="214" r="3" fill="${pih}" opacity=".7"/>
  <circle cx="128" cy="200" r="3.6" fill="${act}"/><circle cx="176" cy="188" r="3.2" fill="${act}"/>
  <ellipse cx="110" cy="188" rx="20" ry="24" fill="none" stroke="${tex}" stroke-width="1" stroke-dasharray="3 3" opacity=".6"/>
  <ellipse cx="190" cy="190" rx="20" ry="24" fill="none" stroke="${tex}" stroke-width="1" stroke-dasharray="3 3" opacity=".6"/>
  <circle cx="46" cy="330" r="6" fill="${dark}" opacity=".6"/><text x="58" y="334" fill="${mut}" font-size="11.5">Under-eye darkness</text>
  <circle cx="46" cy="350" r="6" fill="${pih}" opacity=".7"/><text x="58" y="354" fill="${mut}" font-size="11.5">Post-acne marks (fade)</text>
  <circle cx="190" cy="330" r="6" fill="${act}"/><text x="202" y="334" fill="${mut}" font-size="11.5">Active breakout</text>
  <circle cx="190" cy="350" r="6" fill="none" stroke="${tex}" stroke-width="1.5" stroke-dasharray="3 2"/><text x="202" y="354" fill="${mut}" font-size="11.5">Texture / pores</text>
  </svg>`;
}

function genProfile(){
  const ink=C.ink,mut=C.mut,acc=C.a1,hi=C.a5;
  return `<svg viewBox="0 0 400 340" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <path d="M118,44 C150,34 196,46 202,98 C205,114 200,122 197,130 C210,140 214,152 224,168 C218,174 210,176 202,178 C206,186 206,192 200,198 C205,204 204,212 196,218 C205,226 210,234 200,246 C182,260 156,268 132,264 C110,260 96,248 92,226 C88,202 86,152 92,112 C96,78 100,56 118,44 Z" fill="#f7f8fa" stroke="${mut}" stroke-width="1.8"/>
  <ellipse cx="150" cy="150" rx="26" ry="14" fill="${hi}" opacity=".2" transform="rotate(-12 150 150)"/>
  <line x1="150" y1="140" x2="150" y2="96" stroke="${hi}" stroke-width="1"/><text x="150" y="90" text-anchor="middle" fill="#0f7a3c" font-size="11" font-weight="600">cheekbone reads</text>
  <path d="M104,234 q2,20 28,30" fill="none" stroke="${acc}" stroke-width="1.6"/>
  <line x1="118" y1="266" x2="118" y2="300" stroke="${acc}" stroke-width="1"/><text x="118" y="316" text-anchor="middle" fill="${acc}" font-size="11" font-weight="600">clean jaw angle</text>
  <line x1="168" y1="156" x2="196" y2="240" stroke="${mut}" stroke-width="1.2" stroke-dasharray="4 3"/><path d="M196,240 l-7,-3 l3,7 Z" fill="${mut}"/>
  <text x="214" y="208" text-anchor="start" fill="${mut}" font-size="11">lean taper</text>
  <line x1="222" y1="158" x2="270" y2="150" stroke="${mut}" stroke-width="1"/><text x="274" y="147" text-anchor="start" fill="${mut}" font-size="11">nose: slight,</text><text x="274" y="160" text-anchor="start" fill="${mut}" font-size="11">characterful bump</text>
  </svg>`;
}

function genColoring(){
  const ink=C.ink,mut=C.mut,hi=C.a5;
  return `<svg viewBox="0 0 320 220" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <defs><linearGradient id="tone-fa" x1="0" x2="1"><stop offset="0" stop-color="#f2d7bb"/><stop offset="0.5" stop-color="#c79a6f"/><stop offset="1" stop-color="#6f4a2e"/></linearGradient></defs>
  <text x="26" y="34" fill="${ink}" font-size="11.5" font-weight="600">Depth of tone</text>
  <rect x="26" y="44" width="268" height="20" rx="6" fill="url(#tone-fa)"/>
  <polygon points="204,40 198,30 210,30" fill="${ink}"/><text x="204" y="24" text-anchor="middle" fill="${ink}" font-size="10.5">you — medium-deep</text>
  <text x="26" y="104" fill="${ink}" font-size="11.5" font-weight="600">Undertone</text>
  <rect x="26" y="114" width="58" height="40" rx="8" fill="#c9a3a0"/><text x="55" y="170" text-anchor="middle" fill="${mut}" font-size="10">cool</text>
  <rect x="92" y="114" width="58" height="40" rx="8" fill="#c7ac8f"/><text x="121" y="170" text-anchor="middle" fill="${mut}" font-size="10">neutral</text>
  <rect x="158" y="114" width="58" height="40" rx="8" fill="#c69a5e" stroke="${hi}" stroke-width="2.5"/><text x="187" y="170" text-anchor="middle" fill="#0f7a3c" font-size="10" font-weight="700">warm ✓</text>
  <rect x="224" y="114" width="58" height="40" rx="8" fill="#a7935e" stroke="${hi}" stroke-width="2.5"/><text x="253" y="170" text-anchor="middle" fill="#0f7a3c" font-size="10" font-weight="700">olive ✓</text>
  <text x="26" y="198" fill="${mut}" font-size="10.5">Flatters: olive, rust, cream, tan, forest, warm navy.</text>
  <text x="26" y="213" fill="${mut}" font-size="10.5">Trickier: icy pastels, cool greys next to the face.</text>
  </svg>`;
}

function genFaceGauge(){
  const ink=C.ink,mut=C.mut,warm=C.a4,open=C.a5;
  return `<svg viewBox="0 0 640 240" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,Arial">
  <path d="M60,180 A110,110 0 0 1 180,71" fill="none" stroke="${warm}" stroke-width="16" stroke-linecap="round"/>
  <path d="M180,71 A110,110 0 0 1 300,180" fill="none" stroke="${open}" stroke-width="16" stroke-linecap="round"/>
  <line x1="180" y1="180" x2="108" y2="120" stroke="${ink}" stroke-width="3.5" stroke-linecap="round"/><circle cx="180" cy="180" r="7" fill="${ink}"/>
  <text x="60" y="205" text-anchor="middle" fill="${warm}" font-size="11" font-weight="700">Reserved · intense</text>
  <text x="300" y="205" text-anchor="middle" fill="#0f7a3c" font-size="11" font-weight="700">Warm · open</text>
  <text x="180" y="52" text-anchor="middle" fill="${mut}" font-size="11">resting default →</text>
  <text x="360" y="58" fill="${ink}" font-size="11.5" font-weight="600">What pushes it "intense":</text>
  <rect x="360" y="70" width="150" height="12" rx="6" fill="#eef0f4"/><rect x="360" y="70" width="128" height="12" rx="6" fill="${warm}"/><text x="360" y="98" fill="${mut}" font-size="10.5">heavy straight brow</text>
  <rect x="360" y="108" width="150" height="12" rx="6" fill="#eef0f4"/><rect x="360" y="108" width="116" height="12" rx="6" fill="${warm}"/><text x="360" y="136" fill="${mut}" font-size="10.5">deep-set / hooded eyes</text>
  <rect x="360" y="146" width="150" height="12" rx="6" fill="#eef0f4"/><rect x="360" y="146" width="140" height="12" rx="6" fill="${warm}"/><text x="360" y="174" fill="${mut}" font-size="10.5">neutral, unsmiling mouth</text>
  <text x="360" y="205" fill="#0f7a3c" font-size="10.5">Engage the eyes / a half-smile → swings it right, fast.</text>
  </svg>`;
}
