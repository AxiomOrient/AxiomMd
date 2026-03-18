# Spec Authoring Guide

## 이 문서는 무엇인가

Feature spec을 만들고 싶을 때 어떻게 하면 되는지,
처음부터 끝까지 실제 절차를 설명한다.

사용자가 직접 스크립트를 실행하지 않는다.
**사용자는 에이전트에게 스킬을 지정해서 요청한다.**
에이전트가 스킬 SKILL.md를 읽고, 검증까지 포함해서 작업을 수행한다.

---

## 사용자가 하는 일 (전체 요약)

```
1. raw input 작성  →  무엇을 만들고 싶은지 자유롭게 쓴다
2. 에이전트에게 요청  →  "이 내용으로 스펙 만들어줘"
3. 결과 확인  →  생성된 feature package를 검토한다
```

스크립트 실행, 검증 명령, 파일 이동 — 이 모든 것은 **에이전트가 한다**.

---

## raw_input에 무엇을 넣어야 하나

### 형식

형식은 자유롭다. 아래 중 어떤 것이든 된다.

- 요청 메시지 (한두 문단)
- 기획서나 PRD 발췌
- 미팅 노트
- Slack/Discord 스레드 요약
- 운영 이슈 설명

### 반드시 담겨야 하는 내용

에이전트가 스펙을 만들려면 아래를 raw_input에서 읽어낼 수 있어야 한다.
빠지면 에이전트가 `INPUT_GAP_REPORT`를 내고 멈춘다.

| 항목 | 설명 | 예시 |
|------|------|------|
| **무엇을 만드나** | 기능 이름 + 한 줄 요약 | "수동 실행 계약 — 에이전트가 goal을 받아 launch request를 생성하는 계약" |
| **범위 안** | 이번에 만드는 것 | "goal 구조 정의, launch request 스키마, validation 규칙" |
| **범위 밖** | 명시적으로 제외 | "실제 실행 엔진, UI, 스케줄링" |
| **제약 조건** | 기술/운영 제약 | "Rust 타입 안전, 외부 네트워크 호출 없음" |
| **완료 기준** | 언제 끝난 것인가 | "check_specs 통과, blocking eval 연결 완료" |
| **근거 자료** | 참고할 파일/문서 | "specs/README.md, docs/SERVICE_SPEC.md" |

### raw_input 예시 (짧은 경우)

```markdown
# 수동 실행 계약 기능 요청

에이전트가 goal.json을 받아서 launch_request.json을 생성하는 계약이 필요하다.

만드는 것:
- CompiledGoal 스키마
- LaunchRequest 스키마
- ExecutionBrief 스키마
- 입력 검증 규칙

만들지 않는 것:
- 실행 엔진 자체
- UI
- 스케줄러

제약:
- Rust 타입 시스템 기반
- 외부 서비스 호출 없음

완료 기준:
- 스키마 파일 3개 작성
- blocking eval 연결
- check_specs 통과

참고 파일:
- specs/README.md
- docs/03_SERVICE_SPEC.md
```

### raw_input 예시 (PRD 발췌 형태)

```markdown
# PRD 발췌 — Worker Launch Bridge

## 배경
현재 에이전트 실행 요청이 표준 형식 없이 각 컴포넌트마다 다르게 구현되어 있음.

## 목표
Worker 실행 요청을 표준화하는 launch bridge 계약 정의.

## 요구사항 (요약)
- WorkerLaunchRequest 스키마 정의
- WorkerLaunchResult 스키마 정의
- Codex thread 매핑 문서

## 비목표
- Worker 내부 구현
- 스케줄러

## 참고
- 현재 Axiom 실행 모델: specs/features/FEAT-0001-manual-execution-contract
```

---

## 전체 흐름

### 경로 선택

에이전트(scope-router)가 raw_input을 보고 경로를 자동 판단한다.

```
요청이 좁고 명확하다  →  Direct Path  (바로 feature package 작성)
요청이 넓거나 모호하다  →  Framing Path  (먼저 제품 방향 정리 후 작성)
```

### Direct Path (대부분의 경우)

```
사용자: raw_input.md 작성 후 에이전트에게 요청

에이전트 작업:
  1. intake-normalizer  →  input.packet.yaml 생성
                           workflow_check.py packet 검증
  2. scope-router       →  route.decision.yaml 생성
                           workflow_check.py route 검증
  3. feature-package-author  →  feature package 11개 파일 생성
                                workflow_check.py package 검증
  4. package-readiness-review  →  readiness-report.md 생성
                                   handoff.packet.yaml 생성
                                   workflow_check.py handoff 검증

사용자: 생성된 feature package 검토
        → ready: 구현 착수 가능
        → patch-required: 에이전트에게 수정 요청
        → hold: 근본 이슈 해결 필요
```

### Framing Path (요청이 넓을 때)

```
사용자: raw_input.md 작성 후 에이전트에게 요청

에이전트 작업:
  1. intake-normalizer  →  input.packet.yaml
  2. scope-router       →  route.decision.yaml (route: framing-first)
  3. charter-blueprint-author  →  product-charter.md
                                   system-blueprint.md
                                   handoff.packet.yaml
                                   workflow_check.py framing 검증

  사용자: framing 결과 확인 후 계속 요청

  4. feature-package-author  →  feature package
  5. package-readiness-review  →  readiness verdict
```

---

## 에이전트에게 요청하는 방법

### 처음부터 끝까지 한 번에

```
"raw_input.md 내용을 바탕으로 스펙 만들어줘.
intake-normalizer, scope-router, feature-package-author,
package-readiness-review 스킬 순서로 사용해서
AxiomSpecs에 feature package 완성해줘."
```

### 단계별로

```
# 1단계
"raw_input.md를 intake-normalizer 스킬로 정규화해줘."

# 2단계
"scope-router 스킬로 route 결정해줘."

# 3단계
"feature-package-author 스킬로 FEAT-xxxx 패키지 만들어줘."

# 4단계
"package-readiness-review 스킬로 FEAT-xxxx 검토해줘."
```

### 특정 스킬만

```
"package-readiness-review 스킬로
specs/features/FEAT-0004-evidence-reconcile-loop 검토해줘."
```

---

## 생성되는 파일 (feature package)

에이전트가 `specs/features/FEAT-xxxx-slug/` 아래에 생성한다.

| 파일 | 역할 |
|------|------|
| `intent.md` | 왜 만드나 (문제, 목표) |
| `requirements.yaml` | 무엇을 해야 하나 (must/should/nice) |
| `design.md` | 어떻게 만드나 (경계, 컴포넌트, 실패 모드) |
| `evals.yaml` | 어떻게 검증하나 (blocking/non-blocking) |
| `tasks.md` | 구현 단위 (req/eval 연결) |
| `invariants.yaml` | 항상 지켜야 할 조건 |
| `risks.yaml` | 위험 요소 |
| `decisions.jsonl` | 설계 결정 이력 |
| `package.yaml` | 메타데이터 (id, state, proof_state) |
| `slices.yaml` | 실행 단위 (구현 착수 시 사용) |
| `contracts/` | 스키마, 계약 파일 |

---

## 검증은 에이전트가 한다

사용자가 직접 검증 명령을 실행할 필요 없다.
각 스킬 SKILL.md에 검증 단계가 포함되어 있고, 에이전트가 따른다.

```
feature-package-author 작업 완료
  → 자동: workflow_check.py package <feature-dir> --base-dir <AxiomSpecs>
  → 오류 있으면: 에이전트가 자체 수정 후 재검증
  → pass 후: 다음 단계로 이동
```

직접 확인하고 싶을 때만:

```bash
python scripts/workflow_check.py package specs/features/FEAT-xxxx-slug/ --base-dir /path/to/AxiomSpecs
python scripts/workflow_check.py pipeline ./my-workflow-dir/ --base-dir /path/to/AxiomSpecs
```

---

## readiness 결과 해석

| 결과 | 의미 | 다음 행동 |
|------|------|----------|
| `ready` | 구현 착수 가능 | 구현 에이전트에게 패키지 전달 |
| `patch-required` | 수정 필요 항목 있음 | 에이전트에게 "readiness-report.md 보고 수정해줘" |
| `hold` | 근본 이슈 존재 | raw_input부터 다시 검토 |

---

## 앞으로 개선할 부분

### 단기 (지금 바로 가능)

- raw_input 작성 후 **한 번의 요청**으로 끝내기
  (`"스펙 전체 만들어줘"` → 에이전트가 4단계 자동 진행)
- framing 단계는 에이전트가 필요 여부를 자체 판단
- readiness까지 자동으로 이어지도록 요청

### 중기

- feature package 핵심 4개 파일(intent, requirements, design, evals) 먼저 완성
  → 나머지는 구현 전 보충
- 검증 실패 시 에이전트 자동 재시도 루프

### 장기 (프로토콜 안정화 후)

- 단일 CLI (`axiom spec create raw_input.md`)
- 중간 단계 파일은 숨기고 최종 feature package만 노출
- 상태 추적 (어느 단계까지 완료됐는지 한눈에)
