# Commands ↔ Skills Mapping (CAB, 2026-04-24)

**Author**: orchestrator (CAB Phase 1 of UXL-002 plan)
**Source plan**: `notes/impl-plan-commands-skills-migration-2026-04-24.md`
**Purpose**: categorize each CAB command as **wrapper**, **orphan**, or **hybrid** + flag content-quality preservation + redundancy concerns + naming standardization candidates per F009-F012.

---

## Summary Table

| # | Command | Category | Wraps Skill | F009 Unique Content? | F010 Duplication? | F011 Note | F012 Naming Target | Deprecation Risk |
|---|---|---|---|---|---|---|---|---|
| 1 | `/cab:add-agent` | wrapper | `creating-components` | No (pure shim) | Minimal | — | already verb+object | low |
| 2 | `/cab:add-command` | wrapper | `creating-components` | No | Minimal | — | already verb+object | low |
| 3 | `/cab:add-skill` | wrapper | `creating-components` | No | Minimal | — | already verb+object | low |
| 4 | `/cab:commit-push-pr` | **orphan** | — | Full workflow (multi-step git flow) | N/A | — | compound; keep or `commit-and-publish` | med (logic loss if sunset) |
| 5 | `/cab:context-sync` | **orphan** | — | Full workflow (git + gh + MCP) | N/A | — | `sync-context` (verb+object) | med |
| 6 | `/cab:execute-task` | wrapper | `executing-tasks` | **Minor** — "execution protocol" framing | Some overlap with skill body | **see §F011 analysis** | `execute-task` (skill renames to match) | low |
| 7 | `/cab:init-plugin` | **hybrid** | partial overlap w/ `scaffolding-projects` | Yes — template orchestration + git init + remote setup | Medium with `new-project` and `scaffolding-projects` | — | already verb+object | med |
| 8 | `/cab:init-worktree` | **orphan** | — | Git-specific worktree logic | N/A | — | already verb+object | low (CC built-in `--worktree` covers single case) |
| 9 | `/cab:integrate-existing` | **hybrid** | `project-integrator` agent + discovery logic | Yes — Phase 1 automated discovery is command-side | Partial with `scaffolding-projects` | — | compound; consider `integrate-codebase` | med |
| 10 | `/cab:kb-index` | **orphan** | — | INDEX generation logic | N/A | — | `index-kb` | med |
| 11 | `/cab:new-global` | **orphan** | — | Global config scaffold logic | Partial with `quick-scaffold` for global target | — | `scaffold-global` or consolidate w/ `quick-scaffold` | med |
| 12 | `/cab:new-project` | wrapper | `scaffolding-projects` | No | Minimal | — | `scaffold-project` (skill renames) | low |
| 13 | `/cab:sync-check` | **orphan** | — | Declarative detection logic; UXL-011 just extended | N/A | — | `check-sync` | med |
| 14 | `/cab:techdebt` | **orphan** | — | Full techdebt scan workflow | N/A | — | `scan-techdebt` | med |
| 15 | `/cab:validate` | wrapper (conditional) | `validating-structure` OR `auditing-workspace` (flag-based) | Minor (flag routing) | Minor | — | already verb+object | low |

**Categorization stats**:
- **WRAPPER**: 6 (add-agent, add-command, add-skill, execute-task, new-project, validate)
- **HYBRID**: 2 (init-plugin, integrate-existing)
- **ORPHAN**: 7 (commit-push-pr, context-sync, init-worktree, kb-index, new-global, sync-check, techdebt)
- **Total**: 15 ✓

**Migration estimate** (at current scope, subject to Phase 2 SME decisions):
- **Low-hanging**: 6 wrapper commands → reduce to pure-shim (trivial; ~30 min each)
- **Medium**: 7 orphan commands → promote to new skills where logic is reusable (~1-2 hrs each); some may stay as commands if truly command-specific
- **Complex**: 2 hybrid commands → split carefully to avoid content loss (~2-3 hrs each)

---

## Special Analysis: F011 — executing-tasks ↔ planning-implementation Dynamic

The current split is structurally ambiguous. Evidence from reading both SKILL.md files:

**`planning-implementation` skill** (effort: high):
- Purpose: "Generate SOW, implementation plans, acceptance criteria, and phased backlogs"
- Scope: full-depth plan authoring (SOW template, implementation plan template, phased decomposition)
- Workflow diagram: `Idea → SOW (approved?) → Implementation Plan → EXECUTE (handoff to executing-tasks)`

**`executing-tasks` skill** (effort: high):
- Purpose: "Enforce PLAN → REVIEW → EXECUTE → VERIFY → COMMIT protocol"
- Scope: 5-phase task execution; **Phase 1 is "PLAN"** — state objective, define acceptance criteria, decompose, identify verification method, write plan
- Workflow: self-contained plan→execute loop

**Overlap + tension**:
- `executing-tasks` Phase 1 authors a plan (lightweight, inline)
- `planning-implementation` authors a plan (heavyweight, artifact-producing)
- **Both skills claim "the PLAN phase"** with different semantics
- Current `/cab:execute-task` command comments reference `planning-implementation` skill — suggesting at some point we DID want the delegation, but the skills' bodies haven't been updated to reflect it

**Three Phase 3 consolidation options for SME review**:

- **Option A (delegation)**: `executing-tasks` Phase 1 explicitly delegates to `planning-implementation` for non-trivial work. Quick inline plans stay in executing-tasks. Boundary: plan complexity / artifact persistence.
- **Option B (consolidation)**: merge into single skill `execute-task` with modes (`--quick` inline plan vs `--full` SOW+plan artifact). Reduces two effort:high skills to one.
- **Option C (status quo, clarified)**: keep separate but explicitly document the boundary in both SKILL.md headers. No code change; clarity improvement only.

**My recommendation**: **Option A** — delegation pattern. Reasons:
1. Respects dual-POV: `executing-tasks` owns the EXECUTE workflow; `planning-implementation` owns the PLAN authoring. Single responsibility.
2. Aligns with existing `/cab:execute-task` hint that delegation was once intended
3. Doesn't collapse two distinct high-effort skills into one (preserves specialization)
4. Phase 2 SME decides boundary — e.g., "plans over 100 lines delegate to planning-implementation"

**Not my call** — this is F011 flagged for your Phase 2 SME decision.

---

## Per-Command Detail (expanded where analysis warrants)

### 1-3. `/cab:add-agent`, `/cab:add-command`, `/cab:add-skill` — wrapper trio

All three are thin shims over `creating-components` skill. Command body is ~30-50 lines containing:
- Argument parsing pattern
- File location determination (plugin vs standalone)
- "Use the `creating-components` skill to..." delegation
- Example invocations

**F009 assessment**: no unique content worth preserving beyond trigger-UX framing. Phase 3: trim commands to pure-shim form.

### 4. `/cab:commit-push-pr` — orphan (full git workflow)

Command body is ~60 lines of git+gh workflow: stage → commit → push → gh pr create. No skill wraps this domain. **High F009 content** — the workflow logic IS the value.

**Phase 3 recommendation**: promote to new skill `publish-changes` (or `commit-push-pr` preserved name). Command becomes shim. Skill body carries the multi-step workflow.

**Deprecation risk**: medium — if CC sunsets commands before migration, logic is lost unless skill exists.

### 5. `/cab:context-sync` — orphan (session bootstrapping)

Command body ~50 lines: git log + gh PR/issue + MCP sources scan, produces session-bootstrap context dump. No skill wraps this.

**Phase 3**: promote to `sync-context` skill. Command becomes shim.

### 6. `/cab:execute-task` — wrapper (see F011 above)

Command references `executing-tasks` skill as of commit b0571cc (Session 34). Currently thin-wrapper pattern.

**F009 minor**: command has "execution protocol" framing that's redundant with skill body. Consolidate in Phase 3.

**F011 flag**: ties into the executing-tasks ↔ planning-implementation boundary question. Phase 2 SME decision required.

### 7. `/cab:init-plugin` — hybrid

Command body ~80 lines: directory mkdir + template copy + git init + optional GitHub remote. Partial overlap with `scaffolding-projects` skill (which does similar work interactively).

**F009 unique content**: git init + remote wiring is command-side only; `scaffolding-projects` skill focuses on structure.

**Phase 3 candidate**: either split init-plugin's git-setup logic into a new `init-git-remote` skill, OR expand `scaffolding-projects` to absorb git init responsibility. SME decision.

### 8. `/cab:init-worktree` — orphan (git worktree management)

Command body ~40 lines: worktree setup + shell alias generation. No skill.

**Phase 3 recommendation**: candidate for `init-worktrees` skill IF the logic is reusable across projects; otherwise keep as command. User may choose to defer (CC's built-in `claude --worktree` covers most single-worktree cases per the command's own note).

### 9. `/cab:integrate-existing` — hybrid

Command body is substantial (~100 lines): Phase 1 automated discovery (language/framework detection, git status, structure fingerprinting) + routes to `project-integrator` AGENT (not skill) for analysis.

**F009 unique content**: Phase 1 discovery logic is command-side. Phase 2+ delegates to agent.

**Phase 3**: extract Phase 1 discovery into new `detect-project-profile` skill (reusable by `/cab:new-project`, `/cab:validate` too); keep command as orchestrator of discovery→agent handoff.

### 10. `/cab:kb-index` — orphan (INDEX.md regeneration)

Command body ~30 lines: scan knowledge/ → extract frontmatter → generate INDEX.md files. No skill.

**Phase 3**: promote to `index-kb` skill. Reusable pattern for any KB directory structure.

### 11. `/cab:new-global` — orphan (global config scaffold)

Command body ~40 lines: template-driven global config setup. No skill. Partial overlap with `quick-scaffold` (which has a global-config target mode).

**Phase 3 option**: merge into `quick-scaffold` skill (add `--target=global` mode); command becomes shim. OR keep as separate `scaffold-global` skill.

### 12. `/cab:new-project` — wrapper

Explicit delegation to `scaffolding-projects` skill with interactive discovery wrapping. Thin pattern.

**F009 minor**: "Lifecycle Advisory" section references `knowledge/reference/INDEX.md` — worth preserving as a skill-body cross-reference if not already there.

### 13. `/cab:sync-check` — orphan (recently extended UXL-011)

Command body now ~125 lines after UXL-011 shadow-detection extension. No skill.

**Phase 3 candidate**: promote to `check-sync` skill. Given shadow-scan logic is substantial + reusable from `/validate --cab-audit` (UXL-013 integration), a shared skill is architecturally cleaner. Both command + audit would invoke the skill.

### 14. `/cab:techdebt` — orphan (techdebt scan)

Command body ~70 lines: multi-category scan (duplication, stale markers, dead code, consistency, dependency health). No skill.

**Phase 3**: promote to `scan-techdebt` skill. Reusable pattern for periodic audits.

### 15. `/cab:validate` — wrapper (conditional)

Routes to `validating-structure` OR `auditing-workspace` based on `--cab-audit` flag. Thin wrapper with flag logic.

**F009**: routing logic is command-side; minor.

**Phase 3**: retain conditional wrapper OR move flag routing into skill body (skill takes mode parameter). SME decision.

---

## F012 Naming Standardization — Proposed Skill Renames

> **D5 history**: originally proposed single-word names (Phase 2 SME sign-off 2026-04-24 AM). Amended Session 37 2026-04-24 PM to two-word default after user UX observation on skill-picker type-as-you-go narrowing. The table below is the FINAL rename target applied in Phase 3b.1. See `impl-plan-commands-skills-migration-2026-04-24.md` §D5 Amendment for rationale.

Apply verb+object concise convention during Phase 3 carry-over. Cross-references in CLAUDE.md, plugin.json, KB, and other skills/agents must be updated atomically with renames.

| Current skill | Proposed rename | Rationale |
|---|---|---|
| `architecture-analyzer` | `analyze-architecture` | noun-noun → verb+object |
| `auditing-workspace` | `audit-workspace` | drop `-ing` gerund |
| `creating-components` | `create-components` | drop `-ing` gerund |
| `executing-tasks` | `execute-task` (singular, match command) | drop `-ing`; singular |
| `planning-implementation` | `plan-implementation` | drop `-ing` (but see F011 — may restructure entirely) |
| `pre-push-state-review` | **keep** | compound concept name; not gerund |
| `quick-scaffold` | **keep** | adjective+noun; already concise |
| `scaffolding-projects` | `scaffold-project` | drop `-ing`; singular |
| `session-close` | `close-session` | re-order to verb+object |
| `validating-structure` | `validate-structure` | drop `-ing` gerund |

Proposed command renames (same principle; only if SME approves trigger-name changes):

| Current | Proposed | Rationale |
|---|---|---|
| `context-sync` | `sync-context` | verb+object |
| `kb-index` | `index-kb` | verb+object |
| `sync-check` | `check-sync` | verb+object |
| `techdebt` | `scan-techdebt` | add leading verb |
| `new-global` | `scaffold-global` | replace "new" with specific verb |
| `new-project` | `scaffold-project` | same principle |

**Default for commands**: TRIGGER-COMPAT PRESERVE per Q2 — do NOT rename command triggers unless explicitly approved. Only SKILL renames are default-apply in Phase 3.

---

## Plugin-Prefix Display Observation (from SME Q2)

User observation: CC now natively shows `(cab)` prefix on hover for plugin-provided **commands**. **Skills don't yet** display the plugin prefix.

**Scope**: out of UXL-002; flagged as potential new row UXL-039 if action needed (e.g., requesting CC to extend prefix display to skills, OR CAB-side convention workaround).

---

## Phase 2 SME Decision Surface

Items for your review / decision:

1. **Wrapper shim migrations** (6 commands) — default trim to pure shim; any to exempt?
2. **Orphan promotions** (7 commands) — which orphans promote to new skills vs stay as commands? Per-command below:
   - `commit-push-pr` → new skill? [recommend yes]
   - `context-sync` → new skill? [recommend yes]
   - `init-worktree` → new skill OR defer (CC built-in covers single case)?
   - `kb-index` → new skill? [recommend yes]
   - `new-global` → new skill OR merge into `quick-scaffold`?
   - `sync-check` → new skill (architecturally cleaner with UXL-013 audit coupling)?
   - `techdebt` → new skill? [recommend yes]
3. **Hybrid splits** (2 commands) — `init-plugin` + `integrate-existing` need split architecture decisions
4. **F011 executing-tasks ↔ planning-implementation** — Option A / B / C?
5. **F012 skill renames** — approve the proposed renames or revise?
6. **Command-trigger renames** — default PRESERVE (no changes) unless you explicitly approve per command
7. **Plugin-prefix display for skills** — log as new UXL-039 or skip?
8. **Timing** — execute Phase 3 migrations this wave or defer?

---

## Sources

- `.claude/rules/component-standards.md` — skill + agent frontmatter valid fields
- `knowledge/components/subagents.md` — subagent architecture reference
- `knowledge/overview/design-principles.md` DP2 — wrapping architecture
- `notes/impl-plan-commands-skills-migration-2026-04-24.md` — parent plan
- `notes/ux-log-001-2026-04-22-pass-1.csv` UXL-002 — verbatim user directive
- memory/feedback_dual_pov_check.md — governing principle during mapping analysis
