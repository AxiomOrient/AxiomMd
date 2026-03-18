# Output Profile Interface

## Purpose

이 문서는 generic workflow kernel이
product-specific output profile을 어떻게 연결하는지 정의한다.

핵심 원칙은 단순하다.

- generic artifact contract는 AxiomMd가 소유한다
- product-specific output profile은 각 product repo가 소유한다
- generic kernel은 profile resolution interface만 소유한다

## Why This Exists

같은 workflow라도 제품마다 아래가 달라질 수 있다.

- package metadata 필드
- readiness meaning
- slice local shape
- execution contract shape
- evidence bundle shape
- reconcile record shape

이 차이를 generic kernel 안에 직접 넣으면
kernel이 product repo로 오염된다.

반대로 profile interface를 두면
kernel은 좁게 유지되고 제품별 확장은 분리된다.

## Core Rule

product-specific output profile은 아래 조건을 만족해야 한다.

1. generic required field를 제거할 수 없다
2. generic artifact contract 위에 확장만 할 수 있다
3. profile key와 manifest가 존재해야 한다
4. local validator와 local examples를 가져야 한다

## Required Concepts

### `profile_key`

package가 어떤 product profile을 따르는지 식별한다.

예:

- `axiom-v1`
- `billing-v2`
- `runtime-core-v1`

### profile manifest

product repo는 자기 profile manifest를 제공해야 한다.

manifest는 아래를 설명한다.

- profile key
- version
- package shape
- readiness rules
- slice shape
- optional execution contract shape
- optional evidence shape
- optional reconcile shape

## Resolution Rule

generic workflow 또는 skill은 아래 순서로 동작한다.

1. generic artifact minimum contract를 검사한다
2. `profile_key`를 읽는다
3. 해당 product repo의 profile manifest를 resolve한다
4. local overlay rule을 적용한다
5. generic + local validator를 모두 통과시킨다

## Ownership Rule

AxiomMd가 소유하는 것:

- profile interface
- resolution rule
- generic required fields
- generic validation order

product repo가 소유하는 것:

- 실제 profile implementation
- local shape
- local field meaning
- local readiness rule
- local execution / evidence / reconcile semantics

## Validation Rule

product profile은 아래를 제공해야 한다.

- profile manifest
- local schema or checker
- example package
- failure examples if possible

generic kernel은 profile implementation을 직접 품지 않는다.
대신 profile implementation이 generic contract를 위반하지 않는지 검사한다.

## Final Rule

product-specific output contract는 옵션이지만,
그 옵션을 꽂는 방식은 공통이어야 한다.
그 공통 방식이 바로 output profile interface다.
