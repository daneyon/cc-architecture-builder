---
id: orchestration-framework
title: Orchestration Framework
category: operational-patterns/orchestration
tags: [orchestration, workflows, agents, patterns, verification, tenets]
summary: Core orchestration tenets, canonical agentic workflow patterns, and the standard task execution protocol.
depends_on: [subagents, collaboration-patterns, memory-claudemd]
related: [delegation-templates, cost-model, session-lifecycle]
complexity: advanced
last_updated: 2026-04-05
estimated_tokens: 2200
source: https://code.claude.com/docs/en/sub-agents
confidence: A
review_by: 2026-07-05
revision_note: "v3.0 — Split from monolithic orchestration-framework.md. Tenets + patterns + execution protocol. Delegation and cost model extracted to sibling files."
---

# Orchestration Framework

## Purpose

Defines how CC extensions (skills, agents, hooks) coordinate for complex, multi-step tasks. Establishes canonical workflow patterns, execution protocols, and the tenets that govern all agentic work within CAB.

> **Official docs**: [Sub-agents](https://code.claude.com/docs/en/sub-agents), [Agent Teams](https://code.claude.com/docs/en/agent-teams), [Skills](https://code.claude.com/docs/en/skills) — for CC-native mechanics. This document provides CAB's operational patterns built on top of those primitives.

---

## Core Design Tenets

### Tenet 1: Simplicity-First Complexity Ladder

Start with the simplest solution that works. Escalate only when measured improvement justifies added complexity.

```
Level 0 │ Single optimized prompt            │ Most problems start here
Level 1 │ Single agent + skills              │ Procedural augmentation
Level 2 │ Sequential subagent chains         │ Clear dependencies, context isolation
Level 3 │ Parallel subagents / git worktrees │ Independent simultaneous tasks
Level 4 │ Agent Teams (coordinator mode)     │ Inter-agent communication needed
Level 5 │ Full orchestrator + state mgmt     │ Multi-phase project lifecycle
```

Rule: Validate that Level N is insufficient before moving to Level N+1.

### Tenet 2: Verification as Architectural Requirement

Every agent, task, and phase gate requires a verification method. An agent without a verification section is architecturally incomplete. See [Design Principles P7](../../overview/design-principles.md).

### Tenet 3: Plan Before Execute

Complex tasks follow the Standard Task Execution Protocol (below). If execution goes sideways, stop and re-plan — never push forward on a broken implementation.

### Tenet 4: Compounding Knowledge via CLAUDE.md

CLAUDE.md is a living feedback loop: every correctable error becomes a permanent learning. Over time, the error rate measurably drops. For teams, use `@.claude` in PR reviews to add learnings as part of the PR itself.

### Tenet 5: Token Efficiency as Public Good

Context window space is shared across rules, skills, agent instructions, and actual work. Design for progressive disclosure: load only what the current task requires. See [Context Engineering](../state-management/context-engineering.md).

### Tenet 6: Autonomous Multi-Agent Operation

The global config acts as the orchestrator layer: it receives tasks, classifies them, routes to domain-specialist agents, synthesizes results, and manages cross-project state. `"agent": "orchestrator"` in `~/.claude/settings.json` establishes this as default.

```
Global Orchestrator (~/.claude/)
├── Receives task from user
├── Classifies: domain, complexity, scope
├── Routes to specialist agent (project plugin)
│   ├── Project Agent A (domain specialist)
│   ├── Project Agent B (domain specialist)
│   └── Verifier Agent (QA/QC)
├── Synthesizes results
├── Updates state (progress, learned corrections)
└── Reports to user (only if escalation needed)
```

### Important: Probabilistic Nature

Context engineering increases the *probability* of desired outcomes — it does not guarantee them. This is precisely why verification is an architectural requirement, not an optional nicety.

---

## Canonical Agentic Workflow Patterns

Five foundational patterns for agentic systems. Apply in order of increasing complexity (per Tenet 1).

### Pattern 1: Prompt Chaining

Sequential LLM calls where output of step N feeds step N+1, with gate checks between.

```
[Prompt A] → Gate Check → [Prompt B] → Gate Check → [Prompt C]
```

**CC Implementation**: Main session executes skill A → skill B → skill C. Gate checks are bash commands (lint, test, typecheck) or human approval.

**When**: Tasks decomposable into fixed sequential steps where each step can be validated.

### Pattern 2: Routing

Classify incoming request and direct to the appropriate specialized handler.

**CC Implementation**: Main session acts as router. Agent `description` fields provide semantic matching — well-written descriptions enable automatic routing without explicit classification logic.

**When**: Requests fall into distinct categories requiring different expertise, tools, or context.

### Pattern 3: Parallelization

Two sub-patterns:

- **Sectioning** — Independent subtasks across parallel workers (worktrees or subagents)
- **Voting** — Same task with different approaches, then synthesize best answer

**CC Implementation**: Worktrees for sectioning (3-5 parallel sessions). Subagents with "use N subagents" prompt for voting/parallel exploration within a single session.

**When**: Tasks decomposable into independent subtasks (sectioning) or benefit from diverse perspectives (voting).

### Pattern 4: Orchestrator-Workers

Central orchestrator dynamically decomposes, delegates to specialists, synthesizes results.

**CC Implementation**: Orchestrator agent reads state, determines phase, delegates via Agent tool to specialists. Each specialist has focused tools and skills. Results flow back for synthesis.

**When**: Tasks too complex for single agent but with dynamically identifiable subtasks. Primary pattern for product lifecycle.

### Pattern 5: Evaluator-Optimizer

Generator produces output, evaluator assesses against criteria, generator iterates.

**CC Implementation**: Implementer agent generates code → code-reviewer evaluates → loop until pass or max iterations.

**When**: Output quality requires iterative refinement against measurable criteria.

### Pattern Selection Guide

| Signal | Pattern |
|--------|---------|
| Fixed sequential steps with validation gates | Prompt Chaining |
| Distinct request types needing different handlers | Routing |
| Independent subtasks, no inter-task communication | Parallelization |
| Complex task needing dynamic decomposition | Orchestrator-Workers |
| Quality-critical output needing iterative refinement | Evaluator-Optimizer |

Combinations are common: an orchestrator may use prompt chaining within a worker, parallelization across workers, and evaluator-optimizer for quality-critical deliverables.

---

## Standard Task Execution Protocol

Every non-trivial task follows this cycle:

```
1. PLAN ──▶ 2. REVIEW ──▶ 3. EXECUTE ──▶ 4. VERIFY ──▶ 5. COMMIT
   ▲                                         │
   │              SIDEWAYS?                   │
   └──────── STOP & RE-PLAN ◀────────────────┘
```

### Step 1: PLAN
Enter plan mode (Shift+Tab twice). Describe objective and constraints. Iterate until solid. Advanced: have a second session or subagent review the plan "as a staff engineer."

### Step 2: REVIEW
Human reviews the plan. Check for scope creep, missing edge cases, incorrect assumptions. For automated workflows, a gate-check agent can perform this role.

### Step 3: EXECUTE
Switch to auto-accept mode. Claude implements from the approved plan faithfully.

### Step 4: VERIFY
Run domain-appropriate verification:

| Domain | Method |
|--------|--------|
| Code | Test suite, lint, typecheck, diff |
| Documentation | Link validation, format check |
| Architecture | Diagram generation, constraint check |
| Configuration | Dry-run, plan mode review |
| Any | "Prove to me this works" challenge |

If verification fails → iterate (small) or return to PLAN (fundamental).

### Step 5: COMMIT
Git commit with descriptive message. Update state: `notes/progress.md`, `notes/current-task.md`, or `project-state.yaml`. Always commit working state before ending a session.

### Failure Recovery

1. **Stop immediately** — do not push forward on a broken path
2. **Switch to plan mode** — re-assess with what you now know
3. **Include verification in revised plan** — explicitly plan how to confirm each step
4. **Consider**: "Knowing everything you know now, scrap this and implement the elegant solution"

---

## Agent Failure Mode Catalog

| Failure | Symptom | Mitigation |
|---------|---------|------------|
| **One-Shotting** | Attempts entire project in one context, runs out | Decompose into feature list with boolean pass/fail tracking |
| **Premature Completion** | Declares "Done!" with incomplete work | Comprehensive checklist + actual verification (not verbal assertions) |
| **Broken State Handoff** | Unfinished state between sessions | Mandatory commit + progress file update before session end |
| **Testing Skip** | Marks features done without running tests | Verification as separate explicit step, not part of implementation |
| **Scope Drift** | Wanders into unrelated improvements | Explicit boundaries in delegation prompts; log out-of-scope discoveries |

---

## CC Platform Constraints

| Constraint | Workaround |
|-----------|------------|
| Single subagent nesting depth | Main session routes; Agent Teams for multi-session |
| No native database | YAML/JSON state files; MCP for external DBs |
| No native vector search | Structured INDEX.md catalogs; MCP at scale |
| No self-scheduling | Human triggers via commands; hooks for event-driven automation |
| Context window finite | Subagents for isolation; `/compact` or fresh sessions |
| Agent Teams experimental | Higher cost (~7x); use worktrees for most parallel work |

## See Also

- [Delegation Templates](delegation-templates.md) — Delegation structure, phase-agent routing
- [Cost Model](cost-model.md) — Token economics, optimization levers
- [Collaboration Patterns](../multi-agent/collaboration-patterns.md) — Multi-agent coordination
- [Session Lifecycle](../state-management/session-lifecycle.md) — Context health, persistence
