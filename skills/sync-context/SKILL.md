---
name: sync-context
description: >-
  Pull recent project activity from git log, open PRs, issues, and optional
  MCP-connected sources (Slack, GitHub) into a concise session-bootstrap
  context summary. Triggers: bootstrap session, context sync, what's been
  happening, recent activity, resume after time away.
argument-hint: "Days lookback (default 7); flags: --git-only, --save"
allowed-tools: Read, Bash, Grep, Glob
---

# Sync Recent Context

## Purpose

Bootstraps a session with recent project activity so that the next task can
be selected from current reality, not stale state files alone. Combines
local git history with remote signals (PRs, issues) and optional MCP
sources (Slack, GitHub notifications) into a single skim-able summary.

## When to Invoke

- Starting a new session after >24h away from the project
- Resuming work and unsure what changed in the meantime
- Before picking the next task from `notes/TODO.md`, to verify priority
  hasn't shifted
- After `/compact` or session restart, to re-establish situational awareness

## Protocol

### Step 1: Git Activity (always available)

```bash
# Last N days of commits across all branches (default N=7)
git log --oneline --since="${DAYS:-7} days ago" --all

# Branches with recent activity
git branch -a --sort=-committerdate | head -10

# Uncommitted local changes
git diff --stat
git stash list
```

### Step 2: GitHub Activity (if `gh` CLI available)

```bash
gh pr list --state open --limit 10
gh issue list --state open --limit 10 --sort updated
gh pr list --search "review-requested:@me"
```

Skip silently if `gh` is not authenticated or not installed; do not fail
the entire sync over a missing optional source.

### Step 3: MCP Sources (opportunistic)

Only attempt if explicitly configured and stable:

- Slack MCP: recent messages in project channels
- GitHub MCP: notifications, mentioned issues
- Other MCP servers exposing activity/notification tools

Apply the same degradation: an MCP failure logs a note but does not abort
the sync.

### Step 4: Local State Cross-Check

```bash
# In-progress work captured in notes/
cat notes/current-task.md 2>/dev/null
head -40 notes/progress.md 2>/dev/null

# Recent learned corrections
head -40 CLAUDE.md 2>/dev/null
```

This step reconciles "what state files claim" against "what git/remote
shows" — surfacing drift between captured state and reality.

### Step 5: Synthesize

Present a structured summary:

```markdown
## Context Sync — [date]

### Recent Activity (last [N] days)
- [n] commits across [n] branches
- Key changes: [summary of major commits]

### Open Work
- PRs: [list with status]
- Issues: [assigned/mentioned]
- In-progress tasks: [from notes/current-task.md]

### Drift Signals
- [State file ↔ reality mismatches, if any]

### Attention Needed
- [Review requests, stale PRs, blocked items]

### Session Recommendations
1. [Most urgent / unblocked next task]
2. [Next priority]
```

If `--save` was passed, also write the summary to
`notes/context-sync-YYYY-MM-DD.md` for cross-session reference.

## Arguments

- `$1` (optional): Days lookback (default 7)
- `--git-only`: Skip GitHub and MCP sources (offline mode)
- `--save`: Persist summary to `notes/context-sync-[date].md`

## Verification

This skill is working correctly when:

- Sync runs in <10s for typical projects (git + gh) when sources cached
- Missing optional sources (no `gh`, no MCP) degrade gracefully without
  aborting the run
- Drift between state files and remote is surfaced explicitly, not buried
- Recommendations cite specific items (not vague "review the codebase")

## Integration Points

- `notes/current-task.md` + `notes/progress.md` — local state for cross-check
- `commands/context-sync.md` — shim trigger preserving `/cab:context-sync`
- `agents/orchestrator.md` — may invoke at session start to inform routing
- `execute-task` skill — natural follow-on once context is established

## See Also

- `knowledge/operational-patterns/state-management/session-lifecycle.md` —
  Session resumption patterns
- `knowledge/operational-patterns/state-management/bootstrap-read-pattern.md` —
  Bootstrap cascade governing 3-file cold-start
