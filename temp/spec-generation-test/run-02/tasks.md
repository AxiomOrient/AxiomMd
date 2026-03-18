tasks:
  - id: TASK-0001
    title: "Implement axm run/check/validate command orchestration skeleton"
    req_ids:
      - REQ-0001
      - REQ-0004
    eval_ids:
      - EVAL-0001
    touched_paths:
      - "src/main.rs"
      - "src/workflow.rs"
      - "templates"
    done_when: "run command can generate packet/route/package artifacts and persist run metadata"
    next: "run command creates packet, route, and package artifacts in output dir"

  - id: TASK-0002
    title: "Implement skill context builder and checkpoint validation wiring"
    req_ids:
      - REQ-0001
      - REQ-0003
    eval_ids:
      - EVAL-0002
    touched_paths:
      - "src/state/cache.rs"
      - "src/agent.rs"
      - "src/validate.rs"
    done_when: "checkpoint writes include stage/handoff summary and resume works from last complete stage"
    next: "Artifacts and resume checkpoints pass validation checks"

  - id: TASK-0003
    title: "Add TUI status observability and resume resume command"
    req_ids:
      - REQ-0002
      - REQ-0003
      - REQ-0004
    eval_ids:
      - EVAL-0003
    touched_paths:
      - "src/ui/tui.rs"
      - "src/status.rs"
      - "src/resume.rs"
    done_when: "TUI displays stage, blockers, open_questions, evidence refs, and resume target"
    next: "Operators can inspect failed stages and resume from command"
