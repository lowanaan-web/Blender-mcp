from pathlib import Path

from blender_mcp.contracts import ToolVersion, build_default_registry
from blender_mcp.contracts.registry import TOOL_SCENE_CREATE_OBJECT


REQUIRED_HEADINGS = [
    "## Canonical Model System",
    "## Versioning Rules",
    "## Validation Rules",
    "## Error Envelope",
    "## CI Enforcement",
]


def test_contract_policy_document_has_required_sections() -> None:
    policy = Path("docs/contracts.md")
    assert policy.exists(), "docs/contracts.md must exist"

    content = policy.read_text(encoding="utf-8")
    for heading in REQUIRED_HEADINGS:
        assert heading in content, f"Missing required policy heading: {heading}"


def test_registered_tools_support_v1_and_v1_1() -> None:
    registry = build_default_registry()
    versions = registry.list_versions(TOOL_SCENE_CREATE_OBJECT)

    assert ToolVersion.V1 in versions
    assert ToolVersion.V1_1 in versions
