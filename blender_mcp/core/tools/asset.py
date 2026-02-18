import bpy

def list_assets():
    # In a real addon, this would browse asset libraries
    # For now, we list items in the current file marked as assets
    assets = []
    for obj in bpy.data.objects:
        if obj.asset_data:
            assets.append({"name": obj.name, "type": "OBJECT"})
    for mat in bpy.data.materials:
        if mat.asset_data:
            assets.append({"name": mat.name, "type": "MATERIAL"})
    return {"status": "success", "assets": assets}

def import_asset(name, type='OBJECT'):
    # Basic implementation: find in local data
    if type == 'OBJECT':
        obj = bpy.data.objects.get(name)
        if obj:
            new_obj = obj.copy()
            bpy.context.collection.objects.link(new_obj)
            return {"status": "success", "name": new_obj.name}
    return {"status": "error"}

def setup_pbr_material(name, base_color=(0.8, 0.8, 0.8, 1.0), metallic=0.0, roughness=0.5, specular=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Specular IOR Level'].default_value = specular
    return {"status": "success", "material_name": mat.name}

def setup_glass_material(name, color=(1.0, 1.0, 1.0, 1.0), ior=1.45, roughness=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Transmission Weight'].default_value = 1.0
        bsdf.inputs['IOR'].default_value = ior
        bsdf.inputs['Roughness'].default_value = roughness
    return {"status": "success", "material_name": mat.name}

def setup_emission_material(name, color=(1.0, 1.0, 1.0, 1.0), strength=1.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    node_emit = nodes.new(type='ShaderNodeEmission')
    node_emit.inputs['Color'].default_value = color
    node_emit.inputs['Strength'].default_value = strength
    node_out = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(node_emit.outputs['Emission'], node_out.inputs['Surface'])
    return {"status": "success", "material_name": mat.name}

def setup_car_paint_material(name, color=(0.8, 0.0, 0.0, 1.0)):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Metallic'].default_value = 1.0
        bsdf.inputs['Roughness'].default_value = 0.1
        bsdf.inputs['Clearcoat Weight'].default_value = 1.0
        bsdf.inputs['Clearcoat Roughness'].default_value = 0.03
    return {"status": "success", "material_name": mat.name}
