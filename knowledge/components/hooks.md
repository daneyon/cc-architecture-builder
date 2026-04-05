---
id: hooks
title: Hooks
category: components
tags: [hooks, events, automation, validation, event-driven, lifecycle]
summary: Event-driven automation via 26 lifecycle events and 4 hook types. Enables validation, formatting, logging, and custom workflows triggered by CC system events.
depends_on: [memory-claudemd]
related: [custom-commands, mcp-integration, orchestration-framework, agent-skills]
complexity: intermediate
last_updated: 2026-04-05
estimated_tokens: 1100
source: https://code.claude.com/docs/en/hooks
confidence: A
review_by: 2026-07-05
---

# Hooks

> **Intermediary note**: This file documents CAB-specific hook patterns and extensions.
> For native hook mechanics, configuration syntax, and event payload schemas, see the
> [official hooks documentation](https://code.claude.com/docs/en/hooks).

## Overview

Hooks are **event-driven** automation points that execute automatically in response to Claude Code lifecycle events. CC exposes **26 events** across the session lifecycle, tool use, agent coordination, permissions, and configuration domains. Hooks can be implemented as **4 types**: shell commands, HTTP endpoints, prompt injections, or agent dispatches.

## Hook Types

| Type      | Syntax                              | Use Case                                 | Blocking?                  |
| --------- | ----------------------------------- | ---------------------------------------- | -------------------------- |
| `command` | Shell command (bash/zsh/powershell) | Scripts, formatters, validators          | Yes (unless `async: true`) |
| `http`    | URL endpoint (POST with JSON)       | Webhooks, external integrations, logging | Yes (unless `async: true`) |
| `prompt`  | Inline text injected into context   | Context enrichment, dynamic instructions | N/A (injected)             |
| `agent`   | Dispatches to a subagent            | Complex reasoning on hook events         | Yes                        |

## Event Catalog (26 Events)

### Session Lifecycle

| Event                | Trigger                  | Typical Use                              |
| -------------------- | ------------------------ | ---------------------------------------- |
| `SessionStart`       | Session begins           | Initialization, env validation           |
| `SessionEnd`         | Session ends             | Logging, cleanup, state persistence      |
| `InstructionsLoaded` | CLAUDE.md / rules loaded | Instruction validation, freshness checks |
| `ConfigChange`       | Settings modified        | Config audit, notification               |

### User Interaction

| Event                | Trigger                   | Typical Use                         |
| -------------------- | ------------------------- | ----------------------------------- |
| `UserPromptSubmit`   | User submits a prompt     | Input validation, context injection |
| `Notification`       | Claude sends notification | Custom alerts, external routing     |
| `Elicitation`        | Claude asks user question | Logging, auto-response in CI        |
| `ElicitationResult`  | User answers elicitation  | Response auditing                   |

### Tool Use

| Event                | Trigger                    | Typical Use                          |
| -------------------- | -------------------------- | ------------------------------------ |
| `PreToolUse`         | Before any tool invocation | Approval gates, input validation     |
| `PostToolUse`        | After successful tool use  | Formatting, logging, QA checks       |
| `PostToolUseFailure` | After failed tool use      | Error logging, retry logic, alerting |

### Agent & Task Coordination

| Event           | Trigger                     | Typical Use                                   |
| --------------- | --------------------------- | --------------------------------------------- |
| `Stop`          | Claude attempts to stop     | Final validation, cleanup                     |
| `StopFailure`   | Stop attempt fails          | Error recovery                                |
| `SubagentStop`  | Subagent attempts to stop   | Subagent result validation                    |
| `SubagentStart` | Subagent spawned            | Logging, resource tracking                    |
| `TaskCreated`   | New task created            | Task tracking, audit                          |
| `TaskCompleted` | Task finishes               | Result validation, notifications              |
| `TeammateIdle`  | Teammate agent goes idle    | Load balancing, task reassignment             |

### Permissions

| Event               | Trigger              | Typical Use                 |
| ------------------- | -------------------- | --------------------------- |
| `PermissionRequest` | Permission requested | Auto-approve rules, logging |
| `PermissionDenied`  | Permission denied    | Audit, alternative routing  |

### Context & Environment

| Event            | Trigger                     | Typical Use                                    |
| ---------------- | --------------------------- | ---------------------------------------------- |
| `PreCompact`     | Before context compaction   | State preservation, summary injection          |
| `PostCompact`    | After context compaction    | State restoration, verification                |
| `CwdChanged`     | Working directory changes   | Path validation, env reload                    |
| `FileChanged`    | Watched file modified       | Hot reload, re-validation                      |
| `WorktreeCreate` | Git worktree created        | Worktree initialization                        |
| `WorktreeRemove` | Git worktree removed        | Cleanup, resource release                      |

## Configuration Locations (6 Sources)

CC merges all hook sources at startup and **freezes the config snapshot** — runtime changes are not picked up until the next session (security pattern: prevents runtime injection).

| Location                         | Scope                | Precedence |
| -------------------------------- | -------------------- | ---------- |
| `~/.claude/hooks.json`           | Global user          | Lowest     |
| `~/.claude/settings.json`        | Global user settings |            |
| `.claude/hooks.json`             | Project-level        |            |
| `.claude/settings.json`          | Project settings     |            |
| Plugin `hooks/hooks.json`        | Plugin-scoped        |            |
| Plugin `plugin.json` hooks field | Plugin-scoped        | Highest    |

**CAB default**: Plugin-level `hooks/hooks.json` for distributable patterns.

## Key Configuration Fields

```jsonc
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",          // Regex — which tools/events to match
        "hooks": [
          {
            "type": "command",             // command | http | prompt | agent
            "command": "./scripts/fmt.sh", // Shell command (type: command)
            // "url": "https://...",       // Endpoint (type: http)
            // "prompt": "Check output",   // Injected text (type: prompt)
            "if": "tool_name == 'Write'",  // Permission-rule-syntax filter
            "async": false,                // true = non-blocking (fire-and-forget)
            "once": true,                  // Single-fire (skills only)
            "shell": "powershell"          // Per-hook shell override (Windows)
          }
        ]
      }
    ]
  }
}
```

### Field Reference

| Field     | Type           | Description                                                              |
| --------- | -------------- | ------------------------------------------------------------------------ |
| `matcher` | string (regex) | Regex filter for tools/events. Supports `\|` alternation. Omit = all.    |
| `type`    | enum           | `command`, `http`, `prompt`, or `agent`                                  |
| `command` | string         | Shell command to execute (type: command)                                 |
| `url`     | string         | HTTP endpoint for POST (type: http)                                      |
| `prompt`  | string         | Text injected into context (type: prompt)                                |
| `if`      | string         | Permission-rule-syntax conditional filter for fine-grained control       |
| `async`   | bool           | `true` = non-blocking execution. Does not gate the action.               |
| `once`    | bool           | `true` = fires only once per session. Primarily for skill hooks.         |
| `shell`   | string         | Override shell for this hook (e.g., `powershell` on Windows)             |

**MCP tool matching**: Use `mcp__<server>__<tool>` naming — e.g., `mcp__github__.*` matches all tools from the `github` server.

## Environment Variables (Shell)

| Variable             | Description                               |
| -------------------- | ----------------------------------------- |
| `CLAUDE_PLUGIN_ROOT` | Absolute path to plugin directory         |
| `CLAUDE_PROJECT_DIR` | Absolute path to the project root         |
| `CLAUDE_PLUGIN_DATA` | Plugin-specific data directory            |
| `CLAUDE_CODE_REMOTE` | `true` if running in remote/headless mode |
| `CLAUDE_ENV_FILE`    | Path to the active `.env` file            |

## Hook Output Schema

Hooks communicate back to CC via **exit codes** or **structured JSON on stdout**.

**Exit codes**: `0` = success/continue, `1` = failure/show error, `2` = block action (`Pre*` hooks only).

**JSON output** — CC reads the first valid JSON object from stdout (max **10,000 characters**):

| Field                | Events                             | Description                                          |
| -------------------- | ---------------------------------- | ---------------------------------------------------- |
| `continue`           | All                                | Boolean — whether to proceed                         |
| `message`            | All                                | Feedback string displayed to user                    |
| `addToPrompt`        | All                                | String injected into conversation context            |
| `updatedInput`       | `PreToolUse`, `UserPromptSubmit`   | Rewritten tool input or prompt (replaces original)   |
| `permissionDecision` | `PermissionRequest`                | `"allow"` or `"deny"` — programmatic permission      |
| `decision`           | `Pre*` hooks                       | `"block"`, `"allow"`, or `"modify"`                  |

## Hook Execution Model

- **Parallel execution**: Multiple hooks on the same event run in parallel
- **Deduplication**: Hooks with identical `command` or `url` are deduped (only one instance runs)
- **Frozen at startup**: Hook config is snapshot at session start — not hot-reloaded
- **Two-phase skill loading**: Skill frontmatter parsed at startup; full content loaded on invocation
- **Interactive inspection**: Use `/hooks` browser within a CC session to view all registered hooks, sources, and matchers

## CAB-Specific Hook Patterns

### Pattern 1: PostToolUse Auto-Format (QA/QC)

Standard CAB quality gate — auto-format files after Write/Edit operations:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh" }]
      }
    ]
  }
}
```

### Pattern 2: PreToolUse Security Gate

Intercept Bash tool use for destructive command detection. Script reads `tool_input` from stdin, pattern-matches against dangerous commands, returns `{"decision": "block", "reason": "..."}` or exits `0`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/security-gate.sh" }]
      }
    ]
  }
}
```

### Pattern 3: Freshness Validation (InstructionsLoaded)

Validate that CLAUDE.md and rules haven't drifted from source of truth:

```json
{
  "hooks": {
    "InstructionsLoaded": [
      { "hooks": [{ "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/check-freshness.sh" }] }
    ]
  }
}
```

### Pattern 4: Async Session Telemetry

Fire-and-forget logging to an external service — `async: true` prevents blocking:

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [{ "type": "http", "url": "https://telemetry.internal/api/cc-session", "async": true }] }
    ]
  }
}
```

### Pattern 5: Stop Hook for Final Validation

Ensure deliverables meet standards before session ends:

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [{ "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/final-check.sh" }] }
    ]
  }
}
```

## Best Practices

1. **Keep hooks fast** — Slow synchronous hooks degrade UX. Use `async: true` for non-critical logging.
2. **Use matchers precisely** — Broad matchers fire on every tool call. Be specific.
3. **Prefer exit codes for simple gates** — JSON output only when you need `updatedInput` or `addToPrompt`.
4. **Test with `/hooks` browser** — Verify hooks trigger on intended events before deployment.
5. **Security hooks in global config** — Project-level hooks can be overridden; global hooks cannot.
6. **Remember the frozen snapshot** — Hook config changes require a new session to take effect.

## See Also

- [Custom Commands](custom-commands.md) — User-invoked slash commands
- [MCP Integration](mcp-integration.md) — External tool connections
- [Agent Skills](agent-skills.md) — `once: true` hooks in skill context
- [Orchestration Framework](../operational-patterns/orchestration-framework.md) — Hooks in task execution protocol
- [Official Hooks Documentation](https://code.claude.com/docs/en/hooks) — Canonical reference for all events, payloads, and configuration
