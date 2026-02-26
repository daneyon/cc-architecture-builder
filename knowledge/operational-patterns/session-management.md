---
id: session-management
title: Session Management
category: operational-patterns
tags: [sessions, resume, history, persistence, continue]
summary: Managing Claude Code conversation state including resuming sessions, accessing history, and session persistence patterns.
depends_on: []
related: [git-worktree, multi-agent-collaboration, orchestration-framework]
complexity: foundational
last_updated: 2025-12-12
estimated_tokens: 350
---

# Session Management

## Overview

Claude Code sessions persist conversation history, enabling resumption of previous work and access to conversation context.

## Resuming Sessions

### Continue Most Recent

```bash
# Continue most recent session in current directory
claude --continue

# Or shorthand
claude -c
```

### Resume Specific Session

```bash
# Resume by session ID
claude --resume abc123

# Interactive selection
claude --resume
# Presents list of recent sessions to choose from
```

### Via Interactive Mode

```bash
claude
# Then use:
/resume        # Interactive session selection
/history       # View session history
```

## Session Storage

Sessions stored as JSONL transcript files:
- Location varies by platform
- Contains full conversation history
- Includes tool usage and outputs

## Session Lifecycle

```
┌──────────────┐
│ Session Start│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Conversation │◀──┐
│    Active    │   │ User/Claude
└──────┬───────┘───┘ exchanges
       │
       ▼
┌──────────────┐
│ Session End  │ (exit, /clear, timeout)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Transcript   │
│   Saved      │
└──────────────┘
       │
       ▼
┌──────────────┐
│ Resumable    │ (--continue, --resume)
└──────────────┘
```

## Practical Patterns

### End-of-Day Handoff

```bash
# Before ending session
> Summarize current state and next steps for tomorrow

# Tomorrow
claude --continue
> What were we working on?
```

### Context Preservation

When working on complex tasks:
1. Periodically ask Claude to summarize progress
2. Use TODO comments in code as breadcrumbs
3. Commit incrementally with descriptive messages

### Project-Specific Sessions

Sessions are scoped to working directory:
- Different directories = different session histories
- Use git worktrees for branch-specific sessions

## Commands Reference

| Command | Description |
|---------|-------------|
| `claude -c` | Continue most recent session |
| `claude --resume ID` | Resume specific session |
| `claude --resume` | Interactive session picker |
| `/history` | View session history |
| `/resume` | Interactive resume |
| `/clear` | Clear current session (new start) |

## Limitations

- Sessions scoped to working directory
- Very long sessions may hit context limits
- No built-in session search (use `--resume` picker)

## Best Practices

1. **Use descriptive final messages**: End sessions with summaries
2. **Commit frequently**: Git commits serve as session checkpoints
3. **Use worktrees for parallel work**: Separate sessions per worktree
4. **Don't rely solely on sessions**: Document important decisions

## See Also

- [Git Worktree](git-worktree.md) — Parallel session management
- [Multi-Agent Collaboration](multi-agent-collaboration.md)
- [Orchestration Framework](orchestration-framework.md) — Initializer/iterator harness for cross-session state management
