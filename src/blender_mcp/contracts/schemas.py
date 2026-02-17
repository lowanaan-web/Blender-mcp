"""Versioned tool schemas built on a single canonical model system."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from .canonical import ToolRequestBase, ToolResponseBase

TOOL_SCENE_CREATE_OBJECT = "scene.create_object"


class SceneCreateObjectRequestV1(ToolRequestBase):
    """v1 request schema for scene.create_object."""

    tool_name: Literal[TOOL_SCENE_CREATE_OBJECT] = TOOL_SCENE_CREATE_OBJECT
    object_type: Literal["MESH", "LIGHT", "CAMERA"]
    name: str = Field(min_length=1, max_length=128)


class SceneCreateObjectResponseV1(ToolResponseBase):
    """v1 response schema for scene.create_object."""

    tool_name: Literal[TOOL_SCENE_CREATE_OBJECT] = TOOL_SCENE_CREATE_OBJECT
    object_id: str = Field(min_length=1, max_length=128)
    created: bool


class SceneCreateObjectRequestV11(SceneCreateObjectRequestV1):
    """v1_1 request schema extends v1 with transform initialization."""

    location: tuple[float, float, float] = (0.0, 0.0, 0.0)


class SceneCreateObjectResponseV11(SceneCreateObjectResponseV1):
    """v1_1 response schema extends v1 with compatibility metadata."""

    api_revision: Literal["1.1"] = "1.1"
