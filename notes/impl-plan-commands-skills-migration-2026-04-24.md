# Implementation Plan: Commands → Skills Migration Audit (UXL-002)

**Date**: 2026-04-24
**Owner**: orchestrator (CAB)
**Source row**: UXL-002 — Wave 3 Part 1 of `notes/ux-log-wave-plan-2026-04-22.md`
**Effort**: M (single plan, 3 phases; Phase 2 is SME decision gate)
**Plan scope**: CAB repo only; no cross-project work
**Reference**: `notes/ux-log-001-2026-04-22-pass-1.csv` UXL-002 user_comment (verbatim user directive)

---

## 0. Statement of Work (Embedded)

### 0.1 Problem

Per user's UXL-002 brain-dump (2026-04-22 verbatim):

> per latest official CC dev docs, commands will be gradually be sunset and skills to be used/trigerred instead. luckily, our CAB hirearchical wrapping design philosophy, we already were pretty much effectively leveraging the commands to be essentially equivalent to the domain specialized skill extensions but just serving as the easy trigger mechanism by both CC agents and humans, via the dash function for any consistently repeated operations, so let's make sure we archive and no longer further optimize the commands and properly migrate to skills, if there isn't already the main pertaining skill(s) that was composing exist. we need to be strategic and careful here as I'm currently used to triggerring the skill-wrapped commands, not the skills themselves. let's start with a clear mapping of which existing skills are wrapped into commands and which aren't/disconnected, etc.

Two distinct failure modes this prevents:
- **Latent deprecation exposure**: CC-announced sunsetting of commands means any purely command-based functionality will silently degrade at some future CC release.
- **User-habit disruption risk**: user's trigger muscle memory is on commands (`/cab:execute-task`, not `cab:executing-tasks`). Abrupt migration breaks that workflow.

### 0.2 Proposed Solution

**Three-phase approach with SME gate between Phase 1 and Phase 3**:

- **Phase 1 — Mapping audit** (analytical, produces artifact): enumerate every command in `commands/` (CAB-provided, 15 files) and every skill in `skills/` (10 subdirs). For each command, determine one of three categorizations:
  - (a) **Thin wrapper** — command delegates to an existing skill (command body ≈ "invoke skill X with these args")
  - (b) **Orphan command** — command has no corresponding skill; its logic lives entirely in the command file
  - (c) **Hybrid** — command has skill-adjacent logic but isn't a pure delegation
- **Phase 2 — SME decision gate**: user reviews the mapping artifact, decides migration sequencing (what migrates, in what order, with what user-trigger compatibility strategy). May decide to delay some migrations indefinitely if CC's deprecation timeline allows.
- **Phase 3 — Execute migrations** (bounded scope per Phase 2 decisions): for each command marked for migration, either promote its orphan logic into a new skill OR update the wrapping to match skill-invocation pattern. Preserve user trigger continuity via compat shims where desired.

### 0.3 Challenges & Mitigations

| Challenge | Mitigation |
|---|---|
| User's trigger muscle memory is on commands, not skills | Phase 2 gate allows user to decide compat strategy (e.g., keep commands as thin shims pointing at skills; migrate over time) |
| CC's exact deprecation timeline is unknown | Plan targets ACTIONABLE now (Phase 1 mapping is free of deprecation risk); defers committing to migration until SME sequences |
| Migration might break Claude's auto-delegation behavior | Phase 3 preserves command names where trigger compat required; only the UNDERLYING implementation moves |
| Some commands are cross-project (e.g., `/cab:init-plugin` scaffolds external projects) | Phase 1 mapping categorizes scope; cross-project commands may need special migration paths |

### 0.4 Timeline

- Phase 1 mapping: ~30-45 min in this session
- Phase 2 SME gate: async (user review; next session)
- Phase 3 migrations: per-wave-level effort depending on SME scope decision — could be 1 session (thin-wrapper consolidation) to 3+ sessions (full orphan → skill promotions)

### 0.5 KPIs

| Category | Metric | Target |
|---|---|---|
| Coverage | All 15 commands categorized | 100% |
| Clarity | Each row names the skill it wraps or lacks | 100% |
| Actionability | Phase 3 scope is bounded by explicit SME decisions | yes |
| Trigger continuity (Phase 3) | No user-facing command name loss without explicit SME approval | 100% |
| Audit artifact durability | Mapping artifact is re-usable for future CC deprecation cycles | yes |

---

## 1. Project Overview

### 1.1 Scope Boundaries

**In scope**:
- Phase 1: mapping exercise, produces `notes/commands-skills-mapping-2026-04-24.md` artifact
- Phase 2: SME decision gate — user reviews mapping, scopes Phase 3
- Phase 3: bounded migration execution per SME decision; may include:
  - Promoting orphan command logic into new skills
  - Reducing thin-wrapper commands to pure skill-invocation shims
  - Preserving or archiving commands per trigger-continuity decision
- CSV state-machine update for UXL-002 on completion

**Out of scope**:
- UXL-001 default setup protocol (Wave 3 Part 2 — separate plan, executed after UXL-002 mapping informs its scope)
- Cross-project command migrations (RAS-exec, HydroCast have their own commands; out-of-CAB-scope)
- Building new skills not implied by existing commands (scope creep)
- Changes to CC's own command/skill handling (we can't; this is CC-native behavior)

### 1.2 Assumptions

- CC runtime still supports both commands AND skills in the current release (commands work; migration is proactive not reactive)
- Thin-wrapper commands can be replaced by skill invocation with equivalent user experience
- Skill auto-delegation will cover most former-command use cases; manual skill invocation covers the rest

### 1.3 Constraints

- Component standards (`.claude/rules/component-standards.md`): skill frontmatter must be ≤250 char description + `allowed-tools:` + `effort:`
- kb-conventions: if migration produces new KB cards, they must have frontmatter + source + ≤300 lines
- User trigger continuity is a hard constraint on Phase 3 scope decisions

---

## 2. Requirements

### 2.1 Functional

| ID | Feature | Acceptance Criteria |
|---|---|---|
| F001 | Complete command inventory | All 15 commands in `commands/*.md` enumerated in mapping artifact |
| F002 | Each command categorized | Every command tagged `wrapper`, `orphan`, or `hybrid` with 1-line justification |
| F003 | Wrapper commands name their skill | If `wrapper`, the skill name is listed explicitly; cross-ref link verified |
| F004 | Orphan commands flagged for migration analysis | If `orphan`, note whether a NEW skill is warranted (logic is reusable) vs keep-as-command (command-only mechanics like args with no skill-level semantics) |
| F005 | Hybrid commands annotated | If `hybrid`, note the split — what's command-level vs what's skill-level |
| F006 | User-trigger continuity notes | Per command, note whether the `/cab:xxx` trigger name should survive migration (default: YES, preserve user muscle memory) |
| F007 | Deprecation risk annotation | Per command, note residual risk if CC sunsets commands before migration completes |
| F008 | Mapping artifact SME-reviewable | File at `notes/commands-skills-mapping-2026-04-24.md` with scannable table format + per-command detail sections where analysis warrants |
| **F009** | **Content-quality preservation check** | Per wrapper/hybrid command, explicitly flag whether the command body contains ANY context NOT present in the wrapped skill (e.g., "repeatable workflow" framing, invocation-context nuance, examples tailored to human-trigger use). Flagged content MUST be preserved in Phase 3 migration — either by merging into the skill's body or retaining in a compat-shim command. Default preservation behavior: merge-into-skill; command becomes pure-shim. |
| **F010** | **Redundancy / duplication catch** | Per wrapper/hybrid command, flag content that EXISTS IN BOTH command body AND skill body (duplication risk — skill is canonical source; command should defer). Phase 3 synthesizes to eliminate duplication WITHOUT losing any unique framing flagged under F009. |
| **F011** | **Special attention: executing-tasks ↔ planning-implementation coupling** | The dynamic relationship between these two skills (and their commands `/cab:execute-task` + `/cab:planning-implementation`) is explicitly analyzed: are they one workflow split into two, or distinct workflows? Does the split reflect the standard PLAN→REVIEW→EXECUTE→VERIFY→COMMIT protocol cleanly, or is the current split arbitrary/outdated? Flag for Phase 3 consolidation consideration. |
| **F012** | **Naming convention standardization** | Phase 3 scope includes a pass renaming skills (and preserved command names) to a single standard: **verb + object** format, concise imperative (not gerund). Examples: `executing-tasks` → `execute-tasks` (or `execute-task`, singular); `validating-structure` → `validate-structure`; `auditing-workspace` → `audit-workspace`; `creating-components` → `create-components`. Apply during carry-over; update all cross-references. Default rule: drop `-ing` gerund; use bare verb. |

### 2.2 Non-Functional

| Category | Requirement | Target |
|---|---|---|
| Readability | Mapping artifact is SME-scannable in <5 min | 15-row table + per-row expansion on demand |
| Reversibility | Phase 3 migrations are per-command reversible via `git revert <commit>` | 100% |
| Maintainability | Mapping artifact useful for future CC deprecation cycles | generic format |

---

## 3. System Architecture

### 3.1 Phase 1 Mapping Artifact Structure

Proposed `notes/commands-skills-mapping-2026-04-24.md` format:

```markdown
# Commands ↔ Skills Mapping (CAB, 2026-04-24)

## Summary Table

| Command | Category | Wraps Skill | Migrate? | Trigger-Compat | Deprecation Risk |
|---|---|---|---|---|---|
| /cab:execute-task | wrapper | executing-tasks | already | keep trigger | low |
| /cab:validate | hybrid | validating-structure + auditing-workspace | reduce wrapper | keep trigger | low |
| ... (15 rows) ... |

## Per-Command Analysis

### /cab:execute-task → skill `executing-tasks`
Category: thin wrapper
...

### /cab:kb-index → orphan
Category: orphan (logic lives entirely in command file)
Recommendation: promote to `skill/kb-indexing/` OR keep as command if logic is truly command-specific
...
```

### 3.2 Categorization Rules (for Phase 1 analyst)

A command is a **thin wrapper** if:
- Command body is <30 lines
- Command body primarily invokes a skill (e.g., "Use the X skill to Y")
- Command-specific logic is argument parsing + skill invocation

A command is **orphan** if:
- No skill with matching domain exists
- Command body contains substantive logic (instructions, workflows, decision trees)
- Logic is NOT referenceable from a skill

A command is **hybrid** if:
- Some logic wraps a skill; additional logic is command-native
- Migrating cleanly requires splitting the logic

### 3.3 Architecture Decision Records

| Decision | Options | Choice | Rationale |
|---|---|---|---|
| Artifact location | `notes/` vs `knowledge/` | `notes/` | Audit artifact; not canonical reference; may be superseded by future mapping. Per flat-notes policy + `commands-skills-mapping-YYYY-MM-DD.md` prefix |
| Mapping granularity | Summary table only vs summary + per-command detail | Both (summary scannable; detail on demand) | SME can decide scope from summary; details available when specific commands need attention |
| Phase 3 scope authority | Pre-declared in this plan vs. SME-scoped at Phase 2 gate | SME-scoped at Phase 2 | Honors UXL-002 user directive "strategic and careful" + user trigger continuity concern |
| Trigger compat default | Migrate trigger names vs preserve | Preserve (default) | User directive explicit about muscle-memory risk; CC's native plugin-prefix display e.g. "(cab)" already groups nicely; migration changes UNDERLYING implementation not trigger UX |
| Content-quality preservation default (F009) | Merge-into-skill vs retain-as-command-shim | Merge-into-skill | Skill is canonical source; commands become pure-shim for trigger UX. Exception: if content is TRULY command-specific (e.g., argument-hint framing that only makes sense at trigger time), retain in shim with explicit rationale |
| Naming standardization (F012) | Keep current mixed conventions vs verb+object consistent | verb + object consistent (drop `-ing`) | User directive 2026-04-24. Applies during carry-over migration pass. Reduces cognitive load of mixed conventions across 10 skills + preserved command names. Cross-references (KB links, plugin.json, CLAUDE.md mentions) updated atomically with rename |
| Plugin-prefix display for skills | Add `(cab)` prefix convention to skills vs wait for native CC coverage | Note in mapping artifact; defer to separate row if action needed | CC already prefixes commands natively; skills don't yet. Not blocking UXL-002 scope — flag in artifact as observation, create new row if action needed |

---

## 4. Implementation Phases

### Phase 1 — Mapping Audit (~30-45 min this session)

| Task | Deliverable | Acceptance |
|---|---|---|
| 1.1 | Read all 15 command files + 10 skill SKILL.md files | Summary in scratch memory |
| 1.2 | Categorize each command per §3.2 rules | Per-command verdict with justification |
| 1.3 | Author `notes/commands-skills-mapping-2026-04-24.md` | F001-F008 all pass |
| 1.4 | Commit Phase 1 artifact | `docs(audit): commands↔skills mapping [UXL-002 Phase 1]` |

**Gate**: artifact committed; user reviews in Phase 2.

### Phase 2 — SME Decision Gate (async, next session)

User reviews the mapping artifact and makes explicit decisions:
- Which commands to migrate in Phase 3 (could be: all / some / none-yet)
- Per-command trigger compat strategy (default: preserve)
- Migration priority order (quick wrappers first? orphans first? risk-driven?)
- Phase 3 timeline (this wave? next wave? deferred?)

**Gate**: user posts SME decisions as inline annotations on the mapping artifact OR a separate decision memo. Phase 3 scope is frozen based on those decisions.

### Phase 3 — Execute Migrations (scope-dependent)

| Task type | What it looks like |
|---|---|
| Thin-wrapper consolidation | Update command body to pure skill-invocation pattern; remove duplicated logic |
| Orphan promotion | Create new skill at `skills/<name>/SKILL.md` with the orphan command's logic; update command to wrapper |
| Hybrid split | Extract skill-level logic into new/existing skill; keep command-native logic in command; update command to invoke the skill |
| No-migrate (preserve) | Mark command as "not migrating" with rationale in mapping artifact |

Each migration ships as its own commit with `[UXL-002]` suffix.

**Gate**: CSV state-machine update for UXL-002 → resolved with linked_commit (may be a multi-commit range if Phase 3 has multiple migrations).

---

## 5. Testing Strategy

Phase 1: artifact review only — no code changes, no tests needed.

Phase 3 (per migration): manual verification that the migrated command still triggers as expected:
- Run the command in a test session
- Confirm skill invocation (if wrapper migration)
- Confirm behavior equivalence vs pre-migration

---

## 6. Deployment Plan

In-repo hook-less changes. Rollout is immediate on commit. Rollback via `git revert` per-commit.

---

## 7. Risk Register

| Risk | Prob | Impact | Mitigation |
|---|---|---|---|
| CC deprecates commands before Phase 3 completes | Low | Med | Phase 1 mapping artifact is the canonical reference; re-engage when deprecation timeline firms up |
| Migration introduces user-facing regression (trigger breaks) | Low | High | Phase 2 SME gate + trigger-compat preservation default + Phase 3 manual verification |
| Orphan command logic doesn't fit CC skill format cleanly | Med | Low | Phase 2 analyst notes the fit; SME decides whether to force or keep as command |
| Mapping artifact becomes stale as CAB evolves | Med | Low | Artifact dated + commits provide timeline; re-run mapping as part of future deprecation cycles |

---

## 8. Acceptance Criteria (plan-level)

- [ ] F001-F008 pass in Phase 1 artifact
- [ ] Phase 1 artifact committed with `[UXL-002 Phase 1]` marker
- [ ] Phase 2 SME review captures explicit decisions (artifact or memo)
- [ ] Phase 3 scope is bounded; each migration is a separate commit
- [ ] CSV UXL-002 row marked `resolved` on full plan completion (Phase 3 may be multi-session)
- [ ] User trigger continuity preserved unless explicitly approved otherwise

---

## SME Sign-Off Captured (2026-04-24)

User responses on original 5 questions:
- **Q1 (artifact format)**: "seems good for now; need to keep actively using/testing to truly validate further" → proceed with proposed format
- **Q2 (trigger-compat)**: PRESERVE confirmed. Additional refinements now baked into F009/F010/F011/F012 (content-quality preservation, redundancy catch, executing-tasks↔planning-implementation special attention, verb+object naming standardization). CC now natively shows `(cab)` prefix on hover for commands; skills don't yet — noted as observation, not blocking
- **Q3 (SME scope authority for Phase 3)**: confirmed
- **Q4 (Phase 1 this session)**: confirmed
- **Q5 (UXL-001 waits on UXL-002 Phase 2)**: confirmed

Plan now reflects these refinements as F009-F012 + 3 additional ADRs.

---

## Sign-Off

Plan SME-approved 2026-04-24. Phase 1 mapping audit runs this session; produces `notes/commands-skills-mapping-2026-04-24.md`; commits; pauses for Phase 2 async review.
