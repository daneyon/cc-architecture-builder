---
id: git-worktree
title: Git Worktree Parallel Execution
category: operational-patterns
tags: [git, worktree, parallel, sessions, branching]
summary: Using git worktrees to run multiple Claude Code sessions simultaneously on different branches or features.
depends_on: [git-foundation]
related: [session-management, multi-agent-collaboration]
complexity: intermediate
last_updated: 2026-03-27
estimated_tokens: 900
---

# Git Worktree Parallel Execution

## Overview

Git worktrees allow checking out multiple branches simultaneously in separate directories, enabling **parallel Claude Code sessions** working on different aspects of your project.

## Why Use Worktrees

| Scenario | Without Worktrees | With Worktrees |
|----------|-------------------|----------------|
| Feature + bugfix simultaneously | Switch branches, lose context | Two terminals, full context |
| Testing in isolation | Stash changes, checkout, test | Separate worktree for testing |
| Long-running analysis | Blocks other work | Dedicated worktree |
| Multi-agent collaboration | Single Claude instance | Multiple Claude instances |

## Setup and Usage

### Built-in Worktree Flag (Preferred)

Claude Code has native worktree support. This is the simplest path:

```bash
# Create worktree and start a session in it (auto-creates branch)
claude --worktree feature-auth
claude -w feature-auth          # shorthand

# Auto-generate random worktree name
claude --worktree
```

Worktrees created this way live in `.claude/worktrees/<name>/` and auto-cleanup
if no changes are made when the session exits.

### Manual Git Worktrees (For More Control)

Use standard git commands when you need specific branch names or directory locations:

```bash
git worktree add -b feat/task-name ../project-task-name
git worktree list
```

### Gitignored File Copying

Create `.worktreeinclude` in project root to auto-copy gitignored files (`.env`,
secrets, local configs) into new worktrees:

```text
.env
.env.local
config/secrets.json
```

### Running Parallel Sessions

Each worktree gets its own independent Claude Code session:

```bash
# Terminal / IDE window 1: Main development
cd ~/projects/my-project && claude

# Terminal / IDE window 2: Feature work
cd ~/projects/my-project-feature-auth && claude
# Or: open the worktree folder in a new IDE window

# Terminal / IDE window 3: Hotfix
cd ~/projects/my-project-hotfix && claude
```

### What Each Session Gets

| Resource | Shared | Independent |
|----------|--------|-------------|
| Git repository | ✓ | |
| Project CLAUDE.md | ✓ (via git) | |
| Global user config | ✓ (`~/.claude/`) | |
| Context window | | ✓ |
| Conversation history | | ✓ |
| Working directory | | ✓ |
| Branch state | | ✓ |

## Workflow Patterns

### Feature + Review Pattern

```
┌─────────────────────┐      ┌─────────────────────┐
│ Worktree: feature/  │      │ Worktree: main      │
│                     │      │                     │
│ Claude Session A    │      │ Claude Session B    │
│ - Implement feature │ ───▶ │ - Review changes    │
│ - Write tests       │      │ - Run full test suite│
│ - Commit            │      │ - Merge when ready  │
└─────────────────────┘      └─────────────────────┘
```

### Parallel Analysis Pattern

```
┌─────────────────────┐      ┌─────────────────────┐
│ Worktree: analysis-1│      │ Worktree: analysis-2│
│                     │      │                     │
│ Claude: Security    │      │ Claude: Performance │
│ audit of codebase   │      │ analysis of codebase│
│                     │      │                     │
│ Independent context │      │ Independent context │
└─────────────────────┘      └─────────────────────┘
            │                          │
            └──────────┬───────────────┘
                       ▼
              Combined findings in
              main worktree
```

## Best Practices

### Naming Convention

```bash
# Pattern: project-purpose
git worktree add ../my-project-feature-login feature/login
git worktree add ../my-project-bugfix-auth hotfix/auth-fix
git worktree add ../my-project-analysis feature/security-audit
```

### Cleanup

```bash
# Remove worktree (keeps branch)
git worktree remove ../my-project-feature-auth

# Remove worktree AND delete branch
git worktree remove ../my-project-feature-auth
git branch -d feature/authentication

# Prune stale worktree references
git worktree prune
```

### Don't Do This

- **Same branch in multiple worktrees**: Git prevents this, but plan accordingly
- **Forget to push/pull**: Worktrees share refs but need sync
- **Leave stale worktrees**: Clean up after merging

## Memory Considerations

Project CLAUDE.md works seamlessly across worktrees since it's version-controlled:

```markdown
# In project CLAUDE.md
# Personal preferences via import (works across worktrees)
@~/.claude/my-project-preferences.md
```

## Orchestrator-Initiated Worktree Split

When the orchestrator detects a parallelizable task, it proposes a split —
but the human decides whether to approve. This is a HITL decision, not
autonomous execution.

**When the orchestrator should propose a split:**

- Task is independent but touches files the main branch is actively modifying
- Task requires interactive human-LLM collaboration (background agent insufficient)
- Task has a clear merge-back path and bounded scope

**When NOT to split** (use background agent instead):

- Task is read-only analysis — no file conflicts possible
- Task doesn't need human interaction — background agent with `isolation: "worktree"` suffices
- Overhead of context-switching between sessions exceeds the parallelism benefit

**After human approval, the orchestrator should:**

1. Commit current state (so the new session inherits context via `/context-sync`)
2. Create the worktree: `claude --worktree task-name` (built-in) or
   `git worktree add -b feat/task-name ../project-task-name` (manual)
3. Inform the user to open the worktree in a new terminal or IDE window —
   CC cannot open new sessions programmatically

The new session reconstructs context from committed state files (`notes/`,
CLAUDE.md, git log). No custom init files needed if state management is
working correctly.

**Cleanup** (from either session):

```bash
git merge feat/task-name
git worktree remove ../project-task-name  # or auto-cleaned if using claude -w
git branch -d feat/task-name
```

## Integration with Multi-Agent

Worktrees enable true parallel agent execution:

```
Worktree 1 (main)           Worktree 2 (feature)
┌─────────────────┐         ┌─────────────────┐
│ Claude Session  │         │ Claude Session  │
│ ┌─────────────┐ │         │ ┌─────────────┐ │
│ │ Main Agent  │ │         │ │ Main Agent  │ │
│ └──────┬──────┘ │         │ └──────┬──────┘ │
│   ┌────┴────┐   │         │   ┌────┴────┐   │
│   ▼         ▼   │         │   ▼         ▼   │
│ Subagent  Subagent│       │ Subagent  Subagent│
└─────────────────┘         └─────────────────┘
         │                           │
         └───────────┬───────────────┘
                     ▼
            Shared Git Repository
```

## See Also

- [Git Foundation](../prerequisites/git-foundation.md)
- [Session Management](session-management.md)
- [Multi-Agent Collaboration](multi-agent-collaboration.md)
- [Orchestration Framework](orchestration-framework.md) — Cost model comparing worktrees vs subagents vs Agent Teams
