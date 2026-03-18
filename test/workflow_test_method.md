# AxiomMd Workflow Skill 테스트 방법

## 1) 목적
이 문서는 AxiomMd 프로젝트에서 workflow skill 체인을 통한 spec 패키지 생성/검증 과정을 반복 가능한 방식으로 실행하기 위한 공통 테스트 방법을 정의한다.

## 2) 원칙
- 테스트는 단계별 산출물을 반드시 파일로 남긴다.
- 검증은 각 단계 후 즉시 수행한다.
- 실패가 발생한 단계에서 원인 경로를 기록하고 후속 판단으로 진행한다.
- 실행 결과는 재실행 이력과 비교를 위해 `logs/`에 누적한다.

## 3) 테스트 대상
- 대상 저장소: `/Users/axient/repository/AxiomMd`
- 실행 루트: `/Users/axient/repository/AxiomMd`
- 핵심 스펙: `/Users/axient/repository/AxiomMd/specs/features/FEAT-1001-workflow-skill-manager-cli`
- 스킬 소스: `/Users/axient/repository/AxiomMd/agent/skills`
- 스킬 설치 경로: `/Users/axient/repository/AxiomMd/.agents/skills`

## 4) 사전 점검
1. 명령 실행 환경
   - `cd /Users/axient/repository/AxiomMd`
   - `pwd`가 위 경로인지 확인
2. 스킬 설치 확인
   - `intake-normalizer`, `scope-router`, `feature-package-author`가 `.agents/skills/` 하위에 존재해야 함
3. 실행 증적 디렉토리 준비
   - `logs/` 폴더 존재 확인

## 5) 실행 단계

### 5.1 스킬 설치
1. 로컬 스킬 동기화
   - `rsync -a --delete /Users/axient/repository/AxiomMd/agent/skills/ /Users/axient/repository/AxiomMd/.agents/skills/`
2. 필수 스킬 존재 확인
   - `charter-blueprint-author`
   - `feature-package-author`
   - `intake-normalizer`
   - `manual-contract-compiler`
   - `package-readiness-review`
   - `reconcile-review`
   - `run-evidence-normalizer`
   - `scope-router`
   - `spec-writing-standard`

### 5.2 입력 정규화 준비
1. raw_input 스냅샷 파일 생성
   - 테스트 시작 시 사용한 raw_input 내용을 `docs` 또는 `logs`에서 별도 문서로 기록
2. 정규화 입력 생성
   - `python3 scripts/workflow_check.py packet input.packet.yaml`
3. 산출물 파일 확인
   - `input.packet.yaml`

### 5.3 라우팅 결정
1. 라우팅 실행
   - `python3 scripts/workflow_check.py route route.decision.yaml`
2. 산출물 파일 확인
   - `route.decision.yaml`

### 5.4 패키지 저작
1. 패키지 생성 실행
   - `python3 scripts/workflow_check.py package specs/features/FEAT-1001-workflow-skill-manager-cli`
2. 산출물 확인
   - `specs/features/FEAT-1001-workflow-skill-manager-cli/requirements.yaml`
   - `specs/features/FEAT-1001-workflow-skill-manager-cli/evals.yaml`
   - `specs/features/FEAT-1001-workflow-skill-manager-cli/tasks.yaml`

### 5.5 패키지 정합성 검증
1. 패키지 검증
   - `python3 scripts/workflow_check.py package specs/features/FEAT-1001-workflow-skill-manager-cli`
2. YAML 파싱 확인
   - 위 3개 패키지 파일이 YAML 파싱 가능한지 점검

## 6) PASS/FAIL 규칙
- PASS
  - 스킬 설치 완료
  - input.packet 생성 및 파싱 성공
  - route.decision 생성 및 파싱 성공
  - feature 패키지 생성 완료
  - package 체크 통과
- FAIL
  - 각 단계 산출물 누락
  - YAML 파싱 실패
  - schema 미준수(필수 필드 누락, 타입 불일치)
  - package 단계에서 생성 실패 또는 규칙 위반

## 7) 출력 산출물 정리
- `input.packet.yaml`
- `route.decision.yaml`
- `specs/features/FEAT-1001-workflow-skill-manager-cli/requirements.yaml`
- `specs/features/FEAT-1001-workflow-skill-manager-cli/evals.yaml`
- `specs/features/FEAT-1001-workflow-skill-manager-cli/tasks.yaml`
- 검증 로그(실행 표준 출력/에러)
- 비교 보고서

모든 실행 결과는 `logs/`에 타임스탬프 기반으로 저장해 누적한다.

## 8) 로그/보고 저장 규칙(권장)
- 파일명 형식: `logs/<stage>_<datetime>.<ext>`
- 예시: `logs/workflow_install_20260318-120000.txt`, `logs/packet_20260318-120000.txt`

## 9) 회귀 테스트 케이스(최소 집합)
- 정상 입력 기반 기본 케이스
- scope 불명확 문장 포함 케이스
- 제약 누락 케이스
- 동일 입력 중복 실행 케이스
- 기존 패키지 덮어쓰기/재생성 케이스
