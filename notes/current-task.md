# Current Task: Wave 3 Phase 3b — Commands→Skills Migration (Renames + Wrapper Trims)

**Status**: PLAN authored 2026-04-24 (Session 37). Awaiting REVIEW → EXECUTE.
**Branch**: `master`
**Parent plan**: [notes/impl-plan-commands-skills-migration-2026-04-24.md](impl-plan-commands-skills-migration-2026-04-24.md)
**Mapping artifact**: [notes/commands-skills-mapping-2026-04-24.md](commands-skills-mapping-2026-04-24.md)
**Governing principle**: `memory/feedback_dual_pov_check.md` (dual-POV before building)

---

## Objective

Execute Phase 3b: rename 8 skills per F012/D5, update all cross-references atomically, trim 6 wrapper commands to pure-shim form, verify via `/validate` + grep sweep.

## Acceptance Criteria

- [ ] 8 skill folders renamed (old dirs removed) with frontmatter `name:` updated
- [ ] `grep -r "executing-tasks\|auditing-workspace\|creating-components\|validating-structure\|scaffolding-projects\|planning-implementation\|architecture-analyzer\|session-close"` returns zero functional hits (archival mentions in `notes/` historical records allowed)
- [ ] 6 wrapper commands (add-agent/add-command/add-skill/execute-task/new-project/validate) reference renamed skills
- [ ] Wrapper commands contain no substantive logic duplicated in skills (content F010 duplication eliminated)
- [ ] `/validate` passes structural validation
- [ ] Verifier agent confirms all acceptance criteria
- [ ] `notes/progress.md` + `notes/TODO.md` + `notes/current-task.md` updated

## Subtasks

| # | Subtask | Files | Commit |
|---|---|---|---|
| 3b.1 | Rename 8 skill folders + update `name:` in each SKILL.md + sweep all cross-refs atomically | 8 skill dirs + ~45 files (CLAUDE.md, knowledge/**, agents/**, commands/**, notes/**, other skills) | `refactor(skills): rename 8 skills to single-word/verb+object per F012/D5 [UXL-002 Phase 3b.1]` |
| 3b.2 | Trim wrapper commands — remove F010 duplicated content, retain only trigger-UX framing | 6 command files | `refactor(commands): trim wrappers to pure-shim form [UXL-002 Phase 3b.2]` |
| 3b.3 | Verify — `/validate`, grep sweep, verifier agent | — | (no commit; VERIFY gate) |
| 3b.4 | State updates — progress.md + TODO.md + current-task.md | 3 files | `chore(session-37): state update — Phase 3b landed [UXL-002]` |

## Skill Rename Table (D5-revised 2026-04-24: two-word default)

**D5 amendment rationale** (Session 37 in-flight refinement): single-word names (`plan`, `audit`, `execute`, `validate`) are too generic in multi-plugin namespace. User UX observation: skill-picker type-as-you-go narrows equally fast with two-word names and they're self-documenting. Two-word default; drop `-ing` gerund; verb+object order.

| Old | New | Rationale |
|---|---|---|
| `architecture-analyzer` | `analyze-architecture` | drop noun-suffix; verb+object |
| `auditing-workspace` | `audit-workspace` | drop `-ing` gerund |
| `creating-components` | `create-components` | drop `-ing` gerund |
| `executing-tasks` | `execute-task` | drop `-ing`; singular (matches command) |
| `planning-implementation` | `plan-implementation` | drop `-ing` |
| `scaffolding-projects` | `scaffold-project` | drop `-ing`; singular |
| `session-close` | `close-session` | re-order to verb+object |
| `validating-structure` | `validate-structure` | drop `-ing` |
| `pre-push-state-review` | (keep) | compound concept |
| `quick-scaffold` | (keep) | merges into `scaffold-project --quick` in Phase 3c |

## Verification Method

1. `grep -r '<old-name>'` per skill — zero functional hits in active code paths
2. `/validate` structural validation passes
3. Verifier agent (subagent) independently checks acceptance criteria
4. Spot-check: invoke one renamed skill via `Skill` tool to confirm registration

## Boundaries

**In scope**: 8 skill renames, 6 wrapper trims, cross-ref sweep, state updates
**Out of scope**: orphan promotions (Phase 3c), hybrid merges into unified `scaffold` (Phase 3c), F011 Option A delegation wiring (Phase 3c), wrapper archive (Phase 3d), UXL-001 (Wave 3 Part 2)

## Failure Modes & Mitigations

| Risk | Mitigation |
|---|---|
| Missed cross-ref → broken invocation | Atomic commit per rename batch; post-commit grep verification |
| `validate` or `audit` skill name collides with `/cab:validate` command UX | Names already resolved via SME D5; separate namespaces (skill vs command); flag only if real friction observed |
| CC discovery drift after rename (plugin cache stale) | Restart session post-rename if skills don't appear in Skill tool listing |
| Historical references in `notes/` flagged by grep but valid | Accept historical mentions (commit messages, session logs); only touch active code-path references |

## Reversibility

Each subtask = one commit. Revert via `git revert <commit>` per subtask. 3b.1 is the heaviest commit (~50 files); revert cleanly restores old skill names + cross-refs.

<!-- T1:BOUNDARY — current-task.md is entirely T1, <100 line cold-start anchor. -->
