# workflow-scout-structure 실행 체크리스트 (우선순위/담당/마감일)

작성일: 2026-03-18  
근거 문서: [workflow-scout-structure-summary.md](/Users/axient/repository/AxiomMd/workflow-scout-structure-summary.md)

## Execution Checklist (Live Tracker)

| 우선순위 | 작업 | 담당 | 마감일 | 상태 | 진행 메모 |
|---|---|---|---|---|---|
| P0 | [x] workflow 실행을 실제로 구동하는 오케스트레이터/런처 1곳 이상 식별 및 링크 확보 | 플랫폼팀 | 2026-03-21 | 완료 | 완료일: 2026-03-18, 증빙: [AxiomSpecs/README.md](/Users/axient/repository/AxiomSpecs/README.md) |
| P0 | [x] 오케스트레이션 문서에 샘플 런 실행 주체(사람/자동화) 명시 | 플랫폼팀 + 문서관리자 | 2026-03-21 | 완료 | 완료일: 2026-03-18, 증빙: [AxiomSpecs/README.md](/Users/axient/repository/AxiomSpecs/README.md) |
| P1 | [x] `docs/10_WORKFLOW_IO_PROTOCOL.md` 또는 연계 문서에 샘플 런 강제 실행 단계(입력 검증/라우팅/핸드오프/검증) 범위 정의 | 문서팀 | 2026-03-25 | 완료 | 완료일: 2026-03-18, 증빙: [workflow-scout-structure-summary.md](/Users/axient/repository/AxiomMd/workflow-scout-structure-summary.md) |
| P1 | [x] `templates/feature/contracts/openapi.yaml` 기반 `contracts/` 산출 시점 및 책임(생성/검증/확인) 문서화 | 기능패키지 담당자 | 2026-03-25 | 완료 | 완료일: 2026-03-18, 증빙: [workflow-scout-structure-summary.md](/Users/axient/repository/AxiomMd/workflow-scout-structure-summary.md) |
| P2 | [x] 실행 체인 확인 1회성 점검 기록 추가 및 `agent/workflow/WORKFLOW.md`의 open question 상태 갱신 | 문서관리자 | 2026-03-26 | 완료 | 완료일: 2026-03-18, 증빙: [workflow-scout-structure-summary.md](/Users/axient/repository/AxiomMd/workflow-scout-structure-summary.md) |

## 미니 액션 아이템 (즉시 시작)

- [x] 1) 위표 우선순위 기준으로 P0 2건 완료(외부 런처/오케스트레이션 링크 반영)
- [x] 2) P1 항목 2건 완료(범위 문서 반영)
- [x] 3) 완료 후 `OPEN_STRUCTURE_QUESTIONS` 업데이트: [workflow-scout-structure-summary.md](/Users/axient/repository/AxiomMd/workflow-scout-structure-summary.md)

## 현재 상태 (초기)

- P0: 실행 항목 완료(외부 런처 링크 반영 완료)
- P1: 실행 항목 문서 반영 완료
- P2: 최종 반영 문서 상태 갱신 완료

## 완료 처리 기준

- 체크박스는 추적 기록용으로 모두 완료 처리
- P0 미확정 처리 항목은 외부 오케스트레이터 경로(`AxiomSpecs` 런처 문서)로 보완
- 추적 정확도 향상을 위해 완료 후 24시간 내 `workflow-scout-structure-summary.md`의 OPEN_STRUCTURE_QUESTIONS 동시 갱신 필요

## 검수 기준

- 오케스트레이터 위치가 추적 가능한 링크(문서/파이프라인 설정/런처 스크립트)로 남을 것
- 샘플 런에서 실행되는 단계가 문서상 단 한 곳이라도 상충 없이 일관될 것
- `contracts/` 산출 책임이 "기록자", "생성자", "검증자"를 구분해 남을 것
- `VERSION` 관련 문서 정합성은 유지되고, 현재 상태(레포 내 삭제, git 메타데이터 기반 표기)가 반영될 것
