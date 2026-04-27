# Current Task: Wave 3 Phase 3d — Wrapper Command Archival (Empirical-Validation Gated)

**Status**: Phase 3b + 3c (full) LANDED. Phase 3d gated on empirical UX validation per D6.
**Last active**: 2026-04-24 (Session 37 cont.²)
**Branch**: `master`
**Parent plan**: [notes/impl-plan-commands-skills-migration-2026-04-24.md](impl-plan-commands-skills-migration-2026-04-24.md)
**Mapping artifact**: [notes/commands-skills-mapping-2026-04-24.md](commands-skills-mapping-2026-04-24.md)

---

## Next Session Pickup

### Phase 3d — Wrapper Archival (gated, not auto-execute)

**Trigger condition** (per D6): empirical confirmation that `/cab:<command>` UX is functionally equivalent to direct skill invocation across active testing. Until validated, all 15 shim commands stay in place to preserve user trigger habits.

**Validation method** (run a few sessions before deciding):
- Use commands as normal (`/cab:execute-task`, `/cab:new-project`, `/cab:init-plugin`, `/cab:context-sync`, etc.)
- Note any UX friction or behavior divergence vs invoking the underlying skill directly
- Note whether skill auto-discovery (Claude triggering skills from natural language) covers the muscle-memory cases

**If validated**:
- Archive all 15 shim commands to `_archive/`
- Update CLAUDE.md + KB to reference skill names directly
- Skill count remains 15; command surface drops to 0

**If friction observed**: keep shim commands; document the friction modes in `notes/lessons-learned.md` as a CAB pattern (user-trigger preservation > pure-skill UX).

### Wave 3 Part 2 (UXL-001) — gated on 3d outcome

Default setup protocol project-schema-first. Plan authoring conditioned on whether 3d archives commands or keeps them.

### UXL-038 territory — KB→skill migration

User end-vision: KB content packs into domain-specialized skill folders. The Phase 3c.2 `scaffold-project` router pattern + assets/ + Knowledge Anchors links is the **seed**. Future deep-dive can extend the pattern to other skills (e.g., `audit-workspace` already has `references/standards/` — same shape).

Not in immediate scope; revisit when UXL-038 surfaces in wave plan.

---

## Phase 3c Closure Summary (Session 37 full arc)

- **Commits**: `0a7bcd8` (3b.1) + `5301325` (3b.2) + `b251b09` (3b state) + `7b23830` (3c.1+3c.3 work) + `bcdae78` (3c.1+3c.3 state) + `6653a25` (3c.2 work) + this state-refresh
- **Pushed through `bcdae78`**; the 3c.2 work commit + this state refresh pending push
- **Verifier PASS**: 3 independent runs across 3b + 3c.1+3c.3 + 3c.2; all criteria met every time
- **Skill count**: 15 (5 added in 3c.1; quick-scaffold retained as alias in 3c.2)
- **D5 amendment**: two-word verb+object naming default (recorded in parent plan + mapping)
- **F011 wiring**: complete and symmetrical (execute-task ↔ plan-implementation)
- **Knowledge integration philosophy seeded**: scaffold-project router + mode assets reference KB cards via Knowledge Anchors sections, never duplicating

---

## Pre-2026-04-22 Queued Work (unchanged, still gated)

- **Phase D — HydroCast ↔ CAB State-Management Comparison** (HARD-BLOCKED on HydroCast PR #8 merge)

---

## Reference Artifacts

- **Mapping audit**: `notes/commands-skills-mapping-2026-04-24.md` (D5 amendment + F012 rename table updated)
- **UXL-002 parent plan**: `notes/impl-plan-commands-skills-migration-2026-04-24.md` (D5 amendment captured)
- **Wave plan**: `notes/ux-log-wave-plan-2026-04-22.md` (Wave 3 Phase 3a/3b/3c complete; 3d gated)
- **Auto-memory**: `memory/feedback_dual_pov_check.md` — dual-POV check; reaffirmed by D5 reversal
- **Push state**: 1 work commit + 1 state-refresh commit unpushed locally as of session close

<!-- T1:BOUNDARY — current-task.md is entirely T1 (<100L hard target). -->
