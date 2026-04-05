---
id: plugin-persistent-data
title: Plugin Persistent Data Patterns
category: components
tags: [plugin, persistent-data, CLAUDE_PLUGIN_DATA, CLAUDE_PLUGIN_ROOT, lifecycle]
summary: Patterns for managing plugin persistent data — CLAUDE_PLUGIN_DATA vs CLAUDE_PLUGIN_ROOT lifecycle, dependency installation, and data management across updates/uninstalls.
depends_on: [distributable-plugin]
related: [hooks, mcp-integration, lsp-integration]
complexity: intermediate
last_updated: 2026-04-05
estimated_tokens: 700
source: https://code.claude.com/docs/en/plugins-reference
confidence: A
review_by: 2026-07-05
revision_note: "v1.0 — NEW KB card for T5-04."
---

# Plugin Persistent Data Patterns

> **Official docs**: [Plugins reference](https://code.claude.com/docs/en/plugins-reference) — environment variables, data lifecycle, dependency installation patterns.

## Overview

Plugins operate with two path contexts that have fundamentally different lifecycles. Understanding this distinction is critical for any plugin that manages state, installs dependencies, or caches data.

---

## Two Path Variables

| Variable | Resolves To | Survives Updates | Purpose |
|----------|-------------|-----------------|---------|
| `CLAUDE_PLUGIN_ROOT` | Plugin installation directory (in `~/.claude/plugins/cache/`) | **No** — replaced on every update | Reference bundled scripts, configs, assets |
| `CLAUDE_PLUGIN_DATA` | `~/.claude/plugins/data/{id}/` | **Yes** — persists across versions | Store dependencies, caches, generated files, mutable state |

The `{id}` is derived from the plugin identifier with non-alphanumeric characters (except `_-`) replaced by `-`. Example: `formatter@my-marketplace` → `formatter-my-marketplace`.

Both variables are:
- Substituted inline in skill/agent content, hook commands, MCP/LSP server configs
- Exported as environment variables to all subprocesses (hooks, MCP servers, LSP servers)

---

## Data Lifecycle

| Event | CLAUDE_PLUGIN_ROOT | CLAUDE_PLUGIN_DATA |
|-------|-------------------|-------------------|
| **Install** | Created (copied to cache) | Created on first reference |
| **Update** | **Replaced** with new version | Unchanged |
| **Disable** | Stays in cache | Unchanged |
| **Enable** | Re-activated from cache | Unchanged |
| **Uninstall (not last scope)** | Removed from that scope's settings | Unchanged |
| **Uninstall (last scope, default)** | Deleted from cache | **Deleted** (prompted first) |
| **Uninstall (last scope, --keep-data)** | Deleted from cache | **Preserved** |

**Multi-scope note**: Plugins can be installed in multiple scopes (`user`, `project`, `local`). Data is only deleted when uninstalling from the **last** remaining scope.

---

## Dependency Installation Pattern

The canonical pattern uses a `SessionStart` hook that compares the bundled manifest against a copy in the data directory — handles both first-run and dependency-changing updates:

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
      }]
    }]
  }
}
```

**How it works**:
1. `diff` exits nonzero when the stored copy is missing OR differs → covers first run and updates
2. On mismatch: copies manifest to data dir, runs `npm install`
3. If install fails: removes copied manifest so next session retries

### Referencing Installed Dependencies

Scripts bundled in `CLAUDE_PLUGIN_ROOT` reference persisted `node_modules` via environment variables:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": {
        "NODE_PATH": "${CLAUDE_PLUGIN_DATA}/node_modules"
      }
    }
  }
}
```

---

## Common Data Directory Uses

| Use Case | Pattern |
|----------|---------|
| **Node.js dependencies** | `npm install` in `CLAUDE_PLUGIN_DATA`, reference via `NODE_PATH` |
| **Python virtual environments** | `python -m venv ${CLAUDE_PLUGIN_DATA}/venv` |
| **Compiled binaries** | Build once, cache in data dir, check version on session start |
| **Generated caches** | SQLite DBs, search indexes, processed data |
| **Plugin state** | Configuration files, usage counters, session history |

---

## Important Caveats

- **Data dir is auto-created** only when `CLAUDE_PLUGIN_DATA` is first referenced — checking directory existence alone is **not sufficient** to detect when an update changes dependencies
- **Manifest comparison** is the reliable pattern — always `diff` the bundled manifest against the stored copy
- **Path traversal blocked** — installed plugins cannot reference files outside their directory (`../shared-utils` breaks after marketplace install)
- **Symlinks honored** — symlinks within the plugin directory are followed during the cache copy process
- **~2 KB shared limit** for sensitive `userConfig` values stored in system keychain (shared with OAuth tokens)
- **`/plugin` UI** shows data directory size before deletion on uninstall

---

## CAB Recommendation

For CAB-structured plugins:
1. Use `SessionStart` hooks for dependency management (not manual instructions)
2. Store all mutable state in `CLAUDE_PLUGIN_DATA` — never write to `CLAUDE_PLUGIN_ROOT`
3. Include a `README.md` section documenting what data the plugin stores and approximate size
4. Test the full lifecycle: install → use → update → uninstall (both with and without `--keep-data`)

## See Also

- [Distributable Plugin](../schemas/distributable-plugin.md) — Plugin structure and plugin.json schema
- [Hooks](hooks.md) — SessionStart hooks for dependency installation
- [MCP Integration](mcp-integration.md) — MCP servers that reference plugin data
- [LSP Integration](lsp-integration.md) — LSP servers with plugin data paths
- [Official Plugins Reference](https://code.claude.com/docs/en/plugins-reference) — Authoritative source
