---
id: design-principles
title: CAB Design Principles
category: overview
tags: [philosophy, context-engineering, wrapping, orchestration, knowledge-base, principles]
summary: Core design principles governing the CAB framework — context engineering, the wrapping/composition architecture, standardized knowledge bases for domain specialization, orchestration + state management, and the human-AI collaboration model.
depends_on: [executive-summary, architecture-philosophy]
related: [orchestration-framework, memory-claudemd, agent-skills, subagents]
complexity: foundational
last_updated: 2026-03-26
estimated_tokens: 1200
---

## Principle 1: Context Engineering Is the Foundation

The quality of AI output is determined entirely by the quality of context provided.
Context engineering is the discipline of curating what the model sees — not just
what you ask it, but the entire information environment it operates in.

**Core insight**: Context windows are constrained not by raw token capacity but by
attention mechanics. As context grows, models exhibit predictable degradation —
"lost-in-the-middle" phenomenon, U-shaped attention curves, attention scarcity.

**Implications for design**:

- Every token of configuration displaces productive output. Context is a shared,
  finite resource — treat it as a public good.
- Progressive disclosure: load only what the current task requires. Use @imports,
  skill lazy-loading, and filesystem-based references for everything else.
- Keep high-priority information at the start and end of context, not buried in
  the middle.
- The filesystem is a persistent context layer — offload plans, progress, and
  large outputs to files. They survive compaction and session boundaries.
- Proactively manage context health: continue, compact, or start fresh based on
  signal quality, not just fullness percentage.

**Sources**: Koylan (context fundamentals, degradation patterns), Watts (value-dense
context), Fowler/Böckeler (context engineering taxonomy), Anthropic (effective
context engineering for AI agents).

---

## Principle 2: The Wrapping/Composition Architecture

Extensions compose upward through four runtime layers. Each layer wraps the layer
below it, creating a progressively richer execution environment:

```
LAYER 1: PERSISTENT MEMORY (always loaded)
    CLAUDE.md + rules/*.md
    = WHO you are, HOW you always behave

LAYER 2: EXTENSION REGISTRY (metadata only, ~100 tokens each)
    Skills, Agents, Commands, MCP tool signatures
    = WHAT capabilities exist (catalog, not content)

LAYER 3: INVOCATION (on-demand)
    Skill → loads INTO main context
    Agent → SPAWNS separate context
    Command → executes in main context
    = ACTIVATING capabilities when needed

LAYER 4: EXECUTION (runtime)
    Main Context + Agent Subprocesses + MCP Servers
    = WHERE work happens
```

**The wrapping principle**: Extensions interconnect through deliberate composition.
Rules inform skills. Skills get loaded into agents. Agents get orchestrated by the
orchestrator or commands. MCP provides external data/tools accessible from any layer.
Knowledge base is the reference library that any extension can read on-demand.

**Implications**:

- Design each extension to work independently, but compose well with others.
- Skills are the orchestrator's "how-to" library — agents are its "delegation roster."
- An agent loading a skill is fundamentally different from the orchestrator loading
  the same skill: the agent gets an isolated copy in its own context window.
- Commands are the human's interface to trigger workflows; the orchestrator's
  interface is the agent description field.
- When a skill involves repeatable logic, extract it into executable scripts
  (`skills/[name]/scripts/`) that the skill invokes via Bash. This prevents
  the LLM from regenerating deterministic logic each invocation — a direct
  token efficiency measure and a reliability mechanism (tested code > generated
  code). The skill SKILL.md becomes the orchestration wrapper; the script is
  the pre-programmed execution.

---

## Principle 3: Standardized Knowledge Base for Domain Specialization

The knowledge base is the foundational layer for domain specialization. A well-
structured KB enables the framework to be holistically generalized at its core
while becoming deeply specialized through the knowledge it references.

**KB standardization principles**:

- Every file is atomic: single topic, self-contained, independently retrievable
- Every file has YAML frontmatter: id, title, tags, summary, depends_on, related
- Every directory has an INDEX.md catalog
- Naming: kebab-case.md throughout
- Scaling strategy: <20 files flat, 20-100 category dirs, 100+ MCP semantic search

**Domain specialization pattern**: The base architecture (memory + extensions +
knowledge) stays identical across all projects. What changes is the knowledge
content, agent personas, and skill procedures. The architecture is the operating
system; the domain is the application.

**Efficient RAG**: Prioritize giving agents sufficient context to understand and
operate effectively over aggressive token minimization. A lean but insufficient
context produces worse outcomes than a slightly heavier but adequate one. Balance,
not minimalism, is the goal.

---

## Principle 4: Orchestration + State Management as Core Competency

The orchestrator pattern is the primary operating model: one main agent classifies,
routes, and synthesizes; specialist agents execute scoped tasks.

**Standard task execution protocol**: PLAN → REVIEW → EXECUTE → VERIFY → COMMIT.
This is not bureaucracy — it's the mechanism that prevents the most common agent
failure modes (one-shotting, premature completion, broken state handoff, skipped
tests, scope drift).

**State management**: Context is ephemeral; the filesystem is persistent. Cross-
session state lives in:

- `CLAUDE.md` Learned Corrections (compounding knowledge)
- `notes/progress.md` (multi-session task tracking)
- `notes/current-task.md` (active task plan)
- Git commits (permanent checkpoints)

**Compounding knowledge**: Every correctable error becomes a permanent learning in
CLAUDE.md. Over time, the error rate measurably drops. This is the primary mechanism
by which the system improves without retraining.

---

## Principle 5: Holistically Generalized, Flexibly Adaptive

Extensions should be as general as possible — designed to adapt to any specific
context rather than hard-coding domain assumptions.

**What this means in practice**:

- Global config extensions work across ALL projects (universal strategies, coding
  practices, communication patterns)
- Project plugin extensions specialize for a specific domain (engineering standards,
  domain knowledge, domain-specific agents)
- Reference frameworks (product-design-cycle, a-team-database) are conceptual menus,
  not mandatory checklists — the orchestrator adapts them to actual project scale
  and context
- Avoid overbuilding: if the model handles something well natively, don't build
  an extension for it. The three-question test: (1) Does a real user need demand
  this? (2) Can the model handle it natively? (3) Would hard-coding create rigidity?

---

## Principle 6: Multi-Agent Autonomy with Human Oversight

The end-product objective is a multi-agent system that operates autonomously to the
fullest extent possible — with human involvement limited to strategic direction,
periodic KB alignment with platform upgrades, and review of verification reports.

**Human oversight touchpoints**:

- Strategic direction (what to build, why, priorities)
- Knowledge base maintenance (ensuring domain content is current)
- Verification report review (final quality gate)
- Escalation handling (when agents flag uncertainty)

**Agent autonomy boundaries**: Agents can read, analyze, plan, implement, test,
and commit within pre-approved permission boundaries. They cannot make irreversible
changes without verification passing, deploy to production without human approval,
or modify security-sensitive configurations autonomously.

**Probabilistic acknowledgment**: Context engineering increases the *probability* of
desired outcomes — it does not guarantee them. This is precisely why verification is
an architectural requirement, not an optional nicety.

---

## Principle 7: Verification as Architectural Requirement

Every agent, every task, every phase gate requires a verification method. Providing
the model a way to verify its own work improves output quality by 2-3x.

Verification is not QA bolted on at the end — it is a structural element of every
agent definition, every task plan, and every phase transition. An agent without a
verification section is architecturally incomplete.

---

## Principle 8: Don't Reinvent the Wheel

Before building any extension, check whether an existing package, plugin, MCP server,
or built-in capability already handles it. Design hybrids from proven references
rather than building from scratch. Wrap existing tools via MCP rather than rebuilding
their logic.

**Practical application**: Install and evaluate marketplace plugins before writing
custom equivalents. Reference official documentation via skills (e.g., claude-docs-
helper) rather than duplicating it in knowledge packs. Use established frameworks
(Mermaid for diagrams, pytest for testing, ruff for linting) rather than custom
solutions.

---

## Principle 9: High Agency Problem Solving

The human operator and the AI system share a high agency mindset: clear thinking,
bias to action, and willingness to challenge assumptions.

**For the AI**: Challenge flawed premises directly. Surface contradictions immediately.
Provide honest assessments even when critical. Don't wait for permission to identify
problems.

**For the human**: Define the problem clearly. Provide sufficient context. Review and
iterate — don't expect perfection on first pass. Invest in the KB as compounding
infrastructure, not throwaway prompts.

**For the system**: If it doesn't defy the laws of physics, it's a solvable problem.
Start with the simplest solution. Escalate complexity only when measured improvement
justifies it. Stop and re-plan when execution goes sideways — never push forward on
a broken implementation.

---

## How These Principles Relate

```
Context Engineering (P1)
    └── governs HOW MUCH context each extension receives

Wrapping Architecture (P2)
    └── governs HOW extensions compose at runtime

Knowledge Base Standardization (P3)
    └── governs HOW domain specialization is structured

Orchestration + State (P4)
    └── governs HOW tasks are executed and state persists

Generalized + Adaptive (P5)
    └── governs WHAT SCOPE extensions are designed for

Multi-Agent Autonomy (P6)
    └── governs WHO (human vs. agent) does what

Verification (P7)
    └── governs HOW QUALITY is confirmed

Don't Reinvent (P8)
    └── governs WHEN to build vs. reuse

High Agency (P9)
    └── governs the MINDSET of both human and AI operators
```

## See Also

- [Architecture Philosophy](architecture-philosophy.md) — CC runtime mechanics (memory, invocation, distribution)
- [Orchestration Framework](../operational-patterns/orchestration-framework.md) — Tenets, canonical patterns, execution protocol
- [Session Management](../operational-patterns/session-management.md) — Context health, filesystem-as-context
