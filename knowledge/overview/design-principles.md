---
id: design-principles
title: CAB Design Principles
category: overview
tags: [philosophy, context-engineering, wrapping, orchestration, knowledge-base, principles]
summary: Core design principles governing CAB — context engineering, wrapping/composition architecture, standardized knowledge bases, orchestration + state management, and the human-AI collaboration model.
depends_on: [executive-summary, architecture-philosophy]
related: [orchestration-framework, memory-claudemd, agent-skills, subagents]
complexity: foundational
last_updated: 2026-04-05
estimated_tokens: 1400
source: CAB-original
confidence: A
review_by: 2026-07-05
---

# CAB Design Principles

## Principle 1: Context Engineering Is the Foundation

The quality of AI output is determined by the quality of context provided. Context engineering is the discipline of curating what the model sees — the entire information environment, not just the prompt.

**Core constraints**:

- Context windows are limited not by raw token capacity but by attention mechanics. As context grows, models exhibit predictable degradation — lost-in-the-middle phenomenon, U-shaped attention curves.
- Every token of configuration displaces productive output. Context is a shared, finite resource.
- **200-line discipline**: CLAUDE.md targets ≤200 lines. This is CC's official recommendation and the auto memory load limit. Exceeding it risks truncation and context waste.

**Design implications**:

- Progressive disclosure: load only what the current task requires. Use @imports, skill lazy-loading, and filesystem references for everything else.
- High-priority information at the start and end of context, not buried in the middle.
- The filesystem is a persistent context layer — `notes/`, progress files, and KB docs survive compaction and session boundaries.
- Auto memory (`MEMORY.md` + topic files) is CC's native persistent context. CAB's `notes/` patterns complement it with structured operational state.
- Prompt cache awareness: stable content at context start enables cache hits (~$0.003 vs ~$0.60 at 200K tokens). Avoid cache-breaking changes to system prompt structure.
- Proactively manage context health: compact at ~70%, start fresh when context is poisoned, not just when auto-compact forces it.

---

## Principle 2: The Wrapping/Composition Architecture

Extensions compose upward through four runtime layers:

```
LAYER 1: PERSISTENT MEMORY (always loaded)
    CLAUDE.md + rules/*.md + Auto Memory (MEMORY.md)
    = WHO you are, HOW you always behave

LAYER 2: EXTENSION REGISTRY (metadata only, ~100 tokens each)
    Skills, Agents, MCP tool signatures
    = WHAT capabilities exist (catalog, not content)

LAYER 3: INVOCATION (on-demand)
    Skill → loads INTO main context (inline or fork)
    Agent → SPAWNS separate context
    Hook → executes EXTERNALLY on events
    = ACTIVATING capabilities when needed

LAYER 4: EXECUTION (runtime)
    Main Context + Agent Subprocesses + MCP Servers
    = WHERE work happens
```

**The wrapping principle**: Extensions interconnect through deliberate composition. Rules inform skills. Skills get loaded into agents. Agents get orchestrated by the orchestrator. MCP provides external data/tools accessible from any layer. Knowledge base is the reference library any extension reads on-demand.

**Key implications**:

- Skills are the orchestrator's "how-to" library — agents are its "delegation roster."
- An agent loading a skill gets an isolated copy in its own context window.
- **Commands are now skills**: CC merged commands into skills (2026). Skills are preferred; commands still work but skills win when both exist. CAB maintains concise abbreviated names (e.g., `cab:execute-task`) for quick-trigger usability.
- When a skill involves repeatable logic, extract it into executable scripts (`skills/[name]/scripts/` for plugins, `.claude/skills/[name]/scripts/` for standalone) that the skill invokes via Bash. Tested code > generated code.

---

## Principle 3: Standardized Knowledge Base for Domain Specialization

The knowledge base is the foundational layer for domain specialization. A well-structured KB enables the framework to be generalized at its core while becoming deeply specialized through the knowledge it references.

**KB standardization**:

- Every file is atomic: single topic, self-contained, independently retrievable
- Every file has YAML frontmatter: id, title, tags, summary, depends_on, related
- **Confidence tier** (`confidence:` field): `A` (official CC docs), `B` (observable behavior), `C` (inferred/volatile)
- **Freshness tracking** (`review_by:` field): Tier A = 90 days, Tier B = 90 days, Tier C = 60 days
- Every directory has an INDEX.md catalog
- Naming: kebab-case.md throughout
- Scaling: <20 files flat, 20-100 category dirs, 100+ consider MCP semantic search

**Link-not-duplicate principle**: KB files covering CC-native features include a `source:` URL pointing to official docs and provide only CAB-specific operational extensions. If official docs cover a topic adequately, CAB provides a brief pointer — not a restatement. This keeps KB content concise, reduces maintenance burden, and avoids epistemic contamination from mixing verified and unverified content.

**Domain specialization pattern**: The base architecture (memory + extensions + knowledge) stays identical across all projects. What changes is the knowledge content, agent personas, and skill procedures. CAB is the operating system; the domain is the application.

---

## Principle 4: Orchestration + State Management as Core Competency

The orchestrator pattern is the primary operating model: one main agent classifies, routes, and synthesizes; specialist agents execute scoped tasks.

**Standard task execution protocol**: PLAN → REVIEW → EXECUTE → VERIFY → COMMIT. This prevents the most common agent failure modes (one-shotting, premature completion, broken state handoff, skipped tests, scope drift).

**State management hierarchy**:

1. `CLAUDE.md` Learned Corrections — compounding knowledge that improves over time
2. `notes/progress.md` — multi-session task tracking and bootstrap context
3. `notes/current-task.md` — active task plan (cold-start anchor)
4. Git commits — permanent, verifiable checkpoints

**Enhanced patterns**:

- **Agent Teams** (experimental): Multi-session coordination with shared task list and mailbox-based IPC. Higher cost (~7x tokens) but enables inter-agent communication.
- **Hook-driven QA/QC**: Use hooks for recurring validations (e.g., auto-validate on extension updates, lint on file writes, freshness checks on version bumps).
- Auto memory complements `notes/` — CC manages short-term memory; CAB manages structured operational state.

See [Orchestration Framework](../operational-patterns/orchestration/framework.md) for full detail.

---

## Principle 5: Holistically Generalized, Readily Actionable

Extensions should be as general as possible while remaining **programmatically actionable** — designed to produce concrete, executable outcomes rather than abstract guidance.

**What this means in practice**:

- Global config extensions work across ALL projects (universal strategies, practices, communication patterns)
- Project plugin extensions specialize for a specific domain (engineering standards, domain knowledge, domain-specific agents)
- Reference frameworks (product-design-cycle, a-team-database) are conceptual menus — the orchestrator adapts them to project scale and context
- CAB extensions are not documentation — they are operational tools. Each skill, agent, and command should be directly invocable with measurable outcomes.
- The three-question test: (1) Does a real user need demand this? (2) Can the model handle it natively? (3) Would hard-coding create rigidity?

---

## Principle 6: Multi-Agent Autonomy with Human Oversight

The end-product objective is a multi-agent system that operates autonomously to the fullest extent possible — with human involvement limited to strategic direction, periodic KB alignment with platform upgrades, and review of verification reports.

**Human oversight touchpoints**:

- Strategic direction (what to build, why, priorities)
- Knowledge base maintenance (ensuring domain content is current)
- Verification report review (final quality gate)
- Escalation handling (when agents flag uncertainty)

**Agent autonomy boundaries**: Agents can read, analyze, plan, implement, test, and commit within pre-approved permission boundaries. They cannot make irreversible changes without verification, deploy to production without human approval, or modify security-sensitive configurations autonomously.

**Probabilistic acknowledgment**: Context engineering increases the *probability* of desired outcomes — it does not guarantee them. This is precisely why verification is an architectural requirement, not an optional nicety.

---

## Principle 7: Verification as Architectural Requirement

Every agent, every task, every phase gate requires a verification method. Providing the model a way to verify its own work improves output quality significantly.

Verification is not QA bolted on at the end — it is a structural element of every agent definition, every task plan, and every phase transition. An agent without a verification section is architecturally incomplete.

---

## Principle 8: Don't Reinvent — Wrap and Extend

Before building any extension, check whether an existing package, plugin, MCP server, or built-in capability handles it. Design hybrids from proven references rather than building from scratch. Wrap existing tools via MCP rather than rebuilding their logic.

**The CAB-specific application**: CAB itself follows this principle by wrapping CC's official capabilities rather than duplicating them. KB files link to official docs. Skills wrap CC primitives into standardized workflows. Agents compose CC's native subagent system with domain expertise. The entire framework is an extension layer, not a replacement.

---

## Principle 9: High Agency Problem Solving

The human operator and the AI system share a high agency mindset: clear thinking, bias to action, willingness to challenge assumptions.

**For the AI**: Challenge flawed premises directly. Surface contradictions immediately. Provide honest assessments even when critical.

**For the human**: Define the problem clearly. Provide sufficient context. Review and iterate. Invest in the KB as compounding infrastructure, not throwaway prompts.

**For the system**: Start with the simplest solution. Escalate complexity only when measured improvement justifies it. Stop and re-plan when execution goes sideways.

---

## How These Principles Relate

```
Context Engineering (P1)
    └── governs HOW MUCH context each extension receives

Wrapping Architecture (P2)
    └── governs HOW extensions compose at runtime

Knowledge Base (P3)
    └── governs HOW domain specialization is structured

Orchestration + State (P4)
    └── governs HOW tasks execute and state persists

Generalized + Actionable (P5)
    └── governs WHAT SCOPE extensions are designed for

Multi-Agent Autonomy (P6)
    └── governs WHO (human vs. agent) does what

Verification (P7)
    └── governs HOW QUALITY is confirmed

Wrap & Extend (P8)
    └── governs WHEN to build vs. reuse

High Agency (P9)
    └── governs the MINDSET of both operators
```

## See Also

- [Architecture Philosophy](architecture-philosophy.md) — CC runtime mechanics, memory, invocation
- [Orchestration Framework](../operational-patterns/orchestration/framework.md) — Tenets, canonical patterns, execution protocol
- [Session Management](../operational-patterns/state-management/session-lifecycle.md) — Context health, filesystem-as-context
