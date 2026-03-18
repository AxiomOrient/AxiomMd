# Review Checklist

- [ ] package path가 정확하다.
- [ ] `python $AXIOM_MD/scripts/workflow_check.py ensure-layer <feature-dir>`로 layer 존재 여부를 먼저 확인했다.
- [ ] `python $AXIOM_MD/scripts/workflow_check.py package <feature-dir>`를 먼저 실행했다.
- [ ] required file set를 먼저 확인했다. (profile이 있으면 profile-required files도 포함)
- [ ] `ready`는 모든 generic gate pass (+ profile gates pass if active)일 때만 사용했다.
- [ ] broken `REQ/TASK/EVAL` ids를 정확히 적었다.
- [ ] vague prose 대신 concrete missing items를 적었다.
- [ ] cheapest next fixes는 최소 수정 단위로 적었다.
- [ ] evidence paths를 남겼다.
- [ ] `handoff.packet.yaml`에 `packet_version`, `stage`, `status`, `input_ref`, `changed_paths`, `produced_paths`, `evidence_refs`, `open_questions`, `next_step`, `blockers`를 채웠다.
- [ ] `next_step`는 바로 실행 가능한 최소 repair/action으로 적었다.
- [ ] optional review note를 쓰더라도 authoritative output이 handoff packet이라는 점을 유지했다.
- [ ] repair가 필요하면 authoring과 review를 섞지 않았다.
- [ ] owner repo 정보를 GitHub에서 다시 읽지 않고, skill 안의 summary와 target repo local files만 사용했다.
