# Method Constitution

## Purpose

이 문서는 Spec-Driven Agentic Software Engineering의 불변 원칙을 고정한다.

## Principles

### 1. Specs Compile Intent

사람의 말은 시작점이다.
작업 기준은 spec package다.

### 2. Small Packages Beat Giant Manuals

큰 문서 한 장은 빨리 썩는다.
작은 package와 작은 문서 묶음이 더 오래 유지된다.

### 3. Plan Before Code

비사소한 작업은 plan과 eval 없이 구현으로 들어가지 않는다.

### 4. Humans Steer, Agents Execute

사람은 목표, 승인, 위험 수용, release를 맡는다.
agent는 승인된 범위 안의 실행을 맡는다.

### 5. Evidence Before Acceptance

“작동한다”는 말은 증거가 아니다.
acceptance는 tests, artifacts, traces, reconciliation 결과로만 닫는다.

### 6. Reconcile Over One-Shot Generation

처음 생성보다 더 중요한 것은 이후 동기화다.
코드, spec, tests, decisions는 계속 다시 맞춰야 한다.

### 7. Simplicity Means Precise Boundaries

심플함은 내용을 줄이는 것이 아니다.
정확히 필요한 내용을 제자리에 두는 것이다.

### 8. Failure Must Upgrade the Harness

반복되는 실수는 사람 기억에 남기지 않는다.
규칙, template, test, tool, codemod로 승격한다.

## Role Split

| 역할 | 책임 | 하면 안 되는 일 |
| --- | --- | --- |
| Human | 목표 설정, 승인, 위험 수용, release | 숨은 맥락만 남기고 떠나는 것 |
| Agent | compile, plan, implement, verify, reconcile | 승인 없이 spec 밖 행동을 추가하는 것 |
| Runtime | bounded execution과 artifact 생산 | authoritative truth를 임의로 바꾸는 것 |
| Governance | evidence 기반 accept/hold/reject 판단 | source package를 대신 쓰는 것 |

## Hard Rules

- requirement 없는 task 금지
- eval 없는 requirement 금지
- evidence 없는 completion claim 금지
- release를 execution success와 같은 뜻으로 쓰는 것 금지
- 중요한 결정을 chat에만 남기는 것 금지

## Stop Conditions

아래가 발생하면 계속 밀어붙이지 않는다.

- scope가 불명확하다
- invariant가 깨졌다
- high-risk인데 approval rule이 없다
- evidence를 만들 수 없다
- spec와 구현이 충돌하는데 drift 분류가 안 된다

## Design Consequence

이 방법론을 따르는 저장소는 반드시 아래를 가져야 한다.

- 짧은 routing 문서
- feature package 표준
- task와 eval linkage
- decision log
- handoff 가능한 상태
