import build_deck as D
from build_deck import css, foot, piste_page, dots, SV, INK, CR, GD, FONTCSS
from mk_common import bokeh
P2=[
 dict(n="06",t="L’Étiquette",tag="Le nom, comme sur une cuvée",wide=False,main="piste06_etiquette",s2="piste06_etiquette",
  idea="Une étiquette ovale à l’ancienne : le nom complet en grandes capitales à empattements et en italique, un perlage doré en bordure, un ruban portant le sigle CCE. Le nom se lit avant tout le reste.",
  dessin="Playfair Display (capitales et italique) pour le nom, Jost pour « Évents », Cormorant pour le sigle. Perlage et bulles dessinés à la main, ruban en dégradé d’or.",
  ref="Typographies de la fin du XIXᵉ s. sur les étiquettes de champagne (projet Madagascar Champagne) · capitales gravées à fort contraste, très espacées (guide des polices pour étiquettes de vin) · association serif + sans-serif, courante en champagne (Champagne Club)",
  pro="Le nom est lisible d’un coup d’œil. Très « cuvée » : se décline en étiquette, sous-verre, carton d’invitation, bouchon.",
  con="Très codé, donc moins singulier. Les filets fins tiennent mal en petit. L’ovale et le ruban sont des clichés du genre."),
 dict(n="07",t="L’Affiche",tag="Le nom composé comme une affiche",wide=True,main="piste07_affiche",s2="piste07_affiche",
  idea="Le nom sur trois lignes de tailles et de graisses différentes, comme une affiche de champagne de la Belle Époque. Une colonne de bulles monte à droite, le sigle CCE signe en bas, comme un monogramme d’imprimeur.",
  dessin="Playfair Display romain et italique, Jost en capitales espacées. Pas de symbole : c’est la composition typographique qui fait la marque.",
  ref="Mucha, affiche Champagne Ruinart (1896) · Cappiello, affiche Champagne Delbeck, Reims (1902) · Cappiello, Veuve Amiot (1922)",
  pro="Horizontale, très lisible, forte en bandeau Facebook ou en en-tête de brochure. Elle est chaleureuse et facile à fabriquer.",
  con="Sans symbole, elle est moins mémorisable. Il faut l’associer à un sceau (piste 01) pour les avatars et les tampons."),
 dict(n="08",t="Les Flèches",tag="L’emblème de la ville, dans le Mau",wide=False,main="piste08_fleches",s2="piste08_fleches",
  idea="La façade de Notre-Dame-en-Vaux, stylisée : deux tours carrées surmontées de flèches, et leur reflet dans l’eau. Les bulles montent entre les deux flèches. Le nom suit en dessous.",
  dessin="Tracé au filet (tours, rosace, portail) avec flèches pleines, reflet en traits d’eau qui épousent la silhouette. À redessiner d’après photographies.",
  ref="Notre-Dame-en-Vaux : façade ouest cantonnée de deux tours carrées à flèches plombées (fiche Monumentum, base Mérimée) · « deux flèches couvertes de plomb qui se reflètent dans le Mau » (techno-science.net) · inscription UNESCO, chemins de Compostelle · surnom « Venise pétillante »",
  pro="La plus locale : le monument phare de la ville et son reflet dans l’eau. Elle raconte à la fois patrimoine, canaux et bulles.",
  con="Silhouette stylisée : les sources divergent sur le nombre de flèches (deux ou quatre), à vérifier sur place. Peut se lire comme une église générique."),
 dict(n="09",t="Le Fizz",tag="Le nom, version contemporaine",wide=True,main="piste09_fizz",s2="piste09_fizz",
  idea="Un logotype en minuscules géométriques, sur trois lignes aux graisses alternées. Le « o » de « châlons » devient une bulle encrée à la main, et le sigle CCE vient en pastille.",
  dessin="Jost en graisses 300 et 600. Le contraste entre une typographie nette et une bulle irrégulière donne le côté « fait main ».",
  ref="Les Bulles (Suisse) : identité construite sur un caractère des années 1920-30 · Champagne Castelnau : marque modernisée, sans les codes traditionnels · association serif + sans-serif (Champagne Club) · M.G.Heucq : lettrage dessiné sur mesure",
  pro="Moderne, très lisible en petit, facile à animer. C’est la plus naturelle pour le numérique : site, réseaux, billetterie.",
  con="Moins solennelle, donc moins premium si on retire l’or. La typographie est standard : à personnaliser (lettres dessinées sur mesure)."),
 dict(n="10",t="L’Éclat",tag="La coupe qui fait feu d’artifice",wide=False,main="piste10_eclat",s2="piste10_eclat",
  idea="Une coupe dont jaillissent des rayons terminés par des bulles : un feu d’artifice, donc un événement. Le sigle CCE est dans la coupe, le nom complet en dessous.",
  dessin="Rayons alternés longs et courts, bulles encrées au bout. Italiana (capitales fines d’inspiration Art déco) pour le nom.",
  ref="Double lecture d’un dessin : French Bubbles (Erevan), « BB » avec une coupe cachée · éventails rayonnants de l’Art déco · Moët & Chandon : emblème remis au centre de la marque (refonte Futurebrand)",
  pro="Du mouvement et de l’énergie, sans casser le premium. Symétrique, donc très bonne en avatar. Le sigle y est contenu sans écraser le nom.",
  con="La coupe est un cliché. Les rayons et Italiana sont fins : à épaissir pour la petite taille et la dorure."),
]
ratings=[("Étiquette",4,2,2,2,4),("Affiche",4,3,2,3,4),("Flèches",4,2,5,4,3),("Fizz",3,5,1,3,5),("Éclat",4,4,2,4,4)]
refs=[
("Destinations voisines","Épernay se présente comme « Épernay en Champagne » ; l’office de Châlons a retiré « Office de Tourisme » de sa marque en 2021 pour valoriser la destination. Je n’ai pas trouvé de refonte récente à Reims.","Toutes","reims-tourisme.com · ot-epernay.fr"),
("Mucha, Champagne Ruinart (1896)","Ornement et lettrage dessinés, l’âge d’or de l’affiche de champagne.","07","champagneclub.com (« The Art of Effervescence ») · meisterdrucke.fr"),
("Cappiello, Champagne Delbeck (1902)","Affiche pour une maison de Reims : un personnage et un nom en grand, composition très lisible.","07","1stdibs.com (Cappiello Delbeck)"),
("Perrier-Jouët × Gallé","L’Art nouveau et le champagne : fleurs d’anémones peintes sur les bouteilles.","06, 07","champagneclub.com"),
("Design d’étiquettes de champagne","Capitales gravées, serif + sans-serif, crest et col de bouteille.","06","champagneclub.com (label design) · madegooddesigns.com"),
("Madagascar Champagne · The Labelmaker","Typographie de la fin du XIXᵉ s. appliquée à une étiquette actuelle.","06","packagingoftheworld.com · thelabelmaker.eu"),
("Notre-Dame-en-Vaux","Description de la façade, des tours et des flèches. Base Mérimée.","08","monumentum.fr (PA00078618) · Wikipédia"),
("Les Bulles · French Bubbles · M.G.Heucq","Identités qui jouent avec la bulle, un caractère d’époque ou un lettrage sur mesure.","09, 10","worldbranddesign.com · studio-boam"),
("Champagne Castelnau · Moët & Chandon","Deux exemples de marques de champagne modernisées.","09, 10","harpers.co.uk · futurebrand.com"),
("Identités d’événements locaux","Ladue Street Fest (marque d’un événement municipal), Festival Park (Istanbul), étude de l’identité du Nottingham Riverside Festival.","Toutes","pnmg.com · monroe.works · eprints.nottingham.ac.uk"),
]
rows="".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td style='color:#6b6556'>{d}</td></tr>" for a,b,c,d in refs)
pages=[]
pages.append(f'''<section class="pg dk" style="padding:0"><svg width="1123" height="794" style="position:absolute;inset:0">{bokeh(1123,794,30,14,rmax=52,amax=.1)}</svg>
<img src="{SV}piste10_eclat_negatif-transparent.svg" style="position:absolute;right:30px;top:80px;width:560px">
<div style="position:absolute;left:72px;top:230px;width:480px"><div class="k">SÉRIE 2 · LE NOM EN PREMIER</div><h1 style="font-size:70px;line-height:1;font-weight:300">Cinq nouvelles<br>pistes</h1>
<p style="margin-top:26px;font-size:15px;color:#D8B766">Châlons Champagnes Évents, avec CCE en signature</p></div>
<div style="position:absolute;left:72px;bottom:44px;font-size:10px;letter-spacing:3px;color:#a9b3a8">OFFICE DE TOURISME DE CHÂLONS-EN-CHAMPAGNE · NOVEMBRE 2026 · DOCUMENT DE TRAVAIL</div></section>''')
pages.append(f'''<section class="pg"><div class="k">01 · RÉFÉRENCES</div><h2>Ce qui nourrit cette série</h2>
<style>.rt td{{padding:7px 6px}}</style><table class="rt" style="font-size:11px;margin-top:10px"><tr><th>RÉFÉRENCE</th><th>CE QU’ON EN RETIENT</th><th>PISTE</th><th>À CONSULTER</th></tr>{rows}</table>
<div class="src" style="margin-top:8px;line-height:1.4">Ces références viennent de recherches web dont je n’ai pu lire que le texte, pas les images : il faut les ouvrir pour juger de l’ambiance. Les logotypes de grandes maisons (Moët, Taittinger…) sont des marques déposées : on s’en inspire, on ne les copie pas. Castelnau utilise deux C liés : à éviter aussi.</div>{foot(2)}</section>''')
pages.append(f'''<section class="pg"><div class="k">02 · VUE D’ENSEMBLE</div><h2>Cinq pistes où le nom passe devant</h2>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:24px">{"".join(f'<div style="background:#fff;padding:16px 10px;height:470px;text-align:center;display:flex;flex-direction:column"><div style="flex:1;display:flex;align-items:center;justify-content:center"><img src="{SV}{p["main"]}_couleur.svg" style="max-width:100%;max-height:300px"></div><h3 style="font-size:26px;margin-top:12px">{p["t"]}</h3><div style="font-size:9.5px;letter-spacing:2px;color:{GD};margin-top:4px">{p["tag"].upper()}</div></div>' for p in P2)}</div>{foot(3)}</section>''')
for p in P2: pages.append(piste_page(p))
tr="".join(f'<tr><td>{r[0]}</td><td class="d">{dots(r[1])}</td><td class="d">{dots(r[2])}</td><td class="d">{dots(r[3])}</td><td class="d">{dots(r[4])}</td><td class="d">{dots(r[5])}</td></tr>' for r in ratings)
pages.append(f'''<section class="pg"><div class="k">03 · COMPARATIF</div><h2>Ce que chaque piste fait de mieux</h2>
<table><tr><th>PISTE</th><th>PREMIUM</th><th>PETIT FORMAT</th><th>LIEN CHÂLONS</th><th>ORIGINALITÉ</th><th>DÉCLINAISONS</th></tr>{tr}</table>
<p style="margin-top:20px">Notation de la designer, sur 5, subjective. Les deux séries se combinent : un logotype horizontal (Affiche ou Fizz) avec un symbole ou un sceau (Plaque, Arcade, Éclat) pour les avatars et les objets.</p>
<h4 style="margin-top:26px">ASSOCIATIONS À ESSAYER</h4><ul><li><b>Affiche + Plaque :</b> nom en grand pour les supports papier, sceau rond pour l’avatar et les tampons.</li><li><b>Flèches + Fizz :</b> l’emblème de la ville avec un logotype contemporain pour le numérique.</li><li><b>Éclat seul :</b> un logo complet qui contient déjà un sigle, un symbole et le nom.</li></ul>{foot(10)}</section>''')
html=f'<html><head><meta charset=utf-8><style>{css}</style></head><body>{"".join(pages)}</body></html>'
open("deck2.html","w").write(html)
