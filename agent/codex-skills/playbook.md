# Codex Skills — 운영 플레이북

스킬을 설치, 실행, 유지보수, 디버깅하는 운영 절차서.

---

## 1. 설치

### 1-1. 단일 스킬 설치

개발 저장소의 스킬을 실제 프로젝트에 설치한다.

```bash
# 이 저장소 기준
cp -r agent/skills/<skill-name> /path/to/project/.codex/skills/
```

또는 심볼릭 링크 (개발 중):
```bash
ln -s "$(pwd)/agent/skills/<skill-name>" /path/to/project/.codex/skills/<skill-name>
```

### 1-2. 전체 스킬 설치

```bash
mkdir -p /path/to/project/.codex/skills
cp -r agent/skills/. /path/to/project/.codex/skills/
```

### 1-3. 설치 확인

```bash
ls /path/to/project/.codex/skills/
```

예상 출력:
```
charter-blueprint-author/
feature-package-author/
intake-normalizer/
...
```

---

## 2. 스킬 실행

### 2-1. 자동 선택

Codex에 작업을 요청하면 `SKILL.md`의 `description`을 기반으로 자동 선택된다.

```
"raw meeting notes를 input packet으로 변환해줘"
→ intake-normalizer 자동 선택
```

### 2-2. 명시적 호출

`openai.yaml`의 `default_prompt`에 정의된 `$<skill-name>` 형식으로 직접 호출:

```
"$intake-normalizer를 사용해서 이 노트를 정규화해줘"
```

### 2-3. 스크립트 직접 실행

```bash
# 스킬 경로 기준
python3 .codex/skills/spec-writing-standard/scripts/check_spec_standard.py path/to/spec.md

# 이 저장소 기준
python3 agent/skills/spec-writing-standard/scripts/check_spec_standard.py path/to/spec.md
```

---

## 3. 스킬 업데이트

### 3-1. SKILL.md 업데이트

1. 변경사항을 `agent/skills/<skill-name>/SKILL.md`에 반영한다.
2. 설치된 경로에 복사한다.

```bash
cp agent/skills/<skill-name>/SKILL.md /path/to/project/.codex/skills/<skill-name>/SKILL.md
```

### 3-2. 스크립트 업데이트

```bash
cp agent/skills/<skill-name>/scripts/. /path/to/project/.codex/skills/<skill-name>/scripts/
```

### 3-3. 변경 검증

```bash
# 변경된 스킬의 구조 확인
ls -la /path/to/project/.codex/skills/<skill-name>/
cat /path/to/project/.codex/skills/<skill-name>/SKILL.md | head -10
```

---

## 4. 새 스킬 추가

→ [authoring-guide.md](authoring-guide.md) 참조.

요약:
1. `agent/skills/<new-skill-name>/` 디렉터리 생성
2. `SKILL.md` 작성 (frontmatter + workflow)
3. `agents/openai.yaml` 작성
4. assets, references, scripts 추가 (필요시)
5. 자체 검토 체크리스트 통과
6. 대상 프로젝트에 설치

---

## 5. 스킬 삭제

```bash
# 이 저장소에서 제거
rm -rf agent/skills/<skill-name>

# 설치된 위치에서도 제거
rm -rf /path/to/project/.codex/skills/<skill-name>
```

**삭제 전 체크**:
- 다른 스킬의 `default_prompt`에서 이 스킬을 참조하는가?
- 워크플로우 문서에서 이 스킬을 명시적으로 사용하는가?

---

## 6. 디버깅

### 6-1. 스킬이 Codex에 인식되지 않을 때

```bash
# openai.yaml 위치 확인
find .codex/skills -name "openai.yaml"

# 예상: .codex/skills/<name>/agents/openai.yaml
# 다른 위치라면 이동 필요
```

### 6-2. Codex가 잘못된 스킬을 선택할 때

`SKILL.md`의 `description` 필드를 수정한다.
`When To Use` / `When Not To Use`를 더 구체적으로 작성한다.

**진단 방법**:
1. 현재 description이 모호하거나 너무 일반적인가?
2. 다른 스킬의 description과 겹치는 부분이 있는가?
3. 잘못 선택된 스킬의 description이 더 구체적인가?

### 6-3. 스크립트 실행 오류

```bash
# Python 버전 확인
python3 --version  # 3.8 이상이어야 함

# 스크립트 직접 실행으로 오류 확인
python3 agent/skills/<skill-name>/scripts/<script>.py --help

# 의존성 오류
pip install pyyaml  # YAML 처리가 필요한 경우
```

### 6-4. SKILL.md 검증

```bash
# frontmatter 확인
head -5 agent/skills/<skill-name>/SKILL.md

# 필수 섹션 확인
grep -n "^## " agent/skills/<skill-name>/SKILL.md
```

필수 섹션:
- `## Workflow` 또는 `## Core Workflow`
- `## Stop Conditions`

---

## 7. 현재 스킬 목록

| 스킬 | 목적 | scripts |
|------|------|---------|
| `intake-normalizer` | raw input → input.packet.yaml | 없음 |
| `scope-router` | 작업 범위 결정 및 라우팅 | 없음 |
| `charter-blueprint-author` | product-charter + system-blueprint 작성 | 없음 |
| `feature-package-author` | feature package 작성 | 없음 |
| `spec-writing-standard` | 스펙 및 scoped artifact 작성 | check_spec_standard.py, check_scoped_artifact.py |
| `package-readiness-review` | feature package 준비도 검토 | 없음 |
| `manual-contract-compiler` | execution plan 컴파일 | 없음 |
| `run-evidence-normalizer` | 실행 결과 정규화 | 없음 |
| `reconcile-review` | 실행 결과와 계획 대조 검토 | 없음 |

---

## 8. 유지보수 체크리스트 (분기별 권장)

- [ ] 모든 스킬의 `description`이 현재 워크플로우를 정확히 반영하는가?
- [ ] `references/` 파일이 최신 계약을 반영하는가?
- [ ] `scripts/`가 Python 3 전용인가? (`find agent/skills -name "*.rb"` 결과가 없어야 함)
- [ ] 스킬 이름과 디렉터리명이 일치하는가?
- [ ] 모든 `openai.yaml`에 세 필드가 존재하는가?
- [ ] `assets/` 템플릿이 현재 사용하는 패킷 형식과 일치하는가?

---

## 9. 빠른 참조

```bash
# 모든 스킬 이름 확인
ls agent/skills/

# 특정 스킬 구조 확인
find agent/skills/<skill-name> -type f | sort

# Ruby 파일 검색 (없어야 함)
find agent/skills -name "*.rb"

# 모든 스크립트 확인
find agent/skills -name "*.py"

# openai.yaml 모두 확인
find agent/skills -name "openai.yaml" -exec echo {} \; -exec head -5 {} \;
```
