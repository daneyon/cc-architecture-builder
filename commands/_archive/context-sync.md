---
description: Pull recent project activity from git log, open PRs, issues, and optional MCP sources into a session-bootstrap context summary
allowed-tools: Read, Bash, Grep, Glob
---

# Context Sync

Shim invoking the `sync-context` skill, which pulls recent git/GitHub/MCP
activity into a concise session-bootstrap summary.

## Arguments

- `$1` (optional): Days to look back. Default 7.
- `--git-only`: Skip GitHub and MCP (offline mode)
- `--save`: Persist summary to `notes/context-sync-[date].md`

## Examples

```
/context-sync                  # Full sync, last 7 days
/context-sync 3                # Last 3 days only
/context-sync --git-only       # Local git + state only (no network)
/context-sync --save           # Full sync + persist for cross-session use
```

## See Also

- `skills/sync-context/` — The workflow skill (owns all logic)
- `knowledge/operational-patterns/state-management/session-lifecycle.md`
- `/execute-task` — Start working on the recommended next action
