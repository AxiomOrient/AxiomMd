# Readiness And Handoff Contract

## Source Basis

This skill is aligned to these owner-repo files:

- `AxiomMd/method/package-readiness-gate.md`
- `AxiomMd/method/workflow-io-protocol.md`
- `AxiomMd/templates/handoff.packet.yaml`
- `AxiomSpecs/README.md`
- `AxiomSpecs/docs/03_SERVICE_SPEC.md`
- `AxiomSpecs/specs/STANDARD_STACK.md`
- `AxiomSpecs/profiles/axiom-v1/profile.yaml`
- `AxiomSpecs/profiles/axiom-v1/package-and-readiness.shape.yaml`
- `AxiomSpecs/specs/README.md`
- `AxiomSpecs/specs/features/README.md`
- `AxiomSpecs/scripts/check_specs`
- `AxiomSpecs/specs/features/FEAT-0001-manual-execution-contract/requirements.yaml`

This file is a local summary for the installed skill.
Do not fetch those owner-repo files from GitHub at runtime.
Refresh this summary only when the owner repos change.

## Ownership Split

- AxiomMd owns the review-stage handoff packet format.
- AxiomSpecs owns the meaning of `ready | patch-required | hold` for product-truth packages.
- The review skill should not replace package truth and should not silently edit package files.

## Authoritative Review Output

For workflow continuity, review/readiness must emit `handoff.packet.yaml`.

Required AxiomMd handoff fields:

- `packet_version`
- `stage`
- `status`
- `input_ref`
- `changed_paths`
- `produced_paths`
- `evidence_refs`
- `open_questions`
- `next_step`
- `blockers`

For this skill, `stage` should normally be `readiness-and-handoff`.
Normal review verdicts are `ready | patch-required | hold`.
The generic handoff template also allows `blocked`, but this skill should use that only when review cannot determine a gate status.

## Human-Readable Sidecar

AxiomSpecs FEAT-0001 currently allows the gate result and reason to remain in `package.yaml` or a review note.
This skill is review-only, so the valid sidecar is an optional Markdown review note.
The sidecar is not the authoritative workflow handoff.

## Structural Baseline

Use the owner repo checker:

```bash
python $AXIOM_MD/scripts/workflow_check.py package <feature-dir> --base-dir <AxiomSpecs>
```

This checker is the current owner-repo source for:

- required file set
- `contracts/` directory presence
- package metadata minimum
- REQ/TASK/EVAL linkage completeness
- package handoff metadata presence

At runtime, use the local target repository copy of that checker.

## Additional Review Expectations

Beyond the owner checker, keep reviewing for:

- bounded scope
- no generic duplication
- no implementation-local leakage
- explicit verification posture
- restartability after interruption
