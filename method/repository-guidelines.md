# Repository Guidelines

## Purpose

이 문서는 이 저장소에 무엇을 추가할 수 있고 무엇을 추가하면 안 되는지 고정한다.

## Placement Test

새 문서를 넣기 전에 아래를 먼저 본다.

1. 제품명을 지워도 성립하는가
2. Axiom 말고 다른 제품에도 그대로 재사용 가능한가
3. 특정 저장소 경로나 runtime 대신 generic contract로 설명 가능한가
4. 예시를 generic example로 바꿔도 의미가 보존되는가

모두 "예"면 이 저장소 후보다.
하나라도 "아니오"면 이 저장소 밖이 더 적합하다.

## Allowed

- AI 개발 방법론 문서
- harness engineering 문서
- spec-driven development 문서
- agentic / closed-loop development 문서
- mental model 문서
- skill / workflow / reusable reasoning asset 문서
- generic spec package standard
- generic template
- 문서 승격 / 정리 / 경계 유지 규칙

## Not Allowed

- 특정 제품 blueprint
- 특정 제품 feature spec
- 특정 제품 architecture
- 특정 제품 계획 문서
- 특정 제품 runtime / integration 상세
- 특정 crate, API, endpoint, command에만 맞는 설명

## Writing Rule

- 제품명을 넣지 않아도 설명 가능한 문서만 둔다.
- 특정 저장소 경로를 본문 진실로 삼지 않는다.
- 다른 저장소 파일을 직접 링크하지 않는다.
- 절대경로, 상대경로, `pwd` 기반 경로를 다른 저장소 파일 참조에 쓰지 않는다.
- reusable한 내용만 남긴다.
- 예시는 generic example로 쓴다.
- 한 문서는 한 질문에 답하게 쓴다.
- roadmap와 durable rule을 한 문서에 섞지 않는다.

## Reference Rule

다른 저장소에서 가져온 내용이 필요하면 아래처럼 처리한다.

1. 파일 링크를 남기지 않는다
2. generic lesson만 추출한다
3. 이 저장소 문장으로 다시 쓴다
4. 저장소 의존성이 생기는 표현은 지운다

## Curation Rule

- 같은 규칙을 두 군데 설명하면 합친다.
- generic 복제본은 남기지 않는다.
- 임시 메모는 승격하지 않으면 삭제한다.
- archive는 외부 링크 가치나 결정 이력이 중요한 경우에만 고려한다.

## Final Rule

이 저장소는 방법론 저장소다.
제품 문서가 필요해지는 순간, 그 문서는 이 저장소에 두지 않는다.
