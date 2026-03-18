# Ownership And Output Contract

## Source Basis

This skill is aligned to these kernel files:

- `method/artifact-and-contract.md`
- `method/authoring-workflows.md`
- `templates/input.packet.yaml`
- `templates/route.decision.yaml`
- `templates/handoff.packet.yaml`

If a profile is active, this skill is also aligned to the profile manifest at:

- `<profile_root>/profiles/<profile_key>/shape.yaml`

This file is a local summary for the installed skill.
Do not fetch owner-repo files from GitHub at runtime.
Refresh this summary only when the kernel or profile contract changes.

## Ownership Split

- AxiomMd owns the normalized workflow packet formats and the generic package contract.
- The product profile (if provided) owns product-specific package shape extensions.
- This skill must not invent a new packet envelope or a new product-truth package shape.

## Input Envelope

The authoritative input envelope is `input.packet.yaml`.
The normal workflow also provides `route.decision.yaml`.
If the route is `framing-first`, `product-charter.md` and `system-blueprint.md` are expected to exist before package authoring starts.
This skill may derive missing details from an existing feature package only when `mode=update`.

## Generic Output Shape

Required package files (no profile):

- `intent.md`
- `package.yaml`
- `requirements.yaml`
- `invariants.yaml`
- `design.md`
- `tasks.md`
- `evals.yaml`
- `risks.yaml`
- `decisions.jsonl`
- `slices.yaml`

`slices.yaml` defines the launchable slices for this package.
Each slice must have `path_scope`, `req_ids`, `task_ids`, `eval_ids`, `done_conditions`, `approval_mode`.

When a profile is active, the profile manifest may define additional required files or directories.

## Generic Package Metadata

Required `package.yaml` fields (no profile):

- `id`
- `slug`
- `title`
- `state`
- `layer`

When a profile is active, the profile manifest defines additional required fields.
Generic fields must always be present regardless of profile.

## Validation

Use the kernel checker:

```bash
python $AXIOM_MD/scripts/workflow_check.py package <feature-dir>
```

This checker is the source for required file set, linkage completeness, and handoff metadata.
If a profile specifies a validator, run it after the generic checker passes.

## Authoring Stage Handoff

Emit one `handoff.packet.yaml` at the end of authoring:

- `stage: feature-package-authoring`
- `status: ready | patch-required | hold | blocked`
- concrete `produced_paths`
- concrete `evidence_refs`
- concrete `next_step`

Default path: `<target_feature_path>/handoff.packet.yaml`.
Final readiness handoff (stage: readiness-and-handoff) is owned by the review skill.
