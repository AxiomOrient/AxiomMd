# AxiomMd

workflow / skill 기반 spec 생성의 generic kernel 저장소.

## Skills

`agent/skills/`에 9개 production 스킬이 있다. 레포에서 직접 실행하지 않고 설치 후 사용한다.

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

## Structure

| 경로 | 역할 |
| --- | --- |
| `method/` | 불변 방법론 문서 |
| `agent/skills/` | production 스킬 번들 |
| `agent/policy/` | 실행 정책 (ownership, role, eval, escalation, execution) |
| `agent/workflows/` | 선언형 workflow / pipeline 정의 |
| `templates/**` | package / work item 시작 템플릿 |
| `scripts/workflow_check.py` | artifact contract 검증 |
| `scripts/workflow_runner.py` | workflow / pipeline 정합성 검증 |

## Method

| 문서 | 답하는 질문 |
| --- | --- |
| `method/method-foundation.md` | 이 방법론이 무엇이고 어떤 원칙으로 움직이는가 |
| `method/authoring-workflows.md` | 입력에서 spec으로 어떤 workflow를 거치는가 |
| `method/closed-loop.md` | 표준 실행 루프는 어떻게 닫히는가 |
| `method/artifact-and-contract.md` | artifact contract, readiness gate, skill system |
| `method/operational-policy-workflow.md` | 실행 중단 / 재개 / 운영 제어 |
| `method/governance.md` | 저장소 경계, 문서 운영, 품질 시스템 |

추가 기준은 `method/governance.md` 참고.

## Boundary

- generic하면 여기에 둔다
- product-specific이면 여기 두지 않는다
- 실제 product-specific output profile은 각 product repo에 둔다

Admission Rule: 제품명을 지워도 의미가 남고, 두 개 이상 제품에서 재사용 가능해야 한다.

## Validators

```
python scripts/workflow_check.py packet
python scripts/workflow_check.py route
python scripts/workflow_check.py package <feature-dir>
python scripts/workflow_check.py ensure-layer <package-dir>
python scripts/workflow_check.py handoff <path/to/handoff.packet.yaml>
python scripts/workflow_check.py pipeline <workflow-root>

python scripts/workflow_runner.py validate workflow <workflow.yaml>
python scripts/workflow_runner.py validate pipeline <pipeline.yaml>
python scripts/workflow_runner.py simulate pipeline <pipeline.yaml> --strict
```
