import bpy
import os
import tempfile

def capture_viewport():
    """Captures the current 3D viewport and returns the path to the saved image."""
    try:
        # Create a temporary file for the screenshot
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, "blender_mcp_viewport.png")

        # Set render settings for viewport capture
        scene = bpy.context.scene
        original_format = scene.render.image_settings.file_format
        original_path = scene.render.filepath

        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = file_path

        # Find 3D Viewport context
        override = None
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            override = {
                                'window': window,
                                'screen': window.screen,
                                'area': area,
                                'region': region,
                                'scene': scene,
                            }
                            break
                    if override: break
            if override: break

        if override:
            with bpy.context.temp_override(**override):
                bpy.ops.render.opengl(write_still=True)
        else:
            # Fallback
            bpy.ops.render.opengl(write_still=True)

        # Restore settings
        scene.render.image_settings.file_format = original_format
        scene.render.filepath = original_path

        return file_path
    except Exception as e:
        print(f"Error capturing viewport: {e}")
        return None

def get_base64_viewport():
    """Captures the viewport and returns the base64 encoded image."""
    import base64
    path = capture_viewport()
    if path and os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    return None
