# Design

## Boundary

### In Scope

- Build a Rust CLI (`axm`) that orchestrates feature packaging workflow according to AxiomMd contracts.
- Emit a TUI status surface (read-only + guided actions) for pipeline operators.
- Persist checkpoints in local file cache and resume from last valid handoff.
- Enforce stage gating and handoff contract compliance.

### Out of Scope

- General-purpose source editor/IDE workflow
- Remote multi-tenant cluster orchestration

## Data and State

- `run_id`: workflow invocation identifier.
- `stage`: packet | route | package | readiness-and-handoff | reconcile-and-close.
- `status`: ready | patch-required | hold | blocked.
- `checkpoint`: file-cache record containing stage, handoff summary, and artifact manifests.
- `artifacts`: generated package files and log references.

## Interfaces

- CLI:
  - `axm run` / `axm check` / `axm status --watch` / `axm resume`.
- TUI:
  - Stage dashboard, logs summary, blockers panel, open questions panel, produced_paths link list.
- File cache:
  - Local checkpoint files under `.axm/run/<run_id>/state.jsonl`.
- File contracts:
  - `input.packet.yaml`, `route.decision.yaml`, package artifacts under target directory.

## Failure Modes

- Contract parse error: stop at blocker, emit handoff.reason and keep checkpoint for resume.
- Checker command failure: persist evidence refs with command output path and mark stage failed.
- Resume conflict: detect stale/incompatible run metadata and request manual override.

## Mapping to Requirements

- REQ-0001 -> package generator, contract checks, template outputs
- REQ-0002 -> TUI status and navigation requirements
- REQ-0003 -> file checkpoint read/write and resume path
- REQ-0004 -> handoff/stop gate behavior

## Alternatives Rejected

- Full web dashboard in v1: rejected due to first-priority focus on deterministic CLI/TUI operator workflows.
- SQLite state store: rejected for v1 due added operational complexity; v1 uses file-cache.
