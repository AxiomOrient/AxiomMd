---
name: feature-package-author
description: Create or update one bounded AxiomSpecs feature package from an AxiomMd-normalized input packet and current repo evidence. Use when the target output must be the AxiomSpecs multi-file package shape. Do not use for implementation code, roadmap notes, or generic methodology docs.
---

# Feature Package Author

## Purpose

Produce or repair exactly one **AxiomSpecs feature package**.
The output MUST match the current AxiomSpecs multi-file package shape.
AxiomMd owns the input envelope; AxiomSpecs owns the output shape and local profile.
This bundle carries the minimum owner summaries it needs and must not fetch GitHub content at runtime.
This skill is intentionally **product-specific**. It is not a generic package author.

This is a **source-changing skill**.

## Read First

1. [references/OWNERSHIP_AND_OUTPUT_CONTRACT.md](references/OWNERSHIP_AND_OUTPUT_CONTRACT.md)
2. [assets/input.packet.yaml](assets/input.packet.yaml)
3. [assets/input-packet-template.md](assets/input-packet-template.md)
4. [assets/package-skeleton.md](assets/package-skeleton.md)
5. [assets/author-checklist.md](assets/author-checklist.md)

## Use This Skill When

- the target repository is `AxiomSpecs`
- the output must be `specs/features/FEAT-xxxx-slug/...`
- the work is a bounded feature package, not a monolithic spec
- input arrives as an AxiomMd `input.packet.yaml` or as an existing package plus enough repo evidence to derive the missing facts

## Do Not Use This Skill When

- the task is generic methodology; that belongs in `AxiomMd`
- the task is a one-off AI-facing single spec; use `spec-writing-standard` instead
- the task is implementation code or runtime patching
- the package needs semantic owner decisions that are still unresolved

## Hard Input Contract

Preferred input envelope:

- one `input.packet.yaml` matching AxiomMd `templates/input.packet.yaml`
- one `route.decision.yaml` when the authoring request came through the standard workflow
- optional `authoring.request.yaml` for product-specific authoring metadata
- `target_kind` SHOULD be `feature-package`
- current truth MUST be cited via `source_context_refs` and/or `evidence_refs`
- output contract refs SHOULD cite the owning AxiomSpecs docs from [references/OWNERSHIP_AND_OUTPUT_CONTRACT.md](references/OWNERSHIP_AND_OUTPUT_CONTRACT.md)
- when route is `framing-first`, `product-charter.md` and `system-blueprint.md` SHOULD already exist

Allowed alternate input for `mode=update`:

- existing feature package files under `specs/features/FEAT-xxxx-slug/`
- optional `output_handoff_path` to override the default handoff output location

The following Axiom-specific authoring facts MUST be derivable from the packet, the current package, or cited repository evidence:

- `feature_id`
- `slug`
- `title`
- `implementation_order`
- `profile_key`
- `review_mode`
- `planes`
- `owner_roles`
- `target_repos`
- `adoption`
- `problem`
- `in_scope`
- `out_of_scope`
- current truth evidence paths

`mode` and `target_feature_path` may be passed explicitly, or derived from the existing package path when `mode=update`.
`output_handoff_path` is optional. When omitted, handoff is written to `<target_feature_path>/handoff.packet.yaml`.
`authoring.request.yaml` is optional but recommended for create-mode when product-local metadata would otherwise overload `constraints`.

If any required authoring fact is missing or ambiguous, STOP and return a concise `INPUT_GAP_REPORT` instead of drafting package files.

## Expected Inputs By Mode

- `mode=create`
  - packet SHOULD already carry `feature_id`, `slug`, `implementation_order`, scope boundary, and output contract refs
  - route decision SHOULD already explain why direct package or framed package authoring is valid
  - target package path is usually declared in `constraints`
- `mode=update`
  - existing package directory becomes part of the input truth
  - packet may focus on requested delta, changed boundary, or missing coverage instead of restating the whole package

## Minimal Packet Reading Guide

- `request_summary`
  - feature title + short summary
- `scope.in` / `scope.out`
  - bounded feature scope and non-goals
- `constraints`
  - stable identifiers and package metadata such as `mode=`, `feature_id=`, `slug=`, `planes=`, `target_repos=`
- `source_context_refs` / `evidence_refs`
  - current truth files to read before drafting
- `route.decision.yaml`
  - why this is package-authoring work now, and whether framing docs are required
- `authoring.request.yaml`
  - product-local metadata such as feature id, slug, planes, owner roles, target repos, and adoption
- `done_signals`
  - what the finished package must satisfy, including `python $AXIOM_MD/scripts/workflow_check.py package <feature-dir> --base-dir <AxiomSpecs>`

## Output Contract

Write or update exactly these paths under the target feature directory unless the user explicitly narrows the scope:

- `intent.md`
- `package.yaml`
- `requirements.yaml`
- `invariants.yaml`
- `design.md`
- `tasks.md`
- `evals.yaml`
- `risks.yaml`
- `decisions.jsonl`
- `contracts/`
- `slices.yaml`

Standard workflow output:

- one `handoff.packet.yaml` for the **feature-package-authoring** stage
- default path: `<target_feature_path>/handoff.packet.yaml`
- custom path: specify `output_handoff_path` to override the default
- this authoring-stage handoff does not replace readiness review
- final readiness verdict is still owned by `package-readiness-review`

## Package Authoring Rules

- Keep the package to one bounded feature.
- Preserve stable IDs when semantic continuity exists.
- Use Korean prose for AxiomSpecs package content unless the surrounding package already uses another language.
- Keep file names, stable ids, and enum-like keys in identifier form.
- `contracts/` directory is required because current AxiomSpecs package shape and `scripts/check_specs` both expect it.
- `package.yaml` SHOULD keep the current house fields: `feature_id`, `slug`, `title`, `state`, `review_mode`, `profile_key`, `planes`, `implementation_order`, `owner_roles`, `target_repos`, `adoption`, `proof_state`, `current_progress`, `next_step`, `blockers`.
- `proof_state` SHOULD be `not_proven` for new packages. Valid values: `not_proven | reference_slice_proven | runtime_proven | reconciled`.
- `slices.yaml` MUST define at least one launchable slice. Each slice MUST have `slice_id`, `path_scope`, `req_ids`, `task_ids`, `eval_ids`, `done_conditions`, `verification_checks`, `budget`, `approval_mode`. Without this file, the compile stage cannot determine a bounded launch unit.
- `profile_key` SHOULD stay `axiom-v1` unless direct repository evidence says otherwise.
- `review_mode` SHOULD stay `human_required` unless direct repository evidence says otherwise.
- `planes` SHOULD use values from `source | compile | execution | control | governance | reconcile`.
- `adoption` SHOULD use the baseline modes from AxiomSpecs `profiles/axiom-v1/package-and-readiness.shape.yaml`.
- If an existing package already uses a repo-local adoption token beyond the profile baseline, preserve it on update and do not normalize it away without explicit owner evidence.
- Every `must` requirement MUST have at least one `kind: blocking` eval.
- Every requirement MUST map to at least one task.
- Every task MUST have `req_ids`, `eval_ids`, `touched_paths`, and `next`.
- Every eval MUST have `req_ids`, `task_ids`, `procedure`, and `pass_condition`.
- `package.yaml` MUST retain handoff state: `current_progress`, `next_step`, `blockers`.
- `design.md` MUST include boundary, interfaces, failure modes, and requirement mapping.
- `risks.yaml` SHOULD follow the current AxiomSpecs house shape: `risks:` list with `id`, `title`, `severity`, `mitigation`. Do not add new required top-level keys unless the owner repo introduces them.
- `decisions.jsonl` SHOULD follow the current AxiomSpecs house shape: each line is one JSON object with `id`, `ts`, `summary`, `reason`.
- Do not invent implementation-local semantics that belong to `AxiomRunner`, `AxiomNexus`, or `codex-runtime`.
- When current code reality is unknown, say so explicitly in `intent.md` or `design.md` and keep unresolved items as open questions.

## Read Paths

- `input.packet.yaml` when provided
- `route.decision.yaml` when provided
- `product-charter.md` and `system-blueprint.md` when the route requires framing first
- bundled owner-summary docs in [references/OWNERSHIP_AND_OUTPUT_CONTRACT.md](references/OWNERSHIP_AND_OUTPUT_CONTRACT.md)
- target package files when `mode=update`
- relevant current-truth files cited in the packet's `source_context_refs` and `evidence_refs`

## Write Paths

- exactly one target feature package directory under `specs/features/FEAT-xxxx-slug/`
- one `handoff.packet.yaml` at `<target_feature_path>/handoff.packet.yaml` (or `output_handoff_path` if specified)

## Output Target

- AxiomSpecs feature package source files
- one authoring-stage handoff packet (stage: feature-package-authoring)
- review-stage handoff and final readiness verdict are owned by `package-readiness-review`

## Workflow

> `$AXIOM_MD` = path to the AxiomMd repository root. Steps using this variable require the AxiomMd toolkit to be available locally.

1. If `input.packet.yaml` is provided, run:
   `python $AXIOM_MD/scripts/workflow_check.py packet <path/to/input.packet.yaml>`
2. Read existing package files if `mode=update`.
3. Extract the required authoring facts from the packet, current package, and cited repository evidence.
4. Preserve stable IDs where continuity exists.
5. Draft or patch the package files using [assets/package-skeleton.md](assets/package-skeleton.md).
6. Run:
   `python $AXIOM_MD/scripts/workflow_check.py package <feature-dir> --base-dir <AxiomSpecs>`
7. Write authoring-stage `handoff.packet.yaml` at `<target_feature_path>/handoff.packet.yaml` (or `output_handoff_path`) and run:
   `python $AXIOM_MD/scripts/workflow_check.py handoff <path/to/handoff.packet.yaml> --base-dir <AxiomSpecs>`
8. Patch until the target package is structurally acceptable in the owner repo checker, or stop with a precise blocker list.
9. Before finishing, re-check [assets/author-checklist.md](assets/author-checklist.md).

## Stop Conditions

Stop and return a blocker report if:

- required authoring facts are missing
- feature scope is not bounded
- target repo is not `AxiomSpecs`
- semantic owner is unclear
- adoption mapping is missing for referenced external repos
- `workflow_check.py package` still fails for the target package and the missing data cannot be derived from repository evidence

## Final Rule

This skill does not decide whether the package is launchable.
It produces or repairs package source and closes the authoring stage with a handoff packet.
Readiness is still closed by `package-readiness-review` or equivalent human review.
