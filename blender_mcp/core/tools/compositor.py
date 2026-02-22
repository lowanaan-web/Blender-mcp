import bpy

def enable_compositor(enable=True):
    bpy.context.scene.use_nodes = enable
    return {"status": "success", "enabled": enable}

def add_compositor_node(type, name=None, location=(0,0)):
    if not bpy.context.scene.use_nodes:
        bpy.context.scene.use_nodes = True

    node_tree = bpy.context.scene.node_tree
    node = node_tree.nodes.new(type)
    if name: node.name = name
    node.location = location
    return {"status": "success", "name": node.name}

def connect_compositor_nodes(from_node, from_socket, to_node, to_socket):
    node_tree = bpy.context.scene.node_tree
    start_node = node_tree.nodes.get(from_node)
    end_node = node_tree.nodes.get(to_node)

    if not start_node or not end_node: return {"status": "error"}

    # from_socket/to_socket can be index or name
    output = start_node.outputs[from_socket]
    input = end_node.inputs[to_socket]

    node_tree.links.new(output, input)
    return {"status": "success"}

def set_compositor_node_property(node_name, property, value):
    node_tree = bpy.context.scene.node_tree
    node = node_tree.nodes.get(node_name)
    if not node: return {"status": "error"}

    setattr(node, property, value)
    return {"status": "success"}
