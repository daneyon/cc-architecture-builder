---
description: Start a structured task using the standard execution protocol (PLAN → REVIEW → EXECUTE → VERIFY → COMMIT)
---
# Execute Task Command

Initiates a structured task workflow following the standard execution protocol.
Use this to ensure non-trivial work follows the full PLAN → REVIEW → EXECUTE →
VERIFY → COMMIT cycle.

## Behavior

Use the `execute-task` skill to enforce the protocol:

1. **If arguments provided**: Use as task objective, proceed to PLAN phase
2. **If no arguments**: Ask user for task objective and acceptance criteria
3. **Create plan** ; use `plan-implementation` skill for extensive tasks ideal for phases and/or user requests detailed phased planning 
4. **Present plan** for user review
5. **On approval**: Execute subtasks with incremental commits
6. **After execution**: Run verification (invoke verifier agent if available)
7. **On verification pass**: Final commit and state update

## Arguments

- `$ARGUMENTS` (optional): Task description / objective

## Examples

```
/execute-task Add input validation to all API endpoints
→ Creates plan with acceptance criteria, presents for review, executes

/execute-task
→ Asks: "What task would you like to execute? Please describe the objective."

/execute-task Fix the memory leak in the WebSocket handler
→ Creates plan focused on diagnosis → fix → verify cycle
```

## Output

Each phase produces visible output:

```
── PHASE 1: PLAN ──
Objective: [task]
Acceptance criteria:
- [ ] [criterion]
- [ ] [criterion]
Subtasks: [list]
Verification: [commands]

── PHASE 2: REVIEW ──
[Awaiting user approval or adjustment]

── PHASE 3: EXECUTE ──
[Subtask progress with incremental commits]

── PHASE 4: VERIFY ──
[Automated check results + acceptance criteria review]

── PHASE 5: COMMIT ──
[Final commit message + state update]
```

## See Also

- `skills/execute-task/` — The protocol skill (model-invoked, auto-triggered)
- `agents/verifier.md` — Independent verification agent
- `agents/orchestrator.md` — Autonomous orchestration
