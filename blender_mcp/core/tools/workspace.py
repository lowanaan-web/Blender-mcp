import bpy

def set_workspace(name="Layout"):
    ws = bpy.data.workspaces.get(name)
    if not ws: return {"status": "error", "message": "Workspace not found"}

    bpy.context.window.workspace = ws
    return {"status": "success"}

def set_view_transform(transform='Filmic'):
    bpy.context.scene.view_settings.view_transform = transform
    return {"status": "success"}

def toggle_fullscreen():
    bpy.ops.wm.window_fullscreen_toggle()
    return {"status": "success"}

def set_shading_mode(shading_type='SOLID', wireframe=False):
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = shading_type
                    space.shading.show_wireframe = wireframe
    return {"status": "success"}
