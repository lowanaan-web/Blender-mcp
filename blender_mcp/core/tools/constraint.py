import bpy

def _get_obj(name):
    return bpy.data.objects.get(name)

def add_constraint(obj_name, type='TRACK_TO', target_name=None):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error", "message": f"Object {obj_name} not found"}
    con = obj.constraints.new(type=type)
    if target_name:
        target = _get_obj(target_name)
        if target: con.target = target
    return {"status": "success", "name": con.name}

def add_copy_location_constraint(obj_name, target_name, use_x=True, use_y=True, use_z=True, invert_x=False, invert_y=False, invert_z=False, influence=1.0):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error", "message": "Object or target not found"}
    con = obj.constraints.new(type='COPY_LOCATION')
    con.target = target
    con.use_x, con.use_y, con.use_z = use_x, use_y, use_z
    con.invert_x, con.invert_y, con.invert_z = invert_x, invert_y, invert_z
    con.influence = influence
    return {"status": "success", "name": con.name}

def add_copy_rotation_constraint(obj_name, target_name, use_x=True, use_y=True, use_z=True, invert_x=False, invert_y=False, invert_z=False, influence=1.0):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error", "message": "Object or target not found"}
    con = obj.constraints.new(type='COPY_ROTATION')
    con.target = target
    con.use_x, con.use_y, con.use_z = use_x, use_y, use_z
    con.invert_x, con.invert_y, con.invert_z = invert_x, invert_y, invert_z
    con.influence = influence
    return {"status": "success", "name": con.name}

def add_copy_scale_constraint(obj_name, target_name, use_x=True, use_y=True, use_z=True, influence=1.0):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error", "message": "Object or target not found"}
    con = obj.constraints.new(type='COPY_SCALE')
    con.target = target
    con.use_x, con.use_y, con.use_z = use_x, use_y, use_z
    con.influence = influence
    return {"status": "success", "name": con.name}

def add_copy_transforms_constraint(obj_name, target_name, influence=1.0):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error", "message": "Object or target not found"}
    con = obj.constraints.new(type='COPY_TRANSFORMS')
    con.target = target
    con.influence = influence
    return {"status": "success", "name": con.name}

def add_limit_location_constraint(obj_name, use_min_x=False, min_x=0.0, use_max_x=False, max_x=0.0, use_min_y=False, min_y=0.0, use_max_y=False, max_y=0.0, use_min_z=False, min_z=0.0, use_max_z=False, max_z=0.0):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error", "message": "Object not found"}
    con = obj.constraints.new(type='LIMIT_LOCATION')
    con.use_min_x, con.min_x = use_min_x, min_x
    con.use_max_x, con.max_x = use_max_x, max_x
    con.use_min_y, con.min_y = use_min_y, min_y
    con.use_max_y, con.max_y = use_max_y, max_y
    con.use_min_z, con.min_z = use_min_z, min_z
    con.use_max_z, con.max_z = use_max_z, max_z
    return {"status": "success", "name": con.name}

def add_limit_rotation_constraint(obj_name, use_limit_x=False, min_x=0.0, max_x=0.0, use_limit_y=False, min_y=0.0, max_y=0.0, use_limit_z=False, min_z=0.0, max_z=0.0):
    import math
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error", "message": "Object not found"}
    con = obj.constraints.new(type='LIMIT_ROTATION')
    con.use_limit_x = use_limit_x
    con.min_x, con.max_x = math.radians(min_x), math.radians(max_x)
    con.use_limit_y = use_limit_y
    con.min_y, con.max_y = math.radians(min_y), math.radians(max_y)
    con.use_limit_z = use_limit_z
    con.min_z, con.max_z = math.radians(min_z), math.radians(max_z)
    return {"status": "success", "name": con.name}

def add_limit_distance_constraint(obj_name, target_name, distance=1.0, limit_mode='LIMITDIST_INSIDE'):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error", "message": "Object or target not found"}
    con = obj.constraints.new(type='LIMIT_DISTANCE')
    con.target = target
    con.distance = distance
    con.limit_mode = limit_mode
    return {"status": "success", "name": con.name}

def add_track_to_constraint(obj_name, target_name, track_axis='TRACK_NEGATIVE_Z', up_axis='UP_Y', influence=1.0):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error", "message": "Object or target not found"}
    con = obj.constraints.new(type='TRACK_TO')
    con.target = target
    con.track_axis = track_axis
    con.up_axis = up_axis
    con.influence = influence
    return {"status": "success", "name": con.name}

def add_damped_track_constraint(obj_name, target_name, track_axis='TRACK_NEGATIVE_Z', influence=1.0):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error", "message": "Object or target not found"}
    con = obj.constraints.new(type='DAMPED_TRACK')
    con.target = target
    con.track_axis = track_axis
    con.influence = influence
    return {"status": "success", "name": con.name}

def add_follow_path_constraint(obj_name, target_name, use_fixed_location=True, offset_factor=0.0, use_curve_follow=True, influence=1.0):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error", "message": "Object or target not found"}
    con = obj.constraints.new(type='FOLLOW_PATH')
    con.target = target
    con.use_fixed_location = use_fixed_location
    con.offset_factor = offset_factor
    con.use_curve_follow = use_curve_follow
    con.influence = influence
    return {"status": "success", "name": con.name}

def add_shrinkwrap_constraint(obj_name, target_name, shrinkwrap_type='NEAREST_SURFACE', distance=0.0, influence=1.0):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error", "message": "Object or target not found"}
    con = obj.constraints.new(type='SHRINKWRAP')
    con.target = target
    con.shrinkwrap_type = shrinkwrap_type
    con.distance = distance
    con.influence = influence
    return {"status": "success", "name": con.name}

def add_child_of_constraint(obj_name, target_name, influence=1.0):
    obj = _get_obj(obj_name)
    target = _get_obj(target_name)
    if not obj or not target: return {"status": "error", "message": "Object or target not found"}
    con = obj.constraints.new(type='CHILD_OF')
    con.target = target
    con.influence = influence
    # Note: inverse matrix usually needs to be set manually or via operator if not default
    return {"status": "success", "name": con.name}

def add_ik_constraint(obj_name, target_name=None, chain_count=0, influence=1.0, pole_target_name=None, pole_angle=0.0):
    import math
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error", "message": "Object not found"}
    con = obj.constraints.new(type='IK')
    if target_name:
        target = _get_obj(target_name)
        if target: con.target = target
    if pole_target_name:
        pole = _get_obj(pole_target_name)
        if pole:
            con.pole_target = pole
            con.pole_angle = math.radians(pole_angle)
    con.chain_count = chain_count
    con.influence = influence
    return {"status": "success", "name": con.name}

def remove_constraint(obj_name, constraint_name):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error", "message": "Object not found"}
    con = obj.constraints.get(constraint_name)
    if not con: return {"status": "error", "message": "Constraint not found"}
    obj.constraints.remove(con)
    return {"status": "success"}

def clear_constraints(obj_name):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error", "message": "Object not found"}
    obj.constraints.clear()
    return {"status": "success"}

def set_constraint_influence(obj_name, constraint_name, influence=1.0):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error", "message": "Object not found"}
    con = obj.constraints.get(constraint_name)
    if not con: return {"status": "error", "message": "Constraint not found"}
    con.influence = influence
    return {"status": "success"}

def get_constraints_info(obj_name):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error", "message": "Object not found"}
    constraints = []
    for con in obj.constraints:
        info = {
            "name": con.name,
            "type": con.type,
            "influence": con.influence,
            "mute": con.mute,
            "target": con.target.name if hasattr(con, 'target') and con.target else None
        }
        constraints.append(info)
    return {"status": "success", "constraints": constraints}

def add_limit_scale_constraint(obj_name, use_min_x=False, min_x=1.0, use_max_x=False, max_x=1.0, use_min_y=False, min_y=1.0, use_max_y=False, max_y=1.0, use_min_z=False, min_z=1.0, use_max_z=False, max_z=1.0):
    obj = _get_obj(obj_name)
    if not obj: return {"status": "error", "message": "Object not found"}
    con = obj.constraints.new(type='LIMIT_SCALE')
    con.use_min_x, con.min_x = use_min_x, min_x
    con.use_max_x, con.max_x = use_max_x, max_x
    con.use_min_y, con.min_y = use_min_y, min_y
    con.use_max_y, con.max_y = use_max_y, max_y
    con.use_min_z, con.min_z = use_min_z, min_z
    con.use_max_z, con.max_z = use_max_z, max_z
    return {"status": "success", "name": con.name}
