---
id: architecture-philosophy
title: Architecture Philosophy
category: overview
tags: [philosophy, memory-hierarchy, invocation, distribution, principles]
summary: Core architectural principles including the 4-tier memory hierarchy, component invocation patterns, and distribution strategy using @imports.
depends_on: [executive-summary]
related: [memory-claudemd, agent-skills, subagents]
complexity: foundational
last_updated: 2025-12-12
estimated_tokens: 700
---

# Architecture Philosophy

## The Memory Hierarchy

Claude Code implements a 4-tier memory hierarchy with clear precedence:

| Tier | Location | Purpose | Shared With |
|------|----------|---------|-------------|
| **1. Enterprise Policy** | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | Organization-wide standards | All org users |
| **2. User Memory** | `~/.claude/CLAUDE.md` | Personal preferences (all projects) | Just you |
| **3. Project Memory** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared instructions | Team via git |
| **4. Subtree Memory** | `./subdir/CLAUDE.md` | Directory-specific context | Team via git |

**Precedence Rule**: Files higher in the hierarchy load first and take precedence. Project-level files can supplement but not override enterprise/user policies.

## Invocation Patterns

Understanding how Claude Code components are triggered is critical:

| Component | Invocation Type | Trigger | Context Impact |
|-----------|-----------------|---------|----------------|
| **Memory (CLAUDE.md)** | Automatic | Always loaded at session start | Adds to main context |
| **Skills** | Model-invoked | Claude autonomously decides based on task | Adds to main context when triggered |
| **Subagents** | Model or user-invoked | Auto-delegated or explicitly called | Separate context window |
| **Commands** | User-invoked | Explicitly typed (e.g., `/analyze`) | Adds to main context |
| **Hooks** | Event-driven | System events (PreToolUse, PostToolUse, etc.) | Executes externally |

### Invocation Flow

```
Session Start
    │
    ▼
┌─────────────────────────────────────────┐
│ CLAUDE.md loaded (all tiers merged)     │ ← Automatic
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ Skill metadata loaded (name/description)│ ← Automatic
└────────────────┬────────────────────────┘
                 │
    User sends message
                 │
                 ▼
┌─────────────────────────────────────────┐
│ Claude evaluates:                       │
│ - Does a skill match? → Load SKILL.md   │ ← Model-invoked
│ - Should delegate? → Invoke subagent    │ ← Model-invoked
│ - Tool needed? → Check hooks first      │ ← Event-driven
└─────────────────────────────────────────┘
```

## Distribution Philosophy

**Problem**: How do you share a complete working system while keeping global and project layers separate?

**Solution**: CLAUDE.md `@imports` enable optional personalization without bloating the plugin:

```markdown
# Project CLAUDE.md

## Core Instructions
[Self-contained project instructions]

## Personal Customization (Optional)
@~/.claude/project-preferences.md
```

**How it works**:
- If the user creates `~/.claude/project-preferences.md`, their preferences are loaded
- If the file doesn't exist, Claude proceeds without error
- The plugin remains self-contained and functional out of the box

## Progressive Disclosure

Load only what's needed to conserve tokens:

| Level | Content | When Loaded | Token Cost |
|-------|---------|-------------|------------|
| **1** | INDEX.md summaries | Session start (if referenced) | ~100 tokens each |
| **2** | File frontmatter | When Claude evaluates relevance | ~50 tokens each |
| **3** | Full file content | When Claude confirms need | Variable |

This pattern allows large knowledge bases without overwhelming context.

## Key Implications

1. **Design for Discovery**: Claude must know what exists before it can retrieve
2. **Explicit Relationships**: No semantic search—link files explicitly
3. **Right-Size Content**: Atomic files enable selective loading
4. **Test Invocation**: Verify skills/agents trigger on expected inputs

## See Also

- [Memory System](../components/memory-claudemd.md) — CLAUDE.md details
- [Agent Skills](../components/agent-skills.md) — Model-invoked capabilities
- [Subagents](../components/subagents.md) — Separate context assistants
