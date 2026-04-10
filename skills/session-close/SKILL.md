---
name: session-close
description: >-
  Cleanly close session with state persistence and context handoff. Updates
  progress.md, TODO.md, current-task.md. Triggers: close, wrap up, save state,
  session done, ending session, context full.
argument-hint: "Optional summary of what was accomplished"
allowed-tools: Read, Write, Edit, Glob
effort: medium
---

# Session Close Protocol

## Overview

This skill standardizes session closing to prevent the most common cross-session
failure modes: lost progress, stale state files (LL-26), orphaned current-task
context, and broken bootstrap sequences. Every session should close cleanly with
a **two-commit pattern** that separates work from state refresh.

## When to Invoke

- User explicitly ends the session ("done", "wrap up", "close", "save state")
- Context window approaching capacity (~70%+ and no more subtasks)
- Switching to unrelated domain (stale context dilutes quality)
- After completing a major task group (natural checkpoint)

## Protocol — Two-Commit Pattern (LL-26, DD-1)

The **two-commit pattern** is the default. Work files are committed first;
state files are refreshed in past tense using the work-commit's hash, then
committed separately. This prevents stale-tense state artifacts (Session 24
failure mode — state said `"ready for commit"`, became stale the instant the
commit landed).

### Step 1: Capture Session Summary

Summarize what was accomplished this session:

```markdown
## Session Summary
- **Started**: [task/objective]
- **Completed**: [list of completed subtasks]
- **In progress**: [any partially complete work]
- **Blocked/deferred**: [items pushed to next session]
- **Key decisions**: [architectural choices, design rationale]
```

### Step 2: Work Commit FIRST (if uncommitted work exists)

Before touching tense-sensitive state artifacts, commit the substantive work
(including any new lessons-learned.md entries or KB/plan deliverables that ARE
part of the work):

```bash
git status                            # Inspect uncommitted changes
git add <work-files + notes/lessons-learned.md if new LL codifies this work>
git commit -m "<type>: <description>" # Work commit lands FIRST
WORK_COMMIT=$(git rev-parse --short HEAD)
```

**What counts as "work"**: code, configs, skills, agents, KB files, templates,
NEW lessons-learned.md entries codifying the lesson, and new impl-plans.
**What counts as tense-sensitive state** (exclude from work commit): `progress.md`,
`current-task.md`, `TODO.md` — these get refreshed in Step 3 citing `$WORK_COMMIT`.

**Why first**: State files must reference the work-commit hash in past tense.
This is structurally impossible if state and work are committed together.

If no substantive work is uncommitted (state-only session), skip to Step 3 and
use the tense-neutral single-commit fallback at Step 5.

### Step 3: Refresh State Files in Past Tense

Update **in this order** (most volatile → most stable), using **past-tense
framing** that references `$WORK_COMMIT` from Step 2:

1. **`notes/current-task.md`** — Update status of each subtask. Use approved
   phrasing: `"executed in <hash>"`, `"committed in <hash>"`, `"landed in <hash>"`.
   If task is fully complete, clear or mark complete. If partially done, note
   exact resume point (specific subtask, file, line).

2. **`notes/progress.md`** — Update:
   - `Last session` date and summary
   - `Latest commit` — `$WORK_COMMIT` hash and description
   - `Current Position` section (gate, next action, cumulative status)
   - Session summary block (what was done, commit hashes)
   - `Context health` note if relevant

3. **`notes/TODO.md`** — Check off completed items (cite commit hash where
   appropriate). Add any new items discovered during the session. Reorder
   pending items if priorities shifted.

4. **`notes/lessons-learned.md`** — Add any new operational lessons (LL-XX
   format) if correctable errors or new patterns emerged.

### Step 4: Tense Hygiene Checklist

Before the state-refresh commit, grep the updated files for forbidden
status-line patterns:

```bash
grep -nE '^\*\*(Status|Phase|Gate)\*\*:.*(pending commit|ready for commit|awaiting commit|will commit|EXECUTED ✅ — [Rr]eady)' notes/ || echo "CLEAN"
```

Expected output: `CLEAN`. Any match = forbidden tense in status line; fix
before proceeding. Descriptive prose in body text, code blocks, and headings
is allowed — the regex only flags status-line contexts.

### Step 5: State Refresh Commit

Commit state refresh as a separate commit referencing the work commit:

```bash
git add notes/current-task.md notes/progress.md notes/TODO.md notes/lessons-learned.md
git commit -m "chore(session-NN): refresh state post-$WORK_COMMIT"
```

**Tense-neutral single-commit fallback** (mid-session state touches only, no
substantive work in the same commit):

```bash
git commit -m "chore(notes): mid-session state update — <context>"
```

### Step 6: Verify Clean State

```bash
git status             # Should be clean
git log --oneline -5   # Two commits visible: work commit + state refresh
```

### Step 7: Report to User

Provide a concise closing summary:

```
── SESSION CLOSE ──────────────────────────────
Completed: [X subtasks]
Work commit:  [hash] — [message]
State commit: [hash] — refresh state post-[hash]
Next session: [what to work on next]
Bootstrap: Read notes/current-task.md + notes/progress.md
───────────────────────────────────────────────
```

## State File Reference

| File | Purpose | Update Frequency |
|------|---------|-----------------|
| `notes/current-task.md` | Active task context, subtask status | Every session close |
| `notes/progress.md` | Bootstrap state, session history | Every session close |
| `notes/TODO.md` | Task backlog, completion tracking | When items change |
| `notes/lessons-learned.md` | Operational constraints | When new lessons emerge |

## Anti-Patterns

- **Don't skip state updates** — "I'll remember" fails across sessions
- **Don't leave current-task.md stale** — Next session inherits wrong context
- **Don't close mid-subtask without noting exact resume point** — "Continue T5" is insufficient; "Resume at T5-08: update INDEX.md file counts" is actionable
- **Don't commit state files WITH work files in a single commit** — LL-26 violation. State files must describe work in past tense referencing the work-commit hash. A single combined commit makes this structurally impossible. Use the two-commit pattern (Step 2 → Step 5).
- **Don't use future/pending tense in status lines** — Forbidden patterns: `pending commit`, `ready for commit`, `awaiting commit`, `will commit`. Approved: `executed in <hash>`, `committed in <hash>`, `landed in <hash>`.
