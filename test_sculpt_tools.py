import sys
from unittest.mock import MagicMock
sys.modules['bpy'] = MagicMock()
from blender_mcp.core.engine import AtomicEngine

def test_sculpt_tools():
    engine = AtomicEngine()
    sculpt_features = [
        "set_sculpt_mode", "select_brush", "toggle_dyntopo",
        "mask_all", "voxel_remesh", "set_sculpt_symmetry",
        "get_sculpt_stats", "toggle_steady_stroke"
    ]
    for f in sculpt_features:
        if f not in engine.tools:
            print(f"✗ {f} MISSING")
            return False
        print(f"✓ {f} registered")
    print(f"Total tools registered: {len(engine.tools)}")
    return True

if __name__ == "__main__":
    if test_sculpt_tools():
        print("Sculpt Tools test PASSED")
    else:
        sys.exit(1)
