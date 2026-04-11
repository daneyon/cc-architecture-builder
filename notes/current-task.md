# Current Task: Bootstrap Token Efficiency Restoration

**Status**: P1 landed Session 29 (`8dfef75`). **Session 30 opens fresh to execute P2** (the hinge) via `cab:execute-task`.
**Started**: 2026-04-11 Session 28 (diagnostic + v1 plan + v2 pivot + death mid-state-close on "Prompt is too long")
**Recovery completed**: 2026-04-11 Session 29 (JSONL-transcript-sourced backfill of Session 28 emergent content — see recovery artifact)
**P1 completed**: 2026-04-11 Session 29 (`8dfef75` — bootstrap-cost.sh + baseline log)
**Branch**: `master` (CAB, local-only; solo workflow — no push needed)

---

## ⚠ Session 30 Cold-Start Protocol — DO NOT USE STANDARDIZED BOOTSTRAP

**User directive 2026-04-11**: *"our current state mgmt is BROKEN and the recent changes we have made in the last week or so have effectively downgraded the UX. for our next session, don't use our standardized bootstrapping protocol."*

**Session 30 must read ONLY these 3 files at cold-start** (target: ~8K tokens):

1. `notes/current-task.md` — this file (task pointer + phase status)
2. `notes/impl-plan-bootstrap-efficiency-2026-04-11.md` — authoritative 5-phase plan (see Session Log at bottom for P1 landing notes + byte-weight finding)
3. `notes/references/session-28-recovery-2026-04-11.md` — Session 28 emergent content + operational workflow advice

**Do NOT read at cold-start**: `progress.md`, `TODO.md`, `lessons-learned.md`. Semantically corrupt (still Session 27 content, not refreshed until P5 task close). Grep on-demand only if a specific lookup is needed. Non-standard protocol is the interim workaround until P2-P5 lands the real fix.

**Session 30 first-turn sequence**: cold-start reads → acknowledge P1 landed → invoke `cab:execute-task` with P2 as target → HITL-2 gate after P2 refactor before committing.

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
| P2 — Convention refactor (**the hinge**) | **NEXT (Session 30)** | T1 boundary markers + top-section reorg, zero content deletion | ~12K |
| P3 — Minimal enforcement | pending | `current-task.md` <100 line pre-commit hook + partial-read KB card | ~4K |
| P4 — Docs + LL audit | pending | CLAUDE.md rewrite + `bootstrap-read-pattern.md` + `cc-memory-layer-alignment.md` KB cards + LL integration audit (factor **byte/token weight, not just line count** — lessons-learned.md finding, see impl plan Session Log) | ~10K |
| P5 — Validation + LL-29 | pending | Post-fix metric + LL-29 draft + HITL-4 | ~4K |

**Total remaining**: ~30K tokens across 2 sessions.

## Recommended per-session cadence (Session 30-31)

- **Session 30**: P2 — convention refactor, the hinge. HITL-2 gate before commit. P2 is 12K tokens, close state after if budget tight.
- **Session 31**: P3 + P4 + P5 — hook (4K), docs + LL audit (10K), validation + LL-29 draft + final close (4K). HITL-3 on hook before commit, HITL-4 on final metrics. If 18K is too much for one session, split P3+P4 from P5.

Full operational workflow advice (artifact-carried context pattern, anti-patterns, first-turn sequence) in `session-28-recovery-2026-04-11.md` Part 7.

## HITL Gates

- [X] HITL-1: v2 plan approved (Session 28 dialogue)
- [X] HITL-2 (implicit P1): "proceed" received Session 29, P1 committed `8dfef75`
- [ ] HITL-2 (explicit P2): refactored `progress.md`/`TODO.md`/`lessons-learned.md` T1-section structure before commit
- [ ] HITL-3: `current-task.md` <100 line hook before commit (affects all future commits)
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
