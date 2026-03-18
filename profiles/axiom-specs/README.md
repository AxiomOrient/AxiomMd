# AxiomSpecs Profile

AxiomMd 제네릭 커널 위에 AxiomSpecs 제품 전용 확장을 정의하는 프로파일.

## Profile Key

`axiom-v1`

## How to Use

skill 실행 시 아래 중 하나로 profile을 활성화한다.

**Option A** — `profile_manifest_path`:
```
profile_manifest_path: profiles/axiom-specs/shape.yaml
```

**Option B** — `profile_key` + `profile_root`:
```
profile_key: axiom-v1
profile_root: <path-to-AxiomMd-root>
```
→ resolves to `<profile_root>/profiles/axiom-v1/shape.yaml`

## What This Profile Adds

Generic 커널 계약 위에 다음을 추가한다.

| 항목 | 내용 |
| --- | --- |
| `package.yaml` additional fields | `feature_id`, `review_mode`, `profile_key`, `planes`, `implementation_order`, `owner_roles`, `target_repos`, `adoption`, `proof_state`, `current_progress`, `next_step`, `blockers` |
| Additional required file | `contracts/` directory |
| Path convention | `specs/features/FEAT-{id}-{slug}/` |
| Validator flag | `--base-dir <AxiomSpecs>` |
| Compile facts | `profile_key`, `proof_state` |
| Optional overlay | `authoring.request.yaml` |

## Files

```
profiles/axiom-specs/
  shape.yaml                       ← profile manifest (machine-readable)
  README.md                        ← this file
  assets/
    package-skeleton.md            ← AxiomSpecs package template
    author-checklist.md            ← AxiomSpecs authoring checklist
    input-packet-template.md       ← AxiomSpecs input constraints
    input.packet.yaml              ← AxiomSpecs example input packet
    authoring.request.yaml         ← optional product-local overlay template
    authoring.handoff.packet.yaml  ← AxiomSpecs authoring handoff template
    review-report-template.md      ← AxiomSpecs review report template
  references/
    OWNERSHIP_AND_OUTPUT_CONTRACT.md  ← AxiomSpecs ownership summary
    READINESS_AND_HANDOFF_CONTRACT.md ← AxiomSpecs readiness contract
```

## Generic Contract Unchanged

이 프로파일은 generic 필수 필드와 rules를 제거하지 않는다.
generic contract는 항상 유지된다.
