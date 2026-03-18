# Closed Loop

## Purpose

이 문서는 spec authoring 이후에 이어지는 표준 실행 루프를 정의한다.

## Two Parts

```text
authoring workflows
-> approved package
-> execution loop
```

spec 문서를 만드는 과정과,
승인된 package를 실행하는 과정은 나눠서 본다.

## Execution Loop

```text
approved package
-> bounded execution
-> verification
-> reconcile
-> acceptance
```

## Stage Contract

| Stage | Input | Output | Gate Question |
| --- | --- | --- | --- |
| Approval | approved feature package | approved revision | high-risk와 scope가 승인됐는가 |
| Execution | approved tasks | code, tests, traces, artifacts | 이번 loop의 범위가 bounded한가 |
| Verification | execution result | harness results, evidence draft | 통과/실패를 기계적으로 판단할 수 있는가 |
| Reconcile | spec + diff + tests + traces | spec patch, decision append, drift class | 새 행동이나 누락이 source에 반영됐는가 |
| Acceptance | evidence + reconcile result | accept / hold / patch-required | evidence가 충분한가 |

authoring workflow의 단계 정의는 `method/authoring-workflows.md`가 소유한다.

## Loop Size Rule

- trivial: 1 task
- normal: 1~3 tasks
- risky: 1 task + stronger verification
- large feature: milestone loop로 나눈다

## Artifact Rule

각 loop는 최소한 아래를 남긴다.

- updated task status
- validation result
- changed decisions or "none"
- next step or blocker
- handoff packet or explicit blocker state

## Packet Rule

각 단계는 말로만 넘기지 않는다.
최소 아래 둘 중 하나를 남겨야 한다.

- source file update
- handoff packet

정규화되지 않은 채팅 요약만으로 다음 단계가 시작되면 루프가 약해진다.

## Open Question Rule

모호함은 requirement로 위장하지 않는다.
open question으로 분리해 남긴다.

## Drift Classes

- `bug`: spec는 맞고 구현이 틀림
- `spec-missing`: 구현/현실이 source에 없음
- `intentional-change`: 의도적으로 바뀌었고 source도 바뀌어야 함
- `unclear-requirement`: requirement 자체가 모호함

## Completion Rule

작업은 아래가 모두 있을 때만 complete다.

- code or document change exists
- intended requirement IDs were addressed
- declared validation ran or explicit blocker exists
- reconcile result exists
- another contributor can resume without chat history
