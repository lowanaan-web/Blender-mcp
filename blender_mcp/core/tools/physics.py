import bpy

def _get_obj(name):
    return bpy.data.objects.get(name)

def setup_physics(name, type='RIGID_BODY', physics_type='ACTIVE'):
    obj = _get_obj(name)
    if not obj: return {"status": "error", "message": f"Object {name} not found"}
    bpy.context.view_layer.objects.active = obj
    if type == 'RIGID_BODY':
        if not obj.rigid_body:
            bpy.ops.rigidbody.object_add()
        obj.rigid_body.type = physics_type
    return {"status": "success"}

def setup_rigid_body_world(gravity=(0, 0, -9.81), time_scale=1.0, sub_steps=10):
    scene = bpy.context.scene
    if not scene.rigidbody_world:
        bpy.ops.rigidbody.world_add()
    rw = scene.rigidbody_world
    scene.gravity = gravity
    rw.time_scale = time_scale
    rw.substeps_per_frame = sub_steps
    return {"status": "success"}

def add_rigid_body_constraint(obj_name, target_a, target_b, type='FIXED', disable_collisions=True):
    obj = _get_obj(obj_name)
    if not obj:
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        obj = bpy.context.active_object
        obj.name = obj_name

    bpy.context.view_layer.objects.active = obj
    if not obj.rigid_body_constraint:
        bpy.ops.rigidbody.constraint_add()

    rbc = obj.rigid_body_constraint
    rbc.type = type
    rbc.object1 = _get_obj(target_a)
    rbc.object2 = _get_obj(target_b)
    rbc.disable_collisions = disable_collisions
    return {"status": "success", "name": obj.name}

def setup_cloth(name, preset='COTTON'):
    obj = _get_obj(name)
    if not obj: return {"status": "error"}
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Cloth", type='CLOTH')
    # Presets are usually set via RNA or operator, here we set basic values
    if preset == 'SILK':
        mod.settings.mass = 0.15
        mod.settings.structural_stiffness = 5
    elif preset == 'LEATHER':
        mod.settings.mass = 0.4
        mod.settings.structural_stiffness = 80
    return {"status": "success"}

def setup_dynamic_paint_canvas(name, surface_type='WAVE'):
    obj = _get_obj(name)
    if not obj: return {"status": "error"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_add(type='DYNAMIC_PAINT')
    obj.modifiers[-1].ui_type = 'CANVAS'
    bpy.ops.dpaint.surface_slot_add()
    obj.modifiers[-1].canvas_settings.canvas_surfaces[-1].surface_type = surface_type
    return {"status": "success"}

def setup_dynamic_paint_brush(name):
    obj = _get_obj(name)
    if not obj: return {"status": "error"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_add(type='DYNAMIC_PAINT')
    obj.modifiers[-1].ui_type = 'BRUSH'
    return {"status": "success"}

def add_ocean_modifier(name, resolution=7, size=1.0, spatial_size=50):
    obj = _get_obj(name)
    if not obj: return {"status": "error"}
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Ocean", type='OCEAN')
    mod.resolution = resolution
    mod.size = size
    mod.spatial_size = spatial_size
    return {"status": "success"}

def setup_particle_system(name, type='EMITTER', count=1000, frame_start=1, frame_end=200):
    obj = _get_obj(name)
    if not obj: return {"status": "error"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.particle_system_add()
    psys = obj.particle_systems[-1].settings
    psys.type = type
    psys.count = count
    psys.frame_start = frame_start
    psys.frame_end = frame_end
    return {"status": "success"}

def explode_object(name, count=100):
    obj = _get_obj(name)
    if not obj: return {"status": "error"}
    bpy.context.view_layer.objects.active = obj
    # Needs a particle system first
    setup_particle_system(name, count=count)
    bpy.ops.object.modifier_add(type='EXPLODE')
    return {"status": "success"}

def bake_all_physics():
    bpy.ops.ptcache.bake_all(bake=True)
    return {"status": "success"}

def setup_collision(name, damping=0.1, friction=0.5):
    obj = _get_obj(name)
    if not obj: return {"status": "error"}
    bpy.context.view_layer.objects.active = obj
    if not any(m.type == 'COLLISION' for m in obj.modifiers):
        bpy.ops.object.modifier_add(type='COLLISION')
    coll = obj.modifiers[-1].collision_settings
    coll.damping = damping
    coll.friction = friction
    return {"status": "success"}

def add_force_field(type='WIND', strength=1.0, location=(0,0,0)):
    bpy.ops.object.effector_add(type=type, location=location)
    obj = bpy.context.active_object
    obj.field.strength = strength
    return {"status": "success", "name": obj.name}

def setup_soft_body(name, friction=0.5, mass=1.0, goal_strength=0.5):
    obj = _get_obj(name)
    if not obj: return {"status": "error"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_add(type='SOFT_BODY')
    sb = obj.modifiers[-1].settings
    sb.friction = friction
    sb.mass = mass
    sb.goal_default = goal_strength
    return {"status": "success"}

def setup_fluid_domain(name, type='LIQUID', resolution=32):
    obj = _get_obj(name)
    if not obj: return {"status": "error"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_add(type='FLUID')
    obj.modifiers[-1].fluid_type = 'DOMAIN'
    obj.modifiers[-1].domain_settings.domain_type = type
    obj.modifiers[-1].domain_settings.resolution_max = resolution
    return {"status": "success"}

def setup_fluid_flow(name, type='LIQUID', behavior='INFLOW', velocity=(0,0,0)):
    obj = _get_obj(name)
    if not obj: return {"status": "error"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_add(type='FLUID')
    obj.modifiers[-1].fluid_type = 'FLOW'
    flow = obj.modifiers[-1].flow_settings
    flow.flow_type = type
    flow.flow_behavior = behavior
    if any(velocity):
        flow.use_initial_velocity = True
        flow.velocity_coord = velocity
    return {"status": "success"}
