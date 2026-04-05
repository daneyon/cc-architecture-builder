---
id: lsp-integration
title: LSP Integration
category: components
tags: [lsp, language-server, diagnostics, code-intelligence, plugins]
summary: LSP integration gives Claude real-time code intelligence — diagnostics, navigation, and type information during edits. Configured via .lsp.json or plugin.json.
depends_on: [distributable-plugin]
related: [mcp-integration, hooks, output-styles]
complexity: intermediate
last_updated: 2026-04-05
estimated_tokens: 650
source: https://code.claude.com/docs/en/plugins, https://code.claude.com/docs/en/plugins-reference
confidence: A
review_by: 2026-07-05
revision_note: "v1.0 — NEW KB card for T5-06."
---

# LSP Integration

> **Official docs**: LSP is documented within the [Plugins guide](https://code.claude.com/docs/en/plugins) and [Plugins reference](https://code.claude.com/docs/en/plugins-reference). No dedicated LSP page exists.

## Overview

LSP (Language Server Protocol) integration gives Claude **real-time code intelligence** while working on a codebase:

- **Instant diagnostics**: Errors and warnings appear immediately after each edit
- **Code navigation**: Go-to-definition, find-references, hover information
- **Type awareness**: Type information and documentation for code symbols

This means Claude detects type errors, missing imports, and other issues as it writes code — not only when running the compiler or linter.

---

## Configuration

### Option A: Standalone `.lsp.json`

Place at plugin root (same level as `.claude-plugin/`):

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

### Option B: Inline in `plugin.json`

```json
{
  "name": "my-plugin",
  "lspServers": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"],
      "extensionToLanguage": {
        ".ts": "typescript",
        ".tsx": "typescriptreact"
      }
    }
  }
}
```

Top-level keys are language server names. Each maps to a configuration object.

---

## Configuration Schema

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `command` | string | LSP binary to execute (must be in `$PATH`) |
| `extensionToLanguage` | object | Maps file extensions to language identifiers |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `args` | string[] | Command-line arguments for the LSP server |
| `transport` | string | Communication transport: `stdio` (default) or `socket` |
| `env` | object | Environment variables for the server process |
| `initializationOptions` | object | Options passed during LSP initialization |
| `settings` | object | Settings via `workspace/didChangeConfiguration` |
| `workspaceFolder` | string | Workspace folder path |
| `startupTimeout` | number | Max startup wait (ms) |
| `shutdownTimeout` | number | Max graceful shutdown wait (ms) |
| `restartOnCrash` | boolean | Auto-restart on crash |
| `maxRestarts` | number | Max restart attempts before giving up |

---

## Pre-Built LSP Plugins

Official marketplace provides ready-made LSP plugins:

| Plugin | Language Server | Install Prerequisite |
|--------|----------------|---------------------|
| `pyright-lsp` | Pyright (Python) | `pip install pyright` or `npm install -g pyright` |
| `typescript-lsp` | TypeScript LS | `npm install -g typescript-language-server typescript` |
| `rust-lsp` | rust-analyzer | See rust-analyzer installation docs |

**Recommendation**: Use marketplace LSP plugins for supported languages rather than building custom ones.

---

## Key Operational Notes

- **Plugins provide configuration, not the binary** — users must install the language server separately. Missing binary → `Executable not found in $PATH` in `/plugin` Errors tab.
- **Variable substitution**: `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, and `${user_config.KEY}` are available in LSP configs.
- **Reload**: LSP servers are reloaded when you run `/reload-plugins`.
- **Debug**: Use `claude --debug` to see LSP initialization details.
- **Caching**: Marketplace plugins are copied to `~/.claude/plugins/cache/`; path traversal outside plugin root is blocked.

---

## CAB Patterns

### When to Use LSP vs. Hook-Based Linting

| Approach | Strengths | Limitations |
|----------|-----------|-------------|
| **LSP** | Real-time diagnostics during edits, type-aware, rich navigation | Requires binary install, language-specific |
| **PostToolUse hook** (e.g., `ruff format`) | Simple setup, works with any CLI tool, fire-and-forget | Post-hoc only, no navigation, no type info |

For comprehensive code quality: use both. LSP catches type errors in real-time; hooks enforce formatting and style rules after writes.

### LSP in Plugin Distribution

Bundle `.lsp.json` with installation instructions in `README.md` specifying prerequisite binaries. Consider a `SessionStart` hook that validates the LSP binary exists:

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "command -v gopls >/dev/null || echo 'Warning: gopls not found. Install with: go install golang.org/x/tools/gopls@latest'"
      }]
    }]
  }
}
```

## See Also

- [MCP Integration](mcp-integration.md) — External tool connections (complementary to LSP)
- [Hooks](hooks.md) — Event-driven automation (PostToolUse linting)
- [Distributable Plugin](../schemas/distributable-plugin.md) — Plugin structure and .lsp.json placement
- [Official Plugins Reference](https://code.claude.com/docs/en/plugins-reference) — Full LSP schema
