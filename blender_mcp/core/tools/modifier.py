import bpy

def _get_obj(name):
    return bpy.data.objects.get(name)

def add_modifier(obj_name, type, name=None):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name=name or type, type=type)
    return {"status": "success", "name": mod.name}

def remove_modifier(obj_name, mod_name):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.get(mod_name)
    if mod:
        obj.modifiers.remove(mod)
        return {"status": "success"}
    return {"status": "error"}

def apply_modifier(obj_name, mod_name):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    bpy.context.view_layer.objects.active = obj
    try:
        bpy.ops.object.modifier_apply(modifier=mod_name)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Specialized modifiers
def add_subsurf_modifier(obj_name, levels=1, render_levels=2):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    mod.levels = levels
    mod.render_levels = render_levels
    return {"status": "success", "name": mod.name}

def add_boolean_modifier(obj_name, target_name, operation='DIFFERENCE'):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error"}
    mod = obj.modifiers.new(name="Boolean", type='BOOLEAN')
    mod.object = target
    mod.operation = operation
    return {"status": "success", "name": mod.name}

def add_array_modifier(obj_name, count=2, offset=(1.0, 0.0, 0.0)):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Array", type='ARRAY')
    mod.count = count
    mod.use_relative_offset = True
    mod.relative_offset_displace = offset
    return {"status": "success", "name": mod.name}

def add_mirror_modifier(obj_name, use_x=True, use_y=False, use_z=False):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Mirror", type='MIRROR')
    mod.use_axis[0] = use_x
    mod.use_axis[1] = use_y
    mod.use_axis[2] = use_z
    return {"status": "success", "name": mod.name}

def add_bevel_modifier(obj_name, width=0.1, segments=3):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod.width = width
    mod.segments = segments
    return {"status": "success", "name": mod.name}

def add_solidify_modifier(obj_name, thickness=0.1):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod.thickness = thickness
    return {"status": "success", "name": mod.name}

def add_displace_modifier(obj_name, texture_name=None, strength=1.0):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Displace", type='DISPLACE')
    if texture_name:
        tex = bpy.data.textures.get(texture_name)
        if tex: mod.texture = tex
    mod.strength = strength
    return {"status": "success", "name": mod.name}

def add_simple_deform_modifier(obj_name, type='BEND', angle=45.0):
    import math
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="SimpleDeform", type='SIMPLE_DEFORM')
    mod.deform_method = type
    mod.angle = math.radians(angle)
    return {"status": "success", "name": mod.name}

def add_decimate_modifier(obj_name, ratio=0.5):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
    mod.ratio = ratio
    return {"status": "success", "name": mod.name}

def add_multires_modifier(obj_name):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Multires", type='MULTIRES')
    return {"status": "success", "name": mod.name}

def add_remesh_modifier(obj_name, voxel_size=0.1):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Remesh", type='REMESH')
    mod.voxel_size = voxel_size
    return {"status": "success", "name": mod.name}

def add_screw_modifier(obj_name, angle=360, steps=16):
    import math
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Screw", type='SCREW')
    mod.angle = math.radians(angle)
    mod.steps = steps
    return {"status": "success", "name": mod.name}

def add_skin_modifier(obj_name):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Skin", type='SKIN')
    return {"status": "success", "name": mod.name}

def add_triangulate_modifier(obj_name):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Triangulate", type='TRIANGULATE')
    return {"status": "success", "name": mod.name}

def add_wireframe_modifier(obj_name, thickness=0.01):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Wireframe", type='WIREFRAME')
    mod.thickness = thickness
    return {"status": "success", "name": mod.name}

def add_curve_modifier(obj_name, target_name):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error"}
    mod = obj.modifiers.new(name="Curve", type='CURVE')
    mod.object = target
    return {"status": "success", "name": mod.name}

def add_warp_modifier(obj_name, object_from, object_to):
    obj = _get_obj(obj_name)
    from_obj = _get_obj(object_from)
    to_obj = _get_obj(object_to)
    if not obj or not from_obj or not to_obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Warp", type='WARP')
    mod.object_from = from_obj
    mod.object_to = to_obj
    return {"status": "success", "name": mod.name}

def add_wave_modifier(obj_name, height=0.5, width=1.5):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Wave", type='WAVE')
    mod.height = height
    mod.width = width
    return {"status": "success", "name": mod.name}

def add_cast_modifier(obj_name, type='SPHERE', factor=0.5):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Cast", type='CAST')
    mod.cast_type = type
    mod.factor = factor
    return {"status": "success", "name": mod.name}

def add_surface_deform_modifier(obj_name, target_name):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error"}
    mod = obj.modifiers.new(name="SurfaceDeform", type='SURFACE_DEFORM')
    mod.target = target
    return {"status": "success", "name": mod.name}

def add_mesh_deform_modifier(obj_name, target_name):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error"}
    mod = obj.modifiers.new(name="MeshDeform", type='MESH_DEFORM')
    mod.object = target
    return {"status": "success", "name": mod.name}

def add_smooth_corrective_modifier(obj_name, factor=0.5, iterations=5):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="SmoothCorrective", type='CORRECTIVE_SMOOTH')
    mod.factor = factor
    mod.iterations = iterations
    return {"status": "success", "name": mod.name}

def add_laplacian_smooth_modifier(obj_name, lambda_factor=0.01, iterations=5):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="LaplacianSmooth", type='LAPLACIANSMOOTH')
    mod.lambda_factor = lambda_factor
    mod.iterations = iterations
    return {"status": "success", "name": mod.name}

def add_hook_modifier(obj_name, target_name):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error"}
    mod = obj.modifiers.new(name="Hook", type='HOOK')
    mod.object = target
    return {"status": "success", "name": mod.name}

def add_lattice_modifier(obj_name, target_name):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error"}
    mod = obj.modifiers.new(name="Lattice", type='LATTICE')
    mod.object = target
    return {"status": "success", "name": mod.name}

def add_shrinkwrap_modifier(obj_name, target_name):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error"}
    mod = obj.modifiers.new(name="Shrinkwrap", type='SHRINKWRAP')
    mod.target = target
    return {"status": "success", "name": mod.name}

def add_data_transfer_modifier(obj_name, target_name):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error"}
    mod = obj.modifiers.new(name="DataTransfer", type='DATA_TRANSFER')
    mod.object = target
    return {"status": "success", "name": mod.name}

def add_weighted_normal_modifier(obj_name):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="WeightedNormal", type='WEIGHTED_NORMAL')
    return {"status": "success", "name": mod.name}

def add_mask_modifier(obj_name):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    mod = obj.modifiers.new(name="Mask", type='MASK')
    return {"status": "success", "name": mod.name}

def apply_boolean_difference(obj_name, target_name):
    res = add_boolean_modifier(obj_name, target_name, operation='DIFFERENCE')
    if res["status"] == "success":
        return apply_modifier(obj_name, res["name"])
    return res

def apply_boolean_slice(obj_name, target_name):
    obj = bpy.data.objects.get(obj_name)
    target = bpy.data.objects.get(target_name)
    if not obj or not target: return {"status": "error", "message": "Invalid objects"}

    # Duplicate original
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.duplicate()
    slice_obj = bpy.context.active_object
    slice_obj.name = f"{obj.name}_slice"

    # Intersect on slice
    mod_int = slice_obj.modifiers.new(name="Boolean_Slice", type='BOOLEAN')
    mod_int.object = target
    mod_int.operation = 'INTERSECT'
    bpy.ops.object.modifier_apply(modifier=mod_int.name)

    # Difference on original
    mod_diff = obj.modifiers.new(name="Boolean_Difference", type='BOOLEAN')
    mod_diff.object = target
    mod_diff.operation = 'DIFFERENCE'
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod_diff.name)

    return {"status": "success", "original": obj.name, "slice": slice_obj.name}
