---
type: index
scope: master
file_count: 48
last_updated: 2026-04-30
revision_note: "Reference category resync (1 → 8): back-filled prior-relocated cards (a-team-database.yaml, requirements-doc-guide, visualization-workflow, workflow-processflow, prioritization-frameworks, ux-testing-agentic-os) + new llm-interaction-patterns. Components category bump (10 → 11): added component-decision-framework (DP8 realization layer)."
---

# Knowledge Base Index

> Claude Code Architecture Guide — Atomized for efficient retrieval

## Quick Reference

| Category | Files | Purpose |
|----------|-------|---------|
| `overview/` | 3 | Executive summary, architecture philosophy, design principles |
| `prerequisites/` | 2 | Git foundation, security defaults |
| `schemas/` | 3 | Global user config, distributable plugin, architecture diagrams |
| `components/` | 11 | Deep dives on each component type + DP8 decision framework |
| `distribution/` | 2 | Marketplace, sharing, Cowork |
| `reference/` | 8 | Advisory conceptual frameworks — LLM interaction patterns, product lifecycle, team roster, requirements docs, visualization, diagramming, prioritization, UX testing |
| `operational-patterns/` | 16 | Orchestration (3), multi-agent (4), state management (5), team collaboration, extension discovery, sync protocol, cross-project settings hardening |
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
- `components/output-styles.md` — System prompt customization
- `components/lsp-integration.md` — Real-time code intelligence

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

### Components (11 files)

Detailed documentation for each plugin component type, plus the cross-cutting decision framework that governs which component fits which content/behavior.

- `component-decision-framework.md` — DP8 realization (decision tree + per-component scope tests + 4-component memory ecosystem mechanics + worked examples). Consult **before** authoring any new component.
- `memory-claudemd.md` — 5-tier memory system, imports, project rules
- `agent-skills.md` — Model-invoked capabilities, SKILL.md format, progressive disclosure
- `subagents.md` — Specialized assistants, separate context, built-in agents
- `custom-commands.md` — User-invoked shortcuts, slash commands
- `hooks.md` — Event-driven automation
- `mcp-integration.md` — External tool connections, server development patterns
- `output-styles.md` — System prompt modification, custom style definitions
- `lsp-integration.md` — Real-time code intelligence, .lsp.json configuration
- `plugin-persistent-data.md` — CLAUDE_PLUGIN_DATA lifecycle, dependency patterns
- `knowledge-base-structure.md` — KB organization, indexing, retrieval

### Distribution (2 files)

Sharing and marketplace publication.

- `marketplace.md` — Plugin distribution, team configuration, security review
- `cowork.md` — Cowork sessions, enterprise distribution, team sharing

### Reference (8 files)

Advisory conceptual frameworks consulted on-demand by agents and skills. Not prescriptive doctrine. See `reference/INDEX.md` for per-file summaries.

- `llm-interaction-patterns.md` — Nine observable patterns governing LLM interaction reliability across attention/context, bootstrap/retrieval, invocation, authoring, ontology, verification surfaces
- `product-design-cycle.md` — Universal 7-phase product lifecycle, framework-agnostic synthesis
- `a-team-database.yaml` — Machine-parseable roster of 22 product team roles + CC extension mapping
- `requirements-doc-guide.md` — MRD / PRD / SRD deep dive + hybrid Startup Requirement Document
- `visualization-workflow.md` — Hybrid viz design workflow (Yau + Cleveland-McGill + Munzner)
- `workflow-processflow.md` — Workflow vs process flow diagram comparative reference
- `prioritization-frameworks.md` — 8 frameworks (RICE, MoSCoW, Kano, etc.) + tiered application stack
- `ux-testing-agentic-os.md` — Coupled UX-eval protocol (Nielsen + WCAG + ISO + LLM-eval practice)

### Operational Patterns (16 files in 3 subdirectories + 4 root)

Advanced workflow and orchestration patterns. See `operational-patterns/INDEX.md` for full directory structure.

- `orchestration/` — Framework tenets, canonical patterns, delegation templates, cost model
- `multi-agent/` — Collaboration patterns, Agent Teams, worktree workflows, agent resolution + shadowing
- `state-management/` — Session lifecycle, context engineering, filesystem state patterns, bootstrap read pattern, CC memory-layer alignment
- `team-collaboration.md` — Shared-repo conventions, conflict resolution, PR review workflows
- `extension-discovery.md` — Extension discovery patterns, Three-Point Reinforcement
- `sync-protocol.md` — CAB ↔ global `~/.claude/` deployment + drift protocol
- `cross-project-settings-hardening.md` — Settings.json layering pattern, default-deny on edits, tier discipline, drift detection

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
