# Workflow Definitions

`method/`의 규칙을 실행 가능한 순서로 바인딩한 선언형 실행 정의.

| 위치 | 역할 |
| --- | --- |
| `agent/policy/` | 실행 규칙 (ownership, escalation, eval, execution) |
| `agent/workflows/` | workflow / pipeline 선언 |
| `agent/skills/` | 개별 skill 계약 및 템플릿 |
| `agent/workflows/schemas/` | workflow / pipeline 스키마 + 조건식 문법 |

## Workflow Definition Schema (권장)

workflow 파일은 최소 아래 키를 가져야 한다.

```yaml
id: <slug>
layer: authoring | execution
description: |
  작업 정의

inputs:
  - <input artifact keys>

skills:
  - id: <skill-id>
    reads: [<artifact-or-path>]
    writes: [<artifact-or-path>]
  - id: <skill-id>
    reads: [...]
    writes: [...]

outputs:
  - <artifact-or-path>

acceptance:
  - "<human-readable acceptance check>"

policies:
  - policy/<POLICY_FILE.md>
```

추가 키 `condition`은 pipeline stage에서 조건 실행용으로만 사용한다.

```yaml
stages:
  - workflow: <path-without-extension>
    condition: "<expression>" # optional, truthy면 실행
```

조건식은 실행 런타임에서 문자열로 해석되는 단순 boolean 표현으로 두고, 구현체가 지원하는 형태(예: `route.decision.yaml.route == "framing-first"`)를 권장한다.

## File Responsibilities

- `authoring/*.yaml`: spec authoring 계약 단계를 묶는다.
- `execution/*.yaml`: compile/evidence/reconcile 실행 단계.
- `pipelines/*.yaml`: 여러 workflow를 ordered chain으로 묶는다.

## Path Convention

workflow YAML 파일 안의 모든 경로는 **`agent/`를 기준으로 한 상대 경로**다.

- `policy/ROLE_POLICY.md` → `agent/policy/ROLE_POLICY.md`
- `skills/intake-normalizer` → `agent/skills/intake-normalizer/`

런타임 오케스트레이터는 `agent/`를 작업 루트로 사용한다.
다른 기준점이 필요하면 workflow 파일에 `base:` 필드로 명시한다.

## Notes

- method는 왜/무엇을 설명하고, workflow는 언제/어떤 순서로 실행할지 결정한다.
- 새 workflow를 추가할 때는 `method/artifact-and-contract.md`의 artifact contract를 먼저 확인한다.
