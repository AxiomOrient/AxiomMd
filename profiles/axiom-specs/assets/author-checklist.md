# Author Checklist (AxiomSpecs Profile)

AxiomSpecs profile이 활성화된 경우, 아래 checklist를 generic checklist에 추가로 사용한다.

- [ ] 입력이 AxiomMd `input.packet.yaml` shape를 따르거나, `mode=update`에 필요한 기존 package/source evidence가 충분하다.
- [ ] route decision이 있으면 package authoring 경로와 모순되지 않는다.
- [ ] route가 `framing-first`였으면 framing docs를 읽었다.
- [ ] create-mode metadata가 많으면 `authoring.request.yaml`로 product-local overlay를 분리했다.
- [ ] package가 하나의 bounded feature만 다룬다.
- [ ] `intent.md`, `package.yaml`, `requirements.yaml`, `invariants.yaml`, `design.md`, `tasks.md`, `evals.yaml`, `risks.yaml`, `decisions.jsonl`, `contracts/`, `slices.yaml`가 모두 존재한다.
- [ ] `package.yaml`에 `feature_id`, `slug`, `title`, `state`, `review_mode`, `profile_key`, `planes`, `implementation_order`, `owner_roles`, `target_repos`, `adoption`, `proof_state`, `current_progress`, `next_step`, `blockers`가 있다.
- [ ] `planes`는 AxiomSpecs local profile 값을 사용했다.
- [ ] `adoption`은 profile baseline이나 기존 package evidence에 있는 token만 사용했다.
- [ ] 모든 `must` requirement가 최소 1개의 `kind: blocking` eval에 연결된다.
- [ ] 모든 requirement가 최소 1개의 task에 연결된다.
- [ ] 모든 task가 `req_ids`, `eval_ids`, `touched_paths`, `next`를 가진다.
- [ ] 모든 eval이 `req_ids`, `task_ids`, `procedure`, `pass_condition`을 가진다.
- [ ] `design.md`에 Boundary / Interfaces / Failure / Requirement mapping이 있다.
- [ ] `slices.yaml`에 최소 1개의 launchable slice가 있고 필수 필드가 채워져 있다.
- [ ] `risks.yaml`에 현재 AxiomSpecs house shape와 충돌하는 invented key를 넣지 않았다.
- [ ] `decisions.jsonl` line shape가 current AxiomSpecs examples와 맞다.
- [ ] `decisions.jsonl`은 비어 있지 않다.
- [ ] 기존 package를 수정할 때 semantic continuity가 있으면 ID를 유지했다.
- [ ] AxiomRunner / AxiomNexus / codex-runtime semantics를 로컬에서 재정의하지 않았다.
- [ ] `python $AXIOM_MD/scripts/workflow_check.py package <feature-dir> --base-dir <AxiomSpecs>`를 실행했다.
- [ ] authoring-stage handoff가 필요하면 `python $AXIOM_MD/scripts/workflow_check.py handoff <path>`까지 통과했다.
- [ ] `authoring.request.yaml`을 썼다면 `python $AXIOM_MD/scripts/workflow_check.py authoring-request <path>`를 통과했다.
- [ ] owner repo 정보를 GitHub에서 다시 읽지 않고, skill 안의 summary와 target repo local files만 사용했다.
