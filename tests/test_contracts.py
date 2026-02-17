from blender_mcp.contracts import ContractExecutor, ToolVersion, build_default_registry
from blender_mcp.contracts.registry import TOOL_SCENE_CREATE_OBJECT


def test_happy_path_v1_1_execution() -> None:
    executor = ContractExecutor(build_default_registry())
    result = executor.execute(
        tool_name=TOOL_SCENE_CREATE_OBJECT,
        version=ToolVersion.V1_1,
        payload={
            "tool_name": TOOL_SCENE_CREATE_OBJECT,
            "trace_id": "trace_12345678",
            "object_type": "MESH",
            "name": "Wing",
            "location": [1.0, 2.0, 3.0],
        },
    )

    assert result["ok"] is True
    assert result["data"]["api_revision"] == "1.1"


def test_request_validation_blocks_execution() -> None:
    executor = ContractExecutor(build_default_registry())
    result = executor.execute(
        tool_name=TOOL_SCENE_CREATE_OBJECT,
        version=ToolVersion.V1,
        payload={
            "tool_name": TOOL_SCENE_CREATE_OBJECT,
            "trace_id": "trace_12345678",
            "name": "NoType",
        },
    )

    assert result["ok"] is False
    assert result["error"]["code"] == "invalid_request"


def test_unsupported_contract_returns_standard_error() -> None:
    executor = ContractExecutor(build_default_registry())
    result = executor.execute(
        tool_name="unknown.tool",
        version=ToolVersion.V1,
        payload={"trace_id": "trace_12345678"},
    )

    assert result["ok"] is False
    assert set(result["error"]).issuperset(
        {"code", "message", "recoverable", "next_actions", "trace_id"}
    )
