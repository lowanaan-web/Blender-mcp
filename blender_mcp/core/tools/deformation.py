import bpy
import math

def apply_simple_deform_bend(obj_name, angle=45.0, axis='Z'):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return {"status": "error", "message": f"Object {obj_name} not found"}

    mod = obj.modifiers.new(name="SimpleDeform_Bend", type='SIMPLE_DEFORM')
    mod.deform_method = 'BEND'
    mod.angle = math.radians(angle)
    mod.deform_axis = axis

    bpy.context.view_layer.objects.active = obj
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def apply_lattice_deform(obj_name, lattice_name):
    obj = bpy.data.objects.get(obj_name)
    lattice = bpy.data.objects.get(lattice_name)
    if not obj: return {"status": "error", "message": f"Object {obj_name} not found"}
    if not lattice or lattice.type != 'LATTICE':
        return {"status": "error", "message": f"Lattice {lattice_name} not found or invalid"}

    mod = obj.modifiers.new(name="LatticeDeform", type='LATTICE')
    mod.object = lattice

    bpy.context.view_layer.objects.active = obj
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_loft_curve(curve_names, name="LoftMesh"):
    objs = [bpy.data.objects.get(n) for n in curve_names if bpy.data.objects.get(n)]
    if not objs: return {"status": "error", "message": "No valid curves found"}

    bpy.ops.object.select_all(action='DESELECT')
    for obj in objs:
        obj.select_set(True)

    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.duplicate()

    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.join()

    loft_obj = bpy.context.active_object
    loft_obj.name = name

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    try:
        bpy.ops.mesh.bridge_edge_loops()
    except Exception as e:
        bpy.ops.object.mode_set(mode='OBJECT')
        return {"status": "error", "message": f"Bridge failed: {str(e)}"}

    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success", "name": loft_obj.name}

def bend_mesh_along_curve(obj_name, curve_name, axis='POS_X'):
    obj = bpy.data.objects.get(obj_name)
    curve = bpy.data.objects.get(curve_name)
    if not obj: return {"status": "error", "message": f"Object {obj_name} not found"}
    if not curve or curve.type != 'CURVE':
        return {"status": "error", "message": f"Curve {curve_name} not found or invalid"}

    mod = obj.modifiers.new(name="CurveDeform", type='CURVE')
    mod.object = curve
    mod.deform_axis = axis

    bpy.context.view_layer.objects.active = obj
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
