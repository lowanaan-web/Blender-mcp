import bpy

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    return {"status": "success"}

def set_render_engine(engine='CYCLES'):
    bpy.context.scene.render.engine = engine
    return {"status": "success"}

def set_resolution(x, y):
    bpy.context.scene.render.resolution_x = x
    bpy.context.scene.render.resolution_y = y
    return {"status": "success"}

def render_still(path):
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return {"status": "success"}

def get_screenshot():
    from ...utils.vision import get_base64_viewport
    data = get_base64_viewport()
    if data:
        return {"status": "success", "image_data": data}
    return {"status": "error", "message": "Failed to capture screenshot"}

def request_feedback(message="Please verify the result"):
    # This is a marker tool for the UI to trigger a loop
    return {"status": "success", "feedback_requested": True, "message": message}

def get_scene_info():
    info = {
        "objects": [],
        "materials": [m.name for m in bpy.data.materials],
        "node_groups": [g.name for g in bpy.data.node_groups],
        "collections": [c.name for c in bpy.data.collections],
        "render": {
            "engine": bpy.context.scene.render.engine,
            "resolution": [bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y]
        }
    }
    for obj in bpy.data.objects:
        obj_info = {
            "name": obj.name,
            "type": obj.type,
            "location": list(obj.location),
            "rotation": list(obj.rotation_euler),
            "modifiers": [m.name for m in obj.modifiers],
        }
        info["objects"].append(obj_info)
    return {"status": "success", "info": info}

def set_render_samples(samples=128, preview_samples=32):
    scene = bpy.context.scene
    if scene.render.engine == 'CYCLES':
        scene.cycles.samples = samples
        scene.cycles.preview_samples = preview_samples
    elif scene.render.engine == 'BLENDER_EEVEE':
        scene.eevee.taa_render_samples = samples
        scene.eevee.taa_samples = preview_samples
    return {"status": "success"}

def set_denoising(enabled=True, use_viewport=True):
    scene = bpy.context.scene
    if scene.render.engine == 'CYCLES':
        scene.cycles.use_denoising = enabled
        if hasattr(scene.cycles, "use_preview_denoising"):
            scene.cycles.use_preview_denoising = use_viewport
    return {"status": "success"}

def set_color_management(view_transform='Filmic', look='None', exposure=0.0, gamma=1.0):
    scene = bpy.context.scene
    scene.view_settings.view_transform = view_transform
    scene.view_settings.look = look
    scene.view_settings.exposure = exposure
    scene.view_settings.gamma = gamma
    return {"status": "success"}

def set_output_format(file_format='PNG', color_mode='RGBA', color_depth='8'):
    # file_format: 'PNG', 'JPEG', 'TIFF', 'TARGA', 'FFMPEG', etc.
    # color_mode: 'BW', 'RGB', 'RGBA'
    # color_depth: '8', '16'
    scene = bpy.context.scene
    scene.render.image_settings.file_format = file_format
    scene.render.image_settings.color_mode = color_mode
    scene.render.image_settings.color_depth = color_depth
    return {"status": "success"}

def set_background_transparent(transparent=True):
    bpy.context.scene.render.film_transparent = transparent
    return {"status": "success"}

def add_view_layer(name):
    layer = bpy.context.scene.view_layers.new(name)
    return {"status": "success", "name": layer.name}

def set_render_device(device_type='GPU'):
    # device_type: 'CPU', 'GPU'
    scene = bpy.context.scene
    if scene.render.engine == 'CYCLES':
        scene.cycles.device = device_type
        if device_type == 'GPU':
            prefs = bpy.context.preferences.addons['cycles'].preferences
            prefs.get_devices()
            # This is a bit complex as it depends on user hardware (CUDA, Optix, etc)
            # We just set it to use the first available GPU for now
    return {"status": "success"}

def bake_physics():
    # Bakes all physics in the scene
    bpy.ops.ptcache.bake_all(bake=True)
    return {"status": "success"}

def set_viewport_shading(type='SOLID'):
    # type: 'WIREFRAME', 'SOLID', 'MATERIAL', 'RENDERED'
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = type
    return {"status": "success"}

def toggle_overlays(show=True):
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.overlay.show_overlays = show
    return {"status": "success"}

def set_clipping(start=0.1, end=1000.0, camera_name=None):
    if camera_name:
        cam = bpy.data.cameras.get(camera_name)
        if cam:
            cam.clip_start = start
            cam.clip_end = end
    else:
        # Viewport clipping
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.clip_start = start
                        space.clip_end = end
    return {"status": "success"}

def add_sun_light_env(strength=1.0, rotation=0.0):
    # Sets up a basic environment with a Sun and Sky
    world = bpy.context.scene.world
    if not world: world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    nodes.clear()

    node_env = nodes.new('ShaderNodeTexSky')
    node_bg = nodes.new('ShaderNodeBackground')
    node_out = nodes.new('ShaderNodeOutputWorld')

    node_bg.inputs[1].default_value = strength
    world.node_tree.links.new(node_env.outputs[0], node_bg.inputs[0])
    world.node_tree.links.new(node_bg.outputs[0], node_out.inputs[0])

    return {"status": "success"}

def set_mist_pass(enabled=True, start=5.0, depth=25.0):
    scene = bpy.context.scene
    view_layer = bpy.context.view_layer
    view_layer.use_pass_mist = enabled
    scene.world.mist_settings.start = start
    scene.world.mist_settings.depth = depth
    return {"status": "success"}

def setup_compositor_denoise():
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    nodes = tree.nodes
    nodes.clear()

    node_rl = nodes.new('CompositorNodeRLayers')
    node_denoise = nodes.new('CompositorNodeDenoise')
    node_composite = nodes.new('CompositorNodeComposite')

    tree.links.new(node_rl.outputs['Image'], node_denoise.inputs['Image'])
    tree.links.new(node_denoise.outputs['Image'], node_composite.inputs['Image'])
    return {"status": "success"}

def set_render_region(use_region=True, xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0):
    scene = bpy.context.scene
    scene.render.use_border = use_region
    scene.render.border_min_x = xmin
    scene.render.border_max_x = xmax
    scene.render.border_min_y = ymin
    scene.render.border_max_y = ymax
    return {"status": "success"}

def toggle_simplify(enabled=True, max_subdiv=2):
    scene = bpy.context.scene
    scene.render.use_simplify = enabled
    scene.render.simplify_subdivision = max_subdiv
    return {"status": "success"}

def set_gravity(gravity=(0.0, 0.0, -9.81)):
    bpy.context.scene.gravity = gravity
    return {"status": "success"}

def set_units(length_unit='METERS', mass_unit='KILOGRAMS'):
    scene = bpy.context.scene
    scene.unit_settings.length_unit = length_unit
    scene.unit_settings.mass_unit = mass_unit
    return {"status": "success"}

def get_render_info():
    scene = bpy.context.scene
    return {
        "status": "success",
        "info": {
            "engine": scene.render.engine,
            "resolution": [scene.render.resolution_x, scene.render.resolution_y],
            "fps": scene.render.fps,
            "filepath": scene.render.filepath
        }
    }

def save_file(filepath=None):
    if filepath:
        bpy.ops.wm.save_as_mainfile(filepath=filepath)
    else:
        bpy.ops.wm.save_mainfile()
    return {"status": "success"}

def audit_scene():
    """Provides detailed analysis of the scene (polycount, materials, modifiers)."""
    stats = {
        "total_objects": len(bpy.data.objects),
        "total_vertices": 0,
        "total_faces": 0,
        "objects_audit": []
    }

    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            stats["total_vertices"] += len(obj.data.vertices)
            stats["total_faces"] += len(obj.data.polygons)

        obj_audit = {
            "name": obj.name,
            "type": obj.type,
            "polycount": len(obj.data.polygons) if obj.type == 'MESH' else 0,
            "modifiers": [m.type for m in obj.modifiers],
            "materials": [slot.material.name for slot in obj.material_slots if slot.material]
        }
        stats["objects_audit"].append(obj_audit)

    return {"status": "success", "audit": stats}
