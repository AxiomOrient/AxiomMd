# Operational Control Workflow

## Purpose

이 문서는 spec-contract 레이어 아래, 실행/운영 단계에서 필요한 정책-가시성-복구 규칙을 정의한다.

- workflow가 정지되거나 실패해도 `resume`이 보장되는 실행 규칙을 제공한다.
- `stage`, `blocker`, `next_step`를 일관되게 운영자에게 노출한다.
- 상태를 사람 기준 판단으로만 두지 않고, 캐시/아티팩트/증거로 재현 가능하게 한다.
- 운영 정책(timeout, retry, 승인 조건)을 반복 가능한 방식으로 기록한다.

## Positioning

AxiomMd의 contract-layer workflow는 artifact 정합성을 정의한다.
이 레이어는 그 다음 수준인 **운영 제어 레이어**다.

- Contract workflow의 종료: `handoff.packet.yaml` 또는 feature package
- 운영 제어 시작: 동일 context의 실행 계획/실행/재개

운영 레이어는 authoring 레이어의 "무엇을 만들지"를 바꾸지 않는다.
"어떻게 안정적으로 수행할지"를 정한다.

## Trigger

아래 조건일 때 본 워크플로우가 개시된다.

- `execution.plan.yaml`이 승인됨
- 기존 진행 상태를 재개할 필요가 있음
- 실행 중단/재개/재시도가 요구됨
- 검사 실패/중단에서 사람이 이어서 판단해야 할 필요가 있을 때

## Scope

이 워크플로우는 기술 설계가 아니라 **실행을 안정적으로 돌리는 운영 절차**에 집중한다.

- 실행 준비 단계별 통제
- 상태 공개 (관측성)
- 중단/재개 정책
- 실패 처리 및 재시작
- 정책 변경의 감사성 확보

## Inputs / Outputs

### Inputs

- `execution.plan.yaml`
- 이전 `handoff.packet.yaml`
- 선택: `package.yaml`, `slices.yaml`

### Outputs

- 실행 중 상태 아티팩트 (implementation-specific path로 분리)
- `handoff.packet.yaml`
- `evidence.result.json`
- `reconcile.result.yaml`
- 파일 기반 checkpoint cache 상태 (기본: run-id namespace)

## Minimal State Machine

아래는 운영 레이어의 최소 상태다.

1. `planned` — 계획 수락됨. 실행 조건 (approval, input refs, budgets) 확인
2. `running` — 명령/스킬 실행 중. stage/blocker가 노출돼야 함
3. `blocked` — HILT 조건 또는 필수 승인 실패. 다음 액션이 파일에 남아 있어야 함
4. `failed` — 실패 근거, evidence path, 복구 지시 남김
5. `succeeded` — 다음 reconcile 단계로 이동
6. `resumed` — 이전 실행 상태에서 복원되어 running으로 전환

## Control Policies

구현 스택에 종속되지 않는 형태로 정의한다.

- **Execution timeout** — 단계별 timeout을 지정하고 초과 시 blocked/fail 구분
- **Retry** — idempotent step만 재시도 허용
- **Failure** — 실패는 근거 포함 (파일/command/log path)
- **Approval** — high-risk action은 explicit 승인 필요
- **Budget** — 토큰/시간/디스크/출력량 제한
- **Cache** — 기본 namespace는 `run-id`

## Checkpoint and Resume Rule

기본 checkpoint namespace는 `run-id`다.

- 상태 복원은 동일 run-id에 대해 deterministic하게 수행된다.
- `feature-id`는 집계/지표 레이블로 보조 사용한다.
- resume는 run-id 명시 또는 최근 성공 상태 조회 후 수동 확정으로 동작한다.
- 병렬 실행 시 feature-id를 기본 키로 쓰면 충돌 및 디버깅 난이도가 증가한다.

## Observability Rules

운영자는 아래를 항상 볼 수 있어야 한다.

- 현재 stage / status / next_step
- blockers 및 open questions
- 마지막 실패 이유
- 증거 파일 경로 (evidence_refs)
- 변경/생성 경로 (changed_paths / produced_paths)

## Quality Gates

각 단계는 파일 기반 증거를 남겨야 한다.

- 상태 전이 시 `handoff.packet.yaml` 또는 plan 상태 로그 생성
- 장애 발생 시 evidence path와 재실행 지시를 남김
- restart 시 이전 run-id 상태에서 동일 경로를 재해석 가능한지 점검

## Runbook

- `planned`에서 입력 검증 실패 → 즉시 `blocked` 기록, `open_questions` 남김
- `running`에서 하위 스킬 실패 → `failed` 기록, cache flush 전략 명시
- resume 요청 → `planned`와 `running` 증거를 비교 후 `resumed`로 전환
- 재시작 후 완료 조건 체크 → 증거 포함으로 `succeeded` 종료

## Relation to Existing Workflows

이 레이어는 아래 workflow와 연결된다.

- authoring path: `intake-and-routing`, `framing`, `feature-package-authoring`, `readiness-and-handoff`
- `execution-and-evidence`
- `reconcile-and-close`
