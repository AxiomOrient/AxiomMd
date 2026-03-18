# AxiomMd

AxiomMd는 workflow / skill 기반 spec 생성 프로그램의 generic kernel 저장소다.

## Skills

`agent/skills/`에 9개 production 스킬 번들이 있다.

스킬은 레포에서 직접 실행하지 않는다. `~/.codex/skills/.system/skill-installer`로 설치한 후 사용한다.

| 스킬 | 역할 |
| --- | --- |
| `intake-normalizer` | 클라이언트 입력 → input.packet.yaml |
| `scope-router` | input.packet → route.decision.yaml |
| `charter-blueprint-author` | 광범위한 요청 → product-level framing 문서 |
| `feature-package-author` | 정규화된 입력 → feature package |
| `package-readiness-review` | feature package readiness 검토 |
| `manual-contract-compiler` | 승인된 slice → execution contract |
| `run-evidence-normalizer` | 실행 결과 → evidence bundle |
| `reconcile-review` | evidence → reconcile 결정 |
| `spec-writing-standard` | AI-facing spec 작성 / 업그레이드 |

스킬 runtime ownership 요약은 각 스킬의 `references/`에 있다.

## Role

AxiomMd가 소유하는 것은 아래다.

- 방법론 문서
- closed-loop 운영 규칙
- harness / quality / failure loop 규칙
- generic package standard
- generic readiness gate
- generic skill design primitive
- generic workflow input / output protocol
- generic output profile interface
- generic template
- generic validator script
- 문서 승격 / 정리 / 경계 유지 규칙
- production 스킬 번들 (agent/skills/)
- 스킬 runtime reference 문서 (각 스킬의 `references/`)

AxiomMd가 소유하지 않는 것은 아래다.

- 특정 제품의 blueprint
- 특정 제품 architecture
- 특정 제품 feature package
- 특정 제품 backlog / plan / evidence
- 특정 구현 저장소의 runtime 상세
- product-specific output profile implementation

## Boundary

핵심 원칙은 단순하다.

- generic하면 여기에 둔다
- product-specific이면 여기 두지 않는다
- crate / API / runtime 세부사항이면 여기 두지 않는다
- generic output artifact와 output profile interface는 여기 둔다
- 실제 product-specific output profile은 각 product repo에 둔다

## Admission Rule

다음 질문에 모두 “예”면 AxiomMd 후보다.

1. 제품명을 지워도 의미가 남는가
2. 두 개 이상 제품에서 재사용 가능한가
3. 특정 저장소 경로 대신 generic contract로 설명 가능한가
4. 예시를 generic example로 바꿔도 손상이 없는가

하나라도 “아니오”면 이 저장소 밖에 둔다.

## Link Boundary

이 저장소 문서는 다른 저장소의 파일을 직접 가리키지 않는다.

- 절대경로 금지
- 상대경로 금지
- `pwd` 기반 경로 금지
- 다른 저장소 파일 링크 금지

필요한 내용이 있으면 링크하지 말고 여기 문서에 일반 규칙으로 다시 쓴다.

## Curation Rule

- 중복 문서는 합친다.
- generic 복제본은 삭제한다.
- 임시 메모는 durable 문서로 승격하지 않으면 삭제한다.
- archive는 외부 참조 가치나 중요한 의사결정 이력이 있을 때만 쓴다.

## Scope

- 방법론 문서
- generic spec standard
- generic templates
- generic workflow / skill / harness asset
- 두 저장소 이상에서 재사용 가능한 운영 규칙

## Out of Scope

- 특정 제품 blueprint
- 특정 제품 feature spec
- 특정 제품 runtime architecture
- 특정 제품 implementation backlog
- 특정 제품 local output profile

## Method

불변 방법론 문서. 에이전트가 임의로 추가하지 않는다 — 추가 기준은 `method/governance.md` 참고.

| 문서 | 답하는 질문 |
| --- | --- |
| `method/method-foundation.md` | 이 방법론이 무엇이고 어떤 원칙으로 움직이는가 |
| `method/authoring-workflows.md` | 클라이언트 입력에서 어떤 workflow를 거쳐 spec으로 좁혀 가는가 |
| `method/closed-loop.md` | 표준 실행 루프는 어떻게 닫히는가 |
| `method/artifact-and-contract.md` | artifact contract, readiness gate, skill system이 어떻게 정의되는가 |
| `method/governance.md` | 저장소 경계, 문서 운영, 품질 시스템을 어떻게 운영하는가 |

## Other

| 경로 | 역할 |
| --- | --- |
| `agent/skills/` | 설치 가능한 9개 production 스킬 번들 |
| `agent/policy/` | 실행 정책(ownership, role, eval, escalation, execution) |
| `agent/workflows/` | 선언형 workflow 연결(what to run, ordered pipeline) |
| `agent/workflows/schemas/` | workflow/pipeline 스키마 + 조건식 가이드 |
| `standards/spec-package-standard.md` | generic spec package 구조 표준 |
| `templates/**` | 새 package나 work item 시작 템플릿 |
| `scripts/workflow_check.py` | artifact contract 검증 진입점 |
| `scripts/workflow_runner.py` | workflow/pipeline 선언형 실행 정의 정합성 검증 진입점 |

## Current State

- 이 저장소는 generic methodology, generic package standard, generic readiness gate, generic skill design primitive, generic workflow input/output protocol을 소유한다.
- 이 저장소는 raw input부터 authoring output, execution evidence, reconcile result까지 이어지는 generic workflow artifact contract를 소유한다.
- 이 저장소는 product-specific output contract 자체를 소유하지 않는다.
- 대신 product-specific output profile을 연결하는 generic interface와 resolution rule은 이 저장소가 소유한다.
- 특정 제품의 package shape, readiness meaning, execution contract, evidence / reconcile shape는 각 product repo가 소유한다.
- 방법론의 개선은 observation을 generic asset으로 승격할 때만 이 저장소에 반영한다.
- package가 구현-ready 상태인지 검토할 때는 `method/artifact-and-contract.md`의 Package Readiness Gate를 먼저 통과해야 한다.
- workflow나 skill 세트를 바꿨으면 샘플 입력으로 authoring path와 closed loop를 최소 한 번 끝까지 통과시켜 보고 문서를 고친다.
- workflow 실행 정합성은 `scripts/workflow_runner.py`가 책임지고,
- artifact 형식 체크는 `scripts/workflow_check.py`가 담당한다.

### workflow_check 사용 예시

- `python scripts/workflow_check.py packet`
- `python scripts/workflow_check.py route`
- `python scripts/workflow_check.py framing`
- `python scripts/workflow_check.py authoring-request`
- `python scripts/workflow_check.py handoff --base-dir <workflow-root>`
- `python scripts/workflow_check.py package`
- `python scripts/workflow_check.py ensure-layer <package-dir-or-package.yaml>`
- `python scripts/workflow_check.py execution-plan`
- `python scripts/workflow_check.py evidence-result`
- `python scripts/workflow_check.py reconcile-result`
- `python scripts/workflow_check.py pipeline <workflow-root>`
- `python scripts/workflow_check.py --strict packet`
- `python scripts/workflow_check.py --json pipeline <workflow-root>`

for 에이전트 권장 워크플로우(부작용 방지):
- 1) 변경 없는 검증: `python scripts/workflow_check.py ensure-layer <package-dir-or-package.yaml>`
- 2) 확인 후 필요할 때만 반영: `python scripts/workflow_check.py ensure-layer --write --layer feature <package-dir-or-package.yaml>`

### workflow_runner 사용 예시

- `python scripts/workflow_runner.py validate workflow agent/workflows/authoring/intake-and-routing.yaml`
- `python scripts/workflow_runner.py validate pipeline agent/workflows/pipelines/authoring.yaml`
- `python scripts/workflow_runner.py validate manifests`
- `python scripts/workflow_check.py pipeline <workflow-root>`와 병행해 `runner` 결과를 `workflow_check` 결과와 함께 사용
- `python scripts/workflow_runner.py simulate pipeline agent/workflows/pipelines/full-cycle.yaml --strict`
