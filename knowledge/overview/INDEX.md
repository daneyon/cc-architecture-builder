---
type: index
scope: category
category: overview
file_count: 2
last_updated: 2026-02-25
version: 0.6.0
---

# Overview Index

> Foundational understanding of Claude Code architecture

## Files

| File | Summary | Complexity |
|------|---------|------------|
| `executive-summary.md` | Two-schema architecture, core principles, visual overview | foundational |
| `architecture-philosophy.md` | Memory hierarchy, invocation patterns, distribution strategy | foundational |

## Reading Order

1. **executive-summary.md** — Start here for high-level understanding
2. **architecture-philosophy.md** — Deeper principles and patterns

For orchestration and workflow patterns, proceed to `operational-patterns/orchestration-framework.md` after these foundational files.

## Key Concepts Introduced

- Two-schema separation (global vs project)
- 5-tier memory hierarchy (Enterprise Policy → Project Memory → Project Rules → User Memory → Project Local)
- Invocation patterns (automatic, model-invoked, user-invoked, event-driven)
- Progressive disclosure
- Distribution via @imports
