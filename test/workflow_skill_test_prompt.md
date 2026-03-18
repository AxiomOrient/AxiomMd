# Workflow Skill 재현 테스트 컨텍스트 + 업그레이드 프롬프트 (v3)

- 실행일시(시드): 2026-03-18
- 목적: 스킬 설치부터 패키지 생성/검증까지 완전 재현 가능한 테스트를 정립하고, 중간 산출물 누락을 방지
- 대상 저장소: /Users/axient/repository/AxiomMd
- 핵심 대상 스펙: /Users/axient/repository/AxiomMd/specs/features/FEAT-1001-workflow-skill-manager-cli
- 표준 기준: /Users/axient/repository/AxiomMd/standards/spec-package-standard.md

## 1) 컨텍스트 스냅샷

- 실행 환경
  - cwd: /Users/axient/repository/AxiomMd
  - shell: zsh
  - timezone: Asia/Seoul
  - 사용자 경로: /Users/axient
- 스킬 소스
  - 로컬 스킬: /Users/axient/repository/AxiomMd/agent/skills
  - 설치 경로: /Users/axient/repository/AxiomMd/.agents/skills
- 필수 스킬
  - intake-normalizer
  - scope-router
  - feature-package-author
- 기존 기록
  - [workflow_spec_generation_test_log.md](/Users/axient/repository/AxiomMd/logs/workflow_spec_generation_test_log.md)
  - [workflow_spec_generation_comparison_report.md](/Users/axient/repository/AxiomMd/logs/workflow_spec_generation_comparison_report.md)

## 2) 테스트 정확도를 높이는 설계

- 운영 원칙: 실행 산출물은 logs 폴더에 타임스탬프 기반으로 누적한다. docs는 정적 가이드/기준 문서만 유지한다.
- 단계별 출력물을 반드시 파일로 남김
  - input.packet.yaml
  - route.decision.yaml
  - 최종 패키지 전체 (requirements.yaml, evals.yaml, tasks.yaml)
- 각 단계마다 pass/fail을 분리 기록
  - 설치/파서/라우팅/저자(패키지)/정합성 체크
- 음영 케이스를 추가
  - scope 불명확 케이스
  - 제약 누락 케이스
  - 중복 실행 케이스
  - 기존 산출물 덮어쓰기 케이스
- 결과를 표준 형식(코드블록/파일경로/실패 클래스)으로 저장해 재현성 강화

## 3) 권장 실행 흐름(직접 실행 템플릿)

### 3.1 Skill 설치

```bash
cd /Users/axient/repository/AxiomMd
mkdir -p .agents/skills logs
RUN_TS="$(date +%Y%m%d-%H%M%S)"

rsync -a --delete agent/skills/ .agents/skills/
for s in charter-blueprint-author feature-package-author intake-normalizer manual-contract-compiler package-readiness-review reconcile-review run-evidence-normalizer scope-router spec-writing-standard; do
  if [ ! -d .agents/skills/$s ]; then
    echo "[FAIL] missing skill: $s"
    exit 1
  fi
done
ls -1 .agents/skills > "logs/retest_installed_skills_${RUN_TS}.txt"
```

### 3.2 raw_input 스냅샷 기록

```bash
action_file="logs/retest_raw_input_snapshot_${RUN_TS}.md"
cat > "$action_file" <<EOF2
# Raw Input Snapshot
- capture_time: 2026-03-18
- user_intent: workflow/skill 관리 기능을 가진 Rust CLI spec 패키지 생성
- constraints: local-only, feature package output, 검증+export 지원
- scope_in:
  - workflow, skill 엔티티 CRUD
  - 패키지 템플릿 생성/검증
- scope_out:
  - 웹 UI
  - 원격 API 서버
EOF2
```

### 3.3 intake-normalizer + scope-router

```bash
# input.packet 생성 후 검증
python3 scripts/workflow_check.py packet input.packet.yaml | tee "logs/retest_caseA_packet_${RUN_TS}.txt"
cp -f input.packet.yaml "logs/retest_caseA_input.packet_${RUN_TS}.yaml"
if [ ! -s "logs/retest_caseA_input.packet_${RUN_TS}.yaml" ]; then
  echo "[FAIL] missing or empty input packet artifact"
  exit 1
fi

# route.decision 생성 후 검증
python3 scripts/workflow_check.py route route.decision.yaml | tee "logs/retest_caseA_route_${RUN_TS}.txt"
cp -f route.decision.yaml "logs/retest_caseA_route.decision_${RUN_TS}.yaml"
if [ ! -s "logs/retest_caseA_route.decision_${RUN_TS}.yaml" ]; then
  echo "[FAIL] missing or empty route artifact"
  exit 1
fi
```

### 3.4 feature-package-author + 패키지 생성

```bash
python3 scripts/workflow_check.py package specs/features/FEAT-1001-workflow-skill-manager-cli | tee "logs/retest_caseA_package_${RUN_TS}.txt" || true
cp -f "specs/features/FEAT-1001-workflow-skill-manager-cli/requirements.yaml" "logs/retest_caseA_requirements_${RUN_TS}.yaml"
cp -f "specs/features/FEAT-1001-workflow-skill-manager-cli/evals.yaml" "logs/retest_caseA_evals_${RUN_TS}.yaml"
cp -f "specs/features/FEAT-1001-workflow-skill-manager-cli/tasks.yaml" "logs/retest_caseA_tasks_${RUN_TS}.yaml"
```

### 3.5 산출물 정합성 점검

```bash
python3 scripts/workflow_check.py package specs/features/FEAT-1001-workflow-skill-manager-cli
python3 - <<PY
import os
import yaml
from pathlib import Path

run_ts = os.environ.get("RUN_TS", "manual")
paths = [
    Path(f"logs/retest_caseA_input.packet_{run_ts}.yaml"),
    Path(f"logs/retest_caseA_route.decision_{run_ts}.yaml"),
    Path(f"logs/retest_caseA_requirements_{run_ts}.yaml"),
    Path(f"logs/retest_caseA_evals_{run_ts}.yaml"),
    Path(f"logs/retest_caseA_tasks_{run_ts}.yaml"),
]

for p in paths:
    if not p.exists():
        print(f"[MISS] {p}")
        continue
    try:
        yaml.safe_load(p.read_text())
        print(f"[PASS] yaml_parse: {p}")
    except Exception as e:
        print(f"[FAIL] yaml_parse: {p} :: {e}")
PY
```

## 4) 테스트 다양성 케이스

- 케이스 A: 기본 정상(raw_input 그대로)
- 케이스 B: scope 불명확 문장 추가 후 scope-router가 hold 또는 framing-first인지 확인
- 케이스 C: target_repo/feature_id 누락으로 INPUT_GAP 처리 유도
- 케이스 D: FEAT-1001 패키지 재생성 시 덮어쓰기 정책/id 충돌 처리 확인
- 케이스 E: 기존 검증 실패를 수정한 뒤 반복 실행해 회귀 여부 비교

## 5) 업그레이드 핵심 프롬프트 (복붙용)

아래 프롬프트를 그대로 실행 요청 텍스트로 사용해 주세요.

```text
당신은 /Users/axient/repository/AxiomMd에서 workflow skill 체인을 재현 테스트한다.
목표는 raw_input부터 최종 feature package까지 end-to-end 추적을 완전히 재현하고, 각 단계 output을 파일로 고정해 검증까지 완료하는 것이다.

전제:
1) 스킬 소스는 /Users/axient/repository/AxiomMd/agent/skills
2) 설치 경로는 /Users/axient/repository/AxiomMd/.agents/skills
3) 대상 스펙은 specs/features/FEAT-1001-workflow-skill-manager-cli
4) 모든 실행 산출물은 logs/로 기록하고 파일명은 run_ts 기반으로 남긴다.

실행 순서:
- 스킬 설치 검증
- raw_input 스냅샷 기록
- input.packet 생성 + workflow_check packet + logs 저장
- route.decision 생성 + workflow_check route + logs 저장
- feature-package-author 산출 실행
- 최종 패키지 생성 후 workflow_check package
- requirements/evals/tasks 파싱 점검

출력 형식:
- StageResult(install/intake/route/author/package)
- EvidencePath 목록
- FailureClass(없음/파싱실패/스키마미달/로직미달)
- ReproCommand 목록
- FinalPassRule: all_stages_pass && package_pass

회귀 케이스도 함께 수행:
- scope ambiguity, 제약 누락, 중복 실행, 기존 패키지 덮어쓰기

각 단계에서 중간 파일이 누락되면 즉시 멈추고 원인/다음 액션을 출력한다.
```

## 6) 결과 저장 정책

- 실행 산출물(로그/스냅샷/패킷/라우트/리포트)은 logs 폴더에 버전 라벨(타임스탬프)로 누적한다.
- 문서 템플릿이나 절차 설명은 docs 폴더에 유지한다.
- 최종 비교 보고는 logs/workflow_spec_generation_comparison_report.md 형식을 확장해 _v2 또는 RUN_TS로 분리 저장한다.
