# Workflow Schema Set

`agent/workflows/`는 선언형 실행 정의를 담고, `scripts/workflow_runner.py`는 이를 정합성 측면에서 검증합니다.

## Files

- `workflow.schema.yaml`: workflow 정의의 정적 스키마
- `pipeline.schema.yaml`: pipeline 정의의 정적 스키마
- `condition-grammar.md`: pipeline 조건식 문법

## Validation Order

- YAML parse
- 스키마 검사 (`workflow.schema.yaml` / `pipeline.schema.yaml`)
- 링크 검사: workflow id/pipeline stage 존재성
- 링크 검사: condition 참조 대상이 선행 아티팩트/허용 입력 또는 prior stage outputs인지
- 링크 검사: 정책 경로/skill 경로 존재성
- 실행 계획 모드에서는 실제 파일 write/skill 호출 없이 plan만 출력

## Tooling

- `python scripts/workflow_runner.py validate workflow agent/workflows/authoring/intake-and-routing.yaml`
- `python scripts/workflow_runner.py validate pipeline agent/workflows/pipelines/authoring.yaml`
- `python scripts/workflow_runner.py validate manifests`
- `python scripts/workflow_runner.py simulate pipeline agent/workflows/pipelines/full-cycle.yaml --dry-run`
