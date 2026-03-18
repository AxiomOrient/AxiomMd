---
name: feature-package-author
description: Create or update one bounded feature package from a normalized input packet and available source evidence. Use when the target output must be a structured multi-file feature package ready for readiness review. Optionally accepts a profile manifest to apply product-specific shape on top of the generic contract.
---

# Feature Package Author

## Purpose

Produce or repair exactly one **feature package**.

This is a **source-changing skill**.

The generic contract defines the minimum package shape.
If a profile manifest is provided, product-specific fields are applied on top.
The skill does not decide whether the package is launchable — that is owned by the readiness review step.

## Read First

1. [references/OWNERSHIP_AND_OUTPUT_CONTRACT.md](references/OWNERSHIP_AND_OUTPUT_CONTRACT.md)
2. [assets/input.packet.yaml](assets/input.packet.yaml)
3. [assets/package-skeleton.md](assets/package-skeleton.md)
4. [assets/author-checklist.md](assets/author-checklist.md)

## Use This Skill When

- a bounded feature needs a structured package
- the next step is a readiness review or execution planning
- input arrives as an `input.packet.yaml` (create mode) or an existing package (update mode)

## Do Not Use This Skill When

- the task is a review-only pass
- the task is implementation code or runtime patching
- the input is too broad and product framing has not been done yet
- required authoring facts are still unresolved

## Input Contract

**Required:**

- `input.packet.yaml`

**Optional:**

- `route.decision.yaml`
- `mode: create | update` (default: `create`)
- `package_path` — required for `update`, derived from constraints for `create`
- `profile_manifest_path` — path to a profile manifest YAML
- OR `profile_key` + `profile_root` — resolved to `<profile_root>/profiles/<profile_key>/shape.yaml`
- `authoring_request_path` — path to a profile-local overlay YAML (e.g. `authoring.request.yaml`); activated by the profile if `authoring_request.supported: true` in `shape.yaml`

The following authoring facts MUST be derivable from the packet, current package (update mode), or cited evidence:

- feature identifier and slug
- in-scope / out-of-scope
- success criteria
- constraints
- source truth references

If required facts are missing, STOP and return `INPUT_GAP_REPORT`.

## Profile Resolution

If `profile_manifest_path` or (`profile_key` + `profile_root`) is provided:

1. Load the profile manifest.
2. Apply profile-required additional fields on top of the generic contract.
3. Apply profile-defined path conventions (if any).
4. Run the profile validator if one is specified.
5. The profile cannot remove generic required fields — only extend them.

If no profile is provided, produce generic output only.

## Generic Package Contract

Write or update exactly these files under the target package directory:

**Required files:**

- `intent.md` — feature purpose, scope summary, non-goals
- `package.yaml` — package metadata (see Generic Package Fields below)
- `requirements.yaml` — requirements with `REQ-*` IDs
- `invariants.yaml` — hard constraints that must not be violated
- `design.md` — boundary, data model, interfaces, failure modes, requirement mapping
- `tasks.md` — tasks with `TASK-*` IDs linked to requirements and evals
- `evals.yaml` — evaluations with `EVAL-*` IDs linked to requirements and tasks
- `risks.yaml` — risk list
- `decisions.jsonl` — decision log (one JSON object per line)
- `slices.yaml` — at least one launchable slice

**Standard workflow output:**

- `handoff.packet.yaml` with `stage: feature-package-authoring`

## Generic Package Fields

`package.yaml` minimum (without profile):

```yaml
id: <unique identifier>
slug: <machine-readable slug>
title: <human-readable title>
state: draft | ready | active | done
layer: feature
```

When a profile is applied, the profile manifest defines additional required fields.
Generic fields must always be present regardless of profile.

## Authoring Rules

- Keep the package to one bounded feature.
- Preserve stable IDs when updating an existing package.
- `design.md` MUST include: boundary, interfaces, failure modes, requirement mapping.
- Every `must` requirement MUST have at least one blocking eval.
- Every requirement MUST map to at least one task.
- Every task MUST have `req_ids`, `eval_ids`, and a `touched_paths` estimate.
- Every eval MUST have `req_ids`, `task_ids`, `procedure`, and `pass_condition`.
- `slices.yaml` MUST define at least one launchable slice with bounded `path_scope`, linked `req_ids`, `task_ids`, `eval_ids`, and explicit `done_conditions`.
- When current source reality is unknown, state it explicitly in `intent.md` or `design.md`.

## Read Paths

- `input.packet.yaml`
- `route.decision.yaml` when provided
- framing docs (`product-charter.md`, `system-blueprint.md`) when route required framing first
- existing package files when `mode=update`
- source truth files cited in `source_context_refs` and `evidence_refs`
- profile manifest when provided

## Write Paths

- target package directory (all required package files)
- `handoff.packet.yaml`

## Workflow

1. If `input.packet.yaml` exists, run:
   `python $AXIOM_MD/scripts/workflow_check.py packet <path/to/input.packet.yaml>`
2. If `mode=update`, read existing package files.
3. Resolve profile if provided.
4. Extract required authoring facts.
5. Draft or patch package files using [assets/package-skeleton.md](assets/package-skeleton.md).
6. Layer 존재 여부 비파괴 검사:
   `python $AXIOM_MD/scripts/workflow_check.py ensure-layer <package-dir>`
7. Package 검증 실행:
   `python $AXIOM_MD/scripts/workflow_check.py package <package-dir>`
   (필요 시에만 `ensure-layer --write --layer feature`를 실행해 보정)
8. Write `handoff.packet.yaml` and run:
   `python $AXIOM_MD/scripts/workflow_check.py handoff <path/to/handoff.packet.yaml>`
9. Re-check [assets/author-checklist.md](assets/author-checklist.md).
10. Patch until generic validation passes, or stop with a precise blocker list.

## Stop Conditions

- required authoring facts are missing
- feature scope is not bounded
- in-scope / out-of-scope cannot be determined
- linkage between requirements, tasks, and evals cannot be closed
- `slices.yaml` cannot produce a launchable slice

## Final Rule

This skill produces or repairs package source and closes the authoring stage with a handoff packet.
It does not decide whether the package is ready for execution.
Readiness is owned by the readiness review step.
