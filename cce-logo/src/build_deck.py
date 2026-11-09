from mk_common import *
MK="file:///home/user/Grafiae/cce-logo/mockups/"
INK="#16291F";CR="#F4ECDB";GD="#B08130"
def img(n,s="",st=""): return f'<img src="{SV}{n}.svg" style="{st}">'
P=[
 dict(n="01",slug="plaque",t="La Plaque",tag="Le sceau de muselet",
  idea="Un sceau circulaire inspiré des plaques de muselet, ces petits disques de métal posés sur le bouchon, que les collectionneurs recherchent (la placomusophilie). Monogramme CCE au centre, perlage doré en bordure, nom en exergue.",
  dessin="Cormorant Garamond (monogramme) et Jost (exergue), tracés convertis en courbes. Bulles dessinées à la main : anneaux à épaisseur variable, contour légèrement irrégulier.",
  ref="Plaques de muselet gaufrées · étiquettes de cuvées prestige · tampons et sceaux de cave",
  pro="Très premium, immédiatement champagne. Se décline en sceau, tampon, étiquette, gaufrage, avatar rond. Existe en version simplifiée sans texte.",
  con="Le moins « Châlons » des cinq : un sceau pourrait appartenir à n’importe quelle maison. Le texte en cercle devient illisible sous 25 mm.",
  main="piste01_plaque",s2="piste01_plaque_sceau-simple",wide=False),
 dict(n="02",slug="perlage",t="Le Perlage",tag="Le monogramme qui pétille",
  idea="Un monogramme typographique très aéré, en Cormorant Light, d’où s’échappe une colonne de bulles : petites et pleines en bas, grandes et creuses en haut, comme dans une flûte. L’accent de « Châlons » et d’« Évents » devient une bulle.",
  dessin="Lettres fines à fort contraste, bulles encrées à la main. L’accent-bulle est un parti pris à tester : il peut se lire comme un point plutôt que comme un accent aigu.",
  ref="Monogrammes typographiques de maisons de champagne · traitement de la bulle comme motif",
  pro="Léger, élégant, très simple à animer (les bulles montent). Se prête bien aux bandeaux et aux réseaux sociaux.",
  con="Peu ancré dans le territoire. Les traits fins tiennent mal en petit format et en broderie.",
  main="piste02_perlage",s2="piste02_perlage",wide=True),
 dict(n="03",slug="reflet",t="Le Reflet",tag="Venise pétillante",
  idea="Une coupe posée sur un canal, avec son reflet dessiné en traits d’eau. Clin d’œil direct au surnom de la ville, « Venise pétillante », et à la Marne et au Mau qui la traversent. Les bulles montent hors du verre.",
  dessin="Croissant plein pour la coupe, niveau de champagne doré, reflet construit en filets qui épousent la silhouette. Tout est vectoriel et bicolore.",
  ref="Surnom « Venise pétillante » (déjà utilisé par l’office) · illustrations au trait de l’art déco",
  pro="Le plus narratif et le plus lié à Châlons. Original par rapport à un simple « verre + bulles ».",
  con="Format vertical, donc difficile à placer en bandeau. Le reflet est fin et se perd en petit. Une coupe reste un cliché de la catégorie.",
  main="piste03_reflet",s2="piste03_reflet",wide=False),
 dict(n="04",slug="signature",t="La Signature",tag="Fait main, jusqu’au bout",
  idea="Le nom écrit à la plume, comme une signature de cuvée, souligné d’un trait de pinceau doré qui s’achève en bulles. Un monogramme manuscrit CCE complète le système pour les petits formats.",
  dessin="Pinyon Script pour la base, trait de pinceau à largeur variable dessiné en courbes. À redessiner à la main dans Illustrator pour obtenir un vrai lettrage unique.",
  ref="Lettrages d’affiches de champagne de la Belle Époque (Mucha, affiche Ruinart, 1896) · signatures de cuvées",
  pro="C’est la piste la plus « faite main » et la plus chaleureuse. Très belle sur les supports papier et les cartons d’invitation.",
  con="Le nom est long et la lisibilité en petit est faible. Le sigle CCE passe au second plan, ce qui va à l’encontre de l’abréviation demandée.",
  main="piste04_signature",s2="piste04_signature_monogramme",wide=True),
 dict(n="05",slug="arcade",t="L’Arcade",tag="Trois arches, trois lettres",
  idea="Trois arches, une lettre dans chacune : C, C, E. La plus haute au centre rappelle les arcs de triomphe de la ville, comme la Porte Sainte-Croix. Les bulles montent sous les voûtes et une dernière s’échappe au sommet.",
  dessin="Arches à double filet (gravure d’étiquette), lettres Cormorant, sol doré. Le symbole fonctionne seul, sans le nom.",
  ref="Porte Sainte-Croix (XVIIIᵉ s.) · étiquettes gravées · portails et arcades de la ville",
  pro="Le plus lisible : on lit CCE sans effort. Ancré dans le patrimoine local, singulier, très solide en petit format. Se découpe en motif répétable.",
  con="Plus architectural que festif : il faut les bulles et la couleur pour apporter l’effervescence. Forme proche d’une arcade générique si on ne soigne pas les proportions.",
  main="piste05_arcade",s2="piste05_arcade_symbole",wide=True),
]
def piste_page(p):
    big=SV+p["main"]+"_couleur.svg"
    st="max-height:560px;max-width:100%" 
    return f'''<section class="pg"><div class="L" style="background:{CR}"><div class="lab">PISTE {p["n"]}</div><img src="{big}" style="width:{ '82%' if p['wide'] else 'auto'};height:auto;max-height:{'400px' if p['wide'] else '470px'};max-width:84%">
<div class="mini"><div style="background:{INK}"><img src="{SV}{p['main']}_negatif-transparent.svg"></div><div style="background:#fff"><img src="{SV}{p['main']}_mono.svg"></div><div style="background:{CR};border:1px solid #d8cdb2"><img src="{SV}{p['s2']}_couleur.svg" style="max-height:56px"></div><div class="sm"><img src="{SV}{p['s2']}_couleur.svg" style="max-height:24px;max-width:70px"></div></div>
<div class="lg"><span>négatif</span><span>noir</span><span>variante</span><span>petit format</span></div></div>
<div class="R"><h3>{p["t"]}</h3><em>{p["tag"]}</em><h4>L’idée</h4><p>{p["idea"]}</p><h4>Le dessin</h4><p>{p["dessin"]}</p><h4>Références</h4><p>{p["ref"]}</p>
<div class="pc"><div><h4>Forces</h4><p>{p["pro"]}</p></div><div><h4>Points de vigilance</h4><p>{p["con"]}</p></div></div></div></section>'''
def dots(k): return "●"*k+"○"*(5-k)
ratings=[("Plaque",5,4,2,3,5),("Perlage",4,3,1,3,4),("Reflet",4,2,5,4,3),("Signature",4,2,2,3,3),("Arcade",4,5,4,5,5)]
css=f'''{FONTCSS}
@page{{size:297mm 210mm;margin:0}}*{{box-sizing:border-box}}body{{margin:0;font-family:Jost;color:{INK}}}
.pg{{width:1123px;height:794px;position:relative;overflow:hidden;page-break-after:always;background:{CR};padding:56px 64px}}
.dk{{background:{INK};color:{CR}}}h1,h2,h3{{font-family:Cormorant;font-weight:400;margin:0}}
h2{{font-size:44px;line-height:1.05;margin-bottom:6px}}.k{{font-size:11px;letter-spacing:4px;color:{GD};margin-bottom:12px}}.dk .k{{color:#D8B766}}
p{{font-size:13.5px;line-height:1.55;margin:0 0 10px}}.foot{{position:absolute;left:64px;right:64px;bottom:26px;font-size:9px;letter-spacing:2.5px;color:{GD};display:flex;justify-content:space-between;border-top:1px solid #d8cdb2;padding-top:8px}}
.cols{{display:grid;gap:34px;margin-top:26px}}.c3{{grid-template-columns:repeat(3,1fr)}}.c4{{grid-template-columns:repeat(4,1fr)}}
h4{{font-size:10px;letter-spacing:3px;color:{GD};margin:14px 0 4px;font-weight:500}}ul{{margin:0;padding-left:16px;font-size:13.5px;line-height:1.6}}
.src{{font-size:10px;color:#6b6556;margin-top:14px}}
.L{{position:absolute;left:0;top:0;bottom:0;width:640px;display:flex;align-items:center;justify-content:center;padding:60px 0 150px}}.lab{{position:absolute;left:64px;top:56px;font-size:11px;letter-spacing:4px;color:{GD}}}
.R{{position:absolute;left:640px;right:0;top:0;bottom:0;padding:56px 56px 30px 48px;background:#fff}}.R h3{{font-size:48px}}.R em{{font-family:Cormorant;font-size:21px;color:{GD}}}.R p{{font-size:12.5px;line-height:1.5;margin-bottom:6px}}.pc{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
.mini{{position:absolute;left:64px;right:64px;bottom:70px;display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}.mini div{{height:88px;display:flex;align-items:center;justify-content:center;padding:8px}}.mini img{{max-width:100%;max-height:72px}}.mini .sm{{background:{CR};border:1px solid #d8cdb2}}
.lg{{position:absolute;left:64px;right:64px;bottom:50px;display:grid;grid-template-columns:repeat(4,1fr);gap:12px;font-size:9px;letter-spacing:2px;color:#8a8372;text-align:center}}
table{{width:100%;border-collapse:collapse;margin-top:22px;font-size:13px}}th{{font-size:10px;letter-spacing:2.5px;color:{GD};text-align:left;font-weight:500;padding:8px 6px;border-bottom:1px solid {INK}}}td{{padding:13px 6px;border-bottom:1px solid #d8cdb2}}td.d{{letter-spacing:3px;color:{GD};font-size:13px}}tr.rec td{{background:#EBDFC2;font-weight:600}}
.sw{{display:flex;gap:16px;margin-top:20px}}.sw div{{flex:1;height:120px;border-radius:4px;padding:12px;font-size:11px;display:flex;flex-direction:column;justify-content:flex-end}}
'''
def foot(n): return f'<div class="foot"><span>CCE · CHÂLONS CHAMPAGNES ÉVENTS — EXPLORATION D’IDENTITÉ</span><span>{n}</span></div>'
pages=[]
pages.append(f'''<section class="pg dk" style="padding:0"><svg width="1123" height="794" style="position:absolute;inset:0">{bokeh(1123,794,30,8,rmax=52,amax=.1)}</svg>
<img src="{SV}piste01_plaque_negatif-transparent.svg" style="position:absolute;right:-90px;top:60px;width:700px;opacity:1">
<div style="position:absolute;left:72px;top:230px;width:520px"><div class="k">EXPLORATION D’IDENTITÉ VISUELLE</div><h1 style="font-size:78px;line-height:.98;font-weight:300">Châlons<br>Champagnes<br><i>Évents</i></h1>
<p style="margin-top:28px;font-size:15px;letter-spacing:.5px;color:#D8B766">Cinq pistes de logo pour « CCE »</p></div>
<div style="position:absolute;left:72px;bottom:44px;font-size:10px;letter-spacing:3px;color:#a9b3a8">OFFICE DE TOURISME DE CHÂLONS-EN-CHAMPAGNE · NOVEMBRE 2026 · DOCUMENT DE TRAVAIL</div></section>''')
pages.append(f'''<section class="pg"><div class="k">01 · LE POINT DE DÉPART</div><h2>Ce que le logo doit faire</h2>
<div class="cols c3"><div><h4>LA DEMANDE</h4><ul><li>Nom : Châlons Champagnes Évents</li><li>Abréviation : CCE</li><li>Registre premium, champagne, bulles</li><li>Quelque chose de graphique, fait main</li><li>Explorer plusieurs pistes</li></ul></div>
<div><h4>LES TESTS QU’IL DOIT PASSER</h4><ul><li>Lisible en avatar rond (≈ 40 px)</li><li>Fonctionne en noir seul et en négatif</li><li>Tient sur une brochure comme sur Facebook</li><li>Reproductible : dorure, gaufrage, flocage</li><li>Le sigle CCE se lit d’un coup d’œil</li></ul></div>
<div><h4>CE QUE DIT LE CONTEXTE</h4><p>L’office de tourisme a présenté une nouvelle identité en mai 2021 : un nom de marque et un univers graphique construits avec l’agence Champagne Création (Reims), autour de « la parenthèse touristique ». Le surnom « Venise pétillante » vient de la période précédente.</p><p><b>Conséquence :</b> CCE doit être une marque d’événements qui s’adosse à cette identité sans la concurrencer.</p></div></div>
<div class="src">Source : communiqué de presse de l’office de tourisme, 18 mai 2021 (chalons-tourisme.com). Je n’ai pas eu accès aux fichiers du logo actuel : à comparer avant de valider une piste.</div>{foot(2)}</section>''')
def code(t,d,svg): return f'<div><div style="height:90px">{svg}</div><h4>{t}</h4><p>{d}</p></div>'
pages.append(f'''<section class="pg"><div class="k">02 · LE TERRITOIRE GRAPHIQUE</div><h2>Quatre codes pour une marque</h2>
<div class="cols c4" style="margin-top:44px">
{code("LA CRAIE","Le sous-sol de la Champagne. Fond crème, papier mat, gaufrage : la matière qui fait le premium.",f'<div style="width:90px;height:90px;border-radius:50%;background:{CR};border:2px solid {INK}"></div>')}
{code("LE PERLAGE","La bulle comme signature. Dessinée à la main : anneaux irréguliers, plus ou moins épais.",f'<svg width="140" height="90">{"".join(f"<circle cx=\'{30+i*22}\' cy=\'{70-i*12}\' r=\'{5+i*4}\' fill=\'none\' stroke=\'{GD}\' stroke-width=\'2\'/>" for i in range(4))}</svg>')}
{code("L’EAU","La Marne, le Mau, les canaux : « Venise pétillante ». Reflets, lignes d’eau, symétrie.",f'<svg width="140" height="90"><path d="M10 38H130" stroke="{GD}" stroke-width="2"/>{"".join(f"<path d=\'M{50-i*5} {46+i*10}H{90+i*5}\' stroke=\'{INK}\' stroke-width=\'{3-i*.5}\'/>" for i in range(4))}</svg>')}
{code("L’ARCHE","La Porte Sainte-Croix, les portails, la collégiale Notre-Dame-en-Vaux : le patrimoine de la ville.",f'<svg width="140" height="90"><path d="M20 88V40A28 28 0 0 1 76 40V88M86 88V50A18 18 0 0 1 122 50V88" fill="none" stroke="{INK}" stroke-width="3"/></svg>')}
</div><div class="src" style="margin-top:50px">Repères patrimoniaux issus de la documentation de l’office de tourisme (Notre-Dame-en-Vaux, inscrite au patrimoine mondial au titre des chemins de Compostelle ; Porte Sainte-Croix, arc de triomphe du XVIIIᵉ s.).</div>{foot(3)}</section>''')
refs=[("Plaques de muselet","Disque métal gaufré, bordure perlée, monogramme central. La marque sur le bouchon est un vrai support de branding.","Piste 01","paris-friendly.fr · thelabelmaker.eu"),
("Étiquettes de cuvée gravées","Filets fins, double cadre, typographie à empattements : le langage de la gravure.","Pistes 01, 05","Chez tout caviste"),
("Affiche Ruinart de Mucha (1896)","Lettrage et ornement dessinés à la main : l’âge d’or de l’affiche de champagne.","Piste 04","Musées, banques d’images"),
("Cairn Champagne (Dribbble)","Marque et monogramme en typographie sobre, sur un projet de champagne.","Piste 02","dribbble.com/cairnchampagne"),
("« Les bulles » (Mind Sparkle)","Article sur le traitement de la bulle en design : à lire pour le motif.","Pistes 02, 03","mindsparklemag.com/design/les-bulles"),
("12 champagne branding examples","Panorama des codes premium du secteur, utile pour éviter les clichés.","Toutes","designrush.com"),
("Joseph Perrier","Maison de champagne installée à Châlons-en-Champagne : repère local à consulter pour la cohabitation visuelle.","Toutes","josephperrier.com")]
rows="".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td style='color:#6b6556'>{d}</td></tr>" for a,b,c,d in refs)
pages.append(f'''<section class="pg"><div class="k">03 · RÉFÉRENCES</div><h2>D’où viennent les pistes</h2>
<table><tr><th>RÉFÉRENCE</th><th>CE QU’ON EN RETIENT</th><th>PISTE</th><th>À CONSULTER</th></tr>{rows}</table>
<p style="margin-top:18px;font-size:12px"><b>À éviter :</b> deux C entrelacés. C’est la signature d’une très grande maison de mode, fortement protégée : aucune piste ne s’en approche. Éviter aussi la simple « flûte + bulles », trop générique pour être déposée.</p>
<div class="src">Limite : depuis cet environnement je n’ai pu consulter que le texte des pages (pas leurs images). Les « retenus » ci-dessus viennent de ces textes et de repères généraux : un moodboard visuel (Pinterest, Behance, Firefly Boards) reste à constituer pour valider les ambiances.</div>{foot(4)}</section>''')
pages.append(f'''<section class="pg"><div class="k">04 · VUE D’ENSEMBLE</div><h2>Cinq pistes</h2>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:24px">{"".join(f'<div style="background:#fff;padding:16px 12px;height:470px;text-align:center;display:flex;flex-direction:column"><div style="flex:1;display:flex;align-items:center;justify-content:center"><img src="{SV}{p["main"]}_couleur.svg" style="max-width:100%;max-height:300px"></div><h3 style="font-size:26px;margin-top:12px">{p["t"]}</h3><div style="font-size:9.5px;letter-spacing:2px;color:{GD};margin-top:4px">{p["tag"].upper()}</div></div>' for p in P)}</div>{foot(5)}</section>''')
for p in P: pages.append(piste_page(p))
tr="".join(f'<tr class="{"rec" if r[0]=="Arcade" else ""}"><td>{r[0]}</td><td class="d">{dots(r[1])}</td><td class="d">{dots(r[2])}</td><td class="d">{dots(r[3])}</td><td class="d">{dots(r[4])}</td><td class="d">{dots(r[5])}</td></tr>' for r in ratings)
pages.append(f'''<section class="pg"><div class="k">05 · COMPARATIF</div><h2>Ce que chaque piste fait de mieux</h2>
<table><tr><th>PISTE</th><th>PREMIUM</th><th>PETIT FORMAT</th><th>LIEN CHÂLONS</th><th>ORIGINALITÉ</th><th>DÉCLINAISONS</th></tr>{tr}</table>
<p style="margin-top:20px">Notation de la designer, sur 5. Elle est subjective : c’est une base de discussion, pas un verdict. « Déclinaisons » regroupe brochure, réseaux sociaux, dorure, gaufrage et objets.</p>{foot(11)}</section>''')
pages.append(f'''<section class="pg dk"><div class="k">06 · RECOMMANDATION</div><h2>Un système : l’Arcade, la Plaque et la bulle</h2>
<div style="display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:20px;margin-top:20px;align-items:center">
<div style="background:{CR};height:360px;display:flex;align-items:center;justify-content:center"><img src="{SV}piste05_arcade_couleur.svg" style="width:92%"></div>
<div style="background:{CR};height:360px;display:flex;align-items:center;justify-content:center"><img src="{SV}piste01_plaque_sceau-simple_couleur.svg" style="width:86%"></div>
<div style="background:{CR};height:360px;display:flex;align-items:center;justify-content:center"><svg width="190" height="320" viewBox="0 0 190 320"><g fill="none" stroke="{GD}" stroke-width="3"><circle cx="95" cy="262" r="8" fill="{GD}"/><circle cx="108" cy="222" r="13"/><circle cx="88" cy="168" r="20"/><circle cx="104" cy="98" r="30"/><circle cx="90" cy="36" r="30" stroke="{INK}"/></g></svg></div></div>
<div class="cols c3" style="margin-top:18px"><div><h4>LOGO PRINCIPAL · L’ARCADE</h4><p>Lisible, ancré à Châlons, solide en petit. Il porte la marque sur les brochures, l’affichage et le site.</p></div><div><h4>SCEAU · LA PLAQUE</h4><p>Pour les avatars ronds, tampons, étiquettes, gaufrage et objets de boutique.</p></div><div><h4>MOTIF · LA BULLE ENCRÉE</h4><p>Puces, séparateurs, motifs de fond, animations : l’effervescence qui manquait à l’architecture.</p></div></div>{foot(12)}</section>''')
pages.append(f'''<section class="pg"><div class="k">07 · COULEURS ET TYPOGRAPHIES</div><h2>La palette et les caractères</h2>
<div class="sw"><div style="background:{INK};color:{CR}"><b>Vert bouteille</b>#16291F</div><div style="background:{CR};border:1px solid #cfc3a5"><b>Craie</b>#F4ECDB</div><div style="background:linear-gradient(135deg,#8B6420,#D8B766 40%,#B08130 60%,#DDBF74);color:#16291F"><b>Or</b>dégradé · aplat #B08130</div><div style="background:#fff;border:1px solid #cfc3a5"><b>Perle</b>#FFFFFF</div></div>
<div class="cols c3" style="margin-top:34px"><div><h4>TITRES ET MONOGRAMME</h4><div style="font-family:Cormorant;font-size:64px;line-height:1">Aa <span style="font-weight:300;font-style:italic">Aa</span></div><p>Cormorant Garamond. Licence libre (OFL), utilisable en print et en web.</p></div>
<div><h4>TEXTES ET LÉGENDES</h4><div style="font-size:50px;font-weight:300;letter-spacing:6px">AaBb</div><p>Jost, sans-serif géométrique, en capitales espacées pour les légendes. Licence libre (OFL).</p></div>
<div><h4>SI LE BUDGET LE PERMET</h4><p>Des alternatives payantes plus travaillées pour les titres : Canela, GT Sectra ou Freight Display. À tester avant de figer le dessin des lettres.</p></div></div>{foot(13)}</section>''')
pages.append(f'''<section class="pg"><div class="k">08 · DÉCLINAISONS</div><h2>L’Arcade en couleur, négatif et noir</h2>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:22px"><div style="background:#fff;height:250px;display:flex;align-items:center;justify-content:center"><img src="{SV}piste05_arcade_couleur.svg" style="width:86%"></div><div style="background:{INK};height:250px;display:flex;align-items:center;justify-content:center"><img src="{SV}piste05_arcade_negatif-transparent.svg" style="width:86%"></div><div style="background:#fff;height:250px;display:flex;align-items:center;justify-content:center"><img src="{SV}piste05_arcade_mono.svg" style="width:86%"></div></div>
<div style="display:flex;gap:30px;align-items:center;margin-top:26px"><div style="display:flex;gap:14px;align-items:center"><img src="{SV}piste01_plaque_sceau-simple_couleur.svg" style="width:120px"><img src="{SV}piste01_plaque_sceau-simple_couleur.svg" style="width:64px"><img src="{SV}piste01_plaque_sceau-simple_couleur.svg" style="width:40px"><img src="{SV}piste01_plaque_sceau-simple_couleur.svg" style="width:28px"></div>
<p style="flex:1;font-size:13px">Le sceau simplifié reste lisible jusqu’à environ 40 px : c’est la taille d’un avatar Facebook dans le fil. À 28 px, seul le monogramme CCE se lit : c’est le minimum à ne pas franchir. <b>À valider par un test d’impression réel.</b></p></div>{foot(14)}</section>''')
pages.append(f'''<section class="pg" style="background:#E4E6EA;padding:30px"><div class="k">09 · MAQUETTE FACEBOOK</div><div style="display:flex;justify-content:center;height:690px;overflow:hidden"><img src="{MK}facebook_page.png" style="height:auto;width:620px;align-self:flex-start;box-shadow:0 6px 20px rgba(0,0,0,.18)"></div></section>''')
pages.append(f'''<section class="pg" style="background:#D8D0BF;padding:0"><div class="k" style="position:absolute;left:64px;top:40px">10 · MAQUETTE BROCHURE</div><img src="{MK}brochure.png" style="width:1123px;margin-top:60px"></section>''')
pages.append(f'''<section class="pg dk"><div class="k">11 · ET MAINTENANT</div><h2>Prochaines étapes</h2>
<div class="cols" style="grid-template-columns:1fr 1fr;margin-top:28px;font-size:14px"><ul style="line-height:1.9"><li><b>Choisir</b> une ou deux pistes à pousser</li><li><b>Redessiner à la main</b> : croquis papier, scan, tracé dans Illustrator</li><li><b>Régler les lettres</b> : crénage, épaisseurs, optique des arches</li><li><b>Tester</b> : 40 px, noir seul, dorure, gaufrage, broderie</li></ul>
<ul style="line-height:1.9"><li><b>Vérifier la disponibilité</b> (INPI, classes 35, 41, 43), puis déposer</li><li><b>Trancher</b> sur l’accent-bulle : « Évents » doit rester lisible et bien référencé</li><li><b>Articuler</b> avec l’identité de l’office (2021)</li><li><b>Photographier</b> : remplacer les visuels illustrés des maquettes</li></ul></div>{foot(17)}</section>''')
html=f'<html><head><meta charset=utf-8><style>{css}</style></head><body>{"".join(pages)}</body></html>'
open("deck.html","w").write(html)
