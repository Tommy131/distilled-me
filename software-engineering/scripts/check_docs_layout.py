#!/usr/bin/env python3
"""Validate documentation placement (software-engineering 文档落盘铁律).

Fail if generated markdown (or other docs) sit in the repo root or under source
trees instead of docs/. README* and a small allowlist of root tool files are OK.

Usage:
  python check_docs_layout.py [REPO_ROOT]
  python check_docs_layout.py --extra-root-allow LICENSE.md NOTICE.md

Exit codes: 0 ok, 1 violations, 2 usage/IO error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

DEFAULT_ROOT_ALLOW = {
    "readme",
    "readme.md",
    "license",
    "license.md",
    "licence",
    "licence.md",
    "claude.md",
    "contributing.md",
    "code_of_conduct.md",
    "security.md",  # GitHub security policy often lives at root
    "agents.md",
    "skill.md",  # Agent skill entry (this playbook / project skills)
}

SOURCE_DIR_NAMES = {
    "src",
    "lib",
    "app",
    "apps",
    "packages",
    "internal",
    "cmd",
    "pkg",
}

DOC_SUFFIXES = {".md", ".mdx", ".rst", ".adoc"}

SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "out",
    "target",
    "coverage",
    "__pycache__",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
    ".idea",
    ".vscode",
    ".cursor",
    ".claude",
    ".grok",
    ".agents",
}


def is_readme(name: str) -> bool:
    lower = name.lower()
    return lower == "readme" or lower.startswith("readme.")


def normalize_allow(names: list[str]) -> set[str]:
    return {n.lower() for n in names}


def collect_violations(root: Path, extra_allow: set[str]) -> list[str]:
    allow = {a.lower() for a in DEFAULT_ROOT_ALLOW} | extra_allow
    violations: list[str] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        parts = rel.parts
        if any(p in SKIP_DIR_NAMES for p in parts[:-1]):
            continue
        if path.suffix.lower() not in DOC_SUFFIXES and path.name.lower() not in {
            "readme",
            "license",
            "licence",
        }:
            # only flag documentation-like files
            if path.suffix.lower() not in DOC_SUFFIXES:
                continue

        # Root-level docs
        if len(parts) == 1:
            name = parts[0]
            if is_readme(name):
                continue
            if name.lower() in allow:
                continue
            violations.append(f"root doc not allowed: {rel.as_posix()} (move to docs/)")
            continue

        # Docs under source trees
        if parts[0].lower() in SOURCE_DIR_NAMES:
            # allow README next to packages
            if is_readme(parts[-1]):
                continue
            violations.append(
                f"doc under source tree: {rel.as_posix()} (move to docs/ or keep only README*)"
            )

    return sorted(violations)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "repo_root",
        nargs="?",
        default=".",
        help="Repository root to scan (default: cwd)",
    )
    parser.add_argument(
        "--extra-root-allow",
        nargs="*",
        default=[],
        help="Additional basenames allowed at repo root",
    )
    args = parser.parse_args(argv)

    root = Path(args.repo_root).resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    try:
        violations = collect_violations(root, normalize_allow(args.extra_root_allow))
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not violations:
        print(f"OK: docs layout clean under {root}")
        return 0

    print(f"FAIL: {len(violations)} docs layout violation(s) under {root}")
    for item in violations:
        print(f"  - {item}")
    print(
        "Hint: generated docs MUST live under docs/ "
        "(README* and tool-required root files excepted)."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
