# Execution Contract Summary

## Purpose

이 문서는 `manual-contract-compiler`가 실행 중 반복해서 확인해야 하는
최소 owner-summary다.

이 문서는 owner repo 정본을 대체하지 않는다.
정본은 아래다.

- AxiomMd: generic execution-planning artifact contract
- AxiomSpecs: package truth, slice truth, run-outcome meaning

## Unit of Work

기본 단위는 package 전체가 아니라 **selected slice 하나**다.

compile은 아래를 만족해야 한다.

- 하나의 package만 읽는다
- 하나의 slice만 선택한다
- slice boundary를 넓히지 않는다
- linked req/task/eval ids를 보존한다

## What This Skill Produces

이 스킬은 아래 묶음을 만든다.

- `execution-brief.md`
- `goal.json`
- `workflow-pack.overlay.yaml`
- `launch.request.yaml`
- `execution.plan.yaml`
- compile-stage `handoff.packet.yaml`

이 스킬은 run을 실행하지 않는다.
이 스킬은 evidence를 정규화하지 않는다.
이 스킬은 reconcile 분류를 내리지 않는다.

## Compile Eligibility

compile을 시작하려면 최소 아래가 참이어야 한다.

- package path가 유효하다
- selected slice가 존재한다
- selected slice가 launchable이다
- package state가 compile-eligible이다
- linked req/task/eval ids가 모두 해석 가능하다
- approval posture와 budget이 해석 가능하다

하나라도 아니면 `INPUT_GAP_REPORT`로 멈춘다.

## Boundary Rules

절대 하면 안 되는 것:

- source package를 조용히 수정하기
- slice scope를 넓히기
- req/task/eval linkage를 새로 발명하기
- runtime-specific field를 추측으로 추가하기
- approval posture를 바꾸기

## Output Grounding Rule

모든 출력은 selected package/slice에서 근거를 찾아야 한다.

- `goal.json`은 slice scope 안에서만 작성한다
- `workflow-pack.overlay.yaml`은 package-local verification intent만 반영한다
- `launch.request.yaml`은 approval mode와 budget을 보존한다
- `execution.plan.yaml`은 execution-planning stage artifact다

## Handoff Rule

이 스킬이 쓰는 `handoff.packet.yaml`의 stage는
`execution-planning`이다.

이 handoff는 아래를 넘겨야 한다.

- selected package reference
- selected slice reference
- produced compile artifacts
- unresolved gaps
- next step
- blockers
