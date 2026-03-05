---
id: hooks
title: Hooks
category: components
tags: [hooks, events, automation, validation, event-driven]
summary: Event-driven scripts that execute automatically in response to Claude Code system events. Enable validation, automation, and custom workflows.
depends_on: [memory-claudemd]
related: [custom-commands, mcp-integration, orchestration-framework]
complexity: intermediate
last_updated: 2025-12-12
estimated_tokens: 650
---

# Hooks

## Overview

Hooks are **event-driven** scripts that execute automatically in response to Claude Code system events. They enable validation, automation, and custom workflows without explicit user invocation.

## Key Characteristics

| Aspect | Description |
|--------|-------------|
| **Trigger** | System events (not user actions) |
| **Execution** | Automatic when event fires |
| **Purpose** | Validation, formatting, logging, notifications |
| **Output** | Exit codes or JSON for control flow |

## File Structure

**Location**: `hooks/hooks.json` or inline in `plugin.json`

```
hooks/
├── hooks.json           # Hook configuration
└── scripts/             # Hook scripts (optional)
    ├── format-code.sh
    └── validate-input.py
```

## Configuration Format

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/format-code.sh"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/validate-input.py"
          }
        ]
      }
    ]
  }
}
```

## Available Events

| Event | Trigger | Common Use Cases |
|-------|---------|------------------|
| `PreToolUse` | Before Claude uses any tool | Validation, approval gates |
| `PostToolUse` | After Claude uses any tool | Formatting, logging |
| `UserPromptSubmit` | User submits prompt | Input validation, context injection |
| `Notification` | Claude sends notification | Custom alerts |
| `Stop` | Claude attempts to stop | Cleanup, final validation |
| `SubagentStop` | Subagent attempts to stop | Subagent cleanup |
| `SessionStart` | Session begins | Initialization |
| `SessionEnd` | Session ends | Logging, cleanup |
| `PreCompact` | Before context compaction | State preservation |

## Matchers

Filter which events trigger hooks:

```json
{
  "matcher": "Write|Edit",
  "hooks": [...]
}
```

- `Write|Edit` — Matches Write OR Edit tools
- Regex patterns supported
- Omit matcher to trigger on all events of that type

## Hook Output

### Simple: Exit Codes

| Exit Code | Meaning |
|-----------|---------|
| `0` | Success, continue |
| `1` | Failure, show error |
| `2` | Block action (Pre* hooks only) |

### Advanced: JSON Output

```json
{
  "continue": true,
  "message": "Validation passed",
  "addToPrompt": "Additional context to inject"
}
```

**JSON Fields**:
- `continue`: Boolean, whether to proceed
- `message`: String, feedback to display
- `addToPrompt`: String, inject into prompt
- `decision`: For Pre* hooks, control flow

## Example: Code Formatting Hook

**hooks.json**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

**scripts/format-code.sh**:
```bash
#!/bin/bash

# Get the file that was modified from hook input
FILE=$(cat | jq -r '.tool_input.file_path // empty')

if [[ -z "$FILE" ]]; then
  exit 0
fi

# Format based on extension
case "$FILE" in
  *.py) black "$FILE" 2>/dev/null ;;
  *.js|*.ts) prettier --write "$FILE" 2>/dev/null ;;
  *.md) prettier --write --prose-wrap always "$FILE" 2>/dev/null ;;
esac

exit 0
```

## Example: Input Validation Hook

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/validate-prompt.py"
          }
        ]
      }
    ]
  }
}
```

## Environment Variable

`${CLAUDE_PLUGIN_ROOT}` — Absolute path to plugin directory. Use for all script paths.

## Hook Input

Hooks receive JSON input via stdin:

**PreToolUse/PostToolUse**:
```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file",
    "content": "..."
  }
}
```

**UserPromptSubmit**:
```json
{
  "prompt": "User's message"
}
```

## Security Considerations

- Scripts must be executable (`chmod +x`)
- Validate all input from stdin
- Don't trust tool_input blindly
- Use absolute paths via `${CLAUDE_PLUGIN_ROOT}`
- Test hooks thoroughly before deployment

## Best Practices

1. **Keep hooks fast**: Slow hooks degrade UX
2. **Handle errors gracefully**: Return meaningful exit codes
3. **Log appropriately**: Don't spam, but track important events
4. **Test matchers**: Verify hooks trigger on intended events
5. **Use JSON output for complex control**: When simple exit codes aren't enough

## Advanced Pattern: Security Routing

Use PreToolUse hooks to intercept sensitive operations and apply additional
scrutiny — blocking dangerous commands, requiring confirmation, or logging
for audit:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./hooks/scripts/security-gate.sh"
          }
        ]
      }
    ]
  }
}
```

Example `security-gate.sh` (reads tool_input from stdin):

```bash
#!/bin/bash
# Block destructive commands, log sensitive operations
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block known-dangerous patterns
if echo "$CMD" | grep -qE 'rm -rf /|DROP TABLE|FORMAT|mkfs'; then
  echo '{"decision": "block", "reason": "Destructive command blocked by security hook"}'
  exit 0
fi

# Log operations on sensitive paths
if echo "$CMD" | grep -qE '\.env|credentials|secrets|private'; then
  echo "[SECURITY] $(date): Sensitive path access: $CMD" >> "${CLAUDE_PLUGIN_ROOT}/logs/security.log"
fi

# Allow by default
exit 0
```

This pattern can be extended to route security-sensitive tasks to a stronger
model or require human approval for specific operations.

## See Also

- [Custom Commands](custom-commands.md) — User-invoked actions
- [MCP Integration](mcp-integration.md) — External tool connections
- [Orchestration Framework](../operational-patterns/orchestration-framework.md) — PostToolUse auto-format hook, Stop hook for session-end checks
- [Official Documentation](https://code.claude.com/docs/en/hooks-guide)
