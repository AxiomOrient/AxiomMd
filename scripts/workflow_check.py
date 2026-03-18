#!/usr/bin/env python3
"""
workflow_check.py — single-entry-point validator for AxiomMd workflow artifacts.

Subcommands:
  packet             input.packet.yaml
  route              route.decision.yaml
  framing            product-charter.md + system-blueprint.md
  authoring-request  authoring.request.yaml
  handoff            handoff.packet.yaml (any stage)
  package            feature package directory
  pipeline           run all applicable checks in a workflow directory

Options:
  --json             Machine-readable JSON output (for AI agent consumers)
  --base-dir PATH    Base directory for resolving local file paths in refs
  --strict           Tighter constraints (e.g. target_kind must be feature-package)

Exit: 0 = all pass, 1 = any fail.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    sys.exit("[ERROR] PyYAML not installed. Run: pip install pyyaml")


# ── Result types ─────────────────────────────────────────────────────────────

@dataclass
class Check:
    name: str
    passed: bool
    level: str = "fail"   # "fail" | "warn" | "info"
    detail: str = ""


@dataclass
class Result:
    passed: bool
    target: str
    stage: str
    checks: list = field(default_factory=list)

    def add(self, name: str, ok: bool, detail: str = "", warn: bool = False):
        level = "info" if ok else ("warn" if warn else "fail")
        self.checks.append(Check(name=name, passed=ok, level=level, detail=detail))
        if not ok and not warn:
            self.passed = False
        return ok


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def is_local(ref: str) -> bool:
    return not str(ref).startswith(("http://", "https://", "git@"))


def resolve_path(ref: str, base_dir: Path) -> Optional[Path]:
    if not is_local(ref):
        return None
    return (base_dir / ref).resolve()


def section_content(text: str, token: str) -> str:
    """Content after the heading containing token, up to the next heading."""
    idx = text.find(token)
    if idx == -1:
        return ""
    nl = text.find("\n", idx)
    if nl == -1:
        return ""
    rest = text[nl + 1:]
    m = re.search(r"^#+\s", rest, re.MULTILINE)
    return rest[: m.start()].strip() if m else rest.strip()


# ── Emitter ───────────────────────────────────────────────────────────────────

def emit(result: Result, as_json: bool):
    if as_json:
        def _check_dict(c: Check) -> dict:
            d: dict = {"name": c.name, "pass": c.passed, "level": c.level}
            if c.detail and (not c.passed or c.level == "warn"):
                d["detail"] = c.detail
            return d
        print(json.dumps({
            "pass": result.passed,
            "target": result.target,
            "stage": result.stage,
            "checks": [_check_dict(c) for c in result.checks],
        }, ensure_ascii=False, indent=2))
    else:
        for c in result.checks:
            tag = "[PASS]" if c.passed else ("[WARN]" if c.level == "warn" else "[FAIL]")
            show_detail = c.detail and (not c.passed or c.level == "warn")
            line = f"{tag} {c.name}" + (f": {c.detail}" if show_detail else "")
            print(line)
        print(f"\n{'[PASS]' if result.passed else '[FAIL]'} {result.target}")


# ── packet ────────────────────────────────────────────────────────────────────

REQUIRED_PACKET_KEYS = [
    "packet_version", "request_summary", "target_kind",
    "source_context_refs", "output_contract_refs",
    "scope", "constraints", "done_signals", "open_questions", "evidence_refs",
]

def check_packet(path: Path, strict: bool = False) -> Result:
    r = Result(passed=True, target=str(path), stage="packet")
    if not r.add("file_exists", path.exists(), f"not found: {path}"):
        return r
    try:
        data = load_yaml(path)
    except Exception as e:
        r.add("yaml_parse", False, str(e)); return r
    r.add("yaml_parse", True)
    if not r.add("is_mapping", isinstance(data, dict), "must be a YAML mapping"):
        return r

    for k in REQUIRED_PACKET_KEYS:
        r.add(f"key_{k}", k in data, f"missing key: {k}")

    r.add("packet_version_is_1", data.get("packet_version") == 1,
          f"got: {data.get('packet_version')!r}")

    if strict:
        r.add("target_kind_feature_package",
              data.get("target_kind") == "feature-package",
              f"got: {data.get('target_kind')!r}")

    scope = data.get("scope")
    if isinstance(scope, dict):
        r.add("scope_in_is_list",  isinstance(scope.get("in"),  list))
        r.add("scope_out_is_list", isinstance(scope.get("out"), list))
        r.add("scope_in_non_empty", bool(scope.get("in")),
              "scope.in should not be empty", warn=True)
    else:
        r.add("scope_is_mapping", False, "scope must be a mapping")

    for k in ["source_context_refs", "output_contract_refs",
              "constraints", "done_signals", "open_questions", "evidence_refs"]:
        r.add(f"{k}_is_list", isinstance(data.get(k), list))

    if isinstance(data.get("constraints"), list):
        r.add("constraints_non_empty", bool(data["constraints"]))
    if isinstance(data.get("done_signals"), list):
        r.add("done_signals_non_empty", bool(data["done_signals"]))

    r.add("has_context_or_evidence",
          bool(data.get("source_context_refs")) or bool(data.get("evidence_refs")),
          "at least one of source_context_refs or evidence_refs must be non-empty")

    if strict and isinstance(data.get("output_contract_refs"), list):
        r.add("output_contract_refs_non_empty", bool(data["output_contract_refs"]))

    return r


# ── route ─────────────────────────────────────────────────────────────────────

ALLOWED_ROUTES = {"direct-package", "framing-first", "hold"}
REQUIRED_ROUTE_KEYS = [
    "packet_version", "input_ref", "route", "reason_summary",
    "required_artifacts", "next_step", "open_questions", "blockers",
]

def check_route(path: Path) -> Result:
    r = Result(passed=True, target=str(path), stage="route")
    if not r.add("file_exists", path.exists(), f"not found: {path}"):
        return r
    try:
        data = load_yaml(path)
    except Exception as e:
        r.add("yaml_parse", False, str(e)); return r
    r.add("yaml_parse", True)
    for k in REQUIRED_ROUTE_KEYS:
        r.add(f"key_{k}", isinstance(data, dict) and k in data, f"missing: {k}")
    if not isinstance(data, dict):
        return r

    r.add("packet_version_is_1", data.get("packet_version") == 1)
    route = data.get("route")
    r.add("route_enum", route in ALLOWED_ROUTES,
          f"got: {route!r}, allowed: {sorted(ALLOWED_ROUTES)}")
    r.add("input_ref_non_empty",    bool(data.get("input_ref")))
    r.add("reason_summary_non_empty", bool(data.get("reason_summary")))
    r.add("next_step_non_empty",    bool(data.get("next_step")))
    for k in ["required_artifacts", "open_questions", "blockers"]:
        r.add(f"{k}_is_list", isinstance(data.get(k), list))
    if route == "framing-first":
        r.add("framing_first_has_required_artifacts", bool(data.get("required_artifacts")),
              "framing-first requires required_artifacts non-empty")
    if route == "hold":
        r.add("hold_has_blockers", bool(data.get("blockers")),
              "hold requires blockers non-empty")
    return r


# ── framing ───────────────────────────────────────────────────────────────────

CHARTER_SECTIONS  = ["Problem", "Users", "Goals", "Non-Goals", "Success", "Constraints"]
BLUEPRINT_SECTIONS = ["Boundary", "Major Components", "Primary Flow",
                      "Source Of Truth", "Current Scope"]
MIN_SECTION_CHARS = 20

def check_framing(charter_path: Path, blueprint_path: Path) -> Result:
    r = Result(passed=True, target=f"{charter_path} + {blueprint_path}", stage="framing")
    for path, label, sections in [
        (charter_path,   "charter",   CHARTER_SECTIONS),
        (blueprint_path, "blueprint", BLUEPRINT_SECTIONS),
    ]:
        if not r.add(f"{label}_file_exists", path.exists(), f"not found: {path}"):
            continue
        text = path.read_text(encoding="utf-8")
        for token in sections:
            key = token.lower().replace(" ", "_").replace("-", "_")
            if r.add(f"{label}_has_{key}", token in text,
                     f"missing section: {token}"):
                content = section_content(text, token)
                r.add(f"{label}_{key}_has_content", len(content) >= MIN_SECTION_CHARS,
                      f"section '{token}' has < {MIN_SECTION_CHARS} chars", warn=True)
    return r


# ── authoring-request ─────────────────────────────────────────────────────────

REQUIRED_AUTHORING_KEYS = [
    "feature_id", "slug", "title", "implementation_order",
    "profile_key", "review_mode", "planes", "owner_roles",
    "target_repos", "adoption", "target_feature_path", "mode",
]
ALLOWED_PLANES   = {"source", "compile", "execution", "control", "governance", "reconcile"}
FEATURE_ID_RE    = re.compile(r"^FEAT-\d{4}$")

def check_authoring_request(path: Path) -> Result:
    r = Result(passed=True, target=str(path), stage="authoring-request")
    if not r.add("file_exists", path.exists(), f"not found: {path}"):
        return r
    try:
        data = load_yaml(path)
    except Exception as e:
        r.add("yaml_parse", False, str(e)); return r
    r.add("yaml_parse", True)
    for k in REQUIRED_AUTHORING_KEYS:
        r.add(f"key_{k}", isinstance(data, dict) and k in data, f"missing: {k}")
    if not isinstance(data, dict):
        return r

    fid = str(data.get("feature_id", ""))
    r.add("feature_id_non_empty", bool(fid))
    r.add("feature_id_format", bool(FEATURE_ID_RE.match(fid)),
          f"must match FEAT-NNNN, got: {fid!r}")
    r.add("slug_non_empty",  bool(data.get("slug")))
    r.add("title_non_empty", bool(data.get("title")))
    r.add("implementation_order_numeric",
          isinstance(data.get("implementation_order"), (int, float)),
          f"got type: {type(data.get('implementation_order')).__name__}")
    r.add("profile_key_non_empty", bool(data.get("profile_key")))
    r.add("review_mode_non_empty", bool(data.get("review_mode")))

    for k in ["planes", "owner_roles", "target_repos"]:
        val = data.get(k)
        r.add(f"{k}_non_empty_list", isinstance(val, list) and bool(val))

    planes = data.get("planes", [])
    if isinstance(planes, list):
        unknown = [p for p in planes if p not in ALLOWED_PLANES]
        r.add("planes_valid_values", not unknown,
              f"unknown: {unknown}, allowed: {sorted(ALLOWED_PLANES)}")

    r.add("adoption_is_mapping", isinstance(data.get("adoption"), dict))
    r.add("target_feature_path_non_empty", bool(data.get("target_feature_path")))
    r.add("mode_is_create_or_update",
          data.get("mode") in {"create", "update"},
          f"got: {data.get('mode')!r}")
    return r


# ── handoff ───────────────────────────────────────────────────────────────────

ALLOWED_STAGES = {
    "intake-and-routing", "framing", "feature-package-authoring",
    "readiness-and-handoff", "execution", "verification", "reconcile",
}
ALLOWED_STATUSES = {"ready", "patch-required", "hold", "blocked"}
REQUIRED_HANDOFF_KEYS = [
    "packet_version", "stage", "status", "input_ref",
    "changed_paths", "produced_paths", "evidence_refs",
    "open_questions", "next_step", "blockers",
]

def check_handoff(path: Path, base_dir: Optional[Path] = None,
                  required_stage: Optional[str] = None) -> Result:
    r = Result(passed=True, target=str(path), stage="handoff")
    if not r.add("file_exists", path.exists(), f"not found: {path}"):
        return r
    try:
        data = load_yaml(path)
    except Exception as e:
        r.add("yaml_parse", False, str(e)); return r
    r.add("yaml_parse", True)
    for k in REQUIRED_HANDOFF_KEYS:
        r.add(f"key_{k}", isinstance(data, dict) and k in data, f"missing: {k}")
    if not isinstance(data, dict):
        return r

    r.add("packet_version_is_1", data.get("packet_version") == 1)

    stage = data.get("stage")
    r.add("stage_enum", stage in ALLOWED_STAGES, f"got: {stage!r}")
    if required_stage:
        r.add("stage_matches_expected", stage == required_stage,
              f"expected: {required_stage!r}, got: {stage!r}")

    r.add("status_enum", data.get("status") in ALLOWED_STATUSES,
          f"got: {data.get('status')!r}")
    r.add("input_ref_non_empty", bool(data.get("input_ref")))
    r.add("next_step_non_empty", bool(data.get("next_step")))

    for k in ["changed_paths", "produced_paths", "evidence_refs", "open_questions", "blockers"]:
        r.add(f"{k}_is_list", isinstance(data.get(k), list))

    r.add("produced_paths_non_empty", bool(data.get("produced_paths")))
    r.add("evidence_refs_non_empty",  bool(data.get("evidence_refs")))

    if base_dir is None:
        r.add("path_existence_skipped", True,
              "no --base-dir; skipping file existence checks", warn=True)
    else:
        input_ref = data.get("input_ref", "")
        if is_local(input_ref):
            p = resolve_path(input_ref, base_dir)
            if p and not p.exists():
                r.add("input_ref_exists", False,
                      f"not found: {input_ref}", warn=True)

        for ref in data.get("produced_paths", []):
            if is_local(ref):
                p = resolve_path(ref, base_dir)
                if p and not p.exists():
                    r.add("produced_paths_exist", False,
                          f"not found on disk: {ref}")

        for ref in data.get("evidence_refs", []):
            if is_local(ref):
                p = resolve_path(ref, base_dir)
                if p and not p.exists():
                    r.add("evidence_refs_exist", False,
                          f"not found: {ref}", warn=True)
    return r


# ── package ───────────────────────────────────────────────────────────────────

REQUIRED_PACKAGE_FILES = [
    "intent.md", "package.yaml", "requirements.yaml", "invariants.yaml",
    "design.md", "tasks.md", "evals.yaml", "risks.yaml",
    "decisions.jsonl", "contracts",
]

REQUIRED_PACKAGE_KEYS = ["feature_id", "title", "state", "review_mode"]

DESIGN_REQUIRED_SECTIONS = [
    ("Boundary",           ["Boundary", "Boundaries"]),
    ("Data and State",     ["Data and State", "Data / State"]),
    ("Interfaces",         ["Interfaces"]),
    ("Failure Modes",      ["Failure Modes"]),
    ("Requirement mapping",["Requirement mapping", "Mapping to Requirements"]),
]


def _parse_tasks(tasks_path: Path) -> list:
    raw = tasks_path.read_text(encoding="utf-8")
    try:
        parsed = yaml.safe_load(raw)
        if isinstance(parsed, dict) and isinstance(parsed.get("tasks"), list):
            return [
                {
                    "id":        t.get("id"),
                    "req_ids":   list(t.get("req_ids") or []),
                    "eval_ids":  list(t.get("eval_ids") or []),
                    "paths":     list(t.get("touched_paths") or t.get("paths") or []),
                    "done_when": t.get("done_when") or t.get("next"),
                }
                for t in parsed["tasks"]
            ]
    except Exception:
        pass
    # Fallback: parse markdown
    task_ids = list(dict.fromkeys(re.findall(r"TASK-\d+", raw)))
    tasks = []
    for tid in task_ids:
        m = re.search(rf"{re.escape(tid)}.*?(?=\n- \[|\Z)", raw, re.DOTALL)
        block = m.group(0) if m else ""
        pm = re.search(r"paths:\s*\[(.*?)\]", block, re.DOTALL)
        paths = [p.strip() for p in pm.group(1).split(",") if p.strip()] if pm else []
        dm = re.search(r"done_when:\s*(.+)$", block, re.MULTILINE)
        tasks.append({
            "id":        tid,
            "req_ids":   list(dict.fromkeys(re.findall(r"REQ-\d+", block))),
            "eval_ids":  list(dict.fromkeys(re.findall(r"EVAL-\d+", block))),
            "paths":     paths,
            "done_when": dm.group(1) if dm else None,
        })
    return tasks


def check_package(pkg_dir: Path, base_dir: Optional[Path] = None) -> Result:
    r = Result(passed=True, target=str(pkg_dir), stage="package")
    if not r.add("dir_exists", pkg_dir.exists(), f"not found: {pkg_dir}"):
        return r

    for fname in REQUIRED_PACKAGE_FILES:
        key = fname.replace(".", "_").replace("/", "_")
        r.add(f"file_{key}", (pkg_dir / fname).exists(), f"missing: {fname}")

    # package.yaml
    meta: dict = {}
    pkg_yaml = pkg_dir / "package.yaml"
    if pkg_yaml.exists():
        try:
            raw = load_yaml(pkg_yaml)
            meta = raw.get("feature", raw) if isinstance(raw, dict) else {}
            r.add("package_yaml_is_mapping", isinstance(meta, dict))
            if isinstance(meta, dict):
                for k in REQUIRED_PACKAGE_KEYS:
                    present = k in meta or (k == "feature_id" and "id" in meta)
                    r.add(f"package_key_{k}", present, f"package.yaml missing: {k}")
        except Exception as e:
            r.add("package_yaml_parse", False, str(e))

    # requirements.yaml
    req_ids: list = []
    blocking_by_req: dict = {}
    reqs_path = pkg_dir / "requirements.yaml"
    reqs: list = []
    if reqs_path.exists():
        try:
            rd = load_yaml(reqs_path)
            reqs = rd.get("requirements") if isinstance(rd, dict) else None  # type: ignore
            r.add("requirements_list", isinstance(reqs, list) and bool(reqs),
                  "must contain non-empty requirements list")
            if isinstance(reqs, list):
                for req in reqs:
                    if isinstance(req, dict):
                        r.add("req_has_id",       bool(req.get("id")),       "each requirement must have id")
                        r.add("req_has_priority",  bool(req.get("priority")),  "each requirement must have priority")
                req_ids = [q.get("id") for q in reqs if isinstance(q, dict) and q.get("id")]
        except Exception as e:
            r.add("requirements_yaml_parse", False, str(e))

    # evals.yaml
    eval_ids: list = []
    evals_path = pkg_dir / "evals.yaml"
    if evals_path.exists():
        try:
            ed = load_yaml(evals_path)
            eval_list = ed.get("evals") if isinstance(ed, dict) else None
            r.add("evals_list", isinstance(eval_list, list) and bool(eval_list),
                  "must contain non-empty evals list")
            if isinstance(eval_list, list):
                eval_ids = [e.get("id") for e in eval_list if isinstance(e, dict) and e.get("id")]
                for ev in eval_list:
                    if isinstance(ev, dict):
                        r.add("eval_has_id",       bool(ev.get("id")),                   "each eval must have id")
                        r.add("eval_has_req_ids",   isinstance(ev.get("req_ids"), list),  "each eval must have req_ids list")
                        r.add("eval_has_task_ids",  isinstance(ev.get("task_ids"), list), "each eval must have task_ids list")
                        if ev.get("blocking") is True or ev.get("kind") == "blocking":
                            for rid in (ev.get("req_ids") or []):
                                blocking_by_req.setdefault(rid, []).append(ev)
        except Exception as e:
            r.add("evals_yaml_parse", False, str(e))

    # must-requirements need a blocking eval
    for req in reqs if isinstance(reqs, list) else []:
        if isinstance(req, dict) and req.get("priority") == "must":
            rid = req.get("id", "?")
            r.add(f"must_req_{rid}_has_blocking_eval",
                  bool(blocking_by_req.get(rid)),
                  f"must requirement {rid} has no blocking eval")

    # invariants.yaml
    inv_path = pkg_dir / "invariants.yaml"
    if inv_path.exists():
        try:
            iv = load_yaml(inv_path)
            r.add("invariants_list",
                  isinstance(iv, dict) and isinstance(iv.get("invariants"), list),
                  "must contain invariants list")
        except Exception as e:
            r.add("invariants_yaml_parse", False, str(e))

    # risks.yaml
    risks_path = pkg_dir / "risks.yaml"
    if risks_path.exists():
        try:
            rk = load_yaml(risks_path)
            r.add("risks_list",
                  isinstance(rk, dict) and isinstance(rk.get("risks"), list),
                  "must contain risks list")
        except Exception as e:
            r.add("risks_yaml_parse", False, str(e))

    # tasks.md
    tasks_path = pkg_dir / "tasks.md"
    if tasks_path.exists():
        tasks = _parse_tasks(tasks_path)
        r.add("tasks_non_empty", bool(tasks), "must contain at least one task")
        for task in tasks:
            tid = task.get("id", "?")
            r.add(f"task_{tid}_has_req_ids",   bool(task.get("req_ids")),                    f"task {tid} missing req_ids")
            r.add(f"task_{tid}_has_eval_ids",  bool(task.get("eval_ids")),                   f"task {tid} missing eval_ids")
            r.add(f"task_{tid}_has_paths",     bool(task.get("paths")),                      f"task {tid} missing paths")
            r.add(f"task_{tid}_has_done_when", bool((task.get("done_when") or "").strip()),   f"task {tid} missing done_when")
            for rid in task.get("req_ids", []):
                r.add(f"task_{tid}_req_{rid}_known", not req_ids or rid in req_ids,
                      f"task {tid} references unknown requirement {rid}")
            for eid in task.get("eval_ids", []):
                r.add(f"task_{tid}_eval_{eid}_known", not eval_ids or eid in eval_ids,
                      f"task {tid} references unknown eval {eid}")

    # design.md sections
    design_path = pkg_dir / "design.md"
    if design_path.exists():
        design_text = design_path.read_text(encoding="utf-8")
        for section_name, tokens in DESIGN_REQUIRED_SECTIONS:
            key = section_name.lower().replace(" ", "_")
            r.add(f"design_has_{key}", any(t in design_text for t in tokens),
                  f"design.md missing section: {section_name}")

    return r


# ── pipeline ──────────────────────────────────────────────────────────────────

def _find(workflow_dir: Path, *names: str) -> Optional[Path]:
    for n in names:
        p = workflow_dir / n
        if p.exists():
            return p
    return None

def check_pipeline(workflow_dir: Path, base_dir: Optional[Path] = None,
                   strict: bool = False) -> Result:
    r = Result(passed=True, target=str(workflow_dir), stage="pipeline")
    stages = 0

    def absorb(sub: Result):
        nonlocal stages
        stages += 1
        for c in sub.checks:
            r.checks.append(c)
        if not sub.passed:
            r.passed = False

    p = _find(workflow_dir, "input.packet.yaml")
    if p:
        absorb(check_packet(p, strict=strict))

    p = _find(workflow_dir, "route.decision.yaml")
    if p:
        absorb(check_route(p))

    charter   = _find(workflow_dir, "product-charter.md")
    blueprint = _find(workflow_dir, "system-blueprint.md")
    if charter and blueprint:
        absorb(check_framing(charter, blueprint))

    p = _find(workflow_dir,
              "charter.framing.handoff.packet.yaml",
              "framing.handoff.packet.yaml",
              "framing-handoff.packet.yaml")
    if p:
        absorb(check_handoff(p, base_dir=base_dir, required_stage="framing"))

    p = _find(workflow_dir,
              "handoff.feature.package.packet.yaml",
              "authoring.handoff.packet.yaml",
              "feature-package-authoring.handoff.packet.yaml")
    if p:
        absorb(check_handoff(p, base_dir=base_dir,
                             required_stage="feature-package-authoring"))

    p = _find(workflow_dir,
              "handoff.readiness.packet.yaml",
              "readiness.handoff.packet.yaml",
              "readiness-handoff.packet.yaml")
    if p:
        absorb(check_handoff(p, base_dir=base_dir,
                             required_stage="readiness-and-handoff"))

    # Generic fallback: filename carries no stage info, so don't enforce required_stage.
    p = _find(workflow_dir, "handoff.packet.yaml")
    if p:
        absorb(check_handoff(p, base_dir=base_dir))

    if stages == 0:
        r.add("artifacts_found", False,
              "no recognizable workflow artifacts in directory")
    return r


# ── CLI ───────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="workflow_check.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--json",     action="store_true", help="Emit JSON (for AI agents)")
    p.add_argument("--base-dir", metavar="PATH",      help="Base dir for local path resolution")
    p.add_argument("--strict",   action="store_true", help="Tighter constraints")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("packet",            help="Validate input.packet.yaml"
                   ).add_argument("path")
    sub.add_parser("route",             help="Validate route.decision.yaml"
                   ).add_argument("path")

    fr = sub.add_parser("framing",      help="Validate charter + blueprint")
    fr.add_argument("charter");  fr.add_argument("blueprint")

    sub.add_parser("authoring-request", help="Validate authoring.request.yaml"
                   ).add_argument("path")
    sub.add_parser("handoff",           help="Validate handoff.packet.yaml"
                   ).add_argument("path")
    sub.add_parser("package",           help="Validate feature package directory"
                   ).add_argument("dir")
    sub.add_parser("pipeline",          help="Run all checks in workflow dir"
                   ).add_argument("dir")
    return p


def main():
    args = build_parser().parse_args()
    base_dir = Path(args.base_dir).resolve() if args.base_dir else None

    cmd = args.cmd
    if cmd == "packet":
        result = check_packet(Path(args.path), strict=args.strict)
    elif cmd == "route":
        result = check_route(Path(args.path))
    elif cmd == "framing":
        result = check_framing(Path(args.charter), Path(args.blueprint))
    elif cmd == "authoring-request":
        result = check_authoring_request(Path(args.path))
    elif cmd == "handoff":
        result = check_handoff(Path(args.path), base_dir=base_dir)
    elif cmd == "package":
        result = check_package(Path(args.dir), base_dir=base_dir)
    elif cmd == "pipeline":
        result = check_pipeline(Path(args.dir), base_dir=base_dir, strict=args.strict)
    else:
        sys.exit(f"Unknown command: {cmd}")

    emit(result, as_json=args.json)
    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
