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

## Skill vs Workflow

- skill: 한 가지 reusable move
- workflow: 여러 skill을 순서와 gate로 묶은 실행 경로

## Skill Asset Rule

좋은 skill은 아래를 남긴다.

- stable input contract
- deterministic output shape
- reusable checklist or scaffold
- clear escalation point

## Final Rule

skill system의 목적은 agent를 더 똑똑하게 보이게 하는 것이 아니다.
같은 품질의 reasoning을 반복 가능하게 만드는 것이다.
