---
name: manual-contract-compiler
description: Compile one approved AxiomSpecs package slice into one review-ready manual execution contract bundle. Use when the next output must be bounded compile artifacts for one selected slice. Do not use for package authoring, package readiness review, raw run normalization, or final reconcile classification.
---

# Manual Contract Compiler

## Purpose

Produce exactly one **review-ready manual execution contract bundle**
for exactly one **AxiomSpecs launchable slice**.

AxiomMd owns the generic execution-planning artifact contract.
AxiomSpecs owns package truth, slice truth, and Axiom-local run outcome meaning.
This bundle carries only the installed skill behavior and minimum owner summaries it needs.

This is a **source-preserving skill**.
It MUST NOT silently rewrite package source files.
It does not close launch approval.
It closes only the compile stage and emits the compile-stage handoff.

## Read First

1. [references/OWNER_CONTRACTS_SUMMARY.md](references/OWNER_CONTRACTS_SUMMARY.md)
2. [references/EXECUTION_CONTRACT_SUMMARY.md](references/EXECUTION_CONTRACT_SUMMARY.md)
3. [assets/execution.plan.yaml](assets/execution.plan.yaml)
4. [assets/compile-checklist.md](assets/compile-checklist.md)

## Use This Skill When

- one package already exists under `AxiomSpecs/specs/features/**`
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

The skill MUST read directly from package source and the selected slice.

The following compile facts MUST be derivable from package files, slice files,
or bundled owner summaries:

- `feature_id`
- `profile_key`
- package `state`
- package `proof_state`
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

## Minimal Package Reading Guide

Read at minimum:

- `package.yaml`
- `requirements.yaml`
- `tasks.md`
- `evals.yaml`
- `design.md`
- `contracts/**`
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

- `${output_dir:-/execution-contract}`

Default handoff path:

- `${output_handoff_path:-/handoff.packet.yaml}`

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
- Do not invent AxiomRunner-, AxiomNexus-, or codex-runtime-specific fields without direct owner evidence.
- Every compile artifact MUST cite the selected package and slice as its source.

## Read Paths

- `${package_path}/package.yaml`
- `${package_path}/requirements.yaml`
- `${package_path}/tasks.md`
- `${package_path}/evals.yaml`
- `${package_path}/design.md`
- `${package_path}/contracts/**`
- `${package_path}/slices.yaml`
- bundled owner-summary docs in `references/**`

## Write Paths

- `${output_dir:-/execution-contract}/execution-brief.md`
- `${output_dir:-/execution-contract}/goal.json`
- `${output_dir:-/execution-contract}/workflow-pack.overlay.yaml`
- `${output_dir:-/execution-contract}/launch.request.yaml`
- `/execution.plan.yaml`
- `${output_handoff_path:-/handoff.packet.yaml}`

## Output Target

- one bounded manual execution contract bundle
- one compile-stage `execution.plan.yaml`
- one compile-stage `handoff.packet.yaml`

## Workflow

1. Validate that `package_path` exists.
2. Read `package.yaml` and confirm package state is compile-eligible.
3. Read `slices.yaml` and resolve the selected launchable slice.
4. Pull linked requirement, task, and eval facts from package source.
5. Compile the bounded execution contract bundle.
6. Write `execution.plan.yaml`.
7. Write compile-stage `handoff.packet.yaml`.
8. Stop if any output cannot be grounded in package truth.

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
