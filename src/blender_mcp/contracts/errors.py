"""Error contracts and exception handling for tool execution."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from .canonical import CanonicalModel, TraceId


class ErrorEnvelope(CanonicalModel):
    """Standardized error payload returned for every contract failure."""

    code: str = Field(min_length=3, max_length=64)
    message: str = Field(min_length=1, max_length=2048)
    recoverable: bool
    next_actions: list[str] = Field(default_factory=list, max_length=8)
    trace_id: TraceId
    details: dict[str, Any] | None = None


class ContractExecutionError(RuntimeError):
    """Structured runtime error that serializes to ErrorEnvelope."""

    def __init__(
        self,
        *,
        code: str,
        message: str,
        trace_id: str,
        recoverable: bool,
        next_actions: list[str] | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.envelope = ErrorEnvelope(
            code=code,
            message=message,
            recoverable=recoverable,
            next_actions=next_actions or [],
            trace_id=trace_id,
            details=details,
        )


def to_error_envelope(exc: Exception, trace_id: str) -> ErrorEnvelope:
    """Convert arbitrary exceptions into a standard envelope."""

    if isinstance(exc, ContractExecutionError):
        return exc.envelope

    return ErrorEnvelope(
        code="internal_error",
        message="Unhandled tool execution failure.",
        recoverable=False,
        next_actions=["Retry later", "Escalate to system operator"],
        trace_id=trace_id,
        details={"exception_type": type(exc).__name__},
    )
