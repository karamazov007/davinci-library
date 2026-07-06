#!/usr/bin/env python3
import base64, json, os, html as ihtml

BASE = "/sessions/eloquent-awesome-knuth/mnt/Claude/Projects"
OUT = "/sessions/eloquent-awesome-knuth/mnt/outputs/knowledge-hub.html"
OUT_INDEX = "/sessions/eloquent-awesome-knuth/mnt/outputs/index.html"
NCR_TAXO = json.load(open("/sessions/eloquent-awesome-knuth/mnt/outputs/ncr_taxo.json", encoding="utf-8"))

# (id, relpath, display name, icon, blurb)
TOP_PAGES = [
    ("mvp",      "Building Personality/minimum-viable-personality.html",        "Minimum Viable Personality", "🧬", "The smallest set of traits that let you step into the world feeling ready — not finished, just enough to begin."),
    ("social",   "Social mastery/Social_Mastery.html",                          "Social Mastery",             "🤝", "First principles of human connection: how to be warm, capable, and genuinely understood."),
    ("brain",    "Understanding Human Brain/Brain as a System.html",            "Brain as a System",          "🧠", "A first-principles operating manual for your own mind — from neurons to identity."),
    ("media",    "Media Consumption/media-hub.html",                            "Media Hub",                  "🎬", "Everything you've watched, read, and wrestled with — gathered into one living catalogue."),
    ("systems",  "Systems Thinking & Mental Models/systems-thinking-and-tools.html", "Systems Thinking & Tools", "🕸️", "Mental models and thinking tools for seeing clearly and deciding well."),
    ("swimming", "Swimming/swimming-home.html",                                 "Swimming Home",              "🏊", "A capability stack for mastering the water — and, through it, your own body."),
    ("cards",    "Card Games/card_games.html",                                  "Card Games",                 "🃏", "A living playbook for the games worth learning to win."),
]

# Cornerstone pages, starred and featured on the homepage
FEATURED = {"mvp", "social", "swimming"}

# (relpath, family)  -- only the "brain" family navigates page-to-page, so only it uses last-chapter memory
SUB_FILES = [
    ("Media Consumption/media-atlas.html",                                   "media"),
    ("Media Consumption/media-consumption.html",                             "media"),
    ("Systems Thinking & Mental Models/complete-thinking-tools-toolkit.html","systems"),
    ("Systems Thinking & Mental Models/mental-models-by-party.html",         "systems"),
    ("Systems Thinking & Mental Models/parrish-mental-models.html",          "systems"),
    ("Systems Thinking & Mental Models/thinking-tools-toolkit-original.html","systems"),
    ("Understanding Human Brain/1-components.html",                          "brain"),
    ("Understanding Human Brain/2-interactions.html",                        "brain"),
    ("Understanding Human Brain/3-behaviors.html",                           "brain"),
    ("Understanding Human Brain/4-minds.html",                              "brain"),
    ("Understanding Human Brain/5-faculties.html",                           "brain"),
    ("Understanding Human Brain/6-identity.html",                            "brain"),
    ("Understanding Human Brain/references.html",                            "brain"),
]

FIREBASE_CONFIG = {
    "apiKey": "AIzaSyAFjMHjFtyummI29D2f_vsvOAnU4t-YuuA",
    "authDomain": "knowledge-hub-4d232.firebaseapp.com",
    "projectId": "knowledge-hub-4d232",
    "storageBucket": "knowledge-hub-4d232.firebasestorage.app",
    "messagingSenderId": "120009453713",
    "appId": "1:120009453713:web:88254a60e109b0abf14f30",
}

# ---- injected into EVERY embedded page: link/iframe rewiring + last-chapter memory + deep-state saver ----
INJECT_TEMPLATE = r"""<script>
(function(){try{
var PID=__PID__, FAMILY=__FAMILY__, ENTRY=__ENTRY__;
var TOP=null; try{TOP=window.top;}catch(e){}
function base(n){ n=decodeURIComponent(String(n).split('#')[0].split('?')[0]); return n.substring(n.lastIndexOf('/')+1); }
/* local fallback: pages that carry their own sub-pages (media/systems/brain) resolve them
   here when window.top is blocked — i.e. when the whole file is opened locally (file://). */
var __LB={};
function __localBlob(bn){ if(__LB[bn])return __LB[bn]; var LA; try{LA=window.__DVH_LOCAL__;}catch(e){} if(!LA||!LA[bn])return null;
  try{ var raw=atob(LA[bn]); var bytes=new Uint8Array(raw.length); for(var i=0;i<raw.length;i++)bytes[i]=raw.charCodeAt(i);
    var boot='<scr'+'ipt>window.__DVH_LOCAL__='+JSON.stringify(LA)+';<\/scr'+'ipt>';
    var u=URL.createObjectURL(new Blob([boot,bytes],{type:'text/html'})); __LB[bn]=u; return u;
  }catch(e){ return null; } }
function R(name){ var bn=base(name); try{ if(TOP&&TOP.__HUB_RESOLVE__){ var u=TOP.__HUB_RESOLVE__(bn); if(u) return u; } }catch(e){} return __localBlob(bn); }
function isLocalHtml(h){ return h && /\.html($|[#?])/i.test(h) && !/^(https?:|data:|blob:|mailto:|\/\/)/i.test(h); }

/* ---- last-chapter memory (brain family only) ---- */
if(FAMILY){ var SUBKEY='khub.sub.'+FAMILY;
  try{
    if(ENTRY){ var last=localStorage.getItem(SUBKEY);
      if(last && last!==PID){ var b=R(last); if(b){ location.replace(b); return; } }
      else { localStorage.setItem(SUBKEY, PID); }
    } else { localStorage.setItem(SUBKEY, PID); }
  }catch(e){}
}

/* ---- rewrite iframe src/data-src and intercept <a> clicks to embedded pages ---- */
function fixFrames(){ try{ Array.prototype.forEach.call(document.querySelectorAll('iframe'),function(f){ ['src','data-src'].forEach(function(a){ var v=f.getAttribute(a); if(v&&isLocalHtml(v)){ var u=R(v); if(u&&v!==u) f.setAttribute(a,u);} }); }); }catch(e){} }
document.addEventListener('click',function(e){ try{ var a=e.target.closest?e.target.closest('a[href]'):null; if(!a)return; var h=a.getAttribute('href'); if(!isLocalHtml(h))return; var u=R(h); if(!u)return; e.preventDefault(); if(FAMILY){try{localStorage.setItem('khub.sub.'+FAMILY, base(h));}catch(_){}} location.href=u; }catch(_){} },true);
if(document.readyState!=='loading') fixFrames(); else document.addEventListener('DOMContentLoaded',fixFrames);
try{ new MutationObserver(fixFrames).observe(document.documentElement,{childList:true,subtree:true,attributes:true,attributeFilter:['src','data-src']}); }catch(e){}

/* ---- deep-state saver: remembers tabs / sections / scroll within this page ---- */
var KEY='khub.deep.'+PID, RESTORING=false, scrolledEls=[], timer=null;
function cssPath(el){if(!el||el.nodeType!==1)return null;var parts=[];while(el&&el.nodeType===1){if(el===document.body){parts.unshift('body');break;}var tag=el.tagName.toLowerCase();var par=el.parentNode;if(!par){parts.unshift(tag);break;}var sibs=Array.prototype.filter.call(par.children,function(c){return c.tagName===el.tagName;});parts.unshift(tag+':nth-of-type('+(sibs.indexOf(el)+1)+')');el=par;}return parts.join('>');}
function cls(el){var c=el.className;if(c&&c.baseVal!==undefined)c=c.baseVal;return ' '+(c||'')+' ';}
function isActive(el){if(!el)return false;if(el.getAttribute&&el.getAttribute('aria-selected')==='true')return true;var c=cls(el);return c.indexOf(' active ')>=0||c.indexOf(' is-active ')>=0||c.indexOf(' selected ')>=0;}
var REPLAY_SEL='button,[role=tab],[data-tab],[onclick],.tab,li';
function capture(){if(RESTORING)return;try{var st={h:location.hash,sx:window.pageXOffset,sy:window.pageYOffset,inputs:[],tabs:[],scrolls:[]};document.querySelectorAll('input[type=radio],input[type=checkbox]').forEach(function(el){st.inputs.push(!!el.checked);});var seen={};document.querySelectorAll(REPLAY_SEL).forEach(function(el){if(isActive(el)){var p=cssPath(el);if(p&&!seen[p]){seen[p]=1;st.tabs.push(p);}}});scrolledEls.forEach(function(el){if(el===document.body||el===document.documentElement||!el.isConnected)return;if(el.scrollTop>0||el.scrollLeft>0){var p=cssPath(el);if(p)st.scrolls.push({p:p,t:el.scrollTop,l:el.scrollLeft});}});localStorage.setItem(KEY,JSON.stringify(st));}catch(e){}}
function schedule(){clearTimeout(timer);timer=setTimeout(capture,350);}
document.addEventListener('scroll',function(e){var t=e.target;if(t&&t.nodeType===1&&scrolledEls.indexOf(t)<0)scrolledEls.push(t);schedule();},true);
window.addEventListener('scroll',schedule,{passive:true});
document.addEventListener('click',function(){setTimeout(capture,80);},true);
document.addEventListener('change',function(){setTimeout(capture,40);},true);
window.addEventListener('hashchange',schedule);
window.addEventListener('pagehide',capture);window.addEventListener('beforeunload',capture);
function restore(){var st;try{st=JSON.parse(localStorage.getItem(KEY)||'null');}catch(e){return;}if(!st)return;RESTORING=true;try{
var ins=document.querySelectorAll('input[type=radio],input[type=checkbox]');if(st.inputs&&st.inputs.length===ins.length){ins.forEach(function(el,i){if(el.checked!==st.inputs[i]){el.checked=st.inputs[i];try{el.dispatchEvent(new Event('change',{bubbles:true}));}catch(_){}}});}
if(st.h){try{location.hash=st.h;}catch(_){}}
function passTabs(){(st.tabs||[]).forEach(function(p){var el=null;try{el=document.querySelector(p);}catch(_){}if(el&&!isActive(el)){try{el.click();}catch(_){}}});}
passTabs();setTimeout(passTabs,140);setTimeout(passTabs,400);
function passScroll(){try{window.scrollTo(st.sx||0,st.sy||0);}catch(_){}(st.scrolls||[]).forEach(function(s){var el=null;try{el=document.querySelector(s.p);}catch(_){}if(el){el.scrollTop=s.t;el.scrollLeft=s.l;}});}
[90,300,650,1100,1600].forEach(function(d){setTimeout(passScroll,d);});
}catch(e){}setTimeout(function(){RESTORING=false;},1800);}
if(document.readyState!=='loading')setTimeout(restore,50);else document.addEventListener('DOMContentLoaded',function(){setTimeout(restore,50);});
window.addEventListener('load',function(){setTimeout(restore,150);});
}catch(e){}})();
</script>"""

def insert_before_body(html, snip):
    low = html.lower()
    i = low.rfind('</body>')
    if i == -1: i = low.rfind('</html>')
    return (html + snip) if i == -1 else (html[:i] + snip + html[i:])

def inject(raw_bytes, pid, family, entry, local=None):
    html = raw_bytes.decode('utf-8', 'ignore')
    snip = (INJECT_TEMPLATE
            .replace('__PID__', json.dumps(pid))
            .replace('__FAMILY__', json.dumps(family) if family else 'null')
            .replace('__ENTRY__', 'true' if entry else 'false'))
    if local:
        snip = '<script>window.__DVH_LOCAL__=' + json.dumps(local) + ';</script>' + snip
    return insert_before_body(html, snip)

# ---- page-specific "skins": recolor to the soft cool palette + beautify ----
MVP_SKIN = r"""<style>
/* Da Vinci — soft cool palette for Minimum Viable Personality */
:root{ --bg:#f6f7f9; --surface:#ffffff; --surface2:#ffffff; --line:#e7e9ee;
  --accent-soft:#eef0f4; --amber-bg:#eef2f7; --primary-soft:#e9f1ee; }
/* Prettier home landing (content untouched, just restyled) */
#view-home .hero{max-width:820px;margin:0 auto;text-align:center;padding:48px 20px 6px}
#view-home .kicker{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);font-weight:700}
#view-home h1{font-size:clamp(34px,5vw,52px);line-height:1.05;letter-spacing:-.02em;margin:14px 0 0;background:linear-gradient(120deg,var(--primary-ink),var(--accent));-webkit-background-clip:text;background-clip:text;color:transparent}
#view-home .lead{font-size:18.5px;line-height:1.6;color:var(--muted);max-width:660px;margin:18px auto 0}
#view-home .purpose{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:940px;margin:40px auto 0}
#view-home .purpose .block{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:22px 24px;box-shadow:var(--shadow)}
#view-home .purpose .block h3{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:12.5px;text-transform:uppercase;letter-spacing:.09em;color:var(--accent);margin:0 0 8px}
#view-home .purpose .block.accent{grid-column:1/-1;background:linear-gradient(160deg,var(--primary-soft),var(--surface) 78%);border-color:var(--primary)}
#view-home .purpose .block.accent h3{color:var(--primary-ink)}
#view-home .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;max-width:940px;margin:36px auto 60px}
#view-home .tile{position:relative;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:20px;box-shadow:var(--shadow);transition:transform .15s,border-color .15s,box-shadow .15s;cursor:pointer;display:block}
#view-home .tile:hover{transform:translateY(-4px);border-color:var(--primary);box-shadow:0 12px 30px rgba(40,60,50,.12)}
#view-home .tile .t-icon{font-size:26px;margin-bottom:10px;line-height:1}
#view-home .tile .t-name{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:17px;font-weight:750;color:var(--ink)}
#view-home .tile .t-desc{font-size:14px;color:var(--muted);margin-top:6px;line-height:1.5}
#view-home .tile .t-flag{display:inline-block;margin-top:12px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:11px;font-weight:700;padding:4px 9px;border-radius:999px;letter-spacing:.02em}
@media(max-width:720px){#view-home .purpose{grid-template-columns:1fr}}
</style>
<script>
document.addEventListener('DOMContentLoaded',function(){try{
 var m={grooming:'🧴',fashion:'👔',photos:'📸',communities:'👥',physique:'💪',communication:'💬',culture:'🎭',interests:'✨',work:'🛠️'};
 document.querySelectorAll('#view-home .tile').forEach(function(t){var c=t.getAttribute('data-cat');if(m[c]&&!t.querySelector('.t-icon')){var s=document.createElement('div');s.className='t-icon';s.textContent=m[c];t.insertBefore(s,t.firstChild);}});
}catch(e){}});
</script>"""

MEDIA_ATLAS_SKIN = r"""<style>
/* Da Vinci — Media Atlas: match the Media Consumption palette, drop the hero, clean top-tab bar */
:root{
  --bg:#fbfbfa; --bg-tint:#f4f4f3; --surface:#ffffff;
  --ink:#1d1d1f; --ink-soft:#6b6b70; --faint:#9a9aa0;
  --line:#ececec; --line-soft:#f4f4f3;
  --accent:#1a1a1a; --accent-soft:#e0e0e0; --accent-bg:#f4f4f3;
  --gold:#caa24a; --slate:#6b6b70;
}
/* remove the big "The Atlas" hero entirely */
header.masthead{display:none !important;}
/* make the category nav the clean top-tab bar */
nav.pillars{
  background:#ffffff !important; -webkit-backdrop-filter:none !important; backdrop-filter:none !important;
  border-top:0 !important; border-bottom:1px solid var(--line) !important;
  box-shadow:0 1px 10px rgba(20,20,25,.04); padding:8px 12px !important; justify-content:center;
}
nav.pillars button.pillar.active{color:var(--accent) !important;}
nav.pillars button.pillar.active::after{background:var(--accent) !important;}
</style>"""

EXTRA_SKIN = {
    "minimum-viable-personality.html": MVP_SKIN,
    "media-atlas.html": MEDIA_ATLAS_SKIN,
}

# ---- per-section "home / why this exists" intro overlay ----
def _esc(s): return ihtml.escape(str(s), quote=True)

HOME_CSS = r"""<style>
.dvh-panel{position:fixed;left:0;right:0;bottom:0;top:0;z-index:9998;overflow:auto;display:none;background:radial-gradient(1100px 520px at 15% -10%,rgba(79,70,229,.10),transparent 60%),radial-gradient(900px 480px at 100% 0%,rgba(124,108,255,.10),transparent 55%),#f7f8fb;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif;color:#1c2431;-webkit-font-smoothing:antialiased;text-align:left}
.dvh-panel.show{display:block}
.dvh-tab{display:inline-flex;align-items:center;cursor:pointer;padding:0 16px;font:inherit;color:inherit;text-decoration:none;opacity:.82;white-space:nowrap;align-self:stretch}
.dvh-tab:hover{opacity:1}
.dvh-tab.active{opacity:1;font-weight:800}
.dvh-wrap{max-width:940px;margin:0 auto;padding:40px 32px 92px}
.dvh-kick{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#4f46e5;font-weight:700}
.dvh-h1{font-size:clamp(32px,5vw,50px);line-height:1.06;letter-spacing:-.02em;margin:12px 0 0;font-weight:800;background:linear-gradient(120deg,#1c2431,#4f46e5);-webkit-background-clip:text;background-clip:text;color:transparent}
.dvh-tag{font-size:18px;color:#5b6472;max-width:660px;margin:16px 0 0;line-height:1.6}
.dvh-lbl{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#4f46e5;margin:42px 0 12px;display:flex;align-items:center;gap:10px}
.dvh-lbl::after{content:"";flex:1;height:1px;background:#e6e8ef}
.dvh-p{font-size:16px;line-height:1.75;color:#2b3444;max-width:700px;margin:12px 0}
.dvh-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px;margin:6px 0 0}
.dvh-card{background:#fff;border:1px solid #e6e8ef;border-radius:15px;padding:18px;box-shadow:0 1px 2px rgba(20,25,40,.05),0 8px 22px rgba(20,25,40,.05)}
.dvh-card .i{font-size:23px;line-height:1}
.dvh-card h4{margin:10px 0 4px;font-size:15.5px;font-weight:750;color:#1c2431}
.dvh-card p{margin:0;font-size:13.5px;line-height:1.5;color:#5b6472}
.dvh-res{display:flex;flex-direction:column;gap:10px;margin:6px 0 0}
.dvh-res a{display:flex;align-items:center;gap:13px;text-decoration:none;background:#fff;border:1px solid #e6e8ef;border-radius:13px;padding:14px 16px;color:#1c2431;transition:border-color .15s,transform .15s}
.dvh-res a:hover{border-color:#4f46e5;transform:translateX(3px)}
.dvh-res .badge{font-size:10px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#4f46e5;background:#eef0fb;border-radius:999px;padding:5px 10px;flex:0 0 auto}
.dvh-res .rt{font-weight:650;font-size:14.5px}
.dvh-res .rn{color:#5b6472;font-size:13px}
.dvh-res .arr{margin-left:auto;color:#9aa0ac}
</style>"""

PAGE_NAV = {
  "Social_Mastery.html": {"tabbar":"header nav","brand":".brand"},
  "systems-thinking-and-tools.html": {"tabbar":"nav.tabs","brand":".brand"},
  "media-hub.html": {"tabbar":".tabs","brand":".brand"},
}

def build_home(pid, d):
    nav = PAGE_NAV.get(pid, {"tabbar":"body","brand":".brand"})
    whys = "".join('<p class="dvh-p">%s</p>' % _esc(p) for p in d["why"])
    aspects = "".join('<div class="dvh-card"><div class="i">%s</div><h4>%s</h4><p>%s</p></div>' % (a[0], _esc(a[1]), _esc(a[2])) for a in d["aspects"])
    res = "".join('<a href="%s" target="_blank" rel="noopener"><span class="badge">%s</span><span><span class="rt">%s</span><br><span class="rn">%s</span></span><span class="arr">↗</span></a>' % (_esc(r["url"]), _esc(r["type"]), _esc(r["label"]), _esc(r["note"])) for r in d["resources"])
    panel = ('<div class="dvh-panel" id="dvh-panel"><div class="dvh-wrap">'
          '<div class="dvh-kick">%s</div><h1 class="dvh-h1">%s</h1><p class="dvh-tag">%s</p>'
          '<div class="dvh-lbl">Why this exists</div>%s'
          '<div class="dvh-lbl">What\'s inside</div><div class="dvh-grid">%s</div>'
          '<div class="dvh-lbl">Go deeper</div><div class="dvh-res">%s</div>'
          '</div></div>') % (_esc(d["kicker"]), _esc(d["title"]), _esc(d["tagline"]), whys, aspects, res)
    script = ('<script>(function(){function init(){try{'
              'var K="khub.introseen."+' + json.dumps(pid) + ';'
              'var TB=document.querySelector(' + json.dumps(nav["tabbar"]) + '); if(!TB){return;}'
              'var panel=document.getElementById("dvh-panel"); if(!panel){return;}'
              'var ht=document.createElement("a"); ht.className="dvh-tab"; ht.textContent="Home"; ht.setAttribute("role","tab"); ht.setAttribute("data-dvh-home","1");'
              'function ensure(){ if(!TB.contains(ht)) TB.insertBefore(ht, TB.firstChild); }'
              'function pos(){ var r=TB.getBoundingClientRect(); panel.style.top=r.bottom+"px"; }'
              'function show(){ ensure(); pos(); panel.classList.add("show"); ht.classList.add("active"); }'
              'function hide(){ panel.classList.remove("show"); ht.classList.remove("active"); }'
              'ensure();'
              'ht.addEventListener("click",function(e){ e.preventDefault(); e.stopPropagation(); show(); });'
              'TB.addEventListener("click",function(e){ if(e.target===ht||ht.contains(e.target))return; hide(); }, true);'
              'var brand=document.querySelector(' + json.dumps(nav["brand"]) + '); if(brand){ brand.style.cursor="pointer"; brand.addEventListener("click",function(){ show(); }); }'
              'window.addEventListener("resize",function(){ if(panel.classList.contains("show")) pos(); });'
              'try{ new MutationObserver(function(){ ensure(); }).observe(TB,{childList:true}); }catch(e){}'
              'var seen=false; try{seen=!!localStorage.getItem(K);}catch(e){}'
              'if(!seen){ show(); try{localStorage.setItem(K,"1");}catch(e){} }'
              '}catch(e){}}'
              'if(document.readyState!=="loading") setTimeout(init,60); else document.addEventListener("DOMContentLoaded",function(){setTimeout(init,60);});'
              '})();</script>')
    return HOME_CSS + panel + script

HOME_PANELS = {
  "Social_Mastery.html": {
    "kicker":"Section · Social Mastery","title":"Why Social Mastery","enter":"Explore Social Mastery",
    "tagline":"Connection isn't a fixed trait you're born with — it's a skill you can study, practice, and get measurably better at.",
    "why":[
      "Almost everything good in a life — friendships, love, opportunities, simply being understood — flows through other people. Yet most of us are never actually taught how connection works. We're left to guess.",
      "This section treats human connection as a craft with first principles. Warmth (do you mean me well?) and competence (can you act?) are the two things everyone reads within seconds. Learn the principles and you stop memorising 200 tactics — you recognise what a moment needs and reach for the right move."],
    "aspects":[["🔥","Warmth","Be seen as well-intentioned — safe, present, and genuinely interested in the person in front of you."],
      ["⚙️","Competence","Be seen as capable — someone who knows things, gets them done, and can be relied on."],
      ["🎯","Influence","The levers that move people once they already see you as warm and capable."],
      ["🔁","Repair","Recover gracefully when it goes wrong — awkwardness, conflict, and saving face."]],
    "resources":[
      {"type":"Channel","label":"Charisma on Command","note":"Charlie Houpert breaks down what charismatic people actually do.","url":"https://www.youtube.com/charismaoncommand"},
      {"type":"Site","label":"Science of People","note":"Vanessa Van Edwards' research-backed guides to people skills.","url":"https://www.scienceofpeople.com/"},
      {"type":"Site","label":"The School of Life","note":"Emotional intelligence, relationships, and self-knowledge.","url":"https://www.theschooloflife.com/"}],
  },
  "systems-thinking-and-tools.html": {
    "kicker":"Section · Systems Thinking & Tools","title":"Why Systems Thinking","enter":"Explore Systems Thinking",
    "tagline":"Most people navigate life with the handful of ideas they happened to absorb. A few deliberately collect the best thinking tools humanity has produced — and reach for the right one on purpose.",
    "why":[
      "Reality is made of systems — sets of parts connected by feedback loops that produce behaviour over time. If you only see isolated events, you keep treating symptoms. Learn to see the system and you find the leverage point.",
      "This section gathers mental models and thinking tools — from first principles and second-order thinking to Munger's latticework — so you make more informed, rational, and far better decisions in every part of your life."],
    "aspects":[["🧭","Mental models","Reusable lenses — inversion, incentives, margin of safety — that reveal what a situation really is."],
      ["🕸️","Systems & feedback","See stocks, flows and loops; find the leverage point instead of pushing on symptoms."],
      ["♟️","Second-order thinking","Ask 'and then what?' — trace the ripples, not just the splash."],
      ["🧰","A working toolkit","A latticework you can actually reach for when a real decision lands."]],
    "resources":[
      {"type":"Site","label":"Farnam Street","note":"Shane Parrish's hub for mental models and clearer thinking.","url":"https://fs.blog/mental-models/"},
      {"type":"Book","label":"The Great Mental Models","note":"The Farnam Street series mapping the essential models.","url":"https://fs.blog/tgmm/"},
      {"type":"Site","label":"The Donella Meadows Project","note":"'Thinking in Systems' — leverage points and systems primers.","url":"https://donellameadows.org/"}],
  },
  "media-hub.html": {
    "kicker":"Section · Media Hub","title":"Why the Media Hub","enter":"Explore the Media Hub",
    "tagline":"Everything you watch, read, and wrestle with — gathered on purpose, so it compounds into taste, memory, and conversation instead of vanishing.",
    "why":[
      "We consume enormous amounts of media and remember almost none of it. A film that moved you, a book that changed your mind, a channel you loved — gone in a month, un-findable when you want to talk about it.",
      "This hub is a personal catalogue: the Atlas is everything gathered and filed; the Watchlist is what's in front of you now. Tracking it turns passive consumption into a growing canon you can revisit, recommend, and actually discuss."],
    "aspects":[["🗺️","The Atlas","Everything — films, books, ideas — catalogued and searchable in one place."],
      ["▶️","The Watchlist","What you're watching now, what's on hold, and what's finished."],
      ["⭐","Taste over time","A record of what actually stayed with you — your evolving canon."],
      ["💬","Conversation fuel","Find it again the moment you want to share or discuss it."]],
    "resources":[
      {"type":"Site","label":"Letterboxd","note":"Track, rate and review the films you watch.","url":"https://letterboxd.com/"},
      {"type":"Site","label":"Goodreads","note":"Catalogue and track the books you read.","url":"https://www.goodreads.com/"},
      {"type":"Site","label":"IMDb","note":"The reference for everything on screen.","url":"https://www.imdb.com/"}],
  },
}

# rename Brain's "The Model" nav tab -> "Home" (applied to every brain-family page)
BRAIN_RENAME = r"""<script>document.addEventListener('DOMContentLoaded',function(){try{
var links=document.querySelectorAll('nav.top-nav a');
Array.prototype.forEach.call(links,function(a){ if(a.textContent.trim()==='The Model') a.textContent='Home'; });
Array.prototype.forEach.call(document.querySelectorAll('.pager a .ttl'),function(t){ if(t.textContent.trim()==='The Model') t.textContent='Home'; });
var home=null; Array.prototype.forEach.call(links,function(a){ if(a.textContent.trim()==='Home') home=a; });
var brand=document.querySelector('.brand'); if(brand&&home){ brand.style.cursor='pointer'; brand.addEventListener('click',function(e){ e.preventDefault(); home.click(); }); }
}catch(e){}});</script>"""

assets = {}   # basename -> b64
pages_meta = []

NAME2REL = {}
for _pid, _rel, _n, _i, _b in TOP_PAGES: NAME2REL[os.path.basename(_rel)] = _rel
for _rel, _f in SUB_FILES:               NAME2REL[os.path.basename(_rel)] = _rel

def build_page_html(relpath, family, entry, local=None):
    name = os.path.basename(relpath)
    with open(os.path.join(BASE, relpath), "rb") as f:
        raw = f.read()
    h = inject(raw, name, family, entry, local)
    if name in EXTRA_SKIN:  h = insert_before_body(h, EXTRA_SKIN[name])
    if name in HOME_PANELS: h = insert_before_body(h, build_home(name, HOME_PANELS[name]))
    if family == "brain":   h = insert_before_body(h, BRAIN_RENAME)
    return name, h

def _b64(h): return base64.b64encode(h.encode('utf-8')).decode('ascii')

# Pass 1 — leaf versions (no local map). This is what the hosted site serves and what gets
# embedded inside shells so tabs/links also work when the file is opened locally (file://).
for pid, relpath, name, icon, blurb in TOP_PAGES:
    fam = "brain" if pid == "brain" else ""
    nm, h = build_page_html(relpath, fam, True)
    assets[nm] = _b64(h)
    pages_meta.append({"id": pid, "name": name, "icon": icon, "blurb": blurb, "featured": pid in FEATURED, "file": nm})
for relpath, family in SUB_FILES:
    fam = "brain" if family == "brain" else ""
    nm, h = build_page_html(relpath, fam, False)
    assets[nm] = _b64(h)

# Pass 2 — rebuild multi-page shells carrying their sub-pages (self-contained for file://).
def _fam_subs(fam): return [os.path.basename(r) for r, f in SUB_FILES if f == fam]

_media_map = {n: assets[n] for n in _fam_subs("media")}
_, _h = build_page_html(NAME2REL["media-hub.html"], "", True, local=_media_map)
assets["media-hub.html"] = _b64(_h)

_sys_map = {n: assets[n] for n in _fam_subs("systems")}
_, _h = build_page_html(NAME2REL["systems-thinking-and-tools.html"], "", True, local=_sys_map)
assets["systems-thinking-and-tools.html"] = _b64(_h)

_brain_names = ["Brain as a System.html"] + _fam_subs("brain")
_brain_map = {n: assets[n] for n in _brain_names}
for n in _brain_names:
    _, _h = build_page_html(NAME2REL[n], "brain", n == "Brain as a System.html", local=_brain_map)
    assets[n] = _b64(_h)

# ---- brand-new placeholder sections (content to be defined together) ----
NEW_SECTIONS = [
  {"id":"workout","file":"workout.html","name":"Workout","icon":"🏋️",
   "blurb":"Training, strength, mobility and recovery — building a capable body on purpose.",
   "tagline":"A capable body is the vehicle for everything else. This is where the plan to build it lives.",
   "ideas":["Training split & weekly schedule","Progressive overload & the key lifts","Mobility & injury prevention","Recovery, sleep & deload weeks","A simple log to track progress"]},
  {"id":"nutrition","file":"nutrition.html","name":"Nutrition","icon":"🥗",
   "blurb":"Fuel, macros, meals and habits that make the body and mind work.",
   "tagline":"You can't out-train a poor diet. This is where the fuelling strategy takes shape.",
   "ideas":["Calorie & macro targets","Go-to meals & recipes","Grocery list & meal prep","Supplements & hydration","Eating out without derailing"]},
  {"id":"fashion","file":"fashion.html","name":"Fashion","icon":"🧥",
   "blurb":"Fit, style and presence — dressing like the person you're becoming.",
   "tagline":"Clothes are a language. This is where you learn to speak it deliberately.",
   "ideas":["Fit first — the non-negotiable","Building a capsule wardrobe","Colour & proportion basics","Outfits for the key occasions","Where to shop & what to invest in"]},
  {"id":"humor","file":"humor.html","name":"Humor Development","icon":"😄",
   "blurb":"Wit, timing and playfulness — becoming genuinely fun to be around.",
   "tagline":"Humor is a skill, not a gift. This is where you train it on purpose.",
   "ideas":["Your natural style of humor","Timing, delivery & callbacks","Storytelling & the funny beat","Building a reference bank","Practice reps in real conversations"]},
  {"id":"ncr","file":"ncr.html","name":"Daily NCR Mapping","icon":"🗺️",
   "blurb":"Mapping outings across the Delhi NCR — Noida, Delhi & Gurugram.",
   "tagline":"","ideas":[]},
  {"id":"travel","file":"travel.html","name":"Travel","icon":"✈️",
   "blurb":"Places to go, trips to plan, and the systems that make travel effortless.",
   "tagline":"The world is the syllabus. This is where the trips get dreamed, planned and remembered.",
   "ideas":["Bucket-list destinations & the why","Trip planning & itineraries","Packing systems & essentials","Budget, points & miles","Travel journal & memories"]},
  {"id":"sportsmindset","file":"sportsmindset.html","name":"Sports Mindset","icon":"🧠",
   "blurb":"The mental game — focus, pressure, resilience and the champion's mentality.",
   "tagline":"Talent sets the floor; mindset sets the ceiling. This is where the inner game gets trained.",
   "ideas":["The champion's mentality","Pre-game routines & focus","Handling pressure & nerves","Resilience after a loss","Visualisation & self-talk","Lessons from the greats"]},
  {"id":"cricket","file":"cricket.html","name":"Cricket","icon":"🏏",
   "blurb":"Batting, bowling, fielding and game sense — the craft of the sport.",
   "tagline":"A game of skill, patience and situations. This is where the technique and the tactics live.",
   "ideas":["Batting technique & shot selection","Bowling — pace, spin & variations","Fielding & fitness","Reading the game & match situations","Practice drills & net routines","Learning from the greats"]},
  {"id":"boardgames","file":"boardgames.html","name":"Board Games","icon":"🎲",
   "blurb":"Fun mode — strategies, tactics and notes for the games we play.",
   "tagline":"Every game is a little world with its own logic. This is where the strategies and the lessons from each session live.",
   "ideas":["Catan — setup, trading & robber tactics","Hollywood 1947 — bidding & bluffing","Openings & common mistakes","Win-rate & session tracking","House rules & variants","Reading opponents"]},
]

def make_placeholder(sec):
    cards = "".join('<div class="card"><span class="n">%d</span><span>%s</span></div>' % (i+1, _esc(t)) for i,t in enumerate(sec["ideas"]))
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
      '<meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title>'
      '<style>:root{--bg:#f6f7f9;--surface:#fff;--ink:#1c2431;--dim:#5b6472;--line:#e7e9ee;--accent:#4f46e5;--soft:#eef0fb}'
      '*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}'
      '.wrap{max-width:860px;margin:0 auto;padding:64px 28px 96px}'
      '.badge{display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);background:var(--soft);padding:6px 12px;border-radius:999px}'
      '.ic{font-size:52px;margin:26px 0 0;line-height:1}'
      'h1{font-size:clamp(34px,6vw,54px);letter-spacing:-.02em;margin:10px 0 0;font-weight:800;background:linear-gradient(120deg,var(--ink),var(--accent));-webkit-background-clip:text;background-clip:text;color:transparent}'
      '.tag{font-size:18.5px;color:var(--dim);line-height:1.6;max-width:600px;margin:16px 0 0}'
      '.note{margin:30px 0 0;padding:16px 20px;border:1px dashed var(--line);border-radius:14px;background:var(--surface);color:var(--dim);font-size:14.5px;line-height:1.6}'
      '.lbl{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:44px 0 14px;display:flex;align-items:center;gap:10px}.lbl::after{content:"";flex:1;height:1px;background:var(--line)}'
      '.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}'
      '.card{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px 18px;box-shadow:0 1px 2px rgba(20,25,40,.05),0 6px 18px rgba(20,25,40,.04);font-size:14.5px;color:var(--ink);display:flex;gap:10px;align-items:flex-start;line-height:1.5}'
      '.card .n{color:var(--accent);font-weight:800;flex:0 0 auto}</style></head>'
      '<body><div class="wrap"><span class="badge">✦ New section</span><div class="ic">%s</div><h1>%s</h1>'
      '<p class="tag">%s</p>'
      '<div class="note">This section is set up and ready — we\'ll shape what goes inside it together. The ideas below are just starting points to react to.</div>'
      '<div class="lbl">Ideas to consider</div><div class="cards">%s</div></div></body></html>') % (
      _esc(sec["name"]), sec["icon"], _esc(sec["name"]), _esc(sec["tagline"]), cards)

NCR_PAGE = r"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Daily NCR Mapping</title><style>
:root{--bg:#f6f7f9;--surface:#fff;--ink:#1c2431;--dim:#5b6472;--line:#e7e9ee;--line2:#dcdfe6;--accent:#4f46e5;--soft:#eef0fb}
*{box-sizing:border-box}html,body{margin:0;height:100%}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);-webkit-font-smoothing:antialiased}
.ncr{display:flex;flex-direction:column;height:100vh}
.top{flex:0 0 auto;display:flex;align-items:center;gap:16px;padding:12px 20px;background:var(--surface);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20}
.brand{font-weight:800;font-size:15px;letter-spacing:-.01em;display:flex;align-items:center;gap:8px;white-space:nowrap}
.cities{display:flex;gap:6px;margin-left:auto}
.cities button{border:1px solid var(--line2);background:var(--bg);color:var(--dim);font:inherit;font-size:13.5px;font-weight:600;padding:8px 18px;border-radius:999px;cursor:pointer}
.cities button:hover{color:var(--ink)}
.cities button.active{background:var(--accent);border-color:var(--accent);color:#fff}
.body{flex:1;display:flex;min-height:0}
.catcol{flex:0 0 240px;overflow-y:auto;border-right:1px solid var(--line);background:var(--surface);padding:10px}
.subcol{flex:0 0 200px;overflow-y:auto;border-right:1px solid var(--line);padding:10px}
.content{flex:1;overflow-y:auto;padding:28px 34px 60px}
.catcol .lbl,.subcol .lbl{font-size:10.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--dim);padding:8px 10px 8px;text-transform:uppercase}
.catbtn{display:flex;gap:10px;align-items:center;width:100%;text-align:left;border:1px solid transparent;background:none;font:inherit;padding:9px 10px;border-radius:10px;cursor:pointer;color:var(--dim);margin-bottom:2px}
.catbtn:hover{background:var(--soft);color:var(--ink)}
.catbtn.active{background:var(--soft);color:var(--ink);border-color:var(--accent);font-weight:700}
.catbtn .cn{font-size:11px;font-weight:800;color:var(--accent);flex:0 0 auto;font-variant-numeric:tabular-nums}
.catbtn .cnm{flex:1;font-size:13.5px;line-height:1.2}
.subbtn{display:block;width:100%;text-align:left;border:0;background:none;font:inherit;font-size:13.5px;padding:9px 10px;border-radius:9px;cursor:pointer;color:var(--dim);text-transform:capitalize;margin-bottom:2px}
.subbtn:hover{background:var(--soft);color:var(--ink)}
.subbtn.active{background:var(--accent);color:#fff;font-weight:700}
.chead{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.crumbs{font-size:13px;color:var(--dim)}.crumbs b{color:var(--ink)}
.citybadge{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--accent);background:var(--soft);padding:5px 11px;border-radius:999px}
h2.ct{font-size:26px;font-weight:800;letter-spacing:-.01em;margin:10px 0 0;text-transform:capitalize}
.ideas-lbl,.note-lbl{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--dim);margin:26px 0 10px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:7px 13px;font-size:13px;color:var(--ink)}
textarea.note{width:100%;min-height:220px;border:1px solid var(--line2);border-radius:14px;padding:16px;font:inherit;font-size:14.5px;line-height:1.65;color:var(--ink);background:var(--surface);resize:vertical;outline:none}
textarea.note:focus{border-color:var(--accent)}
.savehint{font-size:12px;color:var(--dim);margin-top:8px}
.search{position:relative;flex:1;max-width:440px}
.search input{width:100%;border:1px solid var(--line2);background:var(--bg);border-radius:999px;padding:9px 16px 9px 38px;font:inherit;font-size:14px;color:var(--ink);outline:none}
.search input:focus{border-color:var(--accent);background:#fff}
.search .si{position:absolute;left:14px;top:50%;transform:translateY(-50%);font-size:14px;color:var(--dim);pointer-events:none}
.results{position:absolute;top:46px;left:0;right:0;background:#fff;border:1px solid var(--line2);border-radius:14px;box-shadow:0 10px 34px rgba(20,25,40,.16);max-height:64vh;overflow:auto;z-index:60;display:none;padding:6px}
.results.open{display:block}
.results .ri{display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:9px;cursor:pointer}
.results .ri:hover,.results .ri.sel{background:var(--soft)}
.results .ri .rt{font-size:14px;font-weight:600;color:var(--ink);flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.results .ri .rs{font-size:12px;color:var(--dim);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:44%}
.results .ri .rk{font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.04em;color:var(--accent);background:var(--soft);border-radius:999px;padding:3px 8px;flex:0 0 auto}
.results .none{padding:16px 12px;color:var(--dim);font-size:13.5px}
@media(max-width:820px){.body{flex-direction:column}.catcol,.subcol{flex:0 0 auto;max-height:160px;border-right:0;border-bottom:1px solid var(--line)}}
@media(max-width:600px){.top{flex-wrap:wrap}.search{max-width:none;order:3;flex:1 0 100%}.cities{margin-left:0}}
</style></head><body>
<div class="ncr">
 <header class="top"><div class="brand">🗺️ Daily NCR Mapping</div><div class="search"><span class="si">🔍</span><input id="q" type="text" placeholder="Search anything — localities, cafés, activities…" autocomplete="off"><div class="results" id="res"></div></div><div class="cities" id="cities"></div></header>
 <div class="body"><nav class="catcol" id="catcol"></nav><nav class="subcol" id="subcol"></nav><main class="content" id="content"></main></div>
</div>
<script>
var TAXO=__TAXO__;var CITIES=["Noida","Delhi","Gurugram"];var CAFE_DOC="__CAFE_DOC__";var CAFE_DATA=__CAFE_DATA__;var __cafeURL=null;
function cafeURL(){ // try cross-frame resolver (works on hosted site); fall back to a self-contained local blob (works on file://)
  try{ if(window.top&&window.top!==window&&window.top.__HUB_RESOLVE__){var u=window.top.__HUB_RESOLVE__("cafe-app.html"); if(u)return u;} }catch(e){}
  if(__cafeURL)return __cafeURL;
  try{ var bin=atob(CAFE_DOC),arr=new Uint8Array(bin.length); for(var i=0;i<bin.length;i++)arr[i]=bin.charCodeAt(i); __cafeURL=URL.createObjectURL(new Blob([arr],{type:"text/html"})); return __cafeURL; }catch(e2){ return null; }
}
(function(){
 var K="ncr.state.v1";
 var S={city:1,cat:0,sub:0}; try{var o=JSON.parse(localStorage.getItem(K)||"null");if(o&&typeof o==="object")S=o;}catch(e){}
 if(S.city==null||S.city<0||S.city>2)S.city=1;
 if(S.cat>=TAXO.length)S.cat=0; if(!TAXO[S.cat]||S.sub>=TAXO[S.cat].subs.length)S.sub=0;
 function save(){try{localStorage.setItem(K,JSON.stringify(S));}catch(e){}}
 function esc(t){return (t||"").replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c];});}
 function pad(n){n=String(n);return n.length<2?"0"+n:n;}
 function noteKey(){return "ncr.note."+CITIES[S.city]+"."+S.cat+"."+S.sub;}
 function renderCities(){var el=document.getElementById("cities");el.innerHTML="";CITIES.forEach(function(c,i){var b=document.createElement("button");b.textContent=c;if(i===S.city)b.className="active";b.onclick=function(){S.city=i;save();render();};el.appendChild(b);});}
 function renderCats(){var el=document.getElementById("catcol");el.innerHTML='<div class="lbl">Categories</div>';TAXO.forEach(function(c,i){var b=document.createElement("button");b.className="catbtn"+(i===S.cat?" active":"");b.innerHTML='<span class="cn">'+pad(i+1)+'</span><span class="cnm">'+esc(c.name)+'</span>';b.onclick=function(){S.cat=i;S.sub=0;save();render();};el.appendChild(b);});}
 function renderSubs(){var el=document.getElementById("subcol");el.innerHTML='<div class="lbl">'+esc(TAXO[S.cat].name)+'</div>';TAXO[S.cat].subs.forEach(function(sc,i){var b=document.createElement("button");b.className="subbtn"+(i===S.sub?" active":"");b.textContent=sc.name;b.onclick=function(){S.sub=i;save();render();};el.appendChild(b);});}
 function renderContent(){var el=document.getElementById("content");var cat=TAXO[S.cat];var scol=document.getElementById("subcol");var isSC=(cat.name==="Social & Chill");if(scol)scol.style.display=isSC?"none":"";el.style.padding=isSC?"0":"";if(isSC){var _u=cafeURL();var _h="#"+encodeURIComponent(CITIES[S.city]);if(S._cafeTarget)_h+="|"+encodeURIComponent(S._cafeTarget);el.innerHTML=_u?'<iframe title="Cafe map" style="width:100%;height:100%;border:0;display:block" src="'+_u+_h+'"></iframe>':'<div style="padding:28px;color:#5b6472">Cafe map unavailable.</div>';S._cafeTarget=null;return;}var sub=cat.subs[S.sub];
   var items=(sub.items||"").split(/[,·]/).map(function(x){return x.trim();}).filter(Boolean);
   var chips=items.map(function(x){return '<span class="chip">'+esc(x)+'</span>';}).join("");
   el.innerHTML='<div class="chead"><span class="crumbs"><b>'+esc(cat.name)+'</b> &nbsp;▸&nbsp; <b style="text-transform:capitalize">'+esc(sub.name)+'</b></span><span class="citybadge">'+esc(CITIES[S.city])+'</span></div>'
     +'<h2 class="ct">'+esc(sub.name)+'</h2>'
     +'<div class="ideas-lbl">Ideas &amp; examples</div><div class="chips">'+chips+'</div>'
     +'<div class="note-lbl">Your '+esc(CITIES[S.city])+' spots &mdash; '+esc(sub.name)+'</div>'
     +'<textarea class="note" id="note" placeholder="List specific places in '+esc(CITIES[S.city])+' for '+esc(sub.name)+' — venues, notes, who to go with, status…"></textarea>'
     +'<div class="savehint">Saved automatically on this device.</div>';
   var ta=document.getElementById("note"); try{ta.value=localStorage.getItem(noteKey())||"";}catch(e){}
   var t=null; ta.addEventListener("input",function(){clearTimeout(t);t=setTimeout(function(){try{localStorage.setItem(noteKey(),ta.value);}catch(e){}},300);});
 }
 function render(){renderCities();renderCats();renderSubs();renderContent();}
 // ---- global search across taxonomy + all café data ----
 var SC_IDX=-1; TAXO.forEach(function(c,i){if(c.name==="Social & Chill")SC_IDX=i;});
 var IDX=null;
 function buildIndex(){var a=[];
   TAXO.forEach(function(c,ci){a.push({t:c.name,s:"Category",k:"category",ci:ci,si:0});
     (c.subs||[]).forEach(function(sc,si){a.push({t:sc.name,s:c.name,k:"activity",ci:ci,si:si});
       (sc.items||"").split(/[,·]/).forEach(function(it){it=it.trim();if(it)a.push({t:it,s:sc.name+" · "+c.name,k:"idea",ci:ci,si:si});});});});
   if(CAFE_DATA&&typeof CAFE_DATA==="object"){Object.keys(CAFE_DATA).forEach(function(cty){var d=CAFE_DATA[cty]||{};var locs={};
     Object.keys(d.geo||{}).forEach(function(k){locs[k]=1;});(d.cafes||[]).forEach(function(p){locs[p[0]]=1;});
     Object.keys(locs).forEach(function(k){a.push({t:k,s:cty+" · locality",k:"locality",city:cty,cl:k});});
     (d.cafes||[]).forEach(function(p){(p[1]||[]).forEach(function(cf){a.push({t:cf[0],s:cty+" · "+p[0],k:"café",city:cty,cl:p[0]});});});});}
   return a;}
 var resEl=document.getElementById("res"),qEl=document.getElementById("q");
 function runSearch(q){q=(q||"").trim().toLowerCase();if(!q){resEl.classList.remove("open");resEl.innerHTML="";return;}
   if(!IDX)IDX=buildIndex();
   var hits=[];for(var i=0;i<IDX.length;i++){var it=IDX[i];if((it.t+" "+it.s).toLowerCase().indexOf(q)>=0){it._i=i;hits.push(it);}}
   hits.sort(function(x,y){var xa=x.t.toLowerCase().indexOf(q),ya=y.t.toLowerCase().indexOf(q);return (xa<0?99:xa)-(ya<0?99:ya);});
   if(!hits.length){resEl.innerHTML='<div class="none">No matches for "'+esc(q)+'"</div>';resEl.classList.add("open");return;}
   var html="";hits.slice(0,40).forEach(function(it,ix){html+='<div class="ri'+(ix===0?' sel':'')+'" data-i="'+it._i+'"><span class="rt">'+esc(it.t)+'</span><span class="rs">'+esc(it.s)+'</span><span class="rk">'+esc(it.k)+'</span></div>';});
   resEl.innerHTML=html;resEl.classList.add("open");}
 function goTo(it){if(!it)return;resEl.classList.remove("open");qEl.value="";
   if(it.city!=null&&it.cl!=null){var cix=CITIES.indexOf(it.city);if(cix>=0)S.city=cix;if(SC_IDX>=0)S.cat=SC_IDX;S.sub=0;S._cafeTarget=it.cl;save();render();return;}
   S.cat=it.ci;S.sub=it.si||0;S._cafeTarget=null;save();render();}
 if(qEl){
   qEl.addEventListener("input",function(){runSearch(qEl.value);});
   qEl.addEventListener("focus",function(){if(qEl.value.trim())runSearch(qEl.value);});
   qEl.addEventListener("keydown",function(e){var arr=Array.prototype.slice.call(resEl.querySelectorAll(".ri"));var sel=resEl.querySelector(".ri.sel");
     if(e.key==="ArrowDown"||e.key==="ArrowUp"){e.preventDefault();if(!arr.length)return;var i=arr.indexOf(sel);i=e.key==="ArrowDown"?Math.min(arr.length-1,i+1):Math.max(0,i-1);arr.forEach(function(el){el.classList.remove("sel");});arr[i].classList.add("sel");arr[i].scrollIntoView({block:"nearest"});}
     else if(e.key==="Enter"){e.preventDefault();var s=sel||arr[0];if(s)goTo(IDX[parseInt(s.getAttribute("data-i"),10)]);}
     else if(e.key==="Escape"){resEl.classList.remove("open");qEl.blur();}});
   resEl.addEventListener("mousedown",function(e){var ri=e.target.closest?e.target.closest(".ri"):null;if(!ri)return;e.preventDefault();goTo(IDX[parseInt(ri.getAttribute("data-i"),10)]);});
   document.addEventListener("click",function(e){if(!(e.target.closest&&e.target.closest(".search")))resEl.classList.remove("open");});
 }
 render();
})();
</script></body></html>"""

def make_ncr_page(taxo):
    return NCR_PAGE.replace("__TAXO__", json.dumps(taxo, ensure_ascii=False))

def make_humor_app():
    b = "/sessions/eloquent-awesome-knuth/mnt/outputs/"
    tpl  = open(b + "humor_app_template.html", encoding="utf-8").read()
    vlib = open(b + "vizlib.js", encoding="utf-8").read()
    tax  = json.load(open(b + "humor_taxonomy.json", encoding="utf-8"))
    emap = {"expansion":"humor_associative-expansion.html","wheel":"humor_association-wheel.html",
            "irony":"humor_comedians-irony-lens.html","engine":"humor_irony-exploitation-engine.html",
            "room":"humor_comedy-engine-room.html","viz":"humor_concept-visualization-explorer.html"}
    embeds = {k: base64.b64encode(open(b + v, "rb").read()).decode("ascii") for k, v in emap.items()}
    return (tpl.replace("__VIZLIB__", vlib)
               .replace("__TAXO__", json.dumps(tax, ensure_ascii=False))
               .replace("__EMBEDS__", json.dumps(embeds)))

def make_workout_app():
    b = "/sessions/eloquent-awesome-knuth/mnt/outputs/"
    tpl  = open(b + "workout_app_template.html", encoding="utf-8").read()
    vlib = open(b + "vizlib.js", encoding="utf-8").read()
    tax  = json.load(open(b + "workout_taxonomy.json", encoding="utf-8"))
    board = base64.b64encode(open(b + "workout_board.jpg", "rb").read()).decode("ascii")
    return (tpl.replace("__VIZLIB__", vlib)
               .replace("__TAXO__", json.dumps(tax, ensure_ascii=False))
               .replace("__BOARD__", board))

def make_cricket_app():
    b = "/sessions/eloquent-awesome-knuth/mnt/outputs/"
    tpl  = open(b + "cricket_app_template.html", encoding="utf-8").read()
    vlib = open(b + "vizlib.js", encoding="utf-8").read()
    def j(f): return json.dumps(json.load(open(b + f, encoding="utf-8")), ensure_ascii=False)
    board = base64.b64encode(open(b + "cricket_board.jpg", "rb").read()).decode("ascii")
    return (tpl.replace("__VIZLIB__", vlib)
               .replace("__LIVE__", j("cricket_live.json"))
               .replace("__HIST__", j("cricket_hist.json"))
               .replace("__VENUES__", j("cricket_venues.json"))
               .replace("__ARCHIVE__", j("cricket_archive.json"))
               .replace("__BOARD__", board))

def make_sm_app():
    b = "/sessions/eloquent-awesome-knuth/mnt/outputs/"
    tpl  = open(b + "sm_app_template.html", encoding="utf-8").read()
    vlib = open(b + "vizlib.js", encoding="utf-8").read()
    ids = ["phenomenology-of-mastery","flow-state-skill-layers","performance-under-pressure",
           "performance-anxiety-framework","fear-to-execution-system","the-fatigued-brain-protocol",
           "the-sport-session-protocol","the-stamina-blueprint","feedback-loop-protocol",
           "internalization-engine","sports-mindsets-mastery-blueprint","the-weak-partner-protocol",
           "character-analysis-framework"]
    emb = {i: base64.b64encode(open(b + "sm_" + i + ".html", "rb").read()).decode("ascii") for i in ids}
    return tpl.replace("__VIZLIB__", vlib).replace("__EMBEDS__", json.dumps(emb))

def make_nutrition_app():
    b = "/sessions/eloquent-awesome-knuth/mnt/outputs/"
    tpl  = open(b + "nutrition_app_template.html", encoding="utf-8").read()
    vlib = open(b + "vizlib.js", encoding="utf-8").read()
    data = json.dumps(json.load(open(b + "nutrition.json", encoding="utf-8")), ensure_ascii=False)
    return tpl.replace("__VIZLIB__", vlib).replace("__DATA__", data)

def add_generated(name, raw_html, meta):
    h = inject(raw_html.encode('utf-8'), name, "", True)
    assets[name] = base64.b64encode(h.encode('utf-8')).decode('ascii')
    m = dict(meta); m["file"] = name; pages_meta.append(m)

def _new_section_raw(sec):
    if sec["id"] == "ncr":           return make_ncr_page(NCR_TAXO)
    if sec["id"] == "humor":         return make_humor_app()
    if sec["id"] == "workout":       return make_workout_app()
    if sec["id"] == "cricket":       return make_cricket_app()
    if sec["id"] == "sportsmindset": return make_sm_app()
    if sec["id"] == "nutrition":     return make_nutrition_app()
    return make_placeholder(sec)

for sec in NEW_SECTIONS:
    raw = _new_section_raw(sec)
    add_generated(sec["file"], raw,
                  {"id":sec["id"], "name":sec["name"], "icon":sec["icon"], "blurb":sec["blurb"], "featured":False})

# ---- Cafe app: NCR -> {city} -> Social & Chill (Districts / Cafes / How to Explore / Navigate) ----
CAFE_EXPLORE_HTML = ('<h2>The Outing Knowledge System</h2>'
 '<p class="lead">You build the map — the taxonomy and branches. The research engine travels each node and fills it in. Pin the node and the output gets far sharper than "best cafés in Delhi."</p>'
 '<h4>Pin four things</h4><div class="grid">'
 '<div class="card"><b>1 · Bucket</b><span>Social &amp; Chill</span></div>'
 '<div class="card"><b>2 · Subcategory</b><span>Cafés (food-based)</span></div>'
 '<div class="card"><b>3 · Geography</b><span>Delhi NCR / Delhi / South Delhi</span></div>'
 '<div class="card"><b>4 · Stage</b><span>Where you are in exploration — the key pin</span></div></div>'
 '<h4>Five stages of exploration</h4><div class="scen" style="padding:6px 20px">'
 '<div class="step"><div class="k">1</div><div class="b"><b>Mapping</b> — <span>"Major café localities in Delhi?" → Khan Market · CP · Lodhi · HKV · Majnu Ka Tila…</span></div></div>'
 '<div class="step"><div class="k">2</div><div class="b"><b>Understanding</b> — <span>"What is each known for?" → Khan Market = premium · Majnu Ka Tila = Tibetan · Lodhi = aesthetic</span></div></div>'
 '<div class="step"><div class="k">3</div><div class="b"><b>Discovery</b> — <span>"Best cafés within Khan Market." → the shortlist, with what each is best for</span></div></div>'
 '<div class="step"><div class="k">4</div><div class="b"><b>Comparison</b> — <span>"Khan Market vs Lodhi for café-hopping." → head-to-head on vibe, price, walkability</span></div></div>'
 '<div class="step"><div class="k">5</div><div class="b"><b>System building</b> — <span>"Permanent café categories for my system." → reusable tags &amp; structure</span></div></div></div>'
 '<h4>Always — which mode?</h4><div class="grid">'
 '<div class="card"><b>🧭 Exploration</b><span>"Help me understand the landscape." Values completeness.</span></div>'
 '<div class="card"><b>📅 Decision</b><span>"I\'m going out tomorrow." Values practicality.</span></div></div>'
 '<h4>The prompt template</h4><pre>Bucket: Social &amp; Chill\nSubcategory: Cafés\nLocation: Delhi\nStage: Mapping\nMode: Exploration\nObjective:\nI\'m building my outing knowledge system. No recommendations yet —\nI want the major café clusters in Delhi and what each is known for.</pre>')

CAFE_NAV_HTML = ('<h2>Navigate the Map — from knowledge to intuition</h2>'
 '<p class="lead">The spreadsheet stores the knowledge; the quizzes make it live in your head. The step most people skip is retrieval: Read → Understand → <b>Retrieve · Retrieve · Retrieve</b> → Internalize.</p>'
 '<h4>What you\'re building — situation → location → venue</h4><div class="scen" style="padding:6px 20px">'
 '<div class="row"><div class="s">Deep conversation</div><div class="c">Khan Market → Perch</div></div>'
 '<div class="row"><div class="s">Visitor from outside Delhi</div><div class="c">Mehrauli → Dramz</div></div>'
 '<div class="row"><div class="s">Student friends</div><div class="c">Satya Niketan → Big Yellow Door</div></div></div>'
 '<h4>The quiz ladder</h4><div class="scen" style="padding:6px 20px">'
 '<div class="step"><div class="k">1</div><div class="b"><b>Direct retrieval</b> — <span>"Deep conversation — which cluster?" → Khan Market</span></div></div>'
 '<div class="step"><div class="k">2</div><div class="b"><b>Cluster + venue</b> — <span>"Friend loves coffee &amp; real talk — where?" → Khan Market → Perch</span></div></div>'
 '<div class="step"><div class="k">3</div><div class="b"><b>Comparison</b> — <span>"First date — Khan Market or Champa Gali?" → justify it</span></div></div>'
 '<div class="step"><div class="k">4</div><div class="b"><b>Constraint-based</b> — <span>"Student · ₹500 · four friends · Saturday." → optimize</span></div></div>'
 '<div class="step"><div class="k">5</div><div class="b"><b>Outing design</b> — <span>"Friend visiting Delhi for one evening." → cluster → venue → why</span></div></div></div>'
 '<h4>Build an outing across branches</h4><div class="grid">'
 '<div class="card"><b>2 PM</b><span>Pottery</span></div><div class="card"><b>4 PM</b><span>Café</span></div>'
 '<div class="card"><b>6 PM</b><span>Heritage walk</span></div><div class="card"><b>8 PM</b><span>Dinner</span></div></div>'
 '<p class="lead" style="margin-top:20px">When you hear a situation and instantly think "that\'s a Lodhi situation" — the knowledge has left the sheet and started living in your head.</p>')

CAFE_APP_TMPL = r"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cafes</title><style>
:root{--bg:#f6f7f9;--surface:#fff;--ink:#1c2431;--dim:#5b6472;--line:#e7e9ee;--line2:#dcdfe6;--accent:#4f46e5;--soft:#eef0fb;--gold:#caa24a}
*{box-sizing:border-box}html,body{margin:0;height:100%}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);-webkit-font-smoothing:antialiased}
.app{display:flex;flex-direction:column;height:100vh}
.top{flex:0 0 auto;display:flex;align-items:center;gap:8px;padding:11px 22px;background:var(--surface);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:10;flex-wrap:wrap}
.ttl{font-weight:800;font-size:15px;display:flex;align-items:center;gap:8px;white-space:nowrap;margin-right:8px}
.tabs{display:flex;gap:4px;flex-wrap:wrap}
.tabs button{border:0;background:none;color:var(--dim);font:inherit;font-size:13.5px;font-weight:600;padding:8px 14px;border-radius:9px;cursor:pointer}
.tabs button:hover{background:var(--soft);color:var(--ink)}
.tabs button.active{background:var(--accent);color:#fff}
.wrap{flex:1;overflow-y:auto;padding:24px 30px 70px}
.note{font-size:13px;color:var(--dim);background:var(--soft);border-radius:10px;padding:10px 14px;margin-bottom:16px}
.dist{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px 20px;margin-bottom:12px;box-shadow:0 1px 2px rgba(20,25,40,.04)}
.dist h3{margin:0;font-size:17px;font-weight:800}
.dist .idn{color:var(--accent);font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:.04em;margin-top:3px}
.dist p{margin:8px 0 0;font-size:14px;color:var(--dim);line-height:1.55}
.dist .bf{margin-top:8px;font-size:13.5px}.dist .bf b{color:var(--ink)}
.scen{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:2px 20px;margin-top:6px}
.scen .row{display:flex;gap:14px;padding:11px 0;border-top:1px solid var(--line);font-size:14px}.scen .row:first-child{border-top:0}
.scen .s{flex:0 0 210px;font-weight:700}.scen .c{color:var(--dim)}
.lochead{font-size:12px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:var(--accent);margin:24px 0 12px;display:flex;align-items:center;gap:10px}.lochead::after{content:"";flex:1;height:1px;background:var(--line)}
.cafe{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:15px 18px;margin-bottom:11px;box-shadow:0 1px 2px rgba(20,25,40,.04)}
.cafe .h{display:flex;align-items:flex-start;gap:12px}
.cafe .nm{font-size:16px;font-weight:750;flex:1}
.cafe.done .nm{color:var(--dim)}
.vbtn{flex:0 0 auto;border:1px solid var(--line2);background:var(--bg);color:var(--dim);font:inherit;font-size:12px;font-weight:700;padding:6px 12px;border-radius:999px;cursor:pointer}
.cafe.done .vbtn{background:var(--accent);border-color:var(--accent);color:#fff}
.tag{display:inline-block;margin-top:8px;font-size:11.5px;font-weight:700;color:var(--gold);background:#faf3df;border-radius:999px;padding:4px 10px}
.why{margin:9px 0 0;font-size:13.5px;color:var(--dim);line-height:1.55}
.cafe textarea{width:100%;margin-top:10px;min-height:40px;border:1px solid var(--line2);border-radius:10px;padding:9px 12px;font:inherit;font-size:13.5px;color:var(--ink);background:var(--bg);resize:vertical;outline:none}
.cafe textarea:focus{border-color:var(--accent)}
.cafe .h{align-items:center}
.maplink{flex:0 0 auto;font-size:12px;font-weight:700;color:var(--accent);text-decoration:none;padding:6px 11px;border:1px solid var(--line2);border-radius:999px;margin-right:8px;white-space:nowrap}
.maplink:hover{border-color:var(--accent);background:var(--soft)}
.addedtag{font-size:10px;font-weight:800;color:var(--accent);background:var(--soft);border-radius:999px;padding:3px 8px;margin-left:8px;vertical-align:middle}
.meta{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:10px}
.stars{display:inline-flex;gap:3px}
.stars .st{cursor:pointer;font-size:18px;color:#d8dbe2;line-height:1}
.stars .st.on{color:#f5a623}
.occ{flex:1;min-width:190px;border:1px solid var(--line2);border-radius:9px;padding:8px 11px;font:inherit;font-size:13px;color:var(--ink);background:var(--bg);outline:none}
.occ:focus{border-color:var(--accent)}
.del{border:0;background:none;color:#c0453a;font:inherit;font-size:12px;font-weight:700;cursor:pointer;padding:4px 6px}
.addbtn{border:1px dashed var(--line2);background:none;color:var(--accent);font:inherit;font-size:13px;font-weight:700;padding:9px 14px;border-radius:10px;cursor:pointer;margin:2px 0 12px}
.addbtn:hover{background:var(--soft)}
.addform{background:var(--soft);border:1px solid var(--line);border-radius:12px;padding:14px;margin:2px 0 14px;display:none;grid-template-columns:1fr;gap:9px;max-width:520px}
.addform.open{display:grid}
.addform input{border:1px solid var(--line2);border-radius:9px;padding:9px 11px;font:inherit;font-size:13.5px;background:#fff;outline:none;width:100%}
.addform input:focus{border-color:var(--accent)}
.addform button{justify-self:start;border:0;background:var(--accent);color:#fff;font:inherit;font-weight:700;font-size:13.5px;padding:9px 18px;border-radius:9px;cursor:pointer}
.newloc{display:flex;gap:8px;margin-top:24px;max-width:460px}
.newloc input{flex:1;border:1px solid var(--line2);border-radius:9px;padding:10px 12px;font:inherit;font-size:14px;background:#fff;outline:none}
.newloc button{border:0;background:var(--ink);color:#fff;font:inherit;font-weight:700;padding:10px 16px;border-radius:9px;cursor:pointer}
.empty{border:2px dashed var(--line2);border-radius:14px;padding:44px 24px;text-align:center;color:var(--dim);font-size:14.5px}
.fx h2{font-size:22px;font-weight:800;letter-spacing:-.01em;margin:4px 0 4px}
.fx .lead{color:var(--dim);font-size:15.5px;line-height:1.6;max-width:680px;margin:0 0 8px}
.fx h4{font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:24px 0 10px;display:flex;align-items:center;gap:10px}.fx h4::after{content:"";flex:1;height:1px;background:var(--line)}
.fx .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.fx .card{background:var(--surface);border:1px solid var(--line);border-radius:13px;padding:14px 16px;box-shadow:0 1px 2px rgba(20,25,40,.04)}
.fx .card b{display:block;font-size:14px;margin-bottom:4px}
.fx .card span{font-size:13px;color:var(--dim);line-height:1.5}
.fx .step{display:flex;gap:14px;padding:12px 0;border-top:1px solid var(--line)}.fx .step:first-child{border-top:0}
.fx .step .k{flex:0 0 26px;font-weight:800;color:var(--accent)}
.fx .step .b b{font-weight:750}.fx .step .b span{color:var(--dim)}
.fx pre{background:#0f1420;color:#e7e9ee;border-radius:12px;padding:16px 18px;font:13px/1.6 ui-monospace,"JetBrains Mono",monospace;white-space:pre-wrap;margin:8px 0 0}
.cafeslayout{display:flex;gap:26px;align-items:flex-start}
.cafeslist{flex:1;min-width:0}
.toc{flex:0 0 208px;position:sticky;top:0;align-self:flex-start;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:10px 8px;max-height:calc(100vh - 92px);overflow:auto;box-shadow:0 1px 2px rgba(20,25,40,.04)}
.toc .tl{font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--dim);padding:7px 10px 9px}
.toc a{display:block;padding:8px 10px;border-radius:8px;font-size:13px;font-weight:600;color:var(--ink);text-decoration:none;cursor:pointer;line-height:1.35}
.toc a:hover{background:var(--soft);color:var(--accent)}
.toc a .ct{display:block;font-size:11px;font-weight:600;color:var(--dim);margin-top:1px}
.lochead{scroll-margin-top:14px}
@media(max-width:760px){.cafeslayout{flex-direction:column}.toc{position:static;flex:0 0 auto;width:100%;max-height:none;order:-1}}
</style></head><body>
<div class="app"><header class="top"><div class="ttl">☕ <span id="ttl">Cafés</span></div><div class="tabs" id="tabs"></div></header><div class="wrap" id="wrap"></div></div>
<script>
var CAFE=__CAFE__;var EXPLORE_HTML=__EXPLORE__;var NAV_HTML=__NAV__;
(function(){
 var TABS=[["cafes","Cafés"],["districts","Districts"],["explore","How to Explore"],["navigate","Navigate"]];
 function dec(s){try{return decodeURIComponent(s||"");}catch(e){return s||"";}}
 function parseHash(){var raw=(location.hash||"").slice(1);var parts=raw.split("|");return {city:dec(parts[0])||"Delhi", target:dec(parts[1]||"")};}
 var _ph=parseHash(); var city=_ph.city; if(!CAFE[city])city="Delhi";
 var TK="cafe.tab.v1"; var tab="cafes"; try{tab=localStorage.getItem(TK)||"cafes";}catch(e){}
 if(_ph.target)tab="cafes";
 function esc(t){return (t||"").replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c];});}
 document.getElementById("ttl").textContent="Cafés — "+city;
 function renderTabs(){var el=document.getElementById("tabs");el.innerHTML="";TABS.forEach(function(t){var b=document.createElement("button");b.textContent=t[1];if(t[0]===tab)b.className="active";b.onclick=function(){tab=t[0];try{localStorage.setItem(TK,tab);}catch(e){}render();};el.appendChild(b);});}
 var U={};
 function DK(){return "cafe.data.v1."+city;}
 function loadU(){try{U=JSON.parse(localStorage.getItem(DK())||"{}");}catch(e){U={};}U.over=U.over||{};U.added=U.added||{};U.locs=U.locs||[];}
 function saveU(){try{localStorage.setItem(DK(),JSON.stringify(U));}catch(e){}}
 function ok(cl,nm){return cl+"|||"+nm;}
 function getO(cl,nm){return U.over[ok(cl,nm)]||{};}
 function setO(cl,nm,o){U.over[ok(cl,nm)]=o;saveU();}
 function maps(nm,cl){return "https://www.google.com/maps/search/?api=1&query="+encodeURIComponent(nm+", "+cl+", "+city);}
 function cq(s){return (s||"").replace(/"/g,'\\"');}
 function districts(){var d=CAFE[city]||{};var g=d.geo||{};var keys=Object.keys(g);var h="";
   if(d.researched)h+='<div class="note">Researched from web sources — refine as you explore.</div>';
   if(!keys.length)h+='<div class="empty">No localities mapped yet for '+esc(city)+'.</div>';
   keys.forEach(function(k){var v=g[k]||{};h+='<div class="dist"><h3>'+esc(k)+'</h3>'+(v.identity?'<div class="idn">'+esc(v.identity)+'</div>':'')+(v.defines?'<p>'+esc(v.defines)+'</p>':'')+(v.bestFor?'<div class="bf"><b>Best for:</b> '+esc(v.bestFor)+'</div>':'')+'</div>';});
   if(d.scen&&d.scen.length){h+='<div class="lochead">Scenario → best clusters</div><div class="scen">';d.scen.forEach(function(r){h+='<div class="row"><div class="s">'+esc(r[0])+'</div><div class="c">'+esc(r[1])+'</div></div>';});h+='</div>';}
   return h;}
 function seedCafes(cl){var f=(CAFE[city].cafes||[]).filter(function(p){return p[0]===cl;});return f.length?f[0][1]:[];}
 function clusterList(){var out=[];(CAFE[city].cafes||[]).forEach(function(p){if(out.indexOf(p[0])<0)out.push(p[0]);});U.locs.forEach(function(l){if(out.indexOf(l)<0)out.push(l);});Object.keys(U.added).forEach(function(l){if(out.indexOf(l)<0)out.push(l);});return out;}
 function stars(r){var h='<span class="stars">';for(var i=1;i<=5;i++)h+='<span class="st'+(r>=i?' on':'')+'" data-r="'+i+'">★</span>';return h+'</span>';}
 function cafeCard(cl,nm,ff,wi,added){var o=getO(cl,nm);var done=o.v?" done":"";
   return '<div class="cafe'+done+'" data-cl="'+esc(cl)+'" data-nm="'+esc(nm)+'"'+(added?' data-added="1"':'')+'>'
     +'<div class="h"><div class="nm">'+esc(nm)+(added?'<span class="addedtag">yours</span>':'')+'</div>'
     +'<a class="maplink" target="_blank" rel="noopener" href="'+maps(nm,cl)+'">📍 Map</a>'
     +'<button class="vbtn">'+(o.v?"✓ Visited":"Mark visited")+'</button></div>'
     +(ff?'<span class="tag">'+esc(ff)+'</span>':'')+(wi?'<div class="why">'+esc(wi)+'</div>':'')
     +'<div class="meta">'+stars(o.r||0)+'<input class="occ" placeholder="Good for… (occasions, who to go with)" value="'+esc(o.occ||"")+'">'+(added?'<button class="del">Delete</button>':'')+'</div>'
     +'<textarea class="note" placeholder="Your notes — been there? standout dish? rating?">'+esc(o.note||"")+'</textarea></div>';}
 function cafesTab(){var d=CAFE[city]||{};var h="";
   if(d.researched)h+='<div class="note">Researched picks to start — rate them, add occasions &amp; notes, or add your own entries.</div>';
   var cls=clusterList();
   if(!cls.length)h+='<div class="empty">No cafés yet for '+esc(city)+' — add a locality below to begin.</div>';
   cls.forEach(function(cl){h+='<div class="lochead" data-cl="'+esc(cl)+'">'+esc(cl)+'</div>';
     seedCafes(cl).forEach(function(cf){h+=cafeCard(cl,cf[0],cf[1],cf[2]||"",false);});
     (U.added[cl]||[]).forEach(function(cf){h+=cafeCard(cl,cf.n,cf.f||"","",true);});
     h+='<button class="addbtn" data-add="'+esc(cl)+'">＋ Add a café to '+esc(cl)+'</button>';
     h+='<div class="addform" data-form="'+esc(cl)+'"><input class="f-name" placeholder="Café name"><input class="f-fam" placeholder="Famous for / speciality"><input class="f-occ" placeholder="Good for… (occasions)"><button class="f-save" data-save="'+esc(cl)+'">Add café</button></div>';});
   h+='<div class="newloc"><input id="newloc" placeholder="Add a new locality…"><button id="addloc">＋ Locality</button></div>';
   var toc='<div class="tl">Localities</div>';
   if(!cls.length){toc+='<div style="padding:8px 10px;color:var(--dim);font-size:12.5px">None yet</div>';}
   cls.forEach(function(cl){var n=seedCafes(cl).length+((U.added[cl]||[]).length);toc+='<a data-goto="'+esc(cl)+'">'+esc(cl)+'<span class="ct">'+n+' spot'+(n===1?'':'s')+'</span></a>';});
   return '<div class="cafeslayout"><div class="cafeslist">'+h+'</div><aside class="toc">'+toc+'</aside></div>';}
 function render(){renderTabs();var w=document.getElementById("wrap");
   if(tab==="districts")w.innerHTML='<div class="fx">'+districts()+'</div>';
   else if(tab==="cafes")w.innerHTML=cafesTab();
   else if(tab==="explore")w.innerHTML='<div class="fx">'+EXPLORE_HTML+'</div>';
   else w.innerHTML='<div class="fx">'+NAV_HTML+'</div>';}
 var wrap=document.getElementById("wrap");
 wrap.addEventListener("click",function(e){var t=e.target;
   var go=t.closest?t.closest("[data-goto]"):null; if(go){scrollToCluster(go.getAttribute("data-goto"));return;}
   var card=t.closest?t.closest(".cafe"):null;
   if(card&&t.classList&&t.classList.contains("st")){var cl=card.getAttribute("data-cl"),nm=card.getAttribute("data-nm");var r=parseInt(t.getAttribute("data-r"),10);var o=getO(cl,nm);o.r=(o.r===r?0:r);setO(cl,nm,o);render();return;}
   if(card&&t.classList&&t.classList.contains("vbtn")){var a=card.getAttribute("data-cl"),b=card.getAttribute("data-nm");var o2=getO(a,b);o2.v=!o2.v;setO(a,b,o2);render();return;}
   if(card&&t.classList&&t.classList.contains("del")){var a2=card.getAttribute("data-cl"),b2=card.getAttribute("data-nm");U.added[a2]=(U.added[a2]||[]).filter(function(x){return x.n!==b2;});delete U.over[ok(a2,b2)];saveU();render();return;}
   if(t.getAttribute&&t.getAttribute("data-add")!=null){var f=wrap.querySelector('.addform[data-form="'+cq(t.getAttribute("data-add"))+'"]');if(f)f.classList.toggle("open");return;}
   if(t.getAttribute&&t.getAttribute("data-save")!=null){var clr=t.getAttribute("data-save");var f2=wrap.querySelector('.addform[data-form="'+cq(clr)+'"]');if(!f2)return;var nv=f2.querySelector(".f-name").value.trim();if(!nv)return;var fam=f2.querySelector(".f-fam").value.trim();var oc=f2.querySelector(".f-occ").value.trim();U.added[clr]=U.added[clr]||[];U.added[clr].push({n:nv,f:fam});if(oc){var oo=getO(clr,nv);oo.occ=oc;U.over[ok(clr,nv)]=oo;}saveU();render();return;}
   if(t.id==="addloc"){var inp=document.getElementById("newloc");var v=(inp.value||"").trim();if(!v)return;if(clusterList().indexOf(v)<0){U.locs.push(v);U.added[v]=U.added[v]||[];saveU();render();}return;}
 });
 wrap.addEventListener("input",function(e){var t=e.target;var card=t.closest?t.closest(".cafe"):null;if(!card)return;var cl=card.getAttribute("data-cl"),nm=card.getAttribute("data-nm");
   if(t.classList.contains("occ")||t.classList.contains("note")){var o=getO(cl,nm);if(t.classList.contains("occ"))o.occ=t.value;else o.note=t.value;U.over[ok(cl,nm)]=o;clearTimeout(t._t);t._t=setTimeout(saveU,300);}});
 function scrollToCluster(name){if(!name)return;setTimeout(function(){try{var el=wrap.querySelector('.lochead[data-cl="'+cq(name)+'"]');if(el)el.scrollIntoView({behavior:"smooth",block:"start"});}catch(e){}},60);}
 window.addEventListener("hashchange",function(){var ph=parseHash();if(ph.city&&CAFE[ph.city]){city=ph.city;loadU();document.getElementById("ttl").textContent="Cafés — "+city;}if(ph.target)tab="cafes";render();if(ph.target)scrollToCluster(ph.target);});
 loadU();render();if(_ph.target)scrollToCluster(_ph.target);
})();
</script></body></html>"""

def build_cafe_data():
    delhi = json.load(open("/sessions/eloquent-awesome-knuth/mnt/outputs/delhi_cafes.json", encoding="utf-8")); delhi["researched"] = False
    noida = json.load(open("/sessions/eloquent-awesome-knuth/mnt/outputs/noida_cafes.json", encoding="utf-8"))
    ggn   = json.load(open("/sessions/eloquent-awesome-knuth/mnt/outputs/ggn_cafes.json", encoding="utf-8"))
    return {"Delhi": delhi, "Noida": noida, "Gurugram": ggn}

def make_cafe_app():
    cafe = build_cafe_data()
    return (CAFE_APP_TMPL
            .replace("__CAFE__", json.dumps(cafe, ensure_ascii=False))
            .replace("__EXPLORE__", json.dumps(CAFE_EXPLORE_HTML, ensure_ascii=False))
            .replace("__NAV__", json.dumps(CAFE_NAV_HTML, ensure_ascii=False)))

assets["cafe-app.html"] = base64.b64encode(make_cafe_app().encode('utf-8')).decode('ascii')

# Re-build the NCR page now that the cafe app exists: embed a self-contained copy (so Social &
# Chill works even from a local file://) and the raw cafe data (so global search can index it).
_ncr_meta = next((m for m in pages_meta if m["id"] == "ncr"), None)
if _ncr_meta:
    _ncr_raw = (make_ncr_page(NCR_TAXO)
                .replace("__CAFE_DOC__", assets["cafe-app.html"])
                .replace("__CAFE_DATA__", json.dumps(build_cafe_data(), ensure_ascii=False)))
    _ncr_h = inject(_ncr_raw.encode('utf-8'), _ncr_meta["file"], "", True)
    assets[_ncr_meta["file"]] = base64.b64encode(_ncr_h.encode('utf-8')).decode('ascii')

assets_json = json.dumps(assets)
pages_json = json.dumps(pages_meta)
config_json = json.dumps(FIREBASE_CONFIG)

html = r"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Da Vinci</title>
<style>
  :root{
    --bg:#f6f7f9; --sidebar:#ffffff; --sidebar2:#f1f3f6; --panel:#ffffff;
    --ink:#1c2431; --ink-dim:#6b7280; --line:#e7e9ee; --line2:#dcdfe6;
    --accent:#4f46e5; --accent2:#7c6cff; --accent-soft:rgba(79,70,229,.10);
    --hero-grad-a:#1c2431; --hero-grad-b:#4f46e5;
    --home-bg:#f6f7f9; --home-glow1:rgba(79,70,229,.06); --home-glow2:rgba(124,108,255,.06);
    --card-bg:#ffffff; --card-bg2:#ffffff; --shadow:0 1px 2px rgba(20,25,40,.05),0 6px 20px rgba(20,25,40,.05);
    --good:#16a34a; --warn:#b45309; --sidebar-w:280px;
  }
  html[data-theme="dark"]{
    --bg:#0f1115; --sidebar:#151821; --sidebar2:#1b1f2a; --panel:#ffffff;
    --ink:#e7e9ee; --ink-dim:#9aa0ac; --line:#262b38; --line2:#2f3545;
    --accent:#6c8cff; --accent2:#8b6cff; --accent-soft:rgba(108,140,255,.14);
    --hero-grad-a:#ffffff; --hero-grad-b:#b9c2ff;
    --home-bg:#0f1115; --home-glow1:rgba(108,140,255,.10); --home-glow2:rgba(139,108,255,.10);
    --card-bg:rgba(255,255,255,.03); --card-bg2:rgba(255,255,255,.01); --shadow:none;
    --good:#3ecf8e; --warn:#e0a458;
  }
  *{box-sizing:border-box}
  html,body{margin:0;height:100%}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
    background:var(--bg);color:var(--ink);height:100vh;overflow:hidden;display:flex}
  .sidebar{width:var(--sidebar-w);flex:0 0 var(--sidebar-w);background:var(--sidebar);
    border-right:1px solid var(--line);display:flex;flex-direction:column;height:100vh;transition:margin-left .25s ease}
  .sidebar.collapsed{margin-left:calc(var(--sidebar-w) * -1)}
  .brand{display:flex;align-items:center;gap:11px;padding:18px 18px 14px;cursor:pointer;user-select:none}
  .brand .logo{width:34px;height:34px;flex:0 0 34px;border-radius:10px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-size:18px}
  .brand .btext b{display:block;font-size:15px;letter-spacing:-.2px;color:var(--ink)}
  .brand .btext span{display:block;font-size:11px;color:var(--ink-dim);letter-spacing:.4px;text-transform:uppercase;margin-top:1px}
  .side-scroll{flex:1;overflow-y:auto;padding:6px 10px 16px}
  .side-scroll::-webkit-scrollbar{width:8px}
  .side-scroll::-webkit-scrollbar-thumb{background:var(--line2);border-radius:8px}
  .nav-label{font-size:10.5px;text-transform:uppercase;letter-spacing:.12em;color:var(--ink-dim);font-weight:700;padding:12px 12px 6px}
  .item{display:flex;align-items:center;gap:10px;padding:9px 10px;border-radius:10px;cursor:pointer;color:var(--ink-dim);font-size:14px;line-height:1.25;position:relative;user-select:none;border:1px solid transparent;transition:background .12s,color .12s}
  .item:hover{background:var(--sidebar2);color:var(--ink)}
  .item.active{background:var(--accent-soft);color:var(--ink);border-color:var(--accent);font-weight:600}
  .item .ic{font-size:16px;width:22px;text-align:center;flex:0 0 22px}
  .item .nm{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .item .handle{opacity:0;cursor:grab;color:var(--ink-dim);font-size:15px;padding:4px 4px;flex:0 0 auto;touch-action:none}
  .item:hover .handle{opacity:.7}
  .item .handle:hover{opacity:1;color:var(--accent)}
  .item.dragging{opacity:.4}
  .item.drop-target{box-shadow:inset 0 2px 0 var(--accent)}
  .side-foot{padding:12px 16px;border-top:1px solid var(--line);font-size:11px;color:var(--ink-dim);display:flex;align-items:center;gap:6px}
  .dot{width:7px;height:7px;border-radius:50%;background:var(--ink-dim);flex:0 0 7px}
  .dot.ok{background:var(--good)} .dot.warn{background:var(--warn)} .dot.busy{background:var(--accent)}
  .main{flex:1;display:flex;flex-direction:column;height:100vh;min-width:0}
  .topbar{flex:0 0 auto;display:flex;align-items:center;gap:12px;padding:10px 16px;background:var(--sidebar);border-bottom:1px solid var(--line)}
  .iconbtn{width:34px;height:34px;border-radius:9px;border:1px solid var(--line2);background:var(--sidebar2);color:var(--ink);display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:16px}
  .iconbtn:hover{border-color:var(--accent);color:var(--accent)}
  .crumb{font-size:14px;color:var(--ink);font-weight:600}
  .crumb .dim{color:var(--ink-dim);font-weight:500}
  .topbar .spacer{flex:1}
  .open-ext{font-size:12.5px;color:var(--ink-dim);text-decoration:none;padding:7px 11px;border-radius:8px;border:1px solid var(--line2)}
  .open-ext:hover{color:var(--accent);border-color:var(--accent)}
  .stage{flex:1;position:relative;background:var(--panel);min-height:0}
  iframe#viewer{position:absolute;inset:0;width:100%;height:100%;border:0;background:#fff}
  .home{position:absolute;inset:0;overflow-y:auto;background:radial-gradient(1200px 600px at 20% -10%, var(--home-glow1) 0%, transparent 60%),radial-gradient(1000px 500px at 100% 0%, var(--home-glow2) 0%, transparent 55%),var(--home-bg);color:var(--ink);display:none}
  .home.show{display:block}
  .home-inner{max-width:1000px;margin:0 auto;padding:64px 40px 80px}
  .hero-kicker{font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);font-weight:700}
  .hero-h1{font-size:44px;line-height:1.08;letter-spacing:-1px;margin:14px 0 0;font-weight:800;background:linear-gradient(120deg,var(--hero-grad-a),var(--hero-grad-b));-webkit-background-clip:text;background-clip:text;color:transparent}
  .hero-sub{font-size:17px;color:var(--ink-dim);max-width:640px;margin:16px 0 0;line-height:1.6}
  /* ---- manifesto / why ---- */
  .lede{font-size:18px;line-height:1.7;color:var(--ink);max-width:680px;margin:22px 0 0;font-weight:400}
  .lede.dim{color:var(--ink-dim);font-size:16.5px}
  .quote{margin:30px 0 4px;padding:18px 26px;border-left:3px solid var(--accent);background:var(--card-bg);border-radius:0 14px 14px 0;box-shadow:var(--shadow)}
  .quote p{margin:0;font-size:19px;line-height:1.5;font-style:italic;color:var(--ink);font-weight:500;letter-spacing:-.01em}
  .sectlabel{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:52px 0 14px;display:flex;align-items:center;gap:10px}
  .sectlabel::after{content:"";flex:1;height:1px;background:var(--line)}
  .sect-sub{font-size:15px;color:var(--ink-dim);margin:-6px 0 0;max-width:640px;line-height:1.6}
  .prose p{font-size:16px;line-height:1.75;color:var(--ink);max-width:700px;margin:14px 0}
  .prose b{font-weight:700}
  .prose .accent{color:var(--accent);font-weight:600}

  /* ---- pillars diagram ---- */
  .pillars{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:16px 0 0}
  .pillar{border:1px solid var(--line);border-radius:16px;padding:18px 16px;background:linear-gradient(180deg,var(--card-bg),var(--card-bg2));box-shadow:var(--shadow);text-align:left}
  .pillar .pic{font-size:24px}
  .pillar h4{margin:11px 0 4px;font-size:15.5px;font-weight:750;color:var(--ink)}
  .pillar p{margin:0;font-size:13px;line-height:1.5;color:var(--ink-dim)}
  @media(max-width:720px){.pillars{grid-template-columns:1fr 1fr}}

  .creed{margin:16px 0 0;padding:0;list-style:none}
  .creed li{position:relative;padding:8px 0 8px 30px;font-size:15.5px;line-height:1.55;color:var(--ink);max-width:700px;border-bottom:1px solid var(--line)}
  .creed li:last-child{border-bottom:0}
  .creed li::before{content:"→";position:absolute;left:2px;top:8px;color:var(--accent);font-weight:700}
  .creed b{font-weight:700}

  /* ---- featured cornerstone cards ---- */
  .featured-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;margin:16px 0 0;min-height:150px}
  @media(max-width:820px){.featured-grid{grid-template-columns:1fr}}
  .dropzone{border:2px dashed var(--line2);border-radius:16px;display:flex;align-items:center;justify-content:center;text-align:center;color:var(--ink-dim);font-size:13.5px;padding:24px;grid-column:1/-1;min-height:110px}
  .dropzone.over{border-color:var(--accent);background:var(--accent-soft);color:var(--accent)}
  .featured-grid.drop-active,.grid.drop-active{outline:2px dashed var(--accent);outline-offset:6px;border-radius:14px}
  .feat-card{position:relative;overflow:hidden;border:1px solid var(--accent);border-radius:18px;padding:22px 20px 20px;background:linear-gradient(160deg,var(--accent-soft),var(--card-bg) 70%);cursor:pointer;transition:transform .16s,box-shadow .16s}
  .feat-card:hover{transform:translateY(-4px);box-shadow:0 14px 34px rgba(79,70,229,.18)}
  .feat-card .feat-star{position:absolute;top:14px;right:16px;color:#f5a623;font-size:18px;filter:drop-shadow(0 1px 1px rgba(0,0,0,.15))}
  .feat-card .feat-ic{font-size:32px}
  .feat-card .feat-nm{font-size:19px;font-weight:800;letter-spacing:-.02em;margin:12px 0 6px;color:var(--ink)}
  .feat-card .feat-blurb{font-size:14px;line-height:1.55;color:var(--ink-dim);min-height:66px}
  .feat-card .feat-go{margin-top:12px;font-size:13.5px;font-weight:700;color:var(--accent);display:inline-flex;align-items:center;gap:6px}
  .feat-card .fhandle{position:absolute;top:14px;left:16px;opacity:0;cursor:grab;color:var(--ink-dim);font-size:15px;touch-action:none}
  .feat-card:hover .fhandle{opacity:.6}
  .feat-card.dragging{opacity:.4}

  /* ---- sidebar & library stars/blurbs ---- */
  .item .star{color:#f5a623;font-size:12px;flex:0 0 auto;margin-left:2px}
  .card .card-star{position:absolute;top:12px;left:14px;color:#f5a623;font-size:15px}
  .card.is-feat{border-color:var(--accent-line,var(--accent))}
  .card .cblurb{font-size:13px;line-height:1.5;color:var(--ink-dim);margin:6px 0 0}
  .grid-head{display:flex;align-items:baseline;gap:10px;margin:36px 0 0}
  .grid-head h2{margin:0;font-size:15px;text-transform:uppercase;letter-spacing:.1em;color:var(--ink-dim);font-weight:700}
  .grid-head .hint{font-size:12.5px;color:var(--ink-dim);opacity:.8}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;margin:14px 0 0}
  .card{position:relative;border:1px solid var(--line);border-radius:16px;padding:20px;background:linear-gradient(180deg,var(--card-bg),var(--card-bg2));box-shadow:var(--shadow);cursor:pointer;transition:transform .15s,border-color .15s}
  .card:hover{transform:translateY(-3px);border-color:var(--accent)}
  .card.dragging{opacity:.4}
  .card.drop-target{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent-soft)}
  .card .cic{font-size:26px}
  .card .cnm{font-size:16px;font-weight:700;margin:12px 0 4px;color:var(--ink)}
  .card .cgo{font-size:12.5px;color:var(--accent);margin-top:10px;display:inline-flex;align-items:center;gap:5px}
  .card .chandle{position:absolute;top:12px;right:12px;opacity:0;cursor:grab;color:var(--ink-dim);font-size:16px;touch-action:none}
  .card:hover .chandle{opacity:.6}
  .card .chandle:hover{opacity:1;color:var(--accent)}
  @media (max-width:720px){
    .sidebar{position:absolute;z-index:100;box-shadow:0 0 40px rgba(0,0,0,.25)}
    .hero-h1{font-size:32px}.home-inner{padding:40px 22px}
    .item .handle,.card .chandle{opacity:.5}
  }
</style>
</head>
<body>
  <aside class="sidebar" id="sidebar">
    <div class="brand" onclick="showHome()">
      <div class="logo">🎨</div>
      <div class="btext"><b>Da Vinci</b><span>Personal Library</span></div>
    </div>
    <div class="side-scroll">
      <div class="nav-label">Home</div>
      <div class="item" id="home-item" onclick="showHome()"><span class="ic">🏠</span><span class="nm">Home</span></div>
      <div class="nav-label">Pages <span style="font-weight:500;text-transform:none;letter-spacing:0;opacity:.7">· drag to reorder</span></div>
      <div id="nav-list"></div>
    </div>
    <div class="side-foot"><span class="dot" id="foot-dot"></span><span id="foot-sync">Starting…</span></div>
  </aside>
  <div class="main">
    <div class="topbar">
      <div class="iconbtn" onclick="toggleSidebar()" title="Toggle sidebar">☰</div>
      <div class="crumb" id="crumb"><span class="dim">Da Vinci</span></div>
      <div class="spacer"></div>
      <div class="iconbtn" id="theme-btn" onclick="toggleTheme()" title="Toggle light / dark">🌙</div>
      <a class="open-ext" id="open-ext" href="#" target="_blank" rel="noopener" style="display:none">Open in new tab ↗</a>
    </div>
    <div class="stage">
      <div class="home show" id="home">
        <div class="home-inner">
          <div class="hero-kicker">The pursuit of a complete self</div>
          <h1 class="hero-h1">Becoming the fullest version of me.</h1>
          <p class="lede">This isn't a folder of bookmarks. It's the operating system for a life I'm deliberately building — one place where the <span style="color:var(--accent);font-weight:600">mind</span>, the <span style="color:var(--accent);font-weight:600">body</span>, the <span style="color:var(--accent);font-weight:600">craft</span>, and the <span style="color:var(--accent);font-weight:600">character</span> I'm working on all live side by side.</p>

          <div class="quote"><p>“A mind that understands, a body that's capable, a will that acts. When I meet something I don't understand, I go and learn it — I don't complain my way around it.”</p></div>

          <div class="sectlabel">Why this exists</div>
          <div class="prose">
            <p>Scattered notes are scattered attention. Ideas spread across a hundred files are ideas you never return to. I built this so everything I'm learning lives <b>under one roof</b> — somewhere I can actually find it, revisit it, and let the pieces talk to each other.</p>
            <p>Organisation isn't tidiness for its own sake. It's <span class="accent">leverage</span>. A clear structure turns a pile of intentions into a path I can walk — a place to go on the days I feel lost, and a focus on the days I feel scattered.</p>
          </div>

          <div class="sectlabel">The ideal I'm building toward</div>
          <p class="sect-sub">Not one talent taken far, but many woven together — a Renaissance kind of person: understanding, health, skill, and the will to act, deliberately made.</p>
          <div class="pillars">
            <div class="pillar"><div class="pic">🧠</div><h4>A sharp mind</h4><p>Think from first principles. See systems, not just events.</p></div>
            <div class="pillar"><div class="pic">💪</div><h4>A capable body</h4><p>Strength, skill and health that let me act in the world.</p></div>
            <div class="pillar"><div class="pic">📚</div><h4>Deep understanding</h4><p>Know <i>why</i> things work — not merely that they do.</p></div>
            <div class="pillar"><div class="pic">⚡</div><h4>Decisive action</h4><p>Turn understanding into doing. Get real things done.</p></div>
          </div>

          <ul class="creed">
            <li>When I don't understand something, I go <b>learn</b> it — not complain about it.</li>
            <li>Build the <b>body and the mind together</b>; neither one is optional.</li>
            <li>Be genuinely <b>warm</b> and genuinely <b>capable</b> — presence over performance.</li>
            <li>Small, consistent reps beat rare, heroic effort.</li>
            <li><b>Progress, not perfection.</b> Start before I feel ready.</li>
          </ul>

          <div class="sectlabel">In progress ★</div>
          <p class="sect-sub">What I'm actively working on right now. Drag a page up here from the library, and it's automatically starred in the sidebar.</p>
          <div class="featured-grid" id="home-featured"></div>

          <div class="sectlabel">The whole library</div>
          <p class="sect-sub">Everything else. Drag a page up to In progress when you start on it — or back down when you're done.</p>
          <div class="grid" id="home-grid"></div>

          <p class="lede dim" style="margin-top:44px">Everything I'm becoming, gathered in one place. Now — go build. 🛠️</p>
        </div>
      </div>
      <iframe id="viewer" title="Page viewer" style="display:none"></iframe>
    </div>
  </div>

<script id="pages-meta" type="application/json">__PAGES__</script>
<script id="assets-data" type="application/json">__ASSETS__</script>
<script>
(function(){
  "use strict";
  var PAGES=JSON.parse(document.getElementById('pages-meta').textContent);
  var ASSETS=JSON.parse(document.getElementById('assets-data').textContent);
  var FIREBASE_CONFIG=__FIREBASE_CONFIG__;
  var CACHE_KEY='khub.state.v1';
  var byId={}; PAGES.forEach(function(p){ byId[p.id]=p; });

  // Blob resolver shared with embedded pages (so their links/iframes load embedded content)
  var _blobs={};
  window.__HUB_RESOLVE__=function(name){
    if(!name) return null;
    if(_blobs[name]) return _blobs[name];
    var b64=ASSETS[name]; if(!b64) return null;
    try{ var bin=atob(b64),len=bin.length,by=new Uint8Array(len); for(var i=0;i<len;i++)by[i]=bin.charCodeAt(i);
      _blobs[name]=URL.createObjectURL(new Blob([by],{type:'text/html'})); return _blobs[name];
    }catch(e){ return null; }
  };

  function uid(){ return Date.now().toString(36)+Math.random().toString(36).slice(2,7); }
  function escapeHtml(s){ return (s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function normalizeOrder(order){ order=(order||[]).filter(function(id){return byId[id];}); PAGES.forEach(function(p){if(order.indexOf(p.id)<0)order.push(p.id);}); return order; }

  var DEFAULT_PROGRESS = PAGES.filter(function(p){return p.featured;}).map(function(p){return p.id;});
  function isProg(id){ return STATE.progress.indexOf(id)>=0; }
  var STATE;
  (function(){ var s=null; try{s=JSON.parse(localStorage.getItem(CACHE_KEY)||'null');}catch(e){} if(!s||typeof s!=='object')s={};
    STATE={ order:normalizeOrder(s.order||[]), theme:(s.theme==='dark'||s.theme==='light')?s.theme:'light', lastOpen:typeof s.lastOpen==='string'?s.lastOpen:'',
      progress: Array.isArray(s.progress)? s.progress.filter(function(id){return byId[id];}) : DEFAULT_PROGRESS.slice() }; })();
  function cacheLocal(){ try{localStorage.setItem(CACHE_KEY,JSON.stringify(STATE));}catch(e){} }

  var FB={ready:false,ref:null}, applyingRemote=false, saveTimer=null;
  function setSync(status){ var map={connecting:['busy','Connecting…'],saving:['busy','Saving…'],synced:['ok','Synced to cloud'],offline:['warn','Offline · saved locally'],local:['warn','Local only']}; var m=map[status]||['','…']; var sd=document.getElementById('sync-dot'),st=document.getElementById('sync-text'),fd=document.getElementById('foot-dot'),ft=document.getElementById('foot-sync'); if(sd)sd.className='dot '+m[0]; if(st)st.textContent=m[1]; if(fd)fd.className='dot '+m[0]; if(ft)ft.textContent=m[1]; }
  function persist(){ cacheLocal(); if(FB.ready&&!applyingRemote){ setSync('saving'); clearTimeout(saveTimer); saveTimer=setTimeout(function(){ FB.ref.set({order:STATE.order,progress:STATE.progress,theme:STATE.theme,lastOpen:STATE.lastOpen,updatedAt:firebase.firestore.FieldValue.serverTimestamp()},{merge:true}).then(function(){setSync('synced');}).catch(function(){setSync('offline');}); },450); } }
  function bootFirebase(){ try{ if(typeof firebase==='undefined'||!firebase.initializeApp){setSync('local');return;} firebase.initializeApp(FIREBASE_CONFIG); var db=firebase.firestore(); FB.ref=db.collection('hub').doc('state'); FB.ready=true; setSync('connecting');
      FB.ref.onSnapshot(function(snap){ if(!snap.exists){setSync('synced');persist();return;} var d=snap.data()||{}; applyingRemote=true; if(Array.isArray(d.order))STATE.order=normalizeOrder(d.order); if(Array.isArray(d.progress))STATE.progress=d.progress.filter(function(id){return byId[id];}); if(d.theme==='dark'||d.theme==='light'){STATE.theme=d.theme;applyTheme(d.theme);} if(typeof d.lastOpen==='string')STATE.lastOpen=d.lastOpen; cacheLocal(); render(); applyingRemote=false; setSync('synced'); }, function(){setSync('offline');});
    }catch(e){ setSync('local'); } }
  function initFirebase(){
    // Load Firebase lazily AFTER the app has rendered, so a slow or blocked CDN
    // can never stall the page (empty sidebar / stuck "Starting..."). Falls back to local-only.
    if(typeof firebase!=='undefined'&&firebase.initializeApp){ bootFirebase(); return; }
    setSync('connecting');
    var base="https://www.gstatic.com/firebasejs/10.12.2/";
    var done=false, failed=function(){ if(done)return; done=true; setSync('local'); };
    var to=setTimeout(failed,8000);
    function load(src,cb){ var s=document.createElement('script'); s.src=src; s.async=true; s.onload=cb; s.onerror=failed; document.head.appendChild(s); }
    load(base+"firebase-app-compat.js", function(){
      load(base+"firebase-firestore-compat.js", function(){ if(done)return; done=true; clearTimeout(to); bootFirebase(); });
    });
  }

  function applyTheme(t){ document.documentElement.setAttribute('data-theme',t); var b=document.getElementById('theme-btn'); b.textContent=(t==='dark'?'☀️':'🌙'); b.title=(t==='dark'?'Switch to light':'Switch to dark'); }
  window.toggleTheme=function(){ STATE.theme=(STATE.theme==='light'?'dark':'light'); applyTheme(STATE.theme); persist(); };

  var viewer=document.getElementById('viewer'),home=document.getElementById('home'),crumb=document.getElementById('crumb'),openExt=document.getElementById('open-ext');
  window.showHome=function(){ STATE.lastOpen=''; persist(); home.classList.add('show'); viewer.style.display='none'; crumb.innerHTML='<span class="dim">Da Vinci</span>'; openExt.style.display='none'; document.getElementById('home-item').classList.add('active'); document.querySelectorAll('#nav-list .item').forEach(function(el){el.classList.remove('active');}); };
  window.openPage=function(id){ var p=byId[id]; if(!p)return; STATE.lastOpen=id; persist(); var url=window.__HUB_RESOLVE__(p.file); if(!url)return; viewer.src=url; viewer.style.display='block'; home.classList.remove('show'); crumb.innerHTML='<span class="dim">Da Vinci &nbsp;/&nbsp;</span> '+p.icon+' '+escapeHtml(p.name); openExt.style.display='inline-block'; openExt.href=url; document.getElementById('home-item').classList.remove('active'); document.querySelectorAll('#nav-list .item').forEach(function(el){el.classList.toggle('active',el.getAttribute('data-id')===id);}); };
  window.toggleSidebar=function(){ document.getElementById('sidebar').classList.toggle('collapsed'); };

  function render(){
    var list=document.getElementById('nav-list'), grid=document.getElementById('home-grid'), feat=document.getElementById('home-featured');
    list.innerHTML=''; grid.innerHTML=''; if(feat)feat.innerHTML='';
    var inprog=STATE.order.filter(function(id){return isProg(id);});
    var lib=STATE.order.filter(function(id){return !isProg(id);});
    inprog.forEach(function(id){ var p=byId[id];
      var c=document.createElement('div'); c.className='feat-card'; c.setAttribute('data-id',id); c.setAttribute('draggable','true');
      c.innerHTML='<div class="feat-star">★</div><span class="fhandle" title="Drag">⠿</span><div class="feat-ic">'+p.icon+'</div><div class="feat-nm">'+escapeHtml(p.name)+'</div><div class="feat-blurb">'+escapeHtml(p.blurb||'')+'</div><div class="feat-go">Enter&nbsp;→</div>';
      c.addEventListener('click',function(e){ if(e.target.classList.contains('fhandle'))return; openPage(id); });
      feat.appendChild(c);
    });
    if(!inprog.length){ var dz=document.createElement('div'); dz.className='dropzone'; dz.textContent='Nothing in progress yet — drag a page up here to start on it.'; feat.appendChild(dz); }
    lib.forEach(function(id){ var p=byId[id];
      var card=document.createElement('div'); card.className='card'; card.setAttribute('data-id',id); card.setAttribute('draggable','true');
      card.innerHTML='<span class="chandle" title="Drag">⠿</span><div class="cic">'+p.icon+'</div><div class="cnm">'+escapeHtml(p.name)+'</div><div class="cblurb">'+escapeHtml(p.blurb||'')+'</div><div class="cgo">Open&nbsp;→</div>';
      card.addEventListener('click',function(e){ if(e.target.classList.contains('chandle'))return; openPage(id); });
      grid.appendChild(card);
    });
    if(!lib.length){ var dz2=document.createElement('div'); dz2.className='dropzone'; dz2.textContent='Everything is in progress — drag a page back down here.'; grid.appendChild(dz2); }
    STATE.order.forEach(function(id){ var p=byId[id]; var star=isProg(id)?'<span class="star" title="In progress">★</span>':'';
      var el=document.createElement('div'); el.className='item'; el.setAttribute('data-id',id); el.setAttribute('draggable','true');
      el.innerHTML='<span class="ic">'+p.icon+'</span><span class="nm">'+escapeHtml(p.name)+'</span>'+star+'<span class="handle" title="Drag to reorder">⠿</span>';
      el.addEventListener('click',function(e){ if(e.target.classList.contains('handle'))return; openPage(id); });
      list.appendChild(el);
    });
    setupContainers(); cardDnD(feat); cardDnD(grid); cardTouch(); sidebarDnD(list);
    var cur=STATE.lastOpen; document.querySelectorAll('#nav-list .item').forEach(function(el){el.classList.toggle('active',cur&&el.getAttribute('data-id')===cur);});
  }

  /* ---- home two-bucket drag: move pages between In progress and the library ---- */
  var dragId=null, sdragEl=null, containersReady=false;
  function clearTargets(){ document.querySelectorAll('.drop-target,.drop-active').forEach(function(x){x.classList.remove('drop-target','drop-active');}); }
  function nearestCard(container,y,x){
    var cards=Array.prototype.filter.call(container.children,function(c){return c.getAttribute('data-id')&&c.getAttribute('data-id')!==dragId;});
    for(var i=0;i<cards.length;i++){ var r=cards[i].getBoundingClientRect(); if(y<r.top+r.height/2){return cards[i];} if(y<=r.bottom && x<r.left+r.width/2){return cards[i];} }
    return null;
  }
  function moveCard(id,toProgress,beforeId){
    STATE.progress=STATE.progress.filter(function(x){return x!==id;});
    if(toProgress) STATE.progress.push(id);
    STATE.order=STATE.order.filter(function(x){return x!==id;});
    var idx = beforeId ? STATE.order.indexOf(beforeId) : STATE.order.length;
    if(idx<0) idx=STATE.order.length;
    STATE.order.splice(idx,0,id);
    persist(); render();
  }
  function setupContainers(){
    if(containersReady) return; containersReady=true;
    [['home-featured',true],['home-grid',false]].forEach(function(pair){
      var container=document.getElementById(pair[0]); if(!container) return; var toProg=pair[1];
      container.addEventListener('dragover',function(e){ if(!dragId)return; e.preventDefault(); e.dataTransfer.dropEffect='move'; container.classList.add('drop-active'); });
      container.addEventListener('dragleave',function(e){ if(e.target===container) container.classList.remove('drop-active'); });
      container.addEventListener('drop',function(e){ if(!dragId)return; e.preventDefault(); var b=nearestCard(container,e.clientY,e.clientX); container.classList.remove('drop-active'); moveCard(dragId,toProg,b?b.getAttribute('data-id'):null); });
    });
  }
  function cardDnD(container){ Array.prototype.forEach.call(container.children,function(el){ if(!el.getAttribute('data-id'))return;
      el.addEventListener('dragstart',function(e){dragId=el.getAttribute('data-id');el.classList.add('dragging');e.dataTransfer.effectAllowed='move';try{e.dataTransfer.setData('text/plain',dragId);}catch(_){}});
      el.addEventListener('dragend',function(){el.classList.remove('dragging');clearTargets();dragId=null;});
    }); }
  function cardTouch(){
    document.querySelectorAll('#home-featured [data-id] .fhandle, #home-grid [data-id] .chandle').forEach(function(h){
      h.addEventListener('touchstart',function(ev){ ev.preventDefault(); var card=h.closest('[data-id]'); dragId=card.getAttribute('data-id'); card.classList.add('dragging');
        function move(e){ e.preventDefault(); }
        function end(e){ var t=e.changedTouches[0]; var el=t?document.elementFromPoint(t.clientX,t.clientY):null; var cont=el&&el.closest?el.closest('#home-featured,#home-grid'):null; card.classList.remove('dragging'); document.removeEventListener('touchmove',move); document.removeEventListener('touchend',end); if(cont){ var b=nearestCard(cont,t.clientY,t.clientX); moveCard(dragId, cont.id==='home-featured', b?b.getAttribute('data-id'):null); } else { dragId=null; } }
        document.addEventListener('touchmove',move,{passive:false}); document.addEventListener('touchend',end);
      },{passive:false});
    });
  }
  /* ---- sidebar reorder (reorders STATE.order only) ---- */
  function sidebarDnD(container){
    Array.prototype.forEach.call(container.children,function(el){
      el.addEventListener('dragstart',function(e){sdragEl=el;el.classList.add('dragging');e.dataTransfer.effectAllowed='move';try{e.dataTransfer.setData('text/plain',el.getAttribute('data-id'));}catch(_){}});
      el.addEventListener('dragend',function(){el.classList.remove('dragging');clearTargets();sdragEl=null;});
      el.addEventListener('dragover',function(e){if(!sdragEl)return;e.preventDefault();if(el===sdragEl)return;clearTargets();el.classList.add('drop-target');});
      el.addEventListener('dragleave',function(){el.classList.remove('drop-target');});
      el.addEventListener('drop',function(e){if(!sdragEl||el===sdragEl)return;e.preventDefault();var nodes=Array.prototype.slice.call(container.children);var from=nodes.indexOf(sdragEl),to=nodes.indexOf(el);if(from<to)container.insertBefore(sdragEl,el.nextSibling);else container.insertBefore(sdragEl,el);el.classList.remove('drop-target');STATE.order=Array.prototype.slice.call(container.children).map(function(x){return x.getAttribute('data-id');});persist();render();});
      var handle=el.querySelector('.handle'); if(handle){ handle.addEventListener('touchstart',function(ev){ev.preventDefault();var moving=el;moving.classList.add('dragging');
        function at(y){var kids=Array.prototype.slice.call(container.children);for(var i=0;i<kids.length;i++){var k=kids[i];if(k===moving)continue;var r=k.getBoundingClientRect();if(y<r.top+r.height/2)return k;}return null;}
        function move(e){var t=e.touches[0];if(!t)return;e.preventDefault();var before=at(t.clientY);if(before)container.insertBefore(moving,before);else container.appendChild(moving);}
        function end(){moving.classList.remove('dragging');document.removeEventListener('touchmove',move);document.removeEventListener('touchend',end);STATE.order=Array.prototype.slice.call(container.children).map(function(x){return x.getAttribute('data-id');});persist();render();}
        document.addEventListener('touchmove',move,{passive:false});document.addEventListener('touchend',end);
      },{passive:false}); }
    });
  }

  applyTheme(STATE.theme);
  render();
  if(STATE.lastOpen && byId[STATE.lastOpen]) openPage(STATE.lastOpen); else showHome();
  initFirebase();
})();
</script>
</body>
</html>
"""

html = (html.replace("__PAGES__", pages_json)
            .replace("__ASSETS__", assets_json)
            .replace("__FIREBASE_CONFIG__", config_json))
with open(OUT, "w", encoding="utf-8") as f: f.write(html)
with open(OUT_INDEX, "w", encoding="utf-8") as f: f.write(html)
print("Embedded files:", len(assets), "| sidebar pages:", len(pages_meta))
print("Wrote %.1f KB" % (os.path.getsize(OUT)/1024))
