---
type: index
scope: components
file_count: 10
last_updated: 2026-04-05
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
| [Output Styles](output-styles.md) | Configuration | System prompt modification |
| [LSP Integration](lsp-integration.md) | Automatic | Real-time code intelligence |
| [Plugin Persistent Data](plugin-persistent-data.md) | Runtime | Plugin state management |
| [Knowledge Base](knowledge-base-structure.md) | Reference | Domain content |

## Reading Order (Recommended)

1. **memory-claudemd.md** — Foundation for everything else
2. **agent-skills.md** — Core extension mechanism
3. **subagents.md** — Specialized task delegation
4. **custom-commands.md** — User shortcuts
5. **hooks.md** — Event automation
6. **mcp-integration.md** — External tools
7. **output-styles.md** — System prompt customization
8. **lsp-integration.md** — Code intelligence
9. **plugin-persistent-data.md** — Plugin data lifecycle
10. **knowledge-base-structure.md** — Domain knowledge organization

## By Invocation Pattern

### Automatic (Always Loaded)
- [memory-claudemd.md](memory-claudemd.md) — All tiers at session start
- [lsp-integration.md](lsp-integration.md) — Real-time diagnostics during edits
- Project rules from `.claude/rules/`

### Configuration (Session Start)

- [output-styles.md](output-styles.md) — System prompt modification

### Model-Invoked (Claude Decides)
- [agent-skills.md](agent-skills.md) — Triggered by task context
- [subagents.md](subagents.md) — Can also be user-invoked

### User-Invoked (Explicit Trigger)
- [custom-commands.md](custom-commands.md) — `/command-name` syntax

### Event-Driven
- [hooks.md](hooks.md) — System events trigger scripts

### Tool Calls
- [mcp-integration.md](mcp-integration.md) — External service integration

### Runtime / Infrastructure

- [plugin-persistent-data.md](plugin-persistent-data.md) — Plugin data lifecycle

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
| Reshape agent persona/behavior | Output Styles |
| Real-time code diagnostics | LSP Integration |
| Plugin mutable state | Plugin Persistent Data |
| Domain reference content | Knowledge Base |

## Official Documentation

| Component | URL |
|-----------|-----|
| Memory | https://code.claude.com/docs/en/memory |
| Skills | https://code.claude.com/docs/en/skills |
| Subagents | https://code.claude.com/docs/en/sub-agents |
| Hooks | https://code.claude.com/docs/en/hooks-guide |
| MCP | https://code.claude.com/docs/en/mcp |
| Output Styles | https://code.claude.com/docs/en/output-styles |
| Plugins | https://code.claude.com/docs/en/plugins |
| Plugins Reference | https://code.claude.com/docs/en/plugins-reference |
