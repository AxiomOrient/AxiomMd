# Method Index

## Purpose

이 저장소에서 어떤 문서가 어떤 generic methodology 질문에 답하는지 고정한다.

## Document Set

| 문서 | 답하는 질문 |
| --- | --- |
| `method/taxonomy.md` | AI 개발 방법론들을 어떻게 구분하는가 |
| `method/constitution.md` | 이 방법론의 불변 원칙은 무엇인가 |
| `method/closed-loop.md` | 표준 실행 루프는 어떻게 닫히는가 |
| `method/quality-system.md` | 코드 품질, 실패, 하네스를 어떻게 운영하는가 |
| `method/skill-system.md` | skill을 어떻게 정의하고 workflow 자산으로 쓰는가 |
| `method/repository-guidelines.md` | 이 저장소 경계와 입고 기준은 무엇인가 |
| `method/two-repo-loop.md` | generic / product / implementation 경계를 어떻게 나누는가 |
| `method/document-upgrade-guide.md` | 문서를 어디에 추가하고 언제 삭제 / 이동 / 아카이브할 것인가 |
| `method/package-readiness-gate.md` | package가 implementation-ready 상태인지 어떻게 판정하는가 |
| `method/workflow-io-protocol.md` | workflow 단계와 skill이 어떤 입력을 읽고 어떤 출력을 남겨야 하는가 |
| `method/authoring-workflows.md` | 클라이언트 입력에서 어떤 workflow를 거쳐 spec으로 좁혀 가는가 |
| `method/output-profile-interface.md` | generic kernel이 product-specific output profile을 어떻게 연결하는가 |

## Boundary

- 이 저장소는 방법론을 다룬다.
- 특정 제품의 blueprint나 feature truth는 다루지 않는다.
- 제품별 내용은 이 저장소 밖에서 소유한다.

## Add / Remove Rule

새 문서를 추가하기 전에 `method/document-upgrade-guide.md`를 먼저 본다.

- `method/` 폴더는 generic methodology 문서만 담는다
- 제품 특화 내용, 임시 메모, 탐색 노트는 이 폴더에 두지 않는다
- 새 문서를 만들기 전에 기존 문서에 합칠 수 없는지 먼저 확인한다
