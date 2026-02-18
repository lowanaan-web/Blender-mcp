bl_info = {
    "name": "Blender MCP (Gemini)",
    "author": "Jules",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Gemini",
    "description": "Advanced Gemini-powered assistant for Blender using MCP",
    "warning": "",
    "doc_url": "",
    "category": "Interface",
}

import bpy
from .utils import deps

class BlenderMCPPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    api_key: bpy.props.StringProperty(
        name="API Key",
        description="Enter your Gemini API Key",
        subtype='PASSWORD',
    )
    model_name: bpy.props.StringProperty(
        name="Model",
        description="Gemini Model ID",
        default="gemini-1.5-flash",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "api_key")
        layout.prop(self, "model_name")
        layout.operator("blender_mcp.install_deps")

class BLENDER_MCP_OT_InstallDeps(bpy.types.Operator):
    bl_idname = "blender_mcp.install_deps"
    bl_label = "Install Dependencies"
    bl_description = "Install required Python packages (google-generativeai, pywebview)"

    def execute(self, context):
        if deps.ensure_dependencies():
            self.report({'INFO'}, "Dependencies installed successfully")
        else:
            self.report({'ERROR'}, "Failed to install dependencies. Check console.")
        return {'FINISHED'}

class BLENDER_MCP_PT_MainPanel(bpy.types.Panel):
    bl_label = "Blender MCP"
    bl_idname = "BLENDER_MCP_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gemini'

    def draw(self, context):
        layout = self.layout
        layout.operator("blender_mcp.install_deps", icon='PACKAGE')
        layout.operator("blender_mcp.open_ui", icon='WORLD')

class BLENDER_MCP_OT_OpenUI(bpy.types.Operator):
    bl_idname = "blender_mcp.open_ui"
    bl_label = "Open Gemini Interface"

    def execute(self, context):
        # This will eventually launch the pywebview floating window
        from .ui import launcher
        launcher.launch()
        return {'FINISHED'}

classes = (
    BlenderMCPPreferences,
    BLENDER_MCP_OT_InstallDeps,
    BLENDER_MCP_PT_MainPanel,
    BLENDER_MCP_OT_OpenUI,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
