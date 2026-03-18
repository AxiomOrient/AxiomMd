# Authoring Workflows

## Purpose

이 문서는 초기 요청에서 구현-ready feature package까지 가는 기본 workflow 세트를 정의한다.

## Why This Exists

한 번에 큰 spec 하나를 쓰려고 하면 아래 문제가 생긴다.

- 범위 판단이 문서 안에 섞인다
- 제품 수준 framing이 필요한지 늦게 알게 된다
- feature package가 너무 크거나 모호해진다
- readiness 검토가 작성 단계와 섞여 기준이 흐려진다

그래서 workflow는 **큰 작업 단위 네 개**로 나눈다.

## Document Levels

아래 순서로 문서를 만든다. 항상 모든 레벨이 필요하지는 않다.

### Level 0. Raw Input

예:

- 클라이언트 요청
- 기획서
- 회의 메모
- PRD
- 운영 이슈 설명

이 단계는 source material이다. 바로 실행 계약으로 쓰지 않는다.

### Level 1. Input Packet

항상 먼저 만든다.

- 형식: `templates/input.packet.yaml`
- 목적: 초기 입력을 agent와 사람이 같이 읽을 수 있는 최소 형식으로 정리

이 문서가 없으면 다음 단계가 입력을 제각각 해석하게 된다.

### Level 2. Route Decision

항상 intake workflow 안에서 같이 만든다.

- 목적: 바로 package로 갈지, framing을 먼저 할지 고정

### Level 3. Product Framing Docs

아래 둘은 필요할 때만 만든다.

**Product Charter** — 언제 필요한가:

- 요청이 제품 전체 방향을 바꾼다
- 무엇을 만들지보다 왜 만드는지가 더 불명확하다
- 범위 밖과 비목표가 아직 흐리다

**System Blueprint** — 언제 필요한가:

- 한 feature가 아니라 여러 영역을 같이 건드린다
- 경계, 역할, plane, major component가 아직 모호하다
- 어느 feature package로 쪼갤지 결정이 안 된다

### Level 4. Feature Package

실제로 구현을 열기 전 반드시 필요하다.

최소 파일:

- `intent.md`
- `package.yaml`
- `requirements.yaml`
- `invariants.yaml`
- `design.md`
- `tasks.md`
- `evals.yaml`
- `risks.yaml`
- `decisions.jsonl`
- `slices.yaml`

### Level 5. Readiness Review

구현 전에 반드시 필요하다.

- 기준: `method/package-readiness-gate.md`
- 결과: `ready | patch-required | hold`

## Routing Rule

처음 입력을 받으면 먼저 이 질문을 본다.

### Case A. 바로 feature package로 갈 수 있는 경우

아래가 이미 보이면 바로 feature package로 간다.

- 문제 범위가 좁다
- in-scope / out-of-scope가 보인다
- 성공 조건이 보인다
- 관련 repo/path/contract 범위가 대략 보인다

```text
raw input
-> intake-and-routing
-> feature-package-authoring
-> readiness-and-handoff
```

### Case B. Product framing이 먼저 필요한 경우

아래 중 하나라도 해당하면 먼저 charter/blueprint가 필요하다.

- 요청이 너무 넓다
- 한 번에 여러 기능을 섞고 있다
- 시스템 경계가 불분명하다
- 무엇이 이번 범위 밖인지 모른다
- feature 분해가 아직 안 된다

```text
raw input
-> intake-and-routing
-> framing
-> feature-package-authoring
-> readiness-and-handoff
```

## Minimum Information That Must Be Recoverable

에이전트는 raw input에서 아래를 읽어낼 수 있어야 한다.

- 무엇을 만들고 싶은가
- 이번 범위 안은 무엇인가
- 이번 범위 밖은 무엇인가
- 제약 조건은 무엇인가
- 완료 기준은 무엇인가
- 참고 근거는 무엇인가

이 정보가 부족하면 에이전트는 추측하지 말고
입력 부족 보고를 남기고 멈춘다.

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

## Generic Authoring Quality Bar

좋은 package는 아래를 만족해야 한다.

- 요구사항이 구체적이다
- 비목표가 명확하다
- 구현 경계가 분리돼 있다
- 모든 must requirement에 검증 경로가 있다
- task가 requirement와 연결된다
- launchable slice가 최소 하나 존재한다
- 다음 workflow가 읽을 handoff가 남는다

## Product-Specific Output Profiles

feature package의 generic 뼈대는 공통이다.
하지만 package metadata나 local rules는 제품마다 다를 수 있다.

이 경우:

- generic kernel은 공통 artifact와 최소 필드를 검사한다
- product repo는 자기 output profile을 선언한다
- authoring skill은 해당 profile을 resolve해서 local shape를 채운다

## Stop Rule

아래 중 하나면 authoring을 멈춘다.

- scope in / out이 분명하지 않다
- 완료 기준이 없다
- 제약이 충돌한다
- 근거 자료가 전혀 없다
- broad request인데 framing을 생략하려 한다

멈출 때도 이유와 다음 단계는 파일로 남겨야 한다.

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
workflow보다 앞에 오면 안 된다.

좋은 구조는 skill 이름을 외우는 구조가 아니다.
어느 workflow를 수행 중인지 먼저 보이고, skill은 그 안에서 보조로 쓰이는 구조다.

## Final Rule

좋은 authoring은 한 번에 긴 문서를 쓰는 것이 아니다.
workflow는 너무 작게 쪼개지지 않아야 한다.
각 workflow는 하나의 일과 작업이 되어야 하고,
다음 workflow가 읽을 결과 파일을 남겨야 한다.
