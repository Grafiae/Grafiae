"""Tests « pont » : CCE intégré dans les arches. Centre (0,0) = milieu de la ligne d'eau."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from lib import n, Font
from client import T, BOD, MAN7
MAN8 = Font("Manrope[wght].ttf", 800)
NAVY, GOLD, PAPER, TINT = "#15305B", "#C9A35A", "#FBF8F1", "#D5DBE6"

def dot(x, y, r, c): return f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(r)}" fill="{c}"/>'
def letter(font, ch, size, cx, cy, col):
    capH = font.cap * size / font.upm
    return T(font, ch, size, cx, cy + capH / 2, col, anchor="middle")[0]
def opening(x, r, wl, rect=0):
    return f"M{n(x-r)} {n(wl)}V{n(wl-rect)}A{n(r)} {n(r)} 0 0 1 {n(x+r)} {n(wl-rect)}V{n(wl)}Z"

def pont(I, A, P, Tn=TINT, style="sigle", r=34, rect=18, pitch=86, W=142, deck=24, camber=0,
         heads=True, hr=12, hgap=12, font="man", reflet=False, mid=1.0, ripples=False, bubbles=0, wlgold=True):
    o = []
    f = MAN8 if font == "man" else BOD
    xs = [-pitch, 0, pitch]
    rs = [r, r * mid, r]
    top = -(max(rs) + rect + deck)
    # tablier + tympan
    if camber:
        body = f"M{-W} 0V{n(top+camber)}Q0 {n(top-camber)} {W} {n(top+camber)}V0Z"
    else:
        body = f"M{-W} 0V{n(top)}H{W}V0Z"
    holes = "".join(opening(x, rr, 0, rect) for x, rr in zip(xs, rs))
    o.append(f'<path d="{body}{holes}" fill="{I}" fill-rule="evenodd"/>')
    if reflet:
        rb = f"M{-W} 0V{n(-top*0.62)}H{W}V0Z"
        rh = "".join(f"M{n(x-rr)} 0V{n(rect)}A{n(rr)} {n(rr)} 0 0 0 {n(x+rr)} {n(rect)}V0Z" for x, rr in zip(xs, rs))
        o.append(f'<path d="{rb}{rh}" fill="{Tn}" fill-rule="evenodd"/>')
    if ripples:
        for i, y in enumerate((10, 20, 30)):
            for x, rr in zip(xs, rs):
                hw = rr * (0.95 - i * 0.22)
                o.append(f'<path d="M{n(x-hw)} {y}H{n(x+hw)}" stroke="{A}" stroke-width="3" stroke-linecap="round"/>')
    if wlgold and not reflet:
        o.append(f'<path d="M{-W-14} 0H{W+14}" stroke="{A}" stroke-width="4"/>')
    # lettres
    for x, rr, ch in zip(xs, rs, "CCE"):
        cy = -rect * 0.5 - rr * 0.32 if not reflet else 0
        size = rr * (1.55 if font == "man" else 1.7) * (1.0 if not reflet else 1.25)
        o.append(letter(f, ch, size, x, cy, A))
    if heads:
        for x, rr in zip(xs, rs):
            yd = top - hgap - hr if not camber else top - camber * (1 - (x / W) ** 2) + camber - hgap - hr
            o.append(dot(x, yd, hr, A))
    for i in range(bubbles):
        o.append(dot(6 + i * 9, top - 18 - i * 22, 7 - i * 1.6, A))
    return "".join(o)

def pont_lettres(I, A, P, **k):
    """Les lettres tournées construisent le pont : C ∩, C ∩, E (П à trois pieds)."""
    t, o = 22, []
    for x in (-92, -8):
        R = 38
        o.append(f'<path d="M{x-R} 0V-30A{R} {R} 0 0 1 {x+R} -30V0H{x+R-t}V-30A{R-t} {R-t} 0 0 0 {x-R+t} -30V0Z" fill="{I}"/>')
    x0 = 46
    o.append(f'<path d="M{x0} 0V-68H{x0+86}V0H{x0+86-t}V-46H{n(x0+43+t/2)}V0H{n(x0+43-t/2)}V-46H{x0+t}V0Z" fill="{I}"/>')
    o.append(f'<path d="M-146 0H146" stroke="{A}" stroke-width="4"/>')
    for x in (-92, -8, 89):
        o.append(dot(x, -94, 12, A))
    return "".join(o)

TESTS = [
 ("01", "Le Pont-sigle", "Tablier droit, trois arches, une lettre dorée sous chaque arche.", pont, dict()),
 ("02", "Arche centrale haute", "L’arche du milieu domine, comme sur les ponts anciens.", pont, dict(mid=1.25, camber=8)),
 ("03", "Le Reflet", "Arche + reflet = cercle : trois bulles, une lettre dans chacune.", pont, dict(reflet=True, rect=0, r=36, heads=False, bubbles=3)),
 ("04", "Le Reflet habité", "Les trois bulles du reflet, et trois convives sur le pont.", pont, dict(reflet=True, rect=0, r=36)),
 ("05", "Reflet en traits d’eau", "Le reflet dessiné par des lignes d’eau dorées.", pont, dict(ripples=True, rect=0, r=36, wlgold=True)),
 ("06", "Le Pont didone", "Mêmes arches, lettres à forts contrastes.", pont, dict(font="bod", mid=1.15)),
 ("07", "Arches étroites", "Arches hautes et serrées, registre plus monumental.", pont, dict(r=26, rect=40, pitch=74, W=120)),
 ("08", "Les lettres-ponts", "Les lettres tournées construisent elles-mêmes le pont.", pont_lettres, dict()),
]

def pont2(I, A, P, Tn=TINT, rs=(34, 34, 34), p=20, a=30, bat=10, span=16, heads="shoulders", hr=11.5, hgap=6, hb=9,
          reflect="tint", font="man", lcol=None, parapet=False, bubbles=0, mono=False, lscale=0.95, lettersin=True):
    o = []
    f = MAN8 if font == "man" else BOD
    lcol = lcol or A
    W = sum(2 * r for r in rs) + 2 * p + 2 * a
    xs, x = [], -W / 2 + a
    for r in rs:
        xs.append(x + r); x += 2 * r + p
    top = -(max(rs) + span)
    d = f"M{n(-W/2)} 0L{n(-W/2+bat)} {n(top)}"
    if heads == "shoulders":
        for xc, r in zip(xs, rs):
            sw = r * 0.82
            d += f"H{n(xc-sw)}Q{n(xc)} {n(top-2*hb)} {n(xc+sw)} {n(top)}"
    d += f"H{n(W/2-bat)}L{n(W/2)} 0Z"
    d += "".join(f"M{n(xc-r)} 0A{n(r)} {n(r)} 0 0 1 {n(xc+r)} 0Z" for xc, r in zip(xs, rs))
    o.append(f'<path d="{d}" fill="{I}" fill-rule="evenodd"/>')
    H = -top
    if reflect == "tint":
        rd = f"M{n(-W/2)} 0L{n(-W/2+bat*0.7)} {n(H*0.78)}H{n(W/2-bat*0.7)}L{n(W/2)} 0Z"
        rd += "".join(f"M{n(xc-r)} 0A{n(r)} {n(r)} 0 0 0 {n(xc+r)} 0Z" for xc, r in zip(xs, rs))
        o.append(f'<path d="{rd}" fill="{Tn}" fill-rule="evenodd"/>')
    elif reflect == "lines":
        for i, yy in enumerate([5 + k * 8 for k in range(int(H * 0.78 / 8))]):
            segs, xl = [], -W / 2 + bat * 0.7 * (yy / (H * 0.78))
            for xc, r in zip(xs, rs):
                hw = math.sqrt(max(r * r - yy * yy, 0))
                segs.append((xl, xc - hw)); xl = xc + hw
            segs.append((xl, W / 2 - bat * 0.7 * (yy / (H * 0.78))))
            for s0, s1 in segs:
                if s1 - s0 > 2:
                    o.append(f'<path d="M{n(s0)} {n(yy)}H{n(s1)}" stroke="{I}" stroke-width="3.2"/>')
    elif reflect == "ring":
        for xc, r in zip(xs, rs):
            o.append(f'<path d="M{n(xc-r)} 0A{n(r)} {n(r)} 0 0 0 {n(xc+r)} 0" stroke="{A}" stroke-width="3.5" fill="none"/>')
    xl, wd = -W / 2 - 16, ""
    for xc, r in zip(xs, rs):
        wd += f"M{n(xl)} 0H{n(xc-r-5)}"; xl = xc + r + 5
    wd += f"M{n(xl)} 0H{n(W/2+16)}"
    o.append(f'<path d="{wd}" stroke="{A}" stroke-width="3"/>')
    if parapet:
        o.append(f'<path d="M{n(-W/2+bat)} {n(top-9)}H{n(W/2-bat)}" stroke="{A}" stroke-width="3"/>')
    if lettersin:
        for xc, r, ch in zip(xs, rs, "CCE"):
            size = lscale * r / (f.cap / f.upm) * (1.0 if font == "man" else 1.05)
            o.append(letter(f, ch, size, xc, 0, lcol))
    if heads in ("shoulders", "dots"):
        for xc, r in zip(xs, rs):
            o.append(dot(xc, top - (2 * hb * 0.5 if heads == "shoulders" else 0) - hgap - hr, hr, A))
    if bubbles:
        xc = xs[-1] + rs[-1] * 0.4
        for i, rr in enumerate((7, 5.2, 3.8)[:bubbles]):
            o.append(dot(xc + i * 8, top - 16 - i * 20, rr, A))
    return "".join(o), W, H

def P2(I, A, P, **k): return pont2(I, A, P, **k)[0]

TESTS2 = [
 ("a", "Le Reflet, trois convives", "Arche + reflet = une bulle. Le tablier se soulève en épaules sous chaque tête.", dict()),
 ("b", "Bulles de tailles croissantes", "Les trois bulles grandissent, comme le perlage dans un verre.", dict(rs=(28, 34, 40))),
 ("c", "Sans personnages", "Le pont, le reflet, trois bulles qui montent.", dict(heads="none", bubbles=3, parapet=True)),
 ("d", "Reflet en lignes d’eau", "Une seule couleur : le reflet est dessiné par des lignes.", dict(reflect="lines")),
 ("e", "Reflet en filet d’or", "Le reflet se réduit à un demi-cercle doré.", dict(reflect="ring", lcol=NAVY)),
 ("f", "Lettres didones", "Mêmes formes, lettres à forts contrastes.", dict(font="bod", lscale=1.0)),
 ("g", "Lettres bleu nuit", "L’or est réservé aux personnages et à la ligne d’eau.", dict(lcol=NAVY)),
 ("h", "Retenue : bulles croissantes, convives, lettres or", "Synthèse : a + b, proportions réglées.", dict(rs=(30, 35, 40), p=18, a=28, span=15, hr=11, hb=8)),
]
