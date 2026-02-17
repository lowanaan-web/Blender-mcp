import bpy
import json
import mathutils

class AtomicEngine:
    def __init__(self):
        self.tools = {
            "create_primitive": self.create_primitive,
            "transform_object": self.transform_object,
            "add_modifier": self.add_modifier,
            "assign_material": self.assign_material,
            "setup_geometry_nodes": self.setup_geometry_nodes,
            "setup_physics": self.setup_physics,
            "create_node": self.create_node,
            "connect_nodes": self.connect_nodes,
            "get_scene_info": self.get_scene_info,
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
            obj.rotation_euler = rotation
        if scale:
            obj.scale = scale
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

        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
        return {"status": "success", "material": mat.name}

    def setup_geometry_nodes(self, name):
        obj = bpy.data.objects.get(name)
        if not obj:
            return {"status": "error", "message": f"Object {name} not found"}

        mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
        # Basic setup, agent would need more tools to manipulate the node tree
        return {"status": "success", "modifier": mod.name}

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
        # tree_type can be 'ShaderNodeTree', 'GeometryNodeTree'
        if tree_type == 'MATERIAL':
            mat = bpy.data.materials.get(tree_name)
            if not mat: return {"status": "error", "message": "Material not found"}
            tree = mat.node_tree
        elif tree_type == 'GEOMETRY':
            tree = bpy.data.node_groups.get(tree_name)
            if not tree: return {"status": "error", "message": "Node group not found"}
        else:
            return {"status": "error", "message": "Invalid tree type"}

        node = tree.nodes.new(type=node_type)
        node.location = location
        if properties:
            for key, value in properties.items():
                if hasattr(node, key):
                    setattr(node, key, value)

        return {"status": "success", "node_name": node.name}

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

    def get_scene_info(self):
        info = {
            "objects": [],
            "materials": [m.name for m in bpy.data.materials],
            "node_groups": [g.name for g in bpy.data.node_groups],
        }
        for obj in bpy.data.objects:
            obj_info = {
                "name": obj.name,
                "type": obj.type,
                "location": list(obj.location),
                "modifiers": [m.name for m in obj.modifiers],
            }
            info["objects"].append(obj_info)
        return {"status": "success", "info": info}
