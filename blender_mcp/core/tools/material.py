import bpy

def assign_material(name, color=(0.8, 0.8, 0.8, 1.0), metallic=0.0, roughness=0.5):
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"status": "error", "message": f"Object {name} not found"}

    mat = bpy.data.materials.new(name=f"Mat_{name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs[0].default_value = color
        bsdf.inputs[6].default_value = metallic
        bsdf.inputs[9].default_value = roughness

    if hasattr(obj.data, 'materials'):
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
    return {"status": "success", "material": mat.name}

def remove_material(name):
    obj = bpy.data.objects.get(name)
    if obj and hasattr(obj.data, 'materials'):
        obj.data.materials.clear()
        return {"status": "success"}
    return {"status": "error"}

def set_material_property(mat_name, node_name, input_index, value):
    mat = bpy.data.materials.get(mat_name)
    if not mat or not mat.use_nodes: return {"status": "error"}
    node = mat.node_tree.nodes.get(node_name)
    if node and len(node.inputs) > input_index:
        node.inputs[input_index].default_value = value
        return {"status": "success"}
    return {"status": "error"}

def add_texture_image(mat_name, image_path):
    mat = bpy.data.materials.get(mat_name)
    if not mat or not mat.use_nodes: return {"status": "error"}
    nodes = mat.node_tree.nodes
    tex_node = nodes.new('ShaderNodeTexImage')
    try:
        img = bpy.data.images.load(image_path)
        tex_node.image = img
        return {"status": "success", "node_name": tex_node.name}
    except:
        return {"status": "error", "message": "Failed to load image"}

def set_world_background(color=(0.05, 0.05, 0.05, 1.0), strength=1.0):
    world = bpy.context.scene.world
    if not world: world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    bg = nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = color
        bg.inputs[1].default_value = strength
    return {"status": "success"}
