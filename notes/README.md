# `notes/` Navigation Map

> Where to look for current state. Updated: 2026-04-24 (Session 37 close — Wave 3 Phase 3c LANDED, Phase 3d gated).

## "Where do I find...?" — quick lookup

| I want to know... | Read this file (anchor if applicable) |
|---|---|
| **What I'm doing right now** | `current-task.md` |
| **Phase 3d details** | `current-task.md` § *Phase 3d — Wrapper Command Archival* |
| What we did last session | `progress.md` (top entry — most recent at top) |
| Live priority list | `TODO.md` (top section is current) |
| Why D5-revised naming | `impl-plan-commands-skills-migration-2026-04-24.md` § *D5 Amendment* |
| UXL-002 plan + acceptance criteria | `impl-plan-commands-skills-migration-2026-04-24.md` |
| Command↔skill mapping audit | `commands-skills-mapping-2026-04-24.md` |
| All UX-log tracker rows | `ux-log-001-2026-04-22-pass-1.csv` |
| Wave sequencing (which wave is next) | `ux-log-wave-plan-2026-04-22.md` |
| Cross-session lessons (LL-01..LL-29+) | `lessons-learned.md` |
| Bootstrap token measurements over time | `bootstrap-cost-log.md` |
| Global extension registry | `global-extensions-map.md` |
| LL-25 propagation status (RAS-exec, HydroCast) | `ll-25-propagation-status-2026-04-22.md` |
| Resolved plans / historical artifacts | `_archive/` (gitignored) |

## Cold-start bootstrap (3-file cascade — read in order)

The CAB orchestrator bootstraps every fresh session via this exact sequence (~7,200 tokens total):

1. **`current-task.md`** — full file (≤100L hard cap). The L1 anchor for the active task. **Phase 3d details live here.**
2. **`progress.md`** — partial read (`limit=100`). T1 section only (most recent session); deeper history available on demand.
3. **`TODO.md`** — partial read (`limit=80`). Top priorities only.

`lessons-learned.md` is **on-demand** at decision-domain matches, not every cold-start (per LL-29).

## File categorization

### Bootstrap state (T1 cascade — always current)
- `current-task.md` · `progress.md` · `TODO.md`

### Active in-flight artifacts (UXL-002 migration cycle, Phase 3d gated)
- `impl-plan-commands-skills-migration-2026-04-24.md` (parent plan)
- `commands-skills-mapping-2026-04-24.md` (Phase 1 mapping audit)
- `ux-log-001-2026-04-22-pass-1.csv` (active 40-row tracker)
- `ux-log-wave-plan-2026-04-22.md` (11-wave sequencing)

### Durable always-on references
- `lessons-learned.md` (cross-session learnings)
- `bootstrap-cost-log.md` (token measurement log)
- `global-extensions-map.md` (extension layer registry)
- `ux-log-guide.md` (tracker usage guide)
- `ux-log-template.csv` · `ux-log-examples.csv` (tracker templates)

### Status-tracking artifacts (semi-durable)
- `ll-25-propagation-status-2026-04-22.md` (RAS-exec + HydroCast LL-25 alignment)

### Resolved plans (kept at top level — useful context for current work, can be archived later)
- `impl-plan-bootstrap-efficiency-2026-04-11.md` (LANDED Sessions 28-32; LL-29 captures the durable lesson)
- `impl-plan-ux-log-tracker-2026-04-22.md` (LANDED Session 35; tracker infrastructure built)

### Archived to `_archive/` (gitignored; available locally only)
- `prior-session-5-findings-2026-04-10.md` (Session 5 findings; predates current architecture)
- `session-28-recovery-2026-04-11.md` (recovery method; content abstracted into LL-28 + `filesystem-patterns.md`)

## Cleanup conventions

- **`notes/_archive/`** is gitignored (per `filesystem-patterns.md` Git Tracking Policy + LL-25 escape hatch). Files moved there disappear from git tracking on next commit but remain in working tree + git history.
- **State curation > compression** — files in `notes/` should optimize for lossless semantic preservation across sessions, not minimum line count (LL-29).
- **Tense hygiene** — state files use past-tense framing referencing commit hashes; pre-push hook + `pre-push-state-review` skill catch draft markers (LL-26).
- **`[UXL-NNN]` commit suffix** — required for commits resolving tracker rows; post-commit hook updates `linked_commit` column.

## Pointers to authoritative sources

- Bootstrap protocol spec: `knowledge/operational-patterns/state-management/bootstrap-read-pattern.md`
- State-management policy: `knowledge/operational-patterns/state-management/filesystem-patterns.md`
- KB conventions: `.claude/rules/kb-conventions.md`
- Component standards: `.claude/rules/component-standards.md`
- Project CLAUDE.md (orchestrator system instruction): `../CLAUDE.md`
