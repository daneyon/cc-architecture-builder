---
type: index
scope: master
file_count: 24
last_updated: 2025-12-18
version: 0.4.0
changelog: Updated agent-skills.md and mcp-integration.md based on Anthropic skill-creator and mcp-builder review; added bundled skills references
---

# Knowledge Base Index

> Claude Code Architecture Guide — Atomized for efficient retrieval

## Quick Reference

| Category | Files | Purpose |
|----------|-------|---------|
| `overview/` | 2 | Executive summary, architecture philosophy |
| `prerequisites/` | 2 | Git foundation, security defaults |
| `schemas/` | 2 | Global user config, distributable plugin |
| `components/` | 7 | Deep dives on each component type |
| `distribution/` | 1 | Marketplace and sharing |
| `operational-patterns/` | 3 | Worktrees, sessions, multi-agent |
| `implementation/` | 1 | Step-by-step workflow |
| `appendices/` | 2 | Glossary, references |

## Bundled Skills Reference

This project includes two Anthropic-derived skills with comprehensive guidance:

| Skill | Purpose | Key Resources |
|-------|---------|---------------|
| `skills/skill-creator/` | Guide for creating effective skills | `references/workflows.md`, `references/output-patterns.md`, `scripts/init_skill.py` |
| `skills/mcp-builder/` | Guide for building MCP servers | `reference/mcp_best_practices.md`, `reference/python_mcp_server.md`, `reference/node_mcp_server.md` |

**When to use**: Consult these skills for detailed implementation guidance beyond what's in the knowledge base.

## Navigation Guide

### New to Claude Code Architecture?

1. Start with `overview/executive-summary.md`
2. Read `overview/architecture-philosophy.md`
3. Review `prerequisites/git-foundation.md`

### Setting Up Your First Project?

1. `schemas/global-user-config.md` — Personal configuration
2. `schemas/distributable-plugin.md` — Project structure
3. `implementation/workflow.md` — Step-by-step guide

### Deep Dive on Components?

See `components/INDEX.md` for reading order and relationships.

**Key updated files (v0.4.0)**:
- `components/agent-skills.md` — Updated with Anthropic skill-creator insights
- `components/mcp-integration.md` — Updated with Anthropic mcp-builder insights

### Advanced Patterns?

- `operational-patterns/git-worktree.md` — Parallel execution
- `operational-patterns/multi-agent-collaboration.md` — Agent coordination

## Category Summaries

### Overview (2 files)
Foundational understanding of the architecture and its principles.

- `executive-summary.md` — Two-schema architecture, core principles, visual overview
- `architecture-philosophy.md` — Memory hierarchy, invocation patterns, distribution strategy

### Prerequisites (2 files)
Required setup and security considerations.

- `git-foundation.md` — Git as requirement, setup checklist, GitHub integration
- `security-defaults.md` — Private repos, pre-publication checklist, credential handling

### Schemas (2 files)
Complete structure specifications for both configuration layers.

- `global-user-config.md` — `~/.claude/` structure, personal baseline, settings
- `distributable-plugin.md` — Plugin structure, plugin.json schema, knowledge organization

### Components (7 files)
Detailed documentation for each plugin component type.

- `memory-claudemd.md` — CLAUDE.md memory system, imports, hierarchy
- `agent-skills.md` — Model-invoked capabilities, SKILL.md format, progressive disclosure, bundled resources **(Updated v0.4.0)**
- `subagents.md` — Specialized assistants, separate context
- `custom-commands.md` — User-invoked shortcuts, slash commands
- `hooks.md` — Event-driven automation
- `mcp-integration.md` — External tool connections, server development patterns **(Updated v0.4.0)**
- `knowledge-base-structure.md` — KB organization, indexing, retrieval

### Distribution (1 file)
Sharing and marketplace publication.

- `marketplace.md` — Plugin distribution, team configuration, security review

### Operational Patterns (3 files)
Advanced workflow patterns for efficiency.

- `git-worktree.md` — Parallel Claude Code sessions
- `session-management.md` — Resuming, history, persistence
- `multi-agent-collaboration.md` — Agent coordination patterns

### Implementation (1 file)
Practical execution guide.

- `workflow.md` — Phased implementation, checklists, validation

### Appendices (2 files)
Reference materials.

- `glossary.md` — Term definitions
- `references.md` — Official documentation links, bundled skills reference **(Updated v0.4.0)**

## Search Tips

When looking for information:
- Use `grep` for specific terms across files
- Check INDEX.md in each category for file summaries
- Follow `related` links in file frontmatter
- Start with foundational files before advanced topics
- **For skill creation**: Consult `skills/skill-creator/SKILL.md`
- **For MCP development**: Consult `skills/mcp-builder/SKILL.md`
