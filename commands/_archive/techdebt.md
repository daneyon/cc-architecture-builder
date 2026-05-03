---
description: Scan codebase for technical debt — duplication, stale TODO/FIXME, dead code, consistency drift, dependency health
allowed-tools: Read, Bash, Grep, Glob
---

# Tech Debt Scanner

Shim invoking the `scan-techdebt` skill, which performs the multi-category
debt scan + classification + optional auto-fix.

## Arguments

- `$ARGUMENTS` (optional): Scope — directory or file pattern. Default:
  entire project.
- `--fix`: Auto-fix low-risk items without per-item prompting
- `--report-only`: Generate report to `notes/techdebt-[date].md`; do not
  modify any code

## Examples

```
/techdebt                  # Full scan, report, ask before fixing
/techdebt src/api/         # Scan only src/api/
/techdebt --fix            # Scan + auto-fix low-risk items
/techdebt --report-only    # Persist report; no code changes
```

## See Also

- `skills/scan-techdebt/` — The workflow skill (owns all logic)
- `agents/verifier.md` — Quality verification
- `/commit-push-pr` — Commit fixes after cleanup
