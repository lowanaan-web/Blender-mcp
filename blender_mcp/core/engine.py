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
            "move_to_collection": object.move_to_collection,
            "apply_transform": object.apply_transform,
            "clear_transform": object.clear_transform,
            "set_origin": object.set_origin,
            "add_empty": object.add_empty,
            "join_objects": object.join_objects,
            "separate_objects": object.separate_objects,
            "make_instance": object.make_instance,
            "convert_object": object.convert_object,
            "align_objects": object.align_objects,
            "randomize_transform": object.randomize_transform,
            "copy_transforms": object.copy_transforms,
            "snap_to_cursor": object.snap_to_cursor,
            "snap_cursor_to_object": object.snap_cursor_to_object,
            "get_object_dimensions": object.get_object_dimensions,
            "set_object_dimensions": object.set_object_dimensions,
            "set_display_color": object.set_display_color,
            "set_draw_type": object.set_draw_type,
            "make_local": object.make_local,
            "set_object_pass_index": object.set_object_pass_index,

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
            "add_subsurf_modifier": modifier.add_subsurf_modifier,
            "add_solidify_modifier": modifier.add_solidify_modifier,
            "add_bevel_modifier": modifier.add_bevel_modifier,
            "add_boolean_modifier": modifier.add_boolean_modifier,
            "add_array_modifier": modifier.add_array_modifier,
            "add_mirror_modifier": modifier.add_mirror_modifier,
            "add_decimate_modifier": modifier.add_decimate_modifier,
            "add_displace_modifier": modifier.add_displace_modifier,
            "add_mask_modifier": modifier.add_mask_modifier,
            "add_multires_modifier": modifier.add_multires_modifier,
            "add_remesh_modifier": modifier.add_remesh_modifier,
            "add_screw_modifier": modifier.add_screw_modifier,
            "add_skin_modifier": modifier.add_skin_modifier,
            "add_triangulate_modifier": modifier.add_triangulate_modifier,
            "add_wireframe_modifier": modifier.add_wireframe_modifier,
            "add_simple_deform_modifier": modifier.add_simple_deform_modifier,
            "add_curve_modifier": modifier.add_curve_modifier,
            "add_warp_modifier": modifier.add_warp_modifier,
            "add_wave_modifier": modifier.add_wave_modifier,
            "add_cast_modifier": modifier.add_cast_modifier,
            "add_surface_deform_modifier": modifier.add_surface_deform_modifier,
            "add_mesh_deform_modifier": modifier.add_mesh_deform_modifier,
            "add_smooth_corrective_modifier": modifier.add_smooth_corrective_modifier,
            "add_laplacian_smooth_modifier": modifier.add_laplacian_smooth_modifier,
            "add_hook_modifier": modifier.add_hook_modifier,
            "add_lattice_modifier": modifier.add_lattice_modifier,
            "add_shrinkwrap_modifier": modifier.add_shrinkwrap_modifier,
            "add_data_transfer_modifier": modifier.add_data_transfer_modifier,
            "add_weighted_normal_modifier": modifier.add_weighted_normal_modifier,

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
            "move_node": node.move_node,
            "duplicate_node": node.duplicate_node,
            "set_node_label": node.set_node_label,
            "set_node_color": node.set_node_color,
            "set_node_use_custom_color": node.set_node_use_custom_color,
            "mute_node": node.mute_node,
            "set_node_width": node.set_node_width,
            "disconnect_nodes": node.disconnect_nodes,
            "add_node_reroute": node.add_node_reroute,
            "add_input_socket_to_group": node.add_input_socket_to_group,
            "add_output_socket_to_group": node.add_output_socket_to_group,
            "remove_socket_from_group": node.remove_socket_from_group,
            "move_socket_in_group": node.move_socket_in_group,
            "set_socket_interface_details": node.set_socket_interface_details,
            "clear_node_tree": node.clear_node_tree,
            "align_nodes": node.align_nodes,
            "expose_to_group": node.expose_to_group,
            "get_node_properties": node.get_node_properties,
            "get_node_sockets": node.get_node_sockets,
            "select_node": node.select_node,
            "deselect_all_nodes": node.deselect_all_nodes,
            "set_active_node": node.set_active_node,

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
            "set_render_samples": scene.set_render_samples,
            "set_denoising": scene.set_denoising,
            "set_color_management": scene.set_color_management,
            "set_output_format": scene.set_output_format,
            "set_background_transparent": scene.set_background_transparent,
            "add_view_layer": scene.add_view_layer,
            "set_render_device": scene.set_render_device,
            "bake_physics": scene.bake_physics,
            "set_viewport_shading": scene.set_viewport_shading,
            "toggle_overlays": scene.toggle_overlays,
            "set_clipping": scene.set_clipping,
            "add_sun_light_env": scene.add_sun_light_env,
            "set_mist_pass": scene.set_mist_pass,
            "setup_compositor_denoise": scene.setup_compositor_denoise,
            "set_render_region": scene.set_render_region,
            "toggle_simplify": scene.toggle_simplify,
            "set_gravity": scene.set_gravity,
            "set_units": scene.set_units,
            "get_render_info": scene.get_render_info,
            "save_file": scene.save_file,

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

    def execute_tool(self, tool_name, args=None):
        if tool_name in self.tools:
            try:
                if args is None: args = {}
                return self.tools[tool_name](**args)
            except Exception as e:
                return {"status": "error", "message": str(e)}
        else:
            return {"status": "error", "message": f"Tool {tool_name} not found"}
