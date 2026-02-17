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

def move_to_collection(name, collection_name):
    obj = bpy.data.objects.get(name)
    col = bpy.data.collections.get(collection_name)
    if obj and col:
        # Remove from all current collections
        for c in obj.users_collection:
            c.objects.unlink(obj)
        col.objects.link(obj)
        return {"status": "success"}
    return {"status": "error", "message": "Object or collection not found"}

def apply_transform(name, location=True, rotation=True, scale=True):
    obj = bpy.data.objects.get(name)
    if not obj: return {"status": "error", "message": "Object not found"}
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=location, rotation=rotation, scale=scale)
    return {"status": "success"}

def clear_transform(name, location=True, rotation=True, scale=True):
    obj = bpy.data.objects.get(name)
    if not obj: return {"status": "error", "message": "Object not found"}
    if location: obj.location = (0, 0, 0)
    if rotation: obj.rotation_euler = (0, 0, 0)
    if scale: obj.scale = (1, 1, 1)
    return {"status": "success"}

def set_origin(name, type='GEOMETRY_ORIGIN'):
    # type can be: 'GEOMETRY_ORIGIN', 'ORIGIN_GEOMETRY', 'ORIGIN_CURSOR', 'ORIGIN_CENTER_OF_MASS'
    obj = bpy.data.objects.get(name)
    if not obj: return {"status": "error", "message": "Object not found"}
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type=type)
    return {"status": "success"}

def add_empty(name, type='PLAIN_AXES', location=(0, 0, 0)):
    empty = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(empty)
    empty.empty_display_type = type
    empty.location = location
    return {"status": "success", "name": empty.name}

def join_objects(names):
    objs = [bpy.data.objects.get(n) for n in names if bpy.data.objects.get(n)]
    if len(objs) < 2: return {"status": "error", "message": "Need at least 2 objects to join"}
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objs:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    return {"status": "success", "name": objs[0].name}

def separate_objects(name, type='SELECTED'):
    # type can be: 'SELECTED', 'MATERIAL', 'LOOSE'
    obj = bpy.data.objects.get(name)
    if not obj or obj.type != 'MESH': return {"status": "error"}
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.mesh.separate(type=type)
    return {"status": "success"}

def make_instance(name, location=(0, 0, 0)):
    obj = bpy.data.objects.get(name)
    if not obj: return {"status": "error"}
    new_obj = obj.copy()
    # Data is NOT copied, making it an instance
    bpy.context.collection.objects.link(new_obj)
    new_obj.location = location
    return {"status": "success", "name": new_obj.name}

def convert_object(name, target='MESH'):
    obj = bpy.data.objects.get(name)
    if not obj: return {"status": "error"}
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.convert(target=target)
    return {"status": "success"}

def align_objects(names, axis='X'):
    # Simple alignment along an axis based on the first object's position
    objs = [bpy.data.objects.get(n) for n in names if bpy.data.objects.get(n)]
    if not objs: return {"status": "error"}
    ref_val = objs[0].location[['X', 'Y', 'Z'].index(axis)]
    for obj in objs[1:]:
        loc = list(obj.location)
        loc[['X', 'Y', 'Z'].index(axis)] = ref_val
        obj.location = tuple(loc)
    return {"status": "success"}

def randomize_transform(names, loc=(0,0,0), rot=(0,0,0), scale=(0,0,0)):
    import random
    objs = [bpy.data.objects.get(n) for n in names if bpy.data.objects.get(n)]
    for obj in objs:
        obj.location[0] += random.uniform(-loc[0], loc[0])
        obj.location[1] += random.uniform(-loc[1], loc[1])
        obj.location[2] += random.uniform(-loc[2], loc[2])
        obj.rotation_euler[0] += math.radians(random.uniform(-rot[0], rot[0]))
        obj.rotation_euler[1] += math.radians(random.uniform(-rot[1], rot[1]))
        obj.rotation_euler[2] += math.radians(random.uniform(-rot[2], rot[2]))
        obj.scale[0] *= (1.0 + random.uniform(-scale[0], scale[0]))
        obj.scale[1] *= (1.0 + random.uniform(-scale[1], scale[1]))
        obj.scale[2] *= (1.0 + random.uniform(-scale[2], scale[2]))
    return {"status": "success"}

def copy_transforms(source, target):
    src = bpy.data.objects.get(source)
    tgt = bpy.data.objects.get(target)
    if src and tgt:
        tgt.location = src.location
        tgt.rotation_euler = src.rotation_euler
        tgt.scale = src.scale
        return {"status": "success"}
    return {"status": "error"}

def snap_to_cursor(name):
    obj = bpy.data.objects.get(name)
    if obj:
        obj.location = bpy.context.scene.cursor.location
        return {"status": "success"}
    return {"status": "error"}

def snap_cursor_to_object(name):
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.context.scene.cursor.location = obj.location
        return {"status": "success"}
    return {"status": "error"}

def get_object_dimensions(name):
    obj = bpy.data.objects.get(name)
    if obj:
        return {"status": "success", "dimensions": list(obj.dimensions)}
    return {"status": "error"}

def set_object_dimensions(name, dimensions):
    obj = bpy.data.objects.get(name)
    if obj:
        obj.dimensions = dimensions
        return {"status": "success"}
    return {"status": "error"}

def set_display_color(name, color):
    obj = bpy.data.objects.get(name)
    if obj:
        obj.color = color
        return {"status": "success"}
    return {"status": "error"}

def set_draw_type(name, type='TEXTURED'):
    # type can be: 'WIRE', 'SOLID', 'TEXTURED', 'BOUNDS'
    obj = bpy.data.objects.get(name)
    if obj:
        obj.display_type = type
        return {"status": "success"}
    return {"status": "error"}

def make_local(name):
    obj = bpy.data.objects.get(name)
    if obj:
        obj.make_local()
        return {"status": "success"}
    return {"status": "error"}

def set_object_pass_index(name, index):
    obj = bpy.data.objects.get(name)
    if obj:
        obj.pass_index = index
        return {"status": "success"}
    return {"status": "error"}
