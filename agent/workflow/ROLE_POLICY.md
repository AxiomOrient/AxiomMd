# ROLE_POLICY.md

## Purpose

This document defines minimum role ownership.

> Ownership must be clear enough that source of truth cannot drift by accident.

## Roles

### PM

Owns project goal, priority, scope, and acceptance posture.

### Architect

Owns boundaries, invariants, risk posture, design approval, and eval-intent changes.

### Developer

Owns implementation of approved tasks and task status updates.

Does not own:

- `evals.yaml`
- blocking test intent
- invariant changes
- unapproved scope expansion

### Verifier

Owns:

- `evals.yaml`
- blocking tests
- verification execution
- evidence draft
- validation result
