---
id: session-lifecycle
title: Session Lifecycle & Context Health
category: operational-patterns/state-management
tags: [sessions, resume, history, context-health, compaction, continue]
summary: Managing CC session state — resumption, context health decision framework, compaction strategy, and monitoring patterns.
depends_on: []
related: [context-engineering, filesystem-patterns, orchestration-framework]
complexity: foundational
last_updated: 2026-04-05
estimated_tokens: 800
source: https://code.claude.com/docs/en/context-window
confidence: A
review_by: 2026-07-05
revision_note: "v3.0 — Split from session-management.md. Session lifecycle + context health. Filesystem patterns and context engineering extracted to sibling files."
---

# Session Lifecycle & Context Health

## Session Mechanics

> **Official docs**: [Context Window](https://code.claude.com/docs/en/context-window), [Costs](https://code.claude.com/docs/en/costs) — for native session mechanics, context pricing, 1M extended context.

### Resuming Sessions

```bash
claude --continue        # Continue most recent (shorthand: claude -c)
claude --resume abc123   # Resume specific session
claude --resume          # Interactive selection
```

In-session: `/resume` (interactive), `/history` (view history).

### Session Storage

Sessions stored as JSONL transcript files locally. Contains full conversation history including tool usage and outputs.

### Cross-Device

```bash
claude --teleport    # Transfer session to claude.ai/code for browser access
```

---

## Context Loading Order

CC loads context in this sequence at session start:

```
1. System prompt (static sections — cached globally)
2. Auto Memory (MEMORY.md, first 200 lines)
3. Environment info
4. MCP tool schemas (deferred by default)
5. Skill descriptions (~100 tokens each)
6. User CLAUDE.md (~/.claude/CLAUDE.md)
7. Project CLAUDE.md (./CLAUDE.md, .claude/rules/*.md)
8. Conversation history
```

**Implication**: CLAUDE.md content lands toward the middle-end of context. Keep high-priority instructions early in the file (they'll be closer to the active attention zone).

**Tool schema deferment**: MCP tools are deferred by default — only the tool name is loaded; full schema fetched on demand. Enable explicit search via `ENABLE_TOOL_SEARCH` env var.

**1M extended context**: Opus 4.6 and Sonnet 4.6 support 1M token context via `[1m]` model suffix. Standard pricing applies.

---

## Context Health Decision Framework

| Signal | Action |
|--------|--------|
| Task going well, related work ahead | **Continue** — momentum is valuable |
| Context >70% full, work on-track | **Compact** — `/compact` to reclaim space |
| Stuck in fix→slop→fix loop | **Fresh session** — context is poisoned |
| Switching to unrelated domain/task | **Fresh session** — stale context dilutes quality |
| Long session, occasional drift | **Compact + re-anchor** — compact, then re-state objective |

### Compaction Cascade (Observable Behavior)

CC uses a multi-stage compaction system:

| Stage | Trigger | What Happens | Cost |
|-------|---------|-------------|------|
| MicroCompact | 60+ min cache expiry | Edits cached tool results locally, zero API calls | Free |
| AutoCompact | `effectiveContextWindow - 13,000` tokens | Generates up to 20K-token structured summary | Moderate |
| Full Compact | Manual `/compact` or system-triggered | 9-section narrative summary, 50K-token budget reset | Expensive |

**Key formula**: `autoCompactThreshold = effectiveContextWindow - 13,000`

**After compaction**:
- CLAUDE.md is re-read from disk (survives compaction)
- Skill descriptions are NOT re-injected — only invoked skills preserved
- Extension awareness may degrade — see [Extension Discovery](../extension-discovery.md)

### Monitoring

```bash
/statusline    # Real-time context %, git branch, session ID
/context       # See what's consuming space; prune if needed
```

---

## Plan Mode

For non-trivial tasks, force plan-first execution:

- **Interactive**: Shift+Tab twice to enter Plan Mode
- **CLI**: `claude --plan` to start in plan-only mode
- **In-session**: Type "plan mode" or Shift+Tab toggle

Plan Mode makes Claude outline approach before writing code. The CAB `execute-task` skill enforces this automatically.

---

## Session Best Practices

1. **End with summaries** — descriptive final messages aid resumption
2. **Commit frequently** — git commits serve as session checkpoints
3. **Use worktrees for parallel work** — separate sessions per worktree
4. **Don't rely solely on sessions** — document decisions in `notes/`
5. **Compact proactively at ~70%** — don't wait for auto-compact cascade
6. **Start fresh when poisoned** — a broken context produces broken output; no amount of compacting fixes a fix→slop→fix loop

## See Also

- [Context Engineering](context-engineering.md) — Optimization patterns, 200-line discipline
- [Filesystem Patterns](filesystem-patterns.md) — State files, cold-start anchors
- [Extension Discovery](../extension-discovery.md) — Post-compaction extension re-anchoring
