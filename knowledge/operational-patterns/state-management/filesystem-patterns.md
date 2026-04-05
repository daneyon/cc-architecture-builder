---
id: filesystem-patterns
title: Filesystem State Patterns
category: operational-patterns/state-management
tags: [state, filesystem, notes, progress, cold-start, persistence, cross-session]
summary: Design patterns for filesystem-based state management — notes/ directory conventions, cold-start anchors, progress files with decision trails, and cross-session persistence strategies.
depends_on: [session-lifecycle, orchestration-framework]
related: [context-engineering, collaboration-patterns]
complexity: intermediate
last_updated: 2026-04-05
estimated_tokens: 800
confidence: A
review_by: 2026-07-05
revision_note: "v3.0 — Extracted from session-management.md. Enhanced with three-tier state hierarchy and CAB-specific patterns."
---

# Filesystem State Patterns

## Core Principle

The filesystem is a persistent context layer that survives compaction and session boundaries. Context is ephemeral; files are permanent. Use them strategically.

---

## Three-Tier State Hierarchy

CAB uses a deliberate state hierarchy where each tier serves a different audience and lifecycle:

| Tier | File | Purpose | Lifecycle |
|------|------|---------|-----------|
| **1. Strategic** | Implementation plan (`.claude/plans/`) | Big picture, phased strategy | Rarely changes |
| **2. Tactical** | `notes/TODO.md` | Incrementalized tasks, prioritized | Never delete items; reorder pending to top |
| **3. Operational** | `notes/progress.md` | Live session state, bootstrap | Can compact/rewrite between sessions |

**Rule**: Only Tier 3 (progress.md) warrants deletions. Tier 2 (TODO.md) preserves history — completed items move to archive sections, not removed. Tier 1 only changes on strategic pivots.

---

## Cold-Start Anchor (`notes/current-task.md`)

The single document an agent reads to re-orient after compaction or fresh session. Structure:

- **Current task and phase** (1 line)
- **Active blockers** with owner and status (table)
- **Key file pointers** — 3-5 files most relevant to current work
- **User directives carried forward** — strategic constraints stated once, easy to lose during compaction

Target: **<100 lines**. If it grows beyond that, detail belongs in `progress.md` or domain-specific files.

---

## Progress with Decision Trail (`notes/progress.md`)

Tracks not just task completion but the *decisions* that shaped the work. Decisions are the most compaction-lossy artifact — stated once, influence all downstream work, vanish when context compresses.

**Recommended sections**:

| Section | Purpose |
|---------|---------|
| **Session state** | Last session date, branch, commit, context health |
| **Current position** | Active gate, next action, pending items |
| **Bootstrap protocol** | Numbered steps to re-orient from cold start |
| **Key user directives** | Persistent constraints (survive across sessions) |
| **Artifact map** | Location of all relevant state files |

**Separation principle**: `current-task.md` answers "where am I right now?" `progress.md` answers "what's the full picture?" Both survive compaction, but only the anchor needs reading on every cold start.

---

## Filesystem-as-Context Patterns

| Pattern | File | When |
|---------|------|------|
| **Plan persistence** | `notes/current-task.md` | Before multi-step work |
| **Tool output offloading** | `notes/scratch.md` or `notes/<topic>.md` | Tool results >500 lines |
| **Progress tracking** | `notes/progress.md` | After each subtask completion |
| **State snapshots** | `notes/` timestamped files | Before `/compact` on complex sessions |
| **Lessons learned** | `notes/lessons-learned.md` | After correctable errors |

**Key pattern**: Write plans and large analysis results to files *before* they're needed. This keeps conversation context lean (high signal-to-noise) while preserving full detail for later retrieval.

---

## Cross-Session Persistence Strategies

Scaled to project complexity:

### Lightweight: Notes Directory

```
notes/
├── progress.md              # Session state + bootstrap
├── current-task.md          # Active task anchor
├── lessons-learned.md       # Compounding corrections
└── <topic-specific>.md      # As needed
```

In CLAUDE.md: reference via `@notes/progress.md` or read at session start via bootstrap protocol.

### Medium: Progress + Feature List

For long-running autonomous tasks:

- `notes/progress.md` — Free-form progress notes
- `features.json` — Structured tracking with `passes: boolean` per feature

```json
{
  "features": [
    {"id": "auth-login", "description": "User login with JWT", "passes": true},
    {"id": "auth-register", "description": "Registration flow", "passes": false}
  ]
}
```

### Full: Project State YAML

For multi-phase lifecycle management:

- `project-state.yaml` — Lifecycle phase, active agents, completion criteria
- `notes/` directory for operational state
- Git commits for permanent checkpoints

**JSON for agent-editable, YAML for human-managed**: Models introduce fewer formatting errors in JSON. Use JSON for files agents modify (feature lists, test results); YAML for files humans primarily maintain (project state, configuration).

---

## Lessons Learned Persistence

`notes/lessons-learned.md` captures operational insights that compound across sessions:

| Field | Purpose |
|-------|---------|
| ID | Sequential (LL-01, LL-02, ...) |
| Date | When discovered |
| Category | `ops`, `arch`, `ctx`, `proc`, `tool` |
| Lesson | One-line summary |
| Detail | Actionable explanation |
| Status | `active`, `integrated`, `superseded` |

**Integration flow**: Active lessons inform current work → when integrated into CLAUDE.md or KB files, status changes to `integrated` → superseded lessons archived when replaced by better understanding.

## See Also

- [Session Lifecycle](session-lifecycle.md) — When to compact vs. fresh session
- [Context Engineering](context-engineering.md) — Reducing context waste
- [Orchestration Framework](../orchestration/framework.md) — Task execution protocol (commit step)
