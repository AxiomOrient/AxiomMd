---
name: run-evidence-normalizer
description: Normalize one bounded run result into one Axiom-aligned evidence bundle for one selected package slice. Use after execution artifacts exist and before reconcile review. Do not use for package authoring, package readiness review, compile-only work, or final reconcile classification.
---

# Run Evidence Normalizer

## Purpose

Produce exactly one normalized **evidence bundle**
for exactly one executed **AxiomSpecs slice**.

AxiomMd owns the generic evidence artifact class.
AxiomSpecs owns Axiom-local evidence and run-outcome meaning.
This bundle carries only the installed skill behavior and minimum owner summaries it needs.

This is a **review and normalization skill**.
It MUST NOT silently edit package source files.
It closes only the evidence stage and emits the evidence-stage handoff.

## Read First

1. [references/OWNER_CONTRACTS_SUMMARY.md](references/OWNER_CONTRACTS_SUMMARY.md)
2. [references/RUN_OUTCOME_SUMMARY.md](references/RUN_OUTCOME_SUMMARY.md)
3. [assets/evidence.result.json](assets/evidence.result.json)
4. [assets/evidence-checklist.md](assets/evidence-checklist.md)

## Use This Skill When

- one execution attempt already happened
- raw run outputs already exist
- the package and selected slice are already known
- the next output must be one normalized evidence bundle for reconcile review

## Do Not Use This Skill When

- no run happened yet
- the main job is to compile a manual execution contract
- the main job is to classify the final reconcile outcome
- the main job is package authoring or package readiness review

## Hard Input Contract

Required inputs:

- `package_path`
- `slice_id`
- `run_input_root`

Optional inputs:

- `execution_plan_path`
- `output_path`
- `output_handoff_path`

The following evidence facts MUST be derivable from the selected slice,
the run root, the execution plan when present, or bundled owner summaries:

- `feature_id`
- `package_ref`
- `slice_id`
- `req_ids`
- `task_ids`
- `eval_ids`
- `produced_artifacts`
- verification results
- changed paths
- run status
- failure summary when applicable

If required evidence facts are missing or ambiguous,
STOP and return a concise `INPUT_GAP_REPORT`
instead of writing partial evidence output.

## Minimal Reading Guide

Read at minimum:

- `package.yaml`
- `slices.yaml`
- `requirements.yaml`
- `tasks.md`
- `evals.yaml`
- `execution.plan.yaml` when present
- raw run outputs under `run_input_root`

Normalize what happened.
Do not classify what should happen next.

## Output Contract

Write:

- one `evidence.result.json`
- one `handoff.packet.yaml` for the **execution-and-evidence** stage

Default paths:

- `${output_path:-/evidence.result.json}`
- `${output_handoff_path:-/handoff.packet.yaml}`

This evidence-stage handoff does not replace reconcile review.
It only closes normalization of one bounded run result.

## Normalization Rules

- Normalize exactly one run outcome for exactly one slice.
- Preserve source ids from package truth.
- Preserve raw failure state when the run failed.
- Distinguish `missing evidence` from `negative evidence`.
- `verification_results` MUST stay linked to `eval_ids`.
- `changed_paths` MUST stay bounded to observed run output.
- `produced_artifacts` SHOULD be path-like or URI-like references, not prose summaries.
- Do not classify `accepted | patch-required | relaunch | hold` here.
- Do not mutate package metadata here.

## Read Paths

- `${package_path}/package.yaml`
- `${package_path}/slices.yaml`
- `${package_path}/requirements.yaml`
- `${package_path}/tasks.md`
- `${package_path}/evals.yaml`
- `${execution_plan_path}` when provided
- `${run_input_root}/**`
- bundled owner-summary docs in `references/**`

## Write Paths

- `${output_path:-/evidence.result.json}`
- `${output_handoff_path:-/handoff.packet.yaml}`

## Output Target

- one normalized `evidence.result.json`
- one evidence-stage `handoff.packet.yaml`

## Workflow

1. Read package truth and selected slice.
2. Read execution plan when available.
3. Read raw run outputs, logs, diffs, and verification results.
4. Normalize all evidence into one bounded bundle.
5. Write `evidence.result.json`.
6. Write evidence-stage `handoff.packet.yaml`.
7. Stop if source ids cannot be preserved or evidence cannot be bounded to the selected slice.

## Stop Conditions

Stop and return a blocker report if:

- package or slice cannot be resolved
- run root is empty or unreadable
- produced artifacts cannot be linked to the selected slice
- verification results cannot be mapped to eval ids
- evidence would require invented success or failure claims

## Final Rule

This skill records what happened in normalized form.
It does not decide whether source truth should be accepted, patched, relaunched, or held.
