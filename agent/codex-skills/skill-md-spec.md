# `SKILL.md` 완전 스펙

`SKILL.md`는 Codex Skills에서 **가장 중요한 파일**이다.
Codex가 스킬을 선택하는 기준이자, 실행할 때 따르는 완전한 지침서다.

---

## 파일 구조

```
---
name: <skill-name>
description: <선택 기준 설명>
---

# <Skill Title>

<본문>
```

---

## Frontmatter 스펙

### `name` [필수]

- **타입**: string
- **형식**: `kebab-case`
- **값**: 디렉터리명과 동일해야 한다.

```yaml
name: intake-normalizer
name: spec-writing-standard
name: babysit-pr
```

### `description` [필수]

- **타입**: string
- **역할**: Codex가 스킬을 **자동 선택**할 때 사용하는 기준.
- **길이**: 1–3 문장 권장.
- **핵심**: 이 필드가 스킬의 선택 기준이다. 언제 사용해야 하는지, 언제 사용하지 말아야 하는지를 담는다.

**좋은 예**:
```yaml
description: Normalize raw client input, PRD notes, or meeting notes into an AxiomMd input packet. Use when the source material is still messy and the next step needs a precise packet instead of free-form prose.
```

**나쁜 예** (너무 모호):
```yaml
description: Helps with writing things.
```

---

## 본문 섹션 스펙

### 권장 섹션 순서

| 섹션 | 필수 여부 | 목적 |
|------|-----------|------|
| `## Purpose` / `## Objective` | 필수 | 이 스킬이 달성하는 것 |
| `## When To Use` / `## Use This Skill When` | 필수 | 사용 조건 |
| `## When Not To Use` | 권장 | 부적절한 사용 차단 |
| `## Input Contract` | 권장 | 허용 입력과 최소 요건 |
| `## Core Workflow` / `## Workflow` | 필수 | 번호 매긴 실행 단계 |
| `## Commands` | 스크립트 있을 때 필수 | 실행할 명령어 |
| `## Output Contract` / `## Write Paths` | 권장 | 출력 파일과 형식 |
| `## Stop Conditions` | 필수 | 중단 조건 |
| `## References` / `## Resources` | 참조 있을 때 필수 | 참고 문서 경로 |

---

## 각 섹션 작성 규칙

### `## Purpose` / `## Objective`

한두 문장으로 스킬의 핵심 목적을 명시한다.

```markdown
## Purpose

Turn raw client input into one normalized `input.packet.yaml`.

This is a **source-changing skill**.
It writes the input packet only.
```

---

### `## Core Workflow` / `## Workflow`

**가장 중요한 섹션**. 번호가 매겨진 명확한 순서로 작성한다.

규칙:
- 각 단계는 하나의 행동만 포함한다.
- 조건 분기는 `If X, do Y` 형식으로 명확히 표현한다.
- 스크립트 실행 단계는 정확한 명령어를 포함한다.
- 단계가 많을 때는 번호 14개까지도 허용된다.

```markdown
## Core Workflow

1. Read the raw source material.
2. Fill `request_summary`.
3. Separate `scope.in` and `scope.out`.
4. If critical input is missing, record in `open_questions` — do not silently guess.
5. Run: `python3 scripts/check_spec_standard.py <path/to/spec.md>`
6. Re-check [assets/normalization-checklist.md](assets/normalization-checklist.md).
```

---

### `## Commands`

스킬이 실행하는 명령어를 코드 블록으로 제공한다.
각 명령 앞에 목적을 설명하는 제목을 붙인다.

```markdown
## Commands

### One-shot snapshot

```bash
python3 .codex/skills/babysit-pr/scripts/gh_pr_watch.py --pr auto --once
```

### Continuous watch

```bash
python3 .codex/skills/babysit-pr/scripts/gh_pr_watch.py --pr auto --watch
```
```

---

### `## Stop Conditions`

Codex가 스킬 실행을 **중단하고 사용자에게 반환해야 하는** 조건을 명시한다.

규칙:
- 불릿 리스트로 작성한다.
- 각 조건은 명확히 관찰 가능한 상태여야 한다.
- "모르겠다"는 stop condition이 아니다 — 구체적인 증거를 요구한다.

```markdown
## Stop Conditions

- raw input is too vague to separate in-scope / out-of-scope
- success criteria cannot be derived
- authentication / permission failure
- flaky retries exhausted (limit: 3)
- reviewer feedback requires product decision
```

---

### `## References`

상대 경로로 참조 파일을 링크한다.

```markdown
## References

- Contract: [references/INPUT_PACKET_CONTRACT.md](references/INPUT_PACKET_CONTRACT.md)
- Heuristics: [references/heuristics.md](references/heuristics.md)
- Template: [assets/normalization-checklist.md](assets/normalization-checklist.md)
```

---

## 완전한 SKILL.md 예시

```markdown
---
name: example-skill
description: Do X when Y is needed. Use when the source is Z. Do not use when A already exists.
---

# Example Skill

## Purpose

Produce a single `output.yaml` from raw inputs.

## When To Use

- source is raw and needs normalization
- next step requires a deterministic output

## When Not To Use

- a valid `output.yaml` already exists
- task is already in final form

## Input Contract

- raw notes, brief, or chat summary
- must provide enough to fill: summary, scope, constraints, done signals

If these cannot be derived, stop with an INPUT_GAP_REPORT.

## Core Workflow

1. Read the raw input.
2. Fill each required field.
3. Record unknowns in `open_questions`.
4. Run: `python3 scripts/validate.py <path/to/output.yaml>`
5. Re-check [assets/checklist.md](assets/checklist.md).

## Commands

### Validate output

```bash
python3 scripts/validate.py path/to/output.yaml
```

## Output Contract

- exactly one `output.yaml`
- no additional files

## Stop Conditions

- input too vague to determine scope
- required fields cannot be filled from evidence

## References

- [references/CONTRACT.md](references/CONTRACT.md)
- [assets/checklist.md](assets/checklist.md)
```

---

## 작성 금지 사항

- SKILL.md에 실행 규칙을 절반만 쓰고 나머지를 다른 파일에 분산하지 않는다.
- Workflow 단계에서 모호한 표현("고려한다", "적절히") 사용 금지.
- `description`을 짧은 제목처럼 쓰지 않는다 — 선택 기준이 담겨야 한다.
- References 없이 다른 파일을 암묵적으로 참조하지 않는다.
