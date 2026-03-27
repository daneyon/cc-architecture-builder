---
id: session-management
title: Session Management
category: operational-patterns
tags: [sessions, resume, history, persistence, continue, state-management]
summary: Managing Claude Code conversation state including resuming sessions, accessing history, session persistence patterns, and filesystem-based state design.
depends_on: []
related: [git-worktree, multi-agent-collaboration, orchestration-framework]
complexity: foundational
last_updated: 2026-03-27
estimated_tokens: 1400
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

## Advanced Session Patterns

### Cross-Device Fluidity

Move active sessions between CLI and browser for mobile/desktop check-ins:

```bash
# Transfer current session to claude.ai/code for browser access
claude --teleport
```

This enables monitoring long-running tasks from a phone or different machine
without losing context.

### Background Execution

Offload thinking-heavy or long-running tasks to background:

```bash
# Run task in background (standard bash)
claude -p "analyze this codebase and write a report to notes/analysis.md" &

# Check status
jobs

# Bring back to foreground
fg
```

Combine with system notifications to know when background tasks need input.

### Plan Mode Shortcuts

For non-trivial tasks, force plan-first execution:

- **Interactive**: Press `Shift+Tab` twice to enter Plan Mode before executing
- **CLI flag**: `claude --plan` to start in plan-only mode
- **In-session**: Type "plan mode" or use Shift+Tab toggle

Plan Mode makes Claude outline architecture and specs before writing any code.
The CAB `executing-tasks` skill enforces this automatically for delegated work.

### Status Monitoring

```bash
# Enable statusline to monitor context usage and git branch
/statusline
```

Shows real-time context window usage percentage, active git branch, and session
ID — critical for managing multiple concurrent worktree sessions.

## Context Health: Continue, Compact, or Fresh?

As sessions grow, context quality degrades. Use this decision framework:

| Signal | Action |
|--------|--------|
| Task going well, related work ahead | **Continue** — momentum is valuable |
| Context >70% full, work still on-track | **Compact** — run `/compact` to reclaim space. The ~22.5% buffer exists for auto-compaction. |
| Stuck in fix→slop→fix loop | **Fresh session** — stop. The current context is poisoned. Start clean with a focused prompt. |
| Switching to unrelated domain/task | **Fresh session** — stale context from prior task dilutes new task quality |
| Long session, occasional drift | **Compact + re-anchor** — compact, then re-state the current objective clearly |

**Key insight** (per Jarrod Watts): Every token in context should aim to aid the LLM's
next request. If it's not doing that, you're accumulating noise that degrades output.

**Context degradation patterns** (per Koylan): As context length increases, models
exhibit predictable failures — "lost in the middle" (middle content gets less
attention), U-shaped attention curves, and attention scarcity. Keep high-priority
information at the start and end of context, not buried in the middle.

**Practical monitoring**:
- Use `/statusline` to track context fullness in real-time
- Use `/context` to see what's consuming space and prune if needed
- Compact proactively at ~70% rather than waiting for auto-compact

## Filesystem as Context Store

The filesystem is a persistent context layer that survives compaction and session
boundaries. Use it strategically:

| Pattern | Implementation | When |
|---------|---------------|------|
| **Plan persistence** | Write plans to `notes/current-task.md` | Before executing multi-step work |
| **Tool output offloading** | Write large outputs to files instead of keeping in context | When tool results exceed ~500 lines |
| **Scratch pad** | Use `notes/scratch.md` for intermediate reasoning | During complex analysis |
| **Progress tracking** | Update `notes/progress.md` after each subtask | Cross-session task continuity |
| **State snapshots** | Save key decisions/context before compaction | Before `/compact` on complex sessions |

This keeps the conversation context lean (high signal-to-noise) while preserving
full detail on disk for later retrieval.

### State File Design Patterns

The `notes/` files above are most effective when they follow deliberate structural
patterns. These emerge from a common failure mode: state files that are *written*
regularly but not *structured* for cold-start re-orientation.

**Cold-Start Anchor** (`notes/current-task.md`):
Structure this as the single document an agent reads to re-orient after compaction
or a fresh session. Include at minimum:

- Current task and phase (1 line)
- Active blockers with owner and status (table)
- Key file pointers — the 3-5 files most relevant to current work
- User directives carried forward — strategic constraints the user stated that
  shape all subsequent work (e.g., "no paid platforms", "design for X but don't
  block on it"). These are often stated once and lost during compaction.

The anchor should be <100 lines. If it grows beyond that, it's accumulating
detail that belongs in `progress.md` or domain-specific files.

**Progress with Decision Trail** (`notes/progress.md`):
Track not just task completion but the *decisions* that shaped the work. Decisions
are the most compaction-lossy artifact — they're stated once in conversation,
influence all downstream work, and vanish when context is compressed.

Recommended sections:

- **Priority-tiered task backlog** — group by urgency/dependency, not just a flat list.
  Include status markers and brief rationale for ordering.
- **Decision log** — ID, decision, rationale, date. Reference these IDs from task
  descriptions so the reasoning chain is traceable.
- **Blockers** — first-class entities with owner + status, not buried in task
  descriptions. Prevents re-attempting blocked work session after session.
- **Deferred / hold items** — explicitly separate "open questions requiring
  discussion" from "executable tasks." This prevents premature execution of
  under-specified work.
- **Completion history** — what was done and when, for audit trail and
  re-orientation after long gaps between sessions.

**Separation principle**: `current-task.md` answers "where am I right now?"
`progress.md` answers "what's the full picture?" Both survive compaction, but
only the anchor needs to be read on every cold start.

## Post-Compaction: Extension Re-Anchoring

Context compaction (`/compact`) is lossy — it may drop extension awareness even if the skills are still available. After compaction in projects with skills:

1. Re-read the project's Available Extensions table (if present in CLAUDE.md)
2. Verify skill awareness before delegating or executing domain tasks
3. If extension table is missing, check `.claude/skills/` to refresh awareness

This is lightweight — a brief check, not a full filesystem scan. See [Extension Discovery](extension-discovery.md) for the full Three-Point Reinforcement Pattern.

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
