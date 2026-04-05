---
name: executing-tasks
description: >
  INVOKE THIS SKILL to enforce the structured task execution protocol
  (PLAN → REVIEW → EXECUTE → VERIFY → COMMIT) for non-trivial work.
  Triggers: implement feature, fix bug, refactor, multi-step task, any work
  producing artifacts that require verification. Prevents one-shotting,
  premature completion, broken state handoff, and scope drift. Automatically
  invoked by the orchestrator agent for delegated work.
argument-hint: "Task objective (e.g., 'refactor auth module to use JWT tokens')"
---

# Task Execution Protocol

## Overview

This skill enforces a structured execution workflow that prevents the most
common agent failure modes: one-shotting, premature completion, broken state
handoff, skipped tests, and scope drift.

## Protocol

### Phase 1: PLAN

Before writing any code or making any changes:

1. **State the objective** in one sentence
2. **Define acceptance criteria** — what "done" looks like (concrete, testable)
3. **Decompose into subtasks** if the work spans multiple files or concerns
4. **Identify verification method** — which commands will confirm correctness
5. **Write plan** to `notes/current-task.md` (or communicate to user if interactive)

**Plan template**:
```markdown
## Task: [objective]

### Acceptance Criteria
- [ ] [Criterion 1 — testable]
- [ ] [Criterion 2 — testable]
- [ ] [Criterion 3 — testable]

### Subtasks
1. [Subtask] → [file(s) affected]
2. [Subtask] → [file(s) affected]

### Verification
- Command: [test/lint/build command]
- Manual check: [what to inspect]

### Boundaries
- In scope: [explicit]
- Out of scope: [explicit]
```

**Failure mode prevented**: One-shotting (dumping a feature list and hoping for the best).

### Phase 2: REVIEW

Before executing:

- If interactive session: Present plan to user, wait for approval or adjustment
- If autonomous/delegated: Verify plan against acceptance criteria from delegation
- If plan has gaps: Ask for clarification rather than assuming

**Failure mode prevented**: Scope drift (doing more or less than intended).

### Phase 3: EXECUTE

Implement one subtask at a time:

1. **Focus on single subtask** — do not jump ahead
2. **Commit after each meaningful subtask** (not at the end):
   ```bash
   git add [specific files]
   git commit -m "[type]: [description of subtask completed]"
   ```
3. **If something goes wrong**: STOP immediately. Do not attempt heroic fixes.
   Switch to plan mode and re-plan from current state.
4. **Update progress** after each subtask:
   ```markdown
   # notes/progress.md
   ## [Task name]
   - [x] Subtask 1 — completed [timestamp]
   - [ ] Subtask 2 — in progress
   - [ ] Subtask 3 — pending
   ```

**Failure mode prevented**: Broken state handoff (no progress tracking between sessions).

### Phase 4: VERIFY

After execution is complete, run verification **before** final commit:

1. **Automated checks** (run ALL applicable):
   ```bash
   npm run typecheck 2>&1 || echo "TYPECHECK FAILED"
   npm run lint 2>&1 || echo "LINT FAILED"
   npm run test 2>&1 || echo "TESTS FAILED"
   npm run build 2>&1 || echo "BUILD FAILED"
   ```
   Adapt commands to project (python: pytest, ruff; other: as defined in CLAUDE.md).

2. **Diff review** — inspect changes against acceptance criteria:
   ```bash
   git diff --stat
   git diff
   ```

3. **Acceptance criteria check** — go through each criterion from the plan:
   - [ ] Criterion 1: PASS/FAIL
   - [ ] Criterion 2: PASS/FAIL

4. **If any check fails**:
   - Do NOT commit
   - Document the failure
   - Return to PLAN phase with failure context
   - Maximum 2 re-plan cycles, then escalate to human

**Failure mode prevented**: Premature completion and skipped testing.

### Phase 5: COMMIT

Only after verification passes:

```bash
git add [specific files — never blind `git add .`]
git commit -m "[type]: [summary of completed work]

[body: what was done, acceptance criteria met]

Verified: [test results summary]"
```

Update state:
- Mark task complete in `notes/progress.md`
- Add any learned corrections to CLAUDE.md if applicable
- Clean up `notes/current-task.md` or archive to `notes/completed/`

## Failure Recovery

If execution goes sideways at any phase:

```
STOP → Assess damage → Re-read plan → Re-plan from current state → Resume
```

Never attempt to fix forward without re-planning. The cost of stopping and
re-planning is always less than the cost of compounding errors.

## When NOT to Use This Protocol

- Simple factual questions (no artifacts produced)
- Single-line edits with obvious verification
- Exploratory conversations without implementation intent
- Tasks explicitly marked as "quick" or "no-protocol" by user

## Integration with Other Extensions

- **Orchestrator agent**: Invokes this protocol for all delegated tasks
- **Verifier agent**: Handles Phase 4 verification as independent subprocess
- **Hooks**: PostToolUse auto-format catches formatting drift during Phase 3
- **Commands**: `/init-worktree` enables parallel execution of Phase 3 across worktrees

## References

- `knowledge/operational-patterns/orchestration/framework.md` — Full theory and failure mode catalog
- `knowledge/operational-patterns/orchestration/cost-model.md` — Token economics, optimization levers
- `knowledge/operational-patterns/multi-agent/collaboration-patterns.md` — Coordination patterns
- `knowledge/operational-patterns/state-management/session-lifecycle.md` — Cross-session persistence
- `knowledge/operational-patterns/team-collaboration.md` — Handoff, delegation, conflict zones
- `knowledge/operational-patterns/multi-agent/worktree-workflows.md` — Parallel task execution
