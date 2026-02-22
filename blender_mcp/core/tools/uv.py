import bpy

def unwrap_mesh(obj_name, method='ANGLE_BASED', margin=0.001):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.unwrap(method=method, margin=margin)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}

def smart_uv_project(obj_name, angle_limit=66.0, island_margin=0.0):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=angle_limit, island_margin=island_margin)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}

def pack_uvs(obj_name, margin=0.001):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.pack_islands(margin=margin)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}

def create_uv_map(obj_name, name="UVMap"):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}

    uv_map = obj.data.uv_layers.new(name=name)
    return {"status": "success", "name": uv_map.name}
