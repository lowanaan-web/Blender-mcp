import bpy

def set_paint_mode(obj_name, mode='TEXTURE_PAINT'):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return {"status": "error"}

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode=mode)
    return {"status": "success", "mode": mode}

def create_vertex_group(obj_name, name="Group"):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return {"status": "error"}

    group = obj.vertex_groups.new(name=name)
    return {"status": "success", "name": group.name}

def assign_to_vertex_group(obj_name, group_name, vertex_indices, weight=1.0):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return {"status": "error"}

    group = obj.vertex_groups.get(group_name)
    if not group: return {"status": "error", "message": "Group not found"}

    group.add(vertex_indices, weight, 'REPLACE')
    return {"status": "success"}

def fill_vertex_color(obj_name, color=(1,1,1,1)):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='VERTEX_PAINT')
    # This operator fills with the current brush color
    bpy.context.tool_settings.vertex_paint.brush.color = color[:3]
    bpy.ops.paint.vertex_color_set()
    bpy.ops.object.mode_set(mode='OBJECT')

    return {"status": "success"}
