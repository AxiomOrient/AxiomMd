# Owner Contracts Summary

## Purpose

이 문서는 skill runtime이 기억해야 하는
최소 ownership map을 고정한다.

이 문서는 owner repo 정본을 대체하지 않는다.
다만 skill이 잘못된 저장소에 의미를 덧씌우지 않도록
경계를 짧고 강하게 유지한다.

## Ownership Split

### `AxiomMd` (generic kernel)

소유:

- generic methodology
- generic workflow stages
- generic workflow artifact classes
- generic handoff packet contract
- generic package standard
- generic readiness gate
- generic output profile interface
- generic templates
- generic workflow validator entrypoint
- production 스킬 번들 (`agent/skills/`)
- 스킬 runtime reference 문서

소유하지 않음:

- product-specific package shape
- product truth
- product local profile implementation
- product runtime semantics

### Product Repo (profile owner)

When a profile is active, the product repo owns:

- product truth
- product-specific package shape extensions
- product local output profile
- product readiness meaning extensions
- product slice meaning extensions
- product execution / evidence / reconcile outcome semantics

소유하지 않음:

- generic workflow truth
- generic packet / handoff contract
- skill bundle behavior

## Decision Rule

충돌 시 우선순위는 아래다.

1. `AxiomMd`
   - generic workflow, artifact, handoff, package-standard 문제
   - skill bundle, local summary, checklist 문제
2. Product profile repo
   - product package, local profile, readiness, run-outcome 문제

## Workflow Boundary

### Authoring path

- input normalization
- route decision
- framing docs
- bounded package authoring
- readiness review

### Closed-loop path

- manual contract compile
- run evidence normalization
- reconcile review

여기부터는 selected slice를 bounded execution unit으로 다룬다.

## Source-Changing vs Review-Only

source-changing skill:

- `feature-package-author`

review-only skill:

- `package-readiness-review`
- `manual-contract-compiler`
- `run-evidence-normalizer`
- `reconcile-review`

원칙:

- review-only skill은 source package를 조용히 수정하지 않는다
- repair가 필요하면 별도 source-changing pass로 넘긴다

## Stage-to-Handoff Rule

각 skill이 쓰는 `handoff.packet.yaml` stage는 아래를 따른다.

- `charter-blueprint-author` -> `framing`
- `feature-package-author` -> `feature-package-authoring`
- `package-readiness-review` -> `readiness-and-handoff`
- `manual-contract-compiler` -> `execution-planning`
- `run-evidence-normalizer` -> `execution-and-evidence`
- `reconcile-review` -> `reconcile-and-close`

stage를 섞으면 workflow trace가 흐려진다.

## Slice Rule

closed-loop path의 기본 단위는 package 전체가 아니라 **selected slice 하나**다.

따라서 후반부 skill은 반드시 아래를 보존해야 한다.

- `feature_id` (or `id`)
- `package_ref`
- `slice_id`
- `req_ids`
- `task_ids`
- `eval_ids`

## Input Gap Rule

필수 사실이 없으면 추측하지 않는다.

- 짧은 `INPUT_GAP_REPORT`를 반환한다
- 어떤 owner fact가 비어 있는지 적는다
- partial truth를 정식 산출물로 쓰지 않는다

## Final Rule

이 문서를 포함한 모든 local summary는
owner repo 정본이 바뀌면 갱신돼야 한다.

이 문서는 convenience layer다.
truth layer가 아니다.
