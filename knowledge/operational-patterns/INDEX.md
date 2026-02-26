---
type: index
scope: operational-patterns
file_count: 4
last_updated: 2026-02-25
version: 0.6.0
changelog: "v0.6.0 — Added orchestration-framework.md, revised multi-agent-collaboration.md to v2.0"
---

# Operational Patterns Index

> Advanced workflow patterns for maximizing Claude Code efficiency.

## Quick Reference

| Pattern | Purpose | Complexity |
|---------|---------|------------|
| [Orchestration Framework](orchestration-framework.md) | Canonical workflow patterns, execution protocol, cost model | advanced |
| [Git Worktree](git-worktree.md) | Parallel Claude Code sessions | intermediate |
| [Session Management](session-management.md) | Resuming, history, persistence | intermediate |
| [Multi-Agent Collaboration](multi-agent-collaboration.md) | Agent coordination, worktrees-first, Agent Teams | advanced |

## Reading Order

1. **orchestration-framework.md** — Core tenets, canonical patterns, execution protocol (start here for v0.6.0+)
2. **git-worktree.md** — Foundational for parallel work
3. **session-management.md** — Managing conversation state
4. **multi-agent-collaboration.md** — Coordination patterns in practice

## When to Use These Patterns

| Situation | Pattern |
|-----------|---------|
| Planning any non-trivial task | Orchestration Framework (Task Execution Protocol) |
| Working on multiple features | Git Worktree |
| Continuing previous work | Session Management |
| Complex multi-step workflows | Multi-Agent Collaboration |
| Parallel analysis tasks | Git Worktree + Multi-Agent |
| Long-running autonomous projects | Orchestration Framework (Initializer/Iterator Harness) |
| Quality-critical deliverables | Orchestration Framework (Evaluator-Optimizer Pattern) |

## What's New in v0.6.0

**orchestration-framework.md** (NEW):
- 5 core design tenets (simplicity-first, verification-as-requirement, plan-before-execute, compounding knowledge, token efficiency)
- 5 canonical agentic workflow patterns mapped to CC primitives
- Standard Task Execution Protocol (PLAN → REVIEW → EXECUTE → VERIFY → COMMIT)
- Agent failure mode catalog (5 patterns with mitigations)
- Multi-agent cost model (token economics)
- Delegation template (5-component structure)
- Initializer/iterator two-phase harness
- CC platform constraints table (Feb 2026)

**multi-agent-collaboration.md** (REVISED to v2.0):
- Reordered to worktrees-first (CC team daily driver)
- Added Agent Teams pattern (experimental)
- Added effort scaling heuristic
- Added cross-session persistence (3 approaches)
- Added subagent triggering patterns
