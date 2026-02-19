import bpy

def setup_geometry_nodes(obj_name):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return {"status": "error", "message": f"Object {obj_name} not found"}
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="GeometryNodes", type='NODES')

    # In 4.0+, we use interface to manage sockets
    node_group = bpy.data.node_groups.new(name="Geometry Nodes", type='GeometryNodeTree')
    mod.node_group = node_group

    nodes = node_group.nodes
    node_in = nodes.new('NodeGroupInput')
    node_out = nodes.new('NodeGroupOutput')
    node_in.location = (-200, 0)
    node_out.location = (200, 0)

    # Add geometry socket via interface (4.0+ style)
    if hasattr(node_group, 'interface'):
        node_group.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        node_group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')

    node_group.links.new(node_in.outputs[0], node_out.inputs[0])
    return {"status": "success", "group_name": node_group.name}

def create_node(group_name, type, location=(0, 0)):
    group = bpy.data.node_groups.get(group_name)
    if not group: return {"status": "error", "message": f"Node group {group_name} not found"}
    node = group.nodes.new(type=type)
    node.location = location
    return {"status": "success", "node_name": node.name}

def connect_nodes(group_name, from_node, from_socket, to_node, to_socket):
    group = bpy.data.node_groups.get(group_name)
    if not group: return {"status": "error"}
    node_from = group.nodes.get(from_node)
    node_to = group.nodes.get(to_node)
    if not node_from or not node_to: return {"status": "error"}

    # 4.0+ handles sockets by name or index
    output = node_from.outputs[from_socket] if isinstance(from_socket, int) else node_from.outputs.get(from_socket)
    input = node_to.inputs[to_socket] if isinstance(to_socket, int) else node_to.inputs.get(to_socket)

    if output and input:
        group.links.new(output, input)
        return {"status": "success"}
    return {"status": "error"}

def add_node_socket(group_name, name, in_out='INPUT', socket_type='NodeSocketFloat'):
    group = bpy.data.node_groups.get(group_name)
    if not group: return {"status": "error"}
    if hasattr(group, 'interface'):
        # 4.0+ API
        group.interface.new_socket(name=name, in_out=in_out, socket_type=socket_type)
        return {"status": "success"}
    return {"status": "error", "message": "Interface not supported (requires Blender 4.0+)"}

def remove_socket_from_group(group_name, socket_index, in_out='INPUT'):
    group = bpy.data.node_groups.get(group_name)
    if not group: return {"status": "error"}
    if hasattr(group, 'interface'):
        # In 4.0+, we iterate interface items
        for i, item in enumerate(group.interface.items_tree):
            if i == socket_index and item.item_type == 'SOCKET' and item.in_out == in_out:
                group.interface.remove(item)
                return {"status": "success"}
    return {"status": "error"}

def create_node_panel(group_name, name):
    group = bpy.data.node_groups.get(group_name)
    if not group: return {"status": "error"}
    if hasattr(group, 'interface'):
        panel = group.interface.new_panel(name=name)
        return {"status": "success", "panel_name": panel.name}
    return {"status": "error"}

def move_node(group_name, node_name, x, y):
    group = bpy.data.node_groups.get(group_name)
    if not group: return {"status": "error"}
    node = group.nodes.get(node_name)
    if node:
        node.location = (x, y)
        return {"status": "success"}
    return {"status": "error"}

def set_node_label(group_name, node_name, label):
    group = bpy.data.node_groups.get(group_name)
    if not group: return {"status": "error"}
    node = group.nodes.get(node_name)
    if node:
        node.label = label
        return {"status": "success"}
    return {"status": "error"}

def template_scatter_objects(obj_name, instance_obj_name, density=10.0):
    res = setup_geometry_nodes(obj_name)
    if res["status"] == "error": return res
    group_name = res["group_name"]
    group = bpy.data.node_groups.get(group_name)
    nodes = group.nodes
    group.links.clear()

    node_in = next(n for n in nodes if n.type == 'GROUP_INPUT')
    node_out = next(n for n in nodes if n.type == 'GROUP_OUTPUT')

    node_dist = nodes.new('GeometryNodeDistributePointsOnFaces')
    node_dist.inputs['Density'].default_value = density

    node_inst = nodes.new('GeometryNodeInstanceOnPoints')
    node_inst.location = (200, 0)

    node_info = nodes.new('GeometryNodeObjectInfo')
    node_info.location = (0, -200)
    target_obj = bpy.data.objects.get(instance_obj_name)
    if target_obj:
        node_info.inputs[0].default_value = target_obj

    group.links.new(node_in.outputs[0], node_dist.inputs[0])
    group.links.new(node_dist.outputs[0], node_inst.inputs[0])
    group.links.new(node_info.outputs[3], node_inst.inputs[2]) # Geometry output
    group.links.new(node_inst.outputs[0], node_out.inputs[0])

    return {"status": "success"}

def remove_node(group_name, node_name):
    group = bpy.data.node_groups.get(group_name)
    if group:
        node = group.nodes.get(node_name)
        if node:
            group.nodes.remove(node)
            return {"status": "success"}
    return {"status": "error"}

def set_node_property(group_name, node_name, property_name, value):
    group = bpy.data.node_groups.get(group_name)
    if group:
        node = group.nodes.get(node_name)
        if node:
            if hasattr(node, property_name):
                setattr(node, property_name, value)
            elif property_name in node.inputs:
                node.inputs[property_name].default_value = value
            return {"status": "success"}
    return {"status": "error"}

def create_node_group(name, type='GeometryNodeTree'):
    group = bpy.data.node_groups.new(name=name, type=type)
    return {"status": "success", "group_name": group.name}

def set_node_socket_value(group_name, node_name, socket_name, value):
    return set_node_property(group_name, node_name, socket_name, value)

def template_random_displace(obj_name, strength=1.0, scale=1.0):
    res = setup_geometry_nodes(obj_name)
    if res["status"] == "error": return res
    group_name = res["group_name"]
    group = bpy.data.node_groups.get(group_name)
    nodes = group.nodes
    group.links.clear()

    node_in = next(n for n in nodes if n.type == 'GROUP_INPUT')
    node_out = next(n for n in nodes if n.type == 'GROUP_OUTPUT')

    node_noise = nodes.new('ShaderNodeTexNoise')
    node_noise.inputs['Scale'].default_value = scale

    node_vector_math = nodes.new('ShaderNodeVectorMath')
    node_vector_math.operation = 'SUBTRACT'
    node_vector_math.inputs[1].default_value = (0.5, 0.5, 0.5)

    node_displace = nodes.new('GeometryNodeSetPosition')

    node_math = nodes.new('ShaderNodeVectorMath')
    node_math.operation = 'SCALE'
    node_math.inputs[3].default_value = strength

    group.links.new(node_in.outputs[0], node_displace.inputs[0])
    group.links.new(node_noise.outputs[1], node_vector_math.inputs[0])
    group.links.new(node_vector_math.outputs[0], node_math.inputs[0])
    group.links.new(node_math.outputs[0], node_displace.inputs[3]) # Offset
    group.links.new(node_displace.outputs[0], node_out.inputs[0])

    return {"status": "success"}

def frame_nodes(group_name, node_names):
    group = bpy.data.node_groups.get(group_name)
    if not group: return {"status": "error"}
    frame = group.nodes.new('NodeFrame')
    for name in node_names:
        node = group.nodes.get(name)
        if node: node.parent = frame
    return {"status": "success", "frame_name": frame.name}

def align_nodes(group_name, node_names, axis='X'):
    group = bpy.data.node_groups.get(group_name)
    if not group: return {"status": "error"}
    nodes = [group.nodes.get(n) for n in node_names if group.nodes.get(n)]
    if not nodes: return {"status": "error"}
    if axis == 'X':
        avg = sum(n.location.x for n in nodes) / len(nodes)
        for n in nodes: n.location.x = avg
    else:
        avg = sum(n.location.y for n in nodes) / len(nodes)
        for n in nodes: n.location.y = avg
    return {"status": "success"}

def mute_node(group_name, node_name, mute=True):
    group = bpy.data.node_groups.get(group_name)
    if group:
        node = group.nodes.get(node_name)
        if node:
            node.mute = mute
            return {"status": "success"}
    return {"status": "error"}
