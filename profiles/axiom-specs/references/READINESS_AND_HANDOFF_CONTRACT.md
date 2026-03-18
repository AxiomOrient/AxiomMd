# Readiness And Handoff Contract (AxiomSpecs Profile)

이 문서는 AxiomSpecs 프로파일이 활성화된 경우 generic READINESS_AND_HANDOFF_CONTRACT를 대체한다.

## Source Basis

This profile is aligned to these owner-repo files:

- `method/artifact-and-contract.md` (Package Readiness Gate section)
- `method/authoring-workflows.md`
- `templates/handoff.packet.yaml`
- `AxiomSpecs/README.md`
- `AxiomSpecs/docs/03_SERVICE_SPEC.md`
- `AxiomSpecs/specs/STANDARD_STACK.md`
- `AxiomSpecs/profiles/axiom-v1/profile.yaml`
- `AxiomSpecs/profiles/axiom-v1/package-and-readiness.shape.yaml`
- `AxiomSpecs/specs/README.md`
- `AxiomSpecs/specs/features/README.md`
- `AxiomSpecs/scripts/check_specs`
- `AxiomSpecs/specs/features/FEAT-0001-manual-execution-contract/requirements.yaml`

Do not fetch owner-repo files from GitHub at runtime.
Refresh this summary only when the owner repos change.

## Ownership Split

- AxiomMd owns the review-stage handoff packet format and the generic 5-gate structure.
- AxiomSpecs owns the meaning of `ready | patch-required | hold` for product-truth packages.
- The review skill must not replace package truth and must not silently edit package files.

## Authoritative Review Output

For workflow continuity, review/readiness must emit `handoff.packet.yaml`.

Required handoff fields:

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
Use `blocked` only when review cannot determine a gate status.

## Human-Readable Sidecar

AxiomSpecs FEAT-0001 currently allows the gate result and reason to remain in `package.yaml` or a review note.
This skill is review-only, so the valid sidecar is an optional `readiness-report.md`.
The sidecar is not the authoritative workflow handoff.

## Structural Baseline

Use the owner repo checker with base-dir:

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
