import bpy

def _get_obj(name):
    return bpy.data.objects.get(name)

def set_sculpt_mode(obj_name, enter=True):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error", "message": f"Object {obj_name} not found"}
    bpy.context.view_layer.objects.active = obj
    if enter:
        if obj.mode != 'SCULPT':
            bpy.ops.object.mode_set(mode='SCULPT')
    else:
        if obj.mode == 'SCULPT':
            bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}

def select_brush(brush_name):
    # Standard brushes in 4.x/5.x are often accessed via context.tool_settings.sculpt.brush
    brush = bpy.data.brushes.get(brush_name)
    if not brush: return {"status": "error", "message": f"Brush {brush_name} not found"}
    bpy.context.tool_settings.sculpt.brush = brush
    return {"status": "success"}

def set_brush_property(size=None, strength=None, hardness=None, use_autosmooth=None, autosmooth_factor=0.0):
    brush = bpy.context.tool_settings.sculpt.brush
    if not brush: return {"status": "error", "message": "No active brush"}
    if size is not None: brush.size = size
    if strength is not None: brush.strength = strength
    if hardness is not None: brush.hardness = hardness
    if use_autosmooth is not None:
        brush.use_autosmooth = use_autosmooth
        brush.autosmooth_factor = autosmooth_factor
    return {"status": "success"}

def set_stroke_method(method='SPACE', spacing=10):
    brush = bpy.context.tool_settings.sculpt.brush
    if not brush: return {"status": "error"}
    brush.stroke_method = method
    brush.spacing = spacing
    return {"status": "success"}

def toggle_dyntopo(enable=True):
    obj = bpy.context.sculpt_object
    if not obj: return {"status": "error", "message": "No sculpt object"}
    if enable != obj.use_dynamic_topology_sculpting:
        bpy.ops.sculpt.dynamic_topology_toggle()
    return {"status": "success"}

def set_dyntopo_detail(method='RELATIVE', detail=12.0):
    settings = bpy.context.scene.tool_settings.sculpt
    settings.detail_type_method = method
    if method == 'RELATIVE': settings.detail_size = detail
    elif method == 'CONSTANT': settings.constant_detail_resolution = detail
    elif method == 'BRUSH': settings.detail_percent = detail
    return {"status": "success"}

def set_dyntopo_refine_mode(mode='SUBDIVIDE_COLLAPSE'):
    # mode: 'SUBDIVIDE_COLLAPSE', 'COLLAPSE_ONLY', 'SUBDIVIDE_ONLY'
    bpy.context.scene.tool_settings.sculpt.dyntopo_refine_mode = mode
    return {"status": "success"}

def voxel_remesh(obj_name, voxel_size=0.1, adaptivity=0.0):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    obj.data.remesh_voxel_size = voxel_size
    obj.data.remesh_adaptivity = adaptivity
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.voxel_remesh()
    return {"status": "success"}

def mask_all():
    bpy.ops.paint.mask_flood_fill(mode='VALUE', value=1.0)
    return {"status": "success"}

def clear_mask():
    bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0.0)
    return {"status": "success"}

def invert_mask():
    bpy.ops.paint.mask_flood_fill(mode='INVERT')
    return {"status": "success"}

def smooth_mask(iterations=1):
    for _ in range(iterations):
        bpy.ops.paint.mask_flood_fill(mode='SMOOTH')
    return {"status": "success"}

def sharpen_mask(iterations=1):
    for _ in range(iterations):
        bpy.ops.paint.mask_flood_fill(mode='SHARPEN')
    return {"status": "success"}

def grow_mask():
    bpy.ops.paint.mask_flood_fill(mode='GROW')
    return {"status": "success"}

def shrink_mask():
    bpy.ops.paint.mask_flood_fill(mode='SHRINK')
    return {"status": "success"}

def dirty_mask(blur_steps=1, iterations=1):
    bpy.ops.sculpt.dirty_mask(blur_steps=blur_steps, iterations=iterations)
    return {"status": "success"}

def create_face_set_from_masked():
    bpy.ops.sculpt.face_set_from_masked()
    return {"status": "success"}

def create_face_set_from_visible():
    bpy.ops.sculpt.face_set_from_visible()
    return {"status": "success"}

def invert_face_sets():
    bpy.ops.sculpt.face_sets_invert()
    return {"status": "success"}

def hide_active_face_set():
    bpy.ops.sculpt.face_set_change_visibility(mode='HIDE_ACTIVE')
    return {"status": "success"}

def reveal_all_face_sets():
    bpy.ops.sculpt.face_set_change_visibility(mode='REVEAL_ALL')
    return {"status": "success"}

def set_sculpt_symmetry(use_x=True, use_y=False, use_z=False):
    settings = bpy.context.tool_settings.sculpt
    settings.use_symmetry_x = use_x
    settings.use_symmetry_y = use_y
    settings.use_symmetry_z = use_z
    return {"status": "success"}

def trim_box():
    # Note: Trim tools usually require interactive input in UI,
    # but we can configure the tool and then the agent might use it.
    # To be "real", we set the tool active.
    bpy.ops.wm.tool_set_by_id(name="builtin.box_trim")
    return {"status": "success"}

def trim_lasso():
    bpy.ops.wm.tool_set_by_id(name="builtin.lasso_trim")
    return {"status": "success"}

def apply_mesh_filter(type='INFLATE', strength=1.0):
    # type: 'SMOOTH', 'SCALE', 'INFLATE', 'SPHERE', 'RANDOM', 'RELAX', 'RELAX_FACE_SETS', 'SURFACE_SMOOTH', 'SHARPEN'
    bpy.ops.sculpt.mesh_filter(type=type, strength=strength)
    return {"status": "success"}

def subdivide_multires(obj_name):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    bpy.context.view_layer.objects.active = obj
    # Find multires modifier or add it
    mod = next((m for m in obj.modifiers if m.type == 'MULTIRES'), None)
    if not mod:
        mod = obj.modifiers.new(name="Multires", type='MULTIRES')
    bpy.ops.object.multires_subdivide(modifier=mod.name)
    return {"status": "success"}

def multires_reshape(obj_name, modifier_name):
    bpy.ops.object.multires_reshape(modifier=modifier_name)
    return {"status": "success"}

def set_steady_stroke(enable=True, radius=20, strength=0.5):
    brush = bpy.context.tool_settings.sculpt.brush
    if not brush: return {"status": "error"}
    brush.use_steady_stroke = enable
    brush.steady_stroke_radius = radius
    brush.steady_stroke_factor = strength
    return {"status": "success"}

def optimize_sculpt_mesh():
    bpy.ops.sculpt.optimize()
    return {"status": "success"}

def get_sculpt_stats(obj_name):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    return {
        "status": "success",
        "vertex_count": len(obj.data.vertices),
        "face_count": len(obj.data.polygons),
        "is_dyntopo": obj.use_dynamic_topology_sculpting if hasattr(obj, 'use_dynamic_topology_sculpting') else False
    }

def set_brush_falloff(shape='SMOOTH'):
    brush = bpy.context.tool_settings.sculpt.brush
    if brush:
        brush.falloff_shape = shape
        return {"status": "success"}
    return {"status": "error"}

def set_sculpt_vertex_color(color=(1,1,1,1)):
    # For Sculpt Vertex Color (4.0+ style)
    brush = bpy.context.tool_settings.sculpt.brush
    if brush:
        brush.color = color[:3]
        return {"status": "success"}
    return {"status": "error"}
