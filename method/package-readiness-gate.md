# Package Readiness Gate

## Purpose

이 문서는 특정 제품이 아니라 **generic feature package**가 implementation-ready 상태인지 판정하는 최소 게이트를 정의한다.

## Why This Exists

문서가 있다고 해서 바로 구현-ready인 것은 아니다.
실행 전에 아래 네 가지가 닫혀야 한다.

1. authoring context가 충분한가
2. source package가 구조적으로 완전한가
3. requirement / task / eval linkage가 닫혀 있는가
4. 다른 사람이 채팅 기록 없이 이어받을 수 있는가

## Gate 0. Authoring Context Completeness

package가 아래 흐름 어디서 왔는지 file state로 보여야 한다.

- `input.packet.yaml`이 있다
- `route.decision.yaml`이 있다
- route가 `framing-first`면 `product-charter.md`, `system-blueprint.md`가 있다

이 정보가 전혀 없으면 package는 restartability가 약하다.
이 경우 최소 `patch-required`다.

## Gate 1. Required File Set

비사소한 feature package는 최소 아래를 가진다.

- `intent.md`
- `package.yaml`
- `requirements.yaml`
- `invariants.yaml`
- `design.md`
- `tasks.md`
- `evals.yaml`
- `risks.yaml`
- `decisions.jsonl`
- `slices.yaml`

필수 파일이 빠져 있으면 `hold`다.

## Gate 2. Linkage Completeness

아래가 모두 참이어야 한다.

- 모든 `must` requirement는 최소 1개의 blocking eval을 가진다
- 모든 requirement는 최소 1개의 task에 연결된다
- 모든 task는 최소 1개의 `REQ-*`와 `EVAL-*`를 가진다
- 모든 task는 touched path 또는 변경 경계를 가진다
- 모든 eval은 `req_ids`, `task_ids`를 가진다
- release-critical invariant는 hard eval 또는 deterministic proof와 연결된다

하나라도 빠지면 `patch-required`다.

## Gate 3. Design Completeness

`design.md`는 최소 아래를 설명해야 한다.

- boundary
- data / state model
- interfaces
- failure modes
- out-of-scope
- requirement mapping

"goal"과 "target paths"만 있고 구조 설명이 없으면 implementation-ready가 아니다.

## Gate 4. Risk And Approval Completeness

아래가 모두 명시돼야 한다.

- approval posture 및 approval 주체는 `profile_key` 기반 profile 규칙으로 해석됨
- high-risk 작업의 launch/posture 규칙
- blocking eval intent 소유/승인 방식이 product profile에 명시됨
- destructive / external / privileged behavior의 처리 방식
- brownfield면 current reality 또는 baseline

위험이 높은데 approval rule이 없으면 `hold`다.

## Gate 5. Handoff Completeness

긴 중단을 버티려면 아래가 file state에 남아 있어야 한다.

- 현재 progress
- 마지막 중요한 결정
- 열린 질문
- 다음 step
- blocker 또는 `none`
- 필요하면 `handoff.packet.yaml`

## Reference Validation

package는 가능하면 아래 검사를 통과해야 한다.

- required file set 존재
- must requirement와 blocking eval 연결
- task와 req/eval linkage 연결
- design 필수 섹션 존재
- handoff packet shape 유효

문서만 보고 "좋아 보인다"로 끝내지 않는다.

generic 저장소는 base validator를 소유할 수 있다.
제품 저장소는 그 base validator 위에 local overlay 검사를 더할 수 있다.

## Output States

게이트 판정은 아래 셋 중 하나다.

- `ready`
- `patch-required`
- `hold`

## Final Rule

좋은 package는 "문서가 많다"가 아니라 아래를 만족한다.

- 구현 범위가 bounded하다
- verification이 기계적으로 가능하다
- drift가 나도 source로 되돌릴 수 있다
- 다른 사람이 채팅 없이 재개할 수 있다
