---
name: spec-writing-standard
description: Write or upgrade an AI-facing specification or scoped execution artifact using a reusable spec writing standard. Use when a repo needs a precise, implementation-ready contract with explicit goals, current evidence, boundaries, commands, validation gates, and approval rules. Do not use for lightweight briefs, changelogs, or loose brainstorm notes.
---

# Spec Writing Standard

## Purpose

Produce a specification that is safe and specific enough for autonomous coding work.
This skill combines contract-style spec structure with AI execution rules.

## Workflow

1. Read [references/AI_FACING_SPEC_WRITING_STANDARD.md](references/AI_FACING_SPEC_WRITING_STANDARD.md).
2. If the target repo already owns a normalized packet format, use the repo-owned packet first. For AxiomMd/AxiomSpecs work, the authoritative normalized input is AxiomMd `templates/input.packet.yaml`.
3. If the target repo does not already own a normalized packet format and the intake is weak or scattered, normalize it with [assets/spec-input-packet-template.md](assets/spec-input-packet-template.md).
4. Use section `16` of the reference standard to decide whether the output should be a full 18-section spec or a smaller scoped artifact.
5. For a full implementation spec, start from [assets/spec-writing-standard-template.md](assets/spec-writing-standard-template.md).
6. For a scoped artifact, start from [assets/scoped-artifact-template.md](assets/scoped-artifact-template.md).
7. Ground the draft in current repository evidence before making design decisions.
8. If a critical input is unknown, ask a targeted question or record an `OPEN` item. Do not silently guess.
9. If the output is a full 18-section spec, run `python3 <skill-root>/scripts/check_spec_standard.py <path/to/spec.md>` before finishing.
10. If the output is a scoped artifact, run `python3 <skill-root>/scripts/check_scoped_artifact.py <path/to/artifact.md>` before finishing.

## Input Ownership

- This skill is generic and does not replace a target repo's owned workflow packet.
- When the target repo already ships `input.packet.yaml` or equivalent, that repo-owned format wins.
- [assets/spec-input-packet-template.md](assets/spec-input-packet-template.md) is a fallback normalization worksheet for repos that do not already own a packet format.
- This skill should not fetch owner-repo GitHub documents at runtime.

## Input Contract

- when the target repo already owns a normalized packet, read that repo-owned packet first
- otherwise use [assets/spec-input-packet-template.md](assets/spec-input-packet-template.md) as the minimum intake worksheet
- minimum decision-ready intake still needs problem, boundary, current evidence, target delta, definition of done, and approval boundary

## Read Paths

- provided repo-owned input packet such as `input.packet.yaml`, when one exists
- relevant source-of-truth files, commands, logs, and failures from the target repository
- [references/AI_FACING_SPEC_WRITING_STANDARD.md](references/AI_FACING_SPEC_WRITING_STANDARD.md)
- local templates and validators inside this skill folder

## Write Paths

- the user-selected output artifact path for one full spec or one scoped artifact
- optional adjacent notes only when the target repo already expects them

## Output Target

- one implementation-ready full spec
- or one scoped artifact with explicit coverage categories

## Stop Conditions

- the intake does not provide, and repository evidence cannot recover, the minimum decision-ready facts
- the requested output is neither a full 18-section spec nor a valid scoped artifact
- the relevant validator still fails and the remaining failure cannot be resolved from repository evidence
- the target repo already owns multi-file package truth and the user is actually asking for package authoring rather than a spec artifact

## References

- Full standard: [references/AI_FACING_SPEC_WRITING_STANDARD.md](references/AI_FACING_SPEC_WRITING_STANDARD.md)
- Fallback input worksheet: [assets/spec-input-packet-template.md](assets/spec-input-packet-template.md)
- Full-spec template: [assets/spec-writing-standard-template.md](assets/spec-writing-standard-template.md)
- Scoped-artifact template: [assets/scoped-artifact-template.md](assets/scoped-artifact-template.md)

## When To Use

- Converting loose notes or PRDs into a working implementation spec.
- Upgrading an existing spec so it can guide AI coding agents safely.
- Writing a bounded scoped artifact that still needs explicit evidence, boundaries, failures, and validation.
- Defining repository execution, validation, and handoff rules.

## When Not To Use

- One-off idea capture.
- Product marketing copy.
- Roadmaps or changelogs.
- Tiny fixes that only need a short task note.
- Multi-file package truth that is already split across repository-owned `method/**` and `specs/**`.

## Commands

### Full-spec validator

```bash
python3 <skill-root>/scripts/check_spec_standard.py <path/to/spec.md>
```

### Scoped-artifact validator

```bash
python3 <skill-root>/scripts/check_scoped_artifact.py <path/to/artifact.md>
```

> `<skill-root>` = this skill's installation directory (the directory containing this SKILL.md).
