import bpy

def add_constraint(obj_name, type='TRACK_TO', target_name=None):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return {"status": "error"}
    con = obj.constraints.new(type=type)
    if target_name:
        con.target = bpy.data.objects.get(target_name)
    return {"status": "success", "name": con.name}
