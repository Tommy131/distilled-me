#!/usr/bin/env python3
"""Validate flat locale JSON maps for key-set parity and placeholder alignment.

Expects either:
  - a directory of locale files: en.json, zh.json, ... (object of string values), or
  - a directory of locale subdirs each containing *.json maps that are merged.

Usage:
  python check_i18n.py path/to/locales
  python check_i18n.py path/to/locales --baseline en
  python check_i18n.py path/to/i18n --glob "*.json"

Exit codes: 0 ok, 1 violations, 2 usage/IO/parse error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

PLACEHOLDER_RE = re.compile(r"\{(\d+)\}|\{\{(\w+)\}\}|\%(\d+)\$[sd]|\%s|\%d")


def load_json(path: Path) -> Any:
    # utf-8-sig tolerates BOM from Windows editors / PowerShell Set-Content
    with path.open(encoding="utf-8-sig") as fh:
        return json.load(fh)


def flatten_strings(node: Any, prefix: str = "") -> dict[str, str]:
    """Accept flat maps or shallow nested objects; values must be strings."""
    out: dict[str, str] = {}
    if isinstance(node, str):
        if not prefix:
            raise ValueError("root value must be an object map")
        out[prefix] = node
        return out
    if not isinstance(node, dict):
        raise ValueError(f"expected object at '{prefix or '<root>'}', got {type(node).__name__}")
    for key, value in node.items():
        if not isinstance(key, str):
            raise ValueError(f"non-string key at '{prefix}'")
        next_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            out.update(flatten_strings(value, next_key))
        elif isinstance(value, str):
            out[next_key] = value
        elif value is None:
            raise ValueError(f"null value at '{next_key}' (use empty string or omit)")
        else:
            raise ValueError(f"non-string value at '{next_key}' ({type(value).__name__})")
    return out


def placeholders(text: str) -> set[str]:
    found: set[str] = set()
    for m in PLACEHOLDER_RE.finditer(text):
        if m.group(1) is not None:
            found.add(f"idx:{m.group(1)}")
        elif m.group(2) is not None:
            found.add(f"name:{m.group(2)}")
        elif m.group(3) is not None:
            found.add(f"printf:{m.group(3)}")
        else:
            found.add(f"printf:{m.group(0)}")
    return found


def discover_locale_maps(locales_dir: Path, pattern: str) -> dict[str, dict[str, str]]:
    """Return locale_code -> flat key/value map."""
    locales: dict[str, dict[str, str]] = defaultdict(dict)

    # Case A: locales/en.json
    direct = sorted(locales_dir.glob(pattern))
    for path in direct:
        if not path.is_file():
            continue
        code = path.stem
        data = load_json(path)
        locales[code].update(flatten_strings(data))

    # Case B: locales/en/*.json merged
    for sub in sorted(p for p in locales_dir.iterdir() if p.is_dir()):
        if sub.name.startswith("."):
            continue
        files = sorted(sub.glob(pattern))
        if not files:
            continue
        for path in files:
            data = load_json(path)
            flat = flatten_strings(data)
            overlap = set(locales[sub.name]).intersection(flat)
            if overlap:
                sample = next(iter(sorted(overlap)))
                raise ValueError(f"duplicate key '{sample}' while merging {path}")
            locales[sub.name].update(flat)

    return dict(locales)


def validate(
    locales: dict[str, dict[str, str]],
    baseline: str | None,
) -> list[str]:
    issues: list[str] = []
    if not locales:
        return ["no locale files found"]

    codes = sorted(locales)
    base = baseline or ("en" if "en" in locales else codes[0])
    if base not in locales:
        return [f"baseline locale '{base}' not found; have: {', '.join(codes)}"]

    base_keys = set(locales[base])
    if not base_keys:
        issues.append(f"baseline locale '{base}' has zero keys")

    # duplicate detection inside each locale already implied by dict; check empty keys
    for code, mapping in locales.items():
        empties = sorted(k for k, v in mapping.items() if v.strip() == "")
        for key in empties:
            issues.append(f"[{code}] empty string for key '{key}'")

    for code in codes:
        if code == base:
            continue
        keys = set(locales[code])
        missing = sorted(base_keys - keys)
        extra = sorted(keys - base_keys)
        for key in missing:
            issues.append(f"[{code}] missing key '{key}' (present in {base})")
        for key in extra:
            issues.append(f"[{code}] extra key '{key}' (not in {base})")

        for key in sorted(base_keys & keys):
            ph_base = placeholders(locales[base][key])
            ph_other = placeholders(locales[code][key])
            if ph_base != ph_other:
                issues.append(
                    f"[{code}] placeholder mismatch for '{key}': "
                    f"{base}={sorted(ph_base)} vs {code}={sorted(ph_other)}"
                )

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("locales_dir", help="Directory containing locale JSON maps")
    parser.add_argument(
        "--baseline",
        default=None,
        help="Baseline locale code (default: en if present, else first)",
    )
    parser.add_argument(
        "--glob",
        default="*.json",
        dest="pattern",
        help="Glob for locale files (default: *.json)",
    )
    args = parser.parse_args(argv)

    root = Path(args.locales_dir).resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    try:
        locales = discover_locale_maps(root, args.pattern)
        issues = validate(locales, args.baseline)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not issues:
        codes = ", ".join(sorted(locales))
        key_count = len(next(iter(locales.values()))) if locales else 0
        print(f"OK: i18n parity for [{codes}] ({key_count} baseline keys) under {root}")
        return 0

    print(f"FAIL: {len(issues)} i18n issue(s) under {root}")
    for item in issues:
        print(f"  - {item}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
