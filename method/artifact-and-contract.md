# Artifact and Contract

## Core Contract Rule

모든 workflow와 skill에서 계약의 실체는 파일이다.
채팅 설명은 보조다.

모든 workflow는 아래를 만족해야 한다.

1. 시작 입력이 file-state로 존재한다.
2. 끝나면 다음 workflow가 읽을 file-state를 남긴다.
3. 중간 판단, 보류 사유, 다음 단계가 파일로 남는다.
4. product-specific shape가 필요하면 generic artifact 위에 profile을 통해 확장한다.

모든 workflow 또는 skill은 아래를 명시해야 한다.

- read paths
- write paths
- output target
- stop condition

## Artifact Classes

공통 artifact class는 열 가지다.

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

공통 workflow는 일곱 개다.

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

## Operational Control Layer (권고)

AxiomMd의 공식 7개 workflow는 contract와 spec 상태를 규정한다.
실행 운영 규칙(재시도/재개/상태 노출/운영 정책)은 아래의 보완 레이어로 분리한다.

- 운영 제어 레이어 문서: [operational-policy-workflow.md](operational-policy-workflow.md)

운영 제어 레이어의 특징:
- 실행 안정성: 실행 중단/재개/재시도 규칙이 파일 기반으로 남는다
- 관측성: stage, blockers, next_step, evidence_refs를 사람이 읽을 수 있게 남긴다
- 재개성: `run-id`를 기본 checkpoint namespace로 사용한다
- 계약 독립성: feature package 계약은 건드리지 않고 운영 정책만 분리

이 레이어는 implementation-space에서 실제 정책 구현(타임아웃, 경로, 캐시 엔진)을 정의하되,
구조는 generic하게 공통으로 두는 것을 목표로 한다.

## Output Profile Interface

generic workflow kernel은 product-specific output profile을 아래 방식으로 연결한다.

- generic artifact contract는 AxiomMd가 소유한다.
- product-specific output profile은 각 product repo가 소유한다.
- generic kernel은 profile resolution interface만 소유한다.

같은 workflow라도 제품마다 아래가 달라질 수 있다.

- package metadata 필드
- readiness meaning
- slice local shape
- execution contract shape
- evidence bundle shape
- reconcile record shape

이 차이를 generic kernel 안에 직접 넣으면 kernel이 product repo로 오염된다.
profile interface를 두면 kernel은 좁게 유지되고 제품별 확장은 분리된다.

### Product Profile Conditions

product-specific output profile은 아래 조건을 만족해야 한다.

1. generic required field를 제거할 수 없다.
2. generic artifact contract 위에 확장만 할 수 있다.
3. profile key와 manifest가 존재해야 한다.
4. local validator와 local examples를 가져야 한다.

### `profile_key`

package가 어떤 product profile을 따르는지 식별한다.

예: `axiom-v1`, `billing-v2`, `runtime-core-v1`

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

### Resolution Rule

generic workflow 또는 skill은 아래 순서로 동작한다.

1. generic artifact minimum contract를 검사한다.
2. `profile_key`를 읽는다.
3. 해당 product repo의 profile manifest를 resolve한다.
4. local overlay rule을 적용한다.
5. generic + local validator를 모두 통과시킨다.

### Ownership

AxiomMd가 소유: profile interface, resolution rule, generic required fields, generic validation order

product repo가 소유: 실제 profile implementation, local shape, local field meaning, local readiness rule, local execution / evidence / reconcile semantics

## Package Readiness Gate

feature package가 implementation-ready인지 아래 여섯 gate로 판정한다.

게이트 판정 결과는 `ready`, `patch-required`, `hold` 셋 중 하나다.

### Gate 0. Authoring Context Completeness

package가 아래 흐름 어디서 왔는지 file state로 보여야 한다.

- `input.packet.yaml`이 있다.
- `route.decision.yaml`이 있다.
- route가 `framing-first`면 `product-charter.md`, `system-blueprint.md`가 있다.

이 정보가 전혀 없으면 package는 restartability가 약하다. 최소 `patch-required`다.

### Gate 1. Required File Set

비사소한 feature package는 최소 아래를 가진다.

- `intent.md`, `package.yaml`, `requirements.yaml`, `invariants.yaml`, `design.md`, `tasks.md`, `evals.yaml`, `risks.yaml`, `decisions.jsonl`, `slices.yaml`

필수 파일이 빠져 있으면 `hold`다.

### Gate 2. Linkage Completeness

아래가 모두 참이어야 한다.

- 모든 `must` requirement는 최소 1개의 blocking eval을 가진다.
- 모든 requirement는 최소 1개의 task에 연결된다.
- 모든 task는 최소 1개의 `REQ-*`와 `EVAL-*`를 가진다.
- 모든 task는 touched path 또는 변경 경계를 가진다.
- 모든 eval은 `req_ids`, `task_ids`를 가진다.
- release-critical invariant는 hard eval 또는 deterministic proof와 연결된다.

하나라도 빠지면 `patch-required`다.

### Gate 3. Design Completeness

`design.md`는 최소 아래를 설명해야 한다.

- boundary, data / state model, interfaces, failure modes, out-of-scope, requirement mapping

"goal"과 "target paths"만 있고 구조 설명이 없으면 implementation-ready가 아니다.

### Gate 4. Risk And Approval Completeness

아래가 모두 명시돼야 한다.

- approval posture 및 approval 주체 (`profile_key` 기반 profile 규칙으로 해석됨)
- high-risk 작업의 launch/posture 규칙
- blocking eval intent 소유/승인 방식 (product profile에 명시됨)
- destructive / external / privileged behavior의 처리 방식
- brownfield면 current reality 또는 baseline

위험이 높은데 approval rule이 없으면 `hold`다.

### Gate 5. Handoff Completeness

긴 중단을 버티려면 아래가 file state에 남아 있어야 한다.

- 현재 progress
- 마지막 중요한 결정
- 열린 질문
- 다음 step
- blocker 또는 `none`
- 필요하면 `handoff.packet.yaml`

## Skill System

### What a Skill Is

skill은 prompt 조각이 아니다.
skill은 반복 가능한 reasoning move를 contract로 고정한 자산이다.

예: scope clarify, structure scout, plan build ready, bounded review, reconcile pass

agent는 raw reasoning을 안정적으로 재사용하지 못한다.
그래서 skill은 아래를 명시해야 한다.

- 목적, 입력, 출력, acceptance, stop condition, evidence

### Skill vs Workflow

- skill: 한 가지 reusable move
- workflow: 여러 skill을 순서와 gate로 묶은 실행 경로

skill은 workflow보다 먼저 만들지 않는다.

```text
workflow
-> artifact contract
-> gate
-> repeated move
-> skill
```

기본 단위는 workflow고, skill은 그 안의 반복 작업을 맡는다.

### Skill Design Rules

- 하나의 skill은 하나의 명확한 질문에 답해야 한다.
- source of truth를 바꾸는 skill과 review-only skill을 섞지 않는다.
- output이 다음 단계에서 바로 읽히는 형태여야 한다.
- failure를 숨기지 말고 stop condition을 노출해야 한다.
- skill은 읽는 경로와 쓰는 경로를 명시해야 한다.

### Skill I/O Rule

모든 skill은 최소 아래를 선언해야 한다.

- input packet
- output target
- read paths
- write paths
- stop condition

입력이 약하면 같은 skill도 다른 결과를 낸다.
출력이 흐리면 다음 단계가 다시 해석 비용을 낸다.
skill은 prompt보다 packet과 file contract가 먼저다.

### Skill Ownership Boundary

이 저장소는 generic skill design primitive를 소유한다.

- 입력 형식의 최소 조건
- 출력 형식이 가져야 할 일반 규칙
- stop condition
- evidence rule
- packaging checklist

제품 특화 output contract는 여기서 직접 정의하지 않는다.
skill bundle이 generic writing rule, generic template 원본, generic validator 원본, generic workflow policy를 canonical truth로 다시 선언하면 안 된다.
같은 규칙이 두 군데에 생기면 skill truth가 둘로 갈라진다.

### Skill Bundle Release Gate

installable bundle은 아래 셋이 닫혀야 release 후보가 된다.

**Gate 1. Required Bundle Set**

- `SKILL.md`
- 참조된 `assets/`, `references/`, `scripts/`
- 선택적 `agents/openai.yaml`
- install manifest entry

**Gate 2. Linkage Completeness**

- `SKILL.md`에 적힌 경로가 실제 파일과 일치한다.
- validator / command가 bundle root 기준으로 실행 가능하다.
- output / acceptance / stop condition / evidence가 명시돼 있다.
- source-changing skill이면 바꾸는 진실의 범위가 적혀 있다.
- review-only skill이면 수정 금지와 판정 출력이 적혀 있다.

**Gate 3. Handoff Completeness**

- source commit 또는 source revision
- generated version
- known limitation
- smoke test result

### Contract Drift Rule

설치형 skill bundle이 local summary를 같이 들고 있으면 drift 위험이 생긴다.

- owner contract가 바뀌면 local summary도 같이 갱신한다.
- field 이름이 바뀌면 asset, validator, reference를 같이 바꾼다.
- route / handoff 같은 핵심 artifact는 sample run으로 다시 확인한다.

### Skill Creation Process

1. raw input 종류를 정한다.
2. 큰 작업 단위 workflow를 정한다.
3. workflow 사이 artifact를 정한다.
4. HILT 지점을 정한다.
5. 반복되는 move만 skill로 뽑는다.
6. sample run으로 끝까지 검증한다.

먼저 존재해야 하는 것: `input.packet.yaml`, `route.decision.yaml`, 필요하면 framing docs, feature package contract, readiness output, handoff packet

결론:

- giant workflow 하나는 약하다.
- micro-step 나열도 약하다.
- 중간 산출물 파일이 제일 중요하다.
- validator 없는 artifact는 오래 못 간다.
- runtime fetch는 self-contained skill을 약하게 만든다.

## Reference Validators

기본 artifact는 기계 검사도 같이 가져야 한다.

단일 체크 진입점: `scripts/workflow_check.py`

검사 대상: packet, route, framing, authoring-request, package, handoff, execution-plan, evidence-result, reconcile-result, pipeline

product profile은 아래를 제공해야 한다.

- profile manifest
- local schema or checker
- example package
- failure examples if possible

generic kernel은 profile implementation을 직접 품지 않는다.
대신 profile implementation이 generic contract를 위반하지 않는지 검사한다.

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

확인 사항:

- artifact field 이름이 실제로 충분한가
- heading과 section 이름이 validator와 맞는가
- handoff stage가 workflow-first 구조와 맞는가
- profile extension이 generic kernel과 충돌하지 않는가
- skill bundle이 local summary drift 없이 따라오는가

## Folder Rule

- artifact는 정해진 파일 형식을 가진다.
- 각 저장소는 자기 문서 구조를 가진다.
- workflow와 skill은 정해진 artifact contract를 따른다.
- 실제 저장 경로는 각 저장소가 정한다.
- product-specific local path rule은 각 product repo가 정한다.
