"""
Médaille ovale en laiton vieilli suspendue à un ruban satin noir.

Utilisation :
  - Dans Blender : onglet Scripting > Ouvrir medal.py > Run Script
  - En ligne de commande :
        blender -b -P medal.py -- --render out.png [--samples 256] [--scale 100]
        blender -b -P medal.py -- --save medal.blend

Unités : 1 unité Blender = 1 cm (Unit Scale = 0.01, donc les dimensions
s'affichent en cm dans l'interface).
"""
import bpy
import bmesh
import math
import sys
from mathutils import Vector, Matrix

# --------------------------------------------------------------------------
# Paramètres
# --------------------------------------------------------------------------
A = 2.5          # demi-largeur de l'ovale (cm)
B = 3.2          # demi-hauteur de l'ovale (cm)
THICK = 0.25     # épaisseur de la médaille
TAB_W = 2.0      # largeur de la bélière (languette du haut)
TAB_TOP = 4.0    # hauteur du haut de la bélière
SLOT_W = 1.45    # fente pour le ruban
SLOT_Z0, SLOT_Z1 = 3.40, 3.72
STROKE = 0.11   # largeur des traits gravés
ENGRAVE = 0.16   # profondeur de gravure (sur 0.25)
RIBBON_W = 1.3
RIBBON_TOP = 24.0

MEDAL_YAW = -24.0   # rotation autour de la verticale (on voit la tranche droite)
MEDAL_ROLL = -3.0   # légère inclinaison dans le plan de l'image


def argv_after_dashes():
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


# --------------------------------------------------------------------------
# Scène
# --------------------------------------------------------------------------
def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    sc.unit_settings.scale_length = 0.01
    sc.unit_settings.length_unit = 'CENTIMETERS'
    return sc


# --------------------------------------------------------------------------
# Géométrie
# --------------------------------------------------------------------------
def medal_outline(n=160, r=0.12):
    """Contour 2D (x, z) : ovale + bélière rectangulaire aux coins arrondis."""
    pts = []
    # angle de départ sur l'ellipse où x = TAB_W/2 (côté droit)
    t0 = math.acos(TAB_W / 2 / A)          # angle depuis l'axe x
    # on parcourt l'ellipse de t0 (droite, haut) dans le sens horaire jusqu'à pi - t0
    span = 2 * math.pi - (math.pi - 2 * t0)
    for i in range(n + 1):
        t = t0 - span * i / n
        pts.append((A * math.cos(t), B * math.sin(t)))
    # côté gauche de la bélière, coins arrondis en haut
    hw = TAB_W / 2
    for cx, a0, a1 in ((-hw + r, math.pi, math.pi / 2), (hw - r, math.pi / 2, 0.0)):
        for k in range(7):
            a = a0 + (a1 - a0) * k / 6
            pts.append((cx + r * math.cos(a), TAB_TOP - r + r * math.sin(a)))
    return pts


def make_prism(name, outline, y0, y1):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    front = [bm.verts.new((x, y0, z)) for x, z in outline]
    back = [bm.verts.new((x, y1, z)) for x, z in outline]
    n = len(outline)
    bm.faces.new(list(reversed(front)))
    bm.faces.new(back)
    for i in range(n):
        j = (i + 1) % n
        f = bm.faces.new((front[i], front[j], back[j], back[i]))
        f.smooth = True
    bm.normal_update()
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return ob


def box(bm, center, axis_u, length, width, y0, y1):
    """Boîte orientée dans le plan xz entre y0 et y1."""
    u = Vector((axis_u[0], 0, axis_u[1])).normalized()
    v = Vector((-u.z, 0, u.x))
    c = Vector((center[0], 0, center[1]))
    corners = []
    for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        corners.append(c + u * su * length / 2 + v * sv * width / 2)
    f = [bm.verts.new((p.x, y0, p.z)) for p in corners]
    b = [bm.verts.new((p.x, y1, p.z)) for p in corners]
    bm.faces.new(list(reversed(f)))
    bm.faces.new(b)
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((f[i], f[j], b[j], b[i]))


# --- Glyphes (segments en coordonnées locales, hauteur ~1) ----------------
def glyph_M(w=0.62, h=0.62):
    return [((-w/2, -h/2), (-w/2, h/2)), ((-w/2, h/2), (0, -h*0.05)),
            ((0, -h*0.05), (w/2, h/2)), ((w/2, h/2), (w/2, -h/2))]


def chevron(w=0.62, h=0.36):
    """Chevron pointant vers +y (Λ)."""
    return [((-w/2, -h/2), (0, h/2)), ((0, h/2), (w/2, -h/2))]


def bar(w=0.5):
    return [((-w/2, 0), (w/2, 0))]


def place(segs, pos, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    out = []
    for (x0, y0), (x1, y1) in segs:
        out.append(((pos[0] + x0*ca - y0*sa, pos[1] + x0*sa + y0*ca),
                    (pos[0] + x1*ca - y1*sa, pos[1] + x1*sa + y1*ca)))
    return out


def snowflake_segments():
    segs = []
    cz = -0.05  # centre du motif
    # 4 « M » au centre (haut/bas droits, gauche/droite tournés -> Σ)
    rm = 0.78
    segs += place(glyph_M(), (0, cz + rm), 0)
    segs += place(glyph_M(), (0, cz - rm), 0)
    segs += place(glyph_M(), (-rm, cz), math.pi / 2)
    segs += place(glyph_M(), (rm, cz), math.pi / 2)
    # 8 branches
    for k in range(8):
        phi = math.pi / 2 + k * math.pi / 4           # direction de la branche
        d = (math.cos(phi), math.sin(phi))
        rot = phi - math.pi / 2                       # +y local -> vers l'extérieur
        ell = 1 / math.sqrt((d[0] / A) ** 2 + (d[1] / B) ** 2)
        if k % 4 == 0:      # haut / bas : Λ / V (losange coupé)
            r_out, r_in = ell * 0.84, ell * 0.58
            segs += place(chevron(), (d[0]*r_out, cz + d[1]*r_out), rot)
            segs += place(chevron(), (d[0]*r_in, cz + d[1]*r_in), rot + math.pi)
        elif k % 4 == 2:    # gauche / droite : < >
            r_out, r_in = ell * 0.84, ell * 0.60
            segs += place(chevron(0.66, 0.34), (d[0]*r_out, cz + d[1]*r_out), rot)
            segs += place(chevron(0.66, 0.34), (d[0]*r_in, cz + d[1]*r_in), rot + math.pi)
        else:               # diagonales : « K » + chevron extérieur
            r_k, r_out = ell * 0.55, ell * 0.80
            segs += place(bar(0.58), (d[0]*r_k, cz + d[1]*r_k), rot)
            segs += place(chevron(0.56, 0.32),
                          (d[0]*(r_k + 0.26), cz + d[1]*(r_k + 0.26)), rot + math.pi)
            segs += place(chevron(0.6, 0.36), (d[0]*r_out, cz + d[1]*r_out), rot)
    return segs


def make_cutters(segs):
    me = bpy.data.meshes.new("Gravure_cutter")
    bm = bmesh.new()
    for (x0, z0), (x1, z1) in segs:
        dx, dz = x1 - x0, z1 - z0
        L = math.hypot(dx, dz)
        # traits raccourcis : petits ponts de métal aux jonctions (effet pochoir)
        box(bm, ((x0 + x1) / 2, (z0 + z1) / 2), (dx, dz), max(L - STROKE * 1.1, 0.05), STROKE,
            -THICK / 2 - 0.05, -THICK / 2 + ENGRAVE)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("Gravure_cutter", me)
    bpy.context.collection.objects.link(ob)
    ob.hide_render = True
    ob.display_type = 'WIRE'
    return ob


def make_slot_cutter():
    me = bpy.data.meshes.new("Fente_cutter")
    bm = bmesh.new()
    box(bm, (0, (SLOT_Z0 + SLOT_Z1) / 2), (1, 0), SLOT_W, SLOT_Z1 - SLOT_Z0, -1, 1)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("Fente_cutter", me)
    bpy.context.collection.objects.link(ob)
    ob.hide_render = True
    ob.display_type = 'WIRE'
    return ob


def make_ribbon(parent):
    """Ruban qui descend devant, passe dans la fente et remonte derrière."""
    yb = THICK / 2 + 0.07
    zc = (SLOT_Z1 + 0.27)  # centre de la boucle autour de la barre
    path = []
    # brin avant (du haut vers le bas)
    for i in range(40):
        t = i / 39
        z = RIBBON_TOP + (zc + 0.6 - RIBBON_TOP) * t
        y = -0.02 + (-yb + 0.02) * (t ** 3)
        path.append((y, z))
    # boucle sous la barre (à travers la fente)
    rr = (zc - (SLOT_Z0 + SLOT_Z1) / 2)
    rad = yb
    for i in range(1, 24):
        a = math.pi + math.pi * i / 24
        path.append((rad * math.cos(a), zc - 0.15 + rr * 0.9 * math.sin(a) * 1.0))
    # brin arrière (vers le haut)
    for i in range(40):
        t = i / 39
        z = zc + 0.6 + (RIBBON_TOP - zc - 0.6) * t
        y = yb - (yb - 0.02) * (t ** (1 / 3) if t > 0 else 0)
        path.append((y, z))

    me = bpy.data.meshes.new("Ruban")
    bm = bmesh.new()
    rows = []
    for idx, (y, z) in enumerate(path):
        # léger vrillage vers le haut pour accrocher la lumière
        h = max(0.0, (z - 6) / (RIBBON_TOP - 6))
        tw = math.radians(10) * h * (1 if idx < 40 else 0.7)
        hw = RIBBON_W / 2
        row = []
        for s in (-1, 1):
            x = s * hw * math.cos(tw)
            yy = y + s * hw * math.sin(tw)
            row.append(bm.verts.new((x, yy, z)))
        rows.append(row)
    for i in range(len(rows) - 1):
        f = bm.faces.new((rows[i][0], rows[i][1], rows[i + 1][1], rows[i + 1][0]))
        f.smooth = True
    uv = bm.loops.layers.uv.new("UVMap")
    for f in bm.faces:
        for l in f.loops:
            l[uv].uv = (0.5 + l.vert.co.x / RIBBON_W, l.vert.co.z / RIBBON_W)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("Ruban", me)
    bpy.context.collection.objects.link(ob)
    sol = ob.modifiers.new("Epaisseur", 'SOLIDIFY')
    sol.thickness = 0.035
    sol.offset = 0
    sub = ob.modifiers.new("Lissage", 'SUBSURF')
    sub.levels = 1
    sub.render_levels = 2
    ob.parent = parent
    return ob


# --------------------------------------------------------------------------
# Matériaux
# --------------------------------------------------------------------------
def node(nt, kind, loc, **props):
    n = nt.nodes.new(kind)
    n.location = loc
    for k, v in props.items():
        setattr(n, k, v)
    return n


def mat_antique_brass():
    m = bpy.data.materials.new("Laiton_vieilli")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = node(nt, 'ShaderNodeOutputMaterial', (1200, 0))
    bsdf = node(nt, 'ShaderNodeBsdfPrincipled', (900, 0))
    bsdf.inputs['Metallic'].default_value = 1.0
    nt.links.new(bsdf.outputs[0], out.inputs[0])

    tc = node(nt, 'ShaderNodeTexCoord', (-1000, 0))
    # grandes taches de patine
    n1 = node(nt, 'ShaderNodeTexNoise', (-750, 250))
    n1.inputs['Scale'].default_value = 0.9
    n1.inputs['Detail'].default_value = 8
    n1.inputs['Roughness'].default_value = 0.6
    nt.links.new(tc.outputs['Object'], n1.inputs['Vector'])
    # micro-rayures brossées (étirées)
    mp = node(nt, 'ShaderNodeMapping', (-750, -150))
    mp.inputs['Scale'].default_value = (60, 1.5, 3)
    mp.inputs['Rotation'].default_value = (0, math.radians(20), 0)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    n2 = node(nt, 'ShaderNodeTexNoise', (-550, -150))
    n2.inputs['Scale'].default_value = 4
    n2.inputs['Detail'].default_value = 4
    nt.links.new(mp.outputs[0], n2.inputs['Vector'])
    # occlusion pour noircir creux et bords (patine accumulée)
    ao = node(nt, 'ShaderNodeAmbientOcclusion', (-550, 450))
    ao.inputs['Distance'].default_value = 0.25
    ao.samples = 8

    cr1 = node(nt, 'ShaderNodeValToRGB', (-350, 250))
    cr1.color_ramp.elements[0].position = 0.25
    cr1.color_ramp.elements[0].color = (0.075, 0.06, 0.035, 1)   # patine brune
    cr1.color_ramp.elements[1].position = 0.80
    cr1.color_ramp.elements[1].color = (0.27, 0.20, 0.095, 1)    # laiton
    nt.links.new(n1.outputs['Fac'], cr1.inputs[0])

    mix_ao = node(nt, 'ShaderNodeMix', (0, 300))
    mix_ao.data_type = 'RGBA'
    mix_ao.blend_type = 'MULTIPLY'
    mix_ao.inputs['Factor'].default_value = 0.8
    nt.links.new(cr1.outputs[0], mix_ao.inputs[6])
    nt.links.new(ao.outputs['AO'], mix_ao.inputs[7])

    scr = node(nt, 'ShaderNodeMix', (300, 300))
    scr.data_type = 'RGBA'
    scr.blend_type = 'OVERLAY'
    scr.inputs['Factor'].default_value = 0.35
    nt.links.new(mix_ao.outputs[2], scr.inputs[6])
    nt.links.new(n2.outputs['Color'], scr.inputs[7])
    nt.links.new(scr.outputs[2], bsdf.inputs['Base Color'])

    rr = node(nt, 'ShaderNodeMapRange', (300, -150))
    rr.inputs['To Min'].default_value = 0.32
    rr.inputs['To Max'].default_value = 0.62
    nt.links.new(n2.outputs['Fac'], rr.inputs['Value'])
    nt.links.new(rr.outputs[0], bsdf.inputs['Roughness'])

    bump = node(nt, 'ShaderNodeBump', (600, -300))
    bump.inputs['Strength'].default_value = 0.08
    bump.inputs['Distance'].default_value = 0.01
    nt.links.new(n2.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs[0], bsdf.inputs['Normal'])
    return m


def mat_polished_brass():
    m = bpy.data.materials.new("Laiton_poli_gravure")
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (1.0, 0.80, 0.45, 1)
    b.inputs['Metallic'].default_value = 1.0
    b.inputs['Roughness'].default_value = 0.22
    # un peu d'émission pour reproduire l'éclat des tranches usinées
    b.inputs['Emission Color'].default_value = (1.0, 0.85, 0.55, 1)
    b.inputs['Emission Strength'].default_value = 0.22
    return m


def mat_satin_black():
    m = bpy.data.materials.new("Satin_noir")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.008, 0.008, 0.009, 1)
    b.inputs['Roughness'].default_value = 0.45
    b.inputs['Specular IOR Level'].default_value = 0.22
    b.inputs['Anisotropic'].default_value = 0.85
    b.inputs['Sheen Weight'].default_value = 0.12
    b.inputs['Sheen Roughness'].default_value = 0.3
    b.inputs['Sheen Tint'].default_value = (0.6, 0.6, 0.65, 1)
    tg = nt.nodes.new('ShaderNodeTangent')
    tg.direction_type = 'UV_MAP'
    tg.uv_map = "UVMap"
    tg.location = (-300, -300)
    nt.links.new(tg.outputs[0], b.inputs['Tangent'])
    return m


# --------------------------------------------------------------------------
# Lumières, caméra, rendu
# --------------------------------------------------------------------------
def add_area(name, loc, target, power, size, color=(1, 1, 1), size_y=None):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.energy = power
    ld.color = color
    if size_y:
        ld.shape = 'RECTANGLE'
        ld.size, ld.size_y = size, size_y
    else:
        ld.size = size
    ob = bpy.data.objects.new(name, ld)
    bpy.context.collection.objects.link(ob)
    ob.location = loc
    d = Vector(target) - Vector(loc)
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob


def build():
    sc = reset_scene()

    # --- médaille
    medal = make_prism("Medaille", medal_outline(), -THICK / 2, THICK / 2)
    bev = medal.modifiers.new("Chanfrein", 'BEVEL')
    bev.width = 0.025
    bev.segments = 3
    bev.limit_method = 'ANGLE'
    bev.angle_limit = math.radians(40)
    bev.harden_normals = True

    slot = make_slot_cutter()
    b1 = medal.modifiers.new("Fente", 'BOOLEAN')
    b1.operation = 'DIFFERENCE'
    b1.solver = 'EXACT'
    b1.object = slot

    cut = make_cutters(snowflake_segments())
    b2 = medal.modifiers.new("Gravure", 'BOOLEAN')
    b2.operation = 'DIFFERENCE'
    b2.solver = 'EXACT'
    b2.object = cut
    b2.use_self = True  # les traits se croisent

    brass = mat_antique_brass()
    polish = mat_polished_brass()
    medal.data.materials.append(brass)
    medal.data.materials.append(polish)
    # le cutter porte le matériau poli : le booléen exact le transfère aux faces gravées
    cut.data.materials.append(brass)
    cut.data.materials.append(polish)
    for p in cut.data.polygons:
        p.material_index = 1
    slot.data.materials.append(brass)

    # pivot commun pour orienter médaille + ruban
    rig = bpy.data.objects.new("Pivot", None)
    sc.collection.objects.link(rig)
    rig.rotation_euler = (0, math.radians(MEDAL_ROLL), math.radians(MEDAL_YAW))
    for o in (medal, slot, cut):
        o.parent = rig

    ribbon = make_ribbon(rig)
    ribbon.data.materials.append(mat_satin_black())

    # --- monde : fond noir mat
    world = bpy.data.worlds.new("Fond")
    sc.world = world
    world.use_nodes = True
    world.node_tree.nodes['Background'].inputs[0].default_value = (0.006, 0.0055, 0.005, 1)
    world.node_tree.nodes['Background'].inputs[1].default_value = 1.0

    # fond de studio (toile noire) derrière le sujet
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 60, 0), rotation=(math.pi / 2, 0, 0))
    bg = bpy.context.active_object
    bg.name = "Fond_noir"
    bm_ = bpy.data.materials.new("Toile_noire")
    bm_.use_nodes = True
    pb = bm_.node_tree.nodes['Principled BSDF']
    pb.inputs['Base Color'].default_value = (0.012, 0.011, 0.010, 1)
    pb.inputs['Roughness'].default_value = 1.0
    bg.data.materials.append(bm_)

    # --- éclairage : grande boîte à lumière douce en haut à gauche,
    #     contre-jour léger, débouchage très faible à droite
    add_area("Key_softbox", (-28, -38, 30), (0, 0, 2), 40000, 30, (1.0, 0.95, 0.88))
    add_area("Rim_haut", (6, 25, 30), (0, 0, 3), 12000, 12, (1.0, 0.92, 0.82))
    add_area("Fill_droite", (40, -20, 0), (0, 0, 0), 2500, 25, (0.9, 0.93, 1.0))
    add_area("Strip_ruban", (-14, -20, 14), (0, 0, 12), 1500, 3, size_y=30)

    # --- caméra (portrait, téléobjectif)
    cd = bpy.data.cameras.new("Camera")
    cd.lens = 85
    cd.sensor_fit = 'VERTICAL'
    cd.sensor_height = 36
    cam = bpy.data.objects.new("Camera", cd)
    sc.collection.objects.link(cam)
    cam.location = (0.2, -57, 3.95)
    cam.rotation_euler = (math.pi / 2, 0, 0)
    cd.dof.use_dof = True
    cd.dof.focus_distance = 57
    cd.dof.aperture_fstop = 8
    sc.camera = cam

    # --- rendu
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = 256
    sc.cycles.use_denoising = True
    sc.render.resolution_x = 1165
    sc.render.resolution_y = 1332
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.look = 'AgX - Medium High Contrast'
    sc.render.film_transparent = False
    return sc


def main():
    args = argv_after_dashes()
    sc = build()
    if "--samples" in args:
        sc.cycles.samples = int(args[args.index("--samples") + 1])
    if "--scale" in args:
        sc.render.resolution_percentage = int(args[args.index("--scale") + 1])
    if "--save" in args:
        bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath(args[args.index("--save") + 1]))
    if "--render" in args:
        sc.render.filepath = args[args.index("--render") + 1]
        bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
