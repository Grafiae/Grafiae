import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from designs import *

OUT = "/home/user/Grafiae/cce-logo/svg"
os.makedirs(OUT, exist_ok=True)

def write(name, body, W, H, ckey, title):
    c = COLORS[ckey]
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(svg_doc(body, W, H, c, title))

for num, slug, label, fn in PISTES:
    for ck, c in COLORS.items():
        body, W, H = fn(c)
        write(f"piste{num}_{slug}_{ck}", body, W, H, ck, f"CCE – Piste {num} {label} ({ck})")
# variantes complémentaires
for ck, c in COLORS.items():
    body, W, H = d1_plaque(c, simple=True)
    write(f"piste01_plaque_sceau-simple_{ck}", body, W, H, ck, f"CCE – Sceau simplifié ({ck})")
    body, W, H = d4_signature(c, monogram=True)
    write(f"piste04_signature_monogramme_{ck}", body, W, H, ck, f"CCE – Monogramme manuscrit ({ck})")
    body, W, H = d5_arcade(c, tagline=False)
    write(f"piste05_arcade_symbole_{ck}", body, W, H, ck, f"CCE – Arcade symbole seul ({ck})")
print(sorted(os.listdir(OUT)))

from designs2 import PISTES2
for num, slug, label, fn in PISTES2:
    for ck, c in COLORS.items():
        body, W, H = fn(c)
        write(f"piste{num}_{slug}_{ck}", body, W, H, ck, f"CCE – Piste {num} {label} ({ck})")
