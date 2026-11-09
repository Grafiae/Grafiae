import os, sys, json, html as _h
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from designs import *
from designs2 import PISTES2

OUT = "/home/user/Grafiae/cce-logo/tests"
G_OR   = ["#8B6420", "#D8B766", "#B08130", "#DDBF74", "#97712A"]
G_ORB  = ["#B8892F", "#F0D68F", "#CFA24A", "#F6E4B0", "#B98B33"]
G_ROSE = ["#9A5A44", "#E9B9A0", "#C27C5E", "#F1CDB8", "#A9654C"]
G_ARG  = ["#7F8794", "#EEF1F6", "#A9B1BF", "#F7F9FC", "#8A92A0"]
G_CUI  = ["#8A4A2A", "#E0A27A", "#B8693E", "#EDBE97", "#9A5530"]
G_AMB  = ["#B8741B", "#F0B95A", "#D9962B", "#F5CE82", "#B8741B"]
G_PAL  = ["#9C7F3B", "#E0C98B", "#BD9A4C", "#E8D6A3", "#A8883F"]
POS = [0, 0.28, 0.5, 0.74, 1]

PALETTES = [
    ("bordeaux-rose",   "Bordeaux & rose poudré", "#F4E1DC", "#5B1A2B", G_ROSE),
    ("bleu-nuit-argent","Bleu nuit & argent",     "#0F1B33", "#EEF1F6", G_ARG),
    ("noir-or",         "Noir & or",              "#0C0C0D", "#F3EBDA", G_ORB),
    ("bleu-canal-cuivre","Bleu canal & cuivre",   "#F1EDE3", "#1F3A5F", G_CUI),
    ("violet-pinot",    "Violet pinot & or",      "#F4EEE6", "#3B2050", G_OR),
    ("vert-canal-ambre","Vert canal & ambre",     "#EAF0EC", "#0E3B3A", G_AMB),
    ("coquelicot",      "Coquelicot & encre",     "#FBF3E4", "#1C1C1C", "#E4462F"),
    ("sauge-craie",     "Sauge & craie",          "#EEF0E6", "#3F5A45", G_PAL),
    ("rose-nuit",       "Rose nuit",              "#2A0F1A", "#F6DDD5", G_ROSE),
]

def doc(body, W, H, bg, grad, title):
    pad = round(0.07 * max(W, H))
    W2, H2 = W + 2 * pad, H + 2 * pad
    if isinstance(grad, list):
        stops = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in zip(POS, grad))
        defs = f'<defs><linearGradient id="or" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W2}" y2="{H2}">{stops}</linearGradient></defs>'
    else:
        defs = ""
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W2} {H2}" width="{W2}" height="{H2}">'
            f'<title>{_h.escape(title)}</title>{defs}<rect id="fond" width="{W2}" height="{H2}" fill="{bg}"/><g id="logo" transform="translate({pad} {pad})">{body}</g></svg>')

ALL = [(n, s, l, f) for (n, s, l, f) in PISTES] + [(n, s, l, f) for (n, s, l, f) in PISTES2]
manifest = []
for i, (num, slug, label, fn) in enumerate(ALL):
    for k in range(4):
        pid, plabel, bg, ink, grad = PALETTES[(i + 2 * k) % len(PALETTES)]
        c = dict(ink=ink, gold=("url(#or)" if isinstance(grad, list) else grad), bg=None, paper=bg)
        body, W, H = fn(c)
        name = f"piste{num}_{slug}_{pid}"
        open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(doc(body, W, H, bg, grad, f"CCE – {label} – {plabel}"))
        manifest.append(dict(file=name, num=num, label=label, palette=plabel, bg=bg, ink=ink))
json.dump(manifest, open("manifest.json", "w"), ensure_ascii=False, indent=1)
print(len(manifest), "tests")
