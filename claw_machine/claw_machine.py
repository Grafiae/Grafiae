"""
Claw Machine de Noël — "la pince qui pêche un chèque-cadeau"
==================================================================

Script Blender (4.2+ / 5.x) qui construit TOUTE la scène de façon procédurale :
  - borne d'arcade vert bouteille laquée : vitrine, néons sur les arêtes avant,
    fronton lumineux, pupitre (joystick, bouton, monnayeur), portes, roulettes
  - pince chromée (corps, 3 griffes articulées, fil rouge, câble spiralé noir, chariot)
  - pile de cadeaux de Noël (papiers à motifs, rubans, nœuds, boules, bougies,
    sucres d'orge), posés par simulation physique (rigid body)
  - un chèque-cadeau recto/verso (textures/cheque_*.png), que la pince va chercher
  - entrée d'hôtel façon photo de référence : façade sombre en bois, grande porte double
    blanche ouverte, imposte, seuil surélevé, tapis rouge, pièce sombre derrière,
    soleil rasant ; matières réalistes (usure, grain, fibres) et halo sur les néons
  - animation : la caméra part d'un plan large et zoome vers la pince pendant
    qu'elle descend, pince le chèque-cadeau et remonte

Utilisation
-----------
  * Dans Blender : onglet "Scripting" > Open > claw_machine.py > Run Script
  * En ligne de commande (sauvegarde claw_machine.blend à côté du script) :
        blender -b -P claw_machine.py
    puis rendu :
        blender -b claw_machine.blend -a

Tous les réglages utiles sont dans la section PARAMÈTRES ci-dessous.
"""

import math
import os
import random

import bpy
import bmesh
from mathutils import Euler, Matrix, Vector

# ---------------------------------------------------------------------------
# PARAMÈTRES
# ---------------------------------------------------------------------------
SEED = 7                    # change la disposition / les couleurs des cadeaux
N_GIFTS = 56                # boîtes cadeaux emballées
N_BALLS = 16                # boules de Noël
N_JARS = 6                  # bougies de Noël en céramique avec couvercle
N_CANES = 8                 # sucres d'orge
FAIRY_LIGHTS = True         # guirlande lumineuse au fond de la vitrine (bokeh chaud)
FRONT_GLASS = True          # vitre devant la caméra (reflets en plus, rendu plus long)

MACHINE_GREEN = (0.004, 0.05, 0.022)   # laque vert bouteille de la borne
NEON_COLOR = (0.06, 1.0, 0.3)          # néons des arêtes avant
NEON_STRENGTH = 14.0
MARQUEE_TEXT = "LE RENARD"             # enseigne lumineuse du fronton
BASE_H = 0.88                          # hauteur du meuble bas (sol de la pièce à z = -BASE_H)

RES_X, RES_Y = 1080, 1440   # format 3:4 (comme la référence)
FPS = 24
FRAME_END = 192             # 8 s
SAMPLES = 256               # échantillons Cycles pour le rendu final
USE_GPU = True

CAB_W, CAB_D, CAB_H = 0.72, 0.60, 0.80   # volume vitré intérieur (m)   # dimensions intérieures de la vitrine (m)
CARD_SIZE = (0.105, 0.0012, 0.159)      # chèque-cadeau (proportions du visuel 895x1356)
CARD_CORNER = 0.0045                    # rayon des coins arrondis
CARD_XY = (0.02, -0.07)                 # position du chèque-cadeau dans la pile

random.seed(SEED)

# ---------------------------------------------------------------------------
# OUTILS
# ---------------------------------------------------------------------------


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    return scene


def link(obj, coll=None):
    (coll or bpy.context.scene.collection).objects.link(obj)
    return obj


def new_collection(name):
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    return coll


def move_to(obj, coll):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    coll.objects.link(obj)
    for child in obj.children:
        move_to(child, coll)


def smooth(obj):
    for p in obj.data.polygons:
        p.use_smooth = True


def add_bevel(obj, width, segments=3, harden=True):
    mod = obj.modifiers.new("Bevel", 'BEVEL')
    mod.width = width
    mod.segments = segments
    mod.limit_method = 'ANGLE'
    try:
        mod.harden_normals = harden
    except AttributeError:
        pass
    smooth(obj)
    return mod


def box(name, size, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, bevel=None, coll=None):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    bm.to_mesh(mesh)
    bm.free()
    obj = link(bpy.data.objects.new(name, mesh), coll)
    obj.location = loc
    obj.rotation_euler = rot
    if mat:
        obj.data.materials.append(mat)
    if bevel:
        add_bevel(obj, bevel)
    return obj


def cylinder(name, radius, depth, loc=(0, 0, 0), rot=(0, 0, 0), mat=None,
             verts=48, bevel=None, coll=None):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts,
                          radius1=radius, radius2=radius, depth=depth)
    bm.to_mesh(mesh)
    bm.free()
    obj = link(bpy.data.objects.new(name, mesh), coll)
    obj.location = loc
    obj.rotation_euler = rot
    if mat:
        obj.data.materials.append(mat)
    if bevel:
        add_bevel(obj, bevel, harden=True)
    else:
        smooth(obj)
    return obj


def sphere(name, radius, loc=(0, 0, 0), mat=None, coll=None, scale=(1, 1, 1)):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=radius)
    bm.to_mesh(mesh)
    bm.free()
    obj = link(bpy.data.objects.new(name, mesh), coll)
    obj.location = loc
    obj.scale = scale
    if mat:
        obj.data.materials.append(mat)
    smooth(obj)
    return obj


def torus(name, major, minor, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1),
          mat=None, coll=None):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    seg_u, seg_v = 48, 16
    grid = []
    for i in range(seg_u):
        u = 2 * math.pi * i / seg_u
        ring = []
        for j in range(seg_v):
            v = 2 * math.pi * j / seg_v
            r = major + minor * math.cos(v)
            ring.append(bm.verts.new((r * math.cos(u), r * math.sin(u), minor * math.sin(v))))
        grid.append(ring)
    for i in range(seg_u):
        for j in range(seg_v):
            bm.faces.new((grid[i][j], grid[(i + 1) % seg_u][j],
                          grid[(i + 1) % seg_u][(j + 1) % seg_v], grid[i][(j + 1) % seg_v]))
    bm.to_mesh(mesh)
    bm.free()
    obj = link(bpy.data.objects.new(name, mesh), coll)
    obj.location, obj.rotation_euler, obj.scale = loc, rot, scale
    if mat:
        obj.data.materials.append(mat)
    smooth(obj)
    return obj


def curve_obj(name, points, radius, mat=None, kind='BEZIER', coll=None, resolution=12):
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = radius
    cu.bevel_resolution = 4
    cu.use_fill_caps = True
    cu.resolution_u = resolution
    if kind == 'BEZIER':
        sp = cu.splines.new('BEZIER')
        sp.bezier_points.add(len(points) - 1)
        for bp, p in zip(sp.bezier_points, points):
            bp.co = p
            bp.handle_left_type = bp.handle_right_type = 'AUTO'
    else:
        sp = cu.splines.new('POLY')
        sp.points.add(len(points) - 1)
        for pt, p in zip(sp.points, points):
            pt.co = (*p, 1.0)
    obj = link(bpy.data.objects.new(name, cu), coll)
    if mat:
        obj.data.materials.append(mat)
    return obj


def catmull_rom(points, samples=10):
    pts = [Vector(p) for p in points]
    pts = [pts[0] * 2 - pts[1]] + pts + [pts[-1] * 2 - pts[-2]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1:i + 3]
        for k in range(samples):
            t = k / samples
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(pts[-2])
    return out


def strip_obj(name, points, width, thick, mat=None, coll=None, taper=0.75):
    """Lame plate balayée le long d'un chemin du plan YZ (largeur selon X)."""
    path = catmull_rom(points)
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rings = []
    for i, p in enumerate(path):
        tan = (path[min(i + 1, len(path) - 1)] - path[max(i - 1, 0)]).normalized()
        nrm = Vector((1, 0, 0)).cross(tan).normalized()
        w = width * (1 - (1 - taper) * i / (len(path) - 1)) / 2
        t = thick / 2
        rings.append([bm.verts.new(p + Vector((sx * w, 0, 0)) + nrm * sn * t)
                      for sx, sn in ((-1, -1), (1, -1), (1, 1), (-1, 1))])
    for a, b in zip(rings, rings[1:]):
        for k in range(4):
            bm.faces.new((a[k], a[(k + 1) % 4], b[(k + 1) % 4], b[k]))
    bm.faces.new(rings[0][::-1])
    bm.faces.new(rings[-1])
    bm.to_mesh(mesh)
    bm.free()
    obj = link(bpy.data.objects.new(name, mesh), coll)
    if mat:
        obj.data.materials.append(mat)
    add_bevel(obj, thick * 0.3, segments=2)
    return obj


def empty(name, loc=(0, 0, 0), coll=None, size=0.02):
    obj = link(bpy.data.objects.new(name, None), coll)
    obj.empty_display_size = size
    obj.location = loc
    return obj


def parent(child, par):
    child.parent = par
    child.matrix_parent_inverse = Matrix.Identity(4)


# ---------------------------------------------------------------------------
# MATÉRIAUX
# ---------------------------------------------------------------------------


def set_in(node, name, value):
    if name in node.inputs:
        node.inputs[name].default_value = value


def new_mat(name, color=(0.8, 0.8, 0.8), rough=0.5, metal=0.0, **extra):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    set_in(bsdf, "Base Color", (*color, 1.0))
    set_in(bsdf, "Roughness", rough)
    set_in(bsdf, "Metallic", metal)
    for key, val in extra.items():
        set_in(bsdf, key.replace("_", " "), val)
    return mat


def bsdf_of(mat):
    return mat.node_tree.nodes["Principled BSDF"]


def add_bump(mat, scale=400.0, strength=0.08, detail=8.0):
    """Micro-relief (grain du papier, fibres) via un bruit procédural."""
    nt = mat.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = scale
    noise.inputs["Detail"].default_value = detail
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = strength
    bump.inputs["Distance"].default_value = 0.0005
    nt.links.new(tc.outputs["Object"], noise.inputs["Vector"])
    nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf_of(mat).inputs["Normal"])


def add_rough_variation(mat, lo, hi, scale=8.0):
    """Variation de rugosité (traces, usure, poussière) pour casser l'aspect 'CG'."""
    nt = mat.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = scale
    noise.inputs["Detail"].default_value = 6.0
    nt.links.new(tc.outputs["Object"], noise.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = 0.35
    mr.inputs["From Max"].default_value = 0.65
    mr.inputs["To Min"].default_value = lo
    mr.inputs["To Max"].default_value = hi
    nt.links.new(noise.outputs["Fac"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], bsdf_of(mat).inputs["Roughness"])


def add_crinkle(mat, scale=60.0, strength=0.25):
    """Papier légèrement froissé : relief de Voronoi + bruit fin."""
    nt = mat.node_tree
    bsdf = bsdf_of(mat)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.feature = 'F1'
    vor.inputs["Scale"].default_value = scale
    nt.links.new(tc.outputs["Object"], vor.inputs["Vector"])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = strength
    bump.inputs["Distance"].default_value = 0.0008
    nt.links.new(vor.outputs["Distance"], bump.inputs["Height"])
    prev = bsdf.inputs["Normal"].links[0].from_socket if bsdf.inputs["Normal"].links else None
    if prev is not None:
        nt.links.new(prev, bump.inputs["Normal"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])


def wood_mat(name, c1, c2, rough=0.4, scale=(2.0, 2.0, 30.0), coat=0.3):
    """Bois veiné procédural (veines étirées le long de Z local)."""
    mat = new_mat(name, c1, rough, Coat_Weight=coat, Coat_Roughness=0.2)
    nt = mat.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = scale
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    wave = nt.nodes.new("ShaderNodeTexWave")
    wave.wave_type = 'RINGS'
    wave.inputs["Scale"].default_value = 3.0
    wave.inputs["Distortion"].default_value = 8.0
    wave.inputs["Detail"].default_value = 4.0
    nt.links.new(mp.outputs["Vector"], wave.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*c1, 1)
    ramp.color_ramp.elements[1].color = (*c2, 1)
    nt.links.new(wave.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf_of(mat).inputs["Base Color"])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.05
    nt.links.new(wave.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf_of(mat).inputs["Normal"])
    return mat


def ramp_colors(nt, colors, threshold_positions=None):
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.interpolation = 'CONSTANT'
    n = len(colors)
    positions = threshold_positions or [i / n for i in range(n)]
    while len(cr.elements) < n:
        cr.elements.new(0.5)
    for el, pos, col in zip(cr.elements, positions, colors):
        el.position = pos
        el.color = (*col, 1.0)
    return ramp


def pattern_mat(name, colors, pattern, scale=20.0, rough=0.45, coat=0.0):
    """Papier cadeau / céramique à motifs : stripes, dstripes, dots, harlequin, solid."""
    mat = new_mat(name, colors[0], rough, Coat_Weight=coat, Coat_Roughness=0.05)
    nt = mat.node_tree
    bsdf = bsdf_of(mat)
    if pattern == 'solid':
        return mat
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mapping = nt.nodes.new("ShaderNodeMapping")
    nt.links.new(tc.outputs["Object"], mapping.inputs["Vector"])
    mapping.inputs["Scale"].default_value = (scale, scale, scale)

    if pattern in ('stripes', 'dstripes'):
        tex = nt.nodes.new("ShaderNodeTexWave")
        tex.wave_type = 'BANDS'
        tex.bands_direction = 'DIAGONAL' if pattern == 'dstripes' else 'X'
        tex.inputs["Scale"].default_value = 1.0
        tex.inputs["Distortion"].default_value = 0.0
        fac = tex.outputs["Fac"]
        ramp = ramp_colors(nt, colors)
    elif pattern == 'dots':
        tex = nt.nodes.new("ShaderNodeTexVoronoi")
        tex.feature = 'F1'
        tex.inputs["Scale"].default_value = 1.0
        if "Randomness" in tex.inputs:
            tex.inputs["Randomness"].default_value = 0.0
        fac = tex.outputs["Distance"]
        ramp = ramp_colors(nt, [colors[1], colors[0]], [0.0, 0.28])
    elif pattern == 'harlequin':
        mapping.inputs["Rotation"].default_value = (math.radians(35), math.radians(45), math.radians(45))
        mapping.inputs["Scale"].default_value = (scale, scale * 0.6, scale)
        tex = nt.nodes.new("ShaderNodeTexChecker")
        tex.inputs["Scale"].default_value = 1.0
        fac = tex.outputs["Fac"]
        ramp = ramp_colors(nt, colors[:2], [0.0, 0.5])
    else:
        raise ValueError(pattern)

    nt.links.new(mapping.outputs["Vector"], tex.inputs["Vector"])
    nt.links.new(fac, ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    return mat


def emission_mix_mat(name, color, strength):
    """Fond blanc rétro-éclairé (diffus + légère émission), comme une vitrine de studio."""
    mat = new_mat(name, color, 0.6)
    bsdf = bsdf_of(mat)
    set_in(bsdf, "Emission Color", (*color, 1.0))
    set_in(bsdf, "Emission Strength", strength)
    return mat


def build_materials():
    M = {}
    M['chrome'] = new_mat("Chrome", (0.92, 0.92, 0.93), 0.06, 1.0)
    add_rough_variation(M['chrome'], 0.04, 0.14, 30.0)
    M['chrome_dark'] = new_mat("ChromeDark", (0.6, 0.6, 0.62), 0.12, 1.0)
    M['alu'] = new_mat("BrushedAlu", (0.78, 0.79, 0.8), 0.28, 1.0, Anisotropic=0.7)
    M['glass'] = new_mat("Glass", (1, 1, 1), 0.0, 0.0, IOR=1.2, Transmission_Weight=1.0)
    add_rough_variation(M['glass'], 0.0, 0.06, 4.0)   # traces de doigts / poussière
    M['paint'] = new_mat("BottleGreenLacquer", MACHINE_GREEN, 0.22, Coat_Weight=0.8, Coat_Roughness=0.04)
    add_bump(M['paint'], 900, 0.015)          # peau d'orange de la laque
    add_rough_variation(M['paint'], 0.16, 0.34, 6.0)
    M['paint_inner'] = new_mat("BottleGreenInner", MACHINE_GREEN, 0.35, Coat_Weight=0.4)
    M['cream'] = new_mat("CreamEnamel", (0.85, 0.78, 0.64), 0.3, Coat_Weight=0.5)
    M['neon'] = emission_mix_mat("NeonGreen", NEON_COLOR, NEON_STRENGTH)
    M['letters'] = emission_mix_mat("MarqueeLetters", (0.95, 0.88, 0.74), 1.2)
    M['ceiling'] = emission_mix_mat("CeilingLightBox", (1.0, 0.9, 0.76), 1.0)
    M['rubber'] = new_mat("BlackRubberMatte", (0.02, 0.02, 0.02), 0.7)
    M['slot'] = new_mat("CoinSlotBlack", (0.005, 0.005, 0.005), 0.5)
    M['joy_ball'] = new_mat("JoystickBall", (0.6, 0.01, 0.02), 0.12, Coat_Weight=1.0)
    M['brass'] = new_mat("Brass", (0.8, 0.58, 0.3), 0.3, 1.0)
    M['card'] = emission_mix_mat("ReflectCard", (1, 1, 1), 3.0)
    M['string'] = new_mat("RedString", (0.6, 0.02, 0.02), 0.5)
    add_bump(M['string'], 2000, 0.3)
    M['cable'] = new_mat("BlackRubber", (0.012, 0.012, 0.014), 0.42)

    paper = new_mat("LabelPaper", (0.96, 0.89, 0.76), 0.72, Sheen_Weight=0.1)
    set_in(bsdf_of(paper), "Subsurface Weight", 0.08)
    set_in(bsdf_of(paper), "Subsurface Radius", (0.002, 0.0015, 0.001))
    add_bump(paper, 900, 0.12)
    M['paper'] = paper

    # Palette de Noël : rouge profond, vert sapin, or, crème, kraft, blanc neige.
    pal = {
        'red': (0.55, 0.015, 0.025), 'scarlet': (0.75, 0.04, 0.03), 'fir': (0.01, 0.16, 0.07),
        'emerald': (0.02, 0.3, 0.14), 'gold': (0.8, 0.56, 0.2), 'cream': (0.9, 0.84, 0.7),
        'kraft': (0.55, 0.36, 0.2), 'snow': (0.93, 0.93, 0.92), 'night': (0.02, 0.04, 0.12),
        'burgundy': (0.28, 0.01, 0.03), 'black': (0.02, 0.02, 0.02),
    }
    M['pal'] = pal
    combos = [
        (['snow', 'red'], 'stripes', 26), (['red', 'snow'], 'dots', 26),
        (['fir', 'gold'], 'dots', 30), (['kraft'], 'solid', 0),
        (['cream', 'fir'], 'dstripes', 24), (['scarlet'], 'solid', 0),
        (['snow', 'emerald', 'red'], 'stripes', 18), (['emerald'], 'solid', 0),
        (['night', 'gold'], 'dots', 34), (['red', 'fir'], 'harlequin', 10),
        (['burgundy'], 'solid', 0), (['kraft', 'snow'], 'dots', 30),
        (['snow'], 'solid', 0), (['cream', 'red'], 'dstripes', 30),
    ]
    M['wraps'] = [pattern_mat(f"Wrap_{i:02d}", [pal[c] for c in cols], pat, sc,
                              rough=random.uniform(0.35, 0.6))
                  for i, (cols, pat, sc) in enumerate(combos)]
    for m in M['wraps']:
        add_bump(m, 600, 0.05)
        add_crinkle(m, random.uniform(30, 70), 0.3)
    M['ribbons'] = [
        new_mat("RibbonGold", (0.9, 0.68, 0.32), 0.25, 1.0),
        new_mat("RibbonRedSatin", (0.55, 0.01, 0.03), 0.28, Sheen_Weight=0.6),
        new_mat("RibbonWhiteSatin", (0.9, 0.9, 0.88), 0.3, Sheen_Weight=0.6),
        new_mat("RibbonGreenVelvet", (0.01, 0.12, 0.05), 0.5, Sheen_Weight=1.0),
        new_mat("RibbonSilver", (0.85, 0.85, 0.86), 0.22, 1.0),
    ]
    # Boules de Noël : verre laqué brillant, métallisé ou satiné
    M['bauble'] = [
        new_mat("Bauble_Red", pal['scarlet'], 0.08, Coat_Weight=1.0, Coat_Roughness=0.02),
        new_mat("Bauble_Gold", (0.95, 0.7, 0.3), 0.12, 1.0),
        new_mat("Bauble_Green", pal['emerald'], 0.1, Coat_Weight=1.0, Coat_Roughness=0.02),
        new_mat("Bauble_Silver", (0.9, 0.9, 0.92), 0.05, 1.0),
        new_mat("Bauble_SatinRed", pal['red'], 0.35, 0.6),
        new_mat("Bauble_Snow", pal['snow'], 0.4, Sheen_Weight=0.8),
    ]
    M['ceramic'] = [pattern_mat(f"Ceramic_{i}", [pal[a], pal[b]], pat, sc, rough=0.3, coat=1.0)
                    for i, (a, b, pat, sc) in enumerate([
                        ('snow', 'red', 'dots', 32), ('red', 'snow', 'stripes', 40),
                        ('fir', 'gold', 'dots', 34), ('cream', 'fir', 'dstripes', 36),
                        ('burgundy', 'gold', 'stripes', 30), ('snow', 'emerald', 'harlequin', 12)])]
    M['candycane'] = pattern_mat("CandyCane", [(0.93, 0.92, 0.9), (0.7, 0.01, 0.02)], 'dstripes', 70,
                                 rough=0.2, coat=1.0)
    M['bulb'] = emission_mix_mat("FairyBulb", (1.0, 0.62, 0.25), 25.0)
    M['wire'] = new_mat("FairyWire", (0.02, 0.05, 0.02), 0.4)
    M['gold'] = new_mat("Gold", (0.95, 0.72, 0.36), 0.2, 1.0)
    return M


# ---------------------------------------------------------------------------
# BORNE D'ARCADE (vitrine + meuble + fronton)
# ---------------------------------------------------------------------------
POST = 0.05
OUT_W, OUT_D = CAB_W + 2 * POST, CAB_D + 2 * POST
FLOOR_Z = -BASE_H
MARQUEE_H = 0.27


def panel_frame(name, w, h, loc, depth, mat, coll, bar=0.022):
    """Cadre en relief (moulure) dans le plan XZ, posé devant une face orientée -Y."""
    x, y, z = loc
    parts = [((w, depth, bar), (x, y, z + h / 2 - bar / 2)), ((w, depth, bar), (x, y, z - h / 2 + bar / 2)),
             ((bar, depth, h), (x - w / 2 + bar / 2, y, z)), ((bar, depth, h), (x + w / 2 - bar / 2, y, z))]
    return [box(f"{name}_{k}", size, l, mat=mat, bevel=min(depth, bar) * 0.3, coll=coll)
            for k, (size, l) in enumerate(parts)]


def build_cabinet(M):
    coll = new_collection("ClawMachine")
    w, d, h, t = CAB_W, CAB_D, CAB_H, 0.008
    colliders = []
    paint = M['paint']

    # --- Volume de jeu (vitrine)
    colliders.append(box("PlayFloor", (w, d, 0.04), (0, 0, -0.02), mat=M['paint_inner'], coll=coll))
    colliders.append(box("BackPanel", (w, t, h), (0, d / 2 + t / 2, h / 2), mat=M['paint_inner'], coll=coll))
    box("CeilingLightBox", (w, d, 0.01), (0, 0, h + 0.005), mat=M['ceiling'], coll=coll)
    for sx in (-1, 1):
        colliders.append(box(f"GlassSide_{'L' if sx < 0 else 'R'}", (t, d, h),
                             (sx * (w / 2 + t / 2), 0, h / 2), mat=M['glass'], coll=coll))
    front = box("GlassFront", (w, t, h), (0, -d / 2 - t / 2, h / 2), mat=M['glass'], coll=coll)
    colliders.append(front)
    if not FRONT_GLASS:
        front.hide_render = True
    # Rebord crème devant la vitre (comme la tablette de la référence)
    box("FrontLedge", (w + 0.02, 0.07, 0.025), (0, -d / 2 - 0.03, 0.0), mat=M['cream'], bevel=0.004, coll=coll)

    # --- Montants laqués + néons sur les arêtes avant
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f"Post_{sx}_{sy}", (POST, POST, h + 0.02),
                (sx * (w / 2 + POST / 2), sy * (d / 2 + POST / 2), h / 2), mat=paint, bevel=0.004, coll=coll)
        neon_h = h + BASE_H - 0.1
        neon = box(f"Neon_{sx}", (0.02, 0.02, neon_h),
                   (sx * (OUT_W / 2 + 0.003), -OUT_D / 2 - 0.003, FLOOR_Z + 0.08 + neon_h / 2),
                   mat=M['neon'], bevel=0.004, coll=coll)
        neon.visible_shadow = False

    # --- Fronton (enseigne)
    box("Marquee", (OUT_W + 0.02, OUT_D + 0.02, MARQUEE_H), (0, 0, h + MARQUEE_H / 2),
        mat=paint, bevel=0.006, coll=coll)
    box("MarqueeLip", (OUT_W + 0.03, OUT_D + 0.03, 0.02), (0, 0, h + 0.01), mat=paint, bevel=0.004, coll=coll)
    cu = bpy.data.curves.new("MarqueeText", 'FONT')
    cu.body = MARQUEE_TEXT
    cu.align_x, cu.align_y = 'CENTER', 'CENTER'
    cu.size = 0.095
    cu.space_character = 1.45
    cu.extrude = 0.006
    cu.bevel_depth = 0.001
    txt = link(bpy.data.objects.new("MarqueeText", cu), coll)
    txt.data.materials.append(M['letters'])
    txt.location = (0, -OUT_D / 2 - 0.012, h + MARQUEE_H / 2 + 0.01)
    txt.rotation_euler = (math.radians(90), 0, 0)
    # Lumière douce de l'enseigne sur le haut de la vitre
    ld = bpy.data.lights.new("MarqueeGlow", 'AREA')
    ld.size, ld.energy, ld.color = 0.6, 6, (1.0, 0.9, 0.75)
    glow = link(bpy.data.objects.new("MarqueeGlow", ld), coll)
    glow.location = (0, -OUT_D / 2 - 0.05, h + MARQUEE_H / 2)
    glow.rotation_euler = (math.radians(90), 0, 0)

    # --- Meuble bas
    plinth = 0.07
    body_h = BASE_H - plinth
    box("BaseBody", (OUT_W, OUT_D, body_h), (0, 0, FLOOR_Z + plinth + body_h / 2), mat=paint, bevel=0.006, coll=coll)
    box("BasePlinth", (OUT_W - 0.04, OUT_D - 0.04, plinth), (0, 0, FLOOR_Z + plinth / 2), mat=M['slot'], coll=coll)
    fy = -OUT_D / 2 - 0.004
    for sx in (-1, 1):
        dx = sx * (OUT_W / 2 - 0.17)
        panel_frame(f"BaseDoor_{sx}", 0.24, 0.42, (dx, fy, FLOOR_Z + plinth + 0.3), 0.008, paint, coll)
        cylinder(f"DoorLock_{sx}", 0.008, 0.012, (dx, fy - 0.004, FLOOR_Z + plinth + 0.47),
                 (math.radians(90), 0, 0), mat=M['chrome'], coll=coll)
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = cylinder(f"Caster_{sx}_{sy}", 0.03, 0.022, (sx * (OUT_W / 2 - 0.08), sy * (OUT_D / 2 - 0.08),
                         FLOOR_Z + 0.03), (0, math.radians(90), 0), mat=M['rubber'], coll=coll)
            cylinder(f"CasterHub_{sx}_{sy}", 0.012, 0.026, c.location, c.rotation_euler, mat=M['chrome'], coll=coll)

    # --- Pupitre de commande (joystick, bouton, monnayeur)
    cw, cd_, ch = 0.26, 0.17, 0.5
    cz = 0.06 - ch / 2
    cy = -OUT_D / 2 - cd_ / 2 + 0.01
    box("ControlBox", (cw, cd_, ch), (0, cy, cz), mat=paint, bevel=0.006, coll=coll)
    box("ControlTop", (cw + 0.012, cd_ + 0.012, 0.018), (0, cy, 0.06), mat=M['cream'], bevel=0.004, coll=coll)
    box("ControlLower", (cw - 0.04, cd_ - 0.03, 0.2), (0, cy + 0.01, cz - ch / 2 - 0.1), mat=paint,
        bevel=0.005, coll=coll)
    for sx in (-1, 1):
        neon = box(f"ControlNeon_{sx}", (0.01, 0.01, ch), (sx * (cw / 2 + 0.002), cy - cd_ / 2 - 0.002, cz),
                   mat=M['neon'], bevel=0.003, coll=coll)
        neon.visible_shadow = False
    cylinder("JoystickBase", 0.022, 0.008, (-0.05, cy, 0.073), mat=M['chrome'], coll=coll)
    cylinder("JoystickShaft", 0.005, 0.075, (-0.05, cy, 0.11), mat=M['chrome'], coll=coll)
    sphere("JoystickBall", 0.019, (-0.05, cy, 0.152), M['joy_ball'], coll)
    cylinder("Button", 0.022, 0.014, (0.06, cy, 0.075), mat=M['cream'], bevel=0.005, coll=coll)
    plate_y = cy - cd_ / 2 - 0.003
    box("CoinPlate", (0.06, 0.006, 0.11), (0, plate_y, cz + 0.08), mat=M['chrome'], bevel=0.002, coll=coll)
    box("CoinSlot", (0.004, 0.004, 0.035), (0, plate_y - 0.003, cz + 0.1), mat=M['slot'], coll=coll)
    box("CoinReturn", (0.03, 0.004, 0.02), (0, plate_y - 0.003, cz + 0.05), mat=M['slot'], coll=coll)
    panel_frame("ControlDoor", 0.16, 0.13, (0, plate_y + 0.001, cz - 0.1), 0.006, paint, coll, bar=0.016)

    # --- Portique du chariot sous le plafond
    for sy in (-1, 1):
        cylinder(f"GantryRail_{sy}", 0.006, w, (0, sy * (d / 2 - 0.04), h - 0.03),
                 (0, math.radians(90), 0), mat=M['chrome'], coll=coll)
    return coll, colliders


def build_gantry(M, rig):
    """Chariot + traverse qui suivent la pince en X/Y sous le plafond."""
    coll = bpy.data.collections["ClawMachine"]
    cross = cylinder("GantryCross", 0.008, CAB_D - 0.06, (0, 0, CAB_H - 0.03),
                     (math.radians(90), 0, 0), mat=M['chrome'], coll=coll)
    c = cross.constraints.new('COPY_LOCATION')
    c.target, c.use_y, c.use_z = rig, False, False
    carriage = box("GantryCarriage", (0.07, 0.06, 0.04), (0, 0, CAB_H - 0.045), mat=M['chrome_dark'],
                   bevel=0.004, coll=coll)
    c = carriage.constraints.new('COPY_LOCATION')
    c.target, c.use_z = rig, False


# ---------------------------------------------------------------------------
# PIÈCE D'HÔTEL
# ---------------------------------------------------------------------------


def parquet_mat():
    mat = new_mat("OakParquet", (0.3, 0.16, 0.07), 0.32, Coat_Weight=0.35, Coat_Roughness=0.15)
    nt = mat.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    brick = nt.nodes.new("ShaderNodeTexBrick")
    brick.offset = 0.5
    brick.inputs["Color1"].default_value = (0.36, 0.19, 0.08, 1)
    brick.inputs["Color2"].default_value = (0.22, 0.11, 0.045, 1)
    brick.inputs["Mortar"].default_value = (0.06, 0.03, 0.015, 1)
    brick.inputs["Scale"].default_value = 1.0
    brick.inputs["Mortar Size"].default_value = 0.0015
    brick.inputs["Brick Width"].default_value = 0.9
    brick.inputs["Row Height"].default_value = 0.13
    nt.links.new(tc.outputs["Object"], brick.inputs["Vector"])
    grain = nt.nodes.new("ShaderNodeTexNoise")
    grain.inputs["Scale"].default_value = 3.0
    grain.inputs["Detail"].default_value = 10.0
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.inputs["Scale"].default_value = (1.0, 40.0, 1.0)
    nt.links.new(tc.outputs["Object"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], grain.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMath")
    mix.operation = 'MULTIPLY'
    nt.links.new(brick.outputs["Fac"], mix.inputs[0])
    nt.links.new(grain.outputs["Fac"], mix.inputs[1])
    tint = nt.nodes.new("ShaderNodeHueSaturation")
    tint.inputs["Value"].default_value = 1.0
    nt.links.new(brick.outputs["Color"], tint.inputs["Color"])
    nt.links.new(grain.outputs["Fac"], tint.inputs["Fac"])
    nt.links.new(tint.outputs["Color"], bsdf_of(mat).inputs["Base Color"])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.15
    nt.links.new(brick.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf_of(mat).inputs["Normal"])
    return mat


# Encadrement de porte façon référence : la borne est posée dans l'ouverture d'une
# grande porte double, sur un seuil surélevé ; la pièce derrière reste dans le noir.
WALL_Y = -OUT_D / 2 - 0.24          # face avant de la façade
WALL_T = 0.32
OPEN_W, OPEN_H = 1.72, 2.7           # ouverture de la porte double
STEP_H, STEP_D = 0.15, 1.25         # seuil surélevé devant la porte
DOOR_OPEN = 100.0                   # angle d'ouverture des battants (°)


def stone_tiles_mat():
    mat = new_mat("LobbyStone", (0.42, 0.39, 0.34), 0.3)
    nt = mat.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    brick = nt.nodes.new("ShaderNodeTexBrick")
    brick.offset = 0.0
    brick.inputs["Color1"].default_value = (0.46, 0.43, 0.38, 1)
    brick.inputs["Color2"].default_value = (0.38, 0.35, 0.3, 1)
    brick.inputs["Mortar"].default_value = (0.2, 0.18, 0.16, 1)
    brick.inputs["Scale"].default_value = 1.0
    brick.inputs["Mortar Size"].default_value = 0.003
    brick.inputs["Brick Width"].default_value = 0.6
    brick.inputs["Row Height"].default_value = 0.6
    nt.links.new(tc.outputs["Object"], brick.inputs["Vector"])
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 6.0
    noise.inputs["Detail"].default_value = 12.0
    nt.links.new(tc.outputs["Object"], noise.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = 'RGBA'
    mix.blend_type = 'OVERLAY'
    mix.inputs[0].default_value = 0.35
    nt.links.new(brick.outputs["Color"], mix.inputs[6])
    nt.links.new(noise.outputs["Color"], mix.inputs[7])
    nt.links.new(mix.outputs[2], bsdf_of(mat).inputs["Base Color"])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.2
    nt.links.new(brick.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf_of(mat).inputs["Normal"])
    add_rough_variation(mat, 0.18, 0.5, 3.0)
    return mat


def carpet_mat():
    mat = new_mat("RedCarpet", (0.25, 0.006, 0.01), 0.95, Sheen_Weight=0.35, Sheen_Roughness=0.5,
                  Sheen_Tint=(1.0, 0.2, 0.2, 1.0))
    nt = mat.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    fib = nt.nodes.new("ShaderNodeTexNoise")
    fib.inputs["Scale"].default_value = 1800.0
    fib.inputs["Detail"].default_value = 2.0
    nt.links.new(tc.outputs["Object"], fib.inputs["Vector"])
    blot = nt.nodes.new("ShaderNodeTexNoise")
    blot.inputs["Scale"].default_value = 4.0
    nt.links.new(tc.outputs["Object"], blot.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (0.16, 0.004, 0.007, 1)
    ramp.color_ramp.elements[1].color = (0.3, 0.01, 0.014, 1)
    nt.links.new(blot.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf_of(mat).inputs["Base Color"])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.6
    bump.inputs["Distance"].default_value = 0.002
    nt.links.new(fib.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf_of(mat).inputs["Normal"])
    return mat


def build_carpet(mat, coll):
    """Tapis épais : posé sur le seuil, il épouse le nez de marche puis file vers la caméra."""
    w, th = 1.15, 0.012
    y_in = -OUT_D / 2 + 0.05
    y_edge = WALL_Y - STEP_D
    z_top, z_low = FLOOR_Z, FLOOR_Z - STEP_H
    prof = [(y_in, z_top)]
    prof += [(y_edge + 0.02 - 0.02 * math.sin(a), z_top - 0.02 + 0.02 * math.cos(a))
             for a in [math.radians(k * 15) for k in range(0, 7)]]
    prof += [(y_edge - 0.03, z_low + 0.03), (y_edge - 0.06, z_low), (y_edge - 6.0, z_low)]
    # densifie les segments longs pour la subdivision + displacement
    pts = []
    for (y0, z0), (y1, z1) in zip(prof, prof[1:]):
        n = max(1, int(abs(y1 - y0) / 0.05))
        pts += [(y0 + (y1 - y0) * k / n, z0 + (z1 - z0) * k / n) for k in range(n)]
    pts.append(prof[-1])
    mesh = bpy.data.meshes.new("RedCarpet")
    bm = bmesh.new()
    nx = 24
    grid = [[bm.verts.new((-w / 2 + w * i / nx, y, z + th)) for i in range(nx + 1)] for y, z in pts]
    for r0, r1 in zip(grid, grid[1:]):
        for i in range(nx):
            bm.faces.new((r0[i], r0[i + 1], r1[i + 1], r1[i]))
    bm.to_mesh(mesh)
    bm.free()
    obj = link(bpy.data.objects.new("RedCarpet", mesh), coll)
    obj.data.materials.append(mat)
    sol = obj.modifiers.new("Thickness", 'SOLIDIFY')
    sol.thickness = th
    sol.offset = -1
    tex = bpy.data.textures.new("CarpetWaves", 'CLOUDS')
    tex.noise_scale = 0.6
    disp = obj.modifiers.new("Ripples", 'DISPLACE')
    disp.texture = tex
    disp.strength = 0.006
    disp.direction = 'Z'
    smooth(obj)
    return obj


def build_door(name, hinge_x, sgn, M, coll):
    """Battant blanc mouluré, ouvert vers l'extérieur ; origine sur l'axe des charnières."""
    piv = empty(name, (hinge_x, WALL_Y - 0.04, FLOOR_Z), coll=coll, size=0.1)
    dw, dt, dh = OPEN_W / 2 - 0.02, 0.055, OPEN_H - 0.03
    paint = M['door_paint']
    leaf = box(f"{name}_Leaf", (dw, dt, dh), (sgn * (dw / 2 + 0.01), 0, dh / 2 + 0.005), mat=paint,
               bevel=0.004, coll=coll)
    parent(leaf, piv)
    parts = []
    for side in (-1, 1):
        y = side * (dt / 2 + 0.006)
        for zc, ph in ((0.55, 0.62), (1.72, 1.55)):
            parts += panel_frame(f"{name}_Panel_{side}_{zc}", dw - 0.2, ph, (sgn * (dw / 2 + 0.01), y, zc),
                                 0.014, paint, coll, bar=0.035)
        # Poignée-béquille chromée
        hx = sgn * (dw - 0.07)
        parts.append(cylinder(f"{name}_Rosette_{side}", 0.026, 0.01, (hx, y + side * 0.002, 1.02),
                              (math.radians(90), 0, 0), mat=M['chrome'], coll=coll))
        parts.append(curve_obj(f"{name}_Lever_{side}",
                               [(hx, y + side * 0.004, 1.02), (hx, y + side * 0.05, 1.02),
                                (hx - sgn * 0.11, y + side * 0.055, 1.015)], 0.008, mat=M['chrome'], coll=coll))
    for zc in (0.25, 1.35, 2.45):
        parts.append(cylinder(f"{name}_Hinge_{zc}", 0.011, 0.1, (0, 0, zc), mat=M['brass'], coll=coll))
    for p_ in parts:
        parent(p_, piv)
    piv.rotation_euler.z = math.radians(-sgn * DOOR_OPEN)
    return piv


def build_entrance(M):
    coll = new_collection("Entrance")
    facade = wood_mat("FacadeWalnut", (0.08, 0.045, 0.028), (0.13, 0.075, 0.045), 0.4, (1.5, 1.5, 12.0), 0.4)
    trim = wood_mat("FacadeTrim", (0.09, 0.05, 0.03), (0.15, 0.085, 0.05), 0.32, (1.5, 1.5, 12.0), 0.5)
    M['door_paint'] = new_mat("DoorPaint", (0.62, 0.6, 0.55), 0.45, Coat_Weight=0.15)
    add_rough_variation(M['door_paint'], 0.25, 0.5, 5.0)
    add_bump(M['door_paint'], 700, 0.02)
    dark = new_mat("InteriorDark", (0.03, 0.025, 0.02), 0.6)

    yc = WALL_Y + WALL_T / 2
    side_w = 3.0
    for sx in (-1, 1):
        box(f"Facade_{sx}", (side_w, WALL_T, 4.2), (sx * (OPEN_W / 2 + side_w / 2), yc, FLOOR_Z + 2.1 - STEP_H),
            mat=facade, coll=coll)
        # Pilastre + chambranle
        box(f"Pilaster_{sx}", (0.3, 0.07, 4.0), (sx * (OPEN_W / 2 + 0.36), WALL_Y - 0.035, FLOOR_Z + 2.0 - STEP_H),
            mat=trim, bevel=0.01, coll=coll)
        box(f"Casing_{sx}", (0.1, 0.05, OPEN_H + 0.1), (sx * (OPEN_W / 2 + 0.05), WALL_Y - 0.025,
            FLOOR_Z + (OPEN_H + 0.1) / 2), mat=trim, bevel=0.008, coll=coll)
        box(f"Reveal_{sx}", (0.02, WALL_T, OPEN_H), (sx * (OPEN_W / 2 + 0.01), yc, FLOOR_Z + OPEN_H / 2),
            mat=facade, coll=coll)
    lint_h = 4.2 - STEP_H - OPEN_H
    box("Lintel", (OPEN_W, WALL_T, lint_h), (0, yc, FLOOR_Z + OPEN_H + lint_h / 2), mat=facade, coll=coll)
    box("HeadCasing", (OPEN_W + 0.2, 0.06, 0.12), (0, WALL_Y - 0.03, FLOOR_Z + OPEN_H + 0.06), mat=trim,
        bevel=0.01, coll=coll)
    # Imposte vitrée au-dessus de la porte
    tz = FLOOR_Z + OPEN_H + 0.5
    box("TransomGlass", (OPEN_W - 0.1, 0.01, 0.6), (0, WALL_Y + 0.03, tz),
        mat=new_mat("TransomGlass", (0.02, 0.02, 0.02), 0.05, Coat_Weight=1.0), coll=coll)
    panel_frame("TransomFrame", OPEN_W, 0.74, (0, WALL_Y - 0.01, tz), 0.04, trim, coll, bar=0.07)

    # Seuil surélevé + sol du hall
    box("Threshold", (OPEN_W + 1.2, STEP_D, STEP_H), (0, WALL_Y - STEP_D / 2, FLOOR_Z - STEP_H / 2),
        mat=new_mat("ThresholdStone", (0.05, 0.045, 0.04), 0.35, Coat_Weight=0.2), bevel=0.01, coll=coll)
    lobby = box("LobbyFloor", (12, 14, 0.02), (0, WALL_Y - 7, FLOOR_Z - STEP_H - 0.01), mat=stone_tiles_mat(),
                coll=coll)
    lobby.name = "LobbyFloor"

    # Pièce sombre derrière
    box("InteriorFloor", (OPEN_W + 2, 3, 0.02), (0, WALL_Y + 1.5, FLOOR_Z - 0.01), mat=parquet_mat(), coll=coll)
    box("InteriorBack", (6, 0.05, 4), (0, 2.6, FLOOR_Z + 2), mat=dark, coll=coll)
    box("InteriorCeiling", (6, 4, 0.05), (0, 0.8, FLOOR_Z + OPEN_H + 0.3), mat=dark, coll=coll)
    for sx in (-1, 1):
        box(f"InteriorSide_{sx}", (0.05, 4, 4), (sx * 2.2, 0.8, FLOOR_Z + 2), mat=dark, coll=coll)

    # Portes ouvertes + bras de retenue
    for sx in (-1, 1):
        build_door(f"Door_{'L' if sx < 0 else 'R'}", sx * OPEN_W / 2, -sx, M, coll)
        a = math.radians(-(-sx) * DOOR_OPEN)
        ex = sx * OPEN_W / 2 + (-sx) * 0.75 * math.cos(a)
        ey = WALL_Y - 0.04 + (-sx) * 0.75 * math.sin(a)
        curve_obj(f"DoorStay_{sx}", [(ex, ey, FLOOR_Z + OPEN_H - 0.08),
                                     (sx * (OPEN_W / 2 - 0.5), WALL_Y - 0.01, FLOOR_Z + OPEN_H + 0.04)],
                  0.006, mat=M['chrome_dark'], kind='POLY', coll=coll)

    build_carpet(carpet_mat(), coll)
    return coll


# ---------------------------------------------------------------------------
# PINCE
# ---------------------------------------------------------------------------
PRONG_PHI = (0.0, 120.0, 240.0)      # 0° = griffe arrière (derrière la carte)
HINGE_R = 0.026
OPEN_ANGLE = math.radians(30)
CLOSED_ANGLE = math.radians(-1)
TIP_DROP = 0.17                      # hauteur entre l'axe des charnières et les pointes


def build_claw(M):
    coll = new_collection("Claw")
    rig = empty("Claw_Rig", coll=coll, size=0.06)
    c, cd = M['chrome'], M['chrome_dark']

    # Corps empilé (pièces tournées chromées)
    parts = [
        ("Flange", 0.031, 0.008, 0.004, cd), ("RingLow", 0.025, 0.006, 0.014, c),
        ("Body", 0.021, 0.062, 0.048, c), ("RingMid", 0.0235, 0.005, 0.032, c),
        ("RingHigh", 0.024, 0.007, 0.078, c), ("Cap", 0.016, 0.014, 0.088, c),
        ("Nut", 0.0085, 0.012, 0.1, cd),
    ]
    for name, r, dep, z, mat in parts:
        o = cylinder(f"Claw_{name}", r, dep, (0, 0, z), mat=mat, bevel=min(0.0015, dep / 4), coll=coll)
        parent(o, rig)
    spindle = cylinder("Claw_Spindle", 0.0035, 0.07, (0, 0, -0.035), mat=c, coll=coll)
    parent(spindle, rig)
    tipball = sphere("Claw_SpindleTip", 0.005, (0, 0, -0.07), mat=c, coll=coll)
    parent(tipball, rig)
    lug = cylinder("Claw_CableLug", 0.0055, 0.022, (0.029, 0, 0.06),
                   (0, math.radians(90), 0), mat=cd, coll=coll)
    parent(lug, rig)
    cable_attach = empty("Claw_CableAttach", (0.041, 0, 0.062), coll=coll, size=0.01)
    parent(cable_attach, rig)

    # Fil de levage rouge
    string = cylinder("Claw_String", 0.0011, 0.3, (0, 0, 0.106 + 0.15), mat=M['string'], verts=12, coll=coll)
    parent(string, rig)

    # Les 3 griffes : chaque charnière (empty) tourne autour de son axe X local.
    prong_path = [(0, 0.0, 0.0), (0, 0.022, -0.022), (0, 0.04, -0.07),
                  (0, 0.032, -0.12), (0, 0.006, -0.155), (0, -0.019, -TIP_DROP)]
    hinges = []
    for i, phi in enumerate(PRONG_PHI):
        a = math.radians(phi)
        hinge = empty(f"Claw_Hinge_{i}", (-HINGE_R * math.sin(a), HINGE_R * math.cos(a), 0.0),
                      coll=coll, size=0.015)
        hinge.rotation_euler = (CLOSED_ANGLE, 0, a)
        parent(hinge, rig)
        arm = strip_obj(f"Claw_Prong_{i}", prong_path, 0.011, 0.0035, mat=c, coll=coll)
        parent(arm, hinge)
        pad = sphere(f"Claw_ProngTip_{i}", 0.0042, prong_path[-1], mat=c, coll=coll, scale=(1.3, 1, 1))
        parent(pad, hinge)
        bracket = box(f"Claw_Bracket_{i}", (0.014, 0.012, 0.01), (0, -0.002, 0.0), mat=cd,
                      bevel=0.0015, coll=coll)
        parent(bracket, hinge)
        # Petite biellette entre le corps et la griffe (détail mécanique)
        link_rod = curve_obj(f"Claw_Link_{i}", [(0, -0.012, -0.03), (0, 0.03, -0.045)],
                             0.0014, mat=cd, coll=coll)
        parent(link_rod, hinge)
        hinges.append(hinge)
    return coll, rig, hinges, cable_attach


def build_cable(M, rig, cable_attach, coll):
    """Câble spiralé noir : ancré au plafond, s'étire jusqu'à la pince (Stretch To)."""
    top_z = CAB_H - 0.02
    start_len = top_z - (rig.location.z + cable_attach.location.z)
    turns_per_m = 190
    pts = []
    n = int(start_len * turns_per_m * 16)
    radius = 0.013
    for k in range(n + 1):
        t = k / n
        ang = 2 * math.pi * turns_per_m * start_len * t
        pts.append((radius * math.cos(ang), t * start_len, radius * math.sin(ang)))
    coil = curve_obj("Claw_Coil", pts, 0.0024, mat=M['cable'], kind='POLY', coll=coll, resolution=2)
    # Suit la pince en X/Y (enfant du rig) mais reste accroché au plafond en Z.
    parent(coil, rig)
    coil.location = (cable_attach.location.x, 0.0, start_len + cable_attach.location.z)
    lim = coil.constraints.new('LIMIT_LOCATION')
    lim.use_min_z = lim.use_max_z = True
    lim.min_z = lim.max_z = top_z
    lim.owner_space = 'WORLD'
    st = coil.constraints.new('STRETCH_TO')
    st.target = cable_attach
    st.volume = 'NO_VOLUME'
    st.rest_length = start_len
    st.keep_axis = 'PLANE_X'
    return coil


# ---------------------------------------------------------------------------
# CADEAUX
# ---------------------------------------------------------------------------


def gift_box(M, i, coll):
    sx, sy, sz = (random.uniform(0.06, 0.13) for _ in range(3))
    sz = min(sz, 0.11)
    wrap = random.choice(M['wraps'])
    g = box(f"Gift_{i:02d}", (sx, sy, sz), mat=wrap, bevel=0.003, coll=coll)
    rib = random.choice(M['ribbons'])
    rw = random.uniform(0.012, 0.02)
    e = 0.0016
    b1 = box(f"Gift_{i:02d}_RibbonA", (sx + e, rw, sz + e), mat=rib, bevel=0.0006, coll=coll)
    b2 = box(f"Gift_{i:02d}_RibbonB", (rw, sy + e, sz + e), mat=rib, bevel=0.0006, coll=coll)
    for b in (b1, b2):
        parent(b, g)
    if random.random() < 0.75:
        loop = min(sx, sy) * 0.22
        for k, ang in enumerate((35, -35)):
            bow = torus(f"Gift_{i:02d}_Bow{k}", loop, rw * 0.18,
                        (math.copysign(loop * 0.8, ang) * 0.9, 0, sz / 2 + loop * 0.55),
                        (math.radians(90), math.radians(ang), 0), (1.0, 1.0, 0.55), rib, coll)
            parent(bow, g)
        knot = sphere(f"Gift_{i:02d}_Knot", rw * 0.45, (0, 0, sz / 2 + rw * 0.25), rib, coll,
                      scale=(1, 1.4, 0.7))
        parent(knot, g)
    return g, 'BOX'


def ball(M, i, coll):
    """Boule de Noël avec sa capsule dorée et son anneau."""
    r = random.uniform(0.032, 0.05)
    b = sphere(f"Bauble_{i:02d}", r, mat=random.choice(M['bauble']), coll=coll)
    cap = cylinder(f"Bauble_{i:02d}_Cap", r * 0.28, r * 0.25, (0, 0, r * 1.02), mat=M['gold'],
                   bevel=0.001, coll=coll)
    parent(cap, b)
    ring = torus(f"Bauble_{i:02d}_Loop", r * 0.14, r * 0.025, (0, 0, r * 1.3),
                 (math.radians(90), 0, 0), mat=M['gold'], coll=coll)
    parent(ring, b)
    return b, 'SPHERE'


def candy_cane(M, i, coll):
    """Sucre d'orge : crosse rayée rouge et blanc."""
    pts = [(0, 0, -0.07), (0, 0, 0.03)]
    rr = 0.022
    for k in range(1, 9):
        a = math.pi * k / 8
        pts.append((rr - rr * math.cos(a), 0, 0.03 + rr * math.sin(a)))
    pts.append((2 * rr, 0, 0.015))
    c = curve_obj(f"CandyCane_{i:02d}", pts, 0.0065, mat=M['candycane'], kind='POLY', coll=coll)
    c.data.splines[0].use_smooth = True
    # Les courbes ne peuvent pas avoir de rigid body : on convertit en maillage.
    dg = bpy.context.evaluated_depsgraph_get()
    mesh = bpy.data.meshes.new_from_object(c.evaluated_get(dg))
    obj = link(bpy.data.objects.new(c.name, mesh), coll)
    bpy.data.objects.remove(c, do_unlink=True)
    return obj, 'CONVEX_HULL'


def jar(M, i, coll):
    r, h = random.uniform(0.034, 0.045), random.uniform(0.08, 0.11)
    mat = M['ceramic'][i % len(M['ceramic'])]
    j = cylinder(f"Jar_{i:02d}", r, h, mat=mat, bevel=0.004, coll=coll)
    label = cylinder(f"Jar_{i:02d}_Label", r + 0.0006, h * 0.45, (0, 0, -h * 0.05),
                     mat=M['paper'], coll=coll)
    parent(label, j)
    lid = cylinder(f"Jar_{i:02d}_Lid", r * 1.04, 0.012, (0, 0, h / 2 + 0.006), mat=mat, bevel=0.003, coll=coll)
    parent(lid, j)
    knob = sphere(f"Jar_{i:02d}_Knob", r * 0.32, (0, 0, h / 2 + 0.02), M['gold'], coll, scale=(1, 1, 1.3))
    parent(knob, j)
    return j, 'CYLINDER'


def build_pile(M, colliders):
    coll = new_collection("Gifts")
    makers = ([gift_box] * N_GIFTS + [ball] * N_BALLS + [jar] * N_JARS
              + [candy_cane] * N_CANES)
    random.shuffle(makers)
    objs = []
    for i, mk in enumerate(makers):
        o, shape = mk(M, i, coll)
        objs.append((o, shape))

    # Zone réservée à la carte pendant la simulation (supprimée ensuite)
    keepout = box("Keepout", (CARD_SIZE[0] + 0.01, 0.025, 4.0), (CARD_XY[0], CARD_XY[1], 2.0), coll=coll)

    # Lâcher en spirale : positions aléatoires, chaque objet un peu plus haut que le
    # précédent, en évitant de superposer deux objets consécutifs -> vrai tas.
    recent = []
    for k, (o, _) in enumerate(objs):
        for _attempt in range(50):
            x = random.uniform(-CAB_W / 2 + 0.07, CAB_W / 2 - 0.07)
            y = random.uniform(-CAB_D / 2 + 0.07, CAB_D / 2 - 0.07)
            if abs(x - CARD_XY[0]) < 0.11 and abs(y - CARD_XY[1]) < 0.05:
                continue
            if all((Vector((x, y)) - p).length > 0.16 for p in recent[-6:]):
                break
        recent.append(Vector((x, y)))
        o.location = (x, y, 0.1 + 0.045 * k)
        o.rotation_euler = Euler([random.uniform(0, 2 * math.pi) for _ in range(3)])

    walls = [box(f"SimWall_{k}", size, loc, coll=coll) for k, (size, loc) in enumerate([
        ((0.02, CAB_D, 6), (-CAB_W / 2 - 0.01, 0, 3)), ((0.02, CAB_D, 6), (CAB_W / 2 + 0.01, 0, 3)),
        ((CAB_W, 0.02, 6), (0, -CAB_D / 2 - 0.01, 3)), ((CAB_W, 0.02, 6), (0, CAB_D / 2 + 0.01, 3))])]
    simulate(objs, colliders + walls + [keepout])
    for o in walls + [keepout]:
        bpy.data.objects.remove(o, do_unlink=True)
    return coll, [o for o, _ in objs]


def simulate(dynamic, passive, frames=220):
    """Lâche les cadeaux avec la physique, puis fige leur position finale."""
    scene = bpy.context.scene
    if scene.rigidbody_world is None:
        bpy.ops.rigidbody.world_add()
    rbw = scene.rigidbody_world
    rbw.point_cache.frame_start = 1
    rbw.point_cache.frame_end = frames
    if hasattr(rbw, "substeps_per_frame"):
        rbw.substeps_per_frame = 20
    rbw.solver_iterations = 20
    if rbw.collection is None:
        rbw.collection = bpy.data.collections.new("RigidBodyWorld")

    def add_rb(obj, kind, shape):
        rbw.collection.objects.link(obj)
        rb = obj.rigid_body
        rb.type = kind
        rb.collision_shape = shape
        rb.friction = 0.7
        rb.restitution = 0.05
        rb.use_margin = True
        rb.collision_margin = 0.001
        rb.linear_damping = 0.2
        rb.angular_damping = 0.3

    for o, shape in dynamic:
        add_rb(o, 'ACTIVE', shape)
        o.rigid_body.mass = 0.3
    for o in passive:
        add_rb(o, 'PASSIVE', 'BOX')

    for f in range(1, frames + 1):
        scene.frame_set(f)
    final = {o.name: o.matrix_world.copy() for o, _ in dynamic}
    scene.frame_set(1)
    bpy.ops.rigidbody.world_remove()
    for o, _ in dynamic:
        o.matrix_world = final[o.name]


def pile_height_near(objs, x, y, radius=0.16):
    h = 0.0
    for o in objs:
        if (Vector((o.location.x, o.location.y)) - Vector((x, y))).length < radius:
            for corner in o.bound_box:
                h = max(h, (o.matrix_world @ Vector(corner)).z)
    return h


# ---------------------------------------------------------------------------
# CHÈQUE-CADEAU
# ---------------------------------------------------------------------------


def texture_dir():
    try:
        here = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        here = ""
    for d in (here, bpy.path.abspath("//"), os.getcwd()):
        if d and os.path.isdir(os.path.join(d, "textures")):
            return os.path.join(d, "textures")
    raise FileNotFoundError("Dossier 'textures' introuvable à côté du script")


def card_face_mat(name, filename):
    """Impression du chèque-cadeau : image en couleur de base, papier couché satiné."""
    mat = new_mat(name, (1, 1, 1), 0.42, Coat_Weight=0.15, Coat_Roughness=0.25)
    nt = mat.node_tree
    img = bpy.data.images.load(os.path.join(texture_dir(), filename), check_existing=True)
    img.pack()
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = 'Cubic'
    nt.links.new(tex.outputs["Color"], bsdf_of(mat).inputs["Base Color"])
    add_bump(mat, 1200, 0.04)
    return mat


def rounded_rect(w, h, r, seg=8):
    pts = []
    for cx, cz, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90),
                       (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for k in range(seg + 1):
            a = math.radians(a0 + 90 * k / seg)
            pts.append((cx + r * math.cos(a), cz + r * math.sin(a)))
    return pts


def build_card(M, base_z):
    """Chèque-cadeau recto/verso : carte cartonnée à coins arrondis.
    Recto (côté caméra, -Y) = textures/cheque_recto.png, verso (+Y) = textures/cheque_verso.png."""
    coll = new_collection("GiftCard")
    w, t, h = CARD_SIZE
    mats = [card_face_mat("Card_Recto", "cheque_recto.png"),
            card_face_mat("Card_Verso", "cheque_verso.png"),
            new_mat("Card_Edge", (0.92, 0.9, 0.86), 0.7)]

    mesh = bpy.data.meshes.new("GiftCard")
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    outline = rounded_rect(w, h, CARD_CORNER)
    front = [bm.verts.new((x, -t / 2, z)) for x, z in outline]
    back = [bm.verts.new((x, t / 2, z)) for x, z in outline]
    f_front = bm.faces.new(front)        # normale vers -Y (caméra)
    f_back = bm.faces.new(back[::-1])
    if f_front.normal.y > 0:
        f_front.normal_flip()
    if f_back.normal.y < 0:
        f_back.normal_flip()
    f_front.material_index, f_back.material_index = 0, 1
    for loop in f_front.loops:
        x, _, z = loop.vert.co
        loop[uv].uv = ((x + w / 2) / w, (z + h / 2) / h)
    for loop in f_back.loops:            # vu de derrière : image miroir en X
        x, _, z = loop.vert.co
        loop[uv].uv = ((w / 2 - x) / w, (z + h / 2) / h)
    n = len(outline)
    for k in range(n):
        side = bm.faces.new((front[k], back[k], back[(k + 1) % n], front[(k + 1) % n]))
        side.material_index = 2
    bmesh.ops.recalc_face_normals(bm, faces=[f for f in bm.faces if f.material_index == 2])
    bm.to_mesh(mesh)
    bm.free()
    card = link(bpy.data.objects.new("GiftCard", mesh), coll)
    for m in mats:
        card.data.materials.append(m)
    bev = card.modifiers.new("Bevel", 'BEVEL')
    bev.width = t * 0.3
    bev.segments = 2
    bev.limit_method = 'ANGLE'

    card.location = (CARD_XY[0], CARD_XY[1], base_z + h / 2)
    card.rotation_euler = (math.radians(-2.5), math.radians(-5), math.radians(2))
    return coll, card


def build_fairy_lights(M):
    """Guirlandes lumineuses tendues en arc sur le fond de la vitrine."""
    coll = new_collection("FairyLights")
    y = CAB_D / 2 - 0.025
    rows = [(0.74, 0.07), (0.56, 0.06)]
    for r, (z_top, sag) in enumerate(rows):
        n = 22
        pts = []
        for k in range(n + 1):
            t = k / n
            x = -CAB_W / 2 + 0.01 + t * (CAB_W - 0.02)
            z = z_top - sag * 4 * t * (1 - t) + 0.004 * math.sin(t * 40 + r)
            pts.append((x, y, z))
        curve_obj(f"FairyWire_{r}", pts, 0.0009, mat=M['wire'], coll=coll)
        for k in range(1, n, 1):
            x, yy, z = pts[k]
            bulb = sphere(f"FairyBulb_{r}_{k:02d}", 0.0045, (x, yy - 0.004, z - 0.007), M['bulb'], coll,
                          scale=(1, 1, 1.5))
            bulb.visible_shadow = False
    return coll


# ---------------------------------------------------------------------------
# LUMIÈRES, CAMÉRA, RENDU
# ---------------------------------------------------------------------------


def area_light(name, size, energy, loc, rot, color=(1, 1, 1), visible_glossy=True, coll=None):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.shape = 'RECTANGLE'
    ld.size, ld.size_y = size
    ld.energy = energy
    ld.color = color
    obj = link(bpy.data.objects.new(name, ld), coll)
    obj.location = loc
    obj.rotation_euler = rot
    if hasattr(obj, "visible_glossy"):
        obj.visible_glossy = visible_glossy
    return obj


def build_lighting(M):
    coll = new_collection("Lighting")
    # Caisson lumineux du plafond de la vitrine
    area_light("Ceiling_Panel", (CAB_W * 0.9, CAB_D * 0.9), 40, (0, 0, CAB_H - 0.03), (0, 0, 0),
               (1.0, 0.9, 0.78), coll=coll)
    # Soleil rasant (ombres nettes en diagonale sur le tapis et les portes, comme la référence)
    sd = bpy.data.lights.new("Sun", 'SUN')
    sd.energy, sd.color, sd.angle = 10.0, (1.0, 0.78, 0.55), math.radians(0.6)
    sun = link(bpy.data.objects.new("Sun", sd), coll)
    sun.location = (-4.0, -3.2, 2.2)
    aim = empty("Sun_Target", (0.5, -1.3, FLOOR_Z), coll=coll)
    tt = sun.constraints.new('TRACK_TO')
    tt.target, tt.track_axis, tt.up_axis = aim, 'TRACK_NEGATIVE_Z', 'UP_Y'
    # Pan d'ombre hors champ (bord d'un bâtiment / d'une verrière) : seule une diagonale de
    # soleil tombe sur le bas du tapis et le battant droit, comme sur la photo de référence.
    def edge_y(x):
        return -2.95 + 0.1125 * (x + 2.0)
    zc = FLOOR_Z + 4.38
    mesh = bpy.data.meshes.new("SunOccluder")
    mesh.from_pydata([(-10, edge_y(-10), zc), (3, edge_y(3), zc), (3, 3, zc), (-10, 3, zc)], [], [(0, 1, 2, 3)])
    occ = link(bpy.data.objects.new("SunOccluder", mesh), coll)
    occ.visible_camera = False
    occ.visible_glossy = False
    occ.visible_transmission = False
    occ.visible_diffuse = False
    # Lumière du hall (grande baie hors champ derrière la caméra) : douce et froide
    area_light("Lobby_Fill", (3.0, 2.0), 18, (0.5, -9.5, FLOOR_Z + 1.6), (math.radians(90), 0, 0),
               (0.85, 0.9, 1.0), coll=coll)
    # Contre-jour discret dans la vitrine pour détacher la pince du fond
    area_light("Rim_Back", (0.5, 0.25), 15, (0.25, 0.25, 0.75), (math.radians(-140), 0, math.radians(20)),
               (1.0, 0.9, 0.8), coll=coll)

    for sx in (-1, 1):
        card = box(f"ReflectCard_{sx}", (0.02, 0.4, 2.0), (sx * 0.8, -0.9, 0.6),
                   (0, 0, math.radians(sx * 35)), mat=M['card'], coll=coll)
        card.visible_camera = False
        card.visible_shadow = False

    world = bpy.data.worlds.new("LobbyWorld")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.75, 0.8, 0.9, 1.0)
    bg.inputs["Strength"].default_value = 0.05
    bpy.context.scene.world = world


def setup_compositor(scene):
    """Léger halo (bloom) sur les néons et l'enseigne, comme un vrai capteur photo."""
    try:
        if hasattr(scene, "compositing_node_group"):          # Blender 5.x
            tree = bpy.data.node_groups.new("Compositor", "CompositorNodeTree")
            tree.interface.new_socket("Image", in_out='OUTPUT', socket_type='NodeSocketColor')
            scene.compositing_node_group = tree
            rl = tree.nodes.new("CompositorNodeRLayers")
            out = tree.nodes.new("NodeGroupOutput")
        else:                                                 # Blender 4.x
            scene.use_nodes = True
            tree = scene.node_tree
            rl = tree.nodes.get("Render Layers") or tree.nodes.new("CompositorNodeRLayers")
            out = tree.nodes.get("Composite") or tree.nodes.new("CompositorNodeComposite")
        glare = tree.nodes.new("CompositorNodeGlare")
        if "Type" in glare.inputs:
            glare.inputs["Type"].default_value = 'Bloom'
            glare.inputs["Threshold"].default_value = 1.2
            glare.inputs["Strength"].default_value = 0.35
            glare.inputs["Size"].default_value = 0.6
        else:
            glare.glare_type = 'FOG_GLOW'
            glare.threshold = 1.2
            glare.mix = -0.7
            glare.size = 8
        tree.links.new(rl.outputs["Image"], glare.inputs["Image"])
        tree.links.new(glare.outputs["Image"], out.inputs[0])
    except Exception as exc:
        print("Compositeur ignoré :", exc)


def build_camera(focus_obj):
    coll = new_collection("Camera")
    cam_data = bpy.data.cameras.new("Camera")
    cam_data.lens = 45
    cam_data.sensor_width = 36
    cam_data.dof.use_dof = True
    cam_data.dof.focus_object = focus_obj
    cam_data.dof.aperture_fstop = 2.8
    cam = link(bpy.data.objects.new("Camera", cam_data), coll)
    cam.location = CAM_WIDE[0]
    target = empty("Camera_Target", CAM_WIDE[1], coll=coll)
    tt = cam.constraints.new('TRACK_TO')
    tt.target = target
    tt.track_axis = 'TRACK_NEGATIVE_Z'
    tt.up_axis = 'UP_Y'
    bpy.context.scene.camera = cam
    return cam, target


# Plan large (position caméra, cible, focale) -> plan serré sur la pince
CAM_WIDE = ((0.0, WALL_Y - 7.0, FLOOR_Z + 1.25), (0.0, WALL_Y, FLOOR_Z + 1.45), 62)
CAM_CLOSE = ((0.02, -1.25, 0.5), (0.02, -0.07, 0.47), 85)


def animate_camera(cam, target, f_start, f_end):
    for f, (loc, aim, lens) in ((f_start, CAM_WIDE), (f_end, CAM_CLOSE)):
        key_loc(cam, f, loc)
        key_loc(target, f, aim)
        cam.data.lens = lens
        cam.data.keyframe_insert("lens", frame=f)


def setup_render(scene):
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = SAMPLES
    scene.cycles.use_denoising = True
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
    scene.cycles.blur_glossy = 1.0
    scene.cycles.max_bounces = 16
    scene.cycles.transmission_bounces = 16
    scene.cycles.transparent_max_bounces = 16
    scene.render.resolution_x, scene.render.resolution_y = RES_X, RES_Y
    scene.render.resolution_percentage = 100
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 1, FRAME_END
    scene.render.use_motion_blur = True
    scene.render.motion_blur_shutter = 0.4
    scene.render.filepath = "//render/claw_"
    scene.render.image_settings.file_format = 'PNG'
    scene.view_settings.view_transform = 'AgX'
    for look in ('AgX - Medium High Contrast', 'Medium High Contrast'):
        try:
            scene.view_settings.look = look
            break
        except TypeError:
            pass
    scene.view_settings.exposure = 0.0

    if USE_GPU:
        try:
            prefs = bpy.context.preferences.addons['cycles'].preferences
            for backend in ('OPTIX', 'CUDA', 'HIP', 'METAL', 'ONEAPI'):
                try:
                    prefs.compute_device_type = backend
                except TypeError:
                    continue
                prefs.get_devices()
                if any(d.type == backend for d in prefs.devices):
                    for d in prefs.devices:
                        d.use = True
                    scene.cycles.device = 'GPU'
                    break
        except Exception:
            pass


# ---------------------------------------------------------------------------
# ANIMATION
# ---------------------------------------------------------------------------


def key_loc(obj, frame, loc):
    obj.location = loc
    obj.keyframe_insert("location", frame=frame)


def key_rot(obj, frame, rot):
    obj.rotation_euler = rot
    obj.keyframe_insert("rotation_euler", frame=frame)


def animate(rig, hinges, env):
    scene = bpy.context.scene
    try:
        bpy.context.preferences.edit.keyframe_new_interpolation_type = 'BEZIER'
    except Exception:
        pass

    ex, ey = env.location.x, env.location.y
    env_top = env.location.z + CARD_SIZE[2] / 2
    grab_z = env_top - 0.011 + TIP_DROP
    top_z = 0.62
    start = (-0.16, ey, top_z)

    F = dict(start=1, arrive=40, settle=48, open_done=54, bottom=86, closed=100,
             grab=98, lift_start=106, top=150, end=FRAME_END)

    # Trajectoire du chariot
    key_loc(rig, F['start'], start)
    key_loc(rig, F['arrive'], (ex + 0.012, ey, top_z))
    key_loc(rig, F['settle'], (ex, ey, top_z))
    key_loc(rig, F['open_done'], (ex, ey, top_z))
    key_loc(rig, F['bottom'], (ex, ey, grab_z))
    key_loc(rig, F['lift_start'], (ex, ey, grab_z))
    key_loc(rig, F['top'], (ex, ey, top_z - 0.02))
    key_loc(rig, F['end'], (ex, ey, top_z - 0.02))

    # Balancement pendulaire (inertie du câble)
    sway = [(F['start'], 0, 0), (F['arrive'], -4, 0), (F['settle'] + 6, 2.5, 0.5),
            (F['open_done'] + 8, -1, 0), (F['bottom'], 0, 0), (F['lift_start'], 0, 0),
            (F['lift_start'] + 14, 0, 2.0), (F['top'], 0, -3.0), (F['top'] + 10, 0.5, 2.0),
            (F['top'] + 18, -0.3, -1.0), (F['end'], 0, 0.3)]
    for f, ry, rx in sway:
        key_rot(rig, f, (math.radians(rx), math.radians(ry), 0))

    # Ouverture / fermeture des griffes (petit décalage entre elles = plus naturel)
    for k, h in enumerate(hinges):
        phi = h.rotation_euler.z
        d = k
        key_rot(h, F['start'], (CLOSED_ANGLE + math.radians(4), 0, phi))
        key_rot(h, F['settle'] + d, (CLOSED_ANGLE + math.radians(4), 0, phi))
        key_rot(h, F['open_done'] + 4 + d, (OPEN_ANGLE, 0, phi))
        key_rot(h, F['bottom'] + 2, (OPEN_ANGLE, 0, phi))
        key_rot(h, F['closed'] - 2 + d, (CLOSED_ANGLE, 0, phi))
        key_rot(h, F['end'], (CLOSED_ANGLE, 0, phi))

    # Le chèque-cadeau est "attrapée" : contrainte Child Of activée au moment du pincement
    scene.frame_set(F['grab'])
    rig_mw = rig.matrix_world.copy()
    con = env.constraints.new('CHILD_OF')
    con.target = rig
    con.inverse_matrix = rig_mw.inverted()
    con.influence = 0.0
    con.keyframe_insert("influence", frame=F['grab'] - 1)
    con.influence = 1.0
    con.keyframe_insert("influence", frame=F['grab'])

    # En remontant, la carte se redresse légèrement sous son propre poids
    env_rot = env.rotation_euler.copy()
    key_rot(env, F['lift_start'], env_rot)
    key_rot(env, F['top'], (env_rot.x * 0.3, env_rot.y * 0.4, env_rot.z))
    scene.frame_set(1)
    return F


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------


def main():
    scene = reset_scene()
    M = build_materials()
    cab_coll, colliders = build_cabinet(M)
    claw_coll, rig, hinges, cable_attach = build_claw(M)
    rig.location = (-0.16, CARD_XY[1], 0.62)
    build_cable(M, rig, cable_attach, claw_coll)
    build_gantry(M, rig)
    build_entrance(M)

    _, gifts = build_pile(M, colliders)
    base = max(0.0, pile_height_near(gifts, *CARD_XY) - CARD_SIZE[2] * 0.62)
    _, env = build_card(M, base)

    if FAIRY_LIGHTS:
        build_fairy_lights(M)
    build_lighting(M)
    cam, cam_target = build_camera(env)
    setup_render(scene)
    setup_compositor(scene)
    F = animate(rig, hinges, env)
    animate_camera(cam, cam_target, 1, F['top'])
    scene.frame_set(1)

    if bpy.app.background:
        here = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
        out = os.path.join(here, "claw_machine.blend")
        bpy.ops.wm.save_as_mainfile(filepath=out)
        print(f"Saved {out}")


if __name__ == "__main__":
    main()
