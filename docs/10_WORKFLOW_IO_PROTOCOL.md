# Workflow I/O Protocol

## Purpose

이 문서는 workflow가 어떤 파일을 입력으로 받고 어떤 파일을 출력으로 남겨야 하는지 고정한다.

## Why This Exists

오해는 대부분 아래 셋에서 생긴다.

- 초기 입력이 제각각이다
- 중간 판단 결과가 파일로 남지 않는다
- 다음 단계가 무엇을 읽어야 하는지 불분명하다

그래서 공통 protocol은 **workflow 단위 입력/출력 파일**을 먼저 고정한다.

## Core Rule

각 workflow는 아래 조건을 만족해야 한다.

1. 시작 입력이 file-state로 존재한다
2. 끝나면 다음 workflow가 읽을 file-state를 남긴다
3. 채팅 설명은 보조다. protocol은 파일이다

## Standard Workflow Artifacts

공통 workflow artifact는 아래 일곱 가지다.

1. `input.packet.yaml`
2. `route.decision.yaml`
3. `product-charter.md`
4. `system-blueprint.md`
5. feature package file set
6. `readiness-report.md`
7. `handoff.packet.yaml`

항상 모든 artifact가 필요한 것은 아니다.
하지만 workflow를 건너뛸 때도 왜 건너뛰는지는 파일로 남아야 한다.

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

### feature package

구현 전 최종 실행 계약이다.

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

## Official Workflow Set

공통 workflow는 아래 네 개를 기본으로 한다.

| Workflow | Required Input | Required Output |
| --- | --- | --- |
| intake-and-routing | raw input | `input.packet.yaml`, `route.decision.yaml` |
| framing | `input.packet.yaml`, `route.decision.yaml` | `product-charter.md`, `system-blueprint.md`, `handoff.packet.yaml` |
| feature-package-authoring | `input.packet.yaml` + optional framing docs | feature package file set, `handoff.packet.yaml` |
| readiness-and-handoff | feature package file set | `readiness-report.md`, `handoff.packet.yaml` |

이 네 workflow는 spec 문서를 만들기 위한 authoring path다.
그 이후 execution, verification, reconcile은 별도 closed loop에서 이어진다.

## Read / Write Rule

모든 workflow 또는 skill은 아래를 명시해야 한다.

- read paths
- write paths
- output target
- stop condition

모든 문서를 다 읽게 두면 엔트로피가 늘어난다.
반대로 read path와 write path를 고정하면 오해가 줄어든다.

## Folder Rule

공통 규칙은 아래만 고정한다.

- artifact는 정해진 파일 형식을 가진다
- 각 저장소는 자기 문서 구조를 가진다
- workflow와 skill은 정해진 read/write path만 사용한다

어느 저장소에 어떤 실제 경로가 있는지는 각 저장소가 정한다.
하지만 artifact 형식과 workflow 입출력 규칙은 공통이어야 한다.

## Reference Validators

기본 artifact는 가능하면 기계 검사도 같이 가져야 한다.

- `scripts/check_input_packet.rb`
- `scripts/check_route_decision.rb`
- `scripts/check_framing_docs.rb`
- `scripts/check_feature_package.rb`
- `scripts/check_handoff_packet.rb`

## Sample Run Rule

workflow contract를 바꿨으면 샘플 입력으로 아래를 끝까지 한 번 돌린다.

```text
raw input
-> intake-and-routing
-> framing if needed
-> feature-package-authoring
-> readiness-and-handoff
```

이 sample run은 아래를 확인해야 한다.

- artifact field 이름이 실제로 충분한가
- heading이나 section 이름이 validator와 맞는가
- handoff stage가 workflow-first 구조와 맞는가
- skill bundle이 local summary drift 없이 따라오는가

## Final Rule

좋은 workflow는 말을 잘하는 workflow가 아니다.
중간 판단과 다음 입력이 파일로 고정돼 있어서 다른 사람이나 다른 agent가 같은 방식으로 이어받을 수 있는 workflow다.
