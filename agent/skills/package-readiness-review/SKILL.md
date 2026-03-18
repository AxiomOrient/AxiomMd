---
name: package-readiness-review
description: Review one AxiomSpecs feature package against the AxiomMd readiness gate and emit an AxiomMd handoff packet, with an optional human-readable review note. Use when deciding ready vs patch-required vs hold. Do not use for authoring or product-roadmap work.
---

# Package Readiness Review

## Purpose

Produce a deterministic readiness decision for exactly one **AxiomSpecs feature package**.
AxiomMd owns the review-stage handoff packet; AxiomSpecs owns the package shape and readiness meaning.
This bundle carries the minimum owner summaries it needs and must not fetch GitHub content at runtime.

This is a **review-only skill**.
It MUST NOT silently edit package files unless the user explicitly asks for a separate repair pass.

## Read First

1. [references/READINESS_AND_HANDOFF_CONTRACT.md](references/READINESS_AND_HANDOFF_CONTRACT.md)
2. [assets/handoff.packet.yaml](assets/handoff.packet.yaml)
3. [assets/review-report-template.md](assets/review-report-template.md)
4. [assets/review-checklist.md](assets/review-checklist.md)

## Use This Skill When

- a package already exists
- the question is `ready | patch-required | hold`
- a human or control loop needs a bounded readiness decision

## Do Not Use This Skill When

- the main job is to author package files from scratch
- the main job is to fix implementation code
- the target output is a monolithic spec instead of a feature package

## Input Contract

Required inputs:

- `package_path`
- optional `input_ref`
- optional `output_handoff_path`
- optional `output_review_note_path`
- optional `focus`: `full`, `linkage-only`, `handoff-only`

The skill MUST read the package files directly from the package path.
It MUST NOT assume chat notes are the truth.
If `output_handoff_path` is omitted, write `handoff.packet.yaml` next to the package being reviewed.
Example: `specs/features/FEAT-xxxx-slug/handoff.packet.yaml`

## Output Contract

Write both of the following:

**Primary**: one `handoff.packet.yaml` that matches [assets/handoff.packet.yaml](assets/handoff.packet.yaml).

The handoff packet MUST include:

- workflow stage for the review output, normally `readiness-and-handoff`
- final `status`: `ready | patch-required | hold`
- concrete `evidence_refs`
- concrete `next_step`
- `blockers`
- `produced_paths`

**Standard sidecar**: one `readiness-report.md` that matches [assets/review-report-template.md](assets/review-report-template.md).

- default path: `<package_path>/readiness-report.md`
- custom path: specify `output_review_note_path` to override the default
- this human-readable gate breakdown is the canonical readiness record for the package
- AxiomSpecs FEAT-0001 allows the gate result to remain in `package.yaml` as a supplement; the canonical record is this file

## Status Semantics

- `ready`
  - owner checker passes and the package is usable for the next workflow step
- `patch-required`
  - package exists and is readable, but at least one gate is incomplete and can be repaired in source
- `hold`
  - required file set is missing, parse fails, or the package is not ready for a bounded repair-only pass
- `blocked`
  - reserved for the handoff envelope only when review cannot determine a valid gate status from available evidence

## Review Rules

- Gate 1 checks the required file set, including `contracts/`.
- Gate 2 checks requirement/task/eval linkage completeness and package metadata.
- Gate 3 checks bounded scope, design completeness, and implementation-local leakage.
- Gate 4 checks review mode and risk/approval posture.
- Gate 5 checks handoff completeness and restartability after interruption.
- If required files are missing, verdict MUST be `hold`.
- If linkage/design/handoff is incomplete but patchable, verdict MUST be `patch-required`.
- Only use `ready` when all gates pass.
- If review cannot determine a gate status because evidence is missing, stop with a blocker note instead of inventing a false verdict.
- Do not rename IDs in the review note. Report the exact broken IDs.
- Do not collapse multiple failures into vague prose.
- Use `workflow_check.py package` as the structural baseline, then add the remaining gate analysis from the owned docs.

## Read Paths

- target feature package files
- bundled owner-summary docs and `workflow_check.py` from AxiomMd
- optional `input_ref` when the review is tied to a known upstream packet

## Write Paths

- review output files only: `handoff.packet.yaml` and optional Markdown review note

## Output Target

- one authoritative AxiomMd handoff packet (stage: readiness-and-handoff)
- one canonical readiness-report.md

## Minimal Output Writing Guide

- `input_ref`
  - path to the upstream packet or, if absent, the reviewed package path
- `produced_paths`
  - at minimum the emitted handoff packet path
- `evidence_refs`
  - exact files read during review
- `next_step`
  - cheapest concrete repair or continuation step
- `blockers`
  - empty only when the review result is fully determined

## Workflow

> `$AXIOM_MD` = path to the AxiomMd repository root. Steps using this variable require the AxiomMd toolkit to be available locally.

1. Run:
   `python $AXIOM_MD/scripts/workflow_check.py package <feature-dir> --base-dir <AxiomSpecs>`
2. Inspect the target package files directly.
3. Fill `handoff.packet.yaml` with evidence-backed `status`, `evidence_refs`, `next_step`, and `blockers`.
4. Run:
   `python $AXIOM_MD/scripts/workflow_check.py handoff <path/to/handoff.packet.yaml> --base-dir <AxiomSpecs>`
5. Write `readiness-report.md` from [assets/review-report-template.md](assets/review-report-template.md) with the full gate breakdown.
6. Stop only when both the handoff packet and readiness-report.md are written and the verdict is explicit.

## Stop Conditions

Stop and return a blocker note if:

- `package_path` is missing
- the target directory is not a feature package directory
- required files cannot be read
- repository evidence is insufficient to determine a gate status

## Final Rule

This skill closes only the review decision and the review-stage handoff.
If repair is needed, request a separate pass with `feature-package-author`.
