import bpy
import math

def create_primitive(type="CUBE", location=(0, 0, 0), scale=(1, 1, 1), name=None):
    if type == "CUBE":
        bpy.ops.mesh.primitive_cube_add(location=location)
    elif type == "SPHERE":
        bpy.ops.mesh.primitive_uv_sphere_add(location=location)
    elif type == "PLANE":
        bpy.ops.mesh.primitive_plane_add(location=location)
    elif type == "CYLINDER":
        bpy.ops.mesh.primitive_cylinder_add(location=location)

    obj = bpy.context.active_object
    obj.scale = scale
    if name:
        obj.name = name
    return {"status": "success", "object": obj.name}

def transform_object(name, location=None, rotation=None, scale=None):
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"status": "error", "message": f"Object {name} not found"}

    if location:
        obj.location = location
    if rotation:
        obj.rotation_euler = [math.radians(r) for r in rotation]
    if scale:
        obj.scale = scale
    return {"status": "success"}

def delete_object(name):
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)
        return {"status": "success"}
    return {"status": "error", "message": "Object not found"}

def duplicate_object(name, location=None):
    obj = bpy.data.objects.get(name)
    if not obj: return {"status": "error", "message": "Object not found"}
    new_obj = obj.copy()
    new_obj.data = obj.data.copy()
    bpy.context.collection.objects.link(new_obj)
    if location: new_obj.location = location
    return {"status": "success", "new_name": new_obj.name}

def rename_object(old_name, new_name):
    obj = bpy.data.objects.get(old_name)
    if obj:
        obj.name = new_name
        return {"status": "success"}
    return {"status": "error", "message": "Object not found"}

def set_parent(child_name, parent_name):
    child = bpy.data.objects.get(child_name)
    parent = bpy.data.objects.get(parent_name)
    if child and parent:
        child.parent = parent
        return {"status": "success"}
    return {"status": "error", "message": "Objects not found"}

def clear_parent(name):
    obj = bpy.data.objects.get(name)
    if obj:
        obj.parent = None
        return {"status": "success"}
    return {"status": "error", "message": "Object not found"}

def hide_object(name, hide=True):
    obj = bpy.data.objects.get(name)
    if obj:
        obj.hide_viewport = hide
        obj.hide_render = hide
        return {"status": "success"}
    return {"status": "error", "message": "Object not found"}
