---
id: filesystem-patterns
title: Filesystem State Patterns
category: operational-patterns/state-management
tags: [state, filesystem, notes, progress, cold-start, persistence, cross-session, git-tracking]
summary: Design patterns for filesystem-based state management — notes/ directory conventions, git-tracking policy, cold-start anchors, progress files with decision trails, and cross-session persistence strategies.
depends_on: [session-lifecycle, orchestration-framework]
related: [context-engineering, collaboration-patterns, worktree-workflows, git-foundation]
complexity: intermediate
last_updated: 2026-04-10
estimated_tokens: 1200
source: CAB-original
confidence: A
review_by: 2026-07-10
revision_note: "v3.1 — Added Git Tracking Policy section (LL-25). notes/ is now tracked by default with exclusion patterns for transient content. Multi-archetype justification: commit-local-only breaks for multi-machine/team/agent workflows."
---

# Filesystem State Patterns

## Core Principle

The filesystem is a persistent context layer that survives compaction and session boundaries. Context is ephemeral; files are permanent. Use them strategically.

---

## Git Tracking Policy

**Default**: `notes/` is **tracked by default**, not gitignored. State artifacts are first-class deliverables that must survive sessions, machines, branches, and collaborators.

### Multi-Archetype Justification

CAB serves multiple user archetypes. The tracking default must hold across all of them:

| Archetype | Collaboration Pattern | Commit-Local-Only Viable? | Requires Tracked `notes/`? |
|-----------|----------------------|---------------------------|----------------------------|
| Solo, single machine | Sequential | Yes (degenerate case) | Recommended (backup, history) |
| Solo, multi-machine | Sequential cross-device | No (needs sync) | Required |
| Small team (humans) | Parallel | No (needs sharing) | Required |
| Human + AI agents | Parallel concurrent | No (LL-17 contamination risk) | Required |
| Distributed OSS | Distributed | No | Required |

**Common denominator**: tracking `notes/` is the only policy that works for all five archetypes. Solo-single-machine workflows work fine under a tracked default — they just don't exercise the cross-machine/collaboration benefits.

### Alignment with Worktree Protocol

CAB's worktree recommendation (see [worktree-workflows.md](../multi-agent/worktree-workflows.md)) implies feat-branch-based code changes. State changes happen *during* agent work inside those worktrees, so state changes already happen on feat branches in the CC-recommended pattern. Tracking `notes/` formalizes this — keeping code changes and state changes on the same branch is a design integrity property that eliminates split-brain workflows.

### Track / Exclude Decision Matrix

| Content | Tracked? | Rationale |
|---------|---------|-----------|
| `notes/progress.md` | Yes | Live session state, bootstrap protocol, cross-session continuity |
| `notes/TODO.md` | Yes | Tactical task queue, append-only history |
| `notes/lessons-learned.md` | Yes | Compounding corrections, cross-project knowledge |
| `notes/current-task.md` | Yes | Cold-start anchor, PLAN phase artifact |
| `notes/impl-plan-*.md` | Yes | Strategic plans, reference for VERIFY phase |
| `notes/<audit>-*.md`/`.yaml` | Yes | Deliverables with traceable decision trails |
| `notes/scratch-*.md` | Excluded | Transient draft marker (ad-hoc) |
| `notes/draft-*.md` | Excluded | Transient draft marker (ad-hoc) |
| `notes/personal-*.md` | Excluded | Private content not for sharing |
| `notes/_drafts/` | Excluded | Organized drafts subdirectory |
| `notes/_archive/` | Excluded | Retroactive scrub escape hatch |

### `.gitignore` Recipe

```gitignore
# State management artifacts — TRACKED BY DEFAULT
# notes/ is intentionally NOT gitignored. Exclusions below are for transient,
# private, or retroactively-scrubbed content only.

# Ad-hoc exclusion patterns (draft markers)
notes/scratch-*.md
notes/draft-*.md
notes/personal-*.md

# Organized drafts subdirectory
notes/_drafts/

# Archive escape hatch (retroactive scrub)
notes/_archive/
```

### Pre-Push Review Protocol

Before pushing, CAB enforces a two-layer review:

1. **Hook layer (deterministic gate)** — `PreToolUse` hook on `Bash(git push*)` scans staged and recent `notes/` changes for draft markers: `WIP`, `DRAFT`, `PRIVATE`, `TODO:redact`, `NOCOMMIT`. Exit code 2 blocks the push if markers found.
2. **Skill layer (intelligent review)** — `pre-push-state-review` skill inspects flagged files semantically, suggests `_archive/` relocation for in-dev artifacts, and prompts the user to confirm publication intent.

The hook provides the deterministic gate; the skill provides the contextual review. Both layers together give reliability (hook catches accidents) and flexibility (skill handles judgment calls).

### Escape Hatches

| Scenario | Action |
|----------|--------|
| File should never be tracked | Name it with `scratch-`, `draft-`, or `personal-` prefix OR place in `notes/_drafts/` |
| File was committed but should be private | Move to `notes/_archive/` and commit the move. File becomes gitignored going forward. |
| Entire work-in-progress branch | Keep on feat branch, don't push until merged |
| Retroactive scrub of remote | `git filter-repo` — requires explicit user intent (not automated) |

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

## CC Memory Layer Alignment

CAB's state management operates **above** Claude Code's 7-layer internal memory system. Understanding the relationship prevents both duplication and false assumptions about what CC handles automatically.

### CC's Internal Layers (Reference)

CC's harness runs a 7-layer memory architecture: tool result storage (L1), microcompaction (L2), session memory (L3), full compaction (L4), auto memory extraction (L5), dreaming/consolidation (L6), and cross-agent communication (L7). L3 (`session-memory/<sessionId>.md`) and L5 (`~/.claude/projects/<path>/memory/`) are the layers most likely to be confused with CAB state files — but they serve different purposes.

### CAB vs CC Memory — Separation of Concerns

| Dimension | CC Internal Memory | CAB State Files |
|-----------|-------------------|----------------|
| **Author** | CC harness (automatic) | Human + agent (curated) |
| **Scope** | Session-bounded (L3) or path-scoped (L5) | Task-bounded and project-bounded |
| **Operation** | Compression (lossy summarization) | Curation (lossless semantic preservation) |
| **Update cadence** | Turn-level, forked agent | Subtask-level, main session |
| **Auto-memory exclusion** | Explicitly excludes CLAUDE.md content | IS the CLAUDE.md supplement — fills the gap CC auto-memory leaves |
| **Failure mode** | Silent summarization loss on compaction | Visible in git diff, human-reviewable |
| **Intent** | Fit more context in window | Survive session boundaries with full meaning intact |

**Design principle**: CAB state files exist **because CC's mechanical memory is insufficient for long-horizon semantic continuity**. Detailed curated summaries outperform compaction-based summarization for cross-session task resumption. CAB optimizes for *meaning preservation*, not *token efficiency*.

### Implications for State File Design

- **Don't shrink files to match CC memory budgets.** CC's MEMORY.md has hard limits (200 lines / 25KB) because it's an index. CAB's `progress.md`, `TODO.md`, `lessons-learned.md` are semantic artifacts and should be as detailed as needed. File size is not a primary optimization target — if bloat becomes a concern, archive to `_archive/` before sync rather than truncate.
- **Curate, don't summarize.** When closing a session, prefer detailed handoff summaries (like HydroCast's precedent) over terse compressions. Cross-session resumption reliability is worth the token cost.
- **Append-friendly where natural.** Cache preservation (CC's prompt cache has ~1 hour TTL) favors append-only patterns. CAB's `TODO.md` is already append-only. `progress.md` benefits from "newest session at top" when convenient — but this is guidance, not prescription. Don't let cache optimization warp the semantic structure.
- **Current-task.md is the exception.** This file has a hard <100 line target because it's the cold-start anchor. Concise by design. Everything else remains agentically flexible.

### Lessons-Referenced Protocols (Always-Load, Architecturally-Enforced)

`notes/lessons-learned.md` is **not optional context**. CAB treats lessons as hard constraints on the protocols they govern, not passive reference documentation. The pattern:

1. **Bootstrap protocol loads lessons-learned alongside progress.md and TODO.md** — never skip.
2. **Protocols, skills, and agents reference LL IDs explicitly** where their behavior is governed by a past correction. Example: the executing-tasks skill should reference LL-12 ("never delegate file writes to background agents") directly in its delegation step, not as a footnote.
3. **New LL entries trigger protocol updates** — adding an LL is the *start* of integration, not the end. The corresponding protocol/skill/agent must cite the LL or mechanically prevent the failure mode.
4. **Re-read before any decision the LL governs** (reinforcing LL-12, LL-20). The value of LLs is proportional to how structurally they're woven into the workflow, not how thoroughly they're documented.

This is the antidote to the LL-12/LL-17/LL-20 recurrence pattern: passive documentation doesn't prevent recurrence; structural integration does.

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
