# AxiomMd

AxiomMd는 generic methodology / reusable asset 저장소다.

## Role

AxiomMd가 소유하는 것은 아래다.

- 방법론 문서
- closed-loop 운영 규칙
- harness / quality / failure loop 규칙
- generic package standard
- generic readiness gate
- generic skill design primitive
- generic workflow input / output protocol
- generic template
- 문서 승격 / 정리 / 경계 유지 규칙

AxiomMd가 소유하지 않는 것은 아래다.

- 특정 제품의 blueprint
- 특정 제품 architecture
- 특정 제품 feature package
- 특정 제품 backlog / plan / evidence
- 특정 구현 저장소의 runtime 상세

## Boundary

핵심 원칙은 단순하다.

- generic하면 여기에 둔다
- Axiom에만 해당하면 여기 두지 않는다
- crate / API / runtime 세부사항이면 여기 두지 않는다

## Admission Rule

다음 질문에 모두 “예”면 AxiomMd 후보다.

1. 제품명을 지워도 의미가 남는가
2. 두 개 이상 제품에서 재사용 가능한가
3. 특정 repo path 대신 generic contract로 설명 가능한가
4. 예시를 generic example로 바꿔도 손상이 없는가

하나라도 “아니오”면 이 저장소 밖에 둔다.

## Curation Rule

- 중복 문서는 합친다.
- generic 복제본은 삭제한다.
- 임시 메모는 durable 문서로 승격하지 않으면 삭제한다.
- archive는 외부 참조 가치나 중요한 의사결정 이력이 있을 때만 쓴다.

## Scope

- 방법론 문서
- generic spec standard
- generic templates
- skill / workflow / harness 같은 reusable asset 문서
- 두 저장소 운영 규칙

## Out of Scope

- 특정 제품 blueprint
- 특정 제품 feature spec
- 특정 제품 runtime architecture
- 특정 제품 implementation backlog

## Read Order

1. `docs/00_DOCUMENT_MAP.md`
2. `docs/01_METHOD_TAXONOMY.md`
3. `docs/02_CONSTITUTION.md`
4. `docs/03_CLOSED_LOOP.md`
5. `docs/04_QUALITY_SYSTEM.md`
6. `docs/05_SKILL_SYSTEM.md`
7. `docs/06_REPOSITORY_GUIDELINES.md`
8. `docs/07_TWO_REPO_LOOP.md`
9. `docs/08_DOCUMENT_UPGRADE_GUIDE.md`
10. `docs/09_PACKAGE_READINESS_GATE.md`
11. `docs/10_WORKFLOW_IO_PROTOCOL.md`
12. `docs/11_CLIENT_INTENT_TO_SPEC_WORKFLOW.md`
13. `agent/workflow/README.md`
14. `specs/README.md`
15. `specs/SPEC_PACKAGE_STANDARD.md`
16. `templates/**`

## Current State

- 이 저장소는 generic methodology, generic package standard, generic readiness gate, generic skill design primitive, generic workflow input/output protocol을 소유한다.
- 제품 특화 output contract는 이 저장소가 소유하지 않는다.
- 방법론의 개선은 observation을 generic asset으로 승격할 때만 이 저장소에 반영한다.
- package가 구현-ready 상태인지 검토할 때는 `docs/09_PACKAGE_READINESS_GATE.md`를 먼저 통과해야 한다.
