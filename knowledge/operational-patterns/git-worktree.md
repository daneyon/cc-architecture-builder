---
id: git-worktree
title: Git Worktree Parallel Execution
category: operational-patterns
tags: [git, worktree, parallel, sessions, branching]
summary: Using git worktrees to run multiple Claude Code sessions simultaneously on different branches or features.
depends_on: [git-foundation]
related: [session-management, multi-agent-collaboration]
complexity: intermediate
last_updated: 2025-12-12
estimated_tokens: 550
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

### Creating Worktrees

```bash
# From your main repository
cd my-project

# Create worktree for a feature branch
git worktree add ../my-project-feature-auth feature/authentication

# Create worktree for bugfix
git worktree add ../my-project-hotfix hotfix/critical-bug

# Create worktree with new branch
git worktree add -b feature/new-thing ../my-project-new-thing

# List all worktrees
git worktree list
```

### Resulting Directory Structure

```
~/projects/
├── my-project/                 # Main worktree (main branch)
├── my-project-feature-auth/    # Feature worktree
└── my-project-hotfix/          # Hotfix worktree
```

## Running Parallel Sessions

### Terminal Setup

```bash
# Terminal 1: Main development
cd ~/projects/my-project
claude

# Terminal 2: Feature work (separate session)
cd ~/projects/my-project-feature-auth
claude

# Terminal 3: Hotfix (separate session)
cd ~/projects/my-project-hotfix
claude
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
