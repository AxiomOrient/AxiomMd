# Spec Package Standard

## 목적

사람과 AI 에이전트가 같은 feature package를 읽고, 같은 방식으로 계획과 구현을 이어갈 수 있도록 최소 표준을 고정한다.
이 문서는 특정 제품이 아닌 generic standard다.

feature package는 보통 아래 흐름 안에서 만들어진다.

```text
input.packet.yaml
-> route.decision.yaml
-> optional product-charter.md + system-blueprint.md
-> feature package
-> readiness-report.md
```

즉 feature package는 단독 문서가 아니라 authoring workflow의 핵심 산출물이다.

## 표준 구조

```text
specs/features/FEAT-xxxx-slug/
  intent.md
  package.yaml
  requirements.yaml
  invariants.yaml
  design.md
  tasks.md
  evals.yaml
  risks.yaml
  decisions.jsonl
  slices.yaml
  contracts/
```

## 파일 책임

### `intent.md`

- 사람의 원래 말
- 예시 / 비예시
- brownfield 배경
- 열린 질문

이 파일은 의미 보존용이다.
canonical truth는 아니다.

### `package.yaml`

- feature 메타데이터
- profile key
- feature / readiness metadata
- profile-specific ownership 및 approval 정책은 output profile에서 확장
- `profile_key`는 필수다
- generic template는 `profile_key` 값을 결정하지 않는다
- 실제 값은 product repo output profile이 결정한다
- generic package standard는 공통 필드만 강제하고 local overlay는 product repo가 정의한다

이 파일은 package의 관리 메타데이터다.

### `requirements.yaml`

- 기능 요구사항
- non-goals
- acceptance 기준

이 파일이 기능 동작의 canonical contract다.

### `invariants.yaml`

- 절대 깨지면 안 되는 규칙
- 보안, 순서, 유일성, 권한, 상태 불변성

### `design.md`

- 경계
- 데이터 / 상태 모델
- 인터페이스
- 실패 모드
- 대안과 배제 이유

### `tasks.md`

- task 분해
- 진행 상태
- 열린 질문
- 다음 step

### `evals.yaml`

- task와 requirement를 닫는 검증 계약
- coverage 정책
- blocking / hard eval
- eval intent owner
- eval intent change approval posture

### `risks.yaml`

- 위험 분류
- review posture
- mitigation

### `decisions.jsonl`

- append-only 의사결정 기록
- 구현 중 생긴 중요한 판단
- drift와 reconcile 결과

### `slices.yaml`

- execution-oriented feature package는 `slices.yaml`을 포함해야 한다.
- launchable slice를 묶어서 실행 단위로 나눠 둔다.
- minimum fields:
  - `slice_id`
  - `feature_id`
  - `path_scope`
  - `req_ids`
  - `task_ids`
  - `eval_ids`
  - `done_conditions`
  - `verification_checks`
  - `approval_mode`
- slice는 package보다 좁고, 리뷰 가능한 범위여야 하며, verification 경로를 가져야 한다.

- 패키지 전체보다 slice를 기본 execution unit으로 다루는 편이 낫다.

### `contracts/`

- OpenAPI
- JSON Schema
- 상태 전이 부록
- 외부 인터페이스 메모

## stable ID 규칙

- feature: `FEAT-xxxx`
- requirement: `REQ-xxxx`
- invariant: `INV-xxxx`
- task: `TASK-xxxx`
- eval: `EVAL-xxxx`
- decision: `DEC-xxxx`
- risk: `RISK-xxxx`

규칙:

- prose만 수정했다고 ID를 바꾸지 않는다.
- revision이 바뀌어도 semantic continuity가 있으면 ID를 유지한다.
- task와 eval이 없으면 requirement는 실행 준비가 되지 않은 상태다.

## 최소 launch 준비 조건

아래가 모두 있어야 비사소한 실행을 열 수 있다.

- `package.yaml`
- `requirements.yaml`
- `design.md`
- `tasks.md`
- `evals.yaml`
- profile_key 기반 output profile에서 approval / owner 규칙을 충족
- 최소 1개 이상의 `REQ-*`
- 모든 `TASK-*`에 `REQ-*`와 `EVAL-*`가 연결됨

그리고 package authoring workflow 바깥에는 아래가 같이 있어야 한다.

- `input.packet.yaml`
- `route.decision.yaml`
- 필요하면 `product-charter.md`
- 필요하면 `system-blueprint.md`
- launch 직전에는 `readiness-report.md`
- 가능하면 feature package validator를 통과한 상태

## authoring 규칙

- 하나의 feature package는 하나의 bounded feature만 다룬다.
- 서로 unrelated한 기능을 한 package에 넣지 않는다.
- brownfield 변경이면 `intent.md`나 `design.md`에 current reality를 적는다.
- 모호한 사항은 requirement로 꾸미지 말고 open question으로 남긴다.
- review mode가 `human_required`면 승인 없이 구현 완료로 닫지 않는다.

## 검증 규칙

- 모든 `must` requirement는 최소 1개의 blocking eval을 가져야 한다.
- release-critical invariant는 hard eval 또는 deterministic proof가 있어야 한다.
- task는 touched paths와 validation을 가져야 한다.

## Reference Validation Surface

generic package는 가능하면 아래 검사를 통과해야 한다.

- file set check
- requirement / task / eval linkage check
- design section check
- handoff packet check

validator가 있다면 문서보다 먼저 validator를 통과해야 한다.

이 저장소의 base validator 예시는 아래다.

- `python scripts/workflow_check.py package <feature-package-dir>`

제품 저장소는 이 base 검사 위에 local overlay 검사를 더할 수 있다.
하지만 generic base와 local overlay를 한 덩어리 진실로 섞지 않는 편이 좋다.

## handoff 규칙

package authoring과 review는 긴 중단을 버텨야 한다.
그래서 작업 중 멈출 때마다 아래가 file state에 남아 있어야 한다.

- 현재 progress
- 열려 있는 질문
- 마지막 결정
- 다음 step
- 필요하면 `handoff.packet.yaml`

`handoff.packet.yaml`의 `stage`는 workflow 이름을 써야 한다.
예:

- `framing`
- `feature-package-authoring`
- `readiness-and-handoff`

## 권장 흐름

```text
input.packet.yaml + route.decision.yaml
-> optional product-charter.md + system-blueprint.md
-> intent.md
-> package.yaml + requirements.yaml + invariants.yaml + risks.yaml
-> design.md
-> tasks.md
-> evals.yaml
-> readiness-report.md
-> execution
-> decisions.jsonl
```

## Field Naming Rule

artifact field 이름은 한 번 정했으면 쉽게 바꾸지 않는다.
route decision, handoff packet 같은 공통 artifact에서 field 이름이 흔들리면
workflow와 skill bundle이 바로 drift 난다.
