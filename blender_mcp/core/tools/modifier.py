import bpy
import math

def add_modifier(name, type="SUBSURF", **kwargs):
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"status": "error", "message": f"Object {name} not found"}

    mod = obj.modifiers.new(name="MCP_Modifier", type=type)
    for key, value in kwargs.items():
        if hasattr(mod, key):
            setattr(mod, key, value)
    return {"status": "success", "modifier": mod.name}

def remove_modifier(obj_name, mod_name):
    obj = bpy.data.objects.get(obj_name)
    mod = obj.modifiers.get(mod_name)
    if obj and mod:
        obj.modifiers.remove(mod)
        return {"status": "success"}
    return {"status": "error"}

def apply_modifier(obj_name, mod_name):
    obj = bpy.data.objects.get(obj_name)
    if obj:
        bpy.context.view_layer.objects.active = obj
        try:
            bpy.ops.object.modifier_apply(modifier=mod_name)
            return {"status": "success"}
        except: return {"status": "error"}
    return {"status": "error"}

def add_subsurf_modifier(name, levels=1, render_levels=2):
    return add_modifier(name, type='SUBSURF', levels=levels, render_levels=render_levels)

def add_solidify_modifier(name, thickness=0.01):
    return add_modifier(name, type='SOLIDIFY', thickness=thickness)

def add_bevel_modifier(name, width=0.1, segments=3):
    return add_modifier(name, type='BEVEL', width=width, segments=segments)

def add_boolean_modifier(name, target, operation='DIFFERENCE'):
    target_obj = bpy.data.objects.get(target)
    return add_modifier(name, type='BOOLEAN', object=target_obj, operation=operation)

def add_array_modifier(name, count=2, offset=(1.0, 0.0, 0.0)):
    return add_modifier(name, type='ARRAY', count=count, use_relative_offset=True, relative_offset_displace=offset)

def add_mirror_modifier(name, use_axis=(True, False, False)):
    return add_modifier(name, type='MIRROR', use_axis=use_axis)

def add_decimate_modifier(name, ratio=0.5):
    return add_modifier(name, type='DECIMATE', ratio=ratio)

def add_displace_modifier(name, strength=1.0):
    return add_modifier(name, type='DISPLACE', strength=strength)

def add_mask_modifier(name):
    return add_modifier(name, type='MASK')

def add_multires_modifier(name):
    return add_modifier(name, type='MULTIRES')

def add_remesh_modifier(name, voxel_size=0.1):
    return add_modifier(name, type='REMESH', voxel_size=voxel_size)

def add_screw_modifier(name, angle=360, steps=16):
    return add_modifier(name, type='SCREW', angle=math.radians(angle), steps=steps)

def add_skin_modifier(name):
    return add_modifier(name, type='SKIN')

def add_triangulate_modifier(name):
    return add_modifier(name, type='TRIANGULATE')

def add_wireframe_modifier(name, thickness=0.02):
    return add_modifier(name, type='WIREFRAME', thickness=thickness)

def add_simple_deform_modifier(name, deform_type='BEND', angle=45):
    return add_modifier(name, type='SIMPLE_DEFORM', deform_method=deform_type, angle=math.radians(angle))

def add_lattice_modifier(name, lattice):
    lattice_obj = bpy.data.objects.get(lattice)
    return add_modifier(name, type='LATTICE', object=lattice_obj)

def add_shrinkwrap_modifier(name, target):
    target_obj = bpy.data.objects.get(target)
    return add_modifier(name, type='SHRINKWRAP', target=target_obj)

def add_data_transfer_modifier(name, target):
    target_obj = bpy.data.objects.get(target)
    return add_modifier(name, type='DATA_TRANSFER', object=target_obj)

def add_weighted_normal_modifier(name):
    return add_modifier(name, type='WEIGHTED_NORMAL')
