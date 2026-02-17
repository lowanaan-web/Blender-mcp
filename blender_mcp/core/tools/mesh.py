import bpy

def add_torus(location=(0,0,0), name="Torus"):
    bpy.ops.mesh.primitive_torus_add(location=location)
    bpy.context.active_object.name = name
    return {"status": "success"}

def add_monkey(location=(0,0,0), name="Suzanne"):
    bpy.ops.mesh.primitive_monkey_add(location=location)
    bpy.context.active_object.name = name
    return {"status": "success"}

def add_icosphere(location=(0,0,0), subdivisions=2, name="IcoSphere"):
    bpy.ops.mesh.primitive_ico_sphere_add(location=location, subdivisions=subdivisions)
    bpy.context.active_object.name = name
    return {"status": "success"}

def subdivide_mesh(name, cuts=1):
    obj = bpy.data.objects.get(name)
    if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid object"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=cuts)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}

def shade_smooth(name, smooth=True):
    obj = bpy.data.objects.get(name)
    if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid object"}
    if smooth:
        bpy.ops.object.shade_smooth({"selected_editable_objects": [obj]})
    else:
        bpy.ops.object.shade_flat({"selected_editable_objects": [obj]})
    return {"status": "success"}
