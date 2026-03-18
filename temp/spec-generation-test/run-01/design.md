# Design

## Boundary

### In Scope

- CLI orchestrator (`axm`) that implements intake → route → feature authoring → readiness handoff loops.
- Contract-driven workflow integration with AxiomMd skill assets and outputs.
- Artifact validation with strict/check modes and machine-readable reporting.
- Optional status UI surface and resume controls in a first-class command model.

### Out of Scope

- Full IDE-level visual editing of all specification files.
- Automatic ticket-system integration in MVP (deferred to adapter layer).

## Data and State

- `axm_state`: runtime metadata for run id, stage, stage inputs, retry counters, and last failures.
- `artifact_index`: resolved paths for stage outputs.
- `hilt_events`: list of gate reasons (scope ambiguity, contradictory requirements, destructive path).

## Interfaces

- `CLI` (commands: `run`, `check`, `validate`, `resume`, `doctor`)
- `Templates`: `templates/*` contract files + skill assets
- `Validators`: `scripts/workflow_check.py` and axm-native validators
- `UI/Status`: operator-facing status surface with queue, artifact health, and artifact diffs

## Failure Modes

- Route is ambiguous: pipeline stops and emits a human gate reason.
- Validator fails: stage output files are not emitted or references are missing.
- Resume conflict: stale working directory artifact conflicts with current run.

## Mapping to Requirements

- REQ-0001 -> package.yaml, requirements.yaml, design.md, tasks.md, evals.yaml, risks.yaml, package validation
- REQ-0002 -> agent-config module + execution logs
- REQ-0003 -> status surface + evidence/diagnostic event stream
- REQ-0004 -> handoff + resume command semantics

## Alternatives Rejected

- Single binary with hardcoded skills: rejected because adding new skills requires code deploy instead of contract-driven extension.
- UI-only status flow: rejected due low-trust environments requiring CLI-first operator control.
- Unbounded workflow DSL execution: rejected due inability to guarantee handoff consistency and replayability.
