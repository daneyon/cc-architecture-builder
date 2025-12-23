---
type: index
scope: components
file_count: 7
last_updated: 2025-12-18
version: 0.4.0
changelog: Updated agent-skills.md and mcp-integration.md with Anthropic skill-creator/mcp-builder insights
---

# Components Index

> Claude Code plugin components that extend functionality.

## Quick Reference

| Component | Invocation | Purpose |
|-----------|------------|---------|
| [Memory (CLAUDE.md)](memory-claudemd.md) | Automatic | Persistent instructions |
| [Agent Skills](agent-skills.md) | Model-invoked | Capabilities **(Updated v0.4.0)** |
| [Subagents](subagents.md) | Model/user | Specialized assistants |
| [Custom Commands](custom-commands.md) | User-invoked | Shortcuts |
| [Hooks](hooks.md) | Event-driven | Automation |
| [MCP Integration](mcp-integration.md) | Tool calls | External connections **(Updated v0.4.0)** |
| [Knowledge Base](knowledge-base-structure.md) | Reference | Domain content |

## What's New in v0.4.0

**agent-skills.md** — Updated based on Anthropic skill-creator review:
- Three bundled resource types: `scripts/`, `references/`, `assets/`
- Allowed frontmatter fields (name, description, license, allowed-tools, metadata)
- Degrees of freedom framework (high/medium/low)
- What NOT to include in skills
- Skill creation process (6 steps)
- Packaging skills as `.skill` files

**mcp-integration.md** — Updated based on Anthropic mcp-builder review:
- Server naming conventions (Python vs TypeScript)
- Tool naming best practices (service prefix)
- Transport selection guide (stdio vs Streamable HTTP)
- Tool annotations (readOnlyHint, destructiveHint, etc.)
- Error handling patterns
- Security best practices

**Related bundled skills**:
- `skills/skill-creator/` — Comprehensive skill authoring guidance
- `skills/mcp-builder/` — MCP server development guide

## Reading Order (Recommended)

1. **memory-claudemd.md** — Foundation for everything else
2. **agent-skills.md** — Core extension mechanism
3. **subagents.md** — Specialized task delegation
4. **custom-commands.md** — User shortcuts
5. **hooks.md** — Event automation
6. **mcp-integration.md** — External tools
7. **knowledge-base-structure.md** — Domain knowledge organization

## By Invocation Pattern

### Automatic (Always Loaded)
- [memory-claudemd.md](memory-claudemd.md) — Loaded at session start

### Model-Invoked (Claude Decides)
- [agent-skills.md](agent-skills.md) — Triggered by task context
- [subagents.md](subagents.md) — Can also be user-invoked

### User-Invoked (Explicit Trigger)
- [custom-commands.md](custom-commands.md) — `/command-name` syntax

### Event-Driven
- [hooks.md](hooks.md) — System events trigger scripts

### Tool Calls
- [mcp-integration.md](mcp-integration.md) — External service integration

## By Complexity

### Foundational
- memory-claudemd.md
- custom-commands.md

### Intermediate
- agent-skills.md
- subagents.md
- hooks.md
- mcp-integration.md
- knowledge-base-structure.md

## Component Relationships

```
CLAUDE.md (memory)
    │
    ├── Points to → Knowledge Base
    │
    ├── Loads → Skills (metadata)
    │
    └── Configures → Hooks, MCP

Skills ←→ Subagents (alternatives for different needs)
    │
    └── Can reference → Knowledge Base files

Commands → User shortcuts (independent)

Hooks → React to all tool usage (cross-cutting)
```

## Decision Guide

| Need | Component |
|------|-----------|
| Persistent instructions | CLAUDE.md |
| Automatic capability trigger | Skills |
| Delegated specialized work | Subagents |
| User-triggered shortcuts | Commands |
| Automated validation/formatting | Hooks |
| External tool access | MCP |
| Domain reference content | Knowledge Base |

## For Detailed Implementation

| Topic | Bundled Skill |
|-------|---------------|
| Creating new skills | `skills/skill-creator/SKILL.md` |
| Workflow patterns | `skills/skill-creator/references/workflows.md` |
| Output patterns | `skills/skill-creator/references/output-patterns.md` |
| Building MCP servers | `skills/mcp-builder/SKILL.md` |
| MCP best practices | `skills/mcp-builder/reference/mcp_best_practices.md` |
| Python MCP servers | `skills/mcp-builder/reference/python_mcp_server.md` |
| TypeScript MCP servers | `skills/mcp-builder/reference/node_mcp_server.md` |
