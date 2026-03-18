# Input Packet Contract

## Source Basis

이 skill은 아래 공통 규약을 기준으로 한다.

- AxiomMd `method/workflow-io-protocol.md`
- AxiomMd `templates/input.packet.yaml`

이 문서는 설치된 skill이 실행 중 참고할 최소 요약본이다.
GitHub에서 owner repo 문서를 다시 읽지 않는다.

## Required Fields

- `packet_version`
- `request_summary`
- `target_kind`
- `source_context_refs`
- `output_contract_refs`
- `scope.in`
- `scope.out`
- `constraints`
- `done_signals`
- `open_questions`
- `evidence_refs`

## Writing Rule

- input이 불명확하면 `open_questions`에 남긴다
- target output을 아직 모르면 `output_contract_refs`는 비워 두지 말고 다음 단계가 읽어야 할 owner docs 후보를 적는다
- 성공 조건이 애매하면 `done_signals`를 먼저 정리한다

## Typical `target_kind`

- `feature-package`
- `scoped-artifact`
- `review`
- `workflow-step`

## Final Rule

좋은 packet은 긴 설명이 아니라 다음 skill이 바로 읽을 수 있는 최소 구조다.
