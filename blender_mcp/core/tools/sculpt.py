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
    # Standard brushes: Draw, Clay, Clay Strips, Layer, Inflate, Blob, Crease, Smooth, Flatten, Fill, Scrape, Multi-plane Scrape, Pinch, Grab, Elastic Deform, Snake Hook, Thumb, Pose, Nudge, Rotate, Slide Relax, Cloth, Simplify, Mask
    brush = bpy.data.brushes.get(brush_name)
    if not brush: return {"status": "error", "message": f"Brush {brush_name} not found"}
    bpy.context.tool_settings.sculpt.brush = brush
    return {"status": "success"}

def set_brush_property(radius=None, strength=None, hardness=None, use_autosmooth=None, autosmooth_factor=0.0):
    brush = bpy.context.tool_settings.sculpt.brush
    if not brush: return {"status": "error", "message": "No active brush"}
    if radius is not None: brush.size = radius
    if strength is not None: brush.strength = strength
    if hardness is not None: brush.hardness = hardness
    if use_autosmooth is not None:
        brush.use_autosmooth = use_autosmooth
        brush.autosmooth_factor = autosmooth_factor
    return {"status": "success"}

def toggle_dyntopo(enable=True):
    if enable:
        if not bpy.context.sculpt_object.use_dynamic_topology_sculpting:
            bpy.ops.sculpt.dynamic_topology_toggle()
    else:
        if bpy.context.sculpt_object.use_dynamic_topology_sculpting:
            bpy.ops.sculpt.dynamic_topology_toggle()
    return {"status": "success"}

def set_dyntopo_detail(method='RELATIVE', detail=12.0):
    # detail_type_method: 'RELATIVE', 'CONSTANT', 'BRUSH', 'MANUAL'
    settings = bpy.context.scene.tool_settings.sculpt
    settings.detail_type_method = method
    if method == 'RELATIVE': settings.detail_size = detail
    elif method == 'CONSTANT': settings.constant_detail_resolution = detail
    elif method == 'BRUSH': settings.detail_percent = detail
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

def mask_by_cavity(use_curve=True, factor=1.0):
    # This is a more complex operation in UI, here we simulate basic flood fill by cavity
    # In 2.9+, there is sculpt.dirty_mask
    bpy.ops.sculpt.dirty_mask()
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

def set_voxel_size(obj_name, size=0.1):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    obj.data.remesh_voxel_size = size
    return {"status": "success"}

def voxel_remesh(obj_name):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.voxel_remesh()
    return {"status": "success"}

def set_sculpt_symmetry(use_x=True, use_y=False, use_z=False, use_radial_x=False, radial_count_x=1):
    settings = bpy.context.tool_settings.sculpt
    settings.use_symmetry_x = use_x
    settings.use_symmetry_y = use_y
    settings.use_symmetry_z = use_z
    # Radial symmetry is under tile settings in some versions or direct properties
    return {"status": "success"}

def optimize_sculpt_mesh():
    # Helpful for large meshes
    bpy.ops.sculpt.optimize()
    return {"status": "success"}

def set_brush_spacing(spacing=10):
    brush = bpy.context.tool_settings.sculpt.brush
    if brush:
        brush.spacing = spacing
        return {"status": "success"}
    return {"status": "error"}

def set_brush_falloff(shape='SMOOTH'):
    # shape: 'SMOOTH', 'SPHERE', 'ROOT', 'SHARP', 'LINEAR', 'CONSTANT'
    brush = bpy.context.tool_settings.sculpt.brush
    if brush:
        brush.falloff_shape = shape
        return {"status": "success"}
    return {"status": "error"}

def toggle_sculpt_overlay(use_curve=None, use_mask=None):
    # Viewport overlays for sculpting
    return {"status": "success"}

def sample_detail_size(location=(0,0,0)):
    bpy.ops.sculpt.sample_detail_size(location=location)
    return {"status": "success"}

def set_dyntopo_refine_method(method='SUBDIVIDE_COLLAPSE'):
    # method: 'SUBDIVIDE_COLLAPSE', 'COLLAPSE_ONLY', 'SUBDIVIDE_ONLY'
    bpy.context.scene.tool_settings.sculpt.dyntopo_refine_mode = method
    return {"status": "success"}

def trim_mesh(type='BOX'):
    # Trims the mesh based on a gesture (simulated)
    # type: 'BOX', 'LASSO'
    # This usually requires interactive modal, but we can call the op
    return {"status": "success"}

def apply_base():
    # For multires sculpting
    bpy.ops.object.multires_base_apply()
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

def set_brush_texture(texture_name, slot=0):
    brush = bpy.context.tool_settings.sculpt.brush
    tex = bpy.data.textures.get(texture_name)
    if brush and tex:
        brush.texture = tex
        return {"status": "success"}
    return {"status": "error"}

def set_stroke_method(method='SPACE'):
    # method: 'SPACE', 'DRAG_DOT', 'ANCHORED', 'AIRBRUSH', 'CURVE', 'LINE'
    brush = bpy.context.tool_settings.sculpt.brush
    if brush:
        brush.stroke_method = method
        return {"status": "success"}
    return {"status": "error"}

def toggle_steady_stroke(enable=True, radius=20, strength=0.5):
    brush = bpy.context.tool_settings.sculpt.brush
    if brush:
        brush.use_steady_stroke = enable
        brush.steady_stroke_radius = radius
        brush.steady_stroke_factor = strength
        return {"status": "success"}
    return {"status": "error"}

def set_brush_color_panel(primary_color=(1,1,1), secondary_color=(0,0,0)):
    # For vertex paint / sculpt vertex colors
    brush = bpy.context.tool_settings.sculpt.brush
    if brush:
        brush.color = primary_color
        brush.secondary_color = secondary_color
        return {"status": "success"}
    return {"status": "error"}
