---
name: manual-contract-compiler
description: Compile one approved feature package slice into one review-ready manual execution contract bundle. Use when the next output must be bounded compile artifacts for one selected slice. Do not use for package authoring, package readiness review, raw run normalization, or final reconcile classification.
---

# Manual Contract Compiler

## Purpose

Produce exactly one **review-ready manual execution contract bundle**
for exactly one **launchable slice**.

This is a **source-preserving skill**.
It MUST NOT silently rewrite package source files.
It does not close launch approval.
It closes only the compile stage and emits the compile-stage handoff.

## Read First

1. [references/EXECUTION_CONTRACT_SUMMARY.md](references/EXECUTION_CONTRACT_SUMMARY.md)
2. [assets/execution.plan.yaml](assets/execution.plan.yaml)
3. [assets/compile-checklist.md](assets/compile-checklist.md)

## Use This Skill When

- one package already exists
- one launchable slice already exists in `slices.yaml`
- package readiness is already closed enough to compile a bounded run unit
- the next output must be a review-ready manual execution contract bundle

## Do Not Use This Skill When

- the main job is to author or repair package source
- the main job is to decide `ready | patch-required | hold`
- the main job is to normalize raw run evidence
- the main job is to classify `accepted | patch-required | relaunch | hold`
- no launchable slice exists yet

## Hard Input Contract

Required inputs:

- `package_path`
- `slice_id`

Optional inputs:

- `input_ref`
- `output_dir`
- `output_handoff_path`
- `focus`: `full | contract-only | handoff-only`
- `profile_manifest_path` — path to a profile manifest YAML
- OR `profile_key` + `profile_root` — resolved to `<profile_root>/profiles/<profile_key>/shape.yaml`

The skill MUST read directly from package source and the selected slice.

The following compile facts MUST be derivable from package files, slice files,
or profile-provided summaries:

- `feature_id`
- package `state`
- selected `slice_id`
- `path_scope`
- `req_ids`
- `task_ids`
- `eval_ids`
- `done_conditions`
- `verification_checks`
- `budget`
- `approval_mode`

If any required compile fact is missing or ambiguous,
STOP and return a concise `INPUT_GAP_REPORT`
instead of writing partial compile artifacts.

## Profile Resolution

If `profile_manifest_path` or (`profile_key` + `profile_root`) is provided:

1. Load the profile manifest.
2. Apply profile-required additional compile fields on top of the generic contract.
3. Apply profile-defined output path conventions (if any).
4. The profile cannot remove generic required compile facts — only extend them.

If no profile is provided, produce generic compile output only.

## Minimal Package Reading Guide

Read at minimum:

- `package.yaml`
- `requirements.yaml`
- `tasks.md`
- `evals.yaml`
- `design.md`
- `slices.yaml`

The selected slice is the compile boundary.
Do not widen scope beyond that slice.

## Output Contract

Write exactly one bounded manual execution contract bundle.

Required compile outputs:

- `execution-brief.md`
- `goal.json`
- `workflow-pack.overlay.yaml`
- `launch.request.yaml`

Standard workflow output:

- one `execution.plan.yaml`
- one `handoff.packet.yaml` for the **execution-planning** stage

Default output root:

- `${output_dir:-./execution-contract}`

Default handoff path:

- `${output_handoff_path:-./handoff.packet.yaml}`

This compile-stage handoff does not replace reconcile-stage review.
It only closes the compile stage.

## Compile Rules

- Compile exactly one slice.
- Preserve stable ids from package source.
- Do not widen `path_scope`.
- `goal.json` MUST stay within slice boundary.
- `workflow-pack.overlay.yaml` MUST reflect package-local verification intent and stop conditions.
- `launch.request.yaml` MUST preserve the slice approval posture and bounded budget.
- `execution.plan.yaml` MUST include `package_ref`, `slice_ref`, `req_ids`, `task_ids`, `eval_ids`, `approval_mode`, `budget`, and `stop_conditions`.
- If `state != ready`, STOP.
- If linked requirement, task, or eval ids are missing, STOP.
- Do not invent platform-runtime-specific fields without direct evidence from source.
- Every compile artifact MUST cite the selected package and slice as its source.

## Read Paths

- `${package_path}/package.yaml`
- `${package_path}/requirements.yaml`
- `${package_path}/tasks.md`
- `${package_path}/evals.yaml`
- `${package_path}/design.md`
- `${package_path}/slices.yaml`
- profile manifest when provided

## Write Paths

- `${output_dir:-./execution-contract}/execution-brief.md`
- `${output_dir:-./execution-contract}/goal.json`
- `${output_dir:-./execution-contract}/workflow-pack.overlay.yaml`
- `${output_dir:-./execution-contract}/launch.request.yaml`
- `./execution.plan.yaml`
- `${output_handoff_path:-./handoff.packet.yaml}`

## Workflow

1. Validate that `package_path` exists.
2. Read `package.yaml` and confirm package state is compile-eligible.
3. Read `slices.yaml` and resolve the selected launchable slice.
4. Resolve profile if provided.
5. Pull linked requirement, task, and eval facts from package source.
6. Compile the bounded execution contract bundle.
7. Write `execution.plan.yaml`.
8. Write compile-stage `handoff.packet.yaml`.
9. Stop if any output cannot be grounded in package truth.

## Stop Conditions

Stop and return a blocker report if:

- package path is invalid
- package state is not compile-eligible
- selected slice does not exist
- selected slice is not launchable
- linked req/task/eval ids are missing
- approval posture is ambiguous
- output would require invented runtime semantics

## Final Rule

This skill compiles one bounded execution contract from source truth.
It does not execute the run.
It does not normalize evidence.
It does not reconcile the result back into source truth.
