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
function genTree(root,{w=720,h=440,pad=44,boxW=104,boxH=40}={}){let leaves=[];const levels=[];
  (function walk(n,d){n._d=d;levels[d]=1;if(!n.children||!n.children.length)leaves.push(n);else n.children.forEach(c=>walk(c,d+1));})(root,0);
  const maxD=levels.length-1,xGap=(w-2*pad)/Math.max(1,leaves.length-1);
  leaves.forEach((lf,i)=>lf._x=leaves.length===1?w/2:pad+i*xGap);
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

/* ============ DETAILED CROSS-DOMAIN EXAMPLES ============ */
