---
description: Pull recent project activity from git log, open PRs, issues, and optionally connected MCP sources (Slack, GitHub) into a single context summary for session bootstrapping
allowed-tools: Read, Bash, Grep, Glob
---

# Context Sync

Bootstraps a session with recent project activity. Pulls the last N days of
commits, open PRs, issues, and optionally MCP-connected sources into a concise
context dump. Ideal for starting a new session or resuming after time away.

## Behavior

1. **Git activity** (always available):
   ```bash
   # Last 7 days of commits (default)
   git log --oneline --since="7 days ago" --all

   # Branches with recent activity
   git branch -a --sort=-committerdate | head -10

   # Open changes
   git diff --stat
   git stash list
   ```

2. **GitHub activity** (if `gh` CLI available):
   ```bash
   # Open PRs
   gh pr list --state open --limit 10

   # Recent issues
   gh issue list --state open --limit 10 --sort updated

   # PR review requests
   gh pr list --search "review-requested:@me"
   ```

3. **MCP sources** (if configured — opportunistic, not required):
   - Slack: Recent messages in project channels (if Slack MCP connected)
   - GitHub: Recent notifications, mentioned issues
   - Other: Any configured MCP server with activity/notification tools

4. **Project state check**:
   ```bash
   # Check notes/ for in-progress work
   cat notes/progress.md 2>/dev/null
   cat notes/current-task.md 2>/dev/null

   # Check CLAUDE.md learned corrections (recent additions)
   ```

5. **Synthesize into context summary**:
   ```markdown
   ## Context Sync — [date]

   ### Recent Activity (last [N] days)
   - [n] commits across [n] branches
   - Key changes: [summary of major commits]

   ### Open Work
   - PRs: [list with status]
   - Issues: [assigned/mentioned]
   - In-progress tasks: [from notes/progress.md]

   ### Attention Needed
   - [Review requests, stale PRs, blocked items]

   ### Session Recommendations
   Based on current state, suggested next actions:
   1. [Most urgent item]
   2. [Next priority]
   ```

## Arguments

- `$1` (optional): Number of days to look back. Default: 7.
- `--git-only`: Skip GitHub and MCP sources
- `--save`: Write summary to `notes/context-sync-[date].md`

## Examples

```
/context-sync
→ Full sync: git + GitHub + MCP, last 7 days

/context-sync 3
→ Last 3 days only

/context-sync --git-only
→ Git log and local state only (no network calls)

/context-sync --save
→ Full sync, saved to notes/ for cross-session reference
```

## See Also

- `knowledge/operational-patterns/state-management/session-lifecycle.md` — Session resumption patterns
- `agents/orchestrator.md` — Uses context sync to inform task routing
- `/execute-task` — Start working on recommended next actions
