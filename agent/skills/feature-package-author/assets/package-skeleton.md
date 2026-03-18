# Package Skeleton

아래 skeleton은 **shape guide**다. 실제 산출물은 각 파일로 나뉘어 저장해야 한다.
Profile이 제공된 경우, profile manifest에 따라 추가 필드를 적용한다.

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

Generic minimum (no profile):

```yaml
id: <unique-identifier>
slug: short-slug
title: ""
state: draft
layer: feature
```

When a profile is active, the profile manifest defines additional required fields.
Generic fields must always be present regardless of profile.

`package.yaml`은 package truth의 진행 상태를 남기는 metadata surface다.
current progress / next step / blockers를 유지하라는 뜻이다.

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
      - <relative-path-estimate>
    done_when: ...
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

## slices.yaml

```yaml
slices:
  - id: SLICE-xxxx
    title: ""
    path_scope:
      - <relative-path>
    req_ids:
      - REQ-xxxx
    task_ids:
      - TASK-xxxx
    eval_ids:
      - EVAL-xxxx
    done_conditions:
      - ...
    approval_mode: human_required
    budget: ~
```
