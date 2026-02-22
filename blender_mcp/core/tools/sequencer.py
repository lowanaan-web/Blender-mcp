import bpy

def add_movie_strip(filepath, channel=1, frame_start=1):
    if not bpy.context.scene.sequence_editor:
        bpy.context.scene.sequence_editor_create()

    strip = bpy.context.scene.sequence_editor.sequences.new_movie(
        name="Movie", filepath=filepath, channel=channel, frame_start=frame_start
    )
    return {"status": "success", "name": strip.name}

def add_image_strip(directory, files, channel=1, frame_start=1):
    if not bpy.context.scene.sequence_editor:
        bpy.context.scene.sequence_editor_create()

    # files is list of filenames
    strip = bpy.context.scene.sequence_editor.sequences.new_image(
        name="Images", directory=directory, relative_path=True, channel=channel, frame_start=frame_start
    )
    for f in files:
        strip.elements.append(f)

    return {"status": "success", "name": strip.name}

def add_sound_strip(filepath, channel=1, frame_start=1):
    if not bpy.context.scene.sequence_editor:
        bpy.context.scene.sequence_editor_create()

    strip = bpy.context.scene.sequence_editor.sequences.new_sound(
        name="Sound", filepath=filepath, channel=channel, frame_start=frame_start
    )
    return {"status": "success", "name": strip.name}

def set_strip_transform(strip_name, location=None, scale=None, rotation=None):
    if not bpy.context.scene.sequence_editor: return {"status": "error"}

    strip = bpy.context.scene.sequence_editor.sequences.get(strip_name)
    if not strip: return {"status": "error", "message": "Strip not found"}

    if hasattr(strip, 'transform'):
        if location:
            strip.transform.offset_x = location[0]
            strip.transform.offset_y = location[1]
        if scale:
            strip.transform.scale_x = scale[0]
            strip.transform.scale_y = scale[1]
        if rotation:
            strip.transform.rotation = rotation

    return {"status": "success"}
