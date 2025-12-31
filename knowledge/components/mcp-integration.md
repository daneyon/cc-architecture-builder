---
id: mcp-integration
title: MCP Integration
category: components
tags: [mcp, tools, external, api, servers, transport]
summary: Complete guide to Model Context Protocol integration - connecting Claude Code to external tools, databases, and APIs.
depends_on: [memory-claudemd]
related: [agent-skills, hooks]
complexity: intermediate
last_updated: 2025-12-23
estimated_tokens: 1100
source: https://code.claude.com/docs/en/mcp
---

# MCP Integration

## Overview

Model Context Protocol (MCP) connects Claude Code to external tools, databases, and APIs through a standardized interface.

**Source**: [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)

> **Quality Measure**: The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks, not just API coverage.

---

## What You Can Do with MCP

- Implement features from issue trackers (JIRA, GitHub)
- Analyze monitoring data (Sentry, Statsig)
- Query databases (PostgreSQL, etc.)
- Integrate designs (Figma)
- Automate workflows (Gmail, Slack)

---

## Transport Types

| Type | Best For | Notes |
|------|----------|-------|
| **HTTP** | Remote servers, cloud services | Recommended for production |
| **stdio** | Local integrations, CLI tools | Don't log to stdout (use stderr) |
| **SSE** | Legacy | Deprecated |

---

## Installing MCP Servers

### HTTP Server (Recommended for remote)

```bash
claude mcp add --transport http <name> <url>

# Example: Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# With authentication
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### stdio Server (Local)

```bash
claude mcp add --transport stdio <name> -- <command> [args...]

# Example: Airtable
claude mcp add --transport stdio airtable --env AIRTABLE_API_KEY=YOUR_KEY \
  -- npx -y airtable-mcp-server
```

**Note**: The `--` separates Claude CLI flags from the server command.

**Windows Users**: Use `cmd /c` wrapper:
```bash
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```

---

## MCP Scopes

| Scope | Location | Visibility | Flag |
|-------|----------|------------|------|
| **Local** | `~/.claude.json` (project path) | Just you, current project | `--scope local` (default) |
| **Project** | `.mcp.json` | Team via git | `--scope project` |
| **User** | `~/.claude.json` | All your projects | `--scope user` |

---

## Configuration File (.mcp.json)

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "local-db": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@company/db-mcp-server"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

### Environment Variable Expansion

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

Supported syntax:
- `${VAR}` — Expand variable
- `${VAR:-default}` — Use default if not set

---

## Managing Servers

```bash
# List all servers
claude mcp list

# Get details
claude mcp get github

# Remove server
claude mcp remove github

# Check status (in Claude Code)
/mcp
```

---

## Authentication

Many cloud MCP servers require OAuth 2.0:

1. Add the server
2. Run `/mcp` in Claude Code
3. Follow browser prompts to login

Tokens are stored securely and refreshed automatically.

---

## Plugin MCP Servers

Plugins can bundle MCP servers in `.mcp.json` or inline in `plugin.json`:

```json
{
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

Plugin servers start automatically when plugin is enabled.

---

## MCP Resources and Prompts

### Resources (@ mentions)

Reference MCP resources like files:
```
> Can you analyze @github:issue://123?
```

### Prompts (slash commands)

MCP prompts become available as `/mcp__servername__promptname`:
```
> /mcp__github__list_prs
> /mcp__github__pr_review 456
```

---

## Server Naming Conventions

| Language | Format | Example |
|----------|--------|---------|
| **Python** | `{service}_mcp` | `slack_mcp`, `github_mcp` |
| **TypeScript** | `{service}-mcp-server` | `slack-mcp-server` |

### Tool Naming

```
# Format: {service}_{action}_{resource}
slack_send_message      # Not: send_message
github_create_issue     # Not: create_issue
```

**Why prefix?** Prevents tool name conflicts across servers.

---

## Enterprise Configuration

### Option 1: Managed MCP (Exclusive Control)

Deploy `managed-mcp.json` to system path:
- macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- Linux: `/etc/claude-code/managed-mcp.json`
- Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

Users cannot add/modify servers when this exists.

### Option 2: Allowlists/Denylists

In managed settings:
```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverUrl": "https://mcp.company.com/*" }
  ],
  "deniedMcpServers": [
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

---

## Output Limits

- Warning threshold: 10,000 tokens
- Default max: 25,000 tokens
- Configure with: `MAX_MCP_OUTPUT_TOKENS=50000`

---

## Practical Examples

### GitHub Integration
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
# Then: /mcp to authenticate
```

### PostgreSQL Database
```bash
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://user:pass@host:5432/db"
```

---

## See Also

- [MCP Introduction](https://modelcontextprotocol.io/introduction)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Agent Skills](agent-skills.md) — Model-invoked capabilities
