import bpy

def add_modifier(name, type="SUBSURF", **kwargs):
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"status": "error", "message": f"Object {name} not found"}

    mod = obj.modifiers.new(name="MCP_Modifier", type=type)
    for key, value in kwargs.items():
        if hasattr(mod, key):
            setattr(mod, key, value)
    return {"status": "success", "modifier": mod.name}

def remove_modifier(obj_name, mod_name):
    obj = bpy.data.objects.get(obj_name)
    mod = obj.modifiers.get(mod_name)
    if obj and mod:
        obj.modifiers.remove(mod)
        return {"status": "success"}
    return {"status": "error"}

def apply_modifier(obj_name, mod_name):
    obj = bpy.data.objects.get(obj_name)
    if obj:
        bpy.context.view_layer.objects.active = obj
        try:
            bpy.ops.object.modifier_apply(modifier=mod_name)
            return {"status": "success"}
        except: return {"status": "error"}
    return {"status": "error"}
