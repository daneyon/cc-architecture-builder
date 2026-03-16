---
type: index
scope: operational-patterns
file_count: 4
last_updated: 2026-03-16
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

1. **orchestration-framework.md** — Core tenets, canonical patterns, execution protocol (start here)
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

## Key Highlights

**orchestration-framework.md**:
- 5 core design tenets, 5 canonical agentic workflow patterns mapped to CC primitives
- Standard Task Execution Protocol (PLAN → REVIEW → EXECUTE → VERIFY → COMMIT)
- Agent failure mode catalog, multi-agent cost model, delegation templates

**multi-agent-collaboration.md**:
- Worktrees-first coordination, Agent Teams (experimental)
- Effort scaling heuristic, cross-session persistence, subagent triggering patterns
