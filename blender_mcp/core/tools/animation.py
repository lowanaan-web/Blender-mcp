import bpy

def set_keyframe(obj_name, data_path, frame=None):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return {"status": "error"}
    if frame is not None:
        obj.keyframe_insert(data_path=data_path, frame=frame)
    else:
        obj.keyframe_insert(data_path=data_path)
    return {"status": "success"}

def set_timeline(start=1, end=250, fps=24):
    bpy.context.scene.frame_start = start
    bpy.context.scene.frame_end = end
    bpy.context.scene.render.fps = fps
    return {"status": "success"}

def set_current_frame(frame):
    bpy.context.scene.frame_set(frame)
    return {"status": "success"}

def create_action_constraint(obj_name, target_name, action_name, frame_start, frame_end):
    obj = bpy.data.objects.get(obj_name)
    target = bpy.data.objects.get(target_name)
    if not obj or not target: return {"status": "error"}
    con = obj.constraints.new(type='ACTION')
    con.target = target
    con.action = bpy.data.actions.get(action_name)
    con.frame_start = frame_start
    con.frame_end = frame_end
    return {"status": "success", "name": con.name}

def add_fcurve_modifier(obj_name, data_path, type='CYCLES'):
    obj = bpy.data.objects.get(obj_name)
    if not obj or not obj.animation_data or not obj.animation_data.action:
        return {"status": "error", "message": "No animation data"}
    for fcurve in obj.animation_data.action.fcurves:
        if fcurve.data_path == data_path:
            fcurve.modifiers.new(type=type)
            return {"status": "success"}
    return {"status": "error", "message": "F-Curve not found"}

def clear_animation(obj_name):
    obj = bpy.data.objects.get(obj_name)
    if obj:
        obj.animation_data_clear()
        return {"status": "success"}
    return {"status": "error"}

def set_interpolation_type(type='BEZIER'):
    # Sets default interpolation for new keyframes
    bpy.context.preferences.edit.keyframe_new_interpolation_type = type
    return {"status": "success"}

def bake_action(obj_name, frame_start, frame_end, only_selected=True):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return {"status": "error"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.nla.bake(frame_start=frame_start, frame_end=frame_end, only_selected=only_selected, visual_keying=True)
    return {"status": "success"}
