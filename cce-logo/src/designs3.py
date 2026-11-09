"""Série 3 : pistes inspirées du tableau Pinterest de l'utilisateur (principes, pas de copie)."""
import math
from lib import *
from designs import CG500, CG600, J400, J500, PF400
from designs2 import PF500, PF500I, J300, J600, ITA, fit, bubbles


def glass_local(ink, gold, a=88, depth=72, stem=110, foot=50):
    pts_o, pts_i = [], []
    for k in range(19):
        t = math.pi * k / 18
        pts_o.append((-a * math.cos(t), depth * math.sin(t)))
        pts_i.append((-(a - 9) * math.cos(t), (depth - 18) * math.sin(t)))
    so = smooth_open(pts_o)
    si = smooth_open(pts_i[::-1])
    d = so + "L" + n(pts_i[-1][0]) + " " + n(pts_i[-1][1]) + si[si.index("C"):] + "Z"
    out = [P(d, ink)]
    out.append(line(-a * 0.76, 17, a * 0.76, 17, gold, 2.4, cap="round"))
    out.append(P(f"M-3.6 {depth-6}L3.6 {depth-6}L2.6 {depth+stem}L-2.6 {depth+stem}Z", ink))
    out.append(f'<path d="M{-foot} {depth+stem+2}Q0 {depth+stem-12} {foot} {depth+stem+2}" stroke="{ink}" stroke-width="5.5" fill="none" stroke-linecap="round"/>')
    return "".join(out)


# ------------------------------------------------------------ 11. TRAIT CONTINU
def d11_trait(c):
    W, H = 900, 420
    ink, gold = c["ink"], c["gold"]
    cx, rim, a, depth = 170, 170, 104, 88
    b = []
    b.append(f'<path d="M{cx-a} {rim}A{a} {depth} 0 0 0 {cx+a} {rim}" stroke="{ink}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    b.append(line(cx - a * 0.76, rim + 24, cx + a * 0.76, rim + 24, gold, 2.4, cap="round"))
    base = 360
    b.append(f'<path d="M{cx} {rim+depth}V{base-40}Q{cx} {base} {cx+40} {base}H820" stroke="{ink}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(P(ink_ring(846, base, 12, seed=7, w=3.4), gold))
    bubbles(b, [(cx + 8, 138, 5), (cx - 12, 104, 8), (cx + 12, 66, 12), (cx - 8, 30, 16)], gold, ink, solid_n=1, start=110)
    sz = fit(PF400, "Châlons Champagnes", 520)
    d, w = PF400.path("Châlons Champagnes", sz, 330, 236)
    b.append(P(d, ink))
    d, bub, tw = J500.path_bubble_accents("ÉVENTS", 30, 334, 300, tracking=22)
    b.append(P(d, ink))
    for (x, y, r) in bub:
        b.append(P(ink_disc(x, y, r * 1.1, seed=3), gold))
    d, w = CG600.path("CCE", 32, 820, 338, tracking=12, anchor="end")
    b.append(P(d, ink))
    return "".join(b), W, H


# ------------------------------------------------------------ 12. ARCHE PLEINE
def d12_arche(c):
    W, H = 700, 760
    ink, gold, paper = c["ink"], c["gold"], c["paper"]
    cx, base, w, h = 350, 470, 320, 430
    x0, r = cx - w / 2, w / 2
    b = []
    b.append(f'<path d="{arch_d(x0-18, w+36, base, h+18)}" stroke="{gold}" stroke-width="2.6" fill="none"/>')
    b.append(f'<path d="M{x0} {base}V{base-h+r}A{r} {r} 0 0 1 {x0+w} {base-h+r}V{base}Z" fill="{ink}"/>')
    b.append(line(x0 - 44, base, x0 + w + 44, base, ink, 6))
    b.append(line(x0 - 44, base + 14, x0 + w + 44, base + 14, gold, 1.8))
    rim = 350
    b.append(P(f"M{cx-72} {rim}A72 58 0 0 0 {cx+72} {rim}Z", paper))
    b.append(line(cx - 56, rim + 14, cx + 56, rim + 14, gold, 2.2, cap="round"))
    b.append(P(f"M{cx-3.8} {rim+52}L{cx+3.8} {rim+52}L{cx+2.8} {base-22}L{cx-2.8} {base-22}Z", paper))
    b.append(f'<path d="M{cx-46} {base-20}Q{cx} {base-36} {cx+46} {base-20}" stroke="{paper}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    for i, (dx, y, rr) in enumerate([(6, 322, 5), (-14, 290, 8), (10, 252, 12), (-8, 210, 17)]):
        b.append(P(ink_disc(cx + dx, y, rr, seed=i) if i == 0 else ink_ring(cx + dx, y, rr, seed=i, w=max(rr * .22, 2)), paper))
    d, w2 = CG600.path("CCE", 46, cx, 150, tracking=16, anchor="middle")
    b.append(P(d, paper))
    sz = fit(PF500, "CHÂLONS CHAMPAGNES", 560, 0.08)
    d, w2 = PF500.path("CHÂLONS CHAMPAGNES", sz, cx, 584, tracking=0.08 * sz, anchor="middle")
    b.append(P(d, ink))
    d, bub, tw = J500.path_bubble_accents("ÉVENTS", 34, cx, 654, tracking=30, anchor="middle")
    b.append(P(d, ink))
    for (x, y, rr) in bub:
        b.append(P(ink_disc(x, y, rr * 1.1, seed=5), gold))
    b.append(line(cx - 250, 641, cx - tw / 2 - 26, 641, gold, 1.6))
    b.append(line(cx + tw / 2 + 26, 641, cx + 250, 641, gold, 1.6))
    return "".join(b), W, H


# ------------------------------------------------------------ 13. SANTÉ
def d13_sante(c):
    W, H = 800, 640
    ink, gold = c["ink"], c["gold"]
    cx, yc, a, th = 400, 250, 88, 20
    cs, sn = math.cos(math.radians(th)), math.sin(math.radians(th))
    g = glass_local(ink, gold, a=a)
    b = []
    b.append(f'<g transform="translate({n(cx-a*cs)} {n(yc-a*sn)}) rotate({th})">{g}</g>')
    b.append(f'<g transform="translate({n(cx+a*cs)} {n(yc-a*sn)}) rotate({-th})">{g}</g>')
    for i in range(7):
        ang = math.radians(28 + i * 124 / 6)
        long_ = i % 2 == 1
        r0, L = 30, (52 if long_ else 26)
        x1, y1 = cx + r0 * math.cos(ang), yc - r0 * math.sin(ang)
        x2, y2 = cx + (r0 + L) * math.cos(ang), yc - (r0 + L) * math.sin(ang)
        b.append(line(x1, y1, x2, y2, ink if long_ else gold, 3 if long_ else 2.2, cap="round"))
        rb = 8 if long_ else 4.5
        bx, by = cx + (r0 + L + rb + 6) * math.cos(ang), yc - (r0 + L + rb + 6) * math.sin(ang)
        b.append(P(ink_ring(bx, by, rb, seed=i, w=2.2) if long_ else ink_disc(bx, by, rb, seed=i), gold))
    bubbles(b, [(cx - 14, 104, 7), (cx + 10, 72, 11), (cx - 6, 34, 15)], gold, ink, solid_n=0, start=130)
    d, w = CG600.path("CCE", 44, cx, 388, tracking=18, anchor="middle")
    b.append(P(d, ink))
    sz = fit(PF500, "Châlons Champagnes", 560)
    d, w = PF500.path("Châlons Champagnes", sz, cx, 500, anchor="middle")
    b.append(P(d, ink))
    d, bub, tw = J500.path_bubble_accents("ÉVENTS", 32, cx, 566, tracking=28, anchor="middle")
    b.append(P(d, ink))
    for (x, y, rr) in bub:
        b.append(P(ink_disc(x, y, rr * 1.1, seed=2), gold))
    b.append(line(cx - 250, 554, cx - tw / 2 - 24, 554, gold, 1.6))
    b.append(line(cx + tw / 2 + 24, 554, cx + 250, 554, gold, 1.6))
    return "".join(b), W, H


# ------------------------------------------------------------ 14. CARTOUCHE À BULLES
def superellipse(cx, cy, A, B, nn, N=900):
    pts = []
    for i in range(N):
        t = 2 * math.pi * i / N
        ct, st = math.cos(t), math.sin(t)
        pts.append((cx + A * math.copysign(abs(ct) ** (2 / nn), ct), cy + B * math.copysign(abs(st) ** (2 / nn), st)))
    return pts


def resample(pts, m):
    L = [0.0]
    for i in range(1, len(pts) + 1):
        a, b_ = pts[i - 1], pts[i % len(pts)]
        L.append(L[-1] + math.hypot(b_[0] - a[0], b_[1] - a[1]))
    tot = L[-1]
    out, j = [], 0
    for k in range(m):
        s = tot * k / m
        while L[j + 1] < s:
            j += 1
        a, b_ = pts[j % len(pts)], pts[(j + 1) % len(pts)]
        f = (s - L[j]) / (L[j + 1] - L[j] or 1)
        out.append((a[0] + (b_[0] - a[0]) * f, a[1] + (b_[1] - a[1]) * f))
    return out


def d14_cartouche(c):
    W, H = 800, 800
    ink, gold = c["ink"], c["gold"]
    cx, cy = 400, 400
    b = []
    outer = superellipse(cx, cy, 345, 315, 2.8)
    for i, (x, y) in enumerate(resample(outer, 52)):
        if i % 2 == 0:
            b.append(P(ink_ring(x, y, 13, seed=i, w=3.4), ink))
        else:
            b.append(P(ink_disc(x, y, 5.5, seed=i), gold))
    inner = superellipse(cx, cy, 309, 279, 2.8)
    b.append('<path d="M' + "L".join(f"{n(x)} {n(y)}" for x, y in inner) + f'Z" stroke="{ink}" stroke-width="2.2" fill="none"/>')
    inner2 = superellipse(cx, cy, 296, 266, 2.8)
    b.append('<path d="M' + "L".join(f"{n(x)} {n(y)}" for x, y in inner2) + f'Z" stroke="{gold}" stroke-width="1.2" fill="none"/>')
    d, w = CG600.path("CCE", 56, cx, 268, tracking=20, anchor="middle")
    b.append(P(d, ink))
    b.append(P(ink_ring(cx - 118, 246, 7, seed=1, w=2), gold))
    b.append(P(ink_ring(cx + 118, 246, 7, seed=2, w=2), gold))
    b.append(line(cx - 150, 296, cx + 150, 296, gold, 1.6))
    sz = fit(PF500, "CHÂLONS", 400, 0.06)
    d, w = PF500.path("CHÂLONS", sz, cx, 392, tracking=0.06 * sz, anchor="middle")
    b.append(P(d, ink))
    sz = fit(PF500I, "Champagnes", 440)
    d, w = PF500I.path("Champagnes", sz, cx, 478, anchor="middle")
    b.append(P(d, ink))
    d, bub, tw = J500.path_bubble_accents("ÉVENTS", 32, cx, 556, tracking=24, anchor="middle")
    b.append(P(d, ink))
    for (x, y, rr) in bub:
        b.append(P(ink_disc(x, y, rr * 1.15, seed=4), gold))
    b.append(line(cx - 190, 544, cx - tw / 2 - 24, 544, gold, 1.6))
    b.append(line(cx + tw / 2 + 24, 544, cx + 190, 544, gold, 1.6))
    bubbles(b, [(cx - 22, 618, 6), (cx + 6, 600, 9), (cx + 36, 622, 5)], gold, ink, solid_n=1, start=150)
    return "".join(b), W, H


# ------------------------------------------------------------ 15. ROSACE
def d15_rosace(c):
    W, H = 1100, 460
    ink, gold = c["ink"], c["gold"]
    cx, cy = 236, 230
    b = []
    b.append(circle_stroke(cx, cy, 196, ink, 4.5))
    b.append(circle_stroke(cx, cy, 184, gold, 1.6))
    for i in range(16):
        t = 2 * math.pi * i / 16 - math.pi / 2
        x, y = cx + 150 * math.cos(t), cy + 150 * math.sin(t)
        b.append(P(ink_ring(x, y, 15, seed=i, w=4), ink) if i % 2 == 0 else P(ink_disc(x, y, 8, seed=i), gold))
    for i in range(8):
        t = 2 * math.pi * i / 8 - math.pi / 2
        x, y = cx + 84 * math.cos(t), cy + 84 * math.sin(t)
        b.append(P(ink_ring(x, y, 25, seed=40 + i, w=5.5), gold))
        t2 = t + math.pi / 8
        b.append(P(ink_disc(cx + 118 * math.cos(t2), cy + 118 * math.sin(t2), 4.5, seed=60 + i), ink))
    b.append(P(ink_disc(cx, cy, 24, seed=99), gold))
    sz = fit(J500, "CHÂLONS CHAMPAGNES", 560, 0.08)
    d, w = J500.path("CHÂLONS CHAMPAGNES", sz, 500, 214, tracking=0.08 * sz)
    b.append(P(d, ink))
    d, bub, tw = J300.path_bubble_accents("ÉVENTS", 66, 500, 300, tracking=40)
    b.append(P(d, ink))
    for (x, y, rr) in bub:
        b.append(P(ink_disc(x, y, rr * 1.2, seed=6), gold))
    b.append(line(500, 342, 1040, 342, gold, 2))
    d, w = CG600.path("CCE", 34, 500, 394, tracking=14)
    b.append(P(d, ink))
    return "".join(b), W, H


# ------------------------------------------------------------ 16. GIGOGNES
def arc_ring(cx, cy, R, wmax, a0=40, a1=320, N=24):
    outer, inner = [], []
    for i in range(N + 1):
        deg = a0 + (a1 - a0) * i / N
        u = (deg - 180) / ((a1 - a0) / 2)
        wv = wmax * (0.16 + 0.84 * (1 - u * u))
        t = math.radians(deg)
        outer.append((cx + R * math.cos(t), cy + R * math.sin(t)))
        inner.append((cx + (R - wv) * math.cos(t), cy + (R - wv) * math.sin(t)))
    so = smooth_open(outer)
    si = smooth_open(inner[::-1])
    return so + "L" + n(inner[-1][0]) + " " + n(inner[-1][1]) + si[si.index("C"):] + "Z"


def d16_gigognes(c):
    W, H = 1000, 520
    ink, gold = c["ink"], c["gold"]
    cx, cy = 250, 260
    b = []
    b.append(P(arc_ring(cx, cy, 196, 30, 42, 318), ink))
    b.append(P(arc_ring(cx, cy, 132, 22, 44, 316), ink))
    b.append(P(arc_ring(cx, cy, 82, 2.2, 0, 360, N=36), gold))
    d, w = CG600.path("E", 118, cx - 4, cy + 38, anchor="middle")
    b.append(P(d, ink))
    bubbles(b, [(346, 238, 5), (382, 208, 8), (424, 170, 12), (470, 124, 18), (522, 66, 26)], gold, ink, solid_n=1, start=170)
    sz = fit(PF400, "Châlons", 330)
    d, w = PF400.path("Châlons", sz, 600, 200)
    b.append(P(d, ink))
    sz = fit(PF500I, "Champagnes", 380)
    d, w = PF500I.path("Champagnes", sz, 600, 292)
    b.append(P(d, ink))
    d, bub, tw = J500.path_bubble_accents("ÉVENTS", 34, 604, 366, tracking=26)
    b.append(P(d, ink))
    for (x, y, rr) in bub:
        b.append(P(ink_disc(x, y, rr * 1.15, seed=8), gold))
    b.append(line(604, 330, 604 + 340, 330, gold, 1.8))
    return "".join(b), W, H


PISTES3 = [
    ("11", "trait", "Le Trait", d11_trait),
    ("12", "arche-pleine", "L’Arche pleine", d12_arche),
    ("13", "sante", "Santé", d13_sante),
    ("14", "cartouche", "Le Cartouche", d14_cartouche),
    ("15", "rosace", "La Rosace", d15_rosace),
    ("16", "gigognes", "Les Gigognes", d16_gigognes),
]
