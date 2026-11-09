import os, sys, json, html as _h
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from designs3 import PISTES3
G_ORB  = ["#B8892F", "#F0D68F", "#CFA24A", "#F6E4B0", "#B98B33"]
G_ROSE = ["#B98472", "#F2D2C6", "#D9A592", "#F6DDD3", "#B98472"]
G_CUI  = ["#8A4A2A", "#E0A27A", "#B8693E", "#EDBE97", "#9A5530"]
POS = [0, 0.28, 0.5, 0.74, 1]
PAL = [
    ("noir-or", "Noir & or", "#111112", "#F3EBDA", G_ORB),
    ("bleu-cobalt", "Bleu cobalt monochrome", "#F7F5EE", "#1F3FB0", "#7C9BE0"),
    ("bleu-ciel", "Bleu ciel & ivoire", "#4479C0", "#FFFFFF", "#F2E7C9"),
    ("brique-poudre", "Brique & rose poudré", "#EBD9D1", "#A12B35", "#A12B35"),
    ("brun-cuivre", "Brun & cuivre", "#FAF8F3", "#6E3B22", G_CUI),
    ("rose-noir", "Rose doré sur noir", "#1A1A1C", "#EBC9BC", G_ROSE),
    ("marine-or", "Marine & or champagne", "#14214A", "#F4ECDB", G_ORB),
]
def doc(body, W, H, bg, grad, title):
    pad = round(0.07 * max(W, H)); W2, H2 = W + 2 * pad, H + 2 * pad
    defs = ""
    if isinstance(grad, list):
        stops = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in zip(POS, grad))
        defs = f'<defs><linearGradient id="or" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W2}" y2="{H2}">{stops}</linearGradient></defs>'
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W2} {H2}" width="{W2}" height="{H2}">'
            f'<title>{_h.escape(title)}</title>{defs}<rect id="fond" width="{W2}" height="{H2}" fill="{bg}"/><g id="logo" transform="translate({pad} {pad})">{body}</g></svg>')
OUT = "/home/user/Grafiae/cce-logo/tests3"
os.makedirs(OUT, exist_ok=True)
man = []
for i, (num, slug, label, fn) in enumerate(PISTES3):
    for k in range(5):
        pid, pl, bg, ink, grad = PAL[(i + k) % len(PAL)]
        c = dict(ink=ink, gold=("url(#or)" if isinstance(grad, list) else grad), bg=None, paper=bg)
        body, W, H = fn(c)
        name = f"piste{num}_{slug}_{pid}"
        open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(doc(body, W, H, bg, grad, f"CCE – {label} – {pl}"))
        man.append(dict(file=name, num=num, label=label, palette=pl, bg=bg, ink=ink))
json.dump(man, open("manifest3.json", "w"), ensure_ascii=False, indent=1)
print(len(man), "variantes")
