---
id: architecture-philosophy
title: Architecture Philosophy
category: overview
tags: [philosophy, memory-hierarchy, invocation, distribution, wrapper, progressive-disclosure]
summary: Core architectural philosophy — CAB as intermediary wrapper layer, 4-scope memory hierarchy, extension invocation patterns, and progressive disclosure design.
depends_on: [executive-summary]
related: [design-principles, memory-claudemd, agent-skills, subagents]
complexity: foundational
last_updated: 2026-04-05
estimated_tokens: 900
source: https://code.claude.com/docs/en/memory
confidence: A
review_by: 2026-07-05
---

# Architecture Philosophy

## The Intermediary Wrapper Architecture

CAB operates as an **intermediary wrapper layer** between two surfaces:

1. **Upstream**: Claude Code's official platform (docs, runtime, APIs)
2. **Downstream**: Project codebases that integrate CC

```
┌──────────────────────────────────────────────────┐
│  Official CC Platform                             │
│  code.claude.com/docs/en/                         │
│  (memory, skills, agents, hooks, plugins, MCP)    │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│  CAB: Intermediary Wrapper Layer                  │
│  ┌──────────────────────────────────────────────┐│
│  │ Operational patterns (orchestration, state)   ││
│  │ Standardized workflows (execute, verify)      ││
│  │ Domain specialization (KB, agents, skills)    ││
│  │ Programmatic extensions (hooks, automation)   ││
│  └──────────────────────────────────────────────┘│
│  Links to CC docs for native details              │
│  Adds value BEYOND what CC docs cover             │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│  Project Codebases                                │
│  Integrated via /integrate-existing               │
└──────────────────────────────────────────────────┘
```

**Core rule**: CAB KB files never duplicate native CC documentation. They:

- **Link** to official docs (`source:` frontmatter) for CC-native feature details
- **Extend** with operational patterns, standardized workflows, and domain frameworks
- **Wrap** CC primitives into readily actionable, programmatic extensions
- **Bridge** multiple CC features into coherent end-to-end guidance

If CC docs cover a topic adequately, CAB provides a pointer with hyperlink — not a restatement.

## Memory Architecture

CC implements a **4-scope configuration hierarchy** with clear precedence:

| Scope | Location | Shared With |
|-------|----------|-------------|
| **1. Managed** | System paths / MDM / registry | Org-wide (enterprise) |
| **2. Project** | `./CLAUDE.md`, `.claude/rules/*.md` | Team via git |
| **3. User** | `~/.claude/CLAUDE.md` | Personal (all projects) |
| **4. Local** | `./CLAUDE.local.md` | Personal (this project) |

> **Official docs**: [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory) — full details on scopes, @imports, HTML stripping, `claudeMdExcludes`, auto memory.

**CAB-specific guidance**:

- **200-line discipline**: Each CLAUDE.md targets ≤200 lines. This aligns with CC's official recommendation and auto memory's 200-line/25KB load limit. Every token of instruction displaces productive output.
- **Seed instruction design**: CC's memory is increasingly autonomous (auto memory, background consolidation via autoDream). Write CLAUDE.md as *seed instructions* that survive consolidation — not exhaustive procedural checklists that get pruned.
- **Auto memory complement**: CC maintains agent-generated memory (`MEMORY.md` + topic files) separate from CLAUDE.md. CAB's `notes/` state management patterns complement this with structured persistent state. See [Memory System](../components/memory-claudemd.md) for detail.

### Runtime Memory Pipeline (Observable Behavior)

Beyond the 4-scope configuration, CC's runtime operates a multi-layer escalation pipeline where each layer prevents the next from firing:

| Layer | What Happens | Cost |
|-------|-------------|------|
| CLAUDE.md + Auto Memory | Loaded at session start | Free |
| Session Memory | Summaries every ~5K tokens | Low |
| MicroCompact | Local editing of cached tool results (zero API calls) | Free |
| AutoCompact | Structured summary at `effectiveContextWindow - 13,000` tokens | Moderate |
| Full Compact | Complete conversation compression (9-section narrative) | Expensive |
| Session Reset | Clears everything except system prompt | Destructive |

**Practical implication**: Proactive management (compacting at ~70%, or starting fresh sessions) avoids forced compaction cascades. See [Session Management](../operational-patterns/session-management.md) for decision framework.

## Invocation & Extension Patterns

CC extensions compose through distinct invocation and context patterns:

| Component | Trigger | Context | Notes |
|-----------|---------|---------|-------|
| **CLAUDE.md + Rules** | Automatic (session start) | Main | Always loaded |
| **Skills** | Model-invoked or `/name` | Main (inline) or forked | Preferred over commands; 11 frontmatter fields |
| **Agents** | Model/user-invoked | Separate context | Isolated; don't inherit parent skills |
| **Hooks** | Event-driven (26 events) | External | 4 types: command, http, prompt, agent |
| **MCP Servers** | Tool calls | Deferred schemas | Connected on start, disconnected on finish |

> **Official docs**: [Skills](https://code.claude.com/docs/en/skills), [Sub-agents](https://code.claude.com/docs/en/sub-agents), [Hooks](https://code.claude.com/docs/en/hooks), [MCP](https://code.claude.com/docs/en/mcp)

**Key evolution (2026)**: Custom commands (`.claude/commands/`) merged into skills. Skills are the preferred path — commands still work but skills win when both exist. CAB maintains concise abbreviated names for plugin-level commands to preserve quick-trigger usability (e.g., `/cab:execute-task` not `/cc-architecture-builder:execute-task`).

### Invocation Flow

```
Session Start
    ├─ CLAUDE.md (all scopes merged)     ── automatic
    ├─ Auto Memory (MEMORY.md ≤200 ln)   ── automatic
    ├─ Skill metadata (name/desc only)    ── automatic (~100 tokens each)
    ├─ MCP tool schemas                   ── deferred by default
    │
    User sends message
    │
    ├─ Skill match? → Load full SKILL.md (inline or context:fork)
    ├─ Delegation? → Spawn subagent (separate context window)
    ├─ Tool call? → Hooks fire pre/post; MCP tools available
    └─ Background? → Forked agent, shared prompt cache (~76% savings)
```

## Progressive Disclosure & 200-Line Discipline

The 200-line discipline naturally enforces progressive disclosure:

| Level | Content | When | Token Cost |
|-------|---------|------|------------|
| **L0** | CLAUDE.md seed instructions | Session start | ≤200 lines |
| **L1** | Skill/agent metadata | Session start | ~100 tokens each |
| **L2** | Full skill content | When triggered | Variable |
| **L3** | KB files, bundled resources | On-demand (grep/read) | Variable |
| **L4** | External docs via MCP/web | When needed | External |

**Design implication**: Keep L0 lean. Reference L2-L4 via @imports and skill invocations rather than embedding content. A CLAUDE.md that tries to load everything upfront wastes the context budget on content that may never be relevant to the current task.

## Key Implications

1. **Link, don't duplicate** — Official CC docs are the source of truth for CC-native features
2. **Design for discovery** — Claude must know what exists (L1 metadata) before retrieving detail (L2-L3)
3. **Atomic files** — Single topic, self-contained, independently retrievable by agents
4. **Test invocation** — Verify skills/agents trigger on expected inputs after any schema change
5. **Modular rules** — Use `.claude/rules/` with `paths:` frontmatter for project-specific scoping
6. **Seed over procedure** — CLAUDE.md instructions should be durable guidance, not brittle step-by-step recipes

## See Also

- [Design Principles](design-principles.md) — Core tenets governing the CAB framework
- [Memory System](../components/memory-claudemd.md) — Detailed memory patterns + auto memory
- [Session Management](../operational-patterns/session-management.md) — Context health, compaction, persistence
- [Orchestration Framework](../operational-patterns/orchestration-framework.md) — Canonical workflow patterns
