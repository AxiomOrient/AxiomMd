# EVAL_POLICY.md

## Purpose

This document defines how evaluation works.

> `evals.yaml` is the source of verification truth.

## Principles

1. Every `must` requirement needs at least one blocking eval.
2. Every task must link to at least one eval.
3. Verifier owns blocking eval intent.
4. Blocking eval intent must be stable.
5. Test implementation may change only if eval intent stays the same.
6. Eval intent change requires Architect approval.
7. Passing tests do not override broken invariants.

## Ownership Boundary

Developer may implement or repair tests, but may not silently rewrite blocking truth.
If the expected behavior itself must change, escalate before editing eval intent.
