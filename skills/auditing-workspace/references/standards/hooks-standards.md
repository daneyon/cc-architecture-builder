---
dimension: hooks
kb_source: knowledge/components/hooks.md
last_verified: 2026-04-07
---

# Hooks Configuration Audit Standards

> Source of truth: `knowledge/components/hooks.md`. This pack contains the
> CAB-specific delta checklist for hooks quality assessment. Hooks are
> event-driven automation with 26 events and 4 types (command, http, prompt, agent).

## Universal Criteria (all project tiers)

| # | Criterion | Check Method | Severity |
|---|-----------|-------------|----------|
| 1 | Hook event names are valid (from the 26 official events) | Check against event catalog | ERROR |
| 2 | `type: "command"` hooks reference scripts that exist | Verify script paths | ERROR |
| 3 | Hook JSON is valid syntax | JSON parse | ERROR |
| 4 | No credentials in hook scripts or configs | Grep for sensitive patterns | ERROR |

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
