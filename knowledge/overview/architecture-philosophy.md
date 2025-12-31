---
id: architecture-philosophy
title: Architecture Philosophy
category: overview
tags: [philosophy, memory-hierarchy, invocation, distribution, principles]
summary: Core architectural principles including the 5-tier memory hierarchy, component invocation patterns, and distribution strategy.
depends_on: [executive-summary]
related: [memory-claudemd, agent-skills, subagents]
complexity: foundational
last_updated: 2025-12-23
estimated_tokens: 800
---

# Architecture Philosophy

## The Memory Hierarchy

Claude Code implements a 5-tier memory hierarchy with clear precedence:

| Tier | Location | Purpose | Shared With |
|------|----------|---------|-------------|
| **1. Enterprise Policy** | System paths* | Organization-wide standards | All org users |
| **2. Project Memory** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared instructions | Team via git |
| **3. Project Rules** | `./.claude/rules/*.md` | Modular topic-specific rules | Team via git |
| **4. User Memory** | `~/.claude/CLAUDE.md` | Personal preferences (all projects) | Just you |
| **5. Project Local** | `./CLAUDE.local.md` | Personal project-specific | Just you |

*Enterprise paths:
- macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
- Linux: `/etc/claude-code/CLAUDE.md`
- Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`

**Precedence Rule**: Files higher in hierarchy load first and take precedence.

### Project Rules (.claude/rules/)

New in 2025: Modular rules for larger projects:

```
.claude/rules/
├── code-style.md     # Code formatting
├── testing.md        # Test conventions
└── security.md       # Security requirements
```

Rules support path-specific scoping via frontmatter:
```yaml
---
paths: src/api/**/*.ts
---
# API-specific rules here
```

## Invocation Patterns

| Component | Invocation Type | Trigger | Context Impact |
|-----------|-----------------|---------|----------------|
| **Memory (CLAUDE.md)** | Automatic | Session start | Main context |
| **Project Rules** | Automatic | Session start | Main context |
| **Skills** | Model-invoked | Claude decides | Main context when triggered |
| **Subagents** | Model or user-invoked | Delegated/explicit | Separate context |
| **Commands** | User-invoked | `/command-name` | Main context |
| **Hooks** | Event-driven | System events | External execution |

### Invocation Flow

```
Session Start
    │
    ▼
┌─────────────────────────────────────────┐
│ Memory loaded (all tiers merged)        │ ← Automatic
│ + Project rules from .claude/rules/     │
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

**Solution**: CLAUDE.md `@imports` enable optional personalization:

```markdown
# Project CLAUDE.md

## Core Instructions
[Self-contained project instructions]

## Personal Customization (Optional)
@~/.claude/project-preferences.md
```

**How it works**:
- If user creates the referenced file, preferences load
- If file doesn't exist, Claude proceeds without error
- Plugin remains self-contained and functional

## Progressive Disclosure

Load only what's needed to conserve tokens:

| Level | Content | When Loaded | Token Cost |
|-------|---------|-------------|------------|
| **1** | Skill metadata | Session start | ~100 tokens/skill |
| **2** | SKILL.md body | When skill triggered | < 5k words |
| **3** | Bundled resources | As needed | Unlimited |

This pattern enables large knowledge bases without overwhelming context.

## Key Implications

1. **Design for Discovery**: Claude must know what exists before retrieval
2. **Explicit Relationships**: No semantic search—link files explicitly
3. **Right-Size Content**: Atomic files enable selective loading
4. **Modular Organization**: Use `.claude/rules/` for larger projects
5. **Test Invocation**: Verify skills/agents trigger on expected inputs

## See Also

- [Memory System](../components/memory-claudemd.md) — CLAUDE.md and rules details
- [Agent Skills](../components/agent-skills.md) — Model-invoked capabilities
- [Subagents](../components/subagents.md) — Separate context assistants
