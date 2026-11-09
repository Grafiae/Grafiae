"""Bibliothèque : texte -> tracés vectoriels, bulles dessinées à la main, assemblage SVG."""
import io, math, random
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import uharfbuzz as hb

FD = "/tmp/claude-0/-home-user-Grafiae/505c24ee-2e35-5947-935f-cfc53e082e9e/scratchpad/fonts/"


def n(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Font:
    def __init__(self, file, wght=None):
        tt = TTFont(FD + file)
        if wght and "fvar" in tt:
            tt = instancer.instantiateVariableFont(tt, {"wght": wght})
        buf = io.BytesIO()
        tt.save(buf)
        data = buf.getvalue()
        self.tt = TTFont(io.BytesIO(data))
        self.gs = self.tt.getGlyphSet()
        self.upm = self.tt["head"].unitsPerEm
        self.hbf = hb.Font(hb.Face(data))
        os2 = self.tt["OS/2"]
        self.cap = getattr(os2, "sCapHeight", 0) or self.upm * 0.7

    def run(self, text, size, kern=True):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbf, buf, {"kern": kern, "liga": False})
        s = size / self.upm
        return [
            (self.tt.getGlyphName(i.codepoint), p.x_advance * s, p.x_offset * s, p.y_offset * s)
            for i, p in zip(buf.glyph_infos, buf.glyph_positions)
        ]

    def glyph(self, name, size, ox, oy, rot=0.0):
        s = size / self.upm
        c, sn = math.cos(rot), math.sin(rot)
        pen = SVGPathPen(self.gs, ntos=n)
        self.gs[name].draw(TransformPen(pen, (s * c, s * sn, s * sn, -s * c, ox, oy)))
        return pen.getCommands()

    def width(self, text, size, tracking=0):
        r = self.run(text, size)
        return sum(a for _, a, _, _ in r) + tracking * (len(r) - 1)

    def path(self, text, size, x, y, tracking=0, anchor="start"):
        r = self.run(text, size)
        w = sum(a for _, a, _, _ in r) + tracking * (len(r) - 1)
        cur = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
        out = []
        for name, adv, xo, yo in r:
            out.append(self.glyph(name, size, cur + xo, y - yo))
            cur += adv + tracking
        return " ".join(o for o in out if o), w

    def arc(self, text, size, cx, cy, R, mid_deg, tracking=0, bottom=False):
        """Texte sur cercle. Haut : sens horaire. Bas : lisible, lettres vers le centre.
        R = rayon de la ligne de base."""
        r = self.run(text, size)
        w = sum(a for _, a, _, _ in r) + tracking * (len(r) - 1)
        span = w / R
        mid = math.radians(mid_deg)
        out, cur = [], 0.0
        for name, adv, _, _ in r:
            frac = (cur + adv / 2) / R
            th = mid - span / 2 + frac if not bottom else mid + span / 2 - frac
            px, py = cx + R * math.sin(th), cy - R * math.cos(th)
            rot = th if not bottom else th + math.pi
            ox = px - (adv / 2) * math.cos(rot)
            oy = py - (adv / 2) * math.sin(rot)
            out.append(self.glyph(name, size, ox, oy, rot))
            cur += adv + tracking
        return " ".join(o for o in out if o)

    def path_bubble_accents(self, text, size, x, y, tracking=0, anchor="start", r=None):
        """Remplace les accents (É, Â...) par une petite bulle. Retourne (d_texte, [(cx,cy,r)], largeur)."""
        mp = {"É": "E", "È": "E", "Ê": "E", "Â": "A"}
        base = "".join(mp.get(c, c) for c in text)
        runs = self.run(base, size)
        w = sum(a for _, a, _, _ in runs) + tracking * (len(runs) - 1)
        cur = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
        d, bub = [], []
        rad = r or size * 0.075
        for ch, (name, adv, xo, yo) in zip(text, runs):
            d.append(self.glyph(name, size, cur + xo, y - yo))
            if ch in mp:
                bub.append((cur + adv / 2 + (size * 0.05 if ch == "É" else 0),
                            y - self.cap * size / self.upm - size * 0.19, rad))
            cur += adv + tracking
        return " ".join(o for o in d if o), bub, w


# ---------- courbes lisses ----------
def smooth_closed(pts):
    N = len(pts)
    d = f"M{n(pts[0][0])} {n(pts[0][1])}"
    for i in range(N):
        p0, p1, p2, p3 = pts[(i - 1) % N], pts[i], pts[(i + 1) % N], pts[(i + 2) % N]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{n(c1[0])} {n(c1[1])} {n(c2[0])} {n(c2[1])} {n(p2[0])} {n(p2[1])}"
    return d + "Z"


def smooth_open(pts):
    N = len(pts)
    d = f"M{n(pts[0][0])} {n(pts[0][1])}"
    for i in range(N - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, N - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{n(c1[0])} {n(c1[1])} {n(c2[0])} {n(c2[1])} {n(p2[0])} {n(p2[1])}"
    return d


def ink_ring(cx, cy, r, seed=0, w=None, wob=0.04, N=16):
    """Bulle 'encrée à la main' : anneau à épaisseur variable, contour légèrement irrégulier.
    Forme pleine (fill-rule evenodd) -> reste un vrai vectoriel sans contour."""
    rnd = random.Random(seed)
    w = w if w is not None else max(r * 0.17, 1.2)
    ph = rnd.uniform(0, 2 * math.pi)
    outer, inner = [], []
    for i in range(N):
        a = 2 * math.pi * i / N
        ro = r * (1 + rnd.uniform(-wob, wob))
        th = w * (0.35 + 0.65 * (0.5 + 0.5 * math.cos(a - ph)))
        ri = ro - th
        outer.append((cx + ro * math.cos(a), cy + ro * math.sin(a)))
        inner.append((cx + ri * math.cos(a + 0.03), cy + ri * math.sin(a + 0.03)))
    return smooth_closed(outer) + smooth_closed(inner[::-1])


def ink_disc(cx, cy, r, seed=0, wob=0.06, N=12):
    rnd = random.Random(seed + 77)
    pts = []
    for i in range(N):
        a = 2 * math.pi * i / N
        rr = r * (1 + rnd.uniform(-wob, wob))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return smooth_closed(pts)


def brush_stroke(center_pts, wmax, taper=0.8):
    """Trait de pinceau : polygone lissé à largeur variable autour d'une ligne médiane."""
    m = len(center_pts)
    left, right = [], []
    for i, (x, y) in enumerate(center_pts):
        a = center_pts[max(i - 1, 0)]
        b = center_pts[min(i + 1, m - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        t = i / (m - 1)
        wv = wmax * (math.sin(math.pi * t) ** taper) * (0.55 + 0.45 * (1 - t)) + 0.4
        left.append((x + nx * wv / 2, y + ny * wv / 2))
        right.append((x - nx * wv / 2, y - ny * wv / 2))
    pts = left + right[::-1]
    return smooth_closed(pts)


def bezier_pts(p0, p1, p2, p3, k=28):
    out = []
    for i in range(k + 1):
        t = i / k
        u = 1 - t
        out.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return out


def arch_d(x0, w, base, h):
    r = w / 2
    return f"M{n(x0)} {n(base)}V{n(base - h + r)}A{n(r)} {n(r)} 0 0 1 {n(x0 + w)} {n(base - h + r)}V{n(base)}"


# ---------- assemblage SVG ----------
INK = "#16291F"      # vert bouteille profond
CRAIE = "#F4ECDB"    # craie / crème
GOLD_STOPS = [(0, "#8B6420"), (0.28, "#D8B766"), (0.5, "#B08130"), (0.74, "#DDBF74"), (1, "#97712A")]

COLORS = {
    "couleur": dict(ink=INK, gold="url(#or)", bg=None, paper=CRAIE, name="couleur"),
    "negatif": dict(ink=CRAIE, gold="url(#or)", bg=INK, paper=INK, name="negatif"),
    "negatif-transparent": dict(ink=CRAIE, gold="url(#or)", bg=None, paper=INK, name="negatif-transparent"),
    "mono": dict(ink="#000000", gold="#000000", bg=None, paper="#FFFFFF", name="mono"),
}


def svg_doc(body, W, H, c, title):
    stops = "".join(f'<stop offset="{o}" stop-color="{col}"/>' for o, col in GOLD_STOPS)
    defs = (f'<defs><linearGradient id="or" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H}">{stops}</linearGradient></defs>')
    bg = f'<rect id="fond" width="{W}" height="{H}" fill="{c["bg"]}"/>' if c["bg"] else ""
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<title>{title}</title>{defs}{bg}<g id="logo">{body}</g></svg>')


def P(d, fill, extra=""):
    return f'<path d="{d}" fill="{fill}" fill-rule="nonzero" {extra}/>'


def line(x1, y1, x2, y2, col, w=1.5, cap="butt"):
    return f'<path d="M{n(x1)} {n(y1)}L{n(x2)} {n(y2)}" stroke="{col}" stroke-width="{n(w)}" stroke-linecap="{cap}" fill="none"/>'


def circle_stroke(cx, cy, r, col, w):
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" stroke="{col}" stroke-width="{n(w)}" fill="none"/>'
