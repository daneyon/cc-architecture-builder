# Current Task: Wave 3 Phase 3c.2 — Hybrid Merges into `scaffold-project --mode`

**Status**: Phases 3b, 3c.1, 3c.3 LANDED (commits `0a7bcd8`, `5301325`, `b251b09`, `7b23830`). Phase 3c.2 queued — needs architectural REVIEW gate.
**Last active**: 2026-04-24 (Session 37 cont.)
**Branch**: `master`
**Parent plan**: [notes/impl-plan-commands-skills-migration-2026-04-24.md](impl-plan-commands-skills-migration-2026-04-24.md)
**Mapping artifact**: [notes/commands-skills-mapping-2026-04-24.md](commands-skills-mapping-2026-04-24.md)

---

## Next Session Pickup

### Immediate scope: Wave 3 Phase 3c.2

**Phase 3c.2 deliverables** (execute next session, after architectural REVIEW):

Merge 4 hybrid commands + 1 standalone skill into a unified `scaffold-project` skill via `--mode` extensions (per D3):

| Source | Target |
|---|---|
| `commands/init-plugin.md` (~70L command body) | `scaffold-project --mode plugin` |
| `commands/integrate-existing.md` (~140L) | `scaffold-project --mode integrate` |
| `commands/new-global.md` (~50L) | `scaffold-project --mode global` |
| `skills/quick-scaffold/SKILL.md` (292L, mostly templates) | `scaffold-project --mode quick` |
| (existing scaffold-project default behavior) | `scaffold-project` (no mode flag) |

After merge:
- Original 4 commands become pure shims invoking `scaffold-project` with appropriate `--mode`
- `quick-scaffold` skill folder removed (absorbed)
- Skill count: 15 → 12

### Architectural REVIEW gate (next session, before EXECUTE)

**Decision needed: how to structure the multi-mode SKILL.md?**

- **Option A — Inline body**: all 4 mode bodies inside `scaffold-project/SKILL.md`. Risk: blows past 400 lines (over 300L kb-conventions soft cap; probably 500+ with quick-scaffold templates inline).
- **Option B — Assets-based progressive disclosure**: `scaffold-project/SKILL.md` becomes a slim router (~150L); each mode has body in `assets/mode-{plugin,integrate,global,quick}.md` referenced from the router. quick-scaffold templates become `assets/templates/*.md`. Likely outcome: skill body ~120L + 4 asset files.
- **Option C — Hybrid**: short modes (global, plugin) inline; long modes (quick with templates, integrate with discovery logic) in assets/.

**Recommendation (subject to your call)**: Option B. Cleanest separation, scales if more modes added later, respects readability invariant. Cost: more files (5 vs 1). Compatible with CC's progressive disclosure pattern (skills can reference asset files via Read tool just-in-time).

### Follow-on Phase 3d (after 3c.2 validates)

- Archive wrapper commands once empirical validation confirms `/cab:<command>` UX equivalence (per D6 conditional approval)
- Candidates for archive: 6 wrapper commands from 3b (`add-agent`, `add-command`, `add-skill`, `execute-task`, `new-project`, `validate`) + 5 orphan-promoted shims from 3c.1 + 4 hybrid-merged shims from 3c.2 = potentially 15 commands → 0 if full archive validated

### Wave 3 Part 2 (after Phase 3d)

- UXL-001 (default setup protocol project-schema-first) — plan authoring after Phase 3c+3d lands

---

## Session 37 (cont.) Closure Summary

- **Commits**: `7b23830` (5 orphan promotions + F011 wiring, 12 files, 777+/400-)
- **State refresh commit**: pending (this commit)
- **Verifier**: independent PASS on all 8 acceptance criteria
- **Skill count**: 10 → 15 (5 new orphan-promoted skills)
- **F011 Option A wiring**: complete and symmetrical between execute-task and plan-implementation

---

## Pre-2026-04-22 Queued Work (unchanged, still gated)

- **Phase D — HydroCast ↔ CAB State-Management Comparison** (HARD-BLOCKED on HydroCast PR #8 merge)

---

## Reference Artifacts

- **Mapping audit**: `notes/commands-skills-mapping-2026-04-24.md` (D5 amendment + F012 rename table updated)
- **UXL-002 parent plan**: `notes/impl-plan-commands-skills-migration-2026-04-24.md` (D5 amendment captured in §SME Sign-Off)
- **Wave plan** (sequencing): `notes/ux-log-wave-plan-2026-04-22.md` (Wave 3 Phase 3a/3b/3c.1/3c.3 complete; 3c.2 + 3d queued)
- **Auto-memory (cross-session)**: `memory/feedback_dual_pov_check.md` — dual-POV check before building; reaffirmed by D5 reversal in Session 37

<!-- T1:BOUNDARY — `current-task.md` is entirely T1 by design (<100 line hard target enforced by hooks/scripts/enforce-current-task-budget.sh). -->
