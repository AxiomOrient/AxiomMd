# Input Packet Contract (AxiomSpecs Profile)

AxiomSpecs profile이 활성화된 경우, 아래 authoring facts가 추가로 유도 가능해야 한다.

## Required Authoring Facts (AxiomSpecs)

아래 값은 packet 내용 또는 기존 package/source evidence에서 유도 가능해야 한다.

- `feature_id` (AxiomSpecs uses feature_id, e.g. FEAT-0042)
- `slug`
- `title`
- `implementation_order`
- `profile_key` (always: axiom-v1)
- `review_mode` (default: human_required)
- `planes`
- `owner_roles`
- `target_repos`
- `adoption`
- problem statement
- `in_scope`
- `out_of_scope`

## Recommended Constraint Encoding (AxiomSpecs)

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

## Done Signals (AxiomSpecs)

- `required package files and contracts/ directory exist`
- `workflow_check.py package returns ready for the target package`

## authoring.request.yaml Overlay

create-mode metadata가 많으면 constraints 대신 `authoring.request.yaml`로 분리한다.
template: `profiles/axiom-specs/assets/authoring.request.yaml`
