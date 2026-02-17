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
    if tree_type == 'MATERIAL':
        tree = bpy.data.materials.get(tree_name).node_tree
    elif tree_type == 'GEOMETRY':
        tree = bpy.data.node_groups.get(tree_name)

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
