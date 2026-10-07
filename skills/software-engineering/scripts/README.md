# Bundled check scripts

Copy these into a project `scripts/` directory or invoke by absolute path from this skill.

| Script | Purpose |
|--------|---------|
| `check_docs_layout.py` | Enforce docs-in-`docs/` placement (root/source-tree scatter fails) |
| `check_i18n.py` | Locale key parity, placeholder alignment, no empty strings |

```bash
python scripts/check_docs_layout.py /path/to/repo
python scripts/check_docs_layout.py /path/to/repo --extra-root-allow SUPPORT.md

python scripts/check_i18n.py /path/to/locales --baseline en
```

Exit code `0` = pass, `1` = violations, `2` = usage/IO/parse errors.
