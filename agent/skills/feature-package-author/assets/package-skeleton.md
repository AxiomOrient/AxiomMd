# Package Skeleton

아래 skeleton은 **shape guide**다. 실제 산출물은 각 파일로 나뉘어 저장해야 한다.
current AxiomSpecs package examples를 따르되, owner repo evidence가 더 강하면 그 evidence를 우선한다.

## intent.md

```md
# Intent

## Original ask
- ...

## Why this feature exists
- ...

## In scope
- ...

## Out of scope
- ...

## Current reality
- ...

## Examples / non-examples
- Example: ...
- Non-example: ...

## Open questions
- ...

## Source refs
- path: ...
  reason: ...
```

## package.yaml

```yaml
feature_id: FEAT-xxxx
slug: short-slug
title: ""
state: draft
review_mode: human_required
profile_key: axiom-v1
planes:
  - source
implementation_order: 0
owner_roles:
  - product
target_repos:
  - AxiomSpecs
adoption:
  generic-methodology: direct-use
current_progress: package draft created
next_step: fill requirements/tasks/evals linkage
blockers: none
```

`package.yaml`은 package truth의 진행 상태를 남기는 metadata surface다.
review result를 직접 쓰라는 뜻은 아니고, current progress / next step / blockers를 유지하라는 뜻이다.

## requirements.yaml

```yaml
requirements:
  - id: REQ-xxxx
    priority: must
    title: ""
    statement: >
      ...
    acceptance:
      - ...
```

## invariants.yaml

```yaml
invariants:
  - id: INV-xxxx
    title: ""
    statement: >
      ...
```

## design.md

```md
# Design

## 1. Boundary
### In scope
- ...

### Out of scope
- ...

## 2. Core entities / data / state
- ...

## 3. Interfaces
- upstream input: ...
- downstream consumer: ...

## 4. Workflows
- ...

## 5. Failure modes
- ...

## 6. Requirement mapping
- `REQ-xxxx` -> ...
```

## tasks.md

```yaml
tasks:
  - id: TASK-xxxx
    title: ""
    status: todo
    req_ids:
      - REQ-xxxx
    eval_ids:
      - EVAL-xxxx
    touched_paths:
      - specs/features/FEAT-xxxx-short-slug/...
    next: ...
```

## evals.yaml

```yaml
evals:
  - id: EVAL-xxxx
    title: ""
    kind: blocking
    method: manual-spec-review
    req_ids:
      - REQ-xxxx
    task_ids:
      - TASK-xxxx
    procedure:
      - ...
    pass_condition: >
      ...
```

## risks.yaml

```yaml
risks:
  - id: RISK-xxxx
    title: ""
    severity: medium
    mitigation: >
      ...
```

## decisions.jsonl

```jsonl
{"id":"DEC-xxxx","ts":"YYYY-MM-DD","summary":"Package initialized from normalized input packet.","reason":"Start bounded feature package authoring."}
```

## contracts/

```text
specs/features/FEAT-xxxx-short-slug/contracts/
```

빈 directory라도 남겨 current AxiomSpecs package shape를 맞춘다.
새 schema/example이 아직 없더라도, directory presence는 유지한다.
