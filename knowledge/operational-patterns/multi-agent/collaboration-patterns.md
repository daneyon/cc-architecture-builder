---
id: collaboration-patterns
title: Multi-Agent Collaboration Patterns
category: operational-patterns/multi-agent
tags: [agents, collaboration, orchestration, multi-agent, subagents, worktrees]
summary: Four coordination patterns for multiple Claude agents — from worktrees (daily driver) through Agent Teams (experimental), with effort scaling heuristics and cross-session persistence.
depends_on: [subagents, orchestration-framework]
related: [agent-teams, worktree-workflows, session-lifecycle]
complexity: advanced
last_updated: 2026-04-05
estimated_tokens: 900
source: https://code.claude.com/docs/en/sub-agents
confidence: A
review_by: 2026-07-05
revision_note: "v3.0 — Split from multi-agent-collaboration.md. Patterns overview + effort scaling. Agent Teams deep-dive extracted to agent-teams.md."
---

# Multi-Agent Collaboration Patterns

## Overview

Complex tasks benefit from multiple specialized agents. CC supports four coordination mechanisms, ordered from most practical to most advanced.

> **Official docs**: [Sub-agents](https://code.claude.com/docs/en/sub-agents), [Agent Teams](https://code.claude.com/docs/en/agent-teams) — for CC-native mechanics.

---

## Pattern 1: Parallel via Git Worktrees (Daily Driver)

Each worktree is an isolated git checkout with its own CC session and context window.

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Worktree 1   │  │ Worktree 2   │  │ Worktree 3   │
│ Feature: Auth│  │ Feature: API │  │ Analysis     │
│ Own Session  │  │ Own Session  │  │ Own Session  │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       └─────────────────┼─────────────────┘
                         ▼
               Shared Git Repository
```

**Use when**: Tasks can run independently. Default for most parallel work.
**Sweet spot**: 3-5 worktrees. Separate token budgets per session.

See [Worktree Workflows](worktree-workflows.md) for setup and patterns.

## Pattern 2: Sequential Subagent Chain

Subagents within a single session, executed sequentially with explicit context passing.

```
Main Agent
    ├──▶ Subagent A (analyze) → results
    ├──▶ Subagent B (implement, using A's results) → results
    └──▶ Subagent C (review B's implementation) → final
```

**Use when**: Tasks have clear sequential dependencies and benefit from context isolation between steps.

**Prompt pattern**: "Use the analyzer agent to find issues in src/auth/, then the implementer to fix them, then the reviewer to verify."

## Pattern 3: Main Agent + Specialists

Main session orchestrates, delegating to specialist agents by task type.

```
┌─────────────────────────────────────────┐
│              Main Agent                  │
│     (orchestrates, synthesizes)          │
└───────────┬──────────┬──────────┬───────┘
            ▼          ▼          ▼
        ┌───────┐  ┌───────┐  ┌───────┐
        │Domain │  │Code   │  │Data   │
        │Expert │  │Review │  │Analyst│
        └───────┘  └───────┘  └───────┘
```

**Use when**: Single problem needs diverse expertise. Each specialist has focused tools and skills.

## Pattern 4: Agent Teams (Experimental)

Multi-session coordination with shared task lists and inter-agent messaging.

**Use when**: Tasks genuinely require inter-agent communication — competing hypotheses, cross-layer coordination, shared intermediate findings.

**Cost**: Significantly higher token cost per teammate (token usage scales linearly with active teammates; ~7x is a CAB estimate, not an official figure). Use worktrees (Pattern 1) unless you specifically need the shared task list and mailbox capabilities.

See [Agent Teams](agent-teams.md) for full deep-dive.

---

## Pattern Selection Quick Reference

| Situation | Pattern | Cost Profile |
|-----------|---------|-------------|
| Independent parallel tasks | Worktrees (1) | Separate session budgets |
| Sequential dependent tasks | Subagent chain (2) | Additive in main context |
| Single problem, multiple perspectives | Main + specialists (3) | Main + isolated agent contexts |
| Inter-agent communication needed | Agent Teams (4) | Significantly higher (linear scaling; ~7x is CAB estimate) |

---

## Effort Scaling Heuristic

Match agent count to task complexity:

| Complexity | Configuration | Example |
|-----------|---------------|---------|
| Simple fact-finding | 1 agent, 3-10 tool calls | "What's the error in this function?" |
| Direct comparison | 2-4 subagents, 10-15 calls each | "Compare auth approaches" |
| Comprehensive research | 5-10+ subagents, clear division | "Audit codebase for security" |
| Multi-phase lifecycle | Orchestrator + state management | Full product development |

**Subagent triggering**: Append "use subagents" or "use N subagents" to any prompt to throw more compute at the problem. Offloads work and keeps main context clean.

---

## Cross-Session Persistence

Three approaches scaled to project complexity:

| Approach | Mechanism | Best For |
|----------|-----------|----------|
| **Lightweight** | `notes/` directory, updated per PR/session | Single-developer feature work |
| **Medium** | Progress file + `features.json` (boolean pass/fail) | Long-running autonomous tasks |
| **Full** | `project-state.yaml` + orchestrator lifecycle | Multi-phase product development |

See [Filesystem Patterns](../state-management/filesystem-patterns.md) for design details.

## Coordination via Git

Git is the universal coordination layer: commits checkpoint work, branches isolate parallel efforts, PRs review cross-agent output, merges integrate findings.

## See Also

- [Agent Teams](agent-teams.md) — Deep-dive on experimental multi-session coordination
- [Worktree Workflows](worktree-workflows.md) — Setup, patterns, best practices
- [Orchestration Framework](../orchestration/framework.md) — Canonical patterns, tenets
- [Cost Model](../orchestration/cost-model.md) — Token economics for agent decisions
