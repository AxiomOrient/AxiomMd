# Workflow Policy Package

## Purpose

이 패키지는 spec-driven agentic execution에 필요한 최소 실행 계약을 고정한다.

과거 경로 `agent/workflow/`에서 정책 문서군을 분리해 `agent/policy/`로 이동했다.

## Included Files

| 파일 | 역할 |
| --- | --- |
| `WORKFLOW.md` | spec authoring workflow set과 execution loop 구조 |
| `ROLE_POLICY.md` | role ownership |
| `EVAL_POLICY.md` | evaluation rules |
| `ESCALATION_POLICY.md` | when to stop and escalate |
| `EXECUTION_POLICY.md` | execution state machine과 operational control |
| `SELF_REVIEW.md` | package self-assessment |

## Final Rule

source of truth drift를 막아야 할 때는 먼저 이 패키지 계약을 확인한다.
