# Current Task: Wave 3 Phase 3c — Orphan Promotions + Hybrid Merges + F011 Wiring

**Status**: Phase 3b LANDED (Session 37, commits `0a7bcd8` + `5301325`). Phase 3c queued — pending next session.
**Last active**: 2026-04-24 (Session 37 close)
**Branch**: `master`
**Parent plan**: [notes/impl-plan-commands-skills-migration-2026-04-24.md](impl-plan-commands-skills-migration-2026-04-24.md)
**Mapping artifact**: [notes/commands-skills-mapping-2026-04-24.md](commands-skills-mapping-2026-04-24.md)
**Wave plan**: [notes/ux-log-wave-plan-2026-04-22.md](ux-log-wave-plan-2026-04-22.md)

---

## Next Session Pickup

### Immediate scope: Wave 3 Phase 3c

**Phase 3c deliverables** (execute next session):

1. **Orphan promotions (5 new skills per D2)** — promote orphan commands to skills:
   - `commit-push-pr` (command body) → `skills/publish-changes/SKILL.md` (or preserve name)
   - `context-sync` → `skills/sync-context/SKILL.md`
   - `kb-index` → `skills/index-kb/SKILL.md`
   - `sync-check` → `skills/check-sync/SKILL.md`
   - `techdebt` → `skills/scan-techdebt/SKILL.md`
   - **Skipped per D2**: `init-worktree` (CC built-in `--worktree` covers single-worktree case)
   - Each command becomes pure shim invoking the new skill; command names preserved per D6

2. **Hybrid merges into unified `scaffold-project` skill (per D3)** — add `--mode` extensions:
   - `scaffold-project --mode plugin` (absorbs `init-plugin` git-init + remote-wiring logic)
   - `scaffold-project --mode integrate` (absorbs `integrate-existing` Phase 1 discovery; agent handoff still command-side)
   - `scaffold-project --mode global` (absorbs `new-global` global-config scaffold)
   - `scaffold-project --mode quick` (absorbs `quick-scaffold` template-driven fast path)
   - Original commands (`init-plugin`, `integrate-existing`, `new-global`, `quick-scaffold`) become shims invoking unified skill with appropriate `--mode`
   - `quick-scaffold` skill folder removed once mode absorbed

3. **F011 Option A delegation wiring (per D4)** — `execute-task` skill Phase 1 explicitly delegates to `plan-implementation` for non-trivial work:
   - Add boundary criterion to `execute-task` SKILL.md (e.g., "plans >100 lines or requiring artifact persistence → invoke `plan-implementation`")
   - `plan-implementation` SKILL.md remains independent invocable; just becomes a documented downstream of `execute-task`
   - No code dependency; just convention + documented pointer

### Follow-on Phase 3d (after 3c validates)

- Archive wrapper commands once empirical validation confirms `/cab:<skill>` ≈ `/cab:<command>` UX equivalence (per D6 conditional approval)
- Candidates for archive after validation: 6 wrapper commands (`add-agent`, `add-command`, `add-skill`, `execute-task`, `new-project`, `validate`) + 5 new orphan-promoted shim commands

### Wave 3 Part 2 (after Phase 3d, now unblocked)

- UXL-001 (default setup protocol project-schema-first) — plan authoring conditioned on UXL-002 migration outcomes (now landed)

---

## Phase 3b Closure Summary (Session 37)

- **Commits**: `0a7bcd8` (skill renames + cross-ref sweep, 56 files) + `5301325` (wrapper trims, 2 files)
- **D5 amendment captured**: original single-word lock-in reverted to two-word verb+object default; recorded in parent plan §SME Sign-Off + mapping artifact §F012
- **Verifier**: independent PASS on all 7 acceptance criteria
- **No regressions**: stale-name grep returns only 3 protected historical-record files

---

## Pre-2026-04-22 Queued Work (unchanged, still gated)

- **Phase D — HydroCast ↔ CAB State-Management Comparison** (HARD-BLOCKED on HydroCast PR #8 merge: https://github.com/daneyon/Flood-Forecasting/pull/8). Read-only comparison; multi-agent fan-out. Preserved for post-this-cycle resumption.

---

## Reference Artifacts

- **Mapping audit**: `notes/commands-skills-mapping-2026-04-24.md` (243 lines; all 15 commands categorized; F012 rename table updated with D5-amended targets)
- **UXL-002 parent plan**: `notes/impl-plan-commands-skills-migration-2026-04-24.md` (now includes D5 amendment block in §SME Sign-Off)
- **Wave plan** (sequencing): `notes/ux-log-wave-plan-2026-04-22.md` (11 waves; Wave 2 VOID, Wave 3 Phase 3a+3b complete)
- **Pass-1 tracker**: `notes/ux-log-001-2026-04-22-pass-1.csv` (40 rows; UXL-002 still in flight — mark resolved after Phase 3d archive)
- **Auto-memory (cross-session)**: `memory/feedback_dual_pov_check.md` — dual-POV check before building; reaffirmed by D5 reversal in Session 37

<!-- T1:BOUNDARY — `current-task.md` is entirely T1 by design (<100 line hard target enforced by hooks/scripts/enforce-current-task-budget.sh). Whole file is the cold-start anchor. -->
