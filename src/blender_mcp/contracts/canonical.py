"""Canonical contract model system shared by all versioned tool schemas."""

from __future__ import annotations

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

TraceId = Annotated[
    str,
    StringConstraints(min_length=8, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$"),
]


class ToolVersion(str, Enum):
    """Supported contract versions for tool interfaces."""

    V1 = "v1"
    V1_1 = "v1_1"


class CanonicalModel(BaseModel):
    """Single canonical model baseline for every request/response schema."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, frozen=False)


class ToolRequestBase(CanonicalModel):
    """Base request envelope shared by all tool request schemas."""

    tool_name: str = Field(min_length=3, max_length=128)
    trace_id: TraceId


class ToolResponseBase(CanonicalModel):
    """Base response envelope shared by all tool response schemas."""

    tool_name: str = Field(min_length=3, max_length=128)
    trace_id: TraceId
