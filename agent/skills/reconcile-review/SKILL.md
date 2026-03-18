---
name: reconcile-review
description: Review one normalized evidence bundle against one selected feature package slice and produce one bounded reconcile decision. Use after evidence normalization to decide accepted vs patch-required vs relaunch vs hold. Do not use for package authoring, compile-only work, or raw evidence normalization.
---

# Reconcile Review

## Purpose

Produce exactly one deterministic **reconcile decision**
for exactly one **package slice**.

This is a **review-only skill**.
It MUST NOT silently edit package source files unless the user explicitly requests a separate repair pass.
It closes only the reconcile decision for one bounded slice.

## Read First

1. [references/EXECUTION_CONTRACT_SUMMARY.md](references/EXECUTION_CONTRACT_SUMMARY.md)
2. [assets/reconcile.result.yaml](assets/reconcile.result.yaml)
3. [assets/reconcile-checklist.md](assets/reconcile-checklist.md)

## Use This Skill When

- one normalized evidence bundle already exists
- the target package and selected slice are already known
- the next question is `accepted | patch-required | relaunch | hold`

## Do Not Use This Skill When

- package authoring is still incomplete
- no normalized evidence bundle exists
- the main job is to execute code
- the main job is to compile an execution contract
- the main job is to normalize raw run output

## Hard Input Contract

Required inputs:

- `package_path`
- `slice_id`
- `evidence_path`

Optional inputs:

- `execution_plan_path`
- `input_ref`
- `output_path`
- `output_handoff_path`
- `focus`: `full | classification-only | next-action-only`

The following reconcile facts MUST be derivable from package truth,
selected slice, normalized evidence, or bundled summaries:

- `feature_id`
- `package_ref`
- `slice_id`
- `done_conditions`
- `verification_checks`
- normalized verification outcome
- bounded changed paths
- unresolved gaps if any

If required reconcile facts are missing or ambiguous,
STOP and return a concise `INPUT_GAP_REPORT`
instead of writing partial reconcile output.

## Minimal Reading Guide

Read at minimum:

- `package.yaml`
- `requirements.yaml`
- `tasks.md`
- `evals.yaml`
- `slices.yaml`
- `evidence.result.json`
- `execution.plan.yaml` when present

The unit of review is one selected slice.
Do not widen scope beyond that slice.

## Output Contract

Write:

- one `reconcile.result.yaml`
- one `handoff.packet.yaml` for the **reconcile-and-close** stage
- optional `reconcile-note.md`

Default paths:

- `${output_path:-./reconcile.result.yaml}`
- `${output_handoff_path:-./handoff.packet.yaml}`

## Review Rules

- Review exactly one slice.
- Compare normalized evidence against slice scope, done conditions, and verification checks.
- Classification MUST be one of:
  - `accepted`
  - `patch-required`
  - `relaunch`
  - `hold`
- `accepted` requires grounded satisfaction of done conditions and verification checks.
- `patch-required` means source truth must change before the next run.
- `relaunch` means source truth may remain stable but execution should be retried under bounded conditions.
- `hold` means a safe bounded next-step decision cannot be made.
- Preserve evidence uncertainty explicitly.
- Do not hide failed checks.
- Do not mutate package metadata here.
- `next_action` MUST be concrete and bounded.
- If the right next step depends on an unresolved owner decision, classify `hold`.

## Read Paths

- `${package_path}/package.yaml`
- `${package_path}/requirements.yaml`
- `${package_path}/tasks.md`
- `${package_path}/evals.yaml`
- `${package_path}/slices.yaml`
- `${evidence_path}`
- `${execution_plan_path}` when provided

## Write Paths

- `${output_path:-./reconcile.result.yaml}`
- `${output_handoff_path:-./handoff.packet.yaml}`
- optional `reconcile-note.md`

## Workflow

1. Read package truth and selected slice.
2. Read normalized evidence bundle.
3. Compare evidence against slice scope, done conditions, and verification checks.
4. Classify the run outcome.
5. Write `reconcile.result.yaml`.
6. Write reconcile-stage `handoff.packet.yaml`.
7. Stop if classification cannot be grounded without invented decisions.

## Stop Conditions

Stop and return a blocker report if:

- package path is invalid
- selected slice is missing
- evidence bundle is missing or malformed
- evidence cannot be mapped to the selected slice
- next action would require invented decisions

## Final Rule

This skill closes one bounded reconcile decision.
It does not auto-patch source truth.
It does not launch the next run.
