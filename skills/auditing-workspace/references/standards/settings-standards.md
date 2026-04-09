---
dimension: settings
kb_source: knowledge/schemas/global-user-config.md
last_verified: 2026-04-07
---

# Settings Configuration Audit Standards

> Source of truth: `knowledge/schemas/global-user-config.md`. This pack
> contains the CAB-specific delta checklist for settings.json quality.

## Universal Criteria (all project tiers)

| # | Criterion | Check Method | Severity |
|---|-----------|-------------|----------|
| 1 | `.claude/settings.json` exists (project-level settings — applies to both plugin and standalone) | Glob | WARN |
| 2 | Valid JSON syntax | `python -c "import json; json.load(open(...))"` | ERROR |
| 3 | No credentials or secrets in settings | Grep for key/token/secret patterns | ERROR |
| 4 | `effortLevel` set (not relying on default) | Read JSON field | INFO |

## Contextual Criteria (by project tier)

| # | Criterion | Minimal | Standard | Advanced |
|---|-----------|---------|----------|----------|
| 5 | `permissions.deny` includes destructive operations (rm -rf, git push --force, etc.) | N/A | WARN | ERROR |
| 6 | `permissions.allow` patterns defined for common safe operations | N/A | INFO | WARN |
| 7 | `$schema` field for editor validation/autocomplete | N/A | INFO | INFO |
| 8 | Hooks section configured (at least SessionStart or PreToolUse) | N/A | INFO | WARN |
| 9 | `sandbox` configured (`enabled: true`) | N/A | N/A | WARN |
| 10 | No deprecated field names (`reasoningEffort` → `effortLevel`, `environmentVariables` → `env`) | WARN | ERROR | ERROR |
| 11 | `agent` field set (default agent for orchestration) | N/A | INFO | WARN |
| 12 | Sensitive path protection (Write/Edit deny to settings*, .ssh/*, .aws/*) | N/A | INFO | WARN |
| 13 | Shell escape prevention (deny patterns for powershell, cmd, eval) | N/A | N/A | INFO |
| 14 | If plugin: root `settings.json` exists with `agent` key (plugin-distributed default agent) | N/A | INFO | WARN |
| 15 | If plugin: root `settings.json` contains ONLY `agent` key (no non-plugin fields like permissions, hooks, effortLevel — those belong in `.claude/settings.json`) | N/A | INFO | WARN |

## Scoring Guide

| Score | What it looks like |
|-------|-------------------|
| 0 ABSENT | No project settings.json, relying entirely on defaults |
| 1 MINIMAL | settings.json exists with basic fields; no permissions, no hooks |
| 2 ADEQUATE | Permissions defined (some allow + deny), effort level set, no deprecated fields |
| 3 EXEMPLARY | Comprehensive deny rules, allow patterns, hooks, $schema, sandbox, agent field, sensitive path protection |
