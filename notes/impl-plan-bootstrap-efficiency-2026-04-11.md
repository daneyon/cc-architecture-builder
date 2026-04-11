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
- `notes/bootstrap-cost-log.md` — append-only log of measurements, baseline row for Session 28 recorded

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
- **DEFERRED (Session 32)**: `ll-integration-audit.md` — standalone one-time audit deferred as follow-on work; replaced in P4 scope by a lighter Classification column added directly to `notes/lessons-learned.md` (see LL refactor below)

**Acceptance criteria**:
- `CLAUDE.md` bootstrap section specifies exact `Read` tool invocations with `limit` parameter
- Two new KB cards exist + linked from `knowledge/INDEX.md`
- LL audit covers all 28 LLs, categorization defensible by grep evidence
- Audit exposes at least 3 passive-only LLs → logged as follow-on TODO items (separate task, not in this plan)

**Estimated cost**: ~10K tokens

### P5 — Validation + LL-29 draft

**Deliverables**:
- Re-run `hooks/scripts/bootstrap-cost.sh` → appends post-fix row to `notes/bootstrap-cost-log.md`
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
- Memory reference: `notes/_archive/references/How Anthropic Built 7 Layers of Memory and a Dreaming System for Claude Code  (video breakdown).md` (archived 2026-04-11 Session 32 during flat-notes cleanup)
- Architecture KB: `knowledge/operational-patterns/state-management/filesystem-patterns.md`
- Session bootstrap config: `CLAUDE.md` §State Management
- Hook scripts: `hooks/scripts/`

---

## Session Log

### Session 29 (2026-04-11) — P1 landed

**Commits**: `8dfef75 feat(bootstrap): P1 instrumentation — bootstrap-cost.sh + baseline log`

**What landed**:
- `hooks/scripts/bootstrap-cost.sh` — Git Bash compatible, pure bash, zero deps. CSV row to stdout (11 fields), human-readable table to stderr. Token heuristic: `bytes / 4` (BPE approximation, directional not absolute). Verified 3× with exit 0.
- `notes/bootstrap-cost-log.md` — markdown table log with two rows:
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

### Session 30 (2026-04-11) — P2 landed

**Commits**: This session's single P2 commit (see git log for hash).

**What landed**:
- `notes/progress.md`: Session 30 T1 section (Current Position → Phase Status → Next-Action Queue split into "This Session" / "Session 31" / User Directives / Reference Artifacts pointer); `<!-- T1:BOUNDARY -->` at line 50; old Session 29 recovery-close T1 content migrated into Historical Narrative as `### Session 29 Recovery Close (archived T1 snapshot)`; the duplicate `## Current Position` header at original line 46 renamed to `## Session 27 Current Position (archived)` to eliminate markdown/grep ambiguity.
- `notes/TODO.md`: `<!-- T1:BOUNDARY -->` at line 38 after Top Priorities section (already T1-compliant by accident from Session 29 — minimal change needed).
- `notes/lessons-learned.md`: `<!-- T1:BOUNDARY -->` at line 49 after LL-28, with an expanded HTML comment flagging the file as a KNOWN P4 TARGET (semantic breadcrumb only, no cost reduction — all 28 LLs are Active and limit=60 captures ~98% of the file at ~7,134-7,261 tokens).
- `notes/current-task.md`: updated to Session 31 orientation (status line, cold-start protocol section, phase status table, cadence, HITL gate checkboxes); added `<!-- T1:BOUNDARY -->` at line 80 for tooling consistency across all 4 state files (redundant with the <100 line hard gate but aids grep-based audits). Still 81 lines, well under target.
- `notes/impl-plan-bootstrap-efficiency-2026-04-11.md`: this Session 30 log entry.

**Pre/post byte delta** (zero semantic content loss):
- Pre-P2 (Session 29 close): 157,640 bytes / 1,551 lines
- Post-P2 (this commit): 161,211 bytes / 1,584 lines
- Delta: +3,571 bytes / +33 lines (+2.3%)
- All growth is additive: 4 boundary markers + Session 30 T1 content + archived Session 29 block + expanded lessons-learned.md boundary comment + current-task.md Session 31 orientation. No content was deleted; Session 29 recovery-close narrative was migrated into the Historical Narrative section rather than discarded.

**Full-file post-P2 bootstrap cost** (via `bootstrap-cost.sh`): 39,923 tokens. This is only a 2.8% reduction from the 41,081-token Session 28 baseline because full-file reads still pull in everything — P2's savings come from the partial-read cascade, not from file shrinkage. This is the expected and designed behavior.

**Partial-read cost estimate (post-P2, pre-P3/P4 real bootstrap protocol)**:
- `current-task.md` full read: ~1,745 tokens (81 lines, entire file is T1)
- `Read(progress.md, limit=100)`: ~2,222 tokens (100 of 945 lines = 10.6%)
- `Read(TODO.md, limit=80)`: ~1,638 tokens (80 of 497 lines = 16.1%)
- `Read(lessons-learned.md, limit=60)`: ~7,261 tokens (60 of 61 lines = 98% — density bottleneck)
- **Total partial-read**: ~12,866 tokens
- **Reduction vs 41,081 baseline**: **69%** — hits P5 `<15K` target.
- **Stretch `<10K` target**: blocked by lessons-learned.md density. Scoped as P4 sub-deliverable (compact-index vs verbose-detail table split).

**Deviations from impl plan**: P2 grew slightly in scope to include design-decision polish after HITL-2. Four of the five design decisions introduced at HITL-2 were applied:
1. Phase Status table format kept as-is (no change, my recommendation)
2. Next-Action Queue split into "This Session" / "Session 31" subsections (+2 lines in progress.md)
3. Boundary marker added to current-task.md for tooling consistency (+2 lines)
4. Reference Artifacts in progress.md tightened to one-line pointer to current-task.md §Reference Artifacts (-5 lines net)
5. lessons-learned.md boundary retained but HTML comment rewritten to explicitly flag the density bottleneck as a P4 target (+1 line, ~500 bytes of explanatory comment)

**Session 30 meta-observations**:
- Non-standard 3-file cold-start protocol continues to work cleanly (~8K tokens budget, ~22% context headroom at end of session)
- User's HITL-2 feedback on #5 was sharp and correct — the boundary marker on lessons-learned.md doesn't reduce partial-read cost when all LL entries are Active. The honest framing is that the boundary is a semantic breadcrumb that future tooling (P4 compact-index split) will cash in. Documenting this in the boundary comment itself prevents the loss of context between Session 30 and P4.
- Discovered and resolved a small LL-28 recurrence: Session 29's recovery backfill had left TWO `## Current Position` headers in progress.md (line 11 + line 46) because the backfill appended new content without renaming the old section. P2 caught and fixed this via header rename. Adds weight to the LL-28 "event-triggered state writes" protocol candidate — reactive backfill produces invisible artifacts that compound across sessions.
- `.mcp.json` dangling deletion still in git status (not staged for P2 commit, scope discipline — carried over from Session 28). Flagged for user awareness; address in a separate scope-limited commit if desired.
- No LL-26 two-commit dogfooding per directive #5. Single commit includes both P2 work + state-update (progress.md + current-task.md + impl plan log entry all together).

**Next session entry point**: Session 31 executes P3 (current-task.md <100 line pre-commit hook) + P4 (CLAUDE.md rewrite + 2 new KB cards + LL integration audit incl. compact-index/verbose-detail LL table split) + P5 (post-fix metrics + LL-29 draft + task close). Cold-start protocol remains non-standard until P3/P4 lands the real fix; partial-read cascade is available for on-demand use. HITL-3 gate before P3 hook commit; HITL-4 gate on post-fix metrics before task close.

### Session 31 (2026-04-11) — P3 landed; early-close on context exhaustion

**Commits**: `731bea0 feat(bootstrap): P3 enforcement — current-task.md <100 line hard gate + partial-read KB card`

**What landed**:
- `hooks/scripts/enforce-current-task-budget.sh` — dual-mode dispatcher (CC PreToolUse JSON-stdin OR git native pre-commit tty-stdin) via `[[ -t 0 ]]` test + empty-stdin + non-JSON fallback cascade. Budget: 100 lines hard cap on `notes/current-task.md`. `wc -l` counting (no filters). Exit 0/1/2 semantics mirror `pre-push-state-review.sh` sibling precedent.
- `hooks/hooks.json` — second `PreToolUse/Bash` entry registered alongside pre-push hook. NOTE: CC hooks.json is cached at session start — the new registration won't take effect until S32. Git pre-commit shim path is live immediately.
- `.git/hooks/pre-commit` — 5-line `exec` shim delegating to the source script. Per-clone install, not tracked (documented in KB card).
- `knowledge/operational-patterns/state-management/bootstrap-read-pattern.md` — NEW KB card, 160 lines, under 300 cap. Documents L1-L4 cheap-to-expensive cascade, T1 boundary marker convention, enforcement surface (hard vs soft gates), density bottleneck (lessons-learned.md ~489 chars/line), escalation-to-full-read criteria, common failure modes. Wrapper philosophy + source frontmatter.
- 3 INDEX updates: `state-management/INDEX.md` (3→4 files), `operational-patterns/INDEX.md` (13→14 files, v3.1 revision note, directory tree + "When to Use" table entry added), `knowledge/INDEX.md` (36→37 files).

**Test matrix (7/7 pass)**: direct-mode pass (81L), direct-mode block (106L + formatted reason), direct-mode restore pass, CC-mode `git commit` JSON pass (81L), CC-mode `ls -la` JSON pass-through, git pre-commit shim delegation, CC-mode + bloat composition block (106L). Real-world validation fired on this session's `git commit 731bea0` — the shim path allowed the commit cleanly.

**Scope excluded**: `.mcp.json D` still in git status — 4th session carrying the same stale deletion. Trivial to clean up but blurs scope boundaries; flagging for task-close commit or a standalone cleanup.

**Deviations from impl plan**: None structural. P3 scope grew by ~2K to cover 3 INDEX updates (`state-management/`, `operational-patterns/`, master `knowledge/`) which weren't explicitly enumerated in the P3 deliverable list but are required by KB conventions. P4's scope was reassessed at HITL-3 close: original estimate ~10K, actual estimate ~20-22K due to LL audit's grep-heavy nature and the Session 30 add-on (LL table compact-index/verbose-detail split).

**CRITICAL S31 finding — assistant-side context estimation is unreliable**:
- After P3 commit, I presented a budget check estimating ~52K / 200K used (~26%), projecting ~79K / 40% at end of P4+P5.
- **Actual user report: ~6% remaining (~188K used, ~94%)**. My estimate undershot by a factor of ~3.6×.
- Likely undercounts: (a) global CLAUDE.md + all 7 rule files (real ~15-20K, I estimated ~10K); (b) full skills/agents/plugins listing injected via system-reminder (~8-10K, I estimated ~3K); (c) MCP/tool schema overhead (~8-12K, I estimated ~6K); (d) cold-start file contents were larger than estimated; (e) 6 cycles of Bash tool stdin/stdout for hook testing each carrying full output into context.
- **Implication for P5 LL-29 draft**: the v2 partial-read cascade is NECESSARY but NOT SUFFICIENT. Bootstrap cost measured by `bootstrap-cost.sh` covers only the 4 state files, which are the tip of the iceberg. **Full session context at cold-start is dominated by harness overhead** (system prompt + CLAUDE.md + rules + plugin listings + tool schemas), not user state files. This is load-bearing for LL-29.
- **Operational correction**: at each phase boundary, check actual budget via `/context` slash command or ask user for budget remaining, instead of self-estimating. Self-estimates drift by 3× or more — this is the second instance of "prompt too long" class failure in this task (S28 death → S31 early-close).

**S31 meta-observations**:
- Single commit per directive #5 (no LL-26 two-commit dogfooding). P3 work commit + state-close commit = 2 commits this session, but they're sequential phase transitions, not a work/state pair for the same phase.
- The `.mcp.json D` persistence across 4 sessions (S28→S29→S30→S31) is itself a data point on scope discipline. Carry it into S32 or clean up in a standalone commit — user call.
- Hook real-world validation was partial: git pre-commit shim path tested live on `git commit 731bea0`, CC PreToolUse path deferred to S32 (hooks.json is cached).

**Next session entry point (S32)**: Cold-start with 3 files (current-task.md + this impl plan + session-28-recovery-2026-04-11.md) per current-task.md protocol. Execute P4 (5 deliverables: CLAUDE.md §Bootstrap rewrite, filesystem-patterns.md v3.3 update, cc-memory-layer-alignment.md NEW KB card, ll-integration-audit.md audit report, LL table compact-index/verbose-detail split) then P5 (bootstrap-cost.sh re-run + LL-29 draft + HITL-4). Ask user for actual context budget at each phase boundary instead of self-estimating.
