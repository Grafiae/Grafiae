import os
from pont import *
from client import textA, svg
OUT="/home/user/Grafiae/cce-logo/client/pont"; os.makedirs(OUT+"/svg",exist_ok=True)
F="file:///tmp/claude-0/-home-user-Grafiae/505c24ee-2e35-5947-935f-cfc53e082e9e/scratchpad/build/fonts2/"
FIN={"A":("Le Reflet",dict(rs=(30,35,40),p=18,a=28,span=15,hr=11,hb=8)),
     "B":("Le Filet d’or",dict(rs=(30,35,40),p=18,a=28,span=15,hr=11,hb=8,reflect="ring",lcol=None))}
NEG=dict(I=PAPER,A=GOLD,P=NAVY,Tn="#2C4775")
def colors(kind):
    if kind=="couleur": return dict(I=NAVY,A=GOLD,P=PAPER,Tn=TINT)
    if kind=="negatif": return NEG
    return dict(I="#000",A="#000",P="#fff",Tn="#000")
def symbol(key,kind):
    kw=dict(FIN[key][1]); c=colors(kind)
    if key=="B": kw["lcol"]=c["I"]
    if kind=="noir" and key=="A": kw["reflect"]="lines"
    body,W,H=pont2(c["I"],c["A"],c["P"],Tn=c["Tn"],**kw)
    return body,W,H
for key in "AB":
    for kind in("couleur","negatif","noir"):
        body,W,H=symbol(key,kind); c=colors(kind)
        y0=-(H+2*8+6+22)-14; y1=46; x0=-W/2-24
        bg=c["P"] if kind=="negatif" else None
        sw,sh=W+48,y1-y0
        open(f"{OUT}/svg/pont{key}_symbole_{kind}.svg","w",encoding="utf-8").write(svg(f'<g transform="translate({n(-x0)} {n(-y0)})">{body}</g>',round(sw),round(sh),f"Pont {key} – symbole – {kind}",bg=bg))
        s=1.75; cc=dict(ink=c["I"],acc=c["A"],acc_text=("#96762F" if kind=="couleur" else c["A"]),paper=c["P"])
        tx=round(40+sw*s+30); t,w=textA(tx,round(40+sh*s/2-6),cc)
        open(f"{OUT}/svg/pont{key}_horizontal_{kind}.svg","w",encoding="utf-8").write(svg(f'<g transform="translate(40 40) scale({s})"><g transform="translate({n(-x0)} {n(-y0)})">{body}</g></g>'+t,round(tx+w+40),round(sh*s+80),f"Pont {key} – horizontal – {kind}",bg=bg))
        VW=max(round(sw*s+80),700); t,w=textA(VW/2,round(40+sh*s+90),cc,anchor="middle")
        open(f"{OUT}/svg/pont{key}_vertical_{kind}.svg","w",encoding="utf-8").write(svg(f'<g transform="translate({n((VW-sw*s)/2)} 40) scale({s})"><g transform="translate({n(-x0)} {n(-y0)})">{body}</g></g>'+t,VW,round(40+sh*s+90+150),f"Pont {key} – vertical – {kind}",bg=bg))
S="file://"+OUT+"/svg/"
def it(l,name,note,kw):
    keep=' style="outline:3px solid #C9A35A;outline-offset:-3px"' if l=="h" else ""
    return f'<div class="c"{keep}><svg viewBox="-180 -128 360 200" width="100%">{P2(NAVY,GOLD,PAPER,**kw)}</svg><div class="l"><b>{l}</b> {name}<p>{note}</p></div></div>'
grid="".join(it(*t) for t in TESTS2)
fin=""
for key in "AB":
    name=FIN[key][0]
    fin+=f'''<div class="f"><div class="fh"><b>Finaliste {key}</b> · {name}</div>
<div class="row"><div class="bx" style="background:{PAPER};flex:1.55"><img src="{S}pont{key}_horizontal_couleur.svg" style="width:88%"></div>
<div class="bx" style="background:{NAVY};flex:1"><img src="{S}pont{key}_vertical_negatif.svg" style="height:86%"></div></div>
<div class="row" style="height:150px"><div class="bx" style="background:#fff;border:1px solid #e3e5ea;flex:1"><img src="{S}pont{key}_symbole_noir.svg" style="width:70%"></div>
<div class="bx" style="background:{NAVY};flex:1"><img src="{S}pont{key}_symbole_negatif.svg" style="width:70%"></div>
<div class="bx" style="background:{PAPER};flex:1.3;gap:22px;align-items:flex-end;padding-bottom:30px">{"".join(f'<img src="{S}pont{key}_symbole_couleur.svg" style="width:{w}px">' for w in (130,80,46,30))}</div></div></div>'''
html=f'''<html><head><meta charset=utf-8><style>@font-face{{font-family:Man;src:url('{F}Manrope.ttf');font-weight:200 800}}
body{{margin:0;width:2200px;background:#ECE8DF;font-family:Man;color:{NAVY};padding:60px;box-sizing:border-box}}
h1{{font-size:46px;margin:0;letter-spacing:-1.2px}}.sub{{font-size:15px;letter-spacing:3.5px;color:#96762F;font-weight:700;margin:10px 0 8px}}.intro{{font-size:17px;line-height:1.55;color:#3b4560;max-width:1500px;margin:0 0 30px}}
h2{{font-size:24px;margin:42px 0 16px;letter-spacing:-.4px}}.g{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}.c{{background:{PAPER};padding:16px 18px 14px}}
.l{{font-size:19px;font-weight:800;margin-top:4px}}.l b{{font-size:12px;letter-spacing:2px;color:#96762F;margin-right:6px}}.l p{{font-size:14px;font-weight:500;color:#555c70;margin:4px 0 0;line-height:1.4}}
.fs{{display:grid;grid-template-columns:1fr 1fr;gap:26px}}.f{{display:flex;flex-direction:column;gap:12px}}.fh{{font-size:21px;font-weight:600}}.fh b{{font-weight:800}}
.row{{display:flex;gap:12px;height:320px}}.bx{{display:flex;align-items:center;justify-content:center;overflow:hidden}}
.notes{{display:grid;grid-template-columns:repeat(3,1fr);gap:30px;margin-top:40px;font-size:15px;line-height:1.55;color:#3b4560}}.notes h3{{font-size:13px;letter-spacing:2.5px;color:{NAVY};margin:0 0 8px}}
</style></head><body><h1>Châlons Champagne Events · Test « Le Pont »</h1><div class="sub">CCE DANS LES ARCHES · BLEU MARINE ET OR · 8 ITÉRATIONS, 2 FINALISTES</div>
<p class="intro">Un pont de Châlons sur le canal. Chaque arche et son reflet dans l’eau forment un cercle : une bulle de champagne, qui porte une lettre du sigle. Sur le tablier, trois convives : il y a du monde. Les bulles grandissent de gauche à droite, comme le perlage qui monte dans un verre.</p>
<h2>Itérations</h2><div class="g">{grid}</div><h2>Les deux finalistes</h2><div class="fs">{fin}</div>
<div class="notes"><div><h3>CE QUI NOUS DISTINGUE DE LA RÉFÉRENCE</h3>Pas de tablier en dos d’âne ni de piles évasées. Pas d’alternance de têtes et d’arches. Notre idée est ailleurs : le reflet qui ferme chaque arche en bulle, et le sigle CCE dans les bulles.</div>
<div><h3>CE QUI RESTE À RÉGLER</h3>Taille des lettres dans les bulles, écart entre têtes et épaules, épaisseur de la ligne d’eau. En dessous de 30 px, les lettres disparaissent : prévoir une version simplifiée sans lettres.</div>
<div><h3>VIGILANCE</h3>Le pont à trois arches et les personnages en tête ronde sont des motifs connus : une recherche d’antériorités (INPI, image inversée) reste nécessaire avant de présenter au client.</div></div></body></html>'''
open("pont_board.html","w").write(html)
