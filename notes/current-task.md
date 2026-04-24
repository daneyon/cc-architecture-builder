# Current Task: UX Log Tracker — Wave 3 Phase 3b+ (Commands→Skills Migration, post-Phase-3a)

**Status**: Phase 3a LANDED (fdfea25, 3c61293). Phase 3b+ pending next session — SME decisions captured; scope frozen.
**Last active**: 2026-04-24 (Session 36 close)
**Branch**: `master`
**Parent plan**: [notes/impl-plan-commands-skills-migration-2026-04-24.md](impl-plan-commands-skills-migration-2026-04-24.md)
**Mapping artifact**: [notes/commands-skills-mapping-2026-04-24.md](commands-skills-mapping-2026-04-24.md)
**Wave plan**: [notes/ux-log-wave-plan-2026-04-22.md](ux-log-wave-plan-2026-04-22.md)

---

## Next Session Pickup

### Immediate scope: Wave 3 Phase 3b

**Phase 3b deliverables** (execute next session):

1. **Wrapper command trims (6 commands)** → pure-shim form (remove duplicated logic; command body delegates to skill):
   - `/cab:add-agent` → shim wrapping `creating-components` skill
   - `/cab:add-command` → shim wrapping `creating-components`
   - `/cab:add-skill` → shim wrapping `creating-components`
   - `/cab:execute-task` → shim wrapping `executing-tasks` (renamed → `execute`)
   - `/cab:new-project` → shim wrapping `scaffolding-projects` (renamed → `scaffold`)
   - `/cab:validate` → shim wrapping `validating-structure` / `auditing-workspace` (renamed → `validate` / `audit`)

2. **Skill renames per F012 + D5 (single-word preferred; verb+action if multi-word required)**:
   - `architecture-analyzer` → `analyze-arch` (two-word; `architect` too generic)
   - `auditing-workspace` → `audit` (single-word)
   - `creating-components` → `create-components` (two-word; `create` too generic)
   - `executing-tasks` → `execute` (single-word)
   - `planning-implementation` → `plan` (single-word)
   - `scaffolding-projects` → `scaffold` (single-word)
   - `session-close` → `close-session` (verb+object)
   - `validating-structure` → `validate` (single-word)
   - Keep: `pre-push-state-review` (compound concept), `quick-scaffold` (merges into `scaffold --quick` in Phase 3c)

3. **Atomic cross-reference updates during renames**:
   - `CLAUDE.md` (project + global templates)
   - `.claude-plugin/plugin.json` component references
   - `knowledge/INDEX.md` + `knowledge/components/*.md` references
   - inter-skill references (SKILL.md bodies cross-citing other skills)
   - `agents/*.md` with `skills:` field references
   - `commands/*.md` command bodies citing skills

### Follow-on Phase 3c (after 3b validates)

- Orphan promotions (5 new skills): `commit-push-pr`, `context-sync`, `kb-index`, `sync-check`, `techdebt` (UXL-002 user directive + SME D2)
- Hybrid merges into unified `scaffold` skill with `--mode` extensions (per D3): `init-plugin`, `integrate-existing`, `new-global`, `new-project`, `quick-scaffold` all become modes of `scaffold`
- F011 Option A: `execute` skill Phase 1 delegates to `plan` skill for non-trivial plan authoring

### Phase 3d (after 3c validates)

- Archive wrapper commands once empirical validation confirms `/cab:<skill>` = `/cab:<command>` UX equivalence (per SME D6 conditional approval)

### Wave 3 Part 2 (after Phase 3d)

- UXL-001 (default setup protocol project-schema-first) — plan authoring conditioned on UXL-002 migration outcomes landing

---

## Phase 2 SME Decisions (captured 2026-04-24)

Captured verbatim in `notes/impl-plan-commands-skills-migration-2026-04-24.md` §SME Sign-Off:
- D1 (effort metadata): REMOVE from 5 skills — done (UXL-039 fdfea25)
- D2 (orphan promotions): all orphans → new skills EXCEPT `init-worktree` (defer; CC built-in `--worktree` covers)
- D3 (hybrid strategy): expand `scaffolding-projects` to merge hybrids + prefer `--mode` extensions for domain-grouping
- D4 (F011 coupling): Option A — delegation pattern (executing-tasks → planning-implementation for non-trivial)
- D5 (naming): single-word preferred; verb+action as fallback (e.g., `techdebt` stays; `executing-tasks` → `execute`)
- D6 (command-trigger preservation): archive commands after empirical UX-equivalence validation
- D7 (plugin-prefix for skills): skip — CC-controlled, not CAB-configurable per docs check
- D8 (timing): proceed at measured pace per dual-POV principle (no deprecation deadline)

---

## Pre-2026-04-22 Queued Work (unchanged, still gated)

- **Phase D — HydroCast ↔ CAB State-Management Comparison** (HARD-BLOCKED on HydroCast PR #8 merge: https://github.com/daneyon/Flood-Forecasting/pull/8). Read-only comparison; multi-agent fan-out. Preserved for post-this-cycle resumption.

---

## Reference Artifacts

- **Mapping audit**: `notes/commands-skills-mapping-2026-04-24.md` (243 lines; all 15 commands categorized)
- **UXL-002 parent plan**: `notes/impl-plan-commands-skills-migration-2026-04-24.md` (265 lines; F001-F012 + 7 ADRs + SME sign-off block)
- **Wave plan** (sequencing): `notes/ux-log-wave-plan-2026-04-22.md` (11 waves; Wave 2 VOID, Wave 3 Phase 3a complete)
- **Pass-1 tracker**: `notes/ux-log-001-2026-04-22-pass-1.csv` (40 rows; 16 resolved / 20 triaged / 2 deferred / 2 wontfix)
- **Auto-memory (cross-session)**: `memory/feedback_dual_pov_check.md` — dual-POV check before building; governing principle for Phase 3b+ execution

<!-- T1:BOUNDARY — `current-task.md` is entirely T1 by design (<100 line hard target enforced by hooks/scripts/enforce-current-task-budget.sh). Whole file is the cold-start anchor. -->
