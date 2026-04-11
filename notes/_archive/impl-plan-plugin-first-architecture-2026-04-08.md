# Implementation Plan: Plugin-First Architecture Correction

**Created**: 2026-04-08 (Session 16)
**Scope**: Fix audit skill + un-nest CAB & RAS-exec + R2 audits + HydroCast read-only R2
**Trigger**: User identified that `distributable-plugin.md` schema and CAB's own structure contradicted CC's official plugin component conventions. Investigation confirmed CC docs specify plugin components at root, not `.claude/`.
**Lesson**: LL-21 candidate — Session 6 `.claude/` migration was incorrect for plugin projects; custom `plugin.json` paths masked the issue but deviated from CC standard.

---

## Problem Statement

CC distinguishes two project types with different component locations:

| Type | Components Location | Manifest | Invocation |
|------|-------------------|----------|------------|
| **Standalone** | `.claude/skills/`, `.claude/agents/`, `.claude/commands/` | None | `/skill-name` |
| **Plugin** | Root: `skills/`, `agents/`, `commands/` | `.claude-plugin/plugin.json` | `/plugin:skill-name` |

Three CAB-audited projects (CAB, RAS-exec, HydroCast) are all plugin-wrapped but use `.claude/` nesting (standalone convention). The audit skill itself enforces standalone conventions on all projects indiscriminately.

**Impact**: 
- CAB works via custom `plugin.json` paths (non-standard workaround)
- RAS-exec would deliver zero components if distributed (no custom paths, no root dirs)
- Audit skill gives false positives (flagging correct plugin structure as wrong) and false negatives (not flagging `.claude/` nesting in plugins)

---

## Phase 1: Audit Skill R2 — Plugin-Architecture-Aware Criteria

**Objective**: Make the audit skill correctly evaluate both plugin and standalone projects.

### 1A: `auditing-workspace/SKILL.md` — Detection & Phase 1 Logic

**File**: `.claude/skills/auditing-workspace/SKILL.md` (will be `skills/` after Phase 2)

Changes:
- **Phase 0 (Context Discovery)**: Already detects plugin vs CC project. Add: set `project_type` variable (`plugin` | `standalone`) and carry through all phases.
- **Phase 1 (Structural Pre-Check)**: Replace the hard-coded check:
  - OLD: "CC components are under `.claude/` (not root-level `agents/`, `skills/`)"
  - NEW: Conditional:
    - If `plugin`: components at ROOT (`agents/`, `skills/`, `commands/`). `.claude/` components = ERROR (wrong convention)
    - If `standalone`: components under `.claude/`. Root-level components = ERROR
  - Add: If plugin, check `plugin.json` has NO stale custom paths pointing to `.claude/`
  - Add: If plugin, check root `settings.json` exists with `agent` key (WARN if missing)

### 1B: `agent-standards.md` — Architecture-Aware Criteria

**File**: `.claude/skills/auditing-workspace/references/standards/agent-standards.md`

Changes:
- Criterion 1: "Agent files are `.md` in `agents/` (plugin) or `.claude/agents/` (standalone)"
- Criterion 14 (plugin-restricted fields): Already correct
- Score 0 ABSENT: "agents outside expected location (`agents/` for plugin, `.claude/agents/` for standalone)"

### 1C: `settings-standards.md` — Plugin Settings Check

**File**: `.claude/skills/auditing-workspace/references/standards/settings-standards.md`

Changes:
- Criterion 1: Keep `.claude/settings.json` check (correct for project settings regardless of type)
- Add criterion 14: If plugin, root `settings.json` should exist with `agent` key (INFO for minimal, WARN for advanced)
- Add criterion 15: If plugin, root `settings.json` should NOT contain non-plugin fields (only `agent` is supported)

### 1D: `skill-standards.md` — Already Architecture-Neutral

**File**: `.claude/skills/auditing-workspace/references/standards/skill-standards.md`
- Criterion 1 uses `*/SKILL.md` glob (no hard-coded path). No change needed.
- Verify scoring guide is architecture-neutral. (It is.)

### 1E: `hooks-standards.md` — Plugin Hooks Location

**File**: `.claude/skills/auditing-workspace/references/standards/hooks-standards.md`
- Currently architecture-neutral. 
- Add: If plugin, hooks in `hooks/hooks.json`. If standalone, hooks in `.claude/settings.json` hooks section or project hooks config.

### 1F: `validating-structure/SKILL.md` — Plugin-Aware Validation

**File**: `.claude/skills/validating-structure/SKILL.md`

Changes:
- Step 1: Already identifies plugin vs global. Add detection for "plugin-wrapped project."
- Step 2, Directory Structure Check: 
  - OLD: "Component directories under .claude/ (per CC project schema)"
  - NEW: Conditional on project type:
    - Plugin: `commands/`, `agents/`, `skills/` at root; `hooks/hooks.json`; `.claude/settings.json` + `.claude/rules/` (project config stays in `.claude/`)
    - Standalone: `.claude/commands/`, `.claude/agents/`, `.claude/skills/`
- Common Issues table line 166: Update "Components inside .claude-plugin/" to also cover "Plugin components inside .claude/ instead of root"

### 1G: `audit-methodology.md` — Add Architecture Context

**File**: `.claude/skills/auditing-workspace/references/audit-methodology.md`
- Add section documenting the plugin vs standalone component location convention
- Reference CC official docs as source of truth

### Phase 1 Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| AC-1 | Phase 0 sets `project_type` and carries through | Read SKILL.md, confirm variable flow |
| AC-2 | Phase 1 structural check is conditional on project type | Read SKILL.md Phase 1 |
| AC-3 | agent-standards criterion 1 is architecture-aware | Read pack, confirm both paths |
| AC-4 | settings-standards has plugin root settings.json check | Read pack |
| AC-5 | validating-structure is plugin-aware | Read skill |
| AC-6 | No audit pack hard-codes `.claude/agents/` without conditional | Grep across all packs |

---

## Phase 2: CAB Structural Migration

**Objective**: Move CAB's own components from `.claude/` to root-level plugin convention.

### 2A: Git Move Operations

```bash
git mv .claude/agents/ agents/
git mv .claude/skills/ skills/
git mv .claude/commands/ commands/
```

**Stays in `.claude/`**: `settings.json`, `settings.local.json` (project config, not distributed)

### 2B: Plugin Manifest Update

**File**: `.claude-plugin/plugin.json`

Remove custom component paths (let CC defaults work):
```json
// REMOVE these three lines:
"agents": ".claude/agents/",
"skills": ".claude/skills/",
"commands": ".claude/commands/"
```

Optionally add root `settings.json` with: `{ "agent": "orchestrator" }`

### 2C: CLAUDE.md Update

**File**: `CLAUDE.md`
- Update any references to `.claude/agents/`, `.claude/skills/`, `.claude/commands/`
- Update Extension Registry section if it references `.claude/` paths

### 2D: Cross-Reference Updates (30 files, ~93 references)

**CRITICAL (4 files)**:
1. `knowledge/schemas/distributable-plugin.md` — Rewrite plugin-first, clarify standalone as alternative
2. `knowledge/operational-patterns/sync-protocol.md` — All path references, bash scripts
3. `commands/sync-check.md` (post-move path) — Sync mapping table, diff/copy scripts
4. `templates/plugin/plugin.json.template` — Already correct (root paths), verify

**HIGH (9 files)**:
5. `skills/auditing-workspace/SKILL.md` — Phase 2 dimension paths, `--changed-only` mapping
6. `skills/auditing-workspace/references/standards/agent-standards.md` — Criterion paths (done in Phase 1)
7. `skills/creating-components/SKILL.md` — mkdir paths, creation instructions
8. `skills/validating-structure/SKILL.md` — Validation checklist (done in Phase 1)
9. `commands/integrate-existing.md` — mkdir scaffold, creation manifest
10. `commands/add-agent.md` — File creation path
11. `commands/add-skill.md` — Structure creation path
12. `commands/add-command.md` — File creation path
13. `commands/init-plugin.md` — Directory scaffold

**MEDIUM (8 files)**:
14. `knowledge/components/subagents.md` — Location table
15. `knowledge/components/agent-skills.md` — Location table
16. `knowledge/components/custom-commands.md` — Location comparison
17. `knowledge/schemas/cc-architecture-diagrams.md` — Diagram 5
18. `knowledge/schemas/global-user-config.md` — Schema documentation
19. `knowledge/overview/design-principles.md` — Historical context
20. `knowledge/operational-patterns/orchestration/framework.md` — Implementation notes
21. `knowledge/implementation/workflow.md` — Implementation checklist

**LOW (4 files)**:
22. `templates/plugin/CLAUDE.md.template` — Extension registry refs
23. `templates/global/CLAUDE.md.template` — Extension registry refs
24. `templates/hooks.json.template` — Location comment
25. `templates/skill.template/SKILL.md.template` — Variable docs

**Agent/Skill internal refs (3 files)**:
26. `agents/project-integrator.md` — Architectural analysis reference
27. `agents/orchestrator.md` — Check for .claude/ refs
28. `skills/scaffolding-projects/SKILL.md` — mkdir scaffold

### 2E: KB Documentation — Plugin-First Framing

**`distributable-plugin.md`**: Key rewrite areas:
- Lead with plugin structure as the DEFAULT/RECOMMENDED
- Reframe standalone as "lightweight alternative for personal experiments"
- Add CAB design philosophy note: "CAB scaffolds plugin by default"
- Keep both schemas documented (CC supports both) but make recommendation clear
- Update the "Key difference" paragraph

**`cc-architecture-diagrams.md`**: 
- Diagram 5 title: Remove "Schema 2" label confusion
- Update Capability Merge section to reflect plugin root paths

### Phase 2 Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| AC-7 | `agents/`, `skills/`, `commands/` exist at root | `ls` root |
| AC-8 | `.claude/agents/`, `.claude/skills/`, `.claude/commands/` do NOT exist | Verify removed |
| AC-9 | `plugin.json` has no custom component paths | Read file |
| AC-10 | Zero grep hits for `.claude/agents/` in non-notes files (excluding settings/rules refs) | Grep sweep |
| AC-11 | `distributable-plugin.md` leads with plugin-first | Read file |
| AC-12 | All templates scaffold root-level components | Grep templates/ |

---

## Phase 3: R2 Audit — CAB Self-Audit

**Objective**: Validate CAB's corrected structure using the fixed audit skill (AC-8 from original: ≥5 findings).

Run `auditing-workspace` skill against CAB itself. This serves dual purpose:
1. Validates CAB's plugin structure is correct
2. Tests the audit skill's plugin detection logic

### Phase 3 Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| AC-13 | Audit detects CAB as plugin project | Check Phase 0 output |
| AC-14 | Structural pre-check passes (root-level components) | Check Phase 1 output |
| AC-15 | ≥5 meaningful findings | Count findings |
| AC-16 | YAML + markdown artifacts produced | Check `notes/cab-audit-*` |

---

## Phase 4: RAS-exec Migration + R2 Audit

**Objective**: Un-nest RAS-exec components + validate with R2 audit.

### 4A: Structural Migration

```bash
cd RAS-exec/
git mv .claude/agents/ agents/
git mv .claude/skills/ skills/
git mv .claude/commands/ commands/
```

Keep: `.claude/settings.json`, `.claude/settings.local.json`, `.claude/rules/`

### 4B: Plugin Manifest Update

Update `plugin.json` — no custom paths needed (defaults work with root-level).
Optionally add root `settings.json` with `{ "agent": "ras-orchestrator" }`.

### 4C: Cross-Reference Updates

Scope TBD — need to grep RAS-exec for `.claude/agents/` etc. references.
Likely: CLAUDE.md, any agent/skill/command that references paths.

### 4D: R2 Audit

Run `auditing-workspace` against RAS-exec.

### Phase 4 Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| AC-17 | RAS-exec components at root | `ls` root |
| AC-18 | Plugin.json correct | Read file |
| AC-19 | R2 audit passes structural pre-check | Audit output |
| AC-20 | R2 audit score documented | YAML artifact |

---

## Phase 5: HydroCast R2 Audit (READ-ONLY)

**Objective**: Audit HydroCast with fixed skill. Report findings only — no remediation (user is active in repo).

### Phase 5 Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| AC-21 | Audit detects HydroCast as plugin | Phase 0 output |
| AC-22 | Findings report includes un-nesting recommendation | Check findings |
| AC-23 | YAML + markdown artifacts produced | Check files |
| AC-24 | Zero writes to HydroCast repo (read-only) | Verify no git changes |

---

## Execution Estimates

| Phase | Files Changed | Complexity | Est. Effort |
|-------|--------------|------------|-------------|
| 1 (Audit fix) | 6-7 files | Medium (logic changes) | 1 focused pass |
| 2 (CAB migration) | 30+ files (3 git mv + 28 cross-ref updates) | High (breadth) | 1-2 passes |
| 3 (CAB R2) | 2 artifacts produced | Low (read-only) | 1 pass |
| 4 (RAS-exec) | TBD (likely 10-15 files) | Medium | 1 pass |
| 5 (HydroCast R2) | 2 artifacts produced | Low (read-only) | 1 pass |

**Session strategy**: Phases 1-2 likely consume one full session. Phases 3-5 in next session. KB consistency pass as separate follow-on.

---

## Deferred (Immediate Follow-On)

- **KB Consistency Pass**: Holistic review of all KB files for cross-cutting inconsistencies. Connected to LL-19 (programmatic knowledge graph architecture).
- **LL-21**: Document this lesson (plugin projects need root-level components; `.claude/` nesting is standalone-only).
- **HydroCast remediation**: Un-nest components after user clears the repo.

---

## Risk Register

| Risk | Mitigation |
|------|-----------|
| Moving skills breaks CAB plugin for current users | Plugin cache means users have stale copy; update is explicit. Test locally with `--plugin-dir` before committing. |
| Audit skill edit changes break existing audit artifacts | Prior audits are snapshots. R2 explicitly re-baselines. |
| RAS-exec has cross-refs we haven't mapped | Grep sweep before moving. |
| Session context limit during Phase 2 (30 file edits) | Batch by priority tier. Commit after each batch. Transfer state via progress.md. |
