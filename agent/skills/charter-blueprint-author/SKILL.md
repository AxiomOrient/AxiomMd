---
name: charter-blueprint-author
description: Create product charter and system blueprint documents when a normalized input packet is too broad for direct feature package authoring. Use when framing must come before feature split.
---

# Charter Blueprint Author

## Purpose

Create product-level framing docs from one normalized `input.packet.yaml`.

This is a **source-changing skill**.

## Read First

1. [references/FRAMING_DOC_CONTRACT.md](references/FRAMING_DOC_CONTRACT.md)
2. [assets/product-charter.md](assets/product-charter.md)
3. [assets/system-blueprint.md](assets/system-blueprint.md)
4. [assets/framing-checklist.md](assets/framing-checklist.md)

## Use This Skill When

- `scope-router` chose `framing-first`
- the request is too broad for direct feature package authoring
- feature split needs product framing first

## Do Not Use This Skill When

- the request is already a bounded feature
- the work is a review-only pass
- the output should be a feature package, not product framing docs

## Input Contract

Required:

- `input.packet.yaml`
- optional `route.decision.yaml`

The packet must already show:

- request summary
- in-scope / out-of-scope
- constraints
- done signals

The packet SHOULD cite current truth via `source_context_refs` and/or `evidence_refs`.

## Output Contract

Write:

- `product-charter.md`
- `system-blueprint.md`
- `handoff.packet.yaml` with `stage: framing`

These are framing docs, not implementation packages.
The handoff packet closes the framing stage and hands off to feature-package-authoring.
If `output_handoff_path` is not specified, write `handoff.packet.yaml` next to the packet at the working directory root.

## Read Paths

- normalized `input.packet.yaml`
- optional `route.decision.yaml`
- bundled owner-summary rules in [references/FRAMING_DOC_CONTRACT.md](references/FRAMING_DOC_CONTRACT.md)
- target repo evidence cited by the packet

## Write Paths

- the user-selected framing doc paths for `product-charter.md` and `system-blueprint.md`
- `handoff.packet.yaml` at `output_handoff_path` or the working directory root

## Output Target

- one bounded pair of framing docs
- one framing-stage handoff packet
- no feature package files

## Workflow

1. Read the packet.
2. If available, confirm `route.decision.yaml` says `framing-first`.
3. Fill `product-charter.md`.
4. Fill `system-blueprint.md`.
5. If the AxiomMd toolkit is available, run:
   `python $AXIOM_MD/scripts/workflow_check.py framing <path/to/product-charter.md> <path/to/system-blueprint.md>`
   (`$AXIOM_MD` = path to the AxiomMd repository root)
6. Re-check [assets/framing-checklist.md](assets/framing-checklist.md).
7. Write `handoff.packet.yaml` with `stage: framing`, `status: ready | patch-required | hold`, `produced_paths` listing the two framing docs, and `next_step` pointing to feature-package-authoring.

## Stop Conditions

- packet missing
- route says `direct-package`
- scope is still too unclear to write framing docs honestly
- repository evidence is too weak to state boundary and major structure without guessing

## Final Rule

This skill does not create feature packages.
It only creates the framing docs needed before feature split.
