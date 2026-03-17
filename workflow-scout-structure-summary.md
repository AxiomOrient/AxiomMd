# workflow-scout-structure 정리 (2026-03-18)

## Context

- 요청 의도: `/Users/axient/repository/AxiomMd`의 현재 구조를 `scope-contract` + `structure-map`으로 정리하고, `VERSION` 삭제 반영을 반영함
- 실행한 skill: workflow-scout-structure
- 요청 대상: 저장소 전체 범위
- 적용 범위: `README`, `docs`, `agent/workflow`, `scripts`, `specs`, `templates`

## DRAFT_SCOPE_CONTRACT

- Goal: generic 방법론 저장소(AxiomMd)의 현재 경계, 책임, 상호작용을 재설계 없이 진실 기반으로 정리한다.
- Scope in: `agent/workflow/` 정책 경계, workflow I/O/validator 템플릿 규약, feature package 표준과 feature package 스캐폴드 산출물.
- Scope out: 제품별 feature 구현/실행 저장소, CI/CD 파이프라인 실행 상세, 코드 수준 구현.
- Acceptance boundary: 정합성 현황과 미해결 구조 질문을 경계별로 분리해 남기고, 문서 기반 오케스트레이션과 실행 진입점 부재 상태를 구분한다.

## BOUNDARY_MAP

### policy-package boundary

- Responsibility: spec 저변의 최소 실행 계약, 역할, 평가, 에스컬레이션의 경계 고정.
- Interaction: docs/scripts/templates의 실행 규약이 지켜질 운영 규칙을 책임.
- Evidence: [agent/workflow/README.md](/Users/axient/repository/AxiomMd/agent/workflow/README.md), [agent/workflow/WORKFLOW.md](/Users/axient/repository/AxiomMd/agent/workflow/WORKFLOW.md), [agent/workflow/ROLE_POLICY.md](/Users/axient/repository/AxiomMd/agent/workflow/ROLE_POLICY.md), [agent/workflow/EVAL_POLICY.md](/Users/axient/repository/AxiomMd/agent/workflow/EVAL_POLICY.md), [agent/workflow/ESCALATION_POLICY.md](/Users/axient/repository/AxiomMd/agent/workflow/ESCALATION_POLICY.md), [agent/workflow/SELF_REVIEW.md](/Users/axient/repository/AxiomMd/agent/workflow/SELF_REVIEW.md)

### artifact contract boundary

- Responsibility: input/route/handoff/feature package 검증기의 형식 강제.
- Interaction: 템플릿이 키 스펙을 충족할 때 검증 pass 가능.
- Evidence: [scripts/check_input_packet.rb](/Users/axient/repository/AxiomMd/scripts/check_input_packet.rb), [scripts/check_route_decision.rb](/Users/axient/repository/AxiomMd/scripts/check_route_decision.rb), [scripts/check_handoff_packet.rb](/Users/axient/repository/AxiomMd/scripts/check_handoff_packet.rb), [scripts/check_feature_package.rb](/Users/axient/repository/AxiomMd/scripts/check_feature_package.rb), [templates/input.packet.yaml](/Users/axient/repository/AxiomMd/templates/input.packet.yaml), [templates/route.decision.yaml](/Users/axient/repository/AxiomMd/templates/route.decision.yaml), [templates/handoff.packet.yaml](/Users/axient/repository/AxiomMd/templates/handoff.packet.yaml)

### feature package scaffold boundary

- Responsibility: feature 패키지 최소 파일 구조와 계약 부록(`contracts/`) 산출물 제시.
- Interaction: check_feature_package가 요구하는 필수 파일 집합과 매핑.
- Evidence: [specs/SPEC_PACKAGE_STANDARD.md](/Users/axient/repository/AxiomMd/specs/SPEC_PACKAGE_STANDARD.md), [templates/feature/package.yaml](/Users/axient/repository/AxiomMd/templates/feature/package.yaml), [templates/feature/contracts/openapi.yaml](/Users/axient/repository/AxiomMd/templates/feature/contracts/openapi.yaml), [templates/feature/requirements.yaml](/Users/axient/repository/AxiomMd/templates/feature/requirements.yaml), [templates/feature/decisions.jsonl](/Users/axient/repository/AxiomMd/templates/feature/decisions.jsonl)

### protocol and workflow boundary

- Responsibility: workflow 단계 입출력 계약 및 sample run 기준 고정.
- Interaction: feature 작성/검증 절차의 최소 규약을 문서로 고정.
- Evidence: [docs/10_WORKFLOW_IO_PROTOCOL.md](/Users/axient/repository/AxiomMd/docs/10_WORKFLOW_IO_PROTOCOL.md), [docs/11_CLIENT_INTENT_TO_SPEC_WORKFLOW.md](/Users/axient/repository/AxiomMd/docs/11_CLIENT_INTENT_TO_SPEC_WORKFLOW.md), [docs/12_SPEC_AUTHORING_WORKFLOW_SET.md](/Users/axient/repository/AxiomMd/docs/12_SPEC_AUTHORING_WORKFLOW_SET.md)

### execution orchestration boundary

- Responsibility: workflow/validator를 실제로 실행하는 런처 또는 orchestration 제공.
- Interaction: 현재 레포 내부에서는 실행 진입점이 없어 외부 런처 의존으로 판단.
- Evidence: `find /Users/axient/repository/AxiomMd -maxdepth 4 -type f -name 'Makefile' -o -name 'Taskfile' -o -name 'Rakefile' -o -path '*/.github/workflows/*' -o -name 'package.json' -o -name 'pyproject.toml'` (결과 없음), [agent/workflow/WORKFLOW.md](/Users/axient/repository/AxiomMd/agent/workflow/WORKFLOW.md), [README.md](/Users/axient/repository/AxiomMd/README.md)

## DECISION_RECORD

- 결론: [agent/workflow/README.md](/Users/axient/repository/AxiomMd/agent/workflow/README.md)의 `VERSION` 누락은 정합성 오류가 아니라 삭제 반영 상태로 판단.
- 수정 결과: `VERSION` 항목을 Included Files에서 제거하고, 버전 표기 규칙을 `git` 태그/커밋 기반으로 안내.

## OPEN_STRUCTURE_QUESTIONS

- 샘플 런 실행 주체가 이 레포 외부 어디인지 아직 문서에서 구체적으로 명시되지 않음
  - Cheapest check: `/Users/axient/repository`에서 이 저장소의 workflow를 호출하는 명령/런처(예: skill bundle/runner) 1건 연결
- contracts 디렉터리 스캐폴딩 시점이 템플릿/검증 문서에서 명시되지 않음
  - Cheapest check: `templates/feature/contracts/openapi.yaml` 기반의 생성 단계가 문서로 표기된 최초 위치 1곳 탐색
- 샘플 run에서 “어느 단계까지 강제 실행되는지”가 실행 주체 미정
  - Cheapest check: 현재 3문서(`docs/10_WORKFLOW_IO_PROTOCOL.md`, `docs/11_CLIENT_INTENT_TO_SPEC_WORKFLOW.md`, `docs/12_SPEC_AUTHORING_WORKFLOW_SET.md`)에 sample run 수행 주체 한 줄 보강

## EXPANDED_ATOMIC_PATH

- `scout-scope-contract`
- `scout-structure-map`
- `scout-structure-map -> policy/package/validator boundary 분해`
- `scout-structure-map -> execution orchestration 부재 확인`

## Summary

- 본 저장소는 메서드·프로토콜·템플릿·검증기 자체는 잘 정합된 상태
- 다만 실행 오케스트레이션은 현재 레포 내에 존재하지 않아, 실무 실행/샘플런의 실제 진입점은 외부 문맥(런타임 skill/배포 파이프라인)에 의존
- 다음 단계는 `실행 주체`와 `샘플 런 주입점`만 좁히면 `완전한 실행 체인` 문서화가 완료됨
