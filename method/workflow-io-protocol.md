# Workflow I/O Protocol

## Purpose

이 문서는 workflow와 skill이 어떤 file-state를 입력으로 받고 어떤 file-state를
출력으로 남겨야 하는지 고정한다.

채팅 설명은 보조다.
실제 계약은 파일이다.

## Why This Exists

오해는 대부분 아래 셋에서 생긴다.

- 초기 입력이 제각각이다
- 중간 판단 결과가 파일로 남지 않는다
- 다음 단계가 무엇을 읽어야 하는지 불분명하다

그래서 공통 protocol은 workflow 단위 입력/출력 artifact를 먼저 고정한다.

## Core Rule

모든 workflow는 아래를 만족해야 한다.

1. 시작 입력이 file-state로 존재한다
2. 끝나면 다음 workflow가 읽을 file-state를 남긴다
3. 중간 판단, 보류 사유, 다음 단계가 파일로 남는다
4. product-specific shape가 필요하면 generic artifact 위에 profile을 통해 확장한다

## Artifact Classes

공통 artifact class는 아래 열 가지다.

1. `input.packet.yaml`
2. `route.decision.yaml`
3. `product-charter.md`
4. `system-blueprint.md`
5. feature package file set
6. `readiness-report.md`
7. `handoff.packet.yaml`
8. `execution.plan.yaml`
9. `evidence.result.json`
10. `reconcile.result.yaml`

모든 workflow가 모든 artifact를 다 쓰는 것은 아니다.
하지만 workflow를 건너뛰거나 중단할 때도 이유와 다음 단계는 파일로 남아야 한다.

## Artifact Rules

### `input.packet.yaml`

초기 입력을 정규화한 문서다.

최소 필드:

- `request_summary`
- `target_kind`
- `source_context_refs`
- `output_contract_refs`
- `scope.in`
- `scope.out`
- `constraints`
- `done_signals`
- `open_questions`
- `evidence_refs`

### `route.decision.yaml`

바로 feature package로 갈지, framing이 먼저 필요한지 판정한 문서다.

최소 필드:

- `input_ref`
- `route`
- `reason_summary`
- `required_artifacts`
- `next_step`
- `open_questions`
- `blockers`

### `product-charter.md`

제품 수준의 문제, 목표, 비목표를 고정한 문서다.

최소 섹션:

- problem
- users / operators
- goals
- non-goals
- success signals
- constraints

### `system-blueprint.md`

제품 수준의 큰 구조와 경계를 고정한 문서다.

최소 섹션:

- current scope
- boundary
- major components
- primary flow
- source of truth
- open questions

### feature package file set

구현 전 최종 source package다.

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

선택적 확장:

- `contracts/`
- `examples/`
- `fixtures/`

### `readiness-report.md`

package를 바로 구현해도 되는지 판정한 문서다.

최소 섹션:

- status
- gate summary
- missing items
- open questions
- next step

### `handoff.packet.yaml`

한 workflow가 끝난 뒤 다음 workflow에 넘기는 결과 packet이다.

최소 필드:

- `stage`
- `status`
- `input_ref`
- `changed_paths`
- `produced_paths`
- `evidence_refs`
- `open_questions`
- `next_step`
- `blockers`

### `execution.plan.yaml`

승인된 source package 또는 slice를 실제 실행 단위로 내리는 계획 문서다.

최소 필드:

- `package_ref`
- `slice_ref`
- `goal_ref`
- `scope_paths`
- `req_ids`
- `task_ids`
- `eval_ids`
- `approval_mode`
- `budget`
- `stop_conditions`

### `evidence.result.json`

실행 결과를 source truth와 분리된 evidence로 남기는 문서다.

최소 필드:

- `run_id`
- `package_ref`
- `slice_ref`
- `produced_artifacts`
- `verification_results`
- `logs`
- `diff_summary`
- `failure_summary`

### `reconcile.result.yaml`

evidence를 source truth에 다시 연결하고 다음 액션을 결정하는 문서다.

최소 필드:

- `stage`
- `status`
- `package_ref`
- `slice_ref`
- `evidence_refs`
- `decision_summary`
- `changed_paths`
- `next_action`
- `open_questions`
- `blockers`

## Official Workflow Set

공통 workflow는 아래 일곱 개를 기본으로 한다.

| Workflow | Required Input | Required Output |
| --- | --- | --- |
| intake-and-routing | raw input | `input.packet.yaml`, `route.decision.yaml` |
| framing | `input.packet.yaml`, `route.decision.yaml` | `product-charter.md`, `system-blueprint.md`, `handoff.packet.yaml` |
| feature-package-authoring | `input.packet.yaml` + optional framing docs | feature package file set, `handoff.packet.yaml` |
| readiness-and-handoff | feature package file set | `readiness-report.md`, `handoff.packet.yaml` |
| execution-planning | approved package or slice | `execution.plan.yaml`, `handoff.packet.yaml` |
| execution-and-evidence | `execution.plan.yaml` | `evidence.result.json`, `handoff.packet.yaml` |
| reconcile-and-close | `evidence.result.json` + source package | `reconcile.result.yaml`, `handoff.packet.yaml` |

앞의 네 workflow는 authoring path다.
뒤의 세 workflow는 closed loop path다.

이 둘을 분리해서 생각할 수는 있어도,
generic kernel 관점에서는 모두 공통 workflow set에 포함된다.

## Product Output Profile Interface

공통 artifact shape는 generic하게 유지한다.
product-specific output shape가 필요하면 각 product repo는 자기 profile을 선언한다.

공통 규칙은 아래와 같다.

- package metadata에는 `profile_key`를 둔다
- generic kernel은 `profile_key`를 보고 product profile manifest를 resolve한다
- generic artifact 필수 필드는 먼저 통과해야 한다
- product profile은 generic 필드를 제거할 수 없고, 확장만 할 수 있다

## Read / Write Rule

모든 workflow 또는 skill은 아래를 명시해야 한다.

- read paths
- write paths
- output target
- stop condition

모든 문서를 다 읽게 두면 엔트로피가 늘어난다.
read path와 write path를 고정하면 오해가 줄어든다.

## Folder Rule

공통 규칙은 아래만 고정한다.

- artifact는 정해진 파일 형식을 가진다
- 각 저장소는 자기 문서 구조를 가진다
- workflow와 skill은 정해진 artifact contract를 따른다
- 실제 저장 경로는 각 저장소가 정한다
- product-specific local path rule은 각 product repo가 정한다

## Reference Validators

기본 artifact는 가능하면 기계 검사도 같이 가져야 한다.

단일 체크 진입점:

- `scripts/workflow_check.py`

검사 대상:

- packet
- route
- framing
- authoring-request
- package
- handoff
- execution-plan
- evidence-result
- reconcile-result
- pipeline

## Sample Run Rule

workflow contract를 바꿨으면 샘플 입력으로 아래 둘을 돌린다.

```text
raw input
-> intake-and-routing
-> framing if needed
-> feature-package-authoring
-> readiness-and-handoff
```

```text
approved package or slice
-> execution-planning
-> execution-and-evidence
-> reconcile-and-close
```

이 sample run은 아래를 확인해야 한다.

- artifact field 이름이 실제로 충분한가
- heading과 section 이름이 validator와 맞는가
- handoff stage가 workflow-first 구조와 맞는가
- profile extension이 generic kernel과 충돌하지 않는가
- skill bundle이 local summary drift 없이 따라오는가

## Final Rule

좋은 workflow는 말을 잘하는 workflow가 아니다.
중간 판단과 다음 입력이 파일로 고정돼 있어서
다른 사람이나 다른 agent가 같은 방식으로 이어받을 수 있는 workflow다.
