# UX-Log Wave Plan — Prioritization Pass 1

**Date**: 2026-04-22
**Source pass**: `notes/ux-log-001-2026-04-22-pass-1.csv`
**Scope**: 23 triaged rows + UXL-034 (total 24 active candidates)
**Framework stack applied**: `knowledge/reference/prioritization-frameworks.md` — Value-vs-Effort + Severity (Tier 1, already captured at log) + Kano (Tier 2, skipped — CAB has no gui surface) + RICE (Tier 2, applied to hook-cluster peer group ≥3) + MoSCoW (Tier 3, applied per wave)
**Output**: 9 waves grouped by coupling, dependency, and effort-value profile

---

## Framework Application Summary

**Value-vs-Effort + Severity (Tier 1 — already captured)**:
- Value distribution: 11 H / 7 M / 5 L
- Effort distribution: 3 H / 11 M / 9 L
- Two H/H rows (UXL-004, UXL-005) anchor long-horizon waves; UXL-023 M/H couples to UXL-022 (resolved).

**Kano (Tier 2 — skipped with justification)**:
CAB has no `gui` surface rows in this pass (0/24). Kano maps poorly to infrastructure/meta surfaces — forcing would produce noise per the prioritization-frameworks.md anti-pattern. Skipped.

**RICE (Tier 2 — applied to hook-cluster peer group)**:
Hook cluster has 6 peer rows (UXL-024, 026, 027, 028, 029, 030) — meets ≥3 peers threshold. Reach = conservative (all affect main-session and all subagents); Impact and Effort from triage; Confidence = B (no empirical data on frequency yet).

| Row | Reach | Impact | Confidence | Effort | **RICE** |
|---|---|---|---|---|---|
| UXL-027 (LL-02/12 pre-gate) | 3 | 3 | 0.8 | 2 | **3.6** |
| UXL-028 (LL-08 post-check) | 3 | 3 | 0.8 | 2 | **3.6** |
| UXL-026 (LL-19/20 counter) | 3 | 3 | 0.5 | 2 | **2.25** |
| UXL-030 (LL-10 fresh-fetch) | 2 | 2 | 0.7 | 2 | **1.4** |
| UXL-029 (LL-17 worktree) | 2 | 2 | 0.6 | 2 | **1.2** |
| UXL-024 (LL-26 regex) | 1 | 1 | 0.9 | 1 | **0.9** |

Top RICE: UXL-027+UXL-028 (tied) → validates pairing them in Wave 2. UXL-026 third = design work needed first (lower Confidence reflects this).

**MoSCoW (Tier 3 — applied per wave)**:
Per-wave M/S/C/W assignments below — a row may be `M` in Wave 3 (release-scoped) and `W` (won't execute) in Waves 1-2.

---

## Waves (Execution Order)

### Wave 1 — Hygiene Batch (5 rows; all L effort)

**Rows**: UXL-008, UXL-019, UXL-020, UXL-021, UXL-024
**Coupling rationale**: All L/L (low value + low effort) — none individually warrants `/cab:planning-implementation` overhead. Batched inline to clear the backlog in one focused pass.
**MoSCoW per row (Wave 1 release)**: M, M, M, M, M
**Execution approach**: Ad-hoc inline with `[UXL-NNN]` commits per row; uxl-update.py helper for resolutions.

| Row | Effort | Lands |
|---|---|---|
| UXL-008 | L | Mojibake fix on `knowledge/reference/workflow-processflow.md` (UTF-16 residue from Phase 2.6) |
| UXL-019 | L | Reversibility inventory table appended to `filesystem-patterns.md` (protocol → commit → revert) |
| UXL-020 | L | RAS-exec LL-25 tracked-notes policy doc alignment |
| UXL-021 | L | HydroCast LL-25 tracked-notes policy doc alignment |
| UXL-024 | L | LL-26 pre-push hook regex refinement (backtick-wrapped marker exclusion via `grep -v` post-filter) |

**Estimated cost**: ~30-60 min total; 5 commits + 5 CSV resolutions.

---

### Wave 2 — VOID (both rows dropped 2026-04-23)

**Rows**: ~~UXL-027~~ (dropped → `wontfix`), ~~UXL-028~~ (dropped → `wontfix`)
**Void rationale**: Perf benchmarking of the UXL-028 prototype hook revealed ~1.27s per fire on Windows Git Bash (python cold-start + process-spawn dominance), ~60x the 20ms acceptance criterion. Combined with empirical non-recurrence of LL-02/12/08 post rules + memory + model upgrades, both rows fail the dual-POV check (memory/feedback_dual_pov_check.md). Artifacts deleted: `hooks/scripts/bg-agent-post-check.sh` + `notes/impl-plan-bg-agent-bracket-2026-04-22.md` (commit history preserves the investigation trail via `f9b035d` and `7054c5c`).

**Escalation path preserved**: if LL-02/12 or LL-08 recurs with empirical evidence, file a fresh row with measurement data + revisit whether a redesigned hook (pure bash, single-python-invocation, or compiled-language variant) can meet perf targets. Rerun dual-POV check before shipping.

**Sequencing consequence**: Wave 3 (strategic CC-trajectory alignment) becomes next active wave.

---

### Wave 3 — Strategic CC-Trajectory Alignment (2 rows; sequential)

**Rows**: UXL-002 (commands→skills migration audit), UXL-001 (default setup protocol project-schema-first)
**Coupling rationale**: UXL-002 produces mapping of existing skill↔command pairs that may inform UXL-001 scope (if default setup creates commands, the commands-deprecation question lands here). Sequential execution.
**MoSCoW**: M (UXL-002), S (UXL-001)
**Execution approach**: TWO separate `/cab:planning-implementation` invocations — these are deep strategic work. UXL-002 FIRST; user reviews mapping; decides on migration sequencing; UXL-001 follows with informed context.

**Why not Wave 1 despite user's original brain-dump**: Both are H/M. Hygiene batch unblocks context; hook bracket proves the per-row planning pattern; THEN strategic work gets full attention.

**Estimated cost**: UXL-002 = 2-3 sessions (audit + migration plan + selective execute); UXL-001 = 1-2 sessions.

---

### Wave 4 — Structural Hook Enforcers (3 rows)

**Rows**: UXL-029 (LL-17 worktree auto-detect), UXL-030 (LL-10 fresh-fetch pre-edit hook), UXL-026 (LL-19/20 sycophancy protocol counter)
**Coupling rationale**: Three independent hook additions. UXL-029 + UXL-030 are straightforward (trigger + action); UXL-026 is design-heavy (what IS the enforcement mechanism for "no sycophantic agreement"? Hook? Output-style? CLAUDE.md invariant?).
**MoSCoW**: M (UXL-029), M (UXL-030), S (UXL-026)
**Execution approach**: UXL-029 + UXL-030 can share a plan (similar hook patterns). UXL-026 gets its own plan because of design ambiguity — need to decide mechanism before implementation.

**Estimated cost**: UXL-029+030 = 1 session; UXL-026 design = 1 session; UXL-026 exec = 1 session.

---

### Wave 5 — LL-28 State-Write Protocol Pair (2 rows; sequential with validation gate)

**Rows**: UXL-017 (fallback dying-session recovery) → UXL-016 (event-triggered state-write)
**Coupling rationale**: UXL-017 FIRST because it codifies the Session 27 recovery method, producing the validation dataset needed by UXL-016. Per Session 27 user directive: "at least one survived dying-session recovery test before hard-coding" the event-triggered write protocol.
**MoSCoW**: M (UXL-017), C (UXL-016) — UXL-016 is `CANDIDATE` until UXL-017 provides recovery validation; may slip.
**Execution approach**: Sequential; UXL-017 gets own plan; UXL-016 plan depends on UXL-017 outcomes.

**Estimated cost**: UXL-017 = 1-2 sessions; UXL-016 = 1-2 sessions conditional on UXL-017's validation.

---

### Wave 6 — Architecture Evolution (2 rows; parallel-OK)

**Rows**: UXL-025 (Global CLAUDE.md v2 — Extension Registry removal + Plugin Hygiene Policy reinvestment), UXL-034 (state-mgmt-capture skill)
**Coupling rationale**: Both touch foundational state-management infrastructure; by Wave 6 we have ≥15 resolved rows for UXL-034's KPI baseline. UXL-025 has been queued behind Phase D (HydroCast state-mgmt comparison) per Session 27 directive — by Wave 6 Phase D may have completed or UXL-025 can execute in parallel worktree.

**UXL-014 + UXL-015 auto-supersede**: when UXL-025 lands, it subsumes the "CAB provides" notes convention. Log them as `status=superseded` at UXL-025 resolution.

**MoSCoW**: M (UXL-025), S (UXL-034)
**Execution approach**: Two separate `/cab:planning-implementation` plans — UXL-025 is architectural; UXL-034 is skill scaffolding. Can execute in parallel worktrees if desired.

**Estimated cost**: UXL-025 = 1-2 sessions; UXL-034 = 2-3 sessions (skill + measurement infrastructure + KPI rollup + documentation).

---

### Wave 7 — Architecture Open Questions (3 rows; light batch)

**Rows**: UXL-003 (CAB orchestrator subagent global-default decision), UXL-023 (Dream consolidation skill — narrowed scope), UXL-006 (planning-implementation a-team + product-design-cycle integration — verify remaining scope post user's SKILL.md commit)
**Coupling rationale**: All M-value architecture-review items. UXL-003 is analysis-only (no implementation needed, just a decision). UXL-023 scope was narrowed post-UXL-022 docs refresh. UXL-006 may be largely resolved already via user's 0275794 commit — needs re-triage.
**MoSCoW**: M (UXL-003), C (UXL-023), C (UXL-006)
**Execution approach**: Batch as "architecture review session" — each row gets a short plan OR a decision memo. UXL-006 may resolve to `status=superseded` if user's edits already address the scope.

**Estimated cost**: ~1 session for the batch.

---

### Wave 8 — KB → Knowledge-Graph Foundation (1 row; H/H)

**Rows**: UXL-005 (KB → knowledge-graph standardization)
**Coupling rationale**: Foundational architectural work. H/H effort but unblocks UXL-004, UXL-009, UXL-010 downstream. Dedicated wave because scope is substantial and stands alone.
**MoSCoW**: M
**Execution approach**: Full `/cab:planning-implementation` with multi-phase plan; likely 3-5 sessions. Should absorb HydroCast KG patterns (cross-refs UXL-009 deferred).

**Pre-req**: Wave 6 completion preferable (UXL-025 + UXL-034 = stable state-mgmt foundation before adding KG on top).

**Estimated cost**: 3-5 sessions.

---

### Wave 9 — Post-KG Deliverables (3 rows; unblocked by Wave 8)

**Rows**: UXL-004 (CAB advisor ↔ project-orchestrator agentic bridge), UXL-009 (HydroCast KB-plan pattern extraction — from deferred), UXL-010 (AgentContextGraphVisualizer feasibility — from deferred)
**Coupling rationale**: All require UXL-005 (Wave 8) foundational KG work to be meaningful. UXL-009 + UXL-010 were the user-directed deferrals from Phase 4 gate — originally marked `status=deferred`; transition to `triaged` at Wave 8 completion.
**MoSCoW**: M (UXL-004), S (UXL-009), S (UXL-010)
**Execution approach**: Post-Wave-8 re-triage + individual plans.

**Estimated cost**: UXL-004 = 3-5 sessions; UXL-009 = 1-2 sessions (pattern extraction synthesis); UXL-010 = 2-3 sessions (feasibility eval + prototype decision + architecture recommendation).

---

### Wave 10 — HydroCast Comprehensive State-Mgmt Alignment (UXL-036; scope added 2026-04-23)

**Rows**: UXL-036 (HydroCast comprehensive state-mgmt alignment audit — full-dimension vs tracked-notes-only)
**Coupling rationale**: The UXL-020/021 propagation rows only covered LL-25 tracked-notes scope. A comprehensive alignment requires auditing: bootstrap-read-pattern (CAB 3-file cascade vs HydroCast LC-08 3-layer), hook presence (pre-push-state-review, enforce-current-task-budget, bg-agent-post-check from UXL-028), T1 boundary conventions, LL classification schema, kb-conventions, memory-layer adoption (UXL-031/032), UX-log tracker pattern (HydroCast's `notes/gui-review-comments/` → CAB's tiered `notes/ux-log-*.csv`), prioritization-frameworks adoption, active-top sort ergonomics.

**Deferral rationale**: CAB still iterating state-mgmt through Wave 5 (LL-28 state-write protocol) + Wave 6 (CLAUDE.md v2 + state-mgmt-capture skill). Aligning HydroCast now = re-aligning later. Wave 10 placement avoids redundant work. HydroCast Phase D comparison (queued on PR #8) will naturally surface alignment deltas as byproduct.

**MoSCoW**: S
**Execution approach**: Dedicated `/cab:planning-implementation` plan; possibly split into sub-phases per alignment dimension. Couples to Phase D output where available.

**Estimated cost**: 3-5 sessions.

---

### Wave 11 — Cross-Project Propagation Pattern Formalization (UXL-035; scope added 2026-04-23)

**Rows**: UXL-035 (CAB-side deliverable + external-repo apply pattern formalization)
**Coupling rationale**: Pattern proved in Wave 1 (UXL-020 RAS-exec patch-ready artifact). Needs standardization: template artifact structure, convention for when CAB-side work is "done" vs "needs external apply," cross-reference schema back to tracker.
**MoSCoW**: C
**Execution approach**: Short standalone plan; produces template + documentation.

**Estimated cost**: ~1 session.

---

## Cross-Cutting Notes

### Rows Not In Any Wave

- **UXL-014, UXL-015**: auto-supersede at Wave 6 execution (subsumed by UXL-025). Until then, remain `triaged` with orchestrator_take noting the supersession expectation.

### Cumulative Row Count Per Wave

| Wave | Rows | Cumulative resolved | Cumulative remaining triaged/deferred |
|---|---|---|---|
| current state | — | 9 | 25 |
| 1 | 5 | 14 | 20 |
| 2 | 2 | 16 | 18 |
| 3 | 2 | 18 | 16 |
| 4 | 3 | 21 | 13 |
| 5 | 2 | 23 | 11 |
| 6 | 2 + auto-supersede 2 | 25 + 2 superseded | 7 |
| 7 | 3 | 28 | 4 |
| 8 | 1 | 29 | 3 |
| 9 | 3 | 32 | 0 |

Wave 9 completion closes the current pass cycle. Pass 2 opens fresh with new captured observations.

### Soft Ceiling Reminders (UXL-018)

- Bootstrap cost is a SIGNAL. If any wave execution pushes bootstrap_tokens past ~10K, investigate (is there legitimate new state? or drift?), don't mechanically compact.
- `notes/progress.md` will grow meaningfully through Wave 9 execution. T1 boundary re-anchoring may be needed around Wave 5-6; that's a normal maintenance operation, not a compaction trigger.

### Execution Discipline Standard (user directive 2026-04-22)

Rows and waves of **L effort** may execute inline with ad-hoc sequencing (Wave 1 hygiene batch).
Rows and waves of **M-H effort** MUST go through `/cab:planning-implementation` → `/cab:execute-task` per the standard protocol. Per-wave plans are preferred over per-row plans when rows are tightly coupled (proven pattern: UXL-011+UXL-013 trio, UXL-022+UXL-032 trio, UXL-027+UXL-028 pair).

### Sign-Off Gate

This wave plan awaits user review before Wave 1 execution begins. Adjustments welcome — sequencing, MoSCoW assignments, wave boundaries are all tunable.

---

## Sources

- `knowledge/reference/prioritization-frameworks.md` — tiered stack applied
- `notes/ux-log-001-2026-04-22-pass-1.csv` — source data (34 rows)
- `notes/progress.md` Session 35 — prior informal ranking (top-10 list; this pass formalizes)
- User directive 2026-04-22: "M-H effort tasks should be operating based on our usual standard of /planning-implementation and /cab:execute-task"
