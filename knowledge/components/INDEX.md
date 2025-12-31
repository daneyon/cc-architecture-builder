---
type: index
scope: components
file_count: 7
last_updated: 2025-12-23
version: 0.5.0
changelog: Updated memory-claudemd.md (5-tier), agent-skills.md, mcp-integration.md, subagents.md with new URLs and content
---

# Components Index

> Claude Code plugin components that extend functionality.

## Quick Reference

| Component | Invocation | Purpose |
|-----------|------------|---------|
| [Memory (CLAUDE.md)](memory-claudemd.md) | Automatic | Persistent instructions |
| [Agent Skills](agent-skills.md) | Model-invoked | Capabilities |
| [Subagents](subagents.md) | Model/user | Specialized assistants |
| [Custom Commands](custom-commands.md) | User-invoked | Shortcuts |
| [Hooks](hooks.md) | Event-driven | Automation |
| [MCP Integration](mcp-integration.md) | Tool calls | External connections |
| [Knowledge Base](knowledge-base-structure.md) | Reference | Domain content |

## What's New in v0.5.0

All files updated with:
- New documentation URLs (`code.claude.com/docs/en/*`)
- `source:` metadata linking to authoritative docs

**memory-claudemd.md** — Major updates:
- 5-tier memory hierarchy (added Project Rules tier)
- `.claude/rules/` modular rules system
- Path-specific rules with `paths:` frontmatter
- User-level rules (`~/.claude/rules/`)

**agent-skills.md** — Updated:
- `allowed-tools` frontmatter for tool restrictions
- Plugin skills documentation
- Debugging guidance

**mcp-integration.md** — Updated:
- Transport types (HTTP recommended, SSE deprecated)
- Scope changes (local/project/user)
- Plugin MCP servers
- Resources and prompts
- Enterprise configuration

**subagents.md** — Updated:
- Built-in subagents (General-purpose, Plan, Explore)
- `permissionMode` and `skills` fields
- Resumable subagents
- CLI-based configuration

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
- [memory-claudemd.md](memory-claudemd.md) — All tiers at session start
- Project rules from `.claude/rules/`

### Model-Invoked (Claude Decides)
- [agent-skills.md](agent-skills.md) — Triggered by task context
- [subagents.md](subagents.md) — Can also be user-invoked

### User-Invoked (Explicit Trigger)
- [custom-commands.md](custom-commands.md) — `/command-name` syntax

### Event-Driven
- [hooks.md](hooks.md) — System events trigger scripts

### Tool Calls
- [mcp-integration.md](mcp-integration.md) — External service integration

## Component Relationships

```
CLAUDE.md (memory) + .claude/rules/
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
| Modular topic rules | .claude/rules/ |
| Automatic capability trigger | Skills |
| Delegated specialized work | Subagents |
| User-triggered shortcuts | Commands |
| Automated validation/formatting | Hooks |
| External tool access | MCP |
| Domain reference content | Knowledge Base |

## Official Documentation

| Component | URL |
|-----------|-----|
| Memory | https://code.claude.com/docs/en/memory |
| Skills | https://code.claude.com/docs/en/skills |
| Subagents | https://code.claude.com/docs/en/sub-agents |
| Hooks | https://code.claude.com/docs/en/hooks-guide |
| MCP | https://code.claude.com/docs/en/mcp |
| Plugins | https://code.claude.com/docs/en/plugins |
