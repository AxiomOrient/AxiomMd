# Author Checklist

완료 전에 아래를 모두 확인한다.

- [ ] 입력이 `input.packet.yaml` shape를 따르거나, `mode=update`에 필요한 기존 package/source evidence가 충분하다.
- [ ] route decision이 있으면 package authoring 경로와 모순되지 않는다.
- [ ] route가 `framing-first`였으면 framing docs를 읽었다.
- [ ] package가 하나의 bounded feature만 다룬다.
- [ ] `intent.md`, `package.yaml`, `requirements.yaml`, `invariants.yaml`, `design.md`, `tasks.md`, `evals.yaml`, `risks.yaml`, `decisions.jsonl`, `slices.yaml`가 모두 존재한다.
- [ ] `package.yaml`에 generic 필수 필드(`id`, `slug`, `title`, `state`, `layer`)가 있다.
- [ ] profile이 제공된 경우, profile-required 추가 필드가 `package.yaml`에 있다.
- [ ] `package.yaml`의 `layer` 값은 `python $AXIOM_MD/scripts/workflow_check.py ensure-layer <feature-dir>`로 확인했고, 누락 시 승인된 경우에만 `--write` 옵션으로 보정한다.
- [ ] 모든 `must` requirement가 최소 1개의 `kind: blocking` eval에 연결된다.
- [ ] 모든 requirement가 최소 1개의 task에 연결된다.
- [ ] 모든 task가 `req_ids`, `eval_ids`, `touched_paths`, `next`를 가진다.
- [ ] 모든 eval이 `req_ids`, `task_ids`, `procedure`, `pass_condition`을 가진다.
- [ ] `design.md`에 Boundary / Interfaces / Failure / Requirement mapping이 있다.
- [ ] `slices.yaml`에 최소 1개의 launchable slice가 있고, `path_scope`, `req_ids`, `task_ids`, `eval_ids`, `done_conditions`가 채워져 있다.
- [ ] `decisions.jsonl`은 비어 있지 않다.
- [ ] 기존 package를 수정할 때 semantic continuity가 있으면 ID를 유지했다.
- [ ] platform-specific runtime semantics를 source evidence 없이 만들어 넣지 않았다.
- [ ] `python $AXIOM_MD/scripts/workflow_check.py package <feature-dir>`를 실행했다.
- [ ] authoring-stage handoff가 필요하면 `python $AXIOM_MD/scripts/workflow_check.py handoff <path>`까지 통과했다.
- [ ] owner repo 정보를 GitHub에서 다시 읽지 않고, skill 안의 summary와 target repo local files만 사용했다.
