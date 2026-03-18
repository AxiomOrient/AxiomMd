# Skill Anatomy — 스킬 해부학

스킬의 모든 구성 요소와 각 파일의 역할, 필수/선택 여부를 정의한다.

---

## 완전한 디렉터리 구조

```
<skill-name>/
├── SKILL.md                  [필수] AI 실행 지침 및 워크플로우
├── agents/
│   └── openai.yaml           [필수] Codex UI 인터페이스 정의
├── assets/                   [선택] 템플릿 및 작업 파일
│   ├── *.yaml                        입출력 패킷, 결과 스키마
│   ├── *.md                          체크리스트, 템플릿
│   └── *.json                        구조화된 출력 스키마
├── references/               [선택] 읽기 전용 참고 문서
│   └── *.md                          계약서, 휴리스틱, 규칙
└── scripts/                  [선택] Python 실행 스크립트
    └── *.py                          Python 3 전용
```

---

## 각 구성 요소 상세

### `SKILL.md` — AI 실행 지침 [필수]

**목적**: Codex가 이 스킬을 선택하고 실행할 때 따르는 완전한 지침서.

**frontmatter (필수)**:
```yaml
---
name: <skill-name>
description: <언제 이 스킬을 선택해야 하는지를 설명하는 한 줄>
---
```

**본문 구조** (권장):
```markdown
# <Skill Title>

## Purpose / Objective
무엇을 달성하는가.

## When To Use / Use This Skill When
이 스킬을 선택해야 하는 조건.

## When Not To Use
이 스킬을 선택하면 안 되는 조건.

## Input Contract
허용하는 입력 형식과 최소 요건.

## Core Workflow
번호가 매겨진 단계별 실행 순서.

## Commands
스킬이 실행하는 구체적인 명령어.

## Output Contract
생성하는 출력 형식과 경로.

## Stop Conditions
중단해야 하는 상황.

## References
참고 문서 경로 목록.
```

**핵심 규칙**:
- `description`은 스킬 선택 기준이다. 구체적이고 명확하게 작성한다.
- 워크플로우는 번호가 매겨진 순서로 작성한다.
- Stop Conditions는 반드시 명시한다.
- 이 파일이 실행 규칙의 유일한 출처여야 한다. 규칙을 여러 파일에 분산하지 않는다.

---

### `agents/openai.yaml` — UI 인터페이스 [필수]

**목적**: Codex CLI와 관련 UI가 스킬을 표시하고 호출하는 방법을 정의.

```yaml
interface:
  display_name: "사람이 읽는 스킬 이름"
  short_description: "UI에 표시되는 짧은 설명"
  default_prompt: "사용자가 이 스킬을 직접 호출할 때의 기본 프롬프트"
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `display_name` | string | UI에 표시되는 이름 |
| `short_description` | string | 스킬 목록에서 보이는 한 줄 설명 |
| `default_prompt` | string | `$<skill-name>` 호출 시 사용되는 기본 지시문 |

**`default_prompt` 작성 규칙**:
- `$<skill-name>`으로 스킬을 명시적으로 참조한다.
- 컨텍스트 힌트를 포함한다 (예: "from the current normalized input packet").
- Codex가 즉시 실행할 수 있을 만큼 구체적이어야 한다.

---

### `assets/` — 템플릿 및 작업 파일 [선택]

**목적**: 스킬 실행 중 읽거나 쓰는 파일들.

| 파일 유형 | 예시 | 사용 |
|-----------|------|------|
| 입력 패킷 | `input.packet.yaml` | 스킬 입력의 구조화된 형식 |
| 출력 패킷 | `handoff.packet.yaml` | 스킬 출력의 구조화된 형식 |
| 체크리스트 | `review-checklist.md` | AI가 완료 기준으로 사용 |
| 템플릿 | `report-template.md` | 출력 문서의 뼈대 |
| 결과 스키마 | `evidence.result.json` | 구조화된 결과 형식 |

**규칙**:
- assets는 스킬 실행 중 **쓰기 가능**하다.
- 패킷 파일은 YAML 형식을 우선 사용한다.
- 템플릿에는 채워야 할 자리표시자를 명확히 표시한다.

---

### `references/` — 읽기 전용 참고 문서 [선택]

**목적**: 스킬 실행 중 참조하는 읽기 전용 계약서, 규칙, 휴리스틱.

| 파일 유형 | 예시 | 내용 |
|-----------|------|------|
| 계약서 | `INPUT_PACKET_CONTRACT.md` | 입출력 형식의 규범적 정의 |
| 휴리스틱 | `heuristics.md` | 판단 기준과 결정 트리 |
| 요약 | `EXECUTION_CONTRACT_SUMMARY.md` | 실행 계약 요약 |
| 노트 | `github-api-notes.md` | API 사용법 등 기술적 참고 |

**규칙**:
- references는 **읽기 전용**이다. 스킬 실행 중 절대 수정하지 않는다.
- 파일명은 UPPER_SNAKE_CASE 또는 kebab-case를 사용한다.
- 계약서 파일명은 UPPER_SNAKE_CASE를 권장한다.

---

### `scripts/` — Python 실행 스크립트 [선택]

**목적**: 스킬이 실행하는 Python 3 헬퍼 스크립트.

**필수 조건**:
- **Python 3 전용** — 다른 언어 사용 금지.
- 첫 줄에 shebang: `#!/usr/bin/env python3`
- 모듈 docstring 필수.
- `argparse`로 CLI 인터페이스를 정의한다.
- SKILL.md의 Commands 섹션에 실행 방법을 명시한다.

**일반적인 패턴**:
```python
#!/usr/bin/env python3
"""스크립트 목적을 설명하는 docstring."""

import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="...")
    parser.add_argument("--option", ...)
    args = parser.parse_args()
    # 로직

if __name__ == "__main__":
    main()
```

---

## 최소 유효 스킬 (Minimal Valid Skill)

스킬이 동작하기 위한 최소 구성:

```
<skill-name>/
├── SKILL.md          ← frontmatter + 워크플로우 필수
└── agents/
    └── openai.yaml   ← interface 섹션 필수
```

scripts, assets, references가 없어도 동작한다.
복잡한 워크플로우일수록 더 많은 구성 요소가 필요하다.

---

## 실제 예시: `babysit-pr` (openai/codex)

```
.codex/skills/babysit-pr/
├── SKILL.md                          PR 모니터링 지침
├── agents/
│   └── openai.yaml                   display_name: "PR Babysitter"
├── references/
│   ├── heuristics.md                 CI 분류 체크리스트 및 결정 트리
│   └── github-api-notes.md           GitHub API 참고
└── scripts/
    └── gh_pr_watch.py                PR 상태 폴링 스크립트 (Python 3)
```
