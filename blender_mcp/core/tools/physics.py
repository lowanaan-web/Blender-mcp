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

def setup_fluid_domain(name, type='LIQUID'):
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_add(type='FLUID')
        obj.modifiers[-1].fluid_type = 'DOMAIN'
        obj.modifiers[-1].domain_settings.domain_type = type
        return {"status": "success"}
    return {"status": "error"}

def setup_fluid_flow(name, type='LIQUID', behavior='INFLOW'):
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_add(type='FLUID')
        obj.modifiers[-1].fluid_type = 'FLOW'
        obj.modifiers[-1].flow_settings.flow_type = type
        obj.modifiers[-1].flow_settings.flow_behavior = behavior
        return {"status": "success"}
    return {"status": "error"}

def setup_smoke_domain(name):
    return setup_fluid_domain(name, type='GAS')

def setup_smoke_flow(name, behavior='INFLOW'):
    return setup_fluid_flow(name, type='SMOKE', behavior=behavior)

def setup_soft_body(name, friction=0.5, mass=1.0):
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_add(type='SOFT_BODY')
        obj.modifiers[-1].settings.friction = friction
        obj.modifiers[-1].settings.mass = mass
        return {"status": "success"}
    return {"status": "error"}
