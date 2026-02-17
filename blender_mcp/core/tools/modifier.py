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

def add_simple_deform_modifier(name, deform_type='BEND', angle=45, axis='Z', origin=None, limits=(0, 1), vertex_group=""):
    origin_obj = bpy.data.objects.get(origin) if origin else None
    return add_modifier(name, type='SIMPLE_DEFORM',
                        deform_method=deform_type,
                        angle=math.radians(angle),
                        deform_axis=axis,
                        origin=origin_obj,
                        limits=limits,
                        vertex_group=vertex_group)

def add_curve_modifier(name, curve_object, axis='POS_X'):
    curve_obj = bpy.data.objects.get(curve_object)
    return add_modifier(name, type='CURVE', object=curve_obj, deform_axis=axis)

def add_warp_modifier(name, object_from, object_to, strength=1.0):
    obj_from = bpy.data.objects.get(object_from)
    obj_to = bpy.data.objects.get(object_to)
    return add_modifier(name, type='WARP', object_from=obj_from, object_to=obj_to, strength=strength)

def add_wave_modifier(name, motion='X', speed=0.25, height=0.5, width=1.5, narrowness=1.5):
    use_x = 'X' in motion
    use_y = 'Y' in motion
    return add_modifier(name, type='WAVE', use_x=use_x, use_y=use_y, speed=speed, height=height, width=width, narrowness=narrowness)

def add_cast_modifier(name, cast_type='SPHERE', factor=0.5, radius=0.0):
    return add_modifier(name, type='CAST', cast_type=cast_type, factor=factor, radius=radius)

def add_surface_deform_modifier(name, target):
    target_obj = bpy.data.objects.get(target)
    return add_modifier(name, type='SURFACE_DEFORM', target=target_obj)

def add_mesh_deform_modifier(name, target, precision=5):
    target_obj = bpy.data.objects.get(target)
    return add_modifier(name, type='MESH_DEFORM', object=target_obj, precision=precision)

def add_smooth_corrective_modifier(name, factor=1.0, repeat=5):
    return add_modifier(name, type='CORRECTIVE_SMOOTH', factor=factor, iterations=repeat)

def add_laplacian_smooth_modifier(name, lambda_factor=0.5, repeat=1):
    return add_modifier(name, type='LAPLACIANSMOOTH', lambda_factor=lambda_factor, iterations=repeat)

def add_hook_modifier(name, object_hook):
    hook_obj = bpy.data.objects.get(object_hook)
    return add_modifier(name, type='HOOK', object=hook_obj)

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
