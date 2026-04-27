---
description: Check for drift between CAB plugin extensions and deployed global (~/.claude/) extensions; detects content mismatches and plugin↔global name-collision shadowing (LL-27)
allowed-tools: Read, Bash, Grep, Glob
---

# Sync Check

Shim invoking the `check-sync` skill, which detects drift + LL-27 shadowing
between the CAB plugin (source of truth) and `~/.claude/` deployment.

## Arguments

- (none): Full sync check across agents/skills/commands; both drift and shadow
- `agents` / `skills` / `commands`: Scope to one extension type
- `--shadow-only`: Skip drift report; LL-27 collision scan only (fast)
- `--drift-only`: Skip shadow scan (legacy behavior)

## Examples

```
/sync-check                     # Full report (drift + shadow, all types)
/sync-check agents              # Agents only (drift + shadow)
/sync-check --shadow-only       # Fast LL-27 audit; skip content diff
/sync-check agents --shadow-only
```

## See Also

- `skills/check-sync/` — The workflow skill (owns all logic)
- `knowledge/operational-patterns/multi-agent/agent-resolution.md` —
  precedence + shadowing reference
- LL-27 — plugin↔global name-collision shadowing (the failure mode)
- `/commit-push-pr` — Deploy fixes after resolving drift
