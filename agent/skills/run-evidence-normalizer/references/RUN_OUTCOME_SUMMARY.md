# Run Outcome Summary

## Purpose

이 문서는 `run-evidence-normalizer`와 `reconcile-review`가 공유하는
최소 owner-summary다.

정본은 아래에 있다.

- AxiomMd: generic evidence / reconcile artifact contract
- Product profile repo (if active): product-local run outcome, evidence, reconcile meaning extensions

## Unit of Review

기본 단위는 **selected slice 하나**다.

run outcome도 evidence bundle도 reconcile decision도
slice 하나를 기준으로 닫는다.

package 전체 의미를 다시 쓰지 말고,
selected slice 기준으로만 읽고 써야 한다.

## Evidence Stage Purpose

evidence stage의 목적은 "무슨 일이 일어났는지"를
정규화된 파일로 남기는 것이다.

이 단계는 아래를 하지 않는다.

- acceptance 결정
- source patch 결정
- relaunch 결정
- owner arbitration

## Reconcile Stage Purpose

reconcile stage의 목적은 normalized evidence를
source truth에 다시 연결해서
다음 액션을 결정하는 것이다.

허용된 classification은 아래 네 가지뿐이다.

- `accepted`
- `patch-required`
- `relaunch`
- `hold`

## Missing vs Negative

반드시 구분해야 한다.

- `missing evidence`
  - 필요한 근거가 없음
- `negative evidence`
  - 근거는 있으나 실패를 가리킴

이 둘을 섞으면 reconcile 분류가 흐려진다.

## Source Preservation Rule

evidence와 reconcile은 source truth를 다시 설명하는 문서가 아니다.

반드시 보존해야 하는 것:

- `feature_id`
- `package_ref`
- `slice_id`
- linked `req_ids`
- linked `task_ids`
- linked `eval_ids`

## Changed Path Rule

`changed_paths`는 반드시 관찰된 결과여야 한다.

- 추측으로 추가 금지
- prose summary만 남기기 금지
- selected slice boundary 밖으로 확장 금지

## Reconcile Decision Rule

- `accepted`: done conditions + verification checks가 근거 있게 만족됨
- `patch-required`: source truth를 바꿔야 다음 단계가 안전함
- `relaunch`: source truth는 유지 가능하지만 bounded rerun이 필요함
- `hold`: 안전한 bounded next step을 결정할 수 없음

## Handoff Rule

evidence-stage handoff와 reconcile-stage handoff를 섞지 않는다.

- evidence-stage handoff stage: `execution-and-evidence`
- reconcile-stage handoff stage: `reconcile-and-close`
