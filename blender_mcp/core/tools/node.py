import bpy

def setup_geometry_nodes(name):
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"status": "error", "message": f"Object {name} not found"}

    mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
    if not mod.node_group:
        node_group = bpy.data.node_groups.new(f"GN_{name}", 'GeometryNodeTree')
        mod.node_group = node_group
        node_group.nodes.new('NodeGroupInput')
        node_group.nodes.new('NodeGroupOutput')
    return {"status": "success", "modifier": mod.name, "node_group": mod.node_group.name}

def create_node(tree_type, tree_name, node_type, location=(0, 0), properties=None):
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

def remove_node(tree_type, tree_name, node_name):
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

def set_node_property(tree_type, tree_name, node_name, prop_name, value):
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

def connect_nodes(tree_type, tree_name, from_node, from_socket, to_node, to_socket):
    if tree_type == 'MATERIAL':
        tree = bpy.data.materials.get(tree_name).node_tree
    elif tree_type == 'GEOMETRY':
        tree = bpy.data.node_groups.get(tree_name)
    elif tree_type == 'WORLD':
        tree = bpy.data.worlds.get(tree_name).node_tree

    node_from = tree.nodes.get(from_node)
    node_to = tree.nodes.get(to_node)

    out_socket = node_from.outputs[from_socket] if isinstance(from_socket, int) else node_from.outputs.get(from_socket)
    in_socket = node_to.inputs[to_socket] if isinstance(to_socket, int) else node_to.inputs.get(to_socket)

    tree.links.new(out_socket, in_socket)
    return {"status": "success"}

def create_node_group(name, type='GeometryNodeTree'):
    group = bpy.data.node_groups.new(name, type)
    return {"status": "success", "name": group.name}

def add_node_socket(tree_type, tree_name, socket_type='NodeSocketFloat', in_out='INPUT', name='Socket'):
    if tree_type == 'GEOMETRY':
        tree = bpy.data.node_groups.get(tree_name)
    elif tree_type == 'MATERIAL':
        tree = bpy.data.materials.get(tree_name).node_tree

    if in_out == 'INPUT':
        socket = tree.inputs.new(socket_type, name)
    else:
        socket = tree.outputs.new(socket_type, name)
    return {"status": "success", "socket_name": socket.name}

def set_node_socket_value(tree_type, tree_name, node_name, socket_name, value, is_output=False):
    if tree_type == 'MATERIAL':
        tree = bpy.data.materials.get(tree_name).node_tree
    elif tree_type == 'GEOMETRY':
        tree = bpy.data.node_groups.get(tree_name)

    node = tree.nodes.get(node_name)
    sockets = node.outputs if is_output else node.inputs
    socket = sockets.get(socket_name)
    if socket:
        socket.default_value = value
        return {"status": "success"}
    return {"status": "error"}

def frame_nodes(tree_type, tree_name, node_names, frame_name="Frame"):
    if tree_type == 'MATERIAL':
        tree = bpy.data.materials.get(tree_name).node_tree
    elif tree_type == 'GEOMETRY':
        tree = bpy.data.node_groups.get(tree_name)

    frame = tree.nodes.new('NodeFrame')
    frame.label = frame_name
    for name in node_names:
        node = tree.nodes.get(name)
        if node:
            node.parent = frame
    return {"status": "success", "frame_name": frame.name}

def get_node_tree_info(tree_type, tree_name):
    tree = _get_tree(tree_type, tree_name)
    if not tree: return {"status": "error"}

    info = {"nodes": [], "links": []}
    for node in tree.nodes:
        info["nodes"].append({"name": node.name, "type": node.type, "location": list(node.location)})
    for link in tree.links:
        info["links"].append({
            "from_node": link.from_node.name,
            "from_socket": link.from_socket.name,
            "to_node": link.to_node.name,
            "to_socket": link.to_socket.name
        })
    return {"status": "success", "info": info}

def _get_tree(tree_type, tree_name):
    if tree_type == 'MATERIAL':
        mat = bpy.data.materials.get(tree_name)
        return mat.node_tree if mat else None
    elif tree_type == 'GEOMETRY':
        return bpy.data.node_groups.get(tree_name)
    elif tree_type == 'WORLD':
        world = bpy.data.worlds.get(tree_name)
        return world.node_tree if world else None
    return None

def move_node(tree_type, tree_name, node_name, location):
    tree = _get_tree(tree_type, tree_name)
    node = tree.nodes.get(node_name)
    if node:
        node.location = location
        return {"status": "success"}
    return {"status": "error"}

def duplicate_node(tree_type, tree_name, node_name, location=None):
    tree = _get_tree(tree_type, tree_name)
    node = tree.nodes.get(node_name)
    if node:
        new_node = tree.nodes.new(node.bl_idname)
        if location: new_node.location = location
        else: new_node.location = (node.location[0] + 30, node.location[1] - 30)
        return {"status": "success", "node_name": new_node.name}
    return {"status": "error"}

def set_node_label(tree_type, tree_name, node_name, label):
    tree = _get_tree(tree_type, tree_name)
    node = tree.nodes.get(node_name)
    if node:
        node.label = label
        return {"status": "success"}
    return {"status": "error"}

def set_node_color(tree_type, tree_name, node_name, color):
    tree = _get_tree(tree_type, tree_name)
    node = tree.nodes.get(node_name)
    if node:
        node.use_custom_color = True
        node.color = color
        return {"status": "success"}
    return {"status": "error"}

def set_node_use_custom_color(tree_type, tree_name, node_name, use=True):
    tree = _get_tree(tree_type, tree_name)
    node = tree.nodes.get(node_name)
    if node:
        node.use_custom_color = use
        return {"status": "success"}
    return {"status": "error"}

def mute_node(tree_type, tree_name, node_name, mute=True):
    tree = _get_tree(tree_type, tree_name)
    node = tree.nodes.get(node_name)
    if node:
        node.mute = mute
        return {"status": "success"}
    return {"status": "error"}

def set_node_width(tree_type, tree_name, node_name, width):
    tree = _get_tree(tree_type, tree_name)
    node = tree.nodes.get(node_name)
    if node:
        node.width = width
        return {"status": "success"}
    return {"status": "error"}

def disconnect_nodes(tree_type, tree_name, to_node, to_socket):
    tree = _get_tree(tree_type, tree_name)
    node_to = tree.nodes.get(to_node)
    in_socket = node_to.inputs[to_socket] if isinstance(to_socket, int) else node_to.inputs.get(to_socket)
    for link in in_socket.links:
        tree.links.remove(link)
    return {"status": "success"}

def add_node_reroute(tree_type, tree_name, location=(0,0)):
    tree = _get_tree(tree_type, tree_name)
    node = tree.nodes.new('NodeReroute')
    node.location = location
    return {"status": "success", "node_name": node.name}

def add_input_socket_to_group(group_name, socket_type='NodeSocketFloat', name='Input'):
    group = bpy.data.node_groups.get(group_name)
    if group:
        socket = group.inputs.new(socket_type, name)
        return {"status": "success", "name": socket.name}
    return {"status": "error"}

def add_output_socket_to_group(group_name, socket_type='NodeSocketFloat', name='Output'):
    group = bpy.data.node_groups.get(group_name)
    if group:
        socket = group.outputs.new(socket_type, name)
        return {"status": "success", "name": socket.name}
    return {"status": "error"}

def remove_socket_from_group(group_name, socket_name, is_output=False):
    group = bpy.data.node_groups.get(group_name)
    if group:
        sockets = group.outputs if is_output else group.inputs
        socket = sockets.get(socket_name)
        if socket:
            sockets.remove(socket)
            return {"status": "success"}
    return {"status": "error"}

def move_socket_in_group(group_name, socket_name, direction='UP', is_output=False):
    group = bpy.data.node_groups.get(group_name)
    if group:
        sockets = group.outputs if is_output else group.inputs
        index = sockets.find(socket_name)
        if index != -1:
            if direction == 'UP' and index > 0:
                sockets.move(index, index - 1)
            elif direction == 'DOWN' and index < len(sockets) - 1:
                sockets.move(index, index + 1)
            return {"status": "success"}
    return {"status": "error"}

def set_socket_interface_details(group_name, socket_name, min_val=0.0, max_val=1.0, default_val=0.5, is_output=False):
    group = bpy.data.node_groups.get(group_name)
    if group:
        sockets = group.outputs if is_output else group.inputs
        socket = sockets.get(socket_name)
        if socket:
            if hasattr(socket, "min_value"): socket.min_value = min_val
            if hasattr(socket, "max_value"): socket.max_value = max_val
            if hasattr(socket, "default_value"): socket.default_value = default_val
            return {"status": "success"}
    return {"status": "error"}

def clear_node_tree(tree_type, tree_name):
    tree = _get_tree(tree_type, tree_name)
    if tree:
        tree.nodes.clear()
        return {"status": "success"}
    return {"status": "error"}

def align_nodes(tree_type, tree_name, node_names, axis='X'):
    tree = _get_tree(tree_type, tree_name)
    objs = [tree.nodes.get(n) for n in node_names if tree.nodes.get(n)]
    if not objs: return {"status": "error"}
    ref_idx = 0 if axis == 'X' else 1
    ref_val = objs[0].location[ref_idx]
    for node in objs[1:]:
        loc = list(node.location)
        loc[ref_idx] = ref_val
        node.location = tuple(loc)
    return {"status": "success"}

def expose_to_group(tree_type, tree_name, node_name, socket_name):
    tree = _get_tree(tree_type, tree_name)
    node = tree.nodes.get(node_name)
    socket = node.inputs.get(socket_name)
    if not tree or not node or not socket: return {"status": "error"}

    # Only works for NodeGroups (Geometry Nodes or Shader Groups)
    if hasattr(tree, "inputs"):
        new_socket = tree.inputs.new(socket.bl_idname, socket.name)
        # Find Group Input node
        group_input = next((n for n in tree.nodes if n.type == 'GROUP_INPUT'), None)
        if not group_input:
            group_input = tree.nodes.new('NodeGroupInput')
        tree.links.new(group_input.outputs[new_socket.name], socket)
        return {"status": "success", "socket_name": new_socket.name}
    return {"status": "error"}

def get_node_properties(tree_type, tree_name, node_name):
    tree = _get_tree(tree_type, tree_name)
    node = tree.nodes.get(node_name)
    if node:
        # This is tricky as properties vary, but we can return basic metadata
        return {"status": "success", "type": node.type, "label": node.label, "mute": node.mute}
    return {"status": "error"}

def get_node_sockets(tree_type, tree_name, node_name):
    tree = _get_tree(tree_type, tree_name)
    node = tree.nodes.get(node_name)
    if node:
        return {
            "status": "success",
            "inputs": [s.name for s in node.inputs],
            "outputs": [s.name for s in node.outputs]
        }
    return {"status": "error"}

def select_node(tree_type, tree_name, node_name, select=True):
    tree = _get_tree(tree_type, tree_name)
    node = tree.nodes.get(node_name)
    if node:
        node.select = select
        return {"status": "success"}
    return {"status": "error"}

def deselect_all_nodes(tree_type, tree_name):
    tree = _get_tree(tree_type, tree_name)
    if tree:
        for node in tree.nodes:
            node.select = False
        return {"status": "success"}
    return {"status": "error"}

def set_active_node(tree_type, tree_name, node_name):
    tree = _get_tree(tree_type, tree_name)
    node = tree.nodes.get(node_name)
    if node:
        tree.nodes.active = node
        return {"status": "success"}
    return {"status": "error"}
