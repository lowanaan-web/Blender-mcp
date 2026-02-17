# Blender MCP Contract Compatibility Policy

## Objective
This policy governs versioned tool contracts under `src/blender_mcp/contracts/` to guarantee safe evolution, deterministic validation, and explicit error semantics.

## Canonical Model System
All request/response contracts MUST inherit from the shared canonical model base (`CanonicalModel`) and envelope primitives (`ToolRequestBase`, `ToolResponseBase`).

## Versioning Rules
1. Every tool contract MUST publish explicit versions (`v1`, `v1_1`, ...).
2. Minor revisions (`v1` -> `v1_1`) MUST remain backward compatible for existing required fields.
3. Breaking changes require a new major version family and parallel registration.
4. Registry entries are keyed by `(tool_name, version)` and must provide both schema and handler.

## Validation Rules
1. Request payloads MUST be validated before handler execution.
2. Handler outputs MUST be validated against response schemas before returning to clients.
3. Validation failures MUST return the standard error envelope.

## Error Envelope
Every contract failure returns:
- `code`: machine-parseable error code
- `message`: human-readable summary
- `recoverable`: whether the client can retry/fix input
- `next_actions`: ordered remediation hints
- `trace_id`: correlation id propagated end-to-end

Optional `details` may include safe diagnostics.

## CI Enforcement
CI MUST fail when:
- The compatibility policy document is missing required sections.
- A registered tool does not provide both `v1` and `v1_1` contracts.
- Contract execution tests detect missing request or response validation.
