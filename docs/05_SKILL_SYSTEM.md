# Skill System

## Purpose

이 문서는 skill을 개발 방법론 자산으로 어떻게 다루는지 정의한다.

## What a Skill Is

skill은 prompt 조각이 아니다.
skill은 반복 가능한 reasoning move를 contract로 고정한 자산이다.

예:

- scope clarify
- structure scout
- plan build ready
- bounded review
- reconcile pass

## Why Skills Matter

agent는 raw reasoning을 안정적으로 재사용하지 못한다.
그래서 skill은 아래를 명시해야 한다.

- 목적
- 입력
- 출력
- acceptance
- stop condition
- evidence

## Compilation Chain

```text
skill
-> scaffold
-> harness
-> workflow step
-> work item
```

## Skill Design Rules

- 하나의 skill은 하나의 명확한 질문에 답해야 한다
- source of truth를 바꾸는 skill과 review-only skill을 섞지 않는다
- output이 다음 단계에서 바로 읽히는 형태여야 한다
- failure를 숨기지 말고 stop condition을 노출해야 한다
- skill은 읽는 경로와 쓰는 경로를 명시해야 한다

## Skill vs Workflow

- skill: 한 가지 reusable move
- workflow: 여러 skill을 순서와 gate로 묶은 실행 경로

## Skill Asset Rule

좋은 skill은 아래를 남긴다.

- stable input contract
- deterministic output shape
- reusable checklist or scaffold
- clear escalation point

## Skill Design Boundary

이 저장소는 generic skill design primitive를 소유한다.

- 입력 형식의 최소 조건
- 출력 형식이 가져야 할 일반 규칙
- stop condition
- evidence rule
- packaging checklist

즉 공통 규칙은 여기서 정한다.

- 어떤 입력 packet을 받는가
- 어떤 출력 packet을 남기는가
- 어떤 source file을 읽는가
- 어떤 source file을 바꿀 수 있는가

제품 특화 output contract는 여기서 직접 정의하지 않는다.

packaging 결과물은 아래를 canonical truth로 다시 선언하면 안 된다.

- generic writing rule body
- generic template 원본
- generic validator 원본
- generic workflow policy

같은 규칙이 두 군데에 생기면 skill truth가 둘로 갈라진다.

## Default Skill Split

기본 skill 세트는 역할이 분리돼야 한다.

- `feature-package-author`: feature package를 생성하거나 수정하는 source-changing skill
- `package-readiness-review`: readiness gate를 판정하는 review-only skill
- `spec-writing-standard`: 호환용 또는 외부 repo용 보조 skill

하나의 skill에 작성, 승인 판단, 구조 감사, 배포 정책을 같이 넣지 않는다.

## Skill I/O Rule

모든 skill은 최소 아래를 선언해야 한다.

- input packet
- output target
- read paths
- write paths
- stop condition

입력이 약하면 같은 skill도 다른 결과를 낸다.
출력이 흐리면 다음 단계가 다시 해석 비용을 낸다.
그래서 skill은 prompt보다 packet과 file contract가 먼저다.

## Skill Bundle Release Gate

installable bundle은 아래 셋이 닫혀야 release 후보가 된다.

### Gate 1. Required Bundle Set

- `SKILL.md`
- 참조된 `assets/`, `references/`, `scripts/`
- 선택적 `agents/openai.yaml`
- install manifest entry

### Gate 2. Linkage Completeness

- `SKILL.md`에 적힌 경로가 실제 파일과 일치한다
- validator / command가 bundle root 기준으로 실행 가능하다
- output / acceptance / stop condition / evidence가 명시돼 있다
- source-changing skill이면 바꾸는 진실의 범위가 적혀 있다
- review-only skill이면 수정 금지와 판정 출력이 적혀 있다

### Gate 3. Handoff Completeness

- source commit 또는 source revision
- generated version
- known limitation
- smoke test result

bundle release gate는 새로운 doctrine이 아니라 skill system의 release 번역본이다.

## Final Rule

skill system의 목적은 agent를 더 똑똑하게 보이게 하는 것이 아니다.
같은 품질의 reasoning을 반복 가능하게 만드는 것이다.
