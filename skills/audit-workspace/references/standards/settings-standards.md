---
dimension: settings
kb_source: knowledge/schemas/global-user-config.md
last_verified: 2026-04-09
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

## Structural Validity Criteria (all project tiers)

CC validates settings.json against a strict JSON schema. A single structural
error causes the ENTIRE file to be rejected — all permissions, hooks, agent
routing, and sandbox are silently disabled. These criteria MUST be checked
before any presence-based criteria below.

| # | Criterion | Check Method | Severity |
|---|-----------|-------------|----------|
| 16 | `$schema` value is exactly `https://json.schemastore.org/claude-code-settings.json` (not just present — wrong URL = entire file rejected) | String comparison | ERROR |
| 17 | `enabledPlugins` is object type `{}` (not array `[]`). Keys are `"name@marketplace"`, values are boolean or string array | `isinstance(data['enabledPlugins'], dict)` | ERROR |
| 18 | Hooks follow nested hookMatcher pattern: each event → array of `{ matcher?, hooks: [{ type, command\|url\|prompt }] }`. The inner `hooks` array is REQUIRED. Flat structure `{ type, command, matcher }` is INVALID | Validate nesting depth + required `hooks` array | ERROR |
| 19 | `sandbox` has only CC-recognized keys (`enabled`, `filesystem`, `network`, `excludedCommands`, `autoAllowBashIfSandboxed`, `ignoreViolations`, etc.). `additionalProperties: false` — extra keys like `permissions` or `_comment` cause rejection | Key allowlist check | ERROR |
| 20 | All top-level field names are CC-recognized. Catch typos like `enabledMcpServers` (should be `enabledMcpjsonServers`) or `subagentModel` (not a CC field) | Compare against official field catalog | WARN |
| 21 | hookMatcher objects have ONLY `matcher` (optional string) and `hooks` (required array) keys. `additionalProperties: false` — `_comment`, `type`, `command` at this level are INVALID | Key allowlist check per hookMatcher | ERROR |

## Contextual Criteria (by project tier)

| # | Criterion | Minimal | Standard | Advanced |
|---|-----------|---------|----------|----------|
| 5 | `permissions.deny` includes destructive operations (rm -rf, git push --force, etc.) | N/A | WARN | ERROR |
| 6 | `permissions.allow` patterns defined for common safe operations | N/A | INFO | WARN |
| 7 | `$schema` field present (structural validity of value checked in #16 above) | N/A | INFO | INFO |
| 8 | Hooks section configured (at least SessionStart or PreToolUse). Structure validated in #18 above | N/A | INFO | WARN |
| 9 | `sandbox` configured (`enabled: true`). Structure validated in #19 above | N/A | N/A | WARN |
| 10 | No deprecated field names (`reasoningEffort` → `effortLevel`, `environmentVariables` → `env`) | WARN | ERROR | ERROR |
| 11 | `agent` field set (default agent for orchestration) | N/A | INFO | WARN |
| 12 | Sensitive path protection (Write/Edit deny to settings*, .ssh/*, .aws/*) | N/A | INFO | WARN |
| 13 | Shell escape prevention (deny patterns for powershell, cmd, eval) | N/A | N/A | INFO |
| 14 | If plugin: root `settings.json` exists with `agent` key (plugin-distributed default agent) | N/A | INFO | WARN |
| 15 | If plugin: root `settings.json` contains ONLY `agent` key (no non-plugin fields like permissions, hooks, effortLevel — those belong in `.claude/settings.json`) | N/A | INFO | WARN |

## Scoring Guide

Structural validity (criteria #16-#21) is a prerequisite. Any structural ERROR
caps the score at 1 regardless of how many contextual criteria pass — because
CC rejects the entire file on schema violation.

| Score | What it looks like |
|-------|-------------------|
| 0 ABSENT | No project settings.json, relying entirely on defaults |
| 1 MINIMAL | settings.json exists with basic fields; no permissions, no hooks. Also: structurally invalid files (wrong $schema, flat hooks, wrong types) are capped here |
| 2 ADEQUATE | All structural criteria PASS + permissions defined (some allow + deny), effort level set, no deprecated fields |
| 3 EXEMPLARY | All structural criteria PASS + comprehensive deny rules, allow patterns, valid hooks, correct $schema, sandbox, agent field, sensitive path protection |
