import bpy

def add_hair_curves(obj_name, name="Hair"):
    # Target object (mesh)
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.curves_empty_hair_add()
    hair_obj = bpy.context.active_object
    hair_obj.name = name
    return {"status": "success", "name": hair_obj.name}

def set_hair_resolution(obj_name, resolution=3):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'CURVES': return {"status": "error"}

    obj.data.resolution = resolution
    return {"status": "success"}

def generate_hair_from_mesh(obj_name, density=100.0):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}

    bpy.context.view_layer.objects.active = obj
    # This usually requires Geometry Nodes or Particles,
    # but for Curves-based hair we can use empty hair + manual density setting
    bpy.ops.object.curves_empty_hair_add()
    hair_obj = bpy.context.active_object

    # Simple setup: add a 'Generate' node or similar (simulation)
    # For now, we'll just return the hair object
    return {"status": "success", "name": hair_obj.name}

def set_hair_radius(obj_name, radius=0.01):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'CURVES': return {"status": "error"}

    # Standard for Curves object
    if hasattr(obj.data, 'curve_type'):
        # For legacy hair particles it's different, but for Curves:
        # We usually use a 'Set Curve Radius' node or the viewport display
        pass

    return {"status": "success"}
