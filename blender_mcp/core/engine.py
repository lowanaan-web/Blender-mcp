import bpy
import json

class AtomicEngine:
    def __init__(self):
        self.tools = {
            # Object & Transform
            "create_primitive": self.create_primitive,
            "transform_object": self.transform_object,
            "delete_object": self.delete_object,
            "duplicate_object": self.duplicate_object,
            "rename_object": self.rename_object,
            "set_parent": self.set_parent,
            "clear_parent": self.clear_parent,
            "hide_object": self.hide_object,

            # Mesh Ops
            "add_torus": self.add_torus,
            "add_monkey": self.add_monkey,
            "add_icosphere": self.add_icosphere,
            "subdivide_mesh": self.subdivide_mesh,
            "shade_smooth": self.shade_smooth,

            # Materials & Textures
            "assign_material": self.assign_material,
            "remove_material": self.remove_material,
            "set_material_property": self.set_material_property,
            "add_texture_image": self.add_texture_image,
            "set_world_background": self.set_world_background,

            # Lighting & Camera
            "add_light": self.add_light,
            "set_light_property": self.set_light_property,
            "add_camera": self.add_camera,
            "set_active_camera": self.set_active_camera,

            # Modifiers
            "add_modifier": self.add_modifier,
            "remove_modifier": self.remove_modifier,
            "apply_modifier": self.apply_modifier,

            # Physics
            "setup_physics": self.setup_physics,
            "setup_cloth": self.setup_cloth,
            "setup_collision": self.setup_collision,
            "add_force_field": self.add_force_field,

            # Nodes
            "setup_geometry_nodes": self.setup_geometry_nodes,
            "create_node": self.create_node,
            "connect_nodes": self.connect_nodes,
            "remove_node": self.remove_node,
            "set_node_property": self.set_node_property,

            # Animation
            "set_keyframe": self.set_keyframe,
            "set_timeline": self.set_timeline,
            "set_current_frame": self.set_current_frame,

            # Collections
            "create_collection": self.create_collection,
            "add_to_collection": self.add_to_collection,

            # Scene & Rendering
            "get_scene_info": self.get_scene_info,
            "get_screenshot": self.get_screenshot,
            "clear_scene": self.clear_scene,
            "set_render_engine": self.set_render_engine,
            "set_resolution": self.set_resolution,
            "render_still": self.render_still,

            # Constraints
            "add_constraint": self.add_constraint,

            # Selection & Context
            "select_object": self.select_object,
            "deselect_all": self.deselect_all,
            "set_active_object": self.set_active_object,

            # Import/Export
            "import_obj": self.import_obj,
            "export_obj": self.export_obj,
        }

    def execute_tool(self, tool_name, args):
        if tool_name in self.tools:
            try:
                return self.tools[tool_name](**args)
            except Exception as e:
                return {"status": "error", "message": str(e)}
        else:
            return {"status": "error", "message": f"Tool {tool_name} not found"}

    def create_primitive(self, type="CUBE", location=(0, 0, 0), scale=(1, 1, 1), name=None):
        if type == "CUBE":
            bpy.ops.mesh.primitive_cube_add(location=location)
        elif type == "SPHERE":
            bpy.ops.mesh.primitive_uv_sphere_add(location=location)
        elif type == "PLANE":
            bpy.ops.mesh.primitive_plane_add(location=location)
        elif type == "CYLINDER":
            bpy.ops.mesh.primitive_cylinder_add(location=location)

        obj = bpy.context.active_object
        obj.scale = scale
        if name:
            obj.name = name
        return {"status": "success", "object": obj.name}

    def transform_object(self, name, location=None, rotation=None, scale=None):
        obj = bpy.data.objects.get(name)
        if not obj:
            return {"status": "error", "message": f"Object {name} not found"}

        if location:
            obj.location = location
        if rotation:
            obj.rotation_euler = [(r * 3.14159 / 180.0) for r in rotation] # Convert from degrees
        if scale:
            obj.scale = scale
        return {"status": "success"}

    def delete_object(self, name):
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)
            return {"status": "success"}
        return {"status": "error", "message": "Object not found"}

    def duplicate_object(self, name, location=None):
        obj = bpy.data.objects.get(name)
        if not obj: return {"status": "error", "message": "Object not found"}
        new_obj = obj.copy()
        new_obj.data = obj.data.copy()
        bpy.context.collection.objects.link(new_obj)
        if location: new_obj.location = location
        return {"status": "success", "new_name": new_obj.name}

    def rename_object(self, old_name, new_name):
        obj = bpy.data.objects.get(old_name)
        if obj:
            obj.name = new_name
            return {"status": "success"}
        return {"status": "error", "message": "Object not found"}

    def set_parent(self, child_name, parent_name):
        child = bpy.data.objects.get(child_name)
        parent = bpy.data.objects.get(parent_name)
        if child and parent:
            child.parent = parent
            return {"status": "success"}
        return {"status": "error", "message": "Objects not found"}

    def clear_parent(self, name):
        obj = bpy.data.objects.get(name)
        if obj:
            obj.parent = None
            return {"status": "success"}
        return {"status": "error", "message": "Object not found"}

    def hide_object(self, name, hide=True):
        obj = bpy.data.objects.get(name)
        if obj:
            obj.hide_viewport = hide
            obj.hide_render = hide
            return {"status": "success"}
        return {"status": "error", "message": "Object not found"}

    # Mesh Ops
    def add_torus(self, location=(0,0,0), name="Torus"):
        bpy.ops.mesh.primitive_torus_add(location=location)
        bpy.context.active_object.name = name
        return {"status": "success"}

    def add_monkey(self, location=(0,0,0), name="Suzanne"):
        bpy.ops.mesh.primitive_monkey_add(location=location)
        bpy.context.active_object.name = name
        return {"status": "success"}

    def add_icosphere(self, location=(0,0,0), subdivisions=2, name="IcoSphere"):
        bpy.ops.mesh.primitive_ico_sphere_add(location=location, subdivisions=subdivisions)
        bpy.context.active_object.name = name
        return {"status": "success"}

    def subdivide_mesh(self, name, cuts=1):
        obj = bpy.data.objects.get(name)
        if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid object"}
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.subdivide(number_cuts=cuts)
        bpy.ops.object.mode_set(mode='OBJECT')
        return {"status": "success"}

    def shade_smooth(self, name, smooth=True):
        obj = bpy.data.objects.get(name)
        if not obj or obj.type != 'MESH': return {"status": "error", "message": "Invalid object"}
        if smooth:
            bpy.ops.object.shade_smooth({"selected_editable_objects": [obj]})
        else:
            bpy.ops.object.shade_flat({"selected_editable_objects": [obj]})
        return {"status": "success"}

    def add_modifier(self, name, type="SUBSURF", **kwargs):
        obj = bpy.data.objects.get(name)
        if not obj:
            return {"status": "error", "message": f"Object {name} not found"}

        mod = obj.modifiers.new(name="MCP_Modifier", type=type)
        for key, value in kwargs.items():
            if hasattr(mod, key):
                setattr(mod, key, value)
        return {"status": "success", "modifier": mod.name}

    def assign_material(self, name, color=(0.8, 0.8, 0.8, 1.0), metallic=0.0, roughness=0.5):
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

    def remove_material(self, name):
        obj = bpy.data.objects.get(name)
        if obj and hasattr(obj.data, 'materials'):
            obj.data.materials.clear()
            return {"status": "success"}
        return {"status": "error"}

    def set_material_property(self, mat_name, node_name, input_index, value):
        mat = bpy.data.materials.get(mat_name)
        if not mat or not mat.use_nodes: return {"status": "error"}
        node = mat.node_tree.nodes.get(node_name)
        if node and len(node.inputs) > input_index:
            node.inputs[input_index].default_value = value
            return {"status": "success"}
        return {"status": "error"}

    def add_texture_image(self, mat_name, image_path):
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

    def set_world_background(self, color=(0.05, 0.05, 0.05, 1.0), strength=1.0):
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

    # Lights & Camera
    def add_light(self, type='POINT', location=(0,0,0), name="Light"):
        light_data = bpy.data.lights.new(name=name, type=type)
        light_obj = bpy.data.objects.new(name=name, object_data=light_data)
        bpy.context.collection.objects.link(light_obj)
        light_obj.location = location
        return {"status": "success", "name": light_obj.name}

    def set_light_property(self, name, energy=10.0, color=(1,1,1)):
        obj = bpy.data.objects.get(name)
        if obj and obj.type == 'LIGHT':
            obj.data.energy = energy
            obj.data.color = color
            return {"status": "success"}
        return {"status": "error"}

    def add_camera(self, location=(0,0,0), rotation=(0,0,0), name="Camera"):
        cam_data = bpy.data.cameras.new(name)
        cam_obj = bpy.data.objects.new(name, cam_data)
        bpy.context.collection.objects.link(cam_obj)
        cam_obj.location = location
        cam_obj.rotation_euler = [(r * 3.14159 / 180.0) for r in rotation]
        return {"status": "success", "name": cam_obj.name}

    def set_active_camera(self, name):
        obj = bpy.data.objects.get(name)
        if obj and obj.type == 'CAMERA':
            bpy.context.scene.camera = obj
            return {"status": "success"}
        return {"status": "error"}

    # Modifiers Expansion
    def remove_modifier(self, obj_name, mod_name):
        obj = bpy.data.objects.get(obj_name)
        mod = obj.modifiers.get(mod_name)
        if obj and mod:
            obj.modifiers.remove(mod)
            return {"status": "success"}
        return {"status": "error"}

    def apply_modifier(self, obj_name, mod_name):
        obj = bpy.data.objects.get(obj_name)
        if obj:
            bpy.context.view_layer.objects.active = obj
            try:
                bpy.ops.object.modifier_apply(modifier=mod_name)
                return {"status": "success"}
            except: return {"status": "error"}
        return {"status": "error"}

    # Physics Expansion
    def setup_cloth(self, name):
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_add(type='CLOTH')
            return {"status": "success"}
        return {"status": "error"}

    def setup_collision(self, name):
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_add(type='COLLISION')
            return {"status": "success"}
        return {"status": "error"}

    def add_force_field(self, type='WIND', location=(0,0,0)):
        bpy.ops.object.effector_add(type=type, location=location)
        return {"status": "success", "name": bpy.context.active_object.name}

    def setup_geometry_nodes(self, name):
        obj = bpy.data.objects.get(name)
        if not obj:
            return {"status": "error", "message": f"Object {name} not found"}

        mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
        # Create a new node group if empty
        if not mod.node_group:
            node_group = bpy.data.node_groups.new(f"GN_{name}", 'GeometryNodeTree')
            mod.node_group = node_group
            # Add Input/Output nodes
            node_group.nodes.new('NodeGroupInput')
            node_group.nodes.new('NodeGroupOutput')
        return {"status": "success", "modifier": mod.name, "node_group": mod.node_group.name}

    def setup_physics(self, name, type='RIGID_BODY', physics_type='ACTIVE'):
        obj = bpy.data.objects.get(name)
        if not obj:
            return {"status": "error", "message": f"Object {name} not found"}

        if type == 'RIGID_BODY':
            bpy.context.view_layer.objects.active = obj
            bpy.ops.rigidbody.object_add()
            obj.rigid_body.type = physics_type

        return {"status": "success"}

    def create_node(self, tree_type, tree_name, node_type, location=(0, 0), properties=None):
        if tree_type == 'MATERIAL':
            mat = bpy.data.materials.get(tree_name)
            if not mat: return {"status": "error", "message": "Material not found"}
            tree = mat.node_tree
        elif tree_type == 'GEOMETRY':
            tree = bpy.data.node_groups.get(tree_name)
            if not tree: return {"status": "error", "message": "Node group not found"}
        elif tree_type == 'WORLD':
            world = bpy.data.worlds.get(tree_name)
            if not world: return {"status": "error"}
            tree = world.node_tree
        else:
            return {"status": "error", "message": "Invalid tree type"}

        node = tree.nodes.new(type=node_type)
        node.location = location
        if properties:
            for key, value in properties.items():
                if hasattr(node, key):
                    setattr(node, key, value)

        return {"status": "success", "node_name": node.name}

    def remove_node(self, tree_type, tree_name, node_name):
        if tree_type == 'MATERIAL':
            tree = bpy.data.materials.get(tree_name).node_tree
        elif tree_type == 'GEOMETRY':
            tree = bpy.data.node_groups.get(tree_name)
        elif tree_type == 'WORLD':
            tree = bpy.data.worlds.get(tree_name).node_tree

        node = tree.nodes.get(node_name)
        if node:
            tree.nodes.remove(node)
            return {"status": "success"}
        return {"status": "error"}

    def set_node_property(self, tree_type, tree_name, node_name, prop_name, value):
        if tree_type == 'MATERIAL':
            tree = bpy.data.materials.get(tree_name).node_tree
        elif tree_type == 'GEOMETRY':
            tree = bpy.data.node_groups.get(tree_name)
        elif tree_type == 'WORLD':
            tree = bpy.data.worlds.get(tree_name).node_tree

        node = tree.nodes.get(node_name)
        if node and hasattr(node, prop_name):
            setattr(node, prop_name, value)
            return {"status": "success"}
        return {"status": "error"}

    def connect_nodes(self, tree_type, tree_name, from_node, from_socket, to_node, to_socket):
        if tree_type == 'MATERIAL':
            mat = bpy.data.materials.get(tree_name)
            tree = mat.node_tree
        elif tree_type == 'GEOMETRY':
            tree = bpy.data.node_groups.get(tree_name)

        node_from = tree.nodes.get(from_node)
        node_to = tree.nodes.get(to_node)

        tree.links.new(node_from.outputs[from_socket], node_to.inputs[to_socket])
        return {"status": "success"}

    def set_keyframe(self, name, property, frame):
        obj = bpy.data.objects.get(name)
        if obj:
            obj.keyframe_insert(data_path=property, frame=frame)
            return {"status": "success"}
        return {"status": "error"}

    def set_timeline(self, start, end):
        bpy.context.scene.frame_start = start
        bpy.context.scene.frame_end = end
        return {"status": "success"}

    def set_current_frame(self, frame):
        bpy.context.scene.frame_set(frame)
        return {"status": "success"}

    # Collections
    def create_collection(self, name):
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
        return {"status": "success"}

    def add_to_collection(self, obj_name, col_name):
        obj = bpy.data.objects.get(obj_name)
        col = bpy.data.collections.get(col_name)
        if obj and col:
            col.objects.link(obj)
            return {"status": "success"}
        return {"status": "error"}

    # Scene & Rendering
    def clear_scene(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        return {"status": "success"}

    def set_render_engine(self, engine='CYCLES'):
        bpy.context.scene.render.engine = engine
        return {"status": "success"}

    def set_resolution(self, x, y):
        bpy.context.scene.render.resolution_x = x
        bpy.context.scene.render.resolution_y = y
        return {"status": "success"}

    def render_still(self, path):
        bpy.context.scene.render.filepath = path
        bpy.ops.render.render(write_still=True)
        return {"status": "success"}

    # Constraints
    def add_constraint(self, obj_name, type='TRACK_TO', target_name=None):
        obj = bpy.data.objects.get(obj_name)
        if not obj: return {"status": "error"}
        con = obj.constraints.new(type=type)
        if target_name:
            con.target = bpy.data.objects.get(target_name)
        return {"status": "success", "name": con.name}

    # Selection & Context
    def select_object(self, name, select=True):
        obj = bpy.data.objects.get(name)
        if obj:
            obj.select_set(select)
            return {"status": "success"}
        return {"status": "error"}

    def deselect_all(self):
        bpy.ops.object.select_all(action='DESELECT')
        return {"status": "success"}

    def set_active_object(self, name):
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.context.view_layer.objects.active = obj
            return {"status": "success"}
        return {"status": "error"}

    # Import/Export
    def import_obj(self, filepath):
        try:
            bpy.ops.import_scene.obj(filepath=filepath)
            return {"status": "success", "object": bpy.context.active_object.name}
        except: return {"status": "error"}

    def export_obj(self, filepath):
        try:
            bpy.ops.export_scene.obj(filepath=filepath)
            return {"status": "success"}
        except: return {"status": "error"}

    def get_screenshot(self):
        # Screenshot is handled by the UI bridge automatically before sending to Gemini
        return {"status": "success", "message": "Screenshot captured"}

    def get_scene_info(self):
        info = {
            "objects": [],
            "materials": [m.name for m in bpy.data.materials],
            "node_groups": [g.name for g in bpy.data.node_groups],
            "collections": [c.name for c in bpy.data.collections],
        }
        for obj in bpy.data.objects:
            obj_info = {
                "name": obj.name,
                "type": obj.type,
                "location": list(obj.location),
                "rotation": list(obj.rotation_euler),
                "modifiers": [m.name for m in obj.modifiers],
            }
            info["objects"].append(obj_info)
        return {"status": "success", "info": info}
