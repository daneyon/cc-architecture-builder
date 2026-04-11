# Implementation Plan: Bootstrap Token Efficiency Restoration

**Created**: 2026-04-11 (Session 28)
**Author**: CAB orchestrator (via `planning-implementation` skill)
**Status**: APPROVED — HITL-1 passed, execution starting
**Scope**: Fix bootstrap token-cost regression introduced by LL-25/26/27/28 cumulative state-management work
**Supersedes**: N/A (new task)
**Related**: LL-25 (tracked by default), LL-26 (tense hygiene), LL-28 (emergence capture), prior-session 5 findings (recovered from `c1f13ecc-...jsonl` Session 2026-04-10)

---

## Problem Statement

Session 28 bootstrap consumed ~40K tokens across 4 full-file state reads — a **37% regression** (+412 lines / +10K tokens) from the pre-LL-25 baseline (`302f872`, Session 24). `current-task.md` breached its <100 line hard target (174 lines, 74% overshoot) one commit after LL-25 landed. `progress.md` grew +269 lines (+44%) as LL-26/27/28 narrative accumulated. No hook or programmatic gate caught any of this — the "architecturally enforced" language in LL-25 was aspirational, not actual.

**Root cause**: The state-management standardization optimized aggressively for semantic preservation and cross-session recovery but provided **zero counter-pressure for cold-start compactness**. LL-26/28 both drove MORE content into state files; nothing pushed back. The "agentically flexible — no hard limits" guidance was interpreted as "write as much as you want" rather than "structure for efficient partial access."

## Architectural Insight (from recovered prior-session findings)

From `c1f13ecc-4e09-45fa-a3e3-a9517f739eae.jsonl` Session (2026-04-10), assistant message idx 136, the 5 findings from analysis of the Anthropic 7-layer memory reference established:

1. **Prompt cache preservation is paramount** — mid-file edits are cache-hostile (~1hr TTL); "newest at top" for updatable sections is cache-friendly
2. **CC auto-memory excludes CLAUDE.md** — validates CAB's Learned Corrections layer as non-duplicative with CC's Layer 5 extraction
3. **Session memory is ready-when-needed** — `progress.md` should be a continuously-updated summary so compaction references it instead of triggering full compaction
4. **Hard limits are a pattern** (CC MEMORY.md: 200 lines / 25KB) — BUT user feedback (2026-04-10): "for TODO and progress, i'm fine with relatively more agentically adaptive/flexible guidance/standardization (not a prescription or hard-coded limit)"
5. **Layered defense — Layer N prevents N+1** — cheap-to-expensive cascade: `current-task.md` → `progress.md` → `TODO.md` → `lessons-learned.md`, each gating the next

**Key user constraint (2026-04-10)**: "lessons-learned as optional is appropriate only if we properly apply the suggestion about having structured protocol to actually architecturally/programmatically incorporate the lessons-learned as an effective standardization of CAB frameworks and operational protocols (multiple instances of not reviewing LLs causing same mistakes)."

**Translation**: Partial/deferred reads of `lessons-learned.md` at bootstrap are acceptable ONLY IF LLs are architecturally woven into the skills/hooks that govern the decisions they constrain. Otherwise we re-introduce the "passive reference" failure mode LL-25 was trying to fix.

## Design Principles

1. **Fix the READ pattern, not the FILE size** — state files stay flexible; bootstrap loads only a bounded prefix
2. **Hard gates only where user explicitly approved** — `current-task.md` <100 lines, nothing else
3. **Convention over enforcement** for `progress.md` / `TODO.md` top-section structure — documented, not hook-gated
4. **Measurement is the compensating control** — instrumentation makes drift visible so it can't compound silently
5. **Don't over-build** — no new artifact types, no mandatory archive rollover, no architectural revolution
6. **Preserve LL-25 tracked-by-default semantically** — no content deleted, only reorganized via top-section convention

## Architecture: Cheap-to-Expensive Cascade (Partial-Read Bootstrap)

| Layer | File | Bootstrap Read Pattern | Full File Policy | When Full File Loads |
|---|---|---|---|---|
| L1 | `current-task.md` | Full read (guaranteed ≤100 lines) | **HARD GATE** <100 lines (hook-enforced) | Always |
| L2 | `progress.md` | `Read(path, limit=100)` → top "Current Position" section only | **Flexible** — no size limit | On-demand if L1 implies cross-session context needed |
| L3 | `TODO.md` | `Read(path, limit=80)` → top "Top Priorities" section only | **Flexible** — no size limit | On-demand when planning new work |
| L4 | `lessons-learned.md` | `Read(path, limit=60)` → compact LL table only | **Flexible** — agentic pruning OK | On-demand when decision matches LL category |

**Partial-read mechanism**: Assistant uses `Read` tool's `limit` parameter — already supported, no new tooling. Top-of-file structure maintained by convention: each file has an anchor section at the top, newer content appended to the top of that section (Finding 1 cache-friendly pattern), older content flows below a boundary marker into narrative/backlog tail.

**Boundary marker**: `<!-- T1:BOUNDARY -->` HTML comment — invisible in rendered markdown, greppable for tooling, reversible.

**LL architectural weaving prerequisite**: L4 being "load on demand" only works if LLs are structurally woven into skills/hooks that govern their domains. Phase 4 includes an audit to quantify current coverage; actual weaving is deferred to follow-on TODO items informed by audit results.

## Phases

### P1 — Instrumentation (baseline first)

**Deliverables**:
- `hooks/scripts/bootstrap-cost.sh` — utility script that counts lines + approximate tokens across the 4 state files, outputs CSV row `{date, session, file_lines..., t1_tokens_estimate, total_tokens_estimate}`
- `notes/metrics/bootstrap-cost-log.md` — append-only log of measurements, baseline row for Session 28 recorded

**Acceptance criteria**:
- Script runs cleanly under Git Bash on Windows (shell compatibility)
- Outputs machine-parseable CSV + human-readable summary
- Baseline recorded: `2026-04-11, session-28, current=174, progress=882, todo=468, ll=59, t1_tokens_estimate=~40000, total_full_tokens=~40000`

**Estimated cost**: ~2K tokens

### P2 — Convention refactor (structural reorganization, no content loss)

**Deliverables**:
- `notes/current-task.md` — compressed to ≤100 lines by moving verbose "Acceptance Criteria" detail into impl-plan file references (content preserved via link, not deletion)
- `notes/progress.md` — top "Current Position" section (≤100 lines) contains latest-session live state + next-action queue; `<!-- T1:BOUNDARY -->` delimiter; all existing narrative history below delimiter unchanged
- `notes/TODO.md` — top "Top Priorities" section (≤80 lines) contains P0/P1 actionable items; `<!-- T1:BOUNDARY -->` delimiter; full backlog below unchanged
- `notes/lessons-learned.md` — already table-first and compact (59 lines); verify table summary is at top, add `<!-- T1:BOUNDARY -->` before any "Pending" / "Detail" sections

**Acceptance criteria**:
- Pre/post `wc -c` shows zero content loss (refactor only, no deletion)
- Each T1 section is at the file top with clear boundary marker
- `Read(file, limit=N)` where N is the layer's budget returns load-bearing content in all 4 files
- Partial-read simulation: execute `Read(progress.md, limit=100)` → result contains Current Position section in full, no tail narrative

**Estimated cost**: ~12K tokens

### P3 — Minimal enforcement + partial-read protocol

**Deliverables**:
- `hooks/scripts/enforce-current-task-budget.sh` — pre-commit hook script, fails with exit 2 if `notes/current-task.md` exceeds 100 lines
- Hook registration in `hooks/hooks.json` under `PreToolUse` or Git pre-commit pathway (whichever matches CAB convention; investigate during implementation)
- No hooks added for `progress.md` / `TODO.md` / `lessons-learned.md` sizes — user directive
- Partial-read protocol documented at `knowledge/operational-patterns/state-management/bootstrap-read-pattern.md` (new KB card) — specifies per-file read pattern with exact `limit` values + escalation to full read

**Acceptance criteria**:
- Hook test: intentionally bloat `current-task.md` to 101 lines → pre-commit blocked with clear error
- Un-bloat → commit passes
- Bootstrap read pattern KB card exists + linked from `CLAUDE.md` bootstrap section
- `progress.md` can grow to any size without commit blocked (verify by appending a test line and committing — not a hook violation)

**Estimated cost**: ~4K tokens

### P4 — Protocol docs + LL integration audit

**Deliverables**:
- `CLAUDE.md` §Bootstrap Protocol rewritten: specifies partial-read pattern per file, cheap-to-expensive cascade framing, explicit `Read(file, limit=N)` invocations
- `knowledge/operational-patterns/state-management/filesystem-patterns.md` v3.3 — adds "Cheap-to-Expensive Bootstrap Cascade" section, reframes "agentically flexible" to clarify it means full-file unbounded + T1-section bounded-by-convention
- `knowledge/operational-patterns/state-management/cc-memory-layer-alignment.md` — NEW KB card (from prior-session deferred list), maps CAB state files to CC's 7 memory layers, documents "wrapper philosophy" (LL-11) applied to runtime memory, documents CC auto-memory directory location at `~/.claude/projects/<slug>/memory/` and its exclusion of CLAUDE.md content
- `notes/metrics/ll-integration-audit.md` — audit report listing each LL-01 through LL-28 with columns: `woven_in_skill` (which skills reference/invoke the LL), `woven_in_hook` (which hooks enforce the LL), `status` (WOVEN / PARTIAL / PASSIVE), `gap_action` (recommendation for passive ones)

**Acceptance criteria**:
- `CLAUDE.md` bootstrap section specifies exact `Read` tool invocations with `limit` parameter
- Two new KB cards exist + linked from `knowledge/INDEX.md`
- LL audit covers all 28 LLs, categorization defensible by grep evidence
- Audit exposes at least 3 passive-only LLs → logged as follow-on TODO items (separate task, not in this plan)

**Estimated cost**: ~10K tokens

### P5 — Validation + LL-29 draft

**Deliverables**:
- Re-run `hooks/scripts/bootstrap-cost.sh` → appends post-fix row to `notes/metrics/bootstrap-cost-log.md`
- Comparison table (baseline vs post-fix) in commit message
- **LL-29** drafted in `notes/lessons-learned.md` — "Partial-read bootstrap cascade preserves flexibility without enforcement" with root-cause analysis of why v1 plan (hard limits) was wrong and v2 (partial reads) is correct
- **LL-30 candidate status** in TODO unchanged — still awaiting Global CLAUDE.md v2 upgrade to validate
- Two-commit session close per LL-26 pattern: work commit → state refresh commit referencing work commit's hash

**Acceptance criteria**:
- Post-fix T1 bootstrap cost: **<15K tokens** (target 60%+ reduction from ~40K baseline)
- Stretch: **<10K tokens** (75%+ reduction)
- LL-29 draft present in `lessons-learned.md`
- User reviews metrics + LL-29 before final close (HITL-4)

**Estimated cost**: ~4K tokens

## Total Cost Estimate

**~32K tokens / ~90 minutes / 5 phases** — single session scope.

## HITL Gates

- [X] **HITL-1**: User reviews this plan (passed via 2026-04-11 dialogue; user said "proceed" after v2 refinement integrating user feedback on hard limits)
- [ ] **HITL-2**: User reviews refactored `current-task.md` + `progress.md` structure before P2 commit
- [ ] **HITL-3**: User reviews hook enforcement (P3 pre-commit hook) before merging — affects all future commits
- [ ] **HITL-4**: User reviews pre/post bootstrap cost metrics + LL-29 draft before task close

## Risks & Mitigations

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | P2 refactor of `current-task.md` to <100 lines loses semantically important detail | Medium | Medium | Move detail to referenced impl-plan file; link, don't delete. HITL-2 inspection catches fidelity loss. |
| R2 | `progress.md` "Current Position" top-section drifts over future sessions because it's convention-not-enforced | High | Medium | Instrumentation (P1) makes drift visible; P5 validation establishes baseline; Session 30+ bootstrap checks detect drift before compounding. |
| R3 | Partial-read `Read(file, limit=100)` misses critical tail content | Medium | Low | Convention: newest/most-load-bearing content at top; tail is historical narrative that's rarely load-bearing for bootstrap. Escalation to full read on demand is always available. |
| R4 | LL-28 emergence writes bypass partial-read pattern by appending to tail during active session | Medium | Medium | LL-28 fallback-recovery protocol update (added in P4) specifies emergence writes go to top "Current Position" append zone, not tail. Documented convention only — not enforced. |
| R5 | LL audit (P4) reveals most LLs are passive-only, making L4 "load on demand" unsafe | High | Medium | Audit is diagnostic; if gap is large, this plan's P5 completes but LL-29 draft explicitly notes the precondition failure. Actual LL weaving becomes follow-on task — plan does NOT mandate fixing the gap, only measuring it. |
| R6 | Pre-commit hook for `current-task.md` blocks legitimate commits during P2 itself | High | Low | P2 executes BEFORE P3 — compress first, enforce after. Temporal ordering prevents self-block. |

## Out of Scope (explicit)

- Hard limits or enforcement hooks on `progress.md` / `TODO.md` / `lessons-learned.md` file sizes (user directive: agentic flexibility)
- Mandatory archive rollover protocol (agentic judgment, no hard trigger)
- New session-transfer artifact type (HydroCast style) — deferred, would be its own architectural decision
- `dream-consolidation` skill (from prior-session deferred list)
- Actually weaving passive LLs into skills/hooks (P4 audits, follow-on tasks prescribe)
- Global CLAUDE.md v2 upgrade (separate queued task)
- Phase D HydroCast comparison (blocked by this task)
- RAS-exec / HydroCast policy propagation of any changes made here

## Dependencies

- **Blocks**: Phase D HydroCast comparison (next session must bootstrap cleanly)
- **Blocked by**: Nothing — all evidence gathered, user approval received, no external dependencies
- **Parallelization**: P4 (docs) can draft concurrently with P2 (refactor) execution, but must commit in sequence

## Reference Files

- Baseline state files: `notes/current-task.md`, `notes/progress.md`, `notes/TODO.md`, `notes/lessons-learned.md`
- Prior-session findings source: `C:\Users\daniel.kang\.claude\projects\c--Users-daniel-kang-Desktop-Automoto-cc-architecture-builder\c1f13ecc-4e09-45fa-a3e3-a9517f739eae.jsonl` (message idx 136)
- Memory reference: `notes/references/How Anthropic Built 7 Layers of Memory and a Dreaming System for Claude Code  (video breakdown).md`
- Architecture KB: `knowledge/operational-patterns/state-management/filesystem-patterns.md`
- Session bootstrap config: `CLAUDE.md` §State Management
- Hook scripts: `hooks/scripts/`

---

## Session Log

### Session 29 (2026-04-11) — P1 landed

**Commits**: `8dfef75 feat(bootstrap): P1 instrumentation — bootstrap-cost.sh + baseline log`

**What landed**:
- `hooks/scripts/bootstrap-cost.sh` — Git Bash compatible, pure bash, zero deps. CSV row to stdout (11 fields), human-readable table to stderr. Token heuristic: `bytes / 4` (BPE approximation, directional not absolute). Verified 3× with exit 0.
- `notes/metrics/bootstrap-cost-log.md` — markdown table log with two rows:
  - `session-28-bootstrap`: 41,081 tokens (recovered from `git show c24968b` — the state that motivated this task)
  - `session-29-pre-p2`: 39,286 tokens (post current-task.md compression + recovery-backfill commit `698eb4e`)

**Deviations from impl plan**: None structural. Actual baseline (41,081) is 3.8% higher than the ~39,575 figure quoted in the recovery artifact, which itself was an estimate. The script's measurement is authoritative going forward.

**Unexpected finding — P4-relevant**: `lessons-learned.md` is 59 lines but 28,852 bytes → **~489 chars/line average**, making it the **3rd-largest state file by token weight** despite being the smallest by line count. The LL-25 "≤300 lines" policy uses line count as the proxy metric — it misses dense-line files entirely. **P4's LL audit and any future state-file size policies must factor byte/token weight, not just line count.** This finding would not have been visible without P1's dual-metric capture — measurement is self-validating.

**Empirical confirmation of P2 necessity**: Net bootstrap delta from current-task.md compression + recovery-backfill is only **−1,795 tokens (−4.4%)**. This empirically validates the v2 thesis that single-file compression is insufficient — partial-read cascade is required for meaningful reduction.

**Session 29 meta-observations**:
- Non-standard 3-file cold-start protocol worked as designed (~8K tokens vs ~40K). Ending session ~18K tokens into context budget, well under any pressure point.
- `git show <sha>:<path>` as retroactive state measurement is a reusable pattern for any future drift-detection work — full timeseries can be reconstructed from commit history without needing to re-run prior sessions.
- No LL-26 two-commit dogfooding per Session 28 recovery directive. Single commit for P1 work; this state-close is a separate cosmetic commit (current-task.md phase update + this session-log entry).

**Next session entry point**: Session 30 executes P2 (the hinge). Cold-start protocol remains non-standard per this file + current-task.md + recovery artifact only. HITL-2 gate before P2 commit.
