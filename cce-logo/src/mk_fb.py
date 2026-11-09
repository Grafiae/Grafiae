from mk_common import *
cover=f'''<svg viewBox="0 0 1000 380" width="1000" height="380" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#21402F"/><stop offset="1" stop-color="#0E1B14"/></linearGradient>
<radialGradient id="h" cx=".78" cy=".3" r=".6"><stop offset="0" stop-color="#E3C77A" stop-opacity=".35"/><stop offset="1" stop-color="#E3C77A" stop-opacity="0"/></radialGradient></defs>
<rect width="1000" height="380" fill="url(#g)"/><rect width="1000" height="380" fill="url(#h)"/>
{bokeh(1000,380,34,5)}
{arches(560,380,.82)}
<g font-family="Cormorant" fill="#F4ECDB"><text x="64" y="156" font-size="58" font-weight="300" font-style="italic">Les rendez-vous</text><text x="64" y="216" font-size="58" font-weight="300" font-style="italic">qui pétillent.</text></g>
<text x="66" y="262" font-family="Jost" font-size="15" letter-spacing="4" fill="#D8B766">CHÂLONS-EN-CHAMPAGNE · TOUTE L’ANNÉE</text>
</svg>'''
def post(img,txt,date,likes="J’aime   Commenter   Partager"):
    return f'''<div class="post"><div class="ph"><img class="av" src="{SV}piste01_plaque_sceau-simple_couleur.svg"><div><b>Châlons Champagnes Évents</b><span>{date} · 🌐</span></div></div>
    <p>{txt}</p>{img}<div class="act">{likes}</div></div>'''
sq=f'''<div class="vis sq" style="background:linear-gradient(160deg,#F4ECDB,#EADFC4)"><img src="{SV}piste05_arcade_symbole_couleur.svg" style="width:66%"><div class="cap">Nuit des Bulles<small>SAMEDI 14 JUIN · 20 H · QUAIS DU CANAL</small></div></div>'''
dk=f'''<div class="vis wide" style="background:radial-gradient(circle at 80% 20%,#2D5240,#0E1B14 70%)"><svg viewBox="0 0 600 315" width="100%" style="position:absolute;inset:0">{bokeh(600,315,22,9,rmax=30)}</svg>
<div style="position:relative;padding:36px 40px;color:#F4ECDB"><img src="{SV}piste05_arcade_negatif-transparent.svg" style="width:150px"><div class="t">Programme<br>d’été</div><small>JUIN → SEPTEMBRE</small></div></div>'''
html=f'''<html><head><meta charset=utf-8><style>{FONTCSS}
body{{margin:0;background:#E4E6EA;font-family:Jost,sans-serif;color:#1c1e21;width:1100px}}
.wrap{{width:1000px;margin:0 auto;padding:40px 0 60px}}
.card{{position:relative;background:#fff;border-radius:10px;box-shadow:0 1px 3px rgba(0,0,0,.15);overflow:hidden}}
.head{{position:relative}}.avatar{{position:absolute;left:40px;top:296px;width:176px;height:176px;border-radius:50%;border:6px solid #fff;background:#F4ECDB;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.25)}}
.avatar img{{width:100%;height:100%;display:block}}
.id{{padding:16px 40px 0 244px;height:110px}}.id h1{{margin:0;font-size:30px;font-weight:600}}.id p{{margin:4px 0 0;color:#65676b;font-size:15px}}
.btn{{position:absolute;right:30px;top:402px;display:flex;gap:10px}}.btn span{{background:#16291F;color:#F4ECDB;padding:9px 20px;border-radius:6px;font-weight:500;font-size:15px}}.btn span.l{{background:#E4E6EA;color:#1c1e21}}
.tabs{{border-top:1px solid #dadde1;margin:0 30px;display:flex;gap:28px;font-size:15px;font-weight:500;color:#65676b;padding:14px 0}}.tabs .on{{color:#16291F;border-bottom:3px solid #16291F;padding-bottom:11px;margin-bottom:-14px}}
.grid{{display:grid;grid-template-columns:330px 1fr;gap:18px;margin-top:18px}}.side{{align-self:start;padding:20px;font-size:15px;line-height:1.5}}.side h3{{margin:0 0 8px;font-size:19px}}
.post{{padding:0 0 10px;margin-bottom:18px}}.ph{{display:flex;gap:10px;align-items:center;padding:14px 16px}}.ph .av{{width:42px;height:42px;border-radius:50%}}.ph b{{display:block;font-size:15px}}.ph span{{font-size:12.5px;color:#65676b}}
.post p{{margin:0 16px 12px;font-size:15.5px;line-height:1.45}}.act{{border-top:1px solid #dadde1;margin:10px 16px 0;padding-top:10px;color:#65676b;font-size:14px;font-weight:500;white-space:pre}}
.vis{{position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center}}.sq{{aspect-ratio:1/1;flex-direction:column}}.wide{{aspect-ratio:1.905/1;justify-content:flex-start}}
.cap{{position:absolute;left:0;right:0;bottom:30px;text-align:center;font-family:Cormorant;font-size:34px;font-weight:500;color:#16291F}}.cap small{{display:block;font-family:Jost;font-size:12px;letter-spacing:3.5px;color:#8B6420;margin-top:4px}}
.t{{font-family:Cormorant;font-size:54px;font-weight:300;font-style:italic;line-height:1;margin-top:16px}}.wide small{{font-size:12px;letter-spacing:4px;color:#D8B766;display:block;margin-top:14px}}
.note{{text-align:center;margin-top:18px;color:#65676b;font-size:13px}}
</style></head><body><div class="wrap">
<div class="card"><div class="head">{cover}<div class="avatar"><img src="{SV}piste01_plaque_sceau-simple_couleur.svg"></div></div>
<div class="id"><h1>Châlons Champagnes Évents</h1><p>Organisateur d’événements · Châlons-en-Champagne</p></div><div class="btn"><span class="l">Message</span><span>Suivre</span></div>
<div class="tabs"><span class="on">Publications</span><span>À propos</span><span>Événements</span><span>Photos</span><span>Avis</span></div></div>
<div class="grid"><div class="card side"><h3>Présentation</h3>Les rendez-vous de Châlons-en-Champagne, entre canaux, jardins et bulles.<br><br>📍 Châlons-en-Champagne<br>🗓 Programme de la saison</div>
<div>{post(sq,"Samedi, on trinque au bord de l’eau. 🥂 Nuit des Bulles : dégustations, musique et lumières sur les quais.","12 juin")}
{post(dk,"Le programme d’été est en ligne : concerts, balades et dégustations, de juin à septembre.","2 juin")}</div></div>
<div class="note">Maquette — contenus et dates fictifs, visuels illustrés (à remplacer par des photographies)</div></div></body></html>'''
open("fb_page.html","w").write(html)
