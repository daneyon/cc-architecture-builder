# Current Task: Phase D — HydroCast ↔ CAB State-Management Strategic Comparison

**Status**: QUEUED (pre-requisite: HydroCast PR #8 merged to main)
**Started**: TBD — target Session 34
**Branch**: CAB `master`; HydroCast work via `git worktree` off post-merge main (LL-17)

---

## Gate

HydroCast `feat/plugin-first-migration-2026-04-09` PR #8 awaiting user review + merge: https://github.com/daneyon/Flood-Forecasting/pull/8

Do NOT start Phase D execution until PR is merged. Working-tree WIP on that branch (Sessions 24-27 strategic assessments + GUI B.5 work) is intentionally preserved for user's parallel resume via `git worktree`.

---

## Outcome (target)

Read-only comparative analysis of CAB's post-Session-32 3-file cascade architecture vs HydroCast's 3-layer LC-08 hierarchy. Produces a canonical comparison document identifying: (a) architectural delta, (b) applicable cross-pollinations, (c) which CAB protocols HydroCast should adopt (or not) given its domain constraints.

**Deliverable**: `Flood-Forecasting/notes/cab-vs-hydrocast-state-mgmt-comparison-2026-04-11.md` (tracked on HydroCast main, post-merge).

---

## Execution Strategy (multi-agent fan-out)

1. **`general-researcher` subagent (background-capable if read-only)** — survey HydroCast state files:
   - `notes/memory/learned-corrections.md` LC-08 hierarchy
   - `CLAUDE.md` state architecture section
   - `notes/current-task.md` / `progress.md` / `session.md` as living examples of the 3-layer pattern
   - Historical context: when/why LC-08 emerged
2. **`cab:architecture-advisor` subagent** — deep-dive CAB's post-fix architecture:
   - `knowledge/operational-patterns/state-management/bootstrap-read-pattern.md` v1.1
   - `knowledge/operational-patterns/state-management/filesystem-patterns.md` v3.3
   - LL-25, LL-26, LL-27, LL-29 (post-Session-32 Classification + Priority schema)
3. **Main session synthesis** — writes comparison doc to HydroCast post-merge worktree, lands commit on HydroCast main via a follow-on PR or direct push (user scopes).

---

## Key Questions to Answer

1. **Separable variables**: Does HydroCast's LC-08 conflate file-size-on-disk with bootstrap-read-budget the way CAB did pre-Session-32? If so, same fix applicable.
2. **Classification vs "never delete"**: CAB's LL Classification (INTEGRATED/ACTIVE/ADVISORY/ARCHIVED) vs HydroCast's "never delete, move to bottom" — are these complementary or contradictory? Which is more token-efficient at scale?
3. **Bootstrap cost**: Is HydroCast's 3-layer hierarchy + cold-start anchor measurably cheaper than CAB's post-fix 3-file cascade? Run `bootstrap-cost.sh` equivalent against HydroCast to measure.
4. **LL-28 enforcement**: HydroCast's recently-closed audit workstream is itself a LL-28 case study (state gap across 4 weeks). Can CAB's event-triggered dialogue-checkpoint candidate be prototyped on HydroCast first?

---

## Reference Artifacts

- **CAB side**: `notes/lessons-learned.md` (LL-25/LL-29), `knowledge/operational-patterns/state-management/*.md`, `CLAUDE.md` §Bootstrap Protocol
- **HydroCast side**: `CLAUDE.md`, `notes/memory/learned-corrections.md`, `notes/current-task.md` (cold-start anchor pattern)
- **Cross-session learnings**: LL-27 (shadowing), LL-28 (dialogue-level state gap — validated by this very audit close workstream)

---

## Blockers / Dependencies

- [ ] **HARD BLOCKER**: HydroCast PR #8 must be merged to main before Phase D can read `knowledge/INDEX.md` reference and frontmatter-complete KB files in their final form
- [ ] `git worktree add` on HydroCast main for parallel-safe access (per CAB LL-17) — document setup in Session 34 progress notes

<!-- T1:BOUNDARY — `current-task.md` is entirely T1 by design (<100 line hard target enforced by hooks/scripts/enforce-current-task-budget.sh). Whole file is the cold-start anchor. -->
