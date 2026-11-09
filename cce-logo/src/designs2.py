"""Série 2 : le nom complet au premier plan."""
import math
from lib import *
from designs import CG500, CG600, J400, J500, PF400

PF500 = Font("PlayfairDisplay[wght].ttf", 500)
PF500I = Font("PlayfairDisplay-Italic[wght].ttf", 500)
J300 = Font("Jost[wght].ttf", 300)
J600 = Font("Jost[wght].ttf", 600)
ITA = Font("Italiana-Regular.ttf")


def fit(font, text, target, track_em=0.0):
    w1 = font.width(text, 1.0)
    return target / (w1 + track_em * (len(text) - 1))


def bubbles(b, items, gold, ink, solid_n=2, start=0):
    for i, (x, y, r) in enumerate(items):
        if i < solid_n:
            b.append(P(ink_disc(x, y, r, seed=i + start), gold))
        else:
            b.append(P(ink_ring(x, y, r, seed=i + start, w=max(r * .2, 2)), gold if i % 2 == 0 else ink))


# ---------------------------------------------------------------- 6. ÉTIQUETTE
def d6_etiquette(c):
    W, H = 800, 800
    cx, cy = 400, 370
    ink, gold, paper = c["ink"], c["gold"], c["paper"]
    rx, ry = 340, 300
    b = []
    b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" stroke="{ink}" stroke-width="6" fill="none"/>')
    b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx-14}" ry="{ry-14}" stroke="{ink}" stroke-width="1.5" fill="none"/>')
    for i in range(84):
        t = 2 * math.pi * i / 84
        b.append(P(ink_disc(cx + (rx - 28) * math.cos(t), cy + (ry - 28) * math.sin(t), 3.2, seed=i, wob=.1, N=8), gold))
    b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx-42}" ry="{ry-42}" stroke="{ink}" stroke-width="1.2" fill="none"/>')
    # bulles couronnant le nom
    bubbles(b, [(cx - 30, 188, 6), (cx - 6, 160, 10), (cx + 22, 184, 5.5), (cx + 40, 150, 14), (cx + 12, 118, 8)], gold, ink, solid_n=1)
    sz = fit(PF500, "CHÂLONS", 440, 0.06)
    d, w = PF500.path("CHÂLONS", sz, cx, 300, tracking=0.06 * sz, anchor="middle")
    b.append(P(d, ink))
    sz = fit(PF500I, "Champagnes", 470)
    d, w = PF500I.path("Champagnes", sz, cx, 404, anchor="middle")
    b.append(P(d, ink))
    d, bub, tw = J500.path_bubble_accents("ÉVENTS", 38, cx, 492, tracking=22, anchor="middle")
    b.append(P(d, ink))
    for (x, y, r) in bub:
        b.append(P(ink_disc(x, y, r, seed=4), gold))
    b.append(line(cx - 250, 478, cx - tw / 2 - 28, 478, gold, 1.8))
    b.append(line(cx + tw / 2 + 28, 478, cx + 250, 478, gold, 1.8))
    b.append(line(cx - 70, 540, cx + 70, 540, gold, 1.6))
    b.append(P(ink_ring(cx, 540, 7, seed=8, w=2), gold))
    # ruban
    b.append(P("M82 628L172 628L172 698L82 698L110 663Z", gold))
    b.append(P("M718 628L628 628L628 698L718 698L690 663Z", gold))
    b.append(P("M152 680L172 698L172 680Z", ink))
    b.append(P("M648 680L628 698L628 680Z", ink))
    b.append(f'<rect x="150" y="606" width="500" height="74" fill="{ink}" stroke="{paper}" stroke-width="3"/>')
    d, w = CG600.path("CCE", 58, cx, 658, tracking=22, anchor="middle")
    b.append(P(d, paper))
    return "".join(b), W, H


# ---------------------------------------------------------------- 7. AFFICHE
def d7_affiche(c):
    W, H = 960, 680
    ink, gold = c["ink"], c["gold"]
    x0 = 70
    b = []
    sz = fit(PF400, "Châlons", 690)
    d, w = PF400.path("Châlons", sz, x0, 210)
    b.append(P(d, ink))
    sz2 = fit(PF500I, "Champagnes", 720)
    d, w = PF500I.path("Champagnes", sz2, x0 + 6, 364)
    b.append(P(d, ink))
    sz3 = fit(J500, "ÉVENTS", 600, 0.55)
    d, bub, tw = J500.path_bubble_accents("ÉVENTS", sz3, x0 + 6, 486, tracking=0.55 * sz3)
    b.append(P(d, ink))
    for (x, y, r) in bub:
        b.append(P(ink_disc(x, y, r * 1.2, seed=5), gold))
    b.append(line(x0 + 6, 540, x0 + 720, 540, gold, 2.4))
    d, w = CG600.path("CCE", 54, x0 + 720, 604, tracking=16, anchor="end")
    b.append(P(d, ink))
    b.append(line(x0 + 6, 590, x0 + 720 - w - 28, 590, gold, 1.4))
    # colonne de bulles à droite
    sx = 880
    bubbles(b, [(sx - 6, 452, 5), (sx + 8, 410, 8), (sx - 2, 360, 13), (sx + 8, 296, 20), (sx - 4, 216, 29), (sx + 4, 108, 42)], gold, ink, solid_n=2, start=40)
    return "".join(b), W, H


# ---------------------------------------------------------------- 8. FLÈCHES
def d8_fleches(c):
    W, H = 700, 900
    ink, gold = c["ink"], c["gold"]
    cx, wl = 350, 470
    tw, th, sp = 96, 230, 150
    fh, gh = 140, 60
    xL0, xR0 = cx - 200, cx + 104
    xR1 = xR0 + tw
    b = []
    sw = 5
    for x0 in (xL0, xR0):
        xc = x0 + tw / 2
        b.append(f'<path d="M{x0} {wl}V{wl-th}H{x0+tw}V{wl}" stroke="{ink}" stroke-width="{sw}" fill="none" stroke-linejoin="round"/>')
        y0 = wl - th
        b.append(f'<path d="M{x0-6} {y0}Q{x0+tw*0.3} {y0-sp*0.42} {n(xc)} {y0-sp}Q{x0+tw*0.7} {y0-sp*0.42} {x0+tw+6} {y0}Z" fill="{ink}"/>')
        for k in (60, 120, 170):
            b.append(line(x0, wl - k, x0 + tw, wl - k, ink, 1.6))
        b.append(f'<path d="{arch_d(xc-11, 22, wl-th+62, 52)}" stroke="{ink}" stroke-width="2.4" fill="none"/>')
        b.append(P(ink_ring(xc, y0 - sp - 14, 6, seed=int(x0), w=2), gold))
    # façade
    b.append(f'<path d="M{xL0+tw} {wl}V{wl-fh}L{cx} {wl-fh-gh}L{xR0} {wl-fh}V{wl}" stroke="{ink}" stroke-width="{sw}" fill="none" stroke-linejoin="round"/>')
    b.append(circle_stroke(cx, wl - fh + 4, 38, ink, 3))
    b.append(circle_stroke(cx, wl - fh + 4, 27, gold, 1.6))
    b.append(f'<path d="{arch_d(cx-34, 68, wl, 84)}" stroke="{ink}" stroke-width="3" fill="none"/>')
    b.append(line(cx - 250, wl, cx + 250, wl, gold, 2.2))
    # reflet dans le Mau
    for i in range(9):
        y = wl + 14 + i * 17 + i * i * 0.8
        h = (y - wl) * 1.15
        sps = []
        if h < fh:
            sps.append((xL0, xR1))
        else:
            for x0 in (xL0, xR0):
                if h < th:
                    sps.append((x0, x0 + tw))
                elif h < th + sp:
                    fr = (1 - (h - th) / sp) ** 1.3
                    sps.append((x0 + tw / 2 - tw * fr / 2, x0 + tw / 2 + tw * fr / 2))
            if h < fh + gh:
                gw = 208 * (1 - (h - fh) / gh)
                sps.append((cx - gw / 2, cx + gw / 2))
        for (a, bb) in sps:
            if bb - a > 3:
                b.append(line(a + i % 2 * 3, y, bb + i % 2 * 3, y, gold if i % 2 else ink, max(4.4 - i * 0.38, 1.2), cap="round"))
    bubbles(b, [(cx + 2, 250, 5), (cx - 12, 214, 8), (cx + 10, 172, 12), (cx - 8, 124, 17), (cx + 6, 66, 24)], gold, ink, solid_n=1, start=60)
    sz = fit(PF400, "Châlons Champagnes", 560)
    d, w = PF400.path("Châlons Champagnes", sz, cx, 770, anchor="middle")
    b.append(P(d, ink))
    d, bub, tw2 = J500.path_bubble_accents("ÉVENTS", 30, cx, 836, tracking=24, anchor="middle")
    b.append(P(d, ink))
    for (x, y, r) in bub:
        b.append(P(ink_disc(x, y, r * 1.1, seed=2), gold))
    b.append(line(cx - 230, 824, cx - tw2 / 2 - 26, 824, gold, 1.6))
    b.append(line(cx + tw2 / 2 + 26, 824, cx + 230, 824, gold, 1.6))
    return "".join(b), W, H


# ---------------------------------------------------------------- 9. FIZZ
def path_replace(font, text, size, x, y, tracking, idx):
    r = font.run(text, size)
    cur, d, rep = x, [], None
    xh = (getattr(font.tt["OS/2"], "sxHeight", 0) or font.upm * 0.48) * size / font.upm
    for i, (name, adv, xo, yo) in enumerate(r):
        if i == idx:
            rep = (cur + adv / 2, y - xh / 2, xh / 2 * 1.06)
        else:
            d.append(font.glyph(name, size, cur + xo, y - yo))
        cur += adv + tracking
    return " ".join(d), rep, cur - tracking - x


def d9_fizz(c):
    W, H = 1000, 540
    ink, gold = c["ink"], c["gold"]
    b = []
    x0, sz = 66, 128
    d, rep, w = path_replace(J300, "châlons", sz, x0, 150, -2, 4)
    b.append(P(d, ink))
    b.append(P(ink_ring(rep[0], rep[1], rep[2], seed=3, w=rep[2] * 0.34, wob=0.02), gold))
    d, w2 = J600.path("champagnes", sz, x0, 284, tracking=-2)
    b.append(P(d, ink))
    d, w3 = J300.path("évents", sz, x0, 418, tracking=-2)
    b.append(P(d, ink))
    px, py = x0 + w3 + 90, 470
    b.append(f'<rect x="{x0}" y="{458}" width="170" height="50" rx="25" stroke="{ink}" stroke-width="3" fill="none"/>')
    d, w = J500.path("CCE", 27, x0 + 85, 492, tracking=12, anchor="middle")
    b.append(P(d, ink))
    sx = 880
    bubbles(b, [(sx - 20, 420, 6), (sx + 10, 378, 10), (sx - 8, 322, 16), (sx + 16, 250, 25), (sx - 14, 160, 36), (sx + 10, 62, 46)], gold, ink, solid_n=2, start=80)
    return "".join(b), W, H


# ---------------------------------------------------------------- 10. ÉCLAT
def d10_eclat(c):
    W, H = 800, 800
    ink, gold = c["ink"], c["gold"]
    cx, cy = 400, 360
    b = []
    a, depth = 130, 130
    pts_out, pts_in = [], []
    for k in range(19):
        t = math.pi * k / 18
        pts_out.append((cx - a * math.cos(t), cy + depth * math.sin(t)))
        pts_in.append((cx - (a - 11) * math.cos(t), cy + (depth - 22) * math.sin(t)))
    seg_o = smooth_open(pts_out)
    seg_i = smooth_open(pts_in[::-1])
    dd = seg_o + "L" + n(pts_in[-1][0]) + " " + n(pts_in[-1][1]) + seg_i[seg_i.index("C"):] + "Z"
    b.append(P(dd, ink))
    b.append(line(cx - a * 0.8, cy + 22, cx + a * 0.8, cy + 22, gold, 2.4, cap="round"))
    # tige et pied
    bb = cy + depth
    b.append(P(f"M{cx-4} {bb+8}L{cx+4} {bb+8}L{cx+3} {bb+70}L{cx-3} {bb+70}Z", ink))
    b.append(f'<path d="M{cx-48} {bb+72}Q{cx} {bb+56} {cx+48} {bb+72}" stroke="{ink}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    d, w = CG600.path("CCE", 40, cx, cy + 78, tracking=14, anchor="middle")
    b.append(P(d, ink))
    # éclat : rayons terminés par des bulles
    n_r = 13
    for i in range(n_r):
        ang = math.radians(8 + i * 164 / (n_r - 1))
        long_ = i % 2 == 0
        r0, L = 160, (120 if long_ else 62)
        x1, y1 = cx + r0 * math.cos(ang), cy - 14 - r0 * math.sin(ang)
        x2, y2 = cx + (r0 + L) * math.cos(ang), cy - 14 - (r0 + L) * math.sin(ang)
        b.append(line(x1, y1, x2, y2, ink if long_ else gold, 3.2 if long_ else 2.4, cap="round"))
        rb = 10 if long_ else 5
        bx, by = cx + (r0 + L + rb + 8) * math.cos(ang), cy - 14 - (r0 + L + rb + 8) * math.sin(ang)
        if long_:
            b.append(P(ink_ring(bx, by, rb, seed=i, w=2.6), gold))
        else:
            b.append(P(ink_disc(bx, by, rb, seed=i), gold))
    sz = fit(ITA, "CHALONS CHAMPAGNES", 640, 0.2)
    d, bub, tw = ITA.path_bubble_accents("CHÂLONS CHAMPAGNES", sz, cx, 678, tracking=0.2 * sz, anchor="middle")
    b.append(P(d, ink))
    for (x, y, r) in bub:
        b.append(P(ink_disc(x, y, r * 1.1, seed=int(x)), gold))
    d, bub, tw2 = ITA.path_bubble_accents("ÉVENTS", 36, cx, 742, tracking=30, anchor="middle")
    b.append(P(d, ink))
    for (x, y, r) in bub:
        b.append(P(ink_disc(x, y, r * 1.1, seed=3), gold))
    b.append(line(cx - 290, 728, cx - tw2 / 2 - 28, 728, gold, 1.6))
    b.append(line(cx + tw2 / 2 + 28, 728, cx + 290, 728, gold, 1.6))
    return "".join(b), W, H


PISTES2 = [
    ("06", "etiquette", "L’Étiquette", d6_etiquette),
    ("07", "affiche", "L’Affiche", d7_affiche),
    ("08", "fleches", "Les Flèches", d8_fleches),
    ("09", "fizz", "Le Fizz", d9_fizz),
    ("10", "eclat", "L’Éclat", d10_eclat),
]
