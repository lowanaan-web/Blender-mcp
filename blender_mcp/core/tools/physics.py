import bpy

def setup_physics(name, type='RIGID_BODY', physics_type='ACTIVE'):
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"status": "error", "message": f"Object {name} not found"}

    if type == 'RIGID_BODY':
        bpy.context.view_layer.objects.active = obj
        bpy.ops.rigidbody.object_add()
        obj.rigid_body.type = physics_type

    return {"status": "success"}

def setup_cloth(name):
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_add(type='CLOTH')
        return {"status": "success"}
    return {"status": "error"}

def setup_collision(name):
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_add(type='COLLISION')
        return {"status": "success"}
    return {"status": "error"}

def add_force_field(type='WIND', location=(0,0,0)):
    bpy.ops.object.effector_add(type=type, location=location)
    return {"status": "success", "name": bpy.context.active_object.name}
