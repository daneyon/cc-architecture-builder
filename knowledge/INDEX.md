---
type: index
scope: master
file_count: 27
last_updated: 2026-04-03
---

# Knowledge Base Index

> Claude Code Architecture Guide — Atomized for efficient retrieval

## Quick Reference

| Category | Files | Purpose |
|----------|-------|---------|
| `overview/` | 3 | Executive summary, architecture philosophy, design principles |
| `prerequisites/` | 2 | Git foundation, security defaults |
| `schemas/` | 3 | Global user config, distributable plugin, architecture diagrams |
| `components/` | 7 | Deep dives on each component type |
| `distribution/` | 2 | Marketplace, sharing, Cowork |
| `reference/` | 1 | Product design lifecycle (conceptual advisory framework) |
| `operational-patterns/` | 6 | Orchestration, worktrees, sessions, multi-agent, team collaboration, extension discovery |
| `implementation/` | 1 | Step-by-step workflow |
| `appendices/` | 2 | Glossary, references |

## Documentation Sources

KB files should include `source:` metadata linking to official documentation. Primary sources:
- **Primary**: https://code.claude.com/docs/en/
- **Agent Skills**: https://code.claude.com/docs/en/skills
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

**Key files**:
- `components/memory-claudemd.md` — 4-scope hierarchy, auto memory, context engineering
- `components/agent-skills.md` — Model-invoked capabilities
- `components/mcp-integration.md` — External tool connections

### Advanced Patterns?

- `operational-patterns/orchestration/framework.md` — Canonical patterns, execution protocol
- `operational-patterns/multi-agent/worktree-workflows.md` — Parallel execution
- `operational-patterns/multi-agent/collaboration-patterns.md` — Agent coordination

## Category Summaries

### Overview (3 files)

Foundational understanding of the architecture and its principles.

- `executive-summary.md` — Two-schema architecture, 4-scope memory, visual overview
- `architecture-philosophy.md` — Memory hierarchy, invocation patterns, distribution strategy
- `design-principles.md` — Core design tenets and guiding principles

### Prerequisites (2 files)
Required setup and security considerations.

- `git-foundation.md` — Git as requirement, setup checklist, GitHub integration
- `security-defaults.md` — Private repos, pre-publication checklist, credential handling

### Schemas (3 files)

Complete structure specifications for both configuration layers.

- `global-user-config.md` — `~/.claude/` structure, personal baseline, settings
- `distributable-plugin.md` — Plugin structure, plugin.json schema, knowledge organization
- `cc-architecture-diagrams.md` — Mermaid architecture diagrams and visual references

### Components (7 files)
Detailed documentation for each plugin component type.

- `memory-claudemd.md` — 5-tier memory system, imports, project rules
- `agent-skills.md` — Model-invoked capabilities, SKILL.md format, progressive disclosure
- `subagents.md` — Specialized assistants, separate context, built-in agents
- `custom-commands.md` — User-invoked shortcuts, slash commands
- `hooks.md` — Event-driven automation
- `mcp-integration.md` — External tool connections, server development patterns
- `knowledge-base-structure.md` — KB organization, indexing, retrieval

### Distribution (2 files)

Sharing and marketplace publication.

- `marketplace.md` — Plugin distribution, team configuration, security review
- `cowork.md` — Cowork sessions, enterprise distribution, team sharing

### Operational Patterns (12 files in 3 subdirectories + 2 root)

Advanced workflow and orchestration patterns. See `operational-patterns/INDEX.md` for full directory structure.

- `orchestration/` — Framework tenets, canonical patterns, delegation templates, cost model
- `multi-agent/` — Collaboration patterns, Agent Teams, worktree workflows
- `state-management/` — Session lifecycle, context engineering, filesystem state patterns
- `team-collaboration.md` — Shared-repo conventions, conflict resolution, PR review workflows
- `extension-discovery.md` — Extension discovery patterns, Three-Point Reinforcement

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
