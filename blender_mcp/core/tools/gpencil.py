import bpy

def add_gpencil_object(name="GPencil", location=(0,0,0)):
    # Create new Grease Pencil object (v3 in 4.3+, legacy in older)
    try:
        bpy.ops.object.gpencil_add(location=location, type='EMPTY')
        obj = bpy.context.active_object
        obj.name = name
        return {"status": "success", "name": obj.name}
    except:
        gp_data = bpy.data.grease_pencils.new(name)
        obj = bpy.data.objects.new(name, gp_data)
        bpy.context.collection.objects.link(obj)
        obj.location = location
        return {"status": "success", "name": obj.name}

def add_gpencil_layer(obj_name, layer_name="Layer"):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return {"status": "error"}

    # GP v2/v3 check
    if hasattr(obj.data, 'layers'):
        layer = obj.data.layers.new(name=layer_name)
    else:
        # For legacy
        bpy.context.view_layer.objects.active = obj
        bpy.ops.gpencil.layer_add()
        layer = obj.data.layers.active
        layer.info = layer_name

    return {"status": "success", "name": layer.info if hasattr(layer, 'info') else layer.name}

def draw_gpencil_stroke(obj_name, layer_name, points, pressure=1.0):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return {"status": "error"}

    layer = obj.data.layers.get(layer_name)
    if not layer: return {"status": "error", "message": "Layer not found"}

    frame = layer.frames.new(bpy.context.scene.frame_current)
    stroke = frame.strokes.new()
    stroke.points.add(len(points))

    for i, p in enumerate(points):
        stroke.points[i].co = p
        stroke.points[i].pressure = pressure

    return {"status": "success"}

def set_gpencil_material(obj_name, material_name):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return {"status": "error"}

    mat = bpy.data.materials.get(material_name)
    if not mat: return {"status": "error", "message": "Material not found"}

    if mat.name not in obj.data.materials:
        obj.data.materials.append(mat)

    return {"status": "success"}
