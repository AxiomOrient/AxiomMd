#!/usr/bin/env python3
"""
workflow_runner.py — declarative workflow/pipeline schema + graph validator.

This script is intentionally separate from workflow_check.py:
 - workflow_check.py: artifact-level validator (existing contract checks)
 - workflow_runner.py: workflow definition/pipeline graph validator (no artifact mutations)

Examples:
  python scripts/workflow_runner.py validate workflow agent/workflows/authoring/intake-and-routing.yaml
  python scripts/workflow_runner.py validate pipeline agent/workflows/pipelines/authoring.yaml
  python scripts/workflow_runner.py validate manifests
  python scripts/workflow_runner.py simulate pipeline agent/workflows/pipelines/full-cycle.yaml --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple

try:
    import yaml
except ImportError:
    sys.exit("[ERROR] PyYAML is required. Install with `pip install pyyaml`.")


DEFAULT_CONDITIONAL_ARTIFACTS = {
    "raw_request",
    "raw_packet_source",
    "run_input_root",
}


WORKFLOW_REQUIRED_KEYS = ["id", "layer", "description", "inputs", "skills", "outputs"]
WORKFLOW_LAYERS = {"authoring", "execution", "shared"}

PIPELINE_REQUIRED_KEYS = ["id", "stages"]


@dataclass
class Check:
    name: str
    ok: bool
    level: str = "fail"
    detail: str = ""


@dataclass
class Result:
    passed: bool
    target: str
    kind: str
    checks: List[Check] = field(default_factory=list)

    def add(self, name: str, ok: bool, detail: str = "", warn: bool = False):
        level = "warn" if warn else ("pass" if ok else "fail")
        self.checks.append(Check(name=name, ok=ok, level=level, detail=detail))
        if not ok and not warn:
            self.passed = False
        return ok


def read_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as fp:
        data = yaml.safe_load(fp)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError("top-level document is not a YAML mapping")
    return data


def is_mapping(value):
    return isinstance(value, dict)


def is_str_list(value) -> bool:
    return isinstance(value, list) and all(isinstance(x, str) for x in value)


def is_id(value: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", value or ""))


def collect_workflow_files(workflows_root: Path) -> List[Path]:
    if not workflows_root.exists():
        return []
    return sorted([p for p in workflows_root.rglob("*.yaml") if p.is_file()])


def build_workflow_index(workflows_root: Path) -> Tuple[Dict[str, Path], Dict[str, Path], Dict[str, str], List[Check]]:
    workflow_by_id: Dict[str, Path] = {}
    workflow_by_stem: Dict[str, Path] = {}
    resolved_refs: Dict[str, str] = {}
    checks: List[Check] = []

    for path in collect_workflow_files(workflows_root):
        if path.name == "README.md":
            continue
        try:
            payload = read_yaml(path)
        except Exception:
            checks.append(Check(name=f"workflow_index_parse:{path}", ok=False, detail=f"invalid YAML: {path}"))
            continue

        if not is_mapping(payload):
            checks.append(Check(name=f"workflow_index_mapping:{path}", ok=False, detail="top-level is not mapping"))
            continue

        wf_id = payload.get("id")
        if not isinstance(wf_id, str) or not wf_id:
            checks.append(Check(name=f"workflow_index_id:{path}", ok=False, detail="missing id"))
            continue

        if wf_id in workflow_by_id:
            checks.append(Check(
                name=f"workflow_index_duplicate_id:{wf_id}",
                ok=False,
                detail=f"duplicated workflow id mapped to {workflow_by_id[wf_id]} and {path}",
            ))
            continue
        workflow_by_id[wf_id] = path

        stem = path.stem
        if stem in workflow_by_stem and workflow_by_stem[stem] != path:
            checks.append(Check(
                name=f"workflow_index_duplicate_stem:{stem}",
                ok=False,
                detail=f"duplicated filename stem {stem}: {workflow_by_stem[stem]} / {path}",
            ))
            continue
        workflow_by_stem[stem] = path

        rel = str(path.relative_to(workflows_root))
        resolved_refs[rel[:-5]] = str(path)
        if rel.startswith("pipelines/"):
            resolved_refs[rel[:-5]] = str(path)

    checks.append(Check(name="workflow_index_complete", ok=True, detail=f"loaded {len(workflow_by_id)} workflow artifacts"))
    return workflow_by_id, workflow_by_stem, resolved_refs, checks


def validate_workflow_schema(path: Path, check_files: bool = False) -> Result:
    result = Result(passed=True, target=str(path), kind="workflow")
    try:
        data = read_yaml(path)
    except Exception as e:
        result.add("yaml_parse", False, str(e))
        return result

    result.add("is_mapping", is_mapping(data))
    if not is_mapping(data):
        return result

    for k in WORKFLOW_REQUIRED_KEYS:
        result.add(f"required:{k}", k in data, f"missing required key: {k}")

    wf_id = data.get("id")
    result.add("id_type", isinstance(wf_id, str), f"must be non-empty string, got {type(wf_id).__name__}")
    if isinstance(wf_id, str):
        result.add("id_pattern", is_id(wf_id), f"id={wf_id!r} not in kebab-case")

    layer = data.get("layer", "")
    result.add("layer_valid", layer in WORKFLOW_LAYERS, f"got {layer!r}, expected one of {sorted(WORKFLOW_LAYERS)}")

    desc = data.get("description")
    result.add("description", isinstance(desc, str) and bool(desc.strip()))

    result.add("inputs_is_list", is_str_list(data.get("inputs", [])))
    result.add("outputs_is_list", is_str_list(data.get("outputs", [])))

    skills = data.get("skills")
    result.add("skills_is_list", isinstance(skills, list), "skills must be list")
    if isinstance(skills, list):
        result.add("skills_non_empty", bool(skills), "at least one skill required")
        skill_ids: Set[str] = set()
        for idx, skill in enumerate(skills):
            prefix = f"skills[{idx}]"
            ok = is_mapping(skill)
            result.add(f"{prefix}_mapping", ok, "must be mapping with id/reads/writes")
            if not ok:
                continue
            sid = skill.get("id")
            result.add(f"{prefix}_id", isinstance(sid, str) and bool(sid), "missing skill id")
            if isinstance(sid, str):
                result.add(f"{prefix}_id_uniq", sid not in skill_ids, f"duplicated skill id: {sid}")
                skill_ids.add(sid)
            result.add(f"{prefix}_reads", is_str_list(skill.get("reads", [])), "reads must be string[]")
            result.add(f"{prefix}_writes", is_str_list(skill.get("writes", [])), "writes must be string[]")

            if check_files:
                candidate = path.parent.parent.parent / "skills" / sid if sid else None
                # path.parent => workflows/authoring or /execution or /pipelines
                if isinstance(sid, str):
                    if not candidate.exists():
                        result.add(
                            f"{prefix}_skill_dir_exists",
                            False,
                            f"skill directory missing: {candidate}",
                            warn=False,
                        )

    acceptance = data.get("acceptance")
    result.add("acceptance_is_list", is_str_list(acceptance), "acceptance must be string[]")

    policies = data.get("policies")
    result.add("policies_is_list", isinstance(policies, list), "policies must be list")
    if isinstance(policies, list):
        for idx, p in enumerate(policies):
            result.add(
                f"policies[{idx}]_string",
                isinstance(p, str),
                "policy entry should be string path like policy/ROLE_POLICY.md",
            )
            if isinstance(p, str) and not p.startswith("policy/"):
                result.add(
                    f"policies[{idx}]_prefix",
                    False,
                    f"policy path should start with policy/: {p}",
                    warn=True,
                )

    return result


def parse_condition_expression(expression: str) -> Tuple[bool, List[str], List[str]]:
    expr = expression.strip()
    if not expr:
        return False, [], ["empty expression"]

    clause_re = re.compile(
        r"^\(?\s*(?P<left>[A-Za-z0-9._/-]+)\s*(?:"
        r"(?P<eqop>==|!=)\s*(?P<rhs>\"[^\"]*\"|'[^']*'|[A-Za-z0-9._/-]+|null|true|false|none)"
        r"|(?P<isop>is)\s+(?P<isnot>not\s+)?null"
        r")?\s*\)?$",
        re.IGNORECASE,
    )

    tokens = re.split(r"\s+\b(and|or)\b\s+", expr, flags=re.IGNORECASE)
    if not tokens:
        return False, [], ["unable to split expression"]

    refs: List[str] = []
    errors: List[str] = []

    for i, token in enumerate(tokens):
        if i % 2 == 1:
            if token.lower() not in {"and", "or"}:
                errors.append(f"unsupported logical token: {token}")
            continue
        token = token.strip()
        m = clause_re.fullmatch(token)
        if not m:
            errors.append(f"unsupported clause: {token}")
            continue
        refs.append(m.group("left"))
        if m.group("eqop") is None and m.group("isop") is None:
            # bare literal path check, e.g. "foo" not a complete condition
            errors.append(f"condition requires operator or null-check: {token}")

    return len(errors) == 0, refs, errors


def normalize_condition_ref(candidate: str) -> Set[str]:
    """
    Convert condition subject path to artifact candidates.
    route.decision.yaml.route -> route.decision.yaml
    readiness-report.md.status -> readiness-report.md
    """
    base = candidate.strip()
    if not base:
        return set()
    parts = base.split(".")
    refs = {base}
    if len(parts) > 1:
        refs.add(".".join(parts[:-1]))
    return refs


def get_workflow_outputs(path: Path, data: Optional[dict] = None) -> Tuple[Set[str], Set[str], Set[str]]:
    if data is None:
        data = read_yaml(path)
    out = set(data.get("outputs", []) or [])
    writes: Set[str] = set()
    for s in data.get("skills", []) or []:
        if isinstance(s, dict):
            writes.update([x for x in s.get("writes", []) if isinstance(x, str)])
    return out, writes, set(data.get("inputs", []) or [])


def validate_pipeline_schema(
    path: Path,
    workflow_root: Path,
    strict: bool = False
) -> Result:
    result = Result(passed=True, target=str(path), kind="pipeline")

    try:
        data = read_yaml(path)
    except Exception as e:
        result.add("yaml_parse", False, str(e))
        return result

    result.add("is_mapping", is_mapping(data))
    if not is_mapping(data):
        return result

    for k in PIPELINE_REQUIRED_KEYS:
        result.add(f"required:{k}", k in data, f"missing required key: {k}")

    pid = data.get("id")
    result.add("id_type", isinstance(pid, str), f"id must be string, got {type(pid).__name__}")
    if isinstance(pid, str):
        result.add("id_pattern", is_id(pid), f"id={pid!r} not in kebab-case")

    stages = data.get("stages")
    result.add("stages_is_list", isinstance(stages, list), "stages must be list")
    if not isinstance(stages, list):
        return result
    result.add("stages_non_empty", bool(stages), "pipeline must include at least one stage")

    wf_by_id, wf_by_stem, wf_by_rel, index_checks = build_workflow_index(workflow_root)
    for c in index_checks:
        if c.name.endswith("_complete"):
            result.add(c.name, c.ok, c.detail, warn=False)
        else:
            result.add(c.name, c.ok, c.detail, warn=True)

    known_outputs: Set[str] = set(DEFAULT_CONDITIONAL_ARTIFACTS)
    stage_refs: List[str] = []
    seen_stage_ids: Set[str] = set()
    pipeline_outputs = set(data.get("outputs", []) or [])

    produced_by_any: Set[str] = set()
    output_provenance: Dict[str, List[str]] = {o: [] for o in pipeline_outputs}

    for idx, stage in enumerate(stages):
        if not isinstance(stage, dict):
            result.add(f"stage[{idx}]_mapping", False, "stage must be mapping")
            continue

        ref = stage.get("workflow")
        if not isinstance(ref, str) or not ref:
            result.add(f"stage[{idx}]_workflow", False, "workflow reference missing")
            continue

        stage_id = stage.get("id") or ref
        result.add(f"stage[{idx}]_id_uniq", stage_id not in seen_stage_ids, f"stage id duplicated: {stage_id}")
        seen_stage_ids.add(stage_id)
        stage_refs.append(ref)

        workflow_path: Optional[Path] = None
        if ref.endswith(".yaml"):
            candidate = (workflow_root / ref).resolve()
            if candidate.exists():
                workflow_path = candidate
        else:
            # id-based reference or subpath reference (authoring/xxx)
            if "/" in ref:
                candidate = (workflow_root / f"{ref}.yaml")
                if candidate.exists():
                    workflow_path = candidate
            if workflow_path is None and ref in wf_by_id:
                workflow_path = wf_by_id[ref]
            if workflow_path is None and ref in wf_by_stem:
                workflow_path = wf_by_stem[ref]
            if workflow_path is None and ref in wf_by_rel:
                workflow_path = Path(wf_by_rel[ref])

        if workflow_path is None:
            result.add(f"stage[{idx}]_workflow_ref", False, f"workflow not found: {ref}")
            continue
        result.add(f"stage[{idx}]_workflow_ref", True, f"resolved to {workflow_path}")

        try:
            wf_data = read_yaml(workflow_path)
        except Exception as e:
            result.add(f"stage[{idx}]_workflow_parse", False, f"failed to parse {workflow_path}: {e}")
            continue

        wf_outputs, wf_writes, wf_inputs = get_workflow_outputs(workflow_path, wf_data)
        result.add(f"stage[{idx}]_workflow_id", isinstance(wf_data.get("id"), str), "workflow artifact has id")

        if wf_outputs:
            result.add(f"stage[{idx}]_workflow_outputs", True, f"declares {len(wf_outputs)} outputs")
        else:
            result.add(f"stage[{idx}]_workflow_outputs", False, "workflow has no outputs")

        # Validate declared writes align to outputs if explicit writes exist.
        if wf_outputs and wf_writes:
            missing = wf_writes.difference(wf_outputs)
            if missing:
                result.add(
                    f"stage[{idx}]_writes_subset_outputs",
                    False,
                    f"writes not declared in outputs: {sorted(missing)}",
                )
            else:
                result.add(f"stage[{idx}]_writes_subset_outputs", True, "all writes are outputs")

        # Condition syntax and dependency checks.
        condition = stage.get("condition")
        if condition is not None:
            ok, refs, errors = parse_condition_expression(str(condition))
            result.add(f"stage[{idx}]_condition_syntax", ok, "; ".join(errors) if errors else "")
            for r in refs:
                ref_candidates = normalize_condition_ref(r)
                if not ref_candidates.intersection(known_outputs):
                    result.add(
                        f"stage[{idx}]_condition_dependency",
                        False if strict else True,
                        f"condition {r!r} references unknown artifact at this point",
                        warn=not strict,
                    )

            if not ok:
                result.add(f"stage[{idx}]_condition", False, f"invalid condition: {condition}")
            else:
                result.add(f"stage[{idx}]_condition", True, "condition can be parsed")

        # Track conditionally reachable stages with no static dependency check.
        produced_by_any.update(wf_outputs)
        for out in wf_outputs:
            output_provenance.setdefault(out, [])
            output_provenance[out].append(f"stage[{idx}]")
        known_outputs.update(wf_outputs)
        known_outputs.update(wf_inputs)

    for out in pipeline_outputs:
        if out not in produced_by_any:
            result.add(f"pipeline_output_{out}_reachable", False, f"pipeline output never produced: {out}", warn=True)

    result.add("pipeline_gates", True, f"gates: {len(data.get('gates', []) or [])} raw gate definitions")
    return result


def validate_manifests(root: Path) -> Result:
    result = Result(passed=True, target=str(root), kind="manifests")
    if not root.exists():
        result.add("root_exists", False, f"{root} not found")
        return result

    wf_by_id, wf_by_stem, wf_by_rel, index_checks = build_workflow_index(root)
    for chk in index_checks:
        result.add(chk.name, chk.ok, chk.detail, warn=chk.level == "warn")

    total = len(set(wf_by_id.values()))
    result.add("workflows_discovered", total > 0, f"workflow artifact count: {total}", warn=False)
    if total == 0:
        return result

    # Validate each discovered workflow artifact as a syntax-level contract.
    for p in sorted(set(wf_by_id.values())):
        sub = validate_workflow_schema(p)
        for c in sub.checks:
            # surface as warn for non-fail checks; fail remains fail.
            result.add(f"{p.name}:{c.name}", c.ok, c.detail, warn=c.level == "warn")

    return result


def simulate_pipeline(path: Path, workflow_root: Path, strict: bool = False) -> int:
    result = validate_pipeline_schema(path, workflow_root, strict=strict)
    emit_result(result, as_json=False)
    return 0 if result.passed else 1


def emit_result(result: Result, as_json: bool):
    if as_json:
        payload = {
            "kind": result.kind,
            "target": result.target,
            "pass": result.passed,
            "checks": [
                {
                    "name": c.name,
                    "pass": c.ok,
                    "level": c.level,
                    "detail": c.detail,
                }
                for c in result.checks
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    for check in result.checks:
        if check.ok and check.level == "pass":
            continue
        symbol = "[PASS]" if check.ok else "[WARN]" if check.level == "warn" else "[FAIL]"
        message = f"{symbol} {check.name}"
        if check.detail:
            message += f": {check.detail}"
        print(message)
    if result.passed:
        print(f"[PASS] {result.target}")
    else:
        print(f"[FAIL] {result.target}")


def run_cli(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="workflow_runner.py",
        description="AxiomMd workflow/pipeline schema validator and runner simulator",
    )
    parser.add_argument(
        "--base-dir",
        default=".",
        help="Repository root used for workflow discovery",
    )
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Promote some warnings to hard failures",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Explicitly request dry-run behavior for simulate mode (no side effects)",
    )
    parser.add_argument(
        "mode",
        choices=("validate", "simulate"),
        help="validate: check schema only, simulate: validate then print execution plan",
    )
    parser.add_argument(
        "kind",
        choices=("workflow", "pipeline", "manifests"),
        help="Target schema kind",
    )
    parser.add_argument("path", nargs="?", help="Path to workflow/pipeline file (not required for manifests)")

    args = parser.parse_args(argv)
    base = Path(args.base_dir).resolve()
    workflow_root = (base / "agent" / "workflows").resolve()

    if args.kind in {"workflow", "pipeline"} and not args.path:
        return parser.error(f"{args.kind} requires a YAML path")

    if args.mode == "validate":
        if args.kind == "workflow":
            result = validate_workflow_schema(Path(args.path).resolve(), check_files=True)
        elif args.kind == "pipeline":
            result = validate_pipeline_schema(Path(args.path).resolve(), workflow_root=workflow_root, strict=args.strict)
        else:
            result = validate_manifests(workflow_root)
        emit_result(result, as_json=args.json)
        return 0 if result.passed else 1

    if args.kind != "pipeline":
        return parser.error("simulate mode currently supports only pipeline")

    result = simulate_pipeline(Path(args.path).resolve(), workflow_root=workflow_root, strict=args.strict)
    if not args.json:
        print("\nExecution sequence")
        print("•  " + "\n•  ".join([str(Path(args.path).resolve())]))
        print("No actual side effects are executed. This mode is for plan inspection only.")
    return result


def main():
    code = run_cli()
    raise SystemExit(code)


if __name__ == "__main__":
    main()
