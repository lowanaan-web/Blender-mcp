import sys
from unittest.mock import MagicMock
sys.modules['bpy'] = MagicMock()
from blender_mcp.core.engine import AtomicEngine

def test_modeling_tools():
    engine = AtomicEngine()
    features = [
        "extrude_faces", "inset_faces", "loop_cut", "boolean_cut",
        "add_bezier_curve", "add_nurbs_path", "knife_project",
        "remove_doubles", "mesh_cleanup"
    ]
    for f in features:
        if f not in engine.tools:
            print(f"✗ {f} MISSING")
            return False
        print(f"✓ {f} registered")
    print(f"Total tools registered: {len(engine.tools)}")
    return True

if __name__ == "__main__":
    if test_modeling_tools():
        print("Modeling Tools test PASSED")
    else:
        sys.exit(1)
