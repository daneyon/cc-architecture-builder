---
type: index
scope: operational-patterns
file_count: 13
last_updated: 2026-04-05
revision_note: "v3.0 — Modularized into subdirectories. 3 monolith files split into 9 focused files across 3 subdirectories."
---

# Operational Patterns Index

> Advanced workflow patterns for maximizing Claude Code efficiency.

## Directory Structure

```
operational-patterns/
├── orchestration/          # Workflow patterns, execution protocol, costs
│   ├── framework.md        # Tenets, 5 canonical patterns, task exec protocol
│   ├── delegation-templates.md  # Delegation structure, phase-agent routing
│   └── cost-model.md       # Token economics, prompt cache, optimization
├── multi-agent/            # Agent coordination, teams, worktrees
│   ├── collaboration-patterns.md  # 4 patterns overview, effort scaling
│   ├── agent-teams.md      # Agent Teams deep-dive, A-team alignment
│   └── worktree-workflows.md  # Git worktree setup and patterns
├── state-management/       # Sessions, context, filesystem state
│   ├── session-lifecycle.md # Session resume, context health, compaction
│   ├── context-engineering.md  # 200-line discipline, optimization
│   └── filesystem-patterns.md  # notes/, cold-start anchors, persistence
├── team-collaboration.md   # Multi-human + multi-agent protocols
├── extension-discovery.md  # Extension awareness, Three-Point Reinforcement
└── sync-protocol.md        # CAB ↔ global ~/.claude/ deployment protocol
```

## Reading Order

1. **orchestration/framework.md** — Core tenets, canonical patterns (start here)
2. **state-management/context-engineering.md** — 200-line discipline, compaction
3. **multi-agent/collaboration-patterns.md** — 4 coordination patterns
4. **state-management/session-lifecycle.md** — Session management
5. **state-management/filesystem-patterns.md** — Persistent state design
6. **orchestration/delegation-templates.md** — Delegation structure
7. **orchestration/cost-model.md** — Token economics
8. **multi-agent/agent-teams.md** — Agent Teams deep-dive
9. **multi-agent/worktree-workflows.md** — Parallel execution
10. **team-collaboration.md** — Human-agent collaboration
11. **extension-discovery.md** — Extension awareness persistence

## When to Use

| Situation | Go To |
|-----------|-------|
| Planning any non-trivial task | `orchestration/framework.md` (Task Execution Protocol) |
| Delegating to specialist agents | `orchestration/delegation-templates.md` |
| Evaluating agent cost/benefit | `orchestration/cost-model.md` |
| Working on multiple features in parallel | `multi-agent/worktree-workflows.md` |
| Need inter-agent communication | `multi-agent/agent-teams.md` |
| Choosing between collaboration patterns | `multi-agent/collaboration-patterns.md` |
| Continuing previous work / session health | `state-management/session-lifecycle.md` |
| Optimizing context usage | `state-management/context-engineering.md` |
| Designing cross-session state | `state-management/filesystem-patterns.md` |
| Multiple people/agents on same repo | `team-collaboration.md` |
| Skills forgotten mid-session | `extension-discovery.md` |
| Deploying CAB changes to global | `sync-protocol.md` |

## Migration Notes (v1.01)

Original monolith files split during modularization (2026-04-05):

| Original | Split Into | Status |
|----------|-----------|--------|
| `orchestration-framework.md` | `orchestration/` (3 files) | ✅ Removed |
| `multi-agent-collaboration.md` | `multi-agent/collaboration-patterns.md` + `agent-teams.md` | ✅ Removed |
| `git-worktree.md` | `multi-agent/worktree-workflows.md` | ✅ Removed |
| `session-management.md` | `state-management/` (3 files) | ✅ Removed |
