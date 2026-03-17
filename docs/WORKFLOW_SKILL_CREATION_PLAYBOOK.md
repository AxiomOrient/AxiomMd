# Workflow Skill Creation Playbook

## Purpose

이 문서는 workflow를 먼저 설계하고, 그 위에서 skill을 만드는 과정을 generic하게 정리한다.

## Core Rule

skill부터 만들지 않는다.

```text
workflow
-> artifact contract
-> gate
-> repeated move
-> skill
```

## Steps

1. raw input 종류를 정한다
2. 큰 작업 단위 workflow를 정한다
3. workflow 사이 artifact를 정한다
4. HILT 지점을 정한다
5. 반복되는 move만 skill로 뽑는다
6. sample run으로 끝까지 검증한다

## What Must Exist First

- `input.packet.yaml`
- `route.decision.yaml`
- 필요하면 framing docs
- feature package contract
- readiness output
- handoff packet

## What We Learned

- giant workflow 하나는 약하다
- micro-step 나열도 약하다
- 중간 산출물 파일이 제일 중요하다
- validator 없는 artifact는 오래 못 간다
- runtime fetch는 self-contained skill을 약하게 만든다

## Final Rule

좋은 skill 세트는 skill이 많은 세트가 아니다.
workflow가 먼저 보이고,
각 workflow가 파일로 닫히고,
정말 반복되는 move만 skill로 남아 있는 세트가 좋은 세트다.
