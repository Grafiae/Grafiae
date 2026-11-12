import os, math
from pro import *
from client import textA, textB, textC, PAL, svg
F="file:///tmp/claude-0/-home-user-Grafiae/505c24ee-2e35-5947-935f-cfc53e082e9e/scratchpad/build/fonts2/"
OUT="/home/user/Grafiae/cce-logo/client/recherche-pro"; os.makedirs(OUT+"/svg",exist_ok=True)
VB={"1":126,"2":100,"3":124}
SLUG={"1":"rencontre","2":"rosace","3":"arcade"}
G='stroke="#D0433B" stroke-width="0.7" fill="none"'
def guides(num,kw):
    o=""
    if num=="1":
        W,top,bot,a,b,rc,h=100,kw.get("top",-62),kw.get("bot",104),kw["a"],kw["b"],kw["rc"],kw["h"]
        o+=f'<rect x="{-W}" y="{top}" width="{2*W}" height="{bot-top}" {G}/><path d="M0 {top-70}V{bot+14}M{-W-14} {top}H{W+14}M{-W-14} {top+b}H{W+14}" {G} stroke-dasharray="4 3"/>'
        o+=f'<ellipse cx="0" cy="{top}" rx="{a}" ry="{b}" {G}/>'
        for m in(-1,1):
            o+=f'<circle cx="{m*(W+a)/2}" cy="{top-9-h}" r="{h}" {G}/><circle cx="{m*(W-rc)}" cy="{top+rc}" r="{rc}" {G}/><circle cx="{m*(W-rc)}" cy="{bot-rc}" r="{rc}" {G}/>'
    elif num=="2":
        N,D,r1,r2=kw["N"],kw["D"],kw["r1"],kw["r2"]
        o+=f'<circle r="{D}" {G} stroke-dasharray="4 3"/><circle r="{D+r2}" {G}/><circle r="{D-r2}" {G}/>'
        for k in range(N):
            x,y=pol(D,-90+k*360/N); x2,y2=pol(D+r2+8,-90+k*360/N)
            o+=f'<circle cx="{n(x)}" cy="{n(y)}" r="{r2}" {G}/><circle cx="{n(x)}" cy="{n(y)}" r="{r1}" {G}/><path d="M0 0L{n(x2)} {n(y2)}" {G} stroke-dasharray="4 3"/>'
    else:
        W,top,bot,d,pitch,hs,hr,g=100,-100,100,kw["d"],kw["pitch"],kw["hs"],kw["hr"],kw["g"]
        o+=f'<circle cx="0" cy="{top+W}" r="{W}" {G}/><path d="M{-W-12} {top+W}H{W+12}M0 {top-10}V{bot+24}" {G} stroke-dasharray="4 3"/>'
        for i in range(3):
            x=(i-1)*pitch; yt=bot-hs[i]
            o+=f'<path d="M{x-d/2} {yt-40}V{bot+8}M{x+d/2} {yt-40}V{bot+8}" {G} stroke-dasharray="4 3"/><circle cx="{x}" cy="{yt+d/2}" r="{d/2}" {G}/><circle cx="{x}" cy="{yt-g-hr}" r="{hr}" {G}/>'
    return o
def sym(num,fn,kw,I,A,P,size,extra=""): return tile(fn,kw,I,A,P,size=size,vb=VB[num],extra=extra)
# ---- fichiers SVG des retenues ----
c=PAL["A"]
for num,name,fn,its,keep in PISTES:
    vb=VB[num]; k=120/vb
    for kind,I,A,P,bg in(("couleur",NAVY,GOLD,PAPER,None),("negatif",PAPER,GOLD,NAVY,NAVY),("noir","#000","#000","#fff",None)):
        open(f"{OUT}/svg/piste{num}_{SLUG[num]}_symbole_{kind}.svg","w",encoding="utf-8").write(svg(f'<g transform="translate(140 144) scale({n(k)})">{fn(I,A,P,**keep)}</g>',280,280,f"{name} – symbole – {kind}",bg=bg))
        cc=dict(ink=I,acc=A,acc_text=(c["acc_text"] if kind=="couleur" else A),paper=P)
        t,w=textA(310,118,cc)
        open(f"{OUT}/svg/piste{num}_{SLUG[num]}_horizontal_{kind}.svg","w",encoding="utf-8").write(svg(f'<g transform="translate(150 144) scale({n(k)})">{fn(I,A,P,**keep)}</g>'+t,round(310+w+40),290,f"{name} – horizontal – {kind}",bg=bg))
        t,w=textA(330,372,cc,anchor="middle")
        open(f"{OUT}/svg/piste{num}_{SLUG[num]}_vertical_{kind}.svg","w",encoding="utf-8").write(svg(f'<g transform="translate(330 150) scale({n(k)})">{fn(I,A,P,**keep)}</g>'+t,660,540,f"{name} – vertical – {kind}",bg=bg))
# typographies sur la piste 3
fn3,keep3=PISTES[2][2],PISTES[2][4]
for key,tf in(("sans",textA),("capitales",textB),("didone",textC)):
    t,w=tf(310,118 if key!="didone" else 132,c)
    open(f"{OUT}/svg/piste3_arcade_typo-{key}.svg","w",encoding="utf-8").write(svg(f'<g transform="translate(150 144) scale({n(120/124)})">{fn3(NAVY,GOLD,PAPER,**keep3)}</g>'+t,round(310+w+40),290,f"Arcade – typo {key}"))
S="file://"+OUT+"/svg/"
css=f'''@font-face{{font-family:Man;src:url('{F}Manrope.ttf');font-weight:200 800}}
@page{{size:297mm 210mm;margin:0}}*{{box-sizing:border-box}}body{{margin:0;font-family:Man;color:#15305B}}
.pg{{width:1123px;height:794px;position:relative;overflow:hidden;page-break-after:always;background:#fff;padding:46px 56px}}
.k{{font-size:10.5px;letter-spacing:3.5px;font-weight:700;color:#96762F;margin-bottom:10px;text-transform:uppercase}}
h2{{font-size:32px;font-weight:800;letter-spacing:-.8px;margin:0 0 4px}}h3{{font-size:11.5px;letter-spacing:2.5px;font-weight:800;margin:14px 0 5px;text-transform:uppercase}}
p,li{{font-size:12.8px;line-height:1.5;margin:0 0 6px;color:#2b3550}}ul{{margin:0;padding-left:17px}}.s{{color:#6b7286}}
.foot{{position:absolute;left:56px;right:56px;bottom:22px;font-size:9px;letter-spacing:2.5px;font-weight:700;color:#9aa0ae;display:flex;justify-content:space-between;border-top:1px solid #e3e5ea;padding-top:8px}}
.it{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:14px}}.t{{background:{PAPER};padding:6px 10px 9px;position:relative;text-align:center}}.t svg{{display:block;margin:0 auto}}
.t b{{position:absolute;left:10px;top:8px;font-size:11px;letter-spacing:1px;color:#96762F}}.t span{{font-size:10.5px;font-weight:600;color:#4a5370;display:block;text-align:left}}.keep{{outline:2.5px solid {GOLD};outline-offset:-2.5px}}
.bx{{display:flex;align-items:center;justify-content:center}}.lab{{font-size:9px;letter-spacing:2px;font-weight:700;color:#9aa0ae;margin-top:5px;text-transform:uppercase}}
table{{width:100%;border-collapse:collapse;font-size:12.5px;margin-top:14px}}th{{font-size:10px;letter-spacing:2px;text-align:left;padding:8px 6px;border-bottom:2px solid {NAVY};text-transform:uppercase}}td{{padding:10px 6px;border-bottom:1px solid #e3e5ea}}td.d{{color:{GOLD};letter-spacing:3px;font-size:14px}}
'''
def foot(i): return f'<div class="foot"><span>Châlons Champagne Events · Recherche de symbole</span><span>{i}</span></div>'
def dots(v): return "●"*v+"○"*(5-v)
TXT={
"1":dict(idea="Deux personnes se font face. L’espace qui les sépare dessine une coupe de champagne : la rencontre d’affaires et le verre partagé ne font qu’une seule forme. Les têtes et les bulles sont les seuls éléments dorés.",
  lect=["Deux interlocuteurs : le rendez-vous, l’accord","Une coupe, en réserve entre eux","Trois bulles qui montent"],
  vig="Le lien avec Châlons est absent : il repose sur le nom. Le verre en réserve dans une forme pleine est un procédé connu (une de vos épingles l’utilise) : ici il naît de deux personnages, mais une recherche d’antériorités est indispensable."),
"2":dict(idea="Six convives, bras ouverts, forment un cercle. Chaque convive est aussi une coupe vue de face, tête en guise de bulle. L’ensemble dessine une rosace, comme celles des églises de Châlons, et rappelle une capsule de champagne.",
  lect=["Un groupe réuni en cercle : séminaire, table ronde","Six coupes levées","Une rosace, une capsule"],
  vig="Les rondes de personnages sont très répandues dans les logos d’événementiel (deux de vos références en sont) : c’est la piste la moins singulière. Elle se brouille sous 24 px."),
"3":dict(idea="Une grande arche pleine, dans laquelle trois portes en plein cintre sont découpées. Chaque porte, surmontée d’une bulle dorée, devient une personne. L’architecture de Châlons et le groupe accueilli sont la même forme ; un filet doré évoque le canal.",
  lect=["Trois personnes accueillies sous un même toit","Les arcades et les portes de Châlons","Des têtes-bulles, et la ligne d’eau"],
  vig="Le champagne n’est présent que par les bulles et l’or : c’est la lecture la plus discrète. Les trois silhouettes peuvent aussi évoquer un lieu de culte : à tester auprès de personnes extérieures."),
}
EVAL={"1":(4,4,5,1,4,3),"2":(3,5,3,3,4,2),"3":(5,4,2,5,5,4)}
pg=[]
pg.append(f'''<section class="pg" style="background:{NAVY};padding:0"><div style="position:absolute;right:70px;top:150px">{sym("3",arcade,A_KEEP,PAPER,GOLD,NAVY,470)}</div>
<div style="position:absolute;left:70px;top:270px;color:#fff"><div class="k" style="color:{GOLD}">Recherche de symbole · Proposition 1</div><div style="font-size:60px;font-weight:800;letter-spacing:-2px;line-height:1.02">Le monde,<br>Châlons,<br>le champagne</div><p style="color:#c9d0e0;font-size:16px;margin-top:22px">Trois pistes construites, bleu marine et or</p></div>
<div style="position:absolute;left:70px;bottom:44px;font-size:10px;letter-spacing:3px;color:#8d98b3;font-weight:700">CHÂLONS CHAMPAGNE EVENTS · TOURISME D’AFFAIRES · NOVEMBRE 2026</div></section>''')
pg.append(f'''<section class="pg"><div class="k">01 · Méthode</div><h2>Ce que le symbole doit réussir</h2>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:34px;margin-top:18px"><div><h3>Le cahier des charges</h3><ul><li>Montrer qu’il y a <b>du monde</b> : des personnes, un groupe</li><li>Parler à des <b>entreprises</b> : net, institutionnel</li><li>Évoquer <b>Châlons</b> et le <b>champagne</b></li><li>Bleu marine et or</li><li>S’inspirer des références sans en reprendre aucune</li></ul></div>
<div><h3>Ce que font vos références</h3><ul><li><b>Une seule idée</b> par symbole</li><li>Des <b>formes pleines</b>, pas des traits fins</li><li>Un <b>module répété</b> ou tourné (2, 3, 5 fois)</li><li>L’<b>espace vide</b> dessine autant que le plein</li><li>Des épaisseurs et des écarts constants</li></ul></div>
<div><h3>Notre règle de construction</h3><ul><li><b>La tête est une bulle</b> : seul élément doré</li><li><b>Le corps est une forme du sujet</b> : une coupe, une arche</li><li>Deux lectures au minimum par symbole</li><li>Tracé sur grille, cercles et droites uniquement</li><li>Lisible à 24 px, en une couleur</li></ul></div></div>
<h3 style="margin-top:26px">Les trois modules</h3><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px">
<div class="t"><svg viewBox="-70 -50 140 100" width="300" height="130"><circle r="20" fill="{GOLD}"/></svg><span>La bulle = la tête</span></div>
<div class="t"><svg viewBox="-70 -50 140 100" width="300" height="130"><path d="{ann(0,-14,18,38,0,180)}" fill="{NAVY}"/><circle cy="-18" r="13" fill="{GOLD}"/></svg><span>La coupe = les bras levés</span></div>
<div class="t"><svg viewBox="-70 -50 140 100" width="300" height="130"><path d="M-22 46V-6A22 22 0 0 1 22 -6V46Z" fill="{NAVY}"/><circle cy="-36" r="12" fill="{GOLD}"/></svg><span>L’arche = le corps, la porte</span></div></div>{foot(2)}</section>''')
i=3
for num,name,fn,its,keep in PISTES:
    tiles="".join(f'<div class="t {"keep" if j==7 else ""}"><b>{l}</b>{sym(num,fn,kw,NAVY,GOLD,PAPER,232)}<span>{lab}</span></div>' for j,(l,lab,kw) in enumerate(its))
    pg.append(f'<section class="pg"><div class="k">Piste {num} · Itérations</div><h2>{name} : huit essais de proportions</h2><div class="it">{tiles}</div>{foot(i)}</section>'); i+=1
    T=TXT[num]
    pg.append(f'''<section class="pg"><div class="k">Piste {num} · Version retenue</div><h2>{name}</h2>
<div style="display:grid;grid-template-columns:330px 330px 1fr;gap:16px;margin-top:12px">
<div><div class="bx" style="background:{PAPER};height:330px">{sym(num,fn,keep,NAVY,GOLD,PAPER,300)}</div><div class="lab">Symbole</div></div>
<div><div class="bx" style="background:#fff;border:1px solid #e3e5ea;height:330px"><svg viewBox="{-VB[num]-22} {-VB[num]-26} {2*VB[num]+44} {2*VB[num]+44}" width="318" height="318"><g opacity=".22">{fn(NAVY,NAVY,PAPER,**keep)}</g>{guides(num,keep)}</svg></div><div class="lab">Tracé de construction</div></div>
<div><h3 style="margin-top:0">L’idée</h3><p>{T["idea"]}</p><h3>Trois lectures</h3><ul>{"".join(f"<li>{x}</li>" for x in T["lect"])}</ul><h3>Points de vigilance</h3><p class="s">{T["vig"]}</p></div></div>
<div style="display:grid;grid-template-columns:1.5fr .7fr .7fr 1.1fr;gap:12px;margin-top:10px">
<div><div class="bx" style="background:{PAPER};height:190px"><img src="{S}piste{num}_{SLUG[num]}_horizontal_couleur.svg" style="width:88%"></div><div class="lab">Avec le nom</div></div>
<div><div class="bx" style="background:{NAVY};height:190px">{sym(num,fn,keep,PAPER,GOLD,NAVY,150)}</div><div class="lab">Négatif</div></div>
<div><div class="bx" style="background:#fff;border:1px solid #e3e5ea;height:190px">{sym(num,fn,keep,"#000","#000","#fff",150)}</div><div class="lab">Une couleur</div></div>
<div><div class="bx" style="background:{PAPER};height:190px;gap:20px;align-items:flex-end;padding-bottom:40px">{"".join(sym(num,fn,keep,NAVY,GOLD,PAPER,s) for s in (96,56,32,20))}</div><div class="lab">96 · 56 · 32 · 20 px</div></div></div>{foot(i)}</section>'''); i+=1
pg.append(f'''<section class="pg"><div class="k">04 · Les trois pistes avec le nom</div><h2>Trois logos à comparer</h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px">{"".join(f'<div class="bx" style="background:{PAPER};height:186px"><img src="{S}piste{nm}_{SLUG[nm]}_horizontal_couleur.svg" style="height:68%"></div><div class="bx" style="background:{NAVY};height:186px"><img src="{S}piste{nm}_{SLUG[nm]}_horizontal_negatif.svg" style="height:68%"></div>' for nm in "123")}</div>{foot(i)}</section>'''); i+=1
pg.append(f'''<section class="pg"><div class="k">05 · Typographie</div><h2>L’Arcade : trois registres pour le nom</h2>
<div style="display:grid;grid-template-columns:1fr;gap:10px;margin-top:14px">{"".join(f'<div class="bx" style="background:{PAPER};height:180px;justify-content:flex-start;padding-left:50px;position:relative"><img src="{S}piste3_arcade_typo-{k}.svg" style="height:70%"><div style="position:absolute;right:40px;width:250px"><h3 style="margin:0 0 4px">{t}</h3><p class="s" style="font-size:11.5px">{d}</p></div></div>' for k,t,d in (("sans","Sans empattement","Manrope. Direct, contemporain, très lisible à l’écran. Le plus « entreprise »."),("capitales","Capitales romaines","Marcellus. Institutionnel, patrimonial : s’accorde avec l’architecture du symbole."),("didone","Didone","Bodoni Moda. Le registre du luxe et des étiquettes. Traits fins, donc plus fragile en petit.")))}</div>{foot(i)}</section>'''); i+=1
rows="".join(f'<tr><td><b>{nm} · {PISTES[int(nm)-1][1]}</b></td>'+"".join(f'<td class="d">{dots(v)}</td>' for v in EVAL[nm])+f'<td><b>{sum(EVAL[nm])}</b> / 30</td></tr>' for nm in "123")
pg.append(f'''<section class="pg"><div class="k">06 · Évaluation</div><h2>Notre lecture, critère par critère</h2>
<table><tr><th>Piste</th><th>Petit format</th><th>« Du monde »</th><th>Champagne</th><th>Châlons</th><th>Registre entreprise</th><th>Singularité</th><th>Total</th></tr>{rows}</table>
<p class="s" style="margin-top:8px">Notation du studio, sur 5. Elle est subjective : c’est une base de discussion.</p>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:20px"><div><h3>Recommandation</h3><p><b>L’Arcade</b> pour la proposition 1 : la plus lisible, la plus institutionnelle et la seule qui ne puisse appartenir qu’à Châlons. <b>La Rencontre</b> est l’alternative si le champagne doit se voir en premier.</p></div>
<div><h3>Pour affiner</h3><ul><li>Régler la taille et l’écart des têtes au dixième près, à l’œil</li><li>Tester trois ou cinq personnages, et la ligne d’eau avec ou sans</li><li>Dessiner le nom sur mesure (espacements, accent du Â)</li><li>Recherche d’antériorités (INPI, recherche par image)</li></ul></div></div>{foot(i)}</section>''')
open("pro.html","w").write(f'<html><head><meta charset=utf-8><style>{css}</style></head><body>{"".join(pg)}</body></html>')
