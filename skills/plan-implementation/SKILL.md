---
name: plan-implementation
description: >-
  Generate SOW, implementation plans, acceptance criteria, and phased backlogs.
  Decomposes requirements into actionable deliverables. Triggers: plan project,
  scope feature, write requirements, create SOW, define acceptance criteria.
argument-hint: "Project or feature to plan (e.g., 'plan migration from REST to GraphQL API')"
allowed-tools: Read, Write, Grep, Glob
---
# Planning & Implementation

## Purpose

This skill provides the procedural knowledge for the PLAN phase of any project or
task — from initial scoping through detailed implementation planning. It bridges
the gap between "we have an idea" and "the team knows exactly what to build and how."

## Core Workflow

```
Idea/Request
    |
    v
+--------------------------+
| 1. SCOPE (SOW)           |  "What are we building and why?"
|    Problem -> Solution    |  Concise, approvable, stakeholder-facing
|    -> Feasibility -> KPIs |  Template: assets/sow-template.md
+-----------+--------------+
            | Approved?
            v
+--------------------------+
| 2. PLAN (Implementation) |  "How exactly do we build it?"
|    Architecture -> Phases |  Detailed, actionable, team-facing
|    -> Tasks -> Acceptance |  Template: assets/implementation-plan-template.md
+-----------+--------------+
            |
            v
+--------------------------+
| 3. EXECUTE               |  Handed off to execute-task skill
|    Sprint -> Build ->    |  or domain-specific project agents
|    Verify -> Commit      |
+--------------------------+
```

## When to Use Which Template

| Situation                              | Template                                                     | Audience                        |
| -------------------------------------- | ------------------------------------------------------------ | ------------------------------- |
| New project proposal / internal pitch  | **SOW**                                                | PM, advisor, client, leadership |
| Approved project ready for development | **Implementation Plan**                                | Engineering team, QA, DevOps    |
| Quick feature addition                 | Neither — use execute-task skill directly                | Self                            |
| Complex feature with unknowns          | SOW (lightweight) -> Implementation Plan (targeted sections) | Team                            |

## Scoping: The SOW Approach

The SOW (Scope of Work) is the **concise approval document** — it defines what
we're building, why, for whom, and what success looks like. It does NOT specify
technical implementation details.

### SOW Structure (9 sections)

1. **Project Information** — Title, owner, team
2. **Problem Statement** — Context, motivation, current pain points with quantified impact
3. **Proposed Solution** — Concept overview, approach type (automation/AI/hybrid), high-level workflow
4. **Key Features & Benefits** — Efficiency gains, user impact, strategic business value
5. **Potential Challenges** — Technical constraints, organizational risks, mitigations
6. **Estimated Timeline & Budget** — Major phases with rough durations, resource estimates
7. **KPIs** — Technical performance, usability, business value, data integrity, innovation
8. **Visualizations** — Before/after workflow diagrams, process flows
9. **Architecture Logic** — Software/data pipeline overview, integration points, output conditions

**Key principle**: The SOW should be approachable by non-technical stakeholders while
containing enough technical signal for engineers to estimate feasibility.

Full template: [assets/sow-template.md](assets/sow-template.md)

## Implementation Planning

Once the SOW is approved, the implementation plan provides the **actionable technical
blueprint**. This is the hybrid PRD+SRD — combining product requirements with system
requirements into a single working document.

### Plan Structure

1. **Quick-Start Guide** — Elevator pitch, approach summary, phase overview, validation checkpoints
2. **Project Overview** — Executive summary, problem analysis, stakeholder map
3. **Requirements** — Functional (user stories + acceptance criteria), non-functional (performance, security, accessibility)
4. **System Architecture** — Component design, data model, API contracts, technology stack decisions (ADRs)
5. **Implementation Phases** — Sprint/phase breakdown with specific deliverables and gate criteria
6. **Testing Strategy** — Unit, integration, E2E, performance, security, UAT approach
7. **Deployment Plan** — Environment strategy, CI/CD, rollback, monitoring
8. **Operational Handoff** — Documentation, training, maintenance procedures

### Phase Gate Criteria

Every phase transition requires explicit criteria before proceeding:

| Transition                     | Gate                                                           |
| ------------------------------ | -------------------------------------------------------------- |
| Discovery -> Strategy          | Problem validated, feasibility confirmed                       |
| Strategy -> Architecture       | Requirements approved, KPIs defined, risks accepted            |
| Architecture -> Implementation | Architecture reviewed, designs approved, specs complete        |
| Implementation -> Validation   | Feature-complete, code reviewed, CI green                      |
| Validation -> Deployment       | Critical bugs resolved, UAT signed off, performance acceptable |
| Deployment -> Operations       | Deployed, monitoring active, rollback tested                   |

Full template: [assets/implementation-plan-template.md](assets/implementation-plan-template.md)

## Requirements Decomposition

### From Vision to User Stories

```
Product Vision (SOW Section 3)
    |
    +-- Epic 1: [Major capability]
    |   +-- Feature 1.1: [Specific feature]
    |   |   +-- User Story 1.1.1: "As a [role], I want [action] so that [benefit]"
    |   |   |   +-- Acceptance Criteria: Given [context], When [action], Then [result]
    |   |   +-- User Story 1.1.2: ...
    |   +-- Feature 1.2: ...
    +-- Epic 2: ...
```

### Prioritization Frameworks

| Framework                  | Best For              | Method                                       |
| -------------------------- | --------------------- | -------------------------------------------- |
| **RICE**             | Feature backlogs      | (Reach x Impact x Confidence) / Effort       |
| **MoSCoW**           | MVP scoping           | Must / Should / Could / Won't                |
| **Kano**             | UX prioritization     | Basic / Performance / Delight classification |
| **Value vs. Effort** | Quick sprint planning | 2x2 matrix: high-value + low-effort first    |

### Acceptance Criteria Standards

Every story/task must have acceptance criteria that are:

- **Specific** — "Renders within 200ms" not "fast"
- **Testable** — Can be verified by running a command or inspecting output
- **Independent** — Each criterion verifiable on its own
- **Complete** — Cover happy path, edge cases, and error conditions

## AI-Integrated Project Planning

When the project involves AI/ML components, add these considerations:

- **AI Threat Modeling** (Phase 0): Assess agentic failure modes before architecture
- **Human-AI Collaboration Model**: What AI decides vs. what humans approve
- **Responsible AI Integration**: Bias monitoring, fairness validation, transparency
- **AI-Specific Testing**: Hallucination detection, drift monitoring, adversarial evaluation
- **Wrap, Don't Rewrite**: Expose existing tools via MCP; preserve working automation

## Integration with Other Extensions

- **Orchestrator agent**: Invokes this skill when decomposing complex tasks
- **execute-task skill**: Takes over at Phase 3 (EXECUTE) with the plan this skill produced
- **assessing-quality skill**: Provides quality framework referenced in Phase 6 (testing strategy)
- **designing-workflows skill**: Produces the workflow diagrams referenced in SOW Section 8
- **verifier agent**: Validates deliverables against acceptance criteria from this plan

## Full-Stack Sprint Coordination

When planning full-stack implementations, consider the dependency graph between layers:

| Pattern                                            | When to Use                              | Approach                                                         |
| -------------------------------------------------- | ---------------------------------------- | ---------------------------------------------------------------- |
| **API-first** (backend leads ~1 sprint)      | Data-heavy apps, complex business logic  | Backend builds endpoints -> frontend integrates with real APIs   |
| **Design-first** (frontend leads with mocks) | UX-critical apps, design-driven products | Frontend builds UI with mock data -> backend implements to match |
| **Contract-first** (parallel)                | Clear API contracts, experienced teams   | Both develop against shared API spec simultaneously              |

Let the project's actual architecture determine which pattern fits — don't default to
one approach for all projects.

## References

- `assets/sow-template.md` — Full SOW template
- `assets/implementation-plan-template.md` — Full hybrid PRD+SRD template
- CAB plugin `knowledge/reference/product-design-cycle.md` — Universal 7-phase lifecycle (conceptual framework, not prescriptive)
