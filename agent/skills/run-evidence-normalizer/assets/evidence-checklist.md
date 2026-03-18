# Evidence Checklist

## Before Normalization

- [ ] package path resolves
- [ ] selected slice resolves
- [ ] run input root exists
- [ ] raw run outputs are readable
- [ ] verification outputs are readable or explicitly absent
- [ ] changed paths can be bounded to the selected slice

## Required Output Fields

- [ ] `run_id`
- [ ] `package_ref`
- [ ] `slice_id`
- [ ] linked req/task/eval ids
- [ ] produced_artifacts
- [ ] verification results
- [ ] changed paths
- [ ] failure summary when applicable

## Final Checks

- [ ] missing evidence vs negative evidence is explicit
- [ ] no reconcile classification was added here
- [ ] no source patch decision was implied here
- [ ] source ids were preserved
