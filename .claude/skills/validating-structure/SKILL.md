---
name: validating-structure
description: >
  INVOKE THIS SKILL to validate Claude Code project structure against CAB
  architecture standards. Triggers: validate project, check structure, audit
  plugin, verify compliance, pre-publish check. Runs required-file checks,
  plugin.json validation, CLAUDE.md validation, component validation (skills,
  agents, commands, hooks), security audit, and KB consumption audit.
argument-hint: "Validation mode and target (e.g., '--full', '--security', '--prepublish', or path to project)"
---

# Structure Validation

## Overview

This skill validates Claude Code projects against the standardized architecture, identifying issues and providing remediation guidance.

## Instructions

### Step 1: Identify Project Type

Determine if validating:
- Global user config (`~/.claude/`)
- Plugin project (has `.claude-plugin/plugin.json`)
- Hybrid/custom structure

### Step 2: Run Validation Checks

#### For Plugin Projects

**Required Files Check**:
```
□ .claude-plugin/plugin.json exists
□ CLAUDE.md exists
□ README.md exists
□ .gitignore exists
```

**plugin.json Validation**:
```
□ "name" field present (kebab-case)
□ "version" field present (semver format)
□ "description" field present
□ Valid JSON syntax
```

**CLAUDE.md Validation**:
```
□ File not empty
□ Contains project purpose
□ References knowledge base (if exists)
□ Lists available commands (if any)
```

**Directory Structure Check**:
```
□ Component directories under .claude/ (per CC project schema)
  - .claude/commands/ (if used)
  - .claude/agents/ (if used)
  - .claude/skills/ (if used)
  - hooks/ (if used)
□ knowledge/ has INDEX.md (if knowledge exists)
```

**Skills Validation** (for each skill):
```
□ SKILL.md exists in skill directory
□ name field: ≤64 chars, lowercase+hyphens only
□ description field: non-empty, ≤1024 chars
□ No reserved words in name
```

**Agents Validation** (for each agent):
```
□ Frontmatter includes name and description
□ tools field valid if present
□ model field valid if present (sonnet/opus/haiku/inherit)
```

**Commands Validation** (for each command):
```
□ description in frontmatter
□ Clear instructions in body
```

**Hooks Validation**:
```
□ hooks.json valid JSON
□ Event names valid
□ Referenced scripts exist
□ Scripts are executable
```

#### For Global User Config

**Structure Check**:
```
□ ~/.claude/CLAUDE.md exists (recommended)
□ ~/.claude/skills/ properly structured (if exists)
□ ~/.claude/agents/ properly structured (if exists)
□ settings.local.json valid JSON (if exists)
```

### Step 3: Security Audit (Pre-Publication)

```
□ No API keys, tokens, or passwords in any file
□ No .env files committed
□ .gitignore excludes sensitive patterns
□ No PII in knowledge base
□ No proprietary content (if public distribution)
```

### Step 4: Generate Report

Output format:

```
# Validation Report

## Summary
- Project Type: [Plugin/Global Config]
- Status: [PASS/FAIL/WARNINGS]
- Checks Run: X
- Issues Found: Y

## Required Files
[✓/✗] List of required file checks

## Structure
[✓/✗] Directory structure compliance

## Components
[✓/✗] Per-component validation results

## Security
[✓/✗] Security audit results (if --security flag)

## Issues Found
1. [ISSUE]: Description
   [FIX]: Remediation steps

## Recommendations
- Suggested improvements (non-blocking)

## Next Steps
- [ ] Action items to resolve issues
```

## Validation Modes

| Mode | Flag | Checks |
|------|------|--------|
| Standard | (default) | Structure, required files |
| Full | `--full` | Standard + all components |
| Security | `--security` | Standard + security audit |
| Pre-publish | `--prepublish` | Full + security |

## Common Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| "plugin.json not found" | Wrong directory or missing | Create `.claude-plugin/plugin.json` |
| "Skill name invalid" | Uppercase or special chars | Rename to lowercase-hyphens only |
| "Description too long" | Over 1024 chars | Shorten to key trigger info |
| "Components inside .claude-plugin/" | Wrong location | Move to project root |
| "INDEX.md missing" | Knowledge without index | Create knowledge/INDEX.md |

### KB Consumption Audit (--full mode)

When running full or pre-publish validation, also verify knowledge base integration:

1. **Orphan check**: Scan all `.md` files in `knowledge/*/` directories (excluding INDEX.md). For each KB file, search `agents/`, `skills/`, `commands/`, and `CLAUDE.md` for references to that filename. Report any KB files not referenced by any extension.

2. **Dead reference check**: Scan all `## References` and `## See Also` sections in extensions (`agents/`, `skills/`, `commands/`). Verify each referenced `knowledge/` path exists on disk.

3. **INDEX integrity**: For each `knowledge/*/INDEX.md`, verify `file_count` in frontmatter matches actual `.md` file count (excluding INDEX.md itself).

Report section:

```text
## KB Consumption
[✓/✗] Orphan check — N/N KB docs referenced by extensions
[✓/✗] Dead references — N/N extension references resolve
[✓/✗] INDEX integrity — N/N file_counts match
```

If issues found:

```text
  ✗ ORPHANED: knowledge/operational-patterns/extension-discovery.md
    → Not referenced by any extension
  ✗ DEAD REF: .claude/agents/orchestrator.md → knowledge/foo.md (not found)
  ✗ INDEX: knowledge/components/INDEX.md says 8 files, found 9
```

## See Also

- `knowledge/schemas/distributable-plugin.md` — Expected structure
- `knowledge/distribution/marketplace.md` — Publication requirements
- `knowledge/prerequisites/security-defaults.md` — Security checklist
