# Implementation Plan: `auditing-workspace` Skill

**Version**: 1.0
**Date**: 2026-04-07
**Related**: Multi-POV strategic assessment + workflow design (Session 10)
**Parent TODO**: Post-Audit → "Deep dive: standardized audit/freshness-check CC extensions (agentic protocol)"

---

## 0. Quick-Start Implementation Guide

### 0.1 Problem Statement
- **Current Gap**: No reusable tooling to audit an existing CC-integrated project against CAB v1.1.0 standards. The PA-01 global config audit was effective but entirely manual — non-reproducible across projects.
- **Solution**: New skill `auditing-workspace` that encodes the PA-01 methodology as a durable, reusable, agentic skill with modular standard packs and persistent artifact output.
- **Human-AI Model**: Claude performs judgment-based quality assessment; user reviews findings and approves remediation before any changes.
- **Impact**: Every project audit becomes systematic, repeatable, and trackable over time.

### 0.2 Technical Approach Summary
- **Architecture**: Separate skill (not a mode in `validating-structure`) with `agent: true` for multi-step investigation
- **Standard Packs**: 7 modular reference files in `references/standards/`, each linking to authoritative KB docs
- **Scoring**: Combined graduated (0-3) + classification (MISSING/STALE/ENHANCEMENT/CURRENT)
- **Output**: YAML (machine-readable) + Markdown (human-readable) artifacts to target project's `notes/`
- **Integration**: Feeds into `/execute-task` for remediation pipeline

### 0.3 Implementation Phases Overview
1. **Phase A**: Skill skeleton + methodology (SKILL.md + classification schema + audit methodology)
2. **Phase B**: Standard packs (7 modular references linking to KB)
3. **Phase C**: Validate command update + CAB CLAUDE.md update + orchestrator awareness
4. **Phase D**: Integration testing on CAB itself + global config

### 0.4 Validation Checkpoints
- [ ] Skill loads via `/memory` and description triggers on audit-related prompts
- [ ] Audit of CAB plugin produces meaningful scored findings across 7 dimensions
- [ ] YAML artifact is parseable and schema-compliant
- [ ] Delta report works against a second run
- [ ] Audit of global config (~/.claude/) reproduces ≥80% of PA-01's 9 ERROR findings

---

## 1. Architecture Decisions (Pre-Resolved)

| Decision | Choice | Rationale | Source |
|----------|--------|-----------|--------|
| Separate skill vs. mode | **Separate skill** | Scope tension (structural ≠ quality), clean permissions, `agent: true` appropriate | Strategic POV |
| Standard pack location | **`references/standards/`** in skill dir, linking to KB docs | Wrapper philosophy (LL-11), independently updatable, progressive disclosure | Strategic POV |
| Scoring system | **Combined**: graduated 0-3 per criterion + MISSING/STALE/ENHANCEMENT/CURRENT per finding | Score = how good, classification = what kind of fix | Synthesis |
| Utility scripts | **None for v1** — inline skill logic | Audit is judgment-based reading; scripts add indirection without value | Workflow POV |
| Artifact format | **YAML primary + Markdown summary** | Enables automated remediation pipeline + human review | Both POVs |
| Multi-pass | **Structural gate → 7-dimension standards → cross-cutting synthesis** | Prevents wasted evaluation on structurally broken projects | Both POVs |
| Context model | **`agent: true`** with `effort: high` | Multi-step investigation with substantial KB reference loading | Strategic POV |

---

## 2. File Inventory

### New Files to Create

```
.claude/skills/auditing-workspace/
  SKILL.md                              # Main skill — methodology + orchestrative instructions
  references/
    audit-methodology.md                # Formalized PA-01 workflow (discover → classify → plan)
    classification-schema.md            # Scoring rubric + classification definitions + examples
    standards/
      claudemd-standards.md             # → knowledge/components/memory-claudemd.md
      agent-standards.md                # → knowledge/components/subagents.md
      skill-standards.md                # → knowledge/components/agent-skills.md
      settings-standards.md             # → knowledge/schemas/global-user-config.md
      rules-standards.md                # → (multiple KB sources)
      knowledge-standards.md            # → knowledge/components/knowledge-base-structure.md
      hooks-standards.md                # → knowledge/components/hooks.md
```

### Files to Update

```
.claude/commands/validate.md            # Add --cab-audit to argument table (routes to new skill)
CLAUDE.md                               # Update Extension Registry (Skills 8→9)
.claude/agents/orchestrator.md          # Add auditing-workspace to routing table
```

**Total**: 10 new files + 3 updates = 13 deliverables

---

## 3. Detailed Phase Plan

### Phase A: Skill Skeleton + Methodology

**Objective**: Create the skill with complete orchestrative instructions, classification schema, and audit methodology reference. The skill should be fully functional for a manual walkthrough after this phase.

| # | Subtask | File | Acceptance Criteria |
|---|---------|------|---------------------|
| A1 | Create SKILL.md | `SKILL.md` | Frontmatter: name, description (imperative, ≤250 chars), `agent: true`, `effort: high`, `allowed-tools: Read Grep Glob Bash`, `argument-hint`. Body: Phase 0-3 methodology, scoring rubric summary, output templates, delta logic, integration guidance |
| A2 | Create classification-schema.md | `references/classification-schema.md` | 4-level scoring rubric (ABSENT/MINIMAL/ADEQUATE/EXEMPLARY) with concrete examples per level. Finding classification (MISSING/STALE/ENHANCEMENT/CURRENT) with action-type mapping. Severity rubric (ERROR/WARN/INFO). Contextual tier adjustments (minimal/standard/advanced projects) |
| A3 | Create audit-methodology.md | `references/audit-methodology.md` | Formalized PA-01 workflow: Phase 0 (context discovery), Phase 1 (structural gate), Phase 2 (7-dimension standards audit), Phase 3 (synthesis + artifact generation). YAML artifact schema definition. Markdown summary template. Delta computation logic. `.cab-audit-ignore` override mechanism |

**Phase Gate**: SKILL.md loads via `/memory`. Methodology documents are coherent and cross-referenced. Skill description triggers on "audit workspace", "check project standards", "cab audit".

### Phase B: Standard Packs

**Objective**: Create 7 modular standard packs, each containing a checklist of CAB-specific requirements linked to its authoritative KB source. Each pack should be independently readable and total under ~400-500 tokens.

| # | Subtask | File | KB Source | Key Criteria to Check |
|---|---------|------|-----------|-----------------------|
| B1 | CLAUDE.md standards | `references/standards/claudemd-standards.md` | `knowledge/components/memory-claudemd.md` | Seed instruction architecture, size discipline, @imports, extension registry table, domain guidelines, available commands table, learned corrections section |
| B2 | Agent standards | `references/standards/agent-standards.md` | `knowledge/components/subagents.md` | 16 frontmatter fields coverage, `tools` field (not `allowedTools`), `model` valid values, `description` with auto-delegation cue, `## Verification` section, no invalid fields (context:, allowedTools) |
| B3 | Skill standards | `references/standards/skill-standards.md` | `knowledge/components/agent-skills.md` | Imperative description format, ≤250 char description, `argument-hint`, `allowed-tools` scoped, `effort` set, `agent: true` when appropriate, invocation control |
| B4 | Settings standards | `references/standards/settings-standards.md` | `knowledge/schemas/global-user-config.md` | `permissions.deny` for destructive ops, `permissions.allow` patterns, `effortLevel`, hooks section, sandbox config, `$schema` for validation |
| B5 | Rules standards | `references/standards/rules-standards.md` | `knowledge/components/memory-claudemd.md` + general | `paths:` frontmatter for scoping, policy coverage (code style, security, domain, interaction), not duplicating CLAUDE.md, rules under `.claude/rules/` |
| B6 | Knowledge standards | `references/standards/knowledge-standards.md` | `knowledge/components/knowledge-base-structure.md` | INDEX.md with `file_count`, frontmatter on KB files (id, tags, summary, depends_on, source, confidence), no orphans, no dead refs, atomic sizing (≤300 lines) |
| B7 | Hooks standards | `references/standards/hooks-standards.md` | `knowledge/components/hooks.md` | Valid event names, `type: "command"` for security gates (not `"prompt"`), referenced scripts exist, PreToolUse for destructive op blocking, matcher patterns |

**Standard Pack Template** (each file follows this structure):

```markdown
---
dimension: [dimension_name]
kb_source: knowledge/path/to/source.md
last_verified: 2026-04-07
---

# [Dimension] Audit Standards

> Source of truth: [kb_source link]. This pack contains the CAB-specific
> delta checklist — criteria extractable from the KB source for audit purposes.

## Universal Criteria (all project tiers)

| # | Criterion | Check Method | Severity |
|---|-----------|-------------|----------|
| 1 | [criterion] | [Read/Grep/Glob instruction] | ERROR/WARN/INFO |

## Contextual Criteria (by project tier)

| # | Criterion | Minimal | Standard | Advanced |
|---|-----------|---------|----------|----------|
| 1 | [criterion] | N/A | WARN | ERROR |

## Scoring Guide

| Score | What it looks like for this dimension |
|-------|---------------------------------------|
| 0 ABSENT | [concrete example] |
| 1 MINIMAL | [concrete example] |
| 2 ADEQUATE | [concrete example] |
| 3 EXEMPLARY | [concrete example] |
```

**Phase Gate**: Each pack is under 500 tokens, links to valid KB source, contains ≥5 criteria with severity assignments, scoring guide has concrete examples.

### Phase C: Integration Updates

**Objective**: Wire the new skill into existing CAB infrastructure.

| # | Subtask | File | Change |
|---|---------|------|--------|
| C1 | Update validate command | `.claude/commands/validate.md` | Add `--cab-audit` to argument table: "Routes to auditing-workspace skill for CAB standards compliance audit" |
| C2 | Update CLAUDE.md | `CLAUDE.md` | Extension Registry: Skills 8→9, add `auditing-workspace` entry |
| C3 | Update orchestrator | `.claude/agents/orchestrator.md` | Add routing: audit/standards-check requests → `auditing-workspace` skill |

**Phase Gate**: `/validate --cab-audit` correctly documents routing to new skill. CLAUDE.md registry is accurate. Orchestrator recognizes audit requests.

### Phase D: Integration Testing

**Objective**: Validate the skill produces meaningful results on real projects.

| # | Test | Target | Success Criteria |
|---|------|--------|-----------------|
| D1 | Self-audit | CAB plugin itself | Produces scored findings across all 7 dimensions. YAML artifact parseable. Markdown summary is actionable. |
| D2 | Global config audit | `~/.claude/` | Reproduces ≥80% of PA-01's 9 ERROR findings. New findings are valid (not false positives). |
| D3 | Delta test | Run D1 twice | Second run detects prior audit, produces delta section showing 0 change. |
| D4 | Structural gate test | Intentionally broken project | Phase 1 correctly blocks Phase 2, suggests `/validate --full` |

**Phase Gate**: All 4 tests produce expected results. No false positives on real projects.

---

## 4. SKILL.md Content Architecture

The SKILL.md is the core deliverable. Here's the structural outline:

```markdown
---
name: auditing-workspace
description: >-
  INVOKE THIS SKILL to audit a CC-integrated project workspace against CAB
  v1.1.0 standards. Triggers: audit project, check standards compliance,
  cab audit, workspace health check, review CC configuration quality.
  Performs read-only 7-dimension assessment with scored findings and
  produces persistent YAML + markdown artifacts for remediation planning.
argument-hint: "Target path (default: cwd) and options (e.g., '--changed-only')"
agent: true
effort: high
allowed-tools: Read, Grep, Glob, Bash
---

# Workspace Audit

## Overview
[Purpose, scope, what it IS and IS NOT]

## Instructions

### Phase 0: Context Discovery
[Project type detection, complexity tier, component counts, previous audit check]

### Phase 1: Structural Pre-Check
[Reuse validating-structure logic. Gate: critical issues → STOP]

### Phase 2: Standards Audit (7 Dimensions)
[For each dimension: read standard pack → read target files → evaluate → score → classify]

### Phase 3: Synthesis + Artifact Generation
[Aggregate scores, rank findings, compute delta, generate YAML + markdown]

## Output Specifications
[YAML schema, markdown template, file naming convention]

## Flags
[--changed-only for incremental re-audit]

## See Also
[Links to standard packs, classification schema, methodology doc, related skills]
```

**Target size**: ~150-180 lines (within skill best practices, leaves room for references to handle detail).

---

## 5. Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Skill body exceeds optimal size | Medium | Low — slightly higher token load | Decompose into references/ (methodology + classification already externalized) |
| Standard packs drift from KB | High (over time) | Medium — stale recommendations | `last_verified:` date in frontmatter; `review_by:` for freshness tracking |
| False positives on diverse projects | Medium | Medium — erodes trust | Two-tier rubric (universal vs. contextual) + `.cab-audit-ignore` |
| YAML artifact schema changes break /execute-task integration | Low | Medium — downstream consumer fails | Version field in artifact (`audit_version: "1.0"`) for compatibility |
| Token overload from loading 7 packs | Medium | High — forced compaction | Sequential dimension processing, never load all packs simultaneously; skill instructions enforce this |

---

## 6. Sequencing & Dependencies

```
Phase A (skeleton + methodology)
    │
    ├── A1: SKILL.md ← no dependencies
    ├── A2: classification-schema.md ← no dependencies
    └── A3: audit-methodology.md ← depends on A2 (references classification)
    │
    ▼ Gate: Skill loads, methodology coherent
    │
Phase B (standard packs) ← depends on A complete
    │
    ├── B1-B7: All 7 packs (can be done in parallel)
    │          Each reads its KB source file for criteria extraction
    │
    ▼ Gate: All packs valid, under 500 tokens each
    │
Phase C (integration) ← depends on A complete (not B)
    │
    ├── C1: validate.md update
    ├── C2: CLAUDE.md update
    └── C3: orchestrator.md update
    │
    ▼ Gate: Integration points documented
    │
Phase D (testing) ← depends on A + B + C complete
    │
    ├── D1: Self-audit (CAB)
    ├── D2: Global config audit
    ├── D3: Delta test
    └── D4: Structural gate test
    │
    ▼ Gate: All tests pass
```

**Phases B and C can run in parallel** (C only depends on A for skill name/description).

---

## 7. Acceptance Criteria (Overall)

| # | Criterion | Verification Method |
|---|-----------|-------------------|
| AC-1 | Skill loads and appears in `/memory` output | Run `/memory`, search for auditing-workspace |
| AC-2 | Description triggers on audit-related prompts | Test: "audit this workspace against CAB standards" |
| AC-3 | 7 standard packs exist, each ≤500 tokens, each links to valid KB source | Token count + file existence + link validation |
| AC-4 | YAML artifact produced with correct schema | Parse output YAML, validate all required fields present |
| AC-5 | Markdown summary matches YAML data | Cross-check scores and findings between formats |
| AC-6 | Delta report works on repeat audit | Run twice, verify delta section populated |
| AC-7 | Structural gate blocks on broken projects | Test with missing CLAUDE.md |
| AC-8 | CAB self-audit produces ≥5 meaningful findings | Run on CAB, verify findings are legitimate |
| AC-9 | Global config audit reproduces ≥80% of PA-01 ERRORs | Compare findings against `notes/pa-01-global-config-audit-2026-04-06.md` |
| AC-10 | CLAUDE.md, validate.md, orchestrator.md updated | File inspection |

---

## 8. Estimated Effort

| Phase | Files | Estimated Lines | Complexity |
|-------|-------|----------------|------------|
| A (skeleton) | 3 | ~400 (SKILL ~170, classification ~120, methodology ~110) | Medium — encoding proven methodology |
| B (standard packs) | 7 | ~350 total (~50 each) | Low-Medium — criteria extraction from existing KB |
| C (integration) | 3 | ~15 total (small edits) | Low |
| D (testing) | 0 (runtime) | N/A | Medium — judgment on test results |

**Total new content**: ~750 lines across 10 new files + ~15 lines of updates.

---

## 9. Post-Implementation TODO

After this skill is validated:

1. **Test on user's project** — First real-world audit outside CAB ecosystem
2. **Wire `planning-implementation` skill** to consume `cab-audit-*.yaml` artifacts
3. **Evaluate `--changed-only` mode** — Add incremental re-audit once baseline established
4. **Consider hook integration** — Lightweight Stop-event prompt for regression awareness
5. **Update TODO.md** — Mark "standardized audit/freshness-check" as DONE
