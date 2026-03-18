# AI-Facing Spec Writing Standard

Status: Working standard v3

Purpose: Define how to write AI-facing specifications that are precise enough to guide autonomous coding work, safe enough to constrain risky behavior, and structured enough to support planning, task breakdown, implementation, and review.

Primary use:

- writing new full specs
- upgrading loose notes into implementable specs
- reviewing whether an existing spec is actionable for an AI coding agent
- defining repository-local execution workflows, validation, and AI handoff

## 1. Why This Standard Exists

A good AI-facing spec is not a memo.
It is an execution contract.

It must do four jobs at once:

1. explain what is being built and why
2. define the contracts the system must obey
3. constrain what the agent may, should, and must not do
4. make success and failure observable through commands, tests, and conformance checks

This standard combines:

- contract-style full-spec discipline from the spec-writing-standard templates and validators
- official OpenAI guidance on skills, workflows, evals, and explicit completion contracts
- spec-driven workflow guidance from GitHub Spec Kit
- requirement quality and verification guidance from INCOSE and SEBoK
- normative wording conventions from RFC 2119 and RFC 8174 when requirement levels must be unmistakable

## 2. The Working Model

Do not treat “the spec” as a single blob.
Treat it as a layered artifact set.

### 2.1 Layer A: Product Brief

This is the short, high-level description.
It answers:

- who is the user or operator
- what problem exists
- why this capability matters
- what success looks like
- what is out of scope

This layer should be brief and directional.

### 2.2 Layer B: Contract Spec

This is the main implementation contract.
It defines entities, files, states, workflows, failures, interfaces, and validation.

This is where ambiguity must be removed.

### 2.3 Layer C: Plan

The plan turns the contract into a technical strategy:

- architecture choices
- stack constraints
- sequencing
- tradeoffs
- migration approach

### 2.4 Layer D: Tasks

Tasks split the plan into reviewable, testable units.

Each task should:

- solve one bounded problem
- have clear inputs and outputs
- be testable in isolation
- avoid unrelated context

### 2.5 Layer E: Implementation and Review

Execution happens only after the previous layers are good enough.
Specs are living documents and must be updated when reality changes.

Important:

- Layer C and Layer D are conceptual layers, not mandatory file or folder names.
- Do not create separate `plans/` or `tasks/` document trees unless the target repo already uses them as its native workflow.
- In repositories that already keep truth in split docs/specs/package files, reuse those files instead of adding a parallel planning layer.

## 3. Core Principles

1. Facts and decisions must be separable.
2. The spec must reflect current code reality or explicitly declare intended divergence.
3. Vague wording is not allowed.
4. Boundaries must be written as contracts, not implied by tone.
5. Defaults, failures, recovery, and migration rules must be explicit.
6. A spec must be testable before it is called complete.
7. Large tasks must be decomposed into smaller prompts or work units.
8. The spec must be usable by both humans and AI agents.
9. Better input is preferable to stricter wording when the choice is between the two.
10. Missing critical facts must become targeted clarification questions or explicit `OPEN` items, not hidden assumptions.

### 3.1 Minimum Input Packet

Before drafting, collect the smallest packet that still supports a correct, reviewable, and testable artifact.

The required core is:

- problem, primary operator or user, and expected outcome
- important boundary or explicit non-goal
- current source-of-truth evidence such as repository paths, code files, existing specs, or observed commands
- target delta: what must change from current reality
- definition of done: the command, test, or observable signal that will prove success
- approval boundary: what changes need review first

These six items form the minimum decision-ready packet.
Without them, a spec usually becomes a polished guess.

If one required slot is unknown, do not silently invent it.
Either ask a targeted question or record an `OPEN` item with decision timing and impact.

### 3.2 High-Clarity Input Packet

Precision improves further when the packet also includes:

- sample inputs, outputs, or external contract examples
- concrete file paths, ownership boundaries, and integration touch points
- current commands, failing tests, logs, or other concrete failure evidence
- stable glossary terms, identifiers, or naming constraints
- state transitions, lifecycle examples, or sequencing constraints
- edge cases and negative cases
- migration triggers, compatibility expectations, and rollback behavior
- performance, security, compliance, or legal constraints when relevant

These are precision boosters, not universal blockers.
Use them to improve difficult or high-risk specs without forcing every small task through a heavyweight questionnaire.

### 3.3 Ambiguity Handling and Balance

Do not turn the intake step into a questionnaire.
Ask only when the missing information changes:

- correctness
- safety or blast radius
- external contract shape
- validation method
- migration behavior

If the gap is a blocker, ask a targeted question or record a time-bound `OPEN` item.
If the gap affects only a reversible local choice, proceed with the narrowest safe assumption and state it explicitly.

Prefer the smallest input packet that still passes review and validation.
More input is useful only when it reduces real ambiguity, not when it adds ceremony.

## 4. Evidence Rules

Use this evidence priority when sources conflict:

1. current running code
2. current primary spec
3. current implementation plan or task ledger, if the repo already uses one
4. other repository docs
5. examples, demos, or screenshots
6. comments, UI copy, or implied behavior

Rules:

- Never infer backend contracts from UI wording alone.
- Never finalize a product contract from examples alone.
- If code and spec differ, classify the mismatch explicitly:
  - current bug
  - outdated doc
  - intentional future divergence

## 5. Mandatory Six Operational Areas

Every AI-facing spec must cover these six operational areas either in the main body or in a dedicated execution appendix.

### 5.1 Commands

List exact executable commands.

- include full command lines
- include flags when relevant
- note whether commands mutate state

Examples:

- `npm test`
- `pytest -v`
- `cargo test --workspace`

### 5.2 Testing

State how correctness is verified.

- test framework
- command
- test location
- required pass criteria
- conformance cases if any

### 5.3 Project Structure

State where important things live.

- source directories
- test directories
- docs directories
- generated output
- config and manifest locations

### 5.4 Code Style

Do not describe style abstractly if examples can make it concrete.

- naming rules
- formatting rules
- preferred patterns
- prohibited patterns

### 5.5 Git Workflow

Document workflow expectations when relevant:

- branch naming
- commit message format
- PR expectations
- rebase, merge, or squash rules

### 5.6 Boundaries

Document what the agent may and may not touch.

- secrets
- generated directories
- vendored dependencies
- production config
- infrastructure definitions
- other high-blast-radius files

## 6. Three-Tier Boundary Policy

Every AI-facing spec should express boundary rules using three levels.

### 6.1 Always Do

Actions that should happen without asking.

Examples:

- always run validation before handoff
- always follow naming conventions
- always preserve structured logs

### 6.2 Ask First

Actions that might be valid but need approval.

Examples:

- schema changes
- dependency additions
- CI/CD changes
- deleting tests

### 6.3 Never Do

Hard stops.

Examples:

- never commit secrets
- never edit vendored dependencies
- never remove failing tests without approval

## 7. Required Spec Shape

For full implementation specs, use this 18-section top-level skeleton.

1. Problem Statement
2. Goals and Non-Goals
3. System Overview
4. Core Domain Model
5. Domain Contract
6. Configuration and Input Contract
7. Lifecycle or State Model
8. Primary Workflows and Reconciliation
9. Storage, Ownership, and Safety Boundaries
10. Execution or Interface Contract
11. External Integration Contract
12. Context Packaging and Prompt Inputs
13. Logging, Status, and Observability
14. Failure Model and Recovery Strategy
15. Safety, Boundaries, and Human Approval Policy
16. Reference Algorithms and Task Decomposition
17. Validation, Commands, and Success Criteria
18. Implementation Checklist and Change Control

Optional appendices may follow section 18.

## 8. Section Intent

### 8.1 Problem Statement

Must answer:

- what the system is
- what problem it solves
- who uses it
- what boundary it does not cross

Include an “important boundary” block when confusion is likely.

### 8.2 Goals and Non-Goals

Goals define required capability.
Non-goals remove likely ambiguity.

If a future implementer could reasonably assume something is included, either make it a goal or a non-goal.

### 8.3 System Overview

Define:

- main components
- abstraction levels
- external dependencies
- key repository paths

### 8.4 Core Domain Model

Define the stable nouns.

Every major entity should include:

- identity
- required fields
- optional fields
- mutability
- storage location
- lifecycle
- references and relations

### 8.5 Domain Contract

Turn the outside world into a contract.

Examples:

- repository contract
- workflow file contract
- manifest contract
- package contract
- API object contract

### 8.6 Configuration and Input Contract

Define:

- precedence
- defaults
- coercion
- validation
- reload behavior

### 8.7 Lifecycle or State Model

Make transitions explicit.

Must include:

- states
- entry conditions
- transition triggers
- guards
- terminal states

### 8.8 Primary Workflows and Reconciliation

Describe the core loops or workflows as stepwise logic:

- trigger
- inputs
- preconditions
- algorithm
- side effects
- failure modes
- idempotency

### 8.9 Storage, Ownership, and Safety Boundaries

Define where state lives and who owns it.

Must cover:

- file layout
- ownership and lock rules
- managed vs unmanaged paths
- destructive boundaries

### 8.10 Execution or Interface Contract

Define how work is launched or invoked:

- CLI
- API
- pipeline step
- app-server protocol
- renderer contract

### 8.11 External Integration Contract

Define external systems explicitly.

For each integration:

- required inputs
- output shape
- assumptions
- failure handling

### 8.12 Context Packaging and Prompt Inputs

This section is required for AI-facing specs.

It must state:

- what context is always required
- what context is task-specific
- what should be summarized vs fully included
- how large specs should be split
- when a fresh context or new session is preferable

### 8.13 Logging, Status, and Observability

Define:

- operator-visible state
- logs and traces
- status surfaces
- minimum observability requirements

### 8.14 Failure Model and Recovery Strategy

Define stable failure classes.

For each important failure:

- error code
- trigger
- severity
- what it blocks
- recovery path

### 8.15 Safety, Boundaries, and Human Approval Policy

Include:

- Always Do
- Ask First
- Never Do
- trust assumptions
- secret and destructive-action policy

### 8.16 Reference Algorithms and Task Decomposition

Give language-agnostic step sequences for important flows.

Also define:

- how work breaks into tasks
- what can run in parallel
- what must remain sequential
- what boundaries prevent task collisions

### 8.17 Validation, Commands, and Success Criteria

This section must make “done” testable.

Include:

- exact commands
- validation matrix
- success criteria
- conformance or regression suite rules
- measurable gates where possible

### 8.18 Implementation Checklist and Change Control

Close with:

- required for conformance
- recommended extensions
- operational validation before release
- when the spec must be updated

## 9. Sentence-Level Writing Rules

### 9.1 Prohibited Phrases

Do not use empty or non-testable language like:

- appropriately
- if needed
- flexibly
- efficiently
- safely handles
- user-friendly
- enough
- as appropriate
- where possible
- if practical
- including but not limited to
- etc.

Replace vague claims with observable rules.
Avoid escape clauses and open-ended wording that lets the document sound precise while hiding the actual obligation.

### 9.2 Normative Wording

Use these intentionally when requirement strength must be unmistakable:

- `MUST`
- `MUST NOT`
- `SHOULD`
- `MAY`

When these words are uppercase, use them with RFC 2119 / RFC 8174-style intent.
Do not capitalize them casually.

- `MUST` / `MUST NOT`: absolute requirement or prohibition
- `SHOULD`: strong default that expects an explicit reason if you deviate
- `MAY`: allowed but optional

Normative text does not require uppercase keywords everywhere.
Use them where the requirement level matters, and write every mandatory rule as a concrete obligation.

### 9.3 Stable Terms

Choose one term for each concept and reuse it consistently.

If the document alternates between `workspace`, `project dir`, and `target path` for the same thing, the spec is not ready.

Prefer one obligation per sentence whenever practical.
Split combined clauses when separate conditions, actions, or exceptions matter.

## 10. Required Entity Rules

When introducing an entity, define:

1. name
2. identity
3. id rules
4. mutability
5. stored location
6. required fields
7. optional fields
8. relationships
9. lifecycle
10. deletion or archival behavior
11. migration impact if relevant

## 11. Required Workflow Rules

Every important workflow should specify:

1. trigger
2. inputs
3. preconditions
4. algorithm
5. side effects
6. failure modes
7. idempotency
8. output or result object

## 12. Required File-Format Rules

For every external or persisted file format, specify:

1. path or location
2. file format
3. version field
4. minimum example
5. required fields
6. defaults
7. unknown-field behavior
8. compatibility and migration rules

## 13. Defaults, Migration, and Drift

If there is a default, specify:

1. the default value
2. why it exists
3. how it can be overridden
4. override precedence

If current code and target design diverge, include a migration strategy:

- from
- to
- detection
- read strategy
- write strategy
- rollback or safety guarantees

## 14. Validation Standard

Specs must define both structural and behavioral validation.

### 14.1 Structural Validation

The document should have:

- stable top-level shape
- stable section naming
- deterministic subsection order

For full specs, structural validation means the stable 18-section skeleton.
For scoped artifacts, structural validation means the required coverage categories are present, non-empty, and explicit even if heading names vary.

### 14.2 Behavioral Validation

The system should have:

- test cases
- conformance rules
- acceptance criteria
- human review gates for subjective quality

### 14.3 Success Criteria

Success criteria should be:

- specific
- measurable
- achievable
- relevant

Whenever possible, prefer:

- pass/fail commands
- explicit thresholds
- edge-case handling expectations

## 15. Context Packaging Rules

Large context degrades quality.
Do not hand an agent the entire world by default.

Preferred pattern:

1. brief
2. contract spec
3. plan or strategy notes, if they exist
4. task slice or bounded work unit
5. relevant local code or files only

For large specs:

- create a concise summary or extended TOC
- keep a high-level overview available
- provide detailed sections on demand

Use one focused prompt or task per work unit whenever possible.

## 16. Minimal vs Full Specs

Do not force a heavyweight spec onto trivial work.

Use a minimal scoped artifact when:

- the task is isolated
- the blast radius is low
- no broad persistent-state or security redesign is involved
- one bounded change can be reviewed without the full 18-section contract

A scoped artifact does not need the 18-section skeleton.
It still MUST expose the following coverage categories in some explicit form:

1. scope declaration and intended use
2. current reality and source-of-truth evidence
3. target delta or contract change
4. omitted standard sections or explicit not-applicable areas
5. boundaries and approval rules
6. failure, risk, recovery, or rollback behavior
7. validation commands or observable success criteria

If there are unresolved blockers or chosen assumptions, record them as `OPEN` items or explicit assumptions.
Preserve any entity, workflow, file-format, or migration rule that still matters to the scoped task.
If the repo already has a stronger native truth structure, scoped artifacts should point back to that structure instead of recreating it.

Headings may vary.
The validator for scoped artifacts should check coverage, not an exact section list.

Recommended minimal heading set:

- Scope and Intended Use
- Current Reality and Evidence
- Target Delta
- Boundaries, Risks, and Approvals
- Validation and Success Criteria
- Omitted / Not Applicable Canonical Areas
- Open Questions / Assumptions

Use a full 18-section spec when:

- state exists
- failures matter
- multiple systems integrate
- migration or persistence exists
- more than one contributor or agent will rely on the artifact
- the document is the main implementation contract rather than a bounded sub-artifact

## 17. Review Loop Standard

Every serious spec workflow should include:

1. draft
2. review against criteria
3. refine
4. validate
5. execute
6. re-sync spec if reality changes

Recommended self-correction loop:

1. generate draft
2. review draft against explicit checklist
3. revise draft
4. validate structure
5. use for planning or implementation

## 18. Practical Checklist

Before handing a spec to an AI coding agent, verify:

- the mission is explicit
- non-goals remove ambiguity
- the six operational areas are covered
- Always / Ask First / Never policy exists
- current evidence is cited or known
- entities, ids, states, and files are explicit
- failures and recovery rules are explicit
- commands and validation gates are explicit
- the spec can be split into task-sized contexts
- the spec can be updated as reality changes

## 19. Repository-Specific Adaptation Notes

For repository-local use:

- do not ignore current code reality
- do not infer contracts from UI copy
- do not omit migration where code and target design diverge
- do not ship schema, CLI, job, benchmark, or UI specs without validation rules
- use `OPEN` only for genuinely unresolved decisions

`OPEN` entries should include:

- what is unresolved
- why it is unresolved
- what is already known
- when the decision must be made

## 20. Source Notes

This standard is synthesized from the following source material:

- OpenAI Codex docs
  - skills: progressive disclosure, `SKILL.md` as the entrypoint, and clear trigger descriptions
  - workflows: explicit context and a precise definition of done
  - eval guidance: evaluate skills against a clear completion contract
  - prompt guidance: prefer the smallest prompt that passes evals, and keep output contracts explicit
  - https://developers.openai.com/codex/skills/
  - https://developers.openai.com/codex/workflows/
  - https://developers.openai.com/blog/eval-skills/
  - https://developers.openai.com/api/docs/guides/prompt-guidance
- GitHub Spec Kit
  - spec-driven workflow, required clarification before planning, and checklist-style quality checks
  - https://github.com/github/spec-kit
  - https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- INCOSE / SEBoK
  - well-formed requirement characteristics such as necessary, unambiguous, complete, singular, feasible, and verifiable
  - verification versus validation and requirement-quality checks
  - https://www.incose.org/docs/default-source/working-groups/requirements-wg/guidetowritingrequirements/incose_rwg_gtwr_v4_summary_sheet.pdf
  - https://sebokwiki.org/wiki/System_Verification
  - https://sebokwiki.org/wiki/System_Validation
- RFC requirement-level conventions
  - uppercase `MUST` / `SHOULD` / `MAY` usage semantics when requirement levels must be explicit
  - https://datatracker.ietf.org/doc/html/rfc2119
  - https://www.rfc-editor.org/rfc/rfc8174.html
- local contract-style spec patterns
  - 18-section discipline, template-first drafting, and structural validation for full specs
