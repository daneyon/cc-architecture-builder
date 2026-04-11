# Current Task: CAB Source-of-Truth Consolidation + HydroCast State Mgmt Harmonization

**Status**: Phases A, B, and C (full scope: agents + commands + skills) complete. Phase A landed in `62bf4a9`, Phase 5b state refresh in `726c50b`, Phase B.5 pushed clean. Phase C.1 inventory completed Session 26, LL-27 shadowing discovered, session died mid-dialogue on HITL-3. Session 27 recovered via transcript-tail backfill (LL-27 + LL-28 in `436ffbd`, state refresh in `bc9ce69`), user confirmed full Option B scope, and all 8 duplicates removed from `~/.claude/`: 2 agents + 4 commands + 2 skills. Global `CLAUDE.md` Extension Registry updated to reflect post-cleanup reality with LL-27 shadowing rule permanently documented. CAB plugin is now the single authoritative source for all overlapping extensions. Phase D (HydroCast comparison) is the next HITL gate.
**Started**: 2026-04-10 (Session 25 plan; Session 26 execution; Session 27 recovery + full Option B execution)
**Branches**: `master` (CAB, local-only state refreshes ahead of origin; user directive: no push needed for solo workflow — still honored), `feat/plugin-first-migration-2026-04-09` (HydroCast, unchanged)
**Prior task**: LL-25 state management reform (`302f872`, PUSHED) exposed tense hygiene gap; LL-26 solved tense staleness; LL-27 captured shadowing; LL-28 captured emergence staleness; Session 27 proved the shadow-cleanup pattern on the full duplication surface (not just agents) and validated LL-27's architectural claim that plugin-provided extensions are the correct authority layer.
**Next action**: Phase D — HydroCast strategic comparison (read-only, fan-out to specialists). After Phase D completes, execute **Global CLAUDE.md v2 Architecture Upgrade** (queued 2026-04-11 Session 27 per user directive; full rationale + proposal in `notes/TODO.md` under "Global CLAUDE.md v2 Architecture Upgrade" section; origin = dialogue identifying Extension Registry as a Policy/Inventory category error wasting ~15% of global memory budget). Then HITL-4 + Phase E remediation + Phase F close. Lazy-load protocol question and LL-29 quality-over-tokens candidate deferred to post-Phase-F review.

## Design Decisions (User-Confirmed 2026-04-10)

- **DD-1**: Two-commit pattern = default for session close. Token cost ~130/session (0.065% of budget) = negligible. Tense-neutral single-commit documented as lightweight fallback for mid-session state touches.
- **DD-2**: Sync-upstream HITL default = present findings + recommendation, user approves. Minor auto-commit escape hatch for truly trivial deltas (whitespace, typos, already-aligned content) with clear log trail.
- **DD-3**: HydroCast comparison-first approach — after comparison (Phase D), if CAB has genuinely captured everything HydroCast's 3-layer practice offers AND nothing unique-to-HydroCast is advantageous, full restructure to align with CAB is pre-approved. Otherwise preserve HydroCast-unique value.
- **DD-4**: Commit-per-phase = default guidance (not prescription) in CAB standardization. Adds item to Phase A: weave into `executing-tasks` skill as recommended cadence.
- **DD-5**: Global dedup = delete confirmed duplicates only; non-overlapping extensions stay global. If global copies are OLDER than CAB (expected case), just delete. If global happens to be NEWER, sync upstream first (rare case, still HITL).

---

## Objective

Three linked goals sequenced so CAB is hardened and consolidated BEFORE being applied to HydroCast:

1. **Phase A — CAB protocol hardening (tense hygiene)**: Structurally prevent recurrence of Session 24's hygiene lag (state files frozen with "pending commit" language). Weave the fix into skills/protocols/hooks so it cannot recur.
2. **Phase C — CAB source-of-truth consolidation**: Remove duplicate global `~/.claude/` copies of CAB commands (and overlapping skills/agents) so CAB plugin becomes the single authoritative source. Eliminates drift risk and operator confusion.
3. **Phases D-E — HydroCast state mgmt harmonization**: Strategically compare CAB framework vs HydroCast's battle-tested 3-layer LC-08 lineage. Apply CAB standardizations where beneficial, preserve HydroCast-unique value, extract upstream opportunities. Enable user to resume HydroCast work on a harmonized foundation.

## Root Causes Summary

### Gap 1 — State File Tense Hygiene

Session 24 committed work + state files together in `302f872`. State files said `"EXECUTED ✅ — Ready for commit + session close"` — true at write time, stale the instant the commit landed. No protocol layer catches this:

- `skills/session-close/` Step 4 commits state updates but doesn't distinguish work-commit from state-refresh-commit
- `skills/executing-tasks/` Phase 5 says update state AFTER commit — but doesn't require a second commit for the refresh, nor forbid "pending" tense
- Pre-push hook regex doesn't include tense markers (`pending commit`, `ready for commit`)
- No documented tense-hygiene convention in `filesystem-patterns.md`

This is exactly the failure mode LL-25's "Lessons-Referenced Protocols" pattern was created to prevent — and it slipped through because LL-25 itself was the work being committed.

### Gap 2 — Global↔CAB Command/Skill Duplication

Global `~/.claude/commands/` contains direct copies of 4 CAB commands (`execute-task`, `commit-push-pr`, `context-sync`, `techdebt`). Global `~/.claude/skills/` and `agents/` also overlap with CAB (`architecture-analyzer`, `planning-implementation` skills; `orchestrator`, `verifier` agents). Impact:

- Two copies drift — already observed: global commands lag behind CAB enhancements
- Operator confusion: unclear which version triggers on `/execute-task`
- Violates CAB's core principle that it IS the source of truth for architectural extensions
- Originally made sense pre-plugin-marketplace; now obsolete since CAB is registered globally via `enabledPlugins`

## Acceptance Criteria

### Phase A — CAB Protocol Hardening ✅ (landed in `62bf4a9`)

- [X] AC-1: LL-26 entry drafted + added to `notes/lessons-learned.md` (tense hygiene + two-commit session close pattern) — `62bf4a9`
- [X] AC-2: `filesystem-patterns.md` gained "State File Tense Hygiene" section (v3.2, approved/forbidden patterns + two-commit protocol) — `62bf4a9`
- [X] AC-3: `skills/session-close/SKILL.md` revised with explicit two-phase close (work commit → state refresh commit) + tense checklist + work-vs-state classification rule — `62bf4a9`
- [X] AC-4: `skills/executing-tasks/SKILL.md` Phase 5 split into 5a/5b/5c; requires post-commit state refresh + second commit; classification table added — `62bf4a9`
- [X] AC-5: `hooks/scripts/pre-push-state-review.sh` regex refactored (v2) — two pattern types (draft labels require colon-suffix; tense markers require status-line anchoring); case-insensitive tense matching — `62bf4a9`
- [X] AC-6: `skills/executing-tasks/SKILL.md` Phase 3 adds commit-per-phase cadence as recommended guidance (DD-4, not prescription) + defer-state-updates rule — `62bf4a9`
- [X] AC-7: Smoke test — retroactively validated against Session 24's `**Status**: EXECUTED ✅ — Ready for commit + session close` (caught), plus 6 scenarios: labels/prose/table-cells/status-lines/lowercase/descriptive all correctly classified — Session 26 A.7

### Phase B — CAB Finalization ✅ (landed in `726c50b` + clean push)

- [X] AC-7: CAB `current-task.md` + `progress.md` refreshed using Phase A protocols — `726c50b` (Session 26) + this Session 27 backfill
- [X] AC-8: LL-25 artifacts smoke-tested (hook runs, skill frontmatter valid, gitignore patterns behave) — verified in Session 26
- [X] AC-9: Push decision resolved + executed — `CAB_SKIP_PREPUSH_REVIEW=1` bypass dependency eliminated by A.5 regex refinement; clean push proceeded without bypass
- [X] AC-10: CAB `master` pushed to origin (Session 26 end), `git status` clean, `git log origin/master..master` empty at push time

### Phase C — Global↔CAB Source-of-Truth Consolidation ✅ (all ACs landed Session 27, 2026-04-11)

- [X] AC-11: Diff each global copy against CAB version — done in Session 26 Phase C.1, all 8 duplicates confirmed as CAB strict supersets, no sync-upstream needed. `execute-task.md` allowed-tools delta confirmed as intentional CAB cleanup, not regression.
- [X] AC-12: Delete duplicate global commands `execute-task`, `commit-push-pr`, `context-sync`, `techdebt` — DONE (Session 27, 2026-04-11). `~/.claude/commands/` is now empty; all 4 commands resolve via CAB plugin path.
- [X] AC-13: Delete duplicate global skills `architecture-analyzer`, `planning-implementation` — DONE (Session 27, 2026-04-11). Both skill directories (including `planning-implementation/assets/` subdir with 2 template files) removed via file-by-file + rmdir cascade (security gate blocks `rm -rf`, LL-14 working correctly). Remaining global skills: 8 non-CAB (assessing-quality, claude-docs-helper, designing-workflows, presentation-outline, readme-generator, slide-designer, token-optimizer, visualizing-data).
- [X] **AC-14**: Delete duplicate global agents `orchestrator`, `verifier` — DONE (Session 27, 2026-04-11). `~/.claude/agents/orchestrator.md` + `~/.claude/agents/verifier.md` removed. Remaining global agents: code-reviewer, debugger-specialist, general-researcher (CAB does not provide these).
- [X] AC-15: Update global `~/.claude/CLAUDE.md` Extension Registry — DONE for all three categories. Agents=3 (with LL-27 past-tense incident note), Skills=8 (with past-tense "removed in Phase C.2" warning for CAB-duplicates), Commands=0 (with same past-tense warning). LL-27 shadowing rule section added as permanent policy for all future plugin adoption.
- [ ] AC-16: Smoke test — open fresh CC session, verify `/execute-task` and friends still resolve via CAB plugin path (now that global copies are gone, resolution path is forced through the plugin). **Deferred to next session cold-start** — this session has mutated `~/.claude/` and continuing verification in-session wouldn't prove anything the plugin registration check hasn't already proven.
- [~] **AC-17 (from LL-27)**: Verify CAB's plugin orchestrator is now the active resolution target. Partial verification done this session: `settings.json` shows `cab@cab: True` in `enabledPlugins` and `cab` in `extraKnownMarketplaces`; plugin discovery chain is intact. Full behavioral verification (e.g., observing that the orchestrator's Session 26+ R2 updates are now active in operational output) deferred to next cold-start session alongside AC-16.

### Phases D-E — HydroCast Harmonization

- [ ] AC-18: Strategic comparison doc written at HydroCast `notes/cab-vs-hydrocast-state-mgmt-comparison-2026-04-10.md` — answers the 7 review questions from `cab-state-mgmt-review-brief.md`; side-by-side matrix; HydroCast-unique value; CAB-unique value; harmonization recommendations with HITL gates; upstream opportunities (renumbered from AC-17 on 2026-04-11 to resolve collision with Phase C's AC-17 LL-27 follow-on)
- [ ] AC-19: HITL gate — user scopes harmonization approvals before any HydroCast structural change
- [ ] AC-20: HydroCast Phase 5 P1 KB frontmatter fixes landed (3 files + `knowledge/INDEX.md` reference)
- [ ] AC-21: Approved harmonization changes applied (docs + protocols only; no structural file moves unless explicitly approved)
- [ ] AC-22: HydroCast state files coherent post-change (`current-task.md` <40 lines, `progress.md`/LC/D intact, bootstrap protocol still works)
- [ ] AC-23: Upstream HydroCast→CAB opportunities added as CAB TODOs (candidates: D96 transfer doc protocol, LC/D numbering, ephemeral session layer)
- [ ] AC-24: HydroCast feat branch committed (incremental subcommits) and pushed; uncommitted pre-existing work disambiguated (not bundled)

## Subtasks

### Phase A: CAB Protocol Hardening

- A.1 LL-26 draft (root cause + corrective protocol + category `proc`)
- A.2 `filesystem-patterns.md` — "State File Tense Hygiene" section
- A.3 `skills/session-close/SKILL.md` — two-phase close pattern
- A.4 `skills/executing-tasks/SKILL.md` — Phase 5 post-commit refresh
- A.5 `hooks/scripts/pre-push-state-review.sh` — tense marker regex extension. **CRITICAL nuance discovered in Session 25 smoke test**: naive regex on "pending commit" matches both (a) actual stale tense in status fields and (b) legitimate documentation/references to the concept (e.g., this very plan references "pending commit" descriptively). The regex must distinguish. Recommended: match only in status-line contexts like `^\*\*(Status|Phase|Gate)\*\*:.*pending commit` or similar anchored patterns. Alternatives considered: (i) unambiguous marker keyword `PENDING_COMMIT_REFRESH`, (ii) skip lines inside code fences/backticks. Anchored status-line matching is preferred because status lines are the actual failure surface; descriptive prose is fine.
- A.6 `skills/executing-tasks/SKILL.md` — add commit-per-phase cadence as recommended guidance (DD-4, not prescriptive)
- A.7 Smoke test: retroactive validation against Session 24 files (verify Session 24's stale `"EXECUTED ✅ — Ready for commit + session close"` would have been caught by the anchored regex)

### Phase B: CAB Finalization

- B.1 Apply Phase A protocols → refresh `current-task.md` + `progress.md`
- B.2 LL-25 artifact smoke tests
- B.3 Resolve push decision
- B.4 Commit Phase A+B: `feat: state file tense hygiene protocol (LL-26)`
- B.5 Push master (with bypass env var if hook false-positives)

### Phase C: Global↔CAB Deduplication

- C.1 Inventory + diff global `commands/`, `skills/`, `agents/` vs CAB equivalents
- C.2 Sync upstream to CAB any global improvements not yet reflected
- C.3 Delete confirmed duplicates from `~/.claude/`
- C.4 Update global `~/.claude/CLAUDE.md` Extension Registry
- C.5 Smoke test in fresh CC session
- C.6 Commit CAB-side changes (if sync-upstream happened); record dedup in CAB progress

### Phase D: HydroCast Strategic Comparison (Read-Only)

- D.1 Read HydroCast Tier 1 (learned-corrections.md, design-decisions.md D96, CLAUDE.md §Persistent Memory Architecture)
- D.2 Read HydroCast Tier 2 (current-task.md, progress.md, session-24-transfer.md exemplar)
- D.3 Read CAB baseline post-Phase-A (filesystem-patterns.md, CLAUDE.md §State Management)
- D.4 Write comparison doc answering the 7 review questions

### Phase E: HydroCast Remediation (HITL Gate)

- E.1 Present comparison doc → HITL scoping
- E.2 Phase 5 P1 KB frontmatter fixes (independent, low-risk — can run in parallel)
- E.3 Apply approved harmonization changes
- E.4 Refresh HydroCast state files using CAB's new tense hygiene protocol
- E.5 Commit incrementally on feat branch, push

### Phase F: CAB Follow-On

- F.1 Update CAB TODO.md — mark LL-25 follow-ons, add upstream HydroCast patterns
- F.2 Final CAB commit + push

## Verification

- **CAB clean**: `git status` → clean working tree
- **CAB pushed**: `git log origin/master..master` → empty
- **CAB tense hygiene**: `grep -rEn "pending commit|ready for commit" notes/` → no matches
- **Global dedup**: duplicate files removed from `~/.claude/commands/`, `skills/`, `agents/`
- **Slash command resolves**: fresh CC session `/execute-task` still works (via CAB plugin path)
- **HydroCast clean**: `git status` shows only intentional changes
- **HydroCast pushed**: feat branch commits visible on origin
- **Comparison doc exists**: `HydroCast/notes/cab-vs-hydrocast-state-mgmt-comparison-2026-04-10.md`
- **Cold-start sim**: read CAB `current-task.md` → no stale tense markers found

## HITL Gates

- **HITL-1**: User reviews this plan → approves Phase A-C scope before execution begins
- **HITL-2**: User reviews Phase A deliverables before commit (tense protocol changes affect all future CAB work)
- **HITL-3**: User reviews Phase C dedup inventory (sign-off on what to delete from global)
- **HITL-4**: User reviews strategic comparison doc → scopes HydroCast harmonization approvals

## Risks / Out of Scope

- **Risk**: HydroCast feat branch has pre-existing modified files (marketplace.json, environment.yml, KB file, state files) + untracked items (diagrams, model tier1 JSONs, strategic assessment notes). Must disambiguate before committing to avoid bundling unrelated work.
- **Risk**: Pre-push hook false-positives on descriptive "WIP" prose — known issue, bypass with env var for this task, regex refinement stays on TODO (LL-25 follow-on)
- **Risk**: Phase C deletion irreversible if CAB plugin is later disabled — mitigated by CAB being the source of truth anyway (backup exists in CAB repo history)
- **Risk**: If Phase C diff reveals global copies have uncommitted improvements, sync-upstream may expand scope; stop and re-plan if >2× estimate
- **Out of scope**: RAS-exec harmonization (deferred per existing TODO), full CC memory layer KB card deep-dive, dream-consolidation skill concept, HydroCast structural file moves unless explicitly approved in HITL-4

## Reference Files

- **Session-close skill**: `skills/session-close/SKILL.md`
- **Executing-tasks skill**: `skills/executing-tasks/SKILL.md`
- **Filesystem patterns KB**: `knowledge/operational-patterns/state-management/filesystem-patterns.md`
- **Pre-push hook script**: `hooks/scripts/pre-push-state-review.sh`
- **Global dedup targets**: `~/.claude/commands/`, `~/.claude/skills/`, `~/.claude/agents/`
- **Global CLAUDE.md registry**: `~/.claude/CLAUDE.md`
- **HydroCast review brief**: `../Flood-Forecasting/notes/cab-state-mgmt-review-brief.md`
- **HydroCast LC lineage**: `../Flood-Forecasting/notes/memory/learned-corrections.md`
- **HydroCast D96**: `../Flood-Forecasting/notes/memory/design-decisions.md`
