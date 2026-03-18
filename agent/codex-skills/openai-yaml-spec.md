# `openai.yaml` 완전 스펙

Codex Skills에서 `agents/openai.yaml`은 스킬의 **UI 인터페이스 레이어**를 정의한다.

---

## 전체 스키마

```yaml
interface:
  display_name: string    # [필수] UI에 표시되는 이름
  short_description: string  # [필수] 한 줄 설명
  default_prompt: string  # [필수] 기본 호출 프롬프트
```

현재 `interface` 키 하나만 존재하며, 그 아래 세 필드가 전부다.

---

## 필드 상세

### `interface.display_name`

- **타입**: string
- **필수**: 예
- **표시 위치**: Codex 스킬 목록, 스킬 선택 UI
- **길이**: 2–5 단어 권장
- **규칙**:
  - 명사구 형태로 작성한다 ("PR Babysitter", "Spec Writing Standard").
  - 동사로 시작하지 않는다.
  - 스킬의 역할을 명확히 표현한다.

**예시**:
```yaml
display_name: "PR Babysitter"
display_name: "Charter Blueprint Author"
display_name: "Package Readiness Review"
```

---

### `interface.short_description`

- **타입**: string
- **필수**: 예
- **표시 위치**: 스킬 목록의 서브텍스트
- **길이**: 한 문장, 10 단어 이내 권장
- **규칙**:
  - 스킬이 **무엇을 하는지** 설명한다 (어떻게 하는지가 아니라).
  - 마침표를 붙이지 않는다.
  - `SKILL.md`의 description과 유사하되 더 짧게 작성한다.

**예시**:
```yaml
short_description: "Watch PR CI, reviews, and merge conflicts"
short_description: "Write framing docs before feature split"
short_description: "Write specs and scoped artifacts"
```

---

### `interface.default_prompt`

- **타입**: string
- **필수**: 예
- **용도**: 사용자가 `$<skill-name>`으로 스킬을 직접 호출할 때 Codex에 전달되는 지시문
- **규칙**:
  - `$<skill-name>` 참조로 시작하거나 명시적으로 포함한다.
  - Codex가 즉시 실행 가능할 만큼 구체적이어야 한다.
  - 컨텍스트 힌트를 포함한다 (현재 브랜치, 현재 패킷 등).
  - 길어도 괜찮다 — 명확성이 우선이다.

**예시**:
```yaml
default_prompt: "Use $charter-blueprint-author to create product-charter.md and system-blueprint.md from the current normalized input packet."

default_prompt: "Babysit the current PR: monitor CI, reviewer comments, and merge-conflict status..."

default_prompt: "Use $spec-writing-standard to draft or upgrade an implementation-ready spec for this repo."
```

---

## 완전한 파일 예시

### 최소 유효 파일

```yaml
interface:
  display_name: "My Skill"
  short_description: "Do the thing"
  default_prompt: "Use $my-skill to accomplish the goal."
```

### 실제 예시 (`babysit-pr`)

```yaml
interface:
  display_name: "PR Babysitter"
  short_description: "Watch PR CI, reviews, and merge conflicts"
  default_prompt: "Babysit the current PR: monitor CI, reviewer comments, and merge-conflict status (prefer the watcher's --watch mode for live monitoring); fix valid issues, push updates, and rerun flaky failures up to 3 times. Keep exactly one watcher session active for the PR (do not leave duplicate --watch terminals running). If you pause monitoring to patch review/CI feedback, restart --watch yourself immediately after the push in the same turn. If a watcher is still running and no strict stop condition has been reached, the task is still in progress: keep consuming watcher output and sending progress updates instead of ending the turn. Continue polling autonomously after any push/rerun until a strict terminal stop condition is reached or the user interrupts."
```

---

## 파일 위치 규칙

```
<skill-name>/
└── agents/
    └── openai.yaml    ← 반드시 이 경로여야 한다
```

- 파일명은 반드시 `openai.yaml`이어야 한다.
- 디렉터리명은 반드시 `agents/`여야 한다.
- 다른 경로에 위치하면 Codex가 인식하지 못한다.

---

## 주의 사항

- 이 파일은 **UI 레이어 전용**이다. AI 실행 지침은 `SKILL.md`에만 작성한다.
- `default_prompt`가 길어도 파일 분리 없이 단일 문자열로 유지한다.
- 현재 스키마에는 `interface` 이외 다른 최상위 키가 없다. 임의로 추가하지 않는다.
