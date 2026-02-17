import bpy

def create_collection(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return {"status": "success"}

def add_to_collection(obj_name, col_name):
    obj = bpy.data.objects.get(obj_name)
    col = bpy.data.collections.get(col_name)
    if obj and col:
        col.objects.link(obj)
        return {"status": "success"}
    return {"status": "error"}
