---
id: filesystem-patterns
title: Filesystem State Patterns
category: operational-patterns/state-management
tags: [state, filesystem, notes, progress, cold-start, persistence, cross-session, git-tracking]
summary: Design patterns for filesystem-based state management — notes/ directory conventions, git-tracking policy, cold-start anchors, progress files with decision trails, and cross-session persistence strategies.
depends_on: [session-lifecycle, orchestration-framework]
related: [context-engineering, collaboration-patterns, worktree-workflows, git-foundation]
complexity: intermediate
last_updated: 2026-04-11
estimated_tokens: 1400
source: CAB-original
confidence: A
review_by: 2026-07-11
revision_note: "v3.3 — Session 32 Pivots 1-2: (1) Flat `notes/` directory policy (no subfolders except `_archive/`); (2) Cheap-to-Expensive Bootstrap Cascade now 3-file (LL excluded from always-load, read on-demand at phase transitions). CC Memory Layer Alignment softened accordingly. Lessons Learned Persistence field list simplified (Status feature removed as unvalidated). v3.2 introduced tense hygiene (LL-26); v3.1 introduced tracked-by-default (LL-25)."
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

## Flat `notes/` Directory Policy

**Rule**: `notes/` is a **flat directory** for all active state artifacts. Only `notes/_archive/` (cold storage) is permitted as a subdirectory. No other nesting — no `references/`, `metrics/`, `qa/`, or per-task folders.

**Rationale**: subfolder proliferation creates multiple path domains the agent must reason about during bootstrap and grep. Flat = one path prefix, one grep root, one mental model. The Session 32 flatten exposed the failure mode: orchestration reflexively referenced stale `notes/references/...` paths even after files were moved, because subfolder paths embedded in historical documentation drift out of sync with the filesystem.

**Archival**: when material becomes reference-only or superseded, move to `notes/_archive/`. The archive may organize internally — it is cold storage, never bootstrapped. **Enforcement** is convention only: author discipline + periodic `ls notes/` sanity check.

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

### Lightweight: Notes Directory (Flat)

```
notes/
├── current-task.md          # Cold-start anchor (L1, hard-gated <100 lines)
├── progress.md              # Session state + historical narrative (L2, partial-read)
├── TODO.md                  # Task queue (L3, partial-read)
├── lessons-learned.md       # Compounding corrections (on-demand only, excluded from bootstrap)
├── impl-plan-<task>.md      # Strategic plans for active tasks
├── <topic-specific>.md      # As needed — flat, no subfolders
└── _archive/                # Cold storage for superseded material (not bootstrapped)
```

Bootstrap protocol reads the 3-file cascade (L1/L2/L3). LLs are consulted on-demand at phase transitions. See `bootstrap-read-pattern.md` for the full cascade specification.

### Medium / Full scales

For long-running autonomous tasks or multi-phase lifecycle management, add structured machine-readable state alongside `notes/`: a `features.json` (per-feature boolean gates, agent-editable) for task tracking, or a `project-state.yaml` (lifecycle phase, active agents, completion criteria, human-managed) for strategic position. **JSON for agent-editable, YAML for human-managed** — models introduce fewer formatting errors in JSON.

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

### Lessons-Referenced Protocols (Structurally Integrated, Not Always-Loaded)

`notes/lessons-learned.md` is **reference data**, not operational state. CAB treats lessons as hard constraints woven into the protocols they govern, but does **not** load the file at every cold-start. The Session 32 Pivot 1 correction recognized that reading the LL file every session was a category error — the v3.2 "always-load" framing was aspirational and generated the 41K bootstrap regression without actually preventing the LL-12/LL-17/LL-20 recurrence pattern (structural integration does that, not rereading).

The pattern:

1. **Structural weaving is the enforcement mechanism** — protocols, skills, agents, and hooks reference LL IDs explicitly where their behavior is governed by a past correction. Example: the `executing-tasks` skill references LL-12 ("never delegate file writes to background agents") directly in its delegation step. The enforcement lives in the skill, not in a cold-start re-read.
2. **Classification drives cadence** — each LL carries a Classification (`INTEGRATED` / `ACTIVE` / `ADVISORY` / `ARCHIVED`). `INTEGRATED` LLs are woven into a skill/hook/rule and don't need operational re-reading. `ACTIVE` LLs lack structural weaving and should be re-read at phase transitions until integrated.
3. **New LL entries trigger protocol updates** — adding an LL is the *start* of integration, not the end. The corresponding protocol/skill/agent must cite the LL or mechanically prevent the failure mode. Until weaving exists, the entry's Classification is `ACTIVE` (not `INTEGRATED`).
4. **On-demand reads at phase transitions** — at major phase boundaries in a task, scan the LL Classification column for `ACTIVE` entries touching the next phase's domain. Grep specific LL IDs when a decision matches their governed domain. See `bootstrap-read-pattern.md §When to Read lessons-learned.md`.

This is the antidote to the LL-12/LL-17/LL-20 recurrence pattern: passive documentation doesn't prevent recurrence; structural integration does. Reading the file every session does neither.

---

## State File Tense Hygiene (LL-26)

State files committed alongside work become **stale the instant the work-commit lands** if they describe the work in future/pending tense. Session 24 tripped this: state said `"ready for commit + session close"` — accurate at write time, stale the moment `302f872` landed. Next session reads stale context.

### Forbidden vs Approved Status-Line Patterns

| | Pattern |
|---|---|
| **Forbidden** | `pending commit`, `ready for commit`, `awaiting commit`, `will commit`, `EXECUTED ✅ — ready for...` |
| **Approved** | `executed in <hash>`, `committed in <hash>`, `landed in <hash>`, `executed YYYY-MM-DD` |

The prohibition applies to **status-line contexts only** (`**Status**:`, `**Phase**:`, `**Gate**:`). Descriptive prose, body text, and code-fenced examples may reference the forbidden phrases freely — that's how this very document does it. The anchored-regex enforcement below distinguishes the two.

### Two-Commit Session Close Pattern (DD-1)

1. **Work commit** lands first with a descriptive message for the substantive change.
2. **Refresh state files** in past tense, citing the work-commit hash (`"Executed in abc1234"`).
3. **State refresh commit** lands as `chore(session-NN): refresh state post-<hash>`.

Token cost ~130/session (0.065% budget) = negligible. A tense-neutral single-commit is a lightweight fallback for mid-session state touches only.

### Enforcement Layers (Architecturally Woven)

- `skills/session-close/SKILL.md` Step 4 — two-phase close protocol
- `skills/executing-tasks/SKILL.md` Phase 5 — requires post-commit refresh + second commit
- `hooks/scripts/pre-push-state-review.sh` — anchored status-line regex blocks stale push
- Commit-per-phase cadence (DD-4) — recommended for multi-phase tasks

See LL-26 in `notes/lessons-learned.md` for full root cause + corrective protocol.

---

## Lessons Learned Persistence

`notes/lessons-learned.md` captures operational insights that compound across sessions. The file is **excluded from bootstrap** and consulted on-demand at phase transitions or when a decision touches a specific LL's domain.

### Schema

| Field | Purpose |
|-------|---------|
| ID | Sequential (`LL-01`, `LL-02`, …) |
| Date | When discovered |
| Category | `ops`, `arch`, `ctx`, `proc`, `tool` |
| Lesson | One-line summary |
| Classification | `INTEGRATED`, `ACTIVE`, `ADVISORY`, `ARCHIVED` (see below) |
| Priority | `P0`, `P1`, `P2` (only for `ACTIVE` entries; otherwise `—`) |
| Detail | Actionable explanation |

### Classification schema

| Value | Meaning | Action Implied |
|-------|---------|----------------|
| `INTEGRATED` | Structurally woven into skill/hook/rule/KB; recurrence is programmatically prevented or canonically documented | None — verification only (periodic re-audit) |
| `ACTIVE` | Load-bearing for current work but NOT yet woven into enforcement; recurrence risk exists | Queue for integration work at priority `P0`/`P1`/`P2` |
| `ADVISORY` | Wisdom, heuristic, or platform fact that doesn't need enforcement; low recurrence risk | Periodic review only |
| `ARCHIVED` | Superseded by a better pattern, fixed at root, or no longer applicable to current architecture | None — historical reference |

**Integration flow**: new LL enters as `ACTIVE-P0/P1/P2` → structural weaving lands in a skill/hook/rule → re-classify to `INTEGRATED` → if later superseded, re-classify to `ARCHIVED`. Re-prioritization and re-scoring happen at major task phase transitions or during periodic audit, not continuously.

**Schema heritage**: modeled on the `auditing-workspace` classification-schema pattern (MISSING/STALE/ENHANCEMENT/CURRENT + severity), adapted to the LL lifecycle. Deliberately kept to two dimensions (Classification + Priority) for operational simplicity.

---

## State-Management Protocol Reversibility Inventory (UXL-019)

**Principle** (per Session 27 user directive): every state-management protocol
addition must be individually revertable. This inventory maps each load-bearing
state-mgmt protocol to the commit that introduced it + the revert command, so
rollback is a one-liner if any layer proves counterproductive in practice.

Append new rows as new protocols land. Remove or update rows only when a
protocol is formally superseded (not just evolved).

| Protocol | Landed commit | Revert command | Notes |
|---|---|---|---|
| LL-25 — notes/ tracked-by-default + pre-push draft-marker gate | `302f872` | `git revert 302f872` | Introduced `.gitignore` adjustments + `hooks/scripts/pre-push-state-review.sh` scaffold. Tracked-by-default was the architectural shift. |
| LL-26 — State-file tense hygiene (status-line anchored regex) | `62bf4a9` | `git revert 62bf4a9` | Refined pre-push regex to require status-line anchoring on tense matches. Subsequent refinement: UXL-024 (backtick exclusion). |
| LL-27 — Plugin↔global shadow detection (pre-incident fix) | `436ffbd` | `git revert 436ffbd` | Initial LL-27 landing. Enforcement layer expanded in UXL-011 (sync-check shadow scan) + UXL-012 (agent-resolution KB) + UXL-013 (audit fold-in). |
| LL-29 — Bootstrap token efficiency restoration (3-file cascade + T1 boundary + L1 hard gate) | `8dfef75..572988e` (P1..P5) | `git revert 572988e^..572988e` (or per-phase reverts) | Multi-commit span across Sessions 28-32. Each phase independently revertable per Session 27 directive. See `notes/impl-plan-bootstrap-efficiency-2026-04-11.md`. |
| UXL-011 — /sync-check shadow detection | `2185da9` | `git revert 2185da9` | Adds shadow-scan step to sync-check command. Declarative-command edit only; no new backing script. |
| UXL-012 — agent-resolution.md KB card (LL-27 canonical spec) | `a9796fa` | `git revert a9796fa` | Reference documentation; no runtime behavior. Revert = remove card + INDEX.md delta. |
| UXL-013 — Shadow scan folded into /validate --cab-audit | `e985760` | `git revert e985760` | Adds criterion 15 to agent-standards.md + shadow-scan step to auditing-workspace SKILL.md. |
| UXL-018 — Bootstrap token cost tracking (soft signal framing) | `d1a0b23` | `git revert d1a0b23` | progress.md header convention + soft-signal philosophy in bootstrap-read-pattern.md. Signal, not prescription (LL-29 alignment). |
| UXL-022 — CC memory layer alignment KB card | `7db3a2a` | `git revert 7db3a2a` | Reference documentation; no runtime behavior. |
| UXL-024 — Pre-push backtick-wrapped marker exclusion | `430fe64` | `git revert 430fe64` | Second-pass filter on draft-marker regex. LL-26 refinement. |
| UXL-032 — Agent memory: field adoption (3 CAB agents) | `600d9ba` | `git revert 600d9ba` | Frontmatter-only change on architecture-advisor, verifier, project-integrator. Orchestrator intentionally skipped. |
| UXL-033 — uxl-update.py helper + active-top sort | `008f90e` | `git revert 008f90e` | Adds `hooks/scripts/uxl-update.py` + applies sort to pass-1 CSV. Future resolutions use the helper; reverting removes the helper but not the CSV changes from other commits. |
| LL-28 candidate (event-triggered state-write protocol) | *TBD (Wave 5)* | *TBD* | Per Session 27 directive: "at least one survived dying-session recovery test before hard-coding." Not yet shipped. |

**Append convention**: when a new state-mgmt protocol lands, add its row here in the same commit that introduces it. Include `[UXL-019]` in the commit message suffix when doing so, so the post-commit hook (once shipped) can verify the inventory stays current.

**Scope note**: this inventory tracks *state-management* protocol additions specifically. Other protocol categories (hooks, skills, rules) don't need revertability tracking at this granularity because their failure modes are more bounded. State-mgmt protocols compound across sessions, so a broken protocol can poison multiple downstream tasks before it's caught.

## See Also

- [Session Lifecycle](session-lifecycle.md) — When to compact vs. fresh session
- [Context Engineering](context-engineering.md) — Reducing context waste
- [Orchestration Framework](../orchestration/framework.md) — Task execution protocol (commit step)
