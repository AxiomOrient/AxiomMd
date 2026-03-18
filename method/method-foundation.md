# Method Foundation

## Taxonomy

AI 개발 방법론은 아래 다섯 가지로 구분한다.

| 방법 | 특징 |
| --- | --- |
| AI-Assisted Coding | LLM을 보조 도구로 사용. 실행 주체는 사람. prompt와 code diff 중심 |
| Agentic Development | agent가 tool을 사용하며 loop. 단일/multi-agent 가능. 범위 넓고 품질 편차 큼 |
| Agent-Orchestrated Development | 계획/구현/검증/handoff가 역할 또는 단계로 나뉨. orchestration layer가 핵심 |
| Closed-Loop Agentic Development | plan → execute → verify → reconcile 루프로 닫힘. feedback과 restartability 전제 |
| Spec-Driven Agentic Software Engineering | 자연어를 spec package로 컴파일. spec package가 source of truth. agent loop가 spec, eval, evidence 기준으로 돌아감 |

## Selected Method

이 저장소가 채택한 공식 이름.

> **Spec-Driven Agentic Software Engineering**

세 뜻을 동시에 가진다.

- `Spec-Driven`: 자연어가 아니라 구조화된 spec package를 기준으로 일한다.
- `Agentic`: 계획, 구현, 검증, 조정이 agent loop 안에서 돌아간다.
- `Software Engineering`: 코드 생성만이 아니라 계약, 검증, 운영, evidence까지 포함한다.

실행 방식의 이름.

> **Closed-Loop Harnessed Development**

- 작업은 열린 프롬프트가 아니라 닫힌 루프로 돈다.
- agent는 자유 방치가 아니라 harness 안에서 움직인다.
- 완료는 self-report가 아니라 evidence로 닫힌다.

이 방법은 아래와 다르다.

- 단순 AI-assisted coding
- vibe coding
- 한 번의 거대 프롬프트로 끝내는 개발
- 문서 한 장을 source-of-truth로 삼는 방식

## Why This Method Exists

AI가 강한 것은 국소 구현이다.
AI가 약한 것은 장기 맥락 유지, 경계 보존, drift 제어다.

따라서 방법론의 본체는 "더 잘 생성하기"가 아니라 아래다.

- intent를 구조화하기
- 작업을 작은 loop로 자르기
- evidence 없이 통과시키지 않기
- 실패를 harness 개선으로 되돌리기

## Core Unit

이 방법의 최소 단위는 "채팅"이 아니다.
최소 단위는 아래 묶음이다.

```text
input packet
-> route decision
-> optional framing docs
-> feature package
-> readiness
-> approved package
-> bounded execution
-> verification
-> reconcile
```

## Source-of-Truth Rule

자연어는 입력이다.
source of truth는 아래 묶음이다.

- `input.packet.yaml`
- `route.decision.yaml`
- `package.yaml`
- `requirements.yaml`
- `invariants.yaml`
- `design.md`
- `tasks.md`
- `evals.yaml`
- `risks.yaml`
- `decisions.jsonl`
- `slices.yaml`

상황에 따라 아래가 추가된다.

- `product-charter.md`
- `system-blueprint.md`
- `readiness-report.md`

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

"작동한다"는 말은 증거가 아니다.
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

- route decision 문서
- input packet
- feature package 표준
- readiness report
- task와 eval linkage
- decision log
- handoff 가능한 상태
