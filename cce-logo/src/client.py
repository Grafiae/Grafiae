"""3 propositions client – Châlons Champagne Events (tourisme d'affaires)."""
import os, sys, math, html as _h
sys.path.insert(0, os.path.dirname(__file__))
from lib import Font, n

MAN5 = Font("Manrope[wght].ttf", 500)
MAN6 = Font("Manrope[wght].ttf", 600)
MAN7 = Font("Manrope[wght].ttf", 700)
MAR = Font("Marcellus-Regular.ttf")
BOD = Font("BodoniModa.ttf", 500)
TAG = "TOURISME D’AFFAIRES"

PAL = {
    "A": dict(ink="#15305B", acc="#C9A35A", acc_text="#96762F", paper="#FBF8F1", nom="Bleu nuit & or (couleurs actuelles)"),
    "B": dict(ink="#16382E", acc="#B9975B", acc_text="#8C6D36", paper="#F7F4EC", nom="Vert profond & laiton"),
    "C": dict(ink="#222221", acc="#B5673F", acc_text="#9A5330", paper="#F6F2EC", nom="Anthracite & cuivre"),
}


def variant(p, kind):
    if kind == "couleur":
        return dict(p)
    if kind == "negatif":
        return dict(ink=p["paper"], acc=p["acc"], acc_text=p["acc"], paper=p["ink"])
    return dict(ink="#000000", acc="#000000", acc_text="#000000", paper="#FFFFFF")


def T(font, text, size, x, y, fill, tracking=0, anchor="start"):
    d, w = font.path(text, size, x, y, tracking=tracking, anchor=anchor)
    return f'<path d="{d}" fill="{fill}"/>', w


def circ(x, y, r, fill):
    return f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(r)}" fill="{fill}"/>'


def arcC(cx, cy, R, sw, col, half=40):
    a = math.radians(half)
    x0, y0 = cx + R * math.cos(a), cy + R * math.sin(a)
    x1, y1 = cx + R * math.cos(a), cy - R * math.sin(a)
    return f'<path d="M{n(x0)} {n(y0)}A{n(R)} {n(R)} 0 1 1 {n(x1)} {n(y1)}" stroke="{col}" stroke-width="{n(sw)}" fill="none"/>'


# ---------- symboles (origine = centre, hauteur utile ~ 200·s) ----------
def symA(cx, cy, s, c):
    o = [arcC(cx, cy, 100 * s, 17 * s, c["ink"]), arcC(cx, cy, 65 * s, 17 * s, c["acc"])]
    t = 12 * s
    x0, x1, xm = cx - 22 * s, cx + 22 * s, cx + 15 * s
    o.append(f'<path d="M{n(x0)} {n(cy-31*s)}H{n(x1)}V{n(cy-31*s+t)}H{n(x0+t)}V{n(cy-t/2)}H{n(xm)}V{n(cy+t/2)}H{n(x0+t)}V{n(cy+31*s-t)}H{n(x1)}V{n(cy+31*s)}H{n(x0)}Z" fill="{c["ink"]}"/>')
    for (dx, dy, r) in [(118, -48, 10), (140, -84, 7), (155, -114, 4.6)]:
        o.append(circ(cx + dx * s, cy + dy * s, r * s, c["acc"]))
    return "".join(o)          # emprise : x -108..160, y -120..108


def symB(cx, cy, s, c):
    o = []
    w, g = 60 * s, 9 * s
    x = cx - 99 * s
    base = cy + 100 * s
    d = ""
    for h in (104, 150, 196):
        r = w / 2
        d += f"M{n(x)} {n(base)}V{n(base-h*s+r)}A{n(r)} {n(r)} 0 0 1 {n(x+w)} {n(base-h*s+r)}V{n(base)}Z"
        iw = 22 * s
        ir = iw / 2
        ix = x + (w - iw) / 2
        ih = (h - 40) * s
        d += f"M{n(ix)} {n(base)}H{n(ix+iw)}V{n(base-ih+ir)}A{n(ir)} {n(ir)} 0 0 0 {n(ix)} {n(base-ih+ir)}Z"
        x += w + g
    o.append(f'<path d="{d}" fill="{c["ink"]}" fill-rule="evenodd"/>')
    for (dx, dy, r) in [(116, -84, 9.5), (134, -116, 6.8), (146, -142, 4.6)]:
        o.append(circ(cx + dx * s, cy + dy * s, r * s, c["acc"]))
    return "".join(o)          # emprise : x -99..151, y -147..100


def symC(cx, cy, s, c):
    R = 100 * s
    a0, a1 = math.radians(-36), math.radians(-74)
    x0, y0 = cx + R * math.cos(a0), cy + R * math.sin(a0)
    x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
    o = [f'<path d="M{n(x0)} {n(y0)}A{n(R)} {n(R)} 0 1 1 {n(x1)} {n(y1)}" stroke="{c["ink"]}" stroke-width="{n(5.5*s)}" fill="none"/>']
    o.append(f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(87*s)}" stroke="{c["acc"]}" stroke-width="{n(1.6*s)}" fill="none"/>')
    p, w = T(BOD, "CCE", 60 * s, cx + 2 * s, cy + 21 * s, c["ink"], tracking=7 * s, anchor="middle")
    o.append(p)
    for (rad, r) in [(100, 9.5), (131, 6.8), (156, 4.6)]:
        a = math.radians(-55)
        o.append(circ(cx + rad * s * math.cos(a), cy + rad * s * math.sin(a), r * s, c["acc"]))
    return "".join(o)          # emprise : x -103..103, y -133..103


# ---------- blocs texte ----------
def textA(x, y, c, anchor="start", k=1.0):
    o = []
    p, w1 = T(MAN7, "Châlons Champagne", 62 * k, x, y, c["ink"], tracking=-1.2 * k, anchor=anchor); o.append(p)
    p, w2 = T(MAN5, "Events", 62 * k, x, y + 70 * k, c["ink"], tracking=-1.2 * k, anchor=anchor); o.append(p)
    p, w3 = T(MAN6, TAG, 16.5 * k, x + (2 * k if anchor == "start" else 0), y + 118 * k, c["acc_text"], tracking=6.2 * k, anchor=anchor); o.append(p)
    return "".join(o), w1


def textB(x, y, c, anchor="start", k=1.0):
    o = []
    sz, tr = 50 * k, 6 * k
    w1 = MAR.width("CHÂLONS CHAMPAGNE", sz, tr)
    w0 = MAR.width("EVENTS", sz, 0)
    tr2 = 26 * k
    p, _ = T(MAR, "CHÂLONS CHAMPAGNE", sz, x, y, c["ink"], tracking=tr, anchor=anchor); o.append(p)
    p, _ = T(MAR, "EVENTS", sz, x, y + 64 * k, c["ink"], tracking=tr2, anchor=anchor); o.append(p)
    xl = x if anchor == "start" else x - w1 / 2
    o.append(f'<path d="M{n(xl)} {n(y+92*k)}H{n(xl+w1)}" stroke="{c["acc"]}" stroke-width="{n(1.8*k)}"/>')
    p, _ = T(MAN6, TAG, 15.5 * k, x + (1 * k if anchor == "start" else 0), y + 126 * k, c["acc_text"], tracking=6.4 * k, anchor=anchor); o.append(p)
    return "".join(o), w1


def textC(x, y, c, anchor="start", k=1.0):
    o = []
    p, w1 = T(BOD, "Châlons Champagne", 64 * k, x, y, c["ink"], tracking=0.4 * k, anchor=anchor); o.append(p)
    p, w2 = T(MAN6, "EVENTS", 25 * k, x + (2 * k if anchor == "start" else 0), y + 52 * k, c["ink"], tracking=15 * k, anchor=anchor); o.append(p)
    if anchor == "start":
        o.append(f'<path d="M{n(x+w2+22*k)} {n(y+43*k)}H{n(x+w1)}" stroke="{c["acc"]}" stroke-width="{n(1.8*k)}"/>')
    else:
        o.append(f'<path d="M{n(x-w1/2)} {n(y+43*k)}H{n(x-w2/2-22*k)}M{n(x+w2/2+22*k)} {n(y+43*k)}H{n(x+w1/2)}" stroke="{c["acc"]}" stroke-width="{n(1.8*k)}"/>')
    p, _ = T(MAN6, TAG, 15.5 * k, x + (2 * k if anchor == "start" else 0), y + 100 * k, c["acc_text"], tracking=6.4 * k, anchor=anchor); o.append(p)
    return "".join(o), w1


SYM = {"A": symA, "B": symB, "C": symC}
TXT = {"A": textA, "B": textB, "C": textC}
# emprises des symboles (xmin, xmax, ymin, ymax) à s=1
BOX = {"A": (-109, 160, -120, 109), "B": (-99, 151, -147, 100), "C": (-103, 103, -133, 103)}
TY = {"A": -40, "B": -42, "C": -22}      # ligne de base du 1er rang, relative au centre du symbole


def horizontal(key, c):
    x0, x1, y0, y1 = BOX[key]
    m = 40
    cx, cy = m - x0, m - y0
    tx = cx + x1 + (26 if key != 'C' else 56)
    t, w = TXT[key](tx, cy + TY[key], c)
    body = SYM[key](cx, cy, 1, c) + t
    return body, round(tx + w + m), round(cy + y1 + m)


def vertical(key, c):
    x0, x1, y0, y1 = BOX[key]
    m = 40
    wt = TXT[key](0, 0, c)[1]
    W = round(max(wt, x1 - x0) + 2 * m)
    cxs = W / 2 - (x0 + x1) / 2
    cy = m - y0
    t, w = TXT[key](W / 2, cy + y1 + 96, c, anchor="middle")
    return SYM[key](cxs, cy, 1, c) + t, W, round(cy + y1 + 96 + 150 + m - 10)


def symbole(key, c):
    x0, x1, y0, y1 = BOX[key]
    m = 30
    return SYM[key](m - x0, m - y0, 1, c), round(x1 - x0 + 2 * m), round(y1 - y0 + 2 * m)


def svg(body, W, H, title, bg=None):
    r = f'<rect id="fond" width="{W}" height="{H}" fill="{bg}"/>' if bg else ""
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<title>{_h.escape(title)}</title>{r}<g id="logo">{body}</g></svg>')


NAMES = {"A": "monogramme", "B": "arches", "C": "sceau"}
if __name__ == "__main__":
    OUT = "/home/user/Grafiae/cce-logo/client/svg"
    os.makedirs(OUT, exist_ok=True)
    k = 0
    for key in "ABC":
        for lay, fn in (("horizontal", horizontal), ("vertical", vertical), ("symbole", symbole)):
            for kind in ("couleur", "negatif", "noir"):
                c = variant(PAL[key], kind)
                body, W, H = fn(key, c)
                open(f"{OUT}/proposition{key}_{NAMES[key]}_{lay}_{kind}.svg", "w", encoding="utf-8").write(
                    svg(body, W, H, f"Châlons Champagne Events – proposition {key} – {lay} – {kind}", bg=(c["paper"] if kind == "negatif" else None)))
                k += 1
        if key != "A":      # B et C aussi dans les couleurs actuelles du client
            for lay, fn in (("horizontal", horizontal), ("symbole", symbole)):
                body, W, H = fn(key, PAL["A"])
                open(f"{OUT}/proposition{key}_{NAMES[key]}_{lay}_bleu-or.svg", "w", encoding="utf-8").write(svg(body, W, H, f"proposition {key} – {lay} – bleu & or"))
                k += 1
    print(k, "fichiers")
