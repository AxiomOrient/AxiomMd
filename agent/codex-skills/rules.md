# Codex Skills — 절대 규칙

어기면 스킬이 동작하지 않거나, 예측 불가능하게 동작하는 규칙들.

---

## 파일 구조 규칙

### R-01: `agents/openai.yaml` 경로는 고정이다

```
<skill-name>/agents/openai.yaml
```

- 파일명을 변경하지 않는다.
- 디렉터리명을 변경하지 않는다.
- 이 경로가 아니면 Codex가 스킬을 인식하지 못한다.

### R-02: `SKILL.md`는 반드시 루트에 위치한다

```
<skill-name>/SKILL.md
```

- 하위 디렉터리에 넣지 않는다.
- 파일명은 반드시 `SKILL.md` (대소문자 일치).

### R-03: 스킬 이름은 `name` 필드와 디렉터리명이 일치해야 한다

```yaml
# SKILL.md frontmatter
---
name: intake-normalizer   ← 디렉터리명과 동일해야 함
---
```

---

## 언어 규칙

### R-04: scripts/는 Python 3 전용

- `.rb` (Ruby) 파일 금지.
- `.sh` (Bash) 파일은 단순 래퍼만 허용, 복잡한 로직 금지.
- `.js`, `.ts` (Node.js) 파일 금지.
- Python 3.8+ 호환 코드를 작성한다.
- 첫 줄은 반드시 `#!/usr/bin/env python3`이어야 한다.

### R-05: 외부 패키지는 표준 라이브러리를 우선한다

가능하면 표준 라이브러리만 사용한다.
외부 패키지가 필요하면 스크립트 상단에 명시한다:

```python
try:
    import yaml
except ImportError:
    print("ERROR: pip install pyyaml", file=sys.stderr)
    sys.exit(1)
```

---

## SKILL.md 규칙

### R-06: `description`은 선택 기준이어야 한다

단순 설명이 아니라 **Codex가 이 스킬을 선택해야 하는 조건**을 포함해야 한다.

나쁜 예:
```yaml
description: A skill for writing specs.
```

좋은 예:
```yaml
description: Write or upgrade an AI-facing specification. Use when a repo needs a precise, implementation-ready contract. Do not use for lightweight briefs or changelogs.
```

### R-07: Workflow 단계는 번호가 있어야 한다

```markdown
## Workflow

1. 첫 번째 단계
2. 두 번째 단계
3. 세 번째 단계
```

번호 없는 불릿 리스트는 단계가 아니라 나열이다. 순서가 있으면 번호를 쓴다.

### R-08: Stop Conditions가 없는 SKILL.md는 미완성이다

모든 SKILL.md는 `## Stop Conditions` 섹션을 포함해야 한다.
Codex는 이 섹션이 없으면 언제 멈춰야 할지 모른다.

### R-09: 실행 규칙을 분산하지 않는다

AI 실행 지침은 `SKILL.md` 하나에 집중한다.
`references/`에 규칙을 넣고 SKILL.md에는 "자세한 내용은 references 참조"만 쓰는 방식은 금지.
`references/`는 **참조 자료**이지 **실행 지침**이 아니다.

---

## assets/ 규칙

### R-10: assets/는 읽기와 쓰기 모두 가능하다

스킬 실행 중 assets/ 파일을 업데이트하는 것은 허용된다.
쓰기 경로는 SKILL.md의 `## Write Paths` 또는 `## Output Contract`에 명시해야 한다.

### R-11: 패킷 파일은 YAML 형식을 우선한다

- 입출력 패킷: `.yaml`
- 결과 보고: `.yaml` 또는 `.json`
- 템플릿: `.md`
- `.xml`, `.toml`, `.ini` 사용 금지.

---

## references/ 규칙

### R-12: references/는 읽기 전용이다

스킬 실행 중 references/ 파일을 절대 수정하지 않는다.
계약서, 규칙, 휴리스틱은 스킬 실행의 입력이지 출력이 아니다.

---

## openai.yaml 규칙

### R-13: `default_prompt`에는 `$<skill-name>` 참조를 포함한다

```yaml
default_prompt: "Use $intake-normalizer to normalize the current input."
```

Codex가 어떤 스킬을 실행해야 하는지 명확히 참조해야 한다.

### R-14: `interface` 아래 세 필드는 모두 필수다

```yaml
interface:
  display_name: ...      ← 필수
  short_description: ... ← 필수
  default_prompt: ...    ← 필수
```

하나라도 빠지면 Codex UI에서 스킬이 불완전하게 표시된다.

---

## 운영 규칙

### R-15: 스킬은 `.codex/skills/` 에 설치되어야 동작한다

개발/관리용 경로 (예: `agent/skills/`)가 아니라
실제 프로젝트의 `.codex/skills/<skill-name>/` 경로에 설치해야 Codex가 인식한다.

### R-16: 스킬 삭제는 신중하게

스킬을 삭제하면 그 스킬을 참조하는 워크플로우가 깨진다.
삭제 전에 이 스킬을 사용하는 `default_prompt` 참조를 검색한다.

### R-17: 스킬 이름 변경은 양쪽을 동시에 업데이트한다

스킬 이름을 변경하면:
1. 디렉터리명 변경
2. `SKILL.md`의 `name` 필드 변경
3. `openai.yaml`의 `default_prompt`에서 `$<old-name>` 참조 변경
4. 이 스킬을 참조하는 다른 스킬의 SKILL.md 변경

---

## 빠른 체크 표

| 항목 | 검사 방법 |
|------|-----------|
| Ruby 파일 없음 | `find . -name "*.rb"` |
| openai.yaml 위치 | `find . -name "openai.yaml" -not -path "*/agents/*"` (결과가 없어야 함) |
| name-디렉터리 일치 | frontmatter의 `name:` 값 = 디렉터리명 |
| Stop Conditions 존재 | SKILL.md에 `## Stop Conditions` 있음 |
| Python 3 shebang | `head -1 scripts/*.py` = `#!/usr/bin/env python3` |
