tasks:
  - id: TASK-0001
    title: "Build axm workflow command skeleton (run/check/validate)"
    req_ids:
      - REQ-0001
      - REQ-0004
    eval_ids:
      - EVAL-0001
    touched_paths:
      - "src/main.rs"
      - "src/workflow.rs"
      - "templates"
    next: "run command creates input.packet.yaml + route.decision.yaml and package artifacts in output dir"

  - id: TASK-0002
    title: "Implement skill context builder and validator wiring"
    req_ids:
      - REQ-0001
      - REQ-0002
    eval_ids:
      - EVAL-0002
    touched_paths:
      - "src/agent.rs"
      - "src/skill/context.rs"
      - "src/validate.rs"
    next: "Artifacts pass workflow_check strict mode for generated package"

  - id: TASK-0003
    title: "Add status observability and resume support scaffold"
    req_ids:
      - REQ-0003
      - REQ-0004
    eval_ids:
      - EVAL-0003
    touched_paths:
      - "src/status.rs"
      - "src/resume.rs"
      - "ui"
    next: "Operators can see stage, blockers, open_questions, and resume from last stage"
