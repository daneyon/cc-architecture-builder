---
id: bootstrap-read-pattern
title: Bootstrap Read Pattern — Cheap-to-Expensive Partial-Read Cascade
category: operational-patterns/state-management
tags: [bootstrap, cold-start, partial-read, cascade, token-efficiency, state, LL-25, LL-28]
summary: How to cold-start a CAB session with a bounded token budget by reading a prefix of each state file, escalating to full reads only when a specific decision demands the tail content.
depends_on: [filesystem-patterns, session-lifecycle]
related: [context-engineering, orchestration-framework]
complexity: intermediate
last_updated: 2026-04-11
estimated_tokens: 1200
source: CAB-original (impl-plan-bootstrap-efficiency-2026-04-11.md, P3/P4)
confidence: A
review_by: 2026-07-11
revision_note: "v1.0 — initial publication as P3/P4 deliverable of the bootstrap efficiency task. Supersedes the 'read all 4 files in full' protocol that caused the Session 28 regression (~40K tokens, 37% over pre-LL-25 baseline)."
---

# Bootstrap Read Pattern

## Core Principle

**File size and bootstrap read size are separable variables.** A state file can be large on disk (durable, semantically preserved) without being read in full at cold-start. Fix the *read pattern*, not the *file size*.

This pattern exists because LL-25/26/27/28 correctly optimized state files for semantic preservation and cross-session recovery — but without counter-pressure for cold-start compactness, the standardized "read all 4 files in full" bootstrap regressed from ~30K tokens (pre-LL-25) to ~40K tokens (post-LL-28) in ~1 week.

---

## The Cheap-to-Expensive Cascade

Each layer gates the next. If Layer N gives you what you need, you never touch Layer N+1.

| Layer | File | Bootstrap Read | Budget | Rationale |
|-------|------|----------------|--------|-----------|
| **L1** | `notes/current-task.md` | Full read | ≤100 lines (hard gate) | Cold-start anchor; pointer to active task + phase status + directives. Size-enforced by `hooks/scripts/enforce-current-task-budget.sh`. |
| **L2** | `notes/progress.md` | `Read(path, limit=100)` | ~100 lines of top section | Current Position (latest session state, next-action queue) sits above a `<!-- T1:BOUNDARY -->` marker; historical narrative flows below. |
| **L3** | `notes/TODO.md` | `Read(path, limit=80)` | ~80 lines of top section | Top Priorities (P0/P1) above the boundary; full backlog below. |
| **L4** | `notes/lessons-learned.md` | `Read(path, limit=60)` | ~60 lines (compact LL table) | LL index/table at top; detailed LL sections below the boundary. See §Density Bottleneck below. |

**Per-file budget is per-file convention, not per-file enforcement.** Only L1 has a hard hook gate. L2/L3/L4 rely on the T1 boundary marker convention being maintained by authors during normal state-writing.

---

## How to Invoke at Cold-Start

```
Read(notes/current-task.md)                        # full file, ~100 lines max
Read(notes/progress.md, limit=100)                 # T1 section only
Read(notes/TODO.md, limit=80)                      # T1 section only
Read(notes/lessons-learned.md, limit=60)           # LL table only
```

Expected cost: **~12-13K tokens** (vs. ~40K for full reads of all four). See `notes/metrics/bootstrap-cost-log.md` for current baseline.

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
- **No enforcement** — authors are trusted to place it correctly; measurement (P1 `bootstrap-cost.sh`) catches drift

See P2 of `notes/impl-plan-bootstrap-efficiency-2026-04-11.md` for the original boundary-marker rollout.

---

## Escalation to Full Read

Partial reads are the *default*. Escalate to full reads when:

| Trigger | Action |
|---------|--------|
| L1 pointer references a section of `progress.md` outside the T1 window | Full read `progress.md` |
| New task planning requires full backlog visibility | Full read `TODO.md` |
| Current decision matches an LL category and the L4 compact table row is insufficient | Full read `lessons-learned.md` + grep for specific LL-NN |
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

- **L2/L3/L4 top-section placement** — no hook. Maintained by authors. Drift is caught by `hooks/scripts/bootstrap-cost.sh` run as a periodic measurement, not a commit gate.
- **LL architectural weaving** — L4 being "load on demand" only works if LLs are structurally woven into the skills/hooks that govern their domains. Audit coverage tracked in `notes/metrics/ll-integration-audit.md` (P4 deliverable).

---

## Density Bottleneck (lessons-learned.md)

`notes/lessons-learned.md` is the outlier in the cascade. Even at 60 lines, `Read(path, limit=60)` costs ~7K tokens because the LL table is dense (~489 chars/line average — ~3× the `progress.md` density). Line-count policies (e.g., LL-25's "≤300 lines") miss this entirely because they use line count as the proxy metric.

**Mitigation (P4)**: split the LL table into a **compact index** (one-line per LL, load-bearing for bootstrap) above the boundary, and **verbose detail sections** (grep-on-demand) below. This is the only L4 structural change planned; no size limit is added.

**General rule**: any future state-file size policy must factor **byte/token weight**, not just line count.

---

## Why This Works

- **Prompt cache friendly** — T1 sections are at the top of each file (newest content above older) so cache hits carry across turns (LL-10/Finding 1 precedent).
- **Semantic preservation invariant** — no content is deleted. The boundary marker is purely a placement convention. LL-25's "tracked by default" guarantee holds byte-for-byte.
- **Agentic flexibility preserved** — files beyond L1 can grow without limit. The read pattern is bounded, not the write pattern.
- **Measurement-driven** — `bootstrap-cost.sh` makes drift visible before it compounds. The instrumentation *is* the compensating control for the soft gates.

---

## Common Failure Modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| Author writes new session narrative at the *tail* of `progress.md` | L2 partial read misses the latest session state | Rewrite top-section convention: append to "Current Position", migrate old section below boundary |
| Boundary marker is deleted in a refactor | Partial reads load unbounded prefix | Re-add marker; `bootstrap-cost.sh` will show the token cost spike |
| `current-task.md` grows past 100 lines | Hook blocks commit | Move verbose task detail into the impl-plan file (the real session-transfer artifact — see `notes/references/session-28-recovery-2026-04-11.md` Part 3) |
| Post-compaction session forgets the cold-start protocol | Reads all 4 files in full again | Re-anchor via `CLAUDE.md §Bootstrap Protocol` (P4 deliverable specifies the exact `Read` invocations) |

---

## References

- `notes/impl-plan-bootstrap-efficiency-2026-04-11.md` — authoritative implementation plan (P1–P5)
- `notes/references/session-28-recovery-2026-04-11.md` — architectural thesis ("Fix the read, not the file"), Parts 2-3
- `notes/metrics/bootstrap-cost-log.md` — timeseries of bootstrap token cost per session
- `hooks/scripts/enforce-current-task-budget.sh` — L1 hard gate (this card's enforcement surface)
- `hooks/scripts/bootstrap-cost.sh` — measurement instrumentation
- `knowledge/operational-patterns/state-management/filesystem-patterns.md` — tracked-by-default policy (LL-25), tense hygiene (LL-26)
- `knowledge/operational-patterns/state-management/session-lifecycle.md` — session resumption flow
