# Spec Package Standard

## 목적

사람과 AI 에이전트가 같은 feature package를 읽고, 같은 방식으로 계획과 구현을 이어갈 수 있도록 최소 표준을 고정한다.
이 문서는 특정 제품이 아닌 generic standard다.

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
- owner 역할
- verification owner 역할
- profile key
- review mode
- state

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
- owner / review mode 정의
- verification owner 정의
- 최소 1개 이상의 `REQ-*`
- 모든 `TASK-*`에 `REQ-*`와 `EVAL-*`가 연결됨

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

## handoff 규칙

package는 긴 중단을 버텨야 한다.
그래서 작업 중 멈출 때마다 아래가 file state에 남아 있어야 한다.

- 현재 progress
- 열려 있는 질문
- 마지막 결정
- 다음 step

## 권장 흐름

```text
intent.md
-> package.yaml + requirements.yaml + invariants.yaml + risks.yaml
-> design.md
-> tasks.md
-> evals.yaml
-> execution
-> decisions.jsonl
```
