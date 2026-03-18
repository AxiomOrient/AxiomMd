# Routing Rules

## Source Basis

이 skill은 아래 공통 규약을 기준으로 한다.

- AxiomMd `method/authoring-workflows.md`
- AxiomMd `templates/input.packet.yaml`

## Route Types

### `direct-package`

아래가 이미 보이면 선택한다.

- 문제 범위가 좁다
- in-scope / out-of-scope가 보인다
- 성공 조건이 보인다
- feature package로 바로 쪼갤 수 있다

### `framing-first`

아래 중 하나라도 해당하면 선택한다.

- 요청이 너무 넓다
- 여러 영역이 섞여 있다
- 경계가 불분명하다
- 이번 범위 밖이 안 보인다
- feature split이 아직 안 된다

### `hold`

아래면 선택한다.

- packet이 너무 약하다
- scope와 done signal이 서로 충돌한다
- evidence가 너무 부족하다

## Required Outputs

- `packet_version`
- `input_ref`
- `route`
- `reason_summary`
- `required_artifacts`
- `next_step`
- `open_questions`
- `blockers`

## Final Rule

좋은 라우팅은 똑똑해 보이는 라우팅이 아니라,
다음 문서 종류를 분명하게 고르는 라우팅이다.
