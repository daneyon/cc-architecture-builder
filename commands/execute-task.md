---
description: Start a structured task using the standard execution protocol (PLAN → REVIEW → EXECUTE → VERIFY → COMMIT)
---
# Execute Task Command

Shim command that invokes the `execute-task` skill to run the standard
PLAN → REVIEW → EXECUTE → VERIFY → COMMIT protocol. Use for non-trivial work
(multi-file changes, bug fixes, feature implementation).

## Invocation

Use the `execute-task` skill. For extensive phased work requiring SOW authoring,
the skill delegates to `plan-implementation` at PLAN phase (F011 Option A).

## Arguments

- `$ARGUMENTS` (optional): Task objective. If omitted, skill asks interactively.

## Examples

```
/execute-task Add input validation to all API endpoints
/execute-task Fix the memory leak in the WebSocket handler
/execute-task                     # interactive prompt for objective
```

## See Also

- `skills/execute-task/` — The protocol skill (owns all phase mechanics)
- `skills/plan-implementation/` — Extensive plan authoring (delegated from PLAN phase)
- `agents/verifier.md` — Independent verification agent
- `agents/orchestrator.md` — Autonomous orchestration
