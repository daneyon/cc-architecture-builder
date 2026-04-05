---
id: distributable-plugin
title: Distributable Plugin Project
category: schemas
tags: [plugin, distributable, marketplace, schema]
summary: CAB wrapper for CC plugin system — directory structure, plugin.json schema, CLI commands, and CAB-specific patterns.
depends_on: [executive-summary, global-user-config]
related: [marketplace, agent-skills, subagents]
complexity: intermediate
confidence: A
review_by: 2026-07-05
last_updated: 2026-04-05
estimated_tokens: 900
source: https://code.claude.com/docs/en/plugins, https://code.claude.com/docs/en/plugins-reference
---

# Distributable Plugin Project

> **Wrapper philosophy**: This file documents CAB-specific structure and patterns. For native CC plugin behavior, see the [Plugins guide](https://code.claude.com/docs/en/plugins) and [Plugins reference](https://code.claude.com/docs/en/plugins-reference).

## Directory Structure

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json            # Required: manifest (only file in this dir)
│
├── CLAUDE.md                  # Project system instructions
├── settings.json              # Default settings (only `agent` key supported)
├── .mcp.json                  # MCP server configurations
├── .lsp.json                  # LSP server configurations
│
├── commands/                  # Slash commands (markdown files)
├── skills/                    # Agent Skills (name/SKILL.md structure)
├── agents/                    # Subagent definitions (markdown)
├── hooks/                     # hooks.json event handlers
│   └── hooks.json
├── bin/                       # Executables added to Bash tool PATH
├── output-styles/             # Custom output style definitions
│
├── scripts/                   # Hook/utility scripts
├── knowledge/                 # Domain knowledge (for Claude)
│   └── INDEX.md
├── docs/                      # Human documentation
├── LICENSE
├── README.md
└── CHANGELOG.md
```

**Critical**: All component directories go at plugin root, never inside `.claude-plugin/`.

## plugin.json Schema

### Required

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | Unique kebab-case identifier; doubles as skill namespace (`name:skill`) |

### Metadata (optional)

| Field | Type | Description |
| --- | --- | --- |
| `version` | string | Semver (e.g. `"1.0.0"`) |
| `description` | string | Brief purpose |
| `author` | object | `{name, email?, url?}` |
| `homepage` | string | Documentation URL |
| `repository` | string | Source code URL |
| `license` | string | SPDX identifier |
| `keywords` | array | Discovery tags |

### Component Paths (optional)

Override default discovery locations. Custom paths **replace** defaults for `commands`, `agents`, `skills`, `outputStyles`. All paths relative to plugin root, prefixed with `./`.

| Field | Type | Default Location |
| --- | --- | --- |
| `commands` | string or array | `commands/` |
| `agents` | string or array | `agents/` |
| `skills` | string or array | `skills/` |
| `hooks` | string, array, or object | `hooks/hooks.json` |
| `mcpServers` | string, array, or object | `.mcp.json` |
| `lspServers` | string, array, or object | `.lsp.json` |
| `outputStyles` | string or array | `output-styles/` |

### userConfig

Declares values prompted at plugin enable time. Available as `${user_config.KEY}` in MCP/LSP configs, hook commands, and (non-sensitive only) skill/agent content. Exported as `CLAUDE_PLUGIN_OPTION_<KEY>` env vars to subprocesses.

```json
{
  "userConfig": {
    "api_endpoint": { "description": "Team API endpoint", "sensitive": false },
    "api_token": { "description": "API auth token", "sensitive": true }
  }
}
```

- **Non-sensitive**: stored in `settings.json` under `pluginConfigs[<id>].options`
- **Sensitive**: stored in system keychain (fallback: `~/.claude/.credentials.json`); ~2 KB total limit shared with OAuth

### channels

Declares MCP-backed message injection channels (Telegram, Slack, Discord style). Each channel binds to an MCP server the plugin provides.

```json
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": { "description": "Telegram bot token", "sensitive": true },
        "owner_id": { "description": "Telegram user ID", "sensitive": false }
      }
    }
  ]
}
```

`server` must match a key in the plugin's `mcpServers`. Per-channel `userConfig` uses the same schema as the top-level field.

## Environment Variables

| Variable | Purpose |
| --- | --- |
| `${CLAUDE_PLUGIN_ROOT}` | Absolute path to plugin install dir. Changes on update — do not write persistent state here. |
| `${CLAUDE_PLUGIN_DATA}` | Persistent data dir (`~/.claude/plugins/data/{id}/`). Survives updates; deleted on uninstall (unless `--keep-data`). Use for `node_modules`, venvs, caches. |

Both are substituted inline in skill/agent content, hook commands, MCP/LSP configs, and exported to subprocesses.

## Plugin Namespacing

All plugin components are namespaced: `plugin-name:skill-name`. This prevents conflicts across plugins. The namespace prefix is the `name` field from `plugin.json`.

## settings.json (Plugin-Level)

Only the `agent` key is supported. Activates a plugin agent as the main thread:

```json
{ "agent": "security-reviewer" }
```

## Plugin CLI Commands

> Full details: [Plugins reference — CLI commands](https://code.claude.com/docs/en/plugins-reference#cli-commands-reference)

| Command | Description |
| --- | --- |
| `claude plugin install <plugin> [-s scope]` | Install from marketplace. Scope: `user` (default), `project`, `local` |
| `claude plugin uninstall <plugin> [-s scope] [--keep-data]` | Remove plugin. `--keep-data` preserves `${CLAUDE_PLUGIN_DATA}` |
| `claude plugin enable <plugin> [-s scope]` | Enable disabled plugin |
| `claude plugin disable <plugin> [-s scope]` | Disable without uninstalling |
| `claude plugin update <plugin> [-s scope]` | Update to latest. Scope includes `managed` |

## Installation Scopes

| Scope | Settings File | Use Case |
| --- | --- | --- |
| `user` | `~/.claude/settings.json` | Personal, all projects (default) |
| `project` | `.claude/settings.json` | Team-shared via git |
| `local` | `.claude/settings.local.json` | Project-specific, gitignored |
| `managed` | Managed settings | Admin-controlled (update only) |

## Plugin Caching

Marketplace plugins are copied to `~/.claude/plugins/cache` (not used in-place). Implications:

- Paths outside plugin dir (`../shared-utils`) break after install
- Symlinks within the plugin dir are followed during copy
- Use `--plugin-dir ./my-plugin` for local dev (bypasses cache)

## Marketplace Source Types

> Full details: [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)

| Source | Fields | Notes |
| --- | --- | --- |
| Relative path | `"./plugins/my-plugin"` | Within marketplace repo |
| `github` | `repo`, `ref?`, `sha?` | GitHub repos |
| `url` | `url`, `ref?`, `sha?` | Any git URL |
| `git-subdir` | `url`, `path`, `ref?`, `sha?` | Sparse clone of monorepo subdir |
| `npm` | `package`, `version?`, `registry?` | npm registry |

## Managed Plugin Controls

> Full details: [Settings — Plugin settings](https://code.claude.com/docs/en/settings)

| Setting | Scope | Purpose |
| --- | --- | --- |
| `strictKnownMarketplaces` | Managed only | Allowlist of marketplace sources users can add. Empty `[]` = lockdown |
| `blockedMarketplaces` | Managed only | Blocklist checked before download; blocked sources never touch filesystem |
| `pluginTrustMessage` | Managed only | Custom message appended to plugin trust warning before installation |
| `extraKnownMarketplaces` | Any | Pre-register marketplaces; prompts team on folder trust |

## CAB-Specific Patterns

### How CAB Structures Its Own Plugin

CAB itself is a plugin. Its structure demonstrates a knowledge-heavy plugin pattern:

```text
cc-architecture-builder/
├── .claude-plugin/plugin.json
├── CLAUDE.md                    # Project instructions + command registry
├── knowledge/                   # Atomized KB (primary value)
│   └── INDEX.md
├── skills/                      # Builder skills
├── agents/                      # Specialist subagents
├── commands/                    # User-facing slash commands
├── templates/                   # Scaffolding templates
└── notes/                       # State management (TODO, progress, lessons-learned)
```

### Distribution Checklist

1. `plugin.json` — name, version, description, keywords
2. `README.md` — installation, usage, prerequisites
3. `LICENSE` — required for marketplace
4. `CHANGELOG.md` — version history
5. `.gitignore` — exclude `node_modules/`, `.env`, credentials
6. Test locally: `claude --plugin-dir ./my-plugin`
7. Validate: `claude plugin validate .`

### Scaffolding

```bash
/init-plugin my-plugin
```

Creates directory structure, generates `plugin.json`, template `CLAUDE.md`, `.gitignore`, and initializes a private git repo.

## See Also

- [Global User Config](global-user-config.md) — Personal configuration schema
- [Marketplace](../distribution/marketplace.md) — Distribution and team setup
- [Knowledge Base Structure](../components/knowledge-base-structure.md) — KB organization
- [Official Plugin Guide](https://code.claude.com/docs/en/plugins) — Native CC documentation
- [Official Plugin Reference](https://code.claude.com/docs/en/plugins-reference) — Complete technical spec
