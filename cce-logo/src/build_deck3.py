import json, html as H
from mk_common import FONTCSS, bokeh
INK="#16291F";CR="#F4ECDB";GD="#8B6420"
m=json.load(open('manifest3.json'))
T="file:///home/user/Grafiae/cce-logo/tests3/"
css=f'''{FONTCSS}
@page{{size:297mm 210mm;margin:0}}*{{box-sizing:border-box}}body{{margin:0;font-family:Jost;color:{INK}}}
.pg{{width:1123px;height:794px;position:relative;overflow:hidden;page-break-after:always;background:{CR};padding:46px 56px}}
h2{{font-family:Cormorant;font-weight:400;font-size:40px;margin:0 0 4px}}.k{{font-size:11px;letter-spacing:4px;color:{GD};margin-bottom:10px}}
.foot{{position:absolute;left:56px;right:56px;bottom:20px;font-size:9px;letter-spacing:2.5px;color:{GD};display:flex;justify-content:space-between;border-top:1px solid #d8cdb2;padding-top:8px}}
p{{font-size:13px;line-height:1.5;margin:0 0 8px}}h4{{font-size:10px;letter-spacing:3px;color:{GD};margin:12px 0 4px;font-weight:500}}
table{{width:100%;border-collapse:collapse;margin-top:14px;font-size:12px}}th{{font-size:10px;letter-spacing:2.5px;color:{GD};text-align:left;font-weight:500;padding:8px 6px;border-bottom:1px solid {INK}}}td{{padding:10px 6px;border-bottom:1px solid #d8cdb2;vertical-align:top;line-height:1.4}}
.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px}}.c{{position:relative;height:300px;display:flex;align-items:center;justify-content:center;overflow:hidden}}
.c img{{max-width:100%;max-height:100%}}.c span{{position:absolute;left:8px;bottom:6px;font-size:10px;letter-spacing:2px;text-transform:uppercase;opacity:.75}}
.tx{{background:#fff;padding:14px 16px;height:300px;overflow:hidden}}.tx p{{font-size:11.2px;line-height:1.42;margin-bottom:5px}}.tx h4{{margin:8px 0 3px}}
.o{{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin-top:14px}}.o div{{height:112px;display:flex;align-items:center;justify-content:center;overflow:hidden}}.o img{{max-width:100%;max-height:100%}}
'''
def foot(n): return f'<div class="foot"><span>CCE · SÉRIE 3 · D’APRÈS VOTRE TABLEAU PINTEREST</span><span>{n}</span></div>'
D={
"11":("Le Trait","Les dessins d’un seul trait (bouteille, verre) de votre tableau.","La tige de la coupe devient le sol, puis un long filet sous le nom, jusqu’à une dernière bulle : un seul tracé continu. Pas de bouteille, pas de cadre.","Le « verre + bulles » est courant : c’est le filet-signature qui rend la piste propre. Trait fin : fixer une épaisseur minimale pour le petit format."),
"12":("L’Arche pleine","Les verres en réserve (négatif) dans une forme pleine.","Une arche de Châlons, pleine, dans laquelle la coupe, les bulles et le sigle CCE apparaissent en réserve. Un filet doré fait le contour.","Forme locale (arche) et non un rectangle ou une bouteille. La réserve demande un fond uni et une impression très propre."),
"13":("Santé","Les verres par deux, en duo.","Deux coupes qui trinquent, avec un éclat de rayons et de bulles au point de contact et CCE entre les pieds. Dessin symétrique, très événementiel.","Le toast est un motif très courant : originalité plus faible, vérification d’antériorités indispensable. Très bon en avatar et en affiche."),
"14":("Le Cartouche","Les écussons, cartouches et monogrammes ornés.","Un cartouche arrondi dont la bordure est faite de bulles (anneaux dessinés à la main et perles). Nom empilé, sigle CCE en tête.","Pas de ruban ni de fleurons classiques : l’ornement est la bulle elle-même. Bordure fine à simplifier en petit format."),
"15":("La Rosace","Les marques d’événement abstraites, symbole + nom (Moments Events).","Une rosace faite uniquement de bulles : on y lit à la fois des convives réunis et une rosace d’église. Nom en capitales géométriques à côté.","Symbole très lisible en grand, mais qui devient un simple disque à 16 px. Prévoir une version simplifiée."),
"16":("Les Gigognes","Les lettres qui deviennent un verre ou un dessin.","C dans C dans E : trois formes imbriquées comme des bulles dans des bulles, avec des bulles qui s’échappent par l’ouverture. On lit CCE de l’extérieur vers l’intérieur.","La lecture du sigle est à tester auprès de non-initiés. Peut aussi évoquer un symbole de signal ou une lune."),
}
pages=[]
pages.append(f'''<section class="pg" style="background:{INK};color:{CR};padding:0"><svg width="1123" height="794" style="position:absolute;inset:0">{bokeh(1123,794,30,41,rmax=52,amax=.1)}</svg>
<div style="position:absolute;left:72px;top:240px"><div class="k" style="color:#D8B766">SÉRIE 3 · D’APRÈS VOTRE TABLEAU</div><h2 style="font-size:70px;line-height:1;font-weight:300">Six pistes,<br>trente variantes</h2><p style="margin-top:22px;color:#D8B766;font-size:15px">Inspirées de vos références, sans en copier aucune</p></div>
<div style="position:absolute;left:72px;bottom:44px;font-size:10px;letter-spacing:3px;color:#a9b3a8">CHÂLONS CHAMPAGNES ÉVENTS · NOVEMBRE 2026 · LOGOS SEULS, SANS MAQUETTE</div></section>''')
pages.append(f'''<section class="pg"><div class="k">01 · VOTRE TABLEAU</div><h2>Ce que je lis dans vos 16 épingles</h2>
<table><tr><th style="width:24%">THÈME</th><th>CE QUE J’Y VOIS</th></tr>
<tr><td><b>Verre et lettre ne font qu’un</b></td><td>Un « S » dont la courbe devient une coupe, une lettre + un verre = un verre penché, un verre en réserve dans un bloc plein, des silhouettes de public dans un verre.</td></tr>
<tr><td><b>Le trait simple</b></td><td>Bouteille de champagne et verres dessinés d’un seul trait fin, avec des bulles ; un cadre géométrique autour d’un verre.</td></tr>
<tr><td><b>Ornement et monogramme</b></td><td>Cartouches à lobes, écussons de mariage, monogramme symétrique, boîtes à motifs : le côté précieux, décoratif et symétrique.</td></tr>
<tr><td><b>Les verres par deux</b></td><td>Deux verres côte à côte dans un rond noir et or : l’idée du toast, de la convivialité.</td></tr>
<tr><td><b>Une arche autour d’une bouteille</b></td><td>Un logo de cave avec une bouteille sous une arche : proche de notre Arcade, à ne pas rapprocher davantage.</td></tr>
<tr><td><b>Les couleurs</b></td><td>Noir et or ; bleu cobalt et blanc ; bleu ciel ; brique sur rose poudré ; brun et cuivre ; rose doré sur noir.</td></tr></table>
<p class="src" style="font-size:10.5px;color:#6b6556;margin-top:12px">Je n’ai pu lire que les 16 épingles exposées par le flux public du tableau (il peut en contenir davantage). Les images ne sont pas recopiées dans ce dossier : elles appartiennent à leurs auteurs.</p>{foot(2)}</section>''')
pages.append(f'''<section class="pg"><div class="k">02 · S’INSPIRER SANS COPIER</div><h2>Un principe retenu, une forme nouvelle</h2>
<table><tr><th>PRINCIPE RETENU</th><th>MA TRADUCTION</th><th>CE QUI LA REND DIFFÉRENTE</th></tr>
<tr><td>Dessin d’un seul trait</td><td><b>Le Trait</b></td><td>Le pied du verre devient le filet sous le nom. Aucune bouteille, aucun cadre.</td></tr>
<tr><td>Verre en réserve dans une forme pleine</td><td><b>L’Arche pleine</b></td><td>Forme tirée de l’architecture de Châlons, sigle et bulles dans la réserve.</td></tr>
<tr><td>Deux verres, toast</td><td><b>Santé</b></td><td>Verres inclinés qui se touchent, éclat de rayons et de bulles, CCE entre les pieds.</td></tr>
<tr><td>Cartouche orné, monogramme</td><td><b>Le Cartouche</b></td><td>La bordure est entièrement faite de bulles dessinées à la main, sans fleurons ni ruban.</td></tr>
<tr><td>Symbole d’événement + nom</td><td><b>La Rosace</b></td><td>Symbole construit en bulles : convives et rosace à la fois.</td></tr>
<tr><td>Lettre qui devient une forme</td><td><b>Les Gigognes</b></td><td>Trois lettres imbriquées (C, C, E) au lieu d’un verre ou d’une lettre unique.</td></tr></table>
<p style="margin-top:14px;font-size:12px">Limites : un verre avec des bulles est un motif universel, et deux verres qui trinquent aussi. Les formes ci-dessous sont dessinées à partir de zéro, mais une <b>recherche d’antériorités</b> (INPI, recherche d’image inversée) reste indispensable avant de choisir.</p>{foot(3)}</section>''')
n=4
for num,(title,insp,idea,vig) in D.items():
    items=[x for x in m if x["num"]==num]
    tiles="".join(f'<div class="c" style="background:{x["bg"]}"><img src="{T}{x["file"]}.svg"><span style="color:{x["ink"]}">{H.escape(x["palette"])}</span></div>' for x in items)
    tx=f'<div class="tx"><h4 style="margin-top:0">INSPIRATION</h4><p>{insp}</p><h4>LA PISTE</h4><p>{idea}</p><h4>VIGILANCE</h4><p>{vig}</p></div>'
    pages.append(f'<section class="pg"><div class="k">PISTE {num}</div><h2>{title}</h2><div class="g">{tiles}{tx}</div>{foot(n)}</section>'); n+=1
tiles="".join(f'<div style="background:{x["bg"]}"><img src="{T}{x["file"]}.svg"></div>' for x in m)
pages.append(f'<section class="pg"><div class="k">VUE D’ENSEMBLE</div><h2>Les 30 variantes</h2><div class="o">{tiles}</div>{foot(n)}</section>')
open("deck3.html","w").write(f'<html><head><meta charset=utf-8><style>{css}</style></head><body>{"".join(pages)}</body></html>')
