# Method Taxonomy

## Purpose

이 문서는 AI 개발 방법론들을 구분하고, 그 안에서 우리가 채택한 방법의 위치를 고정한다.

## Taxonomy

### 1. AI-Assisted Coding

- LLM을 보조 도구로 사용
- 주 실행 주체는 사람
- 보통 prompt와 code diff 중심

### 2. Agentic Development

- agent가 tool을 사용하며 loop를 돈다
- 단일 agent 또는 multi-agent가 가능
- 범위가 넓고 품질 편차가 크다

### 3. Agent-Orchestrated Development

- 계획, 구현, 검증, handoff가 역할 또는 단계로 나뉜다
- orchestration layer가 중요하다

### 4. Closed-Loop Agentic Development

- 작업이 `plan -> execute -> verify -> reconcile` 루프로 닫힌다
- feedback과 restartability를 전제로 한다

### 5. Spec-Driven Agentic Software Engineering

- 자연어를 spec package로 컴파일한다
- spec package가 source of truth다
- agent loop가 spec, eval, evidence를 기준으로 돈다

## Selected Method Name

이 저장소가 채택한 공식 이름은 아래다.

> **Spec-Driven Agentic Software Engineering**

이 이름은 아래 세 뜻을 동시에 가진다.

- `Spec-Driven`: 자연어가 아니라 구조화된 spec package를 기준으로 일한다.
- `Agentic`: 계획, 구현, 검증, 조정이 agent loop 안에서 돌아간다.
- `Software Engineering`: 코드 생성만이 아니라 계약, 검증, 운영, evidence까지 포함한다.

## Operating Name

실행 방식은 아래 표현을 쓴다.

> **Closed-Loop Harnessed Development**

이 말은 아래를 뜻한다.

- 작업은 열린 프롬프트가 아니라 닫힌 루프로 돈다.
- agent는 자유 방치가 아니라 harness 안에서 움직인다.
- 완료는 self-report가 아니라 evidence로 닫힌다.

## Adjacent Terms

- `Autonomous Agent Development`: agent autonomy에 초점을 둔 넓은 표현
- `Closed-Loop Agentic Development`: 실행 구조에 초점을 둔 표현
- `Spec-Driven Agentic Software Engineering`: spec package와 engineering discipline까지 포함한 가장 정확한 표현

## What This Method Is Not

이 방법은 아래와 다르다.

- 단순 AI-assisted coding
- vibe coding
- 한 번의 거대 프롬프트로 끝내는 개발
- 문서 한 장을 source-of-truth로 삼는 방식

## Core Unit

이 방법의 최소 단위는 “채팅”이 아니다.
최소 단위는 아래 묶음이다.

```text
input packet
-> route decision
-> optional framing docs
-> feature package
-> readiness
-> approved package
-> bounded execution
-> verification
-> reconcile
```

## Source-of-Truth Rule

자연어는 입력이다.
source of truth는 아래 묶음이다.

- `input.packet.yaml`
- `route.decision.yaml`
- `package.yaml`
- `requirements.yaml`
- `invariants.yaml`
- `design.md`
- `tasks.md`
- `evals.yaml`
- `risks.yaml`
- `decisions.jsonl`

상황에 따라 아래가 추가된다.

- `product-charter.md`
- `system-blueprint.md`
- `readiness-report.md`

## Why This Method Exists

AI가 강한 것은 국소 구현이다.
AI가 약한 것은 장기 맥락 유지, 경계 보존, drift 제어다.

따라서 방법론의 본체는 “더 잘 생성하기”가 아니라 아래다.

- intent를 구조화하기
- 작업을 작은 loop로 자르기
- evidence 없이 통과시키지 않기
- 실패를 harness 개선으로 되돌리기
