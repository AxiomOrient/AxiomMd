#!/usr/bin/env python3
"""Validate that a scoped artifact covers the minimum operational categories."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Heading:
    level: int
    title: str
    start: int
    end: int


CATEGORY_PATTERNS = {
    "scope": [
        r"\bscope\b",
        r"scoped artifact",
        r"artifact type",
        r"intended use",
        r"in scope",
        r"out of scope",
        r"non-goals?",
    ],
    "evidence": [
        r"current reality",
        r"current state",
        r"current behavior",
        r"source[- ]of[- ]truth",
        r"evidence",
        r"existing behavior",
        r"repo evidence",
    ],
    "target_delta": [
        r"target delta",
        r"delta",
        r"what must change",
        r"proposed change",
        r"proposed contract",
        r"change summary",
        r"intended change",
    ],
    "omissions": [
        r"\bomitted\b",
        r"\bnot applicable\b",
        r"\bn/?a\b",
        r"\bstandard areas\b",
        r"\bstandard sections\b",
        r"\bcanonical areas\b",
        r"\bcanonical sections\b",
        r"\bcoverage map\b",
    ],
    "boundaries": [
        r"boundar(y|ies)",
        r"approval",
        r"always do",
        r"ask first",
        r"never do",
        r"touch restrictions?",
    ],
    "failures": [
        r"failure",
        r"risk",
        r"recovery",
        r"rollback",
        r"hazard",
        r"error handling",
    ],
    "validation": [
        r"validation",
        r"success criteria",
        r"definition of done",
        r"acceptance",
        r"commands?",
        r"tests?",
    ],
}

OPTIONAL_PATTERNS = {
    "open_or_assumptions": [
        r"\bopen\b",
        r"assumptions?",
        r"unknowns?",
        r"decision needed",
    ]
}

PATHISH_RE = re.compile(r"`[^`]+`|\b[\w./-]+\.[A-Za-z0-9]+\b|\b[\w./-]+/[\w./-]+")
COMMANDISH_RE = re.compile(r"`[^`]+`|\b(test|pytest|npm|pnpm|yarn|cargo|go test|make|python|uv)\b", re.I)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)

REQUIRED_KEYS = [
    "scope",
    "evidence",
    "target_delta",
    "omissions",
    "boundaries",
    "failures",
    "validation",
]


def parse_headings(lines: list[str]) -> list[Heading]:
    matches: list[tuple[int, int, str]] = []
    for idx, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            matches.append((idx, len(match.group(1)), match.group(2).strip()))

    headings: list[Heading] = []
    for index, (start, level, title) in enumerate(matches):
        end = len(lines)
        for next_start, next_level, _ in matches[index + 1 :]:
            if next_level <= level:
                end = next_start
                break
        headings.append(Heading(level=level, title=title, start=start, end=end))
    return headings


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def heading_matches(title: str, patterns: Iterable[str]) -> bool:
    value = normalize(title)
    return any(re.search(pattern, value, re.I) for pattern in patterns)


def content_match_score(content: str, patterns: Iterable[str]) -> int:
    value = normalize(content)
    return sum(1 for pattern in patterns if re.search(pattern, value, re.I))


def content_for_heading(lines: list[str], heading: Heading) -> str:
    return "\n".join(lines[heading.start + 1 : heading.end]).strip()


def has_frontmatter_key(frontmatter: str, *keys: str) -> bool:
    lowered = frontmatter.lower()
    return any(f"{key.lower()}:" in lowered for key in keys)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_scoped_artifact.py <path/to/artifact.md>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"[FAIL] file not found: {path}")
        return 1

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    numbered_headers = re.findall(r"^##\s+(\d+)\.\s", text, re.M)
    if numbered_headers[:18] == [str(index) for index in range(1, 19)]:
        print(f"[FAIL] {path}")
        print(" - file appears to be a full 18-section spec; use check_spec_standard.py instead")
        return 1

    frontmatter_match = FRONTMATTER_RE.match(text)
    frontmatter = frontmatter_match.group(1) if frontmatter_match else ""

    headings = parse_headings(lines)
    matched: dict[str, tuple[str, str]] = {}
    warnings: list[str] = []
    errors: list[str] = []

    for category, patterns in CATEGORY_PATTERNS.items():
        for heading in headings:
            content = content_for_heading(lines, heading)
            if heading_matches(heading.title, patterns) and content:
                matched[category] = (heading.title, content)
                break
        if category in matched:
            continue
        content_headings = [heading for heading in headings if heading.level > 1] or headings
        best_match: tuple[int, int, str, str] | None = None
        for heading in content_headings:
            content = content_for_heading(lines, heading)
            if not content:
                continue
            score = content_match_score(content, patterns)
            if score <= 0:
                continue
            candidate = (score, heading.level, heading.title, content)
            if best_match is None or candidate > best_match:
                best_match = candidate
        if best_match is not None:
            _, _, title, content = best_match
            matched[category] = (title, content)

    if "scope" not in matched:
        if has_frontmatter_key(frontmatter, "scoped", "artifact_type", "scope") or re.search(r"\bscoped artifact\b", text, re.I):
            matched["scope"] = ("frontmatter/body", frontmatter or text)

    if "omissions" not in matched:
        if has_frontmatter_key(frontmatter, "omitted_standard_sections", "omitted_canonical_sections", "omitted_sections", "not_applicable"):
            matched["omissions"] = ("frontmatter", frontmatter)

    for category in REQUIRED_KEYS:
        if category not in matched:
            errors.append(f"missing required coverage category: {category}")

    for optional_name, patterns in OPTIONAL_PATTERNS.items():
        for heading in headings:
            if heading_matches(heading.title, patterns):
                matched[optional_name] = (heading.title, content_for_heading(lines, heading))
                break

    if "scope" in matched:
        _, content = matched["scope"]
        if not re.search(r"\bscoped\b|\bin scope\b|\bout of scope\b|\bnon-goal\b", content, re.I):
            warnings.append("scope coverage exists, but the artifact does not explicitly say it is scoped or bounded")

    if "evidence" in matched:
        _, content = matched["evidence"]
        if not PATHISH_RE.search(content):
            warnings.append("evidence section exists, but it does not appear to cite a concrete path, file, or command")

    if "validation" in matched:
        _, content = matched["validation"]
        if not COMMANDISH_RE.search(content):
            warnings.append("validation section exists, but no obvious command or concrete validation signal was detected")

    if "open_or_assumptions" not in matched and re.search(r"\bopen\b|\bassumption\b", text, re.I) is None:
        warnings.append("no explicit OPEN or assumptions section found; this is fine only if no blockers or assumptions remain")

    if errors:
        print(f"[FAIL] {path}")
        for error in errors:
            print(f" - {error}")
        if warnings:
            print("[WARNINGS]")
            for warning in warnings:
                print(f" - {warning}")
        return 1

    print(f"[OK] {path}")
    print(" - required scoped coverage categories present")
    if warnings:
        print("[WARNINGS]")
        for warning in warnings:
            print(f" - {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
