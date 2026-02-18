import bpy

def select_object(name, select=True):
    obj = bpy.data.objects.get(name)
    if obj:
        obj.select_set(select)
        return {"status": "success"}
    return {"status": "error"}

def deselect_all():
    bpy.ops.object.select_all(action='DESELECT')
    return {"status": "success"}

def set_active_object(name):
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.context.view_layer.objects.active = obj
        return {"status": "success"}
    return {"status": "error"}

def select_all():
    bpy.ops.object.select_all(action='SELECT')
    return {"status": "success"}

def select_by_type(type='MESH'):
    # type: 'MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'ARMATURE', 'LATTICE', 'EMPTY', 'LIGHT', 'CAMERA'
    for obj in bpy.data.objects:
        if obj.type == type:
            obj.select_set(True)
    return {"status": "success"}

def select_pattern(pattern='*'):
    bpy.ops.object.select_pattern(pattern=pattern)
    return {"status": "success"}

def select_hierarchy(name):
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.select_hierarchy(direction='CHILD', extend=True)
        return {"status": "success"}
    return {"status": "error"}

def invert_selection():
    bpy.ops.object.select_all(action='INVERT')
    return {"status": "success"}

def get_selected_objects():
    return {"status": "success", "selected": [obj.name for obj in bpy.context.selected_objects]}

def get_active_object():
    obj = bpy.context.view_layer.objects.active
    return {"status": "success", "active": obj.name if obj else None}

def set_mode(mode='OBJECT'):
    # mode: 'OBJECT', 'EDIT', 'POSE', 'SCULPT', 'VERTEX_PAINT', 'WEIGHT_PAINT', 'TEXTURE_PAINT'
    bpy.ops.object.mode_set(mode=mode)
    return {"status": "success"}

def get_mode():
    return {"status": "success", "mode": bpy.context.mode}

def hide_unselected(unselected=True):
    bpy.ops.object.hide_view_clear() if not unselected else bpy.ops.object.hide_view_set(unselected=True)
    return {"status": "success"}

def unhide_all():
    bpy.ops.object.hide_view_clear()
    return {"status": "success"}

def focus_selected():
    # Requires 3D Viewport context
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            with bpy.context.temp_override(area=area):
                bpy.ops.view3d.view_selected()
    return {"status": "success"}

def select_grouped(type='COLLECTION'):
    # type: 'COLLECTION', 'TYPE', 'LAYER', 'PARENT'
    bpy.ops.object.select_grouped(type=type)
    return {"status": "success"}

def select_linked(type='OBDATA'):
    # type: 'OBDATA', 'MATERIAL', 'COLLECTION', 'PARENT'
    bpy.ops.object.select_linked(type=type)
    return {"status": "success"}

def select_random(ratio=0.5, seed=0):
    bpy.ops.object.select_random(ratio=ratio, seed=seed)
    return {"status": "success"}
