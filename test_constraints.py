import sys
from unittest.mock import MagicMock
sys.modules['bpy'] = MagicMock()
from blender_mcp.core.engine import AtomicEngine

def test_constraints():
    engine = AtomicEngine()
    constraints = [
        "add_copy_location_constraint", "add_copy_rotation_constraint",
        "add_limit_location_constraint", "add_ik_constraint", "get_constraints_info"
    ]
    for c in constraints:
        if c not in engine.tools:
            print(f"✗ {c} MISSING")
            return False
        print(f"✓ {c} registered")
    return True

if __name__ == "__main__":
    if test_constraints():
        print("Constraints test PASSED")
    else:
        sys.exit(1)
