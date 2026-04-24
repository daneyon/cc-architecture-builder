---
dimension: hooks
kb_source: knowledge/components/hooks.md
last_verified: 2026-04-09
---

# Hooks Configuration Audit Standards

> Source of truth: `knowledge/components/hooks.md`. This pack contains the
> CAB-specific delta checklist for hooks quality assessment. Hooks are
> event-driven automation with 26 events and 4 types (command, http, prompt, agent).

## Universal Criteria (all project tiers)

| # | Criterion | Check Method | Severity |
|---|-----------|-------------|----------|
| 1 | Hook event names are valid (from the 22 official events — see event catalog below) | Check against event catalog | ERROR |
| 2 | `type: "command"` hooks reference scripts that exist | Verify script paths | ERROR |
| 3 | Hook JSON is valid syntax | JSON parse | ERROR |
| 4 | No credentials in hook scripts or configs | Grep for sensitive patterns | ERROR |
| 14 | Hooks follow nested hookMatcher structure: each event → array of `{ matcher?, hooks: [{ type, ... }] }`. The `hooks` array inside each matcher is REQUIRED. Flat structure (type/command/matcher at same level) is INVALID and causes CC to reject the entire settings file | Validate `hooks` key exists in each matcher object | ERROR |
| 15 | hookMatcher objects have ONLY `matcher` (optional) and `hooks` (required) keys. CC enforces `additionalProperties: false` — keys like `_comment`, `type`, `command` at the matcher level cause rejection | Key allowlist check | ERROR |
| 16 | hookCommand objects inside `hooks[]` have `type` (required) plus type-specific required fields: `command` for type=command, `url` for type=http, `prompt` for type=prompt/agent | Validate per-type required fields | ERROR |

## Contextual Criteria (by project tier)

| # | Criterion | Minimal | Standard | Advanced |
|---|-----------|---------|----------|----------|
| 5 | Any hooks configured at all | N/A | INFO | WARN |
| 13 | If plugin: hooks defined in `hooks/hooks.json` (not only in `.claude/settings.json`) | N/A | INFO | WARN |
| 6 | Security gate via `PreToolUse` with `type: "command"` | N/A | INFO | WARN |
| 7 | Security hooks use `type: "command"` not `type: "prompt"` for gates | N/A | WARN | ERROR |
| 8 | `matcher` patterns used for targeted hook application | N/A | INFO | WARN |
| 9 | `async: true` on non-blocking hooks (logging, telemetry) | N/A | N/A | INFO |
| 10 | Hook scripts use deterministic logic (exit codes, not LLM judgment) | N/A | WARN | ERROR |
| 11 | `SessionStart` hook for initialization/validation | N/A | N/A | INFO |
| 12 | `if` conditional for platform-specific hooks | N/A | N/A | INFO |

## Scoring Guide

| Score | What it looks like |
|-------|-------------------|
| 0 ABSENT | No hooks configured anywhere |
| 1 MINIMAL | Basic hooks exist but may use wrong types (prompt for security), missing scripts |
| 2 ADEQUATE | Valid hooks with command-type security gates, scripts exist, proper event names |
| 3 EXEMPLARY | PreToolUse security gates with deterministic scripts, matcher patterns, async on non-blocking hooks, SessionStart initialization, comprehensive event coverage appropriate to project |
