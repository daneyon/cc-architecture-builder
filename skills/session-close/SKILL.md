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
failure modes: lost progress, stale state files, orphaned current-task context,
and broken bootstrap sequences. Every session should close cleanly.

## When to Invoke

- User explicitly ends the session ("done", "wrap up", "close", "save state")
- Context window approaching capacity (~70%+ and no more subtasks)
- Switching to unrelated domain (stale context dilutes quality)
- After completing a major task group (natural checkpoint)

## Protocol

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

### Step 2: Update State Files

Update **in this order** (most volatile → most stable):

1. **`notes/current-task.md`** — Update status of each subtask. If task is fully
   complete, clear and mark as complete. If partially done, note exactly where to
   resume (specific subtask, file, line).

2. **`notes/progress.md`** — Update:
   - `Last session` date and summary
   - `Latest commit` hash and description
   - `Current Position` section (gate, next action, cumulative status)
   - Session summary block (what was done, key commits)
   - `Context health` note if relevant

3. **`notes/TODO.md`** — Check off completed items. Add any new items discovered
   during the session. Reorder pending items if priorities shifted.

4. **`notes/lessons-learned.md`** — Add any new operational lessons (LL-XX format)
   if correctable errors or new patterns emerged.

### Step 3: Verify Clean State

```bash
git status          # No unexpected uncommitted changes
git diff --stat     # Confirm scope of any remaining changes
git log --oneline -5  # Verify recent commits are sensible
```

If there are uncommitted changes that should be preserved:
- Stage and commit with descriptive message
- Or stash with clear description: `git stash push -m "T5 partial: [description]"`

### Step 4: Final Commit (if state files changed)

Commit the state file updates:

```bash
git add notes/current-task.md notes/progress.md notes/TODO.md
git commit -m "chore: session close — update state for [task context]"
```

### Step 5: Report to User

Provide a concise closing summary:

```
── SESSION CLOSE ──────────────────────────────
Completed: [X subtasks]
Committed: [hash] — [message]
Next session: [what to work on next]
Bootstrap: Read notes/progress.md
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
- **Don't commit state files with unfinished work** — Commit the work first, then update and commit state files
