"""Planche de recherches : « du monde » + Châlons + champagne, bleu marine et or."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from lib import n
from client import T, MAN7, PAL, textA, svg
from lib import Font
MAN8 = Font("Manrope[wght].ttf", 800)
NAVY, GOLD, PAPER = "#15305B", "#C9A35A", "#FBF8F1"

def st(d, col, sw, cap="round"):
    return f'<path d="{d}" stroke="{col}" stroke-width="{n(sw)}" fill="none" stroke-linecap="{cap}" stroke-linejoin="round"/>'
def dot(x, y, r, col):
    return f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(r)}" fill="{col}"/>'
def rot(body, deg, cx=0, cy=0):
    return f'<g transform="rotate({n(deg)} {n(cx)} {n(cy)})">{body}</g>'
def pol(r, deg):
    a = math.radians(deg); return r * math.cos(a), r * math.sin(a)

def s01(I, A):   # arches-convives
    o = ""
    for x, top in ((-72, -6), (0, -40), (72, -6)):
        o += st(f"M{x-26} 92V{top+26}A26 26 0 0 1 {x+26} {top+26}V92", I, 15, "butt") + dot(x, top - 30, 15, A)
    return o
def coupe(x, y0, I, A, base=88):
    return (st(f"M{x-27} {y0}A27 27 0 0 0 {x+27} {y0}", I, 13) + st(f"M{x} {y0+27}V{base}M{x-19} {base}H{x+19}", I, 13) + dot(x, y0 - 8, 12, A))
def s02(I, A):   # coupes-convives
    return coupe(-74, -8, I, A) + coupe(0, -36, I, A) + coupe(74, -8, I, A)
def s03(I, A):   # la ronde
    o = ""
    for k in range(5):
        o += rot(st("M-25 -62A25 25 0 0 0 25 -62", I, 14) + dot(0, -70, 11, A), k * 72)
    return o + dot(0, 0, 9, I)
def s04(I, A):   # rosace
    o = ""
    for k in range(8):
        o += rot(st("M-12 -32V-66A12 12 0 0 1 12 -66V-32", I, 8.5, "butt") + dot(0, -97, 8, A), k * 45)
    return o + dot(0, 0, 11, A)
def s05(I, A):   # CCE = trois personnes
    o = ""
    for x, ch in ((-88, "C"), (0, "C"), (84, "E")):
        o += T(MAN8, ch, 118, x, 86, I, anchor="middle")[0] + dot(x, -36, 16, A)
    return o
def s06(I, A):   # le pont
    o = st("M-102 34A34 34 0 0 1 -34 34A34 34 0 0 1 34 34A34 34 0 0 1 102 34", I, 14) + st("M-102 34V72M-34 34V72M34 34V72M102 34V72", I, 14, "butt")
    for x in (-68, 0, 68):
        o += dot(x, -32, 14, A)
    return o + st("M-112 96H112", A, 5)
def s07(I, A):   # l'assemblée dans la coupe
    o = st("M-92 -22A92 92 0 0 0 92 -22", I, 14) + st("M0 70V104M-34 104H34", I, 14)
    for x, y in ((-46, -52), (0, -74), (46, -52)):
        o += dot(x, y, 14, A) + st(f"M{x-21} {y+44}A21 21 0 0 1 {x+21} {y+44}", I, 12)
    return o
def s08(I, A):   # l'ascension
    o = ""
    for x, y, k in ((-66, 62, .62), (-12, 12, .88), (56, -48, 1.18)):
        o += dot(x, y, 15 * k, A) + st(f"M{n(x-28*k)} {n(y+56*k)}A{n(28*k)} {n(28*k)} 0 0 1 {n(x+28*k)} {n(y+56*k)}", I, 14 * k)
    return o
def s09(I, A):   # la table ronde
    o = f'<circle cx="0" cy="0" r="27" stroke="{I}" stroke-width="10" fill="none"/>'
    for k in range(6):
        d = -90 + k * 60
        x, y = pol(60, d)
        (x0, y0), (x1, y1) = pol(90, d - 19), pol(90, d + 19)
        o += dot(x, y, 12, A) + st(f"M{n(x0)} {n(y0)}A90 90 0 0 1 {n(x1)} {n(y1)}", I, 13)
    return o
def s10(I, A):   # la grande arche
    o = st("M-84 98V-14A84 84 0 0 1 84 -14V98", I, 13, "butt")
    for x, y in ((-42, 14), (0, -14), (42, 14)):
        o += dot(x, y, 13, A) + f'<path d="M{x-17} 98V{y+38}A17 17 0 0 1 {x+17} {y+38}V98Z" fill="{I}"/>'
    return o
def s11(I, A):   # le jaillissement
    o = ""
    for d, L, r in ((0, 150, 14), (-24, 132, 12), (24, 132, 12), (-48, 108, 10), (48, 108, 10)):
        a = math.radians(-90 + d)
        x0, y0 = 42 * math.cos(a), 96 + 42 * math.sin(a)
        x1, y1 = L * math.cos(a), 96 + L * math.sin(a)
        x2, y2 = (L + r + 9) * math.cos(a), 96 + (L + r + 9) * math.sin(a)
        o += st(f"M{n(x0)} {n(y0)}L{n(x1)} {n(y1)}", I, 12) + dot(x2, y2, r, A)
    return o + st("M-26 98H26", I, 12)
def s12(I, A):   # le toast
    return rot(coupe(-40, -20, I, A, 92), 16, -40, 92) + rot(coupe(40, -20, I, A, 92), -16, 40, 92) + dot(0, -84, 6, A) + dot(-14, -104, 4, A) + dot(13, -108, 4.5, A)

S = [("01", "Les Arches", "Chaque convive est une arche de Châlons. Tête = bulle.", s01),
     ("02", "Les Coupes", "Bras levés = coupe, tête = bulle. Double lecture.", s02),
     ("03", "La Ronde", "Cinq convives en cercle, bras ouverts.", s03),
     ("04", "La Rosace", "Rosace d’église faite d’arches et de convives.", s04),
     ("05", "Le Sigle habité", "C, C, E : trois lettres, trois personnes.", s05),
     ("06", "Le Pont", "Trois personnes reliées par un pont sur le canal.", s06),
     ("07", "L’Assemblée", "Un groupe réuni dans une coupe.", s07),
     ("08", "L’Ascension", "Des convives qui montent comme des bulles.", s08),
     ("09", "La Table ronde", "Réunion vue du dessus, façon capsule.", s09),
     ("10", "La Porte", "Un groupe accueilli sous une arche.", s10),
     ("11", "Le Jaillissement", "Une gerbe de champagne, ou un groupe qui se lève.", s11),
     ("12", "Le Toast", "Deux personnes-coupes qui trinquent.", s12)]

if __name__ == "__main__":
    OUT = "/home/user/Grafiae/cce-logo/client/recherches"
    os.makedirs(OUT, exist_ok=True)
    for num, name, note, fn in S:
        for kind, I, A, bg in (("couleur", NAVY, GOLD, None), ("negatif", PAPER, GOLD, NAVY)):
            body = f'<g transform="translate(150 150)">{fn(I, A)}</g>'
            open(f"{OUT}/recherche{num}_{kind}.svg", "w", encoding="utf-8").write(svg(body, 300, 300, f"Recherche {num} – {name}", bg=bg))
    # logos complets pour 3 favoris
    c = PAL["A"]
    for num in ("01", "02", "09"):
        fn = [s for s in S if s[0] == num][0][3]
        t, w = textA(330, 128, c)
        body = f'<g transform="translate(150 150)">{fn(c["ink"], c["acc"])}</g>' + t
        open(f"{OUT}/logo{num}_horizontal.svg", "w", encoding="utf-8").write(svg(body, round(330 + w + 40), 300, f"Logo recherche {num}"))
    print("ok")
