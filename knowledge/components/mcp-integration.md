---
id: mcp-integration
title: MCP Integration
category: components
tags: [mcp, tools, external, api, servers, transport, oauth, resources, channels]
summary: Model Context Protocol integration — connecting Claude Code to external tools, databases, and APIs via stdio, HTTP, and SSE transports.
depends_on: [memory-claudemd]
related: [agent-skills, hooks]
complexity: intermediate
last_updated: 2026-04-05
estimated_tokens: 1400
source: https://code.claude.com/docs/en/mcp
confidence: A
review_by: 2026-07-05
---

# MCP Integration

> **Wrapper file** — CAB-specific patterns and quick reference only. Full documentation: [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)

MCP connects Claude Code to external tools, databases, and APIs through a standardized protocol. Servers expose tools that Claude can invoke during a session.

---

## Server Types

### stdio (Local processes)

Local CLI tools communicating over stdin/stdout. `--` separates CLI flags from the server command. Don't log to stdout — use stderr.

```json
{
  "mcpServers": {
    "local-db": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@company/db-mcp-server"],
      "env": { "DATABASE_URL": "${DATABASE_URL}" }
    }
  }
}
```

```bash
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub --dsn "postgresql://..."
# Windows: wrap with cmd /c
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```

### HTTP / Streamable HTTP (Remote servers)

Recommended for cloud services and remote APIs. Uses `type: "http"` with a URL endpoint. Supports static `headers` and dynamic `headersHelper` (shell command outputting JSON).

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": { "Authorization": "Bearer ${GITHUB_TOKEN}" }
    },
    "dynamic-auth": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headersHelper": "/opt/bin/get-mcp-auth-headers.sh"
    }
  }
}
```

`headersHelper` runs in a shell with a **10-second timeout**. Env vars `CLAUDE_CODE_MCP_SERVER_NAME` and `CLAUDE_CODE_MCP_SERVER_URL` are set during execution. Dynamic headers override static `headers` with the same name.

### SSE (Legacy)

Server-Sent Events transport. **Deprecated** — migrate to HTTP.

```bash
claude mcp add --transport sse legacy-server https://old.example.com/sse
```

---

## Configuration Scopes

| Scope       | Location                        | Visibility                | Flag                      | Notes                      |
| ----------- | ------------------------------- | ------------------------- | ------------------------- | -------------------------- |
| **Local**   | `~/.claude.json` (project path) | You only, current project | `--scope local` (default) | Formerly called "project"  |
| **Project** | `.mcp.json`                     | Team via git              | `--scope project`         |                            |
| **User**    | `~/.claude.json` mcpServers     | You only, all projects    | `--scope user`            | Formerly called "global"   |
| **Managed** | `managed-mcp.json`              | Enterprise-deployed       | N/A                       | See Enterprise section     |

Environment variable expansion: `${VAR}` and `${VAR:-default}` supported in all config files.

---

## Permissions

**`alwaysAllow` is not a feature** — use `permissions.allow` with the `mcp__server__tool` pattern instead.

In `.claude/settings.json` or `settings.local.json`:

```json
{
  "permissions": {
    "allow": ["mcp__github__create_issue", "mcp__github__list_prs", "mcp__db__query"],
    "deny": ["mcp__db__drop_table"]
  }
}
```

Pattern: `mcp__{serverName}__{toolName}`. Wildcard supported — `mcp__puppeteer__*` matches all tools from the puppeteer server.

---

## Timeout & Authentication

**Timeout**: No per-server timeout in config. Use `MCP_TIMEOUT=10000 claude` env var for startup timeout.

**OAuth 2.0**: Add server, run `/mcp`, follow browser prompts. Tokens stored securely and refreshed automatically.

**Static headers**: Pass via `--header` CLI flag or `headers`/`headersHelper` config keys.

---

## Advanced Features

### Resources via @ Syntax

Reference MCP-exposed resources in prompts: `@server:protocol://resource/path`

```text
@github:issue://123
@db:schema://public/users
```

### Channels

MCP-backed message injection for continuous context streams: `claude --channels`

### Elicitation

MCP servers can request structured user input during tool execution — the runtime prompts the user and returns the response to the server.

### MCP Registry API

The registry at `https://api.anthropic.com/mcp-registry/v0/servers` is an **internal component** used by the Claude Code UI, not a documented public endpoint. It supports cursor-based pagination (`cursor`, `limit`) and filtering (`version`, `visibility`). AI agents should fetch `https://api.anthropic.com/mcp-registry/docs` for registry information.

### MCP Tool Search

Tool search defers MCP tool definitions until needed, keeping context usage low. Server instructions are truncated at 2 KB. Controlled by `ENABLE_TOOL_SEARCH` env var:

| Value      | Behavior                                                   |
| ---------- | ---------------------------------------------------------- |
| *(unset)*  | Default — tools deferred automatically                     |
| `true`     | Force tool search on                                       |
| `auto`     | Auto-enable when tool count exceeds internal threshold     |
| `auto:<N>` | Auto-enable when tool count exceeds `N`                    |
| `false`    | Disable — all tool definitions loaded into context upfront |

Requires Sonnet 4+ or Opus 4+.

### MCP Prompts as Commands

MCP servers can expose prompts available as slash commands: `/mcp__servername__promptname`. Arguments are passed space-separated.

### Claude Code as MCP Server

Expose Claude Code itself as an MCP server: `claude mcp serve`

---

## Enterprise Configuration

### Managed MCP

Deploy `managed-mcp.json` to system path (users cannot add/modify servers when this exists):

- macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- Linux: `/etc/claude-code/managed-mcp.json`
- Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

### Allowlists / Denylists

`allowedMcpServers` and `deniedMcpServers` in managed settings control which servers users can add:

```json
{
  "allowedMcpServers": [{ "serverName": "github" }, { "serverUrl": "https://mcp.company.com/*" }],
  "deniedMcpServers": [{ "serverUrl": "https://*.untrusted.com/*" }]
}
```

---

## Output Limits

| Parameter         | Value                         |
| ----------------- | ----------------------------- |
| Warning threshold | 10,000 tokens                 |
| Default max       | 25,000 tokens                 |
| Override          | `MAX_MCP_OUTPUT_TOKENS=50000` |

---

## CAB-Specific Patterns

### MCP Wrapping Philosophy

> **Wrap, don't rewrite** — expose existing tools via MCP; preserve working code.

MCP servers are the integration layer between Claude Code and external systems. Design them as thin wrappers around existing APIs and CLIs, not as reimplementations.

### When to Use MCP vs Skills

| Use Case                     | Choose               | Rationale                                            |
| ---------------------------- | -------------------- | ---------------------------------------------------- |
| External API/database access | **MCP**              | Standardized tool protocol, reusable across projects |
| Complex multi-step reasoning | **Skill**            | SKILL.md provides structured context + instructions  |
| Stateful session workflows   | **Skill**            | Skills maintain session context via filesystem       |
| Simple data retrieval        | **MCP**              | Single tool call, no orchestration needed            |
| Domain-specific analysis     | **Skill**            | Rich prompt engineering, progressive disclosure      |
| Shared team tooling          | **MCP** (.mcp.json)  | Committed to repo, auto-available for team           |

### Plugin MCP Servers

Plugins bundle MCP servers in `.mcp.json` using `${CLAUDE_PLUGIN_ROOT}` for paths. Plugin servers start automatically when the plugin is enabled.

---

## See Also

- [Claude Code MCP docs](https://code.claude.com/docs/en/mcp) — Full reference
- [MCP Protocol spec](https://modelcontextprotocol.io/introduction) — Protocol details
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) | [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Agent Skills](agent-skills.md) — Model-invoked capabilities (compare with MCP)
