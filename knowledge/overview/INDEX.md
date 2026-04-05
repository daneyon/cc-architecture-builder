---
type: index
scope: category
category: overview
file_count: 3
last_updated: 2026-04-05
---

# Overview Index

> Foundational understanding of Claude Code architecture

## Files

| File | Summary | Complexity |
|------|---------|------------|
| `executive-summary.md` | Two-schema architecture, core principles, visual overview | foundational |
| `architecture-philosophy.md` | Intermediary wrapper architecture, 4-scope memory, seed instructions, invocation patterns | foundational |
| `design-principles.md` | 9 core design tenets: verification-first, progressive disclosure, token efficiency | foundational |

## Reading Order

1. **executive-summary.md** — Start here for high-level understanding
2. **architecture-philosophy.md** — Deeper principles and patterns
3. **design-principles.md** — Design tenets that guide all CAB decisions

For orchestration and workflow patterns, proceed to `operational-patterns/orchestration/framework.md` after these foundational files.

## Key Concepts Introduced

- Two-schema separation (global vs project)
- 4-scope memory hierarchy (Managed → Project → User → Local)
- Intermediary wrapper architecture (extend CC, never duplicate)
- Invocation patterns (automatic, model-invoked, user-invoked, event-driven)
- Seed instruction design (durable guidance surviving memory consolidation)
- Progressive disclosure
- Distribution via @imports
