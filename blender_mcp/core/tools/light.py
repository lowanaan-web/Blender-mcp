import bpy
import math

def add_light(type='POINT', location=(0,0,0), name="Light"):
    light_data = bpy.data.lights.new(name=name, type=type)
    light_obj = bpy.data.objects.new(name=name, object_data=light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = location
    return {"status": "success", "name": light_obj.name}

def set_light_property(name, energy=10.0, color=(1,1,1)):
    obj = bpy.data.objects.get(name)
    if obj and obj.type == 'LIGHT':
        obj.data.energy = energy
        obj.data.color = color
        return {"status": "success"}
    return {"status": "error"}

def add_camera(location=(0,0,0), rotation=(0,0,0), name="Camera"):
    cam_data = bpy.data.cameras.new(name)
    cam_obj = bpy.data.objects.new(name, cam_data)
    bpy.context.collection.objects.link(cam_obj)
    cam_obj.location = location
    cam_obj.rotation_euler = [math.radians(r) for r in rotation]
    return {"status": "success", "name": cam_obj.name}

def set_active_camera(name):
    obj = bpy.data.objects.get(name)
    if obj and obj.type == 'CAMERA':
        bpy.context.scene.camera = obj
        return {"status": "success"}
    return {"status": "error"}
