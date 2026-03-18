# Ownership And Output Contract (AxiomSpecs Profile)

이 문서는 AxiomSpecs 프로파일이 활성화된 경우 generic OWNERSHIP_AND_OUTPUT_CONTRACT를 대체한다.

## Source Basis

This profile is aligned to these owner-repo files:

- `method/artifact-and-contract.md`
- `method/authoring-workflows.md`
- `templates/input.packet.yaml`
- `templates/route.decision.yaml`
- `templates/handoff.packet.yaml`
- `AxiomSpecs/README.md`
- `AxiomSpecs/docs/03_SERVICE_SPEC.md`
- `AxiomSpecs/specs/STANDARD_STACK.md`
- `AxiomSpecs/profiles/axiom-v1/profile.yaml`
- `AxiomSpecs/profiles/axiom-v1/package-and-readiness.shape.yaml`
- `AxiomSpecs/profiles/axiom-v1/slice.shape.yaml`
- `AxiomSpecs/profiles/axiom-v1/run-outcome.shape.yaml`
- `AxiomSpecs/specs/README.md`
- `AxiomSpecs/scripts/check_specs`
- current `AxiomSpecs/specs/features/**`

Do not fetch owner-repo files from GitHub at runtime.
Refresh this summary only when the owner repos change.

## Ownership Split

- AxiomMd owns the normalized workflow packet formats and the generic package contract.
- AxiomSpecs owns the feature package output shape and the Axiom local profile.
- This skill must not invent a new packet envelope or a new product-truth package shape.

## Input Envelope

The authoritative input envelope is AxiomMd `input.packet.yaml`.
The normal workflow also provides `route.decision.yaml`.
If the route is `framing-first`, `product-charter.md` and `system-blueprint.md` are expected to exist before package authoring starts.
`authoring.request.yaml` is an optional Axiom-local overlay input for create-mode metadata.
Use it when product-local fields would otherwise be packed into free-form `constraints`.
This skill may derive missing details from an existing feature package only when `mode=update`.

## AxiomSpecs Package Shape

AxiomSpecs package shape (profile-extended):

- `intent.md`
- `package.yaml`
- `requirements.yaml`
- `invariants.yaml`
- `design.md`
- `tasks.md`
- `evals.yaml`
- `risks.yaml`
- `decisions.jsonl`
- `contracts/`
- `slices.yaml`

`slices.yaml` defines the launchable slices for this package.
Each slice must have `slice_id`, `path_scope`, `req_ids`, `task_ids`, `eval_ids`, `done_conditions`, `verification_checks`, `budget`, `approval_mode`.

## AxiomSpecs House Metadata

Current active packages consistently use these `package.yaml` fields:

- `feature_id`
- `slug`
- `title`
- `state`
- `review_mode`
- `profile_key`
- `planes`
- `implementation_order`
- `owner_roles`
- `target_repos`
- `adoption`
- `proof_state`
- `current_progress`
- `next_step`
- `blockers`

`proof_state` tracks implementation proof separate from source package structure:
`not_proven | reference_slice_proven | runtime_proven | reconciled`

## Local Profile

- `review_mode` default: `human_required`
- `profile_key` current value: `axiom-v1`
- baseline `planes`: `source | compile | execution | control | governance | reconcile`
- baseline `adoption` modes:
  - `direct-use`
  - `direct-use-authoring-only`
  - `direct-use-execution-only`
  - `semantic-direct-use`
  - `renewal-base`
  - `reference-only`

Some current packages also use repo-local adoption tokens beyond the baseline profile list.
Preserve those tokens on update when they already exist in package truth.
For new packages, prefer the baseline profile modes unless direct repository evidence supports a new token.

## Validation

Use the owner repo checker with base-dir:

```bash
python $AXIOM_MD/scripts/workflow_check.py package <feature-dir> --base-dir <AxiomSpecs>
```

This checker is the current owner-repo source for required file set, linkage completeness, and handoff metadata.
At runtime, use the local target repository copy of that checker.

## Authoring Stage Handoff

Emit one `handoff.packet.yaml` at the end of authoring:

- `stage: feature-package-authoring`
- `status: ready | patch-required | hold | blocked`
- concrete `produced_paths`
- concrete `evidence_refs`
- concrete `next_step`

Default path: `<target_feature_path>/handoff.packet.yaml`.
Final readiness handoff (stage: readiness-and-handoff) is owned by the review skill.
