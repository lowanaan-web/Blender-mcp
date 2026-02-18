import bpy
import os

def list_assets():
    """Lists available assets in the Blender Asset Browser."""
    assets = []
    # This lists assets in the 'Current File' library
    for asset in bpy.data.assets.local_id_metadata:
        assets.append({
            "name": asset.name,
            "id": asset.id_name,
            "type": asset.id_type
        })
    # Also list assets from external libraries if possible
    # (Note: Browsing external libraries via Python is more complex in 3.6/4.x)
    return {"status": "success", "assets": assets}

def import_asset(asset_name, location=(0,0,0)):
    """Imports an asset by name from the current file's asset library."""
    # This is a simplified version; real asset import might require appending/linking
    obj = bpy.data.objects.get(asset_name)
    if obj:
        new_obj = obj.copy()
        new_obj.data = obj.data.copy()
        bpy.context.collection.objects.link(new_obj)
        new_obj.location = location
        return {"status": "success", "name": new_obj.name}
    return {"status": "error", "message": "Asset not found"}

def setup_pbr_material(name, base_color_path=None, normal_path=None, rough_path=None, metallic_path=None):
    """Sets up a complete PBR material from a set of image textures."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    bsdf = nodes.get("Principled BSDF")

    def add_texture(path, label, color_space='sRGB'):
        if not path or not os.path.exists(path): return None
        tex_node = nodes.new('ShaderNodeTexImage')
        tex_node.label = label
        try:
            img = bpy.data.images.load(path)
            tex_node.image = img
            img.colorspace_settings.name = color_space
            return tex_node
        except:
            return None

    # Base Color
    col_tex = add_texture(base_color_path, "Base Color")
    if col_tex: links.new(col_tex.outputs[0], bsdf.inputs['Base Color'])

    # Roughness
    rough_tex = add_texture(rough_path, "Roughness", 'Non-Color')
    if rough_tex: links.new(rough_tex.outputs[0], bsdf.inputs['Roughness'])

    # Metallic
    met_tex = add_texture(metallic_path, "Metallic", 'Non-Color')
    if met_tex: links.new(met_tex.outputs[0], bsdf.inputs['Metallic'])

    # Normal
    norm_tex = add_texture(normal_path, "Normal", 'Non-Color')
    if norm_tex:
        norm_map = nodes.new('ShaderNodeNormalMap')
        links.new(norm_tex.outputs[0], norm_map.inputs[1])
        links.new(norm_map.outputs[0], bsdf.inputs['Normal'])

    return {"status": "success", "material": mat.name}
