# Quality System

## Purpose

이 문서는 agentic development에서 코드가 왜 흐트러지는지, 실패를 어떻게 환경 개선으로 되돌릴지 정의한다.

## Why Code Gets Messy

AI는 좋은 코드만 빠르게 만들지 않는다.
나쁜 패턴도 빠르게 복제한다.

문제의 본체는 대개 모델 자체보다 아래다.

- 컨텍스트가 약하다
- 완료 조건이 약하다
- 검증이 약하다
- 반복 실수를 규칙으로 올리지 않는다
- 유지보수 루프가 없다

## Quality Thesis

> AI 시대의 코드 품질은 생성 능력이 아니라 정리 능력으로 결정된다.

## Control Layers

### 1. Input Quality

- request를 먼저 `input.packet.yaml`로 정규화한다
- route decision 없이 바로 package로 밀어 넣지 않는다
- 모호함은 open question으로 남긴다

### 2. Plan Quality

- framing이 필요하면 charter / blueprint로 먼저 좁힌다
- 모든 task는 `REQ-*`와 `EVAL-*`를 가진다
- scope expansion을 막는다

### 3. Execution Quality

- 작은 loop만 허용한다
- 승인 없는 새 행동은 막는다

### 4. Verification Quality

- structure check
- contract check
- invariant check
- regression check
- risk check
- readiness check

### 5. Reconciliation Quality

- 결정은 `decisions.jsonl`로 남긴다
- drift를 class로 분류한다
- source를 다시 맞춘다

### 6. Maintenance Quality

- task 종료 시 local tidy
- feature 종료 시 commonization
- 주기적으로 entropy sweep

## Promotion Ladder

반복 실수는 아래 순서로 승격한다.

1. comment
2. checklist
3. repository rule
4. template
5. harness
6. codemod or tool

같은 실수를 두 번 이상 사람 리뷰로만 막고 있다면 승격이 부족한 것이다.

## Failure Analysis Rule

AI 실패는 먼저 모델 탓을 하지 않는다.
아래 순서로 본다.

1. Reproduce
2. Observe
3. Hypothesize
4. Verify
5. Fix root cause

## Failure Thesis

> 많은 AI 실패는 모델 실패가 아니라 하네스 실패다.

그래서 실패 후에는 항상 아래 중 하나가 바뀌어야 한다.

- 문서
- template
- task sizing
- tool contract
- verification
- approval rule

## Cleanup Cadence

| 시점 | 해야 할 정리 |
| --- | --- |
| workflow close | handoff packet, open question, next step 정리 |
| task close | local cleanup, validation update |
| feature close | duplication 정리, decisions 정리, package update |
| periodic maintenance | repeated smell 정리, codemod 기회 발굴 |

## Final Rule

좋은 agentic development는 “더 많이 생성하는 것”이 아니라 아래를 만든다.

- 더 잘 읽히는 구조
- 더 강한 verification
- 더 짧은 feedback loop
- 더 나은 restartability
