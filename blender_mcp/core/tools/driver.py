import bpy

def add_driver(obj_name, path, expression, use_self=False):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return {"status": "error"}

    driver = obj.driver_add(path).driver
    driver.expression = expression
    driver.use_self = use_self
    return {"status": "success"}

def remove_driver(obj_name, path):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return {"status": "error"}

    obj.driver_remove(path)
    return {"status": "success"}

def add_driver_variable(obj_name, path, var_name, type='TRANSFORMS', target_obj=None, data_path=""):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return {"status": "error"}

    fcurve = obj.animation_data.drivers.find(path)
    if not fcurve: return {"status": "error", "message": "Driver not found"}

    var = fcurve.driver.variables.new()
    var.name = var_name
    var.type = type

    if target_obj:
        target = bpy.data.objects.get(target_obj)
        if target:
            var.targets[0].id = target
            var.targets[0].data_path = data_path

    return {"status": "success"}

def set_driver_expression(obj_name, path, expression):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return {"status": "error"}

    fcurve = obj.animation_data.drivers.find(path)
    if not fcurve: return {"status": "error"}

    fcurve.driver.expression = expression
    return {"status": "success"}
