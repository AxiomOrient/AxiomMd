# Compile Checklist

## Before Writing Outputs

- [ ] package path exists
- [ ] package metadata is readable
- [ ] selected slice exists
- [ ] selected slice is launchable
- [ ] req ids are resolvable
- [ ] task ids are resolvable
- [ ] eval ids are resolvable
- [ ] approval mode is explicit
- [ ] budget is explicit enough for bounded launch
- [ ] no runtime-specific invented field is needed

## Required Outputs

- [ ] `execution-brief.md`
- [ ] `goal.json`
- [ ] `workflow-pack.overlay.yaml`
- [ ] `launch.request.yaml`
- [ ] `execution.plan.yaml`
- [ ] compile-stage `handoff.packet.yaml`

## Final Checks

- [ ] scope stayed within selected slice
- [ ] stable ids were preserved
- [ ] next step is explicit
- [ ] blockers are explicit when present
