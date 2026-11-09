from mk_common import *
def cover(w=420,h=594):
    return f'''<div class="cover" style="width:{w}px;height:{h}px">
<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="position:absolute;inset:0"><defs><linearGradient id="cg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1F3A2B"/><stop offset="1" stop-color="#0F1E16"/></linearGradient></defs>
<rect width="{w}" height="{h}" fill="url(#cg)"/>{bokeh(w,h,22,12,col="#E3C77A",rmax=34,amax=.12)}</svg>
<img class="foil" src="{SV}piste05_arcade_couleur.svg" style="position:absolute;left:50px;top:150px;width:320px;filter:drop-shadow(0 1px 0 rgba(255,235,170,.35)) drop-shadow(0 -1px 0 rgba(0,0,0,.6)) brightness(1.15)"></div>'''
cov_neg=f'''<div class="cover" style="width:420px;height:594px"><svg viewBox="0 0 420 594" width="420" height="594" style="position:absolute;inset:0"><defs><linearGradient id="cg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1F3A2B"/><stop offset="1" stop-color="#0F1E16"/></linearGradient></defs><rect width="420" height="594" fill="url(#cg)"/>{bokeh(420,594,22,12,rmax=34,amax=.12)}</svg>
<img src="{SV}piste05_arcade_negatif-transparent.svg" style="position:absolute;left:50px;top:170px;width:320px;filter:drop-shadow(0 1px 0 rgba(255,235,170,.3)) drop-shadow(0 -1px 0 rgba(0,0,0,.6))">
<div style="position:absolute;left:0;right:0;top:468px;text-align:center;font-family:Cormorant;font-style:italic;font-weight:300;font-size:30px;color:#F4ECDB">Saison 2026</div>
<div style="position:absolute;left:0;right:0;top:512px;text-align:center;font-family:Jost;font-size:10px;letter-spacing:4px;color:#D8B766">PROGRAMME · BULLES · CANAUX</div></div>'''
left=f'''<div class="pg left"><svg viewBox="0 0 400 560" width="400" height="560" style="position:absolute;inset:0"><rect width="400" height="560" fill="#16291F"/>{bokeh(400,560,18,21,rmax=40,amax=.14)}{arches(60,520,.7,op=.35)}</svg>
<div style="position:absolute;left:38px;right:38px;top:62px;color:#F4ECDB;font-family:Cormorant;font-weight:300;font-style:italic;font-size:38px;line-height:1.08">Entre canaux<br>et jardins,<br>la fête<br>pétille.</div>
<img src="{SV}piste01_plaque_sceau-simple_negatif-transparent.svg" style="position:absolute;left:38px;bottom:34px;width:70px"></div>'''
def ev(d,m,t,s): return f'<div class="ev"><div class="d">{d}<small>{m}</small></div><div><b>{t}</b><span>{s}</span></div></div>'
right=f'''<div class="pg right" style="background:#F4ECDB"><div style="padding:48px 40px 0"><div class="kick">AU PROGRAMME</div><h2>Les temps forts<br>de la saison</h2>
{ev("14","JUIN","Nuit des Bulles","Dégustations et lumières sur les quais")}{ev("28","JUIN","Balade du Jard","Parcours commenté, goûter champenois")}{ev("12","JUIL.","Soirée au fil de l’eau","Musique et feux sur le canal")}{ev("06","SEPT.","Marché des vignerons","Rencontres et accords gourmands")}
</div><div style="position:absolute;left:40px;right:40px;bottom:30px;border-top:1px solid #C9A24B;padding-top:10px;font-family:Jost;font-size:9px;letter-spacing:2.5px;color:#8B6420;display:flex;justify-content:space-between"><span>CHÂLONS CHAMPAGNES ÉVENTS</span><span>04</span></div></div>'''
html=f'''<html><head><meta charset=utf-8><style>{FONTCSS}
body{{margin:0;width:1500px;height:1000px;position:relative;overflow:hidden;background:#D8D0BF;font-family:Jost}}
.tex{{position:absolute;inset:0}}
.cover,.pg{{position:absolute;overflow:hidden}}
.cover{{box-shadow:0 30px 50px -10px rgba(0,0,0,.45),0 6px 12px rgba(0,0,0,.25);border-radius:2px 5px 5px 2px}}
.pg{{width:400px;height:560px}}.left{{border-radius:2px 0 0 2px}}.right{{border-radius:0 2px 2px 0}}
.spread{{position:absolute;left:640px;top:250px;width:800px;height:560px;transform:rotate(3deg);box-shadow:0 28px 46px -8px rgba(0,0,0,.4),0 6px 10px rgba(0,0,0,.2)}}
.spread:after{{content:"";position:absolute;left:380px;width:40px;top:0;bottom:0;background:linear-gradient(90deg,rgba(0,0,0,0),rgba(0,0,0,.2) 50%,rgba(0,0,0,0));z-index:5}}
.kick{{font-size:10px;letter-spacing:4px;color:#8B6420}}h2{{font-family:Cormorant;font-weight:400;font-size:36px;line-height:1.05;margin:10px 0 26px;color:#16291F}}
.ev{{display:flex;gap:18px;margin-bottom:20px;align-items:center}}.ev .d{{font-family:Cormorant;font-size:42px;font-weight:500;color:#16291F;width:62px;line-height:.9;text-align:center}}.ev .d small{{display:block;font-family:Jost;font-size:9px;letter-spacing:2px;color:#8B6420;margin-top:4px}}
.ev b{{display:block;font-family:Cormorant;font-size:21px;font-weight:600;color:#16291F}}.ev span{{font-size:12px;color:#4a5a50}}
.note{{position:absolute;left:0;right:0;bottom:18px;text-align:center;font-size:13px;color:#6b6556}}
</style></head><body>
<svg class="tex" width="1500" height="1000"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 .3  0 0 0 0 .27  0 0 0 0 .2  0 0 0 .09 0"/></filter><rect width="1500" height="1000" filter="url(#n)"/></svg>
<div class="spread">{left}<div class="pg right" style="left:400px">{right[len('<div class="pg right" style="background:#F4ECDB">'):-6]}</div></div>
<div style="position:absolute;left:150px;top:150px;transform:rotate(-5deg)">{cov_neg}</div>
<div class="note">Maquette brochure A5 — contenus et dates fictifs, visuels illustrés · logo en négatif crème sur vert bouteille</div></body></html>'''
open("brochure.html","w").write(html)
