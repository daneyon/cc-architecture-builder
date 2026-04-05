---
id: global-user-config
title: Global User Configuration (Schema 1)
category: schemas
tags: [schema-1, global, user-config, settings, permissions, sandbox, managed, worktree]
summary: Schema 1 — personal baseline at ~/.claude/. Settings hierarchy (5 levels), permission system, sandbox, model config, hooks, worktree settings, and managed delivery. CAB-specific patterns for orchestrator setup and effort tuning.
depends_on: [executive-summary, architecture-philosophy]
related: [distributable-plugin, memory-claudemd, orchestration-framework, hooks]
complexity: intermediate
last_updated: 2026-04-05
estimated_tokens: 1300
source: https://code.claude.com/docs/en/settings
confidence: A
review_by: 2026-07-05
---

# Global User Configuration (Schema 1)

> **Official docs**: [code.claude.com/docs/en/settings](https://code.claude.com/docs/en/settings) — authoritative reference for all 60+ settings fields, JSON schemas, and configuration mechanics.
> This file documents **CAB-specific patterns, structural guidance, and behavioral notes** only.

---

## Directory Structure

```
~/.claude/
├── CLAUDE.md                     # Personal baseline (always loaded)
├── CLAUDE.local.md               # Machine-specific personal overrides (gitignored equivalent)
├── settings.json                 # User-level settings (precedence level 5)
├── keybindings.json              # Custom keyboard shortcuts
├── rules/                        # Personal modular rules (always loaded)
│   ├── preferences.md
│   └── workflows.md
├── skills/                       # Personal skills (cross-project)
│   └── research-methodology/
│       └── SKILL.md
├── agents/                       # Personal agents (orchestrator + specialists)
│   ├── orchestrator.md
│   └── general-researcher.md
├── output-styles/                # Custom output style definitions
│   └── my-style.md
├── projects/                     # Auto-managed per-project state
│   └── <project-path>/
│       └── memory/               # Auto memory (MEMORY.md + topic files)
│           ├── MEMORY.md
│           └── <topic>.md
├── plugins/                      # Plugin runtime data
│   ├── cache/                    # Installed plugin copies (replaced on update)
│   └── data/                     # Persistent plugin data (survives updates)
│       └── <plugin-id>/
├── plans/                        # Saved plans from plan mode
├── work/                         # Working state (IPC, worktrees)
│   └── ipc/                      # Agent Teams mailbox files
└── shared-knowledge/             # Cross-project reference materials (optional)
    └── frameworks/
```

---

## Settings Hierarchy (5 Levels)

Settings resolve top-down; higher precedence wins on conflict.

| Level | Source | Location / Mechanism | Precedence |
| ----- | ------ | -------------------- | ---------- |
| 1 (highest) | **Managed** | MDM/plist (macOS), registry (Windows), `/etc/claude/` drop-in dir | Enterprise override; users cannot change |
| 2 | **CLI args** | `--model`, `--permission-mode`, etc. | Per-invocation override |
| 3 | **Local** | `.claude/settings.local.json` in project root | Machine-specific, gitignored |
| 4 | **Project** | `.claude/settings.json` in project root | Shared via git; team baseline |
| 5 (lowest) | **User** | `~/.claude/settings.json` | Personal defaults for all projects |

**Merge behavior**: Objects merge recursively. Arrays (e.g., `permissions.allow`) concatenate across levels. Deny rules at any level take precedence over allow rules at the same or lower level.

---

## Settings Categories

CC exposes 60+ settings fields. Below is the CAB-relevant grouping; see official docs for exhaustive field list.

### Core Settings

| Field | Type | Description |
| ----- | ---- | ----------- |
| `model` | string | Default model alias: `"sonnet"`, `"opus"`, `"haiku"` |
| `agent` | string | Default agent for all sessions (e.g., `"orchestrator"`) |
| `reasoningEffort` | string | Thinking budget: `"low"`, `"medium"`, `"high"` |
| `verbose` | boolean | Extra status output during tool execution |
| `theme` | string | Terminal theme: `"dark"`, `"light"`, `"light-daltonized"`, `"dark-daltonized"` |

**Effort levels**: Official docs specify three values (`low`, `medium`, `high`). A `"max"` value has been observed in practice but is not documented; treat as undocumented behavior subject to change.

### Permission Modes

Set via `--permission-mode` CLI flag or `permissions.defaultMode`:

| Mode | Behavior |
| ---- | -------- |
| `default` | Prompt for each non-allowed tool use |
| `acceptEdits` | Auto-accept file edits; prompt for everything else |
| `plan` | Read-only — cannot execute tools that modify state |
| `auto` | AI classifier decides; applies autoMode rules (see below) |
| `dontAsk` | Accept all except deny-listed |
| `bypassPermissions` | Skip all permission checks (requires explicit flag) |

### Fine-Grained Permissions

Three arrays in `permissions`: `allow`, `ask`, `deny`. Each entry uses `Tool(specifier)` syntax:

```json
{
  "permissions": {
    "allow": ["Read", "Write", "Edit", "Bash(git *)", "Bash(npm *)", "mcp__*"],
    "ask": ["Bash(curl *)"],
    "deny": ["Bash(rm -rf /)", "Bash(sudo *)"]
  }
}
```

**Specifier patterns**: Bare tool name (`Read`), glob match (`Bash(git *)`), MCP wildcard (`mcp__server_*`). Deny always wins over allow at the same level.

### Auto Mode Configuration

When `permissions.defaultMode` is `"auto"`, an AI classifier evaluates each tool call against three rule arrays:

```json
{
  "permissions": {
    "defaultMode": "auto",
    "autoMode": {
      "environment": ["This is a development machine", "All code is version-controlled"],
      "allow": ["Reading any file", "Running git commands", "Running tests"],
      "soft_deny": ["Deleting files outside project", "Network requests to unknown hosts"]
    }
  }
}
```

| Array | Purpose |
| ----- | ------- |
| `environment` | Context strings fed to classifier (machine role, safety constraints) |
| `allow` | Natural-language rules for auto-approval |
| `soft_deny` | Rules where classifier should prompt the user |

> **Behavioral note** (confidence: B): Auto mode uses a 2-stage AI classifier. The system strips rules it classifies as dangerous. After 3 consecutive user denials, auto mode reverts to `default` mode for the remainder of the session. This is observable behavior, not a committed API contract.

### Model Configuration

| Field | Type | Description |
| ----- | ---- | ----------- |
| `availableModels` | string[] | Restrict which models can be selected (e.g., `["sonnet", "haiku"]`) |
| `modelOverrides` | object | Map model aliases to provider-specific IDs |

```json
{
  "availableModels": ["sonnet", "opus"],
  "modelOverrides": {
    "sonnet": "us.anthropic.claude-sonnet-4-20250514",
    "opus": "arn:aws:bedrock:us-east-1:123456:inference-profile/opus"
  }
}
```

Use `modelOverrides` for Bedrock ARNs, Vertex AI model IDs, or pinning to specific model versions.

### Sandbox Configuration

Sandbox restricts filesystem and network access. 15+ settings control filesystem allow/deny paths, network domain filtering, and proxy port configuration. See official docs for full schema.

```json
{
  "sandbox": {
    "filesystem": { "allow": ["/home/user/projects", "/tmp"], "deny": ["/etc", "/var"] },
    "network": { "allowedDomains": ["github.com", "api.anthropic.com"], "deniedDomains": ["*"] }
  }
}
```

CAB recommendation: always configure sandbox for autonomous agents.

### Hooks

Event-driven automation configured in settings.json. See [Hooks](../components/hooks.md) for the full event catalog (26 events, 4 hook types) and configuration syntax.

### Worktree Settings

| Field | Type | Description |
| ----- | ---- | ----------- |
| `symlinkDirectories` | string[] | Directories to symlink (not copy) into worktrees |
| `sparsePaths` | string[] | Paths for sparse checkout in worktrees (large repos) |

### Managed Settings Delivery

Enterprise/team deployment mechanisms (precedence level 1 — overrides everything):

| Platform | Mechanism | Location |
| -------- | --------- | -------- |
| macOS | MDM / plist | `/Library/Managed Preferences/com.anthropic.claude-code.plist` |
| Windows | Registry | `HKLM\SOFTWARE\Policies\Anthropic\ClaudeCode` |
| Linux/all | Drop-in directory | `/etc/claude/*.json` (merged alphabetically) |

Use managed settings for organization-wide policy enforcement: model restrictions, permission baselines, sandbox requirements.

---

## CAB Patterns

### Recommended Global Config (Orchestrator Setup)

```json
{
  "model": "sonnet",
  "agent": "orchestrator",
  "reasoningEffort": "high",
  "permissions": {
    "allow": [
      "Read", "Write", "Edit",
      "Bash(git *)", "Bash(npm *)", "Bash(python *)", "Bash(claude *)"
    ],
    "deny": ["Bash(rm -rf /)", "Bash(sudo *)"]
  }
}
```

Setting `"agent": "orchestrator"` makes the orchestrator default for all sessions — the foundation for autonomous multi-agent operation. `Bash(claude *)` enables subagent spawning without prompts.

### Effort Level Guidance

| Task Type | Recommended Effort | Rationale |
| --------- | ------------------ | --------- |
| Quick edits, simple queries | `low` | Minimal thinking budget, fast response |
| Standard development, code review | `medium` | Balanced speed and depth |
| Architecture decisions, complex debugging | `high` | Full thinking budget for multi-step reasoning |

Override per-session with `--reasoning-effort` CLI flag when the default doesn't fit.

### Project-Level Override Pattern

Use `.claude/settings.json` (level 4) to tighten permissions for specific projects:

```json
{
  "permissions": { "deny": ["Bash(npm publish *)", "Bash(docker push *)"] },
  "sandbox": { "filesystem": { "deny": ["/home/user/.ssh", "/home/user/.aws"] } }
}
```

Project deny rules merge with (and override) user-level allow rules — defense in depth.

---

## Personal Components

Skills in `~/.claude/skills/` and agents in `~/.claude/agents/` are available in ALL projects. Use personal skills for research methodologies, analysis frameworks, and productivity patterns. Use personal agents for cross-domain utilities and workflow automation.

Projects can import personal preferences via `@` imports in CLAUDE.md (e.g., `@~/.claude/shared-preferences/project-preferences.md`). If the import file doesn't exist, CC proceeds without error.

---

## See Also

- [Official Settings Reference](https://code.claude.com/docs/en/settings) — authoritative source for all 60+ fields
- [Distributable Plugin](distributable-plugin.md) — Schema 2 (project-level config)
- [Memory System](../components/memory-claudemd.md) — CLAUDE.md hierarchy and @imports
- [Hooks](../components/hooks.md) — Event-driven automation details
- [Orchestration Framework](../operational-patterns/orchestration/framework.md) — Multi-agent patterns
