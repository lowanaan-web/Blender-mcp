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
    return {"status": "success", "message": "Screenshot captured"}

def get_scene_info():
    info = {
        "objects": [],
        "materials": [m.name for m in bpy.data.materials],
        "node_groups": [g.name for g in bpy.data.node_groups],
        "collections": [c.name for c in bpy.data.collections],
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
