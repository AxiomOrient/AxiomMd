# Governance

## Three Spaces

generic / product-specific / implementation 세 공간은 개념 구분이다.
저장소 수가 셋이라는 뜻이 아니다.

| 공간 | 저장소 예시 | 넣는 것 | 넣지 않는 것 |
| --- | --- | --- | --- |
| generic | AxiomMd | method docs, loop rules, quality rules, generic templates, reusable skills | product truth, runtime detail |
| product-specific | AxiomSpecs | blueprint, architecture, local profile, feature packages, delivery plan | generic method duplicates, implementation-local code detail |
| implementation | 실제 코드 저장소 | crates, apps, adapters, tests, runtime integration | generic method 설명, durable product blueprint 설명 |

## Standard Flow

```text
1. generic rule or asset is defined in generic space
2. product-specific space localizes it into a product profile or feature package
3. implementation space ships code against the approved package
4. eval / evidence / drift / failures are observed
5. generic lesson goes back to generic space
6. local lesson stays in product-specific space
```

## Placement Rule

새 문서를 넣기 전에 아래 네 질문을 먼저 본다.

1. 제품명을 지워도 성립하는가?
2. 두 개 이상 제품에서 재사용 가능한가?
3. 특정 저장소 경로나 runtime 대신 generic contract로 설명 가능한가?
4. 예시를 generic example로 바꿔도 의미가 보존되는가?

모두 "예"면 generic space(AxiomMd) 후보다.
하나라도 "아니오"면 generic space 밖이 더 적합하다.

**AxiomMd에 허용되는 것:**

- AI 개발 방법론 문서
- harness engineering 문서
- spec-driven development 문서
- agentic / closed-loop development 문서
- mental model 문서
- skill / workflow / reusable reasoning asset 문서
- generic spec package standard
- generic template
- 문서 승격 / 정리 / 경계 유지 규칙

**AxiomMd에 허용되지 않는 것:**

- 특정 제품 blueprint
- 특정 제품 feature spec
- 특정 제품 architecture
- 특정 제품 계획 문서
- 특정 제품 runtime / integration 상세
- 특정 crate, API, endpoint, command에만 맞는 설명

## Promotion Rule

아래를 모두 만족하면 generic space로 올린다.

- 제품 전용 이름을 제거해도 성립한다.
- 두 개 이상 feature package에서 반복된다.
- 특정 runtime이나 path에 묶여 있지 않다.
- template, rule, checklist, harness로 재사용 가능하다.

아래 중 하나라도 해당하면 product-specific space에 남긴다.

- 제품 surface나 plane을 직접 다룬다.
- 특정 제품 저장소 경로를 직접 다룬다.
- 특정 feature package의 product intent를 다룬다.
- 제품 조직의 runtime adoption 정책을 다룬다.

아래 중 하나라도 해당하면 implementation space에 남긴다.

- crate / API / endpoint / CLI contract가 핵심이다.
- runtime storage / process / transport detail이 핵심이다.
- shipping code와 함께 바뀌어야 한다.

## Document Operations

새 문서를 만들기 전에 항상 아래 순서로 먼저 검토한다.

1. **delete** — 임시 메모, 기존 문서와 질문이 같은 문서, 이미 흡수된 내용
2. **merge** — 같은 규칙을 두 문서가 설명하거나, 같은 독자가 연속으로 읽어야 의미가 나는 경우
3. **move** — 내용은 유효하지만 owner가 잘못됐거나, generic/product 배치가 뒤바뀐 경우
4. **archive** — 외부 참조 가치 또는 중요한 의사결정 이력이 있는 예외적 경우
5. **create** — 마지막 선택지

archive는 예외적으로만 쓴다. 초기 중복 문서에는 archive보다 delete를 우선한다.

**PR Checklist:**

- 이 문서는 정말 새로 필요했는가?
- delete / merge / move 검토를 먼저 했는가?
- owner 저장소가 맞는가?
- 같은 질문에 답하는 기존 문서가 없는가?
- 다른 저장소 파일 링크 없이도 이 문서만으로 읽히는가?
- durable rule과 backlog가 한 문서에 섞이지 않았는가?

## Observation and Feedback

관측 입력은 아래에서 모은다.

- failing eval, drift classification, repeated review comment, restart failure, evidence insufficiency, runtime mismatch, handoff failure

관측 후에는 반드시 아래 셋 중 하나로 닫는다.

1. generic rule / template / harness 개선
2. product-specific space package / profile / architecture 수정
3. implementation space patch

아무 데도 승격되지 않는 반복 실패는 루프가 닫히지 않은 상태다.

## Writing Rule

- 제품명을 넣지 않아도 설명 가능한 문서만 둔다.
- 특정 저장소 경로를 본문 진실로 삼지 않는다.
- 다른 저장소 파일을 직접 링크하지 않는다.
- 절대경로, 상대경로, `pwd` 기반 경로를 다른 저장소 파일 참조에 쓰지 않는다.
- reusable한 내용만 남긴다.
- 예시는 generic example로 쓴다.
- 한 문서는 한 질문에 답하게 쓴다.
- roadmap와 durable rule을 한 문서에 섞지 않는다.

다른 저장소에서 가져온 내용이 필요하면 아래처럼 처리한다.

1. 파일 링크를 남기지 않는다.
2. generic lesson만 추출한다.
3. 이 저장소 문장으로 다시 쓴다.
4. 저장소 의존성이 생기는 표현은 지운다.

## Anti-Patterns

- product-specific space에 generic standard를 그대로 복제
- generic space에 제품 feature truth 저장
- implementation space에 durable product blueprint 저장
- 다른 저장소 파일을 직접 링크해 generic 문서를 설명
- chat에만 결정을 남기고 source를 고치지 않음
- 같은 규칙을 두 군데 설명

## Boundary Rule

공간은 연결돼 있어도 문서는 직접 의존하지 않는다.

- generic space 문서가 다른 저장소 파일 경로를 직접 참조하면 안 된다.
- product-specific space 문서도 generic space 파일 링크에 의존하면 안 된다.
- 필요하면 각 공간이 자기 문장으로 다시 써야 한다.

## Quality System

### Why Code Gets Messy

AI는 좋은 코드만 빠르게 만들지 않는다.
나쁜 패턴도 빠르게 복제한다.

문제의 본체는 대개 모델 자체보다 아래다.

- 컨텍스트가 약하다
- 완료 조건이 약하다
- 검증이 약하다
- 반복 실수를 규칙으로 올리지 않는다
- 유지보수 루프가 없다

> AI 시대의 코드 품질은 생성 능력이 아니라 정리 능력으로 결정된다.

### Control Layers

1. **Input Quality** — request를 `input.packet.yaml`로 정규화한다. route decision 없이 바로 package로 밀어 넣지 않는다. 모호함은 open question으로 남긴다.
2. **Plan Quality** — framing이 필요하면 charter / blueprint로 먼저 좁힌다. 모든 task는 `REQ-*`와 `EVAL-*`를 가진다. scope expansion을 막는다.
3. **Execution Quality** — 작은 loop만 허용한다. 승인 없는 새 행동은 막는다.
4. **Verification Quality** — structure check, contract check, invariant check, regression check, risk check, readiness check.
5. **Reconciliation Quality** — 결정은 `decisions.jsonl`로 남긴다. drift를 class로 분류한다. source를 다시 맞춘다.
6. **Maintenance Quality** — task 종료 시 local tidy. feature 종료 시 commonization. 주기적으로 entropy sweep.

### Promotion Ladder

반복 실수는 아래 순서로 승격한다.

1. comment
2. checklist
3. repository rule
4. template
5. harness
6. codemod or tool

같은 실수를 두 번 이상 사람 리뷰로만 막고 있다면 승격이 부족한 것이다.

### Failure Analysis Rule

AI 실패는 먼저 모델 탓을 하지 않는다.
아래 순서로 본다.

1. Reproduce
2. Observe
3. Hypothesize
4. Verify
5. Fix root cause

> 많은 AI 실패는 모델 실패가 아니라 하네스 실패다.

실패 후에는 항상 아래 중 하나가 바뀌어야 한다.

- 문서, template, task sizing, tool contract, verification, approval rule

### Cleanup Cadence

| 시점 | 해야 할 정리 |
| --- | --- |
| workflow close | handoff packet, open question, next step 정리 |
| task close | local cleanup, validation update |
| feature close | duplication 정리, decisions 정리, package update |
| periodic maintenance | repeated smell 정리, codemod 기회 발굴 |
