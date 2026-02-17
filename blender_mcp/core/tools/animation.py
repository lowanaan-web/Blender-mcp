import bpy

def set_keyframe(name, property, frame):
    obj = bpy.data.objects.get(name)
    if obj:
        obj.keyframe_insert(data_path=property, frame=frame)
        return {"status": "success"}
    return {"status": "error"}

def set_timeline(start, end):
    bpy.context.scene.frame_start = start
    bpy.context.scene.frame_end = end
    return {"status": "success"}

def set_current_frame(frame):
    bpy.context.scene.frame_set(frame)
    return {"status": "success"}
