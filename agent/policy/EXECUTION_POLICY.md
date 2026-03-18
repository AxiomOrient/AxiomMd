# EXECUTION_POLICY.md

## Purpose

This document defines execution state rules and operational control requirements.

> Every state transition must leave file-state. A state change without a file artifact is not a valid transition.

## Execution States

An execution unit must track one of the following states at all times.

| State | Condition | Required File-State |
| --- | --- | --- |
| `planned` | plan accepted, pre-conditions verified | `execution.plan.yaml` exists |
| `running` | execution in progress | stage and blockers visible in file |
| `blocked` | HILT or approval condition not met | next action recorded in `handoff.packet.yaml` |
| `failed` | execution failed | failure evidence path and recovery instruction in file |
| `succeeded` | execution complete | moves to reconcile-and-close |
| `resumed` | restored from prior run-id state | prior checkpoint verified deterministically |

## Checkpoint Rule

- Default checkpoint namespace: `run-id`
- State restore must be deterministic against the same run-id.
- `feature-id` is a secondary label for aggregation only, not a checkpoint key.
- Resume requires run-id to be explicitly named or confirmed after querying last known state.

## Control Policy Requirements

Before execution starts, each of the following must be defined:

- timeout per stage (exceeded → `blocked` or `failed`, not silent)
- retry eligibility (idempotent steps only)
- approval posture for high-risk actions
- budget limits (tokens / time / output size)

## Observability Rule

At any point, the following must be recoverable from file-state:

- current stage and status
- blockers and open questions
- last failure reason
- evidence_refs
- changed_paths and produced_paths

## Escalation Triggers (Execution-Specific)

These apply inside the execution loop. See ESCALATION_POLICY.md for the full list.

- execution hits a timeout with no blocker recorded
- retry attempted on a non-idempotent step
- budget exceeded without prior approval
- checkpoint restore fails determinism check
- `blocked` state has no `next_action` in file
