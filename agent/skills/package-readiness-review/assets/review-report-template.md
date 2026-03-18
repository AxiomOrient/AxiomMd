# Package Readiness Review Note

이 문서는 optional human-readable sidecar다.
authoritative review-stage output은 반드시 `handoff.packet.yaml`이다.

## Summary

- Linked handoff packet: `<package-dir>/handoff.packet.yaml`
- Package: `<package-dir>`
- Handoff status: ready
- Overall verdict: ready

## Gate 1. Required File Set

- Present: ...
- Missing: none
- Result: pass

## Gate 2. Linkage Completeness

- Requirement coverage: ...
- Task coverage: ...
- Eval coverage: ...
- Broken links: none
- Result: pass

## Gate 3. Design Completeness

- Boundary: ...
- Interfaces: ...
- Failure modes: ...
- Requirement mapping: ...
- Result: pass

## Gate 4. Risk And Approval Completeness

- Review mode: ...
- Risk posture: ...
- Missing approval handling: none
- Result: pass

## Gate 5. Handoff Completeness

- Current progress: ...
- Next step: ...
- Blockers: ...
- Missing handoff items: none
- Result: pass

## Missing / Broken Items

- none

## Cheapest Next Fixes

- none

각 fix는 source-changing authoring pass가 바로 수행할 수 있는 최소 단위여야 한다.

## Evidence

- `<package-dir>/package.yaml`
- `<package-dir>/requirements.yaml`
- `<package-dir>/invariants.yaml`
- `<package-dir>/design.md`
- `<package-dir>/tasks.md`
- `<package-dir>/evals.yaml`
- `<package-dir>/risks.yaml`
- `<package-dir>/decisions.jsonl`
- `<package-dir>/slices.yaml`
