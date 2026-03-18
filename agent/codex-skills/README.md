# Codex Skills — Knowledge Base

> **Codex Skills**는 OpenAI Codex CLI에서 실행되는 재사용 가능한 워크플로우 단위다.
> 이 디렉터리는 Skills를 이해하고, 작성하고, 운영하기 위한 완전한 지식 저장소다.

---

## 문서 인덱스

| 문서 | 목적 |
|------|------|
| [skill-anatomy.md](skill-anatomy.md) | 스킬의 모든 파일 구조와 각 파일의 역할 |
| [openai-yaml-spec.md](openai-yaml-spec.md) | `openai.yaml` 완전 스펙 |
| [skill-md-spec.md](skill-md-spec.md) | `SKILL.md` 완전 스펙 |
| [authoring-guide.md](authoring-guide.md) | 새 스킬 작성 단계별 가이드 |
| [script-patterns.md](script-patterns.md) | Python 스크립트 작성 패턴 |
| [rules.md](rules.md) | 절대 규칙 및 컨벤션 |
| [playbook.md](playbook.md) | 운영 플레이북 (설치, 실행, 유지보수) |

---

## Codex Skill이란

Codex Skill은 Codex가 특정 유형의 작업을 수행할 때 따르는 **구조화된 워크플로우 패키지**다.

```
.codex/skills/<skill-name>/
├── SKILL.md          ← AI 실행 지침 (가장 중요)
├── agents/
│   └── openai.yaml   ← UI 인터페이스 정의
├── assets/           ← 템플릿, 패킷, 체크리스트
├── references/       ← 읽기 전용 참고 문서
└── scripts/          ← Python 헬퍼 스크립트
```

---

## 작동 원리

1. 사용자가 Codex에 작업을 요청한다.
2. Codex는 각 스킬의 `SKILL.md` frontmatter `description` 필드를 읽고 가장 적합한 스킬을 선택한다.
3. 선택된 스킬의 `SKILL.md`에 따라 단계별로 작업을 수행한다.
4. 필요하면 `scripts/`의 Python 스크립트를 실행하고, `assets/`의 템플릿을 사용하고, `references/`의 문서를 참조한다.

---

## 이 저장소의 스킬 위치

```
agent/skills/<skill-name>/
```

> 실제 Codex CLI 설치 위치: `.codex/skills/<skill-name>/`
> 이 저장소는 스킬 개발 및 관리 저장소이므로 `agent/skills/` 경로를 사용한다.

---

## 핵심 원칙

- **SKILL.md가 단일 진실 공급원**: 모든 AI 실행 지침은 여기에 있다.
- **scripts/는 Python만**: 도우미 스크립트는 반드시 Python 3이어야 한다.
- **assets/는 템플릿과 작업 파일**: 스킬 실행 중 읽고 쓰는 파일들.
- **references/는 읽기 전용**: 계약서, 휴리스틱, 규칙 문서.
- **openai.yaml은 UI 레이어**: Codex 인터페이스가 표시하는 메타데이터.
