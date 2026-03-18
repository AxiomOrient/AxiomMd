# PRD: axm — Workflow-Skill Spec Compiler (Rust CLI)

**Version**: 0.2
**Date**: 2026-03-18
**Status**: Draft

---

## 1. Executive Summary

`axm`은 AxiomMd의 workflow와 skill을 연계하여 raw input을 implementation-ready feature spec으로 자동 생성하는 **Rust CLI 오케스트레이터**다.

사람이 raw brief를 주면, `axm`이 workflow 순서에 따라 각 단계에 맞는 skill을 AI 에이전트(codex / gemini / claude code)에 디스패치하고, 에이전트가 skill의 I/O 계약을 따라 template 형식의 spec 파일을 생성한다. `axm`은 각 단계의 출력을 검증하고 다음 단계로 파이프한다.

**핵심 가치**:
- **정확한 spec 자동 생성**: 모호한 산문이 아니라 구체적이고 연결된 spec 파일 세트가 나온다
- **워크플로우-스킬 부드러운 연계**: 사람이 pipeline 순서와 skill 선택을 기억할 필요 없다
- **I/O 계약 준수 보장**: 각 단계의 출력이 다음 단계의 입력 조건을 항상 만족한다

---

## 2. 핵심 동작 원리

```
raw input (brief, PRD, meeting note)
    ↓
[axm: intake-and-routing workflow]
    → intake-normalizer skill → AI agent → input.packet.yaml
    → scope-router skill      → AI agent → route.decision.yaml
    ↓
[axm: framing workflow, if route = framing-first]
    → charter-blueprint-author skill → AI agent → product-charter.md, system-blueprint.md
    ↓
[axm: feature-package-authoring workflow]
    → feature-package-author skill → AI agent → feature package file set (11 files)
    ↓
[axm: readiness-and-handoff workflow]
    → package-readiness-review skill → AI agent → readiness-report.md, handoff.packet.yaml
    ↓
OUTPUT: implementation-ready spec package
```

각 화살표에서 `axm`은:
1. skill의 SKILL.md + assets/ + references/ 를 컨텍스트로 구성
2. AI 에이전트에 디스패치
3. 출력 파일이 artifact contract를 만족하는지 검증
4. HILT 조건이면 정지 → 사람 확인 → 재개

---

## 3. Problem Statement

| 사용자 | 현재 고통 | 영향 |
|---|---|---|
| 방법론 사용자 | workflow 4개 × skill 9개의 I/O 순서를 수동으로 관리 | 단계 누락, artifact 불일치가 빈번 |
| AI 에이전트 호출자 | 각 skill에 맞는 컨텍스트(SKILL.md + assets)를 매번 수동 구성 | 프롬프트 품질이 일정하지 않아 spec 내용이 불명확하고 모호함 |
| CI/CD 팀 | spec 생성과 검증을 파이프라인에 삽입할 CLI 없음 | 게이트 없이 구현으로 진입 |
| 멀티 프로덕트 팀 | product profile(axiom-v1 등)을 generic kernel에 수동 연결 | profile drift, 파일 형식 불일치 |

**핵심 문제**: 좋은 skill 정의와 template이 있어도, 그것을 **순서대로 AI에 공급하고 출력을 이어 주는 오케스트레이터**가 없어 spec 품질이 실행자 역량에 의존한다.

---

## 4. Goals & Metrics

### P0 — Authoring Pipeline (MVP)

| 목표 | 측정 지표 | 성공 기준 |
|---|---|---|
| intake → readiness 전 단계 자동 실행 | 샘플 brief 3개로 end-to-end 성공 | readiness status=`ready` 또는 `patch-required` 결과 나옴 |
| 각 skill의 I/O 계약 100% 준수 | artifact validator 통과율 | intake / route / package / readiness 4종 artifact 모두 통과 |
| 생성된 spec 내용의 구체성 | 명시적 ID 연결 완결성 | 모든 must req에 blocking eval 존재, 모든 task에 req_id 존재 |
| HILT 정지/재개 | HILT 조건 감지 → 정지 → 재개 흐름 | 정의된 HILT 조건 3종 모두 감지 |

### P1 — AI Agent 선택 최적화

| 목표 | 측정 지표 | 성공 기준 |
|---|---|---|
| Codex / Gemini / Claude 라우팅 | 단계별 에이전트 선택이 설정 가능 | `axm.toml`에서 skill별 에이전트 지정 |
| Product profile resolve | axiom-v1 profile manifest 자동 로드 | `--base-dir`로 AxiomSpecs 경로 지정 시 profile shape 자동 적용 |
| spec-writing-standard 연계 | AI-facing spec 품질 기준 자동 적용 | spec 초안이 AI_FACING_SPEC_WRITING_STANDARD 규칙 통과 |

### P2 — Closed Loop

| 목표 |
|---|
| Execution loop 지원 (execution-planning → reconcile-and-close) |
| watch 모드 — artifact 변경 감지 → 자동 재검증 |
| `workflow_runner.py`로 workflow/pipeline 정합성 분리, `workflow_check.py`로 artifact contract 유지 |

### Non-goals

- GUI/TUI 없음
- method/ 문서를 동적으로 파싱하여 workflow contract를 추론하지 않음 (skills/ + workflow/ 폴더가 runtime 소스)
- AI가 product-specific 아키텍처 결정을 자율적으로 내리지 않음
- spec 내용 자동 승인 없음 — 사람 review는 HILT 게이트로 강제됨

---

## 5. User Personas

### Persona 1. 스펙 작성자 (Alex)
- 클라이언트 brief를 feature package로 변환하는 PM/Lead Engineer
- 9개 skill의 I/O 형식과 순서를 매번 기억하기 어려움
- **원하는 것**: `axm run --input client-brief.md --output ./specs/FEAT-0012/` → 11개 spec 파일 자동 생성

### Persona 2. AI 에이전트 통합 개발자 (Jamie)
- codex / gemini를 spec 생성 파이프라인에 붙이려는 개발자
- 각 skill에 어떤 컨텍스트를 줘야 하는지, 출력을 어떻게 검증하는지 매번 구현
- **원하는 것**: `axm`이 skill context 구성 + AI 디스패치 + 출력 검증을 일관되게 처리

### Persona 3. CI 자동화 담당 (Morgan)
- feature branch에 spec이 포함됐는지 PR에서 자동 검사
- **원하는 것**: `axm check package ./specs/FEAT-0012/ --json` → exit code + JSON 결과

---

## 6. Functional Requirements

### FR-001. Skill Context Builder
- `agent/skills/<skill-name>/` 폴더에서 SKILL.md, assets/, references/ 파일을 읽어 AI 에이전트에 전달할 컨텍스트 패킷을 구성한다.
- 각 컨텍스트 패킷은 skill의 input contract, output contract, stop conditions, template을 포함해야 한다.
- **정확성 요건**: SKILL.md에 명시된 read paths와 write paths를 그대로 적용해야 하며, 임의 추가·생략 없음.

### FR-002. AI Agent Dispatcher
- 구성된 컨텍스트 패킷을 지정된 AI 에이전트(codex / gemini / claude code)에 전달하고 응답을 받는다.
- 에이전트 선택은 `axm.toml`의 skill별 설정 또는 `--agent` 플래그로 지정.
- 응답에서 write paths에 해당하는 파일을 추출하여 출력 디렉토리에 저장.
- 에이전트가 INPUT_GAP_REPORT 또는 stop condition을 반환하면 HILT 게이트로 라우팅.
- **지원 에이전트**: `codex`, `gemini`, `claude` (claude code CLI 경유)

### FR-003. Artifact Validator
- 생성된 artifact를 10개 artifact class 계약에 따라 검증한다:
  - `input.packet.yaml` — 최소 10개 필드 존재 여부
  - `route.decision.yaml` — 최소 7개 필드, route 값 유효성
  - `product-charter.md` — 5개 섹션 존재 여부
  - `system-blueprint.md` — 6개 섹션 존재 여부
  - feature package 11개 파일 — linkage 완결성 (req↔task↔eval)
  - `readiness-report.md` — gate 5개 존재 여부, status 명시
  - `handoff.packet.yaml` — 최소 9개 필드, stage·status 유효성
  - `execution.plan.yaml` — 최소 9개 필드
  - `evidence.result.json` — 최소 8개 필드
  - `reconcile.result.yaml` — 최소 9개 필드
- **linkage 검증**: 모든 must requirement → blocking eval 존재, 모든 task → req_id + eval_id 존재.
- 검증 실패 시: 누락 항목을 파일·필드·ID 단위로 구체적으로 출력.

### FR-004. Workflow Orchestrator
- 4개 authoring workflow를 ordered pipeline으로 실행:
  1. `intake-and-routing` → intake-normalizer + scope-router skills
  2. `framing` (route=framing-first일 때만) → charter-blueprint-author skill
  3. `feature-package-authoring` → feature-package-author skill
  4. `readiness-and-handoff` → package-readiness-review skill
- 각 workflow는 required input file이 존재하는지 확인 후 실행.
- 각 workflow 완료 후 FR-003 검증을 통과해야 다음 단계로 진행.
- **재개 지원**: 중단 지점부터 재개 가능 (`axm resume --stage <workflow> --dir <path>`).

### FR-005. HILT Gate
- 각 workflow의 HILT 조건을 자동 감지하고 정지:
  - `intake-and-routing`: scope 불명확, non-goal 없음, open question이 핵심 blocking
  - `framing`: 목표-비목표 충돌, feature split 기준 미합의
  - `feature-package-authoring`: destructive/privileged 행동 포함, verification ownership 불명확
  - `readiness-and-handoff`: status=`hold`, high-risk + approval rule 없음
- 정지 시: 이유와 필요한 사람 확인 내용을 구체적으로 출력.
- `axm resume` 명령으로 확인 후 재개.

### FR-006. Template Engine
- `agent/skills/<skill>/assets/` 폴더의 template 파일을 기반으로 출력 파일의 skeleton을 생성.
- AI 에이전트에게 template skeleton을 초기 구조로 제공하여 형식 일탈 방지.
- **패키지 스켈레톤**: `package-skeleton.md`의 11개 파일 형식을 그대로 적용.

### FR-007. Product Profile Resolver
- `package.yaml`의 `profile_key`를 읽어 product repo의 profile manifest를 resolve.
- Manifest 위치: `<base-dir>/profiles/<profile_key>/` (기본: `profiles/axiom-v1/package-and-readiness.shape.yaml`)
- `--base-dir` 플래그로 product repo(AxiomSpecs) 경로 지정.
- Generic required fields 검증 후 local overlay 검증 순서로 적용.
- Profile manifest가 없으면 generic-only 검증으로 폴백, 경고 출력.

### FR-008. Artifact Check Commands
- `axm check packet <path>` — input.packet.yaml 검증
- `axm check route <path>` — route.decision.yaml 검증
- `axm check package <dir> [--base-dir <path>]` — feature package 검증
- `axm check handoff <path>` — handoff.packet.yaml 검증
- `axm check pipeline <dir>` — 전체 authoring path artifact 일관성 검증
- `--strict` 모드: warning을 error로 승격
- `--json` 모드: machine-readable JSON 출력, exit code (0=ready / 1=patch-required / 2=hold / 3=error)

### FR-009. Skill Bundle Validator
- `axm validate skill <skill-dir>` — skill bundle의 Gate 1·2·3 자동 검사
  - Gate 1: SKILL.md + assets/ + references/ 존재 여부
  - Gate 2: SKILL.md에 명시된 경로가 실제 파일과 일치, stop condition 명시 여부
  - Gate 3: source commit, handoff completeness
- 결과: gate별 pass/fail + 누락 항목 목록.

### FR-010. Configuration
- `axm.toml` (프로젝트 루트 또는 `--config` 플래그):
  ```toml
  skills_dir = "agent/skills"
  templates_dir = "templates"
  output_dir = "output"
  base_dir = "../AxiomSpecs"    # product repo 경로

  [agents]
  intake-normalizer   = "claude"
  scope-router        = "gemini"
  charter-blueprint-author = "gemini"
  feature-package-author   = "codex"
  package-readiness-review = "claude"
  ```
- 환경 변수로 오버라이드: `AXM_BASE_DIR`, `AXM_AGENT_DEFAULT`

---

## 7. Architecture Overview

```
axm (Rust binary)
├── cmd/                    # CLI 진입점 (clap)
│   ├── run                 # workflow pipeline 실행
│   ├── check               # artifact 검증
│   ├── validate            # skill bundle 검증
│   └── resume              # HILT 이후 재개
├── skill/
│   ├── loader.rs           # agent/skills/<name>/ 폴더 파싱
│   └── context_builder.rs  # SKILL.md + assets + references → context packet
├── agent/
│   ├── codex.rs            # codex CLI 어댑터
│   ├── gemini.rs           # gemini CLI 어댑터
│   └── claude.rs           # claude code CLI 어댑터
├── workflow/
│   ├── pipeline.rs         # 4-step authoring path 오케스트레이션
│   ├── hilt.rs             # HILT 조건 감지 및 정지/재개
│   └── state.rs            # workflow 진행 상태 (재개용)
├── artifact/
│   ├── validator.rs        # 10개 artifact class 검증
│   ├── linkage.rs          # req↔task↔eval linkage 완결성 검사
│   └── template.rs         # skeleton 생성
├── profile/
│   └── resolver.rs         # product profile resolve + overlay 검증
└── report/
    ├── human.rs            # 사람용 출력
    └── json.rs             # machine-readable JSON 출력
```

**핵심 의존성**:
- `clap` — CLI 파싱
- `serde` + `serde_yaml` + `serde_json` — artifact 직렬화
- `pulldown-cmark` — Markdown 파싱 (SKILL.md, template)
- `tokio` — 비동기 CLI 프로세스 실행 (AI 에이전트 어댑터)
- `notify` — watch 모드 (P2)

---

## 8. AI Agent 라우팅 전략

| Skill | 기본 에이전트 | 이유 |
|---|---|---|
| `intake-normalizer` | claude | 자연어 분석 + 구조화 |
| `scope-router` | gemini | 큰 컨텍스트 분석, 판단 |
| `charter-blueprint-author` | gemini | 장문 분석 + 구조화 |
| `feature-package-author` | codex | 코드 인접 파일 생성, 반복 구조 |
| `package-readiness-review` | claude | 계약 준수 검토, 판정 |
| `spec-writing-standard` | claude | spec 품질 기준 적용 |

모두 `axm.toml`에서 오버라이드 가능.

---

## 9. Product Profile Manifest 위치

```
<AxiomSpecs 또는 product repo>/
└── profiles/
    └── axiom-v1/
        ├── manifest.yaml                    # profile_key, version, shape rules
        ├── package-and-readiness.shape.yaml # package metadata shape + readiness rules
        └── examples/
            └── sample-package.yaml
```

`axm --base-dir ../AxiomSpecs`로 resolve. manifest가 없으면 generic-only 검증으로 폴백.

---

## 10. Implementation Phases

### Phase 1 — Core Check (2주)
```
FR-008 (artifact check commands + workflow_runner.py 정적 검증)
FR-003 (artifact validator)
FR-009 (skill bundle validator)
```
완료 조건: 기존 `workflow_check.py`(artifact contract 검사) 항목 재현 + `workflow_runner.py`(workflow/pipeline 정합성) 항목 통합.

### Phase 2 — Authoring Pipeline (3주)
```
FR-001 (skill context builder)
FR-002 (AI agent dispatcher: codex + gemini + claude)
FR-004 (workflow orchestrator)
FR-005 (HILT gate)
FR-006 (template engine)
FR-010 (configuration)
```
완료 조건: raw brief 3개 입력 → readiness-report.md + 11개 feature package 파일 end-to-end 생성 성공.

### Phase 3 — Profile & Quality (2주)
```
FR-007 (product profile resolver)
spec-writing-standard skill 연계
```
완료 조건: axiom-v1 profile로 생성된 package가 AxiomSpecs 검사 통과.

---

## 11. Risks & Mitigations

| 위험 | 확률 | 영향 | 완화 전략 |
|---|---|---|---|
| AI 에이전트가 SKILL.md 계약을 무시하고 임의 형식 생성 | 고 | 고 | template skeleton을 AI 입력에 포함 + FR-003 출력 검증; 실패 시 자동 retry 1회 후 HILT |
| skill assets/가 변경되어 context builder가 outdated | 중 | 중 | `axm validate skill`로 skill bundle integrity 상시 확인 가능 |
| codex/gemini/claude CLI 버전 불일치 | 중 | 중 | 각 어댑터에 minimum version 체크 + `axm doctor` 명령 |
| HILT 조건 false positive (과도한 정지) | 중 | 중 | HILT는 명시적 필드 기반 감지 우선, heuristic 보조; `--skip-hilt` 플래그 제공 |
| product profile 없을 때 생성된 spec이 product repo 검사 실패 | 중 | 중 | generic-only 검증 폴백 + 경고 출력; profile manifest 위치 규약 표준화 |
| 생성된 spec 내용이 모호함 (ID 없음, vague prose) | 중 | 고 | `spec-writing-standard` skill을 마지막 단계에 항상 적용; linkage validator가 ID 누락을 게이트 |

---

## 12. Open Questions (없음 — 모두 확인됨)

| # | 질문 | 답변 |
|---|---|---|
| 1 | binary 이름 | `axm` |
| 2 | method/ 문서 런타임 역할 | 원칙 참조용만, runtime source는 `agent/skills/` + `agent/policy/` + `agent/workflows/` |
| 3 | `workflow_check.py` 관계 | `check`는 artifact 계약 검증으로 유지, `workflow_runner.py`가 선언형 flow 검증 전담 |
| 4 | LLM 연동 scope | codex / gemini / claude code 모두 in scope |
| 5 | profile manifest 위치 | product repo `profiles/<profile-key>/` 하위 (`--base-dir`로 resolve) |

---

## PRD Self-Score

| 영역 | 점수 | 근거 |
|---|---|---|
| AI-Specific Optimization (25pts) | 24 | 에이전트 라우팅 전략, skill context building, HILT 패턴, I/O 계약 강제 |
| Traditional PRD Core (25pts) | 23 | 문제·목표·페르소나·비목표·위험 완비. P0 KPI 수치 일부 추정(-2) |
| Implementation Clarity (30pts) | 28 | FR 번호화, phase 분리, 아키텍처 + 모듈 목록, 의존성, 에이전트 라우팅 테이블 |
| Completeness (20pts) | 19 | 9개 skill, 4개 workflow, 10개 artifact class, profile 위치까지 전부 반영 |
| **Total** | **94/100** | |

---

*Generated: 2026-03-18*
