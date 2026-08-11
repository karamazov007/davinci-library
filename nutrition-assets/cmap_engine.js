var NCM=(function(){
 function mix(h,t){var a=[parseInt(h.slice(1,3),16),parseInt(h.slice(3,5),16),parseInt(h.slice(5,7),16)];
   return "rgb("+Math.round(a[0]+(255-a[0])*t)+","+Math.round(a[1]+(255-a[1])*t)+","+Math.round(a[2]+(255-a[2])*t)+")";}
 function esc(s){return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
 function hasChildren(id,D){return D.nodes.some(function(m){return m.parent===id;});}
 function nodeSVG(n,D){
   var x=n.x,y=n.y,R=n.r,col=n.color,i,ls,ty,g='';
   if(n.child){
     g+='<g class="ncm-node ncm-child" data-parent="'+n.parent+'" style="opacity:0;pointer-events:none">';
     g+='<circle cx="'+x+'" cy="'+y+'" r="'+(R+6)+'" fill="none" stroke="'+mix(col,0.6)+'" stroke-width="4"/>';
     g+='<circle cx="'+x+'" cy="'+y+'" r="'+(R+2)+'" fill="#f7f8fa"/>';
     g+='<circle cx="'+x+'" cy="'+y+'" r="'+R+'" fill="'+mix(col,0.16)+'"/>';
     ls=n.title.split("\n");ty=y-(ls.length-1)*9+4;
     for(i=0;i<ls.length;i++) g+='<text x="'+x+'" y="'+(ty+i*17)+'" text-anchor="middle" fill="#fff" font-size="13" font-weight="700">'+esc(ls[i])+'</text>';
     return g+'</g>';
   }
   g+='<g class="ncm-node" data-id="'+n.id+'">';
   g+='<circle cx="'+x+'" cy="'+y+'" r="'+(R+9)+'" fill="none" stroke="'+mix(col,0.55)+'" stroke-width="5"/>';
   g+='<circle cx="'+x+'" cy="'+y+'" r="'+(R+4)+'" fill="#f7f8fa"/>';
   g+='<circle cx="'+x+'" cy="'+y+'" r="'+R+'" fill="'+col+'"/>';
   ls=n.title.split("\n");var nl=ls.length;ty=y-(n.sub?10:4)-(nl-1)*9;
   for(i=0;i<nl;i++) g+='<text x="'+x+'" y="'+(ty+i*18)+'" text-anchor="middle" fill="#fff" font-size="16" font-weight="700">'+esc(ls[i])+'</text>';
   if(n.sub) g+='<text x="'+x+'" y="'+(ty+nl*18+2)+'" text-anchor="middle" fill="'+mix(col,0.78)+'" font-size="12" font-style="italic">'+esc(n.sub)+'</text>';
   if(hasChildren(n.id,D)){var bx=x+R*0.72,by=y-R*0.72;
     g+='<g class="ncm-badge" data-exp="'+n.id+'" style="cursor:pointer">';
     g+='<circle cx="'+bx+'" cy="'+by+'" r="13" fill="#fff" stroke="'+mix(col,0.35)+'"/>';
     g+='<text class="ncm-sign" data-sign="'+n.id+'" x="'+bx+'" y="'+(by+5)+'" text-anchor="middle" fill="'+col+'" font-size="17" font-weight="700">+</text></g>';}
   return g+'</g>';
 }
 function edgeSVG(e,byId){
   var A=byId[e.a],B=byId[e.b];if(!A||!B)return'';
   var x1=A.x,y1=A.y,x2=B.x,y2=B.y,dx=x2-x1,dy=y2-y1,d=Math.hypot(dx,dy)||1,ux=dx/d,uy=dy/d;
   var sx=x1+ux*(A.r+9),sy=y1+uy*(A.r+9),ex=x2-ux*(B.r+16),ey=y2-uy*(B.r+16);
   var mx=(sx+ex)/2,my=(sy+ey)/2,px=-uy,py=ux,off=e.curve*d,cx=mx+px*off,cy=my+py*off;
   var col=e.color||A.color,dash=e.dash?(' stroke-dasharray="'+e.dash+'"'):'',w=e.parent?2.0:2.6;
   var s='<g class="ncm-edge'+(e.parent?' ncm-cedge':'')+'"'+(e.parent?(' data-parent="'+e.parent+'"'):'')+(e.parent?' style="opacity:0"':'')+'>';
   s+='<path d="M'+sx.toFixed(1)+','+sy.toFixed(1)+' Q'+cx.toFixed(1)+','+cy.toFixed(1)+' '+ex.toFixed(1)+','+ey.toFixed(1)+'" fill="none" stroke="'+col+'" stroke-width="'+w+'"'+dash+' marker-end="url(#ncmtip)" opacity="0.9"/>';
   if(e.label){var lx=0.25*sx+0.5*cx+0.25*ex,ly=0.25*sy+0.5*cy+0.25*ey,wd=e.label.length*6.6+18;
     s+='<rect x="'+(lx-wd/2).toFixed(1)+'" y="'+(ly-12).toFixed(1)+'" width="'+wd.toFixed(1)+'" height="23" rx="6" fill="#fff" stroke="#e3e5ea"/>';
     s+='<text x="'+lx.toFixed(1)+'" y="'+(ly+4).toFixed(1)+'" text-anchor="middle" fill="#5b6270" font-size="12.5">'+esc(e.label)+'</text>';}
   return s+'</g>';
 }
 function buildOne(root,D){
   var byId={};D.nodes.forEach(function(n){byId[n.id]=n;});
   var W=D.W,H=D.H;
   root.innerHTML='<div class="ncm-stage"><svg class="ncm-svg"><defs>'
     +'<pattern id="ncmdots" width="30" height="30" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="#e6e8ee"/></pattern>'
     +'<marker id="ncmtip" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1.5 1.5L8 5L1.5 8.5" fill="none" stroke="context-stroke" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>'
     +'<rect x="-8000" y="-8000" width="20000" height="20000" fill="#f7f8fa"/>'
     +'<rect x="-8000" y="-8000" width="20000" height="20000" fill="url(#ncmdots)"/>'
     +'<g class="ncm-vp">'+D.edges.map(function(e){return edgeSVG(e,byId);}).join('')+D.nodes.map(function(n){return nodeSVG(n,D);}).join('')+'</g></svg>'
     +'<div class="ncm-toolbar"><span class="ncm-zlabel">zoom</span><input class="ncm-slider" type="range" min="20" max="220" value="70"></div>'
     +'<div class="ncm-hint">drag to pan &middot; scroll to zoom &middot; click + to expand a node</div></div>';
   var svg=root.querySelector('.ncm-svg'),vp=root.querySelector('.ncm-vp'),slider=root.querySelector('.ncm-slider');
   var st={k:0.7,tx:0,ty:0},expanded={};
   function apply(){vp.setAttribute('transform','translate('+st.tx+','+st.ty+') scale('+st.k+')');slider.value=Math.round(st.k*100);}
   function rect(){return svg.getBoundingClientRect();}
   function fit(){var r=rect();if(!r.width)return;var k=Math.min(r.width/W,r.height/H)*0.94;st.k=k;st.tx=(r.width-W*k)/2;st.ty=(r.height-H*k)/2;apply();}
   function zoomAt(cx,cy,nk){nk=Math.max(0.2,Math.min(2.4,nk));var r=rect();var px=cx-r.left,py=cy-r.top;st.tx=px-(px-st.tx)*(nk/st.k);st.ty=py-(py-st.ty)*(nk/st.k);st.k=nk;apply();}
   svg.addEventListener('wheel',function(ev){ev.preventDefault();zoomAt(ev.clientX,ev.clientY,st.k*(ev.deltaY<0?1.12:0.893));},{passive:false});
   var pan=null;
   svg.addEventListener('pointerdown',function(ev){if(ev.target.closest('.ncm-badge'))return;pan={x:ev.clientX,y:ev.clientY,tx:st.tx,ty:st.ty};try{svg.setPointerCapture(ev.pointerId);}catch(e){}svg.classList.add('grab');});
   svg.addEventListener('pointermove',function(ev){if(!pan)return;st.tx=pan.tx+(ev.clientX-pan.x);st.ty=pan.ty+(ev.clientY-pan.y);apply();});
   function endPan(){if(pan){pan=null;svg.classList.remove('grab');}}
   svg.addEventListener('pointerup',endPan);svg.addEventListener('pointercancel',endPan);
   root.addEventListener('click',function(ev){
     var b=ev.target.closest('.ncm-badge');if(!b)return;var id=b.getAttribute('data-exp');expanded[id]=!expanded[id];
     vp.querySelectorAll('[data-parent="'+id+'"]').forEach(function(el){el.style.opacity=expanded[id]?'1':'0';if(el.classList.contains('ncm-child'))el.style.pointerEvents=expanded[id]?'auto':'none';});
     var sg=vp.querySelector('.ncm-sign[data-sign="'+id+'"]');if(sg)sg.textContent=expanded[id]?'–':'+';
   });
   slider.addEventListener('input',function(){var r=rect();zoomAt(r.left+r.width/2,r.top+r.height/2,(slider.value||70)/100);});
   var ro=window.ResizeObserver?new ResizeObserver(function(){fit();}):null;if(ro)ro.observe(svg);
   setTimeout(fit,40);setTimeout(fit,220);
 }
 function setTop(){var h=document.querySelector('.htabs')||document.querySelector('header');
   var t=h?Math.max(0,Math.round(h.getBoundingClientRect().bottom)):56;
   document.documentElement.style.setProperty('--ncm-top',t+'px');}
 function mountAll(){
   var old=document.querySelectorAll('body > .ncm-overlay');[].forEach.call(old,function(e){e.remove();});
   document.body.classList.remove('cmap-active');
   var ph=document.querySelector('#stage .ncm-root[data-cmap]');
   if(!ph)return;
   var key=ph.getAttribute('data-cmap');var D=(typeof NCM_MAPS!=='undefined')?NCM_MAPS[key]:null;
   if(!D)return;
   ph.style.display='none';
   var root=document.createElement('div');root.className='ncm-root ncm-bleed ncm-overlay';
   document.body.appendChild(root);document.body.classList.add('cmap-active');setTop();buildOne(root,D);
 }
 window.addEventListener('resize',setTop);
 return {mountAll:mountAll};
})();
