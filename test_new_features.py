import sys
from unittest.mock import MagicMock
sys.modules['bpy'] = MagicMock()
from blender_mcp.core.engine import AtomicEngine

def test_new_features():
    engine = AtomicEngine()
    features = [
        "setup_rigid_body_world", "add_rigid_body_constraint", "setup_dynamic_paint_canvas",
        "template_scatter_objects", "template_random_displace", "setup_glass_material",
        "bake_action", "create_action_constraint"
    ]
    for f in features:
        if f not in engine.tools:
            print(f"✗ {f} MISSING")
            return False
        print(f"✓ {f} registered")
    return True

if __name__ == "__main__":
    if test_new_features():
        print("New Features test PASSED")
    else:
        sys.exit(1)
