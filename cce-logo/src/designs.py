"""Les 5 pistes graphiques CCE – Châlons Champagnes Évents."""
import math
from lib import *

CG300 = Font("CormorantGaramond[wght].ttf", 300)
CG500 = Font("CormorantGaramond[wght].ttf", 500)
CG600 = Font("CormorantGaramond[wght].ttf", 600)
PF400 = Font("PlayfairDisplay[wght].ttf", 400)
J400 = Font("Jost[wght].ttf", 400)
J500 = Font("Jost[wght].ttf", 500)
PIN = Font("PinyonScript-Regular.ttf")


# ---------------------------------------------------------------- 1. PLAQUE
def d1_plaque(c, simple=False):
    W = H = 640
    cx = cy = 320
    ink, gold = c["ink"], c["gold"]
    b = []
    b.append(circle_stroke(cx, cy, 306, ink, 5))
    b.append(circle_stroke(cx, cy, 294, ink, 1.4))
    for i in range(72):                                  # perlage du bord (comme une plaque de muselet)
        a = 2 * math.pi * i / 72
        b.append(P(ink_disc(cx + 276 * math.cos(a), cy + 276 * math.sin(a), 3.6, seed=i, wob=0.1, N=8), gold))
    b.append(circle_stroke(cx, cy, 256, ink, 1.4))
    if not simple:
        b.append(circle_stroke(cx, cy, 200, ink, 1.4))
        b.append(P(J500.arc("CHÂLONS CHAMPAGNES ÉVENTS", 29, cx, cy, 213, 0, tracking=7.2), ink))
        b.append(P(J500.arc("CHÂLONS-EN-CHAMPAGNE", 22, cx, cy, 234, 180, tracking=9, bottom=True), ink))
        for s in (-1, 1):
            b.append(P(ink_ring(cx + s * 228, cy, 8, seed=3 + s, w=2.4), gold))
        base_y = cy + 52
        size = 150
    else:
        b.append(circle_stroke(cx, cy, 238, ink, 1.4))
        base_y = cy + 60
        size = 168
    d, w = CG600.path("CCE", size, cx, base_y, tracking=8, anchor="middle")
    b.append(P(d, ink))
    # bulles qui s'échappent du E
    if not simple:
        bub = [(cx + 120, cy - 90, 6, 1), (cx + 140, cy - 112, 5.5, 2), (cx + 106, cy - 122, 11, 3), (cx + 128, cy - 130, 7, 4), (cx + 96, cy - 146, 14, 5)]
    else:
        bub = [(cx + 130, cy - 94, 7, 1), (cx + 152, cy - 120, 6, 2), (cx + 116, cy - 138, 13, 3), (cx + 146, cy - 152, 8, 4), (cx + 112, cy - 176, 17, 5)]
    for i, (x, y, r, s) in enumerate(bub):
        b.append(P(ink_ring(x, y, r, seed=s, w=max(r * 0.22, 1.6)) if i % 2 else ink_disc(x, y, r * 0.75, seed=s), gold if i % 2 == 0 else ink))
    if not simple:
        b.append(line(cx - 70, base_y + 34, cx + 70, base_y + 34, gold, 1.6))
        b.append(P(ink_disc(cx, base_y + 34, 4.2, seed=9), gold))
        d, w = J500.path("ÉVENTS", 24, cx, base_y + 78, tracking=13, anchor="middle")
        b.append(P(d, ink))
    return "".join(b), W, H


# ---------------------------------------------------------------- 2. PERLAGE
def d2_perlage(c):
    W, H = 1000, 560
    ink, gold = c["ink"], c["gold"]
    b = []
    x0, base = 70, 360
    d, w = CG300.path("CCE", 360, x0, base, tracking=34)
    b.append(P(d, ink))
    # colonne de bulles : petites et pleines en bas, grandes et creuses en haut
    sx = x0 + w + 62
    ys = [base - 6, base - 46, base - 96, base - 154, base - 220, base - 292]
    rs = [5, 8, 12, 18, 27, 40]
    xs = [sx, sx + 14, sx - 6, sx + 18, sx - 4, sx + 12]
    for i, (x, y, r) in enumerate(zip(xs, ys, rs)):
        if i < 2:
            b.append(P(ink_disc(x, y, r, seed=i), gold))
        else:
            b.append(P(ink_ring(x, y, r, seed=i, w=max(r * 0.2, 2)), gold if i % 2 == 0 else ink))
    # petites bulles qui s'échappent dans la lettre C
    for (x, y, r, s) in [(x0 + 118, base - 88, 6, 20), (x0 + 142, base - 130, 4, 21), (x0 + 106, base - 160, 8, 22)]:
        b.append(P(ink_disc(x, y, r, seed=s), gold))
    ex = x0 + w
    b.append(line(x0 + 4, base + 52, ex - 4, base + 52, gold, 2.4))
    d, bub, tw = J400.path_bubble_accents("CHÂLONS CHAMPAGNES ÉVENTS", 35, x0 + 4, base + 118, tracking=10.8)
    b.append(P(d, ink))
    for (x, y, r) in bub:
        b.append(P(ink_disc(x, y, r * 1.15, seed=int(x)), gold))
    return "".join(b), W, H


# ---------------------------------------------------------------- 3. REFLET
def d3_reflet(c):
    W, H = 640, 980
    ink, gold = c["ink"], c["gold"]
    cx = 320
    wl = 500                       # ligne d'eau (canal)
    b = []
    a, depth = 112, 96             # demi-largeur et profondeur de la coupe
    stem, foot = 78, 76
    bowl_bot = wl - stem
    rim = bowl_bot - depth
    pts_out, pts_in = [], []
    for k in range(0, 19):
        t = math.pi * k / 18
        pts_out.append((cx - a * math.cos(t), rim + depth * math.sin(t)))
        pts_in.append((cx - (a - 9) * math.cos(t), rim + (depth - 19) * math.sin(t)))
    seg_out = smooth_open(pts_out)
    seg_in = smooth_open(pts_in[::-1])
    dd = seg_out + "L" + n(pts_in[-1][0]) + " " + n(pts_in[-1][1]) + seg_in[seg_in.index("C"):] + "Z"
    b.append(P(dd, ink))
    # niveau du champagne
    b.append(line(cx - a * 0.78, rim + 17, cx + a * 0.78, rim + 17, gold, 2.4, cap="round"))
    # tige et pied
    b.append(P(f"M{n(cx-3.6)} {n(bowl_bot+10)}L{n(cx+3.6)} {n(bowl_bot+10)}L{n(cx+2.6)} {n(wl-5)}L{n(cx-2.6)} {n(wl-5)}Z", ink))
    b.append(f'<path d="M{n(cx-foot/2)} {n(wl-3)}Q{n(cx)} {n(wl-16)} {n(cx+foot/2)} {n(wl-3)}" stroke="{ink}" stroke-width="5.5" fill="none" stroke-linecap="round"/>')
    # ligne d'eau
    b.append(line(cx - 230, wl, cx + 230, wl, gold, 2.2))

    # reflet : traits d'eau qui épousent la silhouette (de plus en plus fins)
    def half_w(h):
        if h <= 6: return foot / 2
        if h < stem: return 3
        k = (h - stem) / depth
        return (a - 5) * math.sqrt(max(0.0, 1 - (1 - k) ** 2))
    hs = [4, 30, stem + 4, stem + 18, stem + 34, stem + 52, stem + 72, stem + 92]
    for i, hh in enumerate(hs):
        y = wl + 20 + hh * 0.92 + i * 2.2
        hw = max(half_w(hh), 3)
        b.append(line(cx - hw, y, cx + hw, y, gold if i % 2 else ink, max(4.2 - i * 0.42, 1.2), cap="round"))

    # bulles : petites et pleines au ras du champagne, grandes et creuses en haut
    pos = [(cx + 3, rim - 20, 5.5, 0), (cx - 16, rim - 52, 9, 1), (cx + 14, rim - 94, 14, 2),
           (cx - 12, rim - 148, 21, 3), (cx + 18, rim - 212, 30, 4), (cx - 8, rim - 290, 42, 5)]
    for i, (x, y, r, s) in enumerate(pos):
        if i < 2:
            b.append(P(ink_disc(x, y, r, seed=s), gold))
        else:
            b.append(P(ink_ring(x, y, r, seed=s, w=max(r * 0.2, 2.2)), gold if i % 2 == 0 else ink))
    d_, w = CG500.path("CCE", 104, cx, 800, tracking=34, anchor="middle")
    b.append(P(d_, ink))
    d_, bub, tw = J400.path_bubble_accents("CHÂLONS CHAMPAGNES ÉVENTS", 21, cx, 868, tracking=8, anchor="middle")
    b.append(P(d_, ink))
    for (x, y, r) in bub:
        b.append(P(ink_disc(x, y, r, seed=int(x)), gold))
    return "".join(b), W, H


# ---------------------------------------------------------------- 4. SIGNATURE
def d4_signature(c, monogram=False):
    ink, gold = c["ink"], c["gold"]
    b = []
    if monogram:
        W = H = 520
        cx = cy = 260
        b.append(P(ink_ring(cx, cy, 218, seed=11, w=12, wob=0.012, N=22), ink))
        b.append(P(ink_ring(cx, cy, 196, seed=12, w=2.4, wob=0.012, N=22), gold))
        d, w = PIN.path("CCE", 150, cx, cy + 34, tracking=26, anchor="middle")
        b.append(P(d, ink))
        for (x, y, r, s) in [(cx + 92, cy - 70, 7, 1), (cx + 118, cy - 108, 11, 2), (cx + 84, cy - 130, 5, 3)]:
            b.append(P(ink_ring(x, y, r, seed=s, w=max(r * .22, 1.6)) if s != 3 else ink_disc(x, y, r, seed=s), gold))
        d, w = J500.path("ÉVENTS", 22, cx, cy + 118, tracking=14, anchor="middle")
        b.append(P(d, ink))
        return "".join(b), W, H
    W, H = 1180, 560
    sz = 170 * 1000 / PIN.width("Châlons Champagnes", 170)
    d, w = PIN.path("Châlons Champagnes", sz, 90, 270, tracking=-1)
    b.append(P(d, ink))
    # liane / fioriture peinte sous le nom
    pts = bezier_pts((70, 345), (330, 300), (640, 392), (1010, 318), k=36)
    b.append(P(brush_stroke(pts, 10.5, taper=0.55), gold))
    for (x, y, r, s) in [(1052, 306, 6, 1), (1086, 282, 9, 2), (1110, 244, 13, 3), (1128, 192, 19, 4)]:
        b.append(P(ink_ring(x, y, r, seed=s, w=max(r * .22, 1.8)) if s > 1 else ink_disc(x, y, r, seed=s), gold if s % 2 else ink))
    d, bub, tw = J500.path_bubble_accents("ÉVENTS", 46, W / 2 - 40, 462, tracking=34, anchor="middle")
    b.append(P(d, ink))
    for (x, y, r) in bub:
        b.append(P(ink_disc(x, y, r * 1.2, seed=3), gold))
    b.append(line(90, 446, W / 2 - 40 - tw / 2 - 40, 446, gold, 1.6))
    b.append(line(W / 2 - 40 + tw / 2 + 40, 446, 1010, 446, gold, 1.6))
    return "".join(b), W, H


# ---------------------------------------------------------------- 5. ARCADE
def d5_arcade(c, tagline=True):
    W, H = 760, 640
    ink, gold = c["ink"], c["gold"]
    b = []
    base = 500
    spec = [  # x0, largeur, hauteur, lettre
        (40, 190, 330, "C"),
        (254, 252, 430, "C"),
        (530, 190, 330, "E"),
    ]
    for (x0, w, h, ch) in spec:
        b.append(f'<path d="{arch_d(x0, w, base, h)}" stroke="{ink}" stroke-width="7" fill="none" stroke-linejoin="round"/>')
        b.append(f'<path d="{arch_d(x0 + 15, w - 30, base, h - 15)}" stroke="{ink}" stroke-width="1.6" fill="none"/>')
        d, lw = CG600.path(ch, 168, x0 + w / 2, base - 38, anchor="middle")
        b.append(P(d, ink))
    b.append(line(18, base, W - 18, base, ink, 7))
    b.append(line(18, base + 14, W - 18, base + 14, gold, 1.6))
    # bulles qui montent sous l'arche centrale (la plus haute)
    cxm = 254 + 126
    for i, (dx, dy, r) in enumerate([(4, 190, 6), (-12, 232, 9), (10, 282, 13), (-8, 336, 19), (12, 394, 27)]):
        y = base - dy - 60
        b.append(P(ink_disc(cxm + dx, y, r, seed=i) if i == 0 else ink_ring(cxm + dx, y, r, seed=i, w=max(r * .22, 2)), gold))
    for (x, y, r, s) in [(40 + 95 + 8, base - 248, 9, 31), (40 + 95 - 10, base - 290, 14, 32), (530 + 95 - 6, base - 252, 8, 33), (530 + 95 + 10, base - 296, 13, 34)]:
        b.append(P(ink_ring(x, y, r, seed=s, w=max(r * .22, 1.8)), gold))
    if tagline:
        d, bub, tw = J500.path_bubble_accents("CHÂLONS CHAMPAGNES ÉVENTS", 27, W / 2, base + 82, tracking=11, anchor="middle")
        b.append(P(d, ink))
        for (x, y, r) in bub:
            b.append(P(ink_disc(x, y, r * 1.15, seed=int(x)), gold))
    return "".join(b), W, H


PISTES = [
    ("01", "plaque", "La Plaque", d1_plaque),
    ("02", "perlage", "Le Perlage", d2_perlage),
    ("03", "reflet", "Le Reflet", d3_reflet),
    ("04", "signature", "La Signature", d4_signature),
    ("05", "arcade", "L’Arcade", d5_arcade),
]
