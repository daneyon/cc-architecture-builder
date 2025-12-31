---
id: executive-summary
title: Executive Summary
category: overview
tags: [architecture, two-schema, principles, overview]
summary: High-level overview of the two-schema Claude Code architecture, core design principles, and visual structure representation.
depends_on: []
related: [architecture-philosophy, global-user-config, distributable-plugin]
complexity: foundational
last_updated: 2025-12-23
estimated_tokens: 700
---

# Executive Summary

## Purpose

This architecture establishes a standardized framework for building custom LLM solutions using Claude Code. It addresses the separation of concerns between **personal configuration** (global settings that travel with you) and **distributable projects** (shareable plugins with domain-specific capabilities).

## Core Insight

Claude Code is not merely a coding assistant—it is a configurable AI platform with filesystem access, tool integration, and extensible capabilities. This architecture leverages Claude Code for any custom LLM use case: technical coding projects, research assistants, domain-specific knowledge bases, or educational tutors.

## Two-Schema Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SCHEMA 1: GLOBAL USER CONFIGURATION                                        │
│  Location: ~/.claude/                                                        │
│  Purpose: Personal baseline, cross-project preferences                       │
│  Scope: Private to you, applies to ALL projects                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  ~/.claude/                                                                  │
│  ├── CLAUDE.md              # Your personal system instructions              │
│  ├── settings.json          # User settings (model, permissions)             │
│  ├── rules/                 # Personal modular rules                         │
│  ├── skills/                # Personal skills (available everywhere)         │
│  └── agents/                # Personal agents                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ inherits / supplements
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  SCHEMA 2: DISTRIBUTABLE PLUGIN PROJECT                                      │
│  Location: ./your-project/                                                   │
│  Purpose: Domain-specific custom LLM, shareable via marketplace              │
│  Scope: Team/community distribution                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  your-plugin/                                                                │
│  ├── .claude-plugin/plugin.json   # Marketplace metadata                     │
│  ├── CLAUDE.md                    # Project system instructions              │
│  ├── CLAUDE.local.md              # Personal project overrides (gitignored)  │
│  ├── .claude/rules/               # Modular project rules                    │
│  ├── .mcp.json                    # MCP server configurations                │
│  ├── commands/                    # Custom slash commands                    │
│  ├── agents/                      # Project-specific subagents               │
│  ├── skills/                      # Project-specific skills                  │
│  ├── hooks/                       # Event handlers                           │
│  ├── knowledge/                   # Domain knowledge base                    │
│  └── docs/                        # Documentation                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Memory Hierarchy (5 Tiers)

| Tier | Location | Purpose | Shared With |
|------|----------|---------|-------------|
| **1. Enterprise Policy** | System paths | Organization-wide standards | All org users |
| **2. Project Memory** | `./CLAUDE.md` | Team-shared instructions | Team via git |
| **3. Project Rules** | `./.claude/rules/*.md` | Modular topic-specific rules | Team via git |
| **4. User Memory** | `~/.claude/CLAUDE.md` | Personal preferences | Just you |
| **5. Local Memory** | `./CLAUDE.local.md` | Personal project-specific | Just you |

**Precedence**: Higher tiers load first and take precedence.

## Key Design Principles

| Principle | Description |
|-----------|-------------|
| **Separation of Concerns** | Global config stays personal; project config is distributable |
| **Progressive Disclosure** | Load only what's needed; reference additional files via `@imports` |
| **Convention over Configuration** | Follow official directory structures; minimize custom conventions |
| **Git-Native Workflow** | Version control everything; enable team collaboration |
| **Token Efficiency** | Keep CLAUDE.md concise; use skills/agents for complex instructions |
| **Security by Default** | Private repos, credential exclusion, pre-publication review |

## When to Use Each Schema

### Use Global Config (Schema 1) For:
- Personal communication preferences
- Cross-project utilities and skills
- Default behaviors you want everywhere
- Private settings that shouldn't be shared

### Use Plugin Project (Schema 2) For:
- Domain-specific knowledge and expertise
- Team-shared workflows and standards
- Distributable custom LLM solutions
- Project-specific integrations

## See Also

- [Architecture Philosophy](architecture-philosophy.md) — Deeper principles
- [Global User Config](../schemas/global-user-config.md) — Schema 1 details
- [Distributable Plugin](../schemas/distributable-plugin.md) — Schema 2 details
