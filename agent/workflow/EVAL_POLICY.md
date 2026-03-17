# EVAL_POLICY.md

## Purpose

This document defines how evaluation works.

> `evals.yaml` is the source of verification truth.

## Principles

1. Every `must` requirement needs at least one blocking eval.
2. Every task must link to at least one eval.
3. Blocking eval intent must be stable.
4. Test implementation may change only if eval intent stays the same.
5. Passing tests do not override broken invariants.
