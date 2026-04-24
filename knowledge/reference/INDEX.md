---
type: index
scope: reference
file_count: 7
last_updated: 2026-04-22
---

# Reference Materials Index

> Generalized conceptual frameworks for project planning, team formation,
> lifecycle management, prioritization, and UX evaluation. These are **advisory
> references** — not prescriptive doctrine. Agents and skills read these
> on-demand when relevant to the current task.

## Files

| File | Summary |
|------|---------|
| [product-design-cycle.md](product-design-cycle.md) | Universal 7-phase product lifecycle (Discovery → Operations) with sub-processes, deliverables, discipline mapping, phase gates, and CC extension mapping. Synthesizes Double Diamond, SDLC, Lean Startup, Design Thinking, and Stage-Gate. |
| [a-team-database.yaml](a-team-database.yaml) | Machine-parseable roster of 22 product team roles with CC extension mapping, scaling tiers (solo → enterprise), phase participation, and key deliverables per role. Use for team formation suggestions during project initialization. |
| [requirements-doc-guide.md](requirements-doc-guide.md) | Deep dive on Market / Product / Software Requirements Documents (MRD/PRD/SRD) and hybrid Startup Requirement Document approach. Consulted during plan-implementation scoping for early-stage product work. |
| [visualization-workflow.md](visualization-workflow.md) | Hybrid visualization design workflow (Yau + Cleveland-McGill + Munzner nested model). Consulted when planning dashboards, charts, or visualization-heavy deliverables. |
| [workflow-processflow.md](workflow-processflow.md) | Comparative reference distinguishing workflow diagrams (role-centric sequence) from process flow diagrams (operational detail with decision points). Consulted when selecting diagramming approach. |
| [prioritization-frameworks.md](prioritization-frameworks.md) | Comparative reference on 8 prioritization frameworks (RICE, MoSCoW, Kano, Value-vs-Effort, WSJF, ICE, Eisenhower, Stack Ranking) with tiered-application stack for log-time / triage-time / promotion-time usage. |
| [ux-testing-agentic-os.md](ux-testing-agentic-os.md) | UX-testing protocol for agentic OS platforms — couples traditional UX evaluation (Nielsen, WCAG, ISO 9241-210, ISO-25010) with LLM-evaluation practice (eval harness, observability, context-degradation awareness). Surface-to-framework mapping for the UX-log-tracker. |

## How These Are Used

- **`/cab:integrate-existing` command**: Reads `a-team-database.yaml` to suggest
  domain-appropriate agents and skills based on project characteristics, team
  size, and complexity.
- **`/cab:new-project` command**: References `product-design-cycle.md` to help
  users identify which lifecycle phases their project will traverse.
- **`plan-implementation` skill**: Uses `product-design-cycle.md`,
  `requirements-doc-guide.md`, `visualization-workflow.md`, and
  `workflow-processflow.md` as optional conceptual frameworks when structuring
  SOWs and implementation plans.
- **UX-log-tracker** (`notes/ux-log-*.csv` + `notes/ux-log-guide.md`):
  `prioritization-frameworks.md` and `ux-testing-agentic-os.md` are the
  authoritative framework references the tracker's `framework_anchor`,
  `kano`, `rice_score`, and `moscow` columns anchor to.

## Important: These Are Conceptual References

These documents provide a comprehensive menu of *possibilities*, not a
mandatory checklist. A solo developer building a Python script doesn't need
all 22 roles or all 7 phases. The orchestrator and advisory agents use these
to inform suggestions, adapting to the user's actual context and scale.

The ≤300 line kb-conventions rule is carved out for this folder
(see `.claude/rules/kb-conventions.md`) — reference documents are consulted
on-demand and may preserve cohesive depth where splits would fracture
content.
