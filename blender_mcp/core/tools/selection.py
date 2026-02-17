import bpy

def select_object(name, select=True):
    obj = bpy.data.objects.get(name)
    if obj:
        obj.select_set(select)
        return {"status": "success"}
    return {"status": "error"}

def deselect_all():
    bpy.ops.object.select_all(action='DESELECT')
    return {"status": "success"}

def set_active_object(name):
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.context.view_layer.objects.active = obj
        return {"status": "success"}
    return {"status": "error"}
