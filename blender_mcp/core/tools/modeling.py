import bpy
import math

def _get_obj(name):
    return bpy.data.objects.get(name)

def _enter_edit_mode(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

def _exit_edit_mode():
    bpy.ops.object.mode_set(mode='OBJECT')

def extrude_faces(obj_name, faces_indices=None, translate=(0, 0, 1)):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid mesh object"}

    _enter_edit_mode(obj)
    bpy.ops.mesh.select_all(action='DESELECT')

    # Selection in edit mode
    _exit_edit_mode()
    if faces_indices:
        for i in faces_indices:
            obj.data.polygons[i].select = True
    else:
        # If no indices, we might want to extrude what is already selected or all
        pass

    _enter_edit_mode(obj)
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": translate})
    _exit_edit_mode()
    return {"status": "success"}

def inset_faces(obj_name, faces_indices=None, thickness=0.01, depth=0.0):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}

    _enter_edit_mode(obj)
    bpy.ops.mesh.select_all(action='DESELECT')
    _exit_edit_mode()

    if faces_indices:
        for i in faces_indices:
            obj.data.polygons[i].select = True

    _enter_edit_mode(obj)
    bpy.ops.mesh.inset(thickness=thickness, depth=depth)
    _exit_edit_mode()
    return {"status": "success"}

def loop_cut(obj_name, number_cuts=1, edge_index=0):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}

    _enter_edit_mode(obj)
    # loopcut_slide is context sensitive. Usually requires a window/area override in complex scripts
    # but for simple meshes it might work if the active edge is set.
    try:
        bpy.ops.mesh.loopcut_slide(
            MESH_OT_loopcut={"number_cuts": number_cuts, "object_index": 0, "edge_index": edge_index}
        )
        _exit_edit_mode()
        return {"status": "success"}
    except Exception as e:
        _exit_edit_mode()
        return {"status": "error", "message": str(e)}

def bridge_edge_loops(obj_name, edge_indices=None):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}

    _enter_edit_mode(obj)
    bpy.ops.mesh.select_all(action='DESELECT')
    _exit_edit_mode()

    if edge_indices:
        for i in edge_indices:
            obj.data.edges[i].select = True

    _enter_edit_mode(obj)
    bpy.ops.mesh.bridge_edge_loops()
    _exit_edit_mode()
    return {"status": "success"}

def boolean_cut(obj_name, cutter_name, apply=True):
    obj = _get_obj(obj_name)
    cutter = _get_obj(cutter_name)
    if not obj or not cutter: return {"status": "error", "message": "Object or cutter not found"}

    mod = obj.modifiers.new(name="Cut", type='BOOLEAN')
    mod.object = cutter
    mod.operation = 'DIFFERENCE'

    if apply:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
        # Usually we want to hide or delete the cutter after
        cutter.hide_viewport = True
        cutter.hide_render = True

    return {"status": "success"}

def spin_mesh(obj_name, steps=16, angle=360.0, axis=(0,0,1), center=(0,0,0)):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}

    _enter_edit_mode(obj)
    bpy.ops.mesh.spin(steps=steps, angle=math.radians(angle), axis=axis, center=center)
    _exit_edit_mode()
    return {"status": "success"}

def add_bezier_curve(name="Curve", points=None):
    curve_data = bpy.data.curves.new(name, type='CURVE')
    curve_data.dimensions = '3D'

    spline = curve_data.splines.new('BEZIER')
    if points:
        spline.bezier_points.add(len(points) - 1)
        for i, p in enumerate(points):
            spline.bezier_points[i].co = p
            spline.bezier_points[i].handle_left = (p[0]-1, p[1], p[2])
            spline.bezier_points[i].handle_right = (p[0]+1, p[1], p[2])

    obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(obj)
    return {"status": "success", "name": obj.name}

def set_curve_bevel(name, depth=0.1, resolution=4):
    obj = _get_obj(name)
    if not obj or obj.type != 'CURVE': return {"status": "error"}
    obj.data.bevel_depth = depth
    obj.data.bevel_resolution = resolution
    return {"status": "success"}

def convert_curve_to_mesh(name):
    obj = _get_obj(name)
    if not obj or obj.type != 'CURVE': return {"status": "error"}

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    return {"status": "success"}

def knife_project(obj_name, cutter_name):
    obj = _get_obj(obj_name)
    cutter = _get_obj(cutter_name)
    if not obj or not cutter: return {"status": "error"}

    bpy.ops.object.select_all(action='DESELECT')
    cutter.select_set(True)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Knife project requires EDIT mode on the target object and SELECTION of the cutter
    _enter_edit_mode(obj)
    # This might fail in headless or if view is not aligned, but standard in Blender scripts
    try:
        bpy.ops.mesh.knife_project()
        _exit_edit_mode()
        return {"status": "success"}
    except Exception as e:
        _exit_edit_mode()
        return {"status": "error", "message": str(e)}

def bisect_mesh(obj_name, plane_co=(0,0,0), plane_no=(0,0,1), clear_inner=False, clear_outer=False):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}

    _enter_edit_mode(obj)
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bisect(plane_co=plane_co, plane_no=plane_no, clear_inner=clear_inner, clear_outer=clear_outer)
    _exit_edit_mode()
    return {"status": "success"}

def add_nurbs_path(name="Path", points=None):
    curve_data = bpy.data.curves.new(name, type='CURVE')
    curve_data.dimensions = '3D'

    spline = curve_data.splines.new('NURBS')
    if points:
        spline.points.add(len(points) - 1)
        for i, p in enumerate(points):
            # NURBS points are 4D (x, y, z, w)
            spline.points[i].co = (p[0], p[1], p[2], 1.0)

    spline.use_endpoint_u = True

    obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(obj)
    return {"status": "success", "name": obj.name}

def screw_mesh(obj_name, steps=16, angle=360.0, axis=(0,0,1), center=(0,0,0), screw_dist=1.0):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}

    _enter_edit_mode(obj)
    bpy.ops.mesh.screw(steps=steps, angle=math.radians(angle), axis=axis, center=center, screw=screw_dist)
    _exit_edit_mode()
    return {"status": "success"}

def edge_split(obj_name, angle=30.0):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="EdgeSplit", type='EDGE_SPLIT')
    mod.split_angle = math.radians(angle)
    return {"status": "success", "name": mod.name}

def add_lattice(name="Lattice", location=(0,0,0), scale=(1,1,1), u=2, v=2, w=2):
    lat_data = bpy.data.lattices.new(name)
    lat_data.points_u = u
    lat_data.points_v = v
    lat_data.points_w = w

    obj = bpy.data.objects.new(name, lat_data)
    obj.location = location
    obj.scale = scale
    bpy.context.collection.objects.link(obj)
    return {"status": "success", "name": obj.name}

def apply_lattice_modifier(obj_name, lattice_name):
    obj = _get_obj(obj_name)
    lat = _get_obj(lattice_name)
    if not obj or not lat: return {"status": "error"}

    mod = obj.modifiers.new(name="Lattice", type='LATTICE')
    mod.object = lat
    return {"status": "success"}

def set_curve_extrude(name, extrude=0.1):
    obj = _get_obj(name)
    if not obj or obj.type != 'CURVE': return {"status": "error"}
    obj.data.extrude = extrude
    return {"status": "success"}

def extrude_selected_faces(obj_name):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid mesh object"}
    _enter_edit_mode(obj)
    bpy.ops.mesh.extrude_region_move()
    _exit_edit_mode()
    return {"status": "success"}

def inset_selected_faces(obj_name, thickness=0.01, depth=0.0):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}
    _enter_edit_mode(obj)
    bpy.ops.mesh.inset(thickness=thickness, depth=depth)
    _exit_edit_mode()
    return {"status": "success"}

def bevel_selected_edges(obj_name, offset=0.1, segments=3):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}
    _enter_edit_mode(obj)
    bpy.ops.mesh.bevel(offset=offset, segments=segments)
    _exit_edit_mode()
    return {"status": "success"}

def add_loop_cut_slide(obj_name, number_cuts=1, edge_index=0):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}
    _enter_edit_mode(obj)
    try:
        bpy.ops.mesh.loopcut_slide(
            MESH_OT_loopcut={"number_cuts": number_cuts, "object_index": 0, "edge_index": edge_index}
        )
        _exit_edit_mode()
        return {"status": "success"}
    except Exception as e:
        _exit_edit_mode()
        return {"status": "error", "message": str(e)}

def spin_selected_region(obj_name, steps=16, angle=360.0, axis=(0,0,1), center=(0,0,0)):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}
    _enter_edit_mode(obj)
    bpy.ops.mesh.spin(steps=steps, angle=math.radians(angle), axis=axis, center=center)
    _exit_edit_mode()
    return {"status": "success"}

def knife_project_cut(obj_name, cutter_name, cut_through=False):
    obj = _get_obj(obj_name)
    cutter = _get_obj(cutter_name)
    if not obj or not cutter: return {"status": "error"}

    bpy.ops.object.select_all(action='DESELECT')
    cutter.select_set(True)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    _enter_edit_mode(obj)
    try:
        bpy.ops.mesh.knife_project(cut_through=cut_through)
        _exit_edit_mode()
        return {"status": "success"}
    except Exception as e:
        _exit_edit_mode()
        return {"status": "error", "message": str(e)}

def separate_mesh_selection(obj_name, type='SELECTED'):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}
    _enter_edit_mode(obj)
    bpy.ops.mesh.separate(type=type)
    _exit_edit_mode()
    return {"status": "success"}

def symmetrize_mesh(obj_name, direction='NEGATIVE_X'):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}
    _enter_edit_mode(obj)
    bpy.ops.mesh.symmetrize(direction=direction)
    _exit_edit_mode()
    return {"status": "success"}

def fill_holes(obj_name, sides=4):
    obj = _get_obj(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}
    _enter_edit_mode(obj)
    bpy.ops.mesh.fill_holes(sides=sides)
    _exit_edit_mode()
    return {"status": "success"}

def apply_simple_deform_bend(obj_name, angle=45.0, axis='Z'):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Bend", type='SIMPLE_DEFORM')
    mod.deform_method = 'BEND'
    mod.angle = math.radians(angle)
    mod.deform_axis = axis

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    return {"status": "success"}

def apply_lattice_deform(obj_name, lattice_name):
    obj = _get_obj(obj_name)
    lat = _get_obj(lattice_name)
    if not obj or not lat: return {"status": "error"}

    mod = obj.modifiers.new(name="Lattice", type='LATTICE')
    mod.object = lat

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    return {"status": "success"}

def create_loft_curve(name, points_list, bridge=True):
    curve_data = bpy.data.curves.new(name, type='CURVE')
    curve_data.dimensions = '3D'

    for points in points_list:
        spline = curve_data.splines.new('BEZIER')
        spline.bezier_points.add(len(points) - 1)
        for i, p in enumerate(points):
            spline.bezier_points[i].co = p
            spline.bezier_points[i].handle_left = (p[0]-0.1, p[1], p[2])
            spline.bezier_points[i].handle_right = (p[0]+0.1, p[1], p[2])

    obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(obj)

    if bridge:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.ops.object.convert(target='MESH')
        _enter_edit_mode(obj)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.bridge_edge_loops()
        _exit_edit_mode()

    return {"status": "success", "name": obj.name}

def bend_mesh_along_curve(obj_name, curve_name, deform_axis='POS_X'):
    obj = _get_obj(obj_name)
    curve = _get_obj(curve_name)
    if not obj or not curve: return {"status": "error"}

    mod = obj.modifiers.new(name="CurveDeform", type='CURVE')
    mod.object = curve
    mod.deform_axis = deform_axis

    return {"status": "success", "name": mod.name}
