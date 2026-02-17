# Gemini-Orchestrated Blender Execution Contract

## Status
Canonical (normative) interface for all Gemini-driven tool execution.

## Objective
Define a production-grade orchestration contract that converts Gemini planning output into safe, deterministic, and traceable Blender mutations through MCP tools.

## End-to-End Flow

```text
GeminiPlanner -> OperationGraph -> BlenderExecutor
```

### Phase 1: Planning (`GeminiPlanner -> OperationGraph`)
1. `GeminiPlanner` produces a strict JSON operation set (no free-form directives).
2. The output is validated against the planner schema in this document.
3. `OperationGraph` is built as a Directed Acyclic Graph (DAG):
   - Nodes: individual operations.
   - Edges: `depends_on` references.
4. Invalid plans (schema mismatch, missing dependencies, cycles, disallowed tools) are rejected before execution.

### Phase 2: Execution (`OperationGraph -> BlenderExecutor`)
1. `BlenderExecutor` receives only schema-validated DAG input.
2. It computes a deterministic execution schedule from the DAG.
3. It executes operations via MCP tool calls and Blender mutation APIs.
4. It records mutation journals and correlation IDs for full traceability.
5. It emits either:
   - success with execution receipts, or
   - failure contract payload (defined below).

## Planner Output Schema (Strict JSON)

Planner output MUST conform exactly to the following JSON schema. Additional properties are forbidden at every level.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://blender-mcp.dev/schemas/gemini-planner-operations.json",
  "title": "Gemini Planner Operation Set",
  "type": "object",
  "additionalProperties": false,
  "required": ["request_id", "operations"],
  "properties": {
    "request_id": {
      "type": "string",
      "minLength": 1,
      "description": "Unique Gemini request correlation id."
    },
    "operations": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "operation_id",
          "tool_name",
          "args",
          "depends_on",
          "safety_level"
        ],
        "properties": {
          "operation_id": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9_.:-]{1,128}$",
            "description": "Stable unique identifier for this operation within request scope."
          },
          "tool_name": {
            "type": "string",
            "minLength": 1,
            "description": "Registered MCP tool identifier."
          },
          "args": {
            "type": "object",
            "additionalProperties": true,
            "description": "Tool-specific argument payload validated against tool contract at runtime."
          },
          "depends_on": {
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^[a-zA-Z0-9_.:-]{1,128}$"
            },
            "uniqueItems": true,
            "description": "List of prerequisite operation_ids that must complete successfully."
          },
          "safety_level": {
            "type": "string",
            "enum": ["read_only", "safe_write", "destructive"],
            "description": "Safety class used by policy gates and approvals."
          }
        }
      }
    }
  }
}
```

## Executor Guarantees

`BlenderExecutor` MUST enforce the following guarantees.

### 1) Deterministic Order
- Given the same validated `OperationGraph`, tool registry version, and scene baseline hash, scheduling order is deterministic.
- Topological sort tie-breaker is lexical `operation_id` ascending.
- Non-deterministic tool calls are forbidden unless wrapped by deterministic adapters that pin seed/time/environment.

### 2) Idempotency Handling
- Each operation key is `request_id + operation_id + normalized(args)`.
- Before execution, executor checks operation journal for an existing committed receipt:
  - if present and compatible with current scene hash: return cached receipt, skip mutation;
  - if present but incompatible: return conflict error (`IDEMPOTENCY_CONFLICT`) with recovery hints.
- Retried requests MUST not duplicate side effects for already-committed operations.

### 3) Rollback Semantics
- Execution uses staged checkpoints per rollback boundary (default boundary: per operation).
- On failure:
  - If operation is `read_only`: no rollback required.
  - If operation is mutating and marked rollback-capable: reverse via compensating action or checkpoint restore.
  - If rollback fails: escalate to `ROLLBACK_FAILED` and return latest consistent checkpoint metadata.
- Executor MUST never report full success if any mutating operation failed without reaching a declared consistency point.

## Failure Contract (Executor -> Gemini)

All execution failures MUST return the following JSON payload shape:

```json
{
  "error_code": "<STRING_ENUM>",
  "recoverable": true,
  "retry_hint": "<SHORT_ACTIONABLE_TEXT>",
  "minimal_repair_plan": [
    {
      "operation_id": "<OP_ID>",
      "action": "retry|replace_args|drop|insert_precondition"
    }
  ]
}
```

### Field Requirements
- `error_code` (required): machine-readable enum (examples: `SCHEMA_INVALID`, `GRAPH_CYCLE`, `TOOL_TIMEOUT`, `IDEMPOTENCY_CONFLICT`, `ROLLBACK_FAILED`, `POLICY_BLOCKED`).
- `recoverable` (required): `true` when Gemini can safely issue a follow-up plan; otherwise `false`.
- `retry_hint` (required): concise directive suitable for prompt-conditioning a repair attempt.
- `minimal_repair_plan` (required): smallest operation-level diff needed to re-enter executable state.

## Correlation and Traceability Contract

Every request MUST carry and propagate correlation IDs across all layers:

- `gemini_request_id`: global request identifier generated at Gemini ingress.
- `mcp_call_id`: unique per MCP tool invocation.
- `blender_mutation_id`: unique per committed Blender state mutation.

### Propagation Rules
1. `gemini_request_id` is required in planner output as `request_id`.
2. Executor emits `mcp_call_id` for each tool invocation and links it to one `operation_id`.
3. Every mutating Blender event logs `blender_mutation_id` and references both `mcp_call_id` and `operation_id`.
4. Logs, metrics, and audit events MUST include all applicable IDs to permit end-to-end causal reconstruction.

### Minimum Audit Record
Each executed operation should emit an audit record containing:
- `timestamp`
- `request_id` (`gemini_request_id`)
- `operation_id`
- `mcp_call_id`
- `blender_mutation_id` (nullable for read-only operations)
- `tool_name`
- `safety_level`
- `status` (`succeeded|failed|rolled_back|skipped_idempotent`)
- `scene_hash_before`
- `scene_hash_after` (nullable on pre-mutation failures)

## Normative Adoption

This document is the canonical interface for Gemini-driven execution. New tools, planners, or executor implementations MUST comply with this contract. Any compatibility-breaking change requires versioned schema publication and an explicit migration path.
