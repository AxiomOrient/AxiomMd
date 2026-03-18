---
name: intake-normalizer
description: Normalize raw client input, PRD notes, or meeting notes into an AxiomMd input packet. Use when the source material is still messy and the next step needs a precise packet instead of free-form prose.
---

# Intake Normalizer

## Purpose

Turn raw client input into one normalized `input.packet.yaml`.

This is a **source-changing skill**.
It writes the input packet only.

## Read First

1. [references/INPUT_PACKET_CONTRACT.md](references/INPUT_PACKET_CONTRACT.md)
2. [assets/input.packet.yaml](assets/input.packet.yaml)
3. [assets/normalization-checklist.md](assets/normalization-checklist.md)

## Use This Skill When

- the source is a client request, PRD, meeting note, or rough brief
- the next step needs a deterministic packet
- the target work is not yet ready for direct authoring

## Do Not Use This Skill When

- a valid `input.packet.yaml` already exists
- the task is already in feature package form
- the task is a review-only pass

## Input Contract

Accepted raw inputs:

- PRD
- meeting notes
- client brief
- rough problem statement
- chat summary

The raw input must still provide enough evidence to fill:

- request summary
- in-scope / out-of-scope
- constraints
- done signals
- current source/evidence refs or explicit unknowns

If these cannot be derived, stop with `INPUT_GAP_REPORT`.

## Output Contract

Write exactly one `input.packet.yaml` that matches [assets/input.packet.yaml](assets/input.packet.yaml).

## Read Paths

- raw client brief, PRD, meeting notes, or chat summary provided for normalization
- bundled packet rules in [references/INPUT_PACKET_CONTRACT.md](references/INPUT_PACKET_CONTRACT.md)
- any current truth paths already cited in the raw source

## Write Paths

- `<target_feature_path>/input.packet.yaml`
- `target_feature_path`는 `constraints`에서 파생하거나 호출자가 명시한다.
- 경로를 알 수 없을 때는 STOP하고 `target_feature_path`를 요청한다. 루트에 쓰지 않는다.

## Output Target

- one normalized `input.packet.yaml`
- no product-truth docs
- no review handoff

## Write Rules

- normalize the raw input into packet fields
- keep unknowns in `open_questions`
- do not invent output contract details that belong to product truth
- keep `target_kind` explicit
- keep `source_context_refs` and `evidence_refs` concrete

## Workflow

1. Read the raw source material.
2. Fill `request_summary`.
3. Separate `scope.in` and `scope.out`.
4. Translate constraints into `constraints`.
5. Translate success conditions into `done_signals`.
6. Record missing facts in `open_questions`.
7. If the AxiomMd toolkit is available, run:
   `python $AXIOM_MD/scripts/workflow_check.py packet <path/to/input.packet.yaml>`
   (`$AXIOM_MD` = path to the AxiomMd repository root)
8. Re-check [assets/normalization-checklist.md](assets/normalization-checklist.md).

## Stop Conditions

- raw input is too vague to separate in-scope / out-of-scope
- success criteria cannot be derived
- no source/evidence basis exists and the request is too broad
- target kind cannot be chosen honestly from the available material
- `target_feature_path`를 파생할 수 없어 출력 경로가 불명확한 경우

## Final Rule

This skill does not decide product shape.
It only produces a clean packet for the next step.
