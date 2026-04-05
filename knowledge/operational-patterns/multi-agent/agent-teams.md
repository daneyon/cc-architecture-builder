---
id: agent-teams
title: Agent Teams — Multi-Session Coordination
category: operational-patterns/multi-agent
tags: [agent-teams, coordinator, multi-session, ipc, experimental, a-team]
summary: Deep-dive on CC Agent Teams — architecture, IPC mechanics, known constraints, setup patterns, and alignment with CAB's A-team product design cycle framework.
depends_on: [collaboration-patterns, orchestration-framework, subagents]
related: [worktree-workflows, delegation-templates, cost-model]
complexity: advanced
last_updated: 2026-04-05
estimated_tokens: 1000
source: https://code.claude.com/docs/en/agent-teams
confidence: B
review_by: 2026-07-05
revision_note: "v1.0 — NEW KB card. Synthesizes official Agent Teams docs + observable IPC behavior + A-team alignment."
---

# Agent Teams — Multi-Session Coordination

## Overview

Agent Teams enables multiple Claude sessions to coordinate on a shared task list with inter-agent messaging. Currently experimental — requires feature flag.

> **Official docs**: [code.claude.com/docs/en/agent-teams](https://code.claude.com/docs/en/agent-teams) — setup, display modes, task dependencies, known limitations.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│         TEAM LEAD (Session 1)               │
│   Decomposes tasks, assigns, approves plans │
└─────┬──────────┬──────────┬─────────────────┘
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

**Key components**:
- **Team lead**: Coordinates, assigns tasks, approves/rejects plans
- **Teammates**: Work independently in separate context windows
- **Shared task list**: Pending → in-progress → completed states, with file locking
- **Mailbox IPC**: File-based messaging for inter-agent communication

## Setup

**Primary method** — via `settings.json` (recommended by official docs):

```jsonc
// ~/.claude/settings.json (or project .claude/settings.json)
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

**Alternative** — via shell environment variable:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

Requires CC v2.1.32+. Teammates can be defined in `.claude/agents/*.md` with team-specific configurations.

**Display modes**:
- **In-process** (Shift+Down): Teammates run within the same terminal
- **Split panes** (tmux/iTerm2): Each teammate gets a visible terminal pane

## IPC Mechanism

Agent Teams uses file-based communication with the following officially documented structure:

- **Team config**: `~/.claude/teams/{team-name}/config.json`
- **Task storage**: `~/.claude/tasks/{team-name}/`
- **Task claiming**: File locking prevents duplicate handling
- **Messaging**: Mailbox-based with automatic message delivery (official terminology)
- **Execution backends**: tmux (Linux/macOS), iTerm2 (macOS native split), in-process fallback

> **Observed, not officially documented**: The specific IPC path `~/.claude/work/ipc/` and 500ms polling interval have been observed in practice but are not referenced in official documentation. Treat these as implementation details subject to change.

**Mailbox pattern for dangerous operations**: Worker agents send high-risk tool call requests to the team lead for approval rather than executing autonomously. This is CC's built-in safety mechanism for team-level permission escalation.

### Known Constraints (Observable)

| Constraint | Impact |
|-----------|--------|
| No session resumption | Team sessions are single-use; cannot `--continue` |
| No nested teams | A team cannot spawn sub-teams |
| Lead is fixed | Cannot reassign team lead mid-session |
| Significantly higher token cost | Per teammate; scales linearly (~7x is a CAB estimate, not official) |
| Race conditions possible | File-based IPC has known edge cases under heavy concurrent writes |
| Recommended 3-5 teammates | Beyond 5, coordination overhead exceeds parallelism benefit |
| 5-6 tasks per teammate | Sweet spot for task granularity |

---

## CAB A-Team Alignment

Agent Teams maps naturally to CAB's A-team product design cycle framework. The team lead acts as the orchestrator, with teammates as domain specialists:

| A-Team Role | Agent Teams Mapping | Typical Tasks |
|-------------|-------------------|---------------|
| Product Manager | Team lead or teammate | Requirements, prioritization, user stories |
| Software Architect | Teammate | System design, API contracts, tech decisions |
| UX Designer | Teammate | Interface design, user flows, prototypes |
| Developer | Teammate(s) | Implementation, testing, debugging |
| QA/Verifier | Teammate | Verification, test coverage, quality gates |

**Workflow pattern**: The orchestrator (running as team lead or in main session) decomposes the project into phase-appropriate tasks, assigns to teammates whose agent definitions include the right skills and domain knowledge, and synthesizes results.

### Practical Application

For a CAB-integrated project:

1. **Discovery phase**: Team lead + 2 teammates (researcher, analyst) — gather requirements, competitive analysis
2. **Build phase**: Team lead + 3-4 teammates (frontend, backend, testing, documentation) — parallel implementation
3. **Verify phase**: Verifier teammate runs independently, reports to lead

**Key principle**: Agent Teams excels when tasks have genuine inter-dependencies (shared API contracts, cross-component integration). For fully independent tasks, worktrees remain cheaper and simpler.

---

## Coordinator Mode (CAB Forward-Looking)

> **Confidence: C** — This section is CAB forward-looking speculation based on early signals. Coordinator mode is **not in current official CC documentation** as of 2026-04-05. Do not rely on this for production architectures.

Coordinator mode would enhance the team lead with formal coordination capabilities. CAB's orchestration patterns (PLAN → VERIFY → COMMIT, delegation templates, phase-agent routing) are designed to be compatible with such a mode if it becomes available.

**Architectural preparation**: CAB's orchestrator agent definition, delegation templates, and phase-agent routing map are structured to work both with current Agent Teams (manual task assignment) and a potential future coordinator mode (programmatic task orchestration).

---

## When to Use Agent Teams vs. Alternatives

| Scenario | Recommendation | Rationale |
|----------|---------------|-----------|
| Independent parallel features | **Worktrees** | Separate budgets, no coordination overhead |
| Sequential analysis pipeline | **Subagent chain** | Clear dependencies, simpler than teams |
| Cross-component integration | **Agent Teams** | Shared task list enables coordination |
| Competing approaches to evaluate | **Agent Teams** | Teammates can share intermediate findings |
| Quick parallel research | **Parallel subagents** | "Use 5 subagents" prompt, lower overhead |

## See Also

- [Collaboration Patterns](collaboration-patterns.md) — All 4 patterns overview
- [Worktree Workflows](worktree-workflows.md) — The cheaper alternative for parallel work
- [Delegation Templates](../orchestration/delegation-templates.md) — How to structure task assignments
- [A-Team Framework](../../reference/product-design-cycle.md) — Product design lifecycle
