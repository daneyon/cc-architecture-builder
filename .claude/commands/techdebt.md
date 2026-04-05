---
description: Scan codebase for technical debt including code duplication, unused exports, TODO/FIXME markers, and common anti-patterns. Run at end of session or periodically.
allowed-tools: Read, Bash, Grep, Glob
---

# Tech Debt Scanner

End-of-session (or periodic) scan for technical debt. Identifies actionable
cleanup opportunities and optionally fixes low-risk items automatically.

## Behavior

1. **Scan for indicators** (in priority order):

   **Duplication**:
   ```bash
   # Find duplicate/near-duplicate code blocks (>10 lines)
   # Use project-specific tools if available (jscpd, flake8-duplicate, etc.)
   ```

   **Stale markers**:
   ```bash
   grep -rn "TODO\|FIXME\|HACK\|XXX\|TEMP\|DEPRECATED" --include="*.{py,ts,js,md}" .
   ```

   **Dead code**:
   - Unused imports/exports
   - Unreachable branches
   - Commented-out code blocks (>5 lines)

   **Consistency issues**:
   - Mixed naming conventions
   - Inconsistent error handling patterns
   - Missing type annotations (if project uses types)

   **Dependency health**:
   ```bash
   # Check for outdated dependencies if package manager available
   npm outdated 2>/dev/null || pip list --outdated 2>/dev/null
   ```

2. **Classify findings**:
   - **Auto-fixable**: Dead imports, simple formatting, stale TODO with clear resolution
   - **Manual review**: Duplication requiring architectural decision, deprecated patterns
   - **Track only**: Known debt acknowledged in CLAUDE.md or notes/

3. **Report**:
   ```markdown
   ## Tech Debt Report — [date]

   ### Auto-fixable (low risk)
   - [item]: [file:line] — [description]

   ### Manual Review Required
   - [item]: [file:line] — [description] — [suggested approach]

   ### Tracked (known debt)
   - [item]: [reference to where it's tracked]

   ### Metrics
   - TODO/FIXME count: [n]
   - Duplicate blocks found: [n]
   - Stale imports: [n]
   ```

4. **Optional auto-fix**: If user confirms, fix auto-fixable items and commit:
   ```bash
   git commit -m "chore: clean up tech debt (auto-fix batch)"
   ```

## Arguments

- `$ARGUMENTS` (optional): Scope — directory or file pattern to scan. Default: entire project.
- `--fix`: Auto-fix low-risk items without prompting
- `--report-only`: Generate report without fixing anything

## Examples

```
/techdebt
→ Full project scan, report, ask before fixing

/techdebt src/api/
→ Scan only the API directory

/techdebt --fix
→ Scan and auto-fix low-risk items

/techdebt --report-only
→ Generate report to notes/techdebt-[date].md
```

## See Also

- `.claude/agents/verifier.md` — Quality verification
- `/commit-push-pr` — Commit fixes after cleanup
