"""Recherche approfondie : 3 pistes en formes pleines, paramétriques (itérations réelles)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from lib import n
NAVY, GOLD, PAPER = "#15305B", "#C9A35A", "#FBF8F1"

def pol(r, deg, cx=0, cy=0):
    a = math.radians(deg); return cx + r * math.cos(a), cy + r * math.sin(a)
def dot(x, y, r, col): return f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(r)}" fill="{col}"/>'
def ann(cx, cy, r1, r2, a0, a1):
    lg = 1 if (a1 - a0) > 180 else 0
    p0, p1, p2, p3 = pol(r2, a0, cx, cy), pol(r2, a1, cx, cy), pol(r1, a1, cx, cy), pol(r1, a0, cx, cy)
    return (f"M{n(p0[0])} {n(p0[1])}A{n(r2)} {n(r2)} 0 {lg} 1 {n(p1[0])} {n(p1[1])}L{n(p2[0])} {n(p2[1])}"
            f"A{n(r1)} {n(r1)} 0 {lg} 0 {n(p3[0])} {n(p3[1])}Z")

# ---------------- PISTE 1 : LA RENCONTRE (coupe en réserve entre deux personnes) ----------------
def rencontre(I, A, P, W=100, top=-62, bot=104, a=58, b=74, s=6, f=38, fh=18, rc=40, h=20, hgap=9, bub=1, fill=False, sq=False):
    def half(m):   # m = -1 gauche, +1 droite
        x = lambda v: n(m * v)
        sw0, sw1 = (0, 1) if m < 0 else (1, 0)
        d = f"M{x(W-rc)} {n(top)}H{x(a)}"
        d += f"A{n(a-s)} {n(b)} 0 0 {sw0} {x(s)} {n(top+b)}"
        d += f"V{n(bot-fh)}A{n(f-s)} {n(fh)} 0 0 {sw1} {x(f)} {n(bot)}"
        if sq:
            d += f"H{x(W)}V{n(top+rc)}A{n(rc)} {n(rc)} 0 0 {sw1} {x(W-rc)} {n(top)}Z"
        else:
            d += f"H{x(W-rc)}A{n(rc)} {n(rc)} 0 0 {sw1} {x(W)} {n(bot-rc)}V{n(top+rc)}A{n(rc)} {n(rc)} 0 0 {sw1} {x(W-rc)} {n(top)}Z"
        return f'<path d="{d}" fill="{I}"/>'
    o = half(-1) + half(1)
    hx = (W + a) / 2
    o += dot(-hx, top - hgap - h, h, A) + dot(hx, top - hgap - h, h, A)
    if fill:
        o += f'<path d="M{n(-(a-s)*0.72-s)} {n(top+b*0.42)}H{n((a-s)*0.72+s)}" stroke="{A}" stroke-width="5" stroke-linecap="round"/>'
    if bub >= 1: o += dot(0, top + b * 0.5 if not fill else top + b * 0.16, 7.5, A)
    if bub >= 2: o += dot(9, top + 8, 5.5, A)
    if bub >= 3: o += dot(-5, top - 18, 4, A)
    return o
R_IT = [
    ("a", "Bol profond, pied large", dict(a=58, b=74)),
    ("b", "Coupe évasée, peu profonde", dict(a=70, b=50, f=44, h=13, bub=2)),
    ("c", "Flûte étroite", dict(a=34, b=112, f=30, h=26, bub=3, top=-58)),
    ("d", "Épaules carrées", dict(rc=14, a=56, b=70, bub=2)),
    ("e", "Base droite (socle)", dict(sq=True, a=58, b=74, bub=3)),
    ("f", "Niveau de champagne", dict(a=62, b=78, fill=True, bub=3)),
    ("g", "Têtes larges, rapprochées", dict(a=46, b=80, h=25, bub=2, f=34)),
    ("h", "Retenue : bol plein cintre, trois bulles", dict(a=56, b=78, s=6.5, f=40, fh=20, rc=42, h=20, bub=3)),
]
R_KEEP = R_IT[-1][2]

# ---------------- PISTE 2 : LA ROSACE (convives-coupes en rotation) ----------------
def rosace(I, A, P, N=6, D=62, r1=13, r2=27, h=10.5, e=3, span=180, inward=False, center=0, rot0=-90, ring=0):
    o = ""
    for k in range(N):
        th = rot0 + k * 360 / N
        cx, cy = pol(D, th)
        if not inward:
            o += f'<path d="{ann(cx, cy, r1, r2, th + 180 - span / 2, th + 180 + span / 2)}" fill="{I}"/>'
            hx, hy = pol(D + e, th)
        else:
            o += f'<path d="{ann(cx, cy, r1, r2, th - span / 2, th + span / 2)}" fill="{I}"/>'
            hx, hy = pol(D - e, th)
        o += dot(hx, hy, h, A)
    if center: o += dot(0, 0, center, A)
    if ring: o += f'<circle cx="0" cy="0" r="{n(ring)}" stroke="{I}" stroke-width="5" fill="none"/>'
    return o
Z_IT = [
    ("a", "6 convives, bras ouverts vers l’extérieur", dict()),
    ("b", "5 convives", dict(N=5, D=58, r1=15, r2=31, h=12)),
    ("c", "8 convives, module fin", dict(N=8, D=70, r1=10, r2=21, h=8)),
    ("d", "Bras ouverts vers le centre", dict(inward=True, D=66, e=2)),
    ("e", "Bras refermés (220°)", dict(span=222, r1=14, r2=26, h=10, e=0, D=64)),
    ("f", "Module épais, tête en réserve", dict(r1=11, r2=29, h=8.5, e=0)),
    ("g", "Avec cercle : capsule", dict(D=54, r1=11, r2=23, h=9, ring=98)),
    ("h", "Retenue : 6 convives, bulle centrale", dict(N=6, D=64, r1=14, r2=28.5, h=11, e=3, center=12)),
]
Z_KEEP = Z_IT[-1][2]

# ---------------- PISTE 3 : L’ARCADE (figure-fond : portes = personnes) ----------------
def arcade(I, A, P, W=100, top=-100, bot=100, shape="arch", k=3, d=34, hs=(92, 118, 92), hr=13, g=8, pitch=60, head="gold", rc=16, base=0):
    if shape == "arch":
        blk = f"M{-W} {bot}V{n(top+W)}A{W} {W} 0 0 1 {W} {n(top+W)}V{bot}Z"
    elif shape == "flat":
        blk = f"M{-W} {bot}V{n(top+rc)}A{rc} {rc} 0 0 1 {n(-W+rc)} {top}H{n(W-rc)}A{rc} {rc} 0 0 1 {W} {n(top+rc)}V{bot}Z"
    else:  # fronton
        blk = f"M{-W} {bot}V{n(top+46)}L0 {top}L{W} {n(top+46)}V{bot}Z"
    d_ = blk
    heads = ""
    x0 = -pitch * (k - 1) / 2
    for i in range(k):
        x = x0 + i * pitch
        yt = bot - hs[i]
        d_ += f"M{n(x-d/2)} {bot}V{n(yt+d/2)}A{n(d/2)} {n(d/2)} 0 0 1 {n(x+d/2)} {n(yt+d/2)}V{bot}Z"
        hy = yt - g - hr
        if head == "gold": heads += dot(x, hy, hr, A)
        else: d_ += f"M{n(x-hr)} {n(hy)}A{hr} {hr} 0 1 0 {n(x+hr)} {n(hy)}A{hr} {hr} 0 1 0 {n(x-hr)} {n(hy)}Z"
    o = f'<path d="{d_}" fill="{I}" fill-rule="evenodd"/>' + heads
    if base: o += f'<path d="M{-W} {bot+14}H{W}" stroke="{A}" stroke-width="5"/>'
    return o
A_IT = [
    ("a", "Grande arche, trois convives", dict()),
    ("b", "Bloc droit, angles adoucis", dict(shape="flat", top=-84, hs=(96, 122, 96))),
    ("c", "Fronton (porte monumentale)", dict(shape="fronton", top=-104, hs=(84, 112, 84), hr=12)),
    ("d", "Têtes en réserve (une couleur)", dict(head="cut")),
    ("e", "Cinq convives", dict(k=5, d=24, pitch=37, hs=(70, 92, 112, 92, 70), hr=9.5, g=6)),
    ("f", "Convives de même taille", dict(shape="flat", top=-70, hs=(104, 104, 104), hr=13)),
    ("g", "Portes larges, têtes proches", dict(d=40, pitch=62, hs=(84, 112, 84), hr=15, g=6)),
    ("h", "Retenue : arche, trois convives, ligne d’eau", dict(shape="arch", d=35, pitch=60, hs=(90, 118, 90), hr=13.5, g=8, base=1)),
]
A_KEEP = A_IT[-1][2]

PISTES = [("1", "La Rencontre", rencontre, R_IT, R_KEEP), ("2", "La Rosace", rosace, Z_IT, Z_KEEP), ("3", "L’Arcade", arcade, A_IT, A_KEEP)]

def tile(fn, kw, I=NAVY, A=GOLD, P=PAPER, size=260, vb=130, extra=""):
    return f'<svg viewBox="{-vb} {-vb-4} {2*vb} {2*vb}" width="{size}" height="{size}">{fn(I, A, P, **kw)}{extra}</svg>'
