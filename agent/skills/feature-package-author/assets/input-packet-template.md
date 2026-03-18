# Input Packet Contract

`feature-package-author`는 AxiomMd가 소유한 `input.packet.yaml` envelope를 입력으로 받는다.
정확한 필드 집합은 [assets/input.packet.yaml](input.packet.yaml)의 top-level shape를 따른다.

## Required Envelope

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

## Target-Kind Rule

- `target_kind` SHOULD be `feature-package`.
- `mode=create|update`와 `target_feature_path=specs/features/FEAT-xxxx-slug`는 `constraints`에 명시하거나 기존 package 경로에서 유도한다.

## AxiomSpecs Authoring Facts

아래 값은 top-level key를 새로 추가하지 말고, packet 내용 또는 기존 package/source evidence에서 **유도 가능해야 한다**.

- `feature_id`
- `slug`
- `title`
- `implementation_order`
- `profile_key`
- `review_mode`
- `planes`
- `owner_roles`
- `target_repos`
- `adoption`
- problem statement
- `in_scope`
- `out_of_scope`

권장 encoding:

- `constraints`: 식별자/enum-like metadata
- `request_summary`: title + short summary
- `scope.in` / `scope.out`: in-scope, out-of-scope
- `source_context_refs` / `evidence_refs`: target repo 안의 current truth paths
- `done_signals`: required package files, `contracts/` directory, owner-repo validation expectations

## Recommended Constraint Encoding

문자열 constraint는 아래처럼 `key=value` shape를 권장한다.

- `mode=create`
- `feature_id=FEAT-0042`
- `slug=evidence-replay-repair`
- `target_feature_path=specs/features/FEAT-0042-evidence-replay-repair`
- `implementation_order=5`
- `profile_key=axiom-v1`
- `review_mode=human_required`
- `planes=governance,reconcile`
- `owner_roles=product,governance`
- `target_repos=AxiomSpecs,AxiomRunner`
- `adoption.generic-methodology=direct-use`

## Recommended Packet Shape By Scenario

- create
  - `request_summary`에 title + short summary를 넣는다
  - `scope.in` / `scope.out`로 feature boundary를 잠근다
  - `constraints`로 stable metadata를 넘긴다
  - `source_context_refs`에 nearest current package/docs paths를 넣는다
- update
  - 기존 `package_path` 또는 `feature_id`를 `constraints`에 넣는다
  - `request_summary`에는 무엇을 고치는지 적는다
  - `evidence_refs`에는 broken package files나 failing owner checks를 넣는다

## Stop Rule

- `source_context_refs` 또는 `evidence_refs`에 current truth가 없으면 중단한다.
- semantic owner, target repo, adoption mapping이 packet이나 repo evidence에서 유도되지 않으면 `INPUT_GAP_REPORT`를 반환한다.
