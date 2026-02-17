import bpy
from .tools import (
    object, mesh, material, light, modifier,
    physics, node, animation, collection,
    scene, selection, constraint, io
)

class AtomicEngine:
    def __init__(self):
        self.tools = {
            # Object & Transform
            "create_primitive": object.create_primitive,
            "transform_object": object.transform_object,
            "delete_object": object.delete_object,
            "duplicate_object": object.duplicate_object,
            "rename_object": object.rename_object,
            "set_parent": object.set_parent,
            "clear_parent": object.clear_parent,
            "hide_object": object.hide_object,

            # Mesh Ops
            "add_torus": mesh.add_torus,
            "add_monkey": mesh.add_monkey,
            "add_icosphere": mesh.add_icosphere,
            "subdivide_mesh": mesh.subdivide_mesh,
            "shade_smooth": mesh.shade_smooth,

            # Materials & Textures
            "assign_material": material.assign_material,
            "remove_material": material.remove_material,
            "set_material_property": material.set_material_property,
            "add_texture_image": material.add_texture_image,
            "set_world_background": material.set_world_background,

            # Lighting & Camera
            "add_light": light.add_light,
            "set_light_property": light.set_light_property,
            "add_camera": light.add_camera,
            "set_active_camera": light.set_active_camera,

            # Modifiers
            "add_modifier": modifier.add_modifier,
            "remove_modifier": modifier.remove_modifier,
            "apply_modifier": modifier.apply_modifier,

            # Physics
            "setup_physics": physics.setup_physics,
            "setup_cloth": physics.setup_cloth,
            "setup_collision": physics.setup_collision,
            "add_force_field": physics.add_force_field,

            # Nodes
            "setup_geometry_nodes": node.setup_geometry_nodes,
            "create_node": node.create_node,
            "connect_nodes": node.connect_nodes,
            "remove_node": node.remove_node,
            "set_node_property": node.set_node_property,
            "create_node_group": node.create_node_group,
            "add_node_socket": node.add_node_socket,
            "set_node_socket_value": node.set_node_socket_value,
            "frame_nodes": node.frame_nodes,
            "get_node_tree_info": node.get_node_tree_info,

            # Animation
            "set_keyframe": animation.set_keyframe,
            "set_timeline": animation.set_timeline,
            "set_current_frame": animation.set_current_frame,

            # Collections
            "create_collection": collection.create_collection,
            "add_to_collection": collection.add_to_collection,

            # Scene & Rendering
            "get_scene_info": scene.get_scene_info,
            "get_screenshot": scene.get_screenshot,
            "clear_scene": scene.clear_scene,
            "set_render_engine": scene.set_render_engine,
            "set_resolution": scene.set_resolution,
            "render_still": scene.render_still,

            # Constraints
            "add_constraint": constraint.add_constraint,

            # Selection & Context
            "select_object": selection.select_object,
            "deselect_all": selection.deselect_all,
            "set_active_object": selection.set_active_object,

            # Import/Export
            "import_obj": io.import_obj,
            "export_obj": io.export_obj,
        }

    def execute_tool(self, tool_name, args):
        if tool_name in self.tools:
            try:
                return self.tools[tool_name](**args)
            except Exception as e:
                return {"status": "error", "message": str(e)}
        else:
            return {"status": "error", "message": f"Tool {tool_name} not found"}
