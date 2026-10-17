"""
Maison Renard — vitrine de Noël « montagne de boîtes de champagne ».

Génère toute la scène Blender (géométrie, matériaux, éclairage, caméra) :
un renard-jouet en livrée de groom, perché sur une échelle dorée, pose une
étoile au sommet d'une pyramide de coffrets de champagne rouges, devant une
fenêtre ronde donnant sur une ville la nuit.

Utilisation (Blender 4.2+ / 5.x) :
    blender -b -P build_scene.py                       -> crée renard_champagne.blend
    blender -b -P build_scene.py -- --render out.png   -> crée le .blend et rend l'image
    blender -b -P build_scene.py -- --preview --render preview.png
Ou ouvrir le script dans l'onglet Scripting de Blender et cliquer « Run Script ».
"""

import math
import os
import random
import sys

import bpy  # bpy avant bmesh (requis hors de Blender, module pip)
import bmesh
from mathutils import Euler, Matrix, Vector

SEED = 7
HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()

BRAND = "MAISON RENARD"
SUB = "CHAMPAGNE  ·  REIMS"


# --------------------------------------------------------------------------
# Arguments
# --------------------------------------------------------------------------
def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    opts = {"render": None, "preview": False, "blend": os.path.join(HERE, "renard_champagne.blend")}
    i = 0
    while i < len(argv):
        if argv[i] == "--render":
            opts["render"] = os.path.abspath(argv[i + 1]); i += 1
        elif argv[i] == "--blend":
            opts["blend"] = os.path.abspath(argv[i + 1]); i += 1
        elif argv[i] == "--preview":
            opts["preview"] = True
        i += 1
    return opts


# --------------------------------------------------------------------------
# Helpers : matériaux
# --------------------------------------------------------------------------
def set_input(node, names, value):
    for n in (names if isinstance(names, (list, tuple)) else [names]):
        if n in node.inputs:
            node.inputs[n].default_value = value
            return


def principled(name, color, rough=0.5, metal=0.0, coat=0.0, sheen=0.0,
               emission=None, emission_strength=0.0, aniso=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_input(bsdf, "Base Color", (*color, 1.0))
    set_input(bsdf, "Roughness", rough)
    set_input(bsdf, "Metallic", metal)
    set_input(bsdf, ["Coat Weight", "Clearcoat"], coat)
    set_input(bsdf, ["Coat Roughness", "Clearcoat Roughness"], 0.08)
    set_input(bsdf, ["Sheen Weight", "Sheen"], sheen)
    set_input(bsdf, "Anisotropic", aniso)
    if emission is not None:
        set_input(bsdf, ["Emission Color", "Emission"], (*emission, 1.0))
        set_input(bsdf, "Emission Strength", emission_strength)
    mat.diffuse_color = (*color, 1.0)
    return mat


def emissive(name, color, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*color, 1.0)
    em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    mat.diffuse_color = (*color, 1.0)
    return mat


def box_red_material():
    """Rouge laqué/carton satiné, teinte légèrement différente par boîte."""
    mat = principled("Coffret_Rouge", (0.62, 0.035, 0.05), rough=0.45, coat=0.1)
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    info = nt.nodes.new("ShaderNodeObjectInfo")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (0.42, 0.012, 0.025, 1)
    ramp.color_ramp.elements[1].color = (0.68, 0.045, 0.060, 1)
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 180.0
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.04
    nt.links.new(info.outputs["Random"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def carpet_material():
    mat = principled("Moquette_Rose", (0.95, 0.50, 0.53), rough=0.95, sheen=0.6)
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 900.0
    noise.inputs["Detail"].default_value = 4.0
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.35
    nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


# --------------------------------------------------------------------------
# Helpers : géométrie
# --------------------------------------------------------------------------
def link(obj, collection=None):
    (collection or bpy.context.scene.collection).objects.link(obj)
    return obj


def obj_from_bm(name, bm, mats, collection=None, smooth=False):
    if smooth:
        for f in bm.faces:
            f.smooth = True
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for m in (mats if isinstance(mats, (list, tuple)) else [mats]):
        me.materials.append(m)
    return link(bpy.data.objects.new(name, me), collection)


def sphere(name, loc, scale, mat, col=None, rot=(0, 0, 0), seg=32):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=1.0)
    ob = obj_from_bm(name, bm, mat, col, smooth=True)
    ob.location = loc
    ob.scale = scale if isinstance(scale, (tuple, list)) else (scale,) * 3
    ob.rotation_euler = rot
    return ob


def cylinder(name, r1, r2, depth, mat, col=None, seg=32, smooth=True):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r1, radius2=r2, depth=depth)
    bm.normal_update()
    ob = obj_from_bm(name, bm, mat, col)
    if smooth:
        for p in ob.data.polygons:
            p.use_smooth = abs(p.normal.z) < 0.9
    return ob


def place_between(ob, p1, p2):
    """Oriente un objet construit le long de Z entre deux points."""
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    ob.location = (p1 + p2) / 2
    ob.rotation_mode = "QUATERNION"
    ob.rotation_quaternion = d.to_track_quat("Z", "Y")
    return ob


def limb(name, p1, p2, r1, r2, mat, col=None):
    length = (Vector(p2) - Vector(p1)).length
    ob = cylinder(name, r1, r2, length, mat, col)
    return place_between(ob, p1, p2)


def torus(name, R, r, mat, col=None, seg=48, rseg=16, r_axial=None):
    """Tore ; r_axial != r donne une section elliptique (ruban plat)."""
    ra = r if r_axial is None else r_axial
    bm = bmesh.new()
    rings = []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        ring = []
        for j in range(rseg):
            b = 2 * math.pi * j / rseg
            x = (R + r * math.cos(b)) * math.cos(a)
            y = (R + r * math.cos(b)) * math.sin(a)
            ring.append(bm.verts.new((x, y, ra * math.sin(b))))
        rings.append(ring)
    for i in range(seg):
        for j in range(rseg):
            a, b = rings[i], rings[(i + 1) % seg]
            bm.faces.new((a[j], b[j], b[(j + 1) % rseg], a[(j + 1) % rseg]))
    bm.normal_update()
    return obj_from_bm(name, bm, mat, col, smooth=True)


def rounded_box(name, size, mat, col=None, bevel=0.03, segments=3):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=size, verts=bm.verts)
    bmesh.ops.bevel(bm, geom=list(bm.verts) + list(bm.edges), offset=bevel,
                    segments=segments, profile=0.5, affect="EDGES")
    return obj_from_bm(name, bm, mat, col, smooth=segments > 2)


def star_mesh(name, r_out, r_in, depth, mat, col=None, points=5):
    """Étoile facettée (pointes en relief) dans le plan XZ, face vers -Y."""
    bm = bmesh.new()
    ring = []
    for i in range(points * 2):
        a = math.pi / 2 + i * math.pi / points
        r = r_out if i % 2 == 0 else r_in
        ring.append(bm.verts.new((r * math.cos(a), 0.0, r * math.sin(a))))
    front = bm.verts.new((0, -depth, 0))
    back = bm.verts.new((0, depth, 0))
    n = len(ring)
    for i in range(n):
        bm.faces.new((ring[i], ring[(i + 1) % n], front))
        bm.faces.new((ring[(i + 1) % n], ring[i], back))
    bm.normal_update()
    return obj_from_bm(name, bm, mat, col)


def text_obj(name, body, size, mat, font, col=None, extrude=0.0015):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body
    cu.size = size
    cu.align_x = "CENTER"
    cu.align_y = "CENTER"
    cu.extrude = extrude
    cu.space_character = 1.12
    if font:
        cu.font = font
    cu.materials.append(mat)
    return link(bpy.data.objects.new(name, cu), col)


def load_font():
    candidates = [
        # Windows
        "C:/Windows/Fonts/didot.ttf", "C:/Windows/Fonts/BOD_R.TTF", "C:/Windows/Fonts/times.ttf",
        "C:/Windows/Fonts/georgia.ttf",
        # macOS
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/Library/Fonts/Times New Roman.ttf",
        # Linux
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return bpy.data.fonts.load(p)
            except RuntimeError:
                pass
    return None


# --------------------------------------------------------------------------
# Construction de la scène
# --------------------------------------------------------------------------
class Scene:
    def __init__(self):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.rng = random.Random(SEED)
        self.font = load_font()
        self.cols = {}
        for c in ("Decor", "Ville", "Coffrets", "Deco_Noel", "Renard", "Lumieres"):
            col = bpy.data.collections.new(c)
            bpy.context.scene.collection.children.link(col)
            self.cols[c] = col
        self.M = {
            "box": box_red_material(),
            "line": principled("Filet_Blanc", (0.93, 0.88, 0.84), rough=0.35, coat=0.3),
            "ribbon": principled("Ruban_Satin", (0.55, 0.02, 0.035), rough=0.28, sheen=0.8, aniso=0.6),
            "wall": principled("Mur_Rouge", (0.55, 0.035, 0.06), rough=0.75),
            "wall_dark": principled("Mur_Rouge_Fonce", (0.30, 0.015, 0.03), rough=0.7),
            "carpet": carpet_material(),
            "gold": principled("Or", (1.0, 0.70, 0.33), rough=0.22, metal=1.0),
            "gold_star": principled("Or_Etoile", (1.0, 0.76, 0.38), rough=0.12, metal=1.0,
                                    emission=(1.0, 0.75, 0.35), emission_strength=0.15),
            "bauble_red": principled("Boule_Rouge", (0.60, 0.02, 0.03), rough=0.12, metal=0.7, coat=1.0),
            "leaf": principled("Feuillage", (0.06, 0.20, 0.06), rough=0.45, coat=0.2),
            "sky": emissive("Ciel_Nuit", (0.20, 0.010, 0.020), 0.35),
            "city": principled("Immeubles", (0.16, 0.008, 0.016), rough=0.8),
            "city_far": principled("Immeubles_Loin", (0.24, 0.014, 0.026), rough=0.8,
                                   emission=(0.22, 0.012, 0.022), emission_strength=0.25),
            "window": emissive("Fenetres_Allumees", (1.0, 0.62, 0.22), 6.0),
            "sky_star": emissive("Etoiles_Ciel", (1.0, 0.72, 0.30), 12.0),
            # Renard-jouet : bois laqué
            "fox": principled("Renard_Orange", (0.88, 0.25, 0.04), rough=0.3, coat=1.0),
            "fox_white": principled("Renard_Blanc", (0.92, 0.88, 0.82), rough=0.35, coat=1.0),
            "black": principled("Noir_Laque", (0.012, 0.010, 0.010), rough=0.12, coat=1.0),
            "jacket": principled("Livree_Rouge", (0.58, 0.02, 0.04), rough=0.3, coat=1.0),
            "glove": principled("Gants_Blancs", (0.92, 0.90, 0.86), rough=0.5),
        }
        self.boxes = []        # (x0, x1, y0, y1, ztop, obj, dims)

    # ---------------- décor ----------------
    def build_room(self):
        col = self.cols["Decor"]
        # Sol moquette (estrade)
        floor = rounded_box("Estrade", (24, 9.5, 0.6), self.M["carpet"], col, bevel=0.04, segments=2)
        floor.location = (0, -1.75, -0.3)
        skirt = rounded_box("Estrade_Socle", (24, 0.2, 0.6), self.M["wall_dark"], col, bevel=0.01, segments=1)
        skirt.location = (0, -6.4, -0.75)

        # Mur avec ouverture ronde
        self.win_c = Vector((0.3, 2.8, 4.1))
        self.win_r = 3.0
        wall = rounded_box("Mur", (26, 0.5, 16), self.M["wall"], col, bevel=0.0, segments=1)
        wall.location = (0, self.win_c.y, 7.5)
        cutter = cylinder("Decoupe_Fenetre", self.win_r, self.win_r, 2.0, self.M["wall"], col, seg=128)
        cutter.rotation_euler = (math.pi / 2, 0, 0)
        cutter.location = self.win_c
        cutter.hide_render = True
        cutter.hide_viewport = True
        mod = wall.modifiers.new("Fenetre", "BOOLEAN")
        mod.operation = "DIFFERENCE"
        mod.object = cutter
        mod.solver = "EXACT"
        bev = wall.modifiers.new("Arrondi", "BEVEL")
        bev.width = 0.06
        bev.segments = 4
        bev.limit_method = "ANGLE"

        # Encadrement rond (moulure) en retrait
        ring = torus("Moulure_Fenetre", self.win_r + 0.02, 0.09, self.M["wall_dark"], col, seg=128)
        ring.rotation_euler = (math.pi / 2, 0, 0)
        ring.location = self.win_c + Vector((0, 0.27, 0))
        ring.scale = (1, 1, 1.6)

        # Croisillons de la fenêtre
        mull_y = self.win_c.y + 0.45
        r = self.win_r
        for i, x in enumerate((-1.25, 1.25)):
            m = rounded_box(f"Croisillon_V{i}", (0.16, 0.14, 2 * r), self.M["wall_dark"], col, bevel=0.01, segments=1)
            m.location = (self.win_c.x + x, mull_y, self.win_c.z)
        m = rounded_box("Croisillon_H", (2 * r, 0.14, 0.16), self.M["wall_dark"], col, bevel=0.01, segments=1)
        m.location = (self.win_c.x, mull_y, self.win_c.z + 1.05)
        sill = rounded_box("Appui_Fenetre", (2 * r, 0.14, 0.12), self.M["wall_dark"], col, bevel=0.01, segments=1)
        sill.location = (self.win_c.x, mull_y, self.win_c.z - 0.85)

    def build_city(self):
        col = self.cols["Ville"]
        rng = random.Random(SEED + 1)
        sky = rounded_box("Ciel", (30, 0.1, 22), self.M["sky"], col, bevel=0.0, segments=1)
        sky.location = (0, 16, 6)

        def skyline(y, mat, zmin, zmax, depth, windows):
            x = -9.0
            i = 0
            while x < 9.5:
                w = rng.uniform(0.6, 1.5)
                h = rng.uniform(zmin, zmax)
                b = rounded_box(f"Immeuble_{y:.0f}_{i}", (w, depth, h), mat, col, bevel=0.0, segments=1)
                b.location = (x + w / 2, y, h / 2)
                if rng.random() < 0.3:  # petite tour / toit en gradins
                    t = rounded_box(f"Toit_{y:.0f}_{i}", (w * 0.5, depth * 0.8, h * 0.15), mat, col, bevel=0.0, segments=1)
                    t.location = (x + w / 2, y, h + h * 0.075)
                if windows:
                    for row in range(int(h / 0.32)):
                        for c in range(max(1, int(w / 0.22))):
                            if rng.random() < 0.18:
                                wz = 0.25 + row * 0.32
                                wx = x + 0.12 + c * 0.22
                                if wz < h - 0.15 and wx < x + w - 0.08:
                                    win = rounded_box("Fenetre", (0.07, 0.02, 0.11), self.M["window"], col, bevel=0.0, segments=1)
                                    win.location = (wx, y - depth / 2 - 0.01, wz)
                x += w + rng.uniform(-0.1, 0.25)
                i += 1

        skyline(12.0, self.M["city_far"], 4.0, 9.0, 1.0, windows=False)
        skyline(8.0, self.M["city"], 2.5, 6.8, 1.2, windows=True)

        # Étoiles dans le ciel (petites étoiles à 5 branches + points)
        for i in range(26):
            x = rng.uniform(-3.2, 3.6)
            z = rng.uniform(5.2, 8.2)
            s = rng.uniform(0.035, 0.08)
            st = star_mesh(f"Etoile_Ciel_{i}", s, s * 0.45, s * 0.2, self.M["sky_star"], col)
            st.location = (x, 15.0, z)
            st.rotation_euler = (0, rng.uniform(-0.4, 0.4), 0)

    # ---------------- coffrets ----------------
    def add_box(self, name, w, d, h, x, y, rot_z, tall):
        """Coffret biseauté + filets blancs + texte, posé sur ce qui est dessous."""
        # Hauteur de pose : sommet le plus haut des coffrets sous l'emprise
        hw, hd = w / 2 * 0.85, d / 2 * 0.85
        z = 0.0
        for (x0, x1, y0, y1, zt, *_r) in self.boxes:
            if x - hw < x1 and x + hw > x0 and y - hd < y1 and y + hd > y0:
                z = max(z, zt)

        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(w, d, h), verts=bm.verts)
        bmesh.ops.translate(bm, vec=(0, 0, h / 2), verts=bm.verts)
        bmesh.ops.bevel(bm, geom=list(bm.verts) + list(bm.edges), offset=0.012,
                        segments=2, profile=0.5, affect="EDGES")
        for f in bm.faces:
            f.material_index = 0

        # Filets blancs (cadre fin) sur la face avant et les côtés
        def frame(center, u, v, hu, hv, inset, width):
            corners_o = [center + u * (hu - inset) * su + v * (hv - inset) * sv
                         for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            corners_i = [center + u * (hu - inset - width) * su + v * (hv - inset - width) * sv
                         for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            vo = [bm.verts.new(c) for c in corners_o]
            vi = [bm.verts.new(c) for c in corners_i]
            for k in range(4):
                f = bm.faces.new((vo[k], vo[(k + 1) % 4], vi[(k + 1) % 4], vi[k]))
                f.material_index = 1

        e = 0.0015
        inset = min(w, h) * 0.07
        lw = 0.012
        X, Y, Z = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))
        frame(Vector((0, -d / 2 - e, h / 2)), X, Z, w / 2, h / 2, inset, lw)
        frame(Vector((w / 2 + e, 0, h / 2)), -Y, Z, d / 2, h / 2, min(d, h) * 0.07, lw)
        frame(Vector((-w / 2 - e, 0, h / 2)), Y, Z, d / 2, h / 2, min(d, h) * 0.07, lw)
        frame(Vector((0, 0, h + e)), X, Y, w / 2, d / 2, min(w, d) * 0.07, lw)
        bm.normal_update()

        ob = obj_from_bm(name, bm, [self.M["box"], self.M["line"]], self.cols["Coffrets"])
        ob.location = (x, y, z)
        ob.rotation_euler = (0, 0, rot_z)

        # Texte
        fy = -d / 2 - 0.004
        if tall:
            size = min(w * 0.16, h * 0.075)
            t = text_obj(name + "_Marque", BRAND, size, self.M["line"], self.font, self.cols["Coffrets"])
            t.location = (0, fy, h * 0.55)
            t.rotation_euler = (math.pi / 2, math.pi / 2, 0)
            t.parent = ob
        else:
            size = min(w * 0.065, h * 0.11)
            t = text_obj(name + "_Marque", BRAND, size, self.M["line"], self.font, self.cols["Coffrets"])
            t.location = (0, fy, h * 0.53)
            t.rotation_euler = (math.pi / 2, 0, 0)
            t.parent = ob
            if w > 0.9 and h > 0.5:
                s = text_obj(name + "_Sous", SUB, size * 0.42, self.M["line"], self.font, self.cols["Coffrets"])
                s.location = (0, fy, h * 0.53 - size * 1.1)
                s.rotation_euler = (math.pi / 2, 0, 0)
                s.parent = ob

        self.boxes.append((x - w / 2, x + w / 2, y - d / 2, y + d / 2, z + h, ob, (w, d, h)))
        return ob

    def add_ribbon(self, box, rel_x, diagonal=False):
        w, d, h = box[6]
        ob = box[5]
        col = self.cols["Coffrets"]
        rw = 0.11
        band = rounded_box(ob.name + "_Ruban", (rw, d + 0.02, h + 0.02), self.M["ribbon"], col, bevel=0.004, segments=1)
        band.parent = ob
        band.location = (rel_x * w, 0, h / 2)
        band2 = rounded_box(ob.name + "_Ruban2", (w + 0.02, rw * 0.9, 0.012), self.M["ribbon"], col, bevel=0.003, segments=1)
        band2.parent = ob
        band2.location = (0, 0, h + 0.006)
        if diagonal:
            band.rotation_euler = (0, 0.35, 0)
            band.scale = (1, 1, 1.12)

        # Nœud sur le dessus, côté avant
        knot_pos = Vector((rel_x * w, -d / 2 + 0.12, h + 0.04))
        for side in (-1, 1):
            loop = torus(ob.name + f"_Boucle{side}", 0.11, 0.008, self.M["ribbon"], col, r_axial=0.045)
            loop.parent = ob
            loop.location = knot_pos + Vector((side * 0.15, 0.0, 0.07))
            loop.rotation_euler = (math.pi / 2, side * 0.5, side * 0.6)
            loop.scale = (1.35, 0.7, 1.0)
        k = sphere(ob.name + "_Noeud", knot_pos + Vector((0, -0.03, 0.03)), (0.05, 0.035, 0.045), self.M["ribbon"], col)
        k.parent = ob
        for side in (-1, 1):
            tail = rounded_box(ob.name + f"_Pan{side}", (0.07, 0.012, 0.2), self.M["ribbon"], col, bevel=0.003, segments=1)
            tail.parent = ob
            tail.location = Vector((rel_x * w + side * 0.1, -d / 2 - 0.02, h - 0.07))
            tail.rotation_euler = (0, side * 0.7, 0)

    def build_pile(self):
        rng = self.rng
        cx = 0.35
        levels = [
            # (largeur de rangée, profondeurs y des couches)
            (6.4, (0.8, -0.3)),
            (5.3, (0.65, -0.1)),
            (4.2, (0.55, 0.05)),
            (3.0, (0.45, 0.1)),
            (1.8, (0.3,)),
        ]
        n = 0
        for L, (width, ys) in enumerate(levels):
            for yi, y in enumerate(ys):
                x = cx - width / 2 + rng.uniform(-0.05, 0.05) + (0.3 if yi == 1 else 0)
                end = cx + width / 2
                while x < end - 0.35:
                    tall = rng.random() < (0.2 if L < 2 else 0.3)
                    if tall:
                        w, h, d = rng.uniform(0.5, 0.6), rng.uniform(0.85, 0.95), rng.uniform(0.45, 0.55)
                    else:
                        w, h, d = rng.uniform(0.85, 1.35), rng.uniform(0.42, 0.52), rng.uniform(0.65, 0.85)
                    w = min(w, end - x)
                    if w < 0.45:
                        break
                    if not tall and w < 0.7:
                        tall, h, d = True, rng.uniform(0.85, 0.95), 0.5
                    self.add_box(f"Coffret_{n:02d}", w, d, h, x + w / 2,
                                 y + rng.uniform(-0.08, 0.08), math.radians(rng.uniform(-5, 5)), tall)
                    n += 1
                    x += w + rng.uniform(0.01, 0.04)

        # Coffret sommet (grand, vertical, comme une bouteille)
        apex = self.add_box("Coffret_Sommet", 0.6, 0.5, 1.15, cx - 0.05, 0.1, math.radians(2), True)
        top = self.boxes[-1]
        self.apex = Vector((cx - 0.05, 0.1 - 0.25, top[4]))

        # Rubans sur une sélection de coffrets visibles
        front = [b for b in self.boxes if b[2] < 0.2]
        for b in rng.sample(front, k=min(7, len(front))):
            self.add_ribbon(b, rng.choice((-1, 1)) * rng.uniform(0.3, 0.36), diagonal=rng.random() < 0.4)

    # ---------------- décorations ----------------
    def add_sprig(self, base, direction, length, col, rng):
        """Petite branche de feuillage (type olivier/houx) posée sur un coffret."""
        direction = Vector(direction).normalized()
        n = int(length / 0.045)
        for i in range(n):
            t = i / max(1, n - 1)
            p = Vector(base) + direction * length * t
            for side in (-1, 1):
                ang = rng.uniform(0.6, 1.0) * side
                rot = Euler((rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3),
                             math.atan2(direction.y, direction.x) + ang), "XYZ")
                leaf = sphere("Feuille", p + Vector((0, 0, 0.01)),
                              (0.075 * (1 - 0.5 * t), 0.022, 0.008), self.M["leaf"], col, rot=rot, seg=12)
        stem = limb("Tige", base, Vector(base) + direction * length, 0.008, 0.004, self.M["leaf"], col)

    def build_decorations(self):
        col = self.cols["Deco_Noel"]
        rng = random.Random(SEED + 2)
        cands = [b for b in self.boxes if b[2] < 0.35]
        rng.shuffle(cands)
        placed = 0
        for b in cands:
            if placed >= 9:
                break
            x0, x1, y0, y1, zt = b[:5]
            r = rng.uniform(0.11, 0.15)
            x = rng.uniform(x0 + 0.2, x1 - 0.2)
            y = y0 + 0.2
            # Ne pas poser une boule sous un coffret
            covered = any(o is not b and o[0] < x < o[1] and o[2] < y < o[3] and o[4] > zt + 0.05
                          for o in self.boxes)
            if covered:
                continue
            gold = rng.random() < 0.6
            mat = self.M["gold"] if gold else self.M["bauble_red"]
            c = Vector((x, y, zt + r))
            sphere("Boule", c, r, mat, col)
            cap = cylinder("Attache", r * 0.22, r * 0.22, r * 0.25, self.M["gold"], col)
            cap.location = c + Vector((0, 0, r * 0.98))
            loop = torus("Anneau", r * 0.12, r * 0.03, self.M["gold"], col, seg=16, rseg=6)
            loop.location = c + Vector((0, 0, r * 1.2))
            loop.rotation_euler = (math.pi / 2, 0, 0)
            for k in range(2):
                ang = rng.uniform(0, 2 * math.pi)
                self.add_sprig(c + Vector((0, 0, -r * 0.9)), (math.cos(ang), math.sin(ang) * 0.5 - 0.3, 0.05),
                               rng.uniform(0.3, 0.45), col, rng)
            placed += 1

    # ---------------- renard ----------------
    def build_fox(self):
        col = self.cols["Renard"]
        M = self.M
        star_pos = self.apex + Vector((0.05, -0.15, 0.48))
        zf = star_pos.z - 2.75           # hauteur des pieds (sur l'échelle)
        fx, fy = -1.45, -1.3            # position du corps
        self.ladder = (fx - 0.35, fx + 0.45, fy + 0.25)

        # --- Échelle dorée ---
        lx0, lx1, ly = self.ladder
        top_z = zf + 2.4
        lean = 0.55
        for i, lx in enumerate((lx0, lx1)):
            limb(f"Echelle_Montant{i}", (lx, ly - 0.25, 0), (lx, ly + lean, top_z), 0.035, 0.035, M["gold"], col)
            sphere(f"Echelle_Embout{i}", (lx, ly + lean, top_z), 0.045, M["gold"], col)
        z = 0.38
        while z < top_z - 0.1:
            yy = ly - 0.25 + (lean + 0.25) * z / top_z
            limb("Echelle_Barreau", (lx0, yy, z), (lx1, yy, z), 0.025, 0.025, M["gold"], col)
            z += 0.42

        # --- Jambes (pantalon noir laqué, bottes) ---
        hipL, hipR = Vector((fx - 0.14, fy, zf + 1.05)), Vector((fx + 0.14, fy, zf + 1.05))
        kneeL, footL = Vector((fx - 0.18, fy - 0.05, zf + 0.55)), Vector((fx - 0.17, fy + 0.02, zf + 0.12))
        kneeR, footR = Vector((fx + 0.42, fy - 0.25, zf + 0.82)), Vector((fx + 0.55, fy - 0.05, zf + 0.42))
        for side, (hip, knee, foot) in {"G": (hipL, kneeL, footL), "D": (hipR, kneeR, footR)}.items():
            limb(f"Cuisse_{side}", hip, knee, 0.12, 0.10, M["black"], col)
            sphere(f"Genou_{side}", knee, 0.105, M["black"], col)
            limb(f"Mollet_{side}", knee, foot, 0.10, 0.095, M["black"], col)
            boot = sphere(f"Botte_{side}", foot + Vector((0, -0.08, -0.05)), (0.11, 0.2, 0.09), M["black"], col)
            sole = rounded_box(f"Talon_{side}", (0.18, 0.32, 0.04), M["black"], col, bevel=0.015, segments=2)
            sole.location = foot + Vector((0, -0.06, -0.12))

        # --- Corps : livrée de groom rouge ---
        torso = rounded_box("Veste", (0.66, 0.44, 0.85), M["jacket"], col, bevel=0.14, segments=4)
        torso.location = (fx, fy, zf + 1.42)
        basque = cylinder("Basque_Veste", 0.36, 0.33, 0.18, M["jacket"], col)
        basque.location = (fx, fy, zf + 1.02)
        basque.scale = (1.0, 0.68, 1.0)
        belt = cylinder("Ceinture", 0.345, 0.345, 0.08, M["gold"], col)
        belt.location = (fx, fy, zf + 1.12)
        belt.scale = (1.0, 0.68, 1.0)
        buckle = rounded_box("Boucle", (0.13, 0.03, 0.1), M["gold"], col, bevel=0.01, segments=2)
        buckle.location = (fx, fy - 0.235, zf + 1.12)
        for side in (-1, 1):
            for k in range(6):
                sphere("Bouton", (fx + side * 0.13, fy - 0.222, zf + 1.24 + k * 0.095), (0.022, 0.012, 0.022), M["gold"], col)
            ep = sphere("Epaulette", (fx + side * 0.33, fy, zf + 1.83), (0.15, 0.17, 0.06), M["gold"], col)
            for j in range(7):
                a = -0.8 + j * 0.27
                limb("Frange", (fx + side * (0.33 + 0.13 * math.cos(a)), fy + 0.15 * math.sin(a), zf + 1.81),
                     (fx + side * (0.34 + 0.14 * math.cos(a)), fy + 0.16 * math.sin(a), zf + 1.71), 0.012, 0.01, M["gold"], col)
        collar = cylinder("Col", 0.16, 0.15, 0.09, M["gold"], col)
        collar.location = (fx, fy, zf + 1.88)
        # Plastron blanc (fourrure du poitrail) qui dépasse du col
        sphere("Poitrail", (fx, fy - 0.12, zf + 1.86), (0.13, 0.08, 0.09), M["fox_white"], col)

        # --- Bras ---
        shL, shR = Vector((fx - 0.4, fy, zf + 1.72)), Vector((fx + 0.4, fy, zf + 1.72))
        # bras gauche : tient le montant de l'échelle
        elL, haL = Vector((fx - 0.55, fy - 0.05, zf + 1.32)), Vector((lx0 + 0.02, fy + 0.05, zf + 1.02))
        # bras droit : lève l'étoile vers le sommet
        haR = star_pos + Vector((-0.12, -0.02, -0.22))
        elR = shR.lerp(haR, 0.5) + Vector((0.0, -0.12, -0.12))
        for side, (sh, el, ha) in {"G": (shL, elL, haL), "D": (shR, elR, haR)}.items():
            sphere(f"Epaule_{side}", sh, 0.11, M["jacket"], col)
            limb(f"Bras_{side}", sh, el, 0.095, 0.085, M["jacket"], col)
            sphere(f"Coude_{side}", el, 0.088, M["jacket"], col)
            limb(f"AvantBras_{side}", el, ha, 0.085, 0.075, M["jacket"], col)
            cuff = torus(f"Manchette_{side}", 0.08, 0.022, M["gold"], col, seg=32, rseg=8)
            place_between(cuff, ha.lerp(el, 0.18) - (ha - el).normalized() * 0.001, ha.lerp(el, 0.17))
            sphere(f"Gant_{side}", ha, (0.1, 0.1, 0.1), M["glove"], col)

        # --- Étoile dorée facettée tenue en main ---
        star = star_mesh("Etoile_Sommet", 0.34, 0.15, 0.09, M["gold_star"], col)
        star.location = star_pos
        star.rotation_euler = (0.1, -0.25, -0.12)
        # Scintillement : deux fins rayons lumineux croisés sur la pointe
        glint_c = star_pos + Vector((0.05, -0.12, 0.3))
        for k, ang in enumerate((0.0, math.pi / 2, math.pi / 4, -math.pi / 4)):
            ln = 0.42 if k < 2 else 0.18
            ray = sphere(f"Scintillement_{k}", glint_c, (0.006, 0.006, ln), M["sky_star"], col, rot=(0, ang, 0), seg=12)
        sphere("Scintillement_Coeur", glint_c, 0.025, M["sky_star"], col)

        # --- Tête de renard ---
        H = Vector((fx + 0.03, fy - 0.02, zf + 2.25))
        sphere("Cou", H + Vector((0, 0.02, -0.28)), (0.13, 0.13, 0.12), M["fox"], col)
        sphere("Tete", H, (0.3, 0.27, 0.27), M["fox"], col)
        # joues blanches ébouriffées
        for side in (-1, 1):
            sphere("Joue", H + Vector((side * 0.2, -0.1, -0.12)), (0.16, 0.13, 0.12), M["fox_white"], col,
                   rot=(0, side * 0.5, 0))
        # museau
        snout = cylinder("Museau", 0.13, 0.035, 0.36, M["fox"], col)
        place_between(snout, H + Vector((0, -0.12, -0.06)), H + Vector((0, -0.48, -0.11)))
        sphere("Machoire", H + Vector((0, -0.28, -0.13)), (0.1, 0.18, 0.06), M["fox_white"], col)
        sphere("Truffe", H + Vector((0, -0.49, -0.1)), (0.045, 0.04, 0.035), M["black"], col)
        # yeux
        for side in (-1, 1):
            sphere("Oeil", H + Vector((side * 0.12, -0.235, 0.06)), (0.04, 0.02, 0.055), M["black"], col,
                   rot=(0, 0, side * -0.4))
            sphere("Sourcil", H + Vector((side * 0.13, -0.235, 0.14)), (0.06, 0.015, 0.012), M["black"], col,
                   rot=(0, side * -0.2, 0))
        # oreilles
        for side in (-1, 1):
            base = H + Vector((side * 0.17, 0.04, 0.17))
            tip = H + Vector((side * 0.33, 0.06, 0.55))
            ear = cylinder("Oreille", 0.12, 0.012, 1.0, M["fox"], col, seg=24)
            place_between(ear, base, tip)
            ear.scale = (1.0, 0.55, (tip - base).length)
            inner = cylinder("Oreille_Int", 0.075, 0.008, 1.0, M["fox_white"], col, seg=24)
            place_between(inner, base + Vector((0, -0.05, 0.02)), tip + Vector((0, -0.04, -0.07)))
            inner.scale = (1.0, 0.35, (tip - base).length * 0.85)
            etip = cylinder("Pointe_Oreille", 0.045, 0.006, 0.12, M["black"], col, seg=24)
            place_between(etip, tip.lerp(base, 0.22), tip + (tip - base).normalized() * 0.005)
            etip.scale = (1.0, 0.55, 1.0)
        # Calot de groom (rouge, galon or, monogramme)
        cap_c = H + Vector((0.02, 0.02, 0.3))
        cap = cylinder("Calot", 0.19, 0.18, 0.2, M["jacket"], col, seg=48)
        cap.location = cap_c
        cap.rotation_euler = (0.1, 0.18, 0)
        band = torus("Galon_Calot", 0.19, 0.02, M["gold"], col, seg=48, rseg=8)
        band.location = cap_c + Vector((0, 0, -0.06))
        band.rotation_euler = cap.rotation_euler
        rim = torus("Bord_Calot", 0.18, 0.012, M["gold"], col, seg=48, rseg=8)
        rim.location = cap_c + Vector((-0.018, -0.01, 0.1))
        rim.rotation_euler = cap.rotation_euler
        mono = text_obj("Monogramme", "MR", 0.11, M["gold"], self.font, col, extrude=0.006)
        mono.location = cap_c + Vector((0.0, -0.2, 0.0))
        mono.rotation_euler = (math.pi / 2 + 0.1, 0.0, 0.0)
        # Petite moustache-jouet comme le casse-noisette ? Non : des moustaches de renard
        for side in (-1, 1):
            for k in range(3):
                limb("Vibrisse", H + Vector((side * 0.06, -0.42, -0.1)),
                     H + Vector((side * 0.3, -0.4 + k * 0.03, -0.14 + k * 0.05)), 0.004, 0.002, M["black"], col)

        # --- Queue touffue ---
        cu = bpy.data.curves.new("Queue", "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth = 0.2
        cu.bevel_resolution = 6
        cu.use_fill_caps = True
        sp = cu.splines.new("BEZIER")
        pts = [((fx - 0.15, fy + 0.25, zf + 1.0), 0.35),
               ((fx - 0.5, fy + 0.35, zf + 0.8), 1.0),
               ((fx - 0.82, fy + 0.25, zf + 1.0), 1.05),
               ((fx - 0.92, fy + 0.1, zf + 1.42), 0.6)]
        sp.bezier_points.add(len(pts) - 1)
        for bp, (co, rad) in zip(sp.bezier_points, pts):
            bp.co = co
            bp.radius = rad
            bp.handle_left_type = bp.handle_right_type = "AUTO"
        cu.materials.append(M["fox"])
        link(bpy.data.objects.new("Queue", cu), col)
        tipdir = (Vector(pts[-1][0]) - Vector(pts[-2][0])).normalized()
        tip = sphere("Bout_Queue", Vector(pts[-1][0]) + tipdir * 0.04, (0.125, 0.125, 0.19), M["fox_white"], col)
        tip.rotation_mode = "QUATERNION"
        tip.rotation_quaternion = tipdir.to_track_quat("Z", "Y")

        self.star_pos = star_pos

    # ---------------- lumière & caméra ----------------
    def area(self, name, loc, target, energy, size, color=(1, 1, 1), size_y=None):
        li = bpy.data.lights.new(name, "AREA")
        li.energy = energy
        li.color = color
        if size_y:
            li.shape = "RECTANGLE"
            li.size, li.size_y = size, size_y
        else:
            li.size = size
        ob = link(bpy.data.objects.new(name, li), self.cols["Lumieres"])
        ob.location = loc
        ob.rotation_mode = "QUATERNION"
        ob.rotation_quaternion = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y")
        return ob

    def build_lights_camera(self, preview):
        # Grande lumière douce de face (vitrine), légèrement chaude
        self.area("Key_Face", (-3.5, -9.0, 7.5), (0.2, 0, 2.5), 1000, 7, (1.0, 0.93, 0.86))
        # Contre-plongée de remplissage droite
        self.area("Fill_Droite", (7.0, -6.0, 2.5), (0.5, 0, 2.0), 200, 6, (1.0, 0.82, 0.82))
        # Douche douce au-dessus
        self.area("Top", (0.3, -1.5, 10.0), (0.3, 0, 0), 250, 6, (1.0, 0.9, 0.85))
        # Rasant sur le mur pour le dégradé
        self.area("Mur_Wash", (0.0, -1.0, 0.2), (0.0, 2.8, 6.0), 80, 8, (1.0, 0.45, 0.45), size_y=1.0)
        # Lueur de l'étoile
        li = bpy.data.lights.new("Lueur_Etoile", "POINT")
        li.energy = 40
        li.color = (1.0, 0.75, 0.4)
        li.shadow_soft_size = 0.1
        ob = link(bpy.data.objects.new("Lueur_Etoile", li), self.cols["Lumieres"])
        ob.location = self.star_pos + Vector((0, -0.45, 0.1))

        world = bpy.data.worlds.new("Monde")
        world.use_nodes = True
        bg = world.node_tree.nodes.get("Background")
        bg.inputs["Color"].default_value = (0.35, 0.05, 0.06, 1)
        bg.inputs["Strength"].default_value = 0.12
        bpy.context.scene.world = world

        cam_data = bpy.data.cameras.new("Camera")
        cam_data.lens = 50
        cam_data.dof.use_dof = True
        cam_data.dof.aperture_fstop = 8.0
        cam = link(bpy.data.objects.new("Camera", cam_data))
        cam.location = (0.15, -12.2, 3.3)
        target = Vector((0.15, 0.0, 3.05))
        cam.rotation_mode = "QUATERNION"
        cam.rotation_quaternion = (target - Vector(cam.location)).to_track_quat("-Z", "Y")
        cam_data.dof.focus_distance = (Vector((0, -0.5, 2.5)) - Vector(cam.location)).length

        sc = bpy.context.scene
        sc.camera = cam
        sc.render.engine = "CYCLES"
        sc.render.resolution_x = 1080
        sc.render.resolution_y = 1350
        sc.render.resolution_percentage = 50 if preview else 100
        sc.cycles.samples = 64 if preview else 384
        sc.cycles.use_denoising = True
        sc.cycles.max_bounces = 8
        try:
            prefs = bpy.context.preferences.addons["cycles"].preferences
            for dev in ("OPTIX", "CUDA", "HIP", "METAL", "ONEAPI"):
                try:
                    prefs.compute_device_type = dev
                    prefs.get_devices()
                    if any(d.type == dev for d in prefs.devices):
                        for d in prefs.devices:
                            d.use = True
                        sc.cycles.device = "GPU"
                        break
                except (TypeError, ValueError):
                    continue
        except KeyError:
            pass
        vs = sc.view_settings
        for vt in ("AgX", "Filmic"):
            try:
                vs.view_transform = vt
                break
            except TypeError:
                continue
        for look in ("AgX - Punchy", "AgX - Medium High Contrast", "Medium High Contrast"):
            try:
                vs.look = look
                break
            except TypeError:
                continue
        vs.exposure = 0.0


def main():
    opts = parse_args()
    s = Scene()
    s.build_room()
    s.build_city()
    s.build_pile()
    s.build_decorations()
    s.build_fox()
    s.build_lights_camera(opts["preview"])
    bpy.context.scene.frame_set(1)
    if opts["blend"]:
        bpy.ops.wm.save_as_mainfile(filepath=opts["blend"])
        print("Fichier sauvegardé :", opts["blend"])
    if opts["render"]:
        bpy.context.scene.render.filepath = opts["render"]
        bpy.ops.render.render(write_still=True)
        print("Rendu :", opts["render"])


if __name__ == "__main__":
    main()
