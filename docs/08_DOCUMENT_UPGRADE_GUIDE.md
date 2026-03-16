# Document Upgrade Guide

## Purpose

이 문서는 새 문서를 추가하기 전에 무엇을 먼저 검토해야 하는지, 그리고 언제 삭제/이동/아카이브할지 고정한다.

## Order of Operations

새 문서를 만들기 전에 항상 아래 순서로 본다.

1. delete
2. merge
3. move
4. archive
5. create

즉, “새 문서를 만든다”는 마지막 선택지다.

## Delete First

아래에 해당하면 삭제 우선이다.

- 임시 메모
- 기존 문서와 질문이 완전히 같은 문서
- 승격되지 않은 탐색 메모
- 이미 다른 durable 문서에 흡수된 내용

## Merge When

- 같은 규칙을 두 문서가 설명한다
- 두 문서가 같은 독자를 대상으로 한다
- 둘을 합치면 질문 하나에 대한 답이 더 선명해진다

## Move When

- 문서 내용은 유효하지만 owner가 잘못됐다
- generic lesson이 product repo에 있다
- product-specific overlay가 methodology repo에 있다

## Archive Rarely

archive는 예외적으로만 쓴다.

- 외부 참조 가치가 큰 문서
- 중요한 의사결정 이력이 있는 문서
- 당장 삭제하면 추적성이 크게 깨지는 문서

초기 중복 문서에는 archive보다 delete를 우선한다.

## Promotion Rule

local lesson을 generic asset으로 승격하려면 아래를 만족해야 한다.

- 같은 문제가 반복된다
- 제품명을 지워도 의미가 남는다
- check, template, rule, harness로 바꿀 수 있다
- 다른 feature나 다른 제품에도 재사용 가능하다

## PR Checklist

- 이 문서는 정말 새로 필요했는가
- delete / merge / move 검토를 먼저 했는가
- owner 저장소가 맞는가
- 같은 질문에 답하는 기존 문서가 없는가
- durable rule과 backlog가 한 문서에 섞이지 않았는가

## Final Rule

문서 업그레이드의 목표는 문서 수를 늘리는 것이 아니다.
질문 하나당 답 하나가 남도록 구조를 정리하는 것이다.
