---
type: index
scope: reference
file_count: 2
last_updated: 2026-03-25
---

# Reference Materials Index

> Generalized conceptual frameworks for project planning, team formation, and
> lifecycle management. These are **advisory references** — not prescriptive doctrine.
> Agents and skills read these on-demand when relevant to the current task.

## Files

| File | Location | Summary |
|------|----------|---------|
| [Product Design Cycle](../../docs/_internal/product-design-a-team/product-design-cycle.md) | docs/_internal/ | Universal 7-phase product lifecycle (Discovery → Operations) with sub-processes, deliverables, discipline mapping, phase gates, and CC extension mapping. Synthesizes Double Diamond, SDLC, Lean Startup, Design Thinking, and Stage-Gate. |
| [A-Team Database](../../docs/_internal/product-design-a-team/a-team-database.yaml) | docs/_internal/ | Machine-parseable roster of 22 product team roles with CC extension mapping, scaling tiers (solo → enterprise), phase participation, and key deliverables per role. Use for team formation suggestions during project initialization. |

## How These Are Used

- **`/integrate-existing` command**: Reads a-team-database to suggest domain-appropriate
  agents and skills based on project characteristics, team size, and complexity.
- **`/new-project` command**: References product-design-cycle to help users identify
  which lifecycle phases their project will traverse.
- **`planning-implementation` skill**: Uses product-design-cycle as an optional
  conceptual framework when structuring SOWs and implementation plans.

## Important: These Are Conceptual References

These documents provide a comprehensive menu of *possibilities*, not a mandatory
checklist. A solo developer building a Python script doesn't need all 22 roles or
all 7 phases. The orchestrator and advisory agents use these to inform suggestions,
adapting to the user's actual context and scale.
