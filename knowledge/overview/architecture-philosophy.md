---
id: architecture-philosophy
title: Architecture Philosophy
category: overview
tags: [philosophy, memory-hierarchy, invocation, distribution, wrapper, progressive-disclosure]
summary: Core architectural philosophy — CAB as intermediary wrapper layer, 4-scope memory hierarchy, extension invocation patterns, and progressive disclosure design.
depends_on: [executive-summary]
related: [design-principles, memory-claudemd, agent-skills, subagents]
complexity: foundational
last_updated: 2026-04-28
estimated_tokens: 1100
source: https://code.claude.com/docs/en/memory
confidence: A
review_by: 2026-07-28
---
# Architecture Philosophy

## The Intermediary Wrapper Architecture

CAB operates as an **intermediary wrapper layer** between two surfaces to effectively transform traditional legacy project codebase to an agentic OS platform (codebase + CC CLI):

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

| Scope                | Location                                | Shared With             |
| -------------------- | --------------------------------------- | ----------------------- |
| **1. Managed** | System paths / MDM / registry           | Org-wide (enterprise)   |
| **2. Project** | `./CLAUDE.md`, `.claude/rules/*.md` | Team via git            |
| **3. User**    | `~/.claude/CLAUDE.md`                 | Personal (all projects) |
| **4. Local**   | `./CLAUDE.local.md`                   | Personal (this project) |

> **Official docs**: [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory) — full details on scopes, @imports, HTML stripping, `claudeMdExcludes`, auto memory.

**CAB-specific guidance**:

- **200-line discipline**: Each CLAUDE.md targets ≤200 lines. This aligns with CC's official recommendation and auto memory's 200-line/25KB load limit. Every token of instruction displaces productive output.
- **Seed instruction design**: CC's memory is increasingly autonomous (auto memory, background consolidation via autoDream). Write CLAUDE.md as *seed instructions* that survive consolidation — not exhaustive procedural checklists that get pruned.
- **Auto memory complement**: CC maintains agent-generated memory (`MEMORY.md` + topic files) separate from CLAUDE.md. CAB's `notes/` state management patterns complement this with structured persistent state. See [Memory System](../components/memory-claudemd.md) for detail.

### Runtime Memory Pipeline (Observable Behavior)

Beyond the 4-scope configuration, CC's runtime operates a multi-layer escalation pipeline where each layer prevents the next from firing:

| Layer                   | What Happens                                                     | Cost        |
| ----------------------- | ---------------------------------------------------------------- | ----------- |
| CLAUDE.md + Auto Memory | Loaded at session start                                          | Free        |
| Session Memory          | Summaries every ~5K tokens                                       | Low         |
| MicroCompact            | Local editing of cached tool results (zero API calls)            | Free        |
| AutoCompact             | Structured summary at `effectiveContextWindow - 13,000` tokens | Moderate    |
| Full Compact            | Complete conversation compression (9-section narrative)          | Expensive   |
| Session Reset           | Clears everything except system prompt                           | Destructive |

**Practical implication**: Proactive management (compacting at ~70%, or starting fresh sessions) avoids forced compaction cascades. See [Session Management](../operational-patterns/state-management/session-lifecycle.md) for decision framework.

## Invocation & Extension Patterns

CC extensions compose through distinct invocation and context patterns:

| Component                   | Trigger                    | Context                 | Notes                                          |
| --------------------------- | -------------------------- | ----------------------- | ---------------------------------------------- |
| **CLAUDE.md + Rules** | Automatic (session start)  | Main                    | Always loaded                                  |
| **Skills**            | Model-invoked or `/name` | Main (inline) or forked | Preferred over commands; 13 frontmatter fields |
| **Agents**            | Model/user-invoked         | Separate context        | Isolated; don't inherit parent skills          |
| **Hooks**             | Event-driven (26 events)   | External                | 4 types: command, http, prompt, agent          |
| **MCP Servers**       | Tool calls                 | Deferred schemas        | Connected on start, disconnected on finish     |

> **Official docs**: [Skills](https://code.claude.com/docs/en/skills), [Sub-agents](https://code.claude.com/docs/en/sub-agents), [Hooks](https://code.claude.com/docs/en/hooks), [MCP](https://code.claude.com/docs/en/mcp)

**Key evolution (2026)**: Custom commands merged into skills. Skills are the preferred path — commands still work but skills win when both exist. Plugin projects keep commands at root (`commands/`); standalone projects use `.claude/commands/`. CAB maintains concise abbreviated names for plugin-level commands to preserve quick-trigger usability (e.g., `/cab:execute-task` not `/cc-architecture-builder:execute-task`).

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

| Level        | Content                     | When                  | Token Cost       |
| ------------ | --------------------------- | --------------------- | ---------------- |
| **L0** | CLAUDE.md seed instructions | Session start         | ≤200 lines      |
| **L1** | Skill/agent metadata        | Session start         | ~100 tokens each |
| **L2** | Full skill content          | When triggered        | Variable         |
| **L3** | KB files, bundled resources | On-demand (grep/read) | Variable         |
| **L4** | External docs via MCP/web   | When needed           | External         |

**Design implication**: Keep L0 lean. Reference L2-L4 via @imports and skill invocations rather than embedding content. A CLAUDE.md that tries to load everything upfront wastes the context budget on content that may never be relevant to the current task.

## Skill Composition Model & End-Vision Architecture

The accurate metaphor for a CC skill is **UNIX coreutil + man page + sandbox**, not a Python `src/` module. Three structural reasons:

1. **No in-process imports** — Skills don't import each other's functions. Composition is via **co-activation** (one skill loaded alongside another) or **NL-driven delegation** (orchestrator chooses based on description match), not function-call.
2. **Scripts are CLI subprocesses** — `skills/<name>/scripts/foo.py` runs as a Bash-invoked subprocess when the skill body calls it. Cross-skill code reuse via `import` is impossible at the language level.
3. **State flows via filesystem** — Multiple skills coordinate via files (`notes/`, KB, output artifacts), the same way UNIX programs coordinate via pipes and files.

Each skill is therefore an **autonomous NL-invocable capability** with: NL contract (description, when_to_use, allowed-tools), deterministic logic (`scripts/`), tailored knowledge (`references/`), and optional verification block (machine-readable proof-of-correctness). Composition semantics are **file-based**, not function-call — a feature, not a limit, because it maps directly onto the agentic OS platform vision (operating systems compose autonomous programs via syscalls, files, and pipes).

### End-Vision: Skills-as-Modular-Software with KG as Systematization Map

The mature CAB target architecture treats skills as the modular software layer of an agentic OS platform. Each domain-specialized skill becomes a "live, walking, iterative KB pack" combining:

- NL instruction body (the equivalent of a module's interface contract)
- Orchestration scripts (`scripts/`)
- Utility scripts (the equivalent of `src/` deterministic logic)
- Tailored KB cards (`references/`, programmatically curated)

The Knowledge Graph (KG) is the platform's **service mesh + package registry**:

| KG Function | Solves |
|---|---|
| Maps WHICH KB cards belong in WHICH skill's `references/` | Stranded-doc problem (cards without skill home) |
| Maps WHICH skills compose into WHICH agent (`governs` / `embodies` edges) | Agent composition is queryable, not hand-coded |
| Tracks bi-temporal supersession via git commit hash | Skill-version evolution traceable; old patterns don't silently rot |
| Powers stranded-doc + skill-drift detection | KB audit becomes data-driven |
| Surfaces missing-card gaps | New framing's required content is enumerable |

Under this framing, KB content matures from "static documentation" into "skills-as-modular-software": the agentic OS platform converges on **skill = capability with bundled deterministic logic + tailored knowledge + NL contract + optional verification**.

### Operational Caveats

These constraints shape audit + repacking phases (Wave 8 onward):

1. **Distinguish operational skills from domain skills.** Skills like `close-session`, `recover-session`, `commit-push-pr` are pure procedures — they don't need a `references/` folder. The 5-axis audit framework classifies skills, not just KB cards.
2. **Preserve `source:` provenance during KB → skill `references/` repacking.** When a card moves into a skill, its source URL and last-fetch metadata travel with it.
3. **Minimum-viable-skill threshold** prevents proliferation: a skill earns its slot if (a) it has multi-step orchestration OR deterministic scripts, AND (b) it has reusable domain knowledge OR a verification contract. Single-step "ask the LLM nicely" tasks do not justify a skill.
4. **Cross-skill knowledge duplication policy**: foundational shared content stays in `knowledge/`; skill-specialized derivations go in skill `references/`. The KG tracks both edge types.
5. **Discoverability ↔ modularity tension**: smaller skills = better progressive disclosure but worse description-based dispatch (more competition); larger skills = simpler dispatch but bigger context loads. Each skill's frontmatter description should follow the imperative trigger pattern (when X / DO NOT Y / use Z) to mitigate.
6. **End-vision is multi-wave, not v1.** Wave 8 builds the systematization layer (KG + audit + content quality verdict). Waves 9-11 progressively repack KB content into skill packs. Mature state is iterative.

For session-anchor brain-dump and Wave 8-11 cold-start context: `notes/end-vision-cab-2026-04-28.md`.

## Key Implications

1. **Link, don't duplicate** — Official CC docs are the source of truth for CC-native features
2. **Design for discovery** — Claude must know what exists (L1 metadata) before retrieving detail (L2-L3)
3. **Atomic files** — Single topic, self-contained, independently retrievable by agents
4. **Test invocation** — Verify skills/agents trigger on expected inputs after any schema change
5. **Modular rules** — Use `.claude/rules/` with `paths:` frontmatter for project-specific scoping
6. **Seed over procedure** — CLAUDE.md instructions should be durable guidance, not brittle step-by-step recipes
7. **Skills compose via files, not imports** — Design for filesystem-mediated state handoff, not in-process function calls (see Skill Composition Model above)

## See Also

- [Design Principles](design-principles.md) — Core tenets governing the CAB framework
- [Memory System](../components/memory-claudemd.md) — Detailed memory patterns + auto memory
- [Session Management](../operational-patterns/state-management/session-lifecycle.md) — Context health, compaction, persistence
- [Orchestration Framework](../operational-patterns/orchestration/framework.md) — Canonical workflow patterns
