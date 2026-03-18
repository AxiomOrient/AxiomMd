# Readiness And Handoff Contract

## Source Basis

This skill is aligned to these kernel files:

- `method/artifact-and-contract.md` (Package Readiness Gate section)
- `method/authoring-workflows.md`
- `templates/handoff.packet.yaml`

If a profile is active, this skill is also aligned to the profile manifest at:

- `<profile_root>/profiles/<profile_key>/shape.yaml`

This file is a local summary for the installed skill.
Do not fetch owner-repo files from GitHub at runtime.
Refresh this summary only when the kernel or profile contract changes.

## Ownership Split

- AxiomMd owns the review-stage handoff packet format and the generic 5-gate structure.
- The product profile (if provided) owns product-specific gate extensions.
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

The valid sidecar output is an optional `readiness-report.md`.
The sidecar is not the authoritative workflow handoff.

## Structural Baseline

Use the kernel checker:

```bash
python $AXIOM_MD/scripts/workflow_check.py package <feature-dir>
```

This checker is the source for:

- required file set
- package metadata minimum
- REQ/TASK/EVAL linkage completeness
- package handoff metadata presence

If a profile is active, run the profile validator after generic gates pass.

## Additional Review Expectations

Beyond the generic checker, keep reviewing for:

- bounded scope
- no generic duplication
- no implementation-local leakage
- explicit verification posture
- restartability after interruption
