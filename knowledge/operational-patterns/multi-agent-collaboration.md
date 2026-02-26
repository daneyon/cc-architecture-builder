---
id: multi-agent-collaboration
title: Multi-Agent Collaboration
category: operational-patterns
tags: [agents, collaboration, orchestration, multi-agent, subagents, worktrees, agent-teams]
summary: Patterns for coordinating multiple Claude agents working together on complex tasks, from git worktrees (daily driver) through Agent Teams (experimental).
depends_on: [subagents, git-worktree]
related: [session-management, orchestration-framework]
complexity: advanced
last_updated: 2026-02-25
estimated_tokens: 900
revision_note: "v2.0 — Added Agent Teams pattern, reordered to worktrees-first, added effort scaling, cross-session persistence, subagent triggering patterns. Sources: Anthropic engineering articles (Dec 2024 – Nov 2025), Boris Cherny threads (Dec 2025 – Feb 2026)."
---

# Multi-Agent Collaboration

## Overview

Complex tasks often benefit from multiple specialized agents working together. Claude Code supports this through several coordination mechanisms, ordered here from most practical (daily use by the CC team) to most advanced (experimental).

## Collaboration Patterns

### Pattern 1: Parallel via Git Worktrees (Daily Driver)

The CC team's preferred approach for parallel work. Each worktree is an isolated git checkout with its own Claude session.

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Worktree 1 (za) │  │ Worktree 2 (zb) │  │ Worktree 3 (zc) │
│ Tab: Blue       │  │ Tab: Green       │  │ Tab: Orange      │
│                 │  │                 │  │                 │
│ Feature: Auth   │  │ Feature: API    │  │ Analysis-only   │
│ Claude Session  │  │ Claude Session  │  │ Claude Session  │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
                    Shared Git Repository
                    (merge in main worktree)
```

**Use when**: Tasks can run independently. This is the default for most parallel work.

**Setup**:
```bash
# Create worktrees
git worktree add .claude/worktrees/feature-auth origin/main
git worktree add .claude/worktrees/feature-api origin/main
git worktree add .claude/worktrees/analysis origin/main  # read-only investigation

# Shell aliases for fast switching (add to .zshrc)
alias za='cd .claude/worktrees/feature-auth && claude'
alias zb='cd .claude/worktrees/feature-api && claude'
alias zc='cd .claude/worktrees/analysis && claude'
```

**Tips from the CC team**:
- Name and color-code terminal tabs (one per worktree)
- Enable system notifications to know when a session needs input
- Keep a dedicated "analysis" worktree for read-only investigation (log reading, queries)
- 3-5 worktrees is the practical sweet spot

### Pattern 2: Sequential Subagent Chain

Subagents within a single session, executed sequentially with explicit context passing.

```
Main Agent
    │
    ├──▶ Subagent A (analyze) → results
    │
    ├──▶ Subagent B (implement, using A's results) → results
    │
    └──▶ Subagent C (review B's implementation) → final results
```

**Use when**: Tasks have clear sequential dependencies and benefit from context isolation between steps.

**Example prompt**:
```
Use the analyzer agent to find security issues in src/auth/,
then use the implementer agent to fix them,
then use the reviewer agent to verify the fixes.
```

### Pattern 3: Main Agent + Specialists

The main session acts as orchestrator, delegating to specialist agents based on task type.

```
┌─────────────────────────────────────────┐
│              Main Agent                  │
│     (orchestrates, synthesizes)          │
└─────────────────┬───────────────────────┘
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
   ┌───────┐  ┌───────┐  ┌───────┐
   │Domain │  │Code   │  │Data   │
   │Expert │  │Review │  │Analyst│
   └───────┘  └───────┘  └───────┘
```

**Use when**: A single problem needs diverse expertise. Each specialist has focused tools and skills loaded.

### Pattern 4: Agent Teams (Experimental)

Multi-session coordination with shared task lists and inter-agent messaging.

```
┌─────────────────────────────────────────┐
│         TEAM LEAD (Session 1)           │
│   Coordinates, assigns, synthesizes     │
└─────┬──────────┬──────────┬─────────────┘
      │          │          │
      ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│Teammate A│ │Teammate B│ │Teammate C│
│Session 2 │ │Session 3 │ │Session 4 │
│Own CW    │ │Own CW    │ │Own CW    │
│Shared    │ │Shared    │ │Shared    │
│task list │ │task list │ │task list │
└──────────┘ └──────────┘ └──────────┘
```

**Use when**: Tasks genuinely require inter-agent communication (research with competing hypotheses, cross-layer coordination, tasks where agents need to share intermediate findings).

**Requirements**:
- Feature flag: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
- Higher token cost (~15x vs chat)
- 2-5 teammates recommended for most tasks

**Caution**: Agent Teams is significantly more expensive than worktrees. Use worktrees (Pattern 1) unless you specifically need the inter-agent messaging and shared task list capabilities.

## Effort Scaling Heuristic

Match the number of agents to task complexity (from Anthropic's "Multi-Agent Research System"):

| Task Complexity | Agent Configuration | Example |
|-----------------|---------------------|---------|
| Simple fact-finding | 1 agent, 3-10 tool calls | "What's the error in this function?" |
| Direct comparison | 2-4 subagents, 10-15 calls each | "Compare auth approaches: JWT vs session vs OAuth" |
| Comprehensive research | 5-10+ subagents, clear division of labor | "Audit the entire codebase for security vulnerabilities" |
| Multi-phase lifecycle | Orchestrator + state management | Full product development pipeline |

**Subagent triggering**: Append "use subagents" or "use N subagents" to any prompt where you want Claude to throw more compute at the problem. Offload individual tasks to subagents to keep the main agent's context window clean and focused.

## Cross-Session Persistence

Three approaches scaled to project complexity:

### Lightweight: Notes Directory

Maintain a `notes/` directory per project, updated after each PR or session. Point CLAUDE.md at it. Best for single-developer feature work.

```
notes/
├── 2026-02-15-auth-implementation.md
├── 2026-02-16-api-refactor.md
└── 2026-02-18-test-coverage.md
```

In CLAUDE.md: `@./notes/`

### Medium: Progress File + Feature List

For long-running autonomous tasks. Two files:

- `claude-progress.txt` — Free-form progress notes, updated each session
- `features.json` — Structured feature tracking with pass/fail status

```json
{
  "features": [
    {"id": "auth-login", "description": "User login with JWT", "passes": true},
    {"id": "auth-register", "description": "Registration flow", "passes": false},
    {"id": "auth-reset", "description": "Password reset", "passes": false}
  ]
}
```

### Full: Project State YAML

For multi-phase lifecycle management (see Orchestration Framework for schema).

## Coordination via Git

Git is the universal coordination layer across all patterns:

| Action | Purpose |
|--------|---------|
| Commits | Checkpoint agent work; ensure clean state between sessions |
| Branches | Isolate parallel work (one per worktree) |
| PRs | Review cross-agent output; add CLAUDE.md learnings via @.claude |
| Merge | Integrate findings from parallel sessions |

## When to Use Each Pattern

| Situation | Pattern | Cost |
|-----------|---------|------|
| Independent parallel tasks | Worktrees (Pattern 1) | Separate session budgets |
| Sequential dependent tasks | Subagent chain (Pattern 2) | Additive in main context |
| Single problem, multiple perspectives | Main + specialists (Pattern 3) | Main context + isolated agent contexts |
| Tasks requiring inter-agent communication | Agent Teams (Pattern 4) | ~15x chat tokens |

## Limitations

- Subagents don't share context (must pass findings explicitly)
- Agent Teams is experimental and token-intensive
- Worktree coordination is manual (human merges, resolves conflicts)
- Debugging multi-agent issues requires tracing agent decision patterns
- Complex chains compound errors — verify at each step

## See Also

- [Orchestration Framework](orchestration-framework.md) — Canonical patterns, execution protocol, cost model
- [Subagents](../components/subagents.md) — Agent definitions and configuration
- [Git Worktree](git-worktree.md) — Parallel session setup
- [Session Management](session-management.md) — Resuming and persisting work
