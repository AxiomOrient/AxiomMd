# Skill Authoring Guide — 새 스킬 작성 가이드

새로운 Codex Skill을 처음부터 작성하는 단계별 가이드.

---

## 사전 체크

스킬을 작성하기 전에 다음을 확인한다:

- [ ] 이 워크플로우를 수행하는 기존 스킬이 없는가?
- [ ] 이 워크플로우가 반복적으로 사용되는가? (일회성이면 스킬이 불필요하다)
- [ ] 입력과 출력이 명확히 정의되는가?
- [ ] AI가 혼자 실행할 수 있는 워크플로우인가?

---

## Step 1: 스킬 이름 결정

**형식**: `kebab-case`, 동사-명사 또는 명사 구조

```
intake-normalizer       ← 동사-명사 (권장)
spec-writing-standard   ← 명사구
package-readiness-review ← 명사구
babysit-pr              ← 동사-명사
```

**규칙**:
- 소문자 + 하이픈만 사용한다.
- 너무 일반적인 이름은 피한다 (`helper`, `tool`, `util` 금지).
- 스킬이 하는 일을 이름에서 직접 알 수 있어야 한다.

---

## Step 2: 디렉터리 구조 생성

```bash
mkdir -p agent/skills/<skill-name>/agents
mkdir -p agent/skills/<skill-name>/assets
mkdir -p agent/skills/<skill-name>/references
mkdir -p agent/skills/<skill-name>/scripts
```

스크립트, assets, references가 없다면 해당 디렉터리를 만들지 않는다.

---

## Step 3: `SKILL.md` 작성

이것이 가장 중요한 단계다.

### 3-1. Frontmatter 작성

```yaml
---
name: <skill-name>
description: <선택 기준. 언제 사용하는가, 무엇을 입력받는가, 무엇을 출력하는가를 포함한 1-3문장>
---
```

**description 작성 방법**:
1. "Use when..." 또는 "Use this skill when..." 으로 시작한다.
2. 입력 형태를 언급한다.
3. 출력 형태를 언급한다.
4. 사용하면 안 되는 경우를 추가한다.

### 3-2. Workflow 작성

가장 먼저 워크플로우를 번호 리스트로 초안 작성한다:

```
1. 무엇을 먼저 읽는가?
2. 어떤 판단을 내리는가?
3. 무엇을 쓰는가?
4. 어떻게 검증하는가?
5. 언제 멈추는가?
```

각 단계를 하나의 행동으로 표현한다. 단계가 여러 행동을 포함하면 분리한다.

### 3-3. Stop Conditions 정의

중단 조건이 없는 스킬은 완성되지 않은 스킬이다.
다음 질문으로 stop condition을 도출한다:

- 입력이 불충분하면 어떻게 되는가?
- 외부 의존성(API, 파일)이 없으면?
- 결과가 검증에 실패하면?
- 사용자 결정이 필요한 상황은?

---

## Step 4: `agents/openai.yaml` 작성

```yaml
interface:
  display_name: "<Human-Readable Name>"
  short_description: "<한 줄, 마침표 없음>"
  default_prompt: "Use $<skill-name> to <구체적인 행동>."
```

**체크리스트**:
- [ ] `display_name`은 2–5 단어인가?
- [ ] `short_description`은 10 단어 이내인가?
- [ ] `default_prompt`는 `$<skill-name>` 참조를 포함하는가?
- [ ] `default_prompt`는 Codex가 즉시 실행 가능한가?

---

## Step 5: Assets 작성 (해당하는 경우)

### 입력 패킷 (`input.packet.yaml`)

스킬이 구조화된 입력을 받는다면:

```yaml
# input.packet.yaml
request_summary: ""
scope:
  in: []
  out: []
constraints: []
done_signals: []
open_questions: []
```

### 체크리스트 (`<name>-checklist.md`)

AI가 완료 기준으로 사용할 체크리스트:

```markdown
# <Skill> Checklist

## Required Fields

- [ ] request_summary is not empty
- [ ] scope.in has at least one item
- [ ] done_signals are measurable

## Quality Gates

- [ ] no placeholder values remain
- [ ] open_questions are documented, not guessed
```

### 출력 템플릿 (`<name>-template.md`)

스킬이 보고서나 문서를 생성한다면 템플릿을 제공한다.

---

## Step 6: References 작성 (해당하는 경우)

스킬이 복잡한 판단 기준을 포함한다면 `references/` 에 분리한다.

**휴리스틱 파일** (`heuristics.md`):
```markdown
# <Skill> Heuristics

## Decision Tree

1. If X: do A
2. If Y: do B
3. If uncertain: do C before choosing

## Classification Criteria

Treat as TYPE_A when:
- criterion 1
- criterion 2

Treat as TYPE_B when:
- criterion 1
- criterion 2
```

---

## Step 7: Python 스크립트 작성 (해당하는 경우)

스킬이 자동화된 검사나 외부 API 호출이 필요하다면:

```python
#!/usr/bin/env python3
"""
<Skill Name> 스크립트.

목적: <무엇을 하는가>
사용법: python3 scripts/<script-name>.py --option value
"""

import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="<설명>")
    parser.add_argument("--input", required=True, help="입력 파일 경로")
    parser.add_argument("--once", action="store_true", help="한 번만 실행")
    return parser.parse_args()


def main():
    args = parse_args()
    # 로직 구현
    pass


if __name__ == "__main__":
    main()
```

SKILL.md의 `## Commands` 섹션에 실행 방법을 반드시 문서화한다.

---

## Step 8: 자체 검토

완성 후 다음을 확인한다:

### 필수 파일 체크
- [ ] `SKILL.md` 존재하고 frontmatter가 유효한가?
- [ ] `agents/openai.yaml` 존재하고 세 필드가 모두 있는가?

### SKILL.md 품질 체크
- [ ] `description`은 선택 기준을 포함하는가?
- [ ] Workflow가 번호 순서로 작성되었는가?
- [ ] Stop Conditions가 정의되었는가?
- [ ] 참조 파일이 실제로 존재하는가?

### Naming 체크
- [ ] `name` 값이 디렉터리명과 동일한가?
- [ ] `$<skill-name>` 참조가 `default_prompt`에 있는가?

### Script 체크 (스크립트가 있을 때)
- [ ] Python 3 전용인가?
- [ ] `#!/usr/bin/env python3` shebang이 있는가?
- [ ] `argparse`로 CLI를 정의했는가?
- [ ] SKILL.md에 실행 명령어가 문서화되었는가?

---

## 완성된 스킬 예시: `scope-router`

```
agent/skills/scope-router/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── route.decision.yaml
│   └── routing-checklist.md
└── references/
    └── ROUTING_RULES.md
```

이 스킬은 스크립트 없이 문서만으로 완성된 단순한 스킬의 예시다.
