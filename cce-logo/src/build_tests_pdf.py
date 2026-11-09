import json, html as H
from mk_common import FONTCSS, bokeh
from tests_palettes import PALETTES, POS
m=json.load(open('manifest.json'))
T="file:///home/user/Grafiae/cce-logo/tests/"
INK="#16291F";CR="#F4ECDB";GD="#8B6420"
notes={"bordeaux-rose":"Chaleureux, féminin, très « rosé de Champagne ».","bleu-nuit-argent":"Soirée, élégance froide, lien avec l’eau des canaux.","noir-or":"Le plus luxe et le plus classique du champagne.","bleu-canal-cuivre":"Marne et canaux, avec la chaleur du cuivre (alambic, cuve).","violet-pinot":"Évoque le pinot noir et le raisin : gourmand, original.","vert-canal-ambre":"Eau profonde et miel : naturel, patrimoine, jardins.","coquelicot":"Pop et festif : le rouge ravive l’événement.","sauge-craie":"Doux, naturel, sous-sol de craie : très discret.","rose-nuit":"Soirée intime, bulles qui brillent sur fond sombre."}
used={}
for x in m: used.setdefault(x["palette"],[]).append(x["num"])
css=f'''{FONTCSS}
@page{{size:297mm 210mm;margin:0}}*{{box-sizing:border-box}}body{{margin:0;font-family:Jost;color:{INK}}}
.pg{{width:1123px;height:794px;position:relative;overflow:hidden;page-break-after:always;background:{CR};padding:48px 56px}}
h2{{font-family:Cormorant;font-weight:400;font-size:42px;margin:0 0 4px}}.k{{font-size:11px;letter-spacing:4px;color:{GD};margin-bottom:10px}}
.foot{{position:absolute;left:56px;right:56px;bottom:22px;font-size:9px;letter-spacing:2.5px;color:{GD};display:flex;justify-content:space-between;border-top:1px solid #d8cdb2;padding-top:8px}}
.g4{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}}.c{{position:relative;height:290px;display:flex;align-items:center;justify-content:center;overflow:hidden}}
.c img{{max-width:100%;max-height:100%}}.c span{{position:absolute;left:10px;bottom:8px;font-size:11px;letter-spacing:2.5px;text-transform:uppercase;opacity:.75}}
.sw{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:14px}}.s{{background:#fff;padding:10px 12px}}.s .b{{display:flex;height:46px;margin-bottom:8px}}.s .b div{{flex:1}}
.s b{{font-size:14px}}.s p{{font-size:11px;margin:3px 0;line-height:1.35}}.s small{{font-size:10px;letter-spacing:1.5px;color:#6b6556}}
.o{{display:grid;grid-template-columns:repeat(8,1fr);gap:6px;margin-top:14px}}.o div{{height:98px;display:flex;align-items:center;justify-content:center;overflow:hidden}}.o img{{max-width:100%;max-height:100%}}
'''
def foot(n): return f'<div class="foot"><span>CCE · TESTS DE LOGOS ET DE PALETTES</span><span>{n}</span></div>'
pages=[]
pages.append(f'''<section class="pg" style="background:{INK};color:{CR};padding:0"><svg width="1123" height="794" style="position:absolute;inset:0">{bokeh(1123,794,30,31,rmax=52,amax=.1)}</svg>
<div style="position:absolute;left:72px;top:250px"><div class="k" style="color:#D8B766">CHÂLONS CHAMPAGNES ÉVENTS</div><h2 style="font-size:76px;line-height:1;font-weight:300">40 tests<br>de logos</h2><p style="margin-top:22px;color:#D8B766;font-size:15px">10 pistes × 4 palettes · 9 palettes en tout</p></div>
<div style="position:absolute;left:72px;bottom:44px;font-size:10px;letter-spacing:3px;color:#a9b3a8">DOCUMENT DE TRAVAIL · NOVEMBRE 2026 · AUCUNE MAQUETTE, LOGOS SEULS</div></section>''')
sw=""
for pid,label,bg,ink,grad in PALETTES:
    if isinstance(grad,list):
        g=f"linear-gradient(135deg,{grad[0]},{grad[1]} 30%,{grad[2]} 55%,{grad[3]} 78%,{grad[4]})"; acc=grad[2]
    else: g=grad; acc=grad
    sw+=f'<div class="s"><div class="b"><div style="background:{bg};border:1px solid #d8cdb2"></div><div style="background:{ink}"></div><div style="background:{g}"></div></div><b>{label}</b><p>{notes[pid]}</p><small>FOND {bg} · ENCRE {ink} · ACCENT {acc}</small><p style="margin-top:6px"><small>PISTES : {", ".join(used[label])}</small></p></div>'
pages.append(f'<section class="pg"><div class="k">01 · LES PALETTES</div><h2>Neuf ambiances de couleurs</h2><div class="sw">{sw}</div>{foot(2)}</section>')
labels={}
for x in m: labels.setdefault(x["num"],[]).append(x)
n=3
for num,items in labels.items():
    cards="".join(f'<div class="c" style="background:{x["bg"]}"><img src="{T}{x["file"]}.svg"><span style="color:{x["ink"]}">{H.escape(x["palette"])}</span></div>' for x in items)
    pages.append(f'<section class="pg"><div class="k">PISTE {num}</div><h2>{H.escape(items[0]["label"])}</h2><div class="g4">{cards}</div>{foot(n)}</section>'); n+=1
tiles="".join(f'<div style="background:{x["bg"]}"><img src="{T}{x["file"]}.svg"></div>' for x in m)
pages.append(f'<section class="pg"><div class="k">VUE D’ENSEMBLE</div><h2>Les 40 tests</h2><div class="o">{tiles}</div><p style="margin-top:14px;font-size:12.5px;line-height:1.5;max-width:880px">Lecture rapide : les fonds sombres (noir, bleu nuit, rose nuit) valorisent le plus les dorures et les filets fins. Les fonds clairs avec encre colorée (bleu canal, violet, vert) rendent les pistes plus sobres. Le coquelicot est le seul test franchement festif : il fonctionne surtout sur L’Affiche, L’Arcade et Le Fizz.</p>{foot(n)}</section>')
open("tests.html","w").write(f'<html><head><meta charset=utf-8><style>{css}</style></head><body>{"".join(pages)}</body></html>')
