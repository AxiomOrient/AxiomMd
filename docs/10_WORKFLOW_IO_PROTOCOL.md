# Workflow I/O Protocol

## Purpose

이 문서는 workflow 단계와 skill이 어떤 입력을 읽고 어떤 출력을 남겨야 하는지 정의한다.

## Why This Exists

오해는 대부분 여기서 생긴다.

- 입력이 제각각이다
- 출력이 제각각이다
- 다음 단계가 무엇을 읽어야 하는지 모른다

그래서 공통 규칙은 아래 둘을 고정해야 한다.

1. 입력 packet
2. handoff packet

## Core Rule

각 workflow 단계는 아래 중 하나를 입력으로 받고,
아래 중 하나를 출력으로 남겨야 한다.

### Allowed Inputs

- source file set
- `input.packet.yaml`
- 이전 단계의 `handoff.packet.yaml`

### Required Outputs

- source file update
- `handoff.packet.yaml`

채팅만 남기고 file-state를 남기지 않으면 protocol 위반이다.

## Input Packet

입력 packet은 사람이 준 요청을 다음 단계가 읽기 쉬운 형태로 정규화한 파일이다.

최소 필드:

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

이 packet은 “무엇을 만들지”와 “무엇을 바꾸면 안 되는지”를 같이 전달해야 한다.

## Handoff Packet

handoff packet은 한 단계가 끝난 뒤 다음 단계에게 넘기는 결과 파일이다.

최소 필드:

- `stage`
- `status`
- `input_ref`
- `changed_paths`
- `produced_paths`
- `evidence_refs`
- `open_questions`
- `next_step`
- `blockers`

이 packet은 “무엇이 끝났는지”보다 “다음 단계가 무엇을 읽고 어디서 시작할지”를 먼저 보여줘야 한다.

## Read / Write Rule

모든 skill은 아래를 명시해야 한다.

- read paths
- write paths
- output target
- stop condition

모든 skill이 모든 문서를 읽게 두면 엔트로피가 늘어난다.
반대로 read path와 write path를 고정하면 오해가 줄어든다.

## Stage Mapping

| Stage | Required Input | Required Output |
| --- | --- | --- |
| intent normalize | raw request or existing source | `input.packet.yaml` |
| package authoring | `input.packet.yaml` + source files | package files |
| review / readiness | source files | `handoff.packet.yaml` |
| bounded execution | approved tasks + source files | changed source + evidence |
| verification | source files + evidence | `handoff.packet.yaml` |
| reconcile | source files + evidence + handoff | source patch + `handoff.packet.yaml` |

## Folder Rule

공통 규칙은 아래만 고정한다.

- packet은 정해진 파일 형식을 가진다
- owning repo는 자기 문서 구조를 가진다
- skill은 정해진 read/write path만 사용한다

어느 저장소에 어떤 파일이 있는지는 각 저장소가 정한다.
하지만 packet 형식과 단계 입출력 규칙은 공통이어야 한다.

## Final Rule

좋은 workflow는 말을 잘하는 workflow가 아니다.
입력과 출력이 고정되어 있어서 다른 사람이나 다른 agent가 같은 방식으로 이어받을 수 있는 workflow다.
