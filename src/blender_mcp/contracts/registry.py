"""Registry mapping tool + version to schemas and handlers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from pydantic import BaseModel

from .canonical import ToolVersion
from .schemas import (
    TOOL_SCENE_CREATE_OBJECT,
    SceneCreateObjectRequestV1,
    SceneCreateObjectRequestV11,
    SceneCreateObjectResponseV1,
    SceneCreateObjectResponseV11,
)

HandlerFn = Callable[[BaseModel], BaseModel]


@dataclass(frozen=True, slots=True)
class ToolContract:
    request_schema: type[BaseModel]
    response_schema: type[BaseModel]
    handler: HandlerFn


class ContractRegistry:
    """Production contract registry for versioned tool interfaces."""

    def __init__(self) -> None:
        self._contracts: dict[tuple[str, ToolVersion], ToolContract] = {}

    def register(
        self,
        *,
        tool_name: str,
        version: ToolVersion,
        request_schema: type[BaseModel],
        response_schema: type[BaseModel],
        handler: HandlerFn,
    ) -> None:
        key = (tool_name, version)
        if key in self._contracts:
            raise ValueError(f"Contract already registered for {tool_name=} {version=}")
        self._contracts[key] = ToolContract(
            request_schema=request_schema,
            response_schema=response_schema,
            handler=handler,
        )

    def resolve(self, tool_name: str, version: ToolVersion) -> ToolContract | None:
        return self._contracts.get((tool_name, version))

    def list_versions(self, tool_name: str) -> set[ToolVersion]:
        return {version for name, version in self._contracts if name == tool_name}


# Example production handlers (in real integrations these call Blender bridge services)
def _handle_scene_create_object_v1(request: SceneCreateObjectRequestV1) -> SceneCreateObjectResponseV1:
    object_id = f"obj::{request.object_type.lower()}::{request.name.lower()}"
    return SceneCreateObjectResponseV1(
        tool_name=request.tool_name,
        trace_id=request.trace_id,
        object_id=object_id,
        created=True,
    )


def _handle_scene_create_object_v11(request: SceneCreateObjectRequestV11) -> SceneCreateObjectResponseV11:
    object_id = (
        f"obj::{request.object_type.lower()}::{request.name.lower()}"
        f"::{','.join(f'{axis:.3f}' for axis in request.location)}"
    )
    return SceneCreateObjectResponseV11(
        tool_name=request.tool_name,
        trace_id=request.trace_id,
        object_id=object_id,
        created=True,
        api_revision="1.1",
    )


def build_default_registry() -> ContractRegistry:
    registry = ContractRegistry()
    registry.register(
        tool_name=TOOL_SCENE_CREATE_OBJECT,
        version=ToolVersion.V1,
        request_schema=SceneCreateObjectRequestV1,
        response_schema=SceneCreateObjectResponseV1,
        handler=lambda req: _handle_scene_create_object_v1(req),
    )
    registry.register(
        tool_name=TOOL_SCENE_CREATE_OBJECT,
        version=ToolVersion.V1_1,
        request_schema=SceneCreateObjectRequestV11,
        response_schema=SceneCreateObjectResponseV11,
        handler=lambda req: _handle_scene_create_object_v11(req),
    )
    return registry
