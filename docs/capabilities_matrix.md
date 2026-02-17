# Blender MCP Capabilities Matrix

## Status
Canonical pre-mutation capability contract for scene mutation, node workflows, simulation, game export preparation, and diagnostics.

## Purpose
Define production-safe capability requirements that must be satisfied before any mutating action is executed by Blender MCP tooling.

## Matrix Columns
- **Required permissions**: Minimum policy scope required for invoking the capability.
- **Expected inputs/outputs**: Contract-level payload shape and return artifacts.
- **Deterministic constraints**: Conditions that guarantee reproducible outcomes.
- **Validation rules before mutation**: Mandatory checks that must pass before state changes are allowed.

---

## 1) Scene Authoring

| Capability | Required permissions | Expected inputs | Expected outputs | Deterministic constraints | Validation rules before mutation |
|---|---|---|---|---|---|
| Object lifecycle (create/rename/delete) | `scene.read`, `object.write` (and `object.delete` for destructive ops) | Object type, target collection, transform seed, naming policy context | Object UUIDs, canonical names, creation/deletion receipt, scene hash delta | Stable UUID generation strategy; deterministic default transform and naming tie-breakers | Name collision check, collection existence check, destructive-op safety gate, locked/linked data-block check |
| Collection management (create/link/move/nest) | `scene.read`, `collection.write` | Collection path, parent pointer, membership ops | Collection IDs, hierarchy diff, membership receipt | Parent-child order sorted lexicographically before commit; fixed traversal order | Acyclic hierarchy validation, parent existence, member object existence, linked-library write protection |
| Transform operations (translate/rotate/scale/apply) | `scene.read`, `transform.write` | Object IDs, pivot mode, transform vectors/quaternions, coordinate space | Updated transform matrix, applied-transform receipt, bounds delta | Canonical unit system; deterministic floating-point quantization at configured precision | Object existence, transform domain constraints (no NaN/Inf), frozen/locked channel check, unapplied parent dependency warning gate |
| Modifier stack orchestration (add/reorder/configure/apply) | `scene.read`, `modifier.write` (plus `mesh.write` for apply) | Object IDs, modifier type, parameter block, stack index intent | Modifier stack snapshot, evaluated mesh hash (if applied), mutation receipt | Stack order resolved by explicit index and lexical fallback; parameter serialization normalized | Modifier compatibility check per object type, parameter schema validation, topology safety guard, irreversible-apply confirmation gate |

---

## 2) Node Systems

| Capability | Required permissions | Expected inputs | Expected outputs | Deterministic constraints | Validation rules before mutation |
|---|---|---|---|---|---|
| Geometry Nodes graph editing | `scene.read`, `nodes.geometry.write` | Node group target, node ops (add/remove/connect), typed socket values | Graph diff, node IDs, interface signature, evaluation hash | Deterministic node ID allocation and link ordering; seeded random nodes must pin seed | Node group existence, socket type compatibility, cycle policy validation, referenced attribute existence check |
| Shader Nodes material authoring | `scene.read`, `material.write`, `nodes.shader.write` | Material IDs, node edit operations, texture bindings, color-space intents | Material graph diff, compiled shader status, dependency list | Color-space conversion policy pinned; link order canonicalized | Material existence, texture file availability, socket type validation, render-engine compatibility checks |
| Compositor Nodes pipeline assembly | `scene.read`, `compositor.write`, `nodes.compositor.write` | Scene/view layer refs, node graph edits, output passes, file output paths | Compositor graph diff, pass map, output target receipts | Pass ordering fixed by canonical pass sequence; output path normalization required | View layer existence, pass availability per render settings, writable output path check, format/bit-depth compatibility validation |

---

## 3) Physics Stack

| Capability | Required permissions | Expected inputs | Expected outputs | Deterministic constraints | Validation rules before mutation |
|---|---|---|---|---|---|
| Rigid body setup | `scene.read`, `physics.rigidbody.write` | Object IDs, active/passive mode, mass, shape, damping, world settings | Rigid body component assignments, world config diff, setup receipt | Fixed simulation timestep config; deterministic broadphase seed where supported | Mesh/object type compatibility, non-zero mass constraints, rigid body world presence, transform freeze checks |
| Physics constraints (hinge/fixed/slider/etc.) | `scene.read`, `physics.constraint.write` | Constraint type, object A/B refs, limits, motor params | Constraint IDs, constrained pair map, solver config diff | Constraint application order sorted by pair and type; normalized limit units | Both bodies exist and physics-enabled, constraint frame validity, limit range sanity, circular hard-lock detection |
| Cloth simulation configuration | `scene.read`, `physics.cloth.write` | Mesh object ref, cloth presets/params, pin groups, quality steps | Cloth modifier config diff, cache policy state, setup receipt | Deterministic preset expansion and parameter normalization | Mesh topology suitability, vertex group existence, self-collision parameter bounds, conflicting modifier stack check |
| Collision filters and interaction masks | `scene.read`, `physics.collision.write` | Layer/mask definitions, object group assignments, interaction rules | Filter table diff, object assignment receipts | Bitmask normalization and stable layer ordering | Mask width validity, overlapping policy conflicts, orphan layer reference check |
| Bake controls (start/stop/invalidate/rebake) | `scene.read`, `physics.bake.write`, `cache.write` | Simulation domain, frame range, cache path, bake mode | Bake job receipt, cache artifact manifest, bake checksum | Frame stepping fixed; cache naming derived from scene hash and frame range | Valid frame range, writable cache path, stale cache invalidation policy check, concurrent bake lock enforcement |

---

## 4) Game-Ready Prep

| Capability | Required permissions | Expected inputs | Expected outputs | Deterministic constraints | Validation rules before mutation |
|---|---|---|---|---|---|
| LOD generation hooks | `scene.read`, `mesh.write`, `pipeline.lod.write` | Source mesh refs, target triangle budgets, generation strategy, LOD naming prefix | Generated LOD mesh IDs, reduction reports, LOD chain map | Reduction strategy and simplification seed pinned; target budgets quantized | Source mesh validity, manifold suitability for decimation, budget monotonicity check, naming collision validation |
| Naming standards enforcement | `scene.read`, `scene.write` | Naming rule set, scope filter, auto-fix policy | Rule violation report, rename receipts, compliance summary | Rule evaluation order fixed (scope then rule priority then lexical) | Reserved-name conflict check, external reference update readiness, duplicate target-name preflight |
| Export readiness checks | `scene.read`, `export.preflight` | Target engine profile, format (FBX/GLTF/etc.), unit/axis profile | Readiness report, blocking issues, non-blocking warnings | Profile versions pinned; check ordering stable across runs | Unsupported feature detection, unapplied transforms/material issues, missing external dependency checks |
| Metadata/packaging normalization | `scene.read`, `scene.write`, `asset.pack.write` | Asset metadata fields, pack policy, relative path directives | Normalized metadata manifest, packed-asset receipts | Path canonicalization and field ordering normalized | Required metadata completeness, illegal character/path traversal checks, duplicate asset key detection |

---

## 5) Diagnostics

| Capability | Required permissions | Expected inputs | Expected outputs | Deterministic constraints | Validation rules before mutation |
|---|---|---|---|---|---|
| Non-manifold detection | `scene.read`, `mesh.read` | Mesh scope filters, tolerance profile | Per-mesh issue list, edge/face IDs, severity summary | Deterministic traversal of mesh elements and fixed tolerance constants | Mesh data-block readability, mode/state safety check (object/edit mode constraints), tolerance profile validity |
| Unapplied transforms audit | `scene.read`, `transform.read` | Object filters, transform threshold policy | Object list with unapplied channels, magnitude deltas | Matrix decomposition method fixed and precision-clamped | Object existence, parent-space interpretability check, threshold bounds validation |
| Broken links detection (libraries/data refs) | `scene.read`, `dependency.read` | Link scopes (library paths, data-block refs), path resolution policy | Broken link manifest, impacted object/material/node references | Path resolution order stable (relative->absolute->library remap) | Access policy for linked libraries, path normalization checks, stale override detection |
| Missing textures detection | `scene.read`, `material.read`, `filesystem.read` | Material scope, texture path roots, resolver policy | Missing texture manifest, affected materials/shaders list | Resolver priority pinned and case-sensitivity policy explicit | Read access to search roots, URI/path scheme validation, duplicate logical-texture mapping check |
| Automated fix candidate generation (no auto-apply) | `scene.read`, `diagnostics.fixplan.write` | Diagnostic report IDs, fix strategy profile | Deterministic fix-plan proposal, ranked actions, confidence values | Ranking algorithm and feature weights version-pinned | Input diagnostic report integrity check, prohibited-destructive-fix filter, operator approval-required flagging |

---

## Global Pre-Mutation Gate (Applies to All Mutating Capabilities)
1. **Permission gate**: Verify caller has all required scopes for the selected capability.
2. **Schema gate**: Validate input payload against capability schema; reject unknown fields unless explicitly allowed.
3. **Scene integrity gate**: Confirm baseline scene hash, linked-data state, and lock state are unchanged since planning.
4. **Determinism gate**: Enforce pinned seeds, normalized units, canonical sort orders, and fixed precision policy.
5. **Safety gate**: Block destructive actions unless explicit destructive intent and rollback strategy are present.
6. **Audit gate**: Require correlation identifiers and mutation journal configuration before commit.

## Notes
- Read-only diagnostics may emit fix proposals, but mutation execution is disallowed until a separate authorized write request passes all gates.
- Any capability failing pre-mutation validation must return a machine-readable failure contract with actionable remediation guidance.
