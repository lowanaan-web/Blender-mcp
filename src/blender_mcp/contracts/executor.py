"""Validated contract executor with request/response schema enforcement."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from .canonical import ToolVersion
from .errors import ContractExecutionError, ErrorEnvelope, to_error_envelope
from .registry import ContractRegistry


class ContractExecutor:
    """Executes tools through contract registry with strict validation gates."""

    def __init__(self, registry: ContractRegistry) -> None:
        self._registry = registry

    def execute(
        self,
        *,
        tool_name: str,
        version: ToolVersion,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        trace_id = payload.get("trace_id", "unknown_trace")
        contract = self._registry.resolve(tool_name, version)
        if contract is None:
            error = ErrorEnvelope(
                code="unsupported_contract",
                message=f"No contract registered for {tool_name} @ {version.value}",
                recoverable=False,
                next_actions=["Upgrade client", "Review compatibility policy"],
                trace_id=trace_id,
            )
            return {"ok": False, "error": error.model_dump()}

        try:
            request_model = contract.request_schema.model_validate(payload)
        except ValidationError as exc:
            error = ErrorEnvelope(
                code="invalid_request",
                message="Request payload failed schema validation.",
                recoverable=True,
                next_actions=["Fix request fields", "Re-submit request"],
                trace_id=trace_id,
                details={"validation_errors": exc.errors()},
            )
            return {"ok": False, "error": error.model_dump()}

        try:
            handler_output = contract.handler(request_model)
            response_model = contract.response_schema.model_validate(
                handler_output.model_dump() if hasattr(handler_output, "model_dump") else handler_output
            )
        except ValidationError as exc:
            error = ErrorEnvelope(
                code="invalid_response",
                message="Handler output failed response schema validation.",
                recoverable=False,
                next_actions=["Fix server handler", "Run contract tests"],
                trace_id=request_model.trace_id,
                details={"validation_errors": exc.errors()},
            )
            return {"ok": False, "error": error.model_dump()}
        except ContractExecutionError as exc:
            return {"ok": False, "error": exc.envelope.model_dump()}
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": to_error_envelope(exc, request_model.trace_id).model_dump()}

        return {"ok": True, "data": response_model.model_dump()}
