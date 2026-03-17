# Client Intent To Spec Workflow

## Purpose

이 문서는 클라이언트 요청, 기획서, 미팅 노트 같은 초기 입력에서
실제로 구현 가능한 spec까지 어떤 workflow를 거쳐 좁혀 가는지 정의한다.

## Core Rule

초기 입력은 바로 spec이 아니다.

먼저 workflow 단위로 아래 순서로 정리해야 한다.

1. intake and routing
2. framing if needed
3. feature package authoring
4. readiness and handoff

## Document Stack

항상 모든 문서를 만들 필요는 없다.
상황에 따라 아래처럼 쓴다.

### Level 0. Raw Input

예:

- 클라이언트 요청
- 기획서
- 회의 메모
- PRD
- 운영 이슈 설명

이 단계는 source material이다.
바로 실행 계약으로 쓰지 않는다.

### Level 1. Input Packet

항상 먼저 만든다.

- 형식: `templates/input.packet.yaml`
- 목적: 초기 입력을 agent와 사람이 같이 읽을 수 있는 최소 형식으로 정리

이 문서가 없으면 다음 단계가 입력을 제각각 해석하게 된다.

### Level 2. Route Decision

항상 intake workflow 안에서 같이 만든다.

- 형식: `templates/route.decision.yaml`
- 목적: 바로 package로 갈지, framing을 먼저 할지 고정

### Level 3. Product Framing Docs

아래 둘은 필요할 때만 만든다.

#### Product Charter

언제 필요한가:

- 요청이 제품 전체 방향을 바꾼다
- 무엇을 만들지보다 왜 만드는지가 더 불명확하다
- 범위 밖과 비목표가 아직 흐리다

무엇을 써야 하는가:

- 문제
- 사용자 / 운영자
- 목표
- 비목표
- 성공 조건
- 주요 제약

#### System Blueprint

언제 필요한가:

- 한 feature가 아니라 여러 영역을 같이 건드린다
- 경계, 역할, plane, major component가 아직 모호하다
- 어느 feature package로 쪼갤지 결정이 안 된다

무엇을 써야 하는가:

- 큰 구조
- 경계
- 주요 흐름
- major component / plane
- 무엇을 source truth로 둘지
- 어디까지 이번 범위인지

### Level 4. Feature Package

실제로 구현을 열기 전 반드시 필요하다.

형식:

- `specs/SPEC_PACKAGE_STANDARD.md`

필수 파일:

- `intent.md`
- `package.yaml`
- `requirements.yaml`
- `invariants.yaml`
- `design.md`
- `tasks.md`
- `evals.yaml`
- `risks.yaml`
- `decisions.jsonl`

### Level 5. Readiness Review

구현 전에 반드시 필요하다.

- 기준: `docs/09_PACKAGE_READINESS_GATE.md`
- 결과: `ready | patch-required | hold`
- 형식: `templates/readiness-report.md`

## Routing Rule

처음 입력을 받으면 먼저 이 질문을 본다.

### Case A. 바로 feature package로 갈 수 있는 경우

아래가 이미 보이면 바로 feature package로 간다.

- 문제 범위가 좁다
- in-scope / out-of-scope가 보인다
- 성공 조건이 보인다
- 관련 repo/path/contract 범위가 대략 보인다

이 경우:

```text
raw input
-> intake and routing
-> feature package authoring
-> readiness and handoff
```

### Case B. Product framing이 먼저 필요한 경우

아래 중 하나라도 해당하면 먼저 charter/blueprint가 필요하다.

- 요청이 너무 넓다
- 한 번에 여러 기능을 섞고 있다
- 시스템 경계가 불분명하다
- 무엇이 이번 범위 밖인지 모른다
- feature 분해가 아직 안 된다

이 경우:

```text
raw input
-> intake and routing
-> framing
-> feature package authoring
-> readiness and handoff
```

## What Must Be In The Input Packet

최소 아래는 채워야 한다.

- `request_summary`
- `target_kind`
- `source_context_refs`
- `scope.in`
- `scope.out`
- `constraints`
- `done_signals`
- `open_questions`
- `evidence_refs`

좋은 입력 packet은 아래를 같이 보여준다.

- 무엇을 만들지
- 무엇을 만들지 않을지
- 지금 아는 사실
- 아직 모르는 사실
- 성공을 어떻게 볼지

## What Must Be In The Route Decision

최소 아래는 채워야 한다.

- `input_ref`
- `route`
- `reason_summary`
- `required_artifacts`
- `next_step`
- `open_questions`
- `blockers`

좋은 route decision은 아래를 같이 보여준다.

- 왜 direct path인지 또는 framing path인지
- 어떤 문서가 다음에 필요해지는지
- 지금 멈춰야 하는지 아닌지

## What Makes A Good Feature Package

좋은 feature package는 아래를 만족한다.

- 한 가지 bounded feature만 다룬다
- must requirement가 blocking eval로 닫힌다
- task가 req/eval에 연결된다
- design이 boundary와 failure mode를 설명한다
- 다른 사람이 chat 없이 재개할 수 있다

## Workflow Set

기본 workflow는 아래 네 개가 가장 적합하다.

### 1. Intake And Routing Workflow

역할:

- raw input를 `input.packet.yaml`으로 정리
- direct path인지 framing path인지 판정

출력:

- `input.packet.yaml`
- `route.decision.yaml`

### 2. Framing Workflow

역할:

- product-level framing 문서 작성

출력:

- `product-charter.md`
- `system-blueprint.md`
- `handoff.packet.yaml`

### 3. Feature Package Authoring Workflow

역할:

- `input.packet.yaml`과 current truth를 바탕으로 split feature package 작성

출력:

- feature package file set
- `handoff.packet.yaml`

### 4. Readiness And Handoff Workflow

역할:

- package를 `ready | patch-required | hold`로 판정

출력:

- `readiness-report.md`
- `handoff.packet.yaml`

## Skill Position

skill은 workflow를 이루는 세부 도구다.
workflow보다 앞에 오면 안 된다.

예를 들어 같은 workflow 안에서 아래 같은 세부 작업 도구를 둘 수 있다.

- 입력 정규화
- route 판정
- framing 문서 작성
- feature package 작성
- readiness 판정

## Best Practical Rule

한 번에 큰 spec을 쓰려고 하지 말고,
항상 workflow 단위로 줄여라.

```text
raw input
-> intake and routing
-> framing if needed
-> feature package authoring
-> readiness and handoff
```

## Validation Order

sample run이나 실제 도입 검증에서는 아래 순서로 본다.

1. `input.packet.yaml`
2. `route.decision.yaml`
3. framing docs
4. feature package
5. `handoff.packet.yaml`

앞 단계가 약하면 뒷단 문서가 좋아 보여도 전체 workflow는 약하다.

## Final Rule

좋은 spec workflow는 skill을 많이 나열하는 workflow가 아니다.
하나의 일과 작업이 되는 몇 개의 큰 workflow를 두고,
각 workflow가 다음 단계가 읽을 파일을 남기는 구조가 더 좋다.
초기 입력을 점점 더 좁고 기계적으로 읽히는 형식으로 바꿔 가는 workflow다.
