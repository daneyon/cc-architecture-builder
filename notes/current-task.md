# Current Task: State Management Git-Tracking Reform (LL-25)

**Phase**: EXECUTED ✅ — all 10 ACs pass. Ready for commit + session close.
**Started**: 2026-04-10 (Session 24)
**Branch**: `master` (CAB)
**Parent TODO**: State management git-tracking reform (user-approved Session 23, executed Session 24)
**Related LL**: LL-25 (new), reinforces LL-17, LL-12, LL-20
**Prior task**: Plugin-First Architecture Correction — HydroCast Phase 5 P1 KB remediation remains deferred

---

## Objective (Session 24)

Reform CAB's `notes/` git-tracking policy from "gitignored" to "tracked by default" with targeted exclusions. Propagate the policy through KB, templates, hooks, and a new pre-push review skill. Multi-archetype justification (solo/team/agentic/distributed) formalized as LL-25.

## Status: EXECUTED ✅

All 10 acceptance criteria PASS. Pending commit + session close.

### Next Session Priority Queue

1. **HydroCast Phase 5 P1** — KB frontmatter fixes (3 files) + knowledge/INDEX.md reference
2. **CAB LL-24 enhancement** — marketplace.json awareness in audit skill, validate command, KB, templates (9 checklist items — see TODO.md)
3. **CAB version bump v1.1.1** — after LL-24 enhancements complete
4. **RAS-exec / HydroCast LL-25 policy follow-through** — apply tracked-notes policy to external plugins (documentation update, not structural change; deferred from Session 24)
5. **Pre-push hook refinement (LL-25 follow-on)** — current regex produces false positive on descriptive "WIP" prose; tighten to require markers at line-start or as explicit labels (`WIP:`, `DRAFT:`, etc.)

## Prior Task: Plugin-First Architecture Correction

**Status**: Phase 4 FULLY RESOLVED ✅, Phase 5 P-MKT/P0/P0.5 DONE ✅, P1 remaining (HydroCast)
**Plan**: `notes/impl-plan-plugin-first-architecture-2026-04-08.md`

## Context

- PR #7 (HydroCast D1-2) merged and closed
- User identified `distributable-plugin.md` schema conflicted with CC official convention
- Investigation confirmed: plugin = root components, standalone = `.claude/` components
- All 3 projects (CAB, RAS-exec, HydroCast) are plugin-wrapped but use `.claude/` nesting
- CAB works via custom `plugin.json` paths (workaround); RAS-exec would fail if distributed (no custom paths)
- Audit skill Phase 1 enforces `.claude/` on all projects — wrong for plugins

## Phases

- [x] **Phase 1**: Audit skill R2 — plugin-architecture-aware criteria (7 files, 6/6 AC PASS)
- [x] **Phase 2**: CAB structural migration — un-nest to root + 23 cross-ref updates (51 files, 6/6 AC PASS)
- [x] **Phase 3**: R2 audit — CAB self-audit with fixed skill (4/4 AC PASS, DEVELOPING 48%, 24 findings)
- [x] **Phase 3R**: CAB R2 remediation — 5-tier fix, 20/20 AC PASS (Session 19, commit `7bb6d60`)
- [x] **Re-audit**: DEVELOPING 62% (13/21), +3 pts / +14pp from baseline, 0 ERROR remaining (Session 20)
- [x] **Phase 4**: RAS-exec migration + R2 audit — ALIGNED 81% (17/21), PR #2 (Session 20, commits `7da6752` + `1c55bf3`)
- [ ] **Phase 5**: HydroCast R2 audit + remediation (feat branch, HITL gate)
- [ ] **Follow-on**: KB consistency pass (connected to LL-19), LL-21 documentation

## Session Strategy

- Session 16: Plan + Phase 1 execution — DONE (6/6 AC PASS, commit d8c0456)
- Session 17: Phase 2 — CAB structural migration — DONE (6/6 AC PASS, commit 01cfa2e)
  - 2A: git mv .claude/{agents,skills,commands}/ to root ✅
  - 2B: plugin.json custom paths removed ✅
  - 2C: CLAUDE.md updated ✅
  - 2D: 23 files cross-ref updated across 5 priority tiers ✅
  - 2E: distributable-plugin.md plugin-first framing ✅
- Session 18: Phase 3 (CAB R2 self-audit) — DONE (DEVELOPING 48%, 24 findings, 2 artifacts)
- **Session 18+ (NEXT)**: Phase 3R — CAB R2 remediation (prioritized 5-tier checklist, see `notes/TODO.md`)
- Then: Phase 4 (RAS-exec migration + R2)
- Then: Phase 5 (HydroCast full audit + remediation on feat branch, HITL review gate)
- Follow-on: KB consistency pass

## Key Decisions (Session 16)

1. **Plugin-first is CAB's default philosophy** — plugin = distributable packager, like git repo
2. **Follow CC native conventions** — root-level components for plugins, despite `.claude/` aesthetic preference
3. **`.claude/` retains**: settings.json, settings.local.json, rules/ — project config, not distributed components
4. **Fix measuring instrument first** (audit skill), then use it (R2 audits)
5. **HydroCast strictly read-only** — user is actively working there

## Acceptance Criteria Summary

See full plan for detailed per-phase AC. High-level:
- AC-1–6: Audit skill is plugin-architecture-aware
- AC-7–12: CAB components at root, all cross-refs updated
- AC-13–16: CAB R2 passes with plugin detection
- AC-17–20: RAS-exec migrated and audited
- AC-21–24: HydroCast R2 read-only report produced

## Blast Radius (from investigation)

- **30 files** with `.claude/{agents,skills,commands}` references in CAB
- **4 CRITICAL**: plugin.json, sync-check.md, distributable-plugin.md, sync-protocol.md
- **9 HIGH**: audit/validation skills, add-* commands, integrate-existing, component KB docs
- **8 MEDIUM**: KB docs, templates, orchestration framework
- **4 LOW**: templates with minor refs
