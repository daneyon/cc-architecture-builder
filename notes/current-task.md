# Current Task: Bootstrap Token Efficiency Restoration

**Status**: P1 S29 (`8dfef75`), P2 S30 (`836f3aa`), P3 S31 (`731bea0`). **Session 32 opens fresh for P4 + P5 + task close** (Option A per S31 HITL-3 dialogue).
**Started**: 2026-04-11 Session 28 (diagnostic + v1 plan + v2 pivot + death mid-state-close on "Prompt is too long")
**Recovery completed**: 2026-04-11 Session 29 (JSONL-transcript-sourced backfill of Session 28 emergent content — see recovery artifact)
**P1 completed**: 2026-04-11 Session 29 (`8dfef75` — bootstrap-cost.sh + baseline log)
**Branch**: `master` (CAB, local-only; solo workflow — no push needed)

---

## ⚠ Session 32 Cold-Start Protocol — NON-STANDARD BOOTSTRAP STILL IN EFFECT

**User directive 2026-04-11 (still authoritative)**: standard bootstrap protocol remains in workaround status until P4 lands the CLAUDE.md §Bootstrap rewrite.

**Session 32 must read ONLY these 3 files at cold-start** (target: ~8K tokens):

1. `notes/current-task.md` — this file (task pointer + phase status)
2. `notes/impl-plan-bootstrap-efficiency-2026-04-11.md` — 5-phase plan; Session Log has P1/P2/P3 landing notes + byte-weight finding + S31 context-estimation finding
3. `notes/references/session-28-recovery-2026-04-11.md` — v1→v2 thesis + operational workflow advice

**Partial-read cascade available**: `Read(progress.md, limit=100)` / `Read(TODO.md, limit=80)` / `Read(lessons-learned.md, limit=60)` return T1 sections only. Full reads on-demand via unlimited Read or grep. **`bootstrap-read-pattern.md` KB card** documents the cascade.

**Session 32 first-turn sequence**: cold-start reads → acknowledge P3 landed → execute P4 (5 deliverables: CLAUDE.md §Bootstrap rewrite, filesystem-patterns.md v3.3, cc-memory-layer-alignment.md NEW KB card, ll-integration-audit.md audit report, LL table compact-index/verbose-detail split) → commit P4 → P5 (bootstrap-cost.sh re-run + LL-29 draft + HITL-4) → task close. **CRITICAL S31 finding: assistant context estimation is unreliable** — check `/context` or ask user for actual budget at each phase boundary instead of self-estimating.

---

## Problem Statement (concise)

Session 28 standard bootstrap consumed ~40K tokens across 4 full state-file reads. Root cause: LL-25/26/27/28 cumulative state-mgmt work optimized for semantic preservation without counter-pressure for cold-start compactness. `current-task.md` breached <100 target (174 lines). `progress.md` +44% since LL-25. Zero programmatic enforcement — "architecturally enforced" was aspirational language.

## Fix Approach (v2 — the architectural pivot)

**Fix the READ pattern, not the FILE size.** User rejected v1 (hard limits on progress/TODO) because `progress.md` currently serves as de facto session-narrative durable store. v2 uses partial-read cascade at bootstrap via `Read(file, limit=N)`. Only hard gate: `current-task.md` <100 lines. Other files stay agentically flexible.

**Core thesis (never captured in state files until Session 29 recovery)**: *"File size (on disk) and bootstrap read size (loaded at cold-start) are separable variables. Fix the read, not the file."* Full architectural framing in `session-28-recovery-2026-04-11.md` Parts 2-3.

## Phase Status

| Phase | Status | Deliverable | Est |
|---|---|---|---|
| P1 — Instrumentation | ✅ **DONE** (`8dfef75`) | `hooks/scripts/bootstrap-cost.sh` + `notes/metrics/bootstrap-cost-log.md` (baseline: 41,081 tok) | ~2K |
| P2 — Convention refactor (**the hinge**) | ✅ **DONE** (this commit, Session 30) | T1 boundary markers in 3 files + Session 30 T1 top-section in progress.md + Session 29 content archived to Historical Narrative + duplicate `## Current Position` header renamed. Zero semantic content loss. | ~12K |
| P3 — Minimal enforcement | ✅ **DONE** (`731bea0`, S31) | `enforce-current-task-budget.sh` dual-mode hook (CC PreToolUse + git pre-commit shim) + `bootstrap-read-pattern.md` KB card + 3 INDEX updates. 7/7 tests pass. | ~4K actual |
| P4 — Docs + LL audit | **NEXT (Session 32)** | CLAUDE.md §Bootstrap rewrite + `filesystem-patterns.md` v3.3 + `cc-memory-layer-alignment.md` NEW KB card + `ll-integration-audit.md` + LL table compact-index/verbose-detail split | ~20-22K (scope reassessed S31) |
| P5 — Validation + LL-29 | pending | bootstrap-cost.sh re-run, comparison table, LL-29 draft, HITL-4, task close | ~5K |

**Total remaining**: ~25-27K tokens across 1 session (Session 32).

## Recommended per-session cadence

- **S32**: P4 (~20-22K) + P5 (~5K). Single session per user directive (Option A). If P4 LL audit balloons, split to S33.

Full operational workflow advice (artifact-carried context pattern, anti-patterns, first-turn sequence) in `session-28-recovery-2026-04-11.md` Part 7.

## HITL Gates

- [X] HITL-1: v2 plan approved (Session 28 dialogue)
- [X] HITL-2 (implicit P1): "proceed" received Session 29, P1 committed `8dfef75`
- [X] HITL-2 (explicit P2): approved Session 30 ("follow your final contemplated best recommended advise on the 5 design decisions")
- [X] HITL-3: hook approved S31 (7/7 tests pass), committed `731bea0`
- [ ] HITL-4: pre/post bootstrap metrics + LL-29 draft before task close

## User Directives (Session 28/29, authoritative)

1. **State mgmt is BROKEN** — this task is the authoritative fix; takes priority over all other state-mgmt work
2. **HydroCast audit state-mgmt remediation is DEFERRED** — will NOT be implemented from the now-old audit; revisit after CAB fix stabilizes
3. **Session 29 non-standard bootstrap mandatory** — see protocol above
4. **No over-building** — partial reads + convention, not hard limits + hooks everywhere
5. **No LL-26 two-commit pattern dogfooding during this task** — that's the broken protocol being replaced; use single commit per phase

## Reference Artifacts

- **Impl plan (load at Session 29 cold-start)**: `notes/impl-plan-bootstrap-efficiency-2026-04-11.md`
- **Session 28 recovery (load at Session 29 cold-start)**: `notes/references/session-28-recovery-2026-04-11.md`
- **5 Critical Findings (permanent reference)**: `notes/references/prior-session-5-findings-2026-04-10.md`
- **Session 28 JSONL source**: `~/.claude/projects/c--Users-daniel-kang-Desktop-Automoto-cc-architecture-builder/d17b1e16-a94e-4b33-b222-7fef5fc60773.jsonl`
- **Memory architecture reference**: `notes/references/How Anthropic Built 7 Layers of Memory and a Dreaming System for Claude Code  (video breakdown).md`

<!-- T1:BOUNDARY — `current-task.md` is entirely T1 by design (<100 line hard target, whole file is the cold-start anchor). This marker is for tooling consistency across all 4 state files, not cost reduction. -->

