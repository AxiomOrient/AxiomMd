# Artifact Curator — 구현 계획

## 문제

작업 세션이 반복될수록 아래가 쌓인다.

- 테스트 workflow 디렉터리
- 루트에 방치된 임시 분석 파일
- 신규 구현으로 대체된 레거시 스크립트
- symlink여야 할 파일 복사본
- 검증 실행 로그

정리 기준이 없어서 매번 손으로 판단한다.

---

## 해법

스킬 하나 + 워크플로우 문서 하나.

### 스킬: `artifact-curator`

대상 디렉터리를 스캔해 정리 후보를 분류하고,
확인 후 제거하고, 핸드오프 패킷을 남긴다.

**워크플로우 4단계**

```
scout → manifest → prune → handoff
```

| 단계 | 역할 |
|------|------|
| scout | 대상 디렉터리를 스캔해 후보 목록 생성 |
| manifest | 후보별 분류·근거·제안 동작 기록 |
| prune | `remove` 항목만 실행, `defer`는 보류 |
| handoff | `cleanup.handoff.packet.yaml` 작성 |

**정리 후보 분류**

| 분류 | 예시 |
|------|------|
| `test_artifact` | `workflow-live-test-*/` |
| `temp_report` | 루트에 쌓인 `*-report.md`, `*-summary.md` |
| `stale_log` | `validate.log`, `validation.log` |
| `superseded_script` | 새 구현으로 대체된 스크립트 |
| `duplicate_copy` | canonical 위치의 사본 |

**규칙**

- 기본 모드는 `dry-run` — 명시적으로 `execute`를 지정해야 삭제
- `preserve_patterns`에 매칭되면 어떤 분류도 건드리지 않음
- `superseded_script` 판정은 request에서 명시해야 함 (자동 추론 금지)
- `duplicate_copy`는 diff가 empty일 때만 판정

---

## 생성할 파일

**AxiomMd**

```
agent/skills/artifact-curator/
  SKILL.md
  agents/openai.yaml
  assets/
    cleanup.request.yaml          # 입력 템플릿
    cleanup.handoff.packet.yaml   # 출력 템플릿
    cleanup-checklist.md          # 분류별 판단 기준
  references/
    CURATION_POLICY.md            # 분류 정책 상세
  scripts/
    check_cleanup_request.py      # 입력 유효성 검사
```

**AxiomMd**

```
method/quality-system.md           # 유지보수/품질 운영 규칙
```

---

## 구현 순서

1. `CURATION_POLICY.md` — 분류 기준 정의
2. 템플릿 2개 — `cleanup.request.yaml`, `cleanup.handoff.packet.yaml`
3. `cleanup-checklist.md`
4. `SKILL.md`
5. `check_cleanup_request.py`
6. `agents/openai.yaml`
7. `method/quality-system.md`
