# Two-Repo Loop

## Purpose

이 문서는 methodology repo와 product-truth repo를 이용해 `방법론 -> 적용 -> 관측 -> 환류` 루프를 어떻게 닫을지 고정한다.

## Repository Roles

| 저장소 | 소유하는 진실 | 넣는 것 | 넣지 않는 것 |
| --- | --- | --- | --- |
| methodology repo | generic methodology truth | method docs, loop rules, quality rules, generic templates, reusable skills | product blueprint, feature truth, runtime detail |
| product-truth repo | product truth | blueprint, architecture, local profile, feature packages, delivery plan | generic method duplicates, implementation-local code detail |
| implementation repo | shipping code truth | crates, apps, adapters, tests, runtime integration | generic method 설명, product blueprint 설명 |

## Standard Flow

```text
1. generic rule or asset is defined in the methodology repo
2. the product-truth repo localizes it into a product profile or feature package
3. implementation repo ships code against the approved package
4. eval / evidence / drift / failures are observed
5. generic lesson is promoted back to the methodology repo
6. local lesson stays in the product-truth repo
```

## Promotion Rules

아래를 모두 만족하면 methodology repo로 승격한다.

- Axiom 전용 이름을 제거해도 성립한다
- 두 개 이상 feature package에서 반복된다
- 특정 runtime이나 path에 묶여 있지 않다
- template, rule, checklist, harness로 재사용 가능하다

아래 중 하나라도 해당하면 product-truth repo에 남긴다.

- Axiom surface나 plane을 직접 다룬다
- Axiom repo path를 직접 다룬다
- 특정 feature package의 product intent를 다룬다
- Axiom 조직 runtime adoption 정책을 다룬다

아래 중 하나라도 해당하면 implementation repo가 소유한다.

- crate / API / endpoint / CLI contract가 핵심이다
- runtime storage / process / transport detail이 핵심이다
- shipping code와 함께 바뀌어야 한다

## Observation Inputs

관측 입력은 아래에서 모은다.

- failing eval
- drift classification
- repeated review comment
- restart failure
- evidence insufficiency
- runtime mismatch
- handoff failure

## Feedback Decision

관측 후에는 반드시 아래 셋 중 하나로 닫는다.

1. methodology repo rule / template / harness 개선
2. product-truth repo package / profile / architecture 수정
3. implementation repo patch

아무 데도 승격되지 않는 반복 실패는 루프가 닫히지 않은 상태다.

## Anti-Patterns

- product-truth repo에 generic standard를 그대로 복제
- methodology repo에 제품 feature truth 저장
- implementation repo에 durable product blueprint 저장
- chat에만 결정을 남기고 source를 고치지 않음
