---
id: mcp-integration
title: MCP Integration
category: components
tags: [mcp, model-context-protocol, tools, external-services, apis]
summary: Model Context Protocol connections to external tools, databases, and APIs. Extends Claude Code capabilities through standardized tool interfaces.
depends_on: [memory-claudemd]
related: [hooks, knowledge-base-structure]
complexity: intermediate
last_updated: 2025-12-12
estimated_tokens: 700
---

# MCP Integration

## Overview

Model Context Protocol (MCP) connects Claude Code to external tools, databases, and APIs through a standardized interface. MCP servers extend Claude's capabilities beyond filesystem and bash access.

## Key Concepts

| Term | Description |
|------|-------------|
| **MCP Server** | Service providing tools to Claude |
| **Transport** | Communication method (HTTP, SSE, stdio) |
| **Tools** | Actions Claude can invoke via MCP |
| **Resources** | Data Claude can access via MCP |

## File Structure

**Location**: `.mcp.json` at project root

```
project/
├── .mcp.json              # MCP configuration
└── servers/               # Local MCP servers (optional)
    └── custom-server.py
```

## Configuration Format

```json
{
  "mcpServers": {
    "server-name": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

## Server Types

### HTTP (Recommended)

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.github.com/mcp",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    }
  }
}
```

### stdio (Local Processes)

```json
{
  "mcpServers": {
    "local-db": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "db_mcp_server"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

### SSE (Deprecated)

```json
{
  "mcpServers": {
    "legacy-service": {
      "type": "sse",
      "url": "https://mcp.service.com/sse"
    }
  }
}
```

## Environment Variables

MCP configs support variable expansion:

| Syntax | Behavior |
|--------|----------|
| `${VAR}` | Expands to environment variable value |
| `${VAR:-default}` | Uses default if VAR not set |

**Expansion locations**: `command`, `args`, `env`, `url`, `headers`

## Configuration Scopes

| Scope | Location | Visibility |
|-------|----------|------------|
| **Project** | `./.mcp.json` | Current project |
| **User** | `~/.claude/.mcp.json` | All your projects |
| **Plugin** | `plugin/.mcp.json` | When plugin installed |

## Adding MCP Servers

### Via CLI

```bash
# HTTP server
claude mcp add --transport http github https://api.github.com/mcp

# stdio server with env vars
claude mcp add --transport stdio mydb \
  --env DATABASE_URL \
  -- python -m db_server

# List configured servers
claude mcp list

# Remove server
claude mcp remove github
```

### Via Configuration File

Edit `.mcp.json` directly (useful for version-controlled configs).

## Common MCP Servers

| Server | Purpose | Type |
|--------|---------|------|
| GitHub | Repository operations, issues, PRs | HTTP |
| Figma | Design integration | HTTP |
| Notion | Documentation access | HTTP |
| Postgres | Database queries | stdio |
| Filesystem | Extended file operations | stdio |

## Example: GitHub Integration

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.github.com/mcp",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    }
  }
}
```

**Capabilities once connected**:
- Create/manage issues
- Open pull requests
- Search code
- Review commits

## Example: Database Integration

```json
{
  "mcpServers": {
    "project-db": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-postgres"],
      "env": {
        "POSTGRES_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

## Plugin MCP Servers

Plugins can bundle MCP servers:

```json
{
  "mcpServers": {
    "plugin-service": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/service",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  }
}
```

**Behavior**:
- Start automatically when plugin enabled
- Integrate with Claude's tool system
- Configure independently of user MCP servers

## Security Considerations

- Store credentials in environment variables, not config files
- Review MCP server permissions before connecting
- Be cautious with servers that fetch untrusted content
- Enterprise can restrict allowed MCP servers

## Scaling: When to Add MCP

| Scenario | Recommendation |
|----------|----------------|
| Small knowledge base | Filesystem sufficient |
| External APIs | MCP for structured access |
| Databases | MCP for query capability |
| Large KB (100+ files) | MCP with vector search |
| Team tools | MCP for shared integrations |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not connecting | Check `claude mcp list`, verify credentials |
| Tools not appearing | Restart Claude Code after config change |
| Permission denied | Verify environment variables set |
| Timeout errors | Check network, increase timeout |

## See Also

- [Knowledge Base Structure](knowledge-base-structure.md) — When to use MCP for KB
- [Hooks](hooks.md) — Event-driven automation
- [Official MCP Documentation](https://modelcontextprotocol.io/introduction)
- [Claude Code MCP Guide](https://docs.anthropic.com/en/docs/claude-code/mcp)
