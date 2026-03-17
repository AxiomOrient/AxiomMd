# WORKFLOW.md

## Purpose

This workflow defines the simplest correct loop for spec-driven agentic development.

## Core Rule

> Spec defines intent. Plan defines scope. Verifier defines truth. Developer implements only approved work.

## Standard Loop

```text
intent
-> spec package
-> plan package
-> readiness gate
-> bounded execution
-> verification
-> reconcile
-> acceptance
```

## Required Packages

### Spec Package

- `intent.md`
- `package.yaml`
- `requirements.yaml`
- `invariants.yaml`
- `risks.yaml`

### Plan Package

- `design.md`
- `tasks.md`
- `evals.yaml`
- `decisions.jsonl`

## Verification

Verifier owns verification truth.

- maintain `evals.yaml`
- create and maintain blocking tests
- run verification
- produce evidence
- classify pass, fail, or blocker

## Final Rule

Do not optimize for maximum generation.
Optimize for precise packages, small loops, mechanical verification, and clean handoff.
