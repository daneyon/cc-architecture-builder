---
id: worktree-workflows
title: Worktree Workflows
category: operational-patterns/multi-agent
tags: [git, worktree, parallel, sessions, branching, workflows]
summary: Git worktree setup, workflow patterns, and orchestrator-initiated split protocols for parallel Claude Code sessions.
depends_on: [collaboration-patterns]
related: [agent-teams, session-lifecycle, team-collaboration]
complexity: intermediate
last_updated: 2026-04-05
estimated_tokens: 900
source: https://code.claude.com/docs/en/sub-agents
confidence: A
review_by: 2026-07-05
revision_note: "v3.0 — Migrated from git-worktree.md into multi-agent/ subdirectory. Content preserved, cross-references updated."
---

# Worktree Workflows

## Overview

Git worktrees allow checking out multiple branches simultaneously in separate directories, enabling **parallel CC sessions** on different aspects of a project. This is the CC team's preferred approach for parallel work.

> **Official docs**: [Sub-agents](https://code.claude.com/docs/en/sub-agents) — worktree isolation via `isolation: worktree` frontmatter. Also see `--worktree` CLI flag.

---

## Setup

### Built-in (Preferred)

```bash
claude --worktree feature-auth    # Create worktree + session
claude -w feature-auth            # Shorthand
claude --worktree                 # Auto-generate name
```

Worktrees live in `.claude/worktrees/<name>/` and auto-cleanup if no changes on exit.

### Manual (More Control)

```bash
git worktree add -b feat/task-name ../project-task-name
git worktree list
```

### Gitignored File Copying

Create `.worktreeinclude` to auto-copy gitignored files into new worktrees:

```text
.env
.env.local
config/secrets.json
```

---

## What Each Session Gets

| Resource | Shared | Independent |
|----------|--------|-------------|
| Git repository | ✓ | |
| Project CLAUDE.md | ✓ (via git) | |
| Global user config | ✓ (`~/.claude/`) | |
| Context window | | ✓ |
| Conversation history | | ✓ |
| Working directory | | ✓ |
| Branch state | | ✓ |

---

## Workflow Patterns

### Feature + Review

```
Worktree: feature/        Worktree: main
├─ Implement feature       ├─ Review changes
├─ Write tests       ───▶  ├─ Run full test suite
├─ Commit                  └─ Merge when ready
```

### Parallel Analysis

```
Worktree: analysis-1       Worktree: analysis-2
├─ Security audit           ├─ Performance analysis
│                           │
└─── Combined findings in main worktree ───┘
```

### Orchestrator-Initiated Split

When the orchestrator detects a parallelizable task:

**Propose split when**:
- Task is independent but touches files main is actively modifying
- Task requires interactive human-LLM collaboration
- Task has a clear merge-back path and bounded scope

**Use background agent instead when**:
- Read-only analysis (no file conflicts)
- No human interaction needed
- Context-switching overhead exceeds parallelism benefit

**Split protocol**:
1. Commit current state (so new session inherits context)
2. Create worktree: `claude -w task-name`
3. User opens worktree in new terminal/IDE window
4. After completion: merge, remove worktree, delete branch

---

## Best Practices

- **Name consistently**: `project-purpose` pattern (e.g., `myapp-feature-auth`)
- **3-5 worktrees** is the practical sweet spot
- **Color-code terminal tabs** — one color per worktree
- **Keep a dedicated analysis worktree** for read-only investigation
- **Enable system notifications** to know when a session needs input
- **Clean up after merging** — worktrees are ephemeral task containers

### Cleanup

```bash
git worktree remove ../my-project-feature-auth
git branch -d feature/authentication
git worktree prune    # Clear stale references
```

## See Also

- [Collaboration Patterns](collaboration-patterns.md) — All 4 multi-agent patterns
- [Agent Teams](agent-teams.md) — When inter-agent communication is needed
- [Team Collaboration](../team-collaboration.md) — Multi-human + multi-agent protocols
