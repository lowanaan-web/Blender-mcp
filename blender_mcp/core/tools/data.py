import bpy

def _get_id_data(id_name):
    # Try different ID types
    for collection in [bpy.data.objects, bpy.data.materials, bpy.data.scenes, bpy.data.collections, bpy.data.worlds]:
        item = collection.get(id_name)
        if item: return item
    return None

def set_custom_property(id_name, prop_name, value):
    item = _get_id_data(id_name)
    if not item: return {"status": "error", "message": "ID data not found"}

    item[prop_name] = value
    return {"status": "success"}

def get_custom_property(id_name, prop_name):
    item = _get_id_data(id_name)
    if not item: return {"status": "error"}

    return {"status": "success", "value": item.get(prop_name)}

def add_attribute(obj_name, name, domain='POINT', data_type='FLOAT'):
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH': return {"status": "error"}

    attr = obj.data.attributes.new(name=name, type=data_type, domain=domain)
    return {"status": "success", "name": attr.name}

def remove_custom_property(id_name, prop_name):
    item = _get_id_data(id_name)
    if not item: return {"status": "error"}

    if prop_name in item:
        del item[prop_name]
        return {"status": "success"}
    return {"status": "error", "message": "Property not found"}
