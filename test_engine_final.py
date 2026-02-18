import sys
import os
from unittest.mock import MagicMock

# Mock bpy
sys.modules['bpy'] = MagicMock()
sys.modules['bpy_extras'] = MagicMock()
sys.modules['gpu'] = MagicMock()
sys.modules['gpu_extras'] = MagicMock()

from blender_mcp.core.engine import AtomicEngine

def test_engine_loading():
    engine = AtomicEngine()
    print(f"Total tools registered: {len(engine.tools)}")

    # Check key tools from different modules
    essential_tools = [
        "create_primitive", "add_monkey", "assign_material",
        "add_light", "add_modifier", "setup_physics",
        "setup_geometry_nodes", "get_scene_info", "import_obj",
        "select_object", "setup_pbr_material", "audit_scene", "request_feedback"
    ]

    for tool in essential_tools:
        if tool in engine.tools:
            print(f"✓ {tool} registered")
        else:
            print(f"✗ {tool} MISSING")
            return False
    return True

if __name__ == "__main__":
    if test_engine_loading():
        print("Engine test PASSED")
    else:
        print("Engine test FAILED")
        sys.exit(1)
