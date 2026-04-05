---
id: delegation-templates
title: Delegation Templates & Phase-Agent Routing
category: operational-patterns/orchestration
tags: [delegation, agents, routing, orchestrator, phase-mapping]
summary: Structured delegation templates for orchestrator-to-specialist communication and phase-based agent routing maps.
depends_on: [orchestration-framework, subagents]
related: [cost-model, collaboration-patterns]
complexity: advanced
last_updated: 2026-04-05
estimated_tokens: 800
source: CAB-original
confidence: A
review_by: 2026-07-05
---

# Delegation Templates & Phase-Agent Routing

## Delegation Template

When the orchestrator delegates to a specialist agent, structure with five components:

```markdown
## Task Delegation: [Task Name]

### Objective
[Specific, measurable goal. What does "done" look like?]

### Output Format
[Expected deliverable: file path, summary format, structured data schema]

### Tools & Sources
[Which tools to use. Which files/APIs to consult. What to prioritize.]

### Boundaries
[IN scope. Explicitly OUT of scope. Maximum iterations.]

### Available Extensions
[Which project skills the agent should use rather than implementing manually.]

### Verification Criteria
[How the orchestrator will confirm this subtask succeeded.
 Include specific commands, checks, or criteria.]
```

### Example

```markdown
## Task Delegation: Implement Authentication Module

### Objective
Create login/register/logout endpoints with JWT. All endpoints pass auth test suite.

### Output Format
New files in src/auth/. Updated routes in src/routes.ts. No changes to existing tests.

### Tools & Sources
Read, Write, Edit, Bash. Reference docs/api-spec.md, src/middleware/auth.ts.

### Boundaries
IN: Login, register, logout, JWT.
OUT: OAuth, 2FA, password reset (separate tasks).
Max: 3 implement-verify cycles.

### Verification Criteria
- `npm run test:auth` passes
- `npm run typecheck` passes
- `npm run lint` passes
- Correct status codes (200, 201, 401, 404)
```

---

## Phase-Agent Routing Map

Map project lifecycle phases to specialist agents best suited for each. This aligns with the A-team product design cycle framework.

| Phase | Primary Agents | Supporting Skills |
|-------|---------------|-------------------|
| 0 – Discovery | product-manager, ux-researcher | planning-implementation |
| 1 – Definition | software-architect, product-manager | planning-implementation |
| 2 – Design | ux-designer, software-architect | architecture-analyzer |
| 3 – Build | code-reviewer, debugger-specialist | architecture-analyzer |
| 4 – Verify | verifier, security-auditor | assessing-quality |
| 5 – Launch | tech-writer, product-manager | readme-generator |
| 6 – Iterate | performance-optimizer, codebase-manager | designing-workflows |

**Adaptation principle**: Not every project uses all phases. The orchestrator selects the subset relevant to the current project's scale and needs. The routing map is a menu, not a mandate.

---

## Two-Phase Harness: Initializer + Iterator

For long-running projects spanning multiple sessions:

**Phase 1: Initializer Session**

1. Read requirements/specifications
2. Generate feature list (JSON with `passes: boolean` per feature)
3. Create progress file (`notes/progress.md` or `project-state.yaml`)
4. Write initialization script (environment, dependencies)
5. Initial git commit (clean starting state)
6. Start first feature

**Phase 2: Iterator Sessions**

1. Read progress file and feature list
2. Identify next incomplete feature
3. Implement via Task Execution Protocol
4. Run verification
5. Update feature list (`passes: true`) and progress
6. Commit and push

```
SESSION 1 (Initializer)          SESSIONS 2-N (Iterator)
┌─────────────────────┐          ┌─────────────────────┐
│ Read requirements    │          │ Read progress file   │
│ Generate feature list│          │ Find next feature    │
│ Create progress file │          │ Plan → Execute       │
│ Initial commit       │          │ Verify               │
│ Start feature #1     │          │ Update + Commit      │
└─────────────────────┘          └─────────────────────┘
```

**JSON over YAML for agent-editable state**: Models are less likely to introduce formatting errors in JSON than YAML. Use `features.json` for feature lists even if `project-state.yaml` is used for human-managed tracking.

---

## Agent Teams Delegation

When using Agent Teams (experimental, coordinator mode):

- **Team lead** decomposes tasks and assigns to teammates via shared task list
- **Teammates** work in separate context windows with their own tool access
- **Mailbox-based IPC**: File-based messaging at `~/.claude/work/ipc/` with 500ms polling
- **Known constraints**: No nested teams, lead is fixed, no session resumption, ~7x token cost
- **Recommended sizing**: 3-5 teammates, 5-6 tasks each

> **Official docs**: [Agent Teams](https://code.claude.com/docs/en/agent-teams) — full setup, display modes, task dependencies.

Use Agent Teams when tasks genuinely need inter-agent communication. For independent parallel tasks, worktrees are cheaper and more reliable.

## See Also

- [Orchestration Framework](framework.md) — Tenets, patterns, execution protocol
- [Cost Model](cost-model.md) — Token economics for delegation decisions
- [Agent Teams](../multi-agent/agent-teams.md) — Detailed Agent Teams patterns
- [A-Team Framework](../../reference/product-design-cycle.md) — Product lifecycle phases
