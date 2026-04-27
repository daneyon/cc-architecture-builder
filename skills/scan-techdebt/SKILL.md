---
name: scan-techdebt
description: >-
  Scan codebase for technical debt: code duplication, stale TODO/FIXME markers,
  dead code, consistency drift, and dependency health. Classifies findings as
  auto-fixable, manual-review, or tracked-known. Triggers: tech debt scan,
  end-of-session cleanup, code health check, periodic audit, before refactor.
argument-hint: "Scope path or pattern; flags: --fix, --report-only"
allowed-tools: Read, Bash, Grep, Glob
---

# Tech Debt Scanner

## Purpose

End-of-session (or periodic) actionable scan for technical debt
accumulating across the codebase. Surfaces what can be cleaned up
mechanically vs. what requires architectural judgment, and tracks debt
already acknowledged elsewhere so it isn't re-flagged on every run.

## When to Invoke

- End of a long session, before `close-session` skill runs
- Periodically (weekly/monthly) as hygiene
- Before starting a refactor (so cleanup happens with the refactor, not as
  a separate pass)
- After merging a long-running feature branch (likely accumulated debt)

## Protocol

### Step 1: Scan for Indicators (priority order)

**Duplication**:

```bash
# Use project-specific tools if configured (jscpd, flake8-duplicate, etc.)
# Otherwise hand-spot blocks of >10 nearly-identical lines via grep heuristics
```

**Stale markers** (across code + docs):

```bash
grep -rEn 'TODO|FIXME|HACK|XXX|TEMP|DEPRECATED' \
  --include='*.{py,ts,js,md,sh,go,rs,java}' .
```

**Dead code**:

- Unused imports/exports (project linters when present)
- Unreachable branches (after `if False:` etc.)
- Commented-out code blocks >5 lines (review for delete vs document)

**Consistency drift**:

- Mixed naming conventions (camelCase vs snake_case in same module)
- Inconsistent error-handling patterns
- Missing type annotations (when project uses types elsewhere)

**Dependency health**:

```bash
npm outdated 2>/dev/null
pip list --outdated 2>/dev/null
cargo outdated 2>/dev/null
```

### Step 2: Classify

| Class | Examples | Action |
|---|---|---|
| **Auto-fixable** | Dead imports, formatting, stale TODO with clear resolution in adjacent code | Fix with `--fix` flag, commit |
| **Manual review** | Duplication needing arch decision, deprecated patterns | Report with suggested approach |
| **Tracked already** | Items in `notes/lessons-learned.md`, CLAUDE.md, or open UXL rows | Acknowledge; don't re-surface |

### Step 3: Report

```markdown
## Tech Debt Report — [date]

### Auto-fixable (low risk)
- [item]: file:line — [description]

### Manual Review Required
- [item]: file:line — [description] — [suggested approach]

### Tracked (known debt)
- [item]: [reference to where it's tracked, e.g., UXL-012, LL-15]

### Metrics
- TODO/FIXME count: [n] (delta from last scan: ±[n])
- Duplicate blocks found: [n]
- Stale imports: [n]
- Outdated dependencies: [n] (of which [n] are major-version-behind)
```

### Step 4: Optional Auto-Fix

If `--fix` and user confirms scope, fix auto-fixable items and commit:

```bash
git add <fixed files>
git commit -m "chore: clean up tech debt (auto-fix batch) [scan-techdebt]"
```

Manual-review items never auto-fix — surface and stop.

If `--report-only`, persist the report to `notes/techdebt-YYYY-MM-DD.md`
and exit without modifying any code.

## Arguments

- `$ARGUMENTS` (optional): scope — directory or file pattern. Default:
  entire project root.
- `--fix`: auto-fix low-risk items without per-item prompting
- `--report-only`: report only; persist to `notes/`; do not modify code

## Verification

This skill is working correctly when:

- Auto-fixed items are verifiably safe (e.g., truly-unused imports, not
  imports used only in conditional branches the linter missed)
- "Tracked" classification correctly identifies items already logged in
  `notes/` or CLAUDE.md (no false-new findings)
- Metrics show delta from previous scan (so progress is visible across runs)
- `--report-only` produces a `notes/techdebt-*.md` artifact suitable for
  cross-session reference

## Integration Points

- `commands/techdebt.md` — shim trigger preserving `/cab:techdebt`
- `verifier` agent — quality verification gate
- `commit-push-pr` skill — natural follow-on for fix-batch commits
- `close-session` skill — invoke before session close to capture cleanup
  opportunities into the next session's TODO

## See Also

- `notes/lessons-learned.md` — known-debt cross-reference
- `agents/verifier.md` — independent quality verification
