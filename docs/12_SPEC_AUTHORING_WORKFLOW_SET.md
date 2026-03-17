# Spec Authoring Workflow Set

## Purpose

이 문서는 초기 요청에서 구현-ready feature package까지 가는 기본 workflow 세트를 정의한다.

## Why This Exists

한 번에 큰 spec 하나를 쓰려고 하면 아래 문제가 생긴다.

- 범위 판단이 문서 안에 섞인다
- 제품 수준 framing이 필요한지 늦게 알게 된다
- feature package가 너무 크거나 모호해진다
- readiness 검토가 작성 단계와 섞여 기준이 흐려진다

그래서 workflow는 **큰 작업 단위 네 개**로 나눈다.

## Workflow 1. Intake And Routing

### Job

초기 입력을 정규화하고, 다음 단계 경로를 결정한다.

### Reads

- raw request
- PRD
- meeting note
- client brief

### Writes

- `input.packet.yaml`
- `route.decision.yaml`

### Done When

- 요청이 정규화됐다
- 범위가 바로 package 가능한지 판정됐다
- 다음 workflow가 확정됐다
- route decision에 input ref와 blocker 상태가 남았다

### HILT

아래면 사람 확인이 필요하다.

- scope가 넓은데도 direct package로 보내려 할 때
- open question이 핵심 요구를 막고 있을 때
- non-goal이 비어 있을 때

## Workflow 2. Framing

### Job

제품 수준 방향과 큰 구조를 고정한다.

### Reads

- `input.packet.yaml`
- `route.decision.yaml`

### Writes

- `product-charter.md`
- `system-blueprint.md`
- `handoff.packet.yaml`

### Done When

- 문제 / 목표 / 비목표가 고정됐다
- 시스템 경계와 major component가 고정됐다
- feature split 가능한 수준으로 구조가 좁혀졌다

### HILT

아래면 사람 확인이 필요하다.

- 목표와 비목표가 충돌할 때
- source-of-truth posture가 불명확할 때
- feature split 기준이 합의되지 않았을 때

## Workflow 3. Feature Package Authoring

### Job

구현 전 최종 실행 계약인 feature package를 작성한다.

### Reads

- `input.packet.yaml`
- optional `product-charter.md`
- optional `system-blueprint.md`
- current source truth

### Writes

- feature package file set
- `handoff.packet.yaml`

### Done When

- package file set이 구조적으로 완전하다
- requirement / task / eval linkage가 닫혔다
- boundary와 failure mode가 `design.md`에 설명된다

### HILT

아래면 사람 확인이 필요하다.

- destructive / privileged / external behavior가 포함될 때
- verification ownership이 불명확할 때
- approval posture가 high-risk인데 빠져 있을 때

## Workflow 4. Readiness And Handoff

### Job

feature package가 바로 구현 가능한지 판정하고 다음 단계 handoff를 만든다.

### Reads

- feature package file set

### Writes

- `readiness-report.md`
- `handoff.packet.yaml`

### Done When

- 결과가 `ready | patch-required | hold` 중 하나로 판정됐다
- missing item이 파일 단위로 기록됐다
- 다음 단계가 명확해졌다

### HILT

아래면 사람 확인이 필요하다.

- `hold`
- high-risk 작업인데 승인 posture가 비어 있을 때
- package와 현재 reality가 직접 충돌할 때

## Default Paths

### Direct Path

```text
raw input
-> intake-and-routing
-> feature-package-authoring
-> readiness-and-handoff
```

### Framing Path

```text
raw input
-> intake-and-routing
-> framing
-> feature-package-authoring
-> readiness-and-handoff
```

## Validation Surface

각 workflow는 가능하면 아래 검사 중 하나 이상으로 닫는다.

- input packet validator
- route decision validator
- framing docs validator
- feature package validator
- handoff packet validator

validator가 없다면 최소한 그 부재를 명시하고 sample run에서 수동 확인해야 한다.

## Skill Position

skill은 workflow 자체가 아니다.
skill은 workflow 안에서 반복되는 작업을 수행하는 도구다.

예를 들어 한 workflow 안에서 아래 같은 도구를 쓸 수 있다.

- 입력 정규화 도구
- route 판정 도구
- framing 문서 작성 도구
- feature package 작성 도구
- readiness 판정 도구

좋은 구조는 skill 이름을 외우는 구조가 아니다.
어느 workflow를 수행 중인지 먼저 보이고, skill은 그 안에서 보조로 쓰이는 구조다.

## Final Rule

workflow는 너무 작게 쪼개지지 않아야 한다.
각 workflow는 하나의 일과 작업이 되어야 하고, 다음 workflow가 읽을 결과 파일을 남겨야 한다.
