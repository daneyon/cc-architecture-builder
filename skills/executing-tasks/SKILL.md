---
name: executing-tasks
description: >-
  Enforce PLAN → REVIEW → EXECUTE → VERIFY → COMMIT protocol for non-trivial
  tasks. Prevents one-shotting, premature completion, and scope drift. Triggers:
  implement feature, fix bug, refactor, multi-step task.
argument-hint: "Task objective (e.g., 'refactor auth module to use JWT tokens')"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
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
   git add [specific files — never blind `git add .`]
   git commit -m "[type]: [description of subtask completed]"
   ```
3. **Commit-per-phase cadence (DD-4, recommended)** — For multi-phase tasks
   (Phase A → B → C), prefer one cohesive commit per phase over many small
   per-subtask commits. Cleaner git history, easier audit trail, provides clear
   work-commit anchors for the Phase 5 state refresh. This is guidance, not
   prescription — use per-subtask commits when phases are long-running or when
   incremental rollback is needed.
4. **If something goes wrong**: STOP immediately. Do not attempt heroic fixes.
   Switch to plan mode and re-plan from current state.
5. **Defer state updates to Phase 5** — Do not update `notes/progress.md` or
   `notes/current-task.md` inline during execution. State files describe
   *completed* work in past tense referencing commit hashes; updating them
   before the commit lands guarantees stale tense (LL-26). The lightweight
   exception: crossing-off completed subtasks in `notes/current-task.md` as
   you go is acceptable since that doesn't describe work in tense-sensitive
   status lines.

**Failure mode prevented**: Broken state handoff (no progress tracking between sessions) + stale-tense state files (LL-26).

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

### Phase 5: COMMIT (Two-Commit Pattern, LL-26/DD-1)

Only after verification passes. **Two commits, not one** — work commit first,
state refresh commit second. This structurally prevents stale-tense state files
(Session 24 failure mode).

#### Phase 5a: Work Commit

```bash
git status                            # Inspect uncommitted changes
git add [work files + any new KB/lesson artifacts that ARE the deliverable]
git commit -m "[type]: [summary of completed work]

[body: what was done, acceptance criteria met]

Verified: [test results summary]"
WORK_COMMIT=$(git rev-parse --short HEAD)
```

**Classification rule** — what belongs in the work commit vs the state refresh:

| File | Category | Goes In |
|------|----------|---------|
| Code, configs, skills, agents, KB, templates | **Work artifacts** | Work commit |
| `notes/lessons-learned.md` (NEW LL entry codifying the lesson from this work) | **Work deliverable** | Work commit |
| `notes/impl-plan-*.md` (NEW plan being committed as part of planning work) | **Work deliverable** | Work commit |
| `notes/progress.md` (status refresh citing work-commit hash) | **State artifact** | State refresh commit |
| `notes/current-task.md` (status refresh citing work-commit hash) | **State artifact** | State refresh commit |
| `notes/TODO.md` (check-offs citing work-commit hash) | **State artifact** | State refresh commit |

**Critical**: Exclude tense-sensitive state artifacts (progress.md, current-task.md,
TODO.md) from this commit. They must reference `$WORK_COMMIT` in past tense,
which is structurally impossible if they ride in the same commit as the work
they describe. Knowledge artifacts (lessons-learned.md, KB files, plans) are
NOT tense-sensitive in this way — they describe concepts, not transient status.

#### Phase 5b: State Refresh

Update state files using past-tense framing referencing `$WORK_COMMIT`:

- `notes/current-task.md` — Mark subtasks complete with `"executed in <hash>"`
- `notes/progress.md` — Session summary block with `Latest commit: <hash>`
- `notes/TODO.md` — Check off items, cite hash where appropriate
- `notes/lessons-learned.md` — Add any new LL entries
- CLAUDE.md — Add any learned corrections if applicable

**Tense hygiene check**:
```bash
grep -nE '^\*\*(Status|Phase|Gate)\*\*:.*(pending commit|ready for commit|awaiting commit|will commit)' notes/ || echo "CLEAN"
```
Expected output: `CLEAN`. Any match = stale tense in status line; fix before
proceeding to Phase 5c.

#### Phase 5c: State Refresh Commit

```bash
git add notes/
git commit -m "chore(task): refresh state post-$WORK_COMMIT

State updated with past-tense framing referencing work commit."
```

**Fallback — tense-neutral single-commit** (mid-task state touches with no
substantive work): use `chore(notes): mid-task state update — <context>`.
Only appropriate when no work files are staged.

**Failure mode prevented**: Stale-tense state files (LL-26) — state artifacts
frozen with "pending commit" language become invalid the instant the commit
lands, misleading the next session's cold-start bootstrap.

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
