import google.generativeai as genai
import json
import re

class GeminiManager:
    def __init__(self, api_key, model_name="gemini-1.5-flash"):
        genai.configure(api_key=api_key)

        self.system_instruction = """
You are an expert Blender Assistant. Your goal is to help users build, control, and setup 3D scenes in Blender.
You communicate using natural language but when you need to perform actions, you MUST use the following atomic tools in JSON format.
Wrap your tool calls inside <blender_cmd> tags.

Available Tools:
- create_primitive(type, location, scale, name): type in [CUBE, SPHERE, PLANE, CYLINDER]
- transform_object(name, location, rotation, scale)
- add_modifier(name, type, **kwargs): types like SUBSURF, MIRROR, BEVEL
- assign_material(name, color, metallic, roughness): color is (R, G, B, A)
- setup_geometry_nodes(name)
- create_node(tree_type, tree_name, node_type, location, properties): tree_type in [MATERIAL, GEOMETRY]
- connect_nodes(tree_type, tree_name, from_node, from_socket, to_node, to_socket)
- get_scene_info()
- get_screenshot(): This tool is handled automatically but you can request it if needed.

Example:
To create a red cube:
"I'll create a red cube for you."
<blender_cmd>
{
  "tool": "create_primitive",
  "args": {"type": "CUBE", "name": "MyCube"}
}
</blender_cmd>
<blender_cmd>
{
  "tool": "assign_material",
  "args": {"name": "MyCube", "color": [1, 0, 0, 1]}
}
</blender_cmd>

Important:
- Use atomic tools to build complex scenes step-by-step.
- After performing actions, you can suggest next steps or ask the user if they want you to verify the results.
- You have VISION capabilities. You receive a screenshot of the viewport with every message. Use it to verify your work.
- If you need a fresh screenshot or more scene data, you can ask the user or use get_scene_info().
- Always provide a brief explanation of what you are doing.
"""
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=self.system_instruction
        )
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message, image_data=None):
        content = []
        if image_data:
            content.append({"mime_type": "image/png", "data": image_data})
        content.append(message)

        response = self.chat.send_message(content)
        return response.text

    def extract_commands(self, text):
        pattern = r"<blender_cmd>(.*?)</blender_cmd>"
        commands = re.findall(pattern, text, re.DOTALL)
        parsed_commands = []
        for cmd_str in commands:
            try:
                parsed_commands.append(json.loads(cmd_str.strip()))
            except json.JSONDecodeError:
                print(f"Failed to parse command: {cmd_str}")
        return parsed_commands
