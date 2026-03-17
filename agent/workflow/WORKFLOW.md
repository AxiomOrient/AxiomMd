# WORKFLOW.md

## Purpose

This document defines the smallest correct workflow set for spec-driven agentic development.

## Core Rule

> Spec defines intent. Plan defines scope. Verifier defines truth. Developer implements only approved work.

## Two Layers

이 방법론은 workflow를 두 층으로 나눈다.

1. spec authoring workflow
2. execution loop

작성과 실행을 한 덩어리로 두지 않으면 경계가 더 명확해진다.

## Spec Authoring Workflow Set

```text
intake-and-routing
-> framing (if needed)
-> feature-package-authoring
-> readiness-and-handoff
```

각 workflow는 하나의 큰 작업 단위여야 한다.
micro-step를 workflow로 부르지 않는다.

### Required Outputs

- intake-and-routing: `input.packet.yaml`, `route.decision.yaml`
- framing: `product-charter.md`, `system-blueprint.md`, `handoff.packet.yaml`
- feature-package-authoring: package file set, `handoff.packet.yaml`
- readiness-and-handoff: `readiness-report.md`, `handoff.packet.yaml`

## Execution Loop

```text
approved package
-> bounded execution
-> verification
-> reconcile
-> acceptance
```

spec authoring workflow가 끝난 뒤에만 execution loop가 열린다.

## Required Package Surface

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

## Workflow I/O Rule

Every stage must consume file-state input and leave file-state output.

- authoring path -> packet / document / package files
- execution path -> source changes + evidence
- stage handoff -> `handoff.packet.yaml`

Chat may explain the work, but chat is not the protocol.

## Verification

Verifier owns verification truth.

- maintain `evals.yaml`
- create and maintain blocking tests
- run verification
- produce evidence
- classify pass, fail, or blocker

## Final Rule

Do not optimize for maximum generation.
Optimize for bounded workflows, precise packages, mechanical verification, and clean handoff.
