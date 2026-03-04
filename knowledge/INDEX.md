---
type: index
scope: master
file_count: 26
last_updated: 2026-03-03
version: 0.8.0
changelog: "v0.8.0 — Added cowork.md (desktop automation, enterprise distribution). Updated global-user-config.md (agent field, orchestrator pattern, rules/). Updated orchestration-framework.md (Tenet 6: autonomous multi-agent operation, global-as-orchestrator). Distribution INDEX updated."
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
| `distribution/` | 2 | Marketplace, sharing, Cowork |
| `operational-patterns/` | 4 | Orchestration, worktrees, sessions, multi-agent |
| `implementation/` | 1 | Step-by-step workflow |
| `appendices/` | 2 | Glossary, references |

## Documentation Sources

All KB files include `source:` metadata linking to official documentation:
- **Primary**: https://code.claude.com/docs/en/
- **Agent Skills**: https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/
- **MCP Protocol**: https://modelcontextprotocol.io/

## External Skills Reference

For detailed skill/MCP authoring guidance, install from marketplace:
```bash
claude /plugin marketplace add https://github.com/anthropics/anthropic-agent-skills
claude /plugin install skill-creator@anthropic-agent-skills
claude /plugin install mcp-builder@anthropic-agent-skills
```

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

**Key files (v0.5.0)**:
- `components/memory-claudemd.md` — 5-tier hierarchy with project rules
- `components/agent-skills.md` — Model-invoked capabilities
- `components/mcp-integration.md` — External tool connections

### Advanced Patterns?

- `operational-patterns/orchestration-framework.md` — Canonical patterns, execution protocol, cost model **(New v0.6.0)**
- `operational-patterns/git-worktree.md` — Parallel execution
- `operational-patterns/multi-agent-collaboration.md` — Agent coordination **(Revised v0.6.0)**

## Category Summaries

### Overview (2 files)
Foundational understanding of the architecture and its principles.

- `executive-summary.md` — Two-schema architecture, 5-tier memory, visual overview
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

- `memory-claudemd.md` — 5-tier memory system, imports, project rules
- `agent-skills.md` — Model-invoked capabilities, SKILL.md format, progressive disclosure
- `subagents.md` — Specialized assistants, separate context, built-in agents
- `custom-commands.md` — User-invoked shortcuts, slash commands
- `hooks.md` — Event-driven automation
- `mcp-integration.md` — External tool connections, server development patterns
- `knowledge-base-structure.md` — KB organization, indexing, retrieval

### Distribution (1 file)
Sharing and marketplace publication.

- `marketplace.md` — Plugin distribution, team configuration, security review

### Operational Patterns (4 files)
Advanced workflow and orchestration patterns.

- `orchestration-framework.md` — Canonical agentic workflow patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer), task execution protocol, agent failure modes, multi-agent cost model, delegation templates, initializer/iterator harness, CC platform constraints **(New v0.6.0)**
- `git-worktree.md` — Parallel Claude Code sessions
- `session-management.md` — Resuming, history, persistence
- `multi-agent-collaboration.md` — Worktrees-first coordination, Agent Teams (experimental), effort scaling, cross-session persistence **(Revised v0.6.0)**

### Implementation (1 file)
Practical execution guide.

- `workflow.md` — Phased implementation, checklists, validation

### Appendices (2 files)
Reference materials.

- `glossary.md` — Term definitions
- `references.md` — Official documentation links (updated URLs)

## Search Tips

When looking for information:
- Use `grep` for specific terms across files
- Check INDEX.md in each category for file summaries
- Follow `related` links in file frontmatter
- Start with foundational files before advanced topics
- Check `source:` metadata for authoritative docs
