from client import PAL, NAMES
F="file:///tmp/claude-0/-home-user-Grafiae/505c24ee-2e35-5947-935f-cfc53e082e9e/scratchpad/build/fonts2/"
S="file:///home/user/Grafiae/cce-logo/client/svg/"
def u(k,lay,kind): return f"{S}proposition{k}_{NAMES[k]}_{lay}_{kind}.svg"
INFO={
"A":dict(t="Le Monogramme",sub="Vos couleurs, votre idée, redessinées",font="Manrope",fam="Man",
  idea="Nous repartons de votre intuition : un monogramme bleu nuit et or, avec une bulle. Les trois lettres ne se chevauchent plus, elles s’emboîtent : un grand C, un C doré, un E au centre. Trois bulles s’échappent par l’ouverture.",
  why=["Continuité : mêmes couleurs, même principe de monogramme","Chaque lettre reste lisible, y compris en très petit","Or en aplat (sans dégradé) : net à l’écran, simple à imprimer","Caractère sans empattement, direct et contemporain"],
  vig="Les C concentriques existent chez d’autres marques : recherche d’antériorités à faire. À tester : lit-on bien « C, C, E » sans explication ?",
  typo="Manrope Bold et Medium pour le nom, Manrope SemiBold pour la signature.",banner="Créons votre expérience."),
"B":dict(t="Les Arches",sub="Châlons, l’accueil et la montée en puissance",font="Marcellus",fam="Mar",
  idea="Trois arches qui grandissent, d’où s’échappent trois bulles. On y lit les arcades et les portes de Châlons, des portes ouvertes aux entreprises, et une progression. Le symbole se passe des initiales : c’est le nom, en capitales romaines, qui porte la marque.",
  why=["La plus singulière et la plus ancrée dans la ville","Symbole plein, très robuste : gravure, broderie, signalétique","Capitales romaines : registre institutionnel et premium","Vert profond et laiton : sort du bleu et or, très répandu"],
  vig="Les hauteurs croissantes peuvent se lire comme un graphique : cohérent avec le tourisme d’affaires, mais à valider avec vous. Rupture avec vos couleurs actuelles (une version bleu et or existe, page 13).",
  typo="Marcellus pour le nom, Manrope SemiBold pour la signature.",banner="Créons votre expérience."),
"C":dict(t="Le Sceau",sub="La signature d’une maison",font="Bodoni Moda",fam="Bod",
  idea="Un sceau : le sigle CCE dans un cercle, comme le cachet d’une maison de champagne. Le cercle s’ouvre en haut à droite pour laisser monter trois bulles. Le nom est composé dans un caractère à forts contrastes, celui des étiquettes et des éditions de luxe.",
  why=["Le registre le plus statutaire, pour un public de dirigeants","Le sceau fonctionne seul : avatar, tampon, gaufrage, pin’s","Nom très lisible, sigle présent sans dominer","Anthracite et cuivre : sobre, chaleureux, peu courant"],
  vig="C’est la forme la plus classique des trois, donc la moins distinctive. Les traits fins du caractère demandent une taille minimale plus élevée.",
  typo="Bodoni Moda pour le nom et le sigle, Manrope SemiBold pour « Events » et la signature.",banner="Créons votre expérience."),
}
css=f'''
@font-face{{font-family:Man;src:url('{F}Manrope.ttf');font-weight:200 800}}
@font-face{{font-family:Mar;src:url('{F}Marcellus.ttf')}}
@font-face{{font-family:Bod;src:url('{F}Bodoni.ttf');font-weight:400 900}}
@page{{size:297mm 210mm;margin:0}}*{{box-sizing:border-box}}body{{margin:0;font-family:Man;color:#1b1b1b}}
.pg{{width:1123px;height:794px;position:relative;overflow:hidden;page-break-after:always;background:#fff;padding:52px 60px}}
.k{{font-size:10.5px;letter-spacing:3.5px;font-weight:600;color:#8a8a8a;margin-bottom:12px;text-transform:uppercase}}
h2{{font-size:34px;font-weight:700;letter-spacing:-.6px;margin:0 0 6px}}h3{{font-size:13px;letter-spacing:2.5px;font-weight:700;margin:18px 0 6px;text-transform:uppercase}}
p,li{{font-size:13.5px;line-height:1.55;margin:0 0 8px}}ul{{margin:0;padding-left:18px}}
.foot{{position:absolute;left:60px;right:60px;bottom:24px;font-size:9px;letter-spacing:2.5px;font-weight:600;color:#9a9a9a;display:flex;justify-content:space-between;border-top:1px solid #e3e3e3;padding-top:9px}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:22px}}
.box{{display:flex;align-items:center;justify-content:center;overflow:hidden}}.box img{{max-width:78%;max-height:74%}}
.lab{{font-size:9px;letter-spacing:2px;font-weight:600;color:#9a9a9a;margin-top:6px;text-transform:uppercase}}
.card{{width:340px;height:220px;border-radius:6px;box-shadow:0 14px 30px -10px rgba(0,0,0,.35),0 2px 6px rgba(0,0,0,.15);position:relative;overflow:hidden}}
'''
def foot(n): return f'<div class="foot"><span>Châlons Champagne Events · Propositions d’identité</span><span>{n}</span></div>'
pg=[]
pg.append(f'''<section class="pg" style="background:#15171a;color:#fff;padding:0"><div style="position:absolute;left:72px;top:250px"><div class="k" style="color:#b9b9b9">Identité visuelle · Tourisme d’affaires</div>
<div style="font-size:66px;font-weight:700;letter-spacing:-2px;line-height:1.02">Châlons<br>Champagne Events</div><p style="font-size:17px;color:#cfcfcf;margin-top:26px">Trois propositions de logo</p></div>
<div style="position:absolute;left:72px;bottom:46px;font-size:10px;letter-spacing:3px;color:#8e8e8e;font-weight:600">NOVEMBRE 2026 · DOCUMENT DE PRÉSENTATION</div></section>''')
pg.append(f'''<section class="pg"><div class="k">01 · Point de départ</div><h2>Ce que nous gardons, ce que nous faisons évoluer</h2>
<div class="two"><div><h3>Ce que nous gardons de vos essais</h3><ul><li>Le bleu nuit et l’or, qui installent d’emblée le sérieux et le prestige</li><li>L’idée d’un monogramme construit sur les initiales</li><li>La bulle, clin d’œil au champagne, utilisée avec retenue</li><li>La signature « Tourisme d’affaires »</li></ul>
<h3>L’objectif</h3><p>Un logo pour un public d’entreprises : premium, institutionnel, immédiatement lisible, et qui tient partout, de l’avatar LinkedIn à la signalétique d’un salon.</p></div>
<div><h3>Ce que nous faisons évoluer</h3><ul><li><b>La lisibilité du sigle.</b> Des lettres qui se superposent deviennent difficiles à lire, surtout en petit. Nous les séparons ou les emboîtons proprement.</li><li><b>Le contraste.</b> Un mot en or sur fond clair se lit mal : le nom passe entièrement en couleur foncée, l’or devient un accent.</li><li><b>Les dégradés.</b> Ils vieillissent vite et s’impriment mal : l’or est traité en aplat.</li><li><b>La typographie.</b> Un caractère choisi pour son registre, avec des espacements réglés.</li><li><b>Un système.</b> Version horizontale, verticale, symbole seul, négatif et noir.</li></ul></div></div>{foot(2)}</section>''')
pg.append(f'''<section class="pg"><div class="k">02 · Vue d’ensemble</div><h2>Trois propositions</h2>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:22px">{"".join(f'<div><div class="box" style="height:400px;background:{PAL[k]["paper"]}"><img src="{u(k,"vertical","couleur")}" style="max-width:82%;max-height:80%"></div><div style="font-size:20px;font-weight:700;margin-top:12px">{k} · {INFO[k]["t"]}</div><p style="color:#666;margin-top:2px">{INFO[k]["sub"]}</p></div>' for k in "ABC")}</div>{foot(3)}</section>''')
n=4
for k in "ABC":
    p=PAL[k];i=INFO[k]
    pg.append(f'''<section class="pg" style="padding:0"><div class="box" style="position:absolute;left:0;top:0;bottom:0;width:690px;background:{p["paper"]}"><img src="{u(k,"horizontal","couleur")}" style="max-width:84%"></div>
<div style="position:absolute;left:690px;right:0;top:0;bottom:0;padding:56px 52px 0 46px"><div class="k">Proposition {k}</div><h2>{i["t"]}</h2><p style="color:#666">{i["sub"]}</p>
<h3>L’idée</h3><p>{i["idea"]}</p><h3>Pourquoi</h3><ul>{"".join(f"<li>{x}</li>" for x in i["why"])}</ul><h3>Points de vigilance</h3><p>{i["vig"]}</p></div>{foot(n)}</section>'''); n+=1
    pg.append(f'''<section class="pg"><div class="k">Proposition {k} · Déclinaisons</div><h2>{i["t"]} : le système</h2>
<div style="display:grid;grid-template-columns:1.25fr 1fr 1fr;gap:12px;margin-top:16px">
<div><div class="box" style="height:210px;background:{p["paper"]}"><img src="{u(k,"horizontal","couleur")}"></div><div class="lab">Horizontal · couleur</div></div>
<div><div class="box" style="height:210px;background:{p["ink"]}"><img src="{u(k,"vertical","negatif")}" style="max-height:82%"></div><div class="lab">Vertical · négatif</div></div>
<div><div class="box" style="height:210px;background:{p["paper"]}"><img src="{u(k,"symbole","couleur")}" style="max-height:66%"></div><div class="lab">Symbole seul</div></div>
<div><div class="box" style="height:170px;background:#fff;border:1px solid #e3e3e3"><img src="{u(k,"horizontal","noir")}"></div><div class="lab">Noir · une couleur</div></div>
<div><div class="box" style="height:170px;background:{p["ink"]}"><img src="{u(k,"symbole","negatif")}" style="max-height:62%"></div><div class="lab">Symbole · négatif</div></div>
<div><div class="box" style="height:170px;background:{p["paper"]};gap:18px;align-items:flex-end;padding-bottom:26px"><img src="{u(k,"horizontal","couleur")}" style="width:170px;max-width:none"><img src="{u(k,"horizontal","couleur")}" style="width:105px;max-width:none"><img src="{u(k,"symbole","couleur")}" style="width:34px;max-width:none"><img src="{u(k,"symbole","couleur")}" style="width:20px;max-width:none"></div><div class="lab">Petites tailles</div></div></div>
<div style="display:grid;grid-template-columns:1.25fr 2fr;gap:30px;margin-top:8px"><div><h3>Couleurs</h3><div style="display:flex;gap:8px"><div style="flex:1.4;height:54px;background:{p["ink"]};color:#fff;font-size:10px;padding:8px;font-weight:600">{p["ink"]}</div><div style="flex:1;height:54px;background:{p["acc"]};font-size:10px;padding:8px;font-weight:600">{p["acc"]}</div><div style="flex:1;height:54px;background:{p["paper"]};border:1px solid #e3e3e3;font-size:10px;padding:8px;font-weight:600">{p["paper"]}</div></div><p style="font-size:11.5px;color:#666;margin-top:6px">{p["nom"]}</p></div>
<div><h3>Typographie</h3><div style="font-family:{i["fam"]};font-size:34px;line-height:1.1">Châlons Champagne Events</div><p style="font-size:11.5px;color:#666;margin-top:6px">{i["typo"]} Polices sous licence libre (OFL), utilisables en impression comme sur le web.</p></div></div>{foot(n)}</section>'''); n+=1
    pg.append(f'''<section class="pg" style="background:#ecebe8"><div class="k">Proposition {k} · Aperçus</div><h2>{i["t"]} en situation</h2>
<div style="display:flex;gap:34px;margin-top:26px;align-items:center"><div class="card" style="background:{p["ink"]}"><div class="box" style="position:absolute;inset:0"><img src="{u(k,"symbole","negatif")}" style="max-height:46%"></div></div>
<div class="card" style="background:{p["paper"]}"><img src="{u(k,"horizontal","couleur")}" style="position:absolute;left:24px;top:24px;width:190px"><div style="position:absolute;left:24px;bottom:22px;font-size:10.5px;line-height:1.6;color:{p["ink"]}"><b style="font-size:13px">Prénom Nom</b><br>Fonction<br>00 00 00 00 00 · prenom.nom@exemple.fr</div></div>
<div style="flex:1"><div style="display:flex;gap:16px;align-items:center">{"".join(f'<div class="box" style="width:{s}px;height:{s}px;border-radius:50%;background:{p["ink"]};flex:none"><img src="{u(k,"symbole","negatif")}" style="max-width:62%;max-height:62%"></div>' for s in (110,64,36))}</div><div class="lab" style="margin-top:12px">Avatar (LinkedIn, messagerie)</div></div></div>
<div style="margin-top:34px;height:230px;background:{p["ink"]};position:relative;box-shadow:0 14px 30px -10px rgba(0,0,0,.3)"><img src="{u(k,"horizontal","negatif")}" style="position:absolute;left:44px;top:50%;transform:translateY(-50%);height:118px"><div style="position:absolute;right:54px;top:50%;transform:translateY(-50%);font-family:{i["fam"]};font-size:30px;color:{p["paper"]};text-align:right">{i["banner"]}</div></div>
<div class="lab" style="margin-top:10px">Carte de visite (recto, verso) · Bannière · Coordonnées fictives, aperçus de principe</div>{foot(n)}</section>'''); n+=1
pg.append(f'''<section class="pg"><div class="k">03 · Dans vos couleurs</div><h2>Les trois propositions en bleu nuit et or</h2><p style="color:#666">Pour comparer les formes à couleurs égales. La proposition A est conçue dans ces couleurs ; B et C peuvent les adopter.</p>
<div style="display:grid;grid-template-columns:1fr;gap:10px;margin-top:14px">{"".join(f'<div class="box" style="height:176px;background:{PAL["A"]["paper"]};justify-content:flex-start;padding-left:60px"><img src="{u(k,"horizontal","couleur" if k=="A" else "bleu-or")}" style="max-height:70%;max-width:60%"><span style="position:absolute;right:90px;font-size:12px;font-weight:700;letter-spacing:2px;color:#9a9a9a">{k} · {INFO[k]["t"].upper()}</span></div>' for k in "ABC")}</div>{foot(n)}</section>'''); n+=1
pg.append(f'''<section class="pg"><div class="k">04 · Pour décider</div><h2>Comment choisir</h2>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:20px">
<div><h3>A · Le Monogramme</h3><p><b>Si vous tenez à vos couleurs et au sigle.</b> La transition la plus douce avec ce que vous avez imaginé. Moderne et direct.</p></div>
<div><h3>B · Les Arches</h3><p><b>Si vous voulez vous distinguer.</b> La seule qui parle de Châlons. Le symbole le plus robuste et le plus mémorisable.</p></div>
<div><h3>C · Le Sceau</h3><p><b>Si vous visez le prestige avant tout.</b> Le registre des grandes maisons. La plus classique des trois.</p></div></div>
<h3 style="margin-top:34px">Notre recommandation</h3><p style="max-width:860px">La proposition <b>B, Les Arches</b>, pour sa singularité et son ancrage local. Elle peut être déclinée en bleu nuit et or si vous souhaitez conserver vos couleurs.</p>
<h3 style="margin-top:26px">Les étapes suivantes</h3><ul><li>Choix d’une proposition et retours sur les ajustements souhaités</li><li>Mise au point finale du dessin et des espacements</li><li>Recherche d’antériorités et dépôt éventuel de la marque (INPI)</li><li>Livraison des fichiers (vectoriels, web, impression) et d’une charte d’utilisation</li></ul>{foot(n)}</section>''')
open("client.html","w").write(f'<html><head><meta charset=utf-8><style>{css}</style></head><body>{"".join(pg)}</body></html>')
