---
id: bootstrap-read-pattern
title: Bootstrap Read Pattern — Cheap-to-Expensive Partial-Read Cascade
category: operational-patterns/state-management
tags: [bootstrap, cold-start, partial-read, cascade, token-efficiency, state, LL-25, LL-28]
summary: How to cold-start a CAB session with a bounded token budget by reading a prefix of each state file under a 3-file cascade, escalating to full reads only when a specific decision demands the tail content. Lessons-learned is excluded from bootstrap and read on-demand at phase transitions.
depends_on: [filesystem-patterns, session-lifecycle]
related: [context-engineering, orchestration-framework]
complexity: intermediate
last_updated: 2026-04-11
estimated_tokens: 1300
source: CAB-original (impl-plan-bootstrap-efficiency-2026-04-11.md, P3/P4)
confidence: A
review_by: 2026-07-11
revision_note: "v1.1 — Session 32 Pivot 1: `lessons-learned.md` is excluded from bootstrap entirely. 4-layer cascade reduced to 3-layer. Density-bottleneck section removed (no longer applicable). LL reads are on-demand at phase transitions, not at every cold-start. v1.0 (P3, Session 31) introduced the 4-layer cascade under LL-as-L4."
---

# Bootstrap Read Pattern

## Core Principle

**File size, bootstrap read size, and bootstrap-necessity are three separable variables.** A state file can be large on disk (durable, semantically preserved), read partially at cold-start (bounded cost), AND — critically — not read at cold-start at all if it is reference data rather than operational state. Fix the *read pattern* and the *file list*, not the *file size*.

This pattern exists because LL-25/26/27/28 correctly optimized state files for semantic preservation — but without counter-pressure for cold-start compactness, the standardized "read all 4 files in full" bootstrap regressed from ~30K tokens (pre-LL-25) to ~40K tokens (post-LL-28) in ~1 week. The Session 32 Pivot 1 correction surfaced a deeper category error in the original design: `lessons-learned.md` is *reference data*, not *operational state*, and had no business being in the always-loaded tier.

---

## The Cheap-to-Expensive Cascade (3-File)

Each layer gates the next. If Layer N gives you what you need, you never touch Layer N+1.

| Layer | File | Bootstrap Read | Budget | Rationale |
|-------|------|----------------|--------|-----------|
| **L1** | `notes/current-task.md` | Full read | ≤100 lines (hard gate) | Cold-start anchor; pointer to active task + phase status + directives. Size-enforced by `hooks/scripts/enforce-current-task-budget.sh`. |
| **L2** | `notes/progress.md` | `Read(path, limit=100)` | ~100 lines of top section | Current Position (latest session state, next-action queue) sits above a `<!-- T1:BOUNDARY -->` marker; historical narrative flows below. |
| **L3** | `notes/TODO.md` | `Read(path, limit=80)` | ~80 lines of top section | Top Priorities (P0/P1) above the boundary; full backlog below. |

**Excluded from bootstrap**: `notes/lessons-learned.md`. LLs are reference data that describe hard-won operational constraints; they change every few weeks at most. Reading them every session trades daily token cost for marginal cross-session coherence. Instead, they are consulted **on-demand at phase transitions** or **when a specific decision touches their domain** — see §When to Read `lessons-learned.md` below.

**Per-file budget is per-file convention, not per-file enforcement.** Only L1 has a hard hook gate. L2/L3 rely on the T1 boundary marker convention being maintained by authors during normal state-writing.

---

## How to Invoke at Cold-Start

```
Read(notes/current-task.md)                        # full file, ≤100 lines hard cap
Read(notes/progress.md, limit=100)                 # T1 section only
Read(notes/TODO.md, limit=80)                      # T1 section only
```

Expected cost under this pattern: **~7-8K tokens** measured by `hooks/scripts/bootstrap-cost.sh` (vs. ~40K for the pre-fix "read all 4 files in full" protocol). See `notes/bootstrap-cost-log.md` for the current measurement timeseries.

---

## When to Read `lessons-learned.md` (On-Demand)

LLs are **not loaded by default**. Read them — or grep specific entries — when:

| Trigger | Read Pattern |
|---------|--------------|
| Phase transition in a multi-phase task (P1 → P2, etc.) | Full read once, scan the Classification column for any `ACTIVE-P0` or `PENDING` entries touching the next phase's domain |
| Current decision is about delegation, agent selection, or background-vs-foreground choice | Grep for `LL-02`, `LL-08`, `LL-12` (delegation LLs) |
| Current decision is about state files, tracking, or commit flow | Grep for `LL-25`, `LL-26`, `LL-27`, `LL-28` (state-mgmt LLs) |
| Current decision is about plugins, frontmatter, or CC schema | Grep for `LL-15`, `LL-16`, `LL-21`, `LL-23`, `LL-24` (schema LLs) |
| Periodic audit — re-scoring and re-prioritizing Classification states | Full read, re-evaluate each entry's `WOVEN` / `ACTIVE` / `ADVISORY` / `ARCHIVED` status |
| Drafting a new LL entry after a correctable error | Full read to check for duplicates / related entries before appending |

The cadence is reader-determined, not protocol-mandated. The original LL-25 framing ("lessons-referenced protocols, always-load") was aspirational — in practice, structurally weaving LLs into the skills/hooks/rules that govern their domains is a stronger guarantee than rereading the file every cold-start.

---

## T1 Boundary Marker Convention

Every state file beyond `current-task.md` uses an HTML comment as a structural boundary:

```markdown
## Current Position           ← T1 top section (load-bearing for bootstrap)
...latest session state...

<!-- T1:BOUNDARY -->          ← grep-visible, markdown-invisible

## Historical Narrative       ← T2 tail (load on-demand only)
...prior session narrative...
```

**Properties**:
- **Invisible in rendered markdown** — HTML comments don't affect readers
- **Greppable for tooling** — audit scripts can `grep -n 'T1:BOUNDARY'` to find the split
- **Reversible** — moving a section across the boundary is a pure-text edit, no schema change
- **No enforcement** — authors are trusted to place it correctly; measurement (`bootstrap-cost.sh`) catches drift

See P2 of `notes/impl-plan-bootstrap-efficiency-2026-04-11.md` for the original boundary-marker rollout.

---

## Escalation to Full Read

Partial reads are the *default*. Escalate to full reads when:

| Trigger | Action |
|---------|--------|
| L1 pointer references a section of `progress.md` outside the T1 window | Full read `progress.md` |
| New task planning requires full backlog visibility | Full read `TODO.md` |
| Any of the on-demand triggers in §When to Read `lessons-learned.md` fires | Read or grep `lessons-learned.md` |
| Recovering from abnormal termination (`Prompt is too long`, force-compact, crash) | Grep the CC session JSONL archive at `~/.claude/projects/<slug>/*.jsonl` *before* attempting any state-file re-read (LL-28 fallback-recovery protocol) |

**Escalation is cheap because it's targeted**: full-file reads on demand cost the same as always, but you pay them once when needed instead of every session.

---

## Enforcement Surface

### Hard gate (enforced)

- **L1 budget** — `hooks/scripts/enforce-current-task-budget.sh` blocks any commit that leaves `notes/current-task.md` at 101+ lines. Dual-mode:
  - **CC PreToolUse** — auto-distributed via `hooks/hooks.json`. Catches Claude-invoked commits. Filters on `git commit` regex.
  - **Git native pre-commit** — install per-clone via `.git/hooks/pre-commit` shim that `exec`s the source script. Catches manual terminal commits. Not plugin-distributed — each clone installs locally.

Install the git shim once per clone:

```bash
cat > .git/hooks/pre-commit <<'EOF'
#!/usr/bin/env bash
set -e
repo_root=$(git rev-parse --show-toplevel)
exec "$repo_root/hooks/scripts/enforce-current-task-budget.sh"
EOF
chmod +x .git/hooks/pre-commit
```

### Soft gates (convention only)

- **L2/L3 top-section placement** — no hook. Maintained by authors. Drift is caught by `hooks/scripts/bootstrap-cost.sh` run as a periodic measurement, not a commit gate.
- **LL Classification re-scoring** — not hook-enforced. A periodic audit protocol (to be defined) re-evaluates entries; in the interim, audit is an advisory practice performed at major phase transitions.

---

## Why This Works

- **Prompt cache friendly** — T1 sections are at the top of each file (newest content above older) so cache hits carry across turns (LL-10 / Finding 1 precedent).
- **Semantic preservation invariant** — no content is deleted. The boundary marker is purely a placement convention; LL exclusion from bootstrap does not remove LLs from the repo. LL-25's "tracked by default" guarantee holds byte-for-byte.
- **Agentic flexibility preserved** — files beyond L1 can grow without limit. The read pattern is bounded, not the write pattern.
- **Classification over cadence** — LLs are partitioned by bootstrap-necessity (included vs excluded), not by read-frequency quota. The partition is a structural decision, not a runtime rate limit.
- **Measurement-driven** — `bootstrap-cost.sh` makes drift visible before it compounds. The instrumentation *is* the compensating control for the soft gates.

---

## Common Failure Modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| Author writes new session narrative at the *tail* of `progress.md` | L2 partial read misses the latest session state | Rewrite top-section convention: append to "Current Position", migrate old section below boundary |
| Boundary marker is deleted in a refactor | Partial reads load unbounded prefix | Re-add marker; `bootstrap-cost.sh` will show the token cost spike |
| `current-task.md` grows past 100 lines | Hook blocks commit | Move verbose task detail into the impl-plan file (the real session-transfer artifact — see `notes/session-28-recovery-2026-04-11.md` Part 3) |
| Assistant forgets LL is excluded and bootstraps with `Read(lessons-learned.md, ...)` | Reverts to 4-file cascade, partial savings only | Re-anchor via `CLAUDE.md §Bootstrap Protocol`; the canonical 3-file invocation is the source of truth |
| Post-compaction session forgets the cold-start protocol | Reads all files in full again | Re-anchor via `CLAUDE.md §Bootstrap Protocol` (specifies the exact `Read` invocations) |

---

## Budget Ceiling — Soft Signal, Not Prescription [UXL-018]

Bootstrap token cost is an **observability signal**, not an enforced ceiling.
`hooks/scripts/bootstrap-cost.sh` makes the cost visible; the signal
*informs* judgment, it does not automate behavior.

### Convention: track `bootstrap_tokens` in progress.md session header

At the start of each new session block in `notes/progress.md`, record the
measured bootstrap token cost as a header field:

```markdown
**Session**: 36 — <one-line topic>
**Bootstrap tokens**: ~7,800 (3-file cascade; run `hooks/scripts/bootstrap-cost.sh`)
**Date**: 2026-04-23
```

This creates a timeseries alongside `notes/bootstrap-cost-log.md` so session
narrative + cost data live together. Makes drift visible at session-boundary
review without requiring a separate audit step.

### Soft budget ceiling guidance

A **~15% of context window** soft ceiling on bootstrap cost is a useful
default heuristic: beyond that, each new protocol layer's marginal cost
starts crowding out productive output. When bootstrap approaches or exceeds
this threshold, the signal is: **reconsider whether every auto-loaded layer
is load-bearing for the current session class** — not: mechanically compact
existing content to hit a number.

### User directive (2026-04-22) — preserved verbatim for durability:

> "the limits are soft not prescriptions; final decision should be
> adaptively resorted to the agentic reasoning based on the specific
> user/project request and domain context (e.g. one of the classic
> worst-case scenario of blindly automating this away will be agents
> (and the human users influenced by them) resorting to compact contents
> unnecessarily when the specific in-series sessions or phased task(s)
> at hand require detailed transfers for example)."

### Anti-pattern: mechanical compaction to hit budget

Do NOT compact detailed phase-task transfers, curated session narratives,
or load-bearing `notes/*.md` artifacts to reduce `bootstrap_tokens`. This is
the exact failure mode LL-29 (quality-over-tokens invariant) was recorded
to counter. Detailed cross-session transfers often justify higher bootstrap
cost — especially during complex multi-session work.

Correct responses when `bootstrap_tokens` trends high:

1. **Evaluate what's auto-loaded** — is each file still serving cold-start anchor or has it drifted to on-demand utility? Archival to `_archive/` or move-to-on-demand (like LL exclusion from bootstrap in Session 32) is structural — doesn't lose information.
2. **Check T1 boundaries** — are top-sections in `progress.md` / `TODO.md` still tight, or have they bled past the partial-read budget? Re-anchor boundaries.
3. **Accept the cost if the work demands it** — an 8-week architectural refactor spanning 12 sessions legitimately needs detailed transfer artifacts. Budget signal is a prompt to *reason*, not to *trim*.

The agent's job: interpret the signal in context. The script's job: surface
the data. Neither the script nor this doc should impose behavior that runs
counter to task-specific reasoning.

---

## References

- `notes/impl-plan-bootstrap-efficiency-2026-04-11.md` — authoritative implementation plan (P1–P5)
- `notes/session-28-recovery-2026-04-11.md` — architectural thesis ("Fix the read, not the file"), Parts 2-3
- `notes/bootstrap-cost-log.md` — timeseries of bootstrap token cost per session
- `hooks/scripts/enforce-current-task-budget.sh` — L1 hard gate (this card's enforcement surface)
- `hooks/scripts/bootstrap-cost.sh` — measurement instrumentation (3-file cascade, budget-aware)
- `knowledge/operational-patterns/state-management/filesystem-patterns.md` — tracked-by-default policy (LL-25), tense hygiene (LL-26), flat-notes policy (Session 32)
- `knowledge/operational-patterns/state-management/session-lifecycle.md` — session resumption flow
