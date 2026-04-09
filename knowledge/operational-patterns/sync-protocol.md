---
id: sync-protocol
title: CAB ↔ Global Sync Protocol
category: operational-patterns
tags: [sync, deployment, global, upstream, downstream, drift, freshness]
summary: Protocol for propagating CAB plugin changes to global ~/.claude/ config and detecting drift between upstream (CAB) and downstream (global) extensions.
depends_on: [orchestration-framework, session-lifecycle]
related: [extension-discovery, team-collaboration]
complexity: intermediate
last_updated: 2026-04-05
estimated_tokens: 600
source: CAB-original
confidence: B
review_by: 2026-07-05
---

# CAB ↔ Global Sync Protocol

## Overview

CAB (upstream) is the authoritative source for architecture patterns, agent definitions,
skill templates, and command specifications. The global `~/.claude/` config (downstream)
is the deployed runtime where these extensions execute. Drift between them causes
behavior divergence and stale patterns.

## Sync Direction

```
CAB Plugin (upstream/authoritative)
    │
    ├── agents/            ──→  ~/.claude/agents/
    ├── skills/            ──→  ~/.claude/skills/
    ├── commands/          ──→  ~/.claude/commands/
    ├── templates/        ──→  (scaffolding reference only, not deployed)
    └── knowledge/        ──→  (reference only, not deployed)
    
    settings.json         ──→  ~/.claude/settings.json (merge, not overwrite)
    rules (via CLAUDE.md) ──→  ~/.claude/rules/ + ~/.claude/CLAUDE.md
```

**One-way flow**: CAB → Global. Global never writes back to CAB.
Exceptions: `settings.local.json` and `CLAUDE.local.md` are global-only (personal, gitignored).

## Sync Triggers

| Trigger | Action | Verification |
|---------|--------|--------------|
| After T-tier completion (audit) | Deploy changed agents/skills/commands | Diff CAB vs global, confirm no regressions |
| Version bump | Full sync of all component directories | `/validate` on deployed global config |
| New agent/skill added | Deploy single component | Test invocation in a fresh session |
| Settings change | Merge into global settings.json | Verify precedence didn't break overrides |

## Sync Procedure

### 1. Diff

Compare CAB authoritative files against deployed global copies:

```bash
# Agent diff
diff -rq agents/ ~/.claude/agents/

# Skill diff (skill directories)
diff -rq skills/ ~/.claude/skills/

# Command diff
diff -rq commands/ ~/.claude/commands/

# Settings diff (manual review — merge, don't overwrite)
diff .claude/settings.json ~/.claude/settings.json
```

### 2. Deploy

Copy changed files. Never blindly overwrite — merge where needed:

```bash
# Component directories (safe to overwrite — CAB is authoritative)
cp -r agents/*.md ~/.claude/agents/
cp -r skills/*/SKILL.md ~/.claude/skills/
cp -r commands/*.md ~/.claude/commands/

# Settings (MERGE — global may have personal additions)
# Manual review required — use diff output to guide selective updates
```

### 3. Verify

After deployment:

- Start a fresh CC session
- Confirm all agents route correctly (`/agents` or natural delegation)
- Confirm all skills appear (`/` autocomplete)
- Confirm settings took effect (`model`, `agent`, `permissions`)
- Run `/context-sync` to validate session state

## Drift Detection

### Indicators

| Signal | Likely Cause |
|--------|-------------|
| Agent not routing to expected specialist | Agent description changed in CAB but not deployed |
| Skill missing from autocomplete | Skill added to CAB but not copied to global |
| Permission denied unexpectedly | settings.json update not merged to global |
| Stale behavior after audit | Full sync not performed post-tier completion |

### Automated Check (future)

A `/sync-check` command could automate drift detection:

```
1. Hash all CAB agents/ skills/ commands/ files
2. Hash corresponding ~/.claude/ files
3. Report mismatches with file-level diff summary
4. Optionally auto-deploy with confirmation
```

This is a candidate for T5 or post-audit implementation.

## Constraints

- **Never auto-deploy settings.json** — always manual merge (global may have personal additions)
- **Never deploy templates/** — templates are scaffolding references, not runtime components
- **Never deploy knowledge/** — KB is for Claude's reference within CAB project context only
- **Preserve global-only extensions** — global may have agents/skills not in CAB; sync must not delete them
