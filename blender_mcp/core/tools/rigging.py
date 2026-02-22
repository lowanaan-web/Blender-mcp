import bpy

def create_armature(name="Armature"):
    arm_data = bpy.data.armatures.new(name)
    obj = bpy.data.objects.new(name, arm_data)
    bpy.context.collection.objects.link(obj)
    return {"status": "success", "name": obj.name}

def add_bone(armature_name, bone_name, head=(0,0,0), tail=(0,0,1)):
    obj = bpy.data.objects.get(armature_name)
    if not obj or obj.type != 'ARMATURE': return {"status": "error"}

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bone = obj.data.edit_bones.new(bone_name)
    bone.head = head
    bone.tail = tail
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success", "name": bone_name}

def parent_to_armature(obj_name, armature_name, mode='AUTOMATIC'):
    obj = bpy.data.objects.get(obj_name)
    arm = bpy.data.objects.get(armature_name)
    if not obj or not arm: return {"status": "error"}

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm

    if mode == 'AUTOMATIC':
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    elif mode == 'ENVELOPES':
        bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')
    else:
        bpy.ops.object.parent_set(type='ARMATURE')

    return {"status": "success"}

def set_bone_transform(armature_name, bone_name, location=None, rotation=None, scale=None):
    obj = bpy.data.objects.get(armature_name)
    if not obj or obj.type != 'ARMATURE': return {"status": "error"}

    bpy.ops.object.mode_set(mode='POSE')
    bone = obj.pose.bones.get(bone_name)
    if not bone:
        bpy.ops.object.mode_set(mode='OBJECT')
        return {"status": "error", "message": "Bone not found"}

    if location: bone.location = location
    if rotation:
        if bone.rotation_mode == 'QUATERNION':
            bone.rotation_quaternion = rotation
        else:
            bone.rotation_euler = rotation
    if scale: bone.scale = scale

    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "success"}
