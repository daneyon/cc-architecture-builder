---
id: orchestration-framework
title: Orchestration Framework
category: operational-patterns
tags: [orchestration, workflows, agents, patterns, verification, delegation, state-management]
summary: Comprehensive orchestration framework for Claude Code agentic workflows, covering canonical patterns, task execution protocol, failure modes, cost model, delegation templates, and state management.
depends_on: [subagents, multi-agent-collaboration, memory-claudemd]
related: [session-management, git-worktree]
complexity: advanced
last_updated: 2026-02-25
estimated_tokens: 3500
revision_note: "v2.0 — New file consolidating orchestration patterns from Anthropic engineering articles (Dec 2024 – Nov 2025), Boris Cherny CC creator tips (Dec 2025 – Feb 2026), and context engineering principles (Sep 2025)."
source: https://www.anthropic.com/engineering/building-effective-agents
---

# Orchestration Framework

## Purpose

This document defines how Claude Code components (skills, agents, commands, hooks) coordinate to accomplish complex, multi-step tasks. It establishes the canonical workflow patterns, execution protocols, failure mitigations, and cost models that govern all agentic work within the CAB (cc-architecture-builder) framework.

---

## Core Design Tenets

Before diving into orchestration mechanics, these principles govern all architectural decisions in this framework. They are derived from Anthropic's official engineering guidance and validated by the Claude Code team's daily practice.

### Tenet 1: Simplicity-First Complexity Ladder

Start with the simplest solution that works. Escalate only when measured improvement justifies the added complexity. Never skip levels.

```
COMPLEXITY LADDER

Level 0 │ Single optimized prompt           │ Most problems start and end here
Level 1 │ Single agent + skills             │ Procedural augmentation for domain tasks
Level 2 │ Sequential subagent chains        │ Tasks with clear dependencies needing context isolation
Level 3 │ Parallel subagents / git worktrees │ Independent tasks that can run simultaneously
Level 4 │ Agent Teams [experimental]        │ Tasks requiring inter-agent communication
Level 5 │ Full orchestrator + state mgmt    │ Multi-phase project lifecycle coordination

Rule: Validate that Level N is insufficient before moving to Level N+1.
```

**Reference**: Anthropic, "Building Effective Agents" (Dec 2024) — "Agents can be hard to deploy, so we recommend trying to find the simplest solution possible, and only increasing complexity when needed."

### Tenet 2: Verification as Architectural Requirement

Every agent, every task, every phase gate requires a verification method. Providing Claude a way to verify its own work improves output quality by 2-3x (per Boris Cherny, CC creator). Verification is not optional — it is a required field in every agent definition and a mandatory step in every task cycle.

### Tenet 3: Plan Before Execute

Complex tasks follow the standard Task Execution Protocol (see below). Investment in planning yields disproportionate returns in implementation quality. If execution goes sideways, stop and re-plan — never push forward on a broken implementation.

### Tenet 4: Compounding Knowledge via CLAUDE.md

CLAUDE.md is not a static configuration file. It is a living feedback loop: every time Claude makes a correctable error, instruct it to update CLAUDE.md so the mistake is never repeated. Over time, the error rate measurably drops. For teams, use @.claude in PR reviews to add learnings as part of the PR itself.

### Tenet 5: Token Efficiency as Public Good

Context window space is shared across rules, skills, agent instructions, and the actual work. Every token of configuration displaces a token of productive output. Design for progressive disclosure: load only what the current task requires, reference additional resources via @imports, and prefer lean component definitions.

---

## Canonical Agentic Workflow Patterns

Anthropic identifies five foundational patterns for building agentic systems. Each maps to specific Claude Code primitives. Apply them in order of increasing complexity (per Tenet 1).

### Pattern 1: Prompt Chaining

Sequential LLM calls where the output of step N feeds step N+1, with programmatic gate checks between steps.

```
[Prompt A] → Gate Check → [Prompt B] → Gate Check → [Prompt C]
     │              │            │              │            │
  Generate       Validate     Transform     Validate     Output
   code          (lint ok?)    to tests     (tests pass?)  final
```

**CC Implementation**: Main session executes skill A → skill B → skill C. Commands can trigger the chain. Gate checks are bash commands (lint, test, typecheck) or human approval.

**When to use**: Tasks decomposable into fixed sequential steps where each step can be validated before proceeding.

### Pattern 2: Routing

Classify the incoming request and direct it to the appropriate specialized handler.

```
[User Request]
       │
       ▼
┌─────────────┐     ┌───────────┐
│   Router     │────▶│ Agent A   │  (matches: "debug", "error", "fix")
│  (main       │     └───────────┘
│   session)   │     ┌───────────┐
│              │────▶│ Agent B   │  (matches: "design", "architecture")
│              │     └───────────┘
│              │     ┌───────────┐
│              │────▶│ Skill C   │  (matches: "document", "readme")
└─────────────┘     └───────────┘
```

**CC Implementation**: Main session acts as router. Agent `description` fields provide semantic matching. Well-written descriptions enable automatic routing without explicit classification logic.

**When to use**: Requests fall into distinct categories requiring different expertise, tools, or context.

### Pattern 3: Parallelization

Two sub-patterns:

**Sectioning** — Split independent subtasks across parallel workers:
```
[Decompose Task]
    ├──▶ Worktree 1: Frontend changes
    ├──▶ Worktree 2: Backend changes
    └──▶ Worktree 3: Test suite updates
         │
         ▼
    [Merge in main worktree]
```

**Voting** — Run the same task with different prompts, then synthesize:
```
[Same Question]
    ├──▶ Subagent A (conservative approach)
    ├──▶ Subagent B (aggressive approach)
    └──▶ Subagent C (balanced approach)
         │
         ▼
    [Main agent synthesizes best answer]
```

**CC Implementation**: Worktrees for sectioning (3-5 parallel sessions, each in its own git checkout — the CC team's preferred daily approach). Subagents with "use N subagents" prompt for voting or parallel exploration within a single session.

**When to use**: Tasks are decomposable into independent subtasks (sectioning) or benefit from diverse perspectives (voting).

### Pattern 4: Orchestrator-Workers

A central orchestrator agent dynamically breaks down the task, delegates to specialists, and synthesizes results.

```
┌─────────────────────────────────────────┐
│           ORCHESTRATOR AGENT            │
│  Reads state → Decomposes → Delegates   │
└─────────┬──────────┬──────────┬─────────┘
          │          │          │
          ▼          ▼          ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │Specialist│ │Specialist│ │Specialist│
    │Agent A   │ │Agent B   │ │Agent C   │
    └────┬─────┘ └────┬─────┘ └────┬─────┘
         │            │            │
         └────────────┼────────────┘
                      ▼
              [Orchestrator synthesizes]
```

**CC Implementation**: The orchestrator agent reads `project-state.yaml`, determines the current phase and required disciplines, and delegates via the Task tool to specialist agents. Each specialist has focused tools and skills. Results flow back to orchestrator for synthesis and state update.

**When to use**: Tasks are too complex for a single agent but have subtasks that can be dynamically identified rather than pre-defined. This is the primary pattern for the product lifecycle framework.

### Pattern 5: Evaluator-Optimizer

A generator produces output, an evaluator assesses it against criteria, and the generator iterates based on feedback.

```
┌──────────┐     ┌───────────┐
│ Generator │────▶│ Evaluator │
│ Agent     │◀────│ Agent     │
└──────────┘     └───────────┘
    │  ▲              │
    │  └──────────────┘
    │    (feedback loop until criteria met)
    ▼
[Final Output]
```

**CC Implementation**: Implementer agent generates code → code-reviewer agent evaluates against standards → if fails, implementer revises. The loop continues until the reviewer passes or max iterations reached.

**When to use**: Output quality requires iterative refinement against measurable criteria (code quality, test coverage, writing standards, design consistency).

### Pattern Selection Guide

| Signal | Pattern |
|--------|---------|
| Fixed sequential steps with validation gates | Prompt Chaining |
| Distinct request types needing different handlers | Routing |
| Independent subtasks, no inter-task communication | Parallelization |
| Complex task needing dynamic decomposition | Orchestrator-Workers |
| Quality-critical output needing iterative refinement | Evaluator-Optimizer |

**Combinations are common**: An orchestrator may use prompt chaining within a single worker, parallelization across workers, and evaluator-optimizer for quality-critical deliverables.

---

## Standard Task Execution Protocol

Every non-trivial task follows this cycle. Based on the Claude Code team's daily workflow (Boris Cherny, Threads 1-3, Dec 2025 – Feb 2026) and Anthropic's "Effective Harnesses" engineering article (Nov 2025).

```
┌────────────────────────────────────────────────────────────────┐
│                    TASK EXECUTION CYCLE                         │
│                                                                │
│  1. PLAN ──▶ 2. REVIEW ──▶ 3. EXECUTE ──▶ 4. VERIFY ──▶ 5. COMMIT │
│     ▲                                         │                │
│     │              SIDEWAYS?                   │                │
│     └──────── STOP & RE-PLAN ◀─────────────────┘                │
└────────────────────────────────────────────────────────────────┘
```

### Step 1: PLAN

Enter plan mode (Shift+Tab twice in CC terminal). Describe the objective and constraints. Iterate on the plan with Claude until it is solid. Do not skimp on this step — a well-crafted plan enables one-shot implementation.

**Advanced**: Have a second Claude session (or subagent) review the plan "as a staff engineer" before proceeding. This catches architectural issues early.

### Step 2: REVIEW

Human reviews the plan. Check for scope creep, missing edge cases, incorrect assumptions. Approve or request revisions. For automated workflows, a gate-check agent can perform this role.

### Step 3: EXECUTE

Switch to auto-accept mode. Claude implements from the approved plan. The plan acts as a blueprint — Claude should execute it faithfully, not reinvent the approach mid-implementation.

### Step 4: VERIFY

Claude verifies its own work using the domain-appropriate method:

| Domain | Verification Method |
|--------|--------------------|
| Code | Run test suite, lint, typecheck, diff main vs branch |
| Documentation | Spell-check, link validation, format check |
| Architecture | Mermaid diagram generation, constraint check |
| Data/Analytics | Query result validation, sample spot-checks |
| UI | Browser automation, screenshot comparison |
| Configuration | Dry-run, plan mode review |
| Any | "Prove to me this works" — challenge Claude to demonstrate correctness |

If verification fails, iterate (small issues) or return to PLAN (fundamental issues).

### Step 5: COMMIT

Git commit with a descriptive message. Update progress tracking:
- Update `project-state.yaml` (lifecycle tracking) OR
- Update `notes/` directory (lightweight alternative) OR
- Update `claude-progress.txt` (long-running autonomous tasks)

Always commit working state before ending a session — broken state handoff is one of the top agent failure modes.

### Failure Recovery

If execution goes sideways at any point:

1. **Stop immediately** — do not push forward on a broken path
2. **Switch to plan mode** — re-assess the approach with what you now know
3. **Include verification steps in the revised plan** — explicitly plan how to confirm each step
4. **Consider**: "Knowing everything you know now, scrap this and implement the elegant solution" (Boris Cherny prompting pattern)

---

## Agent Failure Mode Catalog

Five failure patterns observed in production agent systems (from Anthropic's "Effective Harnesses for Long-Running Agents" and CC team practice). Each has specific mitigations.

### Failure 1: One-Shotting

**Symptom**: Agent attempts the entire project in a single context window, runs out of context, produces incomplete or incoherent results.

**Mitigation**: Decompose work into a feature list (JSON or YAML) with boolean pass/fail tracking per feature. The agent should only work on one feature per iteration. The feature list structure should be pre-defined so the agent cannot edit its own success criteria.

```json
{
  "features": [
    {"id": "auth-login", "description": "User login with email/password", "passes": false},
    {"id": "auth-register", "description": "New user registration flow", "passes": false},
    {"id": "auth-reset", "description": "Password reset via email", "passes": false}
  ]
}
```

### Failure 2: Premature Completion

**Symptom**: Agent declares "Done!" with incomplete work, untested features, or missing edge cases.

**Mitigation**: Provide a comprehensive checklist the agent must verify against before declaring completion. Use the Verification Protocol (Step 4 of Task Execution). The agent must run actual verification (tests, lint, build) — verbal assertions of completion are insufficient.

### Failure 3: Broken State Handoff

**Symptom**: Agent leaves the codebase in an unfinished state between sessions. Next session inherits broken code with no context about what was in progress.

**Mitigation**: Mandatory git commit + progress file update before every session ends. The progress file should describe: what was completed, what was in progress, what is next, and any known issues. Use a Stop hook for deterministic enforcement:

```json
{
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "echo 'Remember: commit your work and update progress before ending.'"
    }]
  }]
}
```

### Failure 4: Testing Skip

**Symptom**: Agent marks features as done without running actual tests. Often manifests as features that "work" in isolation but fail in integration.

**Mitigation**: Verification is a separate, explicit step — not part of implementation. The verifier agent (or verification skill) runs independently after implementation. End-to-end testing prompts should be specific to the domain, not generic "make sure it works" instructions.

### Failure 5: Scope Drift

**Symptom**: Agent wanders into unrelated improvements, refactoring, or "nice to have" additions while working on a focused task.

**Mitigation**: Delegation prompts must include explicit boundaries (see Delegation Template below). Agent descriptions should be narrow and action-oriented. If the agent discovers work that should be done but is out of scope, it should log it as a task/note rather than doing it immediately.

---

## Multi-Agent Cost Model

Token consumption data from Anthropic's "Building a Multi-Agent Research System" (Jun 2025). These numbers inform architectural decisions about when multi-agent coordination is justified.

### Token Economics

| Configuration | Relative Token Cost | Notes |
|---------------|--------------------:|-------|
| Chat interaction (baseline) | 1x | Human ↔ Claude conversation |
| Single autonomous agent | ~4x | Agent with tool use and reasoning |
| Multi-agent system | ~15x | Orchestrator + specialist agents |

Token usage alone explains approximately 80% of performance variance in agent systems. Before adding agents, consider whether spending equivalent tokens on a single better-prompted agent would yield comparable results.

### Cost Optimization Levers

1. **Effort level** (`/model` in CC): Low/Medium/High directly controls token consumption. Boris uses High for all work; consider Medium or Low for well-defined, repetitive tasks.
2. **Model selection**: Upgrading from Sonnet 4 to Sonnet 4.5 often yields more improvement than doubling the token budget at the same model tier. Match model to task criticality.
3. **Context isolation**: Subagents only consume tokens for their own context. Use subagents to offload work and keep the main session's context clean and focused.
4. **Worktrees over Agent Teams**: Worktrees run in separate sessions with separate token budgets. Agent Teams shares coordination overhead across all participants.
5. **Progressive disclosure**: Load skills/knowledge on demand rather than pre-loading everything into rules/.

### When Multi-Agent is Justified

Multi-agent coordination is justified when **task value exceeds token cost** AND one of these conditions holds:
- Task requires more knowledge than fits in a single context window
- Task benefits from genuinely different expertise perspectives (not just parallelism)
- Task requires sustained work across multiple phases with different tooling needs
- Task failure cost is high enough to warrant evaluator-optimizer loops

---

## Orchestrator Agent Design

### Orchestrator Workflow

The orchestrator agent serves as the central coordinator for complex multi-step projects:

1. **Read state** — Load project-state.yaml, feature list, and progress file
2. **Assess phase** — Determine current lifecycle phase and completion status
3. **Decompose** — Break the next objective into delegatable subtasks
4. **Delegate** — Assign subtasks to specialist agents using the Delegation Template
5. **Synthesize** — Collect results, update state, determine next steps
6. **Report** — Summarize progress and recommend next actions to the human

### Delegation Template

When the orchestrator delegates to a specialist agent, structure the delegation with these five components (from Anthropic's Multi-Agent Research System, Principle #2: "Teach the orchestrator to delegate"):

```markdown
## Task Delegation: [Task Name]

### Objective
[Specific, measurable goal. What does "done" look like?]

### Output Format
[Expected deliverable: file path, summary format, structured data schema]

### Tools & Sources
[Which tools to use. Which files/APIs to consult. What to prioritize.]

### Boundaries
[What is IN scope. What is explicitly OUT of scope. Maximum iterations.]

### Verification Criteria
[How the orchestrator will confirm this subtask succeeded.
 Include specific commands, checks, or criteria.]
```

**Example**:
```
## Task Delegation: Implement Authentication Module

### Objective
Create login/register/logout endpoints with JWT tokens. All endpoints must pass
the auth test suite and return proper HTTP status codes.

### Output Format
New files in src/auth/. Updated routes in src/routes.ts. No changes to existing tests.

### Tools & Sources
Use Read, Write, Edit, Bash. Reference docs/api-spec.md for endpoint contracts.
Reference src/middleware/auth.ts for existing JWT helper.

### Boundaries
IN SCOPE: Login, register, logout endpoints. JWT generation and validation.
OUT OF SCOPE: OAuth, 2FA, password reset (these are separate tasks).
Max iterations: 3 implement-verify cycles.

### Verification Criteria
- `npm run test:auth` passes (all tests green)
- `npm run typecheck` passes
- `npm run lint` passes
- New endpoints return correct status codes (200, 201, 401, 404)
```

### Phase-Agent Routing Map

Map project lifecycle phases to the specialist agents best suited for each:

| Phase | Primary Agents | Supporting Skills |
|-------|---------------|-------------------|
| 0 – Discovery | product-manager, ux-researcher | plan-apply-strategy |
| 1 – Definition | software-architect, product-manager | plan-design-implementation |
| 2 – Design | ux-designer, software-architect | dev-analyze-architecture, dev-design-data-model |
| 3 – Build | code-reviewer, debugger-specialist | dev-analyze-architecture, doc-generate-readme |
| 4 – Verify | verifier, security-auditor | (domain-specific verification) |
| 5 – Launch | tech-writer, product-manager | doc-generate-readme, plan-design-gtm |
| 6 – Iterate | performance-optimizer, codebase-manager | ops-manage-feedback |

### Two-Phase Harness: Initializer + Iterator

For long-running projects spanning multiple sessions, use the two-phase harness pattern from Anthropic's "Effective Harnesses for Long-Running Agents" (Nov 2025). The first session uses a specialized initialization prompt; all subsequent sessions use a different iteration prompt.

**Phase 1: Initializer Session**

The initializer agent (or `init-project` command) sets up the environment:

1. Reads requirements/specifications
2. Generates a **feature list** (JSON, with `passes: boolean` per feature)
3. Creates a **progress file** (`claude-progress.txt` or `project-state.yaml`)
4. Writes an **initialization script** (environment setup, dependencies, config)
5. Makes an initial **git commit** (clean starting state)
6. Outputs the first feature to work on

**Phase 2: Iterator Sessions**

Each subsequent session:

1. Reads the progress file and feature list
2. Identifies the next incomplete feature
3. Implements the feature using the Task Execution Protocol
4. Runs verification
5. Updates the feature list (`passes: true`) and progress file
6. Commits and pushes

```
SESSION 1 (Initializer)          SESSIONS 2-N (Iterator)
┌─────────────────────┐          ┌─────────────────────┐
│ Read requirements    │          │ Read progress file   │
│ Generate feature list│          │ Find next feature    │
│ Create progress file │          │ Plan → Execute       │
│ Write init script    │          │ Verify               │
│ Initial commit       │          │ Update feature list  │
│ Start feature #1     │          │ Update progress file │
└─────────────────────┘          │ Commit + push        │
                                 └─────────────────────┘
```

**Why JSON over YAML for agent-editable state**: The "Effective Harnesses" article recommends JSON for state files the model must edit, as models are less likely to introduce formatting errors in JSON than in YAML. Consider `features.json` for the feature list even if `project-state.yaml` is used for human-managed lifecycle tracking.

---

## CC Platform Constraints & Workarounds

| Constraint | Impact | Workaround | Status (Feb 2026) |
|---|---|---|---|
| Single subagent nesting depth | Orchestrator cannot chain agent → sub-sub-agent | Main session acts as router; orchestrator advises, main delegates. Agent Teams provides multi-session coordination as alternative. | Still true for subagents; Agent Teams is experimental workaround |
| No native database | State management limited to filesystem | YAML/JSON state files; structured reads. MCP servers for external DBs. | Stable constraint |
| No native vector search | Knowledge retrieval is keyword/path-based | Structured indexes (INDEX.md, JSON manifests); MCP for semantic search at scale | Stable constraint |
| No self-scheduling | Agents cannot auto-trigger phase transitions | Human triggers via commands or conversation. Hooks provide event-driven automation for tool use/session events. | Stable constraint |
| Metadata registry limit (~50-60 skills) | Cannot register unlimited skills globally | Prioritize global skills; domain-specific in plugins. Lean metadata descriptions. | Stable constraint |
| Agent Teams experimental | Inter-agent messaging requires feature flag | Enable via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Higher token cost (~15x). Use worktrees for most parallel work. | Research preview |
| Context window finite | Long sessions degrade quality | Offload subtasks to subagents (separate context). Use `/compact` or start fresh sessions. Worktrees keep each session focused. | Stable constraint |

---

## Context Engineering Principles

The orchestration framework is grounded in context engineering — the discipline of optimizing the information provided to an LLM within its finite context window. Key principles from Anthropic's "Effective Context Engineering for AI Agents" (Sep 2025):

### Core Concept

Context engineering treats the context window as a shared, finite resource. Every token of system prompt, rules, skill instructions, and agent definitions competes with tokens available for the actual task. The goal is the **smallest set of high-signal tokens that maximizes the desired outcome**.

### Application to CAB

| Principle | CAB Implementation |
|-----------|-------------------|
| **Right altitude** | CLAUDE.md at high level; details in skills/knowledge loaded on demand |
| **Token-efficient tools** | Lean skill metadata (name + 1-2 line description); full instructions only when invoked |
| **Progressive disclosure** | @imports in CLAUDE.md; skill references/ loaded only when needed |
| **Context rot awareness** | Use `/compact` for long sessions; offload to subagents; keep main context focused |
| **Just-in-time retrieval** | Knowledge base structured for grep/glob retrieval, not pre-loaded |
| **Compaction for persistence** | Progress files and notes/ directory for cross-session memory |
| **Sub-agent architectures** | Subagents get their own context window — use them to preserve main context |

### Guiding Rule

> Before adding any content to CLAUDE.md, rules/, or skill metadata, ask: "Does this token earn its place in every session, or should it be loaded on demand?"

---

## See Also

- [Multi-Agent Collaboration](multi-agent-collaboration.md) — Coordination patterns in practice
- [Git Worktree](git-worktree.md) — Parallel session setup
- [Session Management](session-management.md) — Resuming and persisting work
- [Memory & CLAUDE.md](../components/memory-claudemd.md) — 5-tier memory hierarchy
- [Subagents](../components/subagents.md) — Agent definitions and configuration
