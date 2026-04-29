# Current Task: Wave 8 Phase 2 (REFRAMED) — KB Standardization + Lightweight KG + Vision-Anchored

**Status**: Session 39 reframe ACTIVE. Wave 8 plan officially switched from "graph over existing KB" → **"skills-as-modular-software with KG as systematization map"** per user direction 2026-04-28. End-vision artifact + KB card update DONE this session. Next: scenario-analyst stress-test → `/cab:plan-implementation` formal plan.
**Last active**: 2026-04-28 (Session 39 in progress)
**Branch**: `master` (Session 38 closed cleanly; Session 39 commits pending)
**End-vision (load every Wave 8-11 bootstrap)**: [notes/end-vision-cab-2026-04-28.md](end-vision-cab-2026-04-28.md)
**Original plan (to be archived)**: [notes/impl-plan-kb-to-kg-2026-04-24.md](impl-plan-kb-to-kg-2026-04-24.md) — superseded by formal plan from `/cab:plan-implementation`

---

## Session 39 Reframe Summary

User brain-dump surfaced the load-bearing reframing: "skill = software = modularized codebase into specific domain-specialized skillsets." After feasibility check + corrected metaphor (skill ≠ Python `src/` module; **skill = UNIX coreutil + man page = autonomous NL-invocable capability**), user confirmed switch.

**Decisions locked (D1-D6)**:
- D1: end-vision at `notes/end-vision-cab-2026-04-28.md` (separate artifact)
- D2: switch to "skills-as-modular-software with KG as systematization map"
- D3: 5-axis audit framework (existence / actionability / skill-pack home / temporal neutrality / end-vision alignment); KEEP/MERGE/REPACK/REWRITE/DELETE/GAP
- D4: JSON KG substrate MVP (`knowledge/_graph/index.json`); SQLite revisit if KB > 100 files
- D5: `knowledge/reference/llm-interaction-patterns.md` card + thin cross-refs from rules
- D6: invoke `strategy-pathfinder:scenario-analyst` BEFORE `/cab:plan-implementation`

**Graphiti**: pattern-steal (bi-temporal, episode-as-provenance, hybrid retrieval, ontology, incremental ingestion); NOT adopt-as-is (over-build at 44-file scale).

---

## Reframed Phasing (CONSOLIDATED post scenario-analyst stress-test)

| Phase | Status |
|---|---|
| 2A — Vision Anchoring | DONE (this session) |
| 2B' — Architectural Tier + Interaction Patterns Card + KB Authoring Rule | PENDING |
| 2C — Component Tier Audit | PENDING |
| 2D' — Operational + Tail Audit | PENDING |
| 2F — KG Schema Design (Schwerpunkt; 1.5 sessions; hand-author stress gate before 2G) | PENDING |
| 2G — Extractor + Indexer | PENDING |
| **HITL gate** — viz scope decision (Mermaid-only / Mermaid + HTML stub / full HTML) | PENDING |
| 2I — Visualization (scope per HITL) | PENDING |
| (deferred) — Notes ↔ KB linking implementation → Wave 9 | DEFERRED |

Total ~7 sessions. Ships when 2G + 2I render a coherent graph (sessions are estimate, not contract).

---

## Next Steps (this session)

1. ✅ End-vision artifact + arch-philosophy KB card — DONE
2. ⏳ Strategy-pathfinder:scenario-analyst stress-test (OODA + First Principles) of phase sequencing
3. ⏳ `/cab:plan-implementation` — formal multi-phase plan with acceptance criteria + KPIs
4. ⏳ Archive `impl-plan-kb-to-kg-2026-04-24.md` → `_archive/`; replace with formal plan
5. ⏳ Session 39 commit + close

---

## Pending User-Side Actions (carried forward from Session 38)

- Apply settings.json diff (9-line allow + 2-line allowedTools removal + `additionalDirectories` fix + `RUST_LOG` removal — confirmed approved)
- Defer decision: `CLAUDE_CODE_DISABLE_TELEMETRY` (CC native OpenTelemetry as DP8 wrap candidate)
- Hooks: KEEP both (`bash-security-gate.sh` + `ruff format` PostToolUse) — defense-in-depth complementary

---

## Reference

- End-vision: `notes/end-vision-cab-2026-04-28.md`
- Wave plan: `notes/ux-log-wave-plan-2026-04-22.md` Wave 8
- KB conventions: `.claude/rules/kb-conventions.md`
- Component standards: `.claude/rules/component-standards.md`
- Phase D HydroCast: still PR #8 blocked (parallel track)

<!-- T1:BOUNDARY — current-task.md is entirely T1 (<100L hard cap). -->
