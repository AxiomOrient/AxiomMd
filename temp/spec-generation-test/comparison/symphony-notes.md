# 비교 메모: openai/symphony vs AxiomMd 테스트 패턴

## 공통점
- 둘 다 작업을 코드 기반 실행 단위/워크플로우로 구조화한다.
- 실행기/스케줄러가 규칙 기반으로 에이전트를 분기/재실행한다.
- 운영자가 상태를 추적할 수 있는 관측성 채널이 필수다.

## Symphony의 장점
- `WORKFLOW.md`를 저장소 소유 정책 문서로 두고 실행 정책을 버전관리한다.
- issue tracker 연동, 워크스페이스 격리, 재시도/타임아웃/상태 관리가 명시된다.

## AxiomMd의 강점
- 입력/출력 artifact를 file-contract-first로 엄격히 정의한다.
- skill/feature package 생성 결과를 `workflow_check`로 정형 검증한다.
- UI-UX는 명시되지 않았지만, 패키지 기반으로 추가 설계가 충분히 가능하다.

## 업그레이드 필요 포인트
- AxiomMd 쪽은 UI 운영면의 기본 상태면에서 화면 설계가 약하다.
- Symphony처럼 `WORKFLOW.md` 같은 repository-owned policy 문서를 함께 병행하면, 운영 정책 변경 내역이 더 직관적이다.
- 두 방식의 장점을 합치려면: AxiomMd 계약(Artifact) + Symphony의 워크플로우 정책 레이어(UI/오케스트레이션 지표) 결합이 유효.
