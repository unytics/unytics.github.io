# -*- coding: utf-8 -*-
"""Assemble the deck into one standalone HTML presentation: index.html, next to this script.

Sources (in deck/): deck.json and slides/<id>.html, as saved by the Claude Slides artifact
https://claude.ai/artifact/Mif2zaVnf5VkZiy8hGsuem (project/deck.json and project/slides/).
After editing the deck in Claude, copy its files into deck/ again, then run:

    uv run --no-project python src/blog/fr/forward-data-conference-2026/assemble.py
    uv run build.py

build.py copies index.html to /blog/fr/forward-data-conference-2026/ (deck/, *.md and *.py are not published).
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DECK = HERE / "deck"
URL = "https://unytics.io/blog/fr/forward-data-conference-2026/"

# Images uploaded to the artifact -> their copy in the site's /assets/
BLOBS = {
    "/_blob/a248c08f2f3169df624df80e6286d25d": "/assets/paul_photo.jpg",
    "/_blob/ad257a649f09457310ddea771c588e1b": "/assets/qr_linkedin.png",
}

DESCRIPTION = ("Talk de Paul Marcombes à la Forward Data Conference 2026 : chez Optic 2000, le conversationnel est "
               "mis au début de la chaîne, dans l'éditeur de code, et 25 contributeurs, en majorité des métiers, "
               "construisent la data platform.")
FONTS = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700"
         "&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@400..700&display=swap")

PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__ | Unytics</title>
<meta name="description" content="__DESC__">
<link rel="canonical" href="__URL__">
<meta property="og:type" content="website">
<meta property="og:url" content="__URL__">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:site_name" content="Unytics">
<meta property="og:locale" content="fr_FR">
<meta property="og:image" content="https://unytics.io/assets/unytics_social_image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="author" content="Paul Marcombes">
<link rel="icon" href="/assets/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="__FONTS__">
<script async src="https://plausible.io/js/pa-YHunZhK65WvaJpQXfwUD_.js"></script>
<script>window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},plausible.init=plausible.init||function(i){plausible.o=i||{}};plausible.init()</script>
<style>
*,*::before,*::after{box-sizing:border-box}
html,body{margin:0;height:100%;background:#0B1120;overflow:hidden;font-family:'Inter',Arial,sans-serif}
#stage{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
#deck{position:relative;width:1920px;height:1080px;flex:none;transform-origin:center center;box-shadow:0 20px 60px rgba(0,0,0,.45)}
#deck section{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:hidden;opacity:0;visibility:hidden;transition:opacity .45s ease,visibility 0s linear .45s}
#deck section.active{opacity:1;visibility:visible;transition:opacity .45s ease}
#deck section.instant{transition:none}
#deck h1,#deck h2,#deck h3,#deck p,#deck ul,#deck ol{margin:0}
#deck img{display:block}
#deck aside{display:none}
#deck [data-build-in]{opacity:0;transform:translateY(12px);transition:opacity .5s ease,transform .5s ease}
#deck [data-build-in].shown{opacity:1;transform:none}
#deck .magic{transition:transform .7s cubic-bezier(.4,0,.2,1)}
#bar{position:fixed;left:0;bottom:0;height:4px;background:#2563EB;transition:width .3s;z-index:3}
#ui{position:fixed;right:16px;bottom:14px;display:flex;gap:8px;align-items:center;z-index:3;font-size:13px;color:#94A3B8;opacity:.25;transition:opacity .3s}
#ui:hover{opacity:1}
#ui button,#ui a{background:#1E293B;color:#E2E8F0;border:1px solid #334155;border-radius:8px;padding:6px 10px;font:inherit;cursor:pointer;text-decoration:none}
#ui button:hover,#ui a:hover{background:#334155}
#notes{position:fixed;left:0;right:0;bottom:0;max-height:38vh;overflow:auto;background:rgba(15,23,42,.96);color:#E2E8F0;padding:20px 24px 56px;font-size:17px;line-height:1.55;display:none;z-index:2;border-top:1px solid #334155}
#notes.open{display:block}
#notes b{color:#60A5FA;font-weight:600}
#hint{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:rgba(15,23,42,.92);color:#E2E8F0;border:1px solid #334155;border-radius:10px;padding:10px 16px;font-size:14px;z-index:4;transition:opacity .6s}
#hint.gone{opacity:0;pointer-events:none}
</style>
</head>
<body>
<div id="stage"><div id="deck">
__SLIDES__
</div></div>
<div id="bar"></div>
<div id="notes" aria-live="polite"></div>
<div id="ui">
<span id="count"></span>
<button id="prev" aria-label="Slide précédente">&larr;</button>
<button id="next" aria-label="Slide suivante">&rarr;</button>
<button id="nbtn" aria-label="Afficher les notes">Notes</button>
<button id="fbtn" aria-label="Plein écran">Plein écran</button>
<a href="/blog/fr/">Blog</a>
</div>
<div id="hint">&larr; &rarr; ou clic pour avancer &middot; N : notes de l’orateur &middot; F : plein écran</div>
<script>
(function(){
  var deck=document.getElementById('deck'),S=[].slice.call(deck.querySelectorAll(':scope > section'));
  var cur=0,step=0,notes=document.getElementById('notes');
  function builds(s){var o={};[].forEach.call(s.querySelectorAll('[data-build-in]'),function(e){var n=parseInt((e.getAttribute('data-build-in').match(/\\d+/)||[1])[0],10);(o[n]=o[n]||[]).push(e)});return Object.keys(o).map(Number).sort(function(a,b){return a-b}).map(function(k){return o[k]})}
  var B=S.map(builds);
  function fit(){var k=Math.min(innerWidth/1920,innerHeight/1080);deck.style.transform='scale('+k+')'}
  function setStep(i,n){B[i].forEach(function(g,j){g.forEach(function(e){e.classList.toggle('shown',j<n)})})}
  function renderNotes(){var a=S[cur].querySelector('aside');var t=a?a.textContent:'';notes.innerHTML='<div style="max-width:1100px;margin:0 auto"><div style="color:#94A3B8;font-size:13px;margin-bottom:6px">Slide '+(cur+1)+' / '+S.length+'</div>'+t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/\\[clic\\]/g,'<b>[clic]</b>')+'</div>'}
  function magic(from,to){
    if(S[from].getAttribute('data-transition')!=='magic'||to!==from+1)return;
    var k=deck.getBoundingClientRect().width/1920;
    [].forEach.call(S[to].querySelectorAll('[id]'),function(e){
      var a=S[from].querySelector('#'+CSS.escape(e.id));if(!a)return;
      var r1=a.getBoundingClientRect(),r2=e.getBoundingClientRect();if(!r2.width||!r2.height)return;
      var dx=(r1.left-r2.left)/k,dy=(r1.top-r2.top)/k,sx=r1.width/r2.width,sy=r1.height/r2.height;
      e.classList.remove('magic');e.style.transformOrigin='0 0';e.style.transform='translate('+dx+'px,'+dy+'px) scale('+sx+','+sy+')';
      e.getBoundingClientRect();e.classList.add('magic');e.style.transform='';
      setTimeout(function(){e.classList.remove('magic');e.style.transformOrigin=''},800);
    });
  }
  function show(i,n,dir){
    i=Math.max(0,Math.min(S.length-1,i));var prev=cur;
    if(i!==prev){S[i].classList.add('active');if(dir>0)magic(prev,i);S[prev].classList.remove('active')}
    cur=i;step=n;setStep(cur,step);
    document.getElementById('count').textContent=(cur+1)+' / '+S.length;
    document.getElementById('bar').style.width=((cur+1)/S.length*100)+'%';
    history.replaceState(null,'','#slide-'+(cur+1));
    renderNotes();
  }
  function next(){if(step<B[cur].length)show(cur,step+1,0);else if(cur<S.length-1)show(cur+1,0,1)}
  function prev(){if(cur>0)show(cur-1,B[cur-1].length,-1);else show(0,0,0)}
  function toggleNotes(){notes.classList.toggle('open')}
  function fs(){if(!document.fullscreenElement)document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen();else document.exitFullscreen()}
  addEventListener('keydown',function(e){
    if(e.metaKey||e.ctrlKey||e.altKey)return;var k=e.key;
    if(k==='ArrowRight'||k===' '||k==='PageDown'||k==='Enter'){e.preventDefault();next()}
    else if(k==='ArrowLeft'||k==='PageUp'||k==='Backspace'){e.preventDefault();prev()}
    else if(k==='Home')show(0,0,0);else if(k==='End')show(S.length-1,B[S.length-1].length,0);
    else if(k==='n'||k==='N')toggleNotes();else if(k==='f'||k==='F')fs();
    hideHint();
  });
  document.getElementById('stage').addEventListener('click',function(e){if(e.target.closest('a'))return;(e.clientX<innerWidth/4?prev:next)();hideHint()});
  document.getElementById('next').onclick=function(){next()};document.getElementById('prev').onclick=function(){prev()};
  document.getElementById('nbtn').onclick=toggleNotes;document.getElementById('fbtn').onclick=fs;
  var tx=null;addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});
  addEventListener('touchend',function(e){if(tx===null)return;var d=e.changedTouches[0].clientX-tx;if(Math.abs(d)>40)(d<0?next:prev)();tx=null},{passive:true});
  var hint=document.getElementById('hint');function hideHint(){hint.classList.add('gone')}setTimeout(hideHint,6000);
  addEventListener('resize',fit);fit();
  var m=location.hash.match(/slide-(\\d+)/),start=m?parseInt(m[1],10)-1:0;
  S.forEach(function(s){s.classList.add('instant')});cur=start;S[start]&&S[start].classList.add('active');show(start,0,0);
  setTimeout(function(){S.forEach(function(s){s.classList.remove('instant')})},50);
})();
</script>
</body>
</html>
"""


def main() -> None:
    index = json.loads((DECK / "deck.json").read_text(encoding="utf-8"))
    slides = []
    for sid in index["order"]:
        s = (DECK / "slides" / f"{sid}.html").read_text(encoding="utf-8").strip()
        for blob, path in BLOBS.items():
            s = s.replace(blob, path)
        if "/_blob/" in s:
            raise SystemExit(f"{sid}: image uploaded to the artifact with no copy in /assets/ (add it to BLOBS)")
        slides.append(s)

    page = (PAGE.replace("__TITLE__", html.escape(index["title"])).replace("__DESC__", html.escape(DESCRIPTION))
            .replace("__URL__", URL).replace("__FONTS__", FONTS).replace("__SLIDES__", "\n".join(slides)))
    out = HERE / "index.html"
    out.write_text(page, encoding="utf-8", newline="\n")
    print(f"{len(slides)} slides -> {out} ({len(page) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
