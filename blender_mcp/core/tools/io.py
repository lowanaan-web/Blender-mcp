import bpy

def import_obj(filepath):
    try:
        bpy.ops.import_scene.obj(filepath=filepath)
        return {"status": "success", "object": bpy.context.active_object.name}
    except: return {"status": "error"}

def export_obj(filepath):
    try:
        bpy.ops.export_scene.obj(filepath=filepath)
        return {"status": "success"}
    except: return {"status": "error"}
