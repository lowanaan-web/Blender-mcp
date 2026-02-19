import bpy

def add_torus(location=(0,0,0), name="Torus"):
    bpy.ops.mesh.primitive_torus_add(location=location)
    bpy.context.active_object.name = name
    return {"status": "success"}

def add_monkey(location=(0,0,0), name="Suzanne"):
    bpy.ops.mesh.primitive_monkey_add(location=location)
    bpy.context.active_object.name = name
    return {"status": "success"}

def add_icosphere(location=(0,0,0), subdivisions=2, name="IcoSphere"):
    bpy.ops.mesh.primitive_ico_sphere_add(location=location, subdivisions=subdivisions)
    bpy.context.active_object.name = name
    return {"status": "success"}

def subdivide_mesh(name, cuts=1):
    obj = bpy.data.objects.get(name)
    if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid object"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=cuts)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}

def shade_smooth(name, smooth=True):
    obj = bpy.data.objects.get(name)
    if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid object"}
    if smooth:
        bpy.ops.object.shade_smooth({"selected_editable_objects": [obj]})
    else:
        bpy.ops.object.shade_flat({"selected_editable_objects": [obj]})
    return {"status": "success"}

def extrude_selected_faces(obj_name, value=(0, 0, 1)):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid object"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": value})
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}

def inset_selected_faces(obj_name, thickness=0.01, depth=0.0):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid object"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.inset(thickness=thickness, depth=depth)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}

def bevel_selected_edges(obj_name, offset=0.1, segments=3):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid object"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.bevel(offset=offset, segments=segments)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}

def add_loop_cut_slide(obj_name, number_cuts=1):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid object"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    try:
        bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts": number_cuts})
    except Exception as e:
        bpy.ops.object.mode_set(mode='OBJECT')
        return {"status": "error", "message": str(e)}
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}

def bridge_edge_loops(obj_name):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid object"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.bridge_edge_loops()
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}

def spin_selected_region(obj_name, steps=12, angle=90.0, axis=(0, 0, 1)):
    import math
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid object"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.spin(steps=steps, angle=math.radians(angle), axis=axis)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}

def knife_project_cut(target_name, knife_names):
    target = bpy.data.objects.get(target_name)
    if not target or target.type != 'MESH': return {"status": "error", "message": "Invalid target object"}

    bpy.ops.object.select_all(action='DESELECT')
    for kname in knife_names:
        kobj = bpy.data.objects.get(kname)
        if kobj: kobj.select_set(True)

    bpy.context.view_layer.objects.active = target
    bpy.ops.object.mode_set(mode='EDIT')
    try:
        bpy.ops.mesh.knife_project()
    except Exception as e:
        bpy.ops.object.mode_set(mode='OBJECT')
        return {"status": "error", "message": str(e)}
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}

def fill_holes(obj_name, sides=4):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid object"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.fill_holes(sides=sides)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}

def separate_mesh_selection(obj_name, type='SELECTED'):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid object"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.separate(type=type)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}

def symmetrize_mesh(obj_name, direction='NEGATIVE_X'):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid object"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.symmetrize(direction=direction)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}
